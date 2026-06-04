---
title: "780. 클라우드 아키텍처 핵심 토픽 780번 시험 요약 (Cloud Architecture Core Topic 780 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST의 5-4-3 모델(5대 특성, 4종 배포 모델, 3종 서비스 모델)을 근간으로, **IaaS(컴퓨팅·스토리지·네트워크 가상화) -> PaaS(쿠버네티스·서비스 메시) -> SaaS(멀티테넌시·API 게이트웨이)** 계층에서 컨테이너 오케스트레이션, IaC(Terraform/CloudFormation), GitOps, eBPF 기반 옵저버빌리티가 결합된 분산 시스템 설계 패러다임이다.
> 2. **가치**: CAPEX->OPEX 전환으로 초기 인프라 투자비 70% 절감, Auto Scaling Group을 통한 트래픽 피크 대응(평균 3~10배 탄력성), 글로벌 멀티리전 배포로 RTO < 1분·RPO 0에 근접하는 DR 확보, FinOps 도입 시 클라우드 비용 20~40% 최적화 효과가 검증된다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs 멀티클라우드(네트워크 지연·데이터 egress 비용), 동기 복제(Strong Consistency, 지연^) vs 비동기 복제(Eventual Consistency, 가용성^), Stateless Microservice(확장성^) vs Stateful Service(데이터 정합성^), Spot Instance 활용(비용v 60~90%) vs On-Demand(안정성^)의 트레이드오프를 트래픽 패턴·SLA·컴플라이언스 기반으로 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

클라우드 아키텍처는 2006년 AWS S3·EC2 출시 이후, 가상화(KVM/Xen) -> 컨테이너(Docker) -> 오케스트레이션(Kubernetes) -> 서버리스(Knative/Lambda) -> 엣지(Wasm/K3s)로 진화해 왔다. 4차 산업혁명·디지털 트랜스포메이션 요구로 인해, **IDC의 Worldwide Cloud Spending 보고서(2024)에 따르면 전 세계 퍼블릭 클라우드 지출이 1조 USD를 돌파**하며 엔터프라이즈 IT의 표준 아키텍처로 자리잡았다.

기존 On-Premise 환경은 CAPEX 위주의 수직적 확장으로, 트래픽 피크 예측 실패 시 과잉투자 또는 장애가 빈번했다. 클라우드 아키텍처는 이를 **"탄력성(Elasticity) + 종량과금(Pay-as-you-go) + 셀프서비스 프로비저닝 + 글로벌 확장성"** 4대 축으로 해결하며, API 기반 제어 평면(Control Plane)과 데이터 평면(Data Plane)의 분리를 통해 선언적 인프라 관리(Declarative Infrastructure)를 실현한다.

NIST SP 800-145 기반 클라우드 아키텍처 개념도:

```text
+------------------------------------------------------------------+
|                    CLOUD COMPUTING STACK                          |
+------------------------------------------------------------------+
|  Service Models:                                                 |
|  +-------------------------------------------------------------+ |
|  | SaaS  |  Gmail, Office365, Salesforce  (End-User)            | |
|  +-------+------------------------------------------------------+ |
|  | PaaS  |  Kubernetes, App Engine, Heroku  (Developer)         | |
|  +-------+------------------------------------------------------+ |
|  | IaaS  |  EC2, S3, VPC, GCE, Azure VM   (Architect)          | |
|  +-------+------------------------------------------------------+ |
|                                                                   |
|  Deployment Models:                                               |
|  +----------+----------+-----------+------------+--------------+ |
|  | Private  | Public   | Hybrid    | Community  | Multi-Cloud  | |
|  | (전용)    | (공용)    | (혼합)     | (공동)      | (다중 CSP)    | |
|  +----------+----------+-----------+------------+--------------+ |
|                                                                   |
|  Essential Characteristics (NIST 800-145):                        |
|  • On-demand Self-Service    • Broad Network Access              |
|  • Resource Pooling          • Rapid Elasticity                  |
|  • Measured Service (미터링/과금)                                  |
+------------------------------------------------------------------+
       |                                    |
       v                                    v
+--------------+                    +------------------+
| Control Plane | ◄--API/SDK-------- |  Data Plane       |
| (관리/제어)    |                    |  (실제 트래픽)      |
+--------------+                    +------------------+
```

**왜 클라우드 아키텍처가 필수인가?**
- **비용 구조 변화**: IDC 보고서상 클라우드 전환 기업은 5년 TCO 평균 30~40% 절감
- **Time-to-Market 단축**: 인프라 프로비저닝 2~4주 -> 5분 이내(IaC 기반)
- **글로벌 가용성**: 멀티리전 Active-Active 구성으로 99.99% SLA 달성
- **기술 민주화**: ML/AI(BigQuery ML, SageMaker), 양자컴퓨팅(Braket) 등 고가 자원의 민주적 접근

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **'수도권 통합 전기 그리드'**와 같다. 발전소(IaaS 데이터센터)의 전력·주파수를 한전(Control Plane)이 API로 실시간 제어하고, 가정·공장(Workload)은 필요할 때만 사용한 만큼만 요금을 내며, 정전 시 다른 그리드(멀티리전)로부터 자동 복구된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **① 네트워크 패브릭 ② 컴퓨트 추상화 ③ 데이터 계층 ④ 오케스트레이션 ⑤ 옵저버빌리티** 5계층으로 구성된다. 각 계층은 API로 연결되며, IaC(Terraform, Pulumi, CloudFormation)와 GitOps(ArgoCD, Flux) 도구로 선언적 관리된다.

레퍼런스 클라우드 네이티브 아키텍처:

```text
                        +-------------------------+
                        |   Edge / CDN Layer      |
                        |  (CloudFront, Cloud CDN) |
                        +------------+------------+
                                     |  HTTPS / QUIC
                        +------------v------------+
                        |  API Gateway / WAF      |
                        |  (Kong, AWS API GW)     |
                        +------------+------------+
                                     |
              +----------------------+----------------------+
              |                      |                      |
    +---------v---------+   +---------v---------+  +--------v--------+
    |  Auth Service     |   |  BFF / GraphQL     |  |  Async Worker   |
    |  (OIDC/OAuth2)    |   |  (Apollo, Hasura)  |  |  (SQS/Kafka)    |
    +---------+---------+   +---------+---------+  +--------+--------+
              |   mTLS                  |  gRPC               |
              |                         |                     |
    +---------v-------------------------v---------------------v--------+
    |                    Service Mesh (Istio / Linkerd)                  |
    |   • Sidecar Proxy (Envoy)  • mTLS  • Traffic Mgmt (Canary/Blue)  |
    +---------+-----------------------+-----------------------+--------+
              |                       |                       |
    +---------v---------+    +---------v---------+    +--------v--------+
    |  Microservice A   |    |  Microservice B   |    |  Microservice C |
    |  (Stateless)      |    |  (Stateful)       |    |  (Batch/AI)     |
    |  HPA: CPU/Mem     |    |  StatefulSet      |    |  Job/CronJob    |
    +---------+---------+    +---------+---------+    +--------+--------+
              |                       |                       |
    +---------v-----------------------v-----------------------v--------+
    |              Data Layer (Polyglot Persistence)                    |
    |  RDBMS (Aurora) | NoSQL (DynamoDB) | Cache (Redis) | Object(S3)  |
    +------------------------------------------------------------------+
              |                                            |
    +---------v---------+                        +---------v----------+
    |  Observability    |                        |  Platform Layer    |
    |  (Prom/Grafana/   |                        |  (K8s, Karpenter,  |
    |   Loki/Tempo)     |                        |   Crossplane, OPA) |
    +-------------------+                        +--------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Edge / CDN** | 글로벌 정적 콘텐츠 전송, DDoS 완화, TLS 종단 | Anycast 네트워크, PoP 200+ 엣지 로케이션, HTTP/3, Brotli 압축, Lambda@Edge (엣지에서 JS 실행) |
| **API Gateway / WAF** | 인증·인가, 트래픽 라우팅, Rate Limiting, 스키마 검증 | OAuth 2.0 / JWT 검증, OPA(Open Policy Agent) 정책, Lambda Authorizer, Circuit Breaker 패턴 |
| **Service Mesh** | 서비스 간 mTLS, 트래픽 관리(카나리/블루그린), 관측성 | Envoy Sidecar(1.21+), Istio Control Plane(xDS API), eBPF로 Sidecar 제거(Cilium Service Mesh), Ambient Mesh |
| **Container Orchestration** | 컨테이너 스케줄링, 자가치유, 오토스케일링, 선언적 배포 | Kubernetes 1.30+, Kustomize/Helm, Karpenter(노드 프로비저닝 90% 단축), KEDA(이벤트 기반 HPA), Cluster Autoscaler |
| **Data Layer** | 다중 데이터 저장소(PoP: Polyglot Persistence), CQRS·Event Sourcing | RDS Proxy(Connection Pool), DynamoDB DAX(< 1ms 캐시), Aurora Global Database(< 1초 크로스 리전 복제), S3 Standard-IA(30일 후 자동 계층화) |
| **Observability Stack** | 메트릭·로그·트레이스 통합 수집 및 분석 | OpenTelemetry(OTLP), Prometheus + Grafana, Loki(로그), Tempo/Jaeger(분산 트레이싱), eBPF(커널 레벨 모니터링), AIOps for 이상탐지 |

### 핵심 알고리즘·프로토콜 원리

**1) Consistent Hashing (분산 캐시·객체 스토리지)**
- Ring 구조에 노드와 키를 해시 분포, 가상 노드(VNode) 150~200개로 데이터 편향 최소화
- Cassandra/DynamoDB가 채택, 노드 추가/제거 시 K/N 만큼의 키만 재배치

**2) Raft Consensus (분산 코디네이션)**
- Leader Election(과반수 투표) + Log Replication + Term 번호로 Split Brain 방지
- etcd, Consul, Kafka KRaft가 사용, Raft Quorum = ⌊N/2⌋+1

**3) CAP Theorem 선택**
- **CP 시스템**: HBase, etcd, MongoDB (네트워크 분할 시 일관성 우선, 쓰기 거부)
- **AP 시스템**: Cassandra, DynamoDB, S3 (가용성 우선, Eventually Consistent)

**4) Auto Scaling 알고리즘**
- HPA: `desiredReplicas = ceil[currentReplicas × (currentMetricValue / targetMetricValue)]`
- Predictive Scaling: ARIMA/LSTM으로 24시간 사전 예측 (CloudWatch Predictive Scaling)
- Karpenter: Spot/On-Demand 혼합, Bin-packing으로 비용 30% 절감

- **📢 섹션 요약 비유**: 클라우드 네이티브 아키텍처는 **'항공사 허브 시스템'**과 같다. 공항(API Gateway)이 항공편을 분류하고, 관제탑(Service Mesh)이 항공기 간 충돌 방지·이착륙 순서(mTLS, 트래픽 관리)를 관리하며, 격납고(Container)가 항공기(마이크로서비스)를 자동으로 정비·대수 배정(스케일링)한다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처의 핵심 개념 비교:

| 구분 | **Monolithic (전통적)** | **Microservices (클라우드 네이티브)** | **Serverless (FaaS)** |
| :--- | :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/EAR | 컨테이너 이미지 (Docker, OCI) | 함수 코드 (zip, 컨테이너) |
| **확장성** | 수직 확장 (Scale-up) | 수평 확장 (HPA, Karpenter) | 자동·무제한 (Concurrency 기반) |
| **장애 격리** | 프로세스 단위, 전파 위험 | Pod/Service 단위 격리, Circuit Breaker | 함수 단위 격리, DLQ |
| **개발 속도** | 느림 (긴 빌드, 통합 테스트) | 빠름 (독립 배포, Trunk-based) | 매우 빠름 (코드만 업로드) |
| **운영 복잡도** | 낮음 (단일 프로세스) | 높음 (분산 추적, 서비스 메시 필요) | 중간 (콜드 스타트, 벤더 종속) |
| **비용 모델** | 상시 가동 (피크 기준 과금) | 리소스 사용량 | 호출당 과금 (GB-초) |
| **적합 사례** | 레거시 시스템, 단순 CRUD | 대규모 트래픽, 도메인 복잡 | 이벤트 드리븐, 간헐적 워크로드 |
| **콜드 스타트** | N/A | N/A (이미 실행 중) | 100ms~3s (SnapStart, Provisioned Concurrency) |

**클라우드 간(AWS vs Azure vs GCP) 핵심 서비스 매핑:**

| 기능 영역 | **AWS** | **Azure** | **GCP** |
| :--- | :--- | :--- | :--- |
| 컴퓨트 (IaaS) | EC2, Lambda | Virtual Machines, Functions | Compute Engine, Cloud Functions |
| 컨테이너 | EKS, Fargate | AKS, Container Apps | GKE, Cloud Run |
| 오브젝트 스토리지 | S3 (11 9s 내구성) | Blob Storage | Cloud Storage |
| 관계형 DB | Aurora, RDS | Cosmos DB, SQL DB | Cloud SQL, Spanner (Global) |
| 메시지 큐 | SQS, SNS, Kinesis | Service Bus, Event Grid | Pub/Sub |
| IaC | CloudFormation, CDK | ARM Template, Bicep | Deployment Manager, Config Connector |
| IAM | IAM, Cognito | Entra ID, RBAC | Cloud IAM, Workload Identity |
| 네트워킹 | VPC, Transit GW | VNet, VWAN | VPC, Cloud Interconnect |

**연계 기술 스택:**
- **CI/CD**: GitHub Actions -> ArgoCD -> Argo Rollouts (Progressive Delivery)
- **보안**: HashiCorp Vault(시크릿) + Falco(런타임 위협 탐지) + Trivy(이미지 스캔) + OPA/Gatekeeper(정책)
- **FinOps**: Kubecost(쿠버네티스 비용 시각화) + Vantage(멀티클라우드 비용 분석) + AWS Cost Explorer
- **데이터 거버넌스**: DataHub / Unity Catalog (메타데이터 카탈로그), Apache Iceberg (테이블 포맷)

- **📢 섹션 요약 비유**: Monolithic는 **'대형 유조선'**, Microservices는 **'컨테이너 선박 fleet'**, Serverless는 **'카셰어링'**이다. 유조선은 한 번 움직이면 막대한 연료가 들지만 적재량^, 컨테이너 선박은 표준화된 컨테이너(API) 단위로 유연하게 조합, 카셰어링은 필요할 때만 빌려 타고 반납한다(콜드
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 780 / 800

<- **이전**: [779. 클라우드 아키텍처 핵심 토픽 779번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/779_cloud_architecture_core_topic_779_exam_summar/)
**다음**: [781. 클라우드 아키텍처 핵심 토픽 781번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/781_cloud_architecture_core_topic_781_exam_summar/) ->

---
