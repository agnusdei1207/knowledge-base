---
title: "Cloud Architecture Core Topic 734 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST SP 500-292 참조 모델 기반의 **탄력적(Elastic) 자원 풀**, **서비스 지향 추상화(IaaS/PaaS/SaaS/FaaS)**, **API·테넌트·셀프프로비저닝 3대 핵심 특성**을 통해 컴퓨팅 자원을 `pay-per-use` 소비 모델로 제공하는 분산 시스템 아키텍처임.
> 2. **가치**: CAPEX->OPEX 전환, Auto Scaling을 통한 **트래픽 100배 변동 대응**(ex. 쿠팡 윙·블랙프라이데이), 글로벌 리전 기반 RTO 분 단위 / RPO 0, 신규 서비스 배포 시간 90% 단축(Traditional 6개월 -> IaC 2주).
> 3. **판단 포인트**: **워크로드 특성 기반 배포 모델 선택**(Public/Hybrid/Private), 6R 전략 중 어느 마이그레이션 경로, 멀티클라우드 vs 싱글 하이퍼스케일러, Well-Architected 6대 필러(운영 우수성·보안·안정성·성능효율·비용최적화·지속가능성)별 Trade-off.

---

## Ⅰ. 개요 및 필요성

클라우드 컴퓨팅은 2006년 AWS S3와 EC2 출시 이후 **NIA(National Institute of Standards and Technology) SP 500-292** 표준을 거쳐, 2024년 기준 글로벌 퍼블릭 클라우드 시장이 약 **$679B**(한국 약 12조 원 규모)으로 성장한 IT 패러다임의 핵심축임. 이는 단순한 서버 외주가 아닌, **가상화(KVM/Xen) -> 컨테이너화(Docker) -> 오케스트레이션(Kubernetes) -> 서버리스(Lambda/Cloud Functions)**로 이어지는 4단계 추상화 진화의 산물임.

기존 On-Premise 환경은 ① **트래픽 변동성 대응 불가**(Peak 기준 Capacity 과잉투자), ② **신규 서비스 도출까지 6~12개월 Lead Time**, ③ **글로벌 서비스 불가**, ④ **Disaster Recovery 비용 과다**(DR Site Capex)라는 4대 구조적 한계 존재. 클라우드는 **리소스 풀링·빠른 탄력성·측정 가능한 서비스(Measured Service)**를 통해 이를 해결하며, 2023년 Gartner 조사에서 **기업 IT 예산의 50% 이상**이 이미 클라우드 전환되었음.

```text
[클라우드 아키텍처 진화 흐름: Mainframe -> On-Premise -> Virtualization -> Cloud -> Cloud-Native]

  +--------------+    +--------------+    +--------------+    +--------------+
  |   1980s      |    |   2000s      |    |   2010s      |    |   2020s~      |
  |  Mainframe   | -> | On-Premise   | -> | Virtualized  | -> |  Cloud-Native |
  |  Monolithic  |    |  Tiered App  |    |   x86 + VM   |    | K8s+Serverless|
  +--------------+    +--------------+    +--------------+    +--------------+
  고정 용량/고비용      수직확장/CAPEX     자원풀링/SLA        선언적·탄력적/OPEX
  (10년 Refresh)       (3~5년 Refresh)    (1~2년 Refresh)     (수 분 단위 AutoScale)
                                                       |
                                                       v
                            +-----------------------------------------+
                            |  Cloud-Native 4대 축 (CNCF Definition)  |
                            +-----------------------------------------+
                            |  ① Container    : Docker / CRI-O        |
                            |  ② Orchestration: Kubernetes / Istio    |
                            |  ③ Observability: Prometheus / OpenTelemetry|
                            |  ④ Provisioning : Terraform / ArgoCD    |
                            +-----------------------------------------+
```

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"전기 그리드"**와 같음. 과거에는 각 가정(기업)이 발전기(On-Premise)를 갖췄지만, 이제는 **전력회사(AWS/Azure/GCP)**가 수요에 맞춰 탄력적으로 전기를 공급하고, **kWh 단위(Compute-Second)**로 요금을 부과하는 모델. 따라서 발전소 설계(데이터센터 설계)는 공급사 책임이고, 우리는 **전등 스위치(API)**만 누르면 됨.

---

## Ⅱ. 아키텍처 및 핵심 원리

NIST SP 500-292 클라우드 컴퓨팅 참조 아키텍처(CCRA)는 **5대 핵심 특성**(On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service) + **3대 서비스 모델**(IaaS/PaaS/SaaS) + **4대 배포 모델**(Public/Private/Hybrid/Community)로 구성됨. 실무 아키텍처는 이 모델을 **Control Plane**(관리 API, IaC, IAM)과 **Data Plane**(실제 워크로드, Network, Storage)으로 이원화하여 설계함.

```text
[클라우드 아키텍처 4-Layer Reference Model: 책임 분계선(Shared Responsibility Model)]

  +------------------------------------------------------------------------+
  |  Layer 4: Application & Data (고객 100% 책임)                         |
  |  - Code, Data Encryption(Client-Side), IAM Policy, OS Patching         |
  +------------------------------------------------------------------------+
  |  Layer 3: Runtime & Middleware (고객 책임)                             |
  |  - JVM/Node.js, Container Image, K8s Manifest, Service Mesh Config     |
  +------------------------------------------------------------------------+
  |  Layer 2: OS & Virtualization (공유 책임 - IaaS)                       |
  |  - Guest OS Patch (고객) / Hypervisor (CSP) / Network ACL (공유)      |
  +------------------------------------------------------------------------+
  |  Layer 1: Physical Infrastructure (CSP 100% 책임)                      |
  |  - DataCenter, Server HW, Network, Storage, Power, Cooling             |
  +------------------------------------------------------------------------+

  [Cloud Service Stack - 책임 영역별 추상화 레벨]

  +----------------------------------------------------------------------+
  |  SaaS        (ex. Slack, Salesforce, MS 365, GitHub)                 |
  |  +----------------------------------------------------------------+  |
  |  |  FaaS    (ex. AWS Lambda, Azure Functions, Cloud Run Jobs)    |  |
  |  |  +----------------------------------------------------------+  |  |
  |  |  |  CaaS    (ex. EKS, AKS, GKE, Cloud Run)                 |  |  |
  |  |  |  +----------------------------------------------------+  |  |  |
  |  |  |  |  PaaS    (ex. RDS, App Engine, Beanstalk)         |  |  |  |
  |  |  |  |  +----------------------------------------------+  |  |  |  |
  |  |  |  |  |  IaaS    (ex. EC2, Azure VM, Compute Engine) |  |  |  |  |
  |  |  |  |  |                                              |  |  |  |  |
  |  |  |  |  |  <- 더 추상화 ^   v 더 제어 ->                |  |  |  |  |
  |  |  |  |  +----------------------------------------------+  |  |  |  |
  |  |  |  +----------------------------------------------------+  |  |  |
  |  |  +----------------------------------------------------------+  |  |
  |  +----------------------------------------------------------------+  |
  +----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Region / Availability Zone (AZ)** | 글로벌 분산 및 장애 격리 단위 | Region 간 **비동기 복제**(ex. S3 Cross-Region Replication, RPO ≥ 1분), AZ 내 **동기 복제 + 99.99% SLA** (3개 이상 AZ로 워크로드 분산, 다중 AZ Active-Active 구성) |
| **Control Plane** | 클라우드 자원 관리 및 API 라우팅 | **API Gateway -> Service Catalog -> Resource Manager** (Terraform/OpenTofu IaC로 선언적 정의, State Lock을 통한 Concurrency 제어) |
| **Compute Layer** | 워크로드 실행 환경 | **Hypervisor**(KVM/Xen) 기반 VM -> **cgroup+namespace** 기반 Container -> **Firecracker/MicroVM** 기반 Serverless(콜드 스타트 100ms 이내) |
| **Storage Tier** | 데이터 영속성 제공 | **Block**(EBS, Persistent Disk, IOPS 64,000+) / **Object**(S3, 11 9s Durability, 12 TB 객체 제한) / **File**(EFS, NFS v4) / **Cold**(Glacier, 최소 1분~12시간 회수) |

### Auto Scaling 알고리즘 핵심 원리

Auto Scaling은 **Target Tracking**(ex. CPU 60% 유지), **Step Scaling**(임계치 기반 단계적 증감), **Predictive Scaling**(ML 기반 시계열 예측, AWS Auto Scaling의 Predictive Scaling은 14일 학습) 3가지 방식이 있음. 핵심 공식은 다음과 같음:

```
DesiredCapacity = ceil( CurrentValue / TargetValue × CurrentCapacity )
                × (K8s HPA의 경우: TargetValue를 utilization 또는 value 기반 설정)

예) HPA: targetCPU = 60%, 현재 12 Pods, 평균 CPU 85%
Desired = ceil(85/60 × 12) = ceil(17) = 17 Pods 자동 증설
```

Karpenter(2022~)는 기존 Cluster Autoscaler 대비 **Pod 단위 동적 프로비저닝**으로 **스케일링 시간 80% 단축**(기존 2~3분 -> 20초) 및 **이종 인스턴스(ARM/GPU/Spot)** 통합 스케줄링을 지원하여 2024년 이후 사실상 표준이 됨.

- **📢 섹션 요약 비유**: 클라우드의 4-Layer 책임 모델은 **"아파트 관리"**와 같음. 외벽·지붕·난방(Data Center / Hypervisor)는 관리사무소(CSP)가 책임지고, **집 안 인테리어·보안장치·소화기**(OS·앱·데이터)는 입주자(고객)가 책임짐. 이 경계가 모호해지면 AWS WAF / Inspector가 입주자 구역을 점검해주는 셈.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처는 배포 모델, 서비스 모델, 아키텍처 패턴 측면에서 다층적 비교가 필요함. 특히 기술사 시험에서는 **Hybrid vs Multi-Cloud**, **Monolith vs Microservices**, **VM vs Container**의 Trade-off가 빈출 출제 영역임.

| 구분 | On-Premise (Private) | Public Cloud | Hybrid Cloud | Multi-Cloud |
| :--- | :--- | :--- | :--- | :--- |
| **초기 투자(CAPEX)** | 높음(서버·IDC) | 0원(OPEX 전환) | 중간(Burst만 클라우드) | 0원(여러 CSP) |
| **확장성** | 제한적(1~2개월 조달) | 무제한(수 분 내) | 데이터센터 Burst 가능 | CSP별 글로벌 활용 |
| **보안 통제** | 100% 자체 통제 | CSP 정책 종속 | 핵심 데이터 On-Prem | CSP별 상이 |
| **컴플라이언스** | 완전 통제 | 리전별 차등 (한국 C-ISMS 등) | 규제 데이터 On-Prem | 이기종 정책 |
| **TCO (3년)** | 고가(감가상각 포함) | 30~50% 절감 (대규모) | 20~35% 절감 | 15~30% 절감 (Egress 비용^) |
| **적합 워크로드** | 규제·금융코어, Legacy | 일반 웹·AI·Dev/Test | Batch·DR, 은행 코어 | 벤더 종속 회피·SLA |

### Microservices vs Monolithic 비교 (기술사 단골 출제)

| 항목 | Monolithic | Microservices |
| :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/JAR | 독립 컨테이너/서비스 |
| **스케일링** | 전체 복제 (비효율) | 서비스 단위 Granular Scale |
| **장애 격리** | 1개 버그 -> 전체 장애 | Circuit Breaker(Resilience4j, Hystrix)로 격리 |
| **데이터 관리** | 단일 DB(강한 일관성) | Saga Pattern / Eventual Consistency |
| **적합성** | 초기 스타트업 / 5인 이하 팀 | 도메인 독립·100명+ 조직 |

### 컨테이너 vs 가상화(VM) 비교

| 항목 | VM (KVM/Hypervisor) | Container (Docker) |
| :--- | :--- | :--- |
| **부팅 시간** | 30~60초 | 50ms~1초 |
| **이미지 크기** | GB 단위 (Guest OS 포함) | MB 단위 (App + lib) |
| **격리 수준** | 하드웨어 레벨 (강함) | 커널 공유 (중간, gVisor/Kata로 보완) |
| **밀도** | 호스트당 10~50개 | 호스트당 100~1000개 |
| **적합 사례** | 멀티 OS, 커널 격리 필수 | MSA, CI/CD, 동일 OS 워크로드 |

**연계 아키텍처**: 클라우드 아키텍처는 **API Gateway(쿠버네티스 Ingress) -> Service Mesh(Istio/Linkerd) -> Container Orchestrator(K8s/EKS) -> Observability(Prometheus+Grafana+Jaeger)**로 연결되며
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 734 / 800

<- **이전**: [733. 클라우드 아키텍처 핵심 토픽 733번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/733_cloud_architecture_core_topic_733_exam_summar/)
**다음**: [735. 클라우드 아키텍처 핵심 토픽 735번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/735_cloud_architecture_core_topic_735_exam_summar/) ->

---
