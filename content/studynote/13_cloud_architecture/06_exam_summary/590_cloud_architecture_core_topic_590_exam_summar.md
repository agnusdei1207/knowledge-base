---
title: "Cloud Architecture Core Topic 590 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

# 590. 클라우드 아키텍처 핵심 토픽 시험 요약

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS 계층 위에 Well-Architected Framework(WAF)의 5대 원칙(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화)을 적용하여, Control Plane과 Data Plane의 분리를 통해 탄력성(Elasticity), 확장성(Scalability), 가용성(Availability)을 SLA 99.99% 이상으로 보장하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: CAP(Consistency, Availability, Partition Tolerance) 트레이드오프 하에서 Auto Scaling 그룹을 통한 수평 확장 시 처리량 10~100배 향상, Region/AZ 다중화로 RTO 4시간->5분·RPO 0분 달성, Pay-as-you-go 모델로 CapEx 대비 OpEx 30~60% 절감, 다중 클라우드(Multi-Cloud) 전략으로 벤더 종속(Lock-in) 리스크 완화 및 BCP 등급 1등급 확보가 가능하다.
> 3. **판단 포인트**: 단일 Region vs Multi-Region 배치 결정 시 RTO/RPO 요구사항과 데이터 주권(데이터 레지던시) 규제 준수 여부 검토, 동기식 복제(Synchronous) vs 비동기식 복제(Asynchronous) 선택에 따른 latency 비용 분석, Stateless 워크로드에 Stateless한 컨테이너 오케스트레이션(Kubernetes/ECS) 적용, Stateful 워크로드는 Managed Service(RDS, ElastiCache, DynamoDB)로 위임하여 운영 부담 최소화 및 책임 공용 모델(Shared Responsibility Model) 경계 명확화 여부가 핵심 의사결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스(On-Premises) 3-Tier 아키텍처는 Monolithic Application, Vertical Scaling(Scale-Up) 방식의 Bare-Metal/Hypervisor, 그리고 정적 Capacity Planning에 의존하여 Peak 부하를 기준으로 하드웨어를 사전에 확보해야 했다. 이로 인해 평균 활용률은 15~25%에 불과하고, 신규 인프라 도입에 8~12주의 Lead Time과 천문학적 CapEx가 발생했으며, DR(Disaster Recovery) 사이트의 이중 투자로 ROI가 급격히 저하되는 문제가 상존했다. 2006년 AWS S3와 EC2의 출시 이후, Utility Computing 모델이 산업 표준으로 자리 잡으면서, NIST SP 800-145에 명시된 5대 특성(On-Demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)을 충족하는 Cloud Computing 패러다임이 보편화되었다.

클라우드 아키텍처는 단순한 인프라 이전(Lift & Shift)을 넘어, **Cloud-Native** 패러다임 — 즉 12-Factor App 원칙, Micro Services, Container/Orchestration, DevOps/GitOps, Immutable Infrastructure — 을 통해 시스템의 본질적 속성(탄력성, 회복탄력성, 관측가능성)을 코드(Code)로 정의하는 **Infrastructure as Code(IaC)** 사상으로 진화했다. 기술사 관점에서 클라우드 아키텍처를 평가할 때는 단순한 "클라우드 사용 여부"가 아니라, **Workload 특성에 맞는 클라우드 서비스 모델(IaaS/PaaS/SaaS/FaaS)의 합리적 선택**, **Multi-Cloud/Hybrid-Cloud의 거버넌스 모델**, **CSP(Cloud Service Provider) SLA 및 책임 공용 모델의 경계**가 핵심 평가 요소이다.

```text
+---------------------------------------------------------------------+
|                클라우드 컴퓨팅 패러다임 진화 (Evolution)              |
+---------------------------------------------------------------------+
|                                                                     |
|  [1960s Mainframe]    [1990s Client-Server]    [2000s Web 2.0]       |
|   Time-Sharing    ->    Tier 1-2-3 분리    ->   LAMP/Stack            |
|   중앙집중형           수직확장 중심          수평확장 도입            |
|        |                    |                     |                 |
|        v                    v                     v                 |
|  +----------------------------------------------------------+      |
|  |              [2010s Cloud-Native Era]                      |      |
|  |  AWS(2006) -> GCP(2008) -> Azure(2010) -> Cloud Native (2015)|      |
|  |                                                           |      |
|  |  +-------------+  +-------------+  +-------------+       |      |
|  |  |   IaaS      |  |   PaaS      |  |   SaaS      |       |      |
|  |  |  EC2/RDS    |  | Elastic Bean|  |  Office 365 |       |      |
|  |  |  (제어^)    |  |  Heroku     |  |  Salesforce  |       |      |
|  |  |  (책임^)    |  |  (균형)     |  |  (제어v)     |       |      |
|  |  +-------------+  +-------------+  +-------------+       |      |
|  |              ^            |            ^                  |      |
|  |              +---- FaaS(Serverless) ---+                  |      |
|  |              Lambda / Cloud Functions                      |      |
|  +----------------------------------------------------------+      |
|                              |                                     |
|                              v                                     |
|  +----------------------------------------------------------+      |
|  |           [2020s Distributed Cloud / Edge Era]             |      |
|  |  Multi-Cloud |  Hybrid-Cloud |  Edge Computing |  Wasm    |      |
|  |  Anthos | Azure Arc | AWS Outposts | Cloudflare Workers   |      |
|  +----------------------------------------------------------+      |
+---------------------------------------------------------------------+
```

**기존 On-Premise 대비 클라우드의 구조적 차이**

| 차원 | On-Premise | Cloud-Native | 비고 |
|:---|:---|:---|:---|
| **확장 모델** | Scale-Up (수직) | Scale-Out (수평) | CPU 1,024코어 -> 인스턴스 1,000대 분산 |
| **Capacity Plan** | Peak 기준 과다 설계 | Auto Scaling (실시간) | TCO 40~70% 절감 (Forrester Report) |
| **배포 주기** | 월 1~4회 (수동) | 일 10~100회 (CI/CD) | Lead Time: 수일 -> 수 분 |
| **DR 전략** | Cold/Hot Standby 별도 구축 | Cross-Region Active-Active | RPO 0, RTO 분 단위 |
| **장애 대응** | MTTR 수 시간 | Self-Healing (K8s) | 자동 재시작·재스케줄링 |
| **보안 모델** | 경계 중심 (Perimeter) | Zero-Trust + ID-Centric | IAM, mTLS, Service Mesh |

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 호텔의 객실 운영과 같다. 손님이 5명일 때 5개 객실만 청소하고, 50명이 몰리면 즉시 추가 객실을 개방하며, 손님이 떠나면 객실을 회수한다. 모든 객실은 표준화(Immutability)되어 있어 다음 손님에게 항상 같은 품질을 보장하고, 호텔 본부는 손님의 실제 사용량(미터기)에 따라 요금을 받는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **Control Plane(제어 평면)** 과 **Data Plane(데이터 평면)** 의 분리에 있다. Control Plane은 API 호출을 통해 리소스 프로비저닝, 설정 변경, 모니터링 명령을 내리고(예: AWS API Gateway, Kubernetes API Server), Data Plane은 실제 트래픽을 처리하며(예: EC2 인스턴스 내부의 Application Load Balancer, kubelet) 두 평면은 독립적으로 확장 및 장애 격리된다. 또 다른 핵심 원리는 **가용 영역(Availability Zone, AZ)** 과 **리전(Region)** 의 계층적 구조이며, 한 리전은 통상 2~4개의 AZ로 구성되고, 각 AZ는 독립된 전력·냉각·네트워크를 가진 하나 이상의 데이터센터로 이루어져 있다. 이를 통해 "단일 장애점(SPOF) 제거"와 "동시 장애(Concurrent Failure) 허용"이라는 분산 시스템의 두 마리 토끼를 모두 잡는다.

```text
+------------------------------------------------------------------------+
|         Multi-Region / Multi-AZ Reference Architecture (AWS 기준)      |
+------------------------------------------------------------------------+
|                                                                        |
|  [User] --► [CloudFront (CDN/Edge)] --► [Route 53 (DNS Latency-Based)]  |
|                                              |                         |
|                          +-------------------+--------------------+    |
|                          |                                        |    |
|              +-----------v----------+               +-------------v--+ |
|              |   Region: Seoul (ap-northeast-2)        | Region: Tokyo | |
|              |                                          | (ap-northeast-1)|
|              |  +------+   +------+   +------+         |                |
|              |  | AZ-a |   | AZ-b |   | AZ-c |         |                |
|              |  +--+---+   +--+---+   +--+---+         |                |
|              |     |          |          |              |                |
|              |     v          v          v              |                |
|              |  +---------------------------------+     |                |
|              |  |  ALB (Application Load Balancer)|     |                |
|              |  +----+-------------------+--------+     |                |
|              |       |                   |              |                |
|              |   +---v----+         +----v---+         |                |
|              |   |ECS/EKS |         |ECS/EKS |         |                |
|              |   |Fargate |         |Fargate |         |                |
|              |   +---+----+         +----+---+         |                |
|              |       |  (Cross-AZ Traffic) |              |                |
|              |       +----------+---------+              |                |
|              |                  v                        |                |
|              |   +--------------------------+           |                |
|              |   | Amazon Aurora (Multi-AZ) |◄--Global--|--Database--+   |
|              |   |  Writer  ◄--► Reader    |  Replica   |             |   |
|              |   +----------+---------------+           |             |   |
|              |              |  Async Replication        |             |   |
|              +--------------+---------------------------+             |   |
|                             v                                         |   |
|                  +----------------------+   +----------------------+   |   |
|                  |  S3 (Object Storage) |   | DynamoDB Global Table|   |   |
|                  |  Cross-Region Repl.  |   |  Multi-Region Active |   |   |
|                  +----------------------+   +----------------------+   |   |
|                                                                        |   |
|  Observability Layer: CloudWatch | X-Ray | CloudTrail | Prometheus     |   |
|  Security Layer: IAM | WAF | Shield | KMS | Secrets Manager | GuardDuty |   |
+------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Region / AZ / Edge Location** | 지리적 격리 단위 | Region은 국가 단위 데이터 주권 적용(예: KR CSAP), AZ간 latency 1~2ms, Edge Location은 400+ PoP로 캐싱(CloudFront) |
| **Control Plane (API Layer)** | 리소스 라이프사이클 관리 | 비동기 Eventually-Consistent, Rate Limit(예: EC2 100 req/s), IAM 인증·인가, API Throttling으로 DoS 방어 |
| **Data Plane (Traffic Path)** | 실제 사용자 요청 처리 | 동기 Strong/Eventual Consistency 선택, Multi-AZ 트래픽 분산, Anycast IP로 BGP 기반 라우팅 |
| **Compute Layer (IaaS/FaaS)** | 워크로드 실행 환경 | IaaS: EC2/Bare-Metal (M5/M6i, Graviton3 ARM64), FaaS: Lambda(128MB~10GB, 15분 timeout, Concurrent 1,000), 컨테이너: ECS/EKS/GKE/AKS |
| **Storage Layer** | 데이터 영속성·내구성 | Block: EBS(gp3 3,000 IOPS, io2 Block Express 256,000 IOPS), Object: S3(11 9s 내구성, Lifecycle Policy), File: EFS/FSx, Key-Value: DynamoDB(Single-digit ms) |
| **Network Layer** | L4/L7 라우팅·격리 | VPC/Subnet CIDR 설계(10.0.0.0/16, /20 권장), PrivateLink로 SaaS Private 연결, Transit Gateway로 Hub-Spoke, TGW peering으로 5,000 VPC 연결 |
| **Identity & Access (IAM)** | Zero-Trust 인증·인가 | RBAC + ABAC(Attribute-Based), IAM Role로 임시 자격증명(STS), SCP(Service Control Policy)로 Org-wide Guardrail, MFA + SSO 통합 |
| **Observability Stack** | SLI/SLO 기반 운영 | Metrics(Prometheus/CloudWatch), Logs(Loki/CloudWatch Logs), Traces(OpenTelemetry/Jaeger/X-Ray), 3 Signal(RED: Rate/Error/Duration) + 4 Golden Signals |
| **Orchestrator (Kubernetes)** | 컨테이너 라이프사이클 자동화 | Control Plane: kube-apiserver, etcd(Raft 합의), scheduler, controller-manager; Node: kubelet, kube-proxy, CNI(Container Network Interface) |
| **IaC Pipeline** | 선언적 인프라 정의 | Terraform(HCL 멀티 클라우드), Pulumi(General-purpose Language), AWS CDK, Ansible(Procedural), ArgoCD/Flux(GitOps Controller) |

**가용성 계산식 (Composite SLA)**

```
가용성(Availability, A) = MTBF / (MTBF + MTTR)
서비스 가용성 = 1 - (1 - A_Component1) × (1 - A_Component2) × ... × (1 - A_ComponentN)
연간 장애 허용 시간(Downtime) = (1 - A) × 365 × 24 × 60 [분]

예시: 99.9% × 99.9% × 99.9% = 99.7% (단일 AZ 3-Tier)
      99.99% × 99.99% × 99.99% = 99.97% (Multi-AZ + Auto Healing)
```

**Well-Architected Framework 5 Pillars (AWS 기준)**
- **운영 우수성 (Operational Excellence)**: Code로 운영(Everything as Code), 점진적 변경, 모니터링 기반 의사결정
- **보안 (Security)**: Strong Identity Foundation, 계층별 Defense-in-Depth, 데이터 보호(At-Rest/In-Transit/In-Use), 추적 가능성(Auditability)
- **안정성 (Reliability)**: 자동 복구(Self-Healing), 수평 확장(Horizontal Scaling), Capacity Quota 관리, 변경 관리 자동화
- **성능 효율성 (Performance Efficiency)**: 컴퓨트·스토리지·데이터베이스·네트워크의 Demystification, 모놀리식 -> 마이크로서비스 분해, 캐싱 전략(Multi-Tier Cache: Browser -> CDN -> API Gateway -> Application -> DB)
- **비용 최적화 (Cost Optimization)**: Pay-as-you-go, TCO 모델링,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 590 / 800

<- **이전**: [589. 클라우드 아키텍처 핵심 토픽 589번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/589_cloud_architecture_core_topic_589_exam_summar/)
**다음**: [591. 클라우드 아키텍처 핵심 토픽 591번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/591_cloud_architecture_core_topic_591_exam_summar/) ->

---
