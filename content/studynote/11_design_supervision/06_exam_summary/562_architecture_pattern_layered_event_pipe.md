---
title: "562. 아키텍처 패턴 레이어드 이벤트 파이프 (Architecture Pattern Layered Event Pipe)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


# 562. 아키텍처 패턴 레이어드 이벤트 파이프 (Layered Event Pipe)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 동기식 계층형 호출(Layered Call) 경로와 비동기식 이벤트 파이프(Event Pipe)를 직교적으로 결합하여, 도메인 트랜잭션의 신뢰성(Exactly-Once/At-Least-Once)과 시스템 확장의 탄력성(Eventual Consistency, Backpressure)을 동시에 확보하는 하이브리드 아키텍처 패턴이다.
> 2. **가치**: 단일 요청의 평균 레이턴시(Sync Layer: ~50ms, Async Pipe: ~300ms~수 분)를 의도적으로 분리하고, Kafka, AWS Kinesis, RabbitMQ, Pulsar 같은 Event Broker를 통한 파티셔닝/리플레이/오프셋 관제로 처리량 10K~1M TPS급 확장이 가능하다. CDC(Change Data Capture)와 CQRS를 통한 읽기/쓰기 분리 시 처리 병목 제거 효과가 명확하다.
> 3. **판단 포인트**: (a) 동기-비동기 경계(Sync-Async Cutover)의 SLA 정의, (b) 이벤트 스키마 진화(Avro/Protobuf+Schema Registry) 및 순서 보장(Partition Key) 전략, (c) 멱등성(Idempotency Key) 확보와 사가(Saga) 보상 트랜잭션 설계, (d) DLQ(Dead Letter Queue)와 Poison Message 처리 정책이 의사결정의 핵심 축이다.

---

## Ⅰ. 개요 및 필요성

모놀리식 아키텍처가 도메인별로 분해되어 마이크로서비스로 전환될 때, 가장 빈번하게 부딪히는 구조적 딜레마가 있다. **"하나의 사용자 요청은 어떻게 계층(Layer)을 타고 흐르되, 시스템 전체는 어떻게 비동기 파이프를 통해 흐르게 만들 것인가?"** 라는 문제다. 전통적인 N-Tier 아키텍처(Presentation -> Business -> Data Access)는 동시성 1,000~3,000 동접 환경에서는 직관적이고 디버깅이 쉽지만, 10K TPS 이상의 이벤트 중심 워크로드(결제 트랜잭션, IoT 텔레메트리, 주문-재고-배송 연쇄 처리 등)에서는 다음과 같은 한계에 부딪힌다.

1. **결합도(Coupling) 폭발**: 상위 계층이 하위 계층의 동기 메서드 시그니처에 직접 의존하여, 도메인 변경 시 호출 그래프 전체가 깨진다.
2. **확장성 정체**: 모든 처리가 단일 트랜잭션 컨텍스트 내에서 직렬로 실행되므로, I/O 대기 시간 누적에 따라 응답 지연이 선형 증가한다.
3. **장애 전파(Failure Cascade)**: 하위 계층의 일시적 장애가 상위 계층 전체의 스레드 풀을 점거하고, Thread Pool Exhaustion으로 이어져 시스템이 연쇄 붕괴한다.
4. **관측성 부재**: 어디서 어떤 이벤트가 발행됐는지 추적하기 어려워, 분산 추적(Distributed Tracing) 도입 없이 인과 관계를 복원할 수 없다.

레이어드 이벤트 파이프(Layered Event Pipe)는 이러한 문제를 해결하기 위해, **동기적 계층 호출은 도메인 불변식(Domain Invariant)을 검증하는 "결정 경로"로, 비동기 이벤트 파이프는 부수 효과(Side Effect)와 외부 시스템 통합을 담당하는 "전파 경로"로 분리**하는 패턴이다. 이 패턴은 2010년대 중반 Reactive Manifesto(Vogels, Bonér 등)와 CQRS(Greg Young, 2010), Event Sourcing의 개념이 결합되며 정형화되었고, 2018년 이후 MSA의 보편화와 함께 AWS EventBridge(2019), Confluent Schema Registry 성숙, Kafka 2.5+의 Exactly-Once Semantics(Kafka EOS) 도입으로 실전 적용이 폭발적으로 증가했다.

```text
[전통적 N-Tier vs Layered Event Pipe 구조 비교]

   (기존) N-Tier (동기 직렬 호출)            (변경) Layered Event Pipe (하이브리드)
   +------------------------+               +------------------------+
   |  Presentation Tier     |               |  Presentation Tier     |
   |  (Web/Mobile/Client)   |               |  (Web/Mobile/Client)   |
   +-----------+------------+               +-----------+------------+
               | HTTP/Sync RPC                          | HTTP/Sync RPC
               v                                        v
   +------------------------+               +------------------------+
   |  Business Logic Tier   |               |  Business Logic Tier   |----> [즉시 응답]
   |  (Service Layer)       |               |  (Sync Domain Kernel)  |         (동기 검증)
   +-----------+------------+               +-----------+------------+
               | JDBC/SQL                                 | Publish Event
               v                                          v
   +------------------------+               +------------------------+
   |  Data Access Tier      |               |   EVENT PIPE LAYER     |
   |  (Repository)          |               |  (Kafka/Pulsar/EventBus)|
   +-----------+------------+               +------------------------+
               | DB I/O                                      |
               v                                            +---> Search Indexer
   +------------------------+                                +---> Notification Svc
   |  Database (RDBMS)      |                                +---> Analytics (Sink)
   |  (단일 트랜잭션)        |                                +---> Audit Logger
   +------------------------+                                +---> External System
```

핵심적인 차이는 **"쓰기 작업이 끝난 직후, 사용자에게 200 OK를 반환한 뒤에도 시스템 내부에서는 여전히 이벤트가 흐른다"**는 점이다. 즉, **사용자 관점의 응답 시간과 시스템 관점의 비즈니스 완료 시간은 의도적으로 분리**된다. 이 분리가 곧 SLA 설계의 핵심 변수가 된다.

- **📢 섹션 요약 비유**: 전통적인 우체국(동기 N-Tier)은 손님이 직접 창구에 가서 등기, 보험, 배송을 순서대로 받아야 하지만, **레이어드 이벤트 파이프**는 손님은 "접수 도장"만 받고(동기 검증), 나머지 등기/보험/배송은 백그라운드의 자동 분류 컨베이어(이벤트 파이프)가 알아서 처리하는 시스템과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

레이어드 이벤트 파이프는 크게 **4개의 논리 계층**과 **3개의 경계 인터페이스**로 구성된다. 각 계층은 단방향 의존성(Unidirectional Dependency)을 가지며, 이벤트 파이프 계층은 양방향으로 흐를 수 있지만 일반적으로 다운스트림(v) 흐름이 우세하다.

```text
[Layered Event Pipe 상세 아키텍처 및 이벤트 흐름]

   +--------------------------------------------------------------------+
   |  L1. PRESENTATION / API GATEWAY LAYER                              |
   |  +--------------+  +--------------+  +--------------+             |
   |  |  Web (SPA)   |  |  Mobile App  |  |  B2B Partner  |             |
   |  +------+-------+  +------+-------+  +------+-------+             |
   |         +-----------------+-----------------+                     |
   |                           v  (HTTPS / gRPC-Web / GraphQL)         |
   |                  +---------------------+                          |
   |                  |  API Gateway        |  <--- Rate Limit, AuthN/Z  |
   |                  |  (Kong/Envoy/Amplify|                          |
   |                  +----------+----------+                          |
   +-----------------------------+------------------------------------+
                                 | Sync Request
                                 v
   +--------------------------------------------------------------------+
   |  L2. APPLICATION / DOMAIN SERVICE LAYER (Sync Domain Kernel)       |
   |  +----------------------------------------------------------+      |
   |  |  Command Handler (Spring @Service, Node, Go)             |      |
   |  |   ① 도메인 불변식 검증 (e.g., "주문 ≥ 재고")              |      |
   |  |   ② Aggregate Root 단위 트랜잭션 (DB write)              |      |
   |  |   ③ Outbox Table에 이벤트 INSERT (원자성 보장)            |      |
   |  |   ④ HTTP 202 Accepted + Sync Domain Result 반환          |      |
   |  +----------------------------------------------------------+      |
   +-----------------------------+------------------------------------+
                                 | [BOUNDARY-1: Sync->Async Cutover]
                                 |  <--- Transactional Outbox Pattern
                                 v
   +-------------------------------------------------------------------+
   |  L3. EVENT PIPE LAYER (Async Backbone)                            |
   |                                                                   |
   |  +------------------+    +------------------+    +------------+   |
   |  |  Outbox Relay    |---->|  Event Broker    |<----|  CDC       |   |
   |  |  (Debezium/      |    |  (Apache Kafka   |    |  Connector |   |
   |  |   Application)   |    |   / Pulsar /     |    |  (DB->Topic)|   |
   |  +------------------+    |   AWS Kinesis /  |    +------------+   |
   |                          |   EventBridge)   |                     |
   |                          +--------+---------+                     |
   |                                   |                               |
   |      +----------+----------+------+------+----------+            |
   |      v          v          v      v      v          v            |
   |  +--------+ +--------+ +--------+ ... +--------+ +--------+      |
   |  |Topic-A | |Topic-B | |Topic-C |     |Topic-X | | DLQ    |      |
   |  |(order) | |(payment)| |(audit) |     |(legacy)| |(error) |      |
   |  +--------+ +--------+ +--------+     +--------+ +--------+      |
   +-------------------------------------------------------------------+
                                 |
                                 | [BOUNDARY-2: Async->Consumer]
                                 | [BOUNDARY-3: Schema Evolution]
                                 v
   +--------------------------------------------------------------------+
   |  L4. INTEGRATION / DOWNSTREAM CONSUMER LAYER                       |
   |  +------------+ +------------+ +------------+ +------------+       |
   |  | Search     | | Notification| | Analytics  | | Reporting  |       |
   |  | Indexer    | | Service     | | (Flink/Spark)| | (BI/BQ)  |       |
   |  | (ES/OS)    | | (Push/SMS)  | |             | |           |       |
   |  +------------+ +------------+ +------------+ +------------+       |
   |  +------------+ +------------+ +------------+                      |
   |  | 3rd-Party  | | ML Inference| | Audit Log  |                      |
   |  | Integration| | Pipeline    | | (S3+WORM)  |                      |
   |  +------------+ +------------+ +------------+                      |
   +--------------------------------------------------------------------+
                                 |
                                 v
              (선택) [CQRS Read Model / Event Sourcing Store]
              +----------------------------------+
              |  Redis / Materialized View /     |
              |  EventStoreDB / Apache Pinot     |
              +----------------------------------+
```

### 경계 인터페이스 상세 (3개의 핵심 인터페이스)

| 경계 | 명칭 | 핵심 기법 | 목적 |
|:---|:---|:---|:---|
| **BOUNDARY-1** | Sync->Async Cutover | **Transactional Outbox Pattern** (단일 트랜잭션 내에서 도메인 상태 + Outbox Row를 함께 INSERT, 이후 CDC 또는 Polling Relay가 Kafka로 publish) | DB 트랜잭션과 이벤트 발행의 원자성 보장 (이중 쓰기 문제 회피) |
| **BOUNDARY-2** | Async Consumer | **At-Least-Once + Idempotency Key** 또는 **Kafka EOS (Idempotent Producer + Transactional Consumer)** | 중복 소비 방지 및 정확히 한 번 처리 보장 |
| **BOUNDARY-3** | Schema Evolution | **Avro/Protobuf + Schema Registry** (Confluent SR, Apicurio), Backward/Forward/Full Compatibility Rule | Producer-Consumer 간 결합도 제거, 무중단 스키마 진화 |

### 구성 요소별 역할 및 핵심 기술

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Command Handler (L2)** | 사용자 의도(Command)를 받아 도메인 규칙 검증 후 상태 변경 + 이벤트 의도(Intent) 기록 | Spring `@Transactional` + Outbox Table (`id, aggregate_type, aggregate_id, payload, created_at, published_at`), Hexagonal Architecture의 Port 역할 |
| **Outbox Relay (L3 진입점)** | Outbox Table의 unpublished 레코드를 polling(WHERE published_at IS NULL LIMIT 100) 또는 CDC 스트림(Debezium log-based)로 감지하여 Event Broker에 publish | Debezium 1.6+ (PostgreSQL/MySQL/MongoDB 지원), Maxwell, Application Poller (10~100ms 주기) |
| **Event Broker** | 이벤트 영속화, 파티셔닝, 오프셋 관리, 컨슈머 그룹 라우팅 | Apache Kafka 3.x (Partition=Order Key, ISR≥3, acks=all), Apache Pulsar (분리 스토리지), AWS Kinesis Data Streams (Shard), RabbitMQ (Quorum Queue) |
| **Schema Registry** | 이벤트 스키마 버전 관리 및 호환성 검증 | Confluent Schema Registry, Apicurio Registry, Karapace — 호환성 모드: BACKWARD(Consumer 자유 업그레이드), FORWARD(Producer 자유), FULL(양쪽 모두) |
| **Consumer Group** | 동일 이벤트를 여러 서비스가 독립적으로 소비 (Fan-out), 순서 보장이 필요하면 동일 Partition Key 사용 | Kafka Consumer Group (Partition 수 ≤ Consumer 수), Consumer Rebalance Protocol, Cooperative Sticky Assignor |
| **DLQ (Dead Letter Queue)** | 재처리 실패 이벤트 격리 (Max Retry: 3~5회, Exponential Backoff: 1s->2s->4s->8s) | Kafka: `topic.dlq`, AWS SQS: `redrive policy`, Sentry/Splunk로 알림 후 수동 재처리 또는 Auto-Parking |
| **Idempotency Store** | 멱등성 키(`event_id + consumer_id`)로 중복 처리 차단 | Redis SETNX with TTL(24h), RDB Unique Constraint, DynamoDB conditional write |
| **Saga Orchestrator (선택)** | 분산 트랜잭션 보상 흐름 제어 (L2↔L3 왕복) | Temporal.io, Apache Airflow, AWS Step Functions, Camunda 8 (Zeebe) |
| **Observability Stack** | 분산 추적, 메트릭, 로그 통합 | OpenTelemetry SDK -> Jaeger/Tempo, Prometheus+Grafana, Loki/ELK, SLO: Sync P99 ≤ 500ms, Pipe Lag P99 ≤ 30s |

### 핵심 알고리즘 및 파라미터 의사결정

**1) 파티셔닝과 순서 보장(Partition Key Selection)**
이벤트의 순서가 비즈니스적으로 의미를 가지는 경우(예: 동일 주문의 생성->결제->배송), 동일 `aggregate_id`(주문번호, 사용자 ID 등)를 Partition Key로 사용한다. Kafka의 Hash Partitioning은 동일 키를 동일 Partition에 매핑하므로, Partition 내에서는 FIFO 순서가 보장된다. 그러나 **다수의 Partition에 걸쳐 순서를 보장하는 것은 불가능**하며, 이 경우 외부 정렬기(Sort Service)나 Key Sharding(부하 분산용)이 필요하다.

**2) 배압(
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 562 / 600

<- **이전**: [561. 아키텍처 평가 ATAM CBAM 트레이드오프](/studynote/11_design_supervision/06_exam_summary/562_architecture_evaluation_atam_cbam_tradeo/)
**다음**: [563. 모놀리스 분해 전략 도메인 경계](/studynote/11_design_supervision/06_exam_summary/563_monolith_decomposition_domain_boundary/) ->

---
