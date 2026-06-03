---
title: 314. 텔레메트리 빅데이터 파싱 수집 엔진 (Telemetry Big Data Parsing)
date: '2026-04-21'
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[146_opentelemetry_otel_observability_standard|OTel]] ([[146_opentelemetry_otel_observability_standard|OpenTelemetry]])은 Traces·[[567_metrics_time_series_prometheus_grafana|Metrics]]·[[568_logs_distributed_logging_elk_fluentd|Logs]] 세 기둥을 표준화된 단일 [[014_api_posix|API]]/SDK로 수집하여 [[051_vendor_lock_in_cloud_computing|벤더 종속]] 없이 [[111_observability_metrics_logs_traces|관측 가능성]]([[642_observability_telemetry|Observability]])을 구현하는 [[190_cncf_landscape_observability|CNCF]] 표준이다.
> 2. **가치**: 4 Golden [[611_conditional_access_signals|Signals]] ([[015_지연_데이터_관점|지연]], 트래픽, 오류율, 포화도)가 모두 실시간 수집될 때 장애 [[451_mttr|MTTR]] (평균 [[658_ir_recovery|복구]] 시간)이 평균 60% 이상 단축된다.
> 3. **판단 포인트**: Tail Sampling은 오류·[[015_지연_데이터_관점|지연]] 트레이스만 선택 보존해 저장 비용을 90% 절감하지만, Collector 메모리를 많이 소비하므로 Collector [[249_scaling_normalization_standardization|스케일링]] 계획이 필요하다.

## Ⅰ. 개요 및 필요성

[[532_microservices_decomposition_patterns|마이크로서비스]] 환경에서 수십~수백 개 [[090_service_kubernetes_network_load_balancing|서비스]]의 [[568_logs_distributed_logging_elk_fluentd|로그]], [[342_routing_metric_hop_bandwidth_delay|메트릭]], 트레이스를 각기 다른 방식으로 수집하면 도구 파편화와 [[001_dikw_pyramid|데이터]] 불일치가 발생한다.

[[146_opentelemetry_otel_observability_standard|OTel]] ([[146_opentelemetry_otel_observability_standard|OpenTelemetry]])은 [[190_cncf_landscape_observability|CNCF]] ([[199_cloud_native_architecture_msa_cicd_devops|Cloud Native]] Computing Foundation) 프로젝트로 표준 [[014_api_posix|API]]/SDK를 제공하여 한 번의 계측으로 어느 백엔드(Jaeger, [[136_prometheus|Prometheus]], [[168_grafana|Grafana]], Datadog)에도 [[001_dikw_pyramid|데이터]]를 전송할 수 있다.

[[642_observability_telemetry|Observability]] 3 기둥 (Three Pillars):
- **Traces ([[569_distributed_tracing_opentelemetry_jaeger|분산 추적]])**: 요청이 여러 [[090_service_kubernetes_network_load_balancing|서비스]]를 지나는 전체 경로 기록
- **[[567_metrics_time_series_prometheus_grafana|Metrics]] ([[342_routing_metric_hop_bandwidth_delay|메트릭]])**: 숫자로 표현되는 시스템 상태 (CPU, 응답시간, 에러율)
- **[[568_logs_distributed_logging_elk_fluentd|Logs]] ([[568_logs_distributed_logging_elk_fluentd|로그]])**: 시간 순서 이벤트 기록

4 Golden [[611_conditional_access_signals|Signals]] ([[100_sre_site_reliability_engineering_error_budget|SRE]] 핵심 지표):
1. [[141_latency|Latency]] ([[015_지연_데이터_관점|지연]]): 요청 처리 시간
2. Traffic (트래픽): 초당 요청 수(RPS)
3. Errors (오류율): 5xx 응답 비율
4. Saturation (포화도): CPU/메모리/디스크 사용률

📢 **섹션 요약 비유**: OTel은 모든 센서가 같은 규격 커넥터를 쓰는 자동차 진단 [[446_port_and_bus|포트]]다. 어떤 진단기(백엔드)를 꽂아도 같은 [[001_dikw_pyramid|데이터]]를 읽을 수 있다.

## Ⅱ. 아키텍처 및 핵심 원리

### [[146_opentelemetry_otel_observability_standard|OTel]] Collector [[123_pipe|파이프]]라인

| 단계 | 역할 | 예시 |
|:---|:---|:---|
| Receiver | [[001_dikw_pyramid|데이터]] 수신 | OTLP, [[136_prometheus|Prometheus]], Jaeger, Zipkin |
| Processor | 변환·필터링·샘플링 | Batch, Memory Limiter, [[056_표본화_Sampling|Sampling]] |
| Exporter | 백엔드 전송 | Jaeger, [[136_prometheus|Prometheus]], [[168_grafana|Grafana]] Tempo, Datadog |

### 샘플링 [[268_strategy_pattern|전략]]

| [[268_strategy_pattern|전략]] | 방법 | 장점 | 단점 |
|:---|:---|:---|:---|
| Head [[056_표본화_Sampling|Sampling]] | 요청 시작 시 [[130_probability|확률]] 샘플링 (1%) | 저지연, 저비용 | 오류 트레이스 누락 가능 |
| Tail [[056_표본화_Sampling|Sampling]] | 완료 후 오류·[[015_지연_데이터_관점|지연]] 기준 선택 | 중요 트레이스 100% 보존 | Collector 메모리 높음 |

### [[103_ascii|ASCII]] 다이어그램: 텔레메트리 수집 [[123_pipe|파이프]]라인

```
  마이크로서비스 (OTel SDK 계측)
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │  Service A   │  │  Service B   │  │  Service C   │
  │ Trace/Metric │  │ Trace/Metric │  │ Trace/Metric │
  │   /Log 생성  │  │   /Log 생성  │  │   /Log 생성  │
  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
         └──────────────────┼──────────────────┘
                            ▼ OTLP (gRPC/HTTP)
               ┌────────────────────────────┐
               │     OTel Collector         │
               │  ┌──────────────────────┐  │
               │  │ Receiver (OTLP)      │  │
               │  ├──────────────────────┤  │
               │  │ Processor            │  │
               │  │ - Batch (500ms)      │  │
               │  │ - Tail Sampling      │  │
               │  │ - PII 마스킹          │  │
               │  ├──────────────────────┤  │
               │  │ Exporter             │  │
               │  └──────────────────────┘  │
               └──────────────┬─────────────┘
          ┌────────────────────┼──────────────────┐
          ▼                    ▼                   ▼
  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
  │   Jaeger     │  │  Prometheus  │  │  Grafana Loki    │
  │  (Tracing)   │  │  (Metrics)   │  │  (Logs)          │
  └──────────────┘  └──────────────┘  └──────────────────┘
          └────────────────────┼──────────────────┘
                               ▼
                     ┌──────────────────┐
                     │   Grafana 대시보드 │
                     │  (4 Golden Sign) │
                     └──────────────────┘
```

### 4 Golden [[611_conditional_access_signals|Signals]] 알람 임계값 예시

| [[130_signal|신호]] | [[342_routing_metric_hop_bandwidth_delay|메트릭]] | 경고 임계값 | 위험 임계값 |
|:---|:---|:---|:---|
| [[141_latency|Latency]] | p99 [[138_response_time|응답 시간]] | >500ms | >1000ms |
| Traffic | RPS 변화율 | ±30% | ±50% |
| Errors | 5xx 비율 | >0.1% | >1% |
| Saturation | CPU 사용률 | >70% | >90% |

📢 **섹션 요약 비유**: [[146_opentelemetry_otel_observability_standard|OTel]] Collector는 여러 센서의 [[130_signal|신호]]를 받아 필터링하고 여러 [[229_monitor|모니터]]링 시스템에 동시에 전달하는 지능형 [[130_signal|신호]] 교환기다.

## Ⅲ. 비교 및 연결

### [[146_opentelemetry_otel_observability_standard|OTel]] vs 기존 [[162_apm_application_performance_management|APM]] 도구

| 항목 | [[146_opentelemetry_otel_observability_standard|OTel]] | Datadog/NewRelic |
|:---|:---|:---|
| [[051_vendor_lock_in_cloud_computing|벤더 종속]] | 없음 (표준) | 있음 (에이전트 교체 어려움) |
| 비용 | [[191_oss_license_compliance|오픈소스]] (수집) + 백엔드 비용 | 고가 ([[001_dikw_pyramid|데이터]] 볼륨 과금) |
| 기능 완성도 | 계속 성장 중 | 성숙, 올인원 |
| 다중 백엔드 | 가능 | 단일 (자사 플랫폼) |
| 엔터프라이즈 지원 | 커뮤니티 | 공식 [[085_sla|SLA]] |

📢 **섹션 요약 비유**: OTel은 표준 [[359_usb|USB]] [[446_port_and_bus|포트]], Datadog은 독자 규격 충전기다. USB는 어디서나 쓰지만 충전 속도는 독자 규격이 더 빠를 수 있다.

## Ⅳ. 실무 적용 및 기술사 판단

### 텔레메트리 도입 [[435_checklist_based_testing|체크리스트]]

- [ ] 4 Golden [[611_conditional_access_signals|Signals]] 수집 [[123_pipe|파이프]]라인 구성 완료 여부
- [ ] [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]: [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[303_trace_id|Trace ID]] 전파 (`traceparent` [[461_http_stateless_connection_oriented|HTTP]] 헤더)
- [ ] 샘플링 [[268_strategy_pattern|전략]]: 개발=100%, 스테이징=[[489_raid_10_hybrid|10]]%, 프로덕션=1% + Tail [[056_표본화_Sampling|Sampling]]
- [ ] PII [[172_maas_mobility_as_a_service|마스]]킹: Collector Processor에서 [[781_personal_information|개인정보]] 필드 제거
- [ ] Cardinality 관리: 레이블 조합 수 제한 ([[136_prometheus|Prometheus]] [[307_memory_protection|메모리 보호]])

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

| [[128_water_scrum_fall_anti_pattern|안티패턴]] | 문제 | 해결 방법 |
|:---|:---|:---|
| 모든 트레이스 100% 보존 | 저장 비용 폭발 | Tail [[056_표본화_Sampling|Sampling]] 적용 |
| 고카디널리티 레이블 | [[136_prometheus|Prometheus]] [[157_oom_killer|OOM]] | user_id는 레이블 금지 |
| [[146_opentelemetry_otel_observability_standard|OTel]] 없이 [[090_service_kubernetes_network_load_balancing|서비스]]별 개별 계측 | 파편화, 상관 불가 | [[146_opentelemetry_otel_observability_standard|OTel]] SDK 표준화 |

📢 **섹션 요약 비유**: 고카디널리티 레이블은 100만 명의 이름을 서랍 라벨로 쓰는 것이다. 서랍장이 폭발한다.

## Ⅴ. 기대효과 및 결론

### 기대효과

| 항목 | [[146_opentelemetry_otel_observability_standard|OTel]] 이전 | [[146_opentelemetry_otel_observability_standard|OTel]] 도입 후 |
|:---|:---|:---|
| 장애 탐지 MTTD | 30~60분 | 2~5분 |
| 장애 [[658_ir_recovery|복구]] [[451_mttr|MTTR]] | 2~4시간 | 30~60분 |
| [[090_service_kubernetes_network_load_balancing|서비스]] 간 호출 추적 | 불가 | 단일 Trace로 전체 경로 |
| [[229_monitor|모니터]]링 도구 수 | 5~10개 (파편화) | 1~3개 (통합) |

### 한계 및 선결 과제

- [[146_opentelemetry_otel_observability_standard|OTel]] SDK 자동 계측 지원 언어 제한 (Go, Java, Python, JS 강력, [[782_memory_safety_rust_compiler_verification|Rust]] 성장 중)
- Collector 클러스터 자체 운영 복잡도 ([[205_kubernetes_container_orchestration|Kubernetes]] [[334_process|DaemonSet]] 권장)
- 대용량 [[568_logs_distributed_logging_elk_fluentd|로그]] 파싱 비용: [[168_grafana|Grafana]] Loki, [[302_cdc|ElasticSearch]] 인덱싱 비용 설계 필요
- Tail [[056_표본화_Sampling|Sampling]] Collector: 모든 스팬 [[454_buffering|버퍼링]] 필요 → 고메모리 필요

📢 **섹션 요약 비유**: [[146_opentelemetry_otel_observability_standard|OTel]] 도입은 병원에 전자의무기록 시스템을 도입하는 것이다. 모든 진료 기록이 통합되면 어느 과 의사든 즉시 전체 이력을 볼 수 있다.

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| [[146_opentelemetry_otel_observability_standard|OTel]] | 표준 | [[190_cncf_landscape_observability|CNCF]] [[111_observability_metrics_logs_traces|관측 가능성]] 표준 |
| Traces | 세 기둥 | [[136_variance|분산]] 요청 추적 |
| [[567_metrics_time_series_prometheus_grafana|Metrics]] | 세 기둥 | 수치 시스템 상태 |
| [[568_logs_distributed_logging_elk_fluentd|Logs]] | 세 기둥 | 시간 순 이벤트 기록 |
| 4 Golden [[611_conditional_access_signals|Signals]] | 핵심 지표 | [[015_지연_데이터_관점|지연]]·트래픽·오류·포화도 |
| Tail [[056_표본화_Sampling|Sampling]] | 최적화 | 중요 트레이스 선택 보존 |

### 📈 관련 키워드 및 발전 흐름도

```
O-RAN 네트워크 장비 지표 수동 수집 한계
    │
    ▼
스트리밍 텔레메트리 (gRPC/gNMI) - 실시간 전송
    │
    ▼
Kafka + Flink - 대용량 텔레메트리 스트리밍 파싱
    │
    ▼
시계열 DB (InfluxDB, OpenTSDB) 저장·분석
    │
    ▼
ML 기반 네트워크 이상 탐지 자동화
```

> **키워드**: Telemetry, [[782_o_ran_open_ran_white_box_interface|O-RAN]], gNMI, [[479_grpc_protobuf_http2|gRPC]], [[179_kafka_flink_watermark_time_window|Kafka]], Flink, Time Series, Network Analytics, Streaming Parsing

### 👶 어린이를 위한 3줄 비유 설명

1. OTel은 모든 선생님이 같은 양식의 출석부를 쓰는 것이에요. 어느 반이든 같은 방식으로 기록해요.
2. 4 Golden Signals는 선생님이 매일 [[396_validation|확인]]하는 4가지 항목이에요: 수업 시간([[015_지연_데이터_관점|지연]]), 출석률(트래픽), 결석 사유(오류), 교실 혼잡도(포화도).
3. Tail Sampling은 결석하거나 지각한 학생 기록만 자세히 남기는 거예요. 모든 학생 기록을 다 남기면 종이가 부족하니까요.
