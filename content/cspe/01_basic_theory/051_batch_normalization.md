---
title: "배치 정규화 (Batch Normalization)"
date: "2026-07-06"
tags:
  - "cspe-basic-theory"
weight: 51
---

# 배치 정규화 (Batch Normalization)

## 1. 개요

- **정의/개념**: 배치 정규화는 mini-batch 단위의 평균과 분산으로 layer 입력을 정규화한 뒤 학습 가능한 scale·shift를 적용하는 신경망 안정화 기법이다.
- **배경/필요성**: 깊은 신경망은 층별 입력 분포가 학습 중 계속 변해 학습이 불안정해질 수 있으므로, 분포를 안정화해 빠르고 안정적인 최적화를 지원해야 한다.

Batch Normalization은 정규화만 하는 것이 아니라 `gamma`, `beta`를 통해 필요한 표현력을 다시 학습한다.

## 2. 특징 및 비교

| 구분 | Batch Normalization | Layer Normalization | Dropout |
|---|---|---|---|
| 기준 | batch 통계 | sample 내부 feature 통계 | 뉴런 무작위 비활성 |
| 강점 | CNN 학습 안정화 | RNN/Transformer에 적합 | 과적합 완화 |
| 약점 | 작은 batch에 취약 | 구조별 효과 차이 | 학습·추론 동작 차이 |
| 주요 목적 | 분포 안정화 | 분포 안정화 | regularization |

선택 기준은 batch 크기, 모델 구조, 학습/추론 통계 차이, 정규화 위치이다.

## 3. 구성요소/구조

| 구성요소 | 설명 | 핵심 포인트 |
|---|---|---|
| Mini-batch | 통계 계산 단위 | batch size 영향 |
| Mean/Variance | 정규화 기준 | 학습 중 계산 |
| Normalize | 평균 0, 분산 1로 변환 | gradient 안정화 |
| Gamma/Beta | scale과 shift | 표현력 복원 |
| Running Statistics | 추론 시 사용할 통계 | train/inference 차이 |

```text
+----------+      +----------+      +----------+      +----------+
| layer입력 | ---> | 평균/분산 | ---> | 정규화   | ---> | scale/shift |
+----------+      +----------+      +----------+      +----------+
```

학습 중 batch 통계와 추론 중 running 통계가 다르므로, 모드 전환과 통계 관리가 실제 성능에 직접 영향을 준다.

## 4. 문제점 및 개선방안

1. **작은 Batch 문제**
   - batch size가 작으면 평균·분산 추정이 불안정해진다.
   - **개선방안**: GroupNorm, LayerNorm, SyncBatchNorm을 검토한다.

2. **Train/Inference 불일치**
   - running statistics가 실제 추론 데이터와 다르면 성능이 저하된다.
   - **개선방안**: eval mode 전환, 통계 재추정, domain별 검증을 수행한다.

3. **분산 학습 통계 차이**
   - GPU별 batch 통계가 달라 전체 학습이 흔들릴 수 있다.
   - **개선방안**: synchronized BN 또는 충분한 per-device batch를 확보한다.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|---|---|---|
| CNN 학습 | Conv 뒤 BN을 적용해 학습 안정화 | 수렴 속도, validation 성능 |
| 전이 학습 | 소량 데이터에서 BN freeze 여부 결정 | train/eval gap |
| 분산 학습 | SyncBatchNorm으로 통계 일관성 확보 | GPU별 성능 편차 |

## 6. 결론

배치 정규화는 층 입력 분포를 안정화해 깊은 신경망 학습을 돕는 기법이다. batch 통계, scale/shift, running statistics, train/inference 차이를 함께 관리해야 학습 안정성과 추론 성능이 연결된다.
