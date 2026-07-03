---
title: "Redis 인메모리 DB (Redis In-Memory Database)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 123
---

# 📖 【암기용】 개념 완전 이해

> 목적: Redis 인메모리 DB를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Redis는 데이터를 디스크가 아니라 **메모리(RAM)**에 저장하는 **인메모리 key-value 데이터 저장소**이며, 캐시·세션·큐 같은 저지연 기능의 대표 구현체다.
- **왜 필요한가**: 관계형 DB(RDBMS)는 디스크 I/O 때문에 단일 쿼리에도 수 ms가 걸린다. 같은 조회가 초당 수만 건 반복되면 디스크 DB만으로는 지연시간·처리량 목표를 맞추기 어렵다. Redis는 메모리 접근(수십~수백 마이크로초)과 단순 명령 처리로 이 반복 조회를 흡수한다.
- **핵심 직관**: 자주 찾는 서류를 창고(디스크)까지 매번 가지러 가지 않고, 책상 위 메모지(메모리)에 올려두고 바로 보는 구조다.

## 핵심 용어 정리
| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 인메모리 DB | 전체 데이터를 RAM에 두고 처리하는 DB — Redis가 속하는 상위 분류 | 창고 대신 책상 위에서 바로 작업 |
| key-value 저장소 | 키 하나로 값을 즉시 찾는 자료 모델 | 사물함 번호로 물건 찾기 |
| String/Hash/List/Set/ZSet/Stream | Redis가 제공하는 값 자료구조 — 각기 전용 명령 보유 | 용도별로 다른 서랍 |
| TTL(Time To Live) | 키가 자동 삭제되는 만료 시간(초) | 우유팩의 유통기한 |
| Eviction(LRU/LFU/noeviction) | 메모리가 다 찼을 때 어떤 키를 버릴지 정하는 정책 | 냉장고가 꽉 찼을 때 정리 규칙 |
| 이벤트 루프(단일 스레드) | 명령을 한 번에 하나씩 순서대로 처리하는 실행 모델 | 창구 하나에서 한 명씩 순서대로 응대 |
| RDB(스냅샷) | 특정 시점 전체 메모리 상태를 파일로 통째 저장 | 특정 순간을 찍은 사진 |
| AOF(Append Only File) | 실행된 쓰기 명령을 순서대로 로그에 기록 | 거래를 한 줄씩 적는 가계부 |
| Sentinel | 마스터 장애를 감지하고 레플리카를 새 마스터로 승격시키는 감시 프로세스 | 심판이 다치면 대기 심판을 투입 |
| Cluster / hash slot(16384) | 키를 16384개 슬롯으로 해시 분산해 여러 노드에 나누는 구조 | 우편번호로 배달 구역을 나눔 |
| Cache-aside | 앱이 캐시를 먼저 조회하고 없으면(miss) DB에서 읽어 캐시를 채우는 패턴 | 진열대가 비면 창고에서 채워 넣기 |
| Cache Stampede | 인기 키들이 동시에 만료돼 요청이 한꺼번에 DB로 몰리는 현상 | 폐점 직전 손님이 한 계산대에 몰림 |
| Hot Key | 특정 키에 요청이 쏠려 그 키를 처리하는 노드에 부하가 집중되는 현상 | 한 줄에만 사람이 몰림 |

## 깊이 이해

### 왜 디스크 DB만으로는 부족한가 (수치로 이해)
- SSD 기반 RDBMS의 단일 랜덤 읽기는 인덱스 탐색을 포함해 보통 1~5ms가 걸린다. 초당 요청이 50,000건이면 DB 커넥션 풀과 디스크 I/O 큐가 곧바로 포화한다.
- Redis는 데이터가 이미 메모리에 있어 네트워크 왕복을 빼면 명령 처리 자체는 마이크로초(µs) 단위다. 상품 상세 조회를 Redis 캐시로 흡수해 hit ratio 90%를 달성하면, 원장 DB는 나머지 10%의 요청만 처리하면 된다.

### 단일 스레드 이벤트 루프가 왜 빠른가
- Redis의 명령 처리 스레드는 하나다(코어 확장은 I/O 스레딩·Cluster로 별도 해결). 한 번에 한 명령만 처리하므로 락 경합, 컨텍스트 스위칭, 캐시 미스 비용이 없다 — "한 줄로 서서 한 명씩 받는 창구"가 병렬 잠금 관리보다 오히려 빠른 이유다.
- 대신 O(n) 이상인 무거운 명령(예: 큰 컬렉션에 대한 `KEYS *`, 대량 `SMEMBERS`)을 실행하면 그동안 다른 모든 클라이언트가 대기한다 — 단일 스레드의 대가다.

### 자료구조별 실제 사용 — ZSet으로 랭킹 만들기
- Sorted Set(ZSet)은 멤버마다 score를 붙여 항상 정렬 상태를 유지하는 자료구조다. `ZADD ranking 15000 "userA"`처럼 점수를 넣으면 내부적으로 skip list가 정렬을 O(log n)에 유지한다.
- 실시간 랭킹 TOP 10을 뽑을 때 `ZREVRANGE ranking 0 9`는 이미 정렬된 구조의 앞 10개만 자르면 되므로 비용이 O(log n + 10)이다. RDBMS라면 `ORDER BY score DESC LIMIT 10`으로 조회 시점마다 정렬 비용을 다시 치러야 한다.

### 영속성의 트레이드오프 — RDB vs AOF (수치로 이해)
- RDB를 5분 주기로 스냅샷하면, 장애 시 마지막 스냅샷 이후 최대 5분치 데이터가 사라질 수 있다 — 파일이 작고 복구가 빠른 대신 손실 폭이 크다.
- AOF를 `appendfsync everysec`로 설정하면 1초마다 디스크에 fsync한다. 장애 시 손실은 최대 1초치로 줄지만, 매초 쓰기 때문에 디스크 부하가 RDB보다 크고 로그 파일도 계속 커져 주기적 rewrite(압축)가 필요하다.
- 실무에서는 두 방식을 병행해 "RDB로 빠른 전체 복구 + AOF로 최근 1초 손실만 감수"하는 조합을 쓴다.

### 분산 구성 — Cluster의 16384 슬롯
- Cluster는 키를 `CRC16(key) mod 16384` 연산으로 16384개 슬롯 중 하나에 배정하고, 슬롯을 노드별로 나눠 담당시킨다. 예: 노드 3대면 슬롯을 대략 5461~5462개씩 나눠 갖는다.
- 클라이언트가 엉뚱한 노드에 요청하면 서버가 `MOVED <slot> <주소>`로 정확한 노드를 알려주고 클라이언트가 재요청한다 — 이 리다이렉트 비율이 높다면 클라이언트가 들고 있는 슬롯 지도가 오래됐다는 신호다.

### Cache Stampede를 막는 법 — TTL Jitter (수치로 이해)
- 인기 상품 10,000건을 모두 TTL 300초로 캐시에 넣으면, 300초 후 이 10,000개가 동시에 만료되어 그 순간 DB에 10,000건의 요청이 한꺼번에 몰린다.
- TTL에 ±10~20% 무작위 지터(jitter)를 섞으면(240~360초 사이로 분산) 만료 시점이 흩어져 DB로의 요청이 시간대별로 나뉜다. 여기에 첫 요청만 DB를 읽도록 락을 거는 singleflight 패턴을 결합하면 폭주를 더 줄인다.

## 연결 개념
- 캐시 계층(Cache Layer) — Redis는 캐시 계층의 대표 구현체이며, cache-aside는 그 적용 패턴이다.
- 분산 락 — `SET key value NX PX 5000`처럼 원자적 SETNX와 만료 시간을 결합해 구현한다.
- CAP 정리 — Redis Cluster는 비동기 복제를 쓰므로 파티션 상황에서 최신 쓰기가 유실될 수 있다(일관성보다 가용성 쪽으로 기운 설계).

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Redis 답안은 캐시 명칭이 아니라 자료구조, 영속성, 클러스터, 장애 시 원장 DB 보호까지 써야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Redis는 메모리 기반 key-value 저장소로 다양한 자료구조와 원자 명령을 제공하는 인메모리 DB임.
> 2. **가치**: 캐시 hit ratio 90% 이상, p95 응답 50ms 이하 같은 목표에서 원장 DB 읽기 부하를 분산함.
> 3. **판단 포인트**: TTL, eviction, persistence, cluster slot, cache stampede 방지가 설계 품질을 결정함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 인메모리 DB 구조 이해 확인 | key-value, 자료구조, event loop, RDB/AOF | "메모리라 빠름" 같은 표현으로 끝내지 않음 |
| 캐시 아키텍처 판단 확인 | cache-aside, write-through, TTL, eviction | 캐시 미스 시 원장 DB 부하 폭증 누락 방지 |
| 운영 리스크 확인 | Sentinel, Cluster, persistence, hot key | Redis를 영속 원장 DB로 단정하지 않음 |

> 요약: Redis 문제는 지연시간 감소뿐 아니라 장애와 캐시 무효화까지 연결해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: Redis는 메모리 기반 데이터 저장소이다.
- 배경: 세션, 캐시, 랭킹, 분산 락처럼 짧은 지연시간과 높은 요청량이 필요한 영역에서 원장 DB만으로는 병목이 발생한다.
- 필요성: 메모리 자료구조와 TTL 정책으로 반복 조회와 임시 상태를 처리해 원장 DB 부하를 분리한다.

---

## Ⅱ. 구조 및 구성요소

```text
Application -> Redis Client -> Event Loop -> Data Structures -> Memory
                              +-> RDB/AOF Persistence
                              +-> Sentinel/Cluster
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 자료구조 | String, Hash, Set, ZSet, Stream 처리 | 랭킹·큐·세션 구현 |
| TTL/Eviction | 키 만료와 메모리 회수 | LRU, LFU, noeviction |
| Persistence | RDB 스냅샷, AOF 로그 | 데이터 복구 지점 결정 |
| Cluster/Sentinel | 장애조치와 분산 | hash slot 16384 기반 |

> 요약: Redis는 메모리 자료구조, 만료 정책, 영속성, 클러스터 구성이 함께 동작함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Request -> Key Hash -> Memory Lookup -> TTL Check -> Command Execute -> Reply
Cache Miss -> DB Read -> Redis Set with TTL -> Reply
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 키 해시와 클러스터 슬롯 판단 | MOVED/ASK redirect 비율 |
| 2 | 메모리에서 값 조회와 TTL 확인 | hit ratio, expired keys |
| 3 | 자료구조 명령 원자 처리 | command latency p95 |
| 4 | 필요 시 RDB/AOF 기록 | fsync 정책, AOF rewrite |
| 5 | 미스 시 원장 DB 조회 후 캐시 채움 | miss penalty, DB QPS |

> 요약: Redis는 메모리 조회와 TTL 판정 후 명령을 처리하고, 미스는 원장 DB 보강 흐름으로 연결함.

---

## Ⅳ. 특징

| 구분 | 디스크 DB | Redis | 판단 포인트 |
|:---|:---|:---|:---|
| 저장 위치 | SSD/HDD 중심 | DRAM 중심 | 데이터 크기와 메모리 비용 |
| 자료구조 | 행·문서 중심 | String, Hash, ZSet, Stream | 랭킹·큐·세션 적합성 |
| 영속성 | 트랜잭션 로그 기본 | RDB/AOF 선택 | 허용 데이터 손실 시간 |

> 요약: Redis는 임시·반복·고빈도 데이터에 적합하며, 영속 원장은 RDBMS 또는 로그 저장소로 분리한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | DB 직접 조회 | cache-aside Redis | 동일 키 반복 조회 비율 60% 이상 |
| 비용/성능 | DB read replica 증설 | 메모리 캐시 | 캐시 hit ratio 90% 이상 목표 |
| 운영/위험 | 단일 DB 병목 | hot key, stampede | key 분산·lock·TTL jitter |

> 요약: Redis는 반복 조회와 지연 목표가 명확할 때 원장 DB 앞단에 배치한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Cache Stampede | 동일 키 동시 만료 | TTL jitter, singleflight lock | miss burst QPS |
| Hot Key | 특정 키 요청 집중 | key 분할, local cache | top key QPS 편차 |
| 데이터 손실 | AOF/RDB 정책 부적합 | appendfsync everysec, 복제 확인 | RPO seconds |

> 요약: Redis 리스크는 만료 폭주, 키 집중, 영속성 정책을 기준으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 캐시 | hit ratio 90% 이상 | Redis INFO stats |
| 지연 | command latency p95 5ms 이하 | latency doctor, APM |
| 메모리 | used_memory_peak 80% 이하 | INFO memory, eviction count |

> 요약: Redis 운영 성공은 hit ratio, 명령 지연, 메모리 여유율로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. cache-aside 패턴에 TTL 300초와 TTL jitter 10~20%를 적용해 동시 만료 폭주를 낮춤.
2. 세션·랭킹·락은 Hash·ZSet·SET NX PX처럼 목적별 명령으로 구현하고, 원장 데이터는 DB에 보관함.
3. Cluster hash slot, Sentinel 장애조치, AOF everysec를 업무 RPO 기준에 맞춰 구성함.

**결론 (2줄):**
- 기술사 판단: 반복 조회·임시 상태는 Redis, 강한 트랜잭션 원장은 RDBMS를 선택함.
- 향후 방향: Redis는 캐시를 넘어 스트림 처리, 벡터 검색, 엣지 세션 저장소와 결합되는 추세임.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Redis를 설명하시오" | 명령 처리, TTL, persistence 흐름 | 디스크 DB와 인메모리 DB 비교 |
| 요구사항 명시형 | "캐시 설계 방안을 제시하시오" | cache-aside와 미스 처리 | stampede, hot key, RPO 대응 |

> 요약: 설명형은 자료구조·동작 원리, 방안형은 캐시 장애 패턴과 운영 지표를 중심으로 작성함.
