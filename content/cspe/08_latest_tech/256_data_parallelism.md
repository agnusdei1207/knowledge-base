---
title: "Data Parallelism 데이터 병렬 (Data Parallelism)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 256
extra:
  question_no: "256"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- 데이터 병렬은 동일한 모델 복제본을 여러 장치에 두고 서로 다른 미니배치를 나눠 학습하는 방식임
- 구현이 비교적 단순하고 확장성이 좋아 가장 기본적인 분산 학습 방식으로 쓰임
- gradient 동기화 비용과 글로벌 배치 증가에 따른 최적화 문제가 핵심 과제임

## Ⅰ. 개요

- **정의/개념**: Data Parallelism은 동일한 모델을 여러 GPU나 노드에 복제한 뒤 입력 데이터를 분할해 병렬로 순전파와 역전파를 수행하고 gradient를 동기화해 하나의 모델처럼 학습하는 병렬화 방식임
- **배경/필요성**: 모델 구조를 바꾸지 않고도 학습 처리량을 높일 수 있어 대규모 데이터셋과 다수 GPU 환경에서 가장 널리 사용되는 기본 분산 학습 전략이 됨

## Ⅱ. 특징

- 모델 전체를 각 장치가 모두 보유해 구현과 디버깅이 상대적으로 단순함
- 데이터셋이 클수록 처리량 향상 효과가 큼
- 장치 수가 늘수록 gradient 동기화 통신 비용이 커짐
- 글로벌 배치 증가에 따라 학습 안정성과 일반화 성능이 변할 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Data Parallelism | Model Parallelism | Pipeline Parallelism |
|:---|:---|:---|:---|
| 분할 대상 | 입력 데이터 | 모델 구조 | 모델 단계와 micro batch |
| 구현 난도 | 낮음 | 높음 | 중간 이상 |
| 대표 병목 | gradient 동기화 | 장치 간 activation 이동 | pipeline bubble |
| 적합 상황 | 모델이 장치에 적재 가능 | 모델이 너무 큼 | 깊은 모델과 다단계 구조 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Replicated Model | 모든 장치가 동일한 모델 가중치를 보유해 같은 계산을 수행하는 복제 모델 구조임 |
| Data Shard Loader | 전체 학습 데이터를 장치별 미니배치로 나눠 공급하는 입력 분배 계층임 |
| Local Trainer | 각 장치에서 순전파와 역전파를 수행해 로컬 gradient를 계산하는 실행 계층임 |
| Gradient Synchronizer | All-Reduce로 gradient를 통합해 복제 모델들의 가중치를 일관되게 유지하는 통신 계층임 |
| Optimizer Step | 동기화된 gradient를 기준으로 각 복제본의 파라미터를 동일하게 갱신하는 업데이트 계층임 |

```text
+---------+   data 1   +---------+
| Model A |<---------  | Batch 1 |
+---------+            +---------+
     |  \                   |
     |   \ All-Reduce       |
     |    \                 |
     v     \                v
+---------+   data 2   +---------+
| Model B |<---------  | Batch 2 |
+---------+            +---------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 데이터 분할  | -> | 로컬 학습    | -> | gradient 동기화 | -> | 파라미터 갱신 | -> | 다음 배치 진행 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **데이터 분할**: 전체 배치를 장치 수만큼 나눔
2. **로컬 학습**: 각 장치가 순전파와 역전파를 수행함
3. **gradient 동기화**: 장치 간 gradient를 집계함
4. **파라미터 갱신**: 같은 결과로 모든 복제 모델을 업데이트함
5. **다음 배치 진행**: 일관된 모델 상태로 다음 배치를 처리함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 장치 수가 늘어날수록 gradient 동기화 통신이 커져 계산보다 통신이 병목이 될 수 있음
   - 해결방안: gradient bucketing과 high speed collective optimization을 적용하고 communication to computation ratio와 scaling efficiency로 검증함
2. 문제: 글로벌 배치가 과도하게 커지면 수렴 특성과 일반화 성능이 나빠질 수 있음
   - 해결방안: learning rate scaling rule과 batch size tuning을 적용하고 convergence stability와 final validation accuracy로 검증함
3. 문제: 데이터 분할이 불균형하거나 일부 작업자가 느리면 straggler가 전체 step time을 끌어올릴 수 있음
   - 해결방안: balanced sharding과 straggler aware scheduling을 적용하고 batch processing skew와 step time variance로 검증함

## Ⅶ. 적용 사례

- 대규모 이미지 학습 클러스터가 gradient bucketing을 적용하며 확인 지표는 communication to computation ratio와 scaling efficiency임
- LLM 사전학습이 배치와 학습률 동조 튜닝을 운영하며 확인 지표는 convergence stability와 final validation accuracy임
- 멀티노드 학습 파이프라인이 균형 샤딩을 적용하며 확인 지표는 batch processing skew와 step time variance임

## Ⅷ. 결론

데이터 병렬은 가장 실용적인 기본 병렬화 방식이지만 통신 비용과 배치 스케일 효과를 함께 다뤄야 확장성이 유지됨.
