---
title: "580. 컴포저블 아키텍처 모듈화 재사용 (Composable Architecture Modular Reuse)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MACH(Microservices, API-first, Cloud-native, Headless) 원칙을 기반으로, 애플리케이션을 독립 배포 가능한 **PBC(Packaged Business Capability)** 단위로 분해하고 표준 API/이벤트 인터페이스로 느슨하게 결합(Loose Coupling)하여 런타임에 조립(Composition)하는 아키텍처 스타일이다.
> 2. **가치**: Gartner 예측 기준 컴포저블 기업은 신규 기능 출시 속도(Lead Time)가 평균 **4배**, TTM(Time-to-Market) **50% 단축**, 그리고 기능별 **Best-of-Breed** 선택을 통해 동일 예산 대비 비즈니스 성과 30% 이상 개선 효과를 보인다.
> 3. **판단 포인트**: 모든 시스템에 적용 시 발생하는 **분산 트랜잭션(Saga) 복잡도**, **데이터 중복/일관성(CQRS+Eventual Consistency)**, **운영 부담(Observability/FinOps)** 을 감당할 수 있는 조직적 성숙도(Conway's Law 관점)가 핵심 결정 변수이며, **Modular Monolith -> PBC -> Composable** 로 점진적 이행하는 것이 리스크 최소화의 정석이다.

---

## Ⅰ. 개요 및 필요성

전통적인 **Monolithic Architecture**(예: SAP ERP, Oracle Commerce, Liferay DXP)는 CRM, 결제, 재고, 콘텐츠, 검색을 단일 코드베이스와 단일 릴리즈 트레인에서 관리한다. 이는 초기 개발 속도는 빠르지만, **10년 이상 운영된 레거시**에서는 ① 릴리즈 주기가 월 1회 이하로 느려지고, ② 한 컴포넌트 변경이 전체 시스템 회귀 테스트를 유발하며, ③ 특정 기능(예: 검색)만 SaaS로 교체할 수 없어 **Vendor Lock-in** 에 갇히게 된다. 실제로 Forester 2023 보고서에 따르면 monolithic commerce 플랫폼의 평균 신규 기능 배포 주기는 **8.5주**, 컴포저블 아키텍처 적용 기업은 **1.7주** 으로 격차가 벌어지고 있다.

이러한 문제를 해결하기 위해 Gartner(2021)는 **Composable Business** 를 전략적 기술 트렌드로 선정하고, 이를 구현하는 기술 아키텍처로 **Composable Architecture** 를 제시했다. 핵심 사고방식은 "비즈니스 역량(Business Capability)을 더 작은 **PBC(Packaged Business Capability)** 단위로 패키징하고, API와 이벤트로 외부에 노출하여 마치 레고 블록처럼 조립하라"는 것이다.

```text
+----------------------- Legacy Monolithic -----------------------+
|  +---------+---------+---------+---------+---------+           |
|  |   UI    |  CMS    |  Search | Commerce|   CRM   |  Coupled  |
|  |  Layer  | Module  |  Engine |  Module |  Module |   WAR/EAR |
|  +----+----+----+----+----+----+----+----+----+----+  --------|
|       +----------+---------+---------+---------+              |
|                         Shared DB                              |
+----------------------------------------------------------------+
                          v Decompose v
+------------------ Composable Architecture ------------------+
|   [PBC: Search]    [PBC: Commerce]    [PBC: CMS]   [PBC:CRM] |
|   (Algolia)        (commercetools)   (Contentful) (Salesforce)
|   -+-              -+-               -+-           -+-       |
|    | REST/gRPC      | GraphQL         | REST        | oData  |
|   -+----------------+-----------------+-------------+---     |
|              +------------------------------+                |
|              |  API Gateway / BFF (GraphQL  |                |
|              |  Federation, Apollo Router)  |                |
|              +--------------+---------------+                |
|                             |                                |
|              +--------------+---------------+                |
|              |   Event Bus (Kafka/NATS)     |  Pub/Sub       |
|              |   topic: order.created       |                |
|              +------------------------------+                |
+--------------------------------------------------------------+
```

**왜 필요한가? (Old vs New Paradigm)**

| 차원 | Monolithic (Old) | Composable (New) |
| :--- | :--- | :--- |
| 변경 영향도 | 전체 빌드/배포 | PBC 단위 독립 배포 |
| 확장 단위 | 수평(전체 인스턴스) | 수직/수평(PBC별 셀별) |
| 기술 선택 | 단일 언어/프레임워크 | Polyglot(Python+Go+Node 공존) |
| 장애 영향 | 전체 장애 가능 | Blast Radius 격리 (Circuit Breaker) |
| 벤더 종속 | All-or-Nothing | Best-of-Breed 조립 |
| 조직 구조 | 기능별 팀(Feature Team) | **스트림 정렬 팀(SAFe/Spotify Model)** |

- **📢 섹션 요약 비유**: 옛날의 짜장면 배달 세트 메뉴(모든 토핑이 한 그릇에 섞여 있음)와, 요즘의 **누구나 조합하는 커스텀 도시락**(메인, 반찬, 국을 각 코너에서 따로 담아 선택)이 다른 것과 같다. 한 코너의 메뉴가 바뀌어도 다른 코너는 영향이 없고, 원하는 코너만 교체할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

컴포저블 아키텍처는 **3계층(Experience -> Composition -> PBC)** 으로 구성된다. 상위에서 하위로 흐르는 **요청 흐름(Request Flow)** 과, 하위에서 상위로 흐르는 **이벤트 흐름(Event Flow)** 이 **API Gateway / Event Bus** 를 통해 양방향으로 연결된다.

```text
+--------------------------------------------------------------+
|                  Experience Layer (Touchpoints)              |
|  Web App | Mobile | Voice | Kiosk | Marketplace | In-Store  |
|   (Next.js) (RN)  (Alexa)  (PWA) (Mirakl)     (PWA)        |
+-------------------------+------------------------------------+
                          | BFF / GraphQL Federation
                          v
+--------------------------------------------------------------+
|              Composition Layer (조립/오케스트레이션)           |
|   +-----------------------------------------------------+   |
|   |  GraphQL Federation (Apollo Router v1.20+)          |   |
|   |  - Schema Stitching / Entity Resolver               |   |
|   |  - @key directive 로 도메인 모델 통합                |   |
|   +-----------------------------------------------------+   |
|   +------------------+  +------------------------------+   |
|   | BFF (Node/Go)     |  | Workflow Orchestrator        |   |
|   | per Channel       |  | (Temporal/Camunda 8/Zeebe)   |   |
|   +------------------+  +------------------------------+   |
+-------------------------+------------------------------------+
                          | REST/GraphQL/gRPC + Webhook
                          v
+--------------------------------------------------------------+
|            PBC Layer (Packaged Business Capability)         |
|  +----------+ +----------+ +----------+ +----------+        |
|  |  Cart    | | Pricing  | | Inventory| |  Search  |        |
|  | (Medusa) | |(Promo Svc)| |(SAP IS) | |(Algolia) |        |
|  |  Port    | |  Port    | |  Port    | |  Port    |        |
|  +----+-----+ +----+-----+ +----+-----+ +----+-----+        |
|       |            |            |            |               |
|       | Outbox -> Kafka: order.events, price.events           |
|       +------------+------------+------------+               |
+--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **PBC (Packaged Business Capability)** | 하나의 비즈니스 역량을 자체적으로 완결(Autonomous)하여 제공하는 패키지. 내부 구현은 Black-Box. | Shopify Functions, commercetools Extension API, Salesforce AppExchange, Stripe Connect 처럼 자체 API/SDK/Event 를 통해 외부에 **계약(Contract)** 노출. DDD의 **Bounded Context** 와 1:1 매핑 권장. |
| **API Gateway / BFF** | 다수의 PBC 호출을 단일 엔드포인트로 통합하고, 인증/인가, Rate Limiting, 캐싱 적용. | Kong(3.6+), AWS API Gateway, Apigee, 그리고 **Apollo Router**(GraphQL Federation v2). 채널별(Web/Mobile) **BFF(Backend for Frontend)** 분리 패턴(Netflix OSS, Sam Newman 저서). |
| **Event Bus / Message Broker** | PBC 간 비동기 결합을 제공하여 결과적 일관성(Eventual Consistency) 보장. | **Apache Kafka**(Partitioning + Exactly-Once Semantics), **NATS JetStream**(경량), **RabbitMQ**(트랜잭셔널), **AWS EventBridge**, **Confluent Schema Registry** 로 Avro/JSON-Schema 진화 관리. |
| **Composition Layer (Orchestration)** | 여러 PBC 호출을 워크플로우로 조합하여 트랜잭션 의미 제공. | **Saga Pattern**(Orchestration vs Choreography), **Temporal**(Workflow-as-Code, Go/TS SDK), **Camunda 8**(BPMN + Zeebe), **Apache Airflow**(배치성 오케스트레이션). |
| **Service Mesh & Observability** | PBC 간 mTLS, 트래픽 관리, 분산 추적, 메트릭 수집. | **Istio 1.20+** Ambient Mesh(Sidecar-less), **Linkerd 2.15** Proxy, **OpenTelemetry Collector**, **Grafana Tempo/Loki/Mimir**, **Datadog APM**, **Honeycomb.io** OpenTelemetry 호환. |
| **Headless Presentation** | 비즈니스 로직이 없는 순수 표현 계층, 다양한 채널에 동일 API 재사용. | **Next.js App Router**(React Server Components), **Nuxt 3**, **Remix**, **Astro**(Islands Architecture), 그리고 **Micro Frontend**: Module Federation 2.0(Webpack 5/Turbopack), Single-SPA, qiankun. |
| **Developer Portal / Internal Platform** | PBC 카탈로그, API 문서, 셀프서비스 프로비저닝. | **Backstage.io**(Spotify), **Port.io**, **Apicurio**, **Stoplight Elements**. IDP(Internal Developer Platform) 패턴. |

**핵심 원리 심화**

1. **계약 우선 설계(API-First + Contract-Driven Development)**: PBC는 OpenAPI 3.1 / GraphQL SDL / AsyncAPI 3.0 명세를 **Single Source of Truth** 로 삼고, 코드보다 먼저 스키마를 git에 커밋. 소비자(PBC-B)는 이 명세로 **계약 테스트(Pact, Spectral)** 를 수행하여 배포 안전성 확보.

2. **이벤트 기반 결합(EDA + Outbox Pattern)**: PBC 내부 DB 트랜잭션과 외부 이벤트 발행을 원자적으로 보장하기 위해 **Transactional Outbox** 패턴 사용. Debezium CDC(Change Data Capture)로 outbox 테이블을 캡처하여 Kafka로 발행(예: order-service DB -> debezium -> kafka topic `order.v1`).

3. **데이터 소유권 원칙(You Build It, You Run It, You Own Its Data)**: 각 PBC는 자기 도메인의 데이터를 **독점**하고, 다른 PBC는 직접 JOIN하지 않음. 통합은 API 또는 이벤트로만. 필요 시 **API Composition** 또는 **CQRS + Read Model 복제** 로 해결.

4. **셀 아키텍처(Amazon 2-Pizza Team + Cell-Based Architecture)**: 한 팀이 1개 PBC의 설계-구현-배포-운영-SRE 책임을 모두 지는 Conway's Law 역이용. Spotify Squad -> GitHub Team -> PBC Owner 로 연결.

```text
Saga Orchestration (주문-결제-재고-배송 예시)

  Order BFF ---> Order PBC (Orchestrator, Local TX)
                   |
                   | Step1. createOrder (Local DB)
                   |
                   | ---- Command ----> Payment PBC
                   |                       (charge, Reply)
                   |     ACK          +- 보상(Refund) --+
                   | <--------------- |                  |
                   |
                   | ---- Command ----> Inventory PBC
                   |                       (reserve)
                   |     ACK
                   | <--------------- 보상(release)
                   |
                   | ---- Event ------> Shipping PBC (Choreography)
                   |     order.created
                   | <-------- order.shipped
                   v
              Saga Complete / Compensating Actions Rollback
```

- **📢 섹션 요약 비유**: 컴포저블 아키텍처는 **자석 블록(LEGO + Smart Brick)** 이다. 각 블록은 자기 핀(Pin)을 통해 결합 패턴을 알고 있고, 나사를 다시 조이지 않아도 똑딱 맞물린다. 만약 한 블록에 균열이 생겨도 그 블록만 교체하면 되며, 다른 블록은 무관하게 동작한다. 이것이 **느슨한 결합(Loose Coupling)** 의 본질이다.

---

## Ⅲ. 비교 및 연결

| 구분 | Composable Architecture | Microservices Architecture | Modular Monolith | SOA (Service-Oriented Architecture) |
| :--- | :--- | :--- | :--- | :--- |
| **유래/시대** | Gartner 2021, MACH 2020~ | Fowler 2014, Netflix/AWS | Shop(Shopify 내부), Simon Brown | OASIS 2000년대, WSDL/SOAP |
| **결합 단위** | PBC (Bounded Context + SaaS 가능) | Service (논리적 분리) | Module (단일 배포 단위) | Service (ESB 통해 통신) |
| **데이터 정책** | PBC별 독립 DB + 이벤트 공유 | DB-per-service | 통합 DB, 스키마 분리 | 중앙 DB 또는 Data Service |
| **통합 방식** | API-first + Event-driven | REST/gRPC 위주, EDA 병행 | In-process function call | ESB(Enterprise Service Bus) |
| **구현 예** | commercetools + Algolia + Contentful | Netflix OSS, Uber Domain | Shopify Rails 모놀리식, Amazon 내부 초기 | SAP NetWeaver, TIBCO |
| **기술 독립성** | Best-of-Breed (언어/DB 자유) | 가능 (Polyglot) | 불가 (단일 스택) | 제한적 |
| **조직 단위** | **PBC Squad + IDP** | DevOps 팀 | 모놀리식 팀 | Center of Excellence |
| **적합 시나리오** | 빠른 시장 대응, 디지털 커머스, M&A 잦은 기업 | 대규모 트래픽, 클라우드 네이티브 | 초기 스타트업, 단일 도메인 | 레거시 통합, 엔터프라이즈 허브 |
| **도입 난이도** | 매우 높음 (벤더
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 580 / 600

<- **이전**: [579. 하이퍼오토메이션 AI 융합 자동화](/studynote/11_design_supervision/06_exam_summary/580_hyperautomation_ai_convergence_automatio/)
**다음**: [581. 제로 트러스트 아키텍처 감리 관점](/studynote/11_design_supervision/06_exam_summary/581_zero_trust_architecture_audit_perspectiv/) ->

---
