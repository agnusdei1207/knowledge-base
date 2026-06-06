---
title: "Cloud Architecture Core Topic 690 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS의 책임 분담 모델, Multi-AZ·Multi-Region 가용성 설계, 12-Factor·Cloud-Native 원칙, MSA·Service Mesh·서버리스 기반의 탄력적 분산 시스템을 통해 "필요한 만큼, 필요한 때, 필요한 곳" 컴퓨팅 자원을 동적 프로비저닝하는 Stateless·API 중심 인프라 패러다임이다.
> 2. **가치**: Auto Scaling으로 트래픽 10배 급증에도 가용성 99.99%(Four Nine) 유지, Pay-per-Use로 TCO 30~60% 절감, Global Edge로 사용자 레이턴시 200ms->20ms 단축, MTTR을 기존 대비 70% 이상 단축하여 비즈니스 연속성과 민첩성을 동시에 확보한다.
> 3. **판단 포인트**: Shared Responsibility Model 경계(고객/OS미들웨어/데이터·IAM), 단일 클라우드 종속(Vendor Lock-in) vs Multi-Cloud·Interoperability, CAP 정리를 기반으로 한 Consistency vs Availability 트레이드오프, 비용 최적화(FinOps)와 SLA 등급(SLA 99.9/99.95/99.99) 간 균형을 설계자의 핵심 판단기준으로 삼아야 한다.

---

## Ⅰ. 개요 및 필요성

전통적 On-Premise 아키텍처는 CAPEX 중심의 수직적 확장(Scale-Up)·모놀리식 애플리케이션·정적 용량 계획(Static Capacity Planning)에 머물러 트래픽 변동성과 글로벌 사용자 요구에 즉응하지 못하는 한계를 보였다. 2006년 AWS S3·EC2 출시 이후 클라우드 컴퓨팅은 인프라의 **추상화(Abstraction)**·**자동화(Orchestration)**·**탄력성(Elasticity)**을 통해 IT 자산을 "코드처럼" 선언적으로 다루는 패러다임(IDC 2023, Gartner Magic Quadrant for Cloud 2024)으로 전환되었다.

클라우드 아키텍처의 본질적 도전 과제는 (1) **탄력적 자원 공급**(Elasticity), (2) **무중단 서비스**(High Availability), (3) **글로벌 확장성**(Geo-Distribution), (4) **운영 자동화**(DevOps/GitOps), (5) **비용-성능 최적화**(FinOps), (6) **제로 트러스트 보안**(BeyondCorp)이다. 이를 위해 Well-Architected Framework(AWS 5대 pillar: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization)와 Cloud Center of Excellence(CCoE) 거버넌스가 요구된다.

```text
[클라우드 아키텍처 진화 흐름]

  1980~2000        2000~2010         2010~2015         2015~2020         2020~현재
   +------+         +------+         +------+         +------+         +------+
   |메인프레임| --->   |클라이언트| --->   |  IaaS | --->   |PaaS/ | --->   |Server|
   |모놀리식 |     |서버    |     | (EC2) |     |컨테이너|     |less/ |
   |Scale-Up|     |  3-Tier|     |Hyperv |     |K8s/Istio|    |Mesh |
   +------+         +------+         +------+         +------+         +------+
      CAPEX            CAPEX+            OPEX            OPEX            Usage-
     중심              가상화           시작            MSA+DevOps        based
   IDC 자가운영      IDC(VMware)     AWS/Azure       Docker/K8s       Lambda/Cloud Run
                                                                      FinOps/AI옵스
```

**왜 클라우드 아키텍처인가?**
- **비즈니스 민첩성**: 인프라 프로비저닝 시간 4~8주 -> 5분(CloudFormation/Terraform IaC)
- **글로벌 도달성**: 1개 Region -> 30+ Region, 600+ Edge Location으로 단시간 내 글로벌 서비스 출시
- **TCO 전환**: CAPEX(전액 선투자) -> OPEX(사용량 과금), 유휴 자원 제로화
- **내장 거버넌스**: KMS, IAM, WAF, GuardDuty 등 컴플라이언스 자동화
- **이중화 자동화**: Multi-AZ, Multi-Region Failover를 매니지드 서비스로 제공

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **"전기 그리드"**와 같다. 과거에는 각 가정·공장이 자가발전기를 돌렸지만(전용发电机), 지금은 전력회사(공급자)가 송배전망과 안정성을 책임지고, 우리는 콘센트(API)에 꽂기만 하면 된다. 사용량(kWh)에 따라 요금이 자동 정산되고, 정전이 생기면 예비 회선으로 자동 전환된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 크게 **(1) 서비스 모델 계층, (2) 글로벌 인프라 토폴로지, (3) 분산 시스템 패턴, (4) Cloud-Native 컴퓨트 런타임, (5) 관측·보안·비용 통제 평면**의 5개 레이어로 구성된다.

```text
[클라우드 아키텍처 5-Layer 참조 모델]

  +--------------------------------------------------------------------------+
  |  L5. 거버넌스 평면 (Governance & FinOps)                                  |
  |  - AWS Organizations / Azure Policy / GCP Org Policy                     |
  |  - Cost Explorer, Budgets, RI/SP, Savings Plan, CUR, CUDOS               |
  +--------------------------------------------------------------------------+
  |  L4. 관측·보안 평면 (Observability & Security)                            |
  |  - Observability: Prometheus/Grafana/ELK/CloudWatch/X-Ray/CloudTrace    |
  |  - Security: IAM, KMS, WAF, GuardDuty, Security Hub, CSPM, SIEM         |
  +--------------------------------------------------------------------------+
  |  L3. 분산 시스템 패턴 (Distributed Patterns)                              |
  |  - L4/L7 LB, Service Mesh(Istio/Linkerd), API Gateway, Circuit Breaker  |
  |  - CQRS, Event Sourcing, Saga, Bulkhead, Sidecar, Ambassador             |
  +--------------------------------------------------------------------------+
  |  L2. 컴퓨트 런타임 (Compute Runtime)                                      |
  |  - IaaS: EC2/VM, PaaS: App Service/Cloud Run                            |
  |  - CaaS: EKS/AKS/GKE(Managed K8s), ECS/Container Apps                   |
  |  - FaaS: Lambda/Azure Functions/Cloud Functions                          |
  +--------------------------------------------------------------------------+
  |  L1. 글로벌 인프라 (Global Infrastructure)                               |
  |  - Region(리전) -> AZ(가용영역 3개+) -> Edge Location/PoP                  |
  |  - 글로벌 백본 네트워크: AWS Global Accelerator, Azure Front Door         |
  |  - 저장: S3 Multi-Region, GCS Multi-Region, Cosmos DB Multi-Region Write |
  +--------------------------------------------------------------------------+
```

### 서비스 모델별 책임 분담 (Shared Responsibility Model)

| 계층 | On-Premise | IaaS | PaaS | SaaS | FaaS |
|:---|:---:|:---:|:---:|:---:|:---:|
| Application | 고객 | 고객 | 고객 | 공급자 | 고객 |
| Data | 고객 | 고객 | 고객 | 공급자 | 고객 |
| Runtime / Middleware | 고객 | 고객 | 공급자 | 공급자 | 공급자 |
| OS | 고객 | 고객 | 공급자 | 공급자 | 공급자 |
| Virtualization | 고객 | 공급자 | 공급자 | 공급자 | 공급자 |
| Server / Storage / Network HW | 고객 | 공급자 | 공급자 | 공급자 | 공급자 |

### 배포 모델 및 토폴로지

```text
[클라우드 배포 모델 아키텍처]

   (a) Public Cloud              (b) Private Cloud
   +--------------+              +--------------+
   |  CSP 계정    |              |  자가/호스팅 |
   | +----------+ |              | +----------+ |
   | | VPC/VNet | |              | |OpenStack | |
   | | Public  | |              | | VMware   | |
   | |Subnet   | |              | |  Tanzu   | |
   | +----------+ |              | +----------+ |
   +--------------+              +--------------+

   (c) Hybrid Cloud              (d) Multi-Cloud
   +--------------+              +--------------+
   | On-Premise   |<--VPN/DEX---->| Public       |
   | + Burst to   |              | AWS + Azure  |
   | Public       |              | (Interconnect|
   +--------------+              |  + Cross-Cloud|
                                 |  K8s Federation)|
                                 +--------------+
```

### 핵심 컴포넌트 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Region / AZ** | 지리적 격리·동기 복제 단위 | Region 내 AZ 3개 이상 독립 DC(수 km 분리), 99.99% SLA. AWS 32+ Region, Azure 60+ Region, GCP 38+ Region 운영 |
| **가상 네트워크(VPC/VNet)** | 논리적 사설망, 서브넷 라우팅 | 10.0.0.0/16 CIDR, Public/Private/Isolated Subnet, Route Table, NAT GW, IGW, Transit GW, VPC Peering, PrivateLink |
| **컴퓨트(Compute)** | 워크로드 실행 런타임 | (1) VM: M7i·C7g·D-Series (Intel/AMD/ARM Graviton) (2) Container: ECS·EKS·AKS·GKE·Container Apps (3) Serverless: Lambda(15분), Fargate, Cloud Run(60분), Azure Functions(무제한 Durable) |
| **스토리지** | 데이터 영속성 | (1) Object: S3(11 9s 내구성, 99.99 가용성), GCS, Blob (2) Block: EBS io2(64TB, 256K IOPS) (3) File: EFS, FSx(Lustre/NetApp) (4) Cold: S3 IA, Glacier(분~12hr 회수) |
| **데이터베이스** | 트랜잭션·분석·벡터 | RDB: Aurora MySQL/PostgreSQL 5x, Cosmos DB(글로벌 분산 Multi-Master, 5가지 Consistency), Spanner. NoSQL: DynamoDB(싱글 Digit ms, 40K+ TPS/Partition), Cassandra. 분석: Redshift·Snowflake·BigQuery(Separation of Storage/Compute), Vector: Pinecone·pgvector·Vertex AI Vector Search |
| **로드밸런서** | 트래픽 분산·헬스체크 | L4: NLB(UDP·TCP, 100만+ TPS), L7: ALB(라우팅, WAF 통합), 글로벌: GLB/CloudFront/Front Door. 알고리즘: RR, LC, LRT(Least Response Time), IP-hash, Consistent Hash |
| **메시지/이벤트 버스** | 비동기 결합·이벤트 스트림 | Kafka(Multi-Producer·Partitioned Log, ISR), Kinesis·Pub/Sub(At-Least-Once), SQS(Standard/FIFO), EventBridge(Schema Registry, Event Bus), NATS JetStream |
| **캐시/인메모리** | 핫 데이터 가속 | Redis(Cluster Mode, AOF), Memcached, ElastiCache·Memorystore·Azure Cache. 80% Read 워크로드에서 DB 부하 90%v |
| **API Gateway / Service Mesh** | 인증·라우팅·관측 | API GW: Kong·Apigee·AWS API Gateway(Usage Plan, Throttle). Service Mesh: Istio(Envoy Sidecar, mTLS, Traffic Mgmt), Linkerd, App Mesh |
| **IaC/오케스트레이션** | 선언적 자원 관리 | Terraform(HCL, State Lock), Pulumi, CloudFormation, Ansible, ArgoCD(GitOps), Crossplane(K8s-native) |
| **관측(Observability)** | 3대 신호 측정 | Metrics: Prometheus·CloudWatch. Logs: ELK·OpenSearch·Loki. Traces: Jaeger·Zipkin·X-Ray·OpenTelemetry(OTLP). RED(요청률·에러·지속시간), USE(활용·포화·에러) |
| **보안/IAM** | Zero Trust 통제 | IAM(RBAC·ABAC), KMS/HSM(Envelope Encryption), Secrets Manager(Vault), WAF(OWASP Top10), GuardDuty/Defender, MFA·FIDO2, CSPM·CWPP·CIEM |
| **FinOps** | 비용 가시화·최적화 | Cost Allocation Tag, RI/SP 1·3년 약정 30~60%v, Spot/Preemptible 70~90%v, Auto Scaling, Right-Sizing, Graviton ARM 40%v TCO, CUR(FOCUS) |

### 핵심 알고리즘·파라미터

**(1) Auto Scaling 정책**
- **Target Tracking**: CPU 60% 유지 등 목표 기반
- **Step Scaling**: 임계치 기반 단계적 증감 (예: 70%->+2, 85%->+4)
- **Predictive Scaling**: 시계열(예: 14일) 기반 사전 확장
- **Scheduled**: cron(예: 매주 월 09:00 KST)

**(2) CAP 정리 (Brewer, 2000) — 분산 트레이저드오프**
- **CA**: 전통 RDBMS(PostgreSQL with 동기 복제) — 단일 Region 한정
- **CP**: HBase, etcd, MongoDB(WriteConcern=majority) — 정합성 우선, 분할 시 가용성v
- **AP**: Cassandra, DynamoDB, Cosmos DB(Eventual/LWW) — 가용성 우선

**(3) Consistency 모델 5단계 (Cosmos DB 기준)**
Strong -> Bounded Staleness(임계 시간) -> Session(클라 모노톤) -> Consistent Prefix -> Eventual

**(4) Sharding 전략**
- Hash Sharding(균등, 리샤딩 비용 大)
- Range Sharding(범위 질의 유리, 핫스팟)
- Lookup/Entity Group(tenant_id 기반, SaaS 멀티테넌시)
- Consistent Hashing(Memcached·DynamoDB Partition Key 256 hash slot)

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"국제 항공 허브 공항"**과 같다. 각 공항(Region) 안에 활주로(AZ)가 3개 이상 있어 한 활주로가 폐쇄돼도 이륙·착륙이 멈추지 않고, 관제탑(Control Plane)이 실시간으로 비행기(트래픽)를 분산 배정한다. 게이트(API Gateway)·라운지(Service Mesh)·화물 시스템(Storage)·연료(FinOps)·보안검색(Security) 모두가 자동화되어 한 비행기의 결항이 전체 시스템 정지로 이어지지 않는다.

---

## Ⅲ. 비교 및 연결

###
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 690 / 800

<- **이전**: [689. 클라우드 아키텍처 핵심 토픽 689번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/689_cloud_architecture_core_topic_689_exam_summar/)
**다음**: [691. 클라우드 아키텍처 핵심 토픽 691번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/691_cloud_architecture_core_topic_691_exam_summar/) ->

---
