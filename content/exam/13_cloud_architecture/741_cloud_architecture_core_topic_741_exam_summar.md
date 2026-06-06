---
title: "Cloud Architecture Core Topic 741 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 API Gateway(예: Kong, AWS API Gateway), Service Mesh(Istio/Linkerd), Container Orchestration(Kubernetes/EKS/AKS), Serverless Platform(Lambda/Cloud Functions), IaC(Terraform/CloudFormation) 등 7~9개 계층의 디커플링된 컴포넌트를 12-Factor App 원칙과 Well-Architected Framework 5대 축(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화)으로 통합하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: Auto Scaling Group + HPA(Horizontal Pod Autoscaler) 기반 탄력적 확장으로 동일 워크로드 대비 CapEx 대비 OpEx 비율을 약 30~70% 절감하고, AZ(Availability Zone) 3개 이상 Multi-AZ 배포 시 SLA 99.99%(연 52분 이내 장애) 달성이 가능하며, Blue-Green/Canary 배포로 무중단 릴리즈 무다운타임(Zero Downtime)을 구현한다.
> 3. **판단 포인트**: Microservices(Choreography vs Orchestration, Saga Pattern, CQRS/Event Sourcing) vs Modular Monolith, 동기(gRPC/REST) vs 비동기(Kafka/RabbitMQ/SNS/SQS) 통신, Multi-Cloud(Cloud-Agnostic, Terraform+Kubernetes) vs Hybrid Cloud(Direct Connect/ExpressRoute) vs Hyperscaler Lock-in, Stateless(Pod Ephemeral) vs Stateful(CSI Driver, Rook, EBS Persistent Volume) 설계의 트레이드오프가 핵심 의사결정 변수다.

---

## Ⅰ. 개요 및 필요성

전통적인 On-Premise 3-Tier 아키텍처(웹서버-WAS-DB)는 수직 확장(Scale-Up) 한계, 수동 용량 계획, CAPEX 중심의 선투자 비용 구조, Disaster Recovery(DR) 구성 복잡성, 그리고 Time-to-Market 6~18개월의 긴 배포 주기를 가진다. 2006년 AWS S3/EC2 출시 이후 클라우드 컴퓨팅은 IaaS -> PaaS -> SaaS -> FaaS(Serverless) -> SaaS+PaaS 통합형(Supabase, Vercel)까지 발전했으며, 2013년 Docker 등장, 2015년 Kubernetes 1.0 GA, 2017년 Knative/Serverless Container, 2020년 EKS Anywhere/Anthos, 2023년 K8s Gateway API GA 등 Cloud-Native Computing Foundation(CNCF) 생태계가 성숙하면서 클라우드 아키텍처는 "인프라 자동화 -> 애플리케이션 현대화 -> 분산 시스템 정형화"의 3단 전환을 거치게 되었다.

기술사 시험 관점에서 클라우드 아키텍처는 단순히 VM을租赁하는 것을 넘어, **신뢰성(Reliability), 회복탄력성(Resilience), 관측가능성(Observability), 보안(Security Zero-Trust), 비용 거버넌스(FinOps)**의 5대 영역을 아키텍처 레벨에서 동시에 해결해야 하는 종합 설계 역량을 평가한다.

```text
[클라우드 아키텍처 진화 패러다임]

  On-Premise (2000s)                Cloud (2010s)              Cloud-Native (2020s~)
  +------------------+         +------------------+         +----------------------+
  | 물리 서버 구매    |         | VM 중심 IaaS     |         | Container/Serverless |
  | 수동 Capacity     |   ->->->   | Auto Scaling     |   ->->->   | K8s/Istio/Knative    |
  | 6~18개월 배포주기 |         | 분 단위 프로비전 |         | 초 단위 배포/HPA     |
  | 수직 확장 한계    |         | CAPEX -> OPEX    |         | Pay-per-Use/FinOps   |
  | DR 구성 복잡      |         | Multi-AZ 기본    |         | Multi-Region/K8s    |
  +------------------+         +------------------+         +----------------------+
        |                              |                              |
        v                              v                              v
  SPOF(단일장애점) 多          Still VM-bound             Ephemeral + Immutable
  Scale-Up 의존              수동 IaC 스크립트          GitOps/Policy as Code
  HW Lead Time ^             벤더 종속 시작            Cloud-Agnostic 추구
```

**기존 vs 신규 패러다임 비교 (심화)**

| 구분 | On-Premise 전통 아키텍처 | 클라우드 네이티브 아키텍처 |
|:---|:---|:---|
| 자원 프로비저닝 | 4~12주 HW 납기, 수동 OS 설치 | 30초~5분, Terraform/IaC 선언적 |
| 장애 대응 | HA Pair + 수동 DR(Active-Passive) | Multi-AZ + Chaos Engineering(LitmusChaos) |
| 배포 방식 | 야간 배치 + 수동 롤백 | Canary(10%->50%->100%) + 자동 Rollback(Argo Rollouts) |
| 확장 모델 | Scale-Up(서버 추가 증설) | Scale-Out(Horizontal: HPA/VPA/Cluster Autoscaler) |
| 비용 모델 | CAPEX 감가상각 5년 | OPEX Pay-per-Second(Lambda), Reserved(1~3년 60%v) |
| 보안 모델 | Perimeter 방화벽(城堡 모델) | Zero Trust + mTLS(Service Mesh) + OPA(Kubernetes 정책) |
| 관측성 | 로그 수집 + Nagios 폴링 | 3-Pillar(Metrics-Prometheus, Logs-Loki, Traces-Jaeger) |

- **📢 섹션 요약 비유**: On-Premise는 "자기 집 짓기처럼 콘크리트 타설부터 인테리어까지 1년 걸리는" 방식이고, 클라우드 네이티브는 "완성된 모듈식 아파트에 가구만 들이고, 가족 수에 맞춰 즉시 이사할 수 있는" 방식이다. Kubernetes는 이 모듈식 아파트의 **자동 엘리베이터 + 호수 배분 시스템** 역할을 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **Decoupling(결합도 분리)**, **Statelessness(무상태성)**, **Automation(자동화)**, **Observability(관측가능성)**의 4대 설계 원리를 계층별로 구현하는 것이다. 아래는 7-Layer Cloud-Native Reference Architecture이다.

```text
[7-Layer Cloud-Native Reference Architecture]

   +------------------------------------------------------------------------+
   | L7: Edge / CDN & Security    | CloudFront, Cloudflare, Akamai, WAF     |
   +------------------------------------------------------------------------+
   | L6: API Gateway & BFF         | Kong, AWS API GW, Apigee, GraphQL       |
   |     (Rate Limit, Auth, Routing)| + Backend-For-Frontend 패턴            |
   +------------------------------------------------------------------------+
   | L5: Service Mesh              | Istio(Envoy Sidecar), Linkerd, Consul   |
   |     (mTLS, Traffic Mgmt, 관측)| + mTLS 자동화 + Circuit Breaker         |
   +------------------------------------------------------------------------+
   | L4: Application Services      | Microservices: Spring Boot, Go, Node.js |
   |     (Business Logic)          | + Saga/CQRS/Event Sourcing              |
   +------------------------------------------------------------------------+
   | L3: Container Orchestration   | Kubernetes(EKS/AKS/GKE), OpenShift     |
   |     (K8s: Pod/Deployment/HPA) | + Operator Pattern + CRD               |
   +------------------------------------------------------------------------+
   | L2: Data Plane                | Polyglot Persistence                   |
   |     (RDB+NoSQL+Cache+Object)  | PostgreSQL/MySQL + MongoDB/Cassandra    |
   |                               | + Redis/ElastiCache + S3/MinIO          |
   +------------------------------------------------------------------------+
   | L1: Infrastructure & Network  | VPC/Subnet Multi-AZ, Transit GW, TGW    |
   |     (IaC, Network)            | Terraform/Pulumi/CloudFormation         |
   +------------------------------------------------------------------------+
   -------------------------------------------------------------------------
   Cross-Cutting: Observability(Prometheus+Grafana+Tempo+Loki),
                  Security(SIEM, Vault, OPA, Falco), FinOps(Kubecost),
                  CI/CD(Argo CD/Flux, GitOps)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Edge / CDN 계층** | 정적 콘텐츠 캐싱, DDoS 방어, TLS Termination | CloudFront/Cloudflare는 Anycast 네트워크로 200+ PoP에서 엣지 캐싱, Cache-Control 헤더와 Origin Shield로 origin 부하 90%v, WAF 룰(SQL Injection/XSS/L7 DDoS)을 OWASP Top 10 기반으로 적용 |
| **API Gateway & BFF** | 단일 진입점, 인증/인가, Rate Limiting, 라우팅, 응답 집계 | Kong은 Nginx + LuaJIT 기반으로 50K+ RPS 처리, OAuth 2.0/JWT 검증, Redis 기반 Token Bucket 알고리즘으로 Rate Limit(예: 100 req/min), BFF(Backend-For-Frontend) 패턴으로 모바일/웹 응답 분리 |
| **Service Mesh (Istio)** | 서비스 간 mTLS, Traffic Management(Canary/Blue-Green), Circuit Breaker, 분산 추적 | Envoy Sidecar Proxy가 Pod 내 모든 L7 트래픽 가로채기, SPIFFE/SPIRE 기반 워크로드 ID, xDS API로 동적 설정, DestinationRule로 mTLS STRICT 모드, VirtualService로 트래픽 분할(90/10) |
| **Container Orchestration (K8s)** | 컨테이너 스케줄링, 자가 치복, 선언적 배포, Service Discovery | Control Plane(API Server + etcd + Scheduler + Controller Manager)이 Desired State -> Actual State로 Reconciliation Loop, kubelet이 CRI(Container Runtime Interface: containerd/CRI-O) 통해 Pod 실행, kube-proxy가 iptables/IPVS로 ClusterIP 서비스 라우팅 |
| **Application Services** | 비즈니스 로직, 도메인 서비스 | 12-Factor App 원칙: Config는 Environment Variable, Backing Services는 Attachable Resource, Processes는 Stateless, Disposability(빠른 시작/우아한 종료), Dev/Prod Parity |
| **Data Plane (Polyglot)** | 데이터 영속성, 캐시, 객체 스토리지 | RDB(PostgreSQL Aurora: 6-way replication, 15 Read Replicas) + NoSQL(DynamoDB: 10ms P99, 3-AZ 동기 복제) + Cache(Redis Cluster: Sub-ms latency) + Object Storage(S3: 99.999999999% 내구성, 11 9s) |
| **Infrastructure & Network** | 컴퓨팅/네트워크/스토리지 프로비저닝, IaC | Terraform HCL로 선언적 인프라 정의, Plan/Apply 2단계 승인, State는 S3+DynamoDB Lock으로 동시성 제어, Module 재사용, VPC는 /16 서브넷 64K IP, 3-Tier(Public/Private/DB) |

**핵심 메커니즘 심화 (Kubernetes를 중심으로)**

1. **Pod 스케줄링 알고리즘**: kube-scheduler는 (1) Filtering(PodFit, Resource, NodeAffinity, Taint/Toleration, PodTopologySpread) -> (2) Scoring(NodeAffinity 가중치, LeastAllocated, BalancedResource, ImageLocality) -> (3) Binding 순으로 노드를 선정한다. Bin-packing이 아닌 Spread(분산) 기본 정책이다.

2. **HPA(Horizontal Pod Autoscaler) 알고리즘**:
   `DesiredReplicas = ceil[currentReplicas × (currentMetricValue / targetMetricValue)]`
   - 기본 15초 폴링, `--horizontal-pod-autoscaler-sync-period` 조정 가능
   - Stabilization Window: Scale-Down 5분, Scale-Up 0분(즉시)
   - KEDA로 Kafka Lag, SQS Queue Length 같은 외부 메트릭 기반 이벤트 드리븐 스케일링

3. **Service Mesh mTLS 핸드셰이크**:
   ```text
   [Service A Pod]                      [Service B Pod]
   +------------------+                 +------------------+
   | App Container    |                 | App Container    |
   | + Envoy Sidecar  | ---- mTLS 1.3 ---- + Envoy Sidecar  |
   +------------------+   (SPIFFE SVID)  +------------------+
   Step 1: SPIRE Agent -> Workload Identity 발급
   Step 2: Envoy Outbound -> SDS로 SVID 요청
   Step 3: TLS Handshake with X.509 SVID
   Step 4: AuthorizationPolicy(ALLOW/DENY) 검증
   ```

4. **Saga Pattern (분산 트랜잭션)**:
   - **Orchestration**: 중앙 Orchestrator(예: Camunda/Temporal)가 각 서비스의 보상 트랜잭션 순서 제어
   - **Choreography**: Kafka Event 기반으로 각 서비스가 자체 보상 로직 수행(OrderService -> PaymentService -> InventoryService -> ShipmentService)

- **📢 섹션 요약 비유**: Service Mesh는 아파트 단지의 **공용 로비 + CCTV + 택배 분류 시스템**과 같다. 각 집(서비스)이 직접 택배를 처리하지 않고, 로비(Envoy Sidecar)가 모든 외부 요청을 인증·라우팅·추적해준다. Istio는 이 로비를 **중앙 관리실(Control Plane)**에서 통합 운영하는 시스템이다.

---

## Ⅲ. 비교 및 연결

### 1. Service Deployment Model 비교 (Public/Private/Hybrid/Multi/Community)

| 구분 | Public Cloud | Private Cloud | Hybrid Cloud | Multi-Cloud | Community Cloud |
|:---|:---|:---|:---|:---|:---|
| **소유/운영** | AWS/Azure/GCP 등 Hyperscaler | 자체 DC 또는 Hosted Private (Outposts) | On-Prem + Public 연결 | 2개 이상 Public Cloud | 정부/산업별 공용 |
| **예시 기술** | EC2, Azure VM, GCE | OpenStack, VMware vSphere, AWS Outposts | AWS Outposts + S3, Azure Arc | EKS(AWS) + GKE(GCP) 동시 사용 | GovCloud, 의료 전용 |
| **연결 방식** | Internet, Direct Connect | 전용선/VPN | Direct Connect(10Gbps) + Transit GW | EIP/Peering, Anthos/Azure Arc | MPLS/VPN |
| **Latency** | 10~100ms (Region 내) | 1~5ms (LAN) | 5~20ms (Cross-DC) | 50~200ms (Cross-Cloud) | 5~50ms |
| **컴플라이언스** | 클라우드 인증(SOC2/ISO27001) | 완전 통제 (금융/공공 요건) | 데이터 분류별 배치 | 벤더 종속 회피 | 도메인 특화 |
| **CAPEX/OPEX** | OPEX 100% | CAPEX 60% + OPEX 40% | CAPEX 40% + OPEX 60% | OPEX 100% | 혼합 |
| **적합 시나리오** | 스타트업, 트래픽 변동 | 금융/공공, 규제 | 레거시 + 신규 서비스 병행 | 벤더 종속 회피, DR | 정부/의료/연구 |
| **Lock-in 리스크** | High (Hyperscaler) | Low (OpenStack) | Medium | Low (Cloud-Agnostic) | Low |

### 2. Microservices vs Serverless vs Container 비교

| 구분 | Monolith | Microservices (Container) | Serverless (FaaS) | BaaS (Backend-as-a-Service) |
|:---|:---|:---|:---|:---|
| **배포 단위** | 단일 WAR/EAR | 컨테이너 이미지 (Docker) | 함수 코드 (ZIP/Inline) | SDK/API 호출 |
| **확장성** | Scale-Up only | HPA, VPA, Cluster Autoscaler | 자동 (Concurrent Executions) | 자동 (Managed) |
| **콜드 스타트** | 30~120초 (앱 기동) | 1~5초 (Pod 기동) | 100ms~5s (Init Duration) | 0 (항상 Warm) |
| **상태 관리** | Stateful 가능 | Stateless + 외부 DB | Stateless 강제, 15분 타임아웃 | 자동 (Firestore, Amplify) |
| **비용 모델** | 서버 시간 과금 | Pod 시간 과금 (CPU/Mem) | 호출 수 + GB-Second | API 호출당 과금 |

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 741 / 800

<- **이전**: [740. 클라우드 아키텍처 핵심 토픽 740번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/740_cloud_architecture_core_topic_740_exam_summar/)
**다음**: [742. 클라우드 아키텍처 핵심 토픽 742번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/742_cloud_architecture_core_topic_742_exam_summar/) ->

---
