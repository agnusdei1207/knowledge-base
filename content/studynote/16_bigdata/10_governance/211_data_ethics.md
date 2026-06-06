---
title: "211. Data Ethics"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
---

## 핵심 인사이트 (3줄 요약)

- **본질**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 윤리([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Ethics)는 공정성(Fairness)·투명성(Transparency)·책임성(Accountability)·프라이버시(Privacy)·선익(Beneficence)의 5원칙으로 구성되며, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템이 사회적 편견을 강화·증폭하지 않도록 방어하는 규범 체계다.
- **가치**: [SHAP](/studynote/10_ai/04_ai_ops_ethics/327_shap/) ([SHapley Additive exPlanations](/studynote/10_ai/04_ai_ops_ethics/327_shap/)), [LIME](/studynote/10_ai/04_ai_ops_ethics/326_lime/) ([Local Interpretable Model-Agnostic Explanations](/studynote/10_ai/04_ai_ops_ethics/326_lime/)) 등 [XAI](/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/)([Explainable AI](/studynote/14_data_engineering/05_exam_keywords/255_xai_lime_shap_explainable_contribution/)) 기법과 EU [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Act(2024) [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계가 결합하여 책임 있는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 구현의 기술·규제 프레임워크를 형성한다.
- **판단 포인트**: [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 편향은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집 단계(Representation [Bias](/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/))에서 시작하여 모델 출력([Deployment](/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/) [Bias](/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/))까지 전 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 발생하므로, 편향 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)([Bias](/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/) [Audit](/studynote/12_it_management/05_security_compliance/363_audit/))는 일회성이 아닌 지속적 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 프로세스여야 한다.

---

## Ⅰ. 개요 및 필요성

### [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 편향의 현실 사례

- **COMPAS 재범 예측 시스템**: 흑인 피고인의 재범 가능성을 백인 피고인 대비 거짓 양성(False Positive)으로 2배 높게 예측 — ProPublica 2016년 조사 (Angwin et al.)
- <strong>Amazon 채용 <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a>(2018)</strong>: 이력서 스크리닝 AI가 여성 지원자를 불리하게 평가 — 역사적으로 IT 채용에 남성 지원자가 많았던 훈련 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 반영
- <strong>의료 이미지 <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a></strong>: 흑인 환자 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 훈련 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 과소 표현되어 피부 질환 진단 정확도 낮음

이처럼 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 편향은 <strong>역사적 불평등을 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>에서 학습하여 더 체계적으로 재생산</strong>하는 위험이 있다.

**📢 섹션 요약 비유**: [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 편향은 <strong>오래된 지도로 항해하는 것</strong>과 같다. 과거의 편향된 현실을 반영한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(오래된 지도)로 AI를 학습시키면, AI는 그 편향을 "정확한 사실"로 학습하여 미래에도 같은 경로(편향된 결정)를 반복한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 편향 유형별 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 매핑

```
+-------------------------------------------------------------+
|              AI 파이프라인 단계별 편향 유형                  |
+-------------------------------------------------------------+
|  [데이터 수집]                                              |
|  ■ Representation Bias (표현 편향):                         |
|    특정 그룹이 훈련 데이터에 과소/과다 표현                  |
|    예: 임상시험 데이터에 여성·고령자 부족                    |
|                                                             |
|  [데이터 전처리]                                            |
|  ■ Measurement Bias (측정 편향):                            |
|    그룹별로 다른 방식으로 데이터 측정                        |
|    예: 빈곤층 의료 데이터는 응급실 기록, 부유층은 정기검진   |
|                                                             |
|  [모델 학습]                                                |
|  ■ Aggregation Bias (집계 편향):                            |
|    다양한 그룹을 하나의 단일 모델로 처리                     |
|    예: 당뇨 진단 기준이 인종별로 다름에도 단일 모델 사용     |
|                                                             |
|  [레이블링]                                                 |
|  ■ Label Bias (레이블 편향):                                |
|    레이블링 과정에서 레이블러의 편견 반영                    |
|    예: 감정 분석 레이블에 문화적 편견 포함                   |
|                                                             |
|  [배포·운영]                                                |
|  ■ Deployment Bias (배포 편향):                             |
|    의도와 다른 환경에서 모델 사용                            |
|    예: 영어 화자용 감정 분석 모델을 비영어권에 적용          |
+-------------------------------------------------------------+
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

### [XAI](/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/) ([Explainable AI](/studynote/14_data_engineering/05_exam_keywords/255_xai_lime_shap_explainable_contribution/), 설명 가능한 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)) 기법 비교

| 기법 | 범위 | 원리 | 특징 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/327_shap/">SHAP</a></strong> | 전역+지역 | 게임이론 Shapley Value — 각 특성의 한계 기여도 | 이론적 보장, 계산 비용 높음 |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/326_lime/">LIME</a></strong> | 지역 | 예측 근방 선형 모델 근사 | 모델 무관, 빠름, 불안정 가능 |
| **Attention** | 모델 내부 | 신경망 어텐션 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/) | [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 특화 |
| **Counterfactual** | 지역 | "X를 바꾸면 결과가 달라진다" | 직관적, 실행 가능한 설명 |

### EU [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Act (2024) [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)

```
금지 (Prohibited)
  +- 사회 신용 점수 시스템
  +- 생체 인식 대량 감시
  +- 무의식적 조작 AI

고위험 (High Risk) <- 규정 준수 의무 부과
  +- 의료 기기 AI
  +- 채용·교육 AI
  +- 신용 평가 AI
  +- 형사 사법 AI (COMPAS 유형)

제한적 위험 (Limited Risk)
  +- 챗봇 (사람임을 알려야 함)

최소 위험 (Minimal Risk)
  +- 스팸 필터, 게임 AI
```

**📢 섹션 요약 비유**: EU [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Act [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)는 <strong>의약품 허가 등급</strong>과 같다. 감기약(최소 위험)은 약국에서 자유 판매지만, 항암제(고위험)는 임상시험·허가·처방전이 필요하고, 독성 화합물(금지)은 아예 판매 불가다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 영향 평가(Algorithmic Impact Assessment, [AIA](/studynote/09_security/04_endpoint_security/194_authority_information_access_aia_ocsp/))

고위험 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템 배포 전 수행해야 하는 체계적 평가:

1. **시스템 범위 정의**: [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템의 용도, 대상 사용자, 영향 받는 집단
2. <strong><a href="/studynote/16_bigdata/10_governance/213_data_audit/">데이터 감사</a></strong>: 훈련 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 그룹별 표현 비율, 레이블 품질
3. **편향 테스트**: 그룹별 공정성 지표 측정 (Demographic Parity, Equal Opportunity)
4. **설명 가능성 평가**: 결정 과정이 충분히 설명 가능한가? ([SHAP](/studynote/10_ai/04_ai_ops_ethics/327_shap/), [LIME](/studynote/10_ai/04_ai_ops_ethics/326_lime/) 적용)
5. <strong><a href="/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/">이해관계자</a> 검토</strong>: 영향 받는 집단 대표자 포함 검토
6. **거버넌스 계획**: 배포 후 지속적 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링, 이의 제기 절차

### 실무에서의 Fairness-Accuracy 트레이드오프

```
Accuracy-Fairness Frontier:

  정확도 ^         × (공정성·정확도 동시 최고는 이론적으로 불가)
  ^                ×
  ^               ×
  ^-----------------------> 공정성 ^

  현실적 선택:
  - 의료 AI: 공정성 > 약간의 정확도 손실 허용
  - 추천 시스템: 상업적 정확도 > 인구통계 다양성
  - 채용 AI: 법적 요건상 Equal Opportunity 필수
```

**📢 섹션 요약 비유**: Fairness-Accuracy 트레이드오프는 <strong>두 줄 타기</strong>와 같다. 오른쪽(정확도)으로 기울면 왼쪽(공정성)이 낮아지고, 왼쪽으로 기울면 오른쪽이 낮아진다. 줄 위에서 균형을 잡는 것이 설계자의 역할이다.

---

## Ⅴ. 기대효과 및 결론

### [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 윤리 내재화 기대효과

| 영역 | 효과 |
|:---|:---|
| <strong>법적 <a href="/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">리스크</a></strong> | EU [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Act 위반 과징금(최대 매출 7%) 예방 |
| **사회적 신뢰** | 편향 없는 AI로 브랜드 [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)·ESG 점수 향상 |
| **의사결정 품질** | 다양한 사용자에게 공정하게 작동하는 견고한 모델 |
| **책임 추적** | [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적·XAI로 결정 근거 사후 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능 |

### 결론

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 윤리는 더 이상 "좋으면 좋고, 없어도 그만인" 선택 사항이 아니다. EU [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Act, [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) Article 22(자동화된 의사결정 이의 제기권), 각국 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 윤리 가이드라인이 법적 의무로 전환되고 있다. 정보통신기술사는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템 설계 시 편향 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 프로세스, [XAI](/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/) [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/), 인간 개입(Human-in-the-Loop) 설계를 핵심 아키텍처 요소로 반영해야 한다.

**📢 섹션 요약 비유**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 윤리를 내재화한 AI는 <strong>교통 <a href="/studynote/02_operating_system/02_process_thread/130_signal/">신호</a>등</strong>과 같다. 공정하게 모든 방향에 동등한 기회를 주고, 작동 이유를 명확히 표시하며(투명성), 오작동 시 사람이 개입할 수 있도록 설계되어야 한다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| Representation [Bias](/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/) | 편향 유형 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집 단계의 그룹 과소 표현 |
| Demographic Parity | 공정성 지표 | 그룹별 긍정 예측 비율 동일 요건 |
| [SHAP](/studynote/10_ai/04_ai_ops_ethics/327_shap/) | [XAI](/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/) 기법 | Shapley Value 기반 특성 기여도 설명 |
| [LIME](/studynote/10_ai/04_ai_ops_ethics/326_lime/) | [XAI](/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/) 기법 | 지역 선형 근사 기반 모델 무관 설명 |
| EU [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Act | 규제 프레임워크 | [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 및 의무 규정 |
| Algorithmic Impact Assessment | 거버넌스 도구 | 고위험 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 배포 전 의무적 위험 평가 |
| Human-in-the-Loop | 설계 원칙 | 고위험 결정에 인간 검토 단계 포함 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 수집 단계 — 표현 편향 (Representation Bias) 내재]
    |
    v
[AI 모델 훈련 — 편향 학습 및 증폭]
    |
    v
[XAI (설명 가능 AI — SHAP/LIME) — 의사결정 근거 투명화]
    |
    v
[공정성 지표 (Fairness Metrics) — Demographic Parity 등]
    |
    v
[EU AI Act / 알고리즘 영향 평가 (AIA) — 법적 의무화]
```
[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 편향은 수집 단계에서 시작해 모델 훈련을 통해 증폭되며, XAI로 투명성을 확보하고 공정성 지표 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 거쳐 EU [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Act 같은 규제 의무 이행까지 이어지는 전주기 거버넌스가 필요하다.

### 👶 어린이를 위한 3줄 비유 설명

- AI가 편향되는 것은 <strong>인종차별적인 선생님에게 배운 학생</strong>과 같아요: 선생님의 편견(편향된 훈련 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 학생([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))이 그대로 배워서 더 체계적으로 차별할 수 있어요.
- [XAI](/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/)(설명 가능한 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))는 AI가 "왜 이 결정을 했는지" 알려주는 것이에요 — "이 사람이 대출 거절된 이유는 신용점수가 낮아서"라고 설명해 줘야 억울하지 않잖아요.
- EU [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Act는 AI도 자동차처럼 <strong>안전 검사 의무</strong>가 있다는 규칙이에요: 생명에 영향 주는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)(의료·채용·사법)는 출시 전 엄격한 공정성 검사를 받아야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 211 / 262

<- **이전**: [204. 합성 데이터 (Synthetic Data) — 통계적 특성 보존 개인정보 대체](/studynote/16_bigdata/10_governance/210_synthetic_data/)
**다음**: [206. 빅데이터 분쟁 (Big Data Legal Disputes) — 데이터 소유권/수집 동의/목적 외 사용](/studynote/16_bigdata/10_governance/212_bigdata_disputes/) ->

---
