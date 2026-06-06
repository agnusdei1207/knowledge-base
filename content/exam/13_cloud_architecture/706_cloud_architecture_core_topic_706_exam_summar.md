---
title: "Cloud Architecture Core Topic 706 Exam Summary"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 **마이크로서비스, 서버리스, 컨테이너 오케스트레이션, IaC(Infrastructure as Code), API Gateway**를 기반으로 한 **탄력적·분산형·자동화** 시스템 설계 패러다임으로, AWS Well-Architected Framework의 6대 필러(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속 가능성)를 만족시켜야 한다.
> 2. **가치**: 온프레미스 대비 **TCO 30~60% 절감**, **Deployment Frequency 200배·Lead Time 2,555배** 향상(DORA Elite 기준), **Auto-Scaling**으로 Peak 트래픽 1,000% 변동에도 가용성 99.99% 유지, Multi-Region DR로 **RTO 1분·RPO 0초** 달성 가능.
> 3. **판단 포인트**: **Cloud-Native vs Cloud-Agnostic**(Kubernetes+Terraform) **vs 하이브리드(AWS Outposts/Azure Stack)** 트레이드오프, **EKS vs ECS vs Lambda** 워크로드 매칭, **동기식(Saga 보상 트랜잭션) vs 비동기식(EventBridge/SQS/Kafka)** 통신 패턴, **결정론적 비용 모델(Reserved/Savings Plan)** vs **탄력성 비용(On-Demand/Spot)**의 균형.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 IT 시스템은 2006년 AWS S3 출시 이후 **CapEx 기반 모놀리식 아키텍처**에서 **OpEx 기반 분산·클라우드 네이티브 아키텍처**로 급격한 패러다임 전환이 일어났다. 기술사 시험의 706번 클라우드 아키텍처 토픽은 이러한 전환의 핵심인 **클라우드 컴퓨팅 모델, 마이크로서비스 패턴, 무중단 배포, 자동 스케일링, 다중 리전 DR, FinOps, 클라우드 보안(Zero Trust)** 등을 통합적으로 다룬다.

기존 온프레미스는 **수직 확장(Scale-Up)**, **예측 기반 Capacity Planning**, **수동 배포(Waterfall)**, **단일 데이터센터**로 운영되어, **BizDevOps 정체·트래픽 폭증 대응 불가·초기 투자비 과다**라는 구조적 한계를 가졌다. 반면 클라우드 아키텍처는 **수평 확장(Scale-Out)**, **선언적 오토스케일링(예: HPA·KEDA)**, **불변 인프라(AMI/Container Image)**, **GitOps(ArgoCD/Flux)** 기반의 **Day-2 Operation 자동화**로 전환되었다.

NIST SP 800-145의 정의에 따르면 클라우드 컴퓨팅은 5대 필수 특성(**On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service**)과 3대 서비스 모델(**IaaS/PaaS/SaaS**), 4대 배포 모델(**Public/Private/Hybrid/Community**)을 갖는다. 기술사 답안 작성 시 **CSP(Cloud Service Provider) 책임 분담 모델(Shared Responsibility Model)**을 명확히 이해하고, **"클라우드 = SaaS"라는 잘못된 통념을 교정**하는 것이 평가 포인트가 된다.

```text
[클라우드 아키텍처 진화 흐름도: 워크로드 중심 -> 자동화 중심 -> 비즈니스 중심]

  +--------------------------------------------------------------+
  | Stage 1: LIFT & SHIFT (단순 이전, 2008~2014)                |
  |  +------------+    1:1 마이그레이션     +-----------------+   |
  |  |  Monolith  | ------------------->  |  EC2/VM (IaaS)  |   |
  |  |  on-Prem   |   IP/Port/Code 보존   |  Lift & Shift   |   |
  |  +------------+                       +-----------------+   |
  |       ⚠ 비용 절감 미미, 클라우드 이점 미활용 (TCO 10%v)      |
  +--------------------------------------------------------------+
                              |
                              v
  +--------------------------------------------------------------+
  | Stage 2: CLOUD-NATIVE (재설계, 2015~2020)                    |
  |  +------------+   Refactor   +-----------------------------+ |
  |  |  Monolith  | ------------> |  Microservices + Containers  | |
  |  |            |              |  12-Factor App + API Gateway | |
  |  +------------+              +-----------------------------+ |
  |       ✅ Auto-Scaling, Resilience, DevOps 파이프라인 구축      |
  +--------------------------------------------------------------+
                              |
                              v
  +--------------------------------------------------------------+
  | Stage 3: CLOUD-INTELLIGENT (AI·지능형 자동화, 2021~현재)     |
  |  +------------+   AIOps    +--------------------------------+|
  |  |  K8s Mesh  | ----------> |  Serverless + AI/ML Inference  ||
  |  |  Observ.   |  FinOps    |  GitOps + Policy as Code       ||
  |  +------------+   FinOps   +--------------------------------+|
  |       ✅ Self-Healing, Cost-Aware, Sustainability-aware      |
  +--------------------------------------------------------------+
```

기술사 출제 트렌드(2020~2025 분석)상 **"Hybrid/Multi-Cloud 전략 수립"**, **"MSA 전환 시 데이터 정합성 확보 방안"**, **"FinOps 기반 비용 최적화"** 가 빈출하며, 단순 암기형이 아닌 **아키텍처 의사결정 정당화(ADR: Architecture Decision Record)** 능력을 평가한다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처 진화는 마치 **"개인 식당(온프레미스) -> 프랜차이즈 직영점(IaaS) -> 중앙 주방 시스템 + 배달 플랫폼(CNCF/Serverless)"** 으로의 변화와 같다. 손님(트래픽)이 1,000명 늘어도 주방(Kitchen Pod)이 자동으로 확장되고, AI가 인기 메뉴를 예측 발주(FinOps)하는 단계까지 온 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **다층 레이어드(Layered) + 이벤트 드리븐(Event-Driven) + 메시지 기반(Message-Driven)** 하이브리드 토폴로지가 표준이다. 핵심은 **"Loose Coupling"** 과 **"Stateless"** 이다. 이를 실현하기 위해 **12-Factor App**(2012, Heroku) 원칙과 **CNCF Trail Map**(Container, CI/CD, Orchestration, Observability, Service Mesh, Distributed Tracing)을 따라야 한다.

### 마이크로서비스 아키텍처 상세 흐름

```text
[API Gateway -> Service Discovery -> Circuit Breaker -> Saga 패턴 상세 흐름]

   Client/Mobile          Edge Layer             Service Mesh         Internal Services
  +----------+    HTTPS  +----------------+                       +--------------+
  |          | ---------> |   CloudFront   |                       |  Order Svc   |
  |   User   |   JWT    |   (CDN/WAF)    |                       |  (Java/SB)   |
  |          | <--------- |  + WAF Rules   |                       +------+-------+
  +----------+   TLS1.3 +--------+-------+                              | gRPC
                                | /api/*                                v
                                v                                +--------------+
                       +----------------+  Route53 Weight        | Payment Svc  |
                       |  API Gateway   | --------------->        | (Go/Gin)     |
                       |  (REST+GraphQL)|                        +------+-------+
                       | + Lambda Auth  |                               |
                       +--------+-------+                               v
                                | JWT Verify                     +--------------+
                                v                                |  Inventory   |
                       +----------------+  mTLS via Istio        |   (Python)   |
                       |  Service Mesh  | --------------->        +------+-------+
                       |  (Istio/Linkerd)|                               |
                       |  Sidecar Proxy  |                               v
                       +--------+-------+                       +--------------+
                                | Retry/CB/Tracing               |  DB Cluster  |
                                v                                | (Aurora/Cockroach)
                       +----------------+                       +--------------+
                       |  Event Bus     |
                       | (Kafka/EventBridge/SQS)  <------------ Saga Choreography
                       +----------------+
```

### 핵심 구성 요소 분해

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Edge / CDN** | 정적 콘텐츠 캐싱, DDoS 방어, TLS Termination | AWS CloudFront, Cloudflare, Akamai — Lambda@Edge로 응답 시 5~50ms 단축 |
| **API Gateway** | 인증/인가, Rate Limiting, 라우팅, 프로토콜 변환 | Amazon API Gateway(10,000 RPS), Kong, Apigee — OpenAPI 3.0/Swagger 기반 컨트랙트 우선 설계 |
| **Service Mesh** | Sidecar Proxy로 L7 트래픽 제어, mTLS, 관측 가능성 제공 | Istio(Envoy), Linkerd, Consul Connect — 0 코드 변경으로 정책·관측·보안 통합 |
| **Container Orchestrator** | Pod 스케줄링, Self-Healing, 선언적 상태 유지 | Kubernetes(K8s) 1.30+, EKS/GKE/AKS — Control Plane(API Server/etcd) + Data Plane(Kubelet) |
| **Serverless FaaS** | 이벤트 기반 stateless 함수 실행, 과금 100ms 단위 | AWS Lambda(15분 timeout, 10GB RAM), Azure Functions, GCP Cloud Run — Cold Start 이슈: SnapStart/Provisioned Concurrency로 해결 |
| **Managed Database** | 자동 백업, Multi-AZ, Read Replica, PITR | Aurora(MySQL/Postgres, 6-way 복제), DynamoDB(Global Tables), Cosmos DB(Multi-Master) |
| **Observability Stack** | 메트릭/로그/트레이스 통합 수집(CNCF Observability Whitepaper) | Prometheus + Grafana + Loki + Tempo(PLG) 또는 OTel + Datadog/New Relic |

### 분산 트랜잭션 처리 — Saga 패턴 (핵심 기술사 포인트)

단일 DB 트랜잭션(ACID)이 불가한 MSA 환경에서 **결과적 일관성(Eventual Consistency)** 을 보장하는 두 가지 방식:

1. **Orchestration(중앙 통제)**: `OrderSaga` Orchestrator가 각 서비스에 보상 트랜잭션을 순차 호출 — Temporal/Cadence/AWS Step Functions 사용
2. **Choreography(분산 이벤트)**: 각 서비스가 도메인 이벤트(`OrderCreated` -> `PaymentProcessed` -> `InventoryReserved`) 발행/구독 — Kafka/EventBridge 사용, 결합도 v, 디버깅 ^

### 글로벌 부하 분산 — Multi-Region Active-Active

```text
[AWS Global Accelerator + Route 53 Latency-Based Routing + Aurora Global Database]

            +--------------------------------------------+
            |            Client (Global Users)            |
            +--------------+-----------------------------+
                           | Anycast IP (Global Accelerator)
                           v
        +------------------+------------------+
        |                                     |
        v                                     v
  +------------+                       +------------+
  |  us-east-1 |  Route 53 Health      |  ap-northeast-2|
  |   (Active) |  Check (30s)          |    (Active)     |
  |  +------+  |                       |  +------+       |
  |  | ALB  |  | <--- Aurora Global ---> |  | ALB  |       |
  |  | ECS  |  |   Cross-Region Replica |  | ECS  |       |
  |  +------+  |   (Storage-based, RPO<1s)|  +------+       |
  +------------+                       +-------------------+
        |                                       |
        +--------------+------------------------+
                       v
            +----------------------+
            |  S3 Cross-Region     |
            |  Replication (CRR)   |
            |  + CloudFront OAC    |
            +----------------------+
```

**핵심 알고리즘·파라미터**:
- **Consistent Hashing**: DynamoDB Partition Key, Cassandra Ring — 데이터 분산 및 리밸런싱 비용 최소화
- **CAP Theorem**: 분산 시스템는 Consistency·Availability·Partition Tolerance 중 2개만 선택 가능 -> AP(DynamoDB, Cassandra) vs CP(etcd, ZooKeeper) vs CA(불가능, P는 필연)
- **Bulkhead Pattern**: Thread Pool/Connection Pool을 서비스별로 분리 -> 한 서비스 장애가 시스템 전체로 전파 차단 (Hystrix, Resilience4j)
- **Circuit Breaker**: Closed -> Open(임계치 초과) -> Half-Open(테스트) -> Closed 상태 머신, 임계치: 50% 실패율·20회 윈도우

- **📢 섹션 요약 비유**: 클라우드 MSA는 **"대형 호텔의 직영 시스템"** 과 같다. 프런트 데스크(API Gateway)·하우스키핑(Order)·레스토랑(Payment)·주방(Inventory)·배관(Kafka)·소방(Istio Security)이 각자 독립 부서로 분리되어, 한 곳이 죽어도 호텔 전체는 돌아간다. 단, 객실 상태(Room=DB)를 항상 동기화하기 위해 **하우스키핑 간 통신(Saga)** 규약이 필수다.

---

## Ⅲ. 비교 및 연결

### 서비스 모델 비교 (IaaS / PaaS / SaaS / FaaS)

| 구분 | IaaS (예: EC2) | PaaS (예: Elastic Beanstalk) | SaaS (예: Salesforce) | FaaS (예: Lambda) |
| :--- | :--- | :--- | :--- | :--- |
| **관리 범위 (CSP 책임)** | HW, Network, Storage | + OS, Runtime | + App, Data | + Runtime + Auto-Scaling 전부 |
| **사용자 책임** | OS Patch, Middleware, App, Data | App Code, Data | Data 입력·구성 | 함수 코드 + 트리거 |
| **확장성** | 수동/Auto Scaling Group | 컨테이너 오토스케일 | SaaS 제공자 정책 | 자동(0->N->0) |
| **과금 단위** | Instance-hour | Instance-hour + Service | Per-User / Per-Month | GB-Second, Invocation Count |
| **적합 워크로드** | 레거시 이전, 커스텀 HW | 웹앱 빠른 배포 | CRM·문서·협업 | 이벤트 처리, Cron, API |
| **TCO 우위 시점** | 장기 상주시 유리 | 트래픽 30% 변동 | 사용자 100명 이상 | 간헐적 트래픽(<15분) |
| **예시 기술** | EC2, GCE, Azure VM | Beanstalk, App Engine, Her
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 706 / 800

<- **이전**: [705. 클라우드 아키텍처 핵심 토픽 705번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/705_cloud_architecture_core_topic_705_exam_summar/)
**다음**: [707. 클라우드 아키텍처 핵심 토픽 707번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/707_cloud_architecture_core_topic_707_exam_summar/) ->

---
