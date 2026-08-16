---
sidebar:
  order: 49
  label: "049. DDD 도메인 주도 설계 (Domain-Driven Design)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "DDD 도메인 주도 설계 (Domain-Driven Design)"
date: "2026-08-13T15:21:00+09:00"
tags:
  - "notes-software"
weight: 49
extra:
  question_no: "049"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "137회 기출, 도메인 모델•경계 설계"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **DDD (Domain-Driven Design)**: Eric Evans가 창안한 소프트웨어 설계 접근법으로, 복잡한 비즈니스 도메인을 중심으로 소프트웨어 모델을 구축하고 도메인 전문가와 개발자가 동일한 보편적 언어를 사용하는 개발 방법론.
- **Ubiquitous Language (보편적 언어)**: 기획자, 현업 전문가, 아키텍트, 개발자 등 모든 이해관계자가 요구사항 정의부터 소스코드의 클래스/메서드 명칭까지 통일되게 사용하는 단일 공통 언어.
- **Strategic vs Tactical Design**: DDD는 전사 도메인을 분할하는 전략적 설계(Bounded Context, Context Map)와 서비스 내부 객체를 모델링하는 전술적 설계(Entity, VO, Aggregate, Repository) 2개 레벨로 나뉨.

</details>

- 정의/개념: 기술 중심이 아닌 비즈니스 도메인 지식에 집중하여 현업과 개발팀이 동일한 보편적 언어(Ubiquitous Language) 기반으로 도메인 모델을 코드로 구체화하는 **DDD (Domain-Driven Design)**
- 배경/필요성: 업무 용어와 코드 모델 불일치는 **규칙 누락•해석 충돌** 유발

#### 한줄 요약

- DDD, 공통 언어, 도메인 모델을 통한 업무 지식 정제가 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Bounded Context**: 특정 모델과 보편적 언어가 일관된 의미를 갖는 명시적 경계.
- **Context Map**: 여러 Bounded Context 간의 관계(Upstream/Downstream, Shared Kernel, ACL)와 데이터 연동 방식을 시각화한 지도.

</details>

- 도메인 전문가와 개발자 간의 **Ubiquitous Language** 수립
- **Strategic Design (Bounded Context, Context Map)** 기반 MSA 분할 가이드
- **Tactical Design (Entity, Value Object, Aggregate, Repository)** 패턴 적용

#### 한줄 요약

- 전략적 설계, 전술적 설계, 불변 조건이 핵심 업무를 보호한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Aggregate & Aggregate Root**: 데이터 변경의 단위이자 트랜잭션 일관성을 보장하는 연관 객체 묶음(Aggregate)과, 외부에서 해당 묶음으로 접근 가능한 유일한 관문 객체(Aggregate Root).
- **Entity vs Value Object (VO)**: Entity는 고유 식별자(ID)와 연속된 생명주기를 가진 객체인 반면, Value Object는 식별자 없이 값(Value) 자체의 불변성(Immutability)만을 표현하는 객체.

</details>

```text
        [하위 도메인]
               |
     [바운디드 컨텍스트] ----- [컨텍스트 맵]
               |
        +------+------+
        |             |
  [공통 언어]    [도메인 모델]
```

선의 의미: 전략적 설계(Subdomain/Bounded Context/Context Map)가 수립된 후, 그 내부가 전술적 설계(Ubiquitous Language/Domain Model - Entity, VO, Aggregate)로 구현되는 체계.

| 구성요소 | 책임 |
|:---|:---|
| 하위 도메인 | 핵심•지원•일반 업무 문제 영역 분류 |
| 바운디드 컨텍스트 | 모델과 언어의 의미 경계 설정 |
| 컨텍스트 맵 | 경계 간 관계•번역•의존 방향 표현 |
| 공통 언어 | 현업과 개발의 모델 용어를 코드까지 일치 |
| 도메인 모델 | Entity•VO•Aggregate로 규칙과 불변 조건 구현 |

#### 한줄 요약

- 하위 도메인, 바운디드 컨텍스트, 컨텍스트 맵의 관계가 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Event Storming**: 도메인 전문가와 개발자가 한자리에 모여 주황색 포스트잇에 도메인 이벤트(Domain Event)를 시간순으로 벽면에 붙여가며 Bounded Context를 도출하는 워크숍 기법.

</details>

```text
┌──────────────────────────────┐
│ Event Storming 워크숍       │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. Domain Event / Command 도출│
│ 2. Ubiquitous Language 정의   │
│ 3. Bounded Context 경계 설정  │
│ 4. Aggregate & Root 모델링    │
│ 5. Tactical Design 코드 구현  │
└──────────────┬───────────────┘
               ▼
     [도메인 모델 완성]
```

### 동작 원리

1. Domain Event / Command 도출: 업무 사건과 이를 유발한 명령•행위자 탐색
2. Ubiquitous Language 정의: 용어 충돌을 정제해 공통 모델 언어 수립
3. Bounded Context 경계 설정: 모델 의미와 변경 책임이 응집된 경계 도출
4. Aggregate & Root 모델링: 트랜잭션 불변 조건과 외부 접근 관문 설계
5. Tactical Design 코드 구현: Entity•VO•Repository로 모델 구체화

#### 한줄 요약

- 업무 시나리오•예외 탐색부터 모델 기반 코드 구현까지 순환한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Anemic Domain Model (빈혈 도메인 모델)**: Entity 내부에 getter/setter만 존재하고 비즈니스 상태 변경 로직은 모두 외부 Service 클래스에 흩어져 있는 악성 antipattern.

</details>

| 비교 항목 | Anemic Domain Model (전통적) | Rich Domain Model (DDD 지향) |
|:---|:---|:---|
| 객체 상태/행위 | 상태(Data)와 행위(Logic)가 완전 분리 | **상태와 행위가 Entity 내부로 결합 캡슐화** |
| 비즈니스 유효성 | Service 계층에서 `if-else` 검증 | **Entity / VO 스스로 불변성(Invariant) 검증** |
| 객체지향성 | 데이터와 절차가 분리되기 쉬움 | 행위와 불변 조건의 **캡슐화** 강조 |
| 객체 변경 안전성 | 외부에서 setter로 무단 변경 가능 | **setter 배제 및 도메인 메서드로만 상태 변경** |

#### 한줄 요약

- 단순 업무는 스크립트, 복잡한 핵심 업무는 DDD가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **ACL (Anti-Corruption Layer)**: 다른 레거시 Bounded Context의 도메인 모델 오염이 내 순수한 도메인 모델로 들어오지 못하도록 중간에서 변환(Translate)해 주는 변환기 레이어.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 레거시 DB 구조가 신규 DDD 도메인 모델을 오염시킴 | **Anti-Corruption Layer (ACL)** 번역기 구현 | 순수 도메인 모델 보호 |
| 잦은 setter 사용으로 Entity 상태 제어 불능 | **setter 메서드 삭제** 및 의미 있는 도메인 메서드 인가 | 도메인 불변성(Invariant) 유지 |
| 단순 CRUD 시스템에 과도한 DDD 적용 | **Event Storming**을 거쳐 도메인 복잡도 높을 때만 적용 | 오버엔지니어링 차단 |

> 사례: **Event Storming 3단계 워크숍 + Spring Data JPA Aggregate Root** 아키텍처 정착

#### 한줄 요약

- 통합 계약, 번역 계층, 애그리게이트 루트로 모델 의미를 격리한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **DDD 도입 판정 기준(DDD Adoption Standards)**: 비즈니스 도메인의 복잡성, 현업의 참여도 및 MSA 전환 요구에 의거한 체계.

</details>

- 복잡한 핵심 업무는 **DDD**, 단순 CRUD는 **Transaction Script** 선택

#### 한줄 요약

- 업무 복잡도•차별성과 설계 비용을 함께 평가하는 것이 핵심이다.
