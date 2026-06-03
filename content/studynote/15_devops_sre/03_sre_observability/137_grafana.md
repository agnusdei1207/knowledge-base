+++
title = "137. Grafana - 통합 관측 가능성 시각화 플랫폼"
date = 2026-04-19

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Grafana는 **[Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/)·Loki·Tempo·[Elasticsearch](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/) 등 다양한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스를 통합하여 대시보드로 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)**하는 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [관측 가능성](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/) 플랫폼이며, LGTM [Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)(Loki+[Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/)+Tempo+Mimir)의 중심이다.
> 2. **가치**: [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·트레이스를 **하나의 대시보드에서 [상관 분석](/knowledge-base/studynote/06_ict_convergence/05_data_science/325_correlation_analysis_pearson_spearman/)**할 수 있어, 장애 시 "[메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 이상→[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)→트레이스 추적"의 워크플로를 단일 도구에서 수행한다.
> 3. **판단 포인트**: Grafana는 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 레이어이지 저장소가 아니며, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스([Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/)·Loki·Tempo)와의 조합이 핵심이다. [Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/) Cloud는 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)이다.

---

## Ⅰ. 개요 및 필요성

```text
Grafana = 다중 데이터 소스 → 통합 대시보드
  Prometheus (메트릭) + Loki (로그) + Tempo (트레이스)
  → 하나의 대시보드에서 상관 분석
  → 알림 → PagerDuty/Slack
```

- **📢 섹션 요약 비유**: Grafana는 **병원 종합 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)**이다. 심전도·혈압·체온을 **한 화면에서** 동시에 본다.

---

## Ⅱ~Ⅴ. 결론

Grafana는 **[관측 가능성](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)의 "눈([시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/))"**이며, LGTM Stack으로 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 관측 표준을 구축할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/)** | 통합 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) |
| **LGTM [Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)** | Loki+[Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/)+Tempo+Mimir |
| **Dashboard** | 대시보드 |
| **[Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Source** | [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/)·Loki·Tempo |
| **[Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/) Cloud** | 관리형 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[Kibana (ELK, 2012)] → [Grafana (2014, Torkel Ödegaard)]
    → [Grafana Labs (2015~)] → [LGTM Stack (2020~)]
    → [현재: Grafana 11 — Scenes·App Platform]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Grafana는 **병원 종합 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)**예요. 심전도·혈압·체온을 **한 화면에서** 봐요.
2. 여러 기계([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스)의 정보를 **예쁜 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)**로 보여줘요.
3. 이상이 생기면 **알림**을 보내서 바로 알 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 137 / 373

← **이전**: [136. Prometheus - 클라우드 네이티브 메트릭 수집·저장 엔진](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/)
**다음**: [138. 로그 (Logs) - 구조화 로깅과 중앙 집중 관리](/knowledge-base/studynote/15_devops_sre/03_sre_observability/138_logs/) →

---
