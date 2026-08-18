---
sidebar:
  order: 8
  label: "008. 스레드 스케줄링•스레드 풀"
  badge:
    text: "미출 • 50%"
    variant: note
title: "스레드 스케줄링•스레드 풀 (Thread Scheduling•Thread Pool)"
date: "2026-08-13T13:02:00+09:00"
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

- **Thread Pool(스레드 풀)**: 작업 요청마다 스레드를 매번 생성·소멸시키는 오버헤드를 방지하기 위해 일정 수의 워커 스레드를 미리 생성하여 큐 기반으로 작업을 재사용·스케줄링하는 자원 관리 패턴.
- **Work Queue(작업 큐)**: 가용 워커 스레드가 없을 때 유입된 작업(Runnable/Callable)을 메모리에 대기시키는 유한/무한 버퍼 큐(BlockingQueue).
- **RejectedExecutionHandler(포화 거절 정책)**: 작업 큐와 최대 스레드 풀이 모두 포화 상태에 도달했을 때 신규 유입 작업을 처리하는 정책(Abort, Discard, DiscardOldest, CallerRuns).

</details>

- 정의/개념: 무분별한 스레드 생성/소멸 오버헤드를 방지하고 시스템 자원 한도 내에서 작업을 효율적으로 스케줄링 및 재사용하는 **스레드 풀(Thread Pool)** 관리 아키텍처
- 배경/필요성: 고빈도 동시 요청 인입 시 스레드 무제한 생성에 따른 **메모리 고갈(OOM) 및 극심한 문맥 전환 오버헤드 방지** 필요

#### 한줄 요약

- 워커 스레드를 사전 할당하고 작업 큐와 포화 정책을 통해 동시성 처리량과 시스템 자원을 최적화하는 기제

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Core / Max Pool Size(코어/최대 스레드 수)**: 상시 유지하는 기본 활성 워커 스레드 수(Core)와 피크 부하 시 동적으로 확장 가능한 최대 워커 스레드 수(Max).
- **Backpressure(역압력)**: 작업 큐 포화 시 생산자(Producer)의 작업 제출 속도를 강제로 억제하여 시스템 과부하를 방어하는 흐름 제어 메커니즘.

</details>

- 스레드 사전 생성 및 재사용을 통한 **스레드 생성/소멸 오버헤드 극소화**
- **Core/Max Pool Size** 및 **유한 작업 큐(Bounded Queue)** 설정을 통한 메모리 자원 캡슐화
- 큐 포화 시 **포화 정책(RejectedExecutionHandler)** 을 통한 상위 계층 **역압력(Backpressure)** 전파 및 시스템 보호

#### 한줄 요약

- **스레드 재사용성 확보·유한 작업 큐 기반 자원 한도 통제·포화 정책 기반 역압력 방어**

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Worker Thread(워커 스레드)**: 작업 큐에서 태스크를 인출(`take()`)하여 실행하고 완료 후 대기 상태로 복귀하는 실행 주체.
- **Keep-Alive Time(유휴 유지 시간)**: 코어 스레드 수를 초과하여 생성된 임시 워커 스레드가 유휴(Idle) 상태로 유지될 수 있는 최대 대기 시간.

</details>

```text
[ 스레드 풀(Executor Framework) 아키텍처 ]
       [ 작업 제출자 (Client / Producer) ]
                       │ (execute / submit)
                       ▼
          [ 스레드 풀 실행기 (ExecutorService) ]
        (수용 검증, 워커 생성, 유휴 스레드 회수)
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
 [ 유한 작업 큐 (Work Queue) ]   [ 워커 스레드 풀 (Worker Threads) ]
 (BlockingQueue: 태스크 대기)    (Core Threads ~ Max Threads)
        │                             │
        └─────── (태스크 인출) ───────┘
```

선의 의미: 클라이언트가 제출한 태스크를 실행기가 작업 큐에 버퍼링하고, 유휴 워커 스레드가 이를 인출하여 병렬 실행하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 스레드 풀 실행기(Executor) | 태스크 수용, 코어/최대 스레드 동적 생성, 유휴 시간 초과 스레드 회수 관리 |
| 유한 작업 큐(Work Queue) | 워커 스레드가 모두 사용 중일 때 태스크를 안전하게 저장하는 BlockingQueue |
| 워커 스레드(Worker) | 작업 큐에서 태스크를 반복 인출하여 실행하고 예외를 격리 처리 |
| 포화 거절 처리기(Rejected Handler) | 큐와 최대 스레드가 모두 포화되었을 때 사전 정의된 거절 정책 수행 |

#### 한줄 요약

- **스레드 풀 실행기·유한 작업 큐(BlockingQueue)·워커 스레드 풀·포화 거절 처리기**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **CallerRunsPolicy(호출자 실행 정책)**: 스레드 풀 포화 시 작업을 제출한 호출자 스레드가 직접 태스크를 실행하도록 유도하여 신규 유입 속도를 늦추는 역압력 정책.

</details>

```text
[ 스레드 풀 태스크 수용 및 스케줄링 흐름 ]
 1. 신규 작업 제출 (execute/submit)
          │
          ▼
 2. 현재 활성 스레드 수 < Core Pool Size ?
      ├── [예] ──► 신규 코어 워커 스레드 즉시 생성 및 태스크 실행
      └── [아니오]
            │
            ▼
 3. 작업 큐(Work Queue)에 여유 공간 존재 ?
      ├── [예] ──► 작업 큐(BlockingQueue)에 태스크 삽입 후 대기
      └── [아니오]
            │
            ▼
 4. 현재 활성 스레드 수 < Max Pool Size ?
      ├── [예] ──► 신규 임시 워커 스레드 생성 및 태스크 실행
      └── [아니오]
            │
            ▼
 5. 포화 거절 정책(RejectedExecutionHandler) 실행
      (Abort / Discard / DiscardOldest / CallerRuns)
```

**동작 원리**

1. **코어 스레드 검사**: 현재 활성 스레드가 Core Pool Size 미만이면 신규 워커를 생성하여 즉시 실행
2. **작업 큐 대기**: 코어 스레드가 모두 동작 중이면 유한 작업 큐에 태스크를 적재하여 대기
3. **최대 스레드 확장**: 작업 큐가 포화 상태이고 활성 스레드가 Max Pool Size 미만이면 추가 임시 워커를 생성하여 처리
4. **포화 정책 발동**: 최대 스레드와 큐가 모두 포화되면 사전에 지정된 `RejectedExecutionHandler` 실행
5. **유휴 스레드 회수**: 임시 워커 스레드가 Keep-Alive Time 동안 유휴 상태를 유지하면 안전하게 소멸

#### 한줄 요약

- **코어 스레드 우선 할당 $\to$ 작업 큐 적재 $\to$ 최대 스레드 확장 $\to$ 포화 거절 정책 발동 $\to$ 유휴 스레드 회수**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ForkJoinPool**: 대규모 분할 정복(Divide-and-Conquer) 작업을 재귀적으로 분할(Fork)하고 병렬 실행 후 결과를 합산(Join)하는 고성능 작업 훔치기(Work-Stealing) 스레드 풀.

</details>

| 스레드 풀 유형 | 특징 및 메커니즘 | 주 적용 분야 | 장단점 |
|:---|:---|:---|:---|
| 고정 스레드 풀 (FixedThreadPool) | 고정된 수의 코어 스레드 유지, 작업 큐 기반 버퍼링 | 트래픽 예측이 가능한 일반 웹 서버/WAS | 자원 예측이 용이하나 무한 큐 설정 시 메모리 위험 |
| 캐시 스레드 풀 (CachedThreadPool) | 60초 유휴 시 회수, 필요 시 무제한 동적 스레드 생성 | 짧고 독립적인 단기 비동기 태스크 | 대기 지연이 없으나 급격한 부하 시 OOM 위험 |
| 스케줄 스레드 풀 (ScheduledThreadPool) | 지연(Delay) 및 주기적(Periodic) 실행 지원 | 백그라운드 주기 배치, 헬스 체크 | 정밀한 시간/주기 스케줄링에 특화 |
| 포크-조인 풀 (ForkJoinPool) | 작업 훔치기(Work-Stealing) 기반 서브태스크 분할 병렬 처리 | CPU 집약 대용량 계산, 병렬 스트림(Parallel Stream) | CPU 코어 활용률이 극대화되나 블로킹 I/O 시 효율 저하 |

#### 한줄 요약

- 일반 백엔드는 **FixedThreadPool**, 단기 작업은 **Cached**, 주기 작업은 **Scheduled**, 대규모 연산은 **ForkJoinPool** 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Work-Stealing(작업 훔치기)**: 유휴 상태의 워커 스레드가 작업이 과도하게 쌓인 다른 워커의 큐 꼬리(Tail)에서 작업을 가져와 실행하는 부하 분산 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 무제한 큐(Unbounded Queue) 사용 시 메모리 누적으로 인한 **OOM(Out of Memory) 발생** | ArrayBlockingQueue 등 **유한 작업 큐(Bounded Queue)** 크기 명시 설정 | 메모리 상한선 강제 및 시스템 다운 방지 |
| 포화 상태에서 기본 AbortPolicy 사용 시 **핵심 비즈니스 요청 유실** | 거절 정책을 **CallerRunsPolicy** 로 전환하여 호출자 스레드가 직접 실행 | 유입 속도 자연 억제(Backpressure) 및 요청 무유실 보장 |
| CPU 바운드 연산과 블로킹 I/O 작업을 단일 풀에서 공유하여 **스레드 고갈 발생** | CPU 집약용 풀(코어 수 비례)과 I/O 블로킹용 풀을 **물리적으로 분리** | I/O 지연으로 인한 CPU 연산 스레드 점유 차단 |

#### 한줄 요약

- **유한 작업 큐(Bounded Queue) 크기 제한·CallerRunsPolicy 역압력 전파·CPU/IO 스레드 풀 분리 격리**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Thread Pool Sizing Formula(스레드 풀 적정 크기 산정)**: CPU 집약 작업은 $N_{\text{threads}} = N_{\text{cpu}} + 1$, I/O 집약 작업은 $N_{\text{threads}} = N_{\text{cpu}} \times (1 + W/C)$로 산정하는 사이징 기준.

</details>

- 고성능 백엔드 아키텍처 설계 시 **워크로드 특성에 따른 CPU/IO 스레드 풀 분리 및 Bounded Queue 기반 CallerRunsPolicy 채택** 필수

#### 한줄 요약

- **적정 풀 사이징과 유한 큐 기반 역압력 제어**를 통한 동시성 시스템의 자원 안정성 및 처리량 극대화

