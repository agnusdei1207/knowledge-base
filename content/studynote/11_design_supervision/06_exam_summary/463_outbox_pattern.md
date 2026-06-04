+++
title = "463. 아웃박스 패턴 메시지 보장 (Outbox Pattern Message Guarantee)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 마이크로서비스 환경에서 발생하는 **이중 쓰기 문제(Dual Write Problem)** 를 원자적 트랜잭션(Atomic Transaction) 내 메시지 저장(Outbox 테이블)으로 회피하여, 비즈니스 데이터 변경과 이벤트 발행을 **트랜잭션 일관성(Transactional Consistency)** 하에 결합하는 분산 트랜잭션 대안 패턴이다.
> 2. **가치**: 2PC(Two-Phase Commit) 대비 **가용성·확장성**을 확보하면서 **최소 1회 전달(At-Least-Once Delivery)** 을 보장하며, Debezium 등 CDC(Change Data Capture) 도구와 결합 시 지연 시간(Latency)을 **수십 ms 수준**으로 단축하고 시스템 간 결합도를 제거한다.
> 3. **판단 포인트**: 구현 난이도, 메시지 순서 보장(Per-Aggregate Ordering), 멱등성(Idempotency) 처리, Outbox 테이블 정리(Archiving) 정책, Polling vs Log-Tailing 방식 선택, 그리고 **Hot Partition** 문제 회피를 위한 파티셔닝/셔딩 전략이 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

### 1.1 분산 환경에서의 메시지 발행 딜레마

MSA(Microservice Architecture) 환경에서 한 트랜잭션이 "주문 생성"과 "주문 완료 이벤트 발행" 두 작업을 동시에 수행해야 할 때, 개발자는 본질적인 모순에 직면한다. **RDBMS는 ACID 트랜잭션을, Kafka/RabbitMQ 같은 Message Broker는 AMQP/Producer-Consumer 프로토콜을 제공**하지만, 둘은 서로 다른 시스템이라 단일 원자성(Atomicity)을 제공할 수 없다.

기존의 모놀리식 아키텍처에서는 RDBMS 내 단일 트랜잭션으로 모든 비즈니스 로직을 처리했기에 메시지 발행 자체가 불필요했다. 그러나 서비스가 분리되면서 **서비스 간 상태 전파**는 결국 비동기 메시지 또는 HTTP API 호출로 대체되었고, 그중 이벤트 기반(Event-Driven) 통신은 **느슨한 결합(Loose Coupling)** 과 **확장성** 측면에서 우월하다.

### 1.2 이중 쓰기 문제(Dual Write Problem)

```text
+------------------------------------------------------------------+
|              Dual Write Problem (기존 방식의 결함)                  |
+------------------------------------------------------------------+

   [Order Service] --- ① 주문 INSERT ---► [Order DB]
        |
        |  ② 주문완료 이벤트 PUBLISH (별도 네트워크 호출)
        v
   [Kafka Broker] -----► [Inventory Service]
        |
        |
   ⚠️  ① 성공, ② 실패 시?
       -> 주문은 생성되었으나 이벤트는 유실 (데이터 불일치)
   ⚠️  ① 실패, ② 성공 시?
       -> Phantom Event (주문 없는 이벤트 발행)
   ⚠️  ①·② 사이 네트워크 단절?
       -> 정합성 깨짐, 보상 트랜잭션(Compensating Transaction) 필요
```

### 1.3 왜 Outbox Pattern인가?

이 문제를 해결하기 위한 후보 기술은 **2PC(2-Phase Commit)**, **XA Transaction**, **Saga Pattern** 등이 존재하지만, 각각 명확한 한계를 가진다.

- **2PC/XA**: Message Broker가 XA를 지원하지 않거나(Kafka는 미지원), Coordinator 장애 시 **Blocking 문제** 발생
- **Saga**: 보상 트랜잭션을 직접 설계해야 하며, 비즈니스 로직 복잡도 증가, **장기 트랜잭션** 부적합
- **Event Sourcing**: 도메인 모델 자체를 이벤트 중심으로 재설계해야 하므로 기존 CRUD 시스템에 적용 어려움

**Outbox Pattern**은 이러한 한계를 우회하면서도 **기존 CRUD 트랜잭션 모델**을 그대로 유지할 수 있는 현실적 해법이다. 핵심 아이디어는 단순하다: **"이벤트도 DB의 한 Row로 취급하라"**.

### 1.4 패러다임 전환: Before vs After

| 구분 | 모놀리식 + JMS | MSA + Outbox Pattern |
|:-----|:--------------|:---------------------|
| 트랜잭션 경계 | 단일 DB + EJB/JTA | 비즈니스 DB + Outbox 테이블 (단일 트랜잭션) |
| 메시지 신뢰성 | XA/JTA 기반 보장 | CDC + Idempotent Consumer로 보장 |
| 장애 시 동작 | Coordinator 복구 대기 | DB WAL(Log) 기반 재처리 |
| 시스템 결합도 | 강한 결합(Strong Coupling) | DB 스키마만 공유, 서비스는 독립 |

- **📢 섹션 요약 비유**: 택배가 두 곳(창고 A, 택배사 B)에 동시에 도착해야 하는데 한 곳에만 보낸 상황입니다. 택배 상자를 "창고 안 박스"에 넣어두고, 별도 직원이 박스만 모아 택배사에 전달하면 **한 번의 거래로 두 곳에 모두 확실히** 보낼 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Outbox Pattern의 핵심 메커니즘

```text
+------------------------------------------------------------------------+
|              Outbox Pattern 상세 아키텍처 (Log-Tailing 방식)            |
+------------------------------------------------------------------------+

  [Client] --HTTP--► [Order Service]
                         |
                         |  @Transactional BEGIN
                         |  +------------------------------+
                         +-►| 1. INSERT INTO orders ...    |
                         |  | 2. INSERT INTO outbox (      |◄--+
                         |  |     event_id, aggregate_type, |   |
                         |  |     aggregate_id, payload,   |   |
                         |  |     created_at, status='NEW')|   |
                         |  +------------------------------+   |
                         |  COMMIT (단일 원자성)                    |
                         v                                       |
                  [Order DB]                                     |
                  +------+------+                                |
                  |  orders     |                                |
                  |  outbox     |◄----------------------------+  |
                  +------+------+                             |  |
                         |  binlog/WAL streaming             |  |
                         |  (Debezium Engine)                 |  |
                         v                                    |  |
                  [Kafka Connect] ---- CDC Source ------------+  |
                         |                                    |
                         |  (commit_log_offset, snapshot)     |
                         v                                    |
                  [Kafka Topic: order.events]                 |
                         |                                    |
                         |  consumer group                    |
                         v                                    |
                  [Inventory Service / Notification / ...]     |
                                                            |
   ----------------------------------------------------------+
   별도 Polling Worker (Fallback)
   [Outbox Poller] --- SELECT * FROM outbox WHERE status='NEW' --► [Broker]
   (5~30초 주기, 1000건 배치, status='SENT' 마킹)
```

### 2.2 구성 요소별 역할

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Business Service** | 도메인 로직 + Outbox Row 동시 INSERT | Spring `@Transactional`, JPA `@TransactionalEventListener(AFTER_COMMIT)`, JDBC BATCH INSERT |
| **Outbox 테이블** | 미발행 이벤트 저장소, 단일 진실 공급원(SSOT) | 스키마: `id BIGINT PK, aggregate_type, aggregate_id, event_type, payload JSON, headers MAP, created_at, processed_at, status(NEW/SENT/FAILED), retry_count, version` |
| **CDC Engine (Debezium)** | DB의 `binlog`(MySQL) / `WAL`(Postgres) / `redo log`(Oracle) 실시간 스트리밍 | `io.debezium.connector.mysql.MySqlConnector`, Kafka Connect REST API로 offset 관리, **Log-Based** -> 지연 50ms 이하 |
| **Message Relay (Polling)** | CDC 장애 대비(Fallback) 또는 단순 구현 시 사용 | `SELECT ... FOR UPDATE SKIP LOCKED`, `@Scheduled(fixedDelay)`, MySQL 8.0+ 또는 Postgres 전용 |
| **Message Broker** | 이벤트 수신·배포·저장 | Kafka(파티션 기반 순서), RabbitMQ(routing key), RocketMQ(`TransactionListener` 네이티브 지원) |
| **Consumer Service** | 멱등성 보장하며 비즈니스 처리 | `Idempotency-Key` 헤더, DB Unique Constraint, Inbox 테이블 패턴 병행 |
| **Outbox Purger** | 처리 완료 Row 정리(아카이빙) | `DELETE WHERE processed_at < NOW() - 7d` 또는 S3/GCS 콜드 스토리지 이전 |
| **Monitoring & DLQ** | 실패 추적, 알람, 데드 레터 큐 | Prometheus `outbox_lag_seconds`, `outbox_pending_count` 메트릭, `retry_count > 5` 시 DLQ |

### 2.3 핵심 알고리즘 및 트랜잭션 원리

#### ① 이벤트 발행을 트랜잭션 내부로 흡수하는 알고리즘 (Pseudocode)

```java
@Transactional  // 단일 트랜잭션
public Order createOrder(OrderRequest req) {
    // 1) 비즈니스 데이터 저장
    Order order = orderRepository.save(new Order(req));

    // 2) 동일 트랜잭션 내에서 Outbox Row 저장
    OutboxEvent event = OutboxEvent.builder()
        .aggregateType("Order")
        .aggregateId(order.getId())
        .eventType("OrderCreated")
        .payload(toJson(order))
        .headers(Map.of("traceId", MDC.get("traceId")))
        .status(OutboxStatus.NEW)
        .createdAt(Instant.now())
        .build();
    outboxRepository.save(event);

    // 트랜잭션 COMMIT 시점에 두 Row가 함께 영구화 (Atomicity)
    return order;
}
```

이후 **커밋 이후**(`AFTER_COMMIT`)에 발행이 일어나야 하므로 다음 두 방식 중 하나를 선택한다.

#### ② Polling Publisher 방식

```text
+----------------------------------------+
|  Scheduled Task (every 1~5 sec)        |
+----------------------------------------+
| 1. BEGIN TX                             |
| 2. SELECT * FROM outbox                |
|    WHERE status = 'NEW'                |
|    ORDER BY id                          |
|    LIMIT 100                            |
|    FOR UPDATE SKIP LOCKED   ◄-- 동시성 |
| 3. publishToBroker(events)              |
| 4. UPDATE outbox                       |
|    SET status = 'SENT',                |
|        processed_at = NOW()            |
| 5. COMMIT                              |
+----------------------------------------+
```

- **장점**: 구현 단순, 단일 DB로 충분
- **단점**: 폴링 지연, DB 부하, Hot Row 문제

#### ③ Transaction Log Tailing (CDC) 방식

```text
+--------------------------------------------------+
|  Debezium MySQL Connector 설정 (예시)            |
+--------------------------------------------------+
|  connector.class: io.debezium.connector.mysql   |
|  database.hostname: order-db                     |
|  database.port: 3306                             |
|  database.user: debezium                         |
|  database.server.id: 184054                      |
|  table.include.list: mydb.outbox                 |
|  transforms: outbox.route                        |
|  transforms.outbox.route.type: org.apache.kafka  |
|    .connect.transforms.RegexRouter                |
|  transforms.outbox.route.regex:                  |
|    (.*)                                          |
|  transforms.outbox.route.replacement:            |
|    outbox.events.$1                              |
|  snapshot.mode: schema_only    ◄-- 스냅샷 미사용  |
|  tombstones.on.delete: false                     |
+--------------------------------------------------+
```

- **장점**: 실시간(수십 ms), DB 부하 없음, 트랜잭션 순서 보장
- **단점**: CDC 인프라 필요(Debezium + Kafka Connect), DB별 WAL 형식 차이, Schema Evolution 관리

### 2.4 멱등성(Idempotency) 및 순서 보장

| 보장 범위 | 메커니즘 | 구현 코드 포인트 |
|:---------|:--------|:----------------|
| **At-Least-Once** | Polling 재시도 또는 CDC offset 리셋 | Broker는 중복 수신 가능 |
| **Exactly-Once-Effect** | Consumer 멱등 키 + DB Unique Constraint | `INSERT ... ON CONFLICT DO NOTHING` (Postgres) |
| **Per-Aggregate Order** | `aggregate_id` 기준 Kafka 동일 파티션 라우팅, 또는 Outbox `seq_no` 필드 사용 | `key=aggregateId`, Consumer는 순서 처리 후 commit |
| **Strict Global Order** | 단일 파티션 사용 시 가능하나 처리량 저하 | 일반적으로 권장하지 않음 |

- **📢 섹션 요약 비유**: 학급 우편함(Outbox 테이블)에 선생님에게 보낼 편지(이벤트)를 넣어두면, 전학생(CDC)이 매일 아침 우편함만 훑어 우체국(Broker)에 가져갑니다. 편지가 사라져도 우편함 기록으로 재발송이 가능하고, **학급 전체에 동일 순서**로 전달되도록 출석번호(aggregate_id) 순으로 분류합니다.

---

## Ⅲ. 비교 및 연결

### 3.1 유사 패턴/기술 비교

| 구분 | **Outbox Pattern (CDC)** | **Outbox Pattern (Polling)** | **2PC / XA** | **Event Sourcing** | **Kafka Transactional Producer** |
|:-----|:------------------------|:-----------------------------|:------------|:-------------------|:---------------------------------|
| **데이터 정합성** | Strong (DB 단일 트랜잭션) | Strong (단일 트랜잭션) | Strong (분산 락) | Strong (이벤트가 SSOT) | Weak (Producer 측 단독 보장) |
| **시스템 결합도** | DB 스키마만 결합 | DB 스키마만 결합 | 모든 노드가 XA 지원 | 서비스별로 분리 | Broker에 결합 |
| **지연 시간** | 50~500ms | 1~30초 (폴링 주기) | 네트워크 RTT × 2 | 100ms 이하 | 5~50ms |
| **장애 복구** | CDC offset 리셋 | Polling 재시도 | Coordinator 복구 | Event Replay | Producer Fencing |
| **구현 복잡도** | 중 (Debezium 필요) | 하 (단순 쿼리) | 상 (XA 드라이버) | 상 (CQRS 강제) | 중 (Producer API) |
| **스케일아웃 한계** | Log I/O에 의존 | Poller 인스턴스 수 | Coordinator 병목 | 이벤트 저장소 성능 | Partition 수 |
| **순서 보장** | Per-Aggregate 가능 | Per-Aggregate 가능 | 전역 보장 | 시간순 보장 | Per-Partition 보장 |
| **적합 시나리오** | 일반 MSA, 고가용성 | 소규모, 단순화 필요 | 단일 DB + Broker 동종 | 금융 도메인, 감사 | Stream Processing |
| **주요 도구** | Debezium, Maxwell, Canal, AWS DMS | Spring `@Scheduled` | Atomikos, Narayana | Axon, EventStoreDB | Kafka EOS API |

### 3.2 인접 시스템과의 통합

| 통합 대상 | 연결 방식 | 기술적 고려사항 |
|:---------|:---------|:---------------|
| **API Gateway** | Event 발행 후 Webhook으로 동기 응답 | 멱등 토큰을 `Idempotency-Key` 헤더로 전달 |
| **Event Bus (Kafka)** | Debezium이 직접
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 463 / 600

<- **이전**: [462. 리트라이 패턴 지수 백오프](/knowledge-base/studynote/11_design_supervision/06_exam_summary/463_retry_pattern/)
**다음**: [464. 데이터베이스 퍼 서비스 독립 저장소](/knowledge-base/studynote/11_design_supervision/06_exam_summary/464_database_per_service/) ->

---
