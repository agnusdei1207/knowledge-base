---
sidebar:
  order: 84
  label: "084. 관계형 데이터베이스 기본: 릴레이션•키•제약조건 (Relational Database)"
  badge:
    text: "미출제 • 30%"
    variant: note
title: "관계형 데이터베이스 기본: 릴레이션•키•제약조건 (Relational Database)"
date: "2026-08-13T18:38:00+09:00"
tags:
  - "notes-software"
weight: 84
extra:
  question_no: "084"
  source_status: "미출제"
  source_history: ""
  priority: 30
  priority_note: "릴레이션•키•제약은 데이터베이스의 기초"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **RDBMS (Relational Database Management System)**: E.F. Codd 박사의 관계형 모델(Relational Model)에 기반하여, 데이터를 2차원 테이블 형태인 릴레이션(Relation)으로 모델링하고 SQL을 통해 데이터 정의, 조회, 제약조건 관리를 수행하는 상용 데이터베이스 엔진.
- **Relation (릴레이션)**: 속성(Attribute, 열)과 튜플(Tuple, 행)들로 구성된 수학적 집합 개념의 2차원 테이블.
- **Integrity Constraints (무결성 제약조건)**: 데이터베이스 내 데이터의 정확성(Accuracy)과 일관성(Consistency)을 유지하기 위해 DBMS가 런타임에 강제하는 규칙(개체, 참조, 도메인 무결성 등).

</details>

- 정의/개념: 데이터를 속성과 튜플로 이루어진 릴레이션(Table)으로 구조화하고, 키(Key) 및 무결성 제약조건(Integrity Constraints)을 통해 데이터의 정합성을 엄격히 통제하는 데이터 관리 시스템인 **RDBMS**
- 배경/필요성: 중복 데이터와 수동 관계 관리는 **갱신 이상•정합성 훼손** 유발

#### 한줄 요약

- 릴레이션•키•제약에 기반한 관계형 데이터베이스가 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Mathematical Set Theory (수학적 집합론)**: 튜플의 순서나 속성의 순서가 무의미하며, 교집합, 합집합, 차집합, 카티션 곱(Cartesian Product) 등 관계 대수(Relational Algebra) 연산 지원.
- **Declarative Query (선언형 질의)**: "어떻게(How) 데이터를 인출할 것인가"를 절차적으로 기술하지 않고, "무슨(What) 데이터를 원하는가"를 SQL로 선언하면 DBMS 옵티마이저가 실행 계획을 자동 수립.

</details>

- **Mathematical Set Theory (관계 대수 및 집합론 기반 구조)**
- **Declarative SQL (선언형 구조화 질의 언어 사용)**
- 엔진 수준의 **ACID Transaction & Integrity Enforcement (무결성 강제)**

#### 한줄 요약

- 집합 연산, 선언형 질의, 무결성 강제가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Primary Key (기본키, PK)**: 릴레이션 내의 모든 튜플을 고유하게 식별(Uniquely Identify)하는 최소한의 속성 집합으로, Null을 허용하지 않음 (개체 무결성).
- **Foreign Key (외래키, FK)**: 참조하는 타 릴레이션의 PK/Unique Key를 가리키는 속성으로, 참조 대상이 존재하거나 Null이어야 함 (참조 무결성).

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                          Relation: Users (릴레이션)                    │
├─────────────────────┬───────────────────┬──────────────────────────────┤
│ PK: user_id (속성)  │ name (속성)       │ email (속성)                 │
├─────────────────────┼───────────────────┼──────────────────────────────┤
│ 1001                │ 홍길동            │ hong@study.com  (Tuple 1)    │
│ 1002                │ 이순신            │ lee@study.com   (Tuple 2)    │
└──────────┬──────────┴───────────────────┴──────────────────────────────┘
           │ (FK 참조 연결: 참조 무결성)
           ▼
┌────────────────────────────────────────────────────────────────────────┐
│                          Relation: Orders                              │
├─────────────────────┬───────────────────┬──────────────────────────────┤
│ order_id (PK)       │ FK: user_id       │ amount                       │
└─────────────────────┴───────────────────┴──────────────────────────────┘
```

선의 의미: Users 릴레이션의 PK(user_id)를 Orders 릴레이션의 FK(user_id)가 참조하여 데이터 무결성을 강제하는 릴레이션 구조.

| 무결성 제약조건 | 정의 및 핵심 개념 | 런타임 제약 예시 |
|:---|:---|:---|
| **Entity Integrity**<br/>(개체 무결성) | 릴레이션의 기본키(PK)는 **Null 값을 가질 수 없으며 고유(Unique)** 해야 함 | PK 필드에 `NULL` 입력 시 Insert Error 방출 |
| **Referential Integrity**<br/>(참조 무결성) | 외래키(FK) 값은 **참조되는 릴레이션의 PK 값과 같거나 Null** 이어야 함 | 부모 테이블에 없는 `user_id`로 Order 생성 불가 |
| **Domain Integrity**<br/>(도메인 무결성)| 속성(Attribute)에 입력되는 값은 **정의된 도메인 영역 범위 내**에 존재해야 함 | 나이(Age) 필드에 음수(`-5`)나 문자열 입력 차단 |

#### 한줄 요약

- 릴레이션, 무결성 제약조건, 구조화 질의 언어의 데이터 처리 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Super Key $\rightarrow$ Candidate Key $\rightarrow$ Primary Key / Alternate Key**: 유일성만 만족하면 슈퍼키, 유일성+최소성 만족 시 후보키, 후보키 중 선정된 1개가 기본키, 선택받지 못한 후보키가 대체키.

</details>

```text
┌──────────────────────────────┐
│ SQL 질의•변경 요청           │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. SQL 구문•권한 검증        │
│ 2. 실행 계획 최적화          │
│ 3. 관계 연산 수행            │
│ 4. 무결성 제약 검증          │
│ 5. 트랜잭션 결과 확정        │
└──────────────┬───────────────┘
               ▼
         [결과 반환]
```

### 동작 원리

1. **SQL 구문•권한 검증**: 객체•열•연산 권한 확인.
2. **실행 계획 최적화**: 통계와 비용으로 접근•조인 순서 결정.
3. **관계 연산 수행**: 선택•투영•조인으로 대상 집합 처리.
4. **무결성 제약 검증**: 도메인•개체•참조 규칙 확인.
5. **트랜잭션 결과 확정**: 성공은 커밋, 실패는 롤백.

#### 한줄 요약

- SQL 해석•최적화•연산•무결성 검증•결과 확정 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ACID vs BASE**: RDBMS는 원자성, 일관성, 격리성, 지속성의 Strict ACID 준수, NoSQL은 Basically Available, Soft-state, Eventual Consistency 준수.

</details>

| 비교 항목 | RDBMS (관계형 데이터베이스) | NoSQL (비관계형 데이터베이스) |
|:---|:---|:---|
| 데이터 구조 | **정형 2차원 테이블 (Schema-First)** | **비정형/반정형 (JSON Document, Key-Value 등)** |
| 트랜잭션 수용 | **다중 행•관계의 ACID 트랜잭션에 강점** | **제품별 ACID 범위와 일관성 모델 상이** |
| 확장성 (Scaling) | 수직•읽기 복제•분할 확장 가능 | **수평 분산을 중심으로 설계된 제품 다수** |
| 주요 질의 언어 | **표준 SQL (Structured Query Language)** | API / JSON 기반 전용 질의 (NoSQL APIs) |

#### 한줄 요약

- 복합 관계는 관계형 데이터베이스, 특정 접근은 비관계형 데이터베이스가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Surrogate Key vs Natural Key**: 인공적으로 생성한 Auto-increment/UUID 키(대리키) 대 실제 비즈니스 도메인의 주민번호/학번(자연키). 실무에서는 변경 여파를 막기 위해 Surrogate Key를 PK로 선호.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 비즈니스 자연키(주민번호/이메일)를 PK로 지정 시 변경 여파 파행 | **Surrogate Key (Auto-Increment BigInt / UUID)를 PK로 채택** | 아키텍처 결합도 해제 |
| 대량 쓰기에서 FK 검증 비용 증가 | 인덱스•배치•파티션 최적화 후 **FK 유지 여부** 판단 | 처리량과 참조 무결성 균형 |
| 복합키(Composite Key) 사용 시 Join SQL 복잡도 폭증 | **단일 대리키(ID) 도입 및 복합 속성은 Unique Index 처리**| SQL 가독성 확보 |

> 사례: **MySQL InnoDB / PostgreSQL 기반 RDBMS 도메인 모델링 정착**

#### 한줄 요약

- 안정 후보키, 참조 무결성, 질의 패턴, 원자성을 지키는 최소 범위가 핵심이다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **RDBMS 수립 기준(RDBMS Modeling Standards)**: 데이터 정합성 수준(ACID), 무결성 제약조건 및 SQL 표준성에 의거한 체계.

</details>

- 복합 관계•원자 변경은 **RDBMS**, 단순 대규모 접근은 **NoSQL** 검토

#### 한줄 요약

- 데이터 특성에 맞는 데이터 모델 선택 기준이 핵심이다.
