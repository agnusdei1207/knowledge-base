---
sidebar:
  order: 8
  label: "008. 스레드 스케줄링•스레드 풀"
  badge:
    text: "미출 · 50%"
    variant: note
title: "스레드 스케줄링•스레드 풀 (Thread Scheduling•Thread Pool)"
date: "2026-08-26T09:32:00+09:00"
tags: [notes-software]
weight: 8
extra:
  question_no: "008"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "스레드 풀은 생성 비용•대기열 절충 설계"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **스레드 풀(Thread Pool)**: 작업마다 스레드를 매번 생성·파괴하지 않고 일정 수의 워커 스레드를 미리 생성하여 큐 기반으로 작업을 재사용하는 자원 관리 기법.
- **작업 큐(Work Queue)**: 워커 스레드가 모두 사용 중일 때 유입된 태스크를 메모리에 대기시키는 유한 버퍼 큐(BlockingQueue).

</details>

- 정의/개념: 스레드 생성 및 소멸 오버헤드를 방지하고 자원 한도 내에서 작업을 재사용·스케줄링하는 **스레드 풀(Thread Pool)** 아키텍처
- 배경/필요성: 고빈도 요청 인입 시 무제한 스레드 생성에 따른 **메모리 고갈(OOM) 및 문맥 전환 지연 폭증 해결 불가**

#### 한줄 요약
- 워커 스레드를 사전 할당하고 유한 큐와 거절 정책을 통해 동시성 자원을 통제한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Core/Max Pool Size**: 상시 유지하는 기본 활성 워커 스레드 수(Core)와 피크 부하 시 동적 확장 가능한 최대 스레드 수(Max).
- **역압력(Backpressure)**: 작업 큐 포화 시 생산자(Producer)의 작업 인입 속도를 강제로 억제하여 시스템을 보호하는 흐름 제어 메커니즘.

</details>

- 스레드 사전 생성 및 재사용을 통한 **스레드 생성/소멸 오버헤드** 극소화
- **Core/Max Pool Size** 및 **유한 작업 큐(Bounded Queue)** 설정을 통한 메모리 자원 한도 통제
- 큐 포화 시 **포화 정책(RejectedExecutionHandler)** 을 통한 상위 계층 **역압력(Backpressure)** 전파

#### 한줄 요약
- 스레드 재사용으로 생성 비용을 없애고, 유한 큐와 역압력으로 메모리 고갈을 방지한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **워커 스레드(Worker Thread)**: 작업 큐에서 태스크를 인출하여 실행하고 완료 후 대기 상태로 복귀하는 실행 주체.
- **포화 거절 정책(RejectedExecutionHandler)**: 작업 큐와 최대 스레드가 모두 찼을 때 신규 유입 작업을 처리하는 정책(Abort, CallerRuns 등).

</details>

```text
[스레드 풀(Executor Framework) 아키텍처]
|-- 작업 제출자 (Client / Producer - execute/submit 호출)
|-- 스레드 풀 실행기 (ThreadPoolExecutor)
|   |-- 코어 워커 스레드 풀 (Core Threads)
|   |-- 유한 작업 큐 (Bounded Work Queue - BlockingQueue)
|   |-- 동적 확장 워커 풀 (Max Threads)
|   `-- 포화 거절 처리기 (RejectedExecutionHandler)
`-- 작업 완료 및 유휴 스레드 대기 (Keep-Alive Time 후 회수)
```

선의 의미: 계층 및 태스크 버퍼링/실행 파이프라인

| 구성요소 | 책임 |
|:---|:---|
| 스레드 풀 실행기 | 태스크 수용, 코어/최대 스레드 동적 관리, 유휴 스레드 회수 총괄 |
| 유한 작업 큐 | 코어 스레드가 포화 상태일 때 태스크를 안전하게 적재하는 **BlockingQueue** |
| 워커 스레드 | 큐에서 태스크를 지속적으로 인출(`take()`)하여 비즈니스 로직 실행 |
| 포화 거절 처리기 | 큐와 최대 스레드가 모두 찼을 때 **CallerRunsPolicy** 등 거절 정책 수행 |

#### 한줄 요약
- 실행기, 유한 작업 큐, 워커 스레드 풀, 포화 거절 처리기가 결합된 구조다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **CallerRunsPolicy**: 스레드 풀 포화 시 작업을 제출한 호출자 스레드가 직접 태스크를 실행하도록 유도하여 신규 유입을 늦추는 정책.

</details>

```text
신규 작업 제출 (execute/submit)
        │
   현재 활성 스레드 수 < Core Pool Size 인가?
   ┌────┴─────┐
  예           아니오
   │             │
신규 코어 워커    유한 작업 큐(Work Queue)에 여유 공간이 있는가?
스레드 즉시 생성   ┌────┴─────┐
후 작업 실행      예           아니오
   │             │             │
   │        작업 큐에 적재     현재 활성 스레드 수 < Max Pool Size 인가?
   │        후 워커 대기       ┌────┴─────┐
   │             │            예           아니오
   │             │             │             │
   │             │        신규 임시 워커   포화 거절 정책 실행
   │             │        생성 후 실행   (CallerRunsPolicy 등)
   └────┬────────┴─────────────┴─────────────┘
        │
   작업 완료 후 유휴 시간(Keep-Alive) 초과 시 임시 스레드 소멸
```

#### 한줄 요약
- 코어 스레드 확인 → 큐 적재 → 최대 스레드 확장 → 포화 거절 정책 발동 순으로 처리된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ForkJoinPool**: 대규모 작업을 재귀 분할(Fork)하고 유휴 스레드가 타 스레드의 큐에서 작업을 가져오는 작업 훔치기(Work-Stealing) 기반 풀.

</details>

| 스레드 풀 유형 | 고정 스레드 풀 (Fixed) | 캐시 스레드 풀 (Cached) | 포크-조인 풀 (ForkJoinPool) |
|:---|:---|:---|:---|
| 스레드 수 관리 | **고정된 Core=Max 수 유지** | 필요 시 무제한 생성 (60초 유휴 회수) | CPU 코어 수 비례 풀 유지 |
| 작업 큐 특성 | 유한/무한 LinkedBlockingQueue | 동기 큐 (SynchronousQueue) | 덱(Deque) 기반 **Work-Stealing** |
| 주 적용처 | 일반 웹 서버, 트랜잭션 처리 WAS | 짧고 독립적인 단기 비동기 작업 | CPU 집약 병렬 연산 (Parallel Stream) |
| 한계점 | 무한 큐 사용 시 메모리 OOM 위험 | 트래픽 폭증 시 스레드 폭증으로 다운 | 블로킹 I/O 작업 시 스레드 기아 발생 |

#### 한줄 요약
- 일반 백엔드는 FixedThreadPool, 단기 태스크는 Cached, 대규모 분할 정복은 ForkJoinPool을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Work-Stealing(작업 훔치기)**: 자신의 큐가 빈 워커 스레드가 다른 바쁜 워커의 큐 꼬리(Tail)에서 작업을 훔쳐와 실행하는 부하 분산 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 무제한 큐(Unbounded) 사용 시 메모리 누적으로 **OOM 발생** | ArrayBlockingQueue 등 **유한 작업 큐(Bounded Queue)** 크기 강제 | 큐 메모리 상한선 고정 및 서버 다운 원천 방지 |
| 포화 상태에서 AbortPolicy 사용 시 **요청 유실** | 거절 정책을 **CallerRunsPolicy** 로 전환 | 호출자 스레드 실행을 통한 유입 속도 자연 억제(**역압력**) |
| CPU 바운드 연산과 블로킹 I/O 작업 혼용으로 풀 고갈 | CPU 집약용 풀과 I/O 블로킹용 풀을 **물리적으로 분리** | I/O 지연으로 인한 CPU 연산 스레드 블로킹 차단 |
| 스레드 풀 적정 크기 산정 미흡 | $N_{\text{threads}} = N_{\text{cpu}} \times (1 + \text{Wait}/\text{Compute})$ 공식 적용 | CPU 이용률 90% 유지 및 문맥 전환 최소화 |

#### 한줄 요약
- 유한 큐 크기 제한, CallerRunsPolicy 역압력, CPU/IO 스레드 풀 분리로 시스템 가용성을 보장한다.

## Ⅶ. 결론

- 작업 성격별 **풀 분리**, 역압력 제어는 **유한 큐** 선택

#### 한줄 요약
- 스레드 풀은 적정 풀 크기 산정과 유한 큐 기반 역압력 제어를 통해 동시성 시스템의 자원 안정성을 완성한다.