---
sidebar:
  order: 91
  label: "091. 데이터베이스 무결성 제약 조건 (Database Integrity Constraints)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "데이터베이스 무결성 제약 조건 (Database Integrity Constraints)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **데이터베이스 무결성 제약(Database Integrity Constraints)**: DB에 저장된 데이터의 정확성, 유효성, 일관성 유지를 위해 DBMS 스키마 수준에서 강제하는 규칙 및 메커니즘.
- **고아 데이터(Orphan Data)**: 참조 무결성(Referential Integrity) 결여로 부모 데이터 삭제 후 자식 테이블에 잔존하는 부정확한 데이터.
- **선언적 강제(Declarative Enforcement)**: DDL(`PK`, `FK`, `CHECK`, `NOT NULL`)을 통해 DBMS 엔진이 런타임에 직접 데이터를 검증하도록 하는 방식.

</details>

- **정의**: 데이터베이스 내 이상 데이터 저장을 방지하기 위해 스키마 수준에서 유효성, 식별성, 참조 관계 규칙을 강제하는 메커니즘.
- **필요성**: 애플리케이션 검증 로직 파편화 방지 및 다중 시스템 접근 시 일관성 보장.
- **요약**: 데이터베이스 엔진 레벨의 데이터 일관성 규칙 강제.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **선제적 런타임 차단(Pre-Validation)**: `INSERT/UPDATE/DELETE` 시 DBMS 엔진이 규칙 검사 후 위반 시 즉시 Abort/Rollback.
- **중앙집중식 규칙 관리(Centralized Rule Management)**: DB 엔진 레벨의 통합 통제로 데이터 무결성 보장.

</details>

- **중앙집중식 엔진 통제**: DBMS 레벨의 통합 규칙 적용으로 데이터 일관성 보장.
- **선제적 런타임 차단**: `INSERT/UPDATE` 시점 위반 사항 즉시 차단 및 롤백.
- **선언적 DDL 활용**: `NOT NULL`, `UNIQUE`, `PK`, `FK`, `CHECK` 등 DDL 기반 규칙 선언.
- **요약**: DBMS 엔진 기반의 선제적 위반 차단 및 일관성 관리.

## Ⅲ. 구조 및 구성요소 (데이터베이스 4대 핵심 무결성 제약조건)

<details><summary>핵심 용어</summary>

- **개체 무결성(Entity Integrity)**: 기본키(PK)는 `NULL` 불가 및 고유성(Unique) 유지 필수.
- **참조 무결성(Referential Integrity)**: 외래키(FK) 값은 참조 테이블의 PK/Unique와 동일하거나 `NULL` 유지.
- **도메인 무결성(Domain Integrity)**: 속성 값은 정의된 타입, 범위, `CHECK` 조건 충족 필수.
- **사용자 정의 무결성(User-Defined Integrity)**: 비즈니스 규칙에 따른 커스텀 제약 (예: `CHECK (salary >= 0)`).

</details>

```text
┌────────────────────────────────────────────────────────────┐
│              데이터베이스 4대 무결성 제약 구조             │
├───────────────────┬───────────────────┬────────────────────┤
│ 1. 개체 무결성    │ 2. 참조 무결성    │ 3. 도메인 무결성   │
│   (Entity)        │   (Referential)   │   (Domain)         │
│  • 기본키(PK)     │  • 외래키(FK)     │  • 널값 불가       │
│  • 유니크(Unique) │  • 연쇄(Cascade)  │  • 타입/제약조건   │
├───────────────────┴───────────────────┴────────────────────┤
│ 4. 사용자 정의 무결성 (User-Defined: 트리거/프로시저)      │
└────────────────────────────────────────────────────────────┘
```

선의 의미: 데이터베이스가 개체 무결성, 참조 무결성, 도메인 무결성, 사용자 정의 무결성을 조합하여 무결성 안전망을 형성하는 구조.

| 무결성 제약 유형 | 적용 선언 구문 (DDL) | 제약 조건 및 런타임 수용 동작 |
|:---|:---|:---|
| **Entity Integrity (개체)** | **`PRIMARY KEY, UNIQUE`** | 행(Tuple)의 유일성 보장, `NULL` 값 입력 원천 차단 |
| **Referential Integrity (참조)**| **`FOREIGN KEY ... REFERENCES`**| 부모-자식 간 참조 관계 보장, 고아 데이터 발생 차단 |
| **Domain Integrity (도메인)**| **`NOT NULL, CHECK, DEFAULT`** | 속성의 데이터 타입, 자릿수, 범위(`age > 0`) 조건 검증 |
| **User-Defined (사용자정의)**| **`TRIGGER, STORED PROCEDURE`**| 복잡한 비즈니스 로직(예: 주말 결제 불가)의 DB level 검증 |

#### 한줄 요약

- 값•행•관계 규칙과 키 탐색 장치가 잘못된 저장을 차단한다.

## Ⅳ. 흐름도 (참조 무결성 4대 제약 옵션: CASCADE, SET NULL 등)

<details><summary>핵심 용어</summary>

- **Referential Action Options**: CASCADE(부모 삭제 시 자식도 자동 연쇄 삭제), SET NULL(자식 FK를 Null로 변경), RESTRICT/NO ACTION(자식이 있으면 부모 삭제 금지).

</details>

```text
[부모 테이블 튜플 삭제 시도]
                │
                ▼ (자식 테이블 FK 참조 존재 확인)
          ├── 아니오 ──► [삭제 완료]
          │
          └── 예 (참조 무결성 옵션 판정)
                ├─► 1. RESTRICT / NO ACTION ──► [삭제 거부 및 롤백]
                ├─► 2. CASCADE ───────────────► [자식 튜플 연쇄 삭제]
                └─► 3. SET NULL ──────────────► [자식 FK 값을 널로 변경]
```

### 동작 원리

1. **Delete Request**: 부모(Users) 튜플 삭제 시도.
2. **FK Check**: 자식(Orders) 테이블에 `user_id`를 참조하는 튜플 스캔.
3. **Action Execution**:
   - **RESTRICT**: 삭제 거부 에러 반환.
   - **CASCADE**: 자식 Order 내역도 자동으로 깔끔히 삭제.
   - **SET NULL**: 자식 Order 내역의 `user_id`를 `NULL`로 변경하여 이력 보존.

#### 한줄 요약

- 값의 범위, 행의 이름표, 부모와의 연결을 차례로 확인한 뒤 저장한다.

## Ⅴ. 종류 및 비교 (App Level Validation vs DB Integrity Constraint)

<details><summary>핵심 용어</summary>

- **Validation Level Tradeoff**: 앱 레벨 검증은 유연하나 다중 앱 접속 시 무결성 구멍 발생, DB 레벨 검증은 완벽하나 DB CPU 오버헤드 증가.

</details>

| 비교 항목 | Application Level Validation | Database Integrity Constraint |
|:---|:---|:---|
| 검증 위치 | Spring/Java 애플리케이션 코드 | **DBMS 엔진 (DDL 선언)** |
| 규칙 일관성 | 앱마다 검증 로직 파편화 위험 존재 | **모든 접속 앱에 대해 100% 동일 규칙 적용** |
| 비즈니스 유연성 | 높음 (조건별 가변 처리 용이) | 낮음 (DDL 변경 시 마이그레이션 필요) |
| 데이터 안전성 | 유실/누락 위험 상존 | **원천적 데이터 붕괴 차단 완벽** |

#### 한줄 요약

- 도메인은 값, 개체는 행의 이름표, 참조는 테이블 사이의 연결을 지킨다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **FK Indexing Requirement**: 외래키(FK) 컬럼에 인덱스를 생성하지 않을 경우, 부모 테이블 삭제/수정 시 자식 테이블 전체에 Table Lock이 걸려 성능이 급락하는 안티패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Foreign Key (FK) 컬럼에 B-Tree 인덱스 부재로 인한 Lock 지연 | **모든 Foreign Key 컬럼에 B-Tree 인덱스 필수 추가** | 부모 삭제 시 Lock 범위 극소화 |
| 대용량 배치 `INSERT` 시 무결성 검사로 인한 쓰기 속도 저하 | **대량 배치 작업 시 임시로 FK Check OFF 후 작업 완료 시 ON**| 배치 처리 속도 극대화 |
| `CASCADE` 삭제 남용으로 인한 주요 데이터 상실 | **실무에서는 `CASCADE` 자제, `RESTRICT` 또는 `SET NULL` 권장**| 데이터 손실 사고 차단 |

> 사례: **PostgreSQL / MySQL `FOREIGN KEY` 인덱싱 및 `ON DELETE RESTRICT` 설정**

#### 한줄 요약

- 규칙을 DB에 선언하되 기존 데이터, 삭제 영향, 검사 비용을 함께 확인해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **무결성 수립 기준(Database Integrity Standards)**: 데이터 정확성 요구 수준, FK 인덱스 정책 및 참조 무결성 런타임 제어성에 의거한 체계.

</details>

- **데이터베이스 무결성 수립 체계 적용** (상용 RDBMS 설계 시 PK/FK/NOT NULL 제약 및 FK 인덱스 설계 필수 적용)

#### 한줄 요약

- 무결성 규칙 배치 기준은 모든 입력 경로에 같은 데이터 규칙을 적용하게 한다.
