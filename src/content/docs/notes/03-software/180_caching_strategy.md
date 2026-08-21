---
sidebar:
  order: 180
  label: "180. 캐싱 전략: Cache-Aside•Write-Through (Caching Strategy)"
  badge:
    text: "미출 · 70%"
    variant: note
title: "캐싱 전략: Cache-Aside•Write-Through (Caching Strategy)"
date: "2026-08-14T03:52:00+09:00"
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

- **Cache (캐시)**: 데이터베이스(DB) 조회의 지연(Latency)을 줄이고 부하를 분산시키기 위해, 자주 사용되는 데이터를 메모리(Redis, Memcached)에 임시 저장하는 고속 데이터 계층.
- **Cache-Aside (캐시 어사이드 / Look-Aside)**: 데이터를 읽을 때 항상 캐시를 먼저 확인하고, 없으면 DB에서 읽어온 후 캐시에 밀어넣는 가장 보편적이고 안전한 지연 적재(Lazy Loading) 전략.
- **Write-Through (라이트 스루)**: 데이터를 쓸 때 무조건 캐시와 DB 양쪽에 동시에 업데이트하여, 캐시의 데이터가 항상 DB와 100% 동일한 최신 상태를 유지하도록 강제하는 동기 쓰기 전략.

</details>

- 정의/개념: 사본의 적재•조회•무효화를 정하는 **Caching Strategy**
- 배경/필요성: 원본 직접 조회는 Traffic Spike에서 **I/O 병목•지연 증가** 유발

#### 한줄 요약

- 가까운 사본을 누가 채우고 언제 버리며 원본 변경 뒤 어떻게 맞출지 정해야 빠른 조회가 오래된 답으로 바뀌지 않는다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Cache Invalidation (캐시 무효화)**: DB의 데이터가 변경(Update/Delete)되었을 때, 캐시에 남아있는 과거 데이터(Stale Data)를 강제로 지워버리는 작업. Cache-Aside의 핵심 쓰기 패턴.

</details>

- **Lazy Loading (지연 로딩)**: (Cache-Aside) 클라이언트가 요청한 데이터만 캐시에 적재하므로, 안 쓰는 데이터가 캐시 메모리를 낭비하지 않는 공간 효율성 확보.
- **Stale Data Risk (구버전 노출 위험)**: (Cache-Aside) 캐시에 들어간 데이터는 DB가 바뀌어도 TTL이 끝날 때까지 갱신되지 않으므로 최신성 위배(Inconsistency) 발생 가능성 내재.
- **Write-Through** 기반 Cache•DB 동기 경로로 최신성 창을 축소

#### 한줄 요약

- 인기 상품 사본이 동시에 만료돼도 대표 요청 하나만 원본을 읽고 나머지가 결과를 공유하면 데이터베이스 폭주를 막을 수 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **TTL (Time To Live)**: 캐시에 저장된 데이터가 유효한 시간(수명). TTL이 만료되면 해당 데이터는 메모리에서 자동 삭제(Eviction)되며, 다음 요청 시 DB에서 새로 조회.

</details>

```text
[Caching Layer]
 ├── [Cache Store]
 ├── [Origin]
 ├── [Eviction Policy]
 └── [TTL•Invalidation]
```

| 구성요소 | 책임 |
|---|---|
| Cache Store | Key별 **고속 사본•Version** 보관 |
| Origin | 권위 있는 **Source of Truth** 및 영속성 제공 |
| Eviction Policy | 용량 부족 때 **축출 Key** 결정 |
| TTL•Invalidation | 사본의 **유효 기간•변경 반영** 통제 |

#### 한줄 요약

- 응용이 사본 주소와 정책을 정하고 캐시는 보관하며 무효화 계층이 원본 변경을 알리고 요청 병합이 몰리는 손님을 한 줄로 세운다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Write-Behind (Write-Back)**: 모든 데이터를 일단 캐시에만 아주 빠르게 쓰고(응답 완료), 백그라운드 스레드가 모아두었다가 나중에(Asynchronous) 한꺼번에 DB에 벌크로 밀어넣는 고성능 쓰기 전략.

</details>

```text
[Read 요청]
    │
    ▼
1. Cache Key 조회
 ┌──┴────────────┐
 │ Hit           │ Miss
2. Hit•Miss 판정
 │ Hit           │ Miss
 │               ▼
 │        3. 원본 단일 조회
 │               │
 │        4. Cache 적재•갱신
 └───────┬───────┘
      5. 결과 반환
```

### 동작 원리

1. Cache Key 조회: 정규화한 Key로 사본 탐색
2. Hit•Miss 판정: Version•TTL로 사본 유효성 확인
3. 원본 단일 조회: Miss 동시 요청을 병합해 Origin 호출
4. Cache 적재•갱신: 원본값을 TTL•Jitter와 저장
5. 결과 반환: 사본 또는 원본 결과 응답

#### 한줄 요약

- 사본이 없을 때 첫 요청만 원본을 읽고 값과 버전을 저장하면 뒤따른 요청은 같은 결과를 받아 원본 호출을 반복하지 않는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Cache Miss (캐시 미스)**: 캐시에 찾는 데이터가 없어 결국 느린 원본 DB까지 다녀와야 하는 상황. 이것이 반복되면 캐시를 도입한 의미가 퇴색됨.

</details>

| 구분 | Cache-Aside (Look-Aside) | Write-Through |
|:---|:---|:---|
| 주요 용도 | **일반적인 읽기 최적화 (가장 많이 씀)** | **읽기/쓰기 모두 중요한 정합성 필수 구간** |
| 캐시 공간 효율 | **실제 요청된 데이터만 적재 (효율 높음)** | **안 읽을 데이터도 무조건 적재 (효율 낮음)** |
| 쓰기 지연 시간 | 원본 Write와 무효화 비용 | **Cache•원본 동기 경로 비용** |
| 구현 난이도 | App에서 코드 라인 증가 (if-else 패턴) | 구조 단순 (DB가 뒷단에 숨겨짐) |

#### 한줄 요약

- 조회 중심은 응용이 필요한 값만 채우고 즉시 원본 반영이 필요하면 동기 쓰기, 지연 반영을 허용하면 비동기 쓰기를 제한적으로 사용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Cache Stampede (캐시 스탬피드 / Thundering Herd)**: 매우 핫(Hot)한 데이터의 TTL이 만료된 순간, 수만 개의 동시 요청이 전부 캐시 미스를 내고 동시에 DB로 돌진하여 DB가 즉사하는 대형 장애 현상.

</details>

| 3대 캐시 장애 요인 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Cache Stampede | 인기 키(Key) 만료 시 DB 동시 조회 폭주 | **요청 병합(Request Collapsing) 및 PER(Probabilistic Early Recomputation)**|
| 2. Cache Penetration | DB에도 없는 악성 키(Key) 무한 요청 | **DB에 없다는 사실 자체를 캐싱 (부정 캐싱, Negative Caching)** |
| 3. 만료 주기(TTL) 쏠림 | 대량 적재된 캐시들이 일제히 동시 만료됨 | **TTL Jitter (기준 시간에 $±10\%$ 난수 지연 부여로 만료 시간 분산)**|

> 사례: **넷플릭스와 트위터의 레디스(Redis) 클러스터 도입 시 Cache Stampede 방어를 위한 백그라운드 사전 갱신(Warm-up) 아키텍처**

#### 한줄 요약

- 캐시 전체 장애 때 모든 요청이 캐시를 건너뛰어 원본으로 향하지 않도록 호출 상한과 차단기로 원본의 연쇄 장애를 막아야 한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **캐싱 전략 수립 기준**: 데이터 정합성 요구 수준(강결합 vs 최종 일관성), 읽기/쓰기 비율 패턴(Read-Heavy vs Write-Heavy), 장애 전파 차단(Circuit Breaker)에 의거한 체계.

</details>

- 조회 중심은 **Cache-Aside**, 최신성 높은 Write는 동기 갱신 검토

#### 한줄 요약

- 조회 중심은 캐시 어사이드로 시작하고 TTL·요청 병합·버전 무효화를 함께 설계해 속도와 원본 보호를 동시에 확보해야 한다.
