---
title: "Cloud Architecture Core Topic 754 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/CaaS/PaaS/FaaS/SaaS의 5계층 서비스 모델과 Public/Private/Hybrid/Multi-Cloud의 4계층 배포 모델이 교차하는 매트릭스 위에서, CNCF 정의의 12-Factor App 원칙, 컨테이너 오케스트레이션(Kubernetes), 선언형 IaC(Terraform/CloudFormation), 서비스 메시(Istio/Linkerd), GitOps(ArgoCD/Flux) 5대 핵심 요소를 결합한 **불변 인프라(Immutable Infrastructure)** + **탄력적 분산 시스템** 설계 패러다임이다.
> 2. **가치**: AWS Well-Architected Framework 6대 기둥(운영 우수성/보안/안정성/성능 효율/비용 최적화/지속가능성) 기준으로, CapEx 대비 OpEx 전환율 30~60%, Auto-Scaling을 통한 Peak 자원利用率 70% 이상 달성, MTTR 80% 단축(평균 4시간->45분), 가용성 SLA 99.99%(연 52분 이내 장애) 실현이 가능하며, 이는 전통 3-Tier On-Premise 대비 TCO 3년 누적 40~50% 절감 효과로 정량화된다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) 회피를 위한 **Multi-Cloud/Cloud-Agnostic 추상화**(Terraform+Kubernetes+Crossplane) 적용 여부, Stateless/Microservices 전환 시의 **Distributed Transaction Saga 패턴** vs **Event Sourcing+CQRS** 선택, Zero-Trust 보안 모델 기반의 **BeyondCorp/SPIFFE/SPIRE** 도입 수준, FinOps 기반의 **Showback/Chargeback** 체계 구축이 핵심 의사결정 분기점이다.

---

## Ⅰ. 개요 및 필요성

전통적 3-Tier 온프레미스 아키텍처(웹서버-WAS-DB)는 수직 확장(Scale-Up)의 물리적 한계, 트래픽 변동성에 따른 평균 30% 이하의 낮은 자원利用率, 장애 시 수 시간~수 일의 복구 시간(MTTR), 그리고 CapEx 중심의 무중단 투자 부담이라는 구조적 한계를 가진다. Netflix가 2008년 8월 8일 AWS EC2로의 마이그레이션(Netflix Cloud Migration)을 계기로 본격화된 클라우드 네이티브 아키텍처는, 2013년 Docker, 2014년 Kubernetes(Borg에서 오픈소스화), 2015년 CNCF(Cloud Native Computing Foundation) 설립, 2018년 Istio 1.0 출시, 2020년 GitOps 표준화(ArgoCD/Flux)까지의 기술 진화를 거쳐, 이제는 "Lift & Shift"가 아닌 **Cloud-Native Refactoring** 단계로 패러다임이 전환되었다.

```text
   +-------------------------------------------------------------+
   |         전통 3-Tier On-Premise -> Cloud-Native 전환 흐름     |
   +-------------------------------------------------------------+

   [Stage 1: Lift & Shift]        [Stage 2: Optimize]
   +--------------------+         +--------------------+
   | • 단순 호스팅 이전  |   ->     | • Managed Service  |
   | • IaaS 위에서      |         |   활용 (RDS, S3)   |
   |   OS/MW 그대로     |         | • Auto Scaling     |
   | • CAPEX -> OPEX     |         | • Reserved Inst.   |
   +--------------------+         +--------------------+
            |                              |
            v                              v
   [Stage 3: Refactor]          [Stage 4: Cloud-Native]
   +--------------------+         +--------------------+
   | • Microservices    |   ->     | • K8s + Service    |
   | • 12-Factor App    |         |   Mesh + Serverless|
   | • CI/CD 파이프라인 |         | • GitOps + AIOps  |
   | • IaC (Terraform)  |         | • FinOps + SRE    |
   +--------------------+         +--------------------+

   ※ Gartner Hype Cycle 기준 Stage 4가 'Plateau of Productivity' 도달 단계
```

기존 **Monolithic Architecture**(코드 베이스 단일, 배포 단일, DB 공유)는 **Conway's Law**(시스템 구조는 조직 소통 구조를 반영한다)에 따라 개발팀 규모 50명 초과 시 생산성이 급감하고, 부분 배포·부분 확장이 불가능하여 **"Big Bang Release"** 리스크를 수반한다. 반면 **Microservices Architecture**(Martin Fowler, 2014)는 도메인 경계(Bounded Context)별 독립 배포, Polyglot Persistence, API Gateway/Kafka 기반 비동기 메시징을 통해 **Deployment Frequency**(배포 빈도)를 월 1회->일 수십~수백 회로, **Lead Time for Changes**(변경 반영 시간)를 주 단위->시간 단위로 단축시키는 **DevOps High Performer** 지표(DORA Report 2023 기준 Elite 팀: 배포 빈도 1,460회/년, MTTR 1시간 미만)를 달성 가능하게 한다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **도시의 수도·전기·가스 인프라**와 같다. 각 가정(서비스)이 자체 발전소·정수장을 둘 필요 없이, 도시 중앙 공급망(클라우드)으로부터 필요량만큼 끌어다 쓰는 **Utility Computing** 모델이며, 수요 폭증 시 수도관·송전선을 탄력적으로 확장하는 **탄력성(Elasticity)**이 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 5계층 참조 모델(SP/SaaS -> FaaS -> PaaS -> CaaS -> IaaS)은 **추상화 수준(Abstraction Level)**과 **고객 책임 범위(Shared Responsibility Model)**의 역관계로 정의된다. 상위 계층일수록 비즈니스 로직에 집중할 수 있으나, 런타임·미들웨어·OS에 대한 제어권과 커스터마이징 자유도는 감소한다.

```text
   +----------------------------------------------------------------+
   |              Cloud-Native 4계층 참조 아키텍처 (4+1 View)        |
   +----------------------------------------------------------------+

   [Logical View]                 [Process View]
   +-------------+                +------------------+
   | API Gateway |<---- HTTPS ----| Microservice A   |
   | (Kong/Envoy)|                | (Spring/Go)      |
   +------+------+                +--------+---------+
          |                                |
          v                                v
   +-------------+                +------------------+
   | Service Mesh|                | Event Bus (Kafka)|
   | (Istio mTLS)|<---- mTLS ----| Pub/Sub Topic    |
   +------+------+                +--------+---------+
          |                                |
          v                                v
   [Development View]            [Physical View]
   +------------------+         +----------------------+
   | Container (OCI)  |         | K8s Node Pool (EKS/  |
   | Image: Multi-    |         | GKE/AKS) Multi-AZ    |
   | stage Build      |         | + Spot/On-Dem Mix    |
   +--------+---------+         +----------+-----------+
            |                              |
            v                              v
   +------------------------------------------------+
   |  IaC Layer: Terraform/CloudFormation + Helm    |
   |  + ArgoCD(Continuous Delivery) + Prometheus    |
   +------------------------------------------------+

   [+] Use-Case View: SRE 관점 SLI/SLO/Error Budget
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway (Kong/Amazon API GW/Apigee)** | 외부 클라이언트 진입점, 라우팅·인증·속도제한·변환 | OAuth 2.0/JWT 검증, Rate Limiting(Token Bucket), Circuit Breaker, gRPC-Web 변환, Lambda Authorizer로 커스텀 인증 |
| **Service Mesh (Istio/Linkerd/Consul Connect)** | L7 트래픽 관리, mTLS, 관측성, 정책 | Envoy Sidecar(1Pod 2Container 패턴), xDS API로 동적 설정 분배, **STRICT mTLS** 모드, Telemetry v2(Envoy Filter) 기반 메트릭 수집 |
| **Container Orchestrator (Kubernetes/EKS/GKE/AKS)** | 컨테이너 스케줄링, 자가치유, 선언적 상태 관리 | Control Plane(API Server/etcd/scheduler) + Data Plane(kubelet/kube-proxy), **Reconciliation Loop**(현재 상태->Desired State 수렴), HPA/VPA/Cluster Autoscaler 3단계 오토스케일링 |
| **CI/CD & GitOps (Jenkins/ArgoCD/Flux/Tekton)** | 빌드·테스트·배포 자동화, Git을 Single Source of Truth로 | **Pull-based 배포**(ArgoCD 5분 동기화 주기), Progressive Delivery(Argo Rollouts: Blue/Green, Canary, Analysis Template), SBOM(Syft/Grype) 기반 보안 검증 |

### 핵심 메커니즘 상세

**1) 선언적 인프라(IaC) 및 Reconciliation Loop**
Kubernetes의 핵심은 **Desired State(원하는 상태)**를 YAML 매니페스트로 선언하면, Control Plane이 **Reconciliation Loop**를 통해 Current State를 Desired State로 수렴시키는 것이다. 이때 `etcd`는 분산 Key-Value 저장소로 **Raft 합의 알고리즘**(Quorum = ⌊N/2⌋+1)을 통해 강한 일관성(Strong Consistency)을 보장하며, 모든 클러스터 상태의 Single Source of Truth 역할을 수행한다. Terraform은 HCL(HashiCorp Configuration Language)로 멀티 클라우드 리소스를 선언하며, **State File**(terraform.tfstate)에 실제 인프라 상태를 저장하여 Plan/Diff 기반의 안전한 변경을 가능케 한다.

**2) 탄력성(Elasticity) 구현 메커니즘**
- **HPA(Horizontal Pod Autoscaler)**: CPU/Memory/RPS/외부 메트릭(Prometheus Adapter) 기반 Pod 수량 조정. `kube_metrics_server`가 15초 주기 메트릭 수집
- **VPA(Vertical Pod Autoscaler)**: Pod별 리소스 Request/Limit 재추정. `recommender`가 1일 주기 과거 데이터 분석
- **Cluster Autoscaler(CA)/Karpenter**: Pending Pod 발생 시 Node Pool 확장. **Karpenter**(AWS, 2021 출시)는 Launch Template 없이 Spot/On-Demand를 30초 내 프로비저닝하며, **Consolidation** 기능으로 미사용 Node를 자동 정리
- **HPA + Cluster Autoscaler + Spot Instance** 조합으로 **Cost-Performance Optimal** 구성 달성

**3) 12-Factor App 원칙 (Heroku, 2011)**
① Codebase(단일 코드베이스, 다중 배포), ② Dependencies(명시적 선언), ③ Config(환경변수 분리), ④ Backing Services(리소스를 Attached Resource로 취급), ⑤ Build/Release/Run(완전 분리), ⑥ Processes(Stateless), ⑦ Port Binding(자체 포트), ⑧ Concurrency(프로세스 모델), ⑨ Disposability(빠른 시작/종료), ⑩ Dev/Prod Parity(환경 일치), ⑪ Logs(Stdout 이벤트 스트림), ⑫ Admin Processes(일회성 관리 작업). 이를 모두 준수하면 **Cloud-Native** 등급 인증 가능.

**4) 가용성 및 재해복구(DR) 패턴**
- **Multi-AZ(Multi Availability Zone)**: AZ 간 Latency 1~3ms, AWS 기준 단일 리전 내 99.99% SLA
- **Multi-Region Active-Active**: 글로벌 트래픽 라우팅(AWS Route 53 Latency-Based/Geolocation), DynamoDB Global Tables로 Multi-Master 복제
- **DR 전략 4단계**: Backup/Restore(RPO: 24h, RTO: 24h) -> Pilot Light(RPO: 분 단위, RTO: 수 시간) -> Warm Standby(RPO: 초 단위, RTO: 분 단위) -> Multi-Site Active-Active(RPO: 0, RTO: 0). 금융사 등 규제 업종은 RPO 0, RTO 1시간 이내 요구

- **📢 섹션 요약 비유**: K8s의 **Reconciliation Loop**는 마치 **자동 온도조절 에어컨**과 같다. 사용자가 24°C를 설정(Desired State)하면, 온도 센서가 현재 28°C(Current State)를 감지하고, **반복적으로** 냉방을 가동해 24°C에 도달할 때까지 계속 비교·조정한다. 이때 사용자는 "어떻게 식힐 것인가"의 명령(Imperative)이 아닌, "24°C를 유지하라"는 선언(Declarative)만 내린다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처의 핵심 의사결정 분기점인 **Service Model**과 **Deployment Model**을 비교하고, 유사·대체 개념과의 관계를 정리한다.

| 구분 | **IaaS** (Infrastructure-as-a-Service) | **PaaS** (Platform-as-a-Service) | **FaaS** (Function-as-a-Service) | **SaaS** (Software-as-a-Service) |
| :--- | :--- | :--- | :--- | :--- |
| **추상화 수준** | VM, Storage, Network | Runtime, Middleware, OS | 함수 코드 단위 | 완전 애플리케이션 |
| **고객 관리 범위** | App + Data + Runtime + OS까지 | App + Data | 코드 + 트리거 | 사용/설정만 |
| **프로비저닝 시간** | 분~시간 | 초~분 | 밀리초(콜드 스타트) | 즉시(설정만) |
| **확장 단위** | VM 단위 | 컨테이너/앱 단위 | 동시 실행 수 단위(Concurrency) | 사용자/테넌트 단위 |
| **대표 서비스** | AWS EC2, Azure VM, GCP Compute Engine | AWS Elastic Beanstalk, Heroku, Google App Engine | AWS Lambda, Azure Functions, GCP Cloud Functions | Salesforce, Microsoft 365, Slack |
| **과금 모델** | 시간/초 단위 (On-Demand/Reserved) | 인스턴스/요청 단위 | GB-초 + 호출 횟수 | 사용자/월 구독 |
| **적합 시나리오** | 레거시 Lift&Shift, 특수 HW 요구 | 웹앱 빠른 출시, 표준 스택 | Event-driven, 간헐적 워크로드 | 표준 업무(메일, CRM, 협업) |
| **제약 사항** | 운영 부담 큼 | 벤더 종속성 높음 | 콜드 스타트, 실행 시간 한도(15분), Stateless 강제 | 커스터마이징 한계 |

**주요 하이퍼스케일러 비교(AWS vs Azure vs GCP, 2024 기준)**

| 평가 항목 | AWS | Azure | GCP |
| :--- | :--- | :--- | :--- |
| 시장 점유률(Q4 2024 Synergy) | 31% | 24% | 11% |
| 최대 강점 | 서비스 폭·깊이(200+), 성숙 생태계 | MS Hybrid(AD/Office), 엔터프라이즈 통합 | AI/ML(Vertex AI, BigQuery), 네트워킹 |
| 컴퓨팅 | EC2(750+ 인스턴스 타입), Graviton3 ARM | VM Series(M-series), HBv
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 754 / 800

<- **이전**: [753. 클라우드 아키텍처 핵심 토픽 753번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/753_cloud_architecture_core_topic_753_exam_summar/)
**다음**: [755. 클라우드 아키텍처 핵심 토픽 755번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/755_cloud_architecture_core_topic_755_exam_summar/) ->

---
