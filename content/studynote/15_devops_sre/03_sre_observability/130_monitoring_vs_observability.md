---
title: 130. 모니터링 vs 관측 가능성 심화 - MELT와 OpenTelemetry
date: '2026-04-19'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MELT([[567_metrics_time_series_prometheus_grafana|Metrics]]·Events·[[568_logs_distributed_logging_elk_fluentd|Logs]]·Traces)는 [[111_observability_metrics_logs_traces|관측 가능성]]의 **4가지 [[130_signal|신호]]**이며, [[146_opentelemetry_otel_observability_standard|OpenTelemetry]]([[146_opentelemetry_otel_observability_standard|OTel]])가 이를 **벤더 중립적으로 통합 수집**하는 [[190_cncf_landscape_observability|CNCF]] 표준이다.
> 2. **가치**: 과거에는 [[136_prometheus|Prometheus]]([[342_routing_metric_hop_bandwidth_delay|메트릭]])+ELK([[568_logs_distributed_logging_elk_fluentd|로그]])+Jaeger(트레이스)를 각각 계측했지만, OTel은 **단일 SDK로 3가지를 동시 수집**하여 통합 관측을 실현한다.
> 3. **판단 포인트**: [[146_opentelemetry_otel_observability_standard|OTel]] Collector가 에이전트/게이트웨이로 [[001_dikw_pyramid|데이터]]를 수집·변환·전송하며, 벤더(Datadog·[[087_process_state_transition|New]] Relic·[[168_grafana|Grafana]] Cloud)에 종속되지 않는 것이 핵심 장점이다.

---

## Ⅰ. 개요 및 필요성

```text
OTel 아키텍처:
  앱 → OTel SDK → OTel Collector → 백엔드
         (자동 계측)   (수집·변환)   (Grafana/Datadog)
```

- **📢 섹션 요약 비유**: OTel은 [[359_usb|USB]]-C 충전기이다. 어떤 기기(벤더)든 **하나의 케이블([[146_opentelemetry_otel_observability_standard|OTel]])**로 연결된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| [[130_signal|신호]] | 설명 | 도구 |
|:---|:---|:---|
| **[[567_metrics_time_series_prometheus_grafana|Metrics]]** | 수치 지표 | [[136_prometheus|Prometheus]] |
| **Events** | 이벤트 | - |
| **[[568_logs_distributed_logging_elk_fluentd|Logs]]** | 텍스트 기록 | Loki |
| **Traces** | [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] | Tempo |

---

## Ⅲ~Ⅴ. 결론

OpenTelemetry는 **[[051_vendor_lock_in_cloud_computing|벤더 종속]] 없는 [[111_observability_metrics_logs_traces|관측 가능성]]의 산업 표준**이며, 모든 [[190_cncf_landscape_observability|CNCF]] 프로젝트의 관측 기반이 되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[146_opentelemetry_otel_observability_standard|OpenTelemetry]]** | [[190_cncf_landscape_observability|CNCF]] 관측 표준 |
| **[[146_opentelemetry_otel_observability_standard|OTel]] Collector** | 수집·변환·전송 |
| **MELT** | 4가지 관측 [[130_signal|신호]] |
| **[[168_grafana|Grafana]] [[057_stack|Stack]]** | LGTM (Loki+[[168_grafana|Grafana]]+Tempo+Mimir) |
| **벤더 중립** | OTel의 핵심 가치 |

### 📈 관련 키워드 및 발전 흐름도

```text
[OpenTracing + OpenCensus (2016~)] → [OpenTelemetry 통합 (2019)]
    → [OTel GA (2023, Traces+Metrics)]
    → [OTel Logs GA (2024)]
    → [현재: OTel Profiling — 프로파일링까지 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. OpenTelemetry는 **만능 충전기([[359_usb|USB]]-C)**예요. 어떤 벤더(기기)든 **하나로 연결**돼요.
2. 예전에는 [[342_routing_metric_hop_bandwidth_delay|메트릭]]·[[568_logs_distributed_logging_elk_fluentd|로그]]·트레이스마다 **다른 충전기**가 필요했어요.
3. [[146_opentelemetry_otel_observability_standard|OTel]] 덕분에 **하나의 도구**로 모든 관측 [[001_dikw_pyramid|데이터]]를 모을 수 있답니다!
