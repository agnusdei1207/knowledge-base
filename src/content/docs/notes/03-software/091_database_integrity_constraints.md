---
sidebar:
  order: 91
  label: "091. 데이터베이스 무결성 제약 조건"
  badge:
    text: "기출 · 70%"
    variant: note
title: "데이터베이스 무결성 제약 조건 (Database Integrity Constraints)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 91
extra:
  question_no: "091"
  source_status: "기출"
  source_history: "128회, 134회"
  priority: 70
  priority_note: "128•134회 반복, 무결성 제약 설계 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **무결성 제약조건(Integrity Constraints)**: 데이터베이스 내 데이터의 정확성, 일관성, 유효성을 보장하기 위해 DBMS 엔진이 강제하는 규칙 체계.
- **4대 무결성 제약**: 개체 무결성(PK), 참조 무결성(FK), 도메인 무결성(Check), 사용자 정의 무결성(Trigger).

</details>

- 정의/개념: 데이터베이스에 저장되는 데이터의 유효성과 일관성을 위해 **개체(PK), 참조(FK), 도메인(Check), 사용자정의(Trigger)** 4대 규칙을 강제하는 스키마 제약 체계
- 배경/필요성: 애플리케이션 단독 검증 시 직접 SQL 접근에 따른 **검증 우회, 부모 삭제 후 고아 데이터(Orphan) 발생 및 데이터 오염 해결 불가**

#### 한줄 요약
- 개체, 참조, 도메인, 사용자 정의 무결성을 DBMS 엔진 레벨에서 선언하여 데이터의 신뢰성을 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Declarative DDL**: 애플리케이션 코드가 아닌 `PRIMARY KEY`, `FOREIGN KEY`, `CHECK` 등 DDL 문법으로 데이터베이스 스키마 자체에 선언.
- **Orphan Data(고아 데이터)**: 부모 테이블의 레코드가 삭제되었는데, 자식 테이블의 외래키 참조 레코드가 그대로 남아 연결이 끊어진 불량 데이터.

</details>

- 모든 데이터 조작에 대해 DBMS 엔진 차원의 **선언적 DDL 기반 중앙집중식 규칙 강제**
- 런타임 제약조건 위반 감지 시 즉각적 에러 방출 및 **트랜잭션 자동 롤백(Fail-Fast)**
- 다중 마이크로서비스 및 배치 직접 접근 환경에서도 **우회 불가능한 최후의 데이터 안전망**

#### 한줄 요약
- 선언적 DDL과 엔진 차원의 중앙 통제로 어떤 우회 경로에서도 데이터 무결성을 절대 방어한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **ON DELETE 옵션**: 부모 레코드 삭제 시 자식 데이터 처리 정책 (RESTRICT, CASCADE, SET NULL, NO ACTION).

</details>

```text
[데이터베이스 4대 무결성 제약 구조]
|-- 1. 개체 무결성 (Entity Integrity: PRIMARY KEY, UNIQUE, NOT NULL - 튜플의 유일 식별성 보장)
|-- 2. 참조 무결성 (Referential Integrity: FOREIGN KEY, ON DELETE/UPDATE CASCADE/RESTRICT)
|-- 3. 도메인 무결성 (Domain Integrity: DataType, NOT NULL, CHECK (age >= 0), DEFAULT)
`-- 4. 사용자 정의 무결성 (User-Defined: Trigger, Stored Procedure, Application Logic)
```

선의 의미: 계층 및 4대 무결성 제약의 분류 및 DDL 매핑 구조

| 무결성 제약조건 | DDL 선언 키워드 | 핵심 엔지니어링 책임 |
|:---|:---|:---|
| **개체 무결성 (Entity)** | **`PRIMARY KEY`, `UNIQUE`** | 레코드의 고유 식별을 위해 **기본키의 유일성과 Not Null 강제** |
| **참조 무결성 (Referential)**| **`FOREIGN KEY`, `ON DELETE`** | 부모-자식 간 관계 유효성을 보장하고 **고아 데이터(Orphan) 차단** |
| **도메인 무결성 (Domain)** | **`NOT NULL`, `CHECK`, `DEFAULT`**| 속성값의 데이터 타입, 자릿수, **허용 범위(Check) 및 기본값 검증** |
| **사용자 정의 무결성** | **`TRIGGER`, `STORED PROCEDURE`**| 단순 DDL로 표현 불가한 **복잡한 비즈니스 규칙 및 감사 로그 검증** |

#### 한줄 요약
- 개체(행 유일성), 참조(관계 유효성), 도메인(값 범위), 사용자 정의(업무 규칙)로 무결성을 완성한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **RESTRICT vs CASCADE**: 자식이 있으면 부모 삭제를 금지하는 RESTRICT와 부모 삭제 시 자식까지 연쇄 삭제하는 CASCADE.

</details>

```text
클라이언트가 부모 테이블(Users) 레코드 삭제 요청 (`DELETE FROM Users WHERE id = 101`)
        │
   1. [FK 참조 탐색] DBMS 엔진이 자식 테이블(Orders)의 외래키 인덱스를 B-Tree 탐색
        │
   해당 user_id(101)를 참조하는 자식 주문 레코드가 존재하는가?
   ┌────┴───────────────────────────┐
  예 (자식 레코드 존재함)           아니오 (참조하는 자식 없음)
   │                                 │
2. [ON DELETE 정책 판정]             [삭제 실행 완료]
   ┌────┼────────────────────┐      부모 레코드 정상 삭제 후 커밋
   │    │                    │
[RESTRICT / NO ACTION]   [CASCADE]                 [SET NULL]
삭제 차단 및 롤백 에러   자식 주문도 연쇄 자동삭제  자식 외래키를 NULL로 변경
```

#### 한줄 요약
- 부모 삭제 → 자식 FK 탐색 → 정책 판정 → RESTRICT(롤백) 또는 CASCADE(연쇄 처리) 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Application Validation vs DB Constraint**: 스프링 애플리케이션 레벨 검증(Java `@Valid`)과 DBMS 엔진 레벨 제약(DDL Constraint).

</details>

| 비교 항목 | 애플리케이션 검증 (Spring `@Valid`) | 데이터베이스 제약 (DB Constraints) |
|:---|:---|:---|
| 검증 주체 | 웹 서버 / 애플리케이션 메모리 | **DBMS 스토리지 엔진 (InnoDB 등)** |
| 장점 | 사용자 친화적 에러 메시지, 복잡한 비즈니스 로직 검증 | **직접 SQL/배치 접근에도 우회 불가능한 100% 무결성** |
| 단점 | DB 직접 쿼리나 타 서비스 연계 시 우회 가능 | 제약조건 변경 시 스키마 DDL 마이그레이션 오버헤드 |
| 최적 전략 | 1차 사용자 UX 및 폼 유효성 검증 | **최후의 데이터 무결성 보루(Defensive Barrier)** |

#### 한줄 요약
- 애플리케이션 검증은 사용자 경험을 개선하고, DB 무결성 제약은 최후의 데이터 안전망을 담당한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Unindexed FK(외래키 인덱스 누락)**: 자식 테이블의 FK 컬럼에 인덱스가 없을 경우, 부모 레코드 삭제/수정 시 자식 테이블 전체에 풀 테이블 락(Table Lock)이 걸리는 성능 재앙.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Foreign Key 인덱스 누락으로 부모 행 삭제 시 Table Lock 발생 | **모든 자식 테이블의 Foreign Key 컬럼에 B-Tree 인덱스 필수 생성** | 참조 검사 속도 향상 및 락 경합 방지 |
| `ON DELETE CASCADE` 남용으로 인한 대규모 데이터 연쇄 유실 | **실무에서는 `CASCADE` 금지, `RESTRICT` 또는 `Soft Delete` 적용** | 운영자의 실수로 인한 핵심 원장 삭제 방지 |
| 대용량 데이터 배치 적재(Bulk Insert) 시 제약조건 부하 | **적재 전 제약조건 일시 비활성화 $\to$ 적재 완료 후 일괄 검증 활성화** | 배치 처리 시간 80% 단축 |
| 분산 MSA 환경에서 DB 간 물리적 Foreign Key 설정 불가 | **카프카 CDC(Debezium) 기반 도메인 이벤트로 참조 정합성 유지** | 서비스 간 결합도 해제 및 최종 정합성 달성 |

#### 한줄 요약
- FK 인덱스 필수 생성, CASCADE 남용 금지, 배치 시 제약 일시 해제, MSA 이벤트 연계로 최적화한다.

## Ⅶ. 결론

- 시스템 아키텍처의 안정성을 위해 **애플리케이션 검증에 더해 DBMS 레벨의 4대 무결성 제약조건(PK/FK/Check)을 필수 선언**하고, **FK 인덱싱 및 Soft Delete 정책**을 결합하여 고성능 무결점 데이터베이스 구축

#### 한줄 요약
- 데이터베이스 무결성 제약 조건은 어떠한 우회 접속이나 시스템 장애에도 데이터의 정확성과 일관성을 지켜내는 데이터베이스의 절대적 안전장치다.