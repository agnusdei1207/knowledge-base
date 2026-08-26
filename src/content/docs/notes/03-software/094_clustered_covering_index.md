---
sidebar:
  order: 94
  label: "094. 클러스터드•커버링 인덱스"
  badge:
    text: "기출 · 70%"
    variant: note
title: "클러스터드 인덱스•커버링 인덱스 (Clustered Covering Index)"
date: "2026-08-27T01:44:00+09:00"
tags:
  - "notes-software"
weight: 94
extra:
  question_no: "094"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "137회 기출, 클러스터•커버링 인덱스 설계"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **클러스터드 인덱스(Clustered Index)**: 실제 데이터 레코드 자체가 인덱스 키(PK) 순서대로 디스크 페이지에 물리적으로 정렬되어 저장되는 인덱스 (테이블당 1개).
- **커버링 인덱스(Covering Index)**: SQL 질의에 필요한 모든 컬럼이 인덱스에 포함되어 있어, 실제 테이블 데이터 블록을 읽는 Key Lookup을 생략하는 쿼리 최적화 상태.

</details>

- 정의/개념: 데이터 행을 키 순서대로 디스크에 물리 정렬하는 **클러스터드 인덱스와 Key Lookup 없이 인덱스만으로 질의를 완결하는 커버링 인덱스**의 최적화 기술
- 배경/필요성: 잦은 범위 검색 및 2차 테이블 접근(Key Lookup) 반복으로 인한 **랜덤 I/O 급증 및 쿼리 응답 시간 지연 해결 불가**

#### 한줄 요약
- 데이터 물리 정렬(클러스터드)과 2차 테이블 접근 제거(커버링)로 디스크 I/O를 극소화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Key Lookup(Bookmark Lookup)**: 보조 인덱스 탐색 후, 인덱스에 없는 나머지 컬럼을 가져오기 위해 PK로 실제 테이블 데이터 블록을 찾는 랜덤 I/O 작업.
- **Using index(실행 계획)**: MySQL `EXPLAIN` 실행 계획의 Extra 컬럼에 표기되어 테이블 접근 없이 인덱스만으로 쿼리가 처리되었음을 입증.

</details>

- 데이터 페이지 자체가 기본키 순서로 물리 정렬되는 **테이블당 단 1개의 클러스터드 인덱스**
- 쿼리에 필요한 모든 컬럼을 인덱스 리프에 완비하여 **Key Lookup을 0으로 만드는 커버링 인덱스**
- 대규모 범위 검색(Range Scan) 및 초고빈도 조회의 **디스크 랜덤 I/O 90% 이상 절감**

#### 한줄 요약
- 물리적 순차 I/O 활용과 2차 테이블 룩업 제거를 통해 대용량 조회 성능을 극대화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **클러스터드 vs 커버링 구조**: 리프 노드가 실제 데이터 행인 클러스터드 인덱스와 인덱스 리프 노드에 요청 컬럼이 모두 캐싱된 커버링 인덱스.

</details>

| 구성요소 | 책임 | I/O 최적화 메커니즘 |
|:---|:---|:---|
| 클러스터드 인덱스 | 데이터 행을 키 순서대로 디스크에 정렬하여 **범위 검색(BETWEEN, <, >) 속도 극대화** | 리프 노드가 곧 실제 데이터 페이지 (테이블당 1개) |
| 커버링 인덱스 | SELECT/WHERE/ORDER BY 컬럼을 인덱스에 포함하여 **2차 Table Access(Key Lookup) 완전 생략** | 실행 계획 Extra에 `Using index` 표시 |
| 포함 컬럼 (INCLUDE) | B+Tree 정렬 키가 아닌 부가 컬럼을 **리프 노드에만 저장하여 인덱스 크기 최적화** | PostgreSQL, MSSQL `CREATE INDEX ... INCLUDE` |
| 보조 인덱스 포인터 | InnoDB 보조 인덱스는 ROWID 대신 **클러스터드 PK 값을 포인터로 보관** | PK 변경 시 모든 보조 인덱스 영향 받음 |

#### 한줄 요약
- 클러스터드는 데이터 물리 정렬을, 커버링은 테이블 접근 제거를 전담하여 디스크 I/O를 최소화한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Zero Key Lookup**: 보조 인덱스 리프 노드에 필요한 모든 데이터가 존재하여 실제 테이블 데이터 블록을 읽는 디스크 I/O를 완전히 건너뛰는 상태.

</details>

```text
클라이언트 SQL 질의 인입 (`SELECT user_id, name, email FROM Users WHERE age = 30`)
        │
   [실행 계획 분석] CBO 옵티마이저가 인덱스 `idx_users_covering(age, user_id, name, email)` 확인
        │
   [컬럼 대조] SELECT 및 WHERE의 모든 컬럼이 인덱스 키에 100% 포함되어 있는가?
   ┌────┴───────────────────────────┐
  예 (커버링 인덱스 성립)            아니오 (일반 보조 인덱스)
   │                                 │
[인덱스 리프 스캔]                [인덱스 스캔 후 Key Lookup]
리프 노드에서 컬럼 즉시 인출        추출된 PK로 테이블 블록 2차 랜덤 I/O 수행
(Table Access Zero!)              (디스크 I/O 병목 발생)
        │                                 │
   클라이언트에 결과 즉시 반환 (`Using index`)
```

#### 한줄 요약
- 질의 접수 → 인덱스 컬럼 대조 → 커버링 판정 → Zero Key Lookup 리프 즉시 반환 순으로 처리된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Clustered vs Non-Clustered vs Covering**: 물리 저장 방식(Clustered/Non-Clustered)과 쿼리 만족 상태(Covering Index) 비교.

</details>

| 비교 항목 | 클러스터드 인덱스 (Clustered) | 일반 보조 인덱스 (Non-Clustered) | 커버링 인덱스 (Covering) |
|:---|:---|:---|:---|
| 테이블당 개수 | **단 1개만 생성 가능 (PK)** | 다수 생성 가능 (수 개~십수 개) | 쿼리별 조합 상태 (복수 가능) |
| 리프 노드 내용 | **실제 테이블 데이터 레코드 전체** | 인덱스 키 컬럼 + PK 포인터 | **쿼리가 요구하는 모든 컬럼 집합** |
| 2차 테이블 룩업 | 없음 (리프가 데이터) | **발생 (Key Lookup 랜덤 I/O)** | **완전 생략 (Using index)** |
| 쿼리 최적화 효과 | 범위 검색, PK 기반 단건 조회 | 특정 조건 탐색 가속 | **초고빈도 대규모 조회 쿼리 극대화** |

#### 한줄 요약
- 클러스터드는 테이블 물리 정렬, 보조 인덱스는 포인터 기반, 커버링은 테이블 조회를 생략하는 최적화 상태다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Random UUID PK 안티패턴**: 클러스터드 인덱스 키로 무작위 UUID를 사용할 경우 매번 페이지 중간에 삽입되어 빈번한 Page Split과 디스크 단편화를 유발하는 문제.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Clustered PK에 무작위 UUID 사용 시 빈번한 Page Split 발생 | **순차 증가하는 Auto-Increment ID 또는 TSID(Time-Sorted) 채택** | 순차 I/O 보장 및 페이지 단편화 방지 |
| 커버링 인덱스를 위해 과도하게 많은 컬럼 추가로 크기 폭증 | **INCLUDE 절(PostgreSQL) 활용 및 핵심 Top 5 쿼리 위주 한정 적용** | 인덱스 크기 팽창 억제 및 DML 비용 최소화 |
| 커버링 인덱스를 의도했으나 실행 계획에서 Key Lookup 발생 | **`EXPLAIN` 실행 계획 상의 `Using index` 표기 여부 상시 모니터링** | 비효율적 2차 테이블 조회 조기 차단 |
| `SELECT *` 남발로 인한 커버링 인덱스 무력화 | **필요한 컬럼만 명시적으로 SELECT하는 쿼리 작성 원칙 준수** | 커버링 인덱스 100% 활용 |

#### 한줄 요약
- 순차 PK 설계, INCLUDE 컬럼 활용, `Using index` 모니터링, `SELECT *` 금지로 성능을 극대화한다.

## Ⅶ. 결론

- 범위 정렬은 **클러스터드**, 룩업 제거는 **커버링 인덱스** 선택

#### 한줄 요약
- 클러스터드 인덱스와 커버링 인덱스는 물리적 순차 I/O와 테이블 룩업 제거를 통해 데이터베이스 디스크 I/O를 최소화하는 최상위 인덱스 최적화 기술이다.
