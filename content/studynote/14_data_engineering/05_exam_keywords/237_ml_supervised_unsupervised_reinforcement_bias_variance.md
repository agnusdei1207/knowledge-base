+++
title = "237. 머신러닝 지도·비지도·강화학습 편향-분산 오류 종합"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)의 세 패러다임—[지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)([Supervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)), [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)([Unsupervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)), [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)([Reinforcement Learning](/knowledge-base/studynote/12_it_management/02_itsm_itil/094_reinforcement_learning/))—은 "레이블(Label) 유무"와 "보상 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)(Reward [Signal](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)) 유무"로 구분된다.
> 2. **가치**: 편향([Bias](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/))·[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)([Variance](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)) 트레이드오프는 모든 ML 모델의 근본 딜레마로, 과적합([Overfitting](/knowledge-base/studynote/10_ai/03_llm_nlp/245_overfitting_variance/))·과소적합([Underfitting](/knowledge-base/studynote/10_ai/03_llm_nlp/246_underfitting_bias/)) 진단과 [교차 검증](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/)([Cross-Validation](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/))을 통해 일반화 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 극대화한다.
> 3. **판단 포인트**: 학습 곡선([Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) Curve)으로 문제를 진단하고, 편향 문제는 모델 복잡도 증가로, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 문제는 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)([Regularization](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/134_regularization_dropout_batch_norm/))·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 증강·[앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/)로 해결한다.

## Ⅰ. 개요 및 필요성

### [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 학습 패러다임 3분류



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">머신러닝 (Machine Learning)</div>
<div class="kb-diagram-tree-item" style="--depth:0">지도 학습 (Supervised Learning)</div>
<div class="kb-diagram-note">조건: 입력 X + 레이블 Y 쌍 존재</div>
<div class="kb-diagram-note">목표: f(X) ≈ Y 함수 학습</div>
<div class="kb-diagram-note">대표: 분류(Classification), 회귀(Regression)</div>
<div class="kb-diagram-tree-item" style="--depth:0">비지도 학습 (Unsupervised Learning)</div>
<div class="kb-diagram-note">조건: 입력 X만 존재 (레이블 없음)</div>
<div class="kb-diagram-note">목표: 데이터 내재 구조·패턴 발견</div>
<div class="kb-diagram-note">대표: 클러스터링(Clustering), 차원 축소, 생성 모델</div>
<div class="kb-diagram-tree-item" style="--depth:0">강화 학습 (Reinforcement Learning)</div>
<div class="kb-diagram-note">조건: 에이전트·환경·보상 신호</div>
<div class="kb-diagram-note">목표: 누적 보상 최대화 정책(Policy) 학습</div>
<div class="kb-diagram-note">대표: Q-학습, DQN, PPO</div>
</div>
</div>



### 3가지 학습 방식 비교

| 항목 | [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/) | [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/) | [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/) |
|:---|:---|:---|:---|
| 레이블 | ✅ 필요 | ❌ 없음 | 보상 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) |
| 피드백 | 즉각적 | 없음 | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
| 목적 | 예측·[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 구조 발견 | 최적 행동 |
| 주요 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | [SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/), DT, NN | K-Means, [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) | [Q-Learning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/316_q_learning/), [PPO](/knowledge-base/studynote/10_ai/05_data_science_ml/395_ppo_clipping/) |
| 예시 | 이메일 스팸 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 고객 세분화 | 게임 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), 로봇 |

📢 **섹션 요약 비유**: [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)은 정답지 있는 시험 공부, [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)은 정답지 없이 책을 읽으며 주제를 찾는 것, [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)은 시행착오로 자전거 타기를 배우는 것이다.

## Ⅱ. 아키텍처 및 핵심 원리

### [편향-분산 트레이드오프](/knowledge-base/studynote/14_data_engineering/02_math_mining/110_bias_variance_tradeoff/) ([Bias-Variance Tradeoff](/knowledge-base/studynote/14_data_engineering/02_math_mining/110_bias_variance_tradeoff/))

모델의 예측 오류는 편향·[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)·노이즈의 합으로 분해된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">총 오류 = 편향² + 분산 + 노이즈(줄일 수 없음)</div>
<div class="kb-diagram-note">편향 (Bias):</div>
<div class="kb-diagram-note">모델의 가정이 잘못되어 발생하는 오류</div>
<div class="kb-diagram-note">→ 단순한 모델, 과소적합 (Underfitting)</div>
<div class="kb-diagram-note">분산 (Variance):</div>
<div class="kb-diagram-note">학습 데이터의 변동에 과민하게 반응</div>
<div class="kb-diagram-note">→ 복잡한 모델, 과적합 (Overfitting)</div>
</div>
</div>



<strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/110_bias_variance_tradeoff/">편향-분산 트레이드오프</a> <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/">그래프</a> (<a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/">ASCII</a>)</strong>



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">오류</div>
<div class="kb-diagram-note">(Error)</div>
<div class="kb-diagram-note">총 오류</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">╲</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">╲ 분산 (Variance)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">╲ ──</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">╲ ─</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">X ← 최적 복잡도 지점</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">──╲</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── ╲ 편향 (Bias)</div></div>
<div class="kb-diagram-tree-item" style="--depth:1">모델 복잡도</div>
<div class="kb-diagram-note">단순 복잡</div>
<div class="kb-diagram-note">(고편향) (고분산)</div>
</div>
</div>



### 과적합 vs 과소적합 진단



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">학습 곡선 (Learning Curve) 해석</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">과소적합 (Underfitting)</div><div class="kb-diagram-cell">과적합 (Overfitting)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">편향이 큰 경우</div><div class="kb-diagram-cell">분산이 큰 경우</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">오류 오류</div><div class="kb-diagram-cell">오류 오류</div></div>
<div class="kb-diagram-note">│ │ │ │ │</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ train ─val</div><div class="kb-diagram-cell">─ train ─ val</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ high</div><div class="kb-diagram-cell">high</div><div class="kb-diagram-cell">↓ low</div><div class="kb-diagram-cell">↑ high</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 모델 복잡도 증가</div><div class="kb-diagram-cell">→ 정규화·데이터 증가</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">피처 추가</div><div class="kb-diagram-cell">드롭아웃·앙상블</div></div>
</div>
</div>



### [교차 검증](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/) ([Cross-Validation](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/))

모델의 일반화 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 있게 추정하는 방법이다.

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

📢 **섹션 요약 비유**: [교차 검증](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/)은 시험 문제를 여러 세트 만들어 번갈아 시험 보는 것이다. 한 번 시험으로 운으로 높은 점수를 받는 것을 막고 진짜 실력을 측정한다.

## Ⅲ. 비교 및 연결

### 과적합 해결 기법

| 기법 | 원리 | 적용 방법 |
|:---|:---|:---|
| [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) L1 ([Lasso](/knowledge-base/studynote/14_data_engineering/02_math_mining/102_lasso_ridge_regression_regularization/)) | 불필요 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 계수 0으로 | `alpha` 하이퍼파라미터 |
| [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) L2 (Ridge) | 계수 크기 전반 축소 | `lambda` 하이퍼파라미터 |
| [드롭아웃](/knowledge-base/studynote/10_ai/03_llm_nlp/280_dropout/) ([Dropout](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/)) | 무작위 뉴런 비활성화 | `rate=0.3~0.5` |
| [조기 종료](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/) ([Early Stopping](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/)) | [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 오류 상승 시 중단 | patience [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 증강 ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Augmentation) | 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 다양화 | 이미지 회전·플립 등 |
| [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) ([Ensemble](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/)) | 여러 모델 결합 | [배깅](/knowledge-base/studynote/10_ai/03_llm_nlp/259_bagging_random_forest/)·[부스팅](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/127_boosting/) |

### [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/) 핵심 요소



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">강화 학습 (Reinforcement Learning) 구조</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">에이전트 (Agent)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">행동 (Action): at</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">환경 (Environment)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">상태 (State): s_{t+1}</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">보상 (Reward): r_{t+1}</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">에이전트 → 정책(Policy) 업데이트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">목표: 누적 보상 최대화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">G_t = R_{t+1} + γR_{t+2} + γ²R_{t+3} + ...</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">감쇠 인자 γ ∈</div><div class="kb-diagram-node">0,1</div></div>
</div>
</div>



📢 **섹션 요약 비유**: 편향은 항상 같은 방향으로 틀리는 것(낡은 지도), [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)은 매번 다른 방향으로 틀리는 것(손 떨리는 화살)이다. 좋은 모델은 둘 다 낮아야 한다.

## Ⅳ. 실무 적용 및 기술사 판단

### 학습 곡선 해석 및 처방

| 학습 곡선 패턴 | 진단 | 처방 |
|:---|:---|:---|
| 훈련·[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 오류 모두 높음 | 과소적합 (고편향) | 복잡 모델 사용, [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 추가, 반복 증가 |
| 훈련 낮음, [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 높음 | 과적합 (고분산) | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/), [드롭아웃](/knowledge-base/studynote/10_ai/03_llm_nlp/280_dropout/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 증가, [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) |
| 훈련·[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 오류 모두 수렴 낮음 | 정상 | 하이퍼파라미터 [미세 조정](/knowledge-base/studynote/10_ai/02_dl_architecture_new/133_fine_tuning/) |
| [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 오류 요동 | 높은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) | 배치 크기 증가, [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/) 감소 |

### 기술사 판단 포인트

1. <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 레이블 <a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a></strong>: 레이블 있으면 지도, 없으면 비지도, 환경 상호작용이면 강화
2. **편향 문제**: 훈련 오류 자체가 높을 때 → 모델 복잡도·[피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 엔지니어링
3. <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 문제</strong>: 훈련-[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 갭이 클 때 → [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)·더 많은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)
4. <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/">교차 검증</a></strong>: 항상 시간 순서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 TimeSeriesSplit, 불균형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 Stratified

📢 **섹션 요약 비유**: 학습 곡선은 모델의 건강 검진표다. "훈련 점수만 높고 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 점수가 낮으면" 과적합—실제 시험에서 못하는 벼락치기 학생이다.

## Ⅴ. 기대효과 및 결론

### 학습 패러다임 선택 가이드



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">문제 정의</div>
<div class="kb-diagram-tree-item" style="--depth:1">레이블이 있는가?</div>
<div class="kb-diagram-note">── 예 → 지도 학습</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── 연속값 예측? → 회귀 (Regression)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── 범주 예측? → 분류 (Classification)</div></div>
<div class="kb-diagram-note">── 아니오</div>
<div class="kb-diagram-note">── 환경 상호작용? → 강화 학습</div>
<div class="kb-diagram-note">── 패턴 발견? → 비지도 학습</div>
<div class="kb-diagram-note">── 군집 찾기 → 클러스터링</div>
<div class="kb-diagram-note">── 차원 압축 → PCA / t-SNE</div>
</div>
</div>



### 결론

[머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)의 세 패러다임은 서로 배타적이지 않다. 반지도 학습(Semi-Supervised)은 소량의 레이블 + 대량 레이블 없는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 활용하고, [자기 지도 학습](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/)([Self-Supervised Learning](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/))은 레이블 없이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 스스로 레이블을 생성한다([BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 사전학습). [편향-분산 트레이드오프](/knowledge-base/studynote/14_data_engineering/02_math_mining/110_bias_variance_tradeoff/)는 이 모든 방법에서 여전히 중심 과제이며, [교차 검증](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/)과 학습 곡선이 핵심 진단 도구이다.

📢 **섹션 요약 비유**: 지도·비지도·강화학습은 각각 학교 수업(정답 있음), 독서(정답 없음), 게임(점수로 배움)이다. 세 가지 방법 중 어떤 "학습 방식"이 적합한지는 내가 가진 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 목표가 무엇이냐에 달려 있다.

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 학습 유형 | [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/) ([Supervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)) | 레이블 있는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 학습 |
| 학습 유형 | [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/) ([Unsupervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)) | 레이블 없이 구조 발견 |
| 학습 유형 | [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/) ([Reinforcement Learning](/knowledge-base/studynote/12_it_management/02_itsm_itil/094_reinforcement_learning/)) | 보상 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)로 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 학습 |
| 오류 분석 | 편향 ([Bias](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/)) | 체계적 예측 오류 (과소적합) |
| 오류 분석 | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) ([Variance](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)) | 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 민감도 (과적합) |
| 해결책 | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) (L1/L2/[Dropout](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/)) | 과적합 방지 |
| 평가 방법 | k-폴드 [교차 검증](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/) | 일반화 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 신뢰 추정 |
| 진단 도구 | 학습 곡선 ([Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) Curve) | 편향·[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 문제 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) |

### 👶 어린이를 위한 3줄 비유 설명

1. [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)은 선생님이 "이건 고양이야, 이건 강아지야"라고 알려주며 공부하는 것, [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)은 동물 사진 묶음을 줬을 때 스스로 비슷한 것끼리 묶는 것이다.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">지도 학습: 분류 · 회귀 (레이블 O)</div>
<div class="kb-diagram-note">비지도 학습: 군집화 · 차원 축소 (레이블 X)</div>
<div class="kb-diagram-note">강화 학습: 보상 기반 정책 최적화</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">편향-분산 트레이드오프 · 과적합 vs 과소적합</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">자기지도 학습 (Self-Supervised) → Foundation Model</div>
</div>
</div>


2. 편향이 크면 항상 같은 곳을 겨냥해 빗나가는 화살(규칙이 틀림), [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)이 크면 매번 다른 곳에 꽂히는 화살(기억력이 너무 좋아 암기만 함)이다.
3. [교차 검증](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/)은 한 번의 시험이 아니라 여러 번 시험 봐서 평균 점수를 재는 것이다—운으로 높은 점수를 받는 것을 막아준다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 237 / 258

← **이전**: [236. A* 휴리스틱 (Heuristic) 미니맥스 (Minimax) MCTS (Monte Carlo Tree Search)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/236_a_star_heuristic_minimax_mcts_monte_carlo/)
**다음**: [238. SVM (Support Vector Machine) 마진 커널 트릭 나이브 베이즈 (Naive Bayes)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) →

---
