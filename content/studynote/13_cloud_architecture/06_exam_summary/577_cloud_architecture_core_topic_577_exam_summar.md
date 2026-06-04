---
title: "577. 클라우드 아키텍처 핵심 토픽 577번 시험 요약 (Cloud Architecture Core Topic 577 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


# 577. 클라우드 아키텍처 핵심 토픽 577번 시험 요약 (Cloud Architecture Core Topic 577 Exam Summary)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 퍼블릭·프라이빗·하이브리드·멀티 클라우드를 아우르는 IaaS/PaaS/SaaS/FaaS/SaaS의 책임 분계 모델(EAM: Enterprise Architecture Model)과 12-Factor App, Well-Architected Framework(AWS·Azure·GCP 공통 5~6개 축), CAP/ACID 트레이드오프, 컨트롤 플레인/데이터 플레인 분리, 셀프서비스 API 기반의 선언적 프로비저닝(Declarative Provisioning)을 결합한 **클라우드 네이티브(Cloud-Native) 컴퓨팅 패러다임**이다.
> 2. **가치**: CapEx->OpEx 전환(일반적으로 30~60% TCO 절감), Auto Scaling을 통한 Peak 대비 40~70% Capacity 우회, Multi-AZ·Multi-Region 구성을 통한 99.99%(Four-Nines) 이상의 가용성, 컨테이너 오케스트레이션(Kubernetes)을 통한 배포 빈도 10배^·복구시간(MTTR) 1/10v 달성, GitOps·Policy as Code(OPA/Kyverno)를 통한 Governance 자동화로 **민첩성·탄력성·관측가능성(Observability)·보안·비용 최적화의 5대 Well-Architected 기둥**을 확보한다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs 멀티/하이브리드(상호운용성/Interop), Stateful 워크로드의 Stateless 마이그레이션, 동기 복제(Strong Consistency) vs 비동기 복제(Eventual Consistency)의 트레이드오프, Cold/Warm/Hot DR 전략별 RPO·RTO·비용 Δ, Egress 요금·Data Gravity·Latency를 고려한 Region·AZ 배치, IaC(Terraform·Pulumi·CDK) 표준화 및 FinOps(Cloud Financial Management) 성숙도, **"Lift & Shift" -> "Replatform" -> "Refactor" -> "Rearchitect" 6R 마이그레이션 전략** 중 워크로드 특성에 맞는 단계 선택이 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스(Enterprise Datacenter) 컴퓨팅 환경은 **수직 확장(Scale-Up)**, **장기 투자(CapEx)**, **수동 운영(Manual Ops)**, **고정 용량(Fixed Capacity)**의 한계를 가진다. 비즈니스 트래픽이 평일 09:00~18:00에만 집중되고 나머지 시간에 유휴(Idle) 자원이 발생함에도, Peak Load 기준으로 HW를 발주해야 하므로 **자원利用率 15~20%**에 불과하다. 더 나아가 HW 도입 리드타임 6~12주, EOL(End-of-Life) 교체 사이클 3~5년, IDC 전력·냉각·회선 비용의 7~10% 연상승률, 그리고 BCP/DR을 위한 이중화(Hot-Standby) 비용은 SI(시스템 통합) 프로젝트의 ROI를 지속적으로 악화시킨다.

NIST SP 800-145(2011)는 클라우드를 **"네트워크, 서버, 스토리지, 애플리케이션, 서비스 등 구성 가능한 컴퓨팅 자원의 공유 풀(Shared Pool)로, 최소한의 관리 노력이나 서비스 제공자 상호작용으로 신속히 프로비저닝 및 해제 가능한 온디맨드(self-service on-demand), 광대역 네트워크 접근(broadband network access), 자원 풀링(resource pooling), 신중한 탄력성(rapid elasticity), 측정 가능한 서비스(measured service)의 5대 필수 특성을 가진 모델"**로 정의한다. 이는 컴퓨팅 자원을 **"전기·수도처럼 사용하는 Utility Computing"** 패러다임으로 전환하며, 가상화(VMware vSphere, KVM, Xen) -> 컨테이너(Docker, containerd) -> 오케스트레이션(Kubernetes, ECS) -> 서버리스(Lambda, Cloud Run) -> 엣지(Cloudflare Workers, Lambda@Edge)로 진화해 왔다.

```text
+---------------------------------------------------------------------+
|                  On-Premise -> Cloud Evolution Paradigm              |
+---------------------------------------------------------------------+
|                                                                     |
|  1980s~1990s (Mainframe/Client-Server)        2000s (Virtualization)
|  +----------------------+                     +------------------+  |
|  | Physical Server HW   |   ---- Hypervisor --->| vSphere / KVM    |  |
|  | Monolithic App       |                     | VM (Guest OS)    |  |
|  | Dedicated Capacity   |                     | Consolidation 4:1|  |
|  +----------------------+                     +------------------+  |
|          | CapEx 100%                                     |          |
|          v                                                v          |
|  2010s (Public/Private Cloud)                2015~ (Container Native)|
|  +----------------------+                     +------------------+  |
|  | IaaS (EC2/VM)        |   ---- Docker ----> | Kubernetes Pod   |  |
|  | PaaS (BeanStalk)     |                     | Microservice     |  |
|  | Auto Scaling Group   |                     | HPA/VPA/Cluster  |  |
|  +----------------------+                     +------------------+  |
|          | OpEx Pay-as-you-go                            |          |
|          v                                                v          |
|  2020s (Serverless & Edge)                  2024+ (AI-Native Cloud)|
|  +----------------------+                     +------------------+  |
|  | FaaS (Lambda/Func.)  |   ---- LLMs -------> | GPU Pool (A100)  |  |
|  | Event-Driven         |                     | Vector DB (RAG)  |  |
|  | BaaS (S3/Dynamo)     |                     | MLOps (KubeFlow) |  |
|  +----------------------+                     +------------------+  |
+---------------------------------------------------------------------+
```

클라우드가 필수가 된 핵심 동인은 ①**디지털 전환(DX) 가속** — MZ세대 모바일 트래픽 폭증·글로벌 서비스·탄력적 프로모션, ②**데이터 폭증** — 5G·IoT·AI 학습 데이터의 페타바이트화, ③**비용 효율화** — IDC 운영 1인당 50~80대 서버 관리 한계, ④**BCP/DR 강화** — 코로나19·재난·랜섬웨어 대비 원격·이중화, ⑤**신기술 도입 가속** — 생성형 AI·블록체인·양자컴퓨팅을 CapEx 투자 없이 즉시 사용, ⑥**규제 컴플라이언스** — 클라우드 보안 인증(CSAP·ISO 27001·SOC 2·PCI-DSS)·개인정보보호법·가상자원 통제법(클라우드컴퓨팅법) 대응이다.

**On-Premise vs Cloud 비교**

| 평가 축 | On-Premise | Public Cloud (IaaS) | Hybrid/Multi-Cloud |
|---|---|---|---|
| 투자비 | CapEx 100% (초기 5억+) | OpEx 0원 (사용량 과금) | 양쪽 혼합 |
| 확장성 | HW 발주 6~12주 | Auto Scaling 분 단위 | Burst 시 Public 사용 |
| 가용성 | Tier-III 99.982% | Multi-AZ 99.99% / Region 99.999% | DR Site로 활용 |
| TCO (3년) | 100% 기준 | 30~50% (가상 시) | 40~60% |
| 거버넌스 | 완전 통제 | Shared Responsibility | Policy Bridge |
| Lock-in 위험 | 없음 | 높음 (전환비용 12~24개월) | 중간 (추상화 계층 필요) |

- **📢 섹션 요약 비유**: 클라우드는 **"전기 회사"**와 같다. 과거에는 각 가정·공장이 **자신만의 발전기(Diesel Generator)**를 돌렸지만, 오늘날은 **전력 그리드(Grid)**에 연결해 켜진 전구(Watt)만큼만 요금을 내고, 정전·과부하 걱정 없이 즉시 스위치를 누르면 된다. 데이터센터는 발전소, Auto Scaling은 자동 변압기, Multi-Region은 송전선 백업에 해당한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **5계층 참조 모델**(Physical -> Virtualization -> Service -> Application -> Workload)과 **2개 플레인 분리**(Control Plane / Data Plane)로 추상화된다. CNCF(Cloud Native Computing Foundation)는 Cloud-Native를 "**컨테이너, 서비스 메시, 마이크로서비스, 불변 인프라(Immutable Infra), 선언적 API(Declarative API)**를 활용하여 **자동화·관측가능성·반복가능성·회복력(Resilience)**을 갖춘 느슨하게 결합된(Loosely Coupled) 시스템"으로 정의한다.

```text
+----------------------------------------------------------------------+
|            Cloud Reference Architecture (NIST + AWS Well-Arch.)     |
+----------------------------------------------------------------------+
|                                                                      |
|   +------------------------------------------------------------+     |
|   | Layer 5: Workload / Application Tier (SaaS / 12-Factor)   |     |
|   |  +- Web/Mobile App  +- API Gateway  +- BFF  +- Streaming   |     |
|   |  +- SaaS (Slack, Salesforce) +- GenAI (Bedrock/Vertex)    |     |
|   |  +- Identity (OAuth2/OIDC/SAML/JWT)                       |     |
|   +------------------------------------------------------------+     |
|   +------------------------------------------------------------+     |
|   | Layer 4: Service / Platform Tier (PaaS / Serverless)       |     |
|   |  +- App Service / Elastic Beanstalk / Cloud Run / App Eng. |     |
|   |  +- FaaS (Lambda / Azure Functions / Cloud Functions)      |     |
|   |  +- Message Bus (SQS / SNS / Pub/Sub / EventBridge / Kafka)|     |
|   |  +- BaaS (Auth0 / Firebase / AWS Cognito / Supabase)      |     |
|   +------------------------------------------------------------+     |
|   +------------------------------------------------------------+     |
|   | Layer 3: Data & Storage Tier                               |     |
|   |  +- RDB (Aurora / Cloud SQL / Cosmos DB) [OLTP, ACID]      |     |
|   |  +- NoSQL (DynamoDB / Firestore / Mongo Atlas) [BASE]      |     |
|   |  +- Object (S3 / GCS / Blob) [11 9s Durability]           |     |
|   |  +- Warehouse (Redshift / BigQuery / Snowflake) [OLAP]     |     |
|   |  +- Lake (S3+Lake Formation / Delta Lake / Iceberg)        |     |
|   +------------------------------------------------------------+     |
|   +------------------------------------------------------------+     |
|   | Layer 2: Compute / Container Tier (IaaS / CaaS)            |     |
|   |  +- VM (EC2 / Compute Engine / VM Scale Set)               |     |
|   |  +- Container (EKS / GKE / AKS / ECS Fargate)              |     |
|   |  +- Bare-Metal / GPU (P4d / A100 / Trainium)               |     |
|   |  +- Edge (Lambda@Edge / Cloudflare Workers / IoT Greengrass)|    |
|   +------------------------------------------------------------+     |
|   +------------------------------------------------------------+     |
|   | Layer 1: Network & Foundation Tier                         |     |
|   |  +- VPC / VNet / GCP VPC (CIDR 10.0.0.0/16)                |     |
|   |  +- Subnet (Public/Private/TGW), NACL/SG, NAT GW/IGW       |     |
|   |  +- Load Balancer (ALB/NLB/CLB, Application GW)            |     |
|   |  +- DNS (Route53 / Cloud DNS / Traffic Manager)             |     |
|   |  +- CDN (CloudFront / Cloud CDN / Front Door)              |     |
|   |  +- Interconnect (Direct Connect / ExpressRoute / Interco.) |     |
|   +------------------------------------------------------------+     |
|                                                                      |
|   +------------------------------------------------------------+     |
|   | Cross-Cutting: Observability & Security & FinOps           |     |
|   |  +- Monitoring (CloudWatch / Stackdriver / Azure Monitor)   |     |
|   |  +- Logging (CloudTrail / Fluentd / Loki)                  |     |
|   |  +- Tracing (X-Ray / OpenTelemetry / Jaeger)               |     |
|   |  +- IAM (RBAC / ABAC / SSO / SCIM / KMS / HSM)            |     |
|   |  +- SecOps (GuardDuty / Security Center / Chronicle)       |     |
|   |  +- FinOps (Cost Explorer / Budgets / CUR / Anomaly Det.)  |     |
|   +------------------------------------------------------------+     |
|                                                                      |
|   +------------------------------------------------------------+     |
|   | Control Plane (Global,  ┄┄┄ Data Plane (Regional/AZ)       |     |
|   | 관리/제어/메타)            데이터 평면/실제 트래픽)            |     |
|   |  +- IAM Policies         +- VM/Container 실제 데이터 패킷     |     |
|   |  +- Route53 GeoDNS       +- Storage 실제 Read/Write         |     |
|   |  +- Auto Scaling Trigger +- Lambda 실제 실행 코드            |     |
|   |  +- API (REST/gRPC)      +- Network 실제 경로                |     |
|   +------------------------------------------------------------+     |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Region & Availability Zone (AZ)** | 지리적 격리 단위 | Region(국가·대륙 단위, 100km 이상 이격), AZ(1개 Region 내 2~6개 DC, 광케이블 연결, 99.99% SLA). ex) ap-northeast-2(서울) Region = a·b·c·d 4개 AZ |
| **Virtual Private Cloud (VPC)** | 논리적 사설 네트워크 | SDN 기반 격리, CIDR(/16 권장)·Subnet(/24)·Route Table·Internet Gateway(IGW)·NAT Gateway·Egress-only IGW, AWS Network Firewall·Azure Firewall 등 5-tuple 기반 보안그룹(SG)/NACL |
| **Elastic Load Balancer (ELB)** | 트래픽 분산·헬스체크 | L4 NLB(TCP/UDP, µs 지연, Static IP) vs L7 ALB(HTTP/HTTPS/gRPC, Path/Host/Header 라우팅, WAF 통합). Cross-Zone LB, Sticky Session, Connection Draining |
| **Auto Scaling Group (ASG)** | 탄력적 Capacity | 3가지 스케일링: **Reactive**(CPU/Queue 지표 -> CloudWatch Alarm), **Predictive**(ML 기반 시계열 예측, AWS Predictive Scaling), **Scheduled**(Cron/
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 577 / 800

<- **이전**: [576. 클라우드 아키텍처 핵심 토픽 576번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/576_cloud_architecture_core_topic_576_exam_summar/)
**다음**: [578. 클라우드 아키텍처 핵심 토픽 578번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/578_cloud_architecture_core_topic_578_exam_summar/) ->

---
