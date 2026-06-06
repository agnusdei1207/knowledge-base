---
title: "Cloud Architecture Core Topic 793 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 컨테이너 오케스트레이션(Kubernetes), 선언적 IaC(Terraform/CloudFormation), 서비스 메시(Istio/Linkerd), 서버리스(FaaS) 및 12-Factor/Cloud-Native 원칙을 결합하여, 워크로드의 탄력적 확장(Scaling), 자가 치유(Self-healing), 불변 인프라(Immutable Infra)를 통해 CAP 정리를 만족하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: Auto Scaling Group + HPA(Horizontal Pod Autoscaler) 조합으로 트래픽 10배 급증 시 60초 내 대응 가능, Spot Instance + Reserved Instance 혼용으로 컴퓨팅 비용 40~70% 절감, Multi-AZ/Region 구성으로 RTO ≤ 4분 / RPO ≤ 1분 수준의 DR(Disaster Recovery) 달성, MTTR(Mean Time To Recovery)을 모놀리식 대비 80% 단축.
> 3. **판단 포인트**: Stateful(데이터베이스, 메시지 큐) vs Stateless(API, 배치) 워크로드의 분리 전략, Synchronous(REST/gRPC) vs Asynchronous(Event Bus/Kafka) 통신 패턴 선택, EDA(Event-Driven Architecture) 기반 Choreography vs Orchestration(Saga) 트랜잭션 모델 결정, FinOps 기반 Reserved/Spot/On-Demand 인스턴스 비율 최적화, Shared Responsibility Model 하의 Zero Trust 보안 모델 적용 여부.

---

## Ⅰ. 개요 및 필요성

전통적인 On-Premise 3-Tier 아키텍처(Monolithic + RDBMS + Load Balancer)는 CAP 정리에서 Consistency를 우선시하여 수직 확장(Vertical Scaling) 위주로 설계되었으며, 최대 18~36개월의 하드웨어 도입 사이클, CapEx 중심의 비용 구조, 트래픽 정점(Peak) 기준의 과다 용량 설계로 평균 30~40%의 유휴 자원(Idle Resource)이 발생한다. 또한, 단일 장애점(SPOF: Single Point of Failure)인 Active-Standby DB 구성은 RTO가 수 시간에서 수일 수준이며, HA(High Availability) 구성 변경 시 수동 개입과 수 시간의 다운타임이 요구된다.

클라우드 아키텍처는 NIST SP 800-145 기준의 5대 특성(탄력적 확장, 측정 가능성, 주문형 셀프서비스, 광범위한 네트워크 접근, 자원 풀링)을 기반으로, IaaS(EC2, Compute Engine), PaaS(Elastic Beanstalk, App Engine), SaaS(Office 365, Salesforce), FaaS(Lambda, Cloud Functions)의 4계층 서비스 모델을 제공한다. 이를 통해 ① 마이크로서비스 경계를 통한 도메인별 독립 배포, ② 컨테이너를 통한 환경 일관성(Dev/Prod Parity) 확보, ③ 선언적 IaC로 GitOps 기반의 불변 인프라 운영, ④ 서비스 메시로 East-West 트래픽의 L7 관찰가능성(Observability) 확보가 가능해진다.

```text
+---------------------------------------------------------------------+
|            전통 모놀리식 On-Premise 아키텍처 vs Cloud-Native          |
+---------------------------------------------------------------------+
|                                                                     |
|  [On-Premise Monolithic]              [Cloud-Native Microservices]  |
|  +----------------------+             +------------------------+    |
|  |   Load Balancer (HW) |             |   Global LB / CDN      |    |
|  +----------+-----------+             |   (CloudFront/Akamai)  |    |
|             |                         +-----------+------------+    |
|  +----------v-----------+                         |                 |
|  |   WAS (WebLogic)     |             +-----------v------------+    |
|  |   +----------------+ |             |  API Gateway (Kong)    |    |
|  |   | Order | User   | |             +-----------+------------+    |
|  |   | Pay   | Stock  | |                         |                 |
|  |   +----------------+ |         +---------------+---------------+ |
|  |   Tomcat 5.x (단일)  |         |               |               | |
|  +----------+-----------+         v               v               v |
|             |              +---------+      +---------+      +---------+
|  +----------v-----------+  | Order   |      | User    |      | Payment |
|  |  Oracle RAC (Active) |  | Service |      | Service |      | Service|
|  |  + Standby           |  | (Pod×3) |      | (Pod×3) |      | (Pod×3)|
|  +----------+-----------+  +----+----+      +----+----+      +----+----+
|             |                   |                |                |    |
|  +----------v-----------+  +----v----+      +----v----+      +----v----+
|  |  SAN Storage         |  | RDS     |      |DynamoDB |      | Aurora  |
|  |  (FC-SAN, 10TB)      |  | (Multi- |      | (NoSQL) |      | (MySQL) |
|  +----------------------+  |  AZ)    |      +---------+      +---------+
|                            +----+----+                                 |
|                                 |         Service Mesh (Istio)        |
|  CapEx 5억 / 18개월 도입        |         +-----------------+          |
|  Peak 기반 35% 유휴             v         | mTLS, Retry,    |          |
|  HA 수동 4시간 다운       +----------+    | Circuit Breaker |          |
|                           | S3/Kafka |◄---+ Telemetry       |          |
|                           +----------+    +-----------------+          |
|                                                                     |
|                           OpEx 기반 / 5분 Provisioning               |
|                           Auto Scaling (HPA: 1->1000 Pod)            |
|                           Multi-AZ Auto-Healing (RTO < 60s)          |
+---------------------------------------------------------------------+
```

온프레미스 대비 클라우드 네이티브의 핵심 차별점은 **불변 인프라(Immutable Infrastructure)** + **선언적 구성(Declarative Configuration)**의 결합이다. 기존 Pet -> Cattle 패러다임 전환으로 VM/컨테이너를 1회 생성 후 폐기(Replace)하는 방식을 채택하여, Configuration Drift(설정 변동) 없이 동일 환경의 수평적 확장이 가능하다. CNCF(Cloud Native Computing Foundation) 2024年度报告에 따르면, 글로벌 Fortune 500 기업의 89%가 Kubernetes를 프로덕션 운영 중이며, 평균 컨테이너 배포 빈도는 주 2.3회 -> 일 12.7회(약 45배 증가)로 증가했다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 호텔의 객실처럼 필요할 때 즉시 예약하고, 체크아웃 시 원래 상태로 자동 복구되는 **"셀프 청소 호텔"**과 같다. 반면 전통적인 온프레미스는 손님이 직접 청소하고 관리하는 **"자택寄宿"**에 비유할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 네이티브 아키텍처의 4대 핵심 계층은 **① 인프라 계층(IaaS) -> ② 런타임 계층(Container/Orchestration) -> ③ 플랫폼 계층(Service Mesh/Serverless) -> ④ 애플리케이션 계층(Microservices/EDA)**으로 구성된다. 각 계층은 독립적으로 스케일링되며, API/Contract 기반의 느슨한 결합(Loose Coupling)으로 운영된다.

```text
+----------------------------------------------------------------------+
|         Cloud-Native 4-Layer Reference Architecture (C4 Model)       |
+----------------------------------------------------------------------+
|                                                                      |
|  [Layer 4: Application - Microservices / Serverless]                |
|  +-------------------------------------------------------------+    |
|  |  Order Service | Payment Service | Inventory | Notification |    |
|  |  (Spring Boot) | (Node.js)      | (Go)      | (Python)     |    |
|  |  REST/gRPC + Circuit Breaker (Resilience4j)                 |    |
|  +------+--------------+--------------+----------+-------------+    |
|         |              |              |          |                   |
|  [Layer 3: Service Mesh & API Gateway]                              |
|  +------v--------------v--------------v----------v-------------+    |
|  |  Istio Control Plane (Istiod)                                |    |
|  |  +----------+  +----------+  +------------+  +----------+  |    |
|  |  | mTLS     |  | Traffic  |  | Observab.  |  | Policy   |  |    |
|  |  | (SPIFFE) |  | Mgmt v2  |  | (Prometheus|  | (OPA)    |  |    |
|  |  |          |  | (Canary) |  |  + Jaeger) |  |          |  |    |
|  |  +----------+  +----------+  +------------+  +----------+  |    |
|  +-------------------------+------------------------------------+    |
|                            |                                          |
|  [Layer 2: Container Orchestration (Kubernetes)]                     |
|  +------------------------v------------------------------------+    |
|  |  +-------------+  +-------------+  +------------------+   |    |
|  |  | kube-apiserver|  | etcd (Raft) |  | kube-scheduler   |   |    |
|  |  | (3 Replica)  |  | Consensus   |  | Affinity/Taint   |   |    |
|  |  +-------------+  +-------------+  +------------------+   |    |
|  |  +-------------+  +-------------+  +------------------+   |    |
|  |  | kubelet     |  | kube-proxy  |  | CNI (Cilium)     |   |    |
|  |  | (CRI-O)     |  | (iptables/  |  | eBPF-based       |   |    |
|  |  |             |  |  IPVS)      |  | Networking       |   |    |
|  |  +-------------+  +-------------+  +------------------+   |    |
|  |  HPA: cpu > 70% -> Scale (30s interval)                     |    |
|  |  VPA: Memory Right-Sizing (Recommender)                    |    |
|  |  Cluster Autoscaler: Pending Pod -> New Node                |    |
|  |  PDB (PodDisruptionBudget): minAvailable: 2                 |    |
|  +-------------------------+------------------------------------+    |
|                            |                                          |
|  [Layer 1: Infrastructure (IaaS)]                                    |
|  +------------------------v------------------------------------+    |
|  |  Region (ap-northeast-2)                                     |    |
|  |  +-- AZ-a: Node Group (m6i.2xlarge × 5, Spot 60%)          |    |
|  |  +-- AZ-b: Node Group (m6i.2xlarge × 5, Spot 60%)          |    |
|  |  +-- AZ-c: Node Group (m6i.2xlarge × 5, On-Demand 40%)     |    |
|  |  Terraform/IaC -> Provider (AWS/GCP/Azure) -> State Locking   |    |
|  |  Karpenter: Just-in-Time Node Provisioning (90s)            |    |
|  +--------------------------------------------------------------+    |
|                                                                      |
|  [Cross-Cutting: Observability & Security]                           |
|  +--------------------------------------------------------------+    |
|  | Prometheus + Grafana + Loki (Logs) + Tempo (Traces)        |    |
|  | SLI/SLO: 99.95% Availability, p99 Latency < 200ms           |    |
|  | Error Budget: 0.05% × 30d = 216분 (Burn Rate Alert)        |    |
|  | Vault: Dynamic Secrets (PostgreSQL Role, AWS IAM)            |    |
|  +--------------------------------------------------------------+    |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Kubernetes Control Plane** | 클러스터 상태 관리 및 선언적 조정의 중추 | kube-apiserver(Etcd Frontend, REST API, RABC 인증), etcd(Raft 합의 알고리즘, Quorum 기반 분산 KV Store, WAL 2GB), kube-scheduler(Bin-packing, Affinity/Anti-Affinity, Taints/Tolerations, Topology Spread Constraints) |
| **Container Runtime & CNI** | 컨테이너 실행 및 Pod 네트워킹 | containerd/CRI-O(OCI 호환), Cilium(eBPF 기반 XDP, kube-proxy 대체, 30~40% Latency 절감), Calico(BGP 모드, Network Policy), Multus(Multiple Network Interface, SR-IOV/NVIDIA GPU) |
| **Service Mesh (Istio/Linkerd)** | East-West 트래픽 L7 제어, mTLS, 관찰가능성 | Envoy Sidecar(1.28 LTS, xDS API), Istiod(Pilot/Citadel/Galley 통합, SPIFFE/SPIRE 인증서 자동 로테이션 24h), Linkerd(Buoyant Rust Proxy, 2.14, Linkerd2-proxy 1ms P99 추가 지연), Ambient Mesh(Sidecar 제거, HBONE 터널) |
| **Serverless (FaaS/BaaS)** | 이벤트 기반 Stateless 컴퓨팅, Zero Scaling | AWS Lambda(15분 Timeout, 10GB Memory, 6 vCPU, SnapStart 200ms->30ms 콜드 스타트), Knative(Serving: 0->N Autoscaling, Eventing: CloudEvent 1.0), OpenFaaS(Cold Start 0.5s, K8s-native), Cloudflare Workers(V8 Isolates, 0ms 콜드 스타트) |
| **Infrastructure as Code (IaC)** | 인프라의 선언적 정의 및 GitOps 자동화 | Terraform 1.7+(HCL, State Locking via DynamoDB, Module Registry, Sentinel Policy as Code), Pulumi(General-purpose Language: TS/Python/Go), Crossplane(K8s CRD 기반, GitOps for Infra), AWS CDK(CloudFormation 추상화) |
| **Event Streaming & Message Bus** | 비동기 이벤트 전달, Pub/Sub, CQRS/Event Sourcing | Apache Kafka(KRaft 모드, ZooKeeper 제거, 3.6+, Partition 1MB/s, ISR 복제), AWS Kinesis(Data Streams/MSK Serverless), NATS JetStream(At-Least-Once, Exactly-Once), RabbitMQ 3.13(Quorum Queue, Streams) |
| **Observability Stack (3 Pillars)** | 메트릭, 로그, 트레이스 통합 | Prometheus(TSDB, PromQL, 14d 기본 보존, 30만 Series/노드), Grafana(Mimir 100× 확장, Loki LogQL), Jaeger/Tempo(OpenTelemetry OTLP, W3C TraceContext), eBPF/Pixie(Zero-Instrumentation Auto-Instrumentation) |
| **Zero Trust Security** | 신원 기반 접근, 최소 권한, 암호화 | SPIFFE/SPIRE(Workload Identity, 1년 Cert 자동 발급), OPA/Gatekeeper(Rego Policy, Admission Webhook), Vault(Transit Engine,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 793 / 800

<- **이전**: [792. 클라우드 아키텍처 핵심 토픽 792번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/792_cloud_architecture_core_topic_792_exam_summar/)
**다음**: [794. 클라우드 아키텍처 핵심 토픽 794번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/794_cloud_architecture_core_topic_794_exam_summar/) ->

---
