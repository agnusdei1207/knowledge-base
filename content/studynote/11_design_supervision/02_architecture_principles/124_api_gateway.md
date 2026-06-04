---
title: "124. API 게이트웨이 (API Gateway)"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이 ([API Gateway](/studynote/04_software_engineering/11_testing_validation/934_api_gateway/))는 [마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/)([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/))에서 외부 클라이언트의 모든 요청이 통과하는 단일 진입점(single entry point)으로, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·[인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/), [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), 로드밸런싱, 속도 제한, [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/), [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 변환 등 공통 관심사(cross-cutting concerns)를 중앙에서 처리한다.
> 2. **가치**: 클라이언트가 내부 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 구조를 알 필요 없이 게이트웨이 하나에만 연결하면 되므로, 내부 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 재편·이동이 클라이언트에게 투명하게 처리된다. 각 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)에서 중복 구현하던 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·로깅·보안 로직을 게이트웨이로 일원화한다.
> 3. **판단 포인트**: [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이는 [SPOF](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) (Single Point of Failure, 단일 실패 지점)이자 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목이 될 수 있으므로, 고가용성(HA, High [Availability](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) 구성과 최소한의 비즈니스 로직 포함이 필수다. 게이트웨이가 비대해지면 "[ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/) ([Enterprise Service Bus](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/), 엔터프라이즈 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)) 재탄생"이라는 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)이 된다.

---

## Ⅰ. 개요 및 필요성

[MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경에서 클라이언트(모바일 앱, 웹 브라우저)가 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 직접 호출하면 심각한 문제가 발생한다. 클라이언트가 수십 개의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 엔드포인트를 알아야 하고, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 이동·재편 시 모든 클라이언트를 수정해야 하며, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 코드를 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)마다 중복 구현해야 한다.

[API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이는 이 모든 문제를 단일 진입점으로 해결한다. 게이트웨이는 프런트엔드와 백엔드 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 사이의 "역방향 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)(reverse [proxy](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/))" 역할을 하며, [BFF](/studynote/04_software_engineering/11_testing_validation/935_bff_backend_for_frontend/) ([Backend for Frontend](/studynote/04_software_engineering/11_testing_validation/935_bff_backend_for_frontend/), 프론트엔드용 백엔드) 패턴으로 각 클라이언트 유형(모바일·웹·[IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/))에 최적화된 게이트웨이를 별도로 구성하기도 한다.

```text
+-------------------------------------------------------------+
|          API 게이트웨이 통합 아키텍처                         |
+-------------------------------------------------------------+
|  [모바일 앱]  [웹 브라우저]  [IoT 디바이스]                 |
|       |            |               |                        |
|       +------------+---------------+                       |
|                    |                                        |
|           [API Gateway]                                     |
|    인증/인가 | 라우팅 | 속도제한 | 캐싱 | 로깅              |
|                    |                                        |
|       +------------+------------+                          |
|       v            v            v                          |
|  [주문 서비스] [결제 서비스] [회원 서비스]                   |
|   (내부 MSA 구조 클라이언트에게 투명)                        |
+-------------------------------------------------------------+
```

[API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이의 핵심 기능은 ① [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)(URL 패턴에 따른 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)), ② [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·[인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)([JWT](/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/) 토큰 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), OAuth 2.0), ③ 속도 제한([Rate Limiting](/studynote/09_security/05_web_app_security/520_rate_limiting/), 과부하 방지), ④ [서킷 브레이커](/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/)(하위 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애 격리), ⑤ 요청·응답 변환([프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 변환, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 집계)이다.

- **📢 섹션 요약 비유**: 대기업 본사 로비의 안내 데스크와 같다. 방문객(클라이언트)은 어떤 부서가 어디에 있는지 몰라도 안내 데스크(게이트웨이)에서 배지([인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))를 받고 올바른 층([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))으로 안내받는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이의 처리 파이프라인은 필터 체인(filter chain) 구조로 동작한다. 요청이 들어오면 사전 처리 필터(pre-filter), [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), 사후 처리 필터(post-filter) 순으로 처리된다. Spring Cloud Gateway의 GatewayFilter, Kong의 Plugin이 이 구조를 구현한다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) | URL 패턴·헤더로 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 선택 | Path Prefix, Header 기반 |
| [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·[인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) | [JWT](/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/), OAuth 2.0 토큰 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 중앙 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서버 연동 |
| 속도 제한 | 클라이언트별 요청 수 제한 | [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) 슬라이딩 윈도우 |
| [서킷 브레이커](/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) | 하위 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애 격리 | Resilience4j 통합 |
| 집계 (Aggregation) | 여러 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 응답을 하나로 합침 | [BFF](/studynote/04_software_engineering/11_testing_validation/935_bff_backend_for_frontend/) 패턴 |

```text
+-------------------------------------------------------------+
|     API 게이트웨이 요청 처리 파이프라인                       |
+-------------------------------------------------------------+
|  요청 수신                                                   |
|     |                                                       |
|  Pre-Filter: 인증 검증 -> 속도 제한 -> 로깅                   |
|     |                                                       |
|  라우팅: /api/orders/* -> 주문 서비스                         |
|     |                                                       |
|  서비스 호출 (서킷 브레이커 보호)                            |
|     |                                                       |
|  Post-Filter: 응답 변환 -> 헤더 추가 -> 로깅                  |
|     |                                                       |
|  응답 반환                                                   |
+-------------------------------------------------------------+
```

[성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 관점에서 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이는 모든 요청이 통과하므로 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 추가 최소화가 핵심이다. [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 토큰 [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/), 정적 응답 [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/), 비동기 비차단(non-blocking) 처리 방식(WebFlux, Netty)으로 게이트웨이 자체 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 최소화한다.

- **📢 섹션 요약 비유**: 공항 출입국 심사대(게이트웨이)는 모든 승객이 통과하므로 처리 속도가 중요하다. 심사관이 느리면 비행기 출발이 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)된다. 신속한 처리(non-blocking)와 사전 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)([캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/))이 필수다.

---
## Ⅲ. 비교 및 연결

[API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이와 [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)([Service Mesh](/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/))는 둘 다 [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 통신을 제어하지만 계층이 다르다.

| 비교 축 | A | B |
|:---|:---|:---|
| **위치** | 외부-내부 경계 (North-South 트래픽) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 내부 (East-West 트래픽) |
| **주 기능** | 외부 클라이언트 진입점 제어 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신 보안·관찰성 |
| **L7 처리** | [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), 변환 | [mTLS](/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/), 트래픽 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| **대표 도구** | Kong, NGINX, Spring Cloud Gateway | [Istio](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/), Linkerd |

[ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/)([Enterprise Service Bus](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/))는 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이의 반면교사다. ESB는 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 변환·[오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)·비즈니스 로직까지 중앙에 집중하여 단일 병목이 되었다. [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이는 "얇은 게이트웨이(thin gateway)" 원칙을 지켜야 ESB의 전철을 밟지 않는다.

- **📢 섹션 요약 비유**: 공항 보안 검색대([API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이)는 여권 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)과 수하물 검사만 한다. 비행 [스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) 결정(비즈니스 로직)까지 검색대에서 하면 줄이 끝없이 길어진다.

---
## Ⅳ. 실무 적용 및 기술사 판단

[API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이 도입 시 가장 중요한 비기능 요구사항은 고가용성(HA)과 낮은 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이다. 게이트웨이는 SPOF이므로 Active-Active [이중화](/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)와 자동 장애 조치([failover](/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/))가 필수다. 속도 제한을 위한 [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) 공유 상태, [서킷 브레이커](/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) 상태 공유도 다중 인스턴스 환경에서 정합성이 필요하다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 게이트웨이가 SPOF가 되지 않도록 Active-Active [이중화](/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 구성이 되어 있는가?
2. 게이트웨이에 비즈니스 로직이 없이 순수 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)·공통 관심사만 처리하는가?
3. 속도 제한, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)을 통해 게이트웨이 자체 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 최소화되어 있는가?
4. [서비스 디스커버리](/studynote/04_software_engineering/05_devops_ci_cd/306_service_discovery_pattern/)(Consul, Eureka)와 연동하여 [동적 라우팅](/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/)이 가능한가?
5. 각 클라이언트 유형(모바일·웹)에 맞는 [BFF](/studynote/04_software_engineering/11_testing_validation/935_bff_backend_for_frontend/) 패턴 적용이 검토되었는가?

- **📢 섹션 요약 비유**: 교통 [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)(게이트웨이)는 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)·지하철·택시 환승을 처리하지, 목적지에서 할 업무를 미리 처리하지 않는다. [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)가 막히면 전체 교통이 마비되므로 [이중화](/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)와 빠른 처리가 핵심이다.

---

## Ⅴ. 기대효과 및 결론

[API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이를 도입하면 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·보안·로깅·속도 제한이 중앙에서 일관되게 적용되어 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 공통 코드가 제거된다. 내부 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 구조 변경이 외부 클라이언트에게 투명하게 처리되어 MSA의 유연한 진화가 가능해진다.

한계는 [SPOF](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 위험과 게이트웨이 비대화다. 게이트웨이에 비즈니스 로직을 추가하는 유혹을 지속적으로 경계해야 하며, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 테스트와 모니터링이 게이트웨이 계층에서 필수적으로 수행되어야 한다.

미래 방향으로는 ① [GraphQL](/studynote/06_ict_convergence/03_cloud_infrastructure/246_graphql_query_language_overfetching_solution/) 게이트웨이로 클라이언트 맞춤 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 지원, ② [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 트래픽 [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)·동적 속도 제한, ③ [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 기반 고성능 게이트웨이 구현이 주목받고 있다.

[API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이는 MSA의 "현관문"이다. 현관문이 튼튼하고 빠르면 집 전체가 안전하고 효율적으로 작동한다.

- **📢 섹션 요약 비유**: 스마트폰의 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(게이트웨이)는 앱([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))들이 하드웨어(인프라)와 직접 통신하지 않고 OS를 통하게 한다. 보안·자원 관리가 중앙에서 일관되게 처리된다.

---

### 📌 관련 개념 맵

MSA 진입점 문제] -> API 게이트웨이] -> BFF 패턴] -> [서비스 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)(내부)] -> [관찰성 플랫폼]

| 개념 | 연결 포인트 |
|:---|:---|
| [BFF](/studynote/04_software_engineering/11_testing_validation/935_bff_backend_for_frontend/) ([Backend for Frontend](/studynote/04_software_engineering/11_testing_validation/935_bff_backend_for_frontend/)) | 클라이언트 유형별 최적화 게이트웨이 |
| [서킷 브레이커](/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) | 게이트웨이에서 하위 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애 격리 |
| [서비스 디스커버리](/studynote/04_software_engineering/05_devops_ci_cd/306_service_discovery_pattern/) | 게이트웨이의 [동적 라우팅](/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/) 테이블 업데이트 |
| [ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/) | [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이의 반면교사: 비즈니스 로직 집중 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) |

### 📈 관련 키워드 및 발전 흐름도

MSA 직접 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 호출 복잡성] -> API 게이트웨이 도입] -> BFF 패턴] -> GraphQL 게이트웨이] -> [서비스 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/) 보완] -> AI 기반 동적 트래픽 제어]

### 👶 어린이를 위한 3줄 비유 설명

1. 놀이공원에서 매표소([API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이)만 거치면 모든 놀이기구([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))를 이용할 수 있어요.
2. 매표소에서 입장권 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)([인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))과 어떤 구역으로 갈지([라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/))를 결정해줘요.
3. 방문객(클라이언트)은 각 놀이기구가 어디 있는지 몰라도 매표소가 안내해줘요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 180 / 530

<- **이전**: [123. 마이크로서비스 아키텍처 (MSA, Microservices Architecture)](/studynote/11_design_supervision/02_architecture_principles/123_msa_microservices_architecture/)
**다음**: [125. 서비스 메시 (Service Mesh)](/studynote/11_design_supervision/02_architecture_principles/125_service_mesh/) ->

---
