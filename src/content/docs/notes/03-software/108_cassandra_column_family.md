---
sidebar:
  order: 108
  label: "108. Cassandra 컬럼 패밀리 데이터베이스 (Cassandra Column Family)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "Cassandra 컬럼 패밀리 데이터베이스 (Cassandra Column Family)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 108
extra:
  question_no: "108"
  source_status: "기출"
  source_history: "137회"
  priority: 30
  priority_note: "137회 기출, 컬럼 패밀리 제품 사례 성격"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Apache Cassandra**: Master 노드가 전혀 없는 완전한 피어-투-피어(Peer-to-Peer Ring) 아키텍처 기반의 대용량 분산 Wide-Column Store NoSQL 데이터베이스.
- **Masterless P2P Architecture**: 마스터-슬레이브 구조의 단일 장애점(SPOF)을 제거하고, 클러스터 내 모든 노드가 동일한 권한으로 쿼리 분산과 데이터 저장을 분담하는 아키텍처.
- **Tunable Consistency (조정 가능한 일관성)**: 쿼리 실행 시 일관성 레벨(Consistency Level: `ONE`, `QUORUM`, `ALL`)을 지정하여 CAP 정리상의 AP와 CP 성격을 가변 선택할 수 있는 파라미터.

</details>

- 정의/개념: 마스터 노드가 없는 P2P 해시 링 구조에서 Partition Key 기반으로 대용량 데이터를 수평 분산하고, 쓰기 성능을 극대화한 Wide-Column NoSQL인 **Apache Cassandra**
- 배경/필요성: 단일 마스터 복제 구조의 쓰기 bottleneck 및 SPOF(단일 장애점) 차단, IoT 시계열 데이터 및 SNS 메시징의 초고속 덧붙이기(Append-Only) 수용 요구성

#### 한줄 요약

- 조회할 묶음을 정해 균등 분산하고 시간순으로 쌓는 저장소이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Query-Driven Modeling**: RDBMS의 정규화와 달리, 오직 애플리케이션의 쿼리 패밀리(Query Table) 패턴에 맞춰 테이블을 각각 비정규화(Denormalization) 설계.
- **Append-Only Write Mechanics**: CommitLog + MemTable + SSTable 구조를 활용해 100% 순차 디스크 I/O(Sequential Write)로 쓰기 처리량 극대화.

</details>

- **Masterless Ring Architecture (SPOF 0%, 무제한 Scale-Out)**
- **Query-Driven Data Modeling (Partition Key + Clustering Key)**
- **LSM-Tree 형태의 CommitLog + MemTable + SSTable 쓰기 파이프라인**

#### 한줄 요약

- 쓰기와 장애 내성은 높지만 파티션 키를 벗어난 조회에는 부적합하다.

## Ⅲ. 구조 및 구성요소 (Partition Key 대 Clustering Key & 쓰기 엔진)

<details><summary>핵심 용어</summary>

- **Partition Key**: 데이터를 어느 물리적 노드(Shard Ring)에 분산 저장할지 결정하는 해시 키.
- **Clustering Key**: 동일 파티션 노드 내부에서 데이터를 물리적으로 정렬(ASC/DESC)해 두는 정렬 키.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                    Cassandra Data Modeling & Architecture              │
├────────────────────────────────────────────────────────────────────────┤
│ Primary Key = (Partition Key, Clustering Key 1, Clustering Key 2)      │
│  • Partition Key: 'user_id' ──► Hash Ring 상의 물리 노드 결정          │
│  • Clustering Key: 'created_at' ──► 노드 디스크 내 시계열 자동 정렬     │
├────────────────────────────────────────────────────────────────────────┤
│ Client Write ──► [Coordinator Node] ──► Gossip Protocol ──► [Replica Nodes]│
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Partition Key로 물리 노드를 결정하고 Clustering Key로 노드 내 시계열을 정렬하며, Coordinator 노드가 Gossip 프로토콜로 레플리카에 전파하는 구조.

| 구성요소 / 지표 | 역할 및 주요 메커니즘 | 실무 튜닝 지침 |
|:---|:---|:---|
| **Partition Key** | 해시 링 상에서 물리적 노드 위치 결정 | 데이터 편향(Data Skew) 없는 고선택성 필드 지정 |
| **Clustering Key** | 파티션 내부 튜플 물리적 정렬 순서 결정 | 시계열(`created_at`) 배치로 범위 검색 극대화 |
| **MemTable & SSTable**| 메모리 버퍼 및 디스크 불변 정렬 파일 | **LSM-Tree 기반 순차 쓰기(Sequential I/O)** |
| **CommitLog** | 복구용 순차 쓰기 디스크 로그 파일 | MemTable 쓰기 전 선행 영속화 보장 |

#### 한줄 요약

- 배치 키, 접수자, 쓰기 기록, 정렬 파일, 사본 수선으로 구성된다.

## Ⅳ. 흐름도 (Cassandra Tunable Consistency: $R + W > N$)

<details><summary>핵심 용어</summary>

- **Quorum Consistency Equation ($R + W > N$)**: 읽기 복제본 수($R$) + 쓰기 복제본 수($W$) > 총 복제 계수($N$) 조건을 충족하면 항상 가장 최신의 데이터를 읽을 수 있음을 보증하는 수식.

</details>

```text
[Replication Factor N = 3]
  • Write Level  (W) = QUORUM (2개 노드 성공 응답)
  • Read Level   (R) = QUORUM (2개 노드 데이터 비교)
  ──► (R=2) + (W=2) = 4 > (N=3) ──► Strong Consistency (강한 일관성 달성!)
```

### 동작 원리

1. **Client Request**: Coordinator 노드가 쿼리 수신.
2. **Quorum Write**: 3개 복제 노드 중 과반수인 2개 노드(W=2)에 쓰기 완료 시 성공 반환.
3. **Quorum Read**: 2개 노드(R=2)에서 데이터를 읽어 겹치는 최신 타임스탬프 값을 렌더링 (**R+W>N 조건에 의해 100% 최신 데이터 보장**).

#### 한줄 요약

- 모든 담당 사본에 쓰기를 보내되 몇 곳의 확인을 기다릴지는 요청마다 정한다.

## Ⅴ. 종류 및 비교 (RDBMS vs Cassandra 데이터 모델링)

<details><summary>핵심 용어</summary>

- **Denormalization in Cassandra**: Cassandra는 조인(`JOIN`)이 없으므로, 쿼리 화면 1개당 테이블 1개를 만들어 동일한 데이터를 중복 저장하는 비정규화가 표준 지침.

</details>

| 비교 항목 | RDBMS (Relational Database) | Apache Cassandra (Wide-Column) |
|:---|:---|:---|
| 데이터 모델링 기준| **엔티티 관계 중심 정규화 (1NF, 2NF, 3NF)**| **화면 쿼리 중심 비정규화 (1 Table per Query)** |
| `JOIN` 연산 지원 | **전면 지원 (Inner, Outer, Subquery)** | **절대 지원 불가 (`JOIN` 0회)** |
| 수평 확장성 | 고비용 분산 아키텍처 (샤딩 필요) | **무제한 수평 Scale-Out (P2P Ring 노드 추가)** |
| 쓰기 메커니즘 | In-Place Update (Random Write I/O) | **LSM-Tree Out-of-Place (Sequential I/O)** |

#### 한줄 요약

- 적게 기다리면 빠르고 잘 버티며, 많이 기다리면 최신 확인 범위가 넓어진다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Tombstone Threshold Overwrite**: DELETE 연산 시 생성되는 묘비(Tombstone)가 파티션 내 수만 개 쌓이면 `SELECT` 스캔 시 읽기 타임아웃 장애가 발생하므로 주기적 Compaction 필수.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Partition Key 없이 `SELECT` 조회 시 전체 노드 Scan 폭사 | **모든 쿼리에 Partition Key 필수 포함 및 테이블 재설계**| 핫스팟/Scan 방지 |
| 삭제 데이터가 디스크에 묘비(**Tombstone**)로 쌓여 읽기 타임아웃 | **`gc_grace_seconds` 튜닝 및 Size-Tiered Compaction 실행**| Tombstone 청소 |
| 특정 Partition Key 용량 폭증 (Hot Partition) | **Partition Key에 날짜/시간 버킷(`user_id + YYYYMM`) 추가** | 균등 수평 분산 |

> 사례: **넷플릭스 / 시스코 시계열 로그 및 유저 시청 이력 저장소로 Cassandra 운용**

#### 한줄 요약

- 장치와 날짜로 서랍을 나누면 한 서랍이 끝없이 커지지 않고 시간순으로 읽을 수 있다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Cassandra 수립 기준(Cassandra Design Standards)**: Masterless P2P 노드 구성, Query-Driven Data Modeling 및 $R+W>N$ Tunable Consistency에 의거한 체계.

</details>

- **Cassandra 수립 기준**에 따라 대용량 시계열/메시징 DB 구축 시 **P2P Ring & Query-Driven Modeling** 필수 수용

#### 한줄 요약

- Cassandra 모델 적용 기준은 키 분배와 파일•사본 정리를 함께 다룬다.
