---
title: "캐싱 전략 — Cache-Aside·Write-Through (Caching Strategy)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 215
---

# 📖 【암기용】 개념 완전 이해

> 목적: 캐싱 전략을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 캐싱 전략은 자주 조회되는 데이터를 원본 저장소(DB)보다 빠른 계층에 두는 **데이터 접근 계층화(Data Access Layering)** 기법이며, 핵심 과제는 캐시와 원본 사이의 **캐시 일관성(Cache Consistency)**을 어떻게 유지하느냐다.
- **왜 필요한가**: 모든 조회가 DB로 직접 가면 특정 데이터에 요청이 몰리는 hot key, 락 경합, I/O 병목으로 응답 지연(p95)이 치솟는다.
- **핵심 직관**: Cache-Aside는 손님이 찾을 때만 창고에서 꺼내 진열대에 두는 것이고, Write-Through는 상품이 바뀔 때 진열대와 창고 장부를 동시에 고치는 것이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| Cache Hit / Miss | 캐시에 원하는 데이터가 있는지(hit) 없는지(miss) | 진열대에 상품이 있나 없나 |
| TTL(Time To Live) | 캐시에 저장된 데이터가 유효한 시간 | 상품의 유통기한 |
| Eviction(LRU/LFU) | 캐시 공간이 부족할 때 오래되거나 덜 쓰인 데이터를 내쫓는 정책 | 안 팔리는 상품을 창고로 되돌림 |
| Invalidation(무효화) | 원본이 바뀌면 캐시를 지우거나 갱신하는 절차 | 가격이 바뀌면 진열 가격표를 즉시 교체 |
| Cache-Aside(Lazy Loading) | miss가 나면 애플리케이션이 DB를 조회한 뒤 그 결과를 캐시에 채우는 방식 | 손님이 찾을 때만 창고에서 꺼내 진열 |
| Write-Through | 쓰기 요청 시 캐시와 원본을 동시에(동기) 갱신하는 방식 | 가격 변경 시 진열대와 창고 장부를 함께 고침 |
| Cache Stampede(Thundering Herd) | 같은 TTL의 데이터가 동시에 만료돼 요청이 한꺼번에 DB로 몰리는 현상 | 유통기한이 같은 상품이 동시에 사라져 손님 모두가 창고로 몰림 |
| Hot Key | 특정 key 하나에 요청이 몰리는 현상 | 인기 상품 한 종류만 손님이 몰려 그 자리만 계속 빔 |
| Single Flight(요청 병합) | 같은 key에 대한 동시 miss를 하나의 DB 조회로 묶어 처리하는 기법 | 같은 상품을 찾는 손님이 몰리면 직원 한 명만 창고에 다녀옴 |

## 깊이 이해

### 왜 필요했나 (배경)
- DB는 영속성과 정합성 보장에 최적화돼 있지만, 모든 읽기 요청을 직접 처리하면 디스크 I/O와 락 경합 비용이 커진다. Redis·Memcached처럼 메모리 기반으로 훨씬 빠른 계층을 앞단에 두면 반복 조회를 값싸게 흡수할 수 있다.

### Hit Ratio를 수치로 이해하기
- 상품 상세 조회가 초당 5,000RPS 들어오는데 캐시 hit ratio가 90%라면, DB로 실제 전달되는 요청은 500RPS(5,000 × 10%)로 줄어든다. hit ratio가 95%면 DB 요청은 250RPS까지 더 줄어든다.
- 즉 hit ratio 5%p 차이가 DB 부하를 2배 가른다. 그래서 캐싱 전략에서는 hit ratio 자체가 핵심 성능 지표가 된다.

### Cache-Aside vs Write-Through 판별 원리
- 판별 기준은 "쓰기 직후 읽기 정합성이 얼마나 중요한가"다.
- Cache-Aside는 읽기 경로만 캐시를 거치고 쓰기는 DB만 갱신한 뒤 캐시를 지운다(또는 그대로 둔다). 구현이 단순하고 읽기 중심 데이터(상품 상세, 설정값)에 적합하지만, 다음 조회 전까지 캐시가 비어 있거나(TTL 동안) 갱신 전 값을 돌려줄 수 있다(stale).
- Write-Through는 쓰기 시점에 캐시와 DB를 함께 갱신해 캐시가 항상 최신 값을 가지도록 보장한다. 재고·가격처럼 쓰기 직후 바로 읽히는 데이터에 적합하지만, 모든 쓰기가 캐시 갱신까지 기다려야 해 쓰기 지연이 늘어난다.
- 실무 판단: 읽기 비율이 80% 이상이고 약간의 지연 허용이 가능하면 Cache-Aside, 쓰기 후 즉시 정합성이 필요하면 Write-Through를 선택한다.

### Cache Stampede를 수치로 이해하기
- TTL을 모두 300초로 동일하게 주면, 같은 시각에 캐시를 채운 key들이 정확히 300초 후 동시에 만료된다. 이때 5,000RPS 트래픽이 한 번에 DB로 쏟아지면 평소 500RPS이던 DB 부하가 순간적으로 5,000RPS까지 10배 튈 수 있다.
- 대응은 두 가지다. ① TTL에 무작위 jitter(예: ±10% = 270~330초)를 줘 만료 시점을 흩뿌린다. ② single flight로 같은 key의 동시 miss를 하나의 DB 조회로 묶어, 나머지 요청은 그 결과를 기다렸다가 재사용한다.

### 비유와 흔한 오해
- **비유**: 도서관 입구의 인기 도서 추천 서가가 캐시다. 서가가 오래 방치되면(무효화 실패) 절판된 판본을 계속 빌려주는 문제가 생긴다.
- **오해**: "캐시 적중률만 높이면 충분하다." 실제로는 stale data, cache stampede, hot key, eviction 정책까지 함께 설계하지 않으면 hit ratio가 높아도 운영 장애가 난다.

## 연결 개념
- Redis - 인메모리 캐시와 분산 락을 제공하는 대표 구현체
- CDN - 정적·동적 콘텐츠를 사용자와 가까운 edge에 캐시하는 상위 확장
- Rate Limiting - Redis 카운터 기반으로 요청 자체를 제한하는 인접 기법

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 캐시 패턴은 읽기/쓰기 비율, 정합성 허용 시간, 장애 시 fallback 기준으로 선택한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 캐싱 전략은 데이터 접근 경로에 임시 저장 계층을 두고 hit/miss/eviction/invalidation을 제어하는 설계이다.
> 2. **가치**: DB QPS, p95 지연, 비용을 cache hit ratio와 TTL 정책으로 제어한다.
> 3. **판단 포인트**: Cache-Aside는 읽기 중심, Write-Through는 쓰기 후 읽기 정합성 요구가 큰 업무에 맞다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 캐시 패턴 이해 확인 | Cache-Aside, Write-Through, TTL, invalidation | 캐시를 단순 메모리 저장소로만 설명 |
| 정합성 판단 확인 | stale 허용 시간, write path, 원본 DB 기준 | "캐시 적중률 향상"만 쓰고 정합성 누락 |
| 장애 대응 확인 | stampede, hot key, eviction, fallback | 캐시 장애 시 전체 장애 전파 누락 |

> 요약: 캐시 답안은 적중률보다 데이터 신선도와 장애 전파 통제를 중심으로 구성해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 반복 조회 데이터 보관 설계
- 배경: DB 직접 조회는 hot data와 피크 트래픽에서 지연과 비용을 만든다.
- 필요성: hit ratio, TTL, 무효화, 장애 시 원본 조회 정책을 함께 정해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> Application -> Cache Layer -> Database
  / Cache Hit -> Return
  / Cache Miss -> DB Read -> Cache Fill -> Return
Write Request -> Cache Update/Invalidate -> DB Commit -> Event Publish
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Cache Store | key-value 임시 저장 | Redis, Memcached, local cache |
| TTL/Eviction | 만료와 공간 회수 | LRU, LFU, TTL jitter |
| Invalidation | 원본 변경 시 캐시 제거·갱신 | 이벤트 기반 삭제, version key |
| Fallback | 캐시 장애 시 원본 접근 | circuit breaker, degraded response |

> 요약: 캐시 구조는 저장소, 만료, 무효화, 장애 fallback을 함께 설계해야 한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Read Request -> Cache Lookup
  / Hit -> Return Cached Data
  / Miss -> DB Query -> Cache Set with TTL -> Return
Write Request -> DB Commit -> Cache Delete/Update -> Event Audit
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | key 설계와 조회 | key cardinality, namespace |
| 2 | miss 시 DB 조회와 cache fill | DB QPS 제한, TTL 300초 |
| 3 | 쓰기 후 삭제 또는 갱신 | invalidation lag 1초 이하 |
| 4 | 장애·동시 miss 제어 | single flight, lock TTL 5초 |

> 요약: 캐시 동작은 읽기 경로와 쓰기 후 무효화 경로를 분리해 검증해야 한다.

---

## Ⅳ. 특징

| 구분 | Cache-Aside | Write-Through | 판단 수치 |
|:---|:---|:---|:---|
| 읽기 | miss 시 애플리케이션이 DB 조회 | 캐시에 항상 최신 값 기대 | 읽기 80% 이상이면 Cache-Aside |
| 쓰기 | DB 갱신 후 삭제/무효화 | 캐시와 DB 동기 갱신 | 쓰기 지연 허용 10ms 이하 여부 |
| 정합성 | TTL 동안 stale 가능 | 쓰기 직후 읽기 일관성 확보 | stale 허용 1~300초 |
| 운영 부담 | stampede 제어 필요 | write path 복잡도 증가 | hit ratio 80% 이상 목표 |

> 요약: Cache-Aside는 읽기 확장, Write-Through는 쓰기 후 즉시 조회 정합성이 판단 기준이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Caching Strategy | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | DB 직접 조회 | Cache -> DB 계층화 | 동일 key 반복 조회 10회/min 이상 |
| 비용/성능 | DB I/O 증가 | hit ratio로 DB QPS 감소 | hit 90%, DB QPS 70% 감소 목표 |
| 운영/위험 | 단순 정합성 | stale·stampede·hot key | stale 허용 시간과 장애 fallback 필요 |

> 요약: 캐시는 반복 조회와 stale 허용 시간이 수치로 확인될 때 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Cache Stampede | TTL 동시 만료 | TTL jitter, single flight, mutex | simultaneous miss count |
| Hot Key | 특정 key 집중 | key sharding, local cache, replication | top key QPS 비율 20% 이하 |
| Stale Data | 무효화 지연 | event invalidation, versioned key | invalidation lag 1초 이하 |

> 요약: 캐시 장애의 핵심은 동시 miss, hot key, stale이며 각각 분산·락·무효화로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 적중률 | cache hit ratio 80~95% | Redis INFO, APM |
| 지연 | cache p95 5ms 이하, API p95 200ms 이하 | tracing, latency histogram |
| 정합성 | stale response 0.1% 이하 | version compare, audit sample |

> 요약: 캐시 효과는 hit ratio, p95 지연, stale 비율을 동시에 확인해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 읽기 중심 상품·설정 데이터는 Cache-Aside, TTL 300초, TTL jitter 10%, miss lock TTL 5초 적용
2. 재고·가격처럼 쓰기 후 조회가 민감한 데이터는 Write-Through 또는 DB commit 후 event invalidation 적용
3. Redis cluster, key namespace, top key 모니터링, circuit breaker로 cache 장애 시 DB QPS 상한 설정

**결론 (2줄):**
- 기술사 판단: 읽기 80% 이상과 stale 허용 가능 업무는 Cache-Aside, 쓰기 직후 일관성이 핵심인 업무는 Write-Through 선택
- 향후 방향: 애플리케이션 캐시, Redis, CDN, DB materialized view를 계층화하고 OpenTelemetry로 hit/miss를 추적하는 방향으로 운영

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "캐싱 전략을 설명하시오" | hit/miss, TTL, invalidation 흐름 | Cache-Aside와 Write-Through 비교 |
| 요구사항 명시형 | "DB 부하 감소 방안을 제시하시오" | stampede, hot key, stale 제어 | hit ratio·DB QPS·정합성 기준 |

> 요약: 설명형은 패턴 원리, 방안형은 DB 부하와 정합성 지표 중심으로 작성한다.
