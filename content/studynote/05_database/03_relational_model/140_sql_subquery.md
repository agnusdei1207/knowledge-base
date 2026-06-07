---
title: "140. Sql Subquery"
date: "2026-04-19"
tags:
  - "studynote-database"
weight: 140
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: EXISTS는 <strong>서브쿼리 결과가 존재하는지(T/F) 판별</strong>하는 반존재(Semi-[Join](/studynote/05_database/04_transactions_concurrency/521_join/)) 연산이고, IN은 <strong>값 목록에 포함되는지 판별</strong>하며, 대량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 EXISTS가 IN보다 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 좋은 경우가 많다.
> 2. **가치**: "주문이 있는 고객만"([EXISTS](/studynote/05_database/07_exam_summary/435_exists_boolean_fast_search/))과 "주문이 없는 고객"(NOT [EXISTS](/studynote/05_database/07_exam_summary/435_exists_boolean_fast_search/))은 실무에서 가장 빈번한 패턴이며, <strong><a href="/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/">옵티마이저</a>가 IN-><a href="/studynote/05_database/07_exam_summary/435_exists_boolean_fast_search/">EXISTS</a>, 서브쿼리->JOIN으로 자동 변환</strong>하기도 한다.
> 3. **판단 포인트**: 서브쿼리 결과가 NULL을 포함하면 NOT IN은 <strong>모든 행을 제외</strong>하는 함정이 있으므로, NOT EXISTS가 안전하다.

---

## Ⅰ. 개요 및 필요성

```text
EXISTS:  SELECT * FROM cust c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.cust_id = c.id)
IN:      SELECT * FROM cust WHERE id IN (SELECT cust_id FROM orders)
NOT IN 함정: NULL 포함 시 전체 제외 -> NOT EXISTS 권장
```

- **📢 섹션 요약 비유**: EXISTS는 "이 사람 명단에 **있어?(T/F)**", IN은 "이 값이 **목록에 있어?**"이다.

---

## Ⅱ~Ⅴ. 결론

[EXISTS](/studynote/05_database/07_exam_summary/435_exists_boolean_fast_search/)·NOT EXISTS는 <strong>Semi-<a href="/studynote/05_database/04_transactions_concurrency/521_join/">Join</a>/Anti-Join의 표준 표현</strong>이며, NOT IN의 NULL 함정을 반드시 인지해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/05_database/07_exam_summary/435_exists_boolean_fast_search/">EXISTS</a></strong> | 존재 여부 (T/F) |
| <strong>NOT <a href="/studynote/05_database/07_exam_summary/435_exists_boolean_fast_search/">EXISTS</a></strong> | Anti-[Join](/studynote/05_database/04_transactions_concurrency/521_join/) (안전) |
| **IN** | 값 목록 포함 |
| **NOT IN** | NULL 함정 주의 |
| <strong>Semi-<a href="/studynote/05_database/04_transactions_concurrency/521_join/">Join</a></strong> | [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) 변환 |

### 📈 관련 키워드 및 발전 흐름도

```text
[IN 서브쿼리 (기본)] -> [EXISTS (상관 서브쿼리)]
    -> [옵티마이저 자동 변환 (IN↔EXISTS)]
    -> [현재: Anti-Join 최적화 — NOT EXISTS 자동 변환]
```

### 👶 어린이를 위한 3줄 비유 설명
1. EXISTS는 **"이 명단에 이름이 있어? 있으면 OK!"** [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 거예요.
2. NOT IN은 <strong>빈칸(NULL)</strong>이 있으면 <strong>모두 탈락</strong>시키는 함정이 있어요.
3. 그래서 <strong>NOT <a href="/studynote/05_database/07_exam_summary/435_exists_boolean_fast_search/">EXISTS</a></strong>를 쓰는 게 더 안전하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 140 / 600

<- **이전**: [139. Window Function (분석 함수) - ROW_NUMBER·RANK·LAG·LEAD](/studynote/05_database/03_relational_model/139_window_function_analytics/)
**다음**: [141. 인라인 뷰 (Inline View) - FROM 절 서브쿼리](/studynote/05_database/03_relational_model/141_inline_view_subquery/) ->

---
