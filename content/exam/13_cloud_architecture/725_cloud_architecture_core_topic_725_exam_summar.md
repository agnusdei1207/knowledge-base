---
title: "Cloud Architecture Core Topic 725 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 가상화·컨테이너·오케스트레이션(K8s)·서버리스(FaaS)·IaC(Terraform/CloudFormation)·옵저버빌리티(Prometheus/EFK)를 기반으로 워크로드의 **탄력성(Elasticity)·가용성(HA)·확장성(Scalability)·무중단 배포(Zero-downtime)**를 SLA 99.99% 수준으로 보장하는 분산 시스템 설계 체계이다.
> 2. **가치**: 온프레미스 대비 **CapEx -> OpEx 전환**(40~60% 비용 절감), Auto Scaling으로 Peak 시 자원 활용률 80%^, MTTR 단축(< 5분), 글로벌 멀티리전 Active-Active로 RPO 0/RTO 분 단위 달성, 개발자 생산성 30~50% 향상.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs Multi-Cloud, 동기(East-West)·비동기(North-South)·이벤트 드리븐(EDA)·사가 패턴 등 **통신 모델 선택**, 12-Factor App + DDD Bounded Context + Cell-Based Architecture, Well-Architected 5대 축(운영 우수성·보안·안정성·성능 효율·비용 최적화) 트레이드오프 분석.

---

## Ⅰ. 개요 및 필요성

전통적 모놀리식 온프레미스 환경은 **수직 확장(Scale-Up) 한계, CAPEX 중심의 선형 비용 구조, 수개월의 프로비저닝 리드타임, Disaster Recovery의 이중화 비용(DR Site 30~50% 추가)**이라는 구조적 문제를 가진다. 2006년 AWS S3/EC2 출시 이후 클라우드는 **API 기반의 선언적 프로비저닝, 사용량 기반 과금(Pay-per-Use), Multi-AZ/Multi-Region 자동 이중화, Managed Service 추상화**로 IT 인프라의 패러다임을 근본적으로 전환시켰다.

특히 2014년 Kubernetes 출시, 2014년 AWS Lambda(Serverless) 출시, 2018년 CNCF 성숙기 진입, 2020년 코로나19 이후 Digital Transformation 가속화로 **클라우드 네이티브(Cloud-Native)** 아키텍처가 엔터프라이즈의 표준이 되었다. 2024년 기준 Gartner 보고서는 신규 워크로드의 70% 이상이 퍼블릭 클라우드에 배포되며, 한국은 2027년까지 클라우드 시장이 연평균 22% 성장(과기정통부 통계)할 것으로 전망된다.

기술사 관점에서 클라우드 아키텍처는 단순한 인프라 이전이 아닌 **도메인 경계(Bounded Context) 기반의 분해, 장애를 전제로 한 설계(Design for Failure), 관측 가능성(Observability) 내재화, FinOps 기반의 비용 거버넌스**라는 4가지 핵심 역량을 요구한다.

```text
+-----------------------------------------------------------------+
|              클라우드 아키텍처 진화 패러다임 비교                  |
+-----------------------------------------------------------------+
|                                                                 |
|  [On-Premise Monolith]  --->  [Virtualized Private Cloud]        |
|   +--------------+         +--------------+                     |
|   | 단일 RDBMS   |         | vSphere HA   |                     |
|   | 수직확장만    |         | DR 이중투자  |                     |
|   | MTTR: 시간   |         | MTTR: 분     |                     |
|   +--------------+         +--------------+                     |
|           |                          |                          |
|           v                          v                          |
|  [IaaS Cloud] ---> [PaaS/Container] ---> [Serverless/Cloud-Native]|
|   +--------------+  +--------------+  +--------------+          |
|   | EC2/VM       |  | K8s/Service  |  | Lambda/FaaS  |          |
|   | Auto Scaling |  | Microservice |  | Event-Driven |          |
|   | MTTR: 10분   |  | MTTR: 1분    |  | MTTR: 초     |          |
|   +--------------+  +--------------+  +--------------+          |
|                                                                 |
|  운영 패러다임:  Reactive ---> Proactive ---> Predictive          |
|  비용 모델:     CapEx ---> CapEx+OpEx ---> Pure OpEx              |
|  배포 주기:     분기/반기 ---> 주간 ---> 일간/시간 단위(Daily N회) |
+-----------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 클라우드 아키텍처 진화는 **'호텔식 주거 생활'**과 같다. 직접 집을 짓고 관리하던 방식(온프레미스 모놀리식)에서 이사만 하면 되는 원룸(Managed Service), 세제까지 맡기는 컨시어지 서비스(Serverless)로 발전해, 입주자는 **핵심 비즈니스(거주 활동) 자체에만 집중**할 수 있게 된 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **7계층 참조 모델(7-Layer Reference Model)**로 이해할 수 있다: ① 물리/리전(Region) -> ② 네트워크(VPC/Subnet) -> ③ 컴퓨팅(EC2/Container/Lambda) -> ④ 스토리지(Object/Block/Archive) -> ⑤ 데이터베이스(RDB/NoSQL/NewSQL) -> ⑥ 오케스트레이션(K8s/Service Mesh) -> ⑦ 관측/보안(Observability/Security/Compliance).

핵심 동작 원리는 **API 호출 -> 선언적 명세(IaC) -> 컨트롤 플레인(Control Plane)이 디시어드 상태(Desired State) 유지 -> 데이터 플레인(Data Plane)이 실제 트래픽 처리**라는 GitOps 사이클이다.

```text
+------------------------------------------------------------------+
|         Cloud-Native 7-Layer Architecture (AWS 기준 매핑)         |
+------------------------------------------------------------------+
|                                                                  |
|   [Client] --TLS 1.3---> [CloudFront/Cloud Armor WAF+DDoS]       |
|      |                         |                                 |
|      |                  [Route 53 Health Check]                  |
|      |                         |                                 |
|      v                         v                                 |
|   +----------------------------------------+                     |
|   |  L7: Observability & Security Layer    |                     |
|   |  CloudWatch(X-Ray) + GuardDuty + IAM   |                     |
|   |  Prometheus/Grafana + Falco + OPA       |                     |
|   +----------------------------------------+                     |
|                       |                                          |
|   +----------------------------------------+                     |
|   |  L6: Orchestration Layer               |                     |
|   |  EKS/K8s + Istio Service Mesh + ArgoCD |                     |
|   |  HPA/VPA/Cluster Autoscaler + Karpenter|                     |
|   +----------------------------------------+                     |
|                       |                                          |
|   +----------------------------------------+                     |
|   |  L5: Application & Data Layer          |                     |
|   |  Microservice(MSA) + Saga/CQRS         |                     |
|   |  Aurora/RDS + DynamoDB + ElastiCache   |                     |
|   |  S3(11 9s durability) + Glacier        |                     |
|   +----------------------------------------+                     |
|                       |                                          |
|   +----------------------------------------+                     |
|   |  L4: Messaging & Event Bus             |                     |
|   |  SQS(Queue) + SNS(Topic) + Kinesis     |                     |
|   |  Kafka/MSK + EventBridge(12-Factor)    |                     |
|   +----------------------------------------+                     |
|                       |                                          |
|   +----------------------------------------+                     |
|   |  L3: Compute Layer (Multi-Workload)    |                     |
|   |  EC2(IaaS) | EKS(Container) | Lambda    |                     |
|   |  Fargate(Serveless K8s) | ECS          |                     |
|   +----------------------------------------+                     |
|                       |                                          |
|   +----------------------------------------+                     |
|   |  L2: Network Layer (VPC)               |                     |
|   |  Private/Public Subnet × 3 AZ          |                     |
|   |  ALB/NLB + NAT GW + Transit GW         |                     |
|   |  VPC Peering + PrivateLink             |                     |
|   +----------------------------------------+                     |
|                       |                                          |
|   +----------------------------------------+                     |
|   |  L1: Region/AZ Physical Layer          |                     |
|   |  ap-northeast-2 (Seoul) +a/b/c (3 AZ)  |                     |
|   |  Edge Location + Direct Connect        |                     |
|   +----------------------------------------+                     |
+------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Control Plane** | 클러스터/리소스의 디시어드 상태 관리 | K8s API Server, AWS Control Tower, Terraform Cloud, Crossplane. 선언적 YAML/HCL로 정의하면 Reconciler가 수렴(Convergence)할 때까지 계속 보정. |
| **Data Plane** | 실제 트래픽 처리 및 비즈니스 로직 실행 | EC2 Nitro System(KVM 기반), Firecracker MicroVM(Lambda 실행 환경, 125ms Cold Start), Envoy Proxy(EnvoyFilter로 L7 라우팅). |
| **Auto Scaling** | 부하에 따른 탄력적 자원 확장/축소 | **3단계 모델**: (1) Reactive HPA(CPU/Mem 임계치 70%) -> (2) Predictive KEDA(이벤트 큐 길이) -> (3) Proactive Karpenter(Spot Interrupt + Bin-packing). Scale-out 60초, Scale-in 5분. |
| **Service Mesh** | 마이크로서비스 간 통신·보안·관측 | Istio/Linkerd가 Sidecar(Envoy) 주입 -> mTLS 자동 적용, Retry/Circuit Breaker/L7 Canary를 YAML로 선언, Distributed Tracing 자동 계측. Sidecar Overhead: p99 Latency +2~5ms, Memory +50MB/Pod. |
| **Observability** | 3대 신호(Metrics/Logs/Traces) 통합 | **RED Method**(Rate/Errors/Duration), **USE Method**(Utilization/Saturation/Errors), **SLI/SLO** 기반 Error Budget(예: 99.9% SLO = 월 43분 Downtime). OpenTelemetry(OTel) SDK로 Vendor-Neutral 수집. |
| **Storage Tiering** | 데이터 액세스 패턴별 비용 최적화 | Hot(S3 Standard $0.023/GB) -> Warm(IA $0.0125) -> Cold(Glacier Instant $0.004) -> Archive(Deep Archive $0.00099). **Lifecycle Policy**로 자동 전환, Intelligent-Tiering ML 기반 최적 배치. |
| **IaC (Infrastructure as Code)** | 인프라의 Git 기반 선언적 프로비저닝 | Terraform(Multi-Cloud HCL, State Lock by DynamoDB), Pulumi(General-purpose Language), AWS CDK(TypeScript/Python), Ansible(Config Mgmt). **Immutable Infrastructure** 원칙: 변경 시 신규 인스턴스 생성 후 Blue/Green 교체. |

핵심 알고리즘/원리 세부:
- **CAP Theorem 분산 환경 적용**: AP 시스템(DynamoDB/Cassandra - 가용성 우선, Eventually Consistent) vs CP 시스템(HBase/Etcd - 일관성 우선) vs CA 시스템(전통 RDBMS - 단일 노드). 클라우드는 **PACELC**(정상 시 Latency vs Consistency 트레이드오프) 모델로 확장.
- **Consensus Algorithm**: Raft(Paxos 변형) - K8s etcd, AWS S3 Strong Consistency(2020), CockroachDB. Leader Election(15s Timeout) + Log Replication(Majority Quorum).
- **Lambda Cold Start 최적화**: Provisioned Concurrency(상시 Warm), SnapStart(Corretto CRIU로 Init Phase 스냅샷, 200ms 이내), Lambda SnapStart for Java 8/11/17/21, ARM64(Graviton2) 34% 가격v + 19% 성능^.

- **📢 섹션 요약 비유**: 클라우드 7계층 아키텍처는 **'주차 가능한 50층 빌딩'**과 같다. 1층은 토지/지역(Region), 2~3층은 도로/주차장(Network), 4층은 사무실/회의실(Compute), 5층은 창고(Storage), 6층은 통신실(Orchestration), 7층은 방재/관제센터(Observability)다. 각 층이 독립적이면서 엘리베이터(Service Mesh)로 연결되어, 한 층에 문제가 생겨도 다른 층은 정상 운영된다.

---

## Ⅲ. 비교 및 연결

| 구분 | **IaaS (EC2/GCE)** | **PaaS (Elastic Beanstalk/App Engine)** | **Container (EKS/GKE/AKS)** | **Serverless (Lambda/Cloud Functions)** |
| :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | OS 미들웨어까지 사용자 | 런타임까지 PaaS | 컨테이너 이미지만 | 코드(함수)만 |
| **확장 단위** | VM 인스턴스 | 인스턴스 그룹 | Pod(수십 ms) | 함수 호출(수 ms) |
| **Cold Start** | 없음(상시) | 없음 | 5~30초(Image Pull) | 100ms~수초 |
| **Long-Running** | ◎(수일) | ○ | ◎ | △(15분 한계) |
| **Burst/Event** | △ | △ | ○ | ◎(S3 Trigger/EventBridge) |
| **비용 모델** | 시간/초 과금 | 인스턴스 시간 | Pod 시간 + 노드 | 호출 수(1M 무료) + GB-초 |
| **State 관리** | 자유(Stateless/Stateful) | 보통 | 자유 + Persistent Volume | 원칙적 Stateless(외부 상태) |
| **적합 워크로드** | 레거시 이관, HPC | 웹앱 표준 배포 | MSA 표준, AI/ML Inference | 비동기 처리, API Gateway 백엔드 |
| **예시 비용**(1k req/s, 200ms) | m5.large 24/7 ≈ $70/월 | App Service ≈ $50/월 | EKS Fargate ≈ $35/월 | Lambda ≈ $5/월 |

**연계 기술 통합 패턴**:
- **CI/CD 파이프라인**: GitHub/GitLab -> Jenkins/Argo Workflows -> Container Build(kaniko/Buildx) -> **SBOM(Syft/Trivy)** -> **Image Signing(Cosign/Sigstore)** -> **Admission Control(OPA Gatekeeper/Kyverno)** -> **Progressive Delivery(Argo Rollouts: Blue/Green + Canary)**
- **IaC-Policy-Code 통합**: Terraform Plan -> **OPA Conftest**(Policy as Code) -> Checkov(IaC 정적 분석) -> **Infracost**(PR 단계 비용 예측) -> Atlantis/Terraform Cloud PR Workflow
- **관측 스택**: **OTel Collector**(수집) -> **Tempo/Jaeger**(Trace) + **Loki**(Log) + **Mimir/Prometheus**(Metric) -> **Grafana**(시각화) -> **Alertmanager -> PagerDuty/OpsGenie**
- **보안 스택**: **Shift-Left**: Trivy(컨테이너) + Semgrep(SAST) + OWASP ZAP(DAST) -> **Runtime**: Falco(런타임 이상 행위) + eBPF(Tetragon/Cilium Tetragon) -> **CSPM**: Prisma Cloud/Wiz(클라우드 설정 감사)

- **📢 섹션 요약 비유**: IaaS/PaaS/Container/Serverless는 **'이사 서비스 단계'**와 같다. IaaS는 트럭만 빌리는 것(운전·정비는 직접), PaaS는 짐까지 옮겨주는 서비스, Container는 표준 박스에 효율적으로 포장, Serverless는 "짐이 있으면
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 725 / 800

<- **이전**: [724. 클라우드 아키텍처 핵심 토픽 724번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/724_cloud_architecture_core_topic_724_exam_summar/)
**다음**: [726. 클라우드 아키텍처 핵심 토픽 726번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/726_cloud_architecture_core_topic_726_exam_summar/) ->

---
