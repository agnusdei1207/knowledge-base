---
title: "Cloud Architecture Core Topic 767 Exam Summary"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 Well-Architected Framework(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속가능성) 기반 위에서 IaC(Infrastructure as Code), MSA(Microservices Architecture), 컨테이너 오케스트레이션(Kubernetes), 서버리스(FaaS/CaaS), 이벤트 기반 메시지 스트리밍(Kafka, EventBridge)을 결합하여 자가 치유(self-healing), 탄력적 확장(auto-scaling), 선언적 API(Declarative API) 패턴을 구현하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: AWS/Azure/GCP 기준 동일 워크로드 대비 온프레미스 대비 TCO 30~60% 절감, Auto Scaling Group을 통한 트래픽 변동 대응 시간 수 분 -> 수 초, 멀티 AZ/리전 배포 시 SLA 99.99%(연간 52.6분 이내 장애), EKS/AKS/GKE 기반 컨테이너 밀도 10~20x 향상, FinOps 도입으로 클라우드 비용 20~40% 최적화가 가능하다.
> 3. **판단 포인트**: 단일 클라우드 종속(vendor lock-in) 회피를 위한 추상화 계층(Terraform, Crossplane, Pulumi) 도입, CAP 정리 기반의 일관성(Consistency) vs 가용성(Availability) 트레이드오프, 동기/비동기 호출 비율에 따른 Saga/CQRS/Event Sourcing 패턴 선택, 12-Factor App 원칙 준수 여부, 데이터 주권·규제(GDPR, 개인정보보호법, CSAP) 충족을 위한 리전 선택이 핵심 의사결정 사안이다.

---

## Ⅰ. 개요 및 필요성

클라우드 아키텍처는 2006년 AWS S3/EC2 출시 이후 가상화(Virtualization) -> 컨테이너화(Containerization) -> 오케스트레이션(Orchestration) -> 서버리스(Serverless) -> 분산 클라우드(Distributed Cloud)로 진화해 왔으며, 2020년경부터는 GitOps, FinOps, AIOps, Platform Engineering이 클라우드 운영의 4대 축으로 자리잡았다. 기술사 시험에서는 단순히 "클라우드를 쓴다"는 수준이 아니라, **어떤 워크로드에 어떤 서비스 모델(IaaS/PaaS/SaaS/FaaS)을, 어떤 배포 모델(Public/Private/Hybrid/Multi)로, 어떤 참조 아키텍처(CAF, WAF, SAFe Cloud)를 적용할지**에 대한 정량적 판단 근거와 마이그레이션 전략(6R: Rehost, Replatform, Refactor, Repurchase, Retire, Retain)을 요구한다.

기존 온프레미스(legacy 3-tier architecture: Web-WAS-DB) 환경은 CAPEX(설비투자) 중심으로 예측 기반 용량 계획(capacity planning)을 수행했으나, 트래픽 피크 대비 과잉 Provisioning으로 인한 유휴 자원 60~80% 발생, 장애 시 수동 대응(MTTR 평균 4~8시간), 수직 확장(Scale-up) 한계, 배포 주기 주~월 단위라는 문제가 상존했다. 반면 클라우드 아키텍처는 OPEX 기반 종량 과금(pay-per-use), HPA(Horizontal Pod Autoscaler)/Cluster Autoscaler 기반 자동 확장, IaC(Terraform, CloudFormation, ARM Template, CDK)를 통한 코드형 인프라 관리, CI/CD 파이프라인(ArgoCD, Spinnaker, Jenkins X)을 통한 일 단위 배포, Chaos Engineering(Chaos Monkey, LitmusChaos, Gremlin)을 통한 선제적 장애 대응이 가능하다.

```text
+------------------------------------------------------------------+
|            Legacy On-Premise vs Modern Cloud Architecture        |
+------------------------------------------------------------------+
|                                                                  |
|  [Legacy 3-Tier]                  [Cloud-Native 12-Factor]       |
|                                                                  |
|  +--------------+                +--------------------------+    |
|  |  Client      |                |  CDN (CloudFront/Akamai) |    |
|  |  Browser     |                +----------+---------------+    |
|  +------+-------+                           |                    |
|         v                                   v                    |
|  +--------------+                +--------------------------+    |
|  |  Web Server  |                |  API Gateway / WAF       |    |
|  |  (Apache)    |                |  + Load Balancer (ALB)   |    |
|  +------+-------+                +----------+---------------+    |
|         v                                   v                    |
|  +--------------+                +--------------------------+    |
|  |  WAS         |                |  Microservices (EKS/AKS) |    |
|  |  (Tomcat)    |                |  + Service Mesh (Istio)  |    |
|  +------+-------+                +----------+---------------+    |
|         v                                   v                    |
|  +--------------+                +--------------------------+    |
|  |  RDBMS       |                |  Polyglot Persistence    |    |
|  |  (Oracle)    |                |  (RDB+NoSQL+Cache+Search)|    |
|  +--------------+                +--------------------------+    |
|                                                                  |
|  Scale: 수직(Scale-up)              Scale: 수평(Scale-out)        |
|  배포: 수개월                       배포: 수 분 (GitOps)         |
|  비용: CAPEX (예측)                  비용: OPEX (사용량)          |
|  가용성: 99.9% (이중화)               가용성: 99.99% (Multi-AZ)   |
+------------------------------------------------------------------+
```

**📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 "수도요금처럼 쓰는 만큼만 내는 전기 시스템"과 같다. 전통적 발전소(온프레미스 데이터센터)는 최대 부하를 기준으로 대형 터빈을 미리 세워야 하지만, 스마트 그리드(클라우드)는 실시간 수요에 따라 가정용 태양광, 풍력, 화력을 동적으로 조합하여 공급한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **4계층 참조 모델**(Presentation/API Layer -> Application/Compute Layer -> Data/Persistence Layer -> Infrastructure/Foundation Layer)과 **5대 설계 원칙**(단일 책임, 느슨한 결합, 자가 치유, 선언적 구성, 불변 인프라)에 기반한다. 기술사 시험에서는 AWS Well-Architected Framework의 6가지 필러(Pillar), Azure Cloud Adoption Framework(CAF)의 8단계, GCP Architecture Framework의 디자인 프로세스를 통합적으로 이해하고 있어야 한다.

```text
+--------------------------------------------------------------------+
|         Multi-Cloud Reference Architecture (with Service Mesh)     |
+--------------------------------------------------------------------+
|                                                                    |
|  [Edge Layer]                                                      |
|   CloudFront / Azure CDN / Cloud CDN -- WAF, DDoS Protection       |
|              |                                                     |
|              v                                                     |
|  [API Gateway Layer]                                               |
|   Kong / AWS API GW / Apigee / Ambassador                          |
|   +-- Auth (OAuth2.0, OIDC, JWT)                                   |
|   +-- Rate Limiting (Token Bucket)                                 |
|   +-- Circuit Breaker (Hystrix/Resilience4j)                       |
|   +-- Request Routing / Transformation                             |
|              |                                                     |
|              v                                                     |
|  [Service Mesh Layer - Istio/Linkerd/Consul Connect]               |
|   +--------------------------------------------------+            |
|   |  Data Plane (Envoy Sidecar)                       |            |
|   |  +-- mTLS 자동 적용                               |            |
|   |  +-- L7 로드밸런싱 (Header/Path 기반)             |            |
|   |  +-- 트래픽 분할 (Canary 90/10, Blue-Green)       |            |
|   |  +-- 재시도/타임아웃/서킷브레이커 정책             |            |
|   |  +-- 분산 트레이싱 (Jaeger/Zipkin 연동)            |            |
|   |  Control Plane (Istiod)                           |            |
|   |  +-- xDS API 기반 설정分发                         |            |
|   |  +-- Pilot (라우팅), Citadel(보안), Galley(설정)    |            |
|   +--------------------------------------------------+            |
|              |                                                     |
|              v                                                     |
|  [Application Layer - Container Orchestration]                     |
|   Kubernetes (EKS/AKS/GKE/OKE) + Operators                        |
|   +----------+----------+----------+----------+                  |
|   | Pod      | Pod      | Pod      | Pod      |  (HPA: 1->100)    |
|   | user-svc | order-svc| pay-svc  | notif-svc|                  |
|   +----------+----------+----------+----------+                  |
|   StatefulSet / Deployment / DaemonSet / Job/CronJob              |
|                                                                    |
|              |                                                     |
|              v                                                     |
|  [Data Layer - Polyglot Persistence]                              |
|   +-------------+-------------+-------------+--------------+     |
|   | RDB         | NoSQL       | Cache       | Search       |     |
|   | Aurora PG   | DynamoDB    | ElastiCache | OpenSearch   |     |
|   | (OLTP, ACID)| (CAP:AP)    | (Redis)     | (Full-text)  |     |
|   +-------------+-------------+-------------+--------------+     |
|              |                                                     |
|              v                                                     |
|  [Event Streaming - Backbone for Async]                           |
|   Apache Kafka / Amazon Kinesis / EventBridge HUB / Pulsar        |
|   +-- CDC (Debezium) -> DB 변경 이벤트 전파                        |
|   +-- Event Sourcing 패턴 (불변 로그)                              |
|   +-- CQRS Read Model 분리                                        |
|              |                                                     |
|              v                                                     |
|  [Observability Layer]                                             |
|   Metrics: Prometheus + Grafana / CloudWatch                       |
|   Logs:    ELK/EFK / Loki / OpenSearch                            |
|   Traces:  Jaeger / Tempo / X-Ray / Datadog APM                   |
|   SLI/SLO: Error Budget 99.9% (월 43분) vs 99.95% (월 21분)       |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway / Edge Proxy** | 외부 트래픽 진입점, 인증/인가, 라우팅, 변환 | Kong(nginx 기반, Lua 플러그인), AWS API Gateway(REST/WebSocket/Lambda 통합), Envoy(xDS API, WASM 필터), Apigee(API 분석·할당량·모놀리식 분해) |
| **Service Mesh (Data+Control Plane)** | 마이크로서비스 간 통신의 비기능 요구사항(보안·관측·트래픽 제어) 분리 | Istio(Envoy sidecar injection, mTLS 1.3 SPIFFE ID, Traffic Mirroring), Linkerd(Linkerd2-proxy Rust 기반 경량, Tokio 런타임), Consul Connect(HashiCorp生态계 통합, Multi-DC 지원) |
| **Container Orchestrator** | 컨테이너 자동 배포, 스케일링, 셀프힐링, 롤링 업데이트 | Kubernetes 1.30+ (CRI/containerd, CNI/Cilium, CSI/ebs-csi-driver), HPA(Metric Server -> CPU/Memory/Custom), VPA, KEDA(이벤트 기반 0->N 스케일링), Karpenter(AWS, 노드 프로비저닝 30초 이내) |
| **Message Broker / Event Bus** | 비동기 통신, 이벤트 기반 결합도 완화, 버스트 흡수 | Apache Kafka(Partition, ISR, Exactly-Once Semantics EOS, KRaft consensus), RabbitMQ(AMQP 0-9-1, Quorum Queue), AWS SQS(Standard/FIFO, Visibility Timeout, DLQ), AWS EventBridge(Schema Registry, Event Bus 규칙) |
| **Polyglot Persistence** | 워크로드별 최적 데이터 저장소 조합 | RDB(Aurora MySQL/PostgreSQL, 5x MySQL, 3x PostgreSQL 성능), NoSQL(DynamoDB Single-digit millisecond, Cassandra Wide-Column, MongoDB Document), Cache(Redis Cluster 16,384 shards, Memcached), Search(OpenSearch BM25+KNN 하이브리드), Data Lake(S3 + Iceberg/Delta Lake/Hudi ACID 트랜잭션) |
| **Observability Stack (3 Pillars)** | 시스템 상태 측정 및 SLI/SLO 기반 의사결정 | Metrics(Prometheus TSDB, 1 샘플=1.4 bytes), Logs(Loki 라벨 기반 인덱싱, 압축 5x), Traces(OpenTelemetry OTLP 표준, W3C Trace Context, 128-bit TraceID), USE/RED 메서드 |
| **IaC & GitOps** | 인프라/앱의 선언적 정의와 자동 동기화 | Terraform(HCL 2.0, State Lock, Module Registry, Sentinel/OPA Policy), Pulumi(타입 안전, Python/TS/Go 멀티 언어), ArgoCD(Application Controller, Sync Wave, Drift Detection), Flux CD(OCI Helm 지원) |

**핵심 메커니즘 - HPA(Horizontal Pod Autoscaler) 동작 알고리즘**:
`desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]`
예: 현재 4개 Pod, CPU 80% 사용 중, 목표 50%일 때 -> `ceil[4 × (80/50)] = ceil[6.4] = 7개`로 스케일 아웃. KEDA의 경우 Kafka Lag, SQS Queue Length, Cron Schedule 등 60+ Scaler를 통해 Event-Driven 0->N 스케일링 지원. 안정화를 위해 `--horizontal-pod-autoscaler-upscale-delay`(기본 3분), `--horizontal-pod-autoscaler-downscale-stabilization-window`(기본 5분) 튜닝 필수.

**📢 섹션 요약 비유**: 클라우드 아키텍처는 "국제공항의 허브 앤 스포크 시스템"과 같다. 공항(API Gateway)에서 탑승 수속·보안검색(인증/인가)을 거친 승객(요청)이 게이트(Service Mesh 라우팅)를 거쳐 비행기(K8s Pod)들 중 적절한 좌석(컨테이너)에 안내되고, 수하물(데이터)은 별도의 벨트 컨베이어(Kafka/EventBridge)로 목적지(DB·Cache·Search)에 분류되어 도착한다.

---

## Ⅲ. 비교 및 연결

| 구분 | IaaS (예: EC2, GCE) | PaaS (예: Beanstalk, App Engine) | CaaS (예: EKS, Cloud Run) | FaaS (예: Lambda, Cloud Functions) |
| :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | HW + 가상화 + 네트워크 + 스토리지 | + 미들웨어 + 런타임 | + OS + 컨테이너 런타임 | + 애플리케이션 코드 외 전부 |
| **확장 단위** | VM 인스턴스 | 인스턴스/슬롯 | Pod/Container | 요청 단위 (ms 과금) |
| **콜드 스타트** | 없음 (이미 부팅) | 30초~수 분 | 1~10초 (이미지 풀) | 100ms~수 초 (SnapStart로 10ms) |
| **적합 워크로드** | 레거시, 특수 HW, 장기 실행 | 웹앱 표준, 빠른 출시 | MSA, 배치, CI/CD | 이벤트 처리, 글루 코드, 스케줄러 |
| **제어력 vs 생산성** | 제어 ^^ / 생산성 v | 제어 ^ / 생산성 ^ | 제어 ^ / 생산성 ^^ | 제어 v / 생산성 ^^^ |
| **대표 제약** | OS 패치 직접, Auto Scaling 직접 구성 | 런
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 767 / 800

<- **이전**: [766. 클라우드 아키텍처 핵심 토픽 766번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/766_cloud_architecture_core_topic_766_exam_summar/)
**다음**: [768. 클라우드 아키텍처 핵심 토픽 768번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/768_cloud_architecture_core_topic_768_exam_summar/) ->

---
