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
- **개요**: 메시지 큐는 발신자(Producer)와 수신자(Consumer) 사이에 메시지를 임시로 저장해 서로 다른 속도로 동작하게 해주는 **비동기 메시징(Asynchronous Messaging) 미들웨어**이다.
- **왜 필요한가**: 주문 생성처럼 빨리 끝나야 하는 작업과 이메일 발송처럼 느려도 되는 작업을 동기 호출 하나로 묶으면, 느린 작업이 빠른 작업의 응답 시간을 그대로 끌어내리고 느린 작업이 죽으면 빠른 작업까지 실패한다.
- **핵심 직관**: 은행 창구의 대기번호표다. 손님(요청)은 번호표를 뽑고 자리에 앉으면 되고, 창구 직원(Consumer)은 자기 처리 속도대로 번호를 부른다 — 손님이 직원 처리 속도를 기다리며 서 있을 필요가 없다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 비동기 메시징 (Asynchronous Messaging) | 발신자가 응답을 기다리지 않고 메시지를 넘긴 뒤 바로 다음 일을 하는 통신 방식 | 번호표 뽑고 바로 자리에 앉음 |
| Producer | 메시지를 만들어 큐에 보내는 쪽 | 번호표를 뽑는 손님 |
| Broker | 메시지를 어디로 보낼지 판단하고 저장·전달하는 중개 서버 | 은행 전체 안내 시스템 |
| Exchange (RabbitMQ) | 메시지를 어느 큐로 보낼지 결정하는 라우팅 규칙 | 번호표 종류별 창구 배정 규칙 |
| Queue | 메시지가 순서대로 쌓여 소비자를 기다리는 저장소 | 대기 줄 자체 |
| Consumer | 큐에서 메시지를 꺼내 실제 업무를 처리하는 쪽 | 번호를 부르는 창구 직원 |
| ACK / NACK | 처리 성공(ACK)·실패(NACK)를 브로커에 알리는 응답 신호 | 처리 완료 도장 |
| Durable Queue | 브로커가 재시작해도 메시지가 사라지지 않도록 디스크에 저장 | 정전돼도 안 지워지는 대기 명부 |
| DLQ (Dead Letter Queue) | 반복 실패한 메시지를 격리해 따로 모아두는 큐 | 처리 못한 민원을 모아두는 별도 창구 |
| Retry / Backoff | 실패한 메시지를 일정 간격 늘려가며 재시도하는 정책 | 다시 줄 서되 점점 더 늦게 재시도 |
| Prefetch | Consumer가 한 번에 몇 개까지 미리 가져갈지 정하는 값 | 직원이 한 번에 처리할 서류 묶음 수 |
| 멱등성 (Idempotency) | 같은 메시지를 여러 번 처리해도 결과가 한 번 처리한 것과 같도록 만드는 성질 | 같은 서류가 두 번 접수돼도 중복 발급 안 되게 |
| AMQP / JMS | 메시지 큐가 따르는 표준 프로토콜(RabbitMQ는 AMQP, ActiveMQ는 JMS 중심) | 창구 운영 매뉴얼 표준 |

## 깊이 이해

### 왜 필요했나 — 동기 호출의 한계를 수치로
- 주문 API가 주문 저장(20ms) 후 이메일 발송(느릴 때 2~3초, 이메일 서버 장애 시 타임아웃 10초)까지 동기로 기다린다고 하면, 사용자는 주문 버튼을 누르고 최대 10초를 기다리게 되고 이메일 서버가 죽으면 주문 자체가 실패로 보인다.
- 메시지 큐를 넣으면 주문 API는 "이메일 보내라"는 메시지를 큐에 적재만 하고 100ms 안에 응답한다. 이메일 발송은 별도 Consumer(worker)가 초당 500건씩 자기 속도로 처리하며, 이메일 서버가 잠깐 죽어도 메시지는 큐에 남아 있다가 복구 후 처리된다 — 주문 성공·실패와 이메일 성공·실패가 분리된다.

### 발행부터 처리까지 흐름과 실패 처리
1. Producer가 메시지를 만들어 Exchange(RabbitMQ) 또는 직접 Queue(ActiveMQ)로 보낸다.
2. Broker는 라우팅 규칙(direct/topic/fanout)에 따라 해당 Queue에 메시지를 쌓는다.
3. Consumer가 Queue에서 메시지를 꺼내 처리하고, 성공하면 ACK를 보낸다 — 그제서야 브로커가 메시지를 큐에서 지운다.
4. 처리 중 오류가 나면 NACK을 보내거나 ACK를 못 보내고 죽는다. 브로커는 이 메시지를 재전달한다. 정해진 재시도 횟수(예: 3회, 1초→2초→4초 간격)를 넘기면 DLQ로 옮겨 사람이 확인하게 한다.
- ACK를 "메시지를 받았을 때"가 아니라 "처리를 끝냈을 때" 보내는 것이 핵심이다. 받자마자 ACK하면, 처리 도중 Consumer가 죽었을 때 메시지가 소실된다.

### 왜 정확히 한 번(exactly-once) 처리가 자동 보장되지 않는가
- Consumer가 처리를 끝내고 ACK를 보내려는 순간 네트워크가 끊기면, 브로커 입장에서는 ACK를 못 받았으니 실패로 보고 메시지를 재전달한다. 하지만 실제로는 Consumer가 처리를 이미 끝낸 상태다 — 그 결과 같은 메시지가 두 번 처리된다(중복).
- 그래서 메시지 큐는 보통 최소 한 번(at-least-once) 전달을 보장하고, 정확히 한 번은 Consumer가 멱등성을 직접 구현해야 완성된다. 예: 결제 처리 메시지에 `order_id`를 키로 하는 "이미 처리한 주문 목록" 테이블을 두고, 같은 order_id가 다시 오면 처리를 건너뛴다.

### 비유와 흔한 오해
- **비유**: 택배 물류센터. 발송자(Producer)가 물건을 맡기면 분류대(Exchange)가 목적지별로 나누고, 배송 기사(Consumer)는 자기 배송 순서대로 가져간다. 반송이 반복되는 물건은 반송 전용 창고(DLQ)로 보내 사람이 확인한다.
- **오해**: "큐에 넣으면 순서와 중복이 자동으로 해결된다"는 생각. 순서는 Consumer를 여러 개 병렬로 두는 순간 깨지기 쉽고(먼저 들어간 메시지가 늦게 끝날 수 있음), 중복은 위에서 설명한 재전달 구조상 발생할 수 있다. 둘 다 애플리케이션 설계(순서가 필요하면 단일 Consumer 또는 파티션 키, 중복 방지는 멱등성 키)로 별도 해결해야 한다.

## 연결 개념
- Event-Driven Architecture — 메시지 큐를 전달 인프라로 쓰는 상위 아키텍처 패턴
- Saga Pattern — 여러 큐 기반 단계를 묶어 분산 트랜잭션을 보상 처리하는 기법
- Dead Letter Queue — 반복 실패 메시지를 격리해 운영자가 재처리·분석하게 하는 저장소

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

- 개요: 비동기 메시지 전달 미들웨어
- 배경: 동기 호출 중심 구조는 피크 트래픽과 하위 서비스 장애를 상위 서비스에 전파한다.
- 필요성: RabbitMQ·ActiveMQ의 queue, ACK, retry, DLQ로 부하 완충과 장애 격리 기준을 제공한다.

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
