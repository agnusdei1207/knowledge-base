---
title: "586. 서비스 메시 관측성 트래픽 제어 (Service Mesh Observability Traffic Control)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 서비스 메시 관측성 트래픽 제어는 Envoy/Linkerd2-proxy 같은 L4/L7 프록시를 사이드카(또는 ztunnel)로 주입하여 데이터 플레인에서 모든 요청의 mTLS 암호화·카나리 라우팅·서킷브레이커를 적용하고, xDS API(LDS/RDS/CDS/EDS/SDS)로 제어 평면이 이를 동적 구성하며, RED/USE 메트릭·W3C TraceContext 분산 트레이싱·JSON 액세스 로그를 OpenTelemetry/Prometheus/Jaeger 파이프라인으로 노출하는 관측가능성-제어 통합 패턴이다.
> 2. **가치**: 제로트러스트 보안(STRICT mTLS)·세밀한 카나리(트래픽 1% 단위 분할)·자동 장애격리(consecutive 5xx 기반 outlier detection)를 코드 변경 없이 YAML 한 줄로 적용할 수 있으며, 평균 MTTR을 약 60% 단축하고, SLO 기반 카나리 분석(예: p99 latency 200ms 이하)을 자동화한다.
> 3. **판단 포인트**: Sidecar 방식(Istio classic)은 mTLS/L7 풍부함과 메모리·CPU 오버헤드(파드당 약 50~100MB, p99 latency +1~3ms) 트레이드오프가 있으며, eBPF 기반 Cilium/Ambient Mesh는 오버헤드를 줄이지만 L7 트래픽 분할 기능이 제한적이므로, 트래픽 패턴(L7 비율), 노드 밀도, SRE 성숙도, 규제 컴플라이언스(PCI-DSS, K-ISMS-P) 요건에 따라 사이드카/앰비언트/eBPF 모드를 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

마이크로서비스 아키텍처(MSA)가 50~500개 단위로 확장되면 서비스 간 호출 그래프가 폭발적으로 증가하고, "어떤 호출이 실패했는지", "왜 느려졌는지", "어디서 보안을 보장할지"라는 세 가지 질문에 답하기 어려워진다. 이를 "관측가능성 3요소(Three Pillars)"인 Metrics·Logs·Traces로 해소하고, 동시에 "트래픽 제어로 안정성을 확보"하려는 요구가 등장하면서 **서비스 메시(Service Mesh)** 가 MSA 인프라의 표준 계층으로 자리 잡았다.

전통적인 방식에서 분산 추적은 애플리케이션 SDK(Hystrix, Resilience4j, Spring Cloud Sleuth 등)에 의존했으나, polyglot 환경(Java·Go·Node·Python·Rust)마다 SDK를 삽입해야 하고, Retry·Circuit Breaker·mTLS·Rate Limit 로직이 비즈니스 코드와 강결합되어 유지보수 비용이 기하급수적으로 증가했다. **사이드카 패턴(Sidecar Pattern)** 을 도입하면, 애플리케이션은 비즈니스 로직만 담당하고 모든 횡단 관심사(Cross-Cutting Concerns)를 Envoy 같은 L4/L7 프록시로 위임할 수 있다. 이때 사이드카에서 발생하는 모든 요청의 메트릭·로그·트레이스가 자동으로 수집되므로 **관측가능성과 트래픽 제어가 단일 데이터 플레인에서 통합** 된다.

```text
+-------------------------------------------------------------------------+
|                    Service Mesh: Control Plane + Data Plane              |
|                                                                         |
|  +--------------- Control Plane (istiod / Linkerd Control / Consul) ---+|
|  |  +------------+  +------------+  +--------------+  +--------------+ ||
|  |  | Pilot /    |  | Citadel /  |  | Galley /     |  | Mixer / OPA  | ||
|  |  | xDS Push   |  | SDS (Cert) |  | Config Valid |  | Policy(Tel)  | ||
|  |  +-----+------+  +-----+------+  +------+-------+  +------+-------+ ||
|  +--------+---------------+----------------+-----------------+--------+|
|           | xDS(gRPC)     | mTLS Cert     | CRD Validation  |         |
|           | LDS/RDS/CDS/  | Rotation      |                 |         |
|           | EDS/SDS       | (24h default) |                 |         |
|  +--------v---------------v----------------v-----------------v--------+|
|  |                   Kubernetes Data Plane (Pod per Node)            ||
|  |                                                                    ||
|  |  +--------------------------+    +--------------------------+      ||
|  |  | Pod: order-service       |    | Pod: payment-service     |      ||
|  |  |  +--------+  +--------+  |    |  +--------+  +--------+  |      ||
|  |  |  |  App   |--| Envoy  |--+----+-->| Envoy  |<--|  App   |  |      ||
|  |  |  |  JVM   |  |:15001  |  |    |  |:15001  |  |  JVM   |  |      ||
|  |  |  | :8080  |  |:15006  |  |    |  |:15006  |  | :8080  |  |      ||
|  |  |  +--------+  +---+----+  |    |  +--------+  +--------+  |      ||
|  |  |   iptables       |       |    |                            |      ||
|  |  |  REDIRECT        |       |    |                            |      ||
|  |  +------------------+-------+    +----------------------------+      ||
|  |                     |  mTLS(Envoy-to-Envoy)                          ||
|  |                     v                                                ||
|  |            +-----------------+                                       ||
|  |            |   observability |  -> Prometheus scrape(15s)              ||
|  |            |   Stack         |  -> Jaeger/Tempo(OTLP)                  ||
|  |            +-----------------+  -> Loki(access log JSON)               ||
|  +----------------------------------------------------------------------+|
+-------------------------------------------------------------------------+
```

기존 SDK 임베디드 방식과 비교한 패러다임 전환의 핵심은 **(1) 언어 중립성**, **(2) 제로트러스트 보안의 자동화**, **(3) declarative 트래픽 제어** 세 가지다. Kubernetes CRD(Custom Resource Definition)로 VirtualService, DestinationRule, ServiceEntry, PeerAuthentication 같은 선언적 API를 작성하면, 제어 평면이 이를 xDS 프로토콜로 변환해 모든 Envoy에 push하고, 데이터 플레인은 코드 변경·재배포 없이 트래픽 비율·재시도·서킷 정책·mTLS 모드를 즉시 반영한다.

- **📢 섹션 요약 비유**: 아파트의 각 세대(마이크로서비스) 안에 택배 분류기·CCTV·출입통제 시스템을 일일이 설치하는 대신, 단지 정문과 각 동 입구(사이드카 프록시)에 통합 관제 시스템을 두는 것과 같다. 택배 분배(트래픽 라우팅), 방문객 신원확인(mTLS), 차량 진입 기록(액세스 로그)이 중앙 관제실에서 모두 통합되어 처리된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

서비스 메시의 아키텍처는 크게 **제어 평면(Control Plane)** 과 **데이터 평면(Data Plane)** 으로 분리된다. 데이터 평면은 L4/L7 프록시(Envoy, Linkerd2-proxy, eBPF/cilium-agent)의 집합체이고, 제어 평면은 정책·설정·인증서를 데이터 평면에 분배하는 두뇌 역할을 한다. 핵심 통신 채널은 **xDS(gRPC streaming) 프로토콜** 이다.

```text
+-----------------------------------------------------------------------+
|            Envoy xDS Push Flow & Observability Data Path              |
|                                                                       |
|  +-------------- istiod (Control Plane) --------------------------+  |
|  |                                                                 |  |
|  |  K8s API <---- watch --- VirtualService / DestinationRule        |  |
|  |     |                          |                                 |  |
|  |     |                  +-------v--------+                        |  |
|  |     |                  | Config Builder |                        |  |
|  |     |                  | (Pilot)        |                        |  |
|  |     |                  +-------+--------+                        |  |
|  |     |                          | xDS gRPC stream                 |  |
|  |     |   +----------------------+--------------------------+     |  |
|  |     |   | LDS  (Listener)     |  :15001 inbound           |     |  |
|  |     |   | RDS  (Route)        |  VirtualHost per host     |     |  |
|  |     |   | CDS  (Cluster)      |  service.cluster.local    |     |  |
|  |     |   | EDS  (Endpoint)     |  10.4.1.12,10.4.1.13,..   |     |  |
|  |     |   | SDS  (Secret/Cert)  |  workload cert, root cert |     |  |
|  |     +---|--------------------------------------------------+     |  |
|  +---------+---------------------------------------------------------+  |
|            |  ADS (Aggregated Discovery Service)                       |
|            v                                                            |
|  +--------------- Envoy Sidecar (Per Pod) ------------------------+  |
|  |  Listener :15006 (outbound)                                     |  |
|  |  |  +-------- Filter Chain: HTTP/gRPC ---------+                |  |
|  |  |  | 1) RBAC filter -> 2) JWT -> 3) ext_authz  |                |  |
|  |  |  | 4) Lua/WASM -> 5) Router (RouteConfig)   |                |  |
|  |  |  | 6) Retry Policy -> 7) Timeout             |                |  |
|  |  |  | 8) Circuit Breaker -> 9) Load Balancer    |                |  |
|  |  |  |   (Maglev/RingHash/LEAST_CONN)           |                |  |
|  |  |  | 10) TCP/TLS termination -> upstream cluster|                |  |
|  |  |  +-------------------------------------------+                |  |
|  |  |                                                              |  |
|  |  |  +----- Telemetry (StatsD/Prom/OTel) -----+                  |  |
|  |  |  | • istio_requests_total                  |                  |  |
|  |  |  | • istio_request_duration_milliseconds_bucket |            |  |
|  |  |  | • istio_request_bytes, response_bytes   |                  |  |
|  |  |  | • tcp_*_sent, tcp_*_received            |                  |  |
|  |  |  +-----------------------------------------+                  |  |
|  |  |  +----- Access Log (stdout JSON) --------+                   |  |
|  |  |  | { "protocol":"HTTP/2", "upstream":..   |                   |  |
|  |  |  |   "method":"POST","status":200,        |                   |  |
|  |  |  |   "duration_ms":42, "trace_id":"abc", |                   |  |
|  |  |  |   "x_forwarded_for":"10.4.2.1" }      |                   |  |
|  |  |  +----------------------------------------+                   |  |
|  |  |  +----- Tracing (W3C traceparent) ------+                    |  |
|  |  |  | 00-aaa-bbb-01 propagated -> OTLP ->     |                    |  |
|  |  |  | Jaeger/Tempo/Telemetry Collector       |                    |  |
|  |  |  +---------------------------------------+                    |  |
|  |  +--------------------------------------------------------------+ |
|  +-------------------------------------------------------------------+ |
|            |                                                            |
|            v scrape (Prom / push OTel)                                  |
|   +------------------+  +----------------+  +------------------+         |
|   | Prometheus +     |  | Jaeger / Tempo |  | Loki / Elasticsearch|       |
|   | Grafana / Mimir  |  | (Trace)        |  | (Log)              |       |
|   +------------------+  +----------------+  +------------------+        |
+-----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Envoy / Linkerd2-proxy** | 데이터 평면 L4/L7 프록시. 사이드카 또는 노트 단위(ztunnel, Cilium) 배치 | HTTP/1.1, HTTP/2, HTTP/3, gRPC, Thrift, Kafka, Mongo, Redis 프로토콜 파싱. 핫리로드 가능한 listener/route/cluster 설정. WASM/Lua 필터로 커스텀 telemetry·인증·변환 로직 임베드. Linkerd2-proxy는 Rust+Tokio 기반 비동기 I/O로 p99
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 586 / 600

<- **이전**: [585. GitOps 선언적 인프라 관리 패턴](/studynote/11_design_supervision/06_exam_summary/586_gitops_declarative_infrastructure_patter/)
**다음**: [587. 인프라 코드화 IaC 선언적 관리](/studynote/11_design_supervision/06_exam_summary/587_infrastructure_as_code_iac_declarative/) ->

---
