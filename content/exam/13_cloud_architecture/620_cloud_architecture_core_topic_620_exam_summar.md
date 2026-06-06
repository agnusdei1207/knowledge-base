---
title: "Cloud Architecture Core Topic 620 Exam Summary"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 온프레미스 모놀리식 자원의 수직 확장(Scale-Up) 한계를 컨테이너 오케스트레이션(Kubernetes), 선언형 API(IaC), 분산 시스템 패턴(MSA, Event-Driven, CQRS, SAGA)을 통해 **탄력성(Elasticity)·가용성(High Availability)·무중단 배포(Zero-Downtime Deployment)**로 전환하는 시스템 설계 패러다임이다.
> 2. **가치**: AWS/Azure/GCP 기준 적절한 Well-Architected Framework 적용 시 **TCO 30~70% 절감, SLA 99.99%(Four-Nines) 달성, 배포 주기(DORA Lead Time) 2,000% 단축, MTTR 90% 감소** 등 정량적 가치를 제공하며, CAPEX를 OPEX로 전환하여 비즈니스 민첩성(Business Agility)을 확보한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **일관성 vs 가용성(CAP Theorem)**, **밀결합(Monolith) vs 느슨결합(Microservices)**, **다중 리전 비용 vs 재해복구 RPO/RTO** 사이의 균형이며, 워크로드 특성(Stateless/Stateful, Latency-Sensitive/Batch)에 따라 동기/비동기 통신, 캐시 전략, 데이터 분할(Sharding/Partitioning) 방식을 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

클라우드 아키텍처는 2006년 AWS S3/EC2 출시 이후 **가상화(Hypervisor -> Container) -> 오케스트레이션 -> 서버리스/엣지**로 발전해 왔다. 4차 산업혁명 시대를 맞아 트래픽 폭증, 데이터 양의 기하급수적 증가(2025년 전 세계 데이터 175ZB 전망), AI/ML 워크로드의 GPU 자원 요구, COVID-19 이후의 디지털 트랜스포메이션 가속화로 인해 기존 온프레미스 IDC 환경은 다음과 같은 한계에 직면했다.

- **자원 프로비저닝 리드타임**: 물리 서버 도입 4~12주 vs 클라우드 VM/EC2 90초
- **탄력성 부재**: 피크 트래픽 10배 증가 시 Scale-Out 불가능 -> 서비스 장애
- **TCO 비대화**: 유휴 자원 60~70%, 수동 운영으로 운영비(OPEX) 지속 증가
- **글로벌 확장성 한계**: 단일 리전/단일 데이터센터의 지리적 제약

클라우드 아키텍처는 **인프라抽象화(Infrastructure Abstraction)**, **API 기반 자동화**, **셀프서비스 프로비저닝**, **사용량 기반 과금(Pay-per-Use)**을 통해 이를 해결한다. NIST SP 800-145는 클라우드를 5대 필수 특성(On-Demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)과 3대 서비스 모델(IaaS/PaaS/SaaS), 4대 배포 모델(Public/Private/Hybrid/Community)로 정의한다.

```text
[클라우드 아키텍처 진화 패러다임 비교]

 온프레미스 시대 (1990~2005)        ->    클라우드 네이티브 시대 (2020~현재)
 +-------------------------+            +------------------------------+
 | 물리 서버 -> VM (Hypervisor) |       |  Bare-Metal -> Container      |
 | 수직확장 (Scale-Up)        |            |  수평확장 (Scale-Out)          |
 | 수동 배포 (FTP, Rsync)     |            |  GitOps + ArgoCD/Flux         |
 | 모놀리식 (Monolith)         |            |  Microservices / Serverless   |
 | 수동 용량 계획 (Capacity)   |            |  Auto-Scaling (HPA/VPA/CA)    |
 | HW 장애 대응 (DR Site)     |            |  Multi-AZ / Multi-Region Active|
 | 연간 CAPEX 100% 선지불      |            |  사용량 기반 OPEX (초단위 과금) |
 +-------------------------+            +------------------------------+
              v                                       v
       [CapEx 중심, 경직성]                  [OpEx 중심, 유연성·민첩성]
              v                                       v
       +-------------------------------------------------------------+
       |       DevOps + SRE + Platform Engineering 통합              |
       |   (CICD + Observability + IaC + Service Mesh + Security)    |
       +-------------------------------------------------------------+
```

추가로, 클라우드 네이티브 12-Factor App(Heroku 2011), CNCF(Cloud Native Computing Foundation) 정의, AWS Well-Architected Framework 5대 기둥(Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization)이 현대 클라우드 아키텍처 설계의 기준선(Baseline)으로 자리잡았다. 마이크로서비스 아키텍처(MSA) 도입 후 서비스 간 통신 지연(Latency), 분산 트랜잭션(2PC 불가 -> SAGA/CQRS), 데이터 일관성(Eventual Consistency), 운영 복잡도(Observability, Distributed Tracing)의 새로운 도전이 등장했으며, 이를 해결하기 위해 Istio/Linkerd 같은 Service Mesh, Jaeger/Tempo 같은 Tracing, Prometheus/Grafana 같은 Monitoring이 필수 요소로 등장했다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **"전기 발전소의 등장과 같다"**. 과거에는 각 가정/공장이 자체 발전기(발전기 = 자체 서버)를 돌렸지만, 클라우드는 중앙 대규모 발전소(공유 자원 풀)에서 전기를 끌어다 쓰는 **"Utility Computing"**으로, 필요할 때 켜고(Scale-Out) 필요 없으면 끄는(Scale-In) **Pay-per-Use 요금제**로 운영된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심 계층은 **물리/가상화 계층 -> 네트워킹/스토리지 계층 -> 컴퓨트/컨테이너 계층 -> 오케스트레이션 계층 -> 애플리케이션/데이터 계층 -> 관측/Observability 계층**으로 구성된다. 각 계층은 명확한 책임 분리를 가지며, API를 통해 느슨하게 결합(Loose Coupling)된다.

```text
[클라우드 네이티브 아키텍처 7계층 참조모델 (CN-RM)]

 +--------------------------------------------------------------------+
 |  ⑦ Observability & Governance                                    |
 |     Prometheus + Grafana + Loki + Jaeger + OPA (Policy)          |
 |     SLO/SLI/SLI 기반 SRE, FinOps                                  |
 +--------------------------------------------------------------------+
 |  ⑥ Application & Data Layer                                      |
 |     Microservices (Spring Boot/Go/Rust) + API Gateway (Kong)     |
 |     Event Streaming (Kafka/Kinesis), Cache (Redis/Memcached)     |
 |     DB: RDB (Aurora/CloudSQL) + NoSQL (DynamoDB/Cassandra)       |
 +--------------------------------------------------------------------+
 |  ⑤ Service Mesh & API Gateway                                    |
 |     Istio (Envoy Sidecar), Linkerd, mTLS, Traffic Management     |
 |     Circuit Breaker (Resilience4j, Hystrix legacy), Retry/Timeout|
 +--------------------------------------------------------------------+
 |  ④ Orchestration & Scheduling                                    |
 |     Kubernetes (K8s) + Helm + Kustomize                          |
 |     Operator Pattern (CRD), GitOps (ArgoCD/Flux)                 |
 +--------------------------------------------------------------------+
 |  ③ Container Runtime                                             |
 |     Docker / containerd / CRI-O / Podman                          |
 |     Image Registry: ECR, GCR, Harbor, Quay                        |
 +--------------------------------------------------------------------+
 |  ② Virtualization & Bare-Metal                                   |
 |     KVM, Xen (Hypervisor) -> Firecracker (MicroVM), gVisor        |
 |     Bare-Metal: AWS Nitro, Azure Confidential Compute            |
 +--------------------------------------------------------------------+
 |  ① Physical Infrastructure (Global Footprint)                    |
 |     Region -> AZ (Availability Zone) -> Edge Location / PoP        |
 |     Cross-Region PrivateLink / VPC Peering / Transit Gateway      |
 +--------------------------------------------------------------------+

 [클라우드 핵심 구성요소 동작 흐름 (요청 처리 시퀀스)]
 Client -> CDN(CloudFront) -> WAF/DDoS Shield -> ALB(Load Balancer)
   -> Ingress Controller (K8s) -> Service Mesh (mTLS)
   -> Microservice Pod (Sidecar Envoy)
   -> Cache (Redis) -> DB (Primary)
   -> Async Event (Kafka) -> Worker Pod -> S3/Object Storage
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Region / AZ** | 지리적 격리 단위 | Region(≥2 AZ), AZ(≥1 DataCenter, 독립 전력/네트워크). **AWS S3 11 9's, EC2 99.99% SLA**는 Multi-AZ 기반 |
| **컴퓨트 서비스** | 가상 서버/컨테이너/함수 제공 | EC2/Bare-Metal(AWS), VM Scale Set(Azure), GCE(GCP), Lambda/Functions(서버리스, 콜드스타트 100~300ms) |
| **스토리지 서비스** | 데이터 영속성 | Block(EBS, iSCSI), File(EFS, NFS, SMB), Object(S3, Azure Blob - 11 9's 내구성), Cold(Glacier - $0.004/GB/월) |
| **네트워크** | L4/L7 라우팅·격리 | VPC(Virtual Private Cloud), Subnet(Public/Private), SG/NACL(Stateless/Stateful FW), Transit GW(Hub-Spoke), PrivateLink(사설 연결) |
| **오케스트레이션 (K8s)** | 컨테이너 자동 배치·스케일·복구 | Control Plane(API Server, etcd, Scheduler, Controller Manager) + Worker Node(kubelet, kube-proxy, CNI). **HPA(CPU 70%)/VPA(메모리)/Cluster Autoscaler**(노드 추가) |
| **IaC (Infrastructure as Code)** | 인프라 선언적 정의·버전관리 | Terraform(HCL 멀티클라우드), AWS CDK(TypeScript/Python), Pulumi, Ansible(설정관리), Crossplane(K8s 기반 IaC) |
| **관측성 (Observability)** | 로그·메트릭·트레이스 통합 수집 | **Prometheus**(Metrics pull-based, PromQL) + **Grafana**(시각화), **Loki/ELK**(Log aggregation), **Jaeger/Tempo**(Distributed Tracing, OpenTelemetry 표준) |
| **보안·거버넌스** | ID/접근/암호화/컴플라이언스 | IAM(RBAC/ABAC), KMS/HSM(Envelope Encryption), Secrets Manager(Vault), SOC2/ISO27001/PCI-DSS/GDPR, CSPM(Cloud Security Posture Mgmt) |

**핵심 알고리즘·원리 심화**:

1. **분산 합의 알고리즘 (CAP Theorem 대응)**: etcd/Consul은 **Raft Consensus Algorithm** 사용. Leader Election + Log Replication + Safety 보장. CP 시스템(Eventual Consistency 불가), `etcd` 쓰기 latency 10ms p99.
2. **Auto-Scaling 의사결정**: KEDA(K8s Event-Driven Autoscaling) + K8s HPA는 `desiredReplicas = ceil[currentReplicas * (currentMetricValue / desiredMetricValue)]` 공식 사용. AWS Target Tracking Scaling은 `TargetValue=70%, Scale-Out Cooldown=60s, Scale-In Cooldown=300s`로 핑퐁 방지.
3. **Consistent Hashing (분산 캐시·DB)**: DynamoDB/Cassandra는 **Virtual Node(128~256개/물리노드)** + Consistent Hash Ring. 키 -> MD5/SHA-1 -> Ring -> 시계방향 첫 노드. 리밸런싱 시 **k/n 키만 이동**(n=노드 수).
4. **SAGA Pattern (분산 트랜잭션)**: 2PC(블로킹, Two-Phase Commit) 회피. **Orchestration SAGA**(중앙 Orchestrator) 또는 **Choreography SAGA**(이벤트 기반). 보상 트랜잭션(Compensating Transaction)으로 ACID -> BASE 모델 전환.
5. **CQRS + Event Sourcing**: 쓰기(Write)와 읽기(Read) 모델 분리. 이벤트 스토어(Apache Kafka, EventStoreDB)에 모든 상태 변경을 append-only로 저장 -> 시간여행 디버깅(Temporal Query) 가능.

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 7계층은 마치 **"고층 빌딩의 설비 시스템"**과 같다. ①~②층은 **토대/골조(물리 인프라)**, ③~④층은 **엘리베이터 시스템(컨테이너·오케스트레이션)**, ⑤층은 **로비 안내 시스템(Service Mesh)**, ⑥층은 **실제 사무실(애플리케이션)**, ⑦층은 **CCTV·방재 시스템(관측성)**이다. 빌딩 관리 시스템(API) 한 곳에서 모든 층을 통합 제어한다.

---

## Ⅲ. 비교 및 연결

### 1. 클라우드 컴퓨팅 핵심 분류 비교

| 구분 | **IaaS (Infrastructure-as-a-Service)** | **PaaS (Platform-as-a-Service)** | **SaaS (Software-as-a-Service)** | **FaaS (Function-as-a-Service)** |
| :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | OS 미들웨어 이상 사용자 관리 | Runtime/Middleware까지 CSP 관리 | 애플리케이션 전체 CSP 제공 | 코드만 작성, CSP가 전체 관리 |
| **예시 기술** | AWS EC2, Azure VM, GCE, Bare-Metal | AWS Elastic Beanstalk, App Engine, Heroku, OpenShift | Salesforce, Office 365, Slack, Notion, SAP S/4HANA | AWS Lambda, Azure Functions, GCP Cloud Functions |
| **확장 단위** | VM/Instance (수 분 소요) | Application/Container (수 분) | 사용자 단위 (즉시) | 함수 호출 단위 (밀리초) |
| **과금 모델** | 시간당 (per-second billing) | 인스턴스 시간/요청 수 | 사용자당/월 (per-seat) | 호출 수 + 실행 시간 (GB-Second) |
| **제어 수준** | ★★★★★ (최대) | ★★★☆☆ | ★☆☆☆☆ (최소) | ★★☆☆☆ |
| **적합 워크로드** | 레거시 이전, 커스텀 인프라 | 웹앱 API, 빠른 프로토타이핑 | 일반 비즈니스 업무 | 이벤트 기반 단기 작업, ETL, Webhook |
| **콜드 스타트** | N/A (항상 실행) | N/A (상시) | N/A | 100ms ~ 수 초 (SnapStart로 완화) |
| **최대 실행 시간** | 무제한 | 무제한 (또는 24h) | 무제한 | 15분 (Lambda 한계) |
| **책임 공유 모델** | 고객: OS^ / CSP: HWv | 고객: App/Data / CSP: 그 외 | 고객: Data·접근권한만 | 고객: 코드만 |

### 2. 배포 모델 비교

| 구분 | **Public Cloud** | **Private Cloud** | **Hybrid Cloud** | **Multi-Cloud**
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 620 / 800

<- **이전**: [619. 클라우드 아키텍처 핵심 토픽 619번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/619_cloud_architecture_core_topic_619_exam_summar/)
**다음**: [621. 클라우드 아키텍처 핵심 토픽 621번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/621_cloud_architecture_core_topic_621_exam_summar/) ->

---
