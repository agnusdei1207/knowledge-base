---
sidebar:
  order: 27
  label: "027. 리액티브 프로그래밍 (Reactive Programming)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "리액티브 프로그래밍 (Reactive Programming)"
date: "2026-08-22T07:15:00+09:00"
tags:
  - "notes-software"
weight: 27
extra:
  question_no: "027"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "비동기 데이터 스트림과 역압 흐름 제어"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **리액티브 프로그래밍(Reactive Programming)**: 데이터 스트림과 변화의 전파를 비동기 논블로킹 방식으로 처리하는 선언적 프로그래밍 패러다임.
- **리액티브 스트림즈(Reactive Streams)**: 비동기 스트림 처리 환경에서 비차단 역압(Non-blocking Backpressure)을 제공하기 위한 표준 사양.

</details>

- 정의/개념: 비동기 데이터 스트림의 변화 전파와 **역압(Backpressure)** 제어로 시스템 자원을 최적화하는 프로그래밍 패러다임
- 배경/필요성: 대규모 동시 요청 환경에서 생산자와 소비자 간 처리 속도 불균형으로 인한 메모리 고갈 및 스레드 블로킹 병목 발생

#### 한줄 요약
- 비동기 데이터 스트림과 역압 제어를 통해 자원 효율성과 시스템 반응성을 보장하는 선언적 프로그래밍 기법이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **역압(Backpressure)**: 소비자가 감당 가능한 처리 용량만큼만 발행자에게 데이터 전송을 요청하는 흐름 제어 메커니즘.
- **리액티브 선언문(Reactive Manifesto)**: 반응성(Responsive), 복원력(Resilient), 탄력성(Elastic), 메시지 기반(Message Driven)의 4대 핵심 가치를 정의한 아키텍처 설계 원칙.

</details>

- **리액티브 스트림즈(Reactive Streams)** 4대 인터페이스(Publisher, Subscriber, Subscription, Processor) 표준 준수
- **역압(Backpressure)** 기반 비차단 수요 요청(`request(n)`)을 통해 소비자 측 버퍼 오버플로우 방지
- 연산자 체이닝(Operator Chain)을 통한 비동기 이벤트 파이프라인 구성 및 비차단 I/O 처리

#### 한줄 요약
- 반응성과 복원력을 목표로 하며, 역압 기반 흐름 제어로 비동기 파이프라인의 안정성을 확보한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **발행자(Publisher)**: 구독자의 요청에 따라 데이터 스트림 이벤트를 생성하고 전달하는 인터페이스.
- **구독자(Subscriber)**: 스트림 이벤트를 수신하여 비즈니스 로직을 처리하는 인터페이스.
- **구독(Subscription)**: 발행자와 구독자 간의 연결 고리로서 데이터 요청(`request`)과 취소(`cancel`)를 관리하는 제어 객체.
- **프로세서(Processor)**: 발행자와 구독자의 역할을 동시에 수행하며 데이터 변환 및 가공을 담당하는 중간 계층.

</details>

```text
[ 발행자 (Publisher) ]
        │
        ├─ 1. onSubscribe(Subscription)
        ▼
[ 구독 (Subscription) ] ─── 2. request(n) / cancel() ─── [ 구독자 (Subscriber) ]
        │                                                        │
        └─────────────── 3. onNext(data) / onComplete() ─────────┘
```

선의 의미: `├─`는 구독 생성 흐름, 화살표는 역압 요청 및 데이터 발행 경로

| 구성요소 | 책임 |
|:---|:---|
| **발행자(Publisher)** | `subscribe(Subscriber)`를 통해 구독자를 등록하고 스트림 데이터 발행 |
| **구독자(Subscriber)** | `onNext()`, `onError()`, `onComplete()`를 통해 이벤트 수신 및 소비 |
| **구독(Subscription)** | `request(n)`으로 역압 수량을 전달하고 `cancel()`로 구독 중단 제어 |
| **프로세서(Processor)** | 스트림 중간에서 데이터 필터링, 변환 및 다중 파이프라인 중계 |

#### 한줄 요약
- 발행자와 구독자 간에 구독(Subscription) 객체를 매개로 데이터 흐름과 역압 요청을 제어한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **콜드 스트림(Cold Stream)**: 구독자가 구독을 시작할 때마다 데이터 생성을 처음부터 독립적으로 시작하는 스트림.
- **핫 스트림(Hot Stream)**: 구독 여부와 무관하게 데이터가 지속적으로 생성 및 방송되는 스트림.

</details>

```text
구독자 (Subscriber)              발행자 (Publisher)            구독 객체 (Subscription)
       │                                │                                │
       ├──────── 1. subscribe() ───────▶│                                │
       │                                ├──── 2. onSubscribe() ─────────▶│
       │◀─────── 3. Subscription 전달 ──┘                                │
       │                                                                 │
       ├──────── 4. request(n) ─────────────────────────────────────────▶│
       │                                                                 │
       │◀─────── 5. onNext(data) ────────────────────────────────────────┤
       │◀─────── 6. onComplete() ────────────────────────────────────────┘
```

**동작 원리**

1. **구독 요청**: 구독자가 발행자에게 `subscribe()`를 호출하여 스트림 구독 등록
2. **구독 객체 생성**: 발행자가 구독자 전용 `Subscription` 인스턴스를 생성
3. **구독 전달**: `onSubscribe()` 콜백을 통해 구독자에게 `Subscription` 제어권 부여
4. **수요 요청**: 구독자가 처리 가능한 용량 `n`만큼 `request(n)`을 호출하여 역압 신호 전달
5. **데이터 발행**: 발행자가 요청받은 수량 `n` 이하의 데이터를 `onNext()`로 비차단 전송
6. **스트림 완료**: 모든 데이터 발행 완료 시 `onComplete()` 호출로 스트림 종료

#### 한줄 요약
- 구독 등록 후 소비자가 요청한 수량만큼만 데이터를 비동기로 전달하여 과부하를 방지한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **모노(Mono)**: 0개 또는 1개의 결과 데이터만을 비동기로 방출하는 리액티브 스트림 타입.
- **플럭스(Flux)**: 0개부터 N개의 무한 데이터 스트림을 비동기로 방출하는 리액티브 스트림 타입.

</details>

| 프로그래밍 패러다임 | 명령형 동기 모델 (Imperative) | 리액티브 비동기 모델 (Reactive) |
|:---|:---|:---|
| 적용 기준 | 정적 트랜잭션, CPU 집약적 연산, 단순 CRUD | 대규모 동시 연결, I/O 바운드 시스템, 스트리밍 처리 |
| 핵심 특징 | 스레드당 단일 요청 처리(Thread-per-Request) 및 동기 블로킹 | 이벤트 루프 기반 비차단 I/O 및 **역압(Backpressure)** 제어 |
| 한계 | 동시 요청 증가 시 스레드 풀 고갈 및 컨텍스트 스위칭 오버헤드 | 비동기 흐름 제어 복잡도 증가 및 디버깅 추적성 저하 |

#### 한줄 요약
- 동기 블로킹 방식과 달리, 리액티브는 이벤트 기반 비차단 I/O와 역압 제어로 동시성 처리량을 극대화한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **스케줄러(Scheduler)**: 리액티브 파이프라인에서 실행될 스레드 풀(Elastic, Parallel 등)의 실행 컨텍스트를 지정하는 관리자.
- **블록하운드(BlockHound)**: 리액티브 이벤트 루프 스레드 내에서 블로킹 호출이 발생하는지 런타임에 감지하는 디버깅 도구.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 이벤트 루프 내 블로킹 I/O(JDBC 등) 호출로 전체 스레드 마비 | 블로킹 연산 구간에 **`publishOn(Schedulers.boundedElastic())`** 격리 적용 | 비차단 이벤트 루프 보호 및 처리 지속성 확보 |
| 비동기 예외 전파 누락 및 디버깅 스택 추적 곤란 | **`onErrorResume()`**, `Hooks.onOperatorDebug()` 및 **BlockHound** 적용 | 장애 격리 및 런타임 오류 추적성 향상 |
| 과도한 연산자 체이닝으로 인한 코드 가독성 저하 | 도메인 로직 모듈화 및 코틀린 **Coroutines** 연계 적용 | 명령형 스타일의 가독성과 비동기 논블로킹 성능 동시 확보 |

#### 한줄 요약
- 블로킹 I/O 격리와 에러 핸들러 설계를 통해 리액티브 런타임의 안정성과 유지보수성을 보장한다.

## Ⅶ. 결론

- 대규모 동시 연결과 I/O 바운드 이벤트 스트리밍에는 **리액티브(WebFlux/R2DBC)** 아키텍처를 도입하되, 레거시 블로킹 라이브러리 의존도가 높은 환경에서는 명령형 MVC 모델을 유지하거나 전용 스케줄러 풀로 격리하여 점진적 전환을 추진

#### 한줄 요약
- 워크로드의 동시성 요구사항과 블로킹 의존성을 분석하여 리액티브 비차단 파이프라인을 선별 적용한다.
