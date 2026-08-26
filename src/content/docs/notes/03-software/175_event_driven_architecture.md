---
sidebar:
  order: 175
  label: "175. 이벤트 기반 아키텍처"
  badge:
    text: "미출 · 70%"
    variant: note
title: "이벤트 기반 아키텍처 (Event-Driven Architecture)"
date: "2026-08-26T10:11:00+09:00"
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
- 배경/필요성: 동기식(HTTP) 연쇄 호출 구조에서 발생하는 **시간적 강결합, 단일 서비스 장애의 전사 전파(Cascading Failure) 및 응답 지연 누적 해결 불가**

#### 한줄 요약
- 비동기 이벤트 발행·구독을 통해 서비스 간 결합도를 제거하고 최종 일관성과 확장성을 달성한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Eventual Consistency**: 실시간 동기 일치 대신 메시지 브로커를 거쳐 시차를 두고 데이터가 일치되는 최종 일관성 모델.
- **Fire-and-Forget**: 생산자가 이벤트를 브로커에 발행한 후 소비자의 처리 완료를 기다리지 않고 즉시 제어권을 반환하는 비동기 패턴.

</details>

- 생산자와 소비자가 서로의 존재를 알 필요가 없는 **시간적·공간적 느슨한 결합(Decoupling)**
- 실시간 2PC 트랜잭션 락 없이 비동기 정합성을 달성하는 **최종 일관성(Eventual Consistency)**
- 브로커 버퍼링을 통해 트래픽 스파이크를 흡수하는 **높은 탄력성 및 수평 확장성**

#### 한줄 요약
- 느슨한 결합, 최종 일관성, 높은 복원력을 통해 대규모 분산 트래픽을 유연하게 처리한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **EDA 4대 아키텍처 구성요소**: Event Producer(발행자), Transactional Outbox(원자 저장), Message Broker(Kafka 채널), Event Consumer(멱등 소비자).

</details>

```text
[이벤트 기반 아키텍처(EDA) 및 Transactional Outbox 구조]
|-- 1. Event Producer Service (주문 서비스)
|   |-- Business Database (RDBMS: `Orders` 테이블 데이터 저장)
|   `-- Transactional Outbox (`Outbox` 테이블에 이벤트를 동일 트랜잭션으로 원자적 커밋)
`-- 2. CDC & Event Ingestion Layer (Debezium Engine -> DB WAL 로그 추출)
`-- 3. Event Channel / Message Broker (Apache Kafka 클러스터)
|   |-- Topics & Partitioning (주문 파티션 로그 영속 보관 및 재생 지원)
|   `-- Schema Registry (Avro / JSON Schema 계약 검증)
`-- 4. Event Consumer Services (구독 서비스)
    |-- Payment Service (이벤트 수신 -> 결제 처리 -> 멱등성 테이블 기록)
    `-- Inventory Service (이벤트 수신 -> 재고 차감 -> 오프셋 커밋)
```

선의 의미: 계층 및 비즈니스 데이터와 이벤트를 Outbox에 원자 저장하고 CDC를 통해 Kafka로 발행하여 구독자가 멱등 처리하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **이벤트 생산자 (Producer)** | 상태 변화를 **불변 이벤트로 모델링하고 Transactional Outbox에 안전 저장** | 발행 주체 |
| **메시지 브로커 (Broker)** | 이벤트를 파티션 디스크에 영속 저장하고 **구독자에게 순서 보장 및 재생(Replay) 제공**| Kafka, RabbitMQ |
| **이벤트 소비자 (Consumer)** | 이벤트를 구독하여 비즈니스 로직을 수행하고 **고유 Event ID 기반 멱등 처리** | 비동기 처리기 |
| **스키마 레지스트리** | 생산자와 소비자 간의 **이벤트 스키마 변경 및 상하위 호환성(Avro/JSON) 검증** | 데이터 계약 거버넌스 |

#### 한줄 요약
- 생산자, 메시지 브로커, 멱등 소비자, 스키마 레지스트리가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Transactional Outbox 발행 및 소비 5단계**: 비즈니스/Outbox 원자 커밋 $\to$ CDC 변경분 감지 $\to$ Kafka 발행 $\to$ Consumer 멱등 처리 $\to$ 결과 저장 및 오프셋 커밋.

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

#### 한줄 요약
- 원자 커밋 → CDC 감지 → 브로커 발행 → 멱등 처리 → 오프셋 커밋 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Event Notification vs Event-Carried State Transfer**: 단순 사건 알림(Notification)과 전체 상태 데이터를 포함하는 전송(State Transfer).

</details>

| 비교 항목 | 이벤트 알림 (Event Notification) | 상태 전송 (Event-Carried State Transfer) |
|:---|:---|:---|
| 페이로드 데이터 | **최소 식별자만 포함 (`{ orderId: 100 }`)**| **전체 상태 데이터 포함 (주문·금액·사용자 일괄)**|
| 추가 API 질의 | **소비자가 상세 조회를 위해 생산자 REST 호출**| **추가 API 호출 0회 (이벤트 데이터만으로 완결)** |
| 런타임 결합도 | 생산자 서버 가용성에 런타임 종속 잔존 | **완벽한 독립성 (생산자가 다운되어도 처리 가능)** |
| 네트워크 대역폭 | 작음 (경량 메시지) | 상대적 큼 (대용량 메시지) |

#### 한줄 요약
- 단순 신호 전달은 이벤트 알림, 생산자 의존성을 완전히 제거하려면 상태 전송(ECST)을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Dual-Write Problem**: DB 저장 성공 후 네트워크 오류로 Kafka 발행에 실패하여 DB와 메시지 브로커 간 정합성이 깨지는 난제.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| DB 저장과 Kafka 발행 간 불일치 (Dual-Write) | **Transactional Outbox 패턴 및 Debezium CDC 파이프라인 구축** | 이벤트 발행 누락 0건 보장 |
| 네트워크 재시도로 인한 이벤트 중복 수신 | **소비자 측 DB에 고유 `event_id` Unique 인덱스 및 멱등 처리 로직 구현**| 중복 결제 및 부작용 원천 차단 |
| 결함 메시지가 파티션을 가로막고 무한 재시도 (Poison Pill)| **재시도 3회 초과 시 DLQ(Dead Letter Queue)로 격리 후 후속 메시지 처리** | 파이프라인 정체 방지 |
| 이벤트 스키마 임의 변경으로 소비자 역직렬화 에러 | **Schema Registry 도입 및 `BACKWARD` 호환성 정책 강제** | 무중단 스키마 진화 보장 |

#### 한줄 요약
- Outbox 패턴, 멱등성 보장, DLQ 격리, 스키마 레지스트리로 운영한다.

## Ⅶ. 결론

- 대규모 분산 마이크로서비스 환경에서 시스템 간 결합도를 제거하고 고가용성을 달성하기 위해 **Transactional Outbox와 Debezium CDC 기반의 Apache Kafka 이벤트 기반 아키텍처를 표준 도입**하고, **Consumer 멱등성 보장과 DLQ 격리 정책**을 결합하여 완벽한 비동기 분산 플랫폼 완성

#### 한줄 요약
- 이벤트 기반 아키텍처는 불변 이벤트의 비동기 발행·구독과 최종 일관성을 통해 마이크로서비스 간의 시간적·공간적 결합을 완벽히 해소하는 핵심 분산 아키텍처다.