---
sidebar:
  order: 27
  label: "027. 리액티브 프로그래밍"
  badge:
    text: "미출 · 50%"
    variant: note
title: "리액티브 프로그래밍 (Reactive Programming)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-software"
weight: 27
extra:
  question_no: "027"
  source_status: "기출"
  source_history: ""
  priority: 50
  priority_note: "비동기 데이터 스트림과 역압 흐름 제어"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **리액티브 프로그래밍(Reactive Programming)**: 데이터 스트림과 변경 사항의 전파를 비동기 논블로킹(Non-blocking) 방식으로 처리하는 선언적 프로그래밍 패러다임.
- **역압(Backpressure)**: 소비자의 처리 속도에 맞춰 발행자의 데이터 전송 속도를 조절하는 비차단 흐름 제어 메커니즘.

</details>

- 정의/개념: 비동기 데이터 스트림의 변화 전파와 **역압(Backpressure)** 제어로 시스템 자원을 최적화하는 선언적 프로그래밍 패러다임
- 배경/필요성: 데이터 생산 속도가 소비 처리 속도를 초과할 때 발생하는 다운스트림 메모리 고갈(OOM) 및 소비자 스레드 블로킹 병목과, 비동기 파이프라인의 오류 전파 난제를 극복하고, 소비자가 수용 가능한 데이터 수량만큼만 요청하는 비차단 역압(Backpressure) 규약과 함수형 데이터 스트림(Reactive Streams)을 통해 **시스템 반응성(Responsive)과 탄력성(Elastic)을 보장**할 필요

#### 한줄 요약
- 비동기 데이터 스트림과 역압 제어를 통해 자원 효율성과 시스템 반응성을 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **리액티브 선언문(Reactive Manifesto)**: 반응성(Responsive), 복원력(Resilient), 탄력성(Elastic), 메시지 구동(Message Driven)의 4대 핵심 원칙.
- **리액티브 스트림즈(Reactive Streams)**: JVM 환경에서 비차단 역압을 구현하기 위한 4대 인터페이스 표준 사양.

</details>

- **리액티브 스트림즈(Reactive Streams)** 4대 표준 인터페이스(Publisher, Subscriber, Subscription, Processor) 준수
- **역압(Backpressure)** 기반의 수요 기반 풀링(`request(n)`)을 통해 버퍼 오버플로우 방지
- 함수형 연산자 체이닝(Operator Chaining)을 통한 비동기 데이터 파이프라인 구성

#### 한줄 요약
- 역압은 시스템이 무너지지 않게 하는 대신 생산자의 속도를 소비자에 맞춰 낮추므로, 안정성은 최대 처리량을 내주고 얻는 속성이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Publisher & Subscriber**: 데이터를 발행하는 주체(Publisher)와 이를 구독하여 소비하는 주체(Subscriber).
- **Subscription**: 발행자와 구독자를 연결하여 데이터 수량 요청(`request`) 및 취소(`cancel`)를 수행하는 제어 객체.

</details>

```text
[리액티브 스트림즈 4대 인터페이스 구조]
|-- 발행자 (Publisher)
|   `-- subscribe(Subscriber) -> Subscription 객체 생성 및 전달
|-- 구독 (Subscription)
|   |-- request(n) -> 소비자가 수용 가능한 데이터 수량 n 역압 전달
|   `-- cancel() -> 스트림 구독 즉시 취소
|-- 구독자 (Subscriber)
|   |-- onSubscribe(Subscription) -> 구독 시작
|   |-- onNext(Item) -> 데이터 수신 처리
|   |-- onError(Throwable) -> 에러 처리
|   `-- onComplete() -> 스트림 완료 처리
`-- 프로세스 (Processor - Publisher와 Subscriber의 결합 중간 파이프라인)
```

선의 의미: 계층 및 구독/역압 제어 파이프라인

| 구성요소 | 책임 |
|:---|:---|
| 발행자 | 요청 수량에 맞춘 **데이터 발행** |
| 구독자 | 이벤트 수신과 **비즈니스 처리** |
| 구독 | `request(n)` **역압·취소 제어** |
| 프로세서 | 변환·필터링·버퍼링 **파이프라인 중계** |

#### 한줄 요약
- Subscription이 소비자에서 생산자로 흐르는 역방향 통로이므로, 데이터 흐름과 제어 흐름이 서로 반대로 놓인다는 점이 리액티브 구조의 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **request(n)**: 소비자가 현재 처리 가능한 버퍼 여유 공간($n$)만큼만 데이터 전송을 요구하는 역압 신호.

</details>

```text
Subscriber                      Publisher                   Subscription
    │                               │                             │
    ├─── subscribe(Subscriber) ────▶│                             │
    │                               ├─── onSubscribe(sub) ───────▶│
    │◀── Subscription 객체 전달 ────┘                             │
    │                                                             │
    ├─── request(n: 역압 수량) ──────────────────────────────────▶│
    │                                                             │
    │◀── onNext(data) 데이터 수신 ────────────────────────────────┤
    │                                                             │
    │◀── onComplete() 완료 통지 ──────────────────────────────────┘
```

#### 한줄 요약
- request(n)이 없으면 데이터가 흐르지 않으므로, 소비자가 요청량을 정하는 순간이 처리량과 안정성의 균형이 실제로 결정되는 지점이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Mono vs Flux**: Project Reactor에서 0~1개의 결과를 방출하는 Mono와 0~N개의 무한 스트림을 방출하는 Flux.

</details>

| 비교 항목 | 명령형 동기 모델 (Spring MVC) | 리액티브 모델 (Spring WebFlux) | 가상 스레드 (Java Loom) |
|:---|:---|:---|:---|
| 스레드 모델 | **Thread-per-Request (스레드 풀)** | **이벤트 루프 (Non-blocking)** | Thread-per-Request (경량 M:N) |
| 흐름 제어 | 블로킹 대기 (버퍼 한계 시 지연) | **역압(Backpressure) 기반 수요 조절** | 블로킹 대기 (OS 스레드 양보) |
| I/O 처리 방식 | 동기 블로킹 I/O (JDBC 등) | **비동기 논블로킹 I/O (R2DBC, Netty)** | 동기 블로킹 인터페이스 유지 |
| 코드 복잡도 | 낮음 (직관적, 디버깅 용이) | **높음 (함수형 체이닝, 학습 곡선)** | 낮음 (기존 동기 코드 유지) |

#### 한줄 요약
- 단순 엔터프라이즈는 MVC/가상스레드가, 실시간 대규모 스트리밍과 완벽한 역압 제어는 WebFlux가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Schedulers.boundedElastic()**: 리액티브 파이프라인 내에서 레거시 블로킹 I/O(파일, JDBC)를 격리 실행하기 위한 탄력적 스레드 풀.
- **BlockHound**: 리액티브 논블로킹 스레드 내에서 실수로 블로킹 API가 호출되는 것을 실시간 감지하여 예외를 던지는 진단 라이브러리.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 이벤트 루프 내 레거시 블로킹 호출로 전체 스레드 마비 | 블로킹 구간에 **`publishOn(Schedulers.boundedElastic())`** 격리 | 논블로킹 이벤트 루프 보호 및 서비스 연속성 확보 |
| 비동기 체인 오류 시 스택트레이스 단절로 디버깅 곤란 | **`Hooks.onOperatorDebug()` 및 BlockHound** 적용 | 오류 발생 위치 정확 추적 및 블로킹 코드 원천 차단 |
| 다운스트림 처리 지연으로 인한 발행자 버퍼 오버플로우 | **`onBackpressureBuffer()` / `onBackpressureDrop()`** 전략 설정 | 메모리 고갈 방지 및 유실 허용 정책 적용 |
| 복잡한 리액티브 연산자 체인으로 인한 유지보수성 저하 | **Kotlin Coroutines (Flow / suspend)** 결합 도입 | 명령형 스타일의 가독성과 리액티브 비동기 성능 동시 확보 |

#### 한줄 요약
- 역압은 처리량을 소비자 속도에 맞춰 낮추는 대가로 시스템 붕괴를 막는 장치이므로, 버퍼·드롭·에러 중 어떤 전략을 쓸지는 데이터 유실과 지연 중 무엇을 감당할 수 있는지로 정한다.

## Ⅶ. 결론

- 대규모 실시간 데이터 스트리밍(Kafka, WebSockets) 및 고동시성 마이크로서비스의 **핵심 비동기 스트림 처리 패러다임**으로 정립되었으며, 실무 엔터프라이즈 환경에서는 **완벽한 논블로킹 I/O(R2DBC, Netty) 기반 파이프라인 구축을 기본으로, 레거시 블로킹 구간의 `Schedulers.boundedElastic()` 격리, BlockHound 런타임 검증, Kotlin Coroutines(Flow)를 통한 코드 가독성 개선**을 결합하여 운영

#### 한줄 요약
- 리액티브 프로그래밍은 역압 제어와 비차단 스트림을 통해 시스템 과부하를 방지하고 무중단 반응성을 실현하는 현대 분산 시스템의 핵심 패러다임이다.
