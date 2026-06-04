---
title: "652. 클라우드 아키텍처 핵심 토픽 652번 시험 요약 (Cloud Architecture Core Topic 652 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 온프레미스 중심의 수직 확장(Scale-Up) 패러다임을 API 기반의 수평 확장(Scale-Out), 셀프서비스 프로비저닝, 사용량 기반 과금(Pay-per-Use) 모델로 전환하는 것으로, AWS Well-Architected Framework의 6대 원칙(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화, 지속가능성)을 기준으로 설계한다.
> 2. **가치**: CapEx에서 OpEx로의 재무 구조 전환, 탄력성(Elasticity)을 통한 평균 30~70% 인프라 비용 절감, 글로벌 리전 기반의 멀티 리전 재해복구(DR) RTO 1분/RPO 수초 달성, Kubernetes·Service Mesh·IaC(Terraform/Ansible) 기반의 GitOps 자동화로 배포 리드타임 90% 단축이 가능하다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) 회피를 위한 멀티/하이브리드 전략, EKS vs GKE vs AKS 컨테이너 오케스트레이션 선정, 데이터 주권(GDPR, 개인정보보호법)·클라우드 액트(EU Data Act)·국내 클라우드 컴퓨팅 발전법 준수, CAP theorem·PACELC theorem 기반 일관성/가용성/분할내성 트레이드오프, FinOps 기반의 Reserved/On-Demand/Spot 인스턴스 비율 최적화가 핵심 의사결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스 데이터센터는 CAPEX(자본적 지출) 기반으로 3~5년 주기의 HW 라이프사이클, 30~40%의 평균 서버 가용률, 그리고 수직적 확장의 물리적 한계(TB급 메모리, 128Core CPU 한계)를 갖는다. 2006년 AWS EC2의 출시 이후 클라우드 컴퓨팅은 NIST SP 800-145 정의에 따라 "네트워크, 서버, 스토리지, 애플리케이션, 서비스를 포함한 구성 가능한 컴퓨팅 자원의 공유 풀에 어디서나 편리하고 주문형으로 네트워크 접근을 가능하게 하는 모델"로 진화했다. 클라우드 아키텍처는 이러한 자원 풀 위에서 **탄력성(Elasticity)**, **확장성(Scalability)**, **고가용성(High Availability)**, **내결함성(Fault Tolerance)**을 보장하기 위해 제어 평면(Control Plane)과 데이터 평면(Data Plane)을 분리하고, 선언적 API(Declarative API)와 불변 인프라(Immutable Infrastructure) 원칙을 적용한다.

```text
[클라우드 컴퓨팅 참조 모델 (NIST SP 800-145 기반)]

+-------------------------------------------------------------+
|              클라우드 컴퓨팅 5대 필수 특성                    |
+-------------------------------------------------------------+
| ① 주문형 셀프서비스 (On-demand Self-service)                 |
| ② 광대역 네트워크 접근 (Broad Network Access)                |
| ③ 자원 풀링 (Resource Pooling) -> Multi-tenancy              |
| ④ 신속한 탄력성 (Rapid Elasticity)                          |
| ⑤ 측정 가능한 서비스 (Measured Service) -> Pay-per-Use       |
+-------------------------------------------------------------+
                          |
        +-----------------+-----------------+
        v                 v                 v
  +----------+      +----------+      +----------+
  | 서비스   |      | 배포     |      | 관리     |
  | 모델     |      | 모델     |      | 모델     |
  +----------+      +----------+      +----------+
        |                 |                 |
   +----+----+       +----+----+       +----+----+
   |IaaS     |       |Public   |       |Managed  |
   |PaaS     |       |Private  |       |Self     |
   |SaaS     |       |Hybrid   |       |Unmanaged|
   |FaaS     |       |Multi    |       |         |
   +---------+       +---------+       +---------+
```

클라우드 도입은 단순한 인프라 이전이 아닌 **운영 모델의 전환**이다. 이를 6R 마이그레이션 전략(Rehost, Replatform, Repurchase, Refactor, Retire, Retain)으로 분류하고, AWS CAF(Cloud Adoption Framework)의 6가지 관점(Business, People, Governance, Platform, Security, Operations) 및 Azure Cloud Adoption Framework의 8단계 프로세스(Strategy, Plan, Ready, Adopt, Govern, Manage, Govern, Organize)를 통해 체계적으로 추진한다. Gartner Magic Quadrant 2024 기준 AWS(Leader, 18% 시장점유율), Azure(Leader, 23%), GCP(Leader, 10%)가 IaaS+PaaS 시장의 51%를 점유하고 있으며, 국내는 네이버 클라우드(NAVER Cloud), KT 클라우드, NHN 클라우드, GS(Goodie) 등이 공공·금융 클라우드 시장을 주도하고 있다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"호텔式的 숙박 시스템"**과 같다. 뷔페(요청 시 자원 할당)에서 원하는 만큼만(탄력성) 먹고, 체크인/체크아웃(API 기반 프로비저닝)이 자유롭고, 다른 손님과 룸을 공유(멀티테넌시)하지만 계산서(미터링)는 내 사용량만큼만 나온다. 고정 식당 임대(On-Premise) 대비 30% 식재료 낭비를 줄일 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **다층 방어(Defense in Depth)**, **단일 장애점(SPOF) 제거**, **느슨한 결합(Loose Coupling)**, **불변 인프라**, **관측 가능성(Observability)**의 5대 설계 원리로 구성된다. 기술 스택은 크게 **인프라 계층**(가상화/KVM, Hyper-V, AWS Nitro), **플랫폼 계층**(Kubernetes, Service Mesh, API Gateway), **애플리케이션 계층**(12-Factor App, Microservices, Serverless), **데이터 계층**(S3, DynamoDB, Aurora, BigQuery, Snowflake), **거버넌스 계층**(IaC, Policy as Code, FinOps) 으로 나뉜다.

```text
[클라우드 네이티브 아키텍처 참조 모델 (CNCF Landscape 기반)]

+-----------------------------------------------------------------+
| Layer 5: Observability & Governance                             |
|  +--------------+ +--------------+ +--------------+            |
|  | Prometheus   | | Grafana      | | OpenTelemetry|            |
|  | Loki/EFK     | | Datadog      | | OPA/Kyverno  |            |
|  +--------------+ +--------------+ +--------------+            |
+-----------------------------------------------------------------+
| Layer 4: Application Runtime                                     |
|  +--------------+ +--------------+ +--------------+            |
|  | 12-Factor App| | Microservices| | Serverless   |            |
|  | (Spring Boot)| | (gRPC/REST)  | | (Lambda/Fn)  |            |
|  +--------------+ +--------------+ +--------------+            |
+-----------------------------------------------------------------+
| Layer 3: Orchestration & Service Mesh                           |
|  +--------------+ +--------------+ +--------------+            |
|  | Kubernetes   | | Istio/Linkerd| | ArgoCD/Flux  |            |
|  | (EKS/GKE/AKS)| | Envoy Proxy  | | (GitOps)     |            |
|  +--------------+ +--------------+ +--------------+            |
+-----------------------------------------------------------------+
| Layer 2: Container & CI/CD                                       |
|  +--------------+ +--------------+ +--------------+            |
|  | Docker/CRI-O | | Jenkins/Argo | | Harbor/CRR   |            |
|  | Buildah       | | GitHub Actions| | Sigstore/Cosign|         |
|  +--------------+ +--------------+ +--------------+            |
+-----------------------------------------------------------------+
| Layer 1: Infrastructure (IaC)                                    |
|  +--------------+ +--------------+ +--------------+            |
|  | Terraform    | | Pulumi/CDK   | | Ansible      |            |
|  | (HCL)        | | (TypeScript) | | (YAML)       |            |
|  +--------------+ +--------------+ +--------------+            |
+-----------------------------------------------------------------+
| Layer 0: Hardware / Hypervisor (AWS Nitro / Azure Hyper-V)     |
|  +--------------+ +--------------+ +--------------+            |
|  | x86_64/ARM64 | | SmartNIC/DPU | | Confidential |            |
|  | Graviton3    | | Nitro Enclave| | Computing(SEV)|            |
|  +--------------+ +--------------+ +--------------+            |
+-----------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway / Ingress** | 외부 트래픽 진입점, 인증/인가, 라우팅, Rate Limiting, Circuit Breaker | AWS API Gateway(10K RPS), Kong(OpenResty + Lua), Envoy xDS, Spring Cloud Gateway(Reactive WebFlux), WebFlux의 Netty 기반 Event Loop 모델로 10K+ 동시 커넥션 처리 |
| **Service Mesh (Control + Data Plane)** | 서비스 간 mTLS, 트래픽 관리(Canary 5%->25%->100%), 분산 추적 | Istio(Envoy sidecar), Linkerd(Linkerd2-proxy Rust), Consul Connect. Sidecar 패턴으로 Application code 수정 없이 정책 주입, Ambient Mesh(eBPF 기반)로 Sidecar 제거 추세 |
| **Container Orchestrator** | 컨테이너 스케줄링, 셀프힐링, 오토스케일링(HPA/VPA/Cluster Autoscaler), 선언적 상태 관리 | Kubernetes 1.30+(CRI, CNI, CSI 통합), Reconciliation Loop(현재 상태->원하는 상태), PDB(Pod Disruption Budget) 50% 이상 보장, Karpenter로 Just-in-Time 노드 프로비저닝(60초 vs 4분) |
| **Object Storage / Data Lake** | 11 9s 내구성, 무제한 확장, S3 호환 API, 계층화 스토리지 | AWS S3(Standard->IA->Glacier Instant->Glacier Deep Archive), Ceph RGW, MinIO. 수명주기 정책으로 30일 후 IA, 90일 후 Glacier 자동 이동 -> 스토리지 비용 80% 절감 |
| **Serverless / FaaS** | 이벤트 기반 실행, 콜드스타트 100~300ms, 자동 스케일링 0->N | AWS Lambda(10GB 메모리, 15분 타임아웃, 1000 동시성), Azure Functions(Durable Functions로 상태 관리), GCP Cloud Run(Knative 기반, 80만 req/sec 사례) |
| **Managed Database (RDBS + NoSQL)** | ACID 보장, 자동 백업, PITR, Read Replica 다중화 | RDS Aurora(MySQL/PostgreSQL 호환, 6-way 복제, 128TB), DynamoDB(GSI/LSI, DAX 인메모리 캐시), Cosmos DB(Multi-Master, 5가지 일관성 모델), Spanner(Globally Distributed Strongly Consistent) |
| **IaC (Infrastructure as Code)** | 인프라의 버전관리, 코드리뷰, 재현성, Policy as Code | Terraform(상태파일 S3+DynamoDB Lock), Atlantis(Pull Request 기반 Plan/Apply), Open Policy Agent(OPA Rego), HashiCorp Sentinel. Drift Detection으로 Configuration 일관성 유지 |
| **Cloud-Native Security** | Zero Trust, CSPM, CWPP, CIEM, SBOM 관리 | SPIFFE/SPIRE(워크로드 identity), Falco(런타임 침입탐지, eBPF), Trivy(컨테이너 이미지 스캔), AWS IAM Roles Anywhere, Snyk, Aqua Security, Palo Alto Prisma Cloud |

**핵심 알고리즘 및 의사결정 원리:**

- **CAP Theorem**: 일관성(C), 가용성(A), 분할내성(P) 중 최대 2개만 보장. DynamoDB는 AP(Eventually Consistent 기본, Strongly Consistent 옵션), Cosmos DB는 5단계 Tunable Consistency, Spanner는 CP + 글로벌 강일관성(Atomic Clocks + GPS + TrueTime API)
- **PACELC Theorem**: 네트워크 분할(P) 시 A/E 트레이드오프, 정상(Else) 시 Latency/Consistency 트레이드오프. DynamoDB는 PA/EL, BigTable은 PA/EC, MongoDB는 PC/EL
- **Hashing for Sharding**: Consistent Hashing(Re-hashing 최소화), Virtual Nodes로 Hot Spot 방지, Rendezvous Hashing(HRW)
- **Replication Factor**: RF=3 + Quorum Write(W=2)/Read(R=2) -> R+W>N 강일관성. Cassandra는 Eventual Consistency + Hinted Handoff
- **Auto Scaling**: Target Tracking Scaling(CPU 70% 기준), Step Scaling(임계값 기반), Predictive Scaling(ML 기반 14일 패턴 학습), Scheduled Scaling(배치 작업)
- **Circuit Breaker**: Closed->Open(임계치 초과, fail fast)->Half-Open(일부 요청 허용)->Closed(복구). Resilience4j, Hystrix(현재 maintenance), Istio Outlier Detection

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 계층 구조는 **"요리 프랜차이즈의 본사-매장 시스템"**과 같다. 본사(IaC/Terraform)가 레시피를 정해 매장(Region/AZ)에 배포하고, 매장 관리자(Kubernetes)가 셰프(Pod)들을 배치·교체하며, 서빙(Service Mesh)은 주문과 배달을 조율하고, 손님의 불만(Observability)을 실시간으로 수집해 본사에 피드백한다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처 설계 시 반드시 비교해야 할 핵심 개념들과 다른 아키텍처 패턴/기술과의 연결 관계를 정리한다.

| 구분 | On-Premise (전통 데이터센터) | Public Cloud (AWS/Azure/GCP) | Private Cloud (OpenStack/VMware) | Hybrid / Multi-Cloud |
| :--- | :--- | :--- | :--- | :--- |
| **투자 방식** | CapEx (HW 사전 구매, 3~5년 감가상각) | OpEx (Pay-per-Use, 초단위 과금) | CapEx + OpEx (HW 투자 + 라이선스) | CapEx(Private) + OpEx(Public) |
| **확장성** | 수직 확장 한계 (8Socket, 6TB RAM) | 수평 확장 무제한, Auto Scaling | 수직+수평, 가상화 클러스터 확장 | 버스팅(Bursting)
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 652 / 800

<- **이전**: [651. 클라우드 아키텍처 핵심 토픽 651번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/651_cloud_architecture_core_topic_651_exam_summar/)
**다음**: [653. 클라우드 아키텍처 핵심 토픽 653번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/653_cloud_architecture_core_topic_653_exam_summar/) ->

---
