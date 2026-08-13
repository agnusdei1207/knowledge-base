---
sidebar:
  order: 108
  label: "108. Cassandra 컬럼 패밀리 데이터베이스 (Cassandra Column Family)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "Cassandra 컬럼 패밀리 데이터베이스 (Cassandra Column Family)"
date: "2026-08-13T21:14:00+09:00"
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
- 배경/필요성: 단일 주 노드 구조는 **쓰기 병목•장애 집중** 유발

#### 한줄 요약

- 조회할 묶음을 정해 균등 분산하고 시간순으로 쌓는 저장소이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Query-Driven Modeling**: RDBMS의 정규화와 달리, 오직 애플리케이션의 쿼리 패밀리(Query Table) 패턴에 맞춰 테이블을 각각 비정규화(Denormalization) 설계.
- **Append-Only Write Mechanics**: CommitLog + MemTable + SSTable 구조를 활용해 100% 순차 디스크 I/O(Sequential Write)로 쓰기 처리량 극대화.

</details>

- **Masterless Ring Architecture**: 대등 노드 기반 분산•확장
- **Query-Driven Data Modeling (Partition Key + Clustering Key)**
- **LSM-Tree 형태의 CommitLog + MemTable + SSTable 쓰기 파이프라인**

#### 한줄 요약

- 쓰기와 장애 내성은 높지만 파티션 키를 벗어난 조회에는 부적합하다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Partition Key**: 데이터를 어느 물리적 노드(Shard Ring)에 분산 저장할지 결정하는 해시 키.
- **Clustering Key**: 동일 파티션 노드 내부에서 데이터를 물리적으로 정렬(ASC/DESC)해 두는 정렬 키.

</details>

```text
[파티션 키] ───── [토큰 링]
     │                │
[코디네이터] ─── [복제 노드]
     │                │
[CommitLog] ──── [MemTable•SSTable]
```

선의 의미: 키 배치•요청 조정•복제•LSM 저장 책임의 정적 관계.

| 구성요소 | 책임 |
|:---|:---|
| **파티션 키** | 토큰으로 데이터 배치 노드 결정 |
| **토큰 링** | 노드별 토큰 범위와 복제 위치 관리 |
| **코디네이터** | 요청을 복제 노드에 전달하고 응답 취합 |
| **복제 노드** | 복제 계수에 따라 파티션 사본 보관 |
| **CommitLog** | 쓰기 복구를 위한 변경 기록 |
| **MemTable•SSTable** | 메모리 적재 후 불변 파일로 플러시 |

#### 한줄 요약

- 배치 키, 접수자, 쓰기 기록, 정렬 파일, 사본 수선으로 구성된다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Quorum Consistency Equation ($R + W > N$)**: 읽기 복제본 수($R$) + 쓰기 복제본 수($W$) > 총 복제 계수($N$) 조건을 충족하면 항상 가장 최신의 데이터를 읽을 수 있음을 보증하는 수식.

</details>

```text
[클라이언트 요청]
       │
       ▼
1. 코디네이터 선택
       │
       ▼
2. 파티션 토큰 계산
       │
       ▼
3. 복제 노드 요청
       │
       ▼
4. 일관성 수준 판정
       │
       ▼
5. 응답 취합
       │
       ▼
  [결과 반환]
```

### 동작 원리

1. **코디네이터 선택**: 접속 노드가 요청 조정 역할 수행
2. **파티션 토큰 계산**: 키 해시로 담당 범위 식별
3. **복제 노드 요청**: 복제 계수에 따른 노드로 전달
4. **일관성 수준 판정**: ONE•QUORUM•ALL 충족 확인
5. **응답 취합**: 최신 타임스탬프 비교와 복구 수행

#### 한줄 요약

- 모든 담당 사본에 쓰기를 보내되 몇 곳의 확인을 기다릴지는 요청마다 정한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Denormalization in Cassandra**: Cassandra는 조인(`JOIN`)이 없으므로, 쿼리 화면 1개당 테이블 1개를 만들어 동일한 데이터를 중복 저장하는 비정규화가 표준 지침.

</details>

| 비교 항목 | RDBMS (Relational Database) | Apache Cassandra (Wide-Column) |
|:---|:---|:---|
| 데이터 모델링 기준| **엔티티 관계 중심 정규화 (1NF, 2NF, 3NF)**| **화면 쿼리 중심 비정규화 (1 Table per Query)** |
| 관계 결합 | **DBMS 조인•서브쿼리 지원** | 쿼리별 비정규화 테이블 설계 |
| 수평 확장성 | 제품•구성별 분산 방식 적용 | **P2P 링 노드 추가와 재분배** |
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

- 파티션 키로 닫히는 대규모 쓰기는 **Cassandra**, 임의 조인은 RDBMS 선택

#### 한줄 요약

- Cassandra 모델 적용 기준은 키 분배와 파일•사본 정리를 함께 다룬다.
