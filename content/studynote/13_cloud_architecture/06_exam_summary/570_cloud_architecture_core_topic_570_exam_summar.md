---
title: "570. 클라우드 아키텍처 핵심 토픽 570번 시험 요약 (Cloud Architecture Core Topic 570 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS 계층 모델 위에 컨테이너 오케스트레이션(Kubernetes), 분산 트랜잭션(Saga/CQRS), 회복성 패턴(Circuit Breaker/Bulkhead), 옵저버빌리티(OpenTelemetry), IaC(Terraform/ArgoCD)를 통합한 12-Factor/App2Container 기반의 클라우드 네이티브 설계 체계이다.
> 2. **가치**: Auto-scaling으로 평균 40~70% 인프라 비용 절감, Multi-AZ/Region 구성으로 99.99% SLA 달성, MTTR(평균 복구시간)을 60분->5분 이내로 단축, 배포 빈도를 주 1회->일 수십 회로 증가시키는 DORA Elite 지표 달성이 가능하다.
> 3. **판단 포인트**: Trade-off는 (1) 일관성 vs 가용성(CAP), (2) Monolith 단순성 vs Microservices 복잡성, (3) 비용 최적화 vs 성능 여유율, (4) Vendor Lock-in 위험 vs 멀티클라우드 운영 부담, (5) 강한 일관성(Strong) vs 결과적 일관성(Eventual) 사이의 균형점이 핵심 의사결정 사항이다.

---

## Ⅰ. 개요 및 필요성

전통적 On-Premise 3-Tier 아키텍처는 최대 트래픽 기준으로 과다 설계(Over-provisioning)되어 평균 활용률 15~25%에 그치고, CAPEX 선투자와 6~12개월 구축 기간, 장애 발생 시 수동 대응(MTTR 평균 4~8시간)의 한계를 가진다. 2020년 이후 클라우드 네이티브 패러다임은 Kubernetes + Service Mesh + GitOps를 중심으로 진화하며, IDC 보고서(2024)에 따르면 글로벌 퍼블릭 클라우드 시장이 1조 달러를 돌파하면서 엔터프라이즈 아키텍처의 표준으로 자리잡았다.

기술사 관점에서 클라우드 아키텍처는 단순한 인프라 이전이 아니라 **분산 시스템 8대 함정(Fallacies of Distributed Computing)**을 명시적으로 다루는 설계 철학이다. 네트워크는 안정적이지 않고, latency는 0이 아니며, bandwidth는 무한하지 않고, 보안 위협은 내부에도 존재한다는 전제로 모든 컴포넌트를 설계해야 한다. Gartner Magic Quadrant(2024)에서 AWS·Azure·GCP가 3대 Hyperscaler로 분류되며, 한국 클라우드 시장은 NIPA 자료 기준 Naver Cloud·NHN Cloud가 독자 생태계를 구축 중이다.

```text
+------------------------------------------------------------------+
|            클라우드 아키텍처 패러다임 전환 (Before vs After)         |
+------------------------------------------------------------------+
|                                                                  |
|  [Before] On-Premise 3-Tier            [After] Cloud-Native      |
|  +------------------+                  +---------------------+   |
|  |   Web Server     |  --변화--->       |   CDN + WAF         |   |
|  |  (Apache/Nginx)  |                  |  (CloudFront/Akamai)|   |
|  +------------------+                  +---------------------+   |
|  |  App Server      |                  |  API Gateway        |   |
|  |  (WAS/Tomcat)    |                  |  (Kong/Apigee/ALB)  |   |
|  +------------------+                  +---------------------+   |
|  |   RDBMS          |                  |  Microservices      |   |
|  | (Oracle/MSSQL)   |                  |  (K8s+Istio+Envoy)  |   |
|  |   + SAN Storage  |                  |  + Polyglot DB      |   |
|  +------------------+                  |  (RDS/Dynamo/Mongo) |   |
|       |                               +---------------------+   |
|       v                                       |                  |
|  고정 CAPEX, 6개월 구축,                       v                  |
|  수동 스케일링, HA 어려움          Auto-scaling, 1일 배포,        |
|  라이선스 종속                       Pay-per-use, Open API       |
+------------------------------------------------------------------+
```

클라우드 아키텍처 도입 필요성은 다음 4가지 비즈니스 동력에서 비롯된다: ① **Time-to-Market** 단축(아이디어->배포까지 수개월->수시간), ② **Global Scale** 즉시 확보(리전 선택만으로 30+ 글로벌 PoP 활용), ③ **탄력성**(Black Friday급 100배 트래픽도 Auto-scaling으로 흡수), ④ **Innovation 접근성**(AI/ML·Quantum·Blockchain 같은 Managed Service 즉시 활용). 반대로 기술 부채(Technical Debt), 데이터 주권(데이터 반출 제한), 벤더 종속(Lock-in), 클라우드 비용 폭증(FinOps 부재)이라는 리스크도 동시에 고려해야 한다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **전기를 자체 발전소에서 만들지 않고 전력회사에서 사용한 만큼만 요금을 내는 모델**과 같다. 발전기(서버)를 살 필요 없이 콘센트(API)에 꽂기만 하면 되고, 에어컨을 새로 사면(스케일 아웃) 요금만 늘어나는 식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 클라우드 컴퓨팅 4계층 서비스 모델

NIST SP 800-145 표준에 따라 클라우드 서비스는 책임 분담(Shared Responsibility) 모델에 따라 4계층으로 분류된다. 각 계층마다 CSP(Cloud Service Provider)가 관리하는 범위와 고객이 관리하는 범위가 명확히 구분된다.

```text
+------------------------------------------------------------------------+
|              Cloud Service Model & Shared Responsibility                |
+------------------------------------------------------------------------+
|                                                                        |
|  책임범위  |  On-Premise  <---------------->  CSP Managed                |
|  ---------+------------------------------------------------------       |
|            |                                                            |
|  On-Prem  | [App][Data][Runtime][OS][Virt][Server][Storage][Network]   |
|           |                                                            |
|  IaaS     | [App][Data][Runtime][OS]  | [Virt][Server][Storage][Net]   |
|           |  <--- 고객 관리 --->          <----- CSP 관리 ----->            |
|           |   예: EC2, Azure VM, GCE                                   |
|           |                                                            |
|  PaaS     | [App][Data]              | [Runtime][OS][Virt][Server]...  |
|           |  <--- 고객 --->              <-------- CSP --------->          |
|           |   예: RDS, EKS, Cloud SQL, App Engine                      |
|           |                                                            |
|  SaaS     |                          | [App][Data][Runtime][OS]...     |
|           |  <------------------------ CSP 전체 관리 ----------->        |
|           |   예: Salesforce, Office365, Slack                          |
|           |                                                            |
|  FaaS     | [Code only]             | [Runtime][OS][Virt]...[Net]     |
|           |   <-- 고객 -->              <-------- CSP --------->          |
|           |   예: Lambda, Azure Functions, Cloud Functions             |
|           |   과금: 100ms 단위, Cold Start 200~800ms                    |
+------------------------------------------------------------------------+
```

### 2. 클라우드 네이티브 아키텍처 4계층 스택

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Infrastructure Layer** | 컴퓨팅·스토리지·네트워크 가상화 | AWS Nitro System, Azure Hyper-V, GCP Andromeda SDN; VM은 KVM/Hyper-V, Bare-metal은 i3.metal, GPU는 A100/H100 NVLink; 스토리지는 Block(EBS), Object(S3), File(EFS) 3-Tier |
| **Container & Orchestration** | 컨테이너 패키징 및 오케스트레이션 | Docker 24.x(OCI 표준), Kubernetes 1.30+(CNCF Graduated); Control Plane(API Server/etcd/scheduler) + Worker Node(kubelet/kube-proxy/cri); CNI(Calico/Cilium), CSI, CRI 런타임 표준 |
| **Service Mesh & API Gateway** | 트래픽 관리, mTLS, 관측 가능성 | Istio 1.22(Envoy 기반 Sidecar), Linkerd 2.15(BuchinRust 프록시), Consul Connect; L7 라우팅, 카나리 배포(Flagger), Circuit Breaking, Retries/Timeouts, mTLS 1.3 자동화 |
| **Application & Runtime** | 비즈니스 로직 실행 | MSA(Spring Boot 3/Quarkus/Go), Serverless(Lambda/CF Workers), Event-driven(Kafka/RabbitMQ/EventBridge), Saga Pattern, CQRS + Event Sourcing, Outbox Pattern |

### 3. 회복성(Resilience) 핵심 패턴 8가지

```text
+--------------------------------------------------------------------+
|           분산 시스템 회복성 패턴 (Resilience Patterns)              |
+--------------------------------------------------------------------+
|                                                                    |
|  1. Circuit Breaker (회로차단기)                                   |
|  +--------+   Closed   +---------+  실패율>임계치  +---------+    |
|  | Closed +------------>| Half-   +---------------->|  Open   |    |
|  | (정상) |   성공     |  Open   |   (N회 실패)    | (차단)  |    |
|  +--------+             | (시험)  |                 +----+----+    |
|       ^                 +----+----+                  Timer만료  |
|       |                      | 실패                        |      |
|       +------- 성공 ---------+                            v      |
|                                                       Half-Open   |
|   라이브러리: Resilience4j, Hystrix(legacy), Polly(.NET)         |
|                                                                    |
|  2. Bulkhead (격벽) - 스레드풀/Connection Pool 분리                |
|  +------+ +------+ +------+  한 서비스 장애가 전체로 전파 방지    |
|  |결제  | |검색  | |알림  |                                       |
|  |Pool  | |Pool  | |Pool  |  HikariCP, Tomcat maxThreads 분리    |
|  +------+ +------+ +------+                                       |
|                                                                    |
|  3. Retry + Exponential Backoff + Jitter                          |
|     재시도: 1s -> 2s(+jitter) -> 4s -> 8s (max 5회)                  |
|     멱등성(Idempotency Key) 필수: UUID 기반 dedup                  |
|                                                                    |
|  4. Timeout & Deadline Propagation                                 |
|     게이트웨이 5s -> 서비스 3s -> DB 2s (계층별 분배)               |
|                                                                    |
|  5. Rate Limiting & Throttling                                    |
|     Token Bucket(Redis Lua), Sliding Window, Leaky Bucket          |
|                                                                    |
|  6. Saga Pattern (분산 트랜잭션 보상)                              |
|     Orchestration(Temporal/Cadence) vs Choreography(EventBridge)  |
|                                                                    |
|  7. CQRS + Event Sourcing                                          |
|     Write/Read 모델 분리, 이벤트 로그로 상태 재구성                 |
|                                                                    |
|  8. Outbox Pattern (이벤트 발행 신뢰성)                            |
|     Transactional Outbox -> Debezium CDC -> Kafka                    |
+--------------------------------------------------------------------+
```

### 4. 클라우드 네이티브 12-Factor App 원칙 (Heroku)

| Factor | 핵심 | 실무 적용 |
| :--- | :--- | :--- |
| ① Codebase | 단일 코드베이스, 다중 배포 | Git Monorepo(Nx/Turbo), Trunk-based Development |
| ② Dependencies | 명시적 의존성 선언 | Maven/Gradle, Poetry, SBOM(Syft/Trivy) |
| ③ Config | 환경변수로 설정 분리 | Vault + External Secrets Operator, K8s ConfigMap/Secret |
| ④ Backing Services | DB/Queue를 첨부 가능한 리소스로 | RDS, ElastiCache, SQS를 URL로 추상화 |
| ⑤ Build/Release/Run | 단계 엄격 분리 | CI(빌드) -> CD(릴리스) -> ArgoCD(런) |
| ⑥ Processes | Stateless 프로세스 | 세션은 Redis/ElastiCache, 로컬 파일 금지 |
| ⑦ Port Binding | 자체 HTTP 포트로 서비스 | Spring Boot embedded Tomcat, FastAPI uvicorn |
| ⑧ Concurrency | 프로세스 모델로 확장 | HPA(K8s) + KEDA Event-driven Auto-scaling |
| ⑨ Disposability | 빠른 시작/优雅 종료 | PreStop Hook + 30s grace period, SIGTERM 처리 |
| ⑩ Dev/Prod Parity | 환경 일치 | Docker 이미지 불변, IaC(Terraform/Pulumi) |
| ⑪ Logs | 이벤트 스트림으로 취급 | stdout -> Fluent Bit -> Loki/Elasticsearch |
| ⑫ Admin Processes | 일회성 관리 작업 | kubectl exec, K8s Job/CronJob |

- **📢 섹션 요약 비유**: 12-Factor App은 **컨테이너 박스에 짐을 어떻게 싸야 효율적으로 배송할 수 있는가**에 대한 12가지 포장 규칙과 같다. 화물차(K8s)가 어디로 가든 똑같은 규격으로 포장되어야 안전하게 운송된다.

---

## Ⅲ. 비교 및 연결

### 1. 배포 모델 비교 (Public / Private / Hybrid / Multi-cloud)

| 구분 | Public Cloud | Private Cloud | Hybrid Cloud | Multi-Cloud |
| :--- | :--- | :--- | :--- | :--- |
| **소유/운영** | CSP(AWS/Azure/GCP) | 자체/전용 CSP | Public + Private 혼용 | 2개 이상 Public |
| **확장성** | 무제한 (수 분 내) | 제한적 (수 주) | 일부는 무제한 | 무제한 (벤더별) |
| **보안/규제** | 일반/금융규제 일부 | 완전 통제 | 핵심데이터는 On-Prem | 워크로드별 최적 |
| **TCO** | OPEX, Pay-per-use | CAPEX+OPEX | 통합 TCO 최적화 | 복잡한 비용 분석 |
| **Latency** | Region별 1~50ms | 내부 0.1~5ms | Interconnect 필요 | 벤더 라우팅 이슈 |
| **Lock-in 위험** | 높음 | 없음 | 중간 | 낮음 (단, 운영비^) |
| **적합 사례** | 신규 SaaS, 스타트업 | 금융/공공/의료 | 레거시+신규 병행 | 벤더 종속 회피, AI/ML 최적화 |
| **연결 기술** | Internet, Direct Connect | VPN, 전용선 | ExpressRoute, Interconnect | Transit Gateway, MCSB |
| **비용 효율** | 높음 (탄력성) | 중간 (고정비) | 높음 (워크로드 분산) | 낮음 (이중 운영) |
| **대표 사례** | Netflix, Airbnb | 정부 G-Cloud | 코엑스 하이브리드 | Spotify (GCP+AWS) |

### 2. 클라우드 마이그레이션 전략 (6R Framework - AWS)

| 전략 | 정의 | 변경 범위 | 비용 | 적용 사례 |
| :--- | :--- | :--- | :--- | :--- |
| **Rehost (Lift & Shift)** | 그대로 이전 | 인프라만 | 낮음 | 빠른 퇴거, PoC |
| **Replatform (Lift & Reshape)** | 일부 최적화 | 런타임/DB | 중간 | RDS 전환, 컨테이너화 |
| **Refactor (Re-architect)** | 클라우드 네이티브 재설계 | 앱 전체 | 높음 | MSA 분리, 서버리스 |
| **Repurchase (Drop & Shop
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 570 / 800

<- **이전**: [569. 클라우드 아키텍처 핵심 토픽 569번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/569_cloud_architecture_core_topic_569_exam_summar/)
**다음**: [571. 클라우드 아키텍처 핵심 토픽 571번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/571_cloud_architecture_core_topic_571_exam_summar/) ->

---
