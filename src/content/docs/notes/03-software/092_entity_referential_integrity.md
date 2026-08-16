---
sidebar:
  order: 92
  label: "092. 개체 무결성•참조 무결성 (Entity Referential Integrity)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "개체 무결성•참조 무결성 (Entity Referential Integrity)"
date: "2026-08-13T19:26:00+09:00"
tags:
  - "notes-software"
weight: 92
extra:
  question_no: "092"
  source_status: "기출"
  source_history: "128회"
  priority: 30
  priority_note: "128회 기출, 개체•참조 무결성의 하위 구분"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Entity Integrity (개체 무결성)**: 릴레이션에서 튜플(행)의 고유 식별을 위해 기본키(Primary Key)를 구성하는 어떤 속성도 `NULL` 값이나 중복 값을 가질 수 없도록 강제하는 규칙.
- **Referential Integrity (참조 무결성)**: 외래키(Foreign Key)의 값은 참조하는 부모 릴레이션의 기본키(또는 Unique Key) 값과 반드시 일치하거나, 또는 `NULL`이어야 한다는 릴레이션 간 관계 강제 규칙.
- **Primary Key vs Foreign Key Relationship**: 부모 릴레이션의 식별자(PK)를 자식 릴레이션이 외래키(FK)로 참조함으로써 구축되는 논리적 관계 연결선.

</details>

- 정의/개념: 행 식별과 릴레이션 연결을 지키는 **개체•참조 무결성**
- 배경/필요성: PK 중복•부모 없는 FK는 **식별 불능•고아 데이터** 유발

#### 한줄 요약

- 각 기록에 겹치지 않는 번호를 주고, 관계는 실제 존재하는 기록에만 연결한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Uniqueness & Non-Null Constraint (개체 무결성의 독점적 지위)**: 기본키는 절대 `NULL`이 될 수 없으며, 중복을 배제하여 릴레이션 내 유일성(Uniqueness)을 확립.
- **Referential Validity (참조 무결성의 유효성)**: 외래키는 부모 릴레이션의 PK 집합에 명확히 존재하는 값에만 바인딩.

</details>

- **개체 무결성**: PK 기반 Unique 및 NOT NULL 보장으로 각 튜플의 유일 식별 체계 확립.
- **참조 무결성**: FK 기반 부모-자식 간 참조 관계 및 정합성 보장.
- **참조 동작**: DDL 선언 시 `CASCADE`, `SET NULL`, `RESTRICT` 등 연쇄 삭제/수정 규칙 지원.

#### 한줄 요약

- 이름표는 하나뿐이어야 하고, 자식 기록은 존재하는 부모에게만 연결되어야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Parent-Child Relation**: PK를 소유한 부모 릴레이션과 해당 PK를 FK로 참조하는 자식 릴레이션 간의 구조적 종속 관계.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [부모 릴레이션: Users]                                                 │
│  기본키(PK): user_id (1001) <─── 개체 무결성 (중복/빈값 불가)          │
└──────────▲─────────────────────────────────────────────────────────────┘
           │ (참조 무결성: FK 값은 부모 PK 또는 널값 유지)
┌──────────┴─────────────────────────────────────────────────────────────┐
│ [자식 릴레이션: Orders]                                                │
│  기본키(PK): order_id (5001) | 외래키(FK): user_id (1001)              │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 부모 테이블의 PK(user_id)에 개체 무결성이 적용되고, 자식 테이블의 FK(user_id)가 이를 참조하며 참조 무결성을 유지하는 아키텍처.

| 구분 (Category) | Entity Integrity (개체 무결성) | Referential Integrity (참조 무결성) |
|:---|:---|:---|
| 대상 키  | **Primary Key (기본키)** | **Foreign Key (외래키)** |
| 핵심 규칙 | **`NOT NULL` & `UNIQUE` (중복/빈값 절대 불가)** | **부모 릴레이션 PK 존재값 또는 `NULL`만 허용** |
| 위반 시 제약 | `INSERT/UPDATE` 시 PK 중복/Null 입력 거부 | 부모 없는 `user_id`로 자식 Order 생성 불가 |
| 목적 | **릴레이션 내 튜플의 유일 식별**| **릴레이션 간 연관성 및 고아 데이터 방지** |

#### 한줄 요약

- 행의 이름표와 부모 연결, 변경 시 처리 규칙을 함께 정의한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Cascade Execution Flow**: 부모 튜플 수정/삭제 시 런타임에 지정된 Referencing Action(RESTRICT, CASCADE, SET NULL, SET DEFAULT)이 트리거되는 절차.

</details>

```text
[부모 PK 데이터 갱신/삭제 요청]
                  │
                  ▼
┌────────────────────────────────────────────────────────┐
│ 자식 FK 연쇄 행동 규칙 (Referential Action)            │
├────────────────────────────────────────────────────────┤
│ 1. 참조 자식 존재 확인                                │
│ 2. 선언된 참조 동작 판정                              │
│ 3. 거부•연쇄 변경•참조 해제                           │
│ 4. 제약 재검증•결과 확정                              │
└────────────────────────────────────────────────────────┘
```

### 동작 원리

1. 참조 자식 존재 확인: FK 인덱스로 종속 행 탐색.
2. 선언된 참조 동작 판정: RESTRICT•CASCADE 등 선택.
3. 거부•연쇄 변경•참조 해제: 업무 정책에 맞게 실행.
4. 제약 재검증•결과 확정: 성공은 커밋, 위반은 롤백.

#### 한줄 요약

- 주문 번호가 겹치지 않고 고객 번호가 실제 고객을 가리킬 때만 주문을 저장한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Dual Pillars of Relational Model**: E.F. Codd의 관계형 모델을 떠받치는 2대 핵심 기둥인 개체 무결성과 참조 무결성.

</details>

| 비교 항목 | 개체 무결성 (Entity Integrity) | 참조 무결성 (Referential Integrity) |
|:---|:---|:---|
| 보호 범위 | **단일 릴레이션 내부의 행 식별** | **두 릴레이션 간의 관계 정합성** |
| 제약 선언 위치 | 테이블 정의 시 `PRIMARY KEY` 지정 | 테이블 정의 시 `FOREIGN KEY ... REFERENCES` |
| `NULL` 값 허용 여부 | **기본키 구성 열은 `NULL` 불가** | **FK 열 정의에 따라 `NULL` 허용 가능** |
| 런타임 검사 오버헤드| 매우 적음 (Unique Index 기반 탐색) | 상대적 큼 (부모 테이블 인덱스 조인 검사) |

#### 한줄 요약

- 개체 무결성은 기록의 이름표를, 참조 무결성은 기록 사이의 연결을 지킨다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Surrogate PK & FK Indexing**: 비즈니스 자연키 대신 대리키(Surrogate Key)를 PK로 사용하여 개체 무결성을 보호하고, FK에는 반드시 B-Tree 인덱스를 생성해 참조 무결성 검사 속도 확보.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 자연키(이메일 등)를 PK로 써서 개체 무결성 갱신 여파 파행 | **Surrogate Key (Auto-Increment / UUID)를 PK로 지정** | PK 불변성 확보 |
| 부모 삭제 시 자식 참조 탐색•잠금 지연 | 실행 계획에 따라 **FK 인덱스** 설계 | 참조 검사 범위 축소 |
| `CASCADE` 설정 오남용으로 인한 전사 데이터 무단 삭제 | **기본 `RESTRICT` 사용 및 필요시 앱 단 소프트 삭제 (Soft Delete)**| 데이터 유실 차단 |

> 사례: **쇼핑몰 회원-주문 테이블 간의 PK Surrogate Key 설정 및 FK B-Tree 인덱싱**

#### 한줄 요약

- 부모를 지울 때 자식을 막을지, 함께 지울지, 연결만 끊을지를 업무 의미에 맞게 정해야 한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **개체•참조 무결성 수립 기준(Entity & Referential Standards)**: PK 식별 유일성, FK 참조 정합성 및 Cascading 삭제 수용성에 의거한 체계.

</details>

- 행 식별은 **PK**, 관계 생명주기는 **FK•참조 동작**으로 통제

#### 한줄 요약

- 식별•참조 정책 선택 기준은 겹치지 않는 이름표와 끊어지지 않는 연결을 함께 보장한다.
