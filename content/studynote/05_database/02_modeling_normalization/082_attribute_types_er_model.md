+++
title = "82. 속성 (Attribute)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 속성 (Attribute)은 개체(Entity)가 가지는 성질이나 특성으로, ER 다이어그램에서 타원으로 표현되며 개체의 구체적 속성 값을 저장하는 기본 단위다.
> 2. **가치**: 개념 모델링 단계에서 속성을 정확히 분류(단순/복합/단일값/다치/유도)해야 이후 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)와 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) 변환이 흔들리지 않는다.
> 3. **판단 포인트**: 속성 분류를 잘못하면 중복 컬럼, 모호한 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/), 설계 오류가 생기므로 업무 용어를 정확히 분석해 속성 유형을 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

속성 (Attribute)은 ER (Entity-Relationship) 모델에서 개체가 가지는 특성을 표현하는 기본 단위다. 타원(Ellipse)으로 나타내며, 개체를 구체적으로 묘사하는 정보 항목이다. 예를 들어 "학생(Student)"이라는 개체는 학번, 이름, 생년월일, 전공 같은 속성을 가진다.

속성의 올바른 정의와 분류는 데이터 모델링의 품질을 결정한다. 개념 모델링 단계에서는 의미 구조를 먼저 고정해야 이후 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)와 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/) 변환이 흔들리지 않는다. 업무 용어를 잘못 자르면 중복 컬럼과 모호한 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)이 생긴다.

### 속성 정의가 잘못될 때의 문제



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">잘못된 예시</div><div class="kb-diagram-note">"주소"를 단일 속성으로 정의</div></div>
<div class="kb-diagram-note">address = "서울시 강남구 역삼동 123-45 2층"</div>
<div class="kb-diagram-note">→ 도시별 분석 불가</div>
<div class="kb-diagram-note">→ 우편번호 자동 검색 불가</div>
<div class="kb-diagram-note">→ 정렬/필터 어려움</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">올바른 예시</div><div class="kb-diagram-note">"주소"를 복합 속성으로 분해</div></div>
<div class="kb-diagram-note">city = "서울시"</div>
<div class="kb-diagram-note">district = "강남구"</div>
<div class="kb-diagram-note">street = "역삼동"</div>
<div class="kb-diagram-note">street_number = "123-45"</div>
<div class="kb-diagram-note">detail = "2층"</div>
<div class="kb-diagram-note">postal_code = "06123"</div>
<div class="kb-diagram-note">→ 도시별, 구별 집계 가능</div>
<div class="kb-diagram-note">→ 우편번호 기반 조회 가능</div>
</div>
</div>



업무 도메인 이해 없이 속성을 단순 나열하면 나중에 스키마 변경이 불가피해진다.

- **📢 섹션 요약 비유**: 속성은 설계도에 방 이름을 붙이는 일에 가깝다. 처음에 방 구분을 명확히 해야 나중에 벽을 부수지 않아도 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ER 모델에서 속성은 다양한 유형으로 분류된다. 이 분류를 이해해야 릴레이션 변환 규칙을 올바르게 적용할 수 있다.

### 속성 유형 분류 체계

| 속성 유형 | 정의 | ER 표기 | 릴레이션 변환 |
| :--- | :--- | :--- | :--- |
| 단순 속성 (Simple) | 더 이상 나눌 수 없는 원자값 | 단순 타원 | 컬럼 하나 |
| 복합 속성 (Composite) | 여러 단순 속성의 조합 | 타원 안에 타원 | 컬럼 여러 개로 분리 |
| 단일값 속성 (Single-valued) | 하나의 값만 가짐 | 단순 타원 | 일반 컬럼 |
| 다치 속성 (Multivalued) | 여러 값을 가질 수 있음 | 이중 타원 | 별도 테이블 분리 |
| 유도 속성 (Derived) | 다른 속성으로부터 계산 | 점선 타원 | 컬럼 생략 또는 계산 컬럼 |
| NULL 속성 (Null) | 값이 없거나 알 수 없음 | 일반 타원 + NULL 허용 | NULL 허용 컬럼 |
| 키 속성 (Key) | 개체를 유일 식별하는 속성 | 타원 + 밑줄 | PRIMARY KEY |

### 각 속성 유형의 릴레이션 변환 예시

```sql
-- 복합 속성 분해: 이름 = 성 + 이름
-- (복합 속성을 그대로 하나의 컬럼으로 두지 않음)
CREATE TABLE Employee (
    emp_id      INT          PRIMARY KEY,
    first_name  VARCHAR(50)  NOT NULL,   -- 복합 속성 분해
    last_name   VARCHAR(50)  NOT NULL,   -- 복합 속성 분해
    birth_date  DATE,
    age         INT AS (DATEDIFF(CURDATE(), birth_date) / 365)  -- 유도 속성 (계산)
);

-- 다치 속성 분리: 직원의 전화번호 (여러 개 가능)
CREATE TABLE Employee_Phone (
    emp_id      INT          NOT NULL,
    phone_type  VARCHAR(20)  NOT NULL,   -- 'mobile', 'home', 'work'
    phone_num   VARCHAR(20)  NOT NULL,
    PRIMARY KEY (emp_id, phone_num),
    FOREIGN KEY (emp_id) REFERENCES Employee(emp_id) ON DELETE CASCADE
);
-- 다치 속성은 별도 테이블로 분리 (7대 매핑 규칙 6번)

-- 유도 속성 처리: 나이는 생년월일에서 계산
-- 방법 1: 뷰(View)로 처리
CREATE VIEW Employee_View AS
SELECT emp_id, first_name, last_name,
       FLOOR(DATEDIFF(CURDATE(), birth_date) / 365) AS age
FROM Employee;

-- 방법 2: 계산 컬럼 (Generated Column, MySQL 5.7+)
ALTER TABLE Employee
ADD COLUMN age INT AS (FLOOR(DATEDIFF(CURDATE(), birth_date) / 365)) VIRTUAL;
```

### 속성과 개체·관계의 역할 구분

속성이 어디에 속하는지 명확히 해야 한다. 잘못된 배치는 데이터 이상(Anomaly) 현상을 일으킨다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">잘못된 배치 예시</div></div>
<div class="kb-diagram-note">수강(Enrollment) 관계 속성을 학생(Student)에 배치한 경우:</div>
<div class="kb-diagram-note">Student(student_id, name, course_id, grade)</div>
<div class="kb-diagram-note">→ 한 학생이 여러 과목을 듣는 경우 학생 행이 중복됨</div>
<div class="kb-diagram-note">→ 삽입 이상: 과목이 없으면 학생을 등록할 수 없음</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">올바른 배치</div></div>
<div class="kb-diagram-note">Student(student_id, name) ← 개체 속성</div>
<div class="kb-diagram-note">Course(course_id, title) ← 개체 속성</div>
<div class="kb-diagram-note">Enrollment(student_id, course_id, grade) ← 관계 속성</div>
</div>
</div>



- **📢 섹션 요약 비유**: 속성은 상자 안 물건을 칸막이로 나누는 일에 가깝다. 물건(속성)을 올바른 칸(개체 또는 관계)에 넣어야 나중에 찾기가 쉽다.

---

## Ⅲ. 비교 및 연결

속성은 종종 개체(Entity) 또는 관계(Relationship)와 같은 묶음으로 설명되지만, 세 개념의 관심사는 다르다. 개체가 "무엇이 존재하는가"를 정의한다면, 속성은 "그것이 어떤 특성을 가지는가"를 정의하고, 관계는 "개체들이 어떻게 연결되는가"를 정의한다.

### 개체 vs 속성 vs 관계 비교

| 비교 축 | 속성 (Attribute) | 개체 (Entity) | 관계 (Relationship) |
| :--- | :--- | :--- | :--- |
| 초점 | 개체의 특성, 성질 | 독립적으로 식별되는 실세계 대상 | 개체 간의 연결, 상호작용 |
| ER 표기 | 타원 | 사각형 | 마름모 |
| 독립성 | 없음 (개체에 종속) | 있음 | 없음 (개체에 종속) |
| 예시 | 이름, 나이, 주소 | 학생, 교수, 과목 | 수강, 강의, 소속 |

### "개체 아닌 속성" 판단 기준

다음 질문으로 속성과 개체를 구분한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">판단 질문:</div>
<div class="kb-diagram-note">1. 이것이 여러 개의 다른 속성을 가지는가?</div>
<div class="kb-diagram-note">→ YES → 개체(Entity)로 모델링</div>
<div class="kb-diagram-note">→ NO → 속성(Attribute)으로 모델링</div>
<div class="kb-diagram-note">2. 시스템에서 이것을 독립적으로 조회·수정하는가?</div>
<div class="kb-diagram-note">→ YES → 개체(Entity)로 모델링</div>
<div class="kb-diagram-note">→ NO → 속성(Attribute)으로 모델링</div>
<div class="kb-diagram-note">예시:</div>
<div class="kb-diagram-tree-item" style="--depth:0">"도시"가 단지 주소의 일부라면 → 속성</div>
<div class="kb-diagram-tree-item" style="--depth:0">"도시"가 인구, 시장, 면적 같은 자체 속성을 가지면 → 개체</div>
</div>
</div>



### 속성과 정규화의 연결

| 정규형 | 속성 관련 요구사항 |
| :--- | :--- |
| 1NF | 모든 속성 값이 원자값 (복합·다치 속성 분리) |
| 2NF | 모든 비키 속성이 PK 전체에 완전 함수 종속 |
| 3NF | 비키 속성 간 이행적 종속 제거 |
| BCNF | 유도 속성 등 모든 결정자가 후보 키 |

- **📢 섹션 요약 비유**: 속성은 비슷한 물건을 분류해 진열하는 일에 가깝다. 분류 기준이 명확해야 나중에 원하는 물건을 빨리 찾을 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 속성을 문법이나 이론 용어로만 이해하면 부족하다. 업무 용어가 수백 개로 늘어나는 프로젝트에서는 속성 분류가 응답시간, 저장 효율, 유지보수 복잡도에 직접 영향을 준다.

### 기술사 판단 체크리스트

1. **복합 속성을 원자값 수준으로 분해했는가?** — 주소, 이름, 기간 같은 복합 속성은 업무 요구에 따라 분해 수준을 결정한다.
2. **다치 속성을 별도 테이블로 분리했는가?** — 하나의 컬럼에 여러 값을 쉼표로 넣는 설계는 1NF 위반이다.
3. **유도 속성을 저장할지 계산할지 결정했는가?** — 실시간 계산이 가능하면 컬럼으로 저장하지 않는 것이 데이터 정합성에 유리하다.
4. **속성이 개체에 올바르게 배치되었는가?** — 관계의 속성을 개체에 둔 경우 함수 종속성 위반이 발생한다.
5. **NULL 허용 속성의 의미가 명확한가?** — NULL이 "알 수 없음"인지 "해당 없음"인지 명확히 정의해야 한다.

### 속성 설계 의사결정 흐름



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">속성 후보 발견</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">단순 속성인가? → YES → 컬럼으로 매핑</div>
<div class="kb-diagram-note">↓ NO</div>
<div class="kb-diagram-note">복합 속성인가? → YES → 원자 속성으로 분해 후 컬럼 매핑</div>
<div class="kb-diagram-note">↓ NO</div>
<div class="kb-diagram-note">다치 속성인가? → YES → 별도 테이블 분리 (FK 연결)</div>
<div class="kb-diagram-note">↓ NO</div>
<div class="kb-diagram-note">유도 속성인가? → YES → 계산 컬럼 또는 뷰로 처리</div>
<div class="kb-diagram-note">↓ NO</div>
<div class="kb-diagram-note">키 속성인가? → YES → PRIMARY KEY 지정</div>
<div class="kb-diagram-note">↓ NO</div>
<div class="kb-diagram-note">일반 속성 → NULL 허용 여부 결정 후 컬럼 매핑</div>
</div>
</div>



결론적으로 속성은 "무조건 채택"의 대상이 아니라, 의미·분해 필요성·저장 방식을 함께 따져 선택해야 하는 설계 포인트다.

- **📢 섹션 요약 비유**: 속성은 건축 전에 방 배치를 정하는 일에 가깝다. 나중에 벽을 부수지 않으려면 처음 설계가 중요하다.

---

## Ⅴ. 기대효과 및 결론

속성을 올바르게 분류하고 배치하면 다음 효과를 얻는다.

### 정량적 효과

| 항목 | 효과 |
| :--- | :--- |
| 저장 효율 | 다치 속성 분리로 중복 데이터 제거, 저장 공간 최적화 |
| 쿼리 성능 | 원자 속성으로 인덱스 활용도 향상 |
| 데이터 정합성 | 유도 속성 계산 처리로 갱신 이상 방지 |
| 유지보수성 | 명확한 속성 분류로 스키마 변경 영향 최소화 |

### 정성적 효과

- 업무 요구사항과 데이터 모델의 일치도가 높아진다.
- 정규화 적용 시 함수 종속성 분석이 명확해진다.
- 팀원 간 데이터 의미 공유가 쉬워진다.

특히 속성은 독립 개념처럼 보이지만 실제로는 개체와 관계 사이의 연결점으로 이해해야 오래 남는다. 시험에서는 정의·비교·판단 기준을 함께 말하고, 실무에서는 릴레이션 변환 규칙과 정규화까지 연결할 수 있어야 완성도 있는 답안이 된다.

- **📢 섹션 요약 비유**: 속성은 정리된 서랍장을 오래 유지하는 일에 가깝다. 처음에 잘 정리된 서랍은 나중에도 빠르게 물건을 찾을 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| ER 모델 (Entity-Relationship Model) | 속성이 배치되는 개념 설계의 틀 |
| 개체 (Entity) | 속성을 소유하는 주체 |
| 관계 (Relationship) | 개체 간 연결, 관계 속성을 가질 수 있음 |
| [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | 모델링된 속성이 [릴레이션](/knowledge-base/studynote/05_database/02_modeling_normalization/061_relation_schema_instance/)으로 변환될 때 중복을 줄이는 다음 단계 |
| [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) | 속성 값의 허용 범위를 정의해 의미를 고정 |
| 다치 속성 (Multivalued Attribute) | 1NF 위반 요인, 별도 테이블로 분리 필요 |
| 유도 속성 (Derived Attribute) | 계산으로 얻을 수 있어 저장 여부 결정 필요 |
| 복합 속성 (Composite Attribute) | 원자 속성으로 분해해 컬럼으로 매핑 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">요구사항 분석 → 업무 용어 식별</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">개체(Entity) 식별 (사각형)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">속성(Attribute) 분류 (타원)</div>
<div class="kb-diagram-tree-item" style="--depth:2">단순/복합 → 분해 여부 결정</div>
<div class="kb-diagram-tree-item" style="--depth:2">단일값/다치 → 테이블 분리 여부</div>
<div class="kb-diagram-tree-item" style="--depth:2">유도 속성 → 계산/저장 여부</div>
<div class="kb-diagram-tree-item" style="--depth:2">키 속성 → PK 지정</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">ER 다이어그램 완성</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">7대 매핑 규칙 적용 → 릴레이션 스키마</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">정규화 (1NF → 2NF → 3NF → BCNF)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">물리 설계 (인덱스, 파티셔닝)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 속성은 사람을 설명하는 특성이에요. 이름, 나이, 좋아하는 음식처럼요.
2. 전화번호가 여러 개라면 따로 기록해야(다치 속성 분리) 헷갈리지 않아요.
3. 나이는 생년월일만 있으면 계산할 수 있어서(유도 속성) 굳이 두 번 적지 않아도 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 82 / 600

← **이전**: [081. 개체 개념 (Entity Concept in E-R Model)](/knowledge-base/studynote/05_database/02_modeling_normalization/081_entity_concept_er_model/)
**다음**: [83. 관계 (Relationship) - 마름모, 개체 간 연관성](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) →

---
