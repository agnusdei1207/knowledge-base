---
title: "Polyglot Persistence"
date: "2026-05-06"
tags:
  - "studynote-enterprise-systems"
weight: 172
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/) ([Polyglot Persistence](/studynote/13_cloud_architecture/03_msa_serverless/132_polyglot_persistence/))는 모든 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 하나의 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)에 맞추는 대신, 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 자신의 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 특성과 접근 패턴에 맞는 저장소를 선택하는 아키텍처 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.
> 2. **가치**: 주문은 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터베이스 관리 시스템](/studynote/05_database/01_db_architecture_relational/003_dbms_database_management_system/) (RDBMS, Relational [Database](/studynote/05_database/04_transactions_concurrency/501_database/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/) System), [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)은 [키-값 저장소](/studynote/14_data_engineering/01_infrastructure/036_key_value/), 추천은 [그래프 데이터베이스](/studynote/14_data_engineering/01_infrastructure/039_graph_db/)처럼 목적에 맞는 저장 기술을 쓰면 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 개발 생산성을 동시에 높일 수 있다.
> 3. **판단 포인트**: 진짜 전제는 기술 다양성이 아니라 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유권, 운영 역량, [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 정합성 설계이며, 이 준비 없이 DB만 늘리면 최적화가 아니라 운영 복잡도만 폭증한다.

---

## Ⅰ. 개요 및 필요성

[폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)는 여러 저장 기술을 무작정 섞어 쓰는 유행어가 아니다. 정확히는 <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>별 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 특성과 비즈니스 요구에 따라 서로 다른 저장 모델을 선택하는 설계 원칙</strong>이다. 같은 시스템 안에도 강한 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 필요한 주문 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변화가 잦은 상품 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 초저지연이 필요한 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 탐색이 중요한 추천 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 공존한다.

단일 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 운영과 교육 측면에서 단순하지만, 모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 하나의 모델에 억지로 맞추는 순간 문제가 생긴다. 예를 들어 주문과 결제는 ACID ([Atomicity](/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/), [Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/), [Durability](/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/)) 보장이 중요하지만, 상품 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)는 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 구조가 자주 바뀌고, 추천은 연결 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 탐색이 핵심이다. 하나의 RDBMS로 모두 해결하려 하면 과도한 조인, 복잡한 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 컬럼, 비효율적인 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 설계 같은 우회로가 늘어난다.

[마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), [Microservices Architecture](/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) 가 확산되며 이 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 더 중요해진 이유도 여기에 있다. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 독립 배포와 독립 확장을 지향한다면, 저장소도 그 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 요구에 맞게 독립적이어야 한다. 즉 [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)는 기술 과시가 아니라 <strong><a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a>별 적합성 확보</strong>를 위한 선택이다.

이 그림은 공유 DB [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)의 차이를 보여 준다.

```text
+----------------------------------------------------------------------+
|              One shared store versus fit-for-purpose stores          |
+----------------------------------------------------------------------+
| shared DB : Order / Catalog / Session / Recommendation -> one RDBMS |
|                                                                      |
| polyglot : Order -> RDBMS                                            |
|            Catalog -> document DB                                    |
|            Session -> key-value store                                |
|            Recommendation -> graph DB                                |
+----------------------------------------------------------------------+
```

핵심은 저장소 수가 아니라 <strong><a href="/studynote/05_database/01_db_architecture_relational/014_data_model_components/">데이터 모델</a>과 접근 패턴의 부합성</strong>이다. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 문제를 저장소가 더 자연스럽게 표현할 수 있을 때 [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)의 가치가 생긴다.

- **📢 섹션 요약 비유**: 모든 요리를 한 냄비로 만들 수는 있지만, 국물요리와 볶음요리와 빵 굽기를 같은 도구로 처리하면 맛도 효율도 떨어진다. [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)는 요리에 맞는 조리도구를 고르는 일과 비슷하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)가 성립하려면 먼저 [데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/) ([Database per Service](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/)) 원칙이 필요하다. 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 자기 저장소의 <strong>소유권과 변경 책임</strong>을 가져야 하며, 다른 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 그 DB를 직접 조인하거나 갱신하지 않는다. 그래야 저장 기술을 독립적으로 바꿀 자유가 생긴다.

| [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)/워크로드 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 성격 | 자주 쓰는 저장소 | 선택 이유 |
| :--- | :--- | :--- | :--- |
| 주문·결제 | 강한 정합성, [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 중심 | RDBMS | ACID, [참조 무결성](/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/), 회계 처리 적합 |
| 상품 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) | [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 구조 변화, 문서 단위 조회 | 문서 지향 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) ([Document](/studynote/14_data_engineering/01_infrastructure/037_document/) [Database](/studynote/05_database/04_transactions_concurrency/501_database/)) | 유연한 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)와 집계 문서 모델 |
| [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)·장바구니 | 초저지연, 단순 키 접근 | [키-값 저장소](/studynote/14_data_engineering/01_infrastructure/036_key_value/) ([Key-Value Store](/studynote/14_data_engineering/01_infrastructure/036_key_value/)) | 빠른 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), [TTL](/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) 처리 |
| 추천·[관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 분석 | 연결 탐색, 다중 홉 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | [그래프 데이터베이스](/studynote/14_data_engineering/01_infrastructure/039_graph_db/) ([Graph Database](/studynote/14_data_engineering/01_infrastructure/039_graph_db/)) | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 질의와 경로 탐색 효율 |

하지만 저장소를 나누는 순간 정합성은 자동으로 따라오지 않는다. 주문 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 상태가 바뀌면 배송 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)나 분석 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)도 이를 알아야 하므로, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 연계는 직접 SQL 조인이 아니라 이벤트, 응용 프로그래밍 인터페이스 ([API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)), [변경 데이터 캡처](/studynote/12_it_management/05_security_compliance/218_cdc_change_data_capture/) ([CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/), [Change Data Capture](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)), [트랜잭셔널 아웃박스](/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/) ([Transactional Outbox](/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/)) 같은 방식으로 풀어야 한다.

아래 구조는 [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)가 "DB 여러 개"가 아니라 "[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 소유 + 이벤트 연계"라는 점을 보여 준다.

```text
+----------------------------------------------------------------------+
|              Service-owned stores with event-based linkage           |
+----------------------------------------------------------------------+
| Order Service ----------> Order DB ----------> Outbox event          |
| Catalog Service --------> Catalog DB --------> API / event           |
| Recommendation Service -> Graph DB <--------- subscribed events      |
|                                                                      |
| rule: no cross-service direct joins, integrate through contracts      |
+----------------------------------------------------------------------+
```

즉 [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)의 핵심 원리는 "자기 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 진실 원천(Source of Truth)은 자기 저장소 안에 둔다"는 것이다. 다른 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 그 진실을 API나 이벤트로 소비할 뿐이며, 그 과정에서 결국 최종적 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Eventual Consistency](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) 을 받아들일 준비가 필요하다.

- **📢 섹션 요약 비유**: 각 부서가 자기 서류함을 책임지고, 다른 부서가 필요하면 공식 공문이나 전달 시스템으로 받아보는 구조가 [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)다. 남의 서류함을 마음대로 열어보는 순간 독립성은 무너진다.

---

## Ⅲ. 비교 및 연결

[폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)를 이해하려면 "공유 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)", "[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 DB이지만 같은 엔진", "[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 다른 엔진"을 구분해야 한다. 세 방식은 독립성과 복잡도의 균형점이 다르다.

| 비교 축 | 공유 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 동일 엔진 DB | [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/) |
| :--- | :--- | :--- | :--- |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유권 | 약함 | 중간 | 강함 |
| 기술 다양성 | 낮음 | 낮음 | 높음 |
| 워크로드 적합성 | 낮음 | 중간 | 높음 |
| 정합성 처리 | 로컬 조인 중심 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계 일부 필요 | 이벤트·[사가](/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/) 중심 |
| 운영 복잡도 | 낮음 | 중간 | 높음 |

즉 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 DB를 쓴다고 해서 곧바로 [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)는 아니다. 모든 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 여전히 같은 MySQL만 쓴다면 독립성은 생기지만, 저장 모델의 다양성을 활용하는 단계까지는 아니다. 반대로 저장소만 여러 개 도입하고 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계가 흐리면, 진짜 이점 없이 운영 부담만 커진다.

이 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 [사가 패턴](/studynote/12_it_management/05_security_compliance/305_saga/) ([Saga](/studynote/12_it_management/05_security_compliance/305_saga/)), [명령-조회 책임 분리](/studynote/11_design_supervision/06_exam_summary/368_cqrs/) ([CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/), [Command Query Responsibility Segregation](/studynote/06_ict_convergence/03_cloud_infrastructure/250_cqrs_command_query_responsibility_segregation_pattern/)), [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) ([Event Sourcing](/studynote/12_it_management/05_security_compliance/307_event_sourcing/)) 과도 자주 연결된다. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)마다 저장 모델이 달라질수록 전역 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 대신 이벤트 기반 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)와 읽기 모델 분리가 중요해지기 때문이다. 따라서 [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)는 독립적인 저장소 선택 문제이면서 동시에 <strong>통합 방식의 재설계 문제</strong>이기도 하다.

- **📢 섹션 요약 비유**: 모두가 같은 서랍장을 쓰면 관리가 단순하지만 물건 특성에 맞춘 보관은 어렵다. 반대로 냉장고, 책장, 공구함을 따로 두면 효율은 올라가지만, 어디에 무엇이 있는지 관리 규칙도 함께 필요해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

전자상거래를 예로 들면, 주문·결제 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 RDBMS가 자연스럽고, 상품 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)는 문서 지향 저장소가 잘 맞으며, [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)과 캐시는 [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) 같은 [키-값 저장소](/studynote/14_data_engineering/01_infrastructure/036_key_value/)가 유리하다. 추천 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 따라가는 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 질의가 많다면 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) DB가 이점을 줄 수 있다. 이처럼 <strong><a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 경계와 접근 패턴이 분명히 다를 때</strong> [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)의 설득력이 커진다.

하지만 같은 조직이라도 모든 팀이 여러 저장소를 운영할 역량을 갖춘 것은 아니다. [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링, 장애 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 보안 패치, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마이그레이션, 드라이버 관리가 모두 다양해지기 때문이다. 그래서 많은 경우 "먼저 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 DB 분리, 필요 시 일부 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)만 다른 엔진 채택"이 현실적인 접근이다.

아래 결정 흐름은 [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)를 도입할지 판단하는 최소 질문을 정리한 것이다.

```text
+----------------------------------------------------------------------+
|        Is polyglot persistence really justified for this domain?     |
+----------------------------------------------------------------------+
| service boundary and ownership clear?                                |
|        +- no  -> keep a simpler store strategy first                 |
|        +- yes                                                         |
| workload/consistency needs differ materially?                        |
|        +- no  -> same-engine database per service may be enough      |
|        +- yes                                                         |
| ops and integration patterns ready?                                  |
|        +- no  -> complexity risk high                                |
|        +- yes -> polyglot candidate                                  |
+----------------------------------------------------------------------+
```

### 기술사 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유권이 명확한가?
2. 저장 모델 차이가 실제 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·생산성 이득으로 이어지는가?
3. 이벤트, [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/), [사가](/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/) 같은 연계 방식이 준비되어 있는가?
4. 팀이 여러 저장소의 운영·[백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)·보안·[모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링을 감당할 수 있는가?
5. 전역 조인과 전역 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 요구를 어떻게 줄일지 합의되었는가?

### 자주 나오는 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 분리했지만 여전히 서로의 DB를 직접 조회하는 경우
- "유행이라서" 저장소를 늘리고, 실제 워크로드 차이는 설명하지 못하는 경우
- 모든 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계를 [2단계 커밋](/studynote/05_database/04_transactions_concurrency/249_two_phase_commit_2pc_distributed/) ([2PC](/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/), [Two-Phase Commit](/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/)) 으로 묶어 복잡도만 키우는 경우
- 조회 편의를 위해 교차 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 조인을 남발해 저장소 독립성을 깨는 경우

좋은 [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)는 DB 종류의 수를 자랑하지 않는다. 오히려 어디까지는 단순성을 유지하고, 어디서부터 저장 모델을 달리해야 하는지 <strong>절제된 분화</strong>를 만드는 설계가 더 중요하다.

- **📢 섹션 요약 비유**: 공구함에 망치, 드라이버, 톱을 따로 두는 것은 현명하지만, 쓰지도 않을 공구를 잔뜩 사서 관리만 힘들어지면 실패다. [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)도 꼭 필요한 도구만 늘려야 가치가 생긴다.

---

## Ⅴ. 기대효과 및 결론

[폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)를 적절히 적용하면 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화, 팀 자율성, 확장성, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 유연성을 함께 확보할 수 있다. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 자신에게 맞는 저장 모델과 배포 주기를 가질 수 있고, 특정 워크로드의 병목을 위해 전체 시스템을 동일하게 희생시키지 않아도 된다.

반면 한계도 명확하다. 저장소가 다양해질수록 운영 도구도 다양해지고, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성은 더 이상 하나의 [로컬 트랜잭션](/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)으로 끝나지 않는다. 따라서 이벤트 재처리, 중복 처리, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보, 관측성 같은 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 문제를 함께 해결해야 한다.

결론적으로 [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)는 "DB를 많이 쓰는 아키텍처"가 아니라, <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 경계와 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 특성에 맞춰 저장소를 책임 있게 분화하는 아키텍처</strong>다. 핵심은 화려한 기술 조합이 아니라, 어디에 어떤 저장 모델이 가장 자연스러운지를 설명할 수 있는가에 있다.

- **📢 섹션 요약 비유**: 좋은 주방은 냄비와 프라이팬과 오븐을 적절히 나눠 쓰지만, 무엇을 언제 쓸지 모르면 오히려 더 혼란스러워진다. [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)도 도구보다 조리 계획이 먼저다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/) | [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)의 기본 전제 |
| 최종적 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Eventual Consistency](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)의 기본 가정 |
| [사가 패턴](/studynote/12_it_management/05_security_compliance/305_saga/) ([Saga](/studynote/12_it_management/05_security_compliance/305_saga/)) | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 비즈니스 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 보상 방식 |
| [트랜잭셔널 아웃박스](/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/) | [로컬 트랜잭션](/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)과 이벤트 발행을 안전하게 연결 |
| [변경 데이터 캡처](/studynote/12_it_management/05_security_compliance/218_cdc_change_data_capture/) ([CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/), [Change Data Capture](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변경을 다른 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 전파하는 방식 |
| [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) | [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 모델과 읽기 모델 분리를 통해 저장소 특화를 강화 |
| 관측성 ([Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)) | 다중 저장소 운영의 필수 관리 기반 |

### 📈 관련 키워드 및 발전 흐름도

```text
Monolithic shared database
    |
    v
Service boundary and data ownership
    |
    v
Database per Service
    |
    v
Fit-for-purpose store selection
    |
    v
Event / Outbox / Saga based integration
```

이 흐름은 단일 공유 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)에서 출발해, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유권을 명확히 하면서 목적 적합형 저장소 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 발전하는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 국은 냄비에 끓이고, 빵은 오븐에 굽고, 샐러드는 그릇에 담는 게 더 잘 어울려요.
2. [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 음식처럼 성격에 맞는 그릇을 따로 고르는 생각이에요.
3. 하지만 그릇만 많고 정리 규칙이 없으면 부엌이 더 어지러워지니까 조심해야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 172 / 482

<- **이전**: [171. 폴백 (Fallback) 회복탄력성 패턴](/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/)
**다음**: [173. 데이터베이스 퍼 서비스 (Database per Service)](/studynote/07_enterprise_systems/03_eai_esb_msa/173_database_per_service/) ->

---
