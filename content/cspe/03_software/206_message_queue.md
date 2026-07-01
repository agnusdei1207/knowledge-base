---
title: "메시지 큐 — RabbitMQ·ActiveMQ (Message Queue)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 206
---

# 📖 【암기용】 개념 완전 이해

> 목적: 메시지 큐를 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 송신자와 수신자 사이에 메시지를 임시 저장해 비동기 처리하는 미들웨어
- **왜 필요한가**: 주문, 결제, 알림처럼 처리 시간이 다른 작업을 동기 호출로 묶으면 한 서비스 장애가 전체 흐름을 막는다. 메시지 큐는 요청을 저장하고 소비자가 가능한 속도로 처리하게 한다.
- **핵심 직관**: 창구 앞 대기번호표처럼 요청을 줄에 넣고 담당자가 순서대로 처리하는 구조이다.

## 깊이 이해
- **배경·문제의식**: 분산 시스템에서 모든 서비스를 동기 호출로 연결하면 지연 전파, 장애 전파, 피크 트래픽 흡수 실패가 발생한다.
- **작동 원리**: Producer가 메시지를 Exchange 또는 Queue에 발행하고, Broker는 라우팅·저장·전달을 수행한다. Consumer는 메시지를 처리한 뒤 ACK를 보내고, 실패 시 재전달 또는 DLQ로 이동한다.
- **비유**: 택배 물류센터에서 발송자가 물건을 맡기면 분류대가 목적지별로 나누고 배송기사가 가능한 순서로 가져가는 방식임.
- **구체 예시**: 주문 생성 후 이메일 발송을 RabbitMQ queue에 적재하면 주문 API는 100ms 내 응답하고, 이메일 worker는 초당 500건씩 별도 처리 가능함.
- **흔한 오해·주의점**: 메시지 큐가 정확히 한 번 처리를 자동 보장하지 않는다. 중복 메시지, 순서, 재처리, 멱등성을 소비자 로직에서 설계해야 한다.

## 연결 개념
- Event-Driven Architecture — 메시지 기반 비동기 아키텍처
- Saga Pattern — 분산 트랜잭션 보상 처리
- Dead Letter Queue — 실패 메시지 격리 저장소

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 수치·표준명·비교축으로 작성한다.
> 핵심: 메시지 큐는 비동기화만이 아니라 장애 격리, 부하 완충, 재처리 통제를 포함하는 운영 설계이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 메시지 큐는 Producer와 Consumer 사이에서 메시지를 저장·라우팅·전달하는 비동기 미들웨어이다.
> 2. **가치**: 동기 호출 결합도를 낮추고, 피크 트래픽을 큐 depth로 흡수하며, 실패 메시지를 재처리한다.
> 3. **판단 포인트**: ordering, delivery guarantee, ACK, retry, DLQ, idempotency를 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 비동기 미들웨어 구조 이해 확인 | Producer, Broker, Queue, Consumer, ACK | 큐를 단순 임시 저장소로만 설명 |
| RabbitMQ·ActiveMQ 특성 비교 확인 | routing, durable queue, JMS, AMQP | Kafka와 로그 스트림을 구분하지 않음 |
| 운영 리스크 판단 확인 | retry, DLQ, 중복 처리, back pressure | exactly-once 자동 보장으로 단정 |

> 요약: 이 문제는 큐 구성요소와 함께 전달 보장, 실패 처리, 멱등성 설계를 요구한다.

---

## Ⅰ. 개요 및 필요성

메시지 큐는 서비스 간 메시지를 비동기로 전달하는 미들웨어이다. 동기 호출 중심 구조는 피크 트래픽과 하위 서비스 장애를 상위 서비스에 전파한다. RabbitMQ·ActiveMQ는 큐 기반 라우팅, 저장, ACK, 재전달로 부하 완충과 장애 격리를 제공한다.

---

## Ⅱ. 구조 및 구성요소

```text
Producer -> Exchange/Broker -> Queue -> Consumer -> ACK
                         +-> Retry Queue -> Dead Letter Queue -> Operator
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Producer | 업무 이벤트·명령 메시지 발행 | correlation id 포함 |
| Broker | 라우팅, 저장, 전달 제어 | RabbitMQ exchange, ActiveMQ broker |
| Queue | 메시지 순서 저장·대기 | durable, TTL, priority 설정 |
| Consumer | 메시지 처리 후 ACK/NACK | 멱등 처리 필요 |

> 요약: 메시지 큐는 발행, 라우팅, 저장, 소비, 실패 격리의 구성요소로 비동기 처리를 수행한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
메시지 발행 -> 라우팅 -> 큐 적재 -> 소비자 전달 -> 업무 처리 -> ACK/DLQ
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Producer가 message와 routing key 발행 | schema validation pass |
| 2 | Broker가 exchange 정책으로 queue 선택 | unroutable message 0건 |
| 3 | Consumer가 prefetch 기준으로 메시지 수신 | consumer lag 목표 이하 |
| 4 | 처리 성공 시 ACK, 실패 시 retry 또는 DLQ | DLQ ratio 1% 이하 |

> 요약: 메시지 큐 처리는 발행, 라우팅, 소비, 확인응답, 실패 격리 순서로 통제된다.

---

## Ⅳ. 특징

| 구분 | RabbitMQ | ActiveMQ | 판단 포인트 |
|:---|:---|:---|:---|
| 표준 | AMQP 중심 | JMS, OpenWire, AMQP 지원 | Java EE·JMS 연계는 ActiveMQ |
| 라우팅 | direct, topic, fanout exchange | queue/topic 모델 | 복합 routing key는 RabbitMQ |
| 전달 | ACK, durable queue, quorum queue | persistent message, transaction | 장애 시 메시지 손실 목표 0건 |
| 처리량 | 저지연 queue workload | enterprise messaging | 초당 1천~1만 메시지 기준 벤치마크 필요 |

> 요약: RabbitMQ는 라우팅 유연성, ActiveMQ는 JMS 기반 엔터프라이즈 연계에 선택 근거가 있다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 동기 REST 호출 | 비동기 queue | 하위 처리 지연이 상위 API p95에 영향 |
| 비용/성능 | 즉시 응답 대기 | 큐 적재 후 worker 처리 | API p95 200ms, 큐 대기 5분 이하 |
| 운영/위험 | 장애 직접 전파 | retry·DLQ 격리 | 중복 처리와 순서 요구 수준 확인 |

> 요약: 메시지 큐는 응답 지연과 장애 전파를 분리해야 할 때 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 중복 처리 | ACK 전 장애, 재전달 | idempotency key, processed table | duplicate side effect 0건 |
| 큐 적체 | consumer 처리량 부족 | autoscaling, prefetch 조정 | queue depth, consumer lag |
| 실패 반복 | poison message | retry limit, DLQ, replay 도구 | DLQ ratio 1% 이하 |

> 요약: 메시지 큐 리스크는 중복, 적체, poison message이며 멱등성과 DLQ 운영으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 처리량 | 초당 메시지 처리량 목표 충족 | broker metric |
| 지연 | 큐 대기 p95 5분 이하 | enqueue/dequeue timestamp |
| 신뢰성 | 메시지 손실 0건, DLQ 1% 이하 | audit log, DLQ dashboard |

> 요약: 도입 효과는 처리량, 큐 대기 지연, 메시지 손실·DLQ 비율로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 업무별 queue와 DLQ를 분리하고 retry 3회, exponential backoff, poison message 격리 정책을 적용함.
2. Consumer에 idempotency key와 처리 이력 테이블을 두어 재전달 시 외부 결제·메일 중복 실행을 차단함.
3. queue depth, consumer lag, publish rate, DLQ ratio를 Prometheus와 Grafana로 관측하고 lag 기준 autoscaling을 적용함.

**결론 (2줄):**
- 기술사 판단: 명령형 업무 큐와 JMS 연계는 RabbitMQ·ActiveMQ, 대용량 이벤트 로그와 재처리는 Kafka를 선택함.
- 향후 방향: 큐는 Saga, outbox pattern, observability와 결합해 분산 트랜잭션 보상 계층으로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "메시지 큐를 설명하시오" | 발행, 라우팅, 소비, ACK, DLQ 흐름 | RabbitMQ·ActiveMQ 특성 비교 |
| 요구사항 명시형 | "비동기 처리 방안을 제시하시오" | retry, DLQ, 멱등성, back pressure | 동기 호출 대비 선택 기준과 지표 |

> 요약: 설명형은 큐 구조와 동작, 방안형은 장애 격리와 재처리 통제 중심으로 전환한다.
