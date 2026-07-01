---
title: "토큰 처리량 (Token Throughput)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 63
---

# 📖 【암기용】 개념 완전 이해

> 목적: Token Throughput을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **정의**: LLM 서빙 시스템이 단위 시간당 처리하는 입력·출력 토큰 수
- **왜 필요한가**: 개별 사용자 지연이 SLA라면, 처리량은 GPU당 수용 가능한 트래픽과 비용을 결정함.
- **핵심 직관**: 식당에서 손님 한 명 대기시간이 지연이라면, 시간당 몇 접시를 내는지가 처리량임.

## 깊이 이해
- **배경·문제의식**: LLM 비용은 GPU 시간과 토큰 수에 비례함. 같은 모델이라도 batch scheduling, KV Cache, quantization에 따라 GPU 1장당 tokens/s가 크게 달라짐.
- **작동 원리**: prefill throughput은 입력 토큰 행렬곱 성능, decode throughput은 KV Cache memory bandwidth와 active batch 크기에 좌우됨. serving engine은 두 작업을 섞어 GPU 유휴 시간을 줄임.
- **비유**: 공장의 컨베이어 처리량처럼 개별 제품 시간이 아니라 전체 라인이 초당 몇 개를 생산하는지 보는 지표임.
- **구체 예시**: output throughput 10,000 tokens/s인 클러스터는 평균 500토큰 응답을 초당 20건 처리함.
- **흔한 오해·주의점**: tokens/s를 높이려고 batch를 키우면 p95 TTFT·TPOT가 악화될 수 있음. 처리량과 지연은 함께 봐야 함.

## 연결 개념
- TTFT/TPOT — 사용자 지연 지표
- Continuous Batching — 처리량 향상 스케줄링
- LLM Serving — 처리량 최적화 적용 영역

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Token Throughput은 LLM 시스템이 초당 처리하는 input/output token 수로 GPU 효율을 나타내는 지표임.
> 2. **가치**: GPU당 수용 요청 수와 token당 원가를 산정하여 LLM 서비스 TCO를 결정함.
> 3. **판단 포인트**: prefill/decode 분리, batch token, latency SLA, cache hit rate를 함께 최적화해야 함.

## Ⅰ. 개요 및 필요성

Token Throughput은 LLM 토큰 처리량 지표임. 생성형 AI 서비스는 호출량 증가 시 GPU 비용이 급증하므로, 초당 토큰 처리량을 기준으로 용량 계획과 비용 최적화를 수행함.

## Ⅱ. 구조 및 구성요소

```text
Requests → Scheduler → Prefill Tokens/s + Decode Tokens/s
       → GPU Utilization → Cost per 1K Tokens
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Input Throughput | prefill 입력 토큰 처리량 | prompt 길이에 비례 |
| Output Throughput | decode 출력 토큰 처리량 | KV bandwidth 영향 |
| Scheduler | batch token·우선순위 제어 | latency와 trade-off |
| Cost Meter | token당 GPU 비용 산정 | $/1K tokens, GPU-hour |

> 요약: Token Throughput은 입력·출력 토큰 처리량과 GPU 비용을 연결하는 LLM 용량 계획 지표임.

## Ⅲ. 동작원리 및 흐름도

```text
트래픽 수집 → 입력/출력 토큰 계측 → batch 구성
    → GPU 실행 → tokens/s 산출 → 비용·SLA 비교
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 요청별 input/output token 수 계측 | tokenizer 기준 |
| 2 | prefill/decode batch 스케줄링 | max batch token |
| 3 | GPU 실행률과 tokens/s 계산 | GPU util 70~90% |
| 4 | 지연 SLA와 비용 동시 평가 | p95 latency, $/1K tokens |

> 요약: 토큰 계측→스케줄링→GPU 실행→비용 환산을 반복해 처리량과 SLA 균형점을 찾음.

## Ⅳ. 특징

| 구분 | 지연 중심 지표 | 처리량 중심 지표 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 대표 지표 | TTFT, TPOT | tokens/s, req/s | 사용자 vs 운영자 관점 |
| 최적화 방향 | batch 축소 | batch 확대 | trade-off 관리 |
| 비용 영향 | SLA 위반 방지 | GPU당 원가 절감 | $/1K token |
| 리스크 | 과소 활용 | tail latency 증가 | p95/p99 동시 관측 |

> 요약: Token Throughput은 비용 최적화 지표이며, latency SLA와 함께 관리해야 운영 품질이 유지됨.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. input/output tokens/s, req/s, GPU util, $/1K tokens를 대시보드로 분리해 용량 계획 수립
2. Continuous Batching으로 GPU 유휴 시간을 줄이되 max waiting time 20~50ms로 tail latency 제한
3. 모델별 처리량 벤치마크를 기준으로 7B/13B/70B 라우팅 정책을 구성해 GPU 비용 30% 이상 절감

**결론 (2줄):**
- 기술사 판단: 대화형 SLA는 TTFT/TPOT 우선, 배치 분석·백오피스는 Token Throughput 우선으로 설계함.
- 향후 방향: 서빙 엔진은 latency-aware batching과 FinOps 계측을 결합해 token당 원가를 자동 최적화함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | 토큰 계측·스케줄링 흐름 | 지연 지표 대비 차이 |
| 요구사항 명시형 | 용량 산정하시오, 최적화하시오 | tokens/s 기반 비용 산정 | batch·SLA·GPU 원가 기준 |

> 요약: 설명형은 처리량 개념, 산정형은 GPU 용량과 token당 비용 계산 중심으로 목차를 전환함.
