---
title: "678. 클라우드 아키텍처 핵심 토픽 678번 시험 요약 (Cloud Architecture Core Topic 678 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 온프레미스의 수직 확장(Scale-Up) 한계를 분산 컴퓨팅의 수평 확장(Scale-Out)과 추상화된 셀프서비스 인프라로 전환하며, IaC(Infrastructure as Code), 12-Factor App, Cloud-Native Computing Foundation(CNCF) 생태계를 기반으로 한 API-기반 선언적 프로비저닝 모델이다.
> 2. **가치**: AWS Well-Architected Framework 5대 축(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화) 달성을 통해 CAPEX 대비 OPEX 30~70% 절감, Auto Scaling을 통한 트래픽 변동 대응력 확보, 멀티 리전 배포로 가용성 99.99%(Four 9s) 이상 달성, Time-to-Market을 기존 대비 60% 단축한다.
> 3. **판단 포인트**: Public/Private/Hybrid/Multi-Cloud 중 배포 모델 선택, IaaS/PaaS/SaaS/FaaS/SaaS 간 책임 영역(Shared Responsibility Model) 경계 설정, Stateless/Microservices/Event-Driven 패턴 채택 여부, 그리고 Cloud Lock-in 위험과 이식성(Portability) 간 트레이드오프가 핵심 의사결정 변수다.

---

## Ⅰ. 개요 및 필요성

전통적 3-Tier 온프레미스 아키텍처는 CAPEX 중심의 정적 용량 계획(Static Capacity Planning), 수동 프로비저닝(Manual Provisioning), 단일 장애점(SPOF: Single Point of Failure), 수직 확장(Scaling-Up)의 물리적 한계로 인해 급증하는 디지털 트래픽과 비즈니스 민첩성(Agility) 요구를 충족하지 못한다. 2020년 이후 코로나19 팬데믹, 비대면 서비스 폭증, AI/ML 워크로드의 등장으로 기존 인프라 패러다임의 근본적 전환이 요구되었으며, 클라우드 아키텍처는 **탄력성(Elasticity)**, **무중단 배포(Zero-Downtime Deployment)**, **API 기반 셀프서비스**를 통해 이를 해결한다.

NIST SP 800-145 정의에 따르면 클라우드 컴퓨팅은 5대 필수 특성(온디맨드 셀프서비스, 광대역 네트워크 접근, 리소스 풀링, 빠른 탄력성, 측정 가능한 서비스)과 3대 서비스 모델(IaaS/PaaS/SaaS), 4대 배포 모델(Public/Private/Hybrid/Community)을 핵심 축으로 한다.

```text
+-----------------------------------------------------------------+
|           온프레미스 vs 클라우드 아키텍처 패러다임 비교              |
+-----------------------------------------------------------------+
|                                                                 |
|  [On-Premise]                      [Cloud-Native]               |
|  +--------------+                  +------------------+         |
|  |   Web/App    |                  |  CDN/Edge (CF)   |         |
|  |   Server     |                  +------------------+         |
|  +--------------+                  |  API Gateway     |         |
|  |   DB Server  |                  +------------------+         |
|  |  (RDBMS)     |                  |  Microservices   |         |
|  +--------------+                  |  (K8s Pods)      |         |
|  |  Storage     |                  +------------------+         |
|  |  (SAN/NAS)   |                  |  Managed DB      |         |
|  +--------------+                  |  (Aurora/Dynamo) |         |
|  |   Network    |                  +------------------+         |
|  |  (L2/L3)     |                  | Object Storage   |         |
|  +--------------+                  | (S3/GCS/Azure)   |         |
|        |                           +------------------+         |
|   정적 용량(Scale-Up)                동적 용량(Scale-Out)        |
|   수동 프로비저닝                    IaC(Terraform/CloudFormation)|
|   6개월~1년 구축                    1일~1주 배포                |
|   CAPEX 중심                        OPEX(Usage-based)            |
+-----------------------------------------------------------------+
```

클라우드의 본질적 가치는 **"Business Agility as a Service"**로, IT 자산을 비용 센터(Cost Center)에서 비즈니스 혁신의 인에이블러(Enabler)로 전환하는 데 있다. IDC 보고서에 따르면 2025년 전 세계 엔터프라이즈 워크로드의 85%가 클라우드 기반이 될 것으로 예측되며, Gartner는 2027년 클라우드 네이티브 플랫폼이 신규 디지털 이니셔티브의 95%를 지원할 것으로 전망한다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 호텔의 객실 운영과 같다. 손님(트래픽)이 몰리면 즉시 컨시어지(Auto Scaling)가 빈방(VM/Container)을 배정하고, 손님이 떠나면 자동으로 청소 후 다음 손님을 받는다. 자기 집(온프레미스)은 손님이 올 때마다 침대를 사야 하지만, 호텔은 사용한 만큼만 비용을 낸다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 4계층(4-Layer) 참조 모델로 분해된다. **물리/리소스 계층**, **가상화/컨테이너 계층**, **플랫폼/미들웨어 계층**, **애플리케이션/서비스 계층**이 있으며, 각 계층은 명확한 API 경계와 책임 분리(Separation of Concerns)를 갖는다.

```text
+--------------------------------------------------------------+
|                  Cloud Architecture 4-Layer Reference Model   |
+--------------------------------------------------------------+
|                                                              |
|  [L4] Application/Service Layer                              |
|  +--------------+ +--------------+ +--------------+         |
|  | SaaS (CRM)   | | FaaS(Lambda) | | Microservice |         |
|  |  Salesforce   | | Event-driven | | Spring Boot  |         |
|  +------+-------+ +------+-------+ +------+-------+         |
|         |                |                |                  |
|  [L3] Platform/Middleware Layer                              |
|  +--------------+ +--------------+ +--------------+         |
|  | PaaS         | | K8s/Service  | | API Gateway  |         |
|  | Beanstalk    | | Mesh (Istio) | | Kong/Apigee  |         |
|  +------+-------+ +------+-------+ +------+-------+         |
|         |                |                |                  |
|  [L2] Virtualization/Container Layer                         |
|  +--------------+ +--------------+ +--------------+         |
|  | Hypervisor   | | Docker       | | Serverless   |         |
|  | KVM/Xen/ESXi | | Container    | | Firecracker  |         |
|  +------+-------+ +------+-------+ +------+-------+         |
|         |                |                |                  |
|  [L1] Physical/Resource Layer                                |
|  +--------------+ +--------------+ +--------------+         |
|  | Region/AZ    | | Bare-Metal   | | Network      |         |
|  | Hyperscaler  | | Server       | | SDN/Overlay  |         |
|  +--------------+ +--------------+ +--------------+         |
|                                                              |
+--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트(Compute)** | 워크로드 실행 가상 자원 제공 | EC2(KVM 기반 Nitro System), GCE, Azure VM / 베어메탈(i3.metal), Graviton ARM(전력 효율 60% 향상), Spot Instance로 비용 70% 절감 |
| **스토리지(Storage)** | 데이터 영속성 및 접근 패턴별 분리 | Block(EBS gp3, io2 Block Express 256K IOPS), Object(S3 11 9s 내구성, GET 100K TPS), File(EFS, FSx for Lustre), Glacier 콜드 계층 |
| **네트워크(Networking)** | VPC/VNet/Subnet/SDN 오버레이 | VPC Peering, Transit Gateway, PrivateLink, VPC Endpoint, AWS Global Accelerator, Anycast EIP, BGP ECMP 라우팅 |
| **데이터베이스(DB)** | 관계형/NoSQL/분석 DB 매니지드 서비스 | RDS Multi-AZ(HA), Aurora 6-way 복제, DynamoDB Global Tables(멀티리전 액티브-액티브), Cosmos DB(다중 모델), BigQuery/Snowflake(데이터 웨어하우스) |
| **오케스트레이션** | 컨테이너 및 워크로드 자동 배치 | Kubernetes(EKS/GKE/AKS), EKS Fargate(서버리스 K8s 노드), Karpenter(지능형 노드 프로비저닝, 1분 내 스케일링), Helm/ArgoCD GitOps |
| **관제/보안** | Observability(메트릭/로그/트레이스) 통합 | CloudWatch, Prometheus/Grafana, OpenTelemetry, AWS X-Ray/Jaeger, CloudTrail(Config 감사), GuardDuty(위협 탐지), WAFv2 + Shield Advanced |
| **IaC/자동화** | 선언적 인프라 코딩 및 GitOps | Terraform(HCL 멀티 클라우드), CloudFormation/CDK(AWS 전용), Pulumi(다국어), Ansible(설정 관리), ArgoCD/FluxCD(GitOps) |
| **메시징/이벤트** | 비동기/이벤트 기반 결합 분리 | SQS(Standard/FIFO), SNS(Pub/Sub), Kinesis(스트림), EventBridge(Cross-account SaaS 이벤트), Kafka/MSK, RabbitMQ |

**클라우드 아키텍처의 5대 핵심 원리:**

1. **선언적 API(Declarative API)**: "어떻게(How)"가 아닌 "무엇을(What)" 정의. Terraform 코드 `desired_state`를 선언하면 Control Plane이 `actual_state`로 수렴(Reconciliation Loop).
2. **불변 인프라(Immutable Infrastructure)**: 패치/업데이트 대신 새 인스턴스 생성 후 트래픽 이동(Blue/Green), AMI/Packer로 베이킹, 컨테이너 이미지는 한 번 빌드 후 변경 불가.
3. **12-Factor App 원칙**: 코드베이스 1개, 의존성 명시적 선언, Config는 환경변수, Backing Services는 분리, 빌드/릴리스/실행 분리, Stateless 프로세스, 포트 바인딩, 동시성(Concurrency) 확장, Disposable Process, Dev/Prod 환경 일치, 로그를 이벤트 스트림으로, Admin 프로세스 일회성.
4. **탄력성(Elasticity)**: CloudWatch Metrics -> Alarm -> Auto Scaling Group. Scale-Out 트리거(예: CPU 70% 5분 지속), Scale-In 쿨다운(300초), Predictive Scaling(머신러닝 기반 사전 확장).
5. **장애를 전제로 한 설계(Design for Failure)**: Chaos Engineering(Netflix Chaos Monkey/Litmus), Circuit Breaker(Hystrix/Resilience4j), Bulkhead Pattern, Retry with Exponential Backoff+Jitter, Idempotency Key.

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 4계층은 햄버거 가게와 같다. 빵(L1 물리 자원)에 패티와 야채(L2 컨테이너/VM)를 얹고, 소스와 양상추(L3 플랫폼/미들웨어)를 더한 뒤, 손님이 원하는 토핑(L4 애플리케이션)을 올린다. 어떤 손님은 패티만, 어떤 손님은 채식 메뉴(FaaS)를 원해도 각 층이 독립적이라 빠르게 조합 가능하다.

---

## Ⅲ. 비교 및 연결

| 구분 | **IaaS** | **PaaS** | **SaaS** | **FaaS/Serverless** |
| :--- | :--- | :--- | :--- | :--- |
| **추상화 수준** | 가상 머신, 네트워크, 스토리지 직접 제어 | 런타임/미들웨어/DB 자동 관리 | 완성된 애플리케이션 제공 | 함수 단위 실행, 인프라 완전 은닉 |
| **책임 영역(고객)** | OS, 미들웨어, 런타임, 데이터, 앱 | 앱과 데이터만 관리 | 사용자 데이터/접근 권한만 | 함수 코드와 트리거 조건만 |
| **확장성** | 수동/반자동(Auto Scaling Group) | 자동(매니지드 서비스 기본) | 벤더 종속 자동 확장 | 자동(True Scale-to-Zero, ms 단위 콜드 스타트) |
| **대표 서비스** | EC2, GCE, Azure VM, Oracle Cloud | Elastic Beanstalk, App Engine, Heroku, Cloud Run | Salesforce, Workday, Microsoft 365, Slack | Lambda, Cloud Functions, Azure Functions |
| **적합 워크로드** | 레거시 마이그레이션, 커스텀 네트워크, 특수 하드웨어(GPU) | 웹앱, API, 표준 프레임워크 기반 개발 | 표준 비즈니스 프로세스, 협업 | 이벤트 처리, 스케줄러, IoT, Webhook, ETL |
| **비용 모델** | 인스턴스 시간 단위 과금 | 인스턴스 + 매니지드 서비스료 | 사용자 라이선스(Per-User/Per-Month) | 호출 횟수 + GB-초 과금(미사용 시 0원) |
| **제어성/유연성** | 매우 높음(OS 커널 접근) | 중간(런타임은 벤더 정책) | 낮음(기능 커스터마이징 한계) | 매우 낮음(실행 환경 통제 불가) |
| **콜드 스타트** | 없음(상시 구동) | 수 초(컨테이너 기동) | 없음 | 100ms~수 초(Lambda 기본 100~500ms, SnapStart로 단축) |
| **장기 실행** | 무제한 | 무제한(환경에 따라 다름) | 무제한 | 최대 15분(Lambda 한도) |
| **벤더 종속성** | 중간(AMI/이미지 이식 가능) | 높음(벤더 API 종속) | 매우 높음 | 매우 높음(벤더별 트리거/런타임 종속) |

### 통합 연결 관계

클라우드 아키텍처는 단독 기술이 아닌 **생태계(Ecosystem)**로 작동한다.

- **CI/CD 통합**: GitHub Actions -> ECR Push -> EKS Helm Chart 배포 -> ArgoCD Sync
- **Observability 3요소**: OpenTelemetry SDK -> OTLP -> Jaeger/Tempo(트레이스) + Prometheus(메트릭) + Loki(로그) -> Grafana 대시보드
- **보안 통합**: IAM(인증/인가) + KMS(암호화) + WAF(웹 방화벽) + GuardDuty(위협 인텔리전스) + Security Hub(통합 대시보드)
- **AI/ML 통합**: SageMaker + Bedrock(RAG) + Step Functions(워크플로우 오케스트레이션) + S3(피처 스토어)

- **📢 섹션 요약 비유**: IaaS/PaaS/SaaS/FaaS는 자동차의 변속기 모드와 같다. P(파킹)=IaaS(직접 운전), D(드라이브)=PaaS(반자동), N(중립)=SaaS(완전 위탁), S(스포츠)=FaaS(필요할 때만 순간 가속). 운전자의 숙련도와路况(워크로드)에 따라 적절히 변속해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **워크로드 특성 분석 및 클라우드 적합성 평가**: 6R 마이그레이션 프레임워크(Rehost/Lift&Shift, Replatform, Repurchase, Refactor
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 678 / 800

<- **이전**: [677. 클라우드 아키텍처 핵심 토픽 677번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/677_cloud_architecture_core_topic_677_exam_summar/)
**다음**: [679. 클라우드 아키텍처 핵심 토픽 679번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/679_cloud_architecture_core_topic_679_exam_summar/) ->

---
