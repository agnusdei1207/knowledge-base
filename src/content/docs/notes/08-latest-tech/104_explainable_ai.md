---
sidebar:
  order: 104
  label: "104. Explainable AI (설명 가능한 AI)"
  badge:
    text: "기출 · 60%"
    variant: note
title: "Explainable AI (설명 가능한 AI)"
date: "2026-09-07T16:00:00+09:00"
tags:
  - "notes-latest-tech"
weight: 104
extra:
  question_no: "104"
  source_status: "기출"
  source_history: "122회, 135회"
  priority: 60
  priority_note: "설명 가능성과 신뢰성 확보가 반복 출제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **설명 가능한 인공지능(Explainable Artificial Intelligence, XAI)**: 블랙박스 AI 모델의 복잡한 예측 및 의사결정 이유를 인간이 이해하고 신뢰할 수 있는 형태로 해석·제공하는 기술.
- **판단 근거(Rationale)**: 특정 출력 결과에 결정적인 영향을 부여한 입력 특성(Feature), 결정 규칙, 가중치 기여도 등의 해석 정보.

</details>

- 정의: AI 판단 근거를 이해•검증 가능하게 제공하는 **XAI**이다.
- 배경/필요성: 딥러닝 신경망, 앙상블 트리, 거대 언어 모델(LLM) 등 현대 고성능 AI 모델은 수억~수조 개의 파라미터로 구성된 복잡한 블랙박스(Black-box) 구조를 지니고 있어, 금융 대출 심사, 의료 진단, 자율주행, 채용 등 고위험 의사결정에서 "왜 이러한 예측 결과를 도출했는가"에 대한 논리적 인과관계를 설명하지 못해 규제 준수(설명요구권: GDPR, EU AI Act) 실패 및 치명적 판단 오류 검증 불가의 한계에 직면함에 따라, 블랙박스 모델의 내부 표현을 해석하거나 사후(Post-hoc) 대리 모델을 통해 개별 예측 및 전체 모델의 판단 근거를 인간이 이해할 수 있는 특성 기여도, 규칙, 히트맵 형태로 제공하는 설명 가능한 AI(Explainable AI: XAI / LIME, SHAP, Integrated Gradients, Grad-CAM, Counterfactual Explanations) 기술을 도입하여 **복잡한 AI 예측에 대한 투명한 판단 근거(Feature Attribution) 산출 및 모델의 디버깅/편향 감지 능력 획득, 고위험 의사결정에 대한 사용자 신뢰 및 법적 설명요구권 충족, 정확도(Accuracy)와 설명 가능성(Explainability) 간의 공학적 최적 절충 체계 확립**을 달성할 필요

#### 한줄 요약
- **규칙•특징•사례** 기반 모델 판단 근거 제공

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **사후 설명(Post-hoc Explanation)**: 학습이 완료된 임의의 복잡한 블랙박스 모델 외부에 별도의 해석 알고리즘을 적용하여 근거를 추정하는 기법.
- **충실도(Fidelity)**: 도출된 설명 모델이 원본 블랙박스 모델의 실제 예측 논리를 얼마나 왜곡 없이 정확하게 반영하는지를 나타내는 척도.
- **안정성(Stability)**: 유사한 입력 데이터에 대해 설명 결과가 불필요하게 급변하지 않고 일관성을 유지하는 성질.

</details>

- 모델 자체 해석과 **사후 설명** 구분
- 개별 출력의 국소 설명과 **전역 설명** 구분
- 충실도•안정성•이해도와 **보증 한계** 평가

#### 한줄 요약
- **설명 방식•범위•충실도•안정성•보증 한계** 구분

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **설명 범위(Explanation Scope)**: 단일 인스턴스 예측에 대한 국소적 설명(Local)과 모델 전체 동작 논리에 대한 전역적 설명(Global).
- **설명 산출물(Explanation Artifact)**: 특성 중요도(Feature Importance), 부분 의존도 플롯(PDP), 결정 트리, 반사실적 설명(Counterfactuals).
- **품질 평가(Quality Evaluation)**: 설명의 충실도, 안정성, 계산 복잡도, 사용자 이해도를 종합 검증하는 평가 체계.

</details>

```text
[Explainable AI Architecture]
├── [설명 대상 및 범위 정의]
│   ├── [설명 대상 모델 (Target Model)]
│   └── [설명 범위 (Local & Global)]
├── [설명 생성 엔진]
│   └── [설명 기법 (XAI Method)]
└── [해석 및 검증 계층]
    ├── [설명 산출물 (Explanation)]
    └── [품질 평가 (Fidelity Eval)]
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 설명 대상 모델 | 동작•출력 근거를 분석할 **AI 시스템** |
| 설명 범위 | **개별 출력•전체 모델** 중 범위 |
| 설명 기법 | **규칙•기여도•사례** 산출 방법 |
| 설명 산출물 | 사용자 역할•목적별 **근거 표현** |
| 품질 평가 | **충실도•안정성•이해도** 판정 |

#### 한줄 요약
- **대상 모델•범위•기법•산출물•품질 평가** 구성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **설명 대상 식별(Target Identification)**: 해석할 AI 모델과 특정 예측 샘플 및 설명 요구사항을 정의하는 단계.
- **설명 기법 적용(XAI Method Application)**: SHAP, LIME, Grad-CAM 등의 대리 모델(Surrogate) 또는 기여도 분석을 수행하는 단계.
- **설명 산출 및 해석(Generation & Interpretation)**: 산출된 특성 기여도와 히트맵을 시각화하고 최종 사용자에게 설명 근거를 전달하는 단계.

</details>

```text
설명 사용자 ── 입력•목적•범위 ──▶ 설명 대상 모델
                                       │ 1. 예측•모델 정보 수집
                                       ▼
                                    설명 기법
                                       │ 2. 판단 근거 산출
                                       │ 3. 설명 품질 평가
                                       ▼
                                   품질 평가자
                                       └── 설명•품질•한계 ──▶ 설명 사용자
```

### 동작 원리

1. 예측•모델 정보 수집: 설명용 입력•출력•내부 정보 확보
2. 판단 근거 산출: 목적에 맞는 **기여도•규칙•사례** 표현
3. 설명 품질 평가: **충실도•안정성•이해도**와 한계 판정

#### 한줄 요약
- **정보 수집•근거 산출•설명 품질 평가** 수행

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **국소 설명(Local Explanation)**: 특정 고객 대출 거절 이유 등 개별 예측 인스턴스의 판단 근거를 설명하는 방식(LIME, SHAP).
- **전역 설명(Global Explanation)**: 모델 전체가 학습한 전반적인 특성 간 관계와 의사결정 경계를 거시적으로 설명하는 방식(Global Surrogate, PDP).

</details>

| 설명 범위 | 국소 설명 | 전역 설명 |
|:---|:---|:---|
| 적용 기준 | 개별 결정 검토•이의제기 | 모델 선택•편향 조사•감시 |
| 핵심 특징 | 특정 예측의 특징 기여 | 전체 모델의 평균 동작 |
| 한계 | 다른 입력으로 일반화 불가 | 개별 예측 세부 누락 |

#### 한줄 요약
- **개별 결정•전체 모델 동작** 대상에 따른 설명 범위 구분

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **충실도 불일치(Fidelity Mismatch)**: 사후 설명 대리 모델의 단순화로 인한 원본 모델과의 해석 왜곡 위험을 줄이기 위해 적정 근사 반경 설정.
- **설명 변조 공격(Adversarial Explanation Attack)**: 적대적 섭동을 통해 예측값은 유지하면서 설명 결과만 조작하는 공격에 대비한 설명 안정성 검증.
- **해석 적합성(Cognitive Usability)**: 개발자용 세부 가중치와 일반 사용자용 직관적 이유를 분리하여 사용자 눈높이에 맞는 설명 제공.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 설명과 원모델 판단의 **충실도 불일치** | 삭제•교란 기반 충실도 검증 | 설명의 **판단 근거성** 확보 |
| 작은 입력 변화로 **설명 불안정** | 반복•근방 표본의 설명 일관성 측정 | 국소 설명 **재현성 향상** |

#### 한줄 요약
- **충실도•안정성•이해도•재현성•보증 한계** 검증

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **신뢰성과 투명성 기반의 책임 있는 인공지능(Responsible AI Trust & Transparency)**: 정확도와 설명 가능성 간의 균형을 최적화하여 고위험 AI 도메인(의료, 금융, 사법)에서 투명성과 사회적 수용성을 확보하는 핵심 기술.

</details>

- 블랙박스 인공지능의 불투명성을 해소하고 인간 전문가와 AI 간의 협력적 신뢰를 구축하며 글로벌 고위험 AI 규제의 핵심 요건을 만족시키는 **신뢰할 수 있는 인공지능(Trustworthy AI) 및 공학적 검증의 최고 핵심 기술(Explainable AI / Post-hoc & Intrinsic Methods / Local & Global Explanations / SHAP Shapley Values & LIME Perturbation / Visual Saliency & Counterfactuals / Regulatory Explainability Compliance)의 확고한 표준**으로 확고히 자리 잡았으며, LLM의 사고의 사슬(Chain-of-Thought) 및 메커니즘 해석학(Mechanistic Interpretability)으로 심화 발전하는 가운데, 실무 XAI 솔루션 구축 시에는 **개별 사용자의 이의제기 대응에는 게임이론 기반의 공정하고 일관된 특성 기여도를 보장하는 SHAP/LIME 국소 설명을 적용하고, 전사 모델 편향 감사에는 부분 의존도 플롯(PDP) 기반 전역 설명을 채택하며, 적대적 설명 조작 공격(Adversarial Explanation Attack)에 대비한 설명의 충실도(Fidelity) 및 안정성 검증**을 결합하여 완벽한 해석 신뢰성과 엔터프라이즈 규제 부합성을 완성

#### 한줄 요약
- **사용자•목적•범위**에 따라 국소•전역 설명 결정
