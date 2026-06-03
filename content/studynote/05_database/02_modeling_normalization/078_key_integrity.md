+++
title = "78. 키 무결성 (Key Integrity)"

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 키 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 PK (Primary Key)가 각 행을 유일하게 식별하고 FK (Foreign Key)가 부모 행을 실제로 가리키게 하는 규칙으로, 관계형 모델의 핵심 기반이다.
> 2. **가치**: 이 규칙이 있어야 중복과 고아 레코드를 막고, 조인(JOIN) 결과를 믿을 수 있으며, 정규화 효과가 실제로 유지된다.
> 3. **판단 포인트**: 기술사는 의미보다 안정성이 높은 키를 선택하고 [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 제약조건으로 강제해야 한다. 자연 키는 의미가 풍부하지만 변경 가능성이 있고, 대리 키는 안정적이나 의미가 없다.

---

## Ⅰ. 개요 및 필요성

키 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 릴레이션의 각 행이 하나의 키로 식별되고, [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 관계가 실제 존재하는 값만 가리키도록 보장하는 규칙이다.
이 규칙이 무너지면 같은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 여러 번 들어가거나, 부모가 사라졌는데 자식만 남는 문제가 생긴다. 그래서 정규화된 모델도 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)이 없으면 신뢰를 잃는다.

### 키 무결성이 보장하는 두 가지 속성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">키 무결성 = 개체 무결성 + 참조 무결성의 실제 구현 기반</div>
<div class="kb-diagram-note">개체 무결성: PK → NOT NULL + UNIQUE</div>
<div class="kb-diagram-note">각 행은 유일하게 식별 가능해야 함</div>
<div class="kb-diagram-note">참조 무결성: FK → 부모 PK 참조</div>
<div class="kb-diagram-note">FK 값은 부모에 존재하거나 NULL이어야 함</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Customer 테이블</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">cust_id(PK)</div><div class="kb-diagram-cell">name</div><div class="kb-diagram-cell">email</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">C001</div><div class="kb-diagram-cell">홍길동</div><div class="kb-diagram-cell">hong@example.com</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">C002</div><div class="kb-diagram-cell">이순신</div><div class="kb-diagram-cell">lee@example.com</div></div>
<div class="kb-diagram-note">↑ PK: 유일 + NOT NULL (개체 무결성)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Order 테이블</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">order_id(PK)</div><div class="kb-diagram-cell">cust_id(FK)</div><div class="kb-diagram-cell">amount</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">O1001</div><div class="kb-diagram-cell">C001</div><div class="kb-diagram-cell">50000</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">O1002</div><div class="kb-diagram-cell">C002</div><div class="kb-diagram-cell">30000</div></div>
<div class="kb-diagram-note">↑ FK: 반드시 Customer.cust_id에 존재 (참조 무결성)</div>
</div>
</div>



- **📢 섹션 요약 비유**: 식별이 흐리면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관계도 같이 흐려진다. 키는 데이터베이스의 기초 공사다.

---

## Ⅱ. 아키텍처 및 핵심 원리

후보키([candidate key](/knowledge-base/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/)) 중 하나가 PK가 되고, 나머지는 UK (Unique Key)로 남을 수 있다. FK는 부모 테이블의 키를 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하면서 [참조 무결성](/knowledge-base/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/)을 유지한다.
PK는 보통 NOT NULL과 UNIQUE를 동시에 만족해야 하고, FK는 삽입·갱신·삭제 규칙까지 함께 설계해야 한다.

### 키 계층 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">전체 속성 집합 (All Attributes)</div>
<div class="kb-diagram-note">↓ 유일성 만족</div>
<div class="kb-diagram-note">슈퍼 키 (Super Key) — 최소성 불필요</div>
<div class="kb-diagram-note">↓ + 최소성 만족</div>
<div class="kb-diagram-note">후보 키 (Candidate Key) — 유일 + 최소</div>
<div class="kb-diagram-note">↓ 대표 선출</div>
<div class="kb-diagram-tree-item" style="--depth:2">기본 키 (Primary Key, PK) — NOT NULL + UNIQUE 강제</div>
<div class="kb-diagram-tree-item" style="--depth:2">대체 키 (Alternate Key, AK) — UNIQUE 제약만 적용</div>
</div>
</div>



### 키 구성 요소 설계 포인트

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| [Candidate Key](/knowledge-base/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/) | 후보 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 집합 | 업무 의미와 안정성을 함께 본다 |
| PK | 대표 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) | 짧고 변하지 않아야 한다 |
| UK (Unique Key) | 대체 유일성 보장 | 중복만 막고 NULL 정책을 확인한다 |
| FK | 부모 행 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) | 고아 레코드 방지와 조인 기준이 된다 |
| [Surrogate Key](/knowledge-base/studynote/12_it_management/05_security_compliance/314_surrogate_key/) | 대리 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경과 변경 안정성을 고려한다 |

### 자연 키 vs 대리 키 선택 SQL 예시

```sql
-- 자연 키(Natural Key) 사용 예시
CREATE TABLE Product_NaturalKey (
    product_code  VARCHAR(20)  PRIMARY KEY,  -- 업무에서 쓰는 코드
    product_name  VARCHAR(100) NOT NULL,
    price         DECIMAL(10,2)
);
-- 문제: 상품 코드가 바뀌면 이를 참조하는 모든 자식 테이블도 변경 필요

-- 대리 키(Surrogate Key) 사용 예시
CREATE TABLE Product_SurrogateKey (
    product_id    INT          PRIMARY KEY AUTO_INCREMENT,  -- 의미 없는 순번
    product_code  VARCHAR(20)  UNIQUE NOT NULL,  -- 자연 키는 UNIQUE로 관리
    product_name  VARCHAR(100) NOT NULL,
    price         DECIMAL(10,2)
);
-- 장점: product_code가 바뀌어도 FK는 product_id를 참조하므로 연쇄 영향 없음

-- 분산 환경의 UUID 키
CREATE TABLE Event (
    event_id   CHAR(36)     PRIMARY KEY DEFAULT (UUID()),  -- UUID v4
    event_type VARCHAR(50)  NOT NULL,
    created_at DATETIME     DEFAULT NOW()
);
```

- **📢 섹션 요약 비유**: 후보키, 대표키, [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)키가 역할을 나눠 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 만든다. 역할 분담이 명확할수록 시스템이 안정적이다.

---

## Ⅲ. 비교 및 연결

키 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 엔터티 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)([entity integrity](/knowledge-base/studynote/05_database/02_modeling_normalization/074_entity_integrity_primary_key/))과 [참조 무결성](/knowledge-base/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/)([referential integrity](/knowledge-base/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/))을 실제로 구현하는 바닥 규칙이다. 둘을 함께 봐야 "행은 자기 자신을 잃지 않고, 관계도 끊기지 않는다"는 뜻이 완성된다.
자연키는 업무 의미가 분명하지만 변경 가능성이 있고, 대리키는 의미는 약하지만 안정성과 조인 성능이 좋다. 그래서 키 선택은 의미와 운영을 동시에 봐야 한다.

### 자연 키 vs 대리 키 상세 비교

| 비교축 | 자연 키 (Natural Key) | 대리 키 (Surrogate Key) |
| :--- | :--- | :--- |
| 의미 | 업무상 읽기 쉽다 | 의미는 없다 |
| 안정성 | 업무 변경에 흔들릴 수 있다 | 대체로 안정적이다 |
| 운영성 | 사람이 이해하기 좋다 | 기계 처리에 최적화 |
| 크기 | 문자열 등 클 수 있다 | 정수나 UUID로 일정하다 |
| 분산 환경 | 조합 시 복잡해진다 | UUID/Snowflake ID 활용 가능 |
| 예시 | 주민등록번호, 상품코드 | AUTO_INCREMENT, UUID |

### 키 무결성과 정규화의 관계



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">키 무결성 → 정규화의 기반</div>
<div class="kb-diagram-note">1NF: 모든 속성이 원자값, PK 존재</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">2NF: PK에 완전 함수 종속 (부분 종속 제거)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">3NF: PK에 이행적 함수 종속 제거</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">BCNF: 모든 결정자가 후보 키</div>
<div class="kb-diagram-note">키 무결성이 무너지면 정규화 효과도 무너진다.</div>
</div>
</div>



- **📢 섹션 요약 비유**: 자연키와 대리키는 의미와 안정성 사이의 선택이다. 자주 바뀌는 이름보다 잘 안 바뀌는 번호를 ID로 쓰는 것이 현명하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 안정성, 길이, 의미, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)성, [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 비용을 함께 본다. 특히 키가 바뀌면 연쇄 갱신이 발생하므로, 바뀔 가능성이 낮은 값을 우선한다.
[DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 제약조건으로 강제하고 애플리케이션은 보조 역할만 맡겨야 한다. 앱 코드만 믿으면 배치 작업이나 수동 수정에서 쉽게 깨진다.

### 설계 판단 체크리스트

1. **PK가 짧고 변하지 않는가?** — 문자열 PK는 인덱스 성능이 정수보다 낮다. 변경 가능한 업무 코드는 PK로 쓰지 않는다.
2. **FK가 실제 부모 행을 강제하는가?** — DBMS FOREIGN KEY 제약이 반드시 활성화되어 있어야 한다.
3. **키 변경 시 연쇄 영향이 통제되는가?** — ON UPDATE CASCADE를 설정했다면 영향 범위를 사전에 파악해야 한다.
4. **복합 PK가 과도하게 크지 않은가?** — 복합 PK는 FK를 통해 자식 테이블 전체로 전파되어 저장 공간을 늘린다.
5. **분산 환경에서 PK의 전역 유일성이 보장되는가?** — 멀티 노드 환경에서는 AUTO_INCREMENT 대신 UUID, Snowflake ID, ULID를 고려한다.

### 안티패턴

- **이메일, 전화번호처럼 바뀌기 쉬운 값을 PK로 쓰는 것**: 나중에 PK 변경 시 연결된 모든 FK를 수정해야 한다.
- **편하다는 이유로 FK 제약을 꺼버리는 것**: 단기적으로 편하지만 장기적으로 고아 레코드가 쌓이고 데이터 정합성이 무너진다.
- **PK 없는 테이블 허용**: 일부 로그 테이블에서 의도적으로 PK를 생략하는 경우가 있지만, 쿼리와 관리가 어려워진다.
- **UUID를 VARCHAR로 저장**: UUID를 문자열로 저장하면 인덱스 성능이 크게 떨어진다. BINARY(16) 또는 전용 UUID 타입을 사용한다.

### 인덱스와 키 무결성

```sql
-- PK에는 클러스터드 인덱스가 자동 생성됨 (MySQL InnoDB)
-- FK 컬럼에는 별도로 인덱스를 생성해야 한다
CREATE INDEX idx_order_cust_id ON Orders(cust_id);

-- 복합 PK의 경우 복합 인덱스 자동 생성
-- 추가로 선두 컬럼만의 인덱스가 필요할 수 있다
CREATE INDEX idx_enrollment_student ON Enrollment(student_id);
```

- **📢 섹션 요약 비유**: 제약조건을 DBMS에 걸어야 키 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)이 실제로 살아난다. 약속은 구두로 하지 말고 계약서(제약조건)로 남겨야 한다.

---

## Ⅴ. 기대효과 및 결론

키 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)이 좋으면 중복 제거, 조인 안정성, 장애 복구가 함께 쉬워진다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질은 결국 키 설계에서 출발한다.
[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서는 UUID (Universally Unique Identifier)처럼 전역 유일성과 운영 편의성을 함께 보는 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 전략이 중요해진다.
기술사는 이 주제를 "행을 찾는 표지판과 관계를 지키는 울타리"로 기억하면 된다.

### 도입 효과

| 항목 | 효과 |
| :--- | :--- |
| 중복 방지 | PK 제약으로 동일 데이터 이중 삽입 차단 |
| 조인 정확성 | FK-PK 연결이 항상 유효하여 JOIN 결과 신뢰 |
| 쿼리 성능 | 클러스터드 인덱스로 PK 기반 검색 최적화 |
| 장애 복구 | 정합성 있는 데이터로 복구 범위 축소 |
| 유지보수성 | 키 구조가 명확하면 스키마 변경 영향도 파악 용이 |

### 미래 전망

분산 데이터베이스, 마이크로서비스 환경에서는 글로벌 유일 식별자(UUID v4, ULID, Snowflake ID)가 표준이 되어가고 있다. 이벤트 소싱(Event Sourcing) 패턴에서는 불변(Immutable) 이벤트 ID가 실질적인 개체 식별자가 된다. NoSQL에서도 키 설계의 중요성은 동일하며, 파티션 키와 정렬 키의 조합이 관계형 DB의 PK+인덱스 역할을 대신한다.

- **📢 섹션 요약 비유**: 좋은 키는 품질과 운영의 첫 번째 안전장치다. 기초가 튼튼해야 위에 무엇을 쌓아도 무너지지 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| PK (Primary Key) | 행을 유일하게 식별하는 대표 키 |
| FK (Foreign Key) | 부모 행과 자식 행을 연결하는 참조 키 |
| UK (Unique Key) | 대체 유일성을 보장하는 후보 키 |
| [Candidate Key](/knowledge-base/studynote/05_database/02_modeling_normalization/069_candidate_key_uniqueness_minimality/) | 유일성+최소성을 만족하는 후보 식별자 집합 |
| [Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | PK 기반으로 함수 종속성을 분리하는 과정 |
| UUID | 분산 환경의 전역 유일 식별자 (36자 문자열) |
| ULID | 시간순 정렬 가능한 분산 유일 식별자 |
| Surrogate Key | 업무 의미 없는 대리 식별자 (AUTO_INCREMENT 등) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">도메인 속성 정의</div>
<div class="kb-diagram-note">↓ 유일성·최소성 분석</div>
<div class="kb-diagram-note">후보 키 선택</div>
<div class="kb-diagram-note">↓ 대표 키 지정</div>
<div class="kb-diagram-note">PK/UK 확정 + DBMS 제약 적용</div>
<div class="kb-diagram-note">↓ 관계 연결</div>
<div class="kb-diagram-note">FK 설계 (ON DELETE/UPDATE 정책)</div>
<div class="kb-diagram-note">↓ 분산 환경</div>
<div class="kb-diagram-note">UUID / ULID / Snowflake ID 전략</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">정규화 + 무결성 검증</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 도서관 책마다 바코드(기본 키)가 있어야 책을 헷갈리지 않는 것과 같다.
2. 다른 책을 빌릴 때도 번호표(외래 키)를 보고 연결해야 반납이 틀리지 않는다.
3. 번호표가 자꾸 바뀌면 혼란이 생기니, 잘 안 바뀌는 표식(대리 키)을 쓰는 게 좋다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 78 / 600

← **이전**: [77. 사용자 정의 무결성 (User-defined Integrity) - 업무 규칙에 따른 제약 (CHECK 제약조건 등)](/knowledge-base/studynote/05_database/02_modeling_normalization/077_user_defined_integrity_check_trigger/)
**다음**: [079. NULL 무결성과 NOT NULL 제약조건](/knowledge-base/studynote/05_database/02_modeling_normalization/079_null_integrity_not_null/) →

---
