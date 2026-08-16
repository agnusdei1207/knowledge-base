---
sidebar:
  order: 44
  label: "044. Saga 패턴: 분산 트랜잭션 (Saga Pattern)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "Saga 패턴: 분산 트랜잭션 (Saga Pattern)"
date: "2026-08-13T15:02:00+09:00"
tags:
  - "notes-software"
weight: 44
extra:
  question_no: "044"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "Saga는 분산 보상 트랜잭션 설계 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Saga Pattern**: 마이크로서비스 아키텍처(MSA) 환경에서 단일 ACID DB 트랜잭션을 사용할 수 없을 때, 각 서비스의 로컬 트랜잭션을 순차 실행하고 중간 실패 시 보상 트랜잭션(Compensating Transaction)을 역순으로 실행하여 최종 일관성(Eventual Consistency)을 달성하는 분산 트랜잭션 패턴.
- **Compensating Transaction (보상 트랜잭션)**: 이미 성공하여 로컬 DB에 커밋(Commit)된 과거 트랜잭션의 효과를 역으로 상쇄(Undo/Rollback)시키는 비즈니스 반대 연산 (e.g., 결제 취소, 재고 복원).
- **2PC (Two-Phase Commit)**: 분산 DB 트랜잭션의 전통적 방식으로 Prepare/Commit 2단계를 거치며, 전역 락(Global Lock)으로 인한 락 경합 및 성능 저하 유발.

</details>

- 정의/개념: 각 마이크로서비스별 독립 로컬 트랜잭션 커밋 후, 실패 발생 시 역순으로 **보상 트랜잭션**을 실행하여 데이터 최종 일관성을 수습하는 **Saga Pattern**
- 배경/필요성: 서비스별 DB에서는 단일 로컬 트랜잭션으로 **원자적 변경 불가**

#### 한줄 요약

- 로컬 커밋 연결과 역순 보상 기반 사가 패턴이 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Choreography Saga**: 중앙 컨트롤러 없이 각 서비스가 비동기 이벤트를 발행/구독(Pub/Sub)하여 자율적으로 다음 트랜잭션 및 보상 트랜잭션을 연쇄 실행하는 방식.
- **Orchestration Saga**: 중앙의 전용 오케스트레이터(Saga Orchestrator) 서비스가 각 마이크로서비스에 실행 커맨드를 하달하고 전체 사가 상태(State)를 총괄 관리하는 방식.

</details>

- 2PC 전역 락 제거 및 **Local Transaction + Compensating Transaction** 조율
- **Choreography (이벤트 기반 자율)** 대 **Orchestration (중앙 제어)** 2대 방식 제공
- **Eventual Consistency (최종 일관성)** 수용 및 **Isolation (격리성)** 부재 극복 대책 필요

#### 한줄 요약

- 전역 잠금 회피와 중간 상태•보상 트랜잭션 복잡도의 절충이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Saga Orchestrator**: Orchestration 방식에서 사가의 전 과정 진행 상태(State Machine)를 DB에 보관하며, 서비스들에 수행 커맨드 전송 및 실패 시 보상 명령을 순차 하달하는 중앙 제어기.

</details>

```text
[Saga 상태 저장소]
         |
         |
[흐름 제어기] -------- [메시지 채널] -------- [참여 서비스•로컬 저장소]
```

선의 의미: Orchestrator 또는 Message Broker가 각 마이크로서비스에 명령/이벤트를 전달하여 로컬 DB 커밋 및 실패 시 보상 트랜잭션을 순차 실행하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| Saga 상태 저장소 | 단계•시도•보상 상태와 상관 식별자 보존 |
| 흐름 제어기 | 다음 로컬 작업 또는 역순 보상 결정 |
| 메시지 채널 | 명령•이벤트를 멱등하게 전달 |
| 참여 서비스•로컬 저장소 | 로컬 트랜잭션과 보상 연산 수행 |

#### 한줄 요약

- 흐름 제어기, Saga 상태 저장소, 메시지 채널, 재전송이 분산 흐름을 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Compensating Flow (보상 흐름)**: 3단계(e.g., 배송)에서 실패 발생 시, 2단계(결제) $\rightarrow$ 1단계(주문) 순서로 역순의 보상 트랜잭션을 실행하여 상태를 취소 수습하는 흐름.

</details>

```text
[사가 요청]
    │
    ▼ 1. 주문 생성
[주문 완료]
    │
    ▼ 2. 결제 승인
[결제 완료]
    │
    ▼ 3. 재고 차감
    ├─ 성공 ─▶ [사가 완료]
    └─ 실패 ─▶ 4. 역순 보상 처리
                    │
                    ▼ 5. 최종 정합성 회복
                 [실패 결과]
```

### 동작 원리

1. **주문 생성**: 주문 서비스의 로컬 트랜잭션 커밋
2. **결제 승인**: 결제 서비스의 로컬 트랜잭션 커밋
3. **재고 차감**: 재고 서비스가 차감 가능 여부 판정•커밋
4. **역순 보상 처리**: 실패 시 결제 취소와 주문 취소를 역순 실행
5. **최종 정합성 회복**: 보상 결과를 대사하고 사가 실패 상태 확정

#### 한줄 요약

- 단계 실패 시 역순 보상 범위 확정과 보상 트랜잭션 실행이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Choreography vs Orchestration**: Choreography는 비동기 Pub/Sub 기반으로 서비스 간 결합도가 낮으나 복잡해지면 추적 난항, Orchestration은 중앙 관리로 흐름 추적이 쉬우나 Orchestrator 결합도 증가.

</details>

| 비교 항목 | Choreography Saga (코레오그래피) | Orchestration Saga (오케스트레이션) |
|:---|:---|:---|
| 제어 방식 | **이벤트 기반 자율 전파 ** | **중앙 Saga Orchestrator 제어** |
| 서비스 결합도 | 매우 낮음 (타 서비스의 존재를 알 필요 없음) | 중간 (Orchestrator가 각 서비스를 호출) |
| 시스템 복잡도 | 서비스가 적을 때 유용 (많아지면 엉킴) | **복잡한 다단계 트랜잭션 통제에 최적** |
| 흐름 추적성 | 난해함 (이벤트 흐름 추적 도구 필수) | **명확함 (Orchestrator DB에서 사가 상태 확인)** |
| 대표적 도구 | Apache Kafka, RabbitMQ | **Temporal, Camunda, AWS Step Functions** |

#### 한줄 요약

- 복잡한 분기는 오케스트레이션, 단순 연쇄는 코레오그래피가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Lack of Isolation (격리성 부재)**: 사가 진행 중 중간 커밋 데이터(Dirty Read)가 타 트랜잭션에 노출되어 데이터 불일치가 유발되는 한계.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Saga의 **Lack of Isolation (격리성 부재)** 로 인한 Dirty Read | **Semantic Lock (상태 값: PENDING 명시)** 적용 | 타 트랜잭션의 오작동 차단 |
| 보상 트랜잭션($C_n$) 실행 자체의 실패 | **Exponential Backoff 재시도** 및 수동 큐(DLQ) 이송 | 보상 실패 리스크 해소 |
| 이중 이벤트 전송에 따른 중복 커밋 | **Transactional Outbox Pattern + 멱등성(Idempotency)** | 이중 처리 방지 |

> 사례: 배달의민족 / 쿠팡 주문-결제-라이더배차 사가 아키텍처 (**Event-driven Orchestration**)

#### 한줄 요약

- 트랜잭셔널 아웃박스, 멱등성, 대사, 수동 복구를 통제한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **분산 트랜잭션 선택 기준(Distributed Transaction Selection Criteria)**: 서비스 개수, 데이터 격리성 요구 및 보상 가능 여부에 기반한 선정 체계.

</details>

- 짧은 강한 원자성은 **2PC**, 보상 가능한 장기 흐름은 **Saga** 선택

#### 한줄 요약

- 보상 가능성과 중간 상태 허용 여부를 함께 평가하는 것이 핵심이다.
