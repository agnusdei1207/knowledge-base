---
sidebar:
  order: 179
  label: "179. 분산 트랜잭션: Saga vs 2PC"
  badge:
    text: "미출 · 70%"
    variant: note
title: "분산 트랜잭션: Saga vs 2PC (Saga vs 2PC)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 179
extra:
  question_no: "179"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "보상 거래와 원자 확정의 비교 가치"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **2PC (Two-Phase Commit)**: 분산된 여러 DB가 모두 준비(Prepare)되었을 때 일제히 커밋(Commit)하여 전역 원자성(ACID)을 보장하는 블로킹 프로토콜.
- **Saga Pattern**: 긴 분산 트랜잭션을 여러 로컬 트랜잭션으로 분할하고, 중간 실패 시 완료된 트랜잭션을 역순으로 되돌리는 보상(Compensating) 트랜잭션을 실행하는 최종 일관성 패턴.

</details>

- 정의/개념: 분산 환경에서 전역 물리적 락으로 원자성을 보장하는 **2PC 프로토콜과 로컬 트랜잭션 및 보상 트랜잭션 연쇄로 최종 일관성을 달성하는 Saga 패턴 비교**
- 배경/필요성: 마이크로서비스 독자 DB 환경에서 **전역 물리적 락(Lock) 유지로 인한 성능 병목, 코디네이터 SPOF 장애 및 이종 DB 간 2PC 지원 불가**

#### 한줄 요약
- 강한 원자성과 짧은 거래는 2PC, 긴 비즈니스 흐름과 마이크로서비스는 Saga 패턴을 선택한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Compensating Transaction**: 이미 커밋된 로컬 트랜잭션의 물리적 변경을 비즈니스 관점에서 상쇄 취소(예: 결제 완료 $\to$ 결제 취소 API 호출)하는 트랜잭션.
- **Semantic Lock**: 물리적 DB 락 대신 비즈니스 레벨에서 상태를 `PENDING`으로 마킹하여 동시 수정을 논리적으로 통제하는 기법.

</details>

- 전역 블로킹 락과 만장일치 커밋을 통해 강력한 ACID 원자성을 보장하는 **2PC 프로토콜**
- 물리적 락 없이 비동기 이벤트 기반으로 고성능을 유지하는 **Saga 최종 일관성(BASE)**
- 격리성(Isolation) 부재를 보완하기 위한 **Semantic Lock 및 피벗(Pivot) 트랜잭션 설계**

#### 한줄 요약
- 2PC는 전역 잠금 기반의 즉각적 원자성, Saga는 보상 트랜잭션 기반의 비차단 최종 일관성을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **2PC vs Saga 구조 비교**: 2PC(XA Coordinator + DB Resource Managers), Saga(Saga Orchestrator + MSA Local DBs).

</details>

```text
[2PC 전역 커밋 구조 vs Saga 보상 트랜잭션 구조 비교]
|-- 1. Two-Phase Commit (2PC: 동기식 물리 잠금 구조)
|   `-- XA Coordinator (중앙 조정자: Phase 1 Prepare 투표 -> Phase 2 Commit 브로드캐스트)
|       |-- DB A (Order DB: Prepare 상태에서 물리 락 유지)
|       `-- DB B (Payment DB: Prepare 상태에서 물리 락 유지)
`-- 2. Saga Pattern (오케스트레이션 방식: 비동기 비차단 구조)
    `-- Saga Orchestrator (상태 머신: 단계별 로컬 트랜잭션 지시 및 실패 시 역순 보상 실행)
        |-- 1. Order Service -> Local Commit (상태: PENDING)
        |-- 2. Payment Service -> Local Commit (결제 완료)
        `-- 3. Inventory Service -> 재고 부족 실패 발생 시 -> [역순 보상 트랜잭션 실행]
            `-- 3-Comp. Payment Service -> [결제 취소 API 호출]
```

선의 의미: 계층 및 2PC의 중앙 잠금 동기 구조와 Saga의 오케스트레이터 기반 단계별 비차단 실행 및 역순 보상 구조

| 구성요소 | 2PC 기반 메커니즘 | Saga 기반 메커니즘 |
|:---|:---|:---|
| **트랜잭션 실행 주체**| **XA 트랜잭션 매니저 (미들웨어 계층)** | **각 MSA 애플리케이션 (비즈니스 코드 계층)** |
| **롤백 및 복구 방식**| **DB 엔진 차원의 물리적 원자적 ROLLBACK** | **애플리케이션 차원의 보상(취소) API 역순 호출**|
| **데이터베이스 잠금**| 트랜잭션 완료 시까지 **모든 참여 DB 물리 락 유지** | 물리 락 없이 **각 로컬 커밋 후 즉시 락 해제**|
| **일관성 보장 수준** | **강한 일관성 (Strong ACID Consistency)** | **최종 일관성 (Eventual Consistency: BASE)** |

#### 한줄 요약
- 2PC(미들웨어 물리 락/원자성)와 Saga(애플리케이션 보상/최종 일관성)가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Saga 오케스트레이션 5단계**: 로컬 트랜잭션 실행 $\to$ 다음 단계 커맨드 전달 $\to$ 중간 실패 감지 $\to$ 역순 보상 트랜잭션 실행 $\to$ 최종 취소 상태 반영.

</details>

```text
주문 프로세스 시작 (Saga Orchestrator)
        │
   1. [로컬 트랜잭션 실행] Order Service가 주문 데이터를 로컬 DB에 커밋 (상태: `PENDING`)
        │
   2. [다음 커맨드 전달] Orchestrator가 Payment Service에 결제 승인 요청 및 로컬 커밋 완료
        │
   3. [후속 단계 실패 감지] Inventory Service에서 재고 부족으로 트랜잭션 실패(Error) 발생
        │
   4. [역순 보상 트랜잭션 실행] Orchestrator가 Payment Service에 `결제 취소` 보상 API 호출
        │
   5. Order Service의 주문 상태를 `CANCELLED`로 변경하고 사용자에게 실패 통지 완료
```

#### 한줄 요약
- 로컬 실행 → 다음 커맨드 전달 → 실패 감지 → 역순 보상 실행 → 최종 취소 반영 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Choreography vs Orchestration**: 이벤트 브로커 기반 탈중앙 릴레이(Choreography)와 중앙 오케스트레이터 상태 머신(Orchestration).

</details>

| 비교 항목 | 코레오그래피 사가 (Choreography) | 오케스트레이션 사가 (Orchestration) |
|:---|:---|:---|
| 제어 방식 | **중앙 통제자 없음 (이벤트 발행/구독 릴레이)**| **중앙 Saga Orchestrator (상태 머신 전담 제어)**|
| 서비스 간 결합도 | **최저 (메시지 브로커를 통한 비동기 결합)** | 오케스트레이터에 대한 중간 수준 결합 |
| 전체 흐름 가시성 | 서비스 증가 시 전체 트랜잭션 흐름 파악 곤란 | **상태 머신을 통해 전체 진행 상황 즉시 파악** |
| 최적 적용 규모 | **2~4개 서비스의 단순한 비즈니스 트랜잭션** | **5개 이상의 복잡하고 조건 분기가 많은 트랜잭션**|

#### 한줄 요약
- 단순 릴레이는 코레오그래피, 복잡한 다단계 트랜잭션은 오케스트레이션 방식을 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Pivot Transaction**: Saga에서 성공 시 이후 단계가 반드시 성공하거나 수동 개입으로 완수되어야 하는 분수령 트랜잭션(예: 외부 금융망 송금).

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 네트워크 장애로 결제 취소 보상 API 호출 실패 | **지수 백오프 재시도 및 DLQ 격리 후 수동 개입 상태 관리** | 트랜잭션 미완료 유실 방지 |
| 보상 API 재전송으로 인한 이중 환불 발생 | **보상 트랜잭션에 고유 `tx_id` 기반 멱등성(Idempotency) 구현** | 중복 환불 사고 원천 차단 |
| Saga 진행 중 타 사용자가 미완료 중간 데이터 조회/수정 | **`Semantic Lock` (상태 컬럼 `PENDING` 마킹) 적용** | Dirty Read 동시성 오염 방지 |
| 외부 결제 등 보상 불가능한 트랜잭션 실패 | **외부 연동을 피벗(Pivot) 트랜잭션으로 배치하고 실패 방어** | 비즈니스 회복 불가 사고 차단 |

#### 한줄 요약
- 보상 재시도/DLQ, 멱등성 구현, Semantic Lock, 피벗 트랜잭션 배치로 운영한다.

## Ⅶ. 결론

- 마이크로서비스 아키텍처 환경에서 분산 데이터 정합성을 달성하기 위해 **동일 관리 범위의 초단기 원자 거래는 2PC로 제한하고, 장기 비즈니스 흐름과 이종 서비스 연계는 Orchestration 기반의 Saga 패턴을 표준 적용**하며 멱등성과 Semantic Lock을 결합하여 고성능 분산 시스템 완성

#### 한줄 요약
- 2PC와 Saga는 강한 원자성(ACID)과 비차단 최종 일관성(BASE)이라는 명확한 트레이드오프 관계를 가지며, 마이크로서비스 환경에서는 Saga 패턴이 사실상의 표준 분산 트랜잭션 기술이다.