---
sidebar:
  order: 86
  label: "086. 트랜잭션 격리 수준 4단계 (Transaction Isolation Levels)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "트랜잭션 격리 수준 4단계 (Transaction Isolation Levels)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 86
extra:
  question_no: "086"
  source_status: "기출"
  source_history: "120회, 138회"
  priority: 70
  priority_note: "120•138회 반복, 격리수준•이상현상 중요"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Transaction Isolation Level (트랜잭션 격리 수준)**: ANSI/ISO SQL 표준에서 정립한 4단계 수준(Read Uncommitted, Read Committed, Repeatable Read, Serializable)으로, 다중 트랜잭션이 동시 실행될 때 데이터 고립성(Isolation)과 동시성(Concurrency) 간의 트레이드오프를 통제하는 동시성 제어 단계.
- **Read Phenomenon / Anomalies (읽기 이상 현상)**: 동시 트랜잭션 수행 시 격리 수준이 낮음으로 인해 발생하는 3대 현상 (Dirty Read, Non-Repeatable Read, Phantom Read).
- **Concurrency vs Consistency Tradeoff**: 격리 수준을 높이면 데이터 일관성과 무결성은 완벽해지나 동시 처리량(TPS) 및 잠금 대기 오버헤드가 폭증하는 트레이드오프 관계.

</details>

- 정의/개념: 다중 사용자 환경에서 트랜잭션의 동시 처리 성능(TPS)과 데이터 정합성을 동시에 제어하기 위해 3대 읽기 이상 현상 방지 수준을 4단계로 규정한 표준 제어 체계인 **Transaction Isolation Level**
- 배경/필요성: 동시 트랜잭션 간의 부정확한 미확정 데이터 읽기로 인한 부정 결제/재고 오류 차단, 서비스 성격별 맞춤형 격리 수준 설정을 통한 DB 성능 최적화 요구성

#### 한줄 요약

- 동시 거래의 가시성과 허용 이상을 정하는 트랜잭션 격리 수준이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **4-Level Isolation Hierarchy**: Read Uncommitted (Level 0) $\rightarrow$ Read Committed (Level 1) $\rightarrow$ Repeatable Read (Level 2) $\rightarrow$ Serializable (Level 3).
- **MVCC & Lock-based Mechanism**: RDBMS 엔진(MySQL InnoDB, Oracle, PostgreSQL)마다 S-Lock/X-Lock 락 기반 방식 또는 MVCC(Undo Log 스냅샷) 방식을 혼용하여 구현.

</details>

- **ANSI/ISO SQL 92 표준 4단계** 격리 수준 제공
- 동시성 이상 현상 (**Dirty Read, Non-Repeatable Read, Phantom Read**) 단계별 차단
- 데이터베이스 엔진별 기본 값 상이 (MySQL: **Repeatable Read**, Oracle/PostgreSQL: **Read Committed**)

#### 한줄 요약

- 이상 방지와 대기•취소•재시도 비용 절충이 핵심이다.

## Ⅲ. 구조 및 구성요소 (4대 격리 수준 & 3대 읽기 이상 현상 매트릭스)

<details><summary>핵심 용어</summary>

- **Dirty Read**: 커밋되지 않은 타 트랜잭션의 변경 데이터를 읽는 현상.
- **Non-Repeatable Read**: 한 트랜잭션 내에서 동일한 쿼리를 두 번 실행할 때 중간에 타 트랜잭션이 `UPDATE`하여 읽기 결과 값이 달라지는 현상.
- **Phantom Read**: 한 트랜잭션 내에서 범위 쿼리를 두 번 실행할 때 중간에 타 트랜잭션이 `INSERT`하여 이전에 없던 유령(Phantom) 행이 나타나는 현상.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                 Transaction Isolation Levels & Read Anomalies           │
├─────────────────────┬──────────────┬──────────────────┬─────────────────┤
│ Isolation Level     │ Dirty Read   │ Non-Repeatable   │ Phantom Read    │
├─────────────────────┼──────────────┼──────────────────┼─────────────────┤
│ 1. Read Uncommitted │ 발생 허용    │ 발생 허용        │ 발생 허용       │
│ 2. Read Committed   │ 방지 (Safe)  │ 발생 허용        │ 발생 허용       │
│ 3. Repeatable Read  │ 방지 (Safe)  │ 방지 (Safe)      │ 발생 (MySQL방지)│
│ 4. Serializable     │ 방지 (Safe)  │ 방지 (Safe)      │ 방지 (Safe)     │
└─────────────────────┴──────────────┴──────────────────┴─────────────────┘
```

선의 의미: 격리 수준이 올라갈수록(Level 0 $\rightarrow$ Level 3) 3대 이상 현상이 순차적으로 차단되는 아키텍처 매트릭스.

| 격리 수준 (Isolation Level) | 방지되는 이상 현상 | 구현 원리 및 런타임 제어 메커니즘 |
|:---|:---|:---|
| **1. Read Uncommitted** | 이상 현상 방지 0% | 타 트랜잭션의 커밋 안 된 **Dirty Data** 조차 무제한 읽기 수용 |
| **2. Read Committed** | **Dirty Read 차단** | Undo Log에서 **커밋된 최신 스냅샷만 조회** (Oracle, PostgreSQL 기본) |
| **3. Repeatable Read** | **Non-Repeatable Read 차단**| **트랜잭션 시작 시점의 Read View 스냅샷 고정** (MySQL InnoDB 기본) |
| **4. Serializable** | **Phantom Read 완벽 차단** | 모든 읽기 연산에 **Shared Lock (S-Lock) 또는 Next-Key Lock** 강제 |

#### 한줄 요약

- 업무•가시성•동시성•충돌 처리 구조가 핵심이다.

## Ⅳ. 흐름도 (MVCC 기반 스냅샷 가시성 원리)

<details><summary>핵심 용어</summary>

- **Read View (스냅샷 가시성)**: Repeatable Read 등급에서 트랜잭션이 시작된 TRX ID 시점의 Undo Log 버전을 고정하여, 타 트랜잭션이 아무리 수정해도 동일 결과 보장.

</details>

```text
[Transaction A (TRX ID: 100) 시작]
       │
       ▼ (1. SELECT Name -> "홍길동")
┌────────────────────────────────────────────────────────┐
│ TRX B (TRX ID: 101) 이 Name을 "이순신"으로 UPDATE & Commit │
└──────────────────────────┬─────────────────────────────┘
                           ▼ (2. TRX A가 SELECT 다시 실행)
 [Read Committed: "이순신" 조회]  vs  [Repeatable Read: Undo 스냅샷 "홍길동" 조회]
```

### 동작 원리

1. **Read Committed**: `SELECT` 문을 실행하는 매 순간마다 새로운 Read View(스냅샷)를 업데이트하므로, 중간 커밋된 "이순신"으로 조회값이 변경됨.
2. **Repeatable Read**: 트랜잭션 A가 시작된 시점(TRX ID: 100)의 Read View를 고정하여, TRX B가 커밋하든 말든 Undo Log 상의 "홍길동" 스냅샷 지속 유지.

#### 한줄 요약

- 가시성•충돌 검사 기반 대기•커밋•취소 흐름이 핵심이다.

## Ⅴ. 종류 및 비교 (Lock-based vs MVCC-based)

<details><summary>핵심 용어</summary>

- **Locking vs MVCC**: Locking은 읽기에도 S-Lock을 걸어 쓰기(X-Lock)와 상호 블로킹(Blocking) 발생, MVCC는 읽기 작업이 락을 걸지 않고 Undo Log 버전을 읽어 "Readers never block Writers" 구현.

</details>

| 비교 항목 | Lock 기반 동시성 제어 (2PL) | MVCC 기반 동시성 제어 (Undo Log) |
|:---|:---|:---|
| 동시성 성능 | **낮음 (읽기와 쓰기가 상호 대기/블로킹 발생)**| **매우 높음 (읽기 작업 시 Lock을 안 검)** |
| 구현 방식 | 공유 락(S-Lock) 및 비상적 락(X-Lock) | **Undo Log 메타데이터 버전 관리** |
| 대표적 DBMS | 과거 RDBMS 기술 표준 | **MySQL InnoDB, PostgreSQL, Oracle** |
| 저장 공간 | 디스크 Lock Manager 테이블 점유 | **Undo Tablespace 메모리/디스크 오버헤드** |

#### 한줄 요약

- 허용 이상 감소와 대기•재시도 증가의 단계 비교가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Write Skew (쓰기 왜곡)**: Repeatable Read 수준에서 두 트랜잭션이 서로 다른 행을 각각 개별 조건 검사 후 수정할 때, 개별조건은 통과했으나 전체 비즈니스 불변식이 파괴되는 현상 (Serializable 필요).

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| MySQL InnoDB에서 Repeatable Read 사용 시 Phantom Read 발생 가능성 | **`SELECT ... FOR UPDATE` (Pessimistic Lock / Next-Key Lock) 적용** | 유령 읽기 차단 |
| Serializable 설정 시 데드락(Deadlock) 및 TPS 폭망 | **기본 Read Committed 사용 + 애플리케이션 Optimistic Lock (Version) 병행**| 고성능 정합성 달성 |
| Long-running 트랜잭션으로 인한 Undo Log 폭증 | **트랜잭션 내부 외부 API 통신 제거 및 빠르게 Commit 완료** | DB 성능 보존 |

> 사례: **결제 및 재고 시스템 내 Read Committed + Optimistic Locking (`@Version`) 조합**

#### 한줄 요약

- 제품 의미 검증과 원자 갱신•멱등성 기반 재시도가 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **격리 수준 수립 기준(Isolation Level Standards)**: 서비스 TPS 요구량, 읽기 이상 허용성 및 Optimistic vs Pessimistic Lock 선택성에 의거한 체계.

</details>

- **격리 수준 수립 기준**에 따라 고성능 OLTP 서비스 구축 시 **Read Committed + 애플리케이션 비관적/낙관적 락** 필수 수용

#### 한줄 요약

- 불변식•허용 이상•충돌 비용 기반 격리 수준 결정 기준이 핵심이다.
