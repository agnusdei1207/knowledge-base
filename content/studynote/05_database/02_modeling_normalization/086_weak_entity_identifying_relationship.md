+++
title = "86. 약한 개체 (Weak Entity) - 이중 사각형, 부모 개체에 종속 (식별 관계)"

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Weak Entity(약한 개체)는 ER (Entity-Relationship) 모델에서 독립 PK를 갖지 못하고 부모 개체(Strong Entity)에 종속되는 개체다. 자체적으로는 유일하게 식별될 수 없다.
> 2. **가치**: 부분 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)(Partial Key)와 [식별 관계](/knowledge-base/studynote/05_database/02_modeling_normalization/087_identifying_vs_non_identifying_relationship/)(Identifying Relationship)를 함께 써야 전역적으로 유일하게 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)할 수 있으며, 주문-주문항목 같은 실무 패턴에 자주 등장한다.
> 3. **판단 포인트**: 전체 참여와 삭제 정책을 이해해야 정규화와 물리 설계가 흔들리지 않는다. 부모 삭제 시 자식도 CASCADE 삭제되어야 하는 것이 일반적이다.

---

## Ⅰ. 개요 및 필요성

약한 개체는 부모가 있어야 이름이 완성된다. 예를 들어 주문(Order) 없이는 주문항목(Line Item)이 어떤 항목인지 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)할 수 없다. 주문항목 번호 "3번"은 주문 "O-1001의 3번"이 되어야 비로소 의미가 있다.

약한 개체가 필요한 이유는 다음과 같다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">강한 개체(Strong Entity) vs 약한 개체(Weak Entity)</div></div>
<div class="kb-diagram-note">강한 개체: 자체 PK로 독립 식별 가능</div>
<div class="kb-diagram-note">Student(student_id, name, grade)</div>
<div class="kb-diagram-note">→ student_id만으로 전세계에서 유일 식별</div>
<div class="kb-diagram-note">약한 개체: 부모 PK에 의존해서만 유일 식별 가능</div>
<div class="kb-diagram-note">OrderItem(order_id, item_no, product_id, qty)</div>
<div class="kb-diagram-note">→ item_no=3은 여러 주문에 존재 가능</div>
<div class="kb-diagram-note">→ order_id + item_no 조합으로만 유일 식별</div>
<div class="kb-diagram-note">현실 세계에서 약한 개체 예시:</div>
<div class="kb-diagram-note">주문 → 주문항목 (Order → OrderItem)</div>
<div class="kb-diagram-note">계좌 → 거래내역 (Account → Transaction)</div>
<div class="kb-diagram-note">직원 → 부양가족 (Employee → Dependent)</div>
<div class="kb-diagram-note">건물 → 층/호 (Building → Room)</div>
<div class="kb-diagram-note">청구서 → 청구항목 (Invoice → InvoiceItem)</div>
</div>
</div>



그래서 약한 개체는 부모 키와 부분 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)를 함께 써서 구분한다.

- **📢 섹션 요약 비유**: 부모 이름이 있어야 자식 이름이 완성된다. "김씨 집안의 첫째"처럼, 부모 맥락 없이는 누구인지 알 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 약한 개체의 구성 요소

| 요소 | 의미 | ER 표기 | 설계 포인트 |
| :--- | :--- | :--- | :--- |
| Strong Entity | 독립 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 가능 | 단일 사각형 | 자체 PK 보유 |
| Weak Entity | 부모에 종속 | 이중 사각형 | 독립 PK 없음 |
| Partial Key | 부모 안에서만 유일 | 밑줄 점선 타원 | line_no, 순번, seq |
| Identifying Relationship | 약한 개체의 식별 관계 | 이중 마름모 | 부모 PK를 포함 |
| Total Participation | 반드시 부모와 연결 | 이중선 | 존재 의존성 (Existence Dependency) |

### ER 다이어그램 표기



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">강한 개체(Strong Entity)와 약한 개체(Weak Entity):</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">주문(Order)</div><div class="kb-diagram-cell">══◇══▶║ 주문항목(Item)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(단일 사각형)</div><div class="kb-diagram-cell">(이중 마름모) ║ (이중 사각형)</div></div>
<div class="kb-diagram-note">PK: order_id Partial Key: item_no (밑줄 점선)</div>
<div class="kb-diagram-note">전체 관계:</div>
<div class="kb-diagram-tree-item" style="--depth:0">Order (Strong): order_id (PK), order_date, cust_id</div>
<div class="kb-diagram-tree-item" style="--depth:0">OrderItem (Weak): order_id + item_no (복합 PK), product_id, quantity</div>
<div class="kb-diagram-note">식별 공식:</div>
<div class="kb-diagram-note">OrderItem의 전역 유일성 = 부모 PK(order_id) + 부분 식별자(item_no)</div>
</div>
</div>



### 물리 스키마 변환 규칙 (매핑 규칙 2번)

약한 개체를 릴레이션으로 변환할 때는 <strong>소유자 FK + 부분 키 = 복합 PK</strong>를 구성한다.

```sql
-- 강한 개체 (Strong Entity) → 일반 테이블
CREATE TABLE Orders (
    order_id    INT          PRIMARY KEY,
    order_date  DATE         NOT NULL,
    cust_id     INT          NOT NULL,
    FOREIGN KEY (cust_id) REFERENCES Customer(cust_id)
);

-- 약한 개체 (Weak Entity) → 복합 PK (소유자FK + 부분키)
CREATE TABLE OrderItem (
    order_id    INT          NOT NULL,  -- 부모 PK (소유자 FK)
    item_no     INT          NOT NULL,  -- 부분 식별자 (Partial Key)
    product_id  VARCHAR(10),
    quantity    INT          NOT NULL DEFAULT 1,
    unit_price  DECIMAL(10,2),
    -- 복합 PK: 두 컬럼 조합으로 전역 유일성 보장
    PRIMARY KEY (order_id, item_no),
    -- 식별 관계: 부모 삭제 시 자식도 CASCADE
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
        ON DELETE CASCADE   -- 부모 삭제 시 자식도 삭제
        ON UPDATE CASCADE   -- 부모 PK 변경 시 자식 FK도 변경
);

-- 부양가족 예시 (직원-부양가족)
CREATE TABLE Dependent (
    emp_id      INT         NOT NULL,  -- 부모 FK
    dep_name    VARCHAR(50) NOT NULL,  -- 부분 식별자 (부모 안에서 유일)
    relationship VARCHAR(20),
    birth_date  DATE,
    PRIMARY KEY (emp_id, dep_name),    -- 복합 PK
    FOREIGN KEY (emp_id) REFERENCES Employee(emp_id)
        ON DELETE CASCADE
);
```

- **📢 섹션 요약 비유**: 부분 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)와 부모 키를 같이 봐야 완전한 식별이 된다. 호수(room_no)만으로는 어느 건물인지 모른다. 건물+호수 조합이어야 한다.

---

## Ⅲ. 비교 및 연결

약한 개체는 강한 개체, 연관 개체(Associative Entity)와 구분해서 이해해야 한다.

### Strong Entity vs Weak Entity vs Associative Entity

| 비교 항목 | Strong Entity | Weak Entity | Associative Entity |
| :--- | :--- | :--- | :--- |
| 독립 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | 가능 | 불가 | 가능 |
| PK 구성 | 자체 PK | 부모 PK + partial key | 관련 개체들의 PK 조합 |
| 존재 의존성 | 낮음 | 높음 (부모 필수) | 낮음~중간 |
| ER 표기 | 단일 사각형 | 이중 사각형 | 단일 사각형 (교차 테이블) |
| 예시 | Customer, Product | OrderItem, Dependent | Enrollment (수강) |

### 식별 관계 vs 비식별 관계

참여 제약조건과 함께 식별 관계 여부도 중요하다.

| 구분 | 식별 관계 (Identifying) | 비식별 관계 (Non-identifying) |
| :--- | :--- | :--- |
| 부모 PK | 자식 PK의 일부 | 자식 FK (NOT PK) |
| 자식 존재 | 부모 없이 불가 | 부모 없어도 존재 가능 |
| 예시 | 주문→주문항목 | 직원→부서 |
| ER 표기 | 이중 마름모 (이중선) | 단일 마름모 |
| SQL 구현 | 복합 PK | 별도 FK 컬럼 |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">식별 관계 예시</div><div class="kb-diagram-note">주문-주문항목</div></div>
<div class="kb-diagram-note">Order(order_id PK) OrderItem(order_id FK+PK, item_no PK)</div>
<div class="kb-diagram-note">이중선</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">비식별 관계 예시</div><div class="kb-diagram-note">직원-부서</div></div>
<div class="kb-diagram-note">Department(dept_id PK) Employee(dept_id FK, emp_id PK)</div>
<div class="kb-diagram-note">단일선</div>
</div>
</div>



약한 개체는 "부모 키에 매달린 존재"라는 점이 핵심이다.

- **📢 섹션 요약 비유**: 강한 개체는 혼자서도 선 수 있는 사람이고, 약한 개체는 부모 손을 잡아야만 길을 걸을 수 있는 어린아이와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 약한 개체 패턴을 올바르게 설계해야 데이터 정합성이 유지된다.

### 설계 체크리스트

- [ ] 부모 개체가 명확히 정의되어 있는가?
- [ ] 부분 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)가 부모 범위 내에서만 유일한지 검토한다.
- [ ] [식별 관계](/knowledge-base/studynote/05_database/02_modeling_normalization/087_identifying_vs_non_identifying_relationship/)와 전체 참여를 ER 다이어그램에 표시한다.
- [ ] 부모 삭제 시 자식 처리 규칙을 정한다 (일반적으로 CASCADE).
- [ ] [외래 키](/knowledge-base/studynote/05_database/02_modeling_normalization/072_foreign_key_fk/)(FK, Foreign Key)와 복합 키 구성을 점검한다.
- [ ] 부분 식별자의 생성 방식(순번 자동증가, 날짜 기반 등)을 결정한다.

### 부분 식별자 생성 전략

```sql
-- 전략 1: 순번 방식 (간단, 직관적)
-- ORDER_ID=1001의 item_no: 1, 2, 3, ...
-- 삽입 시 MAX(item_no) + 1로 계산 (동시성 문제 주의)

-- 전략 2: 자동증가 대리 키 추가 (분산 환경 선호)
CREATE TABLE OrderItem (
    item_id    BIGINT        PRIMARY KEY AUTO_INCREMENT,  -- 전역 유일 대리 키
    order_id   INT           NOT NULL,
    item_no    INT           NOT NULL,  -- 표시용 순번
    UNIQUE KEY uq_order_item (order_id, item_no),  -- 비즈니스 유일성 보장
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE
);
```

### 안티패턴

- ❌ 약한 개체를 강한 개체처럼 독립 PK(UUID, AUTO_INCREMENT)만으로 취급하는 것 — 부모와의 관계가 느슨해지고 고아 레코드 위험이 증가한다.
- ❌ 부모가 없어도 존재 가능한 것처럼 모델링하는 것 — 부분 참여로 설계하면 "어느 주문의 항목인지 모르는" 데이터가 생긴다.
- ❌ ON DELETE CASCADE 없이 약한 개체를 설계하는 것 — 부모 삭제 후 자식만 남는 고아 레코드가 쌓인다.

- **📢 섹션 요약 비유**: 삭제와 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 규칙을 같이 설계해야 한다. 부모집이 사라지면 그 집 주소(부분 식별자)도 함께 없어져야 한다.

---

## Ⅴ. 기대효과 및 결론

약한 개체는 혼자서는 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)이 완성되지 않는다. 부모와 함께 있을 때만 존재와 이름이 완성되는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조다.

### 도입 효과

| 항목 | 효과 |
| :--- | :--- |
| 데이터 정합성 | 부모-자식 관계가 DB 레벨에서 강제됨 |
| 저장 효율 | 중복 데이터 없이 관계로만 의미를 표현 |
| 삭제 관리 | CASCADE로 부모 삭제 시 자식 자동 정리 |
| 모델 명확성 | 실세계 종속 관계를 정확히 표현 |
| 쿼리 일관성 | 복합 PK로 조인 시 명확한 식별 가능 |

### 약한 개체 패턴의 실무 적용 범위



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">주요 실무 패턴:</div>
<div class="kb-diagram-note">1. 주문 시스템: Order → OrderItem (라인 번호)</div>
<div class="kb-diagram-note">2. 청구 시스템: Invoice → InvoiceItem</div>
<div class="kb-diagram-note">3. 인사 시스템: Employee → Dependent (부양가족)</div>
<div class="kb-diagram-note">4. 부동산 시스템: Building → Room (호수)</div>
<div class="kb-diagram-note">5. 문서 시스템: Document → Paragraph (단락 번호)</div>
<div class="kb-diagram-note">6. 금융 시스템: Account → Transaction (거래 순번)</div>
</div>
</div>



기술사 답변에서는 약한 개체를 "독립 PK 없이 소유자 개체의 키를 포함하여 복합 PK를 구성하는 종속 개체"로 정의하고, ER 표기(이중 사각형, 이중 마름모), 물리 구현(복합 PK, CASCADE), 활용 예시를 함께 서술하면 완성도가 높다.

- **📢 섹션 요약 비유**: 종속성을 이해하면 키 설계가 쉬워진다. 약한 개체는 부모의 그늘 아래서만 존재 의미를 갖는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 약한 개체 (Weak Entity) | 부모 없이는 식별이 완성되지 않는다. |
| [식별 관계](/knowledge-base/studynote/05_database/02_modeling_normalization/087_identifying_vs_non_identifying_relationship/) | 부모 키를 자식 PK의 일부로 전달한다. |
| 부분 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) | 부모 범위 안에서만 유일하다. |
| 전체 참여 | 자식이 부모에 반드시 연결된다. |
| PK (Primary Key) | 복합 키로 완성되는 경우가 많다. |
| CASCADE | 부모 삭제 시 자식도 함께 삭제. |
| Strong Entity | 자체 PK로 독립 식별 가능한 개체. |
| Associative Entity | M:N 관계를 풀기 위한 교차 엔터티, 독립 식별 가능. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">실세계 개체 식별</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">강한 개체 선별 (독립 PK 존재)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">약한 개체 발견 (부모 없이 미식별)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">부분 식별자 정의 (부모 내 순번, 이름 등)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">식별 관계 연결 (이중 마름모)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">매핑 규칙 2번 적용</div>
<div class="kb-diagram-note">(Weak Entity → 소유자FK + 부분키 = 복합 PK)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">ON DELETE CASCADE 설정</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">복합 PK 인덱스 최적화</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 가족 성이 먼저 있어야 이름이 완성되는 아이와 비슷하다. "김씨 가족의 첫째"처럼 가족 이름(부모 키)과 순번(부분 식별자)이 합쳐져야 누구인지 알 수 있다.
2. 혼자서는 누구인지 못 알아보지만, 가족 이름이 붙으면 바로 알 수 있다.
3. 부모를 잃으면 아이의 이름도 같이 사라진다 (CASCADE 삭제).

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 86 / 600

← **이전**: [85. 참여 제약조건 (Participation Constraint) - 필수 참여(전체), 선택 참여(부분)](/knowledge-base/studynote/05_database/02_modeling_normalization/085_participation_constraint_total_partial/)
**다음**: [87. 식별 관계 (Identifying) vs 비식별 관계 (Non-identifying)](/knowledge-base/studynote/05_database/02_modeling_normalization/087_identifying_vs_non_identifying_relationship/) →

---
