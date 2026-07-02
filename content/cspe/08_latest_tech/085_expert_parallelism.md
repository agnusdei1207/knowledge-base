---
title: "전문가 병렬 (Expert Parallelism)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 85
---

# 📖 【암기용】 개념 완전 이해

> 목적: Expert Parallelism을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: MoE 모델의 여러 expert를 여러 GPU/노드에 분산 배치해 병렬 실행하는 방식
- **왜 필요한가**: expert 수가 많아지면 단일 GPU 메모리에 담기 어렵고, token routing 결과를 여러 장치에서 처리해야 함.
- **핵심 직관**: 각 전문의를 다른 진료실에 배치하고, 접수창구가 환자를 해당 진료실로 보내는 운영 방식임.

## 깊이 이해
- **배경·문제의식**: MoE는 총 파라미터가 크고 expert가 많다. Expert Parallelism은 expert를 GPU별로 나누어 저장하고, token을 선택된 expert가 있는 GPU로 전송함.
- **작동 원리**: router가 token별 expert를 선택하면 all-to-all 통신으로 token hidden state를 expert 보유 GPU에 보냄. expert 계산 후 결과를 다시 원래 순서로 모아 다음 layer로 전달함.
- **비유**: 물류센터에서 상품 종류별 창고가 다르고, 주문서에 따라 해당 창고로 물건을 보내 포장 후 다시 배송 라인으로 합치는 것과 같음.
- **구체 예시**: expert 64개를 GPU 8장에 나누면 GPU당 expert 8개를 보유하고, token은 top-2 expert 위치로 dispatch됨.
- **흔한 오해·주의점**: Expert Parallelism은 계산을 나누지만 통신을 늘림. 네트워크 bandwidth와 expert load balance가 맞지 않으면 TPOT가 증가함.

## 연결 개념
- Mixture of Experts — Expert Parallelism 적용 모델
- All-to-All Communication — token dispatch 통신
- Tensor Parallelism — matrix 내부 분할 방식

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Expert Parallelism은 MoE expert를 GPU/노드에 분산 배치하고 token을 expert 위치로 dispatch하는 병렬화 방식임.
> 2. **가치**: 총 expert 파라미터를 여러 GPU 메모리에 분산해 대규모 MoE 학습·추론을 가능하게 함.
> 3. **판단 포인트**: all-to-all 통신, expert load balance, capacity factor, TP/DP 조합이 성능을 결정함.

## Ⅰ. 개요 및 필요성

- 개요: MoE expert 분산 병렬화 기법
- 배경: expert 수와 총 파라미터가 큰 MoE 모델은 단일 GPU VRAM에 적재하기 어렵고 expert별 부하도 불균등함.
- 필요성: expert shard, all-to-all dispatch/combine, EP/TP/DP 조합으로 GPU 메모리와 통신 병목을 함께 계획해야 함.

## Ⅱ. 구조 및 구성요소

```text
Tokens -> Router -> All-to-All Dispatch
      -> GPU별 Experts -> Expert Compute -> All-to-All Combine
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Expert Shard | GPU별 expert 배치 | expert 수/GPU |
| Dispatch | token을 expert GPU로 전송 | all-to-all |
| Combine | expert 출력 재조립 | token order 복원 |
| Parallel Planner | EP/TP/DP 조합 결정 | cluster topology |

> 요약: Expert Parallelism은 expert 저장 위치와 token 이동 경로를 설계해 MoE를 분산 실행함.

## Ⅲ. 동작원리 및 흐름도

```text
router top-k 선택 -> token을 expert GPU로 dispatch
    -> expert FFN 계산 -> 결과 combine -> 다음 layer 진행
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | expert를 GPU/노드에 분산 배치 | memory/GPU |
| 2 | token routing 결과로 dispatch 수행 | all-to-all bytes |
| 3 | expert별 FFN 병렬 계산 | expert utilization |
| 4 | 결과 combine·순서 복원 | TPOT, load variance |

> 요약: EP는 expert 메모리를 분산하지만 token 이동 통신이 병목이므로 topology-aware 배치가 필요함.

## Ⅳ. 특징

| 구분 | Tensor Parallelism | Expert Parallelism | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 분할 대상 | 행렬 연산 내부 | expert 단위 | MoE 전용 |
| 통신 | all-reduce 중심 | all-to-all 중심 | 네트워크 민감 |
| 장점 | dense layer 확장 | expert 파라미터 분산 | GPU당 expert 수 |
| 리스크 | matmul 통신 | load imbalance | capacity factor |

> 요약: Expert Parallelism은 MoE 확장에 필수이나, all-to-all 통신과 expert 부하 편차가 지연의 핵심 변수임.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. expert 수, GPU 수, GPU당 VRAM으로 expert placement를 산정하고 NVLink/IB topology 기준으로 배치
2. expert별 token count, all-to-all bytes, p95 TPOT, dropped token을 모니터링
3. EP는 TP/DP와 조합해 dense attention은 TP, MoE FFN은 EP, batch 복제는 DP로 분리 설계

**결론 (2줄):**
- 기술사 판단: MoE 모델은 Expert Parallelism을 기본으로 두고, 통신 병목이 크면 expert 수·top-k·capacity를 재조정함.
- 향후 방향: MoE runtime은 topology-aware routing과 communication overlap으로 all-to-all 병목을 줄이는 방향으로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | dispatch->expert compute->combine 흐름 | TP 대비 특징 |
| 요구사항 명시형 | 설계하시오, 최적화하시오 | expert placement·통신 측정 절차 | all-to-all·load balance 기준 |

> 요약: 설명형은 MoE 분산 실행 원리, 설계형은 GPU 배치와 통신 병목 기준으로 목차를 전환함.
