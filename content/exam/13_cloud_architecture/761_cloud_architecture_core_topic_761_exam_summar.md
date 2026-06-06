---
title: "Cloud Architecture Core Topic 761 Exam Summary"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS의 4계층 서비스 모델을 기반으로, 컨트롤 플레인(API/오케스트레이터)과 데이터 플레인(컴퓨트/스토리지/네트워크)의 책임 분리(Separation of Concerns)를 통해 탄력성(Elasticity)과 페일오버(Failover)를 코드와 정책으로 구현한 분산 시스템 설계 청사진이다.
> 2. **가치**: CAPEX에서 OPEX로의 전환(초기 투자비 60~80% 절감), Auto-Scaling을 통한 트래픽 변동 대응(평균 35~50% 비용 최적화), MTTR(Mean Time To Recovery) 70% 단축, 그리고 글로벌 멀티 리전 아키텍처를 통한 RPO/RTO를 분 단위로 단축시킬 수 있는 비즈니스 연속성 확보가 핵심 가치다.
> 3. **판단 포인트**: "Build vs Buy" 시 SaaS 도입 시 데이터 주권(lock-in) vs 자체 PaaS 기반 구축의 TCO 3~5년 회수율, "Region vs AZ" 선택 시 지연시간(Latency) vs 비용의 트레이드오프, 그리고 "Synchronous(Strong Consistency)" vs "Eventually Consistent(AP)" 모델 선택 시 트랜잭션 무결성 vs 가용성의 분산 시스템 CAP 정리가 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스(On-Premise) 환경은 **수직적 확장(Scale-Up)**, **장기 자산 투자(CAPEX)**, **수동적 장애 대응(Reactive)** 이라는 3대 제약으로 인해 디지털 트랜스포메이션 시대의 요구사항—秒単位의 시장 변화 대응, 예측 불가능한 트래픽 폭증 처리, 글로벌 사용자 대상의 24/7 서비스—을 충족할 수 없게 되었다. 2006년 AWS S3 출시 이후 20여 년간 진화한 클라우드 아키텍처는 **가상화(Hypervisor -> Container -> Unikernel)**, **API-first 설계**, **선언적 인프라(Declarative Infrastructure as Code)**, **불변 인프라(Immutable Infrastructure)** 의 4가지 패러다임 전환을 통해 이러한 한계를 근본적으로 해소했다.

특히 2014년경 Kubernetes 출시와 2018~2020년 Serverless/Service Mesh의 보편화, 그리고 2023년 이후 생성형 AI 워크로드(LLM Inference)를 위한 GPU 가상화/NDP(Network Data Plane) 가속이 더해지면서, 클라우드 아키텍처는 단순한 "외부 위탁 호스팅"이 아니라 **"비즈니스 도메인에 최적화된 분산 시스템의 전사적 설계 표준"** 으로 자리매김했다.

```text
[클라우드 아키텍처 패러다임 진화 흐름]

  +------------------+    +------------------+    +------------------+
  |  Mainframe Era   |    |   Client-Server  |    |  3-Tier Web      |
  |  (1960-1990)     |---->|   (1990-2005)    |---->|  (2005-2010)     |
  |  - 중앙 집중     |    |  - DB 분산       |    |  - WAS + L4 SW   |
  |  - MTTR: 일 단위 |    |  - MTTR: 시간 단위|    |  - MTTR: 분 단위 |
  +------------------+    +------------------+    +--------+---------+
                                                            |
        +---------------------------------------------------+
        v
  +------------------+    +------------------+    +------------------+
  |  Cloud IaaS      |    | Cloud-Native     |    | AI-Native Cloud  |
  |  (2010-2015)     |---->| (2015-2022)      |---->| (2023-현재)      |
  |  - VM 가상화     |    |  - K8s, MSA      |    |  - GPU Pooling   |
  |  - SDN/NFV       |    |  - Istio, Knative|    |  - Vector DB     |
  |  - 객체 스토리지 |    |  - GitOps, OTel  |    |  - LLM Gateway   |
  +------------------+    +------------------+    +------------------+

  [핵심 동인: 트래픽 변동성, 비즈니스 민첩성, 글로벌 확장성, TTM(Time-To-Market)]
```

기존 IDC(Internet Data Center) 운영 모델 대비 클라우드 아키텍처는 **사용량 기반 과금(Usage-Based Pricing)**, **셀프서비스 프로비저닝(API 기반)**, **자동화된 탄력성(Elasticity)**, **글로벌 엣지 배포** 라는 4대 본질적 차이를 가진다. 이는 곧 아키텍트의 사고방식을 "**예측적 용량 계획(Capacity Planning)** -> **실시간 관측 가능성(Observability-Driven) 설계**"로 전환시켰다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **전기 그리드(Electric Grid)** 와 같다. 발전소(On-Premise 데이터센터)가 자체 발전기를 돌리던 시대에서, 송전망(Backbone Network)을 통해 사용량만큼(kWh) 전기를 즉시 공급받고, 정전 시 자동으로 예비 계통(DR Site)에 연결되는 사회적 분산 인프라(Utility Computing)다. 전기의 품질(주파수/전압) = SLA(99.95%), 발전 설비 = Region, 변전소 = AZ, 수용가 = Workload로 대응된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 기술적 핵심은 **5계층 책임 모델(Shared Responsibility Model)** 과 **컨트롤/데이터 플레인 분리**, 그리고 **선언적 API(Declarative API)를 통한 상태 조정(Reconciliation Loop)** 의 3가지 원리에 있다. 이를 컨테이너 오케스트레이션의 대표 사례인 Kubernetes로 구체화하면 다음과 같은 참조 아키텍처(Reference Architecture)로 표현된다.

```text
[클라우드 네이티브 참조 아키텍처 - MSA + Service Mesh + GitOps]

   +------------------------------------------------------------------+
   |                          사용자 (Browser/Mobile)                  |
   +---------------------------------+--------------------------------+
                                     | TLS 1.3, mTLS
                                     v
   +------------------------------------------------------------------+
   |  Global Edge Layer (CloudFront/Cloudflare CDN + WAF + DDoS)     |
   |  [L7 LB, 캐시, Bot 관리, Geo-Routing, Rate-Limiting]              |
   +---------------------------------+--------------------------------+
                                     |
                                     v
   +------------------------------------------------------------------+
   |  API Gateway / Ingress Controller (Kong / AWS API GW / Envoy)    |
   |  [인증(OAuth2/OIDC), 라우팅, Quota, Schema Validation, Tracing]   |
   +---------------------------------+--------------------------------+
                                     |
        +----------------------------+--------------------------------+
        v                            v                                v
   +------------+              +------------+                  +------------+
   | Service A  |              | Service B  |                  | Service C  |
   | (Pod/      |<---- Istio --->| (Pod/      |<----- Istio ----->| (Pod/      |
   |  Container)|     mTLS     |  Container)|       mTLS       |  Container)|
   | K8s/ECS    |              | EKS/AKS    |                  | Lambda/Fn  |
   +-----+------+              +-----+------+                  +-----+------+
         |                           |                               |
         v                           v                               v
   +--------------------------------------------------------------------+
   |  Data Plane: 분산 데이터 저장소 (Polyglot Persistence)            |
   |  +----------+  +----------+  +----------+  +------------------+  |
   |  | RDBMS    |  | NoSQL    |  | Cache    |  | Object/Blob      |  |
   |  | (Aurora, |  | (Dynamo, |  | (Redis,  |  | (S3, MinIO)      |  |
   |  |  Spanner)|  |  Mongo)  |  |  Memcached)| |                  |  |
   |  +----------+  +----------+  +----------+  +------------------+  |
   |  + Event Bus (Kafka, Kinesis, Pub/Sub) + Vector DB (Pinecone)     |
   +--------------------------------------------------------------------+
                                     ^
                                     | OTLP (OpenTelemetry)
   +---------------------------------+--------------------------------+
   |  Observability: Metrics / Logs / Traces (3 Pillars)               |
   |  [Prometheus, Grafana, Loki, Jaeger, Datadog, OpenSearch]         |
   +------------------------------------------------------------------+
                                     ^
                                     | Git Sync (ArgoCD/Flux)
   +---------------------------------+--------------------------------+
   |  Control Plane: IaC + GitOps                                      |
   |  [Terraform/Pulumi -> S3/Consul -> ArgoCD/Flux -> K8s API Server]   |
   +------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 계층 (Compute)** | 워크로드 실행 환경 제공 | VM(EC2/Azure VM), 컨테이너(EKS/AKS/GKE), Serverless(Lambda/Cloud Functions), Bare-Metal(상시 예약형 GPU). **vCPU 단위 과금**, **Burst Capability**(T-series), **Dedicated Host**(규제 준수용) |
| **스토리지 계층 (Storage)** | 데이터 영속성 및 IOPS 보장 | 블록(EBS/gp3, io2 Block Express 256K IOPS), 파일(EFS, FSx for Lustre), 객체(S3 - 11 9s 내구성, IA/Glacier 계층화). **EBS Provisioned IOPS**, **S3 Lifecycle Policy**, **CRR(Cross-Region Replication)** |
| **네트워크 계층 (Networking)** | L3~L7 트래픽 제어 및 격리 | VPC/Subnet(TGW/VPN/Interconnect), L4 NLB(Static IP, 수백만 PPS), L7 ALB(Header 기반 라우팅, WebSocket), PrivateLink(엔드포인트 기반 내부 통신), Cloud WAN(글로벌 Anycast) |
| **오케스트레이터 (Orchestrator)** | 컨테이너 라이프사이클 관리 | Kubernetes(Control Plane: API Server, etcd, Scheduler, Controller Manager + Data Plane: kubelet, kube-proxy, CRI/CSI/CNI). **Reconciliation Loop**(현재 상태->원하는 상태), **Operator Pattern**(CRD+Controller), **HPA/VPA/Cluster Autoscaler** |
| **관측 가능성 (Observability)** | 시스템 상태 측정 및 알림 | **3 Pillars**: Metrics(Prometheus/CloudWatch), Logs(Loki/CloudWatch Logs Insights), Traces(OpenTelemetry/Jaeger/X-Ray). SLI/SLO/SLA 기반 **Error Budget** 관리, **SRE(Service Reliability Engineering)** |
| **보안/ID 계층 (IAM)** | 인증/인가/감사 | **Zero Trust** 모델, IAM Role(OIDC Federation, IRSA), KMS/HSM(Envelope Encryption), Secrets Manager(자동 Rotation), GuardDuty/Inspector(위협 탐지), SCP(Service Control Policy) |
| **IaC/Policy as Code** | 인프라 선언적 정의 및 거버넌스 | Terraform(HCL 모듈), Pulumi(General-purpose Language), CloudFormation(StackSets), OPA(Open Policy Agent)/Conftest, Kustomize/Helm(쿠버네티스 패키징) |

**핵심 원리 1 — Reconciliation Loop (상태 조정 루프)**
Kubernetes Controller는 `Spec(원하는 상태)`과 `Status(현재 상태)`를 주기적으로(기본 10ms~30s 주기) 비교하여 차이를 해소하는 방향으로 API를 호출한다. 이는 **결국적 일관성(Eventual Consistency)** 을 채택한 분산 시스템의 전형적 패턴이며, 데이터베이스 트랜잭션의 ACID 대신 BASE(Basically Available, Soft state, Eventually consistent) 모델을 따른다.

**핵심 원리 2 — 12-Factor App 원칙**
200개 이상의 글로벌 엔지니어의 합의체인 12-Factor는 클라우드 네이티브 애플리케이션의 설계 헌장이다: (1) Codebase, (2) Dependencies, (3) Config(환경변수 분리), (4) Backing Services, (5) Build/Release/Run 분리, (6) Stateless Process, (7) Port Binding, (8) Concurrency, (9) Disposability(빠른 시작/종료), (10) Dev/Prod Parity, (11) Logs(Stdout 스트림), (12) Admin Processes(일회성 작업).

**핵심 원리 3 — Well-Architected Framework (5대 기둥)**
AWS 기준의 WAF는 (1) **Operational Excellence**(IaC, Runbook, Incident Postmortem), (2) **Security**(방어 계층, 최소 권한, 암호화), (3) **Reliability**(Multi-AZ, Auto-Healing, Disaster Recovery: Backup/ Pilot Light/ Warm Standby/ Multi-Site), (4) **Performance Efficiency**(Right-Sizing, Caching, CDN, Serverless), (5) **Cost Optimization**(Reserved/ Savings Plans, Spot Instance, S3 Intelligent-Tiering, Showback/Chargeback)을 정의한다. Google Cloud는 Sustainability 기둥을 추가해 6대 기둥으로 확장했다.

**핵심 공식 (가용성 및 비용 모델)**
- **합성 가용성(Composite Availability)**: `A_total = 1 - ∏(1 - A_i)` (예: 99.9% × 99.95% × 99.99% = 99.84%)
- **MTTR 기반 가용성**: `A = MTTF / (MTTF + MTTR)` (MTTF: Mean Time To Failure)
- **총소유비용(TCO)**: `TCO = CAPEX + OPEX(컴퓨팅 + 스토리지 + 네트워크 + 라이선스 + 인건비) - 비즈니스 기회비용`
- **Payback Period**: `Payback = 초기 CAPEX / (클라우드 절감 OPEX + 생산성 향상)`

- **📢 섹션 요약 비유**: 5계층 책임 모델은 **아파트 관리** 와 같다. 외부 벽체·지반·공용시설(클라우드: 물리적 서버·네트워크·전원)은 관리사무소(클라우드 사업자)가 책임지고, 내 집 인테리어·보안장치·가구 배치(클라우드: OS 패치·방화벽·데이터 암호화)는 입주자(고객)가 책임진다. 경계가 모호해지면(예: 데이터 백업) 양쪽 다 책임이 발생할 수 있어 **명확한 RACI 매트릭스** 가 필수다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처는 유사 개념 및 선행/대안 기술과의 비교를 통해 의사결정의 기준선을 명확히 해야 한다.

| 구분 | **On-Premise (전통적 IDC)** | **Private Cloud (VMware/OpenStack)** | **Public Cloud (AWS/Azure/GCP)** | **Hybrid/Multi-Cloud** |
| :--- | :--- | :--- | :--- | :--- |
| **투자 모델** | CAPEX (3~5년 선투자) | CAPEX + OPEX 혼합 | OPEX (사용량 과금) | OPEX 위주 + 연결 비용 |
| **확장성** | 수직 확장 한계 (48~96 vCPU) | 수평 확장 가능 (제한적) | 무제한 (수평/탄력) | 워크로드별 최적 배치 |
| **배포 속도** | 수 주~수 개월 (HW 조달) | 수 시간~수 일 | 수 분~수 초 (API) | 수 분 (Burst to Public) |

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 761 / 800

<- **이전**: [760. 클라우드 아키텍처 핵심 토픽 760번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/760_cloud_architecture_core_topic_760_exam_summar/)
**다음**: [762. 클라우드 아키텍처 핵심 토픽 762번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/762_cloud_architecture_core_topic_762_exam_summar/) ->

---
