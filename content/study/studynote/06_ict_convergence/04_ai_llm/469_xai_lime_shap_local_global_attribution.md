+++
weight = 469
title = "469. XAI, LIME, SHAP: 국소/전역 기여도 해석 (XAI LIME SHAP Local Global Attribution)"
date = "2026-05-09"
[extra]
categories = "studynote-ict-convergence"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[227_xai_explainable_ai_lime_shap|XAI]]([[255_xai_lime_shap_explainable_contribution|eXplainable AI]], 설명 가능한 [[190_ai_llm_requirements_specification|AI]])는 블랙박스 모델의 예측 근거를 인간이 이해할 수 있는 언어로 번역하는 기술이다.
> 2. **가치**: [[326_lime|LIME]](Local Interpretable Model-agnostic Explanations)은 개별 예측을, [[327_shap|SHAP]]([[327_shap|SHapley Additive exPlanations]])은 게임 이론으로 각 [[247_feature_label_variables|피처]]의 공정한 기여도를 산출한다.
> 3. **판단 포인트**: EU [[190_ai_llm_requirements_specification|AI]] Act 등 규제 환경에서 의료·금융·법적 의사결정 시스템은 설명 가능성이 법적 의무이므로 [[227_xai_explainable_ai_lime_shap|XAI]] 기법 선택이 시스템 설계의 핵심 조건이다.

---

## Ⅰ. 개요 및 필요성

딥러닝 모델은 높은 [[282_performance_tactics|성능]]을 제공하지만, 수억 개의 파라미터로 이루어진 의사결정 과정은 인간에게 불투명하다. 이를 "블랙박스(Black Box)" 문제라 한다.

**[[227_xai_explainable_ai_lime_shap|XAI]] 필요성**
- **신뢰(Trust)**: 의사/법관이 [[190_ai_llm_requirements_specification|AI]] 판단을 수용하려면 근거가 필요하다
- **디버깅(Debugging)**: 모델이 잘못된 특징(Feature)을 학습했는지 탐지
- **규제 준수**: EU [[190_ai_llm_requirements_specification|AI]] Act, GDPR의 "설명을 요청할 권리(Right to Explanation)"
- **공정성(Fairness)**: 인종·성별 등 민감 속성에 의한 편향 탐지

**해석 범위**
- **전역(Global) 해석**: 전체 모델 동작 이해 → [[247_feature_label_variables|피처]] 중요도([[355_random_forest_feature_importance|Feature Importance]])
- **국소(Local) 해석**: 특정 예측 한 건에 대한 근거 → [[326_lime|LIME]], [[327_shap|SHAP]] 개별 예측

- **📢 섹션 요약 비유**: 블랙박스 AI는 "정답은 A야"라고만 말하는 판사이고, XAI는 "왜냐하면 나이가 45세 이상이고 콜레스테롤이 높기 때문이야"라고 판결문을 써주는 판사다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
원본 예측
    │
    ├─── LIME ────► 국소 선형 근사 ──► "이 예측에서 X₁가 +0.3 기여"
    │               (Perturbation 샘플링)
    │
    └─── SHAP ────► 섀플리값 계산 ───► "전체 평균 대비 X₂가 -0.15 기여"
                    (연합 게임 이론)
```

**[[326_lime|LIME]] 작동 원리**
1. 예측하려는 샘플 x 주변에 약한 변형(Perturbation) 샘플 [[087_process_state_transition|생성]]
2. 블랙박스 모델로 각 변형 샘플의 예측값 획득
3. x에 가까울수록 높은 [[267_weight_bias_activation|가중치]] 부여
4. [[267_weight_bias_activation|가중치]] 적용 선형 모델(Ridge Regression) 학습 → 계수가 각 [[247_feature_label_variables|피처]] 기여도

**[[327_shap|SHAP]] 작동 원리**
게임 이론의 섀플리 값(Shapley Value): 협동 게임에서 각 플레이어의 공정한 기여도를 모든 가능한 연합 순서의 평균으로 계산.

$$\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F|-|S|-1)!}{|F|!}[f(S \cup \{i\}) - f(S)]$$

### [[326_lime|LIME]] vs [[327_shap|SHAP]] 비교

| 항목 | [[326_lime|LIME]] | [[327_shap|SHAP]] |
|:---:|:---:|:---:|
| 이론 기반 | 국소 선형 근사 | 게임 이론(Shapley Value) |
| [[194_consistency_database_integrity|일관성]] 보장 | ✗ (불안정) | ✓ (공리 보장) |
| 계산 비용 | 낮음 | 높음(TreeSHAP 제외) |
| 전역 해석 | ✗ | ✓ ([[327_shap|SHAP]] 집계) |
| 주요 구현 | [[326_lime|lime]] [[336_library_vs_framework|라이브러리]] | [[327_shap|shap]] [[336_library_vs_framework|라이브러리]] |

- **📢 섹션 요약 비유**: LIME은 "이 동네 지형만 대충 측량"하고, SHAP은 "나라 전체 토지 공정 분배 원칙"으로 계산한다.

---

## Ⅲ. 비교 및 연결

### 모델 종류에 따른 [[327_shap|SHAP]] 최적화

| 모델 | [[327_shap|SHAP]] [[001_algorithm_definition|알고리즘]] | 복잡도 |
|:---:|:---:|:---:|
| Tree 계열(XGBoost, LightGBM) | TreeSHAP | O(TLD²) - 빠름 |
| 딥러닝 | DeepSHAP, GradientSHAP | 근사 |
| 선형 모델 | LinearSHAP | 정확, 빠름 |
| 임의 모델 | KernelSHAP | 느림 |

**전역 해석 방법**
- **Permutation [[355_random_forest_feature_importance|Feature Importance]]**: [[247_feature_label_variables|피처]] 값 섞었을 때 [[282_performance_tactics|성능]] 하락 측정
- **Partial Dependence Plot(PDP)**: 단일 [[247_feature_label_variables|피처]]와 예측값 [[083_relationship_in_er_model|관계]] [[003_bigdata_7v|시각화]]
- **[[327_shap|SHAP]] [[300_summary|Summary]] Plot**: 전체 샘플의 [[327_shap|SHAP]] 값 분포 [[003_bigdata_7v|시각화]]

- **📢 섹션 요약 비유**: 국소 해석은 "오늘 이 환자가 왜 위험한가"이고, 전역 해석은 "우리 병원 AI가 어떤 증상을 가장 중요하게 보는가"이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**적용 [[064_relation_domain|도메인]]**

1. **의료**: 암 진단 모델 → 어떤 유전자 마커가 양성 예측에 기여했는지 의사에게 제공
2. **신용 대출**: 대출 거절 시 "소득 수준(-0.8), 연체 이력(-1.2)"으로 거절 사유 고객 통보
3. **자율주행**: 급제동 판단 시 "보행자 감지(+2.1)"가 주요 원인임을 로그로 기록

**기술사 판단 포인트**

- **[[326_lime|LIME]] 단점**: 샘플링 노이즈로 동일 입력에 다른 설명 가능 → 의료처럼 [[194_consistency_database_integrity|일관성]] 중요한 분야엔 [[327_shap|SHAP]] 권장
- **TreeSHAP**: 트리 기반 모델에서 정확하고 빠른 [[327_shap|SHAP]] — 금융 스코어링에 실질적 선택지
- **EU [[190_ai_llm_requirements_specification|AI]] Act 고위험 시스템**: Level 3(고위험)은 설명 가능성 문서화 의무 → [[227_xai_explainable_ai_lime_shap|XAI]] 리포트 자동화 파이프라인 구축 필요

- **📢 섹션 요약 비유**: AI가 "너는 대출 불가"라고만 하면 억울하지만, "소득이 부족해서(-70%), 연체 이력 때문에(-30%)"라고 하면 납득할 수 있다.

---

## Ⅴ. 기대효과 및 결론

XAI는 AI의 [[282_performance_tactics|성능]]과 신뢰를 동시에 달성하는 다리 역할을 한다. LIME은 빠른 국소 설명, SHAP은 이론적으로 엄밀한 기여도 분해를 제공한다. 규제 강화 트렌드와 [[190_ai_llm_requirements_specification|AI]] 윤리 요구 속에서 XAI는 선택이 아닌 필수 엔지니어링 요소가 되고 있다.

향후 [[263_llm_large_language_model|LLM]] 해석을 위한 Attention [[267_weight_bias_activation|가중치]] 분석, Probing 기법과 XAI의 통합이 중요 연구 방향이다.

- **📢 섹션 요약 비유**: XAI는 AI에게 "네가 왜 그렇게 판단했는지 설명해봐"라고 요구하는 책임감 교육이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[326_lime|LIME]] | [[227_xai_explainable_ai_lime_shap|XAI]] 국소 · 국소 선형 근사 설명 |
| [[327_shap|SHAP]] | [[227_xai_explainable_ai_lime_shap|XAI]] 국소/전역 · 게임 이론 기반 공정 기여도 |
| Shapley Value | [[327_shap|SHAP]] 기반 · 협동 게임 이론 |
| [[355_random_forest_feature_importance|Feature Importance]] | 전역 해석 · 전체 모델 수준 [[247_feature_label_variables|피처]] 기여도 |
| EU [[190_ai_llm_requirements_specification|AI]] Act | 규제 · [[227_xai_explainable_ai_lime_shap|XAI]] 법적 의무화 근거 |

### 📈 관련 키워드 및 발전 흐름도

```text
[XAI 국소 · 국소 선형 근사 설명] → [XAI · LIME] → [규제 · XAI 법적 의무화 근거]
```

### 👶 어린이를 위한 3줄 비유 설명

1. AI가 "이 사람은 병에 걸릴 것 같아요"라고 할 때, 왜 그렇게 생각하는지 이유를 알려주는 것이 XAI예요.
2. LIME은 "이 환자 주변 사람들을 조금씩 바꿔보며" 이유를 찾고, SHAP은 "모든 가능한 조합을 공평하게 계산해서" 이유를 찾아요.
3. AI가 공평하고 설명 가능해야 사람들이 믿고 쓸 수 있어요.
