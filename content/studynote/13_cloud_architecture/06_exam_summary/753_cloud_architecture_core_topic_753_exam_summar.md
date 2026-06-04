---
title: "753. 클라우드 아키텍처 핵심 토픽 753번 시험 요약 (Cloud Architecture Core Topic 753 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST 표준의 IaaS/PaaS/SaaS·Public/Private/Hybrid 배포 모델을 기반으로, 12-Factor App·Microservices·Serverless·Event-driven 패턴을 조합하여 **탄력성(Elasticity)·확장성(Scalability)·가용성(Availability)**의 세 축을 동시에 만족시키는 분산 시스템 설계 체계이다.
> 2. **가치**: Auto Scaling 그룹을 통한 capacity provisioning 시간 단축(T 수동 -> 분 단위), Multi-AZ 배포로 SLA 99.99% 달성, Spot/Preemptible Instance 활용 시 컴퓨팅 비용 60~90% 절감, Pay-per-use 모델로 CapEx -> OpEx 전환 시 TCO 30~50% 감소 효과를 제공한다.
> 3. **판단 포인트**: CAP Theorem 하의 Consistency/Availability/Partition Tolerance 트레이드오프, Synchronous(Strong) vs Asynchronous(Eventually Consistent) 복제 선택, Stateless vs Stateful 컴포넌트 경계 설정, 그리고 **Lift-and-Shift** vs **Cloud-Native Refactoring** 마이그레이션 전략 결정이 아키텍트의 핵심 의사결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스(On-Premise) 시스템은 **수직 확장(Scale-Up)** 한계, 용량 계획(Capacity Planning) 실패, CAPEX 중심의 과다 투자, 그리고 장애 도메인 단일화(Single Point of Failure)로 인해 디지털 트랜스포메이션 요구사항을 충족하지 못한다. 클라우드 아키텍처는 가상화(Hypervisor: KVM, Xen, Hyper-V) -> 컨테이너화(Docker, containerd) -> 오케스트레이션(Kubernetes) -> 서버리스(Lambda, Cloud Functions)로 진화해왔으며, 이는 **인프라 추상화 수준**을 점진적으로 높여 개발자가 비즈니스 로직에 집중할 수 있게 한다.

```text
+---------------------------------------------------------------------+
|              클라우드 컴퓨팅 진화 패러다임 (Evolution)              |
+---------------------------------------------------------------------+
|                                                                     |
|  [1세대] Mainframe       [2세대] x86 가상화   [3세대] Cloud         |
|  +----------+            +----------+         +----------+          |
|  | 단일 시스템|            |  VM 기반  |         | 분산 클라우드|          |
|  | 분할 불가  |            | 멀티테넌시|         | 글로벌 엣지  |          |
|  +----------+            +----------+         +----------+          |
|        |                       |                     |             |
|        v                       v                     v             |
|  Scale-Up Only         Hypervisor Layer        Multi-Cloud         |
|  Static Capacity       Resource Pooling        Service Mesh        |
|  99.9% SLA              99.95% SLA              99.99% SLA          |
|                                                                     |
|  [추상화 수준]  Low ◄------------------------------► High           |
|  [탄력성]       Low ◄------------------------------► High           |
|  [CAPEX 비중]   High ◄-----------------------------► Low (OpEx)    |
+---------------------------------------------------------------------+
```

NIST SP 800-145 정의에 따르면 클라우드 컴퓨팅은 **5대 필수 특성**(On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)과 **3대 서비스 모델**(IaaS, PaaS, SaaS), **4대 배포 모델**(Public, Private, Hybrid, Community)로 분류된다. 2024년 현재 Gartner 보고서 기준 전 세계 퍼블릭 클라우드 시장 규모는 약 6,790억 USD이며, 한국은 2027년까지 연평균 22% 성장이 전망된다.

**온프레미스 vs 클라우드 패러다임 비교**:
- **프로비저닝**: 수동(2~8주) -> API 호출(초 단위, Terraform/CloudFormation IaC)
- **장애 대응**: 단일 DC, Cold Standby -> Multi-Region Active-Active, 자동 페일오버(<1분)
- **과금**: 선불 CAPEX -> Pay-as-you-go(초/밀리초 단위 과금, Lambda 등)
- **확장**: 하드웨어 구매(Scale-Up) -> HPA/VPA/Cluster Autoscaler(Scale-Out)

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **수도권 전기 그리드**와 같다. 발전소(IaaS 데이터센터)에서 변전소(PaaS 플랫폼)를 거쳐 가정(SaaS 애플리케이션)까지, 사용자는 실시간 수요에 맞춰 전기(컴퓨팅 자원)를 켜고 끌 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **Well-Architected Framework**(AWS 5대 piliers, Azure 6대, GCP 5대)의 공통 원칙인 Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability를 분산 시스템에 구현하는 것이다.

```text
+----------------------------------------------------------------------+
|          클라우드 네이티브 참조 아키텍처 (Reference Architecture)     |
+----------------------------------------------------------------------+
|                                                                      |
|   +----------+   +----------+   +----------+   +----------+         |
|   |  Mobile  |   |   Web    |   |   API    |   | Partner  |  Clients|
|   |   App    |   |   SPA    |   | Consumer |   |   B2B    |         |
|   +-----+----+   +----+-----+   +----+-----+   +----+-----+         |
|         |             |              |              |                |
|         +-------------+------+-------+--------------+                |
|                              v                                       |
|                    +------------------+                              |
|                    |   CDN + WAF      |  (CloudFront, Cloudflare)    |
|                    |   DDoS Shield    |                              |
|                    +--------+---------+                              |
|                             v                                        |
|                    +------------------+                              |
|                    |   API Gateway    |  (Kong, Apigee, AWS API GW)  |
|                    |  Rate Limiting   |                              |
|                    |  AuthN/AuthZ     |                              |
|                    +--------+---------+                              |
|         +-------------------+-------------------+                    |
|         v                   v                   v                    |
|  +-------------+    +-------------+    +-------------+              |
|  | Microservice|    | Microservice|    | Microservice|  Service     |
|  |    (Java)   |    |  (Node.js)  |    |   (Go/Py)   |  Mesh        |
|  |  K8s Pod×N  |    |  K8s Pod×N  |    |  Lambda Fn  |  (Istio)     |
|  +------+------+    +------+------+    +------+------+              |
|         |                  |                  |                     |
|         +------------------+------------------+                     |
|                            v                                        |
|              +--------------------------+                           |
|              |   Message Broker         |  (Kafka, RabbitMQ,        |
|              |   Event Bus (Choreo.)    |   AWS SQS/SNS, EventBridge)|
|              +----------+---------------+                           |
|                         |                                           |
|         +---------------+---------------+                           |
|         v               v               v                           |
|  +-------------+ +-------------+ +--------------+                   |
|  |   RDBMS     | |  NoSQL DB   | | Object Store |  Data Tier        |
|  | (Aurora,    | | (DynamoDB,  | |   (S3, GCS)  |                   |
|  |  Cloud SQL) | |  CosmosDB)  | |              |                   |
|  +-------------+ +-------------+ +--------------+                   |
|                                                                      |
|  [관측성] Prometheus + Grafana, Jaeger(Tracing), ELK(Logging)        |
|  [IaC]      Terraform, Pulumi, Crossplane, Helm Charts              |
|  [CI/CD]    GitHub Actions, ArgoCD (GitOps), Jenkins X               |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway** | 단일 진입점(Edge), L7 라우팅, 인증/인가, Rate Limiting, Request Transformation | Kong(Plugin 기반), AWS API Gateway(Lambda 통합), Envoy Proxy(xDS API), Spring Cloud Gateway(Filter Chain). 처리량: Kong은 노드당 10K+ RPS, API GW는 Burst 10K RPS 지원 |
| **Service Mesh** | Sidecar Proxy로 서비스 간 mTLS, 트래픽 관리(Canary 5%->50%->100%), Circuit Breaker, Observability | Istio(Envoy 기반, Control Plane: Pilot/Citadel), Linkerd(Buoyant, Rust 기반 Rust Proxy), Consul Connect, AWS App Mesh. eBPF 기반 Cilium Service Mesh 등장 |
| **Container Orchestrator** | 컨테이너 스케줄링, 자기 치유(Self-healing), HPA/VPA/Cluster Autoscaler, Service Discovery, Secret 관리 | Kubernetes 1.30+(CRI: containerd, CSI, CNI), ECS Fargate(Serverless Container), EKS/AKS/GKE. Pod 단위 리스케줄링 시간 ~5초 |
| **Serverless Platform** | 이벤트 기반 FaaS, Cold Start 관리(Provisioned Concurrency), Function 단위 Auto Scaling, Pay-per-Invocation | AWS Lambda(128MB~10GB, 15분 Timeout), Azure Functions(Durable Functions), GCP Cloud Run(Stateless Container), Cloudflare Workers(V8 Isolates, Cold Start <5ms) |
| **Event Streaming Platform** | Pub/Sub 메시징, Exactly-Once Semantics, Log-Based Broker, Event Sourcing 백본 | Apache Kafka(KRaft 모드, 100K+ msg/sec/partiton), Pulsar(분산 Segment), AWS Kinesis Data Streams(Shard당 1K write/sec), NATS JetStream |
| **Observability Stack** | Metrics(시계열), Logs(구조화), Traces(Distributed), 3-pillar 통합 | Prometheus + Thanos(장기 저장), Grafana Loki(로그), OpenTelemetry(표준 SDK), Jaeger/Tempo(트레이싱), eBPF(zero-code instrumentation) |

**12-Factor App 핵심 원칙** (Heroku 2011 -> 현재 Cloud Native Computing Foundation 표준):
1. **Codebase**: One codebase, multiple deploys (Git Repo ↔ Dev/Staging/Prod 매핑)
2. **Dependencies**: 명시적 의존성 선언(`requirements.txt`, `package.json`), 시스템 전역 암묵 의존 금지
3. **Config**: 환경변수 주입, 코드와 설정 분리 (Vault, AWS Parameter Store, K8s ConfigMap/Secret)
4. **Backing Services**: DB, Cache, MQ를 **Attached Resource**로 취급, URL/credential로 추상화
5. **Build, Release, Run**: 세 단계 엄격 분리, Immutable Release
6. **Processes**: Stateless 프로세스, Sticky Session 금지, 외부 저장소(Redis Session) 사용
7. **Port Binding**: 자체 HTTP 포트 바인딩, 외부 WAS 의존 제거
8. **Concurrency**: 프로세스 모델로 수평 확장, Worker Process 분리
9. **Disposability**: Fast Startup(<10s), Graceful Shutdown(SIGTERM 처리, In-flight Request 완료 대기)
10. **Dev/Prod Parity**: Gap 최소화, Docker로 환경 일치, 시간 단축 마이그레이션
11. **Logs**: stdout/stderr 스트림, Fluentd/Loki로 집계
12. **Admin Processes**: One-off Task(마이그레이션, 배치) 프로세스로 분리 실행

**핵심 알고리즘/수식**:
- **Auto Scaling 결정 수식** (K8s HPA): `desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]`
- **이벤트 드리븐 일관성** (Saga Pattern): `T = Σ(Compensation Latency)`, 부분 실패 시 보상 트랜잭션으로 결과적 일관성(Eventual Consistency) 확보
- **가용성 수식**: `SLA = 1 - (Σ(Downtime_i) / Total_Time)`, 99.99% (Four 9s) = 연 52.6분, 99.999% (Five 9s) = 연 5.26분

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **우체국 시스템**과 같다. 우체국(API Gateway)이 우편물을 분류하고, 배달부(Service Mesh)가 구역별로 배달하며, 중앙 분류소(Orchestrator)가 배달부 수를 실시간 조절한다. 택배함(Object Store)은 어디서든 찾아 꺼낼 수 있다.

---

## Ⅲ. 비교 및 연결

| 구분 | **Monolithic** | **Microservices** | **Serverless (FaaS)** |
| :--- | :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/EAR/실행파일 (수백 MB~GB) | 독립 서비스 컨테이너 (수십~수백 MB) | 함수 단위 코드 (수 MB, Zip) |
| **확장 방식** | Scale-Up (수직) + Load Balancer | Scale-Out (수평, Pod Replication) | 자동 (요청 수 기반, 0~수천 동시) |
| **장애 격리** | 낮음 (한 모듈 장애 -> 전체 영향) | 높음 (Circuit Breaker, Bulkhead) | 매우 높음 (함수 단위 격리) |
| **Cold Start** | N/A (Long-Running Process) | K8s Pod 시작: 5~30초 | Lambda: 100ms~수초 (Provisioned Concurrency로 0ms) |
| **상태 관리** | In-Memory (서버 간 공유 불가) | 외부화 (Redis, DB), Stateless 선호 | 강제 Stateless (Local FS 비영구) |
| **트랜잭션** | ACID (단일 DB) | Saga Pattern, Eventual Consistency | Step Functions, Durable Functions (Orchestration) |
| **비용 모델** | 상시 비용 (예약 인스턴스) | Pod당 과금 (1분 단위 최소) | 실행 시간(ms) + 호출 횟수 |
| **적합 워크로드** | 단순 CRUD, 레거시, 소규모 | 복잡한 도메인, 다수 팀, 고가용성 | Event-driven, 간헐적, 스파이크 워크로드 |
| **대표 기술** | Spring Boot, Django, Rails | Spring Cloud, K8s + Istio, gRPC | Lambda, Cloud Functions, Cloudflare Workers |

**주변 기술과의 연결 관계**:
- **DevOps/Platform Engineering**: GitOps(ArgoCD, Flux CD), Internal Developer Platform(IDP, Backstage), Dapr(Distributed Application Runtime)
- **AIOps/MLOps**: Kubeflow, MLflow, SageMaker Pipelines, Vector DB(Pinecone, Milvus) 기반 RAG
- **Edge Computing**: AWS Wavelength, Azure
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 753 / 800

<- **이전**: [752. 클라우드 아키텍처 핵심 토픽 752번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/752_cloud_architecture_core_topic_752_exam_summar/)
**다음**: [754. 클라우드 아키텍처 핵심 토픽 754번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/754_cloud_architecture_core_topic_754_exam_summar/) ->

---
