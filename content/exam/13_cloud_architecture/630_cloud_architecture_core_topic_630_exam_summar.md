---
title: "Cloud Architecture Core Topic 630 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 퍼블릭·프라이빗·하이브리드 클라우드 환경에서 컴퓨팅·스토리지·네트워크를 코드(IaC)로 선언하고, 컨테이너·서비스 메시·옵저버빌리티를 통해 워크로드를 **동적·탄력적·자가치유(Self-healing)** 상태로 운영하는 분산 아키텍처 패러다임.
> 2. **가치**: AWS Well-Architected Framework 기준으로 운영 우수성 80% 향상, 비용 30~70% 절감(Reserved/Spot + FinOps), 가용성 SLA 99.99% 확보, 배포 리드타임 1주->1시간(MTTR 60%v) 같은 정량적 효과를 통한 **Time-to-Market 및 Resilience 극대화**.
> 3. **판단 포인트**: **Cloud Native vs Lift & Shift**, **Monolith vs Microservices**, **Multi-Cloud vs Single-Cloud**, **VM vs Container vs FaaS**, **Synchronous vs Event-Driven** 등 5대 아키텍처 결정 포인트에서 트레이드오프(비용·복잡성·데이터 일관성·벤더 종속·보안 책임 경계)를 명확히 분석해야 함.

---

## Ⅰ. 개요 및 필요성

클라우드 컴퓨팅은 NIST SP 800-145에서 **필요 시 자기 서비스(self-service on-demand)**, **광대역 네트워크 접근**, **리소스 풀링**, **신속한 탄력성(elasticity)**, **측정 가능한 서비스(measured service)**의 5대 필수 특성을 정의하며, 이를 통해 CapEx(설비투자) -> OpEx(사용량 기반 과금)로의 IT 재무 구조 전환을 가능케 한다. 2024년 기준 글로벌 퍼블릭 클라우드 시장 규모는 약 7,200억 USD로, IDC/Gartner 보고서에서 전체 엔터프라이즈 워크로드의 70% 이상이 2027년까지 클라우드 네이티브 환경으로 전환될 것으로 전망된다. 한국 정부·공공기관도 '공공클라우드 도입 가이드라인(2022)' 및 '클라우드 이용 가속화 방안'에 따라 SaaS·PaaS 우선 도입 원칙을 천명하였다.

전통적 온프레미스 아키텍처는 다음과 같은 구조적 한계를 가진다:
- **수직 확장(Scale-Up) 한계**: CPU·메모리·스토리지가 단일 물리 서버에 종속되어, Moore's Law 둔화와 함께 비용 곡선이 비선형적으로 증가
- **수동 프로비저닝**: 인프라 배포에 수일~수주 소요, 휴먼 에러율 5~15%
- **고정 용량 계획**: 평균利用率 15~25%, 피크 시간 자원 부족, 비피크 시간 낭비
- **DR(재해복구) 비용**: 이중화·백업 인프라에 전체 IT 예산의 20~30% 소요
- **사일로 조직**: Dev(개발) ↔ Ops(운영) 간 책임 경계·문화 충돌

클라우드 아키텍처는 이를 **가상화·오케스트레이션·자동화·관측가능성**의 4축으로 해결하며, **Infrastructure as Code(Terraform, AWS CDK, Pulumi)**, **선언적 API(Kubernetes, OpenStack)**, **GitOps(ArgoCD, Flux)** 패러다임을 통해 인프라 자체를 버전 관리·테스트·롤백 가능 객체로 전환한다.

```text
+-----------------------------------------------------------------+
|              Legacy On-Premise vs Cloud-Native 비교               |
+--------------------------+--------------------------------------+
|   Legacy (수동·정적)       |   Cloud-Native (자동·동적)            |
+--------------------------+--------------------------------------+
| +------------------+     | +------------------------------+    |
| | 물리 서버 100대    |     | | API 호출 -> Auto Scaling Group |    |
| | 고정 100% 용량     |     | | Min:2 / Desired:5 / Max:100   |    |
| | 수동 설치·패치     |     | | AMI + UserData + Ansible     |    |
| +------------------+     | +------------------------------+    |
| +------------------+     | +------------------------------+    |
| | SAN 스토리지      |     | | S3 / EBS / EFS / FSx         |    |
| | RAID·LUN 수동관리  |     | | 객체·블록·파일·분산형 자동화   |    |
| +------------------+     | +------------------------------+    |
| +------------------+     | +------------------------------+    |
| | 단일 네트워크 VLAN |     | | VPC / Subnet / SG / NLB / ALB |    |
| | 수동 VLAN·ACL     |     | | IaC(Terraform) 선언적 정의    |    |
| +------------------+     | +------------------------------+    |
| 배포: 수주, 변경: 수동    | 배포: 수분, 변경: Git Push -> CI/CD   |
| 가용성: 99.9% (SLA)      | 가용성: 99.99% (Multi-AZ/Region)    |
+--------------------------+--------------------------------------+
```

기술사적 관점에서 클라우드 도입은 단순 IT 인프라 이전이 아니라, **비즈니스 agility(민첩성), 기술 부채(technical debt) 상환, 운영 모델 전환(DevOps/Platform Engineering), 재무 모델 재설계**가 통합된 **디지털 트랜스포메이션의 핵심 엔진**이다.

- **📢 섹션 요약 비유**: 온프레미스는 **소유(own)·정원 가꾸기**처럼 직접 땅을 사고, 씨앗 심고, 물주고, 해충 잡는 일체를 직접 해야 하는 방식이고, 클라우드 아키텍처는 **공유 정원(Community Garden)+스마트 온실 자동화**처럼 필요한 만큼 화분을 빌려 쓰고, 자동 관수·환기 시스템이 일사량·습도에 맞춰 알아서 조절해 주는 차이입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **5계층 참조 모델(Reference Model)**로 추상화할 수 있다. 각 계층은 명확한 책임 경계(Separation of Concerns)를 가지며, 계층 간 통신은 **API·이벤트 버스·서비스 메시 데이터 플레인**을 통해 수행된다.

```text
+--------------------------------------------------------------+
|                    Cloud Architecture 5-Layer Model           |
+--------------------------------------------------------------+
|  L5. Application / Workload                                  |
|      +- Monolith · Microservices · Serverless · Event-Driven|
|      +- API Gateway(Kong, AWS API GW) + BFF Pattern         |
+--------------------------------------------------------------+
|  L4. Data / Storage                                          |
|      +- RDBMS(Aurora, Cloud SQL) · NoSQL(DynamoDB, MongoDB) |
|      +- Cache(ElastiCache Redis, MemoryDB) · Search(OpenSearch)|
|      +- Data Lake(S3+Glue+Athena) · Lakehouse(Iceberg, Delta)|
+--------------------------------------------------------------+
|  L3. Runtime / Orchestration                                 |
|      +- Container: Docker · Containerd · CRI-O              |
|      +- Orchestrator: Kubernetes(EKS/GKE/AKS) · Service Mesh(Istio)|
|      +- Serverless: Lambda · Cloud Run · Fargate · Knative |
+--------------------------------------------------------------+
|  L2. Compute / Virtualization                                |
|      +- Hypervisor: KVM · Xen · Hyper-V (EC2, Compute Engine)|
|      +- Bare-Metal: i3.metal, AWS Nitro System               |
|      +- GPU/Accelerator: T4, A100, H100, Trainium, Inferentia|
+--------------------------------------------------------------+
|  L1. Infrastructure (Region / AZ / Edge)                     |
|      +- Region(지리적 리전) · AZ(가용영역) · PoP(Points of Presence)|
|      +- Network: VPC · Transit Gateway · Cloud WAN · SD-WAN  |
|      +- Power · Cooling · 물리 보안(데이터센터)             |
+--------------------------------------------------------------+

       +--------------- Cross-Cutting Concerns ---------------+
       |  IaC(Terraform, CDK) · CI/CD(ArgoCD, Spinnaker)     |
       |  Observability(Prom+Grafana+TEMPO+Loki)             |
       |  Security(IAM, KMS, WAF, CSPM, CASB, CWPP)          |
       |  FinOps(CUR, Kubecost, Vantage) · Sustainability    |
       +------------------------------------------------------+
```

### 핵심 계층별 동작 원리

**1) L1 - 글로벌 인프라**: AWS·Azure·GCP는 전 세계 30~60개 리전에 분포하며, 각 리전은 2~6개의 **AZ(Availability Zone, 독립 전력·냉각·네트워크의 데이터센터 클러스터)**로 구성된다. 두 AZ 간 거리는 약 100km 이내(레이턴시 < 2ms)이며, Multi-AZ로 구성 시 **동기식 복제**가 가능하다. **리전 간 복제**는 100~200ms 레이턴시를 가지므로 **비동기식(Eventually Consistent)**으로 처리한다.

**2) L2 - 컴퓨트 가상화**: AWS Nitro System은 **Dedicated Nitro Card(Security Chip + VPC 가속 + EBS 최적화 + Nitro Enclaves)**로 호스트 커널 우회, EC2 인스턴스의 **99.999% 보안 격리**와 **네트워크 패킷 처리 오프로드**를 제공한다. 컨테이너는 cgroup(Control Group)+namespace로 OS 레벨 가상화를 수행하며, **부팅 시간 ~100ms, 이미지 크기 ~50~200MB**로 VM 대비 10~50배 빠른 기동성을 보인다.

**3) L3 - 오케스트레이션 (Kubernetes 중심)**: K8s는 다음 핵심 객체 모델을 가진다:
- **Pod**: 1~N개 컨테이너, 네트워크 네임스페이스·스토리지 공유
- **Deployment**: ReplicaSet + 롤링 업데이트 전략(RollingUpdate, Blue/Green, Canary)
- **Service**: ClusterIP(내부) / NodePort(외부 노출) / LoadBalancer(AWS NLB/ALB 연동)
- **Ingress**: L7 라우팅, TLS 종료, Path/Host 기반 분기 (Ingress-NGINX, Traefik, Contour)
- **HPA / VPA / Karpenter**: CPU·Memory·Custom Metric 기반 오토스케일링, Karpenter는 Spot 인스턴스 자동 프로비저닝
- **Operator Pattern**: CRD(Custom Resource Definition)+Controller로 도메인 지식 코딩 (예: ArgoCD, Crossplane)

**4) L4 - 데이터 계층**: CAP 정리에 따라 **일관성(Consistency)·가용성(Availability)·분할 내성(Partition tolerance)** 중 2가지만 선택 가능하며, 클라우드 분산 시스템은 기본적으로 P를 선택한 뒤 AP(Cassandra, DynamoDB) 또는 CP(MongoDB 기본, ZooKeeper) 모델을 워크로드 특성에 따라 채택한다. DynamoDB Global Tables는 Multi-Region **멀티 마스터**로 10ms 레이턴시 Read/Write를 지원한다.

**5) L5 - 애플리케이션 패턴**:
- **Microservices**: 단일 책임(SRP), 독립 배포, 기술 다양성(Polyglot), **Domain-Driven Design(Bounded Context)** 기반 경계 설정. **SAGA 패턴**(Orchestration/Choreography)으로 분산 트랜잭션 처리.
- **Serverless(FaaS)**: Cold Start 100ms~1s 문제 해결을 위해 **Provisioned Concurrency(AWS Lambda)**, **SnapStart(Lambda + Firecracker)**, **Warm Pool** 적용.
- **Event-Driven Architecture**: Kafka(처리량 100만 msg/s), Kinesis, Pub/Sub + **이벤트 소싱(Event Sourcing) + CQRS**로 Read/Write 모델 분리.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 가상화** | 하드웨어 추상화, Multi-tenancy | KVM/Xen/Hyper-V, AWS Nitro Card, **vCPU:Memory 비율(1:2~1:8)**로 인스턴스 패밀리 분류(General/Burstable/Compute/Memory/Storage/GPU) |
| **스토리지 계층** | 데이터 영속성·내구성 | **S3 11 9s(99.999999999%) 내구성**, EBS gp3(3,000 IOPS, 125 MB/s), EFS(NFSv4), S3 Glacier(아카이빙 $0.00099/GB·월) |
| **네트워크 / VPC** | 논리적 격리·트래픽 제어 | VPC CIDR(/16~ /28), **Public/Private/Database 서브넷 3-Tier**, Security Group(상태저장), NACL(상태비저장), VPC Peering·Transit Gateway·PrivateLink |
| **오케스트레이터 (K8s)** | 컨테이너 라이프사이클 관리 | Control Plane(API Server, etcd, Scheduler, Controller Manager) + Worker Node(kubelet, kube-proxy, CRI), **etcd Raft 합의 알고리즘**(Leader Election, Log Replication) |
| **서비스 메시 (Istio)** | L7 트래픽 관리·mTLS·관측 | **Envoy Sidecar(1.18+ iptables -> eBPF)**, Control Plane(Pilot, Citadel, Galley), **Istio Ambient Mesh**(Sidecar 제거,ztunnel) |
| **옵저버빌리티** | Metrics·Logs·Traces 통합 | **OpenTelemetry(OTel) SDK + Collector**, Prometheus(시계열)+Thanos/Cortex(장기저장), Grafana(시각화), **3 Pillars 상관관계**: trace_id·span_id 전파 |
| **IaC / GitOps** | 인프라 선언적 정의·자동화 | Terraform(HCL 선언형, State Locking via DynamoDB), Pulumi(코드형), ArgoCD(K8s GitOps, **자동 Sync·Self-Heal·Drift Detection**) |
| **보안 / IAM** | 인증·인가·암호화 | **Zero Trust 모델**, IAM Role(OIDC + IRSA for EKS), KMS(CMEK), Secrets Manager, **CSPM(Prisma Cloud)·CWPP(Twistlock)·CIEM** |

### 핵심 알고리즘·파라미터

- **일관성 해시(Consistent Hashing)**: DynamoDB·Cassandra의 파티션 분배, 노드 추가/제거 시 키 재배치 비율 **1/N**로 최소화
- **Quorum Write/Read
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 630 / 800

<- **이전**: [629. 클라우드 아키텍처 핵심 토픽 629번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/629_cloud_architecture_core_topic_629_exam_summar/)
**다음**: [631. 클라우드 아키텍처 핵심 토픽 631번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/631_cloud_architecture_core_topic_631_exam_summar/) ->

---
