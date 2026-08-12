---
sidebar:
  order: 93
  label: "093. 인덱스 구조: B+Tree•해시•복합 (Index Structure)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "인덱스 구조: B+Tree•해시•복합 (Index Structure)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 93
extra:
  question_no: "093"
  source_status: "기출"
  source_history: "122회, 135회, 137회"
  priority: 70
  priority_note: "122•135•137회 반복, 인덱스 선택 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Database Index (데이터베이스 인덱스)**: 테이블 검색 속도(Read Latency)를 향상시키기 위해 특정 컬럼의 키-포인터 쌍을 정렬된 별도 자료구조로 생성하여, Full Table Scan 대신 $\mathcal{O}(\log N)$ 또는 $\mathcal{O}(1)$ 탐색을 가능케 하는 검색 전용 보조 자료구조.
- **Selectivity (선택도)**: 전체 행(Tuple) 수 중 해당 컬럼 조건으로 필터링되는 튜플의 비율 ($\text{Selectivity} = \text{Unique Values} / \text{Total Rows}$). 선택도가 높을수록(1에 가까울수록/변별력이 클수록) 인덱스 효율 극대화.
- **Index Scan vs Full Table Scan**: 선택도가 높은 쿼리는 인덱스를 통해 디스크 I/O를 최소화(Index Scan), 반대로 전체 튜플의 15~20% 이상을 읽을 때는 옵티마이저가 차라리 테이블 전체를 읽는 Full Scan을 선택.

</details>

- 정의/개념: 테이블 검색 속도를 향상시키기 위해 특정 컬럼의 키와 행 위치 포인터(ROWID / PK)를 정렬된 자료구조로 추출하여 디스크 I/O를 획기적으로 줄이는 물리적 보조 구조인 **Database Index**
- 배경/필요성: 대용량 데이터베이스에서 Full Table Scan으로 인한 쿼리 응답시간 폭증 해소, $O(\log N)$ 단위의 빠른 탐색 및 `WHERE, JOIN, ORDER BY` 연산 최적화 요구성

#### 한줄 요약

- 책 전체를 넘기지 않고 색인에서 단어를 찾아 해당 쪽으로 이동하는 구조와 같다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **B+Tree Index**: 모든 리프 노드(Leaf Node)가 순차 연결(Doubly Linked List)되어 있어 범위 검색(Range Scan) 및 등가 검색(Equal Scan)에 모두 탁월한 상용 RDBMS 표준 인덱스.
- **Hash Index**: Key 값의 해시 함수 결과(Bucket Address)를 통해 동등 비교(`=`)를 $O(1)$ 속도로 찾지만, 범위원(Range) 및 정렬(`ORDER BY`) 탐색이 절대 불가능한 구조.
- **Composite Index (복합 인덱스)**: 2개 이상의 컬럼을 조합하여 만든 인덱스로, 컬럼의 선서(Order)가 인덱스 타넘기(Index Skip Scan / Range Scan)를 결정하는 인덱스.

</details>

- **High Selectivity (높은 선택도/변별력)** 컬럼 우선 지정
- **B+Tree (범위/정렬 최적화)** 대 **Hash (동등 비교 최적화)** 대 **Composite (다중 컬럼 조합)**
- **Write Overhead (DML 수정 시 인덱스 재정렬 비용 발생)** Trade-off

#### 한줄 요약

- 정렬된 색인은 구간을 찾고 해시는 같은 값만 빠르게 찾으며, 복합 색인은 앞 열부터 조건이 맞아야 효과가 크다.

## Ⅲ. 구조 및 구성요소 (B+Tree vs Hash vs Composite Index 구조)

<details><summary>핵심 용어</summary>

- **Root Node $\rightarrow$ Branch Node $\rightarrow$ Leaf Node**: B+Tree의 3단계 노드 레이어로, 오직 Leaf Node에만 실제 데이터 포인터(ROWID)와 순차 리스트가 존재.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        B+Tree Index Structure                          │
├────────────────────────────────────────────────────────────────────────┤
│                       [Root Node (Key: 50)]                            │
│                      /                     \                           │
│          [Branch Node (Key: 20)]        [Branch Node (Key: 80)]        │
│          /                     \        /                     \        │
│   [Leaf: 10,15] ◄───────────► [Leaf: 20,30] ◄───────────► [Leaf: 80,90]  │
│   (Row Location)              (Row Location)              (Row Location)│
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: B+Tree의 루트-브랜치를 거쳐 최하단 리프 노드에 도달하고, 리프 노드끼리 양방향 링크드 리스트로 연결되어 범위 검색(Range Scan)을 지원하는 아키텍처.

| 인덱스 구조 종류 | 데이터 탐색 복잡도 | 주요 특징 및 적합 연산 |
|:---|:---|:---|
| **B+Tree Index** | **$\mathcal{O}(\log N)$** | **범위 검색 (`BETWEEN, >, <`), 정렬 (`ORDER BY`), 동등 검색 (`=`) 모두 지원 (RDBMS 표준)** |
| **Hash Index** | **$\mathcal{O}(1)$** | **오직 동등 비교 (`=`) 전용**, 범위/정렬 탐색 불가능 (Memory DB / Redis 등) |
| **Composite Index** | **$\mathcal{O}(\log N)$** | **다중 컬럼 조합 인덱스**, 첫 번째 컬럼의 선두 지정(Leading Column)이 필수적 |

#### 한줄 요약

- 질의 조건과 통계로 색인 사용 비용을 계산해 행 위치를 찾는다.

## Ⅳ. 흐름도 (Composite Index 컬럼 순서 배열 원칙)

<details><summary>핵심 용어</summary>

- **Leading Column Principle**: 복합 인덱스 생성 시, `WHERE` 절에서 동등 비교(`=`)로 자주 쓰이고 선택도(Selectivity)가 가장 높은 컬럼을 제일 앞에(Leading) 배치해야 인덱스 스캔 가능.

</details>

```text
[복합 인덱스 컬럼 배열 4대 원칙]
       │
       ├─► 1. WHERE 절에 동등 비교(`=`)로 자주 쓰이는 컬럼을 선두(1순위) 배정
       ├─► 2. 선택도(Selectivity)가 높아 변별력이 뛰어난 컬럼을 앞쪽에 배치
       ├─► 3. 범위 검색(`BETWEEN, LIKE, >`) 컬럼은 뒤쪽에 배치 (앞 배치 시 뒤 컬럼 인덱스 소멸)
       └─► 4. ORDER BY / GROUP BY 컬럼을 연이어 배치하여 정렬 오버헤드(Sort Avoidance) 소멸
```

### 동작 원리

1. **Equal Condition First**: `WHERE status = 'ACTIVE' AND age >= 30` 쿼리 시, 동등 조건인 `status`를 1번 컬럼으로 지정.
2. **Range Condition Last**: 범위 조건인 `age`를 2번 컬럼으로 지정 (`Index(status, age)`).
3. **Sort Avoidance**: `ORDER BY created_at`이 수반될 경우 `Index(status, age, created_at)` 순으로 결합하여 별도 DB 정렬(Sort) 연산 전면 생략.

#### 한줄 요약

- 안내자가 자료 분포를 보고 색인이 더 빠를 때만 색인을 거쳐 실제 자료를 찾는다.

## Ⅴ. 종류 및 비교 (Clustered Index 대 Non-Clustered Index)

<details><summary>핵심 용어</summary>

- **Clustered Index (클러스터형)**: PK 기반으로 실제 데이터 행 자체가 인덱스 키 순서대로 디스크에 물리 정렬된 구조 (테이블당 1개).
- **Non-Clustered Index (보조/비클러스터형)**: 실제 데이터는 무순서로 두고, 키와 데이터 포인터(PK/ROWID)만 정렬 보존한 보조 인덱스 (테이블당 여러 개).

</details>

| 비교 항목 | Clustered Index (클러스터형) | Non-Clustered / Secondary Index (보조형) |
|:---|:---|:---|
| 데이터 물리 정렬| **실제 디스크 데이터 행이 인덱스 키 순으로 정렬** | **인덱스만 정렬되고 실제 데이터는 무순서** |
| 테이블당 개수 | **테이블당 단 1개만 존재 가능 (Primary Key)** | **테이블당 여러 개 생성 가능 (Secondary)** |
| 리프 노드 저장물| **실제 테이블의 전체 레코드 데이터 행 자체** | **실제 행의 위치 포인터 (PK 값 또는 ROWID)** |
| 검색 속도 | **매우 빠름 (추가 포인터 추적 없이 즉시 인출)**| 상대적 둔화 (인덱스 탐색 후 PK로 데이터 재조회) |

#### 한줄 요약

- 범위는 정렬 색인, 정확히 같은 값은 해시, 자주 함께 찾는 열은 조회 순서에 맞춘 복합 색인을 쓴다.

## Ⅵ. 실무 고려사항 및 대책 (인덱스 안티패턴 및 튜닝)

<details><summary>핵심 용어</summary>

- **Index Suppression (인덱스 변형 파괴)**: `WHERE SUBSTR(name, 1, 3) = 'KIM'` 과 같이 컬럼을 좌변 가공하면 인덱스를 타지 못하고 Full Table Scan으로 떨어지는 현상.

</details>

| 3대 안티패턴 | 발생 원인 및 쿼리 예시 | 실무 대책 및 튜닝 수용 방안 |
|:---|:---|:---|
| **1. 컬럼 좌변 가공** | `WHERE YEAR(created_at) = 2026` | **`WHERE created_at >= '2026-01-01' AND ...` 로 변경** |
| **2. 묵시적 형변환** | `WHERE phone_no = 01012345678` (숫자형) | **`WHERE phone_no = '01012345678'` (문자열 일치)** |
| **3. 부정형 조건** | `WHERE status != 'DELETED'` | **`WHERE status IN ('ACTIVE', 'PENDING')` 긍정형 전환** |

> 사례: **MySQL InnoDB B+Tree 기반 복합 인덱스 `Index(dept_id, status, salary)` 튜닝**

#### 한줄 요약

- 조회가 빨라져도 쓰기가 지나치게 느려지면 좋은 인덱스가 아니므로 양쪽 비용을 함께 재야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **인덱스 수립 기준(Database Indexing Standards)**: 컬럼 선택도(Selectivity), 쿼리 패턴, B+Tree 아키텍처 및 DML 쓰기 오버헤드 한계성에 의거한 체계.

</details>

- **인덱스 수립 기준**에 따라 대용량 OLTP 데이터베이스 튜닝 시 **선택도 높은 컬럼 중심 B+Tree & 복합 인덱스** 필수 적용

#### 한줄 요약

- 인덱스 설계 유지 기준으로 실제 조회 이득과 변경 부담을 확인한 뒤 색인을 남긴다.
