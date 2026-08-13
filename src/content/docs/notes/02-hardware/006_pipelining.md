---
sidebar:
  order: 6
  label: "006. 파이프라이닝 기본 구조 5단계 (Pipelining)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "파이프라이닝 기본 구조 5단계 (Pipelining)"
date: "2026-08-13T11:29:52+09:00"
tags:
  - "notes-hardware"
weight: 6
extra:
  question_no: "006"
  source_status: "기출"
  source_history: "122회"
  priority: 50
  priority_note: "처리량 향상과 단계 병목의 기본 구조"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **파이프라이닝(Pipelining)**: 하나의 명령어를 인출, 해독, 실행 등 복수의 독립적 단계로 분할하고, 서로 다른 명령어의 처리 단계를 동일 시점에 겹쳐 실행(Overlapping)하여 단위 시간당 명령어 처리량(IPC)을 높이는 하드웨어 병렬 기법.
- **비파이프라인 구조(Non-Pipelined Architecture)**: 한 명령어의 모든 실행 단계(Fetch~Write-back)가 최종 완결될 때까지 후속 명령어의 진입을 전면 대기시키는 순차 실행 아키텍처.
- **클록당 명령어 수(Instructions Per Cycle, IPC)**: 프로세서가 단일 클록 주기에 완료하여 출력하는 평균 기계어 명령어 수.
- **파이프라인 단계(Pipeline Stage)**: 명령어가 처리되는 세부 하드웨어 논리 분할 단위(RISC 5단계: IF, ID, EX, MEM, WB).

</details>

- 정의/개념: 명령어 처리 과정을 독립된 세부 단계로 세분화하고, 서로 다른 명령어의 처리 단계를 동시 시점에 중첩하여 병렬로 실행하는 **파이프라이닝(Pipelining)** 하드웨어 구조.
- 배경/필요성: 단일 **비파이프라인 구조(Non-Pipelined Architecture)**에서는 명령어 1개가 전체 회로를 다 통과할 때까지 타 하드웨어 블록이 유휴 상태(Idle)로 남게 되어, 클록 주기가 길어지고 CPU 자원 활용률 및 **IPC**가 급격히 저하되는 한계 발생.

#### 한줄 요약
- 명령어 실행 단계를 복수 단계로 중첩하여 단위 시간당 명령어 처리량(IPC)을 극대화하는 하드웨어 병렬 구조.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **처리량(Throughput)**: 단위 시간 동안 파이프라인 최종 단계를 빠져나와 완료(Commit)되는 기계어 명령어의 총량.
- **지연시간(Latency)**: 단일 명령어의 인출(Fetch) 시작 시점부터 결과가 레지스터에 기록(Write-back) 완료될 때까지 소요되는 총 시간.
- **최장 단계 지연(Longest Stage Delay)**: 파이프라인의 5개 단계 중 가장 조합 논리 지연 시간이 길어 시스템 전체 클록 주기를 제약하는 critical path.
- **단계 중첩(Stage Overlapping)**: 동일 클록 주기에 1단계는 IF, 2단계는 ID, 3단계는 EX 등 서로 다른 명령어가 각 단계를 시분할 점유하는 동작.

</details>

- **단계 중첩(Stage Overlapping)** 기법을 활용하여 정상 상태(Steady State) 진입 시 매 클록마다 1개의 명령어 처리를 완료하여 이상적인 IPC=1 달성.
- 파이프라인 전체 동작의 최소 클록 주기(Clock Cycle Time)는 5개 단계 중 조합 논리 지연이 가장 긴 **최장 단계 지연(Longest Stage Delay)**과 파이프라인 레지스터 딜레이의 합에 의해 한정됨.
- 각 명령어의 개별 **지연시간(Latency)**은 중간 파이프라인 레지스터 지연으로 인해 미세하게 증가하지만, 전체 **처리량(Throughput)**은 파이프라인 단계 수 $k$에 비례하여 향상됨.

#### 한줄 요약
- 개별 지연은 늘 수 있으나 단계 중첩으로 전체 처리량을 높임.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **명령어 인출(Instruction Fetch, IF)**: PC가 지시하는 메모리 주소에서 기계어를 읽어오고 PC를 다음 주소로 자동 증가시키는 1단계.
- **명령어 해독(Instruction Decode, ID)**: IR의 오퍼코드를 디코딩하고 지정된 범용 레지스터 파일에서 피연산자를 인출하는 2단계.
- **실행(Execute, EX)**: ALU를 구동하여 산술/논리 계산을 진행하거나 메모리 억세스용 실효 주소(Effective Address)를 계산하는 3단계.
- **메모리 접근(Memory Access, MEM)**: Load/Store 명령어 실행 시 데이터 메모리(D-Cache)에 직접 접근하여 읽기/쓰기를 수행하는 4단계.
- **결과 기록(Write Back, WB)**: ALU 연산 결과나 메모리 로드 값을 최종 목표 범용 레지스터에 기록 래칭하는 5단계.
- **파이프라인 레지스터(Pipeline Register)**: IF/ID, ID/EX, EX/MEM, MEM/WB 단계 사이에 위치하여 중간 결과와 제어 신호를 클록 엣지마다 동기 저장/전달하는 플립플롭 집합.

</details>

```text
[ Classic RISC 5-Stage Pipeline ]
  +------+    +------+    +------+    +------+    +------+
  |  IF  |===>|  ID  |===>|  EX  |===>| MEM  |===>|  WB  |
  +------+    +------+    +------+    +------+    +------+
     ||          ||          ||          ||          ||
  [IF/ID]     [ID/EX]     [EX/MEM]    [MEM/WB] (Pipeline Registers)
```

| 구성요소 | 책임 |
|:---|:---|
| IF | PC 기반 **명령어 인출•PC 갱신** |
| ID | 명령 해독과 **피연산자•제어 신호** 생성 |
| EX | **산술•논리 연산**과 분기 주소 계산 |
| MEM | Load•Store의 **데이터 캐시 접근** |
| WB | 연산•로드 결과의 **레지스터 기록** |
| 파이프라인 레지스터 | 단계 간 **데이터•제어 신호** 동기 전달 |

#### 한줄 요약
- IF->ID->EX->MEM->WB의 5단계 구조와 이들 사이를 격리하는 파이프라인 레지스터를 통해 파이프라인 동기화 제어를 수행함.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **데이터 경로(Data Path)**: 피연산자와 연산 결과가 IF, ID, EX, MEM, WB 레지스터와 연산기를 거쳐 흐르는 하드웨어 통로.
- **레지스터 파일(Register File)**: ID 단계에서 입력값을 읽어오고 WB 단계에서 최종 결과를 기록하는 멀티포트 저장 블록.
- **제어 신호(Control Signal)**: ID 단계에서 생성되어 파이프라인 레지스터를 타고 이동하며 ALU, D-Cache, MUX의 동작을 통제하는 비트열.

</details>

```text
Clock Cycle ──>   CC1   CC2   CC3   CC4   CC5   CC6   CC7
Instruction 1:    IF ──> ID ──> EX ──> MEM ──> WB
Instruction 2:           IF ──> ID ──> EX  ──> MEM ──> WB
Instruction 3:                  IF ──> ID  ──> EX  ──> MEM ──> WB
Instruction 4:                         IF  ──> ID  ──> EX  ──> MEM ──> WB
```

### 동작 원리

- **시동 단계(Fill Phase)**: 첫 네 주기에 명령어를 투입하여 단계를 채움.
- **정상 상태(Steady State)**: 전 단계 가동 후 매 클록 한 명령어를 완료함.
- **제어•데이터 이동**: 클록 엣지마다 **제어 신호**와 연산 데이터를 전달함.

#### 한줄 요약
- Fill Phase를 지나 Steady State에 도달하면 매 클록마다 1개의 명령어가 완료되는 시분할 중첩 파이프라이닝 흐름을 이룸.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **해저드(Hazard)**: 명령어 파이프라인 상에서 자원 경합, 데이터 의존성, 조건 분기로 인해 다음 클록에 명령어를 계속 실행하지 못하는 구조적 장애.
- **버블(Bubble / Stall)**: 해저드 발생 시 파이프라인 하위 단계에 아무런 연산도 수행하지 않는 NOP(No Operation) 신호를 주입하여 1클록 멈추게 하는 지연.
- **플러시(Flush)**: 조건 분기 예측 실패 시 이미 파이프라인에 잘못 인출된 하위 명령어들을 강제로 파기(Clear)하는 작업.
- **긴 주기(Long Cycle Time)**: 비파이프라인 아키텍처에서 인출부터 기록까지의 모든 조합 회로 delay를 합산하여 결정되는 길고 느린 클록 주기.

</details>

| 비교 항목 | 5단계 파이프라인 아키텍처 | 비파이프라인 (Single-Cycle) 아키텍처 |
|:---|:---|:---|
| **클록 주기 (Clock Period)** | **최장 단계 지연** + 레지스터 지연 (매우 짧음) | IF+ID+EX+MEM+WB 전 과정 합산 지연 (**긴 주기**) |
| **명령어 처리량 (IPC)** | 이상적 상태에서 **IPC = 1** 달성 가능 | 모든 명령어 처리에 **IPC = 1**이나 클록 주기가 매우 길어 성능 저하 |
| **회로 복잡도** | 파이프라인 레지스터, 포워딩, **해저드** 감지 로직 추가 | 파이프라인 레지스터 및 해저드 통제 제어 회로 미필요 |
| **장애 요소** | 의존성에 따른 **버블(Stall)** 및 분기 미스 시 **플러시(Flush)** 손실 | 파이프라인 해저드 및 Stall 현상이 원천적으로 발생하지 않음 |

#### 한줄 요약
- 비파이프라인의 긴 클록 주기 단점을 극복하여 높은 클록 주파수와 처리량을 제공하되 Hazard로 인한 Bubble/Flush 오버헤드를 수반함.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **포워딩(Forwarding / Bypassing)**: EX/MEM 단계를 지난 ALU 연산 결과를 WB 레지스터 저장을 기다리지 않고 다음 클록의 EX 단계 입력 MUX로 직통 연결하는 하드웨어 기술.
- **분기 예측(Branch Prediction)**: ID/EX 단계에서 조건 분기 결과가 확정되기 전에 BTB(Branch Target Buffer) 등을 통해 다음 Fetch 주소를 예측 구동하는 기술.
- **해저드 검출기(Hazard Detection Unit)**: 이전 명령어의 타깃 레지스터와 현재 명령어의 소스 레지스터 번호를 실시간 비치하여 파이프라인 Stall/Forwarding을 제어하는 논리 회로.
- **명령 스케줄링(Instruction Scheduling)**: 컴파일러가 코드 생성 시 데이터 의존성이 없는 순수 연산 명령어를 의존성 명령어 사이에 재배치하는 코드 최적화.
- **단계 분할(Stage Splitting)**: 조합 논리 지연이 너무 길어 병목을 유발하는 단계를 2개 이상의 미세 파이프라인 단계로 나누는 하이퍼파이프라이닝(Superpipelining) 기법.
- **단계 사용률(Stage Utilization)**: 파이프라인의 각 단계가 Stall이나 Bubble 없이 실제 유효한 명령을 실행하고 있는 비율.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 데이터 의존성에 의한 RAW(Read-After-Write) 데이터 해저드 발생 및 **버블** 주입 | **포워딩(Forwarding)** 경로 구성 및 컴파일러 **명령 스케줄링** 적용 | 데이터 연산 대기 버블 축소 및 연산 주파수 유지 |
| 조건 분기 명령어 실행 시 타깃 주소 미확정으로 인한 파이프라인 **플러시** 손실 | 2비트 분기 예측기, BTB 기반 **분기 예측** 및 ID 단계 **조기 판정** 회로 내장 | 분기 예측 미스 페널티 최소화 및 I-Cache 파이프라인 흐름 연속성 보장 |
| 특정 단계(예: MEM 단계)의 조합 논리 지연이 길어 전체 클록 주파수 저하 | Critical Path를 분할하는 **단계 분할(Superpipelining)** 및 **회로 재배치** | 최장 단계 지연 단축을 통한 CPU 동작 클록 주파수(GHz) 대폭 상승 |
| 파이프라인 깊이가 깊어짐에 따라 하드웨어 **단계 사용률** 저하 | **해저드 검출기**의 동적 제어 및 비순차 실행(Out-of-Order Execution) 엔진 연동 | 파이프라인 버블 최소화 및 단위 시간당 유효 명령 처리율 극대화 |

#### 한줄 요약
- Forwarding Unit, Branch Predictor, Superpipelining Stage Splitting 및 Instruction Rescheduling 기법을 통해 Pipeline Stall 및 Flush 오버헤드를 제어함.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **파이프라인 개선 기준(Pipeline Optimization Criteria)**: 실행 시간 공식 $\text{Execution Time} = \text{IC} \times \text{CPI} \times \text{Clock Cycle Time}$에 입각하여 파이프라인 깊이, 해저드 제어, 클록 주파수의 공학적 균형을 수립하는 평가 지표.

</details>

- 분기•의존 CPI가 높으면 **예측•포워딩**, 단계 지연이 크면 **단계 재분할** 적용.

#### 한줄 요약
- CPI 손실과 최장 단계 지연을 측정하여 해저드 제어와 깊이를 결정함.
