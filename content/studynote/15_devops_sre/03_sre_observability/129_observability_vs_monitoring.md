---
title: 129. 관측 가능성 vs 모니터링 (Observability vs Monitoring)
date: '2026-04-19'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[229_monitor|모니터]]링은 **"사전에 예상한 문제를 대시보드로 감시"**하는 것이고, [[111_observability_metrics_logs_traces|관측 가능성]]([[642_observability_telemetry|Observability]])은 **"예상하지 못한 문제도 시스템 출력([[342_routing_metric_hop_bandwidth_delay|메트릭]]·[[568_logs_distributed_logging_elk_fluentd|로그]]·트레이스)만으로 내부 상태를 추론"**할 수 있는 시스템 [[082_attribute_types_er_model|속성]]이다.
> 2. **가치**: [[229_monitor|모니터]]링만으로는 "CPU 80% 알림"은 받지만 **"왜 80%인지"를 모르고**, [[111_observability_metrics_logs_traces|관측 가능성]]은 트레이스·[[568_logs_distributed_logging_elk_fluentd|로그]]를 따라가며 **근본 원인을 실시간 탐색**할 수 있다.
> 3. **판단 포인트**: [[111_observability_metrics_logs_traces|관측 가능성]]의 3대 축(Three Pillars)은 **[[342_routing_metric_hop_bandwidth_delay|메트릭]]([[567_metrics_time_series_prometheus_grafana|Metrics]])·[[568_logs_distributed_logging_elk_fluentd|로그]]([[568_logs_distributed_logging_elk_fluentd|Logs]])·트레이스(Traces)**이며, OpenTelemetry가 통합 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    3 Pillars of Observability                         │
├───────────────────────────────────────────────────────┤
│  [Metrics]  수치 지표 — CPU·메모리·요청 수           │
│             → Prometheus, Grafana                     │
│  [Logs]     이벤트 기록 — 에러 메시지·스택트레이스   │
│             → Elasticsearch, Loki                     │
│  [Traces]   요청 흐름 — 서비스 A→B→C 추적           │
│             → Jaeger, Tempo                           │
│                                                       │
│  OpenTelemetry: 3가지를 통합 수집하는 표준           │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[229_monitor|모니터]]링은 체온계(예상 지표만 측정), [[111_observability_metrics_logs_traces|관측 가능성]]은 MRI(내부를 자유롭게 탐색)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 비교 | [[229_monitor|모니터]]링 | [[111_observability_metrics_logs_traces|관측 가능성]] |
|:---|:---|:---|
| **질문** | "알려진 문제 발생?" | **"왜 이런 현상?"** |
| **방식** | 대시보드·알림 | **탐색·[[325_correlation_analysis_pearson_spearman|상관 분석]]** |
| **범위** | 사전 정의 | **자유 질의** |

---

## Ⅲ. 비교 및 연결

| 필러 | 용도 | 도구 |
|:---|:---|:---|
| **[[567_metrics_time_series_prometheus_grafana|Metrics]]** | 추세·알림 | [[136_prometheus|Prometheus]] |
| **[[568_logs_distributed_logging_elk_fluentd|Logs]]** | 상세 이벤트 | ELK, Loki |
| **Traces** | [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] | Jaeger, Tempo |

---

## Ⅳ~Ⅴ. 결론

[[111_observability_metrics_logs_traces|관측 가능성]]은 **[[619_msa_traffic_hardware|MSA]] 시대 운영의 필수 [[082_attribute_types_er_model|속성]]**이며, OpenTelemetry가 [[342_routing_metric_hop_bandwidth_delay|메트릭]]·[[568_logs_distributed_logging_elk_fluentd|로그]]·트레이스를 통합하는 산업 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[567_metrics_time_series_prometheus_grafana|Metrics]]** | 수치 지표 ([[136_prometheus|Prometheus]]) |
| **[[568_logs_distributed_logging_elk_fluentd|Logs]]** | 이벤트 기록 (ELK) |
| **Traces** | [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] (Jaeger) |
| **[[146_opentelemetry_otel_observability_standard|OpenTelemetry]]** | 통합 수집 표준 |
| **[[100_sre_site_reliability_engineering_error_budget|SRE]]** | [[111_observability_metrics_logs_traces|관측 가능성]]의 운영 조직 |

### 📈 관련 키워드 및 발전 흐름도

```text
[SNMP 모니터링 (2000s)] → [ELK Stack (2012~)]
    → [분산 트레이싱 (Zipkin/Jaeger, 2016~)]
    → [OpenTelemetry (2019~) — 통합 표준]
    → [현재: AIOps — AI가 3 Pillars 자동 상관 분석]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[229_monitor|모니터]]링은 **체온계**예요. 열이 나는지(예상 문제)만 [[396_validation|확인]]해요.
2. [[111_observability_metrics_logs_traces|관측 가능성]]은 **MRI**예요. **왜 아픈지** 몸 속을 자세히 볼 수 있어요.
3. MRI(3 Pillars)가 있으면 **예상 못 한 병**도 찾을 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 129 / 373

← **이전**: [[128_blameless_postmortem|128. Blameless Postmortem - 비난 없는 장애 사후 분석]]
**다음**: [[130_monitoring_vs_observability|130. 모니터링 vs 관측 가능성 심화 - MELT와 OpenTelemetry]] →

---
