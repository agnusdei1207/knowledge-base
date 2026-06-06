---
title: "Cloud Architecture Core Topic 633 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 가상화·컨테이너·오케스트레이션·API 기반의 셀프서비스 인프라를 통해 컴퓨팅 자원을 코드(IaC)로 선언하고, 마이크로서비스·이벤트驱动·서버리스 패턴으로 워크로드를 분해하여 **탄력성(Elasticity)·확장성(Scalability)·고가용성(HA)·비용 최적화**를 동시에 달성하는 분산 시스템 설계 체계이다.
> 2. **가치**: AWS·Azure·GCP 등 Hyperscaler의 Region/Edge 네트워크와 Kubernetes·Service Mesh 기반 자동화 스택을 활용 시, 배포 주기 95% 단축(월 1회->일 1~수십 회), 인프라 가용성 99.99%(연 52.6분 이하 장애), CapEx 대비 OpEx 전환으로 초기 투자비 70~80% 절감, Auto-Scaling으로 Peak/Off-Peck 트래픽 차이 10배 환경에서 컴퓨팅 비용 40~60% 절감이 가능하다.
> 3. **판단 포인트**: ① 단일 클라우드 종속(Vendor Lock-in) vs Multi/Hybrid Cloud, ② Monolith->Microservices 리팩토링 시 분산 트랜잭션(Saga·Outbox)·관측가능성(Observability)·데이터 일관성 처리, ③ Stateless 12-Factor vs Stateful StatefulSet, ④ Egress/Storage 비용 폭증 방지를 위한 Region·Storage Tier·Data Lifecycle 정책, ⑤ Zero-Trust·CSPM·CWPP 기반 공유책임 모델 보안 설계가 핵심 의사결정 요소이다.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 IT 시스템은 2006년 AWS S3·EC2 출시 이후 "Utility Computing" 패러다임으로 전환되었으며, 2014년 Docker, 2015년 Kubernetes(1.0) 등장으로 **Infrastructure as Code(IaC) + Container Orchestration**이 클라우드 아키텍처의 표준이 되었다. 633번 토픽은 정보관리기술사/컴퓨터시스템응용기술사가 클라우드 네이티브 시스템의 설계·구축·운영 전 과정을 엔지니어링 관점에서 답안화할 수 있는지를 평가하기 위해 도출된 통합 주제이다.

기존 On-Premise 환경은 **수직 확장(Scale-Up)**, **수동 장애 대응(MTTR 평균 4~8시간)**, **Capacity Over-provisioning(평균利用率 15~25%)**이라는 구조적 한계를 가졌다. 클라우드 아키텍처는 이를 **수평 확장(Scale-Out) + 자동화(Self-Healing) + 사용량 기반 과금(Pay-per-Use)**으로 전환한다. NIST SP 800-145는 클라우드를 5대 핵심 특성(① On-demand Self-Service ② Broad Network Access ③ Resource Pooling ④ Rapid Elasticity ⑤ Measured Service)과 3대 서비스 모델(IaaS/PaaS/SaaS), 4대 배치 모델(Public/Private/Hybrid/Community)로 정의한다.

```text
+----------------------------------------------------------------------+
|          클라우드 아키텍처 패러다임 전환 (On-Prem -> Cloud Native)        |
+----------------------------------------------------------------------+
|                                                                      |
|  [기존 On-Premise Paradigm]            [Cloud-Native Paradigm]       |
|  +------------------+                +------------------+            |
|  | Monolith App     |                | Microservices    |            |
|  |  + RDBMS         |                |  + Polyglot DB   |            |
|  |  + Bare-Metal    |                |  + Container     |            |
|  |  + 수동 배포     |                |  + GitOps/IaC    |            |
|  +------------------+                +------------------+            |
|         |                                       |                    |
|         v                                       v                    |
|  +------------------+                +------------------+            |
|  | ❌ Scale-Up 한계 |                | ✅ Auto Scale-Out|            |
|  | ❌ Capacity 15%  |                | ✅ Util 60~80%   |            |
|  | ❌ Deploy 월1회  |                | ✅ Deploy 일백회 |            |
|  | ❌ MTTR 4~8h     |                | ✅ MTTR < 5min   |            |
|  +------------------+                +------------------+            |
|                                                                      |
|  기술 진화 흐름: Hypervisor -> Container -> Serverless -> Edge          |
|  (2001 VMware) (2013 Docker)  (2014 Lambda) (2018 Cloudflare Workers)|
+----------------------------------------------------------------------+
```

전통적 SI 프로젝트는 6~18개월의 waterfall 방식이었던 반면, 클라우드 아키텍처는 **불변 인프라(Immutable Infrastructure) + Blue/Green·Canary 배포 + Feature Flag**를 통해 비즈니스 가설 검증을 시간 단위로 수행할 수 있게 한다. 또한 2020년 이후 마이크로서비스의 운영 복잡도가 폭증하면서 **관측가능성(Observability: Logs·Metrics·Traces)**, **서비스 메시(Service Mesh: Istio·Linkerd)**, **GitOps(ArgoCD·Flux)**가 새로운 필수 계층으로 부상했다.

- **📢 섹션 요약 비유**: On-Premise는 **"직접 짓고 관리하는 단독 주택(수도·전기·보일러를 모두 직접 유지보수)"**이고, 클라우드 아키텍처는 **"호텔 체인에 룸서비스·자동온도조절·셀프체크인을 요청하는 것"**이다. 다만 호텔이 가진 공용 인프라(Iaas), 셰프가 요리해주는 주방(PaaS), 완전 배달식 도시락(SaaS) 중 어떤 "서비스 수준"을 선택할지가 아키텍트의 첫 번째 결정이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 크게 **① 인프라 계층**, **② 플랫폼 계층**, **③ 애플리케이션 계층**, **④ 운영 계층(Observability/GitOps)**, **⑤ 보안 계층**으로 구성된다. AWS Well-Architected Framework는 5대 기둥(Operational Excellence·Security·Reliability·Performance Efficiency·Cost Optimization), Azure는 6대 원칙(보안·신뢰·우수한 설계·성능 효율성·운영 우수성·비용 최적화), GCP은 5대 원칙(Systems Design·Operational Excellence·Security·Reliability·Performance/Cost)을 제시한다.

```text
+----------------------------------------------------------------------+
|      5-Tier Cloud Reference Architecture (Cloud-Native Stack)         |
+----------------------------------------------------------------------+
|                                                                      |
|  Tier 5: Application & Data                                          |
|  +---------------------------------------------------------+        |
|  |  Microservice A    Microservice B    Microservice C     |        |
|  |  (Node.js)         (Spring Boot)     (Go)               |        |
|  |  Event Sourcing    Saga Orchestrator CQRS Projection     |        |
|  +----------+--------------+-----------------+--------------+        |
|             |              |                 |                        |
|  Tier 4: Service Mesh & API Gateway  -----► [mTLS + RBAC + Retry]   |
|  +---------------------------------------------------------+        |
|  |   Istio Sidecar / Linkerd / Kong / Ambassador           |        |
|  |   Circuit Breaker · Rate Limit · Traffic Split          |        |
|  +----------+--------------+-----------------+--------------+        |
|             |              |                 |                        |
|  Tier 3: Container Orchestration                                     |
|  +---------------------------------------------------------+        |
|  |   Kubernetes (k8s) / EKS / AKS / GKE / OpenShift        |        |
|  |   Pod · Deployment · StatefulSet · Service·Ingress      |        |
|  |   HPA(3종) · VPA · Cluster Autoscaler · Karpenter       |        |
|  +----------+----------------------------------------------+        |
|             |                                                         |
|  Tier 2: Infrastructure as Code (IaC) & Immutable Image            |
|  +---------------------------------------------------------+        |
|  |   Terraform / Pulumi / CDK / Ansible                    |        |
|  |   Packer / Docker / Buildpacks / OCI Image              |        |
|  |   ArgoCD / Flux (GitOps)                                |        |
|  +----------+----------------------------------------------+        |
|             |                                                         |
|  Tier 1: Cloud Infrastructure (IaaS)                                |
|  +---------------------------------------------------------+        |
|  |  Region/Edge  |  VPC/VNet  |  Subnet  |  AZ(3개+)       |        |
|  |  EC2/VM       |  EBS/Disk  |  S3/Blob |  RDS/Cosmos    |        |
|  |  Lambda/Fn    |  Kinesis   |  SQS/SB  |  EventBridge   |        |
|  |  KMS/HSM      |  IAM       |  WAF     |  CloudTrail    |        |
|  +---------------------------------------------------------+        |
|                                                                      |
|  Cross-Cutting: Observability (Prometheus+Grafana+TEMPO+Loki)      |
|  Cross-Cutting: Security (CSPM · CWPP · CIEM · Zero-Trust)          |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Region / AZ(Availability Zone)** | 물리적 데이터센터 그룹 및 장애 격리 단위 | AWS는 30+ Region, 각 Region당 3개 이상의 AZ 운영. AZ 간 latency 1~5ms, Region 간 60~200ms. Multi-AZ는 동기 복제(Sync RPO=0), Multi-Region은 비동기 복제(RPO 수초~수분). |
| **가상 네트워크 (VPC/VNet)** | 논리적 격리, IP 대역·라우팅·보안 그룹 정의 | 10.0.0.0/16 CIDR, /24 Subnet 분할(Public/Private/Data/Management 4-Tier). NACL(Stateless) + Security Group(Stateful) 이중 방화벽. VPC Peering·Transit Gateway·PrivateLink로 다중 VPC 연결. |
| **Kubernetes (오케스트레이터)** | 컨테이너 배치·스케일링·자가 치유·롤링 업데이트 | Control Plane(API Server·etcd·Scheduler·Controller Manager) + Worker Node(kubelet·kube-proxy·Container Runtime). HPA는 CPU/Memory/외부 메트크(QPS·Queue lag) 기준 Pod 수 자동 조정. |
| **Service Mesh (Istio/Linkerd)** | L7 트래픽 제어·관측·보안(mTLS) 분리 | Envoy Sidecar가 Pod 간 모든 트래픽 가로채기. ① Traffic Mgmt(Canary·Fault Injection) ② Security(SPIRE 기반 Workload Identity) ③ Observability(자동 Trace). |
| **API Gateway** | 외부 진입점 단일화, 인증·흐름제어·변환 | Kong·Apigee·AWS API Gateway·Ambassador. Rate Limiting(Token Bucket), OAuth2.0/JWT 검증, GraphQL/REST 매핑, OpenAPI 3.0 기반 계약. |
| **Serverless / FaaS** | 이벤트 기반 stateless 코드 실행, cold start 관리 | AWS Lambda(128MB~10GB, 최대 15분), Azure Functions, GCP Cloud Run(최대 60분). Provisioned Concurrency로 cold start 100ms 이하 유지. Cold start 평균 200~800ms. |
| **Observability 스택 (3요소)** | Logs·Metrics·Traces 통합 수집·분석 | OpenTelemetry SDK로 계측 -> Prometheus(메트릭)·Loki(로그)·Tempo/Jaeger(분산 추적) -> Grafana 대시보드. SLI/SLO 기반 Error Budget 운영. |

**핵심 동작 원리 — Kubernetes의 자기 치유(Self-Healing) 메커니즘:**

1. **선언적 상태(Desired State)**: 사용자가 YAML로 `replicas: 3` 선언
2. **Controller Loop**: kube-controller-manager가 3초 주기(`--node-monitor-period`)로 현재 상태와 비교
3. **불일치 감지**: Pod 사상 시 ReplicaSet이 신규 Pod 기동
4. **준비성 검사(Readiness Probe)**: HTTP `GET /healthz`로 트래픽 수신 가능 시점 통지
5. **Liveness Probe 실패 시**: kubelet이 컨테이너 재기동, 임계치 초과 시 Pod 교체
6. **HPA 동작**: `metrics-server`가 kubelet cAdvisor 메트릭 수집 -> HPA Controller가 `desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]` 계산
7. **Cluster Autoscaler**: Pending Pod 발생 시 노드 그룹 확장, 10분 이상 미사용 노드 축소

**스케일링 알고리즘 핵심 수식:**

$$HPA\ Target = \left\lceil currentReplicas \times \frac{currentMetricValue}{targetMetricValue} \right\rceil$$

이때 `currentMetricValue`가 단조 증가하지 않으면 안정화 윈도우(`--horizontal-pod-autoscaler-downscale-stabilization`, 기본 5분)가 적용되어 Flapping을 방지한다.

**Saga 패턴 (분산 트랜잭션)**: 마이크로서비스 간 데이터 일관성을 위한 2가지 방식
- **Orchestration**: 중앙 Orchestrator(예: Temporal, Camunda)가 단계별 호출·실패 시 보상 트랜잭션 지시
- **Choreography**: 각 서비스가 Event Bus(Kafka)를 통해 비동기 협조, 결합도 v, 추적성 v

**CAP 정리와 클라우드 선택**: 분산 시스템은 ① 일관성(C) ② 가용성(A) ③ 분할 허용성(P) 중 2가지만 보장 가능. DynamoDB는 AP, RDBMS는 CA, Google Spanner는 CP(전 세계 동기식 시계), NoSQL(Cassandra·MongoDB)은 AP가 기본이다. 기술사 답안에서는 "금융 결제" -> CP, "소셜 미디어 피드" -> AP처럼 **업무 특성에 따른 명시적 trade-off**를 보여주어야 한다.

- **📢 섹션 요약 비유**: 5-Tier 스택은 **"도시의 인프라"**이다. Tier1(도로·상하수도)=VPC, Tier2(건물 설계도·건축 표준)=IaC, Tier3(빌딩 관리 시스템)=K8s, Tier4(우편·택배·보안 서비스)=Service Mesh, Tier5(거주자)=Application. 도시가 잘 운영되려면 각 계층이 독립적으로 진화하되 표준 인터페이스(OpenAPI·OCI·CNI·CSI)로 연결되어야 한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **Monolith (전통 3-Tier)** | **Cloud-Native Microservices** |
| :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/EAR 패키지, 1회 배포 = 전체 | 독립 컨테이너, 서비스별 자율 배포 |
| **확장 방식** | Scale-Up(서버 스펙 ^), 동기 호출 | Scale-Out(HPA, Replica ^), 비동기·이벤트 |
| **데이터 일관성** | 단일 RDBMS ACID 트랜잭션 | Saga, Outbox, Eventual Consistency |
| **장애 영향** | 한 컴포넌트 오류 = 전체 Down | Circuit Breaker + Bulkhead로 장애 격리 |
| **기술 스택** | 단일 언어·프레임워크 강제 | Polyglot(Go·Java·Python·Node 각자 최적) |
| **조직** | Conway's Law: 1팀, 컨웨이저비용 1 | Service-per-Team, 독립 배포 파이프라인 |
| **운영 복잡도** | 낮음(1개) | 높음(N개), Service Mesh·Observability 필수 |
| **적합 시나리오** | 소규모 MVP, 단순 CRUD, 레거시 | 대규모 트래픽(Netflix 700+ Microservice), 도메인 복잡 |
| **롤백 비용** | 배포 실패 시 전체 롤백 | Canary + 자동 Rollout(Argo Rollouts)로 부분 영향
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 633 / 800

<- **이전**: [632. 클라우드 아키텍처 핵심 토픽 632번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/632_cloud_architecture_core_topic_632_exam_summar/)
**다음**: [634. 클라우드 아키텍처 핵심 토픽 634번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/634_cloud_architecture_core_topic_634_exam_summar/) ->

---
