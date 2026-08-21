---
sidebar:
  order: 85
  label: "085. 트랜잭션 ACID (Transaction ACID)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "트랜잭션 ACID (Transaction ACID)"
date: "2026-08-17T22:05:00+09:00"
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

- **트랜잭션 ACID**: 원자성(Atomicity: Undo 롤백), 일관성(Consistency: 제약조건 준수), 격리성(Isolation: 2PL/MVCC 간섭 차단), 지속성(Durability: WAL/Redo 영구 보존)의 4대 핵심 트랜잭션 속성.
- **데이터 불일치 및 영속성 훼손(Inconsistency & Data Loss)**: 동시 트랜잭션 충돌이나 시스템 장애로 인해 중간 연산이 잔존하거나 커밋된 데이터가 유실되는 위험.

</details>

- 정의/개념: 데이터베이스 트랜잭션의 신뢰성과 무결성을 보장하기 위해 **원자성(Undo), 일관성(제약조건), 격리성(MVCC/2PL), 지속성(WAL/Redo)** 을 규정한 4대 핵심 속성
- 배경/필요성: 동시 트랜잭션 실행 및 예기치 못한 시스템 충돌 시 발생하는 **데이터 불일치, 갱신 분실 및 커밋된 데이터 유실 위험** 직면

#### 한줄 요약

- 원자성, 일관성, 격리성, 지속성의 4대 속성을 통해 다중 사용자 환경에서 데이터베이스 무결성을 보장

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **All-or-Nothing(원자성 원칙)**: 트랜잭션 내의 모든 연산이 100% 성공적으로 반영(Commit)되거나, 실패 시 전혀 반영되지 않고 롤백(Rollback)되는 이분법적 실행 원칙.
- **WAL(Write-Ahead Logging)**: 데이터 변경 내용을 디스크의 데이터 파일에 쓰기 전에 로그 파일에 먼저 기록하여 장애 복구(Durability)를 보장하는 기법.

</details>

- 실패 시 변경 사항을 완전 롤백하는 **All-or-Nothing 원자적 수행(Undo Log)**
- 트랜잭션 전후의 무결성 제약조건을 항시 만족하는 **일관성(Consistency) 유지**
- **2PL 및 MVCC 기반의 동시성 제어(Isolation)** 와 **WAL 기반 영구 보존(Durability)** #### 한줄 요약

- Undo 로그, 무결성 제약조건, MVCC 동시성 제어, WAL 로그를 상호 결합하여 무결성을 달성

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Undo Log vs Redo Log**: 트랜잭션 롤백 및 MVCC 일관된 읽기를 위한 Undo Log와 시스템 장애 시 커밋된 데이터를 재현 복구하기 위한 Redo Log.

</details>

```text
[ 트랜잭션 ACID 4대 보장 메커니즘 아키텍처 ]

 ┌────────────────────────────────────────────────────────────────────────┐
 │                    Transaction ACID 4대 보장 메커니즘                   │
 ├─────────────────────┬───────────────────┬──────────────────────────────┤
 │ ACID 속성 (Property)│ 보장 메커니즘     │ DBMS 엔진 기술 요소          │
 ├─────────────────────┼───────────────────┼──────────────────────────────┤
 │ 1. Atomicity (원자성)│ Rollback / Undo   │ Undo Log, Savepoint          │
 │ 2. Consistency(일관성)│ Integrity Checks  │ Primary/Foreign Key, Check   │
 │ 3. Isolation (격리성)│ Concurrency Ctrl  │ 2PL Lock, MVCC, 격리 수준    │
 │ 4. Durability (지속성)│ Crash Recovery    │ WAL (Write-Ahead Log), Redo  │
 └─────────────────────┴───────────────────┴──────────────────────────────┘
```

선의 의미: ACID 4가지 속성이 각각 DBMS 내부의 Undo Log, 제약조건, Lock/MVCC, WAL/Redo 엔진에 대응되는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 원자성 (Atomicity) | 연산 중간 실패 시 **Undo Log를 참조하여 이전 상태로 완전 롤백(Rollback)** |
| 일관성 (Consistency) | 트랜잭션 실행 전후 **기본키, 외래키, Check 제약조건 및 불변식 강제 준수** |
| 격리성 (Isolation) | 동시 트랜잭션 간 간섭을 차단하기 위해 **2PL 및 MVCC 기반 동시성 제어** |
| 지속성 (Durability) | 커밋 완료된 데이터를 보호하기 위해 **WAL 및 Redo Log를 통한 영구 디스크 기록** |

#### 한줄 요약

- Undo 로그(원자성), 제약조건(일관성), MVCC/2PL(격리성), WAL/Redo(지속성)가 유기적으로 작동

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **트랜잭션 5대 상태(Transaction States)**: Active(활동), Partially Committed(부분 완료), Committed(완료), Failed(실패), Aborted(철회).

</details>

```text
[ 트랜잭션 상태 전이 및 ACID 처리 파이프라인 ]

              ┌───────────┐
              │ 1. Active │ (DML 실행 및 Undo/Redo 로그 버퍼 기록)
              └─────┬─────┘
                    │ (마지막 DML 연산 성공 완료)
                    ▼
              ┌────────────────────────┐
              │ 2. Partially Committed │ (무결성 제약조건 및 동시성 검증)
              └───────┬────────┬───────┘
      (Commit 성공)   │        │ (검증 실패 / 시스템 에러)
                      ▼        ▼
        ┌───────────────┐    ┌───────────┐
        │ 3. Committed  │    │ 4. Failed │
        │ (WAL 디스크플러시)│    └─────┬─────┘
        └───────────────┘          │ (Undo Log 롤백 수행)
                                   ▼
                             ┌────────────┐
                             │ 5. Aborted │ (초기 상태 복구)
                             └────────────┘
```

### 동작 원리

1. Active: 트랜잭션이 시작되어 DML 연산을 수행하며 메모리 버퍼와 Undo/Redo 로그에 변경 이력을 기록.
2. Partially Committed: 마지막 SQL 연산 완료 후 무결성 제약조건과 직렬화 가능성을 최종 검증.
3. Committed: WAL 원칙에 따라 Redo 로그를 디스크에 플러시(fsync)하여 트랜잭션 영속성을 확정.
4. Failed: 제약조건 위반 또는 런타임 에러 발생 시 트랜잭션이 실패 상태로 전이.
5. Aborted: Undo Log를 역순으로 실행하여 트랜잭션 시작 전의 일관된 상태로 완전 복원.

#### 한줄 요약

- Active $\to$ Partially Committed $\to$ Committed(지속성 확정) 또는 Aborted(원자적 롤백)로 전이

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ACID vs BASE**: 강한 일관성과 트랜잭션 무결성을 중시하는 관계형 DBMS(ACID)와 가용성과 수평 확장을 중시하는 분산 NoSQL(BASE).

</details>

| 구분 | ACID (관계형 DBMS) | BASE (분산 NoSQL DBMS) |
|:---|:---|:---|
| **적용 기준** | 금융 뱅킹, 계좌 이체, 결제, 재고 관리 | 대규모 SNS 피드, 로그 수집, 장바구니 |
| **핵심 특징** | **원자성 및 즉각적 강한 일관성(Strict Consistency)** | **기본 가용성(BA) 및 최종 일관성(Eventual Consistency)** |
| **한계** | 분산 노드 확장 시 성능 및 동시성 제약 (CAP 한계) | 즉각적인 데이터 정합성 보장 불가 및 보상 트랜잭션 필요 |

#### 한줄 요약

- 금융 결제 등 엄격한 정합성에는 ACID, 글로벌 분산 고가용성에는 BASE 모델을 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **장기 트랜잭션(Long-Running Transaction)**: 트랜잭션 범위에 외부 API 호출이나 긴 비즈니스 로직이 포함되어 Lock을 오래 점유하고 커넥션 풀을 고갈시키는 안티패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 장기 트랜잭션으로 인한 커넥션 풀 고갈 및 Lock 경합 | **외부 API 호출 및 대용량 조회를 `@Transactional` 경계 밖으로 분리** | 트랜잭션 점유 시간 최소화 및 TPS 향상 |
| 분산 마이크로서비스(MSA) 환경에서 2PC 분산 락 병목 | **Saga Pattern(코레오그래피/오케스트레이션) 및 보상 트랜잭션 적용** | 서비스 독립성 유지 및 최종 일관성 달성 |
| 동시 갱신 충돌로 인한 데드락(Deadlock) 빈발 | **테이블 및 레코드 접근 순서 표준화 및 Lock Timeout 설정** | 교착 상태 사전 방지 및 즉각적 예외 복구 |

#### 한줄 요약

- 트랜잭션 경계 최소화, MSA Saga 패턴 도입, 접근 순서 표준화로 고성능 트랜잭션을 구현

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **트랜잭션 격리 수준 튜닝(Isolation Level Tuning)**: 성능과 정합성의 균형을 위해 Read Committed, Repeatable Read 등 최적의 격리 수준을 선택하는 튜닝 활동.

</details>

- **트랜잭션 ACID** 기반 데이터베이스 엔지니어링의 핵심 근간이며, 최신 클라우드 및 분산 시스템에서는 단일 노드의 ACID 무결성과 분산 서비스 간 Saga 최종 일관성을 유기적으로 결합하여 아키텍처를 설계해야 함

#### 한줄 요약

- 4대 ACID 메커니즘을 통해 데이터 무결성을 절대 보장하고 분산 환경에서는 최적화된 일관성 모델을 적용
