---
title: "609. 클라우드 아키텍처 핵심 토픽 609번 시험 요약 (Cloud Architecture Core Topic 609 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 609번 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS 서비스 모델, 퍼블릭/프라이빗/하이브리드/멀티클라우드 배포 모델, 마이크로서비스·서버리스·이벤트驱动·메시 기반 아키텍처 패턴, 그리고 12-Factor App과 CNCF 클라우드 네이티브 원칙을 통합한 엔터프라이즈급 분산 시스템 설계 역량을 평가하는 종합 토픽이다.
> 2. **가치**: Well-Architected Framework 5대 축(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화) 및 AWS·Azure·GCP·NAVER Cloud·KT Cloud의 Managed Service 활용으로 CAPEX 대비 OPEX 전환 30~70%, Time-to-Market 60% 단축, Auto Scaling을 통한 리소스 가용성 99.99% SLA 확보가 가능하다.
> 3. **판단 포인트**: 클라우드 네이티브 전환 시 6R 전략(Rehost/Replatform/Refactor/Rearchitect/Retire/Retain), CAP Theorem·BASE vs ACID 트레이드오프, EKS/AKS/GKE/OKE vs 자체 Kubernetes, Circuit Breaker·Saga·CQS 패턴 채택 여부, 그리고 Shared Responsibility Model 기반 보안 경계 설정이 핵심 의사결정 분기점이다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스(legacy monolithic) 환경은 EAI(Enterprise Application Integration) 기반의 SOA(Service-Oriented Architecture)에서 ESB(Enterprise Service Bus) 허브 앤 스포크 구조로 진화했으나, 트래픽 스파이크(Spark), 예측 불가능한 확장성, 그리고 수개월 단위 provisioning cycle의 한계에 부딪혔다. 2006년 AWS S3·EC2 출시 이후 클라우드 컴퓨팅은 NIST SP 800-145 정의(온디맨드 셀프서비스, 광역 네트워크 접근, 리소스 풀링, 탄력적 확장, 측정 가능한 서비스) 5대 필수 특성을 토대로 산업 패러다임을 근본적으로 전환시켰다.

특히 2013년 Docker 등장, 2014년 Kubernetes 오픈소스 공개, 2015년 CNCF(Cloud Native Computing Foundation) 출범 이후 클라우드 네이티브(Cloud Native)는 컨테이너 오케스트레이션, 선언적 API, 불변 인프라스트럭처(Immutable Infrastructure), GitOps 운영 모델을 결합하여 마이크로서비스 아키텍처의 사실 구현 표준으로 자리매김했다. 대한민국 공공부문은 2022년 클라우드 이용촉진基本法, 2023년 행정안전부 클라우드 First 정책, 2024년 KCS(Korea Cloud Security) 인증 강화를 통해 클라우드 전환을 가속화하고 있으며, 금융권은 금융감독원의 클라우드 이용 가이드라인에 따라 2025년까지 핵심 시스템의 단계적 클라우드 도입을 추진 중이다.

```text
+---------------------------------------------------------------------+
|              클라우드 아키텍처 진화 패러다임 (Evolution Map)         |
+---------------------------------------------------------------------+
  [Mainframe Era]     [Client-Server]      [Web 2.0 / SOA]         [Cloud / Cloud-Native]
   1960s~1980s         1990s              2000~2010                2010~현재
       |                  |                   |                       |
       v                  v                   v                       v
  +---------+       +----------+        +----------+          +--------------+
  |Central  |       |2-Tier /  |        |3-Tier /  |          |Micro-services|
  |Host /   |------->|3-Tier DB |-------->|ESB / SOA |---------->|+ k8s +Server |
  |Terminal |       |+ ERP/CRM |        |+ EAI/BPM |          |less + Mesh   |
  +---------+       +----------+        +----------+          +--------------+
   CAPEX heavy      CAPEX 중심         SOA + WSDL         CAPEX -> OPEX 전환
   10년 refresh     5년 refresh         SOAP/XML/REST      Day 1 -> Minute 단위
   단일 장애점      DB 병목화           통합 거버넌스       분산 트레이싱/관측
       |                  |                   |                       |
       v                  v                   v                       v
   CAPEX              CAPEX+OPEX         표준화/통합          Pay-per-use
   수직확장(Scale Up)  수평확장(Scale Out)  인터페이스 거버넌스     무한 확장(Elastic)
```

**📢 섹션 요약 비유**: 클라우드 아키텍처의 진화는 마치 **물의 상태 변화**와 같다. 고체(메인프레임)는 단단하지만 깨지기 쉽고, 액체(SOA)는 흐르지만 증발이 잦다. 기체(클라우드 네이티브)는 어느 그릇이든 채우는 유연성을 가지며, 그 기체의 운동을 제어하는 것이 Kubernetes·Service Mesh·Observability다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 4계층 참조 모델(참조: NIST·AWS·Azure Well-Architected)로 추상화된다: **물리 계층(Hypervisor, Bare-Metal) -> 가상화 계층(VM, Container, Unikernel) -> 플랫폼 계층(Managed K8s, Serverless Runtime) -> 애플리케이션 계층(Microservices, Event Handler, API)**. 각 계층은 선언적 API(Declarative API)와 제어 루프(Control Loop) 패턴으로 자기치유(self-healing)·자기확장(self-scaling)·자기구성(self-configuring) 특성을 구현한다.

```text
+------------------------------------------------------------------------+
|       클라우드 네이티브 4계층 참조 아키텍처 (Reference Architecture)      |
+------------------------------------------------------------------------+
  +----------------------------------------------------------------------+
  |  L4: Application Layer  - Microservices / FaaS / API Gateway / BFF  |
  |       Spring Cloud, Istio, AWS Lambda, Azure Functions              |
  +----------------------------------------------------------------------+
  |  L3: Platform Layer  - Managed K8s / Service Mesh / Serverless      |
  |       EKS / AKS / GKE / NKS / Istio / Linkerd / Knative             |
  +----------------------------------------------------------------------+
  |  L2: Virtualization Layer  - Container Runtime / VM / WASM          |
  |       containerd / CRI-O / runC / Firecracker / KVM                 |
  +----------------------------------------------------------------------+
  |  L1: Physical Layer  - x86 / ARM64 / GPU / DPU / SmartNIC          |
  |       Intel Sapphire Rapids / AMD EPYC / NVIDIA H100 / AWS Nitro    |
  +----------------------------------------------------------------------+
                              ^
                              |  선언적 API + Control Loop (Reconcile)
                              |  GitOps (ArgoCD/Flux) + Observability
                              v
  +---------------------------------------------------------------------+
  |   Observability Stack  - Metrics / Logs / Traces (3 Pillars)        |
  |   Prometheus + Grafana / EFK / Loki / Jaeger / OpenTelemetry       |
  +---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway / BFF** | 클라이언트-서비스 라우팅, 인증/인가, Rate Limiting, 응답 변환 | Kong(nginx+Lua), AWS API Gateway(usage plan/throttle), Apigee(API monetization), Spring Cloud Gateway(WebFlux 기반 non-blocking I/O), BFF(Backend-For-Frontend) 패턴으로 모바일/웹 별 최적화 |
| **Service Mesh (Data/Control Plane)** | L7 트래픽 관리, mTLS, Circuit Breaker, Canary 배포 | Istio(Envoy sidecar + istiod control plane), Linkerd(Linkerd2-proxy Rust기반 경량), Consul Connect, AWS App Mesh, Open Service Mesh(CNCF), eBPF 기반 Cilium Service Mesh |
| **Container Orchestrator (Kubernetes)** | 선언적 배포·스케일링·자가치유, 서비스 디스커버리, Secret 관리 | K8s Control Plane: kube-apiserver(etcd) / scheduler / controller-manager / cloud-controller-manager. Node Component: kubelet / kube-proxy(CNI: Calico/Cilium/Flannel) / CRI(containerd). 워크로드: Deployment, StatefulSet, DaemonSet, Job/CronJob, HPA/VPA/Cluster Autoscaler |
| **Serverless / FaaS Runtime** | 이벤트 기반 stateless 함수 실행, Cold Start 최적화 | AWS Lambda(128MB~10GB, 15분 timeout), Azure Functions(Durable Functions로 stateful), GCP Cloud Run(Knative 기반), Naver Cloud Function. Cold Start: Init Phase->Code Phase->Invoke Phase, SnapStart/Lazy Loading으로 200ms 이하 최적화 |
| **Managed Data Service** | 관계형/NoSQL/NewSQL, Auto Backup, Multi-AZ HA | RDS Aurora(6 replicas, storage auto-scaling), DynamoDB(Global Tables, DynamoDB Streams->Lambda 트리거), Azure Cosmos DB(Multi-Master, 5 consistency level), CockroachDB(분산 SQL, Geo-Partitioning) |
| **Event Streaming / Message Broker** | 비동기 이벤트 전파, CQRS, Saga 오케스트레이션 | Apache Kafka(KRaft 모드, Exactly-Once Semantics, Schema Registry), Pulsar(BookKeeper 세그먼트), RabbitMQ(AMQP 0-9-1), AWS SQS/SNS/Kinesis, NATS JetStream, AWS EventBridge(Event Bus + Archive) |
| **Observability Stack** | 3대 축(Metrics·Logs·Traces) 기반 관측 및 SLO 관리 | OpenTelemetry(SDK + Collector + Protocol), Prometheus(Pull model, PromQL), Grafana(Visualization), Loki(LogQL), Jaeger/Tempo(분산 트레이싱), Datadog/New Relic(SaaS 통합), RED(Rate·Errors·Duration)·USE(Utilization·Saturation·Errors)·SLI/SLO/SLI Budget |
| **IaC (Infrastructure as Code)** | 선언적 인프라 provisioning, GitOps, Drift Detection | Terraform(HCL, State Lock, Module Registry), Pulumi(General-purpose language), AWS CDK(Construct), Crossplane(K8s native IaC), Helm(K8s package manager), ArgoCD/Flux(GitOps Controller) |

### Well-Architected Framework 5대 기둥 심화

1. **운영 우수성(Operational Excellence)**: CodeBuild->CodeDeploy->CodePipeline CI/CD, ChatOps(Slack+Lambda), Runbook 자동화, Mean Time To Detect(MTTD)·Mean Time To Recover(MTTR) KPI 관리
2. **보안(Security)**: Zero Trust Architecture(Identity 기반, BeyondCorp), AWS IAM Roles Anywhere / IRSA(IAM Role for Service Accounts), KMS/HSM 키 관리, VPC 격리, GuardDuty(위협 탐지), WAFv2 + Shield Advanced(L3/L4/L7 DDoS 방어)
3. **안정성(Reliability)**: Multi-AZ + Multi-Region Active-Active, RDS Multi-AZ Cluster(동기 복제), Route53 Health Check + DNS Failover, Chaos Engineering(LitmusChaos, AWS Fault Injection Service, Gremlin)
4. **성능 효율(Performance Efficiency)**: C5n·D3·P4 인스턴스 패밀리 선택, Compute Optimizer 권고, ElastiCache(Redis Cluster), CloudFront/Cloudflare CDN, Database Connection Pool(HikariCP), Async I/O, GraalVM Native Image(AOT 컴파일)
5. **비용 최적화(Cost Optimization)**: Reserved Instance(1/3년 약 40~60% 할인), Savings Plans(Compute SP), Spot Instance(HPC·ML 워크로드, 70% 할인), S3 Intelligent-Tiering(액세스 패턴 자동 분석), Cost Anomaly Detection(ML 기반)

**📢 섹션 요약 비유**: 4계층 클라우드 아키텍처는 **대형 호텔의 운영 체계**와 같다. 1층(물리 인프라)은 토지와 건물, 2층(가상화)은 객실, 3층(플랫폼)은 프론트 데스크·벨보이·하우스키핑 서비스, 4층(애플리케이션)은 게스트의 실제 경험이다. 그리고 Observability는 **CCTV·세무·회계 시스템**에 해당하여 호텔 운영의 모든 상태를 실시간으로 가시화한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **IaaS (Infrastructure-as-a-Service)** | **PaaS (Platform-as-a-Service)** | **SaaS (Software-as-a-Service)** | **FaaS (Function-as-a-Service)** |
| :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | OS, 미들웨어, 런타임, 데이터, 앱 | 데이터, 앱만 관리 | 앱만 관리 (사용자 데이터 포함) | 코드(함수 로직)만 관리 |
| **제어 수준** | 가장 높음 (Hypervisor·OS 통제 가능) | 중간 (런타임/미들웨어 자동) | 낮음 (설정·확장만) | 거의 없음 (이벤트+코드만) |
| **확장성 모델** | 수동/Auto Scaling Group | 자동 (Horizontal/Vertical) | 자동 (Multi-Tenant) | 자동 (Concurrency 기반, 0->1000) |
| **과금 모델** | 초/분 단위 인스턴스 | vCPU·Memory·요청 단위 | 사용자 라이선스 (Per-User/Month) | 호출 횟수 + GB-Second |
| **대표 서비스** | AWS EC2/Azure VM/GCE/NCP Server | AWS Elastic Beanstalk, Heroku, Google App Engine, NCP Cloud Functions | Microsoft 365, Salesforce, Slack, Google Workspace | AWS Lambda, Azure Functions, GCP Cloud Functions |
| **적합 시나리오** | 레거시 lift-and-shift, 특수 HW | 웹앱, API 백엔드 표준화 | 업무 표준화(메일·CRM·협업) | 이벤트 처리, ETL, Webhook, 예약 작업 |
| **Cold Start 이슈** | 없음 (상시 가동) | 보통 (Platform init) | 없음 (관리형) | 큼 (200ms~3s, SnapStart로 완화) |
| **예시 비용(상대)** | $0.05/시~$10/시 | $0.10~$1/요청 | $10~$50/User/Month | $0.20/100만 호출 + $16/GB-Second |

| 구분 | **단일 클라우드(Single Cloud)** | **멀티 클라우드(Multi-Cloud)** | **하이브리드 클라우드(Hybrid)** |
| :--- | :--- | :--- | :--- |
| **정의** | 한 CSP만 사용 | 2개 이상 CSP 병행 | On-Prem + Public Cloud 연결 |
| **연결 기술** | 내부 VPC Peering | Transit Gateway, Megaport, Interconnect | AWS Outposts / Azure Stack / Google Anthos / KT Cloud Z |
| **장점** | 단일 SLA·빌링, 통합 IAM, 낮은 latency | 벤더 종속 제거, Best-of-Breed, 지역별 컴플라이언스 | 데이터 주권, Legacy 호환, Burst Capacity |
| **단점** | 벤더 종속(Vendor Lock-in), 단일 장애점 | 네트워크 egress 비용, 통합 거버넌스 난이도, 자격증명 관리 | 네트워크 복잡도, 통합 관제, 이중 운영비 |
| **도구** | AWS Console, Azure Portal | Terraform Multi-Provider, Crossplane, Anthos | Azure Arc, AWS Systems Manager, Google Anthos |

| 구분 | **모놀리식 (Monolith)** | **모듈러 모놀리식 (Modular Monolith)** | **마이크로서비스 (Microservices)** | **서버리스 (Serverless)** |
| :--- | :--- | :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/EAR | 단일 deploy에 모듈 경계 | 독립 서비스 (Container별) | 함수 단위 (Function
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 609 / 800

<- **이전**: [608. 클라우드 아키텍처 핵심 토픽 608번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/608_cloud_architecture_core_topic_608_exam_summar/)
**다음**: [610. 클라우드 아키텍처 핵심 토픽 610번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/610_cloud_architecture_core_topic_610_exam_summar/) ->

---
