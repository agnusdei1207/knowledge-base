---
title: Prometheus Grafana Monitoring
date: '2026-05-09'
tags:
- studynote-devops-sre
---

> **핵심 인사이트**
> - [[136_prometheus|Prometheus]] (프로메테우스)는 Pull 방식의 시계열 [[342_routing_metric_hop_bandwidth_delay|메트릭]] 수집 시스템으로, PromQL로 강력한 [[298_qkv_attention|쿼리]]가 가능하다.
> - [[168_grafana|Grafana]] (그라파나)는 [[136_prometheus|Prometheus]]·Loki·Tempo를 포함한 다양한 [[001_dikw_pyramid|데이터]]소스를 [[003_bigdata_7v|시각화]]하는 대시보드 도구다.
> - AlertManager (알럿매니저)가 [[136_prometheus|Prometheus]] 경보를 [[339_routing_overview_best_path_selection|라우팅]]·그룹핑·[[656_ir_containment|억제]]해 On-[[189_subroutine_call_return|call]] 팀에 전달한다.

---

## Ⅰ. [[136_prometheus|Prometheus]] 아키텍처

```
┌────────────────────────────────────────────────────┐
│               Prometheus 수집 흐름                │
│                                                    │
│  Targets → /metrics 노출                          │
│                │                                  │
│  Prometheus Server                                │
│  ├── Service Discovery (K8s, Consul, DNS)         │
│  ├── Scrape (15s 주기 Pull)                       │
│  ├── TSDB (시계열 DB) 저장                        │
│  └── PromQL 쿼리 엔진                             │
│                │                                  │
│  AlertManager → 경보 라우팅 → Slack/PagerDuty     │
│  Grafana      → 대시보드 시각화                   │
└────────────────────────────────────────────────────┘
```

Pull 방식 장점: 수집 대상이 Push하지 않아도 되므로 보안·관리가 단순하다.

> 📢 **Ⅰ 섹션 요약 비유**
> Prometheus는 각 매장(앱)을 직접 방문해 재고를 [[396_validation|확인]]하는 본사 재고 관리팀 — 매장이 보고하는 게 아니라 본사가 직접 온다.

---

## Ⅱ. PromQL ([[136_prometheus|Prometheus]] Query Language)

```promql
# HTTP 오류율
rate(http_requests_total{status=~"5.."}[5m])
/ rate(http_requests_total[5m])

# p99 응답시간
histogram_quantile(0.99,
  rate(http_request_duration_seconds_bucket[5m]))
```

| 함수                 | 용도                          |
|----------------------|-------------------------------|
| rate()               | Counter의 초당 증가율          |
| increase()           | 구간 내 증가량                |
| histogram_quantile() | Histogram에서 퀀타일 계산     |
| avg_over_time()      | 구간 평균                     |

> 📢 **Ⅱ 섹션 요약 비유**
> PromQL은 시계열 [[001_dikw_pyramid|데이터]]를 위한 Excel 수식 — rate()는 변화율 계산, histogram_quantile()은 분포에서 특정 백분위를 뽑는다.

---

## Ⅲ. AlertManager 경보 관리

AlertManager 주요 기능:
- **[[535_grouping_counting_free_space|Grouping]]**: 동일 알람을 묶어 알림 폭탄 방지
- **Inhibition**: 심각 알람 발생 시 관련 경고 알람 [[656_ir_containment|억제]]
- **Silencing**: 점검 시간 동안 특정 알람 무음 처리

> 📢 **Ⅲ 섹션 요약 비유**
> AlertManager는 비서 — 중요한 연락만 사장에게 보고하고, 관련 없는 알람은 묶거나 조용히 처리한다.

---

## Ⅳ. [[168_grafana|Grafana]] 대시보드 구성

Grafana는 플러그인 기반으로 다양한 [[001_dikw_pyramid|데이터]]소스를 지원한다:
- [[136_prometheus|Prometheus]] ([[567_metrics_time_series_prometheus_grafana|Metrics]]), Loki ([[568_logs_distributed_logging_elk_fluentd|Logs]]), Tempo (Traces), [[302_cdc|Elasticsearch]], [[255_time_series_rollup_retention_compression|InfluxDB]]

**Exemplar**: [[342_routing_metric_hop_bandwidth_delay|메트릭]] [[001_dikw_pyramid|데이터]] 포인트에 연결된 [[303_trace_id|Trace ID]] — Grafana에서 [[342_routing_metric_hop_bandwidth_delay|메트릭]] → 트레이스 직접 드릴다운이 가능하다.

```
Grafana
  │
  ├── CPU 급등 감지 (Prometheus)
  │       └── Exemplar 클릭 → Trace ID → Tempo 드릴다운
  └── 관련 에러 로그 (Loki)
```

> 📢 **Ⅳ 섹션 요약 비유**
> Grafana는 항공 관제탑 [[229_monitor|모니터]] — 레이더([[136_prometheus|Prometheus]]), 통신 기록(Loki), 항적 추적(Tempo)을 한 화면에서 본다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소        | 역할                                    |
|------------------|-----------------------------------------|
| [[136_prometheus|Prometheus]]       | Pull 방식 [[342_routing_metric_hop_bandwidth_delay|메트릭]] 수집·저장·[[298_qkv_attention|쿼리]]         |
| PromQL           | 시계열 [[298_qkv_attention|쿼리]] 언어                        |
| AlertManager     | 경보 [[339_routing_overview_best_path_selection|라우팅]]·[[656_ir_containment|억제]]·그룹핑                 |
| [[168_grafana|Grafana]]          | 다중 [[001_dikw_pyramid|데이터]]소스 [[003_bigdata_7v|시각화]] 대시보드          |
| Exemplar         | [[342_routing_metric_hop_bandwidth_delay|메트릭]]-트레이스 연결 드릴다운 포인트    |
| Push Gateway     | 배치 잡 [[342_routing_metric_hop_bandwidth_delay|메트릭]] Push 수집 게이트웨이     |

### 관련 키워드 및 발전 흐름도

```
Prometheus + Grafana
    ├── PromQL → 강력한 시계열 쿼리
    ├── AlertManager → 경보 라우팅·억제
    ├── Grafana Loki → 로그 통합 시각화
    ├── Grafana Tempo → 트레이스 통합
    └── Exemplar → Metrics-to-Trace 드릴다운
```

> 🧒 **어린이 비유**
> Prometheus는 학교 성적 기록부, Grafana는 그 성적을 예쁜 [[070_graph_datastructure|그래프]]로 그려주는 프로그램이에요. AlertManager는 성적이 떨어지면 부모님께 문자를 보내는 시스템이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 323 / 373

← **이전**: [[322_cncf|OpenTelemetry CNCF]]
**다음**: [[324_audit|Chaos Engineering]] →

---
