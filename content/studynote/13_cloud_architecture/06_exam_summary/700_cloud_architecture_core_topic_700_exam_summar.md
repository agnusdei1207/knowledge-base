---
title: "Cloud Architecture Core Topic 700 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS의 서비스 모델 계층과 Public/Private/Hybrid/Multi-Cloud 배포 모델의 이원화된 의사결정 축 위에서, 12-Factor App, 클라우드 네이티브 컴퓨팅 파운데이션(CNCF) 기술 스택, AWS Well-Architected 6대 기둥(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화, 지속 가능성)을 통합적으로 적용한 분산 시스템 설계 패러다임이다.
> 2. **가치**: CAP Theorem 하에서 가용성(AP) 또는 일관성(CP) 트레이드오프를 명시적으로 선택하고, Auto Scaling을 통한 30~70% 인프라 비용 절감, Multi-AZ 배포로 99.99%(52.6분/년) 가용성 달성, Infrastructure as Code(Terraform/CloudFormation)로 배포 시간 95% 단축(수동 2주 -> 자동 30분) 등 정량적 효과를 입증할 수 있다.
> 3. **판단 포인트**: Stateless 워크로드의 컨테이너화(Kubernetes/EKS) vs Stateful 워크로드의 관리형 서비스(RDS/DynamoDB) 분리, 동기식(Sync) API vs 비동기식(EventBridge/SQS) 메시징 선택, 무중단 배포 전략(Blue-Green/Canary/Rolling), 그리고 Shared Responsibility Model 기반 보안 경계 설정이 핵심 의사결정 기준이다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 아키텍처는 CAPEX(자본 지출) 중심의 수직적 확장(Scale-Up) 모델로, 트래픽 예측 실패 시 과잉 투자(60% 이상 유휴 자원) 또는 서비스 장애를 동시에 야기했다. 2006년 AWS S3/EC2 출시 이후 IaaS가 본격화되었으며, 2014년 Kubernetes 1.0, 2019년 Cloud Native Computing Foundation 성숙, 2023년 생성형 AI 워크로드의 GPU 자원 탄력성 수요 폭증으로 클라우드 아키텍처는 **"Pay-per-Use Utility Computing"** 패러다임으로 정착되었다.

기술사 관점에서 클라우드 아키텍처의 필요성은 다음 4가지 핵심 동인에서 비롯된다:

1. **탄력성(Elasticity)**: 트래픽 변동성에 맞춘 자동 확장/축소 (예: 1,000 RPS -> 100,000 RPS 대응)
2. **가용성(Availability)**: Region/AZ 이중화로 99.99% SLA 달성
3. **민첩성(Agility)**: IaC 기반 프로비저닝으로 시장 출시 시간(TTM) 단축
4. **글로벌 확장성**: CDN/Edge Computing으로 전 세계 사용자 latency 200ms 이하 보장

```text
+-----------------------------------------------------------------+
|                클라우드 아키텍처 패러다임 전환 흐름               |
+-----------------------------------------------------------------+
|                                                                 |
|   [On-Premise Era]              [Cloud Era]                     |
|   +----------+                  +----------+                    |
|   | Monolith | ---------------►  |Microsvc. |                    |
|   |  rdbms   |   Microservices  | + k8s    |                    |
|   | 고정 cap |   Container     | + SAGA   |                    |
|   | 수직확장 |   Event-Driven  | + Server |                    |
|   +----------+                  |  less   |                    |
|                                 +----------+                    |
|   ❌ 수동 배포                 ✅ GitOps 자동화                  |
|   ❌ 장애 전파                 ✅ Circuit Breaker 격리           |
|   ❌ 수직확장 한계             ✅ 수평확장 무제한                 |
|   ❌ 라이선스 종속             ✅ Open API 기반                  |
|                                                                 |
+-----------------------------------------------------------------+
```

기존 레거시 대비 클라우드 네이티브의 차별점은 **불변 인프라(Immutable Infrastructure)** 와 **선언적 API(Declarative API)** 로 대표된다. 서버에 SSH 접속하여 패치하는 대신, 컨테이너 이미지를 새로 빌드하여 배포하는 방식은 Configuration Drift 문제를 원천 차단한다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "전기 요금제"와 같다. 발전소(데이터센터)를 직접 짓는 대신(온프레미스), 콘센트에 꽂아 쓰는 방식(IaaS)으로 초기 투자비를 0에 수렴시키고, 사용한 만큼만 비용을 지불하는 Utility 모델이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **계층화된 책임 분담(Shared Responsibility Model)** 과 **API 기반 제어 평면/데이터 평면 분리** 에 있다. AWS 기준으로 제어 평면(Control Plane)은 API 요청 라우팅·인증·메타데이터를 처리하고, 데이터 평면(Data Plane)은 실제 트래픽을 처리한다.

### 2.1 Well-Architected 6대 기둥 구조

```text
                    +---------------------------+
                    |  Cloud Architecture        |
                    |  Well-Architected Framework|
                    +-------------+-------------+
                                  |
        +------------+------------+------------+------------+
        |            |            |            |            |
   +----v----+  +----v----+  +-----v----+ +----v----+ +----v----+
   | 운영    |  |  보안   |  |  안정성  | | 성능    | | 비용    |
   | 우수성  |  |Security |  |Reliab.   | |효율성   | |최적화   |
   | (Ops)   |  |         |  |          | |Perf.    | |Cost     |
   +----+----+  +----+----+  +-----+----+ +----+----+ +----+----+
        |            |            |            |            |
   IaC, CI/CD   IAM, KMS,    Multi-AZ,   Auto Scal.,  RI, Spot,
   Observab.    WAF, Guard  Backups,    Caching,     RightSizing
   (3-pillar)   Duty        Pilot Light Serverless  Storage Tier
        |            |            |            |            |
        +------------+------------+------------+------------+
                                  |
                    +-------------v-------------+
                    | 지속가능성 (Sustainability)|
                    | Region Selection,         |
                    | Carbon-Aware Computing    |
                    +---------------------------+
```

### 2.2 핵심 구성 요소 및 동작

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 계층** | 워크로드 실행 | EC2/IaaS(전반적 제어), ECS/EKS/Container(컨테이너 오케스트레이션), Lambda/FaaS(이벤트 기반 15분 제한, 10GB 메모리), Fargate(서버리스 컨테이너) |
| **스토리지 계층** | 데이터 영속화 | S3(객체 스토어 11 9s 내구성), EBS(블록 스토어 IOPS 256K), EFS(병렬 NFS), Glacier(아카이브 검색 시간 분~시간), FSx(Lustre/ONTAP HPC용) |
| **네트워크 계층** | 연결성 및 격리 | VPC/16비트 CIDR, Subnet(/24 권장), Transit Gateway(다중 VPC 허브), PrivateLink(서비스별 ENI), CloudFront(280+ 엣지 로케이션) |
| **데이터 계층** | 관계형/NoSQL | RDS(엔진 자동 패치), Aurora(MySQL 5배, PostgreSQL 3배 성능), DynamoDB(단일 자리수 ms p99, 10MB 항목 제한), ElastiCache(Redis/Memcached) |
| **오케스트레이션** | IaC 및 정책 | Terraform(HCL 선언형, State Lock), CloudFormation(스택 단위), Pulumi(코드형), ArgoCD/Flux(GitOps 지속적 동기화) |
| **관측 가능성** | 3-Pillar | Prometheus/Grafana(메트릭), Loki/EFK(로그), Jaeger/Tempo(분산 트레이싱), CloudWatch/X-Ray 통합 |

### 2.3 핵심 알고리즘 및 의사결정 공식

**가용성(Availability) 계산식**:
$$Availability = \frac{MTBF}{MTBF + MTTR}$$
- 99.9%(Three 9s) = 연간 8.76시간 장애 허용
- 99.99%(Four 9s) = 연간 52.6분 (Multi-AZ 필수)
- 99.999%(Five 9s) = 연간 5.26분 (Active-Active 다중 리전)

**확장 전략 트레이드오프**:
$$Latency = \frac{Requests}{Throughput \times Instances} + Network\_Overhead$$
- 수직 확장(Scale-Up): 단일 노드 성능 ^, 비용 선형 증가, 단일 장애점(SPOF)
- 수평 확장(Scale-Out): 노드 수 ^, 이론적 무한 확장, 분산 트랜잭션 복잡도 ^

**비용 최적화 공식 (TCO 3년)**:
$$TCO = \sum_{i=1}^{3}(Compute + Storage + Network + License + Ops) - ReservedDiscount$$
- On-Demand 대비 Reserved Instance(RI) 1년 약 40%, 3년 약 60% 할인
- Savings Plans는 EC2/Fargate/Lambda 통합 약정으로 RI보다 유연

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "국제 우주 정거장(ISS)"과 같다. 각 모듈(컴퓨트, 스토리지, 네트워크)이 독립적으로 결합되어 있고, 한 모듈이 고장나도 다른 모듈이 임무를 지속하며, 우주에서 모듈을 교체하듯(Blue-Green 배포) 무중단으로 업그레이드할 수 있다.

---

## Ⅲ. 비교 및 연결

### 3.1 클라우드 서비스 모델 비교

| 구분 | On-Premise | IaaS | PaaS | SaaS | FaaS/Serverless |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **제어 범위** | 앱+데이터+런타임+미들웨어+OS+가상화+서버+스토리지+네트워크 | 앱+데이터+런타임+미들웨어+OS | 앱+데이터 | 사용만 | 함수 코드만 |
| **확장성** | 수동 (수주) | 분 단위 자동 | 자동 | 자동 (사용자 투명) | 밀리초 단위 (0->수천) |
| **책임 모델** | 고객 100% | 고객 70% / CSP 30% | 고객 50% / CSP 50% | 고객 10% / CSP 90% | 고객 20% / CSP 80% |
| **적합 워크로드** | 규제 산업, 레거시 | 일반 엔터프라이즈, Lift&Shift | API 백엔드, 데이터 분석 | 이메일, CRM, 협업 | 이벤트 처리, 배치, Webhook |
| **대표 기술** | VMware, Hyper-V | EC2, Compute Engine, Azure VM | Beanstalk, App Engine, Heroku | Office 365, Salesforce, Slack | Lambda, Cloud Functions, Azure Functions |
| **콜드 스타트** | N/A | 없음 | 없음 | 없음 | 100ms ~ 5초 (Provisioned Concurrency로 해결) |
| **가격 모델** | CAPEX (선불) | OPEX (시간/초) | OPEX (요청) | OPEX (사용자/월) | OPEX (호출+GB-초) |

### 3.2 배포 모델 비교

| 구분 | Public Cloud | Private Cloud | Hybrid Cloud | Multi-Cloud |
| :--- | :--- | :--- | :--- | :--- |
| **위치** | CSP 데이터센터 | 온프레미스/Hosted | Public + Private | 2개 이상 CSP |
| **제어력** | 낮음 | 높음 | 중간 | 매우 낮음 |
| **확장성** | 무제한 | 제한적 | 버스트 가능 | CSP별 독립 |
| **규제 준수** | 제한적 | 완전 | 데이터 분류 가능 | 복잡 |
| **벤더 락인** | 높음 | 없음 | 중간 | 회피 가능 |
| **네트워크** | 인터넷 | 전용선 | Direct Connect/ExpressRoute | Inter-Cloud Peering |
| **적합 사례** | 스타트업, 웹 서비스 | 금융, 공공, 의료 | 메인프레임 연계 | 재해복구, 가격 협상 |

### 3.3 컨테이너 오케스트레이션 도구 비교

| 구분 | Kubernetes (EKS) | ECS | Docker Swarm | Nomad |
| :--- | :--- | :--- | :--- | :--- |
| **CNCF 등급** | Graduated | AWS Native | (Deprecated) | Graduated |
| **학습 곡선** | 매우 높음 | 중간 | 낮음 | 중간 |
| **확장성** | 5,000 노드/클러스터 | 무제한 | 제한적 | 10,000+ 작업 |
| **서비스 메시** | Istio/Linkerd 기본 | App Mesh (AWS) | 미지원 | Consul 통합 |
| **사용 사례** | 표준 멀티 클라우드 | AWS 종속 단순 워크로드 | PoC/레거시 | HashiCorp 스택 |

### 3.4 마이그레이션 전략 (6R 프레임워크)

| 전략 | 설명 | 변경 범위 | 소요 시간 | 비용 | 예시 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Rehost (Lift & Shift)** | 그대로 이전 | 인프라만 | 1~3개월 | 낮음 | VMware -> EC2 |
| **Replatform** | 최소 최적화 (RDS 변환) | 약간 | 3~6개월 | 중간 | Oracle -> Aurora |
| **Repurchase** | SaaS 교체 | 전면 | 1~2개월 | 라이선스 | CRM -> Salesforce |
| **Refactor/Re-architect** | 클라우드 네이티브 재설계 | 전면 | 6~18개월 | 높음 | Monolith -> Microservices |
| **Retire** | 불필요 시스템 폐기 | 없음 | 1주 | 회수 | 중복 레거시 |
| **Retain** | 온프레미스 유지 | 없음 | 0 | 0 | 메인프레임 |

- **📢 섹션 요약 비유**: 클라우드 서비스 모델 선택은 "이사 전략"과 같다. IaaS는 빈 집을 통째로 빌리는 것(가구는 직접 배치), PaaS는 가구 포함된 집(입주만), SaaS는 호텔에 머무는 것(방만 사용), FaaS는 택배로 필요한 함수만 호출하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **RTO/RPO 정의 여부**: 재해복구 시 Recovery Time Objective(목표 복구 시간)와 Recovery Point Objective(목표 복구 시점)를 SLA 등급별로 명시했는가? (Tier 1: RTO 1시간/RPO 5분, Tier 4: RTO 24시간/RPO 24시간)
2. **다중 AZ/리전 전략**: 단일 AZ 배포는 허용했는가? Multi-AZ는 최소 2개, DR은 별도 리전(예: Seoul + Tokyo) 교차 배치했는가? Aurora Global Database의 경우 RPO < 1초 달성 가능성을 검토했는가?
3. **데이터 암호화 정책**: At-Rest(AES-256, KMS Customer Managed Key)와 In-Transit(TLS 1.3, mTLS) 양 측면에서 키 회전 주기(자동/수동, 90일 권장)와 BYOK(Bring Your Own Key) 적용 여부를 정의했는가?
4. **비용 거버넌스 수립**: 태그 기반 비용 분류(Tag: Environment, Team, CostCenter), Budget 알림(80%, 100%), Trusted Advisor/Compute Optimizer 기반 Right-Sizing 검토 주기(월 1회)를 운영화했는가?
5. **관측 가능성 3-Pillar 완비**: RED 메서드(Rate, Errors, Duration) 메트릭, 구조화 로그(JSON), 분산 트레이싱(OpenTelemetry) 기반 SLO(Service Level Objective, 예
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 700 / 800

<- **이전**: [699. 클라우드 아키텍처 핵심 토픽 699번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/699_cloud_architecture_core_topic_699_exam_summar/)
**다음**: [701. 클라우드 아키텍처 핵심 토픽 701번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/701_cloud_architecture_core_topic_701_exam_summar/) ->

---
