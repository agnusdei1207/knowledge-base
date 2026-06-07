---
title: "Distributed Tracing Trace ID"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 321
---
> **핵심 인사이트**
> - [Distributed Tracing](/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/) ([분산 추적](/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/))은 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 환경에서 단일 요청의 전체 흐름을 Trace ID로 연결해 병목·오류를 추적한다.
> - Trace (트레이스)는 연관된 Span (스팬)의 집합이고, 각 Span은 하나의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 작업 단위를 나타낸다.
> - W3C Trace [Context](/studynote/02_operating_system/01_overview_architecture/033_context/) 표준으로 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [Trace ID](/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/) 전파가 표준화됐다.

---

## Ⅰ. Trace와 Span 구조

```
Trace ID: abc-123
------------------------------------------------------
Span 1: API Gateway       [0ms ---------------- 200ms]
  Span 2: Order Service     [10ms ------- 180ms]
    Span 3: Inventory Svc      [20ms -- 80ms]
    Span 4: DB Query              [90ms - 160ms]
------------------------------------------------------
```

| 개념       | 정의                                          |
|------------|-----------------------------------------------|
| Trace      | 단일 요청 전체 수명주기를 나타내는 Span 집합   |
| Span       | 하나의 작업 단위 ([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 호출, DB [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 등)    |
| [Trace ID](/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/)   | Trace 전체를 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하는 고유 ID                 |
| Span ID    | 개별 Span을 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하는 ID                       |
| Parent ID  | 상위 Span을 가리키는 ID (트리 구조 형성)      |

> 📢 **Ⅰ 섹션 요약 비유**
> Trace는 여행 일정 전체, Span은 각 도시에서의 일정 — Trace ID는 여행 예약 번호다.

---

## Ⅱ. Trace [Context](/studynote/02_operating_system/01_overview_architecture/033_context/) 전파

[HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 헤더를 통해 Trace ID가 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 전달된다.

W3C Trace [Context](/studynote/02_operating_system/01_overview_architecture/033_context/) 표준 헤더:
```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
             버전  TraceID                          SpanID        플래그
```

B3 Propagation (Zipkin 방식):
```
X-B3-TraceId: 4bf92f3577b34da6a3ce929d0e0e4736
X-B3-SpanId:  00f067aa0ba902b7
X-B3-Sampled: 1
```

> 📢 **Ⅱ 섹션 요약 비유**
> [Trace ID](/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/) 전파는 릴레이 바통 — 각 주자([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))가 같은 바통([Trace ID](/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/))을 넘겨받아 이어 달린다.

---

## Ⅲ. [Sampling](/studynote/03_network/01_data_communication/056_표본화_Sampling/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)             | 설명                                     |
|------------------|------------------------------------------|
| Head [Sampling](/studynote/03_network/01_data_communication/056_표본화_Sampling/)    | 요청 시작 시점에 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)로 샘플링 여부 결정  |
| Tail [Sampling](/studynote/03_network/01_data_communication/056_표본화_Sampling/)    | 요청 완료 후 오류·[지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 기준으로 샘플링   |
| [Rate Limiting](/studynote/09_security/05_web_app_security/520_rate_limiting/)    | 초당 N개 Trace만 샘플링                  |

Tail Sampling이 더 유용하지만 구현 복잡도가 높다 — [OpenTelemetry](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector에서 지원한다.

> 📢 **Ⅲ 섹션 요약 비유**
> 샘플링은 음식점 품질 검사 — 모든 접시를 다 검사하지 않고 의심스러운 것만 골라 집중 점검한다.

---

## Ⅳ. 대표 도구

| 도구         | 특징                                       |
|--------------|--------------------------------------------|
| Jaeger       | [CNCF](/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 졸업 프로젝트, Uber 기원              |
| Zipkin       | Twitter 기원, B3 Propagation 표준화         |
| Tempo        | [Grafana](/studynote/16_bigdata/08_visualization/168_grafana/) Labs, Loki·Prometheus와 통합        |
| AWS X-Ray    | AWS 네이티브 [분산 추적](/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)              |

[OpenTelemetry](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) SDK가 각 도구의 공통 계측 레이어 역할을 한다.

> 📢 **Ⅳ 섹션 요약 비유**
> Jaeger·Zipkin·Tempo는 각각 다른 브랜드의 GPS 앱이고, OpenTelemetry는 표준 지도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 제공하는 플랫폼이다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소         | 역할                                    |
|-------------------|-----------------------------------------|
| Trace             | 단일 요청 전체 수명주기                  |
| Span              | 개별 작업 단위                          |
| [Trace ID](/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/)          | Trace 전체 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)                       |
| W3C Trace [Context](/studynote/02_operating_system/01_overview_architecture/033_context/) | 표준 헤더 기반 Trace 전파 규격          |
| [Sampling](/studynote/03_network/01_data_communication/056_표본화_Sampling/)          | 추적 오버헤드 제어 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)                 |
| Jaeger / Zipkin   | [분산 추적](/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/) 백엔드 도구                   |

### 관련 키워드 및 발전 흐름도

```
Distributed Tracing
    +-- Trace / Span / Trace ID -> 기본 데이터 구조
    +-- W3C Trace Context / B3 -> 전파 표준
    +-- Sampling -> Head / Tail / Rate Limiting
    +-- OpenTelemetry -> 표준 계측 SDK + Collector
```

> 🧒 **어린이 비유**
> Trace ID는 소포 운송장 번호예요. 물건이 어느 배송센터를 거쳤는지 한 번호로 전부 추적할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 321 / 373

<- **이전**: [Observability Metrics Logs Traces](/studynote/15_devops_sre/05_devsecops/320_metric/)
**다음**: [OpenTelemetry CNCF](/studynote/15_devops_sre/05_devsecops/322_cncf/) ->

---
