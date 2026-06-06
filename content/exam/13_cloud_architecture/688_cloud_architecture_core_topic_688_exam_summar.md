---
title: "Cloud Architecture Core Topic 688 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS의 책임공유 모델 위에서 12-Factor App, 마이크로서비스, 이벤트드리븐, 서버리스, 컨테이너 오케스트레이션(Kubernetes/Service Mesh) 패턴을 결합해 탄력성·장애격리·자동확장·관측가능성(Observability)을 코드와 인프라로 동시에 구현하는 분산시스템 설계 패러다임이다.
> 2. **가치**: Well-Architected 5대 축(운영우수, 보안, 안정성, 성능효율, 비용최적화) 점수화에 따라 일반적으로 배포빈도 200%^, MTTR 60%v, 인프라 비용 30~40%v, 가용성 99.95->99.99% SLA 전환 효과가 검증되며, AWS Well-Architected Labs 기준 약 250개 이상의 LQR(Linked Quick Reference) 패턴으로 표준화되어 있다.
> 3. **판단 포인트**: 단일장애점(SPOF) 제거와 분산 트랜잭션(Saga/Outbox), CAP定理 기반의 일관성-가용성 트레이드오프, FinOps 도입 시점(예산 대비 20% 이상 클라우드 사용 시), 멀티클라우드 vs 하이브리드(데이터중심 vs 워크로드중심), EKS/AKS/GKE vs 자체 Kubernetes on EC2 운영 모델 선택이 핵심 의사결정 기준이다.

---

## Ⅰ. 개요 및 필요성

전통적 3-Tier 모놀리식 아키텍처(웹-앱-DB)는 수직확장(Scale-Up) 한계, 야간 배포, 장애의 연쇄 전파, CAPEX 중심의 용량 계획, 18~36개월 갱신주기로 인해 디지털 트랜스포메이션 요구사항을 충족하지 못한다. Gartner(2023) 기준 전 세계 기업의 85%가 클라우드 퍼스트 전략을 선언했고, IDC는 2027년 전 세계 퍼블릭클라우드 지출이 1.35T USD에 이를 것으로 전망한다. 이에 따라 클라우드 아키텍처는 "하드웨어 추상화"에서 "운영 모델과 조직문화의 재설계"로 패러다임이 이동했다.

```text
[전통 모놀리식 vs 클라우드 네이티브 진화]
+--------------------------+      +--------------------------+
|   Monolithic 3-Tier      |      |   Cloud-Native Stack     |
| +----------------------+ |      | +----------------------+ |
| |  LB (F5, L4/L7)     | |      | |  CDN/Edge (CloudFront| |
| +----------------------+ |      | |  /Cloudflare/CloudCDN| |
| +----------------------+ |  ->   | +----------------------+ |
| |  Web (Tomcat/IIS)    | |      | +----------------------+ |
| |  App (WAS)           | |      | |  API GW (Kong,AWS    | |
| |  DB (Oracle RAC)     | |      | |  Apigw,Ambassador)   | |
| +----------------------+ |      | +----------------------+ |
|  Scale-Up, 수동 배포      |      |  +--------------------+  |
|  라이센스 종속(Lock-in)   |      |  | Svc Mesh (Istio/   |  |
+--------------------------+      |  | Linkerd/Consul)    |  |
                                  |  +--------------------+  |
                                  | +----------------------+ |
                                  | | K8s (EKS/AKS/GKE/   | |
                                  | | OpenShift) + Helm    | |
                                  | +----------------------+ |
                                  | +----------------------+ |
                                  | | Observability(Prom/  | |
                                  | | Grafana/Loki/OTel)   | |
                                  | +----------------------+ |
                                  |  Scale-Out, GitOps 자동화 |
                                  |  OpenAPI/CloudEvents 표준|
                                  +--------------------------+
```

핵심 변화는 (1) 불변 인프라(Immutable Infrastructure)와 IaC(Terraform/CloudFormation/Pulumi)로 구성된 **GitOps 루프**, (2) 컨테이너와 서비스메시로 구현된 **폴리글랏 런타임**, (3) SRE/SLI/SLO/Error Budget로 운영되는 **엔지니어링 중심 운영 모델**, (4) FinOps로 코드로 통제되는 **비용 거버넌스**의 4가지 축이다.

- **📢 섹션 요약 비유**: 기존 3-Tier가 백화점 1개 동이라면, 클라우드 네이티브는 백화점 본관 옆에 매일 새 팝업스토어(컨테이너)를 GitHub에 PR 올리면 3분 만에 자동으로 세우는 것과 같다. 손님(트래픽)이 몰리면 옆에 똑같은 팝업을 더 짓고(오토스케일), 문제가 생긴 팝업만 닫고 새 팝업으로 교체한다(셀프힐링).

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **책임공유 모델(Shared Responsibility Model)** 위에서 동작하며, 클라우드 제공자(CSP)는 인프라·물리 보안·하이퍼바이저를, 고객은 OS·미들웨어·데이터·IAM을 책임진다. 핵심 컴포넌트는 다음과 같이 계층화된다.

```text
[클라우드 네이티브 7계층 참조아키텍처 (CNCF Landscape 매핑)]
   +----------------------------------------------------------+
   | L7  Edge / CDN / WAF   (CloudFront, Cloudflare, AWS WAF) |
   +----------------------------------------------------------+
   | L6  API Gateway / BaaS (Kong, Apigee, AWS AppSync)       |
   |     + AuthN/Z (OAuth2/OIDC, JWT, mTLS, SPIFFE)           |
   +----------------------------------------------------------+
   | L5  Service Mesh / Sidecar (Istio, Linkerd, Consul)       |
   |     - Traffic Mgmt (Canary/Blue-Green, Retry, CB)        |
   |     - mTLS, AuthorizationPolicy, Telemetry(EnvoyFilter)   |
   +----------------------------------------------------------+
   | L4  Orchestration       (K8s, EKS, AKS, GKE, Nomad)      |
   |     - Control Plane : API Server, etcd, Scheduler        |
   |     - Node Components: kubelet, kube-proxy, CNI(Calico)   |
   |     - CRD/Operator Pattern (ArgoCD, Crossplane)         |
   +----------------------------------------------------------+
   | L3  Runtime             (Containerd/CRI-O, gVisor, Firecracker)|
   |     - OCI Image, SBOM(Syft/Trivy), Sigstore Cosign       |
   +----------------------------------------------------------+
   | L2  Compute             (EC2, Lambda, Cloud Run, Fargate)|
   |     - Spot/Preemptible, Graviton3, RDMA, Confidential    |
   +----------------------------------------------------------+
   | L1  Storage / DB        (S3, EBS, RDS, Aurora, DynamoDB,|
   |                          CosmosDB, Spanner, Bigtable)    |
   |     + Message Bus (Kafka, Kinesis, Pub/Sub, NATS, Pulsar)|
   +----------------------------------------------------------+
   ⊕ Cross-Cutting: Observability (OTel/Logs/Metrics/Traces)
   ⊕ Cross-Cutting: Security (Vault, KMS, IAM, CSPM, SIEM)
   ⊕ Cross-Cutting: FinOps (Kubecost, CloudHealth, Vantage)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway + BFF** | 외부 트래픽 라우팅, 프로토콜 변환(gRPC↔REST↔GraphQL), 인증 위임, Rate Limit | Kong(Go), Envoy xDS, AWS API Gateway + Lambda Authorizer, BFF(Backend-For-Frontend)로 모바일/웹 분리 |
| **Service Mesh** | L7 트래픽관리, mTLS 자동화, 카나리/트래픽미러링, 분산추적 전파 | Istio(Envoy기반, Istiod 단일컨트롤플레인), Linkerd(Linkerd2-proxy Rust기반, 경량), Consul Connect, Ambient Mesh(eBPF기반) |
| **Container Orchestrator** | 선언적 상태(Desired State) 유지, 스케줄링, 셀프힐링, HPA/VPA/Cluster Autoscaler | Kubernetes 1.30+(SidecarContainer GA), Karmada/ClusterAPI 멀티클러스터, K3s 엣지, Argo Workflows |
| **Observability Stack** | SLI/SLO 기반 모니터링, 분산추적, 이상탐지, AIOps | Prometheus + Grafana + Loki + Tempo(OTel컬렉터), eBPF 기반 Pixie/Tetragon, OpenTelemetry Collector(OTLP) |
| **Serverless/Event** | 이벤트 기반 워크로드, 0->N 자동확장, Pay-per-Use | Lambda(15분 한계), Cloud Run(60분, Knative), EventBridge+Step Functions(상태머신), Durable Functions(체크포인트) |
| **Cloud Storage 계층** | Hot/Warm/Cold 데이터 티어링, CRDT/최종일관성 | S3 IA/Glacier, Aurora DSQL(글로벌), DynamoDB Global Tables(다중리전 액티브-액티브), Snowflake/BigQuery(데이터웨하우스) |

**핵심 알고리즘/메커니즘**:
- **HashiCorp Raft 합의**: etcd/Consul이 리더당 50ms heartbeat, 150~200ms election timeout으로 3-of-5 quorum을 구성하여 AP시스템에서도 메타데이터 CP를 보장
- **HPA v2 알고리즘**: `desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]` (KEDA로 SQS/Kafka lag까지 확장)
- **Circuit Breaker (Hystrix/Resilience4j 패턴)**: Closed->Open(임계치 초과)->Half-Open(시험 트래픽)->Closed 전환, 슬라이딩 윈도우(10s, 100reqs) 기반 실패율 계산
- **Saga 보상 트랜잭션**: Choreography(각 서비스 이벤트 발행) vs Orchestration(Camunda 8/Temporal 워커). Temporal은 이벤트소싱 + 결정론적 리플레이로 exactly-once 보장

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 7계층은 마치 호텔의 총지배인(API Gateway)->층별 매니저(Service Mesh)->하우스키핑팀(K8s)->객실(컨테이너)->건물(Compute)->금고(Storage)처럼, 손님의 요청이 위에서 아래로 흐르되 각 층이 독립적으로 모니터링·장애격리·자동복구되는 운영체계다.

---

## Ⅲ. 비교 및 연결

### 1. 아키텍처 패러다임 비교

| 구분 | Monolithic 3-Tier | SOA (ESB 중심) | Microservice | Cloud-Native (12-Factor+K8s) |
| :--- | :--- | :--- | :--- | :--- |
| **결합도** | 강한결합(Tight), 단일배포 | 느슨(Loose) but ESB 결합 | 서비스별 독립, API기반 | 컨테이너+메시, GitOps |
| **확장 단위** | VM/WAS 전체 복제 | ESB 노드 | 서비스 단위 | Pod/Function 단위 (밀리초 스케일) |
| **데이터 관리** | 단일 DB, ACID | DB per Service(부분) | DB per Service, eventual | Polyglot + CQRS/ES, Saga |
| **장애 전파** | 전체 다운 | ESB SPOF | Bulkhead, CircuitBreaker | Cell-Based + Chaos Eng.(Chaos Mesh/Litmus) |
| **배포 주기** | 월 1~분기 1회 | 월 1~주 1회 | 주 1~일 1회 | 일 수십~수백회 (ArgoCD PR 자동화) |
| **관측성** | 로그 파일 위주 | SOAP/WSDL 모니터링 | 분산추적(Zipkin/Jaeger) | OTel + eBPF + AIOps |
| **조직** | Conway Law: 기능조직 | BizTalk/Oracle SOA팀 | 2-pizza Team(8명) | Platform Engineering+SRE |
| **TCO 패턴** | CAPEX 우세, 3년 회수 | HW+미들웨어 라이센스 | OPEX^, 5년 ROI 2.3x | FinOps로 30~40% 절감 (Mckinsey 2023) |
| **적합 workload** | 레거시, ERP, 거래소 | 금융 코어, EAI | 중규모 SaaS, 커머스 | SaaS, AI/ML, 스트리밍, IoT |
| **대표 실패 사례** | Knight Capital 2012, 45분장애 $440M | Healthcare.gov 2013 출시 실패 | 단일서비스 장애의 팬아웃 | 클러스터 오토스케일 진동(flapping) |

### 2. 멀티클라우드 vs 하이브리드클라우드 vs 폴리클라우드

| 구분 | Public-only (단일 CSP) | Hybrid (Private+Public) | Multi-Cloud (2+ CSP) | Poly-Cloud (Portable) |
| :--- | :--- | :--- | :--- | :--- |
| **정의** | 1개 CSP만 사용 | On-Prem + Cloud (예: Outposts/Anthos/Azure Arc) | AWS+Azure 등 동시 사용 | CSP 중립 (K8s/Terraform+Crossplane) |
| **데이터 거버넌스** | CSP 정책 의존 | 데이터주권(금융/공공) 충족 | 벤더 종속 최소화 | 데이터 카탈로그(Unity/DataHub) 필수 |
| **네트워크** | VPC Peering/Transit GW | Direct Connect/ExpressRoute, SD-WAN | Cloud Interconnect(Equinix), Megaport | 동일 CNI 멀티클러스터(Karmada) |
| **Egress 비용** | 단일 CSP 요율 | CSP↔On-Prem DX요금 | 이중 egress(매우 비쌈) | 데이터 중력(Data Gravity) 최소화 |
| **도구** | AWS Well-Architected | Azure Arc + Stack | Terraform + Spotinst/MultiCloud | Crossplane + ArgoCD ApplicationSet |
| **적합 케이스** | 초기 PoC, SMB | 규제산업(금융/공공/의료) | DR/BCP, 가격협상력 | M&A, 글로벌 SaaS, AI 트레이닝 분산 |

### 3. 데이터베이스 트레이드오프 (CAP/PAICELC 관점)

| 구분 | RDBMS (Aurora/MySQL) | NoSQL Document (Mongo) | Wide-Column (Cassandra/DynamoDB) | NewSQL (CockroachDB/Spanner) |
| :--- | :--- | :--- | :--- | :--- |
| **CAP** | CA (단일리전 한정) | CP or AP (설정) | AP (Tunable Consistency=LOCAL_QUORUM) | CP + 글로벌(동기식) |
| **일관성** | Strong, ACID | Eventual, ACID per doc | Eventual, LWW | Strong, Serializable |
| **확장** | 수직/Read Replica | 샤딩 (Mongo Sharding) | 마스터리스 (해시 링) | 자동샤딩 + Raft |
| **SQL** | ANSI SQL | MQL/Atlas SQL | CQL(부분) | PostgreSQL 호환 |
| **비용 모델** | Provisioned/Serverless v2 | RU/RAM (Cosmos) | WCU/RCU (DynamoDB) | vCPU/RAM + Storage |
| **적합** | 트랜잭션, ERP | 카탈로그, CMS | 시계열, IoT, 게임 | 글로벌 결제, 재고 |

- **📢 섹션 요약 비유**: 단일클라우드는 한 가전매장에서 모든 가전을 사서 A/S를 맡기는 것, 멀티클라우드는 이마트와
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 688 / 800

<- **이전**: [687. 클라우드 아키텍처 핵심 토픽 687번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/687_cloud_architecture_core_topic_687_exam_summar/)
**다음**: [689. 클라우드 아키텍처 핵심 토픽 689번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/689_cloud_architecture_core_topic_689_exam_summar/) ->

---
