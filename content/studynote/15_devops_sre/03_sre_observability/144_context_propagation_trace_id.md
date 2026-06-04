---
title: "144. Context Propagation & Trace ID 전파 상세"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [Context](/studynote/02_operating_system/01_overview_architecture/033_context/) Propagation은 <strong><a href="/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/">Trace ID</a>·Span ID·Baggage를 <a href="/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a> 헤더·<a href="/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/">gRPC</a> <a href="/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a>·<a href="/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/">메시</a>지 큐 <a href="/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/">속성</a>으로 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 간 전파</strong>하여, [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 요청의 전체 호출 체인을 하나의 Trace로 연결하는 메커니즘이다.
> 2. **가치**: 전파가 없으면 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·[메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)이 <strong>독립적으로 <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a></strong>되어 [상관 분석](/studynote/06_ict_convergence/05_data_science/325_correlation_analysis_pearson_spearman/)이 불가능하지만, [Trace ID](/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/) 전파로 <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/">Metrics</a>↔<a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">Logs</a>↔Traces 3축 상관</strong>이 가능해진다.
> 3. **판단 포인트**: W3C traceparent(표준)·B3(Zipkin 레거시)·Jaeger 헤더의 3가지 형식이 있으며, [OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) SDK가 자동 전파를 제공한다. 비동기([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/))에서는 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 헤더로 전파한다.

---

## Ⅰ. 개요 및 필요성

```text
HTTP: traceparent: 00-{traceId}-{spanId}-{flags}
gRPC: metadata에 traceparent 포함
Kafka: message header에 traceparent 포함
자동 전파: OTel SDK -> HTTP Client 인터셉터
```

- **📢 섹션 요약 비유**: [Context](/studynote/02_operating_system/01_overview_architecture/033_context/) Propagation은 <strong>여권</strong>이다. 각 나라([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))를 방문할 때 여권([Trace ID](/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/))을 찍어 <strong>방문 이력</strong>을 추적한다.

---

## Ⅱ~Ⅴ. 결론

[Context](/studynote/02_operating_system/01_overview_architecture/033_context/) Propagation은 <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/">Observability</a> 3축 통합의 핵심</strong>이며, W3C traceparent+[OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) SDK가 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Propagation** | [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 전파 |
| **traceparent** | W3C 표준 |
| <strong><a href="/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/">OTel</a> SDK</strong> | 자동 전파 |
| **Baggage** | 사용자 정의 전파 |
| <strong><a href="/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/">Kafka</a> 헤더</strong> | 비동기 전파 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 헤더 전달 (~2015)] -> [B3 (Zipkin)]
    -> [W3C Trace Context (2020)]
    -> [OTel Auto-instrumentation (2021)]
    -> [현재: 자동 전파 + Baggage 표준화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [Context](/studynote/02_operating_system/01_overview_architecture/033_context/) Propagation은 <strong>여권</strong>이에요. 나라([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))마다 <strong>도장(Span)</strong>을 찍어요.
2. 여권 번호([Trace ID](/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/))로 **어디를 방문했는지** 한눈에 볼 수 있어요.
3. [OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) SDK가 **자동으로 여권을 넘겨줘서** 개발자가 편해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 144 / 373

<- **이전**: [143. Span 상세 - 서비스·오퍼레이션 단위 추적](/studynote/15_devops_sre/03_sre_observability/143_span_service_operation_unit/)
**다음**: [145. Jaeger & Zipkin - 분산 트레이싱 백엔드 비교](/studynote/15_devops_sre/03_sre_observability/145_jaeger_zipkin_distributed_tracing_backend/) ->

---
