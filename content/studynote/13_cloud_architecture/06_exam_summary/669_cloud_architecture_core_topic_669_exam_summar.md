---
title: "669. 클라우드 아키텍처 핵심 토픽 669번 시험 요약 (Cloud Architecture Core Topic 669 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 API-driven 자원 추상화(IaaS/PaaS/SaaS/FaaS)와 컨테이너 오케스트레이션(Kubernetes, Service Mesh) 기반의 12-Factor, Cloud-Native 원칙을 통해 탄력성(Elasticity), 무중단(Zero-Downtime), 관찰가능성(Observability)의 3대 품질속성을 보장하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: CapEx->OpEx 전환으로 TCO 30~60% 절감, Auto-Scaling으로 Peak 트래픽 대비 70% 이상 비용 최적화, Multi-AZ/Region 구성으로 RTO 분 단위, RPO 초 단위 달성, 개발 배포 주기(DORA Lead Time) 80% 단축 효과가 입증되었다.
> 3. **판단 포인트**: 워크로드 특성(I/O Bound vs CPU Bound, Stateful vs Stateless)에 따른 Compute 모델(VM vs Container vs Serverless) 선정, 데이터 일관성 모델(Strong/Eventual/Causal), CAP/ PACELC 이론 기반의 분산 트레이드오프, Shared Responsibility Model 하의 보안 경계 설정이 핵심 의사결정 사항이다.

---

## Ⅰ. 개요 및 필요성

전통적 On-Premise 3-Tier 아키텍처는 CAPEX 기반의 수직적 확장(Scale-Up), 정적 스펙 산정, Monolithic 배포, 수동 페일오버라는 구조적 한계로 인해 ① 트래픽 변동성 대응 실패(Black Friday, COVID-19 사례), ② 재해복구 RTO 24시간 이상, ③ 자원 활용률 10~15% 수준, ④ 신규 비즈니스 출시 6개월~1년 소요라는 4대 고통포인트(Pain Point)를 야기한다. Gartner(2023) 보고서에 따르면 글로벌 Enterprise의 85%가 이미 클라우드 우선(Cloud-First) 전략을 채택하였으며, IDC는 2027년 Public Cloud 시장 규모가 1.5조 USD에 이를 것으로 전망한다.

클라우드 아키텍처는 2006년 AWS S3/EC2 출시 이후 IaaS 시대(2006~2010) -> PaaS 시대(2011~2015: Heroku, Cloud Foundry) -> CaaS/Container 시대(2015~2020: Docker/K8s, Istio) -> Serverless/Edge 시대(2020~현재: Lambda, Cloudflare Workers)로 진화해 왔다. 특히 CNCF(Cloud Native Computing Foundation)가 제시한 Cloud-Native 4대 축(Containers, Orchestration, Microservices, Serverless)은 현대 분산 시스템 설계의 표준이 되었다.

```text
+-----------------------------------------------------------------------------+
|                클라우드 아키텍처 패러다임 전환 (Paradigm Shift)              |
+-----------------------------------------------------------------------------+
|                                                                             |
|  [On-Premise Monolithic] ---------> [Cloud-Native Distributed]               |
|                                                                             |
|   +----------+  +----------+  +----------+    +------+  +------+  +------+|
|   |  Web     |  |   App    |  |    DB    |    | Svc-A|  | Svc-B|  | Svc-C||
|   |  Tier    |--|  Tier    |--|  (RDBMS) |    |Pod×N |  |Pod×N |  |Pod×N ||
|   +----------+  +----------+  +----------+    +------+  +------+  +------+|
|        |             |             |              |         |         |    |
|   +-------------------------------------+    +-----+---------+--------+    |
|   |  Vertical Scale-Up (CPU/Memory ^)   |    |  Horizontal Scale-Out (Pod+)|
|   |  Provisioning: 2~4 weeks            |    |  Provisioning: 30 seconds  |
|   |  Utilization: 10~15%                |    |  Utilization: 60~80%       |
|   |  HA: Active-Passive (Manual)        |    |  HA: Active-Active (Auto)  |
|   +-------------------------------------+    +-----------------------------+ |
|                                                                             |
|   Traffic -+   +- CapEx (고정)                       +- CapEx -> OpEx (변동) |
|            |   |                                       |                    |
|            v   v                                       v                    |
|   ████████████████                                          ░░░░░░░░░░░░░░  |
|   ████████████████  (과다 provisioning)                   ░░░░░░░░░░░░░░  |
|   ████████████████  (유휴 자원 낭비)                      ░░░░░░░░░░░░░░  |
|                                                                             |
+-----------------------------------------------------------------------------+
```

클라우드 네이티브로의 전환이 필요한 본질적 이유는 ① **탄력성(Elasticity)**: HPA/VPA/Cluster Autoscaler 기반 자동 스케일링, ② **회복탄력성(Resilience)**: Chaos Engineering(LitmusChaos, Gremlin), Circuit Breaker, Bulkhead 패턴, ③ **관찰가능성(Observability)**: OpenTelemetry 기반 3 Pillars(Metrics/Logs/Traces), ④ **자동화(Automation)**: GitOps(ArgoCD/Flux), IaC(Terraform/Pulumi) 때문이다.

- **📢 섹션 요약 비유**: On-Premise가 "직접 짓고 관리하는 단독주택"이라면, Cloud-Native는 "필요한 방을 1분 단위로 빌리고 반납하는 호텔 체인"과 같다. 호텔은 체크인/체크아웃이 자동화되어 있고, 투숙객 수에 따라 즉시 층을 추가 개방한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **Edge -> API Gateway -> Service Mesh -> Microservices -> Stateful Workload -> Observability/Governance**의 7계층 참조모델(Reference Model)로 구성된다. 각 계층은 독립적으로 진화 가능하며, CNCF Landscape(2024 기준 1,000+ 프로젝트)가 이를 뒷받침한다.

```text
+------------------------------------------------------------------------------+
|           Cloud-Native 7-Layer Reference Architecture (CNCF 기반)            |
+------------------------------------------------------------------------------+
|                                                                              |
|  +-----------------------------------------------------------------------+  |
|  | Layer 1: Edge & Delivery  (CloudFront, Cloudflare, Fastly, Akamai)    |  |
|  |  - CDN Caching, WAF, DDoS Protection, Edge Functions(Workers/Lambda@E)|  |
|  +--------------------------------+--------------------------------------+  |
|                                   v                                          |
|  +-----------------------------------------------------------------------+  |
|  | Layer 2: API Gateway & BFF  (Kong, Apigee, AWS API GW, GraphQL)      |  |
|  |  - Rate Limiting(Lua/Wasm), OAuth 2.0/OIDC, Schema Validation        |  |
|  +--------------------------------+--------------------------------------+  |
|                                   v                                          |
|  +-----------------------------------------------------------------------+  |
|  | Layer 3: Service Mesh & Ingress  (Istio, Linkerd, Envoy, Consul)     |  |
|  |  - mTLS(SPIRE), Traffic Mgmt(Canary/Blue-Green), Retry/Timeout       |  |
|  +--------------------------------+--------------------------------------+  |
|                                   v                                          |
|  +-----------------------------------------------------------------------+  |
|  | Layer 4: Orchestration  (Kubernetes 1.30+, K3s, EKS/AKS/GKE, Nomad)  |  |
|  |  - Control Plane: kube-apiserver, etcd, scheduler, controller-mgr    |  |
|  |  - Data Plane: kubelet, kube-proxy, CRI(runc/containerd)             |  |
|  +--------------------------------+--------------------------------------+  |
|                                   v                                          |
|  +-----------------------------------------------------------------------+  |
|  | Layer 5: Workload & Runtime  (Pod, Deployment, StatefulSet, Job/Cron) |  |
|  |  - Sidecar(Envoy), Init Container, HPA(v2: CPU/Mem/Custom), PDB      |  |
|  +--------------------------------+--------------------------------------+  |
|                                   v                                          |
|  +-----------------------------------------------------------------------+  |
|  | Layer 6: Stateful & Data  (PostgreSQL/RDS, Redis/ElastiCache,        |  |
|  |  Kafka/MSK, S3/MinIO, DynamoDB, CockroachDB, Snowflake)              |  |
|  |  - StorageClass(GP3/IO2), CSI Driver, Velero Backup                  |  |
|  +--------------------------------+--------------------------------------+  |
|                                   v                                          |
|  +-----------------------------------------------------------------------+  |
|  | Layer 7: Observability & Governance (Prometheus, Grafana, Loki,      |  |
|  |  Tempo, Jaeger, OpenTelemetry, Falco, OPA/Gatekeeper, ArgoCD)        |  |
|  |  - SLO/SLI, Error Budget, GitOps Sync                                 |  |
|  +-----------------------------------------------------------------------+  |
|                                                                              |
+------------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Kubernetes Control Plane** | 클러스터 두뇌, 선언적 상태 관리 | kube-apiserver(요청 검증), etcd(Raft 합의, 5MB/Object 한계), scheduler(Filter+Score 2단계), controller-manager(Reconcile Loop, 기본 30s), cloud-controller-manager(Cloud Provider 연동) |
| **Pod & Container Runtime** | 최소 배포 단위, 격리 실행 | 1Pod=1~N Container, 공유 Network/UTS/IPC 네임스페이스, cgroup v2로 CPU/Memory 제한, OCI 표준(containerd 1.7+, CRI-O, runC), kata-runtime로 VM급 격리 |
| **Service Mesh (Istio)** | L7 트래픽 제어, Zero-Trust 보안 | Envoy Sidecar(iptables init으로 트래픽 가로채기), xDS API로 동적 설정, mTLS 1.3 + SPIFFE ID, Telemetry v2(Stat-Push), WASM/EnvoyFilter로 확장 |
| **API Gateway** | 외부 진입점, 횡단 관심사 | OAuth 2.0 PKCE 플로우, JWT 검증(RS256+JWK 캐시), Rate Limiting(Token Bucket/Lua), Schema Validation(OpenAPI 3.1/JSON Schema), GraphQL Federation |
| **Observability (OpenTelemetry)** | 3 Pillars 통합 수집 | OTLP 프로토콜(gRPC/HTTP+Protobuf), Trace Context(W3C Traceparent), Resource Detection(Cloud Metadata), Tail-based Sampling, Cardinality Limitation |
| **Stateful Storage (Operator 패턴)** | 상태ful 워크로드 관리 | StatefulSet(Stable Network ID: pod-0~N), PVC 동적 프로비저닝(StorageClass), Operator SDK(CRD+Reconcile), 예: postgres-operator, Strimzi(Kafka) |
| **GitOps Engine (ArgoCD/Flux)** | 선언적 지속적 배포 | Pull-based 모델(클러스터->Git Polling 3분), Application CRD, Sync Wave 의존성, Kustomize/Helm 랜더링, Drift Detection, App-of-Apps 패턴 |

핵심 동작 메커니즘으로 **Kubernetes Reconciliation Loop**를 이해해야 한다. 사용자가 `kubectl apply`로 desired state(ReplicaSet=3)를 선언하면, kube-apiserver는 etcd에 저장하고, ReplicaSet Controller가 watch 루프(기본 5s, jitter 포함)로 현재 상태(2 Pods)와 비교하여 Diff를 감지하면 신규 Pod 1개를 스케줄링한다. kube-scheduler는 Node Affinity, Taints/Tolerations, Resource Requests, Topology Spread Constraints를 평가하여 최적 노드를 선정하고, kubelet이 CRI(Container Runtime Interface) 호출을 통해 containerd로 컨테이너를 기동한다.

```text
+----------------------------------------------------------------------+
|         Kubernetes Reconciliation Loop (Declarative State Mgmt)    |
+----------------------------------------------------------------------+
|                                                                      |
|   User ---> kubectl apply -f deployment.yaml                         |
|              |                                                       |
|              v (spec.replicas: 3)                                   |
|   +----------------------+                                           |
|   | kube-apiserver       |  ---- etcd put (desired state)            |
|   | (authn, authz,       |                                           |
|   |  admission: OPA)     |                                           |
|   +----------+-----------+                                           |
|              |                                                       |
|              v (Watch: Deployment)                                  |
|   +----------------------+    Compare: actual=2 vs desired=3         |
|   | Deployment Controller| --------------------------+               |
|   | (control-loop)       |                           |               |
|   +----------+-----------+                           v               |
|              | (Update)                +------------------------+   |
|              v                         | ReplicaSet (rs-abc123) |   |
|   +----------------------+             | spec.replicas=3        |   |
|   | ReplicaSet Controller|             +----------+-------------+   |
|   | (Loop Period 30s)    |                        |                 |
|   +----------+-----------+                        v (Watch)         |
|              | (Create Pod)         +--------------------------+    |
|              v                      | ReplicaSet Controller    |    |
|   +----------------------+          | status.replicas=2 -> 3    |    |
|   | kube-scheduler       |          +----------+---------------+    |
|   | 1. Filter (Predicates)|                    |                    |
|   |    - NodeAffinity     |                    v                    |
|   |    - Taints/Tolerations                  (Create Pod Object)  |
|   |    - PodFitsHost       |                                           |
|   | 2. Score (Priorities) |                                           |
|   |    - LeastAllocated    |                                           |
|   |    - BalancedResource  |                                           |
|   |    - TopologySpread    |                                           |
|   +----------+-----------+                                           |
|              | (Bind)                                                 |
|              v                                                        |
|   +----------------------+    +------------------------------+       |
|   | kubelet (Node-2)     |---->| CRI: containerd -> runC       |       |
|   | - Pod Spec Sync      |    | - cgroup: cpu=500m, mem=512Mi|       |
|   | - Probe: Liveness/   |    | - Network: CNI (Cilium)      |       |
|   |   Readiness/Startup  |    | - Volume: CSI Mount          |       |
|   | - cAdvisor Metrics   |    |   /var/lib/kubelet/pods/...  |       |

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 669 / 800

<- **이전**: [668. 클라우드 아키텍처 핵심 토픽 668번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/668_cloud_architecture_core_topic_668_exam_summar/)
**다음**: [670. 클라우드 아키텍처 핵심 토픽 670번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/670_cloud_architecture_core_topic_670_exam_summar/) ->

---
