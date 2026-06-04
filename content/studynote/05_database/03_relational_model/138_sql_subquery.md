+++
title = "138. SQL 서브쿼리 (Subquery) - 쿼리 안의 쿼리"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 서브쿼리([Subquery](/knowledge-base/studynote/05_database/04_transactions_concurrency/523_subquery/))는 <strong>SQL 문 안에 중첩된 또 다른 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/">SELECT</a> 문</strong>이며, WHERE·FROM·[SELECT](/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/)·HAVING 절에서 사용할 수 있고, 스칼라·[인라인 뷰](/knowledge-base/studynote/05_database/03_relational_model/141_inline_view_subquery/)·상관(Correlated) 서브쿼리로 구분된다.
> 2. **가치**: JOIN으로 해결하기 어려운 **"평균보다 높은 급여의 직원"·"각 부서의 최고 급여"** 등의 복합 조건을 <strong>직관적으로 표현</strong>할 수 있다.
> 3. **판단 포인트**: [상관 서브쿼리](/knowledge-base/studynote/05_database/03_relational_model/144_correlated_subquery_nested_loop/)는 <strong>외부 <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> 행마다 실행</strong>되어 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 나쁘므로, 가능하면 <strong>JOIN이나 Window Function으로 대체</strong>한다.

---

## Ⅰ. 개요 및 필요성

```text
스칼라:  SELECT (SELECT MAX(sal) FROM emp) FROM dual
인라인:  SELECT * FROM (SELECT ... ) AS t
WHERE절: SELECT * FROM emp WHERE sal > (SELECT AVG(sal) FROM emp)
상관:    SELECT * FROM emp e WHERE sal > (SELECT AVG(sal) FROM emp WHERE dept_id = e.dept_id)
```

- **📢 섹션 요약 비유**: 서브쿼리는 <strong>질문 속의 질문</strong>이다. "평균이 얼마야?"를 먼저 답하고, 그 답으로 "평균보다 높은 사람은?"을 묻는다.

---

## Ⅱ~Ⅴ. 결론

서브쿼리는 <strong>복합 조건 표현의 핵심</strong>이지만, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 위해 [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/)·CTE·[Window Function](/knowledge-base/studynote/05_database/03_relational_model/139_window_function_analytics/) 대체를 항상 고려한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **스칼라** | [SELECT](/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/) 절 서브쿼리 |
| <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/141_inline_view_subquery/">인라인 뷰</a></strong> | FROM 절 서브쿼리 |
| **상관** | 외부 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) ([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)v) |
| **CTE** | 서브쿼리 대안 |
| <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/139_window_function_analytics/">Window Function</a></strong> | [상관 서브쿼리](/knowledge-base/studynote/05_database/03_relational_model/144_correlated_subquery_nested_loop/) 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
[기본 서브쿼리 (SQL-86)] -> [상관 서브쿼리 (SQL-92)]
    -> [CTE (SQL:1999)] -> [Window Function (SQL:2003)]
    -> [현재: 옵티마이저 자동 서브쿼리->JOIN 변환]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 서브쿼리는 <strong>질문 속의 질문</strong>이에요. "평균이 얼마야?" -> "평균보다 높은 사람은?"
2. 먼저 <strong>안쪽 질문에 답</strong>하고, 그 답으로 <strong>바깥 질문</strong>에 답해요.
3. 하지만 너무 많이 쓰면 **느려지니까** 다른 방법([JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/))도 알아야 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 138 / 600

<- **이전**: [137. SQL Self JOIN & Recursive CTE - 자기 참조와 재귀 쿼리](/knowledge-base/studynote/05_database/03_relational_model/137_sql_self_join_recursive/)
**다음**: [139. Window Function (분석 함수) - ROW_NUMBER·RANK·LAG·LEAD](/knowledge-base/studynote/05_database/03_relational_model/139_window_function_analytics/) ->

---
