---
title: "533. 클라우드 아키텍처 핵심 토픽 533번 시험 요약 (Cloud Architecture Core Topic 533 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 네이티브 아키텍처는 컨테이너(Container)·마이크로서비스(MSA)·선언적 오케스트레이션(Kubernetes)·불변 인프라(Immutable Infrastructure)·자동 회복(Self-Healing)을 12-Factor App 원칙 기반으로 결합하여, 애플리케이션 라이프사이클 전체를 코드형 인프라(IaC)와 GitOps로 관리하는 구조이다.
> 2. **가치**: AWS Well-Architected Framework 5대 원칙(운영 우수성·보안·안정성·성능 효율·비용 최적화) 적용 시 배포 빈도 200~1,000배, 장애 복구 시간(MTTR) 90% 단축, 인프라 비용 30~60% 절감, 가용성 99.99%(Four-Nines) 달성이 가능하며, CNCF Survey 2023 기준 프로덕션 컨테이너 사용률 92%를 기록한다.
> 3. **판단 포인트**: 모놀리식->분리(Domain-Driven Design 기반 Bounded Context 식별), 동기(REST/gRPC) vs 비동기(EDA·Kafka·EventBridge) 트레이드오프, Stateless 워크로드 비중 80% 이상 확보, Cell-based Architecture·Bulkhead·Circuit Breaker의 회복성 패턴 적용, FinOps 기반 Spot/Preemptible 인스턴스 활용 비중 결정이 핵심 의사결정이다.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스 3-Tier 아키텍처(L7 스위치 - WAS - DB)는 수직 확장(Scale-Up) 한계, 배포 주기 수개월, 장애 도메인 단일화, Capacity Planning 오류(평균 30% 과다 provisioning)라는 구조적 문제를 내포한다. 클라우드 컴퓨팅(2006년 AWS S3/EC2 출시)이 IaaS -> PaaS -> SaaS -> FaaS(Serverless)로 진화하면서, 2015년 Pivotal의 12-Factor App manifesto, 2018년 CNCF의 Cloud Native Definition v1.0을 기점으로 "클라우드 네이티브" 패러다임이 정착되었다. 2024년 Gartner 보고서는 신규 디지털 워크로드의 70%가 클라우드 네이티브 기반으로 구축된다고 예측했다.

기술사 관점에서 클라우드 아키텍처는 단순한 인프라 이전(Lift & Shift)이 아니라, **"Stateless · API-First · Event-Driven · Observability"** 4대 축을 기준으로 애플리케이션·데이터·플랫폼 레이어를 재설계하는 엔지니어링 discipline이다. 특히 NCP·KT Cloud·NHN Cloud 등 국내 CSP(Cloud Service Provider)의 Region 구성(2개 이상 AZ), 가용성 SLA(99.95% 이상), 컴플라이언스(CSAP·ISMS-P·개인정보보호법)를 만족시키기 위한 아키텍처적 의사결정이 시험의 핵심 평가 영역이다.

```text
[클라우드 네이티브 아키텍처 진화 패러다임 비교]

  +------------------+    +------------------+    +------------------+
  |   Monolithic     |    |      SOA         |    |  Cloud Native    |
  |   (2000s 이전)    |    |   (2005~2014)    |    |   (2015~현재)    |
  +------------------+    +------------------+    +------------------+
  | • Scale-Up       |    | • ESB/WS-*       |    | • Scale-Out      |
  | • Waterfall 배포  |    | • SOAP/WSDL      |    | • CI/CD          |
  | • 단일 장애점     |    | • 중앙 Orchestr. |    | • Service Mesh   |
  | • 수개월 릴리즈    |    | • 수주 릴리즈    |    | • 일/시간 단위   |
  | • RDBMS 단일      |    | • RDBMS + Cache  |    | • Polyglot DB    |
  +------------------+    +------------------+    +------------------+
           |                        |                       |
           v                        v                       v
  +--------------------------------------------------------------+
  |  변화의 본질:  Hardware  ->  Software  ->  Architecture        |
  |  비용 모델:    CapEx      ->  OpEx      ->  Pay-per-Value      |
  |  회복 방식:    Hot-spare  ->  Cold-DR   ->  Chaos Engineering  |
  +--------------------------------------------------------------+
```

**기존 vs 신규 패러다임 비교**

| 항목 | 전통적 On-Premise | 클라우드 네이티브 |
|:---|:---|:---|
| Provisioning | 수일~수주 (수작업) | 수십 초 (Terraform/CRD) |
| 확장 단위 | 물리 서버 | Pod(메모리 MB 단위) |
| 배포 방식 | 야간 배치/Window | Canary/Blue-Green 무중단 |
| 장애 대응 | 수동 Failover | Self-Healing + HPA |
| 비용 구조 | CapEx(고정) | OpEx(변동, FinOps) |
| SLA | 99.9%(Three-Nines) | 99.99%(Four-Nines) 이상 |

- **📢 섹션 요약 비유**: 클라우드 네이티브는 "택지분양 후 각자 짓는 단독주택(모놀리스)"에서 "설계도면만 들고 공장에 가면 아파트 한 채가 즉시 조립出厂되는 모듈러 주택"으로의 전환이다. 설계도면 = Container Image, 공장 = Kubernetes, 입주 = Deployment, 리모델링 = Rolling Update이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 네이티브 아키텍처는 **CNCF Cloud Native Trail Map** 8단계(Containerization -> CI/CD -> Orchestration -> Observability -> Service Mesh -> Storage -> Networking -> Security)를 따라 점진적으로 성숙도를 높여간다. 핵심 레이어는 다음과 같이 구성된다.

```text
[클라우드 네이티브 7계층 참조 아키텍처 (CNCF Reference Model)]

  +-------------------------------------------------------------+
  | Layer 7  : Application  |  Microservices · Serverless Fn  |
  +-------------------------------------------------------------+
  | Layer 6  : API Gateway  |  Kong · APIGW · Istio Ingress   |
  +-------------------------------------------------------------+
  | Layer 5  : Service Mesh |  Istio · Linkerd · Consul       |
  |             (mTLS, Retry, Circuit Breaker, Telemetry)       |
  +-------------------------------------------------------------+
  | Layer 4  : Orchestrator |  Kubernetes · ECS · Nomad       |
  |             (Control Plane: API Server, etcd, scheduler)    |
  +-------------------------------------------------------------+
  | Layer 3  : Runtime      |  containerd · CRI-O · gVisor    |
  +-------------------------------------------------------------+
  | Layer 2  : Image/Reg.   |  OCI Image · Harbor · ECR/DTR   |
  +-------------------------------------------------------------+
  | Layer 1  : Infra/IaC    |  Terraform · Pulumi · Crossplane|
  |             (VPC, IAM, KMS, KMS-Backed Secret)              |
  +-------------------------------------------------------------+

  [보완 횡단(Observability & Security) 레이어]
  - Logging: EFK(Loki) / OpenSearch / Splunk
  - Metrics: Prometheus + Grafana / CloudWatch / Datadog
  - Tracing: Jaeger / Zipkin / OpenTelemetry(OTel SDK)
  - Security: Falco · OPA/Gatekeeper · Trivy · Cosign(SBOM)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Kubernetes (K8s) Control Plane** | 선언적 상태(Desired State) 유지 | API Server(6443) ↔ etcd(Raft 합의, Quorum 3/5) ↔ kube-scheduler(bin-packing) ↔ kube-controller-manager. 모든 객체는 `kubectl apply -f`로 YAML 매니페스트 기반 reconcile(기본 30s 주기) |
| **Pod & Workload API** | 최소 배포 단위, IP per Pod(Flat Network) | Deployment(Stateless), StatefulSet(Stable ID + PVC), DaemonSet(Node 단 1개), Job/CronJob(배치). `resources.requests/limits`로 QoS Class(Guaranteed/Burstable/BestEffort) 결정 |
| **Service Mesh (Istio)** | L7 트래픽 관리 + Zero-Trust 보안 | Envoy Proxy(sidecar) -> mTLS 자동화로 Service-to-Service 암호화. VirtualService(라우팅), DestinationRule(트래픽 분할 90/10), Fault Injection(Chaos Test) |
| **API Gateway** | 외부 트래픽 진입점, 인증/인가/Quota | Kong(OpenResty + Lua), AWS API Gateway, Spring Cloud Gateway(WebFlux 기반 Reactive). OAuth 2.1 + JWT 검증, Rate Limiting(Token Bucket 알고리즘, n rps) |
| **CI/CD Pipeline** | 빌드->테스트->배포 자동화 | GitHub Actions / GitLab CI / ArgoCD(GitOps) / Jenkins X. Trunk-based Development + Semantic Versioning, SBOM(CycloneDX) 생성 -> Sigstore/Cosign 서명 |
| **Observability Stack** | 3대 신호(Logs·Metrics·Traces) 통합 | OpenTelemetry Collector(OTLP gRPC) -> Tempo/Jaeger(Trace) + Prometheus(Metric) + Loki(Log). RED 메서드(Rate·Errors·Duration), USE 메서드(Utilization·Saturation·Errors) |
| **Cloud Storage & DB** | Polyglot Persistence | OLTP: RDS/Aurora(MySQL/PG), Spanner/CockroachDB(Global). OLAP: BigQuery/Snowflake/Redshift. Cache: Redis Cluster(Hash Slot 16,384). Search: OpenSearch / Elasticsearch |

**핵심 동작 메커니즘 - Kubernetes Self-Healing Cycle**

```
   +------------------------------------------------------------+
   |  K8s Self-Healing Loop (Control Loop Pattern)              |
   |                                                            |
   |  +----------+  watch   +----------+  reconcile   +------+|
   |  |  etcd    |<---------->|API Server|<-------------|Contr-||
   |  |(state)   |          |(auth+adm)|              |oller||
   |  +----------+          +----+-----+              +------+|
   |       ^                     |                          ^   |
   |       |                     v diff                     |   |
   |       |              +--------------+                  |   |
   |       +------update--| kube-sched + |--exec------------+   |
   |                      |  kubelet     |                      |
   |                      +------+-------+                      |
   |                             v                              |
   |                    +------------------+                    |
   |                    | Container Runtime|                    |
   |                    |  (containerd)    |                    |
   |                    +------------------+                    |
   +------------------------------------------------------------+
```

**핵심 알고리즘 및 파라미터 (기술사 빈출)**

- **HPA(Horizontal Pod Autoscaler)**: `desiredReplicas = ceil[currentReplicas × (currentMetricValue / targetMetricValue)]`. 기본 스케일링 쿨다운 30s, 다운 쿨다운 5분
- **KEDA(Event-driven Autoscaling)**: Kafka Lag · SQS QueueLength · Cron · Prometheus Query를 트리거로 0까지 스케일 다운
- **Consistent Hashing**: Redis Cluster 16,384 slot, `CRC16(key) mod 16384`. 캐시 노드 추가/제거 시 키 재분배 ~`1/N`만 이동
- **Raft 합의**: Leader Election Timeout 150~300ms 랜덤화, Heartbeat 50ms, etcd Write 성능 ~10,000 ops/s
- **AWS Well-Architected 5 Pillar Review 주기**: 분기 1회, 시니어 아키텍트 + SRE + Security + FinOps 4인 이상

- **📢 섹션 요약 비유**: Kubernetes는 "호텔 지배인(Control Plane)"이 객실 현황(etcd)을 실시간 파악하고, 손님이 비어 있는 방(Pod)에 들어갈 수 있도록 안내(scheduler)하고, 룸키카드가 만료되면(check) 즉시 퇴실시켜 청소 후 새 손님을 받는(Self-healing) 시스템이다. Service Mesh는 각 복도마다 CCTV·인터폰·자동 잠금장치를 설치해 손님 간 직접 마주침 없이 안전하게 이동시키는 것이다.

---

## Ⅲ. 비교 및 연결

### 1. 컨테이너 오케스트레이션 비교

| 구분 | Kubernetes (K8s) | Docker Swarm | Apache Mesos | Nomad (HashiCorp) |
|:---|:---|:---|:---|:---|
| **아키텍처** | Master-Worker (Control/Data Plane 분리) | Manager-Worker (Raft 합의) | Master-Agent + Zookeeper | Server-Client (Raft) |
| **확장성** | 5,000 Node / 150,000 Pod (v1.30) | 1,000 Node 수준 | 10,000+ Node (분산) | 수천 Node |
| **서비스 메시** | Istio/Linkerd 통합 | 미지원 | 미지원 | Consul 통합 |
| **학습 곡선** | 매우 높음 (CRD·Operator 패턴) | 낮음 (Docker 호환) | 높음 | 중간 |
| **오토스케일링** | HPA + VPA + KEDA + Cluster Autoscaler | Compose 스케일 정도 | Marathon 자체 | Nomad Autoscaler |
| **적합 워크로드** | MSA · 배치 · AI/ML · Stateful | 소규모 Legacy | 빅데이터(Hadoop/Spark) | 멀티 클라우드 단순 워크로드 |
| **생태계 점유율 (2024)** | 92% (CNCF Survey) | <3% | <2% | <2% |

### 2. 컴퓨트 서비스 추상화 레벨 비교 (AWS 기준)

| 구분 | EC2 | ECS/Fargate | EKS | Lambda |
|:---|:---|:---|:---|:---|
| **추상화** | VM | 컨테이너 | K8s Pod | 함수 |
| **관리 책임** | OS·미들웨어 | 컨테이너·런타임 | K8s 컴포넌트 | 코드만 |
| **콜드 스타트** | 없음 | 30~60s | 30~60s | 200ms~2s |
| **최대 실행 시간** | 무제한 | 무제한 | 무제한 | 15분 |
| **과금 단위** | 초 단위 인스턴스 | vCPU·GB-초 | vCPU·GB-초 | 호출 수 + GB-초 (1ms 단위) |
| **적합 케이스** | 레거시 · Stateful | 일반 MSA | 멀티클라우드 MSA | 이벤트 처리 · ETL · Webhook |

### 3. 분산 트랜잭션 및 데이터 일관성 패턴

| 패턴 | 일관성 모델 | 사용 사례 | Trade-off |
|:---|:---|:---|:---|
| **2PC (Two-Phase Commit)** | Strong | RDB 단일 트랜잭션 | Coordinator SPOF, Lock 점유 시간 ^ |
| **Saga (Orchestration/Choreography)** | Eventual | 주문-결제-재고 MSA | 보상 트랜잭션 설계 복잡 |
| **CQRS + Event Sourcing** | Eventual -> Strong (Read Model) | 금융 도메
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 533 / 800

<- **이전**: [532. 클라우드 아키텍처 핵심 토픽 532번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/532_cloud_architecture_core_topic_532_exam_summar/)
**다음**: [534. 클라우드 아키텍처 핵심 토픽 534번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/534_cloud_architecture_core_topic_534_exam_summar/) ->

---
