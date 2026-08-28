---
sidebar:
  order: 50
  label: "050. 바운디드 컨텍스트"
  badge:
    text: "기출 · 50%"
    variant: note
title: "바운디드 컨텍스트 (Bounded Context)"
date: "2026-08-26T17:29:00+09:00"
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

<details><summary>용어 설명</summary>

- **바운디드 컨텍스트(Bounded Context)**: 동일한 도메인 용어가 특정한 의미를 갖는 명시적인 경계이자, 단일 도메인 모델이 적용되는 물리적/개념적 범위.
- **컨텍스트 맵(Context Map)**: 시스템 내에 존재하는 여러 Bounded Context 간의 관계(U/D, ACL, OHS 등)와 데이터 흐름을 시각화한 조감도.

</details>

- 정의/개념: 도메인 모델과 보편적 언어가 단일한 의미를 유지하도록 격리하고 **컨텍스트 맵과 ACL(오염방지계층)** 로 상호 통합하는 DDD 전략적 설계 경계
- 배경/필요성: 전사 단일 모델은 부서마다 다른 용어 의미를 하나의 스키마에 욱여넣어 결합도와 충돌 비용을 키우므로, 모델이 일관되게 통하는 범위를 바운디드 컨텍스트로 끊고 경계 사이는 컨텍스트 맵의 번역으로만 잇게 할 필요

#### 한줄 요약
- 도메인 용어의 의미가 일관되게 유지되는 명시적 경계를 정의하여 모델의 순수성을 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **업스트림 vs 다운스트림(Upstream/Downstream)**: 데이터와 정책을 공급하는 상류(Upstream: U)와 이를 소비하고 의존하는 하류(Downstream: D)의 관계.
- **콘웨이의 법칙(Conway's Law)**: 시스템 아키텍처 구조는 해당 시스템을 개발하는 조직의 의사소통 구조를 그대로 반영한다는 법칙.

</details>

- 경계 내부에서 **보편적 언어(Ubiquitous Language)** 의 단일하고 명확한 의미(Context) 보장
- **콘웨이의 법칙**에 따라 1개 팀이 1개 Bounded Context를 독립 소유 및 배포
- 컨텍스트 간 통합 시 **ACL, OHS(Open Host Service), Shared Kernel** 등 관계 패턴 적용

#### 한줄 요약
- 경계를 나누면 용어 일관성을 얻는 대신 경계마다 번역과 데이터 중복을 감수해야 하므로, 통합의 편의를 모델의 명확성과 맞바꾼다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **OHS(Open Host Service) & PL(Published Language)**: 업스트림이 다운스트림들에게 표준 프로토콜(REST)과 데이터 포맷(JSON/XML)으로 API를 공개하는 패턴.

</details>

```text
[Context Map 및 통합 패턴 구조]
|-- 업스트림 컨텍스트 (Upstream: 상품/결제 컨텍스트)
|   `-- OHS / PL (Open Host Service: 표준 REST API 및 도메인 이벤트 발행)
|-- 컨텍스트 맵 경계 (Context Map Boundary)
|   |-- Shared Kernel (공통 공유 커널 - 상호 합의 필수)
|   |-- Customer-Supplier (고객-공급자 협력 관계)
|   `-- ACL (Anti-Corruption Layer: 다운스트림 도메인 오염 방지 번역기)
`-- 다운스트림 컨텍스트 (Downstream: 주문/배송 컨텍스트)
    `-- 순수 내부 도메인 모델 (Order Aggregate)
```

선의 의미: 계층 및 컨텍스트 간 Upstream-Downstream 통합 구조

| 구성요소 | 책임 |
|:---|:---|
| Shared Kernel | 모델 일부의 **공동 소유·합의 변경** |
| Customer-Supplier | 상하류의 **요구 협력 관계** |
| Conformist | 상류 모델의 **무변환 수용** |
| ACL | 외부 모델의 **내부 모델 번역** |
| OHS·PL | 다수 소비자용 **표준 API·스키마 제공** |

#### 한줄 요약
- Context Map은 경계 자체가 아니라 경계 사이의 힘의 관계를 기록하므로, 업스트림과 다운스트림 중 어느 쪽이 변경을 감수하는지를 명시한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **이벤트 기반 비동기 통합**: 컨텍스트 간 동기 REST 호출 대신 Kafka 메시지 브로커를 경유하여 시간적/공간적 결합도를 제거하는 방식.

</details>

```text
업스트림(결제 컨텍스트)에서 결제 승인 완료
        │
   업스트림이 'PaymentApproved' 도메인 이벤트를 Kafka 브로커로 발행 (OHS/PL)
        │
   다운스트림(주문 컨텍스트)의 ACL(Anti-Corruption Layer)이 이벤트 수신
        │
   ACL이 업스트림의 결제 DTO를 주문 도메인의 `PaymentInfo` Value Object로 번역
        │
   주문 도메인 서비스가 번역된 VO를 적용하여 주문 상태를 '결제완료'로 갱신
```

#### 한줄 요약
- ACL이 번역을 맡기 때문에 업스트림 모델이 바뀌어도 다운스트림 도메인은 그대로 남으므로, 번역 계층의 유지 비용이 결합도를 낮춘 대가가 된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **단일 전사 통합 모델 vs Bounded Context 분할 모델**: 전사 단일 ERD를 구축하는 레거시 방식과 컨텍스트별로 분리된 모델을 유지하는 DDD 방식.

</details>

| 비교 항목 | 단일 전사 통합 모델 (Enterprise Model) | 바운디드 컨텍스트 분할 (Bounded Context) |
|:---|:---|:---|
| 용어 관리 | 전사 단일 용어 강제 (**의미 충돌 발생**) | **경계 내에서 용어의 단일 의미 완벽 보장** |
| 데이터베이스 | 수백 개 테이블의 단일 공유 DB | **컨텍스트별 독립 Database-per-Service** |
| 도메인 모델 | 속성이 수백 개인 거대 Fat Entity | **해당 문맥에 필요한 핵심 속성만 보유** |
| 조직 및 배포 | 전사 통합 배포 (소통 병목 극심) | **팀별 자율적인 독립 배포 (CI/CD)** |

#### 한줄 요약
- 전사 단일 모델의 의미 충돌과 배포 병목을 Bounded Context의 경계 분리로 해결한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **의미 충돌(Semantic Collision)**: 동일한 '사용자(User)'라는 단어가 인증 컨텍스트에서는 '계정/패스워드', 주문 컨텍스트에서는 '구매자/배송지'로 의미가 달라지는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| '사용자' 용어의 도메인별 의미 충돌로 스키마 비대화 | **인증(Account), 주문(Buyer), 배송(Recipient) 컨텍스트 분리** | 엔티티 경량화 및 문맥별 명확한 책임 부여 |
| 업스트림 레거시 API 변경으로 다운스트림 연쇄 파손 | 다운스트림 진입점에 **ACL(Anti-Corruption Layer)** 구축 | 레거시 스키마 변경의 내부 전파 원천 차단 |
| 복수 팀이 단일 Bounded Context를 공동 수정하며 충돌 | **콘웨이의 법칙 기반 1팀 = 1컨텍스트 소유권 확립** | 팀 간 소통 오버헤드 및 의사결정 병목 해소 |
| 과도하게 잘게 쪼갠 컨텍스트로 인한 네트워크 통신 급증 | **이벤트 스토밍을 통해 응집도가 높은 비즈니스 단위로 재통합** | 불필요한 분산 네트워크 오버헤드 방지 |

#### 한줄 요약
- 컨텍스트를 나누면 모델 일관성을 얻는 대신 경계마다 번역과 데이터 중복을 감수해야 하므로, ACL로 번역 지점을 명시하고 팀 경계와 컨텍스트 경계를 일치시켜 조정 비용을 줄인다.

## Ⅶ. 결론

- 서비스 분할은 **컨텍스트 경계**, 연계는 **ACL** 선택

#### 한줄 요약
- Bounded Context는 도메인 용어의 의미적 일관성을 지키고 MSA의 이상적인 서비스 경계를 도출하는 DDD 전략적 설계의 핵심이다.
