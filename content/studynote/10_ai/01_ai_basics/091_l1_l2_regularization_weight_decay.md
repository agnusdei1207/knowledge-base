---
title: 91. L1/L2 규제 - 가중치 감쇠(Weight Decay)와 과적합 방지
date: '2026-04-10'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: L1/L2 규제는 모델이 훈련 [[001_dikw_pyramid|데이터]]에 과도하게 집착하여 특정 [[267_weight_bias_activation|가중치]]($W$)를 비정상적으로 키우는 과적합([[245_overfitting_variance|Overfitting]])을 막기 위해 [[075_loss_function_cost_function|손실 함수]]([[087_loss_function|Loss Function]])에 [[267_weight_bias_activation|가중치]] 크기에 비례하는 수학적 벌점(Penalty)을 부여하는 기법이다.
> 2. **가치**: 파라미터 값이 튀는 것을 [[656_ir_containment|억제]]하여 모델의 예측 곡선을 부드럽게 만들고, 처음 보는 실전 [[001_dikw_pyramid|데이터]](Test Set)에 대해서도 안정적인 일반화(Generalization) [[282_performance_tactics|성능]]을 보장한다.
> 3. **판단 포인트**: 불필요한 변수를 완전히 0으로 만들어 특성 선택(Feature [[022_mcts_four_stages|Selection]])이 필요하다면 L1을, 변수 정보를 유지하면서 극단적인 [[267_weight_bias_activation|가중치]]만 억눌러 딥러닝의 전반적인 안정성을 높이려면 L2를 채택해야 한다.

---

## Ⅰ. 개요 및 필요성

L1/L2 규제 ([[134_regularization_dropout_batch_norm|Regularization]])는 기계학습 및 딥러닝 모델의 훈련 과정에서 [[075_loss_function_cost_function|손실 함수]]에 [[267_weight_bias_activation|가중치]]의 크기를 제한하는 패널티 항을 추가하는 기법이다. 모델이 학습 [[001_dikw_pyramid|데이터]]의 미세한 노이즈까지 완벽하게 암기해 버리면, 실전 [[001_dikw_pyramid|데이터]]에서 형편없는 [[282_performance_tactics|성능]]을 내는 과적합([[245_overfitting_variance|Overfitting]]) 현상에 빠지게 된다. 

이러한 과적합은 주로 특정 특징에만 과도하게 의존하여 연결된 [[267_weight_bias_activation|가중치]]가 기형적으로 커지는 형태로 나타난다. 규제 기법이 없다면 모델은 오직 오차를 줄이는 데만 혈안이 되어 파라미터를 통제 불능 상태로 키워버린다. 따라서, 오차를 줄이는 동시에 "[[267_weight_bias_activation|가중치]] 크기 자체도 작게 유지하라"는 이중 목표를 강제함으로써, 모델이 일부 노이즈에 휘둘리지 않고 본질적인 패턴에 집중하도록 유도하는 안전장치가 필수적이다.

- **📢 섹션 요약 비유**: 오직 '수학 100점 맞기(오차 최소화)'에 집착해 교과서의 오탈자까지 통째로 외우는 학생(과적합 모델)에게, 선생님이 "점수도 중요하지만, 네가 암기에 쓴 시간([[267_weight_bias_activation|가중치]] 크기)이 너무 길면 전체 성적을 깎겠다"고 선언하여 둥글둥글한 모범생으로 교정하는 과정과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

규제의 핵심 원리는 기존 [[075_loss_function_cost_function|손실 함수]](Loss)에 규제항(Penalty Term)을 더해 새로운 비용 함수(Cost Function)를 구성하는 것이다. $\[[216_lambda_kappa_architecture_batch_realtime|lambda]]$ (하이퍼파라미터)는 벌점의 강도를 조절한다.

| 구성 요소 | 수학적 의미 | 모델에 미치는 영향 |
| :--- | :--- | :--- |
| **기존 [[075_loss_function_cost_function|손실 함수]]** | 정답과 예측값의 오차 ([[076_mse_mean_squared_error_regression|MSE]], [[154_cross_entropy|Cross Entropy]] 등) | [[001_dikw_pyramid|데이터]]에 대한 적합도 향상 |
| **L1 규제항** | $\[[216_lambda_kappa_architecture_batch_realtime|lambda]] \sum \|W\|$ ([[267_weight_bias_activation|가중치]] 절댓값의 합, [[102_lasso_ridge_regression_regularization|Lasso]]) | 덜 중요한 [[267_weight_bias_activation|가중치]]를 정확히 '0'으로 만듦 (희소성) |
| **L2 규제항** | $\[[216_lambda_kappa_architecture_batch_realtime|lambda]] \sum W^2$ ([[267_weight_bias_activation|가중치]] 제곱의 합, Ridge) | 큰 [[267_weight_bias_activation|가중치]]를 강하게 억눌러 '0'에 가깝게 평탄화 (감쇠) |

```text
┌──────────────────────────────────────────────────────────────┐
│             규제 기법에 따른 가중치 최적화 경로             │
├──────────────────────────────────────────────────────────────┤
│ [오차 최소화 구역]                    [가중치 패널티 구역] │
│                                                            │
│ 손실(Loss) 작아짐  ◀──── 갈등 ────▶ 가중치(W) 커지려 함   │
│                                                            │
│ L1 규제 (마름모 꼴) : 교점이 축(0)에서 발생 ─▶ 가중치 = 0   │
│ L2 규제 (원 꼴)     : 교점이 중간에서 발생  ─▶ 가중치 억제  │
└──────────────────────────────────────────────────────────────┘
```

딥러닝에서는 주로 L2 규제를 사용하며, 이를 **[[267_weight_bias_activation|가중치]] 감쇠 ([[267_weight_bias_activation|Weight]] Decay)**라고 부른다. [[267_weight_bias_activation|가중치]]를 업데이트할 때마다 기존 [[267_weight_bias_activation|가중치]] 값에서 일정 비율을 강제로 덜어냄으로써(Decay), 어떤 뉴런 하나가 독단적으로 결과값을 지배하지 못하게 모든 뉴런이 골고루 책임을 나누도록 만든다.

- **📢 섹션 요약 비유**: L1은 성과가 안 나오는 직원의 책상을 완전히 빼버리는 극단적 구조조정([[267_weight_bias_activation|가중치]] 0)이고, L2는 100억씩 독식하는 임원들의 연봉을 대폭 깎아서 모두가 적당한 연봉을 받게 만드는 체질 개선([[267_weight_bias_activation|가중치]] 평탄화)이다.

---

## Ⅲ. 비교 및 연결

L1 규제([[102_lasso_ridge_regression_regularization|Lasso]])와 L2 규제(Ridge)는 [[267_weight_bias_activation|가중치]]를 [[656_ir_containment|억제]]하는 방식에서 극명한 경계를 보인다. 이 차이는 기하학적인 모양 차이에서 비롯되며, 활용 목적 자체를 갈라놓는다.

| 항목 | L1 규제 ([[102_lasso_ridge_regression_regularization|Lasso]]) | L2 규제 (Ridge / [[267_weight_bias_activation|Weight]] Decay) |
| :--- | :--- | :--- |
| **제약 형태** | 절댓값 (마름모 형태 경계) | 제곱합 (원 형태 경계) |
| **특성 선택 기능** | 있음 (중요치 않은 변수의 [[267_weight_bias_activation|가중치]]가 0이 됨) | 없음 (0에 한없이 가까워질 뿐 0이 되진 않음) |
| **장점** | 불필요한 [[247_feature_label_variables|피처]]를 제거하여 모델 해석력(희소성) 증가 | 미분이 수월하며 전체적인 [[267_weight_bias_activation|가중치]] 크기를 안정적으로 [[656_ir_containment|억제]] |
| **딥러닝 활용도** | 미분 불가능 지점과 정보 유실 문제로 잘 안 쓰임 | **딥러닝 [[093_normalization|정규화]]의 절대 표준 ([[267_weight_bias_activation|Weight]] Decay)** |

L1 규제는 수만 개의 변수 중 진짜 핵심만 남기는 희소 모델(Sparse Model)이 필요할 때 적합하다. 반면, L2 규제는 이미지 픽셀처럼 모든 입력 정보가 서로 연관되어 조금씩 기여해야 하는 환경에서 특정 노이즈 픽셀이 결과를 지배하는 현상을 완화하는 데 탁월하다. 이 둘을 혼합한 **[[374_elastic_net_regression|엘라스틱 넷]] ([[374_elastic_net_regression|Elastic Net]])**이라는 기법도 존재한다.

- **📢 섹션 요약 비유**: L1 규제는 짐이 무거울 때 쓸모없는 물건을 바다에 던져버리는(0으로 만듦) 선장이고, L2 규제는 모든 짐을 조금씩 [[347_compaction|압축]]해서(평탄화) 배 전체의 무게 중심을 고르게 맞추는 항해사와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 현장에서 딥러닝 모델의 Loss [[070_graph_datastructure|그래프]]를 관찰할 때, 훈련 손실(Train Loss)은 계속 떨어지는데 [[395_verification_process_review|검증]] 손실([[396_validation|Validation]] Loss)이 어느 순간 튀어 오르기 시작하면 즉각 규제 도입을 판단해야 한다.

### [[435_checklist_based_testing|체크리스트]]
1. **과적합 징후가 명확한가?** 학습 [[001_dikw_pyramid|데이터]]의 정확도와 실전(Test) 정확도의 격차가 비정상적으로 크다면 L2 규제 파라미터([[267_weight_bias_activation|Weight]] Decay)를 추가한다.
2. **하이퍼파라미터 $\[[216_lambda_kappa_architecture_batch_realtime|lambda]]$ 값이 적절한가?** $\[[216_lambda_kappa_architecture_batch_realtime|lambda]]$가 너무 크면 모델이 너무 단순해지는 과소적합([[246_underfitting_bias|Underfitting]])이 발생하고, 너무 작으면 규제 효과가 없다.
3. **입력 변수 중 의미 없는 쓰레기 [[001_dikw_pyramid|데이터]]가 많은가?** 유전자 [[001_dikw_pyramid|데이터]]처럼 [[247_feature_label_variables|피처]]는 수백만 개인데 정답과 무관한 노이즈가 대부분이라면 L1 규제를 통해 변수를 과감히 쳐낸다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 딥러닝에서 [[280_dropout|드롭아웃]]([[242_regularization_dropout_early_stopping_l1_l2_lasso_ridge|Dropout]])과 [[282_batch_normalization|배치 정규화]]([[282_batch_normalization|Batch Normalization]])를 적용하면서 무작정 큰 L2 규제를 중복해서 걸어버리는 설계. (규제가 중첩되면 학습이 아예 멈춰버리는 언더피팅의 늪에 빠진다.)
- L1 규제를 쓰면서 L2처럼 모델의 부드러움을 기대하는 설계.

- **📢 섹션 요약 비유**: 강력한 약(규제)은 병(과적합)을 고치지만, 과다 복용($\[[216_lambda_kappa_architecture_batch_realtime|lambda]]$를 너무 크게 [[009_config|설정]])하면 환자(모델)가 아예 영양실조(과소적합)에 걸려 아무것도 예측하지 못하게 된다.

---

## Ⅴ. 기대효과 및 결론

L1/L2 규제를 도입하면 훈련 [[001_dikw_pyramid|데이터]]에 대한 정확도는 소폭 떨어질 수 있으나, [[444_test_data_management|테스트 데이터]]에 대한 일반화 [[282_performance_tactics|성능]]과 예측의 안정성은 비약적으로 상승한다. 특히 딥러닝에서 L2 규제는 파라미터 폭발을 막아주어 학습 과정 자체의 수치적 안정성을 보장한다.

다만, 규제 강도를 결정하는 $\[[216_lambda_kappa_architecture_batch_realtime|lambda]]$ 값을 실험적으로 찾아야 한다는 부담이 존재하며, 최신 딥러닝에서는 [[280_dropout|드롭아웃]] 등 다른 기법들과 얽혀 복합적인 [[093_normalization|정규화]] [[268_strategy_pattern|전략]]으로 발전하고 있다. 결론적으로 L1/L2 규제는 "가장 똑똑한 모델을 만드는 것이 아니라, 가장 덜 틀리는 유연한 모델을 만드는 수학적 족쇄"로 기억해야 한다.

- **📢 섹션 요약 비유**: 안전벨트(규제)를 매면 레이싱카(모델)의 최고 속도는 조금 줄어들 수 있지만, 코너(새로운 [[001_dikw_pyramid|데이터]])를 돌 때 차가 뒤집어지는 대참사는 확실하게 막아준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **과적합 ([[245_overfitting_variance|Overfitting]])** | 규제 기법이 해결하고자 하는 가장 근본적인 문제 현상 |
| **비용 함수 (Cost Function)** | 오차(Loss)와 규제항(Penalty)이 더해져 최종적으로 최소화해야 할 수학적 목표 |
| **[[280_dropout|드롭아웃]] ([[242_regularization_dropout_early_stopping_l1_l2_lasso_ridge|Dropout]])** | 수식을 변형하는 L1/L2와 달리, 학습 중 뉴런을 [[130_probability|확률]]적으로 꺼서 과적합을 막는 아키텍처적 규제 기법 |
| **[[282_batch_normalization|배치 정규화]] ([[282_batch_normalization|Batch Normalization]])** | [[001_dikw_pyramid|데이터]] 분포를 고르게 만들어 [[267_weight_bias_activation|가중치]] 폭발을 간접적으로 막는 [[093_normalization|정규화]] 보조 수단 |

### 📈 관련 키워드 및 발전 흐름도

```text
오차 최소화 집착 (과적합 발생)
    │
    ▼
손실 함수 + 패널티 항 도입 (Regularization)
    │
    ├─────────┬─────────┐
    ▼         ▼         ▼
  L1 규제   L2 규제   Elastic Net
 (Lasso)   (Ridge)  (L1+L2 혼합)
    │         │
 희소모델   가중치감쇠
    │         │
    ▼         ▼
최신 딥러닝의 일반화 최적화 (Dropout, Batch Norm과 결합)
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[190_ai_llm_requirements_specification|AI]] 모델이 문제를 풀 때, 쓸데없는 [[167_sql_hint_optimizer_override|힌트]](배경색, 먼지)까지 전부 외우려고 하는 나쁜 버릇이 있어요.
2. 그래서 선생님이 "복잡하게 생각하면 벌점을 줄 거야!"라고 규칙을 바꿨어요.
3. 벌점을 받지 않으려고 모델이 가장 중요한 특징(강아지의 귀 모양)만 부드럽게 기억하게 되는 마법이 바로 규제([[134_regularization_dropout_batch_norm|Regularization]])랍니다.
