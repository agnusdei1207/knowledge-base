---
title: "리액티브 스트림 (Reactive Streams)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 276
---

## Ⅰ. 개요
- **정의**: 비동기 데이터 스트림을 배압(Backpressure) 제어와 함께 처리하는 논블로킹 표준 사양
- **배경/필요성**: 생산자-소비자 속도 불일치가 메모리 폭증이나 데이터 유실을 유발하므로 흐름 제어가 필요함
- **비유**: 수도꼭지(생산자)와 컵(소비자) 사이에서 넘치지 않도록 수량을 조절하는 밸브와 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 배압 메커니즘·비동기 흐름 제어 | Publisher-Subscriber 4인터페이스, `request(n)` 흐름 | 리액티브 프로그래밍과 리액티브 스트림 사양을 구분할 것 |

> 요약: 배압 기반 비동기 스트림 처리 표준으로, 생산-소비 속도 불일치를 해결함

## Ⅱ. 구성요소
```text
Publisher --onSubscribe--> Subscriber
Subscriber --request(n)--> Publisher
Publisher --onNext(data)--> Subscriber
           --onComplete/onError-->

Processor = Publisher + Subscriber (중간 연산)
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Publisher | 데이터 항목을 생성하여 Subscriber에게 전달하는 소스 | 신문사 — 기사를 발행함 |
| Subscriber | `onNext`로 데이터를 수신하고 `request(n)`으로 수요량을 통보 | 구독자 — 읽을 수 있는 만큼만 요청함 |
| Subscription | Publisher-Subscriber 간 연결 상태를 관리하고 `request`·`cancel` 제공 | 구독 계약서 — 수량·해지 조건 명시 |
| Processor | Publisher와 Subscriber를 겸하여 중간 변환·필터 역할 수행 | 편집부 — 기사를 가공하여 전달함 |

> 요약: Publisher-Subscriber-Subscription-Processor 4개 인터페이스로 구성됨

## Ⅲ. 절차
```text
subscribe -> onSubscribe -> request(n) -> onNext * n -> onComplete
```
- 1단계: Subscriber가 Publisher에 `subscribe()`를 호출하여 구독 등록
- 2단계: Publisher가 `onSubscribe(Subscription)`으로 Subscription 객체 전달
- 3단계: Subscriber가 `request(n)`으로 처리 가능 항목 수를 통보하면 Publisher가 최대 n개 `onNext` 발행
- 4단계: 모든 항목 발행 완료 시 `onComplete`, 오류 발생 시 `onError` 호출로 스트림 종료

> 요약: 구독 → Subscription 수립 → 배압 요청 → 발행/종료 순서로 동작함

## Ⅳ. 문제점
- 디버깅 난이도: 비동기 콜백 체인이 깊어지면 스택 트레이스가 단절되어 오류 추적이 어려움
- 배압 미구현: Subscriber가 `request`를 호출하지 않으면 무한 버퍼링으로 OOM 발생
- 학습 곡선: 선언형 연산자 체인(`flatMap`, `merge`, `zip`)의 조합 복잡도가 높음

> 요약: 비동기 디버깅 난이도, 배압 미구현 위험, 연산자 학습 비용이 주요 문제임

## Ⅴ. 개선방안
1. 단기: Context Propagation(Micrometer Context)으로 비동기 트레이스 연결 복원
2. 중기: `onBackpressureBuffer`·`onBackpressureDrop` 등 배압 전략을 표준 적용
3. 장기: 코루틴 기반 Flow(Kotlin Flow) 등 순차적 가독성과 배압을 동시에 확보하는 모델 도입

> 요약: 트레이스 전파, 배압 전략 표준화, 코루틴 Flow로 각 문제에 대응함

## Ⅵ. 전망
- 발전 방향: 가상 스레드와 리액티브 스트림의 융합으로 논블로킹과 가독성을 동시 달성하는 추세
- 기술사적 판단: MSA 간 비동기 통신에서 배압 제어가 시스템 안정성의 핵심 요소임
- 기술사 제언: 서비스 간 메시지 큐와 리액티브 스트림의 배압 전략을 통합 설계할 필요
