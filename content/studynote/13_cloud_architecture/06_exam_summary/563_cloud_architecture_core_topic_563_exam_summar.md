---
title: "563. 클라우드 아키텍처 핵심 토픽 563번 시험 요약 (Cloud Architecture Core Topic 563 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 Well-Architected Framework(보안성·신뢰성·성능효율성·비용최적화·운영우수성·지속가능성 6대 축) 기반 위에서, 마이크로서비스·컨테이너·서버리스·이벤트드리븐을 조합하여 **탄력성(Elasticity)·가용성(HA)·확장성(Scalability)·관측가능성(Observability)**을 코드로 구현하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: CapEx->OpEx 전환으로 TCO 30~50% 절감, Auto Scaling으로 트래픽 변동 시 자원利用率 70% 이상 유지, 멀티AZ·리전 구성을 통해 DR RTO/RPO를 분 단위(기존 수 시간 대비 95%v)로 단축하며, MTTR을 Observability 기반으로 60% 이상 개선한다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs 멀티/하이브리드, Stateless·Stateful 서비스 분리, 동기(REST/gRPC)·비동기(Pub/Sub·Kafka·SQS·EventBridge) 트래픽 분리, Consistency 모델(Strong/Eventual) 선택, 12-Factor App·Strangler Fig·Sidecar 등 패턴 적용 여부가 아키텍처 성패를 좌우한다.

---

## Ⅰ. 개요 및 필요성

기존 온프레미스 3-Tier 아키텍처는 트래픽 피크 시 과잉 Provision(평균 30% Idle), 트래픽 저점 시 자원 회수 불가, 장애 시 수동 대응(Mean Time To Repair 평균 4~8시간), CapEx 선투자(3~5년 회수)라는 구조적 한계를 가졌다. 클라우드 아키텍처는 **API 선언형 인프라(IaC)**, **Policy as Code**, **Immutable Infrastructure**, **GitOps**를 통해 자원 생성을 코드화하고, Control Plane이 선언된 의도(Desired State)와 실제 상태(Actual State)를 지속적으로 Reconciliation(Reconcile Loop)하여 자급자족(Self-Healing) 시스템을 구현한다. 컨테이너 오케스트레이션(Kubernetes), 서비스 메시(Istio/Linkerd), 메시 내부 트래픽 관리, 분산 트레이싱(OpenTelemetry/Jaeger/Tempo) 등을 통해 수십~수천 개의 마이크로서비스를 자동화된 운영 체계 하에 통합 관리한다.

```text
[클라우드 네이티브 아키텍처 진화 흐름]

+--------------+   +--------------+   +--------------+   +--------------+
| Monolith     | -> | Modular      | -> | Microservice | -> | Cloud-Native |
| (1 Tier)     |   | Monolith     |   | (수십~수백)  |   | (수천 POD)   |
|              |   |              |   |              |   |              |
| - 단일배포   |   | - 패키지분리 |   | - REST/gRPC  |   | - K8s+Service |
| - 수동스케일 |   | - DB공유     |   | - DB분리     |   |   Mesh       |
| - 장애연쇄   |   | - 부분장애   |   | - API GW     |   | - Serverless |
+--------------+   +--------------+   +--------------+   +--------------+
       |                   |                  |                  |
       +---- CapEx 무거운 HW 의존 -----+    +- OpEx+IaC+자동화 중심 -+

[전통적 vs Cloud-Native 비교]

   전통적 (On-Prem)              Cloud-Native (K8s+AWS)
  +-------------+              +----------------------+
  | App Server  |              | Pod  | Pod  | Pod  |
  |   (Tomcat)  |              | Svc1 | Svc2 | Svc3 |
  +-------------+              +------+------+------+
  |    WAS      |              | Service Mesh (Istio)|
  +-------------+              +---------------------+
  |    DB (RDB) |              | Envoy Sidecar Proxy |
  |   (Oracle)  |              +---------------------+
  +-------------+              | K8s Control Plane   |
  |    HW/OS    |              | (etcd + API Server) |
  +-------------+              +---------------------+
  · 수동장애복구                · Self-Healing (Pod 재기동)
  · 수평확장 불가              · HPA/VPA/Cluster Autoscaler
  · 설정변경 SSHTunnel        · GitOps + ArgoCD
```

**필요성**: ① 글로벌 사용자 대상 SLA 99.99%(연 52분 이내 장애) 달성을 위해 Multi-AZ·Multi-Region 액티브-액티브 구성이 필수, ② 단기 트래픽 폭증(블랙프라이데이, 예약 오픈)에 대응하는 **Elastic Capacity**, ③ GDPR/개인정보보호법/PIPC 등 컴플라이언스 자동 감사(AWS Config·Azure Policy), ④ 신규 서비스 TTM(Time-To-Market) 1주 이내 단축, ⑤ 그린 IT(탄소중립)를 위한 **Region 단위 전력 효율 최적화** 요구가 핵심 동력이다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **"전기를 직접 발전하지 않고 수도꼭지를 틀면 전기가 나오는 그리드"**와 같다. 평소에는 합리적인 요금으로 쓰고, 에어컨을 동시에 100대 켜면 자동으로 발전량이 늘어나며(탄력성), 정전이 나면 다른 계통에서 즉시 전기를 공급받아(자동 페일오버) 집이 캄캄해지지 않는다. 요금제만 잘 짜면 집 한 채 운영이 국가 전력망 운영처럼 똑똑해진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 크게 **5개 계층(Edge -> Network -> Compute -> Storage/Data -> Observability)**과 **2개 횡단 관심사(Cross-Cutting: Security, Governance)**로 구성된다. 각 계층은 IaC(Terraform/CloudFormation/Pulumi)로 선언적으로 정의되며, **Control Plane(제어)**과 **Data Plane(데이터 처리)**이 분리되어 있다.

```text
[클라우드 네이티브 참조 아키텍처 - MSA+EKS+Observability]

                            +--------------------------+
                            |  CloudFront / Cloud CDN  |  <- Edge (정적캐시, WAF)
                            +----------+---------------+
                                       | TLS 1.3, HTTP/2, gRPC
                            +----------v---------------+
                            |   API Gateway / Kong     |  <- 인증/인가/L7 LB
                            |  (OAuth2, JWT, RateLimit)|
                            +----------+---------------+
                                       |
        +------------------------------+------------------------------+
        |                              |                              |
+-------v---------+         +---------v--------+         +---------v--------+
|  Service Mesh   |         |  Service Mesh    |         |  Service Mesh    |
|  (Istio/Linkerd)|         |   (Istio)        |         |   (Istio)        |
| +-------------+ |         | +--------------+ |         | +--------------+ |
| | Payment Svc | |         | |Order Svc     | |         | | Catalog Svc  | |
| | (Pod+Envoy) | |         | |(Pod+Envoy)   | |         | |(Pod+Envoy)   | |
| +-------------+ |         | +--------------+ |         | +--------------+ |
+-------+---------+         +---------+--------+         +---------+--------+
        | mTLS 인증                    |                            |
        |                              |                            |
        +--------------+---------------+------------+---------------+
                       |  Pub/Sub / Kafka / SQS      |
                       |  (비동기 이벤트 스트림)      |
                       |                             |
            +----------v----------+         +-------v----------+
            |  Database Tier     |         |  Serverless Tier |
            |  · Aurora(MySQL)   |         |  · Lambda        |
            |  · DynamoDB        |         |  · Step Functions|
            |  · Redis(ElastiCache)        |  · EventBridge   |
            +----------+----------+         +------------------+
                       |
            +----------v--------------------------------------+
            |     Observability (3 Pillars)                  |
            |  · Metrics: Prometheus / CloudWatch / Datadog   |
            |  · Logs   : Loki / OpenSearch / CloudWatch Logs|
            |  · Traces : Jaeger / Tempo / X-Ray / OTLP      |
            +-------------------------------------------------+

[Reconcile Loop - K8s Control Plane]

   +-----------------+
   | kubectl apply   |  <- User/Operator 의도(Desired)
   | (YAML Manifest) |
   +--------+--------+
            | HTTPS
   +--------v--------+
   |  API Server     |  <- Authn (RBAC), Validating, Mutating
   |  (Auth + AdmW)  |
   +--------+--------+
            |
   +--------v--------+     +--------------+
   |  Scheduler      | <---> |  etcd (Raft) |  <- 클러스터 상태 저장
   +--------+--------+     +--------------+
            |
   +--------v--------+
   |  kubelet        |  <- Node에서 실행
   |  (CNI/CRI)      |
   +--------+--------+
            |
   +--------v--------+
   |  Container      |  <- 실제 App
   |  (Pod)          |
   +-----------------+
            | Status 보고 (Heartbeat 10s)
            +--------------> API Server
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway / Ingress** | L7 라우팅·인증·Rate Limit·프로토콜 변환 | AWS API Gateway, Kong, NGINX, Envoy Gateway, Traefik. JWT 검증, OIDC 통합, gRPC->REST 변환, Circuit Breaker 정책 적용 |
| **Service Mesh (Data/Control Plane 분리)** | 서비스 간 mTLS, 트래픽 관리, 관측 | Istio(Envoy 기반), Linkerd(Linkerd2-proxy Rust기반), Consul Connect. mTLS 자동 발급(SPIFFE/SPIRE), 카나리 배포(Weighted Routing), Fault Injection |
| **Container Orchestrator (K8s)** | 컨테이너 스케줄링·자가치유·오토스케일 | kube-scheduler(리소스/친화성/테인트), kube-proxy(iptables/IPVS), CoreDNS, HPA(CPU/Mem/커스텀 메트릭), VPA, Cluster Autoscaler/Karpenter |
| **Serverless / FaaS** | 이벤트 기반 stateless 코드 실행 | AWS Lambda(15분 timeout, 10GB mem), Azure Functions, GCP Cloud Run, Knative. Cold Start 100~500ms, Provisioned Concurrency로 해결 |
| **Managed Data Services** | 관계형/NoSQL/시계열/검색 통합 | Aurora(MySQL/Postgres 호환, 6-way 복제), DynamoDB(Global Tables 다중리전), Redis 7, MongoDB Atlas, Snowflake(BigQuery/Redshift) |
| **Observability Stack** | 통합 모니터링·로그·트레이싱 | OpenTelemetry(OTLP 표준), Prometheus+Thanos/Grafana, Loki, Jaeger, Tempo, EFK(Elastic+Filebeat+Kibana), Splunk, Datadog |
| **IaC & GitOps** | 인프라 선언·버전관리·자동배포 | Terraform(상태 파일 S3+DynamoDB Lock), Pulumi, CloudFormation, Ansible, ArgoCD/FluxCD(Git을 Single Source of Truth로) |
| **Security & Compliance** | Zero Trust, CSPM, Secrets 관리 | AWS IAM+SCP, Azure AD+RBAC, HashiCorp Vault, AWS Secrets Manager, OPA/Kyverno(Policy as Code), Falco(런타임 보안) |

**핵심 동작 원리**:
1. **선언형 API(Declarative API)**: 사용자가 "원하는 상태(Desired State)"를 YAML/HCL로 선언 -> Controller가 Current State를 읽고 -> Diff 계산 -> Reconcile. K8s Deployment의 Replica, HPA의 min/max/desired CPU, Terraform의 `desired_count` 등 모든 것이 이 원칙을 따른다.
2. **불변 인프라(Immutable Infra)**: 서버에 SSH 접속해 설정 변경 ❌ -> 새 AMI/Container Image로 교체. AMI Dwell Time 단축, Blue/Green & Canary 배포 용이.
3. **12-Factor App 원칙**: Codebase(1), Dependencies(2), Config(환경변수, 3), Backing Services(4), Build/Release/Run 분리(5), Stateless Processes(6), Port Binding(7), Concurrency(8), Disposability(빠른 기동/종료, 9), Dev/Prod Parity(10), Logs(Event Stream, 11), Admin Processes(12).
4. **Bursting & Elasticity**: HPA 메트릭 산정식 `desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]`. KEDA로 Kafka Lag, RabbitMQ 큐 길이 등 이벤트 기반 스케일링.
5. **Resilience 패턴**: Circuit Breaker(Hystrix->Resilience4j, 50% 실패율 시 OPEN), Bulkhead(쓰레드풀 격리), Retry(Exponential Backoff + Jitter), Timeout(전체 99p 기준), Rate Limiter(Token Bucket).
6. **데이터 분산**: CAP Theorem -> CP(RDB+Strong Consistency) vs AP(DynamoDB+Eventually Consistent) 선택. Saga Pattern(2PC 회피, Choreography vs Orchestration), Outbox Pattern(이벤트+DB 트랜잭션 원자성), CDC(Debezium) 기반 동기화.

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 핵심 원리는 **"냉장고 자동발주 시스템"**과 같다. 우유가 떨어지면(메트릭 임계치) 자동으로 주문이 들어가(HPA 스케일아웃), 신선한 우유가 도착하면(새 컨테이너 기동) 다시 정상 상태로 돌아온다. 일주일 동안 우유를 안 쓰면 자동으로 주문도 멈추고(Scale-to-Zero), 냉장고가 고장 나면 예비 냉장고가 즉시 투입된다(Multi-AZ 페일오버). 사람이 매번 확인하지 않아도 똑똑하게 돌아가는 것이 선언형·자동화·자가치유의 본질이다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처는 동일 문제를 푸는 다양한 접근 간 **트레이드오프**가 존재한다. 기술사 답안에서는 "왜 A가 아닌 B를 선택했는가"의 **근거 논리**가 핵심이다.

| 구분 | IaaS (EC2/EKS) | PaaS (Beanstalk/App Service) | SaaS (Salesforce/OutSystems) | FaaS/Serverless (Lambda) |
| :--- | :--- | :--- | :--- | :--- |
| **제어 범위** | OS·미들웨어·런타임까지 | 런타임·미들웨어만 | 애플리케이션만 | 함수 코드만 |
| **확장 단위** | VM/Container 인스턴스 | App Instance / Plan | 사용자
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 563 / 800

<- **이전**: [562. 클라우드 아키텍처 핵심 토픽 562번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/562_cloud_architecture_core_topic_562_exam_summar/)
**다음**: [564. 클라우드 아키텍처 핵심 토픽 564번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/564_cloud_architecture_core_topic_564_exam_summar/) ->

---
