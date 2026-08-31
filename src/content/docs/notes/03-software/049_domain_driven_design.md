---
sidebar:
  order: 49
  label: "049. 도메인 주도 설계 DDD"
  badge:
    text: "기출 · 50%"
    variant: note
title: "도메인 주도 설계 DDD (Domain-Driven Design)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-software"
weight: 49
extra:
  question_no: "049"
  source_status: "기출"
  source_history: "126회"
  priority: 50
  priority_note: "126회 기출, DDD 전략·전술 설계 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **DDD(Domain-Driven Design)**: 에릭 에반스(Eric Evans)가 제안한, 복잡한 소프트웨어를 비즈니스 도메인 모델 중심으로 설계하는 패러다임.
- **보편적 언어(Ubiquitous Language)**: 기획자, 도메인 전문가, 개발자가 소통과 코드 작성에 동일하게 사용하는 단일 도메인 어휘 체계.

</details>

- 정의/개념: 비즈니스 도메인을 중심으로 **보편적 언어(Ubiquitous Language)와 바운디드 컨텍스트**를 정의하고 모델을 캡슐화하는 설계 방법론
- 배경/필요성: 비즈니스 복잡도가 높은 소프트웨어에서 기획자·도메인 전문가와 개발자 간의 언어적 불일치(소통 단절), 서비스 클래스에 if-else 비즈니스 로직이 난립하는 빈혈 도메인 모델(Anemic Model) 및 무분별한 데이터베이스 중심 설계를 극복하고, 보편적 언어(Ubiquitous Language)와 전략적 설계(Bounded Context, Context Map), 전술적 패턴(Aggregate, Entity, VO, Repository)을 통해 **비즈니스 도메인의 본질을 풍부한 객체지향 모델(Rich Domain Model)로 캡슐화하고 시스템 복잡도를 제어**할 필요

#### 한줄 요약
- 비즈니스 도메인을 보편적 언어로 코드에 반영하고 전략/전술적 설계로 복잡도를 제어한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **전략적 설계(Strategic Design)**: 도메인 전체를 Bounded Context로 분할하고 Context Map으로 서비스 간 관계를 정의하는 고수준 설계.
- **전술적 설계(Tactical Design)**: Entity, VO, Aggregate, Repository, Domain Service 등을 활용해 도메인 모델을 코드로 구현하는 패턴.

</details>

- **보편적 언어(Ubiquitous Language)** 수립으로 기획자와 개발자 간의 개념적 괴리 완전 해소
- **전략적 설계(Bounded Context)** 기반으로 마이크로서비스(MSA) 분할의 명확한 경계 제공
- **전술적 설계(Aggregate Root, Entity, VO)** 를 통한 도메인 불변식(Invariant)의 완벽한 캡슐화

#### 한줄 요약
- 보편적 언어와 경계 설정은 번역 오류를 없애는 대신 도메인 전문가와의 지속적 대화 비용을 요구하므로, 복잡도가 낮은 영역에서는 과투자가 된다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **애그리게이트(Aggregate)**: 데이터 변경의 단위로 묶인 연관 객체들의 군집이며, 외부에서는 오직 애그리게이트 루트(Aggregate Root)를 통해서만 접근 가능.

</details>

```text
[DDD 전략적·전술적 설계 계층 구조]
|-- 전략적 설계 (Strategic Design: 전사 도메인 수준)
|   |-- Bounded Context A (주문 컨텍스트) <--- [Context Map: ACL] ---> Bounded Context B (결제)
|   `-- Ubiquitous Language (도메인 공통 어휘 사전)
`-- 전술적 설계 (Tactical Design: Context 내부 객체 모델)
     |-- Aggregate (주문 애그리게이트)
     |   |-- Aggregate Root (Order Entity: 외부 접근 단일 진입점)
     |   |-- 내부 Entity (OrderItem)
     |   `-- Value Object (Address VO, Money VO - 불변 값 객체)
     |-- Domain Service (복수 애그리게이트 간 비즈니스 로직)
     `-- Repository (애그리게이트 단위 영속화 인터페이스)
```

선의 의미: 전략적 도메인 분할 및 전술적 객체 캡슐화 구조

| 구성요소 | 책임 |
|:---|:---|
| Bounded Context·Context Map | 모델 경계와 **서비스 관계 정의** |
| Aggregate·Root | 불변식과 **원자적 변경 단위 보호** |
| Entity·Value Object | 식별 객체와 **불변 값 표현** |
| Domain Service·Repository | 도메인 로직과 **집합 단위 영속화** |

#### 한줄 요약
- 전략적 설계가 경계를 긋고 전술적 패턴이 그 안을 채우는 순서이므로, 컨텍스트 구분 없이 Aggregate만 도입하면 DDD의 이득이 나오지 않는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **이벤트 스토밍(Event Storming)**: 도메인 전문가와 개발자가 모여 도메인 이벤트(주황색 포스트잇)를 시간순으로 나열하며 도메인을 탐색하는 협업 기법.

</details>

```text
이벤트 스토밍(Event Storming) 워크숍 수행 (도메인 이벤트 시간순 도출)
        │
   보편적 언어(Ubiquitous Language) 어휘 사전 확정
        │
   전략적 설계: Bounded Context 경계 식별 및 Context Map(ACL/Shared Kernel) 작성
        │
   전술적 설계: Aggregate Root, Entity, VO 식별 및 도메인 메서드 설계
        │
   Rich Domain Model 구현 (setter 금지, 풍부한 객체지향 도메인 완성)
```

#### 한줄 요약
- 이벤트 스토밍과 언어 확정이 앞서지 않으면 Bounded Context 경계가 조직도나 기술 구조를 따라 잘못 그어지므로, 앞 단계의 부실이 뒤 단계 전체를 왜곡한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **빈혈 도메인 모델(Anemic) vs 풍부한 도메인 모델(Rich)**: getter/setter만 있고 비즈니스 로직이 Service에 몰린 절차적 안티패턴과 객체 스스로 비즈니스 규칙을 수행하는 DDD 모델.

</details>

| 비교 항목 | 빈혈 도메인 모델 (Anemic Model) | 풍부한 도메인 모델 (Rich Domain Model - DDD) |
|:---|:---|:---|
| 비즈니스 로직 위치 | **Service 클래스에 모든 if-else 집중** | **Entity / VO 내부에 캡슐화** |
| 객체의 역할 | 단순 데이터 홀더 (Getter / Setter) | **스스로 상태를 검증하고 행위를 수행하는 객체** |
| 불변성 보장 | setter 남용으로 어디서든 데이터 훼손 | **setter 금지, 의미 있는 도메인 메서드로 변경** |
| 객체지향 패러다임 | 객체지향을 흉내낸 절차적 프로그래밍 | **진정한 객체지향 캡슐화 및 응집도 달성** |

#### 한줄 요약
- 빈혈 모델은 비즈니스 로직이 서비스에 파편화되고, 풍부한 도메인 모델은 객체 스스로 불변식을 통제한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **ACL(Anti-Corruption Layer)**: 레거시 시스템의 불량한 데이터 모델이나 외부 API 용어가 신규 도메인 모델을 오염시키지 않도록 경계에서 번역하는 완충 계층.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 레거시 시스템의 기형적 모델이 신규 도메인 오염 | Bounded Context 경계에 **ACL(Anti-Corruption Layer) 변환기** 배치 | 순수 도메인 모델 보호 및 점진적 전환 |
| Entity에 setter 공개로 비즈니스 불변식 파괴 | **`setter` 전면 금지 및 생성자/도메인 변경 메서드(`cancel()`) 강제** | 캡슐화 유지 및 잘못된 상태 전이 원천 차단 |
| 단순 CRUD 도메인에 DDD 강제 적용으로 생산성 저하 | **도메인 성격에 따라 핵심(Core)만 DDD, 일반은 CRUD 적용** | 불필요한 엔지니어링 비용 절감 |
| Aggregate 크기가 너무 커서 락(Lock) 경합 발생 | **Aggregate 최소화 및 타 Aggregate는 ID로만 참조** | 동시성 처리량 극대화 및 트랜잭션 범위 최소화 |

#### 한줄 요약
- DDD는 도메인 복잡도를 다루는 대신 모델링·학습 비용을 요구하므로, 핵심 도메인에만 적용하고 외부 시스템은 ACL로 격리해 남의 모델이 도메인을 오염시키지 않게 한다.

## Ⅶ. 결론

- 마이크로서비스 아키텍처(MSA) 도메인 분할 및 엔터프라이즈 소프트웨어의 **핵심 도메인 모델링 설계 방법론**으로 정립되었으며, 실무 적용 시에는 **이벤트 스토밍(Event Storming)을 통한 Bounded Context 도출, 세터(Setter)를 배제한 불변식(Invariant) 캡슐화, 외부 레거시 오염을 막는 부패방지계층(ACL), 핵심 도메인(Core Domain)에 리소스를 집중하는 선별적 전략**을 결합하여 가치를 극대화

#### 한줄 요약
- 도메인 주도 설계(DDD)는 소프트웨어의 중심을 기술 인프라가 아닌 비즈니스 본질에 일치시키는 현대 소프트웨어 공학의 정수다.
