---
title: "179. Cqrs Pattern Command Query"
date: "2026-05-06"
tags:
  - "studynote-enterprise"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) ([Command Query Responsibility Segregation](/studynote/06_ict_convergence/03_cloud_infrastructure/250_cqrs_command_query_responsibility_segregation_pattern/))는 상태를 바꾸는 명령 모델과 화면·검색을 위한 조회 모델을 분리해, 하나의 객체 모델에 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 규칙과 읽기 최적화를 동시에 짊어지게 하지 않는 설계 패턴이다.
> 2. **가치**: [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 측은 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)과 비즈니스 불변식에 집중하고, 읽기 측은 화면별 투영 모델과 검색 구조에 집중할 수 있어, 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 부하가 크게 다른 시스템에서 확장성과 단순성을 함께 얻는다.
> 3. **판단 포인트**: CQRS의 대가는 복잡도다. 읽기 모델 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/), 최종 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Eventual Consistency](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)), 재처리, [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링까지 감당할 가치가 있을 때만 채택해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 CRUD (Create, Read, Update, Delete) 기반 설계는 하나의 엔티티 모델과 하나의 저장소로 읽기와 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 함께 처리한다. 단순 업무 시스템에서는 이 방식이 가장 직관적이지만, 읽기와 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)의 성격이 크게 달라지는 순간 한 모델에 서로 다른 요구사항이 충돌하기 시작한다. [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 측은 [무결성](/studynote/09_security/01_intro_principles/003_integrity/), [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/), [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 규칙이 중요하고, 읽기 측은 조인, 검색, 정렬, 화면 맞춤형 집계가 중요하기 때문이다.

[마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), [Microservices Architecture](/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) 에서는 이 충돌이 더 커진다. 주문, 회원, 상품 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)되면 과거처럼 하나의 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)에서 복잡한 조인을 수행하기 어렵다. 게이트웨이에서 여러 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 호출해 결과를 합칠 수도 있지만, [네트워크 지연](/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/)이 누적되고 장애 전파가 쉬워지며, 화면별 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조를 만들기 위해 애플리케이션 코드가 지나치게 복잡해진다.

```text
+--------------------------------------------------------------------+
| Single model overload                                              |
+--------------------------------------------------------------------+
| same domain model + same schema + same database                    |
|   +- Command needs transaction, validation, invariant              |
|   +- Query needs join, search, pagination, denormalized view       |
|                                                                    |
| 결과: 하나의 모델이 두 종류의 요구를 모두 억지로 떠안음              |
+--------------------------------------------------------------------+
```

CQRS는 바로 이 지점에서 출발한다. "같은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다룬다"와 "같은 모델로 다뤄야 한다"는 가정을 분리하는 것이다. 즉 업무 규칙을 지키는 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 모델과, 사용자가 빨리 읽을 수 있게 재구성한 조회 모델을 나누어 각자 다른 목표에 최적화한다.

- **📢 섹션 요약 비유**: 요리사가 주방에서 쓰는 조리대와 손님에게 보여 주는 뷔페 진열대는 같은 음식을 다루지만 모양과 목적이 다르다. CQRS는 그 둘을 억지로 같은 형태로 만들지 않는 생각이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) 아키텍처는 보통 명령 측, 이벤트 전달 계층, 조회 측의 세 부분으로 나뉜다. 명령 측은 주문 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 결제 승인, 재고 차감처럼 상태를 바꾸는 작업을 처리하며, 보통 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)된 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 저장소와 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 사용한다. 조회 측은 사용자 화면이나 검색 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 에 필요한 형태로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 미리 투영해 두고, 문서 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/), 검색 엔진, [키-값 저장소](/studynote/14_data_engineering/01_infrastructure/036_key_value/) 같은 읽기 친화형 구조를 선택할 수 있다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| [Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) Handler | 명령 수신과 유효성 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 중복 명령 처리, 권한, [입력 검증](/studynote/09_security/uncategorized/1034_input_validation/) |
| Write Model / [Aggregate](/studynote/04_software_engineering/04_testing_quality/222_aggregate_ddd_transaction_consistency/) | 비즈니스 규칙과 상태 변경 | 불변식 보장, [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 경계 명확화 |
| Write Store | 시스템의 기준 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 | 보통 [OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) (Online [Transaction](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing) 최적화 |
| Outbox / [Event Bus](/studynote/04_software_engineering/11_testing_validation/931_event_bus_stream_processing/) | 변경 사실 전달 | [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/), 순서, 재시도, 장애 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| Projector | 이벤트를 읽기 모델로 변환 | 재처리 가능성, [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 |
| Read Model | 화면·검색용 투영 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 비정규화, 조회별 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 최적화 |
| Query [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | 읽기 전용 응답 제공 | 낮은 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간, [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)별 응답 구조 |

아래 그림은 CQRS의 전형적인 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름을 요약한다.

```text
+--------------------------------------------------------------------+
| CQRS flow                                                          |
+--------------------------------------------------------------------+
| User command                                                       |
|   |                                                                |
|   v                                                                |
| Command handler --> Write model --> Write store                      |
|                                 |                                  |
|                                 +- outbox / event                  |
|                                            |                       |
|                                            v                       |
|                                      projector / consumer          |
|                                            |                       |
|                                            v                       |
|                                      Read model store              |
|                                            |                       |
| User query  -------------------------------+                       |
|   +- Query API reads optimized projection                          |
+--------------------------------------------------------------------+
```

이 구조에서 중요한 것은 읽기 저장소가 단순 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본이 아니라는 점이다. 조회 모델은 "주문 상세 화면", "고객별 최근 주문 목록", "검색 자동완성"처럼 <strong>사용 사례별로 미리 가공된 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 뷰</strong>가 될 수 있다. 그래서 CQRS는 종종 머티리얼라이즈드 뷰 (Materialized [View](/studynote/05_database/03_relational_model/151_sql_view_virtual_table/)) 나 이벤트 기반 프로젝션과 함께 설명된다.

물론 이 구조는 즉시 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 포기하는 대가를 요구한다. 명령이 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 저장소에 반영된 직후 조회 모델로 전파되기까지는 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 생길 수 있다. 따라서 CQRS의 핵심 원리는 "읽기 모델이 순간적으로 늦을 수 있음"을 받아들이되, 그 대신 읽기와 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 각자 가장 적합한 구조로 분리하는 데 있다.

- **📢 섹션 요약 비유**: 주방에서 요리가 완성되면, 바로 손님용 진열대에 예쁘게 담아 놓는 과정이 따로 있는 셈이다. 조리는 주방 규칙을 따르고, 진열은 손님이 보기 편한 규칙을 따른다.

---

## Ⅲ. 비교 및 연결

CQRS를 제대로 이해하려면 읽기 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본과 [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) ([Event Sourcing](/studynote/12_it_management/05_security_compliance/307_event_sourcing/)) 과 구분해야 한다. 읽기 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본은 보통 같은 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)를 다른 노드에 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)해 읽기 부하를 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)하는 구조이고, CQRS는 애초에 읽기 모델 자체를 다르게 설계한다. [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)은 변경 이벤트 자체를 진실 원천으로 삼는 패턴이고, CQRS는 그것 없이도 적용 가능하다.

| 방식 | 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 모델 | 저장 원천 | 장점 | 한계 |
| :--- | :--- | :--- | :--- | :--- |
| CRUD 단일 모델 | 동일 | 동일 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) | 단순함, 학습 비용 낮음 | 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 요구 충돌 시 비효율 |
| 읽기 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본 (Read Replica) | 동일 | 동일 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | 읽기 부하 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) | 조회 구조 자체는 안 바뀜 |
| [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) | 분리 | [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 저장소 + 조회 저장소 | 사용 사례별 최적화, 독립 확장 | [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)와 운영 복잡도 증가 |
| [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) + [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) | 분리 | 이벤트 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | 재생·[감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적에 강함 | 설계 난이도와 운영 부담 큼 |

또한 CQRS는 [트랜잭셔널 아웃박스](/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/) ([Transactional Outbox](/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/)), [사가](/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/) ([Saga](/studynote/12_it_management/05_security_compliance/305_saga/)), 이벤트 브로커와 자주 연결된다. [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 측의 변경 사실을 안정적으로 조회 모델이나 다른 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 퍼뜨리려면 Outbox 같은 패턴이 필요하고, 여러 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 걸친 장기 업무 흐름은 [Saga](/studynote/12_it_management/05_security_compliance/305_saga/) 로 이어질 수 있다. 즉 CQRS는 단독 기술이라기보다 <strong>이벤트 기반 <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 시스템의 한 축</strong>으로 이해하는 편이 정확하다.

실무에서 자주 생기는 오해는 "[데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)를 둘로 나누면 다 [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/)" 라는 생각이다. 하지만 읽기와 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)에 같은 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)를 그대로 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)해 놓았다면 그건 대부분 읽기 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)에 가깝다. CQRS의 본질은 DB 개수보다 <strong>모델 책임의 분리</strong>에 있다.

- **📢 섹션 요약 비유**: 같은 책을 다른 선반에 한 권 더 두는 것은 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본이고, 어린이용 요약본을 따로 만드는 것은 CQRS에 가깝다. 둘 다 읽기 편하게 만들지만 방식과 목적이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

CQRS는 읽기와 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)의 비대칭이 큰 곳에서 빛난다. 예를 들어 주문 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)은 초당 수십 건인데, 주문 조회와 검색은 초당 수천 건이고 화면마다 요구하는 조인 구조가 다르다면, 조회 모델을 별도로 두는 편이 훨씬 단순하다. 반대로 단순한 사내 관리 시스템처럼 화면 수가 적고 읽기·[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 부하가 모두 크지 않다면, CQRS는 얻는 것보다 운영 부담이 더 클 수 있다.

또한 읽기 모델의 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 업무가 감수할 수 있는지도 중요하다. 주문 직후 조회 화면이 200밀리초 정도 늦게 갱신되는 것은 허용할 수 있지만, 금융 잔액처럼 즉시 반영이 절대적으로 중요한 화면은 별도 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 필요하다. 이때는 명령 응답 자체에 최신 상태를 함께 담거나, 일부 조회만 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 측에서 직접 제공하는 혼합 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 검토할 수 있다.

### 기술사 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 읽기 트래픽과 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 트래픽의 규모·패턴이 실제로 많이 다른가?
2. 조회 화면별로 필요한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 형태가 크게 달라 별도 투영 모델 가치가 큰가?
3. 읽기 모델 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 업무적으로 허용할 수 있는가?
4. 이벤트 재처리, 프로젝션 재구축, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 변경 절차가 준비되어 있는가?
5. 프로젝터와 소비자가 멱등하게 동작하고, 순서 문제를 감당할 수 있는가?
6. 읽기 모델 장애, 적체, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 관측할 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 체계가 있는가?

### 자주 나오는 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 단순 CRUD 시스템에도 유행처럼 CQRS를 도입해 팀 복잡도만 늘리는 경우
- [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 측의 비즈니스 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)된 읽기 모델에 의존하는 경우
- 조회 모델을 화면별로 나누지 않고, 다시 범용 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)처럼 만들어 복잡성을 되살리는 경우
- 프로젝션 재생이나 백필 (Backfill) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 없이 실시간 이벤트만 믿는 경우

실무 시나리오로 보면 더 분명하다. 전자상거래 시스템에서 주문 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)은 주문 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 처리하고, 고객 주문 목록 화면은 주문·결제·배송 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 합친 별도 조회 모델에서 읽는 구조가 CQRS에 잘 맞는다. 이때 조회 모델은 고객번호 기준 문서 구조나 검색 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)로 최적화할 수 있다. 반면 단일 팀이 운영하는 간단한 게시판 시스템에 같은 구조를 강제로 넣으면, 코드보다 운영 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 관리가 더 어려워질 수 있다.

- **📢 섹션 요약 비유**: 작은 가게 장부는 한 권이면 충분하지만, 대형 마트는 재고 관리 장부와 손님 안내 전광판을 따로 운영하는 편이 훨씬 효율적이다.

---

## Ⅴ. 기대효과 및 결론

CQRS를 올바르게 적용하면 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 측은 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 규칙과 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 단단하게 유지하고, 읽기 측은 화면과 검색 요구에 맞게 자유롭게 최적화할 수 있다. 그 결과 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 독립 확장, 단순한 조회 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 화면별 비정규화, 검색 엔진 결합, 장애 격리 같은 효과를 기대할 수 있다. 특히 [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경에서는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계를 지키면서도 복합 조회를 빠르게 제공하는 방법으로 큰 의미가 있다.

하지만 그 이면에는 저장소 [이중화](/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복, 최종 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 처리, 이벤트 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 운영, 재처리 비용이 따라온다. 즉 CQRS는 "더 멋진 아키텍처"가 아니라, <strong>읽기/<a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 불균형을 다른 복잡도로 교환하는 선택</strong>이다. 그래서 도입 판단은 기술 유행보다, 읽기 모델 분리로 얻는 사업적 가치가 충분한지를 기준으로 해야 한다.

결론적으로 CQRS를 기억할 때 가장 중요한 문장은 이것이다. **같은 사실을 다루더라도, 상태를 바꾸는 모델과 보여 주기 위한 모델은 같을 필요가 없다.** 이 관점을 이해하면 CQRS는 단순한 패턴 이름이 아니라, 대규모 시스템에서 책임을 분리하는 설계 원칙으로 남는다.

- **📢 섹션 요약 비유**: 주방 레시피 노트와 손님 메뉴판은 같은 음식을 말하지만, 쓰는 사람과 보는 사람이 다르니 당연히 모양도 달라야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) Model | 상태 변경과 비즈니스 불변식을 담당하는 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 측 모델 |
| Query Model | 화면·검색·통계를 위해 최적화된 읽기 측 모델 |
| 프로젝션 (Projection) | 이벤트나 변경 사항을 읽기 모델로 반영하는 과정 |
| 머티리얼라이즈드 뷰 (Materialized [View](/studynote/05_database/03_relational_model/151_sql_view_virtual_table/)) | 조회용으로 미리 계산해 둔 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조 |
| 최종 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Eventual Consistency](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) | [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)와 읽기 모델 간 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 설명하는 핵심 개념 |
| [트랜잭셔널 아웃박스](/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/) ([Transactional Outbox](/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/)) | 변경 사실을 안전하게 외부로 전달하기 위한 보조 패턴 |
| 읽기 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본 (Read Replica) | CQRS와 혼동되지만 동일 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)에 가까운 구조 |
| [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) ([Event Sourcing](/studynote/12_it_management/05_security_compliance/307_event_sourcing/)) | CQRS와 결합 가능하지만 별도인 저장 모델 패턴 |

### 📈 관련 키워드 및 발전 흐름도

```text
사용자 명령
    |
    v
Command Handler + Write Model
    |
    v
Write Store + Outbox/Event
    |
    v
Projector / Consumer
    |
    v
Read Model (projection)
    |
    v
Query API · 검색 · 화면 응답
```

이 흐름도는 "명령 처리 -> 변경 사실 전달 -> 조회 모델 투영 -> 읽기 응답"이라는 CQRS의 핵심 작동 순서를 요약한다.

### 👶 어린이를 위한 3줄 비유 설명

1. 가게에서 물건을 채워 넣는 창고 장부와 손님이 보는 진열판은 같은 내용을 다루지만 쓰임새가 달라요.
2. 그래서 물건을 바꾸는 장부는 정확하게 쓰고, 손님이 보는 진열판은 보기 쉽게 따로 만들어요.
3. 진열판이 조금 늦게 바뀔 수는 있지만, 손님은 더 빨리 찾고 창고는 더 안전하게 관리할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 179 / 482

<- **이전**: [178. 트랜잭셔널 아웃박스 (Transactional Outbox) 패턴 - DB 커밋과 메시지 브로커 이벤트 발행의 원자성(Atomicity)](/studynote/07_enterprise_systems/03_eai_esb_msa/178_transactional_outbox_pattern_cdc/)
**다음**: [180. 이벤트 소싱 (Event Sourcing) - 상태 변경 이벤트를 불변 로그 (Append-Only Log) 로 저장](/studynote/07_enterprise_systems/03_eai_esb_msa/180_event_sourcing_immutable_log/) ->

---
