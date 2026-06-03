---
title: 125. API Gateway 핵심 기능 - 라우팅·인증·Rate Limiting·변환 상세
date: '2026-04-19'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[014_api_posix|API]] Gateway의 핵심 기능은 **요청 [[339_routing_overview_best_path_selection|라우팅]](URL→[[090_service_kubernetes_network_load_balancing|서비스]] 매핑)·[[303_authentication_authorization_patterns|인증]]/[[509_authorization_models_rbac_abac|인가]]([[549_jwt_json_web_token|JWT]]·OAuth2)·[[520_rate_limiting|Rate Limiting]](과부하 방지)·[[295_protocol_field_tcp_udp_icmp|프로토콜]] 변환([[156_rest_representational_state_transfer|REST]]↔[[479_grpc_protobuf_http2|gRPC]])·응답 집계(Composition)**이다.
> 2. **가치**: 이 기능들이 없으면 모든 마이크로서비스가 **개별적으로 [[303_authentication_authorization_patterns|인증]]·로깅·Rate Limiting을 구현**해야 하지만, Gateway에서 중앙 처리하면 **코드 중복 제거·[[164_policy|정책]] [[194_consistency_database_integrity|일관성]]**이 보장된다.
> 3. **판단 포인트**: Gateway가 너무 많은 비즈니스 로직을 담으면 **"Smart Gateway" [[128_water_scrum_fall_anti_pattern|안티패턴]]**이 되므로, 인프라 관심사([[303_authentication_authorization_patterns|인증]]·[[339_routing_overview_best_path_selection|라우팅]]·로깅)만 Gateway에 두고 비즈니스 로직은 [[090_service_kubernetes_network_load_balancing|서비스]]에 유지해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    API Gateway 핵심 기능                              │
├───────────────────────────────────────────────────────┤
│  1. 라우팅: /api/orders → Order Service              │
│  2. 인증: JWT 검증, OAuth2 토큰 검사                 │
│  3. Rate Limiting: 100 req/s/user                    │
│  4. 프로토콜 변환: REST → gRPC                       │
│  5. 응답 집계: 여러 서비스 응답 합치기               │
│  6. 로깅·모니터링: 요청 추적·메트릭                  │
│  7. 캐싱: 반복 응답 캐시                              │
│  8. CORS: 크로스 도메인 허용                          │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[014_api_posix|API]] Gateway는 공항의 **보안 검색대 + 게이트 안내 + 환전소**를 합친 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[520_rate_limiting|Rate Limiting]] [[001_algorithm_definition|알고리즘]]

| [[001_algorithm_definition|알고리즘]] | 설명 |
|:---|:---|
| **Token Bucket** | 토큰 일정 속도 충전, 요청 시 소비 |
| **Leaky Bucket** | 일정 속도로만 처리 (대기열) |
| **Fixed Window** | 시간 창 내 최대 요청 수 |
| **Sliding Window** | 슬라이딩 창으로 정밀 제어 |

- **📢 섹션 요약 비유**: Token Bucket은 주유소 노즐(일정 속도 충전, 가득 차면 넘침)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[542_api_gateway|API Gateway]] | [[828_service_mesh_microservice_communication_infrastructure|Service Mesh]] |
|:---|:---|:---|
| **위치** | 외부→내부 | **내부→내부** |
| **기능** | [[303_authentication_authorization_patterns|인증]]·[[339_routing_overview_best_path_selection|라우팅]]·Rate Limit | 트래픽 관리·[[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] |
| **대상** | 외부 클라이언트 | **[[090_service_kubernetes_network_load_balancing|서비스]] 간** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Smart Gateway [[128_water_scrum_fall_anti_pattern|안티패턴]]
- ❌ Gateway에 비즈니스 로직(주문 유효성 검사 등) 배치.
- ✅ Gateway는 인프라 관심사만. 비즈니스는 [[090_service_kubernetes_network_load_balancing|서비스]]에.

---

## Ⅴ. 기대효과 및 결론

[[014_api_posix|API]] Gateway는 **MSA의 크로스커팅 관심사를 중앙 처리**하는 핵심 인프라이며, [[090_service_kubernetes_network_load_balancing|Service]] Mesh와 보완적으로 사용된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[520_rate_limiting|Rate Limiting]]** | Token Bucket / Sliding Window |
| **[[549_jwt_json_web_token|JWT]]** | Gateway에서 검증하는 [[303_authentication_authorization_patterns|인증]] 토큰 |
| **[[543_bff_backend_for_frontend|BFF]]** | 클라이언트별 맞춤 Gateway |
| **[[828_service_mesh_microservice_communication_infrastructure|Service Mesh]]** | 내부 통신 인프라 (Gateway 보완) |
| **Smart Gateway [[128_water_scrum_fall_anti_pattern|안티패턴]]** | Gateway에 비즈니스 로직 금지 |

### 📈 관련 키워드 및 발전 흐름도

```text
[리버스 프록시 (Nginx, 2000s)]
    │
    ▼
[API Gateway (Netflix Zuul, 2013~)]
    │
    ▼
[Kong / Envoy (2015~) — 클라우드 네이티브]
    │
    ▼
[API Gateway + Service Mesh (2018~)]
    │
    ▼
[현재: AI Gateway — 토큰 사용량·비용 관리 (LLM API)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[014_api_posix|API]] Gateway는 공항의 **보안 검색대**예요. 신분증([[303_authentication_authorization_patterns|인증]])을 확인하고 게이트([[090_service_kubernetes_network_load_balancing|서비스]])를 안내해요.
2. 너무 많은 사람이 한꺼번에 오면 **줄 세우기([[520_rate_limiting|Rate Limiting]])**로 혼잡을 방지해요.
3. 보안 검색대가 **공항 업무까지 하면 안 되듯**, Gateway는 **교통 정리만** 해야 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 124 / 371

← **이전**: [[124_api_gateway|124. API Gateway - MSA 외부 진입점·라우팅·인증·Rate Limiting]]
**다음**: [[126_bff|126. BFF (Backend For Frontend) - 클라이언트별 맞춤 API 레이어]] →

---
