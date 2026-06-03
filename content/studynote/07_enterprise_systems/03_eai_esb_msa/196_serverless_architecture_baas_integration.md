---
title: 196. 서버리스 아키텍처 - BaaS와 FaaS 기반 엔터프라이즈 통합
date: '2026-05-08'
tags:
- studynote-enterprise
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[215_serverless_architecture_faas_aws_lambda|서버리스 아키텍처]]는 서버가 사라진다는 뜻이 아니라, 인프라 [[528_provisioning|프로비저닝]]·패치·오토스케일링 책임을 클라우드가 맡고 개발자는 기능과 이벤트 흐름에 집중하는 운영 [[198_abstraction_control_data_process|추상화]] 모델이다.
> 2. **가치**: [[186_baas_backend_as_a_service_firebase|BaaS]] ([[186_baas_backend_as_a_service_firebase|Backend as a Service]])와 [[342_faas|FaaS]] (Function [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]])를 조합하면 [[303_authentication_authorization_patterns|인증]], 저장소, 알림, 이벤트 처리 같은 공통 기능을 빠르게 연결해 출시 시간을 크게 줄일 수 있다.
> 3. **판단 포인트**: [[206_serverless_cold_start|서버리스]]는 변동 부하와 이벤트 처리에 특히 강하지만, [[559_serverless_cold_start_mitigation|콜드 스타트]], 실행 시간 제한, 상태 관리, [[051_vendor_lock_in_cloud_computing|벤더 종속]]성을 고려해 적용 범위를 선별해야 한다.

---

## Ⅰ. 개요 및 필요성

[[215_serverless_architecture_faas_aws_lambda|서버리스 아키텍처]]는 애플리케이션 실행에 서버가 없다는 의미가 아니라, 개발 조직이 직접 관리해야 하는 서버 계층이 줄어든다는 뜻이다. [[001_operating_system_purpose|운영체제]] 패치, 인스턴스 확장, 미들웨어 관리 대신, 개발자는 함수 단위 로직과 관리형 [[090_service_kubernetes_network_load_balancing|서비스]] 조합에 집중한다. 그래서 [[206_serverless_cold_start|서버리스]]의 본질은 새로운 프로그래밍 문법이 아니라 **운영 책임의 재배치**다.

이 모델이 중요해진 이유는 디지털 [[090_service_kubernetes_network_load_balancing|서비스]]의 트래픽 패턴이 점점 더 예측하기 어려워졌기 때문이다. 이벤트성 캠페인, 모바일 앱 런칭, 비정기 배치, [[309_saas|SaaS]] 연동은 한동안 요청이 없다가도 특정 순간에 폭증한다. 전통적인 고정 서버 방식은 이런 수요에 맞추려면 평소에도 최대 부하를 기준으로 인프라를 유지해야 해 비용과 운영 부담이 커진다.

또한 많은 프로젝트에서 차별화되지 않는 공통 기능이 개발 시간을 잡아먹는다. [[568_logs_distributed_logging_elk_fluentd|로그]]인, [[501_file_definition_logical_record|파일]] 업로드, 푸시 알림, 간단한 CRUD, 이벤트 후처리 같은 영역은 직접 서버를 짓기보다 관리형 [[090_service_kubernetes_network_load_balancing|서비스]]를 연결하는 편이 훨씬 빠르다. 그래서 [[206_serverless_cold_start|서버리스]]는 특히 신규 [[090_service_kubernetes_network_load_balancing|서비스]], 디지털 채널, 통합 [[152_hub_dummy_switching_intelligent|허브]] 역할에서 의미가 크다.

- **📢 섹션 요약 비유**: [[206_serverless_cold_start|서버리스]]는 매번 행사장마다 무대와 전기를 직접 설치하는 대신, 이미 준비된 공연장을 빌리고 우리는 공연 내용만 준비하는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[206_serverless_cold_start|서버리스]] 통합 구조는 보통 클라이언트, [[542_api_gateway|API Gateway]], [[303_authentication_authorization_patterns|인증]]·저장·알림을 담당하는 [[186_baas_backend_as_a_service_firebase|BaaS]], 맞춤 로직을 수행하는 [[342_faas|FaaS]], 그리고 [[539_event_bus_stream_processing|이벤트 버스]]나 큐 같은 연결 계층으로 구성된다. BaaS는 공통 백엔드 기능을 관리형 [[090_service_kubernetes_network_load_balancing|서비스]]로 제공하고, FaaS는 결제 승인, 이미지 변환, [[498_webhook_rest_api_reverse_callback|웹훅]] 후처리처럼 조직 고유 로직을 함수 단위로 실행한다. 이 둘을 엮어 [[337_standard_vs_paging_swapping|전체 프로세스]]를 설계하는 것이 핵심이다.

| 구성 요소 | 역할 | 실무 포인트 |
| :--- | :--- | :--- |
| [[542_api_gateway|API Gateway]] | 요청 진입점, [[303_authentication_authorization_patterns|인증]], [[520_rate_limiting|rate limiting]] | 함수와 직접 결합하지 말고 [[164_policy|정책]] 계층으로 활용 |
| [[186_baas_backend_as_a_service_firebase|BaaS]] | [[303_authentication_authorization_patterns|인증]], DB, 스토리지, 알림 제공 | 공통 기능은 최대한 재사용해 개발 속도 확보 |
| [[342_faas|FaaS]] | 이벤트 단위 비즈니스 로직 실행 | 짧고 무상태([[239_stateless_redis|stateless]])한 작업에 적합 |
| [[539_event_bus_stream_processing|Event Bus]] / [[058_queue|Queue]] | 비동기 연결과 [[454_buffering|버퍼링]] | 재시도, 순서, fan-out 설계 중요 |
| [[642_observability_telemetry|Observability]] | [[568_logs_distributed_logging_elk_fluentd|로그]], [[342_routing_metric_hop_bandwidth_delay|메트릭]], 추적 수집 | 함수 수가 늘수록 [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] 필수 |

아래 그림은 전형적인 엔터프라이즈 [[206_serverless_cold_start|서버리스]] 통합 경로를 요약한다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Serverless integration: managed backend + event-driven functions    │
├──────────────────────────────────────────────────────────────────────┤
│ Web/Mobile -> API Gateway -> Auth(BaaS) -> FaaS -> DB/Queue/SaaS   │
│      │                             │                    │           │
│      └──── Object Storage/Event Bus┴──── Logs/Tracing ─┘           │
└──────────────────────────────────────────────────────────────────────┘
```

이 구조의 핵심 원리는 "필요할 때만 실행하고, 나머지는 관리형 [[090_service_kubernetes_network_load_balancing|서비스]]에 위임한다"는 것이다. 예를 들어 사용자가 이미지를 업로드하면 스토리지 이벤트가 발생하고, FaaS가 썸네일을 만든 뒤 [[002_database_definition|데이터베이스]]를 갱신하며, 알림 [[090_service_kubernetes_network_load_balancing|서비스]]가 후속 [[389_mesh_topology|메시]]지를 발송한다. 각 단계는 느슨하게 연결되며, 요청량이 증가하면 플랫폼이 동시 실행 수를 자동 확장한다.

- **📢 섹션 요약 비유**: [[206_serverless_cold_start|서버리스]]는 모든 일을 상근 직원이 처리하는 회사가 아니라, 기본 시설은 외주 [[090_service_kubernetes_network_load_balancing|서비스]]가 맡고 필요할 때마다 전문 계약직이 즉시 투입되는 조직과 같다.

---

## Ⅲ. 비교 및 연결

[[206_serverless_cold_start|서버리스]]는 [[561_container_based_deployment|컨테이너]] 기반 [[532_microservices_decomposition_patterns|마이크로서비스]]나 전통적 모놀리식과 경쟁하지만, 우열보다 적합성 차이가 중요하다. 실행 시간이 짧고 요청 변동 폭이 크면 [[206_serverless_cold_start|서버리스]]가 유리하고, 장시간 연결과 예측 가능한 고정 부하라면 [[561_container_based_deployment|컨테이너]]가 더 효율적일 수 있다. 따라서 아키텍처 선택은 기능 분해보다 운영 특성 분석에서 시작해야 한다.

| 항목 | [[206_serverless_cold_start|서버리스]] | [[561_container_based_deployment|컨테이너]] 기반 [[619_msa_traffic_hardware|MSA]] | 전통적 모놀리식 |
| :--- | :--- | :--- | :--- |
| 운영 책임 | 플랫폼이 대부분 담당 | 팀이 이미지·[[073_container_orchestration_tools|오케스트레이션]] 관리 | 서버·미들웨어 직접 관리 |
| 확장 방식 | 요청 수에 따라 자동 확장 | [[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]], 오토스케일 [[164_policy|정책]] 수립 필요 | 수동/제한적 확장 |
| 강점 | 빠른 출시, 이벤트 처리, 사용량 기반 과금 | 유연한 제어, 장기 실행 적합 | 단순 배포, [[459_quic_fec_forward_error_correction|초기]] 구조 단순 |
| 약점 | [[559_serverless_cold_start_mitigation|콜드 스타트]], 제한 시간, [[362_lock_in_portability|lock-in]] | 운영 복잡도 높음 | 배포 단위 큼, 확장 경직 |
| 적합 사례 | [[498_webhook_rest_api_reverse_callback|웹훅]], 배치, 이미지 처리, [[309_saas|SaaS]] 통합 | 핵심 [[064_relation_domain|도메인]] [[014_api_posix|API]], 장기 [[160_session_controlling_terminal|세션]] | 소규모 내부 업무 |

또 [[206_serverless_cold_start|서버리스]]는 [[538_event_driven_architecture_eda|이벤트 기반 아키텍처]]와 자연스럽게 연결된다. [[498_webhook_rest_api_reverse_callback|웹훅]] 수신, [[501_file_definition_logical_record|파일]] 업로드, [[389_mesh_topology|메시]]지 큐 소비, [[208_schedule_history_transaction_execution_order|스케줄]] [[507_acid_properties|트리거]]를 함수로 붙이기 쉽기 때문이다. 반면 [[064_relation_domain|도메인]] 핵심 [[191_transaction_concept_states|트랜잭션]] 전체를 모두 함수로 쪼개면 관측성과 테스트가 어려워질 수 있어, BFF나 핵심 API는 [[561_container_based_deployment|컨테이너]], 주변 후처리는 [[206_serverless_cold_start|서버리스]]로 분리하는 혼합 구성이 흔하다.

- **📢 섹션 요약 비유**: [[206_serverless_cold_start|서버리스]]는 필요할 때마다 불러 쓰는 택시이고, [[561_container_based_deployment|컨테이너]]는 회사 전용 차량, 모놀리식은 모든 일을 한 차로 처리하는 승합차와 같다. 목적과 운행 패턴이 다르면 [[170_selectivity_cardinality_distribution_tuning|선택도]] 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[[206_serverless_cold_start|서버리스]] 도입의 핵심 질문은 "운영을 줄일 수 있는가"와 "플랫폼 제약을 감당할 수 있는가"다. 짧은 실행 시간, 비정기 트래픽, 외부 이벤트 연동, 빠른 출시가 중요하면 채택 가치가 높다. 반대로 상시 고부하, 장시간 처리, 극저지연 응답, 복잡한 상태 공유가 핵심이면 오히려 비용과 복잡도가 커질 수 있다.

### [[435_checklist_based_testing|체크리스트]]

1. 함수 실행 시간이 플랫폼 제한 안에 들어오고, 실패 시 재시도 [[268_strategy_pattern|전략]]이 정의되어 있는가?
2. [[171_idempotency_iac_terraform|멱등성]], 중복 이벤트 처리, [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]], 구조화 [[568_logs_distributed_logging_elk_fluentd|로그]]가 준비되어 있는가?
3. [[559_serverless_cold_start_mitigation|콜드 스타트]]가 사용자 경험에 미치는 영향을 측정했고, 필요하면 [[202_provisioned_concurrency_serverless_cold_start|provisioned concurrency]] 같은 보완책을 검토했는가?
4. 비밀 정보 관리, [[526_iam|IAM]] ([[526_iam|Identity and Access Management]]) 최소 권한, 네트워크 [[189_egress|egress]] 비용을 고려했는가?
5. [[186_baas_backend_as_a_service_firebase|BaaS]] 기능 사용이 vendor [[510_lock|lock]]-in으로 이어질 때 대체 [[268_strategy_pattern|전략]]이나 경계 분리가 가능한가?

### 채택 판단

- **적합**: 이벤트 후처리, 백오피스 자동화, [[498_webhook_rest_api_reverse_callback|webhook]] consumer, 이미지/문서 변환, 간헐적 [[014_api_posix|API]]
- **주의**: 상태가 많은 [[160_session_controlling_terminal|세션]] 서버, 장시간 스트리밍, 초저지연 금융 매칭 엔진
- **권장 [[268_strategy_pattern|전략]]**: 핵심 [[064_relation_domain|도메인]]은 별도 [[090_service_kubernetes_network_load_balancing|서비스]]로 유지하고, 주변 통합과 burst성 작업은 [[206_serverless_cold_start|서버리스]]로 분리

기술사 답안에서는 "운영이 없다"는 표현보다, **운영 책임은 줄지만 설계 책임은 더 중요해진다**는 점을 짚어야 한다. 함수 수가 늘수록 권한, 관측성, 비용 통제가 오히려 더 중요한 설계 주제가 된다.

- **📢 섹션 요약 비유**: [[206_serverless_cold_start|서버리스]]는 가게 임대료를 줄여 주지만, 주문 흐름과 재고 정리를 대신 설계해 주지는 않는다. 주방이 간단해질수록 동선 설계는 더 중요해진다.

---

## Ⅴ. 기대효과 및 결론

[[215_serverless_architecture_faas_aws_lambda|서버리스 아키텍처]]를 적절히 적용하면 출시 속도를 높이고, 공통 기능 개발을 줄이며, 트래픽 급증에 유연하게 대응할 수 있다. 특히 디지털 채널과 통합 [[152_hub_dummy_switching_intelligent|허브]]에서는 작은 기능을 빠르게 실험하고 비용을 사용량에 맞춰 지불할 수 있다는 장점이 크다. 기업 입장에서는 인프라 운영보다 비즈니스 실험에 더 많은 시간을 쓸 수 있게 된다.

그러나 [[206_serverless_cold_start|서버리스]]는 만능 해법이 아니다. [[559_serverless_cold_start_mitigation|콜드 스타트]], 디버깅 복잡성, [[090_service_kubernetes_network_load_balancing|서비스]] 경계 난립, [[051_vendor_lock_in_cloud_computing|벤더 종속]]성은 반드시 관리해야 할 비용이다. 따라서 이 주제는 "서버를 없애는 기술"이 아니라, **BaaS와 FaaS를 활용해 운영 부담을 줄이되 적용 경계를 엄격히 선택하는 아키텍처 [[268_strategy_pattern|전략]]**으로 기억하는 것이 가장 정확하다.

- **📢 섹션 요약 비유**: [[206_serverless_cold_start|서버리스]]는 모든 건물을 철거하는 일이 아니라, 자주 쓰는 공용 설비는 임대하고 우리만의 핵심 공간만 직접 짓는 도시 계획과 같다. 무엇을 빌리고 무엇을 직접 지을지 구분하는 눈이 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[186_baas_backend_as_a_service_firebase|BaaS]] | [[303_authentication_authorization_patterns|인증]], [[001_dikw_pyramid|데이터]] 저장, 알림 등 공통 백엔드 기능을 관리형으로 제공 |
| [[342_faas|FaaS]] | 이벤트나 요청 단위 비즈니스 로직을 함수로 실행 |
| [[542_api_gateway|API Gateway]] | [[206_serverless_cold_start|서버리스]] 함수 앞단의 [[164_policy|정책]]·보안·[[339_routing_overview_best_path_selection|라우팅]] 제어 지점 |
| [[539_event_bus_stream_processing|Event Bus]] | 함수 간 느슨한 연결과 비동기 fan-out을 지원 |
| [[347_cold_start_problem|Cold Start]] | [[206_serverless_cold_start|서버리스]] 적용 범위를 결정하는 대표 [[282_performance_tactics|성능]] 제약 |

### 📈 관련 키워드 및 발전 흐름도

```text
직접 서버 구축
    │
    ▼
관리형 인증 · 저장소 (BaaS)
    │
    ▼
이벤트 기반 함수 실행 (FaaS)
    │
    ▼
API Gateway · Event Bus 연계
    │
    ▼
하이브리드 서버리스 아키텍처
```

이 흐름은 "서버 운영 축소 → 관리형 [[090_service_kubernetes_network_load_balancing|서비스]] 활용 → 이벤트 중심 조합 → 혼합형 최적화"로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[206_serverless_cold_start|서버리스]]는 내가 큰 기계를 직접 돌리지 않고, 필요할 때만 버튼을 눌러 일을 맡기는 방법이에요.
2. [[568_logs_distributed_logging_elk_fluentd|로그]]인이나 저장 같은 기본 도구는 이미 준비된 것을 쓰고, 특별한 일만 내가 만든 작은 함수가 해요.
3. 그래서 빨리 시작할 수 있지만, 어떤 일을 어디에 맡길지는 똑똑하게 정해야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 196 / 482

← **이전**: [[195_eai_edi_van_b2b_integration|195. EDI와 VAN - B2B 전자문서 연동 구조]]
**다음**: [[197_data_mesh_decentralized_domain_ownership|197. 데이터 메시 (Data Mesh)]] →

---
