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
- **개요**: 메모리에 key-value와 다양한 자료구조를 저장하는 저지연 데이터 저장소
- **왜 필요한가**: DB 조회가 반복되거나 세션·랭킹·락처럼 밀리초 이하 응답이 필요한 기능은 디스크 중심 DB만으로 p95 지연 목표를 맞추기 어렵다. Redis는 메모리 접근과 단순 명령 처리로 캐시·세션·큐 역할을 담당한다.
- **핵심 직관**: 창고까지 매번 가지 않고 계산대 옆 선반에 자주 쓰는 물건을 올려두는 구조임

## 깊이 이해
- **배경·문제의식**: 관계형 DB는 트랜잭션과 영속성을 제공하지만 모든 읽기를 원장 DB가 처리하면 병목이 된다. Redis는 String, Hash, List, Set, Sorted Set, Stream 같은 자료구조를 메모리에서 처리한다.
- **작동 원리**: 클라이언트 명령을 이벤트 루프가 처리하고 메모리 데이터 구조에 접근한다. 영속성은 RDB 스냅샷과 AOF 로그로 보완하며, Sentinel 또는 Cluster로 장애조치와 분산을 구성한다.
- **비유**: 시험 답안에 자주 쓰는 공식은 책장이 아니라 책상 위 메모지에 두어 바로 보는 방식임
- **구체 예시**: 상품 상세 API에서 인기 상품 10,000건을 Redis 캐시에 TTL 300초로 저장하면 원장 DB 반복 조회를 줄이고 p95 응답 50ms 목표를 맞출 수 있음
- **흔한 오해·주의점**: Redis는 캐시만이 아니다. 다만 메모리 용량, eviction 정책, persistence 설정을 잘못 잡으면 데이터 손실 또는 원장 DB 부하 폭증이 발생한다.

## 연결 개념
- 캐시 계층(Cache Layer) - 읽기 부하 흡수 구조
- TTL·Eviction - 메모리 한계 통제 정책
- 분산 락 - 원자 명령과 만료 시간을 이용한 동시성 제어

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

Redis는 메모리 기반 데이터 저장소이다. 세션, 캐시, 랭킹, 분산 락처럼 짧은 지연시간과 높은 요청량이 필요한 영역에서 원장 DB만으로는 병목이 발생한다. Redis는 메모리 자료구조와 TTL 정책으로 반복 조회와 임시 상태를 처리한다.

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
