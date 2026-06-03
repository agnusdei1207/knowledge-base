+++
title = "532. 마이크로서비스 (Microservices) 분해 패턴"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 마이크로서비스(Microservices) 분해 패턴은 거대한 모놀리식(Monolithic) 시스템을 독립적으로 배포·확장 가능한 작은 서비스 단위로 나누는 아키텍처 설계 원칙이다.
> 2. **가치**: 올바른 분해 기준을 적용하면 팀 자율성이 높아지고, 서비스별 독립 배포·독립 확장이 가능해져 비즈니스 민첩성이 극적으로 향상된다.
> 3. **판단 포인트**: 분해 경계가 잘못 설정되면 분산 모놀리스(Distributed Monolith) 안티패턴에 빠지므로, 도메인 중심·비즈니스 능력 기준 경계 설정이 핵심이다.

---

## Ⅰ. 개요 및 필요성

마이크로서비스(Microservices) 아키텍처는 2010년대 초반 Netflix, Amazon 등 대형 인터넷 기업들이 거대해진 모놀리식 시스템의 한계를 극복하기 위해 본격적으로 채택하면서 주목받기 시작했다. 기존 모놀리식 구조에서는 코드베이스가 커질수록 빌드·배포 시간이 늘어나고, 일부 기능의 변경이 전체 시스템 재배포를 요구하며, 특정 컴포넌트만 독립적으로 확장하는 것이 불가능했다. 이러한 문제는 수백 명의 개발자가 동일한 코드베이스에서 작업할 때 더욱 심각해졌다.

마이크로서비스는 이런 문제를 해결하기 위해 시스템을 작고 집중된(Focused) 서비스 단위로 분해한다. 각 서비스는 자체 프로세스에서 실행되며, 경량 API(주로 HTTP/REST 또는 gRPC)를 통해 통신한다. 핵심은 **어떤 기준으로** 서비스를 분해하느냐이며, 이것이 아키텍처 전체의 성공과 실패를 좌우한다. 잘못된 분해는 오히려 분산 모놀리스라는 최악의 상황을 만들어낸다. 즉, 시스템은 물리적으로는 분산되었지만 논리적으로는 여전히 강하게 결합된 상태가 된다.

마이크로서비스 분해의 목표는 단순히 서비스를 잘게 쪼개는 것이 아니라, <strong>느슨한 결합(Loose Coupling)</strong>과 <strong>높은 응집도(High Cohesion)</strong>를 동시에 달성하는 것이다. 각 서비스는 명확한 책임을 가지고, 다른 서비스와의 의존성을 최소화하며, 내부 구현 세부사항을 완전히 캡슐화해야 한다. 이를 통해 팀은 자신의 서비스를 독립적으로 개발·테스트·배포·운영할 수 있게 된다.

- **📢 섹션 요약 비유**: 큰 도시(모놀리식 시스템)를 행정 구역(마이크로서비스)으로 나누되, 각 구역이 자체적으로 운영되면서도 도시 전체와 잘 연결되어야 한다. 구역 경계선을 잘못 그으면 하나의 사안이 여러 구역에 걸쳐 처리되는 혼란이 생긴다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 주요 분해 패턴 개요

마이크로서비스 분해에는 크게 세 가지 주요 접근법이 사용된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">분해 패턴 체계</div></div>
<div class="kb-diagram-note">비즈니스 능력 기준 분해</div>
<div class="kb-diagram-note">(Decompose by Business Capability)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">서비스 경계 도출</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">하위 도메인 기준 분해 (DDD 기반)</div>
<div class="kb-diagram-note">(Decompose by Subdomain)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Bounded Context 정의</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">데이터 소유권 할당</div>
<div class="kb-diagram-note">(독립 데이터베이스 per Service)</div>
</div>
</div>



### 분해 기준 4가지 핵심 원칙

| 분해 기준 | 설명 | 적용 시점 |
|:---|:---|:---|
| 비즈니스 능력 (Business Capability) | 조직이 수행하는 업무 기능 단위로 분해 | 초기 서비스 식별 단계 |
| 하위 도메인 (Subdomain/DDD) | 도메인 전문가와 함께 경계 컨텍스트 정의 | 복잡한 도메인 모델링 |
| 변경 빈도 (Rate of Change) | 함께 변경되는 코드는 같은 서비스에 배치 | 운영 중 리팩토링 |
| 팀 구조 (Conway's Law) | 팀 경계와 서비스 경계를 일치시킴 | 조직 설계와 연계 |

### 서비스 경계 설계 원칙



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">이상적인 마이크로서비스 구조</div></div>
<div class="kb-diagram-note">+------------------+ API/Event +------------------+</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">주문 서비스</div><div class="kb-diagram-cell">&lt;-----------&gt;</div><div class="kb-diagram-cell">재고 서비스</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Order Service)</div><div class="kb-diagram-cell">(Inventory Svc)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">주문 DB</div><div class="kb-diagram-node">재고 DB</div></div>
<div class="kb-diagram-note">v v</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">결제 서비스</div><div class="kb-diagram-cell">배송 서비스</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Payment Svc)</div><div class="kb-diagram-cell">(Shipping Svc)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">결제 DB</div><div class="kb-diagram-node">배송 DB</div></div>
</div>
</div>



각 서비스는 자신만의 데이터베이스를 소유하고, 다른 서비스의 데이터에 직접 접근하지 않는다. 이것이 <strong>데이터 소유권 원칙(Database per Service Pattern)</strong>이다.

### 서비스 크기 결정 가이드라인

| 지표 | 너무 큰 서비스 | 적절한 서비스 | 너무 작은 서비스 |
|:---|:---|:---|:---|
| 팀 규모 | 20명 이상 | 2-8명 (피자 두 판 법칙) | 1명 미만 |
| 배포 빈도 | 월 1회 미만 | 주 1-수회 | 하루 수십 회 |
| 코드 라인 | 수십만 줄 | 수천~수만 줄 | 수백 줄 |
| 변경 영향 | 전체 시스템 | 해당 도메인 | 거의 없음 |

### 분해 품질 평가 기준

서비스 분해의 품질을 평가하는 세 가지 핵심 지표가 있다.

| 품질 속성 | 정의 | 측정 방법 |
|:---|:---|:---|
| 결합도 (Coupling) | 서비스 간 의존성 정도 | API 호출 횟수, 공유 자원 수 |
| 응집도 (Cohesion) | 서비스 내부 기능의 관련성 | 단일 책임 원칙 준수 여부 |
| 자율성 (Autonomy) | 독립 배포·운영 가능 여부 | 독립 배포 성공률 |

- **📢 섹션 요약 비유**: 방을 나눌 때 각 방은 명확한 용도(침실, 주방, 욕실)를 가져야 하고, 방 간의 문은 필요한 곳에만 있어야 한다. 모든 방이 서로 통하는 구조는 방을 나눈 의미가 없다.

---

## Ⅲ. 비교 및 연결

### 모놀리식 vs 마이크로서비스 분해 비교

| 비교 항목 | 모놀리식 (Monolithic) | 마이크로서비스 (Microservices) |
|:---|:---|:---|
| 배포 단위 | 전체 시스템 | 개별 서비스 |
| 확장 방식 | 전체 수평 확장 | 서비스별 독립 확장 |
| 기술 스택 | 단일 스택 | 서비스별 최적 선택 |
| 장애 격리 | 어려움 | 가능 (Circuit Breaker) |
| 초기 복잡도 | 낮음 | 높음 |
| 팀 자율성 | 낮음 | 높음 |
| 데이터 일관성 | 강한 일관성 용이 | 최종 일관성 (Eventually Consistent) |

### 좋은 분해 vs 나쁜 분해

| 구분 | 좋은 분해 | 나쁜 분해 |
|:---|:---|:---|
| 기준 | 도메인/비즈니스 능력 중심 | 기술 레이어 중심 (Controller/Service/Repo) |
| 통신 | API 계약을 통한 최소 통신 | 과도한 동기 호출 체인 |
| 데이터 | 서비스별 독립 데이터베이스 | 공유 데이터베이스 |
| 배포 | 독립 배포 가능 | 동시 배포 필요 |
| 소유권 | 팀 경계와 일치 | 여러 팀이 하나의 서비스 관리 |

### 관련 개념과의 연결

마이크로서비스 분해는 여러 핵심 개념과 깊이 연결된다.

- **도메인 주도 설계(DDD, Domain-Driven Design)**: Bounded Context가 서비스 경계를 결정하는 핵심 도구가 된다.
- **콘웨이 법칙(Conway's Law)**: 시스템 설계는 해당 조직의 커뮤니케이션 구조를 따른다. 마이크로서비스는 역콘웨이 전략(Inverse Conway Maneuver)을 통해 원하는 아키텍처에 맞게 팀을 재구성한다.
- **사가 패턴(Saga Pattern)**: 서비스 분해 후 분산 트랜잭션 처리를 위해 필요하다.
- **API 게이트웨이(API Gateway)**: 분해된 서비스들을 클라이언트에게 단일 진입점으로 노출한다.

- **📢 섹션 요약 비유**: 같은 종류의 물건은 같은 창고에 보관하고, 창고 간 이동은 공식 운송 경로를 통해서만 한다. 아무 창고나 직접 들어가는 것은 금지다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 분해 프로세스 단계별 접근

실무에서 마이크로서비스 분해는 다음 단계로 진행한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">분해 프로세스</div></div>
<div class="kb-diagram-note">1단계: 비즈니스 능력 도출</div>
<div class="kb-diagram-note">(조직도, 업무 프로세스 분석)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">2단계: 하위 도메인 식별 (DDD)</div>
<div class="kb-diagram-note">(핵심/지원/범용 도메인 구분)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">3단계: Bounded Context 정의</div>
<div class="kb-diagram-note">(도메인 전문가와 협업)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">4단계: 서비스 경계 검증</div>
<div class="kb-diagram-note">(팀 구조, 데이터 소유권 확인)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">5단계: API 계약 설계</div>
<div class="kb-diagram-note">(OpenAPI, Protobuf 등)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">6단계: 점진적 마이그레이션</div>
<div class="kb-diagram-note">(Strangler Fig Pattern)</div>
</div>
</div>



### 설계 판단 체크리스트

1. **독립 배포 가능성**: 각 서비스를 다른 서비스 변경 없이 독립적으로 배포할 수 있는가?
2. **데이터 소유권 명확성**: 각 서비스가 자신만의 데이터베이스를 소유하고 있는가?
3. **통신 비용 최적화**: 서비스 간 과도한 API 호출 체인이 발생하지 않는가? (N+1 분산 호출 문제)
4. **팀-서비스 경계 일치**: 서비스 경계가 팀 경계와 일치하는가?
5. **비즈니스 의미 일치**: 서비스 이름이 비즈니스 용어와 일치하는가?
6. **변경 전파 최소화**: 하나의 서비스 변경이 다른 서비스의 변경을 유발하지 않는가?
7. **장애 격리**: 하나의 서비스 장애가 전체 시스템에 영향을 미치지 않는가?

### 안티패턴

- **너무 잘게 쪼개기 (Nano-services)**: 서비스를 메서드 수준으로 분해하면 통신 오버헤드가 폭증하고, 트랜잭션 관리가 극도로 복잡해진다. 각 HTTP 호출이 수십 밀리초의 레이턴시를 추가하며, 분산 트랜잭션 처리를 위한 사가 패턴 구현이 필요해 개발 복잡도가 기하급수적으로 증가한다.
- **기술 레이어 기준 분해**: Controller-Service-Repository 계층을 각각 별도 서비스로 만드는 방식은 가장 나쁜 분해이다. 모든 비즈니스 요청이 세 서비스를 순서대로 호출해야 하므로 분산 모놀리스의 전형적 사례가 된다.
- **공유 데이터베이스 안티패턴 (Shared Database)**: 여러 서비스가 같은 데이터베이스를 공유하면 스키마 변경 시 모든 서비스에 영향을 미쳐 독립 배포가 불가능해진다. 이는 분산 모놀리스로 향하는 지름길이다.
- **Big Bang 마이그레이션**: 기존 모놀리스를 한 번에 마이크로서비스로 전환하려는 시도는 매우 위험하다. Strangler Fig Pattern을 적용하여 점진적으로 분해해야 한다.

- **📢 섹션 요약 비유**: 큰 회사를 부서로 나눌 때, 너무 잘게 쪼개면 간단한 일도 여러 부서에 걸쳐 결재를 받아야 하고, 잘못 나누면 결국 모든 부서가 한 팀처럼 움직여야 한다. 일이 자연스럽게 흘러가는 경계가 최선이다.

---

## Ⅴ. 기대효과 및 결론

마이크로서비스 분해를 올바르게 적용하면 다음과 같은 정량적·정성적 효과를 기대할 수 있다.

**정량적 효과**: 팀별 독립 배포로 배포 빈도가 수십 배 증가하고(Netflix의 경우 하루 수천 회 배포), 특정 서비스만 선택적으로 확장하여 인프라 비용을 최적화한다. 장애 격리로 가용성이 높아지며, 전체 시스템 다운타임 대신 개별 서비스 수준의 장애로 영향 범위가 제한된다.

**정성적 효과**: 팀은 자신의 서비스에 집중하므로 인지 부하가 줄어들고, 서비스별로 최적의 기술 스택을 선택할 수 있다. 새 팀원의 온보딩도 전체 시스템이 아닌 담당 서비스만 이해하면 되므로 빨라진다.

그러나 마이크로서비스는 만능이 아니다. 소규모 팀이나 초기 스타트업에서는 모놀리식이 오히려 더 빠른 개발 속도를 제공한다. "모놀리스 먼저(Monolith First)" 전략을 통해 도메인을 충분히 이해한 후 점진적으로 분해하는 것이 현명하다. 분해의 핵심은 기술이 아닌 <strong>경계(Boundary)</strong>이며, 경계가 올바를 때 비로소 마이크로서비스의 가치가 실현된다.

- **📢 섹션 요약 비유**: 도시가 발전하면서 자연스럽게 생긴 동네 경계선이 가장 실용적인 행정 경계가 된다. 처음부터 너무 세세하게 나누면 작은 일도 여러 관청을 거쳐야 하는 행정 낭비가 생긴다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 도메인 주도 설계 (DDD, Domain-Driven Design) | Bounded Context가 서비스 경계 결정의 핵심 도구 |
| 비즈니스 능력 기준 분해 (533) | 분해의 출발점: 조직 업무 능력 기반 서비스 식별 |
| 하위 도메인 분해 (534) | DDD 기반 세밀한 도메인 경계 설정 |
| 분산 모놀리스 안티패턴 (537) | 잘못된 분해의 대표적 결과물, 반면교사 |
| 사가 패턴 (550) | 분해 후 분산 트랜잭션 처리 방법 |
| API 게이트웨이 패턴 | 분해된 서비스의 단일 진입점 제공 |
| 콘웨이 법칙 (Conway's Law) | 팀 구조와 서비스 경계의 상호 영향 관계 |
| 데이터베이스 per 서비스 패턴 | 서비스 자율성을 보장하는 데이터 소유권 원칙 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">모놀리식 아키텍처 한계 인식</div>
<div class="kb-diagram-note">(Netflix, Amazon 사례, 2010년대 초)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">SOA (Service-Oriented Architecture) 시도</div>
<div class="kb-diagram-note">(XML, SOAP 기반 서비스 분리)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">마이크로서비스 패턴 등장</div>
<div class="kb-diagram-note">(REST API, 경량 통신, 독립 배포)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">DDD 기반 분해 기준 정립</div>
<div class="kb-diagram-note">(Bounded Context, 도메인 모델)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">쿠버네티스 기반 서비스 메시(Service Mesh)</div>
<div class="kb-diagram-note">(Istio, Linkerd - 서비스 간 통신 관리)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">서버리스 / 함수형 분해</div>
<div class="kb-diagram-note">(AWS Lambda - 함수 수준 분해)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 큰 레고 성을 만들 때 처음부터 모든 방을 한 덩어리로 만들지 않고, 침실 블록·주방 블록·욕실 블록을 따로따로 만든 후 합치면 나중에 고치기가 훨씬 쉬워요.
2. 각 블록이 다른 블록과 연결되는 부분(경계)을 정확하게 정해야, 한 블록을 바꿔도 다른 블록에 영향이 없어요.
3. 마이크로서비스 분해는 이처럼 큰 프로그램을 작은 조각으로 나누어 각 조각이 독립적으로 일할 수 있게 만드는 설계 방법이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 655 / 973

← **이전**: [531. 클라우드 네이티브 아키텍처 (Cloud Native Architecture) 철학](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/)
**다음**: [532. 마이크로서비스 (Microservices) 분해 패턴](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) →

---
