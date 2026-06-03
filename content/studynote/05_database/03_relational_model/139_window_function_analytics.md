+++
title = "139. Window Function (분석 함수) - ROW_NUMBER·RANK·LAG·LEAD"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Window Function은 <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/522_group_by/">GROUP BY</a> 없이 행 단위로 집계·순위·이전/다음 행 <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a></strong>를 수행하는 SQL:2003 표준 함수이며, OVER([PARTITION BY](/knowledge-base/studynote/05_database/07_exam_summary/436_window_function_over/) ... ORDER BY ...)로 윈도우를 정의한다.
> 2. **가치**: GROUP BY는 결과를 그룹별 1행으로 축소하지만, Window Function은 <strong>원본 행을 유지하면서 집계 결과를 함께 표시</strong>하여 [상관 서브쿼리](/knowledge-base/studynote/05_database/03_relational_model/144_correlated_subquery_nested_loop/)를 대체하고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 크게 향상시킨다.
> 3. **판단 포인트**: ROW_NUMBER(순번)·RANK(순위)·SUM OVER(누적합)·LAG/LEAD(이전/다음 행)가 핵심이며, [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)네이션·순위·이동 평균에 필수이다.

---

## Ⅰ. 개요 및 필요성

```text
SELECT name, dept, sal,
  ROW_NUMBER() OVER (PARTITION BY dept ORDER BY sal DESC) AS rn,
  RANK() OVER (ORDER BY sal DESC) AS rank,
  LAG(sal) OVER (ORDER BY sal) AS prev_sal
FROM emp;
```

- **📢 섹션 요약 비유**: Window Function은 <strong>반 전체 석차표</strong>이다. 각 학생(행)의 성적은 유지하면서 석차(순위)를 옆에 붙인다.

---

## Ⅱ~Ⅴ. 결론

Window Function은 <strong>현대 SQL 분석의 핵심</strong>이며, [상관 서브쿼리](/knowledge-base/studynote/05_database/03_relational_model/144_correlated_subquery_nested_loop/)·자체 조인을 대체하여 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 [가독성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/)을 동시에 향상시킨다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **ROW_NUMBER** | 순번 |
| **RANK** | 순위 (동점 건너뜀) |
| **DENSE_RANK** | 순위 (동점 안 건너뜀) |
| **LAG/LEAD** | 이전/다음 행 |
| **SUM OVER** | 누적합·이동 평균 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">GROUP BY (집계)</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">상관 서브쿼리 (비효율)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Window Function (SQL:2003)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">ROWS/RANGE Frame (세밀한 윈도우)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">현재: 대부분 DB 완전 지원 — 분석 쿼리 필수</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. Window Function은 <strong>석차표</strong>예요. 각 학생 점수는 **그대로 두고 순위만 붙여요**.
2. GROUP BY는 "반 평균만" 보여주지만, Window는 **각 학생 + 반 평균** 모두 보여줘요.
3. "이전 시험보다 올랐나?"도 <strong>LAG</strong>로 쉽게 알 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 139 / 600

← **이전**: [138. SQL 서브쿼리 (Subquery) - 쿼리 안의 쿼리](/knowledge-base/studynote/05_database/03_relational_model/138_sql_subquery/)
**다음**: [140. SQL 서브쿼리 심화 - EXISTS·IN·스칼라·인라인 뷰](/knowledge-base/studynote/05_database/03_relational_model/140_sql_subquery/) →

---
