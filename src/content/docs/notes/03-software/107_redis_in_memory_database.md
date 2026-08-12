---
sidebar:
  order: 107
  label: "107. Redis 인메모리 데이터베이스 (Redis In-Memory Database)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "Redis 인메모리 데이터베이스 (Redis In-Memory Database)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 107
extra:
  question_no: "107"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "137회 기출, 인메모리 자료구조 활용성"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Redis (Remote Dictionary Server)**: 모든 데이터를 메인 메모리(RAM)에 상주시시켜 서브밀리초(Sub-millisecond) 단위의 초고속 응답을 렌더링하는 인메모리 키-값(In-Memory Key-Value) 데이터 구조 저장소.
- **Rich Data Structures**: 단순 String 외에 Hashes, Lists, Sets, Sorted Sets(ZSet), Bitmaps, HyperLogLog, Geospatial 등 풍부한 내장 자료구조(Data Structure)를 원자적(Atomic)으로 제공하는 특성.
- **Single-Threaded Event Loop**: 메인 쿼리 연산을 단일 스레드 비동기 이벤트를 통해 락(Lock) 경합 및 컨텍스트 스위칭 오버헤드 없이 순차 처리하는 커널 아키텍처.

</details>

- **정의**: 모든 데이터를 메인 메모리(`RAM`)에 상주시켜 서브밀리초(`Sub-millisecond`) 단위의 초고속 응답을 제공하는 인메모리 키-값(`In-Memory Key-Value`) 저장소인 **Redis(Remote Dictionary Server)**.
- **필요성**: RDBMS 디스크 I/O 병목 극복, 랭킹 시스템, 세션 관리, Pub/Sub 및 분산 락(`Redlock`) 처리 등 초고속 QPS 대응 요구성.

#### 한줄 요약

- 디스크 창고 대신 메모리 책상에서 다양한 자료형을 바로 계산하는 키값 저장소이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **In-Memory Speed**: RAM 기반 $1\text{ms}$ 이하의 Sub-millisecond 초저지연 성능.
- **Atomic Operations**: 단일 스레드 기반으로 모든 자료구조 명령어가 동시성 충돌 없이 원자적(Atomic)으로 수행.
- **Persistence Support (RDB & AOF)**: 인메모리 휘발성(Volatility) 단점을 극복하기 위해 디스크에 스냅샷(RDB) 및 변경 로그(AOF)를 기록하는 영속성 기능.

</details>

- **고성능 연산**: 단일 스레드 이벤트 루프(`Single-Threaded Event Loop`) 기반의 원자적 연산 보장.
- **자료구조 지원**: `Strings`, `Hashes`, `Lists`, `Sets`, `Sorted Sets` 등 풍부한 내장 자료구조 지원.
- **운영 안정성**: 스냅샷(`RDB`) 및 변경 로그(`AOF`) 기반의 영속성 보장.

#### 한줄 요약

- 빠르지만 메모리 한도와 재시작 복구 및 주 노드 장애를 함께 설계해야 한다.

## Ⅲ. 구조 및 구성요소 (Redis 5대 자료구조 & 영속성 아키텍처)

<details><summary>핵심 용어</summary>

- **Sorted Set (ZSet)**: 각 멤버에 점수(Score)를 부여하여 랭킹 및 순위판(Leaderboard)을 $O(\log N)$으로 유지해 주는 대표 자료구조.
- **RDB vs AOF**: RDB는 특정 시점의 메모리 덤프 파일, AOF는 모든 CUD 명령어를 파일 끝에 덧붙여 기록하는 로그 파일.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Redis Architecture & Persistence                │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ Data Structures   │ In-Memory RAM     │ Disk Persistence               │
├───────────────────┼───────────────────┼────────────────────────────────┤
│ • Strings, Hashes │ • Memory Cache    │ • RDB (Point-in-Time Snapshot) │
│ • Lists, Sets     │ • Single-Thread   │ • AOF (Append Only Log File)   │
│ • Sorted Sets     │   Event Loop      │ (Replication / Cluster HA)     │
└───────────────────┴───────────────────┴────────────────────────────────┘
```

선의 의미: 인메모리 RAM 상의 5대 자료구조를 단일 스레드로 연산하고, RDB/AOF 디스크 백업 및 Cluster 라우팅으로 영속성을 수용하는 구조.

| 자료구조 (Data Structure) | 주요 내부 구조 및 특징 | 실무 활용 도메인 및 유스케이스 |
|:---|:---|:---|
| **String** | 가장 기본 키-값 형태, 최대 512MB | **HTML 캐싱, 세션 저장소, 앰플리튜드 카운터** |
| **Hash** | Field-Value 쌍을 지닌 객체 구조 | **유저 프로필, 객체 데이터 구조 표현** |
| **List** | Linked List 구조, 좌/우 푸시 팝 | **최근 메시지 큐, 타임라인 피드** |
| **Set** | 중복 없는 무순서 집합 | **유저 방문자 수(UV), 교집합/합집합 연산** |
| **Sorted Set (ZSet)** | **Score 기반 자동 정렬 (SkipList)** | **실시간 실시간 검색어, 게임 리더보드 랭킹** |

#### 한줄 요약

- 메모리 서랍과 만료표, 복구 기록, 사본, 슬롯 안내자로 구성된다.

## Ⅳ. 흐름도 (Redis Eviction Policy & Cache Expiration)

<details><summary>핵심 용어</summary>

- **Maxmemory Policy (제거 정책)**: 메모리가 `maxmemory` 한계치에 도달했을 때 키를 삭제하는 정책 (LRU, LFU, Volatile-LRU 등).
- **TTL (Time To Live)**: 키에 만료 시간(Seconds)을 설정하여 자동 소멸시키는 캐시 제어 지표.

</details>

```text
[Client Write Request] ──► [Memory Usage Check vs maxmemory]
                                     │
       ┌─────────────────────────────┴─────────────────────────────┐
       ▼ (Under Limit)                                             ▼ (Over Limit)
[Normal RAM Memory Allocation]             [Eviction Policy (LRU / LFU) 튜플 삭제]
```

### 동작 원리

1. **Memory Allocation**: 데이터 삽입 시 `maxmemory` 설정값 체크.
2. **Eviction Execution**: 메모리가 부족할 경우 설정된 정책(`allkeys-lru`: 가장 오래 사용되지 않은 키 삭제)에 따라 데이터를 쫓아내고(Evict) 메모리 확보 후 쓰기 완료.

#### 한줄 요약

- 키 담당 노드가 메모리 값을 바로 고치고 복구 로그와 사본에 변경을 남긴다.

## Ⅴ. 종류 및 비교 (Redis 대 Memcached)

<details><summary>핵심 용어</summary>

- **Redis vs Memcached**: Redis는 다채로운 자료구조, 영속성, 클러스터링을 지원하는 종합 저장소, Memcached는 단순 String 전용 멀티스레드 정적 캐시.

</details>

| 비교 항목 | Redis (Remote Dictionary Server) | Memcached |
|:---|:---|:---|
| 데이터 구조 | **Strings, Hashes, Lists, Sets, ZSets 등 다채로움**| **단순 String (Key-Value) 전용** |
| 아키텍처 스레드 | **단일 스레드 (Single-Threaded Event Loop)**| **멀티 스레드 (Multi-Threaded)** |
| 영속성 (Persistence)| **지원 (RDB 스냅샷 & AOF 로그)** | **미지원 (메모리 휘발성 100%)** |
| 고가용성 (HA) | **Sentinel (자동 승격) & Redis Cluster** | 독립 노드 운영 (외부 라우팅 필요) |

#### 한줄 요약

- 복구와 계산이 필요하면 Redis, 다시 만들 수 있는 단순 임시 값이면 Memcached를 검토한다.

## Ⅵ. 실무 고려사항 및 대책 (Redis 3대 안티패턴 및 튜닝)

<details><summary>핵심 용어</summary>

- **Cache Stampede (캐시 재앙)**: 대량의 핫키(Hot Key) TTL이 동시에 만료되어 순간적으로 수만 건의 쿼리가 RDBMS로 직접 몰려 DB가 다운되는 현상.
- **O(N) Command Threat**: 단일 스레드 특성상 `KEYS *` 또는 `FLUSHALL` 같은 $O(N)$ 명령을 실행하면 전체 Redis가 먹통(Lockup)이 되는 심각한 위협.

</details>

| 3대 안티패턴 | 발생 원인 및 위험 요소 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. `KEYS *` 명령 실행** | 단일 스레드 블로킹으로 전사 서비스 중단 | **`KEYS` 사용 절대 금지, `SCAN` 명령으로 대체** |
| **2. Cache Stampede** | 핫키 TTL 동시 만료로 DB 폭사 | **TTL에 Random Jitter(가변 오차) 추가 및 Probabilistic Early Expiration** |
| **3. Big Key (거대 키)** | Hash/ZSet 내 10만 개 이상 튜플 축적 | **키 분할 (Key Sharding) 및 주기적 분선** |

> 사례: **카카오 / 쿠팡 Redis Cluster (16384 Hash Slot) 기반 분산 인메모리 캐시 운용**

#### 한줄 요약

- 키가 한꺼번에 사라지거나 하나의 큰 키에 요청이 몰리지 않도록 수명과 크기를 관리한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Redis 수립 기준(Redis Architecture Standards)**: 인메모리 사양, Maxmemory LRU 정책, RDB/AOF 영속성 및 Redis Cluster 구축에 의거한 체계.

</details>

- **Redis 수립 기준 적용** (초고속 세션/캐시/랭킹 시스템 구축 시 `Redis Cluster` 및 `Sentinel HA` 필수 수용)

#### 한줄 요약

- Redis 저장 역할 선택 기준은 값의 재생성 가능성부터 확인한다.
