+++
title = "130. 모니터링 vs 관측 가능성 심화 - MELT와 OpenTelemetry"
date = 2026-04-19

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MELT([Metrics](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)·Events·[Logs](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·Traces)는 [관측 가능성](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)의 <strong>4가지 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/">신호</a></strong>이며, [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/)([OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/))가 이를 <strong>벤더 중립적으로 통합 수집</strong>하는 [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 표준이다.
> 2. **가치**: 과거에는 [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/)([메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/))+ELK([로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))+Jaeger(트레이스)를 각각 계측했지만, OTel은 <strong>단일 SDK로 3가지를 동시 수집</strong>하여 통합 관측을 실현한다.
> 3. **판단 포인트**: [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector가 에이전트/게이트웨이로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수집·변환·전송하며, 벤더(Datadog·[New](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) Relic·[Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/) Cloud)에 종속되지 않는 것이 핵심 장점이다.

---

## Ⅰ. 개요 및 필요성

```text
OTel 아키텍처:
  앱 -> OTel SDK -> OTel Collector -> 백엔드
         (자동 계측)   (수집·변환)   (Grafana/Datadog)
```

- **📢 섹션 요약 비유**: OTel은 [USB](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/)-C 충전기이다. 어떤 기기(벤더)든 <strong>하나의 케이블(<a href="/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/">OTel</a>)</strong>로 연결된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) | 설명 | 도구 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/">Metrics</a></strong> | 수치 지표 | [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) |
| **Events** | 이벤트 | - |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">Logs</a></strong> | 텍스트 기록 | Loki |
| **Traces** | [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/) | Tempo |

---

## Ⅲ~Ⅴ. 결론

OpenTelemetry는 <strong><a href="/knowledge-base/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/">벤더 종속</a> 없는 <a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/">관측 가능성</a>의 산업 표준</strong>이며, 모든 [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 프로젝트의 관측 기반이 되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/">OpenTelemetry</a></strong> | [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 관측 표준 |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/">OTel</a> Collector</strong> | 수집·변환·전송 |
| **MELT** | 4가지 관측 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) |
| <strong><a href="/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/">Grafana</a> <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/">Stack</a></strong> | LGTM (Loki+[Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/)+Tempo+Mimir) |
| **벤더 중립** | OTel의 핵심 가치 |

### 📈 관련 키워드 및 발전 흐름도

```text
[OpenTracing + OpenCensus (2016~)] -> [OpenTelemetry 통합 (2019)]
    -> [OTel GA (2023, Traces+Metrics)]
    -> [OTel Logs GA (2024)]
    -> [현재: OTel Profiling — 프로파일링까지 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. OpenTelemetry는 <strong>만능 충전기(<a href="/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/">USB</a>-C)</strong>예요. 어떤 벤더(기기)든 <strong>하나로 연결</strong>돼요.
2. 예전에는 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·트레이스마다 <strong>다른 충전기</strong>가 필요했어요.
3. [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 덕분에 <strong>하나의 도구</strong>로 모든 관측 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 모을 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 130 / 373

<- **이전**: [129. 관측 가능성 vs 모니터링 (Observability vs Monitoring)](/knowledge-base/studynote/15_devops_sre/03_sre_observability/129_observability_vs_monitoring/)
**다음**: [131. 관측 가능성 Three Pillars - Metrics·Logs·Traces 심층 분석](/knowledge-base/studynote/15_devops_sre/03_sre_observability/131_observability_three_pillars/) ->

---
