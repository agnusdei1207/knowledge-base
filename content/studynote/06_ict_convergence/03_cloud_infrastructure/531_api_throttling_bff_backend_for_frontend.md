+++
title = "531. API 스로틀링과 BFF 백엔드 포 프론트엔드 (API Throttling and BFF Backend For Frontend)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 스로틀링([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Throttling)은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 과부하와 남용을 막는 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 메커니즘이고, [BFF](/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/)([Backend for Frontend](/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/))는 각 클라이언트에 최적화된 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 계층을 분리하여 오버패칭(Overfetching)과 언더패칭(Underfetching)을 해결한다.
> 2. **가치**: 토큰 버킷(Token Bucket), 리키 버킷(Leaky Bucket), 슬라이딩 윈도(Sliding Window) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 각각 버스트 허용, 균일 속도, 시간 [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/)의 트레이드오프를 가진다.
> 3. **판단 포인트**: [BFF](/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/) 패턴은 클라이언트 종류가 다양(모바일/웹/[IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/))하고 각각의 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 요구사항이 다를 때 효과적이며, 그렇지 않으면 GraphQL이 더 단순한 대안이다.

---

## Ⅰ. 개요 및 필요성

<strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a> 스로틀링 필요성</strong>: 공개 API나 내부 [MSA API](/knowledge-base/studynote/15_devops_sre/05_devsecops/336_msa_api/) 모두 무제한 요청을 허용하면 서버 과부하, DDOS(Distributed Denial of [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)), 특정 클라이언트의 자원 독점이 발생한다. [Rate Limiting](/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/)(속도 제한)은 단위 시간당 요청 수를 제한하여 공정한 자원 배분과 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 안정성을 동시에 확보한다.

<strong><a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/">BFF</a> 필요성</strong>: 하나의 범용 API가 모바일, 웹, [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), TV 등 모든 클라이언트를 지원하려 하면:
- **오버패칭(Overfetching)**: 필요 없는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)까지 받아 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 낭비
- **언더패칭(Underfetching)**: 필요한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 얻기 위해 여러 번 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출
- 클라이언트별 최적화가 불가능하여 모바일 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하

- **📢 섹션 요약 비유**: 스로틀링은 수도꼭지 조절 밸브이고, BFF는 각 방에 맞는 수압과 온도를 따로 설정하는 전용 배관이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

<strong><a href="/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/">Rate Limiting</a> <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a> 비교</strong>:

```
[토큰 버킷 (Token Bucket)]
버킷에 토큰이 채워짐 -> 요청마다 토큰 소비
버킷이 비면 요청 거부 -> 버스트(순간 폭주) 허용

[리키 버킷 (Leaky Bucket)]
큐에 요청을 쌓음 -> 일정 속도로 처리
큐가 가득 차면 거부 -> 균일한 출력 속도 보장

[슬라이딩 윈도 (Sliding Window)]
최근 N초 요청 수를 실시간 집계
고정 윈도의 경계 문제 해결 -> 정확한 제한
```

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 버스트 허용 | 구현 복잡도 | [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) | 적합 사례 |
|:---|:---:|:---:|:---:|:---|
| 토큰 버킷 (Token Bucket) | ✓ | 낮음 | 중간 | [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이 기본값 |
| 리키 버킷 (Leaky Bucket) | ✗ | 낮음 | 중간 | 균일한 업스트림 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) |
| 슬라이딩 윈도 (Sliding Window) | 부분 | 높음 | 높음 | 정밀한 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 제어 |
| 고정 윈도 (Fixed Window) | 부분 | 매우 낮음 | 낮음 | 단순 구현 필요 시 |

<strong><a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/">BFF</a>(<a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/">Backend for Frontend</a>) 아키텍처</strong>:

```
클라이언트        BFF 계층               마이크로서비스
+--------+     +------------+
| 모바일  |----->| Mobile BFF |-+
+--------+     +------------+ |  +--------------+
+--------+     +------------+ +-->| 주문 서비스   |
|  웹    |----->|  Web BFF   |-+  +--------------+
+--------+     +------------+ +-->| 사용자 서비스 |
+--------+     +------------+ |  +--------------+
|  IoT   |----->|  IoT BFF   |-+  | 상품 서비스   |
+--------+     +------------+    +--------------+
```

각 BFF는 해당 클라이언트에 최적화된 집계(Aggregation), 변환(Transformation), 필터링(Filtering)을 담당한다.

- **📢 섹션 요약 비유**: BFF는 각 손님(클라이언트)에게 맞춤 메뉴를 제공하는 전담 웨이터다 — 어린이 손님에겐 단 음식, 다이어트 손님에겐 저칼로리 메뉴를 따로 준비한다.

---

## Ⅲ. 비교 및 연결

<strong><a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/">BFF</a> vs <a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/246_graphql_query_language_overfetching_solution/">GraphQL</a></strong>:

| 구분 | [BFF](/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/) | [GraphQL](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/246_graphql_query_language_overfetching_solution/) |
|:---|:---|:---|
| 유연성 | 클라이언트별 완전 최적화 | 단일 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)로 유연한 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| 서버 복잡성 | [BFF](/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수만큼 증가 | 단일 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 유지 |
| 타입 안전성 | 언어 종속 | SDL [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)로 타입 보장 |
| N+1 문제 | BFF에서 사전 집계로 해결 | DataLoader 패턴 필요 |
| 적합 상황 | 클라이언트 종류 다양, 팀 분리 | 다양한 클라이언트, 중앙 집중 선호 |

<strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a> <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/317_versioning_data_model_design/">버저닝</a> <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>:
- URI [버저닝](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/317_versioning_data_model_design/): `/v1/users`, `/v2/users` — 명확하지만 URL 중복
- 헤더 [버저닝](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/317_versioning_data_model_design/): `API-Version: 2` — URL 깔끔하지만 [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/) 복잡
- 콘텐츠 협상: `Accept: application/vnd.api+json;version=2` — RESTful하지만 구현 복잡

- **📢 섹션 요약 비유**: GraphQL은 뷔페처럼 먹고 싶은 것을 원하는 만큼 가져올 수 있지만, BFF는 각 손님의 입맛을 미리 파악해 최적 정식을 차려주는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**기술사 시험 판단 포인트**:
1. 세 가지 [Rate Limiting](/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 트레이드오프(버스트 허용, 구현 복잡도, [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/))를 표로 비교한다.
2. [BFF](/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/) 도입 근거를 "오버패칭/언더패칭"과 "클라이언트별 팀 독립 개발"로 정당화한다.
3. Redis를 이용한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [Rate Limiting](/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/) 구현(슬라이딩 윈도, Lua 스크립트 원자 연산)을 언급하면 깊이를 인정받는다.

**실무 시나리오**: 이커머스 모바일 앱 — 상품 목록 화면에서 상품 기본 정보 + 리뷰 수 + 재고 여부를 하나의 API로 제공해야 할 때, 범용 API는 3개 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 각각 호출해야 하지만, Mobile BFF가 서버 측에서 집계하여 단일 최적화 응답 반환. 모바일 네트워크 요청 수 66% 감소.

- **📢 섹션 요약 비유**: [BFF](/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/) 집계는 배달 대행 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 여러 식당에서 음식을 대신 픽업해 한 번에 배달하는 것이다 — 손님은 한 번만 문을 열면 된다.

---

## Ⅴ. 기대효과 및 결론

[API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 스로틀링과 [BFF](/knowledge-base/studynote/04_software_engineering/11_testing_validation/543_bff_backend_for_frontend/) 패턴을 적용하면:
- <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 안정성</strong>: Rate Limiting으로 과부하, 남용, DDOS 부분 방어
- <strong>클라이언트 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong>: BFF로 오버패칭 제거, 모바일 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사용량 감소
- **팀 독립성**: 각 클라이언트 팀이 자체 BFF를 소유하여 독립 배포
- <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a> 수명</strong>: [버저닝](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/317_versioning_data_model_design/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 하위 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 유지하며 점진적 발전

[API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 설계는 기능 구현만큼이나 <strong>클라이언트 경험과 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> <a href="/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a></strong>를 함께 고려해야 한다.

- **📢 섹션 요약 비유**: 스로틀링과 BFF는 고속도로 설계의 두 축이다 — 스로틀링은 과속 방지 카메라([보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)), BFF는 클라이언트별 맞춤 출구 램프(최적화)다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/) | [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)/[인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/), [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), 로드밸런싱 · 505 |
| [GraphQL](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/246_graphql_query_language_overfetching_solution/) | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/), 리졸버, N+1 문제 · 505 |
| [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 캐시, 슬라이딩 윈도 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) · 506 |
| [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) ([Microservice Architecture](/knowledge-base/studynote/07_enterprise_systems/06_exam_summary/365_msa_microservice_architecture/)) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 집계, 팀 독립 · 505 |
| DDOS ([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [서비스 거부 공격](/knowledge-base/studynote/03_network/19_frequent_topics_terms/989_dos_denial_of_service/)) | [Rate Limiting](/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/), [WAF](/knowledge-base/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/), [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) · 508 |

### 📈 관련 키워드 및 발전 흐름도

```text
[인증 · 인가] -> [API 스로틀링과 BFF 백엔드 포 프론트엔드] -> [Rate Limiting · WAF]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 스로틀링은 놀이공원 입장 줄처럼, 한 번에 너무 많은 사람이 들어오면 잠깐 기다리게 해서 놀이기구(서버)가 고장 나지 않게 해요.
2. BFF는 각 반마다 다른 급식 메뉴를 제공하는 급식 담당 선생님이에요 — 운동부는 많이, 다이어트 반은 적게.
3. 오버패칭은 도시락에 필요 없는 음식이 가득 담긴 것처럼, BFF가 딱 맞는 양만 담아주면 배낭([대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/))이 가벼워져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 531 / 552

<- **이전**: [530. 지식 그래프 기반 검색 증강 생성 (GraphRAG)](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/530_graph_rag/)
**다음**: [532. DPO 직접 선호 최적화 (DPO Direct Preference Optimization)](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/532_dpo_direct_preference_optimization/) ->

---
