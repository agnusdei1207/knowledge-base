---
title: "Cloud Architecture Core Topic 695 Exam Summary"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 **탄력적 리소스 풀(Elastic Resource Pool)** 위에서 **API 기반 선언적 인프라(IaC)**, **마이크로서비스 분해**, **불변 인프라(Immutable Infrastructure)**, **12-Factor 원칙**을 결합하여, 장애를 전제로 한 셀프힐링·오토스케일링·무중단 배포가 가능한 분산 시스템 토폴로지를 의미한다.
> 2. **가치**: AWS Well-Architected 5-Pillar(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화) 적용 시 **가용성 99.99%->99.999% 향상**, TCO는 온프레미스 대비 **CapEx->OpEx 전환으로 30~60% 절감**, 배포 빈도는 월 1회->일 10회 이상으로 **TTM(Time-to-Market) 8배 단축**이 가능하다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **일관성 vs. 가용성(CAP/PACELC)**, **세분화 vs. 운영 복잡성(Conway's Law & 분산 트랜잭션)**, **벤더 종속(Lock-in) vs. 이식성(Portability)**, **콜드 스타트 허용 vs. 지연시간 SLA**, **Egress 비용 vs. Multi-Region Active-Active**이며, 워크로드 특성(OLTP/배치/스트리밍/AI 추론)에 따라 아키텍처 스타일을 다층화해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적 3-Tier 모놀리식 아키텍처는 **수직 확장(Scale-Up)의 한계**, **프로비저닝 리드타임(weeks~months)**, **H/W CAPEX 부담**, **단일 장애점(SPOF)**, **릴리스 간 의존성으로 인한 배포 병목**이라는 5대 구조적 한계에 직면했다. 클라우드 아키텍처는 이를 **가상화·컨테이너화·오케스트레이션·선언적 API**로 해체하면서, 인프라를 코드로(Infrastructure as Code) 다루는 **불변 인프라 패턴**, **셀프서비스 카탈로그**, **수평 확장(Scale-Out)**, **Pay-as-you-go 과금 모델**로 전환한다. 이 변화는 단순한 호스팅 이전이 아니라 **불확실성 하에서의 실험 비용 최소화**와 **가역적 의사결정(Reversible Decision)**을 가능하게 하는 조직·기술·비즈니스의 동시 변혁이다.

```text
[ 진화 패러다임 비교 ]

  1960s Mainframe        1990s Client-Server       2010s Cloud-Native
  +-------------+        +--------------+         +----------------------+
  | Terminal ---+-► Main | Browser --►  |         | K8s Service Mesh     |
  | Dumb Client|   |  +--+ Web/App/DB  |         | Sidecar + Container  |
  |             |   |  |  Tiered Monolith        | + Serverless FaaS    |
  +-------------+   |  +--------------+         | + Managed DB/AI/ML   |
     공유자원,        |   수직확장,                | + IaC/Terraform      |
     배치처리          |   라이선스                 | + GitOps/ArgoCD      |
                    |                           |   (선언적, 불변, 셀프힐링) |
                    +---------------------------+----------------------+
       CapEx Heavy          CapEx/OpEx 혼합            OpEx, Pay-per-Use
       1-year Provisioning  1-month Provisioning       1-min Auto-Scaling
       SPOF 허용            HA Cluster                 Multi-AZ + Region
```

| 항목 | 레거시 On-Premise | 클라우드 네이티브 |
| :--- | :--- | :--- |
| 자원 프로비저닝 | 수동, 4~12주 | API/Terraform, 30초~5분 |
| 확장 모델 | 수직(Scale-Up) | 수평(Scale-Out) + HPA/VPA/Cluster Autoscaler |
| 장애 대응 | Cold Standby, MTTR 수 시간 | Multi-AZ/Region, MTTR 수 분, Chaos Engineering |
| 비용 모델 | CapEx (감가상각) | OpEx (초당/요청당 과금) |
| 릴리스 주기 | 분기 1회 | 일 10회+ (CI/CD + Progressive Delivery) |
| 운영 패러다임 | Pet(개별 관리) | Cattle(교체 가능한 인스턴스) |

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **택시 호출 앱(Uber/Tada)**과 같다. 차를 사서 보관할 필요 없이(온프레미스 CapEx), 필요할 때 호출하며(API), 사람이 많으면 SUV로 자동 배차(오토스케일), 사고 나면 즉시 다른 차량으로 자동 대체(셀프힐링)된다. 운전자 1명당 정산이 자동 처리되는 것(IaC 선언)이 핵심 가치다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **5계층 참조모델(Reference Model)**로 분해할 수 있다: ① Global Edge/Network, ② Region/AZ 토폴로지, ③ 컴퓨트 추상화(VM/Container/Function), ④ 데이터 평면(Managed DB/Object Storage/Stream), ⑤ 제어 평면(IAM/Policy/Observability). 이 위에 **12-Factor App**, **Cloud-Native Computing Foundation(CNCF) Landscape**, **AWS Well-Architected Framework 5-Pillar**, **TOGAF/SABSA**가 거버넌스 층을 형성한다.

```text
[ 클라우드 네이티브 참조 아키텍처 (5-Layer + Cross-Cutting) ]

                         +------------------------------+
                         |   ⑤ 거버넌스/관측/보안(Cross) |
                         |  IAM(OIDC) | OPA | Vault      |
                         |  Prometheus| Loki | Tempo     |
                         |  Falco     | Trivy| OPA/Gatekeeper |
                         +------+-----------------------+
                                |
        +-----------------------+-----------------------+
        |                       |                       |
   +----v-----+           +-----v-----+           +-----v-----+
   | ① Edge  |           | ② Region  |           | ③ Compute |
   |CloudFront|           | Multi-AZ  |           | EKS/AKS   |
   |Global    |           | us-east-1a|           | Fargate   |
   |Accelerator|          | us-east-1b|           | Lambda    |
   | + WAF    |           | us-east-1c|           | + Karpenter|
   +----+-----+           +-----+-----+           +-----+-----+
        |                       |                       |
        +-----------------------+-----------------------+
                                |
                    +-----------v------------+
                    | ④ 데이터 평면           |
                    | +---------+ +--------+ |
                    | |Aurora   | |DynamoDB| |  <- OLTP(ACID vs BASE)
                    | |Global   | |DAX     | |
                    | |Database | +--------+ |
                    | +---------+ +--------+ |
                    | +---------+ |S3+Lake | |  <- Data Lake/Iceberg
                    | |Elasti-  | |House   | |
                    | |Cache    | +--------+ |
                    | +---------+ +--------+ |
                    |             |Kinesis/ | |  <- Streaming
                    |             |Kafka/MSK| |
                    |             +--------+ |
                    +------------------------+

  트래픽 흐름:  Client -> CDN/Edge -> API Gateway/WAF
         -> Service Mesh(Istio) -> Sidecar(Envoy)
         -> Pod(Container) -> Sidecar -> mTLS to Backend
         -> Managed DB(Read Replica) / Cache / Queue
         -> Async Event Bus -> Lambda/Worker -> Object Storage
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway / Ingress** | 외부 트래픽 진입점, 라우팅·인증·속도제한 | Kong, AWS API Gateway, Apigee, Envoy Gateway, gRPC-Gateway. **Rate Limiting(Token Bucket)**, **OAuth2.0/JWT 검증**, **Circuit Breaker(Hystrix/Resilience4j)**, OpenAPI 3.1 사양 기반 계약 우선 개발(Contract-First) |
| **Service Mesh (Data/Control Plane)** | 서비스 간 통신·관측·정책 분리 | Istio(Envoy Sidecar), Linkerd(Linkerd2-proxy), Cilium(eBPF, Sidecar-less). **mTLS 자동화(SPIFFE/SPIRE)**, **L7 트래픽 분할(Canary 5->25->100%)**, **Telemetry(RED: Rate/Error/Duration)** |
| **Container Orchestrator** | 컨테이너 라이프사이클·스케줄링·자가치유 | Kubernetes 1.31+(K8s), **Control Plane(API Server/etcd/scheduler/cm) + Node(kubelet/kube-proxy/cri-o)**. **HPA(Metrics Server)**, **VPA**, **Karpenter(Just-in-time Node Provisioning)**, **Pod Disruption Budget(PDB)**, **Topology Spread Constraints** |
| **Immutable Infra / IaC** | 선언적 인프라 정의, 재현성·드리프트 탐지 | Terraform/OpenTofu(HCL2), Pulumi(TypeScript/Python), AWS CDK, **GitOps(ArgoCD/Flux)** — *desired state*를 Git에 두고 Reconciler가 *actual state*로 수렴. **OPA/Conftest**로 Policy-as-Code 검증 |
| **데이터 계층 (Polyglot Persistence)** | 워크로드별 최적 저장소 선택 | **OLTP**: Aurora PostgreSQL(MySQL 호환, 6-way Replica), CockroachDB(Geo-Partitioned), DynamoDB(Single-digit ms). **Cache**: Redis Cluster(ElastiCache), Dragonfly. **검색**: OpenSearch/Elasticsearch. **Object**: S3(11 9s 내구성). **Lake**: Iceberg/Delta/Hudi on S3 + Athena/Trino. **Queue/Stream**: SQS Standard/FIFO, Kafka(Kraft 모드, ZooKeeper 제거), Kinesis Data Streams |
| **보안/거버넌스 (Zero Trust)** | 신원·기기·컨텍스트 기반 최소권한 | **BeyondCorp**(Google), **ZTNA 2.0** — *네트워크 위치 ≠ 신뢰*. **IAM Roles for Service Accounts(IRSA)**, **OIDC Federation**, **Secrets Manager/Vault(Dynamic Secret)**, **KMS/HSM Envelope Encryption**, **Confidential Computing(SEV-SNP/TDX)** |
| **관측 가능성 (Observability 3 Pillar)** | Metrics·Logs·Traces + 4번째 Profile | **Prometheus + Grafana(10s/30s 메트릭)**, **Loki/ELK(로그 집계)**, **Tempo/Jaeger/Zipkin(분산 트레이싱, OpenTelemetry SDK)**, **Continuous Profiling(Pyroscope/pprof)**. **SLO/SLI** 정의 -> Error Budget 기반 배포 게이트 |
| **CI/CD / Progressive Delivery** | 자동화된 빌드·테스트·점진적 배포 | **GitHub Actions/Argo Workflows**, **Argo Rollouts**(Canary/Blue-Green), **Flagger**(자동 카나리 분석, Prometheus 메트릭 기반), **Keptn**(SLI/SLO 기반 자동 롤백), **Feature Flag(LaunchDarkly/Unleash)** |

**핵심 원리 — 분산 시스템 트레이드오프와 알고리즘**

1. **CAP/PACELC 정리**: 네트워크 분단(Partition) 시 **일관성(C)과 가용성(A) 중 하나**를 양보해야 한다. 클라우드 분산 시스템은 대부분 **AP 우선**(예: DynamoDB, Cassandra -> *Eventually Consistent* + *Tunable Consistency*). PACELC 확장은 *분단 없을 때*의 Latency vs. Consistency까지 명시.
2. **합의 알고리즘**: etcd/Consul은 **Raft** (Leader Election + Log Replication, `O(log N)` 하트비트). Kafka KRaft는 Controller Quorum 기반 메타데이터 합의. Hyperledger Fabric는 **PBFT 변형** (Byzantine 허용).
3. **일관성 모델**: 강한 일관성(Linearizability, Spanner의 TrueTime + GPS/Atomic Clock), 인과적 일관성(Causal, COPS), 읽기-자신의-쓰기(Read-your-writes, Sticky Session), 결과적 일관성(Eventual, Dynamo-style: *(N, R, W)* quorum 튜닝, 예: *N=3, R=2, W=2*).
4. **Saga 패턴**: 마이크로서비스 트랜잭션을 **Choreography(Event-driven)** 또는 **Orchestration(Camunda/Temporal)**로 보상 트랜잭션(Compensating Tx) 기반 처리. *Forward Recovery* + *Backward Recovery* 조합.
5. **CQRS + Event Sourcing**: 쓰기 모델과 읽기 모델 분리, 모든 상태 변경을 불변 이벤트 로그(Kafka Topic)에 저장 -> 시간 여행 디버깅·감사 로그·재구성 가능. 단, **Schema Evolution(Upcaster)**과 **Snapshot** 전략 필수.
6. **캐싱 무효화의 두 가지 난제(Cache Invalidation 2 Hard Things)**: TTL + LRU, **Cache-Aside vs. Read-Through vs. Write-Behind** 패턴, **Stampede 방지**(Probabilistic Early Expiration, Single Flight), **Negative Cache**(에러 TTL 분리).
7. **불변 인프라 & Phoenix Server**: 컨테이너는 평균 수명 1~7일, OS 패치 시 **Recreate Strategy**(Blue/Green) 선호. **Bottlerocket(Container-Optimized OS)**, **Talos Linux**로 가변 영역 최소화.

- **📢 섹션 요약 비유**: 위 아키텍처는 **국제 공항 운영**과 같다. ① 입국장(Edge/CDN)이 승객을 먼저 걸러내고, ② 게이트-활주로(Region/AZ)가 이착륙 안전을 보장하며, ③ 지상조업 오케스트레이터(K8s)가 비행기를 정해진 슬롯에 배치하고, ④ 화물창(데이터 평면)이 짐을 종류별(Polyglot)로 보관하며, ⑤ 관제탑(IAM/관측)이 모든 비행의 안전·연착·보안 이벤트를 실시간 모니터링한다. 이 중 어느 한 층이 무너지면 전체가 마비되므로 **5계층 모두의 다중화**가 필수다.

---

## Ⅲ. 비교 및 연결

| 구분 | Monolith | Microservices | Serverless (FaaS) |
| :--- | :--- | :--- | :--- |
| **배포 단위** | WAR/EAR (1개 프로세스) | Container Image (수십~수백) | Function (Lambda ZIP/Image) |
| **확장성** | 수직, AWM/리플리카 | 수평, HPA/KEDA | 자동, 0->N (Concurrency Limit) |
| **장애 격리** | 프로세스 크래시 = 전체 다운 | Bulkhead/Sidecar 격리 | Function timeout/Quota 격리 |
| **트랜잭션** | ACID, 2PC 가능 | Saga/Outbox/CDC | Step Functions + DLQ |
| **콜드 스타트** | 없음
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 695 / 800

<- **이전**: [694. 클라우드 아키텍처 핵심 토픽 694번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/694_cloud_architecture_core_topic_694_exam_summar/)
**다음**: [696. 클라우드 아키텍처 핵심 토픽 696번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/696_cloud_architecture_core_topic_696_exam_summar/) ->

---
