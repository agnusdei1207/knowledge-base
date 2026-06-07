---
title: "Nested Subquery Where Exists"
date: "2026-04-19"
tags:
  - "studynote-database"
weight: 143
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 중첩 서브쿼리는 <strong>서브쿼리 안에 또 다른 서브쿼리가 포함</strong>된 다단계 구조이며, WHERE EXISTS와 결합하면 <strong>존재 여부를 다단계로 필터링</strong>할 수 있다.
> 2. **가치**: "주문이 있고, 그 주문에 반품이 있는 고객"처럼 <strong>다단계 조건</strong>을 직관적으로 표현할 수 있지만, 깊어질수록 [가독성](/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/)과 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 나빠진다.
> 3. **판단 포인트**: 2단계 이상 중첩 시 <strong>CTE(WITH 절)로 분해</strong>하여 [가독성](/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/)을 높이고, [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) 실행계획을 반드시 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.

---

## Ⅰ. 개요 및 필요성

```text
SELECT * FROM customer c WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.cust_id = c.id
    AND EXISTS (
      SELECT 1 FROM returns r WHERE r.order_id = o.id
    )
);
-> 주문이 있고, 그 주문에 반품이 있는 고객
-> CTE 분해 권장 (가독성)
```

- **📢 섹션 요약 비유**: 중첩 서브쿼리는 <strong>러시안 마트료시카(인형 안의 인형)</strong>이다. 열면 안에 또 있다.

---

## Ⅱ~Ⅴ. 결론

중첩 서브쿼리는 <strong>다단계 필터의 직관적 표현</strong>이지만, 2단계+ 시 CTE 분해로 [가독성](/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/)을 확보한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **중첩** | 다단계 서브쿼리 |
| <strong><a href="/studynote/05_database/07_exam_summary/435_exists_boolean_fast_search/">EXISTS</a></strong> | 존재 필터 |
| **CTE** | [가독성](/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/) 분해 |
| **실행계획** | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 필수 |
| <strong>Semi-<a href="/studynote/05_database/04_transactions_concurrency/521_join/">Join</a></strong> | [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) 변환 |

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 서브쿼리] -> [중첩 서브쿼리 (복잡)]
    -> [CTE 분해 (가독성)]
    -> [LATERAL/APPLY (고급)]
    -> [현재: 옵티마이저 자동 Flatten — 중첩 해소]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 중첩 서브쿼리는 <strong>마트료시카 인형</strong>이에요. 열면 **안에 또 있어요**.
2. 너무 깊으면 **복잡해지니까** CTE로 한 단계씩 나눠요.
3. 한 번에 두 가지 조건("주문 있고 반품 있는")을 <strong><a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 143 / 600

<- **이전**: [142. 스칼라 서브쿼리 (Scalar Subquery) - SELECT 절 단일값 반환](/studynote/05_database/03_relational_model/142_scalar_subquery/)
**다음**: [144. 상관 서브쿼리 (Correlated Subquery) - 외부 참조 Nested Loop](/studynote/05_database/03_relational_model/144_correlated_subquery_nested_loop/) ->

---
