---
title: "Cloud Architecture Core Topic 713 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 **탄력성(Elasticity)·확장성(Scalability)·장애격리(Fault Isolation)**를 코어 설계 원칙으로 삼아, 컨테이너·오케스트레이션(K8s)·서비스 메시(Istio)·서버리스(Lambda/Cloud Run)·IaC(Terraform)·GitOps(ArgoCD)를 결합한 **클라우드 네이티브 12-Factor App** 기반의 분산 시스템 구조이다.
> 2. **가치**: Auto Scaling·Spot Instance로 컴퓨팅 비용을 **30~70% 절감**, Multi-AZ·Multi-Region 구성으로 **RPO 0/RTO 분 단위** 달성, GitOps 기반 선언적 배포로 **배포 리드타임 90% 단축**(DORA Elite 기준), FinOps 적용으로 클라우드 청구액 **20~40% 최적화**가 가능하다.
> 3. **판단 포인트**: **단일 클라우드 종속(Vendor Lock-in) vs 멀티/하이브리드**의 트레이드오프, **동기식 통신(Synchronous REST/gRPC) vs 비동기 이벤트 기반(EventBridge/Kafka)**의 일관성·지연시간·장애전파 트레이드오프, **Stateless 워크로드(컨테이너) vs Stateful 워크로드(DB/스토리지)**의 책임 분리 경계를 명확히 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 3-Tier 아키텍처(웹/WAS/DB)는 **수직 확장(Scale-Up) 한계**, **장기 납기로 인한 Capacity Planning 실패**, **DR(Disaster Recovery) 사이트의 상시 유휴 비용**, **모놀리식 구조로 인한 배포 주기 장기화(주 1~월 1회)**라는 근본적 한계를 가진다. 2020년 이후 마이크로서비스 아키텍처(MSA)와 클라우드 네이티브 기술(CNCF Landscape 1,000+ 프로젝트)이 보편화되면서, **선언적 인프라(Declarative Infrastructure)**, **불변 인프라(Immutable Infrastructure)**, **관측 가능성(Observability)**, **셀프힐링(Self-Healing)**을 핵심으로 하는 클라우드 아키텍처가 표준이 되었다.

```text
   +----------------------------------------------------------------------+
   |             On-Premise Monolithic  vs  Cloud-Native MSA              |
   +----------------------------------------------------------------------+

   [Legacy: Monolithic 3-Tier]              [Modern: Cloud-Native 12-Factor]
   +---------------------+                  +------------------------------+
   |  Client (Browser)   |                  |  Edge: CDN/CloudFront+WAF    |
   +----------+----------+                  +--------------+---------------+
              | HTTPS                                       | HTTPS/QUIC
   +----------v----------+                  +--------------v---------------+
   |  Web Server (Nginx) |                  |  API Gateway / App Gateway  |
   |  (Active-Standby)   |                  |  + WAF + Rate Limiting      |
   +----------+----------+                  +--------------+---------------+
              | AJP/HTTP                                 | mTLS (Service Mesh)
   +----------v----------+                  +--------------v---------------+
   |  WAS (Tomcat/JBoss) | ◄-- Monolith    |  Microservice Pods (K8s)     |
   |  Scale-Up 한계      |     (단일 장애)  |  +------++------++------+    |
   +----------+----------+                  |  |Auth ||Order ||Pay   |    |
              | JDBC                        |  +------++------++------+    |
   +----------v----------+                  |  HPA/VPA + Cluster Autoscaler|
   |  RDBMS (Oracle RAC) |                  +--------------+---------------+
   |  Active-Active      |                                 | gRPC/Async
   +---------------------+                  +--------------v---------------+
   ※ DR Site 별도 구축 (유휴)               |  Event Bus / Kafka / DDB    |
   ※ 배포: 주 1회, 장애 전파 광범위          |  Aurora Global / Cosmos DB  |
   ※ Capacity: Peak 기준 과투자              +------------------------------+
   ※ 트래픽 변동: Peak/Off-Peak 5배 차이     ※ Multi-AZ 기본, DR 자동화
                                              ※ 배포: 일 100~수천 회
                                              ※ Auto Scaling: 트래픽 즉시 대응
```

**기존 패러다임의 한계**:
- **Capacity Provisioning**: Peak 부하 기준으로 하드웨어 과투자 -> 유휴 60~80%
- **MTTR(Mean Time To Recovery)**: Cold Standby -> RTO 수 시간~일
- **Release Train**: 수동 배포, 롤백 어려움 -> Change Failure Rate 45% 이상(DORA Report)
- **Vendor Lock-in**: 특정 HW/SW 종속 -> 기술 부채 누적

**새 패러다임의 등장**:
- **AWS Well-Architected Framework**(2015~) 5대 Pilar: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization
- **12-Factor App**(Heroku 2011) -> 클라우드 네이티브 앱 설계 원칙
- **CNCF Trail Map**(2016~) -> OSS 기반 클라우드 네이티브 성숙도 경로
- **FinOps Foundation**(2019) -> 클라우드 비용 거버넌스

- **📢 섹션 요약 비유**: 기존 모놀리식 시스템이 **"한 채의 큰 호텔에 모든 손님을 수용"**하는 방식이라면, 클라우드 아키텍처는 **"수많은 작은 모텔을 네트워크로 연결하여 손님이 늘면 즉시 객실을 늘리고, 줄면 철거하는"** 에어비앤비(Airbnb) 모델과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **5개 계층(Layer)**으로 분해된다. 각 계층은 독립적 확장·장애격리·기술 교체 가능성이 보장되어야 한다(STRIDE/관심사 분리 원칙).

```text
   +---------------------------------------------------------------------+
   |                  Cloud-Native Reference Architecture                |
   +---------------------------------------------------------------------+

  [L1] Edge / Global Layer          CloudFront / Azure Front Door / Cloud CDN
        |                              (Anycast IP, TLS 1.3, HTTP/3)
        | WAF, Shield, Bot Management
        v
  [L2] Ingress / API Gateway         Kong / AWS API GW / Apigee / Envoy
        |                              (OAuth 2.0, OIDC, Rate Limit, mTLS)
        | AuthN/AuthZ, Quota, Routing
        v
  [L3] Orchestration Layer          Kubernetes (EKS/AKS/GKE) / Istio / Linkerd
        |                              (Control Plane + Data Plane 분리)
        | Pod Scheduling, HPA/VPA/CA, Service Mesh Sidecar
        v
  [L4] Application Layer             Microservices (Spring Boot / Node.js / Go)
        |                              Sidecar Pattern: Envoy Proxy
        | Stateless, Backing Service 분리, Health Check (/healthz, /readyz)
        v
  [L5] Data / Event Layer            OLTP: Aurora / Spanner / CockroachDB
                                     OLAP: Redshift / BigQuery / Snowflake
                                     Cache: Redis / Memcached
                                     Queue: SQS / Pub-Sub / Kafka
                                     Object: S3 / GCS / Blob (3-AZ Replication)
                                     Search: OpenSearch / Elasticsearch
                                     Lake: S3 + Glue + Athena
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Edge/Global** | 글로벌 트래픽 라우팅, DDoS 방어, TLS 종료 | CloudFront/Cloudflare: Anycast, **GSLB(Global Server Load Balancing)** with Route 53 Latency/Geolocation Policy, ACM(AWS Certificate Manager)로 자동 인증서 갱신 |
| **API Gateway** | North-South 진입점, AuthN/AuthZ, 프로토콜 변환 | OAuth 2.0 + OIDC(OpenID Connect) + JWT 검증, **Rate Limiting(Token Bucket/Leaky Bucket)**, Circuit Breaker(Hystrix/Resilience4j) |
| **Orchestration (K8s)** | 컨테이너 스케줄링, 셀프힐링, 선언적 상태 관리 | Control Plane: kube-apiserver/etcd, **Scheduler(K8s Scheduling Framework)**, kubelet/CRI/containerd, **HPA(CPU/Mem)·VPA(리소스 권장)·KEDA(이벤트 기반)·Cluster Autoscaler** |
| **Service Mesh (Istio)** | East-West 통신, mTLS, 트래픽 관리(Canary/Blue-Green) | Envoy Sidecar로 **L7 라우팅**, **mTLS 자동 발급(SPIFFE/SPIRE)**, Traffic Splitting(virtualService 10%->50%->100%), Fault Injection |
| **Stateless App** | 비즈니스 로직, 무상태성 보장 | 12-Factor: Config는 Environment Variable, Logging은 STDOUT, **Disposability(graceful shutdown SIGTERM->30s)**, Backing Service는 URL로 추상화 |
| **Event Bus / CDC** | 비동기 이벤트 전파, 서비스 간 결합도 완화 | Kafka(파티션 키 기반 순서 보장), **Outbox Pattern**(트랜잭션·이벤트 발행 원자성), Debezium(CDC), SQS FIFO / Pub-Sub Ordering Key |
| **Observability (3 Pillars)** | Logs·Metrics·Traces 통합 수집·분석 | **OpenTelemetry(OTel) SDK -> Collector -> Tempo/Jaeger(X-Ray) + Loki/ELK(Logs) + Prometheus/Thanos(Metrics)**, Grafana 통합 대시보드, SLO/SLI/SLA |
| **IaC + GitOps** | 인프라 선언적 정의, Git을 Single Source of Truth로 | Terraform(멀티클라우드 리소스) + **ArgoCD/Flux**(K8s GitOps, drift detection), Atlantis(Terraform PR 자동화), OPA(Policy as Code) |

**핵심 메커니즘 (심층)**:

**1. Auto Scaling 알고리즘**
- **HPA(Horizontal Pod Autoscaler)**: `targetMetric = sum(desiredReplicas) × currentUtilization / targetUtilization`
  - 예: CPU 70% 목표, 현재 5 Pod × 30% = 150, 150/70 = 2.14 -> 3 Pod 스케일 아웃
  - **KEDA**(Kubernetes Event-Driven Autoscaling): Kafka Lag, SQS Queue Length, Cron 등 이벤트 기반
- **Cluster Autoscaler**: Pending 상태 Pod 감지 시 Node Group 확장(5분 이내), 사용률 50% 이하 시 축소
- **Predictive Scaling**: ML 기반 트래픽 예측(AWS Predictive Scaling), 주기성 패턴 학습

**2. CAP Theorem & 일관성 모델**
- **Strong Consistency**: Spanner(TrueTime API, 전 세계 동기 시계), CockroachDB
- **Eventual Consistency**: DynamoDB(CAS: ConditionExpression + Vector Clock), Cassandra
- **Read-Your-Writes**: Sticky Session + Read Replica Routing
- **Saga Pattern**: Choreography(이벤트 체인) vs Orchestration(Temporal/Camunda), 보상 트랜잭션(Compensating Transaction) 설계 필수

**3. 무중단 배포 전략**
- **Rolling Update**: maxSurge=25%, maxUnavailable=0 -> 순차 교체
- **Blue-Green**: Route 53 Weighted Routing 0% -> 100%, ALB Target Group 스왑
- **Canary**: Istio VirtualService weight 5%->25%->50%->100%, **SLO Error Budget** 소진 시 자동 중단(Flagger/Argo Rollouts)
- **Feature Flag**: LaunchDarkly/Split.io, **Dark Launch**(실 트래픽 + Mock 응답) -> **Canary**(5% 사용자) -> **GA**

- **📢 섹션 요약 비유**: K8s 오케스트레이션은 **"항공모함의 비행 갑판"**과 같다. 비행기(컨테이너)가 이륙/착륙(스케줄링)하고, 갑판 요원(Service Mesh Sidecar)이 신호/통신/무장을 관리하며, 갑판 자동화 시스템(HPA/CA)가 이륙 순서를 결정한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **Monolithic On-Premise** | **Cloud-Native (K8s + MSA)** | **하이브리드 (Hybrid/Multi-Cloud)** |
| :--- | :--- | :--- | :--- |
| **확장 단위** | 서버 단위(Scale-Up, 수 시간) | Pod 단위(Scale-Out, 수 초~분) | 워크로드별 클라우드 선택(수 분) |
| **배포 주기** | 주 1~월 1회, 야간 수동 | 일 수십~수천 회, GitOps 자동화 | 변경 빈도별 분리 가능 |
| **장애 영향** | 단일 장애점(SPOF), 전체 장애 | 서비스별 장애격리(Bulkhead), Circuit Breaker | 클라우드 장애 시 Fallback |
| **데이터 일관성** | Strong(분산 트랜잭션, 2PC) | **Eventual + Saga** (BASE) | Cross-Region Replication(DR) |
| **기술 스택** | 단일 언어/DB 종속(J2EE + Oracle) | Polyglot(Java/Go/Python/Rust × 12개 DB) | 워크로드 최적 스택 |
| **비용 모델** | CapEx(선투자), 감가상각 | OpEx(사용량), **Reserved 60% + On-Demand 30% + Spot 10%** | 워크로드 배분 최적화 |
| **거버넌스** | 중앙 집중(Change Advisory
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 713 / 800

<- **이전**: [712. 클라우드 아키텍처 핵심 토픽 712번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/712_cloud_architecture_core_topic_712_exam_summar/)
**다음**: [714. 클라우드 아키텍처 핵심 토픽 714번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/714_cloud_architecture_core_topic_714_exam_summar/) ->

---
