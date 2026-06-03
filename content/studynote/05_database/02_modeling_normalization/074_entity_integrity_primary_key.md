+++
title = "74. 개체 무결성 (Entity Integrity) / 기본 키 (Primary Key)"

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 개체 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 [기본 키](/knowledge-base/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/)가 NULL이 아니고 각 행을 유일하게 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)해야 한다는 규칙이다.
> 2. **가치**: 테이블의 모든 행이 반드시 식별 가능해야 데이터 정합성과 관계 조인(JOIN)의 신뢰성이 보장된다.
> 3. **판단 포인트**: [기본 키](/knowledge-base/studynote/05_database/02_modeling_normalization/070_primary_key_alternate_key/)는 절대 NULL이 될 수 없고 중복될 수 없으며, 이 두 조건이 동시에 만족되어야 개체 무결성이 성립한다.

---

## Ⅰ. 개요 및 필요성

관계형 데이터베이스(Relational Database)에서 테이블은 하나 이상의 행(Row, 튜플)으로 구성된다. 각 행이 동일한 데이터를 가지거나, 어떤 행인지 식별할 수 없다면 데이터베이스로서의 기능을 잃게 된다. 이 문제를 근본적으로 막는 것이 개체 무결성(Entity Integrity)이다.

개체 무결성은 1970년대 E.F. Codd가 관계형 모델을 제안하면서 명시한 핵심 제약조건 중 하나다. 관계형 모델에서 "릴레이션(Relation)"은 수학적 집합(Set)과 같아서 동일한 원소가 두 번 등장할 수 없다. 이 집합 성질을 실제 테이블에서 보장하기 위한 메커니즘이 바로 기본 키(Primary Key, PK)다.

개체 무결성이 없으면 다음과 같은 문제가 발생한다.
- 어떤 행이 어떤 실세계 개체를 나타내는지 알 수 없다.
- 외래 키(FK)가 어느 행을 가리키는지 불분명해진다.
- 조인(JOIN) 결과가 예측 불가능해진다.
- 집계(GROUP BY, COUNT) 결과가 오염된다.

현대 DBMS(Database Management System)는 PK 컬럼에 자동으로 NOT NULL과 UNIQUE 제약을 부여한다. 이는 개체 무결성을 시스템 레벨에서 강제하는 구현 방식이다.

- **📢 섹션 요약 비유**: 학교 학생 명부에서 학번이 없거나 같은 학번이 두 명이면 성적 관리가 불가능하다. 학번이 바로 기본 키이며, 개체 무결성은 "모든 학생에게는 고유한 학번이 있어야 한다"는 규칙이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 기본 키의 두 가지 핵심 조건

기본 키는 다음 두 가지 조건을 반드시 동시에 만족해야 한다.

| 조건 | 의미 | DBMS 제약 |
| :--- | :--- | :--- |
| 유일성 (Uniqueness) | 테이블 내 모든 행에서 PK 값이 서로 달라야 한다 | UNIQUE 제약 자동 적용 |
| 비널성 (Not-Null) | PK 컬럼에 NULL 값이 허용되지 않는다 | NOT NULL 제약 자동 적용 |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">릴레이션(테이블) 내부 구조:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">STUDENT 테이블</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">student_id</div><div class="kb-diagram-cell">name</div><div class="kb-diagram-cell">dept</div><div class="kb-diagram-cell">grade</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(PK)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1001</div><div class="kb-diagram-cell">홍길동</div><div class="kb-diagram-cell">컴퓨터</div><div class="kb-diagram-cell">3</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1002</div><div class="kb-diagram-cell">이순신</div><div class="kb-diagram-cell">경영</div><div class="kb-diagram-cell">2</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1003</div><div class="kb-diagram-cell">강감찬</div><div class="kb-diagram-cell">컴퓨터</div><div class="kb-diagram-cell">4</div></div>
<div class="kb-diagram-note">↑ PK: NOT NULL + UNIQUE 보장</div>
<div class="kb-diagram-note">↑ NULL 삽입 시도 → 거부(REJECT)</div>
<div class="kb-diagram-note">↑ 중복 값 삽입 시도 → 거부(REJECT)</div>
</div>
</div>



### 기본 키 선정 원칙

좋은 기본 키를 선정하려면 다음 원칙을 따른다.

| 원칙 | 설명 | 위반 예시 |
| :--- | :--- | :--- |
| 최소성 (Minimality) | PK를 구성하는 속성 수를 최소화한다 | 이름+주소+생일을 모두 PK로 쓰는 것 |
| 안정성 (Stability) | PK 값이 자주 변하면 안 된다 | 이메일, 전화번호를 PK로 쓰는 것 |
| 의미 분리 (Meaninglessness) | 대리 키(Surrogate Key) 사용 시 비즈니스 의미 없이 순수 식별만 담당 | 자동증가(Auto Increment) ID 사용 |
| 단순성 (Simplicity) | 가능하면 단일 컬럼으로 구성한다 | 복합 PK는 조인 비용이 높아진다 |

### 복합 기본 키 (Composite Primary Key)

단일 컬럼으로 유일성을 보장할 수 없을 때 두 개 이상의 컬럼을 조합하여 PK를 구성한다.

```sql
-- 복합 기본 키 예시: 수강(Enrollment) 테이블
CREATE TABLE Enrollment (
    student_id   INT          NOT NULL,
    course_id    VARCHAR(10)  NOT NULL,
    semester     VARCHAR(6)   NOT NULL,
    grade        CHAR(2),
    PRIMARY KEY (student_id, course_id, semester)  -- 복합 PK
);
```

이 경우 (student_id, course_id, semester)의 조합이 유일하고 NULL이 없어야 한다.

### 개체 무결성 위반 시나리오

```sql
-- 시나리오 1: NULL 삽입 시도
INSERT INTO Student (student_id, name) VALUES (NULL, '김철수');
-- 오류: Column 'student_id' cannot be null

-- 시나리오 2: 중복 값 삽입 시도
INSERT INTO Student (student_id, name) VALUES (1001, '박영희');
-- 오류: Duplicate entry '1001' for key 'PRIMARY'

-- 올바른 삽입
INSERT INTO Student (student_id, name) VALUES (1004, '김영수');
-- 성공: student_id=1004는 유일하고 NOT NULL
```

- **📢 섹션 요약 비유**: 출입카드 시스템에서 카드 번호가 없거나 같은 번호가 두 장이면 게이트가 혼란에 빠진다. 기본 키는 이 카드 번호처럼 "절대 비어있지 않고 절대 겹치지 않는" 규칙이다.

---

## Ⅲ. 비교 및 연결

### 무결성 제약조건 유형 비교

| 구분 | 개체 무결성 | 참조 무결성 | 도메인 무결성 | 사용자 정의 무결성 |
| :--- | :--- | :--- | :--- | :--- |
| 대상 | 기본 키 | 외래 키 | 컬럼 값 | 업무 규칙 |
| 보장하는 것 | 행의 유일 식별 | 관계의 일관성 | 값의 범위/형식 | 비즈니스 규칙 |
| 구현 방법 | PK 제약 | FK 제약 | CHECK, 타입 | TRIGGER, CHECK |
| 위반 예시 | NULL PK, 중복 PK | 존재하지 않는 부모 참조 | 음수 나이, 미래 생일 | 종료일 < 시작일 |

### 기본 키 vs 후보 키 vs 대체 키

| 개념 | 정의 | 특징 |
| :--- | :--- | :--- |
| 슈퍼 키 (Super Key) | 유일성만 만족하는 속성 집합 | 불필요한 속성 포함 가능 |
| 후보 키 (Candidate Key) | 유일성 + 최소성 만족 | PK가 될 자격 있음 |
| 기본 키 (Primary Key) | 후보 키 중 대표로 선택된 키 | NOT NULL + UNIQUE 강제 |
| 대체 키 (Alternate Key) | PK로 선택되지 않은 후보 키 | UNIQUE 제약만 적용 |
| 외래 키 (Foreign Key) | 다른 테이블 PK를 참조 | 참조 무결성 보장 |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">속성 집합 중 키 계층:</div>
<div class="kb-diagram-note">슈퍼 키 ⊇ 후보 키 ⊇ (기본 키 | 대체 키)</div>
<div class="kb-diagram-note">예) Student 테이블:</div>
<div class="kb-diagram-tree-item" style="--depth:0">student_id: 후보 키 → PK 선택됨</div>
<div class="kb-diagram-tree-item" style="--depth:0">resident_number: 후보 키 → 대체 키로 남음 (UNIQUE 제약)</div>
<div class="kb-diagram-tree-item" style="--depth:0">(student_id, name): 슈퍼 키 (최소성 불만족)</div>
</div>
</div>



- **📢 섹션 요약 비유**: 운전면허증과 주민등록번호는 모두 사람을 유일하게 식별할 수 있지만, 국가가 대표 식별자로 주민등록번호를 선택한 것과 같다. 이것이 기본 키 선택이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **기본 키가 NULL이 될 가능성은 없는가?** — 업무 흐름상 PK 값이 나중에 채워지는 구조라면 설계를 재검토해야 한다.
2. **유일성이 실제로 보장되는가?** — 자동증가(Auto Increment)나 UUID 같은 대리 키는 DBMS가 유일성을 보장하지만, 자연 키는 비즈니스 변화로 중복이 생길 수 있다.
3. **복합 PK가 불필요하게 크지 않은가?** — 복합 PK는 FK를 참조하는 모든 자식 테이블에도 동일하게 전파되므로, 설계 비용을 함께 고려해야 한다.
4. **변경 빈도가 낮은 속성을 PK로 선택했는가?** — PK 변경은 FK를 통해 연결된 모든 자식 행에 연쇄 영향을 준다.
5. **대리 키(Surrogate Key)와 자연 키(Natural Key) 중 적절한 선택을 했는가?** — 분산 환경에서는 UUID 방식이 유리하고, 단일 시스템에서는 정수 자동증가가 성능에 유리하다.

### 안티패턴

- **NULL 허용 기본 키**: PK 컬럼에 NULL을 허용하는 것은 관계형 모델의 근본을 위반한다. "나중에 채운다"는 이유로 NULL을 허용하면 안 된다.
- **의미 있는 값을 PK로 사용**: 전화번호, 이메일, 상품코드처럼 비즈니스 정책에 따라 바뀔 수 있는 값을 PK로 쓰면 나중에 대규모 수정이 발생한다.
- **중복 가능한 식별자**: 배치 작업이나 마이그레이션 과정에서 PK 제약을 일시적으로 해제하는 것은 데이터 오염을 야기할 수 있다.
- **PK와 FK 혼동**: 자식 테이블의 FK 컬럼을 PK로 착각하거나, PK가 아닌 컬럼을 FK로 참조하는 설계 오류가 발생할 수 있다.
- **식별 규칙을 애플리케이션에만 위임**: DB 레벨 제약 없이 애플리케이션 코드만 믿으면 배치 작업, 관리자 스크립트, 외부 연동에서 무결성이 깨질 수 있다.

### 기술사 관점 핵심 서술

기술사 답안에서 개체 무결성을 서술할 때는 다음 세 가지 관점을 포함한다.
1. **정의**: 기본 키의 유일성과 비널성을 보장하는 규칙
2. **구현**: DBMS의 PK 제약조건이 NOT NULL + UNIQUE를 자동 강제
3. **영향**: 참조 무결성(외래 키 관계)과 연동되며, 조인 정확성의 기반이 됨

- **📢 섹션 요약 비유**: 우편 시스템에서 우편번호가 없거나 같은 번호가 두 동네에 붙어 있으면 배달이 불가능하다. 개체 무결성은 이 우편번호처럼 "존재하고 유일해야 함"을 강제하는 규칙이다.

---

## Ⅴ. 기대효과 및 결론

개체 무결성을 올바르게 적용하면 다음과 같은 효과를 얻는다.

### 정량적 효과

| 항목 | 효과 |
| :--- | :--- |
| 데이터 정확도 | 중복 행, 고아 레코드 제거로 데이터 품질 향상 |
| 조인 신뢰도 | PK-FK 연결이 명확해 잘못된 JOIN 결과 차단 |
| 쿼리 성능 | DBMS가 PK에 클러스터드 인덱스(Clustered Index) 자동 생성, 검색 속도 향상 |
| 운영 안전성 | 배치/마이그레이션 중 실수로 중복 데이터 삽입 차단 |

### 정성적 효과

- 모델링 단계에서 엔터티 경계를 명확히 하게 한다.
- 관계 무결성(Referential Integrity)과 연계되어 전체 DB 신뢰성의 기반이 된다.
- 분산 데이터베이스, 마이크로서비스 환경에서도 글로벌 유일 식별자(UUID, ULID)를 통해 동일한 원칙이 유지된다.

### 미래 전망

클라우드 네이티브 환경에서는 자동증가 정수 PK 대신 분산 환경에서도 유일성이 보장되는 UUID v4, ULID(Universally Unique Lexicographically Sortable Identifier)가 사용된다. 또한 이벤트 소싱(Event Sourcing) 패턴에서는 이벤트 ID가 실질적인 개체 식별자 역할을 한다.

- **📢 섹션 요약 비유**: 도서관 장서 관리에서 ISBN(국제표준도서번호)이 없는 책은 검색도 대출도 반납도 할 수 없다. 개체 무결성은 모든 데이터에 ISBN을 붙이는 원칙이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 후보 키 (Candidate Key) | PK 선택의 대상이 되는 유일 최소 속성 집합 |
| 대체 키 (Alternate Key) | PK로 선택되지 않은 후보 키, UNIQUE 제약 적용 |
| 외래 키 (Foreign Key) | PK를 참조하여 테이블 간 관계를 연결 |
| 참조 무결성 (Referential Integrity) | FK가 실존하는 PK만 가리키도록 보장 |
| 도메인 무결성 (Domain Integrity) | 컬럼 값의 타입/범위 제약 |
| 정규화 (Normalization) | PK를 기반으로 함수 종속성을 분리하는 과정 |
| 클러스터드 인덱스 (Clustered Index) | DBMS가 PK에 자동 생성하는 물리 정렬 인덱스 |
| UUID / ULID | 분산 환경에서의 전역 유일 식별자 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Codd 관계형 모델 (1970)</div>
<div class="kb-diagram-note">↓ 개체 무결성 원칙 정립</div>
<div class="kb-diagram-note">기본 키 (PK) 개념 도입</div>
<div class="kb-diagram-note">↓ NOT NULL + UNIQUE 제약</div>
<div class="kb-diagram-note">단일 컬럼 PK → 복합 PK</div>
<div class="kb-diagram-note">↓ 분산 환경 대두</div>
<div class="kb-diagram-note">자동증가 정수 PK → UUID / ULID / Snowflake ID</div>
<div class="kb-diagram-note">↓ 이벤트 소싱 등 아키텍처 다양화</div>
<div class="kb-diagram-note">현재: 이벤트 ID, 분산 ID, 글로벌 유일성 보장 전략</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 학교에서 선생님이 학생을 부를 때 이름이 같을 수 있어서 학번을 써요. 학번이 바로 기본 키예요.
2. 학번은 절대 비어 있으면 안 되고(NULL 불가), 두 학생이 같은 학번을 가지면 안 돼요(중복 불가).
3. 개체 무결성은 "모든 학생에게 고유한 학번이 꼭 있어야 해요"라는 학교 규칙이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 74 / 600

← **이전**: [73. 무결성 제약조건 (Integrity Constraints)](/knowledge-base/studynote/05_database/02_modeling_normalization/073_integrity_constraints_overview/)
**다음**: [75. 참조 무결성 (Referential Integrity) - 외래 키 값은 참조하는 릴레이션의 기본키 값이거나 NULL이어야 함](/knowledge-base/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/) →

---
