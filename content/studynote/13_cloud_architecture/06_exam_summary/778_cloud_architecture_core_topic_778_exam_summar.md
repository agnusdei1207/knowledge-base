---
title: "778. 클라우드 아키텍처 핵심 토픽 778번 시험 요약 (Cloud Architecture Core Topic 778 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS·PaaS·SaaS·FaaS의 4계층 서비스 모델을 기반으로, 컨트롤 플레인(Control Plane)과 데이터 플레인(Data Plane)의 분리를 통해 탄력성(Elasticity), 불변 인프라(Immutable Infrastructure), 셀프서비스 API(self-service API)라는 세 가지 핵심 속성을 구현하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: AWS Well-Architected Framework 기준 잘 설계된 시스템은 배포 빈도 200배, 장애 복구 시간(MTTR) 70% 단축, TCO 30~50% 절감, 가용성 99.99%(연간 52.6분 이내 장애)를 달성하며, CAPEX에서 OPEX로의 재정적 전환과 비즈니스 TT(Time-to-Market)을 수개월에서 수시간으로 단축시킨다.
> 3. **판단 포인트**: 트레이드오프의 핵심은 (1) Multi-Cloud vs Hybrid Cloud vs Single Cloud의 운영 복잡도-비용 효율 트레이드오프, (2) Synchronous(강결합, Chatty API) vs Asynchronous(Event-Driven, Loose Coupling) 통신 패턴의 응답성-복원성 트레이드오프, (3) Stateful vs Stateless 워크로드의 수평확장성-데이터 일관성 트레이드오프, (4) EKS/AKS/GKE 같은 managed Kubernetes vs 자체 VM 기반 컨테이너 오케스트레이션의 제어성-운영부담 트레이드오프이다.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스(On-Premise) 아키텍처는 1990년대 이후 RFC 1925 "The Twelve Networking Truths"의 "It is more complicated than you think" 원칙이 현실화되면서 한계에 부딪혔다. 서버 1대의 수명 주기 약 5년, 용량 계획(Capacity Planning) 기반의 정적 프로비저닝, 조달 리드타임 3~6개월, CAPEX(자본 지출) 중심의 회계 처리, 그리고 트래픽 피크(Black Friday, 명절 등) 대비 70% 이상의 유휴 자원 발생은 곧 비용·민첩성·가용성 3축 모두에서 근본적 결함을 드러냈다.

NIST SP 800-145(2011)는 클라우드 컴퓨팅을 "네트워크, 서버, 스토리지, 애플리케이션, 서비스 등 구성 가능한 컴퓨팅 자원의 공유 풀(Shared Pool)에 대한 네트워크 기반의 어디서나(on-demand) 편리한 즉시 접근"으로 정의하며 5대 필수 특성(필수 5대 특징: On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)과 3대 서비스 모델(SaaS/PaaS/IaaS), 4배치 모델(Public/Private/Hybrid/Community)을 표준화했다.

2024년 기준 글로벌 퍼블릭 클라우드 시장 규모는 약 6,200억 USD로 성장했으며, Gartner는 2027년 전체 IT 지출의 51% 이상이 퍼블릭 클라우드로 이동할 것으로 전망한다. COVID-19 이후 디지털 트랜스포메이션이 가속화되며, Netflix의 카오스 엔지니어링(Chaos Engineering, Chaos Monkey -> ChAP), Amazon Prime Day의 1초당 수백만 트랜잭션 처리, 쿠팡의 MSA(Microservices Architecture) 800+ 서비스 분리 운영 등은 클라우드 네이티브(Cloud Native) 아키텍처가 단순한 "클라우드 이전(Lift & Shift)"이 아닌 근본적 아키텍처 재설계를 요구함을 증명했다.

```text
+----------------------------------------------------------------------+
|              클라우드 아키텍처 패러다임 진화 흐름도                      |
+----------------------------------------------------------------------+
|                                                                      |
|  [1960s Mainframe]   [1980s Client-Server]   [2000s Web 2.0]         |
|   중앙집중형          분산 2-Tier            N-Tier (Web/App/DB)      |
|   Time-sharing       단일 RDBMS              LAMP 스택                |
|        |                   |                      |                  |
|        v                   v                      v                  |
|  +----------------------------------------------------------+        |
|  |      [On-Premise: 2000s~2010s 초반]                       |        |
|  |  - 전용 데이터센터, 5년 서버 라이프사이클                     |        |
|  |  - 수직확장(Scale-Up) 한계: 8-way SMP 코어 수 한계           |        |
|  |  - 트래픽 피크 대비 과잉설계 (Avg 30% Utilization)           |        |
|  |  - 프로비저닝: PO->입고->랙장착->OS설치 = 3~6개월               |        |
|  +----------------------------------------------------------+        |
|                              |                                       |
|                              v 2006 AWS S3/EC2 출시, 2008 GCP        |
|  +----------------------------------------------------------+        |
|  |      [Cloud IaaS Era: 2006~2013]                          |        |
|  |  - 가상화(KVM/Xen/Hyper-V) 기반 EC2, GCE, Azure VM         |        |
|  |  - Auto Scaling Group (ASG) + ELB + EBS                    |        |
|  |  - "Lift & Shift" 마이그레이션, CAPEX -> OPEX 전환           |        |
|  +----------------------------------------------------------+        |
|                              |                                       |
|                              v 2013 Docker 1.0, 2014 K8s 출시        |
|  +----------------------------------------------------------+        |
|  |      [Cloud-Native Era: 2013~현재]                         |        |
|  |  - 컨테이너 + 컨테이너 오케스트레이션 (EKS/AKS/GKE)         |        |
|  |  - MSA(8~10개 -> 200~800개 서비스), API Gateway, Service Mesh|        |
|  |  - 12-Factor App, GitOps, Immutable Infrastructure          |        |
|  |  - IaC (Terraform, Pulumi, CloudFormation, ARM)             |        |
|  +----------------------------------------------------------+        |
|                              |                                       |
|                              v 2017 Lambda, 2018 KNative, 2020 Wasm   |
|  +----------------------------------------------------------+        |
|  |      [Serverless/Edge Era: 2017~현재]                      |        |
|  |  - FaaS (Lambda, Cloud Functions, Azure Functions)          |        |
|  |  - BaaS (Firebase, DynamoDB, S3, Cloudflare Workers)       |        |
|  |  - Cold Start < 100ms, Pay-per-Invocation 모델             |        |
|  |  - Event-Driven, EDA(Event-Driven Architecture) 부상        |        |
|  +----------------------------------------------------------+        |
|                              |                                       |
|                              v 2023~ LLM/AI, WebAssembly, eBPF       |
|  +----------------------------------------------------------+        |
|  |      [AI-Native & Edge Era: 2023~미래]                     |        |
|  |  - GPUaaS (H100, A100, TPU v5p), Inferentia, Trainium     |        |
|  |  - RAG + Vector DB (Pinecone, Weaviate, pgvector)          |        |
|  |  - 5G MEC(Multi-access Edge Computing), Cloudflare/CDN     |        |
|  |  - FinOps, GreenOps, Sustainable Cloud (탄소중립)            |        |
|  +----------------------------------------------------------+        |
+----------------------------------------------------------------------+
```

전통 아키텍처 대비 클라우드 아키텍처의 본질적 차이는 **프로비저닝의 추상화 수준**이다. 물리적 서버(CPU 모델, 랙 위치, 네트워크 케이블) -> 가상 머신(Instance Type, AMI) -> 컨테이너(Image, Replica) -> 함수(Code, Trigger) -> 의도(Intent, "트래픽 1000 RPS 처리")로 갈수록 운영자의 관심 영역(Concern)은 비즈니스 로직으로 이동하고, 인프라 관리 부담은 클라우드 제공자(CSP)가 가져간다(Shared Responsibility Model, AWS 기준 보안을 예로 들면, AWS는 "OF the Cloud"(인프라 자체), 고객은 "IN the Cloud"(데이터·액세스 키) 책임).

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 호텔의 객실 임대와 같다. 자가주택(온프레미스)은 단기 투숙객이 없는 침실까지 유지보수해야 하지만, 호텔(클라우드)은 1인실·2인실·스위트룸(IaaS/PaaS/SaaS) 중 필요 시점에만 골라 쓰고, 룸서비스(Managed Service)도 받을 수 있으며, 체크아웃 후에는 비용 청구가 끝나는 OPEX 모델이다. 연중 365일 만실인 호텔은 드물 듯, 클라우드도 FinOps로 낭비 자원을 지속적으로 회수해야 진정한 클라우드 경제성을 거둘 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심 원리는 5개의 기본 모델로 분해할 수 있다: (1) **다중 계층(Multi-Tier)**, (2) **이벤트 기반(Event-Driven)**, (3)** 마이크로서비스(Microservices)**, (4) **서버리스(Serverless)**, (5) **데이터 중심(Data-Centric / Lake House)**. 모든 모델은 AWS Well-Architected Framework의 6가지 필러(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화, 지속 가능성)를 만족하도록 설계되어야 한다.

### 가. 컨트롤 플레인(Control Plane)과 데이터 플레인(Data Plane) 분리

모든 클라우드 아키텍처의 가장 근본적인 설계 원칙은 **두 평면의 물리적·논리적 분리**이다. 컨트롤 플레인은 API 서버, 스케줄러, etcd 같은 메타데이터·정책·오케스트레이션 신호를 처리하고(보통 1Gbps 미만, 지연 시간에 둔감), 데이터 플레인은 실제 사용자 트래픽·데이터 패킷을 처리한다(수십 Gbps, p99 지연 시간 1ms 미만 목표). 두 평면을 같은 네트워크에 혼재시키면 컨트롤 플레인 DoS가 데이터 평면 장애로 확대된다.

```text
+--------------------------------------------------------------------------+
|        AWS Well-Architected 6 Pillars + 클라우드 아키텍처 계층도          |
+--------------------------------------------------------------------------+
|                                                                          |
|  +------------------------------------------------------------------+      |
|  |   Client Layer (사용자 단말)                                      |      |
|  |   - Mobile (iOS/Android), SPA(React/Vue), Desktop, IoT          |      |
|  |   - Edge Compute: CloudFront, Cloudflare Workers, Lambda@Edge  |      |
|  +------------------------------------------------------------------+      |
|                                  | TLS 1.3 (X.509 ACM)                   |
|                                  v                                       |
|  +------------------------------------------------------------------+      |
|  |   Edge / CDN Layer (엣지/전송)                                    |      |
|  |   - AWS CloudFront / Azure CDN / GCP Cloud CDN                   |      |
|  |   - WAF, Shield (DDoS L3~L7), Route 53 Latency-based Routing     |      |
|  |   - Anycast IP (PoP 600+ locations, 캐시 적중률 70~95%)           |      |
|  +------------------------------------------------------------------+      |
|                                  |                                       |
|                                  v                                       |
|  +------------------------------------------------------------------+      |
|  |   Ingress / API Gateway Layer (인그레스 게이트웨이)               |      |
|  |   - API Gateway / Kong / Envoy Gateway / Istio Ingress           |      |
|  |   - Rate Limiting (Token Bucket, 1000 RPS), AuthN/Z (JWT, OAuth) |      |
|  |   - Request Validation, Schema Enforcement (OpenAPI 3.0)          |      |
|  |   - Circuit Breaker (Hystrix -> Resilience4j -> Envoy)              |      |
|  +------------------------------------------------------------------+      |
|                                  |                                       |
|                                  v                                       |
|  +------------------------------------------------------------------+      |
|  |   Application / Compute Layer (애플리케이션 계층)                 |      |
|  |   +--------------+--------------+--------------+------------+    |      |
|  |   |  IaaS        |  CaaS        |  PaaS        |  FaaS      |    |      |
|  |   |  EC2 m7i.4xl |  EKS Pod     |  App Runner  |  Lambda    |    |      |
|  |   |  Stateful    |  Stateless   |  Beanstalk   |  Cloud Fn  |    |      |
|  |   |  Long-lived  |  Sidecar     |  Cloud Run   |  Step Fn   |    |      |
|  |   +--------------+--------------+--------------+------------+    |      |
|  +------------------------------------------------------------------+      |
|                                  |                                       |
|                                  v                                       |
|  +------------------------------------------------------------------+      |
|  |   Service Mesh / Sidecar Layer (서비스 메시)                      |      |
|  |   - Istio / Linkerd / Consul Connect / App Mesh                   |      |
|  |   - mTLS 자동화, Traffic Splitting (Canary 5->25->50->100%)         |      |
|  |   - Distributed Tracing (Jaeger, Zipkin, AWS X-Ray)              |      |
|  +------------------------------------------------------------------+      |
|                                  |                                       |
|                                  v                                       |
|  +------------------------------------------------------------------+      |
|  |   Data Layer (데이터 계층)                                         |      |
|  |   - RDBMS: Aurora, RDS, Spanner, Cosmos DB (Strong/Global)        |      |
|  |   - NoSQL: DynamoDB (p99 < 10ms), MongoDB Atlas, Cassandra        |      |
|  |   - Cache: ElastiCache (Redis/Memcached), DAX                      |      |
|  |   - Warehouse: Snowflake, Redshift, BigQuery, Databricks          |      |
|  |   - Lake: S3 + Glue + Athena, Delta Lake, Iceberg                  |      |
|  |   - Streaming: Kinesis, Kafka (MSK), Pub/Sub, Flink                |      |
|  +------------------------------------------------------------------+      |
|                                  |                                       |
|                                  v                                       |
|  +------------------------------------------------------------------+      |
|  |   Observability Layer (관측 가능성)                                 |      |
|  |   - Logs: CloudWatch, Loki, OpenSearch, ELK Stack                  |      |
|  |   - Metrics: Prometheus + Grafana, CloudWatch, Datadog             |      |
|  |   - Traces: OpenTelemetry SDK -> Jaeger / Tempo / X-Ray             |      |
|  |   - USE Method (Utilization/Saturation/Errors), RED Method          |      |
|  +------------------------------------------------------------------+      |
+--------------------------------------------------------------------------+
```

### 나. 핵심 구성 요소별 역할 및 동작 방식

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Auto Scaling Group (ASG) / HPA·VPA·
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 778 / 800

<- **이전**: [777. 클라우드 아키텍처 핵심 토픽 777번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/777_cloud_architecture_core_topic_777_exam_summar/)
**다음**: [779. 클라우드 아키텍처 핵심 토픽 779번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/779_cloud_architecture_core_topic_779_exam_summar/) ->

---
