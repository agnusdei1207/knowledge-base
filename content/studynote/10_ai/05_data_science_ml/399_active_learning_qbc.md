---
title: "399. 액티브 러닝 (Active Learning)"
date: "2026-05-09"
tags:
  - "studynote-ai"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [액티브 러닝](/studynote/10_ai/03_llm_nlp/214_active_learning/) ([Active Learning](/studynote/10_ai/03_llm_nlp/214_active_learning/))은 레이블이 없는 대규모 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중 "가장 정보가 풍부한" 샘플을 선택적으로 레이블링하여 최소한의 어노테이션으로 최대의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 달성하는 학습 패러다임이다.
> 2. **가치**: QBC (Query By Committee, 위원회 기반 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/))는 여러 모델 [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/)의 예측 불일치가 최대인 샘플을 선택하여 가장 유익한 샘플을 효율적으로 발굴한다.
> 3. **판단 포인트**: 불확실성 샘플링 (Uncertainty [Sampling](/studynote/03_network/01_data_communication/056_표본화_Sampling/)), QBC, 기대 모델 변화 (Expected Model Change), 코어셋 (Core-set) 등 다양한 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 특성을 파악하고 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 및 비용 구조에 맞게 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

의료 영상, 법률 문서, 전문 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 레이블링은 전문가 비용이 매우 높다. 전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 레이블하는 대신, AI가 "어떤 샘플에 레이블이 가장 필요한가"를 스스로 판단해 선택적으로 요청한다.

동일 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 달성에 필요한 레이블 수를 70~90% 감소시키는 것이 가능하다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: [액티브 러닝](/studynote/10_ai/03_llm_nlp/214_active_learning/)은 "시험공부할 때 내가 잘 모르는 문제만 선생님께 질문하는" 효율적 학습 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [액티브 러닝](/studynote/10_ai/03_llm_nlp/214_active_learning/) 사이클

```
+------------------------------------------------------+
|  [초기 레이블 풀] -► [모델 학습] -► [쿼리 전략]      |
|                              ^            v           |
|  [미레이블 풀] ◄--- 정보 풍부 샘플 선택  |           |
|       v                                  |           |
|  [전문가 레이블링] ----------------------+           |
|  반복 -> 성능 수렴                                     |
+------------------------------------------------------+
```

### 불확실성 샘플링 (Uncertainty [Sampling](/studynote/03_network/01_data_communication/056_표본화_Sampling/))

```
최소 신뢰도 (Least Confident):
  x* = argmax (1 - P(ŷ|x))   (최고 확률 클래스의 확신 가장 낮은 것)

마진 샘플링 (Margin Sampling):
  x* = argmin (P(ŷ₁|x) - P(ŷ₂|x))  (상위 2개 클래스 확률 차이 최소)

엔트로피 샘플링 (Entropy Sampling):
  x* = argmax H(y|x) = argmax [-Σ P(yᵢ|x) log P(yᵢ|x)]
```

### QBC (Query By Committee)

```
위원회 C = {θ₁, θ₂, ..., θₙ}  (n개 독립 모델)

불일치 측정 (Vote Entropy):
  x* = argmax [-Σⱼ V(yⱼ|x)/|C| · log V(yⱼ|x)/|C|]

V(yⱼ|x): 위원회에서 yⱼ로 예측한 모델 수
```

**QBC 실용 구현**: [배깅](/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/) ([Bagging](/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/)), MC [Dropout](/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/), 딥 [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/)

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 원리 | 계산 비용 | 적합 상황 |
|:---|:---|:---|:---|
| 불확실성 ([엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/)) | 단일 모델 예측 불확실 | 낮음 | 빠른 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| QBC | [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 불일치 | 중간 | 다양한 모델 |
| 기대 모델 변화 | 기울기 크기 최대화 | 높음 | 정밀한 선택 |
| Core-set | 기하학적 커버리지 | 중간 | 분포 표현성 |
| BALD | [상호 정보량](/studynote/08_algorithm_stats/09_info_theory/152_mutual_information/) 최대화 | 중간 | 베이지안 모델 |

- **📢 섹션 요약 비유**: QBC는 "전문가 패널의 의견이 가장 많이 갈리는 케이스"를 먼저 판별하는 것이다. 모두가 동의하는 케이스보다 이견이 있는 케이스를 레이블링하면 더 많이 배운다.

---

## Ⅲ. 비교 및 연결

<strong>BALD (Bayesian <a href="/studynote/10_ai/03_llm_nlp/214_active_learning/">Active Learning</a> by Disagreement)</strong>: 예측과 파라미터 간의 [상호 정보량](/studynote/08_algorithm_stats/09_info_theory/152_mutual_information/) 최대화:
```
x* = argmax I(y; θ | x, D)
   = H[y|x,D] - E_{θ~p(θ|D)}[H[y|x,θ]]
```

<strong>배치 <a href="/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/">액티브</a> 러닝</strong>: 매 라운드에 여러 샘플 선택 (중복성 방지를 위해 다양성 고려)

- **📢 섹션 요약 비유**: BALD는 "AI의 예측이 고정된 파라미터에 민감하게 변하는 샘플"을 선택한다. 파라미터를 조금 바꿔도 예측이 크게 달라지면 그 샘플이 중요한 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**의료 영상**: 방사선 전문의 레이블링 비용 절감 (암 진단 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))
**NLP**: 텍스트 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 레이블링 (법률 문서, [감성 분석](/studynote/12_it_management/03_ea_isp/889_exploratory_data_analysis/))
**자율주행**: 어엣지 케이스 자동 발굴 및 우선 레이블링

구현 팁:
- MC [Dropout](/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/): 추론 시 [Dropout](/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/) 활성화 -> 다수 예측 -> [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 계산
- Modular 설계: [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 플러그인으로 교체 가능하게

- **📢 섹션 요약 비유**: MC Dropout은 "같은 시험을 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)번 칠 때마다 답이 달라지는 문제"를 찾는다. 그런 문제가 진짜 모르는 것이다.

---

## Ⅴ. 기대효과 및 결론

[액티브](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) 러닝은 레이블 희소 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 실용화의 핵심 기술이다. QBC와 [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/) 샘플링은 간단하면서도 효과적인 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 널리 사용된다. 레이블링 비용의 급격한 감소는 의료, 법률, 과학 연구 등 전문 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 도입의 장벽을 낮춘다.

- **📢 섹션 요약 비유**: [액티브](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) 러닝은 "천 권의 책을 다 읽는 대신, 진짜 도움이 되는 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)0권을 골라 읽는" 지혜로운 학습법이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [액티브 러닝](/studynote/10_ai/03_llm_nlp/214_active_learning/) | [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), 레이블 효율 / 선택적 레이블링 학습 |
| QBC | 위원회, 불일치, [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/) / [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 기반 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| 불확실성 샘플링 | [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/), 마진 / 단일 모델 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| BALD | [상호 정보량](/studynote/08_algorithm_stats/09_info_theory/152_mutual_information/), 베이지안 / 이론적 최적 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| MC [Dropout](/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/) | 베이지안 근사 / 실용적 불확실성 추정 |
| Core-set | 기하학적 커버리지 / 분포 대표성 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] -> [액티브 러닝 (Active Learning)] -> [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [액티브 러닝](/studynote/10_ai/03_llm_nlp/214_active_learning/)은 "내가 모르는 문제만 선생님께 질문하는" [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이야. 다 아는 문제는 설명 안 들어도 되니까.
2. QBC는 여러 선생님(위원회)에게 같은 문제를 보여줬을 때 "선생님마다 답이 다른 문제"를 먼저 물어보는 방법이야.
3. [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/) 샘플링은 AI가 "고양이인지 개인지 확신이 없는 사진"을 먼저 레이블 요청하는 방식이야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 399 / 420

<- **이전**: [398. GAT (Graph Attention Network)](/studynote/10_ai/05_data_science_ml/398_gat/)
**다음**: [400. MLOps 드리프트 탐지 (Mlops Drift Detection)](/studynote/10_ai/05_data_science_ml/400_mlops_drift_detection/) ->

---
