+++
title = "176. DAO 패턴 (Data Access Object Pattern)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 패턴 ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Access Object Pattern)은 비즈니스 로직이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 방식의 세부사항을 모르도록, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 코드를 별도 객체와 인터페이스 뒤로 분리하는 계층화 패턴이다.
> 2. **가치**: SQL (Structured Query Language), ORM (Object-Relational [Mapping](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/)), 커넥션 관리, 예외 변환을 한곳에 모아 기술 교체와 테스트를 쉽게 만들고, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 계층은 유스케이스와 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)에 집중할 수 있다.
> 3. **판단 포인트**: DAO는 저장소 복잡도가 있는 시스템에서 강력하지만, 의미 없는 Generic DAO로 모든 CRUD (Create, Read, Update, Delete)를 감싸거나 비즈니스 규칙을 [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 안에 넣으면 오히려 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 비용만 늘어난다.

---

## Ⅰ. 개요 및 필요성

[DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 패턴은 J2EE (Java 2 Platform, Enterprise Edition) 계열 엔터프라이즈 패턴에서 널리 정리된 접근 방식으로, 핵심 목적은 <strong>비즈니스 규칙과 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/">영속성</a> 세부 구현을 분리하는 것</strong>이다. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 코드 안에 SQL, Connection, ResultSet 매핑, 벤더별 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화가 함께 섞이면, 업무 규칙을 읽기도 어렵고 저장 기술을 바꾸기도 힘들어진다.

이 문제가 커지는 이유는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 코드가 단순히 "값 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)"로 끝나지 않기 때문이다. [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 경계, [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/), [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/), 캐시, 예외 변환, 여러 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)소스 연결이 얽히면서 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 계층이 인프라 의존성으로 오염된다. DAO는 이런 복잡도를 한 계층에 격리해 상위 계층이 "무엇을 조회·저장할 것인가"에만 집중하게 한다.

아래 그림은 DAO가 없을 때와 있을 때의 차이를 단순화해 보여 준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Why DAO is needed</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Without DAO</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Service = business rule + SQL + connection + row mapping</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">With DAO</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Service -&gt; DAO interface -&gt; persistence implementation</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">business rule separated from storage details</div></div>
</div>
</div>



즉 DAO의 필요성은 객체를 하나 더 만드는 데 있지 않다. <strong>변경 가능성이 큰 저장 기술을, 변경 비용이 비싼 업무 로직으로부터 떼어 놓는 것</strong>이 핵심이다.

- **📢 섹션 요약 비유**: 셰프가 요리법에 집중하려면 냉장창고 정리와 재료 반입 동선을 따로 맡는 조달 담당자가 필요한 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 아키텍처의 기본 형태는 "[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 인터페이스에 의존하고, 구현체가 실제 저장소 접근을 담당한다"는 구조다. 이때 DAO는 보통 SQL 실행, ORM 호출, 매핑, 예외 변환을 맡고, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 계층은 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 경계와 유스케이스 조합을 담당한다. 즉 DAO는 "어떻게 저장소와 대화할지"를 담당하고, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 "언제 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 써야 하는지"를 결정한다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) Interface | 상위 계층이 의존하는 계약 | 기술 세부 구현이 아닌 조회·저장 의도를 드러내야 함 |
| [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) Implementation | JDBC (Java [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) Connectivity), JPA (Java Persistence [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)), MyBatis 등 실제 접근 | SQL, 매핑, 벤더 차이, 예외 처리 담당 |
| [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) / Application Layer | 유스케이스 조합, [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 경계 | [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 여러 개를 묶어 업무 흐름 완성 |
| Mapper / Row Mapper | 레코드와 객체 간 변환 | 중복 매핑 로직 분리 |
| [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Source | 연결 관리와 [풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/) | 커넥션 재사용, 보안, 장애 처리 |

아래 그림은 DAO가 레이어 사이에서 어떤 경계를 만드는지 보여 준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DAO in layered architecture</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Controller</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Service / Application Layer &lt;- transaction boundary</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DAO interface</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ JDBC implementation</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ JPA / MyBatis implementation</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ Fake / Mock implementation for test</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Database / external storage</div></div>
</div>
</div>



이 구조에서 중요한 판단은 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)의 주도권을 어디에 둘 것인가다. 보통 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 계층에서 시작하고, DAO는 그 안에서 필요한 질의와 갱신을 수행한다. DAO가 비즈니스 흐름을 주도하거나 독자적으로 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 정책을 결정하기 시작하면 계층 책임이 다시 흐려진다.

또한 테스트 관점에서 DAO는 매우 유용한 seam을 제공한다. 상위 계층은 [Fake](/knowledge-base/studynote/04_software_engineering/11_testing_validation/463_fake_test_double/) DAO나 [Mock](/knowledge-base/studynote/04_software_engineering/11_testing_validation/462_mock_test_double/) DAO를 주입해 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 없이도 유스케이스를 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)할 수 있고, 저장소 구현은 별도의 통합 테스트로 좁혀서 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)할 수 있다.

- **📢 섹션 요약 비유**: [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 인터페이스는 주방의 주문서 양식과 같고, 실제 조달 담당자는 시장을 가든 창고를 열든 그 양식에 맞춰 재료를 가져오면 된다.

---

## Ⅲ. 비교 및 연결

DAO를 제대로 이해하려면 Repository, [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) Record, DTO ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Transfer Object)와의 경계를 분명히 해야 한다. 이름은 함께 등장하지만 바라보는 층이 다르다. DAO는 주로 <strong>저장 기술과 질의 실행</strong>에 초점이 있고, Repository는 <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 집합과 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/222_aggregate_ddd_transaction_consistency/">애그리게이트</a> 조회</strong>에 더 가깝다.

| 패턴 | 초점 | [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 단위 | 적합한 상황 |
| :--- | :--- | :--- | :--- |
| [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)·테이블·저장소 접근 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 메서드 | 레거시 DB, SQL 제어, 다중 저장 기술 |
| Repository | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [애그리게이트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/222_aggregate_ddd_transaction_consistency/) | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 집합 | [DDD](/knowledge-base/studynote/12_it_management/05_security_compliance/310_architecture/) ([Domain-Driven Design](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/127_ddd_domain_driven_design/)) 기반 모델 중심 설계 |
| [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) Record | 객체가 스스로 저장 | 행/레코드와 객체 결합 | 단순 CRUD 중심, 빠른 개발 |
| DTO ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Transfer Object) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전달 계약 | 요청/응답 페이로드 | 계층·프로세스 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 운반 |

실무에서는 Spring [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Repository처럼 프레임워크가 [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 역할 일부를 감춘 경우가 많다. 이때도 원리는 사라지지 않는다. 저장소 세부 구현을 상위 계층에서 분리한다는 DAO의 핵심 정신은 여전히 남아 있으며, 필요하면 Repository 내부에서 [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 수준의 세밀한 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 객체를 둘 수도 있다.

또 한 가지 흔한 혼동은 "[DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) = 무조건 좋은 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)"라는 생각이다. 단순한 CRUD 애플리케이션에서 ORM이 이미 충분한 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)를 제공하는데, 그 위에 메서드 이름만 다른 Generic DAO를 한 겹 더 씌우면 오히려 코드 탐색성과 의미 전달력이 떨어질 수 있다.

- **📢 섹션 요약 비유**: DAO와 Repository의 차이는 창고 담당자와 도서관 사서의 차이에 가깝다. 둘 다 물건을 찾아주지만, 하나는 보관과 꺼내기 기술에, 다른 하나는 어떤 묶음으로 관리할지에 더 초점이 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

DAO는 저장소 접근이 비즈니스 코드에 비해 복잡하거나, 기술 교체 가능성이 있거나, 여러 종류의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)소스를 함께 다룰 때 특히 효과가 크다. 예를 들어 레거시 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)와 신규 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 공존하거나, 특정 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)에 튜닝이 많이 필요하거나, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 없이 상위 계층 테스트를 자주 해야 하는 환경에서는 DAO의 분리 효과가 분명하다.

| 운영 시나리오 | [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 적용 판단 | 이유 |
| :--- | :--- | :--- |
| 레거시 DB + 복잡한 SQL / 저장 프로시저 | 적극 권장 | 저장 기술 복잡도와 벤더 종속성을 격리하기 좋음 |
| 다중 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)소스, 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 분리 | 권장 | 저장소별 구현 차이를 인터페이스 뒤에 숨길 수 있음 |
| Spring [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 단순 CRUD | 선택적 | 프레임워크 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)만으로 충분할 수 있음 |
| [DDD](/knowledge-base/studynote/12_it_management/05_security_compliance/310_architecture/) 중심 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) | Repository 우선, 필요 시 [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 보조 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 모델 의미를 더 잘 드러낼 수 있음 |

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 메서드가 `save`, `findAll` 같은 무의미한 범용 이름만 나열하지 않고, 실제 유스케이스를 드러내는가?
2. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 계층이 SQL, ORM 예외, 커넥션 세부 정보에 직접 노출되어 있지 않은가?
3. [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 경계가 DAO마다 쪼개지지 않고 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 레벨에서 관리되는가?
4. 테스트에서 [Fake](/knowledge-base/studynote/04_software_engineering/11_testing_validation/463_fake_test_double/) DAO나 [Mock](/knowledge-base/studynote/04_software_engineering/11_testing_validation/462_mock_test_double/) DAO를 활용할 수 있게 의존성 역전이 되어 있는가?
5. ORM이 이미 제공하는 기능 위에 중복 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)를 만들고 있지는 않은가?

### 자주 발생하는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모든 엔티티를 하나의 `GenericDao<T>`로 처리해 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 의미를 잃는 설계
- 비즈니스 규칙과 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 로직을 [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 안에 몰아넣는 구현
- `SQLException`, `ResultSet` 같은 저수준 세부사항을 상위 계층에 그대로 노출하는 구조
- 단순 프레임워크 래퍼만 만들고 실제로는 기술 교체성도 테스트성도 얻지 못하는 형식적 [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 도입

기술사 답안에서는 <strong>"DAO는 저장소 접근 세부 구현을 분리해 변경 비용과 테스트 비용을 낮추는 계층화 패턴이며, Repository·ORM과의 역할 경계를 분명히 해야 한다"</strong>라고 정리하면 설계 판단력이 드러난다.

- **📢 섹션 요약 비유**: [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 설계는 배관을 벽 안에 그냥 묻는 것이 아니라, 점검구를 두어 나중에 수리와 교체가 가능하게 만드는 건축 설계와 같다.

---

## Ⅴ. 기대효과 및 결론

[DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 패턴을 제대로 적용하면 비즈니스 로직은 저장 기술 변화에서 비교적 자유로워지고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 로직은 한곳에 모여 유지보수와 튜닝이 쉬워진다. 또한 상위 계층 테스트에서 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 의존성을 줄일 수 있어 개발 속도와 안정성이 함께 좋아진다. 결국 DAO의 가장 큰 효과는 "저장 방식의 변화가 업무 규칙 전체 수정으로 번지지 않게 한다"는 점이다.

다만 DAO는 만능 패턴이 아니다. 저장소 단순성이 높은 시스템에서는 과도한 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)가 오히려 읽기 어려운 코드를 만들 수 있다. 따라서 DAO를 기억할 때는 "무조건 한 계층 더 추가"가 아니라 <strong>"저장소 세부사항을 적절한 경계 뒤에 숨기는 패턴"</strong>으로 이해하는 것이 정확하다.

- **📢 섹션 요약 비유**: 좋은 DAO는 모든 가구에 바퀴를 다는 일이 아니라, 자주 바뀌는 부품만 쉽게 갈아 끼울 수 있게 만드는 모듈식 가구 설계와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Layered Architecture](/knowledge-base/studynote/04_software_engineering/04_testing_quality/205_layered_architecture_separation_of_concerns/) | DAO는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 저장소 사이에 책임 경계를 만든다. |
| Repository | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 중심 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)로, DAO와 비슷해 보여도 초점이 다르다. |
| ORM (Object-Relational [Mapping](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/)) | [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 구현체 안에서 활용될 수 있는 저장 기술이다. |
| DTO ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Transfer Object) | 계층 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전달에 쓰이며, [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 자체와는 역할이 다르다. |
| Mapper / Row Mapper | 레코드와 객체 사이 변환 책임을 분리한다. |
| [Dependency Injection](/knowledge-base/studynote/04_software_engineering/06_software_architecture/337_dependency_injection/) | [DAO](/knowledge-base/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 인터페이스와 구현체 교체, 테스트 대역 주입을 쉽게 한다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">비즈니스 로직과 SQL 혼재</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">DAO interface 도입</div>
<div class="kb-diagram-tree-item" style="--depth:2">JDBC / SQL 구현</div>
<div class="kb-diagram-tree-item" style="--depth:2">ORM 구현</div>
<div class="kb-diagram-tree-item" style="--depth:2">Fake / Mock 구현</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">서비스 계층의 저장소 독립성 확보</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">테스트 용이성 · 기술 교체성 향상</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Repository / DDD와의 역할 분화</div>
</div>
</div>



이 흐름은 DAO가 단순한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 클래스에서 출발해, 계층 분리와 테스트성 확보, 현대적 Repository 설계와의 경계 정립으로 이어지는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. DAO는 선생님이 직접 창고에 들어가지 않고, 필요한 준비물을 맡아 가져다주는 창고 담당자예요.
2. 그래서 선생님은 수업에만 집중하고, 창고 정리 방법이 바뀌어도 수업 방식은 크게 안 바뀌어요.
3. 하지만 창고 담당자를 너무 많이 만들거나 쓸데없이 복잡하게 만들면 오히려 준비물이 더 늦게 올 수도 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 232 / 530

← **이전**: [175. DTO 패턴 (Data Transfer Object Pattern)](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/175_dto_data_transfer_object/)
**다음**: [177. 프론트 컨트롤러 패턴 (Front Controller Pattern)](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/177_front_controller_pattern/) →

---
