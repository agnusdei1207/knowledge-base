---
title: "Cloud Architecture Core Topic 547 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS의 서비스 모델과 Public/Private/Hybrid/Multi-Cloud의 배치 모델 위에서, CAP Theorem과 12-Factor App 원칙, AWS Well-Architected Framework(운영 우수성·보안·안정성·성능 효율·비용 최적화·지속 가능성 6대 필러)에 기반해 **확장성(Scale-out 우선)·탄력성(Auto Scaling)·장애 격리(Availability Zone + Region)**를 코어로 설계하는 것이다.
> 2. **가치**: 온프레미스 대비 CapEx->OpEx 전환(서버 도입 TCO 30~50% 절감), 트래픽 10배 변동 시 Auto Scaling으로 5분 내 100->1,000 EC2 인스턴스 확장, S3 11 9s(99.999999999%) durability, RDS Multi-AZ로 RPO 0초/RTO 60~120초 수준의 DR을 코드 한 줄로 달성 가능하다.
> 3. **판단 포인트**: 단일 장애점(SPOF) 제거를 위한 **단일 AZ 금지**, 동기/비동기 복제 선택(Synchronous: Strong Consistency vs Asynchronous: Latency 절감), Stateless 컴퓨트 + 외부 상태 저장(Redis/ElastiCache, DynamoDB, S3) 설계, 비용 최적화 시 Reserved/Spot/On-Demand 비율, Egress Data Transfer 비용(클라우드 비용의 20~40% 차지), 그리고 Shared Responsibility Model 경계 인식이 핵심 트레이드오프다.

---

## Ⅰ. 개요 및 필요성

전통적 3-tier 온프레미스 아키텍처(웹-WAS-DB)는 **수직적 확장(Scale-up)의 물리적 한계**(단일 서버 CPU 128코어, 메모리 4TB 벽), **발주-도입-설치 리드타임(주문 후 8~12주)**, **Capacity Planning 실패 시 90% Idle Resource 낭비**, 그리고 **DR(Disaster Recovery) 구축의 2~3배 중복 인프라 비용**이라는 4대 구조적 한계를 내포하고 있다. 2006년 AWS S3·EC2 출시 이후 클라우드 컴퓨팅은 "필요한 자원을 API 호출로 1분 내 공급받는" 유틸리티 컴퓨팅 모델로 전환되었으며, NIST SP 800-145는 5대 특성(온디맨드 셀프서비스, 광범위한 네트워크 접근, 리소스 풀링, 빠른 탄력성, 측정 가능한 서비스)을 정의했다.

```text
[클라우드 아키텍처 패러다임 전환: On-Premise -> Cloud-Native]
+------------------------------------------------------------------+
|   On-Premise 3-Tier (수직확장·예측 기반)                         |
|   +------+    +------+    +---------+    +------+              |
|   | F5   |---->| Web  |---->|   WAS   |---->| Oracle|             |
|   |L4/L7 |    | Tier |    |  (Tomcat)|   |  RAC  |              |
|   +------+    +------+    +---------+    +------+              |
|        ^ 단일장애점, 수직확장 한계, CapEx 과다, DR 비용 2배       |
+------------------------------------------------------------------+
                              v (2006~ AWS 출시, 2014~ K8s 등장)
+------------------------------------------------------------------+
|   Cloud-Native 12-Factor + MSA (수평확장·이벤트 기반)            |
|  +-------------------------------------------------------------+ |
|  | CDN(CloudFront) -> ALB -> EKS Pod Auto-scaling(1->1000)        | |
|  |     |              |                                        | |
|  |   WAF              +--> Lambda(Function URL) Event-driven     | |
|  |   Shield           +--> SQS -> S3(Lambda Trigger)             | |
|  |   (DDoS)           +--> DynamoDB / Aurora Global / ElastiCache| |
|  +-------------------------------------------------------------+ |
|        ^ 가용영역(AZ) 다중화, 리전(Region) 복제, IaC(Terraform)   |
+------------------------------------------------------------------+
```

기술사적 관점에서 클라우드 아키텍처는 단순한 "IDC 대체"가 아니라 **탄력성·무상태성·불변 인프라(Immutable Infrastructure)·API 기반 제어**라는 새로운 운영 패러다임이며, 이를 뒷받침하는 분산 시스템 8대 오해(Fallacies of Distributed Computing: 네트워크는 reliable하지 않다, latency는 0이 아니다, bandwidth는 무한하지 않다, 네트워크는 secure하지 않다, topology는 변하지 않는다, admin이 1명이라는 가정, transport cost는 0, network는 homogeneous)와 직접 연결된다. Gartner는 2025년 기준 신규 애플리케이션의 95%가 Cloud-Native 형태로 배포될 것으로 예측하며, 한국 NIPA 보고서에서도 공공·금융권의 클라우드 전환 가속화(클라우드컴퓨팅법 2022.1 시행)를 명시하고 있다.

- **📢 섹션 요약 비유**: 기존 온프레미스는 "직접 정수기를 사서 사무실에 설치하는 것"이고, 클라우드는 "수돗물을 누는 즉시 끝없이 받아 쓰는 것"이다. 정수기는 한 번 사면 5년 묶이지만, 수돗물은 사용한 만큼만 수도요금을 내며, 마실 사람이 100명이든 100만명이든 즉시 배관만 충분하면 공급된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **5대 계층**(Edge/Network/Compute/Storage/Data)과 **6대 설계 원칙**(느슨한 결합, 탄력성, 관측 가능성, 불변성, 선언적 API, 종량제)이며, AWS·Azure·GCP 모두 **Region(지역, 지리적 분리 단위) > Availability Zone(AZ, 1개 이상 데이터센터 군집, 동일 리전 내 100km 이내) > Edge Location(CloudFront/Fronteir 캐시 POP)**의 3단 위계를 따른다. AZ 간에는 **저지연 전용선(예: AWS Direct Connect, AZ 간 RTT < 1ms)**이 연결되어 Synchronous Replication이 가능하며, 리전 간은 **Public Internet 또는 전용 백본(예: AWS Global Backbone, Azure ExpressRoute)**을 통해 Asynchronous 복제된다.

```text
[클라우드 아키텍처 5계층 참조 모델: AWS 기준]
+--------------------------------------------------------------------+
| ① Edge Layer (엣지)                                               |
|    Route 53 (DNS GSLB/Health Check) -> CloudFront (CDN, 600+ POP)   |
|    -> WAF(OWASP Top10 룰셋) + Shield Advanced(L3/L4/L7 DDoS 방어) |
+--------------------------------------------------------------------+
| ② Network Layer (네트워크)                                         |
|    VPC(10.0.0.0/16) -> Subnet(Public/Private/DB 3-Tier)            |
|    -> Internet Gateway / NAT GW / Transit GW / VPC Peering         |
|    -> Security Group(Stateful, ENI 레벨) / NACL(Stateless, Subnet) |
|    -> ALB(L7, Path/Host 라우팅) / NLB(L4, 고정 IP, ms 단위)        |
+--------------------------------------------------------------------+
| ③ Compute Layer (컴퓨트)                                           |
|    EC2(IaaS) / ECS·EKS(Container) / Lambda(Serverless, 15분 timeout,|
|    10GB 메모리) / Fargate(서버리스 컨테이너) / Batch(HPC)          |
|    Auto Scaling Group: min/desired/max, Target Tracking(CPU 70%)   |
+--------------------------------------------------------------------+
| ④ Storage Layer (스토리지)                                         |
|    S3(Object, 11 9s) / EBS(Block, gp3 3,000 IOPS 무료) / EFS(NFS) |
|    / FSx(Windows/Lustre HPC) / S3 Glacier(아카이빙 0.004$/GB)     |
|    Lifecycle Policy: Standard -> IA(30일) -> Glacier(90일) -> Deep(180일)|
+--------------------------------------------------------------------+
| ⑤ Data Layer (데이터)                                              |
|    RDS(MySQL/PostgreSQL, Multi-AZ, Read Replica 최대 5개)          |
|    Aurora(MySQL/PG 호환, 6-way 복제, 15 9s Read Replica)           |
|    DynamoDB(NoSQL, p99 < 10ms, On-Demand/Provisioned)              |
|    ElastiCache(Redis/Memcached, Sub-ms latency) / Redshift(DWH)   |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Region / AZ** | 지리적·물리적 장애 격리 단위 | AWS 33개 리전/105개 AZ(2024), 동일 리전 AZ 간 RTT < 10ms, AZ 손실은 "공유 운명의 사례(Shared Fate)" 회피 목표로 Multi-AZ 분산 필수 |
| **컴퓨트 오퍼링 4종** | 워크로드 특성에 따른 런타임 선택 | EC2(장기 실행·제어권), ECS/EKS(컨테이너·이식성), Lambda(이벤트·최대 15분·콜드 스타트 100~500ms), Fargate(서버리스 컨테이너·vCPU/GB 단위 과금) |
| **스토리지 클래스** | 접근 빈도·내구성·비용 트레이드오프 | S3 Standard(11 9s, 0.023$/GB) -> IA(0.0125$) -> One Zone-IA(0.01$) -> Glacier Instant(0.004$, ms) -> Glacier Deep Archive(0.00099$, 12h 복원) |
| **데이터베이스 선택 기준** | 일관성·트랜잭션·지연시간 요구사항 | OLTP+관계형->RDS/Aurora, 초저지연 KV->DynamoDB(전역 테이블 다중 리전 active-active), 그래프->Neptune, 시계열->Timestream, 검색->OpenSearch(전체 텍스트·로그 분석) |
| **IaC & 관측성** | 코드형 인프라·운영 가시성 | Terraform/Pulumi/CloudFormation으로 리소스 선언, CloudWatch(Metrics+Logs+Alarms), X-Ray(분산 트레이싱), CloudTrail(API 감사 로그) |
| **메시지 & 이벤트** | 비동기·디커플링·배압(Backpressure) | SQS(Standard/Standard/FIFO, 256KB, 무제한 처리량), SNS(Fan-out Pub/Sub), EventBridge(88개 AWS 서비스 SaaS 이벤트 라우팅), Kinesis(실시간 스트림, 1MB/s 샤드) |
| **보안·컴플라이언스** | Shared Responsibility 구현 | IAM(최소권한, ABAC), KMS(CMK/Envelope Encryption, AES-256), Secrets Manager(자동 로테이션), GuardDuty(ML 기반 이상행위 탐지), Config(리소스 규정 준수 평가) |

핵심 알고리즘·파라미터 관점에서 **Auto Scaling**은 `TargetTrackingScaling`이 CloudWatch 지표(평균 CPU, ALB RequestCountPerTarget)와 비교하여 증감 결정하며, **Cooldown Period**(기본 300초)로 불필요한 진동 방지, **Predictive Scaling**은 ML로 14일 패턴 학습해 사전 확장한다. **CAP Theorem** 관점에서 RDBMS는 CA(단일 리전 Multi-AZ, 분할 허용), DynamoDB는 AP(다중 리전 활성-활성, eventually consistent 기본 1초 내 일관성), RDS Aurora Global은 동기 쓰기 리전 + 비동기 리전 확장으로 CP/AP 중간 지점을 취한다. **일관성 모델**은 Strong(쓰기 직후 모든 읽기 일관, Aurora), Read-your-writes(자신 세션은 즉시, 타 세션은 지연, DynamoDB Session Token), Eventually(< 1초, DynamoDB 기본), Bounded Staleness(50ms 이내, Cosmos DB)로 구분된다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "**전 세계에 흩어진 자동화 창고 네트워크**"와 같다. 서울·도쿄·버지니아 등 여러 Region(도시)에 각각 3개 창고(AZ)가 있고, 재고(S3 Object)는 자동으로 3개 창고에 복제되어 한 창고가 불나도 안전하다. 택배기사(데이터)는 가장 가까운 창고(ALB)에서 출발해 컨베이어(Kinesis) 위를 흐르고, 도난 감시 카메라(GuardDuty·CloudTrail)가 24시간 찍는다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처를 논할 때 가장 빈번하게 출제되는 비교는 **IaaS vs PaaS vs SaaS vs FaaS**, **Monolith vs Microservice**, **Synchronous vs Asynchronous Replication**, **Container vs Serverless**, **Single-Cloud vs Multi-Cloud vs Hybrid**이다.

| 구분 | IaaS (EC2, Azure VM) | PaaS (Elastic Beanstalk, App Engine) | SaaS (Salesforce, Slack) | FaaS (Lambda, Cloud Functions) |
| :--- | :--- | :--- | :--- | :--- |
| **제어 범위** | OS·미들웨어·런타임 모두 제어 | 앱 코드만 제어, OS/미들웨어 PaaS 관리 | 완성된 소프트웨어 사용 | 함수 코드만, 인프라 완전 위임 |
| **확장 단위** | 인스턴스(수 분 소요) | 인스턴스 또는 자동 컨테이너 | 사용자 단위 라이선스 | 동시 실행 수(1,000개 기본) |
| **콜드 스타트** | 없음(상시 기동) | 컨테이너 이미지 풀(< 1분) | 없음(공급자 관리) | 100~500ms (Provisioned Concurrency로 0ms 가능) |
| **적합 워크로드** | 레거시·특수 HW(GPU, FPGA) | 웹앱·API 백엔드 | CRM·문서·협업 | 이벤트 트리거·배치·글ue 코드 |
| **과금 모델** | 인스턴스 시간(On/Off 무관) | 인스턴스/요청 단위 | 사용자/월(Subscription) | 호출 수(ms 단위 과금) + GB-초 |

| 구분 | Monolith | Microservice (MSA) | Serverless API |
| :--- | :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/JAR | 독립 컨테이너/서비스 | Lambda Function |
| **장애 영향도** | 전체 장애(Blast Radius 큼) | 서비스 단위 격리 | Lambda 단위 격리 |
| **확장성** | 전체 복제(Scale Cube Y축) | 서비스별 독립(X축) | 자동 무제한 |
| **트랜잭션** | 단일 DB ACID 보존 | Saga / 2PC / Outbox 패턴 필요 | Step Functions로 보상 트랜잭션 |
| **운영 복잡도** | 낮음(하나만 관리) | 높음(서비스 수만큼 CI/CD·관측) | 중간(콜드 스타트·상태 관리) |
| **조직 정렬** | Conway 역법칙 위배 | 2-pizza team과 정렬 | 작은 팀 단위 |

**다른 기술과의 연결**: ① **Kubernetes(EKS/GKE/AKS)**는 컨테이너 오케스트레이션의 사실상 표준(de facto standard)이며, AWS·Azure·GCP 모두 managed K8s 서비스를 제공해 클라우드 네이티브 아키텍처의 운영 부담을 줄인다. ② **DevOps/GitOps**는 IaC(Terraform) + CI/CD(CodePipeline·ArgoCD) + Observability(Prometheus·Grafana) + Service Mesh(Istio·Linkerd)와 결합되어 "코드에서 프로덕션까지" 자동화한다. ③ **Zero Trust Architecture(NIST SP 800-207)**는 전통적 네트워크 경계 방식을 넘어 "**Never Trust, Always Verify**" 원칙으로 클라우드 IAM·mTLS·WAF·CSPM을 통합한다. ④ **SRE(Site Reliability Engineering)**는 Google SRE Book의 SLO/SLI/Error Budget 개념을 통해 "가용성 99.9% 달성을 위해 월 43분, 99.99
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 547 / 800

<- **이전**: [546. 클라우드 아키텍처 핵심 토픽 546번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/546_cloud_architecture_core_topic_546_exam_summar/)
**다음**: [548. 클라우드 아키텍처 핵심 토픽 548번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/548_cloud_architecture_core_topic_548_exam_summar/) ->

---
