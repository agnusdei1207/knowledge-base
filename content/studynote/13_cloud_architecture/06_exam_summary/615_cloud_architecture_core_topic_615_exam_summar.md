---
title: "615. 클라우드 아키텍처 핵심 토픽 615번 시험 요약 (Cloud Architecture Core Topic 615 Exam Summary)"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 컨테이너(Container), 오케스트레이션(Kubernetes), 서비스 메시(Istio/Linkerd), IaC(Terraform/Pulumi), Serverless(Lambda/Cloud Run) 기반의 **클라우드 네이티브 4대 축(Container·CI/CD·Observability·DevOps)**을 통해 stateless·immutable·API-driven 설계 원칙을 구현하는 패러다임이다.
> 2. **가치**: CAPEX→OPEX 전환으로 TCO 30~40% 절감, Auto Scaling으로 트래픽 피크 시 자원利用率 70% 이상 향상, Multi-AZ·Multi-Region 구성으로 RTO 분 단위·RPO 0 달성, 배포 주기 1주→1일로 단축(Lead Time 90% 개선, DORA Elite 지표).
> 3. **판단 포인트**: **5대 아키텍처 결정 포인트** — (① 클라우드 셀렉션: Public vs Private vs Hybrid, ② 컴퓨트 모델: VM vs Container vs Serverless, ③ 데이터 계층: RDB vs NoSQL vs NewSQL, ④ 네트워크 토폴로지: Hub-Spoke vs Mesh, ⑤ 거버넌스: Centralized vs Federated) 간의 Trade-off 분석과 Well-Architected Framework 6대 필드(Operational Excellence·Security·Reliability·Performance Efficiency·Cost Optimization·Sustainability) 검토.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스(3-Tier Monolithic) 아키텍처는 **수직 확장(Scale-Up) 한계, 프로비저닝 리드타임(주 단위), 라이선스 종속성, 이중화 비용**이라는 4대 구조적 한계를 가진다. 2020년대 이후 트래픽 패턴이 평균에서 **Long-tail·Bursty·Spiky** 형태로 변화하면서, 고정 용량 프로비저닝은 자원 낭비(평균 15~25%)와 응답 지연(SLO 위반)을 동시에 유발한다.

이에 따라 **NIST SP 800-145**(2011, 2017 개정)가 정의한 5대 특성(On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)를 만족하는 클라우드 아키텍처가 산업 표준으로 자리잡았으며, Gartner 보고서(2023)에 따르면 전세계 퍼블릭 클라우드 지출은 5,646억 USD(2023) → 7,267억 USD(2027)로 연평균 6.5% 성장 중이다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│        온프레미스(레거시) vs 클라우드 네이티브(Cloud-Native) 비교도   │
└──────────────────────────────────────────────────────────────────────┘

[On-Premise Monolith]                       [Cloud-Native Distributed]
┌────────────────────┐                      ┌──────────────────────────────┐
│   Monolithic App   │                      │   Microservices (12+ pods)   │
│   (1.2GB WAR/EAR)  │                      │   ─────────────────────      │
│   ┌──────────────┐ │                      │   [API GW]→[SvcA,B,C,D,E]   │
│   │ UI+Biz+DB    │ │                      │     ↓        ↓    ↓          │
│   └──────────────┘ │                      │   [Service Mesh - Istio]     │
│         ↓          │                      │   [K8s + 3 Master Nodes]     │
│   ┌──────────────┐ │                      │   [Event Bus - Kafka]        │
│   │ Oracle RAC   │ │                      │   [Observability - 3 Pillars]│
│   │ (Exadata)    │ │                      └──────────────────────────────┘
│   └──────────────┘ │
│  HW Lead-time: 6~8주│                     HW Lead-time: 1~2분(Auto-Scale)
│  Deploy: 1회/월     │                     Deploy: 50~200회/일 (GitOps)
│  가용성: 99.9%      │                     가용성: 99.99% (Multi-AZ+Region)
│  비용: CAPEX 100억  │                     비용: OPEX 월 1.2억 (Pay-per-use)
└────────────────────┘

           [변화 동인 5가지]
  ① 디지털 트래픽 폭증(Moores' Law 초과)  ② Biz 가용성 요구 99.99%+
  ③ Edge Computing·AI 워크로드            ④ 보안 Zero-Trust 패러다임
  ⑤ ESG·탄소중립 → 자원 효율성
```

**📢 섹션 요약 비유**: 온프레미스는 "자기 집 짓기(설계 6개월, 공사 1년)"라면, 클라우드 네이티브는 "빈 방이 1,000개 있는 호텔에서 손님 수에 맞춰 즉시 객실 배정·청소·환기까지 자동화"하는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 4계층(Presentation·Application·Data·Infrastructure)을 클라우드 네이티브로 재설계할 때 핵심은 **무상태성(Statelessness), 불변 인프라(Immutable Infra), 선언적 API(Declarative API), 회복 탄력성(Resilience)** 4대 설계 원칙이다.

```text
[클라우드 네이티브 4계층 아키텍처 - AWS 기준 상세 매핑]

┌─────────────────────────────────────────────────────────────────────┐
│ L7: Edge & Delivery Layer                                          │
│   ├─ CloudFront (CDN)         - 600+ PoPs, TLS 1.3, HTTP/3         │
│   ├─ Route 53 (DNS)           - Latency-Based, GeoDNS, HealthCheck │
│   ├─ WAF v2 + Shield Advanced - L7 DDoS 방어, OWASP Top10 룰셋     │
│   └─ API Gateway (REST/GraphQL) - Throttling 10K RPS, AuthCognito  │
├─────────────────────────────────────────────────────────────────────┤
│ L6: Application & Orchestration Layer                              │
│   ├─ EKS / ECS Fargate        - Control Plane + 100~5,000 Nodes    │
│   ├─ Istio Service Mesh       - mTLS, Canary 5→25→50→100%          │
│   ├─ ArgoCD (GitOps)          - Sync 3분, Drift Detection 자동     │
│   └─ Knative / Lambda         - Cold Start 200ms, Scale to 0       │
├─────────────────────────────────────────────────────────────────────┤
│ L5: Data & Messaging Layer                                         │
│   ├─ Aurora Global Database   - 6 Replicas, <1s Cross-Region      │
│   ├─ DynamoDB DAX             - Microsecond Latency                │
│   ├─ S3 + Glacier             - 11 9s Durability, Lifecycle 정책   │
│   └─ MSK (Kafka) / Kinesis    - Partition 256, Exactly-Once        │
├─────────────────────────────────────────────────────────────────────┤
│ L4: Infrastructure & Observability Layer                           │
│   ├─ VPC (10.0.0.0/16)         - 3 AZs, /20 Subnet × 6             │
│   ├─ Transit Gateway          - 50+ VPC Hub-Spoke                  │
│   ├─ CloudWatch + X-Ray       - Trace+SLog+MMetric 3-Pillar        │
│   └─ Terraform / Pulumi       - State Locking, Plan→Apply          │
└─────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 계층 (Compute)** | 워크로드 실행 단위 | VM(EC2 m7i.4xlarge, 16 vCPU/64GB) / **Container(EKS, Fargate Spot 70%할인)** / **Serverless(Lambda 10GB RAM, 15분 타임아웃)** 3-Tier 선택; Container는 cgroup v2 + namespace 격리, 평균 부팅 1.2초, Image Layer 캐싱으로 풀 800MB → 레이어 5개 공유 80MB로 절감 |
| **오케스트레이터 (K8s)** | 컨테이너 라이프사이클 자동화 | **Control Plane**(API Server·etcd·Scheduler·Controller Manager) + **Worker Node**(kubelet·kube-proxy·CRI runtime); 선언형 Reconciliation Loop(Desired vs Actual State), HPA(CPU/Mem/Custom Metric) 30초 스케일링, Karpenter로 90초 내 노드 자동 프로비저닝 |
| **서비스 메시 (Service Mesh)** | L7 트래픽·정책·보안 통제 | **Sidecar 패턴**(Envoy 프록시 1:1 Pod 주입), **Istio Control Plane**(Istiod: Pilot+Citadel+Galley 통합), **xDS API**로 동적 설정 Push, mTLS 자동화로 Zero-Trust 구현, **Traffic Management**: VirtualService(라우팅), DestinationRule(Subset), Gateway(인/아웃바운드) 3-Resource 구성 |
| **데이터 계층 (Data Fabric)** | Polyglot Persistence | **RDB**(Aurora MySQL 5.6× RDS 대비 5배 TPS, 6-way 복제) / **NoSQL**(DynamoDB GSI+LSI, 1KB 단위 Partition Key) / **NewSQL**(CockroachDB PostgreSQL-wire compatible, Raft 합의) / **Cache**(ElastiCache Redis 7, Cluster Mode 500 Shard); CQRS + Event Sourcing으로 Read/Write 분리 |
| **옵저버빌리티 (3-Pillar)** | 시스템 가시성 확보 | **Metrics**(Prometheus 1s scrape, PromQL 집계) + **Logs**(Loki, ELK, 구조화 JSON) + **Traces**(OpenTelemetry SDK, Jaeger/Tempo로 100% Sampling); **SLO 기반 Alerting**: Error Budget 99.9% SLO → 월 43분 다운타임 허용, Burn Rate 14.4× 알람 |
| **IaC & GitOps** | 인프라 코드로 관리 | **Terraform 1.6+**(State Locking via DynamoDB, Plan→Apply 워크플로우, 200+ Provider) / **ArgoCD**(Application Controller 3분 sync, Self-Healing, Prune Resource); 선언적 Spec을 Git에 단일 진실 원천(SSOT)으로 보관 |

### 핵심 알고리즘 및 트레이드오프

**1. Auto Scaling 의사결정 공식**:
```
desiredReplicas = ceil[currentReplicas × (currentMetricValue / targetMetricValue)]
```
- HPA 기본: CPU 50% → min 2, max 100, stabilizationWindow 300초
- **Predictive Scaling**: 머신러닝(ML)로 14일 패턴 학습, 2시간 후 트래픽 예측(평균 오차 8%)
- **Karpenter** vs **Cluster Autoscaler**: Karpenter는 Pod 단위 Spot 인스턴스 90초 프로비저닝, CA는 Node Group 단위 4분

**2. CAP Theorem in Cloud**:
- **CP 시스템**: ZooKeeper(etcd), HBase, MongoDB(쓰기 시 majority 쿼럼)
- **AP 시스템**: Cassandra, DynamoDB, S3(Eventually Consistent, 1초 내)
- **CA 시스템**: RDBMS 단일 노드(현실적으로 분산 환경에서 CA는 불가능 → PACELC 확장)

**3. 비용 최적화 6대 레버**: RI 1~3년 약정(40~60%↓) + Savings Plan(전체 컴퓨트 30%↓) + Spot Instance(Fargate Spot 70%↓) + Right-Sizing(CloudOptimo 25%↓) + Lifecycle Policy(IA→Glacier 80%↓) + Graviton(ARM64, x86 대비 40% price/perf)

**📢 섹션 요약 비유**: K8s 오케스트레이터는 "100명의 요리사(컨테이너)에게 1,000개의 동시 주문(Order)을 받아 자동으로 배분·조리·서빙·설거지하는 지휘관"이고, Service Mesh는 "요리사들 사이의 식품 안전 검사관 + 배달 추적 시스템"이다.

---

## Ⅲ. 비교 및 연결

### 3-1. 컴퓨트 모델 비교

| 구분 | EC2 (IaaS VM) | EKS (Container) | Lambda (FaaS) |
| :--- | :--- | :--- | :--- |
| **시작 시간** | 1~3분 (AMI boot) | 5~30초 (Pod) | 200ms (Cold), 5ms (Warm) |
| **최대 단위 사양** | 448 vCPU / 24TB RAM | 100 vCPU / 1.2TB RAM | 10GB RAM / 6 vCPU |
| **타임아웃/장기실행** | 무제한 | 무제한 | 15분 (강제 종료) |
| **Scale 단위** | Instance | Pod (수평) | Function (Concurrent 1,000) |
| **가격 모델** | 시간/초 과금 ($0.04/hr) | Pod당 + Node | 호출당 + GB-초 ($0.0000166) |
| **적합 워크로드** | Stateful Legacy, GPU, License-bound | Stateless API, Microservice | Event-driven, Batch, Cron |
| **운영 부담** | OS 패치, AMI 관리 | Manifest, Image 빌드 | 코드만, 인프라 제로 |
| **Cold Start 이슈** | 없음 | 5~10초 (Image Pull) | 200ms~5초 (의존성) |
| **State 관리** | EBS Volume 영구 | PVC + StatefulSet | External Store(DDB/RDS) 필수 |
| **Vendor Lock-in** | 낮음 (K8s 호환) | 중간 (K8s 표준) | 높음 (벤더 종속 런타임) |

### 3-2. 데이터베이스 선택 Trade-off

| 구분 | RDS Aurora (RDB) | DynamoDB (NoSQL) | CockroachDB (NewSQL) | Neptune (Graph) |
| :--- | :--- | :--- | :--- | :--- |
| **데이터 모델** | Relational (SQL) | Key-Value/Document | Distributed SQL | Property Graph/RDF |
| **일관성** | Strong (ACID) | Eventually (조정 가능) | Strong (Serializable) | Strong (Read-your-writes) |
| **확장성** | 수직+읽기 복제 | 무제한 수평 | 무제한 수평 (자동 Shard) | Replica 15개 |
| **Latency (p99)** | 5~10ms (Single) | 1~5ms (DAX 0.5ms) | 10~20ms (Cross-region) | 30~50ms |
| **적합 사례** | 트랜잭션, ERP | 세션, IoT, 게임 | 글로벌 분산, 금융 | 소셜 그래프, 추천 |
| **TPS (Benchmark)** | 100K select/s, 25K write/s | 50M+ read, 10M+ write | 50K TPS/Node | 100K Query/s |

### 3-3. 배포 모델 비교 (NIST 정의 기반)

| 구분 | Public Cloud | Private Cloud | Hybrid Cloud | Multi-Cloud |
| :--- | :--- | :--- | :--- | :--- |
| **소유권** | Hyperscaler (AWS/Azure/GCP) | 자체 DC 또는 Hosted Private | Public + Private 연결 | 2개 이상 Public |
| **연결성** | Internet (VPN/DX) | 전용 회선 | Direct Connect / ExpressRoute | Transit Gateway Peering |
| **컴플라이언스** | 일반 (ISO/SOC) | 규제 산업 (금융·공공) | 데이터 분류별 배치 | 벤더 종속 회피 |
| **Latency** | 20~50ms (Region 내) | 1~5ms (Local) | Private Link 5ms | 50~
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 615 / 800

<- **이전**: [614. 클라우드 아키텍처 핵심 토픽 614번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/614_cloud_architecture_core_topic_614_exam_summar/)
**다음**: [616. 클라우드 아키텍처 핵심 토픽 616번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/616_cloud_architecture_core_topic_616_exam_summar/) ->

---
