---
sidebar:
  order: 175
  label: "175. 이벤트 기반 아키텍처 (Event-Driven Architecture)"
  badge:
    text: "미출 • 70%"
    variant: note
title: "이벤트 기반 아키텍처 (Event-Driven Architecture)"
date: "2026-08-14T03:32:00+09:00"
tags:
  - "notes-software"
weight: 175
extra:
  question_no: "175"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "비동기 결합•계약•재생의 분산 설계 가치"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **EDA (Event-Driven Architecture)**: 마이크로서비스 간에 API를 직접 호출(Sync)하지 않고, 특정 상태의 변화를 나타내는 이벤트(사건)를 발행(Publish)하면 관심 있는 서비스가 비동기적으로 구독(Subscribe)하여 처리하는 느슨한 결합 아키텍처.
- **Event (이벤트/사건)**: 시스템 내에서 의미 있는 상태 변화가 일어났음을 나타내는 불변(Immutable)의 과거 시제 기록 (예: `OrderCreated`, `PaymentCompleted`).
- **Decoupling (느슨한 결합)**: 이벤트를 발행하는 생산자(Producer)는 누가 이벤트를 소비하는지 알 필요가 없으며, 단지 메시지 브로커에 던지기만 하면 되는 독립적 상태.

</details>

- 정의/개념: 상태 변화 Event를 발행•구독하는 **EDA**
- 배경/필요성: 동기 연쇄 호출은 **시간 결합•장애 전파•지연 누적** 발생

#### 한줄 요약

- 주문 서비스가 수신자 주소를 모르고 주문 생성 사건을 게시하면 결제·재고·알림 서비스가 각자 속도로 읽어 처리한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Asynchronous (비동기성)**: 이벤트를 발행한 후, 소비자가 처리를 완료할 때까지 기다리지 않고 즉각 자신의 다음 작업을 수행하는(Fire and Forget) 통신 특성.

</details>

- **Loose Coupling (생산자와 소비자 간의 시간적, 공간적, 수량적 완벽한 분리)**
- **Eventual Consistency (실시간이 아닌 일정 시간 후 시스템 간 데이터가 일치되는 최종 일관성 지향)**
- **Scalability & Resiliency (구독자별 독립적인 확장성 및 특정 서버 장애 시에도 이벤트 유실 없는 탄력성)**

#### 한줄 요약

- 생산자와 소비자가 동시에 켜져 있지 않아도 브로커가 사건을 보관하지만 지연·중복·순서를 각 소비자가 명시적으로 다뤄야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Message Broker (메시지 브로커)**: 발행된 이벤트를 안전하게 저장하고 구독자에게 라우팅해 주는 중앙 허브 인프라 (Apache Kafka, RabbitMQ, AWS SNS/SQS).

</details>

```text
[Event Channel]
 ├── [Event Producer]
 ├── [Event Consumer]
 └── [Schema Registry]
```

| 구성요소 | 책임 |
|---|---|
| Event Producer | 상태 변화를 **불변 Event**로 발행 |
| Event Channel | Event **저장•순서•전달•재생** 제공 |
| Event Consumer | 구독 Event를 **멱등 처리**하고 결과 저장 |
| Schema Registry | 생산자•소비자 간 **계약 호환성** 검증 |

#### 한줄 요약

- 아웃박스가 발송 대장을 업무와 함께 적고 브로커가 배달하며 소비자는 수령 번호를 저장해 같은 소포가 다시 와도 한 번만 반영한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Transactional Outbox Pattern**: 데이터베이스에 비즈니스 데이터를 저장하는 트랜잭션과 동일한 트랜잭션으로 'Outbox' 테이블에 이벤트를 저장하여, 서버가 죽어도 이벤트 발행 누락을 방지하는 필수 패턴.

</details>

```text
[업무 변경 요청]
      │
      ▼
1. 업무•Outbox 원자 저장
      │
      ▼
2. CDC로 Outbox 변경 감지
      │
      ▼
3. Event Channel 발행
      │
      ▼
4. Consumer 멱등 처리
      │
      ▼
5. 처리 결과•Offset 저장
      │
      ▼
[비동기 상태 반영]
```

### 동작 원리

1. **업무•Outbox 원자 저장**: Domain 변경과 발행 기록 Commit
2. **CDC로 Outbox 변경 감지**: Transaction Log에서 Event 추출
3. **Event Channel 발행**: Key•Schema•Header와 함께 전달
4. **Consumer 멱등 처리**: Event ID로 중복 Side Effect 차단
5. **처리 결과•Offset 저장**: 결과와 소비 위치를 일관되게 기록

#### 한줄 요약

- 주문과 발행 기록을 함께 저장하고 소비자가 처리 번호와 결과를 함께 커밋하면 전송이 반복돼도 결제는 한 번만 남는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Event-Carried State Transfer (상태 전송 이벤트)**: 이벤트 데이터 안에 소비자가 필요로 하는 모든 상태 정보(주문액, 유저명)를 꽉 채워서 보내, 소비자가 생산자에게 다시 REST API를 질의할 필요가 없게 만드는 설계 기법.

</details>

| 비교 항목 | Event Notification (이벤트 알림) | Event-Carried State Transfer (상태 전송) |
|:---|:---|:---|
| 페이로드 크기 | 매우 작음 (식별자 ID만 포함) | **상대적으로 큼 (관련 데이터 모두 포함)**|
| 이벤트 예시 | `{"order_id": 123, "status": "created"}` | **`{"order_id": 123, "amount": 5000, "user": "A"}`** |
| 추가 API 호출 | **소비자가 생산자 API를 다시 호출하여 상세 조회**| **이벤트만으로 로직 수행 가능 (독립적)** |
| 결합도 | 상세 조회 시 Runtime 결합 잔존 | **Schema•Data 결합** 증가 |

#### 한줄 요약

- 알림은 사건만 알려 주고 상태 전송은 처리할 값까지 담으며 이벤트 소싱은 처음부터 모든 변경을 다시 재생할 수 있게 남긴다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Idempotency (멱등성)**: 네트워크 재시도나 브로커 오류로 인해 "동일한 이벤트가 2번 이상 수신"되더라도, 결제 중복 차감과 같은 사이드 이펙트 없이 1번만 처리한 것과 같은 상태를 유지하는 설계.

</details>

| 3대 EDA 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Dual-Write Problem | DB 저장 성공 후, Kafka 전송 직전 서버 다운| **Transactional Outbox 패턴 및 CDC 도입**|
| 2. Event Duplication | 브로커의 재전송(At-Least-Once)으로 2번 처리 | **소비자 측 DB에 고유 `event_id` 처리 여부(멱등성) 체크 로직 필수** |
| 3. Poison Message | 버그가 있는 메시지가 파티션 맨 앞을 막고 무한 재시도| **일정 횟수 실패 시 DLQ(Dead Letter Queue)로 격리 조치** |

> 사례: **토스 / 배달의민족 MSA 전환 시 Kafka 비동기 이벤트 통신 및 Spring Outbox Pattern 적용 사례**

#### 한줄 요약

- 실패 메시지를 끝없이 같은 파티션에서 재시도하지 말고 DLQ로 격리해 정상 주문을 계속 처리한 뒤 원인을 고쳐 재전송해야 한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **EDA 수립 기준**: 비동기 느슨한 결합(Decoupling), Transactional Outbox를 통한 원자성 보장, 멱등성(Idempotency) 기반 소비자 설계 및 DLQ 격리에 의거한 체계.

</details>

- 즉시 일관성은 **동기 호출**, 지연 허용 흐름은 Outbox 기반 EDA

#### 한줄 요약

- 즉시 일관성이 필요한 업무는 동기 경계를 유지하고 최종 일관성을 허용하는 흐름은 아웃박스·멱등성·스키마·DLQ를 갖춘 이벤트 방식으로 분리해야 한다.
