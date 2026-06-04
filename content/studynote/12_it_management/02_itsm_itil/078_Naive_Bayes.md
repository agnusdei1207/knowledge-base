+++
title = "78. DataStream API / Table API & SQL — Flink 두 계층"
description = "Naive Bayes 분류기의 확률적 원리, 조건부 독립 가정,贝叶斯定理 적용 방법, 텍스트 분류에서의 활용"
date = 2026-04-05

[taxonomies]
tags = ["it_management"]

[extra]
tags = ["it_management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Naive Bayes는 Bayes theorem과 조건부 독립 가정을 이용한 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)기다.
> 2. **가치**: 희소한 텍스트나 작은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서도 빠르고 설명 가능한 기준선을 만든다.
> 3. **판단 포인트**: [ITSM](/knowledge-base/studynote/12_it_management/02_itsm_itil/880_iso_iec_20000_itsm_certification/) ([IT Service Management](/knowledge-base/studynote/12_it_management/02_itsm_itil/845_itsm/))과 [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/846_itil/) (Information Technology Infrastructure [Library](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/))에서는 티켓 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/), 스팸 필터, 태깅에 특히 잘 맞는다.

---

## Ⅰ. 개요 및 필요성

[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 문제는 "이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어느 클래스에 속하는가"를 빠르게 정하는 일이다. Naive Bayes는 단순하지만 강한 기준선으로 자주 쓰인다.
IT 운영에서는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 요청, 장애 티켓, 문서 태깅처럼 라벨이 분명한 업무가 많다. 이런 곳에서 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 기반 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)는 자동화의 첫 단계가 된다.
```text
특징 -> prior / likelihood -> posterior -> class label
P(class|features) ∝ P(class) × Π P(feature|class)
```

- **📢 섹션 요약 비유**: 문서와 티켓을 빠르게 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하는 단순한 기준선이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

학습 단계에서는 클래스별 prior를 세고, 각 특징의 likelihood를 집계한다. 예측 단계에서는 posterior를 계산해 가장 높은 클래스를 고른다.
조건부 독립 가정은 현실을 단순화한 것이지만, 텍스트처럼 희소하고 특징 수가 많은 문제에서 의외로 잘 동작한다. Laplace smoothing은 0 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 문제를 막는다.
| 요소 | 역할 | 메모 |
| --- | --- | --- |
| Prior | 사전 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) | 클래스 빈도를 반영한다 |
| Likelihood | 특징이 주어졌을 때의 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) | 특징별 증거를 모은다 |
| Posterior | 최종 클래스 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) | 비교 기준이 된다 |
| [Laplace smoothing](/knowledge-base/studynote/10_ai/05_data_science_ml/350_laplace_smoothing/) | 0 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 방지 | 희소 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 중요하다 |
| MAP (Maximum A Posteriori) | 가장 큰 posterior 선택 | [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 결정 규칙이다 |

- **📢 섹션 요약 비유**: prior, likelihood, posterior를 곱해 가장 가능성 높은 클래스를 고른다.

---

## Ⅲ. 비교 및 연결

Naive Bayes는 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 모델이라 분포를 먼저 배우고, logistic regression은 판별 모델이라 경계를 직접 배운다. decision tree는 규칙 분기 중심이라 해석 방식이 또 다르다.
독립 가정이 강할수록 단순해지지만, 상관관계가 큰 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)에서는 성능이 약해질 수 있다. 그래서 모델은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 형태와 함께 선택해야 한다.
| 비교축 | Naive Bayes | [Logistic Regression](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/) | [Decision Tree](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/) |
| --- | --- | --- | --- |
| 학습 철학 | [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 모델 | 판별 모델 | 규칙 분기 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 요구 | 작아도 시작 가능 | 중간 이상 | 중간 |
| 해석성 | [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 증거를 읽기 쉽다 | [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 해석 | 경로 해석 |

- **📢 섹션 요약 비유**: [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 모델의 단순함이 텍스트 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)에서 힘을 발휘한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 티켓 제목, 설명, 키워드 같은 텍스트 특징을 이용해 라우팅에 쓴다. 자동 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)가 잘 되면 1차 응답 속도와 운영 효율이 크게 좋아진다.
다만 특징 간 상관관계가 강하거나 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 보정이 중요하면 다른 모델도 함께 봐야 한다. 특히 smoothing 없이 쓰면 희소 특징에서 0 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)이 쉽게 터진다.
### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 클래스 prior와 likelihood가 충분히 학습됐는가?
2. Laplace smoothing이 적용됐는가?
3. [ITSM](/knowledge-base/studynote/12_it_management/02_itsm_itil/880_iso_iec_20000_itsm_certification/) 프로세스와 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 결과가 연결되는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 0 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 문제를 무시한 채 그대로 쓰는 것
- 상관된 특징을 많이 넣고 독립 가정이 무너지게 두는 것

- **📢 섹션 요약 비유**: smoothing과 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 설계가 성능을 좌우한다.

---

## Ⅴ. 기대효과 및 결론

Naive Bayes는 복잡한 모델이 나오기 전에도 빠른 자동화를 가능하게 하는 강한 기준선이다. 작은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 텍스트 업무에서 특히 유용하다.
앞으로는 임베딩과 결합한 하이브리드 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)가 더 많아지겠지만, [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적 기준선의 가치는 줄지 않는다.
기술사는 이 주제를 "적은 정보로도 빠르게 우선순위를 매기는 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)"로 기억하면 된다.

- **📢 섹션 요약 비유**: 작은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서도 빠르게 자동화를 시작하게 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| --- | --- |
| [Bayes theorem](/knowledge-base/studynote/08_algorithm_stats/08_stats/131_bayes_theorem/) | 사전 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)과 우도를 결합한다 |
| Prior | 클래스의 기본 비율이다 |
| Likelihood | 특징이 주어졌을 때의 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)이다 |
| Posterior | 최종 판단 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)이다 |
| [Laplace smoothing](/knowledge-base/studynote/10_ai/05_data_science_ml/350_laplace_smoothing/) | 희소성 때문에 생기는 0 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)을 막는다 |
| [ITSM](/knowledge-base/studynote/12_it_management/02_itsm_itil/880_iso_iec_20000_itsm_certification/) / [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/846_itil/) | 운영 티켓 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)와 잘 맞는다 |

### 📈 관련 키워드 및 발전 흐름도

```text
training data
  |
  v
count features by class
  |
  v
estimate prior / likelihood
  |
  v
compute posterior
  |
  v
route to class
```

### 👶 어린이를 위한 3줄 비유 설명

1. 탐정이 단서 몇 개만 보고도 어느 상자에서 왔는지 맞히는 것과 같다.
2. 단서가 서로 얼마나 잘 어울리는지 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)로 계산하면 더 빨리 맞힐 수 있다.
3. 그래서 컴퓨터는 적은 정보로도 가장 그럴듯한 답을 찾는다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 139 / 587

<- **이전**: [77. 문제 관리 (Problem Management)](/knowledge-base/studynote/12_it_management/02_itsm_itil/861_problem_management/)
**다음**: [78. KEDB (Known Error Database)](/knowledge-base/studynote/12_it_management/02_itsm_itil/862_kedb/) ->

---
