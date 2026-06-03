+++
title = "186. 분산 추적 (Distributed Tracing) 인프라 - 다수 서비스를 거치는 응용 프로그램 프로그래밍 인터페이스 (Application Programming Interface, API) 호출 구간(Span/Trace) 병목 파악 (Zipkin, Jaeger 연동)"
date = 2026-05-06

[taxonomies]
tags = ["studynote-enterprise"]

[extra]
tags = ["studynote-enterprise"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/) ([Distributed Tracing](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/))은 [마이크로서비스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([Microservice Architecture](/knowledge-base/studynote/07_enterprise_systems/06_exam_summary/365_msa_microservice_architecture/), [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/))에서 하나의 사용자 요청이 여러 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 지나는 동안 같은 Trace ID와 Span 계층으로 연결해 전체 호출 여정을 복원하는 관측성 인프라다.
> 2. **가치**: [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 흩어진 환경에서도 어느 구간에서 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 커졌고 어떤 하위 호출이 실패했는지를 시간축으로 보여 주어 평균 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 (Mean Time To [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/))을 크게 줄인다.
> 3. **판단 포인트**: Zipkin이나 Jaeger 같은 도구를 설치하는 것만으로는 부족하며, [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 전파, 샘플링 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·[메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 연계가 함께 설계되어야 진짜 병목 분석 도구가 된다.

---

## Ⅰ. 개요 및 필요성

[분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)은 여러 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 쪼개진 시스템에서 단일 요청의 인과관계를 다시 이어 붙이기 위한 기술이다. 모놀리식 환경에서는 애플리케이션 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 한 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)만 뒤져도 처리 흐름을 대략 따라갈 수 있었지만, MSA에서는 게이트웨이, 주문, 결제, 재고, [메시지 브로커](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/), [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)가 모두 따로 움직이므로 요청 하나의 여정이 금방 파편화된다. 이때 단순 [로그 수집](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/)만으로는 "이 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)들이 같은 사용자 요청에 속하는가"를 즉시 판단하기 어렵다.

이 문제가 중요한 이유는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 전파되기 때문이다. 예를 들어 주문 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 응답이 2초 느릴 때, 진짜 원인이 주문 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 자체인지 결제 응용 프로그램 프로그래밍 인터페이스 ([Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)) 호출인지, 그 아래 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)인지 알 수 없다면 팀 간 책임 공방만 길어진다. [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)은 요청마다 공통 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)를 부여하고, 각 구간의 시작·종료 시각과 부모-자식 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 기록해 이런 병목의 위치와 순서를 시각적으로 드러낸다.

또한 현대 시스템은 동기 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 호출만 있는 것이 아니라 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐와 비동기 작업도 섞여 있다. 이때 Trace ID가 헤더나 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 따라 끊김 없이 전달되지 않으면, 관측성은 한 구간짜리 부분 지도에 그친다. 결국 [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)의 본질은 화면이 아니라 <strong>문맥을 전파하는 규율</strong>에 있다.

- **📢 섹션 요약 비유**: [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)은 여러 역을 거치는 택배 상자에 같은 송장 번호를 계속 붙여 두는 것과 같다. 그래야 어느 물류센터에서 시간이 오래 걸렸는지 한눈에 찾을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)은 크게 계측, 전파, 수집, 저장, 조회의 다섯 단계로 동작한다. 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 트레이서 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)나 [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 계측 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)를 통해 현재 요청의 Trace ID와 Span을 만들고, 이를 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 헤더나 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)으로 다음 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 넘긴다. 이후 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 Span [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 에이전트나 컬렉터로 보내지고, 저장소에 적재된 뒤 Zipkin이나 Jaeger 같은 사용자 인터페이스에서 조회된다.

아래 그림은 요청 흐름과 추적 수집 흐름을 함께 보여 준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Request path and tracing pipeline</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Client -&gt; Gateway -&gt; Order -&gt; Payment -&gt; DB</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ span-4 : SQL</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">span-3 : payment call</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">span-2 : order handler</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">trace-1 span-1 : gateway</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Services export spans -&gt; Collector -&gt; Storage -&gt; Zipkin / Jaeger</div></div>
</div>
</div>



| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| [Trace ID](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/) | 하나의 요청 전체를 묶는 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 전파가 끊기면 추적도 끊긴다. |
| Span | 개별 작업 구간의 단위 | 이름, 시작·종료 시각, 상태, 태그 설계가 중요하다. |
| [Context Propagation](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/570_trace_id_span_id_context_propagation/) | 헤더와 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지에 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)를 전달 | HTTP뿐 아니라 비동기 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)징까지 고려해야 한다. |
| Collector | 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 Span을 수집 | 애플리케이션 경로와 분리해 비동기 수집하는 편이 안전하다. |
| Storage | 추적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장 | 샘플링 비율과 보존 기간이 비용을 좌우한다. |
| 조회 인터페이스 | 시간축, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/), 검색 제공 | `trace_id`와 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 상관관계가 있으면 분석 속도가 빨라진다. |

여기서 핵심은 Span이 단순 시간 기록이 아니라 계층 구조를 가진다는 점이다. 부모 Span은 하위 호출 전체 시간을 품고, 자식 Span은 세부 구간의 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 보여 준다. 따라서 전체 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 1초일 때, 그중 700밀리초가 결제 호출이고 다시 그 안 500밀리초가 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)였다는 식으로 병목이 단계적으로 드러난다.

또 하나 중요한 축은 샘플링이다. 모든 요청을 100% 저장하면 가장 자세하지만 비용과 저장량이 급격히 커진다. 반대로 너무 적게 수집하면 희귀 오류를 놓친다. 그래서 일반 요청은 일부만 수집하고, 오류나 고지연 요청은 우선 저장하는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 대규모 환경에서 자주 사용된다.

- **📢 섹션 요약 비유**: [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)은 마라톤 중계에서 선수 전체 기록뿐 아니라 구간 통과 시간까지 재는 것과 같다. 전체 순위만 보면 누가 늦었는지 모르지만, 구간 기록이 있으면 어디서 속도가 떨어졌는지 바로 보인다.

---

## Ⅲ. 비교 및 연결

[분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)은 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)와 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 사이에서 독특한 역할을 한다. [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 사건의 상세 문맥을, [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)은 [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)와 수치 추세를, 추적은 요청의 경로와 인과관계를 보여 준다. 따라서 장애 분석에서는 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)으로 이상 시점을 찾고, 추적으로 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 구간을 좁히고, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)로 구체 오류 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 식의 조합이 가장 강력하다.

| [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) | 주로 답하는 질문 | 강점 | 한계 |
| :--- | :--- | :--- | :--- |
| [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) | 얼마나 느려지고 얼마나 실패했는가 | 경보와 추세 파악에 강함 | 개별 요청 문맥은 약함 |
| [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | 어떤 오류 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지와 상태가 발생했는가 | 상세 원인 분석에 강함 | 요청 간 인과관계 복원이 어렵다 |
| [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/) | 어느 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 구간에서 병목이 생겼는가 | 호출 경로와 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 분해에 강함 | 전파 누락 시 전체 흐름이 끊긴다 |

Zipkin과 Jaeger도 지향점이 조금 다르다. Zipkin은 비교적 단순하고 가벼운 배포 경험을 제공해 빠른 도입에 유리하고, Jaeger는 샘플링 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 의존성 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/), 대규모 배포 경험이 풍부해 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 환경에서 많이 선택된다. 최근에는 두 도구 모두 OpenTelemetry와 함께 쓰이거나, [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector를 앞단에 두어 백엔드를 교체 가능한 구조로 가져가는 경우가 늘고 있다.

| 도구 | 강점 | 잘 맞는 환경 |
| :--- | :--- | :--- |
| Zipkin | 단순한 구조, 가벼운 시작, 빠른 학습 | 소규모~중간 규모, 빠른 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)럿 도입 |
| Jaeger | 풍부한 운영 옵션, 샘플링과 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 강점 | [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/), [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/), 대규모 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) |

즉 도구 비교보다 먼저 따질 것은 추적 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)과 전파 표준이다. B3 헤더나 W3C (World Wide Web Consortium) Trace [Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 같은 전파 규약이 맞지 않으면, Zipkin과 Jaeger 중 무엇을 쓰든 연결성이 약해진다. 관측성 인프라의 본질은 백엔드 제품이 아니라 <strong>끊기지 않는 문맥 체인</strong>이다.

- **📢 섹션 요약 비유**: [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)은 자동차 계기판이고, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 정비 기사 메모장이며, [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)은 자동차가 어느 길로 갔는지 그린 내비게이션 기록이다. 세 가지를 합쳐야 사고 원인을 가장 빨리 찾을 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)은 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이, 핵심 비즈니스 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 외부 호출 구간부터 우선 적용하는 것이 효과적이다. [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인, 주문, 결제, 검색처럼 사용자 체감이 큰 경로를 먼저 계측하면 작은 도입으로도 큰 가치를 얻을 수 있다. 특히 외부 결제사, 캐시, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/), [메시지 브로커](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/)와 만나는 경계에 Span을 남기면 시스템 내부와 외부 중 어디가 느린지 빠르게 구분할 수 있다.

또한 추적은 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)와 연결될 때 훨씬 강력하다. 모든 구조화 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에 `trace_id`를 함께 남기면 운영자는 Jaeger나 Zipkin에서 느린 구간을 찾고, 같은 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)로 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 저장소에서 상세 오류를 바로 검색할 수 있다. 반대로 추적 화면만 있고 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 상관관계가 없으면 "어디서 느린지"는 알아도 "왜 느린지"는 다시 수작업으로 찾아야 한다.

### 기술사 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 게이트웨이부터 하위 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 호출까지 [Trace ID](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/) 전파가 끊기지 않는가?
2. Span 이름과 태그가 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)명, [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 경로, 오류 코드, 외부 대상 등 분석 가능한 수준으로 설계되어 있는가?
3. 정상 트래픽과 오류 트래픽에 대해 샘플링 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 분리되어 있는가?
4. [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)와 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)이 같은 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 또는 공통 라벨로 연결되는가?
5. Zipkin 또는 Jaeger 도입 전에 [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 같은 중립 계층을 둘 필요가 있는가?

### 자주 나오는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- Trace ID를 게이트웨이까지만 넣고 내부 비동기 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지에는 전달하지 않는 경우
- 모든 요청을 100% 저장해 비용과 저장소를 감당하지 못하는 경우
- Span 이름을 `method1`, `call2`처럼 모호하게 지어 분석 가치가 떨어지는 경우
- 추적 대시보드만 믿고 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 상관관계를 만들지 않는 경우

결론적으로 기술사 답안에서는 "Zipkin으로 본다"보다, <strong>추적을 위해 문맥을 전파하고 샘플링하며 다른 관측성 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/">신호</a>와 연결한다</strong>는 설계 관점을 강조해야 한다. 도구는 수단이고, 병목의 인과관계를 복원하는 구조가 목적이다.

- **📢 섹션 요약 비유**: 도로마다 CCTV를 달아도 차량 번호가 계속 바뀌면 한 차의 이동 경로를 찾을 수 없다. 같은 번호판이 끝까지 이어져야 어디서 막혔는지 알 수 있는 것처럼 [Trace ID](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/) 전파가 핵심이다.

---

## Ⅴ. 기대효과 및 결론

[분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)이 잘 구축되면 운영팀은 "느리다"는 현상을 구체적인 시간축과 호출 구조로 바꿔 볼 수 있다. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 책임 경계가 복잡한 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경에서도 병목의 위치, 외부 의존성 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 재시도 폭증, 팬아웃 호출 구조를 빠르게 파악할 수 있어 장애 대응 속도가 높아진다. 이는 단순 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링을 넘어 설계 개선에도 직접적인 피드백을 제공한다.

하지만 추적은 공짜가 아니다. 계측 코드, 헤더 전파, 샘플링, 저장 비용, [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹, 대시보드 운영이 함께 필요하다. 특히 비동기 흐름과 배치 작업까지 추적하려면 표준화와 개발 규율이 따라와야 하므로, 도입 범위와 운영 목표를 명확히 잡는 것이 중요하다.

결국 [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)은 "예쁜 [간트 차트](/knowledge-base/studynote/04_software_engineering/01_overview_principles/039_gantt_chart/) 도구"가 아니라, <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 시스템의 인과관계를 복원하는 운영 인프라</strong>다. Zipkin과 Jaeger는 그 결과를 보여 주는 대표 구현일 뿐이며, 기억해야 할 핵심은 요청 문맥을 끊기지 않게 이어 주는 체계라는 점이다.

- **📢 섹션 요약 비유**: 거대한 놀이공원에서 아이가 어디서 길을 잃었는지 찾으려면 입장부터 놀이기구 탑승까지 같은 팔찌 번호가 계속 기록되어야 한다. [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)도 요청에 그 팔찌를 채워 주는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Trace ID](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/) | 하나의 요청을 여러 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)와 Span에 연결하는 기준 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)다. |
| Span | 세부 작업 구간의 시간과 상태를 표현하는 기본 단위다. |
| [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) | 계측과 수집을 표준화해 Zipkin, Jaeger 같은 백엔드를 유연하게 교체하게 해 준다. |
| 구조화 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | `trace_id`를 함께 남기면 추적과 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 상관분석이 쉬워진다. |
| [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/) ([Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/)) | [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 계층에서 자동 계측과 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 전파를 보조할 수 있다. |
| 샘플링 ([Sampling](/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/)) | 비용과 가시성의 균형을 잡는 핵심 운영 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">모놀리식 디버깅 한계 없음</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">MSA 확산과 로그 파편화</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Trace ID · Span 기반 문맥 전파</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Zipkin / Jaeger 수집 · 시각화</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">OpenTelemetry 기반 통합 관측성</div>
</div>
</div>



이 흐름은 단순 [로그 분석](/knowledge-base/studynote/16_bigdata/05_analysis/119_log_analysis/)에서 시작해, 요청 문맥 복원과 표준화된 관측성 플랫폼으로 성숙해 가는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)은 택배 상자에 같은 송장 번호를 붙여서 여러 창고를 지나도 같은 물건인지 알아보게 하는 방법이에요.
2. 그래서 어디 창고에서 오래 멈췄는지, 어디서 문제가 생겼는지 금방 찾을 수 있어요.
3. 번호가 중간에 사라지면 길을 잃어버리니까, 끝까지 같은 번호를 전해 주는 게 가장 중요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 186 / 482

← **이전**: [185. 로그 수집 통합 (Log Aggregation) 아키텍처 - Fluentd -> Elasticsearch 파이프라인](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/185_log_aggregation_fluentd_elasticsearch/)
**다음**: [187. 스트랭글러 피그 패턴 (Strangler Fig Pattern) - 점진적 MSA 전환](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/187_strangler_fig_pattern_msa_migration/) →

---
