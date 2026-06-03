+++
title = "196. 서버리스 아키텍처 - BaaS와 FaaS 기반 엔터프라이즈 통합"
date = 2026-05-08

[taxonomies]
tags = ["studynote-enterprise"]

[extra]
tags = ["studynote-enterprise"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [서버리스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/215_serverless_architecture_faas_aws_lambda/)는 서버가 사라진다는 뜻이 아니라, 인프라 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/)·패치·오토스케일링 책임을 클라우드가 맡고 개발자는 기능과 이벤트 흐름에 집중하는 운영 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 모델이다.
> 2. **가치**: [BaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/186_baas_backend_as_a_service_firebase/) ([Backend as a Service](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/186_baas_backend_as_a_service_firebase/))와 [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/) (Function [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))를 조합하면 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 저장소, 알림, 이벤트 처리 같은 공통 기능을 빠르게 연결해 출시 시간을 크게 줄일 수 있다.
> 3. **판단 포인트**: [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 변동 부하와 이벤트 처리에 특히 강하지만, [콜드 스타트](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/), 실행 시간 제한, 상태 관리, [벤더 종속](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/)성을 고려해 적용 범위를 선별해야 한다.

---

## Ⅰ. 개요 및 필요성

[서버리스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/215_serverless_architecture_faas_aws_lambda/)는 애플리케이션 실행에 서버가 없다는 의미가 아니라, 개발 조직이 직접 관리해야 하는 서버 계층이 줄어든다는 뜻이다. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 패치, 인스턴스 확장, 미들웨어 관리 대신, 개발자는 함수 단위 로직과 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 조합에 집중한다. 그래서 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)의 본질은 새로운 프로그래밍 문법이 아니라 **운영 책임의 재배치**다.

이 모델이 중요해진 이유는 디지털 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 트래픽 패턴이 점점 더 예측하기 어려워졌기 때문이다. 이벤트성 캠페인, 모바일 앱 런칭, 비정기 배치, [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 연동은 한동안 요청이 없다가도 특정 순간에 폭증한다. 전통적인 고정 서버 방식은 이런 수요에 맞추려면 평소에도 최대 부하를 기준으로 인프라를 유지해야 해 비용과 운영 부담이 커진다.

또한 많은 프로젝트에서 차별화되지 않는 공통 기능이 개발 시간을 잡아먹는다. [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 업로드, 푸시 알림, 간단한 CRUD, 이벤트 후처리 같은 영역은 직접 서버를 짓기보다 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 연결하는 편이 훨씬 빠르다. 그래서 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 특히 신규 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 디지털 채널, 통합 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) 역할에서 의미가 크다.

- **📢 섹션 요약 비유**: [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 매번 행사장마다 무대와 전기를 직접 설치하는 대신, 이미 준비된 공연장을 빌리고 우리는 공연 내용만 준비하는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 통합 구조는 보통 클라이언트, [API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/), [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·저장·알림을 담당하는 [BaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/186_baas_backend_as_a_service_firebase/), 맞춤 로직을 수행하는 [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/), 그리고 [이벤트 버스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/539_event_bus_stream_processing/)나 큐 같은 연결 계층으로 구성된다. BaaS는 공통 백엔드 기능을 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 제공하고, FaaS는 결제 승인, 이미지 변환, [웹훅](/knowledge-base/studynote/03_network/09_application_layer_web_email/498_webhook_rest_api_reverse_callback/) 후처리처럼 조직 고유 로직을 함수 단위로 실행한다. 이 둘을 엮어 [전체 프로세스](/knowledge-base/studynote/02_operating_system/06_memory_management/337_standard_vs_paging_swapping/)를 설계하는 것이 핵심이다.

| 구성 요소 | 역할 | 실무 포인트 |
| :--- | :--- | :--- |
| [API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/) | 요청 진입점, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), [rate limiting](/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/) | 함수와 직접 결합하지 말고 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 계층으로 활용 |
| [BaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/186_baas_backend_as_a_service_firebase/) | [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), DB, 스토리지, 알림 제공 | 공통 기능은 최대한 재사용해 개발 속도 확보 |
| [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/) | 이벤트 단위 비즈니스 로직 실행 | 짧고 무상태([stateless](/knowledge-base/studynote/15_devops_sre/05_devsecops/239_stateless_redis/))한 작업에 적합 |
| [Event Bus](/knowledge-base/studynote/04_software_engineering/11_testing_validation/539_event_bus_stream_processing/) / [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/) | 비동기 연결과 [버퍼링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/) | 재시도, 순서, fan-out 설계 중요 |
| [Observability](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/), 추적 수집 | 함수 수가 늘수록 [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/) 필수 |

아래 그림은 전형적인 엔터프라이즈 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 통합 경로를 요약한다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Serverless integration: managed backend + event-driven functions    │
├──────────────────────────────────────────────────────────────────────┤
│ Web/Mobile -> API Gateway -> Auth(BaaS) -> FaaS -> DB/Queue/SaaS   │
│      │                             │                    │           │
│      └──── Object Storage/Event Bus┴──── Logs/Tracing ─┘           │
└──────────────────────────────────────────────────────────────────────┘
```

이 구조의 핵심 원리는 "필요할 때만 실행하고, 나머지는 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 위임한다"는 것이다. 예를 들어 사용자가 이미지를 업로드하면 스토리지 이벤트가 발생하고, FaaS가 썸네일을 만든 뒤 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)를 갱신하며, 알림 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 후속 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지를 발송한다. 각 단계는 느슨하게 연결되며, 요청량이 증가하면 플랫폼이 동시 실행 수를 자동 확장한다.

- **📢 섹션 요약 비유**: [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 모든 일을 상근 직원이 처리하는 회사가 아니라, 기본 시설은 외주 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 맡고 필요할 때마다 전문 계약직이 즉시 투입되는 조직과 같다.

---

## Ⅲ. 비교 및 연결

[서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 기반 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)나 전통적 모놀리식과 경쟁하지만, 우열보다 적합성 차이가 중요하다. 실행 시간이 짧고 요청 변동 폭이 크면 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)가 유리하고, 장시간 연결과 예측 가능한 고정 부하라면 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 더 효율적일 수 있다. 따라서 아키텍처 선택은 기능 분해보다 운영 특성 분석에서 시작해야 한다.

| 항목 | [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 기반 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) | 전통적 모놀리식 |
| :--- | :--- | :--- | :--- |
| 운영 책임 | 플랫폼이 대부분 담당 | 팀이 이미지·[오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 관리 | 서버·미들웨어 직접 관리 |
| 확장 방식 | 요청 수에 따라 자동 확장 | [HPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/), 오토스케일 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 수립 필요 | 수동/제한적 확장 |
| 강점 | 빠른 출시, 이벤트 처리, 사용량 기반 과금 | 유연한 제어, 장기 실행 적합 | 단순 배포, [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 구조 단순 |
| 약점 | [콜드 스타트](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/), 제한 시간, [lock-in](/knowledge-base/studynote/12_it_management/05_security_compliance/362_lock_in_portability/) | 운영 복잡도 높음 | 배포 단위 큼, 확장 경직 |
| 적합 사례 | [웹훅](/knowledge-base/studynote/03_network/09_application_layer_web_email/498_webhook_rest_api_reverse_callback/), 배치, 이미지 처리, [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 통합 | 핵심 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 장기 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) | 소규모 내부 업무 |

또 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 [이벤트 기반 아키텍처](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/538_event_driven_architecture_eda/)와 자연스럽게 연결된다. [웹훅](/knowledge-base/studynote/03_network/09_application_layer_web_email/498_webhook_rest_api_reverse_callback/) 수신, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 업로드, [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐 소비, [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)를 함수로 붙이기 쉽기 때문이다. 반면 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 핵심 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 전체를 모두 함수로 쪼개면 관측성과 테스트가 어려워질 수 있어, BFF나 핵심 API는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/), 주변 후처리는 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)로 분리하는 혼합 구성이 흔하다.

- **📢 섹션 요약 비유**: [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 필요할 때마다 불러 쓰는 택시이고, [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)는 회사 전용 차량, 모놀리식은 모든 일을 한 차로 처리하는 승합차와 같다. 목적과 운행 패턴이 다르면 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 도입의 핵심 질문은 "운영을 줄일 수 있는가"와 "플랫폼 제약을 감당할 수 있는가"다. 짧은 실행 시간, 비정기 트래픽, 외부 이벤트 연동, 빠른 출시가 중요하면 채택 가치가 높다. 반대로 상시 고부하, 장시간 처리, 극저지연 응답, 복잡한 상태 공유가 핵심이면 오히려 비용과 복잡도가 커질 수 있다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 함수 실행 시간이 플랫폼 제한 안에 들어오고, 실패 시 재시도 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 정의되어 있는가?
2. [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/), 중복 이벤트 처리, [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/), 구조화 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 준비되어 있는가?
3. [콜드 스타트](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/)가 사용자 경험에 미치는 영향을 측정했고, 필요하면 [provisioned concurrency](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/202_provisioned_concurrency_serverless_cold_start/) 같은 보완책을 검토했는가?
4. 비밀 정보 관리, [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/) ([Identity and Access Management](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/)) 최소 권한, 네트워크 [egress](/knowledge-base/studynote/16_bigdata/09_platform/189_egress/) 비용을 고려했는가?
5. [BaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/186_baas_backend_as_a_service_firebase/) 기능 사용이 vendor [lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)-in으로 이어질 때 대체 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이나 경계 분리가 가능한가?

### 채택 판단

- **적합**: 이벤트 후처리, 백오피스 자동화, [webhook](/knowledge-base/studynote/03_network/09_application_layer_web_email/498_webhook_rest_api_reverse_callback/) consumer, 이미지/문서 변환, 간헐적 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)
- **주의**: 상태가 많은 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 서버, 장시간 스트리밍, 초저지연 금융 매칭 엔진
- **권장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)**: 핵심 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)은 별도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 유지하고, 주변 통합과 burst성 작업은 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)로 분리

기술사 답안에서는 "운영이 없다"는 표현보다, **운영 책임은 줄지만 설계 책임은 더 중요해진다**는 점을 짚어야 한다. 함수 수가 늘수록 권한, 관측성, 비용 통제가 오히려 더 중요한 설계 주제가 된다.

- **📢 섹션 요약 비유**: [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 가게 임대료를 줄여 주지만, 주문 흐름과 재고 정리를 대신 설계해 주지는 않는다. 주방이 간단해질수록 동선 설계는 더 중요해진다.

---

## Ⅴ. 기대효과 및 결론

[서버리스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/215_serverless_architecture_faas_aws_lambda/)를 적절히 적용하면 출시 속도를 높이고, 공통 기능 개발을 줄이며, 트래픽 급증에 유연하게 대응할 수 있다. 특히 디지털 채널과 통합 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)에서는 작은 기능을 빠르게 실험하고 비용을 사용량에 맞춰 지불할 수 있다는 장점이 크다. 기업 입장에서는 인프라 운영보다 비즈니스 실험에 더 많은 시간을 쓸 수 있게 된다.

그러나 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 만능 해법이 아니다. [콜드 스타트](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/), 디버깅 복잡성, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계 난립, [벤더 종속](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/)성은 반드시 관리해야 할 비용이다. 따라서 이 주제는 "서버를 없애는 기술"이 아니라, **BaaS와 FaaS를 활용해 운영 부담을 줄이되 적용 경계를 엄격히 선택하는 아키텍처 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)**으로 기억하는 것이 가장 정확하다.

- **📢 섹션 요약 비유**: [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 모든 건물을 철거하는 일이 아니라, 자주 쓰는 공용 설비는 임대하고 우리만의 핵심 공간만 직접 짓는 도시 계획과 같다. 무엇을 빌리고 무엇을 직접 지을지 구분하는 눈이 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [BaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/186_baas_backend_as_a_service_firebase/) | [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장, 알림 등 공통 백엔드 기능을 관리형으로 제공 |
| [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/) | 이벤트나 요청 단위 비즈니스 로직을 함수로 실행 |
| [API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/) | [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 함수 앞단의 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)·보안·[라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 제어 지점 |
| [Event Bus](/knowledge-base/studynote/04_software_engineering/11_testing_validation/539_event_bus_stream_processing/) | 함수 간 느슨한 연결과 비동기 fan-out을 지원 |
| [Cold Start](/knowledge-base/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/) | [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 적용 범위를 결정하는 대표 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 제약 |

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

이 흐름은 "서버 운영 축소 → 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 활용 → 이벤트 중심 조합 → 혼합형 최적화"로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 내가 큰 기계를 직접 돌리지 않고, 필요할 때만 버튼을 눌러 일을 맡기는 방법이에요.
2. [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인이나 저장 같은 기본 도구는 이미 준비된 것을 쓰고, 특별한 일만 내가 만든 작은 함수가 해요.
3. 그래서 빨리 시작할 수 있지만, 어떤 일을 어디에 맡길지는 똑똑하게 정해야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 196 / 482

← **이전**: [195. EDI와 VAN - B2B 전자문서 연동 구조](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/195_eai_edi_van_b2b_integration/)
**다음**: [197. 데이터 메시 (Data Mesh)](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/197_data_mesh_decentralized_domain_ownership/) →

---
