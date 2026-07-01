---
title: "접두 캐싱 (Prefix Caching)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 60
---

# 📖 【암기용】 개념 완전 이해

> 목적: Prefix Caching을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 여러 요청이 공유하는 system prompt·문서 prefix의 KV Cache를 재사용해 prefill 지연을 줄이는 기법
- **왜 필요한가**: RAG·에이전트·챗봇은 긴 system prompt와 공통 지침을 매 요청 반복 처리해 TTFT가 증가함.
- **핵심 직관**: 매번 같은 서론을 다시 읽지 않고, 이미 읽어둔 서론의 책갈피를 다음 요청에 재사용하는 방식임.

## 깊이 이해
- **배경·문제의식**: LLM 요청은 `system prompt + policy + retrieved context + user query`로 구성됨. 동일한 앞부분(prefix)을 매번 prefill하면 GPU compute가 반복 낭비됨.
- **작동 원리**: 토큰화된 prefix를 해시 키로 만들고, 해당 prefix의 KV Cache가 있으면 prefill을 건너뛰거나 suffix만 계산함. prefix가 조금이라도 달라지면 cache miss가 발생함.
- **비유**: 시험 답안의 공통 머리말을 매번 새로 쓰지 않고, 미리 작성된 머리말 뒤에 문제별 본문만 이어 쓰는 것과 같음.
- **구체 예시**: 긴 system prompt 2K 토큰이 모든 요청에 공통이면, prefix cache hit 시 prefill 토큰 2K 계산을 생략해 TTFT를 800ms→80ms 수준으로 줄일 수 있음.
- **흔한 오해·주의점**: prefix caching은 완전히 같은 prefix에 강함. 사용자별 권한·시간·검색 결과가 prefix 앞쪽에 섞이면 hit rate가 낮아짐.

## 연결 개념
- TTFT — Prefix Caching의 직접 개선 지표
- KV Cache — 재사용되는 캐시 데이터
- Prompt Template — prefix 안정성이 cache hit를 좌우


# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Prefix Caching은 동일 prefix의 KV Cache를 재사용해 LLM prefill 연산과 TTFT를 줄이는 서빙 최적화임.
> 2. **가치**: 공통 system prompt·정책·문서 prefix를 반복 계산하지 않아 대화형 서비스 응답 시작 지연을 낮춤.
> 3. **판단 포인트**: prefix 안정성, cache key, hit rate, 권한 분리, eviction 정책이 운영 기준임.


## Ⅰ. 개요 및 필요성

Prefix Caching은 공통 프롬프트 KV 재사용 기법임. LLM 서비스는 system prompt와 정책 문구를 반복 포함하므로, 동일 prefix prefill을 재사용해 TTFT와 GPU compute 낭비를 줄임.


## Ⅱ. 구조 및 구성요소

```text
Request Prefix → Token Hash → Prefix Cache Lookup
        ├─ Hit  → Cached KV + Suffix Prefill → Decode
        └─ Miss → Full Prefill → KV Store → Decode
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Prefix Key | prefix token sequence 해시 | tokenizer·template 일치 필요 |
| KV Store | prefix K/V 저장 | GPU/CPU tier 가능 |
| Cache Lookup | hit/miss 판단 | exact match 중심 |
| Eviction Policy | 오래된 prefix 제거 | LRU, TTL, tenant 분리 |

> 요약: Prefix Caching은 prefix token 해시로 KV를 조회하고, hit 시 suffix만 계산해 prefill 비용을 줄임.


## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 → prefix 추출 → hash 조회
    → hit: cached KV 재사용 → suffix 계산 → 응답
    → miss: 전체 prefill → KV 저장 → 응답
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | system prompt·공통 문서 prefix 분리 | prefix token 수 |
| 2 | tokenizer 기준 token hash 생성 | hash collision 방지 |
| 3 | KV cache hit/miss 처리 | hit rate, TTFT |
| 4 | tenant·권한 기준 cache 격리 | cross-tenant leak 0건 |

> 요약: prefix를 안정적으로 분리하고 동일 token sequence를 재사용할 때 TTFT 개선 효과가 커짐.


## Ⅳ. 특징

| 구분 | Prefix Caching 미적용 | Prefix Caching 적용 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| prefill | 매 요청 전체 계산 | 공통 prefix 생략 | 2K token 절감 |
| TTFT | prompt 길이에 비례 | hit 시 suffix 중심 | 800ms→80ms 사례 |
| hit 조건 | 해당 없음 | prefix exact match | template 안정화 필요 |
| 리스크 | 단순 | 권한·tenant 격리 필요 | cache key에 tenant 포함 |

> 요약: Prefix Caching은 반복 prefix가 긴 서비스에서 효과가 크며, 권한별 cache 격리가 보안 설계의 핵심임.


## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. system prompt·정책 문구를 요청 앞단에 고정하고 사용자별 동적 값은 suffix로 이동해 cache hit rate 70% 이상 확보
2. cache key에 model id, tokenizer version, tenant id, prompt version을 포함해 권한 오염 차단
3. TTFT p95, prefix hit rate, saved prefill tokens를 대시보드화하고 LRU/TTL eviction을 운영 정책으로 설정

**결론 (2줄):**
- 기술사 판단: 공통 prefix가 1K 토큰 이상이고 hit rate 50% 이상이면 Prefix Caching을 우선 적용함.
- 향후 방향: RAG·에이전트 시스템은 prompt template 표준화와 prefix cache를 결합해 대화형 SLA를 맞춤.


### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | hit/miss 기반 prefill 재사용 흐름 | 미적용 대비 TTFT |
| 요구사항 명시형 | 최적화 방안을 제시하시오 | prefix 분리·cache key·격리 절차 | hit rate·보안·eviction 기준 |

> 요약: 설명형은 KV 재사용 원리, 최적화형은 hit rate와 tenant 격리 중심으로 목차를 전환함.
