---
title: "Cloud Architecture Core Topic 797 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 CAP Theorem(Consistency, Availability, Partition tolerance)과 12-Factor App 원칙을 기반으로, IaaS/PaaS/SaaS 계층, 컨트롤 플레인/데이터 플레인 분리, 제어 루프(Control Loop) 기반 선언적 인프라(Kubernetes, Terraform)를 통해 탄력성(Elasticity)과 회복탄력성(Resilience)을 코드와 정책으로 보장하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: AWS Well-Architected Framework 6대 기둥(Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability)을 적용 시, 자본 지출(CapEx) 대비 운영 지출(OpEx) 전환으로 TCO 30~60% 절감, Auto Scaling을 통한 리소스 활용률 70% 이상 달성, MTTR(Mean Time To Recovery) 90% 단축, 가용성 99.99%(Four 9s) 달성이 가능하다.
> 3. **판단 포인트**: 핵심 트레이드오프는 (1) Strong Consistency vs Eventual Consistency (DynamoDB의 R+W>N vs Cassandra의 Tunable Consistency), (2) Monolith vs Microservices (배포 독립성 vs 분산 트랜잭션 복잡도), (3) Lift & Shift vs Cloud-Native Refactoring (마이그레이션 속도 vs 장기 TCO), (4) Single Cloud vs Multi-Cloud (벤더 종속성 vs 네트워크 지연·비용 증가)이며, 워크로드 특성(OLTP/OLAP, Batch/Streaming)과 RTO/RPO, 컴플라이언스 요건에 따라 아키텍처 결정이 분기된다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 데이터센터는 정적 용량 계획(Static Capacity Planning), 수직 확장(Scale-Up), CAPEX 중심의 Capex 모델, 그리고 3-tier 아키텍처(Presentation/Business/Data Layer) 기반의 Monolithic 애플리케이션이 지배적이었다. 이러한 패러다임은 (1) 프로비저닝 리드타임 4~12주, (2) 평균 리소스 활용률 12~18% (McKinsey 보고서), (3) DR(Disaster Recovery) 구성 비용의 2배 이중화 투자, (4) 기술 부채(Technical Debt) 누적이라는 구조적 한계를 가졌다.

클라우드 아키텍처는 이러한 한계를 극복하기 위해 **가상화(Hypervisor: KVM/Xen/Hyper-V) -> 컨테이너(Docker/runc) -> 오케스트레이션(Kubernetes/ECS) -> 서버리스(Lambda/Functions) -> 분산 애플리케이션(Service Mesh: Istio/Linkerd)**로 진화해 왔다. 핵심 패러다임 전환은 "Infrastructure as Code(IaC)", "Immutable Infrastructure", "Pet vs Cattle Server", "Conway-Mel定律에 따른 팀 토폴로지(Team Topologies)"다.

NIST SP 800-145는 클라우드를 5대 특성(On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)과 3대 서비스 모델(IaaS/PaaS/SaaS), 4대 배포 모델(Public/Private/Hybrid/Community)으로 정의하며, 이는 클라우드 아키텍처 설계의 기본 어휘집(Vocabulary)이다.

```text
+---------------------------------------------------------------------+
|              클라우드 아키텍처 패러다임 진화 (Evolution)             |
+---------------------------------------------------------------------+
|                                                                     |
|  [On-Premise]        [Virtualization]      [IaaS Cloud]             |
|   Physical            VMware/Hyper-V         EC2/Compute Engine      |
|   +------+           +------+              +------+                |
|   | App  |           |  VM  |              |  VM  |                |
|   |  OS  |           | Guest|              |  OS  |                |
|   | Hyper|  ----►    |  OS  |  ----►       | Guest|  ----►         |
|   | H/W  |           | Hyper|              |  OS  |                |
|   +------+           +------+              |Hyper(Hidden)|        |
|                                             +------+                |
|  TTM: 12weeks       TTM: 1-2 weeks         TTM: minutes            |
|  Utilization: 15%   Utilization: 35%        Utilization: 60%        |
|                                                                     |
|  [PaaS/Container]   [Cloud-Native]        [Serverless/Mesh]         |
|   Kubernetes         Service Mesh          Lambda/Edge              |
|   +------+           +------+              +------+                |
|   | Pod  |           |Sidecar|             | Fn   |                |
|   | Cnt  |  ----►    |Proxy |  ----►       |(ephemeral)|           |
|   |  K8s |           |Istio |              | Event|                |
|   +------+           +------+              +------+                |
|  TTM: hours         TTM: minutes          TTM: ms                  |
|  Utilization: 70%   Utilization: 80%       Utilization: 95%        |
|                                                                     |
|  ※ TTM = Time-To-Market, Utilization = 평균 리소스 활용률           |
+---------------------------------------------------------------------+
```

**기존 vs 신규 패러다임 비교:**

| 차원 | On-Premise (전통) | Cloud-Native (신규) |
| :--- | :--- | :--- |
| 용량 계획 | Peak 기반 과잉 설계 (Over-Provisioning) | Elasticity 기반 동적 확장 (Pay-per-Use) |
| 장애 대응 | HA Pair + Cold Standby | Multi-AZ, Multi-Region, Chaos Engineering |
| 배포 방식 | 수동 배포, 야간 작업 | GitOps, Canary/Blue-Green, Progressive Delivery |
| 트래픽 패턴 | 예측 가능 (Predictable) | 버스트성 (Bursty), Exponential |
| 비용 모델 | CapEx (감가상각) | OpEx (사용량 기반 종량제) |
| 기술 부채 | 3~5년 갱신 주기 | Continuously Refactored |

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **"수도 요금제"**와 같다. 정수기처럼 한 번 큰 돈(전용선, 서버실)을 들이는 대신, 사용한 만큼만(Compute Time, GB-Transfer) 요금을 내며, 여름 한여름 에어컨을 틀면 자동으로 수압이 올라가듯(Auto Scaling), 폭증하는 트래픽에 인프라가 자동 반응한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **계층화된 책임 분담 모델(Shared Responsibility Model)**과 **선언적 API(Declarative API)**이다. 클라우드 제공자(CSP)는 인프라 계층(물리, 네트워크, 스토리지, 가상화)의 보안을 책임지고, 고객은 그 위의 데이터, OS, 미들웨어, 애플리케이션 보안을 책임진다. AWS, Azure, GCP 모두 이 모델을 채택하며, 서비스 종류에 따라 책임 범위가 달라진다(IaaS에서는 OS까지 고객, PaaS에서는 런타임까지 CSP, SaaS에서는 애플리케이션 설정만 고객).

```text
+----------------------------------------------------------------------+
|       클라우드 네이티브 아키텍처 4+1 Layer Reference Model            |
+----------------------------------------------------------------------+
|                                                                      |
|  +---------------------------------------------------------------+  |
|  |  [Layer 4] Application & Business Logic Layer                 |  |
|  |   +- Microservices (Spring Boot, Go-kit, gRPC)                |  |
|  |   +- API Gateway (Kong, AWS API GW, Apigee)                   |  |
|  |   +- BFF (Backend For Frontend) Pattern                       |  |
|  |   +- Event-Driven (Kafka, EventBridge, Pub/Sub)               |  |
|  +---------------------------------------------------------------+  |
|                              |                                       |
|  +---------------------------------------------------------------+  |
|  |  [Layer 3] Data Plane / Application Runtime                    |  |
|  |   +- Service Mesh (Istio, Linkerd, Consul Connect)             |  |
|  |   +- Sidecar Proxy (Envoy, eBPF Data Plane)                   |  |
|  |   +- mTLS, Circuit Breaker, Retry, Timeout Policy             |  |
|  |   +- Distributed Tracing (OpenTelemetry, Jaeger, Zipkin)      |  |
|  +---------------------------------------------------------------+  |
|                              |                                       |
|  +---------------------------------------------------------------+  |
|  |  [Layer 2] Orchestration & Scheduling Plane                   |  |
|  |   +- Kubernetes Control Loop (Reconcile: Desired vs Actual)   |  |
|  |   +- etcd (Distributed KV-Store, Raft Consensus)              |  |
|  |   +- Operator Pattern (CRD + Controller)                      |  |
|  |   +- GitOps (ArgoCD, Flux, Argo Rollouts)                     |  |
|  +---------------------------------------------------------------+  |
|                              |                                       |
|  +---------------------------------------------------------------+  |
|  |  [Layer 1] Infrastructure & Provisioning Layer                |  |
|  |   +- IaC (Terraform HCL, AWS CDK, Pulumi, Crossplane)         |  |
|  |   +- Immutable Image (Packer, AMI, Golden Image)               |  |
|  |   +- Network (VPC, Subnet CIDR, Transit Gateway, SD-WAN)      |  |
|  |   +- Security (IAM, KMS, HSM, Secrets Manager, WAF)           |  |
|  +---------------------------------------------------------------+  |
|                                                                      |
|  +---------------------------------------------------------------+  |
|  |  [+] Cross-Cutting Concerns (횡단 관심사)                      |  |
|  |   Observability(3-pillars) | Security(Zero-Trust) | CI/CD      |  |
|  |   Policy-as-Code(OPA) | Cost FinOps | Sustainability          |  |
|  +---------------------------------------------------------------+  |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway** | 외부 요청의 단일 진입점(Single Entry Point) | Rate Limiting(Token Bucket), OAuth2/JWT 검증, Request Transformation, GraphQL/REST/gRPC 통합, OpenAPI/Swagger 기반 계약(Contract) |
| **Service Mesh** | 서비스 간 통신의 Infra-layer 추상화 | Sidecar Pattern(Envoy), mTLS(Istiod가 SPIFFE ID 발급), 7-Layer Traffic Management(VirtualService), Chaos Injection(Chaos Mesh) |
| **Kubernetes Controller** | 선언적 상태(Desired State) 보장 | Reconcile Loop: `read state -> diff -> patch`, Event-Driven(Watch API), Level-Trigger(Edge-Triggered X), Optimistic Concurrency(resourceVersion) |
| **Distributed Storage** | 데이터의 가용성·내구성·일관성 보장 | CAP/PACELC Trade-off, Consistent Hashing(Ring Topology), Merkle Tree Anti-Entropy, Vector Clock(Causality), LSM-Tree(Write-Heavy) |
| **Observability Stack** | 시스템 상태의 가시성 확보 | **Metrics**(Prometheus, M3, VictoriaMetrics) + **Logs**(Loki, ELK, OpenSearch) + **Traces**(Tempo, Jaeger, Honeycomb) — 3 Pillars 통합 |

**Kubernetes 핵심 제어 루프 원리 (Reconciliation Loop):**

```text
[클라이언트: kubectl apply]
        |
        v
[1] AuthN/AuthZ (RBAC: Role/RoleBinding)
        |
        v
[2] Admission Control (MutatingWebhook, ValidatingWebhook, OPA Gatekeeper)
        |
        v
[3] etcd 저장 (Spec.PodTemplate.Replicas=3 -> write index 5)
        |
        v
[4] Controller Watch (Informer Cache, Resync Period 10~30m)
        |
        v
[5] Diff 계산: Actual(현재 2개) vs Desired(목표 3개) = 1개 부족
        |
        v
[6] Reconcile -> API Server -> Scheduler(kube-scheduler) -> kubelet -> CRI
        |
        v
[7] Status Update (etcd, index 6) -> Client-Go SharedInformer broadcast
        |
        v
[8] backoff: RateLimitQueue, WorkQueue with Exponential Backoff
```

**12-Factor App 핵심 원리 (Cloud-Native App 설계 원칙):**

1. **Codebase**: 단일 저장소, 다중 배포 (One Repo, Many Deploys)
2. **Dependencies**: 명시적 의존성 선언 (requirements.txt, go.mod)
3. **Config**: 환경변수 주입 (12가지 원칙 중 가장 자주 위반)
4. **Backing Services**: 약결합(Loose Coupling) — DB/SMTP를 Attach된 Resource로 취급
5. **Build, Release, Run**: 세 단계 엄격 분리 (Immutable Release)
6. **Processes**: Stateless 프로세스, 세션은 Redis/Sticky Session
7. **Port Binding**: 자체 HTTP 포트 노출 (WAR 컨테이너 X)
8. **Concurrency**: 프로세스 모델로 확장 (HPA: Horizontal Pod Autoscaler)
9. **Disposability**: 빠른 시작(≤10s),优雅 종료(SIGTERM, preStop Hook)
10. **Dev/Prod Parity**: 환경 일치 (Docker Image Tag = Git SHA)
11. **Logs**: Event Stream (stdout/stderr) — Fluent Bit -> Loki
12. **Admin Processes**: 일회성 작업도 동일한 환경에서 (kubectl job, aws-cli in container)

- **📢 섹션 요약 비유**: 클라우드 네이티브 아키텍처는 **"자율주행 자동차"**와 같다. 센서(Observability)가 도로 상황(시스템 상태)을 감지하고, AI Controller(K8s Controller)가 핸들과 액셀러레이터를 자동으로 조작하며, GPS(IaC)는 항상 최적 경로(Desired State)로 차량을 안내한다. 운전자는 목적지만 말하면 된다(선언적 API).

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처의 의사결정에는 다수의 트레이드오프가 존재한다. 실무 기술사 시험에서는 **"왜 이 기술을 선택했는가"**에 대한 정량적 근거와 제약 조건 분석이 핵심 평가 요소다.

| 구분 | IaaS (EC2/GCE/Azure VM) | PaaS (EKS/Cloud Run/Beanstalk) | SaaS (Salesforce/Workday/Slack) | Serverless (Lambda/Cloud Functions) |
| :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | App + Runtime + OS | App + Data | 사용 (Configuration only) | 함수 코드 only |
| **확장 단위** | VM Instance | Container / Pod | 자동 (CSP 전담) | 동시 실행 수(Concurrency) |
| **Cold Start** | 없음 (수 초 부팅) | 컨테이너 이미지 Pull (5~30s) | 없음 | 100ms~3s (VPC 통합 시 ^) |
| **최대 실행 시간** | 무제한 | 무제한 (Pod는) | 무제한 | 15분 (AWS Lambda 한도) |
| **State 관리** | 자유 | 자유 (EBS/PV 지원) | CSP 종속 | Stateless 강제 (Step Functions로 보완) |
| **TCO** | 중간 (인력 ^) | 낮음 (효율 ^) | 최고 (벤더 종속 v) | 매우 낮음 (유휴 0원) |
| **적합 워크로드** | 레거시, HPC, Stateful DB | 일반 웹, MSA, AI 추론 | 정형 비즈니스 (CRM, HR) | 이벤트 처리, Cron, Webhook |

| 구분 | Monolith (모놀리식) | Microservices (마이크로서비스) |
| :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/JAR (수 GB) | 컨테이너 이미지 (수십~수백 MB) |
| **장애 격리** | 1개 버그 -> 전체 다운 | Service별 Circuit Breaker, Bulkhead |
| **팀 구조** | Conway's
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 797 / 800

<- **이전**: [796. 클라우드 아키텍처 핵심 토픽 796번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/796_cloud_architecture_core_topic_796_exam_summar/)
**다음**: [798. 클라우드 아키텍처 핵심 토픽 798번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/798_cloud_architecture_core_topic_798_exam_summar/) ->

---
