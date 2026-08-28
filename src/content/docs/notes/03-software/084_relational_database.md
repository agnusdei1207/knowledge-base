---
sidebar:
  order: 84
  label: "084. 관계형 데이터베이스 기본"
  badge:
    text: "미출 · 30%"
    variant: note
title: "관계형 데이터베이스 기본: 릴레이션•키•제약조건 (Relational Database)"
date: "2026-08-26T18:02:00+09:00"
tags:
  - "notes-software"
weight: 84
extra:
  question_no: "084"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "릴레이션•키•제약은 데이터베이스의 기초"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **RDBMS(Relational Database Management System)**: E.F. Codd의 관계 대수 모델에 기초하여 데이터를 2차원 테이블(릴레이션)로 관리하고 SQL로 제어하는 엔진.
- **무결성 제약조건(Integrity Constraints)**: 데이터베이스 내 데이터의 정확성과 일관성을 유지하기 위해 DBMS 엔진이 강제하는 규칙(개체, 참조, 도메인 무결성).

</details>

- 정의/개념: 데이터를 속성과 튜플의 릴레이션(Relation)으로 구조화하고 **키(Key) 및 무결성 제약조건으로 데이터 정합성을 보장**하는 시스템
- 배경/필요성: 파일 단위 저장은 같은 사실을 여러 파일에 중복 보관해 갱신마다 모든 사본을 찾아 고치는 비용을 치르고 하나만 누락돼도 정합성이 깨지므로, 데이터를 릴레이션에 한 번만 두고 키·제약조건 검증을 엔진 안으로 끌어들여 응용프로그램이 지던 정합성 책임을 대신할 필요

#### 한줄 요약
- 정합성 검증을 응용 계층에 두면 애플리케이션마다 중복 구현되고 하나라도 누락되면 무너지므로, RDBMS는 쓰기 성능 일부를 내주고 그 책임을 엔진이라는 단일 지점으로 모으는 선택을 한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **선언형 질의(Declarative SQL)**: 절차적 알고리즘(How)이 아닌 원하는 결과 집합(What)만 선언하면 옵티마이저가 최적 경로를 찾아 실행.
- **Strict ACID**: 트랜잭션의 원자성, 일관성, 격리성, 지속성을 보장하여 금융 수준의 정합성 유지.

</details>

- 관계 대수(Relational Algebra) 및 집합론에 기반한 **정형 2차원 릴레이션 모델**
- 원하는 결과만 명시하면 옵티마이저가 경로를 탐색하는 **선언형 질의(Declarative SQL)**
- 개체/참조/도메인 무결성을 DBMS 엔진 차원에서 강제하는 **Strict ACID 트랜잭션 보장**

#### 한줄 요약
- 집합론 기반 릴레이션, 선언형 SQL 질의, 엔진 수준의 무결성 강제가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Primary Key vs Foreign Key**: 튜플을 유일하게 식별하는 기본키(PK: Null 불가)와 타 릴레이션의 기본키를 참조하는 외래키(FK).

</details>

```text
[릴레이션 및 3대 무결성 제약조건 구조]
|-- 부모 릴레이션: Users (사용자)
|   |-- [PK: user_id] -> 개체 무결성 (Entity Integrity: Null 불가, 고유성)
|   |-- [name]        -> 도메인 무결성 (Domain Integrity: 허용 타입/범위 준수)
|   `-- [email]       -> 고유 무결성 (Unique Constraint: 중복 금지)
`-- 자식 릴레이션: Orders (주문)
    |-- [PK: order_id]
    `-- [FK: user_id] -> 참조 무결성 (Referential Integrity: Users.user_id 참조 또는 Null)
```

선의 의미: Users 릴레이션의 PK(user_id)를 Orders 릴레이션의 FK가 참조하는 관계

| 구성요소 | 책임 |
|:---|:---|
| 개체 무결성 | 기본키의 **고유성·Null 금지** |
| 참조 무결성 | 외래키의 **부모 키 참조 보장** |
| 도메인 무결성 | 속성의 **타입·범위 제약** |
| 키 계층 | 유일성·최소성 기반 **기본키 선정** |

#### 한줄 요약
- 세 무결성은 모두 쓰기 시점에 검증 비용을 치러 읽기 시점의 정합성 확인을 없애는 거래이므로, 쓰기가 집중되는 워크로드일수록 제약조건의 비용이 성능으로 드러난다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **CBO(Cost-Based Optimizer)**: 통계 정보와 인덱스를 바탕으로 가장 적은 디스크 I/O 비용의 실행 계획을 생성하는 비용 기반 옵티마이저.

</details>

```text
클라이언트 SQL 질의 요청 (`SELECT * FROM Users JOIN Orders ...`)
        │
   [구문/권한 검증] Parser가 SQL 문법 검사 및 테이블/컬럼 접근 권한 확인
        │
   [실행 계획 수립] CBO 옵티마이저가 통계 정보 기반으로 인덱스 스캔 및 조인 방식(Hash/NL) 결정
        │
   [관계 대수 실행] 스토리지 엔진(InnoDB)이 B+Tree 인덱스를 탐색하여 데이터 인출
        │
   [무결성 제약 검사] 데이터 수정/삽입 시 개체 및 참조 무결성 룰 대조
        │
   [결과 반환 및 커밋] WAL(Write-Ahead Logging) 기록 후 클라이언트에 결과 반환
```

#### 한줄 요약
- 선언형 SQL은 접근 경로 결정을 CBO에 위임해 개발자의 튜닝 부담을 없애는 대신, 통계가 실제 분포와 어긋나면 동일한 질의가 자릿수 단위로 느려지는 위험을 함께 떠안는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RDBMS vs NoSQL**: 정형 스키마와 ACID를 보장하는 RDBMS(MySQL, PostgreSQL)와 비정형 데이터와 수평 확장에 유리한 NoSQL(MongoDB, Redis).

</details>

| 비교 항목 | RDBMS (관계형 DB: MySQL, Oracle) | NoSQL (비관계형 DB: MongoDB, DynamoDB) |
|:---|:---|:---|
| 데이터 모델 | **정형 2차원 테이블 (Schema-First)** | **비정형/반정형 Document, Key-Value, Graph** |
| 트랜잭션 보장 | **Strict ACID (금융권 정합성 보장)** | **BASE (Eventual Consistency 중심)** |
| 질의 언어 | **표준 SQL (복잡한 다중 테이블 Join 지원)**| 전용 API 질의 (Join 미지원 또는 제한적) |
| 확장성 | 수직 확장(Scale-up), 읽기 복제 | **수평 분산 확장(Scale-out) 중심 설계** |

#### 한줄 요약
- 복합 관계와 엄격한 정합성은 RDBMS, 대규모 트래픽과 유연한 스키마는 NoSQL을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Surrogate Key(대리키)**: 비즈니스 의미가 없는 인공 식별자(Auto-Increment BigInt, UUID)로, 자연키 변경 시의 파급 효과를 차단.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 주민번호/이메일 등 자연키를 PK로 사용 시 변경 파급 여파 | **비즈니스와 무관한 대리키(Surrogate Key: Auto-Increment)를 PK로 채택** | 테이블 간 결합도 완화 및 안정성 확보 |
| 대규모 초당 쓰기 환경에서 FK 제약으로 인한 락 경합 | **인덱스 추가 및 애플리케이션 레벨 무결성 검증 전환 고려** | 쓰기 처리량(Throughput) 대폭 향상 |
| 복합키(Composite Key) 남용으로 Join SQL 복잡화 | **단일 대리키(ID) 도입 및 복합 속성은 Unique 인덱스로 분리** | SQL 가독성 및 개발 생산성 확보 |
| 잦은 스키마 변경으로 인한 운영 중단 | **Liquibase / Flyway 기반 선언적 DB 마이그레이션 자동화** | 무중단 릴리즈 및 스키마 버전 추적성 확보 |

#### 한줄 요약
- 대리키 PK 채택, FK 쓰기 튜닝, 복합키 단순화, Flyway 마이그레이션으로 정합성을 유지한다.

## Ⅶ. 결론

- 복합 관계·강한 정합성은 **RDBMS**, 유연한 수평 확장은 **NoSQL** 선택

#### 한줄 요약
- 관계형 데이터베이스는 수학적 릴레이션 모델과 무결성 제약조건을 통해 데이터의 신뢰성을 보장하는 소프트웨어 시스템의 영속성 근간이다.
