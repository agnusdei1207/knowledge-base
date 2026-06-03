+++
title = "534. 하위 도메인에 따른 분해 (DDD 기반)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 하위 도메인(Subdomain) 기반 분해는 도메인 주도 설계(DDD, Domain-Driven Design)의 핵심 개념인 Bounded Context를 마이크로서비스 경계에 직접 매핑하는 정교한 분해 전략이다.
> 2. **가치**: 도메인 전문가와 개발자가 공유하는 유비쿼터스 언어(Ubiquitous Language)를 통해 코드와 비즈니스 모델이 일치하고, 핵심·지원·범용 도메인을 명확히 구분하여 자원을 효율적으로 배분할 수 있다.
> 3. **판단 포인트**: 핵심 도메인(Core Domain)은 자체 구현으로 경쟁 우위를 창출하고, 지원·범용 도메인은 외부 솔루션 도입을 우선 검토하여 투자를 최적화해야 한다.

---

## Ⅰ. 개요 및 필요성

도메인 주도 설계(DDD)는 2003년 에릭 에반스(Eric Evans)의 저서 "Domain-Driven Design: Tackling Complexity in the Heart of Software"에서 체계화된 소프트웨어 설계 철학이다. DDD는 복잡한 비즈니스 도메인을 소프트웨어로 표현할 때 도메인 모델을 중심에 두고, 도메인 전문가와 개발자가 동일한 언어로 소통하는 것을 핵심 원칙으로 삼는다.

DDD 기반 분해가 등장하기 전, 마이크로서비스 경계를 결정하는 작업은 주로 비공식적인 경험에 의존했다. 에반스의 DDD 개념, 특히 <strong>경계 컨텍스트(Bounded Context)</strong>와 <strong>하위 도메인(Subdomain)</strong>이 마이크로서비스와 결합하면서 체계적인 서비스 분해 방법론이 확립되었다. 이것이 바로 "Decompose by Subdomain" 패턴이다.

하위 도메인 기반 분해가 필요한 이유는 비즈니스 능력 기준 분해만으로는 부족한 경우가 있기 때문이다. 예를 들어 "주문"이라는 비즈니스 능력 안에도 "온라인 주문 처리"와 "오프라인 주문 처리"는 서로 다른 도메인 모델을 갖는다. 이처럼 동일한 비즈니스 능력 내에서도 도메인 의미(Semantic)가 다른 영역을 정확히 분리하기 위해 DDD 기반 접근이 필요하다.

- **📢 섹션 요약 비유**: 큰 도서관을 단순히 "자연과학", "인문학", "예술"로 나누는 것(비즈니스 능력 분해)과, 더 나아가 같은 자연과학 안에서도 "물리학은 실험 물리와 이론 물리로 다른 방식으로 분류"하는 것(하위 도메인 분해)의 차이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### DDD 핵심 개념 체계



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">DDD 개념 계층 구조</div></div>
<div class="kb-diagram-note">도메인 (Domain)</div>
<div class="kb-diagram-tree-item" style="--depth:2">소프트웨어가 해결하려는 비즈니스 문제 영역</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">하위 도메인 (Subdomain)</div>
<div class="kb-diagram-tree-item" style="--depth:2">Core Domain: 핵심 경쟁 우위</div>
<div class="kb-diagram-tree-item" style="--depth:2">Supporting Domain: 핵심을 지원</div>
<div class="kb-diagram-tree-item" style="--depth:2">Generic Domain: 공통 범용 기능</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">경계 컨텍스트 (Bounded Context)</div>
<div class="kb-diagram-tree-item" style="--depth:2">유비쿼터스 언어가 일관되게 적용되는 경계</div>
<div class="kb-diagram-tree-item" style="--depth:2">하나의 BC = 하나의 마이크로서비스 (이상적)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">유비쿼터스 언어 (Ubiquitous Language)</div>
<div class="kb-diagram-tree-item" style="--depth:2">BC 내에서 팀이 공통으로 사용하는 용어 사전</div>
</div>
</div>



### 하위 도메인 3가지 유형

| 유형 | 정의 | 특성 | 구현 전략 | 예시 (전자상거래) |
|:---|:---|:---|:---|:---|
| 핵심 도메인 (Core Domain) | 비즈니스 경쟁 우위의 원천 | 가장 복잡, 가장 중요 | 내부 최고 개발자 투입, 자체 구현 | 개인화 추천 알고리즘, 가격 최적화 |
| 지원 도메인 (Supporting Domain) | 핵심 도메인을 보조 | 중간 복잡도, 특수성 있음 | 내부 구현 또는 맞춤 외주 | 주문 처리, 재고 관리 |
| 범용 도메인 (Generic Domain) | 일반적 문제 해결 | 낮은 특수성, 표준화 가능 | SaaS 솔루션 또는 오픈소스 도입 | 이메일 발송, 결제 게이트웨이, 인증 |

### Bounded Context 설계 다이어그램



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">전자상거래 Bounded Context 예시</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">주문 컨텍스트</div><div class="kb-diagram-cell">카탈로그 컨텍스트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Order Context)</div><div class="kb-diagram-cell">(Catalog Context)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">주문(Order)</div><div class="kb-diagram-cell">상품(Product)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">주문항목(Item)</div><div class="kb-diagram-cell">카테고리(Category)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">주문상태(Status)</div><div class="kb-diagram-cell">가격(Price)</div></div>
<div class="kb-diagram-note">컨텍스트 맵 (Context Map)</div>
<div class="kb-diagram-note">(Anti-Corruption Layer)</div>
<div class="kb-diagram-note">+--------v--------------------v--+</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">공유 커널 (Shared Kernel)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(공통 가격 계산 규칙 등)</div></div>
</div>
</div>



### 컨텍스트 매핑 패턴

| 패턴 | 설명 | 사용 상황 |
|:---|:---|:---|
| 공유 커널 (Shared Kernel) | 두 팀이 일부 모델 공유 | 긴밀히 협력하는 팀 |
| 고객-공급자 (Customer-Supplier) | 업스트림/다운스트림 관계 | 명확한 의존 방향 존재 |
| 순응자 (Conformist) | 하위 팀이 상위 팀 모델 수용 | 레거시 시스템 연동 |
| 부패 방지 레이어 (ACL) | 번역 레이어로 모델 보호 | 외부 시스템 통합 |
| 오픈 호스트 서비스 (OHS) | 공개 프로토콜로 서비스 노출 | API 공개 서비스 |
| 공개된 언어 (Published Language) | 문서화된 공유 언어 사용 | 표준 데이터 형식 |

- **📢 섹션 요약 비유**: 영화에서 주인공(핵심 도메인), 조연(지원 도메인), 엑스트라(범용 도메인)를 구분하면 주인공 배우에게 집중적으로 투자하고, 엑스트라는 섭외 업체(외부 솔루션)를 활용하여 제작 비용을 최적화하는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 비즈니스 능력 분해 vs 하위 도메인 분해 심층 비교

| 비교 항목 | 비즈니스 능력 기준 분해 | 하위 도메인 (DDD) 분해 |
|:---|:---|:---|
| 출발점 | 조직 차트, 업무 프로세스 | 도메인 전문가 인터뷰, 이벤트 스토밍 |
| 분해 기준 | 기능적 역할 (What) | 도메인 의미, 모델 경계 (Why/How) |
| 정교함 | 중간 수준 | 매우 높음 |
| 필요 시간 | 상대적으로 짧음 | 많은 분석 시간 필요 |
| 적합 상황 | 초기 MSA 설계 | 복잡한 도메인, 성숙한 팀 |
| 결과물 | 서비스 후보 목록 | Bounded Context + 컨텍스트 맵 |
| 활용 도구 | 비즈니스 능력 맵 | 이벤트 스토밍, 유비쿼터스 언어 사전 |

### 하위 도메인과 Bounded Context의 관계

이상적으로는 하나의 하위 도메인이 하나의 Bounded Context에 매핑된다. 그러나 현실에서는 다양한 패턴이 나타난다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">이상적 매핑</div></div>
<div class="kb-diagram-note">핵심 도메인 = Bounded Context A = 마이크로서비스 A</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현실적 매핑 패턴</div></div>
<div class="kb-diagram-note">큰 하위 도메인 = 여러 BC → 여러 서비스</div>
<div class="kb-diagram-note">여러 작은 하위 도메인 = 하나의 BC → 하나의 서비스</div>
<div class="kb-diagram-note">레거시 도메인 = BC 내 여러 모델이 공존</div>
</div>
</div>



### 이벤트 스토밍(Event Storming)과의 연계

이벤트 스토밍은 도메인 전문가와 개발자가 함께 도메인을 탐색하는 협업 워크숍 기법으로, 하위 도메인 경계를 실질적으로 도출하는 가장 효과적인 방법이다.

| 단계 | 활동 | 산출물 |
|:---|:---|:---|
| 도메인 이벤트 도출 | 발생한 사실(과거형)을 포스트잇으로 | 오렌지 포스트잇 이벤트 목록 |
| 커맨드 식별 | 이벤트를 유발하는 명령 도출 | 파란 포스트잇 커맨드 목록 |
| 집계 식별 | 커맨드를 처리하는 도메인 객체 | 노란 포스트잇 집계 목록 |
| BC 경계 도출 | 유비쿼터스 언어가 일관된 영역 구분 | Bounded Context 경계선 |

- **📢 섹션 요약 비유**: 같은 "공"이라도 축구공은 발로 차고, 농구공은 손으로 드리블하며, 야구공은 손으로 던진다. 겉으로 보면 모두 "공"이지만, 각 스포츠의 규칙(도메인)에 따라 완전히 다른 존재이다. Bounded Context는 이 차이를 명확히 구분하는 경계다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### DDD 기반 서비스 분해 프로세스



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">실무 적용 단계</div></div>
<div class="kb-diagram-note">Step 1: 핵심 도메인 식별</div>
<div class="kb-diagram-note">Q: "우리 회사만의 경쟁 우위는 무엇인가?"</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Step 2: 이벤트 스토밍 워크숍</div>
<div class="kb-diagram-note">(도메인 전문가 + 개발자 협업, 2-3일)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Step 3: 유비쿼터스 언어 정립</div>
<div class="kb-diagram-note">(용어 사전 작성, 모호한 용어 제거)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Step 4: Bounded Context 도출</div>
<div class="kb-diagram-note">(자연스럽게 나타나는 언어 경계 = BC 경계)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Step 5: 컨텍스트 맵 작성</div>
<div class="kb-diagram-note">(BC 간 관계 및 통합 방식 정의)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Step 6: 마이크로서비스 매핑</div>
<div class="kb-diagram-note">(BC = 서비스 후보, 크기 검토)</div>
</div>
</div>



### 설계 판단 체크리스트

1. **핵심 도메인이 명확히 식별되었는가?** 경쟁 우위의 원천인 핵심 도메인에 최고 개발자를 배치하고 있는가?
2. **각 Bounded Context 내에서 유비쿼터스 언어가 일관성 있게 사용되는가?** 같은 단어가 다른 의미로 사용되는 충돌이 없는가?
3. **BC 간 통합이 컨텍스트 맵으로 명확히 정의되어 있는가?** 암묵적 의존성이 없는가?
4. **범용 도메인에 외부 솔루션을 적극 활용하는가?** 이메일 발송, 결제 게이트웨이를 자체 개발하고 있지는 않은가?
5. **모델이 코드에 정확히 반영되어 있는가?** 도메인 모델과 코드 구조가 일치하는가?

### 안티패턴

- **빈약한 도메인 모델 (Anemic Domain Model)**: DDD를 적용한다고 하면서 도메인 객체가 데이터만 가지고 행동(메서드)이 없는 경우다. 모든 비즈니스 로직이 서비스 레이어에 몰리고, 도메인 객체는 단순 데이터 전달 객체(DTO)가 된다. 이는 DDD의 핵심 이점인 도메인 로직의 집중화를 포기하는 것이다.
- **BC 무시 공유 모델**: "편의상" 여러 BC가 동일한 Entity 클래스를 공유하면, 한 BC의 요구사항 변경이 다른 BC의 모델까지 영향을 준다. 각 BC는 독립적인 도메인 모델을 가져야 하며, 필요시 부패 방지 레이어(ACL)로 번역해야 한다.
- **과도한 DDD 적용**: CRUD 수준의 단순한 서비스에 집계(Aggregate), 도메인 서비스, 값 객체(Value Object) 등 DDD 개념을 모두 억지로 적용하면 불필요한 복잡도가 증가한다. DDD는 복잡한 도메인에 적합한 도구이다.

- **📢 섹션 요약 비유**: 법원에서 "피고"라는 단어는 형사 소송과 민사 소송에서 다른 의미를 갖는다. 이처럼 같은 단어도 컨텍스트(BC)에 따라 다른 의미가 되며, Bounded Context는 이 언어 혼란을 방지하는 경계선이다.

---

## Ⅴ. 기대효과 및 결론

DDD 기반 하위 도메인 분해를 올바르게 적용하면, 코드와 비즈니스 모델 사이의 간격(Translation Gap)이 최소화된다. 도메인 전문가가 "주문"이라고 말하면 코드에도 Order 클래스가 존재하고, "주문 취소"를 요청하면 Order.cancel() 메서드가 있다. 이 명확한 일치는 개발자와 비즈니스 간 의사소통 오류를 크게 줄인다.

핵심·지원·범용 도메인을 구분함으로써 자원 배분이 최적화된다. 핵심 도메인에는 최고의 개발자와 충분한 시간을 투입하고, 범용 도메인은 외부 솔루션(Stripe, SendGrid, Auth0 등)을 활용하여 개발 비용을 절감한다. 이는 비즈니스 경쟁력의 원천에 집중하는 전략적 선택이다.

결론적으로, DDD 기반 하위 도메인 분해는 복잡한 비즈니스 도메인을 다루는 대규모 시스템에서 가장 강력한 서비스 분해 방법론이다. 초기 투자 비용(이벤트 스토밍, 유비쿼터스 언어 정립)이 크지만, 장기적으로 모델과 코드의 일치로 유지보수 비용이 대폭 감소한다.

- **📢 섹션 요약 비유**: 각각의 방에 이름표를 붙이고(유비쿼터스 언어), 방의 용도를 명확히 정하면(BC 정의), 어떤 물건이 어느 방에 있는지 모두가 알 수 있다. 주방 규칙과 침실 규칙이 다른 것처럼, 각 컨텍스트의 규칙이 독립적으로 적용된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 마이크로서비스 분해 패턴 (532) | DDD 분해는 마이크로서비스 경계 결정의 정교한 방법론 |
| 비즈니스 능력 분해 (533) | DDD 이전 단계로 비즈니스 능력 도출, DDD로 정제 |
| 이벤트 기반 아키텍처 (538) | 도메인 이벤트가 BC 간 통신의 핵심 수단 |
| 사가 패턴 (550) | BC 간 분산 트랜잭션을 도메인 이벤트로 처리 |
| CQRS (554) | DDD의 커맨드/쿼리 분리 원칙을 구현하는 패턴 |
| 이벤트 소싱 (555) | 도메인 이벤트를 상태의 원천으로 활용 |
| 분산 모놀리스 안티패턴 (537) | BC를 무시한 공유 모델 사용 시 발생하는 결과 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Eric Evans의 DDD 저서 발표 (2003)</div>
<div class="kb-diagram-note">(Bounded Context, Ubiquitous Language 개념 정립)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Vaughn Vernon의 "Implementing DDD" 출판 (2013)</div>
<div class="kb-diagram-note">(실용적 DDD 구현 방법 체계화)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">마이크로서비스와 DDD 결합 (2014-2015)</div>
<div class="kb-diagram-note">(Bounded Context = 마이크로서비스 경계)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">이벤트 스토밍 기법 확산 (Alberto Brandolini, 2015~)</div>
<div class="kb-diagram-note">(도메인 탐색 실용 워크숍 도구)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">DDD + CQRS + 이벤트 소싱 조합</div>
<div class="kb-diagram-note">(복잡한 도메인의 표준 아키텍처 패턴)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">DDD 기반 AI 도메인 모델링</div>
<div class="kb-diagram-note">(ML 파이프라인을 핵심/지원 도메인으로 분류)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 큰 학교를 "수학 교실", "미술 교실", "체육관"으로 나누고(하위 도메인), 각 교실에서는 그 교실만의 규칙이 적용되는 것처럼, DDD는 프로그램을 의미 있는 영역으로 나누는 방법이에요.
2. 수학 교실에서 "문제"는 수학 문제이고, 체육관에서 "문제"는 동작 문제인 것처럼(유비쿼터스 언어), 같은 단어도 교실(컨텍스트)마다 다른 의미를 갖도록 명확히 구분해요.
3. 핵심 과목(핵심 도메인)에는 제일 좋은 선생님을 배치하고, 공통 행정 업무(범용 도메인)는 외부 기관에 맡기는 것처럼, 자원을 전략적으로 배분할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 660 / 973

← **이전**: [534. 하위 도메인에 따른 분해 (Decompose by Subdomain - DDD 기반)](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/534_decompose_by_subdomain_ddd/)
**다음**: [535. 서비스 간 동기 통신 - REST API, gRPC](/knowledge-base/studynote/04_software_engineering/11_testing_validation/535_service_to_service_synchronous_communication/) →

---
