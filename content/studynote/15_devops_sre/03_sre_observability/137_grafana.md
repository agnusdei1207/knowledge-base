---
title: 137. Grafana - 통합 관측 가능성 시각화 플랫폼
date: '2026-04-19'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Grafana는 **[[136_prometheus|Prometheus]]·Loki·Tempo·[[302_cdc|Elasticsearch]] 등 다양한 [[001_dikw_pyramid|데이터]] 소스를 통합하여 대시보드로 [[003_bigdata_7v|시각화]]**하는 [[191_oss_license_compliance|오픈소스]] [[111_observability_metrics_logs_traces|관측 가능성]] 플랫폼이며, LGTM [[057_stack|Stack]](Loki+[[168_grafana|Grafana]]+Tempo+Mimir)의 중심이다.
> 2. **가치**: [[342_routing_metric_hop_bandwidth_delay|메트릭]]·[[568_logs_distributed_logging_elk_fluentd|로그]]·트레이스를 **하나의 대시보드에서 [[325_correlation_analysis_pearson_spearman|상관 분석]]**할 수 있어, 장애 시 "[[342_routing_metric_hop_bandwidth_delay|메트릭]] 이상→[[568_logs_distributed_logging_elk_fluentd|로그]] [[396_validation|확인]]→트레이스 추적"의 워크플로를 단일 도구에서 수행한다.
> 3. **판단 포인트**: Grafana는 [[003_bigdata_7v|시각화]] 레이어이지 저장소가 아니며, [[001_dikw_pyramid|데이터]] 소스([[136_prometheus|Prometheus]]·Loki·Tempo)와의 조합이 핵심이다. [[168_grafana|Grafana]] Cloud는 [[309_saas|SaaS]] 관리형 [[090_service_kubernetes_network_load_balancing|서비스]]이다.

---

## Ⅰ. 개요 및 필요성

```text
Grafana = 다중 데이터 소스 → 통합 대시보드
  Prometheus (메트릭) + Loki (로그) + Tempo (트레이스)
  → 하나의 대시보드에서 상관 분석
  → 알림 → PagerDuty/Slack
```

- **📢 섹션 요약 비유**: Grafana는 **병원 종합 [[229_monitor|모니터]]**이다. 심전도·혈압·체온을 **한 화면에서** 동시에 본다.

---

## Ⅱ~Ⅴ. 결론

Grafana는 **[[111_observability_metrics_logs_traces|관측 가능성]]의 "눈([[003_bigdata_7v|시각화]])"**이며, LGTM Stack으로 [[191_oss_license_compliance|오픈소스]] 관측 표준을 구축할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[168_grafana|Grafana]]** | 통합 [[003_bigdata_7v|시각화]] |
| **LGTM [[057_stack|Stack]]** | Loki+[[168_grafana|Grafana]]+Tempo+Mimir |
| **Dashboard** | 대시보드 |
| **[[001_dikw_pyramid|Data]] Source** | [[136_prometheus|Prometheus]]·Loki·Tempo |
| **[[168_grafana|Grafana]] Cloud** | 관리형 [[309_saas|SaaS]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[Kibana (ELK, 2012)] → [Grafana (2014, Torkel Ödegaard)]
    → [Grafana Labs (2015~)] → [LGTM Stack (2020~)]
    → [현재: Grafana 11 — Scenes·App Platform]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Grafana는 **병원 종합 [[229_monitor|모니터]]**예요. 심전도·혈압·체온을 **한 화면에서** 봐요.
2. 여러 기계([[001_dikw_pyramid|데이터]] 소스)의 정보를 **예쁜 [[070_graph_datastructure|그래프]]**로 보여줘요.
3. 이상이 생기면 **알림**을 보내서 바로 알 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 137 / 373

← **이전**: [[136_prometheus|136. Prometheus - 클라우드 네이티브 메트릭 수집·저장 엔진]]
**다음**: [[138_logs|138. 로그 (Logs) - 구조화 로깅과 중앙 집중 관리]] →

---
