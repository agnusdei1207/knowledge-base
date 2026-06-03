---
title: 131. SQL 표준 (ANSI/ISO SQL) - 관계형 데이터베이스 질의 언어 표준
date: '2026-04-19'
tags:
- studynote-database
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SQL(Structured Query Language)은 **[[083_relationship_in_er_model|관계]]형 [[002_database_definition|데이터베이스]]를 정의([[020_ddl|DDL]])·조작([[083_dml|DML]])·제어([[022_dcl|DCL]])**하는 ANSI/ISO 국제 표준 언어이며, SQL-86부터 SQL:2023까지 지속 발전하고 있다.
> 2. **가치**: 표준 SQL 덕분에 [[188_pl_sql_t_sql_procedural|Oracle]]·MySQL·PostgreSQL 등 **서로 다른 DBMS에서도 기본 문법이 동일**하여 이식성이 보장된다. 단, 각 벤더의 확장(PL/SQL, T-SQL)은 호환되지 않는다.
> 3. **판단 포인트**: SQL:1999([[316_olap|OLAP]], CTE), SQL:2003([[139_window_function_analytics|Window Function]]), SQL:2016([[343_json|JSON]]), SQL:2023([[070_graph_datastructure|그래프]] 패턴 매칭)의 주요 [[288_version_ihl_tos_total_length|버전]]별 추가 기능을 파악해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
SQL 구분: DDL (CREATE/ALTER/DROP) + DML (SELECT/INSERT/UPDATE/DELETE)
         + DCL (GRANT/REVOKE) + TCL (COMMIT/ROLLBACK)
```

- **📢 섹션 요약 비유**: SQL은 [[002_database_definition|데이터베이스]]와 대화하는 **공용 언어**이다. 영어가 국제 비즈니스 언어인 것처럼.

---

## Ⅱ. 아키텍처 및 핵심 원리

| [[288_version_ihl_tos_total_length|버전]] | 핵심 추가 |
|:---|:---|
| **SQL:1999** | CTE, [[316_olap|OLAP]], [[014_recursion|재귀]] [[298_qkv_attention|쿼리]] |
| **SQL:2003** | **[[139_window_function_analytics|Window Function]]**, MERGE |
| **SQL:2011** | Temporal (이력) |
| **SQL:2016** | **[[343_json|JSON]]** |
| **SQL:2023** | [[070_graph_datastructure|그래프]] 패턴 매칭 |

---

## Ⅲ~Ⅴ. 결론

SQL 표준은 **50년간 진화하며 여전히 [[001_dikw_pyramid|데이터]] 조작의 핵심 언어**이며, [[035_nosql|NoSQL]]·NewSQL에서도 SQL 인터페이스를 제공하는 추세이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[020_ddl|DDL]]** | 구조 정의 (CREATE) |
| **[[083_dml|DML]]** | [[001_dikw_pyramid|데이터]] 조작 ([[520_select|SELECT]]) |
| **[[139_window_function_analytics|Window Function]]** | SQL:2003 핵심 |
| **CTE** | [[014_recursion|재귀]]·서브쿼리 대체 |
| **SQL:2023** | [[070_graph_datastructure|그래프]] 패턴 매칭 |

### 📈 관련 키워드 및 발전 흐름도

```text
[SQL-86 (최초 표준)] → [SQL-92 (서브쿼리·JOIN)]
    → [SQL:1999 (CTE·OLAP)] → [SQL:2003 (Window)]
    → [SQL:2016 (JSON)] → [SQL:2023 (그래프)]
    → [현재: Text-to-SQL — 자연어→SQL 자동 변환]
```

### 👶 어린이를 위한 3줄 비유 설명
1. SQL은 [[002_database_definition|데이터베이스]]에게 말하는 **공용 언어**예요. "이 [[001_dikw_pyramid|데이터]] 보여줘!" 하면 **보여줘요**.
2. 어떤 [[002_database_definition|데이터베이스]]([[188_pl_sql_t_sql_procedural|Oracle]]·MySQL)든 **같은 말(SQL)**을 이해해요.
3. 최신 SQL은 **[[343_json|JSON]]·[[070_graph_datastructure|그래프]]**도 다룰 수 있어서 **더 강력**해졌답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 131 / 600

← **이전**: [[130_erd_notation_ie_barker_idef1x|130. ERD 표기법 비교 (IE·Barker·IDEF1X)]]
**다음**: [[132_sql_join_types_overview|132. SQL JOIN 유형 총정리 - INNER·LEFT·RIGHT·FULL·CROSS·SELF]] →

---
