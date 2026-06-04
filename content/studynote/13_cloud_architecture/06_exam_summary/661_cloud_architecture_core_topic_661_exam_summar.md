---
title: "661. 클라우드 아키텍처 핵심 토픽 661번 시험 요약 (Cloud Architecture Core Topic 661 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS의 4계층 서비스 모델을 기반으로, Shared Responsibility Model 하에 컴퓨팅·스토리지·네트워크를 API-driven 인프라로 추상화하고, Multi-AZ·Multi-Region 가용성 패턴(예: N+1, 2N Active-Active)과 Cloud-Native 12-Factor 원칙을 적용한 설계 체계이다.
> 2. **가치**: CAPEX를 OPEX로 전환하여 초기 인프라 투자비를 60~80% 절감하고, Auto Scaling Group(ASG)·Spot Instance·Reserved Instance 혼용으로 TCO를 30~45% 추가 절감하며, 글로벌 엣지(CloudFront, Cloudflare) 기반 latency를 100ms 이하로 단축하여 가용성 99.99%(SLA 4-nines)를 달성한다.
> 3. **판단 포인트**: Trade-off는 CAP Theorem(일관성 vs 가용성 vs 분할내성), Synchronous vs Asynchronous 통신(Saga vs 2PC), Stateful vs Stateless 설계, 비용 vs 성능(인스턴스 타입 선택), Lock-in vs Portability(Abstraction Layer 유무)의 5축 의사결정 프레임으로 평가해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적 On-Premise 3-Tier 아키텍처는 L4/L7 로드밸런서 하드웨어, SAN 스토리지, 물리 서버의 수직 확장(Scale-Up) 모델로, Capacity Planning 오차 시 30~40%의 유휴 자원 또는 장애를 야기했다. 2006년 AWS S3·EC2 출시 이후 클라우드 컴퓨팅은 CapEx(선불 자산 투자)에서 OpEx(사용량 기반 과금) 모델로의 전환, API 기반 Programmable Infrastructure, 선언적 IaC(Infrastructure as Code: Terraform/CloudFormation)를 통한 불변 인프라(Immutable Infrastructure) 패러다임을 정착시켰다.

NIST SP 800-145(2011) 표준에 따라 클라우드는 5대 필수 특성(On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)과 4계층 Deployment Model(Public/Private/Hybrid/Community), 3계층 Service Model(IaaS/PaaS/SaaS, 이후 FaaS 추가)로 정의된다. 한국 클라우드컴퓨팅법(2021.9 시행)은 공공부문의 클라우드 이용을 의무화하고, CSAP(Cloud Security Assurance Program) 인증 체계를 통해 가용성·기밀성·무결성을 검증한다.

```text
+---------------------------------------------------------------------+
|                  전통 On-Premise 아키텍처 vs Cloud-Native            |
+---------------------------------------------------------------------+
|                                                                     |
|   [On-Premise 3-Tier]                  [Cloud-Native 12-Factor]     |
|   +------------------+                +--------------------------+  |
|   |   Web Server     |                |  CDN (CloudFront/Akamai) |  |
|   |  (Apache/Nginx)  |                +----------+---------------+  |
|   +--------+---------+                           v                  |
|            v                         +--------------------------+  |
|   +------------------+               |  API Gateway / WAF       |  |
|   |   App Server     |               +----------+---------------+  |
|   |  (Tomcat/WAS)    |                          v                  |
|   +--------+---------+               +--------------------------+  |
|            v                         |  ALB/NLB (L7/L4 LB)     |  |
|   +------------------+               +----------+---------------+  |
|   |   Database       |                          v                  |
|   | (Oracle RAC/SAN) |               +--------------------------+  |
|   +------------------+               |  EKS/AKS/GKE (K8s Pod)  |  |
|                                      |  + HPA/VPA/Cluster Autoscaler |
|  ✗ Scale-Up 한계                      +----------+---------------+  |
|  ✗ CAPEX 선투자 6~12개월                          v                  |
|  ✗ DR Site 별도 구축                  +--------------------------+  |
|  ✗ 라이선스 종속                      |  Microservices (REST/gRPC)|  |
|  ✗ MTTR 평균 4시간+                   |  + Circuit Breaker/Saga  |  |
|                                      +----------+---------------+  |
|                                                 v                  |
|                                      +--------------------------+  |
|                                      | Aurora/CosmosDB/DynamoDB |  |
|                                      | (Multi-AZ + Read Replica)|  |
|                                      +--------------------------+  |
|                                                                     |
|   ✓ Scale-Out (수평)                 ✓ Self-Healing 자동복구       |
|   ✓ Provisioning 5분                 ✓ Multi-Region Active-Active |
|   ✓ Pay-as-you-go                    ✓ Immutable Infra (AMI/Image)|
|   ✓ MTTR 30분 (자동화)               ✓ FinOps 비용 최적화         |
+---------------------------------------------------------------------+
```

전통적 모놀리스(Monolithic) 아키텍처는 ① 배포 주기 지연(주 1회), ② 단일 장애점(SPOF) 전파, ③ 트래픽 Spike 대응 불가(Black Friday 등), ④ DB Connection Pool 고갈로 대표되는 4대 고질적 문제점을 안고 있다. 클라우드 아키텍처는 이를 Event-Driven + Stateless + Elasticity 원칙으로 해결한다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "호텔 체인"과 같다. 큰 호텔(데이터센터)을 직접 짓는 대신(On-Premise), 이미 지어진 호텔 방을 빌려 쓰며(Public Cloud), 손님이 늘면 즉시 층을 추가하고(Auto Scaling), 손님이 떠나면 자동 환불(Scale-In)받아 요금을 낭비하지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 4계층 구조는 Physical Infrastructure(Hypervisor: KVM/Xen/Hyper-V 기반 AWS Nitro), Virtualization Layer(VPC/VNet/VPC + Subnet + Route Table + NAT/IGW), Platform Layer(EKS/ECS/AKS/GKE + RDS/Aurora + ElastiCache + S3), Application Layer(Serverless Lambda + API Gateway + Step Functions + EventBridge)로 구성된다.

```text
+--------------------------------------------------------------------------+
|           Multi-Account / Multi-VPC Reference Architecture              |
+--------------------------------------------------------------------------+
|                                                                          |
|  +-AWS Organization (Control Tower / Landing Zone)------------------+   |
|  |                                                                   |   |
|  |  +-Security OU-----+  +-Infrastructure OU-----+  +-Workloads OU-+|   |
|  |  | • GuardDuty     |  |  +-Network Account----+|  | +-Prod VPC-+ ||   |
|  |  | • Security Hub  |  |  | • Transit Gateway  ||  | | Pub/Priv | ||   |
|  |  | • IAM Identity  |  |  | • Network Firewall ||  | | Subnet   | ||   |
|  |  |   Center (SSO)  |  |  | • Direct Connect   ||  | | AZ-a/b/c | ||   |
|  |  | • CloudTrail    |  |  +---------+----------+|  | +----+-----+ ||   |
|  |  | • AWS Config    |  |            |           |  |      |       ||   |
|  |  +-----------------+  |  +---------v----------+|  | +----v-----+ ||   |
|  |                       |  |Shared Services VPC ||  | |Dev VPC   | ||   |
|  |  +-Log Archive OU--+  |  | • ECR (Container)  ||  | +----------+ ||   |
|  |  | • S3 + Glacier  |  |  | • AD/Okta SSO      ||  |              ||   |
|  |  | • KMS CMK       |  |  | • CI/CD (CodeBuild)||  +--------------+|   |
|  |  +-----------------+  |  +--------------------+|                  |   |
|  |                       +------------------------+                  |   |
|  +-------------------------------------------------------------------+   |
|                                                                          |
|  Cross-Region: S3 CRR | Aurora Global DB | Route53 Latency-Based       |
|  DR Strategy: Pilot Light / Warm Standby / Multi-Site Active-Active      |
+--------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Hypervisor Layer (Nitro/KVM)** | 물리 하드웨어 가상화, EC2 인스턴스 격리 | AWS Nitro System: 전용 Nitro Card(DPDK 가속)로 네트워킹·스토리지 I/O 처리, 호스트 CPU 부담 0%로 Performance 30%^, Intel SR-IOV/SmartNIC 기반 100Gbps 대역폭 |
| **Control Plane** | API-driven 인프라 제어, IaC 자동화 | Terraform/OpenTofu(상태파일 State), AWS CloudFormation(Stack Nested), Pulumi(일반 언어), Ansible(설정 관리), ArgoCD(GitOps) — 선언적 HCL/JSON/YAML로 불변 인프라 배포 |
| **Networking Layer** | VPC/VNet, Subnet, Routing, Peering | VPC: 10.0.0.0/16 CIDR, Public/Private/Isolated Subnet 분리, NAT Gateway(아웃바운드), Internet Gateway, VPC Peering(1:1), Transit Gateway(Hub-Spoke), PrivateLink(엔드포인트), Tailscale/Wireguard(Overlay VPN) |
| **Compute Service** | 컨테이너·서버리스 오케스트레이션 | EKS/AKS/GKE: Kubernetes 1.30+ (CNI Calico/Cilium, Service Mesh Istio/Linkerd), Karpenter(노드 프로비저닝), KEDA(EDA 스케일링); Lambda: 15분 timeout, 10GB memory, 1000 동시성, Cold Start 200~800ms |
| **Storage & Database** | 영구/비영구 데이터, 분산 트랜잭션 | S3(11 9s 내구성, 99.99% 가용성, Lifecycle IA->Glacier), EBS(gp3 3000 IOPS/125MB/s baseline), Aurora(MySQL/Postgres 5x RDS 성능, 6-way 복제), DynamoDB(Single-digit ms p99, Global Tables), Cosmos DB(Multi-Model 5 consistency level) |
| **Edge & CDN** | 글로벌 정적 콘텐츠 캐싱, DDoS 방어 | CloudFront(750+ PoP, Lambda@Edge, Origin Shield), Cloudflare Magic Transit(L3/L4 DDoS 100Tbps 흡수), AWS Global Accelerator(Anycast IP) — TTL 기반 캐시 무효화, Stale-While-Revalidate 패턴 |
| **Observability Stack** | Metrics/Logs/Traces 통합 관제 | OpenTelemetry(OTel SDK), Prometheus + Grafana, ELK/EFK Stack, AWS CloudWatch + X-Ray(분산 트레이싱), Datadog/New Relic(APM SaaS), SLO/SLI 기반 Error Budget 산정 |

**Well-Architected Framework 5 Pillar 상세**:
1. **Operational Excellence**: IaC 100% 적용, CI/CD Pipeline(GitHub Actions/CodePipeline), Runbook 자동화, 무중단 배포(Blue-Green/Canary 10%->50%->100%)
2. **Security**: Defense in Depth(Network/System/Application/Data), Zero Trust(IAM + MFA + mTLS), KMS Envelope Encryption, Secrets Manager + Rotation, WAF OWASP Top 10 룰
3. **Reliability**: Multi-AZ 기본(2N+1, N+1), Circuit Breaker(Hystrix/Resilience4j), Health Check(Liveness/Readiness), Chaos Engineering(LitmusChaos, AWS Fault Injection Service)
4. **Performance Efficiency**: Right-Sizing(Vantage/Turbonomic), Caching 전략(Read-Through/Write-Behind/Refresh-Ahead), CDN 정적자원 오프로드, Database Connection Pool(HikariCP size = (core_count × 2) + effective_spindle_count)
5. **Cost Optimization**: FinOps 팀 운영, Reserved/Spot/Savings Plans 혼용(70/20/10 Rule), S3 Intelligent-Tiering, Compute Optimizer 권고, Cost Anomaly Detection ML

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 5 Pillar는 "비행기 안전 점검 5종 세트"와 같다 — 기체 구조(Reliability), 연료 효율(Performance Efficiency), 관제탑 운영(Operational Excellence), 보안 검색(Security), 연료비 관리(Cost Optimization) — 어느 하나라도 빠지면 추락한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **IaaS (EC2, Azure VM)** | **PaaS (Beanstalk, App Engine)** | **SaaS (Salesforce, Office 365)** | **FaaS/Serverless (Lambda, Cloud Functions)** |
| :--- | :--- | :--- | :--- | :--- |
| **제어 범위** | OS, Middleware, Runtime 모두 제어 | Application/Data만 제어 | 사용자는 설정만 | Function 코드만 |
| **확장성** | 수동/스크립트 기반 Auto Scaling | Platform 제공 자동 확장 | SaaS 제공자 정책 | 밀리초 단위 자동 확장(0~1000) |
| **과금 단위** | 인스턴스 시간(per second) | 인스턴스 시간 + 서비스 사용량 | User/월 구독 | 요청 수 + GB-Second(100ms 단위) |
| **Cold Start** | 없음 (상시 기동) | 없음 (Warm Pool) | 없음 | 100ms~3초 (Provisioned Concurrency로 해결) |
| **적합 워크로드** | 레거시 Lift&Shift, 커스텀 OS | 웹앱 표준 배포, API Backend | CRM, 협업툴, ERP | Event-driven, 간헐적 워크로드, Batch |
| **Lock-in 위험** | 중간 (AMI로 이전 가능) | 높음 (Vendor SDK 종속) | 최고 (Data Egress 비용) | 최고 (벤더 종속 API/이벤트 소스) |

**Cloud Migration 6 Rs 전략** (AWS Migration Hub 기준):
- **Rehost (Lift & Shift)**: 그대로 이동, 빠르지만 ROI 낮음 (예: VM Import/Export, AWS Application Migration Service)
- **Replatform**: 최소 변경(예: SQL Server -> Aurora MySQL, WebLogic -> Tomcat)
- **Refactor/Re-architect**: Cloud-Native 재설계(예: Monolith -> Microservices, 12-Factor App)
- **Repurchase**: SaaS 전환(예: Custom CRM -> Salesforce)
- **Retire**: 사용하지 않는 워크로드 폐기(DataDog, CloudHealth로 미사용 자원 탐지)
- **Retain**: 보안/규제로 On-Prem 유지(예
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 661 / 800

<- **이전**: [660. 클라우드 아키텍처 핵심 토픽 660번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/660_cloud_architecture_core_topic_660_exam_summar/)
**다음**: [662. 클라우드 아키텍처 핵심 토픽 662번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/662_cloud_architecture_core_topic_662_exam_summar/) ->

---
