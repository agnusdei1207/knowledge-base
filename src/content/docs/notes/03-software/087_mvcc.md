---
sidebar:
  order: 87
  label: "087. MVCC 다중 버전 동시성 제어 (MVCC)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "MVCC 다중 버전 동시성 제어 (MVCC)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 87
extra:
  question_no: "087"
  source_status: "미출제"
  source_history: ""
  priority: 50
  priority_note: "MVCC는 동시 읽기•버전 정리 설계 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **MVCC (Multi-Version Concurrency Control, 다중 버전 동시성 제어)**: 데이터베이스에서 데이터를 수정(Update/Delete)할 때 기존 데이터를 직접 덮어쓰지 않고, Undo Log 등에 과거 버전(Historical Version)을 롤백 세그먼트로 보존하여, 읽기(Read)와 쓰기(Write) 작업이 서로를 블로킹하지 않도록 제어하는 고성능 동시성 제어 메커니즘.
- **Lock-Free Read ("Readers Never Block Writers, Writers Never Block Readers")**: 읽기 작업은 공유 락(S-Lock)을 걸지 않고 Undo Log 스냅샷을 읽고, 쓰기 작업은 비상적 락(X-Lock)을 걸어 쓰기를 수행하므로, 읽기와 쓰기가 상호 대기 없이 동시 구동되는 핵심 사상.
- **Undo Log / Rollback Segment**: MVCC 동작을 위해 과거 데이터 버전의 트랜잭션 ID 및 포인터를 보존해 두는 메모리/디스크 영역.

</details>

- 정의/개념: 데이터 수정 시 이전 버전 데이터를 Undo Log 공간에 보존하여 스냅샷 읽기(Snapshot Read)를 구현함으로써, "읽기 작업이 쓰기 작업을 블로킹하지 않고, 쓰기 작업이 읽기 작업을 블로킹하지 않는" 동시성 제어 기법인 **MVCC (Multi-Version Concurrency Control)**
- 배경/필요성: 락(2PL) 기반 동시성 제어의 극심한 블로킹(Blocking) 및 락 대기 오버헤드 해소, 대규모 트래픽 OLTP 환경에서 고성능 읽기/쓰기 동시 처리량(TPS) 확보 요구성

#### 한줄 요약

- 스냅샷별 가시 버전으로 읽기•쓰기 대기를 줄이는 MVCC가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Snapshot Read vs Current Read**: Snapshot Read는 락 없이 Undo Log 버전 스냅샷을 조회하는 일반 `SELECT`, Current Read는 최신 커밋 데이터 조회를 위해 S-Lock/X-Lock을 거는 `SELECT ... FOR UPDATE` 또는 `UPDATE` 구문.
- **Purge Thread / Vacuum**: 트랜잭션이 완료되어 더 이상 그 어떤 트랜잭션도 참조하지 않는 오래된 Undo Log 구버전(Garbage Version)을 주기적으로 메모리/디스크에서 수거 및 정돈하는 디비 백그라운드 프로세스.

</details>

- **Lock-Free Read (읽기/쓰기 무대기 동시성)** 구현
- **Snapshot Read (스냅샷 기반 시점 일관성 관찰)**
- 오래된 구버전 청소를 위한 **Purge / Vacuum 백그라운드 스레드 오버헤드**

#### 한줄 요약

- 스냅샷 읽기와 쓰기 충돌•버전 정리의 비용 절충이 핵심이다.

## Ⅲ. 구조 및 구성요소 (MySQL InnoDB MVCC 행 아키텍처)

<details><summary>핵심 용어</summary>

- **Hidden Metadata Columns (InnoDB 3대 숨은 열)**: DB_TRX_ID(해당 행을 가공한 트랜잭션 ID), DB_ROLL_PTR(Undo Log의 이전 버전을 가리키는 롤백 포인터), DB_ROW_ID(PK 부재 시 자동 생성되는 행 ID).

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   InnoDB Table Row (Data Page)                         │
├─────────┬──────────────┬──────────────────┬────────────────────────────┤
│ user_id │ name         │ DB_TRX_ID (102)  │ DB_ROLL_PTR ──────────────┐│
└─────────┴──────────────┴──────────────────┴────────────────────────────┼┘
                                                                         │ (포인터)
┌────────────────────────────────────────────────────────────────────────▼┐
│                   Undo Log Space (Rollback Segment)                    │
├─────────┬──────────────┬──────────────────┬────────────────────────────┤
│ user_id │ name         │ DB_TRX_ID (100)  │ DB_ROLL_PTR (Null)         │
│ (1001)  │ (홍길동)     │ (초기 Insert TRX)│                            │
└─────────┴──────────────┴──────────────────┴────────────────────────────┘
```

선의 의미: 데이터 페이지의 행에 저장된 `DB_ROLL_PTR`이 Undo Log 공간에 보존된 이전 버전 데이터(TRX ID: 100)를 연결고리로 가리키는 MVCC 체인 구조.

| 구성요소 | 핵심 역할 및 기능 | 주요 작동 방식 |
|:---|:---|:---|
| **DB_TRX_ID (6 Bytes)** | 해당 튜플을 마지막으로 `INSERT` 또는 `UPDATE`한 트랜잭션 식별자 | 가시성(Visibility) 판단의 기준 |
| **DB_ROLL_PTR (7 Bytes)**| Undo Log 레코드에 저장된 이전 버전으로 이동하는 **롤백 포인터** | 단방향 링크드 리스트(Chain) 형성 |
| **Undo Log (Rollback)** | 변경되기 전의 오리지널 레코드 데이터를 보관 | `ROLLBACK` 처리 및 MVCC 스냅샷 제공 |
| **Read View** | `SELECT` 시점에 활성화된 트랜잭션 목록(TRX_IDs)을 포함한 메모리 객체 | "이 버전을 읽을 수 있는가?" 판단 |

#### 한줄 요약

- 스냅샷•메타데이터•체인•충돌•정리 구조가 핵심이다.

## Ⅳ. 흐름도 (MVCC 가시성 평가 루틴)

<details><summary>핵심 용어</summary>

- **Read View Visibility Rule**: 1. 행의 `DB_TRX_ID` < `m_up_limit_id` (Read View 생성 시점 이전 커밋된 TRX) $\rightarrow$ **볼 수 있음(Visible)**. 2. `DB_TRX_ID` $\ge$ `m_low_limit_id` (Read View 생성 이후 TRX) $\rightarrow$ **볼 수 없음(Invisible, Undo 롤백 포인터 추적)**.

</details>

```text
[SELECT 쿼리 실행] ──► [Read View (m_up_limit_id, m_low_limit_id, TRX_IDs) 생성]
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│ 대상 Row의 DB_TRX_ID 확인                              │
│  ├── 1. DB_TRX_ID < m_up_limit_id ──► [현재 Data Page 읽기]│
│  └── 2. DB_TRX_ID >= m_low_limit_id ──► [DB_ROLL_PTR 추적] │
└──────────────────────────┬─────────────────────────────┘
                           ▼
            [Undo Log 체인 스캔 후 가시 버전 반환]
```

### 동작 원리

1. **Read View Creation**: `SELECT` 실행 시 Active 트랜잭션 목록 스냅샷 생성.
2. **TRX ID Check**: 읽으려는 행의 `DB_TRX_ID`를 확인.
3. **Visibility Evaluation**:
   - `DB_TRX_ID`가 Read View의 최소 트랜잭션 ID보다 작으면 이미 커밋된 안전한 데이터이므로 **즉시 렌더링**.
   - `DB_TRX_ID`가 현재 활성 트랜잭션이거나 미래 트랜잭션이면 **`DB_ROLL_PTR`을 타고 Undo Log를 과거로 역추적하여 이전 가시 버전 반환**.

#### 한줄 요약

- 버전 생성•가시성•충돌•안전 회수 흐름이 핵심이다.

## Ⅴ. 종류 및 비교 (Lock 기반 2PL 대 MVCC)

<details><summary>핵심 용어</summary>

- **S-Lock / X-Lock vs MVCC**: 2PL은 Read 시 S-Lock을 걸어 Write의 X-Lock과 상호 블로킹, MVCC는 Read 시 Lock을 걸지 않고 스냅샷을 읽어 최고의 동시 처리량 확보.

</details>

| 비교 항목 | Lock 기반 동시성 제어 (Strict 2PL) | MVCC 기반 동시성 제어 (Multi-Version) |
|:---|:---|:---|
| 읽기/쓰기 블로킹 | **읽기-쓰기, 쓰기-읽기 모두 블로킹 (동시성 낮음)**| **읽기와 쓰기가 서로를 블로킹하지 않음 (동시성 높음)**|
| 읽기 오버헤드 | **공유 락(S-Lock) 획득 및 해제 오버헤드** | **스냅샷 생성 및 Undo Log 역추적 오버헤드** |
| 디스크/메모리 부하 | 낮음 (현재 데이터만 디스크 보존) | **높음 (Undo Log 및 Purge 대기 구버전 점유)** |
| 적용 대표 엔진 | 과거 데이터베이스 스토리지 엔진 | **MySQL InnoDB, Oracle, PostgreSQL** |

#### 한줄 요약

- 읽기 대기는 다중 버전 동시성 제어, 충돌 순서는 잠금 중심 제어가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책 (Undo Log 관리)

<details><summary>핵심 용어</summary>

- **Undo Log Bloat (Undo 공간 팽창)**: 장시간 커밋되지 않는 트랜잭션(Long-running Transaction)이 존재할 경우 Purge 스레드가 구버전을 삭제하지 못해 Undo Log 용량이 폭증하고 조회가 느려지는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 장시간 트랜잭션으로 인한 **Undo Log Bloat (용량 폭증)** | **트랜잭션 내부 외부 API 통신 제거 및 `max_execution_time` 제한**| Undo 공간 폭증 방지 |
| PostgreSQL의 경우 Vacuum 미작동 시 테이블 팽창(Bloat) | **Autovacuum 파라미터 튜닝 및 pg_repack 수동 정돈** | 디스크 성능 보존 |
| MVCC 환경에서 `SELECT ... FOR UPDATE` 시 Locking Read로 변환 | **비관적 락(Locking Read) 대신 Optimistic Lock(버전 칼럼) 병행**| 블로킹 최소화 |

> 사례: **MySQL InnoDB `innodb_undo_tablespaces` 세그먼트 분리 & Purge 스레드 튜닝**

#### 한줄 요약

- 스냅샷 수명•팽창률•보존 지평선 통제가 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **MVCC 수립 기준(MVCC Concurrency Standards)**: 동시성 읽기 처리량(TPS) 요건, Undo Log 용량 쿼터 및 Purge 스레드 효율성에 의거한 체계.

</details>

- **MVCC 수립 기준**에 따라 대용량 트랜잭션 OLTP 시스템 구축 시 **MVCC 엔진 (InnoDB/PostgreSQL) + Undo Purge 튜닝** 필수 인가

#### 한줄 요약

- 읽기 중심은 MVCC, 충돌 순서는 동시성 제어 방식 선택 기준에 따라 판단한다.
