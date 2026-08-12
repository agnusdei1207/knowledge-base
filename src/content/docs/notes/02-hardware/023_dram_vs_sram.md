---
sidebar:
  order: 23
  label: "023. DRAM과 SRAM 비교 (DRAM vs SRAM)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "DRAM과 SRAM 비교 (DRAM vs SRAM)"
date: "2026-08-08T14:34:00+09:00"
tags:
  - "notes-hardware"
weight: 23
extra:
  question_no: "023"
  source_status: "기출"
  source_history: "125회"
  priority: 50
  priority_note: "셀 구조•지연•밀도 비교"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **동적 임의 접근 메모리(Dynamic Random-Access Memory, DRAM)**: 1개의 트랜지스터와 1개의 커패시터(1T1C) 셀 구조를 기반으로 높은 집적도와 경제적 용량을 제공하지만, 전하 방전 방지를 위해 주기적 리프레시(Refresh)가 필수적인 휘발성 반도체.
- **정적 임의 접근 메모리(Static Random-Access Memory, SRAM)**: 6개의 트랜지스터(6T) 래치 회로 셀 구조를 기반으로 리프레시 동작 없이 1~5ns 초고속 접근 속도를 제공하는 휘발성 반도체.
- **휘발성(Volatility)**: 전원 공급(VCC)이 중단되면 저장되어 있던 2진 논리 데이터(0/1)가 즉각 소멸되는 반도체 전하 성질.

</details>

- 정의/개념: 커패시터 전하 저장 방식의 고밀도 **DRAM(Dynamic RAM)**과 플립플롭 래치 상태 저장 방식의 초고속 **SRAM(Static RAM)**으로 구별되는 **휘발성(Volatility)** 메인 반도체 소자 비교 규격.
- 배경/필요성: 단일 반도체 셀 구조로는 초고속 접근 속도와 대용량 고밀도 집적성을 동시에 만족시키는 단일 메모리를 제작할 수 없으므로, 하드웨어 계층 배치(Cache vs Main Memory)의 근거를 제공함.

#### 한줄 요약
- 1T1C 구조의 대용량 DRAM과 6T 래치 구조의 초고속 SRAM의 동작 원리 및 스펙 비교를 통해 메모리 계층 구성을 최적화함.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **1T1C 셀(1T1C Cell)**: 1개 Access Transistor와 1개 Storage Capacitor로 구성된 DRAM 비트 셀로, 커패시터에 전하(Charge)를 충전/방전하여 비트를 구별함.
- **6T 래치(6T Latch)**: 4개의 Cross-coupled Inverter 트랜지스터와 2개의 Pass-gate 트랜지스터로 구성된 SRAM 비트 셀로, 쌍안정(Bistable) 상태를 정적으로 유지함.
- **비파괴 판독(Non-Destructive Read)**: SRAM에서 읽기 연산 시 셀 내부 래치 상태가 훼손되지 않아 복원(Restore) 전송 과정이 필요 없는 독출 특성.
- **파괴적 판독(Destructive Read)**: DRAM에서 워드라인이 켜지며 커패시터 전하가 비트라인으로 유출되어 읽기 순간 데이터가 파괴되므로 Sense Amp가 전하를 즉시 재충전(Restore)해야 하는 특성.

</details>

- **1T1C 셀(1T1C Cell)** 구조를 갖는 **DRAM**은 집적도가 월등히 높아 작은 다이 면적에 기가바이트(GB) 단위 대용량 메인 메모리 구현 가능.
- **6T 래치(6T Latch)** 구조의 **SRAM**은 **비파괴 판독(Non-Destructive Read)** 및 래치 상태 유지 특성을 통해 나노초 미만의 고속 억세스 지원.
- DRAM은 시간 경과에 따른 커패시터 전하 누설(Leakage)을 보충하기 위한 주기적 **리프레시(Refresh)** 동작 필수.

#### 한줄 요약
- DRAM은 1T1C 파괴적 판독 및 periodic Refresh 기반 대용량화를 달성하고 SRAM은 6T 래치 비파괴 판독 기반 저지연 가속을 달성함.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **워드라인(Wordline)**: 메모리 셀 행(Row)을 선택하여 접근 트랜지스터 게이트를 Turn-on 시키는 행 선택 제어선.
- **비트라인(Bitline)**: 선택된 셀의 데이터 전하 및 래치 전압 신호를 Sense Amplifier로 전달하거나 쓰기 전압을 싣는 열 데이터선.
- **감지 증폭기(Sense Amplifier)**: DRAM 셀 파괴적 판독 시 비트라인 상에 발생하는 몇 미전압(mV) 수준의 미세 전하 변위를 VCC/GND 논리 1/0으로 극대 증폭 및 Restore 시키는 핵심 독출 회로.
- **복원(Restore)**: DRAM 독출 직후 감지 증폭기가 비트라인 전압으로 파괴된 1T1C 커패시터 전하를 원상 복구 재충전하는 하드웨어 연산.

</details>

```text
[ DRAM 1T1C Cell Structure ]           [ SRAM 6T Cell Structure ]
      Wordline                               Wordline
         │                                      │
         ▼                                      ▼
   ┌───[Gate]───┐                         ┌───[Pass 1]───┐   ┌───[Pass 2]───┐
Bit──┤Transistor ├──Capacitor──GND  Bit───┤ Inverter 1  ├───┤ Inverter 2  ├───Bit#
   └────────────┘                         └──────────────┘   └──────────────┘
 (Destructive Read -> Restore)         (Bistable Latch -> Non-Destructive)
```

| 비교 항목 | DRAM (Dynamic RAM) | SRAM (Static RAM) |
|:---|:---|:---|
| **셀 구동 회로** | **1T1C** (1 Transistor + 1 Capacitor) | **6T** (6 Transistors Cross-Coupled Latch) |
| **판독 메커니즘** | **파괴적 판독** (Sense Amp **복원** 필수) | **비파괴 판독** (래치 전압 상태 직접 유지) |
| **리프레시 동작** | **필요함** (64ms 마다 Periodic Refresh) | **불필요함** (VCC 전원 공급되는 한 상태 보존) |
| **비트당 면적/단가**| 매우 작고 저렴함 (고밀도 GB 구현) | 크고 비쌈 (DRAM 대비 약 100배 고가) |
| **억세스 지연** | **60 ~ 100 ns** (Row Act + Precharge 수반) | **1 ~ 5 ns** (SRAM Array Direct Decode) |

#### 한줄 요약
- DRAM은 1T1C+Sense Amp 복원 회로 기반으로 동작하고 SRAM은 6T 래치 인버터 결합 회로 기반으로 동작함.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **행 활성(Row Activation / RAS)**: DRAM 주소의 Row Address를 활성화하여 해당 행의 1T1C 셀 전하를 비트라인으로 방출 및 감지 증폭하는 1단계.
- **열 선택(Column Selection / CAS)**: Sense Amp에 래칭된 행 데이터 중 억세스하고자 하는 Column Address 비트를 선택 인출하는 2단계.
- **프리차지(Precharge)**: 다음 Row 억세스를 위해 비트라인 전압을 VCC/2 레벨로 다시 균등화 초기화시키는 준비 연산.

</details>

```text
[ DRAM Read Operation Flow ]
 1. Row Activation (RAS) ──> 2. Cell Charge Discharge to Bitline ──> 3. Sense Amp Boost & Restore
                          ──> 4. Column Selection (CAS) & Data Output ──> 5. Precharge (PR)

[ SRAM Read Operation Flow ]
 1. Wordline Assert      ──> 2. Bitline Differential Voltage Sense  ──> 3. Direct Data Out
```

### 동작 원리

1. **DRAM 억세스 순서**: **행 활성(Row Activation)**으로 셀 전하를 방출하고, **감지 증폭기**로 전압을 증폭하며, 셀 전하를 **복원(Restore)**한 뒤, **열 선택(CAS)**으로 데이터를 출동시키고, 다음 작업을 위해 **프리차지(Precharge)**를 완결함.
2. **SRAM 억세스 순서**: 워드라인(Wordline)이 켜지면 6T 래치의 차동 비트라인 전압을 1클록 내에 정적으로 직접 판독하여 대기 시간 없이 데이터를 출력함.

#### 한줄 요약
- DRAM은 Row Act -> Sense/Restore -> CAS -> Precharge의 복잡한 커패시터 동적 절차를 거치며, SRAM은 Wordline 래치 직통 독출로 완료함.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **리프레시(Refresh)**: 커패시터의 자연 누설 전류(Leakage Current)로 데이터 1이 0으로 변질되는 현상을 방지하기 위해, 매 64ms 주기마다 전체 행을 읽어 재충전하는 동작.
- **접근 지연(Access Latency)**: CPU가 명령을 발생시킨 후 실제 메모리가 유효 데이터를 버스 상에 적재하기까지 걸리는 클록/시간.

</details>

| 성능 지표 | DRAM (Dynamic RAM) | SRAM (Static RAM) |
|:---|:---|:---|
| **핵심 용도** | 시스템 메인 메모리, GPU VRAM, HBM | CPU L1/L2/L3 캐시, 레지스터, Register File |
| **집적 밀도** | 초고밀도 (동일 다이 면적당 SRAM의 약 6~10배) | 저밀도 (트랜지스터 6개로 칩 다이 면적 과다) |
| **동적/정적 전력** | 동적 전력 높음 (Precharge/Refresh 수반) | 정적 누설 전력(Leakage Power) 존재, 동적 전력 저조 |
| **제조 공정** | 커패시터 형성용 특수 3D DRAM 공정 수반 | 표준 논리 트랜지스터(CMOS) 공정과 100% 호환 |

#### 한줄 요약
- DRAM은 대용량 메인 메모리 및 HBM 인프라 구축에 적용되며 SRAM은 표준 CMOS 공정의 CPU 온칩 고속 캐시로 적용됨.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **행 적중(Row Hit / Open-Page Policy)**: 이전에 열린 DRAM Row를 프리차지 없이 연속 Column 인출만 수행하여 DRAM 접근 지연을 60ns에서 15ns로 대폭 절감하는 기술.
- **오류 정정 코드(Error-Correcting Code, ECC)**: 미세 공정화에 따라 우주선(Cosmic Ray)이나 Alpha Particle로 인한 DRAM/SRAM 비트 반전(Single Event Upset)을 1-bit 정정, 2-bit 감지하는 정밀 회로.
- **전력 차단(Power Gating)**: 사용하지 않는 대형 SRAM 캐시 블록의 VCC 전원을 선택 차단하여 미세 공정의 정적 누설 전력(Leakage Power)을 소거하는 기술.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| DRAM **리프레시(Refresh)** 주기 구동 시 CPU 억세스 일시 대기 지연 | 뱅크 분산 리프레시(Per-Bank Refresh) 및 온도 가변 리프레시 | 리프레시 정체 지연 오버헤드 50% 절감 |
| 잦은 DRAM 행 변경(Row Miss)으로 인한 프리차지 오버헤드 | 메모리 컨트롤러 **행 적중(Row Hit)** 인터리빙 스케줄링 | DRAM 유효 억세스 대역폭 획기적 향상 |
| 미세 공정 SRAM 캐시의 **정적 누설 전력(Leakage Power)** 증가 | 캐시 블록 단위 **전력 차단(Power Gating)** 기술 연동 | 대기 상태 캐시 모듈 동적 전력 소모 소거 |
| 소형화 셀 전하 누설 및 Alpha Particle에 의한 비트 반전 Soft Error | On-Die **ECC (Error-Correcting Code)** 및 Parity 내장 | 데이터 정합성 보장 및 1-bit Soft Error 자동 정정 |

#### 한줄 요약
- Per-bank Refresh, Row Hit 우선 스케줄링, SRAM Power Gating 및 On-die ECC 정정 기법을 통합 구동함.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **메모리 소자 선택 기준(Memory Device Selection Criteria)**: 대상 시스템 계층의 대역폭, 단위 용량당 제조 단가, 접근 지연 목표 및 리프레시 오버헤드를 대조하여 최적의 DRAM/SRAM 소자를 배치하는 프레임워크.

</details>

- **메모리 소자 선택 기준(Memory Device Selection Criteria)**에 근거하여 CPU 내장 L1/L2/L3 캐시 유닛에는 6T 래치 기반의 초고속 **SRAM** 소자를 채택하고, 시스템 대용량 주기억장치 및 AI 가속기 패키징 메모리에는 1T1C 고밀도 **DRAM(DDR5/HBM3e)** 소자 및 On-die ECC 체계 적용 필수.

#### 한줄 요약
- 1~5ns 초고속 온칩 캐시용 6T SRAM 및 고밀도 메인 메모리/HBM용 1T1C DRAM 소자의 계층적 이원화 채택 체계 적용.
