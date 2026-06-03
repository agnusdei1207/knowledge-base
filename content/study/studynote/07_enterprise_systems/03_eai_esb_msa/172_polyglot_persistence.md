---
title: 172. 폴리글랏 퍼시스턴스 (Polyglot Persistence)
date: '2026-05-06'
tags:
- studynote-enterprise
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[308_pgvector|폴리글랏 퍼시스턴스]] ([[132_polyglot_persistence|Polyglot Persistence]])는 모든 [[090_service_kubernetes_network_load_balancing|서비스]]를 하나의 [[002_database_definition|데이터베이스]]에 맞추는 대신, 각 [[090_service_kubernetes_network_load_balancing|서비스]]가 자신의 [[064_relation_domain|도메인]] 특성과 접근 패턴에 맞는 저장소를 선택하는 아키텍처 [[268_strategy_pattern|전략]]이다.
> 2. **가치**: 주문은 [[083_relationship_in_er_model|관계]]형 [[003_dbms_database_management_system|데이터베이스 관리 시스템]] (RDBMS, Relational [[501_database|Database]] [[372_management|Management]] System), [[160_session_controlling_terminal|세션]]은 [[036_key_value|키-값 저장소]], 추천은 [[039_graph_db|그래프 데이터베이스]]처럼 목적에 맞는 저장 기술을 쓰면 [[282_performance_tactics|성능]]과 개발 생산성을 동시에 높일 수 있다.
> 3. **판단 포인트**: 진짜 전제는 기술 다양성이 아니라 [[090_service_kubernetes_network_load_balancing|서비스]] 경계, [[001_dikw_pyramid|데이터]] 소유권, 운영 역량, [[136_variance|분산]] 정합성 설계이며, 이 준비 없이 DB만 늘리면 최적화가 아니라 운영 복잡도만 폭증한다.

---

## Ⅰ. 개요 및 필요성

[[308_pgvector|폴리글랏 퍼시스턴스]]는 여러 저장 기술을 무작정 섞어 쓰는 유행어가 아니다. 정확히는 **[[090_service_kubernetes_network_load_balancing|서비스]]별 [[001_dikw_pyramid|데이터]] 특성과 비즈니스 요구에 따라 서로 다른 저장 모델을 선택하는 설계 원칙**이다. 같은 시스템 안에도 강한 [[191_transaction_concept_states|트랜잭션]]이 필요한 주문 [[001_dikw_pyramid|데이터]], [[005_schema|스키마]] 변화가 잦은 상품 [[082_attribute_types_er_model|속성]] [[001_dikw_pyramid|데이터]], 초저지연이 필요한 [[160_session_controlling_terminal|세션]] [[001_dikw_pyramid|데이터]], [[083_relationship_in_er_model|관계]] 탐색이 중요한 추천 [[001_dikw_pyramid|데이터]]가 공존한다.

단일 [[002_database_definition|데이터베이스]] [[268_strategy_pattern|전략]]은 운영과 교육 측면에서 단순하지만, 모든 [[001_dikw_pyramid|데이터]]를 하나의 모델에 억지로 맞추는 순간 문제가 생긴다. 예를 들어 주문과 결제는 ACID ([[193_atomicity_all_or_nothing|Atomicity]], [[194_consistency_database_integrity|Consistency]], [[195_isolation_concurrency_control|Isolation]], [[196_durability_permanent_storage|Durability]]) 보장이 중요하지만, 상품 [[394_catalog_metadata|카탈로그]]는 [[082_attribute_types_er_model|속성]] 구조가 자주 바뀌고, 추천은 연결 [[083_relationship_in_er_model|관계]] 탐색이 핵심이다. 하나의 RDBMS로 모두 해결하려 하면 과도한 조인, 복잡한 [[343_json|JSON]] 컬럼, 비효율적인 [[154_database_index_b_tree_search_optimization|인덱스]] 설계 같은 우회로가 늘어난다.

[[213_msa_microservices_architecture|마이크로서비스 아키텍처]] ([[619_msa_traffic_hardware|MSA]], [[122_msa_microservices_architecture|Microservices Architecture]]) 가 확산되며 이 [[268_strategy_pattern|전략]]이 더 중요해진 이유도 여기에 있다. [[090_service_kubernetes_network_load_balancing|서비스]]가 독립 배포와 독립 확장을 지향한다면, 저장소도 그 [[090_service_kubernetes_network_load_balancing|서비스]]의 요구에 맞게 독립적이어야 한다. 즉 [[308_pgvector|폴리글랏 퍼시스턴스]]는 기술 과시가 아니라 **[[064_relation_domain|도메인]]별 적합성 확보**를 위한 선택이다.

이 그림은 공유 DB [[268_strategy_pattern|전략]]과 [[308_pgvector|폴리글랏 퍼시스턴스]]의 차이를 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│              One shared store versus fit-for-purpose stores          │
├──────────────────────────────────────────────────────────────────────┤
│ shared DB : Order / Catalog / Session / Recommendation -> one RDBMS │
│                                                                      │
│ polyglot : Order -> RDBMS                                            │
│            Catalog -> document DB                                    │
│            Session -> key-value store                                │
│            Recommendation -> graph DB                                │
└──────────────────────────────────────────────────────────────────────┘
```

핵심은 저장소 수가 아니라 **[[014_data_model_components|데이터 모델]]과 접근 패턴의 부합성**이다. [[090_service_kubernetes_network_load_balancing|서비스]]의 문제를 저장소가 더 자연스럽게 표현할 수 있을 때 [[308_pgvector|폴리글랏 퍼시스턴스]]의 가치가 생긴다.

- **📢 섹션 요약 비유**: 모든 요리를 한 냄비로 만들 수는 있지만, 국물요리와 볶음요리와 빵 굽기를 같은 도구로 처리하면 맛도 효율도 떨어진다. [[308_pgvector|폴리글랏 퍼시스턴스]]는 요리에 맞는 조리도구를 고르는 일과 비슷하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[308_pgvector|폴리글랏 퍼시스턴스]]가 성립하려면 먼저 [[311_database_per_service_pattern|데이터베이스 퍼 서비스]] ([[311_database_per_service_pattern|Database per Service]]) 원칙이 필요하다. 각 [[090_service_kubernetes_network_load_balancing|서비스]]가 자기 저장소의 **소유권과 변경 책임**을 가져야 하며, 다른 [[090_service_kubernetes_network_load_balancing|서비스]]는 그 DB를 직접 조인하거나 갱신하지 않는다. 그래야 저장 기술을 독립적으로 바꿀 자유가 생긴다.

| [[064_relation_domain|도메인]]/워크로드 | [[001_dikw_pyramid|데이터]] 성격 | 자주 쓰는 저장소 | 선택 이유 |
| :--- | :--- | :--- | :--- |
| 주문·결제 | 강한 정합성, [[191_transaction_concept_states|트랜잭션]] 중심 | RDBMS | ACID, [[075_referential_integrity_foreign_key_cascade|참조 무결성]], 회계 처리 적합 |
| 상품 [[394_catalog_metadata|카탈로그]] | [[082_attribute_types_er_model|속성]] 구조 변화, 문서 단위 조회 | 문서 지향 [[002_database_definition|데이터베이스]] ([[037_document|Document]] [[501_database|Database]]) | 유연한 [[005_schema|스키마]]와 집계 문서 모델 |
| [[160_session_controlling_terminal|세션]]·장바구니 | 초저지연, 단순 키 접근 | [[036_key_value|키-값 저장소]] ([[036_key_value|Key-Value Store]]) | 빠른 읽기/[[289_cqrs_db|쓰기]], [[294_ttl_time_to_live_looping_prevention|TTL]] 처리 |
| 추천·[[083_relationship_in_er_model|관계]] 분석 | 연결 탐색, 다중 홉 [[083_relationship_in_er_model|관계]] | [[039_graph_db|그래프 데이터베이스]] ([[039_graph_db|Graph Database]]) | [[083_relationship_in_er_model|관계]] 질의와 경로 탐색 효율 |

하지만 저장소를 나누는 순간 정합성은 자동으로 따라오지 않는다. 주문 [[090_service_kubernetes_network_load_balancing|서비스]]의 상태가 바뀌면 배송 [[090_service_kubernetes_network_load_balancing|서비스]]나 분석 [[090_service_kubernetes_network_load_balancing|서비스]]도 이를 알아야 하므로, [[090_service_kubernetes_network_load_balancing|서비스]] 간 연계는 직접 SQL 조인이 아니라 이벤트, 응용 프로그래밍 인터페이스 ([[014_api_posix|API]]), [[218_cdc_change_data_capture|변경 데이터 캡처]] ([[217_cdc_binlog_change_capture_debezium|CDC]], [[217_cdc_binlog_change_capture_debezium|Change Data Capture]]), [[314_transactional_outbox_pattern|트랜잭셔널 아웃박스]] ([[314_transactional_outbox_pattern|Transactional Outbox]]) 같은 방식으로 풀어야 한다.

아래 구조는 [[308_pgvector|폴리글랏 퍼시스턴스]]가 "DB 여러 개"가 아니라 "[[090_service_kubernetes_network_load_balancing|서비스]] 소유 + 이벤트 연계"라는 점을 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│              Service-owned stores with event-based linkage           │
├──────────────────────────────────────────────────────────────────────┤
│ Order Service ----------> Order DB ----------> Outbox event          │
│ Catalog Service --------> Catalog DB --------> API / event           │
│ Recommendation Service -> Graph DB <--------- subscribed events      │
│                                                                      │
│ rule: no cross-service direct joins, integrate through contracts      │
└──────────────────────────────────────────────────────────────────────┘
```

즉 [[308_pgvector|폴리글랏 퍼시스턴스]]의 핵심 원리는 "자기 [[090_service_kubernetes_network_load_balancing|서비스]]의 진실 원천(Source of Truth)은 자기 저장소 안에 둔다"는 것이다. 다른 [[090_service_kubernetes_network_load_balancing|서비스]]는 그 진실을 API나 이벤트로 소비할 뿐이며, 그 과정에서 결국 최종적 [[194_consistency_database_integrity|일관성]] ([[650_eventual_consistency|Eventual Consistency]]) 을 받아들일 준비가 필요하다.

- **📢 섹션 요약 비유**: 각 부서가 자기 서류함을 책임지고, 다른 부서가 필요하면 공식 공문이나 전달 시스템으로 받아보는 구조가 [[308_pgvector|폴리글랏 퍼시스턴스]]다. 남의 서류함을 마음대로 열어보는 순간 독립성은 무너진다.

---

## Ⅲ. 비교 및 연결

[[308_pgvector|폴리글랏 퍼시스턴스]]를 이해하려면 "공유 [[002_database_definition|데이터베이스]]", "[[090_service_kubernetes_network_load_balancing|서비스]]별 DB이지만 같은 엔진", "[[090_service_kubernetes_network_load_balancing|서비스]]별 다른 엔진"을 구분해야 한다. 세 방식은 독립성과 복잡도의 균형점이 다르다.

| 비교 축 | 공유 [[002_database_definition|데이터베이스]] | [[090_service_kubernetes_network_load_balancing|서비스]]별 동일 엔진 DB | [[308_pgvector|폴리글랏 퍼시스턴스]] |
| :--- | :--- | :--- | :--- |
| [[001_dikw_pyramid|데이터]] 소유권 | 약함 | 중간 | 강함 |
| 기술 다양성 | 낮음 | 낮음 | 높음 |
| 워크로드 적합성 | 낮음 | 중간 | 높음 |
| 정합성 처리 | 로컬 조인 중심 | [[090_service_kubernetes_network_load_balancing|서비스]] 경계 일부 필요 | 이벤트·[[312_saga_pattern_choreography_orchestration|사가]] 중심 |
| 운영 복잡도 | 낮음 | 중간 | 높음 |

즉 [[090_service_kubernetes_network_load_balancing|서비스]]별 DB를 쓴다고 해서 곧바로 [[308_pgvector|폴리글랏 퍼시스턴스]]는 아니다. 모든 [[090_service_kubernetes_network_load_balancing|서비스]]가 여전히 같은 MySQL만 쓴다면 독립성은 생기지만, 저장 모델의 다양성을 활용하는 단계까지는 아니다. 반대로 저장소만 여러 개 도입하고 [[090_service_kubernetes_network_load_balancing|서비스]] 경계가 흐리면, 진짜 이점 없이 운영 부담만 커진다.

이 [[268_strategy_pattern|전략]]은 [[305_saga|사가 패턴]] ([[305_saga|Saga]]), [[368_cqrs|명령-조회 책임 분리]] ([[306_cqrs|CQRS]], [[250_cqrs_command_query_responsibility_segregation_pattern|Command Query Responsibility Segregation]]), [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]]) 과도 자주 연결된다. [[090_service_kubernetes_network_load_balancing|서비스]]마다 저장 모델이 달라질수록 전역 [[191_transaction_concept_states|트랜잭션]] 대신 이벤트 기반 [[212_synchronization_mechanisms|동기화]]와 읽기 모델 분리가 중요해지기 때문이다. 따라서 [[308_pgvector|폴리글랏 퍼시스턴스]]는 독립적인 저장소 선택 문제이면서 동시에 **통합 방식의 재설계 문제**이기도 하다.

- **📢 섹션 요약 비유**: 모두가 같은 서랍장을 쓰면 관리가 단순하지만 물건 특성에 맞춘 보관은 어렵다. 반대로 냉장고, 책장, 공구함을 따로 두면 효율은 올라가지만, 어디에 무엇이 있는지 관리 규칙도 함께 필요해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

전자상거래를 예로 들면, 주문·결제 [[090_service_kubernetes_network_load_balancing|서비스]]는 RDBMS가 자연스럽고, 상품 [[394_catalog_metadata|카탈로그]]는 문서 지향 저장소가 잘 맞으며, [[160_session_controlling_terminal|세션]]과 캐시는 [[542_redis|Redis]] 같은 [[036_key_value|키-값 저장소]]가 유리하다. 추천 [[090_service_kubernetes_network_load_balancing|서비스]]는 [[083_relationship_in_er_model|관계]]를 따라가는 [[070_graph_datastructure|그래프]] 질의가 많다면 [[070_graph_datastructure|그래프]] DB가 이점을 줄 수 있다. 이처럼 **[[064_relation_domain|도메인]] 경계와 접근 패턴이 분명히 다를 때** [[308_pgvector|폴리글랏 퍼시스턴스]]의 설득력이 커진다.

하지만 같은 조직이라도 모든 팀이 여러 저장소를 운영할 역량을 갖춘 것은 아니다. [[555_backup_and_restore_strategy|백업]], [[229_monitor|모니터]]링, 장애 [[658_ir_recovery|복구]], 보안 패치, [[001_dikw_pyramid|데이터]] 마이그레이션, 드라이버 관리가 모두 다양해지기 때문이다. 그래서 많은 경우 "먼저 [[090_service_kubernetes_network_load_balancing|서비스]]별 DB 분리, 필요 시 일부 [[090_service_kubernetes_network_load_balancing|서비스]]만 다른 엔진 채택"이 현실적인 접근이다.

아래 결정 흐름은 [[308_pgvector|폴리글랏 퍼시스턴스]]를 도입할지 판단하는 최소 질문을 정리한 것이다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│        Is polyglot persistence really justified for this domain?     │
├──────────────────────────────────────────────────────────────────────┤
│ service boundary and ownership clear?                                │
│        ├─ no  -> keep a simpler store strategy first                 │
│        └─ yes                                                         │
│ workload/consistency needs differ materially?                        │
│        ├─ no  -> same-engine database per service may be enough      │
│        └─ yes                                                         │
│ ops and integration patterns ready?                                  │
│        ├─ no  -> complexity risk high                                │
│        └─ yes -> polyglot candidate                                  │
└──────────────────────────────────────────────────────────────────────┘
```

### 기술사 판단 [[435_checklist_based_testing|체크리스트]]

1. [[090_service_kubernetes_network_load_balancing|서비스]] 경계와 [[001_dikw_pyramid|데이터]] 소유권이 명확한가?
2. 저장 모델 차이가 실제 [[282_performance_tactics|성능]]·생산성 이득으로 이어지는가?
3. 이벤트, [[014_api_posix|API]], [[217_cdc_binlog_change_capture_debezium|CDC]], [[312_saga_pattern_choreography_orchestration|사가]] 같은 연계 방식이 준비되어 있는가?
4. 팀이 여러 저장소의 운영·[[555_backup_and_restore_strategy|백업]]·보안·[[229_monitor|모니터]]링을 감당할 수 있는가?
5. 전역 조인과 전역 [[191_transaction_concept_states|트랜잭션]] 요구를 어떻게 줄일지 합의되었는가?

### 자주 나오는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[090_service_kubernetes_network_load_balancing|서비스]]는 분리했지만 여전히 서로의 DB를 직접 조회하는 경우
- "유행이라서" 저장소를 늘리고, 실제 워크로드 차이는 설명하지 못하는 경우
- 모든 [[090_service_kubernetes_network_load_balancing|서비스]] 경계를 [[249_two_phase_commit_2pc_distributed|2단계 커밋]] ([[549_2pc_two_phase_commit_limitations_msa|2PC]], [[549_2pc_two_phase_commit_limitations_msa|Two-Phase Commit]]) 으로 묶어 복잡도만 키우는 경우
- 조회 편의를 위해 교차 [[090_service_kubernetes_network_load_balancing|서비스]] 조인을 남발해 저장소 독립성을 깨는 경우

좋은 [[308_pgvector|폴리글랏 퍼시스턴스]]는 DB 종류의 수를 자랑하지 않는다. 오히려 어디까지는 단순성을 유지하고, 어디서부터 저장 모델을 달리해야 하는지 **절제된 분화**를 만드는 설계가 더 중요하다.

- **📢 섹션 요약 비유**: 공구함에 망치, 드라이버, 톱을 따로 두는 것은 현명하지만, 쓰지도 않을 공구를 잔뜩 사서 관리만 힘들어지면 실패다. [[308_pgvector|폴리글랏 퍼시스턴스]]도 꼭 필요한 도구만 늘려야 가치가 생긴다.

---

## Ⅴ. 기대효과 및 결론

[[308_pgvector|폴리글랏 퍼시스턴스]]를 적절히 적용하면 [[064_relation_domain|도메인]]별 [[282_performance_tactics|성능]] 최적화, 팀 자율성, 확장성, [[005_schema|스키마]] 유연성을 함께 확보할 수 있다. [[090_service_kubernetes_network_load_balancing|서비스]]는 자신에게 맞는 저장 모델과 배포 주기를 가질 수 있고, 특정 워크로드의 병목을 위해 전체 시스템을 동일하게 희생시키지 않아도 된다.

반면 한계도 명확하다. 저장소가 다양해질수록 운영 도구도 다양해지고, [[001_dikw_pyramid|데이터]] 정합성은 더 이상 하나의 [[548_local_vs_distributed_transactions|로컬 트랜잭션]]으로 끝나지 않는다. 따라서 이벤트 재처리, 중복 처리, [[001_dikw_pyramid|데이터]] 계보, 관측성 같은 [[136_variance|분산]] 시스템 문제를 함께 해결해야 한다.

결론적으로 [[308_pgvector|폴리글랏 퍼시스턴스]]는 "DB를 많이 쓰는 아키텍처"가 아니라, **[[090_service_kubernetes_network_load_balancing|서비스]] 경계와 [[001_dikw_pyramid|데이터]] 특성에 맞춰 저장소를 책임 있게 분화하는 아키텍처**다. 핵심은 화려한 기술 조합이 아니라, 어디에 어떤 저장 모델이 가장 자연스러운지를 설명할 수 있는가에 있다.

- **📢 섹션 요약 비유**: 좋은 주방은 냄비와 프라이팬과 오븐을 적절히 나눠 쓰지만, 무엇을 언제 쓸지 모르면 오히려 더 혼란스러워진다. [[308_pgvector|폴리글랏 퍼시스턴스]]도 도구보다 조리 계획이 먼저다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[311_database_per_service_pattern|데이터베이스 퍼 서비스]] | [[308_pgvector|폴리글랏 퍼시스턴스]]의 기본 전제 |
| 최종적 [[194_consistency_database_integrity|일관성]] ([[650_eventual_consistency|Eventual Consistency]]) | [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[001_dikw_pyramid|데이터]] [[212_synchronization_mechanisms|동기화]]의 기본 가정 |
| [[305_saga|사가 패턴]] ([[305_saga|Saga]]) | [[136_variance|분산]] 비즈니스 [[191_transaction_concept_states|트랜잭션]] 보상 방식 |
| [[314_transactional_outbox_pattern|트랜잭셔널 아웃박스]] | [[548_local_vs_distributed_transactions|로컬 트랜잭션]]과 이벤트 발행을 안전하게 연결 |
| [[218_cdc_change_data_capture|변경 데이터 캡처]] ([[217_cdc_binlog_change_capture_debezium|CDC]], [[217_cdc_binlog_change_capture_debezium|Change Data Capture]]) | [[001_dikw_pyramid|데이터]] 변경을 다른 [[090_service_kubernetes_network_load_balancing|서비스]]에 전파하는 방식 |
| [[306_cqrs|CQRS]] | [[289_cqrs_db|쓰기]] 모델과 읽기 모델 분리를 통해 저장소 특화를 강화 |
| 관측성 ([[642_observability_telemetry|Observability]]) | 다중 저장소 운영의 필수 관리 기반 |

### 📈 관련 키워드 및 발전 흐름도

```text
Monolithic shared database
    │
    ▼
Service boundary and data ownership
    │
    ▼
Database per Service
    │
    ▼
Fit-for-purpose store selection
    │
    ▼
Event / Outbox / Saga based integration
```

이 흐름은 단일 공유 [[002_database_definition|데이터베이스]]에서 출발해, [[090_service_kubernetes_network_load_balancing|서비스]] 경계와 [[001_dikw_pyramid|데이터]] 소유권을 명확히 하면서 목적 적합형 저장소 [[268_strategy_pattern|전략]]으로 발전하는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 국은 냄비에 끓이고, 빵은 오븐에 굽고, 샐러드는 그릇에 담는 게 더 잘 어울려요.
2. [[308_pgvector|폴리글랏 퍼시스턴스]]는 [[001_dikw_pyramid|데이터]]도 음식처럼 성격에 맞는 그릇을 따로 고르는 생각이에요.
3. 하지만 그릇만 많고 정리 규칙이 없으면 부엌이 더 어지러워지니까 조심해야 해요.
