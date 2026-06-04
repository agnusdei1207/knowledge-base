---
title: "538. 클라우드 아키텍처 핵심 토픽 538번 시험 요약 (Cloud Architecture Core Topic 538 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 컨테이너 오케스트레이션(Kubernetes), 서비스 메시(Istio/Linkerd), IaC(Terraform/CloudFormation), GitOps(ArgoCD/Flux) 기반의 **Cloud Native Computing Foundation(CNCF) 12-Factor App 원칙**을 토대로, 무중단·탄력적·관측가능(Observability)한 분산 시스템을 설계하는 것.
> 2. **가치**: Auto Scaling Group을 통해 트래픽 변동에 10초 내 응답(On-Demand vs Reserved Instances로 60~72% 비용 절감), Multi-AZ/Region 구성으로 가용성 **99.99%(Four-Nines, 연 52.6분 이내 장애)** 달성, MTTR을 기존 대비 70% 단축하는 SRE 관점의 운영 효율성 확보.
> 3. **판단 포인트**: Lift & Shift(Rehost) vs Replatform vs Refactoring 간의 TCO 비교, 단일 클라우드 종속(Vendor Lock-in) 회피를 위한 **Abstraction Layer(Strimzi, Crossplane, Terraform)** 채택 여부, Well-Architected Framework 5대 축(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화) 별 트레이드오프 결정.

---

## Ⅰ. 개요 및 필요성

전통적 3-Tier On-Premise 아키텍처는 **CAPEX(자본 지출)**, **프로비저닝 리드타임(주 단위)**, **수직적 확장(Scale-Up)의 한계(HW 物理적 한계)**, 그리고 **수동 장애 대응(Manual Failover)**이라는 구조적 한계를 가진다. 2006년 AWS S3·EC2 출시 이후 IaaS -> PaaS -> SaaS -> FaaS(Serverless)로 진화하며, **IDC(2024) 기준 전 세계 퍼블릭 클라우드 시장이 약 6,790억 달러**로 확대되었고, 국내 또한 2025년 35조 원 규모로 성장할 전망이다(한국IDC 2024).

```text
+------------------------------------------------------------------+
|        클라우드 아키텍처 진화 패러다임 (Evolution Timeline)      |
+------------------------------------------------------------------+

[1세대: 2006~]      [2세대: 2010~]      [3세대: 2014~]      [4세대: 2018~]
  IaaS                 PaaS              CaaS/FaaS         Cloud Native
  -----                -----             ----------         ------------
+--------+          +--------+         +---------+       +-------------+
| EC2    |          |BeanStk |         | K8s     |       | Knative     |
| S3     |   ---►   | Heroku |   ---►  | Docker  | ---►  | Istio       |
| VPC    |          | GAE    |         | Lambda  |       | ArgoCD      |
+--------+          +--------+         +---------+       | Crossplane  |
   |                    |                  |             +-------------+
   v                    v                  v                    |
  VM 단위             App 단위          Container 단위           v
  Provisioning        Deploy            Orchestration      GitOps+Mesh
  (수동)              (반자동)          (자동)             (Self-Healing)

핵심 변화: HW 抽象化 -> OS 抽象化 -> Runtime 抽象化 -> Infrastructure 抽象化
```

**왜 클라우드 아키텍처가 필수인가?**

- **탄력성(Elasticity)**: EKS·GKE·AKS의 **Cluster Autoscaler** + **HPA(Horizontal Pod Autoscaler)** + **KEDA(Event-driven Autoscaling)** 3단 오토스케일링으로, CPU 70%·메모리 80%·Kafka Lag 1000건 등 커스텀 메트릭 기반 동적 확장.
- **불변 인프라(Immutable Infrastructure)**: Packer·AMI·Golden Image 방식으로 배포 시점 스냅샷을 보존, **Configuration Drift**를 원천 차단하여 "Snowflake Server" 문제를 해결.
- **관측 가능성(Observability)**: OpenTelemetry(OTel) 기반 **3대 신호(Metrics-Prometheus, Logs-Loki/EFK, Traces-Jaeger/Tempo)** 통합으로 분산 시스템의 인과관계(Causality) 추적.
- **장애 도메인 격리**: AWS의 **Region(27개) -> AZ(2~6개) -> Subnet -> Security Group** 4계층 격리 모델.

- **📢 섹션 요약 비유**: 전통 인프라가 "매번 청소를 하고 재배치하는 자취방"이라면, 클라우드 아키텍처는 **"이삿짐센터가 갖춰진 호텔 체인"** — 손님(트래픽)이 몰리면 객실(컨테이너)을 즉시 늘리고, 문제가 생긴 객실은 자동 청소 후 신선한 방으로 즉시 교체해준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 네이티브 아키텍처는 **CNI(Container Network Interface) + Service Mesh + IaC + GitOps** 4계층으로 구성되며, 각 계층은 명확한 책임 분리(SoC, Separation of Concerns)를 따른다.

```text
+---------------------------------------------------------------------+
|            Cloud Native 4-Tier Reference Architecture              |
+---------------------------------------------------------------------+

  Layer 0: Governance & Policy
  +-----------------------------------------------------------------+
  | OPA(Open Policy Agent) | Kyverno | Falco(Runtime Security)      |
  | SBOM(Syft) | Sigstore(Cosign Signing)                            |
  +-----------------------------------------------------------------+
                              ^ Policy as Code
  Layer 1: Developer Experience (GitOps)
  +-----------------------------------------------------------------+
  |  Git Repo --► ArgoCD / Flux --► Sync --► Cluster               |
  |  (Argo Rollouts: Blue/Green, Canary, A/B Testing)               |
  +-----------------------------------------------------------------+
                              ^ Declarative
  Layer 2: Orchestration (Kubernetes)
  +-----------------------------------------------------------------+
  |  kube-apiserver | etcd(RAFT 합의) | kube-scheduler              |
  |  kubelet | kube-proxy(CNI: Calico/Cilium)                       |
  |  CoreDNS | Ingress Controller(NGINN/Contour/Traefik)            |
  +-----------------------------------------------------------------+
                              ^ Container Runtime
  Layer 3: Runtime & Service Mesh
  +-----------------------------------------------------------------+
  |  containerd | CRI-O | gVisor/Kata(보안 샌드박스)                |
  |  Istio(Envoy Sidecar) | Linkerd | Cilium Service Mesh           |
  |  mTLS 자동화 | Circuit Breaker | Retry/Timeout 정책              |
  +-----------------------------------------------------------------+
                              ^ Service Abstraction
  Layer 4: Application (12-Factor + Microservices)
  +-----------------------------------------------------------------+
  |  API Gateway(Kong/Ambassador) | Service Registry                |
  |  Event Bus(Kafka/NATS/EventBridge) | Saga/CQRS/Outbox 패턴      |
  |  BFF(Backend-For-Frontend) | Strangler Fig Pattern              |
  +-----------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Kubernetes Control Plane** | 클러스터 상태 관리·조정의 두뇌 | `kube-apiserver`가 유일한 Stateless Gateway, `etcd` RAFT 합의로 분산 일관성 보장, `kube-scheduler`는 **Filter(예: NodeAffinity, Taints) -> Score(예: LeastAllocated, BalancedResource)** 2단계 알고리즘으로 Pod 배치 |
| **Service Mesh (Istio)** | L7 트래픽 관리·보안·관측 | Envoy Sidecar가 **1,000+ RPS** 처리, **istiod**가 xDS API로 CDS·EDS·LDS·RDS 푸시, **mTLS SPIFFE** 기반 Workload Identity, **VirtualService**(라우팅) + **DestinationRule**(트래픽 분할)로 Canary 배포 |
| **Infrastructure as Code (Terraform)** | 멀티 클라우드 인프라 선언적 프로ビジョ닝 | HCL(HashiCorp Configuration Language)로 **Plan -> Apply** 2단계 검증, **State Lock(DynamoDB/Raft)** 로 동시성 제어, **Module Registry**로 재사용, OpenTofu/Pulumi 대안 존재 |
| **GitOps Controller (ArgoCD)** | Git Repository -> Cluster 자동 Sync | **Pull 방식**(보안 우위): ArgoCD가 Cluster 내부에서 Git을 감시, **ApplicationSet**으로 멀티 클러스터/멀티 환경 관리, **Sync Wave**(순서) + **Hook**(Pre/Post Sync)로 마이그레이션 자동화 |

**Kubernetes Scheduling 알고리즘 핵심 공식** (기술사 빈출):

```text
Total Score = (NodeAffinity * 1) + (LeastAllocated * 2) + (TaintToleration * 1)
              -------------------------------------------------
              노드 스코어링(0~100점) 후 최고 점수 노드에 Pod 배치

Bin Packing 모드: MostAllocated (자원 밀집 -> 노드 수 최소화 -> 비용v)
Spread 모드:      LeastAllocated (자원 분산 -> 장애 도메인 격리^)

HPA 공식:
  desiredReplicas = ceil[ currentReplicas × (currentMetricValue / targetMetricValue) ]
  예: 현재 10 Pod, CPU 90% 사용, 목표 60% -> ceil(10 × 90/60) = 15 Pod
```

**탄력적 스케일링 3단계** (EKS 기준 실무 패턴):

```text
[사용자 트래픽] --► [ALB/NLB] --► [Ingress]
                                    |
              +---------------------+---------------------+
              v                     v                     v
      [HPA: Pod 단위]      [KEDA: Event 단위]     [CA: Node 단위]
      CPU/Mem 70%         Kafka Lag, SQS Depth  Pending Pod 발생 시
      30초 주기           Cron, Prometheus        Karpenter로 Spot 인스턴스
                                                   즉시 프로비저닝(45초)
```

- **📢 섹션 요약 비유**: Kubernetes는 **"오케스트라의 지휘자"** — 바이올린(파드)·첼로(노드)·트럼펫(서비스)이 각자 다른 악보를 연주할 때, **지휘자(Control Plane)가 템포(스케줄링)와 하모니(리소스 균형)를 맞춰 하나의 교향곡(서비스)을 만들어내는 것**이며, Service Mesh는 무대 위의 **"이어피스(이어모니터링+자동조정)"** 역할을 한다.

---

## Ⅲ. 비교 및 연결

### 비교 1: 클라우드 배포 모델 3종 + 비교

| 구분 | Public Cloud | Private Cloud | Hybrid Cloud |
| :--- | :--- | :--- | :--- |
| **소유/운영** | AWS·Azure·GCP 등 CSP | 자체 DC 또는 Hosted Private | Public + Private 연결 |
| **확장성** | 무제한(수 분 내 수천 VM) | 물리적 HW 한도 | Burst 시 Public 활용 |
| **초기 비용** | CAPEX 거의 0, OPEX 종량 | CAPEX 높음(수십억) | 양쪽 혼합 |
| **보안/규제** | CSP 책임분담 모델, 격리 수준 B | 금융/공공 규제 우위(전 구간 통제) | 데이터 분류별 배치(메타데이터=Public, PII=Private) |
| **연결 기술** | Internet / Direct Connect / ExpressRoute / Interconnect | 전용선, VPC Peering | **AWS Outposts**, **Azure Arc**, **Google Anthos** |
| **적합 사례** | 스타트업, 글로벌 SaaS | 금융·공공·제조(데이터 주권) | 클라우드 마이그레이션 과도기, AI 학습(Public)+Inference(Private) |

### 비교 2: 마이크로서비스 통신 패턴 (동기 vs 비동기)

| 구분 | REST API (동기) | gRPC (동기) | Kafka/EventBridge (비동기) |
| :--- | :--- | :--- | :--- |
| **프로토콜** | HTTP/1.1, JSON | HTTP/2, Protobuf(2~10배 빠름) | AMQP 0.9.1, Kafka Protocol |
| **레이턴시** | 20~50ms | 5~15ms | 1~5ms(Pub) / 비동기 응답 |
| **결합도** | 높음(서비스 Down 시 Cascade) | 중간(재시도·타임아웃 필요) | **낮음(Eventual Consistency)** |
| **적합 사례** | BFF, 관리자 API | MSA 내부·고성능 RPC | 결제·주문 Saga, CDC, IoT 수집 |
| **장애 전파** | Circuit Breaker 필수(Hystrix->Resilience4j) | Retry + Hedging(병렬 호출, 첫 응답 채택) | DLQ(Dead Letter Queue) + Replay |

### 비교 3: 컨테이너 오케스트레이션 (Kubernetes vs Docker Swarm vs Nomad)

| 구분 | Kubernetes (CNCF) | Docker Swarm | HashiCorp Nomad |
| :--- | :--- | :--- | :--- |
| **생태계** | 88개 CNCF 프로젝트과 통합 | Docker 엔진 종속 | Consul·Vault와 자연 통합 |
| **학습 곡선** | 가파름(YAML 200+ 라인) | 완만 | 중간 |
| **스케줄링** | 정교(예약·亲和성·Taint) | 단순(Raft 합의) | Bin Packing 우수 |
| **적합 규모** | 1,000+ 노드 | 50 노드 이하 | 100~500 노드 |
| **프로덕션 사례** | Google(GKE), Spotify, Airbnb | 소규모/내부 도구 | Cloudflare, PagerDuty |

**다른 시스템과의 연결 (Integration Map):**

- **DevOps 파이프라인**: GitLab/GitHub -> **Tekton/Argo Workflows** (CI) -> **Harbor** (Image Registry) -> **ArgoCD** (CD)
- **관측(Observability)**: Prometheus -> **Thanos/Mimir** (장기 저장) -> Grafana, **Loki**(로그), **Tempo**(트레이스) -> **Datadog/New Relic**(SaaS APM)
- **보안(Security)**: Trivy·Snyk(취약점 스캔) -> **OPA/Gatekeeper**(Admission Control) -> **Falco**(런타임 이상 행위) -> **Wiz/Lacework**(CSPM)
- **비용 최적화**: **Kubecost** + **Cloudability** + AWS Cost Explorer -> FinOps 실무 -> Spot Instance + Savings Plans(72%v) + S3 Intelligent-Tiering
- **데이터 계층**: OLTP(**Aurora Serverless v2**, **Spanner**) + 분석(**Snowflake**, **BigQuery**, **Redshift Spectrum**) + 실시간(**Apache Flink**, **Materialize**)

- **📢 섹션 요약 비유**: Public Cloud는 **"해외여행 중 체인 호텔 투숙"**(즉시入住, 가성비^), Private Cloud는 **"자택 요리"**(완전 통제, 초기 비용^), Hybrid Cloud는 **"주말에는 자택, 평일에는 호텔"** — 각각의 장점을
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 538 / 800

<- **이전**: [537. 클라우드 아키텍처 핵심 토픽 537번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/537_cloud_architecture_core_topic_537_exam_summar/)
**다음**: [539. 클라우드 아키텍처 핵심 토픽 539번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/539_cloud_architecture_core_topic_539_exam_summar/) ->

---
