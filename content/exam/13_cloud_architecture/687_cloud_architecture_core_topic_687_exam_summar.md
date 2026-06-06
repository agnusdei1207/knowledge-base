---
title: "Cloud Architecture Core Topic 687 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST 모델(서비스·배포·참조모델 3축)을 기반으로 한 **탄력성(Elasticity)·가용성(Availability)·확장성(Scalability)** 트레이드오프를 다루는 시스템 설계 패러다임으로, IaaS/PaaS/SaaS/FaaS 계층별 책임 분담과 Control Plane/Data Plane 분리를 통해 추상화 수준을 결정하는 것이 핵심이다.
> 2. **가치**: CAPEX->OPEX 전환(데이터센터 TCO 30~40% 절감), Auto Scaling을 통한 60~80% 비용 최적화, MTTR 90% 단축(Chaos Engineering 기반), SLA 99.99%(Four Nine) 이상 달성을 통한 글로벌 서비스 신뢰성 확보, Time-to-Market 5~10배 단축 효과가 대표적이다.
> 3. **판단 포인트**: ① 워크로드 특성(상태 유지 Stateful vs 무상태 Stateless)에 따른 Compute 모델 선택, ② Shared Responsibility Model에서 보안 책임 경계(SaaS/PaaS/IaaS 별 차이), ③ Multi-Cloud vs Hybrid vs Single Cloud 전략, ④ Cloud-Native(12-Factor, K8s) vs Lift & Shift 결정, ⑤ FinOps 기반 비용 가시성 확보가 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스(On-Premise) 아키텍처는 CAPEX(Capital Expenditure) 중심의 정적 자원 할당, 수직 확장(Scale-Up) 한계, 평균 5~7년의 투자 회수 기간, 그리고 단일 장애점(SPOF) 문제로 인해 급변하는 비즈니스 요구사항에 유연하게 대응하지 못하는 한계를 가졌다. 2006년 AWS S3와 EC2 출시 이후 IaaS가 본격화되었고, 2010년대 Google App Engine·AWS Lambda로 PaaS·FaaS가 대중화되었으며, 2015년 Kubernetes 1.0 출시와 CNCF 설립으로 클라우드 네이티브(Cloud-Native) 시대가 개막되었다. Gartner는 2025년 기준 전체 엔터프라이즈 IT 예산의 65% 이상이 클라우드로 전환될 것으로 예측하며, 한국은 2027년 공공 클라우드 시장이 약 5조 원 규모로 성장할 것으로 전망된다.

클라우드 아키텍처는 5가지 본질적 특성(NIST SP 800-145: On-Demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)과 3가지 서비스 모델(IaaS/PaaS/SaaS), 4가지 배포 모델(Public/Private/Hybrid/Community)로 표준화되어 있다. 특히 MSA(Microservices Architecture), Serverless, Event-Driven Architecture, Cloud-Native 12-Factor App 원칙이 현대 분산 시스템 설계의 표준이 되었으며, 2024~2025년 기준 AI/ML 워크로드, Edge Computing, Sovereign Cloud가 새로운 아키텍처 패러다임으로 부상하고 있다.

```text
[클라우드 진화 패러다임 비교]

  +-------------+     +-------------+     +-------------+     +-------------+
  |  Mainframe  | --> | Client/     | --> |   Web       | --> |  Cloud-     |
  |  (중앙집중) |     | Server      |     |  3-Tier     |     |  Native     |
  |             |     | (2-Tier)    |     | (N-Tier)    |     | (MSA+Server |
  | 1960~1980s  |     | 1980~2000s  |     | 2000~2015s  |     |   less)2015+|
  +-------------+     +-------------+     +-------------+     +-------------+
        |                    |                    |                    |
        v                    v                    v                    v
   Scale-Up            Scale-Up           Scale-Out           Elastic Scale
   전용 HW              RDBMS             L4/L7 LB           K8s AutoScaler
   Static              License          VM 이미지             Immutable Infra
   Monolith            Tight Coupling   ESB/SOA              API Gateway
   MTTR: 일            MTTR: 시간        MTTR: 분             MTTR: 초
```

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 진화는 마치 **수도꼭지에서 물을 받는 방식**과 같다. 과거에는 큰 물탱크(서버)를 직접 사서 저장해 두는 방식(온프레미스)이었다면, 클라우드는 수도꼭지를 돌리기만 하면 필요할 때마다 원하는 양만큼 즉시 물(자원)을 받고, 다 쓰면 바로 반환하여 요금을 낼 수 있는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 클라우드 컴퓨팅 참조 아키텍처 4계층 모델

NIST SP 500-292 참조 아키텍처는 클라우드를 5대 역할(Consumer, Provider, Broker, Carrier, Auditor)과 4개 계층(SERVICE LAYER, RESOURCE LAYER, PHYSICAL LAYER, SERVICE ORCHESTRATION LAYER)으로 정의한다. 실무에서는 이를 단순화하여 **Presentation -> Application -> Data -> Infrastructure** 4계층으로 재구성하여 설계한다.

```text
[클라우드 네이티브 4계층 + Cross-Cutting Concerns 상세 아키텍처]

  +-------------------------------------------------------------------------+
  | L1: Presentation Layer (Edge / CDN / API Gateway)                      |
  | +--------------+ +--------------+ +--------------+ +--------------+    |
  | | CloudFront/  | | API Gateway  | | WAF (Web     | | OAuth 2.0 /  |    |
  | | Cloud CDN    | | (REST/gRPC)  | | App Firewall)| | JWT Auth     |    |
  | +--------------+ +--------------+ +--------------+ +--------------+    |
  +-------------------------------------------------------------------------+
                                    | (TLS 1.3, mTLS)
  +---------------------------------v---------------------------------------+
  | L2: Application Layer (Microservices / Serverless / Event-Driven)      |
  | +----------+  +----------+  +----------+  +----------+  +----------+   |
  | |User Svc  |  |Order Svc |  |Pay Svc   |  |Lambda/   |  |EventBus  |   |
  | |(EKS Pod) |  |(EKS Pod) |  |(Cloud Run)| |Cloud Fn  |  |(Kafka/   |   |
  | |Spring    |  |Node.js   |  |Go        |  |Python    |  |EventBridge)|  |
  | +----+-----+  +----+-----+  +----+-----+  +----+-----+  +----+-----+   |
  |      | Service Mesh (Istio/Linkerd - mTLS, Circuit Breaker)            |
  +-------------------------------------------------------------------------+
                                    |
  +---------------------------------v---------------------------------------+
  | L3: Data Layer (Polyglot Persistence)                                  |
  | +----------+  +----------+  +----------+  +----------+  +----------+   |
  | |RDS/Aurora|  |DynamoDB/ |  |Redis/   |  |S3/Object |  |BigQuery/  |   |
  | |(RDBMS)   |  |Cosmos DB |  |ElastiCache| |Storage   |  |Redshift   |   |
  | |(OLTP)    |  |(NoSQL)   |  |(Cache)   |  |(Lake)    |  |(DWH/OLAP) |   |
  | +----------+  +----------+  +----------+  +----------+  +------------------+
  | CDC: Debezium -> Kafka -> Data Lake -> ETL/ELT (Airflow/dbt)              |
  +-------------------------------------------------------------------------+
                                    |
  +---------------------------------v---------------------------------------+
  | L4: Infrastructure Layer (Virtualization & Containerization)           |
  | +----------+  +----------+  +----------+  +----------+  +----------+   |
  | |K8s (EKS/ |  |EC2/VM    |  |Bare Metal|  |Serverless|  |Edge Node |   |
  | |AKS/GKE)  |  |(Hypervisor|  |(Dedicated|  |Container |  |(Lambda@  |   |
  | |Containerd|  |KVM/Xen)  |  |Host)     |  |(Fargate) |  | Edge)    |   |
  | +----------+  +----------+  +----------+  +----------+  +----------+   |
  | Compute + Storage + Network (VPC/Subnet/Security Group, EBS/EFS, S3)   |
  +-------------------------------------------------------------------------+

  ---------------------------------------------------------------------------
  Cross-Cutting: Observability(Logs/Metrics/Traces) + Security(Zero Trust)
                 + FinOps(Cost) + IaC(Terraform/CloudFormation) + CI/CD
  ---------------------------------------------------------------------------
```

### 2. 핵심 컴포넌트 및 기술 매핑

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway** | L7 트래픽 진입점, 라우팅·인증·속도제한 | AWS API Gateway, Kong, NGINX Plus, Envoy. Rate Limiting(토큰 버킷), Circuit Breaker(Hystrix-Resilience4j), OAuth 2.0 + JWT 검증, gRPC-Web 프록시 |
| **Service Mesh** | 서비스 간 통신 제어·관측·보안 | Istio(Envoy 기반), Linkerd, Consul Connect. mTLS 자동화, Traffic Mirroring(카나리), 분산 트레이싱(OpenTelemetry) |
| **Container Orchestrator** | 컨테이너 라이프사이클·스케줄링·자가치유 | Kubernetes(K8s) 1.30+, EKS/AKS/GKE, OpenShift. Control Plane(etcd+API Server+Scheduler) / Data Plane(kubelet+Proxy). HPA·VPA·Cluster Autoscaler 3단계 오토스케일링 |
| **Object Storage** | 비정형 데이터(PB~EB급) 저장 | S3(11 9s 내구성), GCS, Azure Blob. 3AZ 교차 복제, Lifecycle Policy(IA->Glacier), Pre-signed URL, Multipart Upload |
| **Key-Value Store** | 마이크로서비스용 저지연 NoSQL | DynamoDB(파티션 키 기반 10ms p99), Cosmos DB(Multi-Master), Cassandra. Eventually Consistent 기본, Read/Write Capacity 모드/On-Demand |
| **Message Broker** | 비동기 이벤트 스트리밍·디커플링 | Apache Kafka(파티션+Offset), RabbitMQ(AMQP 0-9-1), AWS SQS/SNS, EventBridge. Pub/Sub, CQRS, Saga 패턴 기반 분산 트랜잭션 |
| **CDN/Edge** | 정적 콘텐츠 캐싱, DDoS 방어 | CloudFront, Cloudflare, Akamai. Anycast, PoP(Point of Presence), Origin Shield, Brotli/Gzip 압축, HTTP/3(QUIC) |
| **Observability Stack** | Logs·Metrics·Traces 통합 관측 | Prometheus+Grafana+EFK/Loki, Datadog, New Relic. SLI/SLO/SLA 기반 SRE, RED(Req/Err/Duration) 메서드, USE(Utilization/Saturation/Errors) |

### 3. 핵심 알고리즘·프로토콜·수식

**① Auto Scaling 알고리즘 (Target Tracking)**
```
desiredReplicas = ceil(currentReplicas × currentMetricValue / targetMetricValue)
```
예: 현재 10개 Pod, CPU 80%, 목표 50% -> `10 × 80/50 = 16개 Pod` 자동 확장. KEDA(Event-Driven), Karpenter(Just-In-Time 노드 프로비저닝)가 차세대 스케일러.

**② CAP 정리와 PACELC 확장**
분산 시스템은 Consistency(C), Availability(A), Partition Tolerance(P) 3가지 중 최대 2가지만 만족 가능. 실제로는 P는 필연적이므로 C vs A 트레이드오프가 핵심. PACELC는 평상시(P 없을 때)에도 Latency(L) vs Consistency(C) 트레이드오프가 발생함을 명시. DynamoDB는 AP, Cosmos DB는 CP 튜닝 가능, RDBMS 단일 노드는 CA.

**③ Consensus 알고리즘 (Raft)**
Kubernetes etcd, CockroachDB가 채택. Leader Election(과반수 투표) + Log Replication(Append-Only) + Snapshot. Split-Brain 방지를 위해 Quorum(과반수) 합의 필수. 3-Node(1 Leader+2 Follower) 구성 시 1대 장애 허용, 5-Node 구성 시 2대 장애 허용.

**④ 일관성 모델 (Consistency Models)**
- Strong Consistency: 쓰기 후 모든 읽기에서 최신값 (RDBMS, etcd)
- Causal Consistency: 인과관계 순서 보장 (Cassandra LWW + Vector Clock)
- Eventual Consistency: 충분한 시간 후 수렴 (DynamoDB 기본)
- Read-Your-Writes: 본인 세션 일관성 (Sticky Session, Session Token)

- **📢 섹션 요약 비유**: API Gateway는 회사의 **종합 안내 데스크**와 같다. 손님(트래픽)이 어디로 가야 할지 안내하고, 출입증(JWT)을 확인하며, 너무 많은 손님이 몰리면 대기열(Rate Limit)을 만들어 시스템을 보호한다.

---

## Ⅲ. 비교 및 연결

### 1. 컴퓨트 서비스 모델 비교

| 구분 | IaaS | PaaS | SaaS | CaaS | FaaS (Serverless) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **추상화 수준** | HW 가상화 | 런타임+미들웨어 | 애플리케이션 | 컨테이너 | 함수 단위 |
| **고객 책임** | OS~App | App+Data | Data만 | Container Image | 코드만 |
| **프로비저닝 시간** | 분~시간 | 분 | 즉시 | 초~분 | 밀리초 |
| **과금 단위** | 인스턴스·시간 | 인스턴스·시간 | 사용자/월 | vCPU·메모리·초 | 실행 시간(ms)·호출 횟수 |
| **예시 서비스** | EC2, Compute Engine, Azure VM | Elastic Beanstalk, App Engine, Azure App Service | Office 365, Salesforce, Slack | EKS, AKS, GKE, Cloud Run | Lambda, Cloud Functions, Azure Functions |
| **적합 워크로드** | 레거시, 특정 HW 요구 | 웹앱, API 서버 | 일반 비즈니스 | MSA, CI/CD, 배치 | 이벤트 처리, 크론, 웹훅 |
| **Cold Start** | 없음 | 없음 | 없음 | 1~5초 | 100ms~10초 |
| **확장 한계** | 수백~수천 | 수백 | 제공자 정의 | 수천 Pod | 1000 동시실행(기본) |
| **상태 관리** | Stateful 가능 | Stateful 가능 | - | StatefulSet/PV | Stateless 전용 |

### 2. 배포 모델 비교


## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 687 / 800

<- **이전**: [686. 클라우드 아키텍처 핵심 토픽 686번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/686_cloud_architecture_core_topic_686_exam_summar/)
**다음**: [688. 클라우드 아키텍처 핵심 토픽 688번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/688_cloud_architecture_core_topic_688_exam_summar/) ->

---
