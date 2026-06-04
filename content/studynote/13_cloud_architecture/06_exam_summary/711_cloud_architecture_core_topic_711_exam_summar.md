---
title: "711. 클라우드 아키텍처 핵심 토픽 711번 시험 요약 (Cloud Architecture Core Topic 711 Exam Summary)"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 컨테이너 오케스트레이션(Kubernetes/서비스 메시), 선언적 IaC(Terraform/CloudFormation), 이벤트 기반 FaaS(Lambda/Cloud Functions), 그리고 12-Factor App 원칙을 통해 **탄력적 컴퓨팅·무상태 서비스·격리된 보안 경계**를 코드화한 컴퓨팅 패러다임의 결정체이다.
> 2. **가치**: AWS Well-Architected Framework 5대 축(운영우수성·보안·신뢰성·성능효율·비용최적화) 적용 시 **가용성 99.99% SLA, MTTR 60% 단축, CapEx->OpEx 전환으로 TCO 30~50% 절감, Auto Scaling으로 트래픽 10배 변동 흡수** 등 정량적 효과를 입증한다.
> 3. **판단 포인트**: **Lift&Shift vs Cloud-Native Refactoring**의 ROI trade-off, **단일 클라우드 종속(Vendor Lock-in) vs Multi-Cloud/Inter-Cloud**의 운영 복잡도, **동기 API vs 이벤트 드리븐(EDA) 비동기**의 일관성·확장성 딜레마가 기술사의 핵심 의사결정 프레임이다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 3-Tier 아키텍처(웹서버-WAS-DB)는 **CAPEX 중심의 수직적 용량 계획(Over-Provisioning 30~40%)**, 하드웨어 수명 주기(3~5년)에 종속된 배포 주기, **단일 장애점(SPOF)** 회피를 위한 Active-Standby 구성의 이중화 비용 증가, 그리고 비즈니스 트래픽 피크(블랙프라이데이, 연말 결제 폭주) 대비 유휴 자원 낭비라는 구조적 한계를 내포한다.

클라우드 아키텍처는 **NIST SP 800-145**(云计算 정의)에서 제시한 5대 핵심 특성(온디맨드 셀프서비스, 광대역 네트워크 접근, 자원 풀링, 빠른 탄력성, 측정 가능한 서비스)을 기반으로, **IaaS->PaaS->SaaS->FaaS(Serverless)**로 추상화 수준을 점진적으로 높여 엔지니어가 인프라가 아닌 비즈니스 로직에 집중하도록 한다. 이는 2006년 AWS S3·EC2 출시 이후 18년간 진화하여, 2024년 기준 글로벌 퍼블릭 클라우드 시장이 **$679B**(Gartner) 규모로 성장하며 엔터프라이즈 IT의 de-facto 표준이 되었다.

```text
+-------------------------------------------------------------+
|                  클라우드 진화 단계 (Evolution)              |
+-------------------------------------------------------------+
|                                                             |
|  +----------+   +----------+   +----------+   +----------+ |
|  | On-Prem  |--->|  IaaS    |--->|  PaaS    |--->|  FaaS    | |
|  | 3-Tier   |   | (EC2,    |   | (Bean-   |   |(Lambda,  | |
|  | (Web-    |   |  VPC,    |   |  stalk,  |   | Cloud    | |
|  |  WAS-DB) |   |  S3)     |   |  RDS)    |   | Funcs)   | |
|  +----------+   +----------+   +----------+   +----------+ |
|       |              |              |              |       |
|    추상화0%       추상화30%       추상화60%       추상화100% |
|    수직확장       수평+수직        컨테이너         이벤트기반 |
|    수동운영       API 제어        선언적 배포        과금/실행 |
|    HW 수명주기    분 단위 프로비저닝  초 단위 배포       ms 단위  |
|                                                             |
|  비즈니스 민첩성 ----------------------------------------->  |
|  운영 복잡도   ----------------------------------------->  |
|  콜드 스타트   <---------------------------------------  |
+-------------------------------------------------------------+
```

**Old Paradigm vs New Paradigm 비교:**

| 차원 | On-Premise (Old) | Cloud-Native (New) |
|---|---|---|
| **확장 모델** | Scale-Up (Scale Vertically, HW 추가) | Scale-Out (HPA, K8s Pod 자동증식) |
| **배포 단위** | Monolith WAR/EAR (수시간) | Container/Microservice (수초~수분) |
| **장애 대응** | MTTR 4~8시간 (전체 HA 페일오버) | MTTR 1분 (Circuit Breaker + Self-Healing) |
| **과금** | CapEx 선불 (5년 감가상각) | OpEx 사용량 기반 (초/GB 단위) |
| **트래픽 대응** | 1.5배 피크 설계 (유휴 30%) | 10배 버스트 (Auto Scaling) |
| **재해복구** | 원격지 DR 사이트 (RPO 1시간) | Cross-Region Multi-AZ (RPO 수초) |

- **📢 섹션 요약 비유**: 기존 자가용(On-Premise)이 주차장에 24시간 갇혀 있는 것과 달리, 클라우드는 **우버(Uber)처럼 필요할 때만 호출하고 사용한 만큼만 결제**하는 ride-sharing 모델이다. 폭우(트래픽 피크) 시 100대의 차량이 자동 배차되는 것이 Auto Scaling이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **7계층 참조모델**(OCA: Oracle Cloud Architecture 또는 AWS Well-Architected Framework)을 기반으로, 다음 4대 핵심 메커니즘이 상호작용한다:

1. **컴퓨팅 추상화 계층**: Hypervisor(KVM/Xen) -> 컨테이너 런타임(containerd/CRI-O) -> 서버리스 런타임(Firecracker/microVM)
2. **네트워크 오버레이 계층**: VPC(Virtual Private Cloud) + SDN(Software Defined Network) + CNI(Container Network Interface, Cilium/Calico)
3. **상태 저장 계층**: 객체 스토리지(S3) + 블록 스토리지(EBS) + 분산 데이터베이스(DynamoDB/Cassandra)
4. **제어 평면(Control Plane)**: API Gateway + Service Mesh(Istio) + Orchestrator(K8s Control Loop)

```text
              +----- 클라우드 네이티브 4계층 아키텍처 -----+

  [Client] -HTTP/3, gRPC--> [Edge Layer]
                              |
                              v
                    +------------------+
                    |   CDN/Edge       | <- CloudFront, Cloudflare
                    |   (캐시, WAF)    |   L7 DDoS, TLS 1.3, HTTP/3
                    +------------------+
                              |
                              v
                    +------------------+
                    |  API Gateway     | <- Kong, AWS API GW, Apigee
                    | (라우팅, thrott) |   Rate Limit, OAuth 2.0/JWT
                    +------------------+
                              |
              +---------------+---------------+
              v               v               v
        +----------+    +----------+    +----------+
        | Service  |    | Service  |    | Service  |  <- Microservices
        |    A     |    |    B     |    |    C     |     (Polyglot)
        | (Node)   |    | (Go)     |    | (Py)     |
        +----------+    +----------+    +----------+
              |               |               |
              +-------+-------+-------+-------+
                      v               v
              +--------------+  +--------------+
              | Service Mesh |  |  Event Bus   |
              |   (Istio)    |  |  (Kafka,     |
              | mTLS, Retry  |  |   EventBridge|
              +--------------+  +--------------+
                      |               |
                      v               v
              +------------------------------+
              |      Data Plane              |
              |  +--------+  +--------+      |
              |  | RDS/   |  | Redis  |      |
              |  | Aurora |  |/Memcd  |      |
              |  +--------+  +--------+      |
              |  +--------------------+     |
              |  | S3/Object Storage  |     |
              |  +--------------------+     |
              +------------------------------+
                      |
                      v
              +------------------+
              | Observability    | <- Prometheus, Grafana
              | (3 Pillars)      |   OpenTelemetry, ELK
              |  - Metrics       |
              |  - Logs          |
              |  - Traces        |
              +------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 추상화** | 워크로드 실행 환경 제공 | EC2(Bare-Metal/Metal Nitro), ECS/Fargate(Managed Container), Lambda(밀리초 과금, 15분 timeout, 10GB tmpfs), EKS(K8s Upstream Conformance Certified) |
| **네트워크 오버레이** | 논리적 격리, 트래픽 제어 | VPC/16(/65,536 IP), 서브넷(/24), Security Group(Stateful L4), NACL(Stateless L4), Transit Gateway(Hub-Spoke), PrivateLink(엔드포인트 서비스) |
| **객체 스토리지** | 무제한 확장 Blob 저장 | S3 Standard(11 9s, ms 단위), IA(30일 후 액세스), Glacier IR(Instant Retrieval, ms 복원), DFR(Dual-Frequency Replicate), CRR(Cross-Region Replication) |
| **분산 데이터베이스** | 글로벌 스케일, 자동 샤딩 | DynamoDB(Global Tables, 10ms p99, 3,000 RCU/1,000 WCU), Aurora(MySQL/PostgreSQL 호환, 6-way 복제), Cosmos DB(5개 일관성 모델: Strong/Bounded Staleness/Session/Consistent Prefix/Eventual) |
| **오케스트레이션** | 컨테이너 라이프사이클 관리 | K8s Control Loop(Reconcile), HPA(Horizontal Pod Autoscaler, CPU/Mem/Custom Metric), Karpenter(Just-in-time 노드 프로비저닝), Cluster Autoscaler |
| **서비스 메시** | L7 트래픽 관리, mTLS, 관측 | Istio(Envoy Sidecar), Linkerd(less memory), Istio Ambient(베이스 없이 HBONE) |
| **IaC (코드형 인프라)** | 인프라 선언적 정의 | Terraform(Multi-Cloud, HCL), CloudFormation(AWS 전용, JSON/YAML), Pulumi(실제 프로그래밍 언어), Crossplane(K8s CRD 기반) |
| **관측가능성 (3 Pillars)** | Metrics/Logs/Traces 통합 | Prometheus(메트릭 시계열), Loki(로그), Tempo/Jaeger(분산 트레이싱), OpenTelemetry(벤더 중립 SDK) |

**핵심 알고리즘 및 파라미터:**

- **HashiCorp Consistent Hashing** (분산 캐시 키 분배): `hash(key) mod N` -> **Virtual Nodes(vnode)** 100~200개로 핫스팟 방지, O(log N) 키 재분배
- **Raft 합의 알고리즘** (etcd, K8s Control Plane): Leader Election(Term 기반), Log Replication(Commit Index), Heartbeat(150ms), Quorum(N/2+1) -> 3-Node 클러스터가 1개 장애 허용
- **RPS 산정 공식**: `RPS = (DAU × Avg_Session_Time × Action_Per_Session) / 86,400 × Peak_Factor(3~5)`. 예: DAU 100만, 세션 30분, 액션 10회, Peak 5배 -> 약 17,361 RPS
- **Auto Scaling 공식**: `Desired = ceil(Current_CPU / Target_CPU × Current_Instance)` (Target Tracking), 또는 `ceil(Metric / TargetValue)` (Step Scaling)

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **레이어드 케이크(千層蛋糕)**와 같다. 가장 아래 과일(물리 데이터센터), 그 위에 크림(IaaS), 그 다음 생크림(PaaS), 그리고 위에 장식(SaaS/FaaS). 맨 아래는 잘 안 보이지만 무게를 받치고, 맨 위는 화려하지만 무너지기 쉽다. 케이크가 무너지지 않으려면 **각 층의 비율과 무게중심**(아키텍처 일관성)이 핵심이다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처 의사결정 시 반드시 비교되는 5대 패러다임을 상세 비교한다.

| 구분 | **Monolith** | **Modular Monolith** | **Microservice** | **Serverless/FaaS** | **Service Mesh 기반 MSA** |
|---|---|---|---|---|---|
| **배포 단위** | 단일 WAR/JAR | 모듈별 패키지, 단일 배포 | 서비스별 독립 컨테이너 | 함수 단위 (수 KB~수 MB) | Pod + Sidecar Proxy |
| **확장성** | 수직 (HW) | 수직 + 부분 수평 | 수평 (서비스별 HPA) | 자동 (Concurrency 모델) | 수평 + mTLS 자동 |
| **장애 격리** | 전체 장애 | 모듈별 부분 장애 | 서비스별 격리 (Bulkhead) | 자동 격리 (실패 격리) | Circuit Breaker, Retry |
| **일관성** | 강한 일관성 (ACID) | 강한 일관성 | 최종 일관성 (Saga, CQRS) | 최종 일관성 (Idempotency Key) | 최종 일관성 + 분산 트랜잭션 |
| **네트워크 비용** | In-Process | In-Process | gRPC/HTTP (~10ms+) | API Gateway 콜드스타트 (~200ms) | mTLS 오버헤드 (~1~3ms) |
| **적합 규모** | ~10 RPS | ~100 RPS | ~수천 RPS | ~수만 RPS (이벤트 폭주) | ~수만~수십만 RPS |
| **적용 사례** | 소규모 SI, 레거시 | 모놀리식 리팩토링 중간 단계 | Netflix, Uber, Amazon | 이미지 리사이징, Webhook | 대규모 금융/이커머스 |

**연계 기술 스택 상세:**

```text
클라우드 아키텍처는 다음 7개 영역과 밀접하게 연결된다:

  [CI/CD] -----> [Container Registry] -----> [Orchestrator]
   (Jenkins,        (ECR, ACR,                (EKS, AKS, GKE
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 711 / 800

<- **이전**: [710. 클라우드 아키텍처 핵심 토픽 710번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/710_cloud_architecture_core_topic_710_exam_summar/)
**다음**: [712. 클라우드 아키텍처 핵심 토픽 712번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/712_cloud_architecture_core_topic_712_exam_summar/) ->

---
