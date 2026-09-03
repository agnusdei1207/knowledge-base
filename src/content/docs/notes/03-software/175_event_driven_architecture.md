---
sidebar:
  order: 175
  label: "175. 이벤트 기반 아키텍처"
  badge:
    text: "미출 · 70%"
    variant: note
title: "이벤트 기반 아키텍처 (Event-Driven Architecture)"
date: "2026-08-31T10:48:00+09:00"
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

- **EDA(Event-Driven Architecture)**: 상태 변화(Event)를 발행하고 구독하는 비동기 메시지 채널을 통해 서비스 간 결합도를 최소화하는 분산 아키텍처.
- **Event**: 시스템 내에서 발생한 비즈니스 상태 변화를 나타내는 불변(Immutable)의 과거 시제 팩트(Fact) 메시지.

</details>

- 정의/개념: 상태 변화(Event)를 불변 메시지로 발행하고 **다수의 구독 서비스가 이를 비동기 수신하여 독립 처리하는 느슨한 결합 기반의 분산 아키텍처**
- 배경/필요성: 마이크로서비스 간 동기 호출 체인 증가 시 발생하는 **강한 시공간적 결합도, 단일 서비스 장애의 전체 연쇄 전파(Cascading Failure) 및 트래픽 스파이크 병목 한계**

#### 한줄 요약
- 비동기 발행·구독으로 시간적 결합을 줄이고 최종 일관성을 관리한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Eventual Consistency**: 실시간 동기 일치 대신 메시지 브로커를 거쳐 시차를 두고 데이터가 일치되는 최종 일관성 모델.
- **Fire-and-Forget**: 생산자가 이벤트를 브로커에 발행한 후 소비자의 처리 완료를 기다리지 않고 즉시 제어권을 반환하는 비동기 패턴.

</details>

- 생산자와 소비자가 서로의 존재를 알 필요가 없는 **시간적·공간적 느슨한 결합(Decoupling)**
- 실시간 2PC 트랜잭션 락 없이 비동기 정합성을 달성하는 **최종 일관성(Eventual Consistency)**
- 브로커 버퍼링을 통해 트래픽 스파이크를 흡수하는 **높은 탄력성 및 수평 확장성**

#### 한줄 요약
- 동기 응답의 즉시성을 포기한 대가로 장애 격리와 확장성을 얻는 구조이므로, 결과를 그 자리에서 확정해야 하는 거래에는 그대로 적용되지 않는다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **EDA 4대 아키텍처 구성요소**: Event Producer(발행자), Transactional Outbox(원자 저장), Message Broker(Kafka 채널), Event Consumer(멱등 소비자).

</details>

```text
[이벤트 기반 아키텍처(EDA) 및 Transactional Outbox 구조]
|-- Event Producer Service
|   |-- Business Database (RDBMS: `Orders` 테이블 데이터 저장)
|   `-- Transactional Outbox (`Outbox` 테이블에 이벤트를 동일 트랜잭션으로 원자적 커밋)
|-- CDC & Event Ingestion Layer
|-- Event Channel / Message Broker
|   |-- Topics & Partitioning (주문 파티션 로그 영속 보관 및 재생 지원)
|   `-- Schema Registry (Avro / JSON Schema 계약 검증)
`-- Event Consumer Services
    |-- Payment Service
    `-- Inventory Service
```

선의 의미: 계층 및 비즈니스 데이터와 이벤트를 Outbox에 원자 저장하고 CDC를 통해 Kafka로 발행하여 구독자가 멱등 처리하는 구조

| 구성요소 | 책임 |
|:---|:---|
| 이벤트 생산자 | 상태 변화를 **불변 이벤트**로 모델링 |
| Transactional Outbox | 데이터와 발행 대상을 로컬 원자 저장 |
| CDC 계층 | Outbox 변경을 읽어 브로커에 전달 |
| 메시지 브로커 | 이벤트 저장·라우팅·재생 지원 |
| 이벤트 소비자 | 고유 Event ID 기반 **멱등 처리** |
| 스키마 레지스트리 | 이벤트 계약과 호환성 정책 검증 |

#### 한줄 요약
- Outbox와 CDC가 DB 커밋과 이벤트 발행을 하나의 원자 단위로 묶고 브로커가 소비 시점을 미뤄 주므로, 생산자와 소비자가 같은 시각에 살아 있지 않아도 흐름이 성립한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Outbox 처리**: 원자 커밋, CDC 감지, 발행, 멱등 소비.

</details>

```text
주문 생성 비즈니스 요청 발생
        │
   1. [원자적 커밋] 비즈니스 데이터(`Orders`)와 이벤트(`Outbox`)를 단일 로컬 트랜잭션으로 DB 커밋
        │
   2. [CDC 로그 감지] Debezium이 DB 트랜잭션 로그(WAL/Binlog)를 읽어 Outbox 변경분 실시간 추출
        │
   3. [브로커 발행] 추출된 `OrderCreated` 이벤트를 Kafka 토픽 파티션으로 안정적 발행
        │
   4. [Consumer 멱등 처리] 결제 서비스가 이벤트를 읽고 고유 `event_id` 중복 여부를 DB에서 검증 후 처리
        │
   비즈니스 상태를 갱신하고 Kafka 오프셋을 커밋하여 비동기 상태 반영 완료
```

동작 원리:

1. 원자적 커밋: 업무 데이터와 Outbox 동시 저장
2. CDC 로그 감지: Outbox 변경분 추출
3. 브로커 발행: 이벤트를 토픽에 전달
4. Consumer 멱등 처리: 중복 확인 후 업무 반영

#### 한줄 요약
- 이중 쓰기 대신 로컬 커밋과 CDC를 거치면 발행 누락이 유실이 아니라 지연으로 바뀌며, 오프셋 커밋 지점이 재처리해야 할 범위의 경계를 정한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Event Notification vs Event-Carried State Transfer**: 단순 사건 알림(Notification)과 전체 상태 데이터를 포함하는 전송(State Transfer).

</details>

| 비교 항목 | 이벤트 알림 (Event Notification) | 상태 전송 (Event-Carried State Transfer) |
|:---|:---|:---|
| 페이로드 데이터 | **최소 식별자만 포함 (`{ orderId: 100 }`)**| **전체 상태 데이터 포함 (주문·금액·사용자 일괄)**|
| 추가 API 질의 | 상세 데이터 조회가 필요할 수 있음 | 이벤트만으로 처리 가능하도록 설계 |
| 런타임 결합도 | 생산자 API 가용성에 의존 가능 | 생산자 API 의존 감소·계약 결합 잔존 |
| 네트워크 대역폭 | 작음 (경량 메시지) | 상대적 큼 (대용량 메시지) |

#### 한줄 요약
- 단순 신호 전달은 이벤트 알림, 생산자 의존성을 완전히 제거하려면 상태 전송(ECST)을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Dual-Write Problem**: DB 저장 성공 후 네트워크 오류로 Kafka 발행에 실패하여 DB와 메시지 브로커 간 정합성이 깨지는 난제.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| DB와 브로커의 **Dual-Write 불일치** | **Transactional Outbox·CDC** 적용 | 발행 누락의 복구 경로 제공 |
| 재시도에 따른 이벤트 중복 수신 | 고유 Event ID와 **멱등 처리** 적용 | 중복 부작용 제한 |
| Poison Pill의 반복 실패 | 정책 횟수 재시도 후 **DLQ 격리** | 후속 이벤트의 처리 정체 방지 |
| 스키마 변경에 따른 역직렬화 오류 | **Schema Registry·호환성 정책** 적용 | 호환되지 않는 계약 변경 차단 |

#### 한줄 요약
- 네 대책은 시간적 결합을 끊은 대가로 생긴 중복·정체·계약 문제를 멱등성과 격리 큐로 되사는 선택이며, 최종 일관성 구간의 지연 자체는 남는다.

## Ⅶ. 결론

- 대규모 분산 클라우드 환경 및 실시간 데이터 스트리밍 시스템의 **가장 지배적인 비동기 마이크로서비스 확장 아키텍처 패러다임**으로 정립되었으며, 실무 구축 시에는 **DB 쓰기와 메시지 발행의 원자성을 보장하는 Transactional Outbox 및 Debezium CDC 패턴, 네트워크 재시도 시 부작용을 방지하는 컨슈머 멱등성(Idempotent Consumer) 보장, 독성 메시지(Poison Pill)를 격리하는 DLQ(Dead Letter Queue), 스키마 붕괴를 막는 Confluent Schema Registry**를 결합하여 데이터 유실 없는 안정적인 최종 일관성 비동기 시스템을 완성

#### 한줄 요약
- EDA에는 Outbox·멱등성·계약 호환성 정책을 함께 적용한다.
