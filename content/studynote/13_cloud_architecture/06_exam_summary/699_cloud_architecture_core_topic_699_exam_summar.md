---
title: "699. 클라우드 아키텍처 핵심 토픽 699번 시험 요약 (Cloud Architecture Core Topic 699 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 컨테이너 오케스트레이션(Kubernetes), 선언형 API, 서비스 메시(Istio/Linkerd), IaC(Terraform/Pulumi)를 기반으로 **불변 인프라(Immutable Infrastructure)** 위에 **Cloud Native 12-Factor + Beyond 12-Factor** 원칙을 적용해 **탄력성(Elasticity)**, **관측 가능성(Observability)**, **자동 회복(Self-Healing)** 을 코드로 구현하는 엔지니어링 패러다임이다.
> 2. **가치**: 적절한 클라우드 아키텍처 적용 시 인프라 프로비저닝 시간 **주 단위 -> 수 분**, Auto-Scaling으로 평균 CPU 사용률 20~30% 유지, MTTR(Mean Time To Recovery) **수 시간 -> 수 분**(카오스 엔지니어링 + GitOps 기반 롤백), TCO는 3년 기준 CapEx 대비 OpEx 전환으로 약 30~50% 절감이 가능하다(워크로드 성격에 따라 차이).
> 3. **판단 포인트**: ① 단일 클라우드 종속(Vendor Lock-in) vs 멀티/하이브리드 ② 서버리스 우선(FaaS+API Gateway) vs 컨테이너 우선(EKS/GKE/AKS) ③ 동기 REST vs 비동기 이벤트 드리븐(EventBridge/Kafka) ④ 영구 스토리지 단일 리전 vs 액티브-액티브 멀티 리전 ⑤ IaC는 Terraform(멀티 클라우드) vs CDK/Pulumi(언어 친화) vs Crossplane(K8s 네이티브) — **워크로드 특성(상태/지연시간/규제)과 팀 역량(GitOps 친숙도)에 따라 정량적 비교 후 결정**해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 모놀리식 온프레미스 아키텍처는 수직 확장(Scale-Up) 한계, 프로비저닝 장기화(서버 도입 6~12주), 용량 계획의 불확실성(트래픽 피크 대비 과다 설계), 그리고 **Snowflake Server(수작업으로 운영되며 재현 불가한 서버)** 의 누적이라는 구조적 문제를 안고 있었다. 2006년 AWS S3/EC2 출시 이후 IaaS가, 2010년대 PaaS(Heroku, Cloud Foundry), 2014년 Kubernetes 1.0 출시, 2014년 AWS Lambda 출시로 FaaS/서버리스가 등장하며 **"인프라는 코드로 정의하고, 애플리케이션은 비즈니스 로직에만 집중"** 하는 클라우드 네이티브 패러다임이 정착했다. 기술사 시험에서는 단순히 "클라우드를 쓴다"가 아니라, **어떤 아키텍처 패턴을 어떤 근거로 선택하는지**, **장애·보안·비용·거버넌스를 어떻게 동시에 만족시키는지**를 묻는다.

```text
+----------------------------------------------------------------------+
|        Monolith On-Premise  vs  Cloud-Native Architecture            |
+----------------------------------------------------------------------+
|                                                                      |
|  [Legacy]                              [Cloud-Native]                |
|  +-----------------+                   +-----------------------+     |
|  |  Monolithic     |                   |  Microservices (40+)  |     |
|  |  WAR / EAR      |     ------►       |  Container (OCI)      |     |
|  |  + RDBMS        |    Cloud-Native   |  + Sidecar (Service   |     |
|  |  + WebSphere    |     Transform     |    Mesh / Dapr)       |     |
|  |  + 수작업 OS    |                   |  + API Gateway        |     |
|  |  + 수작업 HA    |                   |  + Event Bus (Kafka)  |     |
|  +-----------------+                   +-----------------------+     |
|  Scale-Up (수직)                       Scale-Out (수평, HPA/VPA/CA)  |
|  CapEx 중심                            OpEx 중심 (Pay-per-use)       |
|  변경 단위: 월/분기                    변경 단위: 분 (GitOps)        |
|  장애 전파: 폭포식(Cascading)          장애 격리: Bulkhead/Resilience4j|
|  배포: 수동/FTP/주말 작업             배포: ArgoCD/Argo Rollouts    |
|                                                                      |
+----------------------------------------------------------------------+
```

클라우드 아키텍처의 본질적 필요성은 세 가지다. ① **Business Agility**: 시장 변화에 따라 수 분 단위로 용량을 늘리고 줄일 수 있어야 한다(예: 블랙프라이데이 트래픽 평소 대비 10배). ② **Operability at Scale**: 수백~수천 개의 마이크로서비스를 사람이 직접 관리할 수 없으므로, **Self-Healing + Observability + Automation**이 필수다. ③ **Global Reach + Compliance**: GDPR(데이터 주권), PCI-DSS, K-ISMS-P 등 규제 준수와 동시에 전 세계 저지연 서비스를 위해 리전/엣지 분산이 필요하다.

- **📢 섹션 요약 비유**: 모놀리식 온프레미스는 **한 채의 아파트에 수도·전기·난방을 각 세대가 따로 관리**하는 것이고, 클라우드 네이티브는 **모든 인프라가 미리 갖춰진 스마트 오피스텔에 입주해서 핵심 업무(앱 개발)만 하는 것**이다. 입주·퇴거·확장이 컨테이너 단위로 즉시 가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 네이티브 아키텍처는 크게 **① 인프라 계층(Foundation)**, **② 런타임/오케스트레이션 계층**, **③ 애플리케이션/플랫폼 계층**, **④ 운영/관측 계층**의 4계층으로 구성된다. CNCF(Cloud Native Computing Foundation)의 Cloud Native Trail Map이 이를 가장 잘 표현한다.

```text
                          +-------------------------------------+
                          |   10. Observability & Analysis      |
                          |   (Prometheus + Grafana + Loki +    |
                          |    Tempo + OpenTelemetry)           |
                          +--------------+----------------------+
                                         |
  +------------------+    +--------------v----------------------+
  | 7. Service Mesh  |◄---+  9. Database / Stateful Service    |
  |  (Istio/Linkerd) |    |  (CloudNativePG, Cassandra,         |
  +------+-----------+    |   ScyllaDB, Rook-Ceph, Redis)        |
         |                +--------------^----------------------+
  +------v-----------+                   |
  | 6. API Gateway   |    +--------------+----------------------+
  | (Kong/Apigee/    |    |  8. Storage / Distributed Lock      |
  |  AWS API GW)     |    |  (S3 / MinIO / etcd / ZooKeeper)     |
  +------+-----------+    +-------------------------------------+
         |
  +------v-----------+    +-------------------------------------+
  | 5. App Definition |---►|  4. CI / CD (GitOps)                |
  |  (Helm/Kustomize |    |  (Tekton / ArgoCD / FluxCD /       |
  |   / Carvel)      |    |   Spinnaker)                         |
  +------+-----------+    +--------------+----------------------+
         |                               |
  +------v-------------------------------v----------------------+
  |  3. Orchestration & Scheduling: Kubernetes (EKS/AKS/GKE/   |
  |     Self-managed) — Control Plane + Worker Node + CRI/CNI/CSI|
  +-------------------------------+------------------------------+
                                  |
  +-------------------------------v------------------------------+
  |  2. Container Runtime: containerd / CRI-O + OCI Image      |
  |     (BuildKit, Buildpacks, Ko, Jib)                         |
  +-------------------------------+------------------------------+
                                  |
  +-------------------------------v------------------------------+
  |  1. Provisioning: IaC (Terraform / Pulumi / Crossplane) +   |
  |     Image (Packer / Golden AMI) + Secrets (Vault / ESO)     |
  +-------------------------------------------------------------+
```

| 계층 | 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- | :--- |
| **① IaC / Provisioning** | Terraform, Pulumi, Crossplane, AWS CDK | 클라우드 리소스를 선언적으로 정의·버전관리·재현 | HCL/TypeScript 기반 선언형, `plan -> apply` 2단계로 변경 사항 사전 검토, **State Lock**(DynamoDB/S3 Backend)으로 동시성 제어, OPA/Conftest로 정책 검증(Policy as Code) |
| **② Container Runtime** | containerd, CRI-O, BuildKit, Kaniko | 컨테이너 이미지 빌드·실행·OCI 표준 준수 | OCI Image Spec v1.1, Multi-arch Build(amd64/arm64), Distroless/Chainguard Image로 공격면(Attack Surface) 축소, SBOM(CycloneDX/SPDX) 생성 |
| **③ Orchestration** | Kubernetes 1.30+ (EKS/AKS/GKE/OpenShift/Rancher) | 컨테이너 스케줄링·자가 치유·롤링 업데이트 | 선언형 YAML + Reconciliation Loop(현재 상태->원하는 상태), HPA(CPU/Mem/Custom Metric), VPA(리소스 권장), KEDA(이벤트 기반 스케일링 0->N), Karpenter(노드 자동 프로비저닝, Spot 인스턴스 혼합) |
| **④ App Definition & Delivery** | Helm 3, Kustomize, ArgoCD, FluxCD, Argo Rollouts, Keptn | K8s 리소스 패키징 + GitOps 지속 배포 | Git을 Single Source of Truth로 사용, **ArgoCD Application Controller**가 Git과 클러스터 상태를 주기적(3분) Sync, **Progressive Delivery**(Canary/Blue-Green) via Argo Rollouts + Istio 트래픽 분기(2%->10%->50%->100%) + Prometheus 지표 기반 자동 승격/롤백(Flagger) |
| **⑤ API Gateway & Service Mesh** | Kong, Apigee, AWS API Gateway, Istio, Linkerd, Cilium Service Mesh | L7 라우팅·인증·RateLimit·mTLS·트래픽 관리 | Istio Control Plane(Istiod) + Data Plane(Envoy Sidecar), **SMI(Specification Mesh Interface)**, eBPF 기반 Cilium은 Sidecar 없이 커널 레벨에서 처리(Overhead 0.5ms 이하), Ambient Mesh(ztunnel + Waypoint) |
| **⑥ Observability** | Prometheus + Grafana + Loki + Tempo + OpenTelemetry + Datadog/New Relic | 메트릭·로그·트레이스 통합 수집 및 SLO 관측 | **3 Pillars**: Metrics(PromQL, Prom 2.0 TSDB), Logs(Loki, LogQL, 라벨 인덱싱), Traces(OpenTelemetry SDK -> Tempo/Jaeger), **USE Method**(Utilization/Saturation/Errors), **RED Method**(Rate/Errors/Duration), SRE의 SLI/SLO/Error Budget |
| **⑦ Security** | Trivy, Snyk, OPA/Gatekeeper, Kyverno, Falco, cert-manager, Vault | 이미지 스캔·정책 준수·런타임 위협 탐지 | SBOM + CVE 매칭, **Admission Controller**로 K8s API 호출 시 정책 강제(예: `privileged: false` 강제), eBPF 기반 Falco로 비정상 syscall 탐지, SPIFFE/SPIRE로 워크로드 ID 발급, **Zero Trust**(mTLS 기본) |
| **⑧ 데이터/Stateful** | CloudNativePG, Rook-Ceph, Cassandra, ScyllaDB, Redis Cluster, Kafka (Strimzi) | K8s 네이티브 운영으로 Stateful 워크로드 통합 | Operator Pattern으로 CRD(Custom Resource Definition) 기반 도메인 지식 내장, **PetSet -> StatefulSet**, PVC 동적 프로비저닝(CSI Driver), Kafka는 KRaft 모드(ZooKeeper 의존 제거, 3.3+) |

### Cloud Native 핵심 원리 3가지

1. **선언형(Declarative) + Reconciliation Loop**: "어떻게(How)" 가 아니라 "무엇을(What)" 정의하면 컨트롤러가 끊임없이 현재 상태를 관찰하고 원하는 상태로 수렴시킨다. K8s Controller-Runtime 패턴이 모든 Operator의 근간이다.
2. **불변 인프라(Immutable Infrastructure)**: 운영 중 패치·수정하지 않고, **새 이미지를 빌드 -> 기존 인스턴스 교체**한다. 이로써 Snowflake Server가 사라지고, 모든 서버가 Git Commit과 1:1 매핑되어 롤백/감사가 가능해진다. **Borg/Immutable Server -> Phoenix Server -> Cattle vs Pets** 진화 흐름.
3. **12-Factor + Beyond 12-Factor**: Codebase(1), Dependencies(2), Config(3), Backing Services(4), Build/Release/Run(5), Processes(6), Port Binding(7), Concurrency(8), Disposability(9), Dev/Prod Parity(10), Logs(11), Admin Processes(12). Beyond 12-Factor는 **Telemetry, Security, Resilience(회로차단기·Fallback), API First**를 추가한다.

- **📢 섹션 요약 비유**: 클라우드 네이티브는 **레고 블록**과 같다. 컨테이너(블록) + K8s(블록 결합 규칙) + GitOps(블록 배치 도면) + Observability(블록 상태 모니터)를 조합하면 어떤 모양(아키텍처)도 만들 수 있고, 한 블록이 부서져도 다른 블록으로 즉시 교체된다.

---

## Ⅲ. 비교 및 연결

### 1. 컴퓨트 실행 모델 비교

| 구분 | IaaS (EC2/Compute Engine) | PaaS (Beanstalk/Cloud Run/App Engine) | CaaS (EKS/AKS/GKE) | FaaS (Lambda/Cloud Functions) |
| :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | App + Runtime + OS + Middleware + VM | App + Config | App + Container Image | 함수 코드(Handler)만 |
| **Cold Start** | 없음(상시) | 1~5초 | 수 초(Karpenter 시 30초 이내) | 100ms~수 초(Provisioned Concurrency로 0에 수렴) |
| **실행 단위 최대 시간** | 무제한 | 제한적(웹 요청 60초 등) | 무제한 | **15분(Lambda) 한도** |
| **비용 단위** | 인스턴스 시간(秒) | 인스턴스 시간 | Pod 시간 | **GB-초 + 호출 수**(0일 때 0원) |
| **확장 모델** | 수동/Auto Scaling Group | 트래픽 기반 자동 | HPA/VPA/KEDA(0->1000) | **Concurrency 1~1000 자동** |
| **적합 워크로드** | 레거시, 커스텀 커널, GPU 특수 | 웹앱, API 단순 배포 | MSA, Stateful, 복잡한 오케스트레이션 | **이벤트 드리븐, 간헐적, ETL, Webhook, Cron** |
| **Vendor Lock-in** | 중간(AMI/이미지) | 높음(플랫폼 종속) | 낮음(K8s API 표준) | 매우 높음(벤더별 트리거·런타임 종속) |

### 2. 배포 전략(Deployment Strategy) 비교

| 전략 | 가용성 영향 |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 699 / 800

<- **이전**: [698. 클라우드 아키텍처 핵심 토픽 698번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/698_cloud_architecture_core_topic_698_exam_summar/)
**다음**: [700. 클라우드 아키텍처 핵심 토픽 700번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/700_cloud_architecture_core_topic_700_exam_summar/) ->

---
