---
sidebar:
  order: 115
  label: "115. NewSQL: CockroachDB•Spanner"
  badge:
    text: "미출 · 50%"
    variant: note
title: "NewSQL: CockroachDB•Spanner (NewSQL)"
date: "2026-08-26T09:52:00+09:00"
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

<details><summary>용어 설명</summary>

- **NewSQL**: RDBMS의 엄격한 ACID 트랜잭션과 SQL 표준을 보장하면서 NoSQL의 무한한 수평 확장성(Scale-Out)을 결합한 차세대 분산 관계형 DB.
- **TrueTime API & HLC**: Google Spanner의 GPS/원자시계 하드웨어 기반 시간 동기화(TrueTime)와 CockroachDB의 소프트웨어 기반 하이브리드 논리 시계(HLC).

</details>

- 정의/개념: RDBMS의 엄격한 ACID 트랜잭션과 SQL 지원을 유지하면서 **NoSQL의 수평 확장성(Scale-Out)과 분산 합의(Raft/Paxos)를 결합**한 차세대 분산 관계형 데이터베이스
- 배경/필요성: 단일 RDBMS의 수평 확장 한계 및 NoSQL 도입 시 발생하는 **트랜잭션 정합성 결여와 애플리케이션 수동 샤딩 복잡도 해결 불가**

#### 한줄 요약
- 분산 합의와 논리 시계를 통해 분산 환경에서 100% ACID 트랜잭션과 수평 확장을 양립한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Distributed ACID**: 단일 노드가 아닌 네트워크로 분리된 다중 샤드/노드 간 트랜잭션에서도 완전한 ACID 직렬성을 보장.
- **Raft / Paxos Consensus**: 과반수 정족수 합의를 통해 분산 노드 간 로그 복제와 리더 선출을 무중단으로 수행.

</details>

- 표준 SQL 인터페이스 및 다중 노드에 걸친 **100% 분산 ACID 트랜잭션 보장**
- 노드 증설 시 데이터 범위를 자동으로 분할(Split)하는 **Shared-Nothing 수평 확장**
- 네트워크 분할 시에도 정합성을 지키는 **Raft / Paxos 합의 알고리즘 기반 고가용성**

#### 한줄 요약
- 분산 ACID, 자동 수평 샤딩, Raft 합의 엔진을 결합하여 완벽한 관계형 분산 처리를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Range / Region**: NewSQL에서 데이터를 키 순서대로 64MB 단위로 쪼갠 기본 분할 단위로, 각 Range마다 독립된 Raft 그룹을 형성.

</details>

```text
[NewSQL (CockroachDB / Spanner) 계층 아키텍처]
|-- SQL Execution Layer (PostgreSQL 호환 SQL 파서 및 분산 CBO 옵티마이저)
|-- Distributed Transaction Layer (2PC + MVCC + Concurrency Control)
|-- Raft Consensus Layer (Range별 독립 Raft 합의 복제 그룹: 3~5벌 복제)
`-- Distributed Storage Engine (Pebble / RocksDB 기반 LSM-Tree 순차 저장)
```

선의 의미: 계층 및 SQL 실행 계층부터 분산 트랜잭션, Raft 합의, LSM 스토리지로 이어지는 수직 계층 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| SQL 게이트웨이 | 표준 SQL 문법 파싱 및 **분산 질의 계획(Distributed Plan) 수립** | 분산 조인 및 셔플링 최적화 |
| 분산 트랜잭션 조정자 | 다중 Range 간 교차 커밋을 위해 **2PC 및 Lock-Free MVCC 격리성 제어** | Serializable 격리성 보장 |
| Raft 합의 복제 그룹 | 키 범위(Range)마다 독립된 Raft 그룹을 구성하여 **과반수 합의로 변경 로그 복제** | 노드 장애 시 3초 내 리더 재선출 |
| 분산 시계 (TrueTime/HLC) | 글로벌 분산 노드 간 시간 순서를 결정하여 **락 없는 스냅샷 읽기(Lock-Free Read) 실현**| Spanner(GPS), Cockroach(HLC) |

#### 한줄 요약
- SQL 게이트웨이, 분산 트랜잭션 조정자, Raft 합의 그룹, 분산 시계 엔진으로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Range Split & Commit 파이프라인**: 쿼리 접수 $\to$ Range 라우팅 $\to$ Raft 합의 커밋 $\to$ 64MB 초과 시 자동 분할(Split).

</details>

```text
클라이언트 분산 SQL 트랜잭션 요청 (`INSERT/UPDATE`)
        │
   [SQL 파싱 및 라우팅] 게이트웨이 노드가 SQL을 분석하여 대상 키 범위(Range) 리더 식별
        │
   [Raft 합의 쓰기] 대상 Range의 Raft 리더가 변경 로그를 팔로워 노드들에 병렬 전파
        │
   [정족수 커밋] 과반수(2/3) 노드 로그 기록 확인 후 Raft 리더가 로컬 디스크에 반영
        │
   [자동 분할(Split) 검사] 해당 Range 데이터가 64MB를 초과했는가?
   ┌────┴───────────────────────────┐
  예 (용량 임계치 초과)             아니오 (용량 여유 있음)
   │                                 │
32MB 단위로 Range 자동 분할 및   클라이언트에 분산 트랜잭션 완료 응답
타 노드로 청크 자동 리밸런싱
```

#### 한줄 요약
- SQL 분석 → Range 라우팅 → Raft 과반 합의 → 로컬 반영 → 필요 시 자동 분할 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Traditional RDBMS vs NoSQL vs NewSQL**: 관계형 모델(RDBMS), 수평 확장(NoSQL), 두 장점의 결합(NewSQL).

</details>

| 비교 항목 | 전통적 RDBMS (MySQL, Oracle) | 분산 NoSQL (Cassandra, MongoDB) | 차세대 NewSQL (CockroachDB, Spanner) |
|:---|:---|:---|:---|
| 트랜잭션 모델 | **단일 노드 엄격한 ACID** | 최종 일관성 (BASE 위주) | **글로벌 100% 분산 ACID (Strict)** |
| 수평 확장성 | 수직 확장(Scale-Up) 중심 | **수평 분산 확장(Scale-Out) 최적화** | **무제한 자동 수평 분산 확장 (Scale-Out)** |
| 질의 인터페이스 | **표준 SQL 및 복합 Join 지원** | 자체 전용 API 또는 제한적 질의 | **표준 SQL 및 분산 Join 완전 지원** |
| 합의/복제 메커니즘| Master-Replica 비동기/반동기 | Gossip 프로토콜 / Quorum | **Raft / Paxos 과반수 합의 알고리즘** |

#### 한줄 요약
- 금융 원장의 무결성과 클라우드 수평 확장이 모두 필요할 때 NewSQL을 최종 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Locality-Aware Partitioning**: 글로벌 다중 리전 환경에서 데이터가 주로 소비되는 물리 리전 노드에 데이터를 인접 배치하는 최적화 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 멀티 리전 간 분산 트랜잭션 시 네트워크 RTT 왕복 지연 폭증 | **지역 밀착형 파티셔닝(Locality-Aware Partitioning) 적용** | 크로스 리전 합의 지연 80% 절감 |
| 순차 증가 PK(`AUTO_INCREMENT`) 사용 시 특정 Range 핫스팟 | **UUIDv4 또는 Hash 기반 복합 Shard Key로 기본키 설계** | 클러스터 전체 노드에 균등 분산 |
| 클럭 오차로 인한 HLC 시계 왜곡 및 트랜잭션 재시도 급증 | **PTP(Precision Time Protocol) 또는 NTP 주기 10ms 이하 단축**| 트랜잭션 충돌 및 재시도 최소화 |
| 대규모 분산 조인 시 대역폭 병목 | **Colocated Table(부모-자식 Range 동시 배치) 구조화** | 네트워크 셔플링 제로화 |

#### 한줄 요약
- 지역 밀착 파티셔닝, UUID 기본키, NTP 정밀 동기화, Colocated 테이블로 분산 성능을 최적화한다.

## Ⅶ. 결론

- 글로벌 확장은 **NewSQL**, 정합성 보장은 **Raft** 선택

#### 한줄 요약
- NewSQL은 RDBMS의 강력한 정합성과 NoSQL의 무한한 수평 확장을 결합하여 차세대 글로벌 트랜잭션 시스템을 주도하는 분산 데이터베이스다.