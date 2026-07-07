---
title: "역전파 알고리즘 (Backpropagation)"
date: "2026-07-06"
tags:
  - "cspe-basic-theory"
weight: 48
---

# 역전파 알고리즘 (Backpropagation)

## 1. 개요

- **정의/개념**: 역전파는 신경망의 출력 오차를 손실 함수에서 시작해 각 층의 가중치 방향으로 미분값을 전달하고, chain rule로 gradient를 계산하는 학습 알고리즘이다.
- **배경/필요성**: 다층 신경망은 파라미터가 많아 직접 미분을 계산하기 어렵기 때문에, 계산 그래프를 따라 효율적으로 gradient를 구하는 절차가 필요하다.

역전파는 가중치를 직접 바꾸는 최적화 알고리즘이 아니라, optimizer가 사용할 gradient를 계산하는 과정이다.

## 2. 특징 및 비교

| 구분 | 순전파 | 역전파 |
|---|---|---|
| 방향 | 입력에서 출력 | 손실에서 입력 방향 |
| 목적 | 예측값 계산 | gradient 계산 |
| 주요 값 | activation, logits | derivative, gradient |
| 연결 기술 | 모델 구조 | chain rule, 자동미분 |

역전파의 판단 기준은 계산 그래프, 손실 함수, activation 미분, gradient 안정성, 메모리 사용량이다.

## 3. 구성요소/구조

| 구성요소 | 설명 | 핵심 포인트 |
|---|---|---|
| Forward Pass | 입력으로 예측값 계산 | activation 저장 |
| Loss Function | 예측과 정답 차이 측정 | 학습 목표 |
| Chain Rule | 합성 함수 미분 규칙 | gradient 전달 |
| Gradient | 파라미터별 손실 변화율 | optimizer 입력 |
| Optimizer | gradient로 파라미터 갱신 | SGD, Adam |

```text
+----------+      +----------+      +----------+      +----------+
| 순전파   | ---> | 손실계산 | ---> | 역전파   | ---> | 가중치갱신 |
+----------+      +----------+      +----------+      +----------+
```

순전파에서 저장한 중간값이 역전파 계산에 필요하므로, 정확성과 메모리 사용량이 함께 관리된다.

## 4. 문제점 및 개선방안

1. **Gradient 소실·폭주**
   - 깊은 네트워크에서 gradient가 0에 가까워지거나 지나치게 커질 수 있다.
   - **개선방안**: ReLU 계열, residual connection, gradient clipping, 초기화 개선을 적용한다.

2. **메모리 사용 증가**
   - 역전파를 위해 중간 activation을 저장해야 하므로 큰 모델에서 메모리가 부족할 수 있다.
   - **개선방안**: gradient checkpointing, mixed precision, mini-batch 조정을 사용한다.

3. **손실 함수·출력층 불일치**
   - 출력 형태와 손실 함수가 맞지 않으면 gradient가 학습 목표를 잘못 반영한다.
   - **개선방안**: 문제 유형별 softmax+cross entropy, sigmoid+BCE, regression loss를 구분한다.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|---|---|---|
| 딥러닝 학습 | 손실 gradient를 계산해 optimizer로 파라미터 갱신 | loss 감소, gradient norm |
| 자동미분 프레임워크 | 계산 그래프 기반으로 역전파 자동 수행 | 메모리 사용량, 학습 시간 |
| 모델 디버깅 | gradient 흐름을 점검해 학습 불안정 원인 분석 | vanishing, exploding 여부 |

## 6. 결론

역전파는 다층 신경망 학습을 가능하게 하는 gradient 계산 절차이다. 순전파, 손실 함수, chain rule, gradient, optimizer가 연결되어야 학습 과정과 문제점 대응이 일관되게 설명된다.
