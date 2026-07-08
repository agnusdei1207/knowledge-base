---
title: "Mixture of Experts 전문가 혼합 (Mixture of Experts)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 83
extra:
  question_no: "083"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- MoE는 여러 expert 중 일부만 입력마다 선택적으로 활성화하는 조건부 계산 아키텍처임
- dense transformer보다 총 파라미터를 크게 늘리면서도 활성 계산량을 제한할 수 있음
- router, load balancing, expert parallelism이 실제 성능과 운영 안정성을 좌우함

## Ⅰ. 개요

- **정의/개념**: MoE는 여러 개의 expert 네트워크와 이를 선택하는 router를 결합해 입력마다 일부 expert만 활성화함으로써 모델 규모와 계산 비용을 분리하는 희소 아키텍처임
- **배경/필요성**: dense 모델은 성능 향상을 위해 파라미터를 늘릴수록 매 토큰 계산량도 함께 폭증하므로, 총 파라미터는 키우되 활성 계산은 제한하는 구조가 필요함

## Ⅱ. 특징

- 입력마다 top-k expert만 활성화해 동일 활성 FLOPs 대비 더 큰 모델 용량을 확보함
- 특정 expert가 도메인별 패턴을 학습해 다중 능력을 분산 저장하는 구조에 유리함
- router 편향이 생기면 일부 expert에만 토큰이 몰려 품질과 효율이 동시에 무너질 수 있음
- 대규모 학습과 서빙에서는 expert 분산 배치와 통신 최적화가 필수임

## Ⅲ. 종류 및 비교

| 판단 기준 | Dense FFN | Top-1 MoE | Top-2 MoE |
|:---|:---|:---|:---|
| 활성 경로 | 모든 FFN | expert 1개 | expert 2개 |
| 계산 비용 | 높음 | 낮음 | 중간 |
| 표현력 | 기준 | 높음 | 더 높음 |
| 운영 난도 | 낮음 | 높음 | 매우 높음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Router Network | 입력 토큰을 분석해 어떤 expert를 활성화할지 결정하고 부하 균형에도 영향을 줌 |
| Expert Layers | 각 expert가 특정 패턴에 특화된 FFN 계산을 수행해 모델 용량을 확장함 |
| Shared Layers | attention 같은 공통 계층이 전체 문맥을 유지해 expert 선택 전후 흐름을 연결함 |
| Load Balancing Mechanism | 특정 expert 쏠림을 완화해 dead expert와 token drop을 줄임 |

```text
+-------------------+      +-------------------+      +-------------------+
| Shared Layers     | ---> | Router Network    | ---> | Expert Layers     |
+-------------------+      +-------------------+      +-------------------+
                                   |
                                   v
                           +-------------------+
                           | Load Balancing    |
                           +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 토큰 입력      | --> | router 점수 계산 | --> | top-k expert 실행 | --> | 결과 결합/전달  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **토큰 입력**: shared layer를 지난 토큰 표현이 expert 선택 단계로 들어감
2. **router 점수 계산**: 각 expert에 대한 적합도 점수를 계산하고 top-k를 선택함
3. **top-k expert 실행**: 선택된 expert만 토큰을 처리해 조건부 계산을 수행함
4. **결과 결합 및 전달**: expert 출력을 가중 결합해 다음 계층으로 전달함

## Ⅵ. 문제점 및 해결 방안

1. 문제: router가 특정 expert만 반복 선택하면 일부 expert는 훈련되지 않고 일부 expert는 과부하가 걸려 모델 효율이 급격히 떨어질 수 있음
   - 해결방안: auxiliary load balancing loss와 routing noise를 적용하고 expert utilization skew와 dead expert ratio로 균형을 검증함
2. 문제: expert 용량을 초과한 토큰은 drop되거나 지연되어 응답 품질과 안정성이 흔들릴 수 있음
   - 해결방안: capacity factor와 fallback 경로를 설계하고 token drop rate와 tail latency로 처리 안정성을 검증함
3. 문제: 분산 학습과 서빙에서 expert 간 All-to-All 통신이 커지면 계산 이점이 네트워크 병목으로 상쇄될 수 있음
   - 해결방안: expert parallelism과 topology-aware 배치를 적용하고 communication ratio와 throughput으로 확장성을 검증함

## Ⅶ. 적용 사례

- 초거대 LLM 학습이 dense 모델보다 큰 총 파라미터를 운영하도록 MoE를 적용하며 확인 지표는 active FLOPs와 benchmark score임
- 멀티도메인 챗봇이 코딩과 번역과 일반 대화 패턴을 expert별로 분산 학습하도록 MoE를 활용하며 확인 지표는 domain score와 utilization balance임
- 비용 효율형 상용 추론이 활성 계산량을 제한해 비용을 제어하도록 MoE를 적용하며 확인 지표는 cost per token과 throughput임

## Ⅷ. 결론

MoE의 가치는 파라미터 총량과 활성 계산량을 분리해 대형 모델 확장을 가능하게 하는 데 있으며, router 균형과 분산 통신 설계가 성공의 핵심임.
