+++
title = "418. 오버샘플링·언더샘플링·SMOTE (Synthetic Minority Over-sampling Technique)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 오버샘플링 ([Oversampling](/knowledge-base/studynote/14_data_engineering/02_math_mining/096_oversampling_smote/)), 언더샘플링 (Undersampling), [SMOTE](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/231_smote_oversampling_class_imbalance_augmentation/) ([Synthetic Minority Over-sampling Technique](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/231_smote_oversampling_class_imbalance_augmentation/))는 클래스 불균형 (Class Imbalance) 문제를 완화하기 위해 **학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포 자체를 재조정**하는 기법이다.
> 2. **가치**: 다수 클래스가 압도적으로 많은 상황에서는 모델이 정확도는 높아 보여도 소수 클래스 탐지를 거의 못 하게 되는데, 재표본화는 이런 편향을 줄여 [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) ([Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/))과 F1-score를 개선한다.
> 3. **판단 포인트**: 단순 오버샘플링은 과적합 위험, 언더샘플링은 정보 손실 위험이 있으며, SMOTE는 이웃 간 선형 보간으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 늘리지만 노이즈와 클래스 경계 왜곡을 함께 관리해야 한다.

---

## Ⅰ. 개요 및 필요성

사기 거래 탐지, 질병 진단, [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 검출처럼 중요한 문제일수록 양성 클래스가 적은 경우가 많다. 이런 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 정확도만 보고 모델을 학습하면, "전부 정상"이라고 예측해도 높은 점수가 나오므로 실제 현장에서는 쓸모없는 모델이 된다.

재표본화는 이 문제를 가장 직접적으로 다룬다. [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)를 바꾸기 전에, 학습에 들어가는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 비율부터 조정해 모델이 소수 클래스를 충분히 보도록 만드는 것이다. 그래서 불균형 학습의 가장 기본적이면서도 실무적인 출발점으로 여겨진다.

```text
┌──────────────────────────────────────────────────────────────┐
│           클래스 불균형이 만드는 학습 편향                   │
├──────────────────────────────────────────────────────────────┤
│ 원본 데이터 :  ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○   ●                    │
│                 다수 클래스가 의사결정을 지배                │
│                                                              │
│ 재표본화 후 : ○ ○ ○ ○ ○ ○   ● ● ● ●                         │
│                 소수 클래스가 학습에서 보이기 시작           │
└──────────────────────────────────────────────────────────────┘
```

핵심은 "현실 비율"을 바꾸는 것이 아니라 "학습이 보게 되는 비율"을 바꾸는 데 있다. 운영 환경의 클래스 비율은 그대로 두더라도, 학습 단계에서만 분포를 조정해 의사결정 경계를 더 공정하게 만들 수 있다.

- **📢 섹션 요약 비유**: 교실에서 조용한 학생이 한 명뿐이면 토론에서 목소리가 묻힌다. 발표 기회를 더 주거나, 너무 말 많은 학생 발언을 조금 줄여야 전체 의견을 더 제대로 들을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

세 방법의 차이는 소수 클래스를 늘릴지, 다수 클래스를 줄일지, 아니면 인공 샘플을 만들지에 있다.

| 기법           | 작동 방식                       | 장점                 | 약점                        |
| :------------- | :------------------------------ | :------------------- | :-------------------------- |
| **오버샘플링** | 소수 클래스 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)                | 정보 손실 없음       | 중복 학습으로 과적합 가능   |
| **언더샘플링** | 다수 클래스 일부 제거           | 학습 속도 향상       | 중요한 패턴 손실 가능       |
| **[SMOTE](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/231_smote_oversampling_class_imbalance_augmentation/)**      | 이웃 소수 샘플 사이를 선형 보간 | [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)보다 일반화 유도 | 경계 왜곡, 노이즈 증폭 가능 |

SMOTE의 기본 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 규칙은 다음과 같다.

$$
x_{[new](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)} = x_i + \[lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) (x_{nn} - x_i), \quad \[lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) \in [0,1]
$$

여기서 `x_i`는 소수 클래스 샘플, `x_{nn}`은 그 최근접 이웃이다. 즉, 소수 클래스 공간 안에서 두 점을 잇는 선분 위에 새로운 샘플을 만든다. [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)보다 덜 경직되지만, 경계 바깥까지 샘플을 밀어내면 오히려 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)기를 혼란스럽게 할 수 있다.

```text
┌──────────────────────────────────────────────────────────────┐
│                SMOTE의 합성 샘플 생성 원리                   │
├──────────────────────────────────────────────────────────────┤
│ minority point xi ●──────● xnn nearest minority              │
│                     \    /                                    │
│                      \ ● /  new synthetic sample              │
│                       \  /                                   │
│ 핵심: 소수 클래스 내부 이웃 사이를 보간한다                  │
└──────────────────────────────────────────────────────────────┘
```

이 구조는 [K-NN](/knowledge-base/studynote/06_ict_convergence/05_data_science/352_knn_distance_metrics/) ([K-Nearest Neighbors](/knowledge-base/studynote/10_ai/03_llm_nlp/262_knn/))에 기반하므로, 특징 공간이 잘 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)되어 있어야 한다. 거리 기반 이웃이 왜곡되면 잘못된 방향으로 합성 샘플이 생긴다. 따라서 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/), 표준화, 범주형 처리 여부가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 직접 영향을 준다.

- **📢 섹션 요약 비유**: 소수 학생 한 명을 그대로 복사해 세 자리에 앉히는 것이 오버샘플링이라면, SMOTE는 비슷한 두 학생 사이 성향을 섞어 가상의 새 학생을 만드는 방식이다.

---

## Ⅲ. 비교 및 연결

| 비교 축        | 오버샘플링 | 언더샘플링 | [SMOTE](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/231_smote_oversampling_class_imbalance_augmentation/) | 클래스 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) |
| :------------- | :--------- | :--------- | :---- | :------------ |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수 변화 | 증가       | 감소       | 증가  | 변화 없음     |
| 정보 손실      | 없음       | 큼         | 없음  | 없음          |
| 과적합 위험    | 중간~높음  | 낮음       | 중간  | 낮음          |
| 구현 복잡도    | 낮음       | 낮음       | 중간  | 매우 낮음     |

클래스 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) (Class [Weight](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/))는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 건드리지 않고 [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)만 조정하는 방식이다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 규모가 크거나 특징 공간이 복잡할 때는 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 방식이 더 안전할 수 있다. 반면 소수 클래스 표본이 너무 적어 학습 자체가 불안정하다면, 재표본화가 더 직접적인 개선을 준다.

SMOTE는 ADASYN, Borderline-[SMOTE](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/231_smote_oversampling_class_imbalance_augmentation/) 같은 파생 기법으로 확장된다. 특히 경계 근처의 어려운 샘플을 더 많이 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하면 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 경계 학습에는 유리하지만, 노이즈가 섞인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서는 오히려 이상한 표본이 늘어날 수 있다. 즉, 불균형 보정은 늘 "[재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/) 향상 vs 경계 왜곡"의 균형 문제다.

- **📢 섹션 요약 비유**: 발표 기회를 늘리는 것, 말 많은 학생 시간을 줄이는 것, 새 조별 대표를 뽑아 중간 의견을 만드는 것은 모두 토론 균형을 맞추는 다른 방법이다. 어느 방식이 좋은지는 반 분위기에 따라 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 재표본화는 반드시 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분할 이후에만 적용했는가?
2. 평가지표를 정확도가 아니라 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/), [재현율](/knowledge-base/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/), F1, [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)-AUC 중심으로 보았는가?
3. 특징 공간이 거리 기반 보간에 적합하도록 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)되었는가?
4. 소수 클래스 자체에 노이즈가 많지 않은가?
5. 비용 민감 학습 또는 클래스 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)와 비교 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)했는가?

### 실무 판단

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수가 적고 소수 클래스가 극단적으로 희귀하면, 먼저 단순 오버샘플링과 클래스 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)로 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)을 잡고 그다음 SMOTE를 비교하는 편이 안전하다. SMOTE를 처음부터 정답처럼 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)보다, 실제로 경계 품질이 좋아졌는지 [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)-AUC로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해야 한다.

또한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 누수 ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Leakage)를 피하는 것이 중요하다. 전체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 먼저 SMOTE를 적용한 뒤 train/test를 나누면, 합성 샘플이 테스트 분포를 오염시켜 점수가 부풀려진다. 시험 답안에서는 "재표본화는 반드시 학습 폴드 내부에서만 수행"이라고 적으면 실무 감각이 드러난다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- train/test 분할 전에 SMOTE를 적용하는 설계
- 정확도 하나만 보고 불균형 문제를 해결했다고 착각하는 설계
- 노이즈가 심한 소수 클래스에 무차별적으로 합성 샘플을 늘리는 설계

- **📢 섹션 요약 비유**: 시험 문제를 미리 본 학생으로 연습 문제를 만들면 실력이 아니라 요령만 높아진다. SMOTE도 훈련 구간 안에서만 써야 정직한 성적이 나온다.

---

## Ⅴ. 기대효과 및 결론

재표본화 기법은 불균형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 모델이 다수 클래스만 편애하는 현상을 줄여, 실제로 중요한 소수 이벤트를 더 잘 잡아내게 한다. 특히 탐지·경보 시스템에서는 이 차이가 운영 품질을 크게 바꾼다.

결론적으로 오버샘플링, 언더샘플링, SMOTE의 핵심은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 비율을 예쁘게 맞추는 것이 아니라 **의사결정 경계가 소수 클래스를 무시하지 않게 만드는 것**이다. [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), 삭제, 합성의 트레이드오프를 이해하고, 평가지표와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 누수를 함께 관리해야 한다.

- **📢 섹션 요약 비유**: 모두가 비슷하게 말할 기회를 주는 것이 목적이지, 사람 수를 억지로 맞추는 게 목적은 아니다. 균형 잡힌 토론이 결국 더 좋은 결론을 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Class Imbalance | 재표본화가 필요한 출발 문제 |
| [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) / [Recall](/knowledge-base/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/) / F1 | 불균형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 핵심 평가지표 |
| [K-NN](/knowledge-base/studynote/06_ict_convergence/05_data_science/352_knn_distance_metrics/) | SMOTE가 이웃을 찾는 기반 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| ADASYN | SMOTE의 난이도 가중 확장판 |
| Class [Weight](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 대신 손실을 조정하는 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] → [오버샘플링·언더샘플링·SMOTE (Synthetic Minority Over-sampling Technique)] → [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 조용한 친구가 너무 적으면 선생님이 그 친구 말을 잘 못 듣게 돼요.
2. 그래서 조용한 친구 발표를 더 시키거나, 비슷한 생각을 가진 새 예시를 만들어 연습해 보는 거예요.
3. 그러면 컴퓨터가 중요한 드문 경우도 더 잘 배우게 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 418 / 420

← **이전**: [417. BM25 정보 검색 모델 (Best Matching 25)](/knowledge-base/studynote/10_ai/05_data_science_ml/417_bm25_document_length_normalization/)
**다음**: [419. 퍼지 소속 함수·퍼지 추론·디퍼지피케이션 (Fuzzy Membership, Inference, Defuzzification)](/knowledge-base/studynote/10_ai/05_data_science_ml/419_fuzzy_membership_defuzzification/) →

---
