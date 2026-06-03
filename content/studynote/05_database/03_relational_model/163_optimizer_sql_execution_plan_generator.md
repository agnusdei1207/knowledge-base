+++
title = "163. 옵티마이저 (Optimizer) - SQL 실행 최적 경로(Execution Plan) 생성기"
date = 2026-05-05

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트

> 1. **본질**: 옵티마이저 ([Optimizer](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_optimizer/))는 선언형 SQL을 실제 하드웨어가 실행할 수 있는 물리 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) ([Execution Plan](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/))으로 바꾸는 [데이터베이스 관리 시스템](/knowledge-base/studynote/05_database/01_db_architecture_relational/003_dbms_database_management_system/) ([DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/), [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) System)의 의사결정 엔진이다.
> 2. **가치**: 같은 SQL이라도 [조인 순서](/knowledge-base/studynote/05_database/03_relational_model/176_join_order_optimization/), [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 사용 여부, 조인 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 선택에 따라 디스크 입출력 (I/O, Input/Output) 비용이 수십 배 이상 달라지므로, 옵티마이저 품질이 곧 응답시간과 서버 자원 효율을 좌우한다.
> 3. **판단 포인트**: 옵티마이저는 보통 사람보다 빠르게 최적 경로를 찾지만, 통계 정보가 낡거나 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포가 치우치면 오판할 수 있으므로 통계 관리·[실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) 점검·[힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/) 사용 우선순위를 함께 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

옵티마이저 ([Optimizer](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_optimizer/))는 SQL이 요구하는 결과는 그대로 유지한 채, 그 결과를 <strong>가장 낮은 예상 비용으로 얻는 실행 순서</strong>를 선택하는 구성 요소다. SQL은 "무엇을 구할지"만 선언하고 "어떻게 읽을지"는 명령하지 않기 때문에, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)는 내부적으로 접근 경로와 연산 순서를 스스로 정해야 한다.

이 기능이 필요한 이유는 선택지가 너무 많기 때문이다. 한 개 테이블만 읽어도 전체 테이블 스캔 (Full Table Scan)과 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 스캔 ([Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) Scan) 중 무엇이 유리한지 달라지고, 두 개 이상 조인하면 [조인 순서](/knowledge-base/studynote/05_database/03_relational_model/176_join_order_optimization/)·구동 테이블·조인 방식까지 경우의 수가 폭증한다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 수천 건일 때는 큰 차이가 없어 보여도, 수천만 건 환경에서는 잘못된 계획 하나가 응답시간을 밀리초에서 수십 초로 바꿔 버린다.

즉 옵티마이저가 없다면 개발자가 SQL 문장 순서에 사실상 물리 경로까지 책임져야 한다. 이는 선언형 언어의 장점을 무너뜨리고, 같은 비즈니스 로직도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)량 변화에 따라 계속 재작성해야 하는 구조를 만든다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│        옵티마이저의 역할: SQL을 물리 실행 경로로 번역하는 과정       │
├──────────────────────────────────────────────────────────────────────┤
│ SQL Text                                                            │
│   │                                                                  │
│   ▼                                                                  │
│ Parse Tree ──▶ Logical Rewrite ──▶ Candidate Plans ──▶ Best Plan     │
│                                   ▲                 │                │
│                                   │                 ▼                │
│                            Statistics / Cost Model  Executor         │
└──────────────────────────────────────────────────────────────────────┘
```

이 그림의 핵심은 옵티마이저가 단순 문법 검사기가 아니라, <strong>통계와 비용 모델을 바탕으로 여러 후보 중 하나를 선택하는 계획 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a>기</strong>라는 점이다. 그래서 SQL 튜닝은 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 문장만 보는 작업이 아니라, [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)이 왜 그렇게 나왔는지를 읽는 작업이 된다.

- **📢 섹션 요약 비유**: 옵티마이저는 목적지만 말하면 도로 상황과 톨게이트 비용까지 계산해 최적 경로를 잡아 주는 내비게이션과 같다. 주소는 같아도 출근 시간과 새벽 시간에 길이 달라지듯, 같은 SQL도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 상황에 따라 다른 계획이 최선이 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

옵티마이저는 보통 <strong><a href="/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a> 변환 → 후보 계획 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> → 비용 추정 → 최종 선택</strong>의 순서로 동작한다. 먼저 파서 (Parser)가 만든 구문 트리를 받아 불필요한 조건을 정리하고, 뷰 병합이나 조건 푸시다운 같은 재작성 (Rewrite)을 수행한다. 그다음 접근 경로, [조인 순서](/knowledge-base/studynote/05_database/03_relational_model/176_join_order_optimization/), 조인 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 조합을 만들고 각 후보의 예상 비용을 계산해 가장 싼 경로를 채택한다.

| 단계 | 하는 일 | 핵심 판단 요소 |
| :--- | :--- | :--- |
| [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 재작성 | 조건 이동, 서브쿼리 변환, 뷰 병합 | 결과 동일성 유지 |
| 접근 경로 선택 | [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 스캔, 풀 스캔 등 결정 | [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) ([Selectivity](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)량 |
| 조인 계획 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | [조인 순서](/knowledge-base/studynote/05_database/03_relational_model/176_join_order_optimization/)와 방식 결정 | 카디널리티 (Cardinality), 메모리 |
| 비용 계산 | I/O, CPU, 메모리 비용 추정 | 통계 정보, 비용 모델 |
| 계획 확정 | 최종 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) 선택 | 최소 예상 비용 |

아래 그림은 후보 계획이 어떻게 갈라지고 다시 하나로 수렴하는지를 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                 후보 계획 생성과 비용 평가의 내부 흐름              │
├──────────────────────────────────────────────────────────────────────┤
│ SQL                                                                  │
│  │                                                                   │
│  ▼                                                                   │
│ Rewrite                                                               │
│  │                                                                   │
│  ├─ Plan A: Index Range Scan + Nested Loop                           │
│  ├─ Plan B: Full Scan + Hash Join                                    │
│  └─ Plan C: Index Scan + Sort Merge Join                             │
│                 │        │        │                                   │
│                 └────────┴────────┴──▶ Cost Estimation               │
│                                         │                             │
│                                         ▼                             │
│                                   Lowest Cost Plan                    │
└──────────────────────────────────────────────────────────────────────┘
```

비용 계산의 핵심 재료는 통계 정보다. 테이블 건수, 특정 값의 분포, [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 깊이, 히스토그램 (Histogram) 같은 정보가 있어야 "이 조건은 전체의 1%만 읽는지, 40%를 읽는지"를 가늠할 수 있다. 예를 들어 조회 대상이 전체의 1%라면 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 범위 스캔이 유리할 수 있지만, 30%를 읽는다면 순차적으로 밀어 읽는 풀 스캔이 오히려 더 저렴해질 수 있다.

따라서 옵티마이저의 원리는 "[인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 있으면 무조건 탄다"가 아니라, <strong>예상 결과 건수와 물리 비용을 비교해 그 순간 가장 경제적인 경로를 택한다</strong>는 데 있다. [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)은 문법의 정답이 아니라 비용 기반의 선택 결과다.

- **📢 섹션 요약 비유**: 옵티마이저는 요리사가 아니라 주방 총괄 관리자에 가깝다. 같은 메뉴를 만들더라도 재료 위치, 조리도구 상태, 주문량을 보고 어떤 조리 순서가 가장 빠른지 미리 짜는 역할이다.

---

## Ⅲ. 비교 및 연결

옵티마이저를 이해할 때 가장 중요한 경계 비교는 <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/164_rbo_rule_based_optimizer/">규칙 기반 옵티마이저</a> (RBO, Rule-Based <a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/088_optimizer/">Optimizer</a>)</strong> 와 <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/165_cbo_cost_based_optimizer/">비용 기반 옵티마이저</a> (CBO, Cost-Based <a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/088_optimizer/">Optimizer</a>)</strong> 의 차이다. RBO는 정해진 우선순위 규칙을 따르므로 예측은 쉽지만 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변화에 둔감하다. 반면 CBO는 통계 정보와 비용 모델을 활용해 유연하게 계획을 바꾸므로 현대 대용량 환경에 훨씬 적합하다.

| 항목 | RBO | CBO |
| :--- | :--- | :--- |
| 판단 기준 | 고정 규칙 | 통계 기반 비용 계산 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변화 적응 | 낮음 | 높음 |
| 장점 | 단순, 예측 용이 | 대용량·복잡 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)에 강함 |
| 약점 | 비현실적 선택 가능 | 통계 오류에 민감 |

또 다른 경계는 **옵티마이저와 실행기 (Executor)** 의 차이다. 옵티마이저는 계획을 세우고, 실행기는 그 계획을 실제로 수행한다. 실행이 느리다고 해서 항상 실행기 문제가 아니라, 그 앞단에서 잘못된 계획이 선택된 결과일 수도 있다. 이 점에서 옵티마이저는 SQL 튜닝, [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 설계, 통계 수집, 조인 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 문서와 긴밀히 연결된다.

예를 들어 [중첩 루프 조인](/knowledge-base/studynote/05_database/03_relational_model/172_nl_join_nested_loop/) ([Nested Loop Join](/knowledge-base/studynote/05_database/07_exam_summary/431_nested_loop_join/))은 소량 탐색에 강하고, [해시 조인](/knowledge-base/studynote/05_database/03_relational_model/174_hash_join/) ([Hash Join](/knowledge-base/studynote/05_database/03_relational_model/174_hash_join/))은 대량 결합에 유리하다. 옵티마이저는 이 차이를 알고 현재 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)량에 맞는 도구를 골라야 한다. 그래서 옵티마이저 문서는 곧 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/), 조인, 통계, [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/) 문서의 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)가 된다.

- **📢 섹션 요약 비유**: RBO가 정해진 메뉴얼만 읽는 신입 기사라면, CBO는 교통량과 연료비를 같이 보는 숙련 운전사다. 그리고 실행기는 길을 실제로 달리는 차이므로, 차가 늦었다고 해서 항상 엔진 문제가 아니라 길 선택이 잘못됐을 수도 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)을 먼저 보고, 그다음 SQL과 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 본다. 예를 들어 쇼핑몰 주문 테이블이 평소 10만 건일 때는 `주문일자` [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 잘 작동했는데, 프로모션 기간에 하루 주문이 5천만 건으로 늘면 같은 조건도 훨씬 많은 행을 읽게 된다. 이때 통계가 갱신되지 않으면 옵티마이저는 여전히 "조금만 읽는다"고 착각해 비효율적인 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 경로를 선택할 수 있다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)에서 예상 건수와 실제 건수가 크게 다르지 않은가?
2. 테이블·[인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 통계 정보가 최근 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변화를 반영하는가?
3. [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)가 낮은 조건에 불필요한 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 기대하고 있지 않은가?
4. [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/) ([Hint](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)) 없이도 안정적인 계획이 나오도록 구조를 개선할 수 있는가?
5. [조인 순서](/knowledge-base/studynote/05_database/03_relational_model/176_join_order_optimization/), 필터 위치, 불필요한 함수 적용이 계획을 왜곡하지 않는가?

### 판단 원칙

- **채택**: 통계가 신뢰 가능하고 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 패턴이 일반적이면 옵티마이저의 선택을 우선 신뢰한다.
- **보완**: [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)이 흔들리면 통계 수집, [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 재설계, SQL 재작성으로 먼저 해결한다.
- **회피 또는 최후 수단**: [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)는 특정 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포에 종속되기 쉬우므로 마지막 수단으로만 사용한다.

기술사 답안에서는 "옵티마이저가 빠르게 해 준다"보다, <strong>왜 그 계획이 선택되었는지와 언제 오판할 수 있는지</strong>를 함께 설명해야 점수가 높다. 특히 통계 정보의 품질과 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 절차를 언급하면 실무 감각이 드러난다.

- **📢 섹션 요약 비유**: 옵티마이저 튜닝은 내비게이션 화면만 보고 불평하는 일이 아니다. 지도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 최신인지, 도로가 새로 막혔는지, 목적지 입력이 정확한지부터 점검해야 진짜 원인을 찾을 수 있다.

---

## Ⅴ. 기대효과 및 결론

좋은 옵티마이저는 같은 하드웨어에서도 더 적은 자원으로 더 빠른 응답을 만든다. 이는 단순 속도 향상에 그치지 않고, 피크 시간대 서버 안정성, 배치 작업 완료 시간, 동시 사용자 수용 능력까지 좌우한다. 특히 선언형 SQL의 생산성을 유지하면서도 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 확보할 수 있게 해 준다는 점에서 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 핵심 경쟁력이다.

다만 옵티마이저가 만능은 아니다. 통계가 낡거나 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 편향이 심하면 잘못된 계획을 낼 수 있고, 환경이 바뀌면 같은 SQL의 계획도 달라질 수 있다. 따라서 옵티마이저는 "자동 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 보장 장치"가 아니라, <strong>통계·<a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a>·SQL 구조와 함께 움직이는 적응형 의사결정 엔진</strong>으로 기억해야 한다.

앞으로는 적응형 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 처리, 실행 중 재최적화, 피드백 기반 카디널리티 보정처럼 런타임 정보까지 반영하는 방향이 더 중요해진다. 결론적으로 옵티마이저의 본질은 SQL을 이해하는 기능이 아니라, <strong>하드웨어 비용을 가장 적게 쓰는 물리 경로를 고르는 판단 시스템</strong>이다.

- **📢 섹션 요약 비유**: 좋은 옵티마이저는 단순히 빠른 길을 찾는 것이 아니라, 차가 막혀도 목적지까지 가장 덜 지치고 가장 안정적으로 도착하게 만드는 숙련된 배차 관리자와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) ([Execution Plan](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)) | 옵티마이저가 최종 산출하는 물리 경로 |
| RBO (Rule-Based [Optimizer](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_optimizer/)) | 규칙 중심의 과거 방식 |
| CBO (Cost-Based [Optimizer](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_optimizer/)) | 통계와 비용 모델 기반의 현대 방식 |
| [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) ([Selectivity](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/)) | [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 사용 여부 판단의 핵심 지표 |
| 조인 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 중첩 루프·해시·정렬 병합 조인 선택 대상 |
| [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/) ([Hint](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)) | 옵티마이저 선택을 제한하거나 유도하는 수단 |

### 📈 관련 키워드 및 발전 흐름도

```text
선언형 SQL
    │
    ▼
논리 재작성 (Rewrite)
    │
    ▼
실행 계획 (Execution Plan) 생성
    │
    ▼
RBO → CBO
    │
    ▼
통계 정보 · 히스토그램 · 적응형 최적화
```

이 흐름은 "문장 해석 → 계획 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) → 비용 기반 판단 → 지능화"로 발전하는 옵티마이저의 진화를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 옵티마이저는 "장난감을 어디서 어떻게 찾을지"를 먼저 정해 주는 똑똑한 도우미예요.
2. 같은 장난감이라도 책상 서랍을 열지, 장난감 상자를 통째로 뒤질지에 따라 시간이 많이 달라져요.
3. 그래서 컴퓨터는 먼저 가장 덜 힘들고 가장 빠른 찾기 방법을 골라 놓고 움직인답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 163 / 600

← **이전**: [162. 함수 기반 인덱스 (FBI, Function Based Index) - 산술식이나 함수가 적용된 결과 기준 인덱싱](/knowledge-base/studynote/05_database/03_relational_model/162_fbi_function_based_index/)
**다음**: [164. 규칙 기반 옵티마이저 (RBO, Rule Based Optimizer) - 정해진 우선순위 규칙에 따라 계획 수립 (구형)](/knowledge-base/studynote/05_database/03_relational_model/164_rbo_rule_based_optimizer/) →

---
