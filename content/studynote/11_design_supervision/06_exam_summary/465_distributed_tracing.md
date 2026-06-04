---
title: "465. 분산 추적 상관 관계 ID 패턴 (Distributed Tracing Correlation ID Pattern)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 마이크로서비스·멀티티어 환경에서 단일 사용자 요청이 수십~수백 노드를 거치며 발생하는 로그·메트릭·트레이스를 **W3C Trace Context(`traceparent`, `tracestate`)와 OpenTelemetry SDK** 기반으로 **Trace ID(128-bit) -> Span ID(64-bit) -> Parent Span ID** 계층으로 전파(Propagation)하여, 컨텍스트 손실 없이 종단간(End-to-End) 인과 관계를 재구성하는 분산 관측(Observability) 핵심 패턴.
> 2. **가치**: 평균 검출 시간(MTTD) **60%v**, 근본 원인 분석(MTTR) **40~70%v**, 컨테이너·서버리스·메시지 큐 환경에서의 **"Lost Trace" 0%에 근접**, OpenTelemetry 표준 채택으로 벤더 종속 제거 -> Zipkin, Jaeger, Tempo, Datadog APM, AWS X-Ray, Honeycomb 등 백엔드 자유 교체 가능.
> 3. **판단 포인트**: ① `traceparent` 32byte 헤더 오버헤드 vs. 디버깅 ROI 트레이드오프, ② 샘플링 전략(Head-based/Tail-based/Adaptive)의 비용-정확도 균형, ③ **비동기 메시지 브로커(Kafka, RabbitMQ) 전파 시 헤더 주입 위치**(Producer/Consumer/Both), ④ PII·인증 토큰 같은 민감정보의 태그 스팬 오염 방지, ⑤ 128-bit ID 충돌 확률(2⁻¹²²)의 실질적 무시 가능성 검증.

---

## Ⅰ. 개요 및 필요성

**모놀리식 -> 마이크로서비스·멀티클라우드 전환**으로 단일 HTTP 요청이 게이트웨이 -> 인증 서비스 -> 오더 서비스 -> 결제 서비스 -> Kafka -> 재고 서비스 -> 알림 서비스로 흐를 때, **로그가 분산된 N개 저장소**에 흩어져 "왜 결제는 성공했는데 주문이 실패했는가?"를 추적하기 어려워졌다. 전통적인 `MDC`(Mapped Diagnostic Context)나 `ThreadLocal` 기반 `RequestId`는 **스레드 경계를 넘는 순간**(HTTP 클라이언트 풀, `CompletableFuture`, `Reactor`, Kafka Producer/Consumer, gRPC 스트림) 컨텍스트가 **자동 소실**되며, 특히 **메시지 큐의 비동기 처리**는 요청-응답 시간적 인과성을 분리시켜 "어느 요청이 이 큐 메시지를 만들었는가"의 연결 고리가 완전히 끊어진다.

**분산 추적 상관 관계 ID 패턴(Distributed Tracing Correlation ID Pattern)**은 모든 서비스가 공통 ID를 HTTP/gRPC/Kafka 헤더에 주입·전파하여, **타임라인 뷰(Waterfall View)**와 **의존성 그래프(Service Map)**를 자동 생성하고, 이상 트랜잭션에 대해 컨텍스트가 보존된 로그(Structured Logging)와 메트릭(RED/USE)을 결합한다. W3C Trace Context 표준(`traceparent: 00-{trace-id}-{span-id}-{flags}`)과 W3C Baggage(`baggage: userId=alice,tenant=acme`)로 벤더 중립성을 확보했고, OpenTelemetry Collector가 OTLP(OpenTelemetry Protocol, gRPC/HTTP) 수신 후 Jaeger·Tempo·Datadog로 라우팅한다.

```text
   [Client: Mobile App]    trace_id=8a3c...d1, span_id=aaaa (Root)
        |
        |  HTTP POST /order  (traceparent: 00-8a3c...d1-aaaa-01)
        v
   +--------------+
   | API Gateway  | span_id=bbbb, parent=aaaa   --►  Baggage: userId=42
   +------+-------+
          |
          +-- HTTP --► [Auth Service]    span=cccc, parent=bbbb
          |                              SpanEvent: jwt.verified=true
          |
          +-- gRPC --► [Order Service]   span=dddd, parent=bbbb
          |            |
          |            +-- Kafka Produce  Headers: traceparent=00-...-dddd-01
          |            |                  baggage: tenant=acme
          |            v
          |         [Kafka Topic: order.created]
          |            |
          |            | (수 분~수 시간 후)
          |            v
          |         [Inventory Svc Consumer]  span=eeee, parent=dddd
          |                                     Context.restore(headers)
          |
          +-- HTTP --► [Payment Service] span=ffff, parent=bbbb
                       |   SpanAttribute: payment.method=card
                       v
                  [External PSP]         span=gggg, parent=ffff
                                          db.system=postgresql
                  ------------------------------------------------
                  모든 Span이 trace_id=8a3c...d1로 연결 -> Waterfall View
```

**기존 방식과의 결정적 차이**: 전통 `RequestId`는 단일 동기 흐름에만 유효하며, **fire-and-forget 메시지**나 **cron 배치**처럼 "원인 요청"이 없는 케이스에서는 깨진다. 분산 추적은 Span 간 **인과 그래프(Causal DAG)**를 SpanLink·SpanEvent로 모델링하고, **Propagation Injector/Extractor** 추상화로 모든 통신 매체(HTTP, gRPC, Kafka, RabbitMQ, Redis Streams, SQS, NATS, MQTT, DB SQL Comment)를 통합한다. Gartner는 2026년 신규 클라우드 네이티브 프로젝트의 **85% 이상이 OpenTelemetry 기반 관측을 채택**할 것으로 전망(2023 보고서)하며, **CNCF Incubating -> Graduated(2025-09)** 단계의 OpenTelemetry는 사실상 디팩토 표준이다.

- **📢 섹션 요약 비유**: 비유: 흩어진 우편물을 다시 모으기. 손자(앱)가 보낸 택배(요청)가 각 집하장(서비스)을 거치며 **송장 번호(Trace ID)**가 분실되지 않고 5개 물류센터를 지나도록, 발송인(Order Svc)이 송장 복사본을 택배 박스(Kafka 메시지 헤더) 안쪽에 동봉해 도착지(Inventory Svc) 직원이 다시 붙여 일렬로 추적하는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

**OpenTelemetry W3C Trace Context** 명세의 4가지 핵심 구성요소가 동작한다: ① **Trace ID**(16 bytes, 32 hex chars) – 트랜잭션의 글로벌 식별자, ② **Span ID**(8 bytes, 16 hex chars) – 개별 작업 단위, ③ **Parent Span ID** – 인과 관계 링크, ④ **Trace Flags**(sampled, random) – 8비트 컨트롤 플래그. **`00-8a3c60f0d1f2a3b4c5d6e7f8a9b0c1d2-aaaa0bbbbbbbbbbb-01`** 형식의 `traceparent` 헤더 한 줄로 전파되며, gRPC metadata, Kafka header, AMQP properties, Redis Stream XADD field로 **carrier-agnostic**하게 직렬화된다.

**Instrumentation**은 ① **Auto-Instrumentation**(Java Agent `-javaagent:opentelemetry-javaagent.jar`, Node.js `--require @opentelemetry/auto-instrumentations-node`, Python `opentelemetry-instrument`, Go `otelhttp` 미들웨어) – 코드 수정 없이 OpenTelemetry SDK가 클래스 로더 위빙으로 HTTP/gRPC/JDBC 호출을 자동 계측, ② **Manual Instrumentation** – `tracer.spanBuilder("checkout").setParent(context).startSpan()`로 비즈니스 도메인 스팬(`db.query.users`, `cache.lookup`, `business.calculateTax`) 명시, ③ **eBPF 기반 Zero-Code** – Cilium Tetragon, Pixie(flamegraph 자동 생성), Beyla가 커널 레벨에서 syscall·소켓을 후킹해 언어 무관 계측. **Context Propagation**은 OpenTelemetry Context API가 `TextMapPropagator`(W3C Trace Context + Baggage), `JaegerPropagator`(하위호환), `B3Propagator`(Zipkin 형식, `X-B3-TraceId`), `AWSXRayPropagator`를 플러그인 방식으로 지원한다.

**샘플링(Sampling)**은 트래픽 폭증 시 비용 통제의 핵심이다. ① **Head-based Sampling** – 루트 스팬에서 비율 결정(`ParentBased(TraceIdRatioBased(0.1))`로 10%만 샘플링), 장점: 결정성, 단점: **에러 트랜잭션을 놓칠 수 있음**, ② **Tail-based Sampling** – OpenTelemetry Collector의 `tail_sampling_processor`가 N초 윈도우로 모든 스팬을 메모리에 버퍼링 후 **에러·지연시간·특정 태그 기준**으로 보존(`policy { name: errors, type: status_code }`), 장점: 100% 에러 캡처, 단점: **Collector 메모리 압박**(10k span/sec × 10s = 100k span), ③ **Adaptive Sampling** – 서비스 에러율·p99 latency를 실시간 모니터링하며 샘플링 비율 동적 조정(예: 정상 시 1%, 장애 시 100%). **Span Attributes**는 `semantic conventions`로 표준화: `http.method=POST`, `http.status_code=500`, `http.route=/orders/:id`, `db.system=postgresql`, `db.statement="SELECT * FROM users WHERE id=$1"`, `messaging.system=kafka`, `messaging.destination=order.created`, `messaging.kafka.partition=3`, `messaging.kafka.offset=12345`.

```text
                    +--------------------------------------------+
                    |      OpenTelemetry SDK (Application)        |
                    |  +----------+   +----------+  +----------+  |
                    |  | Tracer   |   | Logger   |  | Meter    |  |
                    |  | Provider |   | Provider |  | Provider |  |
                    |  +----+-----+   +----+-----+  +----+-----+  |
                    |       |              |             |        |
                    |       v              v             v        |
                    |  +-------------------------------------+    |
                    |  |   Context (Trace ID, Span ID,       |    |
                    |  |          Baggage)                   |    |
                    |  +--------------+----------------------+    |
                    +-----------------+---------------------------+
                                      | OTLP/gRPC (4317) or HTTP (4318)
                                      v
                    +---------------------------------------------+
                    |   OpenTelemetry Collector (Deployment)      |
                    |  +---------+ +---------+ +--------------+  |
                    |  |Receivers|->|Processors|->|  Exporters   |  |
                    |  |otlp/    | |batch    | |otlp/jaeger   |  |
                    |  |zipkin/  | |tail     | |otlp/tempo    |  |
                    |  |jaeger   | |sampling | |prometheus    |  |
                    |  +---------+ |memory   | |kafka/clickh. |  |
                    |              |limiter  | +--------------+  |
                    |              +---------+                   |
                    +------------------+--------------------------+
                                       |
              +------------------------+------------------------+
              v                        v                        v
     +--------------+         +--------------+         +--------------+
     |   Jaeger     |         |   Tempo      |         |   Datadog    |
     |  (Storage:   |         |  (Storage:   |         |  (Storage:   |
     |   ES/Cass)   |         |   S3+GCS)    |         |  proprietary)|
     +------+-------+         +------+-------+         +------+-------+
            |                        |                        |
            v                        v                        v
       Waterfall UI            Grafana 연동               Service Map
       Service Graph           TraceQL 검색              Watchdog AI
       Dependencies            Trace Exemplar            Error Tracking
```

**핵심 전파 메커니즘 (Java/Pseudo)**: `RestTemplate` 호출 시 `RestClientHttpRequestInterceptor`가 `Context.current()`에서 `traceparent`를 추출해 `HttpHeaders`에 주입, 응답 수신 후 컨텍스트 클린업. Kafka에서는 `TextMapPropagator.inject()`가 `ProducerRecord.headers().add("traceparent", value)`로 직렬화, Consumer는 `KafkaHeaders`에서 추출해 `Context.makeCurrent()`. **순서 보장이 필요한 점**: Consumer는 `TraceContextOrSamplingFlags.extract()` -> `Span.wrap()` -> `tracer.spanBuilder("kafka.process").setParent(extracted).startSpan()` -> `try(Scope s = span.makeCurrent()) { businessLogic() }`로 **반드시 try-with-resources**로 스팬 종료 보장.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Trace Context** | 트랜잭션 전역 ID 컨테이너 | W3C Trace Context(`traceparent`, `tracestate`), 128-bit Trace ID, 64-bit Span ID, 8-bit Flags (`01`=sampled, `00`=not sampled) |
| **Propagator** | 매체 간 컨텍스트 직렬화·역직렬화 | `TextMapPropagator` 인터페이스, `W3CTraceContextPropagator`, `JaegerPropagator`(하위호환), `B3Propagator`(Zipkin), `CompositePropagator`(다중 포맷 동시) |
| **Span / SpanContext** | 작업 단위 + 인과 링크 메타데이터 | `Span` API(`setAttribute`, `addEvent`, `setStatus(ERROR)`, `recordException`), `SpanContext`(`traceId`, `spanId`, `isRemote`, `traceFlags`, `traceState`) |
| **TracerProvider / Exporter** | SDK 라이프사이클, OTLP 송신 | `SdkTracerProvider.builder().addSpanProcessor(BatchSpanProcessor.builder(OtlpGrpcSpanExporter.builder().setEndpoint("http://otel-collector:4317").build()).build()).build()`, 메모리/배치/실시간 모드 |
| **OpenTelemetry Collector** | 중앙 수집·처리·라우팅 파이프라인 | Receiver(`otlp`, `zipkin`, `jaeger`, `kafka`) -> Processor(`batch`, `tail_sampling`, `memory_limiter`, `attributes/insert`, `resource/detect`, `filter`, `probabilistic_sampler`) -> Exporter(`otlp`, `prometheus`, `kafka`, `s3`, `clickhouse`, `elasticsearch`) |
| **백엔드 저장소** | 트레이스 영속화·검색·시각화 | Jaeger(Cassandra/Elasticsearch), Grafana Tempo(S3+GCS, TraceQL), Datadog APM, Honeycomb(고차원 검색), New Relic, Lightstep, AWS X-Ray |
| **Context Baggage** | 비-관측 메타데이터 키-값 전파 | `W3CBaggagePropagator`, `baggage: userId=42,tenant=acme,sessionId=xyz`, 다운스트림 서비스가 `Baggage.current().getEntryValue("tenant")`로 사용, **크기 제한 4096 chars** |

**SpanKind와 인과 모델**: `SpanKind`는 6종류 – `SERVER`/`CLIENT`(HTTP·gRPC), `PRODUCER`/`CONSUMER`(메시지), `INTERNAL`(내부 함수), `CLIENT`(`db.client.operation=SELECT`). **Span Link**는 `addLink(spanContext, attrs)`로 다중 트레이스 연결(예: SAGA 보상 트랜잭션, 배치 작업에서 1000개 사용자 트레이스 모두 링크). **TraceState**(`tracestate: vendor1=abc,vendor2=xyz`)는 벤더별 라우팅 정보로, **첫 256자**가 표준 한계이며 `key=value` 쌍은 32개까지.

- **📢 섹션 요약 비유**: 비유: 병원 진료 기록의 통합 차트. A의원이 발급한 차트 번호(Trace ID)가 X-ray, MRI, 혈액검사 스티커(Span ID)에 부모-자식 관계로 인쇄되어 B의원이 모르는 환자의 이전 검사를 즉시 이어볼 수 있게 한다. 양식(propagator)은 표준 A4지만, 헤더의 부모 ID 덕에 의사가 한눈에 인과 흐름
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 465 / 600

<- **이전**: [464. 데이터베이스 퍼 서비스 독립 저장소](/studynote/11_design_supervision/06_exam_summary/465_database_per_service/)
**다음**: [466. 컨슈머 주도 계약 테스트](/studynote/11_design_supervision/06_exam_summary/466_consumer_driven_contract/) ->

---
