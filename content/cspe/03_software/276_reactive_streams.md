---
title: "리액티브 스트림 (Reactive Streams)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 276
---

# 📖 【암기용】 개념 완전 이해

> 목적: 이 개념을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 리액티브 스트림(Reactive Streams)은 **비동기**(Asynchronous) **스트림**(Stream) 처리에서 생산자와 소비자의 처리 속도 차이를 **Backpressure**(배압)로 제어하는 표준 인터페이스 규격이다.
- **왜 필요한가**: 생산자가 초당 10,000건을 만들어내는데 소비자가 초당 1,000건밖에 못 처리하면 그 차이만큼 큐에 쌓이고, 이 적체가 계속되면 메모리를 다 먹어 OOM으로 이어진다. Backpressure는 이걸 소비자가 감당할 수 있는 양만 생산자에게 요청하는 방식으로 막는다.
- **핵심 직관**: 수도꼭지를 무작정 틀어놓는 게 아니라, 컵을 든 사람이 "지금 이만큼 받을 수 있어"라고 말해준 만큼만 물을 트는 구조다 — 밀어내는(push) 게 아니라 요청받은 만큼만 내주는(pull에 가까운) 흐름이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 비동기(Asynchronous) | 호출자가 결과를 기다리며 멈춰있지 않고, 결과가 나중에 신호로 전달되는 실행 방식 — 이 문서의 상위 주제 | 주문만 넣고 자리로 돌아가 있으면 음식이 나올 때 알려주는 방식 |
| 스트림(Stream) | 한 번에 오는 게 아니라 시간에 걸쳐 연속적으로 도착하는 데이터 시퀀스 | 한 번에 배달되는 택배가 아니라 계속 흘러들어오는 컨베이어 벨트 |
| Backpressure(배압) | 소비자가 처리 가능한 양만큼만 요청해 생산자의 발행 속도를 늦추는 흐름 제어 메커니즘 | 컵을 든 사람이 물을 받을 수 있는 양만 요청하는 것 |
| Publisher(발행자) | 데이터를 만들어 내보내는 쪽 — 소비자가 요청한 수량을 넘겨 보내면 규격 위반 | 주방 — 주문받은 접시 수만 내보냄 |
| Subscriber(구독자) | 데이터를 받아 처리하는 쪽 — 자신이 처리 가능한 수량을 직접 요청함 | 홀 서버 — 나를 수 있는 만큼만 주문(request)함 |
| Subscription(구독) | Publisher와 Subscriber 사이를 잇는 채널로, `request(n)`(수량 요청)과 `cancel()`(취소)을 전달 | 주방과 홀을 잇는 주문 전표 |
| Processor | Publisher와 Subscriber 역할을 동시에 하는 중간 변환자(입력을 받아 가공 후 다시 발행) | 재료를 받아 반가공해서 다음 주방으로 넘기는 중간 조리대 |
| Demand(수요) | Subscriber가 `request(n)`으로 알리는 "지금 처리할 수 있는 수량" | "접시 5개까지 더 받을 수 있어요"라는 신호 |
| onNext/onError/onComplete | 데이터 전달(onNext), 오류(onError), 정상 종료(onComplete) 신호 — onError와 onComplete는 상호 배타적이며 정확히 1회만 발생 | 요리 전달, "주방 사고 발생", "오늘 영업 종료" 신호 |

## 깊이 이해

### Backpressure가 없으면 무슨 일이 생기나 — 수치로 확인
- 생산자가 초당 10,000건, 소비자가 초당 1,000건만 처리할 수 있다면 차이인 9,000건/초가 매초 큐에 쌓인다. 아무 제한 없는(unbounded) 큐라면 10초 후 90,000건, 100초 후 900,000건이 쌓인다. 건당 200바이트라 하면 100초 뒤에는 약 180MB가 추가로 적체된 것이고, 이 추세가 이어지면 결국 OOM에 도달한다.
- Backpressure가 걸려 있으면 소비자가 "나 1,000개까지만 처리 가능해"라고 `request(1000)`을 보내고, Publisher는 그 이상 `onNext`를 호출하지 않는다. 큐가 무한정 자라는 대신, 생산자 쪽에서 속도를 늦추거나(느려짐) 초과분을 정책에 따라 버리거나 보관한다.

### Publisher-Subscriber-Subscription의 실제 신호 순서
1. Subscriber가 Publisher를 구독하면, Publisher는 Subscription 객체를 만들어 `onSubscribe(subscription)`으로 Subscriber에 건넨다.
2. Subscriber가 `subscription.request(256)`을 호출해 "256건까지 처리 가능"이라는 초기 수요를 알린다.
3. Publisher는 정확히 256건 이하로만 `onNext(item)`을 호출할 수 있다 — 이 한도를 넘기면 스펙 위반이다.
4. Subscriber가 처리를 진행하며 수요가 줄면 다시 `request(n)`을 호출해 수요를 보충한다.
5. 스트림이 끝나면 `onComplete()`, 오류가 나면 `onError(e)`가 정확히 한 번 호출되고 이후 신호는 없다.

### Buffer 전략별 트레이드오프
- `onBackpressureBuffer` (무제한 버퍼): 데이터는 안 잃지만 위 계산처럼 계속 쌓이면 결국 OOM 위험이 그대로 남는다.
- `onBackpressureDrop`: 처리 못한 초과분을 버린다 — 최신 시세처럼 일부 유실을 감내할 수 있는 실시간 데이터에 적합하다.
- `onBackpressureLatest`: 가장 최근 값만 남기고 나머지는 버린다 — 상태 갱신(예: 진행률 표시)에 적합하다.
- `limitRate(n)`: 애초에 업스트림에 보내는 요청량 자체를 n으로 제한해 소스 쪽 부하도 줄인다.

### 판별 원리 — 언제 Reactive Stream까지 필요한가
- 처리량이 초당 수백 건 수준이고 동기·blocking 처리로 충분하다면 리액티브 스트림 도입은 과설계다. 반면 생산·소비 속도 차이가 크고 무제한 대기열이 곧 장애(OOM, 지연 폭증)로 이어지는 상황(대용량 이벤트 스트림, 실시간 API, 메시지 브로커 연동)에서는 backpressure 계약이 필요하다.

### 비유
- 식당 주방(Publisher)이 홀 서버(Subscriber)가 나를 수 있는 접시 수(`request(n)`)만큼만 요리를 내놓으면, 테이블(큐)에 접시가 쌓여 넘치는 일이 없다.

### 흔한 오해·주의점
- `CompletableFuture`, `Promise` 같은 단순 비동기 API에는 backpressure가 없다 — 리액티브 스트림의 핵심은 "비동기"가 아니라 "소비자 수요 기반 흐름 제어"다. 이 계약을 안 지키면 이름만 reactive인 그냥 push 파이프라인일 뿐이다.
- event loop(non-blocking 스레드) 안에서 JDBC 같은 blocking 호출을 하면 그 스레드 하나가 막혀 전체 파이프라인이 멈춘다 — 반드시 별도 scheduler(boundedElastic 등)로 격리해야 한다.

## 연결 개념
- 비동기 프로그래밍 — non-blocking I/O와 이벤트 루프라는 리액티브 스트림의 실행 기반
- 스레드 안전(274) — Publisher/Subscriber가 여러 스레드에서 신호를 주고받을 때도 규약(순차적 onNext 등)으로 경쟁을 막음
- 메시지 브로커(Kafka, RabbitMQ) — poll batch·commit 같은 자체적인 수요 기반 흐름 제어로 리액티브 스트림과 개념이 맞닿아 있음

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 리액티브 스트림을 Publisher, Subscriber, Subscription, Processor와 backpressure 계약 중심으로 답안화한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 리액티브 스트림은 비동기 데이터 스트림에서 소비자가 처리 가능한 양을 요청하는 backpressure 표준이다.
> 2. **가치**: 생산·소비 속도 차이로 인한 큐 폭증, 메모리 증가, 지연 전파를 demand 신호로 통제한다.
> 3. **판단 포인트**: non-blocking 여부보다 `request(n)`, scheduler, buffer, retry, cancellation 정책을 함께 봐야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 비동기 스트림 표준 이해 확인 | Publisher, Subscriber, Subscription, Processor | observer pattern과 동일하다고만 서술 |
| backpressure 판단 확인 | demand, buffer, drop, throttle | 비동기 처리만 쓰고 흐름 제어 누락 |
| 운영 적용 역량 확인 | queue depth, consumer lag, p99 latency | 프레임워크 이름만 나열 |

> 요약: 리액티브 스트림 답안은 소비자 demand 기반 제어와 운영 지표를 연결해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 리액티브 스트림은 비동기 스트림 backpressure 표준이다.
- 배경: 마이크로서비스, 이벤트 처리, 실시간 API는 생산자와 소비자 처리량 차이로 큐 적체와 메모리 사용량 증가가 발생한다.
- 필요성: Publisher·Subscriber·Subscription 기반 요청량 제어로 처리량 차이를 흡수해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Publisher -> Subscription -> Subscriber
      |              |
      +-> Processor  +-> request(n) / cancel
Data Signal -> onNext / onError / onComplete
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Publisher | 데이터 발행자 | 요청량 초과 발행 금지 |
| Subscriber | 데이터 소비자 | `onSubscribe`, `onNext` 구현 |
| Subscription | demand·cancel 제어 | `request(n)` 핵심 |
| Processor | 중간 변환자 | publisher와 subscriber 역할 동시 수행 |

> 요약: 구조의 핵심은 Subscription이 소비자 demand를 생산자에게 전달하는 제어 채널이라는 점이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Subscriber 구독 -> onSubscribe 수신 -> request(n)
  -> Publisher onNext n건 발행 -> 처리 완료 후 추가 request
  -> 오류/완료 시 onError/onComplete -> 자원 해제
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Subscriber가 Publisher에 subscribe | subscription 생성 |
| 2 | Subscriber가 `request(n)` 발행 | demand count |
| 3 | Publisher가 n건 이하 `onNext` 전송 | rule violation 0건 |
| 4 | 완료·오류·취소 처리 | terminal signal 단 1회 |

> 요약: 리액티브 스트림은 소비자가 요청한 수량만 생산자가 보내는 pull 기반 비동기 흐름이다.

---

## Ⅳ. 특징

| 구분 | 전통 Push 스트림 | Reactive Streams | 정량·기술 포인트 |
|:---|:---|:---|:---|
| 흐름 제어 | 생산자 주도 | 소비자 demand 주도 | `request(n)` |
| 자원 관리 | 큐 증가 가능 | buffer/drop/backpressure 정책 | queue depth 제한 |
| 오류 처리 | callback 분산 | terminal signal 표준화 | onError 1회 |
| 구현체 | custom async | Reactor, RxJava, Akka Streams | JVM 표준 연계 |

> 요약: 리액티브 스트림은 비동기성보다 backpressure 계약 준수가 차별점이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| Blocking I/O | 스레드당 요청 | event loop+stream | 동시 연결 1만 이상 |
| 단순 Queue | 무제한 적재 위험 | demand 기반 제한 | consumer lag 관리 필요 |
| Batch 처리 | 주기 처리 | 연속 스트림 처리 | 실시간 지연 1초 이하 요구 |

> 요약: 실시간성과 소비 속도 제어가 동시에 필요하면 리액티브 스트림을 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| backpressure 미적용 | 무제한 buffer | bounded buffer, drop/latest 정책 | queue depth, OOM count |
| blocking 호출 혼입 | event loop에서 DB blocking | boundedElastic, async driver | event loop blocking time |
| 오류 전파 누락 | retry 무한 반복 | retry limit, circuit breaker | retry count, error rate |

> 요약: 운영 리스크는 buffer 제한, blocking 제거, retry 한도 설정으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연 | p99 stream latency 500ms 이하 | tracing, metric |
| 적체 | consumer lag 임계값 이하 | broker metric |
| 자원 | event loop blocking 0건 | BlockHound, profiler |

> 요약: 리액티브 스트림 성공 여부는 p99 지연, consumer lag, event loop blocking으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Reactor/RxJava 파이프라인은 bounded buffer, `onBackpressureDrop`, `limitRate`를 명시하고 demand 테스트를 작성함.
2. DB·파일·외부 API는 non-blocking driver를 사용하고 blocking 호출은 별도 scheduler로 격리함.
3. 운영 지표는 queue depth, consumer lag, p99 latency, retry count를 대시보드와 alert에 포함함.

**결론 (2줄):**
- 기술사 판단: 생산·소비 속도 차이가 운영 리스크이면 reactive stream, 단순 CRUD는 동기 구조도 선택 가능.
- 향후 방향: WebFlux, RSocket, Kafka Streams 등에서 backpressure와 observability가 결합된 스트림 운영이 확대됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "리액티브 스트림을 설명하시오" | subscribe, request, signal 흐름 | push 방식과 backpressure 차이 |
| 요구사항 명시형 | "설계하시오", "운영 방안을 제시하시오" | demand, buffer, scheduler 설계 | consumer lag, blocking, retry 대응 |

> 요약: 설명형은 표준 계약, 설계형은 흐름 제어와 운영 지표 중심으로 전환한다.
