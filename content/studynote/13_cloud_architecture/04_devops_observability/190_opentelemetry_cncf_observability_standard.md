+++
title = "190. 오픈텔레메트리 (OpenTelemetry, CNCF 옵저버빌리티 표준)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/)([OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/))는 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 트레이스(MELT의 M·L·T) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·수집·전송하는 벤더 중립 [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/)([Cloud Native](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/) Computing Foundation, [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 컴퓨팅 재단) [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 표준으로, "한 번 계측하면 어떤 백엔드로도 전송 가능"한 [옵저버빌리티](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) 인프라 표준이다.
> 2. **가치**: [벤더 종속](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/)([Vendor Lock-in](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/254_cloud_vendor_lock_in_avoidance_portability_multi_cloud/))을 방지하여 Datadog에서 [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/)/Jaeger로 또는 그 반대로 언제든 백엔드를 교체할 수 있으며, 자동 계측으로 코드 수정 없이 대부분의 프레임워크에 트레이스·[메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)을 즉시 추가할 수 있다.
> 3. **판단 포인트**: [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) SDK + [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector 조합이 현재 최선의 아키텍처이며, Collector를 중간에 두어 백엔드를 결합·분기·필터링하는 파이프라인을 유연하게 구성할 수 있다.

---

## Ⅰ. 개요 및 필요성

[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 추적의 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 시대에는 Jaeger, Zipkin, Datadog [APM](/knowledge-base/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/) 등 각 도구가 자체 SDK를 제공했다. 회사가 Datadog을 쓰다가 Jaeger로 교체하려면 모든 서비스의 계측 코드를 다시 작성해야 했다. 이것이 [벤더 종속](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/) 문제다.

OpenTracing(오픈 추적)과 OpenCensus(오픈 센서스) 두 경쟁 표준이 존재하다가, 2019년 두 프로젝트가 합쳐져 [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/)(오픈텔레메트리)가 탄생했다. 2023년 [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 졸업 프로젝트로 승격되며 사실상 업계 표준이 되었다.

OTel의 설계 철학은 "수집(Instrumentation)과 저장(Backend)의 분리"다. 애플리케이션은 [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) SDK로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고, [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector가 수집·처리하여 여러 백엔드([Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/), Jaeger, Datadog 등)로 동시에 전송할 수 있다. 백엔드를 교체해도 애플리케이션 코드는 바꿀 필요가 없다.

📢 **섹션 요약 비유**: OTel은 [USB](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/) Type-C 표준이다. 표준 케이블 하나로 충전기, [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/), 스토리지를 모두 연결하듯, [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) SDK 하나로 [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/), Jaeger, Datadog 등 어떤 백엔드에도 연결된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 전체 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">애플리케이션 계측</div></div>
<div class="kb-diagram-note">서비스 코드</div>
<div class="kb-diagram-tree-item" style="--depth:0">OTel Java/Python/Go SDK</div>
<div class="kb-diagram-note">── 자동 계측 (Auto-instrumentation)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── HTTP, DB, gRPC 자동 Span 생성</div></div>
<div class="kb-diagram-note">── 수동 계측 (Manual)</div>
<div class="kb-diagram-note">── 비즈니스 로직 커스텀 Span</div>
<div class="kb-diagram-note">↓ OTLP (OpenTelemetry Protocol) gRPC/HTTP</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">수집 파이프라인</div></div>
<div class="kb-diagram-note">OTel Collector</div>
<div class="kb-diagram-tree-item" style="--depth:0">Receivers: OTLP, Jaeger, Zipkin, Prometheus</div>
<div class="kb-diagram-tree-item" style="--depth:0">Processors: 배치, 샘플링, 필터, 보강</div>
<div class="kb-diagram-tree-item" style="--depth:0">Exporters: Prometheus, Jaeger, Datadog, Loki</div>
<div class="kb-diagram-note">Prometheus Jaeger Datadog</div>
<div class="kb-diagram-note">(메트릭) (트레이스) (통합 APM)</div>
</div>
</div>



| [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 구성 요소 | 설명 |
|:---|:---|
| [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) SDK | 언어별 계측 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) (Java, Python, Go, JS 등) |
| Auto-instrumentation | 에이전트/바이트코드 조작으로 코드 수정 없이 계측 |
| OTLP | [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Line [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/), [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 전용 전송 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector | 수집·처리·내보내기 파이프라인 |
| Resource | 서비스명, [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 환경 등 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) |

📢 **섹션 요약 비유**: [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector는 물류 터미널이다. 다양한 공급처(SDK)에서 화물(텔레메트리)을 받아 분류하고, 여러 목적지([Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/), Jaeger, Datadog)로 동시에 배송한다.

---

## Ⅲ. 비교 및 연결

### [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) vs 이전 표준·도구

| 항목 | OpenTracing | OpenCensus | [OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) |
|:---|:---|:---|:---|
| 상태 | 아카이브 | 아카이브 | 현재 표준 |
| 범위 | 추적만 | 추적 + [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) | 추적 + [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) + [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) |
| 벤더 중립 | ✅ | ✅ | ✅ |
| [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 상태 | 아카이브 | 아카이브 | 졸업 (2023) |

<strong><a href="/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/">OTel</a> Collector <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> 예시 (YAML):</strong>
```yaml
receivers:
  otlp:
    protocols:
      grpc: {endpoint: "0.0.0.0:4317"}
      http: {endpoint: "0.0.0.0:4318"}

processors:
  batch:
    timeout: 5s
  tail_sampling:
    policies: [{name: errors, type: status_code, status_code: {status_codes: [ERROR]}}]

exporters:
  prometheus:
    endpoint: "0.0.0.0:8888"
  jaeger:
    endpoint: "jaeger:14250"
  datadog:
    api:
      key: ${DD_API_KEY}

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, tail_sampling]
      exporters: [jaeger, datadog]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```

📢 **섹션 요약 비유**: [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)은 회사 메일 서버 규칙이다. "받은 메일 중 'ERROR' 포함된 것은 Slack에도 보내고, 모든 메일은 아카이브에 저장"처럼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름을 코드로 정의한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**언어별 자동 계측 방법:**

```bash
# Java (에이전트 방식)
java -javaagent:opentelemetry-javaagent.jar \
     -Dotel.service.name=my-service \
     -Dotel.exporter.otlp.endpoint=http://collector:4317 \
     -jar app.jar

# Python (SDK 방식)
pip install opentelemetry-sdk opentelemetry-instrumentation-flask
opentelemetry-instrument python app.py

# Node.js
npm install @opentelemetry/auto-instrumentations-node
node -r @opentelemetry/auto-instrumentations-node app.js
```

<strong><a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/">쿠버네티스</a> 배포 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>:</strong>
- <strong><a href="/knowledge-base/studynote/11_design_supervision/06_exam_summary/334_process/">DaemonSet</a> Collector</strong>: 각 노드에 배포, 노드 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 수집
- <strong><a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/546_sidecar_proxy_pattern/">Sidecar</a> Collector</strong>: Pod마다 배포, 세밀한 필터링
- **Gateway Collector**: 중앙 집중, 외부 전송 전 처리

**Semantic Conventions(시맨틱 컨벤션):**
- OTel이 정의한 표준 속성명 규약
- `http.method`, `db.system`, `net.peer.port` 등
- 일관된 속성명으로 여러 서비스의 트레이스 비교 용이

📢 **섹션 요약 비유**: Semantic Conventions는 국제 도량형 표준이다. "1kg"가 전 세계에서 같은 무게를 의미하듯, `http.method=GET`이 모든 서비스에서 동일한 의미를 가지도록 표준화한다.

---

## Ⅴ. 기대효과 및 결론

[OpenTelemetry](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 도입은 [옵저버빌리티](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) 인프라의 장기 투자 관점에서 필수적이다. 표준 SDK를 사용하면 어떤 백엔드 도구를 선택해도 재계측 없이 전환이 가능하여 도구 선택의 자유도가 극적으로 높아진다.

자동 계측의 가치는 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 도입 비용을 획기적으로 낮춘다는 데 있다. Spring Boot, Django, Express.js 같은 주류 프레임워크는 [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 에이전트 하나로 수십 개의 자동 Span이 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되어, 개발자가 첫 날부터 트레이스를 볼 수 있다.

미래 전망으로 OTel은 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 지원도 성숙되고 있어 MELT 전체를 하나의 표준 SDK로 다루는 날이 가까워지고 있다. [옵저버빌리티](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)의 통합 표준으로서 OTel의 중요성은 계속 커질 것이다.

📢 **섹션 요약 비유**: OpenTelemetry는 전 세계 공통 언어다. 개발자가 영어([OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) SDK)로 한 번 작성하면 프랑스어, 중국어, 스페인어([Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/), Jaeger, Datadog) 사용자 모두와 소통할 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [옵저버빌리티](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) | OTel이 MELT 수집의 표준 인프라 |
| OTLP | [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) 전용 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| [OTel](/knowledge-base/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/) Collector | 수집·처리·분기의 중앙 파이프라인 |
| 벤더 중립성 | OTel의 핵심 가치, 백엔드 교체 자유 |
| Semantic Conventions | 표준 속성명 규약으로 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 보장 |
| 자동 계측 | 코드 수정 없이 Span·[메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |

### 👶 어린이를 위한 3줄 비유 설명
1. OpenTelemetry는 전 세계 어디서나 쓸 수 있는 만능 어댑터예요.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">벤더별 전용 SDK (Jaeger SDK · Datadog SDK → 벤더 종속)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">OpenTelemetry (OTel): CNCF 표준</div>
<div class="kb-diagram-tree-item" style="--depth:2">SDK: 언어별 자동 계측 (Auto-instrumentation)</div>
<div class="kb-diagram-tree-item" style="--depth:2">Collector: 수집 · 처리 · 라우팅</div>
<div class="kb-diagram-tree-item" style="--depth:2">OTLP: 오픈 프로토콜</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">백엔드 선택 자유: Jaeger · Grafana · Datadog · Splunk</div>
</div>
</div>


2. 한 번 계측(plug-in)해두면 [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/), Jaeger, Datadog 어디에든 연결할 수 있어요.
3. 덕분에 더 좋은 도구가 나와도 처음부터 다시 만들 필요 없이 쉽게 바꿀 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 189 / 371

← **이전**: [189. Trace ID / Span ID / Context Propagation](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/189_trace_id_span_context_propagation/)
**다음**: [191. 카오스 엔지니어링 (Chaos Engineering)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/191_chaos_engineering_chaos_monkey/) →

---
