---
title: "142. 스칼라 서브쿼리 (Scalar Subquery) - SELECT 절 단일값 반환"
date: "2026-04-19"
tags:
  - "studynote-database"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스칼라 서브쿼리는 <strong><a href="/studynote/05_database/04_transactions_concurrency/520_select/">SELECT</a> 절에서 단일 행·단일 열(스칼라 값)을 반환</strong>하는 서브쿼리이며, 각 행마다 서브쿼리가 실행되어 결과를 하나의 컬럼으로 표시한다.
> 2. **가치**: "각 직원의 부서 평균 급여"를 한 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)로 표현할 수 있어 <strong>직관적</strong>이지만, 행 수가 많으면 <strong>N번 실행되어 <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>이 나빠지므로</strong> JOIN이나 Window Function으로 대체한다.
> 3. **판단 포인트**: 반드시 <strong>1행 1열만 반환</strong>해야 하며(2행 이상 -> 에러), [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)가 자동으로 JOIN으로 변환하는 경우도 있다.

---

## Ⅰ. 개요 및 필요성

```text
SELECT name, sal,
  (SELECT AVG(sal) FROM emp e2 WHERE e2.dept_id = e1.dept_id) AS dept_avg
FROM emp e1;
  -> 각 직원 행마다 부서 평균을 서브쿼리로 계산
  -> Window Function 대안: AVG(sal) OVER (PARTITION BY dept_id)
```

- **📢 섹션 요약 비유**: 스칼라 서브쿼리는 **각 문제(행)마다 별도 계산기(서브쿼리)를 돌리는** 것이다. 한 번에 계산([JOIN](/studynote/05_database/04_transactions_concurrency/521_join/))하는 것보다 느릴 수 있다.

---

## Ⅱ~Ⅴ. 결론

스칼라 서브쿼리는 <strong>직관적이지만 <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 주의</strong>이며, Window Function이 효율적 대안이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **스칼라** | [SELECT](/studynote/05_database/04_transactions_concurrency/520_select/) 절 단일값 |
| **상관** | 외부 행 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) |
| <strong><a href="/studynote/05_database/03_relational_model/139_window_function_analytics/">Window Function</a></strong> | 효율적 대안 |
| **1행 1열** | 반환 제약 |
| <strong><a href="/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/">옵티마이저</a></strong> | 자동 [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) 변환 |

### 📈 관련 키워드 및 발전 흐름도

```text
[스칼라 서브쿼리 (SQL-92)] -> [상관 서브쿼리 문제 인식]
    -> [Window Function (SQL:2003, 대안)]
    -> [옵티마이저 자동 변환]
    -> [현재: LATERAL JOIN — 고급 대안]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 스칼라 서브쿼리는 <strong>각 문제마다 별도 계산기</strong>를 돌리는 거예요.
2. 문제가 **100개면 계산기를 100번** 돌려서 느려질 수 있어요.
3. Window Function은 <strong>한 번에 다 계산</strong>해서 빨라요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 142 / 600

<- **이전**: [141. 인라인 뷰 (Inline View) - FROM 절 서브쿼리](/studynote/05_database/03_relational_model/141_inline_view_subquery/)
**다음**: [143. 중첩 서브쿼리 & WHERE EXISTS 심화](/studynote/05_database/03_relational_model/143_nested_subquery_where_exists/) ->

---
