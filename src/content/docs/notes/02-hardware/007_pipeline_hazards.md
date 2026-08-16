---
sidebar:
  order: 7
  label: "007. 파이프라인 해저드: 데이터•제어•구조 (Pipeline Hazards)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "파이프라인 해저드: 데이터•제어•구조 (Pipeline Hazards)"
date: "2026-08-13T11:30:37+09:00"
tags:
  - "notes-hardware"
weight: 7
extra:
  question_no: "007"
  source_status: "기출"
  source_history: "122회, 135회"
  priority: 70
  priority_note: "반복 기출, 데이터•제어 대응 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **파이프라인 해저드(Pipeline Hazard)**: 명령어 파이프라인 상에서 선후 명령 간의 데이터 의존성, 조건 분기 또는 하드웨어 자원 충돌로 인해 다음 클록에 명령어를 멈춤 없이 계속 실행하지 못하는 구조적 충돌 조건.
- **스톨(Stall / Bubble)**: 해저드 충돌이 해결될 때까지 파이프라인의 특정 하위 단계를 멈추고 파이프라인 레지스터에 NOP(No Operation)를 투입하는 제어 기법.
- **포워딩(Forwarding / Bypassing)**: 연산 결과를 레지스터 파일에 최종 기록(WB)하기 전에 다음 클록의 연산기(ALU) 입력으로 우회 직접 전송하여 데이터 스톨을 방지하는 기술.
- **플러시(Flush)**: 분기 예측 오류 발생 시 이미 파이프라인 인출 단계에 잘못 적재된 기계어 명령어들을 제어 신호 무효화를 통해 제거하는 작업.

</details>

- 정의/개념: 파이프라인 처리 중 선후 명령어 간 피연산자 의존(Data), 분기 조건 미확정(Control), 하드웨어 자원 경합(Structural)으로 인해 파이프라인의 정상적인 연속 실행 흐름이 정지되는 **파이프라인 해저드**.
- 배경/필요성: 해저드 상황을 정밀하게 감지 및 제어하지 않으면 선행 명령어의 연산 결과가 갱신되기 전의 잘못된 피연산자를 후속 명령어가 읽거나, 잘못된 분기 명령을 수행하여 프로그램 실행의 정확성을 파괴함.

#### 한줄 요약
- 하드웨어 감지 회로를 구동하여 데이터, 제어, 구조 해저드를 감지하고 Forwarding, Stall, Flush 제어를 통해 완벽한 실행 연산 일관성을 유지함.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **명령어당 사이클 수(Cycles Per Instruction, CPI)**: 단일 기계어 명령어를 최종 완결하는 데 소비되는 평균 클록 주기 수 ($\text{CPI} = \text{Ideal CPI} + \text{Hazard Stalls}$).
- **버블(Bubble)**: 스톨이나 플러시 제어로 인해 유효한 명령어가 실행되지 못하고 비어 있는 파이프라인 슬롯.
- **명령 처리량(Instruction Throughput)**: 단위 시간당 완료되어 아키텍처 상태에 반영(Commit)되는 명령어의 총 개수.

</details>

- 발생 원인(Data, Control, Structure)에 따라 **포워딩**, **분기 예측**, **자원 복제** 등 기법을 차별 적용.
- 파이프라인 해저드로 인해 발생하는 **버블** 및 **플러시** 주기가 누적될수록 실제 프로세서의 **명령 처리량** 지연 초과.
- 이상적(Ideal) 환경의 $\text{CPI} = 1$ 대비, 해저드 발생 빈도와 스톨 주기에 비례하여 실제 **명령어당 사이클 수** 오버헤드가 누적 증가함.

#### 한줄 요약
- 해저드 미티게이션 제어를 통해 지연 스톨 주기를 은닉하고 실제 CPI 오버헤드를 이상치에 근접하도록 최소화함.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **해저드 감지기(Hazard Detection Unit)**: 파이프라인 레지스터의 원천 레지스터(Rs1, Rs2)와 선행 명령어의 목적 레지스터(Rd) 번호를 실시간 비교하여 충돌을 감지하는 제어 논리회로.
- **포워딩 경로(Forwarding Path / Bypass Multiplexer)**: EX/MEM 및 MEM/WB 파이프라인 레지스터의 연산 출력 데이터를 ID/EX 레지스터 입력으로 즉각 궤환시키는 우회 통로.
- **자원 중재기(Resource Arbiter)**: 동일 클록 주기에 단일 데이터 메모리 포트나 연산기를 동시 요구하는 제어 신호 간 우선순위를 할당하는 중재 회로.
- **분기 제어기(Branch Control Unit)**: EX 단계의 ALU Zero 플래그 조건과 예측 주소를 비교하여 실제 타깃 주소 분기 및 Flush 신호를 발생하는 장치.
- **파이프라인 레지스터(Pipeline Register)**: IF/ID, ID/EX, EX/MEM, MEM/WB 단계 사이에 매 클록 데이터를 격리 전달하는 래칭 장치.

</details>

```text
+-------------------------------------------------------------------------+
|                  Hazard Detection & Mitigation Unit                     |
|                                                                         |
|  [ Pipeline Register ] ──(Rs1, Rs2 vs Rd)──> [ Hazard Detection Unit ]  |
|         │                                             │                 |
|         ├─ (Data Dependency) ──> [ Forwarding Unit / Bypass MUX ]       |
|         ├─ (Control Branch)  ──> [ Branch Control / Flush Signal ]      |
|         └─ (Structural Conflict)──>[ Resource Arbiter / Stall Signal ]  |
+-------------------------------------------------------------------------+
```

| 구성요소 | 책임 |
|:---|:---|
| 해저드 감지기 | Rs•Rd 비교로 **RAW**•**Load-Use** 탐지 |
| 포워딩 경로 | 선행 결과를 **ALU 입력 MUX**로 우회 |
| 분기 제어기 | 예측 검증 후 **Flush•PC 복구** 제어 |
| 자원 중재기 | 공유 자원 충돌 시 **우선순위**•**Stall** 제어 |

#### 한줄 요약
- Hazard Detection Unit이 레지스터 번호 충돌을 감지하고 Forwarding MUX, Branch Controller, Resource Arbiter가 수습 조치를 실행함.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **원천 레지스터(Source Register, Rs)**: 현재 명령어 연산에 피연산자로 사용하기 위해 레지스터 파일에서 읽어오는 입력 레지스터.
- **목적 레지스터(Destination Register, Rd)**: 이전 명령어가 연산 결과를 최종 기록하기 위해 지정한 Output 레지스터.
- **완화 제어 신호(Mitigation Control Signal)**: 감지된 해저드 종류에 따라 Forwarding Select, PC Stall, Pipeline Flush를 개별 구동하는 제어 비트.

</details>

```text
[ 파이프라인 각 단계 명령어 정보 분석 (Rs1, Rs2 vs Rd) ]
                          │
                          ▼
                 [ 1. 해저드 탐지 ]
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
[ 데이터 해저드 (RAW) ] [ 제어 해저드 (Branch) ] [ 구조적 해저드 (Bus) ]
  ├─ Forwarding 지원:      ├─ 예측 성공:            ├─ 자원 분할 보유:
  │   ALU Bypass 연동     │   Stall 없이 진행       │   정상 동시 실행
  └─ Load-Use 의존:       └─ 예측 실패:            └─ 단일 자원 충돌:
      1-Cycle Stall 주입      IF/ID Flush + PC갱신     1-Cycle Stall 주입
                          │
                          ▼
             [ 2. 완화 방식 결정 ]
                          │
                          ▼
                [ 3. 상태 갱신 ]
```

### 동작 원리

1. **해저드 탐지**: **해저드 감지기**가 Rs•Rd와 메모리 접근 신호를 비교함.
2. **완화 방식 결정**:
   - 데이터 해저드: ALU 우회 연동이 가능하면 Forwarding MUX 신호를 켜고, Load-Use 의존 시 1클록 Stall 주입.
   - 제어 해저드: 분기 예측 성공 시 무정지, 미스 시 IF/ID 레지스터 Flush 및 올바른 PC 주소 전송.
   - 구조적 해저드: 하드웨어 자원 충돌 시 자원 중재기가 후속 명령 1클록 Stall 주입.
3. **상태 갱신**: 레지스터 래칭•NOP 주입 후 파이프라인 가동을 계속함.

#### 한줄 요약
- 레지스터 및 자원 충돌 탐지 후 데이터(Forwarding/Stall), 제어(Flush), 구조(Arbiter Stall)에 맞는 제어 신호를 생성하여 동작함.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **데이터 해저드(Data Hazard)**: 앞선 명령어의 결과 기록(WB)이 완결되지 않은 상태에서 다음 명령어가 해당 레지스터를 읽으려 할 때 발생(RAW, WAR, WAW).
- **제어 해저드(Control Hazard)**: 조건 분기 명령어(Branch) 실행 시 타깃 주소 결정 전 후속 명령어를 인출(Fetch)하여 발생하는 경로 불확정 문제.
- **구조적 해저드(Structural Hazard)**: 동일한 클록 주기에 두 개 이상의 파이프라인 단계가 단일 포트 메모리 등 물리 자원을 동시 점유하려 할 때 발생.
- **쓰기 후 읽기(Read After Write, RAW)**: 진성 의존성(True Data Dependency)으로 앞 명령의 쓰기 전 뒤 명령이 먼저 읽을 때 발생.
- **추측 인출(Speculative Fetch)**: 분기 조건 결과 확정 전 분기 예측기(Branch Predictor)를 기반으로 다음 명령어를 미리 인출하는 동작.
- **자원 복제(Resource Duplication)**: 단일 자원 경합을 해소하기 위해 I-Cache/D-Cache 분리, 레지스터 다중 포트화를 물리적으로 증설하는 설계.

</details>

| 비교 항목 | 데이터 해저드 (Data Hazard) | 제어 해저드 (Control Hazard) | 구조적 해저드 (Structural Hazard) |
|:---|:---|:---|:---|
| 발생 원인 | 선후 명령어 간 **RAW** (Read-After-Write) 데이터 의존성 | 조건 분기 결과 결정 전 **추측 인출** 수행 오예측 | 동일 클록 주기에 단일 하드웨어 자원 동시 접근 |
| 치명도 | 매우 빈번함 (연속적 연산 코드에서 다수 발생) | 분기 미스 시 깊은 파이프라인일수록 페널티 대폭 증가 | 메모리/버스가 잘 분리된 아키텍처에서는 드묾 |
| 주요 대책 | **포워딩**, 컴파일러 스케줄링, Stall | **분기 예측기**, BTB, Branch Target Early Compute | **자원 복제** (Harvard Architecture, Dual-Port Register) |

#### 한줄 요약
- RAW 의존성의 데이터 해저드, 분기 미스의 제어 해저드, 자원 점유의 구조적 해저드로 구분되며 포워딩, 예측기, 자원 복제로 대응함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **적재-사용 의존(Load-Use Dependency)**: Load 명령어 직후 해당 레지스터를 ALU 연산 피연산자로 바로 사용할 때 MEM 단계 완료 전에는 포워딩만으로 완벽 해소가 불가능하여 1클록 Stall이 필수적인 현상.
- **분기 대상 버퍼(Branch Target Buffer, BTB)**: 분기 명령어의 주소와 과거 타깃 jump 주소를 캐싱하여 Fetch 단계에서 즉시 다음 PC를 공급하는 하드웨어.
- **명령 스케줄링(Instruction Scheduling)**: 컴파일러 단계에서 Load-Use 관계인 두 명령어 사이에 의존성 없는 독립 명령어를 끼워 넣어 하드웨어 Stall을 은닉하는 기법.
- **분기 예측기(Branch Predictor)**: 2-bit Saturating Counter, TAGE 예측기 등을 활용하여 조건 분기의 Take/Not-Take 방향을 동적 추정하는 장치.
- **다중 포트(Multi-Port Register File)**: 2-Read Port / 1-Write Port 이상을 기본 탑재하여 동시 읽기/쓰기 접근에 따른 구조적 해저드를 배제하는 구성.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 연속 산술 연산 시 RAW 데이터 의존성으로 인한 대기 지연 | ALU 결과를 파이프라인 레지스터로 즉시 우회하는 **포워딩** 경로 구현 | 데이터 레지스터 쓰기 지연 완벽 은닉 및 CPI=1 유지 |
| **적재-사용 의존(Load-Use Dependency)** 발생 시 포워딩만으로 지연 해소 불가 | 1-Cycle **스톨** 주입 및 컴파일러 **명령 스케줄링** 연동 | Load-Use 지연 슬롯을 무해한 연산으로 채워 체감 지연 제거 |
| 조건 분기 시 타깃 주소 지연 및 미스로 인한 깊은 파이프라인 **플러시** 손실 | **분기 예측기**, **BTB** 및 ID 단계 **조기 판정** 회로 도입 | 예측 적중률 향상과 Flush 페널티 감소 |
| 통합 메모리 사용 시 IF 단계와 MEM 단계의 동시 접근에 따른 자원 충돌 | I-Cache / D-Cache 물리 분리(**자원 복제**) 및 **다중 포트** 레지스터 탑재 | 구조적 해저드 발생 가능성 원천 차단 |

#### 한줄 요약
- Forwarding Path, Compiler Scheduling, BTB 기반 Branch Predictor 및 Dual-Cache Resource Duplication을 통합 적용함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **면적•전력 비용(Area & Power Cost)**: 추가적인 하드웨어 우회 MUX, 예측기 테이블 및 다중 포트 증설 시 초래되는 미세 다이 면적 증가와 동적 전력 소모.
- **추가 CPI(CPI Overhead)**: 완화되지 못한 파이프라인 해저드 스톨 및 플러시로 인해 추가되는 명령어당 클록 수 오버헤드.
- **완화 회로 선택 기준(Hazard Mitigation Design Criteria)**: 대상 칩의 성능 목표(IPC)와 추가되는 물리적 하드웨어 오버헤드(면적, 전력) 간의 공학적 상충 관계를 종합 평가하는 기준.

</details>

- RAW 비중이 높으면 **포워딩**, 분기 손실이 크면 **예측기**, 자원 충돌이 크면 **복제** 적용.

#### 한줄 요약
- 추가 CPI와 면적•전력을 측정하여 해저드별 완화 회로를 선택함.
