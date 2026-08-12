---
sidebar:
  order: 8
  label: "008. 스레드 스케줄링•스레드 풀 (Thread Scheduling•Thread Pool)"
  badge:
    text: "미출 • 50%"
    variant: note
title: 스레드 스케줄링•스레드 풀 (Thread Scheduling•Thread Pool)
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **Thread Pool**: 미리 지정된 유한 개수의 워커 스레드(Worker Thread) 세트를 사전 생성하여 작업 큐(Work Queue)의 Task를 반복 할당/재사용하는 동시성 제어 패턴.
- **Task Queue (Work Queue)**: 제출된 작업(Runnable/Callable)이 워커 스레드에 의해 인출(Take)되기 전까지 대기하는 유한/무한 커널/인메모리 대기열.
- **RejectedExecutionHandler (포화 정책)**: 스레드 풀 및 작업 큐가 100% 포화(Full)되었을 때 신규 유입 작업을 거부(Abort), 호출자 직접 실행(Caller-Runs), 큐 무시(Discard) 등으로 제어하는 예외 정책.

</details>

- 정의/개념: 무분별한 스레드 생성/소멸 오버헤드를 막고 유한 자원 범위 내에서 작업을 병렬 스케줄링 재사용하는 **스레드 풀(Thread Pool)**
- 배경/필요성: 요청(Request)당 1개 스레드를 비동기 생성 시 발생하는 스택 메모리(Default 1MB) 고갈(OOM) 및 컨텍스트 스위칭 과부하 극복 요구성

#### 한줄 요약

- 유한 워커와 작업 큐를 재사용해 동시 실행 수를 제한한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Core Pool Size vs Maximum Pool Size**: 평시 상주하는 기본 워커 스레드 수(Core) 및 큐가 찼을 때 동적 확장 가능한 최대 워커 스레드 수(Max).
- **Backpressure (역압력)**: 스레드 풀 포화 시 **Caller-Runs-Policy** 등을 인가하여 작업 인가자(Producer)의 송신 속도를 강제로 둔화시키는 흐름 제어.

</details>

- 스레드 갱신 생성 및 소멸 파이프라인 수반 오버헤드 소멸
- **Core/Max Pool Size** 및 **Task Queue** 용량 기반 자원 캡슐화
- 과부하 시 **RejectedExecutionHandler**를 통한 상위 시스템 **Backpressure(역압력)** 전파

#### 한줄 요약

- 워커•큐 상한과 포화 정책으로 처리량•지연을 통제한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Worker Thread**: Loop 문을 구동하며 Task Queue로부터 `take()` 블로킹 작업을 래칭하여 계산을 연산하고 다시 풀로 복귀하는 작업 스레드.
- **Keep-Alive Time**: Core Pool Size를 초과하여 동적 생성된 초과 워커 스레드가 유휴(Idle) 상태로 생존 가능한 시간 한계.

</details>

```text
                [작업 제출자]
                      |
              [스레드 풀 실행기]
                 /           \
        [유한 작업 큐]   [워커 스레드]
                              |
                    [운영체제 스케줄러]
```

선의 의미: 작업 제출자가 스레드 풀 실행기로 Task를 제출하면, 유한 작업 큐 래칭 및 유휴 워커 스레드로 할당되어 OS 커널 스케줄러에 의해 CPU로 인가되는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 스레드 풀 실행기 (Executor) | 스레드 생성, 작업 디스패치 및 **Keep-Alive Time** 기반 유휴 스레드 회수 |
| 유한 작업 큐 (Work Queue) | ArrayBlockingQueue, LinkedBlockingQueue 기반 제출 작업 보관 |
| 워커 스레드 (Worker) | 큐 내 Runnable/Callable 작업 인출, 연산 수행 및 예외(Exception) 바운더리 포획 |
| 포화 정책 (Rejected Handler) | **AbortPolicy**, **CallerRunsPolicy**, **DiscardOldestPolicy** 등 예외 핸들링 |

#### 한줄 요약

- 스레드 풀 실행기가 작업 큐와 워커 스레드를 연결한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **CallerRunsPolicy**: 포화 상태 발생 시 작업을 제출한 호출자 스레드(e.g., HTTP Acceptor Thread)가 해당 Task를 직접 실행하게 하여 유입을 차단하는 역압력 제어.

</details>

```text
┌──────────────────────────────┐
│ 작업 제출                    │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 수용 조건 확인            │
└───────┬──────────────────────┘
        ├─ 취소·마감 초과 ───────▶ [취소 반환]
        │ 유효
        ▼
┌──────────────────────────────┐
│ 2. 유휴 워커 확인            │
└───────┬──────────────────────┘
        ├─ 있음 ─────────────────┐
        │ 없음                   │
        ▼                        │
┌──────────────────────────────┐│
│ 3. 큐 용량 확인              ││
└───────┬──────────────────────┘│
        ├─ 여유 ─▶ [큐 대기] ────┤
        │ 가득 참                │
        ▼                        │
┌──────────────────────────────┐│
│ 4. 포화 정책 적용            ││
│ 거절·대기·호출자 실행        ││
└──────────────┬───────────────┘│
               │                │
               ▼                ▼
        [과부하 반환]  ┌────────────────────┐
                       │ 5. 작업 실행       │
                       └─────────┬──────────┘
                                  ▼
                           [결과·오류 반환]
```

### 동작 원리

1. **수용 조건 확인**: 제출된 Task의 유효성 검증 및 실행기 수용.
2. **유휴 워커 확인**: 현재 동작 중인 스레드 수가 **Core Pool Size** 미만이면 즉시 워커 생성 후 실행.
3. **큐 용량 확인**: Core 수 충족 시 **Work Queue** 대기열에 Task 삽입.
4. **포화 정책 적용**: Work Queue가 가득 찼을 때 **Max Pool Size** 미만이면 동적 워커 생성, Max 초과 시 **RejectedExecutionHandler** 발동.
5. **작업 실행**: 유휴 워커 스레드가 Task를 인출하여 연산 완료 및 자원 반납.

#### 한줄 요약

- 수용 조건 확인, 큐 용량 확인, 포화 정책 적용으로 역압력을 건다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **ForkJoinPool**: Work-Stealing 알고리즘을 활용하여 큰 작업을 분할(Fork) 후 병렬 연산하고 합치는(Join) Java 전용 튜닝 스레드 풀.

</details>

| 스레드 풀 유형 | 특징 및 매커니즘 | 주요 용도 | 장단점 |
|:---|:---|:---|:---|
| **Fixed Thread Pool** | 고정된 스레드 수 유지, 무한/유한 Linked Queue | 일반적인 WAS, 백엔드 서버 | 메모리 한계 내 안정적 / 대기 지연 |
| **Cached Thread Pool** | 필요 시 스레드 무제한 확장 (60초 유휴 시 해제) | 단발성 초저지연 비동기 처리 | 고속 응답 / 과부하 시 OOM 위험 |
| **Scheduled Thread Pool** | 주기적 작업 실행 (Delay/Rate 스케줄링) | 주기적 배치, 헬스체크 | 시간 스케줄링 최적화 |
| **ForkJoinPool** | **Work-Stealing** (놀고 있는 워커가 타 큐 작업 훔침) | CPU-bound 병렬 딥러닝/알고리즘 | 최상급 CPU 가용률 / 순서 미보장 |

#### 한줄 요약

- 반복 작업•자원 상한은 스레드 풀 우선을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Work-Stealing**: ForkJoinPool 아키텍처 상에서 유휴 상태의 워커 스레드가 분주한 타 워커 스레드의 덱(Deque) 꼬리(Tail)에서 작업을 훔쳐와 병렬 처리하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 무한 Queue(Unbounded Queue) 적용으로 OOM 발생 | **ArrayBlockingQueue(유한 큐)** 한계 설정 | 메모리 고갈 원천 차단 |
| 풀 포화 시 유입 요청이 무시되어 트랜잭션 유실 | **CallerRunsPolicy** 포화 정책 적용 | 자연스러운 **Backpressure** 전파 |
| I/O 블로킹 작업과 CPU 계산 작업의 동시 믹싱 | CPU-bound 풀(Core 수 비례)과 I/O-bound 풀 분리 | CPU 바운드 스레드 유휴 예방 |

> 사례: Java **ThreadPoolExecutor** / Spring `@Async` 전용 유한 Thread Pool 산정 튜닝

#### 한줄 요약

- 허용 지연과 하위 자원을 기준으로 풀과 큐를 분리한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **스레드 풀 용량 산정 공식**: CPU-bound 작업: $N_{\text{threads}} = N_{\text{CPU}} + 1$, I/O-bound 작업: $N_{\text{threads}} = N_{\text{CPU}} \times (1 + \frac{W}{C})$.

</details>

- **스레드 풀 용량 산정 공식**에 따라 워크로드 속성(CPU vs I/O bound) 및 타깃 TPS를 분석하여 **Thread Pool** 용량 튜닝 적용

#### 한줄 요약

- 하위 연결 수•허용 지연에 따라 워커와 큐 상한을 설정한다.
