---
sidebar:
  order: 85
  label: "085. 트랜잭션 ACID (Transaction ACID)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "트랜잭션 ACID (Transaction ACID)"
date: "2026-08-13T18:44:00+09:00"
tags:
  - "notes-software"
weight: 85
extra:
  question_no: "085"
  source_status: "기출"
  source_history: "120회, 129회, 131회"
  priority: 70
  priority_note: "120•129•131회 반복, ACID 트랜잭션 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Transaction (트랜잭션)**: 데이터베이스의 상태를 변화시키는 논리적 작업 단위(Logical Unit of Work, LUW).
- **ACID Property (ACID 특성)**: 트랜잭션의 정합성과 무결성을 완벽히 보장하기 위한 4가지 대원칙 (Atomicity, Consistency, Isolation, Durability).
- **All-or-Nothing Rule**: 원자성(Atomicity)의 핵심 사상으로, 트랜잭션 내 모든 연산이 100% 반영되거나(Commit) 전혀 반영되지 않는(Rollback) 이분법적 실행 보장.

- **트랜잭션 ACID(Atomicity, Consistency, Isolation, Durability)**: 원자성(All or Nothing), 일관성(Invariants 보존), 격리성(동시성 제어), 지속성(WAL 영속화)의 4대 필수 데이터 무결성 보장 원칙.
</details>

- 정의/개념: 데이터베이스 관리 시스템(DBMS)이 복수의 데이터 연산 집합을 하나의 논리적 단위로 처리하며 무결성을 보장하기 위해 준수해야 하는 4대 근본 속성인 **ACID (Atomicity, Consistency, Isolation, Durability)**
- 배경/필요성: 부분 실패•동시 변경•장애는 **불변식 훼손•결과 유실** 유발

#### 한줄 요약

- 원자성•일관성•격리성•지속성으로 트랜잭션 신뢰성을 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Atomicity (원자성)**: 트랜잭션 내 연산들이 모두 수행(All)되거나 전혀 수행되지 않음(Nothing)을 보장하는 특성.
- **Consistency (일관성)**: 트랜잭션 수행 전과 수행 후 데이터베이스가 무결성 제약조건(Integrity Constraint)을 완벽히 준수하는 상태.
- **Isolation (격리성/고립성)**: 동시에 실행되는 여러 트랜잭션들이 서로 간섭하지 못하도록 통제하여, 마치 단일 트랜잭션이 순차 수행(Serial)되는 듯한 효과 제공.
- **Durability (지속성/영속성)**: 성공적으로 완료(Commit)된 트랜잭션 결과는 향후 시스템 정전이나 장애가 발생해도 데이터베이스에 영구적으로 보존됨.

</details>

- **All-or-Nothing** 원자적 수행 (**Atomicity**)
- DB 무결성 규칙(Integrity Constraints)의 항시 준수 (**Consistency**)
- **Concurrency Control & Lock / MVCC** 기반 동시 간섭 차단 (**Isolation**) 및 **WAL (Write-Ahead Logging)** 영구 보존 (**Durability**)

#### 한줄 요약

- 원자성(Undo Log/Rollback), 일관성(DB Constraints), 격리성(2PL/MVCC), 지속성(WAL/Redo Log)의 상호 결합 메커니즘을 정의한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Undo Log & Redo Log**: Undo Log는 트랜잭션 실패 시 이전 상태로 되돌리는(Rollback) 원자성 메커니즘, Redo Log는 시스템 다운 시 Commit된 데이터를 재현 복구하는 지속성 메커니즘.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                    Transaction ACID 4대 보장 메커니즘                    │
├─────────────────────┬───────────────────┬──────────────────────────────┤
│ ACID 속성 (Property)│ 보장 메커니즘     │ DBMS 엔진 기술 요소          │
├─────────────────────┼───────────────────┼──────────────────────────────┤
│ Atomicity (원자성)  │ Rollback / Undo   │ Undo Log, Savepoint          │
│ Consistency (일관성)│ Integrity Checks  │ Primary/Foreign Key, Trigger │
│ Isolation (격리성)  │ Concurrency Ctrl  │ 2PL Lock, MVCC, Isolation Lvl│
│ Durability (지속성) │ Recovery / Redo   │ WAL (Write-Ahead Log), Redo  │
└─────────────────────┴───────────────────┴──────────────────────────────┘
```

선의 의미: ACID 4가지 속성이 각각 DBMS 내부의 Undo Log, DB 제약조건, Lock/MVCC, WAL/Redo Log 엔진 요소에 대입되어 결합되는 아키텍처.

| ACID 4대 속성 | 핵심 개념 및 보장 내용 | DBMS 내부 구현 메커니즘 |
|:---|:---|:---|
| Atomicity (원자성) | 중간 단계 실패 시 전체 변경 원복(**All or Nothing**) | **Undo Log**를 통한 `ROLLBACK` 처리 |
| Consistency (일관성) | 송금 전후 통장 잔액 합계 등 비즈니스 불변식(Invariant) 유효 | **Primary Key, Foreign Key, Check 제약조건** 강제 |
| Isolation (격리성) | 동시 실행 중인 타 트랜잭션의 중간 미확정 연산 관찰 불가 | **2PL (Two-Phase Locking), MVCC (Multi-Version)** |
| Durability (지속성) | Commit 완료 후 디스크에 불변 보존 (장애 시 복구 가능) | **WAL (Write-Ahead Logging), Redo Log** 기록 |

#### 한줄 요약

- 트랜잭션 관리자와 로그•복구 장치의 제어 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Commit vs Abort**: Commit은 트랜잭션 연산의 성공적 완료 및 영구 저장, Abort는 트랜잭션 중단 및 Undo Log를 이용한 초기 상태 복원.

</details>

```text
             ┌───────────┐
             │ Active    │ (트랜잭션 시작 및 DML 수행)
             └─────┬─────┘
                   │ (마지막 DML 연산 완료)
                   ▼
             ┌───────────┐
             │ Partially │
             │ Committed │
             └───┬───┬───┘
   (Commit 통가) │   │ (에러 발생)
                 ▼   ▼
       ┌───────────┐ ┌───────────┐
       │ Committed │ │ Failed    │ ──► [Aborted] (Undo Log 롤백)
       └───────────┘ └───────────┘
```

### 동작 원리

1. Active: 트랜잭션 경계 안에서 읽기•변경 수행.
2. Partially Committed: 마지막 연산 후 확정 조건 검증.
3. Committed: 선행 로그와 커밋 기록으로 결과 지속성 확보.
4. Failed / Aborted: 실패 변경을 Undo해 이전 일관 상태 복구.

#### 한줄 요약

- 동시성 제어•불변식 검증•WAL 기록 후 커밋 또는 롤백한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **BASE (Basically Available, Soft-state, Eventual Consistency)**: 분산 가용성을 최우선하여 강한 격리를 포기하고, 시간이 지나면 결국 일관성(Eventual Consistency)에 도달하는 NoSQL 대전제.

</details>

| 비교 항목 | ACID (관계형 DBMS) | BASE (분산 NoSQL DBMS) |
|:---|:---|:---|
| 일관성 모델 | **트랜잭션 경계 내 불변식과 격리 수준 보장** | **가용성 중심의 최종 일관성 모델** |
| 동시성 및 가용성 | 격리성(Isolation) 보장으로 동시 처리량 제한 | **High Availability (고가용성) 및 분산 확장성** |
| 응용 도메인 | **금융 뱅킹, 결제, 계좌 이체, 주식 거래** | **SNS 피드, 스트리밍, 로그 수집, 장바구니** |
| 복구 메커니즘 | **WAL, Undo Log, Redo Log** | **CRDT, Read Repair, Hinted Handoff** |

#### 한줄 요약

- Strict 일관성/Financial Domain에는 ACID, High Availability & Scalability 분산 노드 환경에는 BASE(Basically Available, Soft-state, Eventual consistency)를 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Long-Running Transaction**: 트랜잭션 범위가 지나치게 길어 Lock을 오랫동안 점유하여 전체 데이터베이스 TPS를 추락시키는 안티패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 트랜잭션 경계가 너무 길어 커넥션 풀 및 Lock 고사 | **외부 API 호출 및 I/O 연산을 트랜잭션 경계 밖으로 분리**| DB 처리량(TPS) 향상 |
| 분산 마이크로서비스(MSA)에서 ACID 보장 불가 | **Saga Pattern (Choreography/Orchestration) & 보상 트랜잭션** | 최종 일관성 확보 |
| 데드락(Deadlock) 교착 상태 빈발 | **테이블 접근 순서 동일화 및 Lock Timeout 설정** | 교착 상태 즉시 해제 |

> 사례: **Spring `@Transactional` 선언적 트랜잭션 및 MySQL InnoDB WAL 튜닝**

#### 한줄 요약

- Minimum Invariant Scope, 격리 수준 Tuning, Idempotent Producer/Consumer 및 Saga Protocol(Compensating Transaction)을 적용한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **ACID 수립 기준(ACID Transaction Standards)**: 데이터 일관성 등급, RPO/RTO 복구 목표 및 마이크로서비스 분산 트랜잭션 요구에 의거한 체계.

</details>

- 단일 불변식은 **ACID 경계**, 분산 장기 흐름은 **Saga**•**보상** 적용

#### 한줄 요약

- 업무 불변식, 격리 수준, Recovery Point/Time Objective(RPO/RTO) 요구사항에 맞추어 Transaction Boundary를 정밀 획정한다.
