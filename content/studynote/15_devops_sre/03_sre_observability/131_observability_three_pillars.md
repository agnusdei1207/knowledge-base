---
title: 131. 관측 가능성 Three Pillars - Metrics·Logs·Traces 심층 분석
date: '2026-04-19'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[567_metrics_time_series_prometheus_grafana|Metrics]](수치 시계열)·[[568_logs_distributed_logging_elk_fluentd|Logs]](텍스트 이벤트)·Traces([[136_variance|분산]] 요청 추적)는 [[111_observability_metrics_logs_traces|관측 가능성]]의 **3대 필러(Three Pillars)**이며, 세 가지를 **[[325_correlation_analysis_pearson_spearman|상관 분석]](Correlation)**해야 장애 근본 원인을 파악할 수 있다.
> 2. **가치**: Metrics만으로는 "CPU 80%"를 알지만 원인을 모르고, Logs만으로는 에러는 보지만 어디서 발생했는지 모르며, Traces만으로는 느린 구간은 보지만 왜 느린지 모른다. **세 가지를 연결**해야 완전한 진단이 가능하다.
> 3. **판단 포인트**: TraceID·SpanID로 3 Pillars를 연결(Correlation)하고, [[168_grafana|Grafana]] LGTM [[057_stack|Stack]](Loki·[[168_grafana|Grafana]]·Tempo·Mimir)이 [[191_oss_license_compliance|오픈소스]] 관측 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
Metrics: "무엇이" — 에러율 5%↑
Logs:    "왜" — NullPointerException at OrderService
Traces:  "어디서" — Order→Payment→DB 3번째 구간에서 지연
  → TraceID로 3가지를 연결 → 완전한 진단
```

- **📢 섹션 요약 비유**: Metrics는 체온계(숫자), Logs는 의사 진료 기록(텍스트), Traces는 혈류 추적(경로). 셋 다 봐야 정확한 진단.

---

## Ⅱ. 아키텍처 및 핵심 원리

| Pillar | 형태 | 도구 |
|:---|:---|:---|
| **[[567_metrics_time_series_prometheus_grafana|Metrics]]** | 수치 시계열 | [[136_prometheus|Prometheus]], Mimir |
| **[[568_logs_distributed_logging_elk_fluentd|Logs]]** | 텍스트 이벤트 | Loki, ELK |
| **Traces** | [[136_variance|분산]] 요청 추적 | Tempo, Jaeger |

---

## Ⅲ~Ⅴ. 결론

Three Pillars의 **[[325_correlation_analysis_pearson_spearman|상관 분석]](Correlation)**이 [[111_observability_metrics_logs_traces|관측 가능성]]의 진정한 가치이며, [[146_opentelemetry_otel_observability_standard|OpenTelemetry]]+[[168_grafana|Grafana]] Stack이 이를 실현한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[567_metrics_time_series_prometheus_grafana|Metrics]]** | 수치 지표 ([[136_prometheus|Prometheus]]) |
| **[[568_logs_distributed_logging_elk_fluentd|Logs]]** | 텍스트 이벤트 (Loki) |
| **Traces** | [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] (Tempo) |
| **Correlation** | 3 Pillars 연결 (TraceID) |
| **LGTM [[057_stack|Stack]]** | [[168_grafana|Grafana]] 관측 표준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[메트릭만 (Nagios, 2000s)] → [로그 추가 (ELK, 2012~)]
    → [트레이스 추가 (Jaeger, 2016~)]
    → [3 Pillars 통합 (Grafana LGTM, 2020~)]
    → [현재: Profiles (4th Pillar) — 코드 수준 성능 분석]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Metrics는 **체온계**(숫자), Logs는 **진료 기록**(텍스트), Traces는 **혈류 추적**(경로)이에요.
2. 체온계만 보면 "열이 난다"만 알지, **왜 아프고 어디가 아픈지** 몰라요.
3. 셋 다 연결해서 보면 **정확한 병(장애 원인)**을 찾을 수 있답니다!
