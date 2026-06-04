---
title: "657. 클라우드 아키텍처 핵심 토픽 657번 시험 요약 (Cloud Architecture Core Topic 657 Exam Summary)"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 AWS Well-Architected Framework의 5대 원칙(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화)을 기반으로 **가용성·내결함성·확장성·보안·비용**을 Trade-off Matrix로 균형화하는 분산 시스템 설계 체계이며, SLO/SLI 기반의 정량적 의사결정과 Control Plane/Data Plane 분리가 핵심이다.
> 2. **가치**: CAP 정리를 실증적으로 해소하여 **단일 리전 RDS 대비 Multi-Region Active-Active 구성으로 가용성 99.95%→99.99%(연간 다운타임 4.38h→52.6m)** 달성, Auto Scaling과 Spot Instance 조합으로 컴퓨팅 비용 **60~80% 절감**, Serverless 전환으로 운영 오버헤드 **70% 감소** 등 정량적 효과를 입증한다.
> 3. **판단 포인트**: 동시성(Consistency)·분할 내성(Partition Tolerance)·가용성(Availability) 간 Trade-off, **Strong Consistency vs Eventual Consistency 선택**, **Synchronous Replication(동기) vs Asynchronous(비동기)** RPO/RTO 결정, **단일 VPC vs Transit Gateway Hub-Spoke**, **Monolith vs Microservices vs Serverless** 분해 기준이 핵심 결정 변수다.

---

## Ⅰ. 개요 및 필요성

전통적인 On-Premise 3-Tier 아키텍처는 CAPEX 중심의 수직적 확장(Scale-Up) 방식으로, 트래픽 변동성에 대응하기 위해 **항상 최대 부하 기준으로 과잉 프로비저닝(Over-provisioning)** 이 필요했다. 이는 평균 자원 활용률 15~25%의 비효율과, 단일 장애점(SPOF)으로 인한 가용성 99.9%(Three-Nines) 한계를 야기했다.

클라우드 아키텍처는 이를 **수평적 확장(Scale-Out) + 탄력성(Elasticity) + 셀프서비스 프로비저닝 + 사용량 기반 과금(Pay-as-you-go)** 으로 전환한다. 핵심 패러다임 전환은 ① Infrastructure as Code(Terraform/CloudFormation) 기반 선언적 인프라, ② 컨트롤 플레인(API/관리)과 데이터 플레인(트래픽 처리)의 분리, ③ 불변 인프라(Immutable Infrastructure)와 카나리/블루그린 배포, ④ SLO 기반 엔지니어링(SRE)이다.

```text
[클라우드 아키텍처 패러다임 전환 비교도]

  ┌──────────── On-Premise 3-Tier ─────────────┐    ┌──── Cloud-Native 12-Factor ────┐
  │                                            │    │                                │
  │   Client ──▶ Web ──▶ WAS ──▶ DB            │    │   CDN ──▶ API GW ──▶ Lambda    │
  │              (1EA)   (1EA)   (1EA)         │    │         ▼         ▼            │
  │              │        │        │            │    │      WAF       SQS/SNS         │
  │              ▼        ▼        ▼            │    │       │          │             │
  │          물리서버    물리서버   RDBMS         │    │       ▼          ▼             │
  │          (과잉구성)   (Scale-Up) (Active/Passive)│    │   ALB/NLB   DynamoDB        │
  │                                            │    │       │          │             │
  │   CAPEX $500K, 4개월 구축, 가용성 99.9%     │    │   ElastiCache   S3            │
  │   활용률 15~25%, MTTR 4h                    │    │                                │
  └────────────────────────────────────────────┘    │   OPEX Pay-per-Use, 1일 구축  │
                                                     │   가용성 99.99%, 활용률 60~80% │
                                                     │   MTTR < 5min (Auto Healing)  │
                                                     └────────────────────────────────┘
```

온프레미스 대비 클라우드는 **선제적 용량 계획(Capacity Planning)에서 반응적 자동 스케일링(Reactive Auto Scaling)** 으로 전환하며, AWS Auto Scaling Group의 **Desired/Min/Max Capacity 정책**과 **Target Tracking(P:70%), Step Scaling, Scheduled Scaling** 조합으로 동적 워크로드에 대응한다. 또한 **Multi-AZ(Multi-Availability Zone)** 토폴로지를 통해 99.99% 가용성을, **Multi-Region Active-Active**로 99.999%(Five-Nines)를 달성한다.

- **📢 섹션 요약 비유**: 기존 식당은 요리사가 한 명이라 손님이 몰리면 줄이 길어지고(Scale-Up 한계), 주방에 불이나면 문을 닫아야 합니다(SPOF). 클라우드 식당은 주문이 들어올 때마다 자동으로 요리사가 나타나고(Auto Scaling), 여러 개의 주방이 동시에 운영되어(Multi-AZ) 한 곳이 불나도 다른 곳에서 음식을 만듭니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **Well-Architected Framework의 5대 기둥**을 만족하는 계층형 분산 시스템이다. Control Plane은 API 호출로 리소스 상태를 정의하고, Data Plane은 실제 사용자 트래픽을 처리한다. 두 플레인 분리는 보안(최소 권한 IAM)과 안정성(제어 트래픽 장애 격리)의 기반이다.

```text
[Multi-Tier Cloud-Native 아키텍처 상세 흐름도]

                     ┌──────────────── Global Edge ────────────────┐
                     │   Route 53 (Latency/Geolocation Routing)     │
                     │   + CloudFront (CDN, 216 PoP, Origin Shield) │
                     └──────────────┬───────────────────────────────┘
                                    │ HTTPS
                                    ▼
                     ┌──────────────── Regional Edge ───────────────┐
                     │   AWS WAF (OWASP Top 10, Rate-based Rule)   │
                     │   AWS Shield Advanced (DDoS L3/L4/L7)       │
                     │   API Gateway (Throttling 10K RPS, Usage Plan)│
                     └──────────────┬───────────────────────────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                ▼                   ▼                   ▼
        ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
        │   ALB (L7)   │    │   NLB (L4)   │    │   GWLB (L3)  │
        │   Cross-AZ   │    │   Static IP  │    │   3rd-Party   │
        │   Sticky Ses │    │   UDP/TCP    │    │   NGFW         │
        └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
               │                   │                   │
   ┌───────────┴────┐    ┌────────┴────┐    ┌─────────┴────┐
   ▼                ▼    ▼             ▼    ▼              ▼
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│ ECS/EKS │  │ ECS/EKS │  │   EC2    │  │   EC2    │  │   EC2   │
│ Fargate │  │ Fargate │  │ Auto Sc. │  │ Auto Sc. │  │ ASG     │
│ AZ-a    │  │ AZ-c    │  │ AZ-a     │  │ AZ-b     │  │ AZ-c    │
└────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘
     │            │            │            │            │
     └────────────┴─────┬──────┴────────────┴────────────┘
                        │
              ┌─────────┼─────────┐
              ▼         ▼         ▼
        ┌─────────┐ ┌─────────┐ ┌──────────┐
        │ RDS MSSQL│ │Aurora   │ │DynamoDB  │
        │ Multi-AZ │ │Global DB│ │Global    │
        │ (Sync)   │ │(Async)  │ │Table(MR) │
        └─────────┘ └─────────┘ └──────────┘
              │         │         │
              └─────────┴────┬────┘
                             ▼
                    ┌─────────────────┐
                    │  ElastiCache    │
                    │  Redis (Cluster)│
                    │  Read Replica×3 │
                    └─────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Route 53** | DNS 기반 글로벌 트래픽 관리 | Latency-Based Routing(50ms 내 최적 리전), Geolocation, Weighted, Failover 정책, Health Check(30s 간격, 3회 실패 시 Failover) |
| **CloudFront** | 엣지 캐싱 및 TLS 종료 | TTL 기반 Cache-Control, Origin Shield(Origin 부하 50%↓), Lambda@Edge로 L7 로직, OAC/OAI로 S3 보안 |
| **WAF + Shield** | L7/L3·L4 보안 | Managed Rule(20+ 규칙 세트), Rate-Based Rule(2,000 req/5min), Shield Advanced는 DDoS 비용 보장 |
| **API Gateway** | API 라우팅/인증/스로틀링 | REST API(HTTP API 대비 29% 저렴), Lambda Authorizer(Cognito/JWT), Usage Plan으로 API Key별 Quota |
| **ALB/NLB** | L4/L7 로드밸런싱 | ALB: Path/Host-based, WSS 지원, Connection Draining 300s / NLB: Static IP, 100만 TPS, TLS Passthrough |
| **ECS/EKS/Fargate** | 컨테이너 오케스트레이션 | ECS Task Definition(CPU/mem), EKS는 K8s API 100% 호환, Fargate는 서버리스(Per Second 과금) |
| **RDS Multi-AZ** | 관계형 DB 고가용성 | Synchronous Replication(Same Region), Standby 자동 Failover(60~120s), Read Replica는 Async로 다른 리전 복제 |
| **Aurora Global DB** | 글로벌 분산 RDBMS | Cross-Region Async Replication(RPO < 1s), 5×Secondary Read Replica, Storage Auto-Scaling(10GB→128TB) |
| **DynamoDB** | NoSQL Key-Value (서버리스) | Single-digit ms Latency, DAX(10× 성능), Global Table(Multi-Region Active-Active, Eventually Consistent), On-Demand/Provisioned |
| **S3 + Glacier** | 객체 스토리지 + 아카이빙 | 11 9s(99.999999999%) 내구성, Lifecycle Policy(IA→Glacier→Deep Archive), Intelligent-Tiering 자동 계층 이동 |

**핵심 알고리즘 및 파라미터**:
- **Auto Scaling Target Tracking**: `desired_capacity = ceil(metric_value / target_value × current_capacity)`. 예: CPU 70% 유지를 Target으로, 현재 10대@90%면 신규 3대 Launch.
- **DynamoDB Consistent Hashing**: Partition Key를 MD5 해시 후 0~1023 사이 10MB 단위 Partition 분배, **Hot Partition 방지 위해 Composite Key** (예: `UserID#YYYY-MM`).
- **RDS Connection Pooling**: RDS Proxy로 Lambda 동시성 1만일 때 connection 폭주 방지, IAM Auth 통합, Failover 31s 단축.
- **CAP Theorem 적용**: 금융 결제 → Strong Consistency(RDS, 단일 리더) / SNS 피드 → Eventual Consistency(DynamoDB Global Table, SQS).

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 종합병원과 같습니다. 접수실(Route 53)이 응급실 응급도를 분류하고, 대기실(API Gateway)에서 환자 흐름을 조절하며, 각 진료과(ALB→ECS)가 병렬로 진료를 보고, 검사실(RDS)과 약국(DynamoDB)은 24시간 데이터를 공유합니다. 한 명의 의사가 아파도 다른 의사가 즉시 환자를 봐주는 것이 Multi-AZ입니다.

---

## Ⅲ. 비교 및 연결

| 구분 | Monolith (전통 3-Tier) | Microservices (ECS/EKS) | Serverless (Lambda) |
| :--- | :--- | :--- | :--- |
| **배포 단위** | WAR/EAR (10~100MB, 1개) | Container Image (50~500MB, 10~100개) | Function (ZIP 50MB, 100~1000개) |
| **확장 단위** | Instance 전체 복제 | 개별 서비스/Task | 함수 단위 동시성(Concurrency) |
| **Cold Start** | 없음 (Always-on) | 10~30s (이미지 pull) | 100ms~5s (Init Code) |
| **최소 비용** | EC2 1대 분당 과금 | ECS on EC2 또는 Fargate vCPU·mem | 1ms 단위 과금, 100만 req/월 무료 |
| **트래픽 변동 대응** | 수동 Scale-Up, MTTR 수 시간 | Auto Scaling 2~3분, HPA/VPA | 자동 0→1000 동시성, 100ms 스케일 |
| **장애 격리** | 프로세스 1개 = 전체 장애 | 서비스 단위 격리, Circuit Breaker(Hystrix) | Function 단위 격리, DLQ로 실패 분리 |
| **적합 워크로드** | 레거시 통합, 단순 CRUD, 트랜잭션 무결성 핵심 | 대규모 분산, Polyglot, 독립 릴리즈 | Event-Driven, 간헐적/예측불가 트래픽, API |
| **대표 사례** | ERP, 정부 시스템 | Netflix(700+ 마이크로서비스), Amazon | Netflix Image Processing, Coca-Cola Vending |
| **Trade-off** | 단순/성능↑, 유연성↓ | 복잡도↑, DevOps 성숙도 필요 | Cold Start↓, Vendor Lock-in↑, 디버깅 어려움 |

**연계 기술**:
- **CI/CD**: CodeCommit → CodeBuild → CodeDeploy(Blue/Green or Canary 10%→100%) → CodePipeline(워크플로우 오케스트레이션), GitOps(ArgoCD/Flux for EKS).
- **관측성(Observability)**: CloudWatch Metrics/Logs/Events + X-Ray(Distributed Tracing, 5분내 SLO 위반 알람) + CloudTrail(API 감사 로그).
- **IaC(Infrastructure as Code)**: Terraform(Multi-Cloud, HCL 선언형) vs CloudFormation(AWS 전용, JSON/YAML) vs CDK(TypeScript/Python 코드로 IaC 작성).
- **보안**: IAM Role + KMS(Envelope Encryption) + Secrets Manager(자동 Rotation) + GuardDuty(ML 기반 이상 탐지) + Config(규정 준수 평가).
- **비용**: Cost Explorer + Budgets(80% 알림) + Savings Plans(1~3년 약정, 72%↓) vs Reserved Instance(특정 인스턴스) vs Spot(90%↓, Interrupt 가능).

- **📢 섹션 요약 비유**: Monolith는 1권으로 된 백과사전, Microservices는 위키피디아(항목별 독립 수정), Serverless는 검색 엔진(필요한 답만 즉시 생성)입니다. 백과사전은 한 페이지 뜯으면 전체가 손상되지만, 위키피디아는 한 항목 오류가 전체를 망치지 않습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **가용성 목표(SLO) 정의 및 AZ/Region 분산 결정**: RPO/RTO 요건에 따라 Multi-AZ(Sync, RPO=0, RTO=60s), Multi-Region DR(Async, RPO<5min, RTO<1h), Multi-Region Active-Active(DynamoDB Global, RPO<1s, RTO=0) 중 선택. **금융권**은 동기 복제, **콘텐츠**는 비동기 + S3 CRR로 비용 최적화.
2. **데이터 일관성 모델 선택**: Strong(관계 무결성, 단일 리더) vs Eventual(가용성 우선, 다중 리더). **결제/재고** → Strong(RDS Single Writer + Read Replica, 또는 Aurora), **좋아요/댓글** → Eventual(DynamoDB + SQS로 변경 이벤트 전파). **DynamoDB Transactions**(ACID)나 **Saga Pattern**(Choreography vs Orchestration) 활용 여부 검토.
3. **
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 657 / 800

<- **이전**: [656. 클라우드 아키텍처 핵심 토픽 656번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/656_cloud_architecture_core_topic_656_exam_summar/)
**다음**: [658. 클라우드 아키텍처 핵심 토픽 658번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/658_cloud_architecture_core_topic_658_exam_summar/) ->

---
