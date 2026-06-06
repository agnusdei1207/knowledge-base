---
title: "Cloud Architecture Core Topic 782 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS·PaaS·SaaS의 서비스 모델과 Public·Private·Hybrid·Multi-Cloud의 배포 모델을 기반으로, 12-Factor App·Microservices·Serverless·Event-Driven·Service Mesh·Zero-Trust 보안 모델을 결합해 Workload의 탄력성(Elasticity), 가용성(HA), 회복력(Resilience)을 코드·인프라·정책 수준에서 동시에 달성하는 엔지니어링 패러다임이다.
> 2. **가치**: AWS Well-Architected Framework 5대 축(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화) 적용 시 평균 30~40%의 TCO 절감, Auto Scaling을 통한 60~80% 컴퓨팅 비용 절감, Multi-AZ·Multi-Region 구성을 통한 99.99%(Four 9s) 이상의 SLA 확보, MTTR 평균 70% 단축 등 정량적 효과를 입증할 수 있다.
> 3. **판단 포인트**: Lift-and-Shift vs Re-platform vs Re-architect의 마이그레이션 전략 6R(Rehost, Relocate, Replatform, Refactor, Repurchase, Retire) 선택, Stateful 서비스의 데이터 일관성 모델(Strong·Eventual·Read-your-writes) 결정, Vendor Lock-in 위험과 Multi-Cloud 추상화(Kubernetes, Terraform, Service Mesh) 균형, 그리고 CAP Theorem·Quorum 기반 가용성/일관성 트레이드오프가 핵심 의사결정 변수다.

---

## Ⅰ. 개요 및 필요성

전통적인 On-Premise 3-Tier 아키텍처(Presentation-Logic-Data)는 CAPEX 중심의 용량 계획, 수직 확장(Scale-Up)의 한계, 수동 장애 대응, 그리고 Peak Load 기준의 과잉 프로비저닝이라는 구조적 비효율을 내포한다. Netflix가 2008년 Oracle RAC에서 AWS Cassandra 기반 Cloud-native로 전환하며 1,000배 성장에서도 인프라 운영팀을 100명 미만으로 유지한 사례는 클라우드 아키텍처 전환의 대표적 정당성을 보여준다.

클라우드 아키텍처는 **API 기반 선언적 프로비저닝**(Terraform, CloudFormation, Pulumi), **불변 인프라(Immutable Infrastructure)**, **GitOps 기반 지속적 배포**(ArgoCD, Flux), **관측 가능성(Observability) 3요소**(Metrics·Logs·Traces - OpenTelemetry 표준), **Zero-Trust 보안 모델**(BeyondCorp, mTLS, SPIFFE/SPIRE)을 필수 구성으로 한다. NIST SP 800-145(클라우드 컴퓨팅 정의)와 ISO/IEC 22123은 클라우드의 5대 필수 특성(On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)을 규정한다.

```text
+---------------------------------------------------------------------+
|                    클라우드 아키텍처 패러다임 전환                    |
+------------------------------+--------------------------------------+
|   [Legacy On-Premise]        |      [Cloud-Native Architecture]      |
|                              |                                      |
|  +------------+              |  +------------+  +------------+     |
|  | Web Server |              |  | CloudFront |  |   WAF +   |     |
|  | (Tomcat)   |              |  |     CDN    |  | Shield DDos|     |
|  +-----+------+              |  +-----+------+  +-----+------+     |
|        |                     |        |               |            |
|  +-----v------+              |  +-----v---------------v------+     |
|  | WAS (Jeus) |◄-- 단일실패점 |  |  ALB/NLB + API Gateway     |     |
|  |   Cluster  |     (SPOF)   |  |  (Multi-AZ Active-Active)  |     |
|  +-----+------+              |  +-------------+--------------+     |
|        |                     |                |                     |
|  +-----v------+              |  +-------------v--------------+     |
|  | Oracle RAC |◄-- Scale-Up |  | EKS/ECS Fargate (POD Auto  |     |
|  |  Storage   |    한계     |  | Scaling HPA + Cluster AUto)|     |
|  +-----+------+              |  +-------------+--------------+     |
|        |                     |                |                     |
|  +-----v------+              |  +-------------v--------------+     |
|  | SAN/NAS    |◄-- 용량고정 |  | Aurora Global DB (Multi-   |     |
|  | (Storage)  |    (EBS gp3)|  | Region Read Replica + S3)  |     |
|  +------------+              |  +----------------------------+     |
|                              |                                      |
|  ❌ CAPEX 과다 / MTTR 수시간 |  ✅ OPEX / MTTR 분단 / Auto-Heal  |
|  ❌ 수동 스케일링              |  ✅ HPA: CPU>70% 시 30초 내 확장  |
|  ❌ Peak Load 과잉설계         |  ✅ 사용한 만큼 과금(Per-Second)   |
+------------------------------+--------------------------------------+
```

| 비교 항목 | Legacy On-Premise | Cloud-Native |
|:---|:---|:---|
| **프로비저닝 속도** | 수일~수주 (구매·설치) | 수십 초~수분 (API 호출) |
| **확장 단위** | 물리 서버 단위 (수직) | 컨테이너·함수 단위 (수평) |
| **장애 복구** | MTTR 평균 4~8시간 | MTTR 평균 5~15분 (Self-Healing) |
| **비용 구조** | CAPEX 80% / OPEX 20% | OPEX 100% (사용량 기반) |
| **거버넌스** | 수동 정책·절차 | Policy as Code (OPA, Sentinel) |
| **보안 모델** | Castle & Moat (Perimeter) | Zero-Trust (mTLS, Identity-Aware) |

- **📢 섹션 요약 비유**: On-Premise는 **자기 집**(집을 키우려면 땅 사고, 확장하려면 옆집 사야 함)이고, Cloud-Native는 **호텔 체인**(예약하면 즉시 방을 받고, 필요 없으면 즉시 체크아웃, 폭염엔 방을 더 늘리고 한파엔 줄임)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **5계층 책임 분담 모델**(Shared Responsibility Model) 위에서 동작한다. AWS 기준 Physical Infrastructure·Regions·Availability Zones는 CSP 책임, Compute·Storage·Network·DB는 사용자가 구성, OS·Middleware·Application·Data·IAM은 사용자 책임이다. 핵심 아키텍처 결정은 **도메인 경계 컨텍스트(Bounded Context)** 정의, **데이터 분산 전략**(Database per Service, Saga, Outbox), **동기/비동기 통신 패턴**(REST/gRPC vs Kafka/SQS/SNS) 선택에서 시작된다.

```text
+----------------------------------------------------------------------+
|         Cloud-Native Reference Architecture (EKS Based)              |
+----------------------------------------------------------------------+
|                                                                      |
|  [외부 사용자] --► Route 53 (Latency-Based) --► CloudFront (CDN)     |
|                                                       |              |
|                                            +----------v----------+   |
|                                            |  WAF + Shield Adv.  |   |
|                                            |  (OWASP Top 10 방어)|   |
|                                            +----------+----------+   |
|                                                       |              |
|                          +----------------------------v---------+    |
|                          |  API Gateway (Kong / AWS API GW)     |    |
|                          |  - JWT 검증 / Rate Limiting          |    |
|                          |  - OIDC + OAuth 2.0 / PKCE           |    |
|                          |  - Request Transformation            |    |
|                          +------------+---------------+---------+    |
|                                       |               |              |
|                  +--------------------v-+   +---------v--------+    |
|                  |  EKS Cluster (Multi-AZ)|   |  Lambda (Edge)   |    |
|                  |  +------------------+  |   |  - Image Resize  |    |
|                  |  | Istio Service    |  |   |  - Auth Pre-Proc  |    |
|                  |  | Mesh (mTLS,      |  |   +------------------+    |
|                  |  |  Canary, Retry)  |  |                            |
|                  |  +----+-----+----+---+  |                            |
|                  |       |     |    |      |                            |
|                  |  +----v-++--v--++v----+ |                            |
|                  |  |User  ||Order||Pay  | |                            |
|                  |  |Svc   ||Svc  ||Svc  | |                            |
|                  |  |POD×3 ||POD×5||POD×2| |                            |
|                  |  +------++-----++-----+ |                            |
|                  |  HPA: CPU>70% / Mem>75% |                            |
|                  |  PDB: minAvailable=2    |                            |
|                  +----------+--------------+                            |
|                             |                                          |
|        +--------------------+--------------------+                    |
|        |                    |                    |                    |
|   +----v-----+      +-------v------+     +-------v------+            |
|   | Aurora   |      | DynamoDB     |     | S3 + Glacier |            |
|   | Writer×1 |      | Global Table |     | (Object/    |            |
|   | Reader×2 |      | (NoSQL,      |     |  Data Lake) |            |
|   | Multi-AZ |      |  On-Demand)  |     |             |            |
|   +----------+      +--------------+     +--------------+            |
|                                                                      |
|  +-------------------------------------------------------------+    |
|  | Cross-Cutting Concerns                                       |    |
|  | • Observability: Prometheus + Grafana + Tempo (OTel)         |    |
|  | • Security: Vault (Secret), Falco (Runtime), Trivy (Image)   |    |
|  | • CI/CD: GitHub Actions -> ECR -> ArgoCD (GitOps)              |    |
|  | • Policy: OPA/Kyverno (Admission Control)                    |    |
|  +-------------------------------------------------------------+    |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Edge Layer** | DDoS 방어, 정적 콘텐츠 캐싱, TLS Termination | CloudFront·Cloudflare (Anycast), WAF Managed Rules (AWSManagedRulesCommonRuleSet), AWS Shield Advanced (L3/L4 자동 완화) |
| **API Gateway** | 인증·인가, Rate Limiting, API 버전 관리, 요청/응답 변환 | Kong Gateway(Plugin), AWS API Gateway(REST/HTTP/WebSocket), Apigee(API Analytics). OIDC + JWT 검증, Token Bucket 알고리즘 기반 Quota |
| **Service Mesh (Istio/Linkerd)** | 서비스 간 mTLS, Traffic Shifting(Canary 5->25->50->100%), Circuit Breaker, Retries, Observability | Envoy Proxy Sidecar injection, SPIFFE ID 기반 Identity, xDS API로 동적 설정 push, VirtualService + DestinationRule로 트래픽 제어 |
| **Container Orchestration (EKS/GKE/AKS)** | Pod 스케줄링, Self-Healing, Auto Scaling, Service Discovery | Kubernetes 1.30+ Control Plane, Karpenter로 Just-in-Time 노드 프로비저닝, HPA(v2: CPU/Mem/Custom), VPA, KEDA(이벤트 기반 0->N 스케일링) |
| **Serverless (Lambda/Functions)** | 이벤트 기반 stateless 워크로드, Cold Start 최적화 | AWS Lambda(128MB~10GB 메모리, 15분 타임아웃), Provisioned Concurrency로 Cold Start 100ms 이하, SnapStart(Java 11->10배 개선), EventBridge로 Event Bus 구성 |
| **Data Layer** | Polyglot Persistence, CQRS, Event Sourcing | Aurora(MySQL/PostgreSQL 호환, 최대 128TB, 6-way Replication), DynamoDB(Global Table Multi-Region Strong Eventually Consistent), S3 Standard-IA-Glacier 계층, ElastiCache(Redis Cluster Mode) |
| **Observability Stack** | Metrics(RED: Rate·Error·Duration), Logs, Traces | OpenTelemetry SDK(Trace/Meter/Log 통합), Prometheus + Grafana, Loki(Log Aggregation), Tempo/Jaeger(Distributed Tracing), CloudWatch X-Ray, Datadog APM |
| **Security & Compliance** | Zero-Trust, Secrets 관리, 이미지 보안, Runtime 방어 | SPIFFE/SPIRE(Workload Identity), HashiCorp Vault(Dynamic Secrets, Transit Encrypt), Trivy/Clair(이미지 CVE 스캔), Falco(비정상 Syscall 탐지), OPA/Kyverno(Policy as Code) |

**핵심 알고리즘 및 파라미터**:

- **Consistent Hashing**: DynamoDB·Cassandra의 Partition Key 분배, Virtual Node 150~200개로 Hotspot 완화, 해시 링 재배치 시 최소 키 이동
- **Raft Consensus**: etcd/Kubernetes, Quorum(과반수) 기반 Leader Election, Election Timeout 1~2초, Heartbeat 100~500ms, Log Replication with Term·Index
- **Token Bucket Rate Limit**: Capacity(버킷 크기) + Refill Rate(초당 토큰), Burst 허용, 429 응답 + `Retry-After` 헤더
- **Circuit Breaker**: Closed -> Open(연속 5회 실패 시) -> Half-Open(30초 후 1회 시도) -> Closed(성공 시 복귀), Hystrix·Resilience4j·Istio DestinationRule
- **Saga Pattern**: 2PC 회피, Choreography(Event-driven) vs Orchestration(Camunda·Step Functions), 보상 트랜잭션(Compensating Action) 명시
- **CAP Theorem 실전 매핑**: CP(Consistency + Partition Tolerance)= etcd·ZooKeeper·Aurora Synchronous, AP(Availability + Partition Tolerance)= DynamoDB·Cassandra·S3, CA(내부 네트워크 한정)= 단일 RDBMS

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **도시 인프라**다. Edge/CDN은 도시 외곽의 물류센터, API Gateway는 시청 민원창구, Service Mesh는 도로의 신호등·CCTV, Container는 택배 차량, Data Layer는 창고, Observability는 도시 관제센터, Security는 경찰·소방서다. 도시가 커져도 각 구성요소가 독립적으로 확장·복구된다.

---

## Ⅲ. 비교 및 연결

| 구분 | IaaS (EC2/GCE/Azure VM) | PaaS (Beanstalk/App Engine/Heroku) | CaaS (EKS/GKE/AKS) | FaaS/Serverless (Lambda/Cloud Functions) |
|:---|:---|:---|:---|:---|
| **제어 범위** | OS 미드웨어까지 | 런타임까지 | 컨테이너 스케줄러
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 782 / 800

<- **이전**: [781. 클라우드 아키텍처 핵심 토픽 781번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/781_cloud_architecture_core_topic_781_exam_summar/)
**다음**: [783. 클라우드 아키텍처 핵심 토픽 783번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/783_cloud_architecture_core_topic_783_exam_summar/) ->

---
