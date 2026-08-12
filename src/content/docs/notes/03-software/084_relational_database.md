---
sidebar:
  order: 84
  label: "084. 관계형 데이터베이스 기본: 릴레이션•키•제약조건 (Relational Database)"
  badge:
    text: "미출제 • 30%"
    variant: note
title: "관계형 데이터베이스 기본: 릴레이션•키•제약조건 (Relational Database)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **RDBMS (Relational Database Management System)**: E.F. Codd 박사의 관계형 모델(Relational Model)에 기반하여, 데이터를 2차원 테이블 형태인 릴레이션(Relation)으로 모델링하고 SQL을 통해 데이터 정의, 조회, 제약조건 관리를 수행하는 상용 데이터베이스 엔진.
- **Relation (릴레이션)**: 속성(Attribute, 열)과 튜플(Tuple, 행)들로 구성된 수학적 집합 개념의 2차원 테이블.
- **Integrity Constraints (무결성 제약조건)**: 데이터베이스 내 데이터의 정확성(Accuracy)과 일관성(Consistency)을 유지하기 위해 DBMS가 런타임에 강제하는 규칙(개체, 참조, 도메인 무결성 등).

</details>

- 정의/개념: 데이터를 속성과 튜플로 이루어진 릴레이션(Table)으로 구조화하고, 키(Key) 및 무결성 제약조건(Integrity Constraints)을 통해 데이터의 정합성을 엄격히 통제하는 데이터 관리 시스템인 **RDBMS**
- 배경/필요성: 무질서한 데이터 중복(Redundancy) 및 갱신 이상(Anomaly) 방지, 애플리케이션 독립적인 표준 선언적 언어(SQL) 기반 정보 관리 요구성

#### 한줄 요약

- 릴레이션•키•제약에 기반한 관계형 데이터베이스가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Mathematical Set Theory (수학적 집합론)**: 튜플의 순서나 속성의 순서가 무의미하며, 교집합, 합집합, 차집합, 카티션 곱(Cartesian Product) 등 관계 대수(Relational Algebra) 연산 지원.
- **Declarative Query (선언형 질의)**: "어떻게(How) 데이터를 인출할 것인가"를 절차적으로 기술하지 않고, "무슨(What) 데이터를 원하는가"를 SQL로 선언하면 DBMS 옵티마이저가 실행 계획을 자동 수립.

</details>

- **Mathematical Set Theory (관계 대수 및 집합론 기반 구조)**
- **Declarative SQL (선언형 구조화 질의 언어 사용)**
- 엔진 수준의 **ACID Transaction & Integrity Enforcement (무결성 강제)**

#### 한줄 요약

- 집합 연산, 선언형 질의, 무결성 강제가 핵심이다.

## Ⅲ. 구조 및 구성요소 (릴레이션 구조 & 3대 무결성 제약조건)

<details><summary>핵심 용어</summary>

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

## Ⅳ. 흐름도 (RDBMS 5대 키: Key Hierarchy)

<details><summary>핵심 용어</summary>

- **Super Key $\rightarrow$ Candidate Key $\rightarrow$ Primary Key / Alternate Key**: 유일성만 만족하면 슈퍼키, 유일성+최소성 만족 시 후보키, 후보키 중 선정된 1개가 기본키, 선택받지 못한 후보키가 대체키.

</details>

```text
[Super Key (유일성 만족)]
        │
        ▼ (최소성 조건 추가)
[Candidate Key (후보키: 유일성 + 최소성)]
        │
        ├──────────────────────────┐
        ▼ (대표키 선정)             ▼ (미선정)
[Primary Key (기본키)]      [Alternate Key (대체키)]
```

### 동작 원리

1. **Super Key (슈퍼키)**: 튜플을 고유하게 식별할 수 있는 속성 집합 (유일성 O, 최소성 X).
2. **Candidate Key (후보키)**: 튜플을 고유 식별하면서 불필요한 속성을 제거한 최소 집합 (유일성 O, 최소성 O).
3. **Primary Key (기본키)**: 후보키 중에서 대표로 선택된 키 (`NOT NULL` + `UNIQUE`).
4. **Alternate Key (대체키)**: 후보키 중 기본키로 선택되지 않고 남아있는 키.
5. **Foreign Key (외래키)**: 타 릴레이션의 기본키를 참조하는 관계 키.

#### 한줄 요약

- SQL 해석•최적화•연산•무결성 검증•결과 확정 흐름이 핵심이다.

## Ⅴ. 종류 및 비교 (RDBMS vs NoSQL)

<details><summary>핵심 용어</summary>

- **ACID vs BASE**: RDBMS는 원자성, 일관성, 격리성, 지속성의 Strict ACID 준수, NoSQL은 Basically Available, Soft-state, Eventual Consistency 준수.

</details>

| 비교 항목 | RDBMS (관계형 데이터베이스) | NoSQL (비관계형 데이터베이스) |
|:---|:---|:---|
| 데이터 구조 | **정형 2차원 테이블 (Schema-First)** | **비정형/반정형 (JSON Document, Key-Value 등)** |
| 트랜잭션 수용 | **강력한 ACID 트랜잭션 보장** | **Eventual Consistency (최종 일관성)** |
| 확장성 (Scaling) | **Vertical Scaling (수직 확장, Scale-Up 위주)**| **Horizontal Scaling (수평 확장, Scale-Out 용이)**|
| 주요 질의 언어 | **표준 SQL (Structured Query Language)** | API / JSON 기반 전용 질의 (NoSQL APIs) |

#### 한줄 요약

- 복합 관계는 관계형 데이터베이스, 특정 접근은 비관계형 데이터베이스가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Surrogate Key vs Natural Key**: 인공적으로 생성한 Auto-increment/UUID 키(대리키) 대 실제 비즈니스 도메인의 주민번호/학번(자연키). 실무에서는 변경 여파를 막기 위해 Surrogate Key를 PK로 선호.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 비즈니스 자연키(주민번호/이메일)를 PK로 지정 시 변경 여파 파행 | **Surrogate Key (Auto-Increment BigInt / UUID)를 PK로 채택** | 아키텍처 결합도 해제 |
| 대용량 데이터 환경에서 FK 제약으로 인한 Insert 성능 저하 | **DB level FK 대신 Application logic level 참조 무결성 검증**| 쓰기 처리량(TPS) 확보 |
| 복합키(Composite Key) 사용 시 Join SQL 복잡도 폭증 | **단일 대리키(ID) 도입 및 복합 속성은 Unique Index 처리**| SQL 가독성 확보 |

> 사례: **MySQL InnoDB / PostgreSQL 기반 RDBMS 도메인 모델링 정착**

#### 한줄 요약

- 안정 후보키, 참조 무결성, 질의 패턴, 원자성을 지키는 최소 범위가 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **RDBMS 수립 기준(RDBMS Modeling Standards)**: 데이터 정합성 수준(ACID), 무결성 제약조건 및 SQL 표준성에 의거한 체계.

</details>

- **RDBMS 수립 기준**에 따라 금융/결제 등 핵심 도메인 구축 시 **RDBMS + ACID 트랜잭션 + 개체/참조 무결성** 필수 인가

#### 한줄 요약

- 데이터 특성에 맞는 데이터 모델 선택 기준이 핵심이다.
