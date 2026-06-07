---
title: "Cloud Architecture Core Topic 554 Exam Summary"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 가상화·컨테이너·오케스트레이션을 기반으로 **탄력적 자원 풀(Resource Pool)**을 API로 추상화하여, IaaS/PaaS/SaaS/FaaS 계층별로 **셀프서비스 프로비저닝**과 **종량 과금(Usage-based Metering)**을 가능하게 하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: CapEx -> OpEx 전환으로 초기 투자비를 약 **60~80% 절감**하고, Auto-Scaling을 통해 트래픽 변동 시 **5분 이내 수천 노드 확장**, 글로벌 리전 배포로 단일 장애점(SPOF) 제거 및 SLA **99.99%(52.6분/년 장애)** 달성이 가능하다.
> 3. **판단 포인트**: **벤더 락인(Lock-in)** vs 멀티클라우드 이식성, **보안 책임 분담 모델(Shared Responsibility)** 경계, **FinOps** 기반 비용 최적화, **Cold Start·Stateful 처리·네트워크 지연** 같은 서버리스 트레이드오프가 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

클라우드 아키텍처는 2006년 AWS S3·EC2 출시 이후, 단순 가상호스팅을 넘어 **분산 컴퓨팅·마이크로서비스·선언적 API**가 융합된 엔터프라이즈 인프라의 표준으로 자리 잡았다. 정보관리기술사 시험에서는 **클라우드 네이티브 12원칙(12-Factor App)**, **CSA(Cloud Security Alliance) STAR**, **NIST SP 800-145**, **한국 클라우드컴퓨팅법** 등 표준 프레임워크에 기반한 설계 능력이 평가된다.

기존 온프레미스 환경은 정적 용량 계획(Static Capacity Planning) 기반으로, 트래픽 피크 시 **과잉 투자**, 오프 피크 시 **자원 유휴**라는 양면의 비효율을 안고 있었다. 또한 IDC(Internet Data Center) 증설 시 수 개월의 Lead Time이 요구되어, **비즈니스 민첩성(Agility)** 확보가 근본적으로 제한되었다. 클라우드 아키텍처는 **Infrastructure as Code(IaC)**, **Immutable Infrastructure**, **API-First 설계**를 통해 이러한 한계를 해소한다.

```text
 +----------------------------------------------------------------------+
 |                  패러다임 전환: On-Premise -> Cloud Native            |
 +----------------------------------------------------------------------+

 [1단계: 물리 서버 시대 (1990~2000)]       [2단계: 가상화 시대 (2000~2010)]
 +------------------+                    +------------------+
 | App | App | App  |                    |   App | App      |
 |-----+-----+------|                    |---------------   |
 |  OS |  OS |  OS  |                    |       OS          |
 |-----+-----+------|                    |  Hypervisor (Xen, ESXi) |
 |   Hardware       |                    |---------------   |
 |  (고정 CAPEX)    |                    |   Virtual HW      |
 +------------------+                    |  (서버 통합비 4:1) |
                                         +------------------+
              |                                       |
              |                                       v
              |                          [3단계: 클라우드 네이티브 (2010~현재)]
              |                          +--------------------------------+
              +-------------------------->|  API Gateway / Service Mesh    |
                                         |  +---------+---------+------+ |
                                         |  |MicroSvc |MicroSvc |MicroSvc| |
                                         |  +----+----+----+----+----+---+ |
                                         |       v         v         v     |
                                         |  Container Orchestrator (K8s)   |
                                         |  +-- Auto-Scaling(HPA/VPA/CA)  |
                                         |  +-- Self-Healing & Rollout    |
                                         |  +-- Immutable Infra          |
                                         |  v                              |
                                         |  Multi-AZ / Multi-Region       |
                                         |  + S3 / Object Storage         |
                                         |  + RDS / DynamoDB (Distributed)|
                                         |  + CloudWatch/Prometheus       |
                                         +--------------------------------+
                                          ※ 선언적 API + IaC(Terraform/CDK)
                                          ※ 종량 과금(Per-Second Billing)
```

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"전기 요금제"**와 같다. 발전소(데이터센터)를 직접 짓는 대신, 콘센트에 꽂아 쓰는 만큼만 비용을 내는 구조. 사용량이 늘면 자동으로 전력 용량이 증설되고, 줄면 자동 차단되어 **유휴 낭비가 0에 수렴**한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **5계층 참조 모델**(논리적 구분)과 **C4 모델**(Context, Container, Component, Code)로 설계된다. 핵심은 **제어 평면(Control Plane)**과 **데이터 평면(Data Plane)**의 분리, **API-First 인터페이스**, **선언적 정책(Declarative Policy)**이다.

```text
   +---------------------------------------------------------------------+
   |              클라우드 네이티브 아키텍처 (Logical Reference Model)    |
   +---------------------------------------------------------------------+

   +-[1] Edge / CDN Layer (CloudFront, Cloudflare, Akamai)--------------+
   |   • DDoS Shield / WAF / TLS Termination / Cache Hit Ratio 95%+    |
   +--------------------------------+------------------------------------+
                                    v
   +-[2] API Gateway & BFF (Backend-For-Frontend) (Kong, AWS API GW) --+
   |   • 인증(OAuth2/OIDC) / 속도제한(Rate Limit) / 라우팅 / 변환        |
   |   • GraphQL Federation / Circuit Breaker Pattern                   |
   +--------------------------------+------------------------------------+
                                    v
   +-[3] Microservices Layer (Spring Boot / Node.js / Go)--------------+
   |   • Stateless Pods (12-Factor #1)                                  |
   |   • Service Discovery (Consul, Istio Service Mesh)                 |
   |   • 분산 추적 (OpenTelemetry / Jaeger)                             |
   +--------------------------------+------------------------------------+
                                    v
   +-[4] Container Orchestration (Kubernetes/EKS/AKS/GKE)--------------+
   |   +------------------------------------------------------------+  |
   |   |  Master/Control Plane (etcd, API Server, Scheduler,CM)    |  |
   |   +------------------------------------------------------------+  |
   |   +------------------------------------------------------------+  |
   |   |  Worker Nodes: kubelet + kube-proxy + Container Runtime    |  |
   |   |  • Pod: 최소 배포 단위 (1~N Containers, 공유 네트워크 ns)   |  |
   |   |  • Deployment(롤링 업데이트) / StatefulSet / DaemonSet     |  |
   |   +------------------------------------------------------------+  |
   |   • HPA: CPU 70% 임계치 기반 Pod Autoscaler (메트릭 기반 스케줄)  |
   |   • Karpenter: 리소스 부족 시 노드 자동 프로비저닝 (Spot 활용)   |
   +--------------------------------+------------------------------------+
                                    v
   +-[5] Managed Data & Serverless Backend-----------------------------+
   |   • OLTP: Aurora Global DB / Spanner / CockroachDB (RPO=0)       |
   |   • OLAP: Snowflake / BigQuery / Redshift (Columnar, Decoupling) |
   |   • Cache: ElastiCache Redis / Memcached (Read-Through, TTL)      |
   |   • Queue/Stream: Kafka(파티션 3,000+) / SQS FIFO / Kinesis      |
   |   • Object: S3 (11 9s Durability) / MinIO (S3 호환)              |
   |   • FaaS: Lambda (Cold Start 200~800ms), Cloud Functions          |
   +--------------------------------------------------------------------+
                    |
                    v
   +-[Cross-Cutting] Observability & Security (3 Pillars + 0-Trust)--+
   |   • Metrics: Prometheus + Grafana (SLO/Error Budget)              |
   |   • Logs: ELK / OpenSearch / Loki (구조화 로그 JSON)              |
   |   • Traces: OpenTelemetry -> Tempo/Jaeger (W3C TraceContext)      |
   |   • Security: IAM + KMS + Secrets Manager + SIEM + CSPM          |
   |   • IaC: Terraform / Pulumi (State Lock, Plan/Apply)              |
   +--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Control Plane (제어 평면)** | 클러스터 상태·정책·스케줄링 결정 | K8s API Server(8443/TLS) -> etcd(raft 합의 알고리즘) -> Scheduler(노드 필터링 후 점수화: LeastAllocated/Requested) -> Controller Manager(Desired State -> Actual State 조정) |
| **Data Plane (데이터 평면)** | 실제 워크로드 실행·트래픽 처리 | kubelet(PodSpec 수신 후 CRI 호출: containerd/CRI-O) -> kube-proxy(iptables/IPVS 모드로 Service ClusterIP DNAT) -> CNI 플러그인(Calico/Cilium eBPF, VPC Native CNI) |
| **Service Mesh** | 마이크로서비스 간 L7 트래픽 관리·mTLS·관찰 | Envoy Sidecar(1514/15001 포트) + Istio Control Plane -> mTLS 자동 발급(SPIFFE ID) -> 카나리 트래픽 분할(VirtualService weight 90:10) -> Fault Injection(지연 5초/오류 503 비율) |
| **Serverless / FaaS** | 이벤트 기반 stateless 코드 실행 | AWS Lambda: 동기 호출(API GW, 29MB 페이로드) vs 비동기 호출(SNS/SQS, 재시도 2회 + DLQ) -> 동시성 한도(기본 1,000) -> Provisioned Concurrency(예열)로 Cold Start 제거 |
| **Multi-Region Active-Active** | 글로벌 트래픽 부하분산·재해복구 | Route 53 Latency-Based Routing(헬스체크 30s 간격, 3회 실패 시 Failover) -> Aurora Global Database(Secondary Region RPO<1s) -> S3 Cross-Region Replication(SRTC 15분 내) |

**핵심 알고리즘·파라미터**:
- **리소스 스케줄링**: K8s Scheduler는 `LeastAllocated`(분산 우선) vs `MostAllocated`(집중·에너지 효율) vs `Requested`(예약량 기반) 점수 함수로 노드를 선택한다. Pod 스케줄링 시 **requests/limits**는 `QoS Class`를 결정(Guaranteed > Burstable > BestEffort)하며, OOM 시 Guaranteed Pod는 절대 킬되지 않는다.
- **Auto-Scaling 3종**: HPA(CPU/Mem 메트릭, 30초 주기 폴링), VPA(과거 사용량 회귀분석 기반 권장), Karpenter(노드 자체를 동적 프로비저닝, Spot 가격 90% 할인 활용).
- **합의 알고리즘**: etcd는 **Raft**(Leader 선출, 로그 복제, 2N+1 중 과반수 응답)로 분산 합의를 처리. Leader heartbeat 100ms, Election Timeout 1~2s.
- **일관성 모델**: DynamoDB는 **튜닝 가능 일관성**(Strong/Bounded Staleness/Session/Eventually Consistent) + **NWR 모델**(N=3, W=2, R=2 -> Quorum Read/Write)로 가용성·일관성 트레이드오프 제어.

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 핵심 메커니즘은 **"항공 관제탑(Control Plane)과 비행기(Data Plane)"** 관계와 같다. 관제탑은 이륙·착륙·경로만 결정하고, 실제 비행은 각 항공기가 자율적으로 수행한다. 만약 관제탑이 다운되어도 항공기는 **마지막 유효 상태(Last Known Good)**로 자동 비행하다가 복구 시 재동기화된다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처는 출현 배경이 다른 여러 패러다임과 자주 비교된다. 기술사 시험에서는 **"왜 이 선택인가"**에 대한 트레이드오프 분석이 핵심이다.

| 구분 | **On-Premise (전통적)** | **Public Cloud** | **Hybrid / Multi-Cloud** |
| :--- | :--- | :--- | :--- |
| **초기 투자 (CAPEX)** | 서버·네트워크·IDC 동시 투자 (수억~수십억) | 0원 (종량 과금) | 일부 (연결·통합 비용) |
| **확장 속도** | 수 주~수 개월 (HW 발주·입고) | 수 분 (API 호출) | 수 시간 (네트워크 경로 설정) |
| **제어권/거버넌스** | 완전 통제 (규제산업 유리) | CSP 정책 종속 (Audit 필요) | 분산 통제 (단일 창구 부재) |
| **데이터 주권** | 국내 IDC 100% 통제 | 리전 선택 가능하나 CSP 정책 의존 | On-Prem + Cloud 동시 운용 |
| **TCO (3년)** | 100% (기준) | 50~70% (워크로드별 상이) | 70~90% (이중 운영비) |
| **적합 워크로드** | Legacy ERP, 극한 보안, HPC | 웹·API, AI/ML, 배치 | 규제 업무 + 신규 서비스 병행 |

| 구분 | **IaaS (EC2)** | **PaaS (Beanstalk, GAE)** | **SaaS (Salesforce, Office365)** | **FaaS (Lambda, Cloud Functions)** |
| :--- | :--- | :--- | :--- | :--- |
| **제어 범위** | OS, 미들웨어 모두 통제 | 앱 코드만 통제 | 설정·확장만 통제 | 함수 코드 + 트리거만 통제 |
| **확장 단위** | VM/Instance | Application | Tenant
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 554 / 800

<- **이전**: [553. 클라우드 아키텍처 핵심 토픽 553번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/553_cloud_architecture_core_topic_553_exam_summar/)
**다음**: [555. 클라우드 아키텍처 핵심 토픽 555번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/555_cloud_architecture_core_topic_555_exam_summar/) ->

---
