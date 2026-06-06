---
title: "Jaeger Distributed Tracing Service Map"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Jaeger는 Uber에서 CNCF(Cloud Native Computing Foundation) graduated 프로젝트로 기증한 오픈소스 분산 추적 플랫폼으로, **W3C Trace Context(`traceparent`/`tracestate`)** 및 **OpenTelemetry Protocol(OTLP/gRPC, HTTP/protobuf)** 기반의 **Trace(TraceID로 묶인 Span 집합)** 데이터를 통해 마이크로서비스 간 **Service Map(서비스 그래프, DAG)** 을 자동 구성하고, RED(Request Rate, Error Rate, Duration) 메트릭으로 시각화·분석하는 시스템이다.
> 2. **가치**: Kubernetes/Istio 환경에서 수십~수백 개 서비스로 분리된 시스템에서, 코드 변경 없이도 **서비스 간 호출 토폴로지·병목 지점·에러 전파 경로**를 즉시 파악 가능하며, MTTR(Mean Time To Restore)을 평균 60~80% 단축시키고, **SLO/SLI 기반의 Tail Latency(p99) 관리**를 위한 핵심 신호원으로 작동한다.
> 3. **판단 포인트**: Sampling 전략(Constant/Probabilistic/Adaptive/Tail-based), Storage Backend 선택(Elasticsearch vs Cassandra vs Badger), Collector 배치(Agent sidecar vs DaemonSet vs Sidecar), 그리고 OpenTelemetry SDK 마이그레이이션 여부에 따라 **비용·데이터 충실도·운영 복잡도** 간의 트레이드오프가 결정되며, 특히 **100% 샘플링 남용**은 백엔드 비용 폭증과 성능 저하의 핵심 안티패턴이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 분산 시스템 시대의 관측 가능성(Observability) 위기

MSA(Microservices Architecture)가 보편화되면서 단일 요청이 API Gateway -> BFF(Backend For Frontend) -> User Service -> Order Service -> Payment Service -> DB(Sidecar/Connection Pool) -> Message Broker(Kafka) -> Notification Service 등 **7~15개 이상의 서비스와 비동기 큐를 횡단**하는 것이 일상화되었다. 기존 **모놀리식 환경의 로그 기반 디버깅**(`grep "userId=12345" *.log`)은 다음의 한계에 부딪힌다:

- **시계 비동기성(Clock Skew)**: 컨테이너 간 NTP 동기화 오차(수 ms~수백 ms)로 로그 상관관계 분석이 부정확함
- **컨텍스트 단절**: HTTP Header, gRPC Metadata, Kafka Header, DB SQL의 TraceID가 서비스 경계에서 소실됨
- **인덱싱 폭발**: 매초 수십만 건의 로그를 ELK/Loki에 저장·인덱싱 시 스토리지 비용이 기하급수적 증가
- **비동기 흐름의 사각지대**: Kafka, RabbitMQ, SQS 같은 메시지 큐를 통한 호출은 응답이 분리되어 토폴로지 복원이 불가

Google은 2010년 논문 *"Dapper, a Large-Scale Distributed Systems Tracing Infrastructure"*에서 **분산 추적(Distributed Tracing)** 의 원형을 제시했고, 이를 계기로 Zipkin(Twitter, 2012), Jaeger(Uber, 2015, 2017 OSS 공개, 2019 CNCF Incubating -> 2022 Graduated), 그리고 OpenCensus(Google)·OpenTracing(CNCF, 표준 API)이 등장했다. 현재는 이 둘이 통합된 **OpenTelemetry(2021 GA, 2024 v1.30+ 안정화)** 가 사실상 업계 표준이다.

### 1.2 서비스 맵(Service Map)이란?

Jaeger UI의 **System Architecture / DAG 탭**에서 확인할 수 있는 서비스 맵은, 실제 런타임 트래픽의 Span 데이터를 집계하여 **자동으로 그려지는 방향성 비순환 그래프(DAG, Directed Acyclic Graph)** 다. 단순히 인프라 토폴로지를 그리는 것이 아니라 다음을 포함한다:

```
+----------------------------------------------------------------------+
|                    Jaeger Service Map (DAG) Sample                   |
|                                                                      |
|   +---------+  320rps/12ms  +------+  280rps/45ms  +----------+     |
|   | frontend+--------------►|  bff +--------------►| order-svc|     |
|   |   ● 0%  |               | ● 0% |               |  ● 0%    |     |
|   +----+----+               +---+--+               +----+-----+     |
|        | 80rps/8ms               | 280rps/15ms           | 250rps    |
|        v                         v                        v          |
|   +---------+               +--------+              +----------+    |
|   |auth-svc |               |cart-svc|              |  kafka   |    |
|   |  ● 0%   |               | ● 0%   |              | (order)  |    |
|   +----+----+               +---+----+              +----+-----+    |
|        | 80rps/3ms              | 280rps/12ms             |          |
|        v                        v                         v          |
|   +----------+            +----------+              +----------+    |
|   | postgres |            |  redis   |              |payment-svc|    |
|   |  (auth)  |            |  (cart)  |              |  ● 2.1%   |    |
|   +----------+            +----------+              +-----+----+    |
|                                                            |         |
|   ● = Error Rate (서비스 노드 색상/배지로 시각화)          v         |
|                                                  +----------+       |
|                                                  |pg(Billing)|       |
|                                                  +----------+       |
|                                                                      |
|   Edge Label: {request_rate} rps / {p95_latency} ms / {error_rate}% |
+----------------------------------------------------------------------+
```

각 **노드(서비스)** 와 **엣지(서비스 간 의존성)** 에는 다음 메트릭이 표시된다:
- **Request Rate (RPS)**: 단위 시간당 해당 노드/엣지를 통과한 Span 수
- **Error Rate (%)**: HTTP 5xx, gRPC status != OK, 명시적 `error=true` 태그 비율
- **Latency (p50/p95/p99)**: 서비스 내 처리 시간 분포

### 1.3 전통적 모니터링과의 결정적 차이

| 차원 | 전통 모니터링 (Nagios/Zabbix/Prometheus) | Jaeger 분산 추적 |
| :--- | :--- | :--- |
| **관측 단위** | 호스트/컨테이너 단위 CPU, Memory, Disk | **요청(Request) 단위**의 인과 추적 |
| **상관관계** | 정적 라벨(Label) 기반 수동 집계 | **TraceID 자동 전파**로 인과 그래프 구성 |
| **비동기 처리** | 큐 깊이(Queue Depth)만 확인 가능 | **Producer/Consumer Span Link**로 전체 흐름 추적 |
| **근본 원인 분석** | 메트릭 이상 -> 로그 검색 -> 수동 추론 | **Flame Graph, Critical Path**로 즉시 식별 |
| **자동 토폴로지** | CMDB(설정관리DB) 수동 관리 | **실제 트래픽 기반 자동 Service Map** 갱신 |

- **📢 섹션 요약 비유**: 기존 모니터링이 병원 종합검진의 **혈당·혈압·콜레스테롤 수치** 같은 정적 지표라면, Jaeger 서비스 맵은 **순간 CT/MRI 영상**과 같다. 환자가 "가슴이 아프다"고 말할 때, 종합검진 수치만으로는 심근경색인지 협심증인지 알 수 없지만, CT 영상은 혈관 폐색 위치를 **픽셀 단위로 즉시** 보여준다. Jaeger의 TraceID는 이 영상에서 환자의 **혈관을 따라 카테터가 다니는 경로(Contrast Agent)** 와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Jaeger 플랫폼 전체 아키텍처

```text
+--------------------------------------------------------------------------+
|                    Jaeger Platform Architecture (v1.55+)                 |
|                                                                          |
|  +--------------------------------------------------------------------+  |
|  |                      Application Services                         |  |
|  |  +--------------+  +--------------+  +--------------+            |  |
|  |  |  order-svc   |  | payment-svc  |  |  user-svc    |            |  |
|  |  | +----------+ |  | +----------+ |  | +----------+ |            |  |
|  |  | | OTel SDK | |  | | OTel SDK | |  | | OTel SDK | |            |  |
|  |  | |  (Java/  | |  | | (Go/Py)  | |  | | (Node)   | |            |  |
|  |  | |   .NET)  | |  | |          | |  | |          | |            |  |
|  |  | +----+-----+ |  | +----+-----+ |  | +----+-----+ |            |  |
|  |  +------+--------+  +------+--------+  +------+--------+            |  |
|  +---------+-----------------+-----------------+---------------------+  |
|            | OTLP/gRPC :4317  |                 |                         |
|            | OTLP/HTTP :4318  |                 |                         |
|            v                  v                 v                         |
|  +--------------------------------------------------------------------+  |
|  |  Jaeger Agent (DaemonSet on K8s, UDP :6831/UDP :6832/HTTP :14271)  |  |
|  |  • UDP 버퍼링 & 배치 전송 (Batch Size 100, Flush 5s)              |  |
|  |  • Host 정보를 Process 태그로 주입 (pod_name, node_ip)             |  |
|  |  • Application -> Agent 간 gzip 압축으로 네트워크 대역폭 절감       |  |
|  +----------------------------+---------------------------------------+  |
|                               |                                         |
|                               v                                         |
|  +--------------------------------------------------------------------+  |
|  |                  Jaeger Collector (Stateless)                      |  |
|  |  +--------------+    +--------------+    +--------------+         |  |
|  |  | Ingester     |---►|Tail-Based    |---►|   Writer     |         |  |
|  |  | (Thrift/     |    |Sampler       |    |  (Batcher)   |         |  |
|  |  |  ProtoBuf    |    |(Probabilistic|    |              |         |  |
|  |  |  파싱/검증)  |    | + Latency    |    |              |         |  |
|  |  |              |    | + Error 룰)  |    |              |         |  |
|  |  +--------------+    +--------------+    +------+-------+         |  |
|  |                                                  |                  |  |
|  |  +--------------------------------------+        |                  |  |
|  |  |  Sampling Strategy Service            |        |                  |  |
|  |  |  (Client가 주기적 polling, REST :5778)|        |                  |  |
|  |  +--------------------------------------+        |                  |  |
|  +--------------------------------------------------+------------------+  |
|                                                     |                   |
|                          +--------------------------+--------------+    |
|                          |                          v              v    |
|                          |   +----------+    +----------+   +--------+ |
|                          |   |  Kafka   |---►|  ES /    |   |  Badger| |
|                          |   |(Buffer)  |    |Cassandra |   | (Embed)| |
|                          |   +----------+    +----------+   +--------+ |
|                          |                       ^                     |
|                          +-----------------------+---------------------+
|                                                  |
|  +-----------------------------------------------+----------------------+
|  |                   Jaeger Query                |                      |
|  |   +--------------+    +--------------+        |                      |
|  |   |  Query Svc   |◄--►|  Storage     |◄-------+                      |
|  |   |  (gRPC :16685)|    |  Backend     |                                |
|  |   |  (HTTP :16686)|    |  Reader      |                                |
|  |   +-------+------+    +--------------+                                |
|  |           |                                                           |
|  |           v                                                           |
|  |   +------------------------------+                                    |
|  |   |  Jaeger UI (React, SPA)      |                                    |
|  |   |  • Service Map / DAG         |                                    |
|  |   |  • Trace Search & Timeline   |                                    |
|  |   |  • Span Detail / JSON View   |                                    |
|  |   |  • Compare Traces            |                                    |
|  |   |  • System Metrics (Sparkline)|                                    |
|  |   +------------------------------+                                    |
|  +----------------------------------------------------------------------+
+--------------------------------------------------------------------------+
```

### 2.2 핵심 데이터 모델: Trace, Span, SpanContext

Jaeger는 **OpenTracing v1.1 API**(현재는 OpenTelemetry API로 이행)를 구현하며, 데이터 모델은 다음과 같다:

#### 2.2.1 Span의 구조

```text
Span {
  +-----------------------------------------------------------------+
  | TraceID
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 404 / 800

<- **이전**: [403. 오픈텔레메트리 분산 추적 표준 수집](/studynote/13_cloud_architecture/06_exam_summary/403_opentelemetry_distributed_tracing_standard/)
**다음**: [405. 로키 로그 수집 쿼리 경량 스택](/studynote/13_cloud_architecture/06_exam_summary/405_loki_log_collection_query_lightweight_stack/) ->

---
