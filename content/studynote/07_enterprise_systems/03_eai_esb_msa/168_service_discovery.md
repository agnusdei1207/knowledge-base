---
title: 168. 서비스 디스커버리 (Service Discovery) 동적 컨테이너 위치 레지스트리
date: '2026-04-10'
tags:
- studynote-enterprise
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[306_service_discovery_pattern|서비스 디스커버리]] ([[303_service_discovery|Service Discovery]])는 [[090_service_kubernetes_network_load_balancing|서비스]] 이름과 살아 있는 인스턴스의 인터넷 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 주소 (IP, Internet [[295_protocol_field_tcp_udp_icmp|Protocol]]) 및 [[446_port_and_bus|포트]] ([[446_port_and_bus|Port]])를 연결해 주는 동적 위치 해석 체계다.
> 2. **가치**: 오토스케일링, [[193_rolling_update_deployment_kubernetes|롤링 배포]], 장애 [[658_ir_recovery|복구]]가 반복되는 [[619_msa_traffic_hardware|MSA]] ([[365_msa_microservice_architecture|Microservice Architecture]]) 환경에서 정적 [[009_config|설정]]을 줄이고, [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[195_coupling_levels|결합도]]를 낮춘다.
> 3. **판단 포인트**: [[235_registry_immutable_tag|레지스트리]]만 두면 끝나는 것이 아니라 등록, 헬스 체크, 만료, 로드밸런싱, 클라이언트 책임 범위를 함께 정해야 운영 안정성이 나온다.

---

## Ⅰ. 개요 및 필요성

[[306_service_discovery_pattern|서비스 디스커버리]]는 [[136_variance|분산]] 시스템에서 "[[090_service_kubernetes_network_load_balancing|서비스]]가 어디에 있는가"를 실시간으로 찾게 해 주는 패턴이다. 모놀리식 서버에서는 상대 주소가 거의 고정되어 있었지만, [[561_container_based_deployment|컨테이너]]와 [[073_container_orchestration_tools|오케스트레이션]] 환경에서는 인스턴스 수와 위치가 계속 바뀐다. 따라서 호출자는 더 이상 특정 IP를 신뢰할 수 없고, [[090_service_kubernetes_network_load_balancing|서비스]] 이름을 기준으로 현재 살아 있는 대상 목록을 받아야 한다.

이 개념이 필요한 가장 큰 이유는 [[571_resiliency_fault_tolerance_patterns|탄력성]] 때문이다. 주문 [[090_service_kubernetes_network_load_balancing|서비스]]가 트래픽 증가로 2개에서 10개 인스턴스로 늘어나거나, 장애로 특정 노드가 교체되면 주소가 즉시 변한다. 이때 호출 클라이언트가 [[009_config|설정]] [[501_file_definition_logical_record|파일]]에 박힌 주소만 믿고 있으면, 배포 자동화와 확장성의 장점이 모두 사라진다.

[[306_service_discovery_pattern|서비스 디스커버리]]는 단순한 전화번호부가 아니라 생존 정보가 반영되는 명부다. 등록만 하고 제거하지 않으면 죽은 인스턴스가 남고, 조회만 빠르고 건강 상태 판단이 약하면 장애 전파가 커진다. 그래서 이 패턴은 동적 주소 관리와 [[092_availability_management|가용성 관리]]가 결합된 운영 메커니즘으로 이해해야 한다.

- **📢 섹션 요약 비유**: [[306_service_discovery_pattern|서비스 디스커버리]]는 친구 주소록이 아니라, 지금 어디에 있고 연락 가능한지 계속 갱신되는 실시간 위치 공유 지도와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[306_service_discovery_pattern|서비스 디스커버리]]의 기본 흐름은 `인스턴스 기동 → 레지스트리 등록 → 헬스 체크/하트비트 → 호출 시 조회 → 종료 시 제거`다. 인스턴스는 자신이 올라온 주소를 [[235_registry_immutable_tag|레지스트리]]에 등록하고, 주기적으로 살아 있음을 알린다. 호출자나 로드밸런서는 [[090_service_kubernetes_network_load_balancing|서비스]] 이름으로 [[235_registry_immutable_tag|레지스트리]]를 조회해 사용 가능한 대상 중 하나를 선택한다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| [[090_service_kubernetes_network_load_balancing|서비스]] [[235_registry_immutable_tag|레지스트리]] | 인스턴스 목록 저장 | 고가용성, 읽기 [[282_performance_tactics|성능]] |
| 등록자 (Registrar) | 기동 시 주소 등록 | 자동화, 중복 방지 |
| 헬스 체크 / 하트비트 | 생존 여부 갱신 | [[294_ttl_time_to_live_looping_prevention|TTL]] ([[294_ttl_time_to_live_looping_prevention|Time To Live]]) [[164_policy|정책]], 오탐 방지 |
| 해석기 (Resolver) | [[090_service_kubernetes_network_load_balancing|서비스]] 이름으로 대상 조회 | 캐시 [[164_policy|정책]], 장애 전파 제어 |
| 로드밸런서 | 인스턴스 선택·[[136_variance|분산]] | [[178_round_robin_scheduling|라운드 로빈]], [[267_weight_bias_activation|가중치]], 지역성 |

아래 그림은 동적 환경에서 [[306_service_discovery_pattern|서비스 디스커버리]]가 어떻게 순환하는지 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│            Service Discovery control loop in dynamic MSA            │
├──────────────────────────────────────────────────────────────────────┤
│ [Instance boot] ─▶ Register ─▶ [Registry]                           │
│      ▲                         │                                     │
│      │                         ├─ Health check / heartbeat           │
│      │                         ▼                                     │
│ [Scale in / fail] ◀─ Deregister │                                    │
│                                └─ Lookup ─▶ [Caller / LB] ─▶ Route   │
└──────────────────────────────────────────────────────────────────────┘
```

이 구조의 핵심은 [[235_registry_immutable_tag|레지스트리]]가 "정답 그 자체"가 아니라 최신 상태를 최대한 빠르게 반영하는 조정자라는 점이다. 따라서 너무 긴 캐시를 두면 죽은 인스턴스를 오래 호출하게 되고, 너무 짧게 두면 [[235_registry_immutable_tag|레지스트리]] 부하가 커진다. 또한 헬스 체크는 단순 전송 제어 [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[405_tcp_transmission_control_protocol_connection_oriented|TCP]], [[405_tcp_transmission_control_protocol_connection_oriented|Transmission Control Protocol]]) 연결 여부만 보는지, 실제 [[008_dependencies|종속성]]까지 포함하는지에 따라 정확도와 민감도가 달라진다.

[[306_service_discovery_pattern|서비스 디스커버리]]는 보통 클라이언트 사이드와 서버 사이드 방식으로 구현된다. 다만 어떤 방식을 쓰든 공통 핵심은 **[[090_service_kubernetes_network_load_balancing|서비스]] 이름과 실제 주소를 분리하고, 살아 있는 대상만 선택하게 만드는 것**이다.

- **📢 섹션 요약 비유**: [[306_service_discovery_pattern|서비스 디스커버리]]는 가게 간판만 보고 찾아가는 것이 아니라, 오늘 실제로 문을 열었는지 [[396_validation|확인]]한 뒤 길을 안내해 주는 안내소와 같다.

---

## Ⅲ. 비교 및 연결

[[306_service_discovery_pattern|서비스 디스커버리]]의 대표 비교 축은 클라이언트 사이드와 서버 사이드다. 클라이언트 사이드는 호출자가 [[235_registry_immutable_tag|레지스트리]]를 직접 조회하고 로드밸런싱까지 수행한다. 서버 사이드는 애플리케이션 프로그래밍 인터페이스 게이트웨이 ([[542_api_gateway|API Gateway]]), [[264_proxy_pattern_surrogate_access_control|프록시]], [[094_ingress_kubernetes_l7_routing_gateway|인그레스]] ([[094_ingress_kubernetes_l7_routing_gateway|Ingress]]) 등이 대신 조회하고 [[136_variance|분산]]한다. 전자는 유연하고 홉이 적지만 클라이언트 [[336_library_vs_framework|라이브러리]]와 소프트웨어 개발 키트 (SDK, Software Development Kit) 복잡도가 높고, 후자는 호출자 단순화에 유리하지만 중앙 [[264_proxy_pattern_surrogate_access_control|프록시]] 의존성이 커진다.

| 항목 | 클라이언트 사이드 | 서버 사이드 |
| :--- | :--- | :--- |
| 조회 주체 | 애플리케이션 클라이언트 | [[264_proxy_pattern_surrogate_access_control|프록시]]·게이트웨이·로드밸런서 |
| 장점 | 홉 감소, 세밀한 [[164_policy|정책]] 적용 | 클라이언트 단순화, 중앙 통제 용이 |
| 단점 | SDK 의존, 언어별 구현 부담 | [[264_proxy_pattern_surrogate_access_control|프록시]] 병목, 추가 네트워크 홉 |
| 대표 예시 | Eureka + Ribbon 계열 | [[205_kubernetes_container_orchestration|Kubernetes]] [[090_service_kubernetes_network_load_balancing|Service]], Envoy, 클라우드 로드밸런서 |

또한 [[511_dns_hierarchical_distributed_architecture|DNS]] 기반 [[306_service_discovery_pattern|서비스 디스커버리]]와 전용 [[235_registry_immutable_tag|레지스트리]]도 구분해야 한다. DNS는 단순하고 표준적이지만 인스턴스 [[012_metadata|메타데이터]]와 세밀한 헬스 상태 표현이 제한적이다. 전용 [[235_registry_immutable_tag|레지스트리]]는 태그, [[288_version_ihl_tos_total_length|버전]], [[267_weight_bias_activation|가중치]], 지역 정보까지 풍부하게 다룰 수 있지만 운영 복잡도가 더 높다.

실무적으로는 [[302_service_mesh_istio|서비스 메시]] ([[828_service_mesh_microservice_communication_infrastructure|Service Mesh]]), [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] ([[205_kubernetes_container_orchestration|Kubernetes]]), [[014_api_posix|API]] ([[014_api_posix|Application Programming Interface]]) 게이트웨이와도 자연스럽게 이어진다. Kubernetes에서는 Service와 Endpoints가 기본 디스커버리 역할을 제공하고, [[302_service_mesh_istio|서비스 메시]]가 그 위에서 재시도, 회로 차단기, [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] (mutual Transport Layer [[283_security_tactics|Security]]) 같은 통신 [[164_policy|정책]]을 강화한다. 즉 [[306_service_discovery_pattern|서비스 디스커버리]]는 [[136_variance|분산]] 통신의 출발점이고, [[302_service_mesh_istio|서비스 메시]]와 게이트웨이는 그 위에 얹히는 운영 계층이다.

- **📢 섹션 요약 비유**: 클라이언트 사이드는 내가 직접 지도 앱으로 길을 찾는 것이고, 서버 사이드는 기사님이 목적지만 들으면 알아서 최적 경로로 데려다주는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

대표적인 실무 사례는 [[193_rolling_update_deployment_kubernetes|롤링 배포]] 중인 주문 시스템이다. `payment-service`가 새 [[288_version_ihl_tos_total_length|버전]]으로 교체되는 동안 기존 인스턴스와 신규 인스턴스가 함께 존재할 수 있는데, [[306_service_discovery_pattern|서비스 디스커버리]]가 없다면 호출자는 어떤 주소가 유효한지 알기 어렵다. [[235_registry_immutable_tag|레지스트리]]와 헬스 체크가 제대로 동작하면 준비 완료된 새 인스턴스만 목록에 포함시키고, 내려가는 인스턴스는 즉시 제외해 [[082_zero_downtime_deployment_rolling_blue_green_canary|무중단 배포]]에 가까운 운영이 가능해진다.

### 기술사 판단 [[435_checklist_based_testing|체크리스트]]

1. [[235_registry_immutable_tag|레지스트리]]가 [[454_spof|단일 장애점]]이 되지 않도록 [[016_replication_factor|복제]]·합의 구조를 갖췄는가?
2. 헬스 체크가 단순 프로세스 생존이 아니라 실제 요청 가능 상태를 반영하는가?
3. 캐시 만료 시간과 하트비트 주기가 장애 감지 속도와 과부하 사이에서 균형을 이루는가?
4. 클라이언트 또는 [[264_proxy_pattern_surrogate_access_control|프록시]]가 재시도, [[573_timeout_retry_backoff_strategy|타임아웃]], 회로 차단기 ([[304_circuit_breaker|Circuit Breaker]])와 함께 동작하는가?
5. [[090_service_kubernetes_network_load_balancing|서비스]] 이름 체계, [[288_version_ihl_tos_total_length|버전]] [[268_strategy_pattern|전략]], 지역 [[339_routing_overview_best_path_selection|라우팅]] [[164_policy|정책]]이 일관적인가?

### 채택 / 회피 기준

- **채택**: 인스턴스 [[087_process_state_transition|생성]]·삭제가 빈번하고, [[090_service_kubernetes_network_load_balancing|서비스]] 수가 많아 정적 주소 관리가 불가능한 환경
- **회피 또는 단순화**: 서버 수가 매우 적고 주소가 거의 고정된 소규모 시스템, 또는 플랫폼이 이미 충분한 내장 디스커버리를 제공하는 경우

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[235_registry_immutable_tag|레지스트리]]에 등록만 하고 종료 시 제거를 누락해 죽은 인스턴스를 계속 호출하는 경우
- [[306_service_discovery_pattern|서비스 디스커버리]]를 썼다는 이유로 [[573_timeout_retry_backoff_strategy|타임아웃]]·재시도·회로 차단기를 생략하는 경우
- 모든 [[012_metadata|메타데이터]]를 [[235_registry_immutable_tag|레지스트리]]에 몰아 넣어 구성 저장소와 역할을 혼동하는 경우

- **📢 섹션 요약 비유**: [[306_service_discovery_pattern|서비스 디스커버리]]를 잘 쓰는 것은 식당 리스트를 적어 두는 일이 아니라, 영업 중인 가게만 빠르게 골라 손님을 보내는 운영과 같다.

---

## Ⅴ. 기대효과 및 결론

[[306_service_discovery_pattern|서비스 디스커버리]]를 적용하면 [[090_service_kubernetes_network_load_balancing|서비스]] 간 의존성이 정적 주소에서 [[090_service_kubernetes_network_load_balancing|서비스]] 이름과 [[164_policy|정책]]으로 이동한다. 그 결과 오토스케일링, 장애 [[658_ir_recovery|복구]], [[193_rolling_update_deployment_kubernetes|롤링 배포]]가 훨씬 자연스러워지고, 애플리케이션은 "어디에 붙을까"보다 "무슨 [[090_service_kubernetes_network_load_balancing|서비스]]를 부를까"에 집중할 수 있다. 이는 [[531_cloud_native_architecture|클라우드 네이티브]] 운영의 핵심 전제 중 하나다.

하지만 [[235_registry_immutable_tag|레지스트리]]를 도입한다고 [[136_variance|분산]] 시스템의 복잡성이 사라지는 것은 아니다. 오히려 [[194_consistency_database_integrity|일관성]], 캐시, 장애 감지, [[190_split_brain_zookeeper_fencing_quorum|스플릿 브레인]], 잘못된 헬스 체크 같은 새로운 문제가 생길 수 있다. 따라서 [[306_service_discovery_pattern|서비스 디스커버리]]는 단순 편의 기능이 아니라, **동적 시스템의 위치 정보와 생존 정보를 관리하는 기반 인프라**로 기억해야 한다.

앞으로는 플랫폼 내장형 디스커버리와 [[302_service_mesh_istio|서비스 메시]]가 더 보편화되겠지만, 핵심 원리는 그대로다. [[090_service_kubernetes_network_load_balancing|서비스]]의 위치를 하드코딩하지 않고, 실시간 상태를 반영해 가장 적절한 대상에게 요청을 전달하는 것, 그것이 [[306_service_discovery_pattern|서비스 디스커버리]]의 본질이다.

- **📢 섹션 요약 비유**: 좋은 [[306_service_discovery_pattern|서비스 디스커버리]]는 전화번호부 한 권이 아니라, 지금 통화 가능한 사람만 자동으로 골라 주는 스마트 연락망과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 로드밸런싱 ([[196_hard_soft_real_time|Load Balancing]]) | 조회된 여러 인스턴스 중 실제 대상 선택 |
| 헬스 체크 (Health Check) | 죽은 인스턴스를 목록에서 제거하는 핵심 수단 |
| [[014_api_posix|API]] 게이트웨이 ([[542_api_gateway|API Gateway]]) | 서버 사이드 디스커버리의 대표 실행 위치 |
| [[302_service_mesh_istio|서비스 메시]] ([[828_service_mesh_microservice_communication_infrastructure|Service Mesh]]) | 디스커버리 위에 재시도·보안·관측성을 결합 |
| [[205_kubernetes_container_orchestration|Kubernetes]] [[090_service_kubernetes_network_load_balancing|Service]] | 플랫폼 내장 디스커버리와 가상 IP 제공 |
| 회로 차단기 ([[304_circuit_breaker|Circuit Breaker]]) | 잘못된 대상 선택 시 장애 전파를 줄이는 보완 장치 |

### 📈 관련 키워드 및 발전 흐름도

```text
정적 IP / 설정 파일 의존
    │
    ▼
서비스 레지스트리 도입
    │
    ├─ 등록 / 헬스 체크 / 조회
    ├─ 클라이언트 사이드 디스커버리
    └─ 서버 사이드 디스커버리
    │
    ▼
Kubernetes 내장 디스커버리 · 서비스 메시 · 정책 기반 라우팅
```

이 흐름은 [[136_variance|분산]] 시스템이 고정 주소 기반 통신에서, 상태 기반 [[341_dynamic_routing_protocol_operation|동적 라우팅]]과 플랫폼 자동화 중심으로 발전하는 모습을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[306_service_discovery_pattern|서비스 디스커버리]]는 친구 가게가 오늘 어디서 장사하는지 알려 주는 지도예요.
2. 가게가 이사하거나 문을 닫아도 지도가 바로 바뀌면 헛걸음을 하지 않아요.
3. 그래서 컴퓨터들은 주소를 외우지 않고, 이름만 말하고 지도를 물어봐요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 168 / 482

← **이전**: [[167_bff_backend_for_frontend|167. BFF (Backend For Frontend)]]
**다음**: [[169_client_side_vs_server_side_discovery|169. 클라이언트 사이드 디스커버리 (Client-side Discovery) vs 서버 사이드 디스커버리]] →

---
