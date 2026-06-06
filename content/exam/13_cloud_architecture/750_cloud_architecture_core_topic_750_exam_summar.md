---
title: "Cloud Architecture Core Topic 750 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS(EC2, Compute Engine), PaaS(Beanstalk, App Engine), SaaS(Office 365, Salesforce) 및 FaaS(Lambda, Cloud Functions)를 통한 **탄력적 컴퓨팅 추상화(Elastic Compute Abstraction)**와 API 기반의 프로비저닝 자동화, 셀프서비스 프로비저닝, 사용량 기반 과금(Usage-based Metering)의 5대 필수 특성(NIST SP 800-145)을 만족하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: Well-Architected Framework(WAFF) 5대 축(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화 + 지속가능성) 적용 시 인프라 CapEx를 약 60~70% 절감하고, Auto Scaling Group을 통한 트래픽 처리 능력 10~100배 확장, RTO/RPO를 분 단위로 단축하는 재해복구 능력을 확보할 수 있다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs 멀티/하이브리드 전략, 동기적 강한 결합(강한 일관성, 2PC) vs 비동기적 약한 결합(最终 일관성, Saga, Event Sourcing), Stateful 컨테이너 vs Stateless 12-Factor App, Public Internet 노출 vs Private Endpoint(VPC Peering, Transit Gateway) 간의 트레이드오프가 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

전통적인 On-Premise 3-tier 아키텍처(Web-Tier, App-Tier, DB-Tier)는 peak load 기반의 capacity planning으로 인해 평균 15~25%의 자원만 활용되는 비효율을 초래하며, 신규 인프라 도입에 평균 6~12주의 Lead Time과 수천만 원의 CapEx가 발생한다. 또한 BCP/DR 구성 시 이중 투자로 인한 TCO 증가, HA(High Availability) 확보를 위한 Active-Active 구성의 복잡도 상승, 그리고 글로벌 서비스 확장의 물리적 한계 등 근본적 한계를 가진다.

클라우드 아키텍처는 이러한 한계를 극복하기 위해 **가상화(KVM, Xen, Hyper-V) -> 컨테이너화(Docker, containerd) -> 오케스트레이션(Kubernetes) -> 서버리스(Lambda, Cloud Run) -> 분산 엣지(Cloudflare Workers, Lambda@Edge)**로 발전해 왔다. 핵심은 자원을 코드(Infra as Code, Terraform/AWS CDK)로 선언하고, API로 제어하며, 사용량에 따라 자동으로 확장·축소되는 **셀프서비스·프로그래머블·온디맨드(Self-service, Programmable, On-demand)** 인프라이다.

```text
+-------------------------------------------------------------------------+
|              On-Premise vs Cloud Architecture 패러다임 비교             |
+-------------------------------------------------------------------------+
|                                                                         |
|  [전통적 On-Premise 3-Tier]              [Cloud-Native 12-Factor]      |
|  +----------------------+                +--------------------------+   |
|  |  Load Balancer (HW)  |                |  CDN + Global LB (Anycast)|  |
|  +----------+-----------+                +------------+-------------+   |
|             |                                         |                 |
|  +----------v-----------+                +-----------v-------------+   |
|  |  Web Tier (Fixed VM) |  --변화--►     |  API Gateway + Lambda   |   |
|  |  Max: 100, Avg: 20   |                |  (Auto-scale 0->1000)     |   |
|  +----------+-----------+                +-----------+-------------+   |
|             |                                         |                 |
|  +----------v-----------+                +-----------v-------------+   |
|  | App Tier (WAS)       |                | Microservices on EKS    |   |
|  | 수직확장(Scale-Up)    |  --변화--►     | + Service Mesh (Istio)  |   |
|  +----------+-----------+                +-----------+-------------+   |
|             |                                         |                 |
|  +----------v-----------+                +-----------v-------------+   |
|  | DB (Oracle RAC)      |                | RDS Aurora + ElastiCache|   |
|  | 백업: LTO Tape        |  --변화--►     | + DynamoDB (NoSQL)      |   |
|  +----------------------+                +--------------------------+   |
|                                                                         |
|  ❌ Peak 기반 과다투자                  ✅ Pay-per-use 최적화           |
|  ❌ 6~12주 Lead Time                   ✅ API 호출 즉시 프로비저닝      |
|  ❌ 수동 DR 대응                        ✅ Multi-AZ 자동 failover      |
+-------------------------------------------------------------------------+
```

**클라우드 도입의 비즈니스적 필요성**:
- **Time-to-Market 단축**: 신세계아이앤씨 사례, 인프라 배포 시간을 6주 -> 15분으로 단축
- **탄력성(Elasticity)**: 11.11(쌍11) 쇼핑 트래픽 17배 급증에도 Auto Scaling으로 무중단 처리
- **글로벌 확장성**: AWS Global Infrastructure(33개 리전, 105개 가용영역)를 활용한 리전 간 복제
- **TCO 절감**: Netflix 사례, On-Prem 대비 약 30% 인프라 비용 절감 (CFO Report 2018)

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "전기를 자체 발전소에서 만들던 시대를 지나, 콘센트에 꽂아 쓰는 시대"로의 전환과 같다. 발전기(서버)를 직접 사서 굴릴 필요 없이, 필요할 때 콘센트(API)로부터 필요한 만큼 전기를 끌어다 쓰고, 안 쓸 때는 자동으로 차단되어 전기요금(클라우드 비용)만 내는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **NIST SP 800-145**의 4가지 배포 모델(Public, Private, Hybrid, Community)과 **5대 특성**(On-demand Self-service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)을 토대로, **Well-Architected Framework의 5~6대 축**을 반복적으로 검증하며 발전한다.

```text
+----------------------------------------------------------------------+
|         Cloud Reference Architecture (AWS 기준 예시)               |
+----------------------------------------------------------------------+
|                                                                      |
|  [사용자/Client]                                                      |
|       | HTTPS/TLS 1.3                                                |
|       v                                                              |
|  +---------------------------------------------------------+        |
|  | Edge Layer: CloudFront (CDN) + Route 53 (DNS Latency-based)|    |
|  |  + WAF (OWASP Top 10 방어) + Shield Advanced (DDoS)      |    |
|  +------------------------+--------------------------------+        |
|                           v                                          |
|  +---------------------------------------------------------+        |
|  | Global Network Layer: Transit Gateway (Multi-VPC 허브)   |        |
|  |  + Direct Connect (전용선) + VPC Peering                 |        |
|  +------------------------+--------------------------------+        |
|                           v                                          |
|  +---------------------------------------------------------+        |
|  | Application Layer: ALB -> ECS/EKS (Pod) -> Lambda         |        |
|  |  + API Gateway (REST/WebSocket) + AppSync (GraphQL)     |        |
|  |  + Step Functions (Saga Orchestration)                   |        |
|  +------------------------+--------------------------------+        |
|                           v                                          |
|  +---------------------------------------------------------+        |
|  | Data Layer: Aurora (R/W 분리) + DynamoDB (DAX)           |        |
|  |  + ElastiCache (Redis Cluster) + S3 (Versioning)        |        |
|  |  + Kinesis/Kafka (Streaming) + Athena (Lake House)      |        |
|  +------------------------+--------------------------------+        |
|                           v                                          |
|  +---------------------------------------------------------+        |
|  | Ops Layer: CloudWatch + X-Ray (분산 트레이싱)           |        |
|  |  + CloudTrail (Audit) + Config (Compliance)             |        |
|  |  + EventBridge (EDA) + Systems Manager (Patch)          |        |
|  +---------------------------------------------------------+        |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨팅 계층** | 비즈니스 로직 실행 | **EC2**(IaaS, AMI 기반), **Lambda**(FaaS, 15분 타임아웃, 10GB 메모리), **Fargate**(서버리스 컨테이너), **EKS/ECS**(Kubernetes 기반), **EC2 Spot Fleet**(스팟 인스턴스 90% 할인) |
| **스토리지 계층** | 데이터 영속성 보장 | **S3**(Object, 11 9s 내구성, IA/Glacier 티어링), **EBS**(Block, gp3/cold HDD), **EFS/FSx**(Shared File, NFS/SMB), **Instance Store**(로컬 NVMe, 휘발성) |
| **네트워크 계층** | 보안 격리 및 라우팅 | **VPC**(논리적 격리, /16 CIDR), **Subnet**(Public/Private/NAT GW), **Security Group**(Stateful, 인스턴스 레벨), **NACL**(Stateless, 서브넷 레벨), **VPC Endpoint**(Gateway/Interface, PrivateLink) |
| **데이터 계층** | 트랜잭션 및 분석 | **RDS Aurora**(6복제, MySQL/PostgreSQL 호환), **DynamoDB**(Single-digit ms, Global Tables), **Redshift**(MPP DW), **Neptune**(Graph DB) |
| **오케스트레이션** | IaC 및 GitOps | **Terraform**(HCL 멀티클라우드), **CloudFormation**(AWS 전용), **Ansible/Pulumi**, **ArgoCD/Flux**(GitOps), **Packer**(AMI 베이크) |
| **옵저버빌리티** | 모니터링 및 추적 | **3 Pillars**: Metrics(Prometheus, CloudWatch), Logs(Loki, ELK), Traces(Jaeger, X-Ray), **SLO/SLI/SLI** 기반 알람, **AIOps**(이상 탐지) |

**핵심 원리 - 12-Factor App**:
1. **Codebase**: 단일 코드베이스, 다중 배포
2. **Dependencies**: 명시적 선언(`package.json`, `requirements.txt`)
3. **Config**: 환경변수 분리, 코드에서 분리
4. **Backing Services**: DB/Queue를 부착 가능한 리소스로 취급
5. **Build, Release, Run**: 3단계 엄격히 분리
6. **Processes**: Stateless 프로세스, 공유 안 함
7. **Port Binding**: 자체 포트 바인딩
8. **Concurrency**: 프로세스 모델로 확장
9. **Disposability**: 빠른 시작/우아한 종료(SIGTERM 처리)
10. **Dev/Prod Parity**: 환경 일치
11. **Logs**: 이벤트 스트림으로 취급(STDOUT)
12. **Admin Processes**: 1회성 작업도 동일 환경에서 실행

- **📢 섹션 요약 비유**: 12-Factor App은 "출장 시 필요한 짐 싸는 표준 매뉴얼"이다. 출장(배포) 때마다 옷(설정), 충전기(DB 연결정보), 세면도구(로그)를 가방에서 쉽게 꺼낼 수 있도록 정해진 12가지 규칙대로 짐을 싸면, 어떤 도시(환경)에서도 즉시 일할 수 있는 것이다.

---

## Ⅲ. 비교 및 연결

### 1. 컴퓨팅 서비스 비교 (IaaS vs PaaS vs CaaS vs FaaS)

| 구분 | IaaS (EC2) | PaaS (Beanstalk) | CaaS (EKS) | FaaS (Lambda) |
| :--- | :--- | :--- | :--- | :--- |
| **추상화 수준** | VM/Hypervisor | Runtime + Middleware | Container Orchestration | Function Event |
| **책임 모델** | OS 미들웨어 이상 사용자 | App 코드만 사용자 | Container Image만 사용자 | 함수 코드만 사용자 |
| **Cold Start** | 없음 (상시 기동) | 30~60초 | 5~30초 | 100ms~5초 |
| **확장 단위** | 인스턴스 단위 | 인스턴스 단위 | Pod 단위 (1~수십) | 동시실행(Concurrency) 단위 |
| **최대 실행 시간** | 무제한 | 무제한 | 무제한 | **15분 (Lambda 한도)** |
| **상태 관리** | Stateful 가능 | Stateful 가능 | StatefulSet 지원 | **반드시 Stateless** |
| **적합 워크로드** | 레거시, 게임 서버, HPC | 일반 웹앱 마이그레이션 | MSA, CI/CD, 멀티클라우드 | 이벤트 기반, ETL, Webhook |
| **비용 모델** | 시간당 과금 | 시간당 과금 | Pod+Node 과금 | **100ms 단위 과금** |
| **대표 기술** | EC2, GCE, Azure VM | Elastic Beanstalk, App Engine | EKS, GKE, AKS | Lambda, Cloud Functions |

### 2. 분산 트랜잭션 패턴 비교 (강한 일관성 vs 最终 일관성)

| 구분 | 2PC (Two-Phase Commit) | Saga Pattern | Event Sourcing |
| :--- | :--- | :--- | :--- |
| **일관성 모델** | Strong Consistency (ACID) | Eventual Consistency | Eventual Consistency |
| **프로토콜** | Prepare -> Commit | Orchestration/Choreography | Append-only Event Log |
| **성능** | 낮음 (Lock 점유) | 중간 (보상 트랜잭션) | 높음 (비동기 Projection) |
| **확장성** | 수직 확장 위주 | 수평 확장 가능 | 무한 수평 확장 |
| **장애 대응** | Coordinator 단일 장애점 | 보상 트랜잭션 역실행 | 이벤트 재생으로 복구 |
| **적용 사례** | 금융 코어, 결제 정합성 | 전자상거래 주문-재고-결제 | 도메인 이벤트, CQRS |
| **구현 기술** | Java JTA, MySQL XA | Camunda, Temporal, Step Functions | Kafka + Debezium, EventStoreDB |

### 3. 네트워크 연결 옵션 비교

| 구분 | Internet VPN | Direct Connect / ExpressRoute | Transit Gateway | VPC Peering |
| :--- | :--- | :--- | :--- | :--- |
| **연결 방식** | IPSec 터널 (인터넷 경유) | **전용선 (Private)** | 허브-스포크 라우팅 | 1:1 VPC 직접 연결 |
| **대역폭** | 1.25 Gbps/site | 1/10/100 Gbps | 리전 내 통합 | VPC 페어당 100 Gbps |
| **지연 시간** | 20~80ms (가변) | **1~10ms (안정)** | 매우 낮음 | 매우 낮음 |
| **암호화** | IPSec 필수 | MACsec 옵션 | 미암호화 (VPC 내 신뢰) | 미암호화 |
| **비용** | 저가 | 고가 (포트 + 데이터) | 허브 시간당 과금 | 무료 (데이터만 과금) |
| **적합 케이스** | 소규모, PoC, DR | **대규모 Production, 규제** | 100+ VPC 통합 | 단순 1:1 연결 |

### 4. 멀티클라우드 전략 비교

| 구분 | All-in-One | Active-Active Multi-Cloud | Hybrid Cloud | Cloud Bursting |
| :--- | :--- | :--- | :--- | :--- |
| **아키텍처** | 단일 CSP 종속 | 2개 이상 동시 운영 | On-Prem + Public | 평시 On-Prem, 피크시 Public |
| **Lock-in 위험** | 매우 높음 | 낮음 | 중간 | 낮음 |
| **복잡도** | 낮음 | **매우 높음** | 중간 | 중간 |
| **DR 효과** | 낮음 (단일 장애점) | 매우 높음 (리전 단위) | 높음 | 높음 |
| **적용** | 대부분의 스타트업 | 대형 금융, 통신 | 규제 산업(금융, 의료) | HPC, ML 학습 |
| **도구** | AWS Console | Terraform, Anthos, Azure Arc | AWS Outposts, GCP Anthos | Spotinst, ScaleSet |

- **📢 섹션 요약 비유**: 컴퓨팅
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 750 / 800

<- **이전**: [749. 클라우드 아키텍처 핵심 토픽 749번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/749_cloud_architecture_core_topic_749_exam_summar/)
**다음**: [751. 클라우드 아키텍처 핵심 토픽 751번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/751_cloud_architecture_core_topic_751_exam_summar/) ->

---
