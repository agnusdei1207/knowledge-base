---
title: "ZeRO Optimizer 제로 중복 최적화 (Zero Redundancy Optimizer)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 260
extra:
  question_no: "260"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- ZeRO는 분산 학습에서 중복 저장되던 optimizer state와 gradient와 파라미터를 샤딩해 메모리 사용량을 줄이는 기법임
- 초대형 모델을 적은 GPU 메모리로도 학습할 수 있게 만든 핵심 최적화로 평가됨
- 메모리 절감과 통신 복잡도 사이의 균형을 단계별로 조정하는 구조가 핵심임

## Ⅰ. 개요

- **정의/개념**: ZeRO Optimizer는 데이터 병렬 학습에서 각 장치에 중복 저장되던 optimizer state와 gradient와 파라미터를 분산 샤딩하여 메모리 사용량을 획기적으로 줄이는 분산 학습 최적화 기법임
- **배경/필요성**: 초대형 모델은 모델 자체보다 optimizer state와 gradient 복제 비용이 더 커져 기존 데이터 병렬만으로는 GPU 메모리 한계에 빠르게 도달함

## Ⅱ. 특징

- 데이터 병렬의 구조를 유지하면서 메모리 중복만 줄이는 점이 강점임
- stage별로 상태와 gradient와 파라미터까지 점진적으로 샤딩 범위를 넓힐 수 있음
- 메모리 절감 효과가 크지만 통신과 gather 비용이 증가할 수 있음
- offloading과 결합하면 더 큰 모델을 다룰 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | ZeRO Stage 1 | ZeRO Stage 2 | ZeRO Stage 3 |
|:---|:---|:---|:---|
| 샤딩 대상 | optimizer state | optimizer state, gradient | optimizer state, gradient, parameter |
| 메모리 절감 | 중간 | 큼 | 매우 큼 |
| 통신 복잡도 | 낮음 | 중간 | 높음 |
| 적합 상황 | 초기 메모리 개선 | 대규모 학습 일반 | 초대형 모델 학습 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Data Parallel Workers | 각 장치가 일부 상태만 들고 전체 학습에 참여하는 데이터 병렬 실행 주체임 |
| State Sharding Manager | optimizer state와 gradient와 파라미터를 어느 장치에 분산 저장할지 관리하는 메모리 분할 계층임 |
| Gather and Scatter Engine | 연산 직전에 필요한 파라미터를 모으고 사용 후 다시 분산하는 통신 제어 계층임 |
| Optimizer Step Coordinator | 샤딩된 상태를 이용해 업데이트를 수행하고 일관성을 유지하는 학습 제어 계층임 |
| Offload Layer | CPU 메모리나 NVMe로 일부 상태를 넘겨 GPU 메모리 압박을 더 줄이는 확장 계층임 |

```text
+---------+      shard A      +---------+      shard B      +---------+
| GPU 1   |<----------------->| GPU 2   |<----------------->| GPU 3   |
+---------+                   +---------+                   +---------+
     \________________________ gather / scatter ______________________/
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 상태 샤딩    | -> | 필요 파라미터 gather | -> | 순전파와 역전파 | -> | gradient scatter | -> | optimizer step |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **상태 샤딩**: optimizer state와 gradient와 파라미터를 장치별로 나눔
2. **필요 파라미터 gather**: 계산 직전에 필요한 파라미터를 모음
3. **순전파와 역전파 수행**: 분산된 환경에서 학습 계산을 진행함
4. **gradient scatter**: 계산 결과를 다시 분산 상태로 정리함
5. **optimizer step**: 샤딩 상태 기준으로 파라미터를 업데이트함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 메모리 절감을 위해 gather와 scatter가 늘어나면 통신 오버헤드가 커져 step time이 악화될 수 있음
   - 해결방안: overlap communication computation과 stage selective deployment를 적용하고 memory saving ratio와 communication overhead ratio로 검증함
2. 문제: stage가 높아질수록 파라미터 관리와 디버깅 복잡도가 증가해 운영 안정성이 낮아질 수 있음
   - 해결방안: observability instrumentation과 deterministic checkpoint design을 적용하고 checkpoint recovery success rate와 debug turnaround time으로 검증함
3. 문제: CPU나 NVMe offload를 과도하게 쓰면 GPU 메모리는 절약되지만 I O 병목으로 전체 처리량이 떨어질 수 있음
   - 해결방안: tiered offload policy와 bandwidth profiling을 적용하고 offload stall ratio와 tokens per second로 검증함

## Ⅶ. 적용 사례

- 초대형 LLM 학습이 stage별 ZeRO 적용 범위를 조정하며 확인 지표는 memory saving ratio와 communication overhead ratio임
- 분산 학습 플랫폼이 체크포인트 관측 도구를 강화하며 확인 지표는 checkpoint recovery success rate와 debug turnaround time임
- GPU 메모리 부족 환경이 계층형 offload 정책을 운영하며 확인 지표는 offload stall ratio와 tokens per second임

## Ⅷ. 결론

ZeRO는 데이터 병렬 학습의 메모리 중복을 근본적으로 줄이는 핵심 기법이지만 stage 선택과 통신 비용 균형이 실효 성능을 좌우함.
