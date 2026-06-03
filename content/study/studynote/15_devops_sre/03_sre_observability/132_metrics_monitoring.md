---
title: 132. Metrics & 모니터링 심화 - Prometheus·Grafana 기반 메트릭 수집·시각화
date: '2026-04-19'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Metrics는 **시계열 수치 [[001_dikw_pyramid|데이터]](CPU·메모리·요청 수·에러율)**이며, Prometheus가 Pull 방식으로 수집하고 PromQL로 조회하며 Grafana로 [[003_bigdata_7v|시각화]]하는 것이 [[531_cloud_native_architecture|클라우드 네이티브]] [[342_routing_metric_hop_bandwidth_delay|메트릭]] 표준이다.
> 2. **가치**: [[342_routing_metric_hop_bandwidth_delay|메트릭]] 없이는 "시스템이 느리다"만 알고 **어떤 [[090_service_kubernetes_network_load_balancing|서비스]]의 어떤 지표가 [[431_ssthresh_slow_start_threshold|임계치]]를 넘었는지** 알 수 없으며, [[342_routing_metric_hop_bandwidth_delay|메트릭]] 기반 알림으로 **장애를 조기 감지**한다.
> 3. **판단 포인트**: [[133_four_golden_signals|4대 골든 시그널]]([[141_latency|Latency]]·Traffic·Errors·Saturation)이 [[100_sre_site_reliability_engineering_error_budget|SRE]] [[229_monitor|모니터]]링의 핵심이며, RED(Rate·Errors·Duration)·USE(Utilization·Saturation·Errors)가 대안이다.

---

## Ⅰ. 개요 및 필요성

```text
Prometheus → Pull → 서비스 /metrics 엔드포인트
  → TSDB 저장 → PromQL 조회
  → Alertmanager → PagerDuty/Slack
  → Grafana 대시보드 시각화
```

- **📢 섹션 요약 비유**: Prometheus는 **체온계(수집)**, Grafana는 **진료 차트([[003_bigdata_7v|시각화]])**, Alertmanager는 **비상벨(알림)**이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| [[133_four_golden_signals|4대 골든 시그널]] | 설명 |
|:---|:---|
| **[[141_latency|Latency]]** | [[138_response_time|응답 시간]] |
| **Traffic** | 요청 수 |
| **Errors** | 에러율 |
| **Saturation** | 리소스 포화도 |

---

## Ⅲ~Ⅴ. 결론

[[136_prometheus|Prometheus]]+Grafana는 **[[531_cloud_native_architecture|클라우드 네이티브]] [[342_routing_metric_hop_bandwidth_delay|메트릭]]의 사실상 표준**이며, [[133_four_golden_signals|4대 골든 시그널]] 기반 알림이 [[100_sre_site_reliability_engineering_error_budget|SRE]] [[229_monitor|모니터]]링의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[136_prometheus|Prometheus]]** | [[342_routing_metric_hop_bandwidth_delay|메트릭]] 수집 (Pull) |
| **[[168_grafana|Grafana]]** | [[342_routing_metric_hop_bandwidth_delay|메트릭]] [[003_bigdata_7v|시각화]] |
| **PromQL** | [[342_routing_metric_hop_bandwidth_delay|메트릭]] 조회 언어 |
| **Golden [[611_conditional_access_signals|Signals]]** | 4대 핵심 지표 |
| **Alertmanager** | 알림 [[339_routing_overview_best_path_selection|라우팅]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[Nagios/Zabbix (2000s)] → [Prometheus (2012, SoundCloud)]
    → [CNCF 졸업 (2018)] → [Grafana LGTM Stack (2020~)]
    → [현재: Mimir (장기 메트릭 저장) + Thanos (HA)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Prometheus는 **체온계**예요. 시스템의 **건강 수치**를 재요.
2. Grafana는 **진료 차트**예요. 수치를 **[[070_graph_datastructure|그래프]]로 보기 쉽게** 보여줘요.
3. 수치가 위험하면 **비상벨(Alertmanager)**이 울려서 바로 알 수 있어요!
