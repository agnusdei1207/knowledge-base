---
title: "Cloud Architecture Core Topic 789 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 CAP定理와 PACELC 트레이드오프 하에서 **탄력성(Elasticity)**, **불변 인프라(Immutable Infrastructure)**, **API 기반 프로비저닝**을 핵심 추상화로 사용하며, AWS Well-Architected Framework의 6개 기둥(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화, 지속가능성) 및 CNCF의 Cloud Native Definition v1.0(컨테이너 오케스트레이션, 서비스 메시, 마이크로서비스, 불변 인프라, 선언적 API)을 통해 평가되는 시스템 설계 패러다임이다.
> 2. **가치**: 적정 규모 설계(Right-Sizing)와 Auto Scaling을 결합 시 **컴퓨팅 비용 30~70% 절감**, Multi-AZ + Multi-Region 구성으로 **RTO < 1분, RPO = 0** 달성, IaC(Infrastructure as Code) 적용 시 **환경 구성 시간 90% 단축**(수동 대비 4시간 -> 15분), Kubernetes 기반 배포로 **롤백 시간 MTTR 85% 감소** 등의 정량적 효과를 제공한다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs 멀티 클라우드(상호 운용성 비용), Stateless Microservices vs Stateful Service Mesh, EKS vs 자체 Kubernetes(Managed Control Plane의 50% 운영비 절감 vs BYO CNI 유연성), FinOps의 Reserved Instance(40% 할인) vs Savings Plans(유연성) vs Spot Instance(최대 90% 할인, 중단 허용 SLA) 간의 트레이드오프, 그리고 12-Factor App 준수와 Cell-Based Architecture(Netflix OSS) 선택 기준이 핵심 결정 포인트다.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 IT 시스템은 2006년 AWS S3/EC2 출시 이후 자본 지출(CapEx)에서 운영 지출(OpEx)로의 전환, 그리고 비즈니스 요구사항의 10배 빠른 변화 속도 대응이라는 두 가지 거대한 압력에 직면해 있다. 기존 모놀리식 아키텍처(예: WAS 1대 + Oracle RAC + SAN 스토리지)는 **수직 확장의 물리적 한계**(CPU/메모리 추가 시 6~9개월 리드타임), **수동 프로비저닝**(랙 스페이스, 케이블링, OS 설치로 평균 6주), **단일 장애점(SPOF)**으로 인한 가용성 99.9%(연간 8.76시간 장애) 한계, 그리고 **Tight Coupling**으로 인한 배포 주기 6개월이라는 문제를 안고 있었다.

클라우드 아키텍처는 이를 해결하기 위해 **가상화(KVM/Xen/Hyper-V)** -> **컨테이너화(Docker, 2013)** -> **오케스트레이션(Kubernetes, 2014)** -> **Serverless(Lambda, 2014)** -> **서비스 메시(Istio, 2017)**로 진화했으며, NIST SP 500-292 표준 참조 모델에 따라 **On-Premises(Private) / Public / Hybrid / Community** 4가지 배포 모델과 **IaaS / PaaS / SaaS / FaaS / DaaS** 5가지 서비스 모델을 체계화했다.

```text
+---------------------------------------------------------------------+
|         전통 아키텍처 vs 클라우드 네이티브 아키텍처 진화도           |
+---------------------------------------------------------------------+
|                                                                     |
|  [1세대: Mainframe]    [2세대: Client-Server]   [3세대: SOA/ESB]   |
|   물리적 컴퓨팅          수직 스케일링              메시지 버스       |
|   +----------+          +------+                  +------+         |
|   |  Main    |          | App  |                  | ESB  |         |
|   |  Frame   |◄--------►| Tier |◄----------------►|Router|         |
|   +----------+          +------+                  +------+         |
|   1960s~1980s           1990s                    2000s               |
|         |                    |                       |               |
|         +--------+-----------+-----------+-----------+               |
|                  v                       v                           |
|         [4세대: 가상화/Cloud]      [5세대: Cloud Native]              |
|          수평 스케일링             컨테이너+오케스트레이션            |
|          +----------+            +------------------+               |
|          | Hyper-V  |            | K8s Control Plane |               |
|          | VM Pool  |            |  +- etcd          |               |
|          |  +-VM    |            |  +- API Server    |               |
|          |  +-VM    |            |  +- Scheduler     |               |
|          |  +-VM    |            | Worker Nodes      |               |
|          +----------+            |  +- Pod(컨테이너) |               |
|          2006~2013               |  +- Sidecar(Envoy)|               |
|                                  |  +- Operator      |               |
|                                  +------------------+               |
|                                  2014~현재                           |
+---------------------------------------------------------------------+
```

클라우드 아키텍처의 필요성은 IDC 보고서 기준 **2025년 전 세계 엔터프라이즈 워크로드의 85%가 클라우드 우선(Cloud-First)** 전략을 채택한다는 점, 그리고 Gartner의 Hype Cycle에서 **Platform Engineering(2024년 Mainstream)**, **Cloud Sustainability(필수 요구사항)**, **FinOps(경영진 KPI)**로 이동한 트렌드에서 명확히 드러난다. 한국은 **클라우드 컴퓨팅 발전 및 이용자 보호에 관한 법률(2021.9. 시행, 2024.1. 전면 개정)**에 따라 SaaS 사업자의 안정성·이중화 인증이 의무화되었으며, 공공부문의 **클라우드 보안 인증(CSAP)** 등급제가 가속화되고 있다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "택시 호출(Ola/Uber) vs 자가용 보유"의 차이다. 자가용은 초기 비용이 낮지만 고장나면 직접 정비해야 하고 유휴 시간이 95%이며, 택시는 클릭 한 번으로 비즈니스 상황에 맞춰 차량 등급(컴퓨팅)·탑승 인원(메모리)·짐칸(스토리지)을 즉시 변경할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **5계층 참조 모델(IaaS -> CaaS -> PaaS -> FaaS -> SaaS)** 위에서 동작하며, 각 계층은 **API 계약(Contract)**, **멀티 테넌시(Multi-Tenancy)**, **격리(Isolation)**, **탄력성(Elasticity)**, **관측 가능성(Observability)**의 5대 공통 원리를 따른다. AWS는 이를 200개+ 서비스로, Azure는 200개+, GCP는 100개+ 서비스로 구현하며, 모두 **리전(Region) -> 가용 영역(Availability Zone) -> 엣지 로케이션(Point of Presence)**의 3단계 지리적 계층 구조를 가진다.

```text
+----------------------------------------------------------------------+
|         클라우드 아키텍처 5계층 + Cross-Cutting Concerns             |
+----------------------------------------------------------------------+
|                                                                      |
|  +--------------------------------------------------------------+   |
|  | [5] SaaS (Software as a Service)                              |   |
|  |   예: Salesforce, M365, Slack, GitHub.com                    |   |
|  |   제어: 사용자 | 추상화: 완전托管 | 예: SFDC, Workday         |   |
|  +--------------------------------------------------------------+   |
|  | [4] FaaS (Function as a Service) - Serverless                 |   |
|  |   예: AWS Lambda, Azure Functions, GCP Cloud Functions      |   |
|  |   제어: 코드만 | Cold Start 100~800ms, Event-Driven          |   |
|  |   +--------+  +--------+  +--------+                         |   |
|  |   |Lambda  |  |Lambda  |  |Lambda  |  <- 동시 1000개 실행    |   |
|  |   +----+---+  +----+---+  +----+---+                         |   |
|  |        |            |            |                              |   |
|  |   [S3/EventBridge] [DynamoDB Stream] [SQS Queue]            |   |
|  +--------------------------------------------------------------+   |
|  | [3] PaaS (Platform as a Service)                              |   |
|  |   예: EKS, AKS, GKE, RDS, Elastic Beanstalk, App Service    |   |
|  |   제어: 앱/데이터 | 추상화: 런타임+미들웨어托管              |   |
|  |   +----------------------------------------------+           |   |
|  |   |  Managed Kubernetes (EKS/AKS/GKE)            |           |   |
|  |   |  +- Control Plane (API Server, etcd)托管     |           |   |
|  |   |  +- Worker Node (사용자 관리 or Fargate)     |           |   |
|  |   |  +- Add-on (CNI, CSI, Service Mesh)          |           |   |
|  |   +----------------------------------------------+           |   |
|  +--------------------------------------------------------------+   |
|  | [2] CaaS (Container as a Service)                             |   |
|  |   예: ECS, AKS, Cloud Run, Fargate                           |   |
|  |   제어: 컨테이너 이미지 | 추상화: 호스트 OS托管              |   |
|  +--------------------------------------------------------------+   |
|  | [1] IaaS (Infrastructure as a Service)                        |   |
|  |   예: EC2, Azure VM, Compute Engine, S3, EBS                 |   |
|  |   제어: OS/미들웨어 | 추상화: 물리 하드웨어托管              |   |
|  |   +---------+  +---------+  +---------+  +---------+         |   |
|  |   | EC2 m5. |  | EC2 c5. |  | EC2 r5. |  | EC2 x1. |         |   |
|  |   | 4xlarge |  | 9xlarge |  | 16xlarge|  | 32xlarge|         |   |
|  |   +---------+  +---------+  +---------+  +---------+         |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
|  +--- Cross-Cutting Concerns (모든 계층 공통) ---+                   |
|  |                                              |                   |
|  |  [보안]        [관측]         [거버넌스]      |                   |
|  |   +-IAM/RBAC   +-Prometheus   +-IaC(Terraform)|                   |
|  |   +-KMS/HSM    +-Grafana      +-Policy as Code|                   |
|  |   +-WAF/GuardD +-Loki/ELK     +-FinOps        |                   |
|  |   +-Zero Trust +-Jaeger/Tempo +-DR/BCP        |                   |
|  +----------------------------------------------+                   |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 계층** | 워크로드 실행 환경 제공 | **EC2**(가상머신, Nitro System 하드웨어 가상화), **Lambda**(컨테이너 기반 Firecracker microVM, 128MB~10,240MB 메모리, 15분 타임아웃), **EKS Fargate**(서버리스 K8s 노드, vCPU 0.25~96, 메모리 0.5GB~192GB), **Bare Metal**(물리 서버 전용, BYOL 라이선스) |
| **스토리지 계층** | 데이터 영속성 및 IOPS 보장 | **S3 Standard**(11 9s 내구성, 99.99% 가용성, 3-way replication), **EBS gp3**(3,000~16,000 IOPS, 125~1,000 MB/s), **EFS**(NFS v4, 10GB/s+ 집계 처리량), **FSx for Lustre**(100GB/s+ HPC용), **S3 Glacier Instant Retrieval**(밀리초 단위, $0.01/GB/월) |
| **네트워크 계층** | 지연 시간 최적화 및 격리 | **VPC/16**(65,536 IP), **Transit Gateway**(VPC 피어링 매스, 최대 5,000 VPC 연결), **CloudFront**(216+ 엣지 로케이션, HTTP/3 QUIC), **PrivateLink**(퍼블릭 인터넷 우회, 0.05ms 추가 지연), **Global Accelerator**(Anycast IP, BGP 라우팅 최적화) |
| **데이터 계층** | RDBMS/NoSQL/NewSQL 구분 처리 | **RDS Aurora**(MySQL/PostgreSQL 호환, 6-way replication, 128TB 자동 확장), **DynamoDB**(단일 키-값, p99 < 10ms, Global Tables 멀티리전 활성-활성), **Neptune**(그래프 DB, Gremlin/SPARQL), **Redshift**(MPP, 16 PB 페타바이트급 DW) |
| **오케스트레이션 계층** | 컨테이너 라이프사이클 및 선언적 상태 관리 | **Kubernetes Control Plane**(etcd Raft 합의 알고리즘, API Server Stateless, Scheduler Bin-packing), **Operator Pattern**(CRD + Controller, e.g., AWS Controllers for Kubernetes(ACK)), **GitOps**(ArgoCD/Flux, Git 저장소가 Single Source of Truth) |
| **관측 가능성 계층** | SLI/SLO 기반 신뢰성 측정 | **3 Pillars**: Metrics(Prometheus, M3, VictoriaMetrics), Logs(Loki, ELK, CloudWatch), Traces(Jaeger, Zipkin, AWS X-Ray), **USE Method**(Utilization, Saturation, Errors), **RED Method**(Rate, Errors, Duration) |
| **보안 계층** | Zero Trust 및 최소 권한 원칙 | **IAM 정책 JSON**(Action/Resource/Condition), **KMS CMK**(Envelope Encryption, AES-256), **Secrets Manager**(자동 로테이션, $0.40/secret/월), **Cognito**(OAuth 2.0/OIDC/SAML 2.0), **WAF**(OWASP Top 10 룰셋, Rate Limiting 10,000 req/s) |
| **거버넌스 계층** | IaC, 정책 코드화, 비용 최적화 | **Terraform**(HCL 선언형, State 잠금 DynamoDB), **Pulumi**(TypeScript/Python 임퍼러티브), **AWS Config**(규정 준수 평가, 240+ 관리 규칙), **Control Tower**(Landing Zone, SCP(Service Control Policy) 계층) |

핵심 알고리즘 및 결정 공식은 다음과 같다:

**1) CAP 정리와 PACELC**: 분산 시스템은 **C(Consistency)/A(Availability)/P(Partition Tolerance)** 중 2개만 보장 가능. PACELC는 평상시(ELSE)에도 **Latency vs Consistency** 트레이드오프가 있음을 명시. 예: DynamoDB는 **AP**(Eventually Consistent, p99 < 10ms), Google Spanner는 **CP**(TrueTime API, Strongly Consistent, 글로벌 트랜잭션), Cassandra는 **Tunable**(N/R/W 설정으로 일관성 수준 조절).

**2) Consistent Hashing**: 캐시 노드 추가/삭제 시 **O(log N)** 키 재배치, 가상 노드(Virtual Node) 200~500개로 키 분포 균등화. **DynamoDB Partition**은 10GB/3,000 RCU/1,000 WCU 단위로 자동 샤딩.

**3) Auto Scaling 공식**:
```
Desired Capacity = max(
  ceil(CurrentCapacity × (AvgCPU / TargetCPU)),  // CPU 기반
  ceil(CurrentRPS × TargetLatencyP99 / CurrentLatencyP99),  // 커스텀

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 789 / 800

<- **이전**: [788. 클라우드 아키텍처 핵심 토픽 788번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/788_cloud_architecture_core_topic_788_exam_summar/)
**다음**: [790. 클라우드 아키텍처 핵심 토픽 790번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/790_cloud_architecture_core_topic_790_exam_summar/) ->

---
