---
title: Distributed Tracing Trace ID
date: '2026-05-09'
tags:
- studynote-devops-sre
---

> **핵심 인사이트**
> - [[569_distributed_tracing_opentelemetry_jaeger|Distributed Tracing]] ([[569_distributed_tracing_opentelemetry_jaeger|분산 추적]])은 [[532_microservices_decomposition_patterns|마이크로서비스]] 환경에서 단일 요청의 전체 흐름을 Trace ID로 연결해 병목·오류를 추적한다.
> - Trace (트레이스)는 연관된 Span (스팬)의 집합이고, 각 Span은 하나의 [[090_service_kubernetes_network_load_balancing|서비스]] 작업 단위를 나타낸다.
> - W3C Trace [[033_context|Context]] 표준으로 [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[303_trace_id|Trace ID]] 전파가 표준화됐다.

---

## Ⅰ. Trace와 Span 구조

```
Trace ID: abc-123
──────────────────────────────────────────────────────
Span 1: API Gateway       [0ms ──────────────── 200ms]
  Span 2: Order Service     [10ms ─────── 180ms]
    Span 3: Inventory Svc      [20ms ── 80ms]
    Span 4: DB Query              [90ms ─ 160ms]
──────────────────────────────────────────────────────
```

| 개념       | 정의                                          |
|------------|-----------------------------------------------|
| Trace      | 단일 요청 전체 수명주기를 나타내는 Span 집합   |
| Span       | 하나의 작업 단위 ([[090_service_kubernetes_network_load_balancing|서비스]] 호출, DB [[298_qkv_attention|쿼리]] 등)    |
| [[303_trace_id|Trace ID]]   | Trace 전체를 [[655_ir_detection_analysis|식별]]하는 고유 ID                 |
| Span ID    | 개별 Span을 [[655_ir_detection_analysis|식별]]하는 ID                       |
| Parent ID  | 상위 Span을 가리키는 ID (트리 구조 형성)      |

> 📢 **Ⅰ 섹션 요약 비유**
> Trace는 여행 일정 전체, Span은 각 도시에서의 일정 — Trace ID는 여행 예약 번호다.

---

## Ⅱ. Trace [[033_context|Context]] 전파

[[461_http_stateless_connection_oriented|HTTP]] 헤더를 통해 Trace ID가 [[090_service_kubernetes_network_load_balancing|서비스]] 간 전달된다.

W3C Trace [[033_context|Context]] 표준 헤더:
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
> [[303_trace_id|Trace ID]] 전파는 릴레이 바통 — 각 주자([[090_service_kubernetes_network_load_balancing|서비스]])가 같은 바통([[303_trace_id|Trace ID]])을 넘겨받아 이어 달린다.

---

## Ⅲ. [[056_표본화_Sampling|Sampling]] [[268_strategy_pattern|전략]]

| [[268_strategy_pattern|전략]]             | 설명                                     |
|------------------|------------------------------------------|
| Head [[056_표본화_Sampling|Sampling]]    | 요청 시작 시점에 [[130_probability|확률]]로 샘플링 여부 결정  |
| Tail [[056_표본화_Sampling|Sampling]]    | 요청 완료 후 오류·[[015_지연_데이터_관점|지연]] 기준으로 샘플링   |
| [[520_rate_limiting|Rate Limiting]]    | 초당 N개 Trace만 샘플링                  |

Tail Sampling이 더 유용하지만 구현 복잡도가 높다 — [[146_opentelemetry_otel_observability_standard|OpenTelemetry]] Collector에서 지원한다.

> 📢 **Ⅲ 섹션 요약 비유**
> 샘플링은 음식점 품질 검사 — 모든 접시를 다 검사하지 않고 의심스러운 것만 골라 집중 점검한다.

---

## Ⅳ. 대표 도구

| 도구         | 특징                                       |
|--------------|--------------------------------------------|
| Jaeger       | [[190_cncf_landscape_observability|CNCF]] 졸업 프로젝트, Uber 기원              |
| Zipkin       | Twitter 기원, B3 Propagation 표준화         |
| Tempo        | [[168_grafana|Grafana]] Labs, Loki·Prometheus와 통합        |
| AWS X-Ray    | AWS 네이티브 [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] [[090_service_kubernetes_network_load_balancing|서비스]]              |

[[146_opentelemetry_otel_observability_standard|OpenTelemetry]] SDK가 각 도구의 공통 계측 레이어 역할을 한다.

> 📢 **Ⅳ 섹션 요약 비유**
> Jaeger·Zipkin·Tempo는 각각 다른 브랜드의 GPS 앱이고, OpenTelemetry는 표준 지도 [[001_dikw_pyramid|데이터]]를 제공하는 플랫폼이다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소         | 역할                                    |
|-------------------|-----------------------------------------|
| Trace             | 단일 요청 전체 수명주기                  |
| Span              | 개별 작업 단위                          |
| [[303_trace_id|Trace ID]]          | Trace 전체 [[289_identification_flags_fragmentation_offset|식별자]]                       |
| W3C Trace [[033_context|Context]] | 표준 헤더 기반 Trace 전파 규격          |
| [[056_표본화_Sampling|Sampling]]          | 추적 오버헤드 제어 [[268_strategy_pattern|전략]]                 |
| Jaeger / Zipkin   | [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] 백엔드 도구                   |

### 관련 키워드 및 발전 흐름도

```
Distributed Tracing
    ├── Trace / Span / Trace ID → 기본 데이터 구조
    ├── W3C Trace Context / B3 → 전파 표준
    ├── Sampling → Head / Tail / Rate Limiting
    └── OpenTelemetry → 표준 계측 SDK + Collector
```

> 🧒 **어린이 비유**
> Trace ID는 소포 운송장 번호예요. 물건이 어느 배송센터를 거쳤는지 한 번호로 전부 추적할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 321 / 373

← **이전**: [[320_metric|Observability Metrics Logs Traces]]
**다음**: [[322_cncf|OpenTelemetry CNCF]] →

---
