+++
title = "77. 사용자 정의 무결성 (User-defined Integrity) - 업무 규칙에 따른 제약 (CHECK 제약조건 등)"

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

# 사용자 정의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) (User-defined Integrity) - 업무 규칙에 따른 제약

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 사용자 정의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 기본 키, 외래 키, [도메인 무결성](/knowledge-base/studynote/05_database/02_modeling_normalization/076_domain_integrity/)만으로는 막지 못하는 업무 규칙을 [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) (Database Management System)에 강제하는 규칙이다.
> 2. **가치**: CHECK 제약조건은 단순 조건에 강하고, TRIGGER는 행·테이블을 넘는 복합 규칙과 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 처리에 강하다.
> 3. **판단 포인트**: 규칙이 단순하면 CHECK, 복잡하거나 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)·연쇄 처리가 필요하면 TRIGGER를 쓰되 부작용(재귀 호출, 성능 저하)을 최소화해야 한다.

---

## Ⅰ. 개요 및 필요성
사용자 정의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 "이 회사의 규칙"을 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스가 대신 지키게 하는 장치다. 예를 들어 휴가 종료일이 시작일보다 빨라서는 안 되고, 재고는 음수가 될 수 없으며, 한 주문이 승인 없이 다시 상태를 바꾸면 안 된다. 이런 규칙은 표준 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)만으로는 충분히 표현되지 않는다.

애플리케이션 코드만 믿으면 배치 프로그램, 관리자 스크립트, 외부 연동이 규칙을 우회할 수 있다. 그래서 중요한 업무 규칙은 DB 레벨에 내려서 강제하는 편이 더 안전하다.

### 사용자 정의 무결성이 필요한 업무 규칙 예시

| 규칙 유형 | 예시 | 단순 제약으로 처리 가능? |
| :--- | :--- | :--- |
| 날짜 범위 | 종료일 >= 시작일 | CHECK로 가능 |
| 값 범위 | 재고량 >= 0 | CHECK로 가능 |
| 상태 전이 | 주문은 "결제 완료" 후에만 "배송 중"으로 변경 가능 | TRIGGER 필요 |
| 총합 제한 | 한 부서의 월 경비 합계가 예산을 초과하면 안 됨 | TRIGGER 필요 |
| 이력 감사 | 급여 변경 시 변경 전후 값을 감사 테이블에 기록 | TRIGGER 필요 |
| 동시성 규칙 | 같은 시간대에 같은 회의실에 두 예약 불가 | TRIGGER 또는 UNIQUE 인덱스 |

📢 섹션 요약 비유: 출입문에 "모자 쓰지 마세요"라고만 쓰는 것이 아니라, 문지기가 실제로 막아야 규칙이 지켜진다.

---

## Ⅱ. 아키텍처 및 핵심 원리
[DML](/knowledge-base/studynote/12_it_management/02_itsm_itil/083_dml/) (Data Manipulation Language) 문이 들어오면 DB는 제약조건을 먼저 검사하고, 필요하면 TRIGGER를 실행한 뒤 성공하면 COMMIT, 실패하면 ROLLBACK한다. 핵심은 "들어오기 전에 막을지", "들어온 뒤에 처리할지"를 구분하는 것이다.

### 제약 수단 비교

| 방식 | 강점 | 한계 | 적합한 규칙 |
| :--- | :--- | :--- | :--- |
| CHECK | 단순하고 선언적, 읽기 쉬움 | 다른 테이블 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 어려움 | 나이 > 0, 상태값 IN ('A','B','C') |
| TRIGGER | 복합 규칙, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 처리 가능 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), 디버깅, [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) 위험 | 재고, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 연쇄 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| ASSERTION | 표준 개념, 글로벌 규칙 표현 | [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 지원이 매우 약함 | 전체 테이블 수준 규칙 |
| 애플리케이션 검증 | UI/UX 피드백, 유연성 높음 | DB를 직접 접근하는 경우 우회 가능 | 사용자 입력 1차 검증 |

### DML 처리 흐름



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">INSERT / UPDATE 요청</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">1단계: 컬럼 타입/도메인 검사 (Domain Integrity)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">2단계: NOT NULL 검사 (Entity Integrity 일부)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">3단계: UNIQUE / PK 검사 (Entity Integrity)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">4단계: CHECK 제약조건 검사 (User-defined Integrity)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">5단계: FK 제약조건 검사 (Referential Integrity)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">6단계: BEFORE TRIGGER 실행 (필요 시)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">7단계: 실제 행 변경</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">8단계: AFTER TRIGGER 실행 (감사 로그, 연쇄 처리)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">성공: COMMIT | 실패: ROLLBACK</div>
</div>
</div>



### CHECK 제약조건 SQL 예시

```sql
-- 단순 값 범위 CHECK
CREATE TABLE Employee (
    emp_id     INT          PRIMARY KEY,
    name       VARCHAR(50)  NOT NULL,
    age        INT          CHECK (age >= 18 AND age <= 70),
    salary     DECIMAL(10,2) CHECK (salary >= 0),
    emp_type   CHAR(1)      CHECK (emp_type IN ('F', 'P', 'C'))
    -- F: Full-time, P: Part-time, C: Contract
);

-- 날짜 범위 CHECK
CREATE TABLE Vacation (
    vac_id      INT       PRIMARY KEY,
    emp_id      INT       NOT NULL,
    start_date  DATE      NOT NULL,
    end_date    DATE      NOT NULL,
    CHECK (end_date >= start_date),  -- 종료일이 시작일보다 같거나 이후여야 함
    FOREIGN KEY (emp_id) REFERENCES Employee(emp_id)
);

-- 컬럼 간 조건 CHECK (MySQL 8.0+, PostgreSQL 지원)
CREATE TABLE Order_Status (
    order_id      INT    PRIMARY KEY,
    status        VARCHAR(20) CHECK (status IN ('pending','approved','shipped','done')),
    approved_at   DATETIME,
    shipped_at    DATETIME,
    CHECK (shipped_at IS NULL OR approved_at IS NOT NULL)
    -- 배송 일시가 있으면 승인 일시도 있어야 함
);
```

### TRIGGER SQL 예시

```sql
-- 급여 변경 감사 TRIGGER
CREATE TRIGGER trg_salary_audit
AFTER UPDATE ON Employee
FOR EACH ROW
BEGIN
    IF OLD.salary != NEW.salary THEN
        INSERT INTO Salary_Audit (
            emp_id, old_salary, new_salary,
            changed_at, changed_by
        ) VALUES (
            OLD.emp_id, OLD.salary, NEW.salary,
            NOW(), USER()
        );
    END IF;
END;

-- 재고 음수 방지 TRIGGER
CREATE TRIGGER trg_stock_check
BEFORE UPDATE ON Inventory
FOR EACH ROW
BEGIN
    IF NEW.quantity < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '재고는 음수가 될 수 없습니다.';
    END IF;
END;
```

CHECK는 선언형이라 읽기 쉽고, TRIGGER는 절차형이라 더 많은 일을 할 수 있다. 대신 TRIGGER는 사이드 이펙트가 생기기 쉬우므로 규칙을 단순화하고 오류 메시지를 명확히 해야 한다.

📢 섹션 요약 비유: 간단한 규칙은 표지판으로 충분하지만, 복잡한 규칙은 경비원이 직접 확인해야 한다.

---

## Ⅲ. 비교 및 연결
사용자 정의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 [개체 무결성](/knowledge-base/studynote/05_database/02_modeling_normalization/074_entity_integrity_primary_key/), [참조 무결성](/knowledge-base/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/), [도메인 무결성](/knowledge-base/studynote/05_database/02_modeling_normalization/076_domain_integrity/)과 같은 기본 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 보완한다. 기본 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)이 "누가 누구인가"를 지키는 규칙이라면, 사용자 정의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 "우리 조직에서는 어떻게 해야 하는가"를 지키는 규칙이다.

### 무결성 계층 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">데이터 무결성 (Data Integrity)</div>
<div class="kb-diagram-tree-item" style="--depth:2">개체 무결성 (Entity Integrity)</div>
<div class="kb-diagram-note">── PK: NOT NULL + UNIQUE</div>
<div class="kb-diagram-tree-item" style="--depth:2">참조 무결성 (Referential Integrity)</div>
<div class="kb-diagram-note">── FK → PK 유효성</div>
<div class="kb-diagram-tree-item" style="--depth:2">도메인 무결성 (Domain Integrity)</div>
<div class="kb-diagram-note">── 타입, 범위, NULL 허용 여부</div>
<div class="kb-diagram-tree-item" style="--depth:2">사용자 정의 무결성 (User-defined Integrity)</div>
<div class="kb-diagram-tree-item" style="--depth:6">CHECK 제약조건</div>
<div class="kb-diagram-tree-item" style="--depth:6">TRIGGER</div>
<div class="kb-diagram-tree-item" style="--depth:6">ASSERTION (표준)</div>
</div>
</div>



### DB 레벨 vs 애플리케이션 레벨 검증 비교

| 비교 축 | DB 레벨 (CHECK, TRIGGER) | 애플리케이션 레벨 |
| :--- | :--- | :--- |
| 강제력 | 모든 접근 경로에서 강제 | API를 통하지 않으면 우회 가능 |
| 성능 | 행 단위 처리 오버헤드 | 비즈니스 로직과 함께 처리 |
| 유지보수 | 스키마 변경 필요 | 코드 변경으로 유연하게 수정 |
| 오류 메시지 | DB 오류 코드 형태 | 사용자 친화적 메시지 가능 |
| 적합성 | 핵심 데이터 정합성 규칙 | UX 검증, 복잡한 비즈니스 로직 |

애플리케이션 레벨 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 사용자 경험이 좋지만, 우회될 수 있다. DB 레벨 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 강제력이 높지만, 규칙이 복잡하면 유지보수가 어려워진다. 따라서 둘은 경쟁 관계가 아니라 역할 분담 관계다.

📢 섹션 요약 비유: 학교 규칙이 교실 공지판에도 있고, 교문에도 붙어 있어야 더 안전하다.

---

## Ⅳ. 실무 적용 및 기술사 판단
실무에서는 먼저 규칙의 복잡도를 본다. 단일 행의 조건이면 CHECK가 우선이고, 여러 행의 합계나 다른 테이블 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)가 필요하면 TRIGGER를 검토한다.

### 설계 판단 체크리스트

1. **규칙이 행 단위인가, 테이블 단위인가?** — 행 단위는 CHECK, 테이블 단위(집계, 참조)는 TRIGGER.
2. **에러 메시지가 사용자에게 이해 가능한가?** — SIGNAL/SQLSTATE로 의미 있는 오류 메시지를 반환해야 한다.
3. <strong><a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/">재귀</a> 실행이나 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 저하 가능성은 없는가?</strong> — TRIGGER 안에서 TRIGGER를 유발하는 DML을 실행하면 무한 루프가 발생할 수 있다.
4. <strong>애플리케이션 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>과 중복되어 유지비를 키우지 않는가?</strong> — 동일 규칙을 앱과 DB 양쪽에 두면 변경 시 둘 다 수정해야 한다.
5. **TRIGGER가 트랜잭션 전체에 영향을 주지 않는가?** — TRIGGER 안에서 실패하면 원 DML 전체가 롤백된다.

### 채택/회피 기준

```text
채택 (Use):
    ✓ 업무 규칙이 자주 바뀌지 않는다
    ✓ DB가 최종 진실의 원천(Source of Truth)이어야 한다
    ✓ 외부 시스템, 배치, 관리자 접근이 많아 우회 위험이 있다
    ✓ 규칙 위반이 데이터 손상으로 직결된다

회피 (Avoid):
    ✗ TRIGGER 안에서 외부 API 호출이나 복잡한 비즈니스 로직을 넣을 때
    ✗ 자주 바뀌는 임시 규칙에 TRIGGER를 쓸 때
    ✗ TRIGGER가 또 다른 TRIGGER를 연쇄 실행할 때
    ✗ 마이크로서비스에서 DB를 공유하지 않을 때
```

규칙이 단순하면 선언형(CHECK), 복잡하면 절차형(TRIGGER)으로 가되, 최종 목표는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 일관성을 깨지 않게 하는 것이다.

📢 섹션 요약 비유: 집 문에는 간단한 자물쇠를 달고, 금고에는 경보장치를 다는 것과 같다. 보호 가치에 따라 수단의 복잡도를 조절한다.

---

## Ⅴ. 기대효과 및 결론
사용자 정의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성을 높이고, 장애 이후 복구를 쉽게 하며, 시스템 간 규칙 차이를 줄여준다. 결국 이 개념은 "DB가 단순 저장소가 아니라 규칙의 마지막 보루"라는 관점으로 기억하면 된다.

### 도입 효과

| 항목 | 효과 |
| :--- | :--- |
| 데이터 정합성 | 모든 접근 경로에서 업무 규칙 강제 |
| 보안 강화 | 직접 DB 접근 시에도 규칙 우회 불가 |
| 감사 추적 | TRIGGER를 통한 변경 이력 자동 기록 |
| 장애 복구 | 정합성이 보장된 상태에서 복구 시작 |
| 개발 효율 | 중복 검증 로직 제거, 백엔드 코드 간소화 |

### 미래 전망

클라우드 환경에서는 DB 레벨 TRIGGER 대신 변경 데이터 캡처(CDC, Change Data Capture)와 이벤트 스트리밍(Kafka)을 통해 감사·연쇄 처리를 구현하는 추세다. 그러나 핵심 데이터 정합성 규칙은 여전히 DB 레벨의 CHECK와 TRIGGER가 가장 강력한 보장 수단으로 유지된다.

📢 섹션 요약 비유: 규칙을 문서로만 남기지 말고, 문 앞에서 실제로 지키게 만들어야 한다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [개체 무결성](/knowledge-base/studynote/05_database/02_modeling_normalization/074_entity_integrity_primary_key/) | 기본 키 중복 방지, 사용자 정의의 기반 |
| [참조 무결성](/knowledge-base/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/) | 외래 키 관계 보장, 고아 레코드 방지 |
| [도메인 무결성](/knowledge-base/studynote/05_database/02_modeling_normalization/076_domain_integrity/) | 컬럼 타입/범위 보장, 사용자 정의의 출발점 |
| CHECK 제약조건 | 단순 사용자 정의 규칙의 선언형 구현 |
| TRIGGER | 복합 규칙과 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 처리의 절차형 구현 |
| ASSERTION | SQL 표준의 전역 규칙 (DBMS 지원 미흡) |
| CDC (Change Data Capture) | 클라우드 환경에서 TRIGGER를 대체하는 변경 추적 기법 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">기본 무결성 (PK, FK, Domain)</div>
<div class="kb-diagram-note">↓ 업무 규칙 표현 필요성</div>
<div class="kb-diagram-note">CHECK 제약조건 (SQL 표준, 단순 규칙)</div>
<div class="kb-diagram-note">↓ 복합 규칙 처리 요구</div>
<div class="kb-diagram-note">TRIGGER (절차형, 다중 테이블 처리)</div>
<div class="kb-diagram-note">↓ 클라우드/마이크로서비스 대두</div>
<div class="kb-diagram-note">CDC + 이벤트 스트리밍 (Kafka, Debezium)</div>
<div class="kb-diagram-note">↓ 데이터 정합성 강화</div>
<div class="kb-diagram-note">현재: DB 레벨 + 애플리케이션 레벨 이중 검증 표준</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 상자에도 "이 규칙은 꼭 지켜요"라는 약속이 필요해요. 간단한 약속(재고는 음수 불가)은 스티커(CHECK)로 붙이면 돼요.
2. 복잡한 약속(급여 바꿀 때는 기록을 남겨야 해)은 지키는 사람이 직접 봐야(TRIGGER) 해요.
3. 그래야 나중에 장난감이 엉망이 되거나 기록이 사라지지 않아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 77 / 600

← **이전**: [76. 도메인 무결성 (Domain Integrity) - 속성 값은 정의된 도메인에 속해야 함](/knowledge-base/studynote/05_database/02_modeling_normalization/076_domain_integrity/)
**다음**: [78. 키 무결성 (Key Integrity)](/knowledge-base/studynote/05_database/02_modeling_normalization/078_key_integrity/) →

---
