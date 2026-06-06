---
title: "Strangler Fig Pattern Legacy Migration"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Martin Fowler가 2004년 명명한 Strangler Fig Pattern은 레거시 시스템(주로 Monolith, Mainframe)을 **Facade(API Gateway/Reverse Proxy) 기반의 점진적 트래픽 전환**으로 단계적으로 해체(Decomposition)하여 신규 MSA/Cloud-Native 시스템으로 무중단(Zero-Downtime) 치환하는 Evolutionary Migration 아키텍처 패턴이다.
> 2. **가치**: "Big-Bang Cutover" 대비 다운타임 0% 달성, 비즈니스 연속성 100% 보장, 변경 가능 범위를 단위 마이크로서비스(2~6주 Sprint) 단위로 분할하여 PoC->Production 위험을 약 70% 이상 절감하며, 레거시 회수(Technical Debt Reduction) 효과를 점진적으로 실현한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **① Facade의 라우팅 세분화 수준(Path/Header/Cookie/Payload) ② 데이터 이중 쓰기(Dual-Write) 시 일관성 보장 전략(Saga/CDC/Outbox) ③ 레거시 세션·인증 연동(JWT/SAML Bridge) 복잡도 ④ Strangling 기간 중 운영·관측(Observability) 이원화 비용**이며, 이를 ADR(Architecture Decision Record)로 명문화하여 이해관계자 합의하에 진행해야 한다.

---

## Ⅰ. 개요 및 필요성

금융·공공·통신·제조 등 대형 엔터프라이즈에서 20~30년 이상 운영된 COBOL Mainframe, JSP/EJB Monolith, Oracle Forms 기반 시스템은 **① 코드 수정 시 평균 4~8주 리드타임 ② 변경 실패율 60% 이상 ③ 신규 인력Pool 90% 이상 단절 ④ 라이선스 비용 연 5~15% 증가**라는 4대 Dead Sea Effect(죽음의 바닷효과)를 겪는다. 그러나 Big-Bang 방식의 재개발은 통상 18~36개월, 100~500억 원 투입되며, 프로젝트 실패율 68%(Standish Group CHAOS Report 2023 기준)에 달한다. 또한 메인프레임 인력의 평균 은퇴 연령이 55세임을 고려하면 **"지금 천천히 전환하지 못하면, 5년 후엔 할 수조차 없다"**는 Business Continuity Risk가 존재한다.

Strangler Fig Pattern은 **"기존 시스템을 한 번에 죽이지 않고, 트래픽을 점진적으로 새 시스템으로 흡수시켜 서서히 질식(Strangle)시킨다"**는 생물학적 메타포에서 출발한다. 핵심 전제 3가지는 다음과 같다.

| 전제 | 설명 |
|:---|:---|
| **점진성(Incrementality)** | 단일 배포 단위로 1~3개월 이내 완료 가능한 크기(Strangler Application)로 분해 |
| **가역성(Reversibility)** | 신규 서비스 장애 시 트래픽을 1초 내 Legacy로 즉시 복귀(Rollback) 가능 |
| **관측 가능성(Observability)** | 양쪽 시스템의 트랜잭션·로그·메트릭을 통합 OpenTelemetry 기반으로 상시 모니터링 |

```text
[클라이언트: Web/Mobile/3rd-Party]
              | HTTPS / mTLS
              v
   +--------------------------+
   |   Strangler Facade       |  <--- API Gateway / Reverse Proxy
   |   (Kong / Envoy / Nginx  |      (Path/Header 기반 동적 라우팅)
   |    / AWS API GW / Apigee)|
   +------+----------+--------+
          |          |
   +------v-----+ +--v--------------------------+
   |  Legacy    | |   New MSA / Cloud-Native    |
   |  Monolith  | |  - Spring Boot / NestJS     |
   |  (COBOL,   | |  - gRPC / GraphQL / REST    |
   |   EJB, JSP)| |  - DB: PostgreSQL/DynamoDB  |
   +------------+ +-----------------------------+
          |                  |
   +------v------------------v---------+
   |   Cross-Store Data Sync Layer      |
   |   (CDC: Debezium / SharePlex /     |
   |    Outbox Pattern / ETL/Batch)     |
   +------------------------------------+
```

레거시 시스템의 **기술 부채(Technical Debt)**는 단순한 코드 품질 문제가 아니라, **① 자동화 부재(수동 배포) ② 테스트 커버리지 5% 미만 ③ 결합도(Coupling) 1.0에 근접 ④ 평균 MTTR(Mean Time To Recovery) 8시간 이상**이라는 운영 리스크로 구체화된다. Strangler Pattern은 이런 리스크를 **회피(Risk Transfer)**가 아닌 **흡수·환원(Risk Absorption)**하는 방식으로 해결한다.

- **📢 섹션 요약 비유**: 낡은 시청사를 한 번에 부수지 않고, 출입구부터 차례로 신관으로 안내해 시민들은 불편 없이 출입하다가 어느 날 돌아보니 옛 건물이 사라져 있는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Strangler Fig Pattern의 정통 아키텍처는 **4-Layer + 3-Phase** 구조로 정의된다. Martin Fowler의 원문(bliki)에서는 "Transform, Coexist, Eliminate"의 3단계를 제시하며, 이를 실무에선 **IT 현대화 방법론(ADM: Architecture Development Method, TOGAF)**의 Phase B~D와 매핑한다.

```text
+----------------------------------------------------------------+
|  Layer 1: Edge / Facade  --- Kong / Envoy / Nginx-Istio /     |
|                              AWS API GW / Apigee Hybrid       |
|  +----------------------------------------------------------+  |
|  | • Path-based Routing   : /v2/orders/* -> New Service     |  |
|  | • Header-based         : X-Strangler-Canary: A/B        |  |
|  | • Cookie-based         : sessionId=% -> % Routing        |  |
|  | • Tenant-based         : /api/{tenant}/...              |  |
|  | • JWT Claim            : iss, aud, scope, custom claim   |  |
|  +----------------------------------------------------------+  |
+----------------------------------------------------------------+
|  Layer 2: Anti-Corruption Layer (ACL)  --- Hexagonal/Ports   |
|  +----------------------------------------------------------+  |
|  |  Legacy Domain Model  <-->  Translation DTO  <-->  New      |  |
|  |  (COBOL Copybook)         (MapStruct,        Domain     |  |
|  |   VSAM/DB2 Schema)         OpenAPI Generator) Model     |  |
|  +----------------------------------------------------------+  |
+----------------------------------------------------------------+
|  Layer 3: Strangler Services (New MSA) -- 도메인 단위 분해    |
|  +------------+ +------------+ +------------+ +------------+  |
|  | User Svc   | | Order Svc  | | Payment Svc| | Product Svc|  |
|  | (Spring)   | | (Node.js)  | | (Java/Go)  | | (Python)   |  |
|  +------------+ +------------+ +------------+ +------------+  |
+----------------------------------------------------------------+
|  Layer 4: Data Synchronization Plane                          |
|  +----------------------------------------------------------+  |
|  |  • CDC (Change Data Capture) : Debezium -> Kafka -> Sink  |  |
|  |  • Dual-Write + Outbox       : Transactional Outbox      |  |
|  |  • Event Replay              : Kafka Connect / Kinesis  |  |
|  |  • Legacy Read Replica       : Oracle GoldenGate /      |  |
|  |                                SharePlex / AWS DMS      |  |
|  +----------------------------------------------------------+  |
+----------------------------------------------------------------+
```

### 3-Phase Evolution (실무 적용 모델)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Strangler Facade** | 트래픽 라우터, 인증 통합, Rate-Limit | Envoy xDS, Kong(OpenResty/Lua), Istio(Envoy wrapper), AWS API Gateway, Apigee Hybrid. Path/Header/Method/Body 매칭으로 Legacy/New 분기, 카나리 트래픽은 Envoy의 `weighted_clusters`(예: 95/5, 90/10) 또는 Istio VirtualService의 `weight: 90/10`을 사용해 점진적 비율 조절 |
| **Anti-Corruption Layer (ACL)** | 레거시 도메인 ↔ 신규 도메인 번역기 | Hexagonal Architecture의 Port/Adapter, DDD Bounded Context 간 MapStruct, OpenAPI Generator, Avro Schema Registry, Adapter Pattern. 레거시 COBOL Copybook의 `PIC 9(7)V99`(7자리 정수+2자리 소수)를 Java `BigDecimal`로 변환 시 scale/precision 손실 방지를 위한 정밀 매핑 테이블 운영 |
| **Strangler Services (New)** | 도메인 단위 신규 구현체 | Spring Boot 3.x / Quarkus / NestJS / Go-Kit / FastAPI. 데이터베이스는 Polyglot Persistence(PostgreSQL, MongoDB, DynamoDB, Cassandra). 통신은 동기(REST/gRPC), 비동기(Kafka, RabbitMQ, AWS SQS/SNS, Pulsar) 혼용 |
| **Data Sync Plane** | 양쪽 데이터 일관성 유지 | **① CDC**: Debezium(Oracle/MySQL/PostgreSQL log tailing) -> Kafka -> Sink Connector. **② Outbox Pattern**: 동일 트랜잭션 내 Outbox 테이블에 이벤트 기록 -> CDC가 캡처. **③ Event Sourcing**: Aggregate 단위 Event Log 저장. **④ Bulk Backfill**: 초기 1회 Spark/Athena/Snowflake로 히스토리 마이그레이션 |
| **Observability & Governance** | 양 시스템 통합 모니터링 | OpenTelemetry Collector로 양쪽 Trace/Metric/Log 수집 -> Jaeger/Tempo(분산 트레이싱) + Prometheus/Grafana(메트릭) + Loki/ELK(로그). Feature Flag(Unleash, LaunchDarkly)로 신규 기능 On/Off. **Span Correlation**: Facade에서 `traceparent`(W3C Trace Context)를 생성·전파하여 Legacy와 New를 단일 Trace로 연결 |
| **Identity Federation** | 인증/세션 양 시스템 연동 | Legacy WAS 세션(Tomcat `JSESSIONID`/WebLogic `Cookie`/`HttpSession`)을 JWT(RS256, JWE)로 변환하는 **Token Bridge**(Spring Security `OAuth2ResourceServer` + Legacy `SessionRepository`). OAuth2/OIDC(Authorization Code + PKCE) ↔ 레거시 자체 인증 ID/PW 연동 시 `AuthenticationManager`에서 `AuthenticationProvider` 체이닝 |
| **Migration Orchestrator** | 단계별 트래픽 이동·롤백 통제 | Argo Rollouts, Spinnaker, AWS CodeDeploy의 Blue/Green + Canary, Flagger(Progressive Delivery). 카나리 SLO 위반 시 자동 Rollback. 회귀 테스트는 Pact(Contract Test) + Shadow Traffic(미러링, `mirror_percentage: 5%`) + Chaos Engineering(LitmusChaos, Gremlin) |

### 라우팅 알고리즘 의사코드 (Envoy xDS 기반)

```yaml
# EnvoyFilter (Istio VirtualService와 동등)
route_config:
  virtual_hosts:
  - name: legacy_fallback
    domains: ["api.bank.local"]
    routes:
    - match:
        prefix: "/v1/accounts/"
        headers: [{name: ":authority", exact_match: "legacy.bank.local"}]
      route_cluster: legacy_mainframe
      timeout: 30s
    - match:
        prefix: "/v2/accounts/"
        runtime_fraction:
          default_value: 90
          runtime_key: "routing.accounts.v2.weight"
      route_cluster: new_accounts_msa
      request_mirror_policies:
      - cluster: new_accounts_shadow
        runtime_fraction: {default_value: 5, runtime_key: "shadow.percent"}
      retry_policy: {retry_on: "5xx,reset", num_retries: 2}
```

### 데이터 일관성 보장 메커니즘 상세

| 전략 | 적용 시나리오 | 지연(latency) | 일관성 보장 | 도구/패턴 |
|:---|:---|:---:|:---:|:---|
| **Synchronous Dual-Write** | 트래픽 적은 마스터 데이터 | <50ms | At-Most-Once 위험 | Saga Orchestrator (Camunda 8 / Temporal) |
| **Transactional Outbox** | 주문/결제 등 Critical 트랜잭션 | <200ms | At-Least-Once + Idempotency Key | Debezium + Kafka, Outbox 테이블 |
| **CDC (Log-based)** | 대량·실시간 동기화 | <1s | Eventually Consistent | Debezium, Oracle GoldenGate, AWS DMS, Striim |
| **Event Sourcing** | 도메인 이벤트 단위 보존 | 비동기 | Audit-grade | Axon, EventStoreDB, Kafka |
| **API-led ETL** | 초기 Bulk Migration | 수 시간 | Snapshot + Delta | Informatica, Talend, Apache NiFi, Airbyte |
| **Data Virtualization** | Read-only 통합 조회 | <500ms | 쿼리 시점 통합 | Denodo, Dremio, Starburst |

### 핵심 알고리즘·파라미터 결정 공식

- **카나리 진행 속도(SLO 기반 자동화)**:
  $$P_{n+1} = P_n \times (1 + \alpha \cdot \mathbb{1}[\text{SLO}_{\text{error\_rate}} \leq \theta] - \beta \cdot \mathbb{1}[\text{SLO}_{\text{error\_rate}} > \theta])$$
  여기서 $P_n$은 n단계 트래픽 비율, $\theta$는 허용 에러율 SLO(예: 0.1%), $\alpha=0.2$, $\beta=0.5$가 실무 표준 초기값이다.

- **롤백 판정 임계치**: 신규 서비스의 p99 latency가 레거시 대비 **+20% 초과** 또는 에러율 **+0.5%p 초과** 시 자동 Rollback 트리거.

- **DB 분리 전략(데이터베이스 Strangling)**: Chris Richardson의 **"Database per Service"** 원칙에 따라 우선 **단일 DB -> Schema 분리(Schema-per-Service) -> DB 분리(Private DB) -> DB 기술 교체(Polyglot)** 순서로 진행. 즉시 DB 분리 시 2PC(2-Phase Commit) 의존으로 가용성이 떨어지므로, **Trunk-based DB Refactoring + Expand/Contract Pattern**(칼럼 추가 -> 데이터 이관 -> 코드 전환 -> 칼럼 제거)을 사용한다.

- **📢 섹션 요약 비유**: 새 심장(신규 서비스)을 이식할 때, **인공심장기(Bypass = Fac
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 456 / 600

<- **이전**: [455. 사가 패턴 분산 트랜잭션 보상](/studynote/12_it_management/05_security_compliance/948_saga_pattern)
**다음**: [457. API 게이트웨이 패턴 라우팅 인증](/studynote/11_design_supervision/06_exam_summary/457_api_gateway_pattern/) ->

---
