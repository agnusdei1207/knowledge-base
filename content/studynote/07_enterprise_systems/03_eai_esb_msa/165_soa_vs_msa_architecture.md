---
title: "165. SOA vs MSA 차이점 - SOA는 전사적 재사용과 ESB 중앙 파이프 집중 (Smart Pipe, Dumb Endpoint), MSA는 독립 배포/자율적 팀 주도, 메시지 큐 비동기 중심 (Dumb Pipe, Smart Endpoint) 결합"
date: "2026-05-05"
tags:
  - "studynote-enterprise-systems"
---


## 핵심 인사이트

> 1. **본질**: [서비스 지향 아키텍처](/studynote/04_software_engineering/04_testing_quality/212_soa_service_oriented_architecture_esb/) ([SOA](/studynote/01_computer_architecture/15_advanced_topics/618_soa_hardware/), [Service-Oriented Architecture](/studynote/07_enterprise_systems/06_exam_summary/362_soa_wsdl_uddi_soap/))와 [마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), [Microservices Architecture](/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/))는 모두 시스템을 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 분해하지만, SOA는 전사 통합과 재사용에, MSA는 독립 배포와 자율적 변화 대응에 더 큰 무게를 둔다.
> 2. **가치**: SOA는 이기종 시스템 통합과 공통 기능 공유에 강하고, MSA는 빠른 출시·부분 확장·팀 자율성 확보에 강하므로 조직의 목표에 따라 아키텍처 선택 기준이 달라진다.
> 3. **판단 포인트**: MSA가 항상 SOA보다 우월한 것이 아니라, 중앙 거버넌스가 필요한 전사 통합 문제인지, 빠른 제품 진화가 필요한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 문제인지에 따라 적합성이 갈린다.

---

## Ⅰ. 개요 및 필요성

SOA와 MSA는 모두 거대한 모놀리식 (Monolithic) 시스템의 복잡성을 줄이기 위해 등장한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 지향 접근이다. 공통 목표는 기능을 분리해 [결합도](/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)를 낮추고, 재사용성과 변경 용이성을 높이는 데 있다. 그러나 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 분해의 목적과 운영 방식이 다르기 때문에, 둘을 같은 말로 취급하면 실무 판단이 흐려진다.

SOA는 주로 기업 내부의 여러 시스템을 <strong>전사 수준에서 연결</strong>하려는 요구에서 발전했다. 인사, 회계, 영업, 생산처럼 서로 다른 시스템이 공통 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 재사용하고 표준 인터페이스로 연동해야 했기 때문이다. 반면 MSA는 대형 웹 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 클라우드 환경에서, 하나의 애플리케이션을 작은 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 쪼개 빠르게 배포하고 독립적으로 확장하려는 요구 속에서 부상했다.

즉 둘의 차이는 단순한 기술 세대 차이보다, "무엇을 통합하려는가"의 차이다. SOA는 기업 전체를 연결하는 통합 아키텍처 성격이 강하고, MSA는 제품 개발 속도와 운영 자율성을 높이는 [애플리케이션 아키텍처](/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/) 성격이 강하다.

```text
+----------------------------------------------------------------------+
|              같은 서비스 분해라도 출발점이 다르다                   |
+----------------------------------------------------------------------+
| SOA  : enterprise integration / reuse / governance                  |
| MSA  : product agility / independent deployment / scalability       |
|                                                                  |
| Common goal: reduce coupling by separating capabilities             |
+----------------------------------------------------------------------+
```

따라서 아키텍처 비교의 핵심 질문은 "[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 쪼갰는가"가 아니라, <strong>통합과 재사용이 중심인지, 독립 배포와 빠른 변경이 중심인지</strong>다.

- **📢 섹션 요약 비유**: SOA와 MSA는 둘 다 큰 회사를 부서별로 나누는 방식이지만, SOA는 회사 전체 업무를 연결하려는 본사 관점이고, MSA는 각 팀이 더 빨리 움직이게 하려는 현장 관점에 가깝다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SOA의 전형적 구조는 기업 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) ([ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/), [Enterprise Service Bus](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/))를 중심으로 여러 시스템을 연결하는 형태다. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 제공자들은 공통 표준과 중앙 거버넌스를 따르며, ESB가 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 변환, [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 변환, [보안 정책](/studynote/09_security/01_intro_principles/007_security_policy/)을 담당한다. 이 때문에 SOA는 "스마트 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/), 단순 엔드포인트" 성향이 강하다.

MSA는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 독립성을 더 강조한다. 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 자체 애플리케이션 프로그래밍 인터페이스 ([API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [Application Programming Interface](/studynote/02_operating_system/01_overview_architecture/014_api_posix/))와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소를 가지며, 직접 [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) ([Representational State Transfer](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/)), [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/), 이벤트 브로커를 통해 통신한다. 여기서는 중앙 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)보다 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 내부의 비즈니스 책임이 더 중요하므로 "단순 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/), 스마트 엔드포인트"에 가깝다.

| 구분 | [SOA](/studynote/01_computer_architecture/15_advanced_topics/618_soa_hardware/) | [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) |
| :--- | :--- | :--- |
| 중심 목적 | 전사 통합과 재사용 | 독립 배포와 빠른 변화 |
| 핵심 연결 방식 | [ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/) 중심 | [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) / 이벤트 중심 |
| 거버넌스 | 중앙 표준과 통제 강함 | 팀 자율성 상대적으로 큼 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관점 | 공유 [데이터 모델](/studynote/05_database/01_db_architecture_relational/014_data_model_components/) 가능 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유 선호 |
| 변화 단위 | 기업 공통 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 제품 기능 단위 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |

아래 그림은 두 구조의 핵심 차이를 직관적으로 보여준다.

```text
+------------------------------- SOA --------------------------------+
| [ERP]   [CRM]   [Billing]   [Legacy App]                           |
|    \      |       /             /                                  |
|     \     |      /             /                                   |
|      +----v-----v-------------v-----> [ ESB ]                       |
|                 routing / transform / policy                       |
+---------------------------------------------------------------------+

+------------------------------- MSA --------------------------------+
| [Order] <------> [Payment] <------> [Inventory]                        |
|    |             |                 |                                |
|  Order DB     Payment DB       Inventory DB                         |
|            event bus / REST / gRPC                                 |
+---------------------------------------------------------------------+
```

이 구조 차이는 장애 전파 방식에도 영향을 준다. SOA에서는 ESB가 강력한 통합 [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)가 되는 대신 병목이나 단일 고장점 ([SPOF](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/), Single Point of Failure)이 될 위험이 있다. MSA에서는 중앙 [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) 의존은 줄지만, 대신 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수가 많아지면서 네트워크 호출, [분산 추적](/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 관리가 더 어려워진다.

- **📢 섹션 요약 비유**: SOA는 중앙 환승역을 통해 모든 노선이 연결되는 철도망 같고, MSA는 여러 소규모 셔틀이 직접 움직이는 도시 교통망과 같다.

---

## Ⅲ. 비교 및 연결

실무에서 가장 중요한 비교 축은 <strong>통합 범위, <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 소유, 배포 독립성, 운영 복잡성</strong>이다. SOA는 전사 공통 기능을 묶고 표준화하는 데 강해, 여러 계열사 시스템과 레거시를 연결하는 데 유리하다. 반면 MSA는 한 제품 안에서 주문, 결제, 배송처럼 변화 속도가 다른 기능을 분리해 빠르게 개발·배포하는 데 강하다.

| 항목 | [SOA](/studynote/01_computer_architecture/15_advanced_topics/618_soa_hardware/) | [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) |
| :--- | :--- | :--- |
| 적합한 문제 | 기업 간·부서 간 시스템 통합 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 단위 제품 진화 |
| [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 크기 | 비교적 큼, 공통 기능 중심 | 더 작고 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 중심 |
| 배포 방식 | 중앙 조정 성격이 강함 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 독립 배포 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 중앙 모델·공유 모델 허용 | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 보상 처리 중시 |
| 운영 trade-off | 중앙 제어는 쉽지만 민첩성 저하 | 민첩성은 높지만 운영 복잡도 증가 |

또한 SOA와 MSA는 완전히 단절된 개념도 아니다. 기업은 전사 수준에서는 SOA적 통합 레이어를 유지하면서, 신규 디지털 채널이나 고객 접점 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 MSA로 설계할 수 있다. 즉 현실에서는 "SOA냐 MSA냐"의 이분법보다, <strong>어느 계층에 어떤 원칙을 적용할 것인가</strong>가 더 실무적이다.

이 차이는 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과도 연결된다. SOA는 표준 [데이터 모델](/studynote/05_database/01_db_architecture_relational/014_data_model_components/)과 변환을 중시해 공유 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)가 비교적 자연스럽지만, MSA는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 독립성을 위해 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 분리를 더 강하게 요구한다. 그래서 MSA는 [사가 패턴](/studynote/12_it_management/05_security_compliance/305_saga/) ([Saga Pattern](/studynote/12_it_management/05_security_compliance/948_saga_pattern/)), [이벤트 기반 아키텍처](/studynote/04_software_engineering/09_cloud_native_ai_architecture/538_event_driven_architecture_eda/) 같은 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 기법과 함께 논의되는 경우가 많다.

- **📢 섹션 요약 비유**: SOA가 여러 부서가 공용 문서실을 쓰는 회사라면, MSA는 팀마다 자기 문서함을 갖고 필요한 문서만 복사해 주고받는 회사에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

전사적 통합 프로젝트에서는 SOA가 여전히 유효하다. 예를 들어 은행, 보험, 카드, 채널 시스템이 제각각 다른 플랫폼에서 돌아가는 환경에서는 공통 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 고객 정보, [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 변환, [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적을 중앙에서 통제하는 편이 현실적일 수 있다. 반대로 전자상거래나 플랫폼 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)처럼 기능별 배포 속도와 확장 요구가 큰 제품에서는 MSA가 더 잘 맞는다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 문제의 중심이 전사 시스템 통합인가, 제품 기능의 빠른 변화 대응인가?
2. 공통 표준과 중앙 거버넌스가 필수인가, 팀 자율성이 더 중요한가?
3. [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)를 공유해도 되는가, 아니면 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 독립 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 필요한가?
4. 관측성 ([Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)), [지속적 통합](/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/)/[지속적 배포](/studynote/04_software_engineering/02_requirements_analysis/099_continuous_deployment_cd/) ([CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD, [Continuous Integration](/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/)/[Continuous Delivery](/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/)), 장애 격리 체계가 준비되었는가?
5. [ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/) 병목이나 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 모놀리식 같은 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)을 감당할 설계 원칙이 있는가?

### 판단 원칙

- **SOA가 유리한 경우**: 이기종 레거시 연계, 공통 표준 강제, 기업 간 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 중재가 핵심일 때.
- **MSA가 유리한 경우**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 배포 주기 차이, 부분 확장 요구, [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 중심 팀 운영이 중요할 때.
- **주의할 점**: SOA는 [ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/) 과대화가, MSA는 과도한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 분해와 공유 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)가 대표적 실패 원인이다.

기술사 답안에서는 "MSA가 최신이라서 더 좋다"는 식의 서술을 피해야 한다. 핵심은 목적 적합성이다. 전사 통합 문제에 MSA를 무리하게 적용하면 운영 비용만 커지고, 제품 민첩성이 중요한 곳에 무거운 SOA를 적용하면 출시 속도가 떨어질 수 있다.

- **📢 섹션 요약 비유**: SOA와 [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 선택은 더 멋진 공구를 고르는 일이 아니라, 배관 공사인지 가구 조립인지에 따라 맞는 도구를 고르는 일과 같다.

---

## Ⅴ. 기대효과 및 결론

SOA를 잘 적용하면 전사 공통 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 재사용, 인터페이스 표준화, 레거시 통합 비용 절감 효과를 얻을 수 있다. MSA를 잘 적용하면 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 독립 배포, 부분 확장, 장애 격리, 조직 민첩성 향상이라는 이점을 얻을 수 있다. 둘 다 궁극적으로는 복잡한 시스템을 더 다루기 쉽게 만들기 위한 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

하지만 두 방식 모두 전제조건이 있다. SOA는 과도한 중앙화가 민첩성을 해칠 수 있고, MSA는 자동화와 관측성이 부족하면 단순히 복잡한 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템이 될 뿐이다. 따라서 아키텍처의 좋고 나쁨보다, <strong>조직 구조와 운영 역량이 해당 구조를 감당할 수 있는가</strong>가 더 본질적인 판단 기준이다.

앞으로는 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 중심 통합, 이벤트 기반 연계, [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/), 내부 개발 플랫폼이 확산되면서 SOA와 MSA의 경계가 일부 섞일 수 있다. 그래도 기억할 핵심은 분명하다. SOA는 "전사를 연결하는 [서비스 전략](/studynote/12_it_management/02_itsm_itil/848_service_strategy/)", MSA는 "제품을 빠르게 진화시키는 [서비스 전략](/studynote/12_it_management/02_itsm_itil/848_service_strategy/)"에 더 가깝다.

- **📢 섹션 요약 비유**: 좋은 아키텍처는 유행을 따르는 옷이 아니라, 회사 체형과 일하는 방식에 맞는 맞춤 정장과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/) ([Enterprise Service Bus](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/)) | SOA의 대표적 통합 [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) |
| [API Gateway](/studynote/04_software_engineering/11_testing_validation/934_api_gateway/) | MSA의 외부 진입점 통합 수단 |
| [Saga Pattern](/studynote/12_it_management/05_security_compliance/948_saga_pattern/) | MSA의 [분산 트랜잭션](/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 대안 |
| [Monolithic Architecture](/studynote/13_cloud_architecture/03_msa_serverless/121_monolithic_architecture/) | [SOA](/studynote/01_computer_architecture/15_advanced_topics/618_soa_hardware/)·MSA가 해결하려는 출발점 |
| [Event-Driven Architecture](/studynote/13_cloud_architecture/03_msa_serverless/140_event_driven_architecture_eda/) | [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 확장과 느슨한 결합 강화 수단 |
| Governance | SOA와 MSA의 운영 철학을 가르는 축 |

### 📈 관련 키워드 및 발전 흐름도

```text
모놀리식 대형 시스템
    |
    v
SOA (전사 통합 · ESB · 재사용)
    |
    +- 레거시 연계 · 표준 인터페이스
    v
MSA (독립 배포 · 도메인 분리)
    |
    v
API Gateway · Event-Driven · Platform Engineering
```

이 흐름은 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 분해가 전사 통합 중심에서 제품 민첩성 중심으로 확장되어 온 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. SOA는 학교 전체가 같이 쓰는 큰 안내실을 두고 모든 일이 거기를 거쳐 가게 만드는 방법이에요.
2. MSA는 반마다 자기 준비물을 따로 챙기고, 필요할 때만 서로 연락하게 만드는 방법이에요.
3. 학교 전체 규칙을 맞춰야 할 땐 SOA가 좋고, 반마다 빨리 움직여야 할 땐 MSA가 더 잘 맞아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 165 / 482

<- **이전**: [164. 모놀리식 아키텍처 (Monolithic Architecture) - 프론트, 비즈니스 로직, DB 접근이 한 코드베이스와 단일](/studynote/07_enterprise_systems/03_eai_esb_msa/164_monolithic_architecture/)
**다음**: [166. API 게이트웨이 (API Gateway) - 클라이언트 요청을 단일 진입점으로 받아 적절한 마이크로서비스로 라우팅, 인증/인가,](/studynote/07_enterprise_systems/03_eai_esb_msa/166_api_gateway_architecture/) ->

---
