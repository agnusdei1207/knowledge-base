+++
title = "OpenTelemetry CNCF"
date = "2026-05-09"
categories = ["studynote-devops-sre"]
+++

> **핵심 인사이트**
> - [[146_opentelemetry_otel_observability_standard|OpenTelemetry]] ([[146_opentelemetry_otel_observability_standard|OTel]])는 [[567_metrics_time_series_prometheus_grafana|Metrics]]·[[568_logs_distributed_logging_elk_fluentd|Logs]]·Traces 세 기둥을 단일 SDK로 계측하는 [[190_cncf_landscape_observability|CNCF]] ([[199_cloud_native_architecture_msa_cicd_devops|Cloud Native]] Computing Foundation) 표준이다.
> - 벤더 중립적 설계로 Jaeger·[[136_prometheus|Prometheus]]·Datadog 등 어떤 백엔드에도 연결할 수 있다.
> - [[146_opentelemetry_otel_observability_standard|OTel]] Collector가 [[123_pipe|파이프]]라인 중앙에서 수신·처리·내보내기를 담당해 언어별 SDK 변경 없이 백엔드를 교체할 수 있다.

---

## Ⅰ. [[146_opentelemetry_otel_observability_standard|OpenTelemetry]] 등장 배경

이전에는 [[642_observability_telemetry|Observability]] 도구마다 별도 SDK를 사용해야 했다. OpenTelemetry는 OpenCensus(Google)와 OpenTracing([[190_cncf_landscape_observability|CNCF]])의 합병 프로젝트로, 단일 표준 SDK로 [[567_metrics_time_series_prometheus_grafana|Metrics]]·[[568_logs_distributed_logging_elk_fluentd|Logs]]·Traces 모두 계측한다.

```
┌──────────────────────────────────────────────────┐
│           OpenTelemetry 아키텍처                │
│                                                  │
│  앱 → OTel SDK → OTLP → OTel Collector          │
│                             │                   │
│                    ┌────────┼────────┐           │
│                    ▼        ▼        ▼           │
│                 Jaeger  Prometheus  Loki         │
└──────────────────────────────────────────────────┘
```

> 📢 **Ⅰ 섹션 요약 비유**
> OTel은 [[359_usb|USB]]-C 표준 — 기기(SDK)는 하나의 [[446_port_and_bus|포트]]에 연결하고, [[259_adapter_pattern_interface_wrapper|어댑터]](Exporter)를 교체하면 다른 충전기(백엔드)에 꽂힌다.

---

## Ⅱ. [[146_opentelemetry_otel_observability_standard|OTel]] SDK 주요 구성

| 구성 요소         | 역할                                        |
|------------------|---------------------------------------------|
| Tracer [[150_soa_triangle_architecture|Provider]]   | Trace [[087_process_state_transition|생성]] 팩토리                           |
| Meter [[150_soa_triangle_architecture|Provider]]    | [[567_metrics_time_series_prometheus_grafana|Metrics]] 수집 팩토리                         |
| Logger [[150_soa_triangle_architecture|Provider]]   | 구조화 [[568_logs_distributed_logging_elk_fluentd|로그]] 출력 팩토리                      |
| Propagator        | Trace [[033_context|Context]] [[090_service_kubernetes_network_load_balancing|서비스]] 간 전파                |
| Exporter          | [[001_dikw_pyramid|데이터]] 백엔드로 전송 (OTLP, Jaeger, Zipkin) |

OTLP ([[146_opentelemetry_otel_observability_standard|OpenTelemetry]] [[295_protocol_field_tcp_udp_icmp|Protocol]])는 [[479_grpc_protobuf_http2|gRPC]]·[[461_http_stateless_connection_oriented|HTTP]] 기반 표준 전송 [[295_protocol_field_tcp_udp_icmp|프로토콜]]이다.

> 📢 **Ⅱ 섹션 요약 비유**
> Tracer Provider는 GPS [[192_module_independence|모듈]], Meter Provider는 속도계, OTLP는 [[001_dikw_pyramid|데이터]]를 서버로 보내는 통신망이다.

---

## Ⅲ. [[146_opentelemetry_otel_observability_standard|OTel]] Collector [[123_pipe|파이프]]라인

```
Receiver → Processor → Exporter

OTLP Receiver
  ├── Batch Processor (배치 압축)
  ├── Attributes Processor (태그 추가/제거)
  ├── Jaeger Exporter (Trace)
  ├── Prometheus Exporter (Metrics)
  └── Loki Exporter (Logs)
```

Agent 모드([[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]/[[089_daemonset_kubernetes_background_node_agent|데몬셋]])와 Gateway 모드(클러스터 중앙 집결)를 조합해 사용한다.

> 📢 **Ⅲ 섹션 요약 비유**
> Collector는 우편 [[152_hub_dummy_switching_intelligent|허브]] — 여러 곳에서 온 소포를 [[104_classification_analysis|분류]]·처리해 목적지별로 배달한다.

---

## Ⅳ. Auto-Instrumentation

코드 수정 없이 자동 계측:

```bash
# Java
java -javaagent:opentelemetry-javaagent.jar -jar myapp.jar

# Python
opentelemetry-instrument python myapp.py
```

Auto-instrumentation은 [[461_http_stateless_connection_oriented|HTTP]] 클라이언트·DB 드라이버·[[389_mesh_topology|메시]]지 큐 등 인기 [[336_library_vs_framework|라이브러리]]를 자동 계측한다.

> 📢 **Ⅳ 섹션 요약 비유**
> Auto-instrumentation은 자동차 OBD [[446_port_and_bus|포트]]에 꽂기만 하면 모든 주행 [[001_dikw_pyramid|데이터]]를 수집하는 것이다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소           | 역할                                         |
|---------------------|----------------------------------------------|
| [[146_opentelemetry_otel_observability_standard|OpenTelemetry]]       | [[642_observability_telemetry|Observability]] 표준 SDK + [[295_protocol_field_tcp_udp_icmp|프로토콜]]             |
| [[190_cncf_landscape_observability|CNCF]]                | [[199_cloud_native_architecture_msa_cicd_devops|Cloud Native]] [[191_oss_license_compliance|오픈소스]] 프로젝트 관리 재단      |
| OTLP                | [[146_opentelemetry_otel_observability_standard|OTel]] 표준 전송 [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[479_grpc_protobuf_http2|gRPC]]/[[461_http_stateless_connection_oriented|HTTP]])          |
| [[146_opentelemetry_otel_observability_standard|OTel]] Collector      | 수신·처리·내보내기 [[123_pipe|파이프]]라인                |
| Auto-instrumentation| 코드 수정 없는 자동 계측                     |
| Propagator          | [[090_service_kubernetes_network_load_balancing|서비스]] 간 Trace [[033_context|Context]] 전파                 |

### 관련 키워드 및 발전 흐름도

```
OpenTelemetry
    ├── SDK → Metrics / Logs / Traces 계측
    ├── OTLP → 표준 전송 프로토콜
    ├── Collector → 중앙 파이프라인 (Agent + Gateway)
    ├── Auto-instrumentation → 코드리스 계측
    └── CNCF → Cloud Native 표준화
```

> 🧒 **어린이 비유**
> OTel은 모든 가전제품의 리모컨을 하나로 통합하는 만능 리모컨이에요. 어떤 TV(백엔드)에도 같은 버튼(SDK)으로 조종할 수 있어요.
