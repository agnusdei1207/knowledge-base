---
title: 271. 순전파 (Forward Propagation)
date: '2026-05-09'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 순전파([[235_forward_backward_chaining|Forward]] Propagation)는 입력 [[001_dikw_pyramid|데이터]]가 신경망의 입력층→은닉층→출력층 방향으로 흐르며 행렬 곱과 [[129_activation_function|활성화 함수]]를 순차 적용해 예측값을 계산하는 과정이다.
> 2. **가치**: 순전파는 **예측(Inference)**만 수행하며, 중간 계산 결과(활성화 값, 선형 결합값 z)를 저장해 이후 [[272_backpropagation|역전파]]([[272_backpropagation|Backpropagation]])에서 기울기 계산에 활용한다.
> 3. **판단 포인트**: 연산 [[070_graph_datastructure|그래프]](Computational [[104_graph|Graph]])를 이해하면 [[272_backpropagation|역전파]]의 국소 기울기(Local Gradient) 계산이 순전파에서 이미 결정됨을 알 수 있으며, [[228_batch_processing_hadoop_spark|배치 처리]]([[228_batch_processing_hadoop_spark|Batch Processing]])로 [[430_index_fast_full_scan|병렬]] 연산 효율을 극대화한다.

---

## Ⅰ. 개요 및 필요성

### 순전파 정의

순전파는 신경망에 입력 x를 넣으면 출력 ŷ이 계산되는 **전방향 연산 흐름**이다. 각 층(Layer)에서 수행되는 연산:

```
층 ℓ의 순전파 연산:
  zˡ = Wˡ × aˡ⁻¹ + bˡ    ← 선형 변환 (Linear Transformation)
  aˡ = f(zˡ)              ← 활성화 함수 적용 (Non-linear)

  여기서:
  - aˡ   : 층 ℓ의 활성화 출력 (Activation Output)
  - Wˡ   : 층 ℓ의 가중치 행렬 (Weight Matrix)
  - bˡ   : 층 ℓ의 편향 벡터 (Bias Vector)
  - zˡ   : 층 ℓ의 사전 활성화 값 (Pre-activation)
  - f    : 활성화 함수 (Activation Function)
```

### 순전파의 역할

순전파는 두 가지 목적으로 실행된다:
1. **학습([[588_mlops_pipeline_automation|Training]])**: 손실 계산 후 [[272_backpropagation|역전파]] 준비 → 중간 값 저장 필요
2. **추론(Inference)**: 학습된 모델로 새 [[001_dikw_pyramid|데이터]] 예측 → 중간 값 저장 불필요

- **📢 섹션 요약 비유**: 순전파는 수도관에서 물이 저수지(입력)에서 수도꼭지(출력)로 흐르는 과정 — 각 밸브(층)를 통과하며 압력(값)이 변환되고, 최종 수도꼭지에서 나온 물의 양을 측정해 목표 수량과 비교한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 3층 MLP 순전파 전체 흐름

```
┌──────────────────────────────────────────────────────────────────┐
│                순전파 (Forward Propagation) 흐름                  │
│                                                                  │
│  입력층         은닉층 1         은닉층 2         출력층            │
│                                                                  │
│  a⁰ = x         z¹ = W¹a⁰+b¹   z² = W²a¹+b²   z³ = W³a²+b³    │
│  ↓               ↓               ↓               ↓              │
│ [x₁]           a¹ = ReLU(z¹)   a² = ReLU(z²)  ŷ = σ(z³)       │
│ [x₂]                                                             │
│ [x₃]    ←─────  저장: z¹,a¹  ───  저장: z²,a²  ───  저장: z³   │
│                   (역전파에서 사용)                                │
│                                                                  │
│  ↓                                                               │
│  손실 계산: L = loss(ŷ, y_target)                                 │
│  예) 이진 분류: L = -[y·log(ŷ) + (1-y)·log(1-ŷ)]               │
└──────────────────────────────────────────────────────────────────┘
```

### 행렬 연산으로 이해하는 순전파

단일 샘플 (n=1):
```
z = W × x + b
  W: [n_out × n_in], x: [n_in × 1], b: [n_out × 1]
  z: [n_out × 1]
```

[[228_batch_processing_hadoop_spark|배치 처리]] (N개 샘플):
```
Z = W × X + b (브로드캐스팅)
  W: [n_out × n_in], X: [n_in × N], b: [n_out × 1]
  Z: [n_out × N]
```

### 연산 [[070_graph_datastructure|그래프]] (Computational [[104_graph|Graph]])

```
┌──────────────────────────────────────────────────────────────┐
│              연산 그래프 (Computational Graph)                │
│                                                              │
│  x ────────────────────────────────────────────────────┐    │
│                                                         │    │
│  W ──► [×] ──► z = Wx+b ──► [f] ──► a ──► [Loss] ──► L│    │
│                  ↑                                      │    │
│  b ─────────────┘                          ↑            │    │
│                                       y_true ───────────┘    │
│                                                              │
│  노드: 연산 (×, +, f, Loss)                                  │
│  엣지: 데이터 흐름                                            │
│  순전파: 왼쪽 → 오른쪽 (예측)                                 │
│  역전파: 오른쪽 → 왼쪽 (기울기 전파)                           │
└──────────────────────────────────────────────────────────────┘
```

### [[075_loss_function_cost_function|손실 함수]] ([[087_loss_function|Loss Function]]) 계산

| 문제 유형 | 출력층 | [[075_loss_function_cost_function|손실 함수]] |
|:---|:---|:---|
| 이진 [[104_classification_analysis|분류]] | [[268_sigmoid_vanishing_gradient|Sigmoid]] | 이진 [[154_cross_entropy|크로스 엔트로피]] (Binary CE) |
| 다중 [[104_classification_analysis|분류]] | [[270_softmax|Softmax]] | 범주형 [[154_cross_entropy|크로스 엔트로피]] (Categorical CE) |
| 회귀 | Linear | [[076_mse_mean_squared_error_regression|MSE]] ([[076_mse_mean_squared_error_regression|Mean Squared Error]]) |
| 다레이블 [[104_classification_analysis|분류]] | [[268_sigmoid_vanishing_gradient|Sigmoid]] × K | 이진 CE × K |

- **📢 섹션 요약 비유**: 연산 [[070_graph_datastructure|그래프]]는 IKEA 조립 설명서 — 순전파는 그림을 따라 왼쪽에서 오른쪽으로 조립(예측), [[272_backpropagation|역전파]]는 뭔가 틀렸을 때 오른쪽에서 왼쪽으로 분해하며 어디가 잘못됐는지 찾는 과정이다.

---

## Ⅲ. 비교 및 연결

### 순전파 vs [[272_backpropagation|역전파]] 비교

| 비교 항목 | 순전파 ([[235_forward_backward_chaining|Forward]]) | [[272_backpropagation|역전파]] (Backward) |
|:---|:---|:---|
| **방향** | 입력층 → 출력층 | 출력층 → 입력층 |
| **목적** | 예측값(ŷ) 계산 | 기울기(∂L/∂W) 계산 |
| **연산** | 행렬 곱 + 활성화 | 연쇄 법칙 + 야코비안 |
| **저장** | z, a 값 저장 | 기울기 누적 |
| **추론 시** | ✅ 실행 | ❌ 실행 안 함 |
| **학습 시** | ✅ 실행 | ✅ 실행 |

### [[228_batch_processing_hadoop_spark|배치 처리]] ([[228_batch_processing_hadoop_spark|Batch Processing]])

| 처리 방식 | 설명 | 특징 |
|:---|:---|:---|
| **[[130_probability|확률]]적 경사 하강 (SGD)** | N=1, 샘플 1개씩 | 빠른 업데이트, 높은 [[136_variance|분산]] |
| **미니배치 (Mini-batch [[275_gradient_descent_sgd|GD]])** | N=32~256, 배치 단위 | [[418_gpu|GPU]] [[430_index_fast_full_scan|병렬]]화, 표준 방법 |
| **배치 경사 하강 (Batch [[275_gradient_descent_sgd|GD]])** | N=전체 [[001_dikw_pyramid|데이터]] | 안정적, 메모리 비효율 |

- **📢 섹션 요약 비유**: 순전파와 [[272_backpropagation|역전파]]는 학생이 시험을 치르고 채점하는 과정 — 순전파는 답을 쓰는 것(예측), [[272_backpropagation|역전파]]는 틀린 문제를 분석해 어떤 개념([[267_weight_bias_activation|가중치]])을 더 공부해야 하는지 파악하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사 시험 핵심 논점

1. **순전파에서 저장하는 값**: z(선형 결합)와 a(활성화 출력) → [[272_backpropagation|역전파]]의 국소 기울기 계산에 필수
2. **[[228_batch_processing_hadoop_spark|배치 처리]] 효율**: 행렬 연산(GEMM, General Matrix Multiply)으로 GPU에서 [[430_index_fast_full_scan|병렬]] 처리 → 단일 샘플 대비 수십~수백 배 속도
3. **순전파의 계산 복잡도**: 각 층에서 O(n_in × n_out) → 전체 O(L × d²) (L: 층 수, d: 평균 노드 수)
4. **추론(Inference) 최적화**: [[272_backpropagation|역전파]] 불필요 → no_grad() 모드로 중간값 저장 생략 → 메모리·속도 절약

### PyTorch 코드 관점 이해

```python
# 순전파 = 모델 호출
output = model(input)   # z¹, a¹, z², a², ..., ŷ 순차 계산

# 손실 계산
loss = criterion(output, target)   # L = CE(ŷ, y)

# 역전파 (순전파 후 실행)
loss.backward()   # ∂L/∂W, ∂L/∂b 계산

# 추론 시 - 중간 값 저장 생략
with torch.no_grad():
    output = model(input)   # 메모리 절약
```

- **📢 섹션 요약 비유**: 순전파는 공장의 제품 생산 라인 — 원자재(입력)가 각 공정(층)을 거쳐 완성품(예측값)이 되고, 품질 검사(손실 계산) 후 불량이면 역으로 어느 공정이 문제인지 추적([[272_backpropagation|역전파]])한다.

---

## Ⅴ. 기대효과 및 결론

### 순전파 효율화 기법

| 기법 | 내용 | 효과 |
|:---|:---|:---|
| **[[282_batch_normalization|배치 정규화]] (Batch Norm)** | 층 간 활성화 [[093_normalization|정규화]] | 학습 안정화, 수렴 가속 |
| **[[280_dropout|드롭아웃]] ([[242_regularization_dropout_early_stopping_l1_l2_lasso_ridge|Dropout]])** | 순전파 시 랜덤 뉴런 비활성화 | 과적합 방지 |
| **그래디언트 [[071_checkpointing|체크포인팅]]** | 중간 값 일부만 저장 | 메모리 절약, 속도 트레이드오프 |
| **혼합 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] (Mixed [[233_precision_recall_f1_roc_auc_threshold|Precision]])** | FP16/BF16 연산 | 2배 메모리 절약, [[418_gpu|GPU]] 활용도 향상 |

### 결론

순전파는 신경망의 "전방 비행" — 입력에서 예측까지의 모든 수학적 변환을 순차적으로 수행하며, 학습에 필요한 중간 값을 저장한다. 순전파 자체는 예측만 수행하지만, 저장된 중간 값이 [[272_backpropagation|역전파]]의 기울기 계산을 가능하게 하는 핵심 토대다. 기술사 시험에서는 순전파의 연산 흐름, 저장 [[001_dikw_pyramid|데이터]], [[272_backpropagation|역전파]]와의 [[083_relationship_in_er_model|관계]], [[228_batch_processing_hadoop_spark|배치 처리]]가 주요 출제 범위다.

- **📢 섹션 요약 비유**: 순전파는 요리사가 레시피([[267_weight_bias_activation|가중치]])를 따라 요리(예측)를 만드는 과정 — 요리가 완성되면 맛(손실)을 보고, 맛이 없으면 어느 단계 레시피를 수정할지([[272_backpropagation|역전파]]) 결정한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[272_backpropagation|역전파]] ([[272_backpropagation|Backpropagation]]) | 연쇄 법칙, 기울기 계산 / 순전파 이후 실행되는 학습 단계 |
| 연산 [[070_graph_datastructure|그래프]] (Computational [[104_graph|Graph]]) | 노드, 엣지, 자동 미분 / 순전파 경로의 수학적 표현 |
| [[075_loss_function_cost_function|손실 함수]] ([[087_loss_function|Loss Function]]) | [[076_mse_mean_squared_error_regression|MSE]], CE, 예측 오차 / 순전파 최종 단계에서 계산 |
| [[228_batch_processing_hadoop_spark|배치 처리]] ([[228_batch_processing_hadoop_spark|Batch Processing]]) | 미니배치, [[418_gpu|GPU]] [[430_index_fast_full_scan|병렬]]화 / 순전파 효율화의 핵심 기법 |
| 활성화 저장 (Activation [[456_caching|Caching]]) | z, a 저장, [[272_backpropagation|역전파]] 준비 / [[272_backpropagation|역전파]]를 위한 순전파 부산물 |
| 추론 모드 (Inference Mode) | no_grad, 메모리 절약 / 학습 없이 순전파만 실행할 때 |

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수·기울기 계산] → [순전파 (Forward Propagation)] → [대규모 분산 학습·서빙 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 🏭 **"컨베이어 벨트 공장"**
2. 재료(입력 [[001_dikw_pyramid|데이터]])가 컨베이어 벨트(신경망)를 따라 이동하며 각 기계(층)에서 변환되어 완성품(예측값)이 나와요.
3. 완성품의 품질을 검사하고(손실 계산) 불량이면 어느 기계(층)가 문제인지 역방향으로 추적해요([[272_backpropagation|역전파]]).
