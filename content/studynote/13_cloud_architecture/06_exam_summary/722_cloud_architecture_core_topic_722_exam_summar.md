---
title: "722. 클라우드 아키텍처 핵심 토픽 722번 시험 요약 (Cloud Architecture Core Topic 722 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS/CaaS의 서비스 모델 계층화, Multi-region·Multi-AZ 기반 탄력성, API·이벤트 중심의 느슨한 결합(Loose Coupling)을 통해 컴퓨팅 자원을 코드처럼 선언적으로 추상화하는 패러다임임.
> 2. **가치**: CapEx->OpEx 전환(전형적 30~70% TCO 절감), Auto-Scaling을 통한 트래픽 변동 대응(Time-to-scale: 수 분 이내), Well-Architected 5대 원칙 적용 시 가용성 99.99%·장애복구 RTO < 1시간·RPO < 5분 달성 가능.
> 3. **판단 포인트**: Stateless/Stateful 워크로드 분리, 동기·비동기 통신 혼용(AMQP·Kafka·gRPC), 단일 클라우드 종속(Vendor Lock-in) 회피를 위한 추상화 계층(Container/Kubernetes/Terraform) 도입 여부, 보안을 컴퓨팅 외부로 이동한 Shared Responsibility Model 경계 설정이 핵심 결정 사안임.

---

## Ⅰ. 개요 및 필요성

클라우드 아키텍처는 2006년 AWS S3·EC2 출시 이후 컴퓨팅 자원의 **프로비저닝 자동화**, **탄력적 확장(Elasticity)**, **셀프서비스 API 기반 자원 소비 모델**을 정의하면서 IT 인프라의 근본적 전환을 이끌었다. 본 722번 토픽은 정보관리·컴퓨터시스템 분야 기술사 시험에서 빈번히 출제되는 **클라우드 네이티브(Cloud-Native) 설계 원칙**, **Well-Architected Framework의 5대 기둥(Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization)**, **마이크로서비스·서버리스·이벤트 기반 아키텍처**를 포괄하는 메타 주제다.

기존 On-Premise 환경은 LPAR·VMware 기반의 **수직 확장(Scale-Up)**, 정적 캐파시티 플래닝, 수동 패치·배포(릴리스 주기 6개월~1년)라는 한계를 가졌다. 반면 클라우드 아키텍처는 **선언적 인프라(Declarative Infrastructure)**, **Horizontal Pod Autoscaler 같은 컨트롤 루프**, **GitOps 기반 지속적 배포**를 채택하여, **Time-to-Market을 1/10 수준**으로 단축하고 **사용한 만큼만 지불(Pay-per-Use)**하는 경제 모델을 실현한다.

```text
+----------------------------------------------------------------------+
|                  Cloud Architecture Paradigm Shift                    |
+----------------------------------------------------------------------+
|                                                                       |
|   [On-Premise Era]                       [Cloud-Native Era]           |
|   +-----------------+                    +---------------------+     |
|   | Monolithic App  |  --------------->   | Microservices Mesh  |     |
|   | Physical HW     |   CNCF Maturity    | Container/Pod       |     |
|   | Manual Ops      |      Model         | GitOps/ArgoCD       |     |
|   | CapEx 중심      |                    | FinOps/Observability|     |
|   | MTTR: 시간~일   |                    | MTTR: 초~분         |     |
|   +-----------------+                    +---------------------+     |
|            |                                       |                  |
|            v                                       v                  |
|   +---------------------+             +-------------------------+    |
|   | 자원 활용률 15~25%  |             | Auto-Scale 5~80% 활용   |    |
|   | Capacity Over-Provisioned         | Right-Sized Dynamic     |    |
|   +---------------------+             +-------------------------+    |
+----------------------------------------------------------------------+
```

이러한 패러다임 전환의 본질은 **"Infrastructure as Code + Observability + Immutable Deployment"**의 3축으로 요약된다. K8s의 선언형 YAML, Prometheus·Grafana의 4대 골든 시그널(레이턴시·트래픽·에러·포화도), AMI·컨테이너 이미지의 불변 인프라(Immutable Infrastructure) 원칙이 이를 가능케 한다. 기술사 시험 관점에서는 **공통 프레임워크(AWS WAF·Azure WAF·Google CAF)**를 기반으로 아키텍처 의사결정 정당화(ADR: Architecture Decision Record)를 논리적으로 전개할 수 있어야 한다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "수도꼭지처럼 필요한 만큼 즉시 물(컴퓨팅·스토리지·네트워크)을 틀어 쓰는 도시 인프라"와 같다. 전통적 방식은 정수장을 직접 짓는 것이고, 클라우드는 수요에 따라 자동으로 증축되는 수도관망을 빌려 쓰는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 4계층 참조 모델은 **물리/리전(Region) -> 가용영역(AZ) -> 네트워크(VPC/Subent) -> 컴퓨트/데이터 평면(Compute/Data Plane)**으로 구성된다. 글로벌 사용자 트래픽은 **Anycast·GSLB(Global Server Load Balancing)**로 가장 가까운 Edge POP(Points of Presence)로 라우팅되고, **CDN(CloudFront·Cloudflare)**에서 캐싱된다. 데이터 평면은 **컨트롤 플레인(API/Scheduler)**과 분리되어, 사용자는 kubectl·Terraform·CDK로 선언적 리소스만 기술하고 실제 프로비저닝은 컨트롤러가 조정(Reconcile)한다.

```text
                       Cloud-Native Reference Architecture (4-Layer)
   +----------------------------------------------------------------------+
   |  Layer 1: Global Edge / Control Plane                                |
   |  +------------+ +------------+ +------------+ +------------+        |
   |  | Route 53   | | CloudFront | | WAF/DDoS   | | IAM/Org    |        |
   |  | (DNS)      | | (CDN)      | | Shield     | | SSO/Cognito|        |
   |  +-----+------+ +-----+------+ +-----+------+ +-----+------+        |
   |        +----------+---+------------+--+             |               |
   |  Layer 2: Region/VPC Boundary ------+----------------+               |
   |  +--------------------------------------------------------------+    |
   |  | VPC (10.0.0.0/16) - Transit Gateway - DX/VPN                 |    |
   |  | +----------+ +----------+ +----------+ +----------+         |    |
   |  | | Public   | | Private  | | Isolated | | DB Subnet|         |    |
   |  | |  ALB/NLB | | App Svc  | | Workers  | | RDS/Aurora|        |    |
   |  | +----------+ +----------+ +----------+ +----------+         |    |
   |  +--------------------------------------------------------------+    |
   |  Layer 3: Compute / Orchestration                                     |
   |  +--------------+  +--------------+  +--------------+                |
   |  | EKS/AKS/GKE  |  | Lambda/      |  | ECS/Fargate  |                |
   |  | (K8s Control)|  | Cloud Func   |  | (CaaS)       |                |
   |  | +Istio Mesh  |  | (FaaS)       |  |              |                |
   |  +------+-------+  +------+-------+  +------+-------+                |
   |         +---------+-------+----------+-------+                       |
   |  Layer 4: Data / Observability                                        |
   |  +----------+ +----------+ +----------+ +----------+                |
   |  | S3/Blob  | | DynamoDB | | Kafka/MSK| | Aurora   |                |
   |  | (Object) | | (NoSQL)  | | (Stream) | | (RDBMS)  |                |
   |  +----------+ +----------+ +----------+ +----------+                |
   |  +--------------------------------------------------+                |
   |  |  Observability: Prometheus + Loki + Tempo/Jaeger |                |
   |  |  (Metrics / Logs / Traces 통합: OpenTelemetry)   |                |
   |  +--------------------------------------------------+                |
   +----------------------------------------------------------------------+
```

핵심 동작 원리는 **선언적 컨트롤 루프(Reconciliation Loop)**다. K8s Controller는 `spec`(원하는 상태)과 `status`(현재 상태)의 차이를 지속적으로 감지하고, kube-scheduler가 노드 자원·Taint·Toleration·亲和성 규칙을 고려해 Pod를 배치한다. HPA(Horizontal Pod Autoscaler)는 `CPU/Memory/Custom Metric(QPS·Kafka Lag)`을 기반으로 `replicas = ceil[currentReplicas × (currentMetric / targetMetric)]` 공식으로 스케일링한다. **서버리스(Lambda/Functions)**는 콜드 스타트(콜드 시 100~500ms, Warm 시 수 ms)와 동시성 한도(Concurrency Limit: 기본 1,000)로 인해 **Burst 트래픽 패턴에는 Provisioned Concurrency 또는 Cloudflare Workers(V8 isolate, 콜드 스타트 < 5ms)**로 대응한다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway / Ingress** | 외부 트래픽 진입점, 인증/인가/라우팅 | Kong·Ambassador·AWS API Gateway(엔터프라이즈에서는 Apigee), OIDC/JWT 검증, Rate Limit(Token Bucket, 기본 10,000 RPS) |
| **Service Mesh (Istio/Linkerd)** | 서비스 간 mTLS·관측·트래픽 분할 | Envoy Sidecar(0.5 vCPU·40MB Memory), L7 라우팅(Canary 5%->25%->100%), Circuit Breaker(consecutive_5xx_errors > 5) |
| **Container Orchestrator (K8s/EKS)** | 컨테이너 라이프사이클·오토스케일링·셀프힐링 | Control Plane(etcd RAFT 합의) + Worker(CRI: containerd·CRI-O), HPA·VPA·Cluster Autoscaler 3단계 스케일링 |
| **이벤트 버스 / 메시지 브로커** | 비동기·내구성·순서 보장 통신 | Apache Kafka(파티션 키 기반 순서·Exactly-Once Semantics), AWS SQS/SNS, RabbitMQ(AMQP 0-9-1), 처리량 수십만 msg/s |
| **Managed Database (OLTP/OLAP)** | 트랜잭션 일관성·분석·벡터 검색 | Aurora(MySQL/Postgres 호환, 6-way 복제, RPO=0), DynamoDB Global Tables(Multi-Region Strongly Consistent), Snowflake/BigQuery(Serverless DWH) |
| **Observability 스택** | 메트릭·로그·트레이스 통합 수집·분석 | Prometheus + Grafana(시계열), Loki(로그 인덱싱), Tempo/Jaeger(분산 트레이싱), OpenTelemetry SDK 자동 계측 |
| **IaC (Terraform/Pulumi/CDK)** | 인프라 선언적 코딩·드리프트 감지 | Terraform State(Raft Lock), HCL 모듈화, Atlantis/PR 자동화, Crossplane(K8s CRD 기반 클라우드 자원 추상화) |

핵심 파라미터로 **k8s scheduler의 `requests/limits`**, **Lambda의 `memory` 할당(128MB~10GB, CPU 선형 비례)**, **Aurora의 `cluster_size`(1~15 writer, 0~15 reader)**, **Kafka의 `partition_count`(처리량 = `partition × producer_batch`)**, **S3의 `storage_class`(Standard-IA: 30일, Glacier Instant: ms 단위 검색)** 등을 정확히 이해하고 워크로드 특성에 맞게 튜닝해야 한다. 분산 트랜잭션의 경우 **Saga Pattern(Choreography/Orchestration)** 또는 **Outbox Pattern**으로 ACID를 보상 트랜잭션(Compensating Transaction)으로 우회한다.

- **📢 섹션 요약 비유**: K8s 컨트롤 루프는 "교실의 담임선생님이 출석부(sspec)와 현재 교실 상태(status)를 수시로 비교하며 빈자리를 채우는 것"과 같다. Istio Service Mesh는 "각 학생(서비스)마다 전담 심부름꾼(Sidecar)을 붙여서 우편물 전달·호출 기록을 대신 처리하게 하는 것"이다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처 의사결정 시 자주 혼동되는 개념들을 명확히 구분해야 한다. **IaaS vs PaaS vs SaaS**는 책임 분담 모델(Shared Responsibility), **Monolith vs Microservices**는 배포·장애 단위의 차이, **Serverless vs Container**는 콜드 스타트·실행 시간 한도(15분)·상태 관리의 차이로 구분된다.

| 구분 | IaaS (EC2, Compute Engine) | PaaS (Beanstalk, App Engine) | SaaS (Office 365, Salesforce) | FaaS (Lambda, Cloud Functions) | CaaS (EKS, GKE) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | OS·미들웨어·런타임 직접 관리 | 런타임·미들웨어만 관리, 앱 배포 | 모든 계층 CSP 관리, 설정만 조정 | 코드만 배포, 컨테이너·런타임 자동 | 컨테이너 이미지·오케스트레이션 |
| **확장 단위** | VM 인스턴스 (수 분 소요) | 애플리케이션 인스턴스 (수십 초) | 사용자 단위 라이선스 | 함수 호출 단위 (밀리초) | Pod 단위 (수 초) |
| **콜드 스타트** | 1~3분 (인스턴스 부팅) | 30~90초 (런타임 부팅) | 없음 | 100~500ms (V8 isolate: <5ms) | 1~10초 (이미지 풀) |
| **최대 실행 시간** | 무제한 | 무제한 | 무제한 | 15분 (Lambda 한도) | 무제한 (DaemonSet 가능) |
| **비용 모델** | 인스턴스 시간 과금 (예: m5.large $0.096/h) | 인스턴스 시간 + PaaS 라이선스 | 사용자당/월 (예: $12.5/user) | 호출 수 × 실행 시간 (GB-초) | 노드 시간 + 컨트롤 플레인 ($0.10/h) |
| **적합 워크로드** | 레거시·긴 실행·고성능 HPC | 웹앱·API·중규모 배치 | CRM·협업·문서관리 | 이벤트驱动·API·단순 배치 | MSA·CI/CD·하이브리드 |
| **이
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 722 / 800

<- **이전**: [721. 클라우드 아키텍처 핵심 토픽 721번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/721_cloud_architecture_core_topic_721_exam_summar/)
**다음**: [723. 클라우드 아키텍처 핵심 토픽 723번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/723_cloud_architecture_core_topic_723_exam_summar/) ->

---
