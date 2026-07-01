---
title: "TPOT 토큰당 출력 지연 (Time Per Output Token)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 62
---

# 📖 【암기용】 개념 완전 이해

> 목적: TPOT를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **정의**: 첫 토큰 이후 출력 토큰 1개를 생성하는 데 걸리는 평균 지연 시간
- **왜 필요한가**: TTFT가 응답 시작 체감 지표라면, TPOT는 답변이 흘러나오는 속도와 전체 완료 시간을 좌우함.
- **핵심 직관**: 첫 반찬이 TTFT라면, 이후 음식이 한 접시씩 나오는 간격이 TPOT임.

## 깊이 이해
- **배경·문제의식**: LLM 디코딩은 이전 토큰을 조건으로 다음 토큰을 생성하는 순차 구조라 병렬화가 제한됨. 긴 답변일수록 TPOT가 전체 지연의 대부분을 차지함.
- **작동 원리**: prefill 후 KV Cache를 참조하며 새 토큰 Query를 계산하고, logits 산출→sampling→KV append를 반복함. decode 단계는 HBM 대역폭과 KV Cache 접근이 병목임.
- **비유**: 긴 보고서를 한 글자씩 받아쓰는 속도임. 시작은 빨라도 글자당 간격이 길면 전체 보고서 완성이 늦어짐.
- **구체 예시**: 70B 모델에서 TPOT 30ms/token, 출력 500토큰이면 decode 시간만 15초임.
- **흔한 오해·주의점**: Throughput이 높아도 개별 사용자 TPOT가 낮다고 단정할 수 없음. 큰 배치는 tokens/s를 높이지만 사용자별 지연을 늘릴 수 있음.

## 연결 개념
- TTFT — 첫 토큰 지연, prefill 병목
- Token Throughput — 전체 토큰 처리량
- Speculative Decoding — TPOT 감소 기법

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TPOT는 LLM decode 단계에서 출력 토큰 1개당 소요되는 지연 지표임.
> 2. **가치**: 장문 생성의 전체 응답 시간을 결정하며, 대화형 UX와 streaming 품질의 핵심 SLA임.
> 3. **판단 포인트**: 모델 크기, batch size, KV Cache, speculative decoding, 양자화가 TPOT를 좌우함.

## Ⅰ. 개요 및 필요성

TPOT는 토큰당 출력 지연 시간임. LLM 서비스는 첫 토큰 이후에도 수백~수천 토큰을 순차 생성하므로, TPOT 관리는 장문 답변 완료 시간과 streaming 체감 속도를 결정함.

## Ⅱ. 구조 및 구성요소

```text
Prefill 완료 → Decode Loop
  → Query 계산 → KV Cache Attention → Logits → Sampling → Token 출력
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Decode Loop | 토큰별 반복 생성 | auto-regressive 순차 구조 |
| KV Cache | 과거 K/V 재사용 | memory bandwidth 병목 |
| Sampler | logits에서 토큰 선택 | top-p, temperature |
| Scheduler | batch·우선순위 제어 | latency/throughput 균형 |

> 요약: TPOT는 decode loop의 토큰별 반복 비용이며 KV Cache 접근과 batch scheduling이 핵심 변수임.

## Ⅲ. 동작원리 및 흐름도

```text
첫 토큰 출력 → 새 토큰 입력화 → cached K/V 참조
    → 다음 토큰 샘플링 → KV append → 종료 조건까지 반복
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 이전 토큰을 다음 step 입력으로 사용 | token dependency |
| 2 | cached K/V 기반 attention 계산 | GPU memory bandwidth |
| 3 | logits sampling 후 토큰 출력 | ms/token, p95 TPOT |
| 4 | EOS 또는 max token 도달 시 종료 | output length, stop reason |

> 요약: TPOT는 매 토큰마다 attention·sampling·cache append를 반복하는 decode 경로의 단위 지연임.

## Ⅳ. 특징

| 구분 | TTFT | TPOT | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 병목 단계 | prefill | decode | compute-bound vs memory-bound |
| 체감 영향 | 응답 시작 | 출력 속도 | 30ms/token이면 33 token/s |
| 최적화 | prefix cache, TP | speculative, quantization | 장문 생성에 영향 큼 |
| SLA | p95 첫 응답 | p95 ms/token | streaming UX 기준 |

> 요약: TPOT는 장문 생성 완료 시간을 지배하므로 TTFT와 분리해 SLA와 최적화 전략을 설계해야 함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. TPOT p95 50ms/token 이하 목표를 설정하고 모델 크기·batch token·KV cache 사용량을 대시보드화
2. Speculative Decoding으로 512토큰 이상 장문 생성 처리량 1.5~3배 개선 여부 검증
3. INT8/FP8 양자화와 GQA/MQA로 KV bandwidth를 줄이고 정확도 회귀를 MMLU·사내셋으로 확인

**결론 (2줄):**
- 기술사 판단: 대화형 서비스는 TTFT 500ms와 TPOT 50ms/token을 함께 관리하고, 배치 분석은 tokens/s를 우선함.
- 향후 방향: TPOT 최적화는 draft decoding, KV quantization, SLA-aware batching 결합으로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | decode loop와 KV Cache 흐름 | TTFT 대비 차이 |
| 요구사항 명시형 | 최적화 방안을 제시하시오 | speculative·양자화 적용 절차 | TPOT·tokens/s·품질 기준 |

> 요약: 설명형은 토큰별 decode 원리, 최적화형은 지연·처리량·품질 균형 중심으로 목차를 전환함.
