---
title: "656. 클라우드 아키텍처 핵심 토픽 656번 시험 요약 (Cloud Architecture Core Topic 656 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 온프레미스 데이터센터의 한계를 극복하기 위해 **탄력성(Elasticity)·확장성(Scalability)·내결함성(Fault Tolerance)**을 1급 시민(First-Class Citizen)으로 다루는 분산 시스템 설계 패러다임이며, 12-Factor App, 셀프서비스 프로비저닝(Self-Service Provisioning), API 기반 인프라(IaC)라는 세 가지 축으로 수렴한다.
> 2. **가치**: 동일 워크로드 대비 CapEx->OpEx 전환으로 TCO 30~60% 절감, Auto-Scaling을 통한 평균 자원 가용률 60%->85% 향상, 글로벌 멀티리전 구성 시 RTO 4시간->15분·RPO 1시간->수 분 단축, 개발자 생산성(Deployment Frequency) 약 200배·복구 시간(MTTR) 2,604배 개선(DORA 4대 지표 기준)이라는 정량적 가치를 제공한다.
> 3. **판단 포인트**: 5대 설계 결정 포인트 — (a) 단일 클라우드 vs 멀티/하이브리드, (b) Monolith->Microservice 분해 정당성(Conway's Law·Bounded Context), (c) Strong vs Eventual Consistency, (d) Stateless vs Stateful 컴포넌트 비율, (e) Egress 비용·Vendor Lock-in·Data Gravity를 고려한 워크로드 배치 — 가 동일 SLA·예산 하에서 Trade-off를 결정한다.

---

## Ⅰ. 개요 및 필요성

전통적 3-Tier 온프레미스 아키텍처는 **수직적 확장(Scale-Up) 한계**(Moore's Law 둔화, NUMA 노드 수의 HW 제약), **프로비저닝 리드타임**(서버 도입 8~12주, 네트워크 4주, SAN 스토리지 6주), **평균 서버 가용률 12~15%**(McKinsey 2014), **예측 불가능한 트래픽 폭주**(Black Friday·공인인증서 갱신 시즌 10배 Spike)라는 4대 구조적 결함을 내포한다. 2006년 AWS S3·EC2 출시 이후 IaaS, 2010년대 PaaS(Heroku·Cloud Foundry), 2014년 Lambda·Kubeless 등 FaaS로 진화하며 "**Infrastructure as Code + Immutable Infrastructure + Declarative API**"라는 새로운 운영 모델이 확립되었다.

특히 2020년 COVID-19 이후의 **Digital Transformation 가속**으로 컨테이너·오케스트레이션(Kubernetes, 2014년 Google 공개 -> 2015년 CNCF 설립), Service Mesh(Istio·Linkerd, 2017), GitOps(ArgoCD·Flux, 2018), eBPF 기반 Observability(Cilium, 2020)가 클라우드 네이티브 4계층(CNCF Landscape 기준: Provisioning -> Runtime -> Orchestration -> Application)을 완성했다. 기술사 관점에서는 단순 기술 도입이 아닌 **「비즈니스 연속성·규제 준수·비용 최적화」** 3축을 동시에 만족하는 아키텍처 결정을 내려야 한다.

```text
+---------------------------------------------------------------------+
|           On-Premise -> Cloud-Native 패러다임 전환 흐름              |
+---------------------------------------------------------------------+
|                                                                     |
|  [2000s] On-Premise 3-Tier         [2010s] Cloud IaaS/PaaS          |
|  +------------+                    +--------------------+           |
|  | Web/App/DB | ----VM Image---->   | EC2 / RDS / S3     |           |
|  | 물리서버   |      Migration     | Region/AZ 단위     |           |
|  +------------+                    +--------------------+           |
|         |                                  |                       |
|         | CapEx 100%                       | CapEx 30% + OpEx 70% |
|         | Provisioning 8주                 | Provisioning 5분     |
|         | 가용률 12%                       | 가용률 60%+          |
|                                                                     |
|  [2020s] Cloud-Native Stack                                            |
|  +----------------------------------------------------------------+|
|  | Layer 5: App   | Microservice / Serverless / SaaS              ||
|  | Layer 4: API   | GraphQL / gRPC / API Gateway                  ||
|  | Layer 3: Mesh  | Istio (mTLS, Circuit Breaker, Retry)         ||
|  | Layer 2: Orch. | Kubernetes (Control Plane + Worker Node)      ||
|  | Layer 1: Runtime| Container (Docker, containerd) / WASM        ||
|  | Layer 0: IaaS  | EC2 / GCE / Azure VM  (Immutable Infra)       ||
|  +----------------------------------------------------------------+|
+---------------------------------------------------------------------+
```

기존 LAMP 스택에서는 L(Load Balancer), A(Apache), M(MySQL), P(PHP)가 **모놀리식 + 수직확장**으로 결합되어 한 부분의 장애가 전체 장애로 전파되는 **God Server** 안티패턴이 빈번했다. 클라우드 아키텍처는 이를 **Bounded Context별 독립 배포 가능한 단위**로 분해하고, 각 단위가 **Stateless**로 동작하며, **Horizontal Pod Autoscaler(HPA)**·**Cluster Autoscaler(CA)**·**Karpenter**의 3단 오토스케일링이 트래픽 변동에 탄력적으로 대응하도록 한다.

- **📢 섹션 요약 비유**: 마치 한 대의 거대한 화물선(Monolith)을 **5,000개 TEU 표준 컨테이너(Microservice)**로 분해한 후, 수요에 따라 컨테이너를 즉시 투입·제거하는 **범선 자동화 시스템(Kubernetes)**에 실은 것과 같다. 배가 침몰해도 일부 컨테이너만 손실되고, 항구에서 즉시 새 컨테이너로 보충된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 5계층은 **Control Plane(제어)**과 **Data Plane(데이터)**이 분리된 **2-Plane Architecture**가 핵심이다. Control Plane은 사용자의 선언적 명세(YAML/JSON)를 실제 자원으로 매핑하고(Reconciliation Loop), Data Plane은 실제 트래픽을 처리한다. AWS 기준으로 Control Plane API(200 OK 응답)는 무료·비동기·Eventually Consistent이며, Data Plane API(실제 데이터)는 종량제·동기·Strong Consistent이다. 이 분리가 곧 **API 설계·비용·장애 도메인** 결정의 근간이 된다.

```text
+--------------------------------------------------------------------+
|      클라우드 아키텍처 핵심 5계층 + 2-Plane 분리 모델              |
+--------------------------------------------------------------------+
|                                                                    |
|  +----------------------- Control Plane ---------------------+     |
|  |  +------------+  +------------+  +------------+         |     |
|  |  |  Identity  |  | Orchestrator|  |   IaC      |         |     |
|  |  | (IAM/RBAC) |-> | (K8s API)  |<- | (Terraform)|         |     |
|  |  +------------+  +-----+------+  +------------+         |     |
|  |         |              | Desired State ↔ Actual State   |     |
|  +---------+--------------+---------------------------------+     |
|            |              |                                         |
|  +---------v--------------v-------- Data Plane -------------+      |
|  |  +----------+  +----------+  +----------+  +----------+ |      |
|  |  | Edge/CDN |-> | Gateway  |-> | Service  |-> | Storage  | |      |
|  |  |(CloudFront| |(Envoy/   | | Mesh     | | (S3/DDB) | |      |
|  |  |  Akamai) | | Kong)    | | (Istio)  | |          | |      |
|  |  +----------+  +----------+  +----------+  +----------+ |      |
|  |       |              |              |              |      |      |
|  |       v              v              v              v      |      |
|  |   TLS 1.3        mTLS SPIFFE    gRPC/HTTP2    Multi-AZ    |      |
|  |   QUIC/HTTP3     Rate-Limit     Circuit Br.   Erasure Cd. |      |
|  +----------------------------------------------------------+      |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IaC (Infrastructure as Code)** | 인프라의 선언적·버전관리·재현 가능한 프로비저닝 | Terraform(HCL 2.0, State Locking by DynamoDB), Pulumi(다국어 SDK), AWS CDK(Construct Tree), Ansible(YAML 절차적). Plan->Apply 2-Phase Commit, Drift Detection(주기적 Reconcile)으로 Configuration Drift 방지. |
| **Container Runtime** | 애플리케이션 + 의존성의 표준화된 격리 실행 단위 | OCI Spec 1.1 준수, Linux Namespace(pid/net/mnt/uts/ipc/user)+cgroup v2(자원 제한)+Seccomp(syscall 필터) 기반. containerd(2024년 OCI Runtime 표준), CRI-O, Podman(rootless). 이미지 레이어 합성(OverlayFS), Content Addressable Storage(SHA-256). |
| **Orchestrator (Kubernetes)** | 컨테이너의 선언적 배치·스케줄링·자가치유 | K8s 1.31 기준(2024), Control Plane 4 컴포넌트(`kube-apiserver`, `etcd[Raft]`, `kube-scheduler`, `kube-controller-manager`) + Worker Node 3 컴포넌트(`kubelet`, `kube-proxy`, `container runtime`). Pod(1~N 컨테이너) -> ReplicaSet -> Deployment -> Service(Ingress) 계층. PDB(PodDisruptionBudget) 0 표시 시 자가치유 보장. |
| **Service Mesh** | 서비스 간 통신의 mTLS·관측·트래픽 제어 분리 | Sidecar 패턴(Istio Envoy), Data Plane Proxy가 L7 라우팅·Circuit Breaker(연속 5회 실패 시 Open)·Retry(Exponential Backoff + Jitter)·Timeout(분산 추적 헤더 전파) 처리. SPIFFE/SPIRE 기반 Workload Identity. eBPF(Cilium) 모드는 Sidecar 제거로 30~50% Latency 절감. |
| **Observability Stack** | 메트릭·로그·트레이스의 3-Pillar 통합 관측 | Metrics(Prometheus pull model, PromQL, 5s scrape interval, OpenMetrics 1.0), Logs(Loki label-based index, LogQL), Traces(OpenTelemetry SDK, W3C TraceContext, Jaeger/Tempo). RED Method(Rate·Errors·Duration), USE Method(Utilization·Saturation·Errors). SLO 기반 Error Budget. |

**핵심 알고리즘 및 파라미터:**

1. **Consensus (Raft)**: K8s/etcd의 분산 합의 알고리즘. Leader Election(임의 Election Timeout 150~300ms) + Log Replication(과반수 Quorum = N/2+1) + Snapshot. 3-Node Quorum 기준으로 1대 장애 허용(F=1), 5-Node Quorum 기준 2대 허용(F=2)이나 Latency 증가. **Odd Number** 권장 이유는 Split-Brain 방지.
2. **Auto-Scaling 수식**: HPA Target = `desiredReplicas = ceil[currentReplicas × (currentMetricValue / targetMetricValue)]`. 예를 들어 CPU 80% 목표, 현재 30% 시 Replica 1/3로 축소, 200% 시 2.5배 확장. **Stabilization Window**(기본 5분)로 Flapping 방지.
3. **Consistent Hashing**: DynamoDB·Cassandra·Redis Cluster에서 사용. Virtual Node(VNode, 보통 1서버당 150~256개) 분배로 Key 재배치 최소화. **Ring Topology**에서 슬롯 단위 마이그레이션.
4. **CAP Trade-off**: 분산 시스템은 **Consistency** vs **Availability** vs **Partition Tolerance** 3개 중 2개만 만족 가능. **P는 필수**(네트워크 파티션은 피할 수 없으므로). CP 시스템(Etcd·ZooKeeper) vs AP 시스템(DynamoDB·Cassandra) 선택이 곧 아키텍처 결정.
5. **12-Factor App**: (1) Codebase(1 repo = 1 deployable), (2) Dependencies(Manifest 명시), (3) Config(환경변수 주입), (4) Backing Services(URL 추상화), (5) Build/Release/Run(3-stage 분리), (6) Processes(Stateless), (7) Port Binding(자체 서버), (8) Concurrency(Process Model), (9) Disposability(빠른 Startup/Shutdown), (10) Dev/Prod Parity, (11) Logs(Event Stream), (12) Admin Processes(1회성 작업).

- **📢 섹션 요약 비유**: 5계층 클라우드 아키텍처는 **고속도로 시스템**과 같다. (Layer 0) **노면**(물리 인프라), (Layer 1) **차선 표시선**(Container 경계), (Layer 2) **교차로 신호**(Orchestrator), (Layer 3) **톨게이트 운영원**(Service Mesh, 사고 감지·우회), (Layer 4) **내비게이션**(API Gateway, 경로 안내), (Layer 5) **택시·버스·트럭**(MSA·FaaS·SaaS) — Control Plane은 **교통관제센터(ATC)**이며 Data Plane은 **실제 차량이 달리는 도로**다. 도로와 관제센터가 분리되어야 정체와 사고의 영향이 최소화된다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처는 여러 트레이드오프의 교차점에 있다. 가장 빈번한 비교 축은 **Monolith vs Microservice**, **IaaS vs PaaS vs FaaS**, **Single Cloud vs Multi/Hybrid Cloud**이다.

| 구분 | **Monolithic Architecture** | **Microservice Architecture** |
| :--- | :--- | :--- |
| **배포 단위** | 1개 WAR/EAR 파일 또는 1개 Docker Image | 50~500개 독립 Service (Netflix 700+, Amazon 1,500+) |
| **확장 방식** | 수직 확장(Scale-Up, HW 한계 O) | 수평 확장(Scale-Out, HPA·Cluster Autoscaler) |
| **장애 도메인** | 전체 장애(Blast Radius 100%) | 부분 장애(Circuit Breaker로 격리, 1~5%) |
| **기술 스택** | 단일 언어/프레임워크 (예: Java/Spring) | Polyglot (Java·Go·Python·Node.js 혼재) |
| **데이터 관리** | 단일 DB, ACID Transaction | DB-per-Service, Saga Pattern, Eventual Consistency |
| **팀 구조** | 1~3팀 (Conway's Law: 1시스템 = 1팀) | 50~500팀 (Amazon "Two-Pizza Team" 6~10명) |
| **적합 사례** | MVP·도메인 불명확·팀 ≤ 10명·트래
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 656 / 800

<- **이전**: [655. 클라우드 아키텍처 핵심 토픽 655번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/655_cloud_architecture_core_topic_655_exam_summar/)
**다음**: [657. 클라우드 아키텍처 핵심 토픽 657번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/657_cloud_architecture_core_topic_657_exam_summar/) ->

---
