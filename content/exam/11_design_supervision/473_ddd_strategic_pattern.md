---
title: "Domain Driven Design DDD Strategic Pattern"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DDD 전략 패턴(Strategic Pattern)은 Bounded Context(제한된 컨텍스트), Context Map(컨텍스트 맵), Subdomain(하위 도메인)이라는 세 가지 축을 통해 도메인 경계를 설정하고, Partnership·Shared Kernel·Customer-Supplier·Conformist·Anti-Corruption Layer·Open-Host Service·Published Language·Separate Ways 등의 통합 패턴으로 컨텍스트 간 협력 관계를 명세화하는 기법이다.
> 2. **가치**: 마이크로서비스, 모놀리식 모듈화, SOA 등 시스템 분해 시 도메인 경계의 모호성으로 인한 변경 전파, 데이터 불일치, 팀 간 마찰 비용을 평균 30~50% 절감하며, Conways Law(콘웨이 법칙)와 팀 토폴로지(Team Topologies) 관점에서 팀 경계와 코드 경계를 1:1로 정렬하여 인지 부하(Cognitive Load)와 배포 실패율을 현저히 낮춘다.
> 3. **판단 포인트**: Subdomain 분류(Core/Supporting/Generic)와 Bounded Context 분리 기준, Context Map 표현의 정확성, 그리고 통합 패턴 선택 시 트랜잭션 일관성·계약 진화·조직 구조·기술 부채 간의 트레이드오프를 종합적으로权衡해야 하며, 특히 Anti-Corruption Layer 도입은 변환 로직의 복잡도와 운영 비용을 수반하므로 정당화 근거가 필수적이다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 시스템이 대형화되면서 한정된 도메인 모델로 전체 시스템을 표현하려는 시도는 필연적으로 **Bounded Context 경계의 붕괴**를 초래한다. Eric Evans가 2003년 저서 *Domain-Driven Design*에서 제시한 전략 패턴은 코드 레벨의 전술적 패턴(Aggregate, Entity, Value Object 등)과 분리되어, **"어디에 경계를 그을 것인가(Where to draw the line)"** 라는 비즈니스 우선 의사결정 문제를 다룬다.

전통적인 데이터 중심 설계(Anemic Domain Model, 테이블 주도 설계)에서는 한 테이블을 여러 모듈이 공유하면서 스키마 변경 시 폭발 반경(Blast Radius)이 전체 시스템으로 확산된다. 또한 마이크로서비스 도입 초기 단계에서 **Domain-Driven Design 없이 서비스를 분할**하면, 데이터베이스 중심의 CRUD API가 모놀리식과 다름없이 분산되어 도메인 무결성을 잃고, 결과적으로 **Distributed Monolith(분산 모놀리식)** 라는 최악의 아키텍처 안티패턴이 출현한다.

전략 패턴은 이를 해결하기 위해 **(1) 비즈니스 문제 공간(Problem Space)** 의 Subdomain 분류, **(2) 솔루션 공간(Solution Space)** 의 Bounded Context 매핑, **(3) 두 공간을 잇는 Context Map** 으로 구성된 3단계 추상화 모델을 제시한다. 핵심은 기술적 편의가 아닌 **비즈니스 경쟁 우위(Core Domain)** 를 기준으로 투자 비중을 차등화하는 데 있다.

```text
+---------------------------------------------------------------------+
|           전략 패턴의 3단계 추상화 모델 (Evans 2003)                |
+---------------------------------------------------------------------+
|                                                                     |
|   [Problem Space]            [Solution Space]       [Glue Layer]    |
|   (업무 분석가 영역)          (소프트웨어 영역)       (협업 명세)     |
|                                                                     |
|   +--------------+          +--------------+       +----------+    |
|   |  Subdomain   |   ->->->    |   Bounded    |  ->->   | Context  |    |
|   |  · Core      |   1:N    |   Context    |   N:M |   Map    |    |
|   |  · Supporting|   매핑   |  · Model     |  관계  | · 패턴   |    |
|   |  · Generic   |          |  · Lang(uage)|  명세  | · DDD    |    |
|   +--------------+          +--------------+       +----------+    |
|         |                          |                     |         |
|         v                          v                     v         |
|   "무엇을(What)"             "어떻게(How)"         "누가 누구와(Who)|
|    비즈니스 역량            모델·코드·DB 경계      어떤 관계인가"     |
+---------------------------------------------------------------------+
```

기존 패러다임 대비 DDD 전략 패턴의 차별점은 다음과 같다.

| 관점 | 데이터 중심 설계 (1990s~2000s) | 마이크로서비스 우선 (2014~) | **DDD 전략 패턴** |
| :--- | :--- | :--- | :--- |
| **분해 기준** | 데이터베이스 테이블/ERD | 기술적 단위(팀, 배포 빈도) | 비즈니스 유비쿼터스 언어와 컨텍스트 경계 |
| **변경 영향** | 한 테이블 수정 시 전체 영향 | 서비스 간 API 계약 변동 시 폭발 | Bounded Context 내부로 변경 완전 격리 |
| **팀 구조** | 계층별(UI/BL/DA) | 서비스별(Conway 역행) | **Stream-Aligned Team** × Bounded Context 1:1 |
| **일관성 모델** | 강한 일관성(ACID, 단일 DB) | 강한 일관성 강요 시 Saga 복잡도 폭증 | Context별 자율 일관성, **경계 간 최종 일관성(Eventual Consistency)** 수용 |

- **📢 섹션 요약 비유**: 전략 패턴은 마치 **도시 계획의 토지 용도 zoning(지구 계획)** 과 같다. 주거·상업·공업 지역을 명확히 구분(Subdomain/Bounded Context)하지 않으면, 한 지역의 공장 소음이 주거 지역을 오염시키고, 뒤늦게 용도를 변경하는 비용은 기하급수적으로 증가한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Subdomain(하위 도메인) 분류 체계

Subdomain은 실제 업무 세계의 문제 분해 단위이며, 기술적 산출물이 아니다. Evans는 이를 세 가지로 분류하며 각기 다른 투자·팀 구성 전략을 요구한다.

```text
+----------------------------------------------------------------------+
|                Subdomain 분류 매트릭스 (투자/차별화 관점)             |
+----------------------------------------------------------------------+
|                                                                      |
|   차별화 가치(Competitive Value)                                     |
|        ^                                                            |
|   높음 |              ★ Core Domain(핵심 도메인)                    |
|        |              - 사내 정예 팀 + 외부 전문가(예: 1:1 모델링)    |
|        |              - 비즈니스 규칙 복잡, 변경 빈도^               |
|        |                                                            |
|        |   ● Supporting Domain                ○ Generic Domain      |
|        |   (지원 도메인)                        (일반 도메인)         |
|        |   - 사내 개발                           - COTS/OSS 구매      |
|        |   - 보조 기능                           - 외부 위탁 가능     |
|        |   - Core의 경쟁력 보완                  - "차별화 없음"      |
|   낮음 |                                                            |
|        +--------------------------------------------------->         |
|                  낮음                복잡도/내재화 가치              높음   |
+----------------------------------------------------------------------+
```

**Subdomain 분류의 핵심 파라미터**

| 파라미터 | Core Domain | Supporting Domain | Generic Domain |
| :--- | :--- | :--- | :--- |
| 비즈니스 차별화 | **극대**(직접 수익 영향) | 중간(보완 역할) | 없음(범용 기능) |
| 예시 (이커머스) | 가격/프로모션 엔진, 추천 | 재고 관리, 정산 | 결제 게이트웨이, 이메일 발송 |
| 구현 권장 | **Custom Build**(in-house) | Custom Build or 협업 | **Buy**(Stripe, SendGrid, Keycloak) |
| 팀 구성 | Senior + Domain Expert | Mid-level | Vendor / SRE |
| 투자 비율(예) | 50% | 30% | 20% |

### 2. Bounded Context(제한된 컨텍스트) — 모델의 경계

Bounded Context는 **하나의 유비쿼터스 언어가 일관되게 적용되는 모델의 유효 범위**이다. 여기서 "제한(限界)"은 한계점이 아니라 **명시적 경계선**을 의미한다.

```text
+--------------------------------------------------------------------+
|   "Account"라는 단어가 Bounded Context마다 다른 모델로 변환되는 사례 |
+--------------------------------------------------------------------+

  +-----------------+   +------------------+   +------------------+
  |  Sales Context  |   |  Support Context |   | Billing Context  |
  |  -------------  |   |  ---------------  |   |  ---------------  |
  |  Account =      |   |  Account =       |   |  Account =       |
  |  · Customer     |   |  · Ticket Owner  |   |  · Payer         |
  |  · Credit Limit |   |  · SLA Tier      |   |  · Invoice Addr  |
  |  · Sales Rep    |   |  · Contact Pref  |   |  · Tax Region    |
  |                 |   |                  |   |  · Payment Method|
  |  [Account_ID]   |   |  [Account_UUID]  |   |  [Account_No]    |
  |  [CreditScore]  |   |  [Tier]          |   |  [IBAN]          |
  +-----------------+   +------------------+   +------------------+
         |                       |                       |
         +------------ Context Map 으로 관계 명세 ---------+
```

핵심 규칙: **Bounded Context 내부에서는 단일 모델 + 단일 언어 + 단일 팀**이 보장되어야 한다. 만약 한 컨텍스트에서 "Account"의 속성이 두 가지 의미로 동시 사용된다면, 그 자체가 **암묵적 Bounded Context 분할 신호**다.

### 3. Context Map과 9가지 통합 패턴

Context Map은 Bounded Context 간의 관계와 통합 방식을 시각화·문서화한 산출물이다. Vernon(Vaughn Vernon, *Implementing DDD*, 2013)은 이를 **9가지 패턴**으로 체계화했다.

```text
+-------------------------------------------------------------------------+
|             Context Map 통합 패턴 분류 (관계성/방향성 기준)               |
+-------------------------------------------------------------------------+
|                                                                         |
|  [대칭적 협력 패턴]              [상하 관계(의존 방향) 패턴]             |
|   ① Partnership                  ④ Customer-Supplier (Upstream/Down)   |
|   ② Shared Kernel                ⑤ Conformist                            |
|                                   ⑥ Anti-Corruption Layer (ACL)          |
|  [서비스 제공 패턴]              [표준화 패턴]                          |
|   ⑦ Open-Host Service (OHS)      ⑧ Published Language                  |
|                                   (OHS + PL은 종종 결합)                 |
|  [독립/회피 패턴]                                                        |
|   ⑨ Separate Ways                                                   |
|                                                                         |
|  ※ 보너스: Distributed Big Ball of Mud (현실적 회피 상태)              |
+-------------------------------------------------------------------------+
```

**9가지 패턴의 동작 메커니즘**

| # | 패턴 | 관계 방향 | 핵심 메커니즘 | 기술 사상 |
|:-:|:---|:---:|:---|:---|
| ① | **Partnership** | 대칭(피어) | 두 컨텍스트가 **공동 계획·동시 릴리스**로 진화. 양쪽 모두 성공이 다른 쪽에 의존. | XP 통합 릴리스, Shared Sprint Backlog |
| ② | **Shared Kernel** | 대칭(피어) | 두 컨텍스트가 **공유하는 코드/스키마 서브셋**을 명시적 분리. 변경 시 양 팀 동의를 강제. | 공용 라이브러리, Shared Schema subset, Monorepo |
| ③ | **Customer-Supplier** | 비대칭(Up->Down) | Upstream이 Downstream 요구를 **SLA/로드맵에 반영**할 의무. | API 버전 관리, 정기 동기화 회의 |
| ④ | **Conformist** | 비대칭(Up->Down) | Upstream이 Downstream 요구를 수용할 **의무/능력이 없을 때**, Downstream이 Upstream 모델을 **있는 그대로 수용** | 레거시 시스템 통합, 외부 SaaS API 종속 |
| ⑤ | **Anti-Corruption Layer(ACL)** | 비대칭(Up->Down) | Downstream 내부 도메인을 보호하기 위해 **번역/변환 계층**을 둠. Upstream 모델을 격리. | Anti-Corruption Translator(Adapter + Mapper), Facade, BFF |
| ⑥ | **Open-Host Service(OHS)** | 비대칭(Up->Down) | Upstream이 **공식적·안정적 공개 API**를 제공. 내부 모델 캡슐화. | OpenAPI/Swagger, Versioned REST, gRPC, GraphQL Federation |
| ⑦ | **Published Language** | 대칭(공용) | 두 컨텍스트가 **공용 교환 문서/이벤트 스키마**를 사용. | Protobuf, Avro, JSON Schema, AsyncAPI, CloudEvents |
| ⑧ | **Separate Ways** | 무관계 | 두 컨텍스트가 **기능 중복을 감수**하고 독립 진화. 통합 ROI가 낮을 때. | 자체 빌드, 외부 SaaS 별도 도입 |
| ⑨ | **Big Ball of Mud** | 무관계(역사) | 의도적 설계 없이 섞인 상태. 리팩토링 대상. | 점진적 Bounded Context 추출(Strangler Fig Pattern) |

### 4. Context Map 표현의 핵심 그래픽 표기

Vernon의 표기법은 UML 패키지 다이어그램을 차용하되, **두 컨텍스트 사이의 화살표와 라벨**로 관계를 명세한다.

```text
   [ Sales ]            [ Inventory ]           [ Shipping ]
   +--------+           +------------+          +----------+
   |  B.C.  |   UHS+PL  |   B.C.     |  ACL(D)  |   B.C.   |
   |        | <------------------------|<- - - - -|          |
   |        |  Customer |            | Customer |          |
   |        |  Supplier |            | Supplier |          |
   +--------+   -Supplier+            +----------+          |
       |                                       |              |
       | Shared                                | Partnership  |
       | Kernel                                |              |
       v                                       v              v
   [ Pricing ]                           [ Customer ]
   +--------+                            +---------+
   |  B.C.  |                            |   B.C.  |
   +--------+                            +---------+

   ---> : Customer-Supplier (Upstream -> Downstream)
   ---> : Open-Host Service + Published Language
   - --> : Conformist 또는 Anti-Corruption Layer (라벨 명시)
   ◆-◆  : Shared Kernel (두 컨텍스트를 점선으로 묶음)
```

**핵심 알고리즘/판단 규칙**

- **Upstream 결정 알고리즘**: 누가 모델을 정의하는가? 누가 변경 주도권을 가지는가?
- **변환 비용 공식(개념적)**: `Total Cost = C_sync(팀 간) + C_translate(데이터) + C_evolution(계약)`. ACL 도입 시 C_translate 증가, C_evolution 감소.
- **Bounded Context 식별 휴리스틱**:
  1. **유비쿼터스 언어 충돌 검사**: 같은 단어가 다른 의미 -> 분리
  2. **변경 리듬 검사**: A는 분기 1회, B는 주 10회 배포 -> 분리
  3. **팀 경계 검사**: Conway's Law 관점에서 별도 팀이 관리 -> 분리
  4. **데이터 수명주기 검사**: 한 컨텍스트에서 즉시 처리 vs 다른 컨텍스트에서 배치 -> 분리

- **📢 섹션 요약 비유**: Context Map은 **국제 조약 체계**와 같다. 국경(Bounded Context)이 명확하고, 조약(통합 패턴)이 명시되어야 무역을 할 수 있다. ACL은 "우리말로 번역해주는 통역관", OHS는 "공식 영사관 공용 서비스", Shared Kernel은 "공동 군사 기지", Separate Ways는 "국교
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 473 / 600

<- **이전**: [472. 반응형 시스템 리액티브 매니페스토](/studynote/11_design_supervision/06_exam_summary/472_reactive_system)
**다음**: [474. 바운디드 컨텍스트 컨텍스트 매핑](/studynote/11_design_supervision/06_exam_summary/474_bounded_context/) ->

---
