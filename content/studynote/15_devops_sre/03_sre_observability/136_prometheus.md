---
title: "Prometheus"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 136
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Prometheus는 <strong>Pull 방식으로 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>의 /<a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/">metrics</a> 엔드포인트에서 시계열 <a href="/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/">메트릭</a>을 수집·저장</strong>하는 [CNCF](/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 졸업 프로젝트이며, [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링의 사실상 표준이다.
> 2. **가치**: Push 기반(StatsD)은 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 시스템에 종속되지만, Prometheus의 Pull은 <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>가 <a href="/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/">메트릭</a>을 노출만 하면</strong> Prometheus가 주기적으로 가져가므로 느슨한 결합이다.
> 3. **판단 포인트**: PromQL([쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어)·Alertmanager(알림)·[Service Discovery](/studynote/12_it_management/05_security_compliance/946_service_discovery/)(K8s 자동 발견)·장기 저장(Thanos·Mimir)이 핵심 [에코](/studynote/03_network/01_data_communication/031_에코_반향/)시스템이다.

---

## Ⅰ. 개요 및 필요성

```text
서비스 -> /metrics 노출 -> Prometheus (Pull, 15초 주기)
  -> TSDB 저장 -> PromQL 조회 -> Grafana 시각화
  -> Alertmanager -> PagerDuty/Slack 알림
```

- **📢 섹션 요약 비유**: Prometheus는 <strong>우편배달부(Pull)</strong>이다. 각 집([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))의 우편함(/[metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/))에서 편지([메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/))를 수거한다.

---

## Ⅱ~Ⅴ. 결론

Prometheus는 <strong>K8s 환경의 <a href="/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/">메트릭</a> 표준</strong>이며, Thanos/Mimir로 장기 저장·고가용성을 확보한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Prometheus** | Pull [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 수집 |
| **PromQL** | [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 조회 언어 |
| **Alertmanager** | 알림 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) |
| **Thanos** | 장기 저장·HA |
| **Mimir** | [Grafana](/studynote/16_bigdata/08_visualization/168_grafana/) Labs 장기 저장 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Borgmon (Google 내부, 2000s)] -> [Prometheus (SoundCloud, 2012)]
    -> [CNCF 졸업 (2018)] -> [Thanos (2018, HA)]
    -> [Mimir (2022, Grafana Labs)]
    -> [현재: OTel Metrics -> Prometheus 호환]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Prometheus는 <strong>우편배달부</strong>예요. 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(집)의 우편함(/[metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/))에서 <strong>편지를 수거</strong>해요.
2. 수거한 편지를 <strong>정리(TSDB)</strong>하고 <strong><a href="/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/">그래프</a>(<a href="/studynote/16_bigdata/08_visualization/168_grafana/">Grafana</a>)</strong>로 보여줘요.
3. 위험한 편지(이상 지표)가 오면 <strong>비상벨(Alertmanager)</strong>을 울려요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 136 / 373

<- **이전**: [135. RED 메서드 (Rate·Errors·Duration) - 서비스 중심 분석](/studynote/15_devops_sre/03_sre_observability/135_red_method_service_analysis/)
**다음**: [137. Grafana - 통합 관측 가능성 시각화 플랫폼](/studynote/15_devops_sre/03_sre_observability/137_grafana/) ->

---
