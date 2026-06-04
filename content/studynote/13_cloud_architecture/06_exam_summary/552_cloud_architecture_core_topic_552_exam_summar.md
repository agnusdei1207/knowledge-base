---
title: "552. 클라우드 아키텍처 핵심 토픽 552번 시험 요약 (Cloud Architecture Core Topic 552 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 퍼블릭·프라이빗·하이브리드 클라우드를 아우르는 분산 시스템 아키텍처로서, 컨테이너 오케스트레이션(K8s), 서비스 메시(Istio/Linkerd), 서버리스(FaaS), IaC(Terraform/Pulumi), GitOps(ArgoCD/Flux) 기반의 선언적·자동화·탄력적·관측가능(Observability) 인프라가 결합된 클라우드 네이티브 4대 축(Container/Service Mesh/Immutable Infra/Declarative API)의 통합 설계
> 2. **가치**: Well-Architected Framework 6대 권고(운영 우수성·보안·안정성·성능 효율·비용 최적화·지속 가능성) 기반 시 CAPEX->OPEX 전환, Auto Scaling으로 평균 30~70% 비용 절감, Multi-AZ/Region 구성으로 99.99% SLA 달성, 배포 주기 단축(Quarterly->Daily), MTTR 50% 이상 감소
> 3. **판단 포인트**: Workload별 분산 트레이드오프(CAP 정형, 강한 일관성 vs 결과적 일관성), Cloud Lock-in 위험 vs Multi-Cloud 복잡성, Egress 비용·데이터 주권·규제 준수(ISO 27001·CSAP·PIPL) 충족 여부, 동기식 통신(Sync REST/gRPC) vs 비동기(EventBridge/Pub-Sub) 선택 기준, Stateful 워크로드의 영구 볼륨·백업·DR 전략

---

## Ⅰ. 개요 및 필요성

디지털 트랜스포메이션(DX) 가속화와 COVID-19 이후의 비대면 서비스 폭증으로, 전통적 모놀리식(On-Premise) 3-Tier 아키텍처는 다음 4가지 구조적 한계에 직면했다.

1. **수직 확장(Scale-Up) 한계**: 물리 서버 증설 주기 8~12주, ROI 저하
2. **수동 운영(Snowflake Server)**: 환경별 설정 차이로 인한 배포 실패율 30~40%
3. **탄력성 부재**: Peak 트래픽 10배 변동 시 Idle Capacity 70% 낭비
4. **MTTR 장기화**: 장애 인지 후 복구까지 평균 4~8시간 (Gartner Report 2023)

이에 **NIST SP 800-145**가 정의한 5대 특성(온디맨드 셀프서비스·광대역 네트워크 접근·리소스 풀링·신속한 탄력성·측정 가능한 서비스)을 충족하는 클라우드 아키텍처로의 전환이 필수 불가결해졌다. 클라우드 아키텍처는 단순한 인프라 이전이 아니라, **① 컴퓨트(VM/Container/Serverless) ② 스토리지(객체/블록/파일/데이터레이크) ③ 네트워킹(VPC/SD-WAN/Service Mesh) ④ 보안(IAM/KMS/Zero Trust) ⑤ 관측가능성(Logging/Metrics/Tracing)** 의 5개 도메인을 통합 설계하는 **시스템 오브 시스템즈(System of Systems)** 엔지니어링이다.

특히 **CNCF(Cloud Native Computing Foundation)**가 제시한 클라우드 네이티브 4대 트라이어트랙 — Containerization(85% 기업이 프로덕션 활용, Datadog 2023), Service Mesh(Envoy 기반 70% 점유), Immutable Infrastructure(AMI/Golden Image + 재생 전략), Declarative API(K8s CRD/GitOps) — 이 현대 MSA의 사실 표준이 되었으며, 2024년 기준 글로벌 클라우드 시장 규모는 약 **6,800억 USD(Gartner)**, 국내는 **약 30조 원(과기정통부)** 으로 매년 20% 이상 성장 중이다.

```text
[클라우드 아키텍처 패러다임 전환: 모놀리식 -> 클라우드 네이티브 진화]

  +--------------------------+        +----------------------------------+
  |   Traditional On-Premise |        |      Cloud-Native (2014~현재)    |
  | ------------------------|   ->    | --------------------------------|
  | • Monolithic Application |        | • Microservices (12-Factor App) |
  | • Physical Server       |        | • Container (Docker/Podman)      |
  | • Manual Provisioning   |        | • K8s Orchestration             |
  | • Vertical Scaling      |        | • Horizontal Auto-Scaling       |
  | • Waterfall Deploy      |        | • CI/CD + GitOps (ArgoCD)       |
  | • MTTR: 4~8h            |        | • MTTR: < 30min (SRE)           |
  | • Snowflake Server      |        | • Immutable Infra (Packer)      |
  | • CapEx 중심            |        | • OpEx + FinOps                 |
  | • Best-effort SLA       |        | • SLO 99.99% (Multi-AZ/Region)  |
  +--------------------------+        +----------------------------------+
                  |                                  |
                  v                                  v
   +--------------------------+        +----------------------------------+
   |    제약 사항 및 한계      |        |    클라우드 네이티브 4대 축      |
   | ------------------------|        | --------------------------------|
   | ✗ Capacity Planning 실패 |        | ① Container Orchestration       |
   | ✗ 구성 Drift (Snowflake) |        |    (K8s/ECS/Nomad)               |
   | ✗ 야간/휴일 장애 대응 지연|        | ② Service Mesh                   |
   | ✗ 환경별 차이(dev≠prod)  |        |    (Istio/Linkerd/Consul)        |
   | ✗ 이기종 HW 벤더 종속    |        | ③ Immutable Infrastructure        |
   | ✗ 라이선스 비용 고정비   |        |    (Packer/Bakery/AMI)           |
   |                          |        | ④ Declarative API + GitOps       |
   |                          |        |    (Terraform/ArgoCD/Flux)       |
   +--------------------------+        +----------------------------------+
```

- **📢 섹션 요약 비유**: 모놀리식 아키텍처가 "한 거대한 식당 주방에서 모든 요리를 한 사람이 만드는 것"이라면, 클라우드 네이티브는 "각 요리 전문 셰프(Microservice)가 독립 주방(Container)에서 작업하고, 매니저(K8s)가 실시간 주문량에 따라 셰프 수를 조절하며, 주문은 키오스크(Gateway/API)에서 받고, 모든 과정이 CCTV(Prometheus/Grafana)로 모니터링되는 레스토랑 체인"과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 크게 **5계층 참조 모델(Reference Architecture)** 로 분해된다. AWS Well-Architected, Azure Architecture Framework, Google Cloud Architecture Framework 모두 유사한 5계층 구조를 따르며, 각 계층은 독립적으로 진화 가능하도록 **느슨한 결합(Loose Coupling)** 으로 설계된다.

### 5계층 클라우드 아키텍처 참조 모델

```text
[클라우드 네이티브 5계층 + 횡단 관심사(Cross-Cutting Concerns) 통합 아키텍처]

  +--------------------------------------------------------------------------+
  |  ① Presentation / Edge 계층                                              |
  |  +------------+ +------------+ +-------------+ +--------------------+    |
  |  | CloudFront | | CloudFlare | | Global LB   | | WAF + DDoS Shield  |    |
  |  | (CDN/Edge) | | (Anycast)  | | (L7 ALB)    | | (L3-L7 Filtering)  |    |
  |  +-----+------+ +-----+------+ +------+------+ +---------+----------+    |
  +--------+---------------+---------------+-----------------+---------------+
           v               v               v                 v
  +--------------------------------------------------------------------------+
  |  ② API Gateway / BFF 계층                                                |
  |  +------------------------------------------------------------------+    |
  |  |  Kong / AWS API GW / Apigee / GraphQL Federation / gRPC-Gateway  |    |
  |  |  +------------+ +--------------+ +-------------+ +------------+  |    |
  |  |  | Rate Limit | | Auth (OAuth2)| | Circuit Brk | | Schema Val |  |    |
  |  |  +------------+ +--------------+ +-------------+ +------------+  |    |
  |  +------------------------------------------------------------------+    |
  +----------------------------------+---------------------------------------+
                                     v
  +--------------------------------------------------------------------------+
  |  ③ Application / Service 계층 (클라우드 네이티브 4대 축)                  |
  |  +--------------------------------------------------------------------+  |
  |  |  Service Mesh Control Plane (Istio / Linkerd)                       |  |
  |  |  +--------------+--------------+--------------+--------------+      |  |
  |  |  | mTLS 자동화  |  Traffic Mgmt|  Policy(OPA) |  Telemetry   |      |  |
  |  |  +--------------+--------------+--------------+--------------+      |  |
  |  |                                                                     |  |
  |  |  +-------------------------------------------------------------+    |  |
  |  |  |  Microservices Pods (Deployment / StatefulSet / DaemonSet) |    |  |
  |  |  |  +--------+ +--------+ +--------+ +--------+ +--------+  |    |  |
  |  |  |  |Order  | |Payment | |Catalog | |  User  | |Notify  |  |    |  |
  |  |  |  |  Svc  | |  Svc   | |  Svc   | |  Svc   | |  Svc   |  |    |  |
  |  |  |  |[HPA]  | |[HPA]   | |[HPA]   | |[HPA]   | |[CronJob]|  |    |  |
  |  |  |  +--------+ +--------+ +--------+ +--------+ +--------+  |    |  |
  |  |  +-------------------------------------------------------------+    |  |
  |  +--------------------------------------------------------------------+  |
  |  +-----------------+ +-----------------+ +-------------------------+    |
  |  |  Serverless FaaS| |  Event-Driven   | |  Container Orchestrator |    |
  |  |  (Lambda/Funcs) | |  (EventBridge)  | |  (EKS/AKS/GKE)         |    |
  |  +-----------------+ +-----------------+ +-------------------------+    |
  +----------------------------------+---------------------------------------+
                                     v
  +--------------------------------------------------------------------------+
  |  ④ Data / Storage 계층                                                    |
  |  +--------------+ +--------------+ +--------------+ +--------------+     |
  |  |  RDBMS       | |  NoSQL       | |  Object/Blob | |  Data Lake   |     |
  |  |  (Aurora/    | |  (DynamoDB/  | |  (S3/ADLS/   | |  (Iceberg/   |     |
  |  |   Cloud SQL) | |   CosmosDB)  | |   GCS)       | |   Delta)     |     |
  |  |  + CDC(Kafka)| |  + DAX Cache | |  + Lifecycle | |  + Spark/    |     |
  |  |              | |              | |    Policy    | |    Trino     |     |
  |  +--------------+ +--------------+ +--------------+ +--------------+     |
  |  +--------------+ +--------------+ +---------------------------------+   |
  |  |  In-Memory   | |  Search      | |  Streaming (Kafka/Pulsar/Kinesis)|   |
  |  |  (Redis/     | |  (OpenSearch/| |  - Pub/Sub, Exactly-Once Seman. |   |
  |  |   Memcached) | |   ES)        | |  - Schema Registry (Avro/Proto) |   |
  |  +--------------+ +--------------+ +---------------------------------+   |
  +----------------------------------+---------------------------------------+
                                     v
  +--------------------------------------------------------------------------+
  |  ⑤ Infrastructure / Platform 계층 (Immutable + IaC + GitOps)              |
  |  +--------------+ +--------------+ +--------------+ +--------------+     |
  |  |  Terraform   | |  Packer AMI  | |  Ansible     | |  Crossplane  |     |
  |  |  (HCL/2.x)   | |  (Immutable) | |  (Config Mgmt| |  (K8s-native)|     |
  |  +--------------+ +--------------+ +--------------+ +--------------+     |
  |  +------------------------------------------------------------------+    |
  |  |  Multi-Account Org / Landing Zone (Control Tower / Azure CAF)   |    |
  |  |  - Prod / Stage / Dev / Security / Network 계정 분리            |    |
  |  +------------------------------------------------------------------+    |
  +--------------------------------------------------------------------------+

  ---------------------------------------------------------------------------
  ▓▓▓▓▓ Cross-Cutting Concerns (횡단 관심사) ▓▓▓▓▓
  +------------+ +------------+ +------------+ +------------+ +------------+
  |  Security  | |Observability| |  FinOps    | |  SRE/SLO   | | Compliance |
  |  Zero Trust| | OTel/LGTM  | | Cost Opt.  | | Error Bud. | | CSAP/ISO  |
  |  IAM/KMS   | | Prom/Graf. | | Karpenter  | | Chaos Eng. | | GDPR/PIPL |
  +------------+ +------------+ +------------+ +------------+ +------------+
  ---------------------------------------------------------------------------
```

### 핵심 구성 요소별 역할 및 기술 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컨테이너 오케스트레이터 (K8s)** | 컨테이너화된 워크로드의 자동 배치·스케일·복구·롤링 업데이트 | Pod(1~N 컨테이너), Deployment(Stateless), StatefulSet(Stable NetworkID, PVC), DaemonSet(Node당 1개), Job/CronJob. Control Plane: kube-apiserver(REST) -> etcd(Raft 합의) -> scheduler(필터+스코어링: ResourceFit, Affinity, Taints) -> kubelet(CRI gRPC->containerd). Auto-Scaling 3종: HPA(CPU/Mem/Custom Metric, KEDA로 이벤트 기반), VPA(리소스 권장), Cluster Autoscaler/CA(K
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 552 / 800

<- **이전**: [551. 클라우드 아키텍처 핵심 토픽 551번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/551_cloud_architecture_core_topic_551_exam_summar/)
**다음**: [553. 클라우드 아키텍처 핵심 토픽 553번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/553_cloud_architecture_core_topic_553_exam_summar/) ->

---
