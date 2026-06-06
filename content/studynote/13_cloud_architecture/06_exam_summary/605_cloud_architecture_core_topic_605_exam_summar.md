---
title: "Cloud Architecture Core Topic 605 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS 계층 위에 컨테이너 오케스트레이션(Kubernetes, ECS), 서비스 메시(Istio, Linkerd), IaC(Terraform, Pulumi), GitOps(ArgoCD, Flux) 기반의 불변 인프라(Immutable Infrastructure)와 선언형 API(Declarative API)를 결합하여, 워크로드의 탄력성·탄력적 확장·자가 치유·관찰 가능성을 코드와 정책으로 결정하는 엔지니어링 체계이다.
> 2. **가치**: AWS Well-Architected Framework 5대 축(운영 우수성, 보안, 신뢰성, 성능 효율, 비용 최적화) 및 6번째 축(지속 가능성)을 적용하면, 평균 35~70%의 TCO 절감, 배포 빈도 200배·복구 시간 24배·변경 실패율 7배 개선(2019 DORA State of DevOps Report), SLA 99.99%(연 52분 35초) 수준의 가용성을 달성할 수 있다.
> 3. **판단 포인트**: 단일 클라우드(Single Cloud) vs 멀티/하이브리드(Anthos, Azure Arc, Outposts) 트레이드오프, 동기식 통신(Synchronous REST/gRPC) vs 비동식 이벤트 기반(EventBridge, Kafka, Pub/Sub) 선택, 모놀리스 -> 마이크로서비스 -> 셀프 컨테인드 시스템(SCS) -> 서버리스 진화 경로, 그리고 12-Factor App + 카나리/블루그린 배포의 리스크-속도 균형점이 핵심 의사결정 기준이다.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스 3-tier 아키텍처(L7 스위치 - Web/App/DB) 기반의 시스템은 CAPEX(설비투자비) 80%+, 프로비저닝 주수~월 단위, 사용률 평균 6~12%로 운영 비효율이 극심했다. 2006년 AWS S3/EC2 출시 이후 클라우드 컴퓨팅은 가상화(KVM, Xen, Hyper-V) -> 컨테이너(Docker 2013) -> 오케스트레이터(Kubernetes 2015, Borg에서 파생) -> 서비스 메시(Istio 2017) -> 서버리스(Lambda 2014, Knative 2018) -> 엣지 컴퓨팅(WebAssembly, KubeEdge)로 진화하며, **"Infrastructure as Code, Policy as Code, Everything as Code"** 패러다임을 정착시켰다.

NIST SP 800-145는 클라우드를 5대 필수 특성(요구 기반 셀프 서비스, 광범위 네트워크 접근, 리소스 풀링, 빠른 탄력성, 측정 가능한 서비스)과 3대 서비스 모델(IaaS/PaaS/SaaS) + 4대 배포 모델(Public/Private/Hybrid/Community)로 정의하며, 이는 클라우드 아키텍처 설계의 가장 기본적인 분류 체계로 활용된다.

```text
   +--------------------------------------------------------------+
   |                  Cloud Computing Evolution Stack              |
   |                                                              |
   |   사용자/디바이스  -►  Cloud Console / API / CLI / IaC        |
   |      ^                                          |             |
   |      |                                          v             |
   |   +------------------------------------------------------+    |
   |   |  SaaS Layer:  Office 365, Salesforce, Slack, GitHub |    |
   |   +------------------------------------------------------+    |
   |   |  FaaS Layer:  AWS Lambda, Azure Functions,          |    |
   |   |               GCP Cloud Run jobs, Cloudflare Workers |    |
   |   +------------------------------------------------------+    |
   |   |  PaaS Layer:  EKS/ECS, GKE, AKS, App Runner,        |    |
   |   |               Cloud Foundry, Heroku, Render         |    |
   |   +------------------------------------------------------+    |
   |   |  IaaS Layer:  EC2, Compute Engine, Azure VM,        |    |
   |   |               Bare-Metal, Outposts, Local Zones     |    |
   |   +------------------------------------------------------+    |
   |      ^                                          |             |
   |      |                                          v             |
   |   +------------------------------------------------------+    |
   |   |  Foundation: Region -> AZ -> Edge Location -> PoP      |    |
   |   |  Hypervisor: Nitro, Firecracker, KVM, Hyper-V       |    |
   |   |  Network: VPC, Transit Gateway, Cloud Interconnect  |    |
   |   |  Storage: S3, EBS, EFS, FSx, Cloud Storage, Blob    |    |
   |   +------------------------------------------------------+    |
   +--------------------------------------------------------------+
```

기존 DC 운영은 *"서버 1대 추가 = 3개월"* 이었지만, 클라우드는 *API 호출 한 번 30초*에 컴퓨팅이 프로비저닝된다. 그러나 그 이면에는 **상호의존성 매핑**(예: EC2가 IAM + VPC + SG + EBS + ALB와 결합)과 **책임 분담 모델**(Shared Responsibility Model)을 정확히 이해하지 못하면 곧바로 비용 폭증, 데이터 유출, 성능 저하로 이어지는 함정이 존재한다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **전기 그리드(電力網)**와 같다. 발전소(IaaS), 변전소(PaaS), 가정의 전등(SaaS)에 이르기까지 계층이 있고, 사용자는 단지 콘센트에 꽂기만 하면 된다. 다만 *"전기 품질(가용성), 누진 요금(비용), 정전 시 비상발전기(DR)"* 라는 세 가지를 설계하지 않으면 큰 낭패를 본다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 네이티브 아키텍처는 **CNCF(Cloud Native Computing Foundation)**가 정의한 4대 영역(컨테이너화, 오케스트레이션, 마이크로서비스, 이식성 있는 IaC)과 **5대 트레일 맵**(컨테이너, CI/CD, 서비스 메시, 관찰가능성, 분산 추적)을 토대로 한다. 핵심 메커니즘은 크게 ① 컴퓨트, ② 네트워크, ③ 스토리지, ④ 메시/관측 4개 축으로 분해된다.

### A. 컴퓨트 계층 (Compute Plane)

```text
   +--------------------------------------------------------------+
   |              Workload Abstraction Decision Tree              |
   |                                                              |
   |                +-----------------------+                     |
   |       주기적?  |  Cron / Batch 작업?    |  -> FaaS / Step Func |
   |       +-------►|  (배치, 이미지 리사이즈)|    Lambda + S3      |
   |       |        +-----------------------+                     |
   |       |                                                        |
   |       |  HTTP/이벤트 트래픽?                                    |
   |       |  +-----------------------+                            |
   |       |  | 동시성 0~1000, 콜드스타트 |  -> Serverless Container|
   |       |  | 허용? (Cloud Run, App  |     Fargate, K Native   |
   |       |  |  Runner, Lambda+Custom)|                          |
   |       |  +-----------------------+                            |
   |       |                                                        |
   |       |  장시간 상주 Stateful?                                 |
   |       |  +-----------------------+                            |
   |       |  | 트래픽 패턴 규칙적·     |  -> EKS/ECS + ALB +     |
   |       |  | HPA 예측 가능, GPU/NIC |    Karpenter / Cluster  |
   |       |  | 같은 HW 의존성?       |     Autoscaler           |
   |       |  +-----------------------+                            |
   |       |                                                        |
   |       |  레거시/특수 HW/라이선스?                               |
   |       |  +-----------------------+                            |
   |       |  | 메인프레임, 라이선스 SW |  -> EC2, Outposts, BM   |
   |       |  +-----------------------+    Azure Stack Hub        |
   +--------------------------------------------------------------+
```

### B. Kubernetes 핵심 오브젝트 흐름 (Control Plane ↔ Data Plane)

```text
   +--------------- Control Plane (관리) ---------------+
   |  kubectl/Helm/ArgoCD -> API Server -> etcd         |
   |       |                                            |
   |       v                                            |
   |  Scheduler -► Controller Manager (Deployment,     |
   |              ReplicaSet, Service, Ingress, HPA)    |
   +----------------------+----------------------------+
                          | watch / list
                          v
   +--------------- Data Plane (워커 노드) ------------+
   |  kubelet ◄-- kube-proxy (CNI: Calico/Cilium)     |
   |       |                                            |
   |       v                                            |
   |  containerd / CRI-O --► Pod (cgroup, namespace)  |
   |       |                                            |
   |       v                                            |
   |  sidecar: envoy(istio-proxy), filebeat, vault-    |
   |  agent, otel-collector                             |
   +----------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Server** | 클러스터의 단일 진입점(Single Source of Truth), 모든 리소스의 CRUD·감사·인증 라우팅 | TLS 1.3, OIDC, RBAC, Admission Webhook(Mutating/Validating), OpenAPI v3 스키마 기반 선언 검증, `etcd` v3 gRPC 백엔드(`WAL`, snapshot 5분, compaction) |
| **Scheduler** | Pod를 노드에 바이너리 배치, 필터링(예: NodeSelector, Taint/Toleration, Affinity) -> 스코어링(LeastAllocated, BalancedResource) 2단계 알고리즘 | Scheduling Framework 17+ 플러그인, topology spread constraint, volume zone aware scheduling, PodSchedulingReadiness 게이팅 |
| **Controller Manager** | `Deployment`(롤링 업데이트: maxSurge 25%, maxUnavailable 0), `StatefulSet`(Stable Network ID + PVC), `DaemonSet`(노드당 1), `Job/CronJob` 등 reconcile 루프 실행 | `Reconcile -> Observe Diff -> Act` 패턴(Operator 패턴 기반), Custom Controller = CRD + Controller(예: Argo Rollouts, Crossplane, Cert-Manager) |
| **etcd** | 분산 KV 저장소, 모든 클러스터 상태 영속화 | Raft 합의 알고리즘(Leader/Follower/Candidate), Quorum = N/2+1, 1000 write/s@5KB 한계 -> **분리 클러스터화** 필요, `etcdctl defrag`/`snapshot save` 백업 필수 |
| **Pod/Container** | 최소 배포 단위, 네트워크/IPC/PID/Mount namespace 격리, cgroup v2로 CPU·메모리·I/O 제한 | `requests`(스케줄링 기준) vs `limits`(런타임 강제), OOMKilled/Evicted 이벤트, `securityContext`: runAsNonRoot, readOnlyRootFilesystem, seccomp=RuntimeDefault, capabilities drop ALL |
| **Service/Ingress** | L4(LB)+L7(HTTP Path/Host) 라우팅, ClusterIP(NodePort/LoadBalancer)/Ingress-Nginx, Gateway API | kube-proxy IPVS 모드(1k+ 서비스에서 iptables 한계 극복), Cilium eBPF 기반 kube-proxy 대체, AWS LB Controller -> NLB/ALB 자동 프로비저닝, External-DNS로 Route53 연동 |
| **Autoscaler 계층** | HPA(CPU/메모리/custom metric) / VPA(request 재계산) / Karpenter(노드 프로비저닝) / KEDA(이벤트 기반) | HPA v2: `behavior` 필드로 scaleUp/scaleDown 정책 분리, Karpenter: Spot Fleet + consolidation 60초 내 노드 추가, KEDA: Kafka lag, Cron, Prometheus 쿼리 트리거 |

### C. 네트워크 토폴로지 (Multi-AZ, Multi-Region)

```text
   Region: ap-northeast-2 (서울)
   +---------- AZ-a ----------+   +---------- AZ-c ----------+
   |  Public Subnet           |   |  Public Subnet           |
   |   +- ALB (internet-facing)|   |   +- NAT Gateway         |
   |  Private Subnet          |   |  Private Subnet          |
   |   +- EKS Node Group (×2) |   |   +- EKS Node Group (×2) |
   |  DB Subnet (isolated)    |   |  DB Subnet (isolated)    |
   |   +- Aurora Writer/Reader|   |   +- Aurora Reader       |
   +----------+----------------+   +----------+----------------+
              |  Transit Gateway Peering       |
              v                                v
   +--------------------------------------------------+
   |  Inter-Region: Tokyo (ap-northeast-1) DR Site    |
   |   - Aurora Global Database (RPO < 1s)            |
   |   - S3 Cross-Region Replication (CRR)            |
   |   - Route 53 Latency/Geolocation Routing         |
   +--------------------------------------------------+
```

### D. 관측 가능성(Observability) 3대 신호

- **메트릭**: Prometheus -> Thanos/Mimir/Cortex, 1초 스크레이프, PromQL `rate()`, `histogram_quantile()`. OpenMetrics 형식. Grafana 대시보드(Golden Signal: Latency, Traffic, Errors, Saturation + USE: Utilization, Saturation, Errors).
- **로그**: Loki/Loki(라벨 기반 인덱싱, Elasticsearch 대비 1/10 비용) 또는 OpenSearch. 구조화 로그(JSON), `traceId`/`spanId` 주입. Fluent Bit -> Kafka -> S3(Glacier) 계층화 스토리지.
- **트레이스**: OpenTelemetry SDK(자동/수동 계측) -> OTLP -> Jaeger/Tempo/Datadog APM. W3C Trace Context 전파. 샘플링(head-based 1%, tail-based 이상치 100%).

> **SLO/SLI 예시**: 가용성 SLI = `1 - (error_budget_burn / total_requests)`, 99.9% SLO일 때 월 43.83분 다운타임 허용, Error Budget Policy -> Burn Rate Alert (1시간 윈도우 14.4×, 6시간 윈도우 6× 멀티 윈도우).

### E. 보안 모델 (Zero Trust + Defense in Depth)

- **ID**: IAM Roles for Service Accounts(IRSA, OIDC 토큰 -> STS AssumeRole), Workload Identity(GKE), Pod Identity(EKS 2023+). SPIFFE/SPIRE로 workload identity 발급.
- **네트워크**: Security Group(상태저장) + NACL(상태비저장) + WAF(SQLi/XSS/L7 DDoS) + Shield Advanced(L3/4 DDoS) + VPC Flow Logs + PrivateLink/VPC Endpoint.
- **데이터**: KMS envelope 암호화, S3 SSE-KMS, RDS/Aurora TDE, Secrets Manager + External Secrets Operator, 마스킹·토큰화(DLP).
- **컴플라이언스**: AWS Config(규정 준수 평가) + CloudTrail(감사) + GuardDuty(위협 탐지) + Security Hub(통합 뷰) + Trusted Advisor.
- **공급망**: SLSA Level 3, Sigstore Cosign 이미지 서명, SBOM(CycloneDX/SPDX), Admission Controller(Kyverno/OPA Gatekeeper)로 `imagePullPolicy: Always`, 신뢰할 수 있는 레지스트리만 허용.

- **📢 섹션 요약 비유**: Kubernetes는 **"항공모함"**이다. 함재기
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 605 / 800

<- **이전**: [604. 클라우드 아키텍처 핵심 토픽 604번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/604_cloud_architecture_core_topic_604_exam_summar/)
**다음**: [606. 클라우드 아키텍처 핵심 토픽 606번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/606_cloud_architecture_core_topic_606_exam_summar/) ->

---
