---
sidebar:
  order: 77
  label: "077. 소프트웨어 안전: GAMAB•ALARP (Software Safety GAMAB ALARP)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "소프트웨어 안전: GAMAB•ALARP (Software Safety GAMAB ALARP)"
date: "2026-08-10T23:40:00+09:00"
tags:
  - "notes-software"
weight: 77
extra:
  question_no: "077"
  source_status: "기출"
  source_history: "128회"
  priority: 50
  priority_note: "128회 기출, 허용 위험 판단의 안전 기준"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **GAMAB (Globalement Au Moins Aussi Bon)**: 불어 구문으로 "전체적으로 적어도 기존보다 같거나 우수해야 함"을 뜻하며, 신규 소프트웨어/시스템의 리스크 수준이 기존 운영 중인 벤치마크 시스템의 리스크 수준보다 더 높아서는 안 된다는 안전 원칙.
- **ALARP (As Low As Reasonably Practicable)**: "합리적으로 실행 가능한 한 낮추어야 함"이라는 원칙으로, 리스크 경감 비용(Cost)과 그에 따른 안전 이득(Benefit)이 상식적으로 불균형을 이루지 않는 한 리스크를 지속적으로 낮춰야 하는 위험 통제 영역 개념.
- **Residual Risk (잔여 위험)**: 안전 대책 및 위험 저감 조치를 적용한 후에도 최종 시스템에 여전히 남아있는 허용 가능한 수준의 리스크.

</details>

- 정의/개념: 철도, 항공, 자율주행 등 미션 크리티컬 시스템에서 잔여 위험(Residual Risk)의 수용 가능 여부를 판정하기 위한 2대 대표 안전 위험 통제 원칙인 **GAMAB & ALARP**
- 배경/필요성: '위험 0%(Zero Risk)' 달성의 현실적 불가능성 극복, 경제적 비용 투입 한계 내에서 시스템 안전성을 합리적이고 객관적으로 증명(Safety Case)할 기준 필요성

#### 한줄 요약

- 동등 안전성과 합리적 저감에 기반한 위험 수용 판단이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Comparative Safety (GAMAB의 비교 안전성)**: 새로운 시스템의 전체 위험 수치가 기존 레퍼런스 시스템보다 악화되지 않음을 입증.
- **Cost-Benefit Balance (ALARP의 비용-효익 균형)**: 위험 제거에 소요되는 인프라 비용이 감소하는 사고 위험 이익보다 현저히 과도하지(Gross Disproportion) 않은 지점까지 저감.

</details>

- 레퍼런스 시스템 대비 안전성 악화 절대 불가 (**GAMAB**)
- 위험을 **Unacceptable / ALARP / Broadly Acceptable** 3개 구역으로 분할 통제 (**ALARP**)
- 정량적 위험 평가(QRA: Quantitative Risk Assessment)와 **Safety Case (안전 보증 사례)** 연동

#### 한줄 요약

- 안전 사례로 동등성과 합리적 저감 근거를 함께 입증하는 것이 핵심이다.

## Ⅲ. 구조 및 구성요소 (ALARP 3대 위험 영역 모델)

<details><summary>핵심 용어</summary>

- **ALARP 3대 영역**: 1. Intolerable/Unacceptable Region (불허용 영역), 2. ALARP Region (합리적 저감 영역: 비용 대 효과 분석 필요), 3. Broadly Acceptable Region (광범위 허용 영역: 별도 대책 불필요).

</details>

```text
▲ 위험도 (Risk Level)
│
├─── [1. Intolerable Region (불허용 영역)] ──► 예외 없이 무조건 위험 저감 필수 (운행 불가)
│
├─── [2. ALARP Region (합리적 저감 영역)]  ──► 비용 대 이득이 현저히 불균형하지 않으면
│                                               위험을 지속적으로 낮추어야 함 (Tolerable)
├─── [3. Broadly Acceptable Region]        ──► 위험이 매우 낮아 추가 대책 없이 수용 가능
│
└─── Zero Risk (비현실적 목표)
```

선의 의미: 위험 수준에 따라 절대 불허용 영역, ALARP 합리적 저감 영역, 광범위 수용 영역으로 3원화 관리되는 아키텍처.

| 구분 분류 | 안전 원칙 명칭 | 핵심 판단 기준 및 메커니즘 |
|:---|:---|:---|
| **GAMAB** | **Globalement Au Moins Aussi Bon** | 신규 시스템의 총 위험도가 기존 레퍼런스 시스템보다 **적어도 같거나 더 안전해야 함 (Equivalence)** |
| **ALARP** | **Unacceptable Region** | 리스크 수준이 너무 높아 어떤 이유로도 허용 불가 $\rightarrow$ **무조건적인 위험 제거** |
| | **ALARP Region** | 비용이 안전 편익에 비해 현저히 불균형(Gross Disproportion)을 이루지 않는 한 **위험 저감 계속** |
| | **Broadly Acceptable Region** | 리스크가 극히 미미하여 추가 저감 조치 없이 **잔여 위험을 그대로 수용** |

#### 한줄 요약

- 위험 평가•안전 요구•저감 검증을 안전 사례로 잇는 구조가 핵심이다.

## Ⅳ. 흐름도 (ALARP / GAMAB 적용 절차)

<details><summary>핵심 용어</summary>

- **Gross Disproportion Test**: ALARP 구역에서 리스크 저감 조치를 멈추기 위해, "위험 제거에 들어가는 비용이 얻어지는 안전 효과보다 10배 이상 비현실적으로 크다"는 것을 객관적으로 입증하는 시험.

</details>

```text
┌──────────────────────────────┐
│ Hazard Identification (위험원)│
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. GAMAB: 기존 시스템 대조   │
│    (기존보다 안전한가?)      │
│ 2. ALARP: 3대 구역 맵핑      │
│ 3. Gross Disproportion 평가  │
│ 4. Safety Case 보고서 작성   │
└──────────────┬───────────────┘
               ▼
   [잔여 위험 수용 & 인증 획득]
```

### 동작 원리

1. **Hazard Identification**: 시스템의 잠재 위험원 및 심각도 스캔.
2. **GAMAB Check**: 레퍼런스 구형 시스템 대비 종합 위험도 수치 대조 $\rightarrow$ 같거나 우수함 입증.
3. **ALARP Mapping**: 각 위험별 3대 영역 맵핑 후 ALARP 구역 항목에 대해 **Gross Disproportion Test** 수행.
4. **Safety Case**: 독립 평가자(ISA: Independent Safety Assessor)에게 안전 보증 문서(Safety Case) 제출 및 수용.

#### 한줄 요약

- 비교•저감•안전 사례 기반 잔여 위험 결정이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **MEM (Minimum Endogenous Mortality)**: 인간의 자연적 최소 사망률(연간 약 $10^{-4}$)을 기준으로 시스템으로 인한 추가 사망 위험을 $10^{-5}$ 이하로 통제하려는 독일의 대표적 안전 원칙.

</details>

| 비교 항목 | GAMAB (프랑스 중심 유럽 표준) | ALARP (영국 표준 / IEC 61508) | MEM (독일 표준) |
|:---|:---|:---|:---|
| 핵심 관점 | **기존 레퍼런스 시스템과의 상대적 동등성**| **비용 대비 위험 저감 효과의 합리적 균형**| **인간의 자연 사망 확률 기반 절대 수치 통제** |
| 판단 방식 | 벤치마크 시스템과의 상대 비교 | 3개 구역 분할 및 Gross Disproportion 평가 | 연간 사망 위험률 $10^{-5}$ 미만 절대 평가 |
| 주 주요 적용 도메인| **철도 (CENELEC EN 50126), 제어 시스템**| **원자력, 오일/가스, IEC 61508 일반 산업** | **자동차, 철도 (독일계 시스템)** |

#### 한줄 요약

- 참조 동등성은 안전 동등성, 저감 한계는 심한 불균형으로 판단한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Safety Case (안전 보증 사례)**: GSN(Goal Structuring Notation) 등의 기법을 사용하여, 시스템이 필요한 수준의 안전성을 확보했음을 시각적 논리로 입증하는 정형화된 보고서.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| ALARP 수용 판단 시 비용 절감을 위한 주관적 왜곡 | **독립 안전 평가원(ISA: Independent Safety Assessor) 검증 강제** | 검증 중립성 보장 |
| GAMAB 적용 시 비교할 적절한 레퍼런스 시스템 부재 | **IEC 61508 / ISO 26262 규격의 ALARP 정량 지표로 전환** | 표준 검증 완결 |
| Safety Case 작성 시 증거(Evidence) 파편화 | **GSN (Goal Structuring Notation) 아규먼트 구조화** | 시각적 보증 완결 |

> 사례: **철도 신호 SW (EN 50128) 및 자동차 SW (ISO 26262) 내 GAMAB/ALARP 연동**

#### 한줄 요약

- 세 비교 가능성, 보수적 가정, 독립 평가자, 위험 승인자가 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **안전 통제 수립 기준(Software Safety Standards)**: 기능 안전 등급(SIL/ASIL), 안전 원칙(GAMAB/ALARP) 및 ISA 독립 검증 체계에 의거한 체계.

</details>

- **안전 통제 수립 기준**에 따라 고위험 미션 크리티컬 SW 구축 시 **GAMAB + ALARP + Safety Case (GSN)** 필수 인가

#### 한줄 요약

- 참조 가능성과 저감 합리성에 맞는 위험 수용 원칙 선택 기준이 핵심이다.
