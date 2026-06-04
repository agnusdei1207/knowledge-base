---
title: "126. Bagging & Random Forest - 배깅 앙상블과 랜덤 포레스트"
date: "2026-04-19"
tags:
  - "studynote-dataengineering"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [Bagging](/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/)(Bootstrap Aggregating)은 <strong>학습 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 부트스트랩(복원 추출)으로 여러 부분 집합을 만들고, 각 부분 집합으로 독립 모델을 학습 -> 다수결/평균으로 결합</strong>하는 [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 기법이다.
> 2. **가치**: 단일 의사결정 트리는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변화에 민감(높은 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/))하지만, 100개 트리를 Bagging하면 <strong><a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>이 극적으로 감소</strong>하여 과적합이 줄어든다.
> 3. **판단 포인트**: [Random Forest](/studynote/06_ict_convergence/05_data_science/353_random_forest/) = [Bagging](/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/) + <strong><a href="/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> 랜덤 선택</strong>이며, 각 트리가 전체 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)의 √p개만 사용하여 **트리 간 상관관계를 낮추어** [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 효과를 극대화한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Random Forest 동작                                 |
+-------------------------------------------------------+
|  원본 데이터 (N개 샘플, p개 피처)                     |
|  +-- 부트스트랩 1 (N개 복원 추출) + √p 피처 -> 트리 1|
|  +-- 부트스트랩 2 (N개 복원 추출) + √p 피처 -> 트리 2|
|  +-- ...                                              |
|  +-- 부트스트랩 100 -> 트리 100                       |
|                                                       |
|  분류: 다수결 투표                                    |
|  회귀: 평균                                           |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Bagging은 100명의 의사가 독립 진단 후 <strong>다수결</strong>로 최종 진단을 내리는 것이다. Random Forest는 각 의사가 <strong>다른 검사 항목(<a href="/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a>)</strong>으로 진단하여 다양성을 높인다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [Bagging](/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/) vs [Random Forest](/studynote/06_ict_convergence/05_data_science/353_random_forest/)

| 비교 | [Bagging](/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/) | [Random Forest](/studynote/06_ict_convergence/05_data_science/353_random_forest/) |
|:---|:---|:---|
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong> | 부트스트랩 | 부트스트랩 |
| <strong><a href="/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a></strong> | 전체 사용 | **√p 랜덤 선택** |
| **다양성** | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 | <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> + <a href="/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a></strong> |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | 좋음 | **더 좋음** |

### OOB (Out-of-Bag)
부트스트랩에서 선택되지 않은 ~37% [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 자체 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) -> <strong>별도 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> 세트 불필요</strong>.

- **📢 섹션 요약 비유**: OOB는 시험에 출제되지 않은 문제로 <strong>자체 모의고사</strong>를 보는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 단일 트리 | [Random Forest](/studynote/06_ict_convergence/05_data_science/353_random_forest/) | XGBoost |
|:---|:---|:---|:---|
| **과적합** | 높음 | **낮음** | 낮음 |
| **학습** | 빠름 | [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) | 순차 |
| **해석** | 가능 | [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 중요도 | [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 중요도 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [Random Forest](/studynote/06_ict_convergence/05_data_science/353_random_forest/) 장점
1. 하이퍼파라미터 튜닝이 쉬움 (기본값도 잘 동작).
2. [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 중요도([Feature Importance](/studynote/10_ai/05_data_science_ml/355_random_forest_feature_importance/)) 제공.
3. 결측치·이상치에 강건.

---

## Ⅴ. 기대효과 및 결론

Random Forest는 <strong>가장 안정적이고 실용적인 ML <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a> 중 하나</strong>이며, [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 선택·[베이스라인](/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/) 모델·비전문가 ML에 최적이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/">Bagging</a></strong> | 부트스트랩 + 다수결 |
| <strong><a href="/studynote/06_ict_convergence/05_data_science/353_random_forest/">Random Forest</a></strong> | [Bagging](/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/) + [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 랜덤화 |
| **OOB** | 자체 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| <strong><a href="/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> 중요도</strong> | Random Forest의 해석 도구 |
| **XGBoost** | [부스팅](/studynote/14_data_engineering/03_ml_dl_llm/127_boosting/) [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) (비교 대상) |

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 의사결정 트리 (CART, 1984)]
    |
    v
[Bagging (Breiman, 1996)]
    |
    v
[Random Forest (Breiman, 2001) — 피처 랜덤화 추가]
    |
    v
[Extra Trees (2006) — 더 랜덤한 분할]
    |
    v
[현재: AutoML — RF vs XGBoost 자동 선택]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Random Forest는 <strong>100명의 의사</strong>가 각자 진단 후 <strong>다수결</strong>로 결정하는 거예요.
2. 각 의사가 <strong>다른 검사 항목</strong>으로 진단해서 <strong>다양한 의견</strong>이 모여요.
3. 혼자보다 100명이 **함께 판단하면** 훨씬 정확하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 126 / 258

<- **이전**: [125. 앙상블 학습 (Ensemble Learning) - 여러 모델의 결합으로 성능 극대화](/studynote/14_data_engineering/03_ml_dl_llm/125_ensemble_learning/)
**다음**: [127. Boosting (부스팅) - 순차적 오류 보정 앙상블 학습](/studynote/14_data_engineering/03_ml_dl_llm/127_boosting/) ->

---
