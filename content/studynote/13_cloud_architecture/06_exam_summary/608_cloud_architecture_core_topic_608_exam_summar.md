---
title: "608. 클라우드 아키텍처 핵심 토픽 608번 시험 요약 (Cloud Architecture Core Topic 608 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 CAP定理(Consistency, Availability, Partition tolerance)와 ACID/BASE 트레이드오프 위에서, 컨테이너 오케스트레이션(Kubernetes), 서비스 메시(Istio/Linkerd), 무상태(Stateless) 마이크로서비스, 그리고 Infrastructure as Code(Terraform/CloudFormation)를 통해 확장성·탄력성·가용성을 코드 수준으로 제어하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: Auto Scaling Group(ASG)을 통한 수평확장으로 트래픽 피크 시 10분 내 1,000 EC2 인스턴스까지 확장 가능하고, Spot Instance + Reserved Instance 조합으로 compute 비용을 60~72% 절감하며, Multi-AZ/Region 아키텍처로 SLA 99.99%(연간 52.6분 다운타임) 달성이 가능하다.
> 3. **판단 포인트**: "Lift & Shift vs Cloud-Native Refactoring"의 ROI 트레이드오프, "Centralized API Gateway vs Sidecar Service Mesh"의 라우팅 복잡도, "Eager(Strong) Consistency vs Eventual Consistency"의 응답속도·데이터 정합성·장애전파 범위 3자 트레이드오프가 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스(Enterprise Datacenter) 아키텍처는 CAPEX(자본지출) 기반의 정적 용량 계획(Static Capacity Planning), 수직확장(Scale-Up) 한계, 그리고 MTTR(Mean Time To Restore) 평균 4시간 이상의 장애복구 시간을 가졌다. Netflix는 2008년 8월 8일 Oracle RAC DB 손상으로 3일간 DVD 배송이 중단되는 장애를 경험했고, 이를 계기로 2010년대 초 클라우드 네이티브 아키텍처로의 전환을 결정했다. AWS EC2, S3를 기반으로 한 클라우드 아키텍처는 사용량 기반 PAYG(Pay-As-You-Go) 과금, API 기반 프로비저닝, Multi-AZ 복제로 대표되는 가용성 보장, 그리고 컨테이너 오케스트레이션을 통한 선언적(Declarative) 인프라 관리를 제공한다.

```text
[전통적 아키텍처 vs 클라우드 네이티브 아키텍처 비교]

  +--------------------------+         +--------------------------+
  |  Traditional On-Premise  |         |   Cloud-Native Native    |
  +--------------------------+         +--------------------------+
  | Monolithic Application   |         | Microservices (12-factor)|
  |      |                   |         |      |    |    |    |    |
  |   [App Server]           |         | [S1][S2][S3][S4][S5]    |
  |      |                   |         |   |   |   |   |   |     |
  |   [RDBMS]                |         | [Istio Sidecar × 5]     |
  |      |                   |         |   |   |   |   |   |     |
  |   [SAN Storage]          |         | [Envoy Proxy + k8s]     |
  |      |                   |         |      |                  |
  |   [HW LB(F5)]            |         | [Cloud LB(ALB/NLB)]     |
  |   ------------------     |         |   ------------------     |
  |   Physical Datacenter    |         |   Multi-AZ / Multi-Region|
  +--------------------------+         +--------------------------+
    - CAPEX 중심 (서버 3년 선투자)      - OPEX 중심 (초당 과금)
    - 수직확장 한계 (CPU^=APP STOP)     - Auto Scaling (HPA/VPA/CA)
    - 장애복구 4~24시간               - Self-Healing (k8s ReplicaSet)
    - 배포주기: 월 1~4회              - 배포주기: 일 10~1000회
```

클라우드 아키텍처가 필요한 핵심 이유는 (1) **탄력성(Elasticity)**: 트래픽 변동에 따른 자동 스케일링, (2) **가용성(Resilience)**: Cell-Based Architecture와 Circuit Breaker 패턴을 통한 장애 격리, (3) **속도(Agility)**: IaC(Infrastructure as Code)와 GitOps를 통한 환경 일관성 보장, (4) **비용 최적화**: Spot/Preemptible/Reserved/Savings Plans의 4-Tier 가격 모델을 통한 TCO 절감이다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 "전기를 직접 발전소에서 만들지 않고 한전에서 끌어다 쓰는 것처럼", 컴퓨팅 자원을 직접 보유하지 않고 API 한 줄로 빌려쓰는 유틸리티 컴퓨팅(Utility Computing) 모델이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **5계층 분리(5-Layer Decoupling)**이다: Presentation(CDN/Edge) -> API Gateway -> Microservices(Business Logic) -> Data(Polyglot Persistence) -> Infrastructure(K8s/Serverless). 각 계층은 독립적으로 스케일링되며, SLO(Service Level Objective)에 따라 응답시간, 처리량, 가용성 목표가 분리된다.

```text
[Cloud-Native 12-Factor Microservices Architecture 상세 흐름도]

  +---------+    +---------+    +---------+    +---------+
  | Mobile  |    |   Web   |    |  3rd    |    | Partner |
  |   App   |    |  Browser|    |  Party  |    |   API   |
  +----+----+    +----+----+    +----+----+    +----+----+
       |              |              |              |
       +--------------+--------------+--------------+
                              |
                +-------------v-------------+
                |   CloudFront / Cloud CDN  |  <- Edge Layer
                |   (Global Edge Caching)   |     (TTL, Cache Key)
                +-------------+-------------+
                              |
                +-------------v-------------+
                |   WAF + AWS Shield       |  <- Security Layer
                |   (Layer 7 DDoS 방어)     |     (OWASP Top 10)
                +-------------+-------------+
                              |
                +-------------v-------------+
                |  API Gateway (Kong/Apigee) |  <- Routing Layer
                |  - Rate Limiting          |     (Token Bucket)
                |  - Auth (OAuth2/JWT)      |     (OIDC, mTLS)
                |  - Request Transformation  |
                +-------------+-------------+
                              |
       +----------+-----------+-----------+----------+
       |          |           |           |          |
  +----v---+ +---v----+ +----v---+ +-----v--+ +-----v--+
  |User Svc| |Order   | |Payment | |Catalog | |Notif.  |
  |(K8s    | |Svc     | |Svc     | |Svc     | |Svc     |
  |Pod×3)  | |(K8s    | |(k8s    | |(K8s    | |(Lambda)|
  |        | |Pod×5)  | |Pod×3)  | |Pod×8)  | |        |
  +---+----+ +---+----+ +---+----+ +----+---+ +----+---+
      |          |          |           |           |
      |   +------+----+  +--+----+  +---+---+  +---+----+
      |   |Istio Mesh |  |Istio  |  |Istio  |  | Istio  |
      |   |Sidecar    |  |Mesh   |  |Mesh   |  |  Mesh  |
      |   +------+----+  +--+----+  +---+---+  +---+----+
      |          |          |           |           |
      +----------+----------+-----------+-----------+
                              |
       +----------+-----------+-----------+----------+
       |          |           |           |          |
  +----v----+ +---v----+ +---v----+ +----v---+ +----v---+
  |PostgreSQL| |Redis  | |Kafka  | |DynamoDB| |S3      |
  |(RDS     | |Cluster| |(MSK)  | |(NoSQL) | |(Object)|
  |Multi-AZ)| |       | |       | |        | |        |
  +---------+ +-------+ +-------+ +--------+ +--------+
       |
  +----v-----------------------------------------+
  |  Observability Stack                          |
  |  Prometheus + Grafana (Metrics)              |
  |  Loki / ELK (Logs)                            |
  |  Jaeger / Tempo (Distributed Tracing)        |
  +----------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway** | 외부 트래픽 진입점, 라우팅·인증·흐름제어 | Kong(OpenResty+Lua), AWS API Gateway(throttling 10K RPS), Apigee(API monetization). GraphQL Federation, gRPC-Web 변환 지원 |
| **Service Mesh (Istio)** | 서비스 간 통신 제어, mTLS 암호화, 카나리 배포 | Envoy Sidecar(1:1 프록시), Istiod(Control Plane), xDS API 기반 설정 분배. mTLS SPIFFE ID로 Zero-Trust 구현 |
| **Container Orchestrator (K8s)** | 컨테이너 스케줄링, Self-Healing, HPA | Control Plane(API Server, etcd, Scheduler) + Worker Node(kubelet, kube-proxy). HPA: CPU>70%시 30초 내 Pod 추가, PDB로 자가치유 보장 |
| **Event Streaming (Kafka)** | 비동기 이벤트 전파, CQRS/Event Sourcing 기반 | Partition(병렬성) + Offset(순서) + Replication Factor 3(내구성). Exactly-Once Semantics는 Idempotent Producer + Transactional API 조합 |
| **Observability (3 Pillars)** | Metrics·Logs·Traces 통합 가시화 | Prometheus(15초 scrape), Loki(LogQL), Tempo/Jaeger(OpenTelemetry). RED Method(Rate, Errors, Duration), USE Method(Utilization, Saturation, Errors) |
| **IaC (Terraform)** | 인프라 선언적 프로비저닝, 상태 관리 | HCL(HashiCorp Configuration Language), State File(S3+DynamoDB Lock), Plan/Apply 2단계. Module Registry로 재사용성 극대화 |

기술사 시험 관점에서 가장 중요한 4가지 핵심 알고리즘/메커니즘은:

**1. Consistent Hashing**: 분산 캐시(Memcached/Redis Cluster)와 CDN(CloudFront Edge Location) 라우팅에 사용. K=160개 가상 노드(VNode)로 키 공간을 균등 분할하여 노드 추가/제거 시 재분배 키 비율을 1/N에서 1/K로 감소시킨다.

**2. Raft Consensus Algorithm**: etcd/Consul의 분산 합의 알고리즘. Leader Election(과반수 투표, Election Timeout 150~300ms) + Log Replication(AppendEntries RPC) + Safety(Committed Index 보장). MongoDB, CockroachDB, TiDB의 분산 코디네이터로 활용.

**3. Paxos vs Multi-Paxos**: ZooKeeper(ZAB), Google Chubby Lock Service의 기반. Single-Decree Paxos는 Prepare/Promise/Accept/Accepted 4단계. Multi-Paxos는 Leader 안정화 시 Phase 1 생략하여 throughput 향상.

**4. Bloom Filter / HyperLogLog**: Redis Bloom Filter(존재 여부 1% FPR), HyperLogCardinality(12KB로 2^64 카디널리티 ±0.81% 표준오차). 빅데이터 중복제거, UV(Unique Visitor) 카운팅에 필수.

- **📢 섹션 요약 비유**: 12-Factor Microservices 아키텍처는 마치 "한 명의 만능 요리사(모놀리스)가 모든 요리를 만드는 것" 대신, "전문화된 셰프 12명(서비스)이 각자의 요리(책임)만 만들고, 주방장(API Gateway)이 주문(Order)을 적절히 분배하는 레스토랑 키친 시스템"과 같다.

---

## Ⅲ. 비교 및 연결

| 구분 | Monolithic Architecture | Microservices Architecture | Serverless / FaaS |
| :--- | :--- | :--- | :--- |
| **배포 단위** | WAR/EAR 단일 산출물 (수 GB) | 컨테이너 이미지 100~500MB × N개 | 함수 코드 50MB 이하 (Zip) |
| **확장 단위** | 인스턴스 전체 (수직+수평) | 개별 서비스 Pod 단위 (HPA) | 함수 실행 횟수 (동시성 1~1000) |
| **장애 전파** | 한 모듈 장애 = 전체 장애 (Blast Radius 100%) | Circuit Breaker로 격리 (Blast Radius 5~20%) | DLQ + Retry로 격리 (Provider 장애 시 Cold Start 1~3초) |
| **데이터 정합성** | ACID 단일 트랜잭션 가능 (강한 정합성) | Saga Pattern + Compensation (결과적 정합성) | Eventual Consistency (Step Functions로 보완) |
| **기술 스택** | 단일 언어/프레임워크 (Java/Spring 일체) | Polyglot (Go, Python, Node.js 혼재) | Provider 종속 (Lambda: Node/Python/Java/Go/Ruby) |
| **Cold Start 지연** | 0초 (Always On) | 0.5~2초 (이미지 Pull) | 1~10초 (Container 초기화) |
| **비용 모델** | 상시 과금 (24/7 인스턴스) | 사용량 비례 (Pod × 시간) | 호출당 과금 ($0.0000166667/GB-초) |
| **SLA** | 99.9% (설계에 의존) | 99.95~99.99% (Multi-AK8s) | 99.95% (Lambda 자체 SLA) |
| **적합 워크로드** | 소규모 CRUD, 내부 시스템 | 대규모 트래픽, 도메인 분리 명확 | 간헐적·이벤트 기반, API Backend |
| **대표 사례** | 레거시 ERP, Jenkins 자체 | Netflix(700+ Microservices), Uber | AWS Lambda + API Gateway, Firebase |

**연관 기술 통합 관계도:**

```text
  +----------------------------------------------------+
  |  CNCF Cloud Native Landscape (2024)                |
  +----------------------------------------------------+
  |                                                    |
  |  [Provisioning] Terraform / Pulumi / Crossplane    |
  |         |                                          |
  |         v                                          |
  |  [Runtime] Kubernetes (EKS/AKS/GKE) / Nomad       |
  |         |                                          |
  |         +-► [Service Mesh] Istio / Linkerd         |
  |         |         |                                |
  |         |         +-► [Ingress] Envoy / NGINX      |
  |         |                                          |
  |         +-► [Storage] Rook-Ceph / MinIO / etcd     |
  |         |                                          |
  |         +-► [Observability] Prometheus / Grafana   |
  |                   |                                |
  |                   +-► [Tracing] Jaeger / Tempo     |
  |                                                    |
  |  [Application] Spring Boot / Quarkus / Dapr        |
  |         |                                          |
  |         +-► [Database] PostgreSQL / MongoDB / Cassandra|
  |                                                    |
  |  [Security] Falco / OPA / cert-manager / Vault     |
  |                                                    |
  |  [Serverless] Knative / OpenFaaS / KEDA           |
  |                                                    |
  +----------------------------------------------------+
```

- **📢 섹션 요약 비유**: Monolith는 "한 권의 백과사전(찾기 어려움, 분실 시 통째로 손실)", Microservices는 "위키백과 700개 문서
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 608 / 800

<- **이전**: [607. 클라우드 아키텍처 핵심 토픽 607번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/607_cloud_architecture_core_topic_607_exam_summar/)
**다음**: [609. 클라우드 아키텍처 핵심 토픽 609번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/609_cloud_architecture_core_topic_609_exam_summar/) ->

---
