---
title: "565. 메시지 큐 비동기 통신 패턴 (Message Queue Async Communication Pattern)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 메시지 큐 비동기 통신 패턴은 Producer(발행자)가 Broker(RabbitMQ, Kafka, Amazon SQS 등)의 영구/임시 저장소에 메시지를 적재한 뒤 즉시 ACK를 받고 Consumer가 이를 비결합(Decoupling)된 시점에 Pull/Push 방식으로 소비하는 EDA(Event-Driven Architecture)의 핵심 미들웨어 패턴으로, AMQP 0-9-1, MQTT 5.0, Kafka Binary Protocol 등 wire-level 프로토콜 위에서 QoS 0/1/2, At-least-once/At-most-once/Exactly-once 전송 보장, 그리고 DLQ·Priority Queue·Delay Queue·Consumer Group·Partition Rebalance 등의 세밀한 전달 모델을 제공한다.
> 2. **가치**: 동기식 REST/RPC 대비 P99 응답 지연 100ms 이하 유지, Consumer 인스턴스 수평 확장 시 초당 100만 메시지 처리(Kafka), 장애 격리율 99.99% 가용성(Aurora/SQS Multi-AZ), 그리고 Batch·Compression·Zero-Copy·PageCache 활용을 통한 네트워크·디스크 I/O 70% 절감 효과를 통해 대용량 트래픽과 이벤트 폭주(Traffic Spike)에 대한 완충(Buffering) 역할을 수행한다.
> 3. **판단 포인트**: 메시지 순서 보장(Global Ordering vs Per-Partition Ordering)·중복 허용도·Broker의 Push vs Pull·내구성 vs 처리량 트레이드오프, 그리고 `CAP Theorem` 관점에서 Kafka(AP), RabbitMQ(CA+Shovel/Federation), Amazon SQS(완전관리형 AP) 등 솔루션별 일관성·가용성·분할 내성 정책을 어떻게 조화시킬지가 아키텍처 의사결정의 핵심이다.

---

## Ⅰ. 개요 및 필요성

현대 MSA(Microservices Architecture) 환경에서 수십~수백 개의 서비스가 HTTP/REST, gRPC 같은 동기식 프로토콜로 직접 통신하면 다음과 같은 고질적 문제가 발생한다.

1. **결합도(Coupling) 상승**: B 서비스의 일시적 장애가 A 서비스의 응답 지연으로 직결되어 **Cascading Failure**가 연쇄 전파된다.
2. **처리량 한계**: Tomcat/Spring MVC 기준 Thread Pool 200개 제약으로 초당 1,000 TPS 이상의 Spike에서 Connection Pool 고갈 -> 503 에러 폭증.
3. **비즈니스 트랜잭션 경계 모호**: 결제->재고차감->쿠폰발급의 3-Phase 작업을 2PC(Two-Phase Commit)로 처리 시 Coordinator 장애 시 Lock 장기 점유.
4. **시간·공간 결합**: Consumer가 Producer 호출 시점에 반드시 가동 중이어야 함. 야간 배치 시스템과 실시간 시스템의 협업 불가.

이를 해결하기 위해 **메시지 큐(MQ)**는 Producer와 Consumer 사이에서 **시간적 디커플링(Temporal Decoupling)**과 **공간적 디커플링(Spatial Decoupling)**을 제공하며, 1990년대 IBM MQSeries, 2000년대 JMS(Java Message Service) 1.1/2.0, 2010년대 AMQP 1.0 표준화, 그리고 LinkedIn의 Kafka(2011 OSS) 출시를 거치며 **고처리량·분산 로그 기반**으로 진화해 왔다.

```text
  [동기식 요청-응답 모델 vs 비동기 메시지 큐 모델 비교]

   기존 동기식 (Tightly-Coupled)            비동기 메시지 큐 (Loosely-Coupled)
   ---------------------------            -------------------------------
   +--------+    HTTP/JSON    +--------+  +--------+  AMQP/MQTT  +--------+
   |  API   | ---------------->|  Order |  |  API   | -----------> | Broker |
   | Gateway| <------ 200 -----| Service|  | Gateway| <--- ACK -- | (Kafka)|
   +--------+                 +--------+  +--------+             +---+----+
        |                         |                                  |
        |  3초 타임아웃 시         | 503 에러 전파                     v
        v                         v                              +--------+
   +---------------------------------+   [Consumer Group]        |  Order |
   |   ✗ 장애 전파 / Thread 점유     |   ------------------>       | Worker |
   |   ✗ 순서 보존 어려움            |                            +----+---+
   +---------------------------------+                                 |
                                                                      v
                                                                 +--------+
                                                                 |  Stock |
                                                                 | Worker |
                                                                 +--------+
                                                                 5초 후 처리
```

특히 **대규모 트래픽을 견디는 시스템**의 경우, 2024년 기준 Netflix는 하루 2.5조 건의 이벤트를 Kafka로 처리하고, Uber는 300+ Topic으로 1,000개 마이크로서비스를 연결하며, 카카오·배민·토스 같은 국내 플랫폼도 RabbitMQ/Kafka를 통한 **사가(Saga) 패턴**, **이벤트 소싱(Event Sourcing)**, **CQRS** 구현의 근간으로 활용하고 있다.

- **📢 섹션 요약 비유**: 메시지 큐는 마치 우체국의 **우편함(Postbox)**과 같다. 편지(메시지)를 보낸 사람이 우체함에 넣기만 하면 우편부가 분류·배달을 책임지므로, 받는 사람이 부재중이거나 회수하러 갈 시간이 부족해도 손실 없이 전달된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) 메시지 큐의 핵심 구성 요소

```text
  +------------------------------------------------------------------------+
  |                  메시지 큐 비동기 통신 패턴 아키텍처                      |
  +------------------------------------------------------------------------+

       Producer A --+                              +-- Consumer Group 1
       (Order API)  |                              |   (Order Worker x 3)
                    |         +----------+         |
       Producer B --+--------->|  Broker  |---------+-- Consumer Group 2
       (Payment)    |         | +------+ |         |   (Stock Worker x 5)
                    |         | |Topic | |         |
       Producer C --+         | |Partition|       +-- Consumer Group 3
       (Member)               | |  0,1,2  |             (Notification)
                              | +------+ |
                              | +------+ |         [Offset Commit]
                              | |  ZK  | |         [Heartbeat]
                              | |/KRaft| |
                              | +------+ |
                              | +------+ |
                              | | DLQ  | | <--- 실패 메시지 격리 (Retry > N)
                              | +------+ |
                              | +------+ |
                              | |Retry | | <--- 지수 백오프 (1s->2s->4s->...)
                              | |Queue | |
                              | +------+ |
                              +----------+
                                  |
                                  v
                            [ Monitoring ]
                            Prometheus / Grafana
                            Burrow / Kafka-Manager
```

### 2) 핵심 컴포넌트 기술 명세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Producer (발행자)** | 비즈니스 이벤트를 직렬화(Avro/Protobuf/JSON) 후 Broker로 전송 | `linger.ms=10`(배치 대기), `compression.type=lz4/zstd`, `acks=all`로 Leader+ISR(In-Sync Replica) 모두 저장 확인, **Idempotent Producer**로 `enable.idempotence=true` 시 Producer ID(PID) + Sequence Number로 Broker 측 중복 제거 |
| **Broker (중개자)** | 메시지 저장·복제·라우팅·순서 보존의 핵심 엔진 | Kafka는 **Partitioned Log** 구조(Segment File 1GB 기본), `unclean.leader.election.enable=false`로 데이터 손실 방지, `min.insync.replicas=2` 설정으로 HA 보장; RabbitMQ는 **Exchange(Direct/Topic/Fanout/Headers)** -> Binding Key 기반 라우팅 |
| **Consumer (소비자)** | Broker에서 메시지를 가져와 비즈니스 로직 수행, Offset 커밋 | Kafka는 `enable.auto.commit=false` + 수동 `commitSync()` 권장, **Consumer Group**별 Partition 할당 전략(Range/RoundRobin/StickyAssignor), `max.poll.records=500`으로 한 번에 처리량 제한 |
| **Queue / Topic** | 메시지의 논리적 집합, FCM(FIFO) 또는 Pub/Sub 구조 | Kafka Topic은 **Partition**으로 수평 분할(병렬 처리 단위), `num.partitions=12`, `replication.factor=3` 권장; RabbitMQ는 Queue 단위로 Strict FIFO, **Lazy Queue**(`x-queue-mode=lazy`)로 디스크 기반 메모리 절약 |
| **DLQ (Dead Letter Queue)** | 재처리 한도 초과·Poison Message 격리 | `x-dead-letter-exchange` (RabbitMQ) 또는 `DeadLetterPublishingRecoverer` (Spring Kafka)로 `retry.backoff.ms=1000`, `max.retries=5` 정책 적용, 운영팀 알람 연동 필수 |
| **Schema Registry** | 메시지 스키마 버전 관리 및 호환성 검증 | Confluent Schema Registry, Apicurio Registry. Avro/Protobuf 스키마 진화 시 **Backward/Forward/Full Compatibility** 강제, `compatibility.level=BACKWARD` |

### 3) 메시지 전달 보장 수준 (Delivery Guarantee)

| 보장 수준 | 정의 | 구현 메커니즘 | 적용 사례 |
| :--- | :--- | :--- | :--- |
| **At-most-once** | 중복 없이 0~1회 전달, 손실 가능 | `acks=0`(Kafka), Consumer 자동 커밋 | 로그·메트릭 수집(손실 허용) |
| **At-least-once** | 0회 이상 전달, 중복 가능 | `acks=all` + 수동 커밋 + 재시도 | 결제·주문(주문은 멱등 처리 필수) |
| **Exactly-once** | 정확히 1회 전달, 중복/손실 모두 0 | Kafka 0.11+ **EOS(Exactly-Once Semantics)**: 트랜잭션 Producer + `read_committed` Isolation Level + `__consumer_offsets` 트랜잭션 커밋, 또는 **Transactional Outbox Pattern** | 금융 거래, 항공 예약 |

### 4) 순서 보존 (Ordering) 알고리즘

```text
  [Per-Partition Ordering 동작 원리]

   Producer                Partition 0            Partition 1            Partition 2
      |                         |                       |                       |
      | msg1(key=order-100)----->| offset 0              |                       |
      | msg2(key=order-200)-----+----------------------->| offset 0              |
      | msg3(key=order-100)----->| offset 1              |                       |
      |                         |                       |                       |
      |                         v                       v                       v
      |                   Consumer A                Consumer B            Consumer C
      |                   (동일 key의               (다른 key의            (다른 key의
      |                    순서 보장)                순서 보장)             순서 보장)
      |
      +- Hash(key) % num_partitions 로 동일 key는 동일 Partition에 적재
         -> Hash Partitioning (Java: `DefaultPartitioner`, `murmur2`)
```

### 5) 백프레셔(Backpressure)와 흐름 제어

- **Kafka**: Consumer가 `max.poll.records`로 한 번에 가져오는 양을 제한하고, Lag(`kafka_consumergroup_lag`)을 모니터링하여 `lag > 10000` 시 Auto-Scaling.
- **RabbitMQ**: `prefetch_count=N`으로 한 Consumer에게 동시 전달할 미확인 메시지 수 제한, `qos` 정책 적용.
- **Amazon SQS**: Visibility Timeout(기본 30초) 동안 다른 Consumer가 처리 못 함, **Long Polling**(`WaitTimeSeconds=20`)으로 빈 폴링 절감.

- **📢 섹션 요약 비유**: 메시지 큐의 백프레셔는 수도꼭지의 **수압 조절기**와 같다. 수도관(Consumer)이 받아들일 수 있는 물(메시지)의 양 이상으로 공급되면 자동으로 압력을 낮춰 파열(시스템 다운)을 막아준다.

---

## Ⅲ. 비교 및 연결

### 1) 메시지 큐 솔루션 비교

| 구분 | **Apache Kafka** | **RabbitMQ** | **Amazon SQS / SNS** | **Redis Pub/Sub & Streams** | **NATS / JetStream** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **아키텍처 모델** | 분산 로그 (DLog) | AMQP Exchange-Queue | 완전관리형 Queue/SNS Topic | 인메모리 + 디스크 스트림 | 경량 Pub/Sub + JetStream(영구) |
| **프로토콜** | Kafka Binary Protocol | AMQP 0-9-1, MQTT, STOMP | AWS API (HTTP/HTTPS) | RESP (Redis) | NATS Text Protocol, gRPC |
| **처리량(TPS)** | 100만+/Partition | 5만~10만/노드 | 무제한(샤드 자동 확장) | 10만~50만 | 100만+ |
| **메시지 보존** | 디스크 영구(`retention.ms=604800000`) | 큐 소비 시 삭제 | 14일까지(표준), 15일(확장 FIFO) | Streams: XADD 기반 영구 | JetStream: 영구/스트림 |
| **순서 보장** | Partition 내 보장 | 단일 큐 FIFO | Standard: Best Effort, FIFO: 엄격 보장 | Streams: ID 단위 보장 | Subject별 보장 |
| **전달 보장** | At-least-once, Exactly-once(EOS) | At-least-once | At-least-once | At-most-once(Pub/Sub), At-least-once(Streams) | At-least-once, Exactly-once(JetStream) |
| **푸시/풀** | Pull(Long Polling) | Push(prefetch) | Pull(Long Polling) | Push(Pub/Sub), Pull(Streams) | Push(JetStream Push Consumer) |
| **주 사용처** | 이벤트 스트리밍, 로그 수집, CDC, 사가 | 작업 큐, RPC 대체, IoT | AWS 네이티브 MSA, 서버리스 | 캐시 무효화, 실시간 알림 | IoT, Edge, k8s Service Mesh |
| **운영 복잡도** | 높음(ZK/KRaft, Partition 재분배) | 중간(Mirror/Shovel) | 없음(완전관리형) | 낮음 | 낮음 |
| **라이선스** | Apache 2.0 | MPL 2.0 (RabbitMQ) | 상용(SaaS) | BSD | Apache 2.0 |

### 2) 동기식 통신과의 비교

| 구분 | **동기식 REST/gRPC** | **비동기 메시지 큐** |
| :--- | :--- | :--- |
| **결합도** | 높음 (Tight Coupling) | 낮음 (Loose Coupling) |
| **응답 지연** | 네트워크 RTT 합산 (수 ms ~ 수 초) | Producer는 ACK만 수신 (1~10ms) |
| **장애 전파** | 즉시 전파 (Cascading) | 격리 (Broker에 누적) |
| **순서 보장** | 호출 순서 = 실행 순서 | 설계 필요 (Partition Key, Idempotency) |
| **트랜잭션 일관성** | 2PC, Saga(Orchestration) | Saga(Choreography), Eventual Consistency |
| **확장성** | 수직 확장 위주 | 수평 확장 (Partition/Consumer Group) |
| **디버깅** | Trace ID로 비교적 용이 | Distributed Tracing 필수 (OpenTelemetry) |
| **적합 시나리오** | 즉시 응답 필요 (조회, 인증) | 비동기 처리, 이벤트 발행, 배치 |

### 3) 연계 패턴

- **Event Sourcing**: 모든 도메인 상태 변경을 `OrderCreated`, `OrderPaid`, `OrderShipped` 같은 이벤트로 발행 -> Kafka를 Event Store로 활용,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 565 / 600

<- **이전**: [564. API 설계 RESTful GraphQL gRPC](/studynote/11_design_supervision/06_exam_summary/565_api_design_restful_graphql_grpc/)
**다음**: [566. 데이터 일관성 패턴 최종 일관성](/studynote/11_design_supervision/06_exam_summary/566_data_consistency_pattern_eventual_consis/) ->

---
