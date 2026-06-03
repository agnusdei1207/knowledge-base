+++
weight = 144
title = "144. Context Propagation & Trace ID 전파 상세"
date = "2026-04-19"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[033_context|Context]] Propagation은 **[[303_trace_id|Trace ID]]·Span ID·Baggage를 [[461_http_stateless_connection_oriented|HTTP]] 헤더·[[479_grpc_protobuf_http2|gRPC]] [[012_metadata|메타데이터]]·[[389_mesh_topology|메시]]지 큐 [[082_attribute_types_er_model|속성]]으로 [[090_service_kubernetes_network_load_balancing|서비스]] 간 전파**하여, [[136_variance|분산]] 요청의 전체 호출 체인을 하나의 Trace로 연결하는 메커니즘이다.
> 2. **가치**: 전파가 없으면 각 [[090_service_kubernetes_network_load_balancing|서비스]]의 [[568_logs_distributed_logging_elk_fluentd|로그]]·[[342_routing_metric_hop_bandwidth_delay|메트릭]]이 **독립적으로 [[136_variance|분산]]**되어 [[325_correlation_analysis_pearson_spearman|상관 분석]]이 불가능하지만, [[303_trace_id|Trace ID]] 전파로 **[[567_metrics_time_series_prometheus_grafana|Metrics]]↔[[568_logs_distributed_logging_elk_fluentd|Logs]]↔Traces 3축 상관**이 가능해진다.
> 3. **판단 포인트**: W3C traceparent(표준)·B3(Zipkin 레거시)·Jaeger 헤더의 3가지 형식이 있으며, [[146_opentelemetry_otel_observability_standard|OTel]] SDK가 자동 전파를 제공한다. 비동기([[179_kafka_flink_watermark_time_window|Kafka]])에서는 [[389_mesh_topology|메시]]지 헤더로 전파한다.

---

## Ⅰ. 개요 및 필요성

```text
HTTP: traceparent: 00-{traceId}-{spanId}-{flags}
gRPC: metadata에 traceparent 포함
Kafka: message header에 traceparent 포함
자동 전파: OTel SDK → HTTP Client 인터셉터
```

- **📢 섹션 요약 비유**: [[033_context|Context]] Propagation은 **여권**이다. 각 나라([[090_service_kubernetes_network_load_balancing|서비스]])를 방문할 때 여권([[303_trace_id|Trace ID]])을 찍어 **방문 이력**을 추적한다.

---

## Ⅱ~Ⅴ. 결론

[[033_context|Context]] Propagation은 **[[642_observability_telemetry|Observability]] 3축 통합의 핵심**이며, W3C traceparent+[[146_opentelemetry_otel_observability_standard|OTel]] SDK가 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Propagation** | [[033_context|컨텍스트]] 전파 |
| **traceparent** | W3C 표준 |
| **[[146_opentelemetry_otel_observability_standard|OTel]] SDK** | 자동 전파 |
| **Baggage** | 사용자 정의 전파 |
| **[[179_kafka_flink_watermark_time_window|Kafka]] 헤더** | 비동기 전파 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 헤더 전달 (~2015)] → [B3 (Zipkin)]
    → [W3C Trace Context (2020)]
    → [OTel Auto-instrumentation (2021)]
    → [현재: 자동 전파 + Baggage 표준화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[033_context|Context]] Propagation은 **여권**이에요. 나라([[090_service_kubernetes_network_load_balancing|서비스]])마다 **도장(Span)**을 찍어요.
2. 여권 번호([[303_trace_id|Trace ID]])로 **어디를 방문했는지** 한눈에 볼 수 있어요.
3. [[146_opentelemetry_otel_observability_standard|OTel]] SDK가 **자동으로 여권을 넘겨줘서** 개발자가 편해요!
