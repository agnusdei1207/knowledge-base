---
title: "KV Cache 최적화 (KV Cache Optimization)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 56
---

# 📖 【암기용】 개념 완전 이해

> 목적: KV Cache 최적화를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: LLM 디코딩 중 과거 토큰의 Key·Value 텐서를 저장·재사용해 반복 계산을 줄이는 최적화
- **왜 필요한가**: 생성은 한 토큰씩 진행되며, 이전 모든 토큰을 매번 다시 계산하면 지연과 GPU 메모리 사용량이 급증함.
- **핵심 직관**: 이미 읽은 문장의 색인표(K)와 내용표(V)를 책갈피로 저장해 다음 단어 생성 때 다시 읽지 않는 방식임.

## 깊이 이해
- **배경·문제의식**: Transformer 디코더는 새 토큰이 나올 때마다 과거 토큰 전체와 Attention을 계산함. KV Cache가 없으면 길이 T 출력에서 같은 과거 K/V를 T번 재계산함.
- **작동 원리**: prefill 단계에서 입력 프롬프트의 K/V를 만들고, decode 단계에서 새 토큰의 K/V만 cache에 append함. 다음 토큰은 새 Query와 과거 K/V cache를 참조함.
- **비유**: 회의록을 매 질문마다 처음부터 다시 읽지 않고, 주요 문장 색인을 만들어 질문 때마다 색인을 참조하는 것과 같음.
- **구체 예시**: 32-layer, 32-head, head dim 128, FP16 모델에서 4K 토큰 KV Cache는 요청당 수 GB 메모리를 차지할 수 있음.
- **흔한 오해·주의점**: KV Cache는 계산을 줄이지만 메모리를 소비함. 동시 요청 수가 늘면 GPU 메모리 부족과 cache fragmentation이 병목이 됨.

## 연결 개념
- PagedAttention — KV Cache를 페이지 단위로 관리
- Prefix Caching — 공통 prefix의 KV를 재사용
- TPOT — KV Cache 효율이 좌우하는 decode 지연 지표


# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: KV Cache는 과거 토큰의 Key·Value를 저장해 autoregressive decode의 반복 계산을 제거하는 메모리 최적화임.
> 2. **가치**: prefill 이후 토큰당 계산량을 줄여 TPOT와 GPU 사용률을 개선함.
> 3. **판단 포인트**: cache 크기, fragmentation, eviction, quantization, 동시 세션 수가 서빙 처리량을 결정함.


## Ⅰ. 개요 및 필요성

KV Cache 최적화는 LLM 디코딩 메모리 관리 기법임. Auto-regressive 생성은 과거 토큰을 계속 참조하므로, K/V 텐서를 저장·재사용해 반복 계산을 제거하고 동시 요청 처리량을 확보함.


## Ⅱ. 구조 및 구성요소

```text
Prompt Prefill -> K/V Tensor 생성 -> KV Cache 저장

        -------- Decode Token --------
                  Query + Cached K/V -> Next Token
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| K Cache | 과거 토큰 Key 저장 | Attention score 계산 |
| V Cache | 과거 토큰 Value 저장 | context vector 생성 |
| Cache Manager | 할당·해제·eviction 제어 | 세션별 길이 가변 |
| Cache Quantization | KV를 INT8/FP8로 압축 | 메모리 30~50% 절감 |

> 요약: KV Cache는 K/V 저장소와 관리자를 통해 과거 토큰 재계산을 줄이고, 양자화로 메모리 한계를 완화함.


## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> prefill로 초기 KV 생성 -> cache append
    -> 새 토큰 Query 생성 -> cached K/V attention -> 다음 토큰 출력
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 프롬프트 전체 prefill 수행 | TTFT, prompt token 수 |
| 2 | layer/head별 K/V cache 할당 | GB/request, fragmentation |
| 3 | decode마다 새 K/V append | cache hit 100% 유지 |
| 4 | 종료·초과 시 cache 해제/evict | active session, OOM 건수 |

> 요약: prefill에서 만든 K/V를 decode 동안 누적 재사용하고, 요청 종료 시 회수해 GPU 메모리를 순환시킴.


## Ⅳ. 특징

| 구분 | KV Cache 미사용 | KV Cache 사용 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 계산량 | 과거 토큰 반복 계산 | 새 토큰만 계산 | decode FLOPs 감소 |
| 메모리 | 낮음 | 세션 길이에 비례 증가 | GB/request 산정 |
| 처리량 | 긴 출력에서 저하 | 동시 세션 증가 | batching과 결합 |
| 리스크 | 지연 증가 | fragmentation·OOM | PagedAttention 필요 |

> 요약: KV Cache는 decode 계산을 줄이는 대신 GPU 메모리를 소비하므로, 페이지 관리·양자화·eviction 정책이 필수임.


## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. vLLM PagedAttention으로 KV를 16KB~수MB 블록 단위 관리하여 fragmentation과 OOM을 감소
2. KV Cache INT8/FP8 양자화로 메모리 사용량 30~50% 절감, 정확도 회귀는 perplexity·정답률로 검증
3. 세션별 max context와 max output을 제한하고 idle session eviction 5~10분 정책 적용

**결론 (2줄):**
- 기술사 판단: 동시 대화형 LLM 서빙은 KV Cache 최적화 없이는 GPU 메모리와 TPOT SLA를 만족하기 어렵다.
- 향후 방향: PagedAttention·prefix cache·KV quantization 결합이 장문맥 서빙의 표준 구조가 됨.


### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | prefill->decode cache 재사용 흐름 | 계산 절감 vs 메모리 증가 |
| 요구사항 명시형 | 최적화 방안을 제시하시오 | PagedAttention·양자화 적용 절차 | OOM·TPOT·동시성 기준 |

> 요약: 설명형은 KV 재사용 원리, 최적화형은 메모리 관리와 SLA 지표 중심으로 목차를 전환함.
