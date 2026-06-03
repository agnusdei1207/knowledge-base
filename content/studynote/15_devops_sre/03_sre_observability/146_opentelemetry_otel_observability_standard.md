+++
title = "146. OpenTelemetry (OTel) - 관측 가능성 통합 표준"
date = 2026-04-19

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OpenTelemetry는 <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/">Metrics</a>·<a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">Logs</a>·Traces 3축 텔레메트리 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>의 수집·전파·내보내기를 통합 표준화</strong>한 [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 프로젝트이며, OpenTracing+OpenCensus의 통합체이다.
> 2. **가치**: 기존에는 [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/)([Metrics](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/))·ELK([Logs](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))·Jaeger(Traces)가 <strong>각각 다른 SDK·포맷</strong>을 사용했지만, OTel은 <strong>하나의 SDK로 3축을 모두 계측</strong>하고 백엔드를 자유롭게 교체할 수 있다(Vendor-neutral).
> 3. **판단 포인트**: OTel SDK(계측)→OTel Collector(수집·처리·내보내기)→Backend([Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/)·Jaeger·Loki)의 3계층이며, Auto-instrumentation으로 코드 변경 없이 계측할 수 있다.

---

## Ⅰ. 개요 및 필요성

```text
OTel 아키텍처:
  App + OTel SDK (계측) → OTel Collector → Backend
  Collector: 수집 → 처리(필터·샘플링) → 내보내기
  Backend: Prometheus(Metrics) + Jaeger(Traces) + Loki(Logs)
  Auto-instrumentation: 코드 변경 없이 자동 계측
```

- **📢 섹션 요약 비유**: OTel은 <strong>만국 공통 측정 기준(미터법)</strong>이다. 어떤 나라(백엔드)든 같은 단위(포맷)로 측정하면 호환된다.

---

## Ⅱ~Ⅴ. 결론

OpenTelemetry는 <strong>Observability의 <a href="/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/">CNCF</a> 통합 표준</strong>이며, Vendor-neutral로 백엔드 교체가 자유롭다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **OTel** | 통합 텔레메트리 |
| **SDK** | 계측 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) |
| **Collector** | 수집·처리·내보내기 |
| **OTLP** | 전송 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| **Auto-instrumentation** | 자동 계측 |

### 📈 관련 키워드 및 발전 흐름도

```text
[OpenTracing (2016)] + [OpenCensus (Google, 2018)]
    → [OpenTelemetry 통합 (2019)]
    → [OTel Traces GA (2021)] → [OTel Metrics GA (2023)]
    → [현재: OTel Logs GA — 3축 완성]
```

### 👶 어린이를 위한 3줄 비유 설명
1. OTel은 <strong>만국 공통 단위(미터법)</strong>예요. 어디서든 <strong>같은 방식</strong>으로 측정해요.
2. 예전에는 나라마다(도구마다) 단위가 달라서 **비교가 어려웠어요**.
3. OTel 하나면 <strong><a href="/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/">메트릭</a>·<a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a>·트레이스</strong>를 모두 같은 방식으로 수집해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 146 / 373

← **이전**: [145. Jaeger & Zipkin - 분산 트레이싱 백엔드 비교](/knowledge-base/studynote/15_devops_sre/03_sre_observability/145_jaeger_zipkin_distributed_tracing_backend/)
**다음**: [147. eBPF (Extended Berkeley Packet Filter) - 커널 레벨 샌드박스 관측 기술](/knowledge-base/studynote/15_devops_sre/03_sre_observability/147_ebpf_kernel_observability_cilium/) →

---
