---
title: "Tensor Parallelism 텐서 병렬 (Tensor Parallelism)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 259
extra:
  question_no: "259"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- 텐서 병렬은 하나의 층 내부 텐서 연산을 여러 장치에 세분 분할하는 방식임
- 대형 선형층과 attention 계산을 쪼개 거대한 모델 층을 여러 GPU가 함께 처리하게 함
- 미세한 집단 통신이 많아 고속 인터커넥트와 최적화 라이브러리가 중요함

## Ⅰ. 개요

- **정의/개념**: Tensor Parallelism은 하나의 신경망 층 내부의 가중치 행렬과 activation 텐서를 여러 GPU에 나누어 계산하게 함으로써 단일 층조차 한 장치에 담기 어려운 대규모 모델을 병렬 처리하는 방식임
- **배경/필요성**: 트랜스포머의 거대한 선형 변환과 attention 블록은 층 단위 자체가 매우 커져 더 미세한 텐서 차원 분할이 필요해짐

## Ⅱ. 특징

- 층 내부를 직접 분할해 거대한 행렬 연산을 병렬 처리함
- 모델 병렬보다 더 세밀한 분할 방식으로 메모리 부담을 줄임
- forward와 backward 과정마다 집단 통신이 자주 발생함
- NVLink 같은 고속 내부 패브릭이 있어야 효율이 높음

## Ⅲ. 종류 및 비교

| 판단 기준 | Tensor Parallelism | Pipeline Parallelism | Data Parallelism |
|:---|:---|:---|:---|
| 분할 단위 | 층 내부 텐서 차원 | stage와 micro batch | 입력 배치 |
| 장점 | 초대형 층 처리 | 장치 활용률 향상 | 구현 단순성과 범용성 |
| 병목 | 잦은 집단 통신 | bubble | gradient 동기화 |
| 적합 위치 | 노드 내부 고속 패브릭 | stage 기반 거대 모델 | 표준 분산 학습 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Sharded Weight Matrix | 거대한 가중치 행렬을 여러 장치에 나눠 저장해 메모리 부담을 분산하는 핵심 구조임 |
| Partitioned Activation | 입력과 중간 activation을 분할된 텐서 형태로 각 장치에 공급하는 계산 단위임 |
| Local GEMM Engine | 각 GPU가 자신에게 할당된 텐서 블록에 대해 행렬 곱을 수행하는 실행 계층임 |
| Collective Communication | partial result를 합치기 위해 All-Gather나 Reduce-Scatter를 수행하는 통신 계층임 |
| Layout Planner | 어떤 차원으로 텐서를 나눌지 결정해 통신 비용과 메모리 균형을 맞추는 설계 계층임 |

```text
+------------+   shard 1   +------------+
| Weight A   |<----------> | GPU 1      |
+------------+             +------------+
+------------+   shard 2   +------------+
| Weight B   |<----------> | GPU 2      |
+------------+             +------------+
       \______________________________/
        collective combine of results
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 텐서 분할    | -> | 로컬 GEMM 수행 | -> | 부분 결과 통신 | -> | 결과 결합    | -> | 다음 층 진행  |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **텐서 분할**: 가중치와 activation을 차원 기준으로 나눔
2. **로컬 GEMM 수행**: 각 GPU가 자신의 텐서 블록을 계산함
3. **부분 결과 통신**: 필요한 partial result를 서로 교환함
4. **결과 결합**: 최종 출력 또는 gradient를 완성함
5. **다음 층 진행**: 결합된 결과로 다음 연산을 수행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 층 내부 연산마다 잦은 집단 통신이 발생하면 계산보다 통신이 지배적이 되어 효율이 급락할 수 있음
   - 해결방안: fused collective kernel과 high bandwidth intra node fabric을 적용하고 communication overhead ratio와 tensor parallel efficiency로 검증함
2. 문제: 텐서 분할 축 선택이 잘못되면 메모리 균형과 연산 균형이 동시에 깨질 수 있음
   - 해결방안: layout search와 profile based sharding을 적용하고 shard memory variance와 per device compute imbalance로 검증함
3. 문제: 작은 배치나 작은 층에서는 분할 이점보다 통신 비용이 커져 비효율이 발생할 수 있음
   - 해결방안: hybrid parallel policy와 minimum profitable shard rule을 적용하고 low batch efficiency score와 hybrid runtime gain으로 검증함

## Ⅶ. 적용 사례

- 초대형 트랜스포머가 fused collective kernel을 적용하며 확인 지표는 communication overhead ratio와 tensor parallel efficiency임
- 멀티 GPU 노드가 프로파일 기반 텐서 샤딩을 운영하며 확인 지표는 shard memory variance와 per device compute imbalance임
- 하이브리드 병렬 학습기가 최소 유효 분할 규칙을 사용하며 확인 지표는 low batch efficiency score와 hybrid runtime gain임

## Ⅷ. 결론

텐서 병렬은 거대한 층 자체를 분할하는 필수 전략이지만 통신 집약성이 높으므로 고속 패브릭과 분할 최적화가 필수임.
