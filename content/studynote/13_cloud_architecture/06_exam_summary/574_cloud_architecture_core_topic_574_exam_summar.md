---
title: "Cloud Architecture Core Topic 574 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS·PaaS·SaaS·FaaS의 서비스 모델 계층화와 Public·Private·Hybrid·Multi-Cloud 배포 모델의 조합을 통해, API 기반 선언적 프로비저닝(CloudFormation/Terraform), 컨테이너 오케스트레이션(Kubernetes/EKS/AKS/GKE), 서버리스 컴퓨팅(Lambda/Cloud Functions), IaC, GitOps를 핵심 추상화로 다루는 분산 시스템 설계 패러다임이다.
> 2. **가치**: CapEx->OpEx 전환(평균 30~40% TCO 절감), 탄력적 Auto-Scaling으로 트래픽 피크 시 5~20배 용량 확장, 가용성 SLA 99.99%(연 52.6분 이하 장애) 달성, MTTR 평균 70% 단축, 글로벌 리전 간 Active-Active 구성으로 RPO 0/RTO 분 단위 확보가 가능하다.
> 3. **판단 포인트**: 6R 마이그레이션 전략(Rehost/Replatform/Refactor/Re purchase/Retire/Retain) 선택, Egress 비용·데이터 주권·Vendor Lock-in·네트워크 레이턴시·컴플라이언스(CSAP/ISO27001/SOC2)·FinOps 거버넌스 간의 트레이드오프를 정량적 의사결정 프레임워크로 풀어야 한다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스(On-Premise) 엔터프라이즈 시스템은 전용 하드웨어 구매, 수직 확장(Scale-Up)의 한계, CAPEX 중심의 선투자, 수동 패치 및 용량 계획, IDC 공간·전력·냉각 제약 등 구조적 한계를 가진다. 2006년 AWS S3·EC2 출시 이후 클라우드 컴퓨팅은 인프라 추상화(Infrastructure Abstraction), API-Driven 오케스트레이션, 다중 테넌트(Multi-Tenancy), 분산 스토리지, Software-Defined Networking을 통해 컴퓨팅 자원을 "필요한 만큼, 사용한 만큼" 소비하는 유틸리티 컴퓨팅 모델로 진화했다.

NIST SP 800-145(2011)는 클라우드를 "네트워크, 서버, 스토리지, 애플리케이션, 서비스 등 공유 가능한 컴퓨팅 자원을 최소한의 관리 노력으로 신속히 provisioning·release 가능한 ubiquitous·convenient·on-demand 네트워크 접근 모델"로 정의하며, 5대 필수 특성(온디맨드 셀프서비스, 광대역 네트워크 접근, 리소스 풀링, 빠른 탄력성, 측정 가능한 서비스)을 명시했다. 2020년대 들어 Kubernetes의 CNCF 표준화, Service Mesh(Istio/Linkerd), eBPF 기반 관측 가능성(Observability), FinOps, Sustainability(탄소감축)까지 아우르는 Cloud-Native Computing 재정의가 진행 중이다.

```text
+------------------------------------------------------------------------+
|            클라우드 아키텍처의 진화 패러다임 비교 (On-Prem -> Cloud)    |
+------------------------------------------------------------------------+

  [On-Premise Era 2000s]              [Cloud Era 2010s]
  +----------------------+            +----------------------+
  |  Application         |            |  Microservices       |
  |  v                   |            |  Containers(K8s)     |
  |  Middleware (WAS)    |   ---►     |  Serverless(FaaS)    |
  |  v                   |            |  v                   |
  |  Hypervisor (VMware) |            |  Public/Private Cloud|
  |  v                   |            |  Multi/Hybrid Cloud  |
  |  Bare-Metal Server   |            |  Edge Computing      |
  |  SAN / NAS Storage   |            |  Object Storage(S3)  |
  |  L4/L7 HW Switch     |            |  SD-WAN / VPC        |
  +----------------------+            +----------------------+
  • CapEx 100% 선투자                 • OpEx 종량제(Pay-as-you-go)
  • 수직확장 한계 (CPU/RAM)           • 수평확장(Horizontal) 무제한
  • 배포주기: 6~12개월                • 배포주기: 1일 ~ 수시
  • 가용성 99.9% (수동DR)             • 가용성 99.99% (자동 Multi-AZ)
  • MTTR 평균 4~8시간                • MTTR 평균 30분~2시간
```

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 자가용(전용차)에서 카셰어링(필요할 때만 빌려 탄다)으로의 전환과 같다. 평소엔 경제용 소형차(IaaS: 빈 차), 가족여행엔 미니밴(PaaS: 차+기사), 비즈니스엔 택시(SaaS: 목적지만 말하면 OK), 급할 땐 전세버스(FaaS: 이벤트마다 즉석 배차)를 골라 탄다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 4계층 참조모델(Reference Architecture)로 분해된다. **① 인프라 계층(VPC/Subnet/Compute/Storage)**, **② 플랫폼 계층(Managed DB/Container Orchestration/Message Queue)**, **③ 애플리케이션 계층(Microservices/API Gateway/Service Mesh)**, **④ 운영 계층(IaC/CI-CD/Observability/FinOps)**. 각 계층은 API/SDK/CLI로 제어되며, IaC(Terraform/CloudFormation/ARM/Pulumi)로 선언적으로 기술된다.

```text
+-------------------------------------------------------------------------+
|           4-Tier Cloud-Native Reference Architecture (AWS 기준)        |
+-------------------------------------------------------------------------+
                          +----------------------+
                          |   End User / Client  |
                          |  (Web/Mobile/IoT)    |
                          +----------+-----------+
                                     | HTTPS / TLS 1.3 / QUIC
                                     v
+------------------------------------------------------------------------+
|  Edge & Delivery Layer                                                  |
|  +------------+  +------------+  +------------+  +----------------+   |
|  | CloudFront |  |   WAF +    |  |   Route53  |  |  Shield(DDoS)  |   |
|  |    (CDN)   |  | Shield Adv |  | (Anycast)  |  |   L3/L4/L7     |   |
|  +-----+------+  +-----+------+  +-----+------+  +--------+-------+   |
+--------+---------------+---------------+------------------+-----------+
         +---------------+---------------+------------------+
                                     v
+------------------------------------------------------------------------+
|  Application Layer (Microservices / Serverless)                        |
|  +-------------+  +-------------+  +-------------+  +-------------+   |
|  | API Gateway |  |   BFF/MFE   |  | GraphQL     |  | WebSocket   |   |
|  | (REST/gRPC) |  | (Module Fed)|  | Federation  |  | API Gateway |   |
|  +------+------+  +------+------+  +------+------+  +------+------+   |
|         +----------------+----------------+----------------+          |
|  +----------+ +----------+ +----------+ +----------+ +----------+      |
|  | Auth Svc | | Order Svc| |Payment Svc| | Catalog | | Notify   |      |
|  |  (EKS)   | |  (EKS)   | | (Lambda) | |  (EKS)  | | (SQS+λ)  |      |
|  +----+-----+ +----+-----+ +----+-----+ +----+-----+ +----+-----+      |
|       | Istio mTLS |            |             |            |             |
|       +------------+------------+-------------+------------+            |
+------------------------------------------------------------------------+
                                     v
+------------------------------------------------------------------------+
|  Platform Layer (Managed Services & Data)                               |
|  +----------+ +----------+ +----------+ +----------+ +----------+      |
|  | Amazon   | | ElastiC  | |   RDS    | |DynamoDB  | | Neptune  |      |
|  |  EKS/ECS | | ache     | |Aurora(PG)| |  (NoSQL) | | (Graph)  |      |
|  +----------+ +----------+ +----------+ +----------+ +----------+      |
|  +----------+ +----------+ +----------+ +----------+ +----------+      |
|  |   SQS    | |   SNS    | |   MSK    | |  Kinesis | | Step Func|      |
|  | (Queue)  | | (Pub/Sub)| | (Kafka)  | | (Stream) | | (Workflow)|     |
|  +----------+ +----------+ +----------+ +----------+ +----------+      |
+------------------------------------------------------------------------+
                                     v
+------------------------------------------------------------------------+
|  Infrastructure Layer (VPC / Region / AZ)                               |
|  +----------+ +----------+ +----------+ +----------+ +----------+      |
|  | EC2 /    | |   EBS    | |   S3     | |   EFS    | | FSx for  |      |
|  |  Fargate | |  (gp3)   | | (Object) | |  (NFS)   | | Lustre   |      |
|  +----------+ +----------+ +----------+ +----------+ +----------+      |
|  +--------------------------------------------------------------+      |
|  | VPC: Public/Private/Isolated Subnet, NAT GW, IGW, TGW, DX    |      |
|  | Region: us-east-1, ap-northeast-2 (Seoul)                    |      |
|  | AZ: 3개 AZ Multi-AZ 구성 (ap-northeast-2a/2b/2c)              |      |
|  +--------------------------------------------------------------+      |
+------------------------------------------------------------------------+
                                     v
+------------------------------------------------------------------------+
|  Operations Layer (Day-2: IaC + GitOps + Observability + FinOps)        |
|  +----------+ +----------+ +----------+ +----------+ +----------+      |
|  |Terraform | |  ArgoCD  | |  Prometheus| | Grafana  | |  CloudWatch|    |
|  | / CDK    | |  (GitOps)| |   + Loki  | | / Tempo  | | / X-Ray   |    |
|  +----------+ +----------+ +----------+ +----------+ +----------+      |
|  +----------+ +----------+ +----------+                                  |
|  |  AWS     | |  AWS     | |   OPA    |                                  |
|  |Config+SG | |  KMS     | | (Policy) |                                  |
|  +----------+ +----------+ +----------+                                  |
+------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 (Compute)** | 가상 CPU·메모리·GPU 자원 제공 | EC2(bare metal/metal/spot), Lambda(128MB~10GB, 15분 타임아웃), Fargate(컨테이너 서버리스), EKS(Managed K8s Control Plane), Auto Scaling Group + HPA/VPA/Cluster Autoscaler, Karpenter(지능형 노드 프로비저너, 30초 내 cold-start) |
| **스토리지 (Storage)** | 데이터 영속성·내구성 확보 | S3(11 9s 내구성, 99.99% 가용성, IA/Glacier Deep Archive 티어링), EBS(gp3 4,000 IOPS/125MB/s, io2 Block Express 256,000 IOPS), EFS(NFS v4, 병렬 처리), FSx(Lustre/ONTAP/Windows), 객체 잠금(Object Lock) + WORM |
| **네트워크 (Networking)** | VPC·라우팅·로드밸런싱·확장 | VPC(16비트 CIDR, /16=65,536 IP), Transit Gateway(다중 VPC 허브), PrivateLink(엔드포인트), ALB(L7 Path/Host 라우팅), NLB(L4 TCP 100만 TPS), GWLB(3rd-Party Appliance), Cloud WAN(글로벌 정책기반) |
| **데이터베이스 (Database)** | 트랜잭션·분석·캐시·검색 | Aurora(MySQL/PostgreSQL 호환, 6-way Replication, Serverless v2 0.5~128 ACU), DynamoDB(Global Tables Multi-Region Strong/Eventual Consistency), ElastiCache(Redis 7 Cluster Mode, Valkey 7.2), Neptune(Gremlin/SPARQL), DocumentDB(MongoDB 호환) |
| **보안·거버넌스 (Security)** | Zero Trust, 암호화, 컴플라이언스 | IAM(RBAC+ABAC), KMS-CMK/HSM(FIPS 140-2 L3), Secrets Manager(자동 Rotation), GuardDuty(ML 기반 위협탐지), Macie(PII 자동 분류), Security Hub(CIS/AWS Foundational Benchmark), CloudTrail+S3 Object Lock 감사 |
| **관측가능성 (Observability)** | Metrics·Logs·Traces | CloudWatch + Container Insights, Prometheus + Grafana + Loki + Tempo(PLG 스택), OpenTelemetry(OTel SDK, 30+ 언어), X-Ray/Datadog(분산 트레이싱, 100% 샘플링), eBPF 기반 Cilium Tetragon 런타임 보안 |
| **오케스트레이션 (Orchestration)** | 컨테이너 라이프사이클 관리 | EKS(Control Plane AWS 관리), K8s Core(CNI/CSI/CRI), Helm Chart(package), ArgoCD/Flux(GitOps, Git=Single Source of Truth), Istio(Envoy Sidecar mTLS, canary 5%->50%->100%) |
| **IaC·CICD (DevOps)** | 선언적 인프라·지속적 배포 | Terraform(상태파일 S3+DynamoDB Locking, OpenTofu 분기), Pulumi(코드로 IaC, TypeScript/Python), CodePipeline/Argo Workflows(파이프라인), CodeBuild(컨테이너 빌드), Crossplane(K8
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 574 / 800

<- **이전**: [573. 클라우드 아키텍처 핵심 토픽 573번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/573_cloud_architecture_core_topic_573_exam_summar/)
**다음**: [575. 클라우드 아키텍처 핵심 토픽 575번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/575_cloud_architecture_core_topic_575_exam_summar/) ->

---
