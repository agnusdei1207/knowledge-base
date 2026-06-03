---
title: 205. 데이터 윤리 (Data Ethics) — 알고리즘 편향/공정성/투명성
date: '2026-04-21'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)

- **본질**: [[001_dikw_pyramid|데이터]] 윤리([[001_dikw_pyramid|Data]] Ethics)는 공정성(Fairness)·투명성(Transparency)·책임성(Accountability)·프라이버시(Privacy)·선익(Beneficence)의 5원칙으로 구성되며, [[190_ai_llm_requirements_specification|AI]] 시스템이 사회적 편견을 강화·증폭하지 않도록 방어하는 규범 체계다.
- **가치**: [[327_shap|SHAP]] ([[327_shap|SHapley Additive exPlanations]]), [[326_lime|LIME]] ([[326_lime|Local Interpretable Model-Agnostic Explanations]]) 등 [[227_xai_explainable_ai_lime_shap|XAI]]([[255_xai_lime_shap_explainable_contribution|Explainable AI]]) 기법과 EU [[190_ai_llm_requirements_specification|AI]] Act(2024) [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] [[104_classification_analysis|분류]] 체계가 결합하여 책임 있는 [[190_ai_llm_requirements_specification|AI]] 구현의 기술·규제 프레임워크를 형성한다.
- **판단 포인트**: [[001_algorithm_definition|알고리즘]] 편향은 [[001_dikw_pyramid|데이터]] 수집 단계(Representation [[094_bias|Bias]])에서 시작하여 모델 출력([[087_deployment_kubernetes_workload_rolling_update|Deployment]] [[094_bias|Bias]])까지 전 [[123_pipe|파이프]]라인에서 발생하므로, 편향 [[606_auditing_linux_auditd|감사]]([[094_bias|Bias]] [[363_audit|Audit]])는 일회성이 아닌 지속적 [[229_monitor|모니터]]링 프로세스여야 한다.

---

## Ⅰ. 개요 및 필요성

### [[001_algorithm_definition|알고리즘]] 편향의 현실 사례

- **COMPAS 재범 예측 시스템**: 흑인 피고인의 재범 가능성을 백인 피고인 대비 거짓 양성(False Positive)으로 2배 높게 예측 — ProPublica 2016년 조사 (Angwin et al.)
- **Amazon 채용 [[190_ai_llm_requirements_specification|AI]](2018)**: 이력서 스크리닝 AI가 여성 지원자를 불리하게 평가 — 역사적으로 IT 채용에 남성 지원자가 많았던 훈련 [[001_dikw_pyramid|데이터]] 반영
- **의료 이미지 [[190_ai_llm_requirements_specification|AI]]**: 흑인 환자 [[001_dikw_pyramid|데이터]]가 훈련 [[001_dikw_pyramid|데이터]]에서 과소 표현되어 피부 질환 진단 정확도 낮음

이처럼 [[001_algorithm_definition|알고리즘]] 편향은 **역사적 불평등을 [[001_dikw_pyramid|데이터]]에서 학습하여 더 체계적으로 재생산**하는 위험이 있다.

**📢 섹션 요약 비유**: [[001_algorithm_definition|알고리즘]] 편향은 **오래된 지도로 항해하는 것**과 같다. 과거의 편향된 현실을 반영한 [[001_dikw_pyramid|데이터]](오래된 지도)로 AI를 학습시키면, AI는 그 편향을 "정확한 사실"로 학습하여 미래에도 같은 경로(편향된 결정)를 반복한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 편향 유형별 [[190_ai_llm_requirements_specification|AI]] [[123_pipe|파이프]]라인 매핑

```
┌─────────────────────────────────────────────────────────────┐
│              AI 파이프라인 단계별 편향 유형                  │
├─────────────────────────────────────────────────────────────┤
│  [데이터 수집]                                              │
│  ■ Representation Bias (표현 편향):                         │
│    특정 그룹이 훈련 데이터에 과소/과다 표현                  │
│    예: 임상시험 데이터에 여성·고령자 부족                    │
│                                                             │
│  [데이터 전처리]                                            │
│  ■ Measurement Bias (측정 편향):                            │
│    그룹별로 다른 방식으로 데이터 측정                        │
│    예: 빈곤층 의료 데이터는 응급실 기록, 부유층은 정기검진   │
│                                                             │
│  [모델 학습]                                                │
│  ■ Aggregation Bias (집계 편향):                            │
│    다양한 그룹을 하나의 단일 모델로 처리                     │
│    예: 당뇨 진단 기준이 인종별로 다름에도 단일 모델 사용     │
│                                                             │
│  [레이블링]                                                 │
│  ■ Label Bias (레이블 편향):                                │
│    레이블링 과정에서 레이블러의 편견 반영                    │
│    예: 감정 분석 레이블에 문화적 편견 포함                   │
│                                                             │
│  [배포·운영]                                                │
│  ■ Deployment Bias (배포 편향):                             │
│    의도와 다른 환경에서 모델 사용                            │
│    예: 영어 화자용 감정 분석 모델을 비영어권에 적용          │
└─────────────────────────────────────────────────────────────┘
```

### 공정성 지표 3종

| 지표 | 정의 | 수식 | 적합 상황 |
|:---|:---|:---|:---|
| **인구통계학적 동등성** (Demographic Parity) | 그룹별 긍정 예측 비율이 동일해야 함 | P(Ŷ=1 \| A=0) = P(Ŷ=1 \| A=1) | 결과 평등 중시 |
| **동등 기회** (Equal Opportunity) | 그룹별 참 긍정률(TPR)이 동일해야 함 | TPR이 그룹 간 동일 | 자격 있는 사람에 공평한 기회 |
| **동등화된 승산** (Equalized Odds) | 그룹별 TPR과 FPR 모두 동일해야 함 | TPR + FPR 동시 동일 | 전면적 공정성 |

**📢 섹션 요약 비유**: 공정성 지표 차이는 **마라톤 대회 규칙** 차이와 같다. "모두 같은 출발선"(인구통계학적 동등성)은 결과 평등, "핸디캡 적용"(Equal Opportunity)은 능력에 따른 기회 평등 — 어떤 공정성을 추구하냐에 따라 규칙이 달라진다.

---

## Ⅲ. 비교 및 연결

### [[227_xai_explainable_ai_lime_shap|XAI]] ([[255_xai_lime_shap_explainable_contribution|Explainable AI]], 설명 가능한 [[190_ai_llm_requirements_specification|AI]]) 기법 비교

| 기법 | 범위 | 원리 | 특징 |
|:---|:---|:---|:---|
| **[[327_shap|SHAP]]** | 전역+지역 | 게임이론 Shapley Value — 각 특성의 한계 기여도 | 이론적 보장, 계산 비용 높음 |
| **[[326_lime|LIME]]** | 지역 | 예측 근방 선형 모델 근사 | 모델 무관, 빠름, 불안정 가능 |
| **Attention** | 모델 내부 | 신경망 어텐션 [[267_weight_bias_activation|가중치]] [[003_bigdata_7v|시각화]] | [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 특화 |
| **Counterfactual** | 지역 | "X를 바꾸면 결과가 달라진다" | 직관적, 실행 가능한 설명 |

### EU [[190_ai_llm_requirements_specification|AI]] Act (2024) [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] [[104_classification_analysis|분류]]

```
금지 (Prohibited)
  ├─ 사회 신용 점수 시스템
  ├─ 생체 인식 대량 감시
  └─ 무의식적 조작 AI

고위험 (High Risk) ← 규정 준수 의무 부과
  ├─ 의료 기기 AI
  ├─ 채용·교육 AI
  ├─ 신용 평가 AI
  └─ 형사 사법 AI (COMPAS 유형)

제한적 위험 (Limited Risk)
  └─ 챗봇 (사람임을 알려야 함)

최소 위험 (Minimal Risk)
  └─ 스팸 필터, 게임 AI
```

**📢 섹션 요약 비유**: EU [[190_ai_llm_requirements_specification|AI]] Act [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] [[104_classification_analysis|분류]]는 **의약품 허가 등급**과 같다. 감기약(최소 위험)은 약국에서 자유 판매지만, 항암제(고위험)는 임상시험·허가·처방전이 필요하고, 독성 화합물(금지)은 아예 판매 불가다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[001_algorithm_definition|알고리즘]] 영향 평가(Algorithmic Impact Assessment, [[194_authority_information_access_aia_ocsp|AIA]])

고위험 [[190_ai_llm_requirements_specification|AI]] 시스템 배포 전 수행해야 하는 체계적 평가:

1. **시스템 범위 정의**: [[190_ai_llm_requirements_specification|AI]] 시스템의 용도, 대상 사용자, 영향 받는 집단
2. **[[213_data_audit|데이터 감사]]**: 훈련 [[001_dikw_pyramid|데이터]]의 그룹별 표현 비율, 레이블 품질
3. **편향 테스트**: 그룹별 공정성 지표 측정 (Demographic Parity, Equal Opportunity)
4. **설명 가능성 평가**: 결정 과정이 충분히 설명 가능한가? ([[327_shap|SHAP]], [[326_lime|LIME]] 적용)
5. **[[173_stakeholder_identification_impact_matrix|이해관계자]] 검토**: 영향 받는 집단 대표자 포함 검토
6. **거버넌스 계획**: 배포 후 지속적 [[229_monitor|모니터]]링, 이의 제기 절차

### 실무에서의 Fairness-Accuracy 트레이드오프

```
Accuracy-Fairness Frontier:
  
  정확도 ↑         × (공정성·정확도 동시 최고는 이론적으로 불가)
  ↑                ×
  ↑               ×
  ↑──────────────────────→ 공정성 ↑
  
  현실적 선택:
  - 의료 AI: 공정성 > 약간의 정확도 손실 허용
  - 추천 시스템: 상업적 정확도 > 인구통계 다양성
  - 채용 AI: 법적 요건상 Equal Opportunity 필수
```

**📢 섹션 요약 비유**: Fairness-Accuracy 트레이드오프는 **두 줄 타기**와 같다. 오른쪽(정확도)으로 기울면 왼쪽(공정성)이 낮아지고, 왼쪽으로 기울면 오른쪽이 낮아진다. 줄 위에서 균형을 잡는 것이 설계자의 역할이다.

---

## Ⅴ. 기대효과 및 결론

### [[001_dikw_pyramid|데이터]] 윤리 내재화 기대효과

| 영역 | 효과 |
|:---|:---|
| **법적 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]** | EU [[190_ai_llm_requirements_specification|AI]] Act 위반 과징금(최대 매출 7%) 예방 |
| **사회적 신뢰** | 편향 없는 AI로 브랜드 [[085_confidence_association_rule_conditional_probability|신뢰도]]·ESG 점수 향상 |
| **의사결정 품질** | 다양한 사용자에게 공정하게 작동하는 견고한 모델 |
| **책임 추적** | [[606_auditing_linux_auditd|감사]] 추적·XAI로 결정 근거 사후 [[395_verification_process_review|검증]] 가능 |

### 결론

[[001_dikw_pyramid|데이터]] 윤리는 더 이상 "좋으면 좋고, 없어도 그만인" 선택 사항이 아니다. EU [[190_ai_llm_requirements_specification|AI]] Act, [[791_gdpr_eu|GDPR]] Article 22(자동화된 의사결정 이의 제기권), 각국 [[190_ai_llm_requirements_specification|AI]] 윤리 가이드라인이 법적 의무로 전환되고 있다. 정보통신기술사는 [[190_ai_llm_requirements_specification|AI]] 시스템 설계 시 편향 [[606_auditing_linux_auditd|감사]] 프로세스, [[227_xai_explainable_ai_lime_shap|XAI]] [[192_module_independence|모듈]], 인간 개입(Human-in-the-Loop) 설계를 핵심 아키텍처 요소로 반영해야 한다.

**📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 윤리를 내재화한 AI는 **교통 [[130_signal|신호]]등**과 같다. 공정하게 모든 방향에 동등한 기회를 주고, 작동 이유를 명확히 표시하며(투명성), 오작동 시 사람이 개입할 수 있도록 설계되어야 한다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| Representation [[094_bias|Bias]] | 편향 유형 | [[001_dikw_pyramid|데이터]] 수집 단계의 그룹 과소 표현 |
| Demographic Parity | 공정성 지표 | 그룹별 긍정 예측 비율 동일 요건 |
| [[327_shap|SHAP]] | [[227_xai_explainable_ai_lime_shap|XAI]] 기법 | Shapley Value 기반 특성 기여도 설명 |
| [[326_lime|LIME]] | [[227_xai_explainable_ai_lime_shap|XAI]] 기법 | 지역 선형 근사 기반 모델 무관 설명 |
| EU [[190_ai_llm_requirements_specification|AI]] Act | 규제 프레임워크 | [[190_ai_llm_requirements_specification|AI]] 시스템 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] [[104_classification_analysis|분류]] 및 의무 규정 |
| Algorithmic Impact Assessment | 거버넌스 도구 | 고위험 [[190_ai_llm_requirements_specification|AI]] 배포 전 의무적 위험 평가 |
| Human-in-the-Loop | 설계 원칙 | 고위험 결정에 인간 검토 단계 포함 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 수집 단계 — 표현 편향 (Representation Bias) 내재]
    │
    ▼
[AI 모델 훈련 — 편향 학습 및 증폭]
    │
    ▼
[XAI (설명 가능 AI — SHAP/LIME) — 의사결정 근거 투명화]
    │
    ▼
[공정성 지표 (Fairness Metrics) — Demographic Parity 등]
    │
    ▼
[EU AI Act / 알고리즘 영향 평가 (AIA) — 법적 의무화]
```
[[001_dikw_pyramid|데이터]] 편향은 수집 단계에서 시작해 모델 훈련을 통해 증폭되며, XAI로 투명성을 확보하고 공정성 지표 [[395_verification_process_review|검증]]을 거쳐 EU [[190_ai_llm_requirements_specification|AI]] Act 같은 규제 의무 이행까지 이어지는 전주기 거버넌스가 필요하다.

### 👶 어린이를 위한 3줄 비유 설명

- AI가 편향되는 것은 **인종차별적인 선생님에게 배운 학생**과 같아요: 선생님의 편견(편향된 훈련 [[001_dikw_pyramid|데이터]])을 학생([[190_ai_llm_requirements_specification|AI]])이 그대로 배워서 더 체계적으로 차별할 수 있어요.
- [[227_xai_explainable_ai_lime_shap|XAI]](설명 가능한 [[190_ai_llm_requirements_specification|AI]])는 AI가 "왜 이 결정을 했는지" 알려주는 것이에요 — "이 사람이 대출 거절된 이유는 신용점수가 낮아서"라고 설명해 줘야 억울하지 않잖아요.
- EU [[190_ai_llm_requirements_specification|AI]] Act는 AI도 자동차처럼 **안전 검사 의무**가 있다는 규칙이에요: 생명에 영향 주는 [[190_ai_llm_requirements_specification|AI]](의료·채용·사법)는 출시 전 엄격한 공정성 검사를 받아야 해요.
