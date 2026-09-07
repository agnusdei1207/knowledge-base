---
sidebar:
  order: 85
  label: "085. 트랜잭션 ACID"
  badge:
    text: "기출 · 70%"
    variant: note
title: "트랜잭션 ACID (Transaction ACID)"
date: "2026-09-07T10:05:00+09:00"
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
- 배경/필요성: 다중 동시 접근 시의 **갱신 분실(Lost Update) 및 시스템 장애 시의 부분 반영(Partial Commit)으로 인한 데이터 무결성 훼손 한계**

#### 한줄 요약
- ACID의 네 속성은 서로 독립적이지 않아 격리성을 높일수록 동시성이 깎이고 지속성을 엄격히 지킬수록 커밋 지연이 늘어나므로, 실무 설계는 넷을 모두 최대로 두는 것이 아니라 워크로드에 맞춰 어디를 완화할지 고르는 작업이 된다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **All-or-Nothing**: 트랜잭션 내 연산들이 100% 모두 성공하여 반영(Commit)되거나, 실패 시 0%로 완전 취소(Rollback)되는 원칙.
- **WAL(Write-Ahead Logging)**: DB 데이터 블록을 디스크에 쓰기 전에 Redo 로그를 디스크에 먼저 기록하는 기법.

</details>

- 실패 시 변경 사항을 완전 롤백하는 **All-or-Nothing 원자적 수행(Undo Log)**
- 트랜잭션 전후의 무결성 제약조건을 항시 만족하는 **일관성(Consistency) 유지**
- **2PL 및 MVCC 기반의 동시성 제어(Isolation)** 와 **WAL 기반 영구 보존(Durability)**

#### 한줄 요약
- 네 속성은 공짜로 성립하지 않고 각각 로그 기록·잠금 대기·검증 연산이라는 비용으로 사는 것이므로, 처리량이 급한 구간에서는 어떤 속성을 얼마나 양보할지가 곧 설계 결정이 된다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Undo Log vs Redo Log**: 롤백 및 MVCC 일관된 읽기를 위한 Undo Log와 크래시 발생 시 커밋 데이터 복구를 위한 Redo Log.

</details>

```text
[트랜잭션 ACID 체계]
  │
  ├─ [원자성: Atomicity] (All-or-Nothing·Undo Log 롤백)
  │
  ├─ [일관성: Consistency] (무결성 제약조건·도메인 불변식)
  │
  ├─ [격리성: Isolation] (MVCC / 2PL·동시성 제어)
  │
  └─ [지속성: Durability] (WAL·Redo Log 기반 영구 보존)
```
- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 원자성 | 실패한 전체 연산을 **Undo Log**로 롤백 |
| 일관성 | 전후 상태의 **무결성 제약조건** 유지 |
| 격리성 | **2PL·MVCC**로 중간 상태 접근 차단 |
| 지속성 | **WAL·Redo Log**로 커밋 결과 영구 보존 |

#### 한줄 요약
- 원자성과 지속성은 별개 장치가 아니라 변경 전 상태의 사본인 Undo와 변경 후 의도의 기록인 Redo라는 두 로그를 어느 시점에 읽느냐의 차이이므로, 로그 I/O 비용이 곧 ACID를 유지하는 대가다.

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
- 커밋 확정은 Redo 로그가 디스크에 안착한 시점에 성립하므로 커밋 지연은 트랜잭션 길이가 아니라 로그 플러시 횟수에 좌우되고, 반대로 Abort는 Undo를 역순으로 되감는 만큼 변경량에 비례하는 비용을 치른다.

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

- 금융 결제·주문 원장 등 미션 크리티컬 데이터 관리의 **가장 근본적이고 엄격한 데이터 정합성 보장 표준**으로 확립되었으며, 실무 시스템 아키텍처에서는 **트랜잭션 범위 최소화(외부 API 호출 분리), Group Commit 및 WAL 튜닝을 통한 I/O 병목 완화, 분산 마이크로서비스(MSA) 환경에서의 Saga 패턴 및 Outbox 패턴과의 상호 보완**을 결합하여 엄격한 무결성과 고성능 처리량을 양립

#### 한줄 요약
- 트랜잭션 ACID는 다중 동시성 환경과 장애 상황에서도 데이터베이스의 무결성과 영속성을 보장하는 핵심 공학 규약이다.
