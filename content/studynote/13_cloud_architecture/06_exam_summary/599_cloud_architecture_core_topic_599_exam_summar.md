---
title: "599. 클라우드 아키텍처 핵심 토픽 599번 시험 요약 (Cloud Architecture Core Topic 599 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST SP 800-145의 4가지 배포 모델(Public/Private/Hybrid/Community)과 3(+2)가지 서비스 모델(IaaS/PaaS/SaaS + FaaS/CaaS)을 기반으로, **가상화 -> 컨테이너화 -> 오케스트레이션 -> 관측가능성(Observability)**의 4계층을 결합해 **탄력성(Elasticity)·복원력(Resilience)·무중단 배포(Zero-Downtime)**를 보장하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: CapEx->OpEx 전환으로 초기 인프라 투자 70~90% 절감, Auto Scaling으로 피크 트래픽 10배 변동 대응, 멀티 리전 Active-Active 구성으로 SLA **99.99%(연 52.6분 이내 장애)**, GitOps + CI/CD 파이프라인으로 배포 리드타임을 주 단위->분 단위로 80% 단축, 글로벌 엣지(CloudFront/Cloud CDN)로 평균 TTFB 200ms->30ms 개선.
> 3. **판단 포인트**: ①가용성 vs 비용 trade-off(멀티 리전 +6~12% vs 단일 리전), ②CAP Theorem(Strong Consistency vs Eventual Consistency), ③Stateless vs Stateful 워크로드 분리, ④Egress 트래픽 비용($0.02~0.09/GB)이 Latency 개선보다 클 경우 CDN·S3 Same-Region 활용, ⑤EKS/Karpenter(FinOps) 선택으로 노드당 40% 비용 절감 가능.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 3-Tier 아키텍처(웹/앱/DB)는 정적 용량 계획(Static Capacity Planning)에 의존하여 평균 서버 유휴율 30~70%, 트래픽 피크 시 다운타임, HW 수명주기 3~5년 강제 교체, DR(Disaster Recovery) 사이트 별도 운영 등의 비효율을 야기한다. 4차 산업혁명 시대의 AI·빅데이터·IoT 워크로드는 GPU/TPU 같은 특수 자원의 탄력적 공급을 요구하며, B2C 서비스는 **Black Friday·드라마 동시시청(Daum 툰·YouTube 프리미어)·정부 재난 알림(재난문자)** 같은 100배 트래픽 스파이크를 수 초 내에 흡수해야 한다.

클라우드 아키텍처는 **가상화(Hypervisor -> Container -> Unikernel)** 기술 발전과 **SDN(Software Defined Networking)**, **분산 코디네이션(ZooKeeper/etcd/Consensus)**, **선언적 API(Declarative API, K8s Manifest)**의 결합으로 "필요할 때, 필요한 만큼, 필요한 곳에서" 자원을 프로비저닝하는 모델을 가능케 했다. Gartner(2024) 보고에 따르면 글로벌 클라우드 시장 규모는 약 $679B이며, 신규 디지털 워크로드의 70% 이상이 클라우드 네이티브로 설계된다.

```text
        +--------------------------------------------------------------+
        |           Cloud Migration & Adoption Framework               |
        +--------------------------------------------------------------+

   [현재 상태 진단]          [비즈니스 동기]           [기술적 제약]
   +--------------+        +--------------+        +--------------+
   |  5R 전략     |        |  Agility     |        |  Legacy DB   |
   |  (Rehost~    |<-------->|  Innovation  |<-------->|  Mainframe   |
   |   Retire)    |        |  Cost Opt.   |        |  Compliance  |
   +------+-------+        +------+-------+        +------+-------+
          |                       |                       |
          +---------------+-------+-----------------------+
                          v
   +--------------------------------------------------------------+
   |        6단계 클라우드 도입 성숙도 모델 (Cloud Maturity)       |
   |                                                              |
   |  L1: Consolidation --> L2: Migration --> L3: Validation         |
   |  L4: Innovation  --> L5: Optimization --> L6: Transformation  |
   +--------------------------------------------------------------+
                          |
        +-----------------+-----------------+
        v                 v                 v
   [Public Cloud]   [Private Cloud]   [Hybrid/Multi]
   (AWS/Azure/GCP)  (OpenStack,      (EKS Anywhere,
                     Tanzu,        Anthos, Outposts)
                     on-prem K8s)
```

**과거(On-Premise) vs 신규(Cloud-Native) 패러다임 비교**

| 차원 | On-Premise (수직 확장) | Cloud-Native (수평 확장) |
|---|---|---|
| 자원 할당 | 정적, 수개월 예측 | 동적, 실시간 Auto Scaling |
| 장애 대응 | HA Pair, Cold DR | Multi-AZ, Self-Healing |
| 배포 | 분기별, 수동 릴리즈 | 주간/일간, GitOps |
| 모니터링 | SNMP, 로그 파일 | OpenTelemetry, 3-pillar(Logs/Metrics/Traces) |
| 비용 | CapEx 감가상각 | OpEx Pay-as-you-go |
| 팀 구조 | Sysadmin 분리 | SRE/DevOps 일체형 |

- **📢 섹션 요약 비유**: 클라우드는 마치 **전력 그리드(電力網)**와 같다. 각 가정·공장이 자체 발전소를 짓지 않고도 필요할 때 전기를 끌어다 쓰는 것처럼, 더 이상 기업이 자체 데이터센터를 짓지 않고도 컴퓨팅 자원을 콘센트처럼 활용한다. 다만, **누진 요금제**처럼 Egress·API 호출 같은 사용량이 비용을 결정한다는 점에서 **미터기를 확인하는 것(FinOps)**이 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 크게 **① 인프라(Infra) ② 플랫폼(Platform) ③ 애플리케이션(App) ④ 운영(Ops/관측가능성)**의 4개 레이어와 **⑤ 거버넌스(Security/Compliance)** 레이어로 구성된다. 각 레이어는 단방향이 아니라 양방향(예: HPA가 Metric Server를 참조)으로 데이터를 교환한다.

```text
           +------------------------------------------------------------+
           |    5-Layer Cloud-Native Reference Architecture              |
           +------------------------------------------------------------+

  +---------------------------------------------------------------------+
  |  L5. Governance & Security (거버넌스/보안)                            |
  |  +----------+ +----------+ +----------+ +----------+ +----------+    |
  |  | IAM /   | | KMS /    | | CSPM/    | | SIEM/    | | Audit    |    |
  |  | SSO(OIDC)| | HSM/Vault| | PrismaCl.| | Splunk   | | (CloudTr.)|   |
  |  +----------+ +----------+ +----------+ +----------+ +----------+    |
  +--------------------------+------------------------------------------+
                             |
  +--------------------------+------------------------------------------+
  |  L4. Observability & SRE (관측가능성)                                 |
  |  +------------------+ +------------------+ +------------------+     |
  |  | Metrics          | | Logs             | | Traces           |     |
  |  | (Prometheus,     | | (Loki,           | | (Jaeger,         |     |
  |  |  CloudWatch)     | |  CloudWatch, ELK)| |  Zipkin, X-Ray)  |     |
  |  +------------------+ +------------------+ +------------------+     |
  |  OpenTelemetry SDK  ->  OTel Collector  ->  Grafana / Datadog         |
  +--------------------------+------------------------------------------+
                             |
  +--------------------------+------------------------------------------+
  |  L3. Application & Data Platform (애플리케이션/데이터)                 |
  |  +----------------+ +----------------+ +----------------+           |
  |  | MSA / BFF /    | | Serverless     | | Streaming      |           |
  |  | Sidecar(Istio) | | (Lambda, Knative| | (Kafka, Kinesis|           |
  |  |                | |  Cloud Run)    | |  Pub/Sub)      |           |
  |  +----------------+ +----------------+ +----------------+           |
  |  +---------------------------------------------------------+        |
  |  |  DB: RDS/Aurora(MySQL/PG), DynamoDB, Redis, MongoDB Atlas|        |
  |  |  Cache: CloudFront, ElastiCache, Memorystore            |        |
  |  +---------------------------------------------------------+        |
  +--------------------------+------------------------------------------+
                             |
  +--------------------------+------------------------------------------+
  |  L2. Container & Orchestration Platform (컨테이너/오케스트레이션)      |
  |  +----------------------------------------------------------+       |
  |  |  Kubernetes (EKS/GKE/AKS/OKE/ROS)                        |       |
  |  |  +- Control Plane: API Server, etcd, Scheduler, CCM     |       |
  |  |  +- Data Plane: kubelet, kube-proxy, container runtime  |       |
  |  |  Operator Pattern, Helm Chart, Kustomize                |       |
  |  |  Service Mesh: Istio / Linkerd / Consul                  |       |
  |  |  GitOps: ArgoCD / Flux                                   |       |
  |  +----------------------------------------------------------+       |
  +--------------------------+------------------------------------------+
                             |
  +--------------------------+------------------------------------------+
  |  L1. Infrastructure (인프라)                                          |
  |  +----------+ +----------+ +----------+ +----------+ +----------+   |
  |  | Compute  | | Storage  | | Network  | | DB       | | Edge     |   |
  |  | EC2/EKS  | | S3/EBS/  | | VPC/ALB/ | | Aurora/  | | CDN/     |   |
  |  | Node Gp. | | EFS/FSx  | | TGW/Priv.| | DynamoDB | | CloudFront|  |
  |  +----------+ +----------+ +----------+ +----------+ +----------+   |
  |  IaC: Terraform / Pulumi / CDK / Crossplane                         |
  +---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway / Ingress** | 외부 트래픽 진입점, 라우팅, 인증, 속도 제한(Rate Limit) | AWS API Gateway(초당 10K RPS), Kong(Envoy 기반), Nginx Ingress(쿠버네티스 표준). **OWASP API Top 10**(BOLA, BOPLA) 방어 로직 포함 |
| **Service Mesh** | 서비스 간 mTLS(상호 TLS), L7 로드밸런싱, 카나리/블루-그린, 관측 트래픽 | Istio(Envoy 사이드카, Istiod 컨트롤 플레인), Linkerd(Buoyant Rust 프록시, 50% 적은 메모리), Consul Connect. **Sidecar Pattern**으로 비즈니스 로직과 인프라 관심사 분리 |
| **Container Orchestrator (K8s)** | 선언적 상태 관리, 스케줄링, 자가 치유(Self-Healing) | **K8s API Server**(etcd Raft 합의, R&W 시 linearizable), **kube-scheduler**(bin-packing/least-allocated/balanced), **Karpenter**(K8s 1.27+, spot
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 599 / 800

<- **이전**: [598. 클라우드 아키텍처 핵심 토픽 598번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/598_cloud_architecture_core_topic_598_exam_summar/)
**다음**: [600. 클라우드 아키텍처 핵심 토픽 600번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/600_cloud_architecture_core_topic_600_exam_summar/) ->

---
