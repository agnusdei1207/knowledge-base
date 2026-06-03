+++
title = "75. 참조 무결성 (Referential Integrity) - 외래 키 값은 참조하는 릴레이션의 기본키 값이거나 NULL이어야 함"

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) (Referential Integrity)은 자식 행의 [외래 키](/knowledge-base/studynote/05_database/02_modeling_normalization/072_foreign_key_fk/) (Foreign Key) 값이 반드시 부모 테이블에 존재하는 기본 키 값이거나 NULL이어야 한다는 규칙이다.
> 2. **가치**: ON DELETE CASCADE 같은 동작 규칙은 데이터 삭제가 전파될지, 차단될지, 빈값으로 바뀔지를 명시해 애플리케이션의 숨은 버그를 줄이고 고아 레코드(Orphan Record) 생성을 방지한다.
> 3. **판단 포인트**: CASCADE는 편하지만 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)·정산·이력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에는 과삭제 위험이 있으므로, 의도된 소유 관계(부모 없이 자식이 의미 없는 경우)일 때만 사용해야 한다.

---

## Ⅰ. 개요 및 필요성

관계형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스는 테이블 간 연결이 많기 때문에, 한쪽이 지워졌는데 다른 쪽이 그대로 남는다면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 금방 꼬인다. [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 이런 "고아 행(Orphan Row)"을 막기 위한 안전장치다.

SQL (Structured Query Language)에서 [외래 키](/knowledge-base/studynote/05_database/02_modeling_normalization/072_foreign_key_fk/) 제약은 단순한 문법이 아니라 데이터 생명주기(Lifecycle) 정책이다. 부모 행이 사라질 때 자식도 같이 사라질지, 삭제를 막을지, 빈값으로 남길지를 미리 정해야 운영 중 예외를 줄일 수 있다.

### 참조 무결성이 없으면 생기는 문제



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">상황</div><div class="kb-diagram-note">고객(Customer) 테이블에서 고객 C001을 삭제했을 때:</div></div>
<div class="kb-diagram-note">고객 테이블:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">cust_id</div><div class="kb-diagram-cell">name</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">C002</div><div class="kb-diagram-cell">이순신</div><div class="kb-diagram-cell">← C001 행이 삭제됨</div></div>
<div class="kb-diagram-note">주문 테이블 (참조 무결성 없음):</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">order_id</div><div class="kb-diagram-cell">cust_id</div><div class="kb-diagram-cell">amount</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">O1001</div><div class="kb-diagram-cell">C001</div><div class="kb-diagram-cell">50000</div><div class="kb-diagram-cell">← 부모 없는 고아 행!</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">O1002</div><div class="kb-diagram-cell">C002</div><div class="kb-diagram-cell">30000</div></div>
<div class="kb-diagram-note">결과: 주문 O1001은 어느 고객의 주문인지 알 수 없음</div>
</div>
</div>



이 규칙이 없으면 조인은 되지만 의미는 무너진다.

- **📢 섹션 요약 비유**: 전화번호부에서 연결선이 끊기면 장부가 아니라 조각이 된다. 참조 무결성은 이 연결선을 항상 유효하게 유지하는 규칙이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[외래 키](/knowledge-base/studynote/05_database/02_modeling_normalization/072_foreign_key_fk/)는 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)만 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 것이 아니라, 갱신과 삭제에 대한 동작도 함께 정의한다. 즉 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 "존재 여부"와 "변경 전파"를 같이 다루는 제약이다.

### 외래 키 동작 옵션 (ON DELETE / ON UPDATE)

| 동작 옵션 | 의미 | 주의점 | 적합한 상황 |
| :--- | :--- | :--- | :--- |
| RESTRICT / NO ACTION | 부모 삭제/갱신 차단 | 가장 보수적, 애플리케이션이 순서를 제어해야 함 | 독립적 데이터, 이력 보존 |
| CASCADE | 자식도 함께 변경/삭제 | 과삭제 위험, 다단계 전파 주의 | 주문-주문상세처럼 완전 종속 관계 |
| SET NULL | 자식 FK를 NULL로 변경 | FK 컬럼이 NULL 허용이어야 함 | 선택 관계, 부모 없어도 자식 의미 있는 경우 |
| SET DEFAULT | 자식 FK를 기본값으로 변경 | 기본값의 의미 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 필요 | 기본 카테고리, 미분류 항목 존재 시 |

### 참조 무결성 동작 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">부모 테이블 (Parent) 자식 테이블 (Child)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Customer</div><div class="kb-diagram-cell">Order</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">cust_id (PK)</div><div class="kb-diagram-cell">◄</div><div class="kb-diagram-cell">cust_id (FK → Customer)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">name</div><div class="kb-diagram-cell">order_id (PK)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">email</div><div class="kb-diagram-cell">amount</div></div>
<div class="kb-diagram-note">부모 행 삭제 시도:</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">FK 제약조건 검사</div>
<div class="kb-diagram-tree-item" style="--depth:2">RESTRICT: 삭제 거부 → 오류 반환</div>
<div class="kb-diagram-tree-item" style="--depth:2">CASCADE: 자식 행도 함께 삭제</div>
<div class="kb-diagram-tree-item" style="--depth:2">SET NULL: 자식의 cust_id를 NULL로 변경</div>
<div class="kb-diagram-tree-item" style="--depth:2">SET DEFAULT: 자식의 cust_id를 기본값으로 변경</div>
</div>
</div>



### 외래 키 제약 SQL 예시

```sql
-- 기본 외래 키 정의
CREATE TABLE Orders (
    order_id   INT          PRIMARY KEY,
    cust_id    VARCHAR(10)  NOT NULL,
    amount     DECIMAL(10,2),
    FOREIGN KEY (cust_id)
        REFERENCES Customer(cust_id)
        ON DELETE RESTRICT    -- 부모 삭제 시 차단
        ON UPDATE CASCADE     -- 부모 PK 변경 시 자식 FK도 변경
);

-- CASCADE 예시 (주문-주문상세)
CREATE TABLE OrderDetail (
    order_id    INT    NOT NULL,
    line_no     INT    NOT NULL,
    product_id  VARCHAR(10),
    quantity    INT,
    PRIMARY KEY (order_id, line_no),
    FOREIGN KEY (order_id)
        REFERENCES Orders(order_id)
        ON DELETE CASCADE  -- 주문 삭제 시 상세도 함께 삭제
);

-- SET NULL 예시 (직원-부서)
CREATE TABLE Employee (
    emp_id   INT          PRIMARY KEY,
    dept_id  VARCHAR(10),  -- NULL 허용 (부서 없는 직원 가능)
    name     VARCHAR(50),
    FOREIGN KEY (dept_id)
        REFERENCES Department(dept_id)
        ON DELETE SET NULL  -- 부서 폐지 시 직원의 dept_id를 NULL로
);
```

인덱스가 없으면 제약 검사 비용이 커진다. 그래서 FK는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 규칙이면서 동시에 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 설계와도 연결된다.

- **📢 섹션 요약 비유**: 문은 잠그고, 열쇠는 정해진 사람에게만 준다. 참조 무결성은 그 문과 열쇠의 관계를 데이터베이스가 보장하는 규칙이다.

---

## Ⅲ. 비교 및 연결

[참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 "존재하는 부모를 가리키는가"를 묻고, 개체 무결성(Entity Integrity)은 "기본키가 비어 있지 않은가"를 묻는다. 둘은 비슷해 보이지만 대상이 다르다.

### 무결성 유형 간 비교

| 비교 축 | 개체 무결성 | 참조 무결성 | 도메인 무결성 |
| :--- | :--- | :--- | :--- |
| 대상 | 기본 키 컬럼 | 외래 키 컬럼 | 일반 데이터 컬럼 |
| 보장하는 것 | 행의 유일 식별 | 관계의 유효성 | 값의 허용 범위 |
| 위반 현상 | NULL PK, 중복 행 | 고아 레코드 | 음수 나이, 잘못된 날짜 |
| DBMS 구현 | PRIMARY KEY 제약 | FOREIGN KEY 제약 | CHECK 제약, 타입 |

### 참조 무결성 vs CASCADE 비교

| 비교 축 | 참조 무결성 | CASCADE |
| :--- | :--- | :--- |
| 목적 | 잘못된 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 차단 | 변경/삭제 전파 정책 지정 |
| 성격 | 규칙 (Rule) | 행동 (Action) |
| 위험 | 고아 행 생성 | 의도치 않은 대량 삭제 |
| 적용 범위 | 모든 FK 관계 | 소유(Ownership) 관계에 한정 |

### 참조 무결성 vs 소프트 삭제(Soft Delete)

또 하나의 경계는 CASCADE와 소프트 삭제(Soft Delete)다. 이력과 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)가 중요한 시스템은 물리 삭제(Hard Delete)보다 논리 삭제(Soft Delete)가 더 안전한 경우가 많다.

| 방식 | 방법 | 이력 | 위험 |
| :--- | :--- | :--- | :--- |
| 물리 삭제 (Hard Delete) | 행 자체를 제거 | 없음 | CASCADE 과삭제 |
| 논리 삭제 (Soft Delete) | is_deleted 플래그 등으로 표시 | 보존됨 | 쿼리 복잡도 증가 |

- **📢 섹션 요약 비유**: 열쇠가 맞는지 확인하는 일(참조 무결성)과 문을 같이 여는 일(CASCADE)은 다른 역할이다. 중요한 이력이 있는 곳에는 문을 함부로 같이 열면 안 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 자식의 생명주기가 부모에 완전히 종속될 때만 CASCADE를 쓴다. 주문(Order)과 주문상세(OrderDetail)처럼 부모 없이는 자식이 의미 없는 경우가 대표적이다.

### 설계 판단 체크리스트

1. **FK 컬럼에 인덱스가 있는가?** — 외래 키 조회 및 제약 검사 시 인덱스가 없으면 풀 스캔이 발생한다.
2. <strong>대량 삭제 시 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a> 범위를 감당할 수 있는가?</strong> — CASCADE가 수천~수만 건의 자식 행을 삭제하면 락(Lock) 경합과 로그 증가가 발생할 수 있다.
3. <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a>·정산·법적 보존 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>에 물리 삭제를 쓰지 않는가?</strong> — 법적 보존 의무가 있는 데이터는 절대 물리 삭제하면 안 된다.
4. **다단계 CASCADE가 발생하지 않는가?** — A→B→C처럼 연쇄 CASCADE는 예측 범위를 벗어날 수 있다.
5. **NoSQL 환경에서도 참조 무결성이 필요한가?** — MongoDB 같은 NoSQL은 FK 제약이 없으므로, 애플리케이션 레벨이나 데이터 파이프라인에서 정합성을 관리해야 한다.

### 안티패턴

- **"편하니까 CASCADE"**: 특히 다단계 CASCADE는 작은 실수 하나로 많은 행을 날릴 수 있다.
- **FK 제약 비활성화**: 마이그레이션 편의상 FK를 끄는 경우, 작업 후 반드시 재활성화하고 데이터 정합성을 검증해야 한다.
- **소프트 삭제와 CASCADE 혼용**: 논리 삭제된 부모가 CASCADE에서 제외되지 않으면 잘못된 정합성 관리가 된다.
- **애플리케이션만 믿는 설계**: API 레이어에서 순서를 보장하더라도 배치 작업, 직접 SQL 접근, 외부 시스템이 우회할 수 있다.

### 외래 키 인덱스 전략

```sql
-- 외래 키 컬럼에는 반드시 인덱스를 생성한다
CREATE INDEX idx_order_cust_id ON Orders (cust_id);

-- 복합 외래 키의 경우 첫 번째 컬럼부터 인덱스 구성
CREATE INDEX idx_orderdetail_order ON OrderDetail (order_id, line_no);
```

- **📢 섹션 요약 비유**: 편리한 자동문도 방향을 잘못 잡으면 위험하다. CASCADE는 자동문과 같아서, 방향(삭제 정책)을 신중하게 설정해야 한다.

---

## Ⅴ. 기대효과 및 결론

FK 제약은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질의 마지막 선이다. 사람이 깜빡해도 DB가 막아 주므로, 결함이 코드 레벨로 번지기 전에 멈출 수 있다.

### 참조 무결성 도입 효과

| 항목 | 효과 |
| :--- | :--- |
| 고아 레코드 방지 | 부모 없는 자식 행 생성이 DB 레벨에서 차단됨 |
| 조인 신뢰성 | FK-PK 연결이 항상 유효하여 JOIN 결과 보장 |
| 데이터 품질 | 배치 작업, 외부 연동에서도 규칙 자동 적용 |
| 디버깅 용이성 | 참조 오류 발생 시 원인 위치를 DB가 즉시 알려줌 |
| 삭제 전파 통제 | ON DELETE 정책으로 연쇄 삭제 범위 명시적 관리 |

결국 기억할 것은, [외래 키](/knowledge-base/studynote/05_database/02_modeling_normalization/072_foreign_key_fk/)는 단지 연결선이 아니라 관계의 정책이라는 점이다. 어떤 연결은 끊으면 안 되고, 어떤 연결은 같이 움직여야 하며, 그 기준을 DB가 대신 보증한다.

- **📢 섹션 요약 비유**: 가족사진의 이름표가 맞아야 누구인지 알 수 있다. 참조 무결성은 이름표와 사진이 항상 일치하도록 보장하는 규칙이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Primary Key (PK) | 부모 테이블의 고유 식별자, FK가 참조하는 대상 |
| Foreign Key (FK) | 부모를 가리키는 연결 컬럼, 참조 무결성의 구현체 |
| CASCADE | 부모 변경/삭제를 자식에게 전파하는 동작 |
| RESTRICT | 자식이 있을 때 부모 삭제를 차단하는 동작 |
| SET NULL | 부모 삭제 시 자식 FK를 NULL로 만드는 동작 |
| 고아 레코드 (Orphan Record) | 참조 무결성 위반 시 발생하는 부모 없는 자식 행 |
| 소프트 삭제 (Soft Delete) | 물리 삭제 대신 논리 삭제 플래그로 이력 보존 |
| 인덱스 (Index) | FK 컬럼 검색 성능 향상을 위한 필수 구성 요소 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Codd 관계형 모델 (1970)</div>
<div class="kb-diagram-note">↓ 참조 무결성 원칙 정립</div>
<div class="kb-diagram-note">SQL 표준 (ANSI SQL-89)</div>
<div class="kb-diagram-note">↓ FOREIGN KEY 제약 문법 표준화</div>
<div class="kb-diagram-note">ON DELETE CASCADE / RESTRICT / SET NULL</div>
<div class="kb-diagram-note">↓ 다단계 CASCADE 위험 인식</div>
<div class="kb-diagram-note">소프트 삭제 패턴 도입</div>
<div class="kb-diagram-note">↓ NoSQL 등장</div>
<div class="kb-diagram-note">애플리케이션 레벨 참조 관리 (NoSQL)</div>
<div class="kb-diagram-note">↓ 분산 DB, 마이크로서비스</div>
<div class="kb-diagram-note">이벤트 기반 데이터 일관성 (Saga 패턴, Outbox 패턴)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 엄마 이름표가 있어야 아이 이름표도 맞아요. 엄마(부모)가 없으면 아이(자식) 이름표도 의미가 없어요.
2. 엄마가 사라지면 아이도 같이 없어질 수 있어요(CASCADE). 하지만 엄마가 없다고 아이를 없애는 건 위험할 수도 있어요.
3. 중요한 기록(이력, 정산)이 있을 때는 이름표만 바꾸고 아이는 남겨 두는 방법(소프트 삭제)을 써요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 75 / 600

← **이전**: [74. 개체 무결성 (Entity Integrity) / 기본 키 (Primary Key)](/knowledge-base/studynote/05_database/02_modeling_normalization/074_entity_integrity_primary_key/)
**다음**: [76. 도메인 무결성 (Domain Integrity) - 속성 값은 정의된 도메인에 속해야 함](/knowledge-base/studynote/05_database/02_modeling_normalization/076_domain_integrity/) →

---
