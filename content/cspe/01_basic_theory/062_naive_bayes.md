---
title: "나이브 베이즈 분류 (Naive Bayes Classifier)"
date: "2026-07-06"
tags:
  - "cspe-basic-theory"
weight: 62
---

# 나이브 베이즈 분류 (Naive Bayes Classifier)

## 1. 개요

- **정의/개념**: 나이브 베이즈는 클래스가 주어졌을 때 feature들이 조건부 독립이라고 가정하고 베이즈 정리로 사후 확률을 계산하는 확률 기반 분류기이다.
- **배경/필요성**: 텍스트 분류처럼 feature 수가 많고 학습 데이터가 제한된 문제에서는 단순한 확률 가정으로 빠르게 기준 모델을 만들 필요가 있다.

나이브 베이즈의 핵심은 독립 가정이 현실적으로 완벽하지 않아도 계산 단순성과 빠른 학습에서 이점을 얻는 것이다.

## 2. 특징 및 비교

| 구분 | Gaussian NB | Multinomial NB | Bernoulli NB |
|---|---|---|---|
| 입력 | 연속값 | 빈도·count | 존재 여부 |
| 대표 활용 | 수치 feature | 문서 단어 빈도 | binary feature |
| 가정 | 정규 분포 | 다항 분포 | 베르누이 분포 |
| 장점 | 단순 | 텍스트에 강함 | 희소 binary에 적합 |

선택 기준은 feature 유형, 분포 가정, 독립성 정도, 라벨 데이터 규모, 해석 필요성이다.

## 3. 구성요소/구조

| 구성요소 | 설명 | 핵심 포인트 |
|---|---|---|
| Prior | 클래스 사전 확률 | 클래스 비율 |
| Likelihood | 클래스별 feature 발생 확률 | 분류 근거 |
| Independence Assumption | feature 조건부 독립 | 단순화 |
| Posterior | 입력이 각 클래스일 확률 | 예측 기준 |
| Smoothing | 0 확률 방지 | Laplace smoothing |

```text
feature -> 클래스별 우도 계산 -> prior 반영 -> posterior 비교 -> class 선택
```

확률 곱으로 계산하므로 0 확률과 underflow 문제가 실제 구현에서 바로 드러난다.

## 4. 문제점 및 개선방안

1. **독립성 가정 한계**
   - feature 간 상관이 강하면 확률 추정이 왜곡될 수 있다.
   - **개선방안**: feature selection, 상관 feature 제거, 다른 모델과 비교한다.

2. **Zero Frequency**
   - 학습에 없던 단어·feature가 나오면 likelihood가 0이 될 수 있다.
   - **개선방안**: Laplace smoothing을 적용한다.

3. **확률 보정 부족**
   - 분류는 잘해도 posterior 확률이 실제 확률처럼 보정되지 않을 수 있다.
   - **개선방안**: calibration, Brier score, reliability plot을 확인한다.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|---|---|---|
| 스팸 필터 | 단어 출현 확률로 스팸 posterior 계산 | precision, recall |
| 문서 분류 | 카테고리별 단어 빈도 기반 분류 | F1, 학습 시간 |
| 간단 위험 분류 | 제한된 feature로 빠른 baseline 생성 | baseline 성능 |

## 6. 결론

나이브 베이즈는 조건부 독립 가정으로 빠르고 단순한 확률 분류를 제공한다. Prior, likelihood, posterior, smoothing 흐름을 이해해야 독립성 한계와 텍스트 분류에서의 실용성을 함께 설명할 수 있다.
