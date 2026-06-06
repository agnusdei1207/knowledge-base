---
title: "Cloud Architecture Core Topic 648 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 **셀프서비스 API 기반의 탄력적 리소스 풀링(EBS-backed EC2, NVMe-oF, S3 Object Lambda)**, **세분화된 다중테넌시(Kubernetes Namespace+RBAC, VPC+Subnet)**, **선형 확장성(Horizontal Pod Autoscaler v2의 CPU/Memory/Custom/External 메트릭)**의 3대 NIST 특성을 토대로 CAP Theorem, Saga Pattern, CQRS+Event Sourcing을 통해 가용성·확장성·일관성 트레이드오프를 명시적으로 설계하는 것
> 2. **가치**: AWS Well-Architected Framework 6대 축(Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability) 적용 시 배포 빈도 200%^, MTTR 60%v, 인프라 비용 30~40% 절감(FinOps Foundation Benchmark 2023), SLA 99.99%(Four Nines) 달성을 통한 1년 Downtime 52.6분 이내 통제
> 3. **판단 포인트**: **Lift&Shift vs Re-platform vs Refactor** 마이그레이션 전략 선택, **Monolith->Microservices 분해 시 Domain-Driven Design Bounded Context 경계 설정**, **동기(REST/gRPC) vs 비동기(Kafka/SQS/EventBridge) 통신 패턴**, **Centralized(Spring Cloud Config) vs Decentralized(Consul+Vault) 거버넌스**, **Multi-Cloud Abstraction(Terraform/Pulumi) vs Cloud-Native Lock-in(AWS-only)**

---

## Ⅰ. 개요 및 필요성

전통적 3-Tier 온프레미스 아키텍처는 수직 스케일링(Scale-Up) 방식의 SAN/NAS 스토리지, 정적 용량 계획(Capacity Planning), 수동 프로비저닝, 야간 배치 중심의 동기 트랜잭션으로 구성되어 **CAPE(Cost, Availability, Performance, Elasticity)** 4대 제약에 부딪혔다. 2006년 AWS S3와 EC2 출시 이후 IaaS, 2011년 PaaS(GAE, Heroku), 2014년 CaaS(Docker+Kubernetes), 2019년 Serverless(AWS Lambda, Knative)의 4단계를 거쳐 **클라우드 네이티브(Cloud Native)** 패러다임이 정착되었다.

CNCF(Cloud Native Computing Foundation) 정의에 따르면 클라우드 네이티브는 **컨테이너, 서비스 메시, 마이크로서비스, 불변 인프라(Immutable Infrastructure), 선언형 API(Declarative API)**를 활용하여 자동화·관측가능·복원력 있는 느슨하게 결합된 시스템을 구축하는 접근법이다. 2024년 기준 전 세계 기업의 89%가 멀티클라우드 전략을 채택(HashiCorp State of Cloud Strategy Report)하고 있으며, Kubernetes는 컨테이너 오케스트레이션 시장 점유율 92%(CNCF Annual Survey 2023)를 기록하며 사실상 표준이 되었다.

```text
[전통적 온프레미스 vs 클라우드 네이티브 아키텍처 진화]

[1990s] Monolith          [2000s] Tiered           [2010s] SOA            [2020s] Cloud-Native
+--------------+         +--------------+         +--------------+         +--------------+
|   단일 WAR   |         |  Web/App/DB  |         |  ESB 중심    |         |  Microsvc ×N |
|   (Tomcat)   |         |  물리 서버   |         |  (WebSphere) |         |  (K8s Pod)   |
+------+-------+         +------+-------+         +------+-------+         +------+-------+
       |                        |                        |                        |
   년 1회 배포              분기 1회 배포              월 1~4회 배포              일 10~1000회 배포
   수동 스케일              Scale-Up                 Scale-Out                Auto-Scaling
   야간 배치                 야간 배치                CDC+ESB                  Event-Driven
   MTBF 기준                MTTR 부분 도입           MTTR 기준                SRE Golden Signals
```

**기존 방식 대비 클라우드 아키텍처의 본질적 차이**:
- **리소스 모델**: CapEx(자산) -> OpEx(소비 기반, Pay-per-use)
- **용량**: Fixed Capacity -> Elastic(CloudWatch+HPA+Cluster Autoscaler)
- **장애 대응**: Reactive(알람->수동복구) -> Proactive(Chaos Engineering, Litmus/Chaos Monkey)
- **배포**: 수동 FTP/Copy -> GitOps(ArgoCD/Flux), OPA(Open Policy Agent) 기반 Policy as Code
- **관측**: 로그 위주 -> **3 Pillars of Observability**(Metrics/Prometheus, Logs/Loki, Traces/Jaeger) + Continuous Profiling(Pyroscope)

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **전기 자동차와 같다**. 내연기관(온프레미스 Monolith)은 주기정비가 필요하고 변속기(로드밸런서 설정)를 직접 만져야 하지만, 전기차(클라우드 네이티브)는 OTA 업데이트(GitOps)로 성능이 개선되고 회생제동(Auto-Scaling)으로 에너지(비용)를 자동 절감한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **12-Factor App 원칙(Heroku, 2012)**, **Beyond the 12-Factor(Kevin Hoffman, 2016)**, **Cloud Native Triad(Container+Service Mesh+Observability)** 그리고 **5 Pillars of AWS Well-Architected Framework**의 교집합에 있다.

```text
[클라우드 네이티브 참조 아키텍처 - 5계층 + 횡단 관심사]

                    +-------------------------------------------------+
                    |   Layer 5: Edge & Delivery (CloudFront, ALB, API GW) |
                    |   + WAF / Shield / Rate Limiting                     |
                    +---------------------+-------------------------------+
                                          |
                    +---------------------v-------------------------------+
                    |  Layer 4: Application & Microservices               |
                    |  +------+  +------+  +------+  +------+  +------+   |
                    |  |Svc A |  |Svc B |  |Svc C |  |Svc D |  |Svc E |   |
                    |  +--+---+  +--+---+  +--+---+  +--+---+  +--+---+   |
                    |     |  Istio/Linkerd Service Mesh (mTLS, Canary)    |
                    +-----+----------+--------+--------+--------+--------+
                          |          |        |        |        |
                    +-----v----------v--------v--------v--------v--------+
                    |  Layer 3: API & Integration                        |
                    |  REST/gRPC(Envoy), GraphQL, EventBridge, Kafka     |
                    +-----+----------+--------+--------+--------+-------+
                          |          |        |        |        |
                    +-----v----------v--------v--------v--------v--------+
                    |  Layer 2: Runtime & Orchestration                  |
                    |  EKS/AKS/GKE/OKE + Karpenter + Istio + ArgoCD     |
                    |  Pod: liveness/readiness/startup probe             |
                    +-----+----------+--------+--------+--------+-------+
                          |          |        |        |        |
                    +-----v----------v--------v--------v--------v--------+
                    |  Layer 1: Infrastructure as Code (Terraform/Pulumi)|
                    |  VPC, Subnet, IAM, KMS, S3, EBS, RDS, DynamoDB     |
                    +----------------------------------------------------+

    +--------------------------------------------------------------------+
    | Cross-Cutting Concerns                                            |
    | Observability: Prometheus+Grafana+Loki+Jaeger+Tempo                |
    | Security:    Vault/AWS Secrets Manager+Cert-Manager+OPA+Kyverno   |
    | Resilience:  Hystrix/Resilience4j/Polly+Circuit Breaker+Bulkhead |
    | CI/CD:       GitHub Actions+Argo Rollouts+Flagger+Canary Analysis|
    +--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway** | 외부 트래픽 진입점, 인증/인가/속도제한 | AWS API Gateway(REST/WebSocket), Kong(nginx+Lua+OpenResty), Apigee(Apigee Adapter for Envoy). 스로틀링: Token Bucket(Rate=1000/s, Burst=2000) |
| **Service Mesh** | L7 트래픽 관리, mTLS 암호화, 카나리/블루그린 | Istio(Envoy xDS API, Control Plane: istiod), Linkerd(Linkerd2-proxy Rust, SMI), Consul Connect. mTLS 1.3 SPIFFE ID 기반 워크로드 아이덴티티 |
| **Container Orchestrator** | Pod 스케줄링, 자가치유, 선언적 상태 관리 | Kubernetes 1.30+ (kube-scheduler with Topology Spread, Pod Scheduling Readiness), Karpenter(Just-in-time 노드 프로비저닝, 30초 이내), Cluster Autoscaler vs Karpenter 비교: Karpenter가 Spot/ReUse 70%v 지연시간 |
| **Observability Stack** | 3 Pillars + Continuous Profiling | Prometheus(Cortex/Mimir, WAL 기반 TSDB), Grafana(10.4+ unified alerting), OpenTelemetry Collector(OTLP, 27개 Exporter), Loki(LogQL 2.0), Tempo(TraceQL), eBPF 기반 Cilium Tetragon |
| **Service Registry & Discovery** | 동적 인스턴스 등록, Health Check | Consul(DNS Interface, 3-Tier: Server/Client/Follower, Raft 합의), Eureka(Netflix OSS, AP), etcd(K8s 내부, CP, Raft, 8MB WAL, 1.5GB 권장) |
| **Distributed Coordination** | 분산 락, 리더 선출, 설정 공유 | etcd/Consul/ZooKeeper(ZAB), Redis(Redlock 알고리즘, Martin Kleppmann 논문 비판), Apache Curator(Recipes: Barrier/Cache/Counter) |
| **Resilience Pattern** | 장애 격리, 지연 차단, 폴백 | Hystrix(Deprecated, 유지보수 모드), Resilience4j(Java 17, 함수형, Spring Boot 3.x 통합), Polly(.NET), Sentinel(Alibaba, 동적 Rule). 핵심 메커니즘: Thread Pool Bulkhead vs Semaphore Bulkhead, Sliding Window(Count/Time-based) |

**12-Factor App 핵심 원리 (기술사 빈출)**:
1. **Codebase**: 단일 저장소(Trunk-Based Development, GitFlow->Trunk으로 전환), 다중 배포(Staging/Production)
2. **Dependencies**: 명시적 선언(`requirements.txt`, `package.json`, `go.mod`), 시스템 전역 암묵 의존 금지
3. **Config**: 환경변수 12-factor, **The Twelve-Factor App Config는 환경변수 사용 권장** -> Vault/AWS SSM Parameter Store로 secret 관리, .env는 git 제외
4. **Backing Services**: DB/Queue/Cache를 **Attached Resource**로 취급, URL로 추상화(`DATABASE_URL=postgres://...`)
5. **Build, Release, Run**: 3단계 엄격 분리, Build=Compile+Artifact, Release=Build+Config, Run=Container Start
6. **Processes**: Stateless 프로세스, Session은 Redis/Sticky Session 금지 (JWT+Refresh Token)
7. **Port Binding**: 자체 HTTP Port 노출, Tomcat 같은 App Server 임베드(Spring Boot 내장 Tomcat)
8. **Concurrency**: 프로세스 모델로 수평 확장, Process Type별 Worker 분리(API/Web/Queue)
9. **Disposability**: 빠른 Startup(Java Quarkus 0.5s vs Spring Boot 3s), Graceful Shutdown(SIGTERM 30s)
10. **Dev/Prod Parity**: Dev=Prod, docker-compose로 로컬 K8s와 동일 환경(K3d, kind, minikube)
11. **Logs**: 표준 출력(stdout/stderr) -> Fluent Bit/Vector로 수집 -> S3/Loki
12. **Admin Processes**: 일회성 작업도 동일 환경의 REPL 프로세스로 실행(K8s Job/CronJob)

**핵심 알고리즘/수식**:
- **CAP Theorem**: 분산 시스템은 Consistency, Availability, Partition Tolerance 중 2가지만 보장 가능. 실제 네트워크 분할(P)은 필연적이므로 **C vs A 트레이드오프**가 핵심 (CP: etcd/HBase, AP: Cassandra/DynamoDB)
- **Consistent Hashing**: Ring 구조로 노드 추가/제거 시 K/n개 키만 재매핑(K=키수, n=노드수), DynamoDB/Cassandra 파티셔닝의 기본
- **Quorum**: W+R>N (W=Write, R=Read, N=Replicas). Strong Consistency: W=R=⌊N/2⌋+1 (N=3, W=2, R=2)
- **Bloom Filter**: m 비트, k 해시 함수, n 원소, False Positive = (1-e^(-kn/m))^k -> 디스크 읽기 감소(DynamoDB LSI)
- **Token Bucket**: tokens += rate×Δt, max=capacity, 요청 시 tokens--. **AWS API Gateway 기본**: 10000 burst, 5000/s steady

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 5계층은 **현대 호텔 운영**과 같다. 로비(API Gateway)가 손님을 받고, 컨시어지(Service Mesh)가 룸서비스를 연결하며, 청소팀(Orchestrator)이 룸을 자동 정비한다. 객실(Container)은 언제든 변경 가능한 모듈식 구조이고, 전체 호텔 상태는 CCTV/관제실(Observability)에서 24시간 모니터링된다.

---

## Ⅲ. 비교 및 연결

**클라우드 아키텍처는 단일 기술이 아니라 디자인 결정의 집합**이므로, 유사/대안/선행 기술과의 비교를 통해 적합한 패턴을 선택해야 한다.

| 구분 | **Monolith** | **Modular Monolith** | **Microservices** | **Serverless (FaaS)** |
| :--- | :--- | :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/EAR | 단일 WAR (모듈 경계) | 서비스별 컨테이너 | 함수별 ZIP/Image |
| **확장성** | Scale-Up | 모듈 단위 컴파일 격리 | 독립적 HPA | 동시성 한도(1000/Lambda) |
| **장애 격리** | 전체 다운 | 모듈 간 결합도^ | Bulkhead+CB | Region/AZ 자동 격리 |
| **데이터 일관성** | 단일 ACID TX | 단일 ACID TX | Saga/CQRS/2PC | Eventual Consistency |
| **네트워크 비용** | In-process | In-process | 0.5~1ms gRPC | 50~200ms Cold Start |
| **운영 복잡도** | 낮음 | 중간 | 높음(8개 서비스부터) | 낮음(벤더 관리형) |
| **적합 사례** | 소규모, MVP | 중규모, 리팩토링 중 | 대규모, 50+ 엔지니어 | 비동기 이벤트, 스파이크 |
| **예시 기술** | Spring Boot WAR | Spring Modulith, ArchUnit | Spring Cloud/K8s/Istio | AWS Lambda, Vercel |

| 구분 | **IaaS (EC2)** | **PaaS (Beanstalk)** | **CaaS (EKS)** | **SaaS (Salesforce)** | **FaaS (Lambda)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **관리 주체** | OS, Runtime 직접 | App
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 648 / 800

<- **이전**: [647. 클라우드 아키텍처 핵심 토픽 647번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/647_cloud_architecture_core_topic_647_exam_summar/)
**다음**: [649. 클라우드 아키텍처 핵심 토픽 649번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/649_cloud_architecture_core_topic_649_exam_summar/) ->

---
