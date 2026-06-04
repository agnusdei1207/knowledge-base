+++
title = "135. SQL Non-Equi JOIN & Self JOIN - 범위·자기 참조 결합"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Non-Equi JOIN은 **등호(=) 대신 부등호(<, >, BETWEEN)로 조인 조건을 지정**하는 것이며, Self JOIN은 <strong>같은 테이블을 자기 자신과 조인</strong>하여 계층·순위·비교를 수행한다.
> 2. **가치**: "급여 등급 테이블과 직원 급여를 범위 매칭"(Non-Equi), "직원과 그 상사를 같은 테이블에서 결합"(Self)은 <strong>Equi JOIN으로 불가능한 핵심 <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a></strong>이다.
> 3. **판단 포인트**: Self JOIN은 <strong>반드시 별칭(Alias)을 사용</strong>해야 하며, Non-Equi는 <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a> 최적화가 어려워</strong> 대량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 주의가 필요하다.

---

## Ⅰ. 개요 및 필요성

```text
Non-Equi: SELECT e.name, g.grade
          FROM emp e JOIN grade g ON e.sal BETWEEN g.lo AND g.hi
Self:     SELECT e.name, m.name AS manager
          FROM emp e JOIN emp m ON e.mgr_id = m.id
```

- **📢 섹션 요약 비유**: Non-Equi는 "키 150~160cm인 사람은 M사이즈"(범위 매칭), Self는 "같은 가족사진에서 부모-자식 찾기"이다.

---

## Ⅱ~Ⅴ. 결론

Non-Equi·Self JOIN은 <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a>형 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 분석의 필수 기법</strong>이며, 계층 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)·범위 매칭에 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Non-Equi** | 범위 조건 [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) |
| <strong>Self <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a></strong> | 자기 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) (계층) |
| **Alias** | Self [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 필수 |
| **BETWEEN** | Non-Equi 대표 조건 |
| <strong>계층 <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a></strong> | Self [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 활용 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Equi JOIN (기본)] -> [Non-Equi JOIN (범위)]
    -> [Self JOIN (자기 참조)] -> [Recursive CTE (계층 대체)]
    -> [현재: Graph Query — 계층·관계 전용 쿼리]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Non-Equi는 <strong>"키가 150~160이면 M사이즈"</strong>처럼 범위로 매칭해요.
2. Self JOIN은 <strong>같은 사진에서 부모와 자식</strong>을 찾는 거예요.
3. 같은 테이블을 <strong>두 번 사용</strong>하되 **이름(별칭)을 다르게** 붙여요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 135 / 600

<- **이전**: [134. SQL OUTER JOIN (LEFT·RIGHT·FULL) - 비매칭 행도 포함하는 결합](/knowledge-base/studynote/05_database/03_relational_model/134_sql_outer_join_left_right_full/)
**다음**: [136. CROSS JOIN & Cartesian Product - 카테시안 곱 결합](/knowledge-base/studynote/05_database/03_relational_model/136_cross_join_cartesian_product/) ->

---
