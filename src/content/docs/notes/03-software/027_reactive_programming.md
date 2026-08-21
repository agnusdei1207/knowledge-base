---
sidebar:
  order: 27
  label: "027. 리액티브 프로그래밍"
  badge:
    text: "미출 · 50%"
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

<details><summary>용어 설명</summary>

- **리액티브 프로그래밍(Reactive Programming)**: 데이터가 들어올 때마다 파이프라인을 타고 물 흐르듯이 비동기(Asynchronous) 이벤트로 퍼져나가게 만드는 스트림(Stream) 중심의 선언적 프로그래밍 패러다임이다.
- **리액티브 스트림즈 규약(Reactive Streams Specification)**: 비동기 데이터 폭주로 램이 터지는 걸 막기 위해, "내가 소화할 수 있는 만큼만 보내!"라고 역압(Backpressure)을 통제하는 자바 진영의 4대 인터페이스 국제 룰이다.

</details>

- 정의: 데이터 변화를 이벤트 스트림으로 묶어버리고, 역압(Backpressure)으로 폭주를 제어하며 비동기로 쳐내는 **리액티브 프로그래밍**
- 배경: 넷플릭스 같은 데서 생산 속도가 소비 속도를 급격히 넘어서버리면 **버퍼 고갈과 OOM(Out of Memory)** 이 터지기 때문

#### 한줄 요약

- 데이터가 변하면 파이프를 타고 흐르되, 구독자가 감당 가능한 만큼만 쏘게(역압) 통제하는 코딩이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **역압(Backpressure)**: 수돗물 콸콸 틀어놓고 컵으로 받으면 물이 넘치니까, 컵 쥔 사람(Subscriber)이 수도꼭지(Publisher)한테 "나 지금 3방울만 줘(`request(n)`)"라고 통제하는 생존 제어기이다.
- **리액티브 매니페스토(Reactive Manifesto)**: 현대 앱은 무조건 즉각 응답하고(Responsive), 뒤져도 다시 살아나며(Resilient), 쫄깃하게 늘어나야(Elastic) 한다는 메시지 기반 4대 헌장이다.

</details>

- **Reactive Streams (Publisher, Subscriber, Subscription)** 표준 스펙을 따름.
- **Non-blocking Backpressure (`request(n)`)** 로 소비자(구독자) 멱살을 보호함.
- 콜백 지옥을 체인 메서드(Operator Chain)로 묶어 비동기 스레딩을 우아하게 만듦.

#### 한줄 요약

- 반응성, 복원력, 탄력성을 목표로 하며, 역압(Backpressure)으로 데이터 폭주를 제어한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **퍼블리셔(Publisher)**: 데이터(이벤트)를 쉴 새 없이 뱉어내는 놈(`subscribe()`로 구독 받음).
- **서브스크라이버(Subscriber)**: 데이터 받아먹으면서 처리하는 놈(`onNext`, `onError`, `onComplete`).
- **서브스크립션(Subscription)**: 위 두 놈 사이에서 "몇 개 더 줘(`request`)", "그만 줘(`cancel`)" 하고 멱살 조율하는 매개체이다.

</details>

```text
[ 리액티브 스트림 십자포화 아키텍처 ]

 [ Publisher (발행자) ]  ◀── (2) 나 10개만 줘! request(10)
(DB, Message Broker 등)
           │ (1) onSubscribe
           ▼
 [ Subscription (구독) ] ──▶ [ Processor ] (중간 필터/가공)
           │
           ▼ (3) 데이터 투척! onNext()
[ Subscriber (구독/소비자) ]
 (클라이언트, 웹 응답 등)
           │ (4) 끝! onComplete()
           ▼
```

| 구성요소 | 주요 역할 및 핵심 메서드 |
|:---|:---|
| **Publisher** | 스트림 데이터의 발원지, "내꺼 볼 사람?" 하고 **`subscribe(Subscriber)`** 기반 구독자를 받음 |
| **Subscriber** | 데이터를 씹고 맛보는 주체, **`onNext()`** 기반 데이터 받고 **`onComplete/onError()`** 기반 끝냄 |
| **Subscription** | 구독자와 발행자 사이 계약서, 데이터 수량을 역으로 조율하는 **`request(n)`** 및 취소 **`cancel()`** 핸들링 |
| Processor | Publisher와 Subscriber 성질을 둘 다 가져서, 중간에서 데이터를 지지고 볶는 가공자 레이어 |

#### 한줄 요약

- 퍼블리셔가 쏘고, 서브스크라이버가 받는데, 그 사이에서 서브스크립션이 물량을 조율한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **콜드 퍼블리셔 vs 핫 퍼블리셔(Cold vs Hot Publisher)**: Cold는 넷플릭스 VOD처럼 구독할 때마다 1화부터 새로 틀어주는 놈이고, Hot은 아프리카TV 라이브처럼 중간에 들어오면 생방송 중간부터 봐야 하는 놈이다.

</details>

```text
[ 리액티브 역압 제어 십자포화 흐름 ]
┌──────────────────────────────┐
│ 1. 구독 요청 (subscribe)     │
│ (Subscriber ➔ Publisher)     │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 2. 구독 티켓 발급 (onSubscribe)│
│ (Publisher ➔ Subscriber)     │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 3. 데이터 수요 요청 (request)│
│ (Subscriber ➔ Subscription)  │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 4. 데이터 발행 (onNext)      │
│ (Publisher ➔ Subscriber)     │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 5. 스트림 종료 (onComplete)  │
│ (Publisher ➔ Subscriber)     │
└──────────────────────────────┘
```

### 동작 원리

1. 구독 요청: 소비자가 데이터 뱉는 놈한테 `subscribe()`로 나도 껴달라고 조름.
2. 구독 설정: 뱉는 놈이 알았다고 **`Subscription`** 객체를 던져줌 (`onSubscribe`).
3. 수요량 요청: 소비자가 뻗지 않을 만큼만 **`request(n)`** 기반 개수를 콕 집어 요청함(역압).
4. 데이터 발행: 뱉는 놈이 요청받은 개수 안에서만 **`onNext()`** 기반 데이터를 쏴줌.
5. 스트림 완료/에러: 다 줬으면 **`onComplete()`**, 중간에 터지면 **`onError()`** 쏘고 셧다운함.

#### 한줄 요약

- 구독 $\to$ 티켓 발급 $\to$ n개 요청 $\to$ n개 쏴줌 $\to$ 끝남의 우아한 5단계 흐름이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **모노(Mono) vs 플럭스(Flux)**: Spring WebFlux(Reactor)의 두 핵심 객체로, 데이터가 0~1개만 나오면 단발성 `Mono`를 쓰고, 0~N개가 쉴 새 없이 쏟아지면 `Flux`를 쓴다.

</details>

| 구분 | **명령형 동기 (Imperative)** | **리액티브 비동기 (Reactive)** |
|:---|:---|:---|
| 데이터 처리 방향 | 필요할 때 강력히 끌고 옴 (**Pull Model**) | 발행자가 이벤트 생기면 알아서 밀어줌 (**Push Model**) |
| 블로킹(대기) 여부 | DB 쿼리 치고 올 때까지 스레드가 멍 때림 | 찔러놓고 딴짓하다가 이벤트 오면 콜백 쳐냄 (**Non-blocking**) |
| 폭주 제어 | OOM 터지거나 세마포어로 큐를 억지로 틀어막음 | 애초에 감당 가능한 만큼만 줘! 하는 **역압(Backpressure)** 장착 |
| 찰떡 생태계 | Java Stream API, JPA, Spring MVC | **Spring WebFlux (Reactor), RxJava, R2DBC** |

#### 한줄 요약

- 당겨오는(Pull) 동기식과 달리, 리액티브는 이벤트가 오면 밀어주는(Push) 논블로킹 방식이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **publishOn vs subscribeOn**: `publishOn`은 내 밑으로 데이터 처리할 스레드 풀을 갈아타게 하는 놈이고, `subscribeOn`은 아예 맨 위 첫 구독(데이터 생성)부터 무슨 스레드에서 시작할지 멱살 잡는 놈이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 리액티브에 낡은 JDBC(블로킹) 호출 섞었다가 이벤트 루프 스레드 마비됨 | JDBC 찌르는 구역만 **`publishOn(Schedulers.boundedElastic())`** 유배 보냄 | 메인 이벤트 루프 뻗는 심각한 결함 막아내고 생태계 사수 |
| 에러 나면 아무 말 없이 멈추는 리액티브 특유의 장애 혼선 디버깅 헬 | 에러 났을 때 대체 응답을 주는 **`onErrorResume()`** 이나 **`BlockHound`** 훅 박음 | 스트림 붕괴 차단 및 비동기 스택 트레이스 추적성 회복 |
| 콜백 피하려다 `flatMap` 지옥 열려서 코드 가독성 멸망함 | 무지성 체이닝 버리고 코틀린(Kotlin) **Coroutines** 섞어 씀 | 동기식 깡코딩처럼 예쁘게 보이게 만들어 개발자 수명 연장 |

#### 한줄 요약

- 블로킹 로직은 스케줄러로 찢고, 에러는 오퍼레이터로 잡으며, 코드 지옥은 코루틴으로 탈출해라.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **리액티브 도입 선택 기준(Reactive Adoption Criteria)**: 트래픽이 넷플릭스급인지, 개발팀이 비동기 체이닝에 미쳐버리지 않을 자신이 있는지 각 재서 Spring WebFlux를 꽂을지 결정하는 잣대이다.

</details>

- **리액티브 도입 선택 기준** 원칙에 따라, 대규모 실시간 스트리밍/채팅은 무조건 **리액티브(Reactor)**, 구멍가게 CRUD 게시판은 낡은 **명령형(MVC)** 채택 기조 확립함

#### 한줄 요약

- 접속자 수만 명의 실시간 스트리밍은 리액티브, 단순 사내 게시판은 동기식(MVC)이 짱이다.
