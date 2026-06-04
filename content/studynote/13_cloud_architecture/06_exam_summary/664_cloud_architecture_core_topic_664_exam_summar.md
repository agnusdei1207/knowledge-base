---
title: "664. 클라우드 아키텍처 핵심 토픽 664번 시험 요약 (Cloud Architecture Core Topic 664 Exam Summary)"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS(Compute/Storage/Network 가상화) → PaaS(Managed K8s, Serverless) → SaaS(API·구독형 서비스) 의 책임 분담 모델을 기반으로, **Well-Architected 5대 펠러(운영 우수성·보안·안정성·성능 효율·비용 최적화)** 와 **CNCF Cloud Native 트래일맵(컨테이너→오케스트레이션→서비스 메시→관측가능성)** 을 통해 워크로드의 탄력성·가용성·확장성을 확보하는 분산 시스템 설계 청사진이다.
> 2. **가치**: AWS·Azure·GCP 3사 기준 동일 워크로드에서 **온프레미스 대비 30~70% TCO 절감**, Auto Scaling을 통한 **트래픽 피크 시 100배 확장**, 다중 AZ·리전 구성을 통한 **99.99%(52.6분/년) 가용성 SLA**, IaC(Terraform/Pulumi) 적용 시 배포 리드타임을 **수동 수 시간 → 자동 수 분** 수준으로 단축한다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs 멀티/하이브리드, 모놀리식 vs 마이크로서비스, **Stateless vs Stateful 워크로드 분리**, EKS vs GKE vs AKS vs Self-managed K8s 트레이드오프, CAP·PACELC 정리에 기반한 **리전 간 데이터 일관성 전략(동기 복제 vs 비동기 복제 vs CRDT)**, FinOps 기반의 스팟·예약·온디맨드 인스턴스 비율 최적화가 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 IT 시스템은 2006년 AWS S3·EC2 출시 이후 **On-Premise CapEx 중심 → Cloud OpEx 중심** 으로 패러다임이 전환되었고, 2014년 Docker 등장, 2015년 Kubernetes 1.0 GA, 2018년 CNCF의 Knative·Istio 졸업 이후 클라우드 네이티브는 단순한 "클라우드 이용"을 넘어 **"클라우드 철학에 맞는 애플리케이션 설계"** 로 진화했다. 전통적인 3-Tier 모놀리식 아키텍처는 수직 스케일링 한계, 배포 주기 수 주, 장애 도메인 단일화 문제를 안고 있었으며, 클라우드 아키텍처는 이를 **가상화·컨테이너화·오케스트레이션·관측가능성·IaC** 의 5개 축으로 해결한다. 특히 2020년 이후 **"Anywhere Operations"** 와 **"Industry Cloud"** 가 부상하면서, 퍼블릭 클라우드 단일 구성이 아닌 **하이브리드(Private Cloud + Public Cloud)·멀티 클라우드(2개 이상 퍼블릭)·엣지(5G MEC)** 의 조합형 아키텍처가 표준이 되었다.

```text
[클라우드 아키텍처 진화 흐름도: 2006 → 2025]

2006                  2013                2017                 2020                 2025
 │                     │                   │                    │                    │
 ▼                     ▼                   ▼                    ▼                    ▼
┌──────┐          ┌──────────┐        ┌──────────┐         ┌────────────┐     ┌──────────────┐
│ IaaS │          │  PaaS   │        │ CaaS    │         │ Serverless│     │ AI-Native    │
│ 1세대 │          │  2세대  │        │  3세대   │         │  4세대     │     │  5세대        │
└──┬───┘          └────┬─────┘        └────┬─────┘         └─────┬──────┘     └──────┬───────┘
   │                   │                   │                     │                    │
   ▼                   ▼                   ▼                     ▼                    ▼
 VM/Storage         RDS/Beanstalk       Docker/K8s         Lambda/Functions       LLM·Vector DB
 AWS EC2/S3         Heroku/OpenShift     K8s/Istio          Knative/Cloud Run    Bedrock/RAG

 책임: 사용자↑    책임: 사용자=    책임: 사용자↓        책임: 사용자 최소화    책임: AI 모델·데이터
         ↓       공유                 ↑                          ↑                      ↑
       벤더가 다 관리        컨테이너+오케스트    이벤트 기반 FaaS    +GPU·MaaS
```

기존 **"Lift & Shift(단순 이전)"** 전략은 클라우드의 진가가 아닌 단순 호스팅이고, 진정한 클라우드 아키텍처는 **"Re-platform(Managed 서비스 활용)", "Re-architect(Cloud-Native 재설계)"** 단계를 거쳐야 ROI가 극대화된다. Gartner 보고서에 따르면 Lift & Shift는 3년 내 ROI 20% 수준에 그치나, Re-architect는 평균 ROI 200% 이상을 달성한다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **"전기 그리드 발전"** 과 같다. 예전에는 각 가정·공장이 자체 발전소(On-Premise发电机)를 운영했으나, 이제는 중앙 발전소(클라우드)가 전기를 보내고, 우리는 전기 콘센트(API)에 플러그를 꽂기만 하면 된다. 다만 어떤 전기(220V/110V, DC/AC)·어떤 안정성(Generator Backup 필요 여부)을 쓸지는 우리가 설계해야 하므로, **"그리드(Grid) 자체를 설계하는 것"** 이 클라우드 아키텍처다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **5계층 참조 모델** (Physical → Virtualization → Orchestration → Service Mesh → Application) 과 **3축 운영 모델** (Observability, Security, FinOps) 의 교차점이다. 각 계층은 독립적 진화 가능하며(Loose Coupling), 상위 계층은 하위 계층의 추상화(Abstraction) 위에 동작한다.

```text
[클라우드 네이티브 5계층 + 3축 운영 모델 아키텍처]

                         ┌─────────────────────────────────────┐
                         │     Application Layer (L5)          │
                         │  Microservices · API · Frontend     │
                         │  (Spring Boot · NestJS · React)     │
                         └──────────────┬──────────────────────┘
                                        │ mTLS
                         ┌──────────────▼──────────────────────┐
                         │   Service Mesh Layer (L4)           │
                         │  Istio · Linkerd · Consul · App Mesh│
                         │  (Traffic Mgmt · Retry · AuthZ)     │
                         └──────────────┬──────────────────────┘
                                        │ CRD
                         ┌──────────────▼──────────────────────┐
                         │  Orchestration Layer (L3)           │
                         │  Kubernetes · EKS · GKE · AKS · OKE │
                         │  (Pod · Deployment · HPA · ArgoCD)  │
                         └──────────────┬──────────────────────┘
                                        │ Container Runtime
                         ┌──────────────▼──────────────────────┐
                         │  Virtualization Layer (L2)          │
                         │  Docker · containerd · CRI-O · gVisor│
                         │  (Cgroup · Namespace · OverlayFS)   │
                         └──────────────┬──────────────────────┘
                                        │ Hypervisor / Bare Metal
                         ┌──────────────▼──────────────────────┐
                         │   Physical Layer (L1)               │
                         │  X86 · ARM · GPU · DPU · Nitro       │
                         │  (C5n · Graviton3 · H100 · Trainium)│
                         └─────────────────────────────────────┘

        ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
        │Observability │  │   Security   │  │   FinOps     │
        │   (3축)      │  │   (3축)      │  │   (3축)      │
        ├──────────────┤  ├──────────────┤  ├──────────────┤
        │• Metrics     │  │• Zero Trust  │  │• Cost Alloc  │
        │  Prometheus  │  │  IAM+SSO     │  │  CUR·Tagging │
        │• Logs        │  │• Encryption  │  │• Spot/RI Mix │
        │  Loki·EFK    │  │  KMS·TLS 1.3 │  │• Auto-scaling│
        │• Traces      │  │• Compliance  │  │• Right-sizing│
        │  Jaeger·OTel │  │  PCI·ISO27001│  │• Anomaly Det │
        └──────────────┘  └──────────────┘  └──────────────┘
```

### 컨테이너 오케스트레이션(K8s) 핵심 동작 원리

Kubernetes의 Control Plane은 **etcd(분산 KV 저장소) → API Server → Scheduler → Controller Manager → kubelet** 의 선언적(Declarative) 루프를 통해 `Desired State = Actual State`를 지속적으로 수렴시킨다. 사용자는 `kubectl apply -f deployment.yaml`로 의도(Intent)를 제출하면, K8s는 **Reconciliation Loop** (기본 5초 주기) 를 돌며 `replicas: 3` 조건을 맞춘다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Server** | 클러스터 단일 진입점(Front Door) | REST API + watch 기반 pub/sub, RBAC·Admission Webhook으로 인증/인가/검증, 모든 상태 변경의 감사 로그(Audit Log) 기록 |
| **etcd** | 클러스터의 단일 진실 공급원(SSOT) | Raft 합의 알고리즘(Leader + Follower), Quorum = N/2+1, WiscKey 기반 SSD 최적화, `etcdctl snapshot`으로 백업/복구, **쓰기 latency 1ms 이하 목표** |
| **Scheduler** | Pod를 최적 Node에 배치 | Bin-packing·Spread·Affinity/Anti-affinity·Taint/Toleration·Topology Spread Constraints, 커스텀 Scheduler로 GPU 전용 노드 분리 가능 |
| **Controller Manager** | 상태 수렴 담당 | ReplicaSet·Deployment·StatefulSet·DaemonSet·Job/CronJob Controller가 `Status Phase`를 Desired와 비교, **Level-triggered** 방식(Edge-triggered 아님) |
| **kubelet** | Node 내 Pod Life-cycle 관리 | CRI(Container Runtime Interface) → containerd, CSI(Container Storage Interface) → EBS/EFS, CNI(Container Network Interface) → Calico/Cilium, **LivenessProbe 실패 시 자동 재시작** |
| **Service Mesh(Istio)** | L7 트래픽·보안 정책 | Envoy Sidecar(1Pod=1Envoy), mTLS 자동 발급(SPIFFE/SPIRE), **Canary: VirtualService weight 90:10 → 50:50 → 0:100**, Fault Injection(503·Latency) |

### 핵심 알고리즘·파라미터

1. **HPA (Horizontal Pod Autoscaler)** : `desiredReplicas = ceil(currentReplicas × currentMetricValue / targetMetricValue)`. 기본 metric-server 15초 주기, KEDA로 Kafka·SQS·Cron 기반 이벤트 드리븐 확장 가능.
2. **Consistent Hashing** : StatefulSet에서 `pod-{0..N-1}.svc.cluster.local` 형태로 안정적인 네트워크 ID 보장, MongoDB·Cassandra 샤드 키 라우팅에 사용.
3. **Readiness vs Liveness Probe** : Liveness=컨테이너 자체 건강(죽었으면 재시작), Readiness=트래픽 수신 가능 여부(미준비 시 Service Endpoint 제외). **초기 delay 30초**는 Spring Boot JVM 워밍업 고려 필수.
4. **CAP 정리와 클라우드 DB** : DynamoDB·Cosmos DB=AP(Eventually Consistent, `< 1초` 전파), Spanner·CockroachDB=CP(Strongly Consistent, TrueTime API), 전통 RDMS=CA(단일 노드 한계).
5. **Cost Optimization 공식** : `TCO = Compute + Storage + Network Egress + License + Observability + Security + Ops 인건비`. **Egress 비용**(AWS→On-Premise) 이 전체의 15~30%를 차지하므로, CloudFront·CDN 또는 데이터 주권(Residency) 고려 필수.

- **📢 섹션 요약 비유**: Kubernetes는 **"크루즈선의 자동 항법 시스템"** 이다. 선장(사용자)은 "부산행, 3,000톤 화물"이라는 **희망 상태(Desired State)** 만 선언하면, 자동항법장치(Controller)가 **현재 위치·연료·날씨(Actual State)** 와 비교해 엔진 출력·키 방향을 계속 보정한다. 배가 기울면(장애) 자가균형(Reconciliation)이 작동하고, 승객(트래픽) 은 안전 구역(Ready Pod)으로만 태운다.

---

## Ⅲ. 비교 및 연결

### 1) 배포 모델 비교 (On-Premise vs Private Cloud vs Public Cloud vs Hybrid vs Multi)

| 구분 | **On-Premise** | **Private Cloud** | **Public Cloud** | **Hybrid** | **Multi-Cloud** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **투자 방식** | CapEx(초기 100%) | CapEx + OpEx | OpEx 종량제 | 양쪽 혼합 | OpEx 다중 벤더 |
| **제어권** | 완전 통제 | 완전 통제 | 벤더 위임 | 데이터별 분리 | 워크로드별 분리 |
| **확장성** | 수직 스케일 한계 | 제한적(자본 한계) | 무제한(수 분 내) | 워크로드별 선택 | 벤더 failover |
| **가용성 SLA** | 99.9% (자체) | 99.95% (자체) | 99.99% (4개9) | 99.99% 이상 | 99.999% 설계 가능 |
| **TCO(3년)** | 100% 기준 | 80~110% | 30~60% | 50~80% | 60~100% |
| **주 사용 사례** | 규제·데이터 주권 | 정부·금융 | 일반 웹·SaaS | 레거시 연동 | 벤더 종속 회피 |
| **대표 기술** | vSphere | OpenStack·VMware Cloud | AWS·Azure·GCP | Anthos·Azure Arc·Outposts | Terraform·Crossplane·Karmada |

### 2) 컴퓨팅 추상화 수준 비교 (VM vs Container vs Function vs Edge)

| 구분 | **Virtual Machine** | **Container** | **Serverless Function** | **Edge Function** |
| :--- | :--- | :--- | :--- | :--- |
| **부팅 시간** | 30~120초 | 100~500ms | 5~100ms (콜드 스타트) | 1~10ms |
| **이미지 크기** | 5~20GB (GuestOS 포함) | 50~500MB (App + Lib) | N/A (벤더 런타임) | N/A |
| **밀도(호스트당)** | 10~50 VM | 100~1,000 컨테이너 | 수만 동시 실행 | 수십만 |
| **격리 수준** | 하드웨어 가상화(HW) | 프로세스·네임스페이스 | 프로세스 + 샌드박스 | V8 Isolates / Wasm |
| **상태** | Stateful 가능 | Stateless 권장 | Stateless 전용 | Stateless |
| **비용 모델** | 시간/월 정액 | 시간/리소스 | 호출당(GB-초) | 호출당(ms) |
| **적합 워크로드** | DB·레거시 ERP | MSA·API 서버 | 이벤트·ETL·웹훅 | CDN·API 캐싱 |
| **대표 기술** |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 664 / 800

<- **이전**: [663. 클라우드 아키텍처 핵심 토픽 663번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/663_cloud_architecture_core_topic_663_exam_summar/)
**다음**: [665. 클라우드 아키텍처 핵심 토픽 665번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/665_cloud_architecture_core_topic_665_exam_summar/) ->

---
