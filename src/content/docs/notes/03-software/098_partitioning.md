---
sidebar:
  order: 98
  label: "098. 파티셔닝: 범위•해시•리스트 (Partitioning)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "파티셔닝: 범위•해시•리스트 (Partitioning)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 98
extra:
  question_no: "098"
  source_status: "미출제"
  source_history: ""
  priority: 50
  priority_note: "파티션 키•분할 방식은 대용량 설계 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Table Partitioning (테이블 파티셔닝)**: 대용량 테이블을 파티션 키(Partition Key) 기준에 따라 물리적으로 여러 개의 작고 관리하기 쉬운 개별 파티션 파일로 분할하여 관리하되, 애플리케이션에는 단일 테이블로 보여주는 물리적 데이터베이스 설계 기법.
- **Partition Pruning (파티션 프루닝)**: 쿼리의 `WHERE` 절에 사용된 파티션 키 조건을 분석하여, 조건에 해당하지 않는 무관한 파티션 파일 읽기를 디스크 I/O 레벨에서 완전히 제외시키는 옵티마이저 최적화 기술.
- **Partitioning vs Sharding**: 파티셔닝은 단일 DB 서버 인스턴스 내부의 물리적 테이블 분할, 샤딩(Sharding)은 여러 독립된 물리 DB 노드로 데이터를 수평 분산하는 아키텍처.

</details>

- 정의/개념: 대용량 단일 테이블을 파티션 키(Range, Hash, List) 기준으로 물리적 독립 파일로 분할하여 **Partition Pruning**을 통해 I/O 성능을 극대화하고 데이터 수명주기를 관리하는 기법인 **Table Partitioning**
- 배경/필요성: 단일 거대 테이블(수억 건+) 스캔 시 발생하는 I/O 병목 해소, 오래된 과거 이력 데이터의 손쉬운 백업 및 일괄 삭제(DROP PARTITION) 운용 필요성

#### 한줄 요약

- 자료를 날짜나 고객별 서랍으로 나누고 필요한 서랍만 여는 방식이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Partition Pruning (파티션 프루닝)**: 필요한 특정 파티션 영역만 선택적 탐색.
- **Easy Data Lifecycle Management (수명주기 관리)**: `TRUNCATE / DROP PARTITION` 구문으로 수천만 건 데이터 1초 만에 일괄 삭제.

</details>

- **Partition Pruning**을 통한 디스크 I/O 대폭 감소
- **High Availability & Manageability (파티션 단위 백업/복구/삭제)**
- **Global Index 대 Local Index** 간의 락/인덱스 관리 Trade-off

#### 한줄 요약

- 나누는 기준이 나쁘면 한 서랍만 가득 차거나 조회할 때 모든 서랍을 열게 된다.

## Ⅲ. 구조 및 구성요소 (3대 파티셔닝 분할 전략 아키텍처)

<details><summary>핵심 용어</summary>

- **Range Partitioning (범위)**: 일자/날짜/연도 등 연속된 범위 기준으로 파티션 분할.
- **Hash Partitioning (해시)**: 파티션 키에 해시 함수를 적용하여 데이터를 각 파티션에 균등하게 수평 분산.
- **List Partitioning (목록)**: 지역 코드, 부서 코드 등 명확히 구별되는 이산적인(Discrete) 값 목록 기준으로 분할.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Table Partitioning 3대 전략                     │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ 1. Range          │ 2. Hash           │ 3. List                        │
│    (범위 파티셔닝)│    (해시 파티셔닝)│    (목록 파티셔닝)             │
├───────────────────┼───────────────────┼────────────────────────────────┤
│ • 2026-01 Partition│ • Hash(user_id) %4│ • Region: 'SEOUL' Partition    │
│ • 2026-02 Partition│   Part 0, 1, 2, 3 │ • Region: 'BUSAN' Partition    │
│ (시계열/이력 적합)│ (균등 분산 최적)  │ (지역/구분자 코드 적합)        │
└───────────────────┴───────────────────┴────────────────────────────────┘
```

선의 의미: 대용량 테이블 데이터를 Range(날짜), Hash(해시분산), List(코드구분) 3대 전략에 따라 물리적 파티션 파일로 분할하는 구조.

| 파티셔닝 전략 | 분할 기준 키 (Partition Key) | 실무 적합 워크로드 및 특성 |
|:---|:---|:---|
| **Range Partitioning** | **날짜, 일자, 연도 (`created_at`)** | **시계열 데이터, 매출 이력, 로그 테이블 (파티션 Drop 용이)** |
| **Hash Partitioning** | **고객 ID, 주문 ID (`user_id`)** | **데이터가 특정 파티션에 치우치지 않고 균등 분산 필요시** |
| **List Partitioning** | **지역 코드, 국가 코드 (`region_code`)** | **불연속적인 명확한 비즈니스 코드값 분류 시 적합** |
| **Composite Partitioning**| **Range + Hash / Range + List** | 1차로 날짜 분할 후, 2차로 해시/목록 분할 (복합 구조) |

#### 한줄 요약

- 키와 경계표로 저장 위치를 나누고 필요한 파티션만 읽는다.

## Ⅳ. 흐름도 (Partition Pruning 작동 원리)

<details><summary>핵심 용어</summary>

- **Pruning Execution**: SQL `WHERE` 조건절의 파티션 키 조건을 옵티마이저가 해석하여 조건에 안 맞는 파티션을 물리적 스캔 대상에서 아예 삭제하는 처리 과정.

</details>

```text
[SQL 쿼리 입력: SELECT * FROM orders WHERE created_at = '2026-08-12']
                               │
                               ▼
[Optimizer: Partition Key 'created_at' 식별 및 Pruning 실행]
                               │
                               ▼
 ┌─────────────────────────────┴─────────────────────────────┐
 │ 2026-06 Partition (Pruned - Read Skip)                    │
 │ 2026-07 Partition (Pruned - Read Skip)                    │
 │ 2026-08 Partition ──────────► [08월 파티션 파일만 디스크 스캔]│
 └───────────────────────────────────────────────────────────┘
```

### 동작 원리

1. **SQL Parse**: `orders` 테이블 쿼리의 `WHERE created_at` 조건 식별.
2. **Pruning Judgment**: `created_at`이 파티션 키임을 인지하고, `2026-08` 파티션 전용 스캔 결정.
3. **I/O Execution**: `2026-06, 2026-07` 등 수억 건의 타 파티션 파일 스캔을 100% Skip하고 **해당 파티션만 0.01초 만에 조치**.

#### 한줄 요약

- 날짜 조건을 경계표와 대조해 해당 기간의 서랍과 색인만 읽는다.

## Ⅴ. 종류 및 비교 (Local Index 대 Global Index)

<details><summary>핵심 용어</summary>

- **Local Prefixed Index (로컬 인덱스)**: 파티션별로 독립적인 B+Tree 인덱스를 각각 생성하는 방식 (파티션 관리가 매우 용이).
- **Global Index (글로벌 인덱스)**: 파티션 구분 없이 전체 테이블 통합 B+Tree 인덱스를 생성하는 방식 (파티션 Drop 시 인덱스 파행).

</details>

| 비교 항목 | Local Partitioned Index (로컬 인덱스) | Global Partitioned Index (글로벌 인덱스) |
|:---|:---|:---|
| 인덱스 생성 구조| **각 파티션 파일마다 독립적으로 인덱스 관리** | **전체 파티션 통틀어 단 1개의 거대 인덱스 관리**|
| 파티션 삭제 시 영향| **해당 파티션 인덱스만 함께 Drop (오류 없음)** | **전체 글로벌 인덱스 파행 (Unusable 상태)** |
| 인덱스 스캔 속도| 파티션 키 미포함 시 모든 로컬 인덱스 스캔 | 파티션 키 미포함 쿼리도 초고속 탐색 |
| 실무 권장성 | **실무 RDBMS 파티셔닝의 절대적 표준 권장** | 파티션 변경이 없는 정적 테이블에만 선별 수용 |

#### 한줄 요약

- 범위는 기간, 해시는 균등 분배, 리스트는 정해진 업무 구분에 알맞다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Data Skew (데이터 편향 현상)**: Hash Partitioning 키 선정이 잘못되었거나 Range 키에 특정 날짜(이벤트 날짜) 트래픽이 몰려 특정 파티션 파일만 거대해지는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 파티션 키를 `WHERE` 조건절에 포함하지 않아 **Full Partition Scan** 발생 | **모든 주요 쿼리에 파티션 키(`created_at`) 필수 조건 포함** | Partition Pruning 보장 |
| 특정 파티션 파일 용량 폭증 (**Data Skew**) | **Range + Hash Composite Partitioning (복합 파티셔닝) 도입**| 균등 수평 분산 |
| 파티션 삭제 시 글로벌 인덱스가 Unusable 파행 | **인덱스는 Local Index 생성을 표준 지침으로 준수** | 수명주기 관리 안정성 |

> 사례: **PostgreSQL / MySQL `PARTITION BY RANGE (TO_DAYS(created_at))` 파티셔닝 운용**

#### 한줄 요약

- 서랍을 나눈 뒤에는 필요한 서랍만 열리는지와 한 서랍에 자료가 몰리지 않는지 확인해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **파티셔닝 수립 기준(Partitioning Design Standards)**: 테이블 데이터 건수(1천만 건 이상), 파티션 키 Pruning 효율성 및 Local Index 정책에 의거한 체계.

</details>

- **파티셔닝 수립 기준**에 따라 수억 건 대용량 이력 DB 설계 시 **Range Partitioning & Local Index** 필수 적용

#### 한줄 요약

- 파티셔닝 방식 선택 기준은 필요한 파티션만 읽고 오래된 데이터를 단위별로 정리하게 한다.
