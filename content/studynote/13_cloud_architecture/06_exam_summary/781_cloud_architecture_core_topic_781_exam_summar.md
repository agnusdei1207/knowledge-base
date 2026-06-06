---
title: "Cloud Architecture Core Topic 781 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS 4계층 서비스 모델과 Public/Private/Hybrid/Multi-Cloud 4가지 배치 모델을 기반으로, 컨테이너·서비스 메시·eBPF·분산 트레이싱을 결합해 "탄력성(Elasticity)·복원력(Resilience)·관측가능성(Observability)"의 세 축을 동시 만족시키는 시스템 설계 패러다임이다.
> 2. **가치**: Well-Architected Framework 6대 기둥(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속가능성)을 적용 시, 온프레미스 대비 **배포 주기 66% 단축**(DORA 2023), **MTTR 50% 감소**, **인프라 비용 30~40% 절감**(FinOps 기반) 효과를 달성할 수 있다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ① **추상화 수준**(고수준일수록 관리 편의 ^, 제어력·지연시간 v), ② **결합도 vs 배포 독립성**(모놀리식 -> 마이크로서비스 -> 서버리스로 갈수록 복잡도 ^, 장애격리 ^), ③ **일관성 vs 가용성**(CAP 정리 하에서 AP/CP 선택), ④ **보안 경계 위치**(주변부 vs Zero Trust 내부 마이크로세그먼테이션) 이다.

---

## Ⅰ. 개요 및 필요성

클라우드 아키텍처는 단순한 "IDC 외부 위탁"이 아니라, **API로 프로비저닝 가능한 컴퓨트·스토리지·네트워크 자원의 풀(Pool)** 위에서 비즈니스 요구사항(가용성 99.99% 이상, 트래픽 변동성 대응, 글로벌 사용자, TCO 절감)을 만족시키기 위한 **설계 원칙·패턴·거버넌스**의 총체다. 한국 클라우드 시장 규모는 2023년 약 8.4조 원으로, 공공·금융·제조·미디어 전 산업으로 확산되며, **클라우드 컴퓨팅 이용 촉진에 관한 법률**(2025.1 시행) 및 **CSAP(클라우드 보안 인증)** 의무화로 인해 아키텍처 설계 단계부터 컴플라이언스·데이터 주권·상호운용성을 내재화해야 한다.

기존 온프레미스 환경은 **수직 확장(Scale-Up)·예측 기반 용량 계획·장기 라이프사이클** 위주였으나, 클라우드에서는 **수평 확장(Scale-Out)·탄력적 프로비저닝·API 기반 선언적 인프라(IaC)** 로 전환되었다. 이로 인해 ① **Capacity Provisioning Lag**(용량 예측 오차로 인한 과잉/과소 투자), ② **Time-to-Market**(신규 인프라 도입에 평균 4~6주 소요), ③ **Disaster Recovery Gap**(DR 사이트 미비율 60% 이상) 한계가 해소된다.

```text
[ 온프레미스 vs 클라우드 아키텍처 패러다임 비교 ]

  +----------------------+                +----------------------+
  |   On-Premise         |                |   Cloud-Native       |
  |  +--------------+    |                |  +--------------+    |
  |  | Monolithic   |    |                |  | Microservice |    |
  |  | Application  |    |                |  | Mesh (Istio) |    |
  |  +------+-------+    |                |  +------+-------+    |
  |         |            |                |         |            |
  |  +------+-------+    |                |  +------+-------+    |
  |  | Hypervisor   |    |                |  | Kubernetes   |    |
  |  | (vSphere)    |    |   ---> MIGRATE |  | + Containerd |    |
  |  +------+-------+    |                |  +------+-------+    |
  |         |            |                |         |            |
  |  +------+-------+    |                |  +------+-------+    |
  |  | Bare-Metal   |    |                |  | Serverless   |    |
  |  | SAN Storage  |    |                |  | FaaS         |    |
  |  +--------------+    |                |  +--------------+    |
  |  Capacity: 고정        |                |  Capacity: 탄력적     |
  |  Provisioning: 수동    |                |  Provisioning: 자동    |
  +----------------------+                +----------------------+
```

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **전기 요금제**와 같다. 종전의 발전기 자가 운전(온프레미스)은 초기 투자비만 크고 효율이 낮지만, 그리드 전력(클라우드)은 쓴 만큼만 과금되고 수요 피크에 자동 대응한다. 그러나 어떤 요금제·계약 조건을 선택하느냐에 따라 비용이 10배까지 차이 난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **"선언적 인프라 + 마이크로서비스 + 관측가능성"** 의 결합이다. 아래 다이어그램은 12-Factor App + Cloud-Native + Well-Architected를 반영한 **표준 4계층 참조 아키텍처(Reference Architecture)** 이다.

```text
[ 클라우드 네이티브 4계층 아키텍처 (Kubernetes 기준) ]

  +-------------------------------------------------------------+
  |  Layer 1: Edge & Delivery                                    |
  |  +----------+  +----------+  +----------+  +----------+    |
  |  |   WAF    |-> | CloudFront|-> |   ALB    |-> |   APIM   |    |
  |  | (ModSec) |  | /Akamai  |  |  NLB     |  | (Kong)   |    |
  |  +----------+  +----------+  +----------+  +----------+    |
  |       | L7 DDoS |   TLS 1.3  |  mTLS via ACM  | OAuth2/JWT |
  +-------+---------+------------+---------------+-------------+
          |         |            |               |
  +-------v---------v------------v---------------v-------------+
  |  Layer 2: Application & Data Plane (Kubernetes Cluster)     |
  |  +------------------------------------------------------+  |
  |  |  Service Mesh: Istio / Linkerd / Cilium (eBPF)       |  |
  |  |  +----------+  +----------+  +----------+            |  |
  |  |  |  Pod A   |<-->|  Pod B   |<-->|  Pod C   |            |  |
  |  |  | Sidecar  |  | Sidecar  |  | Sidecar  |            |  |
  |  |  +-----+----+  +-----+----+  +-----+----+            |  |
  |  |  HPA: CPU 70% / KEDA: Kafka Lag / VPA: Memory        |  |
  |  +------------------------------------------------------+  |
  |  Workload: Deployment / StatefulSet / DaemonSet / Job/CronJob|
  +-------+-------------+-------------+---------------+--------+
          |             |             |               |
  +-------v-------------v-------------v---------------v--------+
  |  Layer 3: Data Plane                                         |
  |  +----------+  +----------+  +----------+  +----------+    |
  |  | RDBMS    |  | NoSQL    |  | Object   |  | Cache    |    |
  |  | (Aurora  |  | (DynamoDB|  | (S3, OSS)|  | (Redis   |    |
  |  |  Multi-AZ|  |  /Cass.) |  | Versioned|  |  Cluster)|    |
  |  +----------+  +----------+  +----------+  +----------+    |
  |  CDC: Debezium / Kafka Connect / DMS / Dataflow            |
  +-------+-------------+-------------+---------------+--------+
          |             |             |               |
  +-------v-------------v-------------v---------------v--------+
  |  Layer 4: Operations & Observability                         |
  |  +----------+  +----------+  +----------+  +----------+    |
  |  |Prometheus|  | Loki/ELK |  | Jaeger / |  | OpenTel. |    |
  |  | + Grafana|  | Logs     |  | Tempo    |  | Collector|    |
  |  +----------+  +----------+  +----------+  +----------+    |
  |  Policy: OPA/Gatekeeper  |  IaC: Terraform/Pulumi/ArgoCD   |
  |  Security: Falco/Trivy   |  FinOps: Kubecost/Vantage       |
  +-------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Edge & Delivery** | 글로벌 트래픽 라우팅, L7 보안, TLS 종료 | AWS CloudFront·Azure Front Door·Cloudflare는 Anycast 기반 엣지 POP 200+ 곳에서 TLS 1.3, HTTP/3(QUIC) 처리, WAF 룰(SQLi, XSS) 적용 |
| **Control Plane (K8s)** | 컨테이너 오케스트레이션, 선언적 상태 관리 | API Server(etcd 백엔드) ↔ Scheduler ↔ Controller Manager; `kubectl apply -f manifest.yaml`로 GitOps 동기화, Reconciliation Loop(현재->원하는 상태) |
| **Data Plane (Mesh)** | 서비스 간 통신, 트래픽 관리, mTLS | Envoy Sidecar가 L7 라우팅·Circuit Breaking(연결 실패 5회 시 30s open)·Retry(지수 백오프 100ms->1.6s)·Canary Release(가중치 5%->25%->50%->100%) 수행 |
| **Observability Stack** | 메트릭·로그·트레이스 통합 수집 | **3 Pillars**: Prometheus(메트릭, 15s scrape) + Loki/ELK(로그) + Jaeger/Tempo(트레이스, OpenTelemetry SDK로 W3C TraceContext 전파); RED(Req·Error·Duration)·USE(Util·Sat·Error) 메서드 |
| **Policy & IaC** | 거버넌스, 보안 정책 강제, 자동화 | OPA(Rego 언어)로 "모든 Pod는 resource.limits 필수", "허용 이미지 레지스트리 화이트리스트" 적용; ArgoCD/Flux로 Git-PR 기반 자동 동기화 |
| **Serverless/FaaS** | 이벤트 기반 stateless 함수 실행 | AWS Lambda/Azure Functions/GCP Cloud Run; 콜드 스타트 100~500ms 완화 위해 **Provisioned Concurrency**, **SnapStart**(Lambda) 활용 |
| **Multi-Cloud Abstraction** | 클라우드 종속성 제거 | Terraform(상태 파일, Plan/Apply 분리), Crossplane(K8s CRD 기반), Karpenter(노드 프로비저닝, 2분->15초 단축) |

**핵심 알고리즘 및 파라미터**:
- **Auto-Scaling**: HPA는 `desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]`로 30s마다 평가. KEDA는 Kafka Lag, SQS Queue Depth, Cron 등 이벤트 기반 0->N 스케일링. VPA는 과거 사용량 기반으로 requests/limits 자동 조정(권장 모드: `Off`로 두고 HPA와 충돌 회피).
- **Service Discovery**: K8s CoreDNS는 ClusterIP를 A 레코드로, Headless Service는 Pod IP를 직접 반환. K8s EndpointSlice는 100개 Pod 초과 시 자동 분할.
- **Consensus (etcd)**: Raft 알고리즘으로 Leader Election(election timeout 1s) + Log Replication(heartbeat 100ms); 쓰기 latency p99 < 10ms.
- **Eventual Consistency**: DynamoDB는 `Read/Write Capacity Unit`(1 WCU = 1KB/s 쓰기) 기반으로 파티션 키별 일관성 보장, Global Tables는 멀티리전 멀티마스터.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **현대 항공기의 플라이-바이-와이어(Fly-By-Wire)** 시스템과 같다. 기체(인프라) 자체는 비행사가 직접 컨트롤러로 제어하지 않고, 중간 제어 컴퓨터(API·오케스트레이터)가 센서 데이터(메트릭) 기반으로 명령을 자동 보정한다. 장애가 발생하면 제어 컴퓨터가 자동 복원한다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처를 학습할 때 혼동하기 쉬운 **유사·대안·선행 개념**을 명확히 구분해야 한다.

| 구분 | Monolithic | Microservice | Serverless (FaaS) |
| :--- | :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/EAR 또는 단일 컨테이너 | 서비스별 독립 컨테이너 (수십~수백 개) | 함수 단위 (수천 개) |
| **확장 단위** | 인스턴스 전체 복제 (수직+수평) | 서비스별 개별 HPA (수평) | 동시 실행 수(Concurrency) 기반 0~N |
| **장애 격리** | 프로세스 단위, 연쇄 장애 위험 | 프로세스 + Mesh Circuit Breaker | 함수 단위, 자동 격리 |
| **상태 관리** | Stateful (인메모리 세션 가능) | Stateless + 외부 저장소 (Redis, DB) | Stateless 강제 (실행 시간 15분 제한) |
| **적합 workload** | 단순 CRUD, 소규모 팀 (≤ 5명) | 복잡한 도메인, 다수 팀, 지속적 배포 | 이벤트 버스트, 비동기 작업, 간헐적 트래픽 |
| **Latency** | 호출 내(in-process), < 1ms | 네트워크 RPC/gRPC, 1~10ms | 콜드 스타트 100~500ms, 웜 시 5~20ms |
| **예시 기술** | Spring Boot fat JAR, Node.js Express | Spring Cloud, gRPC, Istio | Lambda, Azure Functions, Cloud Run |

**연계 기술**:
- **CI/CD**: Jenkins -> GitHub Actions -> Argo Workflows. 빌드 시간 10분 초과 시 원격 캐시(Bazel, sccache) 적용.
- **IaC**: Terraform(멀티 클라우드 선언형) ↔ Ansible(절차형 구성 관리) ↔ Pulumi(코드형 IaC, TypeScript/Python).
- **AIOps**: 이상 탐지(Prometheus + Thanos long-term), 로그 패턴 분석(Loki + ML), 알림 노이즈 제거(Alertmanager + grouping/inhibition).
- **보안**: CSPM(Cloud Security Posture Management)—Prowler·Sc
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 781 / 800

<- **이전**: [780. 클라우드 아키텍처 핵심 토픽 780번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/780_cloud_architecture_core_topic_780_exam_summar/)
**다음**: [782. 클라우드 아키텍처 핵심 토픽 782번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/782_cloud_architecture_core_topic_782_exam_summar/) ->

---
