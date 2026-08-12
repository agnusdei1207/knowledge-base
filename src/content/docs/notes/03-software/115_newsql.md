---
sidebar:
  order: 115
  label: "115. NewSQL: CockroachDB•Spanner (NewSQL)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "NewSQL: CockroachDB•Spanner (NewSQL)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 115
extra:
  question_no: "115"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "일관성•확장성을 결합한 분산 SQL 현안"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **NewSQL**: RDBMS의 전통적 100% ACID 트랜잭션과 표준 SQL 인터페이스를 그대로 유지하면서, NoSQL이 가진 무한한 수평 확장성(Scale-Out)과 고가용성을 결합한 차세대 분산 관계형 데이터베이스 분류.
- **Google Spanner**: 원자 시계(Atomic Clock)와 GPS 기반의 TrueTime API를 활용하여 글로벌 마티노드 간 전역 직렬성(External Consistency / Serializability)을 100% 달성한 글로벌 NewSQL 표준 DB.
- **CockroachDB**: Google Spanner 아키텍처 논문을 참조해 오픈소스로 구현된 distributed SQL DB로, Raft consensus 및 Hybrid Logical Clock(HLC) 기반의 멀티노드 수평 확장 지원.

</details>

- 정의/개념: RDBMS의 100% Strict ACID 트랜잭션 무결성과 NoSQL의 수평 확장성(Scale-Out)을 동시 만족시키는 현대 분산 SQL 데이터베이스 기술인 **NewSQL**
- 배경/필요성: 기존 RDBMS의 단일 노드 스케일링 한계와 NoSQL의 ACID/SQL 미지원(BASE 모델의 데이터 정합성 파괴) 문제를 동시에 극복하려는 요구성

#### 한줄 요약

- SQL 장부를 지점에 나누고 합의로 하나의 거래처럼 처리한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Distributed ACID & 2PC**: 다중 분산 노드에 걸쳐 100% ACID 트랜잭션 보장.
- **Raft / Paxos Consensus**: 복제 노드 간 데이터 일관성을 위해 Raft/Paxos 합의 알고리즘 수용.

</details>

- **Standard SQL Support & 100% Strict ACID Guarantees**
- **Distributed Shared-Nothing Scale-Out Architecture**
- **Consensus Protocol (Raft / Paxos)** 및 **Distributed Time Sync (TrueTime / HLC)**

#### 한줄 요약

- 확장과 ACID를 함께 제공하지만 합의 왕복과 재시도 비용이 생긴다.

## Ⅲ. 구조 및 구성요소 (CockroachDB vs Google Spanner 기술 아키텍처)

<details><summary>핵심 용어</summary>

- **TrueTime API vs HLC**: Spanner는 GPS+원자시계 하드웨어로 시간 오차 $\epsilon$를 $O(1\text{ms})$로 제어, CockroachDB는 소프트웨어적 HLC(Hybrid Logical Clock)로 시계열 순서 관리.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   NewSQL 2대 대표 제품 아키텍처                        │
├───────────────────────────────────┬────────────────────────────────────┤
│ 1. Google Spanner                 │ 2. CockroachDB                     │
├───────────────────────────────────┼────────────────────────────────────┤
│ • TrueTime API (GPS + Atomic Clock)│ • Hybrid Logical Clock (HLC)       │
│ • Paxos Consensus Engine          │ • Raft Consensus Engine            │
│ • Multi-Region Distributed ACID   │ • PostgreSQL Wire-Protocol 호환    │
└───────────────────────────────────┴────────────────────────────────────┘
```

선의 의미: 시계열 동기화(TrueTime/HLC) 및 합의 알고리즘(Paxos/Raft)을 기반으로 분산 ACID를 수용하는 NewSQL 구조.

| 구성 요소 / 기술 | Google Spanner | CockroachDB |
|:---|:---|:---|
| **시간 동기화 방식** | **TrueTime API (GPS hardware + Atomic Clock)** | **Hybrid Logical Clock (HLC - Software)** |
| **분산 합의 알고리즘**| **Paxos Protocol** | **Raft Protocol** |
| **SQL 인터페이스 호환**| Google Standard SQL / PostgreSQL dialect | **PostgreSQL Wire-Protocol 100% 호환** |
| **운영 인프라 형태** | **Google Cloud Platform (GCP) 전용 PaaS** | **On-Premise / Multi-Cloud 자율 배포 가능** |

#### 한줄 요약

- SQL 접수자, 위치표, 거래 조정자, 합의 사본, 순서 시계로 구성된다.

## Ⅳ. 흐름도 (NewSQL 분산 ACID 트랜잭션 렌더링)

<details><summary>핵심 용어</summary>

- **Distributed Lock-Free Read (TrueTime Read)**: TrueTime / HLC 기반 타임스탬프를 통해 읽기 연산 시 락(Lock)을 전혀 걸지 않고 과거 특정 시점의 Snapshot Read를 즉시 수행하는 기술.

</details>

```text
[Client SQL Transaction] ──► [SQL Gateway Node]
                                    │
                                    ▼ (Range Location Lookup)
[Range 1 (Raft Leader Node A)] ◄─── 2PC ───► [Range 2 (Raft Leader Node B)]
  • Raft Log Replication                     • Raft Log Replication
  • Quorum Commit                            • Quorum Commit
```

### 동작 원리

1. **SQL Routing**: SQL 게이트웨이 노드가 쿼리를 받아 데이터 Range 위치 추적.
2. **Distributed 2PC**: 2개 이상의 Range 노드에 걸친 분산 2PC(Two-Phase Commit) 개시.
3. **Raft Consensus**: 각 Range 내부의 Raft 복제본 과반수 승인을 거쳐 **글로벌 원자 커밋 완결**.

#### 한줄 요약

- SQL을 담당 구간에 나누어 보내고 모든 구간의 사본 확인 뒤 하나의 거래로 확정한다.

## Ⅴ. 종류 및 비교 (RDBMS vs NoSQL vs NewSQL 3대 축 종합 비교)

<details><summary>핵심 용어</summary>

- **NewSQL Position**: RDBMS의 ACID/SQL과 NoSQL의 Scale-Out 장점만을 완전 결합.

</details>

| 비교 항목 | Traditional RDBMS (MySQL) | NoSQL (Cassandra, MongoDB) | NewSQL (CockroachDB, Spanner) |
|:---|:---|:---|:---|
| **트랜잭션 모델** | **Strict ACID** | **BASE (Eventual Consistency)**| **Strict ACID** |
| **수평 확장성** | 매우 낮음 (Scale-Up 위주) | **극대화 (Scale-Out)** | **극대화 (Scale-Out)** |
| **SQL 인터페이스**| **표준 SQL 지원** | NoSQL / Proprietary API | **표준 SQL 100% 지원** |
| **합의 알고리즘** | 단일 Master 복제 | Gossip Protocol | **Raft / Paxos Consensus** |

#### 한줄 요약

- 둘 다 분산 SQL 거래를 제공하지만 배포 방식과 범위 배치•시간 순서 구현이 다르다.

## Ⅵ. 실무 고려사항 및 대책 (NewSQL 실무 도입 시 유의사항)

<details><summary>핵심 용어</summary>

- **Multi-Region Network Latency**: 여러 리전에 분산 노드가 흩어져 있을 경우 Raft/Paxos 합의 네트워크 왕복(RTT)으로 인해 쓰기 Latency가 수십 ms로 증가하는 현상.

</details>

| 고려사항 및 문제 | 위험 요소 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| Cross-Region 트랜잭션 시 RTT 네트워크 지연 폭증 | Paxos/Raft 합의 왕복시간 증대 | **Locality-aware Partitioning (지역 밀착형 핑 배치)** |
| 순차 증가 PK 사용 시 특정 Range로 쓰기 쏠림 | 단일 Range 노드 핫스팟 병목 | **PK에 Hash / UUID / TSID 조합으로 수평 분산** |
| 클럭 오차로 인한 HLC 시계 왜곡 | 트랜잭션 충돌 및 Retry 폭증 | **NTP 클럭 동기화 주기 단축 및 관리** |

> 사례: **토스뱅크 / 카카오페이 CockroachDB 기반 코어 뱅킹 Distributed SQL 운용**

#### 한줄 요약

- 함께 바꾸는 데이터를 가까이 두어 여러 지역을 오가는 합의 횟수를 줄인다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **NewSQL 수립 기준(NewSQL Architecture Standards)**: 100% Distributed ACID, Raft/Paxos 합의, HLC/TrueTime 시계열 및 Multi-Cloud 수용성에 의거한 체계.

</details>

- **NewSQL 수립 기준**에 따라 글로벌 대규모 트래픽 뱅킹/결제 시스템 구축 시 **CockroachDB / Spanner** 필수 수용

#### 한줄 요약

- NewSQL 적용 판단 기준은 분산 거래 가치와 합의 지연을 함께 비교한다.
