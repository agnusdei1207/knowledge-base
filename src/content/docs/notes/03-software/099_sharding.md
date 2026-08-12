---
sidebar:
  order: 99
  label: "099. 샤딩: 수평 분할 (Sharding)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "샤딩: 수평 분할 (Sharding)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 99
extra:
  question_no: "099"
  source_status: "기출"
  source_history: "123회"
  priority: 50
  priority_note: "123회 기출, 샤드 키•재분배 설계 가치"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Database Sharding (데이터베이스 샤딩)**: 단일 데이터베이스 서버의 스케일-업(Scale-Up) 한계를 극복하기 위해, 대용량 데이터를 샤드 키(Shard Key) 기준으로 분할하여 다수의 독립된 물리 DB 노드(Shard Node)에 수평 분산(Scale-Out) 저장하는 아키텍처.
- **Shard Key (샤드 키)**: 데이터 튜플을 어떤 샤드 노드에 배치할지 결정하는 기준 컬럼 (예: `user_id`, `tenant_id`).
- **Cross-Shard Query**: 샤드 키 조건이 쿼리에 포함되지 않아 모든 샤드 노드에 쿼리를 흩뿌려서 결과를 취합하는 고비용 쿼리 (Scatter-Gather 패턴).

</details>

- 정의/개념: 단일 DB의 수직 확장 한계를 극복하기 위해 샤드 키 기반으로 수평 분산 노드(Shard Node)를 구축하여 데이터베이스의 저장 용량과 TPS를 수평 확장(Scale-Out)하는 기술인 **Database Sharding**
- 배경/필요성: 단일 데이터베이스 물리 디스크 용량 한계 및 CPU/Connection 병목 극복, 무제한 데이터 스케일링을 통한 초고가용성 분산 IT 인프라 구축 요구성

#### 한줄 요약

- 샤드 키의 해시 또는 범위 규칙으로 행을 여러 노드에 분배하고 같은 규칙으로 대상 노드를 결정하는 수평 분할 기법이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Horizontal Scaling (Scale-Out)**: DB 노드를 수평 추가하여 읽기/쓰기 처리량 무제한 확장.
- **Data Skew (샤드 데이터 불균형)**: 샤드 키 설정 미숙으로 특정 샤드 노드에만 트래픽과 데이터가 90% 이상 쏠리는 안티패턴.

</details>

- **Horizontal Scale-Out (수평적 디스크/TPS 확장성)**
- **Shard Key** 선택에 따른 데이터 균등 분산 성능 결정
- **Cross-Shard Join / Distributed Transaction** 복잡도 폭증 Trade-off

#### 한줄 요약

- 자료를 고르게 나누고 한 지점에서 찾게 해야 확장 효과가 크며, 여러 지점을 동시에 찾으면 조정 비용이 커진다.

## Ⅲ. 구조 및 구성요소 (샤딩 3대 핵심 분산 방식)

<details><summary>핵심 용어</summary>

- **Consistent Hashing (일관된 해시)**: 샤드 노드가 추가/삭제되더라도 전체 데이터를 다시 재배치(Rebalancing)하지 않고 오직 $1/N$의 데이터만 이동시키는 고성능 해시 샤딩 알고리즘.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Database Sharding 분산 라우팅 구조                   │
├────────────────────────────────────────────────────────────────────────┤
│ Client Query ──► [Shard Router / Proxy (Vitess, Citus, ShardingSphere)]│
│                                │ (Shard Key 라우팅)                    │
│        ┌───────────────────────┼───────────────────────┐               │
│        ▼                       ▼                       ▼               │
│  [Shard Node 1]         [Shard Node 2]          [Shard Node 3]         │
│  (user_id: 1~1000)      (user_id: 1001~2000)    (user_id: 2001~3000)   │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 샤드 라우터(Proxy)가 샤드 키 조건(`user_id`)을 해석하여 해당 데이터를 소유한 특정 샤드 노드로 쿼리를 단일 라우팅하는 구조.

| 샤딩 분산 방식 | 분할 방식 및 매커니즘 | 장점 및 단점 비교 |
|:---|:---|:---|
| **Key-Based (Hash Sharding)** | **`Hash(Shard_Key) % N`** 기반으로 노드 결정 | **데이터 균등 분산 우수**, 노드 추가 시 전체 데이터 재배치 오버헤드 |
| **Range-Based Sharding** | **`user_id: 1~1000` 등 범위별 분할** | **구현 직관적**, 특정 최신 범위 샤드로 트래픽 쏠림(Hotspot) 발생 |
| **Directory-Based Sharding**| **별도 룩업 테이블(Lookup Table) 매핑 정보 관리**| **샤드 재배치 자유로움**, 룩업 테이블 단일 장애점(SPOF) 위험 |

#### 한줄 요약

- 샤드 라우터가 샤드 키와 배치 메타데이터로 대상 데이터 샤드를 결정한다.

## Ⅳ. 흐름도 (Consistent Hashing 기반 링(Ring) 구조 및 Node 확장)

<details><summary>핵심 용어</summary>

- **Hash Ring**: $0 \sim 2^{32}-1$ 범위의 해시 공간을 원형 링으로 구성하여 노드와 데이터의 키 위치를 맵핑하는 구조.

</details>

```text
[Consistent Hash Ring ($0 \sim 2^{32}-1$)]
           [Node A (Virtual Node)]
           /                      \
    [Data Key 1]                [Node B]
          \                      /
           [Node C (Virtual Node)]
```

### 동작 원리

1. **Virtual Node Mapping**: 데이터 쏠림을 방지하기 위해 가상 노드(Virtual Node)를 링 상에 배치.
2. **Node Addition**: 신규 샤드 노드 D 추가 시, 오직 옆 노드의 데이터 일부만 신규 노드로 이관되며 나머지 노드의 데이터는 전혀 영향을 받지 않음 (**재배치 비용 최소화**).

#### 한줄 요약

- 안내소가 번호로 담당 지점을 찾고 요청을 한 곳에서 끝낸 뒤 혼잡도까지 기록한다.

## Ⅴ. 종류 및 비교 (파티셔닝 대 샤딩)

<details><summary>핵심 용어</summary>

- **Partitioning vs Sharding**: 파티셔닝은 single-node 내 파일 분할, 샤딩은 multi-node 간 네트워크 수평 분산.

</details>

| 비교 항목 | Table Partitioning (파티셔닝) | Database Sharding (샤딩) |
|:---|:---|:---|
| 물리 아키텍처 | **단일 DB 서버 (Single Node)** | **다중 독립 DB 노드 (Multi-Node)** |
| 통신 방식 | Shared-Disk / Shared-Memory (내부 I/O) | **Shared-Nothing (네트워크 통신 I/O)** |
| 락 및 트랜잭션 | **단일 DB ACID 트랜잭션 100% 보장** | **분산 트랜잭션 (2PC / Saga Pattern) 필요**|
| 확장 한계성 | 단일 서버 CPU/RAM 물리적 한계 갇힘 | **서버 노드 무한 수평 확장 (Scale-Out)** |

#### 한줄 요약

- 번호 구간으로 나누면 범위 찾기가 쉽고, 해시로 나누면 고르며, 목록으로 지정하면 원하는 위치에 둘 수 있다.

## Ⅵ. 실무 고려사항 및 대책 (샤딩 3대 난제 및 해결책)

<details><summary>핵심 용어</summary>

- **Distributed Transaction Challenge**: 샤드가 나누어지면 RDBMS 표준 ACID 트랜잭션을 쓸 수 없어 2PC(Two-Phase Commit) 또는 Saga Pattern으로 최종 일관성 처리 필요.

</details>

| 3대 샤딩 난제 | 발생 원인 및 위협 요소 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Cross-Shard Join** | 서로 다른 샤드 노드 간 테이블 `JOIN` 불가 | **데이터 중복 허용(Denormalization) 및 앱 단 조인** |
| **2. Distributed Transaction**| 2개 이상 샤드에 걸친 ACID 트랜잭션 불가 | **Saga Pattern & 이벤트 기반 최종 일관성 적용** |
| **3. Global Unique ID** | 단일 DB의 Auto-Increment PK 사용 불가 | **Twitter Snowflake / UUID / TSID 글로벌 ID 적용** |

> 사례: **카카오톡 / 네이버 Vitess 기반 MySQL 샤딩 미들웨어 운용**

#### 한줄 요약

- 고객 자료를 한 지점에 모으되 큰 고객 하나가 지점을 독점하지 않게 분포를 감시한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **샤딩 아키텍처 수립 기준(Sharding Architecture Standards)**: 데이터 스케일, Shard Key 선택성, Consistent Hashing 및 샤딩 미들웨어(Vitess)에 의거한 체계.

</details>

- **샤딩 아키텍처 수립 기준**에 따라 초대규모 트래픽 DB 구축 시 **Consistent Hashing & Vitess 샤딩 미들웨어** 필수 적용

#### 한줄 요약

- 샤딩 방식 선택 기준은 요청을 담당 샤드에 모으면서 과부하를 고르게 분산한다.
