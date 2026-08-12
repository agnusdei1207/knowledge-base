---
sidebar:
  order: 94
  label: "094. 클러스터드 인덱스•커버링 인덱스 (Clustered Covering Index)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "클러스터드 인덱스•커버링 인덱스 (Clustered Covering Index)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **Clustered Index (클러스터드 인덱스)**: 테이블의 실제 디스크 데이터 행(Data Page)이 인덱스 키 순서대로 물리 정렬되어 저장되는 인덱스로, 리프 노드가 곧 실제 데이터 페이지인 구조 (테이블당 단 1개만 존재 가능).
- **Covering Index (커버링 인덱스)**: 쿼리가 요청하는 모든 컬럼(`SELECT, WHERE, ORDER BY, GROUP BY`)이 인덱스 키 및 포함(Include) 컬럼 내에 100% 존재하여, 실제 데이터 페이지를 조회하는 디스크 I/O (Table Access / Key Lookup)를 전혀 수행하지 않고 인덱스 노드 탐색만으로 쿼리를 완결하는 기법.
- **Key Lookup / Bookmark Lookup**: 비클러스터드 인덱스 탐색 후, 인덱스에 없는 다른 컬럼 값을 가져오기 위해 실제 데이터 페이지를 PK/ROWID로 다시 찾아 들어가는 2차 디스크 I/O 행위.

</details>

- **정의**: 실제 데이터 행을 인덱스 순으로 디스크에 물리 정렬시키는 **클러스터드 인덱스(Clustered Index)** 와, 쿼리에 필요한 모든 컬럼을 인덱스 내에 포함시켜 테이블 재조회(`Key Lookup`)를 생략하는 **커버링 인덱스(Covering Index)** 기법.
- **필요성**: 대용량 데이터 환경에서 범위 검색(Range Scan) 및 임의 디스크 I/O 병목 극복, `Key Lookup` 2차 디스크 탐색 비용 소멸을 통한 쿼리 응답시간 최적화.

#### 한줄 요약

- 클러스터드는 자료를 색인 순서로 놓고, 커버링은 색인에 질문의 답까지 적어 원본 책을 다시 펼치지 않게 한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Physical Order Data Alignment (클러스터드의 물리적 정렬)**: PK 순서대로 물리 디스크 레코드가 연속 배치되어 순차 I/O 범위 검색에 압도적 우위.
- **Zero Table Access (커버링의 테이블 접근 소멸)**: `SELECT name FROM users WHERE age = 30` 쿼리에서 `Index(age, name)` 이 존재할 경우, 실제 `users` 데이터 페이지 접근 생략.

</details>

- **클러스터드 인덱스(Clustered Index)**: 물리적 디스크 정렬 구조로 범위 쿼리(Range Query) 성능 극대화, 테이블당 1개(PK 기반).
- **커버링 인덱스(Covering Index)**: 테이블 접근 없이 인덱스만으로 조회 완결(`Zero Key Lookup`), 실행 계획상 `Using index` 렌더링.
- **운영 Trade-off**: DML 발생 시 페이지 분할(Page Split) 및 인덱스 유지 비용 발생.

#### 한줄 요약

- 가까운 값을 한곳에 두면 범위를 빨리 읽고 필요한 답을 색인에 넣으면 원본 조회가 줄지만, 변경할 자료는 늘어난다.

## Ⅲ. 구조 및 구성요소 (Clustered Index vs Covering Index 동작 아키텍처)

<details><summary>핵심 용어</summary>

- **Using Index (MySQL Explain)**: 쿼리 실행 계획(EXPLAIN)에서 Extra 항목에 `Using index`가 표시되면 커버링 인덱스로 작동하여 디스크 테이블 조회가 생략되었음을 의미.

</details>

```text
[Clustered Index 구조]
 Root Node ──► Branch Node ──► Leaf Node (= 실제 테이블 Data Record Page 자체)

[Covering Index 구조]
 쿼리 요청: SELECT name, email FROM users WHERE age = 30;
 Index: Index(age, name, email)
 Leaf Node ──► [age=30, name='홍길동', email='hong@study.com'] (Key Lookup 없이 즉시 반환!)
```

선의 의미: Clustered Index는 리프 노드에 전체 데이터 레코드가 물리 정렬되고, Covering Index는 쿼리가 원하는 필드(name, email)가 인덱스 리프 노드에 이미 완비되어 테이블 2차 조회를 차단하는 아키텍처.

| 구분 (Category) | Clustered Index (클러스터드 인덱스) | Covering Index (커버링 인덱스) |
|:---|:---|:---|
| **핵심 기법 및 목적** | **실제 디스크 데이터 행의 물리적 순서 정렬** | **쿼리가 필요한 모든 컬럼을 인덱스에 포함** |
| **테이블 2차 조회** | **0회 (리프 노드가 데이터 행 자체임)** | **0회 (Key Lookup / Bookmark Lookup 생략)** |
| **실행 계획 표기** | Primary Key 범위 스캔 | **`Using index` (MySQL EXPLAIN)** |
| **생성 한계성** | **테이블당 오직 1개만 생성 가능 (PK)** | **쿼리 패턴에 맞춰 복수 개 지정 가능** |

#### 한줄 요약

- 인덱스 키와 포함 열로 원본 테이블 접근을 줄일지 판단한다.

## Ⅳ. 흐름도 (Covering Index 동작 파이프라인 및 Key Lookup 소멸 과정)

<details><summary>핵심 용어</summary>

- **Key Lookup Elimination**: 일반 인덱스(Non-Covering)는 인덱스 스캔 후 2차로 PK를 통해 실제 데이터 레코드를 읽어 오지만, 커버링 인덱스는 2차 렌더링 과정을 완전 제거.

</details>

```text
[General Index Search (Non-Covering)]
 Index Scan (age=30) ──► ROWID/PK 획득 ──► [Key Lookup: 디스크 Data Page 2차 읽기] ──► Result

[Covering Index Search]
 Index Scan (age=30, name, email) ──────────────────────────────────────────────────► Result
 (※ 2차 Key Lookup 디스크 접근 0회 소멸!)
```

### 동작 원리

1. **Non-Covering Case**: `Index(age)`만 존재 시, `SELECT age, name` 실행 시 `age`로 인덱스 스캔 후 `name`을 가져오기 위해 PK 기반으로 실제 테이블 디스크 2차 접근 (**Key Lookup 발생**).
2. **Covering Case**: `Index(age, name)` 복합 인덱스를 구성하면, `age`로 스캔 시 리프 노드에 `name`이 같이 존재하므로 디스크 2차 접근을 **전면 생략하고 인덱스 노드 상에서 즉시 반환**.

#### 한줄 요약

- 색인에 답이 모두 있으면 원본 테이블을 다시 읽지 않고 결과를 반환한다.

## Ⅴ. 종류 및 비교 (Clustered Index vs Non-Clustered Index vs Covering Index)

<details><summary>핵심 용어</summary>

- **Include Index (포함 인덱스)**: SQL Server/PostgreSQL 등에서 B+Tree 키는 `(age)`로만 구성하고, 부가 결과 컬럼 `(name, email)`은 리프 노드에만 저장(INCLUDE)하여 인덱스 크기를 최적화하는 커버링 기법.

</details>

| 비교 항목 | Clustered Index | Non-Clustered Index | Covering Index (상태적 기법) |
|:---|:---|:---|:---|
| 데이터 정렬 여부 | **물리 디스크 정렬 100%** | 인덱스 키만 논리 정렬 | 쿼리 대응 인덱스 상태 |
| Key Lookup 발생 | **발생 안 함 (0회)** | **발생함 (1회 이상 2차 I/O)**| **발생 안 함 (0회)** |
| 쿼리 의존성 | 독립적 물리 구조 | 독립적 보조 구조 | **특정 쿼리 컬럼 구성에 종속적** |
| 인덱스 크기 | 테이블 자체 크기와 동일 | 상대적 작음 | 컬럼 추가 시 인덱스 용량 증가 |

#### 한줄 요약

- 클러스터드는 책을 색인순으로 꽂는 방식이고, 커버링은 색인 자체에 필요한 답을 모두 적는 방식이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Page Split & DML Overhead**: Clustered Index 키(PK)로 무작위 UUID 등을 사용하거나, Covering Index에 너무 많은 컬럼을 담을 경우 인덱스 페이지 폭증 및 DML 성능 추락 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Clustered PK에 무작위 UUID 사용 시 삽입 마다 **Page Split (페이지 분할)** 폭증 | **Clustered PK는 반드시 Auto-Increment / TSID 등 순차 증가 키 지정** | Page Split 방지 |
| Covering Index를 만들기 위해 지나치게 많은 컬럼을 인덱스에 포함 | **자주 호출되는 대용량 초고속 쿼리(Top 5)에 한해서만 커버링 지정** | DML 쓰기 오버헤드 방지 |
| 실행 계획에서 커버링 인덱스가 동작하는지 검증 필요 | **`EXPLAIN` 실행 계획 상의 `Using index` 표기 유무 상시 모니터링**| 커버링 오작동 차단 |

> 사례: **MySQL InnoDB PK Auto-Increment Clustered Index & `Index(user_id, status, created_at)` 커버링 인덱스 적용**

#### 한줄 요약

- 원본 조회가 줄어든 만큼 인덱스 크기와 수정 비용이 늘지 않았는지 확인해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **인덱스 물리 구조 수립 기준(Index Physical Architecture Standards)**: Range Scan 쿼리 빈도, Key Lookup 소멸성 및 Page Split 방지성에 의거한 체계.

</details>

- **인덱스 물리 구조 수립 기준 적용** (대용량 OLTP 설계 시 순차 Clustered PK 및 초고속 쿼리 Covering Index 필수 수용)

#### 한줄 요약

- 인덱스 물리 설계 선택 기준으로 실제 읽기 감소와 쓰기 증가를 함께 확인한다.
