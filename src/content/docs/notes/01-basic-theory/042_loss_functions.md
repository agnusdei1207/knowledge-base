---
sidebar:
  order: 42
  label: "042. 손실 함수: Cross-Entropy•MSE (Loss Functions)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "손실 함수: Cross-Entropy•MSE (Loss Functions)"
date: "2026-08-17T17:03:00+09:00"
tags:
  - "notes-basic-theory"
weight: 42
extra:
  question_no: "042"
  source_status: "기출"
  source_history: "122회"
  priority: 50
  priority_note: "오류 비용을 학습 기울기로 변환"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **미분 가능한 스칼라 비용(Differentiable Scalar Cost)**: 역전파 연쇄 법칙을 적용할 수 있도록 오차를 1차 편미분 가능한 단일 실수값으로 정의한 수식.
- **역전파 기울기 산출 불가(Non-differentiable Metric Issue)**: 정확도(Accuracy)나 BLEU 같은 계단형 지표는 도함수가 거의 모든 곳에서 0이 되어 가중치를 갱신할 수 없는 한계.

</details>

- 정의/개념: 모델 예측값($\hat{y}$)과 실제값($y$) 간의 오차를 **미분 가능한 스칼라 비용(Cost)** 으로 수량화하여 가중치 갱신을 지휘하는 수학적 목적 함수
- 배경/필요성: 정확도(Accuracy) 등 계단형 비미분 평가 지표 적용 시 발생하는 **역전파 기울기 산출 불가 한계** 직면

#### 한줄 요약

- 예측과 정답 간의 오차를 미분 가능한 스칼라 비용으로 환산하여 역전파 가중치 갱신을 유도

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **최대우도추정(MLE, Maximum Likelihood Estimation)**: 정답 데이터가 관측될 결합 확률(우도)을 최대화하는 파라미터를 찾는 통계적 추정법으로, 음의 로그 우도(NLL)는 교차 엔트로피 손실과 수학적으로 완전 등가.
- **허버 손실(Huber Loss / Smooth L1)**: 오차가 작을 때는 MSE(제곱)의 매끄러운 수렴성을 취하고, 오차가 클 때는 MAE(선형)로 전환하여 이상치(Outlier) 민감도를 억제하는 강건 손실 함수.

</details>

![예측 오차에 따른 MSE MAE Huber 손실 비교 차트](/study/diagrams/loss-function-comparison.svg)

> MSE는 큰 오차에 제곱 페널티를 부여하여 이상치에 취약하나, Huber 손실은 임계치($\delta$) 초과 구간을 선형 페널티로 완화

- Softmax 결합 시 깔끔한 선형 기울기($\hat{y} - y$) 제공
- 회귀 과업에서 정규분포 가정 하의 **MSE 최적화** 지원
- 불균형 데이터 및 이상치에 대한 **손실 함수의 민감도 조절 메커니즘 지원**

#### 한줄 요약

- 과업 형태에 따라 확률 분포 오차는 교차 엔트로피, 연속 수치 오차는 MSE 및 Huber 손실로 모델링

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **손실 축소 연산(Loss Reduction)**: 미니배치 내 $N$개 개별 표본 손실($L_1, \dots, L_N$)을 단일 스칼라로 취합하는 방식(`mean` 또는 `sum`).

</details>

```text
[ 손실 함수 및 역전파 오차 생성 아키텍처 ]
┌──────────────────────────────┐
│ 모델 출력단 (Model Outputs)  │ ── 로짓(Logits) z ──► Softmax / Linear
├──────────────────────────────┤
│ 정답 라벨 (Ground Truth)     │ ── 원-핫 벡터(One-hot) y 또는 연속형 수치 y
├──────────────────────────────┤
│ 손실 함수 연산기 (Loss Fn)   │ ── Cross-Entropy: -∑ y log(p) / MSE: (y - y_hat)²
├──────────────────────────────┤
│ 배치 축소기 (Batch Reducer)  │ ── Loss = (1/N) ∑ Loss_i (스칼라화)
├──────────────────────────────┤
│ 역전파 오차 생성기 (dL/dz)   │ ── Softmax+CE 결합 시: ∂L/∂z = p - y 즉각 도출
└──────────────────────────────┘
```

선의 의미: 모델 로짓, 정답 라벨, 손실 연산, 배치 평균 축소 및 역전파 오차 생성 파이프라인.

| 구성요소 | 책임 |
|:---|:---|
| 출력단 (Logits) | 뉴런의 선형 결합 결과 벡터($z$) 제공 |
| 손실 연산기 | 과업 사양에 따라 **Cross-Entropy / MSE / Huber 오차 비용 산출** |
| 배치 축소기 | 미니배치 표본 손실들을 **평균(Mean)으로 집계하여 단일 스칼라 비용 생성** |
| 역전파 오차 생성기 | 손실 함수 미분을 통해 **출력단 오차 신호 역전송** |

#### 한줄 요약

- 모델 예측과 정답을 대조하여 표본별 손실을 계산하고, 배치 단위로 평균하여 역전파 기울기를 생성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Focal Loss**: $FL(p_t) = -(1-p_t)^\gamma \log(p_t)$ 수식으로 쉬운 표본(높은 $p_t$)의 손실 가중치를 극도로 낮추어 객체 탐지(RetinaNet) 등 극심한 클래스 불균형을 해결하는 손실 함수.

</details>

```text
학습 과업 및 데이터 특성 인입
   │
   ▼
[ 1. 과업 유형 판별 ]
├─ 분류 과업 (Classification)
│  ├─ 클래스 균형 데이터 ⟹ [ 2. Cross-Entropy Loss (-∑ y log p) ]
│  └─ 극심한 클래스 불균형 (1:1000) ⟹ [ 2. Focal Loss (-(1-pt)^γ log pt) ]
│
└─ 회귀 과업 (Regression)
   ├─ 이상치가 적고 가우시안 잡음 ⟹ [ 3. Mean Squared Error (MSE: (y-y_hat)²) ]
   └─ 극단적 이상치(Outlier) 다수 혼재 ⟹ [ 3. Huber Loss (Smooth L1) ]
   │
   ▼
[ 4. 손실 계산 및 역전파 기울기 산출 ] ──► [ 옵티마이저 가중치 갱신 ]
```

**동작 원리**

1. **과업 유형 판별**: 분류 문제인지 수치 회귀 문제인지 판별
2. **분류 손실 선정**: 확률 학습에 Cross-Entropy, 불균형 시 Focal 적용
3. **회귀 손실 선정**: 가우시안 잡음에 MSE, 이상치 혼재 시 Huber 적용
4. **손실 계산 및 역전파 기울기 산출**: 손실 편미분을 통해 가중치 갱신

#### 한줄 요약

- 분류 과업은 Cross-Entropy 및 Focal Loss, 회귀 과업은 이상치 분포에 따라 MSE와 Huber를 선택

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **주요 손실 함수 3종 비교**:
  - 교차 엔트로피 (Cross-Entropy): 분류 과업, 확률 분포 거리(KL Divergence) 최소화, 정답 오답 시 지수적 페널티.
  - 평균 제곱 오차 (MSE / L2 Loss): 회귀 과업, 가우시안 노이즈 최적, 이상치에 매우 민감.
  - 허버 손실 (Huber / Smooth L1): 회귀 과업, 오차 $|e| \le \delta$는 MSE, $|e| > \delta$는 MAE로 전환.

</details>

| 손실 함수 | 교차 엔트로피 (Cross-Entropy) | 평균 제곱 오차 (MSE / L2) | 허버 손실 (Huber / Smooth L1) |
|:---|:---|:---|:---|
| 적용 기준 | **이진/다중 분류 (Classification)** | **가우시안 잡음의 연속형 회귀** | **이상치(Outlier) 혼재 수치 회귀** |
| 핵심 특징 | **다항분포 음의 로그 우도(NLL)** 기반 | **정규분포 MLE 제곱 오차** 기반 | 임계치 $\delta$ 기준 **MSE+MAE 복합** |
| 한계 | 잘못된 고확신 예측 시 과적합 유발 | **제곱 오차로 이상치에 극도로 민감** | 전이 임계치 $\delta$ 튜닝 필요 |

#### 한줄 요약

- 확률 분류는 교차 엔트로피, 잡음이 적은 회귀는 MSE, 이상치에 강건한 회귀는 허버 손실을 적용

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Label Smoothing**: 하드 원-핫 타깃($[1, 0, 0]$)을 완화된 타깃($[0.9, 0.05, 0.05]$)으로 변환하여 모델의 과도한 확신(Over-confidence)과 과적합을 방지하는 정규화 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 회귀 모델에서 소수 이상치로 인한 **기울기 폭발 및 모델 왜곡** | **Huber Loss ($\delta=1.0$) 또는 Smooth L1** 손실 채택 | 이상치 구간 선형화로 강건한 학습 |
| 극심한 배경-객체 불균형으로 인한 **다수 클래스 편향 학습** | **Focal Loss ($\alpha=0.25, \gamma=2.0$)** 적용 | 쉬운 배경 손실 억제 및 난해 객체 집중 |
| 분류 모델의 과도한 확신으로 인한 **과적합 및 캘리브레이션 붕괴** | **라벨 스무딩(Label Smoothing, $\epsilon=0.1$)** 손실 결합 | 소프트 확률 예측 및 일반화 성능 개선 |
| 불균형 이진 분류에서 소수 클래스 재현율 저하 | `BCEWithLogitsLoss(pos_weight=...)` 가중치 부여 | 소수 양성 클래스 오류 페널티 강화 |

#### 한줄 요약

- 이상치가 많으면 Huber 손실로 영향을 억제하고, 클래스 불균형에는 Focal Loss를 적용하며, Label Smoothing으로 과적합을 완화한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **딥러닝 손실 함수 설계 표준**: 모델의 출력 형식(확률/연속값)과 데이터셋의 이상치 및 불균형 특성을 종합적으로 고려하여 손실 함수를 선택하고, 라벨 스무딩 및 클래스 가중치를 결합하여 최적화.

</details>

- 분류는 **Cross-Entropy/Focal**, 회귀는 **MSE/Huber** 선택

#### 한줄 요약

- 과업 출력의 확률적 의미와 이상치 분포를 기준으로 손실 함수를 선정하고 최적화를 수행
