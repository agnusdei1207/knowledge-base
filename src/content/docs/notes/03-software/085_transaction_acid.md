---
sidebar:
  order: 85
  label: "085. 트랜잭션 ACID"
  badge:
    text: "기출 · 70%"
    variant: note
title: "트랜잭션 ACID (Transaction ACID)"
date: "2026-08-26T09:46:00+09:00"
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

- **트랜잭션(Transaction)**: 데이터베이스의 상태를 변화시키는 논리적 작업의 완전한 최소 단위.
- **ACID 4대 속성**: Atomicity(원자성), Consistency(일관성), Isolation(격리성), Durability(지속성).

</details>

- 정의/개념: 데이터베이스 트랜잭션의 무결성을 위해 **원자성(Undo), 일관성(제약조건), 격리성(MVCC/2PL), 지속성(WAL/Redo)** 을 규정한 4대 핵심 속성
- 배경/필요성: 동시 트랜잭션 충돌 및 장애 발생 시 나타나는 **데이터 불일치, 갱신 분실 및 커밋 데이터 유실 해결 불가**

#### 한줄 요약
- 원자성, 일관성, 격리성, 지속성의 4대 속성으로 다중 사용자 환경의 무결성을 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **All-or-Nothing**: 트랜잭션 내 연산들이 100% 모두 성공하여 반영(Commit)되거나, 실패 시 0%로 완전 취소(Rollback)되는 원칙.
- **WAL(Write-Ahead Logging)**: DB 데이터 블록을 디스크에 쓰기 전에 Redo 로그를 디스크에 먼저 기록하는 기법.

</details>

- 실패 시 변경 사항을 완전 롤백하는 **All-or-Nothing 원자적 수행(Undo Log)**
- 트랜잭션 전후의 무결성 제약조건을 항시 만족하는 **일관성(Consistency) 유지**
- **2PL 및 MVCC 기반의 동시성 제어(Isolation)** 와 **WAL 기반 영구 보존(Durability)**

#### 한줄 요약
- Undo 로그, 무결성 제약조건, MVCC 동시성 제어, WAL 로그가 결합되어 작동한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Undo Log vs Redo Log**: 롤백 및 MVCC 일관된 읽기를 위한 Undo Log와 크래시 발생 시 커밋 데이터 복구를 위한 Redo Log.

</details>

```text
[트랜잭션 ACID 4대 보장 메커니즘 체계]
|-- 1. Atomicity (원자성)   -> Undo Log 버퍼 (실패 시 변경 사항을 역순 롤백)
|-- 2. Consistency (일관성) -> DBMS 무결성 제약조건 (PK/FK, Check, Trigger, Cascade)
|-- 3. Isolation (격리성)   -> 동시성 제어 엔진 (2PL 락 잠금, MVCC 다중 버전 읽기)
`-- 4. Durability (지속성)  -> WAL 및 Redo Log (커밋 즉시 로그를 디스크에 fsync)
```

선의 의미: 계층 및 4대 ACID 속성과 DBMS 내부 구현 메커니즘 매핑 구조

| ACID 속성 | 핵심 정의 | DBMS 내부 구현 메커니즘 |
|:---|:---|:---|
| 원자성 (Atomicity) | 트랜잭션 연산 전체가 **완료되거나 전혀 실행되지 않아야 함 (All or Nothing)** | **Undo Log 기반 롤백**, Savepoint 지점 복원 |
| 일관성 (Consistency) | 트랜잭션 전후에 **데이터베이스 무결성 제약조건이 항상 유지됨** | **기본키, 외래키, Check 제약조건**, 트리거 강제 |
| 격리성 (Isolation) | 동시 실행 중인 타 트랜잭션이 **현재 작업 중간 상태를 침범하지 못함** | **2PL (2단계 락킹), MVCC (다중 버전 제어)** |
| 지속성 (Durability) | 커밋 완료된 결과는 **시스템 장애나 전원 차단에도 영구 보존됨** | **WAL (Write-Ahead Log), Redo Log, Checkpoint** |

#### 한줄 요약
- Undo 로그(원자성), 제약조건(일관성), MVCC/2PL(격리성), WAL/Redo(지속성)가 유기적으로 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **트랜잭션 5대 상태**: Active(활동) $\to$ Partially Committed(부분 완료) $\to$ Committed(완료) 또는 Failed $\to$ Aborted(철회).

</details>

```text
트랜잭션 시작 (BEGIN TRANSACTION)
        │
   [Active] DML 실행 및 메모리 버퍼와 Undo/Redo 로그에 변경 이력 기록
        │
   [Partially Committed] 마지막 SQL 연산 완료 후 무결성 제약조건 및 외래키 검증
        │
   제약조건 위반이나 데드락 오류가 발생했는가?
   ┌────┴───────────────────────────┐
  아니오 (정상 완료)                 예 (오류 발생)
   │                                 │
[Committed]                     [Failed]
Redo Log 디스크 플러시 (fsync)    │
트랜잭션 영구 반영 확정           [Aborted]
                                 Undo Log 역순 실행으로 완전 롤백
```

#### 한줄 요약
- Active → Partially Committed → Committed(지속성) 또는 Aborted(원자적 롤백)로 전이된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ACID vs BASE**: 즉각적인 강한 일관성을 보장하는 RDBMS(ACID)와 최종 일관성과 가용성을 추구하는 분산 NoSQL(BASE).

</details>

| 비교 항목 | ACID (관계형 DBMS: Oracle, MySQL) | BASE (분산 NoSQL: Cassandra, DynamoDB) |
|:---|:---|:---|
| 핵심 철학 | **Strict Consistency (강한 일관성 최우선)**| **Availability (가용성 및 분산 확장성 최우선)** |
| 속성 구성 | **원자성, 일관성, 격리성, 지속성** | **기본 가용(BA), 유연한 상태(S), 최종 일관성(E)** |
| 동시성 제어 | 2PL 락킹 및 비관적/낙관적 락, MVCC | 분산 타임스탬프, 벡터 클락, 최종 쓰기 승리(LWW) |
| 주 적용 도메인 | **은행 계좌 이체, 결제, 주식 주문, 원장 관리** | **SNS 피드, 스트리밍 로그, 장바구니, IoT 데이터** |

#### 한줄 요약
- 금융 결제 등 엄격한 정합성에는 ACID, 글로벌 고가용성 분산 처리에는 BASE 모델을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Long-Running Transaction**: 트랜잭션 내에 외부 HTTP API 호출이나 무거운 배치를 넣어 DB 커넥션 풀을 장시간 고갈시키는 안티패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 장기 트랜잭션으로 인한 커넥션 풀 고갈 및 락 대기 폭증 | **외부 API 호출과 파일 I/O를 `@Transactional` 경계 밖으로 분리** | 트랜잭션 점유 시간 밀리초 단위 단축 |
| MSA 환경에서 단일 ACID 트랜잭션 적용 불가 | **Saga Pattern(오케스트레이션) 및 보상 트랜잭션 적용** | 서비스 독립성 유지 및 최종 일관성 달성 |
| 동시 트랜잭션 충돌로 인한 데드락(Deadlock) 빈발 | **테이블 및 레코드 수정 순서 표준화 및 Lock Timeout(5초) 설정** | 교착 상태 사전 방지 및 즉각 예외 복구 |
| 대량 커밋 시 디스크 I/O 병목 발생 | **Group Commit(그룹 커밋) 기법을 통한 WAL 디스크 쓰기 최적화** | TPS(초당 트랜잭션 처리량) 5배 향상 |

#### 한줄 요약
- 트랜잭션 범위 최소화, Saga 패턴 분산 처리, 접근 순서 표준화, Group Commit으로 최적화한다.

## Ⅶ. 결론

- 원장 무결성은 **ACID 트랜잭션**, 분산 환경은 **Saga** 선택

#### 한줄 요약
- 트랜잭션 ACID는 다중 동시성 환경과 장애 상황에서도 데이터베이스의 무결성과 영속성을 보장하는 핵심 공학 규약이다.