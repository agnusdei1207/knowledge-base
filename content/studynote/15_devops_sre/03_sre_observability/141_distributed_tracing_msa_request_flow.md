---
title: 141. 분산 트레이싱 (Distributed Tracing) - MSA 요청 흐름 추적
date: '2026-04-19'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[112_distributed_tracing_microservices|분산 트레이싱]]은 **하나의 사용자 요청이 여러 [[532_microservices_decomposition_patterns|마이크로서비스]]를 거치는 전체 경로를 Trace ID로 추적**하는 기술이며, 각 [[090_service_kubernetes_network_load_balancing|서비스]] 구간을 Span으로 기록하여 [[015_지연_데이터_관점|지연]]·에러 지점을 정확히 [[655_ir_detection_analysis|식별]]한다.
> 2. **가치**: MSA에서 "API가 느리다"는 **어떤 [[090_service_kubernetes_network_load_balancing|서비스]]가 병목인지** [[568_logs_distributed_logging_elk_fluentd|로그]]만으로는 알 수 없지만, 트레이싱은 **A→B→C→D 전체 호출 체인의 각 구간 소요 시간**을 Waterfall로 [[003_bigdata_7v|시각화]]한다.
> 3. **판단 포인트**: [[146_opentelemetry_otel_observability_standard|OpenTelemetry]]([[146_opentelemetry_otel_observability_standard|OTel]])가 계측 표준이며, Jaeger·Tempo·Zipkin이 트레이스 백엔드이다. 샘플링(1~[[489_raid_10_hybrid|10]]%)으로 오버헤드를 제어한다.

---

## Ⅰ. 개요 및 필요성

```text
요청: 사용자 → API GW → 주문 서비스 → 결제 서비스 → DB
Trace: {trace_id: "abc123"}
  Span 1: API GW (10ms)
  Span 2: 주문 서비스 (50ms)
  Span 3: 결제 서비스 (200ms) ← 병목!
  Span 4: DB 쿼리 (30ms)
```

- **📢 섹션 요약 비유**: [[112_distributed_tracing_microservices|분산 트레이싱]]은 **택배 추적**이다. 택배(요청)가 어느 물류센터([[090_service_kubernetes_network_load_balancing|서비스]])에서 얼마나 머물렀는지 추적한다.

---

## Ⅱ~Ⅴ. 결론

[[112_distributed_tracing_microservices|분산 트레이싱]]은 **[[619_msa_traffic_hardware|MSA]] [[282_performance_tactics|성능]] 분석·장애 진단의 필수 도구**이며, [[146_opentelemetry_otel_observability_standard|OTel]]+Jaeger/Tempo가 표준 [[057_stack|스택]]이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Trace** | 전체 요청 경로 |
| **Span** | 개별 [[090_service_kubernetes_network_load_balancing|서비스]] 구간 |
| **[[303_trace_id|Trace ID]]** | 요청 [[289_identification_flags_fragmentation_offset|식별자]] |
| **[[146_opentelemetry_otel_observability_standard|OpenTelemetry]]** | 계측 표준 |
| **Jaeger/Tempo** | 트레이스 백엔드 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Dapper (Google, 2010)] → [Zipkin (Twitter, 2012)]
    → [Jaeger (Uber, 2017)] → [OpenTelemetry (2019)]
    → [Grafana Tempo (2020)]
    → [현재: OTel 통합 — Metrics·Logs·Traces 상관 분석]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[112_distributed_tracing_microservices|분산 트레이싱]]은 **택배 추적**이에요. 택배가 **어디를 거쳤는지** 봐요.
2. "결제 센터에서 **200ms나 머물렀네!**" → 여기가 **병목**이구나!
3. 모든 택배에 **추적 번호([[303_trace_id|Trace ID]])**를 붙여서 끝까지 따라가요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 141 / 373

← **이전**: [[140_structured_logging_json_format|140. 구조화 로깅 (Structured Logging) - JSON 포맷 표준화]]
**다음**: [[142_trace_request_context|142. Trace·Span·Context Propagation - 분산 추적의 핵심 구성]] →

---
