---
title: "Cloud Architecture Core Topic 765 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 **API·IaC(IaC)·선언적 오케스트레이션(Kubernetes/Istio)·탄력적 리소스 풀링**을 기반으로 워크로드를 코드화하여, 셀프서비스 프로비저닝과 메트릭 기반의 자동 제어를 통해 비즈니스 요구사항을 인프라 차원에서 실시간 추종하는 **분산·불변·관측가능(Observable) 시스템**이다.
> 2. **가치**: AWS·Azure·GCP 기준 동일 워크로드에서 평균 **CAPEX->OPEX 전환 30~40%**, Auto-Scaling 적용 시 트래픽 피크 대응 비용 **20~60% 절감**, 멀티 AZ·리전 배포로 **RTO 분 단위 / RPO 0~수 초** 달성, Time-to-Market를 기존 6개월 -> **2~4주**로 단축시킨다.
> 3. **판단 포인트**: **5대 아키텍처 결정 포인트(워크로드 특성, 데이터 일관성·주권, 네트워크 지연, 거버넌스·컴플라이언스, 종속성·종량제 비용 모델)**를 기준으로 Public/Private/Hybrid/Multi-Cloud·Lift&Shift vs Replatform vs Refactor·Synchronous vs Event-Driven 중 최적 조합을 선택해야 한다. 기술사 관점에서는 **트레이드오프(가용성 vs 일관성, 비용 vs 성능, 표준화 vs 유연성)**에 대한 명시적 근거 제시가 핵심이다.

---

## Ⅰ. 개요 및 필요성

전통적 3-Tier 온프레미스 아키텍처는 **수직 스케일링(Scale-Up)**, **장기 납기 HW 도입**, **수동 용량 계획**, **MTTR 수 시간~수 일** 수준의 장애 대응이라는 구조적 한계를 갖는다. 2006년 AWS S3·EC2 출시 이후 클라우드는 **IaaS -> PaaS -> SaaS -> FaaS/Serverless**로 서비스 추상화 수준을 지속적으로 높였으며, 2014년 Kubernetes 등장, 2015년 CNCF 설립, 2018년 이후 Service Mesh(Istio/Linkerd)·GitOps(Argo CD/Flux)·eBPF 기반 Observability가 결합되면서 **클라우드 네이티브(Cloud Native)** 패러다임이 정착되었다.

기술사 시험에서 빈출되는 핵심 도전과제는 ① 트래픽 변동성에 대한 **탄력성(Elasticity)**, ② 글로벌 사용자에 대한 **지연 시간(Latency) 최적화**, ③ 대규모 분산 환경의 **관측가능성·거버넌스**, ④ 클라우드 종속성(Vendor Lock-in) 회피, ⑤ **FinOps**(클라우드 비용 거버넌스)이며, 이를 해결하기 위해 **Well-Architected Framework**(AWS 6대 기둥 / Azure / Google SRE 4대 속성)와 **12-Factor App, C4 Model, TOGAF** 등의 표준 참조 모델이 활용된다.

```text
   [ Legacy On-Premises ]              [ Cloud-Native Architecture ]
  +----------------------+           +------------------------------+
  | Monolithic App        |           | Microservices (12~수백)      |
  |  - Tightly coupled    |  --►      |  - Loosely coupled, API 기반 |
  |  - Manual deploy      |  Migration|  - CI/CD + GitOps 자동 배포  |
  |  - Scale-up HW        |           |  - HPA/VPA/Cluster Autoscaler|
  +------+---------------+           +------+-----------------------+
         |                                  |
  +------v---------------+           +------v-----------------------+
  | Fixed Capacity       |           | Elastic Pool (Compute/Storage)|
  |  - CAPEX 중심        |           |  - OPEX + Pay-per-use        |
  |  - Over-provisioning |           |  - Spot/Reserved/On-Demand    |
  |  - Util 10~20%       |           |  - Util Auto-scaling 60~80%  |
  +------+---------------+           +------+-----------------------+
         |                                  |
  +------v---------------+           +------v-----------------------+
  | Siloed Ops (HW+OS+MW)|           | IaC (Terraform/Pulumi) + K8s  |
  |  - 수개월 구축        |           |  - 선언적 프로비저닝          |
  |  - 절차적 변경        |           |  - Immutable Infra           |
  +----------------------+           +------------------------------+

   ⏱  Provisioning: 주~월 단위             ⏱  Provisioning: 초~분 단위
   📉  Utilization:    10~20%                📈  Utilization:    60~80%
   💰  CAPEX/OPEX 비율: 80/20                💰  CAPEX/OPEX 비율: 20/80
   🔁  MTTR:             수 시간              🔁  MTTR:             수 분
```

- **📢 섹션 요약 비유**: 기존 온프레미스는 **개인 소유 자가용**(고정 보험·주차·정비 비용, 정원 4명뿐)이라면, 클라우드 아키텍처는 **우버/카풀·공유 모빌리티**(필요한 만큼 즉시 호출, 쓴 만큼 지불, 트래픽 폭주 시 차량이 알아서 증차)이다. 차량(VM)·엔진(K8s)·내비게이션(Observability)·보험(Failover)을 모두 API로 즉시 조달한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **리소스 계층(Infra) -> 오케스트레이션 계층(Platform) -> 애플리케이션 계층(App) -> 관측·거버넌스 계층(Ops)**의 4계층으로 분해된다. 각 계층은 **API**로 제어되며, **선언적(Declarative)** 스펙(YAML/HCL)을 Git에 저장하여 **Desired State**를 추구하는 **Reconciliation Loop**가 핵심 동작 원리이다.

```text
  +--------------------------------------------------------------------+
  |                  Cloud Architecture 4-Layer Model                  |
  +--------------------------------------------------------------------+

  +------------------------------------------------------------------+
  |  [Layer 4] Observability & Governance (Ops Plane)               |
  |  +------------+  +------------+  +------------+  +------------+  |
  |  | Prometheus |  | Grafana    |  | Loki/ELK   |  | OPA/Kyverno|  |
  |  | (Metrics)  |  | (Visual)   |  | (Logs)     |  | (Policy)   |  |
  |  +-----+------+  +-----+------+  +-----+------+  +-----+------+  |
  |        | eBPF/Cilium   | Tempo(Trace) | OpenTelemetry Pipeline   |
  +--------|---------------|--------------|--------------|----------+
           v               v              v              v
  +-------------------- Application Layer ----------------------------+
  |  Microservice A  Microservice B  Microservice C  Sidecar(Envoy)   |
  |  +---------+     +---------+     +---------+     +----------+   |
  |  | API GW  |◄---►| BFF     |◄---►| Worker  |◄---►| Service  |   |
  |  | (Kong/  |     | (GraphQL|     | (Kafka  |     | Mesh     |   |
  |  |  Envoy) |     |  Edge)  |     | Consumer)|    | (Istio)  |   |
  |  +---------+     +---------+     +---------+     +----------+   |
  |  Runtime: Container(OCI) / WASM / Lambda Runtime                  |
  |  State:    DB-per-svc / Saga / Event Sourcing / Outbox Pattern     |
  +--------------------+----------------------------------------------+
                       v
  +---------------- Platform / Orchestration Layer ------------------+
  |  Kubernetes (K8s) Control Plane                                  |
  |  +----------+ +----------+ +----------+ +------------------+    |
  |  | Scheduler| | Controller| |etcd(Cons.| | API Server (REST) |    |
  |  | (Binpack/| | Manager  | | Store)   | | + CRD/Operator   |    |
  |  |Spread)   | |(Reconcile)| |          | |                  |    |
  |  +----------+ +----------+ +----------+ +------------------+    |
  |  Add-ons: Istio · Argo CD · cert-manager · ExternalDNS · HPA     |
  +--------------------+----------------------------------------------+
                       v
  +---------------- Infrastructure Layer ----------------------------+
  |  Compute         Storage            Network           Security   |
  |  +---------+    +---------+       +---------+       +---------+  |
  |  |EC2/VM   |    |S3/Blob  |       |VPC/VNet |       |IAM/IdP  |  |
  |  |EKS/GKE  |    |EBS/Disk |       |LB/ALB   |       |KMS/HSM  |  |
  |  |Lambda/  |    |RDS/Aurora|      |CloudFront|      |WAF/SG   |  |
  |  |FaaS     |    |DynamoDB |       |TGW/Peering|    |GuardDuty|  |
  |  +---------+    +---------+       +---------+       +---------+  |
  |  Region / AZ / Edge / On-Prem  <- 멀티 리전·하이브리드 확장     |
  +------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway (Kong, AWS API GW, Apigee)** | 외부 트래픽 진입점, 라우팅·인증·Rate-Limit | JWT/OAuth2 검증, Lambda Authorizer, Request/Response 변환, OpenAPI 3.0 기반 정책 |
| **Service Mesh (Istio, Linkerd, Consul Connect)** | 서비스 간 mTLS, 트래픽 관리(카나리/블루그린), 관측 | Envoy Sidecar(1:1), xDS API로 설정 동기화, L7 라우팅·Retries·Circuit Breaker |
| **Container Orchestrator (Kubernetes)** | 컨테이너 스케줄링·셀프힐링·오토스케일링 | Control Plane(API Server, etcd, Scheduler, Controller Manager) + Node(kubelet, kube-proxy, CRI/CNI/CSI) |
| **IaC & GitOps (Terraform, Pulumi, Argo CD, Flux)** | 선언적 인프라·앱 배포, Git = Single Source of Truth | HCL/Pulumi DSL -> State File 관리, Argo CD는 Git과 클러스터 상태를 **3-way Reconciliation** (Sync Wave·Drift Detection) |
| **Observability Stack (Prometheus, Grafana, Loki, Tempo, OTel)** | Metrics·Logs·Traces 통합 수집·시각화 | OpenTelemetry SDK로 계측 -> Collector -> 시계열/로그/분산 트레이스 저장. **USE/RED 메서드** 적용 |
| **Event Streaming (Kafka, Kinesis, Pub/Sub, NATS)** | 비동기 이벤트 흐름, 백프레셔, 순서 보장 | Partition Key 기반 순서, Exactly-Once Semantics(EOS), **CQRS + Event Sourcing** 패턴 |
| **Cloud-native Storage (S3, EBS, RDS, DynamoDB, Aurora Serverless, Vitess)** | 영구·임시·캐시·오브젝트 저장 | S3=11 9s 내구성, DynamoDB=Single-digit ms p99, Vitess=MySQL 수평 샤딩 |
| **Identity & Security (IAM, SPIFFE/SPIRE, Vault, KMS)** | Zero-Trust 신원, 비밀 관리, 키 관리 | Workload Identity(SPIRFFE ID = SPIFFE://ns/sa), mTLS, KMS Envelope Encryption |

### 2.1 핵심 동작 원리 — Reconciliation Loop (조정 루프)

```text
  Git Repo (Desired State)        Cluster (Actual State)
  +---------------------+         +---------------------+
  | Deployment.yaml     |         | Pod x3 (running)    |
  | replicas: 5         |         | Pod x2 (degraded)   |
  +----------+----------+         +----------+----------+
             | git push                      | watch(API Server)
             v                               v
        +--------------------------------------------+
        |  Argo CD / Controller (Reconcile Loop)     |
        |  diff = Desired - Actual                   |
        |  if diff ≠ ∅: apply(Plan)                  |
        |  if actual.health != healthy: retry/replace|
        +--------------------------------------------+
                          |
                          v
            +--------------------------+
            |  HPA: scale based on     |
            |  CPU/Memory/RPS/QueueLag |
            |  minR ≤ N ≤ maxR         |
            +--------------------------+
```

- **오토스케일링 3계층**: **HPA**(Pod 레벨, CPU/메모리/Custom Metric), **VPA**(리소스 요청량 자동 권고), **Cluster Autoscaler/Karpenter**(노드 레벨, Spot/On-Demand 혼합). **KEDA**는 Kafka Lag, SQS Queue, Cron 같은 이벤트 기반 스케일링을 담당.
- **12-Factor App 핵심**: 코드베이스 1개, 의존성 명시적 선언, Config는 환경변수 분리, Backing Services는 리소스 attach 방식, 빌드/릴리스/실행严格 분리, Stateless 프로세스, Port Binding, Concurrency는 프로세스 모델, Disposability(빠른 시작·우아한 종료), Dev/Prod Parity, Logs는 Event Stream, Admin Processes는 일회성 작업으로 분리.
- **CAP / PACELC 트레이드오프**: 분산 시스템은 **일관성(C) vs 가용성(A)** 중 하나를 선택해야 한다(네트워크 단절 P 시). 평상시(Else)에도 **지연(L) vs 일관성** 트레이드오프 존재 -> RDB=CP, DynamoDB=AP, Cassandra=AP, Etcd=CP.
- **가용성 수식**: 고가용성 목표 `A = MTBF / (MTBF + MTTR)`. 99.99%(Four 9s) 달성을 위해 MTTR 1분 이내·MTBF 1년 이상 필요. 멀티 AZ 배치 + Health Check + Auto-Replace로 MTTR 단축.

- **📢 섹션 요약 비유**: **Reconciliation Loop**는 **온도
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 765 / 800

<- **이전**: [764. 클라우드 아키텍처 핵심 토픽 764번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/764_cloud_architecture_core_topic_764_exam_summar/)
**다음**: [766. 클라우드 아키텍처 핵심 토픽 766번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/766_cloud_architecture_core_topic_766_exam_summar/) ->

---
