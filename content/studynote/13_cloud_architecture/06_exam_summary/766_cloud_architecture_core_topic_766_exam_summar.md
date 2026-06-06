---
title: "Cloud Architecture Core Topic 766 Exam Summary"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 가상화·컨테이너·오케스트레이션(Kubernetes)·서비스 메시(Istio/Linkerd)·서버리스(Lambda/Cloud Functions)를 기반으로 한탄력적·분산·자가치유 컴퓨팅 자원의 추상화 계층이며, NIST SP 800-145의 5대 특성(온디맨드 셀프서비스, 광역 네트워크 접근, 자원 풀링, 빠른 탄력성, 측정 가능한 서비스)을 SLA·API·IaC(Terraform/CloudFormation)로 구현한 시스템 디자인 패러다임이다.
> 2. **가치**: AWS Well-Architected Framework 5대 기둥(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화) 적용 시CAPEX->OPEX 전환으로 인프라 TCO 30~60% 절감, 오토스케일링으로 트래픽 피크 시 응답 지연 P99 50% 개선, 글로벌 멀티 리전 Active-Active 구성으로 RTO < 1분·RPO < 10초의 DR 등급 달성, FinOps 기반 3~18개월 내 클라우드 비용 20~40% 회수 효과를 입증할 수 있다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs 멀티/하이브리드 전략, 동기식 모놀리식 vs 비동기 이벤트 드리븐(EDA)·CQRS·SAGA, Stateful vs Stateless 워크로드 분리, Egress 비용·데이터 주권(GDPR/개인정보보호법)·종량제 폭증(Sticker Shock) 방지를 위한 아키텍처 의사결정이 핵심 트레이드오프이며, 마이그레이션 6R 프레임워크(Rehost, Replatform, Repurchase, Refactor, Retire, Retain)와 카나리·블루그린·피처 플래그 기반 점진적 배포 전략의 조합이 시험의 변별 포인트다.

---

## Ⅰ. 개요 및 필요성

전통적 엔터프라이즈 IT는 베어메탈 서버 위에서 수직 확장(Scale-Up)·강결합 모놀리식 아키텍처·수동 용량 계획·CapEx 중심의 HW 라이프사이클(통상 5년)에 의존했다. 이 구조는 ① 트래픽 피크 대비 과잉 프로비저닝(평균利用率 10~20%)으로 인한 자원 낭비, ② 릴리스 주기 6~12개월의 시장 대응력 저하, ③ IDC CAPEX(랙·전력·냉각·회선) 점진적 증가, ④ 재해 시 DR 사이트 콜드 스탠바이로 인한 RPO/RTO 수시간~수일 발생, ⑤ L4/L7 로드밸런서·방화벽·스토리지 이중화 구성의 복잡성 및 HW 벤더 종속성이라는 5대 구조적 한계를 노출했다.

클라우드 아키텍처는 NIST SP 800-145(2011)에서 정의한 "구성 가능한 컴퓨팅 자원 공유 풀(Shared Pool)에 대한 어디서나·온디맨드·신속한 네트워크 접근 및 제공" 모델을 통해, **가상화(KVM/Xen/Hyper-V) -> 컨테이너(Docker/containerd) -> 오케스트레이션(K8s) -> 서비스 메시(Istio) -> 서버리스(FaaS)**로 이어지는 추상화 스택 진화와 함께 위 한계를 근본적으로 해소한다. 즉, 자원을 HW가 아닌 **API로 정의된 논리적 단위**로 다루게 되었고, 이를 Terraform·Pulumi·CloudFormation 같은 IaC(Infrastructure as Code)로 코드화하여 GitOps 기반의 선언적 프로비저닝·버전관리·롤백이 가능해졌다.

```text
[전통적 온프레미스 아키텍처]                [현대적 클라우드 네이티브 아키텍처]
+-------------------------+                +--------------------------------------+
|   사용자 -> L4 LB -> L7 LB |                |   사용자 -> CDN -> Edge GW (WAF/Shield)|
|   +- Web (Apache+JBoss) |                |   +- API GW (Kong/Apigee/Envoy)      |
|   +- WAS (Cluster)      |                |   +- Microservices (K8s Pod×N)       |
|   +- DB (Oracle RAC)    |                |   +- Service Mesh (mTLS, Sidecar)    |
|   RAID·SAN·FC Switch    |                |   +- Event Bus (Kafka/Pulsar)        |
|   수동 배포, 야간 배포    |                |   +- Serverless (Lambda/Functions)   |
|   CAPEX, 5년 갱신주기     |                |   +- Managed DB (Aurora/Cosmos/Redis)|
+-------------------------+                |   IaC(Terraform)·GitOps(ArgoCD)     |
        v 마이그레이션                         |   Observability(Prom/Grafana/OTel)  |
  [6R 전략·Strangler Fig]                   +--------------------------------------+
                                                          v
                              Multi-Region Active-Active + Chaos Engineering
```

**왜 필요한가 (5대 전환 동인)**
- **경제성**: Pay-per-use 모델 + Spot/Preemptible 인스턴스(70~90% 할인가) + Reserved/Savings Plan(최대 72% 할인) -> 동일 워크로드 대비 3년 TCO 40~60% 절감 (Forrester/IDC 다수 사례)
- **민첩성**: 컨테이너 이미지 빌드 평균 2~5분, K8s 롤링 업데이트 시 무중단 배포, GitHub Actions -> ArgoCD 동기화 30~60초
- **글로벌 확장성**: 단일 리전 -> 멀티 리전 Active-Active, AWS Global Accelerator·Azure Front Door·Cloud CDN으로 글로벌 P99 < 200ms 달성
- **회복탄력성(Resilience)**: AZ(Availability Zone) 단위 장애 격리, Auto Scaling Group + Multi-AZ RDS, Circuit Breaker(Hystrix/Resilience4j)로 연쇄 장애 차단
- **데이터 기반 운영**: CloudWatch·Stackdriver·Azure Monitor + Prometheus + Grafana + OpenTelemetry로 메트릭·로그·트레이스 통합 관측(Observability)

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"호텔의 객실을 필요할 때만 빌리는 단기 임대 시스템"**과 같다. 자기 집(온프레미스)을 짓는 데 수십억 들이고 평생 쓸 방을 남기느니, 여행자처럼 사용한 시간·서비스만큼만 결제하고 늘 적절한 객실 수를 호텔이 알아서 배정해주는 것이 클라우드의 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **계층형 참조 모델(Reference Architecture)**로 이해해야 한다. 전통적 3-tier(Web-WAS-DB)는 클라우드 환경에서 **API Gateway + Microservices + Event Bus + Managed DB** 구조로 진화하며, 각 계층은 특정 AWS·GCP·Azure·NCP(네이버)·KakaoCloud 서비스에 1:1 매핑된다.

```text
[클라우드 네이티브 12-Factor 기반 계층 아키텍처]
+------------------------------------------------------------------------------+
| ① Edge/Network Tier                                                           |
|   Route53(DNS Anycast) -> CloudFront/Azure CDN/Naver nCloud CDN              |
|   WAF·Shield Advanced(DDoS L3/4/7) · Global Accelerator(Anycast IP)        |
+------------------------------------------------------------------------------+
| ② API Gateway Tier                                                            |
|   Kong/Apigee/Amazon API GW · Envoy xDS · GraphQL Federation(Apollo)         |
|   인증(OAuth2/OIDC/JWT) · Rate Limiting(Redis Token Bucket) · Quota 관리     |
+------------------------------------------------------------------------------+
| ③ Application Tier (Stateless Microservices)                                  |
|   Spring Boot 3 / Node.js / Go / Python FastAPI                              |
|   컨테이너: Docker 24 -> containerd -> Kubernetes 1.30 (EKS/GKE/AKS/NKE)       |
|   오토스케일링: HPA(CPU/Mem/Custom Metric) + VPA + KEDA(이벤트 기반)         |
|   Service Mesh: Istio 1.22(Envoy Sidecar) · Linkerd 2.14 · Cilium Service Mesh|
|   카나리 배포: Argo Rollouts · Flagger · Istio VirtualService (10%->50%->100%)|
+------------------------------------------------------------------------------+
| ④ Data Tier (Polyglot Persistence)                                            |
|   OLTP: Aurora MySQL/PostgreSQL · Spanner/CockroachDB · DynamoDB/Cosmos DB  |
|   Cache: ElastiCache(Redis 7) · Memorystore · Memcached                       |
|   Search: OpenSearch/Elasticsearch · Algolia                                  |
|   OLAP: Redshift · BigQuery · Snowflake · ClickHouse                         |
|   Object/S3: S3 호환(MinIO) · 버전관리·Lifecycle·Cross-Region Replication   |
|   Event Store: Apache Kafka 3.7 · Pulsar · Kinesis · Pub/Sub                |
+------------------------------------------------------------------------------+
| ⑤ Cross-Cutting Concerns (횡단 관심사)                                        |
|   Observability: OpenTelemetry SDK -> Collector -> Tempo/Jaeger + Loki + Prom |
|   Security: CSPM(PrismaCloud) · CWPP · IAM/IRSA · Secrets Manager · Vault    |
|   Resilience: Multi-AZ + Multi-Region · Chaos Engineering(LitmusChaos/Gremlin)|
|   FinOps: Kubecost · CloudHealth · Vantage · Apptio                         |
+------------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **가상화/하이퍼바이저** | 물리 HW를 논리 VM으로 분할 | Type-1(KVM-baremetal, Xen, Hyper-V), Type-2(VirtualBox), AWS Nitro System 하드웨어 분산 오프로드 |
| **컨테이너 런타임** | OS 커널 공유로 경량 프로세스 격리 | Docker 24(BuildKit) -> containerd 1.7 / CRI-O, 이미지 레이어 캐싱, OCI 표준 스펙 준수 |
| **오케스트레이터(K8s)** | 컨테이너 라이프사이클·스케줄링·자가치유 | kube-apiserver(etcd 3.5 합의) -> kube-scheduler(예약) -> kubelet(CRI/gRPC) -> kube-proxy(CNI), Controller Manager(ReplicaSet/Deployment/StatefulSet) |
| **서비스 메시(Istio)** | L7 트래픽 관리·mTLS 제로트러스트·관측 | Envoy Sidecar(15090 admin, 15001 outbound), xDS API, Control Plane(Pilot/Citadel/Galley), WASM 필터 확장 |
| **API Gateway** | 외부 트래픽 진입점·프로토콜 변환·정책 | Kong(OpenResty+Lua), AWS API Gateway(REST/WebSocket), Apigee(API 분석), Envoy(고성능 L7), GraphQL Federation(Apollo Router) |
| **Managed Database** | 자동 백업·PITR·Multi-AZ 페일오버 | Aurora 6-Writer(저지연 복제, 1/10 비용), DynamoDB Global Tables(멀티리전 멀티마스터), Cosmos DB(Turnkey 글로벌 분산) |
| **오브젝트 스토리지(S3)** | 11 9s 내구성·EB급 확장·HTTP API | S3 Standard/IA/Glacier(아카이브), 버전관리 + Object Lock(WORM), 교차 리전 복제(CRR), S3 One Zone-IA(단일 AZ, 20% 저렴) |
| **이벤트 스트리밍** | 비동기 메시지·로그·CDC(Change Data Capture) | Kafka 3.7(KRaft 모드, ZooKeeper 제거)·분산 코디네이터·Pulsar(BookKeeper 세그먼트 스토어), exactly-once semantic |

**핵심 알고리즘·파라미터 심화**
- **Kubernetes 스케줄링**: `kube-scheduler`는 (1) Filtering(PodFitsResources, NodeSelector, Taint/Toleration, Affinity) -> (2) Scoring(LeastAllocated, BalancedAllocation, NodeLocality, ImageLocality) -> (3) Binding 3단계로 노드 선택. Topology Spread Constraints는 `maxSkew: 1`로 AZ/Pod 분산.
- **HPA 공식**: `desiredReplicas = ceil[ currentReplicas × ( currentMetricValue / desiredMetricValue ) ]`, 30초 폴링, `--horizontal-pod-autoscaler-sync-period`로 조정. KEDA는 Kafka Lag·SQS 큐 길이·Cron 등 외부 이벤트 기반 스케일링 지원.
- **오토스케일링 알고리즘 비교**: AWS EC2 Target Tracking(평균 CPU 70% 유지), Step Scaling(임계값 점진), Predictive Scaling(LSTM·7일 데이터로 사전 스케일). 게임 트래픽·이커머스 등 예측 가능 워크로드에서 30% 비용 절감.
- **CAP 정리와 분산 DB**: RDBMS(MySQL)는 CP(일관성+분할 허용), DynamoDB/Cassandra는 AP(가용성+분할 허용, eventual consistency), Cosmos DB는 멀티마스터로 PA/ELT 5단계 일관성 모델 tunable. 금융 코어는 CP, SNS 피드는 AP 선택.
- **일관성 해시(Consistent Hashing)**: DynamoDB/Cassandra 파티션 샤딩, 가상 노드(Virtual Node) 256~1024개로 키 분산, 리밸런싱 시 키 재배치 비율 = K/N (K=키수, N=노드수), 리플리카는 R=3 기본, `W+R>R`로 강한 일관성 보장.
- **S3 스토리지 클래스 티어링 자동화**: S3 Intelligent-Tiering(ML 기반 액세스 패턴 분석, 30일/90일 비액세스 시 IA·Archive 자동 이동, 모니터링 비용 $0.0025/1000객체, retrieval fee 없음).
- **mTLS 핸드셰이크**: Istio Citadel이 SPIFFE ID(`spiffe://cluster.local/ns/default/sa/svc-account`) 발급 -> Envoy Sidecar가 1회 RTT 핸드셰이크, TLS 1.3 + X25519 + AES-256-GCM, 인증서 24시간 자동 로테이션.

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 12-Factor + MSA 구조는 **"도시의 상하수도 시스템"**과 같다. 각 가정(마이크로서비스)에 물(요청)이 필요한 만큼만 정수장(K8s)이 보내고, 하수처리장(API Gateway)이 오염된 요청을 걸러내며, 저수지(S3·RDS)가 데이터를 보관한다. 파이프가 하나 막히면 다른 길로 우회(자가치유)되어 도시 전체가 멈추지 않는다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처의 의사결정은 단일 정답이 없다. 동일 목표(고가용·저비용·고성능)에 대해 **다수의 아키텍처 옵션**이 존재하며, 트레이드오프 매트릭스를 통해 비교한다.

| 구분 | Monolithic On-Prem | Cloud-Hosted Monolith (Lift&Shift) | Cloud-Native MSA (Refactor) | Serverless / FaaS |
| :--- | :--- | :--- | :--- | :--- |
| **확장 모델** | 수직 확장(
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 766 / 800

<- **이전**: [765. 클라우드 아키텍처 핵심 토픽 765번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/765_cloud_architecture_core_topic_765_exam_summar/)
**다음**: [767. 클라우드 아키텍처 핵심 토픽 767번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/767_cloud_architecture_core_topic_767_exam_summar/) ->

---
