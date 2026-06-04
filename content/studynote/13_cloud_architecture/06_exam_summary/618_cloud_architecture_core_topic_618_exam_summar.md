---
title: "618. 클라우드 아키텍처 핵심 토픽 618번 시험 요약 (Cloud Architecture Core Topic 618 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 온프레미스 대비 CapEx->OpEx 전환, API 기반의 선언적 인프라(Declarative Infrastructure), 셀프서비스 프로비저닝, 탄력적 확장(Elastic Scalability)을 핵심으로 하며, IaaS/PaaS/SaaS/CaaS/FaaS의 책임공유모델(Shared Responsibility Model)과 12-Factor App, Cloud-Native, MSA 패턴을 결합한 설계 패러다임입니다.
> 2. **가치**: AWS Well-Architected Framework 5대 원칙(운영 우수성, 보안, 안정성, 성능효율, 비용최적화) 기반 설계 시, 인프라 비용 30~50% 절감, 배포 주기 주 1회->일 수십 회, Auto Scaling을 통한 트래픽 피크 대응력 10배 이상, MTTR 80% 단축 등 정량적 효과를 달성합니다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) 회피를 위한 Multi/Hybrid Cloud 전략, Stateless/Stateful 워크로드 분리, CAP Theorem 하의 일관성·가용성 트레이드오프, FinOps 기반 비용 거버넌스, Zero Trust 보안모델, IaC(Infrastructure as Code) 적용 범위, EKS vs AKS vs GKE 컨테이너 오케스트레이션 선택 기준이 핵심 의사결정 포인트입니다.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스(On-Premise) 아키텍처는 2000년대 이후 폭증하는 트래픽, 비정형 데이터(비정형 데이터는 전체 데이터의 80% 이상), BMT(Business Model Transformation) 가속화에 대응하지 못했습니다. 특히 3-tier 웹 아키텍처(웹서버-WAS-DB)의 수직적 확장(Scale-Up)은 HW 비용의 한계, CAPEX(Capital Expenditure) 과다, 용량 계획의 부정확성으로 인한 자원 낭비라는 구조적 한계를 노출시켰습니다. 2006년 AWS EC2 출시 이후 IaaS를 시작으로, 2010년대 PaaS(Heroku, App Engine), 2014년 Docker, 2015년 Kubernetes, 2019년 Lambda·Cloud Run 등 Serverless로 진화하며, **클라우드 네이티브(Cloud-Native)** 패러다임이 정착되었습니다.

CNCF(Cloud Native Computing Foundation)의 정의에 따르면, 클라우드 네이티브는 **컨테이너, 서비스 메시, 마이크로서비스, 불변 인프라(Immutable Infrastructure), 선언적 API(Declarative API)** 를 활용하여 "느슨하게 결합되고, 회복탄력적이며, 관리하기 쉬우며, 관측 가능한(Observable)" 시스템을 구축하는 접근법입니다. 한국 공공부문은 2023년까지 클라우드 우선 정책(Cloud First Policy)을 추진하고, 금융권은 금융감독원의 클라우드 컴퓨팅 이용 가이드(2020.12)에 따라 안전성 심의 후 도입하며, 일반 기업은 DX(Digital Transformation)의 핵심 인프라로 클라우드를 채택하고 있습니다.

```text
+----------------------------------------------------------------------+
|              온프레미스 -> 클라우드 아키텍처 진화 패러다임              |
+----------------------------------------------------------------------+
|                                                                      |
|  [1960~1980 Mainframe]                                               |
|       |  단일 대형 컴퓨터, MVS/JCL, 시분할 시스템(TS)                  |
|       v                                                              |
|  [1990s Client-Server]                                               |
|       |  2-Tier(Fat-Client + DB), Oracle Forms, PowerBuilder         |
|       v                                                              |
|  [2000s 3-Tier Web Architecture]                                     |
|       |  WebServer(Apache/IIS) -> WAS(Tomcat/WebLogic) -> DBMS(Oracle)|
|       |  문제: Scale-Up 한계, 라이선스 비용 폭증, 배포 복잡성          |
|       v                                                              |
|  [2010s Cloud IaaS/PaaS]                                             |
|       |  AWS EC2(2006), S3(2006), RDS(2009), Lambda(2014)           |
|       |  특징: API 기반 프로비저닝, Auto Scaling, Pay-as-you-go        |
|       v                                                              |
|  [2015~ Cloud-Native MSA]                                            |
|       |  Docker(2013->2014) -> Kubernetes(2015) -> Istio(2017)         |
|       |  12-Factor App, DevOps, GitOps(ArgoCD/Flux), CI/CD          |
|       v                                                              |
|  [2020~ Serverless & Edge]                                           |
|       |  FaaS(Lambda/Cloud Functions/Cloud Run), BaaS                |
|       |  Edge Computing(Cloudflare Workers, AWS Wavelength)          |
|       |  AI/ML Cloud(SageMaker, Vertex AI), WebAssembly(WASM)        |
|       v                                                              |
|  [2024+ AI-Native & Sovereign Cloud]                                 |
|       |  LLM Serving(vLLM, Triton), Vector DB(Pinecone, Weaviate)    |
|       |  Data Sovereignty, Confidential Computing(Intel SGX, SEV)    |
+----------------------------------------------------------------------+
```

기존 온프레미스 대비 클라우드의 핵심 차별점은 **"필요할 때, 필요한 만큼, 즉시 사용한 만큼 지불"** 한다는 것입니다. 서버 1대 프로비저닝에 On-Premise는 3~6개월(주문-도입-구성-테스트) 소요되지만, AWS EC2는 **API 호출 1회(예: `aws ec2 run-instances`)로 60초 내** 인스턴스가 생성됩니다. 또한 Auto Scaling Group(ASG) 정책에 따라 트래픽 피크 시 자동으로 인스턴스가 10분 내 100대에서 1,000대로 확장되며, 피크 종료 후 자동으로 축소되어 평균 30~70%의 비용 절감을 실현합니다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **"전기를 직접 발전하는 자가발전기에서, 콘센트에 꽂아 쓰는 한국전력 시스템으로의 전환"** 과 같습니다. 발전소(데이터센터) 건설 없이도 필요할 때 전기를 켜고, 사용량 만큼만 요금을 지불하며, 정전(장애)시 자동으로 백업 회로가 작동합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심 원리는 **5대 기본 특성(NIST SP 800-145)** 과 **AWS Well-Architected Framework 5대 Pillars**, 그리고 **12-Factor App 방법론**으로 체계화됩니다. 시스템은 크게 **프레젠테이션 계층 -> API Gateway/Edge -> 애플리케이션 계층(컨테이너/함수) -> 데이터 계층(관계형/NoSQL/캐시) -> 인프라 계층(IaC, 네트워킹, 보안)** 의 5계층으로 구성됩니다.

```text
+-------------------------------------------------------------------------+
|              클라우드 네이티브 레퍼런스 아키텍처 (Multi-AZ, Multi-Region) |
+-------------------------------------------------------------------------+
                            +------------------+
                            |   End-User/Client| (Web/Mobile/IoT)
                            +--------+---------+
                                     | HTTPS/TLS 1.3
                                     v
        +--------------------------------------------------------+
        |  Global Edge Layer                                     |
        |  +--------------+  +--------------+  +--------------+ |
        |  | CloudFront/  |  | Route 53     |  | WAF +       | |
        |  | Cloud CDN    |  | (Latency     |  | Shield      | |
        |  | (캐싱/압축)  |  |  Based RT)   |  | (DDoS 방어)  | |
        |  +------+-------+  +------+-------+  +------+-------+ |
        +---------╪----------------╪------------------╪---------+
                  |                |                  |
                  v                v                  v
        +------------------------------------------------------+
        |  Region: ap-northeast-2 (서울)                       |
        |  +------------------------------------------------+  |
        |  | AZ-a (가용영역 1)        AZ-c (가용영역 3)     |  |
        |  |                                                |  |
        |  |  +----------+         +----------+              |  |
        |  |  | ALB/NLB  |◄-------►| ALB/NLB  |              |  |
        |  |  +----+-----+         +----+-----+              |  |
        |  |       |  Health Check(5s)  |                    |  |
        |  |       v                    v                    |  |
        |  |  +----------------------------------+           |  |
        |  |  |  EKS/AKS/GKE (Kubernetes)        |           |  |
        |  |  |  +---------+  +---------+       |           |  |
        |  |  |  | Pod/Pod |  | Pod/Pod |  ...  |           |  |
        |  |  |  | Service |  | Service |       |           |  |
        |  |  |  | Account |  | Account |       |           |  |
        |  |  |  +----+----+  +----+----+       |           |  |
        |  |  |       | Istio Service Mesh (mTLS, Observ.)  |  |
        |  |  +-------+--------------+-----------+           |  |
        |  |          |              |                       |  |
        |  |          v              v                       |  |
        |  |  +--------------+ +--------------+             |  |
        |  |  | Aurora MySQL | | ElastiCache  |             |  |
        |  |  | (Multi-AZ,   | | (Redis       |             |  |
        |  |  |  Read Replica)| |  Cluster)    |             |  |
        |  |  +------+-------+ +--------------+             |  |
        |  |         |  CDC via DMS/DBlog                  |  |
        |  |         v                                     |  |
        |  |  +------------------------------+             |  |
        |  |  | S3 Data Lake + Athena/Redshift|             |  |
        |  |  | + Glue ETL + Lake Formation   |             |  |
        |  |  +------------------------------+             |  |
        |  +------------------------------------------------+  |
        |  Observability: CloudWatch/X-Ray/Prometheus+Grafana |
        |  Security: IAM, KMS, Secrets Manager, GuardDuty      |
        |  IaC: Terraform/CloudFormation/CDK, GitOps(ArgoCD)  |
        +------------------------------------------------------+
                  ^                                  ^
                  |      Cross-Region Replication   |
                  |      (Active-Active or Standby)  |
        +---------+----------------------------------+---------+
        | Region: ap-northeast-1 (도쿄) - DR/Active-Active    |
        +------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Edge & Global Network** | 글로벌 트래픽 라우팅, DDoS 방어, 정적 콘텐츠 캐싱 | Route 53(지연시간/가중치/지역 기반 라우팅), CloudFront/Azure CDN(Anycast, 400+ PoP), AWS WAF(SQL Injection/XSS 룰셋), Shield Advanced(L3/L4/L7 DDoS 자동 완화) |
| **API Gateway & BFF** | 인증/인가, 트래픽 관리, 요청 라우팅, Backends-For-Frontends 패턴 | AWS API Gateway(10K RPS), Kong(OpenResty+Lua), Apigee(API 분석), GraphQL Gateway(Apollo/Hive), Rate Limiting(Token Bucket/Leaky Bucket) |
| **Container Orchestration** | 컨테이너 자동 배포/스케일링/복구, 선언적 상태 관리 | Kubernetes 1.30+(Control Plane: API Server, etcd, Scheduler, Controller Manager), EKS/AKS/GKE(Managed K8s), Helm(차트), Kustomize, HPA/VPA/Cluster Autoscaler, Karpenter(2023, 노드 프로비저닝 5분->30초) |
| **Service Mesh** | 마이크로서비스 간 통신 제어(mTLS, 트래픽 분할, 관측) | Istio(Envoy Sidecar), Linkerd(Rust 기반 Buoyant), Consul Connect, Istio Ambient Mesh(2023, Sidecar 제거) - mTLS 1.3, Circuit Breaker, Retry, Timeout, Fault Injection |
| **Serverless/FaaS** | 이벤트 기반 코드 실행, Cold Start 최적화 | AWS Lambda(128MB~10GB, 15분 타임아웃), Azure Functions, GCP Cloud Run, Cloudflare Workers(V8 Isolate, 0ms Cold Start), SnapStart(Lambda, 10배 빠른 기동) |
| **Data Layer** | 트랜잭션/분석/캐시/오브젝트 데이터의 통합 관리 | Aurora MySQL/PostgreSQL(Read Replica 15개, 128TB), DynamoDB(Single-digit ms, Global Table), Redis 7(Cluster Mode), S3(11 9s durability, IA/Glacier 계층화) |
| **Observability (3 Pillars)** | Logs/Metrics/Traces 통합 관측, AIOps | Prometheus(시계열 TSDB)+Grafana, OpenTelemetry(OTel, 표준 계측), Jaeger/Zipkin(분산 추적), Loki(로그 집계), Datadog/New Relic(SaaS 통합), CloudWatch+X-Ray |
| **Security & Identity** | Zero Trust, 최소 권한, 데이터 암호화 | IAM(Policy: Resource/Action/Effect/Principal 4-tuple), KMS(Customer Managed Key, BYOK/HYOK), Secrets Manager/Vault, OPA(Open Policy Agent), RBAC+ABAC, Service Mesh mTLS |
| **IaC & GitOps** | 인프라 코드로 정의, Git을 Single Source of Truth로 | Terraform(상태파일 State Locking, HCL 2.0), Pulumi(일반 언어 IaC), AWS CDK(TS/Python), ArgoCD/Flux(GitOps Reconciliation), Atlantis(Terraform PR 자동화) |

**핵심 동작 원리 심층 분석:**

**1) Auto Scaling 알고리즘**: AWS EC2 Auto Scaling Group(ASG)은 **Target Tracking Scaling**(예: CPU 70% 유지), **Step Scaling**(임계치별 단계별 조정), **Simple Scaling**(CloudWatch Alarm 기반), **Predictive Scaling**(ML 기반 48시간 예측, 2022~) 정책을 제공합니다. Kubernetes HPA(Horizontal Pod Autoscaler)는 `metrics-server`로부터 15초 간격으로 메트릭을 수집하고, `desiredReplicas = ceil[currentReplicas * (currentMetricValue / desiredMetricValue)]` 공식으로 replicas를 산출합니다. **Karpenter**(2023 GA)는 기존 Cluster Autoscaler 대비 90% 빠른 노드 프로비
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 618 / 800

<- **이전**: [617. 클라우드 아키텍처 핵심 토픽 617번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/617_cloud_architecture_core_topic_617_exam_summar/)
**다음**: [619. 클라우드 아키텍처 핵심 토픽 619번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/619_cloud_architecture_core_topic_619_exam_summar/) ->

---
