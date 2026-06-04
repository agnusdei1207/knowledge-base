---
title: "775. 클라우드 아키텍처 핵심 토픽 775번 시험 요약 (Cloud Architecture Core Topic 775 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


# 775. 클라우드 아키텍처 핵심 토픽 775번 시험 요약

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 컴퓨팅·스토리지·네트워크 자원을 API로 추상화하여 On-Demand·탄력적·측정 가능한(Metered) 형태로 제공하는 분산 컴퓨팅 패러다임이며, IaaS/PaaS/SaaS/FaaS의 **책임 공유 모델(Shared Responsibility Model)** 과 **Well-Architected 5대 기둥**(운영 우수성·보안·안정성·성능 효율성·비용 최적화) 프레임워크로 워크로드의 가용성·확장성·복원력을 설계하는 아키텍처이다.
> 2. **가치**: CapEx->OpEx 전환으로 초기 인프라 투자비 50~70% 절감, Auto Scaling·Spot Instance·Reserved Instance 조합으로 TCO(총소유비용) 30~60% 감소, 멀티 AZ·멀티 리전 구성으로 **99.99%(연 52.6분 이내 장애)** SLA 수준의 고가용성 확보 및 BCP/DR(사업연속성) RTO 1시간 이내 달성.
> 3. **판단 포인트**: 워크로드의 **데이터 중력(Data Gravity)**·**상태 유지성(Stateless/Stateful)**·**일관성 요구 수준(CAP/PACELC)** 분석에 따른 퍼블릭/프라이빗/하이브리드/멀티클라우드 배치 결정, 마이그레이션 **6R 전략**(Rehost·Replatform·Refactor·Repurchase·Retire·Retain)의 업무·비용·위험 트레이드오프, **Vendor Lock-in** 회피를 위한 인터페이스 추상화(IaC, Container, Open API) 및 클라우드-중립 아키텍처 패턴 적용 여부.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스 인프라 시대에는 **CAPEX(Capital Expenditure)** 위주의 하드웨어 조달 방식으로 인해, **(1) 용량 계획의 부정확성**, **(2) 트래픽 피크 대비 과잉 투자**, **(3) 프로비저닝 리드타임(수주~수개월)**, **(4) 장애 대응의 수동적 프로세스**, **(5) 글로벌 확장성 부재** 라는 5대 구조적 한계가 존재했다. 특히 2006년 AWS S3/EC2 출시 이후 클라우드 컴퓨팅은 가상화·자동화·API 경제·분산 시스템 이론의 융합체로 진화하며, **NIST SP 800-145** 정의(5대 필수 특성: On-Demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)를 만족하는 새로운 IT 운영 모델을 제시하였다.

클라우드 아키텍처는 단순한 "IDC 외주"가 아니라, **인프라를 코드로 정의(IaC, Infrastructure as Code)** 하고 **API로 모든 자원을 프로그래밍 가능**하게 만드는 **클라우드 네이티브(Cloud-Native) 사고방식**의 근간이다. 775번 시험에서는 단순 기능 암기보다, 워크로드의 특성을 파악해 **적합한 클라우드 서비스·배포 모델·아키텍처 패턴을 선정하고 그 트레이드오프를 논리적으로 설명**할 수 있는 능력이 평가된다.

```text
+------------------------------------------------------------------+
|            On-Premise vs Cloud Paradigm 비교 (구조도)            |
+------------------------------------------------------------------+

  <- 전통적 On-Premise (수직 통합, Silo형) ->        <- Cloud Native (수평 분할, API형) ->

  +---------------------+                  +--------------------------------+
  |   Application        |                  | Application Layer (SaaS)       |
  +---------------------+                  |   - SaaS, FaaS, Microservice   |
  |   Middleware        |   ---------►      +--------------------------------+
  |   (WAS, WebLogic)   |   패러다임 전환    | Platform Layer (PaaS)          |
  +---------------------+                  |   - K8s, App Engine, Lambda    |
  |   OS                |                  +--------------------------------+
  +---------------------+                  | Infrastructure Layer (IaaS)    |
  |   Hypervisor        |                  |   - EC2, VPC, EBS, S3          |
  +---------------------+                  +--------------------------------+
  |   Physical HW       |                  | Global Edge / CDN / Region     |
  +---------------------+                  +--------------------------------+
        CapEx 중심                                OpEx 중심 (Pay-per-use)
   용량 계획/과잉 투자                              Auto Scaling / 탄력 운영
   수동 장애 대응                                  Self-Healing / IaC
   1개 DC 단일 장애점                              Multi-AZ / Multi-Region
```

```text
[클라우드 5대 핵심 특성 - NIST SP 800-145]

     +----------- On-Demand Self-Service -----------+
     |  사용자가 관리자 개입 없이 API/UI로 즉시 프로비저닝
     |     (예: AWS 콘솔에서 EC2 클릭 -> 90초 내 기동)
     +---------------------------------------------+
                           ^
     +----------- Broad Network Access -------------+
     |  HTTP/HTTPS 표준 프로토콜, 다양한 클라이언트
     |     (모바일, 데스크탑, IoT, CLI, SDK)
     +---------------------------------------------+
                           ^
     +----------- Resource Pooling -----------------+
     |  멀티테넌트, 가상화로 자원 통합, 위치 투명성
     |     (예: 동일 하드웨어에서 수백 VM 동시 운영)
     +---------------------------------------------+
                           ^
     +----------- Rapid Elasticity -----------------+
     |  수요 변동에 따라 자동 스케일 인/아웃
     |     (예: Auto Scaling Group, K8s HPA, Karpenter)
     +---------------------------------------------+
                           ^
     +----------- Measured Service ------------------+
     |  사용량 계량·모니터링·투명화 (CloudWatch, Billing API)
     |     (예: vCPU·초, GB·월, 요청 수 기반 과금)
     +---------------------------------------------+
```

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **"전기 수도 그리드(Electricity Grid)"** 와 같다. 과거에는 각 가정·공장이 발전기를 직접 운영해야 했으나(온프레미스), 지금은 송전망(클라우드 인프라)을 통해 **누구나 콘센트만 꽂으면**(API 호출) **필요한 만큼만**(탄력 과금) **안심하고**(SLA) 전기를 쓴다. "누가 전기를 만드는지" 알 필요 없이 **결과(Compute·Storage·Network)만 사용**하는 책임 분리 구조가 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 크게 **① 서비스 모델(IaaS/PaaS/SaaS/FaaS)**, **② 배포 모델(Public/Private/Hybrid/Multi/Community)**, **③ 기술 스택 계층(Compute·Storage·Network·Database·Security·Observability)** 으로 구성된다. 775번 시험에서는 각 계층의 **핵심 서비스·프로토콜·일관성 모델·장애 도메인**에 대한 깊은 이해가 요구된다.

```text
[클라우드 네이티브 아키텍처 전체 구조도 - 12-Factor 기반]

   +------------------------------------------------------------+
   |  ① Edge / CDN Layer                                       |
   |     CloudFront, Cloudflare, Akamai (TLS Termination, WAF)  |
   |     +-► DDoS 방어, 정적 컨텐츠 캐싱, Geo-Routing          |
   +--------------+---------------------------------------------+
                  v (HTTPS)
   +------------------------------------------------------------+
   |  ② API Gateway / Ingress Controller                        |
   |     Kong, AWS API GW, ALB/NLB, Istio Gateway               |
   |     +-► 라우팅, 인증, Rate-Limit, Circuit Breaker          |
   +--------------+---------------------------------------------+
                  v
   +------------------------------------------------------------+
   |  ③ Microservice / Application Layer (Stateless)            |
   |     - EKS/ECS Pod (Container)  / Lambda (FaaS)             |
   |     - Service Mesh: Istio / Linkerd (mTLS, Observability)  |
   |     - HPA/VPA/Cluster Autoscaler로 Pod 수 자동 조정        |
   +--------------+---------------------------------------------+
                  v
   +------------------------------------------------------------+
   |  ④ Messaging / Event Streaming (비동기 결합)               |
   |     Kafka, RabbitMQ, AWS SQS/SNS, EventBridge, Pub/Sub    |
   |     +-► Eventual Consistency, Backpressure, Replay        |
   +--------------+---------------------------------------------+
                  v
   +------------------------------------------------------------+
   |  ⑤ Data Layer (다층 저장소 - Polyglot Persistence)         |
   |     - OLTP:   Aurora MySQL/PostgreSQL, DynamoDB, Spanner   |
   |     - Cache:  ElastiCache (Redis), MemoryDB                |
   |     - Search: OpenSearch, Elasticsearch                    |
   |     - OLAP:   Redshift, BigQuery, Snowflake                |
   |     - Object: S3, GCS, Azure Blob (12-nine's durability)  |
   |     - Cold:   S3 Glacier, Glacier Deep Archive            |
   +--------------+---------------------------------------------+
                  v
   +------------------------------------------------------------+
   |  ⑥ Infrastructure Foundation                              |
   |     VPC, Subnet, IGW, NAT GW, TGW, PrivateLink, Direct    |
   |     Connect, Interconnect, IAM, KMS, Secrets Manager      |
   |     Multi-AZ / Multi-Region / DR Pattern                   |
   +------------------------------------------------------------+
                  ^
   +------------------------------------------------------------+
   |  ⑦ Cross-Cutting Concerns                                 |
   |     Observability: Prometheus / Grafana / OpenTelemetry    |
   |     CI/CD:        GitHub Actions / ArgoCD / CodePipeline   |
   |     IaC:          Terraform / Pulumi / CloudFormation      |
   |     Security:     OPA, Vault, Falco, Trivy, SAST/DAST      |
   +------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Compute (IaaS)** | 가상 서버/네트워크/스토리지 제공 | AWS EC2, GCP Compute Engine, Azure VM. **Hypervisor (KVM/Xen/Hyper-V)** 위에서 가상화, Instance Type별 vCPU·Memory·Network Capacity 차등, **Placement Group** 으로 네트워크 locality 보장. Nitro System으로 호스트 가상화 오버헤드 1% 미만. |
| **Container Orchestrator** | 컨테이너 자동 배포·스케일·복구 | **Kubernetes (K8s)** 가 사실 표준. Control Plane(etcd + kube-apiserver + scheduler) + Worker Node(kubelet + kube-proxy). 선언형 YAML 명세 -> 현재 상태 vs 목표 상태 **Reconciliation Loop**. HPA(메트릭 기반), VPA(리소스 재조정), CA(노드 확장), Karpenter(지능형 프로비저닝) |
| **Serverless / FaaS** | 이벤트 기반 Stateless 코드 실행 | AWS Lambda, Azure Functions, GCP Cloud Functions. **콜드 스타트**(보통 100~500ms, Provisioned Concurrency로 0ms 단축), 15분 최대 실행, 동시성 1000/리전 한도. **이벤트 소스**(API GW, S3, SQS, EventBridge, Kinesis) 트리거 기반 과금(GB-초·호출 수) |
| **Object Storage** | 비정형 데이터 무제한 저장 | **S3, GCS, Azure Blob**. 99.999999999%(11 Nine) 내구성, **Erasure Coding (Reed-Solomon)**, 스토리지 클래스(Standard/IA/Glacier)로 비용-접근성 트레이드오프. **Lifecycle Policy**로 자동 계층 이동, **S3 Object Lambda**로 데이터 변환 코드 임베드 |
| **Block Storage** | 고IOPS 저지연 디스크 | **EBS, Persistent Disk**. Snapshot 기반 증분 백업, Multi-Attach(동시 연결) 일부 지원, IOPS·Throughput 별도 프로비저닝(gp3, io2 Block Express) |
| **Managed Database** | 자동 백업·패치·복제·HA | **RDS, Aurora, Cloud SQL, Azure SQL**. Aurora는 6-way 복제로 quorum 기반 내구성, **Global Database**로 리전 간 복제(< 1초 RPO). DynamoDB는 **Single-Leader 분산 KV**, GSI/LSI로 쿼리 패턴 확장, **DynamoDB Streams + Lambda**로 CDC |
| **Networking & VPC** | 논리적 사설망·라우팅 | **VPC(Virtual Private Cloud)** = 리전 단위, Subnet = AZ 단위, Route Table·NACL·SG 다중 방어선. **Transit Gateway**로 VPC 피어링 N² 문제 해결, **PrivateLink**로 퍼블릭 인터넷 우회 내부 통신 |
| **Identity & Access (IAM)** | 최소 권한·인증·인가 | **RBAC(역할 기반)**, ABAC(속성 기반), SCP(Service Control Policy) OU 단위 거버넌스. **STS + AssumeRole**로 임시 자격증명, IAM Role을 EC2/IRSA에 부여(Pod별 AWS 권한) |
| **Observability** | 모니터링·로깅·트레이싱 | 3대 신호: **Metrics(Prometheus/CloudWatch)** + **Logs(Loki/CloudWatch Logs)** + **Traces(Jaeger/OpenTelemetry)**. **
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 775 / 800

<- **이전**: [774. 클라우드 아키텍처 핵심 토픽 774번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/774_cloud_architecture_core_topic_774_exam_summar/)
**다음**: [776. 클라우드 아키텍처 핵심 토픽 776번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/776_cloud_architecture_core_topic_776_exam_summar/) ->

---
