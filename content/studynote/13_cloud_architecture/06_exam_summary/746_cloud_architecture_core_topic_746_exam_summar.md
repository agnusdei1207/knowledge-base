---
title: "746. 클라우드 아키텍처 핵심 토픽 746번 시험 요약 (Cloud Architecture Core Topic 746 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: API 기반의 셀프서비스 프로비저닝과 선언적 인프라(IaC)를 통해 컴퓨트·스토리지·네트워크를 정책(Policy)·규약(Governance) 단위로 추상화하여, 다중 AZ/리전 확장이 가능한 탄력적 분산 시스템 토폴로지
> 2. **가치**: CAPEX->OPEX 전환으로 초기 인프라 투자 60~80% 절감, Auto-Scaling으로 Peak 트래픽 10배까지 흡수, Multi-AZ 구성 시 99.99%(Four-Nines) 가용성, 배포 주기 1주->1일 단축
> 3. **판단 포인트**: Stateful(데이터베이스) ↔ Stateless(API) 워크로드 분리, 동기식 강한 일관성 ↔ 비동기식 최종 일관성(Eventual Consistency) 트레이드오프, 단일 클라우드 종속(Vendor Lock-in) vs 멀티/하이브리드 운영 복잡도 비용 간 의사결정

---

## Ⅰ. 개요 및 필요성

전통적 3-Tier 온프레미스 아키텍처는 트래픽 변동에 대응하기 위해 Peak Load 기준으로 과다 용량을 사전 확보해야 하므로 평균利用率 15~25%에 그쳤으며, 신규 서비스 배포에 평균 4~8주의 HW 조달·설치·테스트 사이클이 요구되었다. 또한 자연재해·전원 장애·랜섬웨어 등 BCP 리스크에 대한 DR(Disaster Recovery) 사이트 구축 비용이 부담이었다.

클라우드 아키텍처는 AWS(2006), GCP(2008), Azure(2010) 이후 20년간 5단계로 진화했다: ① 가상화(IaaS) -> ② 매니지드 서비스(PaaS) -> ③ 컨테이너 오케스트레이션(K8s, 2015) -> ④ 서버리스/FaaS(Lambda, 2014) -> ⑤ 클라우드 네이티브 + Service Mesh(Istio, 2017~). 이러한 패러다임 전환은 Netflix의 2008년 DB 장애를 계기로 AWS 전면 전환(2016년 완료, 700여 마이크로서비스 운영), Capital One의 클라우드 마이그레이션(2018년 기준 80% AWS), 한국 카카오의 클라우드 전환(2020) 등 글로벌 사례에서 검증되었다.

```text
[클라우드 아키텍처 진화 단계와 책임 분담 모델]

   책임 영역:   On-Prem      IaaS         PaaS         SaaS         FaaS
   ---------------------------------------------------------------------
   Application   ████████    ████████     ████████     ----        ----
   Data          ████████    ████████     ----         ----        ----
   Runtime       ████████    ████████     ----         ----        ----
   Middleware    ████████    ████████     ----         ----        ----
   OS            ████████    ████████     ----         ----        ----
   Virtualization████████    ----         ----         ----        ----
   Servers       ████████    ----         ----         ----        ----
   Storage       ████████    ----         ----         ----        ----
   Network       ████████    ----         ----         ----        ----

   진화 타임라인:
   2006 --- 2010 --- 2014 --- 2017 --- 2020 --- 2024
   AWS EC2   RDS     Lambda   EKS     Graviton3  AI-Native
   S3        DynamoDB         Istio   K8s 1.30   Serverless
```

클라우드 아키텍처의 본질적 가치는 **"탄력성(Elasticity)"**, **"무한 확장성(Infinitely Scalable)"**, **"Pay-as-you-go 과금"**의 세 가지로 집약된다. 한국 클라우드 시장은 2023년 약 7.5조 원 규모이며, 금융·공공·제조 업종 중심으로 Public Cloud 도입이 가속화되고 있다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 "전기 그리드"와 같다. 발전소(클라우드 제공자)가 모든 전력을 관리하고, 우리는 콘센트(IaaS/PaaS API)에 필요한 만큼만 연결해 사용하며, 사용한 전기량(kWh)만큼만 요금을 지불한다. 발전소 증설이나 정전 관리는 발전사 책임이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 크게 **5개 계층**과 **4개 횡단 관심사(Cross-Cutting Concerns)**로 구성된다. 5계층은 Presentation(CDN, ALB), Application(API Gateway, Microservice), Data(RDS, Redis, S3), Integration(SQS, Kafka, EventBridge), Infrastructure(EC2, EKS, Lambda)이고, 횡단 관심사는 Observability, Security, Resilience, IaC/GitOps이다.

```text
[참조 아키텍처: Multi-AZ, Multi-Region 웹 서비스 토폴로지]

                         +--------------------------+
   +----------+          |   Route 53 (DNS + GSLB)  | <- 지연시간 기반 라우팅
   |   User   |---------->|   Health Check (Active)  |
   +----------+          +----------+---------------+
                                    |
                +-------------------+-------------------+
                |                   |                   |
        +-------v------+    +-------v------+    +-------v------+
        |  CloudFront  |    |   CloudFront |    |  CloudFront  |
        | (Edge PoP)   |    |  (Edge PoP)  |    |  (Edge PoP)  |
        +-------+------+    +-------+------+    +-------+------+
                |                   |                   |
        +-------v------+    +-------v------+    +-------v------+
        |  ALB (us-e1) |    |  ALB (us-w2) |    |  ALB (ap-n2) |
        |  WAF + Shield|    |  WAF + Shield|    |  WAF + Shield|
        +-------+------+    +-------+------+    +-------+------+
                |                   |                   |
       +--------+--------+  +-------+-------+  +--------+--------+
       |        |        |  |       |       |  |        |        |
   +---v-+  +---v-+  +--v--+ ... |       | ...+--v--+ +---v-+  +---v-+
   |ECS  |  |ECS  |  |ECS  |     |       |    |ECS  | |ECS  |  |ECS  |
   |Task |  |Task |  |Task |     |       |    |Task | |Task |  |Task |
   |#1   |  |#2   |  |#3   |     |       |    |#N-2 | |#N-1 |  |#N   |
   +--+--+  +--+--+  +--+--+     |       |    +--+--+ +--+--+  +--+--+
      |        |        |        |       |       |       |        |
      +--------+--------+--------+-------+-------+-------+--------+
               |                 |               |       |
        +------v------+   +------v------+  +-----v------v-----+
        | Aurora      |   | ElastiCache |  |  S3 (Multi-AZ)   |
        | MySQL       |   | Redis       |  |  Versioned       |
        | (Writer/    |   | Cluster Mode|  |  + CRR           |
        |  Reader)    |   |             |  |                  |
        +-------------+   +-------------+  +------------------+
               |
        +------v--------------+    +-------------------------+
        |  SQS / Kafka / Kinesis   |  <-- Event-Driven Async |
        |  (Decoupling Buffer)|    |  Pub/Sub for Fan-out    |
        +---------------------+    +-------------------------+
```

### 핵심 동작 메커니즘

**1) Auto-Scaling 알고리즘**: AWS Target Tracking Scaling은 CloudWatch 메트릭(CPUUtilization, RequestCountPerTarget)을 기반으로 `desiredCapacity = currentCapacity × (metricValue / targetValue)` 공식으로 30~60초 주기 조정. Predictive Scaling은 과거 14일 데이터를 LSTM으로 분석해 사전 스케일링. KEDA(Kubernetes Event-Driven Autoscaling)는 Kafka Lag, SQS Queue Length 같은 이벤트 소스 기반 스케일링을 지원한다.

**2) 분산 합의 프로토콜**: Aurora는 Quorum 기반 6복제(4/6 Write, 3/6 Read) + Quorum Set로 100ms 내 P99 Read Latency, 4초 내 Failover 보장. DynamoDB는 3 AZ 동기 복제 + Paxos-like 합의로 11-nines Durability(99.999999999%)를 제공한다. **CAP 정리 트레이드오프**: RDBMS는 CP(강한 일관성), DynamoDB/Cassandra는 AP(가용성+분할 허용), Etcd/ZooKeeper는 CP+Leader Election이다.

**3) 컨테이너 오케스트레이션**: K8s Control Plane(API Server, etcd, Scheduler, Controller Manager)이 Worker Node의 kubelet과 통신하며, Pod 단위 스케줄링, HPA(Horizontal Pod Autoscaler) v2는 CPU/Memory/RPS/Custom Metric 기반 15초 주기 조정, PDB(PodDisruptionBudget)로 자발적 중단 시 최소 가용 Pod 수 보장한다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Edge / CDN 계층** | 글로벌 정적 콘텐츠 캐싱, DDoS 방어 | CloudFront, Cloudflare, Akamai — Anycast IP + Edge Location(PoP) 200+곳, TTL 기반 캐시 무효화, Origin Shield로 백엔드 부하 50%v |
| **L7 Load Balancer** | HTTP/HTTPS 라우팅, TLS Termination, Sticky Session | ALB — Path/Host/Header 기반 라우팅 규칙, WAF 연동 OIDC/JWT 인증, Connection Draining 300초 |
| **API Gateway** | API 단일 진입점, Rate Limiting, Throttling | Kong, AWS API Gateway, Apigee — Token Bucket 알고리즘(Burst + Refill Rate), Client-ID + API Key 기반 Quota, OpenAPI 3.0 명세 기반 |
| **Compute Orchestrator** | 컨테이너 라이프사이클 관리, 스케줄링, 셀프힐링 | EKS/AKS/GKE — Deployment(롤링 업데이트 maxSurge=25%, maxUnavailable=0), StatefulSet(안정적 네트워크 ID), DaemonSet(노드당 1 Pod) |
| **Service Mesh** | mTLS, 트래픽 관리, 관측 가능성 | Istio/Linkerd — Sidecar(Envoy) 주입, mTLS 1.3 SPIFFE ID, 카나리 배포(Traffic Split 90:10->50:50->0:100), 분산 트레이싱 OpenTelemetry |
| **Managed Database** | 자동 백업, PITR, Multi-AZ 복제 | Aurora MySQL/PostgreSQL — Storage Auto-Scaling 10GB->128TB, 6-way Replication, 15개 Read Replica, Backtrack 기능(72시간 내 시점 복구) |
| **Object Storage** | 비정형 데이터(Binary) 저장, 11 9s Durability | S3 Standard/IA/Glacier — Erasure Coding(Reed-Solomon 4+2), Lifecycle Policy로 자동 티어링, S3 Object Lock으로 WORM 지원 |
| **Message Queue / Event Bus** | 비동기 처리, Fan-out, 백프레셔 | SQS Standard(at-least-once, 무순서)/FIFO(Exactly-Once), Kafka(Persistent Log, 7일 Retention), EventBridge(70+ AWS 서비스 SaaS 이벤트 라우팅) |
| **Observability Stack** | 메트릭, 로그, 트레이스 통합 수집 | Prometheus + Grafana(시계열), ELK/EFK(로그), Jaeger/Tempo(분산 트레이싱), 3-Pillar Correlation(Log->Trace->Metric) |
| **IaC / GitOps** | 선언적 인프라 코드화, 자동 배포 | Terraform(HCL 멀티 클라우드), Pulumi(Go/Python), AWS CDK, ArgoCD/Flux(K8s GitOps, Pull 방식 30초 주기 동기화) |
| **Secrets / KMS** | 시크릿 중앙 관리, BYOK, 자동 Rotation | AWS KMS(HSM FIPS 140-2 L3), Secrets Manager(자동 7/30/90일 Rotation), HashiCorp Vault(Dynamic Secrets, PKI) |
| **Identity / IAM** | 최소 권한 원칙, RBAC/ABAC | AWS IAM(Policy JSON, SCP로 OU 단위 제한), IRSA(IAM Role for Service Accounts, OIDC 토큰 기반 K8s 워크로드 자격증명) |

### 핵심 파라미터 및 알고리즘

- **Consistent Hashing**: DynamoDB/Cassandra의 Partition Key 분배 — Ring 구조에서 Node 추가/제거 시 영향 범위 O(K/N), Virtual Node(VNode) 256개로 편향 완화
- **Quorum Read/Write**: N=복제 수, W=쓰기 정족수, R=읽기 정족수일 때 `W + R > N`이면 강한 일관성 (예: N=3, W=2, R=2)
- **Blue/Green 배포**: 두 환경 동시 운영, Route 53 Weighted Routing 100%->0% DNS 전환, DB 스키마는 Expand-Contract 패턴(컬럼 추가->마이그레이션->컬럼 제거)
- **Saga Pattern**: 보상 트랜잭션(Compensating Transaction)으로 분산 트랜잭션 구현 — Orchestration(Saga Orchestrator 중앙 통제) vs Choreography(각 서비스 이벤트 발행) 방식

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 5계층은 마치 "우주 정거
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 746 / 800

<- **이전**: [745. 클라우드 아키텍처 핵심 토픽 745번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/745_cloud_architecture_core_topic_745_exam_summar/)
**다음**: [747. 클라우드 아키텍처 핵심 토픽 747번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/747_cloud_architecture_core_topic_747_exam_summar/) ->

---
