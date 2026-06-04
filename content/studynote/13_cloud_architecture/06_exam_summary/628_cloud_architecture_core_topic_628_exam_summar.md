---
title: "628. 클라우드 아키텍처 핵심 토픽 628번 시험 요약 (Cloud Architecture Core Topic 628 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 API 기반의 탄력적 컴퓨팅 자원 추상화(IaaS/PaaS/SaaS/FaaS)를 통해, CNCF(Cloud Native Computing Foundation) 표준 12-Factor App 원칙과 Kubernetes 오케스트레이션을 중심으로 컨테이너·서비스 메시·관측가능성(Observability)·GitOps를 결합한 **Cloud Native** 패러다임으로 진화했다.
> 2. **가치**: AWS Well-Architected Framework 6대 필러(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속 가능성) 기준, 인프라 프로비저닝 시간 99% 단축(수 주 -> 수 분), Auto-Scaling을 통한 트래픽 변동 대응(평균 70% 비용 절감), MTBF 10배 향상, 그리고 Time-to-Market 60~80% 단축 효과를 달성한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **일관성(Consistency) vs 가용성(Availability)** (CAP Theorem), **밀결합(Monolith) vs 분산결합(Microservices)** 의 운영 복잡도, **Lift-and-Shift vs Cloud-Native Refactoring**의 마이그레이션 전략, 그리고 **단일 클라우드(Vendor Lock-in) vs 멀티클라우드(상호운용성 비용)** 의사결정이며, 기술사적 판단에는 SLA 99.99%(Four 9s) 달성을 위한 Multi-AZ/Region 설계와 RPO/RTO 정의가 필수다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 아키텍처는 **수직 확장(Scale-Up)** 방식의 고가용 HW, 정적 Capacity Plan, 수동 배포·모니터링, 그리고 CAPEX(자본 지출) 중심의 비즈니스 모델이라는 한계를 가진다. 2006년 AWS S3·EC2 출시 이후 시작된 클라우드 컴퓨팅은 가상화(KVM/Xen -> Firecracker), 분산 스토리지(Ceph, MinIO), SDN(Software Defined Networking), 그리고 선언적 인프라(IaC: Terraform/Pulumi)를 통해 컴퓨팅 자원을 **오케스트레이션 가능한 API 객체**로 추상화했다. 2013년 Docker의 등장으로 컨테이너가 보편화되었고, 2015년 CNCF 설립과 Kubernetes 1.0 출시로 컨테이너 오케스트레이션이 표준화되면서, **"어디서나 동일하게 실행되는 클라우드 네이티브"** 시대가 본격 개막했다.

한국 환경에서는 2022년 클라우드 컴퓨팅 이용자 수 약 2,100만 명, 공공부문 클라우드 전환률 35%(2025년 목표 50%), 금융권 클라우드 가드레일(2024년 1월) 시행으로 인해 단순 IaaS 마이그레이션을 넘어 **MSA + DevSecOps + FinOps** 통합 설계가 기술사 시험의 핵심 평가 영역이 되었다.

```text
  +--------------------------------------------------------------------+
  |          On-Premise -> Cloud -> Multi-Cloud -> Cloud Native 진화        |
  +--------------------------------------------------------------------+
  |                                                                    |
  |  1990s               2006~2013           2014~2019          2020~  |
  |  +---------+         +---------+         +---------+      +---------+
  |  | Mainframe|   ->    |  IaaS   |    ->    |  PaaS   |  ->   | Cloud   |
  |  | + Unix  |         | VM기반  |         | Container|      | Native  |
  |  | Scale-Up |         | RDS,S3  |         | K8s     |      | Serverless|
  |  +---------+         +---------+         +---------+      +---------+
  |      |                   |                  |                |
  |  CAPEX 중심          CAPEX+OPEX         OPEX 중심      Usage-Based |
  |  수직확장            수평확장 시작        선언적 IaC     FinOps 시대 |
  |  Waterfall          Agile-DevOps      GitOps+AIOps    AI/ML+Edge |
  +--------------------------------------------------------------------+
```

전통적 아키텍처 대비 클라우드 아키텍처의 핵심 가치는 다음 5가지로 요약된다:

1. **탄력성(Elasticity)**: CloudWatch/Stackdriver 메트릭 기반 Auto-Scaling Group(ASG), Kubernetes HPA(V2: CPU/Memory/Custom Metrics), Karpenter 기반 Just-in-Time 노드 프로비저닝
2. **무중단 배포(Zero-Downtime Deployment)**: Blue-Green, Canary(Flagger/Argo Rollouts), Rolling Update 전략
3. **회복력(Resilience)**: Circuit Breaker(Hystrix -> Resilience4j), Bulkhead, Retry with Exponential Backoff(±Jitter), Chaos Engineering(Chaos Monkey, Litmus)
4. **관측가능성(Observability)**: 3대 축 - Metrics(Prometheus/Grafana), Logs(Loki/ELK), Traces(Jaeger/Tempo); OpenTelemetry 표준
5. **자동화(Automation)**: IaC(Terraform/CloudFormation), GitOps(ArgoCD/Flux), Policy-as-Code(OPA/Kyverno)

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **"전기를 직접 발전하지 않고 콘센트에서 끌어다 쓰는 도시 전력망"**과 같다. 발전소(데이터센터)는 전력회사(클라우드 제공사)가 책임지고, 우리는 전기 요금(사용량 기반 과금)과 콘센트 규격(API/SDK)만 알면 된다. 한정된 콘센트(Auto-Scaling)와 정전 대비 UPS(Multi-AZ) 설계만 신경 쓰면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **NIST 정의의 5대 특성**(온디맨드 셀프서비스, 광대역 네트워크 접근, 자원 풀링, 빠른 탄력성, 측정 가능한 서비스)과 **3대 서비스 모델**(IaaS/PaaS/SaaS), 그리고 **4대 배포 모델**(Public/Private/Hybrid/Community)을 기반으로 한다. 기술사 시험에서는 이 프레임워크 위에 **Cloud Native** 4Pillar(Microservices, Containers, DevOps, Continuous Delivery)가 결합된 현대적 아키텍처를 심층 이해해야 한다.

```text
  +------------------------------------------------------------------+
  |              Cloud Native Architecture 4 + 1 계층 구조              |
  +------------------------------------------------------------------+
  |                                                                  |
  |  [L5] Application Layer    : MSA / Serverless Function / BFF     |
  |       +- API Gateway (Kong, AWS API GW, Envoy)                   |
  |       +- Service Mesh (Istio, Linkerd, Consul Connect)           |
  |  ------------------------------------------------------------    |
  |  [L4] Data Layer           : RDB(PostgreSQL), NoSQL(DynamoDB),   |
  |       Cache(Redis), Search(OpenSearch), Streaming(Kafka)         |
  |  ------------------------------------------------------------    |
  |  [L3] Platform Layer       : Kubernetes (EKS/AKS/GKE/On-Prem)    |
  |       +- Helm/Kustomize/ArgoCD (Package & GitOps)               |
  |       +- Service Mesh Sidecar (Envoy Proxy)                      |
  |       +- Operator Pattern (CRD + Controller)                     |
  |  ------------------------------------------------------------    |
  |  [L2] Infrastructure Layer : IaC (Terraform/Pulumi/CDK)          |
  |       +- Multi-Cloud/Region, VPC Peering, Transit Gateway        |
  |  ------------------------------------------------------------    |
  |  [L1] Hardware/Network     : Hyperscaler DC, Edge POP,           |
  |       Bare-Metal(Kubernetes-on-BM), ARM/x86 Instance             |
  +------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway / Ingress** | 클라이언트 단일 진입점, 인증/인가, Rate Limiting, Routing | Kong(Plugin: OAuth2/JWT/Rate-Limit), AWS API Gateway(Throttling: 10K RPS 기본), NGINX Ingress(Classic), Istio Ingress Gateway(eBPF 가속, mTLS 기본) |
| **Service Mesh** | 서비스 간 L7 트래픽 제어, mTLS, Circuit Breaker, Observability | Istio(Control Plane: istiod + Data Plane: Envoy), Linkerd(Buoyant Rust Proxy, 4x 경량), Consul Connect. Sidecar Pattern: Pod 내 별도 컨테이너로 Proxy 주입 (iptables 리다이렉트) |
| **Container Orchestrator** | 컨테이너 스케줄링, Self-Healing, Service Discovery, HPA | Kubernetes 1.30+ (Scheduler: kube-scheduler with Spread/Priority Plugin), HPA v2(CPU/Mem/Custom: KEDA), Cluster Autoscaler -> Karpenter(Node Template 기반 Bin-Packing 최적화) |
| **CI/CD & GitOps** | 자동 빌드/테스트/배포, 선언적 상태 동기화 | Tekton(Cloud Native CI), ArgoCD(Pull 방식, ApplicationSet), Flux CD, Jenkins X, Spinnaker(Netflix계, Multi-Cloud 배포). 핵심: **선언적(Declarative) + 불변(Immutable) + 멱등(Idempotent)** |
| **Observability Stack** | 3대 시그널 수집·시각화·알림, SLO/SLI 측정 | Metrics: Prometheus + Grafana (PromQL, Recording Rule), Logs: Loki/Label-based(ELK 대비 70% 저장비용 절감) or EFK, Traces: Jaeger/Tempo/Zipkin + OpenTelemetry SDK. **USE Method(Utilization/Saturation/Errors)** + **RED Method(Rate/Errors/Duration)** |
| **Cloud Storage & DB** | 상태 저장, 분산 트랜잭션, 데이터 중복성 | S3(11 9s 내구성, 99.99% 가용성, 3+ AZ 복제), RDS Multi-AZ(Synchronous Replication, RPO=0), DynamoDB Global Table(Multi-Region Active-Active, RPO<1s), Aurora(6 copies across 3 AZ, P99 < 100ms read) |
| **Security & Identity** | Zero Trust, IAM, Secrets, Compliance | IAM(RBAC/ABAC), KMS/HSM, Vault(Dynamic Secrets, Lease 32s), OPA/Kyverno(Policy), Trivy/Snyk(이미지/의존성 SBOM), Falco(런타임 침입탐지 eBPF 기반) |
| **FinOps & Cost Mgmt** | 비용 가시성, 최적화, 예측 | AWS Cost Explorer + CUR, Kubecost(K8s 네임스페이스별 비용), Spot Instance(70%v), Savings Plan(최대 72%v), Reserved Instance, Graviton3(ARM64, 60% 성능/Watt^) |

**심화 핵심 원리 4가지**:

**(1) 12-Factor App (Heroku 2011, 현 CNCF 권고)**:
- **Codebase**: 단일 저장소, 다중 배포
- **Dependencies**: 명시적 선언 (requirements.txt, package.json)
- **Config**: 환경변수 주입 (Vault/Secrets Manager), 코드와 분리
- **Backing Services**: DB/Queue를 연결 자원으로 취급
- **Build/Release/Run**: 3단계 엄격 분리, 불변 릴리스
- **Processes**: Stateless, Shared Nothing
- **Port Binding**: 자체 HTTP Port (Tomcat embed)
- **Concurrency**: Process Model로 수평 확장
- **Disposability**: 빠른 시작(<5s), Graceful Shutdown(SIGTERM, max 30s)
- **Dev/Prod Parity**: 동일 백킹서비스, 동일 빌드
- **Logs**: stdout/stderr 스트림 (Fluent Bit -> Loki)
- **Admin Processes**: 일회성 작업도 동일 환경에서 실행

**(2) CAP Theorem & PACELC**:
- **Consistency vs Availability**: 분산 시스템은 P(네트워크 분할) 발생 시 C 또는 A 중 선택 필수
- **예시**: CP -> HBase, ZooKeeper(etcd); AP -> Cassandra, DynamoDB(Quorum-based eventual consistency)
- **PACELC**: 평시(Else)에도 Latency vs Consistency 트레이드오프 존재
- **기술사 판단**: 금융 원장은 CP(강일관성), 상품 카탈로그는 AP(고가용성) 적용

**(3) Consensus 알고리즘**:
- **Raft** (etcd, Consul, CockroachDB 리더 선출): Leader Election + Log Replication, Term 기반
- **Paxos** (Chubby, Spanner): 이론적 기반, 구현 복잡
- **Quorum**: 쓰기 W + 읽기 R > N (예: N=3, W=2, R=2 -> Strong Consistency)

**(4) Auto-Scaling 3단계**:
- **HPA** (Horizontal Pod Autoscaler): Pod 수량 조절, 메트릭: CPU/Mem/Request-per-Second/Custom(KEDA, SQS Queue Length)
- **VPA** (Vertical Pod Autoscaler): Pod 자원 요청/제한값 자동 조정
- **CA** (Cluster Autoscaler) -> **Karpenter**: 노드 자체 추가/제거, 30초 이내 프로비저닝, Spot Fallback 지원

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"자동화된 호텔 운영 시스템"**과 같다. 체크인(API Gateway) -> 키카드 발급(Auth) -> 룸서비스(Service Mesh) -> 룸 자동 청소(Self-Healing) -> 실시간 객실 현황판(Observability) -> 수요에 따른 층별 증축(Auto-Scaling) -> 표준 운영 매뉴얼(GitOps IaC) — 모든 것이 **API 한 줄**로 제어된다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처 심화 학습을 위해서는 자주 혼동되는 유사 개념들의 정확한 차이를 숙지해야 한다.

| 구분 | **Monolith** | **Microservices (MSA)** | **Serverless (FaaS)** |
| :--- | :--- | :--- | :--- |
| **배포 단위** | WAR/EAR 1개 (수백 MB) | 컨테이너 이미지 (수십~수백 MB) | 함수 코드 (수 KB~수 MB) |
| **확장 단위** | 인스턴스 전체 복제 | 서비스 단위 독립 스케일 | 동시실행(Concurrency) 단위 (1~1000+) |
| **장애 격리** | 전체 다운 가능 | Circuit Breaker로 부분 장애 | 다른 Function으로 자동 격리 |
| **개발 언어** | 단일 (Java/Spring) | Polyglot (Java/Go/Node/Python) | 언어별 Runtime 제약 (Lambda: 14+ 지원) |
| **Cold Start** | 없음 | 수 초 (이미지 Pull) | 100ms~3s (예: Node.js 200ms, Java 3s with SnapStart) |
| **적합 워크로드** | 단순 CRUD, 레거시, 트랜잭션 집중 | 복잡 도메인, 대규모 트래픽 | 이벤트 기반, 간헐적, Webhook 처리 |
| **운영 복잡도** | 낮음 (1개 배포) | 높음 (수십~수백 서비스, Service Mesh 필수) | 중간 (벤더 관리형이지만 콜드
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 628 / 800

<- **이전**: [627. 클라우드 아키텍처 핵심 토픽 627번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/627_cloud_architecture_core_topic_627_exam_summar/)
**다음**: [629. 클라우드 아키텍처 핵심 토픽 629번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/629_cloud_architecture_core_topic_629_exam_summar/) ->

---
