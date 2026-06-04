---
title: "584. 클라우드 아키텍처 핵심 토픽 584번 시험 요약 (Cloud Architecture Core Topic 584 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 **12-Factor App, MSA(마이크로서비스), Container/Orchestration, IaC(Terraform/CloudFormation), Observability(OpenTelemetry 기반 3-Pillar)**를 5대 기둥으로 하며, AWS Well-Architected Framework의 6가지 핵심(운영 우수성/보안/안정성/성능 효율/비용 최적화/지속가능성)을 SLA·RTO·RPO 수치로 정량화하는 것이 본질이다.
> 2. **가치**: 동일 워크로드 대비 IDC 운영 대비 **TCO 35~60% 절감**, Auto-Scaling + Spot Instance 활용 시 컴퓨팅 비용 **50~70% 추가 절감**, GitOps 기반 배포로 **Lead Time 80%(월 단위->시간 단위)**, MTTR 65% 단축(평균 2시간->40분) 등 DevOps Research and Assessment(DORA) 4대 지표 상위권 달성 가능.
> 3. **판단 포인트**: **Public/Private/Hybrid/Multi-Cloud**의 4-Way 선택(데이터 주권·레이턴시·벤더 종속), **Monolith vs Modular Monolith vs MSA vs Serverless**의 세분화(팀 수·배포 빈도·트랜잭션 경계 기준), **동기(REST/gRPC) vs 비동기(Kafka/RabbitMQ/EventBridge)** 통신, **EDA vs Saga vs Choreography vs Orchestration** 패턴의 트레이드오프가 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

전통적인 On-Premise 3-Tier 아키텍처(웹/앱/DB)는 **수직 확장(Scale-Up)** 중심의 정적 용량 계획, **수동 배포(CAP Theorem 위반 없는 모놀리식)**, **CapEx 중심의 HW 투자**라는 한계를 가진다. Netflix가 2008년 DB 손실 이후 클라우드 전환을 시작했고, AWS Lambda(2014), Kubernetes 1.0(2015), Istio 1.0(2018)를 거치며 **Cloud Native Computing Foundation(CNCF)** 산하 150+ 프로젝트가 산업 표준으로 자리잡았다. 2026년 현재 Gartner는 전체 엔터프라이즈 IT 예산의 **51% 이상이 Public Cloud**로 이동할 것으로 예측하며, IDC는 **"By 2027, 85%의 기업이 Multi-Cloud 또는 Hybrid 전략을 채택"**한다고 전망한다.

기술사 관점에서 클라우드 아키텍처의 필요성은 (1) **Business Agility**(탄력적 확장으로 B2C 트래픽 100배 변동 흡수), (2) **Operational Excellence**(Toil 제거·SRE 관행), (3) **Innovation Velocity**(Managed Service 활용으로 차별화 기능 집중), (4) **Global Reach**(Multi-Region Active-Active로 글로벌 가용성 99.99%^)의 4축으로 요약된다.

```text
+--------------------------------------------------------------------------+
|        On-Premise 3-Tier -> Cloud-Native Architecture 진화 흐름          |
+--------------------------------------------------------------------------+
|                                                                          |
|  [1990s] Mainframe    [2000s] 3-Tier        [2010s] Virtualization      |
|   +-----+            +----------+          +------------+               |
|   | HW  |            | Web-App- |          | Hypervisor |               |
|   | 단일 |  --->       | DB 단일  |  --->     | + VM Pool  |               |
|   | 시스템|            | monolith |          | (vSphere)  |               |
|   +-----+            +----------+          +------------+               |
|       |                   |                      |                       |
|       v                   v                      v                       |
|   CapEx 100%         CapEx 80%              IaaS CapEx 40%             |
|   수직확장 한계         단일장애점(SPOF)        VM 단위 과다 provisioning  |
|                                                                          |
|  ------------------- Cloud-Native 전환 (2015~현재) -------------------- |
|                                                                          |
|  [Container]  [Orchestration]  [Service Mesh]  [Serverless]  [GitOps]   |
|  +--------+    +------------+  +------------+  +----------+  +--------+|
|  |Docker  | ->  | Kubernetes | ->| Istio/Linkd| ->|Lambda/   | ->|ArgoCD/ ||
|  |OCI     |    | (K8s 1.30) |  | Envoy      |  |Cloud Fn  |  |Flux    ||
|  +--------+    +------------+  +------------+  +----------+  +--------+|
|       |              |                |              |             |     |
|       v              v                v              v             v     |
|   Immutability   선언적 확장    mTLS/L7 라우팅   Event-Driven   선언적   |
|   + Layer Caching HPA/VPA/     카나리/Blue-Green 0->N Auto-Scale  배포    |
|                  KEDA                                                       |
|                                                                          |
|  결과:  Pay-Per-Use  +  Auto-Healing  +  Policy-as-Code  +  Observability|
+--------------------------------------------------------------------------+
```

**기존 On-Premise vs Cloud-Native 비교 핵심 지표:**
- 배포 주기: 분기 1회 -> 하루 10~100회 (DORA Elite 기준)
- 가용성: 99.9% (8.7h/yr 다운타임) -> 99.99% (52분/yr), 4-nine -> 5-nine
- MTTR: 평균 4시간 -> 30분 이하 (Kubernetes Self-Healing + Observability)
- 인프라 프로비저닝: 수주~수개월 -> **Terraform Plan 기준 5~15분**

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"전세(전액 선불 정액제) -> 월세 + 사용량 요금제(필요한 만큼 즉시 입주/퇴거)"**로의 부동산 패러다임 전환이다. IDC는 자기 집(투자 위험), 클라우드는 Hilton 호텔 체인의 객실 Pool에서 필요한 만큼 빌리는 것.

---

## Ⅱ. 아키텍처 및 핵심 원리

Cloud-Native Reference Architecture(CNCF TAG App Delivery, AWS Well-Architected 기반)는 **수평 계층(Horizontal Layer)**과 **수직 관심사(Vertical Concern)**의 2D 매트릭스로 구성된다. 수평 계층은 Edge -> API Gateway -> Service Mesh -> Microservice -> Data Plane -> Infrastructure이며, 수직 관심사는 Observability, Security, Policy, Identity, Cost가 모든 계층을 관통한다.

### Multi-Region Active-Active 기반 글로벌 클라우드 아키텍처

```text
                       +---------------------------------+
                       |   Global Edge / Anycast Network |
                       |  CloudFront / Cloud CDN / Azure  |
                       |  Front Door / Cloudflare        |
                       +------------+--------------------+
                                    | (TLS 1.3, HTTP/3 QUIC)
                                    v
        +---------------------------------------------------+
        |           Global API Gateway / Load Balancer       |
        |   Route 53 Latency-Based / Azure Traffic Manager   |
        |   (Health Check Interval 30s, Region Failover)    |
        +------+--------------+--------------+--------------+
               |              |              |
        +------v------+ +----v------+ +-----v------+
        |  ap-northeast-2 (서울)   | | us-east-1 (버지니아) | | eu-west-1 (아일랜드) |
        |  +------------------+    | |              | |              |
        |  | WAF + Shield    |    | |              | |              |
        |  | + API Gateway   |    | |              | |              |
        |  | (Rate Limit 1k  |    | |              | |              |
        |  |  RPS per Key)   |    | |              | |              |
        |  +--------+---------+    | |              | |              |
        |           v              | |              | |              |
        |  +------------------+    | |              | |              |
        |  |  EKS / GKE / AKS |    | |              | |              |
        |  |  Service Mesh    |    | |              | |              |
        |  |  (Istio 1.22+)   |    | |              | |              |
        |  |  mTLS STRICT     |    | |              | |              |
        |  |  + Authorization |    | |              | |              |
        |  |     Policy       |    | |              | |              |
        |  +--------+---------+    | |              | |              |
        |           |              | |              | |              |
        |  +--------v---------+    | |              | |              |
        |  | Microservices    |    | |              | |              |
        |  | +----++----+     |    | |              | |              |
        |  | |Auth||User|     |    | |              | |              |
        |  | |Svc ||Svc | ... |    | |              | |              |
        |  | +-+--++-+--+     |    | |              | |              |
        |  |   |Saga|Event     |    | |              | |              |
        |  +---+----+----------+    | |              | |              |
        |      v    v               | |              | |              |
        |  +----------------+       | |              | |              |
        |  |  Event Bus     |◄------+-+--------------+-+              |
        |  |  Kafka/MSK     |  Cross-Region Replication                |
        |  |  MirrorMaker 2 |  (Active-Active or Active-Passive)       |
        |  |  + Schema Reg. |                                        |
        |  +----------------+                                        |
        +-----------------------------------------------------------+
                          |
                          v
        +---------------------------------------------+
        |        Data Tier (Polyglot Persistence)     |
        |  +---------+ +------+ +--------+ +--------+|
        |  |Aurora   | |Redis | |DynamoD | |S3+Lake ||
        |  |Global DB| |Cluster| |Global  | |Iceberg ||
        |  |(RDS)    | |(Elasti| |Tables  | |(Parquet||
        |  |         | |Cache)| |(NoSQL) | | format)||
        |  +---------+ +------+ +--------+ +--------+|
        +---------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Edge / CDN** | 글로벌 정적·동적 콘텐츠 전송, DDoS 방어, TLS Termination | CloudFront, Cloudflare, Fastly — Anycast IP, HTTP/3(QUIC) 지원, Lambda@Edge로 Edge 컴퓨팅 |
| **Global DNS / Traffic Manager** | Region Failover, Geo-Routing, Latency-Based 라우팅 | Route 53 Health Check(30s 간격, 3회 실패 시 Failover), Azure Traffic Manager Priority/Weighted, Cloud DNS |
| **WAF / Shield** | OWASP Top 10 방어, L7 DDoS, Bot Management | AWS WAF Managed Rules + Rate-based Rule(2,000 req/5min), Shield Advanced(L3/L4 DDoS SLA 100% 환불) |
| **API Gateway** | 인증/인가, Rate Limiting, 요청 변환, API 버전관리 | Kong(Plugin 50+), Apigee, AWS API Gateway(10,000 RPS), gRPC-Gateway, GraphQL Federation(Apollo Router) |
| **Service Mesh** | L7 라우팅, mTLS, 카나리 배포, Circuit Breaker, Telemetry | Istio 1.22+(Envoy 1.31 기반 Ambient Mode), Linkerd(2.15, Rust Data Plane), Consul Connect |
| **Container Orchestrator** | 선언적 배포, Self-Healing, HPA/VPA/Cluster Autoscaler, Service Discovery | Kubernetes 1.30(Gateway API GA, Sidecar->Ambient 전환), Karpenter v0.35(노드 프로비저닝 1분 이내) |
| **Microservice Runtime** | 비즈니스 로직 실행, Circuit Breaker, Bulkhead, Distributed Tracing | Spring Boot 3.2+(Virtual Thread), Quarkus 3.6( GraalVM Native 20ms 기동), Node.js 22, .NET 8 AOT |
| **Event Bus / Streaming** | 비동기 메시징, Event Sourcing, CQRS, Saga 오케스트레이션 | Apache Kafka 3.7(KRaft 모드, ZooKeeper 제거), Pulsar(BookKeeper 분리 아키텍처), AWS MSK Serverless, EventBridge |
| **Observability Stack** | Metrics/Logs/Traces 통합, AIOps, SLO 기반 알람 | Prometheus + Grafana + Loki + Tempo(PLGT), Datadog, OpenTelemetry Collector(OTLP 표준), eBPF 기반 Pixie/Tetragon |
| **Data Tier** | 트랜잭션·분석·캐시·Blob 분리 (Polyglot Persistence) | Aurora Global Database(< 1초 RPO), DynamoDB Global Tables(Multi-Region Multi-Active), Redis 7.2 Cluster Mode, S3 + Athena + Iceberg |
| **IaC / GitOps** | 선언적 인프라 정의, Drift Detection, Policy-as-Code | Terraform 1.7+(State Locking via DynamoDB), Pulumi(TS/Python/Go), Crossplane(CRD 기반 K8s Native), ArgoCD/Flux, OPA/Kyverno |
| **Identity / Zero Trust** | ID·암호화·네트워크를 통합 검증(인증되지 않은 신뢰 제거) | SPIFFE/SPIRE(Workload Identity), Vault(동적 Secret), IAM IRSA(EKS Pod별 IAM), KMS BYOK/Hold Your Own Key |

### 핵심 메커니즘 상세

**1. Kubernetes 선언적 오케스트레이션**: `Deployment.spec.replicas=10, strategy=RollingUpdate(maxSurge=25%, maxUnavailable=0)`로 무중단 배포. HPA(Horizontal Pod Autoscaler)는 `metrics.server`로부터 CPU/Memory/custom(external metrics adapter, KEDA 2.13 Prometheus/SQS/Kafka 트리거) 기반으로 `targetMetric: 70%` 임계치로 스케일링. VPA는 권장값을 Recommender 모드로 제공(자동 적용 시 OOMKill 위험). Karpenter는 Spot Interrupt(2분 전 notice) 대응을 위해 **Consolidation + Interruption Queue(AWS SQS)** 통합.

**2. Circuit Breaker & Bulkhead 패턴**: Resilience4j 2.2는 `slidingWindow(10s, count=100), failureRateThreshold=50%, waitDurationInOpenState=30s, permittedNumberOfCallsInHalfOpenState=10`로 구성. **Half
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 584 / 800

<- **이전**: [583. 클라우드 아키텍처 핵심 토픽 583번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/583_cloud_architecture_core_topic_583_exam_summar/)
**다음**: [585. 클라우드 아키텍처 핵심 토픽 585번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/585_cloud_architecture_core_topic_585_exam_summar/) ->

---
