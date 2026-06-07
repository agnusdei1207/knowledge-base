---
title: "Database per Service"
date: "2026-05-06"
tags:
  - "studynote-enterprise-systems"
weight: 173
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/) ([Database per Service](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/))는 [마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), [Microservices Architecture](/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) 에서 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 자기 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소의 소유권과 변경 책임을 독점하는 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 경계 패턴</strong>이다.
> 2. **가치**: 다른 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)를 직접 조회하지 못하게 막아야 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 독립 배포, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화, 장애 격리가 실제로 가능해진다.
> 3. **판단 포인트**: 이득의 대가로 교차 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 조회와 [분산 트랜잭션](/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/)이 어려워지므로, 응용 프로그래밍 인터페이스 ([API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [Application Programming Interface](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)), 이벤트, [사가 패턴](/studynote/12_it_management/05_security_compliance/305_saga/) 같은 보완 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 함께 준비되어야 한다.

---

## Ⅰ. 개요 및 필요성

[데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/)는 "[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 나눴다면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 함께 나눠 소유권을 명확히 하자"는 원칙이다. 핵심은 단순히 [데이터베이스 인스턴스](/studynote/05_database/01_db_architecture_relational/058_database_instance_architecture/)를 여러 개 두는 것이 아니라, <strong>각 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>의 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 변경 규칙을 오직 그 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>만 책임지게 만드는 것</strong>이다.

이 원칙이 필요한 이유는 공유 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)가 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계를 쉽게 무너뜨리기 때문이다. 주문 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 결제 테이블을 직접 조인하고, 배송 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 회원 테이블을 몰래 읽기 시작하면 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 분리돼 보여도 실제로는 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)에 묶인 [분산 모놀리스](/studynote/04_software_engineering/11_testing_validation/929_distributed_monolith_antipattern/)가 된다. 한 팀의 컬럼 변경이나 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 변경이 다른 팀의 장애로 이어지면, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 분리의 이점은 거의 사라진다.

따라서 [데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/)는 MSA의 선택 사항이라기보다, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 자율성을 실질적으로 보장하기 위한 통제 장치에 가깝다. 물리적으로 서로 다른 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)를 둘 수도 있고, 같은 엔진 안에서 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)를 분리할 수도 있다. 중요한 것은 저장 위치보다 <strong>직접 접근 금지와 소유권 계약</strong>이다.

이 그림은 공유 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)와 [데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/)의 차이를 구조적으로 보여 준다.

```text
+--------------------------------------------------------------------+
|              Shared database vs service-owned data                 |
+--------------------------------------------------------------------+
| shared database                                                    |
| Order Svc ---+                                                     |
| Payment Svc -+--> one schema, cross-service joins                  |
| Shipping Svc +                                                     |
|                                                                    |
| database per service                                               |
| Order Svc   -> Order Database                                      |
| Payment Svc -> Payment Database                                    |
| Shipping Svc-> Shipping Database                                   |
| service-to-service access goes through API or events               |
+--------------------------------------------------------------------+
```

즉 [데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/)의 본질은 저장소 개수보다 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 누구에게 직접 열어 줄 것인가</strong>를 명확히 끊는 데 있다.

- **📢 섹션 요약 비유**: 각 방 주인이 자기 서랍을 직접 관리하고, 다른 사람은 허락 없이 열지 못하게 하는 것과 같다. 방문은 나뉘어 있는데 서랍을 모두 같이 쓰면 결국 한집살이와 다를 바가 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/)가 제대로 작동하려면 네 가지 원리가 필요하다. <strong>소유권, <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/">로컬 트랜잭션</a>, 계약 기반 통신, 읽기 모델 분리</strong>다. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 자기 저장소 안에서만 강한 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 보장하고, 다른 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와의 연계는 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출이나 이벤트로 푼다.

| 요소 | 역할 | 핵심 질문 | 대표 기법 |
| :--- | :--- | :--- | :--- |
| [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 소유 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) | 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 진실 원천 (Source of Truth) | 누가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 바꿀 권한을 가지는가? | 전용 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/), 전용 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) |
| [로컬 트랜잭션](/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 내부 정합성 보장 | 어디까지 한 번에 커밋할 수 있는가? | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 [데이터베이스 관리 시스템](/studynote/05_database/01_db_architecture_relational/003_dbms_database_management_system/) (RDBMS, Relational [Database](/studynote/05_database/04_transactions_concurrency/501_database/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/) System) [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) |
| 계약 기반 통신 | 타 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 접근하는 공식 경로 | 직접 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 질의 대신 무엇을 호출할 것인가? | 동기 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 비동기 이벤트 |
| 읽기 모델 분리 | 교차 조회 요구 대응 | 여러 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 어디서 합칠 것인가? | [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Composition, [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) ([Command Query Responsibility Segregation](/studynote/06_ict_convergence/03_cloud_infrastructure/250_cqrs_command_query_responsibility_segregation_pattern/)) |

실무 흐름은 보통 이렇다. 주문 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 자기 Order [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)에 주문을 커밋하고, 그 결과를 이벤트로 발행한다. 결제 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 이 이벤트를 받아 자기 Payment [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)를 갱신한다. 이 과정에서 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 자기 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 안에서는 [원자성](/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/)을 지키지만, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 전체 흐름은 최종적 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Eventual Consistency](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) 을 전제로 움직인다.

아래 그림은 [데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/)에서 직접 조인이 사라지고, 계약 기반 연계가 등장하는 이유를 보여 준다.

```text
+--------------------------------------------------------------------+
|             Database per Service integration pattern               |
+--------------------------------------------------------------------+
| Order Service   -> Order Database   -> outbox event ----------+   |
| Payment Service -> Payment Database <- subscribes / API call <-+   |
|                                                                    |
| rule: no direct database query into another service database       |
| cross-service views are built by API composition or read models    |
+--------------------------------------------------------------------+
```

이 구조에서 중요한 것은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복을 무조건 나쁘다고 보지 않는 태도다. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 조회를 위해 읽기 전용 사본이나 조회 모델을 따로 유지할 수 있다. 대신 그 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)와 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 책임을 명시적으로 드러내야 한다. 감춰진 조인보다 드러난 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)가 더 관리 가능하다는 것이 MSA의 관점이다.

- **📢 섹션 요약 비유**: 각 가게가 자기 장부를 직접 관리하고, 필요한 숫자는 전표나 영수증으로 주고받는 구조와 같다. 남의 장부를 몰래 펴 보는 것보다 번거롭지만, 책임이 훨씬 분명해진다.

---

## Ⅲ. 비교 및 연결

[데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/)는 종종 공유 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)나 [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)와 혼동된다. 하지만 셋은 초점이 다르다.

| 구분 | 공유 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) | [데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/) | [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/) |
| :--- | :--- | :--- | :--- |
| 핵심 목적 | 단순한 통합 조회와 강한 전역 정합성 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 자율성과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유권 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 최적 저장 모델 선택 |
| [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계 | 약함 | 강함 | 강함 |
| 직접 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 조인 | 쉬움 | 원칙적으로 금지 | 원칙적으로 금지 |
| [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 방식 | 단일 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) [로컬 트랜잭션](/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 [로컬 트랜잭션](/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 [로컬 트랜잭션](/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/) |
| 주요 부담 | 강결합, 배포 종속 | 조회/[트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 재설계 | 운영 기술 다양성 증가 |

즉 [데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/)는 **소유권 규칙**, [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)는 <strong>저장소 선택 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>이다. [데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/) 없이 [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)를 말하면 저장소만 여러 개고 경계는 흐린 상태가 되기 쉽다.

또한 이 패턴은 [사가 패턴](/studynote/12_it_management/05_security_compliance/305_saga/) ([Saga Pattern](/studynote/12_it_management/05_security_compliance/948_saga_pattern/)), [명령-조회 책임 분리](/studynote/11_design_supervision/06_exam_summary/368_cqrs/) ([CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/), [Command Query Responsibility Segregation](/studynote/06_ict_convergence/03_cloud_infrastructure/250_cqrs_command_query_responsibility_segregation_pattern/)), [트랜잭셔널 아웃박스](/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/), [변경 데이터 캡처](/studynote/12_it_management/05_security_compliance/218_cdc_change_data_capture/) ([CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/), [Change Data Capture](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)) 와 자주 연결된다. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 직접 조인과 전역 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 버리는 대신, <strong>계약과 이벤트로 정합성을 관리하는 패턴군</strong>이 함께 필요하기 때문이다.

결국 [데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/)는 "[데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)를 분리했다"는 인프라 문장이 아니라, <strong>통합 방식을 조인 중심에서 계약 중심으로 바꿨다</strong>는 아키텍처 선언에 가깝다.

- **📢 섹션 요약 비유**: 모두가 같은 냉장고를 쓰면 음식 찾기는 쉽지만 누가 무엇을 책임지는지 헷갈린다. 각자 냉장고를 따로 쓰면 규칙은 번거로워져도 자기 음식에 대한 책임은 훨씬 선명해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/)를 채택할지 판단할 때는 "[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 몇 개로 쪼갤까"보다 <strong><a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 경계가 정말 독립적으로 운영될 수 있는가</strong>를 먼저 봐야 한다. 주문, 결제, 배송처럼 책임과 변경 주기가 다르고 팀도 분리되어 있다면 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 소유권 분리가 큰 이점을 준다. 반대로 아직 기능 경계가 모호하고, 대부분의 업무가 한 번의 복합 조회로만 성립한다면 너무 이른 분리는 오히려 개발 속도를 늦출 수 있다.

전자상거래를 예로 들면, 주문 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)은 Order [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)에서 끝내고 결제 승인 결과는 Payment [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 가 따로 확정하는 구조가 자연스럽다. 이때 "주문 + 결제 + 배송 현황" 조회 화면은 [백엔드 포 프론트엔드](/studynote/04_software_engineering/05_devops_ci_cd/309_bff_backend_for_frontend_pattern/) ([BFF](/studynote/04_software_engineering/11_testing_validation/935_bff_backend_for_frontend/), [Backend for Frontend](/studynote/04_software_engineering/11_testing_validation/935_bff_backend_for_frontend/)) 나 조회 전용 모델이 조합해야 한다. 즉 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 경계와 읽기 경계를 분리하는 사고가 필요하다.

### 기술사 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유권이 조직적으로 합의되었는가?
2. 다른 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 직접 접근을 금지할 수 있는가?
3. 교차 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 조회를 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Composition, [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) 읽기 모델, [데이터 마트](/studynote/14_data_engineering/05_exam_keywords/209_data_mart_kimball_star_schema/) 중 무엇으로 풀지 정했는가?
4. 전역 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 대신 [사가](/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/), 보상 처리, 재처리 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 수용할 수 있는가?
5. 운영팀이 여러 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링, 보안 패치를 감당할 수 있는가?

### 자주 나오는 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 나눴지만 서로의 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)에 읽기 계정을 열어 두는 경우
- 테이블 단위로 과도하게 쪼개어 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)보다 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 개수가 더 빨리 늘어나는 경우
- 조회 편의를 이유로 교차 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 조인을 계속 남겨 두는 경우
- 읽기 모델 설계 없이 모든 화면을 동기 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 연쇄 호출로만 해결하려는 경우

기술사적 판단의 핵심은 분리 그 자체가 아니라 <strong>분리 이후의 운영 모델을 감당할 준비가 되었는가</strong>다. 이 준비가 없으면 [Database per Service](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/) 는 독립성을 주기보다 복잡도만 늘릴 수 있다.

- **📢 섹션 요약 비유**: 각자 통장을 따로 쓰면 돈 관리는 명확해지지만, 가족 전체 가계부를 보려면 따로 정리표를 만들어야 한다. 통장만 나눈다고 회계가 끝나는 것은 아니다.

---

## Ⅴ. 기대효과 및 결론

[데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/)가 잘 정착하면 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 자율성, 배포 독립성, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화 속도, 장애 격리가 좋아진다. 한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 저장소 변경이 다른 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 즉각적인 수정으로 번지지 않으므로 팀 단위 책임도 선명해진다.

반면 비용도 분명하다. 교차 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 조회는 더 이상 한 번의 조인으로 끝나지 않고, [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 비즈니스 프로세스는 강한 전역 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)보다 보상과 재처리 중심으로 설계해야 한다. 따라서 이 패턴은 "쉬운 구조"가 아니라 <strong>독립성을 얻기 위해 복잡도를 의식적으로 재배치하는 구조</strong>다.

결론적으로 [데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/)는 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)의 부속품이 아니라, [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)가 진짜로 독립적이기 위한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 측면의 최소 조건이다. 기억해야 할 핵심은 하나다. <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 경계는 <a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a> 에만 있는 것이 아니라 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 소유권에도 있어야 한다.</strong>

- **📢 섹션 요약 비유**: 진짜 독립생활은 방만 따로 쓰는 것이 아니라 지갑과 장부도 따로 관리하는 데서 시작된다. [데이터베이스 퍼 서비스](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/)는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 세계의 그런 독립생활 규칙이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), [Microservices Architecture](/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) | [Database per Service](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/) 가 주로 적용되는 기본 구조 |
| [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Composition | 여러 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 조회 결과를 상위 계층에서 조합하는 방식 |
| [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) | [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)와 읽기 모델을 분리해 조회 부담을 줄이는 패턴 |
| [사가 패턴](/studynote/12_it_management/05_security_compliance/305_saga/) ([Saga Pattern](/studynote/12_it_management/05_security_compliance/948_saga_pattern/)) | 전역 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 대신 보상 흐름으로 정합성을 관리 |
| [트랜잭셔널 아웃박스](/studynote/04_software_engineering/05_devops_ci_cd/314_transactional_outbox_pattern/) | [로컬 트랜잭션](/studynote/04_software_engineering/09_cloud_native_ai_architecture/548_local_vs_distributed_transactions/)과 이벤트 발행을 안전하게 연결 |
| [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) ([Change Data Capture](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 반영을 위한 비동기 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 기법 |
| [폴리글랏 퍼시스턴스](/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/) | [Database per Service](/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/) 위에서 확장되는 저장소 다변화 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |

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
API / event based integration
          |
          v
Saga, CQRS, read-model driven microservices
```

이 흐름은 "공유 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 중심 사고 -> [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계 명확화 -> [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유권 분리 -> 계약 기반 연계"로 발전하는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 형, 동생, 누나가 각자 자기 공책에만 자기 비밀과 숙제를 적는 거예요.
2. 다른 사람이 내용이 필요하면 공책을 몰래 보지 않고 물어보거나 쪽지를 받아요.
3. 그래서 한 사람이 공책을 고쳐도 다른 사람 공책이 갑자기 망가지지 않아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 173 / 482

<- **이전**: [172. 폴리글랏 퍼시스턴스 (Polyglot Persistence)](/studynote/07_enterprise_systems/03_eai_esb_msa/172_polyglot_persistence/)
**다음**: [174. 분산 트랜잭션 한계 및 2PC (Two-Phase Commit) 배제 이유 - 블로킹 오버헤드](/studynote/07_enterprise_systems/03_eai_esb_msa/174_distributed_transaction_2pc_limit/) ->

---
