+++
title = "16. 망형 데이터 모델 (Network Model) - 그래프 구조 (N:M 허용)"
description = "다대다(N:M) 관계의 복잡성을 포인터 그래프 구조로 해결하려 했던 CODASYL 표준 모델과 그 한계점"
date = 2024-05-18

[taxonomies]
tags = ["database"]

[extra]
tags = ["database"]
+++

# 16. 망형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/) (Network Model) - [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 구조

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 계층형 모델의 단일 부모 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)(1:N) 한계를 극복하기 위해, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 노드(개체)와 간선(포인터)의 유향 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)(Directed [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/888_graph/)) 형태로 연결하여 N:M([다대다](/knowledge-base/studynote/02_operating_system/02_process_thread/100_many_to_many_model/)) [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 허용한 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)이다.
> 2. **가치**: 현실 세계의 복잡한 네트워크적 비즈니스 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 잃지 않으면서 디스크 레벨의 물리적 연결(Link List)로 정밀하게 구현해냈다.
> 3. **융합**: 고도의 프로그래밍 복잡성으로 인해 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델(RDBMS)에 패배했으나, 그 밑바탕이 된 '[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 중심의 포인터 순회 탐색' 사상은 현대의 [그래프 데이터베이스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/039_graph_db/)([Graph DB](/knowledge-base/studynote/14_data_engineering/01_infrastructure/039_graph_db/), Neo4j)로 완벽하게 계승/발전되었다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

1960년대 후반, 최초의 상용 모델이었던 [계층형 데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/015_hierarchical_data_model/)(트리 구조)은 심각한 구조적 병목에 직면했다. 한 학생이 여러 과목을 수강하고 한 과목도 여러 학생에게 수강되는 일상적인 [다대다](/knowledge-base/studynote/02_operating_system/02_process_thread/100_many_to_many_model/)(N:M) 비즈니스 환경에서, 트리 구조는 자식이 단 하나의 부모만 가져야 한다는 규칙 때문에 엄청난 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복 저장과 [갱신 이상](/knowledge-base/studynote/05_database/02_modeling_normalization/093_update_anomaly/)([Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/)) 현상을 유발했다.

이 복잡한 얽힘 문제를 해결하기 위해 CODASYL([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 시스템 언어 위원회) DBTG 그룹은 망형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)(Network [Data Model](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/))을 제안했다. 이 모델의 핵심 혁신은 자식 레코드가 여러 부모 레코드와 연결될 수 있도록 허용한 것이다. 이를 통해 조직, 사람, 제품, 주문이 거미줄처럼 복잡하게 얽힌 현실 세계를 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 형태의 물리적 포인터 묶음으로 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)할 수 있었다.

그러나 "자유롭게 연결할 수 있다"는 것은 곧 "탐색 구조가 극도로 복잡해진다"는 것을 의미했다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 거미줄처럼 얽혀 있어, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 조회하려면 프로그래머가 복잡한 포인터 경로를 한 치의 오차도 없이 코딩해야만 하는 심각한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Dependency) 문제를 낳게 되었다.

```text
[그림 1: 망형 데이터 모델의 N:M 그래프 연결 구조 (Owner-Member 체계)]

    [고객 개체: 홍길동]           [고객 개체: 이순신]
           | +---------+         +---------+ |
           |           |         |           |
 (Member 링크)        (다중 부모 허용 구조)   (Member 링크)
           v           v         v           v
      [계좌_A]       [계좌_B (공동계좌)]     [계좌_C]
           |                 |               |
           +-------+         |      +--------+
                   v         v      v
                 [은행 지점: 강남 본점]
```

이 도식은 한 계좌(계좌_B)가 고객 홍길동과 이순신이라는 두 개의 부모 노드(Owner)를 동시에 가지며 연결되는 모습을 보여준다. 계층형 모델에서는 불가능했던 다중 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)(N:M 매핑)이 가능해져 중복 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)을 완벽히 막아낸 혁신적인 상태를 묘사한다. 하지만 이 노드들 간의 선 화살표는 단순한 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 개념이 아니라 디스크 내부의 '물리적 포인터 주소 체계'였기 때문에 선 하나가 끊어지면 전체 망이 붕괴되는 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)를 안고 있었다.

📢 **섹션 요약 비유**: 망형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)은 서울의 복잡한 지하철 환승 노선도처럼, 출발지와 목적지(N:M)를 자유롭게 연결해 주지만 노선이 너무 얽혀있어 처음 보는 사람은 길을 잃기 십상인 거대 미로와 같습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

망형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 레코드 타입(Record Type)과 레코드 간의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 맺어주는 세트 타입(Set Type)으로 엄격하게 정의한다. 이를 구현하기 위해 복잡한 환형 [연결 리스트](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)(Circular [Linked List](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)) 자료구조를 엔진 내부에 차용한다.

| 핵심 구성 요소 | 역할 | 내부 동작 메커니즘 | 비유 |
|:---|:---|:---|:---|
| **레코드 타입 (Record)** | 실질적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 단위 | 개체(Entity)에 해당하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 필드 집합 (예: 고객 레코드, 주문 레코드) | 지하철역 (Node) |
| **세트 타입 (Set Type)** | 두 레코드 간의 1:N [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 링크 | 오너(부모)와 멤버(자식)를 묶는 포인터들의 집합 이름 | 두 역을 잇는 철로 (Edge) |
| **오너 (Owner) 레코드** | 세트를 지배하는 부모 노드 | 세트 내에서 유일해야 하며, 다수의 멤버를 거느림 | 회사의 팀장 |
| **멤버 (Member) 레코드** | 세트에 종속된 자식 노드 | 계층형과 달리 <strong>여러 서로 다른 세트의 멤버</strong>가 될 수 있음 (N:M의 비결) | 여러 프로젝트에 차출되는 팀원 |
| **포인터 순회 연산** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조작 및 검색 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | `FIND NEXT`, `FIND OWNER`, `FIND MEMBER` 등 메모리 주소 점프 명령 | 지하철 환승로 표지판 따라 걷기 |

<strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/100_many_to_many_model/">다대다</a>(N:M) 구현의 핵심: 교차 레코드 (Intersection Record)</strong>
망형 모델도 순수하게 M:N 포인터를 직접 그리면 무한 루프나 교착에 빠진다. 따라서 실무 설계에서는 M:N [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 두 개의 1:N 세트로 쪼개고, 그 중간에 물리적인 '교차 레코드(연결 노드)'를 두어 해결했다. 이는 훗날 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB의 '매핑 테이블([Mapping](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/) Table)' 설계 기법의 직접적인 원형이 되었다.

```text
[그림 2: 망형 데이터베이스 내부의 환형 연결 리스트(Circular Linked List) 탐색 포인터 체계]

[오너 레코드: IT 부서] --------------------------+ (First Pointer)
       ^                                         |
       |                                         v
(Owner Pointer)   +-(Next)-> [멤버: 홍개발] -(Next)-> [멤버: 김운영]
       |          |                              |
       +-(Prior)--+<---------(Prior)-------------+

* 개발자 탐색 쿼리:
  1. FIND ANY 부서 USING 'IT 부서'
  2. FIND FIRST 사원 WITHIN 부서_사원_세트
  3. FIND NEXT 사원 WITHIN 부서_사원_세트 (조건 충족 시까지 루프)
```

이 구조도는 겉보기에는 단순한 집합처럼 보이지만, 실제 스토리지 엔진 내부에서는 오너와 멤버가 'First, Next, Prior, Owner'라는 4중 포인터 체인으로 강하게 결합되어 있음을 드러낸다. 이런 포인터 탐색 구조의 치명적인 병목은 애플리케이션 코드가 물리적 포인터 이름과 경로 순서에 100% 종속된다는 것이다. 만약 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 위해 디스크 포인터 구조를 재배열하면, 모든 애플리케이션의 `FIND NEXT` 반복문 코드를 전면 수정해야 하는 악몽([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 심화)이 펼쳐진다.

📢 **섹션 요약 비유**: 친구 집을 찾아갈 때 "서울시 강남구 123번지(SQL)"를 입력하는 게 아니라, "역에서 내려서 왼쪽으로 100m 걷고 두 번째 골목 우회전(포인터 순회)"하라는 지시서를 개발자가 직접 쓰는 셈입니다. 길 공사(DB 구조 변경)가 나면 지시서를 다 폐기해야 합니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

망형 모델의 실패와 현대 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB의 부활을 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델과 비교하여 분석하면, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 아키텍처의 패러다임 이동(Paradigm Shift)을 뚜렷하게 관찰할 수 있다.

| 구분 | 망형 모델 (1970's) | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델 (RDBMS, 1980's~) | [그래프 데이터베이스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/039_graph_db/) (Neo4j, 현대) |
|:---|:---|:---|:---|
| **설계 철학** | 복잡한 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)의 "물리적 포인터 연결" | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)의 "[논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적(값 기반) 수학적 분리" | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 1급 시민(First-Class)으로 취급 |
| <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a> 표현</strong> | 세트 타입 (Set, 포인터명 명시) | [외래 키](/knowledge-base/studynote/05_database/02_modeling_normalization/072_foreign_key_fk/) (Foreign [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)) 값 매칭 | 엣지 (Edge) 자체에 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)과 의미 부여 |
| **질의 방식** | 개발자의 수동 네비게이션 루프 | 선언적 SQL ([DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) [옵티마이저](/knowledge-base/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)가 탐색) | 선언적 탐색어 (Cypher/Gremlin, 패턴 매칭) |
| <strong>조인 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | 빠름 (사전 연결된 주소 직행) | 느림 (실행 시 메모리 해시/루프 매칭 필요) | **가장 빠름** ([Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)-Free [Adjacency](/knowledge-base/studynote/03_network/07_network_layer_routing/358_ospf_adjacency_hello_lsa_lsdb/) 활용) |
| **확장성/독립성** | 최악 (구조 변경 시 앱 전면 재개발) | **최고** ([논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)/물리 완벽 분리) | 우수 ([스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)리스 및 확장 지원) |

**왜 망형 모델은 멸망했는가? (트레이드오프 분석)**
망형 모델은 CPU 파워가 극히 제한적이던 시절, 디스크에서 레코드를 한 번의 I/O로 빠르게 낚아채기 위해 '[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)'에 모든 것을 걸어 '개발 생산성([데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/))'을 희생한 아키텍처다. 반면 E.F. Codd의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델은 하드웨어 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 발전을 믿고, 포인터를 없애는 대신 수학적 조인([Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/)) 연산으로 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)하여 프로그래머를 포인터 미로에서 해방시켰다. 이 생산성의 차이가 승패를 갈랐다.

```text
[그림 3: 관계 표현에 따른 탐색 성능 및 유연성 트레이드오프 매트릭스]

        [데이터 독립성 (유연성 & 생산성)]
               ^
               |          [RDBMS]
      높음     |         (SQL: 논리적 매칭)
               |                 *
               |
      중간     |                          [Graph DB]
               |                         (패턴 매칭 + 엣지 포인터)
               |                                *
               +-----------------------------------------> [탐색 성능 (조인 속도)]
               |                  *
      낮음     |          [망형 모델]           (Index-Free 고속 연결)
               |   (하드코딩 포인터 체인)
               v
```

이 분석 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)는 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 역사의 변증법적 진화를 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)한다. 망형 모델은 탐색 속도는 빠르지만 유연성이 바닥이라 도태되었다. RDBMS는 유연성을 극대화했으나 대량의 딥 조인(Deep [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/)) 시 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 기하급수적으로 저하된다. 현대의 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB(Neo4j)는 망형 모델의 포인터 연결 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 아이디어([Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)-Free [Adjacency](/knowledge-base/studynote/03_network/07_network_layer_routing/358_ospf_adjacency_hello_lsa_lsdb/))를 차용하되, RDBMS처럼 선언적 질의어(Cypher)를 덧씌워 두 마리 토끼([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 유연성)를 모두 잡은 아키텍처 진화의 결과물임을 알 수 있다.

📢 **섹션 요약 비유**: 망형 모델이 조종석 버튼이 100개인 수동 헬리콥터였다면, RDBMS는 목적지만 누르면 가는 자율주행 자동차입니다. 그리고 현대 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB는 자율주행 기능에 날개까지 단 플라잉카라 할 수 있습니다.

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무에서 직접적인 CODASYL 기반의 망형 [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/)(예: IDMS)를 도입하거나 구축하는 프로젝트는 이제 지구상에 존재하지 않는다. 하지만, 시스템 엔지니어는 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 고도로 복잡한(Highly Connected) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다룰 때 망형 모델의 아키텍처적 한계와 [교훈](/knowledge-base/studynote/09_security/13_secops_ir_forensics/659_ir_lessons_learned/)을 바탕으로 올바른 기술 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)을 선택(Decision)해야 한다.

<strong>1. 실무 시나리오: 소셜 네트워크 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>(SNS) 친구 추천 엔진 구축</strong>
- **상황**: "나의 친구의 친구 중 나와 같은 학교를 나온 사람"을 찾는 기능(Depth 3 이상의 N:M 조인)을 RDBMS 상에서 구현했으나, `JOIN` 연산이 3번 이상 중첩되며 [카티션 프로덕트](/knowledge-base/studynote/05_database/07_exam_summary/412_cartesian_product/)가 폭발해 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 수 분간 정체되는 장애(병목) 발생.
- **판단**: 이런 연결 중심([Relationship](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)-Centric)의 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)는 RDBMS의 구조적 한계다. 과거 망형 모델이 잘하던 '포인터 직결 탐색' 방식이 필요하다. 따라서 의도적인 반정규화를 무리하게 수행하기보다는, 백엔드 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)를 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 모델(Neo4j, Amazon Neptune 등)로 분리 마이그레이션하여 포인터 순회 방식으로 밀리초(ms) 단위의 응답을 확보해야 강건한 아키텍처가 된다.

<strong>2. 객체-<a href="/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a> 매핑(ORM) 설계 시 N+1 문제 대응 판단</strong>
- **현상**: JPA나 Hibernate를 사용할 때, 부모 엔티티를 조회하면 자식 엔티티들을 가져오기 위해 수십 개의 추가 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 발생하는 N+1 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 현상 발생.
- <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>: 망형 모델처럼 객체(Object)의 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 포인터(Get/Set)를 무한정 따라가며 [지연 로딩](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/)([Lazy Loading](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/))을 방치하는 행위.
- **해결책**: 객체 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 네비게이션의 맹점을 끊어내고, RDB의 강점인 집합 연산 능력을 활용하여 Fetch [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 등을 통해 한 번의 SQL로 테이블을 결합(Eager Loading)하여 메모리에 올리도록 아키텍처 튜닝을 지시해야 한다.

```text
[그림 4: 딥 조인(Deep Join) 요건 발생 시 아키텍처 분기 의사결정 트리]

[데이터 요건: 여러 테이블 간의 복잡한 다대다 연결 및 다단계 탐색 필요]
               |
               v
[조인의 깊이(Depth)와 탐색 관계의 빈도가 어느 정도인가?]
       +- Depth 2~3 이내 (일반적 업무 요건)
       |       v
       |  [RDBMS 유지] --> 중간 매핑 테이블(Intersection) 설계 및 인덱스 튜닝
       |
       +- Depth 4 이상 또는 관계(연결) 자체가 핵심 비즈니스인 경우 (추천, 사기탐지 등)
               v
   [그래프 모델 적용 검토] --> 과거 망형 모델의 후예인 Neo4j 등 Graph DB 도입
               |               (Index-Free Adjacency로 조인 연산 오버헤드 완벽 회피)
```

이 [의사결정 트리](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 '[관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)' 깊이에 따라 RDB로 버틸지, [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 기반의 모델로 아키텍처를 전환할지를 결정하는 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)이다. 조인이 깊어질수록 RDBMS는 지수적인 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하를 겪는 반면, 포인터를 따라가는 망형/[그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 아키텍처는 깊이와 무관하게 선형적인 탐색 속도를 유지한다는 시스템 구조적 차이에 기인한 판단이다.

📢 **섹션 요약 비유**: RDBMS가 엑셀 표로 된 깔끔한 주소록이라면, 엑셀 표에서 "A의 친구의 동생의 회사 동료"를 찾는 건 눈이 빠지는 작업입니다. 이때는 인물들이 선으로 이어진 마인드맵([그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)/망형 모델) 보드를 꺼내 드는 것이 현명한 판단입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)

[데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 역사에서 망형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 기능(N:M 허용)을 위해 복잡성을 통제하지 못한 "[안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)의 위대한 교보재"로 평가받는다.

1970년대 CODASYL 표준에 의해 주도되었으나, Codd 박사의 논문 "A [Relational Model](/knowledge-base/studynote/05_database/01_db_architecture_relational/017_relational_data_model/) of [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) for Large Shared [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Banks"에 의해 철저하게 논파당하며 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 기술의 주도권은 '비절차적이고 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적인(SQL) RDBMS'로 완전히 넘어갔다.
하지만 현대 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))과 빅데이터 시대에 접어들며, [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)), [시맨틱 웹](/knowledge-base/studynote/06_ict_convergence/01_blockchain/003_semantic_web/), 소셜 분석 등 극도로 복잡하게 얽힌 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/)으로 실시간 처리해야 하는 요건이 폭증하고 있다. 이에 따라 망형 모델이 1970년대에 꿈꾸었던 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 간의 촘촘한 물리적 연결망"이라는 이상향은, 하드웨어의 눈부신 발전과 선언적 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)(Cypher 등) 엔진이라는 새 옷을 입고 <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/039_graph_db/">그래프 데이터베이스</a>(<a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/039_graph_db/">Graph Database</a>)</strong>라는 이름으로 화려하게 귀환하여 현대 [데이터 아키텍처](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)의 필수 융합 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)으로 자리매김하고 있다.

📢 **섹션 요약 비유**: 망형 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)은 시대를 너무 앞서갔지만 조종법이 괴랄하여 외면받았던 '최초의 비행 기계'와 같습니다. 지금은 그 도면을 바탕으로 컴퓨터가 대신 조종해 주는 세련된 첨단 드론([그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB)으로 세상을 날고 있습니다.

---
### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- [계층형 데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/015_hierarchical_data_model/) ([Hierarchical Model](/knowledge-base/studynote/05_database/01_db_architecture_relational/015_hierarchical_data_model/)) | 망형 모델의 이전 세대로, 트리 구조와 1:N 단일 부모 제약이라는 한계를 가졌던 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)
- [관계형 데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/017_relational_data_model/) ([Relational Model](/knowledge-base/studynote/05_database/01_db_architecture_relational/017_relational_data_model/)) | 망형 모델의 복잡한 포인터를 제거하고 수학적 테이블 집합과 키 매핑으로 대체한 현대 DBMS의 사실상 표준
- [그래프 데이터베이스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/039_graph_db/) ([Graph Database](/knowledge-base/studynote/14_data_engineering/01_infrastructure/039_graph_db/)) | 망형 모델의 노드-엣지 연결 개념을 현대적으로 계승하여 딥 조인 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 한계를 극복한 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) 시스템
- [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/) ([Data Independence](/knowledge-base/studynote/05_database/04_transactions_concurrency/504_data_independence/)) | 망형 모델이 실패한 가장 큰 원인으로, 하드웨어 물리 포인터 구조와 애플리케이션 코드를 분리하는 설계 원칙
- N:M [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) ([다대다](/knowledge-base/studynote/02_operating_system/02_process_thread/100_many_to_many_model/) [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)) | 망형 모델이 계층형과 달리 허용했던 다중 부모 연결 구조이자, RDB에서는 매핑 테이블을 통해 구현해야 하는 복잡한 비즈니스 요건


### 📈 관련 키워드 및 발전 흐름도

```text
[계층형 데이터 모델 (Hierarchical Model) — 트리 구조, 1:N 단일 부모 제약]
    |
    v
[망형 데이터 모델 (Network Model / CODASYL) — 포인터 기반 N:M 관계 허용]
    |
    v
[관계형 데이터 모델 (Relational Model) — 수학적 테이블, SQL 선언적 질의]
    |
    v
[객체지향 DB (OODB) — 복잡한 객체와 메서드를 직접 영속화]
    |
    v
[그래프 데이터베이스 (Graph DB) — 노드-엣지 구조로 딥 조인 성능 한계 극복]
```
이 흐름은 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)이 물리적 포인터 복잡성의 한계를 반성하고 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 모델로 수렴되었다가, 고도로 연결된 현대 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 딥 탐색 요건에 부응하여 [그래프 데이터베이스](/knowledge-base/studynote/14_data_engineering/01_infrastructure/039_graph_db/)로 [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)환하는 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/) 패러다임의 순환 진화를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 망형 모델은 친구들과 손과 발을 모두 끈으로 묶어서 거미줄처럼 다 같이 연결된 형태예요.
2. 끈이 연결되어 있어서 누구와 누가 친구인지 선을 따라가면 바로 알 수 있어서 아주 빨라요.
3. 하지만 친구가 늘어날수록 끈이 너무 많이 꼬여서 한 명만 움직여도 모두가 넘어지는 복잡한 문제가 생겨서 지금은 쓰지 않는 방법이 되었어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 16 / 600

<- **이전**: [15. 계층형 데이터 모델 (Hierarchical Model) - 트리 구조 (1:N)](/knowledge-base/studynote/05_database/01_db_architecture_relational/015_hierarchical_data_model/)
**다음**: [17. 관계형 데이터 모델 (Relational Model) - 테이블 구조, E.F. Codd 제안](/knowledge-base/studynote/05_database/01_db_architecture_relational/017_relational_data_model/) ->

---
