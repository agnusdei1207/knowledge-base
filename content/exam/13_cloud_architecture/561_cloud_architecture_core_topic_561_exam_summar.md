---
title: "Cloud Architecture Core Topic 561 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS의 서비스 모델과 Public/Hybrid/Multi-Cloud의 배치 모델을 기반으로, 컨테이너 오케스트레이션(Kubernetes), 서비스 메시(Istio/Linkerd), 이벤트 기반 비동기 아키텍처(EDA), IaC(Terraform/CloudFormation), GitOps(ArgoCD/Flux) 등의 CNCF(Cloud Native Computing Foundation) 표준 기술 스택을 조합하여 **탄력성(Elasticity)**, **회복탄력성(Resilience)**, **관측가능성(Observability)**을 코드로 구현하는 것이다.
> 2. **가치**: 적절한 클라우드 아키텍처는 CAPEX->OPEX 전환으로 초기 인프라 투자비 30~70% 절감, Auto-Scaling으로 트래픽 피크 시 응답지연 P99 기준 50% 이상 감소, Multi-AZ/Region 배포로 RTO(Recovery Time Objective) 분 단위, RPO(Recovery Point Objective) 초 단위 달성, FinOps 기반 비용 최적화로 클라우드 사용료 20~40% 절감이 가능하다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ① **일관성 vs 가용성**(CAP 정리에 따른 DB 선택 - RDBMS vs DynamoDB/Cassandra), ② **결합도 vs 자율성**(Monolith vs Microservices의 분산 트랜잭션/Saga 패턴), ③ **콜드 스타트 vs 비용**(Lambda vs EC2 On-Demand), ④ **관리형 서비스 종속(Vendor Lock-in) vs 운영 부담**(EKS vs Self-managed K8s)이며, 워크로드 특성·데이터 중력·컴플라이언스 요건을 기준으로 Well-Architected Framework 5대 기둥(운영 우수성, 보안, 신뢰성, 성능 효율, 비용 최적화)별로 의사결정해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 On-Premise 3-Tier 아키텍처는 수직 확장(Scale-Up) 방식의 고가 하드웨어, 수동 Capacity Planning, 정적 네트워크 구성, 수 일에서 수 주 단위 배포 주기로 인해 **Digital Transformation**의 요구사항인 "수 초 내 트래픽 폭증 대응, 하루 수십 회 배포, 글로벌 사용자 경험 균일화"를 충족할 수 없게 되었다. 2020년 COVID-19 팬데믹 이후 비대면 서비스 폭증, 5G/IoT 엣지 데이터 폭증, AI/ML 워크로드의 GPU 자원 수요 급증이 기존 인프라 한계를 노출시켰다.

클라우드 아키텍처는 AWS(2006), GCP(2008), Azure(2010) 등 Hyperscaler가 제공하는 **API 기반 프로그래머블 인프라**, **선불/종량 과금 모델**, **글로벌 리전(60+ Regions, 200+ Edge Locations)**을 활용하여, **인프라를 코드로**(Infrastructure as Code) 선언하고, **컨테이너를 오케스트레이션**하며, **관측가능성을 내재화**하는 패러다임이다. NIST SP 800-145에 정의된 5대 특성(요구 기반 셀프서비스, 광범위 네트워크 접근, 자원 풀링, 급탄력성, 측정 가능한 서비스)이 이를 뒷받침한다.

```text
+---------------------------------------------------------------------+
|                  클라우드 아키텍처 패러다임 전환 비교                 |
+---------------------------------------------------------------------+
|                                                                     |
|  [On-Premise 3-Tier - 2000s]              [Cloud-Native - 2020s]    |
|                                                                     |
|   사용자(PC)                              사용자(Mobile/Web/IoT)   |
|       |                                       |                     |
|   [Load Balancer]                       [Global LB / CDN / Edge]   |
|       |                                       |                     |
|   [Web Tier - WAS]                       [API Gateway / BFF]       |
|   (Stateless JSP/Servlet)                (Kong / Apigee / AWS APIGW)|
|       |                                       |                     |
|   [App Server]                           [Microservices Mesh]      |
|   (WebLogic/JBoss)                       (Istio Sidecar + K8s Pod)  |
|       |                                       |                     |
|   [RDBMS - Oracle/DB2]                   [Polyglot Persistence]    |
|   (SAN Storage, RAC)                     (RDS + DynamoDB + Redis)  |
|       |                                       |                     |
|   [물리 Rack + SAN]                      [Multi-AZ + EKS + Lambda] |
|                                                                     |
|  • 수직확장, 수동 배포,                     • 수평확장, GitOps,        |
|    수 일~수 주 프로비저닝                    수 초~수 분 프로비저닝    |
|  • CAPEX(고정자산)                         • OPEX(종량과금)          |
|  • SPOF(Single Point of Failure)           • Multi-AZ Active-Active  |
+---------------------------------------------------------------------+
```

기존 대비 변화의 핵심은 ① **추상화 레벨 상승**(하드웨어->가상화->컨테이너->서버리스), ② **API-First 설계**(모든 자원이 API로 제어), ③ **불변 인프라(Immutable Infrastructure)** + **카나리/블루그린 배포**, ④ **데브옵스/깃옵스 기반 지속적 배포(Continuous Delivery)**이다. Gartner는 2025년 기준 신규 디지털 워크로드의 95%가 클라우드-네이티브 플랫폼에 배포될 것으로 예측했다.

- **📢 섹션 요약 비유**: 기존 3-Tier 아키텍처가 "직접 짓고 관리하는 단독주택"이라면, 클라우드-네이티브는 "검증된 모듈식 아파트(컨테이너) 단지를 자동화 시스템(Istio+ArgoCD)이 운영하며, 입주(K8s Pod 생성)·퇴거(Auto-scaling down)·리모델링(롤링 업데이트)이 모두 자동인 스마트 시티"와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 크게 **4개 계층(Edge/Networking, Compute, Data, Orchestration/Operations)**으로 구성되며, 각 계층은 CNCF Landscape의 검증된 오픈소스 또는 Hyperscaler 관리형 서비스로 구현된다. 핵심 동작 원리는 **선언적(Declarative) Desired State**를 **컨트롤 루프(Control Loop)**가 수렴시키는 Kubernetes Reconciliation 패턴이며, 모든 계층에서 동일하게 적용된다.

```text
+----------------------------------------------------------------------+
|           Cloud-Native Reference Architecture (4+1 View)              |
+----------------------------------------------------------------------+
|                                                                      |
|  +--------------------------------------------------------------+   |
|  |  Edge & Global Networking Plane                              |   |
|  |  +--------+  +--------+  +---------+  +----------------+    |   |
|  |  |  CDN   |  | Route53|  |  WAF    |  |  Global Accel. |    |   |
|  |  |CloudFlr|-> |  DNS   |-> |(Layer 7)|-> |  Anycast IP    |    |   |
|  |  +--------+  +--------+  +---------+  +----------------+    |   |
|  +--------------------------+-----------------------------------+   |
|                             | TLS 1.3, mTLS                         |
|  +--------------------------v-----------------------------------+   |
|  |  Application & API Plane                                     |   |
|  |  +-------------+  +--------------+  +-----------------+     |   |
|  |  | API Gateway |-> | Service Mesh |-> |  Microservices  |     |   |
|  |  | (Kong/Envoy)|  | (Istio/Linkrd|  |  (Spring Cloud, |     |   |
|  |  | Rate Limit, |  |  Sidecar     |  |   gRPC, Dapr)   |     |   |
|  |  | Auth,Quota  |  |  mTLS,Canary |  |  + FaaS (Lambda)|     |   |
|  |  +-------------+  +--------------+  +-----------------+     |   |
|  +--------------------------+-----------------------------------+   |
|                             | Event Bus (Kafka/EventBridge)         |
|  +--------------------------v-----------------------------------+   |
|  |  Data Plane (Polyglot Persistence)                            |   |
|  |  +--------+  +---------+  +------+  +------+  +----------+  |   |
|  |  | RDBMS  |  |  NoSQL  |  |Cache |  |Object|  |Lakehouse |  |   |
|  |  |(Aurora)|  |(DynamoDB|  |(Redis|  |(S3)  |  |(Iceberg/ |  |   |
|  |  | OLTP   |  | Cassandra|  | Elasti| |      |  | Delta)   |  |   |
|  |  |        |  | Wide-Col.|  | Cache)|  |      |  |  OLAP    |  |   |
|  |  +--------+  +---------+  +------+  +------+  +----------+  |   |
|  +--------------------------+-----------------------------------+   |
|                             |                                       |
|  +--------------------------v-----------------------------------+   |
|  |  Platform & Orchestration Plane                               |   |
|  |  +----------+  +----------+  +----------+  +----------+      |   |
|  |  |  IaC     |  | Kubernetes|  | GitOps   |  | Observab.|      |   |
|  |  |Terraform |-> | EKS/AKS/  |-> | ArgoCD/  |-> |Prometheus|      |   |
|  |  |Pulumi/CDK|  | GKE/OKE  |  | Flux     |  | +Tempo + |      |   |
|  |  |          |  | + KNative|  | + Policy |  | Loki+Graf|      |   |
|  |  +----------+  +----------+  +----------+  +----------+      |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
|  Cross-Cutting: Security (Zero-Trust, OPA/Kyverno) + FinOps (Kubecost)|
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Edge/Global Plane** | 글로벌 트래픽 라우팅, DDoS 방어, TLS 오프로딩 | AWS CloudFront/Azure Front Door, Route 53 Latency-Based/Geolocation Routing, AWS WAF(OWASP Top 10 룰셋), Anycast EIP, TLS 1.3 + OCSP Stapling |
| **API Gateway & BFF** | North-South 트래픽 단일 진입점, 인증/인가, Rate Limiting, GraphQL Aggregation | Kong(OpenResty+Lua), Envoy + xDS API, AWS API Gateway(throttle 10K RPS), Spring Cloud Gateway, BFF(Backend-For-Frontend) 패턴으로 모바일/웹별 응답 최적화 |
| **Service Mesh (East-West)** | 서비스 간 mTLS, L7 라우팅, Circuit Breaker, 분산 추적, 카나리(5%->25%->100%) | Istio(Envoy Sidecar, 1앱=2Pod 구성), Linkerd(Linkerd2-proxy Rust 기반 1/10 리소스), Consul Connect, mTLS SPIFFE/SPIRE 기반 워크로드 아이덴티티 |
| **Container Orchestrator** | 선언적 Desired State 관리, Self-healing, HPA/VPA/Cluster Autoscaler | Kubernetes 1.30+, EKS Fargate(Serverless K8s), KARPENTER(Just-in-time 노드 프로비저닝, 30초 내 Ready), Pod Disruption Budget(PDB)로 자발적 중단 제어 |
| **Data Plane (Polyglot)** | 워크로드별 최적 저장소 선택, CQRS/Event Sourcing | Aurora(MySQL/PG 호환, 6-way 복제), DynamoDB Global Tables(Multi-Region Strong/Eventual), Redis Cluster(Sub-ms 응답), S3 Standard-IA/Glacier 티어링, Delta Lake(ACID on Parquet) |
| **GitOps Controller** | Git Repository = Single Source of Truth, Pull-based 동기화, Drift Detection | ArgoCD(ApplicationSet, App-of-Apps 패턴), Flux CD, OpenGitOps 표준 4원칙(Declarative, Versioned, Pulled, Continuously Reconciled) |
| **Observability Stack** | Metrics(RED/USE), Logs, Traces 상관관계 분석 | Prometheus + Grafana(Mimir for long-term), Loki(Label-based Log), Tempo/Jaeger(OpenTelemetry OTLP), eBPF 기반 Cilium Tetragon(런타임 보안) |
| **Policy as Code** | 컴플라이언스 자동 강제, Admission Control | OPA(Rego 정책), Kyverno(쿠버네티스 네이티브), Conftest(IaC 정적 분석), CIS Benchmark 자동 스캔 |

핵심 알고리즘/원리:

- **HPA (Horizontal Pod Autoscaler)**: `desiredReplicas = ceil(currentReplicas * currentMetricValue / targetMetricValue)`. KEDA(Kubernetes Event-Driven Autoscaling)로 Kafka Lag, SQS Queue Length, Cron 스케일까지 확장.
- **K8s Reconciliation Loop**: `if observedState ≠ desiredState: kube-scheduler/controller-manager가 reconcile()` -> 5단계(State, Diff, Apply, Observe, Loop) 반복. 이로써 **Eventual Consistency** 보장.
- **Saga Pattern**: 분산 트랜잭션을 ① Orchestration(Saga Orchestrator) 또는 ② Choreography(Event-driven with Compensation)로 구현. 2PC/XA 대비 가용성 높지만 Idempotency 보장 필수.
- **Consensus 알고리즘**: etcd는 Raft 합의 알고리즘(Log Replication, Leader Election, Term 증가)로 클러스터 일관성 유지. 쓰기 latency p99 = 10ms 수준.

- **📢 섹션 요약 비유**: 클라우드-네이티브 아키텍처는 "지휘자(K8s Control Plane)가 오케스트라(Container Pod) 단원들의 악보(Desired State YAML)를 보고 어긋난 음정(실제 상태)을 즉시 교정하는 자동 교정 시스템"이며, Service Mesh는 "단원들 사이의 호흡을 맞춰주는 이어피스"이다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처의 핵심 의사결정 지점인 **배포 모델**, **컴퓨트 추상화**, **데이터 저장소**, **오케스트레이션** 관점에서 비교한다.

| 구분 | Monolith vs Microservices | IaaS vs PaaS vs FaaS (Serverless) | Kubernetes(자체) vs EKS/AKS/GKE(관리형) |
| :--- | :--- | :--- | :--- |
| **아키텍처 특성** | 단일 코드베이스, In-Process 호출, Shared DB | 자원 프로비저닝 직접 vs 플랫폼 추상 vs 함수 단위 실행 | 클러스터 직접 운영 vs Control Plane 관리형 |
| **확장 단위** | 애플리케이션 전체 복제 | VM/Instance vs Container vs Function | 노드/Pod 단위 |
| **배포 독립성** | 불가(전체 재배포) | 부분 가능 | 서비스별 독립 |
| **장애 격리** | 프로세스 내 전파(Single JVM Down) | 컨테이너 경계(부분 격리) | Pod/Node 장애, 멀티 AZ 격리 |
| **운영 복잡도** | 낮음(Single Binary) | 중간 vs 높음 | 높음 vs 중간(관리형) |
| **콜드 스타트** | 없음(상시 기동) | 없음 vs 수 초 | 수 초~1분 vs N/A(관리형) |
| **적합 워크로드** | 소규모 CRUD, 레거시 | 범용 | MSA |
| **TCO (3년)** | 낮음(초기) -> 높음(성장
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 561 / 800

<- **이전**: [560. 클라우드 아키텍처 핵심 토픽 560번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/560_cloud_architecture_core_topic_560_exam_summar/)
**다음**: [562. 클라우드 아키텍처 핵심 토픽 562번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/562_cloud_architecture_core_topic_562_exam_summar/) ->

---
