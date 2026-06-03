+++
weight = 124
title = "124. API Gateway - MSA 외부 진입점·라우팅·인증·Rate Limiting"
date = "2026-04-19"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[014_api_posix|API]] Gateway는 **MSA에서 모든 외부 요청의 단일 진입점(Single Entry Point)**이며, 요청 [[339_routing_overview_best_path_selection|라우팅]]·[[303_authentication_authorization_patterns|인증]]·[[520_rate_limiting|Rate Limiting]]·로깅·응답 캐시를 수행하는 **리버스 [[264_proxy_pattern_surrogate_access_control|프록시]] + 크로스커팅 관심사 처리기**이다.
> 2. **가치**: 클라이언트가 수십 개 마이크로서비스의 엔드포인트를 직접 알면 **[[090_service_kubernetes_network_load_balancing|서비스]] URL 변경·[[303_authentication_authorization_patterns|인증]] 중복·CORS 관리**가 불가능하지만, Gateway를 통해 **단일 URL([[014_api_posix|api]].example.com)로 모든 [[090_service_kubernetes_network_load_balancing|서비스]]에 접근**할 수 있다.
> 3. **판단 포인트**: **[[543_bff_backend_for_frontend|BFF]]([[543_bff_backend_for_frontend|Backend For Frontend]])** 패턴과 결합하면 클라이언트별(Web/Mobile) 최적화된 API를 제공할 수 있으며, Kong·Envoy·AWS [[014_api_posix|API]] Gateway가 대표 도구이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    API Gateway 아키텍처                               │
├───────────────────────────────────────────────────────┤
│  [Client] → api.example.com                           │
│                │                                      │
│           [API Gateway]                               │
│            ├── 인증 (JWT 검증)                        │
│            ├── Rate Limiting (100 req/s)              │
│            ├── 라우팅 (/orders → Order Service)      │
│            ├── 로깅·모니터링                          │
│            └── 응답 캐시                              │
│                │                                      │
│    ┌───────────┼───────────┐                          │
│    ▼           ▼           ▼                          │
│  Order Svc  Payment Svc  User Svc                    │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[014_api_posix|API]] Gateway는 호텔 프런트 데스크다. 모든 손님(요청)이 프런트(Gateway)를 거치며, 프런트가 신분 [[396_validation|확인]]([[303_authentication_authorization_patterns|인증]])·방 배정([[339_routing_overview_best_path_selection|라우팅]])·보안([[520_rate_limiting|Rate Limiting]])을 처리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[542_api_gateway|API Gateway]] 핵심 기능

| 기능 | 설명 |
|:---|:---|
| **[[339_routing_overview_best_path_selection|라우팅]]** | URL 패턴 → [[090_service_kubernetes_network_load_balancing|서비스]] 매핑 |
| **[[303_authentication_authorization_patterns|인증]]** | [[549_jwt_json_web_token|JWT]]/OAuth2 [[395_verification_process_review|검증]] |
| **[[520_rate_limiting|Rate Limiting]]** | 과도한 요청 차단 |
| **[[833_load_balancing_l4_l7_switch_traffic_distribution|로드 밸런싱]]** | [[090_service_kubernetes_network_load_balancing|서비스]] 인스턴스 분배 |
| **응답 캐시** | 반복 요청 [[456_caching|캐싱]] |

- **📢 섹션 요약 비유**: Gateway는 공항의 보안 검색대 + 게이트 안내이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 직접 호출 | [[542_api_gateway|API Gateway]] |
|:---|:---|:---|
| **진입점** | [[090_service_kubernetes_network_load_balancing|서비스]]마다 다름 | **단일** |
| **[[303_authentication_authorization_patterns|인증]]** | [[090_service_kubernetes_network_load_balancing|서비스]]마다 구현 | **중앙 처리** |
| **CORS** | 복잡 | **Gateway에서 관리** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 대표 도구
- **Kong**: [[191_oss_license_compliance|오픈소스]], 플러그인 생태계.
- **Envoy [[264_proxy_pattern_surrogate_access_control|Proxy]]**: [[190_cncf_landscape_observability|CNCF]], [[302_service_mesh_istio|서비스 메시]] [[001_dikw_pyramid|데이터]] 플레인.
- **AWS [[542_api_gateway|API Gateway]]**: 관리형, [[216_lambda_kappa_architecture_batch_realtime|Lambda]] 연동.

---

## Ⅴ. 기대효과 및 결론

[[014_api_posix|API]] Gateway는 **MSA의 필수 인프라**이며, [[543_bff_backend_for_frontend|BFF]]·[[302_service_mesh_istio|서비스 메시]]와 결합하여 현대 [[531_cloud_native_architecture|클라우드 네이티브]] 아키텍처의 통신 [[152_hub_dummy_switching_intelligent|허브]] 역할을 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[542_api_gateway|API Gateway]]** | [[619_msa_traffic_hardware|MSA]] 단일 진입점 |
| **[[543_bff_backend_for_frontend|BFF]]** | 클라이언트별 맞춤 [[014_api_posix|API]] |
| **[[520_rate_limiting|Rate Limiting]]** | 과부하 방지 |
| **[[828_service_mesh_microservice_communication_infrastructure|Service Mesh]]** | [[090_service_kubernetes_network_load_balancing|서비스]] 간 통신 인프라 (보완 [[083_relationship_in_er_model|관계]]) |
| **Kong/Envoy** | 대표 [[542_api_gateway|API Gateway]] 도구 |

### 📈 관련 키워드 및 발전 흐름도

```text
[로드 밸런서 (L4/L7, 2000s)]
    │
    ▼
[API Gateway (Netflix Zuul, 2013~)]
    │
    ▼
[Kong / Envoy (2015~) — 클라우드 네이티브 Gateway]
    │
    ▼
[BFF Pattern (2016~) — 클라이언트별 Gateway]
    │
    ▼
[현재: API Gateway + Service Mesh — 통합 네트워크 계층]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[014_api_posix|API]] Gateway는 호텔 **프런트 데스크**예요. 모든 손님이 프런트를 거쳐요.
2. 프런트에서 **신분증 [[396_validation|확인]]([[303_authentication_authorization_patterns|인증]])**하고, 너무 많은 손님이 오면 **대기([[520_rate_limiting|Rate Limiting]])**시켜요.
3. 프런트가 없으면 손님이 **직접 방을 찾아야 해서** 혼란스러워요!
