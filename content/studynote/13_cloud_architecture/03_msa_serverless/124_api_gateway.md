---
title: "Api Gateway"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 124
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Gateway는 <strong>MSA에서 모든 외부 요청의 단일 진입점(Single Entry Point)</strong>이며, 요청 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)·[인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·[Rate Limiting](/studynote/09_security/05_web_app_security/520_rate_limiting/)·로깅·응답 캐시를 수행하는 <strong>리버스 <a href="/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/">프록시</a> + 크로스커팅 관심사 처리기</strong>이다.
> 2. **가치**: 클라이언트가 수십 개 마이크로서비스의 엔드포인트를 직접 알면 <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> URL 변경·<a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a> 중복·CORS 관리</strong>가 불가능하지만, Gateway를 통해 <strong>단일 URL(<a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">api</a>.example.com)로 모든 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>에 접근</strong>할 수 있다.
> 3. **판단 포인트**: <strong><a href="/studynote/04_software_engineering/11_testing_validation/935_bff_backend_for_frontend/">BFF</a>(<a href="/studynote/04_software_engineering/11_testing_validation/935_bff_backend_for_frontend/">Backend For Frontend</a>)</strong> 패턴과 결합하면 클라이언트별(Web/Mobile) 최적화된 API를 제공할 수 있으며, Kong·Envoy·AWS [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Gateway가 대표 도구이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    API Gateway 아키텍처                               |
+-------------------------------------------------------+
|  [Client] -> api.example.com                           |
|                |                                      |
|           [API Gateway]                               |
|            +-- 인증 (JWT 검증)                        |
|            +-- Rate Limiting (100 req/s)              |
|            +-- 라우팅 (/orders -> Order Service)      |
|            +-- 로깅·모니터링                          |
|            +-- 응답 캐시                              |
|                |                                      |
|    +-----------+-----------+                          |
|    v           v           v                          |
|  Order Svc  Payment Svc  User Svc                    |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Gateway는 호텔 프런트 데스크다. 모든 손님(요청)이 프런트(Gateway)를 거치며, 프런트가 신분 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)([인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))·방 배정([라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/))·보안([Rate Limiting](/studynote/09_security/05_web_app_security/520_rate_limiting/))을 처리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [API Gateway](/studynote/04_software_engineering/11_testing_validation/934_api_gateway/) 핵심 기능

| 기능 | 설명 |
|:---|:---|
| <strong><a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a></strong> | URL 패턴 -> [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 매핑 |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a></strong> | [JWT](/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/)/OAuth2 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| <strong><a href="/studynote/09_security/05_web_app_security/520_rate_limiting/">Rate Limiting</a></strong> | 과도한 요청 차단 |
| <strong><a href="/studynote/03_network/16_data_center_cloud/833_load_balancing_l4_l7_switch_traffic_distribution/">로드 밸런싱</a></strong> | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 인스턴스 분배 |
| **응답 캐시** | 반복 요청 [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/) |

- **📢 섹션 요약 비유**: Gateway는 공항의 보안 검색대 + 게이트 안내이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 직접 호출 | [API Gateway](/studynote/04_software_engineering/11_testing_validation/934_api_gateway/) |
|:---|:---|:---|
| **진입점** | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)마다 다름 | **단일** |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a></strong> | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)마다 구현 | **중앙 처리** |
| **CORS** | 복잡 | **Gateway에서 관리** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 대표 도구
- **Kong**: [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), 플러그인 생태계.
- <strong>Envoy <a href="/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/">Proxy</a></strong>: [CNCF](/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/), [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플레인.
- <strong>AWS <a href="/studynote/04_software_engineering/11_testing_validation/934_api_gateway/">API Gateway</a></strong>: 관리형, [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 연동.

---

## Ⅴ. 기대효과 및 결론

[API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Gateway는 <strong>MSA의 필수 인프라</strong>이며, [BFF](/studynote/04_software_engineering/11_testing_validation/935_bff_backend_for_frontend/)·[서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)와 결합하여 현대 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 아키텍처의 통신 [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) 역할을 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/04_software_engineering/11_testing_validation/934_api_gateway/">API Gateway</a></strong> | [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 단일 진입점 |
| <strong><a href="/studynote/04_software_engineering/11_testing_validation/935_bff_backend_for_frontend/">BFF</a></strong> | 클라이언트별 맞춤 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) |
| <strong><a href="/studynote/09_security/05_web_app_security/520_rate_limiting/">Rate Limiting</a></strong> | 과부하 방지 |
| <strong><a href="/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/">Service Mesh</a></strong> | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신 인프라 (보완 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)) |
| **Kong/Envoy** | 대표 [API Gateway](/studynote/04_software_engineering/11_testing_validation/934_api_gateway/) 도구 |

### 📈 관련 키워드 및 발전 흐름도

```text
[로드 밸런서 (L4/L7, 2000s)]
    |
    v
[API Gateway (Netflix Zuul, 2013~)]
    |
    v
[Kong / Envoy (2015~) — 클라우드 네이티브 Gateway]
    |
    v
[BFF Pattern (2016~) — 클라이언트별 Gateway]
    |
    v
[현재: API Gateway + Service Mesh — 통합 네트워크 계층]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Gateway는 호텔 <strong>프런트 데스크</strong>예요. 모든 손님이 프런트를 거쳐요.
2. 프런트에서 <strong>신분증 <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a>(<a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>)</strong>하고, 너무 많은 손님이 오면 <strong>대기(<a href="/studynote/09_security/05_web_app_security/520_rate_limiting/">Rate Limiting</a>)</strong>시켜요.
3. 프런트가 없으면 손님이 **직접 방을 찾아야 해서** 혼란스러워요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 123 / 371

<- **이전**: [123. SOA vs MSA 비교 - 서비스 지향 아키텍처의 진화](/studynote/13_cloud_architecture/03_msa_serverless/123_soa_vs_msa_comparison/)
**다음**: [125. API Gateway 핵심 기능 - 라우팅·인증·Rate Limiting·변환 상세](/studynote/13_cloud_architecture/03_msa_serverless/125_api_gateway_functions/) ->

---
