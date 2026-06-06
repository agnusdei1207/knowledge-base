---
title: "Cloud Architecture Core Topic 631 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS·PaaS·SaaS·FaaS의 서비스 모델 계층과 Public·Private·Hybrid·Multi-Cloud의 배치 모델을 기반으로, 컨테이너 오케스트레이션(Kubernetes), IaC(Terraform/CloudFormation), 마이크로서비스, 서버리스, 메시 서비스망(Istio/Linkerd)을 결합해 **탄력성(Elasticity)·가용성(HA)·확장성(Scalability)·비용 최적화(FiNOps)**를 동시에 달성하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: AWS·Azure·GCP의 글로벌 리전(60+ 리전, 200+ AZ)을 활용 시 평균 가용성 99.99%(SLA 4-nine) 확보, Auto Scaling으로 트래픽 피크 대비 70% 비용 절감, MTTR을 기존 4시간에서 15분 이내로 단축, CAPEX->OPEX 전환으로 초기 인프라 투자비 60% 이상 절감 효과가 검증되어 있다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) 회피를 위한 **추상화 계층(Abstraction Layer) 설계 여부**, 12-Factor App 준수 여부, Stateless 워크로드와 Stateful 워크로드의 분리 기준, 데이터 중력(Data Gravity) 및 송신 비용(Egress Cost) 관리, Well-Architected Framework 5대 축(운영 우수성·보안·신뢰성·성능 효율·비용 최적화) 트레이드오프가 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 아키텍처는 CAPEX(자본 지출) 중심의 수직적 확장(Scale-Up) 방식으로, 트래픽 피크 예측 기반으로 3~5년 주기 하드웨어 갱신, IDC 전력·냉각·공간 제약, 장애 시 MTTR 평균 4시간 이상, 프로비저닝 소요 시간 수일~수주의 한계를 가졌다. 2006년 AWS S3·EC2 출시 이후 클라우드 컴퓨팅은 API 기반의 프로그래머블 인프라스트럭처, 사용량 기반 과금(Pay-Per-Use), 셀프서비스 프로비저닝, 무한 확장성(Infinite Scalability)을 제공하며 IT 인프라 패러다임을 근본적으로 전환시켰다.

NIST SP 800-145는 클라우드를 "네트워크, 서버, 스토리지, 애플리케이션, 서비스 등 구성 가능한 컴퓨팅 자원의 공유 풀에 어디서나 편리하고 주문형으로 네트워크 접근을 가능하게 하는 모델"로 정의하며, 5대 핵심 특성(필수 특성 4 + 일반 특성 1)인 **온디맨드 셀프서비스, 광범위 네트워크 접근, 자원 풀링, 빠른 탄력성, 측정 가능한 서비스**를 명시한다.

```text
+---------------------------------------------------------------------+
|              클라우드 컴퓨팅 패러다임 전환 (On-Prem -> Cloud)         |
+---------------------------------------------------------------------+
|                                                                     |
|   [On-Premise Era]              [Cloud-Native Era]                  |
|   +--------------+              +--------------------------+        |
|   |  Application |              |  Microservices + Serverless|     |
|   +--------------+              +--------------------------+        |
|   |  Middleware  |              |  Container (K8s)         |        |
|   +--------------+              +--------------------------+        |
|   |  OS          |   -------►   |  PaaS (Beanstalk, AKS)  |        |
|   +--------------+              +--------------------------+        |
|   |  Virt.       |              |  IaaS (EC2, Compute)    |        |
|   +--------------+              +--------------------------+        |
|   |  Server      |              |  Region / AZ / Edge     |        |
|   +--------------+              +--------------------------+        |
|   |  Storage     |              |  Object/S3, EBS, EFS     |        |
|   +--------------+              +--------------------------+        |
|   |  Network     |              |  VPC, TGW, CloudFront   |        |
|   +--------------+              +--------------------------+        |
|                                                                     |
|   특징:  CAPEX 중심, 수직확장, 수동운영,                  |                       |
|         3-5년 갱신주기, IDC 의존        |  특징: OPEX 중심, 수평확장, IaC,    |
|                                |  Self-Service, Global, Auto-Scaling |
+---------------------------------------------------------------------+
```

클라우드 도입의 핵심 동인은 ① **비용 효율성**(유휴 자원 제거, TCO 30~70% 절감), ② **비즈니스 민첩성**(프로비저닝 시간 수주->수분), ③ **글로벌 확장성**(멀티 리전 배포로 지연시간 200ms->50ms 이하), ④ **고가용성**(멀티 AZ·리전 배포로 99.99% SLA), ⑤ **기술 민주화**(AI/ML·양자컴퓨팅·블록체인 서비스를 클릭 한 번으로 도입)이다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"전기 자가발전에서 중앙 전력망으로의 전환"**과 같다. 자체 발전소(온프레미스 IDC)는 초기 설치비는 적지만 수요 피크에 맞춰 과잉 건설해야 하고 유지보수에 인력이 필요하다. 중앙 전력망(퍼블릭 클라우드)은 사용한 만큼만 비용을 지불하고, 전력 품질(SLA)이 검증되어 있으며, 신재생 에너지(최신 AI/ML 서비스)도 즉시 연결 가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **5계층 참조 모델**(응용·데이터·런타임·미들웨어·인프라)과 **3가지 책임 공유 모델**(CSP·고객·공동 책임)을 기반으로 한다. AWS Well-Architected Framework는 이를 5대 기둥(운영 우수성, 보안, 신뢰성, 성능 효율, 비용 최적화) + 6번째 기둥(지속가능성, 2021년 추가)으로 재구성한다.

```text
+--------------------------------------------------------------------------+
|           클라우드 네이티브 아키텍처 참조 모델 (CNCF Landscape 기반)       |
+--------------------------------------------------------------------------+
|                                                                          |
|  +----------------------------------------------------------------+     |
|  | [Layer 5] Application & API Layer                              |     |
|  |  - Microservice, API Gateway (Kong, Apigee, AWS API GW)       |     |
|  |  - Service Mesh (Istio, Linkerd, App Mesh)                     |     |
|  |  - Event-Driven (Kafka, EventBridge, Pub/Sub)                  |     |
|  +----------------------------------------------------------------+     |
|                              ^                                          |
|  +----------------------------------------------------------------+     |
|  | [Layer 4] Orchestration & Scheduling                            |     |
|  |  - Kubernetes (EKS, AKS, GKE), Nomad                          |     |
|  |  - Helm, Kustomize, ArgoCD/Flux (GitOps)                       |     |
|  |  - Service Discovery (CoreDNS, Consul)                         |     |
|  +----------------------------------------------------------------+     |
|                              ^                                          |
|  +----------------------------------------------------------------+     |
|  | [Layer 3] Runtime & Container                                   |     |
|  |  - Docker, containerd, CRI-O, gVisor, KataContainer            |     |
|  |  - FaaS Runtime (Firecracker, Lambda, CloudRun)                |     |
|  +----------------------------------------------------------------+     |
|                              ^                                          |
|  +----------------------------------------------------------------+     |
|  | [Layer 2] Infrastructure as Code (IaC)                          |     |
|  |  - Terraform, Pulumi, AWS CloudFormation, CDK                  |     |
|  |  - Configuration: Ansible, Chef, Puppet                         |     |
|  +----------------------------------------------------------------+     |
|                              ^                                          |
|  +----------------------------------------------------------------+     |
|  | [Layer 1] Cloud Infrastructure (IaaS)                          |     |
|  |  - Compute: EC2, VM, Bare Metal, GPU/TPU                       |     |
|  |  - Storage: S3(Object), EBS(Block), EFS(Shared File)           |     |
|  |  - Network: VPC, Subnet, TGW, DX, LB, CDN                      |     |
|  |  - Region(60+) / AZ(200+) / Edge Location(400+)                |     |
|  +----------------------------------------------------------------+     |
|                                                                          |
|  [Cross-Cutting Concerns] Observability(Logs/Metrics/Traces),           |
|  Security(IAM, KMS, WAF, Zero Trust), CI/CD(GitHub Actions, Argo)       |
+--------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 서비스** | 워크로드 실행 환경 제공 | EC2(x86·ARM/Graviton), Lambda(128MB~10GB, 15분), Fargate(EKS/ECS의 서버리스 컨테이너), Cloud Run(GCP), Azure Functions. **인스턴스 패밀리**(M:범용, C:컴퓨트, R:메모리, X:DB, P/G:AI/ML, I:스토리지) 선택이 비용·성능 결정. |
| **스토리지 서비스** | 데이터 영속성·내구성·접근 패턴 | S3(객체, 11 9s 내구성, 99.99% 가용성), EBS(블록, gp3: 16K IOPS/1GB·s), EFS(NFS, 페타바이트급 공유 파일), Glacier(아카이빙, $0.00099/GB/월), DynamoDB(키-값, 1자리수 ms p99), Aurora(MySQL/PostgreSQL 호환, 5× MySQL, 3× PostgreSQL 성능). |
| **네트워크 서비스** | 연결성·격리·트래픽 제어 | VPC(논리적 격리, /16~28 서브넷), TGW(리전 간 허브), Direct Connect/VPN(전용선), ALB(L7, WAF 통합), NLB(L4, 초저지연), CloudFront/Cloud CDN(엣지 캐싱, 400+ PoP), Route 53(GeoDNS, Latency-Based, Health Check). |
| **관리·자동화** | 프로비저닝·모니터링·거버넌스 | CloudFormation/Terraform(선언적 IaC), CloudWatch/Prometheus/Grafana(관측 가능성), AWS Config/CloudTrail(감사), Organizations SCP(계정 거버넌스), Service Catalog(셀프서비스 카탈로그). |
| **보안·컴플라이언스** | 신원·데이터·네트워크 보안 | IAM(RBAC/ABAC), KMS/HSM(Envelope Encryption), Secrets Manager/Parameter Store, GuardDuty(위협 탐지), WAF/Shield(DDoS), Macie(데이터 분류), Cloud HSM(FIPS 140-2 L3), 책임 공유 모델(고객이 OS 위·데이터·IAM, CSP가 하드웨어·물리 보안 담당). |

**확장성 알고리즘 핵심 수식**:
- **수평 확장 시 용량 모델**: `C(n) = n × Ci + (n-1) × Cs + Cf` (Ci:인스턴스 용량, Cs:조정 오버헤드, Cf:고정 비용)
- **Little's Law** (큐잉 이론): `L = λ × W` (평균 동시 요청 수 = 도착률 × 평균 체류 시간). 이를 Auto Scaling 정책의 Target Tracking(`RequestCountPerTarget = 1000`)에 적용.
- **HPA(Horizontal Pod Autoscaler) 알고리즘**: `desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]`
- **Karpenter**(2021 GA): 노드 프로비저닝 시간 2분->15초, 빈 노드 자동 통합(Consolidation), Spot·On-Demand 혼합으로 비용 70% 절감.

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 5계층은 **"현대식 호텔의 운영 체계"**와 같다. 1층 인프라(건물·전기·수도), 2층 IaC(자동 청소·환기 시스템), 3층 컨테이너 런타임(각종 객실 규격), 4층 오케스트레이션(프런트 데스크의 예약·배정 시스템), 5층 응용(룸서비스·컨시어지)이 서로 협력하며, 손님(요청)이 몰리면 즉시 다이닝 룸(추가 Pod)을 배정하고 한가해지면 닫아 비용을 절약한다.

---

## Ⅲ. 비교 및 연결

| 구분 | IaaS (예: EC2) | PaaS (예: Beanstalk, AKS) | SaaS (예: Office 365, Slack) | FaaS (예: Lambda) |
| :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | 앱·데이터·런타임·미들웨어·OS | 앱·데이터 | 사용만 (설정 포함) | 함수 코드·이벤트 매핑 |
| **제어 수준** | 높음 (OS 커널 접근) | 중간 (런타임 선택 가능) | 낮음 (구성만) | 극히 낮음 (Cold Start 제약) |
| **확장성** | 수동/Auto Scaling Group | 컨테이너 오토스케일 | 자동 (CSP 관리) | 자동 (밀리초 단위 0->1000) |
| **과금 단위** | 인스턴스 시간 | 컨테이너/노드 시간 | 사용자/월 | 요청 수 × 실행 시간(ms/GB) |
| **적합 워크로드** | 레거시, 커스텀 미들웨어, 라이선스 제약 | 마이크로서비스, API, 웹앱 | 이메일, 협업, CRM | 이벤트 처리, ETL, Webhook, 스케줄러 |
| **예시 비용** | m5.large: $0.096/시간 | EKS: $0.10/시간 + 노드 | Slack: $12.5/사용자/월 | Lambda: $0.20/100만 요청 |

**Private Cloud vs Public Cloud vs Hybrid vs Multi-Cloud 비교**:

| 구분 | Public Cloud | Private Cloud | Hybrid Cloud | Multi-Cloud |
| :--- | :--- | :--- | :--- | :--- |
| **소유권** | CSP (AWS/Azure/GCP) | 자체 (OpenStack, VMware) | 둘의 결합 | 2개 이상 CSP |
| **컴플라이언스** | 글로벌 표준 (ISO27001, SOC2) | 완전 통제 (금융·공공 요건) | 데이터 분류 기반 분리 | 워크로드별 최적 CSP |
| **확장성** | 무제한 | 물리적 제약 | 버스트 가능 | 무제한 (이식성 필요) |
| **TCO** | OPEX, 초기 비용 0 | CAPEX 1억+ | 양쪽 모두 | CSP별 종속 비용 |
| **Lock-in 위험** | 높음 | 없음 (오픈소스) | 중간 | 분산 종속 |
| **대표 아키텍처** | Single Cloud Native | On-Prem + OpenStack | AWS Outposts, Azure Stack | EKS Anywhere + AKS + GKE |

**기존 분산 시스템과의 연결**:
- **REST API + GraphQL**: 마
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 631 / 800

<- **이전**: [630. 클라우드 아키텍처 핵심 토픽 630번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/630_cloud_architecture_core_topic_630_exam_summar/)
**다음**: [632. 클라우드 아키텍처 핵심 토픽 632번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/632_cloud_architecture_core_topic_632_exam_summar/) ->

---
