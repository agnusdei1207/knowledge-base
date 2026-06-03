---
title: 5. 크로스 엔트로피 (Cross-Entropy) — 분류 손실 함수
date: '2026-04-21'
tags:
- studynote-algorithm
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 크로스 [[151_entropy|엔트로피]] H(P,Q) = -Σ P(x)·log Q(x)는 *실제 분포 P를 가정하고 모델 분포 Q로 코딩할 때 평균 코드 길이* — 항상 진짜 [[151_entropy|엔트로피]] H(P) 이상이다.
> 2. **가치**: 딥러닝 [[104_classification_analysis|분류]] 학습의 표준 손실함수로, 최소화가 곧 최대우도추정 ([[143_mle|MLE]], Maximum Likelihood Estimation) 과 수학적으로 동치이며 [[272_backpropagation|역전파]]에 수치적으로 안정적이다.
> 3. **판단 포인트**: H(P,Q) = H(P) + D_KL(P‖Q) — P가 고정 레이블이면 H(P)는 상수이므로 크로스 [[151_entropy|엔트로피]] 최소화 = KL 다이버전스 최소화 = [[143_mle|MLE]] 완전 동치.

---

## Ⅰ. 개요 및 필요성

**크로스 [[151_entropy|엔트로피]] (Cross-[[151_entropy|Entropy]])** 는 두 분포 P(실제), Q(모델) 사이의 정보량 불일치를 측정한다:

```
H(P, Q) = -Σ_{x} P(x) · log Q(x)
```

직관적 해석: "실제 분포 P로 생성된 메시지를, 잘못된 분포 Q를 기준으로 설계한 코드로 인코딩할 때 필요한 평균 [[073_bit|비트]] 수"

### 핵심 부등식

```
H(P, Q) ≥ H(P)        (항등식: Q = P일 때만 등호 성립)
H(P, Q) = H(P) + D_KL(P‖Q)
```

Q가 P에서 멀수록 추가 [[073_bit|비트]] 낭비 = D_KL(P‖Q) 증가.

📢 **섹션 요약 비유**: 크로스 [[151_entropy|엔트로피]]는 "잘못된 지도로 길 찾기"다 — 실제 도시(P)와 다른 지도(Q)를 들고 가면, 올바른 지도일 때보다 더 많이 헤맨다(더 많은 [[073_bit|비트]] 낭비).

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[104_classification_analysis|분류]] 작업에서의 크로스 [[151_entropy|엔트로피]]

**이진 [[104_classification_analysis|분류]] (Binary Cross-[[151_entropy|Entropy]], BCE)**:

```
L_BCE = -[y·log(ŷ) + (1-y)·log(1-ŷ)]
```

- y: 실제 레이블 (0 or 1)
- ŷ: 모델 예측 [[130_probability|확률]] ([[268_sigmoid_vanishing_gradient|시그모이드]] 출력)

**다중 클래스 [[104_classification_analysis|분류]] (Categorical Cross-[[151_entropy|Entropy]], CCE)**:

```
L_CCE = -Σ_{c=1}^{C} y_c · log(ŷ_c)
```

- y_c: [[079_one_hot_encoding_categorical_dummy_variable|원-핫 인코딩]] 레이블
- ŷ_c: [[270_softmax|소프트맥스]] ([[270_softmax|Softmax]]) 출력 [[130_probability|확률]]

### [[270_softmax|소프트맥스]] + 크로스 [[151_entropy|엔트로피]] 연결

```
입력 로짓 z = [z₁, z₂, ..., zC]
       │
       ▼  Softmax
ŷ_c = exp(z_c) / Σ exp(z_j)
       │
       ▼  Cross-Entropy
L = -Σ y_c · log(ŷ_c)
       │
       ▼  역전파 그래디언트
∂L/∂z_c = ŷ_c - y_c     ← 매우 깔끔한 수식!
```

[[270_softmax|소프트맥스]] + CCE 조합의 그래디언트가 **예측 - 실제** 형태로 나오는 것은 [[272_backpropagation|역전파]] 수치 안정성의 핵심이다.

### 크로스 [[151_entropy|엔트로피]] vs [[076_mse_mean_squared_error_regression|MSE]] ([[076_mse_mean_squared_error_regression|Mean Squared Error]]) 비교

| 항목 | 크로스 [[151_entropy|엔트로피]] | [[076_mse_mean_squared_error_regression|MSE]] |
|:---|:---|:---|
| 용도 | [[104_classification_analysis|분류]] ([[130_probability|확률]] 출력) | 회귀 |
| 그래디언트 포화 | 없음 ([[268_sigmoid_vanishing_gradient|시그모이드]]와 결합 시) | 있음 |
| [[130_probability|확률]] 해석 | ✅ 자연스러움 | ❌ 부자연스러움 |
| [[143_mle|MLE]] 동치 | ✅ [[104_classification_analysis|분류]]기 [[143_mle|MLE]] | ✅ 가우시안 노이즈 [[143_mle|MLE]] |

📢 **섹션 요약 비유**: [[270_softmax|소프트맥스]] + 크로스 [[151_entropy|엔트로피]]의 깔끔한 그래디언트는 "정확한 GPS"와 같다 — 어디에 있고(ŷ) 어디로 가야 하는지(y)를 빼기만 하면 방향이 나온다.

---

## Ⅲ. 비교 및 연결

### MLE와의 동치 증명

모델 파라미터 θ의 최대우도 추정:

```
θ* = argmax_{θ} Σᵢ log P_θ(yᵢ|xᵢ)
   = argmin_{θ} -1/N Σᵢ log P_θ(yᵢ|xᵢ)
   = argmin_{θ} H(P_data, P_θ)       ← 크로스 엔트로피 최소화
```

따라서 **[[143_mle|MLE]] = 크로스 [[151_entropy|엔트로피]] 최소화**.

### 크로스 [[151_entropy|엔트로피]] > [[151_entropy|엔트로피]]인 이유

```
H(P, Q) - H(P) = D_KL(P‖Q) ≥ 0

   진짜 엔트로피    추가 낭비 (KL)
   (최솟값)         (Q가 P와 다를수록 증가)
```

완벽한 모델(Q = P)일 때만 크로스 [[151_entropy|엔트로피]] = [[151_entropy|엔트로피]].

### 온도 조정과 크로스 [[151_entropy|엔트로피]]

[[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]], [[263_llm_large_language_model|LLM]] ([[263_llm_large_language_model|Large Language Model]]) 샘플링에서 온도 T 사용:

```
ŷ_c(T) = exp(z_c/T) / Σ exp(z_j/T)

T > 1: 분포 평탄화 (soft labels, 더 불확실)
T < 1: 분포 첨예화 (sharper, 더 확실)
T → 0: 최댓값에 집중 (argmax)
```

📢 **섹션 요약 비유**: 온도 조정은 "자신감 조절기"다 — 온도가 높으면 모델이 "음... 여러 가능성이 있어요"(분포 평탄), 낮으면 "무조건 이거예요!"(분포 첨예)라고 답한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[104_classification_analysis|분류]]기 학습 파이프라인

```
입력 x
  │
  ▼ 신경망 forward
로짓 z (C차원)
  │
  ▼ Softmax
예측 확률 ŷ (Σŷ_c = 1)
  │
  ▼ Cross-Entropy with 원-핫 레이블 y
손실 L = -log(ŷ_y_true)      ← 정답 클래스의 로그 확률만 남음!
  │
  ▼ 역전파
∂L/∂z_c = ŷ_c - y_c
```

정답 클래스 [[130_probability|확률]]이 높을수록 L → 0, 낮을수록 L → ∞.

### 레이블 스무딩 (Label Smoothing)

원-핫 레이블 대신 스무딩된 레이블 사용:

```
y_smooth_c = (1-ε)·y_c + ε/C

예: 3-class, ε=0.1:
  원래 [1, 0, 0] → [0.933, 0.033, 0.033]
```

모델 과확신 (overconfidence) 방지 → 일반화 [[282_performance_tactics|성능]] 향상.

### 불균형 클래스 처리

| 방법 | 수식 변형 |
|:---|:---|
| 가중 크로스 [[151_entropy|엔트로피]] | L = -Σ w_c · y_c · log(ŷ_c) |
| 포컬 손실 (Focal Loss) | L = -Σ (1-ŷ_c)^γ · y_c · log(ŷ_c) |
| 클래스 균형 샘플링 | [[075_loss_function_cost_function|손실 함수]] 변경 없이 [[001_dikw_pyramid|데이터]] 재샘플링 |

포컬 손실은 [[288_object_detection_yolo_rcnn|객체 탐지]] (RetinaNet) 에서 쉬운 예시의 기여를 억제하는 데 활용.

📢 **섹션 요약 비유**: 레이블 스무딩은 "자만심 방지 장치"다 — 모델이 한 답만 100% 옳다고 믿지 않도록 조금씩 여지를 두어 더 겸손한(일반화된) 모델을 만든다.

---

## Ⅴ. 기대효과 및 결론

크로스 [[151_entropy|엔트로피]]는 **현대 딥러닝 [[104_classification_analysis|분류]]의 표준 손실함수**로 자리 잡았다. 그 이유:

1. **[[143_mle|MLE]] 동치**: [[130_probability|확률]]론적 근거가 명확
2. **그래디언트 안정성**: [[270_softmax|소프트맥스]]와 결합 시 포화 없음
3. **정보이론적 해석**: 모델과 실제 분포의 KL 거리 최소화

LLM에서는 다음 토큰 예측이 전부 크로스 [[151_entropy|엔트로피]]로 학습된다 — ChatGPT, GPT-4 등 모든 언어 모델의 사전 훈련 목표가 크로스 [[151_entropy|엔트로피]] 최소화다.

📢 **섹션 요약 비유**: 크로스 [[151_entropy|엔트로피]] 최소화는 "모범 답안 따라 [[289_cqrs_db|쓰기]]"다 — 실제 정답 분포(P)를 최대한 흉내 내도록 모델(Q)을 훈련하는 가장 자연스러운 학습 방법이다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 비고 |
|:---|:---|:---|
| H(P,Q) 크로스 [[151_entropy|엔트로피]] | H(P) + D_KL(P‖Q) | [[151_entropy|엔트로피]] + KL |
| [[143_mle|MLE]] | 크로스 [[151_entropy|엔트로피]] 최소화와 동치 | [[104_classification_analysis|분류]]기 학습 |
| [[270_softmax|소프트맥스]] | 로짓 → [[130_probability|확률]] 변환 | 다중 [[104_classification_analysis|분류]] |
| 레이블 스무딩 | 과확신 방지 [[093_normalization|정규화]] | 일반화 향상 |
| 포컬 손실 | (1-p)^γ 가중 크로스 [[151_entropy|엔트로피]] | 불균형 클래스 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[크로스 엔트로피 (Cross Entropy)]
    │
    ▼
[MLE (Maximum Likelihood Estimation)]
    │
    ▼
[소프트맥스 (Softmax)]
    │
    ▼
[레이블 스무딩 (Label Smoothing)]
    │
    ▼
[포컬 손실 (Focal Loss)]
```

이 흐름도는 크로스 [[151_entropy|엔트로피]] (Cross [[151_entropy|Entropy]])에서 출발해 포컬 손실 (Focal Loss)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. **크로스 [[151_entropy|엔트로피]]는 "잘못된 비밀 코드 [[289_cqrs_db|쓰기]]"**: 실제 언어(P)가 아닌 잘못된 언어(Q)로 쓰면 더 많은 종이([[073_bit|비트]])가 필요하다.
2. **MLE와의 동치는 "최선의 흉내"**: 선생님(실제 [[001_dikw_pyramid|데이터]])의 답을 가장 잘 따라 쓰는 것([[143_mle|MLE]]) = 크로스 [[151_entropy|엔트로피]] 최소화.
3. **레이블 스무딩은 "살짝 겸손하게"**: "반드시 이 답이야!"가 아니라 "이 답이 맞을 것 같아"로 살짝 여지를 두면 더 잘 맞히게 된다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 154 / 175

← **이전**: [[153_kl_divergence|4. KL 다이버전스 (KL Divergence, Kullback-Leibler Divergence) — 분포 차이]]
**다음**: [[155_channel_capacity|6. 채널 용량 (Channel Capacity) — 샤논 용량 공식]] →

---
