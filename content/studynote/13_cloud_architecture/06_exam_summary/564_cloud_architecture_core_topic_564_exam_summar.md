---
title: "564. 클라우드 아키텍처 핵심 토픽 564번 시험 요약 (Cloud Architecture Core Topic 564 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 컴퓨팅·스토리지·네트워크 자원의 추상화 계층을 통해 API 기반 셀프서비스 프로비저닝과 탄력적 스케일링(Elasticity)을 구현하며, 12-Factor App 원칙과 Well-Architected Framework에 입각한 설계가 핵심
> 2. **가치**: CapEx->OpEx 전환으로 초기 투자비 60~80% 절감, Auto Scaling으로 평균 리소스利用率 70%+ 달성, 페일오버 RTO <60초·RPO <5분 수준으로 DR 등급 Tier-IV 구현 가능
> 3. **판단 포인트**: 워크로드 특성(Stateful vs Stateless, I/O Intensive vs CPU Bound), 컴플라이언스 요건(개인정보보호법, CSAP), 멀티/하이브리드 클라우드 전략, FinOps 기반 비용 거버넌스, Egress Lock-in 회피 전략

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 환경에서는 HW 도입(Lead Time 8~12주), 용량 계획(Capacity Planning), 피크 부하 대비 과다 설계(Over-Provisioning 200~300%)로 인해 TCO(Total Cost of Ownership)가 증가하고, 서비스 출시까지 6개월 이상이 소요되었습니다. 클라우드 아키텍처는 **가상화 -> 컨테이너 -> 서버리스**로 진화하며, 자원 추상화 수준을 높여 **밀리초 단위 프로비저닝**과 **사용량 기반 과금(Usage-based Pricing)**을 실현합니다.

2024년 기준 국내 CSAP(Cloud Security Assurance Program) 인증 클라우드는 NHN Cloud, KT Cloud, Naver Cloud, Samsung Cloud Platform 등 4개사이며, 공공·금융권 마이그레이션 시 필수 요건입니다. AWS, Azure, GCP 등 하이퍼스케일러는 200+ 서비스, 50개+ 리전, 200개+ PoP로 글로벌 커버리지를 제공합니다.

```text
+-----------------------------------------------------------------+
|              On-Premise vs Cloud Paradigm 비교                   |
+-----------------------------------------------------------------+
|                                                                 |
|  [On-Premise]              ---►          [Cloud-Native]        |
|  +----------+                              +--------------+    |
|  | Server   |  수동 설치 (8주)              | API 호출     |    |
|  | Rack     | --------►                    | (30초)       |    |
|  +----------+                              +--------------+    |
|  +----------+                              +--------------+    |
|  | Network  |  VLAN/Trunk                  | VPC/Subnet   |    |
|  | Firewall |  HW 방화벽                   | SG/NACL/WAF  |    |
|  +----------+                              +--------------+    |
|  +----------+                              +--------------+    |
|  | Storage  |  SAN/NAS                     | EBS/S3/Blob  |    |
|  | DAS      |  LUN 할당 (3일)              | Snapshot 1초  |    |
|  +----------+                              +--------------+    |
|                                                                 |
|  CapEx 80% / OpEx 20%              CapEx 20% / OpEx 80%        |
|  수직 확장(Scale-Up)                수평 확장(Scale-Out)        |
|  트래픽 피크 = 과다 설계            Auto Scaling = 자동         |
|  장애 대응 = DR Site 구축          Multi-AZ / Multi-Region     |
+-----------------------------------------------------------------+
```

온프레미스 대비 클라우드는 **탄력성(Elasticity)**, **위임(Abstraction)**, **자가치유(Self-Healing)**의 3대 차별점을 제공하며, 2020년 이후 **클라우드 네이티브(Cloud Native)** 패러다임으로 진화했습니다. CNCF(Cloud Native Computing Foundation)가 정의한 클라우드 네이티브 4대 축은 ① 컨테이너화 ② 오케스트레이션 ③ 마이크로서비스 ④ 선언적 API(Declarative API)입니다.

- **📢 섹션 요약 비유**: 온프레미스는 "호텔을 통째로 사서 매일 손님 수에 맞춰 증축하는 것"이고, 클라우드는 "필요한 객실만 1분 단위로 빌리는 에어비앤비"와 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **5계층 모델**(물리 인프라 -> 가상화 -> 자원 풀 -> 서비스 카탈로그 -> 워크로드)로 구성되며, 각 계층은 API·제어 플레인(Control Plane)·데이터 플레인(Data Plane)으로 분리됩니다.

```text
+----------------------------------------------------------------------+
|              Reference Architecture: Multi-Account / Multi-VPC       |
+----------------------------------------------------------------------+
|                                                                       |
|   [Account: prod-001]   [Account: stage-002]   [Account: dev-003]   |
|   +---------------+    +---------------+       +---------------+   |
|   | VPC 10.0.0.0/16|    |VPC 10.1.0.0/16|       |VPC 10.2.0.0/16|  |
|   | +--+ +--+ +--+|    |+--+ +--+ +--+|       |+--+ +--+ +--+|   |
|   | |AZ| |AZ| |AZ||    ||AZ| |AZ| |AZ||       ||AZ| |AZ| |AZ||   |
|   | |a | |b | |c ||    ||a | |b | |c ||       ||a | |b | |c ||   |
|   | +-+ +-+ +-+|    |+-+ +-+ +-+|       |+-+ +-+ +-+|   |
|   |  ALB/NLB     |    |  ALB/NLB     |       |  ALB/NLB     |   |
|   |  EKS/ECS     |    |  EKS/ECS     |       |  EKS/ECS     |   |
|   |  RDS Aurora  |    |  RDS Aurora  |       |  RDS Aurora  |   |
|   |  S3 / EFS    |    |  S3 / EFS    |       |  S3 / EFS    |   |
|   +------+-------+    +------+-------+       +------+-------+   |
|          |     Transit Gateway / Direct Connect      |            |
|          +--------------------+-----------------------+            |
|                               |                                     |
|   +---------------------------v--------------------------+         |
|   |   Centralized Account (Logging, Security, Network)   |         |
|   |   - CloudTrail, GuardDuty, Security Hub              |         |
|   |   - Transit Gateway, Firewall Central                 |         |
|   |   - IAM Identity Center (SSO)                         |         |
|   +------------------------------------------------------+         |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 계층** | 워크로드 실행 환경 제공 | EC2 (m6i.xlarge 4vCPU/16GB), Lambda (15분 Timeout, 10GB Memory), Fargate (0.25vCPU~16vCPU), EKS/ECS (Kubernetes 1.30+) |
| **스토리지 계층** | 데이터 영속성·내구성 보장 | S3 (11 9s = 99.999999999% 내구성, Standard-IA 30일/Glacier 90일~7년), EBS (gp3 3,000 IOPS, io2 Block Express 256,000 IOPS), EFS (NFS v4, 10GB/s+) |
| **네트워크 계층** | 연결성·격리·라우팅 | VPC (CIDR /16, /24 Subnet), Transit Gateway (5,000 VPC Peering), PrivateLink (사설 연결), CloudFront/Cloud CDN (Edge POP 600+) |
| **데이터 계층** | RDBMS·NoSQL·DW 분리 | RDS Multi-AZ (RTO 60~120초, RPO 0), Aurora Global Database (1초 미만 복제), DynamoDB (Single-digit ms, 10ms P99), ElastiCache (Redis 7.2, Cluster Mode 500 Shard) |
| **오케스트레이션** | IaC·GitOps·정책 자동화 | Terraform (State Lock with DynamoDB), Pulumi (TypeScript), Ansible (Agent-less), ArgoCD/Flux (GitOps), OPA (Rego Policy) |

**핵심 동작 원리 - Auto Scaling 의사결정**:
```
Desired Capacity = max( min_capacity,
                       ceil( current_capacity ×
                             ( target_value / current_metric ) ) )
```
- Target Tracking: CPU 70% 기준, 60초 평가 주기
- Step Scaling: 60%^ -2, 80%^ -4 인스턴스 (Cooldown 300초)
- Predictive Scaling: ML 기반 2일 전 예측 (Look-ahead 12시간)

**고가용성(HA) 패턴**:
- **N+1 패턴**: AZ-a 단일 장애 대비 AZ-b에 1개 여유 인스턴스
- **N+M 패턴**: N개 워크로드에 M개 Hot-Standby (M=1 ~ 25% of N)
- **Active-Active 멀티리전**: Route 53 Latency-based Routing + DynamoDB Global Tables

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "전기로 환산하면, 발전소(IaaS)부터 완성된 가전제품(SaaS)까지 선택할 수 있는 에너지 메뉴판"과 같습니다. 직접 발전기 돌리는 건 비효율적이고, 다기능 가전은 전기료가 비싸니, 요리에 맞는 제품을 고르는 지혜가 필요합니다.

---

## Ⅲ. 비교 및 연결

클라우드 서비스 모델은 **책임 분담 모델(Shared Responsibility Model)**에 따라 분류되며, 운영자(클라우드 제공자)와 이용자(고객)의 책임 경계가 다릅니다.

| 구분 | On-Premise | IaaS (EC2, GCE) | PaaS (Beanstalk, App Engine) | SaaS (Office 365, Slack) |
| :--- | :--- | :--- | :--- | :--- |
| **응용 프로그램** | 고객 | 고객 | 고객 | 제공자 |
| **데이터** | 고객 | 고객 | 고객 | 고객 (보안 정책은 제공자) |
| **런타임/미들웨어** | 고객 | 고객 | 제공자 | 제공자 |
| **OS** | 고객 | 고객 | 제공자 | 제공자 |
| **가상화/하이퍼바이저** | 고객 | 제공자 | 제공자 | 제공자 |
| **물리 서버/스토리지/네트워크** | 고객 | 제공자 | 제공자 | 제공자 |
| **제어 범위** | 100% | ~60% | ~30% | ~10% |
| **구축 시간** | 6~12개월 | 1~4주 | 1~3일 | 즉시 (분) |
| **적합 워크로드** | Legacy, Mainframe, 규제산업 | Lift&Shift, 커스텀 미들웨어 | API·Web 표준 워크로드 | 표준 업무 (메일, 협업) |
| **TCO 5년** | 100% | 40~60% | 30~50% | 20~40% |

**클라우드 배포 모델 비교**:

| 구분 | Public Cloud | Private Cloud | Hybrid Cloud | Multi-Cloud |
| :--- | :--- | :--- | :--- | :--- |
| **소유** | 외부 CSP | 자체/전용 | Public+Private | 2개+ Public |
| **확장성** | 무제한 | 제한적 | 양쪽 장점 | 벤더 종속 회피 |
| **보안 통제** | 낮음 | 높음 | 선택적 | 복잡 |
| **컴플라이언스** | CSAP/ISO27001 | 내부 표준 | 데이터 거버넌스 | 데이터 주권 |
| **네트워크 지연** | 20~100ms | 1~5ms | Direct Connect | VPN 50~200ms |
| **비용 모델** | OpEx | CapEx+OpEx | 혼합 | 이중 과금 위험 |
| **Lock-in 위험** | 중간 | 낮음 | 중간 | 낮음 (전략적) |
| **Egress 비용** | $0.05~0.09/GB | 없음 | Direct Connect | 2개 CSP 이중 |

**연계 기술 스택**:
- **컨테이너**: Docker 25.x -> CRI-O -> containerd -> Kubernetes
- **서비스 메시**: Istio (Envoy Sidecar), Linkerd (eBPF 데이터 플레인), Cilium (eBPF Native)
- **CI/CD**: Jenkins -> GitHub Actions -> Argo Workflows -> Tekton
- **관측성(Observability)**: OpenTelemetry SDK -> Prometheus + Grafana + Loki + Tempo
- **보안**: CSPM (Wiz, Prisma Cloud), CIEM (Cloud Infrastructure Entitlement Management)

- **📢 섹션 요약 비유**: 책임 분담 모델은 "아파트 vs 빌라 vs 전원주택"의 관리비 분담과 같습니다. 아파트(SaaS)는 관리사무소가 거의 다 하지만 관리비(요금)가 비싸고, 전원주택(On-Premise)은 모든 걸 직접 해야 하지만 자유도가 높습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **워크로드 분류**: CPU-Bound(배치, ML 추론) vs I/O-Bound(Web, API) vs Memory-Bound(In-Memory DB) -> 인스턴스 패밀리(c/m/r) 선택, Spot Instance 활용 가능 여부 (배치/CI는 Spot 70% 절감)
2. **데이터 거버넌스**: PII/PCI-DSS/HIPAA 데이터는 리전 단위 격리, KMS-CMK(고객 관리 키) 사용, BYOK(Bring Your Own Key) HSM 연동 필요 여부 확인
3. **네트워크 토폴로지**: VPC Peering(최대 125개, 전이 불가) vs Transit Gateway(5,000 VPC, 라우팅 중앙화) vs PrivateLink(1:1 단방향, CIDR 충돌 회피) 선택
4. **DR 등급 설정**: RTO/RPO 정의 -> Backup/Restore(수시간, RPO 24h), Pilot Light(분, RPO 수분), Warm Standby(수십분, RPO 수초), Active-Active(0/0, Multi-Region) 중 선택
5. **FinOps 비용 최적화**: Reserved Instance(40~60%v, 1~3년 약정), Savings Plans(66%v, Compute SP), Spot Instance(90%v, 중단 가능), Egress 비용 0.09/GB, S3 Intelligent-Tiering(자동 계층화)

### 피해야 할 안티패턴

- **Egress 비용 폭탄**: 동일 리전 AZ 간 트래픽은 무료, 리전 간 0.02/GB, Cloud->OnPrem는 0.09/GB. NAT Gateway(0.045/h + 0.045/GB) -> VPC Endpoint(0.01/h, 데이터 무료)로 대체 필수
- **단일 AZ 배포**: 가용 영역 장애 시 전체 서비스 중단. ALB+EKS+RDS 모두 Multi-AZ 구성
- **IAM 과대 권한**: AdministratorAccess를 EC2 인스턴스에 부여, Role 기반 최소 권한(MFA, SCP
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 564 / 800

<- **이전**: [563. 클라우드 아키텍처 핵심 토픽 563번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/563_cloud_architecture_core_topic_563_exam_summar/)
**다음**: [565. 클라우드 아키텍처 핵심 토픽 565번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/565_cloud_architecture_core_topic_565_exam_summar/) ->

---
