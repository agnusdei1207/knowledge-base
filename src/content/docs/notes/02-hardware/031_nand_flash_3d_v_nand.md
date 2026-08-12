---
sidebar:
  order: 31
  label: "031. 3D V-NAND와 2D NAND 비교 (3D vs 2D NAND)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "3D V-NAND와 2D NAND 비교 (3D vs 2D NAND)"
date: "2026-08-08T16:28:00+09:00"
tags:
  - "notes-hardware"
weight: 31
extra:
  question_no: "031"
  source_status: "기출"
  source_history: "126회"
  priority: 50
  priority_note: "수직 적층•셀 상태•공정 비교"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **3D 수직 플래시 (3D V-NAND / Vertical NAND)**: 평면 미세화의 물리적 한계를 극복하기 위해, 전하 트랩 셀(CTF)을 실리콘 기판 위로 층층이 수직 적층(Vertical Stacking, 100~300+ Layer)하여 집적도를 3차원 확장한 낸드 플래시.
- **2D 평면 플래시 (2D Planar NAND)**: 실리콘 기판 평면(XY 축) 방향으로 트랜지스터 노드 선폭(10nm 급)을 미세 축소(Scaling Down)하여 셀 간격을 좁히던 기존 2차원 낸드 플래시.
- **셀 간격 축소 한계 (Planar Scaling Limit)**: 10nm 이하로 회로 선폭이 줄어들면서 인접 셀 간의 전자 간섭(Crosstalk) 및 절연막 파괴로 인한 데이터 보존 불가 물리 현상.

</details>

- 정의/개념: 평면 미세화 대신 수직 적층 방식(100~300+ Layers) 및 **전하 트랩 셀(CTF)** 기술을 적용하여 칩 용량을 3차원으로 확장하는 **3D V-NAND(Vertical NAND)** 아키텍처.
- 배경/필요성: 기존 **2D Planar NAND** 공정이 10nm 대에 진입하면서 발생한 **셀 간격 축소 한계(Planar Scaling Limit)**, 즉 인접 셀 간 간섭(Crosstalk) 및 전하 누설 폭증 문제를 해결하기 위해 도입.

#### 한줄 요약
- 회로 선폭 수평 미세화 한계를 수직 적층(Vertical Stacking) 및 전하 트랩(CTF) 셀로 전환하여 집적도, 신뢰성, 전력 효율을 획기적으로 개선한 반도체 기술.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **전하 트랩 플래시 (Charge Trap Flash, CTF)**: 도전성 부유 게이트(Floating Gate) 대신 부도체 질화막(SiN)에 전자를 트랩 가두어 누설 전류와 셀 간 간섭을 획기적으로 낮춘 셀 구조.
- **수직 층수 (Vertical Layer Count)**: 3D NAND 수직 수직축(Z축)으로 겹겹이 올려 형성한 게이트/워드라인 수직 적층 레이어 수 (예: 128단, 232단, 300단+).
- **고종횡비 식각 (High Aspect Ratio Etching / HAR Contact)**: 100~300단 이상 깊게 쌓인 고층 절연막을 수직 관통하여 직경 수십 나노미터의 정밀 미세 홀(Hole)을 한 번에 뚫어내는 초고난도 반도체 식각 공정.

</details>

- 부도체 질화막 기반 **전하 트랩 플래시(CTF)** 기술을 도입하여 2D Floating Gate 대비 인접 셀 간 크로스톡 간섭을 99% 이상 소거.
- 셀 간격을 무리하게 줄이지 않고 **수직 층수(Layer Count)**를 수직 확장함에 따라 쓰기 속도가 2배 빨라지고 전력 소모 50% 절감.
- 수직 채널을 한꺼번에 뚫어내는 **고종횡비 식각(HAR Etching)** 및 다중 스택(Double Stack) 결합 공정 기술이 제조 수율 수치 결정.

#### 한줄 요약
- CTF 수직 적층 구조를 통해 셀 간 크로스톡 간섭을 없애고 쓰기 속도 및 수명 내구성을 대폭 상향시킴.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **수직 채널 스트링 (Vertical Channel String / Channel Hole)**: 적층된 100~300개 워드라인을 수직 관통하여 DRAM/플래시 전류 신호를 연결하는 수직 기둥 체계.
- **워드라인 적층 (Wordline Gate Stack)**: 층층이 쌓인 게이트 금속(Tungsten) 레이어로 각 층의 셀에 읽기/쓰기 전압을 가하는 수직 레이어 판.
- **COP (Cell on Peri)**: 제어 회로(Peripheral Circuit)를 셀 아래 하단 기판에 먼저 배치하고 그 위에 3D Cell을 적층하여 칩 다이 면적을 극소화하는 기술.

</details>

```text
[ 3D V-NAND Vertical Gate Stack Architecture ]
┌───────────────────────────────────────────────────────────┐
│ Bitline (Top Connection)                                  │
├───────────────────────────────────────────────────────────┤
│ Layer N   Wordline (W/L N) ───[ CTF Cell ]───┐             │
│ Layer ... Wordline ...     ───[ CTF Cell ]───┼─ Vertical  │
│ Layer 2   Wordline (W/L 2) ───[ CTF Cell ]───│  Channel   │
│ Layer 1   Wordline (W/L 1) ───[ CTF Cell ]───┘  Hole      │
├───────────────────────────────────────────────────────────┤
│ COP (Cell-on-Peripheral) Logic Control Circuit Substrate │
└───────────────────────────────────────────────────────────┘
```

| 구성요소 | 역할 및 작동 원리 | 차별점 및 실무 유용성 |
|:---|:---|:---|
| **CTF 셀 (Charge Trap)** | 부도체 SiN 막에 전자를 보관하여 데이터 1/0 상태 유지 | Floating Gate 대비 인접 셀 누설/간섭 원천 차단 |
| **수직 채널 스트링** | 수직 관통 홀을 형성하여 100+개 적층 셀을 직렬 연결 | 2D의 팽창 한계를 수직 축으로 확장하여 고용량화 구현 |
| **워드라인 적층 파티션** | 금속 텅스텐 레이어로 각 높이 층의 Cell Gate 통제 | 층수가 올라가도 동일 칩 다이 면적에 용량 비례 증대 |
| **COP (Cell-on-Peri)** | 로직 제어 회로를 3D Cell 밑바닥에 숨겨 배치 | 칩 크기를 30% 이상 줄여 단위 웨이퍼당 칩 생산량 극대화 |

#### 한줄 요약
- CTF Cell, Vertical Channel String, Wordline Gate Stack 및 COP(Cell-on-Peri) 구조로 구성됨.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **ISPP (Incremental Step Pulse Programming)**: 낸드 셀 프로그래밍 시 전압 맥박을 단계별로 미세하게 높여 목표 임계 전압(Vth) 정밀도를 맞추는 산술 프로그램 방식.
- **다중 스택 (Multi-Stack / Double Stacking)**: 식각 깊이 한계를 넘기 위해 100단 스택 2개를 개별 제작한 후 상하 수직으로 붙여 200단 이상을 달성하는 결합 공정.

</details>

```text
[ 3D V-NAND Manufacturing & Cell Operation Flow ]
                         │
                         ▼
        [ 1. COP Peripheral Substrate Circuit Build ]
                         │
                         ▼
        [ 2. Alternate Oxide/Nitride Layer Stacking (100+ Layers) ]
                         │
                         ▼
        [ 3. High Aspect Ratio (HAR) Channel Hole Etching ]
                         │
                         ▼
        [ 4. CTF Cell Material & Vertical Channel Deposition ]
                         │
                         ▼
        [ 5. ISPP Programming & Multi-Level Cell State Read (SLC/TLC/QLC) ]
```

### 동작 원리

1. **COP 로직 탑재**: 바닥 기판에 **COP(Cell-on-Peri)** 제어 회로를 우선 형성함.
2. **수직 멀티 적층**: 절연막과 몰리브덴/질화막을 100~300+ 층으로 **수직 적층**함.
3. **고종횡비 식각(HAR Etching)**: **HAR 채널 식각**으로 상단에서 하단까지 정밀 수직 통로 구멍을 한 번에 뚫어냄.
4. **ISPP 정밀 프로그래밍**: 완성된 CTF 수직 셀에 **ISPP** 전압 펄스를 통해 TLC(3-bit)/QLC(4-bit) 멀티 레벨 임계 전압을 정밀 프로그래밍함.

#### 한줄 요약
- COP 로직 구축 -> 수직 층 적층 -> HAR Channel Hole Etching -> CTF Deposition -> ISPP Cell Read/Write 순으로 진행됨.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **TLC (Triple-Level Cell)**: 1개 셀당 3비트(8개 전압 상태)를 저장하는 구조.
- **QLC (Quad-Level Cell)**: 1개 셀당 4비트(16개 전압 상태)를 저장하여 용량을 극대화하나 P/E Cycle 수명이 1,000회 이하로 낮아지는 구조.

</details>

| 비교 항목 | 3D V-NAND (Vertical NAND) | 2D Planar NAND (Flat NAND) |
|:---|:---|:---|
| **집적도 확장 축** | **수직 축 (Z-Axis Vertical Stacking)** | 평면 축 (X-Y Axis Horizontal Scaling) |
| **셀 구조** | **전하 트랩 (CTF / Charge Trap Flash)** | 부유 게이트 (Floating Gate) |
| **인접 셀 간섭** | **극도로 낮음** (크로스톡 간섭 소거) | 매우 심함 (15nm 이하에서 데이터 변질) |
| **셀 P/E 수명 내구성**| **우수함** (2D 대비 P/E Cycle 수명 2~10배) | 취약함 (미세화 진행 시 급격한 수명 저하) |
| **쓰기 속도 / 전력** | 속도 2배 향상 / 전력 50% 절감 | 속도 지연 / 높은 정적 전력 소모 |
| **핵심 제조 공정** | **고종횡비 식각 (HAR Etching)** | 미세 노광 (EUV / ArFi Photolithography) |

#### 한줄 요약
- 3D V-NAND는 Z축 수직 적층, CTF 셀, HAR 식각 및 고내구성을 제공하고, 2D NAND는 XY축 평면 미세화 및 고간섭 한계를 가짐.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **원시 비트 오류율 (Raw Bit Error Rate, RBER)**: 낸드 셀에서 데이터 읽기 수행 시 ECC 정정 전 발생하는 초기 물리 비트 에러 비율 (3D V-NAND가 2D 대비 10배 이상 우수).
- **읽기 재시도 (Read Retry)**: 낸드 셀의 경화 전하 누실로 판독 전압 산포가 틀어졌을 때, Vth 기준 전압을 오프셋 변경하며 정답을 되찾는 FTL 기술.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 200단 이상 고층 적층 시 수직 채널 구멍 휘어짐(HAR Etching 결함) | **다중 스택(Double Stacking / Multi-Deck)** 공정 분할 | 식각 수율 확보 및 300단+ V-NAND 안정 생산 |
| QLC(4-bit) V-NAND 적용 시 전압 산포 16개 중첩으로 **RBER** 상승 | 3D CTF 셀 정밀 **ISPP 전압 제어** 및 LDPC ECC 엔진 연동 | Bit Error 발생 정정 및 데이터 정합성 보장 |
| 셀 전하 경화 누실로 인한 Read Error 발생 | FTL **읽기 보정(Read Offset)** 및 **Read Retry** 튜닝 | 무효 데이터 읽기 방지 및 장기 보존성 유지 |
| QLC SSD 지속 쓰기 시 SLC 버퍼 고갈로 인한 속도 급락 | **가변 SLC 캐시(Dynamic SLC Cache)** 영역 가동 | 쓰기 속도 급락 방지 및 일관된 성능 유지 |

#### 한줄 요약
- Double Stacking 분할 공정, LDPC ECC, Read Retry offset 보정 및 Dynamic SLC Cache 기술을 적용함.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **NAND 아키텍처 선택 기준 (NAND Selection Criteria)**: 대상 저장장치의 용량 밀도, P/E Cycle 수명, 칩당 단가 및 RBER 목표를 수립하여 3D V-NAND의 층수 및 TLC/QLC 비트 셀 유형을 확정하는 결정 프레임워크.

</details>

- **NAND 아키텍처 선택 기준 (NAND Selection Criteria)**에 의거하여 enterprise SSD 및 고성능 스토리지 구축 시, 2D 미세화 한계를 완전히 넘어선 100~300단+ **3D V-NAND**와 **전하 트랩(CTF)** 기술을 기본 아키텍처로 채택하고, **Double Stacking** 공정 수율 확보 및 LDPC ECC 엔진 기반의 고신뢰성 메모리 구축 체계 적용 필수.

#### 한줄 요약
- 평면 미세화 한계 극복을 위한 3D V-NAND CTF 수직 적층 아키텍처 채택 및 Double Stacking/LDPC ECC 결합 체계 적용.
