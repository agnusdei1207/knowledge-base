---
title: "Telemetry Big Data Parsing"
date: "2026-04-21"
tags:
  - "studynote-enterprise-systems"
weight: 314
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) ([OpenTelemetry](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/))은 Traces·[Metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)·[Logs](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 세 기둥을 표준화된 단일 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)/SDK로 수집하여 [벤더 종속](/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/) 없이 [관측 가능성](/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)([Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/))을 구현하는 [CNCF](/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 표준이다.
> 2. **가치**: 4 Golden [Signals](/studynote/09_security/12_identity_threat_advanced/611_conditional_access_signals/) ([지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 트래픽, 오류율, 포화도)가 모두 실시간 수집될 때 장애 [MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) (평균 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간)이 평균 60% 이상 단축된다.
> 3. **판단 포인트**: Tail Sampling은 오류·[지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 트레이스만 선택 보존해 저장 비용을 90% 절감하지만, Collector 메모리를 많이 소비하므로 Collector [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) 계획이 필요하다.

## Ⅰ. 개요 및 필요성

[마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 환경에서 수십~수백 개 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/), 트레이스를 각기 다른 방식으로 수집하면 도구 파편화와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치가 발생한다.

[OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) ([OpenTelemetry](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/))은 [CNCF](/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) ([Cloud Native](/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/) Computing Foundation) 프로젝트로 표준 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)/SDK를 제공하여 한 번의 계측으로 어느 백엔드(Jaeger, [Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/), [Grafana](/studynote/16_bigdata/08_visualization/168_grafana/), Datadog)에도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 전송할 수 있다.

[Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) 3 기둥 (Three Pillars):
- <strong>Traces (<a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/">분산 추적</a>)</strong>: 요청이 여러 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 지나는 전체 경로 기록
- <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/">Metrics</a> (<a href="/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/">메트릭</a>)</strong>: 숫자로 표현되는 시스템 상태 (CPU, 응답시간, 에러율)
- <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">Logs</a> (<a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a>)</strong>: 시간 순서 이벤트 기록

4 Golden [Signals](/studynote/09_security/12_identity_threat_advanced/611_conditional_access_signals/) ([SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 핵심 지표):
1. [Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) ([지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)): 요청 처리 시간
2. Traffic (트래픽): 초당 요청 수(RPS)
3. Errors (오류율): 5xx 응답 비율
4. Saturation (포화도): CPU/메모리/디스크 사용률

📢 **섹션 요약 비유**: OTel은 모든 센서가 같은 규격 커넥터를 쓰는 자동차 진단 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)다. 어떤 진단기(백엔드)를 꽂아도 같은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽을 수 있다.

## Ⅱ. 아키텍처 및 핵심 원리

### [OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인

| 단계 | 역할 | 예시 |
|:---|:---|:---|
| Receiver | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수신 | OTLP, [Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/), Jaeger, Zipkin |
| Processor | 변환·필터링·샘플링 | Batch, Memory Limiter, [Sampling](/studynote/03_network/01_data_communication/056_표본화_Sampling/) |
| Exporter | 백엔드 전송 | Jaeger, [Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/), [Grafana](/studynote/16_bigdata/08_visualization/168_grafana/) Tempo, Datadog |

### 샘플링 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 방법 | 장점 | 단점 |
|:---|:---|:---|:---|
| Head [Sampling](/studynote/03_network/01_data_communication/056_표본화_Sampling/) | 요청 시작 시 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 샘플링 (1%) | 저지연, 저비용 | 오류 트레이스 누락 가능 |
| Tail [Sampling](/studynote/03_network/01_data_communication/056_표본화_Sampling/) | 완료 후 오류·[지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 기준 선택 | 중요 트레이스 100% 보존 | Collector 메모리 높음 |

### [ASCII](/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램: 텔레메트리 수집 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인

```
  마이크로서비스 (OTel SDK 계측)
  +--------------+  +--------------+  +--------------+
  |  Service A   |  |  Service B   |  |  Service C   |
  | Trace/Metric |  | Trace/Metric |  | Trace/Metric |
  |   /Log 생성  |  |   /Log 생성  |  |   /Log 생성  |
  +------+-------+  +------+-------+  +------+-------+
         +------------------+------------------+
                            v OTLP (gRPC/HTTP)
               +----------------------------+
               |     OTel Collector         |
               |  +----------------------+  |
               |  | Receiver (OTLP)      |  |
               |  +----------------------+  |
               |  | Processor            |  |
               |  | - Batch (500ms)      |  |
               |  | - Tail Sampling      |  |
               |  | - PII 마스킹          |  |
               |  +----------------------+  |
               |  | Exporter             |  |
               |  +----------------------+  |
               +--------------+-------------+
          +--------------------+------------------+
          v                    v                   v
  +--------------+  +--------------+  +------------------+
  |   Jaeger     |  |  Prometheus  |  |  Grafana Loki    |
  |  (Tracing)   |  |  (Metrics)   |  |  (Logs)          |
  +--------------+  +--------------+  +------------------+
          +--------------------+------------------+
                               v
                     +------------------+
                     |   Grafana 대시보드 |
                     |  (4 Golden Sign) |
                     +------------------+
```

### 4 Golden [Signals](/studynote/09_security/12_identity_threat_advanced/611_conditional_access_signals/) 알람 임계값 예시

| [신호](/studynote/02_operating_system/02_process_thread/130_signal/) | [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) | 경고 임계값 | 위험 임계값 |
|:---|:---|:---|:---|
| [Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) | p99 [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) | >500ms | >1000ms |
| Traffic | RPS 변화율 | ±30% | ±50% |
| Errors | 5xx 비율 | >0.1% | >1% |
| Saturation | CPU 사용률 | >70% | >90% |

📢 **섹션 요약 비유**: [OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector는 여러 센서의 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 받아 필터링하고 여러 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 시스템에 동시에 전달하는 지능형 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 교환기다.

## Ⅲ. 비교 및 연결

### [OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) vs 기존 [APM](/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/) 도구

| 항목 | [OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) | Datadog/NewRelic |
|:---|:---|:---|
| [벤더 종속](/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/) | 없음 (표준) | 있음 (에이전트 교체 어려움) |
| 비용 | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) (수집) + 백엔드 비용 | 고가 ([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 볼륨 과금) |
| 기능 완성도 | 계속 성장 중 | 성숙, 올인원 |
| 다중 백엔드 | 가능 | 단일 (자사 플랫폼) |
| 엔터프라이즈 지원 | 커뮤니티 | 공식 [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/) |

📢 **섹션 요약 비유**: OTel은 표준 [USB](/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/) [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), Datadog은 독자 규격 충전기다. USB는 어디서나 쓰지만 충전 속도는 독자 규격이 더 빠를 수 있다.

## Ⅳ. 실무 적용 및 기술사 판단

### 텔레메트리 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] 4 Golden [Signals](/studynote/09_security/12_identity_threat_advanced/611_conditional_access_signals/) 수집 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 구성 완료 여부
- [ ] [분산 추적](/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/): [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [Trace ID](/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/) 전파 (`traceparent` [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 헤더)
- [ ] 샘플링 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/): 개발=100%, 스테이징=[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%, 프로덕션=1% + Tail [Sampling](/studynote/03_network/01_data_communication/056_표본화_Sampling/)
- [ ] PII [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹: Collector Processor에서 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 필드 제거
- [ ] Cardinality 관리: 레이블 조합 수 제한 ([Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/) [메모리 보호](/studynote/01_computer_architecture/07_virtual_memory_os_integration/803_memory_protection/))

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

| [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) | 문제 | 해결 방법 |
|:---|:---|:---|
| 모든 트레이스 100% 보존 | 저장 비용 폭발 | Tail [Sampling](/studynote/03_network/01_data_communication/056_표본화_Sampling/) 적용 |
| 고카디널리티 레이블 | [Prometheus](/studynote/15_devops_sre/03_sre_observability/136_prometheus/) [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) | user_id는 레이블 금지 |
| [OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 없이 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 개별 계측 | 파편화, 상관 불가 | [OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) SDK 표준화 |

📢 **섹션 요약 비유**: 고카디널리티 레이블은 100만 명의 이름을 서랍 라벨로 쓰는 것이다. 서랍장이 폭발한다.

## Ⅴ. 기대효과 및 결론

### 기대효과

| 항목 | [OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 이전 | [OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 도입 후 |
|:---|:---|:---|
| 장애 탐지 MTTD | 30~60분 | 2~5분 |
| 장애 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) | 2~4시간 | 30~60분 |
| [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 호출 추적 | 불가 | 단일 Trace로 전체 경로 |
| [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 도구 수 | 5~10개 (파편화) | 1~3개 (통합) |

### 한계 및 선결 과제

- [OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) SDK 자동 계측 지원 언어 제한 (Go, Java, Python, JS 강력, [Rust](/studynote/04_software_engineering/10_trends_pm_quality/782_memory_safety_rust_compiler_verification/) 성장 중)
- Collector 클러스터 자체 운영 복잡도 ([Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) [DaemonSet](/studynote/11_design_supervision/06_exam_summary/334_process/) 권장)
- 대용량 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 파싱 비용: [Grafana](/studynote/16_bigdata/08_visualization/168_grafana/) Loki, [ElasticSearch](/studynote/05_database/05_distributed_nosql_newsql/302_cdc/) 인덱싱 비용 설계 필요
- Tail [Sampling](/studynote/03_network/01_data_communication/056_표본화_Sampling/) Collector: 모든 스팬 [버퍼링](/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/) 필요 -> 고메모리 필요

📢 **섹션 요약 비유**: [OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 도입은 병원에 전자의무기록 시스템을 도입하는 것이다. 모든 진료 기록이 통합되면 어느 과 의사든 즉시 전체 이력을 볼 수 있다.

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) | 표준 | [CNCF](/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) [관측 가능성](/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/) 표준 |
| Traces | 세 기둥 | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 요청 추적 |
| [Metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/) | 세 기둥 | 수치 시스템 상태 |
| [Logs](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | 세 기둥 | 시간 순 이벤트 기록 |
| 4 Golden [Signals](/studynote/09_security/12_identity_threat_advanced/611_conditional_access_signals/) | 핵심 지표 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)·트래픽·오류·포화도 |
| Tail [Sampling](/studynote/03_network/01_data_communication/056_표본화_Sampling/) | 최적화 | 중요 트레이스 선택 보존 |

### 📈 관련 키워드 및 발전 흐름도

```
O-RAN 네트워크 장비 지표 수동 수집 한계
    |
    v
스트리밍 텔레메트리 (gRPC/gNMI) - 실시간 전송
    |
    v
Kafka + Flink - 대용량 텔레메트리 스트리밍 파싱
    |
    v
시계열 DB (InfluxDB, OpenTSDB) 저장·분석
    |
    v
ML 기반 네트워크 이상 탐지 자동화
```

> **키워드**: Telemetry, [O-RAN](/studynote/03_network/15_nextgen_communication_architecture/782_o_ran_open_ran_white_box_interface/), gNMI, [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/), [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), Flink, Time Series, Network Analytics, Streaming Parsing

### 👶 어린이를 위한 3줄 비유 설명

1. OTel은 모든 선생님이 같은 양식의 출석부를 쓰는 것이에요. 어느 반이든 같은 방식으로 기록해요.
2. 4 Golden Signals는 선생님이 매일 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 4가지 항목이에요: 수업 시간([지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)), 출석률(트래픽), 결석 사유(오류), 교실 혼잡도(포화도).
3. Tail Sampling은 결석하거나 지각한 학생 기록만 자세히 남기는 거예요. 모든 학생 기록을 다 남기면 종이가 부족하니까요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 314 / 482

<- **이전**: [313. HTAP 하이브리드 트랜잭션 분석 처리 인메모리 아키텍처 (HTAP In-Memory Architecture)](/studynote/07_enterprise_systems/05_data_bi/313_htap_in_memory_architecture/)
**다음**: [315. NoSQL BASE 결과적 일관성 CAP 정리 트레이드오프 (NoSQL BASE CAP Theorem)](/studynote/07_enterprise_systems/05_data_bi/315_nosql_base_cap_theorem/) ->

---
