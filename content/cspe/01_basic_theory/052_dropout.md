---
title: "드롭아웃 (Dropout)"
date: "2026-07-06"
tags:
  - "cspe-basic-theory"
weight: 52
---

# 드롭아웃 (Dropout)

## 1. 개요

- **정의/개념**: 드롭아웃은 학습 중 일부 뉴런 출력을 확률적으로 0으로 만들어 특정 뉴런 조합에 과도하게 의존하는 것을 줄이는 regularization 기법이다.
- **배경/필요성**: 신경망은 파라미터가 많아 학습 데이터에 과적합되기 쉬우므로, 학습 과정에 무작위성을 넣어 일반화 성능을 높일 필요가 있다.

드롭아웃은 추론 시 뉴런을 제거하는 기법이 아니라 학습 중 여러 sub-network를 암묵적으로 앙상블하는 효과를 낸다.

## 2. 특징 및 비교

| 구분 | Dropout | L2 Regularization | Data Augmentation |
|---|---|---|---|
| 방식 | 뉴런 무작위 비활성 | 가중치 크기 제약 | 입력 데이터 변형 |
| 목적 | co-adaptation 완화 | 복잡도 제어 | 데이터 다양화 |
| 적용 위치 | 주로 FC, 일부 hidden layer | 모든 가중치 | 입력·중간 표현 |
| 주의점 | 학습/추론 동작 차이 | 과도하면 underfit | 도메인 적합성 |

선택 기준은 과적합 정도, 모델 구조, dropout rate, batch normalization과의 상호작용이다.

## 3. 구성요소/구조

| 구성요소 | 설명 | 핵심 포인트 |
|---|---|---|
| Dropout Rate | 제거할 뉴런 비율 | 과적합·과소적합 균형 |
| Mask | 뉴런 유지·제거를 결정하는 난수 마스크 | 학습 중 적용 |
| Scaling | 기대 출력 크기 보정 | inverted dropout |
| Train Mode | mask 적용 | regularization |
| Inference Mode | 전체 뉴런 사용 | deterministic output |

```text
+----------+      +----------+      +----------+
| 활성값   | ---> | mask적용 | ---> | scaled출력 |
+----------+      +----------+      +----------+
       학습 중만 무작위 비활성
```

학습과 추론의 동작이 다르므로, 모드 전환과 scaling 처리가 정확해야 성능이 유지된다.

## 4. 문제점 및 개선방안

1. **과도한 Dropout**
   - rate가 높으면 유효 모델 용량이 줄어 과소적합이 발생한다.
   - **개선방안**: validation 성능 기준으로 rate를 조정한다.

2. **BN과 충돌 가능성**
   - Dropout이 batch 통계에 영향을 주면 BatchNorm과 함께 사용할 때 효과가 불안정할 수 있다.
   - **개선방안**: 적용 위치를 조정하고 BN 이후 과도한 dropout을 피한다.

3. **추론 모드 오류**
   - 추론 시 dropout이 켜져 있으면 출력이 랜덤하게 변한다.
   - **개선방안**: eval mode 전환과 배포 테스트를 자동화한다.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|---|---|---|
| MLP 분류 | hidden layer에 dropout 적용 | validation gap |
| NLP 모델 | attention·feed-forward 일부에 dropout 적용 | perplexity, F1 |
| 불확실성 추정 | MC Dropout으로 예측 분산 추정 | uncertainty score |

## 6. 결론

드롭아웃은 학습 중 무작위 뉴런 비활성화로 과적합을 완화하는 정규화 기법이다. dropout rate, 적용 위치, train/inference 모드 차이를 함께 관리해야 일반화 효과가 안정적으로 나타난다.
