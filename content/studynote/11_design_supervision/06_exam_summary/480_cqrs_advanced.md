+++
title = "480. CQRS 명령 조회 분리 패턴 심화 (CQRS Command Query Separation Advanced)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CQRS는 단일 모델에서 Command(상태 변경)와 Query(조회)의 책임과 데이터 저장소·트랜잭션 모델·확장성 정책을 **물리적으로 분리**하여, 쓰기 경로의 무결성과 읽기 경로의 응답성을 독립적으로 최적화하는 아키텍처 패턴이다. 심화 단계에서는 Event Sourcing, Projection, Saga, Polyglot Persistence가 결합된 **이벤트 주도 비동기 시스템**으로 진화한다.
> 2. **가치**: 쓰기/읽기 트래픽이 100:1 이상으로 비대칭이거나, 조회 화면이 10종 이상이며 각기 다른 비정규 뷰를 요구하는 도메인에서 **읽기 p99 latency 70~90% 감소**, **DB write throughput 3~5배 향상**, **이벤트 로그 기반 감사·시간여행 디버깅·이벤트 재투영을 통한 신규 read model 무중단 추가**라는 정량적 가치를 제공한다.
> 3. **판단 포인트**: 모든 시스템에 CQRS를 적용해서는 안 된다. **도메인 복잡도(협상·승인·불변식 다수)**, **읽기/쓰기 비율 비대칭성**, **읽기 모델 다변성**, **팀의 이벤트 기반 설계 역량**이 임계치를 넘어야 도입을 정당화할 수 있다. 핵심 트레이드오프는 *강한 일관성(Strong Consistency) ↔ 결과적 일관성(Eventually Consistent)*, *단일 DB 단순성 ↔ 다중 저장소 운영 복잡성*이다.

---

## Ⅰ. 개요 및 필요성

전통적인 CRUD 아키텍처는 하나의 애그리거트(예: `Order`)를 **정규화된 3NF 테이블**에 저장하고, ORM(JPA/Hibernate) 매핑을 통해 동일한 도메인 객체를 Command 처리와 Query 응답 양쪽에 사용한다. 이러한 "단일 모델" 방식은 다음과 같은 한계에 부딪힌다.

1. **읽기·쓰기 요구사항 충돌**: 쓰기는 강한 ACID와 무결성 제약(FK, Check Constraint, 낙관적 락)이 필요하지만, 조회는 비정규화·全文 검색·집계·정렬·페이지네이션 최적화가 필요하다. 한 테이블에 두 트레이드오프를 공존시키면 인덱스 폭증과 락 경합이 발생한다.
2. **확장성 비대칭**: 전자상거래·IoT·금융 거래 시스템에서 쓰기 트래픽은 초당 수백~수천 건 수준이지만, 동일 도메인의 조회는 캐시 미스 시 초당 수만~수백만 건에 달한다. 단일 RDB는 이 두 부하를 같은 connection pool과 같은 디스크 IO로 감당해야 하므로 **수직 확장 한계**에 빠르게 도달한다.
3. **모델 변형 폭발**: "주문 상세 조회"가 모바일 앱·웹·관리자 대시보드·B2B EDI별로 다른 컬럼·집계·정렬 기준을 요구하면, 동일한 도메인 객체에 **@SecondaryTable, DTO Projection, View SQL**이 난립하여 도메인 모델이 오염된다.
4. **감사·추적 요구**: 금융·의료 도메인은 누가·언제·어떤 값으로 무엇을 변경했는지를 immutable log로 보존해야 한다. CRUD는 update/delete로 인해 이력을 직접 보존하지 못한다.

CQRS는 2010년 Bertrand Meyer의 *CQS(Command-Query Separation)* 원칙을 분산 시스템 수준으로 확장한 **Greg Young(2010)·Udi Dahan(2009)**의 패턴이다. 단일 애플리케이션의 함수 수준 원칙을 넘어, **쓰기 모델(Write Side)·읽기 모델(Read Side)·이벤트 스토어(Event Store)·프로젝션(Projection)·프로세스 매니저(Saga)**의 5개 컴포넌트로 시스템을 분리한다.

```text
+------------------- Legacy CRUD Architecture -------------------+
|                                                                 |
|   Client --► [Web/API] --► [Service] --► [ORM Domain Model]     |
|                                    |                            |
|                                    v                            |
|                            +--------------+                    |
|                            |  RDB (3NF)   |  ◄-- 동일 모델      |
|                            |  Order,Item  |      read+write     |
|                            |  + Indexes   |      양쪽 책임      |
|                            +--------------+                    |
|                                   |                             |
|   Read API ◄-- DTO/JOIN/View ----+                             |
|   (Slow due to lock contention, index bloat)                   |
+-----------------------------------------------------------------+

                              v v v  REFACTOR  v v v

+-------------------- CQRS + Event Sourcing ----------------------+
|                                                                 |
|  Write Side                Event Bus            Read Side       |
|  +------------+         +----------+         +------------+    |
|  |  Command   |--------►|  Kafka   |--------►| Projection |    |
|  |  Handler   | Domain  |  Topic   | Events  |  Workers   |    |
|  |  (Aggregate)| Events |  3 nodes |         +-----+------+    |
|  +-----+------+         +----------+               |           |
|        | append()                            +------v------+    |
|        v                                     |  Read DB    |    |
|  +------------+                              | (Denormal)  |    |
|  | EventStore | --► Snapshot + Snapshot --►   | ES/Redis/   |    |
|  | (append    |     Replay (새 view)         | MongoDB     |    |
|  |  only log) |                              +-------------+    |
|  +------------+                                                 |
+-----------------------------------------------------------------+
```

**Legacy vs CQRS 패러다임 비교**

| 차원 | CRUD Monolith | CQRS Advanced |
| :--- | :--- | :--- |
| 데이터 표현 | 1개의 정규화 모델 | N개의 비정규 read model + 1개의 이벤트 스트림 |
| 트랜잭션 | 단일 ACID, 즉시 일관 | 쓰기는 이벤트 append, 조회는 eventually consistent |
| 확장 단위 | DB 인스턴스 1개 | Command Side / Read Side / Projection 각각 독립 확장 |
| 변경 이력 | update로 덮어씀 | 이벤트 로그로 영구 보존 (immutable) |
| 신규 뷰 추가 | 스키마 변경 + 마이그레이션 | 새 Projection Worker 배포만으로 무중단 추가 |
| 복잡도 | 낮음 | 중~고 (이벤트 스키마 진화, projection lag 모니터링 필수) |

- **📢 섹션 요약 비유**: CRUD는 "주방과 홀이 같은 도마 하나로 요리와 접시 세척을 번갈아 하는 셰프"이고, CQRS는 "주방(명령)은 칼·불·냉장고만, 홀(조회)은 트레이·메뉴판·POS만, 그 사이를 웨이터(이벤트 버스)가 음식을 운반하는 전문 레스토랑"이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

심화 CQRS 시스템은 5개 계층으로 구성된다. 각 계층의 책임·기술 선택·통신 프로토콜을 명확히 구분하는 것이 실무 역량의 핵심이다.

```text
                    +----------------------------------------+
                    |             Client / UI Layer          |
                    |  (Web/Mobile, BFF GraphQL, gRPC stub)  |
                    +--------------+--------------+----------+
                                   |              |
                          Command (POST/PUT)   Query (GET)
                                   |              |
            +----------------------v-+          +-v---------------------+
            |   Write API (Spring    |          |   Read API (FastAPI / |
            |   Boot + Axon/AxonIQ)  |          |   Node + GraphQL)     |
            |   • AuthN/Z, RateLimit |          |   • Cache (Redis/CDN) |
            |   • Idempotency-Key    |          |   • Read-after-write  |
            |   • Aggregate Lock     |          |     hinting           |
            +----------+-------------+          +-^---------------------+
                       |                           |
                       v                           |
            +----------------------+               |
            |   Aggregate (Domain) |               |
            |   • loadFromHistory()|               |
            |   • decide(cmd)->evt  |               |
            |   • apply(evt) state |               |
            |   • @EventSourcing   |               |
            +----------+-----------+               |
                       | events[]                  |
                       v                           |
            +----------------------+               |
            |   EventStore         |               |
            |  +----------------+  |               |
            |  |Stream:order-123|  |               |
            |  |0:Created       |  |               |
            |  |1:ItemAdded     |  |               |
            |  |2:Shipped       |  |               |
            |  |...append only..|  |               |
            |  +----------------+  |               |
            |  (EventStoreDB /     |               |
            |   Kafka+Compacted /  |               |
            |   Postgres+JSONB)    |               |
            +----------+-----------+               |
                       | publish                   |
                       v                           |
            +----------------------+               |
            |   Message Broker     |               |
            |  (Kafka/RabbitMQ/    |               |
            |   Pulsar/NATS)       |               |
            |  • Ordered per agg   |               |
            |  • DLQ + Retry       |               |
            |  • Schema Registry   |               |
            +----------+-----------+               |
                       | subscribe (per view)     |
        +--------------+--------------+------------+
        v              v              v            v
   +---------+    +---------+    +---------+  +---------+
   | Proj. A |    | Proj. B |    | Proj. C |  | Proj. D |
   |OrderSum |    |SearchIdx|    |DashAgg  |  | AuditLog|
   |-> MySQL  |    |-> ES     |    |-> Redis  |  |-> S3     |
   +----+----+    +----+----+    +----+----+  +---------+
        |              |              |
        +--------------+--------------+
                       | API queryable
                       +------------------► Read API
```

### 1. Command Side (쓰기 경로)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Command DTO** | 사용자 의도 표현, 불변 객체 | `record CreateOrderCmd(String id, List<LineItem> items)`; 유효성 검증은 Bean Validation(Java) / FluentValidation(.NET) / Pydantic |
| **Aggregate Root** | 도메인 불변식 강제, 라이프사이클 캡슐화 | `Order` 엔티티: `create()`, `addItem()`, `ship()` 메서드 안에서 비즈니스 규칙(예: 출하 후 아이템 변경 불가) 검증. 외부에서는 `getter`로 상태 조회만 허용 |
| **Command Handler** | Aggregate 라이프사이클·트랜잭션 경계 관리 | Axon `@CommandHandler`, Spring `@Transactional` + `AggregateLifecycle.apply(event)`. **트랜잭션 = 1 커맨드 = N 이벤트 append** |
| **Event Store** | 이벤트 스트림 영구 저장, Optimistic Concurrency | EventStoreDB(20k events/sec/stream), Axon Server, Kafka compacted topic(`min.cleanable.dirty.ratio`, `segment.ms`), Postgres + JSONB(`UNIQUE(stream_id, version)`) |
| **Idempotency Layer** | 중복 커맨드 방지 | `Idempotency-Key` HTTP 헤더 -> 별도 저장소(Redis SETNX TTL 24h)에 키-결과 매핑. 결제·PG 연동에서 필수 |
| **Saga / Process Manager** | 다중 애그리거트 간 장기 트랜잭션 | `OrderSaga`: `OrderCreated -> reserveInventory -> PaymentRequested -> PaymentCompleted -> OrderConfirmed`. **Choreography(중앙 orchestrator 없음) vs Orchestration(중앙 BP) trade-off** |

### 2. Read Side (읽기 경로)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Projection Worker** | 이벤트 스트림을 소비하여 read model 갱신 | At-least-once 소비 -> 멱등 처리(예: `(aggregate_id, version)` UPSERT). Spring Cloud Stream, Kafka Streams DSL, Debezium CDC |
| **Polyglot Read DB** | 뷰 특화 저장소 | MySQL(트랜잭션 뷰), PostgreSQL+JSONB(반정형), Elasticsearch(全文/형태소/지리 검색), Redis(ZSET/SortedSet 랭킹), ClickHouse(시계열 집계), MongoDB(다형성 문서) |
| **Read API** | CQRS의 Q, 캐시 친화적 응답 | GraphQL(DataLoader로 N+1 해결), REST+JPA(읽기 전용 `@Transactional(readOnly=true)`), gRPC streaming(실시간 push) |
| **Catch-up Subscription** | 신규 projection이 과거 이벤트 재처리 | `$all` 백필 잡 -> `currentPosition` 저장 -> `live` tail로 전환. EventStore의 `$projections` 모드(`continuous`, `transient`, `oneTime`) |
| **Snapshot Store** | Aggregate 재구성 비용 절감 | 100개 이벤트마다 또는 1MB 초과 시 snapshot. Snapshot 자체도 이벤트처럼 append하고, `loadFromSnapshot+tail`로 최신 상태 복원 |
| **Materialized View Cache** | 핫키·페이지 단위 캐시 | Redis Cluster(Shard by aggregate id), Caffeine L1(서버 로컬), CDN(Etag/Last-Modified). 캐시 invalidation은 TTL이 아닌 **event-driven purge** 권장 |

### 3. Event Bus & Schema Evolution

이벤트 스키마는 **불변(immutable)**이다. 호환성 규칙은 다음과 같다.

- **Backward Compatible (Consumer 호환)**: 필드 추가(기본값 있음), enum 신규 값 추가. Avro/Protobuf는 `default` 키워드로 처리.
- **Forward Compatible (Producer 호환)**: 필드 제거는 *소비자*가 모두 새 스키마로 배포된 후 진행.
- **Major 버전 전략**: `OrderCreated_v1` -> `OrderCreated_v2`로 topic 분리, 두 버전을 동시에 routing하는 Upcaster 작성(Axon `EventUpcaster`).

### 4. 일관성 모델 (Consistency Model)

| 모델 | 지연 | 적용 시나리오 |
| :--- | :--- | :--- |
| **Strong Consistency** | 0ms (단일 트랜잭션) | 쓰기 후 동일 aggregate 재조회 (Read-your-own-writes hint) |
| **Causal Consistency** | < 10ms | 동일 사용자 세션의 후속 조회, Kafka 동일 partition key 순서 보장 |
| **Read-your-writes** | ~ projection lag | UI에서 "주문 완료" 클릭 후 마이페이지에 반영되어야 함 -> projection lag이 작은 read replica 라우팅 |
| **Bounded Staleness** | k ms (예: 1초) | 대시보드·추천·검색 인덱스 (Elasticsearch `index.refresh_interval=1s`) |
| **Eventual Consistency** | 무제한 (수렴 보장) | 통계·집계·BI·냉장고 같은 부가 read model |

**Projection Lag SLO 예시**: 95 percentile < 2초, 99 percentile < 10초, 99.9 percentile < 60초. 초과 시 `projection_lag_seconds` Prometheus 알람 -> PagerDuty.

### 5. Saga의 보상 트랜잭션 (Compensation)

```text
OrderCreated
   |  +--------------------------------------------------+
   +--►| Saga: OrderFulfillmentSaga                      |
   |   |  step1: Inventory.reserve()                     |
   |   |     success -► step2: Payment.charge()          |
   |   |     failure  -► step2: Payment.charge()         |
   |   |                     success -► ✓
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 480 / 600

<- **이전**: [479. 양파 아키텍처 계층 분리](/knowledge-base/studynote/11_design_supervision/06_exam_summary/480_onion_architecture/)
**다음**: [481. 감리 프로세스 자산 관리 체계](/knowledge-base/studynote/11_design_supervision/06_exam_summary/481_audit_process_asset_management/) ->

---
