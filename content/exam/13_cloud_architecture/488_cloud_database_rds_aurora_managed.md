---
title: "Cloud Database RDS Aurora Managed"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

# 488. 클라우드 데이터베이스 RDS / Aurora 관리형 (Cloud Database RDS & Aurora Managed)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Amazon RDS는 클라우드 상에서 관계형 데이터베이스의 **프로비저닝·패치·백업·HA·모니터링 자동화**를 추상화한 PaaS형 관리형 서비스이고, **Aurora**는 RDS 계열 중에서도 컴퓨팅과 스토리지를 분리하여 **6-way Quorum 기반 분산 스토리지 볼륨(`aurora-volume`)** 위에서 로그 단위 Push 복제와 `Voter`/`Acceptor`로 구성된 합의 모델을 통해 단일 노드처럼 보이는 MySQL/PostgreSQL 호환 엔진을 제공한다.
> 2. **가치**: Aurora는 동일 하드웨어 대비 상용 DB 대비 약 5배, MySQL/PostgreSQL 표준 대비 약 3~5배의 처리량을 제공하며(Percona/Amazon 내부 벤치마크), Replica 추가가 **스토리지 복제 없이** Read Replica EndPoint 확장으로 수초 내 완료되고, RPO 1초 미만·RTO 1분 이내의 Cross-Region DR(Global Database)을 구성 가능하다.
> 3. **판단 포인트**: "**언제 표준 RDS(MySQL/PostgreSQL/Oracle)인가, 언제 Aurora인가, 언제 Aurora Serverless v2인가, 언제 RDS Proxy+Lambda Chassis 패턴인가, 언제 Self-managed on EC2/EKS+ EBS로 회귀하는가**"의 결정 트리와, **Aurora의 비동기 Quorum 복제 특성상 발생하는 Replica Lag·Read-after-Write 일관성·Cross-AZ Latency 비용(쓰기 시 6중 Quorum 4-of-6 commit)** 을 트래픽 프로파일로 환산하는 것이 핵심 판단 포인트다.

---

## Ⅰ. 개요 및 필요성

### 1. 배경: 왜 "관리형"이 필요한가

기존 On-Premise 또는 EC2 Self-managed RDBMS 운영에서는 DBA/Infra 엔지니어가 다음을 직접 수행해야 했다.

- **운영 부담**: MySQL/PostgreSQL/Oracle/MS-SQL 바이너리 설치, OS 커널 파라미터 튜닝(`vm.swappiness`, `dirty_ratio`, XFS/ext4 블록 정렬), 엔진 업그레이드, 보안 패치, CVE 대응
- **HA 직접 설계**: `MHA`, `Orchestrator`, `Patroni`, `MySQL Group Replication`, `Pacemaker + Corosync`, DataGuard, AlwaysOn AG 등 별도 솔루션
- **백업·복구**: `xtrabackup`, `pg_basebackup`, `RMAN`, PITR을 위한 binlog/WAL 아카이빙, S3로의 전송 및 retention 관리
- **스케일링**: Vertical scale(스케일 업) 시 maintenance window + 다운타임, Read scale-out 시 binlog 복제 지연, 스토리지扩容의 shard/re-partition 이슈
- **모니터링**: `information_schema`, `performance_schema`, `pg_stat_statements`, `slow_log`, `alert log`를 Nagios/Zabbix/Prometheus로 통합

**RDS는 "데이터베이스 엔진은 그대로 두고, 운영 계층(Control Plane)을 AWS API/IaC로 추상화"** 했고, **Aurora는 "엔진은 MySQL/PostgreSQL 인터페이스를 유지하되, 스토리지 계층을 클라우드 분산 스토리지로 재설계"** 한 것이다. 즉, RDS = *관리형*, Aurora = *관리형 + 분산 스토리지*의 차이가 핵심이다.

### 2. 시스템 개념도

```text
                         AWS Management Console / CLI / CDK / Terraform
                                          |
                                          v
            +-------------------------------------------------------------+
            |                  RDS Control Plane (Regional)               |
            |   - 프로비저닝·엔진 패치·백업·스냅샷·SG·Parameter Group    |
            |   - Event Notification · Performance Insights · Enhanced  |
            |     Monitoring · RDS Proxy · Auto Scaling                  |
            +------------------------------+------------------------------+
                                           |  (API: CreateDBInstance, Modify…)
                                           v
       +----------------------------------------------------------------------+
       |                       Data Plane (VPC, 고객 계정)                    |
       |                                                                      |
       |   +------------+  Writer Endpoint  +------------+  Reader Endpoint    |
       |   | App/Tier A +-----------------►|  Primary   |◄---------+          |
       |   +-----+------+                  |  (Writer)  |          |          |
       |         |                         +-----+------+          |          |
       |         |                               | (InnoDB redo log|          |
       |         |                               |  records push)  |          |
       |         |                               v                  |          |
       |   +-----+------+               +------------------+   +---+----+     |
       |   | App/Tier B |               | Aurora Storage   |   |Replica |     |
       |   | (ReadOnly) |               |   Volume         |   | AUR1~N |     |
       |   +-----+------+               |  (6-way quorum)  |   +---+----+     |
       |         |                      |  3 AZ × 2 copies |       | (read    |
       |         |                      |  + 1 S3 backup   |       |  page)   |
       |         |                      |  10GB segment    |       |          |
       |         |                      +--------+---------+       |          |
       |         |                               |                  |          |
       |         |       +---------------+       |                  |          |
       |         +------►| Custom EndPt  |◄------+                  |          |
       |                 |  (r5.4xl)     |                          |          |
       |                 +---------------+--------------------------+          |
       +----------------------------------------------------------------------+
                                          |
                                          |  Cross-Region Async Log Recv
                                          v
                                +--------------------+
                                | Aurora Global DB   |
                                |  Secondary Region  |
                                |  (RPO < 1s)        |
                                +--------------------+
```

### 3. 도입 필요성: 전통 운영 vs RDS/Aurora

| 항목 | EC2 Self-managed | Amazon RDS (표준) | Amazon Aurora |
|---|---|---|---|
| 엔진 패치 | DBA 수동 | 자동 minor / Maintenance window major | 엔진 코드 패치 포함, Zero-downtime patching(zDP) 일부 지원 |
| HA | DRBD / MHA / Patroni 직접 | Multi-AZ (Synchronous, Storage-level replication) | Shared-storage 6-way quorum (Storage-level replication) |
| Failover 시간 | 30s~수분 | 60~120s (DNS endpoint switch) | 보통 30s 이내, 종종 10s 이내 (Writer Endpoint 즉시) |
| Read Replica | binlog async | binlog async (lag 발생) | 스토리지 공유(Reader는 log apply만), lag 10~100ms 수준 |
| 스케일링 | Scale up = downtime | Storage Online扩容, Compute는 window | Compute 무중단 scaling, Read Replica 추가 수초 |
| 백업 | 자체 crontab | Automated Snapshot + PITR (binlog 보관) | Continuous backup to S3, Backtrack(rewind) 가능 |

- **📢 섹션 요약 비유**: 일반 RDBMS가 **"한 가게의 단일 요리사"** 라면, RDS는 **"프랜차이즈 본사가 주문·재료·POS를 관리하는 식당 체인"**, Aurora는 **"한 거대한 주방의 위성 셰프들이 같은 냉장고(Storage Volume)에서 재료를 가져다 쓰는 시스템"** 과 같다. 요리사 한 명이 아프면(노드 장애) 냉장고에서 재료를 그대로 가져와 요리를 계속할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. RDS의 표준 아키텍처 (Multi-AZ)

```text
   AZ-a (Primary)                    AZ-b (Standby)
   +--------------+                  +--------------+
   | RDS Primary  |  --- Sync ---►   | RDS Standby  |
   | (r6g.xlarge) |  storage rep     | (r6g.xlarge) |
   |   + EBS gp3  |                  |   + EBS gp3  |
   +------+-------+                  +------+-------+
          |                                 |
          +--------------+------------------+
                         | (장애 시 CNAME swap: ~60s)
                         v
              Endpoint: mydb.cluster-xxxx.rds.amazonaws.com:3306
```

- **동기식 블록 복제**(EBS snapshot-level, 또는 MySQL Group Replication)에 의존하므로 추가 스토리지 비용(Standby의 전체 EBS)이 발생하고, **Failover = DNS TTL 만료 + Warm-up**이 필요.
- Read Replica는 binlog async 복제 -> **lag 존재**, 이 lag는 동일 Aurora 대비 수십 배 크다.

### 2. Aurora의 핵심: Storage-Compute Decoupling + Quorum

Aurora는 **InnoDB의 redo log(record 단위)** 만 스토리지로 보내고, **데이터 페이지 자체는 복제하지 않는다.** 이것이 5~10배 성능 향상의 본질이다.

```text
 +--------------------------------------------------------------+
 |                       Aurora Primary                         |
 |  - InnoDB log records (4KB-512B, log records)                |
 |  - 큐: PG (Protection Group, 10GB) 단위로 Quorum 커밋        |
 |  - VDL: Volume Durable Link                                  |
 +--------------------------+-----------------------------------+
                            |  (TCP, intra-AZ < 1ms)
                            v
 +--------------------------------------------------------------+
 |           Aurora Storage Nodes (Protection Group = 6 노드)   |
 |  +-----+  +-----+  +-----+  +-----+  +-----+  +-----+      |
 |  |AZ-a |  |AZ-a |  |AZ-b |  |AZ-b |  |AZ-c |  |AZ-c |      |
 |  |N1   |  |N2   |  |N3   |  |N4   |  |N5   |  |N6   |      |
 |  +-----+  +-----+  +-----+  +-----+  +-----+  +-----+      |
 |  Read Quorum:  3/6  (V = 10G, R = 6, W = 4, R = 3)         |
 |  Write Quorum: 4/6  (W + R > N -> 4+3=7 > 6)                 |
 |                                                              |
 |  - Segment: 10GB Protection Group                             |
 |  - LSN: Log Sequence Number (monotonic, per segment)         |
 |  - S3: 30초~수 분 단위로 segment snapshot + manifest          |
 +--------------------------------------------------------------+
                            ^
                            |  (read-only: same volume, page fetch)
                            |
                     +------+------+
                     |  Replica    |  -- Reader Endpoint / Custom EP
                     |  (Aurora 1)  |
                     +-------------+
```

- **Write Quorum(4/6)** + **Read Quorum(3/6)** 이므로 정상 시점에 **AZ-a, AZ-b만 살아도 Write 가능**(최소 4 노드, 3개 AZ에 분산) -> 한 AZ 전체 장애에도 운영 지속.
- **Anti-entropy**: 손실 segment는 gossip 프로토콜 + Merkle tree로 background repair.
- **S3 backing**: S3는 11 9s 내구성(11×9s)의 cold archive 역할, segment가 6 노드 모두 손실되어도 S3에서 재구성.

### 3. Read Replica의 본질적 차이

| 구분 | RDS Read Replica (MySQL) | Aurora Replica |
|---|---|---|
| 복제 메커니즘 | binlog dump -> SQL apply | **같은 Storage Volume을 read** + Replica는 `redo log`만 apply |
| 스토리지 | Replica도 자체 EBS | **스토리지 비용 추가 없음** (Primary와 공유) |
| Lag 원인 | binlog dump 단위 (수 MB/s) + single thread apply | log apply만 (보통 10~30ms) |
| 추가 비용 | Replica 인스턴스 + EBS × 2(AZ별) | Replica 인스턴스 비용만 |

### 4. Aurora 주요 컴포넌트 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|---|---|---|
| **Aurora Volume (V)** | 가상 디스크 볼륨, 64TB까지 자동 확장, 10GB 단위 Protection Group | `Protection Group`은 6개 storage node에 분할 배치. 데이터는 6-way mirror, S3로 30초 단위 snapshot push. 공간 자동 10GB 단위 grow, 진짜 `thin-provisioned` |
| **InnoDB Layer (Aurora MySQL)** | SQL 파서·옵티마이저·트랜잭션 | 표준 InnoDB 코드베이스에 **스토리지 엔진(`aurora`)** 만 교체. Redo log를 그대로 Aurora Volume의 log record로 변환하여 push |
| **PostgreSQL Engine (Aurora PG)** | SQL 파싱·계획·실행 | PostgreSQL 15/16/17 호환, `pg_wal`을 Aurora log API로 라우팅 |
| **Reader Endpoint / Custom Endpoint** | 부하분산, 라우팅 | DNS 기반, **Writer Endpoint는 단일 Primary**, Reader Endpoint는 replica 셋을 round-robin 또는 `lag-min` 라우팅. Custom Endpoint는 특정 replica subset 지정 |
| **Backtrack** | 시간 되감기 (Aurora MySQL) | Target Retention(72h 등) 내 임의 시점으로 `rewind`. 데이터 페이지 in-place restore, binlog replay가 아님. 즉, **`DROP TABLE` 복구에 유용하지만 schema 변경에는 무력** |
| **Global Database** | Cross-Region DR | 전용 Aurora storage 기반 **cross-region log streaming** (일반 snapshot copy와 다름). RPO < 1s, RTO < 1m. Secondary는 보통 1개(여러 가능) |
| **Aurora Serverless v2** | ACU(1 ACU ≈ 2GB RAM) 기반 auto-scaling | Compute와 storage가 분리되어 있어, 0.5~128 ACU 사이를 수초~수 분 단위로 auto scale. Cold start 없음(v1과 차이) |
| **Parallel Query** | OLTP 워크로드에 MPP 가속 | Query 일부를 storage node로 push down (predicate/project pushdown), 노드별 100GB+ 임시 결과 셋, MySQL 8.x 호환 Aurora에서 사용 |
| **Aurora Machine Learning** | SageMaker / Bedrock 통합 | SQL `SELECT … FROM ML_PREDICT(…)` 형태, 2024~ Bedrock(Claude/Titan) LLM 통합, SageMaker endpoint 호출(데이터 외부 이동 없이 VPC endpoint) |
| **RDS Proxy** | 커넥션 풀링·Lambda·Burst 대응 | TCP 레벨 풀링. Aurora MySQL은 **"RDS Proxy for MySQL"** 명칭으로 pgBouncer-like 역할, IAM auth, Secrets Manager 통합. v2: native pooling |
| **Performance Insights** | DB 워크로드 시각화 | `pg_stat_statements`/`performance_schema` 기반, **top SQL**, **wait events**, **DB load** 시계열, 7일~2년 보존(긴 보존 시
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 488 / 800

<- **이전**: [487. 클라우드 파일 스토리지 EFS NFS 공유](/studynote/13_cloud_architecture/06_exam_summary/487_cloud_file_storage_efs_nfs_shared/)
**다음**: [489. 클라우드 NoSQL DynamoDB CosmosDB](/studynote/13_cloud_architecture/06_exam_summary/489_cloud_nosql_dynamodb_cosmosdb/) ->

---
