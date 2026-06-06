---
title: "Cloud Architecture Core Topic 650 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 Well-Architected Framework(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속가능성 6대 필러) 기반의 셀프서비스 API·메트릭·이벤트 추상화 계층을 통해 컴퓨트·스토리지·네트워크 자원의 선언적 프로비저닝과 탄력적 오케스트레이션을 실현하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: AWS·Azure·GCP 등 하이퍼스케일러 기준으로 동일 워크로드 대비 CapEx->OpEx 전환 시 TCO 30~60% 절감, Auto Scaling을 통한 피크 트래픽 흡수(평균 70% 이상 비용 회수), 글로벌 멀티리전 액티브-액티브로 RTO/RPO 수 분 -> 수 초 단위 단축이 가능하다.
> 3. **판단 포인트**: Shared Responsibility Model에서 IaaS/PaaS/SaaS별 책임 경계 결정, 단일 리전/멀티 리전/하이브리드/멀티클라우드 토폴로지 선택, Stateless 12-Factor 앱 설계 여부, 그리고 FinOps 기반의 Reserved/On-Demand/Spot 인스턴스 비율 최적화가 아키텍트의 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스 3-Tier 아키텍처는 Capacity Planning의 한계로 평균 자원 활용률 15~25%에 불과하며, 트래픽 피크 시 수직적 스케일업(Scaling Up)의 물리적 한계와 수개월의 조달 리드타임이라는 구조적 병목을 내포한다. 2006년 AWS S3·EC2 출시 이후 클라우드 컴퓨팅은 가상화(KVM/Xen->KVM·Firecracker), 컨테이너(Docker 2013->containerd/CRI-O), 오케스트레이터(Kubernetes 2015, CNCF 졸업 2018), 서버리스(Lambda 2014, Knative 2018), Service Mesh(Istio 2017, Linkerd 2017) 등으로 발전하며 인프라 추상화 수준을 Hardware->VM->Container->Function->API로 끌어올렸다.

NIST SP 800-145는 클라우드를 5대 필수 특성(On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)과 3대 서비스 모델(IaaS/PaaS/SaaS), 4대 배포 모델(Public/Private/Hybrid/Community)로 정의하며, 이는 클라우드 아키텍처 설계 시 모든 의사결정의 기준 프레임이 된다. Gartner가 명명한 Hype Cycle 2024 기준으로 클라우드 네이티브 플랫폼, GitOps, eBPF 기반 옵저버빌리티가 Plateau of Productivity에 진입했고, FinOps·GreenOps가 Innovation Trigger 단계로 부상 중이다.

```text
[ 온프레미스 vs 클라우드 아키텍처 패러다임 비교 ]

   +--- On-Premise ---+                +--- Cloud-Native ---+
   |  [App]-[WAS]-[DB] |                | [Pod] [Pod] [Pod]  |
   |       |           |                |   |   |   |   |    |
   |   [Hypervisor]    |                | +-v---v---v---v-+  |
   |   [HW][HW][HW]    |                | |  Service Mesh |  |
   |  CapEx·Static·HW  |                | | (Istio/Linkerd)|  |
   |  수직확장·수개월   |                | +---------------+  |
   |  활용률 15~25%    |                |   |   |   |   |    |
   +-------------------+                | [K8s Control Plane]|
                                        |   |                 |
   [문제점]                              | [Cloud API·IaC]    |
   • 과잉/과소 프로비저닝                 | (Terraform/ArgoCD) |
   • 피크 손실·유휴 낭비                  |                    |
   • 장애 도메인 단일화                   | 특징:              |
   • DR 비용·복잡도 ^                    | • OpEx·동적·API     |
                                        | • 수평확장·수 초    |
                                        | • 활용률 60~80%     |
                                        | • 멀티 AZ·멀티 리전 |
                                        +--------------------+
```

클라우드의 필요성은 단순한 비용 절감이 아니라 **비즈니스 민첩성(Time-to-Market)**, **글로벌 가용성**, **데이터 기반 의사결정의 민주화**에 있다. Netflix는 2008년 DB 손상 사고 이후 10년+에 걸쳐 700+ 마이크로서비스로 전환하며, AWS 멀티 리전 액티브-액티브로 동시 시청자 2억 명 규모 트래픽을 처리한다. 국내 케이스에서는 카카오의 토큰 인증 시스템 클라우드 전환(2019), NHN의 멀티클라우드(GCP+AWS+NCP) 도입, 그리고 공공부문 클라우드 이용지침(2023.6 시행)에 따른 클라우드 우선 전략(Cloud First) 추진이 대표적이다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **"전기를 직접 발전하는 자가발전(온프레미스)에서 전력회사의 전력망(클라우드)으로 전환한 것"**과 같다. 필요할 때 콘센트(IaaS·PaaS API)를 꽂기만 하면 되고(API 기반 셀프서비스), 사용량(kWh = 컴퓨트·스토리지·네트워크 미터링)만큼만 비용을 지불하며, 전력회사가 발전량 탄력 조정(Auto Scaling)과 정전 대비 이중화(멀티 AZ)를 책임지는 것과 동일한 메커니즘이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 4계층 참조 모델은 (1) 글로벌 인프라 리전·가용영역, (2) 컴퓨트·스토리지·네트워크·데이터베이스 서비스, (3) 오케스트레이션·Service Mesh·CI/CD, (4) Observability·FinOps·Security 거버넌스로 구성된다. 핵심 원리는 **API 선언적 의도(Declarative Intent) -> 컨트롤 플레인(Control Plane) -> 데이터 플레인(Data Plane) -> 피드백 루프(Feedback Loop)**의 4단계 사이클로, Kubernetes의 Reconciliation Loop(원하는 상태 vs 실제 상태의 차이를 줄이는 알고리즘)가 이를 가장 정형화한 구현체다.

```text
[ 클라우드 네이티브 4계층 아키텍처 + 컨트롤/데이터 플레인 분리 ]

  +----------------- Layer 4: 거버넌스 -----------------+
  |  FinOps(CUR·Cost Explorer) | SecOps(CSF·SIEM)       |
  |  SRE(SLI/SLO/Error Budget) | GreenOps(탄소미터)      |
  +------------------------------------------------------+
                              ^ 메트릭/이벤트
  +-------------- Layer 3: 오케스트레이션 ---------------+
  |  +--------------+   +--------------+                 |
  |  | Control Plane|   |  Data Plane  |                 |
  |  |  - API Server|   |  - kubelet   |                 |
  |  |  - etcd      |<--->|  - kube-proxy|                 |
  |  |  - scheduler |   |  - CNI/CSI   |                 |
  |  |  - controller|   |  - sidecar   |                 |
  |  +--------------+   +--------------+                 |
  |  GitOps(ArgoCD) | Service Mesh(Istio) | CI/CD       |
  +------------------------------------------------------+
                              ^
  +-------------- Layer 2: 클라우드 서비스 --------------+
  | Compute      | Storage        | Network     | DB    |
  | EC2/EKS/λ    | S3/EBS/EFS     | VPC/ALB/TGW | RDS   |
  | VMSS/AKS/Fn  | Blob/Disk/Fs   | VNet/LB/vWAN | Cosmos|
  | MIG/GKE/CF   | GCS/Persistent | VPC/GLB/CCN  | Spanner|
  +------------------------------------------------------+
                              ^
  +-------------- Layer 1: 글로벌 인프라 ----------------+
  |  Region(30+개) -> AZ(3~6개) -> Edge Location(400+개) |
  |  PoP(Points of Presence) -> Cdn(Wavelength/Outposts) |
  +------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **리전(Region)·가용영역(AZ)** | 지리적 격리 단위·장애 도메인 | 동일 리전 내 AZ 간 지연시간 1~2ms, AZ 간 독립 전력·냉각·네트워크. 멀티 AZ 동기식 복제(RDS Multi-AZ, Aurora 6-way Replica)로 RPO=0 달성 |
| **컴퓨트 추상화** | CPU·메모리·GPU 자원 제공 | Bare Metal(I3en, EC2 Metal) -> VM(EC2 m6i, D3v) -> 컨테이너(EKS, Fargate, GKE Autopilot) -> Function(Lambda, Cloud Functions) 순으로 추상화 상승, Cold Start 시간은 Bare Metal 0ms~Function 100ms+ |
| **오브젝트 스토리지(S3)** | 11 9s 내구성, HTTP API | Erasure Coding(150% 오버헤드), Sharding·Index 관리, Lifecycle Policy(IA->Glacier->Deep Archive 7단계), Pre-signed URL·Transfer Acceleration |
| **컨트롤 플레인 vs 데이터 플레인** | 의도 해석 vs 실제 트래픽 처리 | K8s의 경우 API Server 6443 포트 etcd 합의 알고리즘 Raft, kubelet이 cAdvisor·CRI로 리소스 사용량 보고, kube-proxy가 iptables/IPVS로 Service 라우팅 |
| **Service Mesh(Istio)** | L7 트래픽 관리·mTLS·관측 | Envoy Sidecar(1500+ 설정 옵션), xDS API(CDS·EDS·LDS·RDS·SDS) 기반 Push 설정, Istiod가 SPIFFE/X.509 SVID 인증서 24h 자동 로테이션 |
| **IaC·GitOps** | 선언적 인프라·불변 인프라 | Terraform Plan/Apply 상태머신(원격 State Lock via DynamoDB), ArgoCD Application Controller 3분 주기 Sync, OPA/Gatekeeper·Kyverno로 Policy-as-Code 적용 |

핵심 알고리즘으로 **Reconciliation Loop**는 `desired_state = spec`, `actual_state = status`일 때 `status = reconcile(spec)` 함수가 무한 반복되며 차이를 줄이는 패턴이다. K8s Deployment는 `Replicas: 3`이라는 의도(spec) -> 현재 Pod 1개(actual) -> controller가 Pod 2개 추가 생성 -> 실제 상태가 의도와 일치하면 idle 상태로 전환. 이 사이클 주기는 기본 5~10초이며 HPA v2는 15초 주기 메트릭 폴링으로 스케일링 결정을 내린다. HPA의 스케일링 공식은 `desiredReplicas = ceil[currentReplicas * (currentMetricValue / desiredMetricValue)]`이며, stabilizationWindow로 스케일링 진동(Thrashing)을 방지한다.

확장성 패턴(Scalability Patterns)으로는 (1) **수평 확장(Horizontal Scaling)**: stateless 웹 티어, ALB/NLB의 Connection Draining 5~300초 설정, (2) **수직 확장(Vertical Scaling)**: RDS db.r6i 24xlarge -> db.r6i 32xlarge 같은 1회성 증설, (3) **오토스케일링**: Scheduled Scaling(예측 가능), Dynamic Scaling(Target Tracking 70% CPU, Step Scaling 임계치 기반), Predictive Scaling ML 기반 2일 예측, (4) **샤딩**: 데이터베이스의 수평 파티셔닝, Customer ID 해시 기반 N개 Shard 분산, (5) **CQRS + Event Sourcing**: 쓰기/읽기 모델 분리, Kafka·Kinesis·EventBridge로 이벤트 스트림 처리.

- **📢 섹션 요약 비유**: 컨트롤 플레인과 데이터 플레인의 분리는 **"비행기의 조종간(Control Plane)과 날개·엔진(Data Plane)"** 관계와 같다. 조종간은 의도("상승·좌회전")를 해석하고, 날개와 엔진이 실제 물리적 추력·양력을 발생시킨다. 관제탑(etcd·API Server)이 모든 조종간 신호를 검증·승인하고, 비행 데이터는 블랙박스(Observability·Audit Log)에 기록되어 사고 후 분석에 사용된다.

---

## Ⅲ. 비교 및 연결

| 구분 | **IaaS (EC2/VMSS)** | **PaaS (EKS/Beanstalk)** | **SaaS (Salesforce/Workday)** | **On-Premise (전통 3-Tier)** |
| :--- | :--- | :--- | :--- | :--- |
| **책임 범위 (Shared Responsibility)** | OS·미들웨어까지 사용자, 그 위는 CSP | 런타임·미들웨어 CSP, 앱·데이터는 사용자 | 모든 스택 CSP, 사용자는 설정·데이터만 | 100% 사용자 책임 |
| **확장 단위** | VM 인스턴스, 5분 이내 부팅 | 컨테이너·앱 단위, 30초 이내 | 자동·사용자 조정 불가 | 하드웨어 도입, 3~6개월 |
| **제어성 vs 편의성** | 제어 ^ / 편의 v | 제어·편의 균형 | 제어 v / 편의 ^ | 제어 최댓값 / 편의 최솟값 |
| **적합 워크로드** | 레거시 Lift&Shift, 커스텀 OS/Hypervisor | 12-Factor 마이크로서비스, CI/CD 친화 | CRM·ERP·HCM 표준 프로세스 | 미션크리티컬·규제산업·데이터 주권 |
| **TCO 3년 모델** | 30~40% 절감 | 50~60% 절감 | 70% 절감 | 기준점(100%) |

| 구분 | **단일 클라우드(Public)** | **멀티 클라우드(Public 복수)** | **하이브리드(Public+Private)** | **멀티 리전 액티브-액티브** |
| :--- | :--- | :--- | :--- | :--- |
| **아키텍처 복잡도** | 낮음 | 높음(2~3개 CSP 통합) | 중간(Direct Connect·ExpressRoute) | 매우 높음(데이터 복제·충돌 해소) |
| **벤더 락인 위험** | 높음 | 낮음(이식성 확보) | 중간 | 동일 벤더 한정 시 중간 |
| **DR 전략** | 동일 리전 내 AZ 장애 대응 | CSP 장애 격리·지리적 재배치 | On-Prem ↔ Cloud 워크로드 이동 | 리전 단위 장애 시 자동 failover |
| **RTO/RPO 목표** | RTO 분, RPO 0(AZ 단위) | RTO 분, RPO 0(CSP 단위) | RTO 시간, RPO 분 | RTO 수 초, RPO 0(리전 단위) |
| **비용** | 낮음 | 높음(중복 학습·인력·연결) | 중간(회선 비용) | 매우 높음(2배+ 트래픽·복제 비용) |

**주변 기술 연계성**:
- **DevOps ↔ 클라우드**: GitHub Actions·GitLab CI·Jenkins X의 파이프라인이 클라우드 API(Terraform·kubectl·Pulumi)를 호출해 자동 배포
- **AIOps ↔ Observability**: Datadog·New Relic·Dynatrace가 eBPF·OpenTelemetry로 수집한 메트릭을 ML로 이상탐지, AIOps가 원인 분석 자동화
- **보안(CSPM/CWPP)**: Wiz·Lacework·Prisma Cloud가 CSP 설정 오류(S3 Public Access Block 미적용)·런타임 위협(Container Escape) 통합 탐지
- **데이터 거버넌스**: Data Lake(S3·ADLS·GCS) + Lakehouse(Delta Lake·Iceberg·Hudi) + Data Mesh 도메인별 데이터 소유 구조
- **엣지 컴퓨팅**: AWS Wavelength(5G MEC), Azure Edge Zones, Google Distributed Cloud로 CDN을 넘어 컴퓨트 워크로드를 단말 근접 배치

- **📢 섹션 요약 비유
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 650 / 800

<- **이전**: [649. 클라우드 아키텍처 핵심 토픽 649번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/649_cloud_architecture_core_topic_649_exam_summar/)
**다음**: [651. 클라우드 아키텍처 핵심 토픽 651번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/651_cloud_architecture_core_topic_651_exam_summar/) ->

---
