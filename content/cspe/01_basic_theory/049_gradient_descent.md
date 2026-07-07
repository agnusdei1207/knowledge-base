---
title: "경사하강법 - SGD·Adam·AdaGrad (Gradient Descent)"
date: "2026-07-06"
tags:
  - "cspe-basic-theory"
weight: 49
---

# 경사하강법 - SGD·Adam·AdaGrad (Gradient Descent)

## 1. 개요

- **정의/개념**: 경사하강법은 손실 함수의 gradient가 가리키는 증가 방향의 반대로 파라미터를 갱신해 손실을 줄이는 최적화 방법이다.
- **배경/필요성**: 머신러닝 모델은 손실을 최소화하는 파라미터를 직접 구하기 어렵기 때문에, 반복적인 gradient 기반 탐색으로 해를 찾아야 한다.

경사하강법은 손실 함수 지형, learning rate, gradient 품질에 따라 수렴 속도와 안정성이 달라진다.

## 2. 특징 및 비교

| 구분 | Batch GD | SGD | Adam | AdaGrad |
|---|---|---|---|---|
| gradient 기준 | 전체 데이터 | 샘플·미니배치 | 모멘텀+적응 학습률 | 누적 gradient 기반 |
| 장점 | 안정적 | 빠른 갱신, 일반화 | 수렴 빠름 | 희소 feature에 유리 |
| 단점 | 계산 비용 큼 | 노이즈 큼 | 과적합·일반화 이슈 | 학습률이 과도하게 감소 |
| 적용 | 작은 데이터 | 대규모 학습 | 딥러닝 기본 선택 | 희소 데이터 |

선택 기준은 데이터 규모, gradient 노이즈, learning rate 민감도, 메모리 비용, 일반화 성능이다.

## 3. 구성요소/구조

| 구성요소 | 설명 | 핵심 포인트 |
|---|---|---|
| Loss Function | 최소화할 목적 함수 | 학습 목표 |
| Gradient | 손실 변화 방향 | 갱신 방향 |
| Learning Rate | 한 번에 이동할 크기 | 수렴 안정성 |
| Batch Size | gradient 추정 데이터 수 | 노이즈와 비용 |
| Update Rule | optimizer별 파라미터 갱신식 | SGD, Adam 등 |

```text
+----------+      +----------+      +----------+      +----------+
| 손실계산 | ---> | gradient | ---> | 갱신규칙 | ---> | 파라미터 |
+----------+      +----------+      +----------+      +----------+
                                      반복
```

gradient는 방향을 주고 learning rate는 이동 크기를 정하므로, 둘의 균형이 수렴 품질을 결정한다.

## 4. 문제점 및 개선방안

1. **Learning Rate 부적절**
   - 너무 크면 발산하고 너무 작으면 수렴이 느리다.
   - **개선방안**: scheduler, warmup, learning rate search를 적용한다.

2. **Local Minima·Saddle Point**
   - 복잡한 손실 지형에서 정체되거나 느리게 움직일 수 있다.
   - **개선방안**: momentum, Adam, 초기화 개선, batch noise 활용을 검토한다.

3. **Gradient 노이즈와 불안정**
   - 작은 batch나 이상치로 gradient 방향이 크게 흔들릴 수 있다.
   - **개선방안**: batch size 조정, gradient clipping, 정규화를 사용한다.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|---|---|---|
| 딥러닝 모델 학습 | Adam 또는 SGD+momentum으로 파라미터 최적화 | loss curve, validation 성능 |
| 대규모 데이터 | mini-batch SGD로 계산 비용과 수렴 균형 확보 | throughput, 수렴 속도 |
| 희소 feature 모델 | AdaGrad 계열로 feature별 학습률 조정 | sparse feature 성능 |

## 6. 결론

경사하강법은 손실을 줄이는 방향으로 파라미터를 반복 갱신하는 최적화의 기본 원리이다. SGD·Adam·AdaGrad는 gradient 사용 방식과 학습률 조정 방식이 다르므로 데이터 규모, 안정성, 수렴 속도, 일반화 성능을 함께 판단해야 한다.
