+++
title = "137. SQL Self JOIN & Recursive CTE - 자기 참조와 재귀 쿼리"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Self JOIN은 같은 테이블을 <strong>별칭(Alias)을 달리하여 자기 자신과 조인</strong>하는 것이고, Recursive CTE([Common Table Expression](/knowledge-base/studynote/05_database/07_exam_summary/513_cte_with_recursive_tree/))는 <strong>WITH RECURSIVE로 계층·트리 구조를 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/">재귀</a> 탐색</strong>하는 SQL:1999 표준 문법이다.
> 2. **가치**: 조직도(직원-상사)·부품 [BOM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)(Part-SubPart)·카테고리 계층 등 <strong>트리 구조 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 SQL로 탐색</strong>하는 데 필수이며, Oracle의 CONNECT BY보다 Recursive CTE가 표준이다.
> 3. **판단 포인트**: 무한 루프 방지를 위해 <strong>MAX <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/">RECURSION</a> DEPTH</strong> [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 필수이며, PostgreSQL·MySQL 8+·SQL Server 모두 지원한다.

---

## Ⅰ. 개요 및 필요성

```text
Recursive CTE:
  WITH RECURSIVE org AS (
    SELECT id, name, mgr_id FROM emp WHERE mgr_id IS NULL  -- Anchor
    UNION ALL
    SELECT e.id, e.name, e.mgr_id FROM emp e JOIN org o ON e.mgr_id = o.id  -- Recursive
  ) SELECT * FROM org;
```

- **📢 섹션 요약 비유**: Recursive CTE는 <strong>가계도 탐색</strong>이다. 시조(Anchor)부터 시작하여 자손을 [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)적으로 찾는다.

---

## Ⅱ~Ⅴ. 결론

Recursive CTE는 <strong>계층·<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/">그래프</a> <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 탐색의 SQL 표준</strong>이며, CONNECT BY([Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) 전용)를 대체한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Self <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a></strong> | 자기 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) |
| **Recursive CTE** | [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) 계층 탐색 |
| **Anchor** | [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) 시작점 |
| **CONNECT BY** | [Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) 전용 (비표준) |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/">BOM</a></strong> | 부품 계층 구조 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Self JOIN (기본)</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">CONNECT BY (Oracle, 1990s)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Recursive CTE (SQL:1999 표준)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Materialized Path / Nested Set (대안)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">현재: Graph Query (Neo4j) — 복잡 계층 전용</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. Self JOIN은 <strong>같은 가족사진에서 부모와 자식</strong>을 찾는 거예요.
2. Recursive CTE는 **가계도를 위에서 아래로** 쭉 따라가는 거예요.
3. 시조(할아버지)부터 시작해서 **자손을 계속 찾아** 내려가요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 137 / 600

← **이전**: [136. CROSS JOIN & Cartesian Product - 카테시안 곱 결합](/knowledge-base/studynote/05_database/03_relational_model/136_cross_join_cartesian_product/)
**다음**: [138. SQL 서브쿼리 (Subquery) - 쿼리 안의 쿼리](/knowledge-base/studynote/05_database/03_relational_model/138_sql_subquery/) →

---
