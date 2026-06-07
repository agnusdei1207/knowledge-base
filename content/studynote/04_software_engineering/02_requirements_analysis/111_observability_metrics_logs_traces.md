---
title: "Observability Metrics Logs Traces"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
weight: 111
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 관측 가능성([Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/))은 시스템의 <strong>외부 출력(<a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/">Metrics</a>·<a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">Logs</a>·Traces)만으로 내부 상태를 추론</strong>할 수 있는 능력이며, 기존 모니터링(알려진 문제 감시)을 넘어 <strong>"몰랐던 문제(Unknown Unknowns)"까지 진단</strong>하는 패러다임이다.
> 2. **가치**: 3대 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)([Metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)=수치, [Logs](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)=이벤트, Traces=요청 경로)를 상호 연결(Correlation)하여, [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경에서 <strong>장애의 근본 원인(Root Cause)을 수분 내 특정 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>·함수·라인</strong>까지 추적한다.
> 3. **판단 포인트**: [OpenTelemetry](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/)([OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/))가 [CNCF](/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 통합 표준으로 수렴하며, <strong><a href="/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/">벤더 종속</a> 없는 계측(Instrumentation)</strong>이 가능해졌다. SRE의 [SLI](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/)/[SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) 체계와 결합하여 장애 대응 자동화의 토대가 된다.

---

## Ⅰ. 개요 및 필요성

모놀리스 시대에는 서버 1대의 CPU·메모리만 보면 됐다. MSA에서는 100개 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 그물망처럼 호출하므로, "어디가 느린지" 찾는 것 자체가 난제다.

```text
+-------------------------------------------------------+
|       Monitoring vs Observability                      |
+-------------------------------------------------------+
|  [Monitoring]                [Observability]           |
|   "CPU 80% 넘으면 알림"      "왜 느린지 추론"          |
|   Known Unknowns 감시        Unknown Unknowns 진단    |
|   대시보드 기반               탐색적 질의(Ad-hoc)      |
|                                                       |
|  3대 신호 (Three Pillars):                            |
|   +---------+  +---------+  +---------+              |
|   | Metrics |  |  Logs   |  | Traces  |              |
|   | (수치)  |  |(이벤트) |  |(경로)   |              |
|   +----+----+  +----+----+  +----+----+              |
|        +------------+------------+                    |
|              Correlation (상관 연결)                   |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 모니터링은 체온계(38도 넘으면 알림), 관측 가능성은 MRI(왜 열이 나는지 내부를 투시)다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 3대 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 상세

| [신호](/studynote/02_operating_system/02_process_thread/130_signal/) | 정의 | 대표 도구 | 질문 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/">Metrics</a></strong> | 시계열 수치 (CPU, 레이턴시, 에러율) | [Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/), Datadog | "얼마나 나쁜가?" |
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">Logs</a></strong> | 이벤트 텍스트 (에러 스택트레이스) | Loki, ELK | "무엇이 일어났는가?" |
| **Traces** | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 요청 경로 (Span 트리) | Jaeger, Tempo | "어디서 병목인가?" |

### [OpenTelemetry](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) ([OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/))

CNCF가 주도하는 **벤더 중립 계측 표준**. SDK 하나로 [Metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)·[Logs](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·Traces를 동시에 수집하고, 백엔드([Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/)·Jaeger·Datadog)를 자유롭게 교체할 수 있다.

- **📢 섹션 요약 비유**: OTel은 USB-C 충전기다. 삼성이든 애플이든 같은 케이블(SDK)로 충전(계측)할 수 있다.

---

## Ⅲ. 비교 및 연결

| 비교 | Monitoring | [Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) |
|:---|:---|:---|
| **범위** | 알려진 문제 감시 | 미지의 문제까지 진단 |
| **방식** | 사전 정의 대시보드 | 탐색적 질의 (Ad-hoc) |
| <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a> 대응</strong> | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 개별 대시보드 | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 트레이싱으로 전체 경로 추적 |
| **도구** | Nagios, Zabbix | [Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/)+Jaeger+Loki+[OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 관측 가능성 성숙도 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. **Level 1**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 [Metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/) 대시보드 ([Grafana](/studynote/16_bigdata/08_visualization/168_grafana/)).
2. **Level 2**: 중앙 집중 [Logs](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 수집 (ELK/Loki).
3. **Level 3**: [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) Traces + [Metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/) 상관 연결.
4. **Level 4**: [OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 통합 + [SLI](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/)/[SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) 기반 자동 알림.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **Logs만 수집하고 Traces 미도입**: "에러가 났다"는 알지만 "어느 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서 시작됐는지" 모름.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 모니터링만 | 관측 가능성 | 개선 |
|:---|:---|:---|:---|
| 장애 원인 특정 시간 | 수시간 | **수분** | 90% 단축 |
| Unknown Unknowns | 감지 불가 | **탐색적 진단** | 신규 역량 |
| [벤더 종속](/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/) | 높음 (전용 에이전트) | **OTel로 중립** | 자유도 확보 |

Observability는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Ops와 결합하여 "이상 징후 자동 감지 -> 근본 원인 자동 추론 -> 자동 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)"의 자율 운영(Autonomous Operations) 시대를 여는 핵심 기반이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/">Metrics</a></strong> | 시계열 수치 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), [Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/) 수집 |
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">Logs</a></strong> | 이벤트 텍스트, ELK/Loki 수집 |
| **Traces** | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 요청 경로, Jaeger/Tempo |
| <strong><a href="/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/">OpenTelemetry</a></strong> | 벤더 중립 계측 표준 ([CNCF](/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/)) |
| <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/">SLI</a>/<a href="/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/">SLO</a> (<a href="/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/">SRE</a>)</strong> | 관측 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 기반으로 [서비스 수준 관리](/studynote/12_it_management/02_itsm_itil/868_service_level_management/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[서버 모니터링 (Nagios, 2000s) — 단일 서버 CPU/메모리 감시]
    |
    v
[로그 중앙화 (ELK, 2010s) — 분산 로그 수집·검색]
    |
    v
[분산 트레이싱 (Zipkin·Jaeger, 2015~) — MSA 요청 경로 추적]
    |
    v
[OpenTelemetry 통합 (2019~) — Metrics·Logs·Traces 단일 SDK]
    |
    v
[현재: AI Ops — 이상 탐지·근본 원인 자동 추론·자동 복구]
```

### 👶 어린이를 위한 3줄 비유 설명
1. <strong>체온계(Monitoring)</strong>는 "열이 났다!"만 알려주지만, <strong>MRI(<a href="/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/">Observability</a>)</strong>는 "어디가 아픈지" 속까지 보여줘요.
2. 서버도 마찬가지로, 숫자([Metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/))·일기장([Logs](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))·발자국(Traces) 3가지를 모아야 "왜 느린지" 정확히 알 수 있어요.
3. OpenTelemetry라는 마법 도구가 이 3가지를 한 번에 모아서, 의사 선생님([SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/))이 빨리 고칠 수 있게 도와준답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 111 / 973

<- **이전**: [110. 내부 개발자 플랫폼 (IDP, Internal Developer Platform) - Backstage·셀프서비스 카탈로그](/studynote/04_software_engineering/02_requirements_analysis/110_idp_internal_developer_platform_backstage/)
**다음**: [112. 분산 트레이싱 (Distributed Tracing) - Span·Trace ID·OpenTelemetry 추적 체계](/studynote/04_software_engineering/02_requirements_analysis/112_distributed_tracing_microservices/) ->

---
