---
title: "582. 클라우드 아키텍처 핵심 토픽 582번 시험 요약 (Cloud Architecture Core Topic 582 Exam Summary)"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST 참조모델(CCRA)을 기반으로 **온디맨드 셀프서비스, 광대역 네트워크, 자원 풀링, 탄력성(Elasticity), 측정 가능한 서비스(Metered Service)**의 5대 필수 특성을 충족하기 위해 컴퓨팅·스토리지·네트워크·데이터 자원을 API 기반으로 추상화·오케스트레이션하는 통합 설계 체계임.
> 2. **가치**: AWS Well-Architected Framework 6대 축(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속 가능성)을 준수할 경우 인프라 운영 비용 **30~50% 절감**, 배포 주기 **70% 단축(Time-to-Market)**, 가용성 **99.99%(Four 9s) 확보**, Auto Scaling을 통한 트래픽 피크 시 **10x 자동 확장** 가능.
> 3. **판단 포인트**: 핵심 트레이드오프는 **CAP 정리**(Consistency vs Availability vs Partition Tolerance)에서의 워크로드별 선택, **12-Factor App** 원칙 준수 여부, **6R 마이그레이션 전략**(Rehost/Replatform/Repurchase/Refactor/Retire/Retain) 결정, **멀티 클라우드/하이브리드** 도입 시 네트워크 지연(보통 50~150ms)과 벤더 Lock-in 리스크 간의 균형.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스(On-Premise) 환경에서는 CAPEX(Capital Expenditure) 중심의 과대 설계를 통해 트래픽 피크에 대응했으나, 평균 사용률은 **15~20% 수준**에 불과하여 자원 낭비가 심했습니다. 또한 HW 도입 후 서비스 제공까지 **3~6개월**, 트래픽 급증 시 대응은 **수일~수주**가 소요되었습니다. 클라우드 아키텍처는 **가상화(Hypervisor/KVM) -> 컨테이너화(Docker) -> 오케스트레이션(Kubernetes) -> 서버리스(Lambda/Functions)**로 진화하며, IT 자원을 코드(Terraform/CloudFormation/IaC)로 선언적으로 프로비저닝하는 **클라우드 네이티브(Cloud-Native)** 패러다임이 표준이 되었습니다. CNCF(Cloud Native Computing Foundation)는 **컨테이너 자동화, 서비스 메시, 마이크로서비스, 불변 인프라(Immutable Infrastructure), 선언형 API**를 클라우드 네이티브의 5대 핵심 요소로 정의합니다.

```text
[NIST 클라우드 컴퓨팅 참조 아키텍처(CCRA) 기반 전체 조감도]

                         +---------------------------------------------+
                         |         Cloud Consumer (클라우드 소비자)        |
                         |   - 클라우드 워커로드/애플리케이션/데이터        |
                         +------------------+--------------------------+
                                            | (서비스 이용)
                                            v
+-----------------------------------------------------------------------------+
|                  Cloud Provider (클라우드 제공자) 환경                        |
|                                                                             |
|  +--------------+  +--------------+  +--------------+  +--------------+    |
|  | SaaS 계층     |  | PaaS 계층     |  | IaaS 계층     |  | FaaS 계층     |    |
|  | (Office 365, |  | (EBS, App    |  | (EC2, VPC,   |  | (Lambda,      |    |
|  |  Salesforce) |  |  Engine)     |  |  S3, EBS)    |  |  Cloud Funcs) |    |
|  +------+-------+  +------+-------+  +------+-------+  +------+-------+    |
|         +-----------------+-----------------+-----------------+            |
|                                  |                                          |
|  +-------------------------------+--------------------------------------+  |
|  |  Cloud Broker (중개자)        |  - 서비스 중개/통합/이동성                |  |
|  +-------------------------------+--------------------------------------+  |
|                                  |                                          |
|  +-------------------------------+--------------------------------------+  |
|  |  Cloud Auditor (감사자)        |  - 보안 통제/성능/SLA 검증              |  |
|  +-------------------------------+--------------------------------------+  |
|                                  |                                          |
|  +-------------------------------+--------------------------------------+  |
|  |  Cloud Carrier (통신사업자)    |  - 네트워크 전송 (IXP, MPLS, Internet) |  |
|  +-------------------------------+--------------------------------------+  |
|                                  |                                          |
|  +-------------------------------+--------------------------------------+  |
|  |  Physical Resource Layer (물리 자원 계층)                             |  |
|  |   - HW: CPU(Xeon/Graviton), GPU(H100/A100), RAM DDR5, NVMe SSD       |  |
|  |   - Facility: Power(UPS/Generator), Cooling, Rack, DataCenter(IDC)   |  |
|  |   - Network: TOR/Leaf-Spine Fabric, 100G/400G Ethernet, DWDM         |  |
|  +----------------------------------------------------------------------+  |
|                                                                            |
|  +----------------------------------------------------------------------+  |
|  |  Abstraction Layer (추상화 계층)                                       |  |
|  |   - Hypervisor: KVM, Xen, ESXi, Hyper-V                              |  |
|  |   - Container Runtime: runc, containerd, CRI-O                       |  |
|  |   - Storage Abstraction: SDS(Software Defined Storage)                |  |
|  |   - Network: SDN(Software Defined Network), NFV                       |  |
|  +----------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------+
```

**왜 클라우드 아키텍처가 필수인가?**
- **기존(AS-IS)**: 물리 서버 수동 구매(Lead Time 90일), LAMP 스택 단일 배포, 야간 배치 윈도우, DR 사이트 별도 운영(고비용)
- **클라우드(TO-BE)**: API 클릭 또는 IaC 1분 프로비저닝, Immutable Image 기반 Blue/Green 배포, **Multi-AZ/Multi-Region** 자동 DR, 사용량 기반 과금(Pay-As-You-Go)
- **핵심 변화**: Monolith -> Microservices, 수동 운영 -> GitOps/AIOps, Capacity Planning -> Auto Scaling Predictive Modeling, 정적 네트워크 -> 동적 Service Mesh(Envoy/Istio)

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **수도관 시스템**과 같습니다. 과거에는 각 가정마다 정수 시설과 저장 탱크를 따로 갖춰야 했지만(전통적 IDC), 클라우드는 중앙의 거대한 정수장과 배관망(NIST 계층)이 모든 가정에 필요한 만큼의 물을 실시간으로 공급하며, 사용량에 따라 요금을 자동 측정합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 크게 **프레젠테이션 계층**, **애플리케이션 계층**, **데이터 계층**, **인프라/플랫폼 계층**, **운영/관측 계층**으로 구성됩니다. 각 계층은 느슨한 결합(Loose Coupling)을 통해 독립적 확장·배포가 가능하도록 설계되며, 이를 **수평적 확장(Scale-Out)**과 **무중단 배포(Zero-Downtime Deployment)**의 토대가 됩니다.

```text
[클라우드 네이티브 MSA 기반 실전 아키텍처 (3-Tier + Cross-Cutting Concerns)]

  +--------------------------------------------------------------------------+
  |                              End Users (Browser / Mobile)                |
  +----------------------------------+---------------------------------------+
                                     | HTTPS (TLS 1.3)
                                     v
  +--------------------------------------------------------------------------+
  |  [Edge / CDN 계층]                                                        |
  |  - CloudFront / Cloud CDN / Azure Front Door                            |
  |  - WAF (OWASP Top10 방어), Shield (DDoS L3~L7), Route53 (GeoDNS)         |
  +----------------------------------+---------------------------------------+
                                     |
                                     v
  +--------------------------------------------------------------------------+
  |  [API Gateway / BFF 계층]                                                 |
  |  - Kong / AWS API Gateway / Apigee / Spring Cloud Gateway                |
  |  - 기능: 인증(JWT/OAuth2), Rate Limit, Routing, Aggregation, Transformation|
  +----+----------------+------------------+------------------+-------------+
       |                |                  |                  |
       v                v                  v                  v
  +---------+     +---------+       +---------+       +---------+
  | User    |     | Order   |       | Payment |       | Product |
  | Service |     | Service |       | Service |       | Service |
  | (Node)  |     | (Java)  |       | (Go)    |       | (Python)|
  +----+----+     +----+----+       +----+----+       +----+----+
       |               |                 |                 |
       |      +--------+--------+        |                 |
       |      | Service Mesh    |        |                 |
       +-----►| (Istio/Linkerd) |◄-------+-----------------+
              | - mTLS 자동화    |
              | - Circuit Breaker, Retry, Timeout, Bulkhead
              | - 카나리 배포 (Traffic Split 90/10)
              +--------+--------+
                       |
   +-------------------+----------------------------------------------+
   |                   |  [데이터 계층 - Polyglot Persistence]         |
   |  +------------+    |   +------------+   +------------+           |
   |  | RDBMS      |    |   | NoSQL      |   | Cache      |           |
   |  | (Aurora,   |    |   | (DynamoDB, |   | (Redis,    |           |
   |  |  Cloud SQL)|    |   |  MongoDB)  |   |  Memcached)|           |
   |  +------------+    |   +------------+   +------------+           |
   |  +------------+    |   +------------+   +------------+           |
   |  | Search     |    |   | Object     |   | Data       |           |
   |  | (OpenSearch|    |   | Storage    |   | Warehouse  |           |
   |  |  / ES)     |    |   | (S3/GCS)   |   | (Redshift, |           |
   |  +------------+    |   +------------+   |  BigQuery)  |           |
   |                    |                    +------------+            |
   +--------------------+----------------------------------------------+
                       |
                       v
  +----------------------------------------------------------------------+
  |  [Messaging / Event Streaming]                                       |
  |   - Apache Kafka (Partition, Exactly-Once Semantics, Kafka Streams) |
  |   - Amazon SQS/SNS, Pub/Sub, RabbitMQ, EventBridge                  |
  |   - Event Sourcing + CQRS 패턴으로 읽기/쓰기 분리                    |
  +----------------------------------------------------------------------+
                       |
                       v
  +----------------------------------------------------------------------+
  |  [Container Orchestration / Platform]                                |
  |   - Kubernetes(EKS/GKE/AKS/OKE), OpenShift                          |
  |   - Operator Pattern, Helm/Kustomize, ArgoCD (GitOps)                |
  |   - Knative(서버리스 K8s), Karpenter(노드 프로비저닝)                |
  +----------------------------------------------------------------------+
                       |
                       v
  +----------------------------------------------------------------------+
  |  [Observability (관측성 - 3대 축)]                                    |
  |   - Metrics: Prometheus, CloudWatch, Datadog                          |
  |   - Logs:    ELK/EFK, Loki, OpenSearch                               |
  |   - Traces:  Jaeger, Zipkin, AWS X-Ray, OpenTelemetry(OTLP)          |
  +----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway** | 외부 트래픽 단일 진입점, 내부 MSA 라우팅 | Kong(OpenResty+Lua), AWS API Gateway(REST/WebSocket/Lambda 통합), Apigee(API 수익화), 인증은 OAuth2.0/JWT, Throttling은 Token Bucket 알고리즘 |
| **Service Mesh** | 서비스 간 통신의 Infra Layer 분리 (Sidecar 패턴) | Istio(Envoy 기반, xDS API), Linkerd(Linkerd2-proxy, Rust 기반 경량), mTLS 자동 발급(SPIFFE/SPIRE), Traffic Management (VirtualService/DestinationRule) |
| **Kubernetes (k8s)** | 컨테이너 오케스트레이션, 선언적 배포 | Pod(최소 단위), Deployment(롤링 업데이트), StatefulSet(상태 유지), HPA(CPU/Mem/Custom Metric 기준 자동 스케일), Cluster Autoscaler/CA(노드 풀 확장), CRI/CNI/CSI 표준 인터페이스 |
| **Object Storage (S3/GCS)** | 정적 파일, 로그, 백업, 데이터 레이크 | 11 9s 내구성(99.999999999%), Storage Class(Standard/IA/Glacier), Lifecycle Policy로 자동 계층 이동, Event Notification(S3->Lambda 트리거) |
| **Managed RDBMS (Aurora 등)**
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 582 / 800

<- **이전**: [581. 클라우드 아키텍처 핵심 토픽 581번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/581_cloud_architecture_core_topic_581_exam_summar/)
**다음**: [583. 클라우드 아키텍처 핵심 토픽 583번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/583_cloud_architecture_core_topic_583_exam_summar/) ->

---
