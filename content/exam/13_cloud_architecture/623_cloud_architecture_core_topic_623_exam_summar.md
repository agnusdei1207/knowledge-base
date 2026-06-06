---
title: "Cloud Architecture Core Topic 623 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 AWS Well-Architected Framework 6대 필러(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화, 지속가능성)와 AZ(Availability Zone)·리전 단위의 분산 설계를 통해, SLO/SLA 기반의 비기능 요건(가용성 99.99%, 내결함성, 탄력성)을 코드로 구현(Architecture as Code)하는 엔지니어링 discipline이다.
> 2. **가치**: 셀 기반 아키텍처(Cell-based Architecture)로 Blast Radius를 1/N로 축소하고, Auto Scaling + Spot Instance + Graviton 조합으로 동일 워크로드 대비 컴퓨팅 비용 40~70% 절감, Multi-AZ Active-Active 구성을 통해 RTO < 1분 / RPO ≈ 0 수준의 DR 체계 구축이 가능하다.
> 3. **판단 포인트**: CAP Theorem 하에서 Strong Consistency ↔ Eventual Consistency, 동기(Synchronous Quorum) ↔ 비동기(Asynchronous Replicaton) 복제, Stateless Microservice ↔ Stateful Stateful(DB/Broker) 분리, EKS vs ECS Fargate vs Lambda의 콜드 스타트·실행 시간·비용 한계(15분) 트레이드오프를 도메인 특성에 따라 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 IT 시스템은 2010년대 이후 3-tier 모놀리스(Presentation-Business Logic-Data Tier)에서 도메인 주도 설계(DDD) 기반 마이크로서비스, 그리고 Serverless·Event-driven 아키텍처로 급격히 진화했다. 클라우드 아키텍처는 이러한 변화를 "인프라 추상화 + API 기반 프로비저닝 + 사용량 과금(Usage-based Billing)"의 세 가지 패러다임 전환으로 실현한다. 과거에는 신규 트래픽 대응을 위해 6개월~1년 선구매(CAPEX) 후 IDC 증설과 OS·미들웨어 수작업 설치가 필요했으나, AWS EC2, GCP Compute Engine, Azure VM 같은 IaaS는 클릭 한 번으로 수십만 코어까지 확장 가능하며, Lambda·Cloud Run 같은 Serverless 플랫폼은 코드를 업로드하는 순간 인프라가 코드를 추적·격리·스케일링한다.

그러나 클라우드 전환 자체가 자동으로 아키텍처 우수성을 보장하지 않는다. Gartner에 따르면 클라우드 마이그레이션 프로젝트의 60%가 "Lift & Shift" 후 재설계 없이 비용 폭증과 성능 저하를 겪고, "명목상 클라우드(Cloud-Subtle)" 현상을 빚는다. 따라서 623번 시험이 요구하는 핵심은 단순한 서비스 카탈로그 암기가 아니라, **비즈니스 도메인의 트래픽 패턴, 데이터 일관성 요건, 컴플라이언스 제약(K-PIPA, PCI-DSS, ISMS-P)**을 분석해 최적의 분산 토폴로지를 설계·검증·운영하는 엔지니어링 역량이다.

특히 On-Premise 환경 대비 클라우드 고유의 "Shared Responsibility Model"에서, OS 패치·IAM 정책·암호화 키 관리 같은 *In-the-Cloud* 책임이 고객에게 이전되므로, 아키텍트는 네트워크 토폴로지뿐 아니라 **제로 트러스트(Zero Trust), IaC(Infrastructure as Code), Observability 3요소(Metrics/Logs/Traces)**까지 통합 설계해야 한다.

```text
+--------------------------------------------------------------+
|        [Legacy Monolith] vs [Cloud-Native Distributed]       |
+--------------------------------------------------------------+
|                                                              |
|  Legacy (On-Premise)              Cloud-Native               |
|  +--------------+                +------------------+        |
|  |   WebSphere  |                |  CloudFront CDN  |        |
|  |   (1 EA App) |                +--------+---------+        |
|  +--------------+                         |                  |
|  |  Oracle RAC  |              +----------v----------+       |
|  |  (Active/Passive)            |   ALB / API GW     |       |
|  +--------------+              +----------+----------+       |
|  | SAN Storage  |       +--------+--------+--------+--+    |
|  +--------------+       v        v        v        v  |    |
|                  +--------++--------++--------++--------+  |
|  Capacity: 고정   |Lambda  ||EKS Pod ||Fargate ||Aurora  |  |
|  Deploy: 6개월    |(이벤트) ||(Stateless)|(배치)||(RDBMS) |  |
|  Cost: CAPEX      +--------++--------++--------++--------+  |
|                              |             |          |      |
|                              +-------------+----------+      |
|                                  EventBridge / Kafka         |
|  Failure: SPOF 다수          Failure: AZ 단위 격리, 99.99%  |
+--------------------------------------------------------------+
```

**기존 방식과의 결정적 차이**:
- **탄력성(Elasticity)**: Auto Scaling Group이 CloudWatch 메트릭(CPU > 70% 5분 지속) 기반으로 인스턴스를 30~300대까지 동적 확장
- **불변 인프라(Immutable Infra)**: AMI/Golden Image로 서버를 재생성하여 구성 드리프트(Configuration Drift) 차단
- **셀 아키텍처**: 한 리전 내에서도 사용자 셔딩(Sharding) -> 장애 확산 방지(N 细胞 Architecture: Roblox, AWS Architecture Blog)
- **📢 섹션 요약 비유**: 레거시 시스템이 "한 채의 큰 호텔"이라면, 클라우드 아키텍처는 **"모듈式 콘도미니엄"** — 각 동(셀)이 독립적인 발전기·정수기·소화설비를 가져, 한 동이 불나도 다른 동은 안전하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 5대 토대는 **① 컴퓨트 추상화, ② 분산 스토리지, ③ 글로벌 네트워킹, ④ 제어 평면(Control Plane), ⑤ 데이터 평면(Data Plane)**이다. AWS를 기준으로 분해하면:

```text
            +-----------------------------------------+
            |     Cloud Well-Architected Framework    |
            |  (6 Pillars) - 의사결정 체크리스트        |
            +-----------------------------------------+
                          |   ^
            +-------------+---+------------------+
            |  Architecture Decision Record(ADR)   |
            +-------------+---+------------------+
                          v   ^
   +----------+----------+----+---+----------+----------+
   v          v          v        v          v          v
[컴퓨트]    [스토리지]  [네트워크]  [DB]     [보안]    [옵저버빌리티]
EC2/Lambda S3/EBS    VPC/Route53 RDS/Aurora  IAM/KMS   CloudWatch
EKS/Fargate  Glacier  CloudFront DynamoDB    WAF/Shield X-Ray
            +-------- AWS Global Infrastructure --------+
            Region(geo) -> AZ(고가용 단위, 1~3개) -> Edge Location
```

**핵심 동작 메커니즘 (4단계)**:

1. **프로비저닝 단계**: Terraform/CloudFormation 같은 IaC가 선언적 HCL/YAML로 VPC, Subnet, SG, IAM Role을 정의 -> AWS Control Tower가 멀티 계정(Landing Zone) 베이스라인 자동 배포
2. **라우팅 단계**: Route 53의 라우팅 정책(Simple, Weighted, Latency-based, Failover, Geolocation, Multi-Value) + ALB의 L7 라우팅(Path/Host/Header 기반)으로 트래픽 분산
3. **데이터 단계**: 쓰기는 Aurora Writer Endpoint(Strong Consistent) -> 6-way 복제 across 3 AZ, 읽기는 Reader Endpoint(Eventually Consistent, lag < 100ms) 분산
4. **관측 단계**: CloudWatch Metrics/Logs + X-Ray Distributed Tracing + CloudTrail Audit -> OpenTelemetry로 Grafana/Tempo/Loki에 통합

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Region / AZ** | 물리적 격리 단위 | Region 간 ≥ 100km, AZ 간 < 1ms RTT, AZ당 1개 이상 데이터센터, 리전 선택 시 latency·컴플라이언스·서비스 가용성 트레이드오프 |
| **VPC + Subnet** | 논리적 네트워크 격리 | /16 CIDR, Public/Private/Isolated Subnet, Route Table·NACL(Stateless)·Security Group(Stateful) 3중 필터, VPC Endpoint로 S3/DynamoDB Private 통신 |
| **컴퓨트 계층** | 워크로드 실행 환경 | EC2(baremetal/M/graviton) / ECS Fargate(컨테이너) / EKS(K8s API 100% 호환) / Lambda(15분·10GB 한계) / Batch(HPC) — 트래픽 패턴(I/O bound vs CPU bound)으로 선택 |
| **스토리지 계층** | 데이터 영속성 | S3(11 9s 내구성, Object Storage), EBS(블록, 단일 AZ), EFS(NFS, Multi-AZ), FSx for Lustre(HPC), Glacier Deep Archive($0.00099/GB/월) — Hot/Warm/Cold 티어링 |
| **데이터 계층** | 트랜잭션/분석 | OLTP(Aurora MySQL/PostgreSQL 5x MySQL, 3x PostgreSQL 성능), OLAP(Redshift, Athena on S3), NoSQL(DynamoDB Single-digit ms, Global Tables Multi-Region Active-Active), 캐시(ElastiCache Redis/Memcached) |
| **메시징/이벤트** | 비동기 결합 | SQS(표준/순서/FIFO), SNS(Pub/Sub Fan-out), EventBridge(75+ SaaS 이벤트 버스), Kinesis Data Streams(실시간 스트림), MSK(Kafka 완전관리) |
| **보안·거버넌스** | 정책·감사 | IAM(Policy-based, ABAC), KMS(Customer Managed Key, Envelope Encryption), Secrets Manager(자동 회전), GuardDuty(위협 탐지), Macie(PII 자동 분류) |
| **옵저버빌리티** | 가시성 | CloudWatch(메트릭/로그), X-Ray(분산 트레이싱), CloudTrail(API 감사), OpenTelemetry SDK 통합, SLO 기반 Error Budget 운영 |

**핵심 알고리즘·파라미터**:
- **Quorum 기반 복제**: DynamoDB는 `(N, R, W)` 파라미터(예: N=3, R=2, W=2)로 일관성·가용성 조절. R+W > N이면 Strong Read, W > N/2이면 Strong Write
- **Consistent Hashing**: DynamoDB/Cassandra가 데이터를 Partition Key 해시로 16384개 vNode에 분산, 가상 노드로 리밸런싱 최소화
- **AIMD(Additive Increase Multiplicative Decrease)**: TCP 혼잡제어 + AWS EBS Burst Balance로 처리량 안정화
- **Bloom Filter**: RocksDB 내부에서 존재하지 않는 키 lookup을 1회 메모리 접근으로 차단 -> I/O 절감

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"교향곡 지휘자"**와 같다 — 1번 바이올린(웹), 2번 바이올린(API), 비올라(메시지), 첼로(데이터베이스) 각 파트(서비스)가 악보(IaC)대로 연주하되, 지휘자(Control Plane)가 템포(SLO)와 다이내믹(Scaling)을 실시간 조율한다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처 패턴은 비슷한 이름의 패턴들이 각기 다른 트레이드오프를 가지므로 정확한 비교가 필수다. 기술사 시험에서는 "왜 A가 아니라 B인가?"를 5가지 이상의 기준으로 정량 비교해야 한다.

| 구분 | **Monolith** | **Microservices (Cloud-Native)** | **Serverless (FaaS)** |
| :--- | :--- | :--- | :--- |
| **배포 단위** | 1개 WAR/EAR | 수십~수백 컨테이너 | 개별 함수(수천 개) |
| **확장 단위** | 전체 인스턴스 복제 | 서비스별 Pod | 호출 단위 (1 req = 1~N invocations) |
| **콜드 스타트** | N/A | 1~3초(EKS 첫 Pod) | Lambda 100ms~2s, EFS mount 시 5s+ |
| **실행 시간 한계** | 무제한 | 무제한 | Lambda 15분, Step Functions로 우회 |
| **상태 관리** | In-Memory Session | DB/Redis 분리 | 반드시 외부(DynamoDB/S3), Stateless only |
| **비용 모델** | 고정 인스턴스 비용 | 컨테이너 시간당 과금 | 호출 100ms 단위 과금, 유휴 시 $0 |
| **장애 격리** | 프로세스 단위, 메모리 leak 시 전체 영향 | Namespace/Network Policy로 격리 | 함수별 격리, Concurrent Execution 한도 |
| **DevOps 복잡도** | 단일 CI/CD | Service Mesh(Istio), ArgoCD, Skaffold | IaC(Terraform) + SAM/CDK, ZIP 업로드 |
| **적합 워크로드** | 소규모 CRUD, 레거시 | 중·대규모 트래픽, 도메인 분리 명확 | 이벤트 드리븐(파일/메시지/크론), 트래픽 변동 큼 |
| **대표 사례** | SAP, 사내 행정 | Netflix 700+ 서비스, 쿠팡 카탈로그 | AWS Lambda + S3 Image Resize, Alexa Skill |

**연계 기술 통합 패턴**:
- **API Gateway + Lambda + DynamoDB**: 3-Tier를 완전관리형으로 구성, Auto Scaling 0->수천, 사용량 0 시 비용 $0
- **EKS + Karpenter + Spot**: Pod 스케줄러가 Spot 인스턴스 Interrupt(2분 전 알림) 시 On-Demand로 자동 마이그레이션
- **CloudFront + Lambda@Edge**: 사용자 위치별 응답 변환, TLS Termination, A/B 테스트를 엣지에서 처리, RTT 50~200ms 단축
- **S3 + Athena + Glue Data Catalog**: 데이터 레이크의 Schema-on-Read, 1TB 스캔 $5, Parquet/ZSTD로 90% 비용
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 623 / 800

<- **이전**: [622. 클라우드 아키텍처 핵심 토픽 622번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/622_cloud_architecture_core_topic_622_exam_summar/)
**다음**: [624. 클라우드 아키텍처 핵심 토픽 624번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/624_cloud_architecture_core_topic_624_exam_summar/) ->

---
