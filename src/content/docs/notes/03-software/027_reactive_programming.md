---
sidebar:
  order: 27
  label: "027. 리액티브 프로그래밍 (Reactive Programming)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "리액티브 프로그래밍 (Reactive Programming)"
date: "2026-08-13T14:05:00+09:00"
tags:
  - "notes-software"
weight: 27
extra:
  question_no: "027"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "리액티브는 비동기 흐름•역압 설계에 유효"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Reactive Programming (리액티브 프로그래밍)**: 데이터 스트림(Data Stream)과 변화 전파(Propagation of Change)에 기반하여, 비동기(Asynchronous) 이벤트 흐름을 선언적(Declarative)으로 작성하는 프로그래밍 파라다임.
- **Reactive Streams Specification**: JVM 상에서 비동기 스트림 처리 시 논블로킹 역압(Non-blocking Backpressure)을 통제하기 위해 제정된 표준 규약 (Publisher, Subscriber, Subscription, Processor 4대 인터페이스).

</details>

- 정의/개념: 데이터의 변화를 이벤트 스트림으로 래핑하고, Subscriber가 처리 가능한 수량만큼 역압(Backpressure)을 조정하며 비동기 처리하는 **리액티브 프로그래밍(Reactive Programming)**
- 배경/필요성: 생산 속도가 소비 속도를 넘으면 **버퍼 고갈•지연 누적** 발생

#### 한줄 요약

- 데이터 변화와 수요량을 스트림 신호로 전파하는 리액티브 프로그래밍이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Backpressure (역압)**: 데이터 소비자(Subscriber)가 자신의 처리 역량(Buffer)에 맞추어 생성자(Publisher)에게 전송 데이터 수량을 역으로 요청(`request(n)`)하여 데이터 폭주를 방지하는 제어 메커니즘.
- **Reactive Manifesto 4대 요소**: Responsive(응답성), Resilient(복원력), Elastic(탄력성), Message-Driven(메시지 기반).

</details>

- **Reactive Streams (Publisher, Subscriber, Subscription)** 표준 사양 수용
- **Non-blocking Backpressure (`request(n)`)** 통한 소비자 중심 흐름 제어
- 선언적 파이프라인(Operator Chain) 및 비동기 멀티스레딩 스케줄링 간편화

#### 한줄 요약

- 수요 범위의 데이터와 종단 신호를 전달한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Publisher**: 데이터를 생성하여 연결된 Subscriber에게 스트림 이벤트를 발행하는 인터페이스 (`subscribe(Subscriber)`).
- **Subscriber**: Publisher가 발행하는 데이터를 수용하여 연산을 처리하는 인터페이스 (`onSubscribe`, `onNext`, `onError`, `onComplete`).
- **Subscription**: Publisher와 Subscriber 간의 매개체로, 역압 수량 요청(`request(n)`) 및 데이터 스트림 취소(`cancel()`) 관리.

</details>

```text
+--------- 리액티브 스트림 ---------+
|                                   |
| [Publisher] ------ [Processor]    |
|     |                    |         |
| [Subscription] ---- [Subscriber]   |
|                                   |
+-----------------------------------+
```

선의 의미: Publisher와 Subscriber가 Subscription 객체를 매개로 연결되어 데이터(`onNext`)는 하향 전파되고 역압(`request(n)`)은 상향 전달되는 리액티브 흐름.

| 구성요소 | 주요 역할 및 핵심 메서드 |
|:---|:---|
| **Publisher** | 데이터 스트림의 발원지, `subscribe(Subscriber s)`로 구독 수용 |
| **Subscriber** | 스트림 데이터 소비 주체, `onSubscribe()`, `onNext()`, `onError()`, `onComplete()` 제공 |
| **Subscription** | 발행자-구독자 간 역압 조율 인터페이스, `request(long n)` 및 `cancel()` 핸들링 |
| **Processor** | Publisher와 Subscriber 기능을 동시 수행하는 intermediate 오퍼레이터 레이어 |

#### 한줄 요약

- 발행자, 구독, 구독자의 양방향 신호 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Cold Publisher vs Hot Publisher**: Cold는 구독(Subscribe)이 발생할 때마다 독립적 스트림 데이터를 처음부터 생성하는 반면, Hot은 구독 여부와 무관하게 이벤트를 상시 발행하는 차이.

</details>

```text
┌──────────────────────────────┐
│ 스트림 구독 요청 (subscribe) │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 구독 설정                │
│ 2. 수요량 요청              │
│ 3. 데이터 발행              │
│ 4. 변환•소비                │
│ 5. 완료•에러                │
└──────────────────────────────┘
```

### 동작 원리

1. **구독 설정**: Publisher가 Subscription을 Subscriber에 전달
2. **수요량 요청**: Subscriber가 `request(n)`으로 허용 수량 지정
3. **데이터 발행**: Publisher가 수요 범위에서 `onNext` 전달
4. **변환·소비**: Processor가 데이터를 변환하고 하류로 전파
5. **완료·에러**: `onComplete` 또는 `onError` 종단 신호 전달

#### 한줄 요약

- 수요량 요청부터 수요 잔량 갱신까지의 반복이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Mono vs Flux**: Project Reactor에서 제공하는 객체로, Mono는 0~1개의 단일 비동기 데이터 발행, Flux는 0~N개의 비동기 연속 데이터 스트림 발행.

</details>

| 비교 항목 | Reactive Programming (리액티브) | Traditional Imperative (명령형) |
|:---|:---|:---|
| 데이터 전달 방식 | **Push Model** (발행자가 데이터 전파) + 역압 | **Pull Model** (소비자가 데이터를 직접 요청) |
| 대기 모델 | 비차단 파이프라인 구성 가능 | 호출 흐름에서 대기 가능 |
| 흐름 제어 | **Backpressure (`request(n)`)** 표준화 | 큐•세마포어 등 별도 제어 |
| 대표 라이브러리 | **RxJava, Project Reactor (Spring WebFlux)** | Java Collections, Stream API |

#### 한줄 요약

- 연속 이벤트는 리액티브, 단순 순차는 명령형 동기 처리가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **publishOn vs subscribeOn**: publishOn은 오퍼레이터 체인 하류(Downstream)의 실행 스케줄러 스레드를 변경하고, subscribeOn은 스트림 상류(Upstream) 구독 시작 스레드를 지정.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 비동기 오퍼레이터 체인 실행 중 예외 처리 난해 | **`onErrorResume()`, `onErrorReturn()`** 오퍼레이터 적용 | 스트림 붕괴 차단 및 대체 응답 전달 |
| Blocking I/O 라이브러리(JPA, JDBC) 호출로 스레드 마비 | **`publishOn(Schedulers.boundedElastic())`** 격리 스레드풀 할당 | 리액티브 이벤트 루프 보호 |
| 런타임 콜백 스택 트레이스 유실로 인한 디버깅 불능 | **`Hooks.onOperatorDebug()`** 디버그 훅 또는 Reactor BlockHound 적용 | 비동기 스택 트레이스 추적성 확보 |

> 사례: **Spring Boot 3 + Spring WebFlux + R2DBC** 기반 전 구간(End-to-End) Non-blocking 리액티브 시스템 구축

#### 한줄 요약

- 수요 묶음, 버퍼 상한, 스케줄러 격리, 재시도 상한을 통제한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **리액티브 도입 선택 기준(Reactive Adoption Criteria)**: 타깃 세션 동시성 수치, DB/외부 API 비동기 R2DBC 수용 여부 및 개발팀 리액티브 숙련도에 기반한 체계.

</details>

- 연속 비동기 스트림은 **Reactor**, 단순 순차 업무는 **명령형** 선택

#### 한줄 요약

- 생산•소비 속도 차와 업무 순차성을 함께 평가하는 것이 핵심이다.
