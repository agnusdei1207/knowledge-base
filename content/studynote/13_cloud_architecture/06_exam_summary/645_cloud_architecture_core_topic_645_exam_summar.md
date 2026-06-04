---
title: "645. 클라우드 아키텍처 핵심 토픽 645번 시험 요약 (Cloud Architecture Core Topic 645 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 645번 클라우드 아키텍처는 **Well-Architected Framework의 6대 축(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속가능성)**과 **Cloud-Native 12-Factor App 원칙**을 토대로, IaaS/PaaS/SaaS/FaaS의 책임 경계를 명확히 분리하고 컨트롤 플레인-데이터 플레인을 독립적으로 확장하는 분산 시스템 설계의 정수이다.
> 2. **가치**: AWS Well-Architected Review 기준으로 200~400% ROI, GCP 사례에서 컴퓨팅 비용 70% 절감·배포 시간 90% 단축, Azure Migration Program에서 3년 TCO 평균 49% 감소가 검증되었으며, MTTR을 전통 모놀리식 대비 65% 단축(예: Netflix EVCache/Chaos Monkey 기반)시킨다.
> 3. **판단 포인트**: **Lift & Shift vs Refactor vs Re-architect** 마이그레이션 전략, 단일 클라우드 종속(Vendor Lock-in) 회피를 위한 **추상화 계층(Kubernetes, Terraform, Multi-Cloud SDK)** 도입 여부, **CAP Theorem 기반 AP/CP 선택**, 그리고 **Egress 요금·Data Gravity·Latency Budget**이 클라우드 아키텍처의 4대 의사결정 변수다.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 IT 시스템은 2010년대 이후 **3-tier 모놀리식 아키텍처**(Web/App/DB 계층을 하나의 큰 애플리케이션으로 패키징하여 WAS에 배포)에서 **클라우드 네이티브 분산 아키텍처**(수십~수백 개의 마이크로서비스를 컨테이너로 패키징하여 오케스트레이터로 관리)로 급격히 전환되었다. 그 배경에는 (1) **IDC의 State of Digital Universe 보고서**(2025년 175 ZB 추정)에 따른 데이터 폭증, (2) **Gartner 예측**(2027년 전 엔터프라이즈 앱의 95%가 클라우드 네이티브)의 비즈니스 압력, (3) AWS Lambda(2014)·Kubernetes(2015)·Istio(2017) 등 핵심 플랫폼 성숙이 있다.

기술사 시험의 645번 토픽은 단순히 "클라우드를 쓴다"는 표층적 지식이 아니라, **클라우드 워크로드 설계 시 반드시 고려해야 하는 7대 의사결정**(① 컴퓨트 추상화 레벨 선택, ② 상태 관리 전략, ③ 서비스 간 통신 패턴, ④ 데이터 일관성 모델, ⑤ 관측 가능성 체계, ⑥ 비용 거버넌스, ⑦ 재해 복구 등급)을 다층적으로 판단할 수 있는 역량을 평가한다. 특히 **AWS·Azure·GCP·NCP·KT Cloud** 같은 퍼블릭 클라우드와 **OpenStack·Kubernetes** 같은 프라이빗 클라우드, 그리고 **Anthos·AKS Arc·EKS Anywhere** 같은 하이브리드/멀티 클라우드 오케스트레이션까지 포괄한다.

```text
+--------------------------------------------------------------------+
|        클라우드 아키텍처 진화 패러다임: 모놀리식 -> 분산형            |
+--------------------------------------------------------------------+
|                                                                    |
|  [Before: 2000~2010]              [After: 2015~현재]               |
|  +-----------------+              +-----------------------------+  |
|  |  Client (PC)    |              |  Mobile/Web/IoT/Edge Client |  |
|  +--------+--------+              +----------+------------------+  |
|           |                                  |                     |
|  +--------v--------+              +----------v------------------+  |
|  |  LB (F5/L7)     |              |  CDN + Edge (CloudFront/    |  |
|  +--------+--------+              |  Cloudflare/Akamai)         |  |
|           |                       +----------+------------------+  |
|  +--------v--------+                         |                     |
|  |  WAS Cluster    |              +----------v------------------+  |
|  |  (WebLogic/JBoss|              | API Gateway (Kong/Apigee/  |  |
|  |   단일 거대한   |              |   AWS API GW)               |  |
|  |   EAR 배포)     |              +----------+------------------+  |
|  +--------+--------+                         |                     |
|           |                       +----------v------------------+  |
|  +--------v--------+              | Service Mesh (Istio/Linkerd)|  |
|  |  Oracle/DB2     |              |  +- Auth, mTLS, Retry       |  |
|  |  (단일 RDBMS)   |              |  +- Circuit Breaker          |  |
|  +-----------------+              |  +- Traffic Split           |  |
|                                   +----------+------------------+  |
|                                              |                     |
|                                   +----------v------------------+  |
|                                   | Microservices (20~200 EA)   |  |
|                                   |  +- K8s Pod (Container)      |  |
|                                   |  +- Lambda/Functions         |  |
|                                   |  +- StatefulSet (DB)        |  |
|                                   +----------+------------------+  |
|                                              |                     |
|                                   +----------v------------------+  |
|                                   | Polyglot Persistence        |  |
|                                   |  +- RDBMS (Aurora/Cockroach)|  |
|                                   |  +- NoSQL (DynamoDB/Mongo)  |  |
|                                   |  +- Cache (Redis/Memcached) |  |
|                                   |  +- Warehouse (BigQuery/S3) |  |
|                                   +-----------------------------+  |
+--------------------------------------------------------------------+
```

**핵심 변화 포인트**: (1) **수직 확장(Scale-Up) -> 수평 확장(Scale-Out)**: 64코어 1TB RAM 단일 서버 대신 2코어 8GB 컨테이너 1,000개로 확장. (2) **Stateful -> Stateless**: 세션 정보를 Redis/ElastiCache로 외부화하여 어떤 인스턴스도 교체 가능. (3) **Push-based Deployment -> Pull-based GitOps**: Jenkins가 SSH로 배포하는 대신 ArgoCD가 Git Repo를 감시하여 자동 동기화. (4) **단일 장애점(SPOF) -> 다중 AZ/리전 이중화**: 한 데이터센터 정전에도 무중단 서비스. 이 변화는 단순한 기술 트렌드가 아니라 **CAP Theorem·Brewer's Conjecture**라는 분산 시스템 이론에 근거한 필연적 귀결이다.

- **📢 섹션 요약 비유**: 🏢 기존 식당은 **한 명이 모든 요리를 하는 주방**(셰프가 죽으면 식당도 폐업)이었지만, 클라우드 아키텍처는 **수십 명의 요리사가 각자 전문 요리(파스타·초밥·스테이크)를 만들고, 헤드 셰프(Orchestrator)가 주문을 분배하며, 보조 셰프(Replicas)가 즉시 투입**되는 구조다. 주방에 불이 나도(서버 장애) 음식은 계속 나온다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **책임 공분담 모델(Shared Responsibility Model)**을 기반으로, **컨트롤 플레인(Kubernetes API Server, AWS Control Tower)**과 **데이터 플레인(Pod, EC2 Instance)**을 분리하여 각각 독립적으로 확장·복구하는 것이다. 12-Factor App(Heroku 2011, Adam Wiggins)은 이를 12개의 원칙(① Codebase, ② Dependencies, ③ Config, ④ Backing Services, ⑤ Build/Release/Run, ⑥ Processes, ⑦ Port Binding, ⑧ Concurrency, ⑨ Disposability, ⑩ Dev/Prod Parity, ⑪ Logs, ⑫ Admin Processes)으로 체계화했다.

```text
+----------------------------------------------------------------------+
|         클라우드 네이티브 아키텍처: 5계층 + 횡단 관심사 분리           |
+----------------------------------------------------------------------+
|                                                                      |
|   [Layer 1: Edge/Client]                                              |
|   +--------------+  +--------------+  +--------------+                |
|   | Mobile App   |  | Web (React)  |  | IoT/Edge     |                |
|   +------+-------+  +------+-------+  +------+-------+                |
|          +------------------+------------------+                      |
|                             |                                         |
|   [Layer 2: Network Edge]      v                                      |
|   +-------------------------------------------------------------+    |
|   | CDN (CloudFront/Akamai) -> WAF (ModSecurity) -> DDoS Shield   |    |
|   | TLS 1.3 Termination / HTTP/3 / QUIC                          |    |
|   +--------------------------+----------------------------------+    |
|                              v                                        |
|   [Layer 3: Gateway/Mesh]                                             |
|   +--------------+  +--------------+  +--------------+                |
|   | API Gateway  |-> | Service Mesh |-> | Service Disc.|                |
|   | (Rate Limit, |  | (Istio/      |  | (Consul/     |                |
|   |  Auth, Trans)|  |  Linkerd)    |  |  Eureka)     |                |
|   +--------------+  +--------------+  +--------------+                |
|                              v                                        |
|   [Layer 4: Compute/Application]                                      |
|   +----------+  +----------+  +----------+  +----------+             |
|   | K8s Pod  |  | Lambda   |  | Cloud Run|  | VM/AMI   |             |
|   | (Stateless|  | (Event   |  | (Knative)|  | (Legacy) |             |
|   |  Container)| |  Driven) |  |          |  |          |             |
|   +----+-----+  +----+-----+  +----+-----+  +----+-----+             |
|        +--------------+--------------+-------------+                  |
|                              v                                        |
|   [Layer 5: Data/Storage]                                             |
|   +----------+  +----------+  +----------+  +----------+             |
|   | RDBMS    |  | NoSQL    |  | Object   |  | Stream   |             |
|   | (Aurora  |  | (DynamoDB|  | (S3/GCS  |  | (Kafka/  |             |
|   |  Multi-AZ|  |  Global  |  |  + Glacier)| Kinesis) |             |
|   |  Raft)   |  |  Tables) |  |          |  |          |             |
|   +----------+  +----------+  +----------+  +----------+             |
|                                                                      |
|   [Cross-Cutting Concerns]                                            |
|   +----------+  +----------+  +----------+  +----------+             |
|   | Obs.     |  | Security |  | IaC      |  | CI/CD    |             |
|   | (Prometheus| | (Vault/  |  | (Terraform| | (ArgoCD/|             |
|   |  + Grafana)| |  KMS/    |  |  Pulumi) |  |  Spinnaker)|           |
|   | + Loki/ELK| |  IAM/    |  |          |  |          |             |
|   | + Jaeger |  |  OPA)    |  |          |  |          |             |
|   +----------+  +----------+  +----------+  +----------+             |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 추상화 (Compute Abstraction)** | 워크로드 실행 단위 결정 | IaaS (EC2, Compute Engine) -> PaaS (App Engine, Beanstalk) -> CaaS (EKS, GKE, AKS) -> FaaS (Lambda, Cloud Functions) 순으로 추상화^ 운영부담v. 단, 콜드 스타트(Lambda 200~800ms), Vendor Lock-in, 디버깅 난이도 증가라는 트레이드오프 존재. |
| **오케스트레이터 (Orchestrator)** | 컨테이너 배치·스케일링·자가치유 | Kubernetes Control Loop: `Reconcile(actualState, desiredState)` 매 10초. **Scheduler**(bin-packing 알고리즘), **Controller Manager**(Deployment 1:1 보장), **etcd**(Raft 합의 알고리즘, Quorum = N/2+1) 3중화로 구성. |
| **서비스 메시 (Service Mesh)** | 서비스 간 통신·보안·관측 분리 | Sidecar 패턴(Envoy Proxy)을 Pod에 주입. **mTLS 자동 발급**(SPIFFE/SPIRE 기반 X.509 SVID), **트래픽 분할**(Canary 5%->25%->100%), **회로 차단기**(연속 5회 실패 시 Open 상태 30초). 데이터 플레인(Envoy) + 컨트롤 플레인(Istiod) 분리. |
| **API 게이트웨이** | 외부 트래픽 진입점·정책 적용 | OAuth 2.0 + JWT 검증, **Rate Limiting**(Token Bucket 알고리즘, 예: 100 req/s/user), **Request/Response Transformation**(JSON->XML, 필드 마스킹), **OpenAPI/Swagger 기반 계약 우선 개발**. Kong(Plugin 구조), Apigee(분석 강점), AWS API Gateway(서버리스 통합) 비교. |
| **오브젝트 스토리지 (Object Storage)** | 비정형 데이터(PB급) 저장 | S3 API 표준. **Erasure Coding**(Reed-Solomon 12+4, 99.999999999% 내구성), **Lifecycle Policy**(IA 30일->Glacier 90일->Deep Archive 365일), **Strong Consistency**(2020년 도입, GET 후 PUT 즉시 반영). Data Lake로 활용 시 Parquet/ORC 컬럼 형식 + Athena/Presto 쿼리. |
| **관계형 관리형 DB (Managed RDBMS)** | 트랜잭션 일관성·ACID 보장 | Aurora: 6-way 복제, Quorum 4/6 쓰기, 3/6 읽기로 **RPO=0, RTO<1분**. Google Spanner: **TrueTime API**(GPS+Atomic Clock)로 글로벌 Strong Consistency. CockroachDB: PostgreSQL 호환 + Raft 합의로 Multi-Region Active-Active. |
| **메시지 큐/스트림 (Messaging)** | 비동기·이벤트 기반 결합도 분리 | **Kafka**(Partition 기반 순서 보장, Exactly-Once Semantics는 Transactional API + Idempotent Producer 조합), **SQS**(최대 14일 보관, Visibility Timeout 중복 처리 방지), **Pub/Sub**(Pull 방식, Global Message Ordering 옵션). |
| **관측 가능성 (Observability)** | 로그·메트릭·트레이스 통합 | **3대 신호**: Logs(구조화 JSON, ELK/Loki), Metrics(4황금 신호 Rate/Error/Duration/Saturation, Prometheus), Traces(OpenTelemetry SDK, Jaeger/Tempo 분산 추적). **SRE Red/Black/USE/BRUM 메트릭** 체계. |

**핵심 알고리즘·파라미터 깊이 분석**:

1. **CAP Theorem (Brewer 2000, Gilbert-Lynch 2002 증명)**: 분산 시스템은 일관성(C), 가용성(A), 분할 내성(P) 중 **동시에 2개만 만족** 가능. 클라우드 선택: HBase/ZooKeeper = CP, DynamoDB/Cassandra = AP, RDBMS 단일 노드 = CA. **PACELC 확장**: 정상 시에도 Latency-Consistency 트레이드오프 존재.
2. **Consensus Algorithm (Raft)**: Leader Election(임의 Timeout 150~300ms) + Log Replication(과반수 ACK 시 Commit). etcd/MongoDB Atlas/CockroachDB의 기반. Paxos 대비 이해하기 쉬워 실사용 증가.
3. **Hash-based Consistent Routing**: DynamoDB/Cassandra의 `Partition Key -> MD
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 645 / 800

<- **이전**: [644. 클라우드 아키텍처 핵심 토픽 644번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/644_cloud_architecture_core_topic_644_exam_summar/)
**다음**: [646. 클라우드 아키텍처 핵심 토픽 646번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/646_cloud_architecture_core_topic_646_exam_summar/) ->

---
