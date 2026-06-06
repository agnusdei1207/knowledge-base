---
title: "Cloud Architecture Core Topic 611 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST 참조 모델(CCRA)을 기반으로 IaaS/PaaS/SaaS/FaaS/CaaS의 책임 분담 모델, Kubernetes·Service Mesh·eBPF 기반의 클라우드 네이티브 런타임, 그리고 Well-Architected Framework의 5대 기둥(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화)을 통합한 **추상화-오토메이션-관측가능성 3축 구조**이다.
> 2. **가치**: AWS/Azure/GCP 기준 CapEx->OpEx 전환으로 인프라 TCO 30~50% 절감, Kubernetes 오토스케일링(HPA+VPA+Cluster Autoscaler)으로 피크 트래픽 시 응답 지연 p99 60% 개선, Multi-Region Active-Active 구성으로 가용성 99.99%(연 52분 이내 장애) 달성이 핵심 정량 가치다.
> 3. **판단 포인트**: **Lift & Shift vs Cloud Refactoring vs Cloud Native** 3가지 마이그레이션 전략, **단일 클라우드 vs 멀티/하이브리드** 선택, **동기 RPC(REST/gRPC) vs 비동기 이벤트(EventBridge/Kafka)** 통신 패턴 결정이 TCO, 락인, 회복력의 트레이드오프를 좌우하는 기술사 핵심 판단 분기점이다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 3-tier 아키텍처(L7 스위치–Web/WAS–DB)는 **수직 확장(Scale-Up) 한계**, **프로비저닝 리드타임(주 단위)**, **Capacity Planning 실패율 70%**라는 구조적 비효율을 내포한다. 2006년 AWS S3·EC2 출시 이후 18년간 진화한 클라우드 아키텍처는 **가상화(KVM/Xen) -> 컨테이너화(Docker, 2013) -> 오케스트레이션(Kubernetes 1.0, 2015) -> 서버리스(Knative, 2018) -> WebAssembly 기반 엣지(Wasmtime, 2022)**로 추상화 수준이 지속적으로 상승해왔다.

2024년 기준 Gartner는 **전세계 퍼블릭 클라우드 지출 679조 원, 한국 23조 원** 규모로 집계했으며, CNCF Landscape에는 **1,000+ 프로젝트**가 등재되어 클라우드 네이티브가 사실상 신규 시스템 구축의 디폴트가 되었다. 특히 **Generative AI workloads**(LLM 추론, Vector DB, GPU 스케줄링)와 **규제 컴플라이언스**(클라우드 보안 인증, 데이터 주권)가 클라우드 아키텍처 설계의 새로운 제약조건으로 부상했다.

```text
[클라우드 아키텍처 진화 패러다임 비교]

  On-Premise          IaaS              PaaS              CaaS             FaaS/Serverless
  +----------+      +----------+      +----------+      +----------+      +----------+
  | App      |      | App      |      | App      |      | App      |      | Fcn Code |
  |----------|      |----------|      |----------|      |----------|      |----------|
  | Runtime  |      | Runtime  |      | Runtime  |      | Runtime  |      | (Managed)|
  | OS       |      | OS       |      | (Managed)|      | Container|      |  Event   |
  | Virt     |      | (Managed)|      | K8s/CF   |      | K8s/ECS  |      |  Driven  |
  | HW       |      | HW(Cloud)|      | HW(Cloud)|      | HW(Cloud)|      | HW(Cloud)|
  +----------+      +----------+      +----------+      +----------+      +----------+
  책임:사용자 100%    OS^사용자     Runtime^사용자   Container^사용자   Fcn코드만 작성
  TCO 5yr: 100%       65%           45%             35%             20%
  +------------------------------------------------------------------------------+
  | 추상화 수준:  Low <----------------------------------------------------> High |
  | 민첩성:       Low <----------------------------------------------------> High |
  | 락인:         없음 <------------------------------------------------> 강함  |
  +------------------------------------------------------------------------------+
```

기존 Monolith 대비 **Microservices + 12-Factor App**은 (1) 독립 배포·스케일링 (2) 장애 격리(Blast Radius) (3) 기술 이질성(Polyglot) (4) 팀 자율성(Conway's Law 역이용)이라는 4가지 본질적 이득을 제공하지만, **분산 시스템의 8가지 함정**(Fallacies of Distributed Computing) — 네트워크 신뢰성, 지연, 대역폭, 보안 경계 등 — 을 함께 떠안게 된다. 이를 해결하기 위해 **Service Mesh**, **분산 트레이싱**, **Saga 패턴**, **Outbox 패턴** 같은 클라우드 네이티브 패턴군이 등장했다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"호텔의 객실 관리 시스템"**과 같다. 손님(워크로드)이 늘면 객실(VM/Container)을 즉시 배정하고, 줄면 회수하며, 요금(OpEx)은 실제 사용한 객실 시간만큼만 청구하는 방식이다. 종래의 "자기 집 짓기"(온프레미스) 대비 유연성과 비용 효율이 압도적이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **"선언적 API(Declarative) + 컨트롤 루프(Reconciliation Loop)"** 이다. 사용자가 "원하는 상태(Desired State)"를 YAML/HCL로 선언하면, **클라우드 컨트롤러 매니저(Cloud Controller Manager, CCM)**, **Kubernetes Controller**, **Terraform Provider** 같은 컨트롤러가 **실제 상태(Actual State)를 지속적으로 reconcile**하여 수렴시킨다.

```text
[Kubernetes 기반 Cloud-Native Reference Architecture — Production급]

                            +-----------------------------------------+
                            |        External Traffic (HTTPS/gRPC)    |
                            +--------------------+--------------------+
                                                 v
   +-------------------------------------------------------------------------+
   |  Edge & Ingress Layer                                                   |
   |  +--------------+  +--------------+  +----------------------------+   |
   |  | CloudFront/  |  | WAF + Shield |  | Global Accelerator (Anycast)|   |
   |  | Cloud CDN    |  | (L7 DDoS)    |  | TCP/UDP 최적 라우팅         |   |
   |  +------+-------+  +------+-------+  +------------+---------------+   |
   +---------+-----------------+-----------------------+-------------------+
             +-----------------+-----------------------+
                               v
   +-------------------------------------------------------------------------+
   |  Cluster Ingress (Envoy/Istio IngressGateway / NGINX / ALB)             |
   |  • TLS Termination, mTLS, Rate Limit, Circuit Breaker                   |
   +-----------------------------+-------------------------------------------+
                                 v
   +-------------------------------------------------------------------------+
   |  Service Mesh Data Plane (Envoy Sidecar / eBPF / Linkerd Proxy)         |
   |  +----------+  +----------+  +----------+  +----------+               |
   |  | Pod-A    |  | Pod-B    |  | Pod-C    |  | Pod-D    |   <-- mTLS    |
   |  | +Sidecar |<-->| +Sidecar |<-->| +Sidecar |<-->| +Sidecar |   자동 암호화  |
   |  +----------+  +----------+  +----------+  +----------+               |
   +-----------------------------+-------------------------------------------+
                                 v
   +-------------------------------------------------------------------------+
   |  Kubernetes Control Plane (HA 3 Masters)                                |
   |  +----------+  +--------------+  +----------+  +------------------+   |
   |  | kube-apiserver  |  | etcd (Raft)|  | scheduler|  | controller-mgr  |   |
   |  | (etcd client)   |  | WAL+Snapshot|  | bin-pack |  | ReplicaSet/Job  |   |
   |  +-----------------+  +--------------+  +----------+  +------------------+   |
   +-----------------------------+-------------------------------------------+
                                 v
   +-------------------------------------------------------------------------+
   |  Observability Stack (OpenTelemetry -> Backend)                          |
   |  Metrics: Prometheus (pull, 15s scrape) + Thanos/Cortex (long-term)     |
   |  Logs:    Fluent Bit -> Loki / OpenSearch                               |
   |  Traces:  Jaeger / Tempo (W3C TraceContext propagation)                |
   |  Profiles: Parca / Pyroscope (Continuous Profiling)                    |
   +-------------------------------------------------------------------------+
                                 v
   +-------------------------------------------------------------------------+
   |  Data Plane (Multi-Region / Multi-AZ)                                  |
   |  AZ-a: RDS Aurora(MySQL) Multi-AZ | Redis Cluster | S3 | DynamoDB GSI |
   |  AZ-b: Standby                    | Replica       |    | Global Tables|
   |  AZ-c: Read Replica               |               |    |             |
   |  DR:   us-west-2 Active-Active via Route 53 Latency-based              |
   +-------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Cloud Controller Manager (CCM)** | K8s ↔ Cloud Provider API 브릿지 | AWS: ALB/NLB Controller, EBS CSI Driver, Karpenter(노드 프로비저너, 60초 내 신규 노드 Join, Spot/On-Demand 혼합 정책). Azure: AKS VPA, GCP: GKE Autopilot 모드 |
| **etcd (Raft 합의)** | 클러스터 상태 저장소(SSOT) | 3/5 노드 Quorum, WAL+WAL fsync=10ms, **2GB 디스크 권장**, `--quota-backend-bytes=8GiB`, `defrag` 주기 실행, v3.5+ gRPC proxy로 read latency 50%v |
| **Service Mesh (Istio/Linkerd)** | L7 트래픽 관리 + mTLS + 관측 | Istio: Envoy xDS(v3 API), Istiod 단일 바이너리(1.20+), Ambient Mesh(2024, Sidecar 제거, Waypoint Proxy+ztunnel). Linkerd: Rust기화 Proxy 2배 성능, 정책 단순화 |
| **CI/CD & GitOps** | 선언적 배포 자동화 | ArgoCD/Flux: Git repo = Source of Truth, **Argo Rollouts** Canary/Blue-Green(AnalysisTemplate + Prometheus 메트릭 기반 자동 Promote/Abort), Tekton/Pipeline as Code |
| **Auto-Scaling (3 계층)** | 용량 탄력성 | **HPA**(CPU/Mem/Custom Metric, 30s 주기), **VPA**(권장치 산정, OOMKill 방지), **Karpenter**(Bin-Packing, Spot interruption 2분 내 대응, 70% 비용v) |
| **Observability (3 신호)** | 시스템 가시화 | RED(Rate/Error/Duration) + USE(Utilization/Saturation/Error) + SLI/SLO/SLI Budget. OpenTelemetry SDK로 자동 계측, eBPF 기반 Pixie로 무침투 트레이싱 |

**핵심 알고리즘/파라미터:**
- **K8s Scheduler bin-packing 점수**: `score = (requested/total) × 10` + spread/least-allocated 가중치
- **HPA 공식**: `desiredReplicas = ceil[currentReplicas × (currentMetricValue / targetMetricValue)]`
- **Service Mesh mTLS**: SPIFFE/SPIRE 기반 Workload Identity, SDS(Secret Discovery Service)로 24시간 키 자동 rotation
- **SLO Error Budget**: `error_budget = 1 − SLO`. 예: 99.9% SLO면 월 43.2분 다운타임 허용 -> Burn Rate Alert(`1% / 1h`, `5% / 6h`)

- **📢 섹션 요약 비유**: 클라우드 네이티브 아키텍처는 **"자율주행 자동차의 제어 시스템"**과 같다. **선언적 YAML**은 "목적지"이고, **컨트롤러**는 운전대·엑셀·브레이크를 반복 조작하여 목적지까지 자율 주행한다. Service Mesh는 "차량 간 V2X 통신", Observability는 "블랙박스·계기판", Auto-Scaling은 "자동 크루즈 컨트롤"에 해당한다.

---

## Ⅲ. 비교 및 연결

**클라우드 서비스 모델별 책임 분담**과 **주요 CSP 비교**, 그리고 **아키텍처 패턴 비교**는 기술사 시험에서 빈출되는 비교축이다.

| 구분 | **IaaS (EC2/VM)** | **PaaS (Beanstalk/GAE)** | **CaaS (EKS/AKS/GKE)** | **SaaS (Salesforce/Workday)** |
| :--- | :--- | :--- | :--- | :--- |
| **사용자 관리 범위** | App + Data + Runtime + OS | App + Data | App + Data + Container | 설정/데이터만 |
| **프로비저닝 속도** | 3~
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 611 / 800

<- **이전**: [610. 클라우드 아키텍처 핵심 토픽 610번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/610_cloud_architecture_core_topic_610_exam_summar/)
**다음**: [612. 클라우드 아키텍처 핵심 토픽 612번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/612_cloud_architecture_core_topic_612_exam_summar/) ->

---
