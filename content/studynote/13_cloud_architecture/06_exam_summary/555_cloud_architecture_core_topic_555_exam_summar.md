---
title: "555. 클라우드 아키텍처 핵심 토픽 555번 시험 요약 (Cloud Architecture Core Topic 555 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 API·SDK 기반의 셀프서비스 프로비저닝, 컨트롤 플레인/데이터 플레인 분리, 선언적 인프라(IaC) 및 Immutable Infrastructure를 통해 **탄력성(Elasticity)·확장성(Scalability)·가용성(Availability)**을 코드 레벨에서 보장하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: CapEx->OpEx 전환으로 인프라 TCO를 30~70% 절감하고, Auto Scaling을 통해 트래픽 변동에 ±15분 내 응답하며, Multi-AZ·Multi-Region 구성으로 RTO/RPO를 분 단위로 단축 가능하다(AWS S3 99.999999999% durability, Azure 99.99% SLA 등).
> 3. **판단 포인트**: 핵심 트레이드오프는 **(1) Control Plane 비용·복잡도 vs 운영 자동화 이득**, **(2) Managed Service 종속(Vendor Lock-in) vs 운영 부담 경감**, **(3) Consistency vs Availability (CAP Theorem)**이며, 12-Factor App·Well-Architected Framework·Cloud-Native Maturity Model로 정량적 의사결정해야 한다.

---

## Ⅰ. 개요 및 필요성

기존 온프레미스 환경은 **수요 예측 기반의 Over-Provisioning**(평균利用率 15~25%), **수동 프로비저닝**(서버 1대 도입 4~8주), **수직 확장(Scale-Up)의 한계**(단일 노드 물리적 한도), **재해복구(DR) 사이트 별도 구축**(투자비 2배) 등 4대 구조적 비효율을 내포하고 있었다. 2006년 AWS S3·EC2 출시 이후, IaaS->PaaS->SaaS->FaaS/Serverless로 진화하며, 클라우드 아키텍처는 단순한 "외부 호스팅"이 아니라 **프로그래밍 가능한 인프라(Programmable Infrastructure)**로 재정의되었다.

NIST SP 800-145는 클라우드를 **5대 필수 특성**(On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)과 **3대 서비스 모델**(IaaS/PaaS/SaaS), **4배 배포 모델**(Public/Private/Hybrid/Community)로 정의하며, 이는 클라우드 아키텍처 설계의 출발점이다.

```text
+--------------------------------------------------------------------+
|              전통 인프라 vs 클라우드 네이티브 아키텍처              |
+--------------------------------------------------------------------+
|                                                                    |
|  [전통적 3-Tier On-Premises]                                       |
|  +--------------+    +--------------+    +--------------+         |
|  | Web Server   |---->| App Server   |---->|   DB Server  |         |
|  | (Stateless)  |    | (Tomcat/JVM) |    | (Oracle RAC) |         |
|  | × 2 (HA)     |    | × 4 (Cluster)|    | × 2 (Active) |         |
|  +--------------+    +--------------+    +--------------+         |
|         |                  |                   |                  |
|         v                  v                   v                  |
|  +-----------------------------------------------------+           |
|  |  SAN/NAS Storage | 물리 방화벽 | 수동 백업(일 1회)  |           |
|  +-----------------------------------------------------+           |
|   ⚠ 도입 6~8주 / 용량利用率 15% / DR 100km 이상 별도 구축          |
|                                                                    |
|  [Cloud-Native 12-Factor Microservices]                            |
|  +-------------------------------------------------------------+  |
|  |  Edge/CDN (CloudFront/Akamai) -- WAF -- API Gateway (Kong) |  |
|  +------------+------------------------------------------------+  |
|               v                                                    |
|  +--------------------------------------------------------------+ |
|  |  K8s Service Mesh (Istio Sidecar)                             | |
|  |  +--------+ +--------+ +--------+ +--------+ +--------+     | |
|  |  |Auth Svc| |Order   | |Payment | |Product | |Notif   |     | |
|  |  |Pod×3   | |Pod×5   | |Pod×4   | |Pod×3   | |Pod×2   |     | |
|  |  +--------+ +--------+ +--------+ +--------+ +--------+     | |
|  |     |           |           |           |           |        | |
|  |     +-----------+-----------+-----------+-----------+        | |
|  |              Event Bus (Kafka/MSK)                            | |
|  +--------------------------------------------------------------+ |
|               v                                                    |
|  +--------------------------------------------------------------+ |
|  | Managed: Aurora Global | DynamoDB | S3 | ElastiCache | SQS   | |
|  | Observability: Prometheus+Grafana+Loki+Tempo (PLG) / EKS    | |
|  | IaC: Terraform/Pulumi | GitOps: ArgoCD/Flux                 | |
|  +--------------------------------------------------------------+ |
|   ✅ 배포 1~3분 / AutoScale / Multi-AZ HA 내장 / IaC 100% 코드화  |
+--------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 전통 인프라가 "정원사 가꾸는 화단"(수동 관리, 경직된 공간)이라면, 클라우드 아키텍처는 "Aquaponics 수경재배 시스템"(센서->제어기->자동 분사->자원 순환)이다. 물(트래픽)이 들어오면 EC2 컨테이너가 자동으로 자라나고, 물이 줄면 자동으로 회수·재배치된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **Control Plane / Data Plane 분리**, **선언적 API(Declarative API)**, **Stateless 인스턴스 + Stateful 외부화**, **결함 허용(Fault Tolerance) by Design**이다. AWS 기준 한 개의 Region은 3개 이상의 독립 Availability Zone(AZ)으로 구성되며, 각 AZ는 100km 이상 이격된 1개 이상의 데이터센터로 구성된다. EBS gp3 볼륨은 99.8~99.9% durability, S3 Standard는 99.999999999%(11 9's) durability를 제공한다.

```text
[클라우드 아키텍처 계층 구조 및 요청 처리 플로우]

  User Device (Mobile/Web)
       | HTTPS (TLS 1.3, HTTP/2)
       v
+----------------------------------------------------------+
|  L7 LB / Global Accelerator                              |
|  (Anycast IP, Health Check 30s)                           |
+----------+-----------------------------------------------+
           v
   +--------------------------------------------+
   |  WAF + Shield Advanced (L7 DDoS 1.5Tbps)   |
   +------------+-------------------------------+
                v
   +----------------------------------------+
   | API Gateway / CloudFront / Cloud CDN   |
   | (Rate Limit 10K rps, JWT Auth)         |
   +------------+---------------------------+
                v
   +----------------------------------------------------+
   |  Service Mesh (Istio/Linkerd) - mTLS, Retry, CB     |
   |  Sidecar Proxy (Envoy) -> Policy Enforcement         |
   |                                                    |
   |  +----------+ +----------+ +----------+            |
   |  |Service A | |Service B | |Service C |            |
   |  |HPA:CPU 70| |HPA:RPS   | |KEDA:Queue|            |
   |  |Min 2 Max | |Min 3 Max | |Min 0 Max |            |
   |  |   20     | |   50     | |   30     |            |
   |  +----+-----+ +----+-----+ +----+-----+            |
   +-------+------------+------------+------------------+
           v            v            v
   +-------------------------------------------------+
   |  Event Streaming (Kafka/MSK, Kinesis, Pub/Sub)   |
   |  Partition Key -> Ordering, Exactly-Once Semantics|
   +------------+------------------------------------+
                v
   +-----------------------------------------------------+
   |  Data Tier (Polyglot Persistence)                   |
   |  - OLTP: Aurora MySQL/PostgreSQL (Read Replica×5)   |
   |  - NoSQL: DynamoDB / CosmosDB (10K wcu/s WCU)       |
   |  - Cache: ElastiCache Redis (Cluster Mode, 6 nodes)  |
   |  - Object: S3 (Lifecycle: IA->Glacier->Deep Archive)  |
   |  - Search: OpenSearch (3 Master + 5 Data)           |
   |  - Warehouse: Redshift/Snowflake (RA3×6)            |
   +-----------------------------------------------------+

   +-----------------------------------------------------+
   |  Cross-Cutting Concerns (Control Plane)             |
   |  Observability: OTLP -> Tempo+Loki+Prometheus        |
   |  Security: IAM + KMS + Secrets Manager + Vault      |
   |  Resilience: Multi-Region Active-Active / Pilot     |
   |  IaC: Terraform (Remote State S3+DynamoDB Lock)     |
   |  Cost: Cost Explorer, Anomaly Detection, Savings Plan|
   +-----------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Edge / CDN 계층** | 글로벌 정적 콘텐츠 전송, DDoS 방어, TLS Termination | CloudFront/Cloudflare/Akamai, Anycast 기반 PoP 600+ 노드, Cache Hit Ratio 85%+ 목표, Brotli 압축 |
| **API Gateway** | 인증·인가, Rate Limiting, Request Routing, Protocol 변환 | Kong(Open Source), AWS API Gateway(10K rps), Apigee(Analytics), gRPC-Web 변환, OpenAPI 3.1 기반 Contract-First |
| **컴퓨트 계층** | 비즈니스 로직 실행, Auto Scaling, 격리 | EC2(Spot/On-Demand/Reserved 3-tier), EKS/ECS Fargate(Serverless Container), Lambda(Cold Start 200ms, 동시성 1000), Warm Pool |
| **Service Mesh** | L7 트래픽 관리, mTLS, Circuit Breaker, Observability | Istio(Envoy Sidecar), Linkerd(2.6MB), Consul Connect, mTLS SPIFFE ID, Istio Ambient(without sidecar, 70% resource 절감) |
| **데이터 계층** | 트랜잭션, 캐시, 검색, 분석의 Polyglot Persistence | Aurora 6-way Read Replica, DynamoDB Global Tables(Multi-Region Strong Consistency), S3 11 9's, Redshift Spectrum(S3 Query) |
| **메시지/이벤트** | 비동기 결합, Backpressure, Fan-out, Exactly-Once | Kafka(Partition 200, ISR 3, Retention 7d), MSK Serverless, SQS Standard vs FIFO, SNS+SQS Fan-out Pattern, EventBridge |
| **보안/IAM** | Zero Trust, 최소 권한, 암호화, 감사 | IAM Role+OIDC(IRSA), KMS Envelope Encryption, Secrets Manager Rotation 30d, VPC Lattice, IAM Access Analyzer, AWS WAF Managed Rule(OWASP Top 10) |
| **Observability** | 메트릭·로그·트레이스 통합, SLO/SLI 측정 | OpenTelemetry(OTel SDK) -> Grafana LGT Stack, MTTD 5분, MTTR 30분, USE/RED Method, SLO Error Budget 기반 Release Gate |

**[핵심 알고리즘·파라미터]**
- **Auto Scaling 결정식**: `DesiredCapacity = max(ceil(CPU_Util × CurrentCapacity / TargetUtil), MinCapacity)` -> Target Tracking 70%, Step Scaling 10% 단위, Predictive Scaling 14일 패턴 학습
- **Consistent Hashing**: Kinesis Partition Key 분배 시 `hash(key) % 360 partitions` (Kinesis) / DynamoDB `hash(partition_key)` mod 4096 partitions
- **CAP Theorem 트레이드오프**: AP 시스템(DynamoDB: 결과적 일관성 1초 내 전파, Latency 5ms p99) vs CP 시스템(Strong Consistency: Latency 2배 증가)
- **Lambda 비용 공식**: `GB-s = (Memory MB / 1024) × Duration ms / 1000`, 128MB@100ms = 12,500회 호출 시 1 GB-s
- **Spot Instance 분배**: Karpenter(2024+ AWS 표준)가 30초 내 Spot 중단 감지 -> Node Rolling Replace -> Pod Eviction 30s 내 완료

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "국제공항의 공항 운영 시스템"과 같다. 관제탑(Control Plane)이 비행기(Instance)의 이착륙을 지시하고, 게이트(API Gateway)에서 승객(Request)이 탑승하며, 수하물 분류 시스템(Message Queue)이 화물을 보내고, 활주로(Multi-AZ)가 다중화되어 한 곳이 닫혀도 항공편이 지연되지 않는다.

---

## Ⅲ. 비교 및 연결

| 구분 | **Monolithic On-Premise** | **Cloud-Native Microservices** | **Serverless / FaaS** | **Hybrid / Multi-Cloud** |
| :--- | :--- | :--- | :--- | :--- |
| **배포 단위** | WAR/EAR (100MB+) | Container Image (50~500MB) | Function (Code Zip) | 컨테이너 + Function 혼합 |
| **확장 모델** | Scale-Up (수직) | HPA/VPA/Cluster Autoscaler (수평) | Concurrency 자동 (1~1000+) | 워크로드별 최적 모델 |
| **확장 시간** | 30분~수 시간 (VM 기동) | 30초~2분 (Pod + Image Pull) | 100ms~1초 (Warm), 200ms (Cold) | 워크로드별 상이 |
| **TCO 패턴** | CapEx 집약 (3년 감가상각) | OpEx (Pay-per-Use, 60% Reserved) | Pure OpEx (Idle=0원) | 데이터 egress 비용 주의 |
| **장애 도메인** | 단일 (전체 장애) | 서비스 단위 (블라스트 반경 제한) | 함수 단위 (격리·자동 재시도) | Region 단위 (리전 격리) |
| **Vendor Lock-in** | 없음 (그러나 이관 곤란) | 중간 (K8s API 표준화) | 높음 (벤더별 트리거·런타임) | 의도적 추상화 (Terraform/Kubernetes) |
| **Stateful 처리** | 인-프로세스 (쉬움) | 외부화 강제 (DB, Redis, S3) | Step Functions / Durable Functions | 워크로드별 분리 |
| **적합 워크로드** | 레거시, 배치, 메인프레임 연계 | Stateful Web/API/이벤트 기반 | 비동기·간헐적·트래픽 변동 큼 | 규제·데이터 주권·클라우드 철회 |
| **관측 도구** | Zabbix/Nagios (에이전트) | Prometheus/Grafana/Tempo (OTel) | CloudWatch/X-Ray (벤더 종속) | 통합 Observability (Datadog/Dynatrace) |
| **개발 생산성** | 릴리즈 주기 1~3개월 | 1~2주 (DORA Elite 기준) | 시간 단위 (이벤트 기반) | 셀프서비스 IaC 필수 |

**[연계·통합 포인트]**
- **IaC 통합**: Terraform 1.
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 555 / 800

<- **이전**: [554. 클라우드 아키텍처 핵심 토픽 554번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/554_cloud_architecture_core_topic_554_exam_summar/)
**다음**: [556. 클라우드 아키텍처 핵심 토픽 556번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/556_cloud_architecture_core_topic_556_exam_summar/) ->

---
