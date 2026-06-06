---
title: "133. Sql Inner Join Intersection"
date: "2026-04-19"
tags:
  - "studynote-database"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: INNER JOIN은 <strong>두 테이블에서 조인 조건을 만족하는 행만 반환</strong>하는 교집합(∩) 연산이며, 가장 기본적이고 빈번한 [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) 유형이다.
> 2. **가치**: [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)로 분리된 테이블의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 <strong>의미 있는 하나의 결과로 결합</strong>하며, 매칭되지 않는 행은 자동 제외되므로 <strong>결과가 항상 완전한 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong>이다(NULL 없음).
> 3. **판단 포인트**: Equi-[Join](/studynote/05_database/04_transactions_concurrency/521_join/)(=), Non-Equi-[Join](/studynote/05_database/04_transactions_concurrency/521_join/)(<,>), [Natural Join](/studynote/05_database/07_exam_summary/413_natural_join/)(동일 컬럼명 자동 매칭)을 구분하고, <strong><a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a>가 <a href="/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a> <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>을 결정</strong>한다.

---

## Ⅰ. 개요 및 필요성

```text
SELECT e.name, d.dept_name
FROM emp e INNER JOIN dept d ON e.dept_id = d.id
-> 양쪽 모두 매칭되는 행만 반환 (교집합)
```

- **📢 섹션 요약 비유**: INNER JOIN은 **양쪽 명단에 모두 있는 사람만** 뽑는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 설명 |
|:---|:---|
| <strong><a href="/studynote/05_database/07_exam_summary/431_nested_loop_join/">Nested Loop</a></strong> | 소규모, [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 활용 |
| <strong><a href="/studynote/05_database/03_relational_model/174_hash_join/">Hash Join</a></strong> | 대규모, 동등 조건 |
| <strong>Merge <a href="/studynote/05_database/04_transactions_concurrency/521_join/">Join</a></strong> | 정렬된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |

---

## Ⅲ~Ⅴ. 결론

INNER JOIN은 <strong>SQL의 가장 기본 연산</strong>이며, [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)·[실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) 최적화가 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>INNER <a href="/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a></strong> | 교집합 (양쪽 매칭) |
| <strong>Equi-<a href="/studynote/05_database/04_transactions_concurrency/521_join/">Join</a></strong> | = 조건 |
| <strong><a href="/studynote/05_database/07_exam_summary/413_natural_join/">Natural Join</a></strong> | 동일 컬럼 자동 매칭 |
| <strong><a href="/studynote/05_database/03_relational_model/174_hash_join/">Hash Join</a></strong> | 대규모 최적화 |
| <strong><a href="/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/">실행 계획</a></strong> | EXPLAIN ANALYZE |

### 📈 관련 키워드 및 발전 흐름도

```text
[Cartesian Product] -> [Theta Join (조건)] -> [Equi-Join (=)]
    -> [INNER JOIN (SQL-92)] -> [Hash/Merge Join 최적화]
    -> [현재: Adaptive Join — 런타임 최적 알고리즘 선택]
```

### 👶 어린이를 위한 3줄 비유 설명
1. INNER JOIN은 **양쪽 명단에 모두 있는 사람만** 뽑아요.
2. A반 명단과 B반 명단에서 **겹치는 사람만** 결과에 나와요.
3. 안 겹치는 사람은 **자동으로 빠지니** 결과에 빈칸(NULL)이 없어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 133 / 600

<- **이전**: [132. SQL JOIN 유형 총정리 - INNER·LEFT·RIGHT·FULL·CROSS·SELF](/studynote/05_database/03_relational_model/132_sql_join_types_overview/)
**다음**: [134. SQL OUTER JOIN (LEFT·RIGHT·FULL) - 비매칭 행도 포함하는 결합](/studynote/05_database/03_relational_model/134_sql_outer_join_left_right_full/) ->

---
