---
sidebar:
  order: 88
  label: "088. 락 관리: 2단계 잠금 프로토콜 (Two-Phase Locking, 2PL)"
  badge:
    text: "미출제 • 30%"
    variant: note
title: "락 관리: 2단계 잠금 프로토콜 (Two-Phase Locking, 2PL)"
date: "2026-08-13T19:02:00+09:00"
tags:
  - "notes-software"
weight: 88
extra:
  question_no: "088"
  source_status: "미출제"
  source_history: ""
  priority: 30
  priority_note: "2PL은 직렬성•교착상태 절충의 기본 기법"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **2PL (Two-Phase Locking Protocol, 2단계 잠금 프로토콜)**: 트랜잭션의 잠금(Lock) 획득과 해제를 2개의 직교되는 단계(성장 단계: Growing Phase, 축소 단계: Shrinking Phase)로 분리하여, 트랜잭션의 충돌 직렬 가능성(Conflict Serializability)을 100% 보장하는 동시성 제어 프로토콜.
- **Growing Phase (확장/성장 단계)**: 트랜잭션이 필요한 새로운 Lock(S-Lock, X-Lock)을 획득만 할 수 있고, 보유한 Lock을 전혀 해제(Unlock)할 수 없는 단계.
- **Shrinking Phase (축소 단계)**: 트랜잭션이 보유한 Lock을 해제(Unlock)할 수만 있고, 새로운 Lock을 절대 획득할 수 없는 단계.

</details>

- 정의/개념: 트랜잭션의 락 획득 시점(Growing Phase)과 락 해제 시점(Shrinking Phase)을 2단계로 명확히 교차 차단하여 트랜잭션의 직렬 가능성(Serializability)을 보장하는 규약인 **2PL Protocol**
- 배경/필요성: 임의 잠금 획득•해제는 **비직렬 실행•연쇄 취소** 유발

#### 한줄 요약

- 잠금을 모으는 동안에는 풀지 않고 하나라도 푼 뒤에는 새 잠금을 받지 않는다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Lock Point**: 트랜잭션이 마지막 Lock을 획득하여 Growing Phase가 완료되고 Shrinking Phase로 넘어가기 바로 직전의 시점.
- **Cascading Rollback (연쇄 롤백)**: 기본 2PL에서 한 트랜잭션이 Unlock한 미커밋 데이터를 타 트랜잭션이 읽었을 때, 원본 트랜잭션 취소 시 타 트랜잭션까지 도미노처럼 연속 롤백되는 현상.

</details>

- **Conflict Serializability (충돌 직렬 가능성 보장)**
- 락 획득만 가능한 **Growing Phase** 대 락 해제만 가능한 **Shrinking Phase** 분리
- **Deadlock (교착 상태)** 발생 가능성 상존 및 **Cascading Rollback (연쇄 롤백)** 위험성

#### 한줄 요약

- 실행 결과의 순서는 맞추지만 서로 자물쇠를 쥔 채 기다리는 교착이 생길 수 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **S-Lock / X-Lock**: Shared Lock(읽기 전용 공유 락), Exclusive Lock(쓰기 전용 배타 락).

</details>

```text
 [트랜잭션 관리자] ─── [잠금 관리자]
         │                    │
 [교착 탐지기] ─────── [잠금 테이블]
```

선의 의미: Growing Phase 동안 락을 누적 획득하여 Lock Point를 찍은 뒤, Shrinking Phase를 통해 락을 해제하는 2단계 타이밍 차트 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 트랜잭션 관리자 | 트랜잭션 상태와 커밋•취소 제어 |
| 잠금 관리자 | S/X 잠금의 호환성•대기•해제 관리 |
| 잠금 테이블 | 자원별 보유자와 대기 큐 기록 |
| 교착 탐지기 | 대기 순환을 찾아 취소 대상 선정 |

#### 한줄 요약

- 잠금 요청과 대기 관계를 관리하고 교착 시 취소 대상을 고른다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Strict 2PL (엄격한 2PL)**: 연쇄 롤백(Cascading Rollback)을 방지하기 위해, 모든 X-Lock(배타 락)을 Shrinking Phase에 해제하지 않고 트랜잭션이 Commit/Rollback 될 때까지 유지하는 프로토콜.
- **Rigorous 2PL (강력한 2PL)**: 모든 S-Lock과 X-Lock을 포함한 모든 락을 Commit/Rollback 시점까지 전혀 해제하지 않는 완벽한 2PL 변형.

</details>

```text
[Basic 2PL]     : Growing ──► Lock Point ──► Shrinking (중간에 Unlock 시작) ──► Commit
[Strict 2PL]    : Growing ──► Lock Point ──► [X-Lock 은 Commit 시점까지 보존] ──► Commit
[Rigorous 2PL]  : Growing ──► Lock Point ──► [모든 S/X-Lock 을 Commit 시점까지 보존] ──► Commit
```

### 동작 원리

1. **Basic 2PL**: 락을 다 얻으면 Shrinking Phase 진입하여 하나씩 `Unlock`. (연쇄 롤백 위험 존재).
2. **Strict 2PL**: `UPDATE`한 X-Lock을 트랜잭션 종료 시(`Commit/Rollback`)까지 유지하여 타 트랜잭션의 Dirty Read 및 Cascading Rollback 원천 차단.
3. **Rigorous 2PL**: 모든 락(S-Lock + X-Lock)을 트랜잭션 종료 시까지 들고 있어 직렬화 완벽 보장.

#### 한줄 요약

- 물건을 담는 동안에는 빼지 않고 하나를 빼기 시작하면 새 물건을 담지 않는다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Cascading Rollback Avoidance**: Strict 2PL 및 Rigorous 2PL은 미커밋 데이터 유출을 막아 연쇄 롤백을 완전 방지(Avoids Cascading Aborts).

</details>

| 비교 항목 | Basic 2PL (기본 2PL) | Strict 2PL (엄격한 2PL) | Rigorous 2PL (강력한 2PL) |
|:---|:---|:---|:---|
| X-Lock 해제 시점 | Shrinking Phase 진입 후 조기 해제 | **트랜잭션 Commit / Rollback 시점** | **트랜잭션 Commit / Rollback 시점** |
| S-Lock 해제 시점 | Shrinking Phase 진입 후 조기 해제 | Shrinking Phase 진입 후 조기 해제 | **트랜잭션 Commit / Rollback 시점** |
| 직렬 가능성 (Serial) | **보장** | **보장** | **보장** |
| 연쇄 롤백 방지 | 미커밋 값 노출 시 발생 가능 | **쓰기 잠금 유지로 방지** | **모든 잠금 유지로 방지** |
| 실무 상용 DBMS 채택| 채택 안 함 | **대다수 상용 RDBMS 채택** | 일부 RDBMS 옵션 채택 |

#### 한줄 요약

- 기본 방식은 축소 단계에서 잠금을 풀고 엄격한 방식은 쓰기 잠금을 종료까지 유지한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Deadlock in 2PL**: 2PL 규약을 준수하다가 두 트랜잭션이 상대방이 보유한 락을 교차 대기(Circular Wait)하여 영원히 멈추는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 2PL 수행 중 교착 상태(**Deadlock**) 발생 | **Wait-for Graph 교착 순환 감지 및 Deadlock Timeout 해제** | 무한 대기 해제 |
| Basic 2PL의 연쇄 롤백(**Cascading Rollback**) | **실무 DBMS에서는 Strict 2PL (X-Lock Commit 시점 해제) 강제**| 연쇄 롤백 완전 차단 |
| 락 점유 기간 장기화로 인한 동시성 TPS 하락 | **2PL 대신 MVCC (Multi-Version Concurrency Control) 엔진 채택**| 동시성 TPS 극대화 |

> 사례: **MySQL InnoDB / Oracle DBMS 내 Strict 2PL 기반 락 매니저 운용**

#### 한줄 요약

- 모든 이체가 계좌 번호순으로 잠그면 반대 순서 대기로 생기는 교착을 줄일 수 있다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **2PL 수립 기준(2PL Protocol Standards)**: 직렬 가능성 요건, 연쇄 롤백 차단성 및 Strict 2PL 채택 여부에 의거한 체계.

</details>

- 연쇄 취소 방지는 **Strict 2PL**, 높은 읽기 동시성은 **MVCC** 병행

#### 한줄 요약

- 2단계 잠금 방식 선택 기준은 올바른 실행 순서와 교착•대기 비용을 함께 고려한다.
