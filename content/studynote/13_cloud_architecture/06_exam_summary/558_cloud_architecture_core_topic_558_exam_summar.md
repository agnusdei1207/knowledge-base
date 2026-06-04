---
title: "558. 클라우드 아키텍처 핵심 토픽 558번 시험 요약 (Cloud Architecture Core Topic 558 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST SP 800-145 서비스 모델(IaaS/PaaS/SaaS/FaaS) 위에 컨테이너 오케스트레이션(Kubernetes), 서비스 메시(Istio/Linkerd), IaC(Terraform/Pulumi), GitOps(ArgoCD/Flux), 관측가능성(OpenTelemetry/Prometheus) 스택을 결합해 **선언적·탄력적·자가치유** 분산 시스템을 구현하는 패러다임이다.
> 2. **가치**: Auto Scaling을 통해 피크 트래픽 10배 변동에도 SLA 99.99%를 유지하고, Time-to-Market을 60~80% 단축하며, FinOps·Reserved Instance·Spot Instance 조합으로 TCO를 30~45% 절감할 수 있다. CAPEX->OPEX 전환과 글로벌 리전 멀티 AZ 배포로 DR RTO/RPO를 수 분 단위로 축소한다.
> 3. **판단 포인트**: **6R 마이그레이션 전략(Rehost/Replatform/Repurchase/Refactor/Retire/Retain)** 중 어느 것을 택할지, **Multi-Cloud vs Hybrid Cloud vs Single-Cloud** 의사결정, **Stateful 워크로드의 CSI/PV 설계와 데이터 중력(Data Gravity) 문제**, **Well-Architected 5대 기둥(운영 우수성·보안·안정성·성능 효율·비용 최적화)** 간의 트레이드오프, 그리고 **Vendor Lock-in vs 기술 주권**의 균형이 핵심 설계 변수다.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스(Enterprise Data Center) 환경은 예측 기반 용량 계획(Peak+20%)으로 인해 CPU Utilization이 평균 10~15%에 불과했고, 신규 서버 도입에 8~12주가 소요되었으며, DR 사이트 별도 구축에 수십억 원이 투입됐다. 2006년 AWS S3·EC2 출시 이후 시작된 클라우드 컴퓨팅은 **가상화(KVM/Xen/Hyper-V) -> 컨테이너화(Docker) -> 오케스트레이션(K8s) -> 서버리스(Lambda) -> 엣지 컴퓨팅(Cloudflare Workers)** 으로 진화하며, 마이크로서비스 아키텍처(MSA)와 DevOps 문화와 결합해 **Cloud Native** 패러다임을 정착시켰다.

가트너는 2025년 기준 신규 디지털 워크로드의 70% 이상, 기존 워크로드의 50% 이상이 퍼블릭 클라우드에서 운영될 것으로 예측했고, CNCF(Cloud Native Computing Foundation) 랜드스페이스에는 1,000+ 프로젝트가 등재되어 클라우드 네이티브 기술 스택의 표준화를 이끌고 있다. 한국 정부도 **클라우드컴퓨팅법(2024.1. 시행)** 과 **클라우드 안심구역(CSAP)**, **조달청 클라우드 SaaS 시장** 등을 통해 공공부문 전환을 가속화하고 있다.

```text
[클라우드 아키텍처 진화 패러다임 시프트 - 4세대 흐름도]

  +-----------------+   +-----------------+   +-----------------+   +-----------------+
  |  1세대: Mainframe|   | 2세대: Client/  |   | 3세대: Web/     |   | 4세대: Cloud    |
  |  (1960s-80s)    |   |   Server        |   |   SOA / Web 2.0 |   |   Native        |
  |                 |   |   (1990s)       |   |   (2000s)       |   |   (2015-now)    |
  | +-------------+ |   | +-------------+ |   | +-------------+ |   | +-------------+ |
  | | 중앙집중식  | |   | | 2-Tier      | |   | | 3-Tier, SOA | |   | | MSA, Serverless|
  | | 터미널      | |   | | DB          | |   | | ESB, BPM    | |   | | K8s, Mesh, IaC |
  | +-------------+ |   | +-------------+ |   | +-------------+ |   | +-------------+ |
  | Scale Up 전용   |   | Scale Out 시작  |   | 가상화·VMWare  |   | Auto·Self-Heal |
  +-----------------+   +-----------------+   +-----------------+   +-----------------+
         v                      v                      v                      v
  +-------------------------------------------------------------------------------------+
  | 기술 트리거:        가상화(Hypervisor)  ->  컨테이너(Docker, 2013)  ->  K8s(2015)     |
  |                  ->  Istio/Envoy(2017)  ->  Lambda(2014)  ->  WASM/Edge(2022+)        |
  +-------------------------------------------------------------------------------------+
         v
  +-------------------------------------------------------------------------------------+
  | 비즈니스 트리거:    Pay-per-use  ->  글로벌 확장  ->  AI/ML GPUaaS  ->  SaaS 시장 폭증  |
  +-------------------------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 클라우드 진화를 **전기 공급망**의 변천에 비유할 수 있다. 초기에는 각 가정이 **발전기(On-Premise)** 를 직접 돌렸지만, 이제는 **원자력·태양광 발전소(Hyperscaler)** 에서 전기를 공급받아 **요금제(Pay-per-use)** 로 사용하듯, 컴퓨팅 자원을 필요한 만큼 즉시 끌어다 쓰는 시대가 도래했다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **Edge/Client -> API Gateway -> Service Mesh -> Container Orchestration -> Serverless/FaaS -> Managed DB/Object Storage** 의 6계층 구조로 설계하며, 각 계층은 CNCF 랜드스페이스 프로젝트로 구현된다. 핵심 동작 원리는 **선언적 API(Declarative API)** 와 **컨트롤 루프(Reconcile Loop)** 의 결합이다. 사용자가 `kubectl apply -f deployment.yaml` 로 "원하는 상태(Desired State)"를 선언하면, K8s Controller가 "현재 상태(Actual State)"와 비교해 **Status=Healthy** 가 될 때까지 끊임없이 수렴(Reconcile)한다.

```text
[클라우드 네이티브 6계층 참조 아키텍처 (CNCF Landscape 기반)]

  [사용자 단말]                                                         [관리/관제]
   📱💻🖥️                                                              📊 SRE/DevOps
       |                                                                      |
       | HTTPS/gRPC                                                          | Git Push
       v                                                                      v
  +------------------------------------------------------------------------------------+
  | Layer 1: Edge / CDN / WAF                                                        |
  |   - Cloudflare / AWS CloudFront / Akamai / GCP Cloud CDN                          |
  |   - DDoS 방어, TLS Termination, Bot Management, Lambda@Edge (0ms cold start)     |
  +------------------------------------------------------------------------------------+
                                          |
                                          v
  +------------------------------------------------------------------------------------+
  | Layer 2: API Gateway / Ingress Controller                                         |
  |   - Kong / Apigee / Ambassador / NGINX / Traefik / Envoy                          |
  |   - 역할: Rate Limiting, OAuth2/JWT 인증, Circuit Breaker, Canary(5%/50%/100%)   |
  |   - OpenAPI 3.0 명세 기반, gRPC-Web/JSON-WS 변환                                  |
  +------------------------------------------------------------------------------------+
                                          |
                                          v
  +------------------------------------------------------------------------------------+
  | Layer 3: Service Mesh (Data Plane + Control Plane)                                |
  |   - Istio (Envoy Sidecar) / Linkerd / Consul Connect / Cilium Service Mesh        |
  |   - 역할: mTLS 자동화, Traffic Shifting, Retry/Timeout, Telemetry, Policy (OPA)    |
  |   - Sidecar Pattern: App 컨테이너 옆에 Envoy 프록시 주입 (1Pod = 2Container)       |
  +------------------------------------------------------------------------------------+
                                          |
                                          v
  +------------------------------------------------------------------------------------+
  | Layer 4: Container Orchestration (Kubernetes)                                     |
  |   - Control Plane: kube-apiserver / etcd(raft) / scheduler / controller-manager   |
  |   - Worker Node: kubelet / kube-proxy / Container Runtime(containerd/CRI-O)        |
  |   - 워크로드: Deployment / StatefulSet / DaemonSet / Job / CronJob                 |
  |   - HPA: CPU 70% -> Pod 2->20 자동 확장, VPA, KEDA(이벤트 기반), Karpenter(노드)  |
  +------------------------------------------------------------------------------------+
                                          |
                          +---------------+---------------+
                          v                               v
  +--------------------------------+  +------------------------------------+
  | Layer 5a: Serverless / FaaS   |  | Layer 5b: Stateful Microservices   |
  |   - AWS Lambda / Azure Func   |  |   - Spring Boot / Node.js / Go    |
  |   - GCP Cloud Run             |  |   - Redis, Kafka, RabbitMQ        |
  |   - Cold Start: 100~500ms     |  |   - gRPC, Protobuf, GraphQL        |
  |   - Event: SQS, Kafka, HTTP   |  |   - Saga Pattern, Outbox Pattern  |
  +--------------------------------+  +------------------------------------+
                          |                               |
                          +---------------+---------------+
                                          v
  +------------------------------------------------------------------------------------+
  | Layer 6: 데이터 계층 (Polyglot Persistence)                                       |
  |   - RDBMS:  Amazon Aurora / Cloud Spanner / CockroachDB (NewSQL)                  |
  |   - NoSQL:  DynamoDB / CosmosDB / MongoDB Atlas / Cassandra                       |
  |   - Cache:  ElastiCache(Redis) / Memorystore / Memcached                          |
  |   - Object: S3 / GCS / MinIO (API: S3 호환)                                      |
  |   - Search: OpenSearch / Elasticsearch / Algolia                                 |
  |   - OLAP:  Snowflake / BigQuery / Redshift / Databricks (Lakehouse)               |
  |   - Queue:  SQS/SNS / Pub/Sub / Kafka (MSK) / RabbitMQ                            |
  +------------------------------------------------------------------------------------+
                                          |
                                          v
  +------------------------------------------------------------------------------------+
  | 횡단 관심사(Cross-Cutting)                                                        |
  |   🔍 Observability: Prometheus + Grafana + Loki + Tempo + Jaeger (OpenTelemetry) |
  |   🔐 Security:      Trivy(취약점) + Falco(런타임) + OPA/Gatekeeper + Vault(Secret)|
  |   📦 IaC:           Terraform / Pulumi / CloudFormation / Crossplane             |
  |   🚀 GitOps:        ArgoCD / Flux / Jenkins X (PR -> 자동 Sync)                   |
  |   💰 FinOps:        Kubecost / Vantage / CloudHealth (RI/SP/Commit 관리)          |
  +------------------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway** | 외부 트래픽 진입점, 인증/인가, 라우팅, 트래픽 정책 | Kong(Plugin 아키텍처), Apigee(API 수익화), Envoy(xDS API). OAuth2.0/OIDC/JWT 검증, Rate Limit(Token Bucket), Canary 배포(Header/Weight 기반) |
| **Service Mesh** | 마이크로서비스 간 통신을 사이드카로 분리, mTLS·관측성·정책 | Istio(Envoy + Istiod): mTLS STRICT 모드, VirtualService(트래픽 분기 90/10), DestinationRule(Load Balancer: ROUND_ROBIN/LEAST_REQUEST). eBPF 기반 Cilium은 커널 레벨 처리로 Sidecar 오버헤드 제거 |
| **Container Runtime** | 컨테이너 실행·격리·자원 제한 | containerd(OCI 호환), CRI-O(K8s 전용). cgroup v2로 CPU/Memory Limit, namespace로
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 558 / 800

<- **이전**: [557. 클라우드 아키텍처 핵심 토픽 557번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/557_cloud_architecture_core_topic_557_exam_summar/)
**다음**: [559. 클라우드 아키텍처 핵심 토픽 559번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/559_cloud_architecture_core_topic_559_exam_summar/) ->

---
