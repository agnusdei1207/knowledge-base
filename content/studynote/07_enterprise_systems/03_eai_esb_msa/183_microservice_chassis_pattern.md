---
title: 183. 마이크로서비스 샤시 (Microservice Chassis) - 공통 뼈대 패턴
date: '2026-05-06'
tags:
- studynote-enterprise
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[532_microservices_decomposition_patterns|마이크로서비스]] 샤시 ([[141_microservice_chassis|Microservice Chassis]])는 [[213_msa_microservices_architecture|마이크로서비스 아키텍처]] ([[365_msa_microservice_architecture|Microservice Architecture]], [[619_msa_traffic_hardware|MSA]])에서 로깅, [[342_routing_metric_hop_bandwidth_delay|메트릭]], [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]], [[009_config|설정]] 바인딩, 헬스 체크 같은 횡단 관심사를 [[090_service_kubernetes_network_load_balancing|서비스]] 코드 안의 공통 프레임워크로 묶어 주는 **인프로세스 표준 뼈대**다.
> 2. **가치**: [[090_service_kubernetes_network_load_balancing|서비스]]마다 반복되던 보일러플레이트를 줄이고 운영 표준을 강제해, 새로운 [[090_service_kubernetes_network_load_balancing|서비스]]를 더 빨리 띄우면서도 관측성·보안·[[009_config|설정]] 방식의 [[194_consistency_database_integrity|일관성]]을 확보할 수 있다.
> 3. **판단 포인트**: 애플리케이션 코드와 강하게 결합된 공통 기능에는 적합하지만, 네트워크 [[164_policy|정책]]이나 언어 독립성이 더 중요한 기능까지 모두 샤시에 넣으면 무거운 플랫폼 락인과 업그레이드 비용만 커진다.

---

## Ⅰ. 개요 및 필요성

[[532_microservices_decomposition_patterns|마이크로서비스]] 샤시는 여러 [[090_service_kubernetes_network_load_balancing|서비스]]가 공통으로 가져야 할 비기능 코드를 하나의 재사용 가능한 뼈대로 제공하는 패턴이다. 자동차의 샤시가 엔진과 바퀴가 올라갈 공통 기반을 제공하듯, [[532_microservices_decomposition_patterns|마이크로서비스]]에서도 [[090_service_kubernetes_network_load_balancing|서비스]]가 뜨기 위해 필요한 로깅, [[009_config|설정]], 예외 처리, 헬스 체크, 추적 연동 같은 기본 구조를 미리 넣어 둔다. 핵심은 "템플릿 [[501_file_definition_logical_record|파일]] 복사"가 아니라 **운영 표준이 포함된 코드 기반**이라는 점이다.

이 패턴이 필요한 이유는 MSA가 [[090_service_kubernetes_network_load_balancing|서비스]] 수를 늘리기 때문이다. [[090_service_kubernetes_network_load_balancing|서비스]]가 5개일 때는 각 팀이 공통 기능을 직접 넣어도 버틸 수 있지만, 수십·수백 개로 늘어나면 팀마다 [[568_logs_distributed_logging_elk_fluentd|로그]] 포맷과 [[342_routing_metric_hop_bandwidth_delay|메트릭]] 이름, [[009_config|설정]] 로딩 방식이 달라져 운영 복잡도가 폭발한다. 비즈니스 기능은 작아졌는데, [[090_service_kubernetes_network_load_balancing|서비스]] 시작을 위한 준비 코드가 오히려 더 비슷하게 반복되는 상황이 생긴다.

플랫폼 팀이 샤시를 제공하면 각 [[090_service_kubernetes_network_load_balancing|서비스]] 팀은 비즈니스 규칙에 집중하고, 조직은 관측성과 기본 보안, [[009_config|설정]] 규약을 일관되게 가져갈 수 있다. 즉 샤시는 개발 생산성 도구이면서 동시에 아키텍처 거버넌스 도구다.

아래 그림은 샤시가 왜 "중복 제거 이상의 의미"를 가지는지 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Without chassis vs with chassis                                   │
├────────────────────────────────────────────────────────────────────┤
│ Service A : biz + log + trace + config + health                   │
│ Service B : biz + log + trace + config + health                   │
│ Service C : biz + log + trace + config + health                   │
│                                                                    │
│ With chassis :                                                     │
│   shared chassis -> log / metrics / tracing / config / health     │
│   each service  -> business capability only                       │
└────────────────────────────────────────────────────────────────────┘
```

이 구조의 가치는 단순한 코드 절감이 아니다. 새 [[090_service_kubernetes_network_load_balancing|서비스]]를 만들 때마다 같은 방식으로 관측과 [[009_config|설정]], 기본 보안을 확보할 수 있으므로, 운영팀 입장에서도 [[090_service_kubernetes_network_load_balancing|서비스]] 수가 늘어도 관리 방식이 크게 흔들리지 않는다.

- **📢 섹션 요약 비유**: [[532_microservices_decomposition_patterns|마이크로서비스]] 샤시는 새 가게를 열 때마다 전기 배선과 계산대, CCTV를 처음부터 직접 설치하지 않도록, 이미 기본 설비가 갖춰진 표준 매장을 제공하는 것과 같다. 점주는 진열과 상품 구성에 집중하면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

샤시는 보통 [[336_library_vs_framework|라이브러리]], 스타터 패키지, 내부 프레임워크 형태로 [[090_service_kubernetes_network_load_balancing|서비스]] 프로세스 안에 포함된다. 그래서 요청 [[033_context|컨텍스트]], 예외, 애플리케이션 생명주기에 직접 접근할 수 있다. 이 점이 [[264_proxy_pattern_surrogate_access_control|프록시]]나 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]처럼 프로세스 밖에서 동작하는 방식과 가장 크게 다른 부분이다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ In-process composition of a chassis                               │
├────────────────────────────────────────────────────────────────────┤
│ Business endpoint / domain logic                                  │
│        │                                                          │
│        ▼                                                          │
│ Chassis layer                                                     │
│   ├─ bootstrapping & dependency wiring                            │
│   ├─ structured logging / metrics / trace context                 │
│   ├─ config binding / secrets integration                         │
│   ├─ resilience policy / client wrapper                           │
│   └─ health check / graceful shutdown                             │
│        │                                                          │
│        ▼                                                          │
│ Language runtime + framework + platform SDK                       │
└────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 부트스트랩 스타터 | [[090_service_kubernetes_network_load_balancing|서비스]] 시작 시 기본 빈 구성, 공통 필터, 예외 처리 연결 | 최소 [[009_config|설정]]으로 시작되되, 필요 시 확장 가능해야 함 |
| 관측성 [[192_module_independence|모듈]] | 구조화 [[568_logs_distributed_logging_elk_fluentd|로그]], [[342_routing_metric_hop_bandwidth_delay|메트릭]], [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] [[033_context|컨텍스트]] 연동 | 팀마다 다른 포맷이 나오지 않도록 기본 규약이 중요 |
| [[009_config|설정]] [[192_module_independence|모듈]] | 외부 [[009_config|설정]] 서버, 비밀값, [[156_environment_variables|환경 변수]] 바인딩 | [[090_service_kubernetes_network_load_balancing|서비스]]별 차이를 허용하되, 읽는 방식은 표준화해야 함 |
| 복원력 [[192_module_independence|모듈]] | 재시도, [[573_timeout_retry_backoff_strategy|타임아웃]], [[171_fallback_resilience_pattern|폴백]] 래퍼 제공 | 네트워크 [[164_policy|정책]]과 중복되지 않도록 경계를 분명히 해야 함 |
| 보안/[[033_context|컨텍스트]] [[192_module_independence|모듈]] | [[303_authentication_authorization_patterns|인증]] 토큰 파싱, 공통 헤더 처리, [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]] 연결 | [[064_relation_domain|도메인]] 규칙을 섞지 않고 공통 규약만 제공해야 함 |
| 테스트 지원 | 기본 테스트 [[331_neuromorphic_ai_db|슬라이스]], [[399_mock_object|목 객체]], 헬스 체크 [[395_verification_process_review|검증]] | 샤시 [[288_version_ihl_tos_total_length|버전]] 업 시 [[090_service_kubernetes_network_load_balancing|서비스]] 회귀 [[395_verification_process_review|검증]]을 쉽게 만들어야 함 |

대표 형태로는 Spring Boot Starter, Micronaut 기반 공통 [[192_module_independence|모듈]], Go [[090_service_kubernetes_network_load_balancing|서비스]]용 내부 툴킷이 있다. 중요한 것은 특정 프레임워크 이름이 아니라, 샤시가 **[[090_service_kubernetes_network_load_balancing|서비스]]마다 반복되는 인프라 접합 코드를 재사용 가능한 계약으로 바꾼다**는 점이다.

다만 샤시는 어디까지나 인프로세스 방식이다. [[090_service_kubernetes_network_load_balancing|서비스]] 코드와 같은 프로세스 안에 있으므로 프레임워크 [[288_version_ihl_tos_total_length|버전]], 런타임, 예외 체계의 영향을 받는다. 이 덕분에 깊은 통합이 가능하지만, 동시에 언어별로 별도 샤시가 필요하거나 [[288_version_ihl_tos_total_length|버전]] [[344_compatibility_usability|호환성]] 관리가 어려워질 수 있다.

- **📢 섹션 요약 비유**: 샤시는 건물 외벽에 붙는 장비가 아니라 건물 안쪽 전기배선과 배관 같은 것이다. 바깥에서 보이지는 않지만, 한 번 공통 규격으로 깔아 두면 방마다 같은 방식으로 전기와 물을 쓸 수 있다.

---

## Ⅲ. 비교 및 연결

[[532_microservices_decomposition_patterns|마이크로서비스]] 샤시를 제대로 이해하려면 비슷해 보이는 다른 패턴과 경계를 나눠야 한다. 프로젝트 템플릿은 처음 [[087_process_state_transition|생성]]할 때 [[501_file_definition_logical_record|파일]]을 복사해 주는 수준이고, 샤시는 [[090_service_kubernetes_network_load_balancing|서비스]]가 실행되는 동안 계속 동작하는 공통 코드다. [[182_sidecar_pattern_proxy_container|사이드카 패턴]]은 프로세스 밖에서 보조 기능을 제공하고, [[302_service_mesh_istio|서비스 메시]]는 네트워크 계층 [[164_policy|정책]]을 대규모로 통제한다. 즉 모두 "공통 기능"을 다루지만 위치와 책임이 다르다.

| 방식 | 동작 위치 | 강한 지점 | 약한 지점 |
| :--- | :--- | :--- | :--- |
| 프로젝트 템플릿 | [[087_process_state_transition|생성]] 시점 1회 | 빠른 시작, [[501_file_definition_logical_record|파일]] 구조 표준화 | 시간이 지나면 복사본이 분기되어 중앙 개선이 어려움 |
| [[532_microservices_decomposition_patterns|마이크로서비스]] 샤시 | [[090_service_kubernetes_network_load_balancing|서비스]] 프로세스 내부 | 코드와 깊게 결합된 [[009_config|설정]]·로깅·예외 처리 표준화 | 언어/프레임워크 종속, [[288_version_ihl_tos_total_length|버전]] [[344_compatibility_usability|호환성]] 부담 |
| [[182_sidecar_pattern_proxy_container|사이드카 패턴]] ([[182_sidecar_pattern_proxy_container|Sidecar Pattern]]) | [[090_service_kubernetes_network_load_balancing|서비스]] 옆 별도 프로세스/[[561_container_based_deployment|컨테이너]] | 언어 독립적 [[264_proxy_pattern_surrogate_access_control|프록시]], 보조 기능 분리 | 인스턴스당 자원 오버헤드, 코드 내부 훅은 제한 |
| [[302_service_mesh_istio|서비스 메시]] ([[828_service_mesh_microservice_communication_infrastructure|Service Mesh]]) | 네트워크 [[001_dikw_pyramid|데이터]] 플레인과 제어 플레인 | 트래픽 [[164_policy|정책]], [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]], [[339_routing_overview_best_path_selection|라우팅]] [[194_consistency_database_integrity|일관성]] | 애플리케이션 내부 예외/[[033_context|컨텍스트]] 처리는 어려움 |

이 비교가 중요한 이유는 모든 횡단 관심사를 샤시에 넣을 필요가 없기 때문이다. 예를 들어 [[461_http_stateless_connection_oriented|HTTP]] 재시도 [[164_policy|정책]]과 [[694_thread_local_storage_tls|TLS]] 강제, [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[339_routing_overview_best_path_selection|라우팅]]처럼 네트워크 중심 기능은 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]나 [[302_service_mesh_istio|서비스 메시]]로 분리하는 편이 더 자연스럽다. 반면 애플리케이션 예외를 어떤 [[568_logs_distributed_logging_elk_fluentd|로그]] 구조로 남길지, 요청별 상관관계 [[289_identification_flags_fragmentation_offset|식별자]]를 [[090_service_kubernetes_network_load_balancing|서비스]] 내부 코드에 어떻게 전달할지는 샤시가 훨씬 잘 다룬다.

외부화된 [[009_config|설정]] ([[544_externalized_configuration|Externalized Configuration]])과의 [[083_relationship_in_er_model|관계]]도 자주 나온다. [[009_config|설정]] 저장소 자체는 별도 시스템일 수 있지만, [[090_service_kubernetes_network_load_balancing|서비스]]가 그 [[009_config|설정]]을 읽고 바인딩하는 공통 코드는 샤시에 포함되기 쉽다. 즉 샤시는 플랫폼 기능을 직접 모두 구현하기보다는, 외부 플랫폼과 [[090_service_kubernetes_network_load_balancing|서비스]] 코드를 연결하는 접착층 역할을 한다.

- **📢 섹션 요약 비유**: 샤시는 건물 안 전기배선이고, [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]는 건물 옆 발전기이며, [[302_service_mesh_istio|서비스 메시]]는 도시 전체 전력망 관제센터에 가깝다. 셋 다 전기를 안정적으로 쓰게 해 주지만, 어디에 설치되고 무엇을 제어하는지는 서로 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 샤시는 [[090_service_kubernetes_network_load_balancing|서비스]] 수가 많고, 같은 언어 [[057_stack|스택]]을 공유하며, 관측성과 [[009_config|설정]] 방식의 표준화가 중요한 조직에서 특히 효과적이다. 새 [[090_service_kubernetes_network_load_balancing|서비스]]가 생길 때마다 헬스 체크, 구조화 [[568_logs_distributed_logging_elk_fluentd|로그]], [[342_routing_metric_hop_bandwidth_delay|메트릭]] 태그, 공통 예외 응답, [[009_config|설정]] 바인딩을 다시 만들지 않아도 되기 때문이다. 온보딩 속도도 빨라지고 운영 표준도 덜 흔들린다.

그러나 샤시가 무거워지면 오히려 조직 전체를 느리게 만들 수 있다. 모든 [[090_service_kubernetes_network_load_balancing|서비스]]에 쓰지 않는 [[002_database_definition|데이터베이스]] 드라이버와 [[389_mesh_topology|메시]]징 [[336_library_vs_framework|라이브러리]], 과도한 자동 [[009_config|설정]]을 묶어 넣으면 시작 시간과 의존성 충돌이 늘어난다. 또한 샤시 [[288_version_ihl_tos_total_length|버전]] 하나를 올리기 위해 수십 개 [[090_service_kubernetes_network_load_balancing|서비스]]가 동시에 수정되어야 한다면, 생산성 도구가 아니라 중앙 병목이 된다.

아래 흐름은 어떤 공통 기능을 샤시에 둘지 판단하는 기준을 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Decide where a common concern should live                         │
├────────────────────────────────────────────────────────────────────┤
│ Need request context / exception / framework hook?                │
│        ├─ Yes ─▶ Chassis                                           │
│        └─ No                                                      │
│             │                                                     │
│             ▼                                                     │
│ Is it mostly network policy or traffic control?                   │
│        ├─ Yes ─▶ Sidecar / Service Mesh                           │
│        └─ No                                                      │
│             │                                                     │
│             ▼                                                     │
│ Is it only for project creation once?                             │
│        ├─ Yes ─▶ Template / Scaffold                              │
│        └─ No  ─▶ Reconsider platform boundary                     │
└────────────────────────────────────────────────────────────────────┘
```

### 기술사 판단 [[435_checklist_based_testing|체크리스트]]

1. 조직이 공통 언어·프레임워크 [[057_stack|스택]]을 충분히 공유하고 있는가?
2. 넣으려는 기능이 진짜 횡단 관심사이며 여러 [[090_service_kubernetes_network_load_balancing|서비스]]에서 반복되는가?
3. 샤시 업그레이드를 안전하게 배포할 [[288_version_ihl_tos_total_length|버전]] [[164_policy|정책]]과 [[344_compatibility_usability|호환성]] [[268_strategy_pattern|전략]]이 있는가?
4. 기능을 선택적으로 켜고 끌 수 있어 [[090_service_kubernetes_network_load_balancing|서비스]]별 과적재를 피할 수 있는가?
5. 네트워크 [[164_policy|정책]], [[303_authentication_authorization_patterns|인증]]서, [[339_routing_overview_best_path_selection|라우팅]]처럼 프로세스 밖이 더 적절한 기능을 억지로 넣고 있지 않은가?

### 자주 나오는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 샤시 안에 비즈니스 규칙까지 넣어 공통 코드가 아니라 공통 업무를 강제하는 경우
- 모든 [[090_service_kubernetes_network_load_balancing|서비스]]에 동일한 무거운 의존성을 주입해 경량 [[090_service_kubernetes_network_load_balancing|서비스]]까지 비대하게 만드는 경우
- 자동 [[009_config|설정]]이 너무 많아 [[090_service_kubernetes_network_load_balancing|서비스]] 팀이 동작 원리를 이해하지 못하는 경우
- 작은 변경에도 전 [[090_service_kubernetes_network_load_balancing|서비스]] 동시 업그레이드를 요구해 배포 병목을 만드는 경우

기술사 답안에서는 "공통 프레임워크"라는 표현만으로는 부족하다. **인프로세스 표준화의 장점, [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]·[[302_service_mesh_istio|서비스 메시]]와의 역할 분담, [[288_version_ihl_tos_total_length|버전]] 관리와 락인 위험**까지 함께 설명해야 실제 플랫폼 설계 논의가 된다.

- **📢 섹션 요약 비유**: 학교에서 모든 교실에 같은 전기 규격과 방송 설비를 넣어 두면 운영은 쉬워지지만, 교실마다 필요 없는 장비까지 억지로 깔면 공간만 좁아진다. 샤시도 필요한 공통 설비만 얇게 넣을수록 오래 간다.

---

## Ⅴ. 기대효과 및 결론

샤시가 잘 설계되면 [[090_service_kubernetes_network_load_balancing|서비스]] [[087_process_state_transition|생성]] 속도, 운영 [[194_consistency_database_integrity|일관성]], 장애 분석 가능성이 함께 좋아진다. [[090_service_kubernetes_network_load_balancing|서비스]] 팀은 본질적인 비즈니스 로직에 더 빨리 집중할 수 있고, 플랫폼 팀은 [[568_logs_distributed_logging_elk_fluentd|로그]] 형식, [[342_routing_metric_hop_bandwidth_delay|메트릭]] 규약, [[009_config|설정]] 바인딩 같은 공통 기반을 중앙에서 개선할 수 있다. 즉 샤시는 개발 생산성과 운영 표준화를 동시에 잡는 패턴이다.

하지만 한계도 분명하다. 특정 프레임워크와 언어에 깊게 결합되므로 다언어 조직에서는 여러 샤시를 유지해야 할 수 있고, 잘못 설계하면 플랫폼 의존성과 업그레이드 비용이 커진다. 그래서 최근에는 "얇은 샤시 + 외부 플랫폼 [[090_service_kubernetes_network_load_balancing|서비스]] + [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]/[[302_service_mesh_istio|서비스 메시]]"처럼 역할을 나누는 하이브리드 접근이 많다.

결론적으로 [[532_microservices_decomposition_patterns|마이크로서비스]] 샤시는 "[[090_service_kubernetes_network_load_balancing|서비스]]를 빨리 만드는 템플릿"을 넘어, **[[090_service_kubernetes_network_load_balancing|서비스]] 안쪽에서 공통 운영 규약을 실행시키는 표준 뼈대**로 기억하는 것이 맞다. 코드 내부와 강하게 결합된 횡단 관심사를 안정적으로 반복해야 할 때 가장 큰 힘을 발휘한다.

- **📢 섹션 요약 비유**: 잘 만든 운동화 브랜드는 겉모양이 달라도 밑창과 충격 흡수 구조는 공통 플랫폼을 쓴다. 그래야 신발마다 디자인은 달라도 기본 착화감과 품질은 흔들리지 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 횡단 관심사 (Cross-cutting Concerns) | 여러 [[090_service_kubernetes_network_load_balancing|서비스]]에 반복되는 로깅, 추적, [[009_config|설정]], [[503_security_features_design|보안 기능]]으로 샤시의 주된 대상이다. |
| 부트스트랩 스타터 | 샤시를 [[090_service_kubernetes_network_load_balancing|서비스]] 시작 시 자동으로 연결하는 [[459_quic_fec_forward_error_correction|초기]]화 장치다. |
| 관측성 ([[642_observability_telemetry|Observability]]) | 구조화 [[568_logs_distributed_logging_elk_fluentd|로그]], [[342_routing_metric_hop_bandwidth_delay|메트릭]], [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]을 공통 규약으로 묶어 주는 핵심 가치다. |
| 외부화된 [[009_config|설정]] ([[544_externalized_configuration|Externalized Configuration]]) | [[009_config|설정]] 저장소 자체와는 별개로, 이를 읽고 바인딩하는 공통 코드가 샤시에 들어간다. |
| [[182_sidecar_pattern_proxy_container|사이드카 패턴]] ([[182_sidecar_pattern_proxy_container|Sidecar Pattern]]) | 프로세스 밖에서 공통 기능을 분리하는 대안으로, 샤시와 자주 비교된다. |
| [[302_service_mesh_istio|서비스 메시]] ([[828_service_mesh_microservice_communication_infrastructure|Service Mesh]]) | 네트워크 중심 횡단 관심사를 샤시 밖으로 옮길 때 연결되는 상위 운영 체계다. |
| 골든 패스 (Golden Path) | 조직이 권장하는 표준 개발 경로로, 샤시는 그 실행 가능한 코드 [[288_version_ihl_tos_total_length|버전]]이 될 수 있다. |

### 📈 관련 키워드 및 발전 흐름도

```text
서비스 수 증가
      │
      ▼
보일러플레이트 중복 · 운영 표준 불일치
      │
      ▼
마이크로서비스 샤시 (Microservice Chassis)
      │
      ├──────────────► 로깅 · 메트릭 · 분산 추적 표준화
      ├──────────────► 설정 · 헬스 체크 · 예외 처리 공통화
      ├──────────────► 서비스 부트스트랩 단축
      └──────────────► 사이드카 · 서비스 메시와 역할 분담
```

이 흐름은 [[090_service_kubernetes_network_load_balancing|서비스]] 수 증가가 공통 코드 표준화를 요구하고, 이후에는 샤시와 외부 플랫폼을 조합하는 방향으로 성숙해 가는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[532_microservices_decomposition_patterns|마이크로서비스]] 샤시는 새 장난감 가게를 열 때마다 계산대와 전등, 안내판을 미리 갖춰 둔 기본 가게 틀과 같아요.
2. 그래서 가게 주인은 어떤 장난감을 팔지만 정하면 되고, 기본 준비는 다시 하지 않아도 돼요.
3. 하지만 필요 없는 물건까지 기본 틀에 너무 많이 넣으면 가게가 무겁고 복잡해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 183 / 482

← **이전**: [[182_sidecar_pattern_proxy_container|182. 사이드카 패턴 (Sidecar Pattern) - MSA 프록시 컨테이너]]
**다음**: [[184_externalized_configuration_server|184. 외부화된 설정 서버 (Externalized Configuration Server)]] →

---
