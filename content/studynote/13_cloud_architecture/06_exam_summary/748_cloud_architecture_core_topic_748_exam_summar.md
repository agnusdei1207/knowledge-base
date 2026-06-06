---
title: "Cloud Architecture Core Topic 748 Exam Summary"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS·PaaS·SaaS·FaaS로 추상화된 자원 위에서 컨테이너·Kubernetes·Service Mesh·IaC(Terraform/Ansible)를 통해 선언적·탄력적·가용성 중심의 분산 시스템을 구성하는 것으로, AWS Well-Architected Framework의 5대 기둥(운영 우수성·보안·안정성·성능 효율·비용 최적화)과 12-Factor App 원칙이 설계의 근간을 이룬다.
> 2. **가치**: Auto Scaling·Multi-AZ·Spot Instance·Reserved/Savings Plan을 통해 CAPEX를 OPEX로 전환하면서 동일 워크로드에서 30~70%의 TCO 절감, RTO 분 단위·RPO 초 단위의 재해복구 능력, 그리고 Time-to-Market을 수 주에서 수 시간으로 단축시키는 비즈니스 민첩성을 제공한다.
> 3. **판단 포인트**: CAP Theorem(일관성·가용성·분할내성) 트레이드오프, 동기식 vs 비동기식 메시지 패턴, 강한 일관성(ACID·2PC·Paxos/Raft) vs 최종 일관성(BASE·SAGA·Event Sourcing) 선택, 그리고 Egress 비용·Vendor Lock-in·Shared Responsibility Model 경계 설정이 아키텍트의 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

전통적인 On-Premise 3-Tier 아키텍처는 LAMP 스택 + RDBMS + SAN 스토리지 + L4/L7 로드밸런서 + Active-Standby HA 구성을 통해 1~3년의 하드웨어 수명주기에 묶여 있었다. 이는 (1) **Capacity Planning의 어려움** — 야간 트래픽 100 RPS, 점심시간 10,000 RPS로 변동하는 B2C 서비스에서 최대 트래픽 기준으로 과다 투자, (2) **Time-to-Provision의 한계** — 신규 DB 서버 도입 시 4~8주의 구매·입고·OS설치·패치·테스트 사이클, (3) **글로벌 확장성 부재** — 한국·일본·미주 동시 진출 시 데이터센터 신축 필요, (4) **재해복구 비용** — 멀티 사이트 DR 구성에 수십억 원의 이중 인프라 투자라는 4대 구조적 한계를 노출했다.

클라우드 아키텍처는 **API를 통한 프로그래머블 인프라(IaC)**, **선언적 오케스트레이션(Kubernetes)**, **다중 가용영역(Availability Zone) 기반 가용성**, **사용량 기반 과금(Pay-as-you-go)**이라는 4가지 패러다임 전환으로 이를 해결한다. AWS 기준 2006년 EC2 출시 이후, 2014년 Kubernetes 1.0, 2015년 Lambda(Serverless), 2017년 Istio(Service Mesh), 2018년 Cloud Native Computing Foundation(CNCF) 설립, 2020년 eBPF 기반 observability, 2023년 Generative AI 워크로드 최적화 인스턴스 등장으로 진화해 왔다.

```text
+----------------------------------------------------------------------+
|              클라우드 아키텍처 패러다임 전환 (Evolution Map)            |
+----------------------------------------------------------------------+
|                                                                      |
|  [1980s~2000s]           [2006~2014]              [2014~현재]         |
|   Mainframe ->              IaaS 시대              Cloud Native 시대    |
|  +----------+           +----------+           +----------+          |
|  | Monolith | --------► |  VM 기반  | --------► |Container |          |
|  | + RDBMS  |  LAMP     |  EC2     |  Docker    |K8s·Mesh  |          |
|  | + SAN    |  3-Tier   |  S3·RDS  |  Terraform |Lambda    |          |
|  +----------+           +----------+           +----------+          |
|   CAPEX 중심              CAPEX->OPEX             완전한 OPEX         |
|   수동 장애대응            Auto Scaling 도입        GitOps·SRE          |
|   1~3년 Provision          수 분 Provision         수 초 Provision    |
|   단일 데이터센터           Multi-AZ                Multi-Region+CDN   |
|                                                                      |
|  비용구조: ^ 높음 ----► v 중 ----► v 낮음 (사용량 비례)              |
|  민첩성:  v 낮음 ----^ 중 ----^ 높음 (Dev->Prod 자동화)               |
+----------------------------------------------------------------------+
```

전통적 방식 대비 클라우드 아키텍처의 핵심 가치는 **탄력성(Elasticity)·불변 인프라(Immutable Infrastructure)·선언적 구성(Declarative Configuration)·관찰 가능성(Observability)** 4대 속성에 있다. 탄력성은 Auto Scaling Group + Target Tracking Policy(CPU 70% 기준)로 구현되며, 불변 인프라는 AMI·컨테이너 이미지·Terraform State로 일관된 배포를 보장한다. 선언적 구성은 "원하는 상태(Desired State)"를 YAML/JSON으로 기술하면 컨트롤러가 수렴(Reconciliation)하는 Kubernetes 패러다임이 대표적이며, 관찰 가능성은 Metrics·Logs·Traces 3대 축을 OpenTelemetry로 통합 수집한다.

- **📢 섹션 요약 비유**: 기존에는 식당 주인이 직접 장을 보고 쌀을 씻어 밥을 짓는 셀프 주방 방식이었다면, 클라우드는 **"위대한 셰프에게 '오늘 손님 100명분'이라고 주문하면 30분 후 정확히 그 양의 밥과 반찬이 도착하는"** 주문형 주방 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 5개 계층(리전·가용영역·엣지 로케이션)과 4개 책임 영역(컴퓨트·스토리지·네트워크·보안)이 교차하는 매트릭스로 이해해야 한다. AWS 기준으로 리전(ap-northeast-2) 내 3개 이상의 독립 AZ(a, b, c)로 구성되며, 각 AZ는 물리적으로 분리된 데이터센터 + 독립 전력·냉각·네트워크를 보유한다. 글로벌 트래픽은 Route 53(Anycast DNS) + CloudFront(220+ PoP) + Global Accelerator로 라우팅되어 지연시간을 최소화한다.

```text
+---------------------------------------------------------------------+
|           클라우드 네이티브 아키텍처 참조 모델 (CNRM)                  |
+---------------------------------------------------------------------+
|                                                                     |
|  +---------------------------------------------------------------+  |
|  | Layer 5: Observability & Governance                          |  |
|  |  Prometheus + Grafana / Loki / Tempo / OpenTelemetry          |  |
|  |  OPA(Policy) · Falco(Security) · ArgoCD(GitOps)              |  |
|  +---------------------------------------------------------------+  |
|  +---------------------------------------------------------------+  |
|  | Layer 4: Application Platform (PaaS)                          |  |
|  |  EKS/AKS/GKE · Knative · Cloud Run · Lambda · Fargate         |  |
|  |  Service Mesh: Istio/Linkerd (mTLS, Traffic Mgmt, Retry)      |  |
|  +---------------------------------------------------------------+  |
|  +---------------------------------------------------------------+  |
|  | Layer 3: Data & Messaging                                     |  |
|  |  RDBMS: Aurora(6-way replication) · Cloud Spanner             |  |
|  |  NoSQL: DynamoDB(GSI/LSI) · CosmosDB · MongoDB Atlas         |  |
|  |  Stream: Kafka·Kinesis·Pub/Sub · SQS(Standard/FIFO)          |  |
|  |  Cache: ElastiCache(Redis)·Memorystore · DAX                  |  |
|  +---------------------------------------------------------------+  |
|  +---------------------------------------------------------------+  |
|  | Layer 2: Compute & Container                                  |  |
|  |  IaaS: EC2(m5/c5/r5)·Bare Metal·Spot·Graviton3(ARM64)        |  |
|  |  Container: Docker·containerd·CRI-O                          |  |
|  |  Orchestration: Kubernetes Control Plane + Worker Node        |  |
|  |    (etcd·kube-scheduler·kube-controller-manager·kubelet)     |  |
|  +---------------------------------------------------------------+  |
|  +---------------------------------------------------------------+  |
|  | Layer 1: Infrastructure Foundation                            |  |
|  |  Region/AZ · VPC/Subnet · Transit Gateway · Direct Connect     |  |
|  |  S3·EBS·EFS·FSx · IAM·KMS·Secrets Manager · WAF·Shield       |  |
|  +---------------------------------------------------------------+  |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **리전(Region) / AZ** | 지리적 분리로 재해복구 및 지연시간 최적화 | 리전 간 데이터 전송은 $0.02~0.09/GB, AZ 간은 $0.01/GB의 Egress 비용 발생. RDS Multi-AZ는 Synchronous Replication로 RPO=0, RTO≈60초 |
| **VPC + Subnet** | 논리적 네트워크 격리 (10.0.0.0/16) | Public/Private/Data Subnet 3-Tier 분리, NAT Gateway로 Outbound 인터넷, Internet Gateway로 Inbound, NACL(Stateless) + SG(Stateful) 이중 방화벽 |
| **컴퓨트 (IaaS/FaaS)** | 워크로드 실행 환경 | EC2 m6i(범용)·c6i(컴퓨트)·r6i(메모리)·Graviton3(ARM, 60% 성능/Watt 향상), Lambda는 15분 타임아웃·10GB 메모리·동시성 1000 기본 |
| **스토리지 (Object/Block/File)** | 데이터 영속성 | S3 Standard(11 9s 내구성, 99.99% 가용성)·S3 IA(30일 후)·Glacier(장기 archival). EBS gp3는 3,000 IOPS 기본 + 1,000 GB/s throughput, EFS는 NFSv4 다수 AZ 공유 |
| **오케스트레이션 (K8s)** | 컨테이너 라이프사이클 관리 | Control Plane은 etcd(Raft 합의) + API Server + Scheduler + Controller Manager. Deployment(Stateless), StatefulSet(순서 보장), DaemonSet(노드당 1개), Job/CronJob(배치) |
| **서비스 메시 (Istio)** | L7 트래픽 관리, mTLS, 관찰성 | Envoy Sidecar(1.x 버전부터 Ambient Mesh로 sidecar 제거), mTLS 1.3, Retry/Timeout/CircuitBreaker 정책, Kiali 시각화 |
| **IaC (Terraform)** | 인프라 선언적 프로비저닝 | HCL(HashiCorp Configuration Language)로 State 관리, Plan -> Apply 2단계, S3 Backend + DynamoDB Lock으로 팀 협업, Module 재사용 |
| **GitOps (ArgoCD)** | 선언적 배포 자동화 | Git Repo가 Single Source of Truth, Controller가 Desired State vs Live State 비교 후 Sync, ApplicationSet으로 멀티 클러스터/멀티 환경 관리 |
| **관찰성 (O11y)** | 3대 신호(Metrics/Logs/Traces) 통합 | RED Method(Rate·Errors·Duration) + USE Method(Utilization·Saturation·Errors), SLO/SLI 기반 Error Budget, Sentry·Datadog·Prometheus + Grafana 스택 |
| **보안 (Zero Trust)** | "Never Trust, Always Verify" | IAM Role + IRSA(IAM Roles for Service Accounts), KMS Envelope Encryption, Secrets Manager + Rotation, VPC Endpoint로 PrivateLink 통신 |

핵심 메커니즘으로 **Kubernetes Controller Pattern**을 이해해야 한다. 사용자가 `kubectl apply -f deployment.yaml`로 ReplicaSet의 desired state(예: replicas=3)를 선언하면, kube-controller-manager의 ReplicaSet Controller가 주기적(기본 5초) Reconcile Loop를 통해 현재 상태를 조회하고 차이(diff)를 계산하여 Pod를 생성/삭제한다. 이는 **결국적 일관성(Eventual Consistency)** 을 보장하며, HPA(Horizontal Pod Autoscaler)는 `metrics-server`로부터 CPU/Memory/사용자 정의 메트릭을 15초 간격으로 수집하여 `targetCPUUtilizationPercentage`(예: 70%)를 초과하면 30초~3분 내에 스케일링한다. `kube-scheduler`는 Predicate(가능 노드 필터) + Priority(점수화)의 2단계 알고리즘으로 Pod를 노드에 배치한다.

또 다른 핵심 원리는 **Shared Responsibility Model**이다. AWS·Azure·GCP는 "of the cloud" (하드웨어·리전·AZ·하이퍼바이저) 책임을 지고, 고객은 "in the cloud" (OS·미들웨어·데이터·IAM·네트워크 설정) 책임을 진다. EKS Managed Control Plane는 AWS가, Worker Node
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 748 / 800

<- **이전**: [747. 클라우드 아키텍처 핵심 토픽 747번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/747_cloud_architecture_core_topic_747_exam_summar/)
**다음**: [749. 클라우드 아키텍처 핵심 토픽 749번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/749_cloud_architecture_core_topic_749_exam_summar/) ->

---
