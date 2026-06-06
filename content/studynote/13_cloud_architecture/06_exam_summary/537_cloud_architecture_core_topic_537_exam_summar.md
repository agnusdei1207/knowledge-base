---
title: "Cloud Architecture Core Topic 537 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처의 본질은 "가상화·컨테이너화·오케스트레이션을 통한 IT 자원의 추상화(Abstraction)와 API 기반 프로그래머블 셀프서비스"이며, 12-Factor App 원칙, 마이크로서비스 분해, 불변 인프라(Immutable Infrastructure), 선언적 정책(Declarative Policy) 4대 축이 모든 설계 결정의 근간을 이룬다.
> 2. **가치**: IaaS/PaaS/SaaS/FaaS 모델을 통해 CAPEX->OPEX 전환, TCO 30~40% 절감(Forrester Research 기준), 배포 주기 6개월->1일, 글로벌 멀티리전 가용성 99.99% (연 52.6분 장애), Auto-Scaling을 통한 Peak-time 10배 트래픽 흡수, MTTR 평균 70% 단축이 대표적 정량 효과다.
> 3. **판단 포인트**: Public/Private/Hybrid/Multi-Cloud 4-way 트레이드오프, Lift&Shift(Rehost) vs Re-platform vs Re-architecture(Re-build) 마이그레이션 전략, 동기(REST/gRPC) vs 비동기(Pub/Sub·Event Streaming) 통신, CAP 정리의 Consistency vs Availability, Stateful(StatefulSet·DB) vs Stateless(Deployment) 워크로드 분리, 비용 최적화(RI·Spot·Savings Plan) vs 성능·탄력성 균형이 기술사형 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 IT는 2006년 AWS S3·EC2 출시 이후 "유틸리티 컴퓨팅"으로의 패러다임 전환을 겪었다. 전통적 온프레미스(Procurement-Centric) 환경은 (1) 용량 예측 실패에 따른 30~40% 유휴 자원, (2) 프로비저닝 리드타임 4~8주, (3) CAPEX 중심의 Sunk Cost 문제, (4) 단일 장애점(SPOF)·수직 확장 한계, (5) DR(Disaster Recovery) 사이트 별도 구축 비용이라는 5대 구조적 한계를 가졌다.

NIST SP 800-145는 클라우드 컴퓨팅을 "네트워크, 서버, 스토리지, 애플리케이션, 서비스 등 구성 가능한 컴퓨팅 자원의 공유 풀(Shared Pool)에 대해 어디서나(on-demand network access)·측정 가능한 서비스(Measured Service)로 제공되는 모델"로 정의하며, 5대 필수 특성(On-Demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)과 3대 서비스 모델(IaaS/PaaS/SaaS), 4대 배치 모델(Public/Private/Hybrid/Community)을 규정한다.

클라우드 네이티브(Cloud-Native) 아키텍처는 CNCF(Cloud Native Computing Foundation)에 의해 "컨테이너·서비스 메시·마이크로서비스·불변 인프라·선언적 API"를 활용하는 접근 방식으로 정의되며, KubeCon·CNCF Landscape 1,000+ 프로젝트를 통해 사실상 산업 표준으로 자리 잡았다. Gartner는 2025년 이후 신규 엔터프라이즈 워크로드의 70% 이상이 클라우드 네이티브 기반으로 구축될 것으로 예측한다.

```text
[클라우드 아키텍처 패러다임 전환도]

  +-----------------+      +-----------------+      +-----------------+
  |  Mainframe Era  | --->  |  Client-Server  | --->  |   Cloud-Native  |
  |   (1970~1990)   |      |   + SOA/Web     |      |   Era (2010~)   |
  +-----------------+      +-----------------+      +-----------------+
        |                         |                         |
   Monolithic               Distributed           Microservices
   Vertical Scale           Horizontal Scale     Container/K8s/Serverless
   CAPEX 100%               CAPEX->OPEX 전환       Usage-based Metering
   4~8주 Provisioning       1~2주 Provisioning    1분~1시간 Auto-Provisioning
   단일 IDC                 Active-Standby DR     Multi-Region Active-Active
   SPOF 다수                SPOF 일부 잔존         Region/AZ 단위 격리

   [클라우드 컴퓨팅 5대 필수 특성 (NIST SP 800-145)]
   +--------------------------------------------------------------+
   |  ① On-Demand Self-Service   (API/Console 자동 프로비저닝)    |
   |  ② Broad Network Access     (HTTP/HTTPS, 표준 프로토콜)     |
   |  ③ Resource Pooling         (Multi-Tenant 가상화)           |
   |  ④ Rapid Elasticity         (Scale-out/in 1분 이내)          |
   |  ⑤ Measured Service         (CPU·Mem·Net·Storage 미터링)    |
   +--------------------------------------------------------------+
```

기존 온프레미스 대비 클라우드의 필요성은 (1) **비즈니스 민첩성**(신규 시장 진입 시 인프라 즉시 확보), (2) **글로벌 확장성**(CDN·Edge 노드 200+ POP 활용), (3) **기술 민주화**(Kafka·SageMaker·Bedrock 같은 매니지드 PaaS를 클릭으로 도입), (4) **재해복구 자동화**(Cross-Region Replication, RDS Multi-AZ), (5) **FinOps 실현**(Showback/Chargeback) 5가지 관점에서 설명된다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "자가 발전하는 스마트 그리드"와 같다. 화력발전소(전용 발전기) 대신, 수요가 늘면 자동으로 전기를 더 보내고 줄이면 회수하는 그리드처럼, 트래픽 변동에 따라 컴퓨팅·스토리지 자원이 탄력적으로 흐른다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 4계층(Layered Reference Architecture)은 **① 인프라 계층(IaaS)** -> **② 런타임/플랫폼 계층(PaaS·CaaS)** -> **③ 애플리케이션 계층(SaaS·FaaS)** -> **④ 거버넌스 계층(Security·FinOps·Observability)** 로 구성된다. 각 계층은 추상화 수준을 높이며, 상위 계층로 갈수록 비즈니스 로직 집중도가 증가한다.

핵심 메커니즘은 (1) **가상화·컨테이너화**(Hypervisor: KVM/Xen/ESXi, Container Runtime: containerd/CRI-O, Sandbox: gVisor/Kata), (2) **오케스트레이션**(Kubernetes Control Plane: API Server/etcd/Scheduler/kubelet), (3) **서비스 디스커버리**(DNS-based: CoreDNS, Service Mesh: Istio/Linkerd), (4) **선언적 정책**(IaC: Terraform/Pulumi, GitOps: ArgoCD/Flux), (5) **관측가능성**(Metrics: Prometheus, Logs: Loki/EFK, Traces: Jaeger/Tempo) 5대 원리로 동작한다.

```text
[클라우드 네이티브 4계층 + Kubernetes 중심 참조 아키텍처]

   +------------------------------------------------------------------+
   |  ④ 거버넌스 계층: IAM/RBAC · KMS · CloudTrail · FinOps · SIEM   |
   +------------------------------------------------------------------+
   |  ③ 애플리케이션 계층 (SaaS / FaaS)                                |
   |     SaaS:  SaaS (Slack·Salesforce)   PaaS: Heroku·App Engine    |
   |     FaaS:  AWS Lambda · Azure Func · Cloud Run · Cloud Functions|
   |     API Gateway · GraphQL · API Composition                      |
   +------------------------------------------------------------------+
   |  ② 런타임/플랫폼 계층 (PaaS / CaaS)                              |
   |   +----------------------------------------------------------+   |
   |   |  Kubernetes (k8s) Control Plane                           |   |
   |   |  +----------+  +------+  +----------+  +----------+     |   |
   |   |  | API Srv  |  |etcd  |  |Scheduler |  |Controller|     |   |
   |   |  +----+-----+  +------+  +----+-----+  | Mgr(CM)  |     |   |
   |   |       +-----------+------------+----------+            |   |
   |   |                   v                                     |   |
   |   |  Worker Node 1, 2, 3 ...                                |   |
   |   |  +--------------+ +--------------+ +--------------+    |   |
   |   |  | kubelet      | | kube-proxy   | | CNI (Calico) |    |   |
   |   |  | +----------+ | | iptables/IPVS| | Pod-to-Pod   |    |   |
   |   |  | |containerd| | +--------------+ | Routing      |    |   |
   |   |  | +----------+ |                                       |   |
   |   |  | Pod: App+C   |  Sidecar: Envoy/Istio (mTLS, Tracing) |   |
   |   |  +--------------+                                       |   |
   |   +----------------------------------------------------------+   |
   |   Helm/ArgoCD · Operator Pattern · CRD · HPA/VPA/Cluster Autoscaler|
   +------------------------------------------------------------------+
   |  ① 인프라 계층 (IaaS)                                             |
   |  Region -> AZ -> Edge Location                                      |
   |  Compute: EC2·VM·BareMetal · GPU(인스턴스: p4d·H100)              |
   |  Storage: Block(EBS)·Object(S3)·File(EFS)·Archive(Glacier)       |
   |  Network: VPC·Subnet·Transit GW·PrivateLink·Cloud Interconnect    |
   |  Hypervisor: KVM·Xen·ESXi · Unikernel · Firecracker MicroVM       |
   +------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Region / AZ (가용 영역)** | 지리적 격리 단위, 장애 도메인 | Region 내 2~4개 AZ, AZ 간 Latency < 5ms, 100km 이내 거리, Multi-AZ 시 Synchronous Replication (RPO=0) |
| **가상화 / 컨테이너 런타임** | OS·커널·자원 격리 | Type-1 Hypervisor(KVM/Xen) + LXC/cgroup·namespace -> containerd/CRI-O -> Pod 단위 cgroup v2·seccomp·AppArmor |
| **Kubernetes Control Plane** | 클러스터 상태 조정 (Reconciliation Loop) | API Server(REST) -> etcd(raft 합의) -> Scheduler(노드 점수) -> Controller Manager(Desired vs Actual State) -> kubelet(Heartbeat) |
| **Service Mesh (Istio/Linkerd)** | L7 트래픽 제어·mTLS·관측 | Envoy Sidecar(EnvoyFilter), xDS API로 CDS·EDS·LDS·RDS 동적 설정, mtls STRICT/PERMISSIVE 모드, Telemetry V2 (Envoy WASM) |
| **오토스케일링 (HPA·VPA·CA·KEDA)** | 부하 기반 탄력적 확장 | HPA: CPU/메모리/Custom Metric(MQ Length) -> Scale-out, VPA: Resource Recommender, Cluster Autoscaler: Node Group 확장, Karpenter: Spot·Fargate 1초 프로비저닝 |
| **API Gateway / BFF** | 외부 트래픽 진입점, 인증·라우팅 | Kong/Apigee/AWS API Gateway: OAuth 2.0 + JWT 검증, Rate Limiting(Token Bucket 1000 RPS), BFF(Backend-For-Frontend) 패턴으로 채널별 응답 최적화 |
| **메시지 큐 / 이벤트 스트림** | 비동기·이벤트 기반 결합도 완화 | Kafka(Raft KRaft 모드, Partition 100+/Topic), RabbitMQ(AMQP 0-9-1, DLX), AWS SQS·SNS·EventBridge(At-least-once), Pub/Sub, NATS |
| **매니지드 데이터 계층** | RDB·NoSQL·캐시·검색 분리 | RDS Aurora(MySQL/PG, 6-way Replication)·DynamoDB(Global Tables, P99 < 10ms)·ElastiCache(Redis Cluster)·OpenSearch·BigQuery/Snowflake/Databricks(레이크하우스) |
| **IaC / GitOps** | 인프라·앱 배포의 선언적 자동화 | Terraform(상태파일 HCL)->S3 Backend+DynamoDB Lock, Pulumi(Multi-lang), ArgoCD(ApplicationSet·Sync Wave), Atlantis(Terraform PR 봇) |
| **Observability 3-Pillar** | Metrics·Logs·Traces 통합 | Prometheus(Grafana Mimir)·Loki/Promtail·Tempo/Jaeger OTLP, OpenTelemetry SDK -> Collector -> Vendor Backend, RED/USE/SLI-SLO 방법론 |
| **보안/컴플라이언스** | Zero-Trust, 암호화, 감사 | IAM(SCP·Permission Boundary)·KMS(CMEK·HSM)·VPC Flow Log·GuardDuty(ML 이상행탐지)·CSPM(Wiz·Prisma Cloud)·KSPM(Kubernetes) |
| **FinOps** | 비용 가시화·최적화·거버넌스 | CUR(비용 사용 리포트)·CUDOS·Kubecost·Spot/RI/Savings Plan 권장, Tagging Strategy(Env·Team·CostCenter), Showback/Chargeback |

**Kubernetes 핵심 알고리즘 (기술사 빈출)**: Pod 스케줄링은 **2-Phase Filter-Score** 방식으로, (1) NodeSelector·Affinity·Taint/Toleration·Resource Request·PVC 바인딩으로 **필터링**, (2) LeastAllocated·BalancedAllocation·NodeLocality·TaintSpread **점수화** -> Top-N 노드 선출. QoS Class는 (a) Guaranteed(Request==Limit), (b) Burstable(일부 설정), (c) BestEffort(미설정) 3단계로 분류되며, kubelet은 (c)->(b)->(a) 순서로 Pod Eviction을 수행한다.

**12-Factor App 12원칙**은 클라우드 네이티브의 설계 헌법이다: ①Codebase(1 Repo = 1 App), ②Dependencies(명시적 선언), ③Config(환경변수, 12-Factor 위반 #1 빈출), ④Backing Services(URL 추상화), ⑤Build/Release/Run(3단계 분리), ⑥Stateless Processes(상태 외부화), ⑦Port Binding(자체 포트), ⑧Concurrency(프로세스 모델), ⑨Disposability(빠른 시작/우아한 종료 SIGTERM), ⑩Dev/Prod Parity, ⑪Logs(STDOUT 이벤트 스트림), ⑫Admin Processes(1회성 작업).

- **📢 섹션 요약 비유**: 클라우드 아키텍처 4계층은 "도시 인프라"와 같다. ① 토지·도로(IaaS), ② 전기·수도·통신(PaaS), ③ 빌딩·상가(SaaS/FaaS), ④ 경찰·소방·재무(거버넌스) 계층이 추
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 537 / 800

<- **이전**: [536. 클라우드 아키텍처 핵심 토픽 536번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/536_cloud_architecture_core_topic_536_exam_summar/)
**다음**: [538. 클라우드 아키텍처 핵심 토픽 538번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/538_cloud_architecture_core_topic_538_exam_summar/) ->

---
