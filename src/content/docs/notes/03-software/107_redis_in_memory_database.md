---
sidebar:
  order: 107
  label: "107. Redis 인메모리 데이터베이스"
  badge:
    text: "기출 · 50%"
    variant: note
title: "Redis 인메모리 데이터베이스 (Redis In-Memory Database)"
date: "2026-08-31T10:48:00+09:00"
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

<details><summary>용어 설명</summary>

- **Redis(Remote Dictionary Server)**: 모든 데이터를 RAM에 상주시켜 서브밀리초 단위 응답을 제공하는 고성능 인메모리 Key-Value 데이터베이스.
- **RDB & AOF**: 메모리 스냅샷을 주기적으로 덤프하는 RDB와 모든 쓰기 명령어를 순차 기록하는 AOF(Append-Only File) 영속성 기술.

</details>

- 정의/개념: 초저지연 처리를 위해 **모든 데이터를 RAM에 상주시키고 다양한 자료구조와 영속성(RDB/AOF)을 제공**하는 고성능 인메모리 Key-Value 데이터베이스
- 배경/필요성: 디스크 기반 데이터베이스의 기계적 I/O 지연으로 인해 실시간 고성능 웹 서비스의 세션 관리, 실시간 랭킹 산정, 분산 락 제어 및 고빈도 캐싱 요구를 충족하기 어려운 한계를 극복하고, 모든 데이터를 메인 메모리(RAM)에 상주시켜 1ms 미만의 서브밀리초(Sub-millisecond) 초저지연 응답을 제공하며 단일 스레드 기반의 다양한 자료구조(ZSet, Hash, Stream)와 디스크 영속성(RDB/AOF)을 지원하는 Redis를 도입하여 **백엔드 RDBMS의 부하를 원천 차단하고 시스템 처리량을 극대화**할 필요

#### 한줄 요약
- Redis는 지연을 메모리 용량과 맞바꾼 저장소이므로, 데이터가 RAM 한도를 넘는 순간 축출 정책은 성능 조정 항목이 아니라 어떤 데이터를 잃을지의 문제로 성격이 바뀐다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Single-Threaded Event Loop**: 멀티스레드 락(Lock) 경합과 컨텍스트 스위칭 오버헤드 없이, 비동기 이벤트 루프로 명령어를 원자적(Atomic)으로 순차 처리.
- **ZSet(Sorted Set)**: 스킵리스트(SkipList)와 해시 테이블을 결합하여 점수(Score) 기반으로 정렬된 상태를 유지하는 고성능 자료구조.

</details>

- 메인 메모리(RAM) 기반 **1ms 미만의 초저지연 응답 속도(Sub-millisecond Latency)**
- Strings, Hashes, Lists, Sets, Sorted Sets(ZSet) 등 **풍부한 내장 자료구조 원자적 지원**
- RDB 스냅샷 및 AOF 변경 로그를 통한 **인메모리 데이터의 디스크 영속성(Persistence) 보장**

#### 한줄 요약
- 단일 스레드 비동기 루프로 동시성 락 경합 없이 초고속 원자적 연산을 수행한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Redis 4대 핵심 컴포넌트**: Single-Thread Event Loop(엔진), Data Structures(RAM 저장소), RDB/AOF(영속성), Eviction Manager(메모리 만료 관리).

</details>

```text
[Redis 인메모리 엔진 및 클러스터 아키텍처]
|-- 클라이언트 요청 (epoll / kqueue 기반 논블로킹 I/O 멀티플렉싱)
`-- Redis Core Engine (단일 스레드 비동기 이벤트 루프)
    |-- 인메모리 자료구조 (Strings, Hashes, Lists, Sets, ZSets, Bitmaps, HyperLogLog)
    |-- 만료 및 축출 관리자 (TTL Expire 타이머 + Maxmemory LRU/LFU 정책)
    |-- 영속성 서브시스템 (RDB bgsave 백그라운드 포크 + AOF appendfsync 쓰기)
    `-- 분산 클러스터링 (Redis Sentinel 자동 페일오버 + Redis Cluster 16384 슬롯 샤딩)
```

선의 의미: 계층 및 단일 스레드 이벤트 루프가 메모리 자료구조, 영속성, 만료 관리를 총괄하는 구조

| 구성요소 | 책임 |
|:---|:---|
| 이벤트 루프 | 명령의 **원자적 순차 실행** |
| 인메모리 자료구조 | RAM 기반 **자료형 저장·연산** |
| 영속성 엔진 | **RDB 스냅샷·AOF 기록** |
| 만료 관리자 | TTL·LRU·LFU 기반 **키 회수** |

#### 한줄 요약
- 단일 스레드 이벤트 루프가 명령을 직렬로 처리하기에 잠금 없이 원자성이 성립하지만, 그 대가로 무거운 명령 하나가 나머지 모든 요청을 그대로 멈춰 세운다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Maxmemory Eviction 파이프라인**: 새 키 쓰기 요청 시 메모리 한도를 검사하고, 초과 시 LRU/LFU 알고리즘으로 과거 키를 제거한 후 메모리를 할당하는 절차.

</details>

```text
클라이언트 쓰기 명령 접수 (`ZADD leaderboard 100 "user1"`)
        │
   [메모리 검사] 현재 RAM 사용량이 설정된 `maxmemory` 임계치를 초과했는가?
   ┌────┴───────────────────────────┐
  예 (메모리 포화 상태)             아니오 (메모리 여유 있음)
   │                                 │
[Eviction 실행]                   [메모리 즉시 할당]
설정된 정책(`volatile-lru`)으로   RAM 상의 SkipList에 노드 추가
오래된 키를 즉시 축출(Evict)     │
        │                            │
   인메모리 ZSet 자료구조 갱신 완료 ($O(\log N)$)
        │
   AOF 버퍼에 명령어 추가 기록 및 클라이언트에 0.3ms 성공 응답 반환
```

#### 한줄 요약
- 축출이 요청 처리 경로 안에서 일어나므로 지연은 데이터량이 아니라 메모리 한도 근접 여부에서 튀어 오르고, AOF 기록 주기를 늦출수록 응답은 빨라지지만 장애 시 잃는 구간이 그만큼 길어진다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Redis vs Memcached**: 다채로운 자료구조와 영속성을 지원하는 Redis와 단순 Key-Value 멀티스레드 정적 캐시인 Memcached.

</details>

| 비교 항목 | Redis (Remote Dictionary Server) | Memcached (정적 캐시 엔진) |
|:---|:---|:---|
| 지원 자료구조 | **Strings, Hashes, Lists, Sets, ZSets, Stream** | **단순 String (Key-Value)만 지원** |
| 스레드 모델 | **단일 스레드 이벤트 루프 (Atomic 보장)** | **멀티스레드 모델 (멀티코어 CPU 활용)** |
| 영속성 (Persistence)| **지원 (RDB 스냅샷 + AOF 로그)** | **미지원 (서버 재부팅 시 데이터 전멸)** |
| 복제 및 클러스터 | **Redis Sentinel (HA), Redis Cluster (샤딩)** | 자체 미지원 (클라이언트 라이브러리 샤딩) |

#### 한줄 요약
- 복합 자료형 연산과 영속성이 필요하면 Redis, 단순 정적 캐싱에는 Memcached를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Cache Stampede**: 특정 인기 캐시 키가 만료되는 순간 수많은 동시 요청이 백엔드 DB로 일제히 몰려 DB가 다운되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| `KEYS *` 실행으로 인한 단일 스레드 전체 서버 락업(Lockup) | **운영 환경 `KEYS` 명령어 비활성화 및 `SCAN` 커서 명령 대체** | 무중단 커서 순회 처리 보장 |
| 대량 캐시 TTL 동시 만료로 DB 다운 (**Cache Stampede**) | **TTL에 랜덤 지터(Random Jitter: $\pm 10\%$) 추가 및 Redlock 선점**| 백엔드 DB 과부하 원천 방지 |
| 수십만 개 원소를 가진 Big Key로 인한 메모리/지연 병목 | **해시 태그 기반 키 분할(Sharding) 및 `MEMORY USAGE` 모니터링** | 메모리 접근 및 직렬화 병목 해소 |
| Master 다운 시 데이터 유실 | **Redis Sentinel 자동 페일오버 및 `appendfsync everysec` 설정** | RPO 1초 이내 고가용성 달성 |

#### 한줄 요약
- SCAN 대체, TTL 지터 부여, Big Key 분할, Sentinel 페일오버로 안전하게 운용한다.

## Ⅶ. 결론

- 현대 분산 시스템 및 클라우드 애플리케이션의 **표준 인메모리 캐시 및 데이터 구조 서버**로 확립되었으며, 실무 운영 시에는 **단일 스레드 락업을 방지하는 `KEYS *` 금지 및 `SCAN` 커서 순회 원칙 준수, Cache Stampede를 방어하는 TTL 랜덤 지터(Random Jitter) 부여, 데이터 안전성을 위한 AOF `everysec` 및 Redis Sentinel 기반 자동 페일오버, Redis Cluster 수평 샤딩**을 결합하여 고성능과 무중단 영속성을 동시 보증

#### 한줄 요약
- Redis는 단일 스레드 기반 인메모리 자료구조와 RDB/AOF 영속성을 활용하여 서브밀리초 응답 속도를 완성하는 핵심 인메모리 데이터 플랫폼이다.
