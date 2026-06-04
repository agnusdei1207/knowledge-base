+++
title = "271. 순전파 (Forward Propagation)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 순전파([Forward](/knowledge-base/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/) Propagation)는 입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 신경망의 입력층->은닉층->출력층 방향으로 흐르며 행렬 곱과 [활성화 함수](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/129_activation_function/)를 순차 적용해 예측값을 계산하는 과정이다.
> 2. **가치**: 순전파는 <strong>예측(Inference)</strong>만 수행하며, 중간 계산 결과(활성화 값, 선형 결합값 z)를 저장해 이후 [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/)([Backpropagation](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/))에서 기울기 계산에 활용한다.
> 3. **판단 포인트**: 연산 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)(Computational [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/888_graph/))를 이해하면 [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/)의 국소 기울기(Local Gradient) 계산이 순전파에서 이미 결정됨을 알 수 있으며, [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)([Batch Processing](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/))로 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 연산 효율을 극대화한다.

---

## Ⅰ. 개요 및 필요성

### 순전파 정의

순전파는 신경망에 입력 x를 넣으면 출력 ŷ이 계산되는 <strong>전방향 연산 흐름</strong>이다. 각 층(Layer)에서 수행되는 연산:

```
층 ℓ의 순전파 연산:
  zˡ = Wˡ × aˡ⁻¹ + bˡ    <- 선형 변환 (Linear Transformation)
  aˡ = f(zˡ)              <- 활성화 함수 적용 (Non-linear)

  여기서:
  - aˡ   : 층 ℓ의 활성화 출력 (Activation Output)
  - Wˡ   : 층 ℓ의 가중치 행렬 (Weight Matrix)
  - bˡ   : 층 ℓ의 편향 벡터 (Bias Vector)
  - zˡ   : 층 ℓ의 사전 활성화 값 (Pre-activation)
  - f    : 활성화 함수 (Activation Function)
```

### 순전파의 역할

순전파는 두 가지 목적으로 실행된다:
1. <strong>학습(<a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/">Training</a>)</strong>: 손실 계산 후 [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/) 준비 -> 중간 값 저장 필요
2. **추론(Inference)**: 학습된 모델로 새 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 예측 -> 중간 값 저장 불필요

- **📢 섹션 요약 비유**: 순전파는 수도관에서 물이 저수지(입력)에서 수도꼭지(출력)로 흐르는 과정 — 각 밸브(층)를 통과하며 압력(값)이 변환되고, 최종 수도꼭지에서 나온 물의 양을 측정해 목표 수량과 비교한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 3층 MLP 순전파 전체 흐름

```
+------------------------------------------------------------------+
|                순전파 (Forward Propagation) 흐름                  |
|                                                                  |
|  입력층         은닉층 1         은닉층 2         출력층            |
|                                                                  |
|  a⁰ = x         z¹ = W¹a⁰+b¹   z^ = W^a¹+b^   z³ = W³a^+b³    |
|  v               v               v               v              |
| [x₁]           a¹ = ReLU(z¹)   a^ = ReLU(z^)  ŷ = σ(z³)       |
| [x₂]                                                             |
| [x₃]    <------  저장: z¹,a¹  ---  저장: z^,a^  ---  저장: z³   |
|                   (역전파에서 사용)                                |
|                                                                  |
|  v                                                               |
|  손실 계산: L = loss(ŷ, y_target)                                 |
|  예) 이진 분류: L = -[y·log(ŷ) + (1-y)·log(1-ŷ)]               |
+------------------------------------------------------------------+
```

### 행렬 연산으로 이해하는 순전파

단일 샘플 (n=1):
```
z = W × x + b
  W: [n_out × n_in], x: [n_in × 1], b: [n_out × 1]
  z: [n_out × 1]
```

[배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) (N개 샘플):
```
Z = W × X + b (브로드캐스팅)
  W: [n_out × n_in], X: [n_in × N], b: [n_out × 1]
  Z: [n_out × N]
```

### 연산 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) (Computational [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/888_graph/))

```
+--------------------------------------------------------------+
|              연산 그래프 (Computational Graph)                |
|                                                              |
|  x ----------------------------------------------------+    |
|                                                         |    |
|  W --► [×] --► z = Wx+b --► [f] --► a --► [Loss] --► L|    |
|                  ^                                      |    |
|  b -------------+                          ^            |    |
|                                       y_true -----------+    |
|                                                              |
|  노드: 연산 (×, +, f, Loss)                                  |
|  엣지: 데이터 흐름                                            |
|  순전파: 왼쪽 -> 오른쪽 (예측)                                 |
|  역전파: 오른쪽 -> 왼쪽 (기울기 전파)                           |
+--------------------------------------------------------------+
```

### [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) ([Loss Function](/knowledge-base/studynote/12_it_management/02_itsm_itil/087_loss_function/)) 계산

| 문제 유형 | 출력층 | [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) |
|:---|:---|:---|
| 이진 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | [Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/) | 이진 [크로스 엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/) (Binary CE) |
| 다중 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | [Softmax](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/) | 범주형 [크로스 엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/) (Categorical CE) |
| 회귀 | Linear | [MSE](/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/) ([Mean Squared Error](/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/)) |
| 다레이블 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | [Sigmoid](/knowledge-base/studynote/10_ai/03_llm_nlp/268_sigmoid_vanishing_gradient/) × K | 이진 CE × K |

- **📢 섹션 요약 비유**: 연산 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)는 IKEA 조립 설명서 — 순전파는 그림을 따라 왼쪽에서 오른쪽으로 조립(예측), [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/)는 뭔가 틀렸을 때 오른쪽에서 왼쪽으로 분해하며 어디가 잘못됐는지 찾는 과정이다.

---

## Ⅲ. 비교 및 연결

### 순전파 vs [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/) 비교

| 비교 항목 | 순전파 ([Forward](/knowledge-base/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/)) | [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/) (Backward) |
|:---|:---|:---|
| **방향** | 입력층 -> 출력층 | 출력층 -> 입력층 |
| **목적** | 예측값(ŷ) 계산 | 기울기(∂L/∂W) 계산 |
| **연산** | 행렬 곱 + 활성화 | 연쇄 법칙 + 야코비안 |
| **저장** | z, a 값 저장 | 기울기 누적 |
| **추론 시** | ✅ 실행 | ❌ 실행 안 함 |
| **학습 시** | ✅ 실행 | ✅ 실행 |

### [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) ([Batch Processing](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/))

| 처리 방식 | 설명 | 특징 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/">확률</a>적 경사 하강 (SGD)</strong> | N=1, 샘플 1개씩 | 빠른 업데이트, 높은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) |
| <strong>미니배치 (Mini-batch <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/">GD</a>)</strong> | N=32~256, 배치 단위 | [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화, 표준 방법 |
| <strong>배치 경사 하강 (Batch <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/275_gradient_descent_sgd/">GD</a>)</strong> | N=전체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 안정적, 메모리 비효율 |

- **📢 섹션 요약 비유**: 순전파와 [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/)는 학생이 시험을 치르고 채점하는 과정 — 순전파는 답을 쓰는 것(예측), [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/)는 틀린 문제를 분석해 어떤 개념([가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/))을 더 공부해야 하는지 파악하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사 시험 핵심 논점

1. **순전파에서 저장하는 값**: z(선형 결합)와 a(활성화 출력) -> [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/)의 국소 기울기 계산에 필수
2. <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/">배치 처리</a> 효율</strong>: 행렬 연산(GEMM, General Matrix Multiply)으로 GPU에서 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 -> 단일 샘플 대비 수십~수백 배 속도
3. **순전파의 계산 복잡도**: 각 층에서 O(n_in × n_out) -> 전체 O(L × d^) (L: 층 수, d: 평균 노드 수)
4. **추론(Inference) 최적화**: [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/) 불필요 -> no_grad() 모드로 중간값 저장 생략 -> 메모리·속도 절약

### PyTorch 코드 관점 이해

```python
# 순전파 = 모델 호출
output = model(input)   # z¹, a¹, z^, a^, ..., ŷ 순차 계산

# 손실 계산
loss = criterion(output, target)   # L = CE(ŷ, y)

# 역전파 (순전파 후 실행)
loss.backward()   # ∂L/∂W, ∂L/∂b 계산

# 추론 시 - 중간 값 저장 생략
with torch.no_grad():
    output = model(input)   # 메모리 절약
```

- **📢 섹션 요약 비유**: 순전파는 공장의 제품 생산 라인 — 원자재(입력)가 각 공정(층)을 거쳐 완성품(예측값)이 되고, 품질 검사(손실 계산) 후 불량이면 역으로 어느 공정이 문제인지 추적([역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/))한다.

---

## Ⅴ. 기대효과 및 결론

### 순전파 효율화 기법

| 기법 | 내용 | 효과 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/282_batch_normalization/">배치 정규화</a> (Batch Norm)</strong> | 층 간 활성화 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | 학습 안정화, 수렴 가속 |
| <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/280_dropout/">드롭아웃</a> (<a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/242_regularization_dropout_early_stopping_l1_l2_lasso_ridge/">Dropout</a>)</strong> | 순전파 시 랜덤 뉴런 비활성화 | 과적합 방지 |
| <strong>그래디언트 <a href="/knowledge-base/studynote/16_bigdata/03_spark/071_checkpointing/">체크포인팅</a></strong> | 중간 값 일부만 저장 | 메모리 절약, 속도 트레이드오프 |
| <strong>혼합 <a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/">정밀도</a> (Mixed <a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/">Precision</a>)</strong> | FP16/BF16 연산 | 2배 메모리 절약, [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 활용도 향상 |

### 결론

순전파는 신경망의 "전방 비행" — 입력에서 예측까지의 모든 수학적 변환을 순차적으로 수행하며, 학습에 필요한 중간 값을 저장한다. 순전파 자체는 예측만 수행하지만, 저장된 중간 값이 [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/)의 기울기 계산을 가능하게 하는 핵심 토대다. 기술사 시험에서는 순전파의 연산 흐름, 저장 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/)와의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/), [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)가 주요 출제 범위다.

- **📢 섹션 요약 비유**: 순전파는 요리사가 레시피([가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/))를 따라 요리(예측)를 만드는 과정 — 요리가 완성되면 맛(손실)을 보고, 맛이 없으면 어느 단계 레시피를 수정할지([역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/)) 결정한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/) ([Backpropagation](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/)) | 연쇄 법칙, 기울기 계산 / 순전파 이후 실행되는 학습 단계 |
| 연산 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) (Computational [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/888_graph/)) | 노드, 엣지, 자동 미분 / 순전파 경로의 수학적 표현 |
| [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/) ([Loss Function](/knowledge-base/studynote/12_it_management/02_itsm_itil/087_loss_function/)) | [MSE](/knowledge-base/studynote/10_ai/01_ai_basics/076_mse_mean_squared_error_regression/), CE, 예측 오차 / 순전파 최종 단계에서 계산 |
| [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) ([Batch Processing](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)) | 미니배치, [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 / 순전파 효율화의 핵심 기법 |
| 활성화 저장 (Activation [Caching](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)) | z, a 저장, [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/) 준비 / [역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/)를 위한 순전파 부산물 |
| 추론 모드 (Inference Mode) | no_grad, 메모리 절약 / 학습 없이 순전파만 실행할 때 |

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수·기울기 계산] -> [순전파 (Forward Propagation)] -> [대규모 분산 학습·서빙 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 🏭 **"컨베이어 벨트 공장"**
2. 재료(입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 컨베이어 벨트(신경망)를 따라 이동하며 각 기계(층)에서 변환되어 완성품(예측값)이 나와요.
3. 완성품의 품질을 검사하고(손실 계산) 불량이면 어느 기계(층)가 문제인지 역방향으로 추적해요([역전파](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/)).

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 271 / 420

<- **이전**: [270. 소프트맥스 (Softmax)](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/)
**다음**: [272. 역전파 (Backpropagation)](/knowledge-base/studynote/10_ai/03_llm_nlp/272_backpropagation/) ->

---
