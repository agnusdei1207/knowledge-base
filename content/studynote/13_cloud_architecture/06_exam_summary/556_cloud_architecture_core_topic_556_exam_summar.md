---
title: "556. 클라우드 아키텍처 핵심 토픽 556번 시험 요약 (Cloud Architecture Core Topic 556 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 **탄력성(Elasticity)**, **내결함성(Fault Tolerance)**, **불변 인프라(Immutable Infrastructure)**를 코드(Code)로 선언하여, AWS Well-Architected Framework 5대 원칙(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화)과 12-Factor App 방법론을 통해 CAP定理와 PACELC 트레이드오프 하에서 가용성/일관성 목표를 달성하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: AWS, Azure, GCP의 관리형 서비스를 활용 시 인프라 프로비저닝 시간은 **주 단위 -> 분 단위(±90%)**, CAPEX는 **OPEX 전환으로 약 30~40% TCO 절감**, Auto Scaling과 Multi-AZ 구성을 통해 **SLA 99.99%(연 52분 이내 장애)** 달성이 가능하며, Reserved Instance/ Savings Plan을 통한 비용 최적화 시 동일 워크로드 대비 **최대 72% 비용 절감** 효과를 얻는다.
> 3. **판단 포인트**: 핵심 의사결정은 ①**단일 클라우드 vs 멀티/하이브리드**(잠금 효과 vs 운영 복잡성), ②**모놀리식 vs 마이크로서비스**(배포 속도 vs 분산 트랜잭션 복잡도), ③**베어메탈/EC2 vs 컨테이너/EKS vs 서버리스/Lambda**(콜드 스타트 vs 세밀한 제어), ④**동기 vs 이벤트 드리븐**(Strong Consistency vs 최종 일관성), ⑤**Lift & Shift vs Cloud-Native Refactoring**(단기 마이그레이션 vs 장기 TCO 최적화) 등 5개 축의 트레이드오프 분석을 통해 결정한다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 데이터센터 아키텍처는 **수직 확장(Scale-Up)**, **정적 용량 계획(Capacity Planning)**, **수동 패치/배포**를 기반으로 하였으며, CAPEX 중심의 5~7년 교체 주기를 통해 약 **30~40%의 유휴 자원**이 발생하고, 신규 서비스 출시까지 **평균 6~12주**가 소요되는 구조적 한계를 지닌다. 디지털 전환(Digital Transformation) 가속화와 트래픽의 비선형적 변동(블랙프라이데이, 코로나19 사례: 줌(ZOOM)은 2020년 3월 DAU 1,000만 -> 2억으로 폭증), 그리고 BaaS·BaaS·SaaS 산업 전반의 API 기반 비즈니스 모델 확장으로 인해 **탄력적 확장(Elastic Scaling)**, **셀프서비스 프로비저닝**, **사용량 기반 과금(Pay-per-Use)**이 가능한 클라우드 네이티브 아키텍처가 필수 요소로 자리잡았다.

NIST SP 800-145는 클라우드 컴퓨팅을 ①**온디맨드 셀프서비스**, ②**광대역 네트워크 접근**, ③**자원 풀링**, ④**신속한 탄력성**, ⑤**측정 가능한 서비스**의 5대 필수 특성으로 정의하며, 이를 통해 SPI(SaaS/PaaS/IaaS) 3계층 서비스 모델과 Public/Private/Hybrid/Community 4종 배치 모델로 분류한다.

```text
[클라우드 아키텍처 패러다임 전환 흐름]

  +------------------+         +------------------+         +------------------+
  |   On-Premise     |  --->    |   Virtualized    |  --->    |  Cloud-Native    |
  |   (2000 이전)     |  하이퍼  |   (2005~2015)     |  도커/  |   (2015~현재)     |
  |                  |  바이저  |                   |  쿠버네 |                  |
  | • 수직확장        |  --->    | • 수평확장 시작    |  티스   | • 마이크로서비스   |
  | • Static Infra   |         | • VMware vSphere |  --->    | • Immutable Infra|
  | • 수동 운영       |         | • 수동/반자동     |         | • GitOps, IaC    |
  | • CAPEX 100%     |         | • CAPEX+OPEX     |         | • OPEX 중심      |
  +------------------+         +------------------+         +------------------+
                                                                       |
                                                                       v
                                                          +----------------------+
                                                          |  AI-Native/Serverless|
                                                          |  (2024~미래)          |
                                                          |  • LLM 통합           |
                                                          |  • Function-as-a-    |
                                                          |    Service 범용화     |
                                                          +----------------------+
```

클라우드 아키텍처의 필요성은 **①TCO 절감**(IDC 보고서: 3년 기준 평균 30~51% 절감), **②Time-to-Market 단축**(Netflix 사례: 스피드 기반 DevOps 문화로 주 1,000+회 배포), **③글로벌 가용성**(리전 간 복제로 자연재해 대응), **④보안/규제 준수 자동화**(ISO 27001, SOC 2, PCI-DSS 인증 자동 상속)의 4대 가치에서 기인한다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **"전력 자가발전(온프레미스)에서 전력회사 배전망 전환"**과 같다. 발전기를 직접 운영·유지보수하지 않고, 필요할 때만 전기를 끌어다 쓰는 모델로, 설비 투자 없이 즉시 사용·확장·결제가 가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **프레젠테이션 계층(CDN/Load Balancer)**, **애플리케이션 계층(Stateless Service)**, **데이터 계층(Polyglot Persistence)**, **인프라 계층(IaC/Immutable Image)**의 4계층 논리 구조로 설계되며, **12-Factor App**과 **AWS Well-Architected Framework 5대 기둥**이 핵심 설계 원칙으로 작동한다.

```text
[AWS Well-Architected Framework 기반 표준 참조 아키텍처]

                           +-----------------------------------------+
                           |  Route 53 (DNS + Health Check + GeoDNS) |
                           +--------------------+--------------------+
                                                | TLS 1.3
                                                v
   +----------------------------------------------------------------------+
   |  CloudFront / Cloud CDN (정적·동적 컨텐츠 캐싱, 엣지 로케이션 600+)  |
   +------------------------------------+---------------------------------+
                                        |
                                        v
   +----------------------------------------------------------------------+
   |  ALB (L7) / NLB (L4) --- WAF (OWASP Top 10 방어, Rate Limit)        |
   |  +-- Target Group: Multi-AZ Auto Scaling Group (EC2 ASG)             |
   |  +-- Target Group: ECS Fargate / EKS Pod (HPA + VPA + KEDA)         |
   |  +-- Target Group: AWS Lambda (동시성/예열/Provisioned Concurrency) |
   +------------------------------------+---------------------------------+
                                        |
              +-------------------------+-------------------------+
              v                         v                         v
   +------------------+     +------------------+     +------------------+
   |  Amazon Aurora   |     |  Amazon DynamoDB |     |  ElastiCache     |
   |  MySQL/PostgreSQL |     |  (NoSQL,         |     |  Redis/Memcached |
   |  Multi-AZ +      |     |   Global Tables, |     |  Cluster Mode)   |
   |  Read Replica    |     |   DAX, Streams)  |     |                  |
   +------------------+     +------------------+     +------------------+
              |                         |                         |
              +-------------------------+-------------------------+
                                        v
   +----------------------------------------------------------------------+
   |  Amazon S3 (Versioning + Cross-Region Replication + Object Lock)    |
   |  +-- Glacier / Glacier Deep Archive (라이프사이클 정책: IA->Glacier) |
   +----------------------------------------------------------------------+

   +----------------------------------------------------------------------+
   |  [관측가능성 계층]                                                    |
   |  CloudWatch(Metrics/Logs) + X-Ray(분산 트레이싱) + CloudTrail(Audit)|
   |  + EventBridge(이벤트 버스) + SNS/SQS(비동기 메시징)                |
   +----------------------------------------------------------------------+

   +----------------------------------------------------------------------+
   |  [거버넌스 계층] IaC: Terraform / CloudFormation / CDK              |
   |  + Policy: SCP(Service Control Policy) + IAM + AWS Config          |
   +----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Edge / CDN** | 글로벌 정적·동적 컨텐츠 전송, DDoS 방어, TLS 종료 | CloudFront(AWS), Azure Front Door, Cloud CDN(GCP); PoP(Point of Presence) 기반 Anycast 라우팅, Lambda@Edge로 엣지 컴퓨팅 수행. 캐시 적중률(Cache Hit Ratio) 90% 이상 권장 |
| **로드밸런서** | L4/L7 트래픽 분산, Health Check 기반 자동 페일오버 | ALB(L7, Path/Host 기반 라우팅, gRPC 지원), NLB(L4, 초당 수백만 요청, 고정 IP), GWLB(3계층 어플라이언스). 알고리즘: Round Robin, Least Outstanding Requests, Weighted, IP Hash |
| **컴퓨트 계층** | Stateless 워크로드 실행, Auto Scaling | EC2(베어메탈 Graviton4 ARM 기반, c7i/r7i), ECS Fargate(서버리스 컨테이너, 0.25vCPU~16vCPU), EKS(쿠버네티스 오케스트레이션), Lambda(15분 타임아웃, 10GB 메모리). HPA는 CPU 70% 임계치, KEDA는 Kafka/CloudWatch 이벤트 기반 0-스케일링 |
| **데이터 계층 (Polyglot)** | 워크로드별 최적 저장소 선택 | RDB(Aurora: 5× MySQL, 3× PostgreSQL 성능, Storage Auto-Scaling), NoSQL(DynamoDB: 단일 리전 p99 1-digit ms, Global Tables 다중 리전 액티브-액티브), 캐시(ElastiCache Redis Cluster: 250 노드, 68TiB 메모리), 검색(OpenSearch), 시계열(Timestream), 그래프(Neptune) |
| **메시징 / 비동기** | 서비스 간 느슨한 결합(Loose Coupling), 백프레셔 처리 | SQS(Standard: Best-Effort 순서·중복, FIFO: 정확한 순서, Visibility Timeout 12시간), SNS(Fan-out Pub/Sub), EventBridge(53개 AWS 서비스 이벤트 라우팅, Schema Registry), Kinesis Data Streams(Shard당 초당 1,000 레코드, 1MB/s) |
| **스토리지 계층** | 객체/블록/파일/아카이브 분리 | S3(11 9's 내구성, 4 9's 가용성 Standard, IA 30일 후, Glacier 90일 후, Intelligent-Tiering ML 기반 자동 계층 이동), EBS(gp3: 125MB/s~1,000MB/s, IOPS 3,000~16,000), EFS(NFS v4, Bursting/Provisioned Throughput), FSx(Lustre HPC용) |
| **보안 / IAM** | 최소 권한(Zero Trust), 암호화, 감사 | IAM Role + SCP(Service Control Policy), KMS(자동 키 회전, BYOK/Hold Your Own Key), Secrets Manager(자동 로테이션, RDS 통합), GuardDuty(ML 기반 이상 탐지), Macie(데이터 분류 PII), Security Hub(CIS/NIST 통합 점수) |
| **관측가능성 (Observability)** | 메트릭·로그·트레이스 3대 신호 + 이벤트 | CloudWatch Logs Insights(10PB 규모), X-Ray(서비스 맵 자동 생성, 샘플링 규칙), Grafana/Prometheus, OpenTelemetry(표준 계측), SLO 기반 알람(Error Budget 30일 누적) |

**핵심 동작 메커니즘**:
- **Auto Scaling의 3단계 의사결정**: ①CloudWatch Metric(CPU/메모리/큐 길이) 발생 -> ②Step Scaling/Target Tracking Policy 평가 -> ③EC2/ECS 인스턴스 추가 후 ALB Target Group에 자동 등록, Health Check Grace Period(기본 300초) 통과 후 트래픽 수신. **Cooldown Period**(기본 300초)는 스케일링 진동 방지.
- **불변 인프라 배포 패턴**: AMI/Packer로 베이스 이미지 생성 -> CodeDeploy의 Blue/Green(In-Place 또는 Canary 10%->50%->100%, 5분 간격) 또는 롤링 배포 -> CloudFormation Stack의 Auto Scaling Group Refresh로 인스턴스 교체. 롤백은 스냅샷/S3 버전 또는 Git Commit Revert로 수행.
- **결함 도메인 분리의 수학적 근거**: AWS 리전은 **가용 영역(AZ) 3개 이상**(물리적 데이터센터 분리, 광케이블 이중화, 독립 전력·냉각)으로 구성되며, Multi-AZ RDS는 동기식 복제(commit 시 2개 AZ 동기 쓰기)로 RPO=0, RTO 약 60~120초 달성. Multi-Region은 비동기 복제로 RPO 수 초~수 분.

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 4계층은 **"택배 물류 시스템"**과 같다. CDN은 **가까운 집배 센터**(엣지 캐싱), ALB는 **물류 분류 센터**(라우팅), Auto Scaling은 **배송 차량 동적 배차**(탄력성), S3는 **장기 창고**(내구성 11 9's), CloudWatch는 **CCTV·GPS 추적**(관측가능성)이다.

---

## Ⅲ. 비교 및 연결

| 구분 | IaaS (EC2) | PaaS (Elastic Beanstalk / App Runner) | SaaS (Salesforce / Workday) | FaaS (Lambda) |
| :--- | :--- | :--- | :--- | :--- |
| **제어 범위** | OS, 미들웨어, 런타임, 데이터, 앱 | 앱, 데이터만 | 앱 사용만 (No Code) | 함수 코드만 |
| **책임 분담 (AWS Shared Responsibility)** | 고객: OS 패치, 네트워크, 데이터 / AWS: 하드웨어, 물리 보안 | AWS: OS~런타임 관리 | AWS: 전 계층 | AWS: 전 계층 (고객: 코드 + IAM만) |
| **확장 단위** | 인스턴스 단위 (수 분) | 인스턴스 단위 (수 분) | 사용자 단위 라이선스 | 요청 단위 (밀리초) |
| **콜드 스타트** | 없음 | 없음 | 없음 | 100ms~수 초 (Java/Python 100ms, .NET 200~300ms, Node.js 100~200ms) |
| **적합 워크로드** | 레거시, 커스텀 OS, GPU/네트워크 튜닝 | 빠른 웹앱 배포, 표준 스택 | CRM, HR, 협업, 정형업무 | 이벤트 드리븐, 짧은 비동기 작업, ETL |
| **단가 모델** | On-Demand/Reserved/Spot(최대 90%v) | 인스턴스 기반 + PaaS 프리미엄 | 사용자당/월 구독 ($25~150/user) | GB-초(메모리 128MB~10GB) + 호출 수 ($0.20/1M req) |
| **예시 비용 (1년, t
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 556 / 800

<- **이전**: [555. 클라우드 아키텍처 핵심 토픽 555번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/555_cloud_architecture_core_topic_555_exam_summar/)
**다음**: [557. 클라우드 아키텍처 핵심 토픽 557번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/557_cloud_architecture_core_topic_557_exam_summar/) ->

---
