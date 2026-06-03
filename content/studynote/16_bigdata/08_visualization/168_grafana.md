---
title: 168. Grafana — 메트릭/로그/추적 통합 관측성 시각화
date: '2026-04-21'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)

- **본질**: Grafana는 [[342_routing_metric_hop_bandwidth_delay|메트릭]]([[567_metrics_time_series_prometheus_grafana|Metrics]])·[[568_logs_distributed_logging_elk_fluentd|로그]]([[568_logs_distributed_logging_elk_fluentd|Logs]])·추적(Traces)의 3대 관측성([[642_observability_telemetry|Observability]]) 기둥을 단일 UI에서 통합 [[003_bigdata_7v|시각화]]하는 플랫폼으로, LGTM [[057_stack|스택]](Loki+Grafana+Tempo+Mimir)을 통해 완전한 [[191_oss_license_compliance|오픈소스]] 관측성 환경을 구성할 수 있다.
- **가치**: Prometheus의 PromQL로 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 클러스터 [[342_routing_metric_hop_bandwidth_delay|메트릭]], Loki의 LogQL로 애플리케이션 [[568_logs_distributed_logging_elk_fluentd|로그]], Tempo로 [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]을 하나의 Grafana 대시보드에서 [[325_correlation_analysis_pearson_spearman|상관 분석]]하여 장애 근본 원인을 분 단위로 파악할 수 있다.
- **판단 포인트**: Grafana는 BI([[282_business_intelligence_bi_technology_framework|비즈니스 인텔리전스]])가 아닌 운영 관측성(Operational [[642_observability_telemetry|Observability]]) 도구이므로, 비즈니스 [[018_kpi|KPI]] 대시보드에는 [[164_tableau|Tableau]]/[[069_type_1_2_error_statistical_power|Power]] BI가, 인프라·애플리케이션 [[229_monitor|모니터]]링에는 Grafana가 각각 더 적합하다.

---

## Ⅰ. 개요 및 필요성

### 관측성([[642_observability_telemetry|Observability]])의 3대 기둥

[[532_microservices_decomposition_patterns|마이크로서비스]], [[196_kubernetes_k8s_container_orchestration|쿠버네티스]], [[136_variance|분산]] 시스템에서 "왜 [[090_service_kubernetes_network_load_balancing|서비스]]가 느린가?"를 파악하려면 3가지 [[130_signal|신호]]가 필요하다:

```
관측성 3대 기둥:
┌──────────────────────────────────────────────────────┐
│  1. 메트릭 (Metrics)                                 │
│     - CPU, 메모리, 요청 수, 응답 시간, 오류율         │
│     - 시계열 데이터 (시간 + 숫자값)                   │
│     - "무슨 일이 일어나고 있나?" → 양적 측정           │
│                                                      │
│  2. 로그 (Logs)                                      │
│     - 애플리케이션 이벤트 기록 (ERROR, INFO, WARN)    │
│     - 비정형 텍스트 + 타임스탬프                      │
│     - "왜 이런 일이 일어났나?" → 상세 이유             │
│                                                      │
│  3. 추적 (Traces)                                    │
│     - 분산 서비스 간 요청 흐름 추적                   │
│     - Span 연결 (A서비스 → B서비스 → DB 순서)         │
│     - "어디서 느렸나?" → 병목 위치 식별               │
└──────────────────────────────────────────────────────┘
```

**📢 섹션 요약 비유**: 관측성 3기둥은 **자동차 계기판·블랙박스·GPS** 조합과 같다. 계기판([[342_routing_metric_hop_bandwidth_delay|메트릭]])으로 이상을 감지하고, 블랙박스([[568_logs_distributed_logging_elk_fluentd|로그]])로 원인을 파악하며, GPS(추적)로 어느 경로에서 문제가 생겼는지 추적한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### LGTM [[057_stack|스택]] 아키텍처

```
┌──────────────────────────────────────────────────────────────┐
│                     LGTM 스택 구조                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  데이터 수집                                                 │
│  ┌────────────┬──────────────┬─────────────────────────────┐ │
│  │Prometheus  │ Promtail/    │ OpenTelemetry / Jaeger /    │ │
│  │(메트릭 수집)│ Fluentbit   │ Zipkin                      │ │
│  │Pull 기반   │ (로그 수집)  │ (추적 데이터 수집)           │ │
│  └─────┬──────┴──────┬───────┴──────────────┬──────────────┘ │
│        │             │                       │               │
│  저장  ▼             ▼                       ▼               │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────────┐   │
│  │  Mimir   │  │  Loki    │  │         Tempo            │   │
│  │(메트릭   │  │(로그     │  │(추적 데이터 저장)          │   │
│  │ 장기저장)│  │ 집계·저장)│  │TraceQL 쿼리 지원          │   │
│  └──────────┘  └──────────┘  └──────────────────────────┘   │
│        │             │                       │               │
│  시각화 ▼             ▼                       ▼               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                    Grafana UI                          │  │
│  │  PromQL / LogQL / TraceQL 통합 쿼리                    │  │
│  │  Explore, Dashboard, Alerting                         │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### 핵심 [[298_qkv_attention|쿼리]] 언어 비교

| 언어 | [[001_dikw_pyramid|데이터]] 소스 | 주요 용도 |
|:---|:---|:---|
| **PromQL** | [[136_prometheus|Prometheus]], Mimir | [[342_routing_metric_hop_bandwidth_delay|메트릭]] [[298_qkv_attention|쿼리]]·집계·알림 |
| **LogQL** | Loki | [[568_logs_distributed_logging_elk_fluentd|로그]] 필터링·패턴 추출 |
| **TraceQL** | Tempo | 추적 검색·필터링 |

```
PromQL 예시:
  # 5분 평균 CPU 사용률 (전체 서비스)
  avg(rate(cpu_usage_seconds_total[5m])) by (service)

  # 오류율 > 5% 서비스 필터
  sum(rate(http_requests_total{status=~"5.."}[5m]))
  / sum(rate(http_requests_total[5m])) > 0.05

LogQL 예시:
  # 에러 로그만 필터
  {app="api-server"} |= "ERROR"
  
  # 분당 오류 발생 건수
  count_over_time({app="api-server"} |= "ERROR" [1m])
```

**📢 섹션 요약 비유**: LGTM [[057_stack|스택]]은 **병원 종합 진단 시스템**과 같다. 혈압계([[136_prometheus|Prometheus]] [[342_routing_metric_hop_bandwidth_delay|메트릭]]), 의무기록(Loki [[568_logs_distributed_logging_elk_fluentd|로그]]), 내시경 카메라(Tempo 추적)가 모두 하나의 [[229_monitor|모니터]](Grafana)에 표시되어 의사(엔지니어)가 종합 진단한다.

---

## Ⅲ. 비교 및 연결

### Grafana vs [[169_kibana|Kibana]] 비교

| 차원 | Grafana | [[169_kibana|Kibana]] |
|:---|:---|:---|
| **주 용도** | 다중 소스 [[342_routing_metric_hop_bandwidth_delay|메트릭]]·관측성 | [[302_cdc|Elasticsearch]] [[119_log_analysis|로그 분석]] |
| **[[001_dikw_pyramid|데이터]] 소스** | 다수 ([[136_prometheus|Prometheus]], Loki, [[255_time_series_rollup_retention_compression|InfluxDB]], 등) | [[302_cdc|Elasticsearch]] 전용 |
| **강점** | 멀티소스 통합, [[342_routing_metric_hop_bandwidth_delay|메트릭]] [[003_bigdata_7v|시각화]] | 전문 [[568_logs_distributed_logging_elk_fluentd|로그]] 검색, [[624_siem|SIEM]] |
| **ML 기능** | 기본 이상 감지 | Elastic ML (고급) |
| **무료 수준** | [[191_oss_license_compliance|오픈소스]] 전체 | 기본 기능 (고급은 유료) |

### Grafana k6: [[446_load_test|부하 테스트]] 통합

Grafana k6는 JavaScript 기반 [[446_load_test|부하 테스트]] 도구로, 테스트 결과를 Grafana 대시보드로 실시간 [[003_bigdata_7v|시각화]]한다:

```javascript
// k6 테스트 스크립트
import http from 'k6/http';
export const options = { vus: 100, duration: '30s' };
export default function() {
  const res = http.get('https://api.example.com/products');
  check(res, { 'status was 200': (r) => r.status == 200 });
}
```

**📢 섹션 요약 비유**: Grafana + k6의 조합은 **의사 + [[447_stress_test|스트레스 테스트]] 장비**와 같다. [[446_load_test|부하 테스트]]([[447_stress_test|스트레스 테스트]])를 수행하면서 실시간으로 시스템 반응(Grafana 대시보드)을 [[229_monitor|모니터]]링하여 한계점을 파악한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] [[229_monitor|모니터]]링 [[057_stack|스택]]

```
쿠버네티스 표준 모니터링 스택:
  kube-state-metrics: K8s 오브젝트 상태 노출
  node-exporter: 노드 수준 메트릭 (CPU, 메모리, 디스크)
  Prometheus: 메트릭 수집 + 저장 (Pull 방식)
  Grafana: 시각화

  주요 대시보드:
  - Cluster Overview: 전체 클러스터 리소스 현황
  - Node Exporter Full: 노드별 상세 메트릭
  - Pod/Deployment: 워크로드별 CPU/메모리
  - Kubernetes Events: 이벤트 로그 연동
  
  커뮤니티 대시보드: grafana.com/grafana/dashboards/
  (ID 번호로 바로 가져오기 가능)
```

### Grafana Alerting

```yaml
# 알림 규칙 예시
- alert: HighErrorRate
  expr: |
    sum(rate(http_requests_total{status=~"5.."}[5m]))
    / sum(rate(http_requests_total[5m])) > 0.05
  for: 5m  # 5분 이상 지속 시 발화
  annotations:
    summary: "서비스 오류율 5% 초과"
    description: "{{ $labels.service }} 오류율: {{ $value | humanizePercentage }}"
  labels:
    severity: critical
```

알림 채널: Slack, PagerDuty, OpsGenie, 이메일, [[498_webhook_rest_api_reverse_callback|Webhook]]

**📢 섹션 요약 비유**: Grafana Alerting은 **화재경보기**와 같다. 정상 범위(임계값)를 벗어나는 순간 경보가 울리고, 담당자에게 즉시 알림이 전달된다. 경보 기준(임계값)은 미리 정의한다.

---

## Ⅴ. 기대효과 및 결론

### Grafana 도입 효과

| 영역 | 효과 |
|:---|:---|
| **[[451_mttr|MTTR]] 단축** | [[026_mttr|Mean Time To Recover]] — 장애 원인 파악 시간 대폭 단축 |
| **관측성** | [[342_routing_metric_hop_bandwidth_delay|메트릭]]·[[568_logs_distributed_logging_elk_fluentd|로그]]·추적 통합으로 전체 시스템 상태 파악 |
| **비용** | [[191_oss_license_compliance|오픈소스]] + 클라우드 관리형 Grafana Cloud 선택 가능 |
| **표준화** | 전사 [[229_monitor|모니터]]링 플랫폼 단일화 |

### 결론

Grafana는 **[[531_cloud_native_architecture|클라우드 네이티브]] 시대의 표준 관측성 플랫폼**이다. [[532_microservices_decomposition_patterns|마이크로서비스]]와 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 환경에서 시스템의 "건강 상태"를 지속적으로 [[229_monitor|모니터]]링하고, 이상 감지 시 즉각 대응할 수 있는 가시성을 제공한다. 정보통신기술사는 LGTM [[057_stack|스택]]의 각 [[603_component_independent_deployment_unit|컴포넌트]] 역할과 PromQL 기반 알림 설계를 이해하고 클라우드 인프라 [[229_monitor|모니터]]링 아키텍처 설계에 적용할 수 있어야 한다.

**📢 섹션 요약 비유**: Grafana가 있는 엔지니어링 팀은 **항공 관제사가 있는 공항**과 같다. 관제사(Grafana)가 모든 비행기([[090_service_kubernetes_network_load_balancing|서비스]])의 상태를 실시간으로 파악하고, 이상이 감지되면 즉각 대응하여 충돌(장애)을 방지한다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| [[136_prometheus|Prometheus]] | [[342_routing_metric_hop_bandwidth_delay|메트릭]] [[001_dikw_pyramid|데이터]] 소스 | Pull 방식 시계열 [[342_routing_metric_hop_bandwidth_delay|메트릭]] 수집·저장 |
| Loki | [[568_logs_distributed_logging_elk_fluentd|로그]] [[001_dikw_pyramid|데이터]] 소스 | 수평 확장 [[568_logs_distributed_logging_elk_fluentd|로그]] 집계, LogQL [[298_qkv_attention|쿼리]] |
| Tempo | 추적 [[001_dikw_pyramid|데이터]] 소스 | [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] 백엔드, TraceQL |
| Mimir | [[136_prometheus|Prometheus]] 확장 | [[310_multi_tenant_database_architecture|멀티테넌트]] 고가용성 [[136_prometheus|Prometheus]] |
| LGTM [[057_stack|스택]] | 통합 관측성 | Loki+Grafana+Tempo+Mimir |
| PromQL | [[298_qkv_attention|쿼리]] 언어 | [[136_prometheus|Prometheus]] [[342_routing_metric_hop_bandwidth_delay|메트릭]] [[298_qkv_attention|쿼리]] 언어 |
| Grafana k6 | [[446_load_test|부하 테스트]] | JavaScript 기반 [[446_load_test|부하 테스트]] + Grafana 통합 |
| [[169_kibana|Kibana]] | 비교 도구 | [[302_cdc|Elasticsearch]] 특화 [[119_log_analysis|로그 분석]] [[003_bigdata_7v|시각화]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[메트릭 수집 (Metrics) — Prometheus Pull 방식]
    │
    ▼
[로그 집계 (Log Aggregation) — Loki]
    │
    ▼
[분산 추적 (Distributed Tracing) — Tempo]
    │
    ▼
[Grafana 대시보드 — 통합 관측성 (Unified Observability)]
    │
    ▼
[LGTM 스택 (Loki + Grafana + Tempo + Mimir)]
```

관측성 기술이 개별 [[342_routing_metric_hop_bandwidth_delay|메트릭]]·[[568_logs_distributed_logging_elk_fluentd|로그]]·추적을 통합하여 Grafana 중심의 단일 가시성 플랫폼으로 수렴한 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

- Grafana는 **병원 중환자실 [[229_monitor|모니터]]**예요: 환자(서버·[[090_service_kubernetes_network_load_balancing|서비스]])의 심장 박동(CPU), 혈압(메모리), 체온(오류율)이 실시간으로 표시되고, 이상이 생기면 경보가 울려요.
- LGTM [[057_stack|스택]]은 **의료 검사 세트**예요: 혈액 검사([[342_routing_metric_hop_bandwidth_delay|메트릭]]), 의무기록([[568_logs_distributed_logging_elk_fluentd|로그]]), 내시경(추적) 세 가지가 함께 있어야 의사가 정확한 진단을 내릴 수 있어요.
- PromQL은 **의료 [[001_dikw_pyramid|데이터]]를 묻는 질문 형식**이에요: "지난 5분간 심장 박동이 100을 넘었나?"처럼 복잡한 질문을 짧은 수식으로 표현해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 168 / 262

← **이전**: [[167_apache_superset|167. Apache Superset — 오픈소스 엔터프라이즈 BI SQL Lab]]
**다음**: [[169_kibana|169. Kibana — ELK Stack 시각화 로그 분석 도구]] →

---
