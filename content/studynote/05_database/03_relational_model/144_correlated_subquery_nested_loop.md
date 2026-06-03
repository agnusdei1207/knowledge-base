+++
title = "144. 상관 서브쿼리 (Correlated Subquery) - 외부 참조 Nested Loop"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 상관 서브쿼리는 <strong>내부 서브쿼리가 외부 <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a>의 행을 <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a></strong>하여, 외부 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)의 <strong>각 행마다 서브쿼리가 반복 실행</strong>되는 구조이며, Nested Loop와 유사한 O(N×M) 특성을 가진다.
> 2. **가치**: "각 직원이 자기 부서 평균보다 높은가?"처럼 <strong>행 단위 비교</strong>를 직관적으로 표현할 수 있지만, 대량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>이 급격히 나빠진다</strong>.
> 3. **판단 포인트**: [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)가 자동으로 <strong>Semi-<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">Join</a>·Anti-Join으로 변환</strong>하는 경우가 많지만, 변환되지 않으면 JOIN이나 Window Function으로 수동 대체한다.

---

## Ⅰ. 개요 및 필요성

```text
상관 서브쿼리:
SELECT * FROM emp e1
WHERE sal > (SELECT AVG(sal) FROM emp e2 WHERE e2.dept_id = e1.dept_id);
  → e1의 각 행마다 e2 서브쿼리 실행
  → 100행 × 100행 = 10,000회 실행 가능
대안: Window Function → AVG(sal) OVER (PARTITION BY dept_id)
```

- **📢 섹션 요약 비유**: 상관 서브쿼리는 <strong>각 학생마다 반 평균을 따로 계산</strong>하는 것이다. 한 번에 계산하는 것(Window)보다 비효율적이다.

---

## Ⅱ~Ⅴ. 결론

상관 서브쿼리는 <strong>직관적이지만 O(N×M) 주의</strong>이며, [Window Function](/knowledge-base/studynote/05_database/03_relational_model/139_window_function_analytics/)·JOIN이 효율적 대안이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **상관** | 외부 행 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) |
| <strong><a href="/knowledge-base/studynote/05_database/07_exam_summary/431_nested_loop_join/">Nested Loop</a></strong> | 반복 실행 |
| <strong>Semi-<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">Join</a></strong> | [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) 변환 |
| <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/139_window_function_analytics/">Window Function</a></strong> | 효율적 대안 |
| **실행계획** | EXPLAIN [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 필수 |

### 📈 관련 키워드 및 발전 흐름도

```text
[상관 서브쿼리 (SQL-92)] → [성능 문제 인식]
    → [옵티마이저 Semi-Join 변환]
    → [Window Function 대안 (SQL:2003)]
    → [현재: LATERAL JOIN — 고급 대안]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 상관 서브쿼리는 <strong>각 학생마다 반 평균을 따로 계산</strong>하는 거예요.
2. 학생이 100명이면 <strong>100번 계산</strong>해야 해서 느려요.
3. Window Function은 <strong>한 번에 다 계산</strong>해서 훨씬 빨라요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 144 / 600

← **이전**: [143. 중첩 서브쿼리 & WHERE EXISTS 심화](/knowledge-base/studynote/05_database/03_relational_model/143_nested_subquery_where_exists/)
**다음**: [145. SQL Window Function 심화 - ROWS/RANGE Frame & 누적합](/knowledge-base/studynote/05_database/03_relational_model/145_sql_window_function_analytics/) →

---
