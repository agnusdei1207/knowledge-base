+++
weight = 124
title = "124. API 게이트웨이 (API Gateway)"
date = "2026-05-10"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[014_api_posix|API]] 게이트웨이 ([[542_api_gateway|API Gateway]])는 [[213_msa_microservices_architecture|마이크로서비스 아키텍처]]([[619_msa_traffic_hardware|MSA]])에서 외부 클라이언트의 모든 요청이 통과하는 단일 진입점(single entry point)으로, [[303_authentication_authorization_patterns|인증]]·[[509_authorization_models_rbac_abac|인가]], [[339_routing_overview_best_path_selection|라우팅]], 로드밸런싱, 속도 제한, [[456_caching|캐싱]], [[295_protocol_field_tcp_udp_icmp|프로토콜]] 변환 등 공통 관심사(cross-cutting concerns)를 중앙에서 처리한다.
> 2. **가치**: 클라이언트가 내부 [[090_service_kubernetes_network_load_balancing|서비스]] 구조를 알 필요 없이 게이트웨이 하나에만 연결하면 되므로, 내부 [[090_service_kubernetes_network_load_balancing|서비스]] 재편·이동이 클라이언트에게 투명하게 처리된다. 각 [[532_microservices_decomposition_patterns|마이크로서비스]]에서 중복 구현하던 [[303_authentication_authorization_patterns|인증]]·로깅·보안 로직을 게이트웨이로 일원화한다.
> 3. **판단 포인트**: [[014_api_posix|API]] 게이트웨이는 [[454_spof|SPOF]] (Single Point of Failure, 단일 실패 지점)이자 [[282_performance_tactics|성능]] 병목이 될 수 있으므로, 고가용성(HA, High [[452_availability|Availability]]) 구성과 최소한의 비즈니스 로직 포함이 필수다. 게이트웨이가 비대해지면 "[[146_esb_enterprise_service_bus_architecture|ESB]] ([[146_esb_enterprise_service_bus_architecture|Enterprise Service Bus]], 엔터프라이즈 [[090_service_kubernetes_network_load_balancing|서비스]] [[344_bus|버스]]) 재탄생"이라는 [[128_water_scrum_fall_anti_pattern|안티패턴]]이 된다.

---

## Ⅰ. 개요 및 필요성

[[619_msa_traffic_hardware|MSA]] 환경에서 클라이언트(모바일 앱, 웹 브라우저)가 각 [[090_service_kubernetes_network_load_balancing|서비스]]에 직접 호출하면 심각한 문제가 발생한다. 클라이언트가 수십 개의 [[090_service_kubernetes_network_load_balancing|서비스]] 엔드포인트를 알아야 하고, [[090_service_kubernetes_network_load_balancing|서비스]] 이동·재편 시 모든 클라이언트를 수정해야 하며, [[303_authentication_authorization_patterns|인증]] 코드를 각 [[090_service_kubernetes_network_load_balancing|서비스]]마다 중복 구현해야 한다.

[[014_api_posix|API]] 게이트웨이는 이 모든 문제를 단일 진입점으로 해결한다. 게이트웨이는 프런트엔드와 백엔드 [[532_microservices_decomposition_patterns|마이크로서비스]] 사이의 "역방향 [[264_proxy_pattern_surrogate_access_control|프록시]](reverse [[264_proxy_pattern_surrogate_access_control|proxy]])" 역할을 하며, [[543_bff_backend_for_frontend|BFF]] ([[543_bff_backend_for_frontend|Backend for Frontend]], 프론트엔드용 백엔드) 패턴으로 각 클라이언트 유형(모바일·웹·[[101_iot_concept|IoT]])에 최적화된 게이트웨이를 별도로 구성하기도 한다.

```text
┌─────────────────────────────────────────────────────────────┐
│          API 게이트웨이 통합 아키텍처                         │
├─────────────────────────────────────────────────────────────┤
│  [모바일 앱]  [웹 브라우저]  [IoT 디바이스]                 │
│       │            │               │                        │
│       └────────────┴───────────────┘                       │
│                    │                                        │
│           [API Gateway]                                     │
│    인증/인가 │ 라우팅 │ 속도제한 │ 캐싱 │ 로깅              │
│                    │                                        │
│       ┌────────────┼────────────┐                          │
│       ▼            ▼            ▼                          │
│  [주문 서비스] [결제 서비스] [회원 서비스]                   │
│   (내부 MSA 구조 클라이언트에게 투명)                        │
└─────────────────────────────────────────────────────────────┘
```

[[014_api_posix|API]] 게이트웨이의 핵심 기능은 ① [[339_routing_overview_best_path_selection|라우팅]](URL 패턴에 따른 [[090_service_kubernetes_network_load_balancing|서비스]] [[339_routing_overview_best_path_selection|라우팅]]), ② [[303_authentication_authorization_patterns|인증]]·[[509_authorization_models_rbac_abac|인가]]([[549_jwt_json_web_token|JWT]] 토큰 [[395_verification_process_review|검증]], OAuth 2.0), ③ 속도 제한([[520_rate_limiting|Rate Limiting]], 과부하 방지), ④ [[307_circuit_breaker_pattern|서킷 브레이커]](하위 [[090_service_kubernetes_network_load_balancing|서비스]] 장애 격리), ⑤ 요청·응답 변환([[295_protocol_field_tcp_udp_icmp|프로토콜]] 변환, [[001_dikw_pyramid|데이터]] 집계)이다.

- **📢 섹션 요약 비유**: 대기업 본사 로비의 안내 데스크와 같다. 방문객(클라이언트)은 어떤 부서가 어디에 있는지 몰라도 안내 데스크(게이트웨이)에서 배지([[303_authentication_authorization_patterns|인증]])를 받고 올바른 층([[090_service_kubernetes_network_load_balancing|서비스]])으로 안내받는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[014_api_posix|API]] 게이트웨이의 처리 파이프라인은 필터 체인(filter chain) 구조로 동작한다. 요청이 들어오면 사전 처리 필터(pre-filter), [[339_routing_overview_best_path_selection|라우팅]], 사후 처리 필터(post-filter) 순으로 처리된다. Spring Cloud Gateway의 GatewayFilter, Kong의 Plugin이 이 구조를 구현한다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| [[339_routing_overview_best_path_selection|라우팅]] | URL 패턴·헤더로 [[090_service_kubernetes_network_load_balancing|서비스]] 선택 | Path Prefix, Header 기반 |
| [[303_authentication_authorization_patterns|인증]]·[[509_authorization_models_rbac_abac|인가]] | [[549_jwt_json_web_token|JWT]], OAuth 2.0 토큰 [[395_verification_process_review|검증]] | 중앙 [[303_authentication_authorization_patterns|인증]]서버 연동 |
| 속도 제한 | 클라이언트별 요청 수 제한 | [[542_redis|Redis]] 슬라이딩 윈도우 |
| [[307_circuit_breaker_pattern|서킷 브레이커]] | 하위 [[090_service_kubernetes_network_load_balancing|서비스]] 장애 격리 | Resilience4j 통합 |
| 집계 (Aggregation) | 여러 [[090_service_kubernetes_network_load_balancing|서비스]] 응답을 하나로 합침 | [[543_bff_backend_for_frontend|BFF]] 패턴 |

```text
┌─────────────────────────────────────────────────────────────┐
│     API 게이트웨이 요청 처리 파이프라인                       │
├─────────────────────────────────────────────────────────────┤
│  요청 수신                                                   │
│     │                                                       │
│  Pre-Filter: 인증 검증 → 속도 제한 → 로깅                   │
│     │                                                       │
│  라우팅: /api/orders/* → 주문 서비스                         │
│     │                                                       │
│  서비스 호출 (서킷 브레이커 보호)                            │
│     │                                                       │
│  Post-Filter: 응답 변환 → 헤더 추가 → 로깅                  │
│     │                                                       │
│  응답 반환                                                   │
└─────────────────────────────────────────────────────────────┘
```

[[282_performance_tactics|성능]] 관점에서 [[014_api_posix|API]] 게이트웨이는 모든 요청이 통과하므로 [[015_지연_데이터_관점|지연]] 추가 최소화가 핵심이다. [[303_authentication_authorization_patterns|인증]] 토큰 [[456_caching|캐싱]], 정적 응답 [[456_caching|캐싱]], 비동기 비차단(non-blocking) 처리 방식(WebFlux, Netty)으로 게이트웨이 자체 [[015_지연_데이터_관점|지연]]을 최소화한다.

- **📢 섹션 요약 비유**: 공항 출입국 심사대(게이트웨이)는 모든 승객이 통과하므로 처리 속도가 중요하다. 심사관이 느리면 비행기 출발이 [[015_지연_데이터_관점|지연]]된다. 신속한 처리(non-blocking)와 사전 [[395_verification_process_review|검증]]([[456_caching|캐싱]])이 필수다.

---
## Ⅲ. 비교 및 연결

[[014_api_posix|API]] 게이트웨이와 [[302_service_mesh_istio|서비스 메시]]([[828_service_mesh_microservice_communication_infrastructure|Service Mesh]])는 둘 다 [[619_msa_traffic_hardware|MSA]] 통신을 제어하지만 계층이 다르다.

| 비교 축 | A | B |
|:---|:---|:---|
| **위치** | 외부-내부 경계 (North-South 트래픽) | [[090_service_kubernetes_network_load_balancing|서비스]] 간 내부 (East-West 트래픽) |
| **주 기능** | 외부 클라이언트 진입점 제어 | [[090_service_kubernetes_network_load_balancing|서비스]] 간 통신 보안·관찰성 |
| **L7 처리** | [[461_http_stateless_connection_oriented|HTTP]] [[339_routing_overview_best_path_selection|라우팅]], 변환 | [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]], 트래픽 [[164_policy|정책]] |
| **대표 도구** | Kong, NGINX, Spring Cloud Gateway | [[302_service_mesh_istio|Istio]], Linkerd |

[[146_esb_enterprise_service_bus_architecture|ESB]]([[146_esb_enterprise_service_bus_architecture|Enterprise Service Bus]])는 [[014_api_posix|API]] 게이트웨이의 반면교사다. ESB는 [[389_mesh_topology|메시]]지 변환·[[073_container_orchestration_tools|오케스트레이션]]·비즈니스 로직까지 중앙에 집중하여 단일 병목이 되었다. [[014_api_posix|API]] 게이트웨이는 "얇은 게이트웨이(thin gateway)" 원칙을 지켜야 ESB의 전철을 밟지 않는다.

- **📢 섹션 요약 비유**: 공항 보안 검색대([[014_api_posix|API]] 게이트웨이)는 여권 [[396_validation|확인]]과 수하물 검사만 한다. 비행 [[208_schedule_history_transaction_execution_order|스케줄]] 결정(비즈니스 로직)까지 검색대에서 하면 줄이 끝없이 길어진다.

---
## Ⅳ. 실무 적용 및 기술사 판단

[[014_api_posix|API]] 게이트웨이 도입 시 가장 중요한 비기능 요구사항은 고가용성(HA)과 낮은 [[015_지연_데이터_관점|지연]]이다. 게이트웨이는 SPOF이므로 Active-Active [[456_dual_redundancy|이중화]]와 자동 장애 조치([[300_failover_architecture|failover]])가 필수다. 속도 제한을 위한 [[542_redis|Redis]] 공유 상태, [[307_circuit_breaker_pattern|서킷 브레이커]] 상태 공유도 다중 인스턴스 환경에서 정합성이 필요하다.

### 판단 [[435_checklist_based_testing|체크리스트]]
1. 게이트웨이가 SPOF가 되지 않도록 Active-Active [[456_dual_redundancy|이중화]] 구성이 되어 있는가?
2. 게이트웨이에 비즈니스 로직이 없이 순수 [[339_routing_overview_best_path_selection|라우팅]]·공통 관심사만 처리하는가?
3. 속도 제한, [[303_authentication_authorization_patterns|인증]] [[456_caching|캐싱]]을 통해 게이트웨이 자체 [[015_지연_데이터_관점|지연]]이 최소화되어 있는가?
4. [[306_service_discovery_pattern|서비스 디스커버리]](Consul, Eureka)와 연동하여 [[341_dynamic_routing_protocol_operation|동적 라우팅]]이 가능한가?
5. 각 클라이언트 유형(모바일·웹)에 맞는 [[543_bff_backend_for_frontend|BFF]] 패턴 적용이 검토되었는가?

- **📢 섹션 요약 비유**: 교통 [[152_hub_dummy_switching_intelligent|허브]](게이트웨이)는 [[344_bus|버스]]·지하철·택시 환승을 처리하지, 목적지에서 할 업무를 미리 처리하지 않는다. [[152_hub_dummy_switching_intelligent|허브]]가 막히면 전체 교통이 마비되므로 [[456_dual_redundancy|이중화]]와 빠른 처리가 핵심이다.

---

## Ⅴ. 기대효과 및 결론

[[014_api_posix|API]] 게이트웨이를 도입하면 [[303_authentication_authorization_patterns|인증]]·보안·로깅·속도 제한이 중앙에서 일관되게 적용되어 각 [[090_service_kubernetes_network_load_balancing|서비스]]의 공통 코드가 제거된다. 내부 [[090_service_kubernetes_network_load_balancing|서비스]] 구조 변경이 외부 클라이언트에게 투명하게 처리되어 MSA의 유연한 진화가 가능해진다.

한계는 [[454_spof|SPOF]] 위험과 게이트웨이 비대화다. 게이트웨이에 비즈니스 로직을 추가하는 유혹을 지속적으로 경계해야 하며, [[282_performance_tactics|성능]] 테스트와 모니터링이 게이트웨이 계층에서 필수적으로 수행되어야 한다.

미래 방향으로는 ① [[246_graphql_query_language_overfetching_solution|GraphQL]] 게이트웨이로 클라이언트 맞춤 [[298_qkv_attention|쿼리]] 지원, ② [[190_ai_llm_requirements_specification|AI]] 기반 트래픽 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]·동적 속도 제한, ③ [[615_ebpf|eBPF]] 기반 고성능 게이트웨이 구현이 주목받고 있다.

[[014_api_posix|API]] 게이트웨이는 MSA의 "현관문"이다. 현관문이 튼튼하고 빠르면 집 전체가 안전하고 효율적으로 작동한다.

- **📢 섹션 요약 비유**: 스마트폰의 [[001_operating_system_purpose|운영체제]](게이트웨이)는 앱([[090_service_kubernetes_network_load_balancing|서비스]])들이 하드웨어(인프라)와 직접 통신하지 않고 OS를 통하게 한다. 보안·자원 관리가 중앙에서 일관되게 처리된다.

---

### 📌 관련 개념 맵

[[[619_msa_traffic_hardware|MSA]] 진입점 문제] → [[[014_api_posix|API]] 게이트웨이] → [[[543_bff_backend_for_frontend|BFF]] 패턴] → [서비스 [[389_mesh_topology|메시]](내부)] → [관찰성 플랫폼]

| 개념 | 연결 포인트 |
|:---|:---|
| [[543_bff_backend_for_frontend|BFF]] ([[543_bff_backend_for_frontend|Backend for Frontend]]) | 클라이언트 유형별 최적화 게이트웨이 |
| [[307_circuit_breaker_pattern|서킷 브레이커]] | 게이트웨이에서 하위 [[090_service_kubernetes_network_load_balancing|서비스]] 장애 격리 |
| [[306_service_discovery_pattern|서비스 디스커버리]] | 게이트웨이의 [[341_dynamic_routing_protocol_operation|동적 라우팅]] 테이블 업데이트 |
| [[146_esb_enterprise_service_bus_architecture|ESB]] | [[014_api_posix|API]] 게이트웨이의 반면교사: 비즈니스 로직 집중 [[128_water_scrum_fall_anti_pattern|안티패턴]] |

### 📈 관련 키워드 및 발전 흐름도

[[[619_msa_traffic_hardware|MSA]] 직접 [[090_service_kubernetes_network_load_balancing|서비스]] 호출 복잡성] → [[[014_api_posix|API]] 게이트웨이 도입] → [[[543_bff_backend_for_frontend|BFF]] 패턴] → [[[246_graphql_query_language_overfetching_solution|GraphQL]] 게이트웨이] → [서비스 [[389_mesh_topology|메시]] 보완] → [[[190_ai_llm_requirements_specification|AI]] 기반 동적 트래픽 제어]

### 👶 어린이를 위한 3줄 비유 설명

1. 놀이공원에서 매표소([[014_api_posix|API]] 게이트웨이)만 거치면 모든 놀이기구([[090_service_kubernetes_network_load_balancing|서비스]])를 이용할 수 있어요.
2. 매표소에서 입장권 [[396_validation|확인]]([[303_authentication_authorization_patterns|인증]])과 어떤 구역으로 갈지([[339_routing_overview_best_path_selection|라우팅]])를 결정해줘요.
3. 방문객(클라이언트)은 각 놀이기구가 어디 있는지 몰라도 매표소가 안내해줘요!
