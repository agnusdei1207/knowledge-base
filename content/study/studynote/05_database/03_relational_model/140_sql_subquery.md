+++
weight = 140
title = "140. SQL 서브쿼리 심화 - EXISTS·IN·스칼라·인라인 뷰"
date = "2026-04-19"
[extra]
categories = "studynote-database"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: EXISTS는 **서브쿼리 결과가 존재하는지(T/F) 판별**하는 반존재(Semi-[[521_join|Join]]) 연산이고, IN은 **값 목록에 포함되는지 판별**하며, 대량 [[001_dikw_pyramid|데이터]]에서 EXISTS가 IN보다 [[282_performance_tactics|성능]]이 좋은 경우가 많다.
> 2. **가치**: "주문이 있는 고객만"([[435_exists_boolean_fast_search|EXISTS]])과 "주문이 없는 고객"(NOT [[435_exists_boolean_fast_search|EXISTS]])은 실무에서 가장 빈번한 패턴이며, **[[163_optimizer_sql_execution_plan_generator|옵티마이저]]가 IN→[[435_exists_boolean_fast_search|EXISTS]], 서브쿼리→JOIN으로 자동 변환**하기도 한다.
> 3. **판단 포인트**: 서브쿼리 결과가 NULL을 포함하면 NOT IN은 **모든 행을 제외**하는 함정이 있으므로, NOT EXISTS가 안전하다.

---

## Ⅰ. 개요 및 필요성

```text
EXISTS:  SELECT * FROM cust c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.cust_id = c.id)
IN:      SELECT * FROM cust WHERE id IN (SELECT cust_id FROM orders)
NOT IN 함정: NULL 포함 시 전체 제외 → NOT EXISTS 권장
```

- **📢 섹션 요약 비유**: EXISTS는 "이 사람 명단에 **있어?(T/F)**", IN은 "이 값이 **목록에 있어?**"이다.

---

## Ⅱ~Ⅴ. 결론

[[435_exists_boolean_fast_search|EXISTS]]·NOT EXISTS는 **Semi-[[521_join|Join]]/Anti-Join의 표준 표현**이며, NOT IN의 NULL 함정을 반드시 인지해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[435_exists_boolean_fast_search|EXISTS]]** | 존재 여부 (T/F) |
| **NOT [[435_exists_boolean_fast_search|EXISTS]]** | Anti-[[521_join|Join]] (안전) |
| **IN** | 값 목록 포함 |
| **NOT IN** | NULL 함정 주의 |
| **Semi-[[521_join|Join]]** | [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 변환 |

### 📈 관련 키워드 및 발전 흐름도

```text
[IN 서브쿼리 (기본)] → [EXISTS (상관 서브쿼리)]
    → [옵티마이저 자동 변환 (IN↔EXISTS)]
    → [현재: Anti-Join 최적화 — NOT EXISTS 자동 변환]
```

### 👶 어린이를 위한 3줄 비유 설명
1. EXISTS는 **"이 명단에 이름이 있어? 있으면 OK!"** [[396_validation|확인]]하는 거예요.
2. NOT IN은 **빈칸(NULL)**이 있으면 **모두 탈락**시키는 함정이 있어요.
3. 그래서 **NOT [[435_exists_boolean_fast_search|EXISTS]]**를 쓰는 게 더 안전하답니다!
