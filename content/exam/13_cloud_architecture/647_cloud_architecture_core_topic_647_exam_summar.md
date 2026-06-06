---
title: "Cloud Architecture Core Topic 647 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 647번 토픽은 퍼블릭/하이브리드/멀티클라우드 환경에서 **Well-Architected Framework의 5~6개 pillar(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속가능성)**를 만족시키는 클라우드 네이티브 아키텍처 설계 역량을 평가하며, 핵심은 **컨테이너 오케스트레이션(Kubernetes/EKS/AKS/GKE), 서비스 메시(Istio/Linkerd), IaC(Terraform/Pulumi/Bicep), 옵저버빌리티(OpenTelemetry/Prometheus/Grafana/Loki/Tempo), FinOps**의 통합적 운용이다.
> 2. **가치**: AWS Well-Architected Review를 적용한 프로젝트는 운영 인시던트 **MTTR 60% 단축**, 자동화된 IaC 파이프라인은 배포 리드타임 **90% 감소(일 단위 -> 분 단위)**, FinOps 도입 시 클라우드 비용 **20~35% 절감**(2024 Flexera State of the Cloud Report 기준), 멀티 AZ/리전 아키텍처는 가용성 **99.95% -> 99.99%** 향상을 달성한다.
> 3. **판단 포인트**: **Lift & Shift vs Replatform vs Refactor**의 마이그레이션 전략, **단일 클라우드 종속(Vendor Lock-in) vs 멀티 클라우드 추상화**, **동기식 API vs 이벤트 드리븐(Choreography vs Orchestration)**, **강한 일관성 vs eventual consistency(CAP 트레이드오프)**, **중앙 집중식 거버넌스 vs 분산 셀프서비스 플랫폼 팀(Internal Developer Platform)** 사이의 균형점이 핵심 의사결정 사항이다.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스 3-tier 아키텍처(L7 스위치 -> Web -> WAS -> DB)는 CAPEX 중심의 정적 용량 계획, 수직적 확장(Vertical Scaling)의 한계, 장애 대응의 수동적 운영, 그리고 비즈니스 변화 속도(TTM: Time-to-Market)에 대한 부적응이라는 **4대 구조적 한계**를 내포하고 있다. 2024년 기준 글로벌 클라우드 시장 규모는 약 **6,790억 USD(Gartner)**에 달하며, 디지털 트랜스포메이션, AI/ML 워크로드의 폭증, 그리고 원격 근무의常态化로 인해 **탄력적 컴퓨팅, 글로벌 분산, 사용량 기반 과금(Pay-as-you-use)** 모델이 새로운 표준으로 자리잡았다.

647번 토픽은 단순히 "클라우드를 쓴다"는 차원을 넘어, **클라우드 네이티브 12-Factor App 원칙**, **CNCF(Cloud Native Computing Foundation) 랜드스케이프** 기반의 기술 스택 선정, **AWS Well-Architected / Azure WAF / Google Cloud Architecture Framework**를 활용한 정량적 평가, 그리고 **SRE(Site Reliability Engineering)** 문화 정착을 포괄하는 통합적 설계 역량을 측정한다.

```text
+------------------------------------------------------------------+
|                  클라우드 아키텍처 패러다임 전환 흐름도             |
+------------------------------------------------------------------+

   [On-Premise Era]              [Private Cloud]            [Hybrid/Multi-Cloud]
   1990s ~ 2010s                 2010 ~ 2015                2015 ~ Present
       |                              |                          |
       v                              v                          v
   +--------+                    +---------+               +--------------+
   |Mainframe|  -- 비용 v --->  |OpenStack| -- 유연성^ --->  | AWS/Azure/GCP|
   |단일장애점|     ①           | vSphere |      ②          | SaaS/PaaS    |
   |수동운영 |                 | Hyper-V  |                | Serverless   |
   +--------+                  +---------+                | K8s Service  |
       |                              |                    | Mesh/AI Ops  |
   ❌ 18개월 구축              ⚠️ 6개월 구축              ✅ 1일 ~ 1주 배포
   ❌ CapEx 100%               ⚠️ CapEx 70% OpEx 30%      ✅ OpEx 90%+
   ❌ 가용성 99.9%              ⚠️ 99.95%                   ✅ 99.99% (Multi-AZ)
       |                              |                          |
       +--------------- [Key Driver: TTM, TCO, 탄력성, AI 워크로드] -----+
```

전통적 아키텍처 대비 클라우드 네이티브 아키텍처는 **① 탄력적 오토스케일링(HPA/VPA/Cluster Autoscaler)**, **② 선언적 인프라(IaC + GitOps)**, **③ 회복성(Resilience) - Chaos Engineering(LitmusChaos/Chaos Mesh)**, **④ 마이크로서비스 + API Gateway + Service Mesh** 기반의 세밀한 트래픽 제어로 진화했다.

- **📢 섹션 요약 비유**: 클라우드 전환은 **자가용(소유)에서 카셰어링(공유)으로의 이동**과 같다. 자가용은 초기 비용은 낮지만 유지보수, 보험, 주차, 고장이 전부 본인 책임이지만, 카셰어링은 사용한 만큼만 비용을 내고, 갑자기 가족 10명이 타야 한다면 대형 차량으로 즉시 교체되며, 차량 결함은 운영사가 즉시 해결한다. 단, 어떤 카셰어링 회사를 쓸지, 해외여행 시 호환성 있는지를 신중히 골라야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 크게 **① 컴퓨트/컨테이너 계층**, **② 네트워크/서비스 메시 계층**, **③ 데이터/스토리지 계층**, **④ 운영/관측/보안 계층**의 4-tier로 구성된다. 각 계층은 독립적으로 진화하면서도 CNCF의 **CKA/CKAD** 기반의 통합 운영 모델로 수렴한다.

```text
+---------------------------------------------------------------------+
|              레퍼런스 클라우드 네이티브 아키텍처 (4-Tier)              |
+---------------------------------------------------------------------+

 [End User] --HTTPS/TLS1.3---> [Cloud CDN (CloudFront/Cloud CDN)]
                                    |
                                    v
 +- Tier 1: Edge & Ingress -----------------------------------------+
 |  WAF (OWASP Top10)  ->  ALB/NLB  ->  API Gateway (Kong/Apigee)    |
 |  Rate Limit · JWT Auth · mTLS 종단점                              |
 +------------------------------------------------------------------+
                                    | mTLS (Service Mesh)
                                    v
 +- Tier 2: Application (Kubernetes/EKS/AKS/GKE) ------------------+
 |                                                                   |
 |   [Pod]   [Pod]    [Pod]                                         |
 |     |       |        |                                            |
 |   +-+-------+--------+--+     Istio/Linkerd Sidecar Proxy        |
 |   | Service Mesh Data Plane (Envoy)                              |
 |   | - Traffic Split (Canary 90/10)                                |
 |   | - Retry/Circuit Breaker/Timeout Policy                       |
 |   | - Distributed Tracing (OpenTelemetry)                        |
 |   +------+----------+---------+---------+                        |
 |          v          v         v                                   |
 |   +---------+ +---------+ +----------+                          |
 |   |Auth Svc | |Order Svc| |Payment Svc|  (MSA + DDD Bounded Ctx) |
 |   |+ Sidecar| |+ Sidecar| |+ Sidecar |                          |
 |   +----+----+ +----+----+ +-----+----+                          |
 +--------+-----------+-------------+-------------------------------+
          |           |             |
          v           v             v
 +- Tier 3: Data & Messaging --------------------------------------+
 |  RDBMS:  Aurora Global / Spanner / CosmosDB (CP 시스템)         |
 |  NoSQL:  DynamoDB / MongoDB Atlas / Cassandra (AP 시스템)        |
 |  Cache:  ElastiCache(Redis) / Memcached                          |
 |  Event:  Kafka / EventBridge / Pub/Sub (Choreography)           |
 |  Search: OpenSearch / Elasticsearch                              |
 +------------------------------------------------------------------+
          |           |             |
          v           v             v
 +- Tier 4: Observability & Security ------------------------------+
 |  Metrics : Prometheus + Grafana / CloudWatch / Datadog           |
 |  Logs    : Loki / ELK / OpenSearch / Cloud Logging              |
 |  Traces  : Jaeger / Tempo / AWS X-Ray (OTLP)                     |
 |  Security: Falco (Runtime) · OPA/Kyverno (Policy)                |
 |            Vault (Secret) · IAM + IRSA (Workload Identity)       |
 |  Cost    : Kubecost · CloudHealth · Vantage · FinOps dashboards  |
 +------------------------------------------------------------------+

  IaC: Terraform/Pulumi  |  CI/CD: ArgoCD/Flux (GitOps)  |  Security: Trivy, Snyk
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway** | 외부 트래픽의 단일 진입점, 인증/인가/라우팅/스피드 리미팅/변환 | Kong(Plugin 100+), Apigee(API 수익화), AWS API Gateway(Throttling 10K RPS), Envoy 기반의 Gloo Edge, 게이트웨이 + 메시 통합 아키텍처(API Gateway-less) |
| **Kubernetes Control Plane** | 컨테이너 오케스트레이션: 스케줄링, 자가 치유, 롤링 업데이트, 선언적 상태 관리 | etcd Raft 합의 알고리즘, kube-scheduler(2단계: Filter->Score), kubelet ↔ CRI(Containerd/CRI-O), CNI(Calico/Cilium eBPF), CSI(스토리지) |
| **Service Mesh** | 마이크로서비스 간 mTLS, 트래픽 관리(Canary/A/B), 관측성, 정책(Retry/Timeout/CB) | Istio(Envoy sidecar, xDS API), Linkerd(Linkerd2-proxy Rust 경량), Istio Ambient Mesh(sidecar 제거, 70% 리소스 절감), Cilium Service Mesh(eBPF 기반) |
| **Managed Database** | 다중 AZ 자동 복제, PITR, 자동 백업, 글로벌 분산 | Aurora 6개 복제본(3 AZ, Quorum 4/6), DynamoDB Global Tables(Multi-Region active-active, <1s RTT), Spanner(TrueTime API -> 외부 일관성), CosmosDB(Tunable Consistency: Strong/Bounded/Eventual) |
| **Observability Stack** | 3본석(Metrics/Logs/Traces) 통합, SLO/SLI 측정, 알람 | OpenTelemetry SDK -> OTel Collector -> 백엔드 분기(Prometheus/Loki/Tempo), RED 메서드(Rate/Errors/Duration), USE 메서드(Utilization/Saturation/Errors) |
| **IaC + GitOps** | 인프라의 코드화, 선언적 배포, Git을 Single Source of Truth로 사용 | Terraform(상태 파일 S3+DynamoDB Lock, HCL), Pulumi(general-purpose 언어), ArgoCD(Application CRD, Sync Wave), Flux(v2, Helm Controller, Kustomize Controller) |

**핵심 알고리즘 및 파라미터 심화**:
- **Kubernetes HPA 수식**: `desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]` (예: CPU 80% 목표, 현재 5 Pod, 평균 CPU 200% -> `ceil[5 × (200/80)] = 13 Pod`)
- **Karpenter** (AWS): 전통적 Cluster Autoscaler 대비 **60초 이내 노드 프로비저닝**, Spot/On-Demand 혼합 전략, NodePool CRD 기반
- **CAP Theorem**: 분산 시스템은 **일관성(C)**, **가용성(A)**, **분단 내성(P)** 중 2가지만 만족 가능. 실제 시스템은 PACELC 원칙(분단 시 P vs A, 평시 E vs L)으로 평가
- **Saga Pattern**: 2PC의 한계(장기 lock, cascade rollback) 극복을 위한 **Choreography**(이벤트 기반) vs **Orchestration**(중재자, e.g., Temporal/Camunda) 방식
- **Circuit Breaker 패턴**: Closed -> Open(연속 실패 N회) -> Half-Open(일부 트래픽 허용) -> Closed 복귀, Resilience4j/Hystrix 설정: `failureRateThreshold=50, waitDurationInOpenState=10s, slidingWindowSize=100`

- **📢 섹션 요약 비유**: 이 아키텍처는 **공항의 4개 운영 층**과 같다. 1층(Edge)은 입국장·검표, 2층(Application)은 게이트별 탑승(각 비행기=Pod), 3층(Data)은 화물 터미널(짐을 안전하게 분류), 4층(Observability)은 관제탑이다. 관제탑이 라디오를 끊으면 비행기들이 제각각 날아가므로 **3본석(레이더/통신/로그)**이 반드시 실시간으로 살아있어야 한다.

---

## Ⅲ. 비교 및 연결

647번 토픽은 마이크로서비스, 서버리스, 데브옵스, 전통적 아키텍처 등 인접 개념과 명확한 비교 구분이 필요하다.

| 구분 | Monolithic | Microservice | Serverless (FaaS) |
| :--- | :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/JAR/EAR, 전체 재배포 | 서비스별 컨테이너, 독립 배포 | 함수 단위(Lambda, 250MB 메모리, 15분 타임아웃) |
| **확장성** | 수직 확장(Scale-up) 한계 | 수평 확장(HPA), 서비스별 독립 | 자동 확장(0->1000 동시, 콜드 스타트 200ms~) |
| **장애 격리** | 전체 장애(Blast Radius 100%) | 서비스 단위 격리(CB) | 함수 단위 격리, DLQ |
| **데이터 관리** | 단일 DB(Shared Kernel 안티패턴) | DB per Service, Saga/CQRS | 외부 DB(Glue Catalog) 또는 Stateless |
| **운영 복잡도** | 낮음(초기), 높음(규모^) | 높음(Service Mesh, Observability) | 매우 낮음(벤더 관리형), 콜드 스타이트 이슈 |
| **적합 워크로드** | 소규모 CRUD, 빠른 MVP | 대규모 도메인, 다팀 개발 | 이벤트 드리븐, 스파이크 워크로드, Glue 코드 |
| **TCO** | 초기 낮음, 유지보수 비용 폭증 | 중간(DevOps 인력 필요) | 유휴 시 0원, 대량 호출 시 고비용 |

| 구분 | IaaS (EC2) | PaaS (Beanstalk/App Service) | SaaS (Salesforce) | CaaS (EKS/AKS) |
| :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | OS ~ App 직접 관리 | Runtime까지 관리 | 모든 것 관리 | K8s Control Plane만 관리 |
| **이식성** | 매우 높음(리프트 쉬프트) | 낮음(Vendor 종속) | 없음 | 중간(Manifest는 표준) |
| **제어 수준** | 가장 높음 | 중간 | 가장 낮음 | 높음 |
| **적합 케이스** | 레거시, 특정 커널 튜닝 | 웹앱 빠른 배포 | CRM/ERP/협업 | MSA, AI/ML 파이프라인 |

**타 시스템·도구 연계 포인트**:
- **DevOps 파이프라인**: Git -> Jenkins/GitHub Actions/GitLab CI -> Container Registry(ECR/ACR/GAR) -> ArgoCD/Flux -> K8s -> Datadog/Prometheus
- **보안 통합**: SAST(Veracode/Checkmarx) + DAST(OWASP ZAP) + SCA(S
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 647 / 800

<- **이전**: [646. 클라우드 아키텍처 핵심 토픽 646번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/646_cloud_architecture_core_topic_646_exam_summar/)
**다음**: [648. 클라우드 아키텍처 핵심 토픽 648번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/648_cloud_architecture_core_topic_648_exam_summar/) ->

---
