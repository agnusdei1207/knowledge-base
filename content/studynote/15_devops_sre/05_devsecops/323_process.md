+++
title = "Prometheus Grafana Monitoring"
date = 2026-05-09

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

> **핵심 인사이트**
> - [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) (프로메테우스)는 Pull 방식의 시계열 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 수집 시스템으로, PromQL로 강력한 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 가능하다.
> - [Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/) (그라파나)는 [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/)·Loki·Tempo를 포함한 다양한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)소스를 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)하는 대시보드 도구다.
> - AlertManager (알럿매니저)가 [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) 경보를 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)·그룹핑·[억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/)해 On-[call](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/) 팀에 전달한다.

---

## Ⅰ. [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Prometheus 수집 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Targets → /metrics 노출</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Prometheus Server</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── Service Discovery (K8s, Consul, DNS)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── Scrape (15s 주기 Pull)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── TSDB (시계열 DB) 저장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── PromQL 쿼리 엔진</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">AlertManager → 경보 라우팅 → Slack/PagerDuty</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Grafana → 대시보드 시각화</div></div>
</div>
</div>



Pull 방식 장점: 수집 대상이 Push하지 않아도 되므로 보안·관리가 단순하다.

> 📢 **Ⅰ 섹션 요약 비유**
> Prometheus는 각 매장(앱)을 직접 방문해 재고를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 본사 재고 관리팀 — 매장이 보고하는 게 아니라 본사가 직접 온다.

---

## Ⅱ. PromQL ([Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) Query Language)

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
> PromQL은 시계열 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 위한 Excel 수식 — rate()는 변화율 계산, histogram_quantile()은 분포에서 특정 백분위를 뽑는다.

---

## Ⅲ. AlertManager 경보 관리

AlertManager 주요 기능:
- <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/535_grouping_counting_free_space/">Grouping</a></strong>: 동일 알람을 묶어 알림 폭탄 방지
- **Inhibition**: 심각 알람 발생 시 관련 경고 알람 [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/)
- **Silencing**: 점검 시간 동안 특정 알람 무음 처리

> 📢 **Ⅲ 섹션 요약 비유**
> AlertManager는 비서 — 중요한 연락만 사장에게 보고하고, 관련 없는 알람은 묶거나 조용히 처리한다.

---

## Ⅳ. [Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/) 대시보드 구성

Grafana는 플러그인 기반으로 다양한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)소스를 지원한다:
- [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) ([Metrics](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)), Loki ([Logs](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)), Tempo (Traces), [Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/), [InfluxDB](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/255_time_series_rollup_retention_compression/)

**Exemplar**: [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포인트에 연결된 [Trace ID](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/) — Grafana에서 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) → 트레이스 직접 드릴다운이 가능하다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Grafana</div>
<div class="kb-diagram-tree-item" style="--depth:1">CPU 급등 감지 (Prometheus)</div>
<div class="kb-diagram-note">── Exemplar 클릭 → Trace ID → Tempo 드릴다운</div>
<div class="kb-diagram-tree-item" style="--depth:1">관련 에러 로그 (Loki)</div>
</div>
</div>



> 📢 **Ⅳ 섹션 요약 비유**
> Grafana는 항공 관제탑 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/) — 레이더([Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/)), 통신 기록(Loki), 항적 추적(Tempo)을 한 화면에서 본다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소        | 역할                                    |
|------------------|-----------------------------------------|
| [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/)       | Pull 방식 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 수집·저장·[쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)         |
| PromQL           | 시계열 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어                        |
| AlertManager     | 경보 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)·[억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/)·그룹핑                 |
| [Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/)          | 다중 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)소스 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 대시보드          |
| Exemplar         | [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)-트레이스 연결 드릴다운 포인트    |
| Push Gateway     | 배치 잡 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) Push 수집 게이트웨이     |

### 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Prometheus + Grafana</div>
<div class="kb-diagram-tree-item" style="--depth:2">PromQL → 강력한 시계열 쿼리</div>
<div class="kb-diagram-tree-item" style="--depth:2">AlertManager → 경보 라우팅·억제</div>
<div class="kb-diagram-tree-item" style="--depth:2">Grafana Loki → 로그 통합 시각화</div>
<div class="kb-diagram-tree-item" style="--depth:2">Grafana Tempo → 트레이스 통합</div>
<div class="kb-diagram-tree-item" style="--depth:2">Exemplar → Metrics-to-Trace 드릴다운</div>
</div>
</div>



> 🧒 **어린이 비유**
> Prometheus는 학교 성적 기록부, Grafana는 그 성적을 예쁜 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)로 그려주는 프로그램이에요. AlertManager는 성적이 떨어지면 부모님께 문자를 보내는 시스템이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 323 / 373

← **이전**: [OpenTelemetry CNCF](/knowledge-base/studynote/15_devops_sre/05_devsecops/322_cncf/)
**다음**: [Chaos Engineering](/knowledge-base/studynote/11_design_supervision/06_exam_summary/324_audit/) →

---
