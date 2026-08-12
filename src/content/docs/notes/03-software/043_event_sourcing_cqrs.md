---
sidebar:
  order: 43
  label: "043. 이벤트 소싱•CQRS (Event Sourcing CQRS)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "이벤트 소싱•CQRS (Event Sourcing CQRS)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 43
extra:
  question_no: "043"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "이벤트 소싱•CQRS는 상태 분리 설계 가치"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Event Sourcing**: 시스템의 현재 상태(Current State)만을 DB에 덮어써서 보관하는 대신, 상태를 변화시키는 모든 비즈니스 도메인 사건(Event)들을 순차적 추가 전용(Append-Only) 로그로 저장하여 상태를 재생(Replay) 및 복원하는 패턴.
- **CQRS (Command Query Responsibility Segregation)**: 시스템의 상태를 변경하는 명령(Command: C/U/D) 데이터 모델과, 상태를 단순 조회하는 쿼리(Query: R) 데이터 모델을 아예 데이터베이스 수준까지 분리(Separation)하는 아키텍처 패턴.
- **Event Store**: 이벤트 소싱 아키텍처에서 수정/삭제 없이 오직 Append-Only 방식으로만 이벤트 로그를 원자적으로 보관하는 이벤트 전용 데이터베이스.

</details>

- 정의/개념: 상태 변경 이벤트 자체를 불변(Immutable) 원본 데이터로 축적(Event Sourcing)하고, 쓰기 전용 Command 모델과 읽기 전용 Query 모델을 분리(CQRS)하는 결합 패턴인 **Event Sourcing & CQRS**
- 배경/필요성: traditional CRUD 기반의 덮어쓰기로 인한 과거 이력 및 감사 데이터 유실 방지, 읽기(Query)와 쓰기(Command) 트래픽의 스케일링 불균형 극복 요구성

#### 한줄 요약

- 이벤트 소싱과 CQRS로 이벤트 원본과 명령•조회 모델을 관리한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Append-Only Immutable Event**: 한번 발생하여 저장소에 기재된 이벤트는 절대 수정(UPDATE)되거나 삭제(DELETE)되지 않고, 변경이 필요한 경우 보상 이벤트(Compensating Event)를 추가 기재하는 특성.
- **Eventual Consistency (최종 일관성)**: 쓰기(Command) 저장소에 반영된 이벤트가 메시지 브로커를 거쳐 읽기(Query) 전용 DB로 동기화될 때까지 약간의 시간 지연(Lag)이 존재하나, 최종적으로는 데이터 정합성이 수렴하는 속성.

</details>

- **Append-Only** 방식의 완전한 감사 트레일(Audit Trail) 및 타임 트래블(Time Travel) 상태 복원
- 쓰기(Command) DB 대 읽기(Query) DB의 수평적 독립 확장성(Scale-out)
- **Eventual Consistency (최종 일관성)** 수용 및 **Snapshotting**을 통한 이력 재생 성능 최적화

#### 한줄 요약

- 추가 전용, 프로젝션, 결과적 일관성의 절충이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Projection (프로젝션)**: Event Store에 축적된 순차적 비즈니스 이벤트를 재생/가공하여, 읽기 전용 Query DB(RDBMS, Elasticsearch, Redis) 형태의 Read Model 데이터 뷰를 만드는 과정.
- **Snapshot (스냅샷)**: 수천 개 이상의 이벤트 이력을 매번 처음부터 재구성하는 오버헤드를 막기 위해, 특정 시점(e.g., 매 100번째 이벤트)의 도메인 상태를 주기적으로 덤프 저장하는 기술.

</details>

```text
          [명령 모델]
                |
         [이벤트 스토어]
                |
           [프로젝션]
                |
           [조회 모델]
```

선의 의미: Command 모델이 Event Store에 Append-Only로 이벤트를 발생시키면, Projection엔진이 비동기로 이벤트를 읽어 Read DB(Query 모델)로 동기화 반영하는 아키텍처.

| 구분 레이어 | 핵심 역할 및 기능 | 주요 사용 기술 / DB |
|:---|:---|:---|
| **Command Model (Write)** | 비즈니스 유효성 검증, C/U/D 연산 처리, 신규 도메인 이벤트 생성 | RDBMS, EventStoreDB, Axon |
| **Event Store (Storage)** | 발생된 이벤트를 **Append-Only** 불변 상태로 시퀀셜 저장 | EventStoreDB, Apache Kafka |
| **Projection (Sync Engine)** | 이벤트를 구독하여 Read Model 형태에 맞게 데이터 변환 및 동기화 | Event Handler, Kafka Connect |
| **Query Model (Read)** | 클라이언트의 complex 조회를 초고속 수행하는 전용 Read-only View | Elasticsearch, Redis, RDBMS |
| **Snapshot Manager** | 주기적 **Snapshot** 저장을 통해 Event Replay 성능 시간복잡도 $O(N) \rightarrow O(1)$ 단축 | S3, Redis Snapshot |

#### 한줄 요약

- 명령, 예상 버전, 이벤트 스토어, 조회가 쓰기와 읽기를 연결한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Replay (이벤트 재생)**: 버그 수정이나 신규 Read Model 구축 시, Event Store에 저장된 처음부터의 모든 이벤트를 재실행하여 원하는 형태의 뷰 DB를 재구성하는 기법.

</details>

```text
┌──────────────────────────────┐
│ 상태 변경 명령 (Command)     │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 유효성 검증 & 이벤트 생성 │
│ 2. Event Store Append 기재   │
│ 3. Event Broker 비동기 전파 │
│ 4. Projection 뷰 변환        │
│ 5. Read DB 반영 (Eventual)   │
└──────────────┬───────────────┘
               ▼
   [Query 단순 초고속 조회]
```

### 동작 원리

1. **Command 수신**: 클라이언트로부터 주문(CreateOrder) Command 전달.
2. **유효성 검증 & 이벤트 생성**: 도메인 로직 검증 후 `OrderCreatedEvent` 불변 객체 생성.
3. **Event Store Append**: Event Store에 원자적으로 Append-Only 저장.
4. **Projection 뷰 변환**: Kafka/Event Handler가 이벤트를 수신하여 Read 전용 Elasticsearch/RDBMS 뷰로 변환.
5. **Read DB 반영**: Query 모델 DB에 즉시 반영 및 클라이언트는 읽기 전용 API를 통해 **Eventual Consistency** 상태로 초고속 조회.

#### 한줄 요약

- 새 이벤트 추가 후 조회 모델•반영 버전 갱신으로 읽기 상태를 갱신한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **CQRS without Event Sourcing vs CQRS with Event Sourcing**: CQRS만 적용 시 Command DB와 Query DB를 일반 CRUD 형태로 분리하고, Event Sourcing 결합 시 Command DB 자체를 Event Store 기반으로 대체.

</details>

| 비교 항목 | Traditional CRUD Architecture | Event Sourcing + CQRS Architecture |
|:---|:---|:---|
| 데이터 저장 상태 | 현재 최종 데이터 상태만 UPDATE 덮어쓰기 | **모든 상태 변경 이벤트를 Append-Only 원본 저장** |
| 감사 및 이력 추적 | 별도 Audit 테이블 작성 필요 (누락 위험) | **완벽한 Audit Trail 및 과거 시점 복원(Time Travel)** |
| 읽기/쓰기 확장성 | 락(Lock) 경합으로 읽기/쓰기 상호 병목 유발 | **Read DB와 Write DB의 독립적 극대화 Scale-out** |
| 시스템 복잡도 | 낮음 (직관적 개발) | **높음 (이벤트 버전 관리, Eventual Consistency)** |

#### 한줄 요약

- 이력 복원은 이벤트 소싱, 독립 확장은 CQRS가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Event Versioning**: 이벤트 클래스 스키마가 변경(필드 추가/삭제)될 때 과거 저장된 구버전 이벤트와의 하향 호환성(Upcasting)을 유지하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 오랜 기간 축적된 이벤트로 인한 Replay 속도 저하 | **Snapshotting (주기적 상태 덤프 저장)** 인가 | 복원 시간 단축 |
| 시간 경과에 따른 이벤트 클래스 스키마 변형 | **Upcaster (이벤트 버저닝 변환기)** 구현 | 하향 호환성 보장 |
| Read DB 동기화 지연으로 인한 화면 갱신 시차 | 클라이언트 UI 차원의 **Optimistic UI Update** 또는 렌더링 지연 처리 | UX 불쾌감 소멸 |

> 사례: 금융/증권 거래소 타임 트래블 이력 시스템, **Axon Framework + EventStoreDB + Elasticsearch** 구축

#### 한줄 요약

- 이벤트 스키마 진화, 멱등 중복 처리, 프로젝션 지연을 통제한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **이벤트 소싱 CQRS 도입 기준(Event Sourcing CQRS Criteria)**: 변경 이력 감사 필수성, 읽기/쓰기 비율(e.g., 100:1), 및 도메인 복잡도에 기반한 채택 체계.

</details>

- **이벤트 소싱 CQRS 도입 기준**에 따라 금융 거래/주문 이력 등 미션 크리티컬 트랜잭션 시스템에 **Event Sourcing + CQRS** 선택 채택

#### 한줄 요약

- 상태 복원•독립 확장 이익과 스키마 진화 비용을 함께 평가하는 것이 핵심이다.
