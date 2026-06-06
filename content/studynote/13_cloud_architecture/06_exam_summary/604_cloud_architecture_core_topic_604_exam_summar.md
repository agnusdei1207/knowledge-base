---
title: "Cloud Architecture Core Topic 604 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

# 604. 클라우드 아키텍처 핵심 토픽 604번 시험 요약

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 퍼블릭/프라이빗/하이브리드/멀티 클라우드 환경에서 컴퓨팅·스토리지·네트워크를 코드(IaC)로 선언하고, 컨트롤 플레인(API/Kubernetes/IAM)과 데이터 플레인(CNI/CNI/CSI)을 분리하여 탄력성(Elasticity), 회복탄력성(Resilience), 관측가능성(Observability)을 SLA로 보장하는 12-Factor + Well-Architected 기반의 분산 시스템 청사진이다.
> 2. **가치**: Auto-Scaling을 통해 트래픽 10배 변동 시 Capacity 비용 35~60% 절감, Multi-AZ/Multi-Region 구성으로 RTO < 1분/RPO < 1초 달성, IaC(Terraform/CloudFormation) 적용 시 환경 provisioning 시간 90% 단축(수동 2주 -> 자동 30분) 및 구성 편차(Configuration Drift) 제거.
> 3. **판단 포인트**: (a) Shared Responsibility Model 경계 — IaaS는 OS·미들웨어부터, SaaS는 데이터·접근권한까지 CSP 책임이 아닌 영역 식별, (b) Vendor Lock-in 회피 시 Karpenter+Spot+EKS Anywhere 멀티클라우드 vs CSP 종속(AWS-native) 간의 TCO 트레이드오프, (c) CAP/PACELC 관점에서 Consistency vs Availability 우선순위 결정(RDBMS 강결합 vs DynamoDB/Cassandra Eventually Consistent).

---

## Ⅰ. 개요 및 필요성

클라우드 컴퓨팅은 NIST SP 800-145 정의에 따라 "네트워크, 서버, 스토리지, 애플리케이션, 서비스 등 구성 가능한 컴퓨팅 자원의 공유 풀(Shared Pool)에 대해 어디서나 편리한 온디맨드 네트워크 접근을 가능하게 하는 모델"이다. 2006년 AWS S3·EC2 출시 이후 18년간演进해왔으며, 현재는 Hyperscaler 3사(AWS 32%·Azure 23%·GCP 11%, Synergy 2024Q4 기준)가 전체 IaaS 시장의 66%를 점유한다.

**전통적 온프레미스 아키텍처의 한계**:
- **Capacity Planning 실패**: Netflix 사례(2008년 데이터베이스 손상)처럼 Peak 기반 과잉 설비(평균 활용률 15~20%)로 자본 지출(CapEx) 낭비
- **Time-to-Market 지연**: 신규 서비스 인프라 준비에 평균 6~13주 소요 (요구사항->발주->입고->설치->테스트)
- **재해복구(DR) 비용**: 핫사이트 유지 비용이 본계 시스템의 80~120%에 달함
- **글로벌 확장 불가**: 리전별 데이터센터 신규 구축에 12~24개월, 1,000억 원 이상의 초기 투자

**클라우드 패러다임 전환의 3대 축**:
1. **CapEx -> OpEx 전환**: 사용한 만큼만 지불(Pay-As-You-Go), 1분 단위 과금·秒 단위 Provisioning
2. **수직적 규모(Scale-Up) -> 수평적 규모(Scale-Out)**: 단일 고가 장비 -> Commodity HW + 분산 소프트웨어
3. **수동 운영 -> 셀프서비스 API**: 콘솔 클릭 -> Terraform/SDK/Ansible 코드화, GitOps 기반 선언적 배포

```text
+---------------------------------------------------------------------+
|                  Cloud Computing Evolution Timeline                  |
+---------------------------------------------------------------------+
| 1960s         1990s           2006         2014         2020+      |
| Mainframe  ---> ASP/Hosting ---> AWS EC2 ---> K8s 1.0 ---> Serverless|
| (Time-share)   (Colocation)    (IaaS)      (CaaS)        (FaaS)    |
|                                v             v             v       |
|                             Virtual     Container    Event-driven  |
|                             Machine     Orchestration  Functions   |
|                                                                      |
|  2006: AWS S3, EC2      2009: GCP      2010: Azure    2011: OpenStack|
|  2013: Docker           2014: K8s      2017: Lambda   2019: Istio  |
|  2020: eBPF, Wasm       2021: Karpenter  2023: GenAI  2024: FinOps |
+---------------------------------------------------------------------+
        +-------------------------------------------------+
        |  Shared Responsibility Model (NIST/SP 800-144)   |
        |  "클라우드 위의 것(Customer)"과 "클라우드 자체"   |
        |          의 책임을 CSP와 고객이 공동 분담          |
        +-------------------------------------------------+
```

**왜 "아키텍처"가 핵심인가**: 단순한 VM/Lift&Shift는 클라우드 도입 효과의 15%만 활용한다는 Gartner 분석(2023)이 있으며, 진짜 가치는 Cloud-Native 리팩토링, 마이크로서비스, 분산 데이터 패턴을 적용할 때 발생한다. 12-Factor App, AWS Well-Architected Framework(5대 기둥: Operational Excellence·Security·Reliability·Performance Efficiency·Cost Optimization), Google SRE Book의 SLI/SLO/Error Budget 개념이 아키텍처 설계의 표준으로 자리잡았다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"호텔 체인 프랜차이즈 운영 노하우"** 와 같다. 매번 신축(데이터센터)하는 게 아니라, 예약 시스템(API)·룸 키 발급(IAM)·하우스키핑(Managed Service)·체인 본사 표준화(Well-Architected)를 갖춘 호텔에 투숙객(애플리케이션)이 빈 방(리소스)만 골라入住하는 형태다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **5계층(Governance->Application->Platform->Infrastructure->Facility)** 의 논리적 분리와 **3축(보안·네트워크·데이터)** 의 횡단 관심사(Cross-Cutting Concerns)로 구성된다. 핵심은 **제어 평면(Control Plane)** 과 **데이터 평면(Data Plane)** 의 분리다.

```text
+---------------------------------------------------------------------+
|            Reference Architecture: 4-Tier Cloud-Native Stack        |
+---------------------------------------------------------------------+
|  Layer 1: Presentation & Edge                                       |
|  +--------------------------------------------------------------+ |
|  | CloudFront/Cloud CDN | WAF | Route 53/Cloud DNS | Global Acc. | |
|  |   (Anycast, TLS 1.3, DDoS Shield, GeoDNS Latency-based)     | |
|  +--------------------------------------------------------------+ |
|  Layer 2: Application & API                                         |
|  +--------------------------------------------------------------+ |
|  | ALB/NLB -> API Gateway -> Microservices (EKS/AKS/GKE)         | |
|  | Spring Cloud · Istio Service Mesh · Lambda/Cloud Functions    | |
|  | BFF · GraphQL Federation · EventBridge · Pub/Sub · Kafka     | |
|  +--------------------------------------------------------------+ |
|  Layer 3: Data & Storage                                            |
|  +--------------------------------------------------------------+ |
|  | RDBMS(ProxySQL) | NoSQL(DynamoDB/Cassandra/MongoDB)         | |
|  | Cache(ElastiCache/Redis) | Object(S3/Blob) | Search(OpenSearch)||
|  | Data Lake(S3+Glue+Athena) | Lakehouse(Iceberg/Delta)        | |
|  +--------------------------------------------------------------+ |
|  Layer 4: Infrastructure & Runtime                                  |
|  +--------------------------------------------------------------+ |
|  | Compute(EC2/VMSS) | Containers(EKS/GKE) | Serverless(Lambda) | |
|  | Network(VPC/VNet, TGW, PrivateLink, Direct Connect)          | |
|  | Storage(EBS/Managed Disks, EFS, FSx) | KMS/HSM               | |
|  +--------------------------------------------------------------+ |
|  Layer 5: Governance & Observability (X-cutting)                    |
|  +--------------------------------------------------------------+ |
|  | IAM · CloudTrail · Config · Security Hub · GuardDuty          | |
|  | Prometheus · Grafana · Loki · Jaeger · OpenTelemetry          | |
|  | Terraform · Pulumi · ArgoCD · Backstage (IDP)                 | |
|  +--------------------------------------------------------------+ |
+---------------------------------------------------------------------+

        +----------------------------------------------+
        |     Control Plane vs Data Plane 분리         |
        |  +--------------+    +------------------+    |
        |  | Control Plane |    |  Data Plane       |   |
        |  |  (뇌/명령)    |    |  (근육/실행)     |    |
        |  | • API Server  |    | • kubelet         |   |
        |  | • Scheduler   |    | • CNI (Cilium)    |   |
        |  | • IAM AuthN/Z |    | • CSI Driver      |   |
        |  | • HSM/KMS     |    | • Envoy Sidecar   |   |
        |  | 결정: "무엇을  |    | 실행: "실제 트래픽|   |
        |  |   어디서"     |    |   포워딩/처리"    |   |
        |  +--------------+    +------------------+    |
        +----------------------------------------------+
```

### 1. 컴퓨트 추상화 (Compute Abstraction) 4단계

| 계층 | 추상화 수준 | 책임 경계 | 대표 기술 | 스케일 단위 | 콜드 스타트 |
|------|------------|----------|----------|------------|------------|
| **IaaS** | VM/Hypervisor | OS^ 고객, HWv CSP | EC2, Azure VM, Compute Engine, Firecracker microVM | 1분 | 30~60초 |
| **CaaS** | Container | Runtime^ 고객, Clusterv CSP | EKS/AKS/GKE, ECS, Fargate, Nomad | 10초 | 5~10초 (이미지 캐시) |
| **PaaS** | Application Runtime | Code/DATA 고객, Platform CSP | App Engine, Beanstalk, Heroku, Cloud Run | 1초 | 1~3초 |
| **FaaS** | Function | 함수 코드 + 트리거 | Lambda, Azure Functions, Cloud Functions, Knative | 100ms | 50~500ms |

### 2. 핵심 구성 요소 및 동작 메커니즘

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Hypervisor (Type-1)** | 물리 HW를 다수의 VM으로 가상화, 자원 격리 및 과할당(Over-commit) | KVM(리눅스 커널 통합), Xen(AWS 초기), VMware ESXi, MS Hyper-V. **Nested Virtualization**(L1에서 L2 VM 실행) 지원 여부가 Bare-Metal 워크로드(K8s, RDMA) 가능 여부 결정 |
| **VPC/VNet (Virtual Private Cloud)** | 논리적 사설 네트워크, SDN 기반의 L2/L3 분리 | RFC 1918 CIDR(10.0.0.0/8, 172.16/12, 192.168/16), Public/Private Subnet, Route Table, NACL(Stateless), Security Group(Stateful), Transit Gateway(Hub-Spoke), VPC Peering vs TGW(전 트래픽 50Gbps 한계) |
| **IAM (Identity & Access Management)** | 인증(AuthN)·인가(AuthZ)·감사(Audit) 3A | AWS IAM Policy JSON: `Effect·Action·Resource·Condition` 4-tuple, ABAC(Attribute: `aws:PrincipalTag/team=dev`), RBAC(Role-based), PBAC(Policy-based). SCP(Service Control Policy)로 OU(Org Unit) 단위 권한 상한선 봉인 |
| **Object Storage (S3)** | 11 9s 내구성(99.999999999%)를 위한 분산 스토리지 | 데이터 3개 AZ에 자동 복제, **Erasure Coding**(Reed-Solomon, 4+2 -> 1.5배 저장 오버헤드 vs 3복제 3배), Versioning + Object Lock(WORM, 컴플라이언스), Lifecycle Policy(IA->Glacier 180일, Deep Archive 365일) |
| **Managed Kubernetes** | 컨테이너 오케스트레이션 표준(CNCF 졸업) | K8s 1.30+: Sidecar Container, Stable Structured Authorization, Pod Sandbox(런타임 gVisor/Kata). Control Plane HA(etcd Raft 합의, 3/5 Quorum), CNI 분리(Cilium·eBPF로 kube-proxy 대체) |
| **Observability 3-Pillar** | 시스템 상태 측정 및 인과관계 추론 | Metrics(Prometheus·Cortex·Thanos, 시계열 DB), Logs(Loki·ELK·OpenSearch), Traces(Jaeger·Tempo·Zipkin, OpenTelemetry SDK/W3C TraceContext 분산 컨텍스트 전파). RED(Req/Error/Duration)·USE(Utilization/Saturation/Error) 방법론 |
| **Serverless/FaaS** | 이벤트 기반 stateless 함수 실행, ms 단위 과금 | Lambda: 동기(API GW), 비동기(SQS/SNS), EventSource Mapping(Kinesis/DynamoDB Streams). 한도 1000 동시, /tmp 512MB, 15분 타임아웃, 10GB 메모리(1.8GHz vCPU 비례) |

### 3. 핵심 알고리즘/패턴

- **Consistent Hashing**: DynamoDB/Cassandra/Memcached가 데이터를 N개 노드에 분산 저장할 때, 노드 추가/제거 시 재배치되는 키 비율을 1/N으로 최소화. **Virtual Node(VNode)** 를 노드당 128~256개 할당하여 부하 편향 해결.
- **Raft 합의 알고리즘**: etcd/Consul/K8s가 사용하는 Leader Election + Log Replication. 3~5 노드 클러스터에서 Quorum(과반수) 기반 Commit, 네트워크 분할 시 Split-Brain 방지. **PreVote** 단계로 비잔틴 노드의 Election Storm 억제.
- **Leader/Follower Replication**: RDS Multi-AZ, Kafka 파티션 리더. 동기 복제(Quorum=2, RPO=0, Latency +10ms) vs 비동기(RPO=수초, Latency 동일).
- **CQRS + Event Sourcing**: 쓰기(Command)와 읽기(Query) 모델
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 604 / 800

<- **이전**: [603. 클라우드 아키텍처 핵심 토픽 603번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/603_cloud_architecture_core_topic_603_exam_summar/)
**다음**: [605. 클라우드 아키텍처 핵심 토픽 605번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/605_cloud_architecture_core_topic_605_exam_summar/) ->

---
