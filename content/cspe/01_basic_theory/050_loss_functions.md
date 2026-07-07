---
title: "손실 함수 - Cross-Entropy·MSE (Loss Functions)"
date: "2026-07-06"
tags:
  - "cspe-basic-theory"
weight: 50
---

# 손실 함수 - Cross-Entropy·MSE (Loss Functions)

## 1. 개요

- **정의/개념**: 손실 함수는 모델 예측값과 실제 정답의 차이를 수치화해 학습 과정에서 최소화할 목표를 제공하는 함수이다.
- **배경/필요성**: 모델은 무엇을 틀렸다고 볼지 정의해야 학습 방향이 생기므로, 문제 유형과 평가 목적에 맞는 손실 함수 선택이 필요하다.

손실 함수는 단순 성능 지표가 아니라 gradient를 통해 파라미터 갱신 방향을 결정하는 학습 목표이다.

## 2. 특징 및 비교

| 구분 | MSE | Cross-Entropy | Hinge Loss |
|---|---|---|---|
| 대상 | 회귀 | 분류 확률 | margin 기반 분류 |
| 민감도 | 큰 오차에 민감 | 확률 오분류에 민감 | 경계 위반에 민감 |
| 출력 조합 | linear output | sigmoid/softmax | SVM 계열 |
| 주요 지표 | RMSE, MAE | log loss, accuracy | margin |

선택 기준은 문제 유형, 출력층 형태, 오차 비용, class imbalance, gradient 안정성이다.

## 3. 구성요소/구조

| 구성요소 | 설명 | 핵심 포인트 |
|---|---|---|
| Prediction | 모델 출력 | logit, probability, value |
| Target | 정답 라벨·값 | 회귀·분류 구분 |
| Error Measure | 차이 계산 방식 | 제곱, 로그, margin |
| Reduction | batch 손실 집계 | mean, sum |
| Gradient | 파라미터 갱신 방향 | 학습 안정성 |

```text
+----------+      +----------+      +----------+      +----------+
| 예측값   | ---> | 정답비교 | ---> | 손실계산 | ---> | gradient |
+----------+      +----------+      +----------+      +----------+
```

손실 함수와 출력층이 맞지 않으면 gradient가 문제 목표를 잘못 반영하므로 학습 전체가 흔들린다.

## 4. 문제점 및 개선방안

1. **문제 유형과 손실 불일치**
   - 분류 문제에 회귀 손실을 쓰거나 확률 출력 없이 cross-entropy를 쓰면 학습이 비효율적이다.
   - **개선방안**: 회귀는 MSE/MAE, 이진 분류는 BCE, 다중 분류는 softmax cross-entropy를 기본으로 검토한다.

2. **Class Imbalance**
   - 소수 클래스 오류가 손실에 충분히 반영되지 않을 수 있다.
   - **개선방안**: class weight, focal loss, sampling 전략을 적용한다.

3. **이상치 민감성**
   - MSE는 큰 오차에 민감해 이상치가 학습을 지배할 수 있다.
   - **개선방안**: MAE, Huber loss, robust preprocessing을 사용한다.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|---|---|---|
| 가격 예측 | MSE 또는 Huber loss로 연속값 오차 최소화 | RMSE, MAE |
| 이미지 분류 | softmax cross-entropy로 클래스 확률 학습 | accuracy, log loss |
| 불균형 탐지 | focal loss로 어려운 소수 클래스 학습 강화 | recall, F1 |

## 6. 결론

손실 함수는 모델이 무엇을 줄여야 하는지 정의하는 학습 목표이다. Cross-Entropy와 MSE는 문제 유형과 출력 구조가 다르므로, 평가 지표·오차 비용·gradient 안정성을 함께 고려해 선택해야 한다.
