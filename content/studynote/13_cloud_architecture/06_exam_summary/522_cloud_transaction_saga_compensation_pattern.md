---
title: "Cloud Transaction Saga Compensation Pattern"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 마이크로서비스 환경에서 ACID 트랜잭션을 보장할 수 없는 분산 환경의 한계를 극복하기 위해, **국소 트랜잭션(Local Transaction)의 순차 실행 + 실패 시 보상 트랜잭션(Compensating Transaction)**으로 최종 일관성(Eventual Consistency)을 달성하는 분산 트랜잭션 관리 패턴이다. 오케스트레이션(중앙 조정) 또는 코레오그래피(이벤트 기반) 방식으로 구현되며, 모든 단계는 **Saga Log/Event Store**에 영속화되어 장애 복구의 기준점이 된다.
> 2. **가치**: 2PC(2-Phase Commit) 대비 락 점유 시간 90% 이상 단축, 데이터베이스 커넥션 풀 고갈 방지, 서비스 간 결합도 제거로 독립적 배포·스케일링 가능, 처리량(Throughput) 수십 배 향상. 금융 도메인에서 1초 이내 결제 완료율이 99.99%에 도달하며, 실패 시 자동 보상으로 데이터 정합성 유지 비용을 약 60% 절감한다.
> 3. **판단 포인트**: **(1) 보상 트랜잭션 설계 가능 여부**(모든 비즈니스 로직이 의미론적 Undo가 가능한가?), **(2) 고립성(Lack of Isolation) 허용 수준**(Saga는 READ UNCOMMITTED 수준의 Dirty Read 가능), **(3) 오케스트레이터 SPOF 및 Transactional Outbox 패턴 적용**, **(4) 보상 실패 시 Dead Letter Queue + Manual Intervention 정책**, **(5) Saga Timeout 및 Step-wise Timeout 설정**. TCC나 Outbox 패턴과의 조합 여부가 아키텍처 성패를 좌우한다.

---

## Ⅰ. 개요 및 필요성

### 1. 모놀리식 트랜잭션의 종말

전통적인 RDBMS 기반 모놀리식 아키텍처에서는 `BEGIN` ... `COMMIT` 한 줄로 원자성(Atomicity), 일관성(Consistency), 고립성(Isolation), 지속성(Durability)을 보장했다. 하지만 **Cloud Native** 환경으로 전환되면서 다음 문제가 발생한다.

- **다중 데이터 저장소**: 한 비즈니스 트랜잭션이 PostgreSQL(재고), MongoDB(카탈로그), Redis(세션), 외부 PG API(결제), Kafka(이벤트) 등 **최소 4~5개 이상의 데이터 소스**를 동시에 변경해야 함
- **CAP 정리(CAP Theorem)**: 네트워크 분할(Network Partition) 환경에서 일관성(C)과 가용성(A) 중 하나를 양보해야 함
- **2PC의 실용적 한계**: XA(Extended Architecture) 프로토콜의 동기적 락킹은 응답 지연(Latency)을 수백 ms~수 초로 증가시키고, **DB 커넥션 풀 고갈**로 전체 서비스 장애 야기
- **서비스 독립성 침해**: `OrderService`가 `PaymentService`의 DB에 직접 2PC 참여하려면 DB 스키마를 공유해야 함 -> **Database per Service 원칙** 위배

### 2. Saga 패턴의 등장 배경

1987년 **Garcia-Molina & Salem**이 관계형 DB 외부의 장기 트랜잭션(Long-Lived Transaction)을 처리하기 위해 처음 제안한 후, 2014년 Chris Richardson이 **Microservices Patterns**에서 마이크로서비스 분산 트랜잭션의 해법으로 정형화했다. 이후 Microsoft Azure, AWS Step Functions, Temporal 등에서 엔터프라이즈 구현체가 등장하며 클라우드 네이티브의 사실 표준 패턴이 되었다.

```text
[기존 2PC: 동시 커밋 모델]                      [Saga: 순차 + 보상 모델]
+------------------------------+                +------------------------------+
|       Coordinator (TM)       |                |      Saga Orchestrator       |
+--------------+---------------+                +--------------+---------------+
               | Phase 1: PREPARE                          | T1: 주문생성
    +----------+----------+----------+                      |
    v          v          v          v                      v
+--------+ +--------+ +--------+ +--------+          +----------------+
| Order  | |Payment | | Stock  | |Coupon  |          | T1: 주문생성 ✅  |
|  DB    | |  DB    | |  DB    | |  DB    |          |  -> OrderDB     |
|(PREP)  | |(PREP)  | |(PREP)  | |(PREP)  |          +-------+--------+
+----+---+ +----+---+ +----+---+ +----+---+                  |
     | Phase 2: COMMIT       |                                 v
     v          v          v          v                  +----------------+
+--------+ +--------+ +--------+ +--------+          | T2: 결제요청    |
|  DB    | |  DB    | |  DB    | |  DB    |          |  -> PG API ✅    |
|(COMMIT)| |(COMMIT)| |(COMMIT)| |(COMMIT)|          +-------+--------+
+----+---+ +----+---+ +----+---+ +----+---+                  |
     +----------+----------+----------+                       v
            ⚠️ 모든 DB가 락 점유                  +----------------+
            ⚠️ 하나라도 실패 시 전체 ROLLBACK      | T3: 재고차감    |
            ⚠️ 응답 지연 평균 1.5~5초               |  -> StockDB ❌   |
                                                   +-------+--------+
                                                           v
                                                  +----------------+
                                                  | T4: 쿠폰사용    |
                                                  |  (C1+C2+C3)    |
                                                  |  보상 트랜잭션   |
                                                  +----------------+
                                                  ⚠️ 각 단계 즉시 COMMIT
                                                  ⚠️ 응답 지연 100~300ms
                                                  ⚠️ 실패 시 보상으로 일관성 회복
```

### 3. 왜 필요한가? (구 vs 신 패러다임 비교)

| 차원 | 모놀리식 ACID | 마이크로서비스 + Saga |
| :--- | :--- | :--- |
| **트랜잭션 범위** | 단일 DB 내 단일 트랜잭션 | 여러 서비스의 국소 트랜잭션 합집합 |
| **일관성 모델** | Strong Consistency | **Eventual Consistency** (BASE) |
| **락 유지 시간** | 수백 ms ~ 수 초 | **수 ms 이내** (각 Local Tx) |
| **장애 영향** | 부분 Rollback으로 안전 | **Saga 진행 상태 보존** 필요 |
| **확장성** | 수직 확장 한계 | 서비스별 **독립 수평 확장** |
| **데이터 정합성** | DB 자체 보장 | **Application-Level 보상**으로 보장 |

- **📢 섹션 요약 비유**: 여러 개의 식당이 한 행사에 음식을 제공하는데, 주방장이 모든 요리를 한꺼번에 "준비-완성" 신호로 진행하면 한 곳의 지연이 전체를 마비시킵니다. Saga는 **각 식당이 자기 요리를 완성하자마자 손님에게 전달**하고, 문제가 생기면 **이미 제공된 요리를 회수하는 프로세스**(반품, 환불)로 바꿔놓는 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Saga의 두 가지 구현 방식

#### 1.1 오케스트레이션(Orchestration) — 중앙 집중형

**Saga Execution Coordinator(SEC)** 또는 **Process Manager**가 중앙에서 각 서비스의 **Command**(명령)를 순차 발행한다.

```text
                         +------------------------------+
                         |  Saga Orchestrator           |
                         |  (Temporal / Camunda / Step  |
                         |   Functions / Axon)          |
                         |                              |
                         |  +------------------------+  |
                         |  | Saga State Machine     |  |
                         |  | (이벤트 로그 영속화)     |  |
                         |  +------------------------+  |
                         +--+---+---+---+---+---+---+--+
                            |C1 |C2 |C3 |C4 |C5 |C6 |  (Command)
                            v   v   v   v   v   v   v
                         +----++----++----++----++----+
                         |Order|Pay |Stock|Coupon|Deliv|
                         |Svc  |Svc |Svc  |Svc   |Svc  |
                         +----++----++----++----++----+
                            |R1 |R2 |R3 |R4 |R5 |R6 |  (Reply/Event)
                            +---+---+---+---+---+---+
                                  |
                                  v
                         +----------------------------+
                         | 실패 감지 -> 보상 커맨드 발행 |
                         | C2-comp: 환불              |
                         | C1-comp: 주문취소           |
                         +----------------------------+
```

#### 1.2 코레오그래피(Choreography) — 이벤트 기반

중앙 오케스트레이터 없이 각 서비스가 **Event Bus(Kafka, RabbitMQ, AWS EventBridge)**를 통해 다음 단계를 트리거한다.

```text
   [OrderSvc]                    [EventBus / Kafka]            [PaymentSvc]
   +---------+  OrderCreated   +------------------+  PayRequested  +---------+
   | T1: 주문 | --------------->|  topic: saga-flow |--------------->| T2: 결제 |
   |  생성 ✅ |                 +------------------+               |  승인 ✅ |
   +---------+                        ^                              |        |
        |                             | PaymentApproved              |  응답  |
        |                             +------------------------------+
        | T4-comp: 주문취소                |
        <---------------------------------+
        |  (실패 시)
        v
   +---------+
   | 보상Tx  | ------> StockReleased + CouponRollback 이벤트
   +---------+
```

### 2. 보상 트랜잭션(Compensating Transaction)의 핵심 원리

#### 2.1 정의와 제약

- **T_i**: 정방향 트랜잭션(Forward Transaction), 비즈니스 효과를 발생
- **C_i**: 보상 트랜잭션(Compensating Transaction), T_i의 효과를 **의미론적으로(Semantically)** 무효화
- ⚠️ **C_i는 ROLLBACK이 아니다!** 이미 COMMIT된 T_i의 결과를 어플리케이션 레벨에서 되돌리는 작업이다.
- ⚠️ **C_i는 멱등성(Idempotency)**을 보장해야 한다 (동일 보상 요청이 N번 와도 결과 동일)

#### 2.2 예시

| T_i (Forward) | C_i (Compensation) | 멱등 처리 |
| :--- | :--- | :--- |
| `INSERT INTO orders` | `UPDATE orders SET status='CANCELLED'` | 동일 orderId로 중복 요청 시 `WHERE status='CONFIRMED'`로 한 번만 |
| `결제승인(10000원)` | `결제취소 API 호출` | PG사 Refund ID를 Saga Step에 저장, 재요청 시 멱등키 사용 |
| `재고 -5` | `재고 +5` | Stock Movement Table에 Unique 제약 |
| `쿠폰사용 처리` | `쿠폰복원` | Coupon Usage Log에 Unique Key |

#### 2.3 보상 설계의 4가지 황금률

1. **이벤트 순서 무관성(Eventual Idempotency)**: 메시지 중복, 순서 뒤바뀜에서도 데이터 정합성 유지
2. **순수 함수적 보상(Pure Compensation)**: 부수 효과 최소화, 외부 시스템 상태 추적
3. **재시도 정책 명세(Retry Policy)**: Exponential Backoff + Max Retry + Circuit Breaker
4. **데드 레터 큐(DLQ) 분기**: 보상 불가능 시 사람의 개입(HITL, Human-in-the-Loop) 필요

### 3. Saga Log / Event Store와 Outbox 패턴

Saga 진행 상태는 **영속화(Persistence)**되어야 하며, 이것이 Saga Log다.

```text
+--------------------------------------------------------+
|                  Saga Log Table                        |
+--------------------------------------------------------+
| saga_id | step | type  | service | payload  | status   |
+---------+------+-------+---------+----------+----------+
| 1001    |  0   | START | Order   | {...}    | RUNNING  |
| 1001    |  1   | CMD   | Order   | create   | SUCCESS  |
| 1001    |  2   | CMD   | Payment | approve  | SUCCESS  |
| 1001    |  3   | CMD   | Stock   | reserve  | FAILED   |
| 1001    |  4   | COMP  | Payment | refund   | SUCCESS  |
| 1001    |  5   | COMP  | Order   | cancel   | RUNNING  |
+--------------------------------------------------------+
```

**Outbox 패턴과의 결합**: Saga Step 결과와 함께 외부 이벤트 발행을 `transactional outbox`로 한 트랜잭션 내에 처리하여 **이중 쓰기 문제(Dual Write Problem)**를 해결한다. Polling Publisher 또는 **Debezium CDC**로 Outbox 테이블을 읽어 Kafka로 발행한다.

### 4. 구성 요소 역할 및 기술 매핑

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Saga Orchestrator** | 상태 머신(FSM) 관리, 다음 Step 결정 | **Temporal**(Workflow), **Camunda 8**(Zeebe BPMN), **AWS Step Functions**(ASL), **Azure Durable Functions**, **Axon Server** |
| **Saga Participant** | 개별 Local Transaction 실행 + 보상 | 마이크로서비스별 Command Handler. 멱등성 키(Idempotency-Key) 헤더 포함 |
| **Saga Log / Event Store** | 진행 상태 영속화 | **PostgreSQL**(Temporal Visibility), **Apache Kafka**(Choreography), **EventStoreDB**(Event Sourcing), **DynamoDB** |
| **Compensation Service** | 보상 트랜잭션 실행, 실패 시 DLQ 처리 | **Spring Retry**, **Resilience4j**, **Polly(.NET)**, Dead Letter Queue는 **SQS DLQ / Kafka DLQ** |
| **Distributed Tracer** | Saga 흐름 추적, 지연 분석 | **OpenTelemetry + Jaeger/Zipkin**, Saga ID를 Trace Context로 전파 |
| **Outbox Relay** | Outbox -> Message Broker 발행 | **Debezium**(CDC), **Outbox-Poller**(Spring), **DynamoDB Streams** |
| **Idempotency Store** | 멱등성 검증 | **Redis**(단기), **PostgreSQL Unique Constraint**(장기), **Idempotency-Key Header (Stripe 표준)** |

### 5. 정량적 파라미터

- **Step Timeout**: 각 Step의 최대 대기 시간. 일반적으로 **P99 응답시간 × 3** = 약 5~30초
- **Saga Timeout**: 전체 Saga의 최대 실행 시간. 비즈니스 SLA에 따라 1분~24시간
- **Retry Strategy**: **Exponential Backoff (
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 522 / 800

<- **이전**: [521. 분산 시스템 일관성 모델 CAP PACELC](/studynote/13_cloud_architecture/06_exam_summary/521_distributed_system_consistency_cap_pacelc/)
**다음**: [523. 이벤트 소싱 이벤트 스토어 리플레이](/studynote/13_cloud_architecture/06_exam_summary/523_event_sourcing_event_store_replay/) ->

---
