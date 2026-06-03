+++
weight = 133
title = "133. SQL INNER JOIN - 교집합 결합의 기본"
date = "2026-04-19"
[extra]
categories = "studynote-database"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: INNER JOIN은 **두 테이블에서 조인 조건을 만족하는 행만 반환**하는 교집합(∩) 연산이며, 가장 기본적이고 빈번한 [[521_join|JOIN]] 유형이다.
> 2. **가치**: [[093_normalization|정규화]]로 분리된 테이블의 [[001_dikw_pyramid|데이터]]를 **의미 있는 하나의 결과로 결합**하며, 매칭되지 않는 행은 자동 제외되므로 **결과가 항상 완전한 [[001_dikw_pyramid|데이터]]**이다(NULL 없음).
> 3. **판단 포인트**: Equi-[[521_join|Join]](=), Non-Equi-[[521_join|Join]](<,>), [[413_natural_join|Natural Join]](동일 컬럼명 자동 매칭)을 구분하고, **[[154_database_index_b_tree_search_optimization|인덱스]]가 [[521_join|JOIN]] [[282_performance_tactics|성능]]을 결정**한다.

---

## Ⅰ. 개요 및 필요성

```text
SELECT e.name, d.dept_name
FROM emp e INNER JOIN dept d ON e.dept_id = d.id
→ 양쪽 모두 매칭되는 행만 반환 (교집합)
```

- **📢 섹션 요약 비유**: INNER JOIN은 **양쪽 명단에 모두 있는 사람만** 뽑는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| [[521_join|JOIN]] [[001_algorithm_definition|알고리즘]] | 설명 |
|:---|:---|
| **[[431_nested_loop_join|Nested Loop]]** | 소규모, [[154_database_index_b_tree_search_optimization|인덱스]] 활용 |
| **[[174_hash_join|Hash Join]]** | 대규모, 동등 조건 |
| **Merge [[521_join|Join]]** | 정렬된 [[001_dikw_pyramid|데이터]] |

---

## Ⅲ~Ⅴ. 결론

INNER JOIN은 **SQL의 가장 기본 연산**이며, [[154_database_index_b_tree_search_optimization|인덱스]]·[[166_execution_plan_optimizer_navigation_tree|실행 계획]] 최적화가 [[282_performance_tactics|성능]]의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **INNER [[521_join|JOIN]]** | 교집합 (양쪽 매칭) |
| **Equi-[[521_join|Join]]** | = 조건 |
| **[[413_natural_join|Natural Join]]** | 동일 컬럼 자동 매칭 |
| **[[174_hash_join|Hash Join]]** | 대규모 최적화 |
| **[[166_execution_plan_optimizer_navigation_tree|실행 계획]]** | EXPLAIN ANALYZE |

### 📈 관련 키워드 및 발전 흐름도

```text
[Cartesian Product] → [Theta Join (조건)] → [Equi-Join (=)]
    → [INNER JOIN (SQL-92)] → [Hash/Merge Join 최적화]
    → [현재: Adaptive Join — 런타임 최적 알고리즘 선택]
```

### 👶 어린이를 위한 3줄 비유 설명
1. INNER JOIN은 **양쪽 명단에 모두 있는 사람만** 뽑아요.
2. A반 명단과 B반 명단에서 **겹치는 사람만** 결과에 나와요.
3. 안 겹치는 사람은 **자동으로 빠지니** 결과에 빈칸(NULL)이 없어요!