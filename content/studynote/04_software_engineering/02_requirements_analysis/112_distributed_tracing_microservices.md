+++
title = "112. 분산 트레이싱 (Distributed Tracing) - Span·Trace ID·OpenTelemetry 추적 체계"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 트레이싱은 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경에서 하나의 사용자 요청이 <strong>N개 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>를 거치는 전체 경로(Trace)</strong>를 고유 ID([Trace ID](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/))로 추적하고, 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 내 처리 구간(Span)의 <strong>레이턴시·에러를 <a href="/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/">시각화</a></strong>하여 병목을 특정하는 기법이다.
> 2. **가치**: 모놀리스에서는 하나의 스택트레이스로 디버깅이 가능하지만, MSA에서는 "주문→결제→배송→알림" 4개 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중 **어디서 500ms가 추가됐는지** 찾는 것 자체가 난제이며, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 트레이싱이 유일한 해법이다.
> 3. **판단 포인트**: [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/)([OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/))가 [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 표준으로 계측(Instrumentation)을 통일하고, Jaeger·Tempo·Zipkin이 백엔드 저장·[시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)를 담당하며, <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/570_trace_id_span_id_context_propagation/">Context Propagation</a>(W3C Trace <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/">Context</a>)</strong>으로 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 Trace ID를 전파한다.

---

## Ⅰ. 개요 및 필요성

MSA에서 [API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/) → Auth → Order → Payment → Notification으로 이어지는 요청 체인에서, 전체 응답이 2초 걸린다. "어디서 느린가?"를 찾으려면 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 일일이 시간순으로 대조해야 한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">분산 트레이싱 Trace/Span 구조</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Trace ID: abc-123 (전체 요청 1건)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─ Span 1: API Gateway</div><div class="kb-diagram-node">0ms ─── 50ms</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─ Span 2: Auth Service</div><div class="kb-diagram-node">50ms ── 100ms</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─ Span 3: Order Service</div><div class="kb-diagram-node">100ms ─ 800ms</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">병목!</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">│ ─ Span 3.1: DB Query</div><div class="kb-diagram-node">200ms ─ 750ms</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">원인!</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─ Span 4: Payment</div><div class="kb-diagram-node">800ms ─ 1200ms</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─ Span 5: Notification</div><div class="kb-diagram-node">1200ms ─ 1250ms</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">총 응답: 1250ms</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: Trace ID는 택배 송장번호이고, 각 Span은 물류 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))에서의 체류 시간이다. 송장을 추적하면 어느 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)에서 택배가 멈췄는지 즉시 알 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 핵심 개념

| 개념 | 정의 | 비유 |
|:---|:---|:---|
| **Trace** | 하나의 요청이 거치는 전체 경로 | 택배 배송 전체 경로 |
| **Span** | Trace 내 하나의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 처리 구간 | 물류 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) 1곳에서의 체류 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/">Trace ID</a></strong> | 전체 Trace를 식별하는 고유 ID | 택배 송장번호 |
| **Span ID** | 개별 Span을 식별하는 ID | [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)별 스캔 바코드 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/570_trace_id_span_id_context_propagation/">Context Propagation</a></strong> | [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 헤더로 Trace ID를 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 전파 | 송장을 다음 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)로 넘기기 |

### [Context Propagation](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/570_trace_id_span_id_context_propagation/) 방식

W3C Trace [Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 표준: [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 헤더 `traceparent: 00-{trace-id}-{span-id}-{flags}`를 요청에 실어 다음 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 전달한다.

- **📢 섹션 요약 비유**: [Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) Propagation은 릴레이 경주에서 바통([Trace ID](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/))을 다음 주자([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))에게 넘기는 것이다. 바통을 놓치면 추적이 끊긴다.

---

## Ⅲ. 비교 및 연결

| 비교 | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) ([Logs](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)) | [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) ([Metrics](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)) | 트레이싱 (Traces) |
|:---|:---|:---|:---|
| **질문** | 무엇이 일어났나? | 얼마나 나쁜가? | **어디서 병목인가?** |
| **형태** | 텍스트 이벤트 | 시계열 수치 | Span 트리 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a> 대응</strong> | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 집계 | **전체 경로 추적** |
| **도구** | ELK, Loki | [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) | Jaeger, Tempo |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. <strong><a href="/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/">OTel</a> SDK 계측</strong>: 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) SDK 추가 (Auto-instrumentation 권장).
2. **Collector 배포**: [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector를 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 또는 DaemonSet으로 배포하여 Span 수집.
3. **백엔드 선택**: Jaeger(분석)·Tempo(비용 효율)·Datadog([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/)).
4. <strong>샘플링 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>: 전량 수집은 비용 폭발 → Head-based 또는 Tail-based 샘플링.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **샘플링 없이 전량 수집**: 초당 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000 요청 × 5 Span = 50,000 Span/s → 저장 비용 폭발.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 트레이싱 미도입 | 트레이싱 도입 | 개선 |
|:---|:---|:---|:---|
| 병목 특정 시간 | 수시간 ([로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 대조) | <strong>수분 (Span <a href="/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/">시각화</a>)</strong> | 90% 단축 |
| [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) ([복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간) | 30분+ | **10분 이하** | 66% 단축 |
| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 의존성 가시성 | 문서 기반 | <strong>자동 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 맵</strong> | 실시간 |

[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 트레이싱은 [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 기반 무계측(Zero-instrumentation) 추적과 결합하여, 코드 변경 없이 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨에서 Span을 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 방향으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/">OpenTelemetry</a></strong> | 계측 표준, [Metrics](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)·[Logs](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·Traces 통합 SDK |
| **Jaeger / Tempo** | 트레이싱 백엔드 (저장·[시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)) |
| <strong>W3C Trace <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/">Context</a></strong> | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [Trace ID](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/) 전파 표준 헤더 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/">Observability</a></strong> | 트레이싱이 속하는 3대 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 중 하나 |
| <strong><a href="/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/">Service Mesh</a> (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/">Istio</a>)</strong> | [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 프록시가 자동으로 Span [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Google Dapper 논문 (2010) — 분산 트레이싱 개념 정립</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Zipkin (2012, Twitter) — 최초 OSS 분산 트레이싱</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Jaeger (2017, Uber) — CNCF 졸업 프로젝트</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">OpenTelemetry 통합 (2019~) — OpenTracing+OpenCensus 합병</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재: eBPF Zero-instrumentation — 코드 변경 없는 자동 추적</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. 택배를 보내면 <strong>송장번호(<a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/">Trace ID</a>)</strong>로 지금 어디에 있는지 추적할 수 있죠?
2. [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 트레이싱도 인터넷 요청에 송장번호를 붙여서, **어느 컴퓨터에서 오래 멈췄는지** 찾아내요.
3. 덕분에 개발자가 "아! 여기가 느렸구나!"라고 **바로 고칠 수 있답니다!**

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 112 / 973

← **이전**: [111. 관측 가능성 (Observability) - Metrics·Logs·Traces 3대 신호와 SRE 실천](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)
**다음**: [113. 카오스 엔지니어링 (Chaos Engineering) - Chaos Monkey·정상 상태 가설·실험 설계](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/113_chaos_engineering_chaos_monkey/) →

---
