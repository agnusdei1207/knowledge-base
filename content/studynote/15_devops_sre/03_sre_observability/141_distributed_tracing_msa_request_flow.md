---
title: "141. Distributed Tracing Msa Request Flow"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [분산 트레이싱](/studynote/04_software_engineering/02_requirements_analysis/112_distributed_tracing_microservices/)은 <strong>하나의 사용자 요청이 여러 <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/">마이크로서비스</a>를 거치는 전체 경로를 Trace ID로 추적</strong>하는 기술이며, 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 구간을 Span으로 기록하여 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)·에러 지점을 정확히 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)한다.
> 2. **가치**: MSA에서 "API가 느리다"는 <strong>어떤 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>가 병목인지</strong> [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)만으로는 알 수 없지만, 트레이싱은 <strong>A->B->C->D 전체 호출 체인의 각 구간 소요 시간</strong>을 Waterfall로 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)한다.
> 3. **판단 포인트**: [OpenTelemetry](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/)([OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/))가 계측 표준이며, Jaeger·Tempo·Zipkin이 트레이스 백엔드이다. 샘플링(1~[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%)으로 오버헤드를 제어한다.

---

## Ⅰ. 개요 및 필요성

```text
요청: 사용자 -> API GW -> 주문 서비스 -> 결제 서비스 -> DB
Trace: {trace_id: "abc123"}
  Span 1: API GW (10ms)
  Span 2: 주문 서비스 (50ms)
  Span 3: 결제 서비스 (200ms) <- 병목!
  Span 4: DB 쿼리 (30ms)
```

- **📢 섹션 요약 비유**: [분산 트레이싱](/studynote/04_software_engineering/02_requirements_analysis/112_distributed_tracing_microservices/)은 <strong>택배 추적</strong>이다. 택배(요청)가 어느 물류센터([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))에서 얼마나 머물렀는지 추적한다.

---

## Ⅱ~Ⅴ. 결론

[분산 트레이싱](/studynote/04_software_engineering/02_requirements_analysis/112_distributed_tracing_microservices/)은 <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a> <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 분석·장애 진단의 필수 도구</strong>이며, [OTel](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/)+Jaeger/Tempo가 표준 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Trace** | 전체 요청 경로 |
| **Span** | 개별 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 구간 |
| <strong><a href="/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/">Trace ID</a></strong> | 요청 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) |
| <strong><a href="/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/">OpenTelemetry</a></strong> | 계측 표준 |
| **Jaeger/Tempo** | 트레이스 백엔드 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Dapper (Google, 2010)] -> [Zipkin (Twitter, 2012)]
    -> [Jaeger (Uber, 2017)] -> [OpenTelemetry (2019)]
    -> [Grafana Tempo (2020)]
    -> [현재: OTel 통합 — Metrics·Logs·Traces 상관 분석]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [분산 트레이싱](/studynote/04_software_engineering/02_requirements_analysis/112_distributed_tracing_microservices/)은 <strong>택배 추적</strong>이에요. 택배가 **어디를 거쳤는지** 봐요.
2. "결제 센터에서 **200ms나 머물렀네!**" -> 여기가 <strong>병목</strong>이구나!
3. 모든 택배에 <strong>추적 번호(<a href="/studynote/13_cloud_architecture/05_data_engineering/303_trace_id/">Trace ID</a>)</strong>를 붙여서 끝까지 따라가요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 141 / 373

<- **이전**: [140. 구조화 로깅 (Structured Logging) - JSON 포맷 표준화](/studynote/15_devops_sre/03_sre_observability/140_structured_logging_json_format/)
**다음**: [142. Trace·Span·Context Propagation - 분산 추적의 핵심 구성](/studynote/15_devops_sre/03_sre_observability/142_trace_request_context/) ->

---
