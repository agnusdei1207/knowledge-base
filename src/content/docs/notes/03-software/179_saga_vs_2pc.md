---
sidebar:
  order: 179
  label: "179. 분산 트랜잭션: Saga vs 2PC"
  badge:
    text: "미출 · 70%"
    variant: note
title: "분산 트랜잭션: Saga vs 2PC (Saga vs 2PC)"
date: "2026-08-26T13:23:57+09:00"
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

- 정의/개념: **2PC의 전역 원자 커밋**과 **Saga의 로컬 커밋·보상** 비교
- 배경/필요성: 2PC는 커밋 결정까지 모든 참여 자원의 락을 붙들어 대기 시간이 곧 처리량 손실이 되고 코디네이터가 멈추면 락이 남으므로, 락 대신 단계별 로컬 커밋과 보상 트랜잭션으로 원자성을 대체하는 계층을 애플리케이션 쪽에 둘 필요

#### 한줄 요약
- 강한 원자성과 짧은 거래는 2PC, 긴 비즈니스 흐름과 마이크로서비스는 Saga 패턴을 선택한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Compensating Transaction**: 이미 커밋된 로컬 트랜잭션의 물리적 변경을 비즈니스 관점에서 상쇄 취소(예: 결제 완료 $\to$ 결제 취소 API 호출)하는 트랜잭션.
- **Semantic Lock**: 물리적 DB 락 대신 비즈니스 레벨에서 상태를 `PENDING`으로 마킹하여 동시 수정을 논리적으로 통제하는 기법.

</details>

- Prepare·Commit 투표로 전역 원자성을 조정하는 **2PC 프로토콜**
- 로컬 커밋과 보상 동작을 연결하는 **Saga 최종 일관성**
- 격리성(Isolation) 부재를 보완하기 위한 **Semantic Lock 및 피벗(Pivot) 트랜잭션 설계**

#### 한줄 요약
- 2PC는 전역 잠금 기반의 즉각적 원자성, Saga는 보상 트랜잭션 기반의 비차단 최종 일관성을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **2PC vs Saga 구조 비교**: 2PC(XA Coordinator + DB Resource Managers), Saga(Saga Orchestrator + MSA Local DBs).

</details>

```text
[분산 트랜잭션 제어 구조]
├── 2PC
│   ├── XA Coordinator
│   └── Resource Managers
└── Saga
    ├── Saga Orchestrator
    └── Local Transaction Services
```

선의 의미: 계층 및 2PC의 중앙 잠금 동기 구조와 Saga의 오케스트레이터 기반 단계별 비차단 실행 및 역순 보상 구조

| 구성요소 | 책임 |
|:---|:---|
| XA Coordinator | Prepare 투표와 전역 Commit·Abort 결정 |
| Resource Manager | 로컬 자원 준비와 결정 반영 |
| Saga Orchestrator | 단계 상태와 보상 순서 관리 |
| Local Transaction Service | 로컬 커밋과 **보상 동작** 제공 |

#### 한줄 요약
- 2PC는 원자성을 미들웨어의 락으로 사고 Saga는 같은 결과를 애플리케이션의 보상 로직으로 사므로, 정합성 책임이 인프라에 있는지 도메인 코드에 있는지가 갈린다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Saga 오케스트레이션**: 로컬 실행, 커맨드 전달, 실패 감지, 보상 실행.

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
   Order Service의 주문 상태를 `CANCELLED`로 변경하고 사용자에게 실패 통지 완료
```

동작 원리:

1. 로컬 트랜잭션 실행: 주문을 PENDING으로 커밋
2. 다음 커맨드 전달: 결제 서비스에 작업 요청
3. 후속 단계 실패 감지: 재고 실패 결과 수신
4. 역순 보상 트랜잭션 실행: 결제 취소 호출

#### 한줄 요약
- 실패 이후는 롤백이 아니라 역순 보상으로 되돌려야 하므로, 보상이 불가능한 단계를 흐름의 어디에 두느냐가 실패 시 감당할 비용의 상한을 정한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Choreography vs Orchestration**: 이벤트 브로커 기반 탈중앙 릴레이(Choreography)와 중앙 오케스트레이터 상태 머신(Orchestration).

</details>

| 비교 항목 | 코레오그래피 사가 (Choreography) | 오케스트레이션 사가 (Orchestration) |
|:---|:---|:---|
| 제어 방식 | **중앙 통제자 없음 (이벤트 발행/구독 릴레이)**| **중앙 Saga Orchestrator (상태 머신 전담 제어)**|
| 서비스 간 결합도 | 이벤트 계약과 흐름이 분산 | 오케스트레이터 계약에 결합 |
| 전체 흐름 가시성 | 서비스 증가 시 전체 트랜잭션 흐름 파악 곤란 | **상태 머신을 통해 전체 진행 상황 즉시 파악** |
| 적용 기준 | 단순하고 분산 가능한 이벤트 흐름 | 분기·보상 가시성이 필요한 흐름 |

#### 한줄 요약
- 단순 릴레이는 코레오그래피, 복잡한 다단계 트랜잭션은 오케스트레이션 방식을 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Pivot Transaction**: Saga에서 성공 시 이후 단계가 반드시 성공하거나 수동 개입으로 완수되어야 하는 분수령 트랜잭션(예: 외부 금융망 송금).

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 네트워크 장애로 결제 취소 보상 API 호출 실패 | **지수 백오프 재시도 및 DLQ 격리 후 수동 개입 상태 관리** | 트랜잭션 미완료 유실 방지 |
| 보상 재전송에 따른 이중 환불 | 고유 `tx_id` 기반 **멱등성** 구현 | 중복 보상의 부작용 제한 |
| Saga 진행 중 타 사용자가 미완료 중간 데이터 조회/수정 | **`Semantic Lock` (상태 컬럼 `PENDING` 마킹) 적용** | Dirty Read 동시성 오염 방지 |
| 외부 결제 등 보상 곤란 단계 실패 | **Pivot 트랜잭션** 위치와 수동 복구 설계 | 비가역 단계의 실패 경로 관리 |

#### 한줄 요약
- 네 대책은 전역 락을 버려 얻은 처리량의 대가로 생긴 중복 보상과 중간 상태 노출을 멱등성과 의미적 락으로 되사는 선택이다.

## Ⅶ. 결론

- 짧은 원자 커밋은 **2PC**, 장기 업무 보상은 **Saga** 선택

#### 한줄 요약
- Saga에는 멱등성·Semantic Lock·수동 복구 경로를 설계한다.
