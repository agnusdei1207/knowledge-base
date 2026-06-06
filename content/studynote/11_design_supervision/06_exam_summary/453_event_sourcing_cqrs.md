---
title: "453. 이벤트 소싱 CQRS 설계 패턴 (Event Sourcing CQRS Design Pattern)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 도메인 객체의 **현재 상태(Current State)를 직접 갱신(UPDATE)하지 않고, 상태를 변화시킨 모든 사실(Fact)을 불변(Immutable) 이벤트 로그**로 Event Store에 Append-Only 방식으로 기록한다. **CQRS(Command and Query Responsibility Segregation)**는 쓰기(Command) 측의 도메인 모델과 조회(Query) 측의 읽기 전용 프로젝션(Read Model/Projection)을 **물리적·논리적으로 분리**하여, 각 책임에 최적화된 스토리지·확장성·일관성 정책을 독립적으로 운용하는 아키텍처 스타일이다.
> 2. **가치**: 금융·공공·물류 등 **감사 추적(Audit Trail)·법적 컴플라이언스** 도메인에서 100% 이력 보존, 장애 발생 시 **이벤트 리플레이(Event Replay)**를 통한 임의 시점 복구/리빌드, **시간 여행 디버깅(Time-Travel Debugging)**, 쓰기·읽기 트래픽의 비대칭을 **독립 스케일링**(예: 읽기 10배 확장으로 CPU 40% 절감)으로 해소한다.
> 3. **판단 포인트**: **Eventual Consistency** 허용 범위(보통 수십 ms~수 초), **이벤트 스키마 진화(Schema Evolution) 전략**(Upcasting, Versioned Events, Eventual Schema Registry), **Event Store의 순서 보장 메커니즘**(Kafka Partition Key vs Aggregate ID Ordering), **Saga/Outbox/CDC** 등 보상 트랜잭션과 발행 패턴 채택 여부가 설계 난이도와 운영 복잡도를 결정한다.

---

## Ⅰ. 개요 및 필요성

전통적인 CRUD 기반 아키텍처는 RDBMS 한 대에서 **단일 트랜잭션으로 4가지 연산(Create, Read, Update, Delete)**을 처리한다. 그러나 **클라우드 네이티브·MSA 시대**로 접어들면서 다음과 같은 한계가 폭증한다.

1. **상태와 이력의 결합**: `UPDATE account SET balance=5000 WHERE id=1`과 같은 SQL은 1년 전 잔액을 알 수 없게 만든다. 별도 `account_history` 테이블을 만들어 트리거/CDC로 동기화하지만, 이중 쓰기(Dual Write) 문제로 데이터 정합성이 깨진다.
2. **읽기/쓰기 간 트레이드오프**: 정규화된 3NF 모델은 무결성에는 강하지만, 복잡한 분석 조회에서는 JOIN 폭발이 발생한다. 반대로 비정규화 모델은 쓰기 경합과 갱신 이상(Update Anomaly)을 유발한다.
3. **도메인 복잡도의 비대화**: 엔티티 수가 수백 개로 늘어나면서 단일 ORM 모델이 수천 라인의 Fat Service를 만들고, 트랜잭션 경계가 모호해진다.
4. **확장성의 한계**: 모놀리식 RDBMS의 수직 확장 한계, 마스터-슬레이브 복제 지연으로 인한 읽기 일관성 깨짐.

**Event Sourcing + CQRS**는 Greg Young(2010), Vaughn Vernon, Chris Richardson 등의 DDD/MSA 철학 위에 정립된 패턴으로, **"상태란 이벤트의折叠(Fold)이다"**라는 함수형 사고에 기반한다.

```text
+--------------------------------------------------------------------------+
|                  전통적 CRUD 모델 (단일 모델, 단일 DB)                       |
|                                                                          |
|   [Client] --HTTP--> [Service+ORM] --ACID Tx--> [RDBMS(Single Model)]   |
|                                              |                            |
|                              +---------------+---------------+            |
|                              v               v               v            |
|                          INSERT          UPDATE          SELECT           |
|                       (현재 상태 저장)  (이력 손실)    (JOIN 비용^)         |
+--------------------------------------------------------------------------+
                                  |
                                  |  패러다임 전환
                                  v
+--------------------------------------------------------------------------+
|              Event Sourcing + CQRS 모델 (모델 분리, 책임 분리)              |
|                                                                          |
|   [Client]                                                               |
|     |                                                                    |
|     +--[Command]--> [Command API] --> [Aggregate/Domain]                 |
|     |                              |                                     |
|     |                              v (이벤트 1..N 생성)                  |
|     |                       +--------------+                             |
|     |                       |  Event Store | <---- Append-Only 로그       |
|     |                       | (불변 사실)  |                             |
|     |                       +------+-------+                             |
|     |                              | (Event Subscription)                |
|     |                              v                                     |
|     |                       [Projection Builder]                         |
|     |                              |                                     |
|     |                              v                                     |
|     |                       +--------------+                             |
|     +--[Query]------------->|  Read Model  | (PostgreSQL, ES, Redis...)  |
|        (CQRS 조회)           +--------------+                             |
+--------------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 기존 CRUD는 **현재 잔액만 적힌 은행 통장**과 같다. Event Sourcing은 **모든 입출금 내역이 절대 지워지지 않는 회계 장부**이며, CQRS는 "돈을 넣고 빼는 창구(은행원)"와 "잔액을 조회하는 창구(ATM)"를 **물리적으로 분리**해 각자 최적의 설비를 쓰는 것에 비유할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Command Side (쓰기 경로)

클라이언트의 **명령(Command, 의도(Intent))**은 검증 후 Aggregate에 도달한다. Aggregate는 **불변 조건(Invariant)**을 검사하고, 비즈니스 규칙에 따라 **0개 이상의 도메인 이벤트**를 생성한다. 생성된 이벤트는 단일 트랜잭션으로 Event Store에 **Append**된다.

```text
+------------------------------------------------------------------------------+
|                          Command Side 상세 흐름                                |
|                                                                              |
|  [Client]                                                                    |
|     |                                                                        |
|     | POST /orders {"command":"CreateOrder","items":[...]}                   |
|     v                                                                        |
|  +------------------+    ① Command 객체 생성 및 입력 검증                      |
|  | Command Controller|--(Bean Validation, AuthZ)----------------+            |
|  +------------------+                                              |            |
|                              |                                       v            |
|                              |  ② CommandBus.dispatch(cmd)  +-----------------+ |
|                              +------------------------------>| Command Handler | |
|                                                              +--------+--------+ |
|                                                                       |          |
|                                                                       | ③ Load   |
|                                                                       v          |
|   +--------------------------------------------------------------------------+ |
|   | Aggregate (e.g., Order Aggregate)                                          | |
|   |  - AggregateID, Version, Uncommitted Events                                | |
|   |  - 비즈니스 메서드: createOrder(), addItem(), pay()                        | |
|   |  - 불변식 검사: "재고 >= 주문수량", "결제 전 취소 가능" 등                   | |
|   +--------------------------------------------------------------------------+ |
|                              |                                                |
|                              | ④ 이벤트 생성 (OrderCreated, ItemAdded, ...)    |
|                              v                                                |
|   +--------------------------------------------------------------------------+ |
|   | Event Store (Append)                                                      | |
|   |  +--------+------------+---------+------------+--------------+            | |
|   |  |StreamID| Version    | EventID | EventType  | Payload(JSON)|            | |
|   |  +--------+------------+---------+------------+--------------+            | |
|   |  |order-1 | 0          | evt-001 | OrderCreated| {...}       |            | |
|   |  |order-1 | 1          | evt-002 | ItemAdded  | {...}       |            | |
|   |  |order-2 | 0          | evt-003 | OrderCreated| {...}       |  <- Partition| |
|   |  +--------+------------+---------+------------+--------------+            | |
|   |                                                                          | |
|   |  * 동일한 StreamID(=AggregateID) 내에서는 Version 단조 증가(Optimistic)   | |
|   |  * 글로벌 순서는 보장 안 됨 -> StreamID 단위 순서 보장                     | |
|   +--------------------------------------------------------------------------+ |
+------------------------------------------------------------------------------+
```

### 2. Query Side (읽기 경로)

이벤트는 **비동기(at-least-once)로 Projection에 전파**된다. Projection Builder는 **Tumbling Window / CDC / Kafka Consumer**로 이벤트를 폴링 또는 구독하여, 조회에 최적화된 별도 Read Model을 갱신한다.

```text
+------------------------------------------------------------------------------+
|                           Query Side & Projection                            |
|                                                                              |
|   [Event Store]                                                              |
|       |                                                                      |
|       |  Kafka Topic: "domain.orders"  (key=orderId, partition=Hash)         |
|       |  +----------+--------------+--------------+                           |
|       |  |Partition0| Partition1   | Partition2   |                           |
|       |  |order-1,3 | order-2,7    | order-4,5    |                           |
|       |  +----------+--------------+--------------+                           |
|       v                                                                      |
|   +--------------------+                                                     |
|   | Projection Worker  |  ① 토픽 구독, ② Offset Commit                         |
|   | (Group=query-svc)  |  ③ 멱등 처리: OrderID+Version 체크                  |
|   +--------+-----------+                                                     |
|            |                                                                 |
|            +-----------------+-----------------+-----------------+           |
|            v                 v                 v                 v           |
|   +-----------------+ +--------------+ +--------------+ +-------------+    |
|   | Read Model 1    | |Read Model 2  | |Read Model 3  | |Search Index |    |
|   | OrderDetailView | |OrderListView | |DailySales    | |Elasticsearch|    |
|   | (PostgreSQL)    | |(Redis Cache) | |(ClickHouse)  | |             |    |
|   +-----------------+ +--------------+ +--------------+ +-------------+    |
|            ^                                                                  |
|            |  ④ GET /orders/1 (단일 ReadModel 질의)                            |
|   [Client]-+                                                                  |
+------------------------------------------------------------------------------+
```

### 3. 핵심 메커니즘

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Aggregate (집합체)** | 비즈니스 불변식 캡슐화, 트랜잭션 일관성 경계 정의 | DDD의 Aggregate Root가 Command를 받아 도메인 이벤트 생성. 한 Aggregate = 한 Event Stream. **크기 가이드**: 100~200개 이벤트 이내, 1MB 미만 (카프카 제약) |
| **Command Bus / Handler** | 명령 라우팅, 입력 검증, 인증/인가 처리 | Axon Server, MediatR(.NET), NServiceBus, Spring Cloud Stream. 동기 호출 시 응답은 `Accepted(202)` + 위치 추적 ID |
| **Event Store** | 이벤트의 단일 진실 공급원(Single Source of Truth), Append-Only | **Apache Kafka**(Partition=AggregateID, compaction), **EventStoreDB**(gRPC 스트림, 낙관적 동시성), **Axon Server**, **DynamoDB Streams**, **Cosmos DB Change Feed**. 옵션으로 PostgreSQL + Debezium CDC 구성 가능 |
| **Snapshot** | Aggregate 재생 비용 절감을 위한 주기적 상태 저장 | N개 이벤트(예: 100건)마다 또는 임계 시간마다 스냅샷. 저장소: 별도 컬렉션 또는 Event Store 내 `Snapshot` 이벤트 |
| **Projection Builder** | 이벤트를 Read Model로 변환, 멱등성 보장 | 배치/실시간 모드. **체크포인트** 테이블로 처리 위치 추적. **리플레이** 시 Read Model을 truncate 후 처음부터 재투영 |
| **Read Model (Materialized View)** | 조회 패턴별 최적화된 데이터 사본 | PostgreSQL(트랜잭션 일관성), Elasticsearch(전문 검색/분석), Redis(초저지연), ClickHouse(OLAP), GraphQL 스키마 |
| **Saga / Process Manager** | 여러 Aggregate에 걸친 장기 트랜잭션 조정 | **Orchestration**(중앙 조율, e.g., Camunda, Axon Saga) vs **Choreography**(이벤트 기반 자율). 보상 트랜잭션(Compensating Action)으로 정합성 회복 |
| **Schema Registry** | 이벤트 스키마 버전 관리, 호환성 검증 | Confluent Schema Registry(Avro/Protobuf/JSON Schema), Apicurio. **호환성**: Backward, Forward, Full |

### 4. 핵심 알고리즘 / 패턴

- **Optimistic Concurrency Control**: `expectedVersion`과 Event Store의 `currentVersion` 비교 후, 일치 시에만 Append. 불일치 시 `ConcurrencyException` -> 클라이언트 재시도 또는 409 Conflict.
- **Event Replay & Rebuild**: `Read Model`을 `TRUNCATE` -> 모든 Stream을 처음부터 소비 -> 이벤트 순차 적용. 이때 외부 시스템 호출이 섞여 있으면 부작용(Side Effect) 발생 위험 -> **결정론적(Deterministic) 프로젝션** 강제.
- **Upcasting**: 이벤트 v1 -> v2 변환 시 저장된 원본은
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 453 / 600

<- **이전**: [452. 마이크로서비스 아키텍처 설계 패턴 심화](/studynote/11_design_supervision/06_exam_summary/452_msa_design_pattern_advanced)
**다음**: [454. 서킷 브레이커 패턴 장애 격리](/studynote/11_design_supervision/06_exam_summary/454_circuit_breaker_pattern/) ->

---
