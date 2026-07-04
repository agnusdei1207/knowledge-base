---
title: "라우터 네트워크 (Router Network)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 84
---

# 📖 【암기용】 개념 완전 이해

> 목적: Router Network를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: MoE에서 입력 토큰을 어떤 expert에 보낼지 점수화하고 선택하는 작은 신경망
- **왜 필요한가**: expert가 많아도 적합한 expert를 고르지 못하면 정확도와 처리량이 모두 떨어짐.
- **핵심 직관**: 병원 접수 창구가 환자 증상을 보고 적합한 진료과를 배정하는 역할임.

## 깊이 이해
- **배경·문제의식**: MoE는 token마다 일부 expert만 활성화하므로 routing 품질이 모델 품질을 좌우함. 한 expert로 쏠리면 병목과 expert collapse가 발생함.
- **작동 원리**: token hidden state를 입력받아 expert별 logits를 계산하고 softmax로 확률을 만든 뒤 top-k expert를 선택함. load balancing loss와 capacity factor로 쏠림을 완화함.
- **비유**: 콜센터 IVR이 고객 문의를 결제·배송·환불 부서로 배정하는 것과 같음.
- **구체 예시**: top-2 router는 각 token을 점수 상위 2개 expert로 보내고, expert capacity 초과 시 token drop 또는 fallback을 적용함.
- **흔한 오해·주의점**: router 복잡도 증가는 이득을 보장하지 않음. routing 계산과 통신 오버헤드가 expert 연산 절감 이득을 넘으면 지연이 증가함.

## 연결 개념
- Mixture of Experts — router가 동작하는 모델 구조
- Load Balancing Loss — expert 쏠림 방지
- Expert Parallelism — routing 결과를 분산 GPU로 전송

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Router Network는 MoE에서 token별 expert 선택을 수행하는 gating 신경망임.
> 2. **가치**: 적합한 expert만 활성화해 모델 용량과 추론 비용의 균형을 만든다.
> 3. **판단 포인트**: top-k, capacity factor, load balance loss, expert collapse, routing latency를 관리해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| gating 메커니즘 이해 확인 | logits->softmax->top-k->capacity 처리 순서 | router를 로드밸런서(인프라)와 혼동 |
| 학습 안정화 판단 확인 | load balance loss, router z-loss, collapse 방지 | 선택 정확도만 쓰고 균형 통제 누락 |
| 운영 지표 역량 확인 | entropy, drop rate, load variance 관측 | 지표 없이 "잘 분산된다" 서술 |

> 요약: 이 문제는 router 구조가 아니라 선택 정확도와 부하 균형을 동시에 만족시키는 통제 설계를 묻는다.

## Ⅰ. 개요 및 필요성

- 개요: MoE expert 선택 모듈
- 배경: MoE는 token을 일부 expert에만 보내므로 router 편중이 발생하면 품질 저하, expert 과부하, all-to-all 지연이 생김.
- 필요성: softmax gate, top-k selection, capacity factor, load balance loss로 expert utilization과 token drop rate를 측정해야 함.

## Ⅱ. 구조 및 구성요소

```text
Token Hidden State -> Router Linear -> Expert Logits
      -> Softmax -> Top-k Selection -> Dispatch to Experts
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Router Linear | expert별 점수 계산 | 작은 FFN/linear |
| Softmax Gate | 선택 확률 산출 | entropy 관측 |
| Top-k Selector | 활성 expert 결정 | top-1/top-2 |
| Capacity Control | expert 과부하 제한 | drop/fallback |

> 요약: Router는 token representation을 expert 점수로 바꾸고 top-k 선택과 capacity 제어로 expert에 배정함.

## Ⅲ. 동작원리 및 흐름도

```text
token 입력 -> expert score 계산 -> top-k 선택
    -> capacity 확인 -> expert dispatch -> load 통계 갱신
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | hidden state로 expert logits 계산 | router entropy |
| 2 | top-k expert 선택 | top-k 분포 |
| 3 | capacity 초과 처리 | drop token rate |
| 4 | load balancing loss 반영 | expert load variance |

> 요약: Router는 정확한 expert 선택과 균등 부하 분산을 동시에 만족해야 MoE 효율을 확보함.

## Ⅳ. 특징

| 구분 | Static Routing | Learned Router | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 선택 방식 | 규칙·해시 | token 기반 학습 | 품질 우위 |
| 비용 | 낮음 | routing 계산 추가 | latency 측정 |
| 부하 | 예측 가능 | 쏠림 가능 | load loss 필요 |
| 리스크 | 적응성 낮음 | expert collapse | monitoring 필수 |

> 요약: Learned Router는 expert 적합도를 높이지만, 부하 쏠림과 routing latency를 운영 지표로 통제해야 함.

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | Static Routing (해시·규칙) | Learned Router (gating) | 선택 기준 |
|:---|:---|:---|:---|
| 선택 품질 | 입력 무관 균등 분배 | token 적합 expert 선택 | 품질 우선이면 learned |
| 부하 예측성 | 완전 균등 보장 | 쏠림 가능, loss로 보정 | 지연 예측성 우선이면 static 검토 |
| 학습 비용 | 없음 | auxiliary loss·튜닝 필요 | 학습 인프라·운영 성숙도 |

> 요약: 품질은 learned router가 우위이나, 부하 예측성이 최우선인 환경은 static/hybrid routing도 검토함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| expert collapse | 초기 우세 expert로 선택 고착 | load balance loss, routing temperature | router entropy 하한 유지 |
| token drop | capacity 초과 dispatch | capacity factor 상향, 재라우팅 | drop rate 1% 미만 |
| routing 지연 | 대규모 expert logits 계산 | router 경량화, fused kernel | routing latency 비중 |

> 요약: router 리스크는 고착·drop·지연이며, 균형 손실과 capacity 튜닝으로 통제함.

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. MoE 학습 시 load balance loss와 router z-loss를 적용해 expert load variance를 제한
2. 서빙 시 expert별 token count, drop rate, capacity overflow, all-to-all latency를 수집
3. router collapse 발생 시 capacity factor 조정, expert dropout, routing temperature 조정으로 재학습

**결론 (2줄):**
- 기술사 판단: MoE 성능 병목이 정확도면 routing 품질, 지연이면 capacity와 통신량을 우선 최적화함.
- 향후 방향: Router는 domain expert 선택, tool routing, multi-model routing까지 확장되는 AI 라우팅 핵심 기술이 됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | score->top-k->dispatch 흐름 | static 대비 learned router |
| 요구사항 명시형 | 개선 방안을 제시하시오 | collapse·load imbalance 대응 | entropy·drop rate·latency 기준 |

> 요약: 설명형은 라우팅 계산 원리, 개선형은 expert 쏠림과 지연 통제 중심으로 목차를 전환함.
