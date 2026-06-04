+++
title = "125. API Gateway 핵심 기능 - 라우팅·인증·Rate Limiting·변환 상세"
date = 2026-04-19

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Gateway의 핵심 기능은 <strong>요청 <a href="/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a>(URL-><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 매핑)·<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>/<a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">인가</a>(<a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/">JWT</a>·OAuth2)·<a href="/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/">Rate Limiting</a>(과부하 방지)·<a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> 변환(<a href="/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/">REST</a>↔<a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/">gRPC</a>)·응답 집계(Composition)</strong>이다.
> 2. **가치**: 이 기능들이 없으면 모든 마이크로서비스가 <strong>개별적으로 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>·로깅·Rate Limiting을 구현</strong>해야 하지만, Gateway에서 중앙 처리하면 <strong>코드 중복 제거·<a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a> <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a></strong>이 보장된다.
> 3. **판단 포인트**: Gateway가 너무 많은 비즈니스 로직을 담으면 <strong>"Smart Gateway" <a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>이 되므로, 인프라 관심사([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·[라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)·로깅)만 Gateway에 두고 비즈니스 로직은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 유지해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    API Gateway 핵심 기능                              |
+-------------------------------------------------------+
|  1. 라우팅: /api/orders -> Order Service              |
|  2. 인증: JWT 검증, OAuth2 토큰 검사                 |
|  3. Rate Limiting: 100 req/s/user                    |
|  4. 프로토콜 변환: REST -> gRPC                       |
|  5. 응답 집계: 여러 서비스 응답 합치기               |
|  6. 로깅·모니터링: 요청 추적·메트릭                  |
|  7. 캐싱: 반복 응답 캐시                              |
|  8. CORS: 크로스 도메인 허용                          |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Gateway는 공항의 <strong>보안 검색대 + 게이트 안내 + 환전소</strong>를 합친 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [Rate Limiting](/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 설명 |
|:---|:---|
| **Token Bucket** | 토큰 일정 속도 충전, 요청 시 소비 |
| **Leaky Bucket** | 일정 속도로만 처리 (대기열) |
| **Fixed Window** | 시간 창 내 최대 요청 수 |
| **Sliding Window** | 슬라이딩 창으로 정밀 제어 |

- **📢 섹션 요약 비유**: Token Bucket은 주유소 노즐(일정 속도 충전, 가득 차면 넘침)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/) | [Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/) |
|:---|:---|:---|
| **위치** | 외부->내부 | **내부->내부** |
| **기능** | [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·[라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)·Rate Limit | 트래픽 관리·[mTLS](/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/) |
| **대상** | 외부 클라이언트 | <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 간</strong> |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Smart Gateway [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- ❌ Gateway에 비즈니스 로직(주문 유효성 검사 등) 배치.
- ✅ Gateway는 인프라 관심사만. 비즈니스는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에.

---

## Ⅴ. 기대효과 및 결론

[API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Gateway는 <strong>MSA의 크로스커팅 관심사를 중앙 처리</strong>하는 핵심 인프라이며, [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Mesh와 보완적으로 사용된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/">Rate Limiting</a></strong> | Token Bucket / Sliding Window |
| <strong><a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/">JWT</a></strong> | Gateway에서 검증하는 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 토큰 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/">BFF</a></strong> | 클라이언트별 맞춤 Gateway |
| <strong><a href="/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/">Service Mesh</a></strong> | 내부 통신 인프라 (Gateway 보완) |
| <strong>Smart Gateway <a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong> | Gateway에 비즈니스 로직 금지 |

### 📈 관련 키워드 및 발전 흐름도

```text
[리버스 프록시 (Nginx, 2000s)]
    |
    v
[API Gateway (Netflix Zuul, 2013~)]
    |
    v
[Kong / Envoy (2015~) — 클라우드 네이티브]
    |
    v
[API Gateway + Service Mesh (2018~)]
    |
    v
[현재: AI Gateway — 토큰 사용량·비용 관리 (LLM API)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Gateway는 공항의 <strong>보안 검색대</strong>예요. 신분증([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))을 확인하고 게이트([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))를 안내해요.
2. 너무 많은 사람이 한꺼번에 오면 <strong>줄 세우기(<a href="/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/">Rate Limiting</a>)</strong>로 혼잡을 방지해요.
3. 보안 검색대가 **공항 업무까지 하면 안 되듯**, Gateway는 **교통 정리만** 해야 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 124 / 371

<- **이전**: [124. API Gateway - MSA 외부 진입점·라우팅·인증·Rate Limiting](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/124_api_gateway/)
**다음**: [126. BFF (Backend For Frontend) - 클라이언트별 맞춤 API 레이어](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/126_bff/) ->

---
