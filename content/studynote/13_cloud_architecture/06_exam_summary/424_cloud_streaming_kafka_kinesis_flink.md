---
title: "Cloud Streaming Kafka Kinesis Flink"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 스트리밍은 **Apache Kafka**(분산 커밋 로그 + 파티셔닝 + KRaft 합의), **AWS Kinesis**(관리형 샤드 스트림 + Lambda/Firehose 연동), **Apache Flink**(상태 기반 이벤트 시간 처리 + 정확히 한 번 의미론 + 체크포인트)을 결합하여, 배치 지연 없이 지속적으로 흐르는 대용량 이벤트 데이터를 **저지연·고가용성**으로 처리하는 분산 데이터 파이프라인 패러다임이다.
> 2. **가치**: 전통적 ETL 대비 **End-to-End 지연을 수 시간 -> 수십 ms 수준으로 단축**(예: Kafka + Flink 조합 시 P99 Latency 50~200ms), 수평 확장으로 **초당 수백만 이벤트 처리**(Kinesis 샤드당 1MB/s, Kafka 브로커 3-node 기준 100만 msg/s), 그리고 **Lambda 대비 Kappa 아키텍처 단순화**로 운영 복잡도 약 60% 절감이 가능하다.
> 3. **판단 포인트**: (a) **자체 운영(Kafka on EKS/MSK) vs 완전 관리형(Kinesis)** 트레이드오프, (b) **At-most-once / At-least-once / Exactly-once** 보장 수준 선택, (c) **이벤트 시간 vs 처리 시간** 의미론 결정, (d) **상태 백엔드(RocksDB vs HashMapState) 선택**과 **체크포인트 vs 세이브포인트** 분리 운영, (e) **처리량 중심 vs 지연 시간 중심** 워크로드 특성에 따른 파티션/샤드 및 병렬도 튜닝이 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 패러다임 전환: 배치 -> 스트리밍

기존 데이터 처리는 **Hadoop/Spark Batch ETL** 위주의 **T+1 ~ T+0(시간 단위)** 지연이 일반적이었다. 그러나 4차 산업혁명 시대를 맞아 **실시간 사기 탐지(FDS)**, **IoT 센서 모니터링**, **클릭스트림 분석**, **A/B 테스트 즉시 반영**, **실시간 추천**, **증권 시장 HFT 대응** 등 **밀리초~초 단위 의사결정**이 요구되는 워크로드가 폭증하면서, RDBMS/배치 시스템의 한계가 명확해졌다.

특히 클라우드 네이티브 환경에서는 **컨테이너 기반 마이크로서비스 간 비동기 이벤트 전파**가 필수 아키텍처 패턴이 되었고, **이벤트 드리닝 아키텍처(EDA)** 구현을 위한 **고성능 메시지 버스 + 스트림 프로세서** 조합이 핵심 인프라로 자리 잡았다.

### 1.2 도출되는 핵심 기술적 과제

1. **백프레셔(Backpressure)**: Producer 속도가 Consumer 처리 속도를 초과할 때 데이터 유실 방지
2. **순서 보장(Ordered Processing)**: 파티션 키 기반 해싱으로 동일 키 내 순서 유지
3. **내결함성(Fault Tolerance)**: 브로커/태스크 매니저 장애 시에도 정확히 한 번(Exactly-Once) 처리 보장
4. **상태 관리(Stateful Processing)**: 윈도우 집계, 조인, CEP(Complex Event Processing)를 위한 대용량 상태 영속화
5. **지연 시간 최소화**: 네트워크 hop, 직렬화/역직렬화, 디스크 I/O 병목 최적화

```text
+--------------------------------------------------------------------------+
|         전통적 배치 처리 파이프라인 (T+1, T+0)                            |
|                                                                          |
|   [App Logs]--+                                                         |
|   [DB CDC]----+---> [Kafka/Filebeat] ---> [HDFS/S3] ---> [Spark/Hive ETL] |
|   [API]-------+                              (수 분~수 시간)  ---> [BI]   |
|                                                                          |
|   ⚠️ 의사결정 지연 / 비용 폭증 / 운영 복잡도 (다중 스토리지)                |
+--------------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------------------------------------------------+
|         클라우드 스트리밍 파이프라인 (실시간, ms~sec 단위)                |
|                                                                          |
|   [Producers] ---> [Kafka / Kinesis Stream] ---> [Flink / Lambda]        |
|       |                  | (영구 로그 저장)        |                     |
|       |                  |                        +---> [실시간 알림]     |
|       |                  |                        +---> [Dashboard]      |
|       |                  |                        +---> [ML Inference]   |
|       |                  |                        +---> [Lakehouse Sink] |
+--------------------------------------------------------------------------+
```

### 1.3 왜 "Kafka + Kinesis + Flink"인가?

- **Apache Kafka**: LinkedIn에서 시작되어 de-facto 표준 분산 스트리밍 플랫폼, **높은 처리량(수백만 msg/s)**, **영구 로그(Retention)**, **넓은 생태계(Kafka Connect, Kafka Streams, Schema Registry)** 보유
- **AWS Kinesis Data Streams**: AWS의 **완전 관리형 스트림 서비스**로, 운영 부담 없이 VPC 내부에서 통합, **Lambda·Firehose·Analytics**와 즉시 연동
- **Apache Flink**: **진정한 스트림 우선(Stream-First) 엔진**으로, 이벤트 시간·워터마크·체크포인트 기반의 **정확한 상태 기반 처리**의 대표 주자. Spark Streaming의 마이크로배치 한계 극복

> **📢 섹션 요약 비유**: 기존 우편 시스템(배치 ETL)이 택배(스트리밍)로 바뀌면서, **택배 창고(Kafka/Kinesis)**에서 **자동 분류 로봇(Flink)**이 실시간으로 목적지별 분류·포장·배송을 처리하는 모습과 같다. 택배 창고 자체를 짓고 관리할지(Kafka 자체운영), 외부 물류센터를 빌릴지(Kinesis 관리형) 선택하는 것이 핵심 전략 결정이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Apache Kafka 내부 아키텍처

Kafka는 **Topic-Partition-Offset** 모델을 기반으로 한다. 하나의 토픽은 여러 파티션으로 나뉘며, 각 파티션은 **불변의 순차 로그(append-only log)**이다. 메시지는 **고유한 Offset**으로 식별되고, Consumer는 자기 offset을 commit하여 재시작 시 이어서 처리한다.

**KRaft 모드(Kafka Raft, KIP-500)**: 기존 ZooKeeper 의존성을 제거하고 Kafka 자체적으로 컨트롤러 quorum을 구성한다. **메타데이터 확장성**, **장애 복구 시간 단축**(수십 초 -> 수 초), **단일 보안 모델**이 장점이다.

```text
+---------------------------- Kafka Cluster (KRaft Mode) -------------------------+
|                                                                                 |
|  +--- Controller Quorum (KRaft) -------------------------------------------+  |
|  |  [Controller-1 (Active)] <---Raft---> [Controller-2] <---Raft---> [Ctrl-3] |  |
|  |  • Topic/Partition 메타데이터 관리 / Leader Election                     |  |
|  +------------------------------------------------------------------------+  |
|                                                                                 |
|  +--- Broker Pool ------------------------------------------------------+    |
|  |                                                                      |    |
|  |  +- Broker-1 -+  +- Broker-2 -+  +- Broker-3 -+                    |    |
|  |  | P0[L] P1[F]|  | P0[F] P1[L]|  | P0[F] P1[F]|   L=Leader, F=Follower|
|  |  | ^          |  | ^          |  | ^          |                    |    |
|  |  | | ISR Sync  |  | | ISR Sync  |  | | ISR Sync  |                    |    |
|  |  | v          |  | v          |  | v          |                    |    |
|  |  +------------+  +------------+  +------------+                    |    |
|  |                                                                      |    |
|  |  [Topic-A: 3 Partitions]  [Topic-B: 6 Partitions]                  |    |
|  |  Partition 0: [msg0][msg1][msg2][msg3]... (segmented log file)    |    |
|  |  Retention: 7 days (log.retention.hours) or 1TB (log.retention.bytes)|   |
|  +----------------------------------------------------------------------+    |
|                                                                                 |
|  +--- Producers --+    +--- Consumer Groups ---------------------+           |
|  | App-A (acks=all)|    | Group-G1: [C1 -> P0,P1] [C2 -> P2]        |           |
|  | App-B (acks=1)  |    | Group-G2: [C3 -> P0,P1,P2]                |           |
|  +----------------+    +----------------------------------------+           |
+---------------------------------------------------------------------------------+
```

### 2.2 AWS Kinesis 내부 아키텍처

Kinesis Data Streams(KDS)는 **샤드(Shard)** 단위로 데이터를 분할한다. **각 샤드는 1MB/s 입력, 2MB/s 출력, 초당 1,000 레코드 PUT** 용량을 제공하며, 데이터 보존 기간은 **최대 365일(Enhanced Fan-Out + Long-term Retention 시)** 까지 확장 가능하다.

- **Hot Shard 문제**: 잘못된 파티션 키 선택 시 특정 샤드만 과부하 -> **MD5 해시 키 + Composite Key** 설계 필요
- **Enhanced Fan-Out**: Consumer별 전용 2MB/s 처리량 제공 (Lambda 등)

```text
+-------------------- AWS Kinesis Data Streams ---------------------+
|                                                                  |
|   [Producer: EC2/IoT/Mobile SDK/CloudWatch/DB]                  |
|        |  PutRecord / PutRecords (batched)                      |
|        v                                                         |
|   +--- Stream: "user-events" (Provisioned / On-demand) ---+    |
|   |  Shard-1  [seqNo: 100~]  ---->  [Lambda / KCL App]     |    |
|   |  Shard-2  [seqNo: 200~]  ---->  [Firehose -> S3]        |    |
|   |  Shard-3  [seqNo: 300~]  ---->  [Flink KDA Application] |    |
|   |  Shard-4  [seqNo: 400~]  ---->  [Custom EC2 Consumer]   |    |
|   +--------------------------------------------------------+    |
|                                                                  |
|   +--- Kinesis Data Firehose (Delivery Stream) -----------+    |
|   |  Source(MSK/KDS/Direct) -> Buffer(1~128MB) ->            |    |
|   |  Transform(Lambda) -> Compress/Encrypt -> S3/Redshift/    |    |
|   |  OpenSearch/Splunk                                     |    |
|   +---------------------------------------------------------+    |
|                                                                  |
|   +--- Kinesis Data Analytics (Managed Flink / SQL) ------+     |
|   |  KDA Studio: SQL Editor (Streampipe)                  |     |
|   |  KDA for Flink: Zeppelin/Flink Job + S3 Checkpointing |     |
|   +---------------------------------------------------------+    |
+------------------------------------------------------------------+
```

### 2.3 Apache Flink 처리 모델

Flink는 **"스트림은 경계가 없는 데이터, 배치는 스트림의 특수한 경우"** 라는 철학을 가진 **진정한 네이티브 스트림 프로세서**다. 핵심 추상화는 다음과 같다:

- **DataStream API**: Low-level, 상태 기반 이벤트 처리
- **Table API / SQL**: 선언적, 최적화된 쿼리
- **상태(State)**: Keyed State(ValueState, ListState, MapState), Operator State(UnionListState, BroadcastState)
- **시간 의미론**: Event Time(실제 발생 시각) + Watermark(지연 허용 한계) + Processing Time
- **체크포인트(Checkpoint)**: Chandy-Lamport 알고리즘 기반 분산 스냅샷, **정확히 한 번(Exactly-Once)** 보장
- **세이브포인트(Savepoint)**: 명시적 외부 저장용 스냅샷, 버전 업그레이드/리플레이용

```text
+----------------------- Apache Flink Job Architecture -----------------------+
|                                                                              |
|  +--- JobManager (Master) ---------------------------------------------+   |
|  |  • Scheduler (Slot Pool)   • Checkpoint Coordinator                  |   |
|  |  • ResourceManager         • Web UI (localhost:8081)                 |   |
|  +---------------------------------------------------------------------+   |
|         ^                              ^                                    |
|    (deploy)                  (heartbeat / task status)                      |
|         |                              |                                    |
|  +------+------------------------------+------------------------------+   |
|  |  TaskManager-1    TaskManager-2    TaskManager-3                    |   |
|  |  +-Slot-1-+      +-Slot-1-+       +-Slot-1-+                      |   |
|  |  |Source  |      |Source  |       |Window  |                      |   |
|  |  | -> Map  |      | -> Map  |       | Agg    |                      |   |
|  |  +--------+      +--------+       +--------+                      |   |
|  |  +-Slot-2-+      +-Slot-2-+       +-Slot-2-+                      |   |
|  |  | KeyBy  | ----> | KeyBy  |  ----> | Sink   |                      |   |
|  |  | State  |      | State  |       | Kafka  |                      |   |
|  |  +--------+      +--------+       +--------+                      |   |
|  |   [RocksDB State Backend]  [HashMapState]  [S3 Checkpoint]         |   |
|  +--------------------------------------------------------------------+   |
|                                                                              |
|  +--- Two-Phase Commit Sink (Exactly-Once) -------------------------+    |
|  |  1. beginTransaction()  -> pre-commit to Kafka/DB                  |    |
|  |  2. notifyCheckpointComplete() -> final commit                    |    |
|  |  3. 장애 시: pre-commit 데이터 롤백 + 재시작 시 마지막 checkpoint 복구|   |
|  +--------------------------------------------------------------------+    |
+------------------------------------------------------------------------------+
```

### 2.4 핵심 구성 요소 매핑

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Producer / Kinesis Producer** | 데이터 수집/발행 | **Batching**(`linger.ms=5~100`, `batch.size=16KB~1MB`), **Compression**(`lz4`, `zstd`, `snappy`), **Idempotent Producer**(`enable.idempotence=true`로 동일 세션 내 중복 제거), `acks=all` 설정으로 min.insync.replicas 충족 시에만 commit |
| **Broker / Kinesis Shard** | 메시지 저장·복제 | **ISR(In-Sync Replicas)** 동기화 후 ack, **Leader-Follower** 구조, **Page Cache + Zero-Copy(`sendfile()`)** 활용, `log.flush.interval.messages`로 fsync 정책 제어 |
| **Consumer / KCL / Flink Source** | 메시지 폴링·처리 | **Consumer Group Rebalance**(Cooperative Sticky Assignor), **Manual Offset Commit**(`enable.auto.commit=false` 권장), Flink의 경우 `setStartFromGroupOffsets` 또는 `setStartFromTimestamp` |
| **Stream Processor (Flink)** | 변환·집계·CEP | **Operator Chain** 최적화, **Watermark Generator**(`forBoundedOutOfOrderness(Duration.ofSeconds(5))`), **Tumbling/S
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 424 / 800

<- **이전**: [423. 클라우드 DW 빅쿼리 레드시프트 스노우플레이크](/studynote/13_cloud_architecture/06_exam_summary/423_cloud_dw_bigquery_redshift_snowflake/)
**다음**: [425. 클라우드 ETL 글루 데이터플로 데이터퓨전](/studynote/13_cloud_architecture/06_exam_summary/425_cloud_etl_glue_dataflow_datafusion/) ->

---
