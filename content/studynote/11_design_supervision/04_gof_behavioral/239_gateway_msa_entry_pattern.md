+++
title = "239. 게이트웨이 MSA 진입점 패턴 (Gateway MSA Entry Pattern)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이 ([API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/)) 는 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) ([Microservices Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) 의 모든 외부 요청이 통과하는 단일 진입점으로, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·[라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)·로드밸런싱·속도제한을 중앙화한다.
> 2. **가치**: 클라이언트가 개별 마이크로서비스의 내부 구조를 알 필요가 없어 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)가 낮아지고, 횡단 관심사 (Cross-Cutting Concerns) 를 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 코드 밖에서 처리한다.
> 3. **판단 포인트**: 게이트웨이가 [SPoF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) (Single Point of Failure: [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)) 이 될 수 있으므로, 고가용성 (HA: High [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) 구성과 회로 차단기 ([Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/)) 가 필수다.

---

## Ⅰ. 개요 및 필요성
모놀리식 (Monolithic) 아키텍처에서는 단일 서버가 모든 요청을 처리했다. [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) ([Microservices Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) 로 전환하면 주문 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 결제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 사용자 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 등 수십 개의 마이크로서비스가 각자의 포트와 프로토콜을 가진다.

클라이언트(모바일 앱, 웹 브라우저)가 이 모든 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 주소를 알아야 한다면:

- **[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 변경 시 클라이언트도 수정** 필요
- **[인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·로깅이 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)마다 중복** 구현
- **CORS (Cross-Origin Resource Sharing) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)마다 개별** [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)

[API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이는 이 모든 문제를 해결하는 **MSA의 정문**이다.

[API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이가 동기 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) ([HyperText Transfer Protocol](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)) 요청의 진입점이라면, **[메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 게이트웨이 (Message Gateway)** 는 비동기 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 채널([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), RabbitMQ)에서 동일한 역할을 수행한다—[메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 포맷 변환, [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), 필터링.

```text
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Problem      │──▶│ Core Idea    │──▶│ Expected Gain │
└──────────────┘    └──────────────┘    └──────────────┘
```

- **📢 섹션 요약 비유**: 쇼핑몰 백화점의 정문 안내 데스크처럼, [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이는 모든 방문객(요청)을 맞이하고 적절한 매장([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))으로 안내한다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
┌──────────────────────────────────────────────────────────────────┐
│                    API Gateway 아키텍처                           │
│                                                                  │
│  [클라이언트]                                                     │
│  Mobile App ─────┐                                               │
│  Web Browser ────┤                                               │
│  Partner API ────┤                                               │
│                  ▼                                               │
│         ┌────────────────────────────────────────┐               │
│         │          API Gateway                   │               │
│         │  ┌─────────────────────────────────┐   │               │
│         │  │  1. SSL 종료 (TLS Termination)   │   │               │
│         │  │  2. 인증/인가 (Auth/AuthZ)        │   │               │
│         │  │  3. 요청 라우팅 (Routing)         │   │               │
│         │  │  4. 속도 제한 (Rate Limiting)     │   │               │
│         │  │  5. 요청 집계 (Aggregation)       │   │               │
│         │  │  6. 로드 밸런싱 (Load Balancing)  │   │               │
│         │  │  7. 캐싱 (Caching)               │   │               │
│         │  └─────────────────────────────────┘   │               │
│         └──────────────────┬───────────────────┘               │
│                            │                                     │
│          ┌─────────────────┼──────────────────────┐             │
│          ▼                 ▼                       ▼             │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐     │
│  │ User Service │  │ Order Service│  │  Payment Service   │     │
│  │ :8081        │  │ :8082        │  │  :8083             │     │
│  └──────────────┘  └──────────────┘  └────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

단일 게이트웨이 대신 클라이언트 유형별로 최적화된 게이트웨이를 두는 패턴:

```
Mobile App  ──▶  Mobile BFF  ──▶  마이크로서비스들
Web App     ──▶  Web BFF     ──▶  마이크로서비스들
Partner     ──▶  Partner GW  ──▶  마이크로서비스들
```

| 기능 | 설명 | 대표 구현 |
|:---|:---|:---|
| [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) ([Routing](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)) | URL → [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 매핑 | Spring Cloud Gateway, Kong |
| [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) ([Authentication](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/)) | [JWT](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/) ([JSON Web Token](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/)) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | OAuth2 통합 |
| 속도 제한 ([Rate Limiting](/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/)) | 초당 요청 수 제한 | [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 기반 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) |
| [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) ([Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/)) | 장애 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 격리 | Resilience4j |
| 집계 (Aggregation) | 여러 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 결과 합산 | [GraphQL](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/246_graphql_query_language_overfetching_solution/) Gateway |

- **📢 섹션 요약 비유**: 게이트웨이는 공항 관제탑이다. 모든 비행기(요청)의 이착륙([라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/))을 관리하고, 악천후([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애) 시 회항([Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/))을 결정한다.

---

## Ⅲ. 비교 및 연결
| 제품 | 유형 | 특징 | 적합 환경 |
|:---|:---|:---|:---|
| Kong | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) + 상용 | Lua 플러그인, 고성능 | 대규모 기업 |
| AWS [API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/) | 클라우드 관리형 | [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 통합, [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) | AWS 환경 |
| Spring Cloud Gateway | Java 기반 | Reactor 비동기, Spring 통합 | Spring Boot [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) |
| Nginx (엔진엑스) | 범용 리버스 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) | 경량, 빠름 | 간단한 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) |
| [Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/) [Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/) | [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/) | [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 방식, [mTLS](/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/) | [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 환경 |

| 항목 | [API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/) | [Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/) ([Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)) |
|:---|:---|:---|
| 위치 | 외부 경계 (Edge) | 내부 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 (East-West) |
| 제어 대상 | 외부 → 내부 트래픽 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 트래픽 |
| [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) | 불필요 | Envoy [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 필요 |
| 복잡도 | 중간 | 높음 |
| 주요 기능 | 외부 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) | 내부 [mTLS](/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/), 트레이싱 |

- **📢 섹션 요약 비유**: [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이는 나라의 국경 검문소(외부→내부), [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)는 나라 안에서 도시 간 이동을 관리하는 고속도로 시스템이다.

---

## Ⅳ. 실무 적용 및 기술사 판단
```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://USER-SERVICE
          predicates:
            - Path=/api/users/**
          filters:
            - StripPrefix=1
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 10
                redis-rate-limiter.burstCapacity: 20
        - id: order-service
          uri: lb://ORDER-SERVICE
          predicates:
            - Path=/api/orders/**
```

게이트웨이 자체가 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)이 되지 않도록:

1. **수평 확장 (Horizontal Scaling)**: 게이트웨이 인스턴스 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)
2. **Health Check (상태 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/))**: 주기적 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 상태 모니터링
3. **[Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/) ([서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/))**: 장애 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 자동 격리
4. **[Fallback](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/)**: [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 불가 시 기본 응답 반환

"[MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 도입 시 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이가 왜 필요한가?" — 답은 **캡슐화 + 횡단 관심사 중앙화**다. 클라이언트-[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)를 낮추고, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·로깅을 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 코드와 완전히 분리한다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 해결하려는 변화 축이 분명한가?
2. [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 비용보다 변경 절감 효과가 큰가?
3. 테스트·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 게이트웨이는 건물 로비의 방문객 등록 시스템이다. 누가 들어오는지 기록하고(로깅), 허가받은 사람만 통과([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))하며, 특정 층([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))으로 안내([라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/))한다.

---

## Ⅴ. 기대효과 및 결론
[API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이 도입 효과:

- **[결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) 감소**: 클라이언트가 내부 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 구조 변경에 영향받지 않음
- **보안 강화**: 외부에 노출되는 진입점을 하나로 제한
- **운영 가시성**: 게이트웨이에서 전체 트래픽 모니터링 가능
- **개발 생산성**: 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·로깅 코드 제거

[MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 전환에서 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이는 선택이 아닌 필수 인프라가 됐다. [BFF](/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/) ([Backend For Frontend](/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/)) 패턴과 결합하면 모바일·웹·파트너 API를 각각 최적화할 수 있어 클라이언트 경험도 향상된다.

확장 방향은 ① 선언형 API와의 결합, ② [관측 가능성](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)([Observability](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)) 내장, ③ [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이가 없는 MSA는 입구 없는 대형 쇼핑몰이다. 각 매장에 직접 들어가야 하니 안전도 없고, 안내도 없고, 혼란만 가득하다.

---

### 📌 관련 개념 맵
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) ([Microservices Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) | 게이트웨이가 필요한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 아키텍처 |
| 하위 개념 | [BFF](/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/) ([Backend For Frontend](/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/)) | 클라이언트별 최적화 게이트웨이 변형 |
| 하위 개념 | [Rate Limiting](/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/) (속도 제한) | 게이트웨이 핵심 기능 |
| 연관 개념 | [Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/) ([Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)) | 내부 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 트래픽 관리 |
| 연관 개념 | [Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/) ([서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/)) | 장애 격리 패턴 |
| 연관 개념 | [Load Balancer](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/031_load_balancer/) (로드 밸런서) | 요청 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 인프라 |

### 📈 관련 키워드 및 발전 흐름도
edge [routing](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) → 게이트웨이 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 진입점 패턴 → [service mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/)·[BFF](/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/)

### 👶 어린이를 위한 3줄 비유 설명
1. 놀이공원 입구([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이)에서 표를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)), 어떤 놀이기구([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))로 갈지 안내해 줘.
2. 입구가 하나라서, 어떤 놀이기구가 어디 있는지 손님은 몰라도 돼—입구가 다 알아서 안내해!
3. 놀이기구 하나가 고장 나도([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애) 입구에서 미리 알고 다른 데로 안내([Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/))해 줄 수 있어.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 300 / 530

← **이전**: [238. 클래스 테이블 상속 (Class Table Inheritance)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/238_class_table_inheritance/)
**다음**: [240. 조건문을 다형성으로 전환 (Replace Conditional with Polymorphism)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/240_refactoring_conditional_to_polymorphism/) →

---
