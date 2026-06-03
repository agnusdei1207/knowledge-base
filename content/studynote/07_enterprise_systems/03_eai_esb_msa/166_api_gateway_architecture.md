---
title: 166. API 게이트웨이 (API Gateway) - 클라이언트 요청을 단일 진입점으로 받아 적절한 마이크로서비스로 라우팅, 인증/인가,
  스로틀링(Throttling), 응답 통합(Aggregation) 담당 모듈
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트

> 1. **본질**: [[014_api_posix|API]] ([[014_api_posix|Application Programming Interface]]) 게이트웨이 ([[542_api_gateway|API Gateway]])는 [[213_msa_microservices_architecture|마이크로서비스 아키텍처]] ([[619_msa_traffic_hardware|MSA]], [[122_msa_microservices_architecture|Microservices Architecture]]) 앞단에서 모든 외부 요청을 받아 적절한 내부 [[090_service_kubernetes_network_load_balancing|서비스]]로 [[339_routing_overview_best_path_selection|라우팅]]하는 단일 진입점이다.
> 2. **가치**: [[303_authentication_authorization_patterns|인증]], 속도 제한, 응답 조합, 로깅 같은 공통 기능을 중앙에서 처리해 클라이언트 복잡도와 백엔드 중복 구현을 동시에 줄인다.
> 3. **판단 포인트**: [[014_api_posix|API]] 게이트웨이는 강력하지만 비대해지기 쉬우므로, 공통 [[164_policy|정책]]만 담당하는 얇은 계층으로 유지하고 비즈니스 로직의 본체가 되지 않도록 통제해야 한다.

---

## Ⅰ. 개요 및 필요성

[[014_api_posix|API]] ([[014_api_posix|Application Programming Interface]]) 게이트웨이 ([[542_api_gateway|API Gateway]])는 외부 클라이언트와 내부 [[532_microservices_decomposition_patterns|마이크로서비스]] 사이에 위치해 요청을 수신, [[395_verification_process_review|검증]], 전달하는 [[264_proxy_pattern_surrogate_access_control|프록시]] 계층이다. 모바일 앱, 웹, 파트너 시스템은 게이트웨이 주소만 알면 되고, 내부 [[090_service_kubernetes_network_load_balancing|서비스]]의 실제 위치나 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 변화는 게이트웨이가 흡수한다. 따라서 게이트웨이는 단순 [[264_proxy_pattern_surrogate_access_control|프록시]]를 넘어서 외부 인터페이스의 안정성을 보장하는 접점 역할을 한다.

이 구조가 필요해진 이유는 [[090_service_kubernetes_network_load_balancing|서비스]] 분해가 늘수록 클라이언트 부담이 급격히 커지기 때문이다. 주문, 결제, 배송, 리뷰가 각각 독립 [[090_service_kubernetes_network_load_balancing|서비스]]가 되면, 클라이언트는 여러 주소를 알고 각 [[090_service_kubernetes_network_load_balancing|서비스]]별 [[303_authentication_authorization_patterns|인증]] 규칙과 에러 처리를 구현해야 한다. [[090_service_kubernetes_network_load_balancing|서비스]]가 늘수록 앱 배포 주기, [[007_security_policy|보안 정책]], 장애 대응이 복잡해지므로, 이를 한곳에서 조율할 진입점이 필요해진다.

아래 그림은 게이트웨이가 없을 때의 직접 연결 구조와, 게이트웨이를 둔 뒤의 단일 진입 구조를 대비해 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│              API 게이트웨이의 필요성: 다중 호출을 단일 진입으로      │
├──────────────────────────────────────────────────────────────────────┤
│ Without Gateway                                                     │
│ Client ─▶ Order Service                                             │
│ Client ─▶ Payment Service                                           │
│ Client ─▶ Delivery Service                                          │
│                                                                      │
│ With Gateway                                                        │
│ Client ─▶ API Gateway ─┬─▶ Order Service                            │
│                        ├─▶ Payment Service                          │
│                        └─▶ Delivery Service                         │
└──────────────────────────────────────────────────────────────────────┘
```

즉 [[014_api_posix|API]] 게이트웨이는 내부 복잡성을 감추고 외부와의 계약을 안정화하는 경계 계층이다. [[090_service_kubernetes_network_load_balancing|서비스]] 수가 많아질수록 그 가치는 더 커진다.

- **📢 섹션 요약 비유**: [[014_api_posix|API]] 게이트웨이는 건물의 안내 데스크와 같다. 방문객은 방 번호를 모두 외울 필요 없이 안내 데스크에 목적만 말하면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[014_api_posix|API]] 게이트웨이의 핵심 원리는 **수신 → [[164_policy|정책]] 적용 → [[339_routing_overview_best_path_selection|라우팅]] → 응답 조합 → 관측** 흐름이다. 우선 요청을 받으면 [[303_authentication_authorization_patterns|인증]] 토큰을 [[396_validation|확인]]하고, 속도 제한이나 [[993_waf_web_application_firewall|웹 방화벽]] [[164_policy|정책]]을 적용한 뒤, [[306_service_discovery_pattern|서비스 디스커버리]] ([[303_service_discovery|Service Discovery]])나 [[340_static_routing_default_route_0_0_0_0|정적 라우팅]] 규칙을 바탕으로 적절한 백엔드로 전달한다. 필요하면 여러 [[090_service_kubernetes_network_load_balancing|서비스]] 응답을 모아 하나의 응답으로 재구성하고, 전 구간의 [[568_logs_distributed_logging_elk_fluentd|로그]]와 추적 정보를 남긴다.

| 기능 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| [[339_routing_overview_best_path_selection|라우팅]] ([[339_routing_overview_best_path_selection|Routing]]) | 통합 자원 [[289_identification_flags_fragmentation_offset|식별자]] (URI, Uniform Resource [[088_identifier_in_er_model|Identifier]])와 메서드에 따라 대상 [[090_service_kubernetes_network_load_balancing|서비스]] 결정 | 경로 규칙, [[288_version_ihl_tos_total_length|버전]] 관리 |
| [[303_authentication_authorization_patterns|인증]]·[[509_authorization_models_rbac_abac|인가]] | [[343_json|JSON]] 웹 토큰 ([[549_jwt_json_web_token|JWT]], [[549_jwt_json_web_token|JSON Web Token]]) 등 [[395_verification_process_review|검증]] | 중앙 [[164_policy|정책]], 만료 처리 |
| 속도 제한 | 남용·[[710_ddos_distributed_denial_of_service_botnet|분산 서비스 거부 공격]] (DDoS, Distributed Denial of [[090_service_kubernetes_network_load_balancing|Service]]) 완화 | 사용자별·키별 한도 |
| 응답 조합 | 여러 [[090_service_kubernetes_network_load_balancing|서비스]] 결과를 하나로 묶음 | [[015_지연_데이터_관점|지연]]시간 증가 주의 |
| [[295_protocol_field_tcp_udp_icmp|프로토콜]] 변환 | 외부 [[156_rest_representational_state_transfer|REST]] ([[477_rest_api_architecture|Representational State Transfer]])와 내부 [[479_grpc_protobuf_http2|gRPC]] (Google [[126_rpc|Remote Procedure Call]]) 등 연결 | 표준화와 [[282_performance_tactics|성능]] 균형 |
| 관측성 | [[568_logs_distributed_logging_elk_fluentd|로그]], [[342_routing_metric_hop_bandwidth_delay|메트릭]], 추적 수집 | 병목 가시화 |

아래 그림은 게이트웨이가 단순 전달자가 아니라, 요청 입구에서 여러 [[164_policy|정책]]을 순차 적용하는 계층임을 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                   API 게이트웨이 요청 처리 파이프라인               │
├──────────────────────────────────────────────────────────────────────┤
│ Client Request                                                      │
│      │                                                              │
│      ▼                                                              │
│ [Auth] → [Rate Limit] → [Route Decision] → [Backend Call]           │
│                                              │                       │
│                           ┌──────────────────┴───────────────┐       │
│                           ▼                                  ▼       │
│                    Service A                           Service B      │
│                           └──────────────┬───────────────────┘       │
│                                          ▼                           │
│                                 [Aggregate / Transform]              │
│                                          ▼                           │
│                                   Client Response                    │
└──────────────────────────────────────────────────────────────────────┘
```

중요한 점은 게이트웨이가 모든 일을 대신하면 안 된다는 것이다. 공통 [[164_policy|정책]]과 외부 계약 안정화는 게이트웨이의 역할이지만, 주문 계산이나 결제 규칙 같은 핵심 비즈니스 로직은 각 [[064_relation_domain|도메인]] [[090_service_kubernetes_network_load_balancing|서비스]]에 남겨야 한다. 그렇지 않으면 게이트웨이가 또 하나의 거대한 모놀리식 병목이 된다.

- **📢 섹션 요약 비유**: [[014_api_posix|API]] 게이트웨이는 공항 보안 검색대와 같다. 신분 [[396_validation|확인]], 금지 물품 검사, 게이트 안내까지는 맡지만, 비행기를 직접 조종하지는 않는다.

---

## Ⅲ. 비교 및 연결

[[014_api_posix|API]] 게이트웨이는 로드 밸런서 ([[031_load_balancer|Load Balancer]]), [[302_service_mesh_istio|서비스 메시]] ([[828_service_mesh_microservice_communication_infrastructure|Service Mesh]]), [[309_bff_backend_for_frontend_pattern|백엔드 포 프론트엔드]] ([[543_bff_backend_for_frontend|BFF]], [[543_bff_backend_for_frontend|Backend For Frontend]])와 자주 비교된다. 로드 밸런서는 동일 [[090_service_kubernetes_network_load_balancing|서비스]] 인스턴스들 사이의 [[136_variance|분산]]에 집중하고, [[302_service_mesh_istio|서비스 메시]]는 내부 [[090_service_kubernetes_network_load_balancing|서비스]] 간 통신 [[164_policy|정책]]에 집중한다. BFF는 특정 클라이언트 경험에 맞춘 맞춤형 백엔드 계층이다.

| 항목 | [[014_api_posix|API]] 게이트웨이 | 로드 밸런서 | [[302_service_mesh_istio|서비스 메시]] | [[543_bff_backend_for_frontend|BFF]] |
| :--- | :--- | :--- | :--- | :--- |
| 주 위치 | 외부 진입점 | [[090_service_kubernetes_network_load_balancing|서비스]] 앞단 | [[090_service_kubernetes_network_load_balancing|서비스]] 간 내부 통신 | 클라이언트별 전용 계층 |
| 핵심 목적 | 외부 요청 통제와 통합 | 트래픽 [[136_variance|분산]] | 내부 통신 제어 | 화면별 [[001_dikw_pyramid|데이터]] 최적화 |
| 대표 기능 | [[303_authentication_authorization_patterns|인증]], [[339_routing_overview_best_path_selection|라우팅]], 조합 | 헬스체크, [[136_variance|분산]] | 상호 전송계층 보안 ([[831_mtls_mutual_tls_microservices_zero_trust|mTLS]], Mutual Transport Layer [[283_security_tactics|Security]]), 재시도, 추적 | 모바일/웹 맞춤 응답 |
| 주의점 | 비대화 위험 | 기능 범위 제한 | 운영 복잡도 | 계층 증가 |

이 비교에서 중요한 트레이드오프는 중앙화와 [[136_variance|분산]]화다. 게이트웨이는 공통 [[164_policy|정책]]을 한곳에서 관리할 수 있어 편하지만, 모든 규칙이 몰리면 변경 속도가 느려지고 병목이 생길 수 있다. 반대로 [[164_policy|정책]]을 각 [[090_service_kubernetes_network_load_balancing|서비스]]에 [[136_variance|분산]]하면 자율성은 높아지지만, [[303_authentication_authorization_patterns|인증]]·로깅·제한 [[164_policy|정책]]이 중복 구현되어 [[194_consistency_database_integrity|일관성]]이 깨지기 쉽다.

실무적으로는 [[014_api_posix|API]] 게이트웨이와 [[543_bff_backend_for_frontend|BFF]], [[302_service_mesh_istio|서비스 메시]]를 경쟁 [[083_relationship_in_er_model|관계]]로 보기보다 역할 분담으로 보는 편이 맞다. 외부 진입은 게이트웨이, 내부 [[090_service_kubernetes_network_load_balancing|서비스]] 간 보안과 재시도는 [[302_service_mesh_istio|서비스 메시]], 화면 최적화는 BFF가 맡는 식으로 계층을 분리하면 복잡성을 더 잘 통제할 수 있다.

- **📢 섹션 요약 비유**: [[014_api_posix|API]] 게이트웨이는 건물 정문 경비실, [[302_service_mesh_istio|서비스 메시]]는 건물 내부 복도 규칙, BFF는 각 층 VIP 라운지 안내원에 가깝다. 비슷해 보여도 맡는 구역이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

전자상거래 [[090_service_kubernetes_network_load_balancing|서비스]]를 예로 들면, 모바일 앱의 홈 화면 하나를 위해 상품, 할인, 장바구니, 추천 [[090_service_kubernetes_network_load_balancing|서비스]]를 각각 직접 호출하면 네트워크 왕복 횟수가 크게 늘어난다. 이때 게이트웨이가 요청을 받아 내부 호출을 조합하면 클라이언트는 단 한 번의 호출로 필요한 [[001_dikw_pyramid|데이터]]를 얻을 수 있다. 동시에 [[303_authentication_authorization_patterns|인증]]과 속도 제한을 중앙 처리해 외부 공격과 오남용도 줄일 수 있다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 외부 공통 [[164_policy|정책]]만 게이트웨이에 두고, [[064_relation_domain|도메인]] 로직은 [[090_service_kubernetes_network_load_balancing|서비스]] 내부에 남겼는가?
2. 다중 인스턴스, [[082_zero_downtime_deployment_rolling_blue_green_canary|무중단 배포]], 장애 조치 구성이 되어 [[454_spof|단일 장애점]] ([[454_spof|SPOF]], Single Point of Failure)을 피했는가?
3. [[303_authentication_authorization_patterns|인증]] 실패율, [[015_지연_데이터_관점|지연]]시간, 백엔드별 에러율이 관측되도록 [[342_routing_metric_hop_bandwidth_delay|메트릭]]과 추적을 수집하는가?
4. 응답 조합이 과도해져 게이트웨이 자체가 병목이 되지 않는가?
5. 모바일·웹 요구가 크게 다르면 [[543_bff_backend_for_frontend|BFF]] 분리까지 검토했는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 모든 비즈니스 규칙을 게이트웨이에 몰아넣어 거대한 중앙 [[090_service_kubernetes_network_load_balancing|서비스]]로 만드는 경우
- 장애 전파 차단 장치 없이 [[573_timeout_retry_backoff_strategy|타임아웃]]을 길게 잡아 백엔드 장애가 전체로 번지는 경우
- 외부 계약 [[288_version_ihl_tos_total_length|버전]] 관리 없이 내부 [[090_service_kubernetes_network_load_balancing|서비스]] 변경을 그대로 노출하는 경우

기술사 답안에서는 [[014_api_posix|API]] 게이트웨이를 "[[339_routing_overview_best_path_selection|라우팅]] 서버" 정도로만 쓰면 부족하다. 왜 필요한지, 어떤 공통 기능을 중앙화하는지, 그리고 왜 비대화를 막아야 하는지까지 함께 설명해야 실제 설계 판단이 된다.

- **📢 섹션 요약 비유**: 좋은 [[014_api_posix|API]] 게이트웨이는 호텔 프런트처럼 손님을 안내하지만, 객실 청소와 주방 요리까지 직접 하겠다고 나서지는 않는다.

---

## Ⅴ. 기대효과 및 결론

[[014_api_posix|API]] 게이트웨이를 잘 설계하면 클라이언트는 더 단순해지고, 백엔드는 공통 기능 중복에서 벗어나며, [[007_security_policy|보안 정책]]과 외부 인터페이스 관리가 쉬워진다. 특히 [[303_authentication_authorization_patterns|인증]], [[339_routing_overview_best_path_selection|라우팅]], 로깅, 속도 제한을 한곳에서 통제할 수 있어 운영 [[194_consistency_database_integrity|일관성]]이 높아진다. [[090_service_kubernetes_network_load_balancing|서비스]] 수가 많아질수록 이러한 장점은 더 크게 체감된다.

하지만 게이트웨이는 만능 해결책이 아니다. 모든 요청이 통과하는 계층인 만큼 고가용성, 수평 확장, 캐시 [[268_strategy_pattern|전략]], 장애 격리가 충분히 설계되지 않으면 오히려 전체 시스템의 약점이 될 수 있다. 또한 화면별 요구까지 모두 끌어안으면 변경 속도를 떨어뜨리는 비대한 중앙 [[152_hub_dummy_switching_intelligent|허브]]가 되기 쉽다.

따라서 [[014_api_posix|API]] 게이트웨이는 "모든 것을 처리하는 중앙 서버"가 아니라, **외부 경계에서 공통 [[164_policy|정책]]을 담당하는 얇고 강한 진입점**으로 기억하는 것이 가장 실무적이다.

- **📢 섹션 요약 비유**: 좋은 정문은 사람을 빠르게 통과시키고 위험한 사람만 막는다. 정문이 쇼핑몰 전체를 대신 운영하려 하면 오히려 붐비고 무너진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[306_service_discovery_pattern|서비스 디스커버리]] ([[303_service_discovery|Service Discovery]]) | 게이트웨이가 대상 [[090_service_kubernetes_network_load_balancing|서비스]] 위치를 찾는 기반 |
| [[343_json|JSON]] 웹 토큰 ([[549_jwt_json_web_token|JWT]], [[549_jwt_json_web_token|JSON Web Token]]) | 중앙 [[303_authentication_authorization_patterns|인증]]·[[509_authorization_models_rbac_abac|인가]]에 자주 쓰이는 토큰 방식 |
| [[307_circuit_breaker_pattern|서킷 브레이커]] ([[304_circuit_breaker|Circuit Breaker]]) | 백엔드 장애 전파를 줄이는 [[571_protection_vs_security|보호]] 장치 |
| [[302_service_mesh_istio|서비스 메시]] ([[828_service_mesh_microservice_communication_infrastructure|Service Mesh]]) | 내부 통신 [[164_policy|정책]]을 [[136_variance|분산]] 처리하는 구조 |
| [[543_bff_backend_for_frontend|BFF]] ([[543_bff_backend_for_frontend|Backend For Frontend]]) | 클라이언트별 맞춤 응답 계층 |
| 로드 밸런서 ([[031_load_balancer|Load Balancer]]) | 인스턴스 [[136_variance|분산]]과 게이트웨이 [[456_dual_redundancy|이중화]] 기반 |

### 📈 관련 키워드 및 발전 흐름도

```text
클라이언트 직접 호출
    │
    ▼
API 게이트웨이 (API Gateway)
    │
    ├─ 인증·인가
    ├─ 라우팅
    ├─ 속도 제한
    └─ 응답 조합
    │
    ▼
BFF · 서비스 메시 · 제로 트러스트 경계 강화
```

이 흐름은 [[136_variance|분산]] 시스템이 단순 [[264_proxy_pattern_surrogate_access_control|프록시]]를 넘어, 외부 경계 [[164_policy|정책]]과 클라이언트 최적화를 분리하는 방향으로 발전하고 있음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[014_api_posix|API]] 게이트웨이는 가게 입구에서 손님을 맞아 주는 안내원이에요.
2. 손님은 안내원에게 한 번만 말하면, 안내원이 주문실과 계산실로 알아서 연결해 줘요.
3. 그래서 손님은 덜 헷갈리고, 가게는 규칙을 한곳에서 쉽게 지킬 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 166 / 482

← **이전**: [[165_soa_vs_msa_architecture|165. SOA vs MSA 차이점 - SOA는 전사적 재사용과 ESB 중앙 파이프 집중 (Smart Pipe, Dumb Endpoint),]]
**다음**: [[167_bff_backend_for_frontend|167. BFF (Backend For Frontend)]] →

---
