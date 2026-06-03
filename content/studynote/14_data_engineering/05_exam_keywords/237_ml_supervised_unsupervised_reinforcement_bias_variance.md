---
title: 237. 머신러닝 지도·비지도·강화학습 편향-분산 오류 종합
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[241_machine_learning_basics|머신러닝]]의 세 패러다임—[[121_supervised_learning|지도 학습]]([[121_supervised_learning|Supervised Learning]]), [[122_unsupervised_learning|비지도 학습]]([[122_unsupervised_learning|Unsupervised Learning]]), [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]([[094_reinforcement_learning|Reinforcement Learning]])—은 "레이블(Label) 유무"와 "보상 [[130_signal|신호]](Reward [[130_signal|Signal]]) 유무"로 구분된다.
> 2. **가치**: 편향([[094_bias|Bias]])·[[136_variance|분산]]([[136_variance|Variance]]) 트레이드오프는 모든 ML 모델의 근본 딜레마로, 과적합([[245_overfitting_variance|Overfitting]])·과소적합([[246_underfitting_bias|Underfitting]]) 진단과 [[250_cross_validation_kfold|교차 검증]]([[250_cross_validation_kfold|Cross-Validation]])을 통해 일반화 [[282_performance_tactics|성능]]을 극대화한다.
> 3. **판단 포인트**: 학습 곡선([[240_switch_learning_forwarding_flooding|Learning]] Curve)으로 문제를 진단하고, 편향 문제는 모델 복잡도 증가로, [[136_variance|분산]] 문제는 [[093_normalization|정규화]]([[134_regularization_dropout_batch_norm|Regularization]])·[[001_dikw_pyramid|데이터]] 증강·[[257_ensemble_learning|앙상블]]로 해결한다.

## Ⅰ. 개요 및 필요성

### [[241_machine_learning_basics|머신러닝]] 학습 패러다임 3분류

```
머신러닝 (Machine Learning)
│
├── 지도 학습 (Supervised Learning)
│   조건: 입력 X + 레이블 Y 쌍 존재
│   목표: f(X) ≈ Y 함수 학습
│   대표: 분류(Classification), 회귀(Regression)
│
├── 비지도 학습 (Unsupervised Learning)
│   조건: 입력 X만 존재 (레이블 없음)
│   목표: 데이터 내재 구조·패턴 발견
│   대표: 클러스터링(Clustering), 차원 축소, 생성 모델
│
└── 강화 학습 (Reinforcement Learning)
    조건: 에이전트·환경·보상 신호
    목표: 누적 보상 최대화 정책(Policy) 학습
    대표: Q-학습, DQN, PPO
```

### 3가지 학습 방식 비교

| 항목 | [[121_supervised_learning|지도 학습]] | [[122_unsupervised_learning|비지도 학습]] | [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] |
|:---|:---|:---|:---|
| 레이블 | ✅ 필요 | ❌ 없음 | 보상 [[130_signal|신호]] |
| 피드백 | 즉각적 | 없음 | [[015_지연_데이터_관점|지연]] |
| 목적 | 예측·[[104_classification_analysis|분류]] | 구조 발견 | 최적 행동 |
| 주요 [[001_algorithm_definition|알고리즘]] | [[238_svm_margin_kernel_trick_naive_bayes|SVM]], DT, NN | K-Means, [[163_pca|PCA]] | [[316_q_learning|Q-Learning]], [[395_ppo_clipping|PPO]] |
| 예시 | 이메일 스팸 [[104_classification_analysis|분류]] | 고객 세분화 | 게임 [[190_ai_llm_requirements_specification|AI]], 로봇 |

📢 **섹션 요약 비유**: [[121_supervised_learning|지도 학습]]은 정답지 있는 시험 공부, [[122_unsupervised_learning|비지도 학습]]은 정답지 없이 책을 읽으며 주제를 찾는 것, [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]은 시행착오로 자전거 타기를 배우는 것이다.

## Ⅱ. 아키텍처 및 핵심 원리

### [[110_bias_variance_tradeoff|편향-분산 트레이드오프]] ([[110_bias_variance_tradeoff|Bias-Variance Tradeoff]])

모델의 예측 오류는 편향·[[136_variance|분산]]·노이즈의 합으로 분해된다.

```
총 오류 = 편향² + 분산 + 노이즈(줄일 수 없음)

편향 (Bias):
  모델의 가정이 잘못되어 발생하는 오류
  → 단순한 모델, 과소적합 (Underfitting)

분산 (Variance):
  학습 데이터의 변동에 과민하게 반응
  → 복잡한 모델, 과적합 (Overfitting)
```

**[[110_bias_variance_tradeoff|편향-분산 트레이드오프]] [[070_graph_datastructure|그래프]] ([[103_ascii|ASCII]])**

```
  오류
  (Error)
   │
   │  ┌ 총 오류
   │  │╲
   │  │  ╲       ╭─── 분산 (Variance)
   │  │   ╲   ╭──╯
   │  │    ╲╭─╯
   │  │     X ← 최적 복잡도 지점
   │  │  ╭──╲
   │  │──╯    ╲──── 편향 (Bias)
   │
   └────────────────────────── 모델 복잡도
      단순                     복잡
    (고편향)                 (고분산)
```

### 과적합 vs 과소적합 진단

```
┌─────────────────────────────────────────────────────────┐
│              학습 곡선 (Learning Curve) 해석              │
├───────────────────────┬─────────────────────────────────┤
│  과소적합 (Underfitting)│     과적합 (Overfitting)         │
│  편향이 큰 경우        │     분산이 큰 경우                │
│                       │                                 │
│  오류         오류     │  오류              오류          │
│  │            │       │  │    ╮            │            │
│  ├─ train      ├─val  │  │    ╰─ train    ├─ val        │
│  │  └─ high    │ high │  │      ↓ low    │  ↑ high     │
│                       │                                 │
│  → 모델 복잡도 증가   │  → 정규화·데이터 증가            │
│    피처 추가           │    드롭아웃·앙상블               │
└───────────────────────┴─────────────────────────────────┘
```

### [[250_cross_validation_kfold|교차 검증]] ([[250_cross_validation_kfold|Cross-Validation]])

모델의 일반화 [[282_performance_tactics|성능]]을 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 있게 추정하는 방법이다.

```
k-폴드 교차 검증 (k-Fold Cross-Validation), k=5:

전체 데이터
  └── 5등분 분할

  Fold 1: [검증] [훈련] [훈련] [훈련] [훈련]
  Fold 2: [훈련] [검증] [훈련] [훈련] [훈련]
  Fold 3: [훈련] [훈련] [검증] [훈련] [훈련]
  Fold 4: [훈련] [훈련] [훈련] [검증] [훈련]
  Fold 5: [훈련] [훈련] [훈련] [훈련] [검증]

  최종 성능 = 5번 검증 점수의 평균 (± 표준편차)

특수 변형:
  Stratified k-Fold: 클래스 비율 유지 (불균형 데이터)
  LOOCV (Leave-One-Out CV): k=n, 데이터 희귀 시
  Time-Series Split: 미래 데이터 누출 방지
```

📢 **섹션 요약 비유**: [[250_cross_validation_kfold|교차 검증]]은 시험 문제를 여러 세트 만들어 번갈아 시험 보는 것이다. 한 번 시험으로 운으로 높은 점수를 받는 것을 막고 진짜 실력을 측정한다.

## Ⅲ. 비교 및 연결

### 과적합 해결 기법

| 기법 | 원리 | 적용 방법 |
|:---|:---|:---|
| [[093_normalization|정규화]] L1 ([[102_lasso_ridge_regression_regularization|Lasso]]) | 불필요 [[247_feature_label_variables|피처]] 계수 0으로 | `alpha` 하이퍼파라미터 |
| [[093_normalization|정규화]] L2 (Ridge) | 계수 크기 전반 축소 | `lambda` 하이퍼파라미터 |
| [[280_dropout|드롭아웃]] ([[242_regularization_dropout_early_stopping_l1_l2_lasso_ridge|Dropout]]) | 무작위 뉴런 비활성화 | `rate=0.3~0.5` |
| [[281_early_stopping|조기 종료]] ([[281_early_stopping|Early Stopping]]) | [[395_verification_process_review|검증]] 오류 상승 시 중단 | patience [[009_config|설정]] |
| [[001_dikw_pyramid|데이터]] 증강 ([[001_dikw_pyramid|Data]] Augmentation) | 학습 [[001_dikw_pyramid|데이터]] 다양화 | 이미지 회전·플립 등 |
| [[257_ensemble_learning|앙상블]] ([[257_ensemble_learning|Ensemble]]) | 여러 모델 결합 | [[259_bagging_random_forest|배깅]]·[[127_boosting|부스팅]] |

### [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] 핵심 요소

```
┌─────────────────────────────────────────────────────┐
│              강화 학습 (Reinforcement Learning) 구조  │
│                                                     │
│  에이전트 (Agent)                                    │
│      │                                             │
│      │ 행동 (Action): at                           │
│      ▼                                             │
│  환경 (Environment)                                │
│      │                                             │
│      │ 상태 (State): s_{t+1}                       │
│      │ 보상 (Reward): r_{t+1}                      │
│      ▼                                             │
│  에이전트 → 정책(Policy) 업데이트                   │
│      목표: 누적 보상 최대화                          │
│      G_t = R_{t+1} + γR_{t+2} + γ²R_{t+3} + ...   │
│              감쇠 인자 γ ∈ [0,1]                   │
└─────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 편향은 항상 같은 방향으로 틀리는 것(낡은 지도), [[136_variance|분산]]은 매번 다른 방향으로 틀리는 것(손 떨리는 화살)이다. 좋은 모델은 둘 다 낮아야 한다.

## Ⅳ. 실무 적용 및 기술사 판단

### 학습 곡선 해석 및 처방

| 학습 곡선 패턴 | 진단 | 처방 |
|:---|:---|:---|
| 훈련·[[395_verification_process_review|검증]] 오류 모두 높음 | 과소적합 (고편향) | 복잡 모델 사용, [[247_feature_label_variables|피처]] 추가, 반복 증가 |
| 훈련 낮음, [[395_verification_process_review|검증]] 높음 | 과적합 (고분산) | [[093_normalization|정규화]], [[280_dropout|드롭아웃]], [[001_dikw_pyramid|데이터]] 증가, [[257_ensemble_learning|앙상블]] |
| 훈련·[[395_verification_process_review|검증]] 오류 모두 수렴 낮음 | 정상 | 하이퍼파라미터 [[133_fine_tuning|미세 조정]] |
| [[395_verification_process_review|검증]] 오류 요동 | 높은 [[136_variance|분산]] | 배치 크기 증가, [[080_gradient_descent_learning_rate|학습률]] 감소 |

### 기술사 판단 포인트

1. **[[001_dikw_pyramid|데이터]] 레이블 [[452_availability|가용성]]**: 레이블 있으면 지도, 없으면 비지도, 환경 상호작용이면 강화
2. **편향 문제**: 훈련 오류 자체가 높을 때 → 모델 복잡도·[[247_feature_label_variables|피처]] 엔지니어링
3. **[[136_variance|분산]] 문제**: 훈련-[[395_verification_process_review|검증]] 갭이 클 때 → [[093_normalization|정규화]]·더 많은 [[001_dikw_pyramid|데이터]]
4. **[[250_cross_validation_kfold|교차 검증]]**: 항상 시간 순서 [[001_dikw_pyramid|데이터]]는 TimeSeriesSplit, 불균형 [[001_dikw_pyramid|데이터]]는 Stratified

📢 **섹션 요약 비유**: 학습 곡선은 모델의 건강 검진표다. "훈련 점수만 높고 [[395_verification_process_review|검증]] 점수가 낮으면" 과적합—실제 시험에서 못하는 벼락치기 학생이다.

## Ⅴ. 기대효과 및 결론

### 학습 패러다임 선택 가이드

```
문제 정의
  │
  ├── 레이블이 있는가?
  │    ├── 예 → 지도 학습
  │    │        ├── 연속값 예측? → 회귀 (Regression)
  │    │        └── 범주 예측?  → 분류 (Classification)
  │    └── 아니오
  │         ├── 환경 상호작용? → 강화 학습
  │         └── 패턴 발견?    → 비지도 학습
  │                              ├── 군집 찾기  → 클러스터링
  │                              └── 차원 압축 → PCA / t-SNE
```

### 결론

[[241_machine_learning_basics|머신러닝]]의 세 패러다임은 서로 배타적이지 않다. 반지도 학습(Semi-Supervised)은 소량의 레이블 + 대량 레이블 없는 [[001_dikw_pyramid|데이터]]를 활용하고, [[266_self_supervised_learning|자기 지도 학습]]([[266_self_supervised_learning|Self-Supervised Learning]])은 레이블 없이 [[001_dikw_pyramid|데이터]]에서 스스로 레이블을 생성한다([[301_bert_mlm|BERT]], [[302_gpt_autoregressive|GPT]] 사전학습). [[110_bias_variance_tradeoff|편향-분산 트레이드오프]]는 이 모든 방법에서 여전히 중심 과제이며, [[250_cross_validation_kfold|교차 검증]]과 학습 곡선이 핵심 진단 도구이다.

📢 **섹션 요약 비유**: 지도·비지도·강화학습은 각각 학교 수업(정답 있음), 독서(정답 없음), 게임(점수로 배움)이다. 세 가지 방법 중 어떤 "학습 방식"이 적합한지는 내가 가진 [[001_dikw_pyramid|데이터]]와 목표가 무엇이냐에 달려 있다.

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 학습 유형 | [[121_supervised_learning|지도 학습]] ([[121_supervised_learning|Supervised Learning]]) | 레이블 있는 [[001_dikw_pyramid|데이터]]로 학습 |
| 학습 유형 | [[122_unsupervised_learning|비지도 학습]] ([[122_unsupervised_learning|Unsupervised Learning]]) | 레이블 없이 구조 발견 |
| 학습 유형 | [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] ([[094_reinforcement_learning|Reinforcement Learning]]) | 보상 [[130_signal|신호]]로 [[164_policy|정책]] 학습 |
| 오류 분석 | 편향 ([[094_bias|Bias]]) | 체계적 예측 오류 (과소적합) |
| 오류 분석 | [[136_variance|분산]] ([[136_variance|Variance]]) | 훈련 [[001_dikw_pyramid|데이터]] 민감도 (과적합) |
| 해결책 | [[093_normalization|정규화]] (L1/L2/[[242_regularization_dropout_early_stopping_l1_l2_lasso_ridge|Dropout]]) | 과적합 방지 |
| 평가 방법 | k-폴드 [[250_cross_validation_kfold|교차 검증]] | 일반화 [[282_performance_tactics|성능]] 신뢰 추정 |
| 진단 도구 | 학습 곡선 ([[240_switch_learning_forwarding_flooding|Learning]] Curve) | 편향·[[136_variance|분산]] 문제 [[003_bigdata_7v|시각화]] |

### 👶 어린이를 위한 3줄 비유 설명

1. [[121_supervised_learning|지도 학습]]은 선생님이 "이건 고양이야, 이건 강아지야"라고 알려주며 공부하는 것, [[122_unsupervised_learning|비지도 학습]]은 동물 사진 묶음을 줬을 때 스스로 비슷한 것끼리 묶는 것이다.

### 📈 관련 키워드 및 발전 흐름도

```text
지도 학습: 분류 · 회귀 (레이블 O)
비지도 학습: 군집화 · 차원 축소 (레이블 X)
강화 학습: 보상 기반 정책 최적화
    │
    ▼
편향-분산 트레이드오프 · 과적합 vs 과소적합
    │
    ▼
자기지도 학습 (Self-Supervised) → Foundation Model
```
2. 편향이 크면 항상 같은 곳을 겨냥해 빗나가는 화살(규칙이 틀림), [[136_variance|분산]]이 크면 매번 다른 곳에 꽂히는 화살(기억력이 너무 좋아 암기만 함)이다.
3. [[250_cross_validation_kfold|교차 검증]]은 한 번의 시험이 아니라 여러 번 시험 봐서 평균 점수를 재는 것이다—운으로 높은 점수를 받는 것을 막아준다.
