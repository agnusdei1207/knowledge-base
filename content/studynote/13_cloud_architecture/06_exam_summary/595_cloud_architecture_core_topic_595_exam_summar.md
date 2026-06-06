---
title: "Cloud Architecture Core Topic 595 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 5대 핵심 특성(탄력적 확장성, 종량 과금, 추상화된 인프라, API 기반 프로비저닝, 글로벌 가용성)과 4계층 서비스 모델(IaaS/PaaS/SaaS/FaaS) 위에 마이크로서비스, 이벤트 드리븐, 메시 기반 통합이 결합된 분산 시스템 설계 패러다임으로, AWS Well-Architected Framework의 6기둥(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화, 지속 가능성)이 평가 기준이다.
> 2. **가치**: 자본지출(CapEx)을 운영지출(OpEx)로 전환하여 TCO 30~40% 절감, Auto Scaling을 통한 트래픽 변동 대응력(평상시 30% 자원 대비 Peak 300% 대응), Multi-AZ 배포로 SLA 99.99%(연 52.6분 다운타임) 달성, Time-to-Market을 6~12개월에서 2~4주로 단축시킨다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs 멀티클라우드 전략, Stateful 워크로드의 Stateless 마이그레이션 여부, 동시성 모델(강일관성 vs eventual consistency) 선택, CAP 정리에 따른 트레이드오프, 그리고 12-Factor App 원칙 준수 수준이 아키텍처 성패를 결정한다.

---

## Ⅰ. 개요 및 필요성

클라우드 컴퓨팅은 NIST SP 800-145 정의에 따르면 "네트워크, 서버, 스토리지, 애플리케이션, 서비스 등 구성 가능한 컴퓨팅 자원의 공유 풀에 대해 어디서나 편리한 주문형 네트워크 액세스를 가능하게 하는 모델"이다. 2006년 AWS S3 출시와 EC2 베타 서비스를 시작으로, 현재는 Hyperscaler 3사(AWS, Azure, GCP)가 전 세계 IaaS 시장 점유율 약 65%를 점유하고 있으며(2024년 Gartner 기준), 한국은 네이버 클라우드, NHN Cloud, KT Cloud가 공공·금융 시장을 중심으로 성장 중이다.

기존 온프레미스 환경은 **프로비저닝 리드 타임 4~12주, 유휴 자원 60~80%, CAPEX 5~7년 회수**라는 구조적 한계를 가졌다. 트래픽 예측 실패로 인한 과잉 투자(평균 35%)와 Peak 시간대 장애가 반복되면서, 자원의 **탄력성(Elasticity)**과 **온디맨드 셀프서비스**가 필수 요구사항이 되었다. 2020년 코로나19 팬데믹 이후 디지털 전환 가속화로 전 세계 퍼블릭 클라우드 지출은 2024년 약 679조 원 규모로 성장했다.

```text
+-----------------------------------------------------------------+
|          전통 온프레미스 vs 클라우드 네이티브 비교               |
+-----------------------------------------------------------------+
|                                                                 |
|  [기존 모델]                      [클라우드 네이티브]           |
|  +-----------------+              +-----------------+          |
|  | Monolithic App  |              | Microservices   |          |
|  |   (단일 배포)   |              |  (독립 배포)    |          |
|  +--------+--------+              +--------+--------+          |
|           |                                |                   |
|  +--------v--------+              +--------v--------+          |
|  |  Bare Metal /   |              |  K8s/EKS/AKS    |          |
|  |  Hypervisor     |              |  Service Mesh   |          |
|  +--------+--------+              +--------+--------+          |
|           |                                |                   |
|  +--------v--------+              +--------v--------+          |
|  | SAN/NAS Storage |              | Object/S3/Blob  |          |
|  | (정적 용량)     |              | (무한 확장)     |          |
|  +--------+--------+              +--------+--------+          |
|           |                                |                   |
|  +--------v--------+              +--------v--------+          |
|  | 수동 장애 대응  |              | Auto Healing    |          |
|  |  (MTTR 4시간)  |              | (MTTR 30초)     |          |
|  +-----------------+              +-----------------+          |
|                                                                 |
|  CAPEX 80% / OPEX 20%              CAPEX 20% / OPEX 80%        |
|  스케일링: 수직 확장                스케일링: 수평 확장            |
|  배포 주기: 분기 1회               배포 주기: 일 10회+            |
+-----------------------------------------------------------------+
```

클라우드 아키텍처는 단순한 인프라 이전이 아니라, **장애를 전제로 한 설계(Design for Failure)**, **불변 인프라(Immutable Infrastructure)**, **선언적 API(Declarative API)**, **관측 가능성(Observability)**이라는 4대 새로운 사고방식을 요구한다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"호텔式的 숙박 시스템"**과 같다. 마치 호텔이 전체 객실을 미리 짓지 않고 예약 수요에 따라 즉시 객실을 배정하듯(탄력성), 전기·수도처럼 사용한 만큼만 청구하며(종량제), 전국 어디서나 같은 품질의 서비스를 받을 수 있다(추상화). 다만 호텔 선택이 한번 정해지면 옷장 크기, 와이파이 규격 등에 종속되듯, 클라우드 벤더 종속성 관리가 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **책임 공유 모델(Shared Responsibility Model)** 위에 5계층 기술 스택이 구성된다. 아래는 실무에서 가장 많이 사용되는 **3-Tier + Edge + Data 계층** 구조이다.

```text
+------------------------------------------------------------------+
|                    클라우드 네이티브 참조 아키텍처                |
+------------------------------------------------------------------+
|                                                                  |
|  [사용자 단말] ---DNS/Routing---► [CloudFront/Cloud CDN]         |
|                                          |                      |
|                                          v                      |
|   +------------------------------------------------------+      |
|   |  Layer 1: Edge & Delivery                            |      |
|   |  +- CDN (정적 콘텐츠 캐싱, TTL 86400s)              |      |
|   |  +- WAF (OWASP Top 10 방어, Rate Limit)             |      |
|   |  +- Global LB (Anycast IP, Geo-routing)             |      |
|   +--------------------+---------------------------------+      |
|                        v                                        |
|   +------------------------------------------------------+      |
|   |  Layer 2: API Gateway & Service Mesh                 |      |
|   |  +- API GW (Kong, AWS API GW, Apigee)              |      |
|   |  |   - Throttling, Auth, Routing                    |      |
|   |  +- Service Mesh (Istio/Linkerd, mTLS)              |      |
|   |  |   - Circuit Breaker, Retry, Timeout              |      |
|   |  +- Event Bus (Kafka, EventBridge, Pub/Sub)         |      |
|   +--------------------+---------------------------------+      |
|                        v                                        |
|   +------------------------------------------------------+      |
|   |  Layer 3: Compute (Stateless Microservices)          |      |
|   |  +- Container Orchestrator (EKS/AKS/GKE)            |      |
|   |  |   - Pod Auto-scaling (HPA: CPU>70%, Custom QPS)  |      |
|   |  +- Serverless (Lambda/Functions/Cloud Run)         |      |
|   |  |   - Cold Start (Lambda: 200~800ms, SnapStart)    |      |
|   |  +- HPA/KEDA/Cluster Autoscaler                     |      |
|   +--------------------+---------------------------------+      |
|                        v                                        |
|   +------------------------------------------------------+      |
|   |  Layer 4: Stateful & Data Tier                       |      |
|   |  +- RDBMS (Aurora MySQL, Cloud SQL)                 |      |
|   |  |   - Multi-AZ, Read Replica (5개까지)             |      |
|   |  +- NoSQL (DynamoDB, Cosmos DB, MongoDB Atlas)      |      |
|   |  |   - Partition Key 기반 자동 샤딩                 |      |
|   |  +- Cache (Redis/ElastiCache, Memcached)            |      |
|   |  |   - Read-through, Write-behind 패턴              |      |
|   |  +- Data Lake (S3+Glue+Athena, BigQuery)            |      |
|   +--------------------+---------------------------------+      |
|                        v                                        |
|   +------------------------------------------------------+      |
|   |  Layer 5: Cross-Cutting (Observability/Security)    |      |
|   |  +- Logging (CloudWatch, OpenSearch, Loki)          |      |
|   |  +- Metrics (Prometheus, CloudWatch, Datadog)       |      |
|   |  +- Tracing (Jaeger, X-Ray, Zipkin)                 |      |
|   |  +- IaC (Terraform, Pulumi, CloudFormation)         |      |
|   +------------------------------------------------------+      |
+------------------------------------------------------------------+
```

### 핵심 구성 요소 및 동작 원리

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Auto Scaling Group (ASG)** | 동적 인스턴스 수 조절 | CloudWatch Alarm(Metric: CPU>70%, Target Tracking) -> Launch Template 기반으로 신규 EC2/VM 기동. Scale-out Cooldown 300s, Scale-in 300s로 안정성 확보. Predictive Scaling은 ML 기반으로 2일 전 트래픽 예측 |
| **로드 밸런서 (L4/L7)** | 트래픽 분산 및 Health Check | L4(Network LB): TCP/UDP 레벨, 5-tuple 해시, 1초당 수백만 RPS 처리. L7(Application LB): HTTP 헤더/쿠키/Path 기반 라우팅, gRPC 지원, WebSocket. **Connection Draining 30s** 설정 필수 |
| **CQRS + Event Sourcing** | 읽기/쓰기 분리, 이벤트 기반 일관성 | Command 모델은 DynamoDB, Query 모델은 Elasticsearch 비동기 복제. Kafka 토픽으로 도메인 이벤트 발행, Outbox Pattern으로 트랜잭션 정합성 보장. Eventually Consistent 윈도우는 50~200ms |
| **Service Mesh (Istio)** | 마이크로서비스 간 통신 제어 | Sidecar(Envoy) 프록시로 mTLS 자동 적용, L7 메트릭 수집, Traffic Splitting(Canary 5%->25%->50%->100%), Fault Injection으로 카오스 엔지니어링 수행. Control Plane은 xDS API로 설정分发 |
| **Multi-Region Active-Active** | 글로벌 장애 대응 및 지연 시간 최소화 | Route 53 Latency-Based Routing 또는 AWS Global Accelerator. DynamoDB Global Tables(Multi-Region Replication, <1s lag), Aurora Global Database(Storage-based replication, <1s). RPO 0, RTO 30초 달성 |
| **Serverless (FaaS)** | 이벤트 기반 stateless 코드 실행 | Lambda: 1006MB 메모리, 15분 타임아웃, 6MB 동기 페이로드. Cold Start 해결: Provisioned Concurrency(상시 워밍), SnapStart(Java, <200ms), Lambda Warmer(Node.js 30초 ping). 동시성 Quota 관리(기본 1,000) |
| **Observability 3축** | 시스템 상태 가시화 | **Logs**(구조화 JSON, 중앙 수집), **Metrics**(RED: Rate/Error/Duration, USE: Utilization/Saturation/Errors), **Traces**(OpenTelemetry 표준, W3C Trace Context, sampling 1% 권장). SLO/Error Budget 기반 알람 |

### 분산 시스템 핵심 알고리즘 및 파라미터

**CAP 정리**: 일관성(C), 가용성(A), 분할 내성(P) 중 2개만 보장 가능. 클라우드 환경은 P가 필수이므로, **CP 시스템**(etcd, ZooKeeper, HBase, MongoDB 기본) vs **AP 시스템**(Cassandra, DynamoDB, Riak) 중 비즈니스 요구에 따라 선택한다.

**컨시스턴시 해시 링(Consistent Hashing)**: DynamoDB, Cassandra의 분산 스토리지 샤딩 알고리즘. 가상 노드(Virtual Node) 256개로 키-노드 매핑하여 노드 추가/제거 시 재분배를 1/N 수준으로 제한. **리플리카 팩터(RF) 3**이 표준.

**Quorum 기반 합의**: W+R>N 공식. W(쓰기 Quorum)=2, R(읽기 Quorum)=2, N(리플리카)=3이면 Strong Consistency. Sloppy Quorum + Hinted Handoff로 장애 시 가용성 확보.

**서킷 브레이커 패턴**: Hystrix/Resilience4j 기반. Closed(정상) -> Open(차단, 5초) -> Half-Open(테스트). 임계값: Error Rate >50%, Sliding Window 10s, Slow Call Duration >2s.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"대도시 지하철 시스템"**과 같다. 각 노선(마이크로서비스)이 독립적으로 운행되면서도 환승센터(API Gateway)에서 연결되고, 배차 간격(Auto Scaling)이 수요에 따라 자동 조절되며, 일부 구간 장애 시 다른 노선으로 우회(서킷 브레이커)할 수 있다. 가장 중요한 것은 **"한 곳이 막혀도 전체가 멈추지 않는 설계"**이다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처를 논할 때 혼동되기 쉬운 핵심 개념들을 명확히 구분해야 한다.

| 구분 | **IaaS (EC2, Compute Engine)** | **PaaS (Beanstalk, App Engine)** | **SaaS (Office 365, Salesforce)** | **FaaS (Lambda, Cloud Functions)** |
| :--- | :--- | :--- | :--- | :--- |
| **제어 범위** | OS, 미들웨어, 런타임, 데이터, 앱 | 앱, 데이터 | 설정·사용자 데이터만 | 코드(함수)만 |
| **책임 분담** | 고객: OS 패치, 미들웨어 | 고객: 앱, 데이터 | 제공자: 전부 | 고객: 코드 의존성 |
| **확장 단위** | 인스턴스(VM) | 애플리케이션 인스턴스 | 자동(사용자) | 함수 호출 단위 |
| **Cold Start** | 없음(상시 기동) | 없음(Warmer) | 없음 | 200ms~5s |
| **최대 실행 시간** | 무제한 | 무제한 | - | 15분(Lambda) |
| **요금 모델** | 인스턴스 시간 | 인스턴스 시간 | 사용자 라이선스 | 호출 수 × 실행 시간(ms) |
| **적합 워크로드** | 레거시, Stateful, 커스텀 | 웹앱 표준 배포 | 일반 업무 | 이벤트 처리, ETL, Webhook |
| **Lock-in 위험** | 중간 | 높음 | 매우 높음 | 높음 |

| 구분 | **Monolithic** | **Microservices** | **Serverless** |
| :--- | :--- | :--- | :--- |
| **배포 단위** | 1개 프로세스 | 10~500개 서비스 | 함수 수천 개 |
| **확장성** | 전체 복제 | 서비스별 독립 | 호출 단위 자동 |
| **장애 격리** | 약함(1개 실패=전체) | 강함(서킷 브레이커) | 강함(함수별 격리) |
| **데이터 일관성** | 단일 트랜잭션 | Saga/Eventual | Idempotency + Outbox |
| **개발 조직** | 1~50명 | 50~500명(Conway
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 595 / 800

<- **이전**: [594. 클라우드 아키텍처 핵심 토픽 594번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/594_cloud_architecture_core_topic_594_exam_summar/)
**다음**: [596. 클라우드 아키텍처 핵심 토픽 596번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/596_cloud_architecture_core_topic_596_exam_summar/) ->

---
