---
title: "Expert Parallelism 전문가 병렬 (Expert Parallelism)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 85
extra:
  question_no: "085"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- expert parallelism은 MoE의 expert를 여러 GPU나 노드에 분산 배치하는 병렬화 방식임
- expert 선택 결과에 따라 토큰이 장비 사이를 이동하므로 All-to-All 통신이 핵심 병목이 됨
- tensor parallelism, data parallelism, pipeline parallelism과 함께 조합되는 경우가 많음

## Ⅰ. 개요

- **정의/개념**: expert parallelism은 MoE 모델의 여러 expert를 서로 다른 GPU나 노드에 나누어 배치하고, router가 선택한 토큰을 해당 장비로 전달해 병렬 처리하는 분산 실행 기법임
- **배경/필요성**: MoE는 총 파라미터가 매우 커 단일 장비에 적재하기 어렵고, dense 모델용 병렬화만으로는 expert 단위 분산과 조건부 계산을 효율적으로 처리하기 어려움

## Ⅱ. 특징

- expert를 장비별로 분산해 총 모델 용량을 확장하면서 개별 GPU 메모리 부담을 줄임
- 토큰 라우팅에 따라 All-to-All 통신이 발생해 네트워크 토폴로지가 성능의 핵심 변수가 됨
- tensor parallelism보다 MoE 구조에 직접 대응하지만 운영 난도와 디버깅 복잡도는 더 높음
- 토큰 쏠림이 생기면 특정 장비가 병목이 되어 병렬 효율이 급격히 떨어질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Data Parallelism | Tensor Parallelism | Expert Parallelism |
|:---|:---|:---|:---|
| 분산 대상 | 배치 | 텐서 연산 | expert 단위 |
| 대표 병목 | 동기화 | All-reduce | All-to-All |
| 적합 구조 | 일반 학습 | dense 대형 모델 | MoE |
| 운영 난도 | 중간 | 높음 | 매우 높음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Expert Shards | 여러 expert를 GPU와 노드에 나누어 배치해 메모리 수용 한계를 넘김 |
| Token Dispatcher | router 결과에 따라 토큰을 해당 expert가 있는 장비로 전송함 |
| Communication Fabric | NVLink, InfiniBand 같은 고속 네트워크가 병렬 효율을 좌우함 |
| Result Combiner | expert 처리 결과를 원래 순서로 재조합해 다음 계층으로 전달함 |

```text
+-------------------+      +-------------------+      +-------------------+
| Token Dispatcher  | ---> | Expert Shards     | ---> | Result Combiner   |
+-------------------+      +-------------------+      +-------------------+
             |                        ^
             v                        |
   +-------------------+              |
   | Comm. Fabric      |--------------+
   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| router 선택 결과 | --> | 토큰 분산 전송   | --> | 원격 expert 실행 | --> | 결과 재결합     |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **router 선택 결과 확인**: 각 토큰이 어떤 expert로 가야 하는지 결정됨
2. **토큰 분산 전송**: 장비 간 All-to-All 통신으로 토큰을 해당 expert 위치로 보냄
3. **원격 expert 실행**: 각 장비가 자신이 가진 expert로 토큰을 처리함
4. **결과 재결합**: 계산 결과를 원래 흐름에 맞게 다시 합쳐 다음 계층으로 전달함

## Ⅵ. 문제점 및 해결 방안

1. 문제: All-to-All 통신량이 커지면 GPU 계산이 끝나도 네트워크 병목 때문에 전체 처리량이 제한될 수 있음
   - 해결방안: topology-aware 배치와 노드 내 우선 배치를 적용하고 communication ratio와 throughput으로 확장성을 검증함
2. 문제: 특정 expert로 토큰이 몰리면 일부 GPU만 과부하가 걸려 병렬 효율과 tail latency가 함께 악화될 수 있음
   - 해결방안: load balancing과 capacity tuning을 함께 적용하고 per-device utilization skew와 p99 latency로 균형을 검증함
3. 문제: TP, PP, DP와 EP를 섞는 복합 분산 구조는 설정 오류와 장애 분석 난도를 크게 높일 수 있음
   - 해결방안: 병렬화 조합별 표준 토폴로지와 모니터링 지표를 정의하고 deployment failure rate와 MTTR로 운영 복잡도를 검증함

## Ⅶ. 적용 사례

- 초거대 MoE 학습이 수백 개 expert를 다중 노드에 분산하도록 expert parallelism을 적용하며 확인 지표는 throughput과 network utilization임
- 상용 MoE 추론이 비용을 낮추면서 큰 모델을 서빙하도록 expert parallelism을 활용하며 확인 지표는 cost per token과 p95 latency임
- 연구용 하이브리드 병렬화가 TP와 EP를 조합해 확장성을 실험하도록 expert parallelism을 적용하며 확인 지표는 scaling efficiency와 communication overhead임

## Ⅷ. 결론

expert parallelism은 MoE를 실제 대규모 시스템으로 확장하는 핵심 분산 기법이지만, 계산 효율보다 통신 토폴로지와 부하 균형이 성능을 결정한다는 점을 전제로 설계해야 함.
