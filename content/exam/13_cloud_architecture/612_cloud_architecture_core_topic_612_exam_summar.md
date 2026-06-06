---
title: "Cloud Architecture Core Topic 612 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 퍼블릭/프라이빗/하이브리드/멀티클라우드 환경에서 IaaS·PaaS·SaaS·FaaS 모델을 워크로드 특성에 맞게 조합하고, 컨테이너·서비스 메시·IaC·GitOps를 통해 선언적·자동화·탄력적 아키텍처를 구현하는 것이 클라우드 아키텍처의 본질이다.
> 2. **가치**: Well-Architected Framework 5대 원칙(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속 가능성) 기반으로 CAPEX를 OPEX로 전환(평균 30~50% TCO 절감), 배포 주기 10배 단축(Time-to-Market), 가용성 99.99%(Four 9s) 달성이 가능하다.
> 3. **판단 포인트**: 클라우드 락인 리스크 vs 멀티클라우드 복잡성, Stateless/Stateful 워크로드 분리, Cold Start 지연 vs Warm Pool 비용, Egress 비용·데이터 주권·규제 준수(데이터 3법, GDPR) 간 트레이드오프를 아키텍처 결정 매트릭스로 정량화해야 한다.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 IT 시스템은 2006년 AWS S3·EC2 출시 이후 18년간 서버리스·컨테이너·AI 인프라 패러다임으로 급격히 진화했다. 기존 모놀리식 온프레미스 환경은 **수직 확장(Scale-Up) 한계, 수개월 단위 프로비저닝, 30~40% 유휴 자원, CapEx 과다 투자**라는 4대 구조적 문제에 직면했다. 2024년 기준 전 세계 퍼블릭 클라우드 시장 규모는 약 6,800억 USD(Kubernetes 기반 컨테이너 워크로드 비중 78%)이며, 국내 클라우드 전환율은 41%(2024 KISA 실태조사)까지 도달했다.

기술사 관점에서 클라우드 아키텍처는 단순한 인프라 이전이 아니라 **도메인 주도 설계(DDD)·12-Factor App·Cell-Based Architecture·Zero Trust** 원칙을 코드와 인프라에 동시에 적용하는 소프트웨어 엔지니어링 패러다임이다. 특히 금융·공공·제조 분야는 **클라우드 안전성 평가·SaaS 보안 인증·DAMA(데이터 관리) 거버넌스**와 결합하여 아키텍처의 정합성을 증명해야 한다.

```text
+-------------------------------------------------------------+
|          클라우드 아키텍처 패러다임 전환 (On-Prem -> Cloud)  |
+-------------------------------------------------------------+
|                                                              |
|   [기존 모놀리식]              [모던 클라우드 네이티브]       |
|                                                              |
|   +--------------+           +--------------------------+   |
|   |  Monolith    |           |  Microservices + Mesh    |   |
|   |  (1-tier)    |     ->     |  (Cell/Region 분산)       |   |
|   |              |           |                            |   |
|   |  Bare Metal  |           |  EKS/AKS/GKE + Istio     |   |
|   |  SAN Storage |           |  S3/Blob + RDB+NoSQL     |   |
|   |  수동 배포    |           |  ArgoCD/Flux GitOps      |   |
|   |  수평확장 ✗   |           |  HPA/VPA/Cluster Autoscaler|   |
|   +--------------+           +--------------------------+   |
|                                                              |
|   Cycle: 6~12개월             Cycle: 1일~1시간 (CI/CD)      |
|   가용성: 99.9% (3 nines)      가용성: 99.99% (4 nines)      |
|   CAPEX 100%                  OPEX 60~70% (Pay-as-you-go)  |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **호텔 체인 프랜차이즈**와 같다. 직접 건물을 짓고 관리하는 것(온프레미스)이 아니라, 표준화된 객실(컴퓨팅·스토리지·네트워크)을 필요할 때 즉시 빌려 쓰고, 객실 수를 자동 조절하며, 전 세계 어디서나 동일한 품질의 서비스(SLA 99.99%)를 제공받는 모델이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **5계층 책임 분담 모델(Shared Responsibility Model)**과 **선언적 API(Declarative API)**를 통한 자동화이다. AWS·Azure·GCP·NCP·Kakao Cloud 등 모든 CSP(Cloud Service Provider)는 컴퓨팅·스토리지·네트워크·데이터베이스·보안을 IaC(Infrastructure as Code) 도구(Terraform, Pulumi, AWS CDK)로 코드로 정의하고, GitOps 컨트롤러(ArgoCD, Flux)가 실제 상태를 desired state로 수렴시킨다.

핵심 작동 원리는 **선언(Declare) -> 조화(Reconcile) -> 관측(Observe) -> 자가 치유(Self-heal)**의 4단계 제어 루프이다. Kubernetes의 Control Plane(API Server, etcd, Scheduler, Controller Manager)이 이를 구현하며, Service Mesh(Istio, Linkerd, Consul)가 L7 트래픽 관리·mTLS·Circuit Breaker·카나리 배포를 사이드카 패턴(Envoy Proxy)으로 처리한다.

```text
+--------------------------------------------------------------+
|         클라우드 네이티브 아키텍처 7계층 참조 모델           |
+--------------------------------------------------------------+
|                                                              |
|  [L7] Observability    : Prometheus+Grafana+Loki+Jaeger+Tempo|
|  [L6] GitOps/CI-CD     : GitHub Actions -> ArgoCD (Pull)     |
|  [L5] Service Mesh     : Istio (mTLS, Traffic Mgmt, Policy) |
|  [L4] Orchestration    : Kubernetes (EKS/AKS/GKE/NKS)        |
|  [L3] Runtime          : Containerd / CRI-O (Pod/Sandbox)   |
|  [L2] Image/Registry   : OCI Image (Harbor, ECR, ACR)       |
|  [L1] IaC/Provisioning : Terraform / Pulumi / Crossplane     |
|  [L0] Infra            : Region/AZ/Edge PoP (VPC, Subnet)   |
|                                                              |
|  ------------ 데이터 평면 (Data Plane) -------------         |
|  Application Pod -> Sidecar(Envoy) -> Node CNI -> VPC Endpoint |
|  -----------------------------------------------------       |
+--------------------------------------------------------------+

         [GitOps 자동화 루프]
         +----------------------------------+
         |  Developer -> Git Push (main)     |
         |        v                          |
         |  CI: Build -> Test -> SBOM -> Sign  |
         |        v                          |
         |  Registry: Push OCI Image (Cosign)|
         |        v                          |
         |  CD: ArgoCD Sync (3-way merge)   |
         |        v                          |
         |  K8s: Reconcile -> Rollout        |
         |        v                          |
         |  Observe: Metrics/Logs/Traces     |
         |        v                          |
         |  Feedback -> Git (Policy as Code) |
         +----------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Control Plane (K8s/API)** | 클러스터 상태 관리·스케줄링·조화 | etcd 분산 KV 저장(RAFT 합의), API Server(8000+ CRD), Scheduler(2단계 필터링+스코어링), Controller Manager(Garbage Collection, Node Lifecycle) |
| **Service Mesh (Istio/Linkerd)** | L7 트래픽 관리·제로트러스트 보안 | Envoy Sidecar(15090 stats), mTLS SPIFFE ID, VirtualService(라우팅 규칙 4-tuple), DestinationRule(Load Balancer: ROUND_ROBIN/LEAST_REQUEST/RING_HASH) |
| **IaC (Terraform/OpenTofu)** | 인프라 선언적 프로비저닝 | HCL DSL -> Plan(310+ Provider) -> Apply, State Lock(DynamoDB), Module Registry(Ver. SemVer), Sentinel/OPA Policy as Code |
| **Observability Stack** | 3대 신호(메트릭·로그·트레이스) 통합 | Prometheus(시계열 TSDB, PromQL 200+ 함수), Grafana(다중 데이터소스), OpenTelemetry(OTLP gRPC 4317), Loki(LogQL, Chunk Store), Tempo/Jaeger(분산 트레이싱) |
| **Edge/Serverless Runtime** | 콜드스타트 최소화·글로벌 엣지 배포 | Lambda/Lambda@Edge(Cold Start 200~500ms), Cloudflare Workers(V8 Isolate <5ms), Knative Serving(Queue-Proxy + Activator), Cloud Run(Request-driven) |
| **Data Layer** | 폴리글랏 영속성·이벤트 스트리밍 | Aurora(6-way 복제, 1s lag), DynamoDB Global Tables(Multi-Region Active-Active), Cosmos DB(5개 일관성 모델), Kafka(KRaft, ZooKeeper 제거) |

**핵심 알고리즘 및 파라미터:**
- **K8s 스케줄링**: Spread(균등 분산) vs Binpack(밀집) vs MostRequested(우선순위) 토폴로지 스프레드 제약 조건
- **Consensus**: Raft Leader Election (Election Timeout 150~300ms, Heartbeat 50ms)
- **Auto Scaling**: HPA 지표(CPU/Memory/Custom: 50%) -> KEDA 이벤트 소스(Kafka lag, SQS depth) -> Karpenter 노드 프로비저닝(spot 우선, 90초 내)
- **비용 공식**: `TCO = (Compute × On-Demand/Reserved/Spot 비율) + Egress GB × $0.05~0.09 + Storage × IOPS/GB + API Call 회수`
- **가용성**: `SLA = 1 - ∏(1 - SLA_i)`, 직렬 시 가용성 곱셈 법칙 (예: 99.9% × 99.9% = 99.8%)

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **항공사 관제 시스템**과 같다. 비행기(Pod)·관제탑(Control Plane)·레이더(Observability)·비행경로(Network Policy)·탑승구(Service Mesh)가 정밀하게 조화되어야 수천 대의 항공기가 충돌 없이(Zero Trust) 안전하게(99.99%) 이륙·착륙(Deploy/Rollback)할 수 있다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처는 배포 모델, 서비스 모델, 컴퓨팅 추상화 수준에 따라 직교하는 다축 비교가 필요하다. 특히 기술사 시험에서는 **"왜 이 조합을 선택했는가"**의 정당화를 CAP Theorem, 12-Factor, Conway's Law 관점에서 설명해야 한다.

| 구분 | **Public Cloud** | **Private Cloud** | **Hybrid Cloud** | **Multi-Cloud** |
| :--- | :--- | :--- | :--- | :--- |
| **소유/운영** | CSP 완전 관리 (AWS/Azure/GCP) | 자체 DC + OpenStack/VMware | Public + Private 연동 (Outposts, Anthos, Azure Arc) | 2개 이상 Public CSP |
| **확장성** | 무제한 (수 분 내) | 자사 DC 용량 한계 | 버스팅 가능 (Cloud Bursting) | CSP별 차등 |
| **TCO** | OPEX 100% | CAPEX+OPEX 혼합 | 평시 On-Prem + 첨두 Cloud | 복잡한 Egress 비용 |
| **컴플라이언스** | CSP 인증 활용 (ISO 27001) | 완전 통제 (금융/공공) | 데이터 주권 분리 가능 | 각 CSP별 정책 상이 |
| **적용 사례** | SNS·E-Commerce·스타트업 | 금융 코어뱅킹·의료 HIS | 폐쇄망-공개망 연계 | DR·벤더 종속 제거 |
| **도입 난이도** | 낮음 (5단계) | 높음 (24개월+) | 중간 (12개월) | 높음 (Terraform/Crossplane 필수) |

**서비스 모델 비교 (IaaS vs PaaS vs CaaS vs FaaS):**

| 구분 | **IaaS (EC2/VM)** | **PaaS (Beanstalk/App Service)** | **CaaS (EKS/AKS)** | **FaaS (Lambda/Cloud Functions)** |
| :--- | :--- | :--- | :--- | :--- |
| **추상화 수준** | 하드웨어 | 런타임+미들웨어 | 컨테이너 오케스트레이션 | 함수 단위 |
| **관리 범위** | OS~애플리케이션 | 애플리케이션만 | 이미지~네트워크 | 코드만 |
| **Cold Start** | 없음 (영구) | 없음 | 1~3초 (이미지 Pull) | 200ms~10s (런타임) |
| **확장 단위** | 인스턴스 | 인스턴스 | Pod (1~1000s) | 요청당 컨테이너 |
| **적합 워크로드** | 레거시·Stateful | 웹앱·API | MSA·배치·AI 학습 | 이벤트·단순 API·ETL |
| **비용 모델** | 인스턴스 시간 | 인스턴스 시간 | Pod 시간 + 노드 | GB-초 + 호출 횟수 |

**아키텍처 패턴 진화:**
- **Monolith -> SOA -> Microservices -> Cell-Based -> Serverless Mesh**: Cell-Based는 Netflix에서 유래, 사용자 트래픽을 격리된 Cell(예: 10K 사용자/Cell)로 분할하여 Blast Radius를 최소화한다.
- **연계 기술**: Service Mesh(Istio) + API Gateway(Kong, Apigee, AWS API GW) + Event Bus(EventBridge, Pub/Sub, Kafka) + BFF(Backend-For-Frontend) + Sidecar/Ambient Mesh

- **📢 섹션 요약 비유**: 클라우드 배포 모델은 **전기 공급 방식**과 같다. Public(전력 회사 완전 위탁), Private(자체 발전소), Hybrid(평시 발전소+첨두 시 전력사), Multi-Cloud(여러 전력사 이중화) — 각 방식은 안정성·비용·통제권 사이의 다른 균형점을 제공한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **워크로드 분류 매트릭스 적용 여부**: ① 트랜잭션/배치/실시간 스트리밍 ② Stateful/Stateless ③ CPU-bound vs I/O-bound vs Memory-bound를 분류하고, "Stateless API -> FaaS, Stateful 코어 -> StatefulSet/DB, 배치 -> Spot Instance + Karpenter"로 매핑했는가?
2. **Well-Architected Review 6대 pillar 수행**: ①운영 우수성(Incident Postmortem Blameless, IaC 100%) ②보안(Zero Trust, KMS CMEK, Secrets Manager, CSPM) ③안정성(Multi-AZ, RTO/RPO 정의, Chaos Engineering via AWS FIS) ④성능 효율(Caching Redis/ElastiCache, CDN CloudFront/Cloudflare, DB Connection Pool) ⑤비용 최적화(RI/Savings Plan 60%, Spot 70%, Graviton ARM 40% 성능/비용) ⑥지속 가능성(Carbon Footprint Dashboard, Region Selection by PUE)
3. **마
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 612 / 800

<- **이전**: [611. 클라우드 아키텍처 핵심 토픽 611번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/611_cloud_architecture_core_topic_611_exam_summar/)
**다음**: [613. 클라우드 아키텍처 핵심 토픽 613번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/613_cloud_architecture_core_topic_613_exam_summar/) ->

---
