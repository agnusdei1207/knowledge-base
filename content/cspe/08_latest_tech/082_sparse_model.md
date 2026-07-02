---
title: "희소 모델 (Sparse Model)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 82
---

# 📖 【암기용】 개념 완전 이해

> 목적: 희소 모델을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 전체 파라미터 중 일부 연결·뉴런·전문가만 활성화해 연산량을 줄이는 모델 구조
- **왜 필요한가**: dense model은 모든 요청마다 모든 파라미터를 사용해 비용이 크므로, 필요한 부분만 계산하는 구조가 필요함.
- **핵심 직관**: 모든 부서가 매 업무에 참여하지 않고, 해당 업무 전문가만 호출하는 조직 운영 방식임.

## 깊이 이해
- **배경·문제의식**: 모델 규모를 키우면 정확도는 올라가지만 추론 비용도 증가함. Sparse model은 총 파라미터는 크게 유지하면서 활성 파라미터만 줄여 비용과 성능의 균형을 노림.
- **작동 원리**: weight sparsity는 일부 weight를 0으로 만들고, activation sparsity는 일부 뉴런만 활성화함. MoE는 여러 expert 중 top-k만 선택해 조건부 계산을 수행함.
- **비유**: 백화점 전체 직원 명단은 크지만, 고객 질문에 맞는 매장 직원 1~2명만 응대하는 것과 같음.
- **구체 예시**: MoE 모델은 총 파라미터가 크더라도 token당 활성 expert 수를 1~2개로 제한해 FLOPs를 조절함.
- **흔한 오해·주의점**: sparsity가 있으면 무조건 빨라지는 것은 아님. sparse kernel, load balancing, 통신 비용이 맞아야 실제 지연이 줄어듦.

## 연결 개념
- Model Pruning — weight sparsity 생성 기법
- Mixture of Experts — 조건부 sparse model
- Expert Parallelism — MoE 분산 실행 방식

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Sparse Model은 전체 파라미터 중 일부만 활성화해 연산량과 추론 비용을 줄이는 모델 구조임.
> 2. **가치**: 모델 용량은 키우면서 token당 계산량을 제한해 대규모 AI의 비용 효율을 높임.
> 3. **판단 포인트**: sparsity 유형, kernel 지원, load balancing, 정확도·지연 실측이 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 희소 구조 원리 이해 확인 | 총 파라미터와 활성 FLOPs 분리, mask/router 선택 계산 | pruning(압축)과 sparse 구조(MoE) 혼동 |
| 비용 효율 판단 확인 | active params/token 기준 비용 산정 | "가볍다" 수준의 근거 없는 서술 |
| 운영 리스크 인식 확인 | load imbalance, expert collapse, kernel 미지원 시 효과 상실 | 이론 FLOPs 절감을 실측 지연 개선으로 단정 |

> 요약: 이 문제는 구조 소개가 아니라 용량-계산량 분리의 원리와 실측 기반 효율 검증을 묻는다.

## Ⅰ. 개요 및 필요성

- 개요: 필요한 연산만 활성화하는 모델 구조
- 배경: dense model은 요청마다 모든 파라미터를 사용해 모델 용량 증가가 token당 FLOPs 증가로 이어짐.
- 필요성: sparsity mask, router, sparse kernel, load balance loss로 활성 FLOPs와 품질·부하 편중을 함께 관리해야 함.

## Ⅱ. 구조 및 구성요소

```text
Input Token -> Router/Mask -> Active Weights/Experts
      -> Sparse Compute -> Output -> Load/Quality Monitor
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Sparsity Mask | 활성 요소 선택 | pruning, gating |
| Sparse Kernel | 0 또는 비활성 요소 skip | HW 지원 필요 |
| Router/Gate | expert 선택 | MoE top-k |
| Balancer | 활성도 편중 완화 | load balance loss |

> 요약: 희소 모델은 mask·router로 계산 대상을 선택하고 sparse kernel·balancer로 실제 효율을 확보함.

## Ⅲ. 동작원리 및 흐름도

```text
입력 수신 -> 활성 요소 선택 -> 선택 부분만 계산
    -> 출력 결합 -> load·latency·accuracy 평가
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | weight/neuron/expert 중요도 판단 | sparsity ratio |
| 2 | 활성 subset 계산 | active params/token |
| 3 | 결과 결합·정규화 | output quality |
| 4 | 부하·정확도 모니터링 | p95 latency, imbalance |

> 요약: Sparse model은 선택 계산으로 FLOPs를 줄이지만 선택 편중과 kernel 효율을 계속 관리해야 함.

## Ⅳ. 특징

| 구분 | Dense Model | Sparse Model | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 계산 | 모든 파라미터 활성 | 일부만 활성 | active params/token |
| 용량 | 파라미터=계산량 | 총 용량과 계산량 분리 | MoE 구조 |
| 지연 | 예측 용이 | router·통신 비용 | p95 실측 |
| 리스크 | 비용 증가 | load imbalance | expert collapse |

> 요약: 희소 모델은 대형 모델 용량과 추론 비용을 분리하지만, 하드웨어와 분산 실행이 맞아야 효과가 발생함.

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | Pruning (정적 희소화) | MoE (동적 희소화) | 선택 기준 |
|:---|:---|:---|:---|
| 희소성 결정 시점 | 학습 후 고정 | 추론 시 token별 선택 | 입력 다양성이 크면 동적 |
| 효과 조건 | sparse kernel HW 지원 | expert parallel 인프라 | 보유 인프라 지원성 |
| 품질 영향 | 압축률 비례 저하 | 용량 유지·품질 보존 | 품질 요구 수준 |

> 요약: 단말 배포용 경량화는 pruning, 대형 모델 용량 확장은 MoE로 희소화 방식을 구분해 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 이론-실측 괴리 | sparse kernel 미지원 | 대상 HW에서 latency 직접 측정 | 실측 p95 개선율 |
| 부하 편중 | router가 특정 expert 집중 선택 | load balance loss, capacity factor | expert load variance |
| 품질 저하 | 과도한 sparsity ratio | 비율 단계적 상향, 회귀 테스트 | 벤치마크 점수 유지 |

> 요약: 희소화 리스크는 실측 미검증과 편중이며, HW 실측과 균형 손실 함수로 통제함.

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. LLM 확장은 dense 70B 대신 MoE top-2 구조를 검토하고 active FLOPs/token 기준으로 비용 산정
2. pruning 기반 sparse model은 sparse kernel 지원 GPU/CPU에서 latency를 직접 측정
3. MoE 운영은 expert별 token 비율, p95 latency, dropped token, load balance loss를 모니터링

**결론 (2줄):**
- 기술사 판단: 모델 용량 확대와 추론 비용 절감이 동시에 필요하면 sparse/MoE, 예측 가능한 지연은 dense model을 선택함.
- 향후 방향: 희소 모델은 router 학습, expert parallelism, sparse accelerator와 결합해 대규모 LLM의 핵심 구조가 됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | 활성 subset 선택·계산 흐름 | Dense 대비 특징 |
| 요구사항 명시형 | 비교하시오, 설계하시오 | sparsity ratio·kernel 검증 절차 | 비용·지연·load balance 기준 |

> 요약: 설명형은 선택 계산 원리, 설계형은 실제 지연과 부하 균형 기준으로 목차를 전환함.
