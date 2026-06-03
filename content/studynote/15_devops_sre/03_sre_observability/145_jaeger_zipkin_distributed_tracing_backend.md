+++
title = "145. Jaeger & Zipkin - 분산 트레이싱 백엔드 비교"
date = 2026-04-19

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Jaeger(Uber, [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/))와 Zipkin(Twitter, [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/))은 **[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 트레이스 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수집·저장·[시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)**하는 트레이싱 백엔드이며, Waterfall UI로 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 호출 체인의 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)·에러를 분석한다.
> 2. **가치**: [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)만으로는 **MSA의 어느 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 병목인지** 알 수 없지만, Jaeger/Zipkin은 **전체 호출 체인을 Gantt 차트로 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)**하여 병목 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)·[쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 즉시 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)한다.
> 3. **판단 포인트**: Jaeger(Go, [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/), [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 지원)가 K8s 환경에서 주류이며, [Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/) Tempo(저비용, [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/))가 차세대 대안이다. [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) SDK로 계측하면 백엔드를 자유롭게 교체할 수 있다.

---

## Ⅰ. 개요 및 필요성

```text
Jaeger 아키텍처:
  OTel SDK → Collector → Storage(ES/Cassandra) → UI
Zipkin 아키텍처:
  SDK → Transport(HTTP/Kafka) → Storage(ES) → UI
Tempo: OTel → S3/GCS (인덱스 없음, 저비용)
```

- **📢 섹션 요약 비유**: Jaeger/Zipkin은 **비행 관제탑**이다. 모든 비행기(요청)의 경로·[지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)·이상을 **한눈에** [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링한다.

---

## Ⅱ~Ⅴ. 결론

Jaeger는 **K8s 트레이싱의 [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 표준**이며, Tempo(저비용)와 [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/)(표준 계측)이 트렌드이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Jaeger** | [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 트레이싱 |
| **Zipkin** | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 선구자 |
| **Tempo** | 저비용 대안 |
| **[OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/)** | 계측 표준 |
| **Waterfall** | [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) UI |

### 📈 관련 키워드 및 발전 흐름도

```text
[Dapper (Google, 2010)] → [Zipkin (Twitter, 2012)]
    → [Jaeger (Uber/CNCF, 2017)]
    → [Grafana Tempo (2020, 저비용)]
    → [현재: OTel 수렴 — 백엔드 교체 자유]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Jaeger/Zipkin은 **비행 관제탑**이에요. 모든 비행기(요청) 경로를 봐요.
2. "이 비행기는 **서울 공항에서 2시간 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)됐네!**" → 병목 발견!
3. OTel로 계측하면 **관제탑(백엔드)을 자유롭게** 바꿀 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 145 / 373

← **이전**: [144. Context Propagation & Trace ID 전파 상세](/knowledge-base/studynote/15_devops_sre/03_sre_observability/144_context_propagation_trace_id/)
**다음**: [146. OpenTelemetry (OTel) - 관측 가능성 통합 표준](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) →

---
