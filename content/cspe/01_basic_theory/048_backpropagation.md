---
title: "역전파 알고리즘 (Backpropagation)"
date: "2026-07-08"
tags:
  - "cspe-basic-theory"
weight: 48

extra:
  question_no: "048"
  exam_status: "미출제"
---

## 미리 알고가기

- chain rule: 합성 함수 미분을 단계별로 전개하는 규칙임
- loss: 예측과 정답 차이를 나타내는 함수값임
- gradient: 손실을 줄이기 위한 변화 방향과 크기임

## Ⅰ. 개요

- **정의/개념**: 역전파는 출력층의 손실을 기준으로 각 층 가중치의 기울기를 연쇄법칙으로 계산해 신경망 전체를 효율적으로 학습시키는 알고리즘임
- **배경/필요성**: 다층 신경망은 파라미터 수가 많아 각 가중치의 영향도를 직접 구하기 어렵기 때문에, 오차를 뒤에서 앞으로 전달하는 체계적 미분 절차가 필요함

## Ⅱ. 특징

- 한 번의 forward/backward pass로 모든 파라미터 기울기를 계산함
- 연쇄법칙을 이용해 깊은 네트워크 학습을 가능하게 함
- 자동미분 프레임워크의 핵심 원리로 사용됨
- gradient vanishing/exploding이 있으면 학습 품질이 급격히 나빠짐

## Ⅲ. 종류 및 비교

| 판단 기준 | 수치 미분 | 역전파 |
|:---|:---|:---|
| 정확도 | 근사치 | 해석적 기울기 |
| 계산 비용 | 매우 큼 | 효율적 |
| 적용 목적 | gradient check | 실제 학습 |
| 대표 장점 | 구현 단순 | 대규모 학습 가능 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| 순전파 그래프 | 연산 흐름을 저장하고 backward 경로의 기준임 |
| 손실 함수 | 최종 오차를 정의하고 학습 목표를 결정함 |
| 국소 도함수 | 각 연산의 미분값이며 chain rule 입력임 |
| gradient buffer | 파라미터별 기울기 저장소이며 optimizer 입력값임 |

## Ⅴ. 원리 및 절차 흐름도

```text
+----------+     +----------+     +----------+     +----------+
| 순전파 | --> | 손실계산 | --> | 오차역전파 | --> | 가중치갱신 |
+----------+     +----------+     +----------+     +----------+
```

1. **순전파**: 입력을 각 층에 통과시켜 예측값을 계산함
2. **손실계산**: 예측과 정답 차이로 손실을 구함
3. **오차역전파**: 출력층부터 입력 방향으로 gradient를 계산함
4. **가중치갱신**: optimizer가 gradient를 반영해 파라미터를 조정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: gradient vanishing/exploding이 발생해 깊은 층에서 학습 신호가 사라지거나 폭증함
   - 해결방안: ReLU, batch norm, residual connection, 초기화를 개선하고 gradient norm로 검증함
2. 문제: 메모리 사용량이 커 backward를 위해 중간 activation을 저장해야 함
   - 해결방안: gradient checkpointing, mixed precision을 사용하고 GPU memory usage로 검증함
3. 문제: 미분 불가능하거나 불연속 연산에 약해 direct gradient가 없을 수 있음
   - 해결방안: surrogate gradient, differentiable relaxation을 적용하고 training stability로 검증함

## Ⅶ. 적용 사례

- 딥러닝 학습 전반: CNN, RNN, Transformer 가중치 갱신에 사용함, 확인 지표는 loss 감소율임
- 자동미분 프레임워크: PyTorch, TensorFlow 내부 핵심 메커니즘임, 확인 지표는 backward 시간임
- 모델 디버깅: gradient check로 구현 오류를 찾음, 확인 지표는 numerical gradient 차이임

## Ⅷ. 결론

역전파의 핵심은 모든 층에 학습 신호를 효율적으로 전달하는 데 있으므로, 모델 설계에서는 표현력만큼 gradient 흐름 보존이 중요함.
