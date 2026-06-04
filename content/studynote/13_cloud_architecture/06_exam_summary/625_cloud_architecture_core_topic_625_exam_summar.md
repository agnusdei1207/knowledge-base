---
title: "625. 클라우드 아키텍처 핵심 토픽 625번 시험 요약 (Cloud Architecture Core Topic 625 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


# 625. 클라우드 아키텍처 핵심 토픽 — 시험 요약

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 "탄력적 자원 풀(Elastic Resource Pool) + 셀프서비스 API + 사용량 기반 과금(Metered Billing) + 추상화된 인프라 레이어"를 통해 CAP 정리·PACELC·12-Factor 원칙 위에서 워크로드의 가용성·확장성·비용 효율성을 동적으로 최적화하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: AWS·Azure·GCP의 Well-Architected Framework 적용 시 평균 MTTR 65% 단축, Auto-Scaling으로 Peak 시간대 컴퓨팅 비용 40–70% 절감, Multi-AZ·Multi-Region 구성으로 RPO 0~15분 / RTO 15분~1시간 달성, Time-to-Market를 On-Prem 대비 1/3~1/5 수준으로 단축한다.
> 3. **판단 포인트**: Lift-and-Shift(Rehost) vs Cloud-Native(Refactor/Replatform) 트레이드오프, 단일 클라우드 종속(Vendor Lock-in) 회피를 위한 **추상화 계층(Kubernetes, Terraform, Crossplane)** 도입 여부, 그리고 CAP 정리 관점에서 **일관성(Consistency)을 양보할 수 있는 도메인**(결제·재고 vs SNS 피드)에 대한 AP/CP 선택, 마지막으로 **FinOps·보안 거버넌스·데이터 주권**을 동시에 만족하는 Multi-Cloud/Hybrid 토폴로지 설계가 핵심 결정 사안이다.

---

## Ⅰ. 개요 및 필요성

클라우드 아키텍처는 2006년 AWS S3·EC2 출시로 시작된 컴퓨팅 자원의 **Utility Computing** 모델이 2014년 Kubernetes 1.0, 2017년 Knative/Serverless, 2020년 GitOps·ArgoCD, 2023년 Generative AI·LLMOps로 진화하면서 단순한 "가상 서버 임대"에서 **분산 시스템·이벤트 기반·셀프서비스형 플랫폼 엔지니어링**으로 패러다임이 전환된 결과물이다.

기존 On-Premise 아키텍처는 **수직 확장(Scale-Up)**, **예측 기반 용량 산정(Capacity Planning)**, **수동 배포(Manual Deployment)**, **장기 자산화(CAPEX)** 모델이 지배적이었으나, 디지털 전환 가속·트래픽 폭증(Bursty Traffic)·글로벌 사용자 분산·짧은 시장 출시 기한(Time-to-Market) 요구로 한계에 부딪혔다. 이에 **수평 확장(Scale-Out)**, **선언적 인프라(IaC)**, **불변 인프라(Immutable Infra)**, **사용량 기반 과금(OPEX)**, **API 기반 셀프서비스**를 핵심으로 하는 클라우드 네이티브 아키텍처가 등장했다.

```text
   [Legacy On-Premise 시대의 한계]              [Cloud-Native 아키텍처의 등장]
   +--------------------------+                +--------------------------------------+
   |  • Scale-Up 한계 (단일 HW)|                |  • Scale-Out (무한 수평 확장)         |
   |  • Provisioning 수개월    |   ------->     |  • Self-Service API (분 단위)        |
   |  • Silo 조직·수동 배포   |                |  • GitOps · CI/CD · Immutable Image  |
   |  • CAPEX 중심 (고정비)   |                |  • OPEX · Pay-per-Use (가변비)      |
   |  • DC 단일 장애점(SPOF)  |                |  • Multi-AZ · Multi-Region 이중화    |
   |  • DR 사이트 별도 투자   |                |  • Cross-Region Replica + Auto-Failover|
   +--------------------------+                +--------------------------------------+
              v                                                v
       TCO 절감 불가 / Time-to-Market ^              TCO 30~50%v / Agility^^ / 탄력성
```

```text
   [클라우드 아키텍처의 4대 핵심 특성 (NIST SP 800-145 + 클라우드 네이티브 확장)]
   +-------------------+-------------------+-------------------+-------------------+
   |  On-Demand Self-  |  Broad Network    |  Resource Pooling |  Rapid Elasticity |
   |  Service (API)    |  Access (Anywhere)|  (Multi-Tenant)   |  (Auto-Scale)     |
   +-------------------+-------------------+-------------------+-------------------+
            |                    |                   |                    |
            +--------+-----------+---------+---------+                    |
                     v                     v                              v
              +-------------------------------------------------------------+
              |  Measured Service (Metering) + Service Catalog + Marketplace|
              +-------------------------------------------------------------+
                                       |
                                       v
              +-------------------------------------------------------------+
              |  ★ 현대 클라우드 아키텍처의 7대 추가 핵심 (Cloud-Native 7P)   |
              |  ① Microservice  ② Container(OCI)  ③ Orchestrator(K8s)       |
              |  ④ Service Mesh  ⑤ Serverless(FaaS)  ⑥ GitOps(IaC)          |
              | ⑦ Observability(OpenTelemetry)                               |
              +-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"호텔 체인 프랜차이즈"**와 같다. 각 호텔(Region/AZ)은 동일한 품질 기준(Well-Architected Framework)으로 운영되며, 손님(워크로드)은 체크인 시 Self-Service 키오스크(IAM·API)로 빈 방(EC2·Pod)을 즉시 배정받고, 사용한 미니바·조식(스토리지·네트워크)은 자동 정산(Metering)된다. 호텔 측은 룸 클리닝·메인터넌스(패치·백업·DR)를 책임지며 손님은 비즈니스 로직에만 집중한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **"제어 평면(Control Plane) + 데이터 평면(Data Plane)"**의 이원화된 구조로 동작하며, 글로벌 트래픽 라우팅부터 워크로드 격리까지 다층 계층(Layered Architecture)으로 구성된다. AWS·Azure·GCP 같은 하이퍼스케일러는 Region -> Availability Zone(1개 이상 DC) -> Edge Location(PoP·CDN) -> Interconnect(Direct Connect·ExpressRoute·Cloud Interconnect) 계층을 제공하며, 컨트롤러 평면은 **분산 합의 알고리즘(Raft/Paxos)** 기반으로 글로벌 상태를 동기화한다.

```text
   [글로벌 클라우드 아키텍처 — 4계층 토폴로지 (AWS 기준)]
   +---------------------------------------------------------------------+
   | L0: Edge / CDN Layer                                               |
   |   - CloudFront / Azure Front Door / Cloud CDN (250+ PoP)            |
   |   - Anycast IP, TLS Termination, WAF, DDoS Shield(L3-L7)           |
   +---------------------------------------------------------------------+
   | L1: Global Control Plane (Region 간 복제·라우팅)                    |
   |   - Route 53 Latency/Geolocation/Weighted Policy                    |
   |   - Global Accelerator (TCP/UDP Anycast)                            |
   |   - DynamoDB Global Tables / Cosmos DB Multi-Region (Active-Active)|
   +---------------------------------------------------------------------+
   | L2: Regional Services (Region 단위 격리·재해복구)                   |
   |   +------------+------------+------------+                          |
   |   | AZ-a (DC-1)| AZ-b (DC-2)| AZ-c (DC-3)|   <- 독립 전력·냉각·네트워크|
   |   | +--------+ | +--------+ | +--------+ |                          |
   |   | | NLB/ALB| | | NLB/ALB| | | NLB/ALB| |   L4/L7 Load Balancer     |
   |   | +--------+ | +--------+ | +--------+ |                          |
   |   | +--------+ | +--------+ | +--------+ |                          |
   |   | |EC2/ECS | | |EC2/ECS | | |EC2/ECS | |   Compute Plane          |
   |   | +--------+ | +--------+ | +--------+ |                          |
   |   |  EBS·EFS·S3 (AZ-scoped / Cross-AZ)                              |
   |   +------------+------------+------------+                          |
   |   - Auto Scaling Group · EKS/ECS Control Plane · RDS Multi-AZ      |
   +---------------------------------------------------------------------+
   | L3: Interconnect & Private Network                                 |
   |   - VPC Peering / Transit Gateway / PrivateLink                      |
   |   - Direct Connect / ExpressRoute (전용선, 1~100Gbps)               |
   |   - Site-to-Site VPN (IPsec), MACsec, BGP AS-Path                  |
   |   - Egress: NAT Gateway · Internet Gateway · Egress-only IGW       |
   +---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **전역 제어 평면(Global Control Plane)** | 계정·리소스·라우팅 테이블의 글로벌 일관성 보장 | IAM(STS·OIDC·SAML)·Org Unit·SCP(Service Control Policy)·Route 53 HealthCheck 기반 DNS Failover(TTL 60s)·Global Accelerator(Anycast) |
| **컴퓨트 추상화(Compute Abstraction)** | 가상화(KVM/Xen/Nitro Hypervisor) -> 컨테이너 -> 함수로의 추상화 스펙트럼 | EC2(Nitro System: 하드웨어 오프로드, 400Gbps) · ECS/EKS(Kubernetes 1.30, eBPF) · Lambda(컨테이너 이미지 10GB·15분 타임아웃) · Fargate(서버리스 K8s) |
| **스토리지 계층(Storage Tier)** | Hot·Warm·Cold·Glacier 단계별 가격·내구성 트레이드오프 | S3(99.999999999% 11 9s, Object-Lock·Versioning) · EBS(gp3 4,000 IOPS, io2 Block Express 256K IOPS) · EFS/FSx(Lustre·ONTAP, NFS/SMB) · Glacier Instant Retrieval(밀리초) · Deep Archive(12h) |
| **데이터 평면 네트워킹(Data Plane Network)** | VPC(Virtual Private Cloud) 기반 L3·L4·L7 정책 | VPC CIDR(/16, ENI·EFA·SR-IOV) · Security Group(Stateful) vs NACL(Stateless) · Transit Gateway(Hub-Spoke, 5,000 VPC) · PrivateLink(서비스 단위 ENI, 0 Hot-Potato) · Cloud WAN(Segmentation) |
| **오케스트레이션·서비스 메시(Orchestration & Service Mesh)** | 선언적 배포·트래픽 관리·관측성 | Kubernetes(etcd Raft, CRD·Operator) · Istio(Envoy xDS, mTLS SPIFFE) · Linkerd(Linkerd2-proxy Rust) · ArgoCD/Flux(GitOps) · Crossplane(Cloud Resource Controller) |
| **관측 가능성(Observability)** | Metrics·Logs·Traces 3축 + Continuous Profiling | OpenTelemetry(OTLP 프로토콜) · Prometheus + Thanos/Cortex(Multi-Cluster) · Grafana(Loki·Tempo·Mimir) · AWS X-Ray / CloudWatch RUM / GCP Cloud Operations |
| **보안·컴플라이언스(Security & Compliance)** | Zero Trust·CSPM·CWPP·CIEM | IAM Access Analyzer · AWS GuardDuty(Threat Intel) · Security Hub(CIS·PCI·HIPAA) · KMS/HSM(FIPS 140-2 L3) · Macie(데이터 분류) · VPC Flow Logs·CloudTrail |

### 핵심 동작 원리 심화

**(1) 탄력성(Elasticity) 알고리즘**: 클라우드 오토스케일링은 **예측형(Predictive: 머신러닝 기반, Amazon EC2 Auto Scaling Predictive Scaling) + 반응형(Reactive: CloudWatch·Prometheus 메트릭 기반) + 예약형(Scheduled: cron·KEDA CronScaler)** 3가지가 결합된다. HPA(Horizontal Pod Autoscaler) v2는 CPU/Memory/RPS/Custom Metric을 기반으로 `desiredReplicas = ceil[currentReplicas × (currentMetricValue / targetMetricValue)]` 공식을 사용하며, KEDA(Event-Driven Autoscaler)는 Kafka Lag·SQS QueueDepth·Cron 같은 이벤트 소스 60+개를 기반으로 0↔N 스케일링을 수행한다. **Cool-down(Stabilization Window)** 기본 5분은 스케일링 플래핑(Thrashing)을 방지한다.

**(2) 일관성 모델(Consistency Model)**: 글로벌 분산 시스템에서 CAP 정리는 **CP(Consistency + Partition Tolerance: DynamoDB Global Tables는 Multi-Region Strong 옵션, DynamoDB Local에서 `ConsistentRead=true`)** vs **AP(Availability + Partition Tolerance: DynamoDB Global Tables 기본, S3, Aurora Global Database의 Write Forwarding)** 선택으로 귀결된다. PACELC 관점에서는 "분단 시 일관성·가용성, 평시 지연시간·일관성"의 4개 트레이드오프가 존재하며, **금융 결제(Strong) / 카탈로그·SNS(Eventual) / 분석·로그(Read-Your-Writes)** 등 도메인별로 다른 모델을 적용해야 한다.

**(3) 컴퓨트 격리 메커니즘**: 클라우드 컴퓨트는 **하드웨어 가상화(Type-1 Hypervisor: KVM·Xen·Nitro) -> 마이크로 VM(Firecracker, gVisor) -> 컨테이너(runc, containerd) -> 샌드박스(WASM, gVisor runsc, kata-runtime)** 의 스펙트럼을 가지며, 보안·콜드 스타트·성능 간 트레이드오프가 있다. AWS Nitro System은 2017년 도입되어 EC2 인스턴스의 네트워킹·스토리지·관리 기능을 전용 하드웨어·경량 하이퍼바이저로 오프로드, 인스턴스 대역폭을 100Gbps -> 400Gbps로 확대하고 호스트 OS를 제거해 **Attack Surface 87% 감소**를 달성했다.

- **📢 섹션 요약 비유**: **"스마트 그리드 + 공항 관제탑"**의 결합이라 할 수 있다. 스마트 그리드는 사용자 수요에 따라 전기(컴퓨트)를 실시간 배분하고(탄력성), 공항 관제탑은 활주로(Availability Zone)별로 이착륙(트래픽)을 조정하며 모든 비행기(워크로드)는 출발전 매니페스트(IAM 역할)와 탑승권(OAuth 토큰)을 검증받는다. 정전(장애) 시에는 자동으로 다른 활주로로 우회(라우팅)된다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처는 전통적 아키텍처뿐 아니라 컨테이너·서버리스·엣지 컴퓨팅 등 유사·경쟁 기술과 명확한 구분이 필요하다. 기술사 시험에서는 **"왜 이 기술을 선택했는가"**의 정당화를 요구하므로 비교 기준을 정확히 이해해야 한다.

| 구분 | **On-Premise(전통적 3-Tier)** | **Private Cloud(OpenStack·VMware)** | **Public Cloud(AWS·Azure·GCP)** | **Hybrid / Multi-Cloud** |
| :--- | :--- | :
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 625 / 800

<- **이전**: [624. 클라우드 아키텍처 핵심 토픽 624번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/624_cloud_architecture_core_topic_624_exam_summar/)
**다음**: [626. 클라우드 아키텍처 핵심 토픽 626번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/626_cloud_architecture_core_topic_626_exam_summar/) ->

---
