---
sidebar:
  order: 180
  label: "180. 캐싱 전략: Cache-Aside•Write-Through"
  badge:
    text: "미출 · 70%"
    variant: note
title: "캐싱 전략: Cache-Aside•Write-Through (Caching Strategy)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 180
extra:
  question_no: "180"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "무효화•동시 미스•원본 보호의 설계 가치"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Caching Strategy(캐싱 전략)**: 데이터베이스의 I/O 병목을 줄이고 초저지연 읽기를 실현하기 위해 메모리(Redis)에 데이터를 적재, 조회, 갱신하는 패턴.
- **Cache-Aside vs Write-Through**: 애플리케이션이 캐시 확인 후 DB를 조회하는 지연 적재(Cache-Aside)와 쓰기 시 캐시와 DB를 동기 갱신하는 방식(Write-Through).

</details>

- 정의/개념: 데이터베이스의 I/O 병목을 줄이고 응답 속도를 높이기 위해 **고속 인메모리 저장소에 데이터를 적재, 조회, 무효화하는 아키텍처 전략**
- 배경/필요성: 트래픽 급증 시 데이터베이스 직접 조회로 인한 **디스크 I/O 병목, 커넥션 풀 고갈 및 서비스 응답 지연 해결 불가**

#### 한줄 요약
- 인메모리 캐시를 활용하여 데이터베이스 부하를 90% 이상 절감하고 마이크로초 단위 응답을 달성한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Lazy Loading**: 클라이언트가 요청한 데이터만 선별적으로 캐시에 적재하여 메모리 낭비를 방지하는 지연 로딩 방식.
- **Cache Invalidation**: 데이터베이스가 업데이트되었을 때 캐시에 남아있는 과거 데이터(Stale Data)를 즉시 삭제/갱신하는 작업.

</details>

- 요청된 데이터만 메모리에 적재하여 공간 효율성을 극대화하는 **지연 적재(Lazy Loading)**
- 캐시와 원본 DB의 데이터 불일치를 방지하기 위한 **적절한 TTL 및 무효화(Invalidation)**
- 캐시 장애 시에도 데이터베이스로 장애가 전파되지 않도록 보호하는 **서킷 브레이커 방어**

#### 한줄 요약
- 지연 적재, TTL 기반 무효화, 원본 DB 보호를 통해 성능과 정합성의 균형을 유지한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **캐싱 계층 4대 요소**: Cache Store(Redis), Origin Database(RDBMS), Invalidation Engine(무효화), Eviction Policy(LRU/LFU 메모리 관리).

</details>

```text
[캐싱 전략 아키텍처 및 데이터 흐름 구조]
|-- 1. Client Read / Write Requests
`-- 2. Application Layer (캐싱 제어 로직)
    |-- Cache-Aside Pattern: [Cache Get] -> [Hit 시 반환] / [Miss 시 DB 조회 후 Cache Put]
    `-- Write-Through Pattern: [App] -> [Cache & DB 동시 동기 갱신]
`-- 3. In-Memory Cache Layer (Redis Cluster / Memcached)
    |-- Key-Value Store (TTL 기반 자동 만료, LRU 메모리 축출 정책)
    `-- Mutex Lock (Cache Stampede 방어용 분산 락)
`-- 4. Origin Database Layer (Source of Truth: RDBMS / NoSQL)
```

선의 의미: 계층 및 애플리케이션이 캐시와 원본 DB 간의 조회와 갱신 경로를 전략에 따라 제어하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **캐시 저장소 (Cache Store)**| Key별 **고속 사본과 TTL을 메모리에 보관하여 초저지연 읽기 제공** | Redis, Memcached |
| **원본 저장소 (Origin DB)** | 권위 있는 **단일 진실 공급원(Source of Truth) 및 영속 데이터 보존** | RDBMS (MySQL/PG) |
| **축출 정책 (Eviction)** | 메모리 부족 시 **LRU(최근 미사용) 또는 LFU(빈도 기반) 기준 데이터 삭제** | 메모리 상한 제어 |
| **무효화 계층 (Invalidation)**| 원본 변경 시 **캐시 키를 삭제하거나 TTL 만료를 통해 데이터 최신성 유지** | 정합성 보장 |

#### 한줄 요약
- 캐시 저장소, 원본 DB, 축출 정책, 무효화 계층이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Cache-Aside 읽기 및 쓰기 5단계**: 캐시 조회 $\to$ Hit 시 즉시 반환 $\to$ Miss 시 DB 조회 $\to$ 캐시 적재(TTL) $\to$ 쓰기 시 원본 갱신 및 캐시 무효화.

</details>

```text
클라이언트의 데이터 조회 요청
        │
   1. [캐시 키 조회] 애플리케이션이 Redis에서 `user:100` 키의 데이터 조회
   ┌────┴───────────────────────────┐
  Cache Hit                         Cache Miss
   │                                 │
2A. [즉시 반환]                     2B. [원본 DB 조회]
   Redis에서 1ms 만에 데이터 회신       RDBMS에서 무거운 디스크 쿼리 실행
   │                                 │
   │                                3. [캐시 적재]
   │                                   조회된 결과를 TTL(예: 300초)과 함께 Redis에 저장
   │                                 │
   └────┬────────────────────────────┘
        ▼
   4. 클라이언트에 최종 데이터 반환
        │
   5. [데이터 수정 발생 시] DB에 신규 데이터를 쓰고, Redis의 기존 캐시 키를 즉시 삭제(Invalidation)
```

#### 한줄 요약
- 캐시 조회 → Hit 반환/Miss DB 조회 → 캐시 적재 → 결과 반환 → 수정 시 캐시 삭제 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **4대 캐싱 전략 패턴**: Cache-Aside(지연 로딩), Write-Through(동기 동시 쓰기), Write-Behind(비동기 지연 쓰기), Read-Through(캐시 대리 읽기).

</details>

| 비교 항목 | Cache-Aside (Look-Aside) | Write-Through | Write-Behind (Write-Back) |
|:---|:---|:---|:---|
| 데이터 적재 시점 | **실제 읽기 요청 발생 시 (Lazy Loading)**| **쓰기 요청 발생 즉시 (동기 적재)** | **쓰기 요청 발생 즉시 (캐시만 쓰기)** |
| 쓰기 경로 및 지연 | DB 직접 갱신 후 캐시 삭제 | **캐시와 DB를 동시에 동기 쓰기 (지연 증가)**| **캐시에만 쓰고 비동기 벌크 DB 반영 (최고속)**|
| 데이터 정합성 | TTL 만료 전 일시적 불일치 가능 | **항상 캐시와 DB가 100% 일치** | 캐시 서버 다운 시 데이터 유실 위험 |
| 최적 적용 사례 | **대부분의 읽기 중심 일반 서비스** | **금융 잔액, 실시간 주문 재고** | **로그 수집, 게임 실시간 랭킹 포인트** |

#### 한줄 요약
- 일반적 읽기 중심은 Cache-Aside, 정합성 필수 구간은 Write-Through, 초고속 대량 쓰기는 Write-Behind를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Cache Stampede (Thundering Herd)**: 핫한 키의 TTL이 만료된 순간 수만 개의 동시 요청이 전부 캐시 미스를 내고 DB로 몰려 DB가 다운되는 장애.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 인기 키 만료 시 수만 개 동시 요청의 DB 폭주 (Cache Stampede) | **분산 락(Mutex) 또는 PER(Probabilistic Early Recomputation) 적용** | 단 1개 요청만 DB 조회 후 갱신 |
| DB에 없는 악성 키 무한 조회로 DB 부하 유발 (Cache Penetration) | **`null` 결과도 30초 짧은 TTL로 저장 (Negative Caching) 및 Bloom Filter**| DB 악성 쿼리 100% 차단 |
| 수백만 개 캐시가 특정 시간에 일제히 만료 (TTL Avalanche) | **기본 TTL(300초)에 $\pm 10\%$의 무작위 난수(Jitter) 부여** | 만료 시점 균등 분산 |
| 캐시 클러스터 전면 다운 시 DB 연쇄 다운타임 | **Resilience4j 서킷 브레이커 도입 및 정적 폴백 응답 반환** | DB 다운타임 연쇄 전파 차단 |

#### 한줄 요약
- 분산 락(PER), 부정 캐싱, TTL Jitter 난수 분산, 서킷 브레이커로 캐시 장애를 방어한다.

## Ⅶ. 결론

- 대규모 분산 시스템의 읽기 성능을 극대화하고 데이터베이스를 보호하기 위해 **일반 서비스는 Cache-Aside와 Invalidation 패턴을 표준 도입하고, Cache Stampede 방어용 PER 알고리즘 및 TTL Jitter 정책을 필수 적용**하여 고성능 엔터프라이즈 캐싱 아키텍처 완성

#### 한줄 요약
- 캐싱 전략은 Cache-Aside, Write-Through 등의 패턴과 정밀한 무효화 및 Stampede 방어를 결합하여 데이터베이스 부하를 최소화하고 초저지연 성능을 달성하는 핵심 아키텍처 기술이다.