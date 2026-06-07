---
title: "OpenTelemetry Distributed Tracing Standard"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OpenTelemetry는 CNCF 표준 API/SDK/Collector로 W3C Trace Context(`traceparent`, `tracestate`)와 OTLP(OpenTelemetry Protocol, gRPC/HTTP)를 통해 컨텍스트 전파(Context Propagation)와 Span 데이터 수집·처리·내보내기를 벤더 중립적으로 통합한 분산 추적 표준이다.
> 2. **가치**: Jaeger/Zipkin/기존 APM 벤더 SDK 종속을 제거하여 ①계측 코드 1회 작성으로 다중 백엔드 전환 가능, ②OTel Collector의 Pipeline(Receiver->Processor->Exporter) 구성으로 트래픽 100k+ span/s 처리 시 약 70% 이상 저장 비용 절감, ③Trace+Metric+Log 3축 신호(Signal) 상관관계로 MTTR 평균 40~60% 단축 효과를 제공한다.
> 3. **판단 포인트**: Sampling 전략(Head-based vs Tail-based), 컬럼너(Collector) 단일/다중 배포 모델, eBPF/Zero-code Auto-instrumentation 적용 범위, 카디널리티 폭주 방지(Attribute Key 설계), 그리고 OTLP 전송 시 TLS/mTLS 보안과 백프레셔(backpressure) 처리가 핵심 설계 결정 포인트다.

---

## Ⅰ. 개요 및 필요성

MSA(마이크로서비스 아키텍처) 환경에서 한 번의 사용자 요청은 평균 6~50개의 서비스를 거치며, Kafka/RabbitMQ/Redis 같은 비동기 메시지 큐와 gRPC/HTTP/GraphQL을 혼합 호출한다. 기존에는 Zipkin, Jaeger, Datadog APM, New Relic, Dynatrace 등 **각 벤더의 독자 SDK**를 코드에 삽입해 추적 데이터를 수집했으나, 이는 ①벤더 Lock-in, ②이중/삼중 계측 코드 유지보수, ③신호(Signal) 간 상관관계 부재(Trace↔Metric↔Log) 문제를 야기했다.

OpenTelemetry(OTel)는 2019년 OpenTracing + OpenCensus 프로젝트가 합병되어 CNCF Incubating(2021) -> Graduated(2024) 단계로 성장한 **관측 가능성(Observability) 표준**이다. 핵심 목표는 **"한 번 계측(Instrument), 어디든 내보내기(Export)"** 이며, 현재 Java/JVM, .NET, Python, Go, Node.js, Rust, C++, PHP, Ruby, Swift 등 11개 이상 언어에 대한 공식 SDK를 제공한다.

```text
[기존 방식: 벤더 종속형 분산 추적]
  +-------------+   +-------------+   +-------------+
  |  Service A  |   |  Service B  |   |  Service C  |
  |  +-------+  |   |  +-------+  |   |  +-------+  |
  |  |Jaeger |  |   |  |Zipkin |  |   |  |Datadog|  |
  |  |  SDK  |  |   |  |  SDK  |  |   |  |  SDK  |  |
  |  +---+---+  |   |  +---+---+  |   |  +---+---+  |
  +------+------+   +------+------+   +------+------+
         |                 |                 |
         v                 v                 v
   +----------+      +----------+      +----------+
   |  Jaeger  |      |  Zipkin  |      | Datadog  |
   |  Backend |      | Backend  |      |   SaaS   |
   +----------+      +----------+      +----------+
   -> SDK 교체 = 코드 수정 = 서비스 재배포 = 운영 리스크

[OpenTelemetry 방식: 표준 API + Collector 기반 중립형 추적]
  +-------------+   +-------------+   +-------------+
  |  Service A  |   |  Service B  |   |  Service C  |
  |  +-------+  |   |  +-------+  |   |  +-------+  |
  |  | OTel  |  |   |  | OTel  |  |   |  | OTel  |  |
  |  |  API  |  |   |  |  API  |  |   |  |  API  |  |
  |  +---+---+  |   |  +---+---+  |   |  +---+---+  |
  +------+------+   +------+------+   +------+------+
         |  OTLP (gRPC 4317 / HTTP 4318) |
         v                                v
   +----------------------------------------------+
   |       OpenTelemetry Collector (Agent)        |
   |   Receivers -> Processors -> Exporters          |
   |   - Batch / MemoryLimit / TailSampling        |
   |   - Filter / Attributes / Transform          |
   +--------------+-------------------------------+
                  |  OTLP / Prometheus / Kafka
       +----------+----------+
       v          v          v
  +--------+ +--------+ +---------+
  | Jaeger | |Tempo   | |Datadog  |
  |(OSS)   | |(Grafana)| |(SaaS)   |
  +--------+ +--------+ +---------+
   -> Backend 변경 = Exporter 설정 변경만 필요
```

기존 패러다임(코드 + 백엔드 강결합)에서 **관측 가능성 4대 신호(Metrics·Traces·Logs·Baggage)의 통합** 패러다임으로 전환되었으며, 2023년 1.0 GA 이후 Baggage·Profiles·eBPF Profiler까지 표준 신호로 확장되고 있다.

- **📢 섹션 요약 비유**: 기존엔 택배마다 다른 운송장 봉투(Jaeger, Zipkin 봉투)를 써야 했다면, OpenTelemetry는 **ISO 국제 표준 운송장 봉투** 하나로 UPS·FedEx·CJ대한통운 어디로든 보낼 수 있게 해주는 **국제 물류 표준**과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

OpenTelemetry는 크게 **4계층 아키텍처**로 구성된다. ①**API 계층**(어플리케이션 코드와 상호작용하는 추상화), ②**SDK 계층**(구현체, 샘플링/배치/리소스 처리), ③**데이터 계층**(OTLP 및 W3C Trace Context), ④**Collector 계층**(수집·가공·라우팅 파이프라인).

```text
[OpenTelemetry 4-Layer Architecture 상세]
================================================================
  Application Code (Java/Python/Go/...)
     |  imports opentelemetry-api
     v
+------------------------------------------------------------+
|  ① API Layer (의존성: API만, 가벼움 ~2MB)                  |
|   - TracerProvider / MeterProvider / LoggerProvider        |
|   - Span, SpanContext, Context, Baggage                     |
|   - Tracer.startSpan() -> Span Builder -> Span 객체 반환     |
+--------------------+---------------------------------------+
                     v
+------------------------------------------------------------+
|  ② SDK Layer (의존성: SDK, 플러그인)                       |
|   - SpanProcessor: SimpleSpanProcessor / BatchSpanProcessor|
|   - Exporter: OTLP, Console, Jaeger, Zipkin, Prometheus    |
|   - Sampler: AlwaysOn/Off, ParentBased, TraceIDRatio,      |
|              TailBased(Collector 단), JaegerRemote          |
|   - Resource: 서비스명, 버전, k8s pod, cloud region 메타   |
+--------------------+---------------------------------------+
                     v
+------------------------------------------------------------+
|  ③ Data Layer (전송 규약)                                  |
|   - OTLP/gRPC (TCP 4317, HTTP/2 + Protobuf)                |
|   - OTLP/HTTP (TCP 4318, JSON or Protobuf, gzip 가능)      |
|   - W3C Trace Context: traceparent (00-{trace_id}-{span_id}|
|                    -{flags}), tracestate (벤더별 추가 정보) |
|   - Baggage: kv pair, 모든 서비스에 전파되는 자유 메타데이터|
+--------------------+---------------------------------------+
                     v
+------------------------------------------------------------+
|  ④ Collector Layer (별도 프로세스/Deployment)               |
|   Receivers -> Processors -> Exporters 3-Stage Pipeline     |
+------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API (Tracer/Meter/Logger)** | 개발자가 코드에서 호출하는 추상 인터페이스 | `tracer.spanBuilder("checkout").startSpan()` 형태로 언어별 관용구(idiomatic) 제공. TraceProvider는 DI/Service Locator로 SDK 구현 주입 |
| **SDK (TracerProvider 등)** | API의 실제 구현. 샘플링·배치·내보내기 정책 결정 | BatchSpanProcessor는 큐(기본 2048 span) + Worker Thread(기본 5) + 스케줄러(기본 5s/512건)로 비동기 처리. `OTEL_BSP_*` 환경변수로 튜닝 |
| **OTLP (OpenTelemetry Protocol)** | SDK↔Collector, Collector↔Backend 간 데이터 전송 | gRPC: 양방향 스트리밍·고효율, HTTP/1.1+protobuf 또는 JSON, **양쪽 모두 `4317(gRPC)`, `4318(HTTP)`** 표준 포트. gRPC Keep-alive 10s, max msg 4MB |
| **W3C Trace Context** | 서비스 간 trace_id/span_id HTTP/gRPC 헤더 전파 표준 | `traceparent` = `version(00) - trace-id(16B) - parent-id(8B) - flags(1B)`. `tracestate`는 벤더별 key=value, 32개 항목 제한 |
| **Collector (otelcol)** | 텔레메트리 파이프라인의 중앙 처리 노드 | **Receivers**(OTLP/Zipkin/Jaeger/Prometheus/Kafka 50+) -> **Processors**(batch/filter/memory_limiter/tail_sampling/transform/k8sattributes) -> **Exporters**(OTLP/Prometheus/Kafka/Splunk/Datadog). YAML로 구성 |
| **Auto-Instrumentation** | 코드 변경 없이 자동 계측 | Java: `-javaagent:opentelemetry-javaagent.jar` JVM Bytecode 위빙. Python: `opentelemetry-instrument` 패키지 + `OTEL_PYTHON_AUTO_*` 환경변수 |
| **Resource & Semantic Conventions** | 신호에 부착되는 서비스/인프라 메타데이터 | `service.name`, `service.version`, `service.namespace`, `k8s.pod.name`, `cloud.region`, `deployment.environment` 등 RFC 규약 |

핵심 메커니즘인 **Context Propagation(컨텍스트 전파)** 은 다음과 같이 동작한다. ①Client 서비스가 `tracer.spanBuilder("GET /orders").setSpanKind(CLIENT).startSpan()` 호출 -> ②SpanContext(trace_id, span_id) 추출 -> ③HTTP 요청 헤더에 `traceparent` 자동 주입(Instrumentation 라이브러리가 OkHttp, RestTemplate, gRPC Channel 등에 후킹) -> ④Server 서비스가 헤더에서 추출해 **Parent Span**으로 설정 -> ⑤DB/Kafka/Redis 호출 시 **Internal Span** 추가 -> ⑥응답 완료 시 Span 종료(Status=OK/ERROR) -> ⑦BatchSpanProcessor가 큐 적재 -> ⑧Exporter가 OTLP로 Collector 전송.

샘플링의 경우 **Head-based Sampling**(SDK 단계에서 trace_id 해시 비율로 결정, 결정적·저비용)은 일반적이며, **Tail-based Sampling**(Collector에서 전체 Trace 수집 후 에러/지연 기준 보존, 정확·고비용)은 비즈니스 KPI 기반 보존이 필요할 때 사용한다. Tail-based는 메모리 사용량이 트래픽에 비례하므로 `loadbalancing.exporter` + 다중 Collector 인스턴스로 부하 분산이 필수다.

- **📢 섹션 요약 비유**: OpenTelemetry는 **국제 우편 시스템**과 같다. ①API는 "편지 쓰기 도구(편지지, 봉투)", ②SDK는 "우체국 직원이 보내는 규칙", ③OTLP는 "국제 우편 규격 봉투(EMS)", ④Collector는 "국제 우편집중국(인천 Hub)", ⑤Exporter는 "각국 배달업체(Jaeger, Datadog 등)"로, 보내는 사람이 봉투만 잘 쓰면 어디든 배송된다.

---

## Ⅲ. 비교 및 연결

| 구분 | **OpenTelemetry(OTel)** | **Zipkin** | **Jaeger** | **Datadog APM** |
| :--- | :--- | :--- | :--- | :--- |
| **계열** | API/SDK/Collector 통합 표준 (CNCF Graduated) | 트레이스 전용 OSS (Twitter 시작, 2012) | 트레이스 전용 OSS (Uber 시작, 2016, CNCF Graduated) | 상용 SaaS 통합 관측 플랫폼 |
| **데이터 모델** | Span(속성 64KB 제한), Event, Link, Status, Resource | Span, Annotation(키/값), Binary Annotation | Span(속성 무제한), Log, Process | Trace, Span, Flame Graph, Continuous Profiler |
| **프로토콜** | OTLP(gRPC/HTTP), Zipkin v2 호환 Receiver | Zipkin v1/v2 JSON/Thrift, OTLP 수신 가능 | jaeger.thrift UDP, OTLP 수신 가능 | Datadog 전용 프로토콜 (Trace Agent -> DogStatsD) |
| **컨텍스트 전파** | W3C Trace Context(표준) + B3 호환 가능 | B3(B3 single/multi/joined header) | B3, W3C 모두 지원 | X-Request-ID, Datadog 헤더 |
| **신호 통합** | Trace + Metric + Log + Baggage + Profile (단일 표준) | Trace만 (Log는 별도) | Trace만 (Log는 ELK 별도) | Trace + Metric + Log + RUM + Security 통합 SaaS |
| **샘플링** | SDK: ParentBased/Ratio, Collector: Tail-based, Adaptive | Per-Span 확률, Adaptive (최근 deprecate) | Remote via Collector, Probabilistic, Tail-based | Head + Intelligent Sampling(에러/지연 자동 보존, 100% 옵션 유료) |
| **백엔드 종속** | **없음 (벤더 중립)** - Collector Exporter로 자유 선택 | Zipkin Server 의존 | Jaeger Query/Cassandra/Elasticsearch 의존 | Datadog SaaS 종속 (Agent + API Key) |
| **운영 비용/도입 난이도** | 중간 (Collector 구성, 샘플링 정책 필요) | 낮음 (단일 바이너리) | 중간 (스토리지 의존) | 낮음 (Agent 설치만) / 단 SaaS 비용 높음 |
| **확장성** | ⭐⭐⭐⭐⭐ (Receiver/Processor/Exporter 플러그인) | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ (SaaS 의존) |
| **적합 시나리오** | 표준 기반 멀티 백엔드, 하이브리드/멀티클라우드, Trace+Metric+Log 상관 | 소규모 단순 환경, Zipkin 기존 보유 시 | 대규모 MSA, k8s 환경 + ES/Cassandra 운영 가능 | 적은 운영 부담 + 통합 SaaS 원할 때 (예산 충분 시) |

OpenTelemetry는 **독자 백엔드가 없으므로** 다음 도구들과 함께 구성된다: ①**Grafana Tempo**(코스트 효율적 Trace 스토리지, Object Storage 백엔드, Loki·Prometheus와 TraceQL로 상관), ②**Elastic Observability**(ELK 기반 통합), ③**Datadog/Splunk/New Relic**(SaaS Exporter 지원, OTLP->벤더 변환), ④**Prometheus + Grafana**(Metric), **Loki**(Log)와 OTel Collector의 [trace.span_id](file:///trace.span_id) 라벨 매핑으로 **3-시그널 상관 분석**이 가능하다.

```text
[3-시그널 상관 분석 아키텍처]
  Service A --OTLP--+
  Service B --OTLP--+
  Service C --OTLP--+---> OTel Collector ---> Tempo(Trace)
                     |              |       ---> Mimir/Prometheus(Metric)
                     |              |       ---> Loki(Log)
                     |              |
                     |              +-- TraceID/spanID로 라벨 주입
                     |
                     +-- Grafana에서 단일 Trace 선택 시
                         동일 trace_id로 Metric·Log 자동 검색/연결
```

- **📢 섹션 요약 비유**: OTel은 **만국 공통 어학 사전**, Zipkin/Jaeger는 **각 나라 사전**, Datadog은 **번역가 고용 서비스**다. 사전(OT
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 403 / 800

<- **이전**: [402. 그라파나 대시보드 시각화 알림](/studynote/13_cloud_architecture/06_exam_summary/402_grafana_dashboard_visualization_alerting/)
**다음**: [404. 예거 분산 추적 서비스 맵 분석](/studynote/13_cloud_architecture/06_exam_summary/404_jaeger_distributed_tracing_service_map/) ->

---
