---
title: "132. Metrics & 모니터링 심화 - Prometheus·Grafana 기반 메트릭 수집·시각화"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Metrics는 <strong>시계열 수치 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>(CPU·메모리·요청 수·에러율)</strong>이며, Prometheus가 Pull 방식으로 수집하고 PromQL로 조회하며 Grafana로 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)하는 것이 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 표준이다.
> 2. **가치**: [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 없이는 "시스템이 느리다"만 알고 <strong>어떤 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>의 어떤 지표가 <a href="/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/">임계치</a>를 넘었는지</strong> 알 수 없으며, [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 기반 알림으로 <strong>장애를 조기 감지</strong>한다.
> 3. **판단 포인트**: [4대 골든 시그널](/studynote/15_devops_sre/03_sre_observability/133_four_golden_signals/)([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)·Traffic·Errors·Saturation)이 [SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링의 핵심이며, RED(Rate·Errors·Duration)·USE(Utilization·Saturation·Errors)가 대안이다.

---

## Ⅰ. 개요 및 필요성

```text
Prometheus -> Pull -> 서비스 /metrics 엔드포인트
  -> TSDB 저장 -> PromQL 조회
  -> Alertmanager -> PagerDuty/Slack
  -> Grafana 대시보드 시각화
```

- **📢 섹션 요약 비유**: Prometheus는 **체온계(수집)**, Grafana는 <strong>진료 차트(<a href="/studynote/16_bigdata/01_intro/003_bigdata_7v/">시각화</a>)</strong>, Alertmanager는 <strong>비상벨(알림)</strong>이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| [4대 골든 시그널](/studynote/15_devops_sre/03_sre_observability/133_four_golden_signals/) | 설명 |
|:---|:---|
| <strong><a href="/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">Latency</a></strong> | [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) |
| **Traffic** | 요청 수 |
| **Errors** | 에러율 |
| **Saturation** | 리소스 포화도 |

---

## Ⅲ~Ⅴ. 결론

[Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/)+Grafana는 <strong><a href="/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/">클라우드 네이티브</a> <a href="/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/">메트릭</a>의 사실상 표준</strong>이며, [4대 골든 시그널](/studynote/15_devops_sre/03_sre_observability/133_four_golden_signals/) 기반 알림이 [SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/15_devops_sre/03_sre_observability/136_prometheus/">Prometheus</a></strong> | [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 수집 (Pull) |
| <strong><a href="/studynote/16_bigdata/08_visualization/168_grafana/">Grafana</a></strong> | [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/) |
| **PromQL** | [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 조회 언어 |
| <strong>Golden <a href="/studynote/09_security/12_identity_threat_advanced/611_conditional_access_signals/">Signals</a></strong> | 4대 핵심 지표 |
| **Alertmanager** | 알림 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[Nagios/Zabbix (2000s)] -> [Prometheus (2012, SoundCloud)]
    -> [CNCF 졸업 (2018)] -> [Grafana LGTM Stack (2020~)]
    -> [현재: Mimir (장기 메트릭 저장) + Thanos (HA)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Prometheus는 <strong>체온계</strong>예요. 시스템의 <strong>건강 수치</strong>를 재요.
2. Grafana는 <strong>진료 차트</strong>예요. 수치를 <strong><a href="/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/">그래프</a>로 보기 쉽게</strong> 보여줘요.
3. 수치가 위험하면 <strong>비상벨(Alertmanager)</strong>이 울려서 바로 알 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 132 / 373

<- **이전**: [131. 관측 가능성 Three Pillars - Metrics·Logs·Traces 심층 분석](/studynote/15_devops_sre/03_sre_observability/131_observability_three_pillars/)
**다음**: [133. 4대 골든 시그널 (Four Golden Signals) - SRE 핵심 모니터링 지표](/studynote/15_devops_sre/03_sre_observability/133_four_golden_signals/) ->

---
