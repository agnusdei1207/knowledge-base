+++
weight = 163
title = "163. 마이크로서비스 아키텍처 (MSA, Microservices Architecture) - 거대한 모놀리식(Monolithic) 앱을 독립적으로 배포 및 확장 가능한 수십~수백 개의 작은 서비스(DB 포함 분리)로 쪼개는 차세대 엔터프라이즈 아키텍처"
date = "2026-05-05"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트

> 1. **본질**: [[213_msa_microservices_architecture|마이크로서비스 아키텍처]] ([[619_msa_traffic_hardware|MSA]], [[122_msa_microservices_architecture|Microservices Architecture]])는 하나의 거대한 애플리케이션을 비즈니스 기능 중심의 작은 [[090_service_kubernetes_network_load_balancing|서비스]]들로 분해하고, 각 [[090_service_kubernetes_network_load_balancing|서비스]]를 독립 배포·독립 확장·독립 운영 가능한 단위로 만드는 [[114_architecture_style|아키텍처 스타일]]이다.
> 2. **가치**: [[090_service_kubernetes_network_load_balancing|서비스]]별로 기술 선택, 배포 주기, 확장 [[268_strategy_pattern|전략]]을 다르게 가져갈 수 있어 빠른 출시와 팀 자율성을 높이고, 특정 기능의 장애나 트래픽 급증이 시스템 전체를 멈추지 않게 만들 수 있다.
> 3. **판단 포인트**: MSA의 진짜 난점은 분해 자체보다 [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]], [[090_service_kubernetes_network_load_balancing|서비스]] 경계, 관측성 ([[642_observability_telemetry|Observability]]), 자동화 수준을 감당할 수 있느냐에 있으므로, 조직과 운영 체계가 준비되지 않았다면 오히려 모놀리식보다 복잡해질 수 있다.

---

## Ⅰ. 개요 및 필요성

MSA는 애플리케이션을 주문, 결제, 배송, 회원 같은 **업무 능력 (Business Capability)** 단위로 쪼개어 각각 별도의 [[090_service_kubernetes_network_load_balancing|서비스]]로 운영하는 구조다. 각 [[090_service_kubernetes_network_load_balancing|서비스]]는 자체 [[007_codebase|코드베이스]]와 배포 단위를 가지며, 가능하면 자신의 [[001_dikw_pyramid|데이터]] 저장소도 함께 소유한다.

이 개념이 등장한 배경은 대형 모놀리식 시스템의 한계 때문이다. 처음에는 하나의 [[007_codebase|코드베이스]]가 개발과 배포에 유리하지만, 기능이 늘고 팀이 커지면 빌드 시간이 길어지고, 사소한 수정에도 전체 재배포가 필요하며, 특정 [[192_module_independence|모듈]]만 확장하고 싶어도 시스템 전체를 함께 키워야 한다. 클라우드와 [[076_ci_continuous_integration|지속적 통합]]/[[099_continuous_deployment_cd|지속적 배포]] ([[090_configuration_item|CI]]/CD, [[019_continuous_integration|Continuous Integration]]/[[164_continuous_delivery|Continuous Delivery]])가 일반화되면서, 기능 단위로 더 자주 배포하고 싶은 요구가 MSA를 밀어 올렸다.

즉 MSA는 "[[090_service_kubernetes_network_load_balancing|서비스]]를 잘게 쪼갠다"는 형식보다, **변화 속도가 다른 기능들을 서로의 발목을 잡지 않게 분리한다**는 목적에서 이해해야 한다. 이 목적이 없다면 단순 [[136_variance|분산]]은 이득보다 비용이 커질 수 있다.

- **📢 섹션 요약 비유**: MSA는 한 건물에 모든 부서가 몰려 있는 거대한 회사 대신, 주문팀·결제팀·배송팀이 각자 독립 사무실을 두고 필요할 때만 연결되는 구조와 같다. 한 팀이 야근한다고 다른 팀까지 모두 건물 전체를 다시 열 필요가 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

MSA의 핵심은 [[090_service_kubernetes_network_load_balancing|서비스]] 경계, 통신 방식, [[001_dikw_pyramid|데이터]] 소유권, 자동화된 운영 체계다. 각 [[090_service_kubernetes_network_load_balancing|서비스]]는 외부와는 애플리케이션 프로그래밍 인터페이스 ([[014_api_posix|API]], [[014_api_posix|Application Programming Interface]])나 [[145_message_broker_sync_async|메시지 브로커]]를 통해 통신하고, 내부 [[001_dikw_pyramid|데이터]]는 [[090_service_kubernetes_network_load_balancing|서비스]] 스스로 책임진다. 이때 [[014_api_posix|API]] 게이트웨이, [[306_service_discovery_pattern|서비스 디스커버리]], [[089_configuration_management|구성 관리]], [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]], [[626_log_collection|로그 수집]], [[205_kubernetes_container_orchestration|컨테이너 오케스트레이션]]이 함께 따라온다.

| 요소 | 역할 | 핵심 포인트 |
| :--- | :--- | :--- |
| [[090_service_kubernetes_network_load_balancing|서비스]] 경계 | [[064_relation_domain|도메인]]별 기능 분리 | 높은 [[193_cohesion_levels|응집도]], 낮은 [[195_coupling_levels|결합도]] |
| 독립 배포 | [[090_service_kubernetes_network_load_balancing|서비스]] 단위 릴리스 | 배포 속도와 장애 격리 |
| [[001_dikw_pyramid|데이터]] 분리 | [[090_service_kubernetes_network_load_balancing|서비스]]별 저장소 소유 | 강한 결합 방지 |
| 통신 방식 | [[156_rest_representational_state_transfer|REST]], [[479_grpc_protobuf_http2|gRPC]], [[389_mesh_topology|메시]]징 | 동기/비동기 trade-off |
| 운영 플랫폼 | [[561_container_based_deployment|컨테이너]], [[090_configuration_item|CI]]/CD, 관측성 | 자동화 없이는 운영 부담 증가 |

아래 그림은 MSA의 대표적인 구성 [[083_relationship_in_er_model|관계]]를 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                      MSA의 기본 서비스 구성도                       │
├──────────────────────────────────────────────────────────────────────┤
│ Client                                                              │
│   │                                                                  │
│   ▼                                                                  │
│ API Gateway                                                          │
│   ├─ Order Service   ── Order DB                                     │
│   ├─ Payment Service ── Payment DB                                   │
│   ├─ Delivery Service ── Delivery DB                                 │
│   └─ User Service    ── User DB                                      │
│                                                                      │
│ Services communicate via REST / gRPC / Event Bus                    │
└──────────────────────────────────────────────────────────────────────┘
```

이 구조에서 중요한 원리는 두 가지다. 첫째, [[090_service_kubernetes_network_load_balancing|서비스]]는 단순히 코드를 나눈 것이 아니라 **배포와 장애의 경계를 나눈 것**이어야 한다. 둘째, [[002_database_definition|데이터베이스]]를 공유하면 결국 배포와 변경 영향도가 다시 엮이므로, "[[090_service_kubernetes_network_load_balancing|서비스]]별 [[001_dikw_pyramid|데이터]] 소유"가 매우 중요하다. 그래서 MSA는 아키텍처와 동시에 [[001_dikw_pyramid|데이터]] 설계, 팀 구조, 배포 [[123_pipe|파이프]]라인까지 함께 바꾸는 전환이다.

- **📢 섹션 요약 비유**: MSA는 한 주방에서 모든 음식을 만드는 방식이 아니라, 피자집·초밥집·디저트 가게가 각자 자기 주방을 가지고 주문받은 뒤 한 플랫폼에서 조합해 내보내는 구조와 같다.

---

## Ⅲ. 비교 및 연결

MSA를 이해하는 가장 쉬운 방법은 [[121_monolithic_architecture|모놀리식 아키텍처]]와 비교하는 것이다. 모놀리식은 [[459_quic_fec_forward_error_correction|초기]] 개발과 단일 [[191_transaction_concept_states|트랜잭션]] 처리에 강하지만, 규모가 커질수록 배포와 확장이 둔해진다. MSA는 변화 대응과 독립 확장에 강하지만, 네트워크 호출과 [[001_dikw_pyramid|데이터]] [[136_variance|분산]]으로 인해 복잡성이 커진다.

| 항목 | 모놀리식 | [[619_msa_traffic_hardware|MSA]] |
| :--- | :--- | :--- |
| 배포 단위 | 전체 애플리케이션 | [[090_service_kubernetes_network_load_balancing|서비스]]별 개별 배포 |
| [[001_dikw_pyramid|데이터]] 관리 | 주로 단일 [[002_database_definition|데이터베이스]] | [[090_service_kubernetes_network_load_balancing|서비스]]별 [[001_dikw_pyramid|데이터]] 분리 |
| 확장 방식 | 전체를 함께 확장 | 필요한 [[090_service_kubernetes_network_load_balancing|서비스]]만 선택 확장 |
| 장애 영향 | 한 [[192_module_independence|모듈]] 문제가 전체로 번질 수 있음 | 격리 가능하나 연쇄 장애 주의 |
| 운영 난이도 | 개발은 단순, 대형화 시 느림 | 자동화 없으면 매우 복잡 |

또한 MSA는 [[212_soa_service_oriented_architecture_esb|서비스 지향 아키텍처]] ([[618_soa_hardware|SOA]], [[362_soa_wsdl_uddi_soap|Service-Oriented Architecture]])와도 연결된다. 둘 다 [[090_service_kubernetes_network_load_balancing|서비스]] 분해를 지향하지만, SOA가 전사 통합과 중앙 [[344_bus|버스]]에 무게를 두었다면 MSA는 애플리케이션 내부의 빠른 배포와 자율 팀 운영에 더 초점을 둔다. 이 때문에 MSA에서는 "스마트 [[123_pipe|파이프]]"보다 "스마트 엔드포인트"가 강조되고, [[538_event_driven_architecture_eda|이벤트 기반 아키텍처]], [[305_saga|사가 패턴]] ([[305_saga_pattern|Saga Pattern]]), [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] 같은 운영 개념이 함께 중요해진다.

결국 MSA의 장점은 기능 분해 그 자체가 아니라, **변화 속도와 장애 범위를 작은 단위로 제한할 수 있다는 점**에서 나온다. 반대로 [[090_service_kubernetes_network_load_balancing|서비스]] 경계가 잘못되면 네트워크 왕복만 늘어난 [[136_variance|분산]] 모놀리식이 된다.

- **📢 섹션 요약 비유**: 모놀리식이 큰 백화점 한 건물이라면, MSA는 전문점 거리다. 전문점 거리는 필요한 가게만 확장하기 좋지만, 길 안내와 물류 체계가 엉성하면 오히려 손님이 더 헤맨다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 MSA를 도입하기 좋은 경우는 팀 규모가 커지고, 기능별 배포 주기와 확장 패턴이 뚜렷하게 달라질 때다. 예를 들어 전자상거래 플랫폼에서 상품 조회는 초당 수만 건의 읽기 트래픽을 처리해야 하지만, 결제는 상대적으로 적은 요청이라도 높은 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]과 [[606_auditing_linux_auditd|감사]] 추적이 중요하다. 이런 경우 두 기능을 분리하면 각자 다른 확장 [[268_strategy_pattern|전략]]과 기술 [[057_stack|스택]]을 적용할 수 있다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. [[090_service_kubernetes_network_load_balancing|서비스]] 경계를 [[064_relation_domain|도메인]] 기준으로 설명할 수 있는가?
2. [[090_service_kubernetes_network_load_balancing|서비스]]별 [[001_dikw_pyramid|데이터]] 소유권이 명확한가, 아니면 결국 같은 [[002_database_definition|데이터베이스]]를 공유하는가?
3. 장애 추적을 위한 [[568_logs_distributed_logging_elk_fluentd|로그]]·[[342_routing_metric_hop_bandwidth_delay|메트릭]]·[[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] 체계가 있는가?
4. [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[191_transaction_concept_states|트랜잭션]]을 동기식 [[249_two_phase_commit_2pc_distributed|2단계 커밋]]이 아니라 [[312_saga_pattern_choreography_orchestration|사가]]나 보상 처리로 설계했는가?
5. 자동 배포, [[098_rollback_strategy_pipeline_error_threshold|롤백]], 헬스체크 없이는 운영이 불가능하다는 점을 준비했는가?

### 판단 원칙

- **채택**: 대규모 조직, 기능별 배포 빈도 차이, 부분 확장 요구가 클 때 유리하다.
- **보류**: 팀이 작고 [[064_relation_domain|도메인]]이 단순하며 단일 [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]]이 더 중요할 때는 모놀리식이 더 낫다.
- **주의**: 공통 테이블 공유, 과도한 동기 호출, [[090_service_kubernetes_network_load_balancing|서비스]] 경계 불명확은 대표적인 [[128_water_scrum_fall_anti_pattern|안티패턴]]이다.

기술사 답안에서는 "확장성이 좋다"는 장점만 쓰면 부족하다. 독립 배포의 대가로 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]], [[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]], 운영 복잡성이 증가한다는 trade-off를 반드시 같이 적어야 한다. 즉 MSA는 구조적 해법인 동시에 **운영 자동화를 전제로 하는 선택**이다.

- **📢 섹션 요약 비유**: [[619_msa_traffic_hardware|MSA]] 도입은 책상을 여러 개로 나누는 일이 아니라, 각 책상에 전화기·문서함·업무 규칙을 따로 두는 일과 같다. 자리만 쪼개고 협업 방식은 그대로면 방만 더 복잡해진다.

---

## Ⅴ. 기대효과 및 결론

MSA가 제대로 정착되면 기능별 독립 배포, 빠른 릴리스, 선택적 확장, 조직 자율성, 장애 격리 측면에서 큰 효과를 얻을 수 있다. 특히 [[531_cloud_native_architecture|클라우드 네이티브]] 환경에서는 [[561_container_based_deployment|컨테이너]] 기반 스케일아웃, [[194_blue_green_deployment_strategy|블루-그린 배포]], [[115_canary_deployment_gradual_rollout|카나리 배포]] 같은 운영 [[268_strategy_pattern|전략]]과 잘 결합된다. 결과적으로 변화가 잦은 [[090_service_kubernetes_network_load_balancing|서비스]]에서 비즈니스 민첩성을 높이는 데 매우 유리하다.

하지만 전제조건 없이 MSA를 도입하면 [[136_variance|분산]] 시스템 복잡성만 떠안게 된다. 네트워크 장애, [[001_dikw_pyramid|데이터]] 불일치, 테스트 난이도, 관측성 부족은 모놀리식에서 보지 못한 새로운 문제를 만든다. 따라서 MSA는 "더 현대적인 구조"라서가 아니라, **[[090_service_kubernetes_network_load_balancing|서비스]] 수명주기와 조직 운영 요구를 더 잘 반영할 수 있을 때만 가치가 있는 구조**로 기억해야 한다.

앞으로는 [[302_service_mesh_istio|서비스 메시]], [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]], 내부 개발 플랫폼과 결합한 형태로 계속 진화하겠지만, 핵심은 변하지 않는다. MSA의 본질은 [[136_variance|분산]] 그 자체가 아니라 **독립적으로 바뀌어야 하는 것들을 독립적으로 다룰 수 있게 만드는 설계**다.

- **📢 섹션 요약 비유**: 좋은 MSA는 여러 팀이 자기 속도로 달려도 서로 충돌하지 않게 차선을 나눠 둔 고속도로와 같다. 차선만 늘리는 것이 아니라 표지판, 관제, [[009_incident_response|사고 대응]]까지 같이 갖춰야 진짜 효과가 난다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[121_monolithic_architecture|모놀리식 아키텍처]] | MSA가 해결하려는 출발점 |
| [[618_soa_hardware|SOA]] | [[090_service_kubernetes_network_load_balancing|서비스]] 분해 철학의 선행 개념 |
| [[542_api_gateway|API Gateway]] | 외부 요청 진입점 통합 |
| [[305_saga_pattern|Saga Pattern]] | [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] 대안 |
| [[303_service_discovery|Service Discovery]] | 동적 [[090_service_kubernetes_network_load_balancing|서비스]] 위치 탐색 |
| [[642_observability_telemetry|Observability]] | [[568_logs_distributed_logging_elk_fluentd|로그]]·[[342_routing_metric_hop_bandwidth_delay|메트릭]]·트레이싱 기반 운영 가시성 |

### 📈 관련 키워드 및 발전 흐름도

```text
모놀리식 아키텍처
    │
    ▼
서비스 분해 요구 증가
    │
    ▼
MSA (독립 배포 · 독립 데이터)
    │
    ├─ API Gateway · Service Discovery
    ├─ Event-Driven Architecture
    └─ Saga · Observability · Platform Engineering
```

이 흐름은 "거대 단일 시스템 → [[090_service_kubernetes_network_load_balancing|서비스]] 분리 → 운영 자동화와 관측성 강화"로 이어지는 MSA의 확장 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 예전에는 장난감 가게, 과자 가게, 책 가게가 한 건물 안에 다 붙어 있어서 작은 고장에도 모두 쉬어야 했어요.
2. MSA는 가게들을 따로 나눠서, 과자 가게가 바빠도 책 가게는 자기 일만 잘할 수 있게 만든 거예요.
3. 대신 가게들이 서로 잘 이야기하도록 전화와 약속을 더 잘 정해야 해요.
