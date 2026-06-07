---
title: "Observability Metrics Logs Traces"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 320
---
> **핵심 인사이트**
> - [Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) ([관측 가능성](/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/))는 [Metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)·[Logs](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·Traces 세 기둥(Three Pillars)으로 시스템 내부 상태를 외부에서 추론하는 능력이다.
> - Monitoring([모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링)은 알고 있는 것을 감시하지만, Observability는 알 수 없는 것도 질문할 수 있게 한다.
> - [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 단일 지표로는 문제 진단이 불가능하기 때문에 세 기둥의 상관관계 분석이 필수다.

---

## Ⅰ. Three Pillars of [Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)

```
+------------------------------------------------------+
|             Observability 세 기둥                   |
|                                                      |
|  Metrics (수치 집계)  Logs (이벤트)  Traces (흐름)  |
|     무엇이               왜              어디서       |
+------------------------------------------------------+
```

| 기둥      | 질문               | 도구 예시                     |
|-----------|-------------------|-------------------------------|
| [Metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)   | 무엇이 느린가?     | [Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/), Datadog           |
| [Logs](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)      | 왜 오류가 났나?    | ELK [Stack](/studynote/08_algorithm_stats/04_datastructure/057_stack/), Loki              |
| Traces    | 어느 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 병목?  | Jaeger, Zipkin, Tempo         |

> 📢 **Ⅰ 섹션 요약 비유**
> Metrics는 체중계, Logs는 일기, Traces는 GPS 이동 경로 — 셋이 함께야 건강 상태를 정확히 안다.

---

## Ⅱ. [Metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/) ([메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/))

4가지 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 유형([Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/) 기준):

| 타입      | 특성                   | 예시              |
|-----------|------------------------|-------------------|
| [Counter](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)   | 단조 증가 [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)        | [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 요청 총 수    |
| Gauge     | 오르내리는 현재값       | 메모리 사용량      |
| Histogram | 버킷별 분포 측정        | 응답시간 분포      |
| [Summary](/studynote/14_data_engineering/05_exam_keywords/300_summary/)   | 퀀타일(p50, p99) 계산  | 레이턴시 p99      |

> 📢 **Ⅱ 섹션 요약 비유**
> Counter는 걸음 수 측정기, Gauge는 온도계, Histogram은 성적 분포표다.

---

## Ⅲ. [Logs](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) ([로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))

구조화 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)([Structured Logging](/studynote/15_devops_sre/03_sre_observability/140_structured_logging_json_format/))는 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 형식으로 ELK 또는 Loki에서 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)·필터링이 쉽다.

```
{timestamp, level, service, trace_id, message, latency_ms}
```

> 📢 **Ⅲ 섹션 요약 비유**
> 구조화 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 정형화된 업무 보고서 — 날짜·담당자·결과가 정해진 형식에 맞아야 검색이 빠르다.

---

## Ⅳ. Traces (트레이스)와 [Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) 연결

Distributed Tracing은 단일 요청이 여러 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 거치는 경로를 Trace ID로 연결해 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)한다.

```
User Request -> API Gateway -> Order Svc -> Inventory Svc -> DB
      Trace ID: xyz   Span 1         Span 2           Span 3
```

세 기둥 연결 흐름:
- Alert([Metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)) -> 문제 시간대 특정
- Log 검색 -> 에러 원인 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)
- Trace [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/) -> 병목 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 특정

> 📢 **Ⅳ 섹션 요약 비유**
> 택배 추적 시스템이 [Tracing](/studynote/04_software_engineering/uncategorized/657_observability/) — 어느 물류센터에서 얼마나 지체됐는지 한눈에 보인다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소          | 역할                               |
|--------------------|------------------------------------|
| [Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)      | 시스템 내부 상태 외부 추론 능력     |
| [Metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)            | 집계 수치 시계열 지표               |
| [Logs](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)               | 이벤트 텍스트 기록                 |
| Traces             | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 요청 흐름 추적                |
| [Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/)         | [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 수집·저장 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)          |
| ELK / Loki         | [로그 수집](/studynote/09_security/13_secops_ir_forensics/626_log_collection/)·검색 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)                |
| Jaeger / Tempo     | [분산 트레이싱](/studynote/04_software_engineering/02_requirements_analysis/112_distributed_tracing_microservices/) 백엔드               |

### 관련 키워드 및 발전 흐름도

```
Observability
    +-- Metrics -> Prometheus + Grafana
    +-- Logs -> ELK Stack / Loki
    +-- Traces -> Jaeger / Zipkin / Tempo
    +-- OpenTelemetry -> 세 기둥 통합 표준 SDK
```

> 🧒 **어린이 비유**
> 몸이 아플 때 체온계([Metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/))·의사 일지([Logs](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))·혈액 이동 경로 사진(Traces), 이 세 가지가 있어야 정확한 진단이 가능해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 320 / 373

<- **이전**: [Blameless Postmortem](/studynote/15_devops_sre/05_devsecops/319_process/)
**다음**: [Distributed Tracing Trace ID](/studynote/15_devops_sre/05_devsecops/321_trace_id/) ->

---
