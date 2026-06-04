---
title: "684. 클라우드 아키텍처 핵심 토픽 684번 시험 요약 (Cloud Architecture Core Topic 684 Exam Summary)"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 VPC/Subnet 네트워크 토폴로지, IAM 기반 Zero-Trust 신원 모델, 컨트롤 플레인(Orchestration)과 데이터 플레인(Workload)의 분리, 그리고 선언적 IaC(Terraform/CloudFormation/Pulumi)를 통한 코드형 인프라 실현이 핵심 골격이며, 12-Factor App과 Well-Architected Framework 6대 기둥(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속가능성)을 동시에 만족시켜야 한다.
> 2. **가치**: 온프레미스 대비 CapEx->OpEx 전환으로 초기 인프라 비용 60~80% 절감, Auto-Scaling으로 Peak 대비 평균 자원 35~50% 활용률 향상, Multi-AZ/Region 구성으로 RTO 분 단위·RPO 0~수 분 달성, MTTR 평균 70% 단축(AWS Well-Architected Lab 기준), 글로벌 엣지 배포로 사용자 체감 latency 100~300ms -> 20~50ms 수준으로 개선.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs 멀티/하이브리드 전략, Synchronous(Strong consistency) vs Asynchronous(Eventually consistent) 데이터 복제, Stateless microservice + Eventual consistency + Saga 패턴 채택 시 트레이드오프 분석, Workload 특성(IaaS/CaaS/PaaS/FaaS/SaaS)에 따른 책임공유 모델(Shared Responsibility) 경계 설정, Cloud Egress 비용·Data Gravity·Compliance 거주성(데이터 주권) 고려 여부.

---

## Ⅰ. 개요 및 필요성

클라우드 컴퓨팅은 NIST SP 800-145 정의에 따라 **"네트워크, 서버, 스토리지, 애플리케이션, 서비스 등 구성 가능한 컴퓨팅 자원을 어디서나(on-demand) 최소한의 관리 노력으로 신속히 provisioning 및 해제 가능한 범용 접속 모델"** 로, 2006년 AWS S3/EC2 출시 이후 18년 동안 IT 인프라 패러다임을 자본지출(CapEx) 중심의 정적 자원 모델에서 사용량 기반 종량제(OpEx) 동적 탄력 모델로 전환시켰다. 특히 COVID-19 이후 글로벌 트래픽의 비대칭적 급증(예: Netflix 스트리밍 30%^, 카카오톡 DAU 1.6배)에 대응하기 위해, 전통적인 Capacity Planning의 한계(과잉 provisioning으로 평균 30% 이상 idle, 부족 시 기회비용 막대)를 **Elastic Demand-Response** 모델로 대체해야 하는 필연적 과제가 대두되었다.

기술사 관점에서 클라우드 아키텍처의 본질은 단순한 "IDC 이전"이 아니라, **"가용성·확장성·탄력성·관측가능성·자동화"라는 5대 NFR(Non-Functional Requirement)** 을 달성하기 위한 분산 시스템 설계의 집약체이다. 이를 위해 Region/AZ(Availability Zone) 단위의 물리적 격리, Control Plane/Data Plane 분리, Immutable Infrastructure, Ephemeral Workload, Declarative API, Event-Driven Architecture(EDA), Cell-Based Architecture, Bulkhead/Shedder/Backpressure 패턴, Chaos Engineering(Netflix Chaos Monkey -> Gremlin) 같은 기법이 필수적으로 등장했다. 또한 CNCF(Cloud Native Computing Foundation) 생태계의 확산으로 Kubernetes(K8s) + Service Mesh(Istio/Linkerd) + GitOps(ArgoCD/Flux) + Observability(OpenTelemetry/Prometheus/Grafana/Loki/Tempo) 스택이 사실상 표준 런타임 추상화 계층이 되었으며, 한국 공공/금융 시장에서는 2024년 이후 **클라우드 보안인증(CSAP) 등급 강화**, **금융데이터 이동규제**, **개인정보보호법 가명정보 처리 가이드라인** 등 컴플라이언스 요건이 클라우드 아키텍처 설계에 직접적인 제약으로 작용하고 있다.

```text
        +----------------------------------------------------------+
        |              Cloud Architecture 5-Layer 모델            |
        +----------------------------------------------------------+
                                       ^
                                       | API/SDK/CDK/Terraform
                                       |
        +------------------------------+-------------------------------+
        | L5. Governance & Compliance  (IAM/Org/Policy/CSAP/ISO27001)  |
        +--------------------------------------------------------------+
        | L4. Observability & FinOps   (Logs/Metrics/Traces/Cost/CFM)  |
        +--------------------------------------------------------------+
        | L3. Platform & Orchestration (K8s/ServiceMesh/GitOps/Argo)  |
        +--------------------------------------------------------------+
        | L2. Distributed Workload     (μSvc/Serverless/EDA/SAGA/CQRS)|
        +--------------------------------------------------------------+
        | L1. Infrastructure (Global)  (Region/AZ/Edge/PoP/Backbone)   |
        +--------------------------------------------------------------+

   +--------------+  +--------------+  +--------------+  +--------------+
   |   Region A   |  |   Region B   |  |   Region C   |  |      Edge    |
   | Seoul(apne) |  | Tokyo(apne1)|  | Virginia(us) |  | CloudFront/  |
   |              |  |              |  |              |  |  Cloudflare  |
   | +--+ +--+   |  | +--+ +--+   |  | +--+ +--+   |  |   CDN/PoP    |
   | |A1| |A2|   |  | |B1| |B2|   |  | |C1| |C2|   |  |              |
   | +--+ +--+   |  | +--+ +--+   |  | +--+ +--+   |  |              |
   |  AZ  AZ      |  |  AZ  AZ      |  |  AZ  AZ      |  |              |
   +------+-------+  +------+-------+  +------+-------+  +------+-------+
          |                 |                 |                 |
          +-----------------+--------+--------+-----------------+
                                     |
                          +----------v----------+
                          |  Transit GW / WAN   |
                          |  VPC Peering / DX   |
                          |  Interconnect 100G  |
                          +---------------------+
```

온프레미스 대비 클라우드 네이티브 패러다임의 차이는 **(1) 자원 모델**: 사전 할당(Reservation)->사후 청구(Consumption), **(2) 실패 모델**: MTBF(Mean Time Between Failure) 중심 -> MTTR(Mean Time To Recovery) 중심, **(3) 변경 모델**: 수동 OS/미들웨어 패치 -> Immutable AMI/Container Image, **(4) 네트워크 모델**: L2 VLAN 확장 -> L3 Overlay(VXLAN/Segment Routing), **(5) 보안 모델**: Perimeter(Castle) -> Zero-Trust(Identity+Policy+Encryption Everywhere), **(6) 데이터 모델**: RDBMS 중심 -> Polyglot Persistence(SQL+NoSQL+Object+Data Lakehouse+Vector DB) 6가지 축에서 근본적으로 전환되었다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **"전 세계에 미리 깔려 있는 수도·전기·도로 인프라(Region/AZ/Backbone) 위에, 필요할 때마다 우체국에서 택배 박스(VM/Container/Function)를 빌려서 자기 집 인테리어(IaC/Config)를 마음대로 꾸미고, 이사할 때 박스째 반납하면 청소 비용만 청구되는 시스템"** 과 같다. 직접 발전소를 짓는(On-Prem) 것 대비 초기 비용은 0에 가깝지만, 전기료를 많이 쓰면 청구서가 커지듯 Egress·API 호출·Managed 서비스 사용량에 대한 FinOps 감시가 필수적이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 4대 핵심 메커니즘은 **① 셀 단위 격리(Cell-Based) ② 제어 평면/데이터 평면 분리 ③ 선언적 API와 Reconciliation Loop ④ 다계층 방어(Defense-in-Depth) + Zero-Trust** 이다. 각 메커니즘은 단순한 기술이 아니라 "분산 시스템의 8대 함정(Fallacies of Distributed Computing: 네트워크는 안정적이지 않다, latency는 0이 아니다, 대역폭은 무한하지 않다, 보안은 1명이 책임진다, 토폴로지는 변하지 않는다, 관리자는 1명이다, 전송 비용은 0이다, 네트워크는 동질적이다)"을 회피하기 위한 실전 노하우의 집약체이다.

```text
   +-------------------------------------------------------------------+
   |             Control Plane vs Data Plane 분리 구조                 |
   +-------------------------------------------------------------------+

   +----------------------+              +--------------------------+
   |     Control Plane    |              |      Data Plane          |
   |  (Brain / Slow Path) |              |  (Muscle / Fast Path)    |
   +----------------------+              +--------------------------+
   | • K8s API Server     |  -- watch--->| • kubelet (Node Agent)   |
   | • etcd (Raft)        |              | • kube-proxy / CNI       |
   | • IAM Policy Engine  |              | • Envoy Sidecar (xDS)    |
   | • Route 53 DNS       |              | • VPC ENI / Hypervisor   |
   | • S3 ListObjects     |              | • SSD/NVMe Data Path     |
   | • Auto-Scaling Group |              | • User Workload Pods     |
   |                      |              |                          |
   | 가용성: 99.99% SLA   |              | 처리량: 100K req/s/node  |
   | 지연: 수 초          |              | 지연: μs ~ ms            |
   | 상태: Strong Cons.   |              | 상태: Eventually Cons.   |
   +----------------------+              +--------------------------+
                ^                                  ^
                |                                  |
        +-------+--------+                +-------+--------+
        |  Operator/Admr |                |  End-User /   |
        |  GitOps PR/CD  |                |  Client SDK   |
        +----------------+                +----------------+
```

```text
   +-------------------------------------------------------------------+
   |      Multi-AZ Active-Active Stateful Service 패턴                |
   +-------------------------------------------------------------------+

                        Internet / CloudFront
                                 |
                          Route 53 (Latency/Weighted)
                          +------+------+
                          v             v
                    +---------+   +---------+
                    |  ALB-A  |   |  ALB-B  |  (Cross-Region)
                    +----+----+   +----+----+
                         |             |
              +----------+-------------+----------+
              v          v             v          v
         +--------+ +--------+   +--------+ +--------+
         | EKS-A1 | | EKS-A2 |   | EKS-B1 | | EKS-B2 |  (Stateless Pod)
         +---+----+ +---+----+   +---+----+ +---+----+
             |          |             |          |
             +----+-----+             +----+-----+
                  v                        v
           +--------------+         +--------------+
           | Aurora WR    | <-------> | Aurora WR    |   (Writer/Reader)
           | Global DB    |  Cross- | Global DB    |   (<1s RPO)
           | (MySQL PG.)  |  Region | (MySQL PG.)  |
           +------+-------+  Replica+------+-------+
                  |                        |
                  +----------+-------------+
                             v
                    +------------------+
                    |   S3 / DynamoDB  |
                    |  (11x9s Object)  |
                    +------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Region / AZ (Edge Locality)** | 지리적 격리 단위 (e.g., `ap-northeast-2` 서울, 4개 AZ) | Region 간 ≥100km 물리 분리, AZ 간 ≤100km ≤2ms RTT, 광케이블 다중화, 99.99% 인프라 SLA. Active-Active 시 Global DB/Route 53 Health Check 활용, Cross-Region Replication S3 CRR·DynamoDB Global Tables·Aurora Global Database(<1s RPO) |
| **VPC / Subnet (Network Plane)** | L2/L3 가상 네트워크 격리, RFC1918 10.0.0.0/8 CIDR 분할 | /16~ /28 Subnet 설계, Public/Private/Isolated Tiers 3-Tier, NAT Gateway/Instance Egress 제어, VPC Endpoint(AWS PrivateLink, Azure Private Link, GCP Private Service Connect)로 S3/DynamoDB/KMS/Secrets Manager 등 Managed 서비스 사설 통신, TGW(Transit Gateway) + RAM(Resource Access Manager)로 Hub-Spoke |
| **IAM / Zero-Trust (Identity Plane)** | 신원·권한 기반 접근 통제, "Never Trust, Always Verify" | IAM Role + OIDC/Federation(GitHub Actions, GKE Workload Identity, IRSA), IAM Access Analyzer, SCP(Service Control Policy), ABAC(Attribute-Based), RBAC(Role-Based), PBAC(Policy-Based), RBAC+K8s(Role/ClusterRole), MFA + FIDO2, AWS IAM Identity Center(SSO), Short-lived STS Token(15~60min), mTLS SPIFFE/SPIRE |
| **Orchestrator (K8s/EKS/AKS/GKE)** | 컨테이너 스케줄링·자기치유·롤링업데이트 | K8s API Server + etcd(Raft 합의), ReplicaSet/Deployment(Stateless), StatefulSet(Stable NetworkID/Volume), DaemonSet(Node-level), HPA/VPA/Cluster Autoscaler/Karpenter(예측적 스케일링), PodDisruptionBudget(PDB), PriorityClass, TopologySpreadConstraints(AZ 분산), ResourceQuota·LimitRange |
| **Data Layer (Polyglot Persistence)** | 트랜잭션·분석·객체·시계열·벡터 등 워크로드별 최적 저장 | OLTP: Aurora(MySQL/PostgreSQL, 6-way Replication, <10ms Read Replica Lag), DynamoDB(Global Tables, 3-region Multi-Active, Single-digit ms), Cloud Spanner(Strongly Consistent Global, TrueTime API). OLAP: Redshift/Snowflake/BigQuery/Databricks (Lakehouse: Delta Lake + Iceberg + Hudi). 캐시: ElastiCache(Redis Cluster)/Memorystore/Amazon DAX. 객체: S3 11x9s(99.999999999%) + Intelligent-Tiering. 검색: OpenSearch/Elasticsearch. 시계열: Timestream/InfluxDB. 벡터: Pinecone/Weaviate/Milvus/RDS pgvector |
| **Messaging / EDA (Async Backbone)** | 비동기·느슨한 결합·이벤트 기반 워크플로우 | Pub/Sub: Amazon SQS(Standard/FIFO, Visibility Timeout, DLQ), SNS(Topic Fan-out), EventBridge(Cross-account, Schema Registry), Kafka(Exactly-Once Semantics v3, KRaft, Tiered Storage), Pub/Sub Lite, Azure Service Bus. 워크플로우: Step Functions/Apache Airflow/Temporal, Saga 보상 트랜잭션 |
| **Observability (O11y)** | 3대 신호(Logs/Metrics/Traces) 통합 + 사용자 경험 | Metrics: Prometheus + Grafana + Thanos/Cortex/Mimir(장기 저장), CloudWatch/Stackdriver. Traces: OpenTelemetry SDK + Jaeger/Tempo/Honeycomb(OpenTelemetry Collector, OTLP). Logs: Fluent Bit/Vector -> Loki/CloudWatch/Elasticsearch. SLO/SLI: SLI(가용성·지연·처리량) + Error Budget + Burn Rate(Google SRE Workbook). AIOps: Anomaly Detection, RCA 자동화 |
| **Edge / CDN** | 사용자에게 가장 가까운 캐시·컴퓨팅 | CloudFront/Cloudflare/Fastly(Akamai), Lambda@Edge/Cloudflare Workers(Sub-ms Cold Start), 이미지 최적화(Image Resizing), WAF(OWASP Top
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 684 / 800

<- **이전**: [683. 클라우드 아키텍처 핵심 토픽 683번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/683_cloud_architecture_core_topic_683_exam_summar/)
**다음**: [685. 클라우드 아키텍처 핵심 토픽 685번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/685_cloud_architecture_core_topic_685_exam_summar/) ->

---
