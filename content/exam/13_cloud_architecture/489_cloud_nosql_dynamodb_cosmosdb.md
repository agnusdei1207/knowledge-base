---
title: "Cloud NoSQL DynamoDB CosmosDB"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AWS DynamoDB와 Azure CosmosDB는 파티션 키 기반의 수평적 샤딩(Partitioning)으로 무한 확장성을 확보하면서, DynamoDB는 결과적 일관성(Eventual Consistency) 중심의 Key-Value/Document 모델을, CosmosDB는 5단계 튜닝 가능한 일관성(Tunable Consistency) 위에 SQL/MongoDB/Cassandra/Gremlin/Table 5종 API를 노출하는 Multi-Model 글로벌 분산 데이터베이스이다.
> 2. **가치**: 단일 리전에서 초당 1,000만+ 요청 처리(DynamoDB 사례: Prime Day 8,920만 req/s), CosmosDB는 멀티 리전 쓰기 99.999% SLA 및 p99 단위 10ms 미만 읽기/15ms 미만 쓰기 보장으로 CAP 트레이드오프를 SLA로 해소한다.
> 3. **판단 포인트**: 핫 파티션(Hot Partition) 방지를 위한 파티션 키 설계(카디널리티, 스큐), 비용 모델(DynamoDB: WCU/RCU vs On-Demand, CosmosDB: RU/s vs Autoscale), 멀티 리전 트랜잭션 필요성, 일관성-지연시간-비용의 3차원 트레이드오프가 핵심 결정 변수이다.

---

## Ⅰ. 개요 및 필요성

기존 RDBMS(Oracle, MySQL)는 ACID 트랜잭션과 정규화된 스키마로 데이터 무결성을 보장했지만, 빅데이터·IoT·소셜미디어 시대에 발생하는 **초대형 트래픽(VLDB, Velocity)**, **다양한 데이터 형태(Variety)**, **수평 확장 요구(Volume)** 에서는 Master-Slave 복제, Sharding, Read Replica 같은 수작업 확장이 한계에 부딪혔다. 2000년대 후반 등장한 NoSQL은 "일관성을 약화시켜 가용성과 분할 내성(Partition Tolerance)을 확보"하는 CAP 이론의 실용적 해석이었으나, 자체 운영 시 노드 추가/장애복구/리밸런싱/Cassandra의 Gossip 프로토콜 관리 같은 운영 부담이 막대했다.

이 문제를 해결하기 위해 2012년 AWS가 DynamoDB를, 2017년 Microsoft가 CosmosDB를 출시하면서 **"운영 오버헤드 0"** 의 완전관리형(PaaS) NoSQL 시대가 열렸으며, 핵심 가치 제안은 다음 세 가지다:

- **제로 운영(Zero Ops)**: 패치, 백업, 복제, 샤드 리밸런싱 모두 클라우드 제공자가 처리
- **페이즈 단위 과금(Pay-per-Use)**: DynamoDB는 WCU/RCU 1시간 단위, CosmosDB는 RU(Request Unit) 초 단위
- **글로벌 분산(Global Distribution)**: DynamoDB Global Tables, CosmosDB Turnkey Global Distribution으로 클릭 한 번에 멀티 리전 복제

```text
+---------------------------------------------------------------------+
|  기존 RDBMS 시대 (2000s 초반)         |  클라우드 NoSQL 시대 (2012~)  |
+--------------------------------------+------------------------------+
|  - 단일 인스턴스 + 수직 확장          |  - 무한 수평 확장 (Auto-Shard)|
|  - 수동 Sharding (앱 코드 내 분기)    |  - 자동 분할 (Hash Partition) |
|  - CAP 중 C+A 선택                   |  - AP 기본, 일관성 SLA 제공   |
|  - 5,000 TPS 한계                    |  - 1,000만+ TPS              |
|  - 라이선스 + HW + DBA 3중 비용      |  - 사용량 기반 종량제         |
+--------------------------------------+------------------------------+
       v                        v                       v
   [ Oracle RAC ]          [ Cassandra ]      [ DynamoDB / CosmosDB ]
   수직 확장 한계         셀프 운영 부담       완전관리형 + 글로벌 분산
```

전통적 아키텍처의 한계: Cassandra는 자체 클러스터 운영 시 컴팩션(Compaction) 튜닝, 힙 메모리 관리(G1GC), vnode 설정 같은 깊은专业知识이 요구되었고, DynamoDB는 이를 AWS가 모두 자동화하여 개발자가 파티션 키와 접근 패턴에만 집중하도록 설계 철학을 전환했다.

- **📢 섹션 요약 비유**: 기존 RDBMS가 "직접 운전해야 하는 대형 트럭"이라면, 클라우드 NoSQL은 "GPS·주유·정비 모두 자동화된 자율주행 택시"와 같다. 목적지(파티션 키)만 지정하면 자동으로 최적 경로(샤드)로 안내한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### DynamoDB 내부 아키텍처

DynamoDB는 Amazon의 내부 Dynamo Paper(2007)에서 출발하여 **Sloppy Quorum + Hinted Handoff + Merkle Tree Anti-Entropy + Consistent Hashing** 4대 핵심 기법을 11년간 클라우드 규모로 재설계한 시스템이다.

```text
                              DynamoDB 요청 처리 흐름
                              ━━━━━━━━━━━━━━━━━━━━━━
   [Client App]
       |
       |  1. PutItem / GetItem / Query
       v
  +-------------+    2. 인증/스로틀링(5xx/ProvisionedThroughputExceeded)
  | API Gateway |
  +------+------+
         |
         v
  +----------------+    3. 파티션 키 -> MD5 -> Consistent Hash Ring
  |  Request Router|       위치 결정 (예: Partition 0xA3)
  +--------+-------+
           |
           v
  +-------------------------------------------------------------+
  |  Partition (10GB or 3000 RCU/1000 WCU 단위로 자동 분할)       |
  |  +----------+  +----------+  +----------+  +----------+    |
  |  | Storage  |  |  Primary |  |   Replica|  |   Replica|    |
  |  |  (SSD)   |◄-+   Node   +-►|  AZ-a    |  |  AZ-b    |    |
  |  |  B-tree  |  |          |  |(Sync 복제)|  |(Async 복제)|    |
  |  +----------+  +----+-----+  +----------+  +----------+    |
  |                     |                                       |
  |              4. Global Table 활성화 시                        |
  |                     | 다른 리전으로 비동기 복제                |
  +---------------------+---------------------------------------+
                        v
              +----------------------+
              |   DynamoDB Streams   |  Kinesis 기반 변경 로그
              |   (24h 보존)         |  Lambda 트리거
              +----------------------+
```

### CosmosDB 내부 아키텍처

CosmosDB는 **Multi-Master + Turnkey Global Distribution + 5단계 튜닝 가능 일관성** 을 차별화 요소로 내세우며, 내부적으로는 "물리적 파티션 -> 논리적 파티션"의 2단계 매핑과 **Conflict-Free Replicated Data Type(CRDT)** 기반의 자동 충돌 해결을 사용한다.

```text
                          CosmosDB 요청 처리 흐름
                          ━━━━━━━━━━━━━━━━━━━━━━
   [Client SDK (.NET/Node/Python)]
       |  SQL/MongoDB/Cassandra/Gremlin/Table API
       v
  +--------------+    글로벌 계정 -> 데이터베이스 -> 컨테이너
  |  Gateway     |    (개념적 계층; 실제 라우팅은 Partition Key 기반)
  +------+-------+
         v
  +------------------------------------------------------------+
  |            Frontend (5개 일관성 레벨 라우팅)                |
  |  Strong -> Bounded Staleness -> Session -> Consistent Prefix |
  |                                       -> Eventual           |
  +--------+---------------------------------------------------+
           v
  +-----------------------------------------------------------+
  |  Backend Partition (물리적: 10GB 단위 자동 분할)            |
  |  +----------+  +----------+  +----------+                |
  |  | Replica  |  | Replica  |  | Replica  |  (4-방향 복제) |
  |  |  Set     |  |  Set     |  |  Set     |                |
  |  | Region A |  | Region B |  | Region C |  Multi-Master  |
  |  +----+-----+  +----+-----+  +----+-----+                |
  |       |             |             |                      |
  |  +----v-------------v-------------v--------------------+ |
  |  | Conflict Resolution: Last-Writer-Wins(LWW) 또는     | |
  |  | Custom Stored Procedure (CRDT 방식 병합)            | |
  |  +----------------------------------------------------+ |
  +-----------------------------------------------------------+
           |
           v
  +------------------+
  |   Change Feed    | -> Azure Functions / Synapse Link
  |  (증분 변경 로그) |
  +------------------+
```

### 핵심 구성 요소 비교

| 구성 요소 | DynamoDB | CosmosDB |
| :--- | :--- | :--- |
| **파티션 키 (Partition Key)** | 필수, MD5 해시 -> 3개 노드에 분산 저장 (Sloppy Quorum) | 필수, 10GB 초과 시 자동 Split, Logical Partition ↔ Physical Partition 분리 |
| **정렬 키 (Sort Key)** | 옵션, 동일 파티션 내 범위 쿼리·계층 데이터 지원 | 없음(단일 키), 계층은 트리 구조로 모델링 |
| **인덱스** | LSI(Local Secondary Index, 테이블당 5개, 생성 후 변경 불가), GSI(Global Secondary Index, 계정당 20개) | 자동 인덱싱 정책(Include/Exclude/IndexingMode) |
| **일관성 모델** | Eventual(기본) / Strong(0.5배 RCU 비용) | 5단계: Strong, Bounded Staleness(K,L), Session, Consistent Prefix, Eventual |
| **글로벌 분산** | Global Tables(2024 기준 20+ 리전), Multi-Active, DynamoDB Streams 기반 비동기 복제 | Turnkey Global Distribution, Multi-Master Writes, 99.999% SLA |
| **캐시** | DAX(DynamoDB Accelerator, 10분 TTL, in-memory microsecond 응답) | 내장 캐시 없음, Azure Cache for Redis 별도 구성 |
| **변경 캡처** | DynamoDB Streams(24h) + Kinesis Data Streams(365일) | Change Feed(컨테이너별 독립, TTL 기반 유지) |
| **과금 단위** | WCU(1KB/s Write), RCU(4KB/s Strongly Consistent Read) | RU(Request Unit): 1KB Read=1RU, 1KB Write=5RU, 자동·고정 모드 |
| **트랜잭션** | TransactGetItems(최대 100개), ACID, 2배 WCU/RCU | 스냅샷 격리(SI) Transactional Batch, 다중 문서 ACID |
| **쿼리 언어** | PartiQL(2020~, SQL 호환) 또는 AWS SDK | SQL API(native), MongoDB/Cassandra/Gremlin/Table API |
| **TTL** | 항목별 epoch timestamp, 백그라운드 정리(48h 이내) | 컨테이너 단위, PITR(Point-in-Time Restore)과 통합 |

### 핵심 알고리즘·파라미터

- **DynamoDB 적응형 용량(Adaptive Capacity)**: 파티션별 RCU/WCU를 자동 모니터링하여 핫 파티션에 5분 내 최대 5분 전 트래픽의 2배까지 재할당, "예전에는 핫 파티션 분리 위해 사전 Shard 설계가 필수였으나 2018년 이후 자동화"
- **DynamoDB RCU 계산**: `Strong Read 4KB/초 = 1 RCU`, `Eventually Consistent Read는 0.5 RCU`, `Transaction Read 2 RCU`
- **DynamoDB 파티션 한도**: 파티션당 최대 3000 RCU + 1000 WCU, 10GB 저장 용량. 초과 시 자동 Split, 단 Split 직후 트래픽 쏠림 주의 필요
- **CosmosDB RU 계산 공식**: `RU = (DocSize_KB / 4) × 1(Read) / 5(Write) / 2(Query) / N(여러 문서 Batch)`, Indexed 속성은 추가 RU 발생
- **CosmosDB 일관성 토폴로지**: Strong(Quorum 4/4, 지연^, 가용성v) -> Eventual(Quorum 2/4, 지연v, 가용성^)까지 5단계 점진적 트레이드오프
- **CosmosDB 멀티 리전 쓰기 충돌**: 기본 LWW(Last-Writer-Wins, _ts 타임스탬프), 사용자 정의 Stored Proc로 `setMerge`/`setUnion` 같은 CRDT 함수 가능

- **📢 섹션 요약 비유**: DynamoDB는 "3개 우체통에 사본을 넣어두는 시스템"으로 한 개 우체국이 폭파되어도 배달이 가능하며, CosmosDB는 "전 세계 4개 우체국이 동시에 같은 문서를 작성해도 마지막에 누가 썼는지 자동으로 합쳐주는 시스템"이다.

---

## Ⅲ. 비교 및 연결

### 주요 NoSQL 데이터베이스 비교

| 구분 | AWS DynamoDB | Azure CosmosDB | Cassandra (Astra) | MongoDB Atlas | Google Spanner |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **데이터 모델** | Key-Value + Document | Multi-Model (5종 API) | Wide-Column (CQL) | Document (BSON) | Relational + NewSQL |
| **일관성** | Eventual / Strong (2종) | 5단계 튜닝 가능 | Eventual / Quorum 조절 | Read Concern 5종, Write Concern 2종 | Strong (TrueTime API) |
| **트랜잭션** | 제한적(100개 항목) ACID | Multi-Document ACID | LWT(Lightweight) | Multi-Document ACID | 글로벌 ACID |
| **확장 한계** | 무제한 (파티션 자동) | 무제한 (물리 파티션 자동) | 무제한 (Linear) | 샤딩 1024개 (2024 기준) | 무제한 (실질적 한계 큼) |
| **글로벌 분산** | Global Tables (Multi-Active) | Turnkey Multi-Master | 자체 DC 간 복제 (복잡) | Global Clusters (제한적) | Multi-Region Strong |
| **SLA** | 99.99% (단일 리전) | 99.999% (Multi-Region) | 99.
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 489 / 800

<- **이전**: [488. 클라우드 데이터베이스 RDS Aurora 관리형](/studynote/13_cloud_architecture/06_exam_summary/488_cloud_database_rds_aurora_managed/)
**다음**: [490. 클라우드 그래프 DB Neptune 관계 분석](/studynote/13_cloud_architecture/06_exam_summary/490_cloud_graph_db_neptune_relation_analysis/) ->

---
