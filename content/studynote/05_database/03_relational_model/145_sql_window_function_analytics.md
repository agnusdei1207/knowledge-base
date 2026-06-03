+++
title = "145. SQL Window Function 심화 - ROWS/RANGE Frame & 누적합"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Window Frame은 **ROWS(물리적 행 수)/RANGE([논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 값 범위)로 현재 행 기준 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 범위를 정의**하며, UNBOUNDED PRECEDING·[CURRENT](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/002_current/) ROW·N FOLLOWING 등으로 세밀하게 제어한다.
> 2. **가치**: SUM(sal) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND [CURRENT](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/002_current/) ROW)처럼 **이동 평균·누적합·연속 N일 집계**를 SQL만으로 구현할 수 있어 별도 프로그래밍이 불필요하다.
> 3. **판단 포인트**: ROWS(물리적 행 수, 동점 무관)와 RANGE([논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 값, 동점 포함)의 차이를 이해하고, 기본 Frame(RANGE UNBOUNDED PRECEDING)을 명시적으로 지정하는 것이 안전하다.

---

## Ⅰ. 개요 및 필요성

```text
누적합: SUM(sal) OVER (ORDER BY id ROWS UNBOUNDED PRECEDING)
이동평균(3일): AVG(val) OVER (ORDER BY dt ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
RANGE: AVG(sal) OVER (ORDER BY sal RANGE BETWEEN 1000 PRECEDING AND 1000 FOLLOWING)
```

- **📢 섹션 요약 비유**: Window Frame은 **망원경 줌**이다. 얼마나 넓게(UNBOUNDED) 또는 좁게(1 PRECEDING) 볼지 조절한다.

---

## Ⅱ~Ⅴ. 결론

Window Frame은 **이동 평균·누적합·연속 집계의 핵심**이며, ROWS/RANGE 차이를 명확히 이해해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **ROWS** | 물리적 행 수 |
| **RANGE** | [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 값 범위 |
| **UNBOUNDED** | 전체 범위 |
| **누적합** | Running Total |
| **이동 평균** | Moving Average |

### 📈 관련 키워드 및 발전 흐름도

```text
[기본 Window Function (SQL:2003)] → [ROWS/RANGE Frame]
    → [GROUPS Frame (SQL:2011)]
    → [현재: Window Function 최적화 — Segment Tree 기반]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Window Frame은 **망원경 줌**이에요. 넓게 or 좁게 볼 범위를 정해요.
2. "최근 3일 평균"은 **2 PRECEDING**으로 앞 2행+현재 행을 봐요.
3. "전체 누적합"은 **UNBOUNDED PRECEDING**으로 처음부터 다 더해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 145 / 600

← **이전**: [144. 상관 서브쿼리 (Correlated Subquery) - 외부 참조 Nested Loop](/knowledge-base/studynote/05_database/03_relational_model/144_correlated_subquery_nested_loop/)
**다음**: [146. PARTITION BY & ORDER BY - Window 함수 핵심 절](/knowledge-base/studynote/05_database/03_relational_model/146_window_function_partition_by_order_by/) →

---
