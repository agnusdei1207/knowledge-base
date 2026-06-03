+++
title = "OpenTelemetry CNCF"
date = 2026-05-09

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

> **핵심 인사이트**
> - [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) ([OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/))는 [Metrics](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)·[Logs](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·Traces 세 기둥을 단일 SDK로 계측하는 [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) ([Cloud Native](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/) Computing Foundation) 표준이다.
> - 벤더 중립적 설계로 Jaeger·[Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/)·Datadog 등 어떤 백엔드에도 연결할 수 있다.
> - [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector가 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 중앙에서 수신·처리·내보내기를 담당해 언어별 SDK 변경 없이 백엔드를 교체할 수 있다.

---

## Ⅰ. [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 등장 배경

이전에는 [Observability](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) 도구마다 별도 SDK를 사용해야 했다. OpenTelemetry는 OpenCensus(Google)와 OpenTracing([CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/))의 합병 프로젝트로, 단일 표준 SDK로 [Metrics](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)·[Logs](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·Traces 모두 계측한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">OpenTelemetry 아키텍처</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">앱 → OTel SDK → OTLP → OTel Collector</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Jaeger Prometheus Loki</div></div>
</div>
</div>



> 📢 **Ⅰ 섹션 요약 비유**
> OTel은 [USB](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/)-C 표준 — 기기(SDK)는 하나의 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 연결하고, [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)(Exporter)를 교체하면 다른 충전기(백엔드)에 꽂힌다.

---

## Ⅱ. [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) SDK 주요 구성

| 구성 요소         | 역할                                        |
|------------------|---------------------------------------------|
| Tracer [Provider](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/150_soa_triangle_architecture/)   | Trace [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 팩토리                           |
| Meter [Provider](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/150_soa_triangle_architecture/)    | [Metrics](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/) 수집 팩토리                         |
| Logger [Provider](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/150_soa_triangle_architecture/)   | 구조화 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 출력 팩토리                      |
| Propagator        | Trace [Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 전파                |
| Exporter          | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 백엔드로 전송 (OTLP, Jaeger, Zipkin) |

OTLP ([OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))는 [gRPC](/knowledge-base/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/)·[HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 기반 표준 전송 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다.

> 📢 **Ⅱ 섹션 요약 비유**
> Tracer Provider는 GPS [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/), Meter Provider는 속도계, OTLP는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 서버로 보내는 통신망이다.

---

## Ⅲ. [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Receiver → Processor → Exporter</div>
<div class="kb-diagram-note">OTLP Receiver</div>
<div class="kb-diagram-tree-item" style="--depth:1">Batch Processor (배치 압축)</div>
<div class="kb-diagram-tree-item" style="--depth:1">Attributes Processor (태그 추가/제거)</div>
<div class="kb-diagram-tree-item" style="--depth:1">Jaeger Exporter (Trace)</div>
<div class="kb-diagram-tree-item" style="--depth:1">Prometheus Exporter (Metrics)</div>
<div class="kb-diagram-tree-item" style="--depth:1">Loki Exporter (Logs)</div>
</div>
</div>



Agent 모드([사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)/[데몬셋](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/089_daemonset_kubernetes_background_node_agent/))와 Gateway 모드(클러스터 중앙 집결)를 조합해 사용한다.

> 📢 **Ⅲ 섹션 요약 비유**
> Collector는 우편 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) — 여러 곳에서 온 소포를 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)·처리해 목적지별로 배달한다.

---

## Ⅳ. Auto-Instrumentation

코드 수정 없이 자동 계측:

```bash
# Java
java -javaagent:opentelemetry-javaagent.jar -jar myapp.jar

# Python
opentelemetry-instrument python myapp.py
```

Auto-instrumentation은 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 클라이언트·DB 드라이버·[메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐 등 인기 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)를 자동 계측한다.

> 📢 **Ⅳ 섹션 요약 비유**
> Auto-instrumentation은 자동차 OBD [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 꽂기만 하면 모든 주행 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수집하는 것이다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소           | 역할                                         |
|---------------------|----------------------------------------------|
| [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/)       | [Observability](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) 표준 SDK + [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)             |
| [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/)                | [Cloud Native](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/) [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 프로젝트 관리 재단      |
| OTLP                | [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 표준 전송 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) ([gRPC](/knowledge-base/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/)/[HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/))          |
| [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector      | 수신·처리·내보내기 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인                |
| Auto-instrumentation| 코드 수정 없는 자동 계측                     |
| Propagator          | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 Trace [Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 전파                 |

### 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">OpenTelemetry</div>
<div class="kb-diagram-tree-item" style="--depth:2">SDK → Metrics / Logs / Traces 계측</div>
<div class="kb-diagram-tree-item" style="--depth:2">OTLP → 표준 전송 프로토콜</div>
<div class="kb-diagram-tree-item" style="--depth:2">Collector → 중앙 파이프라인 (Agent + Gateway)</div>
<div class="kb-diagram-tree-item" style="--depth:2">Auto-instrumentation → 코드리스 계측</div>
<div class="kb-diagram-tree-item" style="--depth:2">CNCF → Cloud Native 표준화</div>
</div>
</div>



> 🧒 **어린이 비유**
> OTel은 모든 가전제품의 리모컨을 하나로 통합하는 만능 리모컨이에요. 어떤 TV(백엔드)에도 같은 버튼(SDK)으로 조종할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 322 / 373

← **이전**: [Distributed Tracing Trace ID](/knowledge-base/studynote/15_devops_sre/05_devsecops/321_trace_id/)
**다음**: [Prometheus Grafana Monitoring](/knowledge-base/studynote/15_devops_sre/05_devsecops/323_process/) →

---
