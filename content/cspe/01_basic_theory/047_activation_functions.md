---
title: "활성화 함수 - ReLU·Sigmoid·Tanh (Activation Functions)"
date: "2026-07-06"
tags:
  - "cspe-basic-theory"
weight: 47
---

# 활성화 함수 - ReLU·Sigmoid·Tanh (Activation Functions)

## 1. 개요

- **정의/개념**: 활성화 함수는 신경망 각 뉴런의 선형 결합 결과에 비선형성을 부여해 복잡한 함수 근사를 가능하게 하는 함수이다.
- **배경/필요성**: 활성화 함수가 없으면 여러 층을 쌓아도 전체 모델은 하나의 선형 변환과 같아지므로, 비선형 패턴을 학습할 수 없다.

활성화 함수 선택은 표현력, gradient 흐름, 출력 범위, 계산 비용을 함께 결정한다.

## 2. 특징 및 비교

| 구분 | Sigmoid | Tanh | ReLU |
|---|---|---|---|
| 출력 범위 | 0~1 | -1~1 | 0~무한 |
| 장점 | 확률 해석 가능 | zero-centered | 계산 단순, gradient 유지 |
| 한계 | vanishing gradient | 포화 구간 | dying ReLU |
| 주요 활용 | 이진 출력층 | 일부 RNN·은닉층 | CNN·DNN 은닉층 |

선택 기준은 출력 목적, gradient 안정성, 입력 분포, 학습 속도, dead neuron 위험이다.

## 3. 구성요소/구조

| 구성요소 | 설명 | 핵심 포인트 |
|---|---|---|
| Pre-activation | `z = Wx + b` | 선형 결합 |
| Activation Function | `a = f(z)` | 비선형 변환 |
| Derivative | 역전파 gradient 계산 | 학습 안정성 |
| Output Range | 함수 출력 범위 | 다음 층 입력 분포 |
| Saturation | gradient가 작아지는 구간 | 학습 지연 |

```text
+----------+      +----------+      +----------+
| 입력 x   | ---> | Wx + b   | ---> | f(z) 출력 |
+----------+      +----------+      +----------+
```

활성화 함수의 미분 특성이 역전파 gradient를 좌우하므로, 표현력과 학습 안정성이 같은 구조에서 결정된다.

## 4. 문제점 및 개선방안

1. **Vanishing Gradient**
   - sigmoid, tanh는 포화 구간에서 gradient가 작아져 깊은 모델 학습이 느려진다.
   - **개선방안**: ReLU 계열, batch normalization, 적절한 초기화를 적용한다.

2. **Dying ReLU**
   - ReLU 뉴런이 음수 영역에 머물면 gradient가 0이 되어 학습하지 못한다.
   - **개선방안**: Leaky ReLU, ELU, learning rate 조정을 사용한다.

3. **출력층 함수 오선택**
   - 다중분류에 sigmoid를 단순 적용하면 확률 합 해석이 맞지 않을 수 있다.
   - **개선방안**: 문제 유형에 따라 sigmoid, softmax, linear 출력을 구분한다.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|---|---|---|
| CNN 은닉층 | ReLU 계열로 빠른 학습과 sparse activation 유도 | 학습 속도, dead neuron |
| 이진 분류 | sigmoid로 양성 클래스 확률 출력 | log loss, calibration |
| 다중 분류 | softmax로 클래스 확률 분포 출력 | accuracy, cross-entropy |

## 6. 결론

활성화 함수는 신경망에 비선형성과 학습 가능한 gradient 흐름을 제공한다. ReLU·Sigmoid·Tanh는 출력 범위와 gradient 특성이 다르므로, 은닉층·출력층 목적과 학습 안정성을 연결해 선택해야 한다.
