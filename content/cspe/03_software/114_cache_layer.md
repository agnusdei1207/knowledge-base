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
- **개요**: 자주 읽는 데이터를 DB보다 가까운 메모리 저장소에 두는 계층
- **왜 필요한가**: 동일 상품·세션·설정 조회가 반복되면 DB CPU와 IOPS가 낭비된다. Redis·Memcached 같은 메모리 캐시는 p95 조회 지연을 ms 단위로 줄이고 DB 부하를 낮춘다.
- **핵심 직관**: 자주 쓰는 도구를 창고가 아니라 책상 위에 올려두는 방식이다.

## 깊이 이해
- **배경·문제의식**: 트래픽 피크 시간에 인기 상품 상세 조회가 초당 5만 건 발생하면 DB가 같은 행을 반복 읽는다. 캐시는 자주 읽는 결과를 key-value로 저장해 반복 조회를 흡수한다.
- **작동 원리**: cache-aside는 애플리케이션이 먼저 캐시를 조회하고 miss 시 DB를 읽은 뒤 캐시에 저장한다. write-through는 쓰기 시 캐시와 저장소를 같이 갱신하고, write-back은 캐시에 먼저 쓰고 나중에 저장소에 반영한다.
- **비유**: 식당에서 자주 나가는 반찬을 주방 깊숙한 냉장고가 아니라 앞 조리대에 준비해 두는 것과 같다.
- **구체 예시**: 상품 상세 API에서 Redis TTL 300초, cache hit ratio 90%를 달성하면 DB read QPS 50,000 중 45,000을 캐시가 흡수한다.
- **흔한 오해·주의점**: 캐시는 데이터 원본이 아니다. TTL, 무효화, stampede 방지, 장애 시 DB 보호 회로가 없으면 장애가 확대된다.

## 연결 개념
- Redis — 자료구조·TTL·pub/sub·replication을 제공하는 인메모리 저장소
- Memcached — 단순 key-value 캐시에 적합한 메모리 캐시
- Cache stampede — 다수 요청이 동시에 miss 후 DB로 몰리는 현상
- TTL·무효화 — 캐시 정합성과 부하를 조절하는 수단

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
