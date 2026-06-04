---
title: "794. 클라우드 아키텍처 핵심 토픽 794번 시험 요약 (Cloud Architecture Core Topic 794 Exam Summary)"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 12-Factor App·Well-Architected Framework·CNCF Cloud Native Landscape 기반의 **IaC(코드형 인프라) + 컨테이너 오케스트레이션(K8s) + 서버리스(FaaS) + 옵저버빌리티(3-Pillar: Metrics/Logs/Traces)** 4축을 통합한 선언적·탄력적 분산 시스템 설계 패러다임이다.
> 2. **가치**: 6R 마이그레이션(Rehost/Replatform/Repurchase/Refactor/Retire/Retain) 전략으로 **TCO 30~60% 절감**, Auto Scaling + Spot Instance로 **컴퓨팅 비용 70%v**, 다중 AZ + Multi-Region DR로 **RTO 1시간·RPO 5분 이내**의 사업연속성을 달성한다.
> 3. **판단 포인트**: CAP 정리 하의 **일관성·가용성·분단내성** 트레이드오프, Multi-Cloud vs Hybrid Cloud의 **데이터 주권·벤더 락인·네트워크 지연** 균형, FinOps 기반의 **사용량 기반 과금(Usage-based) vs 예약 인스턴스(Commitment Discount)** 비용 모델 선택이 핵심 의사결정 기준이다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스(On-Premise) 아키텍처는 **CapEx(자본 지출) 중심의 수직 확장(Scale-Up)**, **모놀리식(Monolithic) 구조**, **수동 용량 계획**, **MTTR 기준의 장애 대응**으로 특징지어진다. 이는 비즈니스 트래픽 변동성(Black Friday·신년 트래픽 등 최대 100배 스파이크), 글로벌 사용자 24×7 서비스 요구, 데이터 폭증(연 40~60% 증가)에 대응하기 어렵다. 클라우드 아키텍처는 이를 **OpEx(운영 지출) 기반 사용량 과금(Pay-Per-Use)**, **수평 확장(Scale-Out)**, **자가 치유(Self-Healing)**, **불변 인프라(Immutable Infrastructure)**로 전환한다.

```text
+-------------------------------------------------------------------------+
|           온프레미스 -> 클라우드 아키텍처 패러다임 전환 (Paradiagm Shift)        |
+-------------------------------------------------------------------------+

  [ On-Premise Era ]                              [ Cloud-Native Era ]
  +------------------+                            +------------------+
  | • CapEx 위주 투자  |                            | • OpEx 종량제 과금 |
  | • Scale-Up (수직) |  -------------------►      | • Scale-Out (수평)|
  | • Monolithic      |   Digit. Transformation   | • Microservices   |
  | • 수동 Capacity   |                            | • Auto-Scaling    |
  | • MTTR 장애대응   |                            | • MTTF Self-Heal  |
  | • Snowflake서버   |                            | • Immutable Infra |
  | • 월~년 단위배포   |                            | • 일~분 단위배포   |
  +------------------+                            +------------------+
         |                                                |
         v                                                v
   +-----------+                                  +---------------+
   | 고정비용^  |                                  | 변동비용 최적화 |
   | 유휴자원v  |                                  | 탄력적 확장    |
   | 장애위험^  |                                  | 고가용성·DR    |
   +-----------+                                  +---------------+
```

기술사 출제 관점에서 클라우드 아키텍처는 단순히 서버를 IaaS로 이전하는 것을 넘어, **도메인 분해(DDD: Domain-Driven Design)**, **이벤트 기반(Event-Driven) 비동기 메시징**, **데이터 일관성 모델(Saga·Outbox·CDC)**, **제로 트러스트(Zero Trust) 보안**, **FinOps(클라우드 재무 운영)** 등 다양한 엔지니어링 분야의 융합이 평가된다. Gartner의 하이퍼사이클에서도 Cloud-Native Platform, Platform Engineering, AI-Augmented Engineering이 Innovation Trigger 단계에 위치해 기술사 기출 적합성이 매우 높다.

- **📢 섹션 요약 비유**: 온프레미스는 "직접 짓고 유지하는 단독 주택(수도·전기·난방 모두 자가 관리)"이고, 클라우드 아키텍처는 "수도·전기·난방·보안 모두 통합 관리되는 스마트 아파트 + 필요 시 즉시 옆동 호수로 확장 가능한 엘라스틱 빌딩"이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 NIST SP 500-292의 **5대 필수 특성(On-Demand·Broad Network Access·Resource Pooling·Rapid Elasticity·Measured Service)**과 3대 서비스 모델(IaaS/PaaS/SaaS) + 4가지 배포 모델(Public/Private/Hybrid/Community)을 기반으로 한다. 실무에서는 AWS Well-Architected Framework 6 Pillars, Azure Well-Architected Framework 5 Pillars, Google Cloud Architecture Framework를 벤치마킹한다.

```text
+--------------------------------------------------------------------------+
|      클라우드 네이티브 참조 아키텍처 (Cloud-Native Reference Architecture)    |
+--------------------------------------------------------------------------+

                          +----------------------+
                          |   Users / Devices    |
                          |  (Web·Mobile·IoT·API)|
                          +----------+-----------+
                                     | HTTPS / mTLS
                                     v
              +------------------------------------------------+
              |        Edge Layer (Global Accelerator / CDN)    |
              |   CloudFront · Cloudflare · Akamai · Cloud CDN |
              +--------------------+---------------------------+
                                   v
              +-------------------------------------------------+
              |       API Gateway / BFF / API Management        |
              |  Kong · Apigee · AWS API GW · Spring Cloud GW   |
              +------+--------------+--------------+------------+
                     |              |              |
                     v              v              v
        +-----------------+ +--------------+ +-----------------+
        |  Microservice A | |Microservice B| |  Lambda / FaaS  |
        |  (Spring Boot)  | | (Node.js)    | |  (Serverless)   |
        |  + Svc Mesh     | | + Svc Mesh   | |  Event-Driven   |
        +--------+--------+ +------+-------+ +--------+--------+
                 |                 |                  |
                 +-----------------+------------------+
                                   v
              +-------------------------------------------------+
              |   Container Orchestration (Kubernetes / EKS)    |
              |  Pod·Deployment·StatefulSet·HPA·VPA·Cluster Autoscaler|
              +--------------------+----------------------------+
                                   v
        +----------------------------------------------------------+
        |  Data Plane (Polyglot Persistence)                        |
        |  +------+ +------+ +------+ +------+ +------+ +------+ |
        |  |RDS   | |Dynamo| |Redis | |S3    | |ES    | |Kafka | |
        |  |(RDB) | |(KV)  | |(Cache| |(Obj) | |(검색)| |(스트림)|
        |  +------+ +------+ +------+ +------+ +------+ +------+ |
        +----------------------------------------------------------+
                                   |
                                   v
              +-------------------------------------------------+
              |  Observability (3-Pillar)                        |
              |  • Metrics : Prometheus · CloudWatch · Datadog   |
              |  • Logs    : Loki · ELK · OpenSearch             |
              |  • Traces  : Jaeger · Zipkin · X-Ray             |
              +-------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Edge & CDN** | 글로벌 트래픽 종단 처리·캐싱·DDoS 방어 | CloudFront·Cloudflare Magic Transit, Anycast IP 라우팅, TLS 1.3·QUIC 기반 핸드셰이크 가속 |
| **API Gateway** | 라우팅·인증·Rate Limiting·트랜스폼 | OAuth 2.0 / OIDC / mTLS, Token Bucket·Leaky Bucket 알고리즘, GraphQL Federation, gRPC-Web 프록시 |
| **Service Mesh** | L7 트래픽 관리·관측·mTLS 자동화 | Istio (Envoy Sidecar), Linkerd, App Mesh. Istiod가 xDS API로 Envoy 설정 분배, **SMI(Spec Mesh Interface)** 표준 |
| **Container Orchestration** | 컨테이너 라이프사이클·자가치유·오토스케일 | K8s 1.30+ Control Plane (kube-apiserver·etcd·scheduler·controller-manager), **HPA v2**(CPU·Memory·Custom Metric), **Karpenter**(Just-In-Time 노드 프로비저닝), **ArgoCD**(GitOps) |
| **Serverless (FaaS)** | 이벤트 기반 stateless 단기 실행 | AWS Lambda(15분 타임아웃·10GB 메모리), Azure Functions(20분·14GB), Cold Start 100~800ms, **SnapStart·Provisioned Concurrency**로 콜드스타트 완화 |
| **Data Plane** | 폴리글랏 영속성·CQRS·이벤트 소싱 | RDB(OLTP) + Data Lake(S3 Parquet) + Lakehouse(Iceberg/Delta/Hudi) + Search(OpenSearch), CDC: Debezium -> Kafka -> Sink |

### 12-Factor App 원칙 (Heroku, 2011)
기술사 단골 키워드. **(1) Codebase**(단일 코드베이스·다중 배포), **(2) Dependencies**(명시적 선언, `requirements.txt`/`package.json`), **(3) Config**(환경변수 분리, 12Factor.net), **(4) Backing Services**(DB·캐시를 attached resource로), **(5) Build/Release/Run**(엄격한 빌드-릴리스-런 분리), **(6) Processes**(Stateless), **(7) Port Binding**(자체 포트 바인딩), **(8) Concurrency**(프로세스 모델로 확장), **(9) Disposability**(빠른 기동·정상 종료 SIGTERM), **(10) Dev/Prod Parity**(dev-prod 간격 최소화), **(11) Logs**(stdout/stderr 스트림), **(12) Admin Processes**(마이그레이션·REPL 일회성 작업).

### CAP 정리 & 일관성 모델
분산 시스템 트레이드오프. **CP 시스템**(RDB+2PC·etcd·ZooKeeper: 강한 일관성·분단 시 가용성 손실), **AP 시스템**(Cassandra·DynamoDB·Cosmos DB: Eventually Consistent·항상 쓰기 가능, **N=R+W quorum 튜닝**), **CA 시스템**(전통 RDB, 단일 노드 한정). PACELC 정리는 평상시(Else)에도 지연(Latency)과 일관성(Consistency) 간 트레이드오프가 있음을 명시한다.

### 마이크로서비스 패턴 (Chris Richardson)
- **서비스 디스커버리**: Consul, Eureka, CoreDNS, K8s Service+Ingress
- **Circuit Breaker**: Hystrix -> Resilience4j (Closed/Open/Half-Open 상태 머신, 임계치 초과 시 fail-fast)
- **Saga Pattern**: Choreography(이벤트 기반) vs Orchestration(Camunda·Temporal·Step Functions). 보상 트랜잭션(Compensating Tx)으로 분산 트랜잭션 구현
- **Outbox Pattern**: 동일 DB 트랜잭션에 비즈니스 데이터 + 이벤트 메시지를 `outbox` 테이블에 저장, 별도 CDC(Change Data Capture) 프로세스가 Kafka로 발행 -> **At-Least-Once + 멱등(idempotency key)** 보장
- **CQRS + Event Sourcing**: 쓰기 모델(명령)·읽기 모델(조회) 분리, 상태 변경을 이벤트 로그로 저장(append-only), Materialized View로 비정규화 조회 최적화

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "도미노와 자석의 결합"이다. 도미노처럼 MSA를 작은 단위로 쪼개되(Microservice), 자석처럼 API Gateway·Service Mesh·옵저버빌리티로 강하게 결합시켜 한 곳의 장애가 전체로 전파되지 않도록 한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **IaaS** (Infrastructure-as-a-Service) | **PaaS** (Platform-as-a-Service) | **SaaS** (Software-as-a-Service) | **FaaS** (Function-as-a-Service) |
| :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | OS·미들웨어 직접 관리 | 런타임·미들웨어 자동 관리 | 애플리케이션까지 제공 | 코드만 배포, 나머지 전부 위임 |
| **제어 수준** | 가장 높음 (가상화·네트워크) | 중간 (앱 코드·데이터) | 가장 낮음 (설정만) | 코드·이벤트 핸들러 |
| **확장성** | 수동/스크립트 기반 | 앱 단위 자동 확장 | 벤더 정책에 종속 | 요청 단위 0->N 자동 |
| **과금 모델** | 인스턴스 시간당 | 인스턴스·환경 시간당 | 사용자(Seat) 단위 | 호출 횟수·GB-초 |
| **대표 서비스** | EC2·Compute Engine·Azure VM | Beanstalk·App Engine·Azure App Service | Office 365·Salesforce·Slack | Lambda·Cloud Functions·Azure Functions |
| **적합 워크로드** | 레거시 Lift&Shift, 커스텀 네트워크 | 웹앱·API 표준 배포 | 표준 업무·협업 도구 | 이벤트 처리·간헐적 워크로드 |
| **TCO** | CapEx->OpEx 부분 전환 | 운영 부담 30%v | 도입 즉시 사용 | 유휴 시 비용 0원 |

| 구분 | **Monolithic** | **Microservice** | **Serverless MSA** |
| :--- | :--- | :--- | :--- |
| **배포 단위** | 전체 앱 1개 | 서비스별 독립 | 함수 단위 |
| **장애 격리** |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 794 / 800

<- **이전**: [793. 클라우드 아키텍처 핵심 토픽 793번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/793_cloud_architecture_core_topic_793_exam_summar/)
**다음**: [795. 클라우드 아키텍처 핵심 토픽 795번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/795_cloud_architecture_core_topic_795_exam_summar/) ->

---
