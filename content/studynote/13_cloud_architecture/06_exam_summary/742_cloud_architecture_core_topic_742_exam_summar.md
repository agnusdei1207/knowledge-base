---
title: "742. 클라우드 아키텍처 핵심 토픽 742번 시험 요약 (Cloud Architecture Core Topic 742 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS·PaaS·SaaS·FaaS 계층 위에 Well-Architected Framework(WAF) 5대 기둥(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화)과 12 Factor App, Cell-Based Architecture, Bulkhead/Shuffle Sharding 같은 회복성 패턴을 결합해 "가용성 99.99%·MTTR < 1분·탄력적 자동확장"을 코드·정책·인프라로 구현하는 엔지니어링 체계이다.
> 2. **가치**: 동일 워크로드 대비 CapEx->OpEx 전환으로 TCO 30~70% 절감, Auto Scaling으로 트래픽 피크 시 5분 내 10배 용량 확장, Multi-AZ·Multi-Region 배포로 재해복구 RPO ≤ 5초·RTO ≤ 1분 달성, 개발자 생산성 40% 향상(DORA Elite 기준 208배 더 빈번한 배포).
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs Multi/Hybrid Cloud의 거버넌스 비용, Stateless Microservices + Event-Driven 아키텍처 vs Stateful Monolith의 마이그레이션 비용, Spot/Preemptible 인스턴스 활용도 vs SLA 보장 수준, Egress 비용(예: AWS $0.09/GB) vs Cross-Region Latency 간 트레이드오프, Zero Trust + CSPM vs 전통적 Perimeter 보안 모델의 운영 복잡도.

---

## Ⅰ. 개요 및 필요성

전통적 On-Premise 데이터센터는 5~10년 주기의 Capacity Planning, 평균利用率 15~25%의 낮은 자원 활용률, 수동 패치·구성 관리로 인한 변경 실패율 15~25%(CHAOS Report), 그리고 CapEx 중심의 선투자 구조로 인해 트래픽 피크 대응이 불가능했다. 2024년 기준 글로벌 기업의 94%가 클라우드를 사용하고 있으며, 클라우드 네이티브 아키텍처는 ①인프라의 코드화(IaC: Terraform/AWS CDK/Pulumi) ②선언적 API(Desired State Reconciliation) ③불변 인프라(Immutable Infra, Container Image 기반) ④탄력성(Elasticity, 1초 단위 Auto Scaling)을 통해 "Pay-as-you-use" 모델과 7개 9(99.99999%) 가용성 목표를 달성한다.

특히 마이크로서비스 아키텍처(MSA)와 컨테이너 오케스트레이션(Kubernetes)가 보편화되면서, 클라우드 아키텍처는 단순한 VM 임대에서 **Cloud-Native Platform**(CNI/CSI/CRI 표준 인터페이스, Service Mesh, GitOps, Observability 3-Pillar) 기반의 분산 시스템 설계 패러다임으로 진화했다. 2024년 CNCF Survey에 따르면 프로덕션 K8s 사용률 89%, 서비스 메시 사용률 62%로, 클라우드 아키텍처의 중심은 "어디에 배포할까"에서 "어떻게 안전하고 빠르게 변경·회복할까"로 이동했다.

```text
클라우드 아키텍처 진화 패러다임 비교

[전통적 On-Premise]              [가상화 시대]              [클라우드 네이티브]
   +----------+                +----------+              +------------------+
   |  Monolith |                |  SOA     |              |  Microservices   |
   |  물리서버  |                |  ESB     |              |  API Gateway     |
   |  수동배포  |                |  VM     |              |  Service Mesh    |
   +----+-----+                +----+-----+              +--------+---------+
        |                            |                            |
   CapEx 중심                  CapEx+OpEx                    OpEx 100%
   이용률 15%                  이용률 35%                    이용률 60~80%
   배포 주기: 월               배포 주기: 주                 배포 주기: 일~시간
   장애복구: 일                장애복구: 시간                장애복구: 분~초
   변경실패율: 25%             변경실패율: 15%               변경실패율: 5%v
   (전통적 3-Tier)             (Hypervisor)                (K8s + Serverless)
   v                           v                             v
   SNMP/Zabbix                Prometheus 초입              Observability 3-Pillar
   (모니터링)                  (단일 시계열)                (Logs+Metrics+Traces)
```

```text
클라우드 컴퓨팅 계층 구조 (NIST SP 500-292 참조 모델)

  +-------------------------------------------------------------+
  | SaaS (Software as a Service)                                |
  |  - 예: Salesforce, MS 365, Google Workspace, Slack           |
  |  - 사용자 책임: 데이터·접근관리                              |
  +-------------------------------------------------------------+
  | FaaS (Function as a Service) - Serverless                  |
  |  - 예: AWS Lambda, Azure Functions, Cloud Functions         |
  |  - Cold Start 100~500ms, 동시성 1000, Event-Driven          |
  +-------------------------------------------------------------+
  | PaaS / CaaS (Container as a Service)                       |
  |  - 예: EKS, AKS, GKE, Cloud Run, App Engine                |
  |  - K8s Control Plane(Managed), Node Pool만 사용자 관리      |
  +-------------------------------------------------------------+
  | IaaS (Infrastructure as a Service)                         |
  |  - 예: EC2, Azure VM, Compute Engine, Lightsail            |
  |  - 가상화(KVM/Xen), 네트워크·스토리지는 API로 즉시 provisioning|
  +-------------------------------------------------------------+
  | 물리 인프라 (데이터센터, Power, Cooling, Network)            |
  |  - Hypervisor(KVM, Xen, Hyper-V) 통한 Multi-Tenancy        |
  +-------------------------------------------------------------+

  Shared Responsibility Model (공유 책임 모델)
  +------------+--------------------------------------+
  |  고객 책임   | 데이터, Identity, App, OS, Network  |
  |  (In)       | (IaaS 기준) / Runtime+OS 제외(PaaS)  |
  +------------+--------------------------------------+
  |  CSP 책임   | 물리, Host OS, 가상화, 인프라 서비스  |
  |  (Of)      | (전 계층 가용성, Compliance 보장)     |
  +------------+--------------------------------------+
```

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "호텔 체인 프랜차이즈"와 같다. 전통적 자가 주택(On-Premise)은 한 번 지으면 확장이 어렵지만, 호텔은 예약량에 따라 즉시 객실을 늘리고(check-in API), 쓰지 않는 방은 자동 청소·재판매되며(Auto Scaling), 프랜차이즈 본사(CSP)가 시설·보안·소방을 관리하고 고객은 룸서비스(SaaS)만 신경 쓰면 된다. 핵심은 "내가 관리하지 않는 것(Undifferentiated Heavy Lifting)"을 전문가에게 위임하는 책임 분배 모델이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **선언적 인프라**(Desired State) + **불변 인프라**(Immutable) + **관측 가능성**(Observability) 3대 축과, 이를 구현하는 6가지 핵심 컴포넌트(Compute, Storage, Network, Database, Security, Orchestration)로 구성된다. 이 컴포넌트들은 API-Driven 방식으로 상호작용하며, 모든 상태는 코드로 관리되고 Git을 Single Source of Truth로 사용한다.

### 핵심 컴포넌트 아키텍처

```text
클라우드 네이티브 아키텍처 상세 흐름도 (Request Lifecycle)

   Client(웹/모바일)
        | HTTPS
        v
  +------------------+
  |  Global LB / CDN |  <- Anycast IP, Edge Location, TLS Termination
  |  (CloudFront/    |     DDoS Shield (L3~L7), WAF Rules
  |   Cloudflare)    |     Cache-Control, Origin Shield
  +--------+---------+
           |
           v
  +------------------+
  |  API Gateway     |  <- Rate Limiting(Leaky Bucket), JWT 검증
  |  (Kong/Apigee/   |     Request Transformation, Circuit Breaker
  |   AWS API GW)    |     OIDC/OAuth2.0, mTLS
  +--------+---------+
           |
     +-----+-----+
     v           v
  +------+    +------+
  |Svc A |    |Svc B |  <- Stateless Pod(12 Factor), HPA/CPA
  |Python|    |  Go  |     Health Check(/healthz, /readyz)
  +--+---+    +--+---+     Graceful Shutdown(SIGTERM)
     |           |
     |   +-------+-------+
     |   | Service Mesh  |  <- Istio/Linkerd, mTLS, Traffic Split
     |   | (Sidecar)     |     Retry, Timeout, Telemetry
     |   +-------+-------+
     |           |
     v           v
  +------------------+
  | Message Broker   |  <- Kafka/RabbitMQ/SQS, At-least-once
  | (Event Bus)      |     Idempotency Key, Dead Letter Queue
  +--------+---------+
           |
     +-----+------+
     v            v
  +------+     +------+
  | DB   |     | Cache|  <- Read Replica, Sharding, CDC
  |RDS/  |     |Redis |     Connection Pool(HikariCP), Cache-Aside
  |Aurora|     |Cluster|
  +------+     +------+
     |
     v
  +------------------+
  |  Observability   |  <- Logs(Loki), Metrics(Prometheus),
  |  (3-Pillar)      |     Traces(Jaeger/Tempo), SLO/SLI
  +------------------+     OpenTelemetry SDK
```

### 구성 요소별 상세 명세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Compute Layer** | 비즈니스 로직 실행, Stateless 워크로드 처리 | EC2/VM(vCPU 1~128, RAM 0.5~3,904GB), ECS/EKS(K8s 1.29+, Pod Scheduling: binpack/spread), Lambda(최대 15분, 메모리 128MB~10GB, 동시성 1000/Account), Fargate(Serverless K8s, 0.25~16 vCPU); Spot Instance로 70%v 비용, Graviton3 ARM 기반 40%^ 성능/전력 |
| **Storage Layer** | 데이터 영속성, 다중 접근 패턴 지원 | Object(S3: 11 9s durability, 5TB/object, Lifecycle 정책), Block(EBS gp3: 16K IOPS baseline, 1,000 MiB/s), File(EFS: 10GB/s aggregate, NFS v4.1), Archival(Glacier: $0.00099/GB·월, 복원 1~12시간); Storage Class 자동 전환(Standard->IA->Glacier)으로 TCO 80%v |
| **Network Layer** | 지리 분산, L4~L7 트래픽 제어 | VPC/Subnet(16M IP/16비트, NACL+SG Defense-in-Depth), Transit Gateway(Hub-Spoke, 5,000 VPC peering), PrivateLink(서비스 간 사설 연결, NAT 우회), VPC Endpoint(Gateway/Interface, $0.01/hr), Direct Connect(1~100Gbps 전용선, Latency < 10ms), Cloud WAN(글로벌 SD-WAN, 정책 기반 라우팅) |
| **Database Layer** | 트랜잭션 일관성, 고가용성, 수평 확장 | RDBMS(Aurora: 6-way replication, 15 read replica, 128TB, Serverless v2 0.5~128 ACU), NoSQL(DynamoDB: 10ms p99 at any scale, 40K+ rcu/wcu, GSI/LSI), NewSQL(CockroachDB/PlanetScale: Raft 합의, 자동 샤딩), In-Memory(ElastiCache Redis 7.2: 73GB, Cluster Mode 500 Shard); CAP 정리상 AP vs CP 트레이드오프 |
| **Security Layer** | Zero Trust, 암호화, 거버넌스, 컴플라이언스 | IAM(RBAC+ABAC, SCP, Permission Boundary), KMS(Envelope Encryption, FIPS 140-2 L3 HSM), Secrets Manager(Rotate every 30d), WAF(SQLi/XSS/L7 DDoS, Rate-based Rule), GuardDuty(ML 기반 위협 탐지, $0.10/event), CSPM(Cloud Security Posture Management), Confidential Computing(Enclave/SEV-SNP, 메모리 암호화) |
| **Orchestration Layer** | 선언적 배포, 자동복구, 카나리/블루그린 | Kubernetes(Control Plane: etcd Raft 합의, Scheduler 1000 node/3000 pod), ArgoCD/Flux(GitOps, pull-based 3-way sync), Helm+Kustomize(템플릿 vs 오버레이), Crossplane(CRD로 K8s에서 클라우드 리소스 관리), Terraform(Plan->Apply, State Lock via DynamoDB, Module Registry) |

### 12 Factor App + Cloud-Native 확장 (15 Factor)

```text
12 Factor App 준수 체크리스트 + Cloud Native 확장 요소

I.   Codebase       -> 1 Codebase = Many Deploys (Git monorepo or polyrepo)
II.  Dependencies   -> 명시적 선언 (requirements.txt, package.json, OCI Image)
III. Config         -> 환경변수 주입 (Vault/Secrets Manager, CSI Secret Driver)
IV.  Backing Services -> URL로 attach, 교체 가능 (RDS->Aurora 무중단)
V.   Build/Release/Run -> 3단계 분리, CI/CD 파이프라인 (Tekton/Spinnaker)
VI.  Processes      -> Stateless, 공유 X (Redis/DB로 상태 외부화)
VII. Port Binding   -> Self-contained (ContainerPort, no Tomcat war)
VIII.Concurrency    -> 프로세스 모델로 수평 확장 (ReplicaSet, HPA)
IX.  Disposability  -> Fast startup(<5s), Graceful shutdown(SIGTERM, preStop hook)
X.   Dev/Prod Parity -> Docker Compose 로컬 = K8s 프로덕션 (Skaffold/Tilt)
XI.  Logs           -> stdout/stderr -> Fluent Bit -> Loki/S3 (12 Factor+)
XII. Admin Process  -> REPL/Task를 One-off Pod로 (kubectl exec, K8s Job)
-----------------------------------------------------------------
XIII. API First     -> OpenAPI 3.1/Swagger로 Contract-Driven (Cloud Native)
XIV.  Telemetry     -> Health/Metrics/Logs 표준화 (Prometheus/OpenTelemetry)
XV.   AuthN/AuthZ   -> OIDC + OAuth2.0 + Zero Trust (Cloud Native)
```

### 회복성(Resilience) 패턴 핵심 알고리즘

```text
Circuit Breaker 상태 전이 (Hystrix/Resilience4j)

      +---------+   실패율 > 임계치(50%/10s)    +----------+
      | CLOSED  | -----------------------------> |   OPEN   |
      | (정상)   |                                | (차단)    |
      +----^----+                                +----+-----+
           | 성공                                      | wait(D) = 5s
           |                                           v
           |                                      +----------+
           |           Half-Open 시도 50% 통과     | HALF_OPEN|
           +-------------------------------------|  (시험)   |
                                                 +----------+
  * Closed->Open: 실패율 임계치 초과 시 즉시 차단
  * Open->Half-Open: Sleep Window(5s) 경과 후 일부 트래픽 허용
  * Half-Open->Closed: 성공률 회복 시 정상화
  * 파라미터: failureRateThreshold(50), slowCallRateThreshold(100),
              waitDurationInOpenState(5s), permittedNumberOfCallsInHalfOpenState(10)

Bulkhead & Shuffle Sharding (격리 패턴)

  [전통적 Bulkhead]                      [Shuffle Sharding]
   Thread Pool A  ---> Service X         Pod 1: [S1,S2,S3]  (5/100개)
   Thread Pool B  ---> Service Y         Pod 2: [S4,S5,S6]  (다른 조합)
   -> 한 서비스 장애 시 자원 격리           Pod 3: [S7,S8,S9]
   ->
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 742 / 800

<- **이전**: [741. 클라우드 아키텍처 핵심 토픽 741번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/741_cloud_architecture_core_topic_741_exam_summar/)
**다음**: [743. 클라우드 아키텍처 핵심 토픽 743번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/743_cloud_architecture_core_topic_743_exam_summar/) ->

---
