---
title: "730. 클라우드 아키텍처 핵심 토픽 730번 시험 요약 (Cloud Architecture Core Topic 730 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS의 서비스 모델과 Public/Private/Hybrid/Multi-Cloud 배포 모델을 기반으로, 컨테이너·오케스트레이션(Kubernetes)·서비스 메시(Istio)·API Gateway·IaC(Terraform/Pulumi)·Observability(OpenTelemetry)를 결합한 **분산·탄력적·장애 허용(Self-healing) 시스템 설계**의 총합이다.
> 2. **가치**: Auto-Scaling으로 트래픽 변동 시 자원 사용률을 30~70% 최적화하고, AZ(Availability Zone) 다중화·Region 복제로 RTO/RPO를 분 단위로 단축, CapEx->OpEx 전환과 Pay-per-use 모델로 인프라 TCO를 평균 20~40% 절감한다.
> 3. **판단 포인트**: Shared Responsibility Model 경계 설정, Statefull vs Stateless 워크로드 분리, Egress·API 호출·Managed Service 종속에 따른 **Vendor Lock-in vs 이식성(Portability)** 균형, 그리고 12-Factor/CNCF Cloud-Native 원칙 준수 여부가 아키텍처 품질을 결정한다.

---

## Ⅰ. 개요 및 필요성

전통적 모놀리식 아키텍처는 수직 확장(Scale-Up) 방식의 한계, 장애의 단일점(SPOF), 트래픽 예측 기반의 과잉/과소 용량 계획, 배포 주기 수개월의 Time-to-Market 지연, HW CapEx의 선투자 부담이라는 **5대 구조적 한계**를 가진다. 2006년 AWS S3·EC2 출시 이후 클라우드 컴퓨팅은 "필요 시 무한 자원"이라는 패러다임을 도입했고, 이는 **수평 확장(Scale-Out)**, **선언적 IaC(Declarative Infrastructure)**, **불변 인프라(Immutable Infrastructure)**, **DevOps + GitOps**의 4축으로 진화했다.

기술사 관점에서 730번 토픽은 단순히 "AWS 쓰는 법"이 아니라, **NIST SP 800-145 클라우드 정의**, **ISO/IEC 22123**, **클라우드 네이티브 컴퓨팅 재단(CNCF) Cloud Native Definition v1.0**, **AWS Well-Architected Framework 6 Pillars**, **Azure Architecture Center**, **Google Cloud Architecture Framework**를 통합한 **엔터프라이즈급 분산 시스템 설계 능력**을 검증한다. 특히 730번은 정보관리기술사·컴퓨터시스템응용기술사 출제 빈도가 높은 영역으로, KISA 클라우드 보안 인증(CSAP), 개인정보보호법 가이드라인, 전자금융감독규정의 컴플라이언스 요구사항과 결합되어 출제된다.

```text
+------------------------------------------------------------------+
|            클라우드 아키텍처 패러다임 전환 흐름                    |
+------------------------------------------------------------------+
|                                                                  |
|  [On-Premise Monolith] -------> [Private Cloud]                   |
|   • Scale-Up, SPOF             • Virtualization (KVM/VMware)     |
|   • HW CapEx 선투자            • HA Clustering                    |
|   • 수개월 배포주기              • Self-Service Portal            |
|           |                            |                         |
|           v                            v                         |
|  [Public Cloud IaaS] -------> [Cloud-Native]                     |
|   • EC2/VM Scale-Out           • Container + K8s                 |
|   • Pay-per-use                • Microservices + Service Mesh    |
|   • Region/AZ 이중화            • Serverless/FaaS                 |
|   • 수주 배포주기                • GitOps + Observability         |
|                                          |                       |
|                                          v                       |
|                              [Multi/Hybrid Cloud]               |
|                               • Workload Portability             |
|                               • Cloud Bursting                   |
|                               • Edge Computing 통합              |
|                                                                  |
+------------------------------------------------------------------+
```

기존 On-Premise 환경 대비 클라우드는 **탄력성(Elasticity)**, **글로벌 가용성(Global Reach)**, **무한 확장성(Infinite Scale)**, **고가용성(HA 99.99%+)**, **운영 효율성**, **보안 자동화**, **데이터 분석 통합**의 7가지 이점을 제공한다. 그러나 동시에 **데이터 주권(데이터 3법)**, **클라우드 종속성(Lock-in)**, **네트워크 지연(Egress 비용)**, **보안 통제 공백(Misconfiguration)**이라는 4대 신 risks가 발생하며, 이는 **Well-Architected Review**로 사전 통제해야 한다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **수도권 교통체계의 진화**와 같다. 과거 자가용 보유(On-Premise)는 사고 시 1대 마비, 도로 정체 시 대안이 없었다. 그러나 이제는 **KTX·지하철·공유 자동차·렌터카(Public/Private/Hybrid Cloud)**를 실시간 혼잡도·날씨·목적지에 따라 자유롭게 조합하여, 1시간 거리도 15분 만에 도달하는 **탄력적 이동 체계**가 가능해졌다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **프레젠테이션 계층(CDN/WAF) -> API 계층(Gateway/Service Mesh) -> 애플리케이션 계층(MSA/Serverless) -> 데이터 계층(Polyglot Persistence) -> 인프라 계층(IaC/K8s) -> 운영 계층(Observability/FinOps)**의 6계층 Reference Architecture로 표준화된다. 핵심 동작 원리는 **선언적 정의(YAML/HCL)** -> **컨트롤 루프(Reconciliation Loop)** -> **불변 배포(Immutable Artifact)** -> **관측 가능성(OpenTelemetry 3-Pillar: Metrics/Logs/Traces)**의 4단계로 요약된다.

```text
+--------------------------------------------------------------------+
|        6-Layer Cloud-Native Reference Architecture (CNRA)         |
+--------------------------------------------------------------------+
|                                                                    |
|  +----------------------------------------------------------+     |
|  | L1. Presentation: CloudFront/Cloudflare CDN + WAF + DDoS |     |
|  |     -> Edge Location 캐싱, TLS Termination, Bot Management|     |
|  +----------------------------------------------------------+     |
|                          | TLS 1.3, mTLS                          |
|                          v                                         |
|  +----------------------------------------------------------+     |
|  | L2. API Gateway: Kong/Apigee/ALB + Service Mesh (Istio)  |     |
|  |     -> Rate Limiting, Circuit Breaker, OAuth2/JWT, Routing |     |
|  +----------------------------------------------------------+     |
|                          | gRPC/REST                              |
|                          v                                         |
|  +----------------------------------------------------------+     |
|  | L3. Application: EKS/AKS/GKE + Microservices + FaaS      |     |
|  |     • Sidecar Pattern • HPA/VPA/Cluster Autoscaler       |     |
|  |     • Saga/CQRS/Event Sourcing • Lambda/Cloud Functions  |     |
|  +----------------------------------------------------------+     |
|                          |                                        |
|                          v                                         |
|  +----------------------------------------------------------+     |
|  | L4. Data: Polyglot Persistence                            |     |
|  |     • RDB (Aurora MySQL) + NoSQL (DynamoDB)               |     |
|  |     • Cache (Redis/ElastiCache) + Search (OpenSearch)     |     |
|  |     • OLAP (Redshift/BigQuery) + Lake (S3/ADLS GCS)      |     |
|  +----------------------------------------------------------+     |
|                          |                                        |
|                          v                                         |
|  +----------------------------------------------------------+     |
|  | L5. Infrastructure: Terraform/Pulumi + Ansible + ArgoCD  |     |
|  |     • GitOps (Single Source of Truth) • Policy as Code   |     |
|  |     • OPA/Kyverno • CIS Benchmark 자동 검증              |     |
|  +----------------------------------------------------------+     |
|                          |                                        |
|                          v                                         |
|  +----------------------------------------------------------+     |
|  | L6. Operations: Prometheus + Grafana + Loki + Tempo      |     |
|  |     + Jaeger + OpenTelemetry Collector                    |     |
|  |     • SLO/SLI/SRE Error Budget • FinOps (Kubecost)        |     |
|  +----------------------------------------------------------+     |
|                                                                    |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 계층** | 워크로드 실행·확장·격리 | EC2/VM (배치·레거시), 컨테이너(EKS/AKS/GKE/OpenShift) -> cgroup+namespace 기반 OS-level 가상화, FaaS(Lambda/Functions/Cloud Run) -> Cold Start 100~500ms, Warm Pool 관리 |
| **네트워크 계층** | L4/L7 라우팅·서비스 간 통신 | VPC/Subnet/CIDR 설계(10.0.0.0/16 권장), Transit Gateway(Hub-Spoke), PrivateLink/Private Endpoint, ALB/NLB(GLB), Service Mesh(eBPF + Envoy Sidecar) mTLS 제로트러스트 |
| **스토리지 계층** | 데이터 영속성·내구성·가용성 | Object(S3 11 9s, 3-way replication), Block(EBS gp3 4,000 IOPS), File(EFS/FSx for Lustre), Cold(S3 Glacier IR/Deep Archive) — **Hot-Warm-Cold 티어링**으로 비용 60% 절감 |
| **데이터 계층** | 트랜잭션·분석·검색 | RDB(Aurora 6-way replication, Read Replica 15개), NoSQL(DynamoDB Global Table Multi-Region), 캐시(Redis Cluster 30 Shard), 그래프(Neptune), 시계열(Timestream) |
| **오케스트레이션** | 컨테이너 라이프사이클 관리 | Kubernetes 1.30+ Control Plane(etcd RAFT 합의) + Worker(NodePool), Helm Chart 패키지, Operator Pattern(CRD+Controller), Kustomize 오버레이 |
| **관측 가능성** | 시스템 상태 가시화·장애 진단 | **3 Pillars**: Metrics(Prometheus 1초 해상도), Logs(Loki/ELK, 구조화 JSON), Traces(OpenTelemetry + Jaeger/Tempo, W3C TraceContext 전파) + Continuous Profiling(Pyroscope/Parca) |
| **보안·컴플라이언스** | 제로트러스트·정책 자동화 | IAM + ABAC/RBAC, KMS/HSM(Cloud HSM FIPS 140-2 L3), Secrets Manager/Vault, OPA/Gatekeeper, GuardDuty/Security Hub, Macie(데이터 분류) |
| **IaC·GitOps** | 인프라 선언적 프로비저닝·배포 | Terraform 1.7+(State Lock with DynamoDB), Pulumi(General-purpose Language), Ansible(설정 관리), ArgoCD/FluxCD(Git Repository = Source of Truth) |
| **FinOps** | 클라우드 비용 최적화·거버넌스 | Kubecost/Vantage/AWS Cost Explorer, RI/SP(예약 인스턴스 60%v), Savings Plan, Spot(90%v) + 자동 Recommendations, Showback/Chargeback |
| **DR·BCP** | 재해 복구·사업 연속성 | RTO/RPO 정의 -> Pilot Light / Warm Standby / Multi-Site Active-Active 3-tier, Cross-Region Replication, AWS CloudEndure/Azure Site Recovery |

**핵심 알고리즘·파라미터**:

- **Kubernetes HPA 공식**: `desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]` (CPU 70% 임계값 권장)
- **Cap Theorem 분산 트레이드오프**: Consistency / Availability / Partition Tolerance 중 2개 선택 -> 클라우드는 AP(PAXOS/Raft) 또는 CP(Quorum) 선택
- **Circuit Breaker**: Closed(정상) -> Open(임계치 초과·요청 차단) -> Half-Open(일부 요청 시험) 상태 머신
- **Bulkhead Pattern**: Thread Pool/Semaphore로 리소스 격리 (예: HikariCP Connection Pool)
- **SLA 계산**: 가용성 99.9% = 월 43.2분, 99.99% = 월 4.32분, 99.999% = 월 26초 downtime 허용
- **Lambda Concurrency 모델**: Reserved + Provisioned Concurrency로 Cold Start 제거, Account-level Quota 1,000 기본값

- **📢 섹션 요약 비유**: 클라우드 아키텍처 6계층은 **현대 백화점의 운영 체계**와 같다. 1층 전시장(Presentation/CDN)이 고객을 맞이하고, 2층 안내데스크(API Gateway)가 길을 안내하며, 3층 매장(Application/Service)이 실제 판매를 한다. 4층 창고(Data)가 상품을 보관하고, 5층 시설관리실(Infrastructure/Ops)이 전기관경·냉난방을 자동 조절하며, 6층 경영지원실(Observability/FinOps)이 CCTV·매출·재고를 실시간 분석한다. 어느 한 층이 멈춰도 전체가 자동 복구되는 **항체 시스템을 갖춘 백화점**이다.

---

## Ⅲ. 비교 및 연결

| 구분 | IaaS (EC2/GCE) | PaaS (Beanstalk/App Service) | CaaS (EKS/AKS/GKE) | FaaS (Lambda/Cloud Functions) |
| :--- | :--- | :--- | :--- | :--- |
| **제어 범위** | HW + OS + 미들웨어 + 앱 | 앱·데이터만 관리 | 컨테이너·앱·오케스트레이션 | 함수 코드만 관리 |
| **확장 단위** | VM 인스턴스 | App 인스턴스 | Pod/Deployment | 함수 호출 단위 |
| **확장 속도** | 분(minute) | 분 | 초(second) HPA | 밀리초(ms) Event-driven |
| **Cold Start** | N/A (상시 기동) | 분 단위 | 1~10초 (이미지 pull) | 100ms~10s |
| **상태 관리** | Stateful 가능 | Stateful 가능 | StatefulSet 가능 | **Stateless 원칙** |
| **장기 실행** | 무제한 | 무제한 | 무제한 | 15분(Lambda) 한계 |
| **적합 워크로드** | 레거시·DB·배치 | 웹앱·API | MSA·CI/CD | 이벤트·단순 API·ETL |
| **TCO 패턴** | CapEx 근접 | 중간 | OpEx 최적 | **Pay-per-Invocation 최적** |
| **Lock-in 정도** | 낮음 (API 표준화) | 중간 (Vendor Runtime) | 낮음 (K8s 표준) | 높음 (벤더 종속) |
| **운영 복잡도** | 높음 | 낮음 | 중간 (K8s 학습곡선) | 매우 낮음 (NoOps 지향) |

**연계 기술**:
- **DevOps/CI-CD**: GitHub Actions -> Jenkins -> ArgoCD(선언적 GitOps), Progressive Delivery(Canary/Blue-Green with Argo Rollouts/Flagger)
- **AIOps**:異常検知(Anomaly Detection) + 자동 근본 원인 분석(RCA) + Self-Healing (예: AWS DevOps Guru, Datadog Watchdog)
- **Edge Computing**: AWS Wavelength, Azure Edge Zones, Google Distributed Cloud — 5G MEC(Multi-access Edge Computing)와 결합하여 5ms 이하 지연
- **Zero-Trust Architecture**: BeyondCorp -> mTLS + Identity-Aware Proxy + SPIFFE/SPIRE(Workload Identity)
- **Confidential Computing**: AMD SEV-SNP, Intel TDX, NVIDIA H100 CC — 사용 중 데이터(Encryption at Use) 보호
- **Sustainable Cloud**: Region별 PUE(Power Usage Effectiveness), Carbon Footprint Dashboard, Spot
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 730 / 800

<- **이전**: [729. 클라우드 아키텍처 핵심 토픽 729번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/729_cloud_architecture_core_topic_729_exam_summar/)
**다음**: [731. 클라우드 아키텍처 핵심 토픽 731번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/731_cloud_architecture_core_topic_731_exam_summar/) ->

---
