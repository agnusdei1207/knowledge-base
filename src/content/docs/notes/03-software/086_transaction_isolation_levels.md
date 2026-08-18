---
sidebar:
  order: 86
  label: "086. 트랜잭션 격리 수준 4단계 (Transaction Isolation Levels)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "트랜잭션 격리 수준 4단계 (Transaction Isolation Levels)"
date: "2026-08-17T22:10:00+09:00"
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

<details><summary>용어 설명</summary>

- **트랜잭션 격리 수준 4단계**: Read Uncommitted(Level 0), Read Committed(Level 1), Repeatable Read(Level 2), Serializable(Level 3)로 구성된 ANSI/ISO SQL 표준 동시성 제어 등급.
- **3대 읽기 이상 현상(Read Anomalies)**: Dirty Read(미커밋 데이터 조회), Non-Repeatable Read(동일 행 재조회 시 값 변경), Phantom Read(범위 재조회 시 유령 행 출현).

</details>

- 정의/개념: 다중 트랜잭션 동시 실행 시 발생하는 3대 읽기 이상 현상을 제어하기 위해 **Read Uncommitted부터 Serializable까지 4단계로 직렬화 수준을 규정**한 동시성 제어 표준
- 배경/필요성: 동시성(Concurrency)과 격리성(Isolation)의 상충으로 인한 **Dirty Read, Phantom Read 등 데이터 부정합 및 Lock 경합 지연 위험** 직면

#### 한줄 요약

- 4단계 격리 수준과 MVCC/Lock 메커니즘을 통해 동시 처리 성능과 데이터 정합성 간 최적의 트레이드오프를 달성

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **MVCC(Multi-Version Concurrency Control)**: 읽기 작업이 락을 걸지 않고 Undo Log의 특정 시점 스냅샷(Read View)을 조회하여 동시성을 극대화하는 기법.
- **Next-Key Lock**: MySQL InnoDB에서 레코드 락과 갭 락을 결합하여 Repeatable Read 수준에서도 Phantom Read를 방지하는 잠금 기법.

</details>

- **ANSI/ISO SQL 92 표준 4단계** 격리 수준 계층화
- 격리 수준 상승에 따른 **Dirty Read, Non-Repeatable Read, Phantom Read 단계적 차단**
- 데이터베이스 엔진별 기본값 상이 (MySQL: **Repeatable Read**, Oracle/PostgreSQL: **Read Committed**)

#### 한줄 요약

- 4대 격리 수준별로 이상 현상을 단계적으로 차단하며 MVCC 스냅샷과 잠금을 통해 동시성을 제어

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Read View(가시성 스냅샷)**: 트랜잭션 시작 시점의 활성 트랜잭션 ID 목록을 기반으로 어떤 버전의 Undo 레코드를 읽을지 결정하는 가시성 판단 구조체.

</details>

```text
[ 트랜잭션 격리 수준 및 읽기 이상 현상 매트릭스 구조도 ]

 ┌────────────────────────────────────────────────────────────────────────┐
 │                 Transaction Isolation Levels & Read Anomalies          │
 ├─────────────────────┬──────────────┬──────────────────┬────────────────┤
 │ 격리 수준 (Level)   │ Dirty Read   │ Non-Repeatable   │ Phantom Read   │
 ├─────────────────────┼──────────────┼──────────────────┼────────────────┤
 │ 1. Read Uncommitted │ 발생 허용    │ 발생 허용        │ 발생 허용      │
 │ 2. Read Committed   │ 차단 (Safe)  │ 발생 허용        │ 발생 허용      │
 │ 3. Repeatable Read  │ 차단 (Safe)  │ 차단 (Safe)      │ 발생(InnoDB방지│
 │ 4. Serializable     │ 차단 (Safe)  │ 차단 (Safe)      │ 차단 (Safe)    │
 └─────────────────────┴──────────────┴──────────────────┴────────────────┘
```

선의 의미: 레벨이 올라갈수록 데이터 무결성은 향상되나 잠금 대기 및 동시 처리량(TPS)이 저하되는 트레이드오프 관계.

| 구성요소 | 책임 |
|:---|:---|
| Read Uncommitted (Level 0) | 커밋되지 않은 데이터 조회를 허용하며 **최대 동시성 제공** |
| Read Committed (Level 1) | 커밋 완료된 데이터만 조회하여 **Dirty Read 차단 (Undo Log 최신 커밋본 조회)** |
| Repeatable Read (Level 2) | 트랜잭션 시작 시점 스냅샷을 고정하여 **Non-Repeatable Read 차단** |
| Serializable (Level 3) | 모든 트랜잭션을 순차 직렬화하여 **Phantom Read를 포함한 모든 이상 현상 원천 차단** |

#### 한줄 요약

- Level 0부터 Level 3까지 단계별로 Dirty Read, Non-Repeatable Read, Phantom Read를 순차적으로 억제

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **MVCC 읽기 판정 절차**: 쿼리 실행 시 생성된 Read View와 대상 레코드의 DB_TRX_ID를 대조하여 Undo 체인을 역추적하는 과정.

</details>

```text
[ 격리 수준별 MVCC 및 락 판정 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. 트랜잭션 시작: TRX_ID 및 격리수준확인│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. Read View 생성: 가시성 스냅샷 고정  │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. 쿼리 실행: Undo 체인 역추적 조회    │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. 쓰기 충돌 검사: 행 락/Next-Key 검증  │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. 커밋 및 가시성 확정: Read View 소멸 │
 └────────────────────────────────────────┘
```

### 동작 원리

1. 트랜잭션 시작: 고유한 트랜잭션 ID(TRX_ID)를 할당받고 설정된 격리 수준을 확인.
2. Read View 생성: Repeatable Read는 첫 SELECT 시점에, Read Committed는 매 SELECT마다 Read View를 생성.
3. 쿼리 실행: 레코드의 TRX_ID가 Read View 범위보다 최신이면 Undo Log를 역추적하여 일관된 과거 버전을 조회.
4. 쓰기 충돌 검사: UPDATE/DELETE 수행 시 대상 행에 X-Lock을 획득하고 직렬화 충돌 여부를 검증.
5. 커밋 및 확정: 트랜잭션 커밋 완료 후 Read View를 해제하고 변경 사항을 영속화.

#### 한줄 요약

- 트랜잭션 시작 $\to$ Read View 생성 $\to$ Undo 역추적 조회 $\to$ 잠금 검증 $\to$ 커밋 확정의 5단계 흐름

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **2PL vs MVCC**: 읽기와 쓰기가 상호 블로킹되는 비관적 2단계 잠금(2PL)과 읽기가 쓰기를 블로킹하지 않는 다중 버전 동시성 제어(MVCC).

</details>

| 구분 | Lock 기반 동시성 제어 (2PL) | MVCC 기반 동시성 제어 (Undo Log) |
|:---|:---|:---|
| **적용 기준** | 데이터 충돌이 극심하여 완벽한 직렬화가 요구될 때 | 읽기 비중이 높고 대규모 동시 조회가 요구되는 웹 서비스 |
| **핵심 특징** | **공유락(S-Lock)과 배타락(X-Lock)으로 상호 대기 제어** | **스냅샷 조회를 통해 읽기와 쓰기가 상호 블로킹되지 않음** |
| **한계** | 읽기/쓰기 동시 실행 시 잠금 대기 및 데드락 빈발 | 장기 트랜잭션 시 Undo 영역 비대화 및 스냅샷 오버헤드 |

#### 한줄 요약

- 2PL은 잠금 기반으로 엄격하게 직렬화하며, MVCC는 스냅샷 기반으로 읽기 성능과 동시성을 극대화

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Write Skew(쓰기 왜곡)**: Repeatable Read 수준에서 두 트랜잭션이 각각 서로 다른 행을 검사 후 갱신할 때 전체 시스템 불변식이 파괴되는 이상 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Serializable 설정 시 극심한 락 경합 및 TPS 폭락 | **Read Committed 기본 채택 + 애플리케이션 Optimistic Lock(`@Version`) 결합** | 고성능 동시 처리와 갱신 분실 방지 동시 달성 |
| Repeatable Read에서 `SELECT.. FOR UPDATE` 누락 시 쓰기 왜곡 | **비즈니스 불변식 검증 쿼리에 명시적 비관적 잠금(Pessimistic Lock) 적용** | 데이터 정합성 보장 및 갭 락 활성화 |
| 장기 트랜잭션 방치로 인한 Undo 테이블스페이스 폭증 | **트랜잭션 내부 외부 API 통신 제거 및 짧은 트랜잭션 경계 유지** | Undo 영역 팽창 방지 및 DB 성능 보존 |

#### 한줄 요약

- Read Committed + 낙관적 락 조합, 비관적 락 선별 적용, 트랜잭션 경계 최소화로 최적의 튜닝을 달성

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **격리 수준 설계 원칙(Isolation Design Principle)**: 비즈니스 도메인의 정합성 요구 수준과 시스템 처리량(TPS) 목표를 고려하여 최적의 격리 수준을 결정하는 공학적 원칙.

</details>

- **트랜잭션 격리 수준**은 무결성과 성능의 타협점을 찾는 핵심 아키텍처 결정 요소이며, 기본 Read Committed/Repeatable Read 수준에 낙관적/비관적 락을 적절히 결합하여 최적의 데이터베이스 성능을 도출해야 함

#### 한줄 요약

- 4대 격리 수준의 특성을 이해하고 MVCC와 락 기법을 조합하여 데이터 정합성과 동시 처리량을 최적화
