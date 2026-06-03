---
title: 143. 중첩 서브쿼리 & WHERE EXISTS 심화
date: '2026-04-19'
tags:
- studynote-database
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 중첩 서브쿼리는 **서브쿼리 안에 또 다른 서브쿼리가 포함**된 다단계 구조이며, WHERE EXISTS와 결합하면 **존재 여부를 다단계로 필터링**할 수 있다.
> 2. **가치**: "주문이 있고, 그 주문에 반품이 있는 고객"처럼 **다단계 조건**을 직관적으로 표현할 수 있지만, 깊어질수록 [[333_readability_vs_efficiency|가독성]]과 [[282_performance_tactics|성능]]이 나빠진다.
> 3. **판단 포인트**: 2단계 이상 중첩 시 **CTE(WITH 절)로 분해**하여 [[333_readability_vs_efficiency|가독성]]을 높이고, [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 실행계획을 반드시 [[396_validation|확인]]한다.

---

## Ⅰ. 개요 및 필요성

```text
SELECT * FROM customer c WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.cust_id = c.id
    AND EXISTS (
      SELECT 1 FROM returns r WHERE r.order_id = o.id
    )
);
→ 주문이 있고, 그 주문에 반품이 있는 고객
→ CTE 분해 권장 (가독성)
```

- **📢 섹션 요약 비유**: 중첩 서브쿼리는 **러시안 마트료시카(인형 안의 인형)**이다. 열면 안에 또 있다.

---

## Ⅱ~Ⅴ. 결론

중첩 서브쿼리는 **다단계 필터의 직관적 표현**이지만, 2단계+ 시 CTE 분해로 [[333_readability_vs_efficiency|가독성]]을 확보한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **중첩** | 다단계 서브쿼리 |
| **[[435_exists_boolean_fast_search|EXISTS]]** | 존재 필터 |
| **CTE** | [[333_readability_vs_efficiency|가독성]] 분해 |
| **실행계획** | [[282_performance_tactics|성능]] [[396_validation|확인]] 필수 |
| **Semi-[[521_join|Join]]** | [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 변환 |

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 서브쿼리] → [중첩 서브쿼리 (복잡)]
    → [CTE 분해 (가독성)]
    → [LATERAL/APPLY (고급)]
    → [현재: 옵티마이저 자동 Flatten — 중첩 해소]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 중첩 서브쿼리는 **마트료시카 인형**이에요. 열면 **안에 또 있어요**.
2. 너무 깊으면 **복잡해지니까** CTE로 한 단계씩 나눠요.
3. 한 번에 두 가지 조건("주문 있고 반품 있는")을 **[[396_validation|확인]]**할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 143 / 600

← **이전**: [[142_scalar_subquery|142. 스칼라 서브쿼리 (Scalar Subquery) - SELECT 절 단일값 반환]]
**다음**: [[144_correlated_subquery_nested_loop|144. 상관 서브쿼리 (Correlated Subquery) - 외부 참조 Nested Loop]] →

---
