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

- **포워딩(Forwarding, Bypassing)**: 연산 결과를 레지스터에 쓰기 전 후속 명령어의 입력으로 직접 전달하여 데이터 대기 사이클(Stall)을 제거하는 기법.
- **분기 예측(Branch Prediction)**: 조건 분기의 실행 결과가 확정되기 전 과거 이력을 기반으로 방향과 타깃 주소를 사전에 추정하는 기술.
- **파이프라인 스톨(Pipeline Stall, Bubble)**: 의존성으로 인해 명령어를 진행하지 못하고 유휴 상태로 대기하는 클록 주기.
- **명령어당 사이클 수(Cycles Per Instruction, CPI)**: 명령어 1개를 실행 완료하는 데 소요되는 평균 클록 주기.

</details>

- 정의/개념: RAW 데이터 의존성과 조건 분기 지연을 해결하기 위해 연산 결과 우회 전송(**Forwarding**) 및 인출 경로 사전 추정(**Branch Prediction**)을 결합한 파이프라인 최적화 기법.
- 배경/필요성: 파이프라인이 심화됨에 따라 데이터/제어 해저드로 인한 버블 발생이 증가하여 CPI가 상승하는 문제 해결.

#### 한줄 요약

- 포워딩과 분기 예측을 통해 파이프라인 대기를 최소화하고 이상적 CPI(1.0)에 수렴하도록 제어하는 최적화 구조.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **분기 오예측(Branch Misprediction)**: 예측된 분기 방향이 실제 계산 결과와 일치하지 않는 상태.
- **플러시 패널티(Flush Penalty)**: 오예측 시 오경로 명령어를 무효화하고 올바른 주소에서 재인출할 때 발생하는 사이클 손실.

</details>

- **포워딩(Forwarding)**: EX/MEM, MEM/WB 레지스터의 결과를 후속 명령어의 ALU 입력으로 즉시 바이패스.
- **분기 예측(Branch Prediction)**: ID 단계에서 분기 타깃을 추정하여 I-Cache 인출 끊김 방지.
- **플러시 패널티(Flush Penalty)**: 깊은 파이프라인일수록 오예측 시 버블 손실 증가.

#### 한줄 요약

- 데이터 우회와 분기 타깃 사전 추정으로 파이프라인 버블을 최소화하는 하드웨어 제어 기법.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **포워딩 제어기(Forwarding Unit)**: 파이프라인 레지스터의 목적지 레지스터 번호와 후속 명령어의 소스 레지스터 번호를 비교하는 회로.
- **우회 MUX(Bypass Multiplexer)**: 레지스터 파일 출력과 포워딩 경로 중 유효 피연산자를 선택하는 다중화기.
- **분기 예측기(Branch Predictor)**: BHT, BTB 기반으로 분기 방향 및 타깃 주소를 예측하는 모듈.
- **복구 로직(Recovery Logic)**: 오예측 시 파이프라인을 무효화(Flush)하고 PC를 복원하는 제어 회로.

</details>

```text
[ 데이터 및 제어 경로 최적화 구조 ]
 ├─ 데이터 해저드 : 파이프라인 레지스터 ──> [ 포워딩 제어기 ] ──> [ 우회 MUX ] ──> ALU
 └─ 제어 해저드   : 조건 분기 명령어   ──> [ 분기 예측기 ]   ──> [ 인출 제어기 ] ──> PC
                                                 │ (오예측)
                                                 └─> [ 복구 로직 ] ──> 플러시 및 복원
```

| 구성요소 | 역할 및 작동 원리 | 실무적 유용성 |
|:---|:---|:---|
| **포워딩 제어기** | Rd와 Rs 번호를 비교하여 바이패스 제어 신호 생성 | 레지스터 쓰기 대기 없이 연산 결과 즉시 전달 |
| **우회 MUX** | 레지스터값과 포워딩 데이터 중 ALU 입력 선택 | 1클록 내 피연산자 공급 |
| **분기 예측기** | BHT/BTB 기반으로 분기 방향 및 타깃 주소 추정 | 해독 전 연속적인 Fetch 유지 |
| **복구 로직** | 오예측 시 파이프라인 Flush 및 올바른 PC 복구 | 추측 실행 오류 보정 및 정밀 예외 보장 |

#### 한줄 요약

- 포워딩 제어기와 MUX로 데이터 해저드를 해소하고, 분기 예측기와 복구 로직으로 제어 해저드를 제어하는 구조.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **분기 이력 표(Branch History Table, BHT)**: 분기 성공/실패 이력을 저장하는 2비트 카운터 기반 테이블.
- **분기 타깃 버퍼(Branch Target Buffer, BTB)**: 분기 명령어 주소와 타깃 주소를 매핑 보관하는 캐시.
- **적재-사용 스톨(Load-Use Stall)**: Load 데이터가 MEM 단계에서 확정되어 EX 단계 포워딩이 불가능해 발생하는 1클록 대기.

</details>

```text
 [ 명령어 해독 (ID) ]
        │
        ├─ RAW Data Hazard ──> [ 포워딩 MUX ] (EX/MEM, MEM/WB 우회)
        │                       └─ Load-Use 의존 시 1-Cycle Stall 후 포워딩
        │
        └─ Control Hazard ───> [ BTB / BHT 동적 예측 ]
                                ├─ 예측 성공 : 연속 인출 (No Stall)
                                └─ 오예측 발생 : EX단계 감지 ─> Flush ─> PC 복구
```

### 동작 원리

1. **의존성 검출**: ID 단계에서 RAW 데이터 의존 또는 조건 분기 명령어 감지.
2. **포워딩/스톨 적용**: EX/MEM 레지스터 결과를 MUX로 우회하며, Load-Use 의존 시 1사이클 스톨 후 포워딩.
3. **분기 예측 및 복구**: BTB/BHT를 참조하여 예측 인출을 수행하고, EX 단계에서 오예측 확인 시 파이프라인 Flush 및 PC 복구.

#### 한줄 요약

- RAW 의존 시 연산 결과 우회 및 Load-Use 스톨을 처리하고, 조건 분기 시 예측 인출과 오예측 플러시를 집행하는 흐름.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **RAW 데이터 해저드(Read After Write Data Hazard)**: 앞 명령어의 쓰기가 완료되기 전에 뒤 명령어가 읽기를 시도하는 상태.
- **제어 해저드(Control Hazard)**: 분기 명령어의 실행 결과가 확정되지 않아 인출 경로를 결정하지 못하는 상태.

</details>

| 비교 항목 | 포워딩 메커니즘 (Forwarding) | 분기 예측 메커니즘 (Branch Prediction) |
|:---|:---|:---|
| **대상 해저드** | **RAW 데이터 해저드** | **제어 해저드 (Control Hazard)** |
| **작동 방식** | 레지스터 래칭 전 결과를 ALU 입력으로 바이패스 | 과거 이력 기반 분기 방향/주소 사전 인출 |
| **제약 사항** | **Load-Use 의존** 시 1클록 스톨 불가피 | 오예측 시 파이프라인 **플러시 패널티** 발생 |
| **주요 요소** | Forwarding Unit, Bypass MUX | BHT, BTB, Recovery Logic |

#### 한줄 요약

- 포워딩은 데이터 우회로 연산 대기를 제거하고, 분기 예측은 제어 추측으로 인출 대기를 제거하는 비교 체계.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **명령어 재배치(Instruction Reordering)**: 컴파일러가 독립적인 명령어를 Load와 Use 사이에 배치하여 스톨을 은닉하는 기법.
- **재주문 버퍼(Reorder Buffer, ROB)**: 추측 실행 결과를 순서대로 Commit하여 정밀 예외를 보장하는 버퍼.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| **Load-Use 스톨** 발생 | 컴파일러 **명령어 재배치** 적용 | 1클록 대기 시간 은닉 |
| **분기 오예측** 빈발 | TAGE 예측기 및 **BTB** 용량 확장 | 예측 정확도 향상 및 플러시 감소 |
| 오경로 명령어의 상태 오염 | **ROB(Reorder Buffer)** 기반 Commit 및 정밀 예외 적용 | 메모리 및 레지스터 오염 방지 |
| 포워딩 MUX 증가로 인한 타이밍 병목 | Critical Path 분석 및 MUX 구조 최적화 | 파이프라인 클록 주파수 확보 |

#### 한줄 요약

- 컴파일러 재배치, 고급 예측기(TAGE), ROB 커밋 구조를 연계하여 파이프라인 효율성을 최적화하는 대책.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **해저드 제어 체계(Hazard Control Framework)**: 포워딩, 분기 예측, ROB 커밋 구조를 통합하여 파이프라인 손실을 최소화하는 아키텍처.

</details>

- 데이터 해저드는 하드웨어 포워딩과 컴파일러 재배치로 차단하고, 제어 해저드는 BTB/TAGE 동적 예측 및 ROB 정밀 예외 복구 구조를 결합하는 파이프라인 성능 최적화 체계 적용 필수.

#### 한줄 요약

- 포워딩 바이패스와 동적 분기 예측 및 ROB 복구 구조를 결합한 CPI(1.0) 수렴 최적화 체계 적용.
