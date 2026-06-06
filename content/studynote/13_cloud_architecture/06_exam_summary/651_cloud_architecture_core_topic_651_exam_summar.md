---
title: "Cloud Architecture Core Topic 651 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST 표준 모델(IaaS/PaaS/SaaS/FaaS)을 기반으로 한 온디맨드 셀프서비스, 광역 네트워크 접근, 리소스 풀링, 탄력적 확장, 측정 가능한 서비스의 5대 필수 특성을 구현하기 위해 컨트롤 플레인(API/Orchestrator)과 데이터 플레인(Compute/Storage/Network)을 분리하여 선언적 API(예: Kubernetes Reconciliation Loop, Terraform HCL)로 추상화하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: CAPEX를 OPEX로 전환하여 초기 인프라 투자비를 60~80% 절감하고, Auto-Scaling을 통해 트래픽 변동 시 자원利用率을 30~70% 향상시키며, 글로벌 리전/엣지 배포로 사용자에게 평균 지연시간(Latency) 50~200ms 단축, DR(Disaster Recovery) RTO를 4시간에서 수 분 수준으로 단축시킨다.
> 3. **판단 포인트**: 12-Factor App 마이그레이션 시 Stateless vs Stateful 워크로드 구분, EKS/AKS/GKE 등 Managed Kubernetes 도입 시 컨트롤 플레인 관리 주체 책임 분담(Shared Responsibility Model), Multi-Cloud 적용 시 데이터 이그레스 비용(Egress Fee)과 벤더 종속(Lock-in) 간 트레이드오프, FinOps 기반의 Reserved Instance vs Spot Instance vs Savings Plans 비용 최적화 전략이 핵심 의사결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스(On-Premises) 환경에서는 CAPEX(Capital Expenditure) 기반의 정적 프로비저닝, 수동 패치 및 용량 계획, 단일 장애점(SPOF) 문제, 그리고 비즈니스 요구사항 대응까지 3~6개월의 리드타임이 필요했다. 2006년 AWS EC2 출시 이후 클라우드 컴퓨팅은 가상화(KVM/Xen/Hyper-V) -> 컨테이너화(Docker) -> 오케스트레이션(Kubernetes) -> 서버리스(Lambda/Cloud Functions) -> 엣지 컴퓨팅으로 진화하며, 현대 MSA(Microservices Architecture)와 DevOps/CI-CD 파이프라인의 기반 인프라로 자리잡았다.

특히 NIST SP 800-145 표준에 정의된 클라우드 컴퓨팅은 `분산 컴퓨팅`, `가상화`, `서비스 지향 아키텍처(SOA)`, `유틸리티 컴퓨팅`의 4가지 핵심 기술이 융합된 결과물이며, 2020년 이후 COVID-19 팬데믹으로 인한 디지털 전환 가속화와 함께 기존 대비 트래픽 10배 증가를 5분 이내에 Auto-Scaling으로 흡수하는 사례가 일반화되었다.

```text
[클라우드 아키텍처 진화 흐름도]

  +--------------+     +--------------+     +--------------+     +--------------+
  |   2006-2010  |     |   2010-2014  |     |   2014-2019  |     |   2020-현재  |
  |   1세대: VM  | ---> |  2세대: IaaS | ---> | 3세대: PaaS  | ---> |4세대: Serverless|
  |   가상화     |     |  AWS EC2/S3  |     |  Docker/K8s  |     | Lambda/Edge  |
  +--------------+     +--------------+     +--------------+     +--------------+
        |                     |                     |                     |
        v                     v                     v                     v
   [물리서버 통합]      [API 기반 제어]       [선언적 오케스트레이션]    [이벤트 기반]
   하이퍼바이저         OpenStack/AWS API    Helm/Operator 패턴      Event-Driven
   Xen -> KVM           Auto Scaling Group   CRD/Custom Controller   Cloudflare Workers
```

기존 온프레미스 대비 클라우드 도입의 핵심 동기는 ①TCO(Total Cost of Ownership) 절감 ②비즈니스 민첩성(Agility) 확보 ③글로벌 가용성 ④보안 및 컴플라이언스 자동화이며, 2024년 기준 Gartner 보고서에서 전체 엔터프라이즈 IT 예산의 60% 이상이 클라우드 전환되었음을 밝히고 있다.

- **📢 섹션 요약 비유**: 클라우드 컴퓨팅은 호텔의 룸서비스와 같다. 매달 자기 집을 짓고 관리하는 대신(온프레미스), 필요한 방을 빌려 쓰고(Elastic Capacity), 전기수도 사용량만큼만 청구되며(Usage-based Billing), 투숙객이 늘면 즉시 옆방을 추가 배정(Scale-out)해주는 똑똑한 숙박 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 크게 **프론트엔드(클라이언트) ↔ 백엔드(클라우드 플랫폼) ↔ 클라우드 기반 인프라(네트워크/스토리지/서버)**의 3계층으로 구성되며, 백엔드 내부적으로는 컨트롤 플레인(Control Plane)과 데이터 플레인(Data Plane)이 논리적으로 분리된다.

```text
[클라우드 아키텍처 4계층 참조 모델 (AWS Well-Architected Framework 기준)]

   +------------------------------------------------------------------------+
   |  Layer 1: 사용자 인터페이스 (Console / CLI / SDK / API Gateway)        |
   |           AWS Console, Terraform, Pulumi, AWS CDK, kubectl, Helm        |
   +------------------------------------------------------------------------+
   |  Layer 2: 서비스 오케스트레이션 (IaaS/PaaS/SaaS/FaaS)                  |
   |   +----------+  +----------+  +----------+  +----------+               |
   |   |  IaaS    |  |  PaaS    |  |  SaaS    |  |  FaaS    |               |
   |   | EC2/ECS  |  | RDS/EKS  |  | Office365|  | Lambda   |               |
   |   | 직접관리 |  | 부분관리 |  | 완전관리 |  | 함수단위 |               |
   |   +----------+  +----------+  +----------+  +----------+               |
   +------------------------------------------------------------------------+
   |  Layer 3: 가상화/컨테이너 런타임                                       |
   |   +----------------+    +----------------+    +----------------+       |
   |   | Hypervisor     |    | Container      |    | MicroVM        |       |
   |   | KVM, Xen, ESXi |    | runC, containerd|    | Firecracker    |       |
   |   | Guest OS 포함  |    | Host OS 커널공유|    | Lambda 전용    |       |
   |   +----------------+    +----------------+    +----------------+       |
   +------------------------------------------------------------------------+
   |  Layer 4: 물리 인프라 (Region/AZ/Edge)                                 |
   |   Region(리전) -> AZ(가용영역) -> Edge Location -> 물리 데이터센터        |
   |   전 세계 30+ 리전, 100+ AZ, 400+ PoP(Points of Presence)              |
   +------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컨트롤 플레인 (Control Plane)** | 리소스 상태 정의, 스케줄링, API 게이트웨이 | Kubernetes API Server(etcd 기반 RAFT 합의 알고리즘), AWS Step Functions, Terraform State Management, 선언적 desired state -> actual state Reconciliation |
| **데이터 플레인 (Data Plane)** | 실제 워크로드 실행, 데이터 처리 | kubelet(노드 에이전트), AWS Nitro System(전용 하드웨어 가상화), VPC CNI, eBPF 기반 Cilium CNI, 1ms 단위 네트워크 성능 보장 |
| **가상화 계층** | 물리 자원의 논리적 분할/격리 | Type-1 Hypervisor(KVM/Xen), KVM-QEMU 조합, vhost-net/virtio 패스스루, SR-IOV를 통한 NIC 직접 할당, NUMA-aware 스케줄링 |
| **스토리지 추상화** | 블록/오브젝트/파일 스토리지 | S3(오브젝트, 11 9s 내구성), EBS(블록, gp3/io2), EFS(파일, NFSv4), CSI(Container Storage Interface) 표준으로 K8s 연동, RDMA over Converged Ethernet(RoCE) |

**Kubernetes Reconciliation Loop 핵심 원리**: `etcd(분산 KV 저장소) -> API Server(인증/인가/Admission) -> Scheduler(노드 할당) -> kubelet(컨테이너 기동) -> cAdvisor(리소스 모니터링) -> Controller Manager(상태 비교)`의 끊임없는 폐루프 구조이며, 선언적 YAML(`spec.replicas: 3`)과 실제 상태(`status.readyReplicas: 2`)를 비교하여 1초 단위로 보정한다.

**주요 기술 파라미터**:
- **가용성(Availability)**: SLA 99.99% (연 52분 장애 허용) -> Multi-AZ 배포로 99.999% (연 5분) 달성
- **일관성(Consistency)**: CAP Theorem -> DynamoDB(AP), Google Spanner(CP+Linearizability), Cosmos DB(Tunable Consistency)
- **확장성**: AWS Auto Scaling의 Target Tracking Policy(CPU 70% 기준), K8s HPA(Horizontal Pod Autoscaler) – 15초 기본 동기화 주기
- **네트워크**: VPC CIDR/16 (/65,536 IP), VXLAN 오버레이, BGP Anycast for Global Accelerator, Latency-Based Routing

- **📢 섹션 요약 비유**: 클라우드의 컨트롤 플레인은 자동차의 `자율주행 두뇌`이고 데이터 플레인은 `바퀴와 엔진`이다. 두뇌(컨트롤 플레인)가 "목표 속도 60km/h"라고 선언하면, 엔진과 바퀴(데이터 플레인)가 매 순간 실제 속도를 측정해서 두뇌에 보고하고, 두뇌가 차이가 나면 즉시 가속 페달을 조정한다. 이 끊임없는 피드백 루프가 클라우드의 자기 치유(Self-healing) 능력이다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처는 다양한 레이어에서 대체 기술과 비교되며, 각각의 트레이드오프가 존재한다.

| 구분 | **IaaS (EC2/EKS 노드)** | **PaaS (EKS/Cloud Run/App Engine)** | **FaaS (Lambda/Cloud Functions)** | **On-Premises** |
| :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | OS~미들웨어 직접 관리 | 런타임/미들웨어 부분 관리 | 코드만 관리 (전부 위임) | HW~앱 전부 자체 관리 |
| **확장 단위** | VM/Instance 단위 | 컨테이너/Pod 단위 | 함수 단위 (1ms 단위 스케일) | 수동, 수일~수주 소요 |
| **콜드 스타트** | 없음 (이미 기동) | 1~10초 | 100ms~5초 (Provisioned Concurrency로 해결) | 없음 |
| **최소 과금** | 1초 단위 (Linux) | 100ms 단위 | 1ms 단위, 100만 요청 무료 | 초기 HW 투자비 |
| **적합 워크로드** | Stateful DB, 레거시, HPC | MSA API 서버, 배치 | 이벤트 드리븐, ETL, Webhook | 보안/규제 필수, 극저지연 |
| **Lock-in 정도** | 낮음 (Kubernetes 표준) | 중간 (Managed K8s API 차이) | 높음 (벤더 종속 트리거/IAM) | 없음 |
| **TCO (3년)** | 중간 | 낮음 | 매우 낮음 (유휴 0원) | 높음 |
| **디버깅 용이성** | 높음 (SSH 접근) | 중간 (Sidecar 로그) | 낮음 (분산 트레이싱 필수) | 매우 높음 |
| **보안 책임** | Shared (OS 패치 필요) | Shared (런타임은 CSP) | 완전 위임 (CSP 책임) | 전사 자체 책임 |
| **네트워크 지연** | 0.1~0.5ms (같은 AZ) | 0.1~0.5ms | 1~5ms (Cold Path) | 0.01~0.1ms (Direct) |

**Multi-Cloud vs Hybrid Cloud vs Sovereign Cloud**:
- **Multi-Cloud**: AWS+S+GCP를 동시 사용 -> 벤더 종속 회피, 최적의 서비스 선택(예: GCP BigQuery + AWS Lambda)
- **Hybrid Cloud**: AWS Outposts/Azure Arc/Azure Stack HCI -> 온프레미스 + 퍼블릭 클라우드 통합, 데이터 주권 확보
- **Sovereign Cloud**: AWS European Sovereign Cloud(2025 런칭), Azure for Government, Google Sovereign Cloud -> EU GDPR, 한국 클라우드 보안인증(CSAP) 등 데이터 주권 규제 대응

**주요 CSP별 차별점**:
- **AWS**: 가장 성숙한 서비스(200+), Nitro System 하드웨어 가상화, Graviton3 ARM 프로세서(20% 성능^/60% 전력v)
- **Azure**: Active Directory 통합, Hybrid 강점(Azure AD, Arc), Microsoft 365 SaaS 생태계
- **GCP**: Kubernetes 원조(Borg 내부 -> GKE 오픈소스), BigQuery(페타바급 분석), Anthos 멀티클라우드
- **Naver Cloud / NHN / KT Cloud**: 한국 CSAP 인증, 공공/금융 시장 강점, 한국어 지원

**MSA(Microservices)와의 연결**:
- Service Mesh: Istio/Linkerd (L7 트래픽 관리, mTLS, Canary 5%->50%->100%)
- API Gateway: Kong, AWS API Gateway, Apigee
- 분산 트레이싱: OpenTelemetry + Jaeger/Zipkin
- Saga Pattern: 보상 트랜잭션 (Temporal/Cadence 워크플로 엔진)

- **📢 섹션 요약 비유**: IaaS는 토지를 빌려서 직접 집을 짓는 것이고, PaaS는 설계도가 제공되는 조립식 주택이며, FaaS는 한 가지 요리만 시키는 배달 서비스(요청할 때만 요리사가 움직이고, 안 시키면 0원)다. Multi-Cloud는 토지를 여러 지역에 분산해 짓는 것이고, Hybrid Cloud는 본가(온프레미스)와 별장(클라우드)을 오가는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **워크로드 분류 (Stateless vs Stateful)**: API 서버/웹 프론트는 Stateless -> EKS/ECS Fargate로 컨테이너화, RDS/ElastiCache/StatefulSet(DB)은 Stateful -> Multi-AZ 배포 + 자동 백업 + 읽기 전용 복제본 구성. `12-Factor App` 원칙 적용 시 프로세스는 Stateless해야 Auto-Scaling이 가능하다.
2. **비용 최적화 (FinOps)**: 1) Compute Savings Plans(최대 66% 할인) vs Reserved Instance vs Spot Instance(최대 90% 할인) -> 70% Steady State는 Savings Plans, 20% Baseline은 RI, 10% Batch는 Spot. 2) S3 Intelligent-Tiering(자동 계층 이동), 3) Egress 비용 최적화(같은 Region 내부 트래픽 0원, CloudFront/CDN 활용), 4) Rightsizing(GPU/메모리 과다 할당 제거) -> 평균 30~40% 비용 절감 가능.
3. **보안 및 컴플라이언스**: Shared Responsibility Model에서 고객은 데이터/IAM/VPC/앱 보안 책임, CSP는 물리/하이퍼바이저/글로벌 인프라 책임. WAF + Shield Advanced(DDoS 방어), GuardDuty(위협 탐지), Macie(데이터 식별), KMS(Customer Managed Key) + CloudHSM, VPC Flow Logs 90일 보관을 통한 `제로 트러스트(Zero Trust)` 구현. 한국 CSAP(
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 651 / 800

<- **이전**: [650. 클라우드 아키텍처 핵심 토픽 650번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/650_cloud_architecture_core_topic_650_exam_summar/)
**다음**: [652. 클라우드 아키텍처 핵심 토픽 652번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/652_cloud_architecture_core_topic_652_exam_summar/) ->

---
