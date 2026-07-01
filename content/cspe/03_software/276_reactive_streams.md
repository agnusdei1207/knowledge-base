---
title: "리액티브 스트림 (Reactive Streams)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 276
---

# 📖 【암기용】 개념 완전 이해

> 목적: 리액티브 스트림을 비동기 데이터 흐름에서 생산자와 소비자 속도 차이를 backpressure로 제어하는 표준으로 이해하게 만든다.

## 한눈에
- **개요**: 리액티브 스트림은 비동기 스트림 처리와 backpressure를 규정한 표준 인터페이스다.
- **왜 필요한가**: 생산자가 초당 10,000건을 만들고 소비자가 1,000건만 처리하면 큐가 증가해 메모리와 지연 문제가 발생한다.
- **핵심 직관**: 수도꼭지 물을 컵이 받을 수 있는 만큼만 틀도록 소비자가 양을 요청하는 구조다.

## 깊이 이해
- **배경·문제의식**: 이벤트 기반 시스템은 네트워크, DB, 메시지 브로커 속도가 서로 다르다. 단순 push 방식은 느린 소비자를 고려하지 않아 큐 적체와 OOM을 만든다.
- **작동 원리**: Subscriber가 Subscription을 통해 `request(n)`을 보내고, Publisher는 요청 수만큼 `onNext`를 전달한다. 오류와 완료는 `onError`, `onComplete`로 끝난다.
- **비유**: 식당 주방이 손님이 주문한 접시 수만 내보내면 테이블이 넘치지 않는다.
- **구체 예시**: Project Reactor `Flux`는 `request(256)` 같은 demand를 사용하고, Kafka 소비자는 poll batch와 commit으로 처리량을 조절한다.
- **흔한 오해·주의점**: 리액티브 스트림은 단순 비동기 API가 아니다. backpressure 계약을 지키지 않으면 이름만 reactive인 push 파이프라인이 된다.

## 연결 개념
- 비동기 프로그래밍 — non-blocking I/O와 이벤트 루프
- Backpressure — 소비자 demand 기반 흐름 제어
- 메시지 브로커 — Kafka, RabbitMQ와 스트림 처리 연결

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
