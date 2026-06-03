+++
weight = 125
title = "125. 서비스 메시 (Service Mesh)"
date = "2026-05-10"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[302_service_mesh_istio|서비스 메시]] ([[828_service_mesh_microservice_communication_infrastructure|Service Mesh]])는 [[532_microservices_decomposition_patterns|마이크로서비스]] 간 내부 통신(East-West 트래픽)의 [[339_routing_overview_best_path_selection|라우팅]], 로드밸런싱, [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] ([[187_mtls_mutual_tls_authentication|mutual TLS]], 상호 [[694_thread_local_storage_tls|TLS]] [[303_authentication_authorization_patterns|인증]]), 장애 주입, 관찰성을 비즈니스 코드에서 분리하여 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]]([[830_sidecar_proxy_architecture_envoy_decoupling|sidecar proxy]])로 인프라 계층에서 처리하는 아키텍처 패턴이다.
> 2. **가치**: 네트워크 [[571_resiliency_fault_tolerance_patterns|탄력성]] 코드(재시도, [[307_circuit_breaker_pattern|서킷 브레이커]], [[573_timeout_retry_backoff_strategy|타임아웃]])와 보안 코드([[090_service_kubernetes_network_load_balancing|서비스]] 간 암호화, [[509_authorization_models_rbac_abac|인가]])를 각 [[090_service_kubernetes_network_load_balancing|서비스]]에서 제거하고 인프라 계층에 일관되게 적용하므로, 개발자는 비즈니스 로직에만 집중할 수 있다.
> 3. **판단 포인트**: [[302_service_mesh_istio|서비스 메시]]는 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]]의 추가 메모리·CPU 오버헤드와 운영 복잡도를 수반하므로, [[090_service_kubernetes_network_load_balancing|서비스]] 수가 충분히 많고(20개 이상) [[090_service_kubernetes_network_load_balancing|서비스]] 간 보안·관찰성 요구가 높을 때 도입 가치가 있다.

---

## Ⅰ. 개요 및 필요성

[[619_msa_traffic_hardware|MSA]] 환경에서 [[090_service_kubernetes_network_load_balancing|서비스]] 수가 수십~수백 개로 늘어나면, 각 [[090_service_kubernetes_network_load_balancing|서비스]]마다 재시도(retry), [[573_timeout_retry_backoff_strategy|타임아웃]]([[319_timeout_prevention|timeout]]), [[307_circuit_breaker_pattern|서킷 브레이커]], [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] 코드를 별도로 구현하고 관리해야 하는 부담이 선형으로 증가한다. 언어가 다른 [[090_service_kubernetes_network_load_balancing|서비스]]들(Java, Go, Python)에서 동일한 네트워크 [[164_policy|정책]]을 일관되게 구현하기도 어렵다.

[[302_service_mesh_istio|서비스 메시]]는 이 문제를 [[182_sidecar_pattern_proxy_container|사이드카 패턴]]([[182_sidecar_pattern_proxy_container|Sidecar Pattern]])으로 해결한다. 각 [[090_service_kubernetes_network_load_balancing|서비스]] [[085_pod_kubernetes_container_unit|파드]]([[198_pod_kubernetes_minimum_deployment_unit|Pod]]) 옆에 Envoy [[264_proxy_pattern_surrogate_access_control|프록시]] [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]를 주입하면, 모든 인바운드·아웃바운드 트래픽이 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]를 거쳐 흐른다. 비즈니스 코드는 네트워크 [[164_policy|정책]]을 전혀 알 필요 없이 localhost:port로만 통신한다.

```text
┌─────────────────────────────────────────────────────────────┐
│           서비스 메시 사이드카 패턴 구조                      │
├─────────────────────────────────────────────────────────────┤
│  [서비스 A Pod]                 [서비스 B Pod]               │
│  ┌──────────┬───────────┐       ┌──────────┬───────────┐    │
│  │ 비즈니스  │ Envoy     │  ←──  │ Envoy    │ 비즈니스  │    │
│  │  코드     │ 사이드카  │  ──▶  │ 사이드카 │  코드     │    │
│  └──────────┴───────────┘       └──────────┴───────────┘    │
│                                                             │
│  [컨트롤 플레인 (Istio Control Plane)]                      │
│   Pilot(라우팅 설정) + Citadel(인증서 관리) + Galley(설정)  │
│        │                              │                     │
│        └──── 사이드카 정책 배포 ──────┘                     │
└─────────────────────────────────────────────────────────────┘
```

[[302_service_mesh_istio|서비스 메시]]는 [[001_dikw_pyramid|데이터]] 플레인([[001_dikw_pyramid|Data]] Plane)과 컨트롤 플레인(Control Plane)으로 구성된다. [[001_dikw_pyramid|데이터]] 플레인은 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]]들이 실제 트래픽을 처리하고, 컨트롤 플레인은 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]들에게 [[339_routing_overview_best_path_selection|라우팅]] 규칙, [[303_authentication_authorization_patterns|인증]]서, [[164_policy|정책]]을 중앙에서 배포한다.

- **📢 섹션 요약 비유**: [[302_service_mesh_istio|서비스 메시]]는 도로 교통 시스템(인프라)이 신호등·속도 제한·과속 단속을 담당하는 것과 같다. 운전자(비즈니스 코드)는 교통법규를 직접 집행하지 않고 도로 시스템이 자동으로 처리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[302_service_mesh_istio|서비스 메시]]의 핵심 기능은 네 가지 영역으로 나뉜다. ① 트래픽 관리: [[115_canary_deployment_gradual_rollout|카나리 배포]], 트래픽 분할, 재시도·[[573_timeout_retry_backoff_strategy|타임아웃]] [[164_policy|정책]], ② 보안: [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] 상호 [[303_authentication_authorization_patterns|인증]], [[509_authorization_models_rbac_abac|인가]] [[164_policy|정책]]([[569_rbac|RBAC]]), ③ 관찰성: [[342_routing_metric_hop_bandwidth_delay|메트릭]], [[112_distributed_tracing_microservices|분산 트레이싱]], 액세스 로그의 자동 수집, ④ [[571_resiliency_fault_tolerance_patterns|탄력성]]: [[307_circuit_breaker_pattern|서킷 브레이커]], 장애 주입([[751_chaos_engineering|chaos engineering]]).

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 트래픽 관리 | [[267_weight_bias_activation|가중치]] 기반 [[339_routing_overview_best_path_selection|라우팅]], 재시도, [[573_timeout_retry_backoff_strategy|타임아웃]] | VirtualService, DestinationRule |
| 보안 | [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]], [[549_jwt_json_web_token|JWT]] [[395_verification_process_review|검증]], [[569_rbac|RBAC]] | PeerAuthentication, AuthorizationPolicy |
| 관찰성 | [[342_routing_metric_hop_bandwidth_delay|메트릭]], 트레이싱 자동 수집 | [[136_prometheus|Prometheus]] + Jaeger 통합 |
| [[571_resiliency_fault_tolerance_patterns|탄력성]] | [[307_circuit_breaker_pattern|서킷 브레이커]], 장애 주입 | DestinationRule outlierDetection |

```text
┌─────────────────────────────────────────────────────────────┐
│      서비스 메시 카나리 배포 (트래픽 분할) 예시              │
├─────────────────────────────────────────────────────────────┤
│  [VirtualService 설정]                                      │
│  /api/orders → 주문 서비스 v1: 90% 가중치                   │
│              → 주문 서비스 v2: 10% 가중치 (카나리)          │
│                                                             │
│  서킷 브레이커 임계치: 5초 내 50% 에러율 초과 → 회로 열기   │
└─────────────────────────────────────────────────────────────┘
```

mTLS는 [[302_service_mesh_istio|서비스 메시]]의 핵심 보안 기능이다. 각 [[090_service_kubernetes_network_load_balancing|서비스]] [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]가 [[303_authentication_authorization_patterns|인증]]서를 갖고 [[090_service_kubernetes_network_load_balancing|서비스]] 간 통신을 암호화·[[303_authentication_authorization_patterns|인증]]하므로, 클러스터 내부에서도 [[090_service_kubernetes_network_load_balancing|서비스]] 간 통신을 도청하거나 위조할 수 없다. 이는 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]([[667_zero_trust_runtime_integrity_measurement|Zero Trust]]) 보안 모델의 구현이다.

- **📢 섹션 요약 비유**: 회사 내부에서도 건물 출입증([[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] [[303_authentication_authorization_patterns|인증]]서)이 없으면 아무 부서나 들어갈 수 없는 보안 시스템과 같다. 사내 네트워크라도 신원이 확인된 [[090_service_kubernetes_network_load_balancing|서비스]]만 통신할 수 있다.

---
## Ⅲ. 비교 및 연결

[[302_service_mesh_istio|서비스 메시]]와 [[014_api_posix|API]] 게이트웨이는 상호 보완적이지 대체 [[083_relationship_in_er_model|관계]]가 아니다. [[014_api_posix|API]] 게이트웨이는 외부-내부 경계(North-South), [[302_service_mesh_istio|서비스 메시]]는 내부 [[090_service_kubernetes_network_load_balancing|서비스]] 간(East-West) 통신을 담당한다.

| 비교 축 | A | B |
|:---|:---|:---|
| **트래픽 방향** | 외부 → 내부 (N-S) | 내부 [[090_service_kubernetes_network_load_balancing|서비스]] 간 (E-W) |
| **주 관심사** | [[303_authentication_authorization_patterns|인증]], [[339_routing_overview_best_path_selection|라우팅]], 속도 제한 | [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]], 관찰성, [[571_resiliency_fault_tolerance_patterns|탄력성]] |
| **구현 위치** | 경계 엣지 | 각 [[090_service_kubernetes_network_load_balancing|서비스]] [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] |
| **대표 도구** | Kong, NGINX, AWS [[014_api_posix|API]] GW | [[302_service_mesh_istio|Istio]], Linkerd, Consul |

[[302_service_mesh_istio|서비스 메시]] 없이 MSA를 운영하면 Resilience4j, Hystrix 같은 라이브러리를 각 [[090_service_kubernetes_network_load_balancing|서비스]]마다 통일되지 않게 적용하거나, 특정 언어에서만 사용 가능한 라이브러리의 한계에 부딪힌다. [[302_service_mesh_istio|서비스 메시]]는 언어 독립적으로 동일한 네트워크 [[164_policy|정책]]을 적용한다.

- **📢 섹션 요약 비유**: [[014_api_posix|API]] 게이트웨이가 도시의 정문 경비원이라면, [[302_service_mesh_istio|서비스 메시]]는 도시 내 각 건물 사이의 교통경찰과 보안 시스템이다. 두 역할 모두 필요하며 서로 다른 지점을 담당한다.

---
## Ⅳ. 실무 적용 및 기술사 판단

[[302_service_mesh_istio|서비스 메시]] 도입의 핵심 검토 사항은 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 오버헤드다. Envoy [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 하나당 약 50~100MB 메모리와 추가 CPU가 필요하다. [[090_service_kubernetes_network_load_balancing|서비스]] 100개라면 최소 5~10GB 추가 메모리가 필요하므로, 클러스터 사양과 비용을 사전에 계획해야 한다.

### 판단 [[435_checklist_based_testing|체크리스트]]
1. [[090_service_kubernetes_network_load_balancing|서비스]] 수가 20개 이상이고 [[090_service_kubernetes_network_load_balancing|서비스]] 간 통신 복잡성이 높은가?
2. [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] 상호 [[303_authentication_authorization_patterns|인증]]이 보안 요구사항인가?
3. [[112_distributed_tracing_microservices|분산 트레이싱]]·[[342_routing_metric_hop_bandwidth_delay|메트릭]] 수집을 비즈니스 코드 수정 없이 적용하고 싶은가?
4. [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 오버헤드를 수용할 수 있는 클러스터 자원 여유가 있는가?
5. [[615_ebpf|eBPF]] 기반 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]리스 [[389_mesh_topology|메시]]([[825_cilium_ebpf_kubernetes_networking_security|Cilium]])를 검토할 만큼 오버헤드가 문제인가?

- **📢 섹션 요약 비유**: 공장 자동화 시스템([[302_service_mesh_istio|서비스 메시]])을 도입하면 작업자([[090_service_kubernetes_network_load_balancing|서비스]])가 안전 규정을 직접 체크하지 않아도 기계가 자동으로 적용한다. 하지만 자동화 시스템 자체를 유지보수하는 비용이 발생한다.

---

## Ⅴ. 기대효과 및 결론

[[302_service_mesh_istio|서비스 메시]]를 적용하면 운영팀이 코드 변경 없이 트래픽 [[164_policy|정책]](재시도, [[573_timeout_retry_backoff_strategy|타임아웃]], [[115_canary_deployment_gradual_rollout|카나리 배포]])을 동적으로 변경할 수 있어 배포 위험이 감소한다. 모든 [[090_service_kubernetes_network_load_balancing|서비스]] 간 통신이 자동으로 암호화되어 내부 네트워크 보안이 강화된다. [[112_distributed_tracing_microservices|분산 트레이싱]]이 자동으로 수집되어 장애 원인 추적 시간이 단축된다.

한계는 운영 복잡도와 러닝 커브다. [[302_service_mesh_istio|Istio]] 같은 도구의 설정이 복잡하고, 컨트롤 플레인 장애 시 전체 [[090_service_kubernetes_network_load_balancing|서비스]] 통신에 영향을 미칠 수 있다. 최근 [[615_ebpf|eBPF]] 기술을 활용한 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]리스 [[302_service_mesh_istio|서비스 메시]]([[825_cilium_ebpf_kubernetes_networking_security|Cilium]], Ambient [[389_mesh_topology|Mesh]])가 이 한계를 해결하는 방향으로 발전하고 있다.

미래 방향으로는 ① [[615_ebpf|eBPF]] 기반 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]리스 [[389_mesh_topology|메시]]([[302_service_mesh_istio|Istio]] Ambient Mode)로 오버헤드 제거, ② [[319_webassembly_architecture|WebAssembly]] 플러그인으로 [[389_mesh_topology|메시]] 기능 확장, ③ [[190_ai_llm_requirements_specification|AI]] 기반 적응형 트래픽 [[164_policy|정책]] 자동 조정이 주목받고 있다.

[[302_service_mesh_istio|서비스 메시]]는 "네트워크를 코드에서 분리하여 인프라의 책임으로 돌리는" 현대 [[531_cloud_native_architecture|클라우드 네이티브]] 아키텍처의 핵심 인프라 패턴으로 기억해야 한다.

- **📢 섹션 요약 비유**: 건물의 전기·수도·냉난방([[302_service_mesh_istio|서비스 메시]])은 각 세입자([[090_service_kubernetes_network_load_balancing|서비스]])가 직접 관리하지 않고 건물 관리 시스템이 공통으로 제공한다. 세입자는 자신의 업무에만 집중할 수 있다.

---

### 📌 관련 개념 맵

[분산 [[090_service_kubernetes_network_load_balancing|서비스]] 네트워크 [[164_policy|정책]] 중복] → [서비스 메시] → [사이드카 패턴] → [[[302_service_mesh_istio|Istio]]] → [[[615_ebpf|eBPF]] [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]리스]

| 개념 | 연결 포인트 |
|:---|:---|
| [[182_sidecar_pattern_proxy_container|사이드카 패턴]] | [[302_service_mesh_istio|서비스 메시]]의 핵심 구현 패턴 |
| [[014_api_posix|API]] 게이트웨이 | [[302_service_mesh_istio|서비스 메시]]의 상호 보완 [[083_relationship_in_er_model|관계]] (N-S vs E-W) |
| [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] | [[302_service_mesh_istio|서비스 메시]]의 [[090_service_kubernetes_network_load_balancing|서비스]] 간 상호 암호화 [[303_authentication_authorization_patterns|인증]] |
| [[615_ebpf|eBPF]] | [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 없는 고성능 [[302_service_mesh_istio|서비스 메시]] 구현 기술 |

### 📈 관련 키워드 및 발전 흐름도

[서비스별 네트워크 코드 중복] → [사이드카 패턴] → [서비스 [[389_mesh_topology|메시]]([[302_service_mesh_istio|Istio]]·Linkerd)] → [[[615_ebpf|eBPF]] [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]리스 메시] → [Ambient [[389_mesh_topology|Mesh]]] → [[[190_ai_llm_requirements_specification|AI]] 적응형 트래픽 정책]

### 👶 어린이를 위한 3줄 비유 설명

1. 각 집([[090_service_kubernetes_network_load_balancing|서비스]])마다 보안 카메라와 잠금장치를 따로 설치하는 대신, 아파트 단지([[302_service_mesh_istio|서비스 메시]])에서 공동 보안 시스템을 제공해요.
2. 집주인(개발자)은 보안 시스템을 신경 쓰지 않고 자기 생활(비즈니스 로직)에 집중할 수 있어요.
3. 단지 관리자(컨트롤 플레인)가 모든 집의 보안 [[164_policy|정책]]을 한 곳에서 관리해요!
