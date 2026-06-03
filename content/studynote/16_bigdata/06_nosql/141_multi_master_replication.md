---
title: 141. 멀티 마스터 복제 (Multi-Master Replication) — CouchDB/DynamoDB Global Tables
date: '2026-04-21'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
- **본질**: [[272_multi_master_replication|멀티 마스터 복제]]는 여러 노드 또는 리전에서 동시에 [[289_cqrs_db|쓰기]]를 허용하여 단일 [[289_cqrs_db|쓰기]] [[172_maas_mobility_as_a_service|마스]]터의 지리적 병목과 [[454_spof|단일 장애점]]을 제거하는 [[136_variance|분산]] [[016_replication_factor|복제]] 아키텍처다.
- **가치**: 글로벌 [[090_service_kubernetes_network_load_balancing|서비스]]에서 "가장 가까운 리전에 [[289_cqrs_db|쓰기]]"가 가능해져 [[289_cqrs_db|쓰기]] [[015_지연_데이터_관점|지연]]이 수백ms에서 수ms로 줄어들고, 리전 전체 장애 시에도 다른 리전이 [[289_cqrs_db|쓰기]]를 계속 수용한다.
- **판단 포인트**: 충돌 해결 [[268_strategy_pattern|전략]](LWW/벡터 클록/CRDT) 선택이 핵심으로, [[001_dikw_pyramid|데이터]] 손실을 최소화하려면 CRDT 또는 앱 레벨 병합이 필요하며 LWW는 단순하지만 [[289_cqrs_db|쓰기]] 손실 위험이 있다.

---

## Ⅰ. 개요 및 필요성

### 단일 [[172_maas_mobility_as_a_service|마스]]터 vs 멀티 [[172_maas_mobility_as_a_service|마스]]터 비교

```text
┌─────────────────────────────────────────────────────────────┐
│  단일 마스터 복제 (Single-Master)                             │
│                                                             │
│  서울 사용자       도쿄 마스터        뉴욕 레플리카            │
│  [쓰기 요청] ─────→ [Primary] ─────→ [Replica]              │
│                                                             │
│  지연: 서울→도쿄 ~30ms + 처리 = ~50ms                        │
│  장애: 도쿄 다운 → 전 세계 쓰기 불가                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  멀티 마스터 복제 (Multi-Master)                              │
│                                                             │
│  서울 Master ←──────────────────────→ 뉴욕 Master            │
│      ↕  (양방향 비동기 복제)              ↕                   │
│  도쿄 Master ←──────────────────────→ 유럽 Master            │
│                                                             │
│  서울 사용자 → 서울 Master (로컬 쓰기, ~5ms)                  │
│  장애: 서울 다운 → 다른 3개 Master가 계속 쓰기 수용            │
└─────────────────────────────────────────────────────────────┘
```

### 충돌 발생 시나리오

```text
충돌 예시: 동일 문서를 두 리전에서 동시 수정

  서울 Master: user:john.age = 30  (T=1000)
  도쿄 Master: user:john.age = 31  (T=1001, 거의 동시)

  복제 완료 후: 두 Master에 상충하는 버전 존재
  → 충돌 해결 전략 필요
```

📢 **섹션 요약 비유**
> [[272_multi_master_replication|멀티 마스터 복제]]는 구글 독스의 실시간 협업 편집과 같다. 서울과 뉴욕의 두 편집자가 같은 문서를 동시에 수정할 수 있지만, 같은 단어를 서로 다르게 고쳤다면 충돌을 어떻게 해결할지 규칙이 필요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 충돌 해결 [[268_strategy_pattern|전략]] 3가지

```text
┌────────────────────────────────────────────────────────────┐
│  1. LWW (Last-Write-Wins, 최신 쓰기 우선)                  │
│                                                            │
│  서울 쓰기 (T=1000) vs 도쿄 쓰기 (T=1001)                   │
│  → 타임스탬프 비교 → T=1001 (도쿄) 승리                      │
│                                                            │
│  장점: 단순, 빠른 충돌 해결                                   │
│  단점: 서울 쓰기 손실 (데이터 유실)                           │
│  사용: DynamoDB Global Tables (기본값)                      │
├────────────────────────────────────────────────────────────┤
│  2. 벡터 클록 (Vector Clock)                               │
│                                                            │
│  각 쓰기에 [Seoul:3, Tokyo:1] 형태의 벡터 클록 부여          │
│  비교: 한쪽이 다른 쪽의 모든 버전을 포함하면 더 최신            │
│  충돌: 어느 쪽도 포함하지 않으면 진짜 충돌 → 앱 해결          │
│                                                            │
│  장점: 인과 관계 추적, 의미 있는 충돌 감지                    │
│  단점: 클록 크기 노드 수에 비례 증가                          │
│  사용: Riak, CouchDB                                       │
├────────────────────────────────────────────────────────────┤
│  3. CRDT (Conflict-free Replicated Data Type)              │
│                                                            │
│  수학적으로 항상 병합 가능한 자료구조 설계                     │
│  예: G-Counter (증가만) → merge = max(각 노드 값)            │
│  예: OR-Set → add/remove가 충돌 없이 병합 가능               │
│                                                            │
│  장점: 자동 충돌 해결, 데이터 손실 없음                        │
│  단점: 모든 연산에 적용 불가 (복잡한 비즈니스 로직)             │
│  사용: Riak (기본), Redis CRDT (엔터프라이즈)                 │
└────────────────────────────────────────────────────────────┘
```

### [[545_dynamodb|DynamoDB]] Global Tables 아키텍처

```text
┌───────────────────────────────────────────────────────────────┐
│              DynamoDB Global Tables                           │
│                                                               │
│  ┌──────────────┐        ┌──────────────┐                    │
│  │  ap-northeast │        │  us-east-1   │                    │
│  │  (서울 리전)  │        │  (버지니아)   │                    │
│  │              │        │              │                    │
│  │  table:orders│←──────→│  table:orders│                    │
│  │  (Active)    │  양방향  │  (Active)    │                    │
│  │              │  복제   │              │                    │
│  └──────────────┘        └──────────────┘                    │
│           ↕                      ↕                            │
│  ┌──────────────┐        ┌──────────────┐                    │
│  │  eu-west-1   │        │  ap-southeast│                    │
│  │  (아일랜드)  │←──────→│  (싱가포르)  │                    │
│  │  (Active)    │        │  (Active)    │                    │
│  └──────────────┘        └──────────────┘                    │
│                                                               │
│  충돌 해결: LWW (타임스탬프 기반)                               │
│  복제 지연: 일반적으로 수초 이내                                 │
│  조건: 각 리전에서 고유한 PK 사용 권장 (충돌 최소화)             │
└───────────────────────────────────────────────────────────────┘
```

### CouchDB 개정(Revision) 기반 충돌 감지

```text
CouchDB 문서:
{
  "_id": "user:john",
  "_rev": "3-abc123",   ← 개정 번호:해시
  "age": 30
}

충돌 발생:
  서울: _rev: "3-abc123" → 수정 → "4-def456"
  도쿄: _rev: "3-abc123" → 수정 → "4-xyz789"

CouchDB 충돌 처리:
  - 두 버전 모두 보존 (충돌 상태로 저장)
  - 앱이 충돌 감지 + 해결 책임
  - 해결된 버전으로 "winning" 버전 저장

CouchDB 오프라인 우선 동기화:
  모바일 앱 → 오프라인 작업 → 온라인 시 서버와 복제
  → 동기화 충돌 자동 감지 + 앱 레벨 해결
```

📢 **섹션 요약 비유**
> CRDT의 G-Counter는 학급의 팀 점수판과 같다. 서울팀과 도쿄팀이 동시에 점수를 추가해도 충돌이 없다 — 최종 합계는 모든 노드의 최댓값을 더하면 된다. "감점"이 없어서 충돌 없이 병합 가능한 수학적 설계다.

---

## Ⅲ. 비교 및 연결

### 멀티 [[172_maas_mobility_as_a_service|마스]]터 vs 단일 [[172_maas_mobility_as_a_service|마스]]터 vs [[172_maas_mobility_as_a_service|마스]]터리스

| 항목 | 단일 [[172_maas_mobility_as_a_service|마스]]터 | 멀티 [[172_maas_mobility_as_a_service|마스]]터 | [[172_maas_mobility_as_a_service|마스]]터리스 ([[541_cassandra|Cassandra]]) |
|:---:|:---:|:---:|:---:|
| [[289_cqrs_db|쓰기]] 지점 | 1개 | N개 (리전별) | 모든 노드 |
| 충돌 가능성 | 없음 | 있음 (해결 필요) | 있음 (QUORUM) |
| [[289_cqrs_db|쓰기]] [[452_availability|가용성]] | [[172_maas_mobility_as_a_service|마스]]터 의존 | 높음 | 매우 높음 |
| [[015_지연_데이터_관점|지연]] (로컬 [[289_cqrs_db|쓰기]]) | [[172_maas_mobility_as_a_service|마스]]터까지 거리 | 로컬 | 로컬 |
| 복잡도 | 낮음 | 중간 | 낮음 (설계만 다름) |
| 적합 | 단순 [[090_service_kubernetes_network_load_balancing|서비스]] | 글로벌 RDBMS/[[035_nosql|NoSQL]] | 대규모 [[035_nosql|NoSQL]] |

### Operational Transformation vs CRDT

```text
Operational Transformation (OT): 구글 독스 방식
  - 동시 편집 작업(연산)을 변환하여 충돌 해결
  - 중앙 서버에서 순서 조정 필요
  - 복잡한 알고리즘

CRDT: 분산 시스템 방식
  - 데이터 타입 자체가 병합 가능하게 설계
  - 중앙 서버 불필요
  - 일부 연산에만 적용 가능 (증가, 집합 추가 등)
```

📢 **섹션 요약 비유**
> 멀티 [[172_maas_mobility_as_a_service|마스]]터와 [[172_maas_mobility_as_a_service|마스]]터리스의 차이는 다국적 기업의 의사결정 구조와 같다. 멀티 [[172_maas_mobility_as_a_service|마스]]터는 "서울·뉴욕 둘 다 결재권 있음" (그러나 같은 안건에 서로 다른 결재 시 충돌), [[172_maas_mobility_as_a_service|마스]]터리스는 "모든 지사가 결재권 있지만 과반수 동의 필요" ([[541_cassandra|Cassandra]] QUORUM).

---

## Ⅳ. 실무 적용 및 기술사 판단

### 글로벌 e-커머스 멀티 [[172_maas_mobility_as_a_service|마스]]터 설계

```text
요구: 서울·뉴욕·유럽 동시 쓰기, 재고 정확도 보장

설계 결정:
  ① 상품 카탈로그(낮은 충돌) → DynamoDB Global Tables (LWW)
  ② 재고 수량(충돌 위험 높음) → Cassandra + QUORUM 또는
                                  단일 재고 서비스(분산 잠금)
  ③ 사용자 프로필(Session 일관성) → Session + Last-Write-Wins
  ④ 장바구니(동시 추가) → CRDT OR-Set (충돌 없는 추가)

핵심 원칙:
  높은 충돌 위험 데이터 → 멀티 마스터 지양 (단일 마스터 유지)
  낮은 충돌 위험 데이터 → 멀티 마스터 적극 활용
```

### 충돌 최소화 설계 패턴

| 패턴 | 설명 | 적용 예시 |
|:---:|:---|:---:|
| **[[514_partition_slice_volume|파티션]]별 소유권** | 각 리전이 다른 키 범위 담당 | 서울: KR 사용자, 뉴욕: US 사용자 |
| **수렴 자료구조** | CRDT 사용 | 좋아요 [[059_counter|카운터]], 장바구니 |
| **[[171_idempotency_iac_terraform|멱등성]] 연산** | 같은 요청 여러 번 실행해도 동일 결과 | 결제 처리 |
| **인과 [[012_metadata|메타데이터]]** | [[288_version_ihl_tos_total_length|버전]] 토큰과 함께 [[289_cqrs_db|쓰기]] | 조건부 업데이트 |

📢 **섹션 요약 비유**
> [[514_partition_slice_volume|파티션]]별 소유권 패턴은 나라별 담당자를 정하는 것과 같다. 한국 고객 [[001_dikw_pyramid|데이터]]는 서울 [[172_maas_mobility_as_a_service|마스]]터만, 미국 고객 [[001_dikw_pyramid|데이터]]는 뉴욕 [[172_maas_mobility_as_a_service|마스]]터만 수정한다. 담당 구역이 겹치지 않으니 충돌 자체가 발생하지 않는 가장 근본적인 충돌 방지 방법이다.

---

## Ⅴ. 기대효과 및 결론

### 멀티 [[172_maas_mobility_as_a_service|마스]]터 도입 효과 (글로벌 [[090_service_kubernetes_network_load_balancing|서비스]] 기준)

| 지표 | 단일 [[172_maas_mobility_as_a_service|마스]]터(도쿄) | 멀티 [[172_maas_mobility_as_a_service|마스]]터(4 리전) |
|:---:|:---:|:---:|
| 서울 [[289_cqrs_db|쓰기]] [[015_지연_데이터_관점|지연]] | ~30ms (도쿄 왕복) | ~3ms (로컬) |
| 도쿄 장애 시 [[289_cqrs_db|쓰기]] | 불가 (수십 초 페일오버) | 즉시 다른 리전 |
| 글로벌 [[289_cqrs_db|쓰기]] [[452_availability|가용성]] | 99.95% | 99.999% |
| 아키텍처 복잡도 | 낮음 | 중간 (충돌 처리 필요) |

### 결론
[[272_multi_master_replication|멀티 마스터 복제]]는 글로벌 [[289_cqrs_db|쓰기]] [[452_availability|가용성]]과 낮은 [[015_지연_데이터_관점|지연]]이 비즈니스 요구 사항일 때의 필수 아키텍처 패턴이다. 그러나 충돌 해결은 [[001_dikw_pyramid|데이터]]의 비즈니스 특성에 맞게 세심하게 설계해야 한다. 기술사 시험에서는 **LWW vs 벡터 클록 vs CRDT 충돌 해결 비교**, **[[545_dynamodb|DynamoDB]] Global Tables 작동 원리**, **CouchDB 개정 기반 충돌 감지**, **[[514_partition_slice_volume|파티션]]별 소유권 설계 패턴**이 핵심 논점이다.

📢 **섹션 요약 비유**
> [[272_multi_master_replication|멀티 마스터 복제]]는 세계 각지에 지사를 두되, 각 지사가 독립적으로 결정을 내릴 수 있게 하는 [[136_variance|분산]] 경영 방식이다. 결정이 충돌하면 누구의 결정을 따를지 규칙(충돌 해결 [[268_strategy_pattern|전략]])이 있어야 하고, 충돌이 최소화되도록 각 지사의 담당 업무를 명확히 나누는([[514_partition_slice_volume|파티션]]별 소유권) 것이 운영의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---:|:---:|:---|
| LWW (Last-Write-Wins) | 충돌 해결 | 타임스탬프로 최신 [[289_cqrs_db|쓰기]] 선택 |
| 벡터 클록 | 충돌 탐지 | 인과 [[083_relationship_in_er_model|관계]] 기반 충돌 정밀 감지 |
| CRDT | 충돌 없는 설계 | 자동 병합 가능한 자료구조 |
| [[483_active_vs_passive_ftp|Active]]-[[483_active_vs_passive_ftp|Active]] | 배포 패턴 | 모든 노드가 읽기/[[289_cqrs_db|쓰기]] 처리 |
| [[556_master_slave_replication_lag_inconsistency|Replication Lag]] | [[016_replication_factor|복제]] [[015_지연_데이터_관점|지연]] | 노드 간 [[001_dikw_pyramid|데이터]] [[212_synchronization_mechanisms|동기화]] [[141_latency|지연 시간]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[싱글 마스터 복제 (Single Master) — 단일 쓰기 노드, 읽기 확장]
    │
    ▼
[멀티 마스터 복제 (Multi-Master) — 여러 노드 동시 쓰기, 고가용성]
    │
    ▼
[충돌 해결 (Conflict Resolution) — 최종 쓰기 우선·벡터 클록·사용자 정의]
    │
    ▼
[CRDT (무충돌 복제 자료구조) — 수학적으로 충돌 없는 분산 자료구조]
    │
    ▼
[글로벌 분산 DB (CockroachDB·Spanner) — 지역별 멀티 마스터 + 일관성 보장]
```
[[272_multi_master_replication|멀티 마스터 복제]]는 단일 [[172_maas_mobility_as_a_service|마스]]터의 [[452_availability|가용성]] 한계를 극복하지만 충돌 해결 복잡성을 낳으며, CRDT와 글로벌 [[136_variance|분산]] [[002_database_definition|데이터베이스]]로 진화해 지역 레이턴시와 [[194_consistency_database_integrity|일관성]]을 동시에 해결한다.

### 👶 어린이를 위한 3줄 비유 설명
1. 멀티 [[172_maas_mobility_as_a_service|마스]]터는 분반된 학급에서 모든 반이 수업을 동시에 [[216_progress_in_synchronization|진행]]하는 것 — 어느 반에 가도 수업을 받을 수 있어서 한 반이 쉬어도 괜찮아요.
2. 충돌은 두 선생님이 같은 칠판에 동시에 다른 내용을 쓰는 것 — 나중에 쓴 것을 채택(LWW)하거나, 내용을 합쳐서(CRDT) 해결해요.
3. [[545_dynamodb|DynamoDB]] Global Tables는 전 세계 편의점 체인처럼 — 어느 나라 지점에서 상품을 사도 재고가 자동으로 업데이트되고, 충돌 시 가장 최신 시각의 정보가 채택돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 141 / 262

← **이전**: [[140_consistency_levels|140. 일관성 수준 선택 (Consistency Levels) — Strong/Eventual/Bounded Staleness]]
**다음**: [[142_schemaless_design_patterns|142. 스키마리스 설계 패턴 (Schemaless Design Patterns) — 임베딩 vs 참조]] →

---
