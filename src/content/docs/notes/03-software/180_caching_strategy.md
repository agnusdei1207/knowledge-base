---
sidebar:
  order: 180
  label: "180. 캐싱 전략: Cache-Aside•Write-Through (Caching Strategy)"
  badge:
    text: "미출 • 70%"
    variant: note
title: "캐싱 전략: Cache-Aside•Write-Through (Caching Strategy)"
date: "2026-08-10T10:00:00+09:00"
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

<details><summary>핵심 용어</summary>

- **Cache (캐시)**: 데이터베이스(DB) 조회의 지연(Latency)을 줄이고 부하를 분산시키기 위해, 자주 사용되는 데이터를 메모리(Redis, Memcached)에 임시 저장하는 고속 데이터 계층.
- **Cache-Aside (캐시 어사이드 / Look-Aside)**: 데이터를 읽을 때 항상 캐시를 먼저 확인하고, 없으면 DB에서 읽어온 후 캐시에 밀어넣는 가장 보편적이고 안전한 지연 적재(Lazy Loading) 전략.
- **Write-Through (라이트 스루)**: 데이터를 쓸 때 무조건 캐시와 DB 양쪽에 동시에 업데이트하여, 캐시의 데이터가 항상 DB와 100% 동일한 최신 상태를 유지하도록 강제하는 동기 쓰기 전략.

</details>

- 정의/개념: 애플리케이션과 원본 데이터베이스 사이에서 읽기/쓰기 성능을 극대화하고 데이터 정합성을 유지하기 위해 사본(Cache)의 적재와 만료 시점을 제어하는 **캐싱 아키텍처 패턴**
- 배경/필요성: 디스크 기반의 RDBMS는 트래픽 스파이크 시 I/O 병목이 발생하므로, 마이크로초($\mu s$) 수준의 응답 속도를 제공하는 인메모리 캐시 계층을 도입하여 전체 시스템 처리량(Throughput)을 방어하기 위한 필수 기법

#### 한줄 요약

- 가까운 사본을 누가 채우고 언제 버리며 원본 변경 뒤 어떻게 맞출지 정해야 빠른 조회가 오래된 답으로 바뀌지 않는다.

## Ⅱ. 특징 (캐싱 전략별 데이터 정합성 유지 기법)

<details><summary>핵심 용어</summary>

- **Cache Invalidation (캐시 무효화)**: DB의 데이터가 변경(Update/Delete)되었을 때, 캐시에 남아있는 과거 데이터(Stale Data)를 강제로 지워버리는 작업. Cache-Aside의 핵심 쓰기 패턴.

</details>

- **Lazy Loading (지연 로딩)**: (Cache-Aside) 클라이언트가 요청한 데이터만 캐시에 적재하므로, 안 쓰는 데이터가 캐시 메모리를 낭비하지 않는 공간 효율성 확보.
- **Stale Data Risk (구버전 노출 위험)**: (Cache-Aside) 캐시에 들어간 데이터는 DB가 바뀌어도 TTL이 끝날 때까지 갱신되지 않으므로 최신성 위배(Inconsistency) 발생 가능성 내재.
- **Strong Consistency (강한 정합성)**: (Write-Through) 캐시와 DB를 항상 동시에 업데이트하므로 데이터 불일치가 원천 차단되지만, 쓰기(Write) 작업의 지연 시간(Latency)이 2배로 증가하는 트레이드오프.

#### 한줄 요약

- 인기 상품 사본이 동시에 만료돼도 대표 요청 하나만 원본을 읽고 나머지가 결과를 공유하면 데이터베이스 폭주를 막을 수 있다.

## Ⅲ. 구조 및 구성요소 (캐시 시스템 아키텍처)

<details><summary>핵심 용어</summary>

- **TTL (Time To Live)**: 캐시에 저장된 데이터가 유효한 시간(수명). TTL이 만료되면 해당 데이터는 메모리에서 자동 삭제(Eviction)되며, 다음 요청 시 DB에서 새로 조회.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Caching Strategies (Read & Write)                    │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Cache-Aside (Read)                                                  │
│   [App] ──(1.조회)──► [Cache (Miss)]                                   │
│     │◄─(4.응답)──       │                                              │
│     └──(2.조회)──► [Database] ──(3.캐시에 저장(TTL 설정))─► [Cache]    │
│                                                                        │
│ 2. Write-Through (Write)                                               │
│   [App] ──(1.저장)──► [Cache (동기화)] ──(2.동시 저장)──► [Database]   │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Cache-Aside는 애플리케이션(App)이 중심이 되어 캐시와 DB를 직접 오가며 조율하고, Write-Through는 캐시가 앞단에 서서 DB 쓰기까지 동기적으로 밀어내는(Through) 통제 구조.

| 구성요소 | 역할 및 정의 | 실무 적용 예시 |
|:---|:---|:---|
| **Cache Store** | **Key-Value 형태로 고속 메모리 적재** | Redis, Memcached, CDN |
| **Origin (원본 DB)** | **데이터가 영구 보존되는 Source of Truth**| MySQL, Oracle |
| **Eviction Policy** | **메모리가 꽉 찼을 때 삭제할 데이터 선정 기준**| LRU(Least Recently Used), LFU |
| **TTL (만료 시간)** | **캐시의 유효기간 설정 (Stale 방지망)** | `EXPIRE key 3600` (1시간) |

#### 한줄 요약

- 응용이 사본 주소와 정책을 정하고 캐시는 보관하며 무효화 계층이 원본 변경을 알리고 요청 병합이 몰리는 손님을 한 줄로 세운다.

## Ⅳ. 흐름도 (Cache-Aside 및 동기/비동기 쓰기 전략 흐름)

<details><summary>핵심 용어</summary>

- **Write-Behind (Write-Back)**: 모든 데이터를 일단 캐시에만 아주 빠르게 쓰고(응답 완료), 백그라운드 스레드가 모아두었다가 나중에(Asynchronous) 한꺼번에 DB에 벌크로 밀어넣는 고성능 쓰기 전략.

</details>

```text
[Read Strategy: Cache-Aside]
   요청 ──► 캐시 확인 ──(Hit)──► 반환 (완료)
               │
             (Miss)
               ▼
          원본 DB 조회 ──► 캐시에 Write (TTL) ──► 반환 (완료)

[Write Strategy 비교]
 1. Write-Through: [App] ──(Write)──► [Cache] ──(동기 Write)──► [DB] ──(응답)
 2. Write-Around : [App] ──(Write)──► [DB] (캐시는 무시, 무효화만 수행) ──(응답)
 3. Write-Behind : [App] ──(Write)──► [Cache] ──(즉시 응답) 
                                        └────(비동기 Batch)────► [DB]
```

### 동작 원리

1. **읽기 (Read)**: 대부분의 시스템은 Cache-Aside를 사용하여, 히트율이 높은 데이터만 메모리에 유지.
2. **쓰기 (Write)**:
    - 정합성이 절대적이면 **Write-Through** (느림, 안전함).
    - 일반적인 쓰기면 **Write-Around** (DB에만 쓰고 캐시 삭제, 다음 조회 시 채워짐).
    - 쓰기 속도가 최우선이면 **Write-Behind** (매우 빠름, 캐시 죽으면 데이터 날아감 위험).

#### 한줄 요약

- 사본이 없을 때 첫 요청만 원본을 읽고 값과 버전을 저장하면 뒤따른 요청은 같은 결과를 받아 원본 호출을 반복하지 않는다.

## Ⅴ. 종류 및 비교 (캐싱 패턴 1:1 비교 분석)

<details><summary>핵심 용어</summary>

- **Cache Miss (캐시 미스)**: 캐시에 찾는 데이터가 없어 결국 느린 원본 DB까지 다녀와야 하는 상황. 이것이 반복되면 캐시를 도입한 의미가 퇴색됨.

</details>

| 비교 항목 | Cache-Aside (Look-Aside) | Write-Through |
|:---|:---|:---|
| **주요 용도** | **일반적인 읽기 최적화 (가장 많이 씀)** | **읽기/쓰기 모두 중요한 정합성 필수 구간** |
| **캐시 공간 효율** | **실제 요청된 데이터만 적재 (효율 높음)** | **안 읽을 데이터도 무조건 적재 (효율 낮음)** |
| **쓰기 지연 시간** | DB에만 쓰므로 빠름 (또는 캐시 삭제 1회) | **캐시와 DB 모두 써야 하므로 2배로 지연** |
| **구현 난이도** | App에서 코드 라인 증가 (if-else 패턴) | 구조 단순 (DB가 뒷단에 숨겨짐) |

#### 한줄 요약

- 조회 중심은 응용이 필요한 값만 채우고 즉시 원본 반영이 필요하면 동기 쓰기, 지연 반영을 허용하면 비동기 쓰기를 제한적으로 사용한다.

## Ⅵ. 실무 고려사항 및 대책 (분산 캐시 3대 장애 요인 대책)

<details><summary>핵심 용어</summary>

- **Cache Stampede (캐시 스탬피드 / Thundering Herd)**: 매우 핫(Hot)한 데이터의 TTL이 만료된 순간, 수만 개의 동시 요청이 전부 캐시 미스를 내고 동시에 DB로 돌진하여 DB가 즉사하는 대형 장애 현상.

</details>

| 3대 캐시 장애 요인 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Cache Stampede** | 인기 키(Key) 만료 시 DB 동시 조회 폭주 | **요청 병합(Request Collapsing) 및 PER(Probabilistic Early Recomputation)**|
| **2. Cache Penetration**| DB에도 없는 악성 키(Key) 무한 요청 | **DB에 없다는 사실 자체를 캐싱 (부정 캐싱, Negative Caching)** |
| **3. 만료 주기(TTL) 쏠림**| 대량 적재된 캐시들이 일제히 동시 만료됨 | **TTL Jitter (기준 시간에 $±10\%$ 난수 지연 부여로 만료 시간 분산)**|

> 사례: **넷플릭스와 트위터의 레디스(Redis) 클러스터 도입 시 Cache Stampede 방어를 위한 백그라운드 사전 갱신(Warm-up) 아키텍처**

#### 한줄 요약

- 캐시 전체 장애 때 모든 요청이 캐시를 건너뛰어 원본으로 향하지 않도록 호출 상한과 차단기로 원본의 연쇄 장애를 막아야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **캐싱 전략 수립 기준**: 데이터 정합성 요구 수준(강결합 vs 최종 일관성), 읽기/쓰기 비율 패턴(Read-Heavy vs Write-Heavy), 장애 전파 차단(Circuit Breaker)에 의거한 체계.

</details>

- **캐싱 전략 수립 기준**에 따라 대용량 B2C 서비스는 **Cache-Aside + Write-Around (만료) 전략** 필수 채택

#### 한줄 요약

- 조회 중심은 캐시 어사이드로 시작하고 TTL·요청 병합·버전 무효화를 함께 설계해 속도와 원본 보호를 동시에 확보해야 한다.
