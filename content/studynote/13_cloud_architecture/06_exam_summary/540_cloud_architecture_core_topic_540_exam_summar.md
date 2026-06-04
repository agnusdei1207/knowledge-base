---
title: "540. 클라우드 아키텍처 핵심 토픽 540번 시험 요약 (Cloud Architecture Core Topic 540 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 Well-Architected Framework(보안·신뢰성·성능효율·비용최적화·운영우수·지속가능성 6대 필러) 기반 하에, 마이크로서비스·서버리스·컨테이너 오케스트레이션(Kubernetes)·서비스 메시(Istio/Linkerd)·IaC(Terraform/CloudFormation)를 통합하여 워크로드의 탄력성, 무중단 배포, 분산 트랜잭션을 보장하는 설계 패러다임이다.
> 2. **가치**: AWS Well-Architected Review 적용 조직 평균 25~40% TCO 절감, EKS/AKS/GKE 기반 컨테이너 오토스케일링으로 Peak 시 70% 이상 응답지연 단축, 카나리/블루그린 배포로 무중단 가용성 99.99% SLA 달성, FinOps 도입으로 클라우드 지출 최적화 20~30% 실현.
> 3. **판단 포인트**: 모놀리스->마이크로서비스 분해 시 도메인 경계(DDD Bounded Context) 정의, 동기(REST/gRPC) vs 비동기(Kafka/EventBridge) 통신 비율, Cell-Based/Zonal Redundancy/Multi-Region Active-Active 아키텍처 선택, IAM Zero Trust + CSPM(Cloud Security Posture Management) 적용 여부가 장애 격리·보안 사고 대응 능력의 결정적 분기점.

---

## Ⅰ. 개요 및 필요성

전통적 3-Tier On-Premise 아키텍처는 CAPEX 중심의 정적 용량 계획, 수직적 확장(Scale-Up) 한계, MTTR 평균 4~8시간, IDC 시설 운영 부담(전력·냉각·회선)이라는 구조적 문제에 직면했다. 클라우드 아키텍처는 가상화(KVM/Xen)->컨테이너화(Docker)->오케스트레이션(Kubernetes)->서버리스(FaaS)->에지 컴퓨팅으로 진화하며, **가용 리소스의 추상화**, **API 기반 셀프서비스 프로비저닝**, **Pay-per-Use 과금 모델**을 통해 비즈니스 민첩성을 제공한다. 디지털 전환(DX) 가속화로 트래픽 패턴이 예측 불가능해지면서, Auto Scaling + HPA(Horizontal Pod Autoscaler) + KEDA(Event-driven Autoscaling) 기반의 탄력적 아키텍처는 더 이상 선택이 아닌 필수다. Gartner 2024 보고서에 따르면, 전체 엔터프라이즈 워크로드의 70% 이상이 2027년까지 클라우드 네이티브 방식으로 재설계될 것으로 전망된다.

```text
[전통적 아키텍처 -> 클라우드 네이티브 아키텍처 진화]

On-Premise 3-Tier        IaaS 기반          PaaS/Container       Cloud-Native MSA
+--------------+      +--------------+   +--------------+    +--------------+
|  Web Server  |      |   EC2/VM     |   |  ECS/EKS     |    |  Pod+Service |
+--------------+      +--------------+   +--------------+    |     Mesh     |
| App Server   | ---► | Auto Scaling |--►| Fargate/     |--► | Lambda+FaaS  |
+--------------+      |    Group     |   | Lambda       |    | EventBridge  |
|   RDBMS      |      +--------------+   +--------------+    +--------------+
|  (Oracle)    |      |      RDS     |   | Aurora/Dynamo|    | DynamoDB+S3  |
+--------------+      +--------------+   +--------------+    +--------------+
   CAPEX 중심            OPEX 전환        컨테이너 오케스트    Serverless 극대화
   수직확장 한계         인스턴스 단위       선언적 배포          이벤트 기반
   6개월~1년 구축        1주~1개월         IaC 자동화           ms 단위 Billing
   99.9% SLO             99.95% SLA        99.99% 가용          무한 확장
   MTTR 4~8H             MTTR 1H           MTTR 분 단위         MTTR 초 단위
```

```text
[Cloud-Native Reference Architecture (CNCF Landscape 기반)]

                          +---------------------------------+
                          |   GitOps / CI-CD Pipeline       |
                          |  (ArgoCD / Flux / JenkinsX)     |
                          +----------------+----------------+
                                           | (Sync)
       +-----------------------+-----------+----------+------------------------+
       |                       |                      |                        |
+------v------+         +------v------+        +-----v-----+         +--------v--------+
|  Observability|       | Service Mesh|        |  API GW   |         |    Security     |
| (Prometheus+ |       | (Istio/     |        | (Kong/    |         | (Vault/Cert-    |
|  Grafana +   |       |  Linkerd/   |        |  Apigee/  |         |  Manager/OPA)   |
|  Loki+Tempo) |       |  Consul)    |        |  AWS AGW) |         |                 |
+------+------+         +------+------+        +-----+-----+         +--------+--------+
       |                       | mTLS/Traffic Mgmt    | Auth/Throttle           | Secret/IAM
       |                       |                      |                        |
       +-----------------------+----------+-----------+------------------------+
                                          |
                                +---------v---------+
                                |  Kubernetes (EKS/ |  <--- CNI: Calico/Cilium
                                |   AKS/GKE/OKE)    |  <--- CRI: containerd
                                |  + Operators      |  <--- CSI: EBS/EFS/CSI
                                +---------+---------+
                                          |
                +-------------------------+--------------------------+
                |                         |                          |
         +------v------+           +------v------+            +------v------+
         | StatefulSet |           | Deployment  |            |   FaaS      |
         | (DB/Queue)  |           | (Stateless) |            | (Lambda/    |
         |  + PVC      |           | + HPA/VPA   |            |  CloudFunc) |
         +-------------+           +-------------+            +-------------+
```

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **전기를 자체 발전소(On-Prem)에서 모든 가정용 전기까지 직접 만들어 쓰던 시대**에서, **한전(NCP/Public Cloud)이 24시간 안정적으로 전기를 공급하고, 사용한 만큼만 요금을 내는 모델**로 전환한 것과 같다. 발전기 고장·정전은 한전이 책임지고, 우리는 전기를 쓰는 가전제품(서비스) 개발에만 집중할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 클라우드 컴퓨팅 서비스 모델 (NIST SP 800-145 기준)

| 모델 | 추상화 수준 | 제공 범위 | 대표 서비스 | 기술사 출제 포인트 |
|:---|:---|:---|:---|:---|
| **IaaS** | VM/Network/Storage | 인프라 전체 | EC2, Azure VM, GCE, Compute Engine | 가상화(KVM), 하이퍼바이저, 베어메탈 비교 |
| **PaaS** | Runtime+Middleware+OS | 앱 실행환경 | Elastic Beanstalk, App Service, App Engine | Lock-in 위험, Platform 종속성 |
| **SaaS** | Application | 완성된 앱 | Office 365, Salesforce, Workday | Multi-Tenancy, 데이터 격리 |
| **FaaS** | Function | 코드 단위 | Lambda, Azure Functions, Cloud Functions | 콜드 스타트, 동시성, 실행 시간 15분 한계 |
| **CaaS** | Container | 컨테이너 런타임 | EKS, AKS, GKE, ECS | K8s 관리 책임 분담(Managed vs Self-hosted) |

### 2. 클라우드 배포 모델

- **Public Cloud**: 다중 테넌트, Shared Responsibility Model, AWS/Azure/GCP
- **Private Cloud**: 단일 조직 전용, VMware on AWS/Azure Stack/Google Anthos
- **Hybrid Cloud**: On-Prem ↔ Public Cloud 간 네트워크 연결(Direct Connect, ExpressRoute, Interconnect), 워크로드 이동성
- **Multi-Cloud**: 2개 이상 CSP 동시 사용, 벤더 종속 제거(Anti-Lock-in), 각 CSP별 강점 활용
- **Community Cloud**: 동일 산업군(의료·금융·정부) 공동 사용, 컴플라이언스 공유

### 3. 클라우드 네이티브 아키텍처 핵심 구성요소 (12-Factor App + CNCF)

```text
[12-Factor App 마이크로서비스 단일 인스턴스 내부 구조]

    +------------------------------------------------------+
    |                API Gateway / Ingress                  |
    |         (Rate Limit, AuthN, AuthZ, Routing)          |
    +----------------------+-------------------------------+
                           |
                +----------v----------+
                |   Service Mesh      | <---- mTLS, Retry, CircuitBreaker
                |   Sidecar Proxy     |      (Envoy/Istio/Linkerd)
                |  +--------------+   |
                |  |  App Pod     |   |
                |  |  (Business   |   |
                |  |   Logic)     |   |
                |  +--------------+   |
                |  +--------------+   |
                |  | Sidecar      |   |  <---- L7 Proxy, Telemetry
                |  | (Envoy)      |   |
                |  +--------------+   |
                +----------+----------+
                           |
       +-------------------+-------------------+
       |                   |                   |
+------v------+    +------v------+    +------v------+
| ConfigMap/  |    |   Secret    |    |  Persistent |
| Vault KV    |    |  Manager    |    |  Volume     |
| (Settings)  |    |  (Tokens)   |    |  (PVC/CSI)  |
+-------------+    +-------------+    +-------------+
       |
       |   +-------------------------------------+
       +--►|  Backing Services (Stateless)      |
           |  - RDBMS Proxy (RDS Proxy, ProxySQL)|
           |  - Cache (Redis/ElastiCache)        |
           |  - Message Broker (Kafka/RabbitMQ)  |
           |  - Object Storage (S3/Blob/GCS)     |
           |  - Search (OpenSearch/Elasticsearch)|
           +-------------------------------------+
```

### 4. 컴포넌트별 상세 역할

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **API Gateway** | 외부 트래픽 진입점, 인증/인가/라우팅/속도제한 | Kong(Plugin), Apigee(Analytics), AWS API Gateway(Usage Plan+Lambda Auth), Spring Cloud Gateway(WebFlux 기반 Reactive), GraphQL Federation(Apollo Router) |
| **Service Mesh** | 서비스 간 통신의 mTLS 암호화, 트래픽 관리, 관찰가능성 | Istio(Envoy+xDS), Linkerd(Linkerd2-proxy Rust), Consul Connect, AWS App Mesh, Open Service Mesh(OSM, deprecated). eBPF 기반 Cilium Service Mesh가 부상 |
| **Container Orchestrator** | 컨테이너 스케줄링, 자가치유, 롤링 업데이트, 오토스케일링 | Kubernetes 1.30+ (Sidecar Container GA, JobSet Beta), K3s(엣지용), EKS/AKS/GKE(Managed Control Plane), Karpenter(Just-in-time 노드 프로비저닝) |
| **IaC (Infrastructure as Code)** | 인프라의 선언적 정의 및 버전관리 | Terraform(Multi-Cloud, HCL), Pulumi(코드형), AWS CDK(TypeScript/Python), Ansible(설정관리), Crossplane(K8s 기반 IaC) |
| **CI/CD Pipeline** | 빌드/테스트/배포 자동화, 점진적 배포 | GitHub Actions, GitLab CI, Jenkins X, ArgoCD/Flux(GitOps), Spinnaker(Multi-Cloud 배포), Tekton(클라우드 네이티브 CI) |
| **Observability Stack** | 메트릭/로그/트레이스 통합 수집 및 분석 | Prometheus + Grafana, Loki(로그), Tempo/Jaeger(분산 트레이스), OpenTelemetry(SDK 표준), Datadog/New Relic(SaaS형), eBPF 기반 Pixie/Pyroscope |
| **Secrets Management** | 비밀 정보(API Key, DB Pwd) 중앙 관리 및 자동 순환 | HashiCorp Vault(Dynamic Secrets, PKI), AWS Secrets Manager(KMS 통합), Sealed Secrets(K8s), External Secrets Operator |
| **Service Discovery** | 동적 환경에서 서비스 위치 자동 탐색 | K8s CoreDNS, Consul(Health Check 포함), Eureka(Netflix OSS), AWS Cloud Map |

### 5. 탄력성(Resilience) 핵심 메커니즘

- **Circuit Breaker Pattern**: Hystrix(legacy) -> Resilience4j(Spring生态), Polly(.NET). Closed/Open/Half-Open 3상태로 외부 서비스 장애 격리. 임계치: failureRateThreshold=50%, waitDurationInOpenState=60s, slidingWindowSize=100
- **Bulkhead Pattern**: ThreadPool 또는 ConnectionPool 분리로 한 서비스의 장애가 전체로 전파되는 것 방지. AWS SDK Client-Side Retry with Jitter(Exponential Backoff + Decorrelated Jitter) 적용
- **Retry with Backoff**: `delay = min(cap, base * 2^attempt) + random(0, jitter)` 공식. AWS 공식 권장 jitter 공식: `sleep = min(cap, random_between(base, delay*3))`
- **Chaos Engineering**: Chaos Monkey(Netflix), Gremlin, AWS Fault Injection Service(FIS), LitmusChaos(K8s). Game Day를 통한 지속적 회복성 검증
- **SLO/SLI/SLA**: SLI(Indicator, 예: p99 응답시간 < 300ms), SLO(Objective, 예: 월 99.9% 성공률), SLA(Agreement, 계약). Error Budget = 1 - SLO. 30일 기준 99.9% SLO는 43.2분 다운타임 허용

### 6. 데이터 분산 및 일관성

- **CAP Theorem**: 일관성(C), 가용성(A), 분할 내성(P) 중 2개만 선택. AP 시스템(S3, DynamoDB) vs CP 시스템(etcd, HBase, ZooKeeper)
- **Saga Pattern**: Long-Running Transaction 처리. Orchestration(Central Coordinator) vs Choreography(Event-Driven). Compensation 트랜잭션으로 eventual consistency 보장
- **CQRS + Event Sourcing**: 쓰기/읽기 모델 분리, 도메인 이벤트를 Event Store에 저장 -> Materialized View(읽기전용) 비동기 갱신. Kafka + Debezium CDC 패턴
- **Strong Consistency 필요 구간**: 결제/재고/인증. DynamoDB Global Tables(다중리전), Cosmos DB(Multi-Master, 5가지 일관성 레벨), Spanner(TrueTime, 외부 일관성)

### 7. AWS Well-Architected Framework 6대 Pillars (2024 기준)

| Pillar | 핵심 설계 원칙 | 주요 KPI/지표 |
|:---|:---|:---|
| **Operational Excellence** | 코드형 운영, 지속적 개선, 장애 대비 | MTTR, 배포 빈도, 변경 실패율(DORA) |
| **Security** | 강력한 자격증명, 추적성, 모든 계층 보안, 자동화 | 보안 사고 MTTD/MTTR, CVE 패치 주기 |
| **Reliability** | 자동 복구, 용량 계획, 변경 관리 | 가용성(%), RTO/RPO |
| **Performance Efficiency** | 모니터링, 고급 기술 활용, 글로벌화 | p50/p95/p99 Latency,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 540 / 800

<- **이전**: [539. 클라우드 아키텍처 핵심 토픽 539번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/539_cloud_architecture_core_topic_539_exam_summar/)
**다음**: [541. 클라우드 아키텍처 핵심 토픽 541번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/541_cloud_architecture_core_topic_541_exam_summar/) ->

---
