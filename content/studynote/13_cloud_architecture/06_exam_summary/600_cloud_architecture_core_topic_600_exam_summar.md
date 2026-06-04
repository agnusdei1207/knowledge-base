---
title: "600. 클라우드 아키텍처 핵심 토픽 600번 시험 요약 (Cloud Architecture Core Topic 600 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST 참조모델(IaaS/PaaS/SaaS/FaaS)을 기반으로 컨테이너 오케스트레이션(Kubernetes), 인프라 코드화(Terraform/IaC), 메시 네트워킹(Istio/Service Mesh), 그리고 셀프서비스 셀링 API를 결합해 **탄력성(Elasticity)**, **가용성(HA)**, **비용 최적화(FinOps)** 를 동시 달성하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: AWS Auto Scaling + Spot Instance 조합으로 동일 워크로드 대비 60~70% TCO 절감, Multi-AZ/EKS 기반 99.99% SLA, CI/CD 파이프라인을 통한 배포 주기 단축(주 1회 -> 일 10회 이상, DORA Elite 지표 달성)이 가능하며, MTTR 90% 이상 감소 사례가 다수 보고된다.
> 3. **판단 포인트**: **Lift & Shift vs Replatform vs Refactor** 중 어느 마이그레이션 전략을 채택할지, **단일 클라우드 종속(Vendor Lock-in) vs 멀티/하이브리드**, **모놀리식 -> 마이크로서비스 -> 서버리스**의 분해 수준, 그리고 **EKS vs AKS vs GKE** 간 컨트롤 플레인 관리 모델 차이를 워크로드 특성(상태 유무, 트래픽 패턴, 데이터 중력)에 따라 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 데이터센터는 **수요 예측 기반 과잉 용량 프로비저닝(Over-provisioning)**, **수직 확장(Scale-up) 한계**, **캡엎(CapEx) 편중**, **배포 주기 수개월**, **장애 복구 시간 RTO 수시간~수일**이라는 구조적 한계를 갖는다. 클라우드 아키텍처는 이를 **탄력적 자원 풀링(Elastic Resource Pool)**, **수평 확장(Scale-out)**, **사용량 기반 OpEx 전환**, **불변 인프라(Immutable Infrastructure)**, **셀프서비스 API**로 전환하여 비즈니스 민첩성(Agility)과 운영 효율성을 동시에 확보한다.

```text
+---------------------------------------------------------------------+
|          전통 On-Premise  --->  Cloud-Native 전환 패러다임            |
+---------------------------------------------------------------------+
|                                                                     |
|  [Before] On-Premise                   [After] Cloud-Native         |
|  +-------------------+                 +-----------------------+    |
|  |  전용 HW (3yr ROI) |                 |  API 호출형 임시 자원  |    |
|  |  고정 Capacity      |    --->         |  Auto-Scale (sec~min) |    |
|  |  수동 배포/CM       |                 |  GitOps 자동 배포     |    |
|  |  수평확장 어려움     |                 |  K8s HPA/VPA/Cluster  |    |
|  |  DR Site 별도 구축  |                 |  Multi-AZ 기본 내장  |    |
|  |  TTM: 6~12개월     |                 |  TTM: 1~4주           |    |
|  +-------------------+                 +-----------------------+    |
|                                                                     |
|  비용 모델: CapEx 100%             비용 모델: OpEx 80% + CapEx 20%  |
|  장애 대응: MTTR 평균 4h          장애 대응: MTTR 평균 15min        |
|  가용성: 99.9% (Single DC)        가용성: 99.99% (Multi-AZ/Region)  |
+---------------------------------------------------------------------+
```

클라우드 도입의 **기술적 필요성**은 다음 4가지 축으로 요약된다:

1. **탄력성(Elasticity)**: 트래픽 변동성에 맞춘 자동 스케일링(예: EKS HPA가 CPU 70% 임계치로 5분 내 Pod 10->100개 증설)
2. **글로벌 도달성(Global Reach)**: AWS 33개 리전/105개 AZ, Azure 60+ 리전을 활용한 엣지 배치로 P99 레이턴시 50%v
3. **서비스 카탈로그(Self-Service)**: 200+ 매니지드 서비스(RDS, Lambda, S3, EKS)로 운영 부담 외부화
4. **거버넌스 자동화**: CSPM(Cloud Security Posture Management), IaC Policy-as-Code(OPA, Sentinel)로 컴플라이언스 코드화

- **📢 섹션 요약 비유**: 기존 온프레미스는 마치 **"정원용 정수기"** 처럼 사용량과 무관하게 큰 용량을 사두고 정체되는 반면, 클라우드는 **"수도꼭지"** 처럼 필요할 때 즉시 필요한 만큼 받아 쓰고 안 쓰면 잠그는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 **4계층 참조모델**은 다음과 같이 구성된다. 각 계층은 독립적 책임을 가지며, API/Contract로 결합된다.

```text
+-------------------------------------------------------------------------+
|                     Cloud-Native 4-Layer Reference Model                 |
+-------------------------------------------------------------------------+
|                                                                         |
|  +-----------------------------------------------------------------+    |
|  | L4. Application & Workload Layer (Stateless Microservice)       |    |
|  |  +-----+ +-----+ +-----+ +-----+   Spring Boot / Quarkus /     |    |
|  |  | Pod | | Pod | | Pod | | Pod |   Go(gin) / Node.js            |    |
|  |  +--+--+ +--+--+ +--+--+ +--+--+   12-Factor App 원칙 적용      |    |
|  |     +------+-------+------+----+                                |    |
|  |                    Service Mesh (Istio/Linkerd)                 |    |
|  |                    mTLS, Traffic Mgmt, Telemetry                 |    |
|  +-----------------------------+-----------------------------------+    |
|                                | gRPC/HTTP                             |
|  +-----------------------------v-----------------------------------+    |
|  | L3. Orchestration & Scheduling Layer (K8s Control Plane)       |    |
|  |  +--------------+  +--------------+  +--------------+         |    |
|  |  | API Server   |  |  Scheduler   |  | Controller   |         |    |
|  |  | (etcd 백엔드) |  | (Bin-packing)|  | Manager      |         |    |
|  |  +--------------+  +--------------+  +--------------+         |    |
|  |  HPA / VPA / KEDA / Karpenter (오토스케일링)                   |    |
|  |  ArgoCD / Flux (GitOps)                                       |    |
|  +-----------------------------+-----------------------------------+    |
|                                | CNI/CSI/CRI                            |
|  +-----------------------------v-----------------------------------+    |
|  | L2. Platform & Runtime Layer (Container + OS)                  |    |
|  |  +----------+  +----------+  +----------+  +----------+        |    |
|  |  |  EKS     |  |  AKS     |  |  GKE     |  |  Self-K8s|        |    |
|  |  |(managed) |  |(managed) |  |(autopilot)| |(kubeadm) |        |    |
|  |  +----------+  +----------+  +----------+  +----------+        |    |
|  |  Bottlerocket / Flatcar Linux (경량 OS)                        |    |
|  |  containerd / CRI-O                                           |    |
|  +-----------------------------+-----------------------------------+    |
|                                | Cloud SDK/ECM/ARM                     |
|  +-----------------------------v-----------------------------------+    |
|  | L1. Infrastructure & Provisioning Layer (IaC + Cloud API)      |    |
|  |  +----------+  +----------+  +----------+  +----------+        |    |
|  |  | Terraform|  | Pulumi   |  | CDK      |  | Crossplane|       |    |
|  |  |(HCL)     |  |(Python/TS)| |(TypeScript)| |(K8s native)|       |    |
|  |  +----------+  +----------+  +----------+  +----------+        |    |
|  |  VPC/Subnet/IGW/NAT/EKS/RDS/S3/CloudFront 선언적 프로비저닝   |    |
|  +-----------------------------------------------------------------+    |
|                                                                         |
|  Cross-Cutting: Observability(Prom/Grafana/Loki/Tempo)                 |
|                 Security(IAM/OAuth/OIDC/Vault/SIEM)                    |
|                 Cost(FinOps/CUR/Kubecost)                              |
+-------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **L1. IaC 엔진** | 인프라 선언적 프로비저닝 및 Drift Detection | Terraform은 HCL로 선언 -> `plan/apply` 2단계, 상태파일(`tfstate`)을 S3+DynamoDB Lock으로 원자성 보장. Pulumi는 일반 언어(TS/Python) 사용으로 SDK 통합 용이. Crossplane은 K8s CRD로 클라우드 리소스 관리(Control Plane 패턴) |
| **L2. 컨테이너 런타임** | 애플리케이션 격리 실행 및 리소스 격리(cgroups) | containerd는 CRI(Container Runtime Interface) 표준으로 Kubelet과 통신. gVison/Kata는 보안 샌드박스, Firecracker는 microVM 기반 함수 실행(1ms cold start) |
| **L3. 오케스트레이터** | 컨테이너 스케줄링, 자기치유, 선언적 상태 관리 | K8s Control Plane(etcd 합의 알고리즘 Raft 기반)이 desired state ↔ actual state를 `Reconcile Loop`로 지속 비교. HPA는 `metrics-server`로부터 15초 단위 메트릭 수집 후 `targetMetricValue` 도달 시 Pod 증설. Karpenter는 노드 프로비저닝 시간을 5분->1분으로 단축 |
| **L4. 애플리케이션** | 비즈니스 로직 실행, 무상태(Stateless) 원칙 | 12-Factor App: Config는 환경변수, Backing Service는 URL 추상화, Disposability(빠른 기동/종료), Dev/Prod Parity. Spring Cloud, Dapr 등으로 분산 트랜잭션(Saga) 처리 |
| **Cross-Cutting 관측성** | 로그/메트릭/트레이스 통합 수집 | OpenTelemetry SDK -> OTLP -> Tempo/Jaeger(Trace) + Prometheus(Metric) + Loki(Log). SLO/Error Budget 기반 알람 |
| **Cross-Cutting 보안** | Zero Trust, IAM, Secret 관리 | SPIFFE/SPIRE로 워크로드 Identity 발급, Vault로 동적 Secret(TTL 1시간), IAM Role for Service Accounts(IRSA)로 Pod 단위 최소권한 |
| **Cross-Cutting 비용** | FinOps, Rightsizing, Reserved/Spot 혼합 | Compute Optimizer 권고 기반 인스턴스 타입 다운사이징, Savings Plan(1~3년 약정 30~60%v), Spot Instance(70~90%v, Interrupt 허용 워크로드 한정), Kubecost로 네임스페이스별 비용 귀속 |

**핵심 알고리즘 및 원리 심화:**

- **K8s 스케줄러의 Bin-Packing**: `LeastAllocated`(리소스 여유 많은 노드 우선) vs `MostAllocated`(집중 배치로 노드 수 절감, FinOps 친화) vs `RequestedToCapacityRatio` (가중치 기반) 전략이 존재하며, K8s 1.22+부터 **Scheduling Framework**가 Pluggable Plugin 구조로 확장성을 제공
- **CAP 이론의 클라우드 적용**: AWS DynamoDB는 **AP 시스템**(가용성 우선, 결과적 일관성), Google Spanner는 **CP 시스템**(전역 강한 일관성, TrueTime API 기반). 기술사 논술에서 "일관성 모델 선택"은 빈출 주제
- **CQRS + Event Sourcing 패턴**: 쓰기/읽기 모델 분리, Kafka 이벤트 스트림을 통해 도메인 이벤트를 Materialized View에投影. 이벤트 순서 보장을 위해 Kafka Partition Key + Offset 사용

- **📢 섹션 요약 비유**: 클라우드 아키텍처 4계층은 **"자동화 식당 주방"** 과 같다. 손님 주문(L4 Application) -> 주방장(L3 Orchestration)이 코스 요리 순서 결정 -> 화덕(L2 Runtime)에서 실제 조리 -> 식재료 창고(L1 Infra)는 매니저(IaC)가 자동 발주한다. 모든 단계가 **레시피(IaC 선언)와 영수증(Observability)** 으로 추적 가능하다.

---

## Ⅲ. 비교 및 연결

### 1. 마이그레이션 전략 6R 비교 (AWS Well-Architected Framework)

| 구분 | Rehost (Lift&Shift) | Replatform | Refactor (Re-architect) | Repurchase (SaaS) | Retire | Retain |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **변경 범위** | 코드 변경 없음 | 최소 변경(Managed 전환) | 클라우드 네이티브 재설계 | 상용 SaaS 교체 | 폐기 | 온프레미스 유지 |
| **소요 기간** | 1~3개월 | 3~6개월 | 6~18개월 | 1~2개월 | 즉시 | - |
| **TCO 효과** | CapEx->OpEx 전환(20~30%v) | 30~50%v | 50~70%v | 40~60%v | - | - |
| **리스크** | 기존 기술부채 이전 | 중간 | 높음(재설계) | 벤더 종속 | 낮음 | - |
| **적용 대상** | Legacy ERP, Mainframe, 배치 | DB->RDS, MQ->SQS, Tomcat->Beanstalk | 모놀리식->MSA, RDBMS->DynamoDB | CRM->Salesforce, HR->Workday | 미사용 자산 | 규제/보안 요건 |
| **대표 사례** | Velostrata, AWS SMS | RDS Proxy, ElastiCache 도입 | Strangler Fig Pattern | SaaS 전환 | - | - |

### 2. 오케스트레이션 플랫폼 비교 (EKS vs AKS vs GKE vs OpenShift)

| 구분 | Amazon EKS | Azure AKS | Google GKE (Autopilot) | Red Hat OpenShift |
| :--- | :--- | :--- | :--- | :--- |
| **Control Plane 관리** | AWS 완전 관리($0.10/hr) | Azure 완전 관리(무료) | GCP 완전 관리(무료) | 고객/IaaS 모두 선택 |
| **노드 OS** | Amazon Linux 2, Bottlerocket | Ubuntu, Azure Linux | COS(Container-Optimized OS) | RHCOS(Immutable) |
| **네트워크 CNI** | AWS VPC CNI(파드별 ENI) | Azure CNI Overlay(2022+) | GKE Dataplane V2(eBPF) | OVN-Kubernetes |
| **통합 서비스** | IAM/IRSA, ALB Controller, Karp
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 600 / 800

<- **이전**: [599. 클라우드 아키텍처 핵심 토픽 599번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/599_cloud_architecture_core_topic_599_exam_summar/)
**다음**: [601. 클라우드 아키텍처 핵심 토픽 601번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/601_cloud_architecture_core_topic_601_exam_summar/) ->

---
