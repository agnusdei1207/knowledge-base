---
title: "Cloud Architecture Core Topic 567 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 탄력적 자원 풀(Elastic Resource Pool), API 기반 셀프서비스, 분산 코디네이터(K8s/Service Mesh), 불변 인프라(Immutable Infra), 그리고 폴리글랏 영속성(Polyglot Persistence)을 12-Factor/App+Ops 원칙 위에서 결합하여, **Workload-Driven SLA**(可用性/확장성/비용)를 동적으로 만족시키는 컴퓨팅 패러다임이다.
> 2. **가치**: CapEx->OpEx 전환(통상 30~40% TCO 절감), Auto-Scaling을 통한 Peak/Off-Peak 격차 해소(EC2 기준 60~80% 비용 최적화), MTTR 90% 단축(Chaos Engineering + Observability), 그리고 Time-to-Market 5~10배 가속(예: Netflix의 일 1,000+ 배포, Amazon의 23.6초 평균 배포).
> 3. **판단 포인트**: 마이크로서비스 분할 경계(도메인 응집도 vs 분산 트랜잭션 CAP 비용), Stateful 워크로드의 Storage Decoupling(S3+EFS vs StatefulSet), 컨테이너 오버헤드(10~15%) vs VM 오버헤드(40~60%), 동기(HTTP/gRPC) vs 비동기(Event/Queue) 통신 비율, 그리고 Multi-Cloud 종속성(Lock-in vs 가용성) 사이의 트레이드오프를 정량적으로 분석해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 3-Tier 모놀리식 아키텍처는 IBM mainframe(1960s) -> Client-Server(1990s) -> J2EE/.NET 엔터프라이즈(2000s)로 진화하며 **Tightly-coupled**, **Stateful**, **Scale-up** 중심의 설계를 고수했다. 그러나 2006년 AWS S3·EC2 출시, 2013년 Docker 등장, 2015년 Kubernetes 1.0 GA를 기점으로 **Cloud-Native** 패러다임이 본격화되었다. 마이크로서비스가 수백~수천 개로 분산됨에 따라 네트워크 장애·부분 실패(Partial Failure)·데이터 일관성·배포 복잡도가 기하급수적으로 증가했고, 이를 해결하기 위한 아키텍처 패턴(Circuit Breaker, Saga, Service Mesh, GitOps)이 필수 요소로 자리잡았다.

NIST SP 800-145는 클라우드를 **5대 필수 특성**(On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)과 **3대 서비스 모델**(IaaS/PaaS/SaaS), **4대 배치 모델**(Public/Private/Hybrid/Community)로 정의하며, CNCF(Cloud Native Computing Foundation)는 컨테이너·서비스 메시·마이크로서비스·불변 인프라·선언적 API를 Cloud Native의 5대 축으로 규정한다.

```text
        +-------------------------------------------------------+
        |        전통 엔터프라이즈 -> 클라우드 네이티브 전환 흐름   |
        +-------------------------------------------------------+
   1960s~2000s                    2006~2014                   2015~현재
   +--------------+         +------------------+         +------------------+
   | Mainframe ->  |         | IaaS 가상화 시대  |         | Cloud-Native 시대 |
   | Client/Server|   ->     | (EC2, vSphere)   |   ->     | (K8s, Serverless)|
   | -> J2EE SOA   |         | Scale-up + VM    |         | Scale-out+Contnr |
   +--------------+         +------------------+         +------------------+
        |                          |                            |
   Tightly-coupled           Loosely-coupled            Polyglot, Event-driven
   Stateful, RDBMS           VM-based, NFS              Stateless, NoSQL+EventStore
   18~24개월 릴리즈          3~6개월 릴리즈              일 수십~수천 배포
   CAP: CA 우선              CAP: AP/CP 혼합             CAP: AP 우선, Eventual
   99.9% SLO (8.76h/yr)      99.95% SLO (4.38h/yr)      99.99%+ SLO (52m/yr)
```

2024년 Gartner 보고서에 따르면, 전 엔터프라이즈 워크로드의 **75% 이상이 이미 Public Cloud에 배포**되어 있으며, 신규 애플리케이션의 **95%가 Cloud-Native 패턴**을 채택한다. 그러나 마이크로서비스 전환 실패율(ThoughtWorks 기준 65~75%)이 매우 높기 때문에 **Domain-Driven Design(DDD)의 Bounded Context**, **Strangler Fig Pattern**(점진적 모놀리시스 분리), **Anti-Corruption Layer**(ACL)가 필수적이다. KISA·CSAP·P-ISMS 인증 등 규제 환경에서는 데이터 주권(Data Sovereignty)·암호화 키 관리(KMS/HSM)·감사 로깅(CloudTrail/Audit Log)이 아키텍처 결정의 1차 제약 조건이 된다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"전력 회사 모델"**과 같다. 발전소(데이터센터)·변전소(리전/존)·배전망(CDN/Edge)을 통해 전기(컴퓨팅)를 즉석에서 끌어다 쓰듯, 자원·플랫폼·소프트웨어를 **API 한 줄**로 즉시 프로비저닝하고 사용량만큼 요금을 지불한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Cloud-Native Reference Architecture는 **Control Plane**(관리·오케스트레이션)과 **Data Plane**(실제 트래픽 처리)으로 이원화된다. CNCF Landscape(2024 기준 1,000+ 프로젝트)는 인프라(IaC, Container Runtime), 오케스트레이션(K8s, Service Mesh), 런타임(DB, Streaming, Serverless), 프로비저닝/배포(ArgoCD, Spinnaker), 관측(Observability) 5개 계층으로 분류된다.

```text
        Cloud-Native Architecture 5-Layer Reference Model
        ------------------------------------------------
   Layer 5  | +--------------+  +--------------+  +--------------+
   App/UI   | |  Frontend    |  |  BFF/Mobile  |  |  Edge/SSR   |
            | | (Next.js)    |  | (GraphQL)    |  | (CloudFront)|
            | +------+-------+  +------+-------+  +------+-------+
   ---------+--------+-----------------+-----------------+---------
   Layer 4  |        |  API Gateway (Kong/Apigee/Envoy)    |
   API/GW   |        |  +-Rate Limit, OAuth2/JWT, Routing  |
            |        |  +-Circuit Breaker, Retry, Timeout   |
   ---------+--------+--------------------------------------+---------
   Layer 3  | +------+------------------------------------+------+
   Service  | |  Microservices (Spring Boot/Go/Node.js)         |
            | |  +-Auth | Order | Pay | Catalog | Inventory     |
            | |  +-gRPC/HTTP3 | mTLS | OpenTelemetry Trace     |
            | |  +--------------------------------------+      |
            | |  | Service Mesh (Istio/Linkerd)         |      |
            | |  |  +-Sidecar Proxy(Envoy)             |      |
            | |  |  +-mTLS, Traffic Mgmt, Telemetry    |      |
            | |  |  +-Canary, Blue/Green, A/B Test     |      |
            | |  +--------------------------------------+      |
   ---------+-+------------------------------------------------+----
   Layer 2  | | Orchestrator (K8s/EKS/GKE/AKS)                  |
   Runtime  | |  +-Control Plane (kube-apiserver, etcd)        |
            | |  +-Scheduler, Controller Mgr, Cloud-CSI        |
            | |  +-Node(Pod, kubelet, kube-proxy, CNI)         |
   ---------+-+------------------------------------------------+----
   Layer 1  | +------+ +------+ +--------+ +--------+ +--------+
   Infra    | | VPC  | |Subnet| | IGW/NAT| | EBS/EFS| |S3/Obj  |
            | |AZ-a/b| |Pub/Pr| |Route   | | Block  | | Storage|
            | +------+ +------+ +--------+ +--------+ +--------+
   ---------╧-------------------------------------------------------
              |                                |
        +-----v-----+                    +------v------+
        |  Observ.  |                    |  Sec/Compliance|
        | Prom+Graf |                    | IAM, KMS, WAF |
        | Loki+EFK  |                    | SIEM, SOC     |
        +-----------+                    +--------------+
```

### 핵심 계층별 컴포넌트 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway / BFF** | 외부 트래픽 단일 진입점, L7 라우팅·인증·속도제한 | Kong(OpenResty+Lua), Apigee(API Management), AWS API Gateway(10K RPS 기본, Burst 30K), Envoy 기반 Envoy Gateway. GraphQL Federation(Apollo Router) 또는 REST+gRPC 혼용, OAuth 2.0 + PKCE, mTLS, OPA(Open Policy Agent) 정책 |
| **Service Mesh (Istio/Linkerd)** | Sidecar 패턴으로 서비스 간 통신을 투명하게 가로채 mTLS·관측·트래픽 제어 | Envoy Sidecar(메모리 ~50MB, CPU 0.1~0.5 core/pod), Istio Control Plane(Istiod: Pilot+Citadel+Galley 통합), xDS API 기반 동적 설정, eBPF(Cilium Service Mesh)로 Sidecar 제거 가능, Ambient Mesh(2024 GA) |
| **Container Orchestrator (Kubernetes)** | 컨테이너 자동 배치·스케일링·자가치유·롤링 업데이트 | Control Plane: kube-apiserver(REST 6443), etcd(Raft 합의, 1GB 한계 -> 분할 권장), scheduler(2단계: Filter->Score), controller-manager. Node: kubelet(Cri-API->containerd/CRI-O), kube-proxy(iptables/IPVS/eBPF), CNI(Calico/Cilium/Flannel), CSI(Ceph/AWS EBS), CRI, HPA/VPA/Cluster Autoscaler, KEDA(이벤트 기반) |
| **Serverless / FaaS** | 이벤트 기반 Stateless 함수 실행, Cold Start 최적화 | AWS Lambda(128MB~10GB, 15분 타임아웃, 1000 동시), GCP Cloud Run(knative 기반, 60분, 80GB), Azure Functions(Premium Plan: pre-warmed). Cold Start 200ms~1s(Golang < Node < Python < Java). SnapStart/Provisioned Concurrency로 해결 |
| **Observability Stack** | 메트릭·로그·트레이스 통합 관측, SLO 기반 알림 | **Metrics**: Prometheus(Scrape, PromQL, TSDB 2h retention) + Grafana + Thanos/Cortex(Multi-cluster). **Logs**: Loki(라벨 인덱스) 또는 EFK(Elastic+Fluentd+Kibana). **Traces**: OpenTelemetry SDK -> Jaeger/Tempo/Zipkin. **SLO**: SLI(예: p99 latency < 300ms, Error Rate < 0.1%) -> Error Budget 기반 배포 게이팅(Argo Rollouts) |
| **IaC & GitOps** | 인프라·앱 모두 코드로 선언적 관리, Git을 Single Source of Truth로 | Terraform/OpenTofu(상태 파일 S3+DynamoDB Lock, 2024+ Tofu로 HashiCorp 라이선스 이슈 대응), Pulumi(General-purpose 언어), AWS CDK, Crossplane(K8s CRD로 클라우드 관리). GitOps: ArgoCD(Application Controller 3분 Sync), Flux CD, Progressive Delivery(Argo Rollouts) |
| **Polyglot Storage** | 워크로드 특성별 최적 저장소 선택 | RDBMS(PostgreSQL, Aurora, Spanner), NoSQL(DynamoDB 단일 ms p99, MongoDB, Cassandra, Cosmos DB), Cache(Redis 7, Memcached), Search(OpenSearch/Elasticsearch), Object(S3 11 9s 내구성, MinIO), Wide-Column(Bigtable, ScyllaDB), Graph(Neptune), TimeSeries(InfluxDB, Timescale), Ledger(QLDB) |
| **Event Streaming** | 비동기 이벤트 기반 결합도 분리, CQRS·이벤트 소싱 기반 | Apache Kafka(파티션 순서·내구성, KRaft 모드-ZooKeeper 제거 2024), RabbitMQ(AMQP 0-9-1), Pulsar(계층화 스토리지), AWS Kinesis(KCL), AWS SQS(Standard vs FIFO, exactly-once via deduplication ID), SNS(Pub/Sub Fan-out) |

### 핵심 알고리즘·프로토콜·공식

- **K8s Scheduler 2단계**: `Filter`(`NodeAffinity`, `Taints/Tolerations`, `PodTopologySpreadConstraints`로 AZ 분산, `NodeSelector`로 GPU 노드 지정) -> `Score`(LeastAllocated, BalancedResourceAllocation). HPA 공식: `desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]`
- **CAP/BASE 선택**: 결제·재고 = **CP**(강일관성, Spanner/CockroachDB), 피드·좋아요·조회수 = **AP**(최종일관성, DynamoDB/Cassandra). DynamoDB Tunable Consistency: `ConsistentRead=true` 시 R+W>N, `false` 시 W+R>N(보통 R=1, W=2로 1개만 응답).
- **Karpenter** (2023 GA): 기존 Cluster Autoscaler 대비 **55% 비용 절감**(Spot+Consolidation), 30초 내 Node 프로비저닝. `NodePool` CRD로 `disruption` 정책(consolidation, expire, drift) 정의.
- **eBPF (Cilium)**: 커널 4.19+ 에서 Hook을 통해 Zero-Copy 패킷 처리. Hubble로 L3/L4/L7 Observability, 기존 Sidecar 대비 **CPU 30~40%, 메모리 70% 절감**.
- **Vectorized DB (RAG)**: Pinecone, Weaviate, Milvus. ANN 알고리즘 HNSW(Memory ~O(N), Recall 0.95+), IVF-PQ(Disk 기반, Recall 0.85).
- **Lambda Cold Start 공식**: 평균 = `Init Duration` = `Runtime Init(~100ms) + VPC ENI Init(~500ms)* + Code Init`. VPC Lambda는 ENI 부착 때문에 500ms~2s 추가 -> **VPC Endpoint + Hyperplane ENI**(2020+)로 0ms로 단축.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"항공 관제 시스템"**과 같다. 파일럿(Pod)·항공기(컨테이너)·활주로(Node)·관제탑(Control Plane)·레이더(Service Mesh)가 정밀하게 통신하고, Service Mesh의 mTLS가 **여러 비행기의 통신을 자동으로 암호화**하듯 모든 내부 통신을 안전하게 유지한다. 한 비행기(서비스)가 지연·실패해도 다른 비행기들은 **자동으로 우회(Circuit Breaker)**하여 활주로 위 사고를 방지한다.

---

##
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 567 / 800

<- **이전**: [566. 클라우드 아키텍처 핵심 토픽 566번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/566_cloud_architecture_core_topic_566_exam_summar/)
**다음**: [568. 클라우드 아키텍처 핵심 토픽 568번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/568_cloud_architecture_core_topic_568_exam_summar/) ->

---
