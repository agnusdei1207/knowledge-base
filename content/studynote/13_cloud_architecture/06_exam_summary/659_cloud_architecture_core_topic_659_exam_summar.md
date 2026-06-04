---
title: "659. 클라우드 아키텍처 핵심 토픽 659번 시험 요약 (Cloud Architecture Core Topic 659 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST 참조모델(CCRA) 기반의 IaaS/PaaS/SaaS/FaaS 서비스 계층과 Public/Private/Hybrid/Multi-Cloud 배치 모델을 결합하여, 12-Factor App 원칙·Microservices·Container Orchestration(Kubernetes)·Service Mesh(Istio/Linkerd)·Event-Driven(EDA) 패턴을 통해 `탄력성(Elasticity)`, `확장성(Scalability)`, `가용성(Availability)`을 코드/정책으로 구현하는 클라우드 네이티브 설계 패러다임이다.
> 2. **가치**: AWS Well-Architected 5대 기둥(운영 우수성·보안·신뢰성·성능 효율·비용 최적화) 적용 시, On-Prem 대비 인프라 조달 시간 **6~12개월 -> 5분 이내**, Auto-Scaling을 통한 트래픽 처리 능력 **수 배~수십 배**, CapEx->OpEx 전환으로 TCO **30~50% 절감**, IDC 보고서 기준 글로벌 퍼블릭 클라우드 시장 2027년 **1.5조 USD 규모**의 사업적 임팩트를 창출한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ① **Cloud Native vs Lift & Shift** (Application Re-architect vs Rehost), ② **Single Cloud vs Multi-Cloud** (벤더 종속·Lock-in vs 이기종 운영 복잡도), ③ **Monolith vs Microservices** (운영 단순성 vs 독립 배포/확장), ④ **Eager vs Lazy Migration(Strangler Fig Pattern)** 이며, **6R 전략(Rehost/Replatform/Refactor/Repurchase/Retire/Retain)**과 CAF(Cloud Adoption Framework), FinOps 성숙도 모델을 근거로 워크로드별 최적 배치 모델·서비스 모델을 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적 On-Premise IT는 CapEx(Capital Expenditure) 기반의 정적 용량 설계, 수직 확장(Scale-Up)의 한계, 수동 패치/장애 대응, HW 도입 리드타임 8~16주 등의 구조적 한계를 가진다. 디지털 전환(DX)·4차 산업혁명 시대를 맞아 트래픽 변동성이 극대화되고, AI/ML·IoT·빅데이터 워크로드가 폭증하면서, **5G·모바일 First 환경**에서 분 단위 Auto-Scaling, **Pay-as-you-go** 과금, 글로벌 엣지 배포가 가능한 **클라우드 컴퓨팅**이 선택이 아닌 필수가 되었다.

NIST SP 500-292(2011) 「Cloud Computing Reference Architecture(CCRA)」는 클라우드를 **5대 핵심 특성**(On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)과 **3대 서비스 모델**(IaaS/PaaS/SaaS), **4대 배치 모델**(Public/Private/Hybrid/Community)로 정의하며, 이 표준이 한국 정보관리기술사·컴퓨터시스템응용기술사 시험의 토대이다.

```text
+------------------------------------------------------------------+
|                클라우드 컴퓨팅 패러다임 전환 개념도               |
+------------------------------------------------------------------+
|                                                                  |
|  [On-Premise 전통 모델]              [Cloud-Native 신규 모델]     |
|  +-----------------+                +-----------------+          |
|  | Application     |                | Container/Pod   |  <- K8s  |
|  | --------------- |                | Microservice    |          |
|  | Middleware      |                | Service Mesh    |  <- Istio|
|  | OS              |                | Serverless Fn   |  <- Lambda|
|  | Virtualization  |                | Managed DB/Svc  |  <- RDS  |
|  | Server / Storage|                | Infra as Code   |  <- TF   |
|  | Network / SAN   |                | Region/Edge PoP |  <- CDN  |
|  +-----------------+                +-----------------+          |
|        |                                      |                   |
|   CapEx 일시 투자                       OpEx 사용량 과금           |
|   HW 수명 3~5년                        무한 수직+수평 확장        |
|   수동 운영·장애대응                    IaC·GitOps 자동화          |
|   트래픽 = Peak 기준 과다설계            Auto-Scaling 수요대응      |
|   단일 IDC 위치                         Multi-Region/Edge         |
+------------------------------------------------------------------+
```

```text
[NIST CCRA 클라우드 참조 아키텍처 계층]
+------------------------------------------------------------+
|  Cloud Consumer (사용자) -- Broker Service (중개) -- Provider|
|                                                              |
|  +--- Cloud Services Layer -----------------------------+  |
|  |  SaaS  : Gmail, Office365, Salesforce, Slack          |  |
|  |  PaaS  : EKS, App Engine, Beanstalk, Heroku, Lambda  |  |
|  |  IaaS  : EC2, S3, VPC, Azure VM, GCE, NLB, EBS      |  |
|  |  FaaS  : Lambda, Azure Functions, Cloud Functions     |  |
|  |  CaaS  : EKS/AKS/GKE, ECS, Cloud Run                  |  |
|  +------------------------------------------------------+  |
|  +--- Resource Abstraction Layer (가상화/추상화) -------+  |
|  |  KVM, Xen, Hyper-V, Docker, cgroup/namespace          |  |
|  |  Software-Defined Network (SDN), SDS, SDN-WAN         |  |
|  +------------------------------------------------------+  |
|  +--- Physical Resource Layer (물리 자원) --------------+  |
|  |  Server, Storage, Network, Datacenter, Region/AZ/Edge |  |
|  +------------------------------------------------------+  |
+------------------------------------------------------------+
```

**왜 필요한가?**
- **민첩성(Agility)**: 인프라 Provisioning 시간 8주 -> 5분 (AWS CloudFormation/Terraform 기준)
- **글로벌 확장성**: 1회 클릭으로 30+ Region, 100+ Edge Location 배포 (CloudFront/Akamai/Cloudflare)
- **탄력성**: CPU 사용률 80% 시 Auto-Scaling Group(ASG)이 인스턴스 1->100대 자동 증설
- **비용 최적화**: Spot/Preemptible Instance로 70~90% 할인, RI/Savings Plan으로 1~3년 약정 시 30~60% 절감
- **고가용성**: Multi-AZ(Availability Zone)·Multi-Region Active-Active로 99.99~99.999% SLA 확보

- **📢 섹션 요약 비유**: 클라우드 컴퓨팅은 마치 **"수도관 시스템"**과 같다. 종전에는 각 가정마다 우물을 팠지만(On-Premise), 지금은 수도관에 연결만 하면 끝(클라우드). 사용량에 따라 수도 요금이 자동 정산되고(Pay-per-use), 수도관이 끊겨도 자동 우회(Auto-Scaling)된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 크게 **① 컴퓨트/스토리지/네트워크 서비스 계층**, **② 관리·자동화 계층**, **③ 보안·거버넌스 계층**으로 나뉘며, 각각은 API·IaC(Infrastructure as Code)·GitOps 방식으로 선언적(Declarative) 제어가 가능하다.

```text
[클라우드 아키텍처 3계층 + Cross-Cutting Concern 상세도]
+---------------------------------------------------------------------+
|  Layer 1: 서비스 활용 계층 (Service Consumption Layer)               |
|  +-------------+-------------+-------------+-------------+          |
|  | SaaS        | FaaS        | CaaS        | PaaS        |          |
|  | Workday     | Lambda      | EKS/AKS/GKE | Beanstalk   |          |
|  | Office365   | Cloud Func  | ECS/Fargate | App Engine  |          |
|  | Salesforce  | Step Func   | Cloud Run   | Heroku      |          |
|  +-------------+-------------+-------------+-------------+          |
+---------------------------------------------------------------------+
|  Layer 2: 플랫폼/데이터/통합 계층                                   |
|  +----------+----------+----------+----------+----------+           |
|  | Container| Service  | API GW   | MQ/EDA   | DBaaS    |           |
|  | Runtime  | Mesh     | Kong     | Kafka    | RDS/Aurora|          |
|  | Docker   | Istio    | Apigee   | SQS/SNS  | DynamoDB |           |
|  | Pod/CRI  | Linkerd  | CloudFront| Pub/Sub | Cosmos   |           |
|  +----------+----------+----------+----------+----------+           |
+---------------------------------------------------------------------+
|  Layer 3: 인프라 추상화/물리 계층 (IaaS + Physical)                 |
|  +----------+----------+----------+----------+----------+           |
|  | Compute  | Storage  | Network  | Edge/CDN | Bare-Mtl |           |
|  | EC2/VM   | S3/Blob  | VPC/VNet | CloudFront| Graviton |          |
|  | Bare-Mtl | EBS/Disk | TGW/Peering| Lambda@Edge| FPGA/GPU|          |
|  | Lambda   | EFS/FSx  | PrivateLink| WAF    | Trainium |          |
|  +----------+----------+----------+----------+----------+           |
+---------------------------------------------------------------------+
|  Cross-Cutting Concerns (횡단 관심사)                                |
|  +----------+----------+----------+----------+----------+           |
|  | IaC/GitOps| Security | Observ.  | FinOps   | DR/BCM   |           |
|  | TF/CDK   | IAM/KMS  | Prom/Graf| CUR/CMDB | Backup/SR|           |
|  | Pulumi   | WAF/Shield| ELK/Loki | CostExp  | PilotLight|          |
|  | Ansible  | ZeroTrust| Jaeger   | Karpenter| Multi-Rgn|           |
|  +----------+----------+----------+----------+----------+           |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 서비스** | 워크로드 실행 환경 제공, 가상화·컨테이너·서버리스 추상화 | EC2(VM), Lambda(Serverless), EKS(K8s), Fargate(Serverless K8s); Instance Type(M/T/C/R/G/P/X 시리즈)별 CPU·Memory·네트워크·가속기(GPU/FPGA/Trainium) 자원 분리; Spot·On-Demand·Reserved·Savings Plan·Dedicated Host 5종 과금 모델 |
| **스토리지 서비스** | 데이터 영속성·내구성·접근성 제공, Hot/Warm/Cold 계층화 | S3(Object, 11 9s 내구성, IA/Glacier Deep Archive로 GB당 $0.00099/월), EBS(Block, gp3/io2), EFS(NFS), FSx(Lustre/ONTAP/Windows), DynamoDB(Key-Value NoSQL, p99 1ms), Aurora(MySQL/PostgreSQL 호환, 5× MySQL, 3× PostgreSQL 성능) |
| **네트워크 서비스** | Region-AZ-VPC-Subnet 계층, L4/L7 분리, 글로벌 트래픽 관리 | VPC/Subnet(RFC1918 10.0.0.0/8), TGW(Transit Gateway, 최대 5,000 VPC 피어링), PrivateLink(Private API), NLB(L4, 초당 수백만 PPS), ALB(L7, Path/Host/Header 라우팅), Route 53(Latency/Weighted/Geolocation), CloudFront(250+ Edge, Lambda@Edge) |
| **관리·자동화 계층** | IaC·GitOps·정책 as 코드, 선언적 인프라 관리 | Terraform(HCL 모듈식 멀티클라우드), AWS CDK(TypeScript/Python), Pulumi, Ansible/Puppet/Chef(설정), ArgoCD/Flux(GitOps), Crossplane(K8s-native IaC), OPA(Open Policy Agent, Rego 정책), Atlantis(Terraform PR 자동화) |
| **보안·거버넌스 계층** | Zero Trust, 공유 책임 모델, 암호화·IAM·컴플라이언스 | IAM(RBAC+ABAC), KMS/HSM(Envelope Encryption), Secrets Manager/Parameter Store, WAF(SQLi/XSS 룰셋), GuardDuty(ML 위협 탐지), Security Hub(통합 대시보드), CloudTrail(API Audit), Macie(PII/DLP), SCP(Service Control Policy), Confused Deputy 방지 |
| **관찰가능성(Observability)** | Metrics·Logs·Traces 통합, SLI/SLO/SRE | Prometheus(메트릭 수집, 200+ Exporter), Grafana(시각화), Loki(로그 집계), Tempo/Jaeger(분산 트레이싱), OpenTelemetry(표준 SDK), AWS X-Ray, CloudWatch, Datadog/New Relic(SaaS형 APM) |
| **FinOps 계층** | 클라우드 비용 가시화·최적화·예산 통제 | AWS Cost Explorer·CUR, Azure Cost Management, GCP Billing, CloudHealth·Vantage·Apptio, Karpenter(비용 최적 노드 프로비저닝), Spot.io, Spotinst/CAST.ai, Savings Plan·RI 권장 엔진 |

**핵심 동작 원리 및 파라미터**

1. **탄력성(Elasticity) 알고리즘**: AWS Auto Scaling은 CloudWatch Metric(예: `CPUUtilization > 70%`) 기반의 Target Tracking, Step Scaling, Simple Scaling, Scheduled Scaling, Predictive Scaling 5가지 정책 제공. **Predictive Scaling**은 ML 기반(Holt-Winters, ARIMA) 트래픽 예측으로 2~3일치 선제 증설.
2. **가용성(Availability) 수식**: 직렬 시스템 가용성 = `Π(1 - MTTR_i / MTBF_i)`. 3-Tier Web/WAS/DB를 단일 AZ에 두면 99.5%, Multi-AZ 이중화 시 99.95%, Multi-Region Active
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 659 / 800

<- **이전**: [658. 클라우드 아키텍처 핵심 토픽 658번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/658_cloud_architecture_core_topic_658_exam_summar/)
**다음**: [660. 클라우드 아키텍처 핵심 토픽 660번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/660_cloud_architecture_core_topic_660_exam_summar/) ->

---
