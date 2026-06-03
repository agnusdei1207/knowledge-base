+++
weight = 145
title = "145. Jaeger & Zipkin - 분산 트레이싱 백엔드 비교"
date = "2026-04-19"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Jaeger(Uber, [[190_cncf_landscape_observability|CNCF]])와 Zipkin(Twitter, [[191_oss_license_compliance|오픈소스]])은 **[[136_variance|분산]] 트레이스 [[001_dikw_pyramid|데이터]]를 수집·저장·[[003_bigdata_7v|시각화]]**하는 트레이싱 백엔드이며, Waterfall UI로 [[090_service_kubernetes_network_load_balancing|서비스]] 간 호출 체인의 [[015_지연_데이터_관점|지연]]·에러를 분석한다.
> 2. **가치**: [[568_logs_distributed_logging_elk_fluentd|로그]]만으로는 **MSA의 어느 [[090_service_kubernetes_network_load_balancing|서비스]]가 병목인지** 알 수 없지만, Jaeger/Zipkin은 **전체 호출 체인을 Gantt 차트로 [[003_bigdata_7v|시각화]]**하여 병목 [[090_service_kubernetes_network_load_balancing|서비스]]·[[298_qkv_attention|쿼리]]를 즉시 [[655_ir_detection_analysis|식별]]한다.
> 3. **판단 포인트**: Jaeger(Go, [[190_cncf_landscape_observability|CNCF]], [[179_kafka_flink_watermark_time_window|Kafka]] 지원)가 K8s 환경에서 주류이며, [[168_grafana|Grafana]] Tempo(저비용, [[494_object_storage|오브젝트 스토리지]])가 차세대 대안이다. [[146_opentelemetry_otel_observability_standard|OTel]] SDK로 계측하면 백엔드를 자유롭게 교체할 수 있다.

---

## Ⅰ. 개요 및 필요성

```text
Jaeger 아키텍처:
  OTel SDK → Collector → Storage(ES/Cassandra) → UI
Zipkin 아키텍처:
  SDK → Transport(HTTP/Kafka) → Storage(ES) → UI
Tempo: OTel → S3/GCS (인덱스 없음, 저비용)
```

- **📢 섹션 요약 비유**: Jaeger/Zipkin은 **비행 관제탑**이다. 모든 비행기(요청)의 경로·[[015_지연_데이터_관점|지연]]·이상을 **한눈에** [[229_monitor|모니터]]링한다.

---

## Ⅱ~Ⅴ. 결론

Jaeger는 **K8s 트레이싱의 [[190_cncf_landscape_observability|CNCF]] 표준**이며, Tempo(저비용)와 [[146_opentelemetry_otel_observability_standard|OTel]](표준 계측)이 트렌드이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Jaeger** | [[190_cncf_landscape_observability|CNCF]] 트레이싱 |
| **Zipkin** | [[191_oss_license_compliance|오픈소스]] 선구자 |
| **Tempo** | 저비용 대안 |
| **[[146_opentelemetry_otel_observability_standard|OTel]]** | 계측 표준 |
| **Waterfall** | [[003_bigdata_7v|시각화]] UI |

### 📈 관련 키워드 및 발전 흐름도

```text
[Dapper (Google, 2010)] → [Zipkin (Twitter, 2012)]
    → [Jaeger (Uber/CNCF, 2017)]
    → [Grafana Tempo (2020, 저비용)]
    → [현재: OTel 수렴 — 백엔드 교체 자유]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Jaeger/Zipkin은 **비행 관제탑**이에요. 모든 비행기(요청) 경로를 봐요.
2. "이 비행기는 **서울 공항에서 2시간 [[015_지연_데이터_관점|지연]]됐네!**" → 병목 발견!
3. OTel로 계측하면 **관제탑(백엔드)을 자유롭게** 바꿀 수 있어요!
