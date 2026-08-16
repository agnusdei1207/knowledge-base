---
sidebar:
  order: 5
  label: "005. 멀티레벨 피드백 큐 MLFQ (Multilevel Feedback Queue)"
  badge:
    text: "기출 • 50%"
    variant: note
title: 멀티레벨 피드백 큐 MLFQ (Multilevel Feedback Queue)
date: "2026-08-13T12:52:00+09:00"
tags: [notes-software]
weight: 5
extra:
  question_no: "005"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "138회 기출, 피드백 큐•기아 방지 설계"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **MLFQ(Multilevel Feedback Queue)**: 사전에 작업 실행시간(CPU Burst)을 알 수 없는 환경에서, CPU 할당량 소진 이력을 바탕으로 프로세스의 큐(Queue) 우선순위를 강등/승격 제어하는 선점 스케줄링.
- **Priority Boost**: 하위 큐에 잔류하여 기아(Starvation) 상태에 빠진 프로세스들을 일정 주기($S$)마다 최상위 큐로 일괄 승격시키는 보정 메커니즘.
- **Gaming Defense**: 할당량 소진 직전 CPU를 반납해 강등을 피하는 행위를 누적 사용시간으로 방지하는 정책.

- **다단계 피드백 큐(Multilevel Feedback Queue, MLFQ)**: 서로 다른 우선순위와 타임 슬라이스를 가진 다중 큐를 구성하고 프로세스의 실행 이력에 따라 동적으로 우선순위를 조정하는 스케줄링 알고리즘.
- **우선순위 부스트(Priority Boost)**: 기아 현상(Starvation)을 방지하기 위해 일정 주기마다 모든 프로세스의 우선순위를 최상위 큐로 일괄 승격하는 메커니즘.
</details>

- 정의/개념: 프로세스의 실행 동작 이력(I/O-bound vs CPU-bound)에 따라 우선순위 레벨을 자율 피드백 조율하는 대표적 실무 스케줄링 정책인 **MLFQ(Multilevel Feedback Queue)**
- 배경/필요성: CPU 버스트를 모르면 **SJF 우선순위 사전 결정 불가**

#### 한줄 요약

- CPU 사용 이력으로 작업 우선순위 큐를 동적으로 조정한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Demotion (강등)**: 지정된 Time Quantum을 100% 모두 소진한 프로세스를 1단계 하위 큐로 떨어뜨리는 동작.
- **Interactive Job Prioritization**: CPU를 잠시 사용하고 바로 I/O 대기로 빠지는 응답형 프로세스를 상위 큐에 상주시키는 속성.

</details>

- 복수의 차등 타임 슬라이스 큐 계층(Q0 > Q1 > Q2) 형성
- 신규 프로세스의 최상위 큐(Q0) 인가 및 타임 슬라이스 소진 시 하위 큐로의 **Demotion(강등)**
- 주기적 **Priority Boost**로 기아 완화와 누적 사용량 기반 방어

#### 한줄 요약

- 버스트를 사전에 예측하지 않고 대화형•CPU 집중 작업을 분리한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Time Slice Scaling**: 상위 큐(Q0: 10ms)에서 하위 큐(Q1: 20ms, Q2: 40ms)로 내려갈수록 타임 슬라이스 크기를 2배씩 늘려 문맥 전환 오버헤드를 억제하는 기술.

</details>

```text
[우선순위 큐 계층]
          |
[우선순위 선택기]
          |
    [피드백 규칙] -- [상향 타이머]
```

선의 의미: 우선순위 큐 계층에서 선택기가 최고 큐의 프로세스를 디스패치하고, 피드백 규칙 및 상향 타이머가 프로세스의 강등/승격 위치를 제어하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 우선순위 큐 계층 | Q0(최고 우선순위, 짧은 Time Slice) ~ Qn(최저 우선순위, 긴 Time Slice) 큐 분격 |
| 우선순위 선택기 | 비어있지 않은 최상위 큐의 헤드 프로세스를 선택하여 CPU 코어 디스패치 |
| 피드백 규칙 | 타임 슬라이스 소진 시 **Demotion**, I/O 자진 포기 시 큐 유지 판단 |
| 상향 타이머 | 일정 주기($S$) 경과 시 **Priority Boost** 신호를 발생시켜 전 프로세스 Q0 일괄 이송 |

#### 한줄 요약

- 우선순위 큐 계층, 피드백 규칙, 상향 타이머의 피드백 구조이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Rules of MLFQ**: 
  1. Priority(A) > Priority(B) 이면 A 실행. 
  2. Priority(A) == Priority(B) 이면 RR 실행. 
  3. 신규 입입은 최상위 큐(Q0)에 배치. 
  4. 주어진 큐 몫의 타임 슬라이스를 소진하면 우선순위 1단계 강등. 
  5. 일정 시간 $S$ 후 전 프로세스 Q0로 승격.

</details>

```text
[신규 작업을 최상위 큐에 등록]
              │
              ▼
┌──────────── MLFQ 실행 반복 ────────────┐
│ 1. 최상위 비어 있지 않은 큐 선택       │
│              │                         │
│              ▼                         │
│ 2. 큐별 시간 할당량 실행               │
│              │                         │
│              ▼                         │
│ 3. CPU 사용 이력 판정                  │
│       ┌──────┴─────────┐               │
│       │ 조기 대기      │ 할당량 소진   │
│       ▼                ▼               │
│ [현재 큐 유지]   4. 하위 큐 강등       │
│       └────────┬───────┘               │
│                │ 상향 주기 도달        │
│                ▼                       │
│         5. 우선순위 상향               │
│                └── 큐 선택으로 반복    │
└────────────────────────────────────────┘
```

### 동작 원리

1. **최상위 비어 있지 않은 큐 선택**: 우선순위가 가장 높은 큐에서 작업 선택
2. **큐별 시간 할당량 실행**: 선택한 작업에 해당 큐의 할당량 부여
3. **CPU 사용 이력 판정**: 조기 반납과 할당량 소진 여부 판정
4. **하위 큐 강등**: 타임 슬라이스를 소진한 CPU-bound 프로세스를 하위 큐(Q1/Q2)로 **Demotion**.
5. **우선순위 상향**: 상향 주기 도달 시 작업을 상위 큐로 승격

#### 한줄 요약

- CPU 사용 이력 판정 뒤 할당량을 소진하면 하위 큐 강등, 최대 대기시간에 이르면 우선순위 상향을 수행한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **MLQ(Multilevel Queue)**: 프로세스를 성격에 따라 개별 큐에 정적 고정(No Movement)하여 큐 간 이동이 불가능한 방식.

</details>

| 비교 항목 | MLFQ (Multilevel Feedback Queue) | MLQ (Multilevel Queue) |
|:---|:---|:---|
| 큐 간 이동 유무 | 동적 이동 가능 (**Demotion & Priority Boost**) | 이동 불가 (정적 고정 큐 배치) |
| 프로세스 정보 요구 | 필요 없음 (실행 이력 기반 동적 학습) | 생성 시점에 프로세스 타입(System/Interactive/Batch) 지정 필수 |
| 유연성•기아 대응 | **Priority Boost**로 장기 대기 완화 | 하위 큐의 기아 위험 |

#### 한줄 요약

- 실행 이력이 변하면 MLFQ, 유형이 고정되면 MLQ가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Gaming the Scheduler**: 프로세스가 큐 강등을 피하기 위해 타임 슬라이스 종료 직전 고의로 무의미한 I/O를 발생시켜 상위 큐에 잔류하는 취약점 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 하위 큐 CPU 집중 작업의 **Starvation** | 일정 주기마다 **Priority Boost** 적용 | 최대 대기시간 제한 |
| 고의적 I/O 연산 인가에 의한 **Gaming the Scheduler** | 큐 진입 시 타임 슬라이스 리셋 금지 및 누적 CPU accounting 적용 | 스케줄러 꼼수 방지 |
| 짧은 할당량으로 잦은 **문맥 전환** | 하위 큐의 시간 할당량을 점진적으로 확대 | 계산 처리량 확보 |

> 사례: BSD 및 전통적 UNIX OS 커널 상의 **MLFQ 스케줄러** 튜닝 및 Priority Boost 파라미터 적용

#### 한줄 요약

- I/O 대기형 작업은 짧은 CPU 버스트로 상위 큐를 유지한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **MLFQ 파라미터 튜닝 기준(MLFQ Tuning Criteria)**: 큐 개수, 큐별 타임 슬라이스 크기, Priority Boost 주기($S$)에 근거한 설계 체계.

</details>

- 버스트를 모르는 혼합 작업은 **MLFQ**, 고정 작업군은 **MLQ** 선택

#### 한줄 요약

- 꼬리 응답시간과 최대 대기시간으로 할당량•상향 주기를 조정한다.
