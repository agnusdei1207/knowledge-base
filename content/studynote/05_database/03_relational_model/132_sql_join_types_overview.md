---
title: "132. SQL JOIN 유형 총정리 - INNER·LEFT·RIGHT·FULL·CROSS·SELF"
date: "2026-04-19"
tags:
  - "studynote-database"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SQL JOIN은 <strong>두 테이블의 공통 컬럼(키)을 기준으로 행을 결합</strong>하는 연산이며, INNER(교집합)·LEFT(좌측 전체+매칭)·RIGHT(우측 전체+매칭)·FULL(합집합)·CROSS(카테시안 곱)·SELF(자기 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/))로 구분된다.
> 2. **가치**: JOIN은 <strong><a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a>된 DB에서 분리된 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 하나로 합치는 유일한 수단</strong>이며, [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) 유형 선택이 결과 행 수와 NULL 처리를 결정한다.
> 3. **판단 포인트**: INNER는 양쪽 모두 매칭, LEFT는 왼쪽 전체 보존(매칭 없으면 NULL), FULL OUTER는 양쪽 모두 보존이며, <strong><a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a>·<a href="/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/">실행 계획</a> 최적화</strong>가 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
INNER JOIN:  A ∩ B (교집합)
LEFT JOIN:   A 전체 + B 매칭 (없으면 NULL)
RIGHT JOIN:  B 전체 + A 매칭 (없으면 NULL)
FULL JOIN:   A ∪ B (합집합, 없으면 NULL)
CROSS JOIN:  A × B (카테시안 곱)
SELF JOIN:   A ⋈ A (자기 참조)
```

- **📢 섹션 요약 비유**: INNER는 "둘 다 참석한 사람만", LEFT는 "A반 전체 + B반에서 겹치는 사람", FULL은 "양쪽 모두 포함".

---

## Ⅱ. 아키텍처 및 핵심 원리

| [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) | NULL 가능 | 행 수 |
|:---|:---|:---|
| **INNER** | 없음 | 매칭만 |
| **LEFT** | 우측 NULL | **좌측 ≤ 결과** |
| **FULL** | 양쪽 NULL | 최대 |
| **CROSS** | 없음 | A×B |

---

## Ⅲ~Ⅴ. 결론

JOIN은 <strong><a href="/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a>형 DB의 핵심 연산</strong>이며, 적절한 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)·[JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) 순서·[실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) 분석이 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 결정한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>INNER <a href="/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a></strong> | 교집합 |
| <strong>LEFT <a href="/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a></strong> | 좌측 전체 보존 |
| **FULL OUTER** | 합집합 |
| <strong>Hash/<a href="/studynote/05_database/07_exam_summary/431_nested_loop_join/">Nested Loop</a>/Merge</strong> | [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| <strong><a href="/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a></strong> | [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 핵심 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Cartesian Product (이론)] -> [INNER/OUTER JOIN (SQL-92)]
    -> [Lateral Join (SQL:2003)] -> [Hash Join 최적화 (2010s)]
    -> [현재: Adaptive Join — DB가 런타임에 최적 알고리즘 선택]
```

### 👶 어린이를 위한 3줄 비유 설명
1. INNER JOIN은 **양쪽 모두 참석한 사람만** 명단에 남겨요.
2. LEFT JOIN은 <strong>A반 전체 + B반에서 겹치는 사람</strong>을 포함해요.
3. 겹치지 않는 사람은 <strong>빈칸(NULL)</strong>으로 채워진답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 132 / 600

<- **이전**: [131. SQL 표준 (ANSI/ISO SQL) - 관계형 데이터베이스 질의 언어 표준](/studynote/05_database/03_relational_model/131_sql_ansi_iso_standard/)
**다음**: [133. SQL INNER JOIN - 교집합 결합의 기본](/studynote/05_database/03_relational_model/133_sql_inner_join_intersection/) ->

---
