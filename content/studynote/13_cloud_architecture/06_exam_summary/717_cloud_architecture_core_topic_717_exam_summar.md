---
title: "717. 클라우드 아키텍처 핵심 토픽 717번 시험 요약 (Cloud Architecture Core Topic 717 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS의 서비스 모델과 Public/Private/Hybrid/Multi-Cloud 배포 모델을 기반으로, 12-Factor App 원칙, 마이크로서비스, 컨테이너 오케스트레이션(Kubernetes), 서비스 메시(Istio/Linkerd), 서버리스(Lambda/Cloud Functions), IaC(Terraform/CloudFormation) 등을 유기적으로 결합하여 탄력성·가용성·확장성·비용 최적화를 동시에 달성하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: AWS Well-Architected Framework 5대 축(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화)과 Azure/AWS/GCP의 managed 서비스 활용으로, CapEx를 OpEx로 전환하고(평균 30~40% TCO 절감), Time-to-Market을 60~80% 단축하며, Auto Scaling을 통한 트래픽 변동 대응력(Gaussian workload에서 최대 90% 비용 절감)을 확보한다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) 회피를 위한 Multi-Cloud/Abstraction Layer 설계, 마이크로서비스의 분할 단위(Domain-Driven Design의 Bounded Context), 서버리스의 콜드 스타트 지연, 컨테이너 오버헤드 vs VM, 데이터 일관성(Strong vs Eventual Consistency), FinOps 기반 비용 거버넌스, Zero Trust 보안 모델 적용 여부가 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX) 가속화와 4차 산업혁명 시대의 도래로, 전통적 온프레미스 데이터센터는 급증하는 트래픽 변동성, 짧아지는 비즈니스 요구사항 반영 주기, 글로벌 서비스 확장에 따른 한계에 직면했다. 2020년 코로나19 팬데믹 이후 비대면 서비스 폭증으로 클라우드 전환은 선택이 아닌 필수(Necessity)가 되었고, Gartner(2023) 보고서에 따르면 전 세계 엔터프라이즈 IT 지출의 65% 이상이 클라우드로 전환되었다. 한국 또한 「클라우드 컴퓨팅 발전 및 이용자 보호에 관한 법률」(2023. 9. 시행)로 클라우드 컴퓨팅의 법적·제도적 기반이 마련되어 공공·금융·의료 분야의 도입이 가속화되고 있다.

기존 모놀리식 아키텍처는 **배포 주기 수개월**, **수직 확장(Scale-Up) 한계**, **단일 장애점(SPOF)**, **하드웨어 CapEx 과다 투자**, **유휴 자원 70% 이상 발생** 등의 구조적 문제를 안고 있었다. 반면 클라우드 네이티브 아키텍처는 **마이크로서비스 분할**, **컨테이너 기반 패키징**, **동적 오케스트레이션**, **선언적 IaC(Infrastructure as Code)**, **CI/CD 자동화**, **불변 인프라(Immutable Infrastructure)**를 통해 **배포 주기 수분 단위**, **수평 확장(Scale-Out) 무제한**, **자가 치유(Self-healing)**, **사용량 기반 과금(Pay-per-Use)**을 실현한다.

```text
[기존 모놀리식 vs 클라우드 네이티브 아키텍처 진화 흐름]

   +---------------------+                     +-----------------------------+
   |  Monolithic (Legacy) |  ---- DX 전환 --->  |   Cloud-Native (Modern)     |
   |                     |                     |                             |
   |  +--------------+   |                     |  +------+ +------+ +------+ |
   |  |   단일 WAR   |   |                     |  | Auth | |Order | |Pay   | |
   |  |  (Spring)    |   |                     |  | MS   | | MS   | | MS   | |
   |  |  + RDBMS     |   |                     |  +------+ +------+ +------+ |
   |  +--------------+   |                     |      ↕   Istio Mesh        |
   |   단일 WAS × N대   |                     |  +----------------------+    |
   |   수직 확장 한계   |                     |  |  K8s Cluster (EKS)   |    |
   |   배포 주기 3~6M   |                     |  +----------------------+    |
   |   장애 전파 위험   |                     |  + Lambda(Serverless)        |
   +---------------------+                     |  + Aurora/ DynamoDB          |
                                                |  + S3 / CloudFront           |
                                                |  + GitOps(ArgoCD)            |
                                                +-----------------------------+

[필요성 3대 동기]
  ① Speed    : 비즈니스 변화 속도 대응 (Release Train: 3개월 -> 1일)
  ② Scale    : 트래픽 변동 탄력적 대응 (Black Friday 100x 트래픽 흡수)
  ③ Spend    : CapEx -> OpEx, 유휴 자원 제거 (FinOps)
```

- **📢 섹션 요약 비유**: 기존 모놀리식 시스템이 "한 채의 아파트에 가족·회사·학교를 모두 수용하는 형태"라면, 클라우드 네이티브는 "용도별(거주/업무/교육)로 분리된 스마트 타운에 공유 인프라(도로·전기·수도)를 MSA로 조달하는 형태"와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **NIST SP 800-145**에서 정의한 4대 배포 모델(Public/Private/Hybrid/Community)과 3대 서비스 모델(IaaS/PaaS/SaaS)을 기반으로, 12-Factor App(Heroku, 2012) 원칙을 마이크로서비스로 구현하고, 이를 Kubernetes 위에서 컨테이너로 운영하며, IaC와 GitOps로 자동화하는 **Cloud-Native Computing Foundation(CNCF) Landscape**(현재 1,000+ 프로젝트)의 생태계로 구성된다.

```text
[클라우드 아키텍처 4계층 참조 모델 (CNCF Trail Map 기준)]

   +----------------------------------------------------------------------+
   | Layer 4: Observability & Analysis                                    |
   |  +----------+  +----------+  +----------+  +---------------------+  |
   |  |Prometheus|  | Grafana  |  |Loki/EFK  |  |Jaeger / OpenTelemetry| |
   |  +----------+  +----------+  +----------+  +---------------------+  |
   +----------------------------------------------------------------------+
   | Layer 3: App Definition & Development (PaaS Layer)                  |
   |  +----------+  +----------+  +----------+  +---------------------+  |
   |  |Helm/Kustomize |  |Buildpacks| |Backstage| |Crossplane  (IaC)    |  |
   |  +----------+  +----------+  +----------+  +---------------------+  |
   +----------------------------------------------------------------------+
   | Layer 2: Orchestration & Management (Container Platform)            |
   |  +--------------------------------------------------------------+    |
   |  |   Kubernetes (EKS / AKS / GKE / Self-managed on Bare-Metal) |    |
   |  |   - Control Plane: API Server / etcd / Scheduler / CM/Sched  |    |
   |  |   - Worker Node: kubelet / kube-proxy / Container Runtime    |    |
   |  +--------------------------------------------------------------+    |
   |  + Service Mesh: Istio(Envoy Sidecar) / Linkerd / Consul              |
   |  + Ingress: NGINX / Contour / Gateway API                            |
   +----------------------------------------------------------------------+
   | Layer 1: Provisioning (IaaS Layer)                                   |
   |  +--------------+  +--------------+  +--------------+  +---------+  |
   |  | AWS / Azure  |  | Terraform /  |  |Packer / AMI  |  |CAPI /   |  |
   |  | / GCP / NCP  |  | Pulumi / CDK |  |              |  |Crossplane|  |
   |  +--------------+  +--------------+  +--------------+  +---------+  |
   +----------------------------------------------------------------------+

   -------------------------------------------------------------
   [Cloud-Native App 구조 (12-Factor + Microservices)]
   -------------------------------------------------------------

   +--------+  HTTPS/gRPC  +------------------+
   |  User  | ------------> | API Gateway      | (Kong, Apigee, AWS API GW)
   |(Mobile/|              |  + WAF (Layer 7) |
   | Web)   |              +---------+--------+
   +--------+                        | JWT 검증/라우팅
                                    v
            +---------------------------------------------+
            |       Service Mesh (Istio Sidecar)          |
            |  +---------+ +---------+ +---------+        |
            |  |Auth Svc | |Order Svc| |Pay  Svc |  ...   |
            |  |(Envoy)  | |(Envoy)  | |(Envoy)  |        |
            |  +----+----+ +----+----+ +----+----+        |
            +-------+----------+----------+---------------+
                    |          |          |
                    v          v          v
            +---------+ +---------+ +---------+
            |PostgreSQL| |DynamoDB | |Redis    | (Polyglot Persistence)
            |  RDS     | |         | |Cluster  |
            +---------+ +---------+ +---------+

   --- 비동기 이벤트 흐름 ------------------------------

   Order Svc --[Kafka/EventBridge]---> Inventory Svc
                                    +-> Notification Svc (Lambda)
                                    +-> Analytics Svc (Flink/Spark)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway** | 외부 트래픽 진입점, 라우팅·인증·속도 제한 | Kong, AWS API Gateway, Apigee — OAuth2/JWT 검증, Rate Limiting(예: 1000 RPS/Client), Circuit Breaker 패턴 |
| **Service Mesh (Istio)** | 서비스 간 통신·트래픽 관리·보안 | Envoy Sidecar Proxy(2개 컨테이너: App + Envoy in 1 Pod)로 mTLS 자동 적용, Canary 배포(Traffic Split 90:10), Retry/Timeout 정책 |
| **Kubernetes (CNI/Pod)** | 컨테이너 오케스트레이션, 선언적 상태 관리 | Control Plane(API Server ↔ etcd Raft 합의) ↔ Worker Node(kubelet이 PodSpec 감시), HPA(CPU/Mem/커스텀 메트릭) -> min/max Replica 자동 조정, PDB로 자가 치유 |
| **Managed DB / Polyglot** | 도메인별 최적 데이터 저장소 | RDBMS(Aurora MySQL/PostgreSQL, Multi-AZ + Read Replica), NoSQL(DynamoDB Global Table, Cassandra), Cache(Redis Cluster, ElastiCache) — CAP 정리에 따라 일관성/가용성 trade-off |
| **IaC (Terraform/CloudFormation)** | 인프라 프로비저닝 자동화, 불변 인프라 구현 | HCL/JSON 선언적 코드 -> Plan/Apply 2단계, State 파일(S3+DynamoDB Lock), Module 재사용, Drift Detection |
| **Observability (3 Pillars)** | 통합 모니터링·로그·분산 추적 | Metrics(Prometheus pull + PromQL), Logs(Loki/ELK, 구조화 JSON), Traces(OpenTelemetry SDK -> Jaeger/Tempo) — RED 메서드(Rate/Errors/Duration) + USE(Utilization/Saturation/Errors) |
| **CI/CD + GitOps** | 지속적 통합·배포 자동화 | Jenkins/ArgoCD/Flux — PR 트리거 -> Build -> Container Registry(ECR) -> Helm Chart -> ArgoCD Sync(실제 상태 vs Git 선언 상태 일치화), Progressive Delivery(Argo Rollouts) |
| **Serverless (FaaS)** | 이벤트 기반 stateless 코드 실행 | AWS Lambda / Azure Functions / GCP Cloud Functions — 콜드 스타트(예: Java 5s, Node.js 200ms) 이슈 -> Provisioned Concurrency로 해결, 동시성 1000/함수, 15분 타임아웃 |

**12-Factor App 핵심 원칙 (Pivotal/Heroku)**:
① Codebase(단일 코드베이스, 다중 배포) ② Dependencies(명시적 선언, `requirements.txt`/`pom.xml`) ③ Config(환경변수, 코드와 분리) ④ Backing Services(연결 자원 추상화) ⑤ Build/Release/Run(3단계 엄격 분리) ⑥ Processes(Stateless, Shared Nothing) ⑦ Port Binding(자체 포트 노출) ⑧ Concurrency(프로세스 모델로 수평 확장) ⑨ Disposability(빠른 시작/우아한 종료, SIGTERM 핸들링) ⑩ Dev/Prod Parity(환경 차이 최소화) ⑪ Logs(이벤트 스트림, stdout/stderr) ⑫ Admin Processes(일회성 관리 작업).

- **📢 섹션 요약 비유**: 12-Factor App은 "이사 가기 좋은 집 꾸리기 12계명"이다. 가구는 박스(`Container`)에 담고, 설치 방법(`IaC`)은 매뉴얼로 남기며, 인테리어(`Config`)는 입주 시 조달하고, 가구 배치(`Topology`)는 도면(`Manifest`)대로 — 그러면 어떤 집(환경)에서도 즉시 입주 가능하다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처는 모놀리식, SOA, 마이크로서비스, 서버리스 등 다양한 아키텍처 스타일과 IaaS/PaaS/SaaS/FaaS 등 서비스 모델, 그리고 Public/Hybrid/Multi-Cloud 등 배포 모델 사이에서 trade-off가 발생한다.

| 구분 | **Monolithic** | **Microservices (MSA)** | **Serverless (FaaS)** | **Managed Kubernetes** |
| :--- | :--- | :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/EAR (수 GB) | 서비스별 컨테이너 (수백 MB) | 함수 단위 (수십~수백 KB) | Pod 단위 (수백 MB) |
| **확장 방식** | Scale-Up (수직) | Scale-Out (수평, 서비스별) | 자동 (요청 기반, 0->N) | HPA/VPA/Cluster Autoscaler |
| **장애 격리** | 전체 영향 (SPOF) | 서비스 단위 격리, Circuit Breaker | 함수 단위 격리 | Pod 단위 격리, PDB |
| **트랜잭션** | ACID, 분산 트랜잭션 | Saga Pattern (Choreography/Orchestration) | Step Functions로 보상 트랜잭션 | Saga, Outbox Pattern |
| **운영 복잡도** | 낮음 (단일 시스템) | 높음 (다수 서비스 + Mesh) | 중간 (벤더 관리형) | 높음 (K8s 전문성 필요) |
| **적합 workload** | 소규모 CRUD, 레거시 | 대규모·고변동·팀별 독립 배포 | 이벤트 드리븐, 간헐적 workload | 장기 실행·상태 보유·이식성 중시 |
| **콜드 스타트** |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 717 / 800

<- **이전**: [716. 클라우드 아키텍처 핵심 토픽 716번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/716_cloud_architecture_core_topic_716_exam_summar/)
**다음**: [718. 클라우드 아키텍처 핵심 토픽 718번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/718_cloud_architecture_core_topic_718_exam_summar/) ->

---
