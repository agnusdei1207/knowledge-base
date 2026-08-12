---
sidebar:
  order: 50
  label: "050. 바운디드 컨텍스트 (Bounded Context)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "바운디드 컨텍스트 (Bounded Context)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 50
extra:
  question_no: "050"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "137회 기출, 컨텍스트 경계•통합 관계"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Bounded Context (바운디드 컨텍스트)**: DDD(도메인 주도 설계)에서 특정한 도메인 모델과 보편적 언어(Ubiquitous Language)가 일관되게 적용되는 명시적 경계(Boundary)로, 마이크로서비스(MSA) 서비스 분할의 1:1 직결 기준.
- **Context Map (컨텍스트 맵)**: 프로젝트 내에 존재하는 여러 Bounded Context 간의 상호 의존성, 통합 관계 및 데이터 흐름 방식을 시각화한 조감도.
- **Ubiquitous Language Scope**: 동일한 단어(e.g., 'Account')가 회계 컨텍스트에서는 '계좌', 마케팅 컨텍스트에서는 '사용자 계정'으로 다르게 의미 정의되는 경계 한계선.

</details>

- 정의/개념: 동일한 도메인 모델과 보편적 언어(Ubiquitous Language)의 무결성이 오롯이 유지되는 명시적 경계 영역인 **Bounded Context**
- 배경/필요성: 전사 단일 모델 구축 시 발생하는 도메인 용어의 의미 충돌 해결, MSA 아키텍처 상의 서브모듈 독립성 및 배포 경계 확보 요구성

#### 한줄 요약

- 도메인 모델과 공통 언어의 바운디드 컨텍스트가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Upstream / Downstream (U/D)**: Context 간 의존 방향을 나타내는 관계로, Upstream(U)은 데이터/계약을 제공하는 공급자, Downstream(D)은 그 계약에 의존하는 소비자.
- **Anti-Corruption Layer (ACL)**: Upstream의 모델이나 레거시 인터페이스 오염이 Downstream 도메인 모델로 들어오지 못하도록 중간에서 차단/변환해 주는 오염 방지 계층.

</details>

- 경계 내부 단일 보편적 언어(**Ubiquitous Language**) 100% 일관성 보장
- Bounded Context 1개당 1개 팀(Team) 전담 할당 (Conway's Law 준수)
- Context 간 관계 패턴 (**Shared Kernel, Customer-Supplier, Conformist, ACL**)

#### 한줄 요약

- 경계 내부, 컨텍스트 맵, 번역 계약이 의미 일관성을 보호한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Shared Kernel (공유 커널)**: 두 Bounded Context가 도메인 모델의 일부(코드/DB)를 밀접하게 공유하는 통합 관계.
- **Open Host Service (OHS) / Published Language (PL)**: Upstream 컨텍스트가 Downstream들에 표준화된 접근 프로토콜(REST/gRPC)과 데이터 표준 형식(JSON/XML)을 공개하는 관계.

</details>

```text
[업스트림 컨텍스트 (Upstream)]
          | (Published Language)
   [컨텍스트 맵 (Context Map)]
          |
  [오염 방지 계층 (ACL)]
          |
[다운스트림 컨텍스트 (Downstream)]
```

선의 의미: Upstream(U)의 데이터가 Published Language 및 ACL(Anti-Corruption Layer)을 경유하여 Downstream(D)의 pure 도메인 모델로 인입되는 매핑 구조.

| Context 관계 패턴 | 상호작용 방식 및 특징 |
|:---|:---|
| **Shared Kernel** | 두 Context가 도메인 모델 일부를 공동 소유하고 함께 변경 관리 |
| **Customer-Supplier** | Upstream(Supplier)이 Downstream(Customer)의 요구사항을 반영하여 개발 |
| **Conformist (준수자)** | Downstream이 Upstream의 도메인 모델을 변환 없이 그대로 받아들임 |
| **Anti-Corruption Layer (ACL)**| Downstream이 자신만의 모델을 보호하기 위해 중간에 **Translation Layer** 구축 |
| **Open Host Service (OHS)** | Upstream이 다수 소비자를 위해 표준화된 **API 서브시스템**을 제공 |
| **Separate Ways (각자의 길)**| 통합 비용이 너무 커서 상호 관계를 완전히 끊고 독립적으로 개발 |

#### 한줄 요약

- 업스트림, 공개 계약, ACL, 다운스트림의 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Event-Driven Context Integration**: Bounded Context 간 결합도를 최저로 낮추기 위해, REST API 직접 호출 대신 Domain Event (Kafka)를 발행하여 비동기 동기화하는 기법.

</details>

```text
[업스트림 상태 변경]
          │
          ▼
┌──────────────────────────────┐
│ 1. Domain Event 발행         │
│ 2. Kafka Message Broker 전달 │
│ 3. ACL (Anti-Corruption) 수신│
│ 4. 내부 언어 번역 (Mapping)  │
│ 5. 다운스트림 상태 반영      │
└──────────────┬───────────────┘
               ▼
   [독립적 데이터 일관성 완결]
```

### 동작 원리

1. **Domain Event 발행**: Upstream Bounded Context(주문)에서 `OrderPlaced` 이벤트 인가.
2. **Message Broker 전달**: Event Store 및 Kafka Topic에 불변 객체 기재.
3. **ACL (Anti-Corruption Layer) 수신**: Downstream Bounded Context(배송)의 ACL이 이벤트 트랩.
4. **내부 언어 번역**: Upstream의 용어 `Order`를 Downstream 내부 용어 `DeliveryPackage`로 Translate.
5. **다운스트림 상태 반영**: 배포 전용 DB에 보편적 언어 무결성을 유지하며 멱등(Idempotent) 커밋.

#### 한줄 요약

- 공개 계약 이벤트 발행부터 다운스트림 상태 반영까지의 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Single Model vs Bounded Context**: 전사 단일 모델은 모든 팀이 1개 대형 ERD/클래스를 공유하여 병목 유발, Bounded Context는 도메인별로 모델을 쪼개어 독립성 확보.

</details>

| 비교 항목 | Enterprise Shared Model (전체 공유) | Bounded Context (분리) |
|:---|:---|:---|
| 용어 정의 | 전사 단일 용어 집합 사용 (의미 오염발생) | **Context 경계 내에서만 독자적 의미 성립** |
| DB 스키마 | 대형 단일 RDBMS 공유 | **Context별 독립 DB (Database-per-service)** |
| 팀 간 의존성 | 커밋 시 전체 팀 간 충돌 발생 | **인터페이스(ACL/OHS)만 유지하면 독립 변경** |
| MSA 직결성 | 적용 불가 (Monolithic에 적합) | **마이크로서비스(MSA) 경계 1:1 매핑** |

#### 한줄 요약

- 의미•책임이 같으면 통합, 다르면 컨텍스트 분리가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Conway's Law (콘웨이의 법칙)**: 소프트웨어 아키텍처 구조는 그 소프트웨어를 개발하는 조직의 소통 구조를 그대로 반영한다는 법칙 (1 팀 = 1 Bounded Context 인가 이유).

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 경계 구분을 비즈니스가 아닌 기술/DB 테이블 위주로 나눔 | **Event Storming**을 거쳐 보편적 언어 경계로 재정립 | 도메인 독립성 확보 |
| Upstream의 거친 변화가 Downstream 코드를 붕괴시킴 | **Anti-Corruption Layer (ACL)** 변환기 인가 | 도메인 모델 오염 차단 |
| 1개 Bounded Context를 여러 개발팀이 공유 | **Conway's Law**에 의거 1개 팀당 1개 Context 매핑 | 소통 오버헤드 소멸 |

> 사례: 배달 애플리케이션 내 **주문 Context**, **결제 Context**, **라이더배차 Context** 분리 및 Context Map 수립

#### 한줄 요약

- 데이터 소유권, 명시적 번역, 계약 시험, 멱등성을 적용한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **컨텍스트 경계 설정 기준(Bounded Context Boundary Standards)**: Ubiquitous Language 일관성, 조직 구조(Conway's Law) 및 MSA 서비스 분할 타깃에 기반한 체계.

</details>

- **컨텍스트 경계 설정 기준**에 따라 MSA 아키텍처 수립 시 **Event Storming 기반 Bounded Context + ACL** 도출 인가

#### 한줄 요약

- 의미와 변경 책임을 함께 평가하는 것이 핵심이다.
