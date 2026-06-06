---
title: "Cloud Architecture Core Topic 635 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST의 5대 필수 특성(온디맨드 셀프서비스, 광범위한 네트워크 접근, 리소스 풀링, 빠른 탄력성, 측정 가능한 서비스)과 3대 서비스 모델(IaaS/PaaS/SaaS)을 기반으로, **Well-Architected Framework의 5대 기둥(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화)**과 **Cloud Native Computing Foundation(CNCF) 트레이드オフ 맵**을 통해 설계된다.
> 2. **가치**: AWS Well-Architected Tool 활용 시 평균 **클라우드 비용 25~30% 절감**, 다운타임 **63% 감소**(Forrester 연구), 배포 빈도 **200배 증가**(DORA Report Elite Performers), MTTR(mean time to recovery) **2,604배 단축**을 달성하며, CAPEX를 OPEX로 전환하여 초기 인프라 투자 대비 ROI를 12~18개월 내 회수한다.
> 3. **판단 포인트**: 핵심 트레이오프는 (1) **일관성 vs. 가용성** (CAP Theorem, AP vs CP 시스템 선택), (2) **통제력 vs. 민첩성** (Lift-and-Shift vs Cloud-Native Refactoring), (3) **중앙 집중식 vs. 분산 아키텍처** (Monolith vs Microservices, 데이터베이스 분할 여부)이며, **6R 마이그레이션 전략(Rehost/Replatform/Refactor/Repurchase/Retire/Retain)** 중 워크로드 특성에 맞는 최적 경로를 선택하는 것이 기술사의 핵심 판단 영역이다.

---

## Ⅰ. 개요 및 필요성

클라우드 컴퓨팅은 2006년 AWS S3와 EC2 출시 이후 **가상화 -> 컨테이너화 -> 서버리스 -> 엣지 컴퓨팅**으로 진화해왔으며, 2024년 기준 글로벌 퍼블릭 클라우드 시장 규모는 약 **6,790억 USD**(Gartner), 국내 시장은 약 **12조 원**에 도달했다. 이러한 클라우드 전환은 단순한 인프라 이전이 아니라 **아키텍처 패턴 자체의 패러다임 전환**을 의미한다. 전통적인 온프레미스 3-Tier 아키텍처(Presentation-Business-Data Tier)는 수직 확장(Scale-Up)에 의존하여 CAPEX가 높고 프로비저닝에 수 주가 소요되었으나, 클라우드 네이티브 아키텍처는 수평 확장(Scale-Out) 기반으로 **Auto Scaling Group, 멀티 AZ 배포, 글로벌 엣지 로케이션(CloudFront, Cloud CDN)**을 활용하여 트래픽 피크 시 수 분 내 수천 대의 인스턴스를 자동 확장한다.

핵심 기술적 과제로는 (1) **다중 장애 도메인 관리**(단일 AZ 장애가 전체 서비스에 영향 없도록 설계), (2) **데이터 일관성 모델 선택**(Strong Consistency vs Eventual Consistency, DynamoDB의 tunable consistency), (3) **Vendor Lock-in 최소화**(Terraform IaC, Kubernetes 추상화, Cloud-agnostic API 설계), (4) **FinOps**(클라우드 비용 거버넌스 및 최적화), (5) **제로트러스트 보안 모델** 구현(Identity-Aware Proxy, mTLS, SPIFFE/SPIRE) 등이 있다.

```text
[클라우드 아키텍처 패러다임 전환]

   온프레미스 시대 (1990~2010)              클라우드 네이티브 시대 (2020~)
   +---------------------+                 +-----------------------------+
   |  Monolith           |                 |  Microservices              |
   |  +---------------+  |                 |  +--+ +--+ +--+ +--+ +--+  |
   |  |   단일 WAS    |  |      ------►    |  |S1| |S2| |S3| |S4| |S5|  |
   |  |  (WebLogic)   |  |                 |  +-++ +-++ +-++ +-++ +-++  |
   |  +---------------+  |                 |    +----+----+----+----+     |
   |  RDBMS (Oracle)     |                 |   Service Mesh (Istio)      |
   |  Scale-Up           |                 |   Polyglot Persistence      |
   |  수주 프로비저닝    |                 |   Scale-Out (수 분 내 확장)  |
   +---------------------+                 +-----------------------------+

   장애 대응: HA Pair                       장애 대응: Chaos Engineering
   배포: 수 개월                            배포: 하루 수십~수백 회
   비용: CAPEX 중심                         비용: OPEX + Reserved/Spot 혼합
```

기술사적 관점에서 클라우드 아키텍처의 본질은 **"비즈니스 요구사항(가용성 99.99%, RTO 1시간, RPO 5분)을 클라우드 서비스 프리미티브로 매핑하는 역량"**이다. 동일한 SLO(서비스 수준 목표)라도 **Active-Active 멀티리전(비용 3배, 가용성 99.999%)**과 **Warm Standby(비용 1.5배, 가용성 99.95%)** 사이의 선택은 기술적 깊이를 결정짓는 핵심이다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"전기 그리드"**와 같다. 자체 발전소(온프레미스)를 짓는 대신 전력회사(클라우드 제공자)의 그리드에 연결하되, **전압(보안 정책), 차단기(서킷 브레이커), 변전소(리전/AZ)**를 어떻게 배치하느냐가 안정성을 결정한다. 한국전력 같은 단일 제공자에 **전적으로 의존하면 감전 위험(Lock-in)**이 있고, **태양광 자가발전(Hybrid Cloud)**을 병행해야 에너지 주권(데이터 주권)을 지킬 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심 원리는 **NIST SP 500-292 참조 모델**과 **ISO/IEC 22123** 표준에 기반하며, 5계층(클라우드 클라이언트/애플리케이션/플랫폼/인프라/서버)과 3개 역할(클라우드 소비자/제공자/감사자)로 구성된다. 실무적으로는 **AWS/Azure/GCP의 Well-Architected Framework**가 표준 참조 모델로 사용된다.

**핵심 동작 메커니즘**은 다음과 같이 6단계로 분해된다:
1. **요청 라우팅**: Route 53/Cloud DNS가 GeoDNS, Latency-Based Routing, Weighted Round Robin으로 트래픽 분산
2. **로드 밸런싱**: L4(NLB, Network Load Balancer, 5 tuple hash) vs L7(ALB, Application Load Balancer, path/host-based routing) 선택
3. **컨테이너 오케스트레이션**: Kubernetes가 Pod 스케줄링, HPA(Horizontal Pod Autoscaler, CPU 70% 임계치), Cluster Autoscaler, Karpenter로 노드 자동 확장
4. **서비스 디스커버리**: CoreDNS, Consul, Istio Control Plane이 서비스 레지스트리 관리
5. **데이터 분산**: DynamoDB의 Consistent Hashing (vNode 16개, 256개 파티션), Cassandra의 Gossip Protocol (1초 주기), Kafka의 Partition Leader Election (Zab/KRaft)
6. **관측 가능성(Observability)**: OpenTelemetry 기반 3대 시그널(Metrics: Prometheus, Logs: Loki/ELK, Traces: Jaeger/Tempo) 수집

```text
[클라우드 네이티브 마이크로서비스 아키텍처 상세 구조]

   +----------------------------------------------------------------------+
   |  Global Edge: CloudFront / Cloud CDN (TLS 1.3, HTTP/3, WAF)          |
   +--------------------+-------------------------------------------------+
                        |
   +--------------------v-------------------------------------------------+
   |  DNS & Traffic Management: Route 53 (Health Check, Failover Policy)   |
   |       +------------+------------+------------+                       |
   |       | us-east-1  | eu-west-1  | ap-northeast-2                     |
   |       +------------+------------+------------+                       |
   +--------------------+-------------------------------------------------+
                        |
   +--------------------v-------------------------------------------------+
   |  API Gateway: Kong / AWS API Gateway / Apigee                        |
   |   - Rate Limiting (Token Bucket), JWT Validation, OAuth 2.0/OIDC     |
   +--------------------+-------------------------------------------------+
                        |
   +--------------------v-------------------------------------------------+
   |  Service Mesh (Istio): mTLS, Circuit Breaker, Retry, Timeout         |
   |  +----------+  +----------+  +----------+  +----------+  +---------+ |
   |  | Order    |  | Payment  |  | Inventory|  | User     |  | Notify  | |
   |  | Service  |  | Service  |  | Service  |  | Service  |  | Service | |
   |  | (Java 21 |  | (Node 20 |  | (Go 1.22 |  | (Python  |  | (Rust)  | |
   |  | Spring 3)|  | Express) |  | Gin)     |  |  FastAPI)|  | Actix)  | |
   |  +----+-----+  +----+-----+  +----+-----+  +----+-----+  +----+----+ |
   |       |             |             |             |             |      |
   |       |    +--------+-------------+-------------+--------+    |      |
   |       |    |  Event Bus: Apache Kafka (KRaft, 3 Brokers) |    |      |
   |       |    |  Topics: order.events, payment.events       |    |      |
   |       |    |  Partition: 12, Replication Factor: 3        |    |      |
   |       +----►  Exactly-Once Semantics (Idempotent Producer) ◄---+      |
   +--------------------+-------------------------------------------------+
                        |
   +--------------------v-------------------------------------------------+
   |  Data Tier (Polyglot Persistence)                                    |
   |  +--------------+ +--------------+ +--------------+ +-------------+ |
   |  | PostgreSQL   | | DynamoDB     | | Redis Cluster| | S3 / MinIO  | |
   |  | (RDS Aurora) | | (Key-Value)  | | (Session)    | | (Object)    | |
   |  | Multi-AZ     | | Global Table | | 6 Shards     | | Intelligent | |
   |  | Read Replica | | PITR 35일    | | Sentinel     | | Tiering     | |
   |  +--------------+ +--------------+ +--------------+ +-------------+ |
   +--------------------+-------------------------------------------------+
                        |
   +--------------------v-------------------------------------------------+
   |  Observability Stack: OpenTelemetry -> Prometheus + Grafana + Loki    |
   |  + Tempo + Alertmanager (SLO 기반 알림: Error Budget Burn Rate)      |
   +----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway** | 단일 진입점, 인증/인가, 트래픽 제어 | Kong/Envoy/AWS API Gateway, **OAuth 2.0 + JWT 검증**, Rate Limiting(Token Bucket 알고리즘, 예: 1000 RPS/IP), Circuit Breaker(Hystrix-Resilience4j, 실패율 50% 임계치 시 OPEN) |
| **Service Mesh** | 서비스 간 통신 제어, 관측성 | Istio/Linkerd, **mTLS 자동 발급**(SPIFFE ID: `spiffe://cluster.local/ns/default/sa/order-svc`), 사이드카 프록시(Envoy 1.29+), **트래픽 분할**(Canary 10%->50%->100%, Header-based routing) |
| **Container Orchestrator** | 컨테이너 라이프사이클 관리, 자동 확장 | Kubernetes 1.30+, **HPA**(메트릭: CPU/Memory/Custom Prometheus Adapter), **VPA**(Vertical Pod Autoscaler, 권장 리소스 자동 조정), **Karpenter**(노드 프로비저닝, Spot/On-Demand 혼합, Bin-packing), **Pod Disruption Budget**(PDB, minAvailable 50%) |
| **Event Streaming** | 비동기 메시징, 이벤트 소싱 | Apache Kafka 3.7+ (KRaft 모드, ZooKeeper 의존성 제거), **파티션 키 해싱**(동일 주문 ID 동일 파티션 보장), **Compacted Topic**(최신 상태 스냅샷), **Schema Registry**(Avro/Protobuf, backward compatibility 검증) |
| **Serverless/FaaS** | 이벤트 기반 코드 실행, 완전 관리형 | AWS Lambda/Azure Functions/Cloud Functions, **콜드 스타트 최적화**(Provisioned Concurrency, SnapStart, Custom Runtime), **동시성 제한**(Reserved Concurrency = 100, 계정 한도 1,000), **Lambda Extensions**(Datadog APM, Datadog 트레이서) |
| **Data Lake/Warehouse** | 대용량 분석, ETL/ELT | S3 + Athena(서버리스 SQL, Glue Data Catalog), **Delta Lake/Iceberg/Hudi**(ACID 트랜잭션, Time Travel), **Lakehouse 아키텍처**(Databricks, Apache Spark 3.5+ Photon 엔진), Columnar Format(Parquet/ORC) |
| **CI/CD & GitOps** | 지속적 통합/배포, 선언적 배포 | Argo CD/Flux, **Progressive Delivery**(Argo Rollouts, Flagger, AnalysisTemplate: Prometheus Success Rate ≥ 99%), **GitOps Sync Wave**(순차 배포: DB -> Backend -> Frontend), **OPA Gatekeeper/Kyverno**(Policy as Code) |

**핵심 알고리즘 및 파라미터**:
- **일관성 해싱 (Consistent Hashing)**: DynamoDB/Cassandra에서 데이터 분산. 키 공간을 0~2^160 원형에 매핑, 가상 노드(VNode) 16~256개로 키 공간 균등화. 노드 추가/제거 시 **약 1/N 키만 재배치**(N=노드 수).
- **벡터 시계 (Vector Clock)**: DynamoDB의 Causality Tracking. `[server, counter]` 쌍 배열로 인과관계 추적, 충돌 시 클라이언트가 Last-Write-Wins 또는 애플리케이션 로직으로 병합.
- **Raft 합의 알고리즘**: Kafka KRaft, etcd, Consul이 사용. Leader Election(과반수 투표, Election Timeout 150~300ms 랜덤 jitter), Log Replication(AppendEntries RPC), Snapshot/Compaction.
- **SLA 계산식**: 가용성 = (총 시간 - 다운타임) / 총 시간. 99.9%(3 nines) = 월 43.83분, 99.99%(4 nines) = 월 4.38분, 99.999%(5 nines) = 월 26.3초 허용 다운타임.
- **비용 최적화 공식**: TCO = CapEx(서버,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 635 / 800

<- **이전**: [634. 클라우드 아키텍처 핵심 토픽 634번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/634_cloud_architecture_core_topic_634_exam_summar/)
**다음**: [636. 클라우드 아키텍처 핵심 토픽 636번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/636_cloud_architecture_core_topic_636_exam_summar/) ->

---
