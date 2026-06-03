+++
title = "141. 인라인 뷰 (Inline View) - FROM 절 서브쿼리"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인라인 뷰는 <strong>FROM 절에 서브쿼리를 작성하여 가상 테이블(파생 테이블)처럼 사용</strong>하는 SQL 기법이며, 복잡한 집계·필터 결과를 임시 테이블 없이 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 내에서 활용한다.
> 2. **가치**: "부서별 최고 급여 직원"처럼 <strong>집계 후 조인</strong>이 필요한 경우, 인라인 뷰로 집계 결과를 가상 테이블로 만들어 메인 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)와 조인하면 깔끔하게 해결된다.
> 3. **판단 포인트**: CTE(WITH 절)가 인라인 뷰의 <strong><a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/">가독성</a> 높은 대안</strong>이며, [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 대부분 동일하게 처리한다.

---

## Ⅰ. 개요 및 필요성

```text
SELECT e.name, e.sal, t.max_sal
FROM emp e
JOIN (SELECT dept_id, MAX(sal) AS max_sal FROM emp GROUP BY dept_id) t
  ON e.dept_id = t.dept_id AND e.sal = t.max_sal;
  → 인라인 뷰 t = 부서별 최고 급여 가상 테이블
```

- **📢 섹션 요약 비유**: 인라인 뷰는 <strong>임시 메모</strong>이다. 복잡한 계산 결과를 메모(가상 테이블)에 적어두고 본 작업에 활용한다.

---

## Ⅱ~Ⅴ. 결론

인라인 뷰는 <strong>복잡한 집계+조인의 핵심 기법</strong>이며, CTE가 [가독성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/) 높은 현대적 대안이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **인라인 뷰** | FROM 절 서브쿼리 |
| **파생 테이블** | 가상 테이블 |
| **CTE** | WITH 절 ([가독성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/) 대안) |
| <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/139_window_function_analytics/">Window Function</a></strong> | 인라인 뷰 대체 가능 |
| <strong>뷰 (<a href="/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/">View</a>)</strong> | 영구 저장 가상 테이블 |

### 📈 관련 키워드 및 발전 흐름도

```text
[기본 서브쿼리] → [인라인 뷰 (SQL-92)]
    → [CTE (SQL:1999)] → [Materialized CTE]
    → [현재: 옵티마이저 자동 인라인/CTE 변환]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 인라인 뷰는 <strong>임시 메모</strong>예요. 복잡한 계산 결과를 **메모에 적어둬요**.
2. 메모를 보면서 <strong>본 작업(메인 <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a>)</strong>을 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)하면 쉬워요.
3. CTE(WITH)는 **같은 메모를 더 깔끔하게** 적는 방법이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 141 / 600

← **이전**: [140. SQL 서브쿼리 심화 - EXISTS·IN·스칼라·인라인 뷰](/knowledge-base/studynote/05_database/03_relational_model/140_sql_subquery/)
**다음**: [142. 스칼라 서브쿼리 (Scalar Subquery) - SELECT 절 단일값 반환](/knowledge-base/studynote/05_database/03_relational_model/142_scalar_subquery/) →

---
