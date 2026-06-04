---
title: "583. 클라우드 아키텍처 핵심 토픽 583번 시험 요약 (Cloud Architecture Core Topic 583 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS 4계층 모델을 기반으로 CAP 정리(Consistency, Availability, Partition tolerance)와 12-Factor App 원칙을 준수하여, 컨트롤 플레인(Control Plane)과 데이터 플레인(Data Plane)을 분리하고, Well-Architected Framework의 5대 필러(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화)를 통해 설계하는 분산 시스템 아키텍처임.
> 2. **가치**: Auto Scaling Group과 Multi-AZ 배포를 통해 트래픽 10배 증가 시에도 SLA 99.99%(연 52.6분 장애) 유지, IaC(Infrastructure as Code)로 프로비저닝 시간 90% 단축(수일->수분), Pay-per-use 모델로 유휴 자원 비용 30~70% 절감, MTTR(Mean Time To Recovery)을 60% 단축하여 비즈니스 연속성 확보.
> 3. **판단 포인트**: Lift-and-Shift(Rehost) vs Cloud-Native(Refactor) 트레이드오프, 동기식 복제(Strong Consistency) vs 비동기식 복제(Eventual Consistency) 선택, EKS/AKS/GKE 등 컨테이너 오케스트레이션 도입 시 복잡도 대비 운영 효율성 검증, FinOps 도구(Cost Explorer, Kubecost) 기반의 비용 가시성 확보 여부가 아키텍처 성패를 결정함.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스(On-Premise) 3-Tier 아키텍처는 예측 기반의 용량 계획(Capacity Planning), 수직적 확장(Scale-Up) 한계, CapEx(자본적 지출) 중심의 정적 인프라, 그리고 단일 장애점(SPOF, Single Point of Failure) 문제를 안고 있었음. 2020년대 들어 클라우드 네이티브(Cloud-Native) 패러다임은 Netflix가 2010년 1월 12일 AWS US-EAST-1 리전 장애로 3일간의 서비스 중단을 겪은 후 Hystrix, Eureka, Zuul, Ribbon으로 대표되는 "Netflix OSS" 레질리언스 패턴을 도입하며 본격화되었음.

기술사 시험에서 다루는 클라우드 아키텍처는 단순한 가상머신(EC2, Compute Engine) 사용이 아니라, **가용 영역(Availability Zone) 간 다중화**, **리전(Region) 간 재해복구(DR)**, **마이크로서비스 분할**, **서버리스 컴퓨팅**, **서비스 메시(Service Mesh)**, **GitOps 기반 배포** 등 분산 시스템의 본질적 문제를 다루는 것이 핵심임.

```text
[클라우드 아키텍처 진화 패러다임]

  +---------------------------------------------------------------------+
  |                  Monolith (2000s) -> Microservice (2015~)             |
  |                                                                     |
  |  +--------------+        +----------------------------------------+ |
  |  |   Monolith   |        |     Microservices (Cloud-Native)       | |
  |  |              |        | +------+ +------+ +------+ +------+  | |
  |  | +----------+ |   ->    | | User | |Order | |Pay   | |Notif |  | |
  |  | |   UI     | |        | | Svc  | | Svc  | | Svc  | | Svc  |  | |
  |  | +----------+ |        | +------+ +------+ +------+ +------+  | |
  |  | |  Business| |        |   ^         ^         ^         ^     | |
  |  | |  Logic   | |        | API Gateway(Envoy/Kong) + Service Mesh | |
  |  | +----------+ |        |   v         v         v         v     | |
  |  | |   Data   | |        | +---------------------------------+   | |
  |  | +----------+ |        | | Polyglot Persistence (RDB+NoSQL)|   | |
  |  +--------------+        | +---------------------------------+   | |
  |  Scale-Up (수직확장)       | Scale-Out (수평확장) + Auto-Healing      |
  |  CapEx 80% + OpEx 20%     | CapEx 20% + OpEx 80% (Pay-per-use)      |
  +---------------------------------------------------------------------+

  +---------------------------------------------------------------------+
  |  클라우드 아키텍처 필요성 4대 Driver                                |
  |                                                                     |
  |  1) 탄력성(Elasticity):  TPS 1K -> 100K 급변, Auto Scaling 3분 이내  |
  |  2) 글로벌 확장성:      Multi-Region Active-Active, Edge Computing |
  |  3) TCO 절감:           IDC 5년 운영비 vs Cloud 5년 운영비 (40%v)  |
  |  4) Time-to-Market:     신기능 배포 주기 6개월 -> 1일 (CI/CD)         |
  +---------------------------------------------------------------------+
```

온프레미스 환경에서는 신규 서버 도입에 평균 6~12주가 소요되었고, 트래픽 피크(블랙프라이데이, 설·추석)에 대비한 과도한 용량 프로비저닝으로 70% 이상의 자원이 유휴 상태로 남았음. 반면 AWS Auto Scaling, Azure VMSS(Virtual Machine Scale Sets), GCP MIG(Managed Instance Groups)는 CloudWatch/Azure Monitor/Stackdriver 지표(CPU, 메모리, 큐 길이, 사용자 정의 지표)를 기반으로 60~300초 내 자동으로 인스턴스를 확장/축소하여, **탄력성(Elasticity)**을 자본이 아닌 운영 변수로 전환함.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **전기 수도 그리드**와 같음. 발전소(IdC, On-Premise)에서 직접 발전하는 것보다, 전력 회사의 그리드(Public Cloud)에 연결하여 필요한 만큼만 끌어쓰는 것이 더 경제적이고 안정적임. 다만 정전(클라우드 장애) 시를 대비해 자가발전(DR 사이트)을 병행하는 하이브리드 전략이 필요함.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **5계층 책임 공유 모델(Shared Responsibility Model)**을 근간으로 함. 클라우드 제공업체(CSP)는 "Of the Cloud"(물리적 보안, 하드웨어, 하이퍼바이저, 네트워크)를 책임지고, 고객은 "In the Cloud"(OS 패치, 미들웨어, 데이터 암호화, IAM 정책, 네트워크 구성)을 책임짐. 이 경계를 명확히 이해하는 것이 기술사 시험의 핵심임.

```text
[AWS 기준 클라우드 아키텍처 핵심 컴포넌트 다이어그램]

                          +--------------------------+
                          |   Route 53 (DNS)         |
                          |   Health Check + Latency |
                          |   Based Routing          |
                          +------------+-------------+
                                       | A/Alias Record
                                       v
              +----------------------------------------------+
              |   CloudFront (CDN) + WAF (Layer 7 Firewall)  |
              |   - TLS 1.3, Shield Standard/Advanced (DDoS)  |
              |   - OAC (Origin Access Control) for S3        |
              +--------------------+-------------------------+
                                   |
              +--------------------+---------------------+
              |                                          |
              v                                          v
   +----------------------+                 +----------------------+
   |  ALB (Application LB)|                 |  API Gateway (REST/  |
   |  L7 Path/Host Routing|                 |  WebSocket/GraphQL)  |
   |  WAF, ACM SSL/TLS    |                 |  + Lambda Authorizer |
   +----------+-----------+                 +----------+-----------+
              |                                        |
              v                                        v
   +--------------------------------------------------------------+
   |   EKS (Kubernetes) Service Mesh (Istio/Linkerd/App Mesh)      |
   |   - Sidecar Proxy (Envoy): mTLS, Retry, Circuit Breaker       |
   |   - Control Plane: K8s API + Istiod (Pilot/Citadel/Galley)   |
   +----+--------------+--------------+--------------+------------+
        |              |              |              |
        v              v              v              v
   +---------+    +---------+    +---------+    +---------+
   | User Svc|    |Order Svc|    | Pay Svc |    |Notif Svc|
   | (Pod×N) |    | (Pod×N) |    | (Pod×N) |    | (Pod×N) |
   +----+----+    +----+----+    +----+----+    +----+----+
        |              |              |              |
        +--------------+--------------+--------------+
                              |
        +---------------------+---------------------+
        v                     v                     v
   +---------+         +-------------+       +--------------+
   | Aurora  |         | DynamoDB    |       | ElastiCache  |
   | MySQL   |         | (NoSQL,     |       | Redis        |
   | Global  |         |  Single-digit|       | Cluster Mode|
   | Database|         |  ms latency) |       | (Sub-ms)     |
   | Multi-AZ|         | DAX, GSI/LSI|       |              |
   +---------+         +-------------+       +--------------+
        |                     |                     |
        +---------------------+---------------------+
                              |
                              v
              +-------------------------------+
              |  Observability Layer (3-Pillars)|
              |  - CloudWatch/X-Ray/Prometheus|
              |  - Logs / Metrics / Traces    |
              |  - Centralized: Grafana+Loki  |
              +-------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Edge Layer (Route 53 + CloudFront)** | DNS 라우팅, 글로벌 캐싱, DDoS 방어 | Route 53 Health Check는 30초 간격으로 endpoint 헬스체크하여 비정상 endpoint를 자동 fail-over, CloudFront는 600+ Edge Location에 캐싱하여 S3 Origin 부하 90% 감소, Lambda@Edge로 viewer request 단계 인증/인가 수행 |
| **API Gateway / ALB** | L7 라우팅, API 스로틀링, 인증/인가 통합 | API Gateway는 API Key별 초당 요청 한도(기본 10,000 RPS) 설정, Lambda Authorizer로 JWT 검증, ALB는 Target Group Health Check(HTTP 200 OK, 30s interval) 기반 정상 인스턴스만 라우팅 |
| **Kubernetes (EKS/AKS/GKE)** | 컨테이너 오케스트레이션, 셀프힐링, 선언적 배포 | kube-scheduler가 Pod를 노드 affinity/anti-affinity, taints/tolerations, resource requests/limits 기반으로 스케줄링, HPA(Horizontal Pod Autoscaler)는 CPU/메모리/사용자 정의 지표(via KEDA)로 replica 수 자동 조정, PDB(Pod Disruption Budget)로 자발적 중단 통제 |
| **Service Mesh (Istio/Linkerd)** | mTLS, 트래픽 관리, 관측 가능성 | Sidecar Proxy(Envoy)가 모든 east-west 트래픽을 L7 단에서 가로채어 mTLS 암호화, Retry(기본 2회), Circuit Breaker(consecutive 5xx 5회 시 half-open), Traffic Split(카나리 90:10) 처리, OpenTelemetry 표준으로 trace 전파 |
| **Polyglot Persistence** | 데이터 특성별 DB 분리 (CQRS/Event Sourcing) | 트랜잭션 데이터는 Aurora MySQL/PostgreSQL(Audit Log, ACID), 대용량 읽기는 DynamoDB/CosmosDB(Single-digit ms, On-demand/Provisioned), 세션/캐시는 ElastiCache Redis(MemoryStore, sub-ms), 분석은 Redshift/BigQuery(Columnar, MPP), 시계열은 Timestream/InfluxDB |
| **Observability (3 Pillars)** | 로그/메트릭/트레이스 통합 분석 | **Metrics**: CloudWatch/Prometheus(시계열, 1분/15초 단위), **Logs**: OpenSearch/Loki(중앙 집중), **Traces**: X-Ray/Jaeger(OpenTelemetry SDK로 traceparent 헤더 전파), SLO 기반 알람(Error Budget 소진 시 알림) |

**핵심 알고리즘 및 프로토콜 심화**

1. **분산 합의 알고리즘 - Raft/Paxos**: Kubernetes etcd는 Raft 알고리즘으로 leader election(log replication, leader lease 15s) 수행, DynamoDB는 quorum 기반 (W+R > N) 튜닝으로 일관성/가용성 trade-off 조정 (예: N=3, W=2, R=2 -> Strong Consistency)
2. **Eventual Consistency의 수렴 보장**: DynamoDB는 Vector Clock 대신 Lexicographic Versioning(Latest Timestamp + LWW) 사용, S3는 Read-After-Write Consistency를 2020년 12월부터 모든 리전에서 지원
3. **SAGA 패턴**: 마이크로서비스 간 분산 트랜잭션을 **Orchestration**(Step Functions, Temporal) 또는 **Choreography**(EventBridge, Kafka)로 처리, 보상 트랜잭션(Compensating Transaction)으로 롤백 구현
4. **CQRS(Command Query Responsibility Segregation)**: 쓰기는 RDB(Aurora), 읽기는 별도 Read Model(Elasticsearch, DDB GSI)로 분리하여 읽기/쓰기 트래픽 비대칭 해결

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 5계층은 마치 **우체국 시스템**과 같음. 우편번호(API Gateway)가 우편물의 종류(POST/GET/PUT)를 분류하고, 집배원(API Gateway -> Microservice)이 해당 구역(Region/AZ)에 배달하며, 각 가정(Service)이 자체 사물함(Database)에 보관함. 중앙 관리국(Control Plane)이 모든 배달 경로와 사물함 상태를 추적합니다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처는 전통적 아키텍처, 컨테이너, 서버리스 등 유사 개념과 명확히 구분되어야 함. 기술사 시험에서는 **어떤 워크로드에 어떤 아키텍처를 적용할지**의 판단력을 평가함.

| 구분 | Monolith (On-Premise) | Container (EKS) | Serverless (Lambda/Fargate) | SaaS (Multi-Tenant) |
| :--- | :--- | :--- | :--- | :--- |
| **확장 단위** | 서버 전체 (Scale-Up) | Pod 단위 (수평 확장) | 함수/태스크 단위 | 테넌트별 워크스페이스 |
| **배포 주기** | 월 1~2회 (야간 배포) | 주 1~수 회 (Blue/Green) | 하루 수십~수백 회 (Canary) | CSP 자동 업데이트 |
| **콜드 스타트** | N/A (상시 기동) | 5~30초 (이미지 pull) | 100ms~5초 (Init 단계) | N/A |
| **비용 모델** | CapEx 80% (5년 감가) | OpEx (EC2+License) | Pay-per-Invocation (ms 단위) | Subscription/User |
| **운영 부담** | 자체 IDC 운영 (24/7 NOC) | 노드/OS/K8s 패치
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 583 / 800

<- **이전**: [582. 클라우드 아키텍처 핵심 토픽 582번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/582_cloud_architecture_core_topic_582_exam_summar/)
**다음**: [584. 클라우드 아키텍처 핵심 토픽 584번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/584_cloud_architecture_core_topic_584_exam_summar/) ->

---
