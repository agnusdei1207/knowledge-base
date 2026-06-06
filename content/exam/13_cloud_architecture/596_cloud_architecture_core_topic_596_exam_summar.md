---
title: "Cloud Architecture Core Topic 596 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 퍼블릭·프라이빗·하이브리드 클라우드 위에서 IaaS/PaaS/SaaS/FaaS 계층을 분해하고, 컨테이너·서비스 메시·GitOps·IaC로 구성요소를 코드화·자동화·관측가능하게 만드는 **분산 시스템 아키텍처 패턴의 총합**이다.
> 2. **가치**: Auto Scaling으로 트래픽 피크 대비 CAPEX->OPEX 전환, MTTR 단축(관측성), 배포 리드타임 90% 이상 감소(GitOps), 가용성 99.99% SLA 달성을 통한 **TCO 30~60% 절감과 비즈니스 민첩성** 확보.
> 3. **판단 포인트**: 12-Factor/카나리/Blue-Green 같은 분산 트랜잭션 패턴, CAP 정리·Quorum·Consistent Hashing 기반의 데이터 정합성, **Cloud Native vs Lift&Shift** 트레이드오프, 그리고 Shared Responsibility Model의 경계 설정이 핵심 의사결정 변수.

---

## Ⅰ. 개요 및 필요성

클라우드 컴퓨팅은 NIST SP 800-145 정의에 따라 "네트워크, 서버, 스토리지, 애플리케이션, 서비스 등 구성 가능한 컴퓨팅 자원의 공유 풀에 대한 편리한 온디맨드 네트워크 액세스"로 정의된다. 2006년 AWS S3/EC2 출시 이후 클라우드는 단순한 가상호스팅을 넘어 **클라우드 네이티브(Cloud Native)** 패러다임으로 진화했다. CNCF(Cloud Native Computing Foundation)는 2015년 설립 이후 Kubernetes, Prometheus, Envoy, Istio, ArgoCD 등 핵심 프로젝트를 표준화하며, **컨테이너 오케스트레이션 + 선언적 API + 불변 인프라(Immutable Infrastructure)**를 3대 축으로 자리잡았다.

전통적 모놀리식(On-Premise) 아키텍처는 수직 확장(Scale-Up) 한계, 수개월의 배포 주기, HW 장애 시 수시간 RTO, CAPEX 중심의 비용 구조라는 4대 고질적 문제를 안고 있었다. 클라우드 아키텍처는 이를 **수평 확장(Scale-Out) + 마이크로서비스 + IaC + 관측성(Observability)** 4요소로 해체한다.

```text
[전통적 아키텍처]                              [클라우드 네이티브 아키텍처]
+----------------------+                +------------------------------+
|   Monolithic App     |                |   API Gateway / Service Mesh|
|  +----------------+  |                | +--------+ +--------+ +----+|
|  | UI + Biz + DB  |  |   --->         | |Svc A   | |Svc B   | |Svc C||
|  |   (단일 JVM)   |  |                | +--------+ +--------+ +----+|
|  +----------------+  |                |   |    |       |     |      |
|   v 수직확장 한계     |                |   v    v       v     v      |
|   Big HW Box        |                | [K8s Pod] [Pod]  [Pod]  [Pod]|
+----------------------+                |   v        v      v      v   |
                                         | [Container Runtime: containerd]
                                         |   v        v      v      v   |
                                         | [OS: Bottlerocket / Flatcar] |
                                         | +--------------------------+ |
                                         | | EKS / AKS / GKE / Self    | |
                                         | +--------------------------+ |
                                         +------------------------------+
   * 배포주기: 분기 1회                              * 배포주기: 하루 수십~수백회
   * 장애영향: 100% 서비스 중단                       * 장애영향: Pod 단위 격리
   * 트래픽피크: HW 사전 구매 필요                    * AutoScaler로 자동 대응
```

**왜 클라우드 아키텍처인가?** 비즈니스 트래픽이 비선형(Daily 5x, Promo Day 50x) 패턴을 보이는 환경에서, **탄력성(Elasticity)**과 **관측가능성(Observability)**은 곧 매출과 직결된다. Netflix는 2017년경 AWS Chaos Monkey -> Chaos Engineering으로 전환, AWS 리전 장애 시에도 99.99% 가용성을 유지한 사례가 그 대표적이다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **"전기를 직접 발전하지 않고 수도꼭지를 틀면 즉시 쓰는 스마트 그리드"**와 같다. 발전기(On-Premise HW)는 직접 관리하지만, 클라우드에서는 수요-공급을 자동 조절하는 그리드 컨트롤러(Kubernetes HPA/Cluster Autoscaler)만 신뢰하면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **계층화된 책임 분담(Shared Responsibility Model)**과 **선언적(Declarative) 제어**이다. 아래는 4계층 참조 아키텍처이다.

```text
                       +-------------------------------------+
   [사용자/디바이스]     |   CDN (CloudFront/AKAMAI/Cloud CDN)| <- Edge / WAF
                       +------------+------------------------+
                                    | HTTPS/TLS 1.3
                       +------------v------------------------+
   [트래픽 계층]        |   L7 Load Balancer (ALB/NLB/GLB)   |
                       |   + API Gateway (Kong/Apigee/AWS)  |
                       +------------+------------------------+
                                    | mTLS via Service Mesh
                       +------------v------------------------+
   [플랫폼 계층]        |   Kubernetes Service Mesh (Istio)  |
                       |   +-----+ +-----+ +-----+ +-----+|
                       |   |Pod A| |Pod B| |Pod C| |Pod D|| <- Sidecar Envoy
                       |   +-----+ +-----+ +-----+ +-----+|
                       |   HPA / VPA / KEDA / Karpenter     |
                       +------------+------------------------+
                                    | gRPC / REST / Async (Kafka)
                       +------------v------------------------+
   [데이터 계층]        |  Polyglot Persistence              |
                       |  RDBMS (Aurora) + NoSQL (DynamoDB) |
                       |  + Cache (Redis) + Search (OpenSearch)|
                       |  + Lakehouse (Iceberg/Delta) + S3  |
                       +------------+------------------------+
                                    |
                       +------------v------------------------+
   [운영/거버넌스 계층]  |  IaC (Terraform/ Pulumi)           |
                       |  GitOps (ArgoCD/Flux)               |
                       |  Observability (OTel -> Prom/Grafana)|
                       |  Security (Trivy, OPA, Falco, Vault)|
                       +-------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway / L7 LB** | 외부 트래픽 진입점, 인증·라우팅·속도제한 | AWS ALB는 OIDC 통합, Kong은 Lua 플러그인, Envoy는 xDS API로 동적 구성. Round Robin 외에 **EWMA, Least Connections, P2C(Power of Two Choices)** 알고리즘 적용 |
| **Kubernetes Control Plane** | 컨테이너 스케줄링·자가치유·오토스케일링 | Kube-Scheduler가 Bin-packing, Taints/Tolerations, Node Affinity로 Pod 배치. **etcd**는 Raft 합의 알고리즘으로 강한 일관성 보장, Quorum = ⌊N/2⌋+1 |
| **Service Mesh (Istio/Linkerd)** | 서비스 간 mTLS, 트래픽 관리(카나리/서킷브레이커) | **Envoy Sidecar**가 1:1로 Pod에 주입되어 L4/L7 프록시 역할. xDS API로 CDS/EDS/LDS/RDS 동적 푸시, **Istiod**가 Citadel(CA) + Pilot(Control) + Galley(Config) 통합 |
| **관측성 스택 (OpenTelemetry)** | Metrics·Logs·Traces 통합 수집 | **OTel Collector**가 OTLP 프로토콜로 수신, **3 Signal**: Prometheus(메트릭, Counter/Gauge/Histogram), Loki(로그, 라벨 인덱싱), Tempo/Jaeger(분산 트레이스, TraceID/SpanID 상관) |
| **데이터 계층 (Polyglot)** | 트래픽 특성에 맞는 DB 선택 | **CQRS + Event Sourcing**: 쓰기는 RDBMS(Aurora), 읽기는 ElasticSearch, 캐시는 Redis Cluster(Consistent Hashing 16384 slot). **Saga Pattern**으로 분산 트랜잭션 보상 트랜잭션 처리 |
| **IaC + GitOps** | 인프라/앱 모두 코드로 선언 | Terraform은 HCL로 Plan->Apply, Pulumi는 일반 언어(TS/Python). **ArgoCD**가 Git Repo ↔ K8s Cluster 상태 동기화(Sync Wave, Prune, Self-Heal) |

**핵심 알고리즘 및 파라미터 심화:**

- **Consistent Hashing**: 캐시 노드 추가/제거 시 키 재배치 비율을 O(K/N) -> O(K/N) 수준으로 유지. Virtual Node(VNode) 150~200개로 핫스팟 완화. DynamoDB는 SHA-1 기반 128-bit 해시 + 256개 VNode.
- **CAP 정리와 실전 트레이드오프**: CP 시스템(etcd, ZooKeeper)은 네트워크 분할 시 일관성 우선, AP 시스템(Cassandra, DynamoDB)는 가용성 우선 -> **Tunable Consistency**(W+R>N)로 강도 조절.
- **HPA 공식**: `desiredReplicas = ceil(currentReplicas * (currentMetricValue / desiredMetricValue))`. KEDA는 이벤트 소스(Kafka Lag, SQS Queue, Cron) 기반 0->N 스케일링.
- **Circuit Breaker 상태기계**: CLOSED(정상) -> OPEN(차단, 5xx 임계치 초과) -> HALF_OPEN(일부 트래픽 시험) -> CLOSED. Resilience4j의 `failureRateThreshold`, `waitDurationInOpenState` 튜닝.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"도시의 상하수도·전기·교통 인프라"**와 같다. 각각의 처리장치(데이터센터)가 분산되어 있고, 도시 운영청(Kubernetes)이 수요에 맞춰 공급을 조정하며, 시민(개발자)은 관로·배선(API)만 신뢰하면 된다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처는 유사·대체 개념들과 명확히 구분되어야 한다.

| 구분 | **모놀리식 아키텍처** | **마이크로서비스 아키텍처** | **서버리스(FaaS) 아키텍처** |
| :--- | :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/EAR, 1~10GB | 컨테이너 이미지, 100~500MB | 함수 코드, ZIP/KB~MB |
| **확장 단위** | 애플리케이션 전체 복제 | 서비스 단위 수평확장 | 함수 호출 단위 자동확장 |
| **장애 격리** | 프로세스 1개 -> 전사 영향 | 서비스 단위 격리, Bulkhead 적용 | 함수 단위 격리, Cold Start 존재 |
| **데이터 관리** | 단일 RDBMS, ACID 보장 | DB per Service, Saga/CQRS 필요 | Stateful 어려움, 외부 저장소 필수 |
| **적합 워크로드** | CRUD 단순 업무, 레거시 | 고트래픽/고가용성, 도메인 복잡 | 스파이크성, 이벤트 기반, IoT |
| **대표 기술** | Spring Boot 단일 JAR | Spring Cloud, Istio, K8s | AWS Lambda, Azure Functions |
| **운영 복잡도** | 낮음 (1팀) | 높음 (SRE + DevOps) | 중간 (벤더 종속, Cold Start) |
| **TCO (3년)** | 높음 (HW 라이센스) | 중간 (인건비^, 인프라v) | 낮음 (사용량 과금, 0 idle) |
| **Cold Start** | 없음 | 수초~수십초 (이미지 pull) | 100ms~수초 (Init Phase) |
| **State 관리** | JVM Heap | Redis/DB 외부화 | DynamoDB/Step Functions |

**배포 모델 비교 (Public/Private/Hybrid/Multi-Cloud):**

| 기준 | Public | Private | Hybrid | Multi-Cloud |
| :--- | :--- | :--- | :--- | :--- |
| **소유** | Hyperscaler | 자체/전용 | Public+Private | 2개 이상 Public |
| **컴플라이언스** | 글로벌 인증 多 | 데이터 주권 확보 | 온프레 데이터 보존 | 벤더 종속 회피 |
| **확장성** | 무제한 | 제한 | 버스트 확장 | 리전 장애 대비 |
| **비용** | OPEX, 종량제 | CAPEX 多 | CAPEX+OPEX | 복잡한 비용 최적화 |
| **네트워크** | Internet | 전용선 | Direct Connect/ExpressRoute | Inter-Cloud Peering |

**연계 기술 스택:**

- **데이터**: Kafka(Knative Eventing), Debezium(CDC), Apache Flink(실시간 스트림 처리)
- **AI/ML**: Kubeflow, SageMaker, Vertex AI — MLOps 파이프라인 (Feature Store -> Training -> Serving)
- **엣지**: KubeEdge, OpenYurt — 클라우드 컨트롤 플레인이 엣지 노드까지 확장
- **보안**: SPIFFE/SPIRE (Workload Identity), OPA/Gatekeeper (Policy as Code), Confidential Computing (Intel SGX, AMD SEV)

- **📢 섹션 요약 비유**: 모놀리식은 **"1층짜리 단독주택"**, 마이크로서비스는 **"아파트 단지(각 동이 독립)", 서버리스는 "호텔(필요한 방만 빌림)"**이다. 상황에 따라 거주 형태를 바꿔야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

기술사 시험에서 단순 암기형이 아닌 **트레이드오프와 의사결정 근거**를 요구한다. 실무 적용 시 다음 체크리스트가 결정적이다.

### 기술사형 판단 체크리스트

1. **워크로드 분류**: ① OLTP(낮은 지연, ACID), ② OLAP(고吞吐, 컬럼형), ③ Batch(높은 지연 OK), ④ Streaming(낮은 지연, 무한 데이터) — 각각 적합한 컴퓨팅(EC2/EKS/Lambda/EMR) 선택
2. **배포 전략 선택**: Rolling(점진, 다운타임 無) vs Blue-Green(이중화, 즉시 롤백) vs Canary(1%->10%->100%, 위험 최소화) — Feature Flag(LaunchDarkly)와 Metric 기반 진행
3. **데이터 정합성 전략**: 강한 일관성 필요 -> RDBMS(Aurora) + 2PC 또는 Outbox Pattern; 약한 일관성 OK -> DynamoDB + SQS + 보상 트랜잭션(Saga Choreography/Orchestration)
4. **비용 최적화**: Compute Savings Plans(1~3년 약정 30~60%v), Spot Instance(70~90%v, Fault-Tolerant 워크로드 한정), S3 Intelligent-Tiering(스토리지 자동 계층화), Reserved Capacity(예측 가능 부하)
5. **재해복구(DR) 전략**: RPO/RTO 목표에 따라 Pilot Light(<10분 RTO), Warm Standby(<1분), Multi-Region Active-Active(0) 선택 — **CRUD 비율·데이터 전송 비용**까지 계산

### 피해야 할 안티패턴

- **Distributed Monolith**: 마이크로서비스로 분리했으나 동기 HTTP 호출 체인(5+ hop)으로 결합 -> 장애 전파, Latency 누적. **해결**: 비동기 메시지 + Bulkhead + Timeout 계층화(1s->2s->4s)
- **Chatty I/O**: 서비스 간 1요청 수십 회 마이크로콜 -> 네트워크 비용 폭증. **해결**: BFF(Backend For Frontend) 패턴, GraphQL로 콜리싱
- **Cloud Lock-in 무시**: AWS 고유 서비스(S3, DynamoDB) 전면 사용 -> 이관 비용 막대. **해결**: Hexagonal Architecture(Port/Adapter), Strangler Fig Pattern으로 점진적 분리
- **관측성 부재**: 로그만 수집, 분산 트레이스 없음 ->
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 596 / 800

<- **이전**: [595. 클라우드 아키텍처 핵심 토픽 595번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/595_cloud_architecture_core_topic_595_exam_summar/)
**다음**: [597. 클라우드 아키텍처 핵심 토픽 597번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/597_cloud_architecture_core_topic_597_exam_summar/) ->

---
