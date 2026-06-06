---
title: "Cloud Architecture Core Topic 705 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 **API 선언형 프로비저닝(Terraform/CloudFormation)**, **불변 인프라(AMI/Container Image)**, **12-Factor App**, **Saga/CQRS/Event Sourcing** 등 분산 시스템 패턴을 토대로, 컨트롤 플레인(Control Plane)과 데이터 플레인(Data Plane)을 분리해 셀프서비스형 탄력 리소스를 제공
> 2. **가치**: AWS Well-Architected 5대 필러 적용 시 CAPEX->OPEX 전환, Auto Scaling으로 피크 트래픽 30~70% 비용 절감, Multi-AZ + Circuit Breaker로 MTTR 90% 단축, MTTR 평균 4시간->15분 수준 달성 (Netflix/Amazon 사례 기준)
> 3. **판단 포인트**: **단일 클라우드(Single Cloud) vs 멀티/하이브리드**, **Monolith->Microservice 분할 경계(Bounded Context)**, **Strong Consistency vs Eventual Consistency**, **Cold Start 허용 latency budget**, **Egress 비용** 등 트레이드오프를 워크로드 SLO·데이터 주권·규제 요구사항 기준으로 판단

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 아키텍처는 **수직 확장(Scale-Up)**, **장기 납기 하드웨어 도입(6~12개월)**, **수동 Capacity Planning**, **수직 스택(Vendor Lock-in)** 이라는 제약으로 인해 디지털 트랜스포메이션 시대의 **비정형 트래픽, 글로벌 확장, 페타바이트급 데이터 처리 요구**를 감당하지 못합니다. Gartner 2024 보고서에 따르면, 글로벌 엔터프라이즈 IT 지출의 **65% 이상이 클라우드로 전환**되었고, 신규 애플리케이션의 **90% 이상이 클라우드 네이티브(Cloud-Native)** 방식으로 설계됩니다.

클라우드 아키텍처는 **가상화(Hypervisor->Container) -> 오케스트레이션(Kubernetes) -> 서버리스(FaaS) -> 엣지(Edge)** 로 발전해왔으며, 핵심 패러다임 전환은 다음과 같습니다.

| 패러다임 | 온프레미스 | 클라우드 |
|:---|:---|:---|
| 확장성 | Scale-Up(수직), 수개월 소요 | Scale-Out(수평), Auto Scaling 분 단위 |
| 장애 대응 | Cold Standby, MTTR 수 시간 | Multi-AZ/Region Active-Active, MTTR 분 단위 |
| 프로비저닝 | 수동 티켓/SoR(2~4주) | IaC(API/Terraform), 30초 이내 |
| 비용 모델 | CAPEX(감가상각) | OPEX(사용량 기반 Pay-as-you-go) |
| 데이터센터 | 자사 DC, 단일 리전 | 글로벌 30+ 리전, 100+ Edge Location |

```text
        클라우드 아키텍처 진화 흐름 (세대별 추상화 레벨)

  +--------------------------------------------------------------+
  |  G1. Bare Metal      : 물리 서버 단위, 하이퍼바이저(KVM/Xen)  |
  |  G2. IaaS (2006~)    : EC2, Azure VM, GCE - 가상머신 단위    |
  |  G3. PaaS (2010~)    : Heroku, App Engine, Beanstalk        |
  |  G4. CaaS (2014~)    : Docker + Kubernetes, ECS, EKS, AKS   |
  |  G5. FaaS (2014~)    : Lambda, Azure Functions, Cloud Run   |
  |  G6. Edge (2020~)    : Cloudflare Workers, Lambda@Edge      |
  +--------------------------------------------------------------+
       ^ 추상화 레벨 증가 ----►  ^ 관리 책임 감소 (CSP로 이관)
       ^ 제어력 감소       ----►  ^ 유연성/탄력성 증가
```

```text
        책임 공유 모델 (Shared Responsibility Model)

  +------------------------------------------+------------------+
  |              Customer (사용자 책임)       |  CSP 책임        |
  |  +------------------------------------+  |                  |
  |  | 데이터, IAM, OS 패치, 네트워크 ACL|  |  +-------------+ |
  |  | 클라이언트 측 암호화, 콘텐츠 보호  |  |  | 물리 시설   | |
  |  | 방화벽 설정, 보안그룹 룰           |  |  | 하드웨어    | |
  |  +------------------------------------+  |  | 네트워크    | |
  |  ----------- 책임 경계선 ----------- -► |  | 하이퍼바이저| |
  |  IaaS   : OS부터 사용자                  |  | 서비스      | |
  |  PaaS   : App/Config부터 사용자          |  +-------------+ |
  |  SaaS   : Data/IAM만 사용자              |                  |
  +------------------------------------------+------------------+
```

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"전기 요금제"**와 같습니다. 발전소(CSP)가 발전·송배전을 책임지고, 사용자는 콘센트에 꽂아 쓰는 **Pay-per-Use 모델**로, **한전에서 직접 발전기를 돌릴 필요가 없는** 것 처럼 IT 인프라를 빌려 쓰는 패러다임입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **컨트롤 플레인**과 **데이터 플레인**의 분리가 핵심입니다. 컨트롤 플레인은 리소스 상태/정책/API를 관리하고, 데이터 플레인은 실제 사용자 트래픽을 처리합니다. **Kubernetes**, **AWS API Gateway+Lambda**, **Service Mesh(Istio/Linkerd)** 가 모두 이 분리 원칙을 따릅니다.

```text
        클라우드 네이티브 시스템 아키텍처 (4계층 레이어링)

  +-------------------------------------------------------------+
  |  L7  Edge / Ingress  : CloudFront, Cloudflare, NLB, ALB    |
  +-------------------------------------------------------------+
  |  L6  API Gateway     : Kong, Apigee, AWS API Gateway       |
  |      - 인증(OAuth2/JWT), Rate Limit, Transformation        |
  +-------------------------------------------------------------+
  |  L5  Service Mesh    : Istio, Linkerd, Consul Connect        |
  |      - mTLS, Circuit Breaker, Traffic Split, Observability  |
  +-------------------------------------------------------------+
  |  L4  App Runtime     : Kubernetes Pod, Lambda, Cloud Run    |
  |      - HPA, PDB, Sidecar, Init Container                    |
  +-------------------------------------------------------------+
  |  L3  Stateful/Storage: RDS Aurora, DynamoDB, S3, EBS, RDS  |
  |      - Multi-AZ, Read Replica, Sharding, CDC(Debezium)     |
  +-------------------------------------------------------------+
  |  L2  Messaging/Async : SQS, Kafka, Pub/Sub, EventBridge    |
  |      - At-Least-Once, Dead Letter Queue, Backpressure      |
  +-------------------------------------------------------------+
  |  L1  Observability   : Prometheus, OpenTelemetry, Loki,    |
  |      - 3대 축: Logs / Metrics / Traces (RED/USE 메서드)    |
  +-------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **컴퓨트 (Compute)** | 비즈니스 로직 실행, 요청 처리 | **VM 계열**: EC2(m5/c6i/g5), Azure VM(Av2/D/E), **Container**: EKS(Managed K8s), GKE Autopilot, **Serverless**: Lambda(15분 timeout, 10GB mem), Azure Functions(Premium Plan), **Edge**: Cloudflare Workers(V8 Isolates) |
| **스토리지 (Storage)** | 데이터 영속성, Object/Block/File/Archive | **Object**: S3(11 9s 내구성, 99.99% 가용성), Azure Blob(Access Tier: Hot/Cool/Archive), **Block**: EBS gp3(io2 64TB, 256K IOPS), **File**: EFS( NFS 4.1), FSx for Lustre(100GB/s+), **Key-Value**: DynamoDB(Global Tables), Cosmos DB(Multi-Master) |
| **네트워크 (Network)** | L3/L4/L7 라우팅, 글로벌 백본 | **VPC**: AWS(IPv4/IPv6 Dual Stack, 5개 CIDR/100+), Azure VNet, GCP VPC(Global), **Hybrid**: Direct Connect(1/10/100Gbps), Transit Gateway(5000 VPC Peering), **CDN**: CloudFront(4500+ PoP), **Load Balancer**: NLB(L4, 초당 수백만 pps), ALB(L7, gRPC/HTTP2/WebSocket) |
| **데이터베이스 (DB)** | 트랜잭션, 분석, 캐시 | **RDBMS**: Aurora MySQL(Read Replica 15개, Lag < 100ms), **NoSQL**: DynamoDB(DynamoDB Streams, PITR 35일), **NewSQL**: CockroachDB, TiDB(HTAP), **인메모리**: ElastiCache(Redis Cluster, 73GB/노드), **검색**: OpenSearch/Elasticsearch |
| **보안/거버넌스 (Sec/Gov)** | 인증, 암호화, 감사, 컴플라이언스 | **IAM**: AWS IAM(RBAC+ABAC), Azure AD(Conditional Access), **KMS**: Envelope Encryption, BYOK, HSM, **감사**: CloudTrail, Config(규정 준수), **비밀**: Secrets Manager, HashiCorp Vault(KV v2), **WAF**: AWS WAF, Cloudflare Bot Mgmt |
| **옵저버빌리티 (Observability)** | Logs/Metrics/Traces, AIOps | **메트릭**: Prometheus + Thanos/Cortex, CloudWatch, **로그**: Loki, ELK, **트레이스**: Jaeger, Zipkin, OpenTelemetry SDK, **APM**: Datadog, New Relic, Dynatrace, **SRE**: SLI/SLO/Error Budget 기반 알람 |

```text
        Kubernetes Pod 라이프사이클 & 핵심 컨트롤 루프

   +-------------+    kubectl apply    +-----------------+
   |  kubectl/   | -----------------► |  API Server     |
   |  Helm/Argo  |   (YAML 매니페스트) |  (etcd 저장)     |
   +-------------+                     +--------+--------+
                                                | watch
                                                v
   +------------------------------------------------------+
   | kube-controller-manager  (Reconcile Loop)             |
   |  - Deployment Controller: replicas = spec            |
   |  - StatefulSet: PVC + Stable Network ID              |
   |  - HPA: CPU>70% -> Replica +1 (3분 안정 윈도우)      |
   |  - PDB: minAvailable=80% (자율적 격리 제한)          |
   +------------------------------------------------------+
                                                |
                                                v
   +--------------+  kubelet  +------------------------+
   |  Scheduler   | ◄------- |  Node (kubelet)         |
   |  - binpack   |  ------► |  - cgroup/CPU/Mem Limit |
   |  - spread    |  exec    |  - readinessProbe       |
   |  - taints    |          |  - livenessProbe        |
   +--------------+          +------------------------+

   컨트롤 루프 = "Observe -> Diff -> Reconcile" ( 선언형 API 핵심 )
```

```text
        마이크로서비스 간 트랜잭션 정합성: Saga 패턴 (Orchestration)

  +--------+  HTTP  +----------+  gRPC  +----------+  SQL   +--------+
  |  Client| ----► | Order    | ----► | Payment  | ----► |Pay DB  |
  +--------+       | Service  |        | Service  |        +--------+
                   |(Orchestr)|        +-----+----+
                   +----+-----+              | success
                        | 1.주문생성           v
                        | 2.결제요청    +----------+
                        |               |Inventory | --► Stock DB
                        |               | Service  |
                        |               +----+-----+
                        v                    | fail
                   +--------+  ◄--- 보상트랜잭션 --+
                   | Compens|  결제취소 / 주문취소
                   | ation  |
                   +--------+
   ※ ACID 2PC 대신, 최종 일관성(Eventual Consistency) 수용
   ※ 2PC 대비 가용성^, latencyv, but 디버깅 난이도^
```

```text
        Well-Architected Framework 6대 필러 (AWS 기준)

  +------------+ +----------+ +----------+ +----------+
  | 운영 우수성 | |  보안    | |  안정성  | | 성능효율  |
  |(Ops Excel.)| |Security  | |Reliab.   | |Perf.Eff. |
  +----+-------+ +----+-----+ +----+-----+ +----+-----+
       | Code/Deploy  | IAM/Enc   | Multi-AZ  | 선택/Caching
       | 모니터링     | 최소권한  | CircuitBr | 비동기
       |              | 추적성    | Chaos Eng | 선택 알고리즘
  +----+-----------+ +------+----------------------------+
  |  비용 최적화    | |  지속가능성(Sustainability, 2021+)|
  | Cost Optim.    | |  - 리전별 탄소 강도 고려          |
  | - RI/Savings   | |  - 워크로드 지역 매칭으로         |
  | - Spot/RightS  | |    네트워크 전력 최소화            |
  +----------------+ +-----------------------------------+
```

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"우주정거장(ISS) 모듈"**과 같습니다. 각 모듈(마이크로서비스)이 독립적으로 교체/수리 가능하고, 중앙 관제실(Control Plane)이 모듈 상태를 모니터링하며, 한 모듈 손상 시 산소 차단 격리(Bulkhead)되는 방식으로 **단일 실패가 전체를 무너뜨리지 않도록 설계**합니다.

---

## Ⅲ. 비교 및 연결

### 1) 컴퓨트 추상화 레벨 비교

| 구분 | VM (EC2) | Container (ECS/EKS) | Serverless (Lambda) | Edge (Workers) |
|:---|:---|:---|
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 705 / 800

<- **이전**: [704. 클라우드 아키텍처 핵심 토픽 704번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/704_cloud_architecture_core_topic_704_exam_summar/)
**다음**: [706. 클라우드 아키텍처 핵심 토픽 706번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/706_cloud_architecture_core_topic_706_exam_summar/) ->

---
