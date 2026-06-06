---
title: "Observability vs Monitoring"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링은 <strong>"사전에 예상한 문제를 대시보드로 감시"</strong>하는 것이고, [관측 가능성](/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)([Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/))은 <strong>"예상하지 못한 문제도 시스템 출력(<a href="/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/">메트릭</a>·<a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a>·트레이스)만으로 내부 상태를 추론"</strong>할 수 있는 시스템 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)이다.
> 2. **가치**: [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링만으로는 "CPU 80% 알림"은 받지만 **"왜 80%인지"를 모르고**, [관측 가능성](/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)은 트레이스·[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 따라가며 <strong>근본 원인을 실시간 탐색</strong>할 수 있다.
> 3. **판단 포인트**: [관측 가능성](/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)의 3대 축(Three Pillars)은 <strong><a href="/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/">메트릭</a>(<a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/">Metrics</a>)·<a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a>(<a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">Logs</a>)·트레이스(Traces)</strong>이며, OpenTelemetry가 통합 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    3 Pillars of Observability                         |
+-------------------------------------------------------+
|  [Metrics]  수치 지표 — CPU·메모리·요청 수           |
|             -> Prometheus, Grafana                     |
|  [Logs]     이벤트 기록 — 에러 메시지·스택트레이스   |
|             -> Elasticsearch, Loki                     |
|  [Traces]   요청 흐름 — 서비스 A->B->C 추적           |
|             -> Jaeger, Tempo                           |
|                                                       |
|  OpenTelemetry: 3가지를 통합 수집하는 표준           |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링은 체온계(예상 지표만 측정), [관측 가능성](/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)은 MRI(내부를 자유롭게 탐색)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 비교 | [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 | [관측 가능성](/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/) |
|:---|:---|:---|
| **질문** | "알려진 문제 발생?" | **"왜 이런 현상?"** |
| **방식** | 대시보드·알림 | <strong>탐색·<a href="/studynote/06_ict_convergence/05_data_science/325_correlation_analysis_pearson_spearman/">상관 분석</a></strong> |
| **범위** | 사전 정의 | **자유 질의** |

---

## Ⅲ. 비교 및 연결

| 필러 | 용도 | 도구 |
|:---|:---|:---|
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/">Metrics</a></strong> | 추세·알림 | [Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/) |
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">Logs</a></strong> | 상세 이벤트 | ELK, Loki |
| **Traces** | [분산 추적](/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/) | Jaeger, Tempo |

---

## Ⅳ~Ⅴ. 결론

[관측 가능성](/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)은 <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a> 시대 운영의 필수 <a href="/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/">속성</a></strong>이며, OpenTelemetry가 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·트레이스를 통합하는 산업 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/">Metrics</a></strong> | 수치 지표 ([Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/)) |
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">Logs</a></strong> | 이벤트 기록 (ELK) |
| **Traces** | [분산 추적](/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/) (Jaeger) |
| <strong><a href="/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/">OpenTelemetry</a></strong> | 통합 수집 표준 |
| <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/">SRE</a></strong> | [관측 가능성](/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)의 운영 조직 |

### 📈 관련 키워드 및 발전 흐름도

```text
[SNMP 모니터링 (2000s)] -> [ELK Stack (2012~)]
    -> [분산 트레이싱 (Zipkin/Jaeger, 2016~)]
    -> [OpenTelemetry (2019~) — 통합 표준]
    -> [현재: AIOps — AI가 3 Pillars 자동 상관 분석]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링은 <strong>체온계</strong>예요. 열이 나는지(예상 문제)만 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해요.
2. [관측 가능성](/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)은 <strong>MRI</strong>예요. **왜 아픈지** 몸 속을 자세히 볼 수 있어요.
3. MRI(3 Pillars)가 있으면 <strong>예상 못 한 병</strong>도 찾을 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 129 / 373

<- **이전**: [128. Blameless Postmortem - 비난 없는 장애 사후 분석](/studynote/15_devops_sre/03_sre_observability/128_blameless_postmortem/)
**다음**: [130. 모니터링 vs 관측 가능성 심화 - MELT와 OpenTelemetry](/studynote/15_devops_sre/03_sre_observability/130_monitoring_vs_observability/) ->

---
