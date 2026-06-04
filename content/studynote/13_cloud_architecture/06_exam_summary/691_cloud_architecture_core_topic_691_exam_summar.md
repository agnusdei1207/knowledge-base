---
title: "691. 클라우드 아키텍처 핵심 토픽 691번 시험 요약 (Cloud Architecture Core Topic 691 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 퍼블릭·프라이빗·하이브리드 클라우드 환경에서 IaaS/PaaS/SaaS/FaaS 계층별 책임 분산 모델과 Well-Architected Framework 6대 원칙(운영 우수성, 보안, 안정성, 성능 효율성, 비용 최적화, 지속 가능성)을 토대로 워크로드의 가용성·확장성·탄력성을 엔지니어링하는 것이 클라우드 아키텍처의 본질이다.
> 2. **가치**: Auto Scaling + 다중 AZ(가용 영역) + 다중 리전 구성을 통해 99.99%(Four Nine) 이상의 SLA를 달성하고, Pay-as-you-go 모델로 인해 기존 CAPEX 대비 OPEX 전환 시 TCO를 약 30~60% 절감하며, MTTR(평균 복구 시간)을 분 단위로 단축 가능하다.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs 멀티 클라우드 전략, Egress 비용·데이터 주권·지연 시간(Latency) 트레이드오프, Stateless/Microservices 우선 설계 여부, 그리고 12-Factor App 원칙 준수 수준이 아키텍처의 장기적 유지보수성과 TCO를 결정짓는 핵심 분기점이다.

---

## Ⅰ. 개요 및 필요성

클라우드 아키텍처는 가상화·컨테이너·오케스트레이션·IaC(Infrastructure as Code)·관측 가능성(Observability) 기술을 통합하여, 온프레미스 중심의 Monolithic 구조에서 **Cloud-Native 분산 시스템**으로의 패러다임 전환을 가능하게 한다. 2006년 AWS S3·EC2 출시 이후, 클라우드는 단순한 "외부 호스팅"을 넘어 **API 기반 셀프서비스 프로비저닝, 선언적 인프라(Terraform/CloudFormation), GitOps 기반 배포(ArgoCD/Flux), Service Mesh(Istio/Linkerd)** 가 결합된 운영 모델로 진화했다.

기술사 시험 관점에서 클라우드 아키텍처는 **"비즈니스 요구사항을 SLA·SLO·SLI로 정량화하고, 이를 클라우드 서비스 프리미티브(EC2, S3, RDS, Lambda, EKS, DynamoDB 등)로 매핑"** 하는 능력을 평가한다. 특히 한국 클라우드 컴퓨팅법(2021), 개인정보보호법, CSAP(클라우드 보안 인증) 요건이 결합되면서, 아키텍처 결정이 단순 기술 선택을 넘어 **규제 준수·감사 대응·데이터 주권** 문제로 확장된다.

```text
[전통 아키텍처 -> 클라우드 네이티브 전환 흐름]

 +------------------+      +------------------------------+
 |  On-Premise      |      |      Cloud-Native Platform    |
 | +--------------+ |      | +--------------------------+ |
 | | Monolithic   | |  ->   | | Microservices + Mesh     | |
 | | App Server   | |      | | (Istio/Envoy Sidecar)    | |
 | +--------------+ |      | +--------------------------+ |
 | | RDBMS        | |      | | Polyglot Persistence     | |
 | | (Oracle)     | |      | | (RDS+Redis+Dynamo+S3)    | |
 | +--------------+ |      | +--------------------------+ |
 | | 수동 운영    | |      | | GitOps + Observability   | |
 | +--------------+ |      | | (Prometheus/Grafana/OTel) | |
 +------------------+      | +--------------------------+ |
       3-Tier 정적         |   Dynamic, Event-Driven,     |
                           |   Self-Healing, Auto-Scaling |
                           +------------------------------+
```

**왜 필요한가?**

- **CAPEX -> OPEX 전환**: 데이터센터 전력·냉각·하드웨어 감가상각비를 변동비화하여, 유휴 자원 비용(평균 30~40%) 제거
- **탄력성(Elasticity)**: 트래픽 스파이크(블랙프라이데이, 게임 오픈, 공모주 청약)에 대해 HPA(Horizontal Pod Autoscaler)가 5분 내 1,000 -> 10,000 Pod 자동 확장
- **글로벌 도달성**: AWS 33개 리전·105개 가용 영역, Azure 60+ 리전, GCP 38개 리전을 통한 엣지 배포로 글로벌 사용자 P99 지연 시간 200ms 이내 달성
- **회복 탄력성(Resilience)**: Circuit Breaker(Resilience4j, Hystrix), Chaos Engineering(Chaos Monkey, LitmusChaos)을 통한 능동적 장애 대응

- **📢 섹션 요약 비유**: 기존 Monolithic 아키텍처는 "한 채의 거대한 호텔"이라 손님이 늘어나면 호텔을 통째로 지어야 하지만, 클라우드 네이티브는 "모듈식 콘테이너 호텔"이라 손님 수에 따라 방(컨테이너)을 즉시 조립·해체할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **관심사 분리(Separation of Concerns)** 와 **선언적 인터페이스(Declarative API)** 이다. 시스템은 크게 5개 계층으로 분해되며, 각 계층은 독립적으로 확장·장애 격리·기술 교체 가능하도록 설계된다.

```text
[5-Tier Cloud-Native Reference Architecture]

+-------------------------------------------------------------+
|  Tier 1: Edge & Delivery                                    |
|  +----------+  +----------+  +----------+                  |
|  | CloudFront|  |   WAF   |  | Global   |  DDoS Shield    |
|  |   (CDN)  |  | (L7방어) |  |  LB      |  (L3/L4)        |
|  +----------+  +----------+  +----------+                  |
+-------------------------------------------------------------+
|  Tier 2: API Gateway & Service Mesh                         |
|  +--------------+  +--------------+  +--------------+     |
|  | API Gateway  |-> |  Istio Mesh  |-> | gRPC/REST    |     |
|  | (Rate Limit) |  | mTLS, Retry  |  | Service      |     |
|  +--------------+  +--------------+  +--------------+     |
+-------------------------------------------------------------+
|  Tier 3: Application Runtime                                |
|  +--------------+  +--------------+  +--------------+     |
|  | EKS/ECS Pod  |  | Lambda/Func  |  | Cloud Run    |     |
|  | (Container)  |  | (Serverless) |  | (Knative)    |     |
|  +--------------+  +--------------+  +--------------+     |
+-------------------------------------------------------------+
|  Tier 4: Data Plane                                         |
|  +----------+ +----------+ +----------+ +----------+     |
|  | Aurora   | | DynamoDB | | S3/Blob  | | ElastiC  |     |
|  | (RDBMS)  | | (NoSQL)  | | (Object) | | (Cache)  |     |
|  +----------+ +----------+ +----------+ +----------+     |
+-------------------------------------------------------------+
|  Tier 5: Cross-Cutting (Observability + Security)          |
|  Prometheus + Grafana + Jaeger + OTel + Vault + OPA        |
+-------------------------------------------------------------+
         ^                  ^                  ^
         |                  |                  |
     IaC (Terraform)    CI/CD (GitHub Actions/ArgoCD)
         |                  |                  |
     +---+------------------+------------------+---+
     |  Control Plane: IAM, KMS, CloudTrail, Config |
     +----------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Edge Layer (CDN/WAF/LB)** | 글로벌 트래픽 진입점, L3~L7 보안, 정적 콘텐츠 캐싱 | CloudFront·Cloudflare·Akamai는 Anycast IP로 POP(Points of Presence) 400+ 곳에 라우팅, WAF는 OWASP Top 10 SQLi/XSS 시그니처 기반 차단(평균 5~50ms 레이턴시 추가) |
| **API Gateway & Service Mesh** | 트래픽 라우팅, 인증/인가, mTLS, 카나리/블루그린 배포 | Envoy Proxy Sidecar가 모든 east-west 트래픽을 L7 가시화, Istio VirtualService로 트래픽 5%->25%->100% 단계적 분할, OPA(Open Policy Agent)로 Rego 정책 평가 |
| **Container Orchestrator (Kubernetes)** | 컨테이너 스케줄링, 셀프힐링, 선언적 상태 관리 | K8s Control Plane(etcd 기반) + Worker Node, Pod 단위로 IP 할당(CNI: Cilium/Calico), HPA는 CPU/Mem/Custom Metric(QPS·RPS) 기반 30초 주기 스케일링 |
| **Serverless Runtime** | 이벤트 기반 단기 실행, Cold Start 최적화 | Lambda는 128~10,240MB 메모리·1ms 단위 과금, Provisioned Concurrency로 Cold Start 100~300ms 제거, SnapStart(Java 11+)로 10x 기동 단축 |
| **Polyglot Data Store** | 워크로드 특성에 맞는 저장소 선택 | CQRS 패턴 적용 — Write는 DynamoDB(단일 ms 지연) + Write-Ahead Log, Read는 Aurora Read Replica + ElastiCache Redis(서브 ms), S3는 11 9s(99.999999999%) 내구성 |
| **Observability Stack** | 메트릭·로그·트레이스 통합 관측 | 3 Pillars: Metrics(Prometheus, 1초 해상도) / Logs(Loki, ELK, 구조화 JSON) / Traces(OpenTelemetry + Jaeger/Tempo), SLO 기반 Error Budget으로 Feature Release 게이팅 |
| **Infrastructure as Code (IaC)** | 선언적 인프라 프로비저닝 및 Drift Detection | Terraform State는 S3 + DynamoDB Lock으로 동시성 보장, Pulumi는 TypeScript/Python으로 일반 언어 사용, Crossplane은 K8s CRD로 클라우드 리소스 관리 |

**핵심 동작 메커니즘 심층 분석**

1. **Auto Scaling 알고리즘**: AWS Target Tracking Scaling은 `TargetValue = 70%`로 CPU 사용률을 설정하면 CloudWatch Alarm이 1분 간격으로 평가하여 `DesiredCapacity = ceil(CurrentMetric/TargetValue × CurrentCapacity)`로 인스턴스 수 산출. 예측 스케일링(Predictive Scaling)은 LSTM 시계열 모델로 2일 전 트래픽 예측.
2. **Consensus 알고리즘**: etcd는 Raft 합의 알고리즘으로 Leader Election(150~200ms) + Log Replication 수행, K8s API Server의 모든 상태 변경은 etcd v3 gRPC API를 거치므로 etcd I/O latency가 클러스터 전체 응답 시간의 바닥.
3. **CAP Trade-off**: DynamoDB는 AP(가용성·분할 허용) 우선, Cosmos DB는 Tunable Consistency(Strong/Bounded Staleness/Session/Consistent Prefix/Eventual) 5단계로 CAP 트레이드오프를 애플리케이션이 선택.

- **📢 섹션 요약 비유**: 5-Tier 아키텍처는 "우체국 시스템"과 같다 — 우편물(요청)이 들어오면(Edge) -> 분류기(API Gateway)가 우편번호별 분류하고 -> 택배 차량(K8s Pod)이 동네별로 배달하며 -> 창고(Data Store)에 보관하고 -> 중앙 관제실(Observability)이 모든 배달 상태를 실시간 모니터링한다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처는 등장 배경·설계 철학에 따라 여러 변형이 존재하며, 각 모델은 상충하는 요구사항(비용·지연·일관성·통제) 사이에서 trade-off를 가진다.

| 구분 | IaaS (EC2, Compute Engine) | PaaS (Beanstalk, App Engine) | Serverless (Lambda, Cloud Functions) | On-Premise (VMware, Bare-metal) |
| :--- | :--- | :--- | :--- | :--- |
| **관리 책임 범위** | OS·Middleware·Runtime·App·Data 모두 사용자 | App·Data만 사용자, 그 외는 CSP | 코드(함수)만 사용자, 나머지 전부 CSP | 모든 계층 자체 관리 |
| **확장 단위** | VM 인스턴스 (수 분 소요) | 컨테이너·애플리케이션 (수 분) | 함수 호출 단위 (ms 단위 Auto Scale) | 수동 하드웨어 추가 (주~월) |
| **Cold Start** | 없음 (상시 기동) | 보통 30~60초 | 100ms~10초 (언어·크기 의존) | 없음 |
| **최소 과금 단위** | 시간(per-hour) | 시간(per-hour) | 1ms 단위, 100ms 최소 | CAPEX (5~7년 감가) |
| **Lock-in 위험** | 낮음 (Lift & Shift 가능) | 중간 (Vendor SDK 종속) | 높음 (벤더 고유 트리거·API) | 없음 (자체 통제) |
| **적합 워크로드** | 레거시 앱, GPU/HPC, 커스텀 커널 | 웹앱 API, 표준 스택 | 이벤트 드리븐, 스파이크성, IoT·파일 처리 | 데이터 주권, 규제 산업, 초저지연 |
| **예상 TCO 절감** | 30~40% | 40~55% | 50~70% (저사용률 시) | 기준점(Baseline) |

**다른 아키텍처 패턴과의 연결**

- **Microservices vs Monolith**: Monolith는 ①개발 단순 ②트랜잭션 일관성 쉬움 ③배포 단위 1개라는 장점이 있지만, 클라우드 Auto Scaling의 이점을 살릴 수 없어 부분 확장 불가. Microservices는 Domain-Driven Design(Bounded Context) + API Contract(OpenAPI/Protobuf) +
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 691 / 800

<- **이전**: [690. 클라우드 아키텍처 핵심 토픽 690번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/690_cloud_architecture_core_topic_690_exam_summar/)
**다음**: [692. 클라우드 아키텍처 핵심 토픽 692번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/692_cloud_architecture_core_topic_692_exam_summar/) ->

---
