---
sidebar:
  order: 72
  label: "072. CBAM 비용 편익 분석 방법 (Cost Benefit Analysis Method)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "CBAM 비용 편익 분석 방법 (Cost Benefit Analysis Method)"
date: "2026-08-13T17:26:00+09:00"
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
- 배경/필요성: 기술 위험만으로는 **예산 내 투자 우선순위** 결정 불가

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

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Architectural Strategy (AS, 아키텍처 전략)**: 품질 속성 요구를 충족시키기 위해 아키텍터가 제안한 디자인 패턴, 아키텍처 스타일 및 기술 요소 결정.

</details>

```text
 [품질 응답] ─── [응답 측정값]
      │                 │
 [시나리오 가중치] ─ [수명주기 비용]
```

선의 의미: ATAM에서 도출된 시나리오와 아키텍처 전략(AS)을 수거하여 가중치 $W_i$, 효용 변화량 $\Delta U_{ij}$, 개발비용 $C_j$를 대입 후 BCR을 산출하는 체계.

| 구성요소 | 책임 |
|:---|:---|
| 품질 응답 | 전략 적용 전후 시스템 동작 정의 |
| 응답 측정값 | 품질 개선량을 효용 함수의 입력으로 제공 |
| 시나리오 가중치 | 품질 시나리오의 상대적 사업 가치 표현 |
| 수명주기 비용 | 구현•운영•전환•폐기 비용 포함 |

#### 한줄 요약

- 품질 응답, 응답 측정값, 시나리오 가중치, 수명주기 비용의 평가 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **CBAM 9 Step Process**: 1. 시나리오 정제 $\rightarrow$ 2. 아키텍처 전략(AS) 도출 $\rightarrow$ 3. 효용 수치 산정 $\rightarrow$ 4. 시나리오 가중치 할당 $\rightarrow$ 5. 효익 계산 $\rightarrow$ 6. 비용 계산 $\rightarrow$ 7. BCR 계산 $\rightarrow$ 8. 우선순위 결정 $\rightarrow$ 9. 투자 확정.

</details>

```text
┌──────────────────────────────┐
│ ATAM 시나리오 정제           │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 시나리오•전략 정제        │
│ 2. 효용•가중치 산정          │
│ 3. 수명주기 비용 산정        │
│ 4. 효익•비용 환산            │
│ 5. 예산 내 투자 조합 결정    │
└──────────────┬───────────────┘
               ▼
 [BCR 순위별 아키텍처 예산 집행]
```

### 동작 원리

1. **시나리오•전략 정제**: 품질 시나리오와 실행 대안 구체화.
2. **효용•가중치 산정**: 응답 변화의 사업 가치와 중요도 평가.
3. **수명주기 비용 산정**: 구현•운영•전환 비용 범위 추정.
4. **효익•비용 환산**: 가중 효익과 비용 대비 가치 계산.
5. **예산 내 투자 조합 결정**: 의존성•불확실성을 반영해 선택.

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
| 수치 정량화 | 품질 시나리오 기반 위험•절충 분석 | **효용•비용 추정에 기반한 상대 가치 산출** |
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
| 운영•전환 비용 누락으로 ROI 착시 | **분석 기간의 인프라•유지보수•폐기 비용** 포함 | 수명주기 총비용 반영 |
| 여러 아키텍처 전략 간의 상호 의존성 발생 | **시너지 효과 및 공통 기반 비용 합산 보정 알고리즘 적용** | 현실적 투자 판단 |

> 사례: 대형 차세대 금융 시스템 구축 시 **ATAM 수립 후 CBAM 기반 100억 예산 분배**

#### 한줄 요약

- 범위 추정, 민감도 분석, 의존성에 기반한 투자 위험 통제가 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **CBAM 평가 수립 기준(CBAM Evaluation Standards)**: IT 프로젝트 예산 제약성, ROI 정량화 요건 및 C-Level 의사결정 체계에 의거한 체계.

</details>

- 품질 위험은 **ATAM**, 예산 내 투자 조합은 **CBAM**으로 순차 판단

#### 한줄 요약

- 예산 안에서 실행 가능한 투자 조합 선택 기준이 핵심이다.
