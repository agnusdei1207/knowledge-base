---
title: "Cloud Architecture Core Topic 737 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST SP 500-292 참조모델 기반의 5대 핵심 특성(온디맨드 셀프서비스, 광범위 네트워크 접근, 리소스 풀링, 급격한 탄력성, 측정 가능한 서비스)과 3대 서비스 모델(IaaS/PaaS/SaaS) 위에, 마이크로서비스·서버리스·이벤트드리븐·서비스 메시·멀티클라우드 등 분산 시스템 패턴을 결합하여 CAP 정리와 12-Factor App 원칙 하에 가용성·확장성·복원력(Resilience)을 동적으로 확보하는 소프트웨어 아키텍처 패러다임이다.
> 2. **가치**: AWS Auto Scaling Group 기준 트래픽 10배 증가 시 5분 이내 인스턴스 확장, Spot Instance 활용 시 EC2 비용 최대 90% 절감, Kubernetes HPA + Cluster Autoscaler 결합으로 평균 CPU 60% 유지, S3 11 9s(99.999999999%) 내구성을 통한 데이터 손실 0에 수렴, Multi-AZ RDS 배포로 RTO 60초/RPO 0초 달성, MTTR 70% 단축 및 DevOps 파이프라인을 통한 배포 주기 일 100회 이상(DORA Elite) 실현이 가능하다.
> 3. **판단 포인트**: Public/Private/Hybrid/Multi/Community 배포 모델 선택 시 데이터 주권·규제 준수(GDPR, PDPA, 개인정보보호법), 5대 클라우드 아마존(AWS/Azure/GCP/Naver Cloud/Kakao Cloud) 간 종속성(Lock-in) 회피 전략, Stateful vs Stateless 워크로드 분리, 동기·비동기·이벤트 기반 통신 방식의 트레이드오프(Strong Consistency vs Eventual Consistency), FinOps 기반 비용 최적화 vs 성능 확보, Zero Trust 보안 모델 적용 수준 결정이 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스(Enterprise On-Premise) 데이터센터는 CapEx(자본지출) 중심의 고정 용량 설계로 인해 트래픽 변동성 대응, 고가용성(HA) 확보, 재해복구(DR) 구축에 한계가 있었다. 2006년 AWS S3와 EC2 출시 이후 클라우드 컴퓨팅은 Infrastructure as Code(Terraform, AWS CDK, Pulumi)로 정의된 프로비저닝, 컨테이너 오케스트레이션(Kubernetes, ECS, Nomad), 서비스 메시(Istio, Linkerd, Consul Connect) 기반 트래픽 관리, GitOps(ArgoCD, Flux) 기반 선언적 배포 모델로 진화했다.

NIST SP 500-292(2011) 클라우드 컴퓨팅 참조모델에서 정의한 5대 핵심 특성과 3대 서비스 모델, 4대 배포 모델을 기준으로, 현대 클라우드 아키텍처는 Well-Architected Framework(AWS 6대 pilares: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability; Azure 5대: Cost, Operational, Performance, Reliability, Security; Google 5대: Operational, Security, Privacy, Reliability, Cost Efficiency)를 통해 설계 품질을 보증한다.

```text
[클라우드 아키텍처 진화 흐름도]

  +--------------+    +--------------+    +--------------+
  |  Monolith    |    |  SOA / ESB   |    |  Microservice|
  |  (1990s)     |---->|  (2000s)     |---->|  (2014-)     |
  |              |    |              |    |  + Container |
  |  단일 바이너리|    |  WSDL/SOAP   |    |  K8s/Istio   |
  |  RDBMS 단일   |    |  WS-* 표준   |    |  gRPC/Envoy  |
  +--------------+    +--------------+    +--------------+
                                                     |
                          +--------------------------+
                          v
  +--------------+    +--------------+    +--------------+
  |  Serverless  |    |  Event-Driven|    |  Edge Cloud  |
  |  (2017-)     |    |  (2018-)     |    |  (2020-)     |
  |  Lambda/Func |    |  Kafka/Kinesis|   |  CDN/WASM    |
  |  Pay-per-Use |    |  CQRS/EventS |    |  5G MEC      |
  +--------------+    +--------------+    +--------------+
```

Monolithic Architecture는 단일 코드베이스로 배포가 단순하나 부분 스케일링 불가, 단일 장애점(SPOF), 기술 스택 종속이라는 문제가 있다. Cloud-Native Microservices는 도메인 단위 분리(Bounded Context, DDD), 독립 배포, 폴리글랏 퍼시스턴스(Polyglot Persistence: PostgreSQL, MongoDB, Cassandra, Redis, DynamoDB), Circuit Breaker(Resilience4j, Hystrix), Saga Pattern(Orchestration/Choreography), Distributed Tracing(Jaeger, Zipkin, OpenTelemetry)을 통해 이러한 한계를 해결한다.

- **📢 섹션 요약 비유**: 기존 온프레미스는 가족이 단독주택을 짓는 것과 같아 평수 부족 시 증축이 어렵고, 초기 건축비(CapEx)가 막대하다. 클라우드 아키텍처는 이케아의 모듈식 가구처럼, 필요 시 책장·옷장 단위(서비스)만 조립하고 사용한 만큼만 비용을 지불하는 서비스형 인프라다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 크게 **프레젠테이션 계층**(CDN, WAF, API Gateway), **애플리케이션 계층**(Microservice, Serverless Function, Service Mesh Sidecar), **데이터 계층**(RDBMS, NoSQL, Data Lake, Cache, Search Index), **인프라 계층**(Compute, Network, Storage, Container Orchestrator), **플랫폼 계층**(IAM, Observability, CI/CD, IaC, Secret Management)로 구성된다. CNCF Cloud Native Interactive Landscape 기준 1,500+ 프로젝트가 각 계층을 담당한다.

```text
[클라우드 네이티브 4계층 + 횡단 관심사 아키텍처]

  사용자 디바이스 (Mobile/IoT/Browser)
        | HTTPS/TLS 1.3, HTTP/3 (QUIC)
        v
  +---------------------------------------------+
  | Edge / CDN 계층                              |
  |  CloudFront / Cloudflare / Akamai / Cloud CDN|
  |  DDoS Shield (L3-L7), WAF (OWASP Top 10)    |
  |  Lambda@Edge / Cloud Functions / Workers     |
  +---------------------------------------------+
        |
        v
  +---------------------------------------------+
  | API Gateway / Service Mesh Control Plane     |
  |  Kong / AWS API GW / Apigee / Istio Gateway  |
  |  AuthN(OAuth2/OIDC/JWT) / Rate Limit / Quota|
  |  Canary(5%) -> Staging -> Prod  Progressive   |
  +---------------------------------------------+
        |
        v  gRPC over mTLS, GraphQL, WebSocket
  +---------------------------------------------+
  | Service Mesh Data Plane (Envoy Sidecar)      |
  |  mTLS 자동화 / Circuit Breaker / Retry/Timeout|
  |  Traffic Split(90/10) / Fault Injection      |
  |  --- Microservices (12개 Pod per Service) ---|
  |  Order / Payment / Inventory / User / Notif |
  |  각각 HPA: min=3, max=50, target CPU=60%    |
  +---------------------------------------------+
        |
        v
  +---------------------------------------------+
  | 데이터 계층 (Polyglot Persistence)            |
  |  OLTP: PostgreSQL(RDS Multi-AZ) / CockroachDB|
  |  NoSQL: DynamoDB / MongoDB Atlas / Cassandra |
  |  Cache: Redis Cluster (ElastiCache)          |
  |  Search: Elasticsearch / OpenSearch          |
  |  OLAP: Snowflake / BigQuery / Redshift       |
  |  Object: S3 11 9s / MinIO 12 9s              |
  |  Streaming: Kafka (3 AZ), Kinesis, Pulsar    |
  +---------------------------------------------+
        |
        v
  +---------------------------------------------+
  | 횡단 관심사 (Cross-Cutting Concerns)          |
  |  Observability: Prometheus + Grafana + Loki  |
  |                Tempo(Trace) / OpenTelemetry  |
  |  Security: Vault / SOPS / AWS Secrets Manager|
  |  CI/CD: GitHub Actions -> ArgoCD (GitOps)     |
  |  IaC: Terraform / Pulumi (State: S3+DynamoDB)|
  +---------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway** | 단일 진입점(Edge), 인증/인가, 트래픽 정책, 요청 라우팅 | OAuth 2.0 + JWT 검증, Rate Limiting(Token Bucket 알고리즘, 1000 RPS/IP), Request/Response Transformation(DSL: OpenAPI 3.0, AsyncAPI 2.6), WebSocket·gRPC-Web 변환, Lambda Authorizer로 커스텀 인증 |
| **Service Mesh** | 서비스 간 통신 인프라 추상화, 관측 가능성, 정책 적용 | Istio 1.20+ / Linkerd 2.14+ 기반 Envoy Sidecar 프록시, mTLS SPIFFE ID 기반 제로트러스트, Istio VirtualService로 트래픽 분할(90/10 카나리), DestinationRule로 Circuit Breaker(consecutive_5xx_errors: 5, interval: 30s) |
| **Container Orchestrator** | 컨테이너 라이프사이클 관리, 스케줄링, 자기치유 | Kubernetes 1.29+ Control Plane(etcd 3.5+ Raft 합의, kube-apiserver, scheduler, controller-manager, cloud-controller-manager), kubelet이 CRI(O) 인터페이스로 containerd 1.7 연동, CNI(Calico/Cilium eBPF) 네트워크 |
| **Serverless Platform** | 이벤트 기반 FaaS, Pay-per-Invocation(100ms 단위 과금) | AWS Lambda 15분 Timeout / 10GB Memory, Azure Functions Premium Plan으로 콜드스타트 50ms 이하, Knative Serving(KPA: Knative Pod Autoscaler) + Cloud Run으로 K8s 위 FaaS 구현 |
| **Event Streaming** | 비동기 메시지 전달, 로그 기반 변경 데이터 캡처(CDC) | Apache Kafka 3.7 KRaft 모드(ZooKeeper 제거), Partition 3개+Replication Factor 3, Exactly-Once Semantics(트랜잭션 프로듀서 + read_committed), Schema Registry로 Avro/Protobuf 진화 |
| **Observability Stack** | 3대 신호(Metrics/Logs/Traces) + 사용자 경험(RUM/Synthetic) | Prometheus 2.50+ Pull 모델(15s scrape), OpenTelemetry Collector로 vendor-neutral 수집, Grafana Tempo로 분산 트레이싱, SLO 기반 Alerting(Error Budget: 월 99.9% -> 43.2분 다운타임 허용) |

**핵심 알고리즘 및 수식**

- **CAP 정리**: 분산 시스템은 Consistency(일관성), Availability(가용성), Partition tolerance(파티션 허용) 3가지 중 최대 2가지만 만족. DynamoDB는 AP(Eventually Consistent, Quorum=2/3), etcd/RDBMS는 CP, 전통 RDBMS 단일 노드는 CA.
- **Consensus 알고리즘**: Raft Leader Election(election timeout 150-300ms 랜덤화), Log Replication(Commit Index 전파), Paxos 대비 이해도 향상.
- **부하 분산 알고리즘**: Round Robin, Least Connections, IP Hash, Consistent Hashing(노드 추가/제거 시 재해시 1/N만 발생, DynamoDB/Cassandra/Memcached 채택).
- **리소스 스케줄링**: Kubernetes LeastAllocated / BalancedAllocation / MostAllocated 점수 함수, Bin-packing과 Spread 전략의 트레이드오프.
- **배압(Backpressure)**: Reactive Streams 사양(Netflix RxJava, Reactor, Akka Streams)으로 publisher-subscriber 간 처리량 조절, TCP 슬라이딩 윈도우와 결합.
- **12-Factor App**: Codebase(1 repo 다수 배포), Dependencies(명시적 선언), Config(환경변수), Backing Services(attached resource), Build/Release/Run(완전 분리), Processes(Stateless), Port Binding(자체 포트), Concurrency(프로세스 모델), Disposability(빠른 시작/종료), Dev/Prod Parity, Logs(스트림), Admin Processes.

- **📢 섹션 요약 비유**: Service Mesh는 도시의 도로·교통신호·CCTV가 통합된 스마트 교통 시스템과 같다. 차량(서비스)이 직접 신호를 관리하지 않아도, 도시 관제 센터(Istio Control Plane)가 모든 교차로(Envoy Sidecar)에 일관된 신호 정책과 모니터링을 적용한다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처는 유사·경쟁·선행 개념과 명확한 차이점을 가진다. 마이크로서비스와 모놀리식, Serverless와 Container, Multi-Cloud와 Hybrid Cloud, Event-Driven과 Request-Response 패턴의 비교는 기술사 시험에서 빈출된다.

| 구분 | Monolithic Architecture | Microservices Architecture |
| :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/JAR/EAR, 전체 동시 배포 | 서비스별 컨테이너 이미지, 독립 배포 |
| **스케일링** | Horizontal: 전체 복제(비효율), Vertical만 가능 | 서비스별 독립 HPA, KEDA 이벤트 기반 확장 |
| **장애 격리** | 단일 버그로 전체 다운, SPOF | Circuit Breaker로 장애 전파 차단, Bulkhead 패턴 |
| **기술 스택** | 단일 언어/프레임워크 종속 | Polyglot(Go/Rust/Python/Node), gRPC/protobuf |
| **데이터 관리** | 단일 RDBMS, ACID 트랜잭션 보장 | Database per Service, Saga로 분산 트랜잭션 |
| **팀 구조** | Conway's Law 위반, 단일 팀 전체 관리 | 2-pizza Team, Bounded Context별 독립 |
| **관측성** | 단일 로그 파일, 단순 APM | 분산 트레이싱 + 3 Pillars 통합, SRE 관점 필수 |
| **적합 규모** | 사용자 10만 이하, 도메인 단순, MVP | 사용자 100만+, 도메인 복잡, 5+ 엔터프라이즈 |
| **배포 주기** | 월 1~4회, 통합 테스트 부담 | 일 10~100회(DORA Elite), Blue/Green, Canary |
| **TCO(5년)** | 초기 낮으나 스케일 시 급증 | 초기 30~50% 높으나 운영 효율로 회수 |

| 구분 | Container (Docker) | Serverless (FaaS) |
| :--- | :--- | :--- |
| **추상화 수준** | OS-Level 가상화(컨테이너) | 함수 단위 완전 관리형 |
| **콜드스타트** | 1~3초 (이미지 pull + 시작) | 100ms ~ 5초 (VPC Lambda 50ms) |
| **최대 실행 시간** | 무제한 (K8s livenessProbe로 관리) | Lambda 15분, Azure Functions unbounded |
| **가격 모델** | Pay for Provisioned (Fargate/vCPU-시간) | Pay per Invocation(GB-s) |
| **상태 관리** | Stateful 가능(PVC, StatefulSet) | Stateless 권장, 외부 스토리지 필수 |
| **네트워크** | Pod IP, Service ClusterIP, Ingress | VPC Internal, API GW, EventBridge |
| **확장** |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 737 / 800

<- **이전**: [736. 클라우드 아키텍처 핵심 토픽 736번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/736_cloud_architecture_core_topic_736_exam_summar/)
**다음**: [738. 클라우드 아키텍처 핵심 토픽 738번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/738_cloud_architecture_core_topic_738_exam_summar/) ->

---
