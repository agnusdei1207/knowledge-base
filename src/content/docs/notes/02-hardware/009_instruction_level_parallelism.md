---
sidebar:
  order: 9
  label: "009. 명령어 수준 병렬성 ILP (Instruction-Level Parallelism)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "명령어 수준 병렬성 ILP (Instruction-Level Parallelism)"
date: "2026-08-13T17:50:00+09:00"
tags:
  - "notes-hardware"
weight: 9
extra:
  question_no: "009"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "병렬성 수준별 선택 기준을 묻는 핵심 주제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **명령어 수준 병렬성(Instruction-Level Parallelism, ILP)**: 단일 프로그램 실행 스레드 내에서 상호 데이터 의존성이 없는 독립적인 기계어 명령어들을 찾아 동일 클록 주기에 다중 파이프라인에서 동시 처리하는 프로세서 하드웨어 병렬 기법.
- **클록당 명령어 수(Instructions Per Cycle, IPC)**: 프로세서가 1클록 주기에 완결(Commit) 처리하는 평균 명령어 수 지표.
- **실행 유닛(Execution Unit, EU)**: 파이프라인 백엔드에서 정수 ALU, 부동소수점 FPU, 로드/스토어 AGU 등 독립적 연산을 동시 수행하는 물리적 하드웨어 연산 블록.

</details>

- 정의/개념: 단일 스레드 내에서 데이터 및 제어 의존성이 없는 기계어 명령어들을 탐지하여 동시 시점에 중첩 또는 복수 파이프라인에 발행 실행하는 **명령어 수준 병렬성**.
- 배경/필요성: 단순 순차 실행 구조에서는 선행 명령어의 데이터 지연으로 인해 후속 독립 명령어가 파이프라인에 진입하지 못하고 **실행 유닛**이 유휴 상태에 빠져 **IPC** 상승이 정체되는 한계를 극복하기 위해 제안됨.

#### 한줄 요약
- 단일 스레드의 상호 독립된 기계어 명령어를 다중 파이프라인 연산기에 동시 발행하여 단일 스레드 처리량(IPC)을 극대화하는 아키텍처 기술.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **슈퍼스칼라(Superscalar)**: 단일 클록 주기에 복수의 기계어 명령어를 동시 인출, 해독, 발행할 수 있도록 다중 데이터 경로를 파라메트릭 구축한 하드웨어 아키텍처.
- **비순서 실행(Out-of-Order Execution, OoO)**: 피연산자 연산 준비가 끝난 독립 명령어부터 원래 프로그램 서순과 다르게 먼저 계산(OoO)하되, 결과는 서순대로 저장(In-order Commit)하는 기술.
- **발행 폭(Issue Width)**: 프로세서가 1클록 주기에 실행 유닛으로 보낼 수 있는 최대 명령어 수.
- **발행 슬롯 활용률(Issue Slot Utilization)**: 하드웨어가 제공하는 파이프라인 발행 슬롯 대비 실제 유효 기계어가 할당되어 연산에 투입된 비율.
- **순차 커밋(In-Order Commit)**: 비순서(Out-of-Order)로 완료된 연산 결과들을 Reorder Buffer(ROB)를 통해 원래 프로그램 순서(Program Order)대로 레지스터 및 메모리에 반영하는 기법.

</details>

- 의존 사슬(Dependency Chain), 조건 분기 미스, 캐시 미스로 인한 메모리 지연이 **발행 슬롯 활용률**을 떨어뜨리는 지배적 요인.
- 다중 인출 디코더와 연산기를 탑재한 **슈퍼스칼라** 기법을 통해 **발행 폭** 확장.
- **비순서 실행**과 **순차 커밋**을 결합하여 정밀 예외와 프로그램 순서 상태를 유지.

#### 한줄 요약
- Superscalar 4/8-way Issue 구조와 Out-of-Order Engine을 활용하여 의존성 없는 독립 명령어를 동시 병렬 처리함.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **레지스터 리네이밍(Register Renaming)**: 소수의 아키텍처 레지스터(GPR)를 다수의 물리 레지스터(PRF)에 매핑하여 가짜 의존성(WAR, WAW)을 제거하는 기술.
- **명령어 윈도(Instruction Window / Issue Queue)**: 인출·해독된 기계어들이 적재되어 피연산자의 ALU 연산 준비 완료 여부를 실시간 추적 스케줄링하는 대기열.
- **재정렬 버퍼(Reorder Buffer, ROB)**: 비순서(OoO) 연산 결과를 임시 보관하여 원래 기계어 프로그램 순서대로 최종 Commit시키는 원형 큐 버퍼.
- **프런트엔드(Frontend)**: 분기 예측기, I-Cache, 명령어 디코더로 구성되어 파이프라인 윈도로 기계어 후보를 끊임없이 공급하는 장치.
- **읽기 후 쓰기 의존(Write After Read, WAR)**: 선행 명령어가 읽기 전 후행 명령어가 쓰기를 수행하려는 가짜 데이터 의존성(Anti-Dependency).
- **쓰기 후 쓰기 의존(Write After Write, WAW)**: 두 쓰기 명령어 간의 완료 순서 교란으로 최종 결과가 덮어씌워지는 가짜 데이터 의존성(Output Dependency).
- **정밀 복구(Precise Recovery)**: 예외나 분기 예측 오류 시 ROB의 순차 커밋 지점까지의 아키텍처 상태만 보존하고 이후 비순서 결과를 무효화하는 하드웨어 보장 기법.

- **물리 레지스터 파일(Physical Register File, PRF)**: 레지스터 리네이밍(Register Renaming)을 통해 WAW/WAR 가짜 의존성을 제거하고 다수의 명령어를 비순서(OoO) 병렬 실행할 수 있도록 지원하는 확장 레지스터 배열.
</details>

| 구성요소 | 책임 |
|:---|:---|
| 프런트엔드 | **분기 예측•다중 인출•해독** 수행 |
| 레지스터 리네이밍 | 물리 레지스터 매핑으로 **WAR**•**WAW** 제거 |
| 명령어 윈도 | 준비 명령의 **Wakeup**•**Select** 수행 |
| 실행 유닛 | ALU•FPU•AGU의 **병렬 연산** 수행 |
| 재정렬 버퍼 | 결과의 **순차 커밋•정밀 복구** 보장 |

#### 한줄 요약
- Register Renaming으로 가짜 의존성을 제거하고 Instruction Window와 ROB를 통해 Out-of-Order Execution 및 In-Order Commit을 달성함.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **종속 명령 깨우기(Wakeup & Select)**: ALU 연산이 완료되어 결과를 생성한 순간, 해당 연산 결과를 기다리던 이슈 큐 내부의 종속 명령어 활성화 비트를 켜는 스케줄링 제어 logic.
- **비순서 발행(Out-of-Order Issue)**: 프로그램의 정적 순서와 무관하게 연산 피연산자가 모두 준비된 명령어를 하드웨어 실행 유닛으로 즉각 즉시 내보내는 방식.

</details>

### 동작 원리

1. **인출**•**해독**: 발행 폭만큼 명령어 후보를 연속 공급
2. **레지스터 리네이밍**: 물리 레지스터로 WAR•WAW 제거
3. **깨우기**•**선택**: 피연산자가 준비된 명령어를 우선 선택
4. **비순서 실행**: 준비 순서에 따라 ALU•FPU•AGU에 발행
5. **순차 커밋**: ROB 선두부터 결과와 예외 상태를 반영

#### 한줄 요약
- 리네이밍 후 준비 명령을 먼저 실행하고 ROB에서 순차 확정.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **스레드 수준 병렬성(Thread-Level Parallelism, TLP)**: 멀티코어 환경에서 서로 독립적인 소프트웨어 스레드/프로세스를 동시 구동하는 병렬성.
- **데이터 수준 병렬성(Data-Level Parallelism, DLP)**: SIMD 및 Vector 연산기에서 단일 명령어로 대량의 데이터 배열 항목을 병렬 연산하는 기법.
- **동적 ILP(Dynamic ILP)**: 실행 중 하드웨어(OoO Engine, ROB)가 직접 명령어 간 병렬성을 추출하는 방식(x86, ARM Cortex-A).
- **정적 ILP(Static ILP)**: 컴파일러가 빌드 시점에 명령어 순서를 재배치하고 긴 묶음 기계어로 만드는 방식(VLIW).
- **매우 긴 명령어(Very Long Instruction Word, VLIW)**: 컴파일러가 독립 연산을 하나의 명령어 묶음으로 편성하는 정적 ILP 구조.

</details>

| 비교 항목 | 명령어 수준 병렬성 (ILP) | 스레드 수준 병렬성 (TLP) | 데이터 수준 병렬성 (DLP) |
|:---|:---|:---|:---|
| 병렬성 추출 주체 | 단일 스레드 내의 독립 기계어 연산 | 독립적인 소프트웨어 스레드/프로세스 | 동일 연산이 적용되는 벡터/배열 데이터 |
| 하드웨어 구현 | Superscalar, **OoO Engine**, ROB, PRF | 멀티코어, SMT (Simultaneous Multithreading) | SIMD (NEON, AVX), Vector Processor (SVE) |
| 주요 한계점 | RAW **임계 경로** 및 복잡한 하드웨어 | 스레드 동기화, Lock, 메모리 경합 | **분기 발산**, 비정열 주소 |

| 스케줄링 방식 | 동적 ILP (Dynamic ILP) | 정적 ILP (Static ILP - VLIW) |
|:---|:---|:---|
| 주요 하드웨어 | Out-of-Order Exec Engine, Instruction Window | 컴파일러 종속적 단순 In-Order 다중 연산기 |
| 바이너리 호환성 | 같은 ISA에서 **이진 호환성** 유지 용이 | 발행 폭 변경 시 **재컴파일** 필요 가능 |
| 하드웨어 복잡도 | 높은 다이 면적 및 탐색 동적 전력 소모 | 디코더 및 스케줄러 간소화로 하드웨어 전력 절감 |

#### 한줄 요약
- ILP는 단일 스레드 명령어 병렬화, TLP는 다중 스레드 병렬화, DLP는 SIMD 데이터 병렬화이며, ILP는 동적(OoO)과 정적(VLIW) 모델로 나뉨.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **쓰기 후 읽기 의존 사슬(RAW Dependency Chain)**: 연산 결과가 연속하여 다음 연산의 피연산자로 줄지어 사슬을 형성하여 ILP 추출을 저해하는 현상.
- **다중 누산기(Multiple Accumulators)**: 루프 내 연산 사슬을 2~4개의 독립 레지스터 변수로 분할 연산 후 최종 합산하여 RAW 의존 길이를 짧게 줄이는 루프 최적화 기법.
- **프런트엔드 병목(Frontend Bottleneck)**: I-Cache 미스나 디코더 대역폭 한계로 이슈 큐에 충분한 기계어 후보가 적재되지 못하는 현상.
- **물리 레지스터 리네이밍(Physical Register Renaming)**: PRF 레지스터 파일 개수를 늘려 WAR/WAW 의존성 제거율을 상승시키는 기술.
- **클록 게이팅(Clock Gating)**: OoO 탐색 회로 중 유휴 상태인 이슈 큐 블록의 클록 신호를 차단하여 동적 전력을 절감하는 기술.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 루프의 긴 **RAW 의존 사슬**로 실행 유닛이 유휴 상태 | **다중 누산기** 및 Loop Unrolling 적용 | RAW 사슬 단축 및 **실행 유닛 활용률** 향상 |
| 물리 레지스터 부족으로 리네이밍 정체 | **PRF** 용량과 RAT 체크포인트 조정 | 가짜 의존과 디스패치 정체 완화 |
| 8-way 이상 발행 폭 확장 시 이슈 큐 탐색 면적 및 동적 전력 폭증 | 이슈 큐 **클록 게이팅** 및 파이프라인 윈도 적정 크기 튜닝 | 전력 한도(TDP) 내 초고속 동작 주파수 보장 |
| 분기 오예측 및 캐시 미스의 **프런트엔드 병목** | $\mu\text{op}$ Cache와 분기 예측기 개선 | 명령어 공급 중단 빈도 감소 |

#### 한줄 요약
- Multiple Accumulators loop unrolling, PRF Expansion, Clock Gating 및 $\mu\text{op}$ Cache를 통해 ILP 추출의 한계 및 전력 오버헤드를 제어함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **임계 경로(Critical Path)**: 프로그램 코드 내에서 직렬로 연결된 가장 긴 RAW 데이터 의존 사슬로, 단일 스레드가 추출할 수 있는 이론적 최고 ILP 한계선.
- **병렬성 전환 기준(Parallelism Shift Criteria)**: ILP 확장이 RAW 임계 경로와 하드웨어 전력 한계에 도달했을 때 TLP(멀티스레드) 또는 DLP(SIMD/GPU)로 구조 전환을 결정하는 기준.

</details>

- 독립 명령이 충분하면 **ILP**, 의존•전력 한계에 닿으면 **TLP**•**DLP**로 전환.

#### 한줄 요약
- 임계 경로와 슬롯 활용률을 기준으로 ILP 확장 또는 TLP•DLP를 선택함.
