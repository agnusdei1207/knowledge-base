---
title: "Cloud Architecture Core Topic 578 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS의 서비스 모델과 Public/Private/Hybrid/Multi-Cloud의 배치 모델이 직교하는 2차원 설계 공간에서, **Well-Architected Framework 6대 축(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속 가능성)**과 **CNCF Cloud Native Landscape**의 구성요소를 비즈니스 요구사항과 SLA에 최적 결합하는 엔지니어링 discipline이다.
> 2. **가치**: AWS, Azure, GCP 등 hyperscaler 기반의 capex->opex 전환으로 인프라 투자 대비 ROI를 30~60% 향상시키고, Auto Scaling + Multi-AZ 아키텍처로 99.99% 가용성을 달성하며, **6R 마이그레이션(Rehost/Replatform/Refactor/Re-purchase/Retire/Retain)**을 통해 일반적으로 TCO 20~40% 절감, 배포 주기 수십 배 단축(리드타임: 수개월->수시간), 글로벌 사용자에 대한 p99 레이턴시를 100ms 이하로 확보한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **컨트롤 vs 편의(Managed Service 종속성·Vendor Lock-in)**, **일관성 vs 최적화(Multi-Cloud의 Cross-cloud 관리 복잡도 vs Cloud-native 최적화)**, **탄력성 vs 비용(Always-on 리소스 vs Burstable Workload)**, **강한 일관성 vs 결과적 일관성(분산 트랜잭션 CAP theorem)**이며, **Region/AZ 선택, 데이터 주권(데이터 레지던시), DR 전략(RPO/RTO 정의), FinOps 거버넌스, IaC와 GitOps 성숙도**가 아키텍처 의사결정의 핵심 변수가 된다.

---

## Ⅰ. 개요 및 필요성

전통적인 On-Premise 3-tier 아키텍처는 **EOL(End of License) 도래, 하드웨어 노후화, 트래픽 정적 용량 설계(Peak 기준 과잉투자), 수직 확장(Scale-up)의 한계, IDC 비용 상승(전력·냉각·회선), 24×7 운영 인력 부족**이라는 구조적 한계에 직면했다. 2006년 AWS S3·EC2 출시 이후 클라우드는 단순한 가상호스팅을 넘어 **프로그래머블 인프라(API-first), 선언적 오케스트레이션(Terraform/CloudFormation), 셀프서비스 카탈로그(Service Catalog), Consumption-based Billing**으로 진화했고, 2014년경 Kubernetes 1.0 출시와 2015년 CNCF 창립을 기점으로 **Cloud Native Computing** 패러다임이 정착되었다. 이는 **컨테이너(OCI 표준) -> 오케스트레이션(K8s) -> 서비스 메시(Istio/Linkerd) -> GitOps(ArgoCD/Flux) -> Observability(Prometheus/Grafana/OpenTelemetry) -> Serverless(Knative/Lambda)**로 이어지는 생태계 성숙을 의미한다.

기술사적 관점에서 클라우드 아키텍처는 더 이상 "클라우드를 쓸 것인가"가 아니라, **어떤 클라우드抽象化 레이어(VM/Container/Function/Managed Service)에서, 어떤 거버넌스 모델(중앙 집중 Cloud Center of Excellence vs 분산 Federated)로, 어떤 마이그레이션 전략(6R)을 적용할 것인가**의 의사결정 문제로 재정의되었다. 특히 **Digital Transformation(DX)**, **AI/ML 워크로드의 GPU 자원 탄력적 소비**, **데이터 주권 규제(개인정보보호법, GDPR, 데이터3법)**, **탄소 중립(Scope 3 배출량)**이 새로운 아키텍처 제약으로 부상하면서, 단순 비용 절감을 넘어 **탄력성(Elasticity), 회복탄력성(Resilience), 관측가능성(Observability), 자동화(Automation)**라는 4대 목표가 통합 설계되어야 한다.

```text
+--------------------------------------------------------------------------+
|           클라우드 아키텍처 진화 타임라인과 트리거 이벤트                     |
+--------------------------------------------------------------------------+
|                                                                          |
|  2006 --- AWS S3, EC2 출시 ---- "Infrastructure as a Service"            |
|   |       (가상화 기반, AMI 모델)                                         |
|   v                                                                      |
|  2010 --- RDS, Beanstalk ---- "Managed Service" 등장                     |
|   |       (운영 부담 외부화)                                              |
|   v                                                                      |
|  2014 --- K8s 1.0, Docker 1.0 -- "Container Orchestration"               |
|   |       (Cloud Native 1세대)                                            |
|   v                                                                      |
|  2015 --- CNCF 창립, Lambda -- "Serverless + Cloud Native 2세대"         |
|   |       (이벤트 기반, FaaS)                                             |
|   v                                                                      |
|  2017 --- Istio 1.0 -------- "Service Mesh"                              |
|   |       (Sidecar 패턴, mTLS, Traffic Mgmt)                              |
|   v                                                                      |
|  2018 --- Terraform 1.0 ---- "IaC 표준화"                                 |
|   |       (HCL 선언적 언어)                                               |
|   v                                                                      |
|  2020 --- ArgoCD, Flux ---- "GitOps 선언적 배포"                         |
|   |       (Git = Single Source of Truth)                                 |
|   v                                                                      |
|  2021 --- eBPF, OpenTelemetry -- "Observability 2.0"                     |
|   |       (Kernel-level Tracing)                                          |
|   v                                                                      |
|  2023 --- LLM/AI Cloud, FinOps -- "AI-Native + GreenOps"                |
|   |       (GPU TPU Pool, Carbon-aware Computing)                          |
|   v                                                                      |
|  2024~ -- Platform Engineering, IDP -- "Internal Developer Platform"     |
|          (Backstage, 셀프서비스 추상화)                                    |
+--------------------------------------------------------------------------+
```

기존 On-Premise 대비 클라우드의 핵심 차별점은 **①유한한 자원의 무한화(API로 수천대 VM을 1분 내 생성), ② 글로벌 엣지(CDN, CloudFront, Cloudflare)**, **③ API 거버넌스 기반의 셀프서비스(개발자가 인프라팀 승인 없이 5분 내 DB 생성)**, **④ 사용량 기반 과금(Pay-per-Use, Reserved/Committed Discount)**, **⑤ 컴플라이언스 자동화(SOC2, ISO27001, PCI-DSS 인증 inherit)**로 요약된다. 그러나 동시에 **Egress 비용 폭탄(데이터 반출 시 GB당 $0.09~0.12), Shadow IT(셀프서비스의 역기능), Vendor Lock-in(클라우드별 고유 서비스 종속), Shared Responsibility Model의 경계 인지 실패(클라우드 제공자가 OS 위는 보장하지만 데이터/접근제어는 고객 책임)**라는 새로운 리스크를 수반한다.

- **📢 섹션 요약 비유**: 클라우드 진화는 **"발전기 자가 발전 -> 수도·전기 공동주택 -> 스마트 그리드 + AI 에너지 매니저"**와 같다. 1세대 발전기(On-Premise)는 각자 연료를 넣고 관리해야 했고, 수도 공영(Public Cloud)은 계량기 과금으로 무제한 사용이 가능해졌으며, 현재의 스마트 그리드(Cloud Native + FinOps + GreenOps)는 AI가 수요 예측과 탄소 배출을 자동 최적화하는 단계에 도달했다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **① 계층화(Presentation -> API Gateway -> Service -> Data -> Infrastructure)**, **② 책임 분산(Shared Responsibility Model)**, **③ 제어 루프(Observe -> Decide -> Act)**의 3원칙으로 구성된다. AWS Well-Architected Framework, Azure Well-Architected Framework, Google Cloud Architecture Framework 모두 **운영 우수성(Operational Excellence), 보안(Security), 안정성(Reliability), 성능 효율(Performance Efficiency), 비용 최적화(Cost Optimization)** 5대 기둥을 공통으로 채택하며, AWS는 2021년 **지속가능성(Sustainability)**을 추가해 6대 기둥으로 확장했다.

핵심 구성요소는 **① 컴퓨트 추상화 레이어**, **② 네트워킹 토폴로지**, **③ 데이터 저장소 분류**, **④ 오케스트레이션·서비스 메시**, **⑤ IaC/GitOps**, **⑥ Observability 스택**, **⑦ 보안·컴플라이언스**로 분해된다. 컴퓨트 레이어는 **EC2(가상머신, 1ms 단위 과금) -> ECS/EKS/ACI/Kubernetes Engine(컨테이너 오케스트레이션) -> Fargate/Cloud Run(서버리스 컨테이너) -> Lambda/Functions/Cloud Functions(이벤트 기반 FaaS, ms 단위 과금)** 순으로 추상화 수준이 높아지고 관리 책임은 감소한다(반대로 커스터마이징 자유도는 감소).

```text
+------------------------------------------------------------------------------+
|        Cloud-Native Reference Architecture (Multi-Account/Project)           |
+------------------------------------------------------------------------------+
|                                                                              |
|  +--- Global Edge Layer ------------------------------------------------+   |
|  |  Route 53 / Cloud DNS / Cloud CDN | WAF | DDoS Shield | CloudFront   |   |
|  |  TLS 1.3 Termination | Anycast IP | GeoDNS Routing                   |   |
|  +----------------------------------------------------------------+------+   |
|                                                                   |          |
|  +--- Edge / API Gateway Layer -------------------------------------v-----+   |
|  |  API Gateway (REST/WebSocket) | Cloud Load Balancer (L7 ALB, L4 NLB)  |   |
|  |  AuthN/AuthZ (OAuth2.1, OIDC, mTLS) | Rate Limiting | Circuit Breaker|   |
|  |  Schema Validation | Request/Response Transformation                  |   |
|  +----------------------------------------------------------------+------+   |
|                                                                   |          |
|  +--- Service Mesh / Application Layer ----------------------------v-----+   |
|  |  +----------+  +----------+  +----------+  +----------+              |   |
|  |  | Service  |  | Service  |  | Service  |  | Service  |   Sidecar    |   |
|  |  | A (Pod)  |◄-+ B (Pod)  |◄-+ C (Pod)  |◄-+ D (Pod)  |   Proxy      |   |
|  |  | Envoy    |  | Envoy    |  | Envoy    |  | Envoy    |  (Istio)     |   |
|  |  +----+-----+  +----+-----+  +----+-----+  +----+-----+              |   |
|  |       +------+-------+------+------+-------+------+                   |   |
|  |              |   mTLS | Retry | Timeout | TraceID                     |   |
|  |              v              v              v                            |   |
|  |  +--------------+  +--------------+  +--------------+                |   |
|  |  | ConfigMap/   |  | Secret Mgr   |  | Service      |  Control Plane|   |
|  |  | Vault        |  | (KMS/HSM)    |  | Discovery    |  (istiod)     |   |
|  |  +--------------+  +--------------+  +--------------+                |   |
|  +---------------------------------------------------------------------+   |
|                                                                              |
|  +--- Data Layer -------------------------------------------------------+    |
|  |  OLTP: Aurora / Cloud SQL / CosmosDB / Spanner (Strong/Global)       |    |
|  |  OLAP: Redshift / BigQuery / Synapse (Columnar, Decoupled Storage)  |    |
|  |  Cache: ElastiCache (Redis) / Memorystore | DAX | CDN Edge Cache     |    |
|  |  Object: S3 / GCS / Blob (11 9's Durability) | Lifecycle Policy     |    |
|  |  Queue: SQS/SNS, Pub/Sub, EventBridge, Service Bus, Kafka (MSK)     |    |
|  +---------------------------------------------------------------------+    |
|                                                                              |
|  +--- Platform / Observability / Security Plane ------------------------+    |
|  |  Prometheus + Grafana | Loki/EFK | Jaeger/Tempo | OpenTelemetry      |    |
|  |  Terraform/Pulumi/Crossplane | ArgoCD/Flux | Helm/Kustomize         |    |
|  |  IAM (RBAC+ABAC) | KMS | GuardDuty | Security Hub | CloudTrail      |    |
|  |  FinOps: CUR, Cost Explorer, Kubecost, Vantage                       |    |
|  +---------------------------------------------------------------------+    |
+------------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 추상화** | 워크로드 실행 환경, 추상화 수준별 관리 책임 분배 | EC2/Compute Engine(IaaS, OS/패치 직접 관리) / EKS/AKS/GKE(CaaS, K8s API로 컨테이너 오케스트레이션, Control Plane은 Managed) / Fargate/Cloud Run(Serverless CaaS, 노드도 Managed) / Lambda/Functions(FaaS, 콜드스타트 100~800ms, 15분 타임아웃) |
| **네트워크 토폴로지** | VPC/Sub-net 격리, Cross-AZ/Region 트래픽 라우팅, Zero Trust 구현 | VPC/Virtual Network/Cloud VPC(10.0.0.0/16 RFC1918) -> Subnet 분할(Public/Private/Database/Isolated) -> Route Table -> NAT Gateway/Instance -> Internet
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 578 / 800

<- **이전**: [577. 클라우드 아키텍처 핵심 토픽 577번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/577_cloud_architecture_core_topic_577_exam_summar/)
**다음**: [579. 클라우드 아키텍처 핵심 토픽 579번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/579_cloud_architecture_core_topic_579_exam_summar/) ->

---
