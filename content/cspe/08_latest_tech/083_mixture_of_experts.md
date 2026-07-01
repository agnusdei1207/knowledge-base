---
title: "전문가 혼합 (Mixture of Experts)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 83
---

# 📖 【암기용】 개념 완전 이해

> 목적: MoE를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 여러 expert network 중 입력 토큰에 적합한 일부 expert만 선택해 계산하는 조건부 sparse 모델 구조
- **왜 필요한가**: 모델 파라미터를 크게 늘리면서도 매 토큰 계산량은 제한해 비용 대비 성능을 높이기 위함.
- **핵심 직관**: 모든 의사가 한 환자를 보지 않고, 증상에 맞는 전문의 1~2명만 진료하는 방식임.

## 깊이 이해
- **배경·문제의식**: Dense LLM은 파라미터를 키우면 추론 FLOPs도 함께 증가함. MoE는 expert를 많이 두되 router가 top-k expert만 활성화해 총 용량과 활성 계산량을 분리함.
- **작동 원리**: Transformer FFN 일부를 MoE layer로 바꾸고, router가 각 token을 expert로 배정함. expert 출력은 가중합되고, load balancing loss로 특정 expert 쏠림을 방지함.
- **비유**: 콜센터가 모든 상담사를 연결하지 않고, 문의 유형에 맞는 상담사 몇 명만 연결하는 구조임.
- **구체 예시**: top-2 MoE는 token당 expert 2개만 활성화해 총 expert 수가 많아도 활성 FLOPs를 제한함.
- **흔한 오해·주의점**: MoE는 파라미터가 커서 항상 빠른 것이 아님. expert 간 통신, router 편중, 배치 불균형이 지연을 만든다.

## 연결 개념
- Router Network — expert 선택 모듈
- Expert Parallelism — expert를 GPU에 분산하는 방식
- Sparse Model — MoE의 상위 범주

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MoE는 router가 token별 top-k expert를 선택해 일부 전문가만 활성화하는 sparse Transformer 구조임.
> 2. **가치**: 총 파라미터를 늘리면서 활성 FLOPs를 제한해 대형 모델의 비용 효율을 높임.
> 3. **판단 포인트**: top-k, load balancing, expert capacity, all-to-all 통신, expert parallelism이 핵심임.

## Ⅰ. 개요 및 필요성

MoE는 조건부 전문가 선택 모델 구조임. Dense 모델은 파라미터와 계산량이 함께 증가하므로, MoE는 여러 expert 중 일부만 활성화해 모델 용량과 추론 비용을 분리함.

## Ⅱ. 구조 및 구성요소

```text
Token Hidden State → Router → Top-k Experts
      → Expert FFN 계산 → Weighted Combine → Next Layer
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Router | token별 expert 점수 계산 | softmax gating |
| Expert | 독립 FFN 네트워크 | 수십~수백개 구성 |
| Top-k Gate | 선택 expert 제한 | top-1/top-2 |
| Load Balancer | expert 쏠림 방지 | auxiliary loss |

> 요약: MoE는 router가 token을 일부 expert로 보내고 expert 출력만 결합하는 조건부 계산 구조임.

## Ⅲ. 동작원리 및 흐름도

```text
입력 token → router score 산출 → top-k expert 선택
    → expert 병렬 계산 → 출력 가중합 → load 통계 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | hidden state 기반 routing score 계산 | router entropy |
| 2 | top-k expert와 capacity 결정 | drop token rate |
| 3 | expert FFN 병렬 계산 | all-to-all latency |
| 4 | 출력 결합·부하 균형 평가 | expert load variance |

> 요약: MoE 성능은 expert 선택 정확도와 expert 간 부하 균형, GPU 간 통신 비용에 의해 결정됨.

## Ⅳ. 특징

| 구분 | Dense Transformer | MoE Transformer | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 계산 | 모든 FFN 활성 | top-k expert 활성 | active FLOPs 감소 |
| 용량 | 파라미터=계산량 | 총 파라미터와 활성량 분리 | top-2 구조 |
| 병목 | matmul | routing·all-to-all | EP 필요 |
| 리스크 | 예측 가능 | expert imbalance | load loss |

> 요약: MoE는 모델 용량 확장에 유리하지만 router·통신·부하 균형을 운영 지표로 관리해야 함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. MoE 모델 배포 시 expert별 token 분포, drop rate, all-to-all latency를 대시보드화
2. GPU 클러스터는 expert parallelism과 tensor parallelism을 조합해 expert 배치와 통신량을 최적화
3. router collapse 방지를 위해 load balance loss와 capacity factor를 튜닝하고 p95 TPOT를 측정

**결론 (2줄):**
- 기술사 판단: 모델 용량 확장과 추론 비용 절감이 필요하면 MoE, 단순 운영과 안정 지연은 Dense를 선택함.
- 향후 방향: MoE는 LLM scaling의 핵심 구조로 router 품질과 expert parallel runtime이 경쟁력이 됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | routing→expert 계산 흐름 | Dense 대비 특징 |
| 요구사항 명시형 | 설계하시오, 비교하시오 | load balance·EP 설계 절차 | 비용·지연·통신 기준 |

> 요약: 설명형은 조건부 계산 원리, 설계형은 router와 expert 병렬 운영 기준으로 목차를 전환함.
