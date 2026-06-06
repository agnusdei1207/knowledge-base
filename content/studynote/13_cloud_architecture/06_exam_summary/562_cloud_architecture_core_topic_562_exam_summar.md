---
title: "Cloud Architecture Core Topic 562 Exam Summary"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS로 추상화된 컴퓨팅·스토리지·네트워크 자원을 API·IaC·정책 기반으로 선언적(Declarative)하게 프로비저닝하고, 컨트롤 플레인과 데이터 플레인을 분리하여 워크로드의 탄력성·가용성·확장성을 보장하는 분산 시스템 설계 원리이다.
> 2. **가치**: AWS Well-Architected 5대 기둥(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화 + 지속 가능성) 준거 시 MTTR 60% 단축, Auto Scaling을 통한 CapEx->OpEx 전환으로 TCO 30~70% 절감, 멀티 리전 Active-Active 구성으로 99.99% SLA(연간 52.6분 이내 장애) 달성이 가능하다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs 멀티/하이브리드, Stateless Microservices + Managed Service 우선 vs 레거시 Lift&Shift, 동기적 강결합(Synchronous Tight Coupling) vs 비동기 Event-Driven(EDA), Consistency vs Availability(CAP/PACELC), Egress 비용·데이터 주권·종량제 과금의 트레이드오프를 워크로드의 RTO/RPO·트래픽 패턴·컴플라이언스 요건과 함께 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 아키텍처는 3-tier(Monolithic Web-App-DB) 구조로 수직 확장(Scale-Up)·장기 용량 계획·수작업 프로비저닝에 의존해, 트래픽 변동성(예: Black Friday 100배 스파이크), DR(Disaster Recovery) 한계, CapEx 과다 투자, 수개월의 조달 리드타임이라는 구조적 한계를 가진다. 2006년 AWS S3·EC2 출시 이후 IaaS가, 2014년 Kubernetes 1.0과 동시에 서버리스(Lambda, 2014)/컨테이너 오케스트레이션이 등장하면서 **"코드 = 인프라"** 패러다임이 정착되었고, CNCF(Cloud Native Computing Foundation) 라이브러리 landscape는 2024년 기준 1,000+ 프로젝트를 포함한다. 12-Factor App(Heroku, 2012), AWS Well-Architected Framework(2015, 지속 가능성 2021 추가), AWS Cloud Adoption Framework(CAF), Azure Architecture Center, GCP Cloud Architecture Framework 같은 거버넌스 프레임워크가 기술사 시험의 평가축으로 작용한다.

```text
+---------------------------------------------------------------------+
|              On-Premise -> Cloud-Native 진화 아키텍처                 |
+---------------------------------------------------------------------+
|                                                                     |
|  [T0: Mainframe 1960s]      [T1: Client-Server 1990s]               |
|  +----------+               +----------+                            |
|  | 단일 대형 |               | 2-Tier   |   물리적 HW 의존            |
|  | 컴퓨팅   |               | C/S      |   수직 확장 한계             |
|  +----+-----+               +----+-----+                            |
|       |                          |                                  |
|       v                          v                                  |
|  [T2: 3-Tier + Virtualization 2000s]                                |
|  +--------+--------+--------+                                       |
|  |  Web   |  App   |   DB   |  <- Hypervisor(VirtualBox/VMware)      |
|  |  Tier  |  Tier  |  Tier  |    VM 기반 수동 스케일링              |
|  +--------+--------+--------+    L4 LB(F5, 하드웨어)                 |
|       |                                                              |
|       v                                                              |
|  [T3: Public Cloud IaaS 2006+]                                      |
|  +------------+  +------------+  +------------+                    |
|  | EC2(VM)    |  | S3(Obj)    |  | RDS(MP)   | <- API/CLI 프로비저닝 |
|  | Auto Scale |  | 11 9s Dur. |  | Multi-AZ  |    Pay-as-you-go    |
|  +-----+------+  +-----+------+  +-----+------+                    |
|        +-----------------+---------------+                          |
|                          v                                          |
|  [T4: Cloud-Native 2015+]                                           |
|   +--------------------------------------------+                    |
|   |  Container (Docker) + Orchestrator (K8s)   |                    |
|   |  Service Mesh (Istio) + Serverless (Lambda)|  <- 선언적 IaC      |
|   |  GitOps (ArgoCD) + Observability (Prometheus)|  <- 불변 인프라    |
|   +--------------------------------------------+                    |
|                          v                                          |
|  [T5: AI-Native / Platform Engineering 2024+]                       |
|   Internal Developer Platform(IDP) + AIOps + FinOps 자동화           |
+---------------------------------------------------------------------+
```

**왜 클라우드 아키텍처가 필수인가?**

| 차원 | 온프레미스 | 클라우드 네이티브 |
|:---|:---|:---|
| 프로비저닝 | 수주~수개월 (조달) | 수초~수분 (API/Terraform) |
| 확장성 | Scale-Up(수직, HW 한계) | Scale-Out(수평, 무제한) |
| 장애 대응 | Cold Standby(RTO 수시간) | Multi-AZ Active-Active(RTO < 1분) |
| 비용 모델 | CapEx(선투자, 감가상각) | OpEx(사용량 기반, TCO 30~70%v) |
| 거버넌스 | 수동 티켓, Change Board | Policy as Code(OPA, SCP), GuardRails |

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 진화는 마치 **"발전기 자가 발전 -> 수도꼭지에서 물 끌어다 쓰기"** 로의 변화와 같다. 발전기(자체 데이터센터)는 초기 설치비가 크고 고장 시 직접 수리해야 하지만, 수도관(클라우드)은 필요한 만큼 즉시 끌어다 쓰고 누수(장애)도 공급자가 책임진다. 그러나 수도요금(Egress/스토리지)을 관리하지 않으면 청구서가 폭탄이 되듯, FinOps 없이는 비용 폭증이 발생한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **4계층 참조 모델**(워크로드, 데이터, 거버넌스, 플랫폼)로 분해되며, 각 계층은 API·IaC·Observability로 횡단 연결된다. AWS Well-Architected 5(+1) 기둥이 평가 프레임워크, 12-Factor App이 애플리케이션 설계 원칙, TOGAF·Zachman이 엔터프라이즈 통합 관점의 청사진을 제공한다.

```text
+---------------------------------------------------------------------+
|         Cloud-Native Reference Architecture (4-Layer Model)         |
+---------------------------------------------------------------------+
|                                                                     |
|  +---------------------------------------------------------------+  |
|  | Layer 4: Workload (비즈니스 로직)                              |  |
|  |  Microservices(12-Factor)  |  Event-Driven(EDA)               |  |
|  |  Serverless(FaaS)          |  Strangler Fig Pattern            |  |
|  |  예: Order/Payment/Inventory Svc, Saga Orchestrator            |  |
|  +-----------------------╤---------------------------------------+  |
|                          | mTLS / gRPC / REST + OAuth2/JWT         |
|  +-----------------------v---------------------------------------+  |
|  | Layer 3: Application Platform                                  |  |
|  |  +------------+ +------------+ +----------------+              |  |
|  |  | K8s Service| | Service    | | API Gateway    |              |  |
|  |  | (EKS/AKS)  | | Mesh(Istio)| | (Kong/Apigee)  |              |  |
|  |  +-----+------+ +-----+------+ +--------+-------+              |  |
|  |        | Sidecar(Envoy) | Circuit Breaker| Rate Limiting        |  |
|  +--------╪----------------╪--------------╪-----------------------+  |
|           |                |              |                          |
|  +--------v----------------v--------------v-----------------------+  |
|  | Layer 2: Data Plane                                           |  |
|  |  +----------+  +----------+  +----------+  +----------+       |  |
|  |  | RDBMS    |  | NoSQL    |  | Object   |  | Stream   |       |  |
|  |  | Aurora   |  | DynamoDB |  | S3(11x9) |  | Kafka/MSK|       |  |
|  |  | (OLTP)   |  | (KV/Wide)|  | (DataLk) |  | (EDA)    |       |  |
|  |  +----------+  +----------+  +----------+  +----------+       |  |
|  |  CDC(Debezium) -> Lakehouse(Iceberg) -> BI(Redshift/BigQuery)  |  |
|  +----------------------------------------------------------------+  |
|           |                                                          |
|  +--------v--------------------------------------------------------+  |
|  | Layer 1: Infrastructure (Control + Data Plane)                 |  |
|  |  Compute(EC2/VM)  Network(VPC/TGW/CloudWAN)  Storage(EBS/EFS)  |  |
|  |  Region(≥2) -> AZ(≥3) -> Edge Location / CDN(CloudFront)         |  |
|  |  IaC: Terraform/CloudFormation/Pulumi  |  Policy: SCP/OPA      |  |
|  +----------------------------------------------------------------+  |
|           |                                                          |
|  +--------v--------------------------------------------------------+  |
|  | Cross-Cutting: Observability & Security                        |  |
|  |  Logs/Metrics/Traces (OpenTelemetry -> Prometheus/Loki/Tempo)   |  |
|  |  IAM(least priv.) + KMS + Secrets Mgr + GuardDuty(UEBA)        |  |
|  |  FinOps: Cost Explorer, Anomaly Detection, CUR(비용 사용 리포트) |  |
|  +----------------------------------------------------------------+  |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **컴퓨트 추상화 계층** | 워크로드 실행 환경 제공 | **EC2/VM**(AMI+EBS, M5/C5/Inf2), **컨테이너**(ECS Fargate, EKS, GKE Autopilot — K8s 1.30+ Sidecarless via eBPF/Cilium), **서버리스**(Lambda 15분 제한 + EFS/SnapStart, Azure Functions Flex Consumption, Cloud Run Jobs). Cold Start 100~800ms 완화 위해 Provisioned Concurrency/SnapStart/Pre-warming 적용. |
| **스토리지 계층** | 데이터 영속성·내구성·접근 패턴 최적화 | **Object(S3 Standard/IA/Glacier Instant Retrieval·Deep Archive)** 99.999999999%(11 9s) 내구성, **Block(EBS gp3, io2 Block Express)**, **File(EFS, FSx for Lustre)**, **NoSQL(DynamoDB Global Tables — Multi-Region Strong/Eventual Consistency)**, **RDBMS(Aurora 6-way replication, 읽기 복제 < 1s lag)**, **Lakehouse(Iceberg/Delta/Hudi + Athena/Trino/Redshift Spectrum)**. |
| **네트워크 & 연결** | L3~L7 트래픽 제어, 보안 경계 | **VPC**(Private/Public/Database 서브넷, /16~19 CIDR), **TGW(Transit Gateway)** Hub-Spoke, **Cloud WAN**(SD-WAN 글로벌), **Direct Connect/ExpressRoute**(전용선 1~10Gbps), **ALB/NLB/GLB**(L7/L4/Anycast), **CloudFront/Azure Front Door/Cloud CDN**(TLS 1.3, HTTP/3/QUIC), **Route 53**(Latency/Geolocation/Weighted Policy). |
| **오케스트레이션 & 메시** | 컨테이너 라이프사이클, 트래픽 관리 | **Kubernetes 1.31+**(Sidecar Containers GA, Pod Resources QOS), **Istio/Linkerd**(mTLS 자동, mTLS STRICT/PERMISSIVE 모드, Circuit Breaker — Consecutive5xxErrors -> 30s Eject), **Argo Rollouts**(Canary/Blue-Green 10%->50%->100%, AnalysisTemplate + Prometheus 쿼리 기반 자동 롤백), **Knative**(Event-driven autoscaling, KEDA). |
| **거버넌스·보안·관측** | 정책·컴플라이언스·가시성 | **IAM**(RBAC + ABAC Tag 기반
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 562 / 800

<- **이전**: [561. 클라우드 아키텍처 핵심 토픽 561번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/561_cloud_architecture_core_topic_561_exam_summar/)
**다음**: [563. 클라우드 아키텍처 핵심 토픽 563번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/563_cloud_architecture_core_topic_563_exam_summar/) ->

---
