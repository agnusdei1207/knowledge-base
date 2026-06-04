---
title: "686. 클라우드 아키텍처 핵심 토픽 686번 시험 요약 (Cloud Architecture Core Topic 686 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


# 686. 클라우드 아키텍처 핵심 토픽 686번 시험 요약

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST 정의 5대 특성(온디맨드 셀프서비스, 광대역 네트워크 접근, 리소스 풀링, 탄력적 확장, 측정 가능한 서비스)과 4개 배포 모델(Public/Private/Hybrid/Community) 위에서 **IaaS·PaaS·SaaS·FaaS**의 책임 분담 모델을 통해 컴퓨트·스토리지·네트워크 자원을 추상화·오케스트레이션하는 분산 시스템 아키텍처다.
> 2. **가치**: AWS Well-Architected Framework 기준 클라우드 네이티브 전환 시 TCO 30~60% 절감, Auto Scaling을 통한 트래픽 피크 시 5~20배 용량 자동 확보, Multi-AZ 구성을 통해 99.99% 가용성(SLA 4-nines), CAPEX->OPEX 전환으로 초기 투자 회수 기간 평균 18개월 단축이 가능하다.
> 3. **판단 포인트**: 핵심 의사결정 ① 단일 클라우드 종속(Vendor Lock-in) vs 멀티/하이브리드 ② Stateful 워크로드의 컨테이너화 vs VM 기반 유지 ③ Egress 비용·데이터 주권·컴플라이언스(국내 개인정보보호법, GDPR) ④ CAP 정리의 일관성·가용성·분단 내성 트레이드오프, ⑤ Spot/On-Demand/Reserved 인스턴스 비율 최적화를 통한 3~7배 비용 효율화를 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

클라우드 아키텍처는 더 이상 단순한 "데이터센터 외주"가 아니라, **API 기반 셀프서비스 프로비저닝, 선언적 인프라스트럭처(Infrastructure as Code), 마이크로서비스 분해, GitOps 운영 체계**가 융합된 새로운 컴퓨팅 패러다임이다. 686번 시험은 이러한 패러다임 전환을 시스템 아키텍처 관점에서 평가하며, 단순한 클라우드 서비스 나열이 아니라 **"왜 그 아키텍처 패턴이 해당 SLA/성능/비용 요구사항에 정합적인가"**를 묻는 것에 중점을 둔다.

기존 온프레미스 환경의 한계는 명확하다. ① Capex 기반의 과잉 프로비저닝(평균利用率 15~25%), ② 수직적 확장(Scale-Up)의 물리적 한계, ③ 장애 대응을 위한 MTTR 평균 4시간, ④ IDC 전력·냉각 제약(데이터센터 PUE 1.5~2.0), ⑤ 신기술 도입 시 하드웨어 리드타임 8~12주. 반면 클라우드 아키텍처는 수요 기반 탄력성(Elasticity), 글로벌 엣지 배포, Pay-per-use 과금, 자동화된 장애 복구(Healing)를 통해 이를 해결한다.

```text
+---------------------------------------------------------------------+
|              On-Premise vs Cloud-Native 아키텍처 패러다임 비교        |
+---------------------------------------------------------------------+
|                                                                     |
|  [On-Premise - 1990~2010]            [Cloud-Native - 2010~현재]     |
|  +------------------+                +------------------+            |
|  |   Monolith App   |                | Microservices    |            |
|  |   (EAR/WAR)      |                | (12-factor)      |            |
|  +------------------+                +------------------+            |
|  |   App Server     |                | Container Runtime|            |
|  |   (WebLogic)     |                | (K8s/ECS)        |            |
|  +------------------+                +------------------+            |
|  |   RDBMS + SAN    |                | Polyglot Storage |            |
|  |   (Oracle + EMC) |                | (NoSQL/NewSQL)   |            |
|  +------------------+                +------------------+            |
|  |   수동 배포       |                | GitOps/CI-CD     |            |
|  |   (릴리스 6개월)   |                | (릴리스 일/시간)   |            |
|  +------------------+                +------------------+            |
|  CAPEX ^^  / 유연성 v                OPEX ^ / 유연성 ^^             |
|  가용성 99.9% /  탄력성 ✗            가용성 99.99%+ / 탄력성 ◎       |
+---------------------------------------------------------------------+
```

NIST SP 500-292 참조 모델에 따르면 클라우드 아키텍처는 **5대 필수 특성(Essential Characteristics)**과 **3대 서비스 모델(SaaS/PaaS/IaaS)**, **4대 배포 모델(Public/Private/Hybrid/Community)**의 매트릭스로 정의된다. 기술사 시험에서는 이 매트릭스를 기반으로 워크로드 특성(워크로드 패턴, 데이터 중복성, 컴플라이언스 요구사항)에 따라 **적합한 서비스 모델과 배포 모델을 선정하는 정당성**을 평가한다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **전기 그리드**와 같다. 발전소(클라우드 공급자)에서 송전선(네트워크)을 통해 가정·공장(사용자)에 전기를 공급하되, 사용하는 만큼만 요금을 내며, 수요 급증 시 자동 증설이 이루어지는 구조. 직접 발전소(온프레미스)를 짓는 것 대비 초기 비용·운영 부담이 대폭 줄어든다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심 메커니즘은 **"추상화 -> 분할 -> 자동화 -> 관측가능성"**의 4단계 사이클로 요약된다. ① 컴퓨트/스토리지/네트워크 자원을 하이퍼바이저(예: AWS Nitro, KVM, Xen)와 컨테이너 런타임(예: containerd, CRI-O)으로 추상화하고, ② 마이크로서비스로 도메인을 분할(Bounded Context, DDD)한 뒤, ③ IaC(Terraform/CloudFormation/Pulumi) + 오케스트레이터(Kubernetes/EKS/AKS/GKE)로 자동화하며, ④ Observability 3요소(Metrics, Logs, Traces) 기반 SLI/SLO로 관측한다.

```text
+----------------------------------------------------------------------+
|         Cloud-Native Reference Architecture (CNCF Landscape)         |
+----------------------------------------------------------------------+
|                                                                      |
|   [사용자]                                                            |
|      | HTTPS/TLS 1.3                                                 |
|      v                                                               |
|   +--------------------------------------------------+               |
|   |  Edge: CDN + WAF (CloudFront/Akamai/Cloudflare)  |  <- L4~L7     |
|   +------------------+-------------------------------+               |
|                      v                                               |
|   +--------------------------------------------------+               |
|   |  API Gateway: 인증/인가/Throttling/Transform      |  <- OAuth2/JWT |
|   +------------------+-------------------------------+               |
|                      v                                               |
|   +--------------------------------------------------+               |
|   |  Service Mesh: Istio/Linkerd (mTLS, Retry, CB)   |  <- Sidecar    |
|   +------------------+-------------------------------+               |
|                      v                                               |
|   +--------------------------------------------------+               |
|   |  Microservices: Bounded Context별 독립 배포        |  <- K8s Pod   |
|   |  +--------+ +--------+ +--------+ +--------+      |               |
|   |  |Order Svc| |Pay Svc | |Item Svc| |User Svc|      |               |
|   |  +----+---+ +----+---+ +----+---+ +----+---+      |               |
|   +-------+----------+----------+----------+----------+               |
|           v          v          v          v                          |
|   +--------------------------------------------------+               |
|   |  Event Bus: Kafka / SQS+Kinesis / Pub/Sub        |  <- CDC/Async  |
|   +------------------+-------------------------------+               |
|                      v                                               |
|   +--------------------------------------------------+               |
|   |  Data Tier: Polyglot Persistence                   |               |
|   |  OLTP(RDBMS)|Cache(Redis)|Search(ES)|DW(BigQuery) |               |
|   +--------------------------------------------------+               |
|                                                                      |
|   [Cross-cutting] Observability(Prometheus+Grafana+Tempo/Loki)       |
|                  IaC(Terraform), GitOps(ArgoCD), Security(OPA)        |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 추상화 계층** | 물리 하드웨어를 논리 컴퓨트 자원으로 변환 | 하이퍼바이저(Xen, KVM, AWS Nitro System), 베어메탈(I3en, 전용 호스트), 컨테이너(Docker, containerd), MicroVM(Firecracker) — `Overcommit Ratio 1:1~1:4`, Live Migration으로 무중단 유지보수 |
| **스토리지 계층** | 데이터 영속성·내구성·접근 패턴별 분리 | Block(EBS gp3: 3,000 IOPS/GB), Object(S3: 99.999999999% 11 nines 내구성), File(EFS, FSx for Lustre), Cold(S3 Glacier IR/Deep Archive) — **3-2-1 백업 원칙** 및 Cross-Region Replication |
| **네트워크/SDN** | VPC·서브넷·라우팅·보안 그룹 정책 | VPC Peering vs Transit Gateway(50+ VPC 허브), PrivateLink(엔드포인트 서비스), Direct Connect(전용선 1~10Gbps), VPC CNI(Pod별 IP 할당), IPv6 Dual-Stack |
| **오케스트레이션/스케줄러** | 컨테이너 라이프사이클·자동 복구·롤링 업데이트 | Kubernetes Control Plane(API Server, etcd Raft 합의, Scheduler, Controller Manager) — **HPA/VPA/Cluster Autoscaler** 3종 오토스케일링, Karpenter로 노드 프로비저닝 시간 30초->5초 |
| **데이터베이스/Polyglot** | 트랜잭션·분석·검색·캐시 분리 | RDS Aurora(MySQL/PostgreSQL 호환, 6-way 복제), DynamoDB(전역 테이블 Multi-Region Active-Active), Redis(ElastiCache), OpenSearch, Snowflake/BigQuery(DW) |
| **메시지/이벤트 스트리밍** | 서비스 간 비동기 통신, CDC, 사가 패턴 | Apache Kafka(KRaft 모드, Partition Rebalance, Exactly-Once Semantics), AWS SQS/SNS/Kinesis, RabbitMQ, NATS |
| **관측가능성(Observability)** | SLI/SLO 기반 운영·장애 탐지 | **3 Pillars**: Metrics(Prometheus/CloudWatch), Logs(Loki/ELK), Traces(Jaeger/Tempo/X-Ray) — **USE/RED 메서드**, OpenTelemetry SDK 표준화 |
| **보안/거버넌스** | 제로트러스트, IAM, 암호화, 컴플라이언스 | IAM Role + KMS envelope encryption, Secrets Manager/Vault, OPA/Kyverno(Policy as Code), CSPM(Cloud Security Posture Management), SIEM(Security Lake) |

### 핵심 원리 상세: 12-Factor App + 클라우드 디자인 패턴

**12-Factor App 원칙**(Heroku, 2011)은 클라우드 네이티브 애플리케이션 설계의 기반이다. ① Codebase(단일 저장소), ② Dependencies(명시적 선언), ③ Config(환경변수 분리), ④ Backing Services(리소스를 attached resource로), ⑤ Build/Release/Run(완전 분리), ⑥ Processes(Stateless), ⑦ Port Binding(자체 포트 서비스), ⑧ Concurrency(프로세스 모델로 확장), ⑨ Disposability(빠른 시작/종료), ⑩ Dev/Prod Parity, ⑪ Logs(스트림), ⑫ Admin Processes(일회성 관리 작업).

**핵심 분산 알고리즘**:
- **CAP 정리**: 일관성(Consistency), 가용성(Availability), 분단 내성(Partition tolerance) 중 2개만 보장. AP 시스템(DynamoDB, Cassandra)은 eventual consistency, CP 시스템(HBase, etcd)는 분단 시 일관성 우선.
- **Consensus**: Raft 합의 알고리즘(etcd, Kafka KRaft, CockroachDB) — Leader Election + Log Replication, 3~5 노드 Quorum 구성.
- **샤딩**: Consistent Hashing(Ring 구조, Dynamo/Cassandra), 가상 노드(Virtual Node) 256개로 데이터 편향 방지, 리밸런싱 시 가상 노드 단위 이동.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **도시의 상하수도 시스템**과 같다. 가정(서비스)은 수도관(API/네트워크)을 통해 정수장(컴퓨트/스토리지)에서 물(데이터)을 공급받고, 사용량에 따라 자동으로 배압이 조절되며(Autoscaling), 일부 구역 정수(Region/AZ)가 고장나도 다른 지역에서 우회 공급(Multi-AZ Failover)된다.

---

## Ⅲ. 비교 및 연결

### 3-1. 배포 모델 비교

| 구분 | Public Cloud | Private Cloud | Hybrid Cloud | Community Cloud |
| :--- | :--- | :--- | :--- | :--- |
| **소유/운영** | 외부 CSP(AWS/Azure/GCP) | 자체/전담 운영(VMware, OpenStack) | On-Prem + Public 연결 | 동일 커뮤니티 공동 사용 |
| **TCO 모델** | OPEX 100%, 종량제 | CAPEX+OPEX 혼합, 3~5년 회수 | 양쪽 혼합, 폭증 시 Cloud Bursting | CAPEX 분담, 도메인 특화 |
| **확장성** | 사실상 무제한(수 분 내) | 물리 자원 한계 | 평상시 On-Prem, 피크 시 Public | 커뮤니티 내 한정 |
| **컴플라이언스** | 리전·인증 의존(CSAP, ISO 27001) | 완전 통제, 금융/공공 적합 | 데이터 주권·GDPR 준수 가능 | 의료/정부 공동체 |
| **적합 워크로드** | 일반 웹·SaaS, 배치, AI/ML | 규제 데이터, Legacy ERP, HPC | 코어-뱅킹, 데이터 레이크 | 연구 컨소시엄, 군·정부 |
| **Latency** | 리전별 1~50ms | 사내 1~5ms | Direct Connect 1~10ms | 사내 수준 |
| **대표 사례** | Netflix, Airbnb, Slack | 금융사 내부 시스템, 정부 G-Cloud | 코엑스-S3 연동, 의료 하이브리드 | CERN, GAIA-X, 의료 클러스터 |
| **Lock-in 위험** | 매우 높음 | 낮음(Open API) | 중간(중간 계층 추상화 필요) | 낮음 |

### 3-2. 서비스 모델 책임 분담 비교

| 계층 | On-Premise | IaaS (EC2) | PaaS (Beanstalk) | SaaS (Office 365) | FaaS (Lambda) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Application | 사용자 | 사용자 | 사용자 | CSP | 사용자 |
| Data | 사용자 | 사용자 | 사용자 | CSP | 사용자 |
| Runtime | 사용자 | 사용자 | CSP | CSP | CSP |
| Middleware | 사용자 | 사용자 | CSP | CSP | CSP |
| OS | 사용자 | 사용자 | CSP | CSP | CSP |
| Virtualization | 사용자 | CSP | CSP | CSP | CSP |
| Server
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 686 / 800

<- **이전**: [685. 클라우드 아키텍처 핵심 토픽 685번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/685_cloud_architecture_core_topic_685_exam_summar/)
**다음**: [687. 클라우드 아키텍처 핵심 토픽 687번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/687_cloud_architecture_core_topic_687_exam_summar/) ->

---
