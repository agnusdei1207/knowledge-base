+++
weight = 135
title = "135. SQL Non-Equi JOIN & Self JOIN - 범위·자기 참조 결합"
date = "2026-04-19"
[extra]
categories = "studynote-database"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Non-Equi JOIN은 **등호(=) 대신 부등호(<, >, BETWEEN)로 조인 조건을 지정**하는 것이며, Self JOIN은 **같은 테이블을 자기 자신과 조인**하여 계층·순위·비교를 수행한다.
> 2. **가치**: "급여 등급 테이블과 직원 급여를 범위 매칭"(Non-Equi), "직원과 그 상사를 같은 테이블에서 결합"(Self)은 **Equi JOIN으로 불가능한 핵심 [[298_qkv_attention|쿼리]]**이다.
> 3. **판단 포인트**: Self JOIN은 **반드시 별칭(Alias)을 사용**해야 하며, Non-Equi는 **[[154_database_index_b_tree_search_optimization|인덱스]] 최적화가 어려워** 대량 [[001_dikw_pyramid|데이터]]에서 [[282_performance_tactics|성능]] 주의가 필요하다.

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

Non-Equi·Self JOIN은 **[[083_relationship_in_er_model|관계]]형 [[001_dikw_pyramid|데이터]] 분석의 필수 기법**이며, 계층 [[298_qkv_attention|쿼리]]·범위 매칭에 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Non-Equi** | 범위 조건 [[521_join|JOIN]] |
| **Self [[521_join|JOIN]]** | 자기 [[316_reference_pattern_nosql|참조]] (계층) |
| **Alias** | Self [[521_join|JOIN]] 필수 |
| **BETWEEN** | Non-Equi 대표 조건 |
| **계층 [[298_qkv_attention|쿼리]]** | Self [[521_join|JOIN]] 활용 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Equi JOIN (기본)] → [Non-Equi JOIN (범위)]
    → [Self JOIN (자기 참조)] → [Recursive CTE (계층 대체)]
    → [현재: Graph Query — 계층·관계 전용 쿼리]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Non-Equi는 **"키가 150~160이면 M사이즈"**처럼 범위로 매칭해요.
2. Self JOIN은 **같은 사진에서 부모와 자식**을 찾는 거예요.
3. 같은 테이블을 **두 번 사용**하되 **이름(별칭)을 다르게** 붙여요!