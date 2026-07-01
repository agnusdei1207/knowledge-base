---
title: "리액티브 프로그래밍 (Reactive Programming)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 29
---

# 📖 【암기용】 개념 완전 이해

> 목적: 리액티브 프로그래밍을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 데이터와 이벤트의 흐름을 스트림으로 보고 변화에 반응해 처리하는 프로그래밍 모델
- **왜 필요한가**: 사용자 요청, 메시지, 센서 이벤트, 외부 API 응답은 시간 순서로 계속 들어온다. 리액티브는 이 흐름을 publisher/subscriber와 backpressure로 제어한다.
- **핵심 직관**: 수도관에 물이 흐르듯 데이터가 흘러오면 필터, 변환, 합치기 밸브를 지나 소비자에게 전달되는 구조이다.

## 깊이 이해
- **배경·문제의식**: 동기 호출 기반 시스템은 느린 소비자나 장애 지점이 전체 요청 지연을 끌어올린다. 이벤트 기반 시스템은 흐름을 분리하지만 큐가 무한히 쌓이면 메모리 장애가 발생한다.
- **작동 원리**: Publisher는 데이터를 발행하고 Subscriber는 구독한다. Operator는 map, filter, flatMap 같은 변환을 수행하며, backpressure는 Subscriber가 처리 가능한 개수만 request하도록 제어한다.
- **비유**: 신문사가 무제한으로 신문을 보내지 않고 구독자가 하루 1부를 요청하면 그 양만 배송하는 방식이다.
- **구체 예시**: Reactive Streams는 `Publisher`, `Subscriber`, `Subscription`, `Processor` 인터페이스를 표준화했다. Reactor와 RxJava는 이를 기반으로 비동기 스트림 연산을 제공한다.
- **흔한 오해·주의점**: 리액티브는 단순 비동기 호출이 아니다. 핵심은 이벤트 스트림, 조합 연산, backpressure, 오류 전파 규칙을 갖춘 처리 모델이다.

## 연결 개념
- Reactive Streams — JVM 기반 비동기 스트림 표준
- Reactor/RxJava — 리액티브 연산자와 스케줄러 제공 프레임워크
- Backpressure — 생산자와 소비자 속도 차이를 통제하는 메커니즘

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 리액티브는 이벤트 기반이라는 말로 끝내지 말고 stream, publisher/subscriber, operator, scheduler, backpressure, 오류 전파를 구조화한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 리액티브 프로그래밍은 데이터·이벤트 흐름을 비동기 스트림으로 모델링하고 변화에 반응해 처리하는 프로그래밍 패러다임이다.
> 2. **가치**: 생산자와 소비자를 느슨하게 결합하고 backpressure로 처리 속도 차이를 제어해 tail latency와 큐 폭증을 통제한다.
> 3. **판단 포인트**: Publisher/Subscriber, operator chain, scheduler, backpressure 전략, 오류 처리 규칙을 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 반응형 모델 이해 확인 | stream, publisher, subscriber, operator | 이벤트 기반이라고만 서술 |
| backpressure 설계 확인 | request(n), buffer, drop, latest | 큐 무제한 사용 위험 누락 |
| 실무 적용 판단 확인 | Reactor, RxJava, WebFlux, observability | 디버깅 난도와 스레드 전환 비용 미제시 |

> 요약: 이 문제는 데이터 흐름 기반 설계와 소비 속도 제어를 함께 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 리액티브는 이벤트 스트림 처리 모델이다.
- 배경: 비동기 이벤트가 많은 시스템에서 동기 호출만 사용하면 느린 소비자가 upstream queue와 전체 지연을 키운다.
- 필요성: Reactive Streams, request(n), backpressure로 queue depth, dropped event rate, p99 latency 기준의 흐름 제어가 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
Event Source -> Publisher -> Operator Chain -> Scheduler
  -> Subscriber -> Backpressure Signal -> Publisher
  -> Error Channel / Completion Signal
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Publisher | 데이터·이벤트 발행 | Reactive Streams 표준 |
| Subscriber | 데이터 소비와 request 신호 전송 | onNext, onError, onComplete |
| Subscription | 구독 관계와 수요량 제어 | request(n), cancel |
| Operator | map, filter, flatMap 변환 | 체인 구성 |
| Scheduler | 실행 스레드 전환 | boundedElastic, parallel |

> 요약: 리액티브 구조는 Publisher와 Subscriber 사이에 operator와 backpressure 신호가 흐르는 스트림 처리 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
구독 생성 -> request(n) 전달 -> Publisher 발행
  -> operator 변환 -> Subscriber 소비
  -> 오류 / 완료 신호 처리 -> backpressure 조정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Subscriber가 Publisher를 구독 | subscription count |
| 2 | Subscription을 통해 request(n) 전달 | demand signal |
| 3 | Publisher가 요청량 이하 이벤트 발행 | emitted item count |
| 4 | operator chain이 변환·필터·병합 수행 | operator latency |
| 5 | 오류·완료·취소 신호 처리 | error rate, cancel count |

> 요약: 리액티브 흐름은 구독, 수요 신호, 발행, 변환, 소비, 오류/완료 처리 순서로 진행된다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | 본 기술 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 동기 호출 | 호출자가 응답 대기 | 비동기 stream 처리 | I/O 대기 많은 API |
| 단순 이벤트 | 큐 기반 전달 | request(n) backpressure | queue depth 임계치 |
| Callback | 중첩 구조 | operator chain | 오류 전파 규칙 |
| Batch | 모아서 처리 | event-driven 처리 | p95 latency, throughput |

> 요약: 리액티브는 비동기 스트림과 backpressure가 결합될 때 대량 이벤트 처리에서 가치가 있다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 동기 request/response | stream pipeline | 이벤트 연속성, I/O 대기 비율 |
| 비용/성능 | 스레드 대기 | non-blocking + scheduler | p99 지연, scheduler hop |
| 운영/위험 | 단순 stack trace | operator chain 복잡도 | tracing, checkpoint 필요성 |

> 요약: 리액티브는 이벤트 흐름과 backpressure가 필요한 시스템에 적합하며 단순 CRUD에는 복잡도를 추가할 수 있다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 큐 폭증 | 소비자 처리량 부족 | request(n), buffer limit, drop/latest | queue depth, dropped count |
| 디버깅 난도 | operator chain과 스레드 전환 | checkpoint, trace id, context propagation | trace coverage 100% |
| 블로킹 혼입 | JDBC·파일 I/O를 event loop에서 실행 | boundedElastic, R2DBC, worker 분리 | blockhound violation 0건 |

> 요약: 리액티브 운영은 큐, 추적성, 블로킹 혼입을 중심으로 통제해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 성능/지연 | p95 100ms 이하, p99 300ms 이하 | Gatling, APM |
| 품질/흐름 | dropped event 0.1% 이하, queue depth 임계치 이하 | Micrometer, broker metric |
| 운영/관측 | trace propagation 100%, blockhound 0건 | OpenTelemetry, BlockHound |

> 요약: 리액티브 도입 효과는 지연, drop 비율, 추적성, 블로킹 위반 지표로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. WebFlux/Reactor 또는 RxJava 적용 시 외부 I/O를 non-blocking client로 통일하고 JDBC는 R2DBC 또는 boundedElastic로 분리한다.
2. 각 stream에 buffer 크기, timeout, retry 횟수 3회 이하, circuit breaker를 명시해 backpressure와 장애 전파를 통제한다.
3. OpenTelemetry trace, operator checkpoint, queue depth alert를 적용해 operator chain 지연과 오류 위치를 추적한다.

**결론 (2줄):**
- 기술사 판단: 이벤트 스트림과 속도 제어가 필요한 시스템은 리액티브, 단순 CRUD와 낮은 동시성 업무는 동기 모델을 선택한다.
- 향후 방향: 리액티브 모델은 virtual thread, coroutine, event streaming과 결합해 비동기 코드 복잡도와 운영 관측성을 함께 개선한다.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "리액티브 프로그래밍을 설명하시오" | 구독, request(n), operator 흐름 | stream, backpressure, framework |
| 요구사항 명시형 | "설계하시오", "도입 방안을 제시하시오" | backpressure와 오류 처리 흐름 | 블로킹 제거, 추적성, 지표 |

> 요약: 설명형은 스트림 모델을, 설계형은 backpressure와 관측성 중심으로 목차를 전환한다.
