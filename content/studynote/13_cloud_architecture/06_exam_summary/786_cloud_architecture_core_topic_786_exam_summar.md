---
title: "786. 클라우드 아키텍처 핵심 토픽 786번 시험 요약 (Cloud Architecture Core Topic 786 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 AWS Well-Architected Framework의 6대 원칙(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화, 지속 가능성)을 기반으로, **컨트롤 플레인(Control Plane)**과 **데이터 플레인(Data Plane)**을 분리하여 API 기반 선언적 인프라(IaC: Terraform/OpenTofu/CloudFormation)와 GitOps를 통해 자원을 코드로 통제하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: CapEx에서 OpEx로의 전환(전형적 TCO 30~40% 절감), 탄력적 Auto Scaling을 통한 99.99% SLA 달성, Multi-AZ/Region 아키텍처로 RTO < 1분·RPO ≈ 0 구현, 글로벌 엣지(CloudFront/Azure CDN/Cloud CDN)를 통한 p99 지연시간 50ms 이하 보장.
> 3. **판단 포인트**: **Lift-and-Shift vs Replatform vs Refactor** 마이그레이션 전략, **Multi-Cloud vs Hybrid Cloud vs Single Cloud**의 거버넌스 복잡도, **Egress Lock-in 비용**(AWS -> 타 클라우드 시 GB당 $0.02~0.09), **Shared Responsibility Model** 경계에서의 보안 책임 소재, 12-factor app 기반 Stateless 워크로드 전환 여부.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스(On-Premise) 아키텍처는 **수직적 확장(Scale-Up)** 방식의 모놀리식(Monolithic) 구조로, 최대 트래픽 예측 기반의 과잉 프로비저닝(Over-provisioning) 때문에 평균 자원 활용률이 15~25%에 불과했다. 또한 CAPEX(Capital Expenditure) 중심의 HW 수명 주기(통상 5년 refresh)는 비즈니스 변화 속도(수 개월 단위)와 본질적 불일치를 야기했다.

클라우드 아키텍처는 이를 **수평적 확장(Scale-Out)**, **가상화/컨테이너화**, **API-Driven Provisioning**, **Pay-as-you-go** 모델로 전환한다. NIST SP 800-145는 클라우드를 5대 필수 특성(온디맨드 셀프서비스, 광범위한 네트워크 접근, 자원 풀링, 빠른 탄력성, 측정 가능한 서비스)과 3대 서비스 모델(IaaS/PaaS/SaaS), 4배출 모델(Public/Private/Hybrid/Community)로 정의한다.

```text
+----------------------------------------------------------------------+
|                  클라우드 아키텍처 패러다임 전환 흐름                  |
+----------------------------------------------------------------------+
|                                                                      |
|  [전통적 On-Premise]                  [Cloud-Native Era]              |
|  +-----------------+                 +---------------------+         |
|  |  Monolithic App | ---------------►| Microservices(MSA)  |         |
|  |  + RDBMS        |   Refactor      | + Polyglot DB       |         |
|  |  + 물리 서버     |                 | + Container/K8s     |         |
|  +-----------------+                 +---------------------+         |
|         |                                      |                     |
|  수직확장(Scale-Up)                    수평확장(Scale-Out)            |
|  수동 운영(Manual Ops)                GitOps/AIOps                   |
|  5년 Refresh Cycle                    Immutable Infra + CI/CD        |
|  CAPEX 중심                          OPEX + FinOps                   |
|  평균 가용성 99.5%                   SLA 99.99% (Multi-AZ)           |
|  TCO 3년 기준 100%                   동일 워크로드 60~70%            |
|                                                                      |
+----------------------------------------------------------------------+

        [Cloud Computing 계층 구조]
        +---------------------------------+
        |   SaaS  (Slack, Notion, SaaS)   | <- Application Layer
        +---------------------------------+
        |   PaaS  (EKS, App Service)      | <- Platform Layer
        +---------------------------------+
        |   FaaS  (Lambda, Cloud Func)    | <- Function Layer
        +---------------------------------+
        |   IaaS  (EC2, VM, VPC)          | <- Infrastructure Layer
        +---------------------------------+
        |   물리  (Region/AZ/Edge DC)     | <- Physical Layer
        +---------------------------------+
```

**왜 필요한가?**
- **비즈니스 민첩성(Time-to-Market)**: 신규 인프라 배포가 3개월 -> 5분(ClickOps) 또는 1분(IaC)
- **글로벌 확장성**: 30+ 리전, 400+ POP(Points of Presence) 엣지 로케이션을 즉시 활용
- **탄력성**: 트래픽 10배 급증 시 Auto Scaling Group(ASG) + Warm Pool + Predictive Scaling으로 대응
- **DR(재해복구)**: Pilot Light / Warm Stand-by / Multi-Site Active-Active 패턴으로 RTO 분 단위 달성

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **수도요금처럼** 전력량을 사용한 만큼만 지불하는 *Pay-as-you-go*의 '전기 회로'로, 한 번 큰 발전소를 짓는 대신(온프레미스) 필요할 때마다 전기를 끌어다 쓰는(Electric Grid) 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **API 기반의 선언적(Declarative) 인프라**와 **제어 루프(Control Loop)**를 통한 지속적 조화(Reconciliation)이다. 사용자가 *"원하는 상태(Desired State)"*를 YAML/JSON으로 선언하면, 컨트롤 플레인이 실제 상태(Actual State)와 비교·조정한다.

```text
+------------------------------------------------------------------------+
|           Cloud-Native 4계층 + Cross-Cutting Concerns                  |
+------------------------------------------------------------------------+

  [사용자] --► [Route 53 / Cloud DNS] --► [CloudFront/Cloud CDN (Edge)]
                                                    |
                                          +---------v----------+
                                          |   WAF + Shield    |  <- L7 보안
                                          |   (Layer 7 보호)   |
                                          +---------+----------+
                                                    |
                              +---------------------v---------------------+
                              |  Multi-AZ Application Tier (Stateless)     |
                              |  +-------+  +-------+  +-------+          |
                              |  |ALB/NLB|  |ALB/NLB|  |ALB/NLB|          |
                              |  |App1   |  |App2   |  |App3   |          |
                              |  |EKS Pod|  |ECS    |  |Lambda |          |
                              |  +-------+  +-------+  +-------+          |
                              +---------------------+---------------------+
                                                    |
                              +---------------------v---------------------+
                              |  Data Tier (Stateful + Polyglot)           |
                              |  +--------+ +--------+ +--------+         |
                              |  |Aurora  | |DynamoDB| |Redis   |         |
                              |  |(RDBMS) | |(NoSQL) | |(Cache) |         |
                              |  +--------+ +--------+ +--------+         |
                              |  Read Replica + Multi-AZ + Backup          |
                              +---------------------+---------------------+
                                                    |
                              +---------------------v---------------------+
                              | Cross-Cutting:                           |
                              | • IAM + KMS + Secrets Manager             |
                              | • CloudWatch/Prometheus + Grafana         |
                              | • VPC FlowLog + CloudTrail + Config       |
                              | • Service Mesh (Istio/App Mesh)           |
                              +-------------------------------------------+
```

### 클라우드 아키텍처 6대 Well-Architected 핵심 원칙

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① 운영 우수성(Operational Excellence)** | 모니터링·자동화·지속적 개선 | CloudWatch + X-Ray, Runbook 자동화, IaC 100% 적용, **SLO/SLI/SLA** 기반 사고 관리, **Blameless Postmortem** 문화, **GitOps** (ArgoCD/FluxCD) |
| **② 보안(Security)** | CIA + 비거부성 + 최소권한 | **Zero Trust**(BeyondCorp), IAM 정책(SCP/RBAC/ABAC), KMS/HSM, **Shared Responsibility Model**, CSPM(Cloud Security Posture Mgmt), CWPP, Secrets Manager/Vault |
| **③ 안정성(Reliability)** | 장애 복구·자동 치유 | **Multi-AZ/Region**, Auto Scaling + Health Check, Circuit Breaker(Resilience4j), Chaos Engineering(Litmus/Chaos Monkey), **RTO/RPO** 정의, Backup 3-2-1 규칙 |
| **④ 성능 효율성(Performance Efficiency)** | 컴퓨팅 자원의 최적 활용 | **Right-Sizing**, Auto Scaling 정책(Target Tracking/Step/Predictive), Caching(ElastiCache/CloudFront), gp3/EBS 최적화, Graviton3/ARM64 전환, **FinOps** |
| **⑤ 비용 최적화(Cost Optimization)** | 클라우드 지출의 가시성·최소화 | **RI(Reserved Instance)/Savings Plans** 60~72% 할인, Spot Instance 90% 할인, S3 Intelligent-Tiering, Cost Anomaly Detection, **태그 기반 Showback/Chargeback** |
| **⑥ 지속 가능성(Sustainability)** | 탄소 발자국 최소화 | **Carbon Footprint Dashboard**, 리전 선택(탄소 집약도 낮은 리전 우선), Graviton/AMD EPYC(에너지 효율 60%^), 사용하지 않는 자원 정리(Lambda의 idle 상태) |

### 핵심 동작 메커니즘: **선언형 API + Reconciliation Loop**

```text
   [사용자 선언]                  [클라우드 내부]                  [실제 상태]
       |                              |                              |
       | desired_state.yaml           |      +-------------+          |
       v                              |      | Control     |          |
   +----------+  PUT/POST  +----------v-----► Plane     |          |
   |Terraform | ---------► |  API Gateway  |  (Reconcile)|          |
   | OpenTofu |            |  + Auth (IAM) |      |      |          |
   +----------+            +--------------+      |      |          |
       ^                                     Compare  Apply  +-----v-----+
       |                                     Diff      |      | Actual     |
       | state_drift_detected -------------------+       | State      |
       |                                                 +------------+
       | Reconcile Loop(3~30초 주기, K8s는 5초 주기)
```

**핵심 알고리즘/파라미터:**
- **Consensus**: 클라우드 컨트롤 플레인은 **Raft/Paxos** 알고리즘으로 분산 합의(예: 3개 AZ에 분산된 컨트롤 노드 중 과반수 동의)
- **Consistency Model**: DynamoDB는 **Tunable Consistency**(Eventually Consistent vs Strongly Consistent), Aurora는 **Quorum 기반 6-Replica 복제(3-AZ x 2)**
- **수학적 제약**: CAP Theorem — Partition Tolerance는 필수, **CP vs AP** 트레이드오프 (예: DynamoDB는 AP 기본, RDBMS는 CP)
- **Auto Scaling 공식**: `Desired Capacity = max( ceil(CurrentLoad/TargetMetric), MinSize )`  단, HPA의 경우 `desiredReplicas = currentReplicas × (currentMetricValue / targetMetricValue)`

- **📢 섹션 요약 비유**: 선언형 API + Reconciliation Loop는 마치 **보온병 자동 온도조절기**와 같다. "물을 70도로 유지하라"고 설정하면(Desired State), 센서가 현재 온도(Actual State)를 재고 히터를 켜거나 끄는 것(Reconcile)을 끊임없이 반복한다.

---

## Ⅲ. 비교 및 연결

### A. 클라우드 서비스 모델 비교

| 구분 | IaaS (Infrastructure-as-a-Service) | PaaS (Platform-as-a-Service) | SaaS (Software-as-a-Service) | FaaS (Function-as-a-Service) |
| :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | OS·미들웨어부터 직접 관리 | 런타임·미들웨어·OS 자동 관리 | 애플리케이션까지 제공 | 코드만 업로드, 나머지 전부 |
| **대표 서비스** | EC2, Azure VM, Compute Engine | Elastic Beanstalk, App Service, App Engine | Microsoft 365, Salesforce, Slack | Lambda, Cloud Functions, Azure Functions |
| **확장성** | 수동/스크립트 기반 | 설정 기반 Auto Scale | 자동 (사용자 모름) | 자동 (0->N 이벤트 기반 Cold Start) |
| **제어 수준** | 높음 (거의 모든 설정 가능) | 중간 (코드/데이터에 집중) | 낮음 (설정만) | 매우 낮음 (함수 단위) |
| **적합 워크로드** | 레거시 Lift&Shift, 커스텀 미들웨어 | 웹/API/마이크로서비스 | 일반 업무 (이메일/문서) | 이벤트 기반, 간헐적 워크로드 |
| **청구 단위** | Instance·Hour | Instance·Hour + 요청 수 | Per User/Month | GB-Second, 요청 수 (100만 건당 $0.20) |
| **대표 기술 스택** | Ansible, Chef, Puppet | Docker, K8s (PaaS형) | — | SAM, Serverless Framework, CDK |

### B. 클라우드 배포 모델 비교

| 구분 | Public Cloud | Private Cloud | Hybrid Cloud | Multi-Cloud |
| :--- | :--- | :--- | :--- | :--- |
| **소유권** | CSP (AWS/Azure/GCP) | 자체/전용 | On-Prem + Public | 2개 이상 Public |
| **도입 속도** | 즉시 (수 분) | 3~6개월 | 6~12개월 | 6~12개월 |
| **컴플라이언스** | CSP 책임 (FedRAMP, ISO 27001) | 자체 통제 | 데이터 주권 문제 해결 | 벤더 종속 회피 |
| **TCO** | 가장 낮음 (규모의 경제) | 높음 | 중간 | 가장 복잡 (Egress 비용) |
| **핵심 사용 사례** | 신사업 PoC, 글로벌 서비스 | 금융/공공/제조 규제 | 데이터 주권 + 클라우드 민첩성 | **DR 전용 2nd CSP** + 워크로드별 최적 |
| **네트워크** | Internet (VPN/Direct Connect) | 전용선 (On-Prem) | **Direct Connect / ExpressRoute** | **Interconnect + Transit Gateway** |
| **거버넌스** | 단일 CSP 콘솔 | 자체 IAM/SSO | **단일 ID 페더레이션** (Azure AD/Okta) | **Cloud Center of Excellence(CCoE)** 필수 |

### C. 클라우드 아키텍처 ↔ 다른 시스템 레이어 통합

```text
+------------------------------------------------------------------+
| [프레젠테이션 계층]  S3+CloudFront, SPA (React/Vue/Angular)       |
|         |                                                        |
| [API 게이트웨이]   API Gateway, Kong, Apigee -> OAuth 2.0 + JWT   |
|         |                                                        |
| [서비스 메시]      Istio/Linkerd/Consul Connect -> mTLS, Traffic Mgmt
|         |                                                        |
| [오케스트레이션]   Kubernetes(EKS/AKS/GKE) + Helm/ArgoCD + Service Mesh
|         |                                                        |
| [컨테이너 런타임]  Docker, containerd, CRI-O, gVisor (보안 샌드박스)
|         |                                                        |
| [클라우드 인프라]  EC2/VM, VPC/Subnet/Security Group, EBS/
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 786 / 800

<- **이전**: [785. 클라우드 아키텍처 핵심 토픽 785번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/785_cloud_architecture_core_topic_785_exam_summar/)
**다음**: [787. 클라우드 아키텍처 핵심 토픽 787번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/787_cloud_architecture_core_topic_787_exam_summar/) ->

---
