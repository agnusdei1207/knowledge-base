---
title: "714. 클라우드 아키텍처 핵심 토픽 714번 시험 요약 (Cloud Architecture Core Topic 714 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 탄력성(Elasticity), 온디맨드 셀프서비스(On-Demand Self-Service), 측정 가능한 서비스(Measured Service)의 NIST 5대 필수 특성을 충족하면서, AWS Well-Architected Framework의 6대 필러(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화, 지속가능성) 위에서 워크로드를 설계하는 통합 엔지니어링 discipline이다.
> 2. **가치**: Capital Expenditure(CapEx)를 Operational Expenditure(OpEx)로 전환하여 약 30~40%의 인프라 비용 절감을 달성하고, Auto Scaling Group을 통해 트래픽 변동에 대응하여 가용성 99.99%(Four Nines) 이상을 SLA로 보장하며, Global Edge Network(CloudFront, Azure CDN)를 통해 P99 레이턴시를 100ms 이하로 유지 가능하다.
> 3. **판단 포인트**: Lift-and-Shift(IaaS) vs Cloud-Native Refactoring(PaaS/Serverless) 사이의 TCO 5년 분석, 단일 리전 단일 AZ 구성의 단일 장애점(SPOF) 제거 여부, 그리고 Egress Data Transfer 비용이 전체 TCO의 20%를 초과하는지 여부로 Multi-Cloud 전략의 정당성을 판단한다.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스(On-Premise) 환경은 3-tier 모놀리식 아키텍처(Web-Tier, App-Tier, DB-Tier)에서 수직적 확장(Scale-Up) 방식으로 트래픽 피크에 대비해 평균 60~70%의 유휴 자원을 상시 보유해야 했다. 이는 `소프트웨어 라이선스 + 하드웨어 + 운영 인건비 + 데이터센터 전력·냉각비`의 4중 비용 구조로 이어졌으며, 비즈니스 출시 시간(Mean Time to Market, MTM)이 평균 6개월 이상 소요되는 병목 현상을 야기했다.

2006년 AWS S3와 EC2 출시 이후, 클라우드 아키텍처는 인프라 추상화(Infrastructure Abstraction)를 통해 컴퓨팅·스토리지·네트워크를 API로 호출 가능한 프로그래머블 자원(Programmable Resource)으로 전환했다. 이를 통해 `Infrastructure as Code(IaC) - Terraform, AWS CloudFormation, Pulumi` 기반으로 선언적(Declarative) 인프라 정의가 가능해졌으며, GitOps(ArgoCD, Flux)와 CI/CD 파이프라인의 결합으로 배포 주기를 6개월 -> 1일 단위로 단축하는 DevOps-to-NoOps 전환이 가능해졌다.

```text
+------------------------------------------------------------------+
|        On-Premise vs Cloud Architecture Paradigm Shift          |
+------------------------------------------------------------------+
|                                                                  |
|   [On-Premise 3-Tier Monolith]     [Cloud-Native Distributed]    |
|                                                                  |
|   +---------------------+         +---------------------+       |
|   |  Web Server (Nginx) |         |   CDN/Edge (CF)     |       |
|   |  1 ~ N instances    |         |  Static + Dynamic   |       |
|   +----------+----------+         +----------+----------+       |
|              |                              |                   |
|   +----------v----------+         +----------v----------+       |
|   |  App Server (WAS)   |         |   ALB / API Gateway |       |
|   |  1 ~ N instances    |         |   + WAF + Shield    |       |
|   |  (Vertical Scale)  |         +----------+----------+       |
|   +----------+----------+                    |                   |
|              |                +--------------+--------------+    |
|   +----------v----------+     |              |              |    |
|   |  Oracle/MySQL HA    |     v              v              v    |
|   |  (Active/Standby)   |  +-----+      +-----+      +-----+    |
|   +---------------------+  | EKS |      | EKS |      | EKS |    |
|                            | Pod |      | Pod |      | Pod |    |
|   Lead Time: 6 Months      +--+--+      +--+--+      +--+--+     |
|   CapEx: 100% 선투자          |            |            |        |
|   Utilization: 30~40%     +---v------------v------------v--+     |
|                          |  Aurora Global + DynamoDB        |    |
|                          |  (Multi-Region, Multi-Master)    |    |
|                          +----------------------------------+    |
|                                                                  |
|                          Lead Time: 1 Day                       |
|                          OpEx: Pay-per-Use                      |
|                          Utilization: 70~85% (Auto-Scaling)     |
+------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 온프레미스는 "물리적 정수기"를 사무실에 직접 들여놓는 것이고, 클라우드는 "정수기 앱을 호출해서 필요한 만큼 물을 받는" 것과 같다. 전자는 공간·전력·관리가 직접 필요하지만, 후자는 사용량만큼만 요금을 내고 유지보수는 공급자가 맡는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **가상화(Hypervisor Type 1: KVM, Xen / Type 2: VMware Workstation) -> 컨테이너화(Docker, containerd, CRI-O) -> 오케스트레이션(Kubernetes, ECS, EKS, AKS, GKE)** 의 3단계 추상화 스택 위에 위치한다. 각 계층은 API Contract를 통해 상위 계층에 자원을 노출하며, 이는 곧 `Compute -> Network -> Storage -> Identity` 4대 자원 도메인의 분리와 재결합을 의미한다.

```text
+--------------------------------------------------------------------+
|         Cloud Architecture 4-Layer Stack (Bottom-Up)              |
+--------------------------------------------------------------------+
|                                                                    |
|  +--------------------------------------------------------------+  |
|  | Layer 4: Application & Workload (SaaS / FaaS / Microsvc)   |  |
|  |  - Lambda / Cloud Functions / Azure Functions                |  |
|  |  - Spring Boot, Node.js, Go Services                        |  |
|  |  - EventBridge, SQS/SNS, Pub/Sub, Kafka (MSK/Confluent)     |  |
|  +--------------------------------------------------------------+  |
|                              ^                                     |
|  +--------------------------------------------------------------+  |
|  | Layer 3: Platform & Orchestration (PaaS / CaaS)              |  |
|  |  - Kubernetes Control Plane (API Server, etcd, Scheduler)    |  |
|  |  - Helm Chart, Kustomize, ArgoCD                            |  |
|  |  - Service Mesh: Istio, Linkerd (mTLS, Traffic Mgmt)         |  |
|  +--------------------------------------------------------------+  |
|                              ^                                     |
|  +--------------------------------------------------------------+  |
|  | Layer 2: Infrastructure as a Service (IaaS)                  |  |
|  |  - EC2, Compute Engine, Azure VM (M5/C5/D3/G4 family)       |  |
|  |  - EBS/PD/Managed Disks, S3/GCS/Blob, EFS/FSx               |  |
|  |  - VPC/VNet (Subnet, Route Table, NAT/IGW, SG/NACL)         |  |
|  +--------------------------------------------------------------+  |
|                              ^                                     |
|  +--------------------------------------------------------------+  |
|  | Layer 1: Physical & Virtualization Foundation                |  |
|  |  - Nitro System (AWS), Hyper-V, Nitro Enclaves               |  |
|  |  - Nitro Card: VPC, EBS, Instance Storage Offload            |  |
|  |  - Bare Metal: i3.metal, m5.metal, Oracle BM.Standard      |  |
|  +--------------------------------------------------------------+  |
|                                                                    |
|  Cross-Cutting Concerns:                                           |
|  [IAM/OIDC] [KMS/HSM] [CloudWatch/Stackdriver/Monitor]            |
|  [CloudTrail/Audit Log] [VPC Flow Log] [AWS Config]               |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 계층 (Compute)** | 워크로드 실행 | 인스턴스 타입(범용 M, 컴퓨트 최적화 C, 메모리 최적화 R, GPU P/G, 스토리지 최적화 D/I, 가속 컴퓨팅 F/Trn), Auto Scaling Group(Desired/Min/Max), Spot Fleet(미사용 용량 70% 할인) |
| **스토리지 계층 (Storage)** | 데이터 영속화 | Object(S3/GCS/Blob, 11 9s 내구성, Lifecycle Policy -> IA/Glacier), Block(EBS gp3/io2, NVMe SSD, 16K IOPS ~ 256K IOPS), File(EFS, FSx for Lustre/ONTAP, NFS/SMB 프로토콜) |
| **네트워크 계층 (Network)** | 트래픽 라우팅 | VPC Peering, Transit Gateway(50+ VPC 허브), PrivateLink(서비스별 사설 연결), Cloud WAN(Segmentation), DX/VPN(전용선), VPC Endpoint(Gateway/Interface) |
| **오케스트레이션 (Orchestration)** | 컨테이너 라이프사이클 | Kubernetes Control Plane: kube-apiserver(YAML 파싱) -> etcd(클러스터 상태) -> scheduler(PDB 고려) -> kubelet(CRI 호출) -> kube-proxy(CNI). HPA(CPU/Mem)·VPA·Cluster Autoscaler 3단계 스케일링 |
| **관리·거버넌스 (Governance)** | 정책/비용/감사 | AWS Organizations(SCP), Azure Policy/GCP Org Policy, Config Rules(보안 컴플라이언스), Cost Explorer + CUR(FinOps), Tagging Strategy(Env/Owner/CostCenter) |

**핵심 알고리즘 및 메커니즘**:
- **Consistent Hashing**: DynamoDB/Cassandra의 파티션 키 분산 (vnode 256개, 90% 부하 시 rebalance)
- **Raft Consensus**: etcd, Kafka KRaft, CockroachDB (Leader Election + Log Replication)
- **Two-Phase Commit (2PC)**: 분산 트랜잭션 (Prepare -> Commit, 단 코디네이터 장애 시 Blocking 가능)
- **Saga Pattern**: 보상 트랜잭션(Compensating Tx)으로 Long-Running Business Transaction 처리 (Orchestration vs Choreography)
- **Quorum (W+R>N)**: DynamoDB 튜닝 가능 일관성 (`W=2, R=2, N=3` -> Strong; `W=1, R=1, N=3` -> Eventual)

- **📢 섹션 요약 비유**: 클라우드 4계층 스택은 "고층 아파트"와 같다. 1층은 토대(물리 하드웨어), 2층은 뼈대(EC2·VPC), 3층은 엘리베이터 시스템(K8s), 4층은 실제 거주자(앱·Lambda)다. 4층의 입주민이 늘어나면 3층의 엘리베이터가 자동으로 더 많은 캐빈(Pod)을 배치하고, 2층의 뼈대는 유연하게 확장된다.

---

## Ⅲ. 비교 및 연결

| 구분 | IaaS (EC2, Compute Engine) | PaaS (Beanstalk, App Engine, Heroku) | Serverless (Lambda, Cloud Functions) | On-Premise (VMware) |
| :--- | :--- | :--- | :--- | :--- |
| **추상화 수준** | VM·OS·미들웨어 직접 제어 | 런타임·미들웨어 자동 관리 | 함수 코드만 작성, 인프라 0관리 | 하드웨어부터 직접 운영 |
| **Cold Start 지연** | 30초~수 분 (인스턴스 기동) | 30초~2분 (컨테이너 풀) | **100ms~1초** (Init 단계, SnapStart로 10ms) | 0ms (이미 가동 중) |
| **최소 과금 단위** | 1시간 (또는 초 단위, Linux만) | 1시간 ~ 1일 | **100ms 단위, 1M 요청 무료** | CapEx (감가상각 5년) |
| **확장성 패턴** | 수동/예약 기반, 최대 ~10K 인스턴스 | 자동(5~50 인스턴스), Quota 제한 | 자동 0~수천 동시 (Concurrency Limit) | 수동, HW 조달 리드타임 |
| **적합 워크로드** | 레거시 Lift-Shift, GPU/CUDA, Stateful | 12-Factor App, 일반 웹/API | Event-Driven, Spike 워크로드, Batch | 규제/데이터 주권, 극저지연 |
| **이전 비용 vs 운영 비용** | 중간 전환, 운영 부담 큼 | 높은 전환, 운영 경감 | 매우 높은 전환(리팩터링), 운영 최소 | CapEx 최대 |
| **네트워크 통제력** | 완전 통제 (SG, NACL, Routing) | 부분 통제 | VPC Connector로만 제한적 | 완전 통제 |

**Multi-Cloud vs Hybrid Cloud 연결 아키텍처**:
- **Multi-Cloud**: AWS + GCP + Azure를 동시 사용. 클라우드 간 트래픽은 **Egress 비용** ($0.02~$0.09/GB)이 발생하며, 일반적으로 `Cloud Interconnect (AWS DX, GCP Partner Interconnect, Azure ER)` 같은 전용선으로 TCO를 절감한다. 데이터 중복성 확보, 벤더 종속(Vendor Lock-in) 회피, 지역별 컴플라이언스 대응이 목적이다.
- **Hybrid Cloud**: On-Prem + Public Cloud (예: AWS Outposts, Azure Stack, Google Anthos). 일반적으로 `Outposts는 리전 API와 동일 IAM 사용`, 데이터 주권이 필요한 워크로드(DB, PII)만 온프레미스에 유지하고, 나머지는 클라우드로 Burst Out한다.
- **Cloud-to-Ground Integration**: Direct Connect(MACsec 지원) + Transit Gateway + Site-to-Site VPN(Redundant Tunnels) 조합으로 99.9% 연결성 보장.

- **📢 섹션 요약 비유**: IaaS는 "렌터카", PaaS는 "대리운전", Serverless는 "택시 호출"과 같다. 렌터카는 운전대를 잡지만 주유·정비를 내가 하고, 대리운전은 차는 제공되지만 경로만 알려주면 되고, 택시는 목적지만 말하면 모든 것이 자동이다. 대신 택시 요금이 미터기로 누적되듯 Serverless는 호출 횟수·실행 시간에 따라 과금된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **워크로드 특성 분류 (Stateful vs Stateless, Latency-Sensitive vs Batch)**: RDBMS(Aurora, RDS, Cloud SQL)는 Stateful·Latency-Sensitive이므로 단일 AZ가 아닌 Multi-AZ(Master + Standby, Sync Replication, RPO=0) 구성 필수. Stateless API(ALB + ECS)는 Multi-AZ Auto Scaling으로 가용성 확보. Lambda는 Stateless 한정, 상태는 DynamoDB/ElastiCache에 위임.
2. **단일 장애점(SPOF) 식별 및 제거**: NAT Gateway 단일 -> NAT Gateway × 2 + 각 AZ 배치. ALB 단일 리전 -> Global Accelerator + 리전별 ALB. Aurora 단일 인스턴스 -> Aurora Multi-Master 또는 Global Database(리전 간 복제, RPO < 1초, RTO < 1분).
3. **데이터 거버넌스 및 컴플라이언스**: PII/금융/의료 데이터는 KMS-CMK(Customer Managed Key) + BYOK(Bring Your Own Key) + CloudHSM(FIPS 140-2 Level 3) 적용. 로그/감사 데이터는 Object Lock(WORM) + Cross-Account + Glacier Deep Archive로 변조 방지. 한국 개인정보보호법·전자금융거래법·의료법의 국내 리전(Seoul/Tokyo) 강제.
4. **비용 최적화 (FinOps)**: Reserved Instance(1/3년, 40~60% 할인) + Savings Plans(Compute/Flex, EC2·Fargate·Lambda 통합)
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 714 / 800

<- **이전**: [713. 클라우드 아키텍처 핵심 토픽 713번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/713_cloud_architecture_core_topic_713_exam_summar/)
**다음**: [715. 클라우드 아키텍처 핵심 토픽 715번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/715_cloud_architecture_core_topic_715_exam_summar/) ->

---
