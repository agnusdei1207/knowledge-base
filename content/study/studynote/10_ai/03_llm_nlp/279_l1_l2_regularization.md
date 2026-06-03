+++
weight = 279
title = "279. L1/L2 규제 (Regularization)"
date = "2026-05-09"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: L1 규제([[102_lasso_ridge_regression_regularization|Lasso]], Least Absolute Shrinkage and [[022_mcts_four_stages|Selection]] [[565_operator_pattern_kubernetes_automation|Operator]])는 λΣ|w|, L2 규제(Ridge)는 λΣw²의 페널티를 [[075_loss_function_cost_function|손실 함수]]에 추가해 [[267_weight_bias_activation|가중치]]가 커지는 것을 [[656_ir_containment|억제]]하며, L1은 희소 해(Sparse Solution)를, L2는 전체 [[267_weight_bias_activation|가중치]]의 균형 있는 축소를 유도한다.
> 2. **가치**: L1은 불필요한 특성을 자동으로 제거하는 특성 선택(Feature [[022_mcts_four_stages|Selection]]) 효과가 있고, L2는 학습을 안정화하는 [[267_weight_bias_activation|가중치]] 감쇠([[091_l1_l2_regularization_weight_decay|Weight Decay]]) 효과로 딥러닝에서 널리 사용된다.
> 3. **판단 포인트**: 기술사 시험에서 L1과 L2의 기하학적 해석(L1은 다이아몬드, L2는 원형 제약 영역), 희소 해 발생 이유, 엘라스틱넷([[374_elastic_net_regression|Elastic Net]])의 목적을 묻는 문제가 출제된다.

---

## Ⅰ. 개요 및 필요성

딥러닝 모델의 [[075_loss_function_cost_function|손실 함수]]는 **예측 오차(Prediction Error)만 최소화**하도록 설계되므로, [[267_weight_bias_activation|가중치]]가 불필요하게 커져도 제약이 없다. 큰 [[267_weight_bias_activation|가중치]]는:

- 특정 특성에 과도하게 의존 → 과적합
- 입력의 미세한 변화에 극단적으로 반응 → 불안정

L1/L2 규제는 [[075_loss_function_cost_function|손실 함수]]에 **[[267_weight_bias_activation|가중치]] 크기에 비례하는 페널티(Penalty)를 추가**해 [[267_weight_bias_activation|가중치]]가 작게 유지되도록 강제한다:

```
규제된 손실 = 원래 손실 + λ · 규제항
L1: J(w) = L(w) + λΣ|w_i|
L2: J(w) = L(w) + λΣw_i²
```

- **📢 섹션 요약 비유**: L1/L2는 학생의 짐 가방(모델)이 너무 무거워지지 않도록 "짐을 버릴수록 가산점"을 주는 제도다. L1은 작은 짐(작은 [[267_weight_bias_activation|가중치]])을 통째로 버리게 하고, L2는 모든 짐을 골고루 조금씩 줄이게 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### L1 vs L2 규제 수식 비교

```
┌────────────────────────────────────────────────────────────┐
│                  L1 vs L2 규제 비교                        │
├──────────────────────────┬─────────────────────────────────┤
│        L1 규제 (Lasso)   │       L2 규제 (Ridge)           │
├──────────────────────────┼─────────────────────────────────┤
│  페널티: λΣ|w_i|         │  페널티: λΣw_i²                │
│                          │                                 │
│  미분: λ·sign(w_i)       │  미분: 2λ·w_i                  │
│  (부호 함수)             │  (선형 비례)                    │
│                          │                                 │
│  w → 0 에서 불연속       │  w → 0 에서 연속               │
│  (Subgradient 필요)      │  (Smooth)                       │
│                          │                                 │
│  결과: 일부 w = 0 (희소) │  결과: 모든 w ≈ 0 (작게 축소)  │
└──────────────────────────┴─────────────────────────────────┘
```

### 기하학적 해석

```
L1 제약 (다이아몬드)           L2 제약 (원/구)

      w2                             w2
       │   ●                          │     ●
       │  /│\        손실 등고선       │    /│\
       │ / │ \       접점에서 최솟값   │   / │ \
     ──┼───●──┼──→ w1           ──────┼───●────┼──→ w1
       │ \ │ /                        │   \ │ /
       │  \│/      ◆ L1의 꼭짓점에서  │    \│/
       │   ●       접하면 w=0 발생     │     ●
                   → 희소 해!         반드시 꼭짓점 없음
```

L1의 다이아몬드 모양 꼭짓점(축 위)에서 손실 등고선이 접할 가능성이 높아, 해당 [[267_weight_bias_activation|가중치]]가 **정확히 0**이 된다 → 특성 선택 효과.

### [[267_weight_bias_activation|가중치]] 갱신에서의 차이

| 항목 | L1 ([[102_lasso_ridge_regression_regularization|Lasso]]) | L2 (Ridge) |
|:---|:---|:---|
| 페널티 미분 | λ·sign(w) (±λ 상수) | 2λ·w (w에 비례) |
| 큰 [[267_weight_bias_activation|가중치]]에 대한 페널티 | 동일 (크기 무관) | 더 큰 페널티 (제곱 비례) |
| 작은 [[267_weight_bias_activation|가중치]]에 대한 페널티 | 동일 (크기 무관) | 더 작은 페널티 |
| w = 0 만들 수 있는가 | ✓ 가능 (완전 제거) | ✗ 0에 수렴만 (완전 제거 불가) |
| 희소 모델 | ✓ | ✗ |

### 엘라스틱넷([[374_elastic_net_regression|Elastic Net]])

L1과 L2를 선형 결합한 규제:

```
Elastic Net: J(w) = L(w) + λ1·Σ|w_i| + λ2·Σw_i²
```

- **r (혼합 비율, Mix Ratio)**: r=1이면 L1, r=0이면 L2
- **장점**: L1의 희소성 + L2의 안정성 동시 확보
- **사용처**: 특성 수가 많고 일부 특성이 상관된 경우

- **📢 섹션 요약 비유**: L1은 가차 없는 다이어트 코치("이것도 버려, 저것도 버려")이고, L2는 엄격하지만 부드러운 코치("모든 걸 조금씩만 줄여")다. 엘라스틱넷은 두 코치를 함께 고용하는 것이다.

---

## Ⅲ. 비교 및 연결

### λ ([[093_normalization|정규화]] 강도)의 역할

```
λ = 0       →  규제 없음 (원래 손실만 최적화)
λ = 작음    →  약한 규제 (원래 목적 + 약한 가중치 제약)
λ = 적당    →  균형 잡힌 일반화
λ = 큰 값   →  강한 규제 (가중치 → 0, 과소적합 위험)
```

### 딥러닝에서의 L2 사용 = [[267_weight_bias_activation|가중치]] 감쇠([[091_l1_l2_regularization_weight_decay|Weight Decay]])

딥러닝에서 L2 규제는 주로 **[[267_weight_bias_activation|가중치]] 감쇠([[091_l1_l2_regularization_weight_decay|Weight Decay]])**라는 이름으로 사용된다. [[277_adam_optimizer|Adam]] [[163_optimizer_sql_execution_plan_generator|옵티마이저]]에서는 L2 규제를 그래디언트에 더하는 방식과, [[267_weight_bias_activation|가중치]]에 직접 감쇠를 적용하는 AdamW 방식이 구분된다.

### L1이 자주 사용되는 경우

- 수백만 개의 특성 중 소수만 실제로 유용한 경우 (유전체 [[001_dikw_pyramid|데이터]], 텍스트 [[104_classification_analysis|분류]])
- 모델 해석 가능성이 필요한 경우 (어떤 특성이 중요한지 파악)
- [[347_compaction|압축]]([[159_compression|Compression]]) 및 경량화([[435_pruning_hardware|Pruning]])가 필요한 엣지 [[190_ai_llm_requirements_specification|AI]]

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [[009_config|설정]] | 작은 규모, 개념 학습 |
| L1/L2 규제 ([[134_regularization_dropout_batch_norm|Regularization]]) | [[282_performance_tactics|성능]]과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [[090_service_kubernetes_network_load_balancing|서비스]] 고도화 단계 |

- **📢 섹션 요약 비유**: L1 규제는 "많이 팔리지 않는 상품은 재고에서 완전 제거"하는 편의점 재고 관리이고, L2는 "모든 상품의 재고를 조금씩 줄이는" 방식이다. 편의점은 상황에 따라 두 [[268_strategy_pattern|전략]]을 조합해 쓴다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사 시험 판단 포인트

1. **L1 희소 해 원인**: 다이아몬드 모양 제약 조건의 꼭짓점에서 [[075_loss_function_cost_function|손실 함수]]와 접하기 때문
2. **L2 [[267_weight_bias_activation|가중치]] 감쇠**: 기울기 갱신 시 w_t+1 = (1-2αλ)·w_t - α·∇L(w_t)로 매 스텝 w를 일정 비율 감소
3. **λ 선택**: [[250_cross_validation_kfold|교차 검증]]([[250_cross_validation_kfold|Cross-Validation]])으로 최적 λ 탐색
4. **[[374_elastic_net_regression|Elastic Net]] 적용**: L1+L2가 모두 필요할 때, r=0.5로 시작해 탐색

### 실무 시나리오

- **신경망 [[696_fibre_channel_protocol|FC]] 레이어**: L2([[091_l1_l2_regularization_weight_decay|Weight Decay]] 1e-4) + [[242_regularization_dropout_early_stopping_l1_l2_lasso_ridge|Dropout]] 조합이 표준
- **선형 회귀/[[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]]**: 특성이 많으면 L1([[102_lasso_ridge_regression_regularization|Lasso]]), [[080_multicollinearity_vif_variance_inflation_factor_regression|다중 공선성]]이 있으면 L2(Ridge)
- **모델 프루닝([[435_pruning_hardware|Pruning]])**: L1 규제로 0이 된 [[267_weight_bias_activation|가중치]]를 제거해 경량 모델 [[087_process_state_transition|생성]]

### L1/L2 규제 코드 패턴

```python
# PyTorch에서 L2 규제 (Weight Decay)
optimizer = torch.optim.Adam(model.parameters(),
                             lr=0.001,
                             weight_decay=1e-4)  # L2 강도 λ

# PyTorch에서 L1 규제 (수동 추가)
l1_lambda = 1e-4
l1_loss = sum(p.abs().sum() for p in model.parameters())
loss = criterion(output, target) + l1_lambda * l1_loss
```

- **📢 섹션 요약 비유**: L2 규제([[267_weight_bias_activation|가중치]] 감쇠)는 모든 직원([[267_weight_bias_activation|가중치]])의 월급을 매달 1% 자동 삭감하는 회사 [[164_policy|정책]]과 같다. 열심히 일하는 직원(중요한 [[267_weight_bias_activation|가중치]])은 충분한 월급을 받지만, 게으른 직원(불필요한 [[267_weight_bias_activation|가중치]])은 결국 최저 수준으로 줄어든다.

---

## Ⅴ. 기대효과 및 결론

L1/L2 규제의 적용 효과:

1. **과적합 감소**: [[267_weight_bias_activation|가중치]]가 작아져 입력 노이즈에 덜 민감한 모델
2. **특성 선택 (L1)**: 관련 없는 특성의 [[267_weight_bias_activation|가중치]]를 0으로 만들어 모델 해석 용이
3. **학습 안정화 (L2)**: 큰 [[267_weight_bias_activation|가중치]]를 [[656_ir_containment|억제]]해 그래디언트 폭발 방지
4. **모델 경량화**: L1 규제 후 0 [[267_weight_bias_activation|가중치]] 제거로 추론 속도 향상

λ의 최적값은 문제에 따라 다르므로 반드시 **[[250_cross_validation_kfold|교차 검증]]([[250_cross_validation_kfold|Cross-Validation]])** 또는 **하이퍼파라미터 탐색(Hyperparameter Search)**을 통해 결정해야 한다.

- **📢 섹션 요약 비유**: L1/L2 규제는 모델이 가진 정보를 "필요한 것만 남기는" 미니멀리즘이다. L1은 "쓰지 않는 건 다 버려", L2는 "모든 걸 조금씩 줄여"라는 원칙으로, 결국 더 가볍고 일반적인 모델을 만들어낸다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| L1 규제 ([[102_lasso_ridge_regression_regularization|Lasso]]) | λΣ / w / , 희소 해, 특성 선택 / [[267_weight_bias_activation|가중치]] 절댓값 페널티 |
| L2 규제 (Ridge) | λΣw², [[267_weight_bias_activation|가중치]] 감쇠 / [[267_weight_bias_activation|가중치]] 제곱 페널티 |
| 엘라스틱넷 ([[374_elastic_net_regression|Elastic Net]]) | L1+L2, 혼합 비율 / L1/L2 선형 결합 |
| 희소 해 (Sparse Solution) | [[267_weight_bias_activation|가중치]]=0, 특성 제거 / L1 규제의 핵심 효과 |
| [[267_weight_bias_activation|가중치]] 감쇠 ([[091_l1_l2_regularization_weight_decay|Weight Decay]]) | AdamW, L2 / L2의 딥러닝 구현 방식 |
| 과적합 ([[245_overfitting_variance|Overfitting]]) | 일반화 [[282_performance_tactics|성능]] / L1/L2 규제가 방지하는 문제 |

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수·기울기 계산] → [L1/L2 규제 (Regularization)] → [대규모 분산 학습·서빙 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. L1 규제는 중요하지 않은 물건을 쓰레기통에 완전히 버리는 정리정돈이고, L2는 모든 물건을 조금씩 줄이는 미니멀리즘이에요.
2. 버린 물건(L1의 0 [[267_weight_bias_activation|가중치]])이 있으면 방(모델)이 더 깔끔하고 뭐가 중요한지 알기 쉬워요.
3. λ는 "얼마나 엄격하게 버릴까" 결정하는 강도인데, 너무 강하면 필요한 것도 버려서(과소적합) 곤란해요.
