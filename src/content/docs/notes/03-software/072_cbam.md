---
sidebar:
  order: 72
  label: "072. CBAM 비용 편익 분석 방법 (Cost Benefit Analysis Method)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "CBAM 비용 편익 분석 방법 (Cost Benefit Analysis Method)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 72
extra:
  question_no: "072"
  source_status: "기출"
  source_history: "131회"
  priority: 30
  priority_note: "131회 기출, 아키텍처 대안 비용•효익 평가"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **CBAM (Cost Benefit Analysis Method, 아키텍처 비용 편익 분석 기법)**: 카네기 멜론 대학 SEI가 ATAM의 후속으로 정립한 평가 기법으로, ATAM에서 도출된 다양한 아키텍처 전략(Architectural Strategies)의 비용(Cost) 대 비즈니스 편익/효용(Benefit/Utility) 및 ROI를 정량 평가하여 투자 우선순위를 결정하는 경제적 분석 모델.
- **ROI (Return on Investment, 투자 대비 수익)**: 아키텍처 변경에 투자되는 수명주기 총비용 대비 얻게 되는 비즈니스 효용의 비율.
- **Utility Score (효용 점수)**: 이해관계자가 특정 품질 속성의 응답 측정치(Response Measure)에 부여한 0~100점 사이의 정량적 비즈니스 가치점수.

</details>

- 정의/개념: ATAM 아키텍처 평가의 기술적 결과를 바탕으로, 제시된 각 아키텍처 전략들의 경제적 비용(Cost)과 효익(Benefit)을 정량 계산하여 최적의 아키텍처 투자 우선순위를 의사결정하는 기법인 **CBAM**
- 배경/필요성: ATAM만으로는 "이 아키텍처 변경에 돈을 얼마나 투입해야 하는가?"라는 최고경영자(C-Level)의 경제적 의사결정 질문에 답을 제공하지 못하는 한계 극복 요구성

#### 한줄 요약

- 품질 효익과 수명주기 비용에 기반한 비용 편익 분석 방법이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Benefit-Cost Ratio (BCR, 효익-비용 비율)**: 특정 아키텍처 전략 $j$의 가중 효익($B_j$)을 그 전략 도입 수명주기 비용($C_j$)으로 나눈 산출값 ($BCR_j = B_j / C_j$).
- **Economic Evaluation of Architecture**: 기술적 우수성에 국한되지 않고, 한정된 IT 예산(Budget) 내에서 최대 ROI를 내는 아키텍처 투자 전략 선발.

</details>

- **ATAM 평가의 경제성 확장 모델 (ATAM $\rightarrow$ CBAM 연계)**
- **BCR (Benefit-Cost Ratio)** 수치 기반 투자 전략 우선순위(Priority) 산출
- 기술적 아키텍처 용어와 C-Level 예산 통제 언어의 결합

#### 한줄 요약

- 효용 함수, 전략 비용, 의존성, 불확실성이 핵심이다.

## Ⅲ. 구조 및 구성요소 (CBAM 6대 계산 요소)

<details><summary>핵심 용어</summary>

- **Architectural Strategy (AS, 아키텍처 전략)**: 품질 속성 요구를 충족시키기 위해 아키텍터가 제안한 디자인 패턴, 아키텍처 스타일 및 기술 요소 결정.

</details>

```text
[ATAM 평가 결과 (품질 시나리오 & AS 전략)]
                   │
                   ▼ (CBAM 경제성 평가 대입)
┌────────────────────────────────────────────────────────┐
│ 1. 품질 속성 시나리오 중요도 가중치 ($W_i$) 설정       │
│ 2. 전략 적용 전/후 효용 점수 변화량 ($\Delta U_{ij}$)   │
│ 3. 전략별 총 수명주기 개발/운용 비용 ($C_j$) 산정      │
└──────────────────────────┬─────────────────────────────┘
                           ▼
[BCR ($B_j/C_j$) 계산] ──► [최적 아키텍처 투자 우선순위 확정]
```

선의 의미: ATAM에서 도출된 시나리오와 아키텍처 전략(AS)을 수거하여 가중치 $W_i$, 효용 변화량 $\Delta U_{ij}$, 개발비용 $C_j$를 대입 후 BCR을 산출하는 체계.

| CBAM 구성요소 | 개념 및 정의 | 수식 및 계산 수단 |
|:---|:---|:---|
| **Scenario Weight ($W_i$)** | 시나리오 $i$가 비즈니스 전체에서 갖는 상대적 중요도 | 이해관계자 100점 배분 투표 |
| **Utility Change ($\Delta U_{ij}$)**| 전략 $j$ 적용 시 시나리오 $i$의 효용 점수 증가량 | $\Delta U_{ij} = U_{\text{after}} - U_{\text{before}}$ |
| **Strategy Benefit ($B_j$)** | 전략 $j$가 제공하는 총 가중 효익의 합 | $B_j = \sum (W_i \times \Delta U_{ij})$ |
| **Strategy Cost ($C_j$)** | 전략 $j$를 구현/운영하는 총 수명주기 비용 | 인건비 + 라이선스 + 인프라 비용 |
| **Benefit-Cost Ratio ($BCR_j$)**| **전략 $j$의 최종 투자 대비 효익 비율** | **$BCR_j = \frac{B_j}{C_j}$ (우선순위 지표)** |

#### 한줄 요약

- 품질 응답, 응답 측정값, 시나리오 가중치, 수명주기 비용의 평가 구조가 핵심이다.

## Ⅳ. 흐름도 (CBAM 9단계 수행 절차)

<details><summary>핵심 용어</summary>

- **CBAM 9 Step Process**: 1. 시나리오 정제 $\rightarrow$ 2. 아키텍처 전략(AS) 도출 $\rightarrow$ 3. 효용 수치 산정 $\rightarrow$ 4. 시나리오 가중치 할당 $\rightarrow$ 5. 효익 계산 $\rightarrow$ 6. 비용 계산 $\rightarrow$ 7. BCR 계산 $\rightarrow$ 8. 우선순위 결정 $\rightarrow$ 9. 투자 확정.

</details>

```text
┌──────────────────────────────┐
│ ATAM 시나리오 정제           │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 시나리오 가중치 $W_i$ 할당 │
│ 2. AS 전략별 효용변화 $\Delta U$│
│ 3. 총 가중 효익 $B_j$ 합산   │
│ 4. 총 소요 비용 $C_j$ 산정   │
│ 5. $BCR_j = B_j / C_j$ 산출  │
└──────────────┬───────────────┘
               ▼
 [BCR 순위별 아키텍처 예산 집행]
```

### 동작 원리

1. **Weighting**: 이해관계자들이 시나리오별 가중치($W_i$) 정량 배분.
2. **Utility Estimation**: 각 아키텍처 전략(AS) 적용 시 응답시간/가용성이 개선되는 효용 변화량($\Delta U_{ij}$) 측정.
3. **Costing**: AS 전략 구현에 필요한 인건비, 인프라 비용($C_j$) 산정.
4. **BCR Calculation**: 수식 $BCR_j = B_j / C_j$ 에 의해 가장 적은 돈으로 가장 높은 가치를 주는 아키텍처 1위 선택.

$$B_j = \sum_i W_i \cdot \Delta U_{ij}, \qquad BCR_j = \frac{B_j}{C_j}$$

#### 한줄 요약

- 효용•비용 환산과 예산 내 투자 조합 결정이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **ATAM vs CBAM Comparison**: ATAM은 기술적 리스크(Risk/Tradeoff) 식별에 집중, CBAM은 그 리스크 해소를 위한 자본 투자(Cost/Benefit/ROI) 식별에 집중.

</details>

| 비교 항목 | ATAM (기술 중심 아키텍처 평가) | CBAM (경제성 중심 아키텍처 평가) |
|:---|:---|:---|
| 핵심 관점 | **기술적 품질 속성 충돌 (Tradeoff) 분석** | **IT 투자 대비 효익 (Cost / Benefit ROI) 분석** |
| 수치 정량화 | 정성적 분석 (Risk, Non-Risk, Sensitivity) | **정량적 정밀 산출 ($W_i, \Delta U_{ij}, C_j, BCR_j$)** |
| 주 주요 의사결정자 | 아키텍트, 소프트웨어 엔지니어, QA | **CIO, CFO, 기획자, 최고 경영진 (C-Level)** |
| 도출 산출물 | 위험(Risk) 항목, 절충점(Tradeoff) | **아키텍처 전략별 BCR 순위표 & 예산 집행안** |

#### 한줄 요약

- 투자 순위는 비용 편익 분석 방법, 품질 위험은 아키텍처 트레이드오프 분석 방법으로 평가한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Subjective Utility Bias**: 효용 점수나 시나리오 가중치 평가 시 개별 이해관계자의 정성적 편향(Bias)이 개입되어 수치가 왜곡되는 문제.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 주관적 효용 평가 오류 (**Subjective Utility Bias**) | **Delphi 기법 등 다수 이해관계자 무기명 투표 및 평균화** | 정량 객관성 확보 |
| 수명주기 운영 비용($C_j$) 산정 누락으로 ROI 착시 | **개발비 외 5년간의 Cloud 인프라/유지보수 TCO 비용 포함** | 수명주기 총비용 반영 |
| 여러 아키텍처 전략 간의 상호 의존성 발생 | **시너지 효과 및 공통 기반 비용 합산 보정 알고리즘 적용** | 현실적 투자 판단 |

> 사례: 대형 차세대 금융 시스템 구축 시 **ATAM 수립 후 CBAM 기반 100억 예산 분배**

#### 한줄 요약

- 범위 추정, 민감도 분석, 의존성에 기반한 투자 위험 통제가 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **CBAM 평가 수립 기준(CBAM Evaluation Standards)**: IT 프로젝트 예산 제약성, ROI 정량화 요건 및 C-Level 의사결정 체계에 의거한 체계.

</details>

- **CBAM 평가 수립 기준**에 따라 IT 아키텍처 신규 수립 시 **ATAM (기술적 상충점) $\rightarrow$ CBAM (BCR 정량 투자)** 순차 연계 수용

#### 한줄 요약

- 예산 안에서 실행 가능한 투자 조합 선택 기준이 핵심이다.
