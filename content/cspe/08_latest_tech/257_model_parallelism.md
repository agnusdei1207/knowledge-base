---
title: "Model Parallelism 모델 병렬 (Model Parallelism)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 257
extra:
  question_no: "257"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- 모델 병렬은 하나의 모델을 여러 장치에 나눠 담아 학습하는 방식임
- 장치 하나에 모델 전체가 올라가지 않을 만큼 큰 모델에서 필수 전략이 됨
- 분할 방식에 따라 activation 이동과 통신 비용 구조가 크게 달라짐

## Ⅰ. 개요

- **정의/개념**: Model Parallelism은 하나의 거대한 모델을 여러 GPU나 노드에 분할 배치해 각 장치가 모델의 일부 연산만 담당하도록 만드는 병렬화 방식임
- **배경/필요성**: 파라미터 수와 activation 메모리 요구가 폭증한 초대형 모델은 단일 장치 메모리에 적재할 수 없어 모델 자체를 나눠 저장하고 계산하는 구조가 필요해짐

## Ⅱ. 특징

- 모델 크기 한계를 극복해 초대형 파라미터 학습을 가능하게 함
- 장치 간 activation과 gradient 이동이 필수라 통신 최적화가 중요함
- 분할 전략이 잘못되면 계산 불균형과 메모리 불균형이 생김
- 데이터 병렬보다 구현과 디버깅 난도가 높음

## Ⅲ. 종류 및 비교

| 판단 기준 | Model Parallelism | Data Parallelism | Tensor Parallelism |
|:---|:---|:---|:---|
| 분할 대상 | 모델 전체 구조 | 입력 배치 | 층 내부 텐서 차원 |
| 주요 목적 | 메모리 수용 한계 극복 | 처리량 향상 | 거대 층 세분 분할 |
| 핵심 병목 | activation 이동 | gradient 동기화 | 세밀한 집단 통신 |
| 구현 난도 | 높음 | 낮음 | 높음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Partitioned Layers | 모델의 층이나 블록을 여러 장치에 나눠 저장해 메모리 수용 한계를 넘는 핵심 구조임 |
| Inter Device Activation Path | 앞 장치 출력이 다음 장치 입력으로 전달되도록 activation을 이동시키는 통신 경로임 |
| Local Compute Stage | 각 장치가 자신에게 할당된 부분 연산만 수행하는 실행 단위임 |
| Gradient Return Flow | 역전파 시 분할된 경로를 따라 gradient를 반대로 전달하는 학습 통신 계층임 |
| Load Balancer | 메모리와 계산량을 고려해 층 배치를 조정하는 분할 최적화 계층임 |

```text
+--------+    act    +--------+    act    +--------+
| GPU A  |---------> | GPU B  |---------> | GPU C  |
| Layer1 |           | Layer2 |           | Layer3 |
+--------+ <---------+--------+ <---------+--------+
            gradient             gradient
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 모델 분할    | -> | 순전파 전달  | -> | 장치 간 activation 이동 | -> | 역전파 회수  | -> | 파라미터 갱신 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **모델 분할**: 모델 층과 블록을 장치에 나눠 배치함
2. **순전파 전달**: 입력이 첫 장치부터 순차적으로 처리됨
3. **장치 간 activation 이동**: 중간 결과를 다음 장치로 전달함
4. **역전파 회수**: gradient가 역방향으로 이동함
5. **파라미터 갱신**: 각 장치가 자신의 파라미터를 업데이트함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 층별 계산량과 메모리 사용량이 불균형하면 일부 장치가 병목이 되어 전체 처리 속도가 떨어질 수 있음
   - 해결방안: balanced partition planning과 profile based placement를 적용하고 stage utilization variance와 step time imbalance로 검증함
2. 문제: activation 이동이 잦으면 장치 간 통신 지연이 순전파와 역전파 시간을 크게 늘릴 수 있음
   - 해결방안: communication aware partitioning과 activation recomputation tuning을 적용하고 activation transfer overhead와 end to end step time로 검증함
3. 문제: 분할 경계가 많을수록 디버깅과 장애 복구가 복잡해져 운영 안정성이 낮아질 수 있음
   - 해결방안: clear partition boundary design과 observability instrumentation을 적용하고 partition fault isolation time와 debug turnaround time으로 검증함

## Ⅶ. 적용 사례

- 초대형 트랜스포머 학습이 프로파일 기반 층 분할을 적용하며 확인 지표는 stage utilization variance와 step time imbalance임
- 멀티 GPU 모델 병렬 환경이 activation 재계산 튜닝을 운영하며 확인 지표는 activation transfer overhead와 end to end step time임
- 연구 클러스터가 분할 경계 관측 도구를 강화하며 확인 지표는 partition fault isolation time과 debug turnaround time임

## Ⅷ. 결론

모델 병렬은 초대형 모델 학습의 필수 전략이지만 분할 균형과 activation 통신 최적화가 성패를 가름함.
