---
title: "698. 클라우드 아키텍처 핵심 토픽 698번 시험 요약 (Cloud Architecture Core Topic 698 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS·PaaS·SaaS·FaaS·CaaS 계층 위에 Well-Architected 5대 원칙(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화)과 6R 마이그레이션 전략을 결합하여 워크로드의 이식성, 탄력성, 자동 복구력을 달성하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: CapEx->OpEx 전환으로 초기 인프라 투자 약 60~70% 절감, Auto Scaling으로 평균 자원利用率 30~45% 향상, Multi-AZ/Region 구성으로 RTO 분 단위·RPO 0~수 초 달성, FinOps 적용 시 클라우드 지출 20~35% 회수 가능하다.
> 3. **판단 포인트**: Single Cloud vs. Multi/Hybrid Cloud의 Lock-in·데이터 중력·네트워크 latency·컴플라이언스 거주성(데이터 주권) 트레이드오프, Stateful 워크로드의 무중단 마이그레이션(DB CDC, dual-write, traffic shifting) 전략, Egress 비용과 백본 라우팅 설계가 핵심 의사결정 분기점이다.

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스 3-tier 아키텍처는 CapEx 중심의 용량 계획(Capacity Planning), 수직 확장(Scale-Up)의 한계, Disaster Recovery 구성의 고비용(DR Site CapEx 약 40~60%), 그리고 트래픽 피크 대비 과잉 프로비저닝(평균 활용도 15~25%)이라는 구조적 비효율을 내포하고 있다. 698번 토픽은 이러한 문제를 해결하기 위해 **클라우드 네이티브 아키텍처(Cloud-Native Architecture)** 가 가져오는 핵심 기법—탄력적 자원 풀링, 선언적 API(Declarative API), 불변 인프라(Immutable Infrastructure), GitOps 기반 지속적 배포—를 엔터프라이즈 환경에 안전하게 정착시키기 위한 설계·운영·거버넌스 역량을 평가한다.

```text
+--------------------------------------------------------------------------+
|        Enterprise Cloud Architecture Reference Model (Layered)          |
|                                                                          |
|  +--------------------------------------------------------------------+  |
|  |  L7  Governance & FinOps : CCoE, Tag Policy, Budget Alarm, RI/SP   |  |
|  +--------------------------------------------------------------------+  |
|  |  L6  Security & Compliance: IAM, KMS, WAF, CSPM, SIEM, Audit Trail|  |
|  +--------------------------------------------------------------------+  |
|  |  L5  Observability   : Prometheus, Grafana, OpenTelemetry, X-Ray   |  |
|  +--------------------------------------------------------------------+  |
|  |  L4  Application     : MSA, Serverless, Event-Driven, Saga, DDD   |  |
|  +--------------------------------------------------------------------+  |
|  |  L3  Data Platform   : OLTP RDS, NoSQL, Data Lake, Lakehouse, CDC |  |
|  +--------------------------------------------------------------------+  |
|  |  L2  Runtime         : Kubernetes(EKS/AKS/GKE), ECS, Istio, Envoy |  |
|  +--------------------------------------------------------------------+  |
|  |  L1  Infrastructure  : IaaS(EC2/VM), Bare-Metal, Edge, 5G MEC      |  |
|  +--------------------------------------------------------------------+  |
+--------------------------------------------------------------------------+
           ^                      ^                       ^
           |                      |                       |
     Public Cloud          Private Cloud           Hybrid/Multi-Cloud
   (AWS, Azure, GCP)    (On-Prem, Outposts)    (Anthos, Arc, ARO)
```

기존 온프레미스는 **고정 용량 + 수동 변경** 패러다임이었다면, 클라우드 아키텍처는 **API 기반 프로비저닝 + 선언적 상태 + 정책 자동화** 패러다임이다. CNCF(Cloud Native Computing Foundation)의 정의에 따르면 클라우드 네이티브는 컨테이너·서비스 메시·마이크로서비스·불변 인프라·선언형 API로 구성되며, 이를 뒷받침하는 OSS 생태계(Kubernetes, Istio, ArgoCD, Prometheus)가 사실상 표준이다.

- **📢 섹션 요약 비유**: 온프레미스는 자가용을 사서 관리하는 것이고, 클라우드 아키텍처는 수요에 따라 택시·버스·기차·비행기를 클릭 한 번으로 환승하는 **MaaS(Mobility as a Service)** 와 같다. 다만 요금 정산·안전벨트(보안)·교통카드 연동(IAM) 같은 운영 체계가 전제되어야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **제어 루프(Control Loop)** 와 **불변 인프라(Immutable Infrastructure)** 의 결합이다. Kubernetes의 `Desired State -> Actual State` 수렴, Auto Scaling Group의 CloudWatch -> Launch Template 갱신, Terraform의 `plan/apply` 리컨실(Reconciliation) 모두 동일하게 “선언 -> 감지 -> 보정”의 폐루프 구조를 갖는다.

```text
        +-------------------------------------------------------------+
        |           Cloud-Native Request & Control Flow              |
        +-------------------------------------------------------------+

   [User] --(HTTPS)--> [CloudFront/CDN/ALB] --> [WAF: OWASP Top 10]
                                              |
                                              v
                                    +--------------------+
                                    |  API Gateway       |  (Throttle, Auth)
                                    |  + Service Mesh    |  (mTLS, Retry)
                                    +---------+----------+
                                              |
                          +-------------------+-------------------+
                          v                   v                   v
                   +-------------+     +-------------+     +-------------+
                   | Pod/MSA-A   |     | Pod/MSA-B   |     | Lambda/Func  |
                   | (Stateless) |     | (Stateful)  |     | (Event-Driven)|
                   +------+------+     +------+------+     +------+------+
                          |                   |                   |
                          v                   v                   v
                    [RDS Proxy]          [ElastiCache]       [DynamoDB DAX]
                          |                   |                   |
                          +----------+--------+-----------+-------+
                                     v                    v
                              [Amazon Aurora]      [S3+Glacier]
                              (Multi-AZ, R/W)      (Object Storage)

   -------------  Cross-cutting Concerns (Sidecar Pattern)  -------------
   -> Secret Manager -> Vault -> CSI Driver KMS Encryption
   -> OpenTelemetry Collector (Trace/Metric/Log)
   -> Istio Envoy (L7 Routing, Circuit Breaker, Fault Injection)
   -> Falco / Trivy (Runtime Security, Image Scan)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Control Plane** | 클러스터/리소스 상태 관리 및 선언적 API 처리 | Kubernetes API Server (etcd Raft 합의), AWS Control Tower(Landing Zone), Terraform Cloud(Sentinel Policy as Code) |
| **Data Plane** | 실제 워크로드 실행 및 트래픽 처리 | kubelet(CRI/OPI), CNI(Calico/Cilium eBPF), gRPC/Envoy, GPU/DPU 가속, Nitro Enclave/TEE |
| **Service Mesh** | L7 트래픽 관리, mTLS, 관측성 | Istio/Linkerd (Sidecar/Ambient), OpenTelemetry Collector, WASM 필터, SPIFFE/SPIRE ID |
| **Resilience Layer** | 자동 복구, 서킷 브레이커, 재시도·백오프 | HPA/VPA/Cluster Autoscaler(KEDA 이벤트 기반), Karpenter(Just-in-Time 노드 프로비저닝), Resilience4j, Polly |
| **Data & State** | 트랜잭션·분석·스트리밍 데이터 계층 | Multi-AZ RDS/Aurora, DynamoDB Global Tables(Multi-Region Active-Active), Kafka/MSK, Lakehouse(Iceberg/Delta/Hudi) |
| **Edge & Delivery** | 글로벌 라우팅·캐싱·이미지 최적화 | CloudFront/Cloudflare/Fastly, Lambda@Edge/Cloudflare Workers, Image Optimizer, Signed URL/cookie |

핵심 알고리즘·파라미터: Auto Scaling은 **Target Tracking (예: CPU 60%) / Step Scaling / Scheduled / Predictive Scaling** 의 4가지 정책을 조합하며, Karpenter는 Bin-Packing 알고리즘으로 노드 단위 비용을 20~40% 절감한다. 데이터베이스 무중단 전환 시 **CDC(Change Data Capture) Lag**가 RPO를 결정하며, 일반적으로 0.5~3초 이내로 유지된다. 회로차단기 임계값은 일반적으로 **연속 실패 5~20회 -> 30~60초 OPEN -> Half-Open 1~3회** 로 설정한다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **항공 관제 시스템**과 같다. 탑승객(요청)은 관제탑(API Gateway/Service Mesh)의 안내를 받고 활주로(Control Plane)에서 이륙(스케줄링)하며, 비상시에는 다른 공항(Multi-AZ/Region)으로 자동 회항(자동 페일오버)한다. 중요한 건 “비행기 자체(불변 AMI/Container Image)”를 매번 새로 만들어서 검증된 형태로만 띄우는 점이다.

---

## Ⅲ. 비교 및 연결

| 구분 | Monolithic On-Prem | IaaS Lift-and-Shift (Rehost) | Cloud-Native Refactor (MSA+Container+Serverless) |
| :--- | :--- | :--- | :--- |
| **확장 모델** | Scale-Up (수직) | Scale-Out (수평, ASG) | Auto-Scale + Event-Driven Elastic |
| **배포 주기** | 월 1~4회 (수동) | 주 1~수 회 (CI/CD 일부) | 일 수십~수천 회 (GitOps, Progressive Delivery) |
| **장애 도메인** | 서버 단위 (단일 장애점 多) | AZ 단위 (Multi-AZ 가능) | Pod/Service 단위 (Chaos Engineering) |
| **총소유비용(TCO)** | CapEx 100% (5~7년 감가) | CapEx 30% + OpEx 70% | OpEx 90% 이상, Pay-per-Use |
| **기술 스택 예** | WebLogic+Oracle+SAN | EC2 + RDS + ALB | EKS+Istio+Lambda+DynamoDB+EventBridge |
| **적합 워크로드** | 레거시·규제 산업 (금융 코어) | 초기 마이그레이션·테스트 | 신규 디지털 서비스·트래픽 변동성 큰 서비스 |

```text
   6R Migration Strategy Decision Tree (AWS Prescribed)
   --------------------------------------------------

                         [기존 워크로드]
                               |
                +--------------+--------------+
                |  ROI/Payback 분석 (TCO 3Y)  |
                +--------------+--------------+
                               |
        +----------+-----------+-----------+----------+
        v          v           v           v          v
    Retire     Retain       Rehost     Relocate    Repurchase
   (EoL)    (보류/On-Prem)  (Lift)    (vMotion)   (SaaS 전환)
        |          |           |           |          |
        +----------+-----------+-----------+----------+
                               |
                               v
                       Refactor / Replatform
                  (MSA·Serverless·DB 엔진 교체)
```

**연계 기술 스택**: IaC(Terraform/Pulumi/CDK) -> CI/CD(GitHub Actions/Argo Workflows) -> Container Build(Buildpacks/Kaniko) -> Registry(ECR/Harbor) -> Orchestrator(EKS/AKS/GKE/OpenShift) -> Service Mesh(Istio/Linkerd) -> Observability(OTel + Prometheus + Loki + Tempo) -> FinOps(Kubecost, Vantage, CloudHealth).

- **📢 섹션 요약 비유**: 6R 마이그레이션은 **이사 전략**과 같다. 짐을 그대로 트럭에 싣는 게 Rehost(개미헛불이), 짐을 정리해서 최적의 박스에 다시 담는 게 Repackage(Replatform), 새 아파트 구조에 맞춰 인테리어까지 바꾸는 게 Refactor, 아예 새 가구를 사는 게 Repurchase(SaaS)다. 어느 집으로 이사할지(어느 CSP)는 신중히 결정해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

엔터프라이즈 클라우드 전환은 **Landing Zone -> Migration Factory -> Modernization -> FinOps -> Sovereignty** 의 5단계 로드맵으로 추진한다. 1단계 Landing Zone은 Account/VPC 분리, SCP(Service Control Policy), Centralized Logging, IAM Identity Center, Transit Gateway, Egress 제로트러스트 설계가 핵심이다. 2단계 Migration Factory는 Wave 기반(파일럿 -> 10% -> 50% -> 100%)으로 진행하며, 각 Wave는 Application Discovery(Ivanti/Cloudamize), Dependency Map, Performance Baseline, Cut-over Runbook, Roll-back Plan을 포함한다.

### 기술사형 판단 체크리스트

1. **데이터 주권/거버넌스**: 워크로드의 PII/PCI/PHI 보유 여부를 분류하고, 데이터 레지던시(예: 한국 리전 지정), 암호화 키 관리 방식(CMK/Hold Your Own Key), 그리고 클라우드 사업자의 컴플라이언스 인증(ISO 27001/27017/27018/27701, K-ISMS-P, CSAP) 충족 여부를 검증했는가?
2. **네트워크 토폴로지**: Hub-Spoke vs. Mesh, Direct Connect/ExpressRoute 회선 이중화(Active-Active BGP ECMP), Transit Gateway vs. VPC Peering 한도(Peering 125개/계정), Egress 비용 최적화(NAT Gateway -> VPC Endpoint -> S3 Gateway Endpoint 0원) 설계를 했는가?
3. **신뢰성 목표 정의**: RTO/RPO를 워크로드 티어(Tier 0/1/2/3)별로 설정하고, Multi-AZ(同城 HA) vs. Multi-Region(异地 DR) vs. Pilot Light vs. Warm Standby vs. Active-Active 중 어느 패턴을 채택할지 정량적으로 결정했는가?
4. **비용 거버넌스**: RI(Reserved Instance)/Savings Plans(Compute/SP) 1~3년 약정 비율, Spot 활용 가능 워크로드(Batch/Stateless) 분류, 데이터 티어링(Standard -> IA -> Glacier Instant/Deep Archive) 정책, 그리고 Cost Anomaly Detection + Budget Alarm 임계치(예: 120% 초과 알람)가 수립되어 있는가?
5. **관측성/보안 가드레일**: SLI/SLO/Error Budget을 정의하고, OpenTelemetry 기반 3-pillar(Trace/Metric/Log) 통합 수집, 런타임 보안(Falco/eBPF), IaC 정책 검사(Conftest/Checkov/Sentinel), 이미지 서명(Cosign/Sigstore) 및 SBOM 생성이 CI/CD 파이프라인에 포함되어 있는가?

### 피해야 할 안티패턴

- **Lift-and-Shift 후 방치(Rehost Anti-Pattern)**: 클라우드 IaaS에 그대로 올리고 Auto Scaling·Managed Service 활용 없이 EC2를 24/7 띄워두는 경우. TCO가 오히려 20~30% 증가할 수 있다.
- **Snowflake Account**: 환경별/팀별로 독립 계정을 생성하여 거버넌스·비용 통합이 불가능해지는 상태.
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 698 / 800

<- **이전**: [697. 클라우드 아키텍처 핵심 토픽 697번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/697_cloud_architecture_core_topic_697_exam_summar/)
**다음**: [699. 클라우드 아키텍처 핵심 토픽 699번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/699_cloud_architecture_core_topic_699_exam_summar/) ->

---
