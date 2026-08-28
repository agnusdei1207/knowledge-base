---
sidebar:
  order: 108
  label: "108. Cassandra 컬럼 패밀리 데이터베이스"
  badge:
    text: "기출 · 30%"
    variant: note
title: "Cassandra 컬럼 패밀리 데이터베이스 (Cassandra Column Family)"
date: "2026-08-26T13:09:18+09:00"
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

<details><summary>용어 설명</summary>

- **Apache Cassandra**: Facebook이 개발하고 아파치에서 오픈소스화한 분산 Wide-Column 데이터베이스로, 완전한 P2P 마스터리스 링 아키텍처 지원.
- **Wide-Column Store**: 각 행(Row)마다 서로 다른 수와 종류의 동적 컬럼을 가질 수 있는 희소 행렬 기반 스토리지 모델.

</details>

- 정의/개념: 마스터리스(Masterless) P2P 링 구조에서 **파티션 키 기반 수평 분산과 LSM-Tree 쓰기 최적화 및 가변 일관성을 제공**하는 Wide-Column NoSQL
- 배경/필요성: 단일 마스터 구조는 모든 쓰기가 한 노드를 통과해 처리량이 그 노드 상한에 갇히고 리전 장애 시 승격이 끝날 때까지 쓰기가 멈추므로, 모든 노드가 동등한 P2P 링에서 파티션 키로 쓰기를 분산하고 일관성 수준을 요청 단위로 고르게 해 확장과 가용성을 함께 확보할 필요

#### 한줄 요약
- Cassandra는 조인과 임의 조건 질의를 포기하는 대가로 쓰기 확장과 무중단 가용성을 얻으므로, 테이블 설계가 데이터의 구조가 아니라 실행할 질의 하나하나에서 출발한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Query-Driven Modeling**: 조인을 지원하지 않으므로, 애플리케이션의 화면 조회 쿼리(1 Query)마다 전용 비정규화 테이블(1 Table)을 생성하는 모델링.
- **Tunable Consistency**: 쿼리마다 응답을 수신할 복제 노드 수($R+W>N$, Quorum)를 지정하여 가용성과 일관성의 균형을 동적으로 조절.

</details>

- 마스터가 없어 단일 장애점(SPOF)이 전혀 없는 **완전 대등 노드 P2P 링 아키텍처**
- CommitLog + MemTable + SSTable을 통한 **100% 순차 쓰기(Sequential I/O) 극대화**
- 파티션 키(분산 저장)와 클러스터링 키(물리 정렬)를 결합한 **복합 기본키(Primary Key) 구조**

#### 한줄 요약
- 마스터리스 P2P 링과 순차 쓰기 기반 스토리지 엔진으로 대규모 시계열 및 로그 쓰기를 초고속 처리한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Partition Key vs Clustering Key**: 데이터를 어느 노드에 저장할지 정하는 파티션 키와 노드 내부에서 정렬할 기준인 클러스터링 키.

</details>

```text
[Cassandra P2P 토큰 링 및 노드 내부 스토리지 구조]
|-- Masterless P2P 토큰 링 (Consistent Hashing Hash Ring)
|   |-- Node 1 (Token 0~1000) ◄──(Gossip Protocol 상태 교환)──► Node 2 (Token 1001~2000)
|   `-- Node 4 (Token 3001~4000) ◄─────────────────────────► Node 3 (Token 2001~3000)
`-- 노드 내부 쓰기 엔진 (LSM-Tree 구조)
    |-- CommitLog (디스크 순차 추가 Append-Only 로그: 크래시 복구용)
    |-- MemTable (인메모리 SkipList 정렬 버퍼)
    `-- SSTable (디스크 불변 정렬 파일: Flush 및 Background Compaction)
```

선의 의미: 계층 및 P2P 토큰 링으로 데이터 노드를 분산하고 노드 내부에서는 CommitLog와 MemTable로 순차 쓰기를 수행하는 구조

| 구성요소 | 책임 |
|:---|:---|
| 파티션 키 | 토큰 기반 **저장 노드 결정** |
| 클러스터링 키 | 파티션 내부 **물리 정렬** |
| 코디네이터 노드 | 복제 요청의 **분기·응답 취합** |
| LSM-Tree 엔진 | CommitLog·MemTable·**SSTable 순차 쓰기** |

#### 한줄 요약
- 파티션 키가 노드 배치를, 클러스터링 키가 파티션 내부 정렬을 결정하므로 두 키가 사실상 접근 경로 전부이며, 키에 없는 조건은 전 노드를 훑는 최악 비용으로만 처리된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Gossip Protocol**: 분산 노드 간에 1초마다 무작위 피어와 상태 정보를 교환하여 클러스터 토폴로지와 장애 여부를 감지하는 탈중앙 프로토콜.

</details>

```text
클라이언트가 임의의 노드에 CQL 쓰기 요청 접수
        │
   [코디네이터 지정] 요청을 수신한 해당 노드가 트랜잭션 코디네이터(Coordinator) 역할 수행
        │
   [토큰 계산] 파티션 키에 Murmur3Partitioner 적용하여 Hash Token 값 도출
        │
   [병렬 전송] 토큰 링 메타데이터 대조 후 대상 복제 노드 3대(Replica Factor=3)에 동시 전송
        │
   [QUORUM 검증] 설정된 일관성 수준(`ConsistencyLevel.QUORUM` = 2대) 응답 도달 확인
        │
   클라이언트에 1ms 이내 성공 반환 (복제본 불일치 시 백그라운드 Read Repair 수행)
```

#### 한줄 요약
- 정족수를 높이면 최신 값을 읽을 확률이 오르는 대신 응답이 가장 느린 복제 노드에 묶이므로, 일관성 수준의 선택이 곧 요청 단위로 지연 예산을 배분하는 결정이 된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RDBMS vs Cassandra**: 정규화된 테이블과 조인을 지원하는 RDBMS와 쿼리별 비정규화 테이블을 구성하는 Cassandra.

</details>

| 비교 항목 | RDBMS (관계형 데이터베이스) | Apache Cassandra (Wide-Column NoSQL) |
|:---|:---|:---|
| 아키텍처 모델 | **단일 Primary + 다수 Replica (마스터 의존)** | **완전 대등 노드 마스터리스 P2P 링 (SPOF Zero)** |
| 데이터 모델링 | **3NF 정규화 모델링 (다중 테이블 Join 지원)**| **쿼리 주도 비정규화 (1 Query = 1 Table, Join 불가)** |
| 쓰기 성능 (Write) | 보통 (디스크 블록 랜덤 I/O 발생) | **최고 (CommitLog + MemTable 100% 순차 I/O)** |
| 주요 제약사항 | 수평 확장의 물리적 한계 봉착 | **파티션 키 누락 시 전체 클러스터 풀스캔 폭망** |

#### 한줄 요약
- 복합 조인은 RDBMS, 단일 마스터 한계를 넘는 대규모 분산 쓰기는 Cassandra를 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Tombstone**: Cassandra에서 `DELETE` 수행 시 즉시 삭제되지 않고 생성되는 삭제 표식으로, 수만 개가 누적되면 SELECT 시 타임아웃 발생.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 파티션 키 없이 `SELECT` 조회 시 전체 클러스터 스캔 발생 | **조회 쿼리마다 파티션 키를 필수로 포함하는 테이블 전용 재설계** | 노드 스캔 폭사 방지 및 $O(1)$ 라우팅 |
| 대량 DELETE로 인한 묘비(Tombstone) 누적 및 쿼리 타임아웃 | **`gc_grace_seconds` 단축 및 Size-Tiered Compaction 스케줄 가동** | 묘비 조기 제거 및 읽기 성능 복원 |
| 특정 파티션에 수 GB 데이터 누적 (Hot Partition) | **파티션 키에 날짜/시간 버킷(`user_id + YYYYMM`) 결합 분할** | 파티션 크기 100MB 이내 균등 분산 |
| 노드 간 데이터 불일치 누적 | **Nodetool Repair 정기 실행 및 Read Repair 활성화** | 분산 복제본 간 100% 정합성 유지 |

#### 한줄 요약
- 파티션 키 필수 포함, 컴팩션 기반 묘비 정리, 시간 버킷 키 결합, Nodetool Repair로 운용한다.

## Ⅶ. 결론

- 대규모 쓰기는 **Cassandra**, 가용성은 **P2P 링** 선택

#### 한줄 요약
- Apache Cassandra는 마스터리스 P2P 아키텍처와 쿼리 주도 비정규화 모델링을 통해 무중단 대용량 쓰기를 완성하는 대표적인 Wide-Column NoSQL이다.
