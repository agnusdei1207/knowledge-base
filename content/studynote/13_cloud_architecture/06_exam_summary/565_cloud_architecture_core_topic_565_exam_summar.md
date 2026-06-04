---
title: "565. 클라우드 아키텍처 핵심 토픽 565번 시험 요약 (Cloud Architecture Core Topic 565 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST 참조모델(5대 핵심특성·3대 서비스모델·4개 배치모델)을 기반으로 **자원 추상화(Resource Pooling)·자동화(Orchestration)·탄력성(Elasticity)·API 셀프서비스**를 통해 CAP 정리의 트레이드오프를 분산 시스템 차원에서 재해석한 것이다. 핵심은 12-Factor App, MSA, Immutable Infrastructure, GitOps를 결합한 **클라우드 네이티브 4원칙**이다.
> 2. **가치**: McKinsey & Gartner 2024 보고 기준 CapEx->OpEx 전환으로 **TCO 30~72% 절감**, 배포 리드타임 **일->분 단위**, 가용성 **99.95~99.99% (연 4.38h~52.56m 다운타임)**, Auto-Scaling으로 Peak 시점 **300~1,000% 트래픽 흡수**(Black Friday, 신년 첫날 등).
> 3. **판단 포인트**: (a) **워크로드의 상태성**(Stateful: RDS, StatefulSet vs Stateless: Lambda, Deployment), (b) **데이터 중력(Data Gravity)** — 데이터를 옮기지 않고 컴퓨팅을 가까이 끌어오는 전략, (c) **종속성 vs 이식성**(Vendor Lock-in 위험도: IaaS 20% < PaaS 40% < SaaS 70%), (d) **보안 경계**(공용망/사설망/VPC Peering/Transit GW), (e) **비용 모델**(On-Demand vs Reserved vs Savings Plan vs Spot).

---

## Ⅰ. 개요 및 필요성

클라우드 컴퓨팅은 NIST SP 800-145(2011)에서 **"네트워크, 서버, 스토리지, 애플리케이션, 서비스 등 구성된 IT 자원의 공유 풀(shared pool)을 최소한의 관리 노력이나 서비스 제공자 상호작용으로 빠르게 제공·할당·해제할 수 있는 ubiquitous, convenient, on-demand network access 모델"** 로 정의된다. 이는 2006년 AWS S3·EC2 출시 이후 18년간 진화하여, 2024년 현재 전 세계 퍼블릭 클라우드 시장이 **약 6,790억 USD**(Gartner 2024Q4), 국내는 약 9.3조 원 규모로 성장했다.

기존 On-Premise 아키텍처는 **3-tier(Presentation-Logic-Data)** 의 수직 확장(Scale-Up) 중심, CAPEX 과다, 프로비저닝 수주 소요, 트래픽 변동성 대응 불가, 1개 IDC 장애 시 DR 복구 RTO 수시간~수일이라는 한계가 있었다. 코로나19(2020~) 이후 비대면 트래픽 폭증, K-PaaS, MSA 컨테이너 기반 배포 표준화, FinOps 성숙, 생성형 AI workloads의 GPU 수요 급증이 **클라우드 우선(Cloud-First) 전략** 을 필수가 되게 만들었다.

```text
+----------------------------------------------------------------+
|                Cloud Computing Reference Model                 |
|                (NIST SP 800-145 기반)                           |
|                                                                |
|   +----------------------------------------------------+       |
|   |    Cloud Consumer  <- SaaS 사용자 / 업무시스템       |       |
|   |         |  (HTTPS/API/Console/SDK)                 |       |
|   |         v                                          |       |
|   |   Service Broker / API Gateway (예: AWS API GW)   |       |
|   |   - 인증/인가(IAM, OAuth2, OIDC)                   |       |
|   |   - 요금(Usage Metering) / 카탈로그                 |       |
|   |         |                                          |       |
|   |         v                                          |       |
|   |   +------------ Cloud Service Layer ------------+  |       |
|   |   | IaaS  : EC2, EBS, VPC, S3 (저수준 제어)     |  |       |
|   |   | PaaS  : RDS, EKS, Elastic Beanstalk        |  |       |
|   |   | SaaS  : Office365, Salesforce, SAP on AWS   |  |       |
|   |   | FaaS  : Lambda, Cloud Functions (이벤트형)  |  |       |
|   |   +---------------------------------------------+  |       |
|   |         |                                          |       |
|   |         v                                          |       |
|   |   Resource Abstraction & Control Layer            |       |
|   |   - Hypervisor (Xen, KVM, Hyper-V) / MicroVM(Firecracker)|
|   |   - Container Runtime (containerd, CRI-O)         |       |
|   |   - SDN Controller / Storage Virtualization       |       |
|   |         |                                          |       |
|   |         v                                          |       |
|   |   Physical Layer                                  |       |
|   |   - DC(Power/Cooling), 서버(CPU/Mem/NIC), NVMe,   |       |
|   |     ToR-Leaf-Spine 패브릭                          |       |
|   +----------------------------------------------------+       |
+----------------------------------------------------------------+
```

기존 **소유 모델(CapEx) -> 사용 모델(OpEx)** 전환은 단순 비용 회계 변경이 아니라, **용량 계획(Capacity Planning)·장애 대응(DR)·조직(DevOps vs 전통 SI)** 까지 패러다임을 전환시키는 것이다. AWS Well-Architected Framework 6대 기둥(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속가능성)이 이를 평가 기준으로 자리 잡았다.

- **📢 섹션 요약 비유**: 온프레미스 데이터센터가 **개인 차량 소유**(보험·주차·정비 직접 부담)라면, 클라우드는 **카셰어링 + 렌터카 + 택시 앱** 을 필요에 따라 골라 쓰는 것이다. 출퇴근(SaaS)·장거리(IaaS)·반나절 업무(FaaS)에 따라 차량 종류가 달라진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **Control Plane(제어 평면)·Data Plane(데이터 평면)·Management Plane(관리 평면)·Observability Plane(관측 평면)** 의 4개 평면으로 구성된다. AWS를 예로 들면 Control Plane는 `aws.amazon.com` 콘솔, API 호출, IAM 정책, CloudFormation 스택을 의미하고, Data Plane는 실제 EC2 인스턴스, S3 버킷, VPC 내부 트래픽이 흐르는 영역이다.

### 핵심 동작 메커니즘 (12-Factor + MSA + IaC + GitOps)

```text
   Git Repo  --CI--->  Registry  --CD--->  Orchestrator (EKS/AKS)
   (소스)              (ECR/ACR)            |
       |                  |                 v
       |                  |            +---------+
       |                  |            | Pod/VM  | <- HPA/KEDA
       |                  |            | Sidecar |     (Auto-Scale)
       |                  |            +---------+
       |                  |                 |
       v                  v                 v
   Code Review <--- IaC(Terraform) --->  Service Mesh(Istio)
       |                                       |
       v                                       v
   Observability <------ mTLS, Circuit Breaker, Retry, Timeout
   (Prom/Grafana/
    Loki/Tempo)
       |
       v
   FinOps Dashboard (예: Kubecost, Vantage, CloudHealth)
```

### 4대 평면 상세 구성요소

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Control Plane** | API/콘솔/SDK/IAM 정책으로 리소스 선언·생성·삭제 | AWS API GW + IAM(ABAC/RBAC) + CloudFormation StackSets / GCP Anthos Config Mgmt / Azure ARM Template. 모든 변경은 **Declarative**(원하는 상태 선언)로 기술되어 Reconciliation Loop가 실행. |
| **Data Plane** | 실제 사용자 트래픽·데이터 패킷이 흐르는 영역 | VPC 내부의 ENI/IPv4, NLB/ALB(Application/Gateway LB), EBS gp3, S3 Multi-AZ, Aurora Writer/Reader 분리, Global Accelerator(Anycast IP). 일반적으로 **암호화(in-transit TLS 1.3, at-rest AES-256)** 필수. |
| **Management Plane** | 가시성·로깅·컴플라이언스 | CloudTrail(Config 변경), CloudWatch(지표), Config(규정 준수), GuardDuty(
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 565 / 800

<- **이전**: [564. 클라우드 아키텍처 핵심 토픽 564번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/564_cloud_architecture_core_topic_564_exam_summar/)
**다음**: [566. 클라우드 아키텍처 핵심 토픽 566번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/566_cloud_architecture_core_topic_566_exam_summar/) ->

---
