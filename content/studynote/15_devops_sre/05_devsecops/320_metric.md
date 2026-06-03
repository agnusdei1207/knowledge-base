---
title: Observability Metrics Logs Traces
date: '2026-05-09'
tags:
- studynote-devops-sre
---

> **핵심 인사이트**
> - [[642_observability_telemetry|Observability]] ([[111_observability_metrics_logs_traces|관측 가능성]])는 [[567_metrics_time_series_prometheus_grafana|Metrics]]·[[568_logs_distributed_logging_elk_fluentd|Logs]]·Traces 세 기둥(Three Pillars)으로 시스템 내부 상태를 외부에서 추론하는 능력이다.
> - Monitoring([[229_monitor|모니터]]링)은 알고 있는 것을 감시하지만, Observability는 알 수 없는 것도 질문할 수 있게 한다.
> - [[136_variance|분산]] 시스템에서 단일 지표로는 문제 진단이 불가능하기 때문에 세 기둥의 상관관계 분석이 필수다.

---

## Ⅰ. Three Pillars of [[642_observability_telemetry|Observability]]

```
┌──────────────────────────────────────────────────────┐
│             Observability 세 기둥                   │
│                                                      │
│  Metrics (수치 집계)  Logs (이벤트)  Traces (흐름)  │
│     무엇이               왜              어디서       │
└──────────────────────────────────────────────────────┘
```

| 기둥      | 질문               | 도구 예시                     |
|-----------|-------------------|-------------------------------|
| [[567_metrics_time_series_prometheus_grafana|Metrics]]   | 무엇이 느린가?     | [[136_prometheus|Prometheus]], Datadog           |
| [[568_logs_distributed_logging_elk_fluentd|Logs]]      | 왜 오류가 났나?    | ELK [[057_stack|Stack]], Loki              |
| Traces    | 어느 [[090_service_kubernetes_network_load_balancing|서비스]] 병목?  | Jaeger, Zipkin, Tempo         |

> 📢 **Ⅰ 섹션 요약 비유**
> Metrics는 체중계, Logs는 일기, Traces는 GPS 이동 경로 — 셋이 함께야 건강 상태를 정확히 안다.

---

## Ⅱ. [[567_metrics_time_series_prometheus_grafana|Metrics]] ([[342_routing_metric_hop_bandwidth_delay|메트릭]])

4가지 [[342_routing_metric_hop_bandwidth_delay|메트릭]] 유형([[136_prometheus|Prometheus]] 기준):

| 타입      | 특성                   | 예시              |
|-----------|------------------------|-------------------|
| [[059_counter|Counter]]   | 단조 증가 [[059_counter|카운터]]        | [[461_http_stateless_connection_oriented|HTTP]] 요청 총 수    |
| Gauge     | 오르내리는 현재값       | 메모리 사용량      |
| Histogram | 버킷별 분포 측정        | 응답시간 분포      |
| [[300_summary|Summary]]   | 퀀타일(p50, p99) 계산  | 레이턴시 p99      |

> 📢 **Ⅱ 섹션 요약 비유**
> Counter는 걸음 수 측정기, Gauge는 온도계, Histogram은 성적 분포표다.

---

## Ⅲ. [[568_logs_distributed_logging_elk_fluentd|Logs]] ([[568_logs_distributed_logging_elk_fluentd|로그]])

구조화 [[568_logs_distributed_logging_elk_fluentd|로그]]([[140_structured_logging_json_format|Structured Logging]])는 [[343_json|JSON]] 형식으로 ELK 또는 Loki에서 [[298_qkv_attention|쿼리]]·필터링이 쉽다.

```
{timestamp, level, service, trace_id, message, latency_ms}
```

> 📢 **Ⅲ 섹션 요약 비유**
> 구조화 [[568_logs_distributed_logging_elk_fluentd|로그]]는 정형화된 업무 보고서 — 날짜·담당자·결과가 정해진 형식에 맞아야 검색이 빠르다.

---

## Ⅳ. Traces (트레이스)와 [[642_observability_telemetry|Observability]] 연결

Distributed Tracing은 단일 요청이 여러 [[090_service_kubernetes_network_load_balancing|서비스]]를 거치는 경로를 Trace ID로 연결해 [[003_bigdata_7v|시각화]]한다.

```
User Request → API Gateway → Order Svc → Inventory Svc → DB
      Trace ID: xyz   Span 1         Span 2           Span 3
```

세 기둥 연결 흐름:
- Alert([[567_metrics_time_series_prometheus_grafana|Metrics]]) → 문제 시간대 특정
- Log 검색 → 에러 원인 [[396_validation|확인]]
- Trace [[003_bigdata_7v|시각화]] → 병목 [[090_service_kubernetes_network_load_balancing|서비스]] 특정

> 📢 **Ⅳ 섹션 요약 비유**
> 택배 추적 시스템이 [[657_observability|Tracing]] — 어느 물류센터에서 얼마나 지체됐는지 한눈에 보인다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소          | 역할                               |
|--------------------|------------------------------------|
| [[642_observability_telemetry|Observability]]      | 시스템 내부 상태 외부 추론 능력     |
| [[567_metrics_time_series_prometheus_grafana|Metrics]]            | 집계 수치 시계열 지표               |
| [[568_logs_distributed_logging_elk_fluentd|Logs]]               | 이벤트 텍스트 기록                 |
| Traces             | [[136_variance|분산]] 요청 흐름 추적                |
| [[136_prometheus|Prometheus]]         | [[342_routing_metric_hop_bandwidth_delay|메트릭]] 수집·저장 [[191_oss_license_compliance|오픈소스]]          |
| ELK / Loki         | [[626_log_collection|로그 수집]]·검색 [[057_stack|스택]]                |
| Jaeger / Tempo     | [[112_distributed_tracing_microservices|분산 트레이싱]] 백엔드               |

### 관련 키워드 및 발전 흐름도

```
Observability
    ├── Metrics → Prometheus + Grafana
    ├── Logs → ELK Stack / Loki
    ├── Traces → Jaeger / Zipkin / Tempo
    └── OpenTelemetry → 세 기둥 통합 표준 SDK
```

> 🧒 **어린이 비유**
> 몸이 아플 때 체온계([[567_metrics_time_series_prometheus_grafana|Metrics]])·의사 일지([[568_logs_distributed_logging_elk_fluentd|Logs]])·혈액 이동 경로 사진(Traces), 이 세 가지가 있어야 정확한 진단이 가능해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 320 / 373

← **이전**: [[319_process|Blameless Postmortem]]
**다음**: [[321_trace_id|Distributed Tracing Trace ID]] →

---
