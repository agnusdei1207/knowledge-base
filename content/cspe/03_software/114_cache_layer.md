---
title: "캐시 계층 - Redis·Memcached (Cache Layer)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 114
---

# 📖 【암기용】 개념 완전 이해

> 목적: 캐시 계층을 처음 보는 사람도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 컴퓨터 구조의 **지역성(Locality)** 원리를 응용해, 자주 조회되는 데이터를 원본 저장소(DB)보다 빠른 **메모리 계층**(Redis·Memcached)에 두어 반복 조회 비용을 낮추는 **캐시** 기법이다.
- **왜 필요한가**: 같은 상품·세션·설정을 반복 조회하면 DB의 CPU·디스크 IO가 매번 같은 일을 되풀이한다. 메모리 캐시는 이 반복 조회를 흡수해 DB 부하와 응답 지연을 함께 낮춘다.
- **핵심 직관**: 자주 쓰는 도구를 창고(DB) 깊숙이 보관하지 않고 책상 위(캐시)에 꺼내 두어, 매번 창고까지 가지 않고 바로 손에 쥐는 방식이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 지역성(Locality) | 최근 쓴 데이터가 곧 다시 쓰일 가능성이 높다는 성질 — 캐시가 성립하는 **근거** | 방금 꺼낸 책을 또 찾을 확률이 높다 |
| Cache Hit / Miss | 캐시에서 값을 찾음 / 못 찾아 원본을 조회함 | 책상에 있음 / 없어서 창고까지 감 |
| Hit Ratio | 전체 조회 중 hit 비율 | 책상에서 바로 찾는 비율 |
| TTL(Time To Live) | 캐시 값이 유효한 시간 | 유통기한 |
| Eviction(축출) | 메모리가 부족할 때 오래되거나 안 쓰는 값을 밀어내는 것 | 책상이 좁아 안 쓰는 책부터 치움 |
| Cache-aside | 애플리케이션이 캐시를 먼저 보고, miss 시 DB를 읽어 캐시에 채움 | 책상에 없으면 창고에서 가져와 책상에 올려둠 |
| Write-through | 쓰기 시 캐시와 DB를 동시에 갱신 | 책상과 창고 장부를 같이 고침 |
| Write-back(write-behind) | 캐시에 먼저 쓰고, DB 반영은 나중에 | 책상에만 먼저 적고 창고 장부는 나중에 |
| Cache Stampede | TTL이 동시에 끝나며 다수 요청이 한꺼번에 DB로 몰리는 현상 | 유통기한이 같은 날 몰려 있어 한꺼번에 창고로 몰려감 |
| Single-flight(요청 병합) | 동시에 들어온 같은 key의 miss 요청을 1건으로 묶어 DB에 보냄 | 같은 물건 요청 여러 건을 창고엔 한 번만 보냄 |

## 깊이 이해

### 왜 캐시가 필요했나 (지역성과 메모리 계층)
- CPU 캐시가 레지스터·메모리·디스크 사이의 속도 차이를 메우듯, 애플리케이션 캐시는 메모리와 디스크 기반 DB 사이의 속도 차이를 메운다. 메모리 접근은 마이크로초 단위, 네트워크를 거치는 DB 조회는 밀리초 단위로 최소 수백 배 이상 차이가 난다.
- 인기 상품 상세 조회처럼 같은 key가 초당 5만 건씩 반복되면, 이 요청들은 "지역성"이 매우 높은 트래픽이다 — 즉 캐시 효과가 극대화되는 대상이다.

### Hit Ratio로 효과를 계산해보기 (수치)
- 상품 상세 API에 Redis TTL 300초를 적용해 hit ratio 90%를 달성했다고 하자. 전체 DB read QPS 50,000 중 45,000(=50,000×0.9)건은 캐시가 흡수하고, DB에는 miss분 5,000건만 도달한다. DB 부하가 **10분의 1**로 줄어드는 셈이다.
- 반대로 hit ratio가 50%로 떨어지면 DB에는 25,000건이 몰린다. hit ratio는 TTL 길이, key 설계, 트래픽 편중(hot key)에 따라 크게 달라지므로 캐시 도입 효과는 hit ratio 수치로 검증해야 한다.

### 3가지 쓰기 패턴 판별 — 언제 무엇을 쓰나
- **Cache-aside**: 애플리케이션이 캐시를 먼저 조회(get)하고, miss면 DB를 읽어 캐시에 저장(set)한다. 가장 흔한 패턴이며 읽기가 많고 최신성 요구가 느슨할 때 적합하다.
- **Write-through**: 쓰기 요청마다 캐시와 DB를 함께 갱신한다. 캐시가 항상 최신이지만 모든 쓰기에 캐시 갱신 비용이 붙어 쓰기 지연이 늘어난다.
- **Write-back**: 캐시에 먼저 쓰고 DB 반영은 배치로 미룬다. 쓰기는 가장 빠르지만, 캐시가 죽으면 아직 DB에 반영되지 않은 데이터가 **유실**될 수 있어 손실 허용도가 낮은 데이터엔 부적합하다.

### Stampede가 발생하는 조건과 방지 (수치)
- 인기 상품 key의 TTL을 모두 300초로 동일하게 설정하면, 300초마다 같은 순간에 대량의 요청이 동시에 miss가 되어 DB로 몰린다 — 이것이 stampede다. 초당 5만 QPS 트래픽에서 만료 순간에 수천 건이 한꺼번에 DB를 때리면 순간적으로 DB가 과부하에 빠질 수 있다.
- **방지책**: TTL에 ±10~20% jitter(무작위 편차)를 주어 만료 시점을 분산시키거나, single-flight lock으로 같은 key의 동시 miss 요청 중 1건만 DB를 조회하고 나머지는 그 결과를 기다리게 한다.

### 비유와 흔한 오해
- **비유**: 식당에서 자주 나가는 반찬을 주방 냉장고 깊숙이 두지 않고 조리대 앞에 미리 꺼내 두는 것과 같다 — 손님이 몰려도 매번 냉장고까지 갈 필요가 없다.
- **오해 1**: 캐시는 데이터의 원본이 아니다. 캐시가 사라져도 DB에 원본이 남아 있어야 하며, 캐시만 믿고 DB write를 생략하면 안 된다.
- **오해 2**: 캐시를 도입하면 무조건 안전하다는 착각이 위험하다. 캐시 서버 자체가 장애 나면(예: Redis 다운) 모든 요청이 한꺼번에 DB로 쏟아지는 "캐시 장애 = DB 장애 전이" 상황이 생길 수 있어, timeout·circuit breaker 같은 DB 보호 장치가 함께 필요하다.

## 연결 개념
- 지역성(Locality) — 캐시가 성립하는 이론적 근거(CPU 캐시와 동일 원리)
- TTL·Eviction — 캐시 정합성과 메모리 사용량을 조절하는 두 축
- Cache Stampede·Single-flight — 동시 miss로 인한 DB 과부하와 그 방지책
- 데이터베이스 복제(113) — 캐시로도 못 줄인 나머지 부하를 replica로 분산하는 보완 기법

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 캐시 계층 답안은 hit ratio만 쓰지 말고, 패턴·TTL·stampede·정합성·장애 시 DB 보호까지 포함해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 캐시 계층은 반복 조회 데이터를 Redis·Memcached 등 메모리 저장소에 저장해 원본 DB 접근을 줄이는 구조이다.
> 2. **가치**: cache hit ratio 80~95% 구간에서 p95 지연과 DB read QPS를 동시에 낮춘다.
> 3. **판단 포인트**: cache-aside/write-through/write-back 선택, TTL, 무효화, stampede 방지, 일관성 허용 범위를 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 캐시 아키텍처 설계 역량 확인 | Redis/Memcached, cache-aside, write-through, write-back | 캐시를 DB 대체 저장소로 설명 |
| 정합성·장애 리스크 이해 확인 | TTL, invalidation, stampede, stale data | hit ratio만 제시하고 무효화 전략 누락 |
| 운영 지표 기반 판단 확인 | hit ratio, evictions, miss QPS, p95 latency | 장애 시 DB 과부하 보호 대책 누락 |

> 요약: 이 문제는 캐시 도입 효과보다 캐시 miss와 정합성 리스크를 통제하는 설계가 핵심이다.

---

## Ⅰ. 개요 및 필요성

- 개요: 캐시 계층은 반복 조회용 메모리 저장소이다.
- 배경: DB 반복 조회, 외부 API 호출, 세션 조회가 증가하면 원본 시스템의 read QPS와 p95 지연이 커진다.
- 필요성: Redis·Memcached, TTL, invalidation, cache-aside, stampede 방지로 hit ratio와 miss QPS를 관리해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> Application
  / Cache hit -> Redis/Memcached -> Response
  / Cache miss -> DB/API -> Cache set -> Response
Invalidation Event -> Cache delete/update
Metrics -> hit ratio / evictions / latency
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Redis | 캐시·세션·분산락 저장 | TTL, 자료구조, replication 지원 |
| Memcached | 단순 key-value 캐시 | 멀티스레드, 단순 객체 캐시에 적합 |
| 캐시 키 | 데이터 식별자 | 버전, tenant, locale 포함 필요 |
| TTL | 만료 시간 | 최신성 요구와 부하 절감 사이 조정 |
| 무효화 이벤트 | 변경 시 캐시 제거 | DB commit 이후 outbox/event 사용 |

> 요약: 캐시 계층은 애플리케이션, 캐시 저장소, 원본 DB, 무효화 이벤트, 관측 지표가 함께 동작한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Request -> cache get
  / hit -> cached value 반환
  / miss -> DB read -> cache set with TTL -> 반환
Write 발생 -> DB commit -> cache invalidate/update
Stampede 감지 -> lock/single-flight -> DB 보호
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | key 설계 후 cache get 수행 | key collision 0건 |
| 2 | hit 시 캐시 값 반환 | hit ratio 80% 이상 |
| 3 | miss 시 DB 조회 후 TTL과 함께 저장 | miss QPS와 DB CPU |
| 4 | 데이터 변경 시 delete 또는 update 수행 | stale read 비율 |
| 5 | 동시 miss 시 lock, jitter, pre-warm 적용 | stampede 발생 건수 |

> 요약: 캐시는 hit 경로보다 miss·write·동시 만료 경로를 설계해야 장애 시 DB 부하를 통제할 수 있다.

---

## Ⅳ. 특징

| 구분 | DB 직접 조회 | 캐시 계층 적용 | 수치·판단 기준 |
|:---|:---|:---|:---|
| 지연 | 디스크·네트워크 포함 | 메모리 조회 중심 | Redis p95 1~5ms |
| DB 부하 | 반복 read 집중 | hit 만큼 read 감소 | hit ratio 80~95% |
| 정합성 | 원본 기준 | TTL 동안 stale 가능 | 허용 지연 5초/300초 구분 |
| 장애 | DB만 보호 대상 | 캐시 장애·miss 폭증 추가 | circuit breaker 필요 |

> 요약: 캐시는 읽기 지연과 DB 부하를 낮추지만, TTL 동안 stale data와 miss 폭증을 운영 리스크로 관리해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 패턴 | DB 직접 조회 | cache-aside | 읽기 많고 stale 허용 |
| 쓰기 | DB만 갱신 | write-through | 쓰기 후 즉시 캐시 반영 필요 |
| 내구성 | 원본 DB | write-back | 손실 허용 낮으면 부적합 |
| 제품 | Memcached | Redis | 자료구조·TTL·replication 필요 시 Redis |
| 대안 | CDN | Application cache | 개인화·DB 결과 캐시 |

> 요약: 읽기 중심 서비스는 cache-aside, 강한 쓰기 반영이 필요한 서비스는 write-through를 검토한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Stampede | 동일 TTL 동시 만료 | TTL jitter, single-flight, request coalescing | 동시 miss 수 |
| Stale data | 무효화 누락 | DB commit 후 event delete, versioned key | stale read 비율 |
| Eviction 폭증 | 메모리 부족 | maxmemory 정책, hot key 분리 | evicted_keys |

> 요약: 캐시 리스크는 동시 miss, stale data, eviction, hot key이며 key 단위 지표로 조기 탐지한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Hit ratio | 80~95% | Redis INFO, APM tag |
| 지연 | cache p95 5ms 이하 | client latency histogram |
| DB 보호 | cache 장애 시 DB CPU 70% 이하 | fault injection |
| 정합성 | stale read 허용 SLA 내 | synthetic check, version compare |

> 요약: 캐시 도입 평가는 hit ratio, p95 지연, 장애 시 DB CPU, eviction, stale read 지표를 함께 본다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 조회 캐시: 상품·설정·권한 조회는 cache-aside, TTL 60~300초, key versioning으로 무효화 범위를 통제함
2. Stampede 방지: TTL jitter 10~20%, single-flight lock, hot key pre-warm으로 동시 만료 시 DB QPS 급증을 차단함
3. 장애 대응: cache timeout 20ms, circuit breaker, fallback 응답, DB rate limit을 설정해 캐시 장애가 DB 장애로 번지지 않게 함

**결론 (2줄):**
- 기술사 판단: 읽기 반복률이 높고 stale 허용 시간이 명확하면 캐시 계층을 적용하고, 금융 원장처럼 즉시 정합성이 필요한 데이터는 캐시 범위를 제한함
- 향후 방향: Redis Cluster, client-side caching, CDC 기반 무효화로 대규모 캐시 정합성 통제가 정교해지는 방향임

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "캐시 계층을 설명하시오", "기술하시오" | hit/miss, TTL, 무효화 흐름 | DB 직접 조회 대비 지연·정합성 차이 |
| 요구사항 명시형 | "장애 방안을 제시하시오", "설계하시오" | stampede, fallback, write 정책 | hit ratio·stale read·eviction 대응 |

> 요약: 설명형은 캐시 패턴을 넓게, 설계형은 TTL·무효화·장애 보호를 중심으로 답안을 구성한다.
