---
sidebar:
  order: 8
  label: "008. 파이프라인 포워딩•분기 예측 (Pipeline Forwarding Branch Prediction)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "파이프라인 포워딩•분기 예측 (Pipeline Forwarding Branch Prediction)"
date: "2026-08-08T12:19:00+09:00"
tags:
  - "notes-hardware"
weight: 8
extra:
  question_no: "008"
  source_status: "기출"
  source_history: "122회"
  priority: 50
  priority_note: "포워딩•분기 예측 처리량 분석"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **포워딩(Forwarding / Bypassing)**: 선행 명령어의 연산 결과가 파이프라인 레지스터(EX/MEM, MEM/WB)에 들어오는 즉시 후속 명령어의 ALU 연산 입력으로 직접 직통 전달하여 레지스터 파일 쓰기 대기 사이클을 제거하는 하드웨어 완화 기법.
- **분기 예측(Branch Prediction)**: 조건 분기 명령어(Branch)의 실행 결과와 타깃 주소가 EX 단계에서 확정되기 전에 과거 이력을 바탕으로 분기 방향(Taken/Not-Taken)을 사전에 추정하여 Fetch 연속성을 유지하는 기술.
- **버블(Bubble / Stall)**: 파이프라인 상의 데이터 및 제어 의존성으로 인해 유효한 명령어가 실행되지 못하고 유휴 상태로 대기하는 빈 파이프라인 클록 주기.
- **명령어당 사이클 수(Cycles Per Instruction, CPI)**: 단일 기계어 명령어를 최종 실행 완결(Commit)하는 데 들어가는 평균 클록 주기 수.

</details>

- 정의/개념: 레지스터 최종 저장을 기다리지 않고 연산 결과를 직접 우회 전송하는 **포워딩(Forwarding)**과 분기 타깃 확정 전 인출 경로를 사전 예측하는 **분기 예측(Branch Prediction)**을 결합한 파이프라인 연산 성능 최적화 기법.
- 배경/필요성: RAW 데이터 의존성 및 조건 분기 미확정으로 발생하는 **버블(Bubble)**이 깊은 파이프라인 구조에서 동시다발적으로 누적되면 **CPI**가 급상승하고 CPU 연산 처리 속도가 급격히 저하되므로 이를 차단할 기술 필요성 증대.

#### 한줄 요약
- Forwarding을 통해 데이터 대기를 제거하고 Branch Prediction을 통해 제어 대기를 차단하여 실제 CPI를 이상치(Ideal CPI=1)에 수렴시키는 파이프라인 최적화 체계.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **분기 오예측(Branch Misprediction)**: 동적 예측기가 추정한 분기 방향 및 타깃 주소가 실제 EX 단계에서의 연산 결과와 상충하여 잘못된 기계어가 파이프라인에 인출된 상태.
- **플러시 패널티(Flush Penalty)**: 분기 오예측을 감지했을 때 오경로 기계어들을 무효화(Flush)하고 올바른 PC 주소로부터 명령어를 다시 가져오는 동안 발생하는 사이클 지연 손실.

</details>

- **포워딩(Forwarding)**을 통해 레지스터 파일 래칭(WB)을 건너뛰고 EX/MEM, MEM/WB 라인의 계산된 값을 후속 연산기의 입력으로 직통 공급.
- **분기 예측(Branch Prediction)**을 내장하여 분기 판단 주기가 오기 전에 타깃 주소를 추정하여 I-Cache 인출 끊김 방지.
- 파이프라인 깊이(Pipeline Depth)가 늘어날수록 **분기 오예측(Branch Misprediction)** 시 수반되는 **플러시 패널티(Flush Penalty)** 주기가 비례하여 커지는 딜레마 상충.
- 두 기법의 조합을 통해 파이프라인 내 자원 유휴 상태인 버블 발생 빈도를 대폭 감소시킴.

#### 한줄 요약
- 포워딩의 데이터 래칭 우회와 분기 예측의 인출 사전 구동 특성을 결합하여 CPI 저하 오버헤드를 제어함.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **포워딩 장치(Forwarding Unit)**: ID/EX, EX/MEM, MEM/WB 파이프라인 레지스터의 레지스터 번호 비트를 실시간 대조하여 우회 제어 신호를 생성하는 비교 로직.
- **우회 선택기(Bypass Multiplexer)**: 범용 레지스터 파일 출력값, EX/MEM 포워딩값, MEM/WB 포워딩값 중 하나를 ALU 피연산자로 선택 입력하는 MUX.
- **복구 로직(Recovery Logic / Reorder Buffer)**: 분기 예측 오류 판정 시 잘못 들어온 파이프라인 명령어들을 Flush 처리하고 아키텍처 PC 주소를 복원하는 회로.
- **분기 예측기(Branch Predictor)**: BHT(Branch History Table), 2-bit Saturating Counter, TAGE 등을 이용하여 분기 방향을 결정하는 예측기.
- **인출 제어기(Fetch Controller)**: 예측된 target PC 주소 또는 복구 주소를 선택하여 I-Cache로 공급하는 제어 모듈.
- **프로그램 카운터(Program Counter, PC)**: 다음 주기의 기계어 인출 주소를 보유하는 레지스터.

</details>

```text
[ Data & Control Path Optimization Logic ]
 ├─ Data Hazard Path  : Pipeline Regs ──> [ Forwarding Unit ] ──> [ Bypass MUX ] ──> ALU
 └─ Control Hazard Path: Branch Ins.   ──> [ Branch Predictor ]──> [ Fetch Controller ] ──> PC
                                                │ (Mispredict)
                                                └─> [ Recovery Logic ] ──> Flush & Restore
```

| 구성요소 | 역할 및 작동 원리 | 차별점 및 실무 유용성 |
|:---|:---|:---|
| **포워딩 장치** | 선행 명령의 Rd와 후속 명령의 Rs1, Rs2 레지스터 번호 실시간 비교 | RAW 해저드 발생 시 레지스터 대기 없는 즉시 우회 제어 신호 출력 |
| **우회 선택기** | Forwarding Unit의 신호에 따라 ALU 입력선 데이터 3-way MUX 선택 | 연산기 입력 지연을 1주기 이내로 최소화 |
| **분기 예측기** | BHT 및 2-bit Counter 기반으로 Taken/Not-Taken 동적 예측 | 분기 명령 해독 전에도 다음 명령어 Fetch 라인 가동 유지 |
| **인출 제어기 & 복구 로직**| 오예측 판정 시 파이프라인 NOP 처리(Flush) 및 올바른 PC 복원 | 추측 실행(Speculative Execution)의 결점 수습 및 정밀 예외 보장 |

#### 한줄 요약
- Forwarding Unit & Bypass MUX가 데이터 우회를 제어하고 Branch Predictor & Recovery Logic이 제어 추측 및 오류 플러시를 관장함.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **분기 이력(Branch History Table, BHT)**: 과거 조건 분기의 실행 결과(Taken/Not-Taken)를 2비트 포화 카운터 등에 기록해 두는 표.
- **분기 대상 버퍼(Branch Target Buffer, BTB)**: 분기 기계어의 주소와 과거 점프했던 타깃 주소를 매핑 보관하는 고속 캐시.
- **플러시(Flush)**: 잘못 예측된 파이프라인 단계의 명령어 비트들을 0(NOP)으로 소거하는 무효화 연산.
- **쓰기 후 읽기 데이터 해저드(Read After Write, RAW)**: 앞 명령어가 쓰기 전 뒤 명령어가 읽으려 하여 최신 피연산자를 얻지 못하는 의존성.
- **적재-사용 스톨(Load-Use Stall)**: Load 명령어 결과가 MEM 단계를 거쳐 나오므로 EX 단계 우회가 불가능하여 1클록 강제 정지되는 현상.

</details>

```text
[ 명령어 인출 및 해독 (IF / ID) ]
             │
             ▼
   [ 1. 해저드 감지 유닛 판정 ]
   ├─ RAW Data Hazard ──> [ 2. 결과 우회 가능 여부 ]
   │                       ├─ ALU 연산 결과 : [ Forwarding Bypass 연동 ] (Stall 없음)
   │                       └─ Load-Use 의존 : [ 1-Cycle Stall 주입 ] -> 후속 주기에 Forwarding
   │
   └─ Control Hazard ───> [ 3. BTB / Branch Predictor 동적 예측 ]
                           ├─ 예측 성공 : [ Continuous Pipeline Fetch ]
                           └─ 오예측 발생 : [ EX단계 감지 -> Flush -> PC 복원 & BTB 갱신 ]
```

### 동작 원리

1. **해저드 감지**: 명령어 실행 중 RAW 데이터 의존 혹은 조건 분기 명령어가 디코딩되면 완화 기법 발동.
2. **포워딩 실행**: 이전 명령어의 연산 결과가 EX/MEM 레지스터에 존재 시 **우회 선택기**를 구동하여 ALU에 전달하되, **적재-사용 스톨(Load-Use Stall)** 관계일 경우 1클록 Stall 후 MEM/WB 라인에서 포워딩함.
3. **분기 예측 및 검증**: **BHT/BTB** 정보를 참조하여 Fetch Controller가 예측 주소로 명령어를 끊김 없이 인출하고, EX 단계에서 최종 계산된 분기 조건과 다를 경우 파이프라인 **플러시(Flush)** 및 올바른 주소 재인출 수행.

#### 한줄 요약
- RAW 의존 시 Forwarding/Stall 경로를 태우고 조건 분기 시 Predictor/BTB 기반 추측 인출 및 Flush 복구를 구동함.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **적재-사용 의존(Load-Use Dependency)**: Load 명령어 데이터가 D-Cache 메모리 접근(MEM) 후에 완성되므로 EX 단계 포워딩이 불가능해 발생하는 1사이클 구조적 지연.
- **분기 이력 기반 선인출(History-Based Prefetch)**: past execution pattern을 관찰하여 2-bit counter 또는 TAGE 알고리즘 기반으로 예측 인출을 실행하는 방식.
- **파이프라인 플러시(Pipeline Flush)**: 예측 실패 판명 시 이미 들어온 후속 기계어를 래치에서 무효화(Clear)하는 조치.

</details>

| 기법 구분 | 포워딩 메커니즘 (Forwarding) | 분기 예측 메커니즘 (Branch Prediction) |
|:---|:---|:---|
| **대상 해저드** | **RAW 데이터 해저드** 완화 | **제어 해저드 (Control Hazard)** 완화 |
| **작동 원리** | 레지스터 래칭 전 연산 결과를 ALU 입력선으로 우회 | 과거 실행 **분기 이력** 기반 타깃 주소 사전 인출 |
| **극복 한계** | **적재-사용 의존**의 1클록 스톨은 우회 불가 | 예측 실패 시 깊은 **파이프라인 플러시** 오버헤드 |
| **주요 요소** | Forwarding Unit, Bypass MUX | BHT, BTB, 2-bit Counter, Recovery Logic |

#### 한줄 요약
- Forwarding은 데이터 의존 지연을 ALU direct 우회로 해결하고 Branch Prediction은 제어 불확정성을 역사적 예측 및 Flush로 해결함.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **커밋(Commit / Retire)**: 파이프라인 백엔드에서 추측 실행된 결과를 최종 확인하여 아키텍처 레지스터와 메모리에 영구 반영하는 단계.
- **정밀 예외(Precise Exception)**: 예측 실패나 예외 발생 시 예외 직전 명령어까지만 정확히 Commit 상태를 남기고 이후 추측 명령어의 흔적을 완벽히 제거하는 성질.
- **명령어 재배치(Instruction Reordering)**: 컴파일러가 Load-Use 관계 사이에 상관없는 독립 연산 명령어를 끼워 넣어 하드웨어 Stall 주기를 은닉하는 기법.
- **플러시 복구(Flush Recovery)**: 잘못 인출된 파이프라인 슬롯들을 NOP으로 바꾸고 ROB(Reorder Buffer) 및 PC를 이전 정상 상태로 복원하는 과정.
- **하드웨어 오버헤드 분석(Hardware Overhead Analysis)**: MUX 회로 및 BTB 예측 테이블 증설로 인한 미세 다이 면적과 동적 전력 소모(Power Consumption)의 실측 평가.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| Load 명령어 직후 연산 수행으로 **적재-사용 스톨** 발생 | 컴파일러 **명령어 재배치(Instruction Reordering)** 및 1-Cycle Stall 감지 통제 | 메모리 접근 대기 시간 완벽 은닉 |
| 루프 및 중첩 조건문에서 **분기 오예측** 빈발로 오경로 인출 누적 | TAGE(Tagged Geometric) 예측기, 2-bit BHT 및 **BTB** 용량 확장 | 예측 정확도 95% 이상으로 대폭 향상 및 플러시 차단 |
| 추측 실행된 잘못된 인출 명령어가 메모리에 직접 쓰여 아키텍처 훼손 | Reorder Buffer(ROB) 기반 **커밋(Commit)** 단계와 **정밀 예외** 구조 적용 | 잘못된 오경로 결과의 메모리 오염 원천 방지 |
| 포워딩 MUX 및 예측기 회로 과다 증설로 칩 발열 및 전력 폭증 | Static Timing Analysis(STA) 기반 **하드웨어 오버헤드 분석** 및 MUX 경로 최적화 | 전력 한도 지키면서 최고 파이프라인 frequency 확보 |

#### 한줄 요약
- Instruction Reordering, TAGE/BTB Predictor, ROB Commit precise exception 및 Timing Overhead Analysis 체계를 통합 적용함.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **오예측 페널티(Misprediction Penalty)**: 오예측 시 파이프라인에 주입된 NOP 버블과 재인출에 소비되는 지연 사이클 수.
- **해저드 제어 기준(Hazard Control Selection Criteria)**: 파이프라인 깊이, 예측기 정확도, MUX 딜레이 및 전력 소비를 종합하여 최적의 포워딩/예측 회로 규모를 결정하는 하드웨어 평가 프레임워크.

</details>

- **해저드 제어 기준(Hazard Control Selection Criteria)**을 기반으로 데이터 해저드는 최우선 하드웨어 포워딩 경로 및 컴파일러 스케줄러로 차단하고, 제어 해저드는 BTB/TAGE 동적 예측기 및 ROB 기반 정밀 예외 플러시 복구 체계를 구축하여 파이프라인의 이상적 CPI=1 달성 체계 적용 필수.

#### 한줄 요약
- Hardware Forwarding Bypass 및 TAGE/BTB Branch Predictor와 ROB Flush Recovery 구조를 결합하여 CPI 지연을 극소화하는 파이프라인 통합 최적화 체계 적용.
