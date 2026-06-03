+++
title = "533. 비즈니스 능력에 따른 분해"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 비즈니스 능력에 따른 분해(Decompose by Business Capability)는 조직이 "무엇을 할 수 있는가"라는 업무 역량 단위로 마이크로서비스 경계를 설정하는 패턴이다.
> 2. **가치**: 서비스 경계가 실제 비즈니스 조직 구조와 일치하므로 팀-서비스 소유권이 명확해지고, 비즈니스 변화에 따라 자연스럽게 서비스를 진화시킬 수 있다.
> 3. **판단 포인트**: 비즈니스 능력은 기술 구현이 아닌 업무 기능(What) 중심이며, 동일 능력은 하나의 서비스에 응집되어야 하고 팀 경계와 반드시 맞춰야 한다.

---

## Ⅰ. 개요 및 필요성

비즈니스 능력(Business Capability)이란 조직이 특정 목표를 달성하기 위해 보유한 업무적 역량(Capability)을 의미한다. 예를 들어 전자상거래 회사는 "주문 관리", "결제 처리", "재고 관리", "배송 추적", "고객 관리" 등의 비즈니스 능력을 보유한다. 이 개념은 기업 아키텍처(Enterprise Architecture) 분야에서 오랫동안 사용되어 왔으나, 마이크로서비스 아키텍처와 결합하면서 서비스 경계를 결정하는 핵심 도구로 부상했다.

기존의 기술 레이어 중심(프레젠테이션/비즈니스 로직/데이터 접근층) 분해 방식은 여러 팀이 여러 서비스를 공동으로 수정해야 하는 강결합 구조를 만들었다. 반면 비즈니스 능력 기준 분해는 각 팀이 하나의 비즈니스 능력 전체를 소유하므로, 비즈니스 요구사항 변경이 단일 서비스·단일 팀에 의해 독립적으로 처리될 수 있다.

비즈니스 능력 기준 분해의 핵심 전제는 <strong>"조직의 비즈니스 능력은 기술보다 더 안정적이다"</strong>라는 점이다. 기술 스택은 Python에서 Go로 바뀔 수 있지만, 회사가 "주문을 처리한다"라는 능력은 수십 년 동안 유지된다. 따라서 더 안정적인 비즈니스 능력을 경계로 삼으면 서비스 구조 자체의 수명이 길어진다.

이 패턴은 마이크로서비스 아키텍처의 창시자로 꼽히는 마틴 파울러(Martin Fowler)와 제임스 루이스(James Lewis)의 2014년 논문에서 핵심 서비스 분해 원칙으로 제시되었으며, 현재까지 가장 널리 활용되는 마이크로서비스 분해 패턴이다.

- **📢 섹션 요약 비유**: 슈퍼마켓을 채소 코너, 정육 코너, 수산물 코너, 계산대 코너로 나누는 것은 기술적 구분(냉장 설비, 포장 방식)이 아니라 "무슨 제품을 다루는가"라는 비즈니스 능력 기준이다. 각 코너는 해당 제품 전문가가 담당하므로 운영이 효율적이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 비즈니스 능력 식별 방법

비즈니스 능력 도출은 다음 계층적 분석 과정을 거친다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">비즈니스 능력 분석 계층</div></div>
<div class="kb-diagram-note">Level 0: 회사 전체 (전자상거래)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Level 1: 핵심 비즈니스 영역</div>
<div class="kb-diagram-tree-item" style="--depth:2">상품 관리 / 주문 / 결제 / 배송 / 고객</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Level 2: 세부 비즈니스 능력</div>
<div class="kb-diagram-note">주문 영역: 주문 접수 / 주문 조회 / 주문 취소 / 반품 처리</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Level 3: 마이크로서비스 후보</div>
<div class="kb-diagram-note">"주문 서비스" (Order Service) 도출</div>
</div>
</div>



### 전자상거래 비즈니스 능력 맵 예시

| 비즈니스 영역 | 비즈니스 능력 | 마이크로서비스 |
|:---|:---|:---|
| 상품 (Product) | 상품 목록 조회, 상품 등록, 재고 확인 | 상품 서비스 (Product Service) |
| 주문 (Order) | 주문 접수, 주문 조회, 주문 취소 | 주문 서비스 (Order Service) |
| 결제 (Payment) | 결제 처리, 환불, 결제 이력 조회 | 결제 서비스 (Payment Service) |
| 배송 (Shipping) | 배송 등록, 추적, 배송 완료 처리 | 배송 서비스 (Shipping Service) |
| 고객 (Customer) | 회원 가입, 프로필 관리, 인증 | 고객 서비스 (Customer Service) |
| 알림 (Notification) | 이메일/SMS/푸시 알림 발송 | 알림 서비스 (Notification Service) |

### 서비스 구조 다이어그램



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">비즈니스 능력 기반 서비스 분해 구조</div></div>
<div class="kb-diagram-note">클라이언트 (Client)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">API 게이트웨이 (API Gateway)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">상품 주문 결제 배송 고객</div>
<div class="kb-diagram-note">서비스 서비스 서비스 서비스 서비스</div>
<div class="kb-diagram-note">각 서비스는 독립 DB + 독립 배포 파이프라인 보유</div>
</div>
</div>



### 비즈니스 능력의 특성

| 특성 | 설명 | 예시 |
|:---|:---|:---|
| 안정성 | 기술보다 훨씬 오래 유지됨 | "주문 처리" 능력은 10년 이상 변하지 않음 |
| 계층성 | 큰 능력 안에 작은 능력이 중첩됨 | 주문 > 주문 취소 > 부분 취소 |
| 독립성 | 다른 능력과 독립적으로 존재 가능 | 결제 서비스 장애 시 상품 조회 가능 |
| 소유권 | 하나의 팀이 전담 소유 | 결제팀이 결제 서비스 전체 책임 |

- **📢 섹션 요약 비유**: 각 매대(코너)가 자기 제품만 책임지고, 담당 직원이 그 코너의 모든 것을 관리한다. 과일 코너 직원이 정육 코너 재고까지 관리하면 혼란이 생기듯, 서비스 경계도 명확해야 한다.

---

## Ⅲ. 비교 및 연결

### 기술 레이어 vs 비즈니스 능력 기준 비교

| 비교 항목 | 기술 레이어 기준 분해 | 비즈니스 능력 기준 분해 |
|:---|:---|:---|
| 분해 기준 | 기술적 역할 (Controller, Service, DAO) | 비즈니스 기능 (주문, 결제, 배송) |
| 변경 영향 | 기능 변경 시 여러 서비스 수정 필요 | 기능 변경 시 단일 서비스만 수정 |
| 팀 소유권 | 모든 팀이 모든 레이어 수정 | 특정 팀이 특정 서비스 전담 |
| 서비스 수명 | 기술 변화 시 구조 변경 필요 | 비즈니스 유지되면 서비스도 유지 |
| 도메인 전문성 | 분산됨 | 팀별 집중 |

### 비즈니스 능력 vs 하위 도메인 (DDD) 비교

| 비교 항목 | 비즈니스 능력 분해 | 하위 도메인 분해 (DDD) |
|:---|:---|:---|
| 접근법 | 탑다운 (조직/프로세스 분석) | 바텀업 (도메인 전문가 협업) |
| 초점 | "무엇을 하는가" | "어떤 의미를 갖는가" |
| 분석 도구 | 비즈니스 능력 맵, 조직도 | 이벤트 스토밍, 유비쿼터스 언어 |
| 적용 시점 | 초기 서비스 식별 | 복잡한 도메인 모델링 단계 |
| 결과물 | 서비스 후보 목록 | Bounded Context 정의 |

### 콘웨이 법칙(Conway's Law)과의 관계

비즈니스 능력 기준 분해는 콘웨이 법칙과 깊이 연결된다.
- **콘웨이 법칙**: "소프트웨어 구조는 그것을 개발한 조직의 커뮤니케이션 구조를 따른다."
- **역콘웨이 전략**: 원하는 서비스 경계에 맞게 팀을 재편성하여 아키텍처를 목표 방향으로 이끈다.
- 비즈니스 능력 단위로 팀을 구성하면 서비스와 팀 경계가 자연스럽게 일치한다.

- **📢 섹션 요약 비유**: 부서(팀)가 업무별로 나뉘어 있으면 같은 부서 사람끼리 협업하기 쉽다. 결제 업무는 결제팀이, 배송은 배송팀이 담당하면 다른 팀에 물어볼 필요가 없다. 서비스도 마찬가지다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 비즈니스 능력 도출 워크숍 진행

실무에서는 다음 방식으로 비즈니스 능력을 도출한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">비즈니스 능력 도출 프로세스</div></div>
<div class="kb-diagram-note">1단계: 이해관계자 인터뷰</div>
<div class="kb-diagram-note">(경영진, 도메인 전문가, 현업 담당자)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">2단계: 업무 흐름 분석</div>
<div class="kb-diagram-note">(As-Is 프로세스 맵 작성)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">3단계: 능력 목록 작성</div>
<div class="kb-diagram-note">(동사+명사 형식: "주문을 처리한다")</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">4단계: 능력 계층화</div>
<div class="kb-diagram-note">(큰 능력 → 세부 능력으로 분류)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">5단계: 서비스 후보 도출</div>
<div class="kb-diagram-note">(Level 2~3 능력 = 서비스 후보)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">6단계: 검증</div>
<div class="kb-diagram-note">(독립 배포 가능? 팀 소유권 명확?)</div>
</div>
</div>



### 설계 판단 체크리스트

1. **비즈니스 언어와 서비스 이름이 일치하는가?** 기술 용어가 아닌 비즈니스 용어로 서비스 이름을 지을 수 있어야 한다.
2. **하나의 팀이 서비스를 완전히 소유할 수 있는가?** 두 팀이 공동 소유하는 서비스는 경계가 잘못된 것이다.
3. **비즈니스 기능 변경 시 단일 서비스만 수정하면 되는가?** 여러 서비스가 동시에 변경되면 경계 재검토가 필요하다.
4. **서비스 간 통신이 과도하지 않은가?** 빈번한 동기 호출은 서비스 경계 재설정의 신호다.
5. **각 서비스가 자체 데이터를 소유하는가?** 공유 데이터베이스는 즉시 개선이 필요하다.

### 안티패턴

- **기술적 서비스 분리 (Technology-Driven Decomposition)**: UserController 서비스, UserRepository 서비스처럼 기술 레이어로 나누면 하나의 비즈니스 기능 추가가 모든 서비스의 동시 변경을 요구한다. 이는 배포 단위가 기술 레이어로 묶여 독립 배포가 불가능해지는 최악의 패턴이다.
- **능력 없는 서비스 추가 (Utility Service Sprawl)**: "공통 유틸리티 서비스"처럼 명확한 비즈니스 능력이 없는 서비스를 만들면, 여러 서비스가 이 서비스에 의존하여 단일 실패 지점(Single Point of Failure)이 된다.
- **너무 큰 서비스 (Fat Service)**: 하나의 서비스에 "주문, 결제, 배송"을 모두 넣으면 모놀리식과 다를 바 없다. 비즈니스 능력별로 책임이 명확히 분리되어야 한다.

- **📢 섹션 요약 비유**: 회사에서 한 팀이 영업, 재무, 인사를 모두 담당하면 업무 혼란이 생기고, 반대로 영업팀을 영업기획팀, 영업실행팀, 영업보고팀으로 너무 세세하게 나누면 사소한 일도 여러 팀을 거쳐야 한다. 적절한 업무 경계가 핵심이다.

---

## Ⅴ. 기대효과 및 결론

비즈니스 능력 기준 분해를 올바르게 적용하면, 기술 변화와 무관하게 안정적인 서비스 경계를 유지할 수 있다. 비즈니스 요구사항 변경이 특정 팀의 특정 서비스 내에서만 처리되므로, 다른 팀과의 조율 없이 독립적으로 빠르게 배포할 수 있다.

Amazon이나 Netflix가 하루에 수천 번의 배포를 수행할 수 있는 핵심 이유 중 하나가 바로 이 비즈니스 능력 기준 분해다. 각 서비스 팀은 자신의 능력 범위 내에서 자율적으로 결정하고 배포한다. Netflix의 경우 수백 개의 마이크로서비스가 독립적으로 운영되며, 각 서비스는 명확한 비즈니스 능력을 담당한다.

결론적으로, 비즈니스 능력에 따른 분해는 마이크로서비스 아키텍처의 출발점이다. 기술이 아닌 비즈니스 가치를 중심으로 경계를 설정함으로써, 서비스 구조가 비즈니스 변화에 자연스럽게 대응하는 살아있는 시스템을 만들 수 있다.

- **📢 섹션 요약 비유**: 가게에서 맡은 코너가 분명하면 각자 책임지고 일하기 쉽고, 코너가 바뀌어도 담당자만 바꾸면 된다. 기술(진열대 종류)이 바뀌어도 판매 품목(비즈니스 능력)은 그대로 유지된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 마이크로서비스 분해 패턴 (532) | 비즈니스 능력 분해는 마이크로서비스 분해의 핵심 기준 중 하나 |
| 하위 도메인 분해 / DDD (534) | 비즈니스 능력 → Bounded Context 정제 단계로 발전 |
| 콘웨이 법칙 (Conway's Law) | 비즈니스 능력 단위 팀 구성이 서비스 경계와 자연스럽게 일치 |
| 분산 모놀리스 안티패턴 (537) | 기술 레이어 기준 분해 시 발생하는 안티패턴 |
| 이벤트 스토밍 (Event Storming) | 비즈니스 능력 식별에 활용되는 협업 워크숍 기법 |
| API 게이트웨이 | 비즈니스 능력별 서비스를 단일 진입점으로 클라이언트에 노출 |
| 팀 토폴로지 (Team Topologies) | 비즈니스 능력 기반 팀 구성 방법론 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">엔터프라이즈 아키텍처 (EA) - 비즈니스 능력 맵 개념 탄생</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">SOA (Service-Oriented Architecture) 시대</div>
<div class="kb-diagram-note">(비즈니스 서비스 개념 도입)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">마이크로서비스 아키텍처 등장</div>
<div class="kb-diagram-note">(Fowler &amp; Lewis, 2014)</div>
<div class="kb-diagram-note">"비즈니스 능력 중심 분해" 원칙 발표</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">비즈니스 능력 기준 분해 실무 확산</div>
<div class="kb-diagram-note">(Netflix, Amazon, Uber 사례)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">팀 토폴로지 (Team Topologies, 2019)</div>
<div class="kb-diagram-note">(스트림 정렬 팀 = 비즈니스 능력 팀)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">AI/ML 기능의 비즈니스 능력 통합</div>
<div class="kb-diagram-note">(ML 능력도 독립 서비스로 분해)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 학교에서 수학 선생님은 수학만, 과학 선생님은 과학만 가르치듯이, 비즈니스 능력 분해는 각 팀이 자신의 업무 영역(능력)만 담당하게 하는 방법이에요.
2. 수학 교과서를 바꿀 때 과학 선생님한테 물어볼 필요가 없는 것처럼, 서비스 경계가 명확하면 한 팀이 다른 팀 도움 없이 자기 일을 처리할 수 있어요.
3. "무엇을 할 수 있는가"라는 기준으로 서비스를 나누면, 회사의 업무 구조와 소프트웨어 구조가 딱 맞아서 소통이 훨씬 편해진답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 657 / 973

← **이전**: [532. 마이크로서비스 (Microservices) 분해 패턴](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)
**다음**: [533. 비즈니스 능력에 따른 분해 (Decompose by Business Capability)](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/533_decompose_by_business_capability/) →

---
