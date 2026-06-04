+++
title = "340. DeepFM 딥러닝 추천 엔진 (Deepfm Recommendation)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DeepFM 은 FM (Factorization Machine, 인수분해 머신) 의 2차 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 상호작용 (Feature Interaction) 과 DNN (Deep Neural Network) 의 고차 상호작용을 공유 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) (Shared [Embedding](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)) 으로 동시에 학습해 [CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/) (Click-Through Rate, 클릭률) 예측 정확도를 높인다.
> 2. **가치**: Wide & Deep 과 달리 FM [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)가 수동 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 엔지니어링 없이 저차 상호작용을 자동 학습하므로, [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 전문 지식 없이도 고품질 추천이 가능하다.
> 3. **판단 포인트**: FM 은 O(kd) 복잡도로 2차 상호작용을 학습하고, DNN 은 3차 이상 고차 상호작용을 암묵적으로 학습한다는 상보적 역할을 반드시 서술해야 한다.

---

## Ⅰ. 개요 및 필요성

### [CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/) 예측의 핵심 과제

[추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)에서 [CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/) 예측은 "사용자 u 가 아이템 i 를 클릭할 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)" 을 예측하는 회귀/[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 문제다. 핵심 도전은 다음과 같다.

| 과제 | 기존 방법 한계 | DeepFM 해결 방식 |
|:---|:---|:---|
| 저차 상호작용 | [로지스틱 회귀](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/227_logistic_regression_clt_pvalue_type_error/): 선형만 가능 | FM [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 자동 학습 |
| 고차 상호작용 | FM: 2차까지만 명시적 학습 | DNN [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 암묵적 학습 |
| [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 엔지니어링 | Wide & Deep: 수동 Cross Feature | 불필요 (공유 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)) |
| 희소 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | [협업 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/): [콜드 스타트](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/) 취약 | [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)으로 저차원 밀집 표현 |

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)은 "쇼핑몰에서 손님이 어떤 상품을 클릭할지 예측하는 점원"이다. 단순히 나이·성별만 보면 부족하고, "30대 남성이 스포츠 신발을 자주 보던 패턴"처럼 조합 패턴을 읽어야 정확하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### DeepFM 전체 구조

```
  입력 (Sparse Features: UserID, ItemID, Category, ...)
  +------------------------------------------------------+
  |             Embedding Layer (공유 임베딩)             |
  |  [e_1]  [e_2]  [e_3]  [e_4]  ...  [e_d]            |
  +------------+---------------------------+-------------+
               |                           |
  +------------v--------+  +---------------v-------------+
  |   FM 컴포넌트        |  |      DNN 컴포넌트            |
  |                     |  |                             |
  | y_FM = <w,x>        |  | Layer 1: ReLU(W1·e + b1)   |
  |   + Σᵢ<ΣⱼVᵢ·Vⱼ·xᵢxⱼ|  | Layer 2: ReLU(W2·h1 + b2) |
  | (1차 + 2차 상호작용) |  | Layer 3: σ(W3·h2 + b3)    |
  +------------+--------+  +---------------+-------------+
               |                           |
               +----------+----------------+
                           v
                    y = sigmoid(y_FM + y_DNN)
                    (최종 CTR 예측값)
```

### FM (Factorization Machine, 인수분해 머신) 원리

FM 의 2차 상호작용 항:

```
  기존 Polynomial Model: Σᵢ Σⱼ wᵢⱼ · xᵢ · xⱼ  -> 파라미터 O(d^)

  FM 분해:             Σᵢ Σⱼ <Vᵢ, Vⱼ> · xᵢ · xⱼ -> 파라미터 O(kd)
  where <Vᵢ, Vⱼ> = Σf vᵢf · vⱼf  (잠재 벡터 내적)

  FM 전개를 통한 효율적 계산: O(kd) 복잡도 달성
  = 1/2 · (||Σᵢ vᵢxᵢ||^ - Σᵢ ||vᵢ||^xᵢ^)
```

### Wide & Deep vs DeepFM 비교

| 항목 | Wide & Deep | DeepFM |
|:---|:---|:---|
| 저차 상호작용 | Wide 파트 (수동 Cross Feature) | FM 파트 (자동 학습) |
| 고차 상호작용 | Deep 파트 | DNN 파트 |
| [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 엔지니어링 | 필요 (Wide 입력 설계) | 불필요 |
| [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 공유 | Wide/Deep 별도 | 완전 공유 |

- **📢 섹션 요약 비유**: DeepFM 은 "FM 이라는 날카로운 안경(2차 패턴 포착)과 DNN 이라는 전체 그림 보는 광각렌즈를 같은 코에 동시에 얹은" 듀얼 카메라 시스템이다. 둘이 같은 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)을 공유하니 렌즈 교환 비용도 없다.

---

## Ⅲ. 비교 및 연결

### 딥러닝 추천 모델 계보

| 모델 | 연도 | 핵심 아이디어 | 한계 |
|:---|:---:|:---|:---|
| FM | 2010 | 2차 상호작용 분해 | 고차 학습 불가 |
| Wide & Deep | 2016 | 광역 기억 + 심층 일반화 | 수동 Wide [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 필요 |
| DeepFM | 2017 | FM + DNN 공유 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) | 암묵적 고차 상호작용만 |
| xDeepFM | 2018 | CIN (Compressed Interaction Network) | 연산 비용 증가 |
| AutoInt | 2019 | [Self-Attention](/knowledge-base/studynote/10_ai/02_dl_architecture_new/124_self_attention/) 상호작용 | [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 비용 |

- **📢 섹션 요약 비유**: 추천 모델의 진화는 "간단한 곱셈기(FM) -> 기억력+직관의 결합(Wide&Deep) -> 공유 두뇌의 이중 시각(DeepFM) -> 모든 연결 동시 분석([Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 기반)" 으로 점점 복잡해지는 과정이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 산업 적용 사례

- **텐센트 (Tencent)**: DeepFM 제안 회사, 앱스토어 광고 [CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/) 예측
- **Alibaba**: DIN (Deep Interest Network) 으로 확장
- **Criteo**: 광고 클릭률 예측 Kaggle 벤치마크에서 우수 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)

### 기술사 출제 포인트

- FM 의 O(kd) 복잡도 달성 원리: 잠재 벡터 분해와 전개 수식
- DeepFM 의 공유 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)이 Wide & Deep 대비 유리한 이유
- [CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/) 예측에서 1차 (선형) + 2차 (FM) + 고차 (DNN) 상호작용의 역할
- [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/): Binary [Cross-Entropy](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/) (이진 클릭/비클릭)

- **📢 섹션 요약 비유**: FM 의 잠재 벡터 분해는 "1,000×1,000 체스판의 모든 칸 조합을 외우는 대신, 각 칸의 특성 점수 10개씩만 외워서 필요할 때 곱하는" [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. 1,000,000 개 파라미터가 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000개로 줄어든다.

---

## Ⅴ. 기대효과 및 결론

- **자동화**: [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 엔지니어링 없이 저차·고차 상호작용 동시 학습
- <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong>: Criteo 벤치마크에서 Wide & Deep, PNN 대비 AUC 향상
- **효율**: 공유 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)으로 파라미터 수 절감 및 학습 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)
- **한계**: 명시적 고차 상호작용 (3차 이상) 은 xDeepFM 이 더 유리

DeepFM 은 [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)의 두 핵심 과제인 저차·고차 상호작용 학습을 단일 아키텍처로 해결한 균형 잡힌 모델이다. 기술사 시험에서는 FM 의 잠재 벡터 분해 원리, 공유 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)의 장점, Wide & Deep 와의 비교를 중심으로 서술하면 고득점 가능하다.

- **📢 섹션 요약 비유**: DeepFM 은 [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)의 "만능 요리사" — 간단한 레시피(FM, 2차 조합)와 복잡한 창의 요리(DNN, 고차 조합)를 같은 재료(공유 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/))로 동시에 만들어낸다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| FM (Factorization Machine) | 잠재 벡터, O(kd) / DeepFM 의 저차 상호작용 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) |
| DNN (Deep Neural Network) | 고차 상호작용, 비선형 / DeepFM 의 고차 상호작용 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) |
| 공유 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) (Shared [Embedding](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)) | [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 표현 통합 / FM/DNN 동시 활용 핵심 |
| [CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/) (Click-Through Rate) | 클릭률, 이진 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) / DeepFM 의 주 예측 목표 |
| Wide & Deep | 메모리+일반화 / DeepFM 의 선행 모델 비교 기준 |
| xDeepFM | CIN, 명시적 고차 / DeepFM 의 발전된 후속 모델 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] -> [DeepFM 딥러닝 추천 엔진 (Deepfm Recommendation)] -> [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 🛒 DeepFM 은 "어떤 물건을 살지" 예측하는 쇼핑 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 인데, 단순한 패턴과 복잡한 패턴을 동시에 배워요.
2. 🔗 FM 파트는 "농구공 + 운동화 = 스포츠 관심자" 처럼 2가지 조합 패턴을, DNN 파트는 더 복잡한 여러 개 조합을 봐요.
3. 🤝 둘이 같은 재료([임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/))를 쓰니까 따로 공부하는 것보다 더 효율적이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 340 / 420

<- **이전**: [339. Word2Vec (Word2vec)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/339_word2vec/)
**다음**: [341. 고유값 분해 (Eigenvalue Decomposition, EVD)](/knowledge-base/studynote/10_ai/05_data_science_ml/341_eigenvalue_decomposition/) ->

---
