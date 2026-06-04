---
title: "52. 옵티마이저 (Optimizer) - 최적의 SQL 실행 계획 생성"
date: "2026-05-01"
tags:
  - "studynote-database"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) ([Optimizer](/studynote/12_it_management/02_itsm_itil/088_optimizer/))는 SQL 문을 실제로 어떻게 실행할지 결정하는 DBMS의 의사결정 엔진이다.
> 2. **가치**: 같은 결과를 내는 SQL이라도 [조인 순서](/studynote/05_database/03_relational_model/176_join_order_optimization/), [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 선택, 접근 경로에 따라 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이가 극단적으로 갈리므로, [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) ([Execution Plan](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)) 선택이 핵심이다.
> 3. **판단 포인트**: [규칙 기반 옵티마이저](/studynote/05_database/03_relational_model/164_rbo_rule_based_optimizer/) (RBO, Rule-Based [Optimizer](/studynote/12_it_management/02_itsm_itil/088_optimizer/))는 단순하지만 경직되고, [비용 기반 옵티마이저](/studynote/05_database/03_relational_model/165_cbo_cost_based_optimizer/) (CBO, Cost-Based [Optimizer](/studynote/12_it_management/02_itsm_itil/088_optimizer/))는 유연하지만 통계 정보가 낡으면 잘못된 계획을 고른다.

---

## Ⅰ. 개요 및 필요성

SQL은 "무엇을 가져올지"만 말하고 "어떻게 가져올지"는 말하지 않는다. 그래서 DBMS는 파서 (Parser) 뒤에서 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 해석하고, 최적의 접근 경로를 스스로 찾아야 한다. 이 판단을 맡는 것이 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)다.

[옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)가 중요한 이유는 동일한 결과를 내는 실행 방법이 매우 많기 때문이다. 풀 스캔, [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 스캔, [Nested Loop Join](/studynote/05_database/07_exam_summary/431_nested_loop_join/), [Hash Join](/studynote/05_database/03_relational_model/174_hash_join/), [Sort Merge Join](/studynote/05_database/03_relational_model/173_sort_merge_join/) 중 무엇을 택하느냐에 따라 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 수십 배 이상 달라질 수 있다.

- **📢 섹션 요약 비유**: [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 목적지만 말하면 알아서 최단 경로를 고르는 내비게이션과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)의 입력은 SQL의 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 구조이고, 출력은 [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)이다. 이 사이에서 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 통계 정보, [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 유무, [선택도](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) ([Selectivity](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)), 카디널리티 (Cardinality), 조인 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 평가한다.

```text
+--------------------------------------------------------------+
|               SQL -> 실행 계획 -> 실제 실행 흐름             |
+--------------------------------------------------------------+
| SQL 문                                                        |
|   |                                                           |
|   v                                                           |
| Parser / Rewrite                                              |
|   |                                                           |
|   v                                                           |
| Optimizer                                                     |
|   |   +- 통계 정보 확인                                       |
|   |   +- 접근 경로 비교                                       |
|   |   +- 조인 순서/알고리즘 선택                              |
|   v                                                           |
| Execution Plan -> Executor                                    |
+--------------------------------------------------------------+
```

| 판단 요소 | 의미 | 왜 중요한가 |
| :--- | :--- | :--- |
| [선택도](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) ([Selectivity](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)) | 조건이 얼마나 많은 행을 줄이는가 | [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 사용 여부를 좌우 |
| 카디널리티 (Cardinality) | 결과 행 수 추정 | [조인 순서](/studynote/05_database/03_relational_model/176_join_order_optimization/)와 비용 계산에 핵심 |
| 통계 정보 | 행 수, 분포, 히스토그램 | CBO 판단의 재료 |
| 접근 경로 | 풀 스캔, [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 스캔 등 | I/O 비용 차이를 만든다 |
| 조인 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | [Nested Loop](/studynote/05_database/07_exam_summary/431_nested_loop_join/), Hash, Merge | 대용량 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 핵심 |

[옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 추측이 아니라 계산을 한다. 물론 그 계산은 통계에 의존하므로, 통계가 낡으면 계산도 틀린다. 따라서 "빠른 SQL"의 절반은 좋은 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 아니라 좋은 통계 관리다.

- **📢 섹션 요약 비유**: [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 배달 앱이 아니다. 주소를 보고 가장 빠른 길을 찾지만, 도로 공사 정보가 오래되면 잘못된 길을 안내할 수 있다.

---

## Ⅲ. 비교 및 연결

RBO와 CBO는 최적화 철학이 다르다. RBO는 미리 정한 규칙에 따라 길을 고르고, CBO는 여러 경로의 비용을 비교해 더 싼 쪽을 고른다. 현대 DBMS는 거의 모두 CBO 계열이다.

| 항목 | RBO | CBO |
| :--- | :--- | :--- |
| 기준 | 규칙 우선순위 | 비용 계산 |
| 장점 | 단순하고 예측 가능 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포를 반영 |
| 약점 | 경직됨 | 통계 의존성 큼 |
| 현재 위치 | 대부분 구형 | 사실상 표준 |

[옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 설계, [힌트](/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/) ([Hint](/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)), [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/), 통계 갱신과 연결된다. [힌트](/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)는 사람이 계획에 개입하는 장치이지만, 남용하면 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)의 장점을 죽인다. 따라서 [힌트](/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)는 "최후의 수단"으로 쓰는 편이 좋다.

- **📢 섹션 요약 비유**: RBO는 교통 규칙만 외우는 초보 운전자이고, CBO는 실시간 교통량까지 보는 내비게이션이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)이 갑자기 바뀌는 이유는 대부분 통계 정보 변화, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 증가, [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 분포 변화, [조인 순서](/studynote/05_database/03_relational_model/176_join_order_optimization/) 변화 때문이다. 그래서 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 장애를 볼 때는 SQL만 보지 말고 통계, [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/), [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)을 함께 봐야 한다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 최신 통계가 반영되어 있는가?
2. [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) [선택도](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)가 충분히 좋은가?
3. [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)에서 예상 카디널리티와 실제 행 수가 크게 어긋나지 않는가?
4. [힌트](/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/) 없이도 안정적인 계획이 나오는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 통계를 오래 방치한 채 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝을 하는 경우
- [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)만 잔뜩 만들고 [선택도](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)를 보지 않는 경우
- 느린 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)에 무조건 [힌트](/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)를 박아서 다른 환경에서 망가지는 경우

기술사 관점에서는 "왜 느린가"보다 "왜 그 계획이 선택됐는가"를 설명할 수 있어야 한다. 즉 SQL [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 문제는 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)의 판단 근거를 해석하는 문제다.

- **📢 섹션 요약 비유**: [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) 튜닝은 요리사가 레시피보다 냄비 크기와 불 세기를 먼저 보는 일과 같다.

---

## Ⅴ. 기대효과 및 결론

[옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 DBMS가 선언형 SQL을 효율적으로 실행할 수 있게 만드는 핵심 엔진이다. 좋은 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 개발자가 "무엇"만 쓰면 "어떻게"는 시스템이 알아서 고르게 해 준다.

하지만 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)가 똑똑해질수록 통계 관리와 계획 해석 능력도 같이 중요해진다. 그래서 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝은 결국 [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)을 읽고, 통계를 갱신하고, 적절한 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)와 조인 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 고르는 일이다.

- **📢 섹션 요약 비유**: [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 도시에 깔린 교통 관제 시스템이다. 길을 잘 짜면 차가 빨리 흐르고, 정보가 틀리면 아무리 좋은 차도 막힌다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 파서 (Parser) | SQL을 구조화해 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)에 전달 |
| 통계 정보 | CBO의 핵심 입력 |
| [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) ([Execution Plan](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)) | [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)의 최종 산출물 |
| [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | 접근 경로 선택에 직접 영향 |
| 조인 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 대용량 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 결정하는 핵심 |

### 📈 관련 키워드 및 발전 흐름도

```text
SQL 문
    |
    v
Parser / Rewrite
    |
    v
RBO (Rule-Based Optimizer)
    |
    v
CBO (Cost-Based Optimizer)
    |
    v
실행 계획 (Execution Plan) · 실행 엔진
```

이 흐름은 정적인 규칙 기반 판단이 통계 기반 비용 계산으로 진화한 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)는 "공원 가는 길 알려줘"라고 하면 제일 빠른 길을 골라 주는 안내 로봇이에요.
2. 그런데 지도 정보가 오래되면 공사 중인 길로 안내할 수도 있어요.
3. 그래서 길 안내 로봇도 최신 지도가 있어야 똑똑하게 일할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 52 / 600

<- **이전**: [51. 로깅 엔진 (Logging 엔진)](/studynote/05_database/01_db_architecture_relational/051_logging_engine_wal_redo_undo/)
**다음**: [53. DB 파서와 파스 트리 (DB Parser Parse Tree)](/studynote/05_database/01_db_architecture_relational/053_db_parser_parse_tree/) ->

---
