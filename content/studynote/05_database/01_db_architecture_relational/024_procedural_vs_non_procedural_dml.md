---
title: 24. 절차적 DML vs 비절차적 DML — 네비게이션 vs 선언형
date: '2026-04-29'
tags:
- studynote-database
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[083_dml|DML]] ([[021_dml|Data Manipulation Language]], [[001_dikw_pyramid|데이터]] 조작어)은 절차적(Procedural) 방식과 비절차적(Non-Procedural) 방식으로 구분되며, 절차적 DML은 레코드를 어떻게(HOW) 탐색할지 지정하고 비절차적 DML은 무엇을(WHAT) 원하는지만 선언한다.
> 2. **가치**: 비절차적 DML인 SQL은 [[298_qkv_attention|쿼리]] 최적화(Query Optimization)를 [[502_dbms|DBMS]] 내부 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]([[088_optimizer|Optimizer]])에 위임하여 개발자가 접근 경로를 몰라도 최적 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]([[166_execution_plan_optimizer_navigation_tree|Execution Plan]])을 자동 [[087_process_state_transition|생성]]하므로, 생산성과 이식성이 절차적 [[083_dml|DML]] 대비 월등히 높다.
> 3. **판단 포인트**: SQL의 비절차적 특성이 항상 유리하지는 않다. 복잡한 커서(Cursor) 처리나 행별 비즈니스 로직이 필요한 경우 절차적 [[083_dml|DML]](PL/SQL, T-SQL)을 활용하여 세밀한 제어가 필요하며, [[163_optimizer_sql_execution_plan_generator|옵티마이저]] [[167_sql_hint_optimizer_override|힌트]]([[167_sql_hint_optimizer_override|Hint]])로 최적화를 유도하는 것이 실무 핵심 역량이다.

---

## Ⅰ. 개요 및 필요성

DML은 [[002_database_definition|데이터베이스]]의 [[001_dikw_pyramid|데이터]]를 조회·삽입·갱신·삭제하는 언어로, 구현 철학에 따라 두 가지로 [[104_classification_analysis|분류]]된다.

```text
┌──────────────────────────────────────────────────────────┐
│         절차적 DML vs 비절차적 DML 비교                    │
├──────────────────────────┬───────────────────────────────┤
│     절차적(Procedural)    │    비절차적(Non-Procedural)    │
├──────────────────────────┼───────────────────────────────┤
│  HOW: 레코드 탐색 경로    │  WHAT: 원하는 결과 선언        │
│  네트워크·계층형 DB 시대  │  관계형 DB, SQL               │
│  DL/1 (IBM IMS), COBOL   │  SQL (SELECT, UPDATE 등)      │
│  레코드 단위 처리         │  집합(Set) 단위 처리           │
│  옵티마이저 불필요        │  옵티마이저 필수               │
└──────────────────────────┴───────────────────────────────┘
```

- **📢 섹션 요약 비유**: 절차적 DML은 "1번 서랍 열고 → 3번 [[501_file_definition_logical_record|파일]] 꺼내고 → 5번 항목 찾아라"는 지시이고, 비절차적 DML은 "김철수 씨 정보 주세요"라는 요청이다. 두 번째는 내부 과정은 DB가 알아서 처리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### SQL 비절차적 실행 흐름

```text
SQL 문 입력
    │
    ▼
[파서 (Parser)] — 문법 검사, 파스 트리 생성
    │
    ▼
[옵티마이저 (Optimizer)] — 최적 실행 계획 선택
    │  ├─ 규칙 기반 (RBO, Rule-Based Optimizer)
    │  └─ 비용 기반 (CBO, Cost-Based Optimizer) ← 현대 표준
    ▼
[실행 엔진 (Execution Engine)] — 계획 실행
    │
    ▼
결과 집합(Result Set) 반환
```

### 커서(Cursor) — 절차적 처리의 SQL 내 활용

```sql
-- 절차적 처리가 필요한 경우: 행별 계산 후 갱신
DECLARE cur CURSOR FOR SELECT id, salary FROM emp WHERE dept = 'IT';
OPEN cur;
FETCH cur INTO @id, @salary;
WHILE @@FETCH_STATUS = 0
BEGIN
    UPDATE emp SET salary = @salary * 1.1 WHERE id = @id;
    FETCH cur INTO @id, @salary;
END
CLOSE cur;
```

비절차적 집합 처리로 대체 시: `UPDATE emp SET salary = salary * 1.1 WHERE dept = 'IT';` — 단 1줄, [[282_performance_tactics|성능]] 대폭 향상.

- **📢 섹션 요약 비유**: 커서를 쓰는 건 편지를 한 통씩 손으로 봉투에 넣는 것이고, 집합 처리 SQL은 봉투 넣는 기계로 한 번에 전부 처리하는 것이다. 후자가 훨씬 빠르지만 개별 처리가 필요할 때는 손봉투가 필요하다.

---

## Ⅲ. 비교 및 연결

| 항목 | 절차적 [[083_dml|DML]] | 비절차적 [[083_dml|DML]] (SQL) |
|:---|:---|:---|
| **처리 단위** | 레코드 단위 | 집합(Set) 단위 |
| **접근 경로** | 개발자가 명시 | [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 자동 결정 |
| **유연성** | 복잡한 로직 처리 용이 | 단순하고 이식성 높음 |
| **[[282_performance_tactics|성능]]** | 행별 오버헤드 | 집합 처리로 고성능 |
| **대표 기술** | PL/SQL, T-SQL, COBOL | SQL (ANSI 표준) |

- **📢 섹션 요약 비유**: 비절차적 SQL은 자동 내비게이션이고, 절차적 DML은 운전자가 직접 경로를 지정하는 것이다. 내비게이션이 대부분의 경우 더 빠른 길을 찾지만, 특수한 상황에서는 운전자의 경험이 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: [[316_olap|OLAP]] [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]] 최적화
10억 행 주문 테이블에서 월별 매출을 집계하는 [[298_qkv_attention|쿼리]]가 15초 소요.

1. `EXPLAIN PLAN` [[396_validation|확인]] → Full Table Scan 탐지.
2. [[163_optimizer_sql_execution_plan_generator|옵티마이저]] [[167_sql_hint_optimizer_override|힌트]]: `/*+ INDEX(orders idx_order_date) */` 추가.
3. [[179_table_partitioning_concept|파티셔닝]]: `PARTITION BY RANGE (order_date)` → 월별 [[184_partition_pruning|파티션 프루닝]].
4. 결과: 15초 → 0.3초 (50배 향상).

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 비절차적 SQL 대신 커서 루프로 대규모 [[001_dikw_pyramid|데이터]]를 행별 처리하는 [[128_water_scrum_fall_anti_pattern|안티패턴]]. 100만 행을 커서로 처리하면 SQL 집합 처리 대비 수십~수백 배 느리다. "SQL로 집합 처리하고, 부득이한 경우만 PL/SQL 커서 사용"이 원칙이다.

- **📢 섹션 요약 비유**: 수영장을 양동이로 채우는 것(커서 루프)과 호스로 채우는 것(집합 처리 SQL)의 차이다. 특별한 이유 없이 양동이를 고집하면 시간만 낭비된다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **생산성** | WHAT만 선언 → 개발 속도 향상 |
| **이식성** | ANSI SQL 표준 → DB 독립성 |
| **[[282_performance_tactics|성능]]** | [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 자동 최적화 |

현대 NewSQL과 [[136_variance|분산]] SQL(Distributed SQL)은 비절차적 SQL의 선언적 간결함을 유지하면서 수평 확장([[202_scale_out_distributed_horizontal_expansion|Scale-out]])을 지원하는 방향으로 발전하고 있다. [[163_optimizer_sql_execution_plan_generator|옵티마이저]]도 [[190_ai_llm_requirements_specification|AI]] 기반 학습형 [[163_optimizer_sql_execution_plan_generator|옵티마이저]](Learned [[088_optimizer|Optimizer]])로 진화하여 [[166_execution_plan_optimizer_navigation_tree|실행 계획]] 선택의 정확도를 높이고 있다.

- **📢 섹션 요약 비유**: SQL은 "결과만 말하면 돼"라는 마법이다. 컴퓨터가 어떻게 [[001_dikw_pyramid|데이터]]를 찾을지 스스로 고민하고, 개발자는 "무엇이 필요한지"만 이야기하면 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **SQL [[163_optimizer_sql_execution_plan_generator|옵티마이저]]** | 비절차적 DML의 [[166_execution_plan_optimizer_navigation_tree|실행 계획]] 자동 [[087_process_state_transition|생성]] 핵심 |
| **[[166_execution_plan_optimizer_navigation_tree|실행 계획]] ([[166_execution_plan_optimizer_navigation_tree|Execution Plan]])** | [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 선택 결과; EXPLAIN으로 [[396_validation|확인]] |
| **PL/SQL / T-SQL** | 절차적 확장 SQL; 커서·제어 구조 지원 |
| **커서 (Cursor)** | 집합 SQL을 행 단위로 처리하는 절차적 메커니즘 |
| **Learned [[088_optimizer|Optimizer]]** | [[190_ai_llm_requirements_specification|AI]] 기반 차세대 [[298_qkv_attention|쿼리]] 최적화 |

### 📈 관련 키워드 및 발전 흐름도

```text
[절차적 DML — 네트워크/계층형 DB, 레코드 단위 네비게이션]
    │
    ▼
[비절차적 DML (SQL) — 관계형 DB, 집합 처리, 옵티마이저]
    │
    ▼
[PL/SQL / T-SQL — 절차적 확장; 커서·트리거·저장 프로시저]
    │
    ▼
[CBO 옵티마이저 — 통계 기반 비용 최적 실행 계획]
    │
    ▼
[AI Learned Optimizer — 머신러닝 기반 실행 계획 예측]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 절차적 DML은 "첫 번째 서랍 열고, 세 번째 [[501_file_definition_logical_record|파일]] 찾고, 다섯 번째 줄 읽어라"처럼 단계를 하나하나 지시하는 방식이에요!
2. 비절차적 SQL은 "김철수 씨 성적 알려줘"처럼 결과만 말하면 컴퓨터가 알아서 찾아주는 방식이에요.
3. SQL 덕분에 개발자들은 [[001_dikw_pyramid|데이터]] 찾는 방법 대신 어떤 [[001_dikw_pyramid|데이터]]가 필요한지에만 집중할 수 있게 됐답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 24 / 600

← **이전**: [[023_tcl|23. TCL (Transaction Control Language)]]
**다음**: [[025_dba_database_administrator|25. DBA (Database Administrator) — 데이터베이스 관리자]] →

---
