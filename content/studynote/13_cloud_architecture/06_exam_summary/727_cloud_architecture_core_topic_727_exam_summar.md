---
title: "727. 클라우드 아키텍처 핵심 토픽 727번 시험 요약 (Cloud Architecture Core Topic 727 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Well-Architected Framework 5대 기둥(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화)과 Cloud Native Computing Foundation(CNCF) 참조 아키텍처를 통합하여, **마이크로서비스·Service Mesh·GitOps·eBPF 기반 Observability**를 결합한 12-Factor App 확장형 설계 원칙이 클라우드 아키텍처의 정수이다.
> 2. **가치**: AWS Well-Architected Tool 활용 시 인프라 비용 평균 25~30% 절감, AZ(Multi-AZ) 기반 99.99% SLA 확보, Chaos Engineering을 통한 MTTR 60% 단축, FinOps 도입으로 클라우드 낭비 비용 20~40% 회수 효과가 검증되었다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs 멀티 클라우드, **EKS vs GKE vs AKS** 컨테이너 오케스트레이션 선택, **Active-Active vs Active-Passive** DR 전략, **동기식 vs 비동기식(SAGA, CDC)** 트랜잭션 경계 설계, 그리고 Stateless Service 수평확장 시 **Connection Pool 고갈** 및 **Cache Stampede** 방지가 핵심 의사결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

전통적 3-Tier 모놀리식 아키텍처는 On-Premise 환경에서 **수직확장(Scale-Up)**, **강결합 컴포넌트**, **수개월 단위 릴리즈 사이클**, **수동 Capacity Planning**을 전제로 설계되었다. 그러나 2020년 이후 클라우드 네이티브 패러다임은 **수평확장(Scale-Out)**, **약결합 마이크로서비스**, **CI/CD 기반 지속적 배포**, **Auto-Scaling을 통한 탄력적 자원 운영**으로 근본적으로 전환되었다. 이 변화는 Netflix가 2009년 AWS로 마이그레이션하며 7년여에 걸쳐 모놀리스를 700여 개 마이크로서비스로 분해한 사례, 그리고 Amazon Prime Day(2023) 기준 1초당 1억 건 이상의 트랜잭션을 단일 리전 내에서 처리하는 규모의 운영 노하우에서 출발한다.

기술사 출제 관점에서 727번 토픽은 단순히 "클라우드를 쓴다"가 아니라, **클라우드 네이티브 4C(Command & Control, Communication, Connectivity, Cloud)**, **Kubernetes + Service Mesh(Istio/Linkerd)**, **Observability 3요소(Metrics·Logs·Traces)**, **Infrastructure as Code(Terraform/CloudFormation/Pulumi)**, **보안 4-Layer(Network/Identity/Application/Data)**를 통합적으로 판단할 수 있는 역량을 평가한다. 특히 2023~2025년 출제 트렌드는 **eBPF 기반 observability(Cilium, Pixie)**, **WebAssembly(WASM) 엣지 컴퓨팅**, **FinOps와 Sustainability Engineering**, **Zero Trust Architecture(ZTA) with SPIFFE/SPIRE**가 빈출한다.

```text
+----------------------------------------------------------------------+
|          Cloud Native Architecture Evolution Timeline                |
+----------------------------------------------------------------------+
|                                                                      |
|  2010        2014        2017        2020         2023      2025     |
|   |           |           |           |            |         |       |
|   v           v           v           v            v         v       |
| +-----+   +-----+    +-----+    +--------+    +--------+ +------+  |
| |VM기반|--->|Docker|---->|K8s  |---->|Service |---->|eBPF/  |->|AIops |  |
| | IaaS |   |컨테이너|   |오케  |    | Mesh/  |    |FinOps |  |+ESG |  |
| |     |   |화    |    |스트 |    | GitOps |    |  WASM |  |      |  |
| +-----+   +-----+    +-----+    +--------+    +--------+ +------+  |
|                                                                      |
|  Monolith -> Microservice -> Cloud Native -> Platform Engineering      |
|                                                                      |
+----------------------------------------------------------------------+
```

기존 On-Premise 대비 클라우드 전환의 본질적 필요성은 다음 4가지로 요약된다:
- **탄력성(Elasticity)**: 트래픽 변동에 따라 5분 내 Auto-Scaling (HPA: Horizontal Pod Autoscaler는 CPU/메모리/커스텀 메트릭 기반)
- **글로벌 배포 용이성**: AWS Global Accelerator, CloudFront(210+ Edge), Azure Front Door를 통한 50ms 이하 지연시간 확보
- **장애 격리(Fault Isolation)**: Cell-Based Architecture, Bulkhead Pattern으로 한 AZ/리전 장애 시 전체 시스템 영향 최소화
- **TCO 최적화**: Pay-as-you-go 모델로 초기 CAPEX를 OPEX로 전환, Reserved Instance(1~3년 약정)로 60~72% 할인, Spot Instance로 70~90% 추가 절감

- **📢 섹션 요약 비유**: 기존 모놀리식 아키텍처가 **하나의 거대한 빵집**이었다면, 클라우드 네이티브 아키텍처는 **프랜차이즈 본부가 레시피와 부자재만 제공**하고 각 가게가 수요에 따라 빵을 만드는 구조입니다. 빵이 부족하면 즉시 신규 가게(Auto-Scaling)를 띄우고, 한 가게에 불이 나도(Bug) 다른 가게는 정상 영업합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심 원리는 **CNCF Cloud Native Trail Map**의 10단계와 **AWS Well-Architected Framework 5 Pillars**의 교차점에서 정의된다. 12-Factor App(2011, Heroku)은 선언적 설정, Stateless 프로세스, Dev/Prod 일치, 로그 스트림, 일회성 프로세스, Admin 프로세스, Port 바인딩, 동시성, 격리, 의존성 명시, 빌드/릴리즈/실행 분리 12개 원칙을 제시하며, 이는 현재 K8s, OpenTelemetry, ArgoCD 등의 구현체에 그대로 반영된다.

```text
+------------------------------------------------------------------------+
|           Cloud Native Reference Architecture Stack                    |
+------------------------------------------------------------------------+
|                                                                        |
|  +--------------------------------------------------------------+      |
|  |  Layer 5: Application & Microservices (Spring Boot, Go, ..) |      |
|  |  - 12-Factor, DDD, BFF, SAGA, CQRS, Event Sourcing         |      |
|  +--------------------------------------------------------------+      |
|  |  Layer 4: Service Mesh & API Gateway                         |      |
|  |  - Istio/Linkerd (mTLS, Traffic Mgmt), Envoy, Kong, APIGEE  |      |
|  +--------------------------------------------------------------+      |
|  |  Layer 3: Container Orchestration & Runtime                  |      |
|  |  - Kubernetes (K8s) 1.30+, Helm, Kustomize, OPA/Kyverno     |      |
|  +--------------------------------------------------------------+      |
|  |  Layer 2: Observability (3 Pillars + eBPF)                   |      |
|  |  - Prometheus, Grafana, Loki, Tempo, Jaeger, OpenTelemetry  |      |
|  |  - Cilium Tetragon, Pixie, Falco (Runtime Security)         |      |
|  +--------------------------------------------------------------+      |
|  |  Layer 1: Infrastructure & IaC                               |      |
|  |  - Terraform, Pulumi, Crossplane, AWS CDK, CloudFormation   |      |
|  +--------------------------------------------------------------+      |
|  |  Layer 0: Multi-Cloud/Hybrid Foundation                      |      |
|  |  - EKS/AKS/GKE, VPC Peering, Transit Gateway, Karpenter     |      |
|  +--------------------------------------------------------------+      |
|                                                                        |
|  ↕ GitOps(ArgoCD/FluxCD) | Policy-as-Code | SPIFFE/SPIRE Zero Trust  |
+------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Kubernetes Control Plane** | 컨테이너 오케스트레이션, 선언적 상태 관리 | API Server + etcd(raft 합의) + Scheduler(bin-packing) + Controller Manager + Cloud Controller Manager. Pod 단위 스케줄링, ReplicaSet/Deployment로 자가치유, PDB(Pod Disruption Budget)로 안전성 보장 |
| **Service Mesh (Istio)** | L7 트래픽 관리, mTLS, 관측성 | Envoy Sidecar(1개 Pod당 1개)로 모든 east-west 트래픽 프록시. mTLS 1.3 자동 발급, Istio VirtualService로 Canary 배포(90/10 -> 50/50 -> 0/100), Circuit Breaker, Retry, Timeout 정책 |
| **Observability 3-Pillar** | 시스템 가시성 확보 | Metrics(Prometheus 15s scrape + PromQL + Recording Rules), Logs(Loki LogQL, 구조화 JSON, tail sampling), Traces(OpenTelemetry SDK + Jaeger/Tempo, W3C Trace Context 전파) |
| **IaC + GitOps** | 인프라 선언적 관리, 불변 인프라 | Terraform State(RDS 암호화, S3 backend lock) + ArgoCD Application Controller가 Git Repo 3-way sync(HEAD/Live/Cluster). Helm Values 오버라이드, Kustomize patch, OPA Gatekeeper로 정책 강제 |

**핵심 메커니즘 심화 분석**:
- **HPA(Horizontal Pod Autoscaler) 알고리즘**: `desiredReplicas = ceil[currentReplicas × (currentMetricValue / targetMetricValue)]`. KEDA(Kubernetes Event-Driven Autoscaling) 도입 시 Kafka Lag, SQS Queue Length, Cron Schedule 등 60+ 트리거로 확장
- **Kubernetes Scheduler 동작**: Node Affinity, Taint/Toleration, Pod Topology Spread Constraints, Resource Request/Limit 기반으로 100만 노드/클러스터 규모까지 확장(Borg 2015년 논문 기준)
- **Consensus 알고리즘 (etcd)**: Raft 합의 알고리즘으로 Leader Election + Log Replication. Write Quorum 3/5, Read는 Linearizable. fsync WAL로 디스크 영속성 확보, Snapshot으로 compaction
- **SAGA 패턴**: 2PC(2-Phase Commit)의 가용성 문제를 해결. Choreography(Event-driven, Kafka topic) 또는 Orchestration(중앙 Saga Manager) 방식. 보상 트랜잭션(Compensating Transaction)으로 eventual consistency 달성. **Pessimistic Locking vs Optimistic + Retry** 전략 비교 필요
- **Event Sourcing + CQRS**: 모든 상태 변경을 append-only event log(`OrderCreated`, `OrderPaid`, `OrderShipped`)로 저장, Read Model은 별도 projection으로 비정규화. Stripe/Datadog/Linkspreed 실제 사례, **Snapshot**으로 replay 시간 단축

- **📢 섹션 요약 비유**: Kubernetes는 **컨테이너 호텔의 컨시어지**입니다. 손님(Pod)이 오면 빈 방(Node)을 찾아 배정하고, 손님이 아프면(컨테이너 사망) 즉시 같은 방에 새 손님을 배치하며(ReplicaSet), 프런트 데스크(Service Mesh)가 손님들끼리의 대화(트래픽)를 안전하게 중재합니다.

---

## Ⅲ. 비교 및 연결

| 구분 | **On-Premise Monolith** | **Cloud Native Microservice** |
| :--- | :--- | :--- |
| **확장성 모델** | 수직확장(Scale-Up, HW 추가) | 수평확장(Scale-Out, Pod 레플리카 증식) |
| **배포 주기** | 분기/반기 단위 Big-Bang 배포 | 지속적 배포(CD, ArgoCD 자동 sync, 1일 수십 회) |
| **장애 도메인** | 단일 장애점(SPOF) 존재 | Bulkhead Pattern, Cell-Based Architecture로 격리 |
| **기술 스택** | 단일 언어/DB (Java + Oracle) | Polyglot(Go, Python, Rust), Polyglot Persistence(Redis+Cassandra+PostgreSQL) |
| **상태 관리** | Stateful, 세션 서버 의존 (Sticky Session) | Stateless, 외부 상태 저장소(Redis, DynamoDB) |
| **네트워크** | 내부 L4 스위치, 세그멘테이션 | mTLS(서비스 메시), VPC CNI, Calico/Cilium CNI |
| **관측성** | 로그 파일 + SNMP 폴링 | OpenTelemetry 기반 3-Pillar, eBPF, AIOps(Anomaly Detection) |
| **비용 모델** | CAPEX (HW 감가상각 5년) | OPEX (Pay-per-use, Reserved로 60%+ 절감) |
| **DR 전략** | Cold Backup + 수동 복구(RTO 24h+) | Active-Active Multi-Region, Pilot Light(RTO 분 단위) |
| **팀 구조** | 기능별 팀(Frontend, Backend, DBA) | Squad/Pod 모델, 2-pizza team(Conway's Law 적용) |

**다른 시스템 컴포넌트와의 통합**:
- **API Gateway ↔ Service Mesh**: North-South 트래픽(Kong, AWS API Gateway)과 East-West 트래픽(Istio)의 역할 분리. Kong의 JWT 플러그인 인증 -> Istio의 mTLS 내부 통신으로 End-to-End 암호화
- **Kafka ↔ DB**: **CDC(Change Data Capture)** 패턴. Debezium으로 PostgreSQL WAL -> Kafka Connect -> Downstream(Elasticsearch, S3 Data Lake). Transactional Outbox 패턴으로 Dual Write 문제 해결
- **Service Mesh ↔ Observability**: Istio의 Envoy가 생성한 access log, trace span을 OTLP로 Tempo/Jaeger 전송. RED 메트릭(Rate, Errors, Duration) 자동 수집
- **K8s ↔ Cloud Provider**: **Cluster Autoscaler** vs **Karpenter**(2023 AWS 출시, 30초 내 노드 프로비저닝, Spot Fallback 자동화) 비교
- **Serverless ↔ Container**: Lambda(콜드 스타트 200ms, 15분 타임아웃)와 Fargate(콜드 스타트 없음, vCPU 1초 과금)의 Trade-off

- **📢 섹션 요약 비유**: On-Premise는 **직접 짓고 관리하는 단독주택**, Cloud Native는 **호텔 체인에 살고 싶은 날 일수만 머무는 라이프스타일**입니다. 라이프스타일이 유연하지만, 호텔 규칙(Service Mesh 정책) 안에서 살아야 하고, 비용 관리를 소홀히 하면 영수증이 끔찍해집니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 클라우드 아키텍처를 설계할 때 기술사 등급의 판단이 필요한 핵심 의사결정 지점은 다음과 같다. 단순히 "어떤 기술을 쓰느냐"가 아니라 **"왜 그 기술을 선택했는지, 트레이드오프는 무엇인지, 장애 시 어떻게 복구하는지"**를 정량적 근거와 함께 설명할 수 있어야 한다.

### 기술사형 판단 체크리스트

1. **워크로드 특성 분석**: 트래픽 패턴(Steady/Variable/Spike), Latency 요구(SLO 99%ile < 100ms?), 데이터 크기(PB급 Data Lake 여부), 컴플라이언스 요구(PCI-DSS, K-ISMS-P, GDPR, CSAP)를 4주차 PoC 이전에 정의했는가?
2. **Multi-AZ + Multi-Region 설계**: 단일 리전은 **Natural Disaster(지진, 화재)** 시 RTO 24h 이상. **Active-Active(DynamoDB Global Tables, Aurora Global Database)** vs **Active-Passive(DR Site Warm Standby)**의 비용 2배 vs RPO 0/RTO 분 단위 Trade-off 검토
3. **가용성 수치(SLA) 산정**: 99.9%(연 8.7h 다운) vs 99.99%(연 52m) vs 99.999%(연 5m). **Component별 SLA 곱셈**: (1 - 0.999^4) × 100 = 동시 4개 컴포넌트 의존 시 가용성 급락. 직렬 vs 병렬 의존성 그래프 분석 필수
4. **비용 거버넌스(FinOps)**: Tagging 전략(80% 태깅 커버리지 목표), Cost Anomaly Detection ML 알람, **RI/SP 커버리지 70% 이상** 유지, **Idle Resource 자동 종료 스케줄러(Kubernetes Descheduler + CronHPA)**, Unit Economics(요청당 비용) 추적 체계 수립
5. **보안 Zero Trust 구현**: Network Micro-segmentation(Cilium NetworkPolicy), **SPIFFE/SPIRE** 워크로드 identity 발급, mTLS 전 구간 적용, **OPA/Kyverno** Policy-as-Code,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 727 / 800

<- **이전**: [726. 클라우드 아키텍처 핵심 토픽 726번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/726_cloud_architecture_core_topic_726_exam_summar/)
**다음**: [728. 클라우드 아키텍처 핵심 토픽 728번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/728_cloud_architecture_core_topic_728_exam_summar/) ->

---
