+++
title = "251. 그리드 서치 (Grid Search) / 랜덤 서치 (Random Search)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 하이퍼파라미터(Hyperparameter)는 모델이 학습으로 결정하지 못하고 사람이 직접 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)해야 하는 값이며, 그리드 서치(Grid Search)와 랜덤 서치(Random Search)는 이를 체계적으로 탐색하는 기법이다.
> 2. **가치**: 최적 하이퍼파라미터 선택은 모델 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 수십 % 향상시킬 수 있으며, 탐색 비용(시간/계산) 대비 효율을 극대화하는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 실무에서 핵심이다.
> 3. **판단 포인트**: 그리드 서치는 좁은 범위를 정밀하게 탐색할 때, 랜덤 서치는 넓은 탐색 공간에서 효율적으로 쓸 때, 베이지안 최적화(Bayesian Optimization)는 탐색 이력을 학습하며 지능적으로 탐색할 때 사용한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 파라미터 vs 하이퍼파라미터

| 구분 | 파라미터(Parameter) | 하이퍼파라미터(Hyperparameter) |
|:---|:---|:---|
| 정의 | 모델이 학습으로 결정하는 값 | 사람이 사전에 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하는 값 |
| 예시 | 신경망 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)(w, b), 선형 회귀 계수 | [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)(LR), 트리 깊이, [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 계수(λ) |
| 결정 방법 | [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/), 경사하강법 | 그리드 서치, 랜덤 서치, 베이지안 최적화 |
| 저장 위치 | 모델 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 실험 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) |

### 1.2 주요 하이퍼파라미터 예시

| 모델 | 하이퍼파라미터 | 영향 |
|:---|:---|:---|
| 신경망 | [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)([Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) Rate) | 너무 크면 발산, 너무 작으면 느린 수렴 |
| 결정 트리 | 최대 깊이(Max Depth) | 깊을수록 과대적합 위험 |
| [랜덤 포레스트](/knowledge-base/studynote/06_ict_convergence/05_data_science/353_random_forest/) | 트리 수(n_estimators) | 많을수록 안정, 계산 비용 증가 |
| [SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)([Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)), C 파라미터 | 결정 경계 복잡도 조절 |
| Ridge/[Lasso](/knowledge-base/studynote/14_data_engineering/02_math_mining/102_lasso_ridge_regression_regularization/) | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 계수(λ, [alpha](/knowledge-base/studynote/14_data_engineering/02_math_mining/068_significance_level_alpha_p_value_hypothesis/)) | 과대적합 [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/) 강도 |
| [KNN](/knowledge-base/studynote/10_ai/03_llm_nlp/262_knn/) | K 값 | 작을수록 복잡한 경계 |

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 하이퍼파라미터는 오븐 온도와 굽는 시간 같은 것이다. 반죽([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))과 레시피(모델 구조)가 같아도 온도와 시간(하이퍼파라미터)을 잘 맞춰야 맛있는 빵(좋은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))이 나온다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 탐색 기법 비교 도식

```
┌──────────────────────────────────────────────────────────┐
│            하이퍼파라미터 탐색 공간 비교                     │
│                                                          │
│  파라미터 A  │  그리드 서치      │  랜덤 서치              │
│  (학습률)    │  ● ● ● ● ●      │  ●   ●   ●            │
│  10⁻¹       │  ● ● ● ● ●      │      ● ●    ●         │
│  10⁻²       │  ● ● ● ● ●      │  ●      ●   ●         │
│  10⁻³       │  ● ● ● ● ●      │     ●    ●            │
│  10⁻⁴       │  ● ● ● ● ●      │  ●   ●       ●        │
│             └────────────────   └────────────────        │
│              파라미터 B(깊이)     파라미터 B(깊이)          │
│                                                          │
│  그리드: 격자 모든 교점 탐색 → 완전 탐색                    │
│  랜덤:   무작위 샘플링 → 같은 시간에 더 넓은 범위 탐색        │
└──────────────────────────────────────────────────────────┘
```

### 2.2 그리드 서치 (Grid Search)

- **방법**: 모든 하이퍼파라미터 후보의 <strong>데카르트 곱(<a href="/knowledge-base/studynote/05_database/07_exam_summary/412_cartesian_product/">Cartesian Product</a>)</strong> 조합을 전부 탐색
- **장점**: 지정 범위 내 최적값 보장
- **단점**: 조합 수 폭발적 증가 (파라미터 수 × 범위 크기)
- **계산 비용**: n₁ × n₂ × ... × nₖ 번 모델 학습

```
예시: LR = {0.001, 0.01, 0.1} × Depth = {3, 5, 7, 10} × λ = {0.1, 1.0}
→ 3 × 4 × 2 = 24번 모델 학습 필요
각 학습에 K=5 CV 적용 시 → 24 × 5 = 120번 학습
```

### 2.3 랜덤 서치 (Random Search)

- **방법**: 탐색 공간에서 하이퍼파라미터를 <strong>무작위 샘플링</strong>하여 n_iter번 탐색
- **장점**: 동일한 탐색 횟수에서 더 넓은 공간 탐색
- **핵심 통찰**: 중요한 파라미터가 소수일 때, 그리드 서치는 불필요한 조합에 낭비 발생

| 방법 | 탐색 횟수 20회 기준 | 탐색 범위 |
|:---|:---|:---|
| 그리드 서치 | 5×4 = 20 (각 5, 4개 값) | 매우 좁음 |
| 랜덤 서치 | 20회 무작위 | 더 넓음 |

### 2.4 베이지안 최적화 (Bayesian Optimization)

```
이전 탐색 결과(관측값)를 활용하여
다음에 탐색할 가장 유망한 지점 예측:

반복 1: 무작위 초기 탐색
반복 2: 결과 기반 확률 모델(Gaussian Process) 업데이트
반복 3: 획득 함수(Acquisition Function)로 탐색 지점 결정
...
→ 탐색 이력이 쌓일수록 더 효율적으로 최적값 근사
```

- **📢 섹션 요약 비유**: 그리드 서치는 지도의 모든 교차로를 다 방문하는 것이고, 랜덤 서치는 무작위 위치를 돌아다니는 것이다. 베이지안 최적화는 지금까지 좋은 곳이 발견된 동네 근처를 집중 탐색하는 부동산 투자 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

---

## Ⅲ. 비교 및 연결

### 3.1 탐색 기법 종합 비교

| 기법 | 탐색 방식 | 계산 비용 | 최적값 보장 | 적합 상황 |
|:---|:---|:---|:---|:---|
| 그리드 서치 | 완전 탐색 (격자 모든 점) | 매우 높음 | 격자 내 보장 | 파라미터 수 적고 범위 좁을 때 |
| 랜덤 서치 | 무작위 샘플링 | 조절 가능 | 보장 없음 | 탐색 공간 넓고 파라미터 많을 때 |
| 베이지안 최적화 | 이전 결과 기반 지능적 탐색 | 낮음 (효율적) | 보장 없음 | 탐색 비용이 매우 클 때 |
| 할버닝([Halving](/knowledge-base/studynote/06_ict_convergence/01_blockchain/062_bitcoin_halving_supply_shock/)) | [조기 종료](/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/) 기반 탐색 | 낮음 | 보장 없음 | 빠른 실험 필요 시 |

### 3.2 [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)([Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) Rate) 탐색 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)
- <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> 스케일 탐색</strong>: [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/)은 0.001~0.1 사이에서 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 균등 분포로 샘플링이 효과적
- **그리드**: {0.001, 0.01, 0.1} — 10배 간격 격자
- **랜덤**: `10^Uniform(-4, -1)` — [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 스케일 무작위

### 3.3 [하이퍼파라미터 튜닝](/knowledge-base/studynote/10_ai/01_ai_basics/041_bagging_boosting/)과 [교차 검증](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/)

```
하이퍼파라미터 튜닝 전체 프로세스:

탐색 공간 정의
→ Grid/Random/Bayesian 중 선택
→ 각 후보에 K-Fold CV 적용
→ CV 평균 성능 기준 최적 파라미터 선택
→ 최적 파라미터로 전체 훈련 데이터 재학습
→ 테스트 세트 최종 평가
```

- **📢 섹션 요약 비유**: 그리드 서치는 수능 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 모든 기출문제 유형을 빠짐없이 풀어보는 것이고, 랜덤 서치는 무작위로 여러 단원에서 골고루 풀어보는 것이다. 베이지안 최적화는 "이 단원에서 자꾸 틀리네, 집중 공략하자"는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 실무 권장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| 상황 | 권장 기법 | 이유 |
|:---|:---|:---|
| 파라미터 1~2개, 좁은 범위 | 그리드 서치 | 완전 탐색 가능 |
| 파라미터 3개 이상 | 랜덤 서치 | 차원의 저주 방지 |
| 모델 학습 비용 높음 (딥러닝) | 베이지안 최적화 | 탐색 횟수 최소화 |
| 빠른 프로토타이핑 | 랜덤 서치 (n_iter=20~50) | 빠른 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 범위 파악 |

### 4.2 탐색 공간 설계 원칙

```
좋은 탐색 공간:
  학습률: [1e-5, 1e-1] (로그 스케일)  ← 수십 배 범위
  트리 깊이: {3, 5, 7, 10, 15}
  정규화: [1e-4, 1e2] (로그 스케일)

나쁜 탐색 공간:
  학습률: {0.001, 0.0011, 0.0012, ...} ← 너무 촘촘
  트리 깊이: {3, 4} ← 너무 좁음
```

### 4.3 기술사 핵심 판단 포인트
- **모델 학습 횟수 계산**: `그리드 서치 = Π(각 파라미터 후보 수) × K(CV fold 수)`
- **랜덤 서치 우수성**: Bergstra & Bengio(2012) 논증 — 중요 파라미터 적을 때 랜덤이 그리드 대비 효율적
- <strong>내부/외부 <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/">교차 검증</a>(Nested <a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/156_cv_cost_variance/">CV</a>)</strong>: 튜닝과 평가를 이중 루프로 분리하여 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 추정 편향 방지

- **📢 섹션 요약 비유**: 파라미터가 10개인 그리드 서치는 10가지 요리 재료를 각각 5가지 양으로 조합 시험하는 것 — 5^[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) = 약 천만 번의 요리 실험이 필요하다. 랜덤 서치는 100번만 랜덤으로 조합을 시도해도 꽤 좋은 레시피를 찾을 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [하이퍼파라미터 튜닝](/knowledge-base/studynote/10_ai/01_ai_basics/041_bagging_boosting/)의 기대효과
- [베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/) 대비 예측 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 수십 % 향상 가능
- 모델 안정성 및 일반화 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 확보
- 불필요한 컴퓨팅 리소스 낭비 방지

### 5.2 결론
[하이퍼파라미터 튜닝](/knowledge-base/studynote/10_ai/01_ai_basics/041_bagging_boosting/)은 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최대화를 위한 필수 과정이다. 그리드 서치는 정밀하지만 비용이 크고, 랜덤 서치는 넓은 공간을 효율적으로 탐색하며, 베이지안 최적화는 탐색 이력을 활용하여 지능적으로 최적값을 찾는다. 기술사 시험에서는 파라미터와 하이퍼파라미터의 차이, 각 탐색 기법의 원리와 비교를 명확히 서술할 수 있어야 한다.

- **📢 섹션 요약 비유**: [하이퍼파라미터 튜닝](/knowledge-base/studynote/10_ai/01_ai_basics/041_bagging_boosting/)은 사진 작가가 최적의 카메라 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)(조리개, 셔터속도, ISO)을 찾는 것이다. 카메라(모델) 자체를 바꾸지 않아도 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)(하이퍼파라미터) 최적화만으로 사진 품질을 극적으로 개선할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 하이퍼파라미터 | [학습률](/knowledge-base/studynote/10_ai/01_ai_basics/080_gradient_descent_learning_rate/), 트리 깊이, [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 계수 / 사람이 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하는 모델 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)값 |
| 그리드 서치 | 완전 탐색, 데카르트 곱 / 하이퍼파라미터 탐색 기법 |
| 랜덤 서치 | 무작위 샘플링, 넓은 탐색 / 하이퍼파라미터 탐색 기법 |
| 베이지안 최적화 | Gaussian [Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/), 획득 함수 / 지능적 하이퍼파라미터 탐색 |
| K-Fold [CV](/knowledge-base/studynote/12_it_management/04_sdlc_testing/156_cv_cost_variance/) | [교차 검증](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/), [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 추정 / 각 후보 평가에 함께 사용 |
| 파라미터 | [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/), [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/) 학습 / 하이퍼파라미터와 대비 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] → [그리드 서치 (Grid Search) / 랜덤 서치 (Random Search)] → [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [하이퍼파라미터 튜닝](/knowledge-base/studynote/10_ai/01_ai_basics/041_bagging_boosting/)은 <strong>게임 캐릭터 스탯 포인트</strong>를 어디에 넣을지 정하는 것이에요.
2. 그리드 서치는 모든 조합을 다 써보는 것이고, 랜덤 서치는 무작위로 여러 조합을 테스트해요.
3. 베이지안 최적화는 "이 스탯 조합이 지금까지 제일 강했으니까 비슷하게 더 조정해볼게"라는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 251 / 420

← **이전**: [250. 교차 검증 (Cross-Validation)](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/)
**다음**: [252. 혼동 행렬 (Confusion Matrix)](/knowledge-base/studynote/10_ai/03_llm_nlp/252_confusion_matrix/) →

---
