---
title: "673. 클라우드 아키텍처 핵심 토픽 673번 시험 요약 (Cloud Architecture Core Topic 673 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 **Multi-Tenancy(다중 테넌시) + Elasticity(탄력성) + Pay-per-Use(사용량 과금)**라는 3대 속성을 기반으로, 온프레미스의 한계를 극복하기 위해 **추상화된 리소스 풀(Compute/Storage/Network 가상화)**을 API로 소비하는 컴퓨팅 패러다임이다.
> 2. **가치**: CapEx->OpEx 전환으로 초기 투자비 60~80% 절감, Auto Scaling을 통한 Peak-time 트래픽 10~100배 흡수, 다중 AZ·리전 기반 99.99% SLA(연간 52분 이내 장애) 보장, 글로벌 엣지 로케이션 활용 레이턴시 50~200ms 단축 효과를 제공한다.
> 3. **판단 포인트**: **제어권(Control) vs 편의성(Convenience)**, **단일 클라우드(Lock-in) vs 멀티 클라우드(복잡도)**, **강한 일관성(Strong Consistency) vs 가용성(AP)**, **Cold Start 지연 vs 비용 최적화** 등 4축의 Trade-off에서 아키텍처 결정이 분기된다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 아키텍처는 **예측 기반 용량 계획(Capacity Planning)**, **수직 확장(Scale-Up)의 물리적 한계**, **수동 프로비저닝(수일~수주 소요)**, **고정 비용 구조(CapEx)**라는 4대 병목으로 인해 급변하는 디지털 트래픽과 비즈니스 요구에 대응하지 못했다. 클라우드 아키텍처는 **가상화(Hypervisor/KVM/Xen) + 자동화(API/Infra as Code) + 분산 시스템(CAP Theorem 기반)** 기술을 융합하여, 리소스를 코드처럼 선언적으로 다루고 수요 변동에 따라 자동으로伸缩하는 **유틸리티 컴퓨팅(Utility Computing)** 모델을 실현한다.

```text
+--------------------------------------------------------------------+
|       [On-Premise]  ------- 디지털 전환 요구 -------->  [Cloud]      |
|                                                                    |
|  +--------------+                              +----------------+  |
|  | 전용 하드웨어|   ① 용량 계획 실패            |  가상화 풀     |  |
|  | (랙/서버/스토|   ② Provisioning 수동(수일)   | (EC2/VM)       |  |
|  |  리치)       |   ③ CapEx 과다 투자           |  Pay-per-Use   |  |
|  |  CapEx 중심  |   ④ 트래픽 Peak 유실          |  OpEx 중심     |  |
|  +--------------+                              +----------------+  |
|         |                                              |           |
|         v                                              v           |
|   +---------------+                            +--------------+   |
|   | 단일 장애점   |    <---- 아키텍처 패러다임---> |  Multi-AZ    |   |
|   | (SPOF)        |         시프트             |  Multi-Region|   |
|   +---------------+                            +--------------+   |
+--------------------------------------------------------------------+
  ⮕ AWS Well-Architected 5 Pillar + Azure CAF + GCP ACE 프레임워크 등장
```

클라우드 도입의 핵심 동기는 **비즈니스 민첩성(Time-to-Market 단축)**, **글로벌 확장성(Global Reach)**, **비용 최적화(FinOps)**, **이벤트 기반 워크로드(AI/ML/IoT/실시간 스트리밍) 처리**이며, 코로나19 이후 **원격 근무 인프라, D2C(Direct-to-Consumer) 트래픽 폭증, 생성형 AI 서비스** 수요와 맞물려 **클라우드 네이티브(Cloud-Native) + AI 워크로드 아키텍처**가 표준으로 자리잡았다.

- **📢 섹션 요약 비유**: 온프레미스는 **"각 가정의 자체 발전기(수동 연료 보충, 정전多)"**, 클라우드는 **"국가 전력망(자동 스케일링, 다중 화력/원자력, 실시간 복구)"**이다. 발전기容量을 직접 사지 않고, 사용한 만큼만 요금을 낸다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **5계층 스택(물리 인프라 -> 가상화 -> 오케스트레이션 -> 서비스 추상화 -> 워크로드)** 위에서 동작하며, 각 계층은 API·선언적 IaC(Terraform/CloudFormation)·관찰가능성(Observability) 도구로 연결된다.

```text
        +------------------------------------------------------+
        |   ⑤ Workload Layer (사용자 애플리케이션)              |
        |      Microservice / Serverless / ML Pipeline         |
        +------------------------------------------------------+
        |   ④ Service Abstraction Layer (관리형 서비스)         |
        |      DBaaS / MQSaaS / AIaaS / Observability         |
        +------------------------------------------------------+
        |   ③ Orchestration Layer (오케스트레이터)              |
        |      Kubernetes (EKS/AKS/GKE) + Service Mesh(Istio) |
        +------------------------------------------------------+
        |   ② Virtualization Layer (가상화/컨테이너)            |
        |      Hypervisor (KVM/Xen) + Container (cri-o/runc)   |
        +------------------------------------------------------+
        |   ① Physical Layer (물리 인프라)                      |
        |      Global DC + Edge POP + Software-Defined Network |
        +------------------------------------------------------+
              ⮕ 모든 계층이 API/SDK/IaC로 자동화(Programmable)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Region / Availability Zone (AZ)** | 지리적 격리 단위 / 데이터센터 클러스터 | 리전 간 독립, AZ 간 100km 이내 분리, 동기식 복제 가능 거리. 예: AWS `ap-northeast-2`(서울) + 4개 AZ |
| **Compute 가상화** | CPU/Memory/Network의 논리적 분리 | Type-1 Hypervisor(KVM, Xen, ESXi), MicroVM(Firecracker, gVisor)로 Cold Start 125ms 이하 구현 |
| **컨테이너 런타임** | OS 커널 공유 + 프로세스 격리 | OCI 표준, runc/containerd/cri-o, 이미지 레이어 캐싱으로 배포 속도 10배^ |
| **오케스트레이터 (K8s)** | 컨테이너 자동 배치·스케일·복구 | Control Plane(API Server/etcd/scheduler) + Node(Kubelet/Proxy), 선언적 ReplicaSet/Deployment |
| **오브젝트 스토리지 (S3 호환)** | HTTP 기반 무한 확장 저장 | **Erasure Coding(Reed-Solomon) + 3-AZ 동시 저장**, 11 9s(99.999999999%) 내구성 |
| **SDN (Software-Defined Network)** | 가상 라우터/스위치/방화벽 프로그래밍 | VPC(Virtual Private Cloud) + Subnet + Security Group, BGP Anycast + SDN 컨트롤러(ONOS/OpenDaylight) |
| **관리형 서비스 (PaaS)** | DB·MQ·AI·모니터링 추상화 | RDS Aurora(6-way 복제), Lambda(밀리초 과금), CloudWatch/Prometheus + Grafana, OpenTelemetry |
| **IaC (Infrastructure as Code)** | 인프라를 코드로 선언·버전관리 | Terraform(HCL 멀티클라우드), CloudFormation(AWS 전용), Pulumi(범용 언어), GitOps(ArgoCD/Flux) |

클라우드의 **핵심 동작 원리 4가지**를 반드시 이해해야 한다:
1. **Elasticity vs Scalability**: 수동 확장(Scalability) ↔ 자동 확장(Elasticity) — Auto Scaling Group이 CPU/Memory/Queue Depth 메트릭 기반 HPA/VPA/Cluster Autoscaler로 구현.
2. **Multi-Tenancy**: 하이퍼바이저 레벨 격리 + cgroup/namespace 컨테이너 격리 + IAM(RBAC) 논리 격리의 3중 보안 모델. **Noisy Neighbor 문제**를 NUMA-Aware Scheduling + SR-IOV로 완화.
3. **결정성(Consistency) 모델**: CAP Theorem -> AP(가용성 우선, DynamoDB/Cassandra) vs CP(일관성 우선, etcd/Consul) vs CA(전통 RDBMS). **최종 일관성(Eventual Consistency)**이 글로벌 분산의 기본.
4. **Pay-per-Use 과금**: 초 단위 컴퓨팅(Per-Second Billing), GB-월 단위 스토리지, IOPS/Throughput 별도 과금, **3가지 할인 모델**(On-Demand / Reserved Instances 40~60%v / Spot Instance 70~90%v).

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 5계층은 **"아파트 단지"**와 같다 — ① 토지·기반 시설(물리), ② 골조 구조(가상화), ③ 엘리베이터·배관 시스템(오케스트레이션), ④ 택배·경비·청소 서비스(관리형), ⑤ 입주자(워크로드). 입주자는 골조 걱정 없이 자신의 인테리어만 신경 쓰면 된다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처를 평가할 때 가장 빈번하게 등장하는 비교 축은 **서비스 모델(IaaS/PaaS/SaaS/FaaS)**과 **배포 모델(Public/Private/Hybrid/Multi/Community)**이며, 컴퓨팅 단위 선택(VM/Container/Serverless)은 워크로드 특성에 따라 결정된다.

| 구분 | **IaaS (EC2, Azure VM)** | **PaaS (Beanstalk, App Service)** | **SaaS (Office 365, Slack)** | **FaaS (Lambda, Cloud Functions)** |
| :--- | :--- | :--- | :--- | :--- |
| 관리 범위 | OS·Middleware·Runtime까지 사용자 관리 | App·Data만 관리, Platform은 CSP | 모두 CSP 관리, 설정만 사용자 | 코드(Function)만 관리, Event 기반 자동 실행 |
| 확장성 | 수동/Auto Scaling (분 단위) | Auto Scale (초~분 단위) | CSP가 자동 처리 | Sub-second Auto Scale, **0->수천 동시** |
| 과금 단위 | 인스턴스·시간 | 인스턴스·시간 + 관리형 서비스료 | 사용자·월 (Subscription) | 호출 수 + GB-초 (밀리초 과금) |
| 적용 사례 | 레거시 마이그레이션, 커스텀 네트워크 | 웹앱·API 표준 배포 | 이메일·CRM·협업툴 | 이미지 리사이즈, Webhook, IoT 이벤트 |
| Lock-in 위험 | 낮음 (Lift & Shift 가능) | 중간 | 높음 | 매우 높음 (벤더 특화 트리거) |

| 구분 | **VM (가상머신)** | **Container (Docker)** | **Serverless (FaaS)** |
| :--- | :--- | :--- | :--- |
| 부팅 시간 | 30초~수 분 | 100~500ms | 1~100ms (Warm), 100~500ms (Cold Start) |
| 밀도 (호스트당) | 10~50대 | 100~500개 | 수천 Function |
| 격리 수준 | 하드웨어 가상화(HW Isolation) | 프로세스 격리(커널 공유) | MicroVM/네임스페이스 |
| Stateful 지원 | ✅ 강함 | ⚠️ PV/PVC 필요 | ❌ 원칙적 Stateless |
| 적합 워크로드 | DB·ERP·레거시 | MSA·CI/CD | 이벤트·단순 API·ETL |

**다른 시스템과의 연결**:
- **DevOps 파이프라인**: Git -> Jenkins/GitHub Actions -> Container Registry(ECR/ACR) -> Helm/Kustomize -> ArgoCD GitOps -> K8s/Serverless
- **AI/ML 워크로드**: SageMaker/Vertex AI + GPU Pool(A100/H100) + Vector DB(Pinecone/Milvus) + LLM Serving(vLLM/Triton)
- **레거시 통합**: Strangler Fig Pattern으로 API Gateway(Kong/AWS API GW) + Adapter MSA로 단계적 이관
- **보안 연계**: CSPM(Cloud Security Posture Management, Wiz/Prisma) + CWPP(Workload Protection) + IAM Federation(SAML/OIDC SSO) + KMS HSM 기반 BYOK

- **📢 섹션 요약 비유**: IaaS는 **"렌탈 아파트(빈집, 인테리어 자유)"**, PaaS는 **"서비스드 아파트(가전·가구 포함)"**, SaaS는 **"호텔(다 갖춰진, 짐만 풀면 됨)"**, FaaS는 **"택배 보관함(불러야 작동, 안 쓰면 비용 0)"**이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

클라우드 아키텍처 설계는 **요구사항(비기능: 가용성/확장성/보안) -> Well-Architected 5 Pillar 평가 -> CSP 선정 -> PoC -> 마이그레이션 -> 운영 최적화(FinOps)** 순서로 진행된다. 기술사 시험은 **6R 전략(Rehost/Replatform/Refactor/Rehire/Retain/Retire)**의 적절한 조합, **CAP Trade-off** 명시, **DR 전략(RPO/RTO 정의)**를 요구한다.

### 기술사형 판단 체크리스트

1. **워크로드 분류를 수행했는가?** — OLTP(낮은 지연, 강한 일관성) vs OLAP(배치, 약한 일관성) vs Streaming(Kafka/Kinesis) vs AI/ML(GPU) vs Batch(MapReduce)별로 적합한 서비스 매핑(예: OLTP->Aurora, OLAP->Redshift/BigQuery, Streaming->Flink/KDA, ML->SageMaker/Vertex AI)을 제시했는가?
2. **가용성 목표 수치와 비용을 Trade-off 분석했는가?** — 99.9%(연 8.7시간 장애) vs 99.99%(52분, Multi-AZ 필수) vs 99.999%(5분, Multi-Region Active-Active)별 아키텍처·비용 차이(예: 99.99%는 단일 리전 Multi-AZ, 99.999%는 Global Aurora + Route53 Latency-Based Routing)를 명시했는
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 673 / 800

<- **이전**: [672. 클라우드 아키텍처 핵심 토픽 672번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/672_cloud_architecture_core_topic_672_exam_summar/)
**다음**: [674. 클라우드 아키텍처 핵심 토픽 674번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/674_cloud_architecture_core_topic_674_exam_summar/) ->

---
