---
title: "581. 클라우드 아키텍처 핵심 토픽 581번 시험 요약 (Cloud Architecture Core Topic 581 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 가상화·컨테이너·오케스트레이션·서비스 메시·서버리스·IaC(Infrastructure as Code)를 기반으로 한 **탄력적 분산 컴퓨팅 패러다임**이며, Well-Architected Framework(보안·안정성·성능 효율·비용 최적화·운영 우수성·지속 가능성) 6대 축 위에서 워크로드의 요구사항을 SLA/SLO로 정량화하여 설계하는 것이 핵심이다.
> 2. **가치**: Capital Expenditure(CapEx)를 Operational Expenditure(OpEx)로 전환하여 약 30~70%의 TCO 절감을 달성하고, Auto-Scaling·Multi-AZ 배포·Chaos Engineering을 통해 가용성 99.99%(연 52.6분 이내 장애) 수준을 구현하며, Time-to-Market를 온프레미스 대비 1/5 수준으로 단축할 수 있다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs Multi/Hybrid Cloud, EKS·AKS·GKE·GKS 같은 관리형 K8s vs Self-Managed K8s, Monolith -> Microservices -> Serverless로의 점진적 분해, 동기(HTTP/REST/gRPC) vs 비동기(EventBridge/Kafka/SQS) 통신 모델, CAP/ACID/BASE 트레이드오프, Spot·Reserved·On-Demand 인스턴스 조합 비율(통상 50:30:20) 결정이 기술사 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

클라우드 아키텍처는 NIST SP 800-145 기준에 따라 **온디맨드 셀프서비스, 광범위한 네트워크 접근, 리소스 풀링, 빠른 탄력성, 측정 가능한 서비스**의 5대 필수 특성과 **Public·Private·Hybrid·Community** 4가지 배포 모델, **IaaS·PaaS·SaaS·FaaS·DaaS·CaaS** 6가지 서비스 모델로 분류된다. 2006년 AWS S3·EC2 출시 이후 20년 동안 IT 인프라의 패러다임은 **Mainframe -> Client/Server -> 3-Tier Web -> SOA -> Cloud-Native(Microservices + Containers + DevOps)**로 진화했으며, 2024년 기준 전 세계 퍼블릭 클라우드 시장 규모는 약 6,800억 USD로 전년 대비 20% 성장하였다( Gartner 2024 ). 국내는 클라우드 컴퓨팅 발전법(2021), 클라우드 보안인증제도(CSAP) 등 규제 정비가 완료되어, 공공·금융권의 도입이 가속화되고 있다.

기존 온프레미스 환경은 **수직 확장(Scale-Up) 한계, Capacity Planning 실패, Idle Resource 낭비(평균 20~30%), Disaster Recovery RTO/RPO 미흡, CapEx 중심의 무거운 의사결정**이라는 구조적 한계를 지녔다. 클라우드 아키텍처는 이를 **수평 확장(Scale-Out), Pay-as-you-go, Multi-AZ/Region HA, OpEx 기반 Agile 비용 모델, API 기반 셀프프로비저닝**으로 전환하여, 비즈니스 변동성에 IT가 능동적으로 대응할 수 있는 기반을 제공한다. 또한 12-Factor App, Beyond the 12-Factor App, Cloud Native Computing Foundation(CNCF) Trail Map 등의 표준화된 설계 원칙이 성숙 단계에 진입하여, 기술사 시험에서 클라우드 네이티브 아키텍처 설계 역량을 검증하는 비중이 매년 확대되고 있다.

```text
[기존 온프레미스 vs 클라우드 네이티브 아키텍처 진화도]

  +--------------------------+         +--------------------------------------+
  |  On-Premise (Past)       |   ->->->   |  Cloud-Native (Present/Future)        |
  +--------------------------+         +--------------------------------------+
  | • 전용 HW 서버/스토리지  |         | • 가상화 -> 컨테이너 -> 서버리스       |
  | • 수직확장(Scale-Up)     |         | • 수평확장(Scale-Out) + Auto-Scaling |
  | • 수동 Capacity 계획     |         | • Metric 기반 Elastic Provisioning   |
  | • 수개월 배포 사이클      |         | • CI/CD 기반 수분~수시간 배포        |
  | • 라이선스/계약 종속     |         | • API 기반 셀프서비스 + IaC          |
  | • CAPEX 중심 (HW 투자)  |         | • OPEX 중심 (사용량 과금)            |
  | • DR Site 별도 구축      |         | • Multi-AZ/Region 기본 제공          |
  | • Monolith + RDBMS      |         | • Microservices + Polyglot Persistence|
  +--------------------------+         +--------------------------------------+
              |                                       |
              v                                       v
    [연간 CAPEX 100억,                    [사용량 기반 과금, Scale-to-Zero,
     3년 감가상각, 유휴율 25%]            Pay-per-Request, Cold Start 최적화]
```

- **📢 섹션 요약 비유**: 온프레미스는 "집을 직접 짓고 유지보수하는 소유"이고, 클라우드 네이티브는 "필요한 만큼 호텔 룸을 빌리고, 체크아웃하면 비용이 0원이 되는 빌린 삶의 방식"이다. 호텔은 공사·청소·보안·전기·수도 모두 책임지며, 손님은 비즈니스(핵심 로직)에만 집중한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심 메커니즘은 **① 가상화 및 컨테이너화를 통한 리소스 추상화 -> ② 오케스트레이터(Kubernetes)가 선언적(desired state) 모델로 워크로드 배치·복제·자가치유 -> ③ 서비스 메시(Istio/Linkerd/Consul)가 L7 트래픽·mTLS·관측가능성 제공 -> ④ API Gateway·Service Discovery가 외부 트래픽 라우팅 -> ⑤ IaC(Terraform/Pulumi/CloudFormation)가 인프라를 코드로 선언 -> ⑥ GitOps(ArgoCD/Flux)가 선언적 배포 자동화**의 6계층으로 구성된다. 이 모든 계층은 **OpenTelemetry 기반의 통합 관측가능성(Observability)** — Metrics(예: Prometheus + Grafana), Logs(예: Loki/ELK), Traces(예: Jaeger/Tempo) — 으로 연결되어 SRE가 MTTR(Mean Time To Recover)을 최소화한다.

아래는 **Multi-Account, Multi-Region, Multi-AZ, EKS 기반 표준 참조 아키텍처(Reference Architecture)** 이다.

```text
[클라우드 네이티브 3-Tier + EKS + Observability 참조 아키텍처]

                          +-----------------------------------------+
                          |       Global Edge / CDN Layer           |
                          |   CloudFront / Cloudflare / Akamai      |
                          |   (WAF + DDoS Shield + Bot Management)  |
                          +-------------+---------------------------+
                                        | TLS 1.3, HTTP/2, HTTP/3 (QUIC)
                                        v
                          +-----------------------------------------+
                          |   API Gateway / Application Load Balancer|
                          |   - Rate Limiting, JWT, OAuth2.1/OIDC   |
                          |   - Canary 5% -> 25% -> 50% -> 100%       |
                          +-------------+---------------------------+
                                        |
                +-----------------------+-----------------------+
                v                       v                       v
       +-----------------+    +-----------------+    +-----------------+
       |  EKS Pod (Svc A)|    |  EKS Pod (Svc B)|    |  EKS Pod (Svc C)|
       |  - HPA: CPU 70% |    |  - KEDA Event   |    |  - Karpenter    |
       |  - PDB: min 2   |    |  - SQS/Kafka    |    |  - Spot Mix      |
       +--------+--------+    +--------+--------+    +--------+--------+
                | gRPC/HTTP2           | Async                | GraphQL
                | mTLS (Istio)         | Kafka/MSK            |
                v                      v                      v
       +-----------------+    +-----------------+    +-----------------+
       |  Aurora PostgreSQL |  |  DynamoDB       |    |  ElastiCache    |
       |  Multi-AZ + R/O   |  |  Global Tables  |    |  Redis Cluster  |
       |  ProxySQL/RDS Proxy| |  On-Demand/Prov |    |  (Session/Cache)|
       +--------+--------+    +--------+--------+    +--------+--------+
                |                      |                      |
                +----------------------+----------------------+
                                       v
                          +-----------------------------------------+
                          |   Observability Stack (OpenTelemetry)   |
                          |  Prometheus + Grafana + Loki + Tempo    |
                          |  + CloudWatch/X-Ray + Datadog/NewRelic  |
                          |  + PagerDuty (Incident Response)        |
                          +-----------------------------------------+
                                       |
                                       v
                          +-----------------------------------------+
                          |   IaC + GitOps                          |
                          |  Terraform -> Atlantis -> ArgoCD -> EKS    |
                          |  Policy: OPA/Gatekeeper + Conftest      |
                          |  SBOM: Sigstore/Cosign (이미지 서명)     |
                          +-----------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 계층 (Compute)** | 워크로드 실행 환경 추상화 | EC2(가상머신) -> ECS/EKS(컨테이너) -> Lambda/Functions(서버리스) -> Fargate(컨테이너 서버리스) 순으로 추상화 레벨 상승. AWS Graviton3(ARM64), Intel Sapphire Rapids, AMD EPYC Genoa 등 인스턴스 패밀리별 CPU·메모리·네트워크 성능 특성(M5: 균형, C5: 컴퓨트, R5: 메모리, I3: I/O)에 따라 워크로드 매핑. |
| **오케스트레이션 (K8s)** | 컨테이너 자동 배치·복제·자가치유 | Kubernetes Control Plane(etcd + kube-scheduler + controller-manager)이 **Desired State ↔ Actual State** 차이를 reconcile(기본 5s). Deployment, StatefulSet(순서 보장·영구 볼륨), DaemonSet(노드당 1개), Job/CronJob(배치) 워크로드 타입별 사용. Pod Disruption Budget(minAvailable), Topology Spread Constraints, Taint/Toleration, Node Affinity로 가용성·성능 튜닝. |
| **서비스 메시 (Service Mesh)** | L7 트래픽 관리·mTLS·관측가능성 | Istio/Linkerd/Consul Connect가 사이드카 프록시(Envoy)로 모든 Pod 간 통신을 가로채 mTLS(STRICT 모드), Retry(지수 백오프), Circuit Breaker, Traffic Splitting을 코드 변경 없이 적용. Ambient Mesh(2024 GA)는 사이드카 제거로 지연 30~50% 개선. |
| **API Gateway / Ingress** | 외부 트래픽 진입점 정책 | AWS API Gateway(엔터프라이즈), Kong(고성능 Lua 플러그인), Apigee(분석), NGINX Ingress(K8s 표준), Traefik, Envoy Gateway(2024). 기능: Rate Limit(Token Bucket), Quota, Transformation, OAuth 2.1, WebSocket, GraphQL Federation, AsyncAPI/Webhook. |
| **데이터 계층 (Data)** | Polyglot Persistence | RDB(Aurora/MySQL), NoSQL(DynamoDB·Cassandra·MongoDB), Cache(Redis·Memcached), Search(OpenSearch·Elasticsearch), Warehouse(Redshift·Snowflake·BigQuery), Lake(S3+Iceberg/Delta/Hudi). CAP Trade-off: DynamoDB는 AP, Cosmos DB는 tunable consistency, Spanner는 CP+Global Strong. |
| **관측가능성 (Observability)** | 시스템 상태 가시화·장애 대응 | 3 Pillars: **Metrics**(시계열·Cardinality 주의) + **Logs**(구조화 JSON) + **Traces**(분산 컨텍스트 전파 W3C TraceContext). SLI/SLO/Error Budget 기반 SRE 운영. RED Method(Rate·Error·Duration), USE Method(Utilization·Saturation·Error). |

**핵심 알고리즘·파라미터**:
- **Auto-Scaling 정책**: HPA는 `targetMetric: cpu=70%` 또는 KEDA가 SQS 큐 길이·Kafka Lag·cron 스케줄 기반 이벤트 드리븐 스케일링. Karpenter(2023 GA)는 Spot/O(n-demand) 혼합, Bin-packing, Node TTL(기본 30s)까지 자동화.
- **리소스 요청·제한**: `requests`는 스케줄링·Quota 산정, `limits`는 cgroup 강제. JVM/HPA 환경에서는 `requests=limits`로 설정해야 HPA 정확도 향상. `LimitRange` + `ResourceQuota`로 Namespace별 가드레일.
- **배포 전략**: Recreate(다운타임 O) -> RollingUpdate(maxUnavailable=0, maxSurge=1, 기본) -> Blue/Green(라우터 스왑) -> Canary(Istio VirtualService weight 5->25->50->100) -> A/B(헤더 기반) -> Feature Flag(LaunchDarkly·Unleash) -> Shadow/Mirror.
- **가용성 수식**: 99.9%(Three 9s)=연 8.77시간, 99.95%=연 4.38시간, 99.99%(Four 9s)=연 52.6분, 99.999%(Five 9s)=연 5.26분. 가용성 = MTBF/(MTBF+MTTR). MTTR 50% 절감 시 동일 SLA 대비 MTBF 여유 2배.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "오케스트라"와 같다. Kubernetes가 지휘자(컨덕터)이고, 각 Pod는 악기 연주자, 서비스 메시는 악보 가이드(파트·음정·속도), API Gateway는 객석 안내 방송, Observability는 청중석에서 음 하나하나의 박자를 잡아주는 녹음 장비, IaC는 전체 공연 매뉴얼이다. 한 명만 어긋나도 화음이 무너지므로 **표준화된 매뉴얼 + 실시간 모니터링**이 필수다.

---

## Ⅲ. 비교 및 연결

| 구분 | **Monolith + On-Premise** | **Microservices + Cloud-Native** | **Serverless / FaaS** |
| :--- | :--- | :--- | :--- |
| **배포 단위** | WAR/EAR 통째로 (수GB) | 컨테이너 이미지 (수백 MB) | 함수 코드 ZIP (수 MB) |
| **확장 단위** | VM 수직 확장 (Scale-Up) | Pod 수평 확장 (Scale-Out) | 동시 실행 수 (Concurrency) |
| **배포 주기** | 월~분기 1회 (Waterfall) | 일~시간 단위 (CI/CD) | 수 초~수 분 (Event-driven) |
| **장애 전파** | 단일 프로세스 -> 전체 다운 | Circuit Breaker + Bulkhead 격리 | 자동 재시도 + DLQ |
| **트랜
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 581 / 800

<- **이전**: [580. 클라우드 아키텍처 핵심 토픽 580번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/580_cloud_architecture_core_topic_580_exam_summar/)
**다음**: [582. 클라우드 아키텍처 핵심 토픽 582번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/582_cloud_architecture_core_topic_582_exam_summar/) ->

---
