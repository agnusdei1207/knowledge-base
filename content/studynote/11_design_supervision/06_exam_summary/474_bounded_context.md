+++
title = "474. 바운디드 컨텍스트 컨텍스트 매핑 (Bounded Context Context Mapping)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 바운디드 컨텍스트(Bounded Context)는 단일 도메인 모델이 의미를 가지는 명시적 경계이며, 컨텍스트 매핑(Context Mapping)은 이 경계들 사이의 관계(U/D: Upstream/Downstream)와 통합 패턴(Shared Kernel, ACL, OHS 등)을 전략적으로 정의하여 다중 모델 간의 충돌을 제거하는 DDD 전략 설계의 핵심 메커니즘이다.
> 2. **가치**: 컨텍스트 매핑을 적용 시 도메인 모델의 경계 명확화로 모델 무결성 100% 유지가 가능하며, 팀 토폴로지와의 정렬을 통해 조직 구조(Conway's Law)와 시스템 아키텍처의 일치를 통한 변경 전파 속도를 평균 40~60% 단축할 수 있다.
> 3. **판단 포인트**: Shared Kernel(결합도 ↑, 도메인 정합성 ↑) vs Separate Ways(결합도 ↓, 중복 ↑)의 트레이드오프, Anti-Corruption Layer의 변환 비용 vs Conformist의 의존성 수용, 그리고 비즈니스 연속성을 위한 Open-Host Service의 API 안정성 정책 수립이 핵심 의사결정 요인이다.

---

## Ⅰ. 개요 및 필요성

기존 모놀리식 시스템에서는 단일 도메인 모델("Account", "Product", "Order" 등)이 전사적으로 강제 적용되어왔다. 이로 인해 **소프트웨어 도메인 모델의 분열(Domain Model Divergence)** 현상이 발생한다. 같은 "고객(Customer)"이라는 용어라도 CRM 팀은 '마케팅 관점의 잠재고객+기존고객+이탈고객'을 의미하고, Billing 팀은 '과금 대상+결제수단+신용등급'을 의미하며, Delivery 팀은 '수령지+배송상태+물류정보'로 해석한다. 이처럼 **Ubiquitous Language(보편 언어)**는 단일 조직 내부에서도 의미가 다층적으로 존재하며, 이를 무시한 통합은 **Big Ball of Mud** 안티패턴으로 귀결된다.

Eric Evans의 DDD(Domain-Driven Design, 2003)에서는 이러한 문제를 해결하기 위해 **Bounded Context**라는 경계 안에서만 단일 모델과 언어가 의미를 갖도록 제한하고, **Context Map**을 통해 경계들 간의 관계를 명시적으로 문서화하도록 강제한다. 이는 마이크로서비스 아키텍처(MSA, 2014~)와 결합되면서, 각 서비스를 도메인 단위의 Bounded Context로 매핑하는 현대 클라우드 네이티브 설계의 표준 패턴이 되었다.

기존의 **Enterprise Service Bus(ESB)** 기반의 거대한 통합 레이어 패턴이 갖는 결합도·단일 장애점·확장성 문제를 해결하고, 도메인별로 자율성을 부여하면서도 비즈니스 정합성을 유지하는 현대적 해법이 바로 Context Mapping이다.

```text
[기존 모놀리식 모델의 문제: 다층적 의미 충돌]

  ┌─────────────────────────────────────────────────────┐
  │  단일 통합 도메인 모델 (Monolithic Domain Model)      │
  │                                                     │
  │   "Customer" 라는 단일 엔터티로 통합 시:              │
  │   ┌──────────────┬──────────────┬──────────────┐     │
  │   │  CRM 모듈    │ Billing 모듈 │  Delivery    │     │
  │   │  Customer    │ Customer     │  Customer    │     │
  │   │ ─────────── │ ──────────── │ ──────────── │     │
  │   │  잠재고객    │  과금대상    │  수령인       │     │
  │   │  리드스코어  │  결제수단    │  배송지       │     │
  │   │  캠페인반응  │  신용등급    │  배송상태     │     │
  │   │  이탈예측    │  청구이력    │  도착예정     │     │
  │   └──────────────┴──────────────┴──────────────┘     │
  │         ↓ ↓ ↓ 모순·중복·결합도 급증                  │
  │      [Big Ball of Mud / 대혼란]                      │
  └─────────────────────────────────────────────────────┘

[Bounded Context + Context Map으로 해결]

  ┌────────────┐    Context Map    ┌────────────┐
  │    CRM     │ ←──Conformist───→ │  Billing   │
  │  Context   │                   │  Context   │
  │            │    ┌───ACL────┐   │            │
  │ Customer   │ ←──┤  변환    ├──→│ Customer   │
  │ (잠재고객)  │    │  Layer   │   │ (과금대상)  │
  └────────────┘    └───────────┘   └────────────┘
        │                              │
        │ Published Language           │ Open Host
        │ (Avro/JSON Schema)            │ Service (REST)
        ↓                              ↓
  ┌────────────┐                 ┌────────────┐
  │  Delivery  │                 │  Analytics │
  │  Context   │                 │  Context   │
  └────────────┘                 └────────────┘
  → 각 Context는 자기만의 "Customer" 모델과
    Ubiquitous Language를 가짐
```

기존 모델에서는 `Customer`가 모든 하위 모듈에 강제 동일하게 적용되어 모델의 무결성이 깨지고, 변경 시 도미노 효과(Ripple Effect)가 발생했다. Bounded Context + Context Map은 이를 **경계(Boundary)**로 분리하고, **의도적 변환(Translation)**과 **명시적 의존 관계**로 대체한다.

- **📢 섹션 요약 비유**: 마치 같은 '밥'이라는 단어가 한국에서는 흰쌀밥, 이탈리아에서는 리조또, 일본에서는 초밥, 인도에서는 비르야니인 것처럼, 같은 'Customer'도 부서(주방)마다 다른 의미를 가지므로 각 주방(Bounded Context) 안에서만 자기만의 레시피(모델)를 유지하고, 사이에는 번역가(ACL/Translator)를 두는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Bounded Context는 단순한 패키지 경계가 아니라 **모델의 의미론적 경계(Semantic Boundary)**이다. 이 경계 안에서 도메인 모델, 용어, 비즈니스 규칙, 트랜잭션 무결성이 일관되게 유지된다. Context Mapping은 이 경계들 사이의 **상류(U: Upstream)**와 **하류(D: Downstream)** 관계 및 통합 방식을 정의한다. 상류는 모델을 제공(제공자)하는 측, 하류는 모델을 소비(소비자)하는 측이다.

핵심 통합 패턴은 Eric Evans의 원본 7개 패턴에 Vaughn Vernon이 2개를 추가하여 9개로 확장되었다.

```text
[Context Map 상세 관계도: 항공 도메인 예시]

  ┌──────────────────────────────────────────────────────┐
  │  Marketing Context (Core Subdomain)                  │
  │  ┌──────────────┐  Pro: 캠페인/프로모션/세그먼트      │
  │  │  Campaign    │  Customer = 잠재고객+리드            │
  │  │  Lead        │                                    │
  │  └──────┬───────┘                                    │
  │         │                                            │
  │         │ (1) OHS + Published Language               │
  │         │     GET /campaigns/active?segment=...      │
  │         │     Schema: Avro "CampaignEvent.avsc"      │
  │         │                                            │
  │  ───────┴──── U/D 경계 (Upstream→Downstream) ──────  │
  │         │                                            │
  │  ┌──────┴───────┐  (2) Customer-Supplier            │
  │  │  Booking     │  Model: 예약/좌석/탑승객            │
  │  │  Reservation  │  Customer = 탑승객+여정정보         │
  │  │  Context      │  하류팀이 상류팀에 우선순위 요청O   │
  │  └──────┬───────┘                                    │
  │         │                                            │
  │  ───────┴──── Shared Kernel (항공편 코드) ─────────  │
  │         │         "KE703", "ICN", "JFK"              │
  │         │         [중복 도메인 모델 - 양 팀 합의]     │
  │         │                                            │
  │  ┌──────┴───────┐  (3) ACL (Anti-Corruption Layer)   │
  │  │  Loyalty     │  Marketing의 "Lead"를               │
  │  │  Mileage     │  "Member + Tier" 로 변환            │
  │  │  Context     │  Translator: LegacyMainframeAdapter│
  │  └──────┬───────┘                                    │
  │         │                                            │
  │         │ (4) Conformist                              │
  │         │     "Legacy Reservation System"             │
  │         │     SOAP/XML 인터페이스 그대로 수용         │
  │         │     (변환 비용 감수)                         │
  │         │                                            │
  │  ┌──────┴───────┐                                    │
  │  │   Legacy     │  Generic Subdomain                  │
  │  │   Mainframe  │  (외부 SaaS - Sabre/Amadeus)        │
  │  │   GDS        │  Separate Ways: 일부 기능은         │
  │  └──────────────┘  직접 GDS API 호출                  │
  └──────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Bounded Context (BC)** | 도메인 모델의 의미론적 경계, 트랜잭션 일관성 보장 경계, 마이크로서비스의 자연스러운 경계 | Aggregate Root 단위의 트랜잭션 정합성, 단일 Ubiquitous Language 강제, 패키지/모듈/네임스페이스(`com.kakao.pay.order`) 분리. Event Storming으로 도메인 이벤트를 도출하여 BC 경계 후보를 식별함 |
| **Context Map** | BC들 간의 관계와 통합 방식을 명시적으로 문서화한 2D 다이어그램 (U/D 화살표 + 패턴 라벨) | 화살표의 방향이 데이터/의존성 흐름을 의미, 각 화살표에 Partnership/ACL/Shared Kernel 등의 라벨 부착. 보통 C4 Model의 System Context Diagram + Sequence Diagram을 함께 사용 |
| **Subdomain 분류** | Core(핵심 차별화), Supporting(보조), Generic(범용/외부 도입) | Core는 내부 정예팀(Strategic Investment), Supporting은 내부 개발(Internal Investment), Generic은 SaaS/Package 도입(Outsource). Netflix Conductor, Kafka 같은 범용 솔루션은 Generic으로 분류 |
| **Context Mapping 패턴** | BC 간 통합 시 발생할 수 있는 7~9가지 표준 시나리오 정의 | Partnership(동기적 공동 진화), Shared Kernel(일부 모델 공유), Customer-Supplier(우선순위 협상), Conformist(있는 그대로 수용), Anti-Corruption Layer(번역 계층), Open-Host Service(안정적 공개 API), Published Language(공용 스키마), Separate Ways(통합 안 함), Big Ball of Mud(레거시 존중) |
| **Anti-Corruption Layer (ACL)** | 외부 시스템/레거시/타 BC의 모델을 내부 도메인 언어로 변환하는 격리 레이어 | Hexagonal Architecture의 Adapter 패턴, `LegacyBillingTranslator.translateToInternalFormat(rawDTO)`, 데이터 매핑은 MapStruct/Java/Kotlin Extension Func, 도메인 이벤트를 `DomainEvent → ExternalEvent`로 직렬화할 때도 활용 |
| **Open-Host Service (OHS)** | BC가 자신을 사용하는 모든 다운스트림에게 일관된 안정적 인터페이스를 공개 | REST API + HATEOAS, gRPC + Protocol Buffers, GraphQL Federation, Kafka Schema Registry(Confluent) + Avro/Protobuf로 스키마 진화 관리. **API 버전 호환성 전략**(URI versioning vs Header versioning vs Semantic versioning)이 핵심 |

**기술적 세부 고려사항:**

- **OHS API 버전 관리**: 하류 컨슈머(다른 BC)를 보호하기 위해 `v1`, `v2` URI 분리, `Sunset` 헤더와 `Deprecation` 정책 수립. Netflix는 **API Deprecation Pipeline**을 운영하여 자동 폐기 일정 통보.
- **Shared Kernel의 위험성**: 두 팀이 공유 모델을 변경 시 양 팀의 배포가 동기화되어야 하므로 **테스트 슈트 공유 + CI 통합**이 필수. Vernon은 Shared Kernel이 비대해질 경우 다시 Customer-Supplier로 분리할 것을 권고.
- **ACL의 위치**: DDD Layered Architecture에서 Interface Adapters 계층에 위치하며, 외부에서 들어오는 모든 메시지(DTO, Event, JSON, XML)는 여기서 도메인 객체로 변환되어야 함. Spring/Kotlin에서는 `AntiCorruptionTranslator` 컴포넌트로 캡슐화.
- **Subdomain → Bounded Context 매핑 비율**: 통상 1:1을 권장하나, Core Subdomain이 지나치게 크면 1:N 분할, 반대로 Supporting 두 개가 응집력이 높으면 N:1 통합을 검토.

- **📢 섹션 요약 비유**: 바운디드 컨텍스트는 각각의 '도시(City)'이고, 컨텍스트 매핑은 도시 간의 '외교 협정'과 같다. 어떤 도시는 동맹(Partnership), 어떤 도시는 보호국(Customer-Supplier), 어떤 도시는 통역사(ACL)를 두고 교류하며, 어떤 도시는 자급자족(Separate Ways)한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **Bounded Context (전략 패턴)** | **Microservices (배포 단위)** | **Monolithic (모놀리식)** |
| :--- | :--- | :--- | :--- |
| **경계의 본질** | 도메인 모델의 의미론적 경계 (논리적) | 독립 배포 가능한 프로세스 (물리적) | 단일 코드베이스, 단일 프로세스 |
| **데이터 정합성** | BC 내 강한 일관성(Strong Consistency), BC 간은 결과적 일관성(Eventual Consistency) via Saga/Choreography | DB per Service, 각 서비스가 자기 DB 소유 (CAP 정리 적용) | 단일 트랜잭션으로 ACID 강제 |
| **팀 구조** | Team Topologies: Stream-Aligned Team + Enabling Team | Conway's Law 역이용, 2-pizza team (Amazon 규칙) | Feature Team, 계층별 전담팀 |
| **통합 방식** | Context Mapping 패턴 (ACL, OHS, Shared Kernel 등) | REST/gRPC/Async Messaging, Service Mesh(Istio) | In-process method call, Shared Library |
| **변경 영향도** | 컨텍스트 내 변경은 자족, 외부 인터페이스만 영향 | 서비스 단위 배포, 전파 한정 가능 (단, 분산 트랜잭션 복잡) | 작은 변경이 전체 빌드/배포 트리거 |
| **조직/비용** | 도메인 이해도↑, 초기 모델링 비용↑ | 인프라 자동화 필수 (K8s, CI/CD), 운영 복잡도↑ | 초기 빠름, 장기 부채 누적 |

**Context Map vs ERD/Class Diagram:** ERD는 데이터 구조의 정적 관계, Context Map은 **팀 간의 힘의 분포(U/D)**와 **통합 패턴의 의도**를 표현한다. 즉, "누가 누구에게 맞춰야 하는가(Conformist vs Customer-Supplier)"라는 조직·계약적 관계를 보여준다.

**Team Topologies와의 결합:** Matthew Skelton & Manuel Pais의 Team Topologies(2019)는 DDD의 Bounded Context를 팀 경계로 직접 매핑한다. **Stream-Aligned Team**(핵심 BC 담당), **Enabling Team**(기술 역량 지원), **Complicated-Subsystem Team**(기술 집약적 BC), **Platform Team**(내부 PaaS)을 정의하며, 4가지 팀 상호작용(Collaboration, X-as-a-Service, Facilitating, SRE)도 Context Map에 명시한다.

- **📢 섹션 요약 비유**: 모놀리식은 '한 권의 두꺼운 백과사전', 마이크로서비스는 '개별 출판된 시리즈 책들', 바운
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 474 / 600

<- **이전**: [473. 도메인 주도 설계 DDD 전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/474_ddd_strategic_pattern/)
**다음**: [475. 애그리게이트 루트 일관성 경계](/knowledge-base/studynote/11_design_supervision/06_exam_summary/475_aggregate_root/) ->

---
