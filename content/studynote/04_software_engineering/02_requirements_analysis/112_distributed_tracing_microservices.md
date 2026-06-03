---
title: 112. 분산 트레이싱 (Distributed Tracing) - Span·Trace ID·OpenTelemetry 추적 체계
date: '2026-04-19'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[136_variance|분산]] 트레이싱은 [[619_msa_traffic_hardware|MSA]] 환경에서 하나의 사용자 요청이 **N개 [[090_service_kubernetes_network_load_balancing|서비스]]를 거치는 전체 경로(Trace)**를 고유 ID([[303_trace_id|Trace ID]])로 추적하고, 각 [[090_service_kubernetes_network_load_balancing|서비스]] 내 처리 구간(Span)의 **레이턴시·에러를 [[003_bigdata_7v|시각화]]**하여 병목을 특정하는 기법이다.
> 2. **가치**: 모놀리스에서는 하나의 스택트레이스로 디버깅이 가능하지만, MSA에서는 "주문→결제→배송→알림" 4개 [[090_service_kubernetes_network_load_balancing|서비스]] 중 **어디서 500ms가 추가됐는지** 찾는 것 자체가 난제이며, [[136_variance|분산]] 트레이싱이 유일한 해법이다.
> 3. **판단 포인트**: [[146_opentelemetry_otel_observability_standard|OpenTelemetry]]([[146_opentelemetry_otel_observability_standard|OTel]])가 [[190_cncf_landscape_observability|CNCF]] 표준으로 계측(Instrumentation)을 통일하고, Jaeger·Tempo·Zipkin이 백엔드 저장·[[003_bigdata_7v|시각화]]를 담당하며, **[[570_trace_id_span_id_context_propagation|Context Propagation]](W3C Trace [[033_context|Context]])**으로 [[090_service_kubernetes_network_load_balancing|서비스]] 간 Trace ID를 전파한다.

---

## Ⅰ. 개요 및 필요성

MSA에서 [[542_api_gateway|API Gateway]] → Auth → Order → Payment → Notification으로 이어지는 요청 체인에서, 전체 응답이 2초 걸린다. "어디서 느린가?"를 찾으려면 각 [[090_service_kubernetes_network_load_balancing|서비스]]의 [[568_logs_distributed_logging_elk_fluentd|로그]]를 일일이 시간순으로 대조해야 한다.

```text
┌───────────────────────────────────────────────────────┐
│      분산 트레이싱 Trace/Span 구조                     │
├───────────────────────────────────────────────────────┤
│  Trace ID: abc-123 (전체 요청 1건)                    │
│  ├─ Span 1: API Gateway    [0ms ─── 50ms]            │
│  ├─ Span 2: Auth Service   [50ms ── 100ms]           │
│  ├─ Span 3: Order Service  [100ms ─ 800ms] ← 병목!  │
│  │   └─ Span 3.1: DB Query [200ms ─ 750ms] ← 원인!  │
│  ├─ Span 4: Payment        [800ms ─ 1200ms]          │
│  └─ Span 5: Notification   [1200ms ─ 1250ms]         │
│  총 응답: 1250ms                                      │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Trace ID는 택배 송장번호이고, 각 Span은 물류 [[152_hub_dummy_switching_intelligent|허브]]([[090_service_kubernetes_network_load_balancing|서비스]])에서의 체류 시간이다. 송장을 추적하면 어느 [[152_hub_dummy_switching_intelligent|허브]]에서 택배가 멈췄는지 즉시 알 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 핵심 개념

| 개념 | 정의 | 비유 |
|:---|:---|:---|
| **Trace** | 하나의 요청이 거치는 전체 경로 | 택배 배송 전체 경로 |
| **Span** | Trace 내 하나의 [[090_service_kubernetes_network_load_balancing|서비스]] 처리 구간 | 물류 [[152_hub_dummy_switching_intelligent|허브]] 1곳에서의 체류 |
| **[[303_trace_id|Trace ID]]** | 전체 Trace를 식별하는 고유 ID | 택배 송장번호 |
| **Span ID** | 개별 Span을 식별하는 ID | [[152_hub_dummy_switching_intelligent|허브]]별 스캔 바코드 |
| **[[570_trace_id_span_id_context_propagation|Context Propagation]]** | [[461_http_stateless_connection_oriented|HTTP]] 헤더로 Trace ID를 [[090_service_kubernetes_network_load_balancing|서비스]] 간 전파 | 송장을 다음 [[152_hub_dummy_switching_intelligent|허브]]로 넘기기 |

### [[570_trace_id_span_id_context_propagation|Context Propagation]] 방식

W3C Trace [[033_context|Context]] 표준: [[461_http_stateless_connection_oriented|HTTP]] 헤더 `traceparent: 00-{trace-id}-{span-id}-{flags}`를 요청에 실어 다음 [[090_service_kubernetes_network_load_balancing|서비스]]로 전달한다.

- **📢 섹션 요약 비유**: [[033_context|Context]] Propagation은 릴레이 경주에서 바통([[303_trace_id|Trace ID]])을 다음 주자([[090_service_kubernetes_network_load_balancing|서비스]])에게 넘기는 것이다. 바통을 놓치면 추적이 끊긴다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[568_logs_distributed_logging_elk_fluentd|로그]] ([[568_logs_distributed_logging_elk_fluentd|Logs]]) | [[342_routing_metric_hop_bandwidth_delay|메트릭]] ([[567_metrics_time_series_prometheus_grafana|Metrics]]) | 트레이싱 (Traces) |
|:---|:---|:---|:---|
| **질문** | 무엇이 일어났나? | 얼마나 나쁜가? | **어디서 병목인가?** |
| **형태** | 텍스트 이벤트 | 시계열 수치 | Span 트리 |
| **[[619_msa_traffic_hardware|MSA]] 대응** | [[090_service_kubernetes_network_load_balancing|서비스]]별 [[136_variance|분산]] | [[090_service_kubernetes_network_load_balancing|서비스]]별 집계 | **전체 경로 추적** |
| **도구** | ELK, Loki | [[136_prometheus|Prometheus]] | Jaeger, Tempo |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 도입 [[435_checklist_based_testing|체크리스트]]
1. **[[146_opentelemetry_otel_observability_standard|OTel]] SDK 계측**: 각 [[090_service_kubernetes_network_load_balancing|서비스]]에 [[146_opentelemetry_otel_observability_standard|OpenTelemetry]] SDK 추가 (Auto-instrumentation 권장).
2. **Collector 배포**: [[146_opentelemetry_otel_observability_standard|OTel]] Collector를 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 또는 DaemonSet으로 배포하여 Span 수집.
3. **백엔드 선택**: Jaeger(분석)·Tempo(비용 효율)·Datadog([[309_saas|SaaS]]).
4. **샘플링 [[268_strategy_pattern|전략]]**: 전량 수집은 비용 폭발 → Head-based 또는 Tail-based 샘플링.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **샘플링 없이 전량 수집**: 초당 [[489_raid_10_hybrid|10]],000 요청 × 5 Span = 50,000 Span/s → 저장 비용 폭발.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 트레이싱 미도입 | 트레이싱 도입 | 개선 |
|:---|:---|:---|:---|
| 병목 특정 시간 | 수시간 ([[568_logs_distributed_logging_elk_fluentd|로그]] 대조) | **수분 (Span [[003_bigdata_7v|시각화]])** | 90% 단축 |
| [[451_mttr|MTTR]] ([[658_ir_recovery|복구]] 시간) | 30분+ | **10분 이하** | 66% 단축 |
| [[090_service_kubernetes_network_load_balancing|서비스]] 간 의존성 가시성 | 문서 기반 | **자동 [[090_service_kubernetes_network_load_balancing|서비스]] 맵** | 실시간 |

[[136_variance|분산]] 트레이싱은 [[615_ebpf|eBPF]] 기반 무계측(Zero-instrumentation) 추적과 결합하여, 코드 변경 없이 [[022_kernel_role|커널]] 레벨에서 Span을 자동 [[087_process_state_transition|생성]]하는 방향으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[146_opentelemetry_otel_observability_standard|OpenTelemetry]]** | 계측 표준, [[567_metrics_time_series_prometheus_grafana|Metrics]]·[[568_logs_distributed_logging_elk_fluentd|Logs]]·Traces 통합 SDK |
| **Jaeger / Tempo** | 트레이싱 백엔드 (저장·[[003_bigdata_7v|시각화]]) |
| **W3C Trace [[033_context|Context]]** | [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[303_trace_id|Trace ID]] 전파 표준 헤더 |
| **[[642_observability_telemetry|Observability]]** | 트레이싱이 속하는 3대 [[130_signal|신호]] 중 하나 |
| **[[828_service_mesh_microservice_communication_infrastructure|Service Mesh]] ([[302_service_mesh_istio|Istio]])** | [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 프록시가 자동으로 Span [[087_process_state_transition|생성]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[Google Dapper 논문 (2010) — 분산 트레이싱 개념 정립]
    │
    ▼
[Zipkin (2012, Twitter) — 최초 OSS 분산 트레이싱]
    │
    ▼
[Jaeger (2017, Uber) — CNCF 졸업 프로젝트]
    │
    ▼
[OpenTelemetry 통합 (2019~) — OpenTracing+OpenCensus 합병]
    │
    ▼
[현재: eBPF Zero-instrumentation — 코드 변경 없는 자동 추적]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 택배를 보내면 **송장번호([[303_trace_id|Trace ID]])**로 지금 어디에 있는지 추적할 수 있죠?
2. [[136_variance|분산]] 트레이싱도 인터넷 요청에 송장번호를 붙여서, **어느 컴퓨터에서 오래 멈췄는지** 찾아내요.
3. 덕분에 개발자가 "아! 여기가 느렸구나!"라고 **바로 고칠 수 있답니다!**

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 112 / 973

← **이전**: [[111_observability_metrics_logs_traces|111. 관측 가능성 (Observability) - Metrics·Logs·Traces 3대 신호와 SRE 실천]]
**다음**: [[113_chaos_engineering_chaos_monkey|113. 카오스 엔지니어링 (Chaos Engineering) - Chaos Monkey·정상 상태 가설·실험 설계]] →

---
