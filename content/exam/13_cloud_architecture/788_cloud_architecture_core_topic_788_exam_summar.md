---
title: "Cloud Architecture Core Topic 788 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS의 서비스 모델과 Public/Private/Hybrid/Multi-Cloud의 배포 모델 위에서, Well-Architected Framework(보안·안정성·성능·비용·운영 우수성·지속가능성 6대 기둥) 및 12-Factor App 원칙을 통해 **탄력성(Elasticity), 장애 격리(Fault Isolation), 셀프서비스 프로비저닝, 선언적 IaC(Immutable Infrastructure)**를 달성하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: AWS Well-Architected Lab 기준 모범 사례 적용 시 **운영 비용 30~40% 절감, 배포 빈도 200배 증가(애자일 전환 시), 장애 복구 시간(MTTR) 60% 단축, 가용성 99.99%(Four-Nines) 달성**, FinOps 도입 시 클라우드 지출의 20~35% 최적화가 가능하며, Multi-AZ + Multi-Region 구성으로 연간 가동 중단 시간 52.56분->4.38분 수준까지 압축 가능하다.
> 3. **판단 포인트**: CAP Theorem 하에서 **일관성(Consistency) vs 가용성(Availability) 트레이드오프**, Synchronous(강결합, 낮은 지연) vs Asynchronous(느슨한 결합, Eventual Consistency) 통신 선택, Microservices Granularity(도메인 경계의 정확성), Lift-and-Shift(빠른 이전) vs Re-platforming vs Re-architecting(장기 가치), Serverless(콜드 스타트 지연 200~800ms) vs Container(상시 워밍) vs VM(가장 낮은 밀도)의 운영 모델 결정이 핵심 의사결정 분기점이다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스(Enterprise On-Premise) 아키텍처는 CapEx(자본 지출) 중심의 **수직적 확장(Scale-Up)**, 수동 프로비저닝(평균 서버 배포 6~8주), 정적 IP/방화벽 정책, 단일 장애점(SPOF) 회피형 HW 이중화로 구성되어, 비즈니스 변동성에 유연하게 대응하지 못하는 한계가 있었다. 2006년 AWS S3/EC2 출시 이후 IaaS가 상용화되고, 2014년 Kubernetes v1.0, 2014년 AWS Lambda(서버리스 패러다임 전환), 2018년 EKS/AKS/OKE 같은 Managed Kubernetes, 2020년경 Service Mesh(Istio 1.0 GA 이후)와 eBPF 기반 관측성, 2023년경 LLM/Generative AI 워크로드의 GPUaaS 폭증으로 클라우드 아키텍처는 **클라우드 네이티브(Cloud-Native) 4대 축 — Containers / Orchestration / Microservices / DevSecOps —** 위에서 재정의되었다.

기술사 시험에서는 **클라우드 도입의 기술적·조직적·재무적 정당성, 마이그레이션 전략(6R: Rehost/Replatform/Refactor/Repurchase/Retire/Retain), 하이브리드/멀티클라우드 거버넌스, 클라우드 네이티브 12-Factor 및 K8s 기반 운영 모델, FinOps와 그린 컴퓨팅**을 종합적으로 평가한다. 즉, 단순히 "클라우드 서비스"를 나열하는 것이 아니라, **왜(Why) 어떤 아키텍처 패턴을 선택해야 하는가**에 대한 공학적 판단력을 검증한다.

```text
[클라우드 아키텍처 진화 패러다임 비교]

   2000s              2010s               2018~2020            2021~2024           2024~
 +----------+      +----------+       +----------+        +----------+       +----------+
 |On-Premise| ----> |  IaaS    | ---->  |Cloud-Nat.|  ---->  | Serverless| ----> |AI/Edge   |
 |Monolith  |      |Lift&Shift|       |K8s+MSA   |        |+Mesh+Fin |        |+Quantum  |
 +----------+      +----------+       +----------+        +----------+       +----------+
   6~8주 배포        1~2일 VM 기동       10분 컨테이너        초 단위 함수        GPUaaS
   수직확장          수평+수직 하이브리드   선언적 HPA/VPA        Event-Driven        LLM 추론
   수동 CapEx        OpEx+Predict        GitOps+ArgoCD        Pay-per-Invoke      분산 추론
```

클라우드 도입의 핵심 동인은 **(1) 비즈니스 민첩성(Time-to-Market 단축), (2) 글로벌 확장성(Global Footprint, Multi-Region), (3) 운영 부담 경감(Managed Service 활용), (4) 비용 최적화(사용량 기반 과금, Reserved/Spot 차등), (5) 재해복구(DR) 내장**으로 요약되며, 한국 공공부문의 경우 **클라우드 이용 촉진에 관한 법률(2024년 시행, "클라우드 컴플라이언스 검증" 의무화)** 및 금융권의 **금융 클라우드 컴플라이언스 가이드라인(2022.12, 금융위원회)** 등 규제 환경이 도입 전략에 직접 영향을 미친다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 진화는 마치 **"사제 식당(온프레미스) -> 대형 프랜차이즈 벤더(IaaS) -> 도시락 배달 앱 클라우드키친(클라우드 네이티브) -> 주문 즉시 조리 서빙(서버리스)"**으로 변해 온 과정과 같다. 손님(비즈니스)은 더 이상 주방(HW)을 짓지 않고, 메뉴(API)와 배달(Service Level)만 신경 쓰면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 크게 **① 인프라 계층(Virtualization/Hypervisor/KVM/Xen/VMware), ② 런타임 계층(Container Runtime/containerd/CRI-O, WASM), ③ 오케스트레이션 계층(Kubernetes/Control Plane/Data Plane), ④ 서비스 계층(Service Mesh, Service Discovery, API Gateway), ⑤ 관측/보안 계층(Observability Stack, Zero Trust, CSPM)**으로 추상화된다. 12-Factor App은 이러한 추상화의 애플리케이션 측면 설계 원칙(코드 베이스, 의존성, 설정, 백킹 서비스, 빌드/릴리스/실행 분리, 무상태 프로세스, 포트 바인딩, 동시성, 폐기 가능성, dev-prod parity, 로그 스트림, Admin Process)을 정의한다.

핵심 동작 메커니즘은 **선언적 API(Declarative API)와 Reconciliation Loop(조화 루프)**이다. Kubernetes의 경우 사용자가 `kubectl apply`로 `desiredState`(Pod 3개, replicas=3)를 선언하면, kube-controller-manager의 각 컨트롤러(Deployment/ReplicaSet/Pod Controller)가 `currentState`를 지속적으로 관찰(watch)하며 차이를 reconcile한다. 이 **"Observe -> Diff -> Act"** 루프가 수십 개 노드, 수천 개 Pod 규모에서도 자가 치유(Self-healing) 및 자동 확장이 가능하게 하는 본질이다.

```text
[클라우드 네이티브 아키텍처 5계층 + 데이터/제어 평면]

   +------------------------------------------------------------------------------+
   |                    Layer 5: Application (Microservices/Function)              |
   |  +----------+  +----------+  +----------+  +----------+  +----------+        |
   |  | Auth Svc |  | Order Svc|  | Pay Svc  |  | Notif Svc|  | LLM Svc  |  ...   |
   |  +----+-----+  +----+-----+  +----+-----+  +----+-----+  +----+-----+        |
   |       |   Sidecar(Envoy/Istio Proxy: mTLS, Retry, CircuitBreaker)             |
   +-------+--------------+--------------+--------------+--------------+------------+
   |  Layer 4: Service Mesh + API Gateway(Kong, AWS API GW, Apigee, Envoy)         |
   |            [Service Discovery(K8s DNS/CoreDNS, Consul)]                       |
   +------------------------------------------------------------------------------+
   |  Layer 3: Orchestration (Kubernetes 1.30+, k3s, Nomad, EKS, AKS, GKE)        |
   |   [HPA, VPA, KEDA, Cluster Autoscaler, Karpenter(2023~), ArgoCD/Flux GitOps]  |
   +------------------------------------------------------------------------------+
   |  Layer 2: Container Runtime (containerd 1.7+, CRI-O, gVisor, Firecracker)    |
   |            [OCI Image Registry(Harbor, ECR, ACR), BuildKit, Buildpacks]       |
   +------------------------------------------------------------------------------+
   |  Layer 1: Infrastructure (IaaS / Bare-Metal / Edge)                           |
   |   [VPC, Subnet, IAM, EBS/EFS/S3, KMS, GPU Pool(H100/A100), Nitro Enclave]     |
   +------------------------------------------------------------------------------+

   Data Plane(트래픽) <-━━━━━━━━━━━━ Control Plane(설정/제어) ━━━━━━━━━━━━━━━━->

   eBPF(cilium)        K8s API Server    IAM/OIDC         Cloud Controller Manager
   XDP(부하분산)        etcd(raft)        Cloud IAM        Cluster API(클러스터 자체)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Hypervisor / Bare-Metal** | 물리 자원의 가상화, Strong Isolation | Type-1: KVM(QEMU+KVM), Xen, Hyper-V, VMware ESXi(Type-1, Bare-metal), AWS Nitro System(2017~, 경량 하이퍼바이저 + 전용 HW 카드, VM당 <1% 호스트 자원 오버헤드). Type-2: VirtualBox, VMware Workstation. 컨테이너 대비 **강한 보안 경계(커널 분리)** 제공하지만 밀도(밀집도)는 낮음(1호스트당 수십~수백 VM). |
| **Container Runtime** | Linux Namespace(PID/Network/Mount/UTS/IPC/User) + cgroups(v1->v2 unified) 기반 프로세스 격리, OCI(Open Container Initiative) 표준 준수 | containerd(v1.7~), CRI-O(K8s 전용 경량 런타임), runc(OCI 표준 reference 구현), gVisor(샌드박스 커널, 멀티 테넌시 보안), Firecracker(μVM, AWS Lambda/Lambda@Edge 기반, 부팅 125ms 미만, 메모리 오버헤드 <5MiB). |
| **Kubernetes Control Plane** | 선언적 상태 관리(Reconciliation Loop), 스케줄링, 자가 치유 | kube-apiserver(etcd 앞단 REST API, 인증·인가·Admission), etcd(Raft 합의 알고리즘, Quorum 기반, write≥50% 이상 노드 응답 필요), kube-scheduler(Bin-packing/스프레드/리소스 매칭), kubelet(노드 에이전트, cAdvisor로 자원 메트릭 수집). K8s 1.30 기준 50+ 리소스 타입(Pod, Deployment, StatefulSet, DaemonSet, Job, CronJob, Service, Ingress, NetworkPolicy, CRD). |
| **Service Mesh (Istio/Linkerd/Cilium)** | 서비스 간 mTLS, 트래픽 관리(카나리 90/10, A/B 테스트), 관측성(자동 metrics/logs/traces) | Istio 1.22(2024): Envoy Proxy를 Sidecar로注入, Istiod 단일 컨트롤 플레인(원래 Pilot/Citadel/Galley 통합), xDS API(LDS/RDS/CDS/EDS)로 동적 구성, Ambient Mesh(2023~) — Sidecar 제거, ztunnel(L4) + Waypoint(L7) 2단 분리. Linkerd 2.15(Linkerd2-proxy Rust 재작성, 10x 빠름, ~10MB 메모리). |
| **Auto-Scaling Stack** | 부하 변동에 따른 Pod/Node 자동 증감 | HPA(Horizontal Pod Autoscaler, v2: CPU/Memory + Custom/External Metrics), VPA(Vertical Pod, Resource Recommender), KEDA(Event-driven, Kafka/RabbitMQ/SQS 큐 길이 기반), Karpenter(AWS, 2023 GA, 노드 프로비저닝 30초 -> Spot/On-Demand 혼합, Bin-packing 최적화), Cluster Autoscaler(전통적, 노드 그룹 단위). |
| **Observability (3 Pillars)** | Logs, Metrics, Traces 통합 가시성 | **Metrics**: Prometheus(시계열 TSDB, PromQL, Pull 방식, retention 15일 기본, Thanos/Cortex/Mimir로 페타바이트 확장), Grafana, Datadog. **Logs**: EFK Stack(Elasticsearch+Fluentbit+Kibana) or Loki+Grafana(로그 인덱싱 없이 라벨 기반). **Traces**: OpenTelemetry(SDK+Collector, OTLP 프로토콜, W3C TraceContext 전파), Jaeger, Zipkin, Tempo. **eBPF 기반**: Pixie, Cilium Tetragon, Falco(런타임 보안). |
| **IaC (Infrastructure as Code)** | 인프라의 선언적 코드화, Git 기반 버전 관리 | Terraform 1.7+(HCL, 멀티클라우드, State Locking with DynamoDB), Pulumi(TypeScript/Python/Go로 IaC 작성, SDK 기반), AWS CDK(L2/L3 Construct, CloudFormation 합성), Crossplane(K8s CRD로 클라우드 자원 관리), Ansible(설정 관리/프로비저닝). GitOps: ArgoCD(Application Controller, ApplicationSet), Flux CD. |
| **Security & Compliance** | Zero Trust, 암호화, 취약점 관리, 규제 준수 | Zero Trust(NIST SP 800-207, "절대 신뢰하지 않고 항상 검증"), mTLS(서비스 간 양방향 TLS, SPIFFE/SPIRE ID), OPA(Open Policy Agent, Rego 정책 언어), Kyverno(K8s 네이티브 정책), Falco(런타임 이상 행위 탐지), Trivy(컨테이너 이미지 SBOM/CVE 스캔
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 788 / 800

<- **이전**: [787. 클라우드 아키텍처 핵심 토픽 787번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/787_cloud_architecture_core_topic_787_exam_summar/)
**다음**: [789. 클라우드 아키텍처 핵심 토픽 789번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/789_cloud_architecture_core_topic_789_exam_summar/) ->

---
