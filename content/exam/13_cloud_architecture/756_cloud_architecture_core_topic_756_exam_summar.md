---
title: "Cloud Architecture Core Topic 756 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 제어 평면(Control Plane)과 데이터 평면(Data Plane)의 분리, API 기반 선언적 인프라(IaC), 셀프서비스 프로비저닝을 통해 "탄력적 자원 풀(Elastic Resource Pool)"을 추상화하는 분산 시스템 설계 패러다임이며, 12-Factor App, 셀프힐링(Self-healing), 불변 인프라(Immutable Infrastructure) 원칙이 근간을 이룬다.
> 2. **가치**: AWS Well-Architected Framework 5대 원칙(운영 우수성, 보안, 안정성, 성능효율, 비용최적화) 준거 시 CAPEX 대비 OPEX 전환 30~70%, 오토스케일링으로 평균 트래픽 피크 대응 비용 40% 절감, MTTR(평균복구시간) 60% 단축, 멀티 AZ 배포로 가용성 99.99%(연 52분 이내 장애) 달성.
> 3. **판단 포인트**: 일관성(Consistency)·가용성(Availability)·분단내성(Partition Tolerance) 간 CAP theorem 트레이드오프, EKS vs AKS vs GKE vs Self-managed Kubernetes, VM vs Container vs Serverless(FaaS) 워크로드 매칭, 단일 클라우드 종속(Vendor Lock-in) 회피를 위한 멀티/하이브리드 전략과 추상화 계층(Kubernetes, Terraform) 설계가 핵심 결정 사항.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스(On-Premise) 3-Tier 아키텍처는 Web/App/DB 계층이 물리 서버에 강결합되어, 트래픽 증가 시 수동 하드웨어 조달(Lead Time 4~12주), 라이선스 갱신, 용량 계획의 불확실성이라는 3대 병목을 야기했다. Netflix는 2008년 DVD 대여 사업의 클라우드 전환을 계기로 AWS EC2 전면 도입, 2016년 글로벌 190개국 서비스 확장에서 증명된 바와 같이, 클라우드 아키텍처는 **"Pay-as-you-use"** 과금 모델, **선언적 API(Declarative API)**, **무한 확장 가능한 글로벌 인프라**를 통해 디지털 비즈니스 민첩성(Digital Business Agility)을 확보하는 핵심 인프라 패러다임이다.

한국 정보시스템 기술사 756번 토픽은 클라우드 네이티브(Cloud-Native) 4대 핵심 축인 ① 마이크로서비스(Microservices) ② 컨테이너 오케스트레이션 ③ CI/CD 자동화 ④ DevOps 문화의 통합적 이해와, MSA, 서버리스(Serverless), 이벤트 드리븐(Event-Driven), 메쉬(Serivce Mesh) 등 최신 아키텍처 패턴의 트레이드오프 분석 능력을 평가한다.

```text
[클라우드 진화 단계 및 기술 부재 별 한계점]

  +--------------+      +--------------+      +--------------+      +--------------+
  | Mainframe    | ---► | Client-Server| ---► | 3-Tier (LAMP)| ---► | Cloud-Native |
  | (1960s~80s)  |      | (1990s)      |      | (2000s)      |      | (2015~현재)  |
  +--------------+      +--------------+      +--------------+      +--------------+
        |                      |                      |                      |
        v                      v                      v                      v
  * 단일 시스템          * TCO 높음             * 수직확장 한계           * 자동화/관측성
  * Vendor 종속         * HW 수동조달          * 장애 전파(Single       * 셀프힐링
  * 탄력성 없음          * 24x7 운영            Point of Failure)        * 글로벌 멀티 리전
  * 시분할 처리          * 라이선스 종속         * Peak 기준 과투자       * GitOps/IaC
```

**기존 패러다임 대비 클라우드 아키텍처 도입의 핵심 가치**:
- **Capex->Opex 전환**: IDC 조사 결과 클라우드 전환 시 3년 TCO 37% 절감, 인프라 조달 리드타임 87% 단축
- **탄력성(Elasticity)**: Auto Scaling Group(ASG) + Launch Template 조합으로 트래픽 피크 시 5분 내 1,000대 EC2 인스턴스 확장(예: Amazon Prime Day)
- **글로벌 가용성**: AWS 33개 리전, 105개 가용영역(AZ) — Active-Active 멀티 리전으로 RPO(Recovery Point Objective) 0초, RTO(Recovery Time Objective) 60초 이내 달성
- **기술 민주화**: 200+ AWS 서비스, 100+ Azure 서비스, 100+ GCP 서비스로 ML/IoT/양자컴퓨팅 같은 신기술 즉시 활용

- **📢 섹션 요약 비유**: 온프레미스는 "내 집 지하실에 발전소를 짓는 것"이고, 클라우드는 "전 세계에 분산된 무한 전기 그리드에 플러그만 꽂으면 되는 것"입니다. 전기요금은 사용량(kWh)만큼만 청구되며, 정전 시 자동으로 백업 계통이 작동합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 NIST SP 800-145 기준으로 **배치 모델(Public/Private/Hybrid/Community)** 과 **서비스 모델(IaaS/PaaS/SaaS/FaaS)** 의 2차원 매트릭스로 분류된다. 기술사 관점에서는 이를 **"책임 분담 모델(Shared Responsibility Model)"** 과 **"5계층 참조 아키텍처"** 로 변환하여 심층 분석해야 한다.

### 5계층 클라우드 참조 아키텍처

```text
[클라우드 네이티브 5계층 아키텍처 및 핵심 컴포넌트 매핑]

  +----------------------------------------------------------------------------+
  |  Layer 5: Application / Workload                                          |
  |  +- Microservice (Spring Boot, Node.js, Go, Python FastAPI)               |
  |  +- Serverless Function (AWS Lambda, Azure Functions, GCP Cloud Functions) |
  |  +- SPA (React, Vue.js) + BFF (Backend for Frontend)                      |
  +----------------------------------------------------------------------------+
  |  Layer 4: API Gateway / Service Mesh                                      |
  |  +- API Gateway: Kong, AWS API Gateway, Apigee, Azure API Management       |
  |  +- Service Mesh: Istio, Linkerd, Consul Connect (Envoy Sidecar)          |
  |  +- 인증/인가: OAuth 2.0 + OIDC + JWT, mTLS (SPIFFE/SPIRE)                |
  +----------------------------------------------------------------------------+
  |  Layer 3: Orchestration & Runtime                                          |
  |  +- Kubernetes (K8s): Control Plane (etcd, kube-apiserver, scheduler)      |
  |  |                + Data Plane (kubelet, kube-proxy, container runtime)    |
  |  +- Container Runtime: containerd, CRI-O                                  |
  |  +- Package Manager: Helm, Kustomize, ArgoCD (GitOps)                     |
  +----------------------------------------------------------------------------+
  |  Layer 2: Compute Abstraction / Virtualization                             |
  |  +- VM: KVM, Xen, VMware ESXi, Hyper-V, AWS Nitro System                  |
  |  +- Container: Docker, Podman, OCI Runtime Spec                           |
  |  +- Serverless Platform: Firecracker microVM (Lambda), gVisor (Cloud Run)  |
  +----------------------------------------------------------------------------+
  |  Layer 1: Infrastructure (전역 인프라)                                     |
  |  +- Region / Availability Zone (AZ) / Edge Location / PoP                 |
  |  +- Global Network: AWS Backbone 100Gbps+, Private 5G, Cloud WAN           |
  |  +- Hardware: Graviton3 ARM, Nitro Enclave, TPU v5, GPU H100 InfiniBand    |
  +----------------------------------------------------------------------------+
```

| 계층 | 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- | :--- |
| **Layer 5** Application | 마이크로서비스 / Lambda | 비즈니스 로직 실행 | 12-Factor App 원칙(설정 외부화, 무상태성, 로그 STDOUT), Circuit Breaker(Hystrix, Resilience4j) |
| **Layer 4** API Gateway | Kong / Istio Ingress | 라우팅, 인증, Rate Limiting | L7 로드밸런싱(Envoy), OPA(Open Policy Agent) 정책 엔진, mTLS 종단 |
| **Layer 3** Orchestration | Kubernetes 1.30+ | 컨테이너 라이프사이클 관리 | 선언적 YAML + Reconciliation Loop, HPA/VPA/Cluster Autoscaler, PDB(Pod Disruption Budget) |
| **Layer 2** Runtime | Firecracker / containerd | 프로세스 격리 및 실행 | microVM(125ms 부팅, 5MB 메모리), cgroups v2, seccomp, AppArmor/SELinux |
| **Layer 1** Infrastructure | Region / AZ | 물리 데이터센터 추상화 | 100마일 이내 AZ 간 지연시간 < 2ms, 리전 간 비동기 복제(CRDT, S3 Cross-Region Replication) |
| **Cross-Cutting** Observability | Prometheus / OpenTelemetry | 통합 모니터링 | 3대 신호(Metrics/Logs/Traces), SLO/SLI/SLI 기반 에러버닝(Error Budget) |
| **Cross-Cutting** Security | IAM / KMS / Vault | Zero Trust 구현 | RBAC + ABAC, SPIFFE ID, HashiCorp Vault Dynamic Secrets (TTL 1시간 자동 회전) |

### 핵심 메커니즘: 제어 평면 vs 데이터 평면 분리

```text
[AWS VPC를 예시로 한 Control Plane vs Data Plane 동작 흐름]

   +--------------------------+                  +--------------------------+
   |      CONTROL PLANE       |                  |      DATA PLANE          |
   |   (느림, 일관성 중요)     |                  |   (빠름, 처리량 중요)     |
   |                          |                  |                          |
   |  +--------------------+  |   API Call       |  +--------------------+  |
   |  | AWS Management     |--+-----------------►|  | EC2 Instance       |  |
   |  | Console / SDK /    |  |  (Intent 기반)   |  | (실제 트래픽 처리)  |  |
   |  | Terraform          |  |                  |  |                    |  |
   |  +--------------------+  |                  |  +--------------------+  |
   |           |              |                  |           ^              |
   |           v              |                  |           |              |
   |  +--------------------+  |                  |  +--------------------+  |
   |  | API Server         |  |                  |  | Hyperplane         |  |
   |  | (최종적 일관성)     |  |                  |  | (AWS Nitro 기반    |  |
   |  | Quorum 기반 Raft   |  |                  |  |  고성능 패킷 처리) |  |
   |  +--------------------+  |                  |  +--------------------+  |
   |           |              |                  |           |              |
   |           v              |                  |           v              |
   |  +--------------------+  |                  |  +--------------------+  |
   |  | Distributed Store  |  |                  |  | Local SSD Cache    |  |
   |  | (etcd / Spanner /  |  |                  |  | + EBS gp3 / NVMe   |  |
   |  |  Aurora Storage)   |  |                  |  | (밀리초 IOPS)      |  |
   |  +--------------------+  |                  |  +--------------------+  |
   +--------------------------+                  +--------------------------+
                    |                                       |
                    +----- 상태 전파 (Eventual Consistency) -+
                              (수십 ms ~ 수 초 지연)
```

**클라우드 핵심 알고리즘 및 정량 파라미터**:
- **Consensus Algorithm**: etcd는 Raft 합의 알고리즘 사용, Leader Election Timeout 1~2초, Heartbeat 100ms, Quorum = N/2+1 (3-node 클러스터에서 2개 과반수)
- **Auto Scaling 수식**: `Desired = ceil(Current × (CurrentMetricValue / TargetMetricValue))` — 예: CPU 80% 목표, 현재 30% 인스턴스, 40% 사용률 -> `ceil(30 × 40/80) = 15대`로 축소
- **카나리 배포 트래픽 분할**: Istio VirtualService 1% -> 5% -> 25% -> 50% -> 100% 단계적 라우팅, 각 단계별 5~15분 관측
- **MapReduce 데이터 처리**: 100TB 데이터 정렬 시 Hadoop on EMR로 1,000 노드 × 8시간 -> Spark on Kubernetes로 200 노드 × 30분 단축
- **S3 Storage Class 계층화**: Standard($23/TB/월) -> IA($12.5) -> Glacier Instant($4) -> Glacier Flexible($3.6) -> Glacier Deep Archive($0.99) — 90일 미접근 시 IA로 자동 전환(Lifecycle Policy)

- **📢 섹션 요약 비유**: 제어 평면은 "항공 관제탑(명령과 상태 관리)"이고, 데이터 평면은 "실제 비행 중인 항공기(빠르게 승객/화물 운송)"입니다. 관제탑이 모든 비행기의 위치를 추적·명령하지만, 실제 이륙·착륙은 각 항공기가 자체적으로 수행합니다. 이 분리 덕분에 1개 관제탑이 10만 대 비행기를 동시에 관제할 수 있습니다.

---

## Ⅲ. 비교 및 연결

### 온프레미스 vs 퍼블릭 클라우드 vs 하이브리드

| 구분 | On-Premise | Public Cloud (AWS/Azure/GCP) | Hybrid (Outposts/Anthos/Azure Arc) |
| :--- | :--- | :--- | :--- |
| **투자 비용 (TCO)** | 초기 Capex 100억+, 5년 ROI 불확실 | Opex 종량제, 3년 TCO 30~50% 절감 | Capex+Opex 혼합, 클라우드 버스트로 20% 절감 |
| **확장성** | HW 조달 4~12주, 수직확장 한계 | 5분 내 1,000+ 인스턴스 자동 확장 | 평시 On-Prem + 피크 시 클라우드 버스트 |
| **가용성 SLA** | 자체 구축 99.9% (연 8.7시간 장애) | 99.99% (연 52분), 99.999% (Premium) | 클라우드 측 SLA + 자체 이중화 |
| **보안 통제** | 물리/논리 전수 통제, 컴플라이언스 유리 | CSP 책임분담, FedRAMP/ISO27001/PCI-DSS | 민감 데이터는 On-Prem, 일반 워크로드는 클라우드 |
| **운영 부담** | 24x7 NOC, IDC 냉각/전력 관리 | CSP가 패치/백업/DR 자동화 | 양쪽 모두 관리 필요, CloudOps 팀 필요 |
| **적합 시나리오** | 규제 금융 코어뱅킹, 국방, 극저지연 HFT | 웹/모바일, 빅데이터/AI, 글로벌 SaaS | 레거시 + 신규 시스템 공존, 단계적 전환 |
| **대표 기술** | VMware vSphere, OpenStack, Ceph | EKS/AKS/GKE, Lambda, S3, BigQuery | AWS Outposts, Azure Stack Hub, Anthos, Rancher |
| **마이그레이션 비용** | - | 6-Factor R(Rehost/Replatform/Refactor),
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 756 / 800

<- **이전**: [755. 클라우드 아키텍처 핵심 토픽 755번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/755_cloud_architecture_core_topic_755_exam_summar/)
**다음**: [757. 클라우드 아키텍처 핵심 토픽 757번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/757_cloud_architecture_core_topic_757_exam_summar/) ->

---
