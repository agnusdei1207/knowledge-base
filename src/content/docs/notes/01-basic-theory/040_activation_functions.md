---
sidebar:
  order: 40
  label: "040. 활성화 함수: ReLU•Sigmoid•Tanh (Activation Functions)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "활성화 함수: ReLU•Sigmoid•Tanh (Activation Functions)"
date: "2026-08-17T09:25:00+09:00"
tags:
  - "notes-basic-theory"
weight: 40
extra:
  question_no: "040"
  source_status: "기출"
  source_history: "120회"
  priority: 30
  priority_note: "함수별 출력 범위•기울기 비교"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **활성화 함수(Activation Function)**: 인공신경망의 각 뉴런에서 가중합(Weighted Sum, $z = \mathbf{w}^T\mathbf{x} + b$)을 입력받아 비선형 활성값($a = f(z)$)으로 변환하는 수학 함수.
- **비선형성(Nonlinearity)**: 다층 신경망(MLP)이 단순 선형 결합($W_2(W_1X) = W_{new}X$)으로 축퇴되는 것을 방지하고 임의의 복잡한 함수를 근사(Universal Approximation Theorem)할 수 있도록 보장하는 성질.
- **기울기 소실(Vanishing Gradient)**: 역전파 연쇄 법칙(Chain Rule) 적용 시 1보다 작은 도함수($f'(z) < 1$)가 여러 층에 걸쳐 누적 곱해져 초기 층의 가중치 갱신 기울기가 0으로 소멸하는 현상.

</details>

- 정의/개념: 선형 결합된 입력 신호에 비선형 변환을 부여하여 심층 신경망의 복잡한 결정 경계 학습을 가능케 하고 역전파 시 도함수로 기울기를 전달하는 **신경망 핵심 수학 소자**
- 배경/필요성: 비선형 함수 부재 시 아무리 깊은 심층망도 단일 선형 회귀와 등가가 되며, 초기 Sigmoid의 양극단 포화로 인한 **기울기 소실 문제를 극복하기 위한 ReLU 계열 도입 필수**

#### 한줄 요약

- 뉴런의 가중합을 비선형 출력으로 변환하여 신경망의 표현력을 극대화하고 역전파 기울기를 전달

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **영중심(Zero-Centered)**: 함수의 출력 범위가 0을 중심으로 양수와 음수를 고르게 대칭 출력하여($[-1, 1]$) 가중치 갱신 시 지그재그 경로(Zigzag Dynamics)를 방지하는 특성.
- **Dying ReLU**: 입력이 음수일 때 기울기가 0이 되어 가중치가 전혀 갱신되지 않고 영구적으로 비활성화되는 현상.

</details>

![Sigmoid Tanh ReLU 활성화 함수 비교 차트](/study/diagrams/activation-function-comparison.svg)

> Sigmoid와 Tanh는 큰 절댓값 입력에서 도함수가 0으로 포화되나, ReLU는 양수 구간에서 도함수 1을 유지하여 기울기 소실 방지

- **비선형 매핑을 통한 범용 함수 근사(Universal Function Approximation)** 지원
- ReLU의 양수 구간 도함수 1($f'(z)=1$) 유지로 **심층망에서의 기울기 소실(Vanishing Gradient) 극복**
- Sigmoid의 비영중심(Non Zero-Centered) 한계 및 Tanh의 영중심 대칭성

#### 한줄 요약

- 출력 범위와 도함수 포화 특성에 따라 기울기 전달력이 결정되며, 양수 구간 선형성을 갖는 ReLU가 심층 학습의 표준

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **신경망 뉴런 연산 파이프라인**: 입력 벡터 $\mathbf{x}$ $\to$ 선형 가중합 $z = \sum w_i x_i + b$ $\to$ 비선형 변환 $a = f(z)$ $\to$ 차기 층 전달.

</details>

```text
[ 인공 뉴런 내부의 활성화 함수 변환 구조 ]
  입력 x1 ──(w1)──┐
  입력 x2 ──(w2)──┼──► [ 선형 결합기: z = Wx + b ] ──► [ 활성화 함수: a = f(z) ] ──► 출력 a
  입력 x3 ──(w3)──┘              │                                 │
  편향 b ─────────┘              ▼ (역전파)                        ▼ (역전파)
                          [ ∂L/∂W = ∂L/∂z · x ] ◄── [ ∂L/∂z = ∂L/∂a · f'(z) ]
```

선의 의미: 순전파 선형 가중합 및 비선형 활성화, 역전파 도함수 연쇄 법칙 전파 구조도.

| 구성요소 | 책임 |
|:---|:---|
| 선형 결합기 ($z = \mathbf{w}^T\mathbf{x} + b$) | 입력과 가중치의 행렬곱 및 편향 가산 수행 |
| 활성화 함수 ($a = f(z)$) | 가중합에 **비선형 함수를 적용하여 출력 신호 강도 결정** |
| 도함수 연산기 ($f'(z)$) | 역전파 시 상위 층 손실 기울기에 **국소 기울기($f'(z)$)를 곱해 하위 층 전달** |

#### 한줄 요약

- 활성화 함수가 이전 층의 가중합을 비선형 값으로 바꾸고, 역전파 때 도함수만큼 기울기를 전달

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **순환 순전파-역전파**: 순전파 시 활성화 함수 출력 $a$를 기록하고, 역전파 시 저장된 $z$를 바탕으로 도함수 $f'(z)$를 곱해 연쇄 법칙을 완성.

</details>

```text
순전파 (Forward Pass)
   │
   ▼
[ 1. 가중합 z = Wx + b 계산 ]
   │
   ▼
[ 2. 비선형 활성값 a = f(z) 산출 및 캐싱 ] ──► [ 다음 은닉층 / 손실 함수 인입 ]
 
============================================================
 
역전파 (Backward Pass)
   │
   ▼
[ 3. 상위 층 손실 기울기 ∂L/∂a 수신 ]
   │
   ▼
[ 4. 활성화 함수 국소 도함수 f'(z) 계산 ]
├─ Sigmoid: f'(z) = a(1-a) (최대 0.25)
├─ Tanh: f'(z) = 1 - a² (최대 1.0)
└─ ReLU: f'(z) = 1 (if z>0) else 0
   │
   ▼
[ 5. 연쇄 법칙 적용: ∂L/∂z = (∂L/∂a) × f'(z) ──► 하위 층 가중치 갱신 ]
```

**동작 원리**

1. **가중합 연산**: 입력 벡터와 가중치 행렬을 곱하여 선형 스칼라/벡터 $z$ 생성
2. **비선형 변환**: 활성화 함수 $f(z)$를 통과시켜 활성값 $a$를 산출하고 다음 층으로 전달
3. **손실 기울기 수신**: 손실 함수로부터 역전파된 오차 신호 $\frac{\partial L}{\partial a}$ 인입
4. **도함수 연쇄 곱**: 활성화 함수의 1차 도함수 $f'(z)$를 곱하여 선형 입력단 오차 $\frac{\partial L}{\partial z}$ 도출
5. **하위 층 전파**: 가중치 기울기 $\frac{\partial L}{\partial W}$를 계산하고 이전 레이어로 오차 신호 전달

#### 한줄 요약

- 순전파 시 비선형 활성값을 전파하고, 역전파 시 해당 지점의 도함수를 곱해 오차 기울기를 역전달

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **주요 활성화 함수 수식**:
  - Sigmoid: $\sigma(z) = \frac{1}{1 + e^{-z}}$, 출력 $(0, 1)$, 도함수 최댓값 $0.25$.
  - Tanh: $\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$, 출력 $(-1, 1)$, 영중심 대칭.
  - ReLU: $f(z) = \max(0, z)$, 출력 $[0, \infty)$, 연산 초고속, 도함수 $1$ (양수).

</details>

| 비교 항목 | Sigmoid | Tanh | ReLU (Rectified Linear Unit) |
|:---|:---|:---|:---|
| 수식 | $f(z) = \frac{1}{1 + e^{-z}}$ | $f(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$ | $f(z) = \max(0, z)$ |
| 출력 범위 | $(0, 1)$ | $(-1, 1)$ (영중심) | $[0, \infty)$ |
| 도함수 최댓값 | **$0.25$ (심각한 기울기 소실)** | **$1.0$ (포화 시 소실)** | **$1.0$ (양수 구간 소실 없음)** |
| 주 적용처 | **이진 분류 최종 출력층** | RNN/LSTM 순환 은닉 상태 | **심층 신경망(CNN, MLP) 은닉층 표준** |
| 한계 및 위험 | 기울기 소실, 비영중심 | 양극단($|z| \gg 0$) 포화 시 기울기 소실 | **Dying ReLU (음수 뉴런 영구 불능)** |

#### 한줄 요약

- 이진 확률 출력은 Sigmoid, 순환 제어는 Tanh, 심층 신경망의 은닉층 학습은 ReLU를 적용

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Leaky ReLU / PReLU**: $f(z) = \max(\alpha z, z)$로 음수 구간에 작은 기울기($\alpha=0.01$)를 부여하여 Dying ReLU를 방지하는 함수.
- **GELU(Gaussian Error Linear Unit)**: 입력의 정규분포 누적확률을 반영하여 가중치를 부여하는 트랜스포머(BERT, GPT) 표준 활성화 함수 ($f(x) = x \Phi(x)$).

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Sigmoid의 은닉층 적용 시 **심각한 기울기 소실(Vanishing Gradient)** | 은닉층을 **ReLU / GELU**로 전면 교체 | 심층망(100+ 층) 안정적 학습 보장 |
| ReLU 음수 구간 뉴런 불능화인 **Dying ReLU 현상** | **Leaky ReLU ($\alpha=0.01$) 또는 ELU / GELU** 채택 | 음수 영역 미세 기울기 보존 |
| 큰 가중치로 인한 활성화 함수의 **극단 포화(Saturation)** | **배치 정규화(BatchNorm)** 및 He/Xavier 초기화 | 가중합 $z$ 분포 안정화 |
| 트랜스포머 언어 모델의 확률적 활성화 요구 | **GELU (Gaussian Error Linear Unit)** 적용 | LLM/BERT 자연어 표현력 극대화 |

#### 한줄 요약

- **은닉층 ReLU 표준화·Dying ReLU 방지용 Leaky ReLU/GELU·배치 정규화 결합**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **딥러닝 아키텍처별 활성화 함수 표준**: CNN/MLP 은닉층은 ReLU, 트랜스포머 LLM은 GELU/SwiGLU, 이진 분류 출력층은 Sigmoid, 다중 분류 출력층은 Softmax를 배치하는 설계 표준.

</details>

- 은닉층 고속 학습은 **ReLU/GELU**, 이진 분류 출력은 **Sigmoid**, 순환 시계열 상태는 Tanh 선택

#### 한줄 요약

- 출력 계층은 과업 의미에 맞추고, 심층 은닉층은 기울기 소실 없는 ReLU 및 GELU를 적용
