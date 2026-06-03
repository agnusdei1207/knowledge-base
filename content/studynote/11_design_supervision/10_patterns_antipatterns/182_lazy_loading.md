+++
title = "182. 지연 로딩 (Lazy Loading)"
date = 2026-05-06

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 로딩 ([Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Loading)은 연관 객체나 무거운 자원을 즉시 가져오지 않고, 가상 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) (Virtual [Proxy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/))나 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화 장치를 통해 실제 접근 시점까지 비용을 미루는 패턴이다.
> 2. **가치**: 목록 조회나 큰 객체 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에서 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)과 메모리 사용량을 줄여 주며, ORM (Object-Relational [Mapping](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/)) 환경에서는 불필요한 JOIN과 과다 로딩을 억제하는 핵심 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 된다.
> 3. **판단 포인트**: [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Loading은 비용을 없애는 것이 아니라 뒤로 미루는 것이므로, 명시적 Fetch Plan과 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 경계를 함께 설계하지 않으면 N+1 문제, LazyInitializationException, 직렬화 오류 같은 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)으로 곧바로 바뀐다.

---

## Ⅰ. 개요 및 필요성

[지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 로딩은 "지금 당장 필요하지 않은 것은 아직 읽지 말자"는 설계 원리다. 엔터프라이즈 애플리케이션에서 주문, 회원, 결제, 상품처럼 객체 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 깊어질수록 연관 객체를 모두 즉시 로드하면 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 조회가 무거워지고, 화면이나 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) ([Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))가 실제로 쓰지 않는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)까지 메모리에 올리게 된다. 이 문제는 ORM을 쓰는 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 모델에서 특히 자주 드러난다.

예를 들어 주문 목록 화면이 주문번호, 상태, 주문일자만 보여 준다면 회원 주소, 주문 상세, 상품 설명까지 동시에 가져오는 것은 낭비다. 반대로 상세 화면에서는 그 연관 객체들이 곧바로 필요할 수 있다. 즉 같은 엔티티라도 유스케이스마다 필요한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 폭이 달라지므로, 로딩 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 하나로 고정하면 과소 조회 또는 과다 조회가 발생한다.

그래서 [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Loading은 "기본은 가볍게 읽고, 필요한 순간에만 확장하자"는 균형점을 제공한다. 설계감리 관점에서 중요한 것은 이 패턴이 단순 ORM 옵션이 아니라, <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/">응답 시간</a>·메모리·<a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> 수를 유스케이스별로 조절하는 비용 통제 장치</strong>라는 점이다.

- **📢 섹션 요약 비유**: [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 로딩은 책 한 권을 빌릴 때 도서관 전체 책장을 집으로 가져오지 않고, 읽고 싶은 책만 나중에 꺼내 오는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 로딩은 보통 실제 객체 대신 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를 먼저 돌려주는 방식으로 구현된다. 애플리케이션은 엔티티를 받지만, 연관 필드에는 아직 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화되지 않은 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)나 컬렉션 래퍼가 들어 있다. 코드가 해당 필드에 처음 접근하면 [영속성](/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/)(Persistence [Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/))나 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)([Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/))이 SQL을 실행해 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 로드하고, 이후부터는 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화된 객체를 재사용한다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 엔티티 / [Aggregate](/knowledge-base/studynote/04_software_engineering/04_testing_quality/222_aggregate_ddd_transaction_consistency/) | 비즈니스 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 담는 주체 | 어떤 연관이 기본 조회 대상인지 판단 필요 |
| [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) ([Proxy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)) | 실제 객체 대리자 | 첫 접근 시 로딩 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 발생 |
| Persistence [Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) / [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) | 로딩 가능 범위 유지 | 경계가 종료되면 [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) 접근 실패 가능 |
| Fetch [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) / Entity [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/) | 명시적 선로딩 도구 | 필요한 경우만 계획적으로 사용 |
| Batch Fetch | 여러 [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) 접근을 묶어 완화 | N+1 완화에 유용 |

아래 그림은 [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Loading의 실행 경로를 요약한다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Lazy loading execution path                                          │
├──────────────────────────────────────────────────────────────────────┤
│ Service / Use case                                                   │
│    │                                                                 │
│    ▼                                                                 │
│ Order entity loaded                                                  │
│   ├─ id, status, orderedAt   -> loaded now                           │
│   └─ member, items           -> proxy / lazy collection              │
│                                  │ first access                      │
│                                  ▼                                   │
│                       Persistence Context / Session                  │
│                                  │ SQL / cache lookup                │
│                                  ▼                                   │
│                           DB or 2nd-level cache                      │
│                                  │                                   │
│                                  └─ real object initialized          │
└──────────────────────────────────────────────────────────────────────┘
```

핵심은 "[지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)"이지 "무료"가 아니라는 점이다. [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)는 가벼워지지만, 나중에 접근하는 순간 추가 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 발생한다. 따라서 [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Loading의 품질은 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 기술 자체보다, 어떤 화면과 서비스가 어떤 시점에 어떤 연관을 실제로 읽는지 예측하고 설계했는가에 달려 있다.

- **📢 섹션 요약 비유**: [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 로딩은 커튼 뒤에 필요한 소품만 숨겨 두었다가 장면이 시작될 때 꺼내는 무대 연출과 같다.

---

## Ⅲ. 비교 및 연결

[Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Loading은 즉시 로딩 (Eager Loading)의 반대말처럼 보이지만, 실제 실무에서는 "명시적 Fetch Plan"과 함께 봐야 한다. 기본 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 Lazy로 두고, 상세 조회나 리포트처럼 반드시 필요한 경우에만 Fetch Join이나 DTO ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Transfer Object) Projection으로 선로딩하는 방식이 가장 안정적이다.

| 비교 축 | Eager Loading | [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Loading | 명시적 Fetch Plan |
| :--- | :--- | :--- | :--- |
| 기본 시점 | 조회 즉시 연관 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 로드 | 첫 접근 시 로드 | 유스케이스에 맞춰 필요한 것만 선별 로드 |
| 장점 | 한 번에 가져와 예측 가능 | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 응답 가벼움, 메모리 절감 | 과소/과다 로딩 균형 조절 |
| 대표 위험 | 과다 [JOIN](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/), 카테시안 곱, 메모리 증가 | N+1, [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 종료 후 예외 | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 설계 복잡도 증가 |
| 적합 상황 | 항상 함께 쓰는 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 선택적으로 쓰는 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 목록/상세/배치별 최적화 |

이 패턴은 [Repository Pattern](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/179_repository_pattern/), Unit of Work Pattern과도 밀접하다. Repository는 어떤 Aggregate를 어떤 방식으로 꺼낼지 결정하는 입구이고, Unit of Work는 같은 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 안에서 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화와 변경 추적을 가능하게 하는 실행 맥락이다. 즉 [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Loading은 혼자 작동하는 패턴이 아니라, <strong>조회 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>과 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a> 경계 패턴 위에서 비로소 안전해지는 패턴</strong>이다.

또한 [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Loading은 캐시와도 다르다. 캐시는 이미 읽은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다시 빠르게 주는 메커니즘이고, [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Loading은 처음 읽는 시점을 미루는 메커니즘이다. 둘을 혼동하면 "Lazy면 무조건 빠르다" 같은 잘못된 결론에 이르기 쉽다.

- **📢 섹션 요약 비유**: Eager가 장을 볼 때 필요한지 모르더라도 카트에 다 담는 방식이라면, Lazy는 메모만 해 두었다가 실제 요리할 때만 재료를 가져오는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 가장 안전한 원칙은 "기본은 [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/), 조회별로 Fetch Plan을 명시"다. 특히 JPA (Java Persistence [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))에서는 `@ManyToOne`, `@OneToOne` 기본값이 즉시 로딩이지만, 대부분의 실무 프로젝트는 이를 LAZY로 바꿔 두고 필요한 조회 메서드에서 Fetch [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/), `@EntityGraph`, DTO Projection을 선택적으로 사용한다. 그래야 화면별 요구에 맞는 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 제어가 가능하다.

| 실무 상황 | 권장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 이유 |
| :--- | :--- | :--- |
| 목록 화면 | [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) + DTO Projection 또는 필요한 Join만 사용 | 불필요한 연관 객체 방지 |
| 상세 화면 | [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) 기본 + Fetch [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) / Entity [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/) | 필요한 연관을 한 번에 로드 |
| 대량 [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) | [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) + Batch Fetch + 주기적 flush/clear | 메모리와 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 폭증 방지 |
| [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 직렬화 | 엔티티 직접 노출 지양, DTO 변환 | [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 직렬화·순환 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 방지 |

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 연관 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 기본값이 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 습관이 아니라 실제 조회 패턴에 맞춰 설정되어 있는가?
2. [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 밖에서 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를 건드려 LazyInitializationException이 나지 않도록 경계를 관리하는가?
3. 반복문 안의 [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) 접근으로 N+1 문제가 발생하지 않는지 SQL 로그로 검증하는가?
4. 목록/상세/배치/리포트 각각에 맞는 Fetch [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/), Batch Fetch, DTO Projection [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 있는가?
5. Open [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) In View를 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 문제 은폐 수단으로 남용하지 않는가?

### 자주 발생하는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모든 연관을 무조건 EAGER로 바꿔 두고 "예외가 안 나니 안전하다"고 생각하는 설계
- [REST](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) ([Representational State Transfer](/knowledge-base/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/)) 응답에서 엔티티를 그대로 직렬화해 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화와 순환 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 문제를 일으키는 구조
- 템플릿 또는 Controller 계층에서 반복문마다 [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) 연관을 접근해 N+1을 만드는 구현
- Open [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) In View에 의존해 조회 계획 없이 화면 계층에서 아무 때나 로딩하는 운영

기술사 답안에서는 <strong>"<a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/">Lazy</a> Loading은 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/">프록시</a>로 비용을 뒤로 미루는 패턴이며, 기본 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>으로는 유용하지만 유스케이스별 Fetch Plan과 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a> 경계가 함께 설계되지 않으면 곧바로 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> <a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a>이 된다"</strong>고 정리하면 좋다.

- **📢 섹션 요약 비유**: [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 로딩을 잘 쓰는 팀은 필요한 물건만 제때 가져오는 창고 관리자이고, 못 쓰는 팀은 찾을 때마다 창고를 들락거리며 줄을 세우는 팀과 같다.

---

## Ⅴ. 기대효과 및 결론

[지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 로딩의 가장 큰 효과는 기본 조회를 가볍게 만들 수 있다는 점이다. 목록 화면, 검색 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 대시보드처럼 일부 필드만 필요한 경우에는 과다 JOIN과 메모리 사용을 줄이고 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)을 개선할 수 있다. 또한 설계자가 유스케이스별로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 폭을 조절할 수 있어, 대형 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 모델에서도 확장성이 좋아진다.

반면 잘못 적용하면 문제는 더 교묘해진다. 예외는 실행 후반부에 터지고, N+1은 기능 테스트에서는 잘 보이지 않다가 운영 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 폭발하며, 장수명 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)은 원인 파악을 어렵게 만든다. 그래서 [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Loading은 "[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 옵션"이라기보다, <strong>의도적인 조회 설계와 관측성을 요구하는 패턴</strong>으로 이해하는 편이 맞다.

결론적으로 기억할 문장은 간단하다. <strong><a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/">Lazy</a> Loading은 비용을 숨기는 기술이 아니라, 비용 발생 시점을 통제하는 기술이다.</strong> 설계감리에서는 이 통제가 실제로 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 계획, [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 경계, DTO [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 구현되어 있는지를 확인해야 한다.

- **📢 섹션 요약 비유**: [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 로딩은 냉장고를 꽉 채워 두는 대신, 오늘 요리할 재료만 꺼내 쓰는 습관과 같지만 장보기 계획이 없으면 오히려 더 자주 왕복하게 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Virtual [Proxy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) | [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Loading을 구현하는 대표적인 대리 객체 메커니즘이다. |
| [Repository Pattern](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/179_repository_pattern/) | 어떤 Aggregate를 어떤 Fetch Plan으로 로드할지 결정하는 입구가 된다. |
| Unit of Work Pattern | 같은 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 안에서 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화와 변경 추적이 일어나는 실행 맥락이다. |
| Fetch [Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) | 필요한 연관을 한 번에 선로딩해 N+1을 줄이는 대표 기법이다. |
| Batch Fetch | [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) 접근이 여러 번 발생할 때 IN 조회 등으로 완화하는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. |
| DTO Projection | [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 직렬화와 과다 로딩을 피하기 위한 읽기 전용 대안이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
객체 그래프 확장
    │
    ▼
즉시 로딩의 과다 JOIN / 메모리 증가
    │
    ▼
Lazy Loading + Virtual Proxy 도입
    │
    ├─ first access -> 추가 SQL
    ├─ transaction boundary 중요
    ├─ N+1 -> fetch join / batch fetch
    └─ API 응답 -> DTO projection 필요
    │
    ▼
유스케이스별 Fetch Plan 설계
```

이 흐름은 [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Loading이 단순 ORM 속성이 아니라, 객체 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 비용을 유스케이스 단위로 재배치하는 설계 기법임을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 로딩은 장난감 상자를 전부 꺼내지 않고, 지금 놀 장난감만 하나씩 꺼내는 거예요.
2. 그래서 처음에는 방이 덜 어질러지지만, 필요할 때마다 어디 있는지 잘 알아야 해요.
3. 많이 놀 장난감이면 처음부터 같이 꺼내 두는 게 더 편할 때도 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 238 / 530

← **이전**: [181. 유닛 오브 워크 패턴 (Unit of Work Pattern)](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/181_unit_of_work_pattern/)
**다음**: [183. 마스터-워커 패턴 (Master-Worker Pattern)](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/183_master_worker_pattern/) →

---
