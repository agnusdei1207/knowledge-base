---
title: "Cloud Architecture Core Topic 566 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS·PaaS·SaaS·FaaS의 **책임 공유 모델(Shared Responsibility Model)**과 **12-Factor App 원칙**, **Well-Architected Framework**(운영 우수성·보안·신뢰성·성능 효율·비용 최적화·지속 가능성 6개 기둥)를 기반으로, 마이크로서비스·컨테이너(K8s)·서버리스·이벤트 기반 구조를 조합하여 **탄력성(Elasticity)·가용성(HA)·확장성(Scalability)**을 달성하는 시스템 설계 체계이다.
> 2. **가치**: CAPEX에서 OPEX로의 전환, **Auto Scaling**을 통한 Peak 시 60~80% 인프라 비용 절감, **Multi-AZ/Region** 구성을 통한 99.99%(52.6분/년) SLA 확보, **Pay-per-use** 모델로 TCO(Time-to-Market) 기준 약 3배 이상 개발 생산성 향상.
> 3. **판단 포인트**: **Stateless/Stateful** 워크로드 분리, **CAP 정리**(Consistency/Availability/Partition tolerance) 트레이드오프, **동기/비동기** 통신 비율, **Multi-Cloud vs Hybrid Cloud** 전략, **Egress 비용**(AWS 기준 $0.09/GB)과 같은 숨은 비용 구조, **Cold Start latency** 등 런타임 특성의 이해가 핵심.

---

## Ⅰ. 개요 및 필요성

전통적인 On-Premise(온프레미스) monolithic 아키텍처는 초기 투자비(CAPEX)가 막대하고, **수직적 확장(Scale-Up)**의 물리적 한계, 프로비저닝에 수 주 소요, 트래픽 급증 시 장애 전파, 그리고 DR(Disaster Recovery) 사이트의 이중 투자라는 고질적인 문제를 안고 있다. 2006년 AWS EC2 출시 이후 클라우드 컴퓨팅은 **가상화(Hypervisor: Xen->KVM)-> 컨테이너(Docker, 2013)-> 오케스트레이션(K8s, 2015)-> 서버리스(Lambda, 2014)**로 진화하며, 인프라 추상화 수준을 계속 높여왔다.

클라우드 아키텍처는 단순한 "서버 대여"가 아니라, **셀프 서비스 프로비저닝, API 기반 인프라(IaC: Terraform/CloudFormation), 선언적 정책(Policy as Code: OPA), 분산 시스템 패턴**을 포괄하는 광범위한 설계 철학이다. NIST SP 800-145는 클라우드를 **5대 필수 특성**(On-demand self-service, Broad network access, Resource pooling, Rapid elasticity, Measured service)과 **3대 서비스 모델**(IaaS/PaaS/SaaS), **4대 배치 모델**(Public/Private/Hybrid/Community)로 정의한다.

```text
[클라우드 아키텍처 진화 흐름]

 2006        2009        2013        2014        2015        2019        2023~
  |           |           |           |           |           |           |
  v           v           v           v           v           v           v
+------+  +------+   +------+   +------+   +------+   +------+   +------+
| IaaS |-> |PaaS  | -> |CaaS  | -> |FaaS  | -> |CaaS  | -> |Multi | -> |AI/   |
| EC2  |  |BeanSt|   |Docker|   |Lambda|   |K8s   |   |Cloud |   |Edge  |
|      |  |alk   |   |      |   |      |   |GA    |   |Mesh  |   |      |
+------+  +------+   +------+   +------+   +------+   +------+   +------+
   |           |           |           |           |           |           |
   + 추상화 수준(Abstraction) 증가 ->--------------------------------------+
   + 책임 공유 영역(AWS 관리) 감소 ->-- 클라이언트 책임 증가
```

**왜 필요한가?**
- **비용 구조의 혁신**: AWS TCO Calculator 기준 3년 운영 시 On-Prem 대비 약 40~60% 절감 (워크로드 유형에 따라 차이)
- **글로벌 확장성**: 한 버튼으로 리전 확장, CDN(CloudFront/Cloudflare) 연동으로 전 세계 수십 ms 응답시간 확보
- **탄력성**: 트래픽 예측 불가한 워크로드(블랙프라이데이, 선거, 신년 트래픽)에 대해 **Predictive Scaling(K8s HPA + KEDA)**으로 자동 대응
- **MTTR 단축**: IaC + GitOps(ArgoCD/Flux) + ChatOps로 장애 복구 시간 평균 70% 단축

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"전기 공급망과 같다"** — 발전소(클라우드 제공자)가 모든 발전·송전을 책임지고, 우리는 콘센트(API)에 꽂아 전기(컴퓨팅)를 사용하되, 우리 집의 배선·차단기(네트워크·보안)는 직접 관리하는 **책임의 분리(separation of concerns)** 모델이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **"느슨하게 결합되고(loosely coupled), 상태가 없으며(stateless), 이벤트로 통신하는(EDA) 분산 시스템"**을 어떻게 구성하느냐에 있다. 이를 위해 **12-Factor App** 원칙(2011, Heroku 창시자 Adam Wiggins)이 사실상 표준으로 자리 잡았으며, **AWS Well-Architected**, **Azure WAF**, **Google Cloud Architecture Framework**가 각 CSP 별 구현 가이드를 제공한다.

```text
[클라우드 네이티브 참조 아키텍처 - 4계층 + 횡단 관심사]

  +-------------------------------------------------------------+
  |              Edge / Global Layer (CloudFront, WAF, Route53)  |
  |   +------------------------------------------------------+  |
  |   |  TLS 1.3 Termination, DDoS Shield, Geo-Routing       |  |
  |   +------------------------------------------------------+  |
  +---------------------------+---------------------------------+
                              |
  +---------------------------v---------------------------------+
  |          API Gateway / Service Mesh (Istio, App Mesh)        |
  |   mTLS, Circuit Breaker, Retry/Timeout, Rate Limiting        |
  |   +---------+  +---------+  +---------+  +---------+      |
  |   | User Svc|  |Order Svc|  |Pay Svc  |  |Notif Svc|      |
  |   | (K8s)   |  |(Lambda) |  |(EKS)    |  |(Fargate)|      |
  |   +---------+  +---------+  +---------+  +---------+      |
  +---------------------------+---------------------------------+
                              |
  +---------------------------v---------------------------------+
  |   Data Plane  (Polyglot Persistence)                         |
  |   +------------+  +------------+  +----------+  +--------+ |
  |   |RDS/Aurora  |  |DynamoDB    |  |S3/Blob   |  |Redis   | |
  |   |(RDBMS OLTP)|  |(NoSQL KV)  |  |(Object)  |  |(Cache) | |
  |   +------------+  +------------+  +----------+  +--------+ |
  +---------------------------+---------------------------------+
                              |
  +---------------------------v---------------------------------+
  |   Cross-Cutting: Observability(CW/X-Ray/Prometheus/Grafana)  |
  |   Security(IAM/KMS/ Secrets Manager/Vault), IaC(Terraform)  |
  |   CI/CD(CodePipeline/GitHub Actions/ArgoCD)                  |
  +--------------------------------------------------------------+
```

### 12-Factor App 핵심 요약

| # | 요인 | 클라우드 구현 |
| :--- | :--- | :--- |
| 1 | **Codebase** | 단일 Git Repo, 다중 배포(Dev/Stg/Prod) |
| 2 | **Dependencies** | `requirements.txt`, `package.json` 명시적 선언, 컨테이너 이미지 |
| 3 | **Config** | 환경 변수(12-factor), AWS SSM Parameter Store, Vault |
| 4 | **Backing Services** | DB·Cache·Queue를 **Attached Resource**로 취급, URL로 추상화 |
| 5 | **Build, Release, Run** | 3단계 엄격 분리, Immutable Artifact |
| 6 | **Processes** | Stateless 프로세스, 세션은 Redis/ElastiCache |
| 7 | **Port Binding** | 자체 HTTP 서버(Tomcat 내장, gunicorn) |
| 8 | **Concurrency** | 프로세스 모델로 수평 확장 |
| 9 | **Disposability** | 빠른 Startup(컨테이너 < 5s), Graceful Shutdown(SIGTERM 핸들링) |
| 10 | **Dev/Prod Parity** | Docker로 환경 일치, K8s Namespace 분리 |
| 11 | **Logs** | stdout/stderr 스트림, Fluent Bit -> OpenSearch |
| 12 | **Admin Processes** | One-off 프로세스는 동일 환경에서 실행 |

### 4대 서비스 모델 비교

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IaaS** (Infrastructure-as-a-Service) | 가상화된 컴퓨팅·스토리지·네트워크를 OS 단위까지 제공 | AWS EC2(bare metal: `*.metal` 인스턴스, Nitro System), Azure VM, GCP Compute Engine. 사용자 책임: Guest OS·Middleware·Runtime·Data·Application. |
| **PaaS** (Platform-as-a-Service) | 애플리케이션 배포·확장에 필요한 런타임·미들웨어·OS·인프라 통합 관리 | AWS Elastic Beanstalk, Azure App Service, GCP App Engine, Heroku, Cloud Foundry. 코드만 Push하면 자동 Provisioning·Auto Scaling·Health Check. |
| **SaaS** (Software-as-a-Service) | 완성된 애플리케이션을 멀티 테넌트 형태로 제공 | Salesforce, Microsoft 365, Slack, Notion, GitHub, Snowflake. 사용자는 설정과 데이터만 관리. |
| **FaaS/Serverless** (Function-as-a-Service) | 이벤트 기반 단발성 함수 단위로 실행, 0~N Auto Scaling | AWS Lambda(15분 타임아웃, 10GB 메모리, 6 vCPU), Azure Functions, GCP Cloud Functions, Cloudflare Workers(Global Edge). **Cold Start**: Java 1~3s, Node/Python 100~300ms, Go < 50ms, SnapStart(Lambda) 활용. |

### 클라우드 아키텍처의 4가지 핵심 특성 (NIST)

1. **On-demand Self-Service**: API 호출 시 자동 Provisioning (예: `aws ec2 run-instances` -> 30~90초 내 인스턴스 가용)
2. **Broad Network Access**: HTTP/HTTPS, gRPC, MQTT 등 표준 프로토콜로 다양한 디바이스 접근
3. **Resource Pooling**: Multi-Tenant 모델, **Placement Group**(cluster/spread/partition)으로 물리적 위치 추상화
4. **Rapid Elasticity**: HPA(Horizontal Pod Autoscaler, 15초 주기) + Cluster Autoscaler(1분 주기) + **KEDA**(외부 이벤트 기반: Kafka lag, SQS depth)
5. **Measured Service**: **CloudWatch Detailed Monitoring**(1분), **Cost Explorer**, **Trusted Advisor**로 사용량 정량 측정

- **📢 섹션 요약 비유**: 12-Factor App은 **"이사 가기 좋은 가짐"**이다 — 모든 짐(코드, 의존성, 설정)이 **표준 박스(컨테이너)**에 **라벨(env, log)** 붙어 있어 어느 집(환경)으로 이사 가도 **30분 만에 입주**할 수 있다.

---

## Ⅲ. 비교 및 연결

### 클라우드 배치 모델(Deployment Model) 비교

| 구분 | Public Cloud | Private Cloud | Hybrid Cloud | Multi-Cloud |
| :--- | :--- | :--- | :--- | :--- |
| **소유권** | AWS/Azure/GCP 등 CSP | 자체 DC 또는 Hosted Private (Outsour) | On-Prem + Public 혼용 | 2개 이상의 Public CSP |
| **확장성** | 무제한(리전 한도 내) | 자체 용량 한계 | Burst 시 Public 활용 | CSP별 종속 회피 |
| **보안·컴플라이언스** | FedRAMP, ISO 27001 인증 필요 시 Region 제한 | 완전한 통제, 금융·공공 요건 충족 용이 | 데이터 주권(데이터 주체별 분리) | CSP Lock-in 회피, 견고한 DR |
| **네트워크** | Internet or Direct Connect/ExpressRoute | 전용선/내부망 | **Interconnect**(DX, VPN IPSec), **Transit Gateway** | **Cloud Router**, **Megaport**, **Equinix** |
| **Egress 비용** | 높음(AWS $0.09/GB) | 없음 | On-Prem->Cloud 무료, 반대는 과금 | CSP 간 전송 비용 발생 |
| **적합 사례** | 웹 서비스, SaaS, AI/ML | 금융 코어뱅킹, 공공 G-Cloud, Legacy | 단계적 클라우드 전환, 데이터+연산 분리 | 벤더 종속 회피, Best-of-Breed (DB=Spanner, AI=Azure OpenAI) |
| **대표 기술** | AWS, Azure, GCP, Naver Cloud, KT Cloud | VMware on AWS, Azure Stack, OpenStack | AWS Outposts, Azure Arc, GCP Anthos | Terraform + Crossplane, Cross-cloud IAM Federation |

### Monolith vs SOA vs Microservices

| 구분 | Monolith | SOA | Microservices | Serverless |
| :--- | :--- | :--- | :--- | :--- |
| **배포 단위** | 1개 WAR/EAR | 서비스 버스(ESB) 중심 | 컨테이너/이미지 | 함수(Handler) |
| **결합도** | 강한 결합(tight) | 느슨한(ESB 의존) | 느슨한 + 독립 DB | 이벤트 + Stateless |
| **확장 단위** | 애플리케이션 전체 | 서비스 단위 | 서비스 단위 | 함수 단위(자동) |
| **기술 스택** | 단일 | 다양(ESB 제약) | Polyglot(언어·DB 자유) | Runtime 제약(Lambda: Node, Py, Go, Java, Ruby, .NET) |
| **장애 영향** | 전체 장애 | ESB 병목 시 전체 | 서비스 단위 격리 | 함수 단위 격리, DLQ |
| **운영 복잡도** | 낮음 | 중(ESB 관리) | 높음(Observability 필수) | 중간(벤더 종속) |
| **적합 규모** | 1팀, 1~
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 566 / 800

<- **이전**: [565. 클라우드 아키텍처 핵심 토픽 565번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/565_cloud_architecture_core_topic_565_exam_summar/)
**다음**: [567. 클라우드 아키텍처 핵심 토픽 567번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/567_cloud_architecture_core_topic_567_exam_summar/) ->

---
