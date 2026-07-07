---
title: "XGBoost, LightGBM (Gradient Boosted Decision Trees)"
date: "2026-07-06"
tags:
  - "cspe-basic-theory"
weight: 64
---

# XGBoost, LightGBM (Gradient Boosted Decision Trees)

## 1. 개요

- **정의/개념**: XGBoost와 LightGBM은 이전 트리의 오류를 다음 트리가 보정하도록 순차적으로 학습하는 Gradient Boosted Decision Tree 계열 알고리즘이다.
- **배경/필요성**: 정형 데이터에서는 feature engineering과 비선형 관계가 중요하므로, 결정 트리의 표현력과 boosting의 오류 보정 구조를 결합한 강력한 모델이 필요하다.

두 모델의 핵심은 boosting이라는 공통 원리 위에서 정규화, 분할 전략, 학습 속도 최적화가 다르다는 점이다.

## 2. 특징 및 비교

| 구분 | XGBoost | LightGBM |
|---|---|---|
| 분할 방식 | level-wise 중심 | leaf-wise 중심 |
| 강점 | 정규화, 안정성, 범용성 | 빠른 학습, 대용량 처리 |
| 주요 기법 | regularization, shrinkage | histogram, GOSS, EFB |
| 위험 | 튜닝 복잡 | 과적합 가능성 |
| 적합 상황 | 안정적 정형 데이터 모델 | 대규모·고차원 정형 데이터 |

선택 기준은 데이터 크기, feature 수, 과적합 위험, 학습 시간, 튜닝 가능성이다.

## 3. 구성요소/구조

| 구성요소 | 설명 | 핵심 포인트 |
|---|---|---|
| Base Tree | 순차적으로 추가되는 결정 트리 | 약한 모델 |
| Gradient | 손실 함수의 잔차 방향 | 다음 트리 학습 신호 |
| Learning Rate | 트리 기여도 축소 | 과적합 완화 |
| Regularization | 트리 복잡도 제어 | 일반화 |
| Split Strategy | 노드 분할 방식 | 성능·속도 차이 |

```text
예측 -> 손실/gradient 계산 -> 새 트리 학습 -> 예측 보정 -> 반복
```

boosting은 이전 오류를 계속 보정하므로 성능이 높지만, 과도하게 반복하면 학습 데이터에 민감해진다.

## 4. 문제점 및 개선방안

1. **과적합**
   - 트리 깊이, leaf 수, 반복 수가 커지면 학습 데이터에 과도하게 맞춰진다.
   - **개선방안**: max depth, num leaves, early stopping, regularization을 조정한다.

2. **튜닝 복잡성**
   - 하이퍼파라미터가 많아 성능 재현이 어렵다.
   - **개선방안**: 검증 전략, search space 제한, seed·버전 관리를 적용한다.

3. **범주형·결측 처리 오해**
   - 자동 처리 기능에만 의존하면 데이터 의미가 왜곡될 수 있다.
   - **개선방안**: encoding 정책과 결측 원인을 검토하고 feature importance를 검증한다.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|---|---|---|
| 정형 데이터 예측 | 고객·거래 feature로 분류·회귀 모델 구성 | AUC, RMSE |
| 리스크 스코어링 | 변수 중요도와 성능을 함께 고려 | KS, 안정성 |
| 대용량 로그 분석 | LightGBM으로 빠른 학습과 feature 탐색 | 학습 시간, 메모리 |

## 6. 결론

XGBoost와 LightGBM은 정형 데이터에서 강력한 성능을 내는 GBDT 계열 모델이다. boosting 원리, 분할 전략, regularization, early stopping을 함께 설명해야 높은 성능과 과적합 위험을 균형 있게 판단할 수 있다.
