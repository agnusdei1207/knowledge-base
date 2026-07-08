---
title: "Pipeline Parallelism 파이프라인 병렬 (Pipeline Parallelism)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 258
extra:
  question_no: "258"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- 파이프라인 병렬은 모델을 여러 stage로 나누고 micro batch를 흘려보내 장치 활용률을 높이는 방식임
- 모델 병렬의 한 유형이지만 시간축 병행 실행을 적극 활용한다는 점이 다름
- 핵심 과제는 pipeline bubble과 stage 불균형과 스케줄 설계임

## Ⅰ. 개요

- **정의/개념**: Pipeline Parallelism은 모델의 연속된 층을 여러 stage로 나눈 뒤 입력 배치를 여러 micro batch로 쪼개 순차 투입하여 각 장치가 서로 다른 micro batch를 동시에 처리하게 하는 병렬화 방식임
- **배경/필요성**: 초대형 모델을 나눠 담으면서도 단순 순차 실행으로 인한 장치 유휴 시간을 줄이기 위해 stage 간 파이프라인화가 필요해짐

## Ⅱ. 특징

- 모델이 단일 장치 메모리에 올라가지 않을 때 유용함
- micro batch 기반으로 장치 활용률을 높일 수 있음
- 시작과 끝 구간의 pipeline bubble이 효율을 깎음
- stage 간 계산량 차이가 크면 일부 장치가 병목이 됨

## Ⅲ. 종류 및 비교

| 판단 기준 | Pipeline Parallelism | Model Parallelism | Data Parallelism |
|:---|:---|:---|:---|
| 핵심 아이디어 | stage 분할과 시간 중첩 | 구조 분할 자체 | 배치 분할 |
| 병목 | bubble과 stage imbalance | activation 이동 | gradient 동기화 |
| 메모리 이점 | 큼 | 큼 | 제한적 |
| 처리량 향상 방식 | micro batch overlap | 메모리 확장 중심 | 동시 배치 확장 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Stage Partition | 모델을 연속된 단계로 나눠 장치별로 배치하는 구조로 파이프라인의 기본 단위임 |
| Micro Batch Splitter | 큰 배치를 작은 micro batch로 분할해 stage들이 중첩 실행되도록 만드는 입력 분할 계층임 |
| Forward Pipeline | micro batch가 stage를 따라 순전파로 이동하는 처리 흐름임 |
| Backward Pipeline | 역전파가 역방향으로 흐르며 gradient를 계산하는 학습 흐름임 |
| Scheduler | 1F1B 같은 실행 순서를 제어해 bubble과 메모리 사용량을 조절하는 운영 계층임 |

```text
+---------+    +---------+    +---------+
| Stage 1 | -> | Stage 2 | -> | Stage 3 |
+---------+    +---------+    +---------+
   mb1           mb1           mb1
   mb2           mb2           mb2
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| stage 분할   | -> | micro batch 생성 | -> | 순전파 중첩  | -> | 역전파 중첩  | -> | step 완료    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **stage 분할**: 모델 층을 여러 장치 단계로 나눔
2. **micro batch 생성**: 큰 배치를 작은 묶음으로 쪼갬
3. **순전파 중첩**: 각 stage가 서로 다른 micro batch를 동시에 처리함
4. **역전파 중첩**: 스케줄에 맞춰 gradient 계산을 중첩 수행함
5. **step 완료**: 모든 micro batch 처리가 끝나면 파라미터를 갱신함

## Ⅵ. 문제점 및 해결 방안

1. 문제: stage 계산량이 불균형하면 일부 stage가 병목이 되어 pipeline bubble이 커지고 장치 활용률이 낮아질 수 있음
   - 해결방안: stage rebalancing과 profile based partitioning을 적용하고 bubble ratio와 per stage utilization variance로 검증함
2. 문제: micro batch 수가 너무 적으면 중첩 효과가 약해 throughput 향상이 제한될 수 있음
   - 해결방안: micro batch tuning과 schedule optimization을 적용하고 pipeline efficiency와 tokens per second로 검증함
3. 문제: 스케줄 설계가 부적절하면 activation 저장량이 늘어 메모리 압박과 디버깅 복잡도가 커질 수 있음
   - 해결방안: 1F1B scheduling과 activation memory control을 적용하고 peak activation memory와 recovery debugging time으로 검증함

## Ⅶ. 적용 사례

- 초대형 트랜스포머 학습이 profile 기반 stage 재분할을 적용하며 확인 지표는 bubble ratio와 per stage utilization variance임
- 분산 학습 플랫폼이 micro batch 튜닝을 운영하며 확인 지표는 pipeline efficiency와 tokens per second임
- 메모리 민감 워크로드가 1F1B 스케줄을 사용하며 확인 지표는 peak activation memory와 recovery debugging time임

## Ⅷ. 결론

파이프라인 병렬은 메모리 한계를 넘으면서 처리량을 높이는 유용한 방식이지만 stage 균형과 bubble 제어가 핵심 성공 조건임.
