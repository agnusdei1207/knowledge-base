---
title: "Cloud Architecture Core Topic 726 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

```markdown
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 **선언형 API(Declarative API) + 컨트롤 루프(Reconciliation Loop) + 불변 인프라(Immutable Infrastructure)** 3축으로 추상화되며, Terraform/IaC·Kubernetes Operator·OCI 이미지를 통해 "원하는 상태(Desired State)"를 단일 진실 공급원(SSOT, Single Source of Truth)으로 코드화한다.
> 2. **가치**: 워크로드별 **4-Layer 서비스 모델(IaaS/CaaS/PaaS/FaaS)** 선택으로 운영 부담 40~70% 절감, HPA+VPA+Cluster Autoscaler의 3단 스케일링으로 p99 latency 30%v·비용 25%v, 멀티리전 Active-Active로 RTO 4h->5min·RPO≈0 실현.
> 3. **판단 포인트**: 워크로드의 **상태성(stateful/stateless) × 트래픽 변동성(spiky/steady) × 컴플라이언스 등급(PCI-DSS/개인정보보호법)** 매트릭스로 적절한 추상화 레벨을 결정하며, 벤더 종속(Lock-in) ↔ 출시 속도(TTM), 일관성(Consistency) ↔ 가용성(Availability) 간 CAP 트레이드오프를 정량적으로 평가해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 아키텍처는 **수직 확장(Scale-Up)**, **변경 가능 인프라(Mutable Infra)**, **수동 티켓 기반 운영**이라는 3대 제약으로 인해, 트래픽이 디지털 전환·모바일 폭증으로 GB당 1,000배 증가하는 현대 워크로드에 대응하지 못했다. Gartner(2024) 기준 글로벌 퍼블릭 클라우드 시장 규모는 **6,784억 USD**로 YoY 20.4% 성장 중이며, IDC는 2027년 신규 애플리케이션의 **80% 이상이 Cloud-Native 패턴**으로 개발될 것으로 전망한다.

클라우드 아키텍처는 (1) **Infrastructure as Code(IaC)**로 인프라를 GitOps 기반 버전 관리하고, (2) **컨테이너 오케스트레이션**으로 마이크로서비스 간 선언적 배포·네트워킹·롤아웃을 자동화하며, (3) **Serverless/FaaS**로 이벤트 기반 세밀한 과금(per-100ms)을 통해 유휴 자원 0을 실현한다. 핵심 패러다임 전환은 "**Pet vs Cattle**"로, 장애를 특수 사례로 취급하던 방식에서 컨테이너를 멸균 후 재생하는 **Phoenix Server** 모델로 이동했다는 점이다.

```text
[클라우드 네이티브 아키텍처 진화 흐름]

  Mainframe (1960s)        Client-Server (1990s)         3-Tier Web (2000s)
  +----------+             +----+    +----+             +----+  +----+  +----+
  | 단일 대형 |             | PC |---->|서버|             |Web |-->|App |-->| DB |
  | 컴퓨팅    |             +----+    +----+             +----+  +----+  +----+
  +----------+
        |                       |                          |
        v                       v                          v
   Scale-Up              Scale-Out (수동)            Scale-Out (Auto)
   Mutability            Mutability                  Mutable VM
        |                       |                          |
        +-----------+-----------+--------------+-----------+
                    v                          v
            Cloud-Native (2015~)       Serverless Edge (2020~)
            +-----------------+         +--------------+
            | K8s + Service   |         | FaaS + CDN   |
            | Mesh + GitOps   |         | Lambda@Edge  |
            | Immutable       |         | WASM/Firecr. |
            +-----------------+         +--------------+
```

기존 온프레미스는 "**고가용성을 위해 2배의 유휴 자원을 상시 점유**"했지만, 클라우드는 수요 변동에 따라 **수십 초 내 수백 노드로 확장**한다. Netflix는 2014년 AWS 전환 후, Black Friday 트래픽(평시의 8배)을 5분 내 흡수하며 동종 사고 0건을 달성했고, 이는 클라우드 아키텍처의 자기 치유(Self-healing) 능력 덕분이다.

- **📢 섹션 요약 비유**: 온프레미스는 "**회사 소유 사옥**"(고정 비용·수동 증축)이고, 클라우드는 "**시간 단위 회의실 대여 + 1분 전 100명 확장 가능 코워킹**"(사용량 과금·자동 신축)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 4-Layer 참조 모델(CNF, Cloud Native Foundation 정의)은 **인프라 계층(IaaS) -> 컨테이너 계층(CaaS) -> 런타임 계층(PaaS) -> 함수 계층(FaaS)**으로 추상화 수준이 점진적으로 상승하며, 각 계층은 상위 계층의 API로 캡슐화된다. 핵심 메커니즘은 **선언(Declare) -> 관측(Observe) -> 조정(Reconcile)**의 무한 컨트롤 루프이며, 이를 통해 시스템은 항상 desired state로 수렴한다.

```text
[클라우드 네이티브 4-Layer 아키텍처 + 컨트롤 루프]

                    +-----------------------------------------+
                    |  FaaS / Serverless (Lambda, Cloud Func) |
                    |  -- 이벤트 기반, 콜드스타트 100~300ms --|
                    +-----------------+-----------------------+
                                      | API GW
                    +-----------------v-----------------------+
                    |  PaaS / Managed Runtime (EKS, GKE, AKS)|
                    |  -- K8s API, HPA, Operator, CRD -------|
                    +-----------------+-----------------------+
                                      | Container Runtime
                    +-----------------v-----------------------+
                    |  CaaS (Docker, containerd, CRI-O)      |
                    |  -- OCI Image, OverlayFS, cgroup v2 ---|
                    +-----------------+-----------------------+
                                      | Hypervisor
                    +-----------------v-----------------------+
                    |  IaaS (EC2, Compute Engine, Nitro Sys.) |
                    |  -- KVM/Xen, VPC SDN, EBS gp3/io2 -----|
                    +-----------------------------------------+

  [컨트롤 루프 동작 사이클]
        +---------+   Observe    +--------------+
        |  User   |--------------->|  Actual State|
        |(Manifest|               |(K8s/Provider)|
        |  .yaml) |               +------+-------+
        +----+----+                      |
             | Declare                   | Diff
             v                           v
        +--------------+          +--------------+
        | Desired State|<----------|  Reconciler  |
        |   (SSOT)     |  Reconcile|  (Controller)|
        +--------------+          +------+-------+
                                         | API Call
                                         v
                                  +--------------+
                                  | Infra APIs   |
                                  |(EC2/LB/RDS)  |
                                  +--------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **선언형 IaC (Terraform/Pulumi)** | 인프라를 코드로 정의·버전 관리 | HCL(HashiCorp Configuration Language)로 `resource "aws_instance"` 블록 작성 -> `terraform plan`으로 desired/actual diff 계산 -> `apply`로 API 호출. 상태 파일(`terraform.tfstate`)을 S3+DynamoDB Lock으로 동시성 제어. |
| **컨테이너 런타임 (OCI 표준)** | 이미지 패키징·격리 실행 | OCI Image Spec v1.1(2023) 기반 layered FS(OverlayFS)로 AUFS/Btrfs 대체. `containerd 1.7+`는 CRI(Container Runtime Interface) gRPC로 Kubelet과 통신, eBPF 기반 Cilium CNI는 kube-proxy iptables 규칙 폭증(5,000svc 기준 250만 rule) 문제를 해결. |
| **Kubernetes 컨트롤러** | desired state로 수렴 | K8s Controller Manager 내 35개 내장 컨트롤러(Deployment/ReplicaSet/Endpoint…)가 `Informer` 캐시 + `Workqueue`로 watch-loop 실행. 사용자 정의 리소스(CRD)는 Operator 패턴(`controller-runtime` SDK)으로 도메인별 자동화(예: `cert-manager`로 TLS 자동 갱신). |
| **오토스케일링 3단 결합** | 부하-비용 최적화 | (1) **HPA**(CPU/Mem/Custom metric 15s 주기) -> (2) **VPA**(Pod 자원 권장값 자동 조정, 재시작 필요) -> (3) **Karpenter**(노드 프로비저닝, 30s 내 Ready). AWS 사례: Karpenter 도입 후 스케일 아웃 시간 4분->22초, 비용 38% 절감. |
| **서비스 메시 (Istio/Linkerd)** | L7 트래픽·정책·관측 | Envoy Proxy를 Sidecar로 주입, xDS(CDS/EDS/LDS/RDS) gRPC 스트림으로 설정 push. mTLS 자동화로 Zero-Trust 네트워크 구현, 헤더 기반 카나리(weight 10%->50%->100%), Fault Injection으로 카오스 엔지니어링. |
| **Observability 3-Pillar** | 메트릭·로그·트레이스 통합 | **Prometheus**(Pull 방식, PromQL, 30s scrape) + **Loki**(LogQL, 라벨 인덱스) + **Tempo/Jaeger**(OpenTelemetry OTLP, traceID 전파). Grafana 대시보드로 SLO 기반 Error Budget 추적. |
| **FaaS 콜드스타트 완화** | 이벤트 기반 응답 지연 단축 | AWS Lambda: SnapStart(Linux CRiu로 Init Phase 스냅샷, 콜드스타트 5s->200ms), Provisioned Concurrency(상시 워밍), Cloudflare Workers: V8 Isolates로 5ms 이내 부팅. |
| **Multi-Region Active-Active** | 글로벌 가용성·재해복구 | Route 53 Latency-Based Routing + DynamoDB Global Tables(다중 리전 복제, 1초 내 RPO) + S3 Cross-Region Replication(SRTC, 15분 RPO). 카카오·토스 사례: 리전 장애 시 30초 내 자동 페일오버. |

컨트롤 루프의 수학적 표현은 `Δ = |ActualState - DesiredState|`이며, K8s의 기본 reconcile 주기는 10초(조정 가능, `--minReadySeconds`). 분산 시스템의 **CAP 정리**에 따라 일관성·가용성·분단 내성 중 2개만 선택 가능하므로, 클라우드 아키텍처는 대부분 **AP(가용성+분단 내성)** 채택(예: DynamoDB Eventually Consistent, Cosmos DB Tunable Consistency) 후 결과적 일관성(Eventual Consistency)을 Saga 패턴/Outbox로 보완한다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "**자동 온도 조절 스마트 빌딩**"이다. 사용자가 "22℃"를 선언하면, 센서가 현재 온도를 관측하고, 차이가 나면 보일러/에어가 알아서 작동해 다시 22℃로 맞춘다. 이 과정에서 사람 개입이 없다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처의 핵심 의사결정 중 하나는 **추상화 레벨 선택**이다. 아래 표는 동일 "Hello World HTTP API" 워크로드를 4가지 모델로 구현했을 때의 트레이드오프를 정량화한 것이다.

| 구분 | **IaaS (EC2 + ALB)** | **CaaS (EKS/Fargate)** | **PaaS (App Runner/Cloud Run)** | **FaaS (Lambda)** |
| :--- | :--- | :--- | :--- | :---
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 726 / 800

<- **이전**: [725. 클라우드 아키텍처 핵심 토픽 725번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/725_cloud_architecture_core_topic_725_exam_summar/)
**다음**: [727. 클라우드 아키텍처 핵심 토픽 727번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/727_cloud_architecture_core_topic_727_exam_summar/) ->

---
