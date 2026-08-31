---
sidebar:
  order: 87
  label: "087. MVCC 다중 버전 동시성 제어"
  badge:
    text: "미출 · 50%"
    variant: note
title: "MVCC 다중 버전 동시성 제어 (Multi-Version Concurrency Control)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-software"
weight: 87
extra:
  question_no: "087"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "MVCC는 동시 읽기•버전 정리 설계 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **MVCC(Multi-Version Concurrency Control)**: 데이터를 갱신할 때 기존 데이터를 직접 덮어쓰지 않고 Undo Log에 과거 버전을 보존하여, 읽기와 쓰기가 상호 대기 없이 실행되도록 하는 고성능 동시성 메커니즘.
- **Lock-Free Read**: 읽기 트랜잭션이 공유 락(S-Lock)을 획득하지 않고 Undo 스냅샷을 조회하므로, 쓰기 트랜잭션(X-Lock)과 서로 블로킹되지 않는 원칙.

</details>

- 정의/개념: 데이터 수정 시 이전 버전을 Undo Log에 보존하여 **읽기와 쓰기가 상호 블로킹 없이 동시 실행되도록 지원하는 다중 버전 동시성 제어** 기법
- 배경/필요성: 전통적인 2단계 락킹(2PL) 방식에서 읽기(S-Lock)와 쓰기(X-Lock)가 상호 블로킹되어 대규모 트래픽 환경에서 동시 처리량(TPS)이 급락하고 대기 지연이 심화되는 한계를 극복하고, 데이터 갱신 시 변경 전 원본을 Undo Log 체인에 다중 버전으로 보존하여 읽기 트랜잭션이 락 없이 특정 시점의 일관된 스냅샷(Read View)을 조회하도록 지원함으로써 **"읽기는 쓰기를 막지 않고 쓰기는 읽기를 막지 않는" 초고속 동시성 제어를 실현**할 필요

#### 한줄 요약
- MVCC는 대기 비용을 저장 공간과 버전 정리 비용으로 바꾸는 거래이므로, 장기 트랜잭션이 옛 버전을 붙잡으면 없앴던 비용이 테이블 팽창과 체인 순회 지연이라는 형태로 되돌아온다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Snapshot Read vs Current Read**: 락 없이 Undo Log 스냅샷을 읽는 일반 `SELECT`와 행 락을 걸고 최신 데이터를 읽는 `SELECT ... FOR UPDATE` 및 DML.
- **Purge Thread / Vacuum**: 트랜잭션이 종료되어 더 이상 어떤 트랜잭션도 참조하지 않는 오래된 Undo Log 가비지 버전을 수거하는 백그라운드 프로세스.

</details>

- **"읽기는 쓰기를 막지 않고, 쓰기는 읽기를 막지 않는"** Lock-Free 동시성 제어
- Undo Log 체인 및 Read View를 통한 **스냅샷 기반 시점 일관성(Snapshot Isolation)** 보장
- 트랜잭션 종료 후 오래된 구버전을 자동 수거하는 **Purge(MySQL) / Vacuum(PostgreSQL) 엔진** 필수

#### 한줄 요약
- Lock-Free 스냅샷 읽기로 대규모 동시성을 보장하며 백그라운드 버전 정리를 수행한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **InnoDB 3대 숨은 컬럼**: `DB_TRX_ID`(트랜잭션 ID), `DB_ROLL_PTR`(이전 Undo 로그를 가리키는 롤백 포인터), `DB_ROW_ID`(행 식별자).

</details>

```text
[MVCC 버전 관리 구조]
|-- DB_TRX_ID
|-- DB_ROLL_PTR
|-- Undo Log 공간
`-- Read View
```

선의 의미: 현재 행과 과거 버전의 가시성을 판정하는 구성

| 구성요소 | 책임 |
|:---|:---|
| DB_TRX_ID | 행을 변경한 **트랜잭션 식별자** 기록 |
| DB_ROLL_PTR | **이전 버전**의 Undo 레코드 참조 |
| Undo Log 공간 | 변경 전 데이터를 보존해 **롤백·스냅샷** 제공 |
| Read View | 활성 트랜잭션 목록으로 **가시성** 판정 |

#### 한줄 요약
- 각 레코드가 자기 버전 이력으로 가는 포인터를 직접 들고 있어 가시성 판정이 중앙 잠금 테이블을 거치지 않고 레코드 단위로 끝나며, 그 대가로 버전 체인이 길어질수록 조회가 되짚어야 하는 단계가 늘어난다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Read View 가시성 공식**: `DB_TRX_ID < min_trx_id`이면 커밋 완료(보임), `DB_TRX_ID >= max_trx_id`이면 이후 시작(안 보임, Undo 체인 역추적).

</details>

```text
클라이언트 SELECT 질의 요청 (트랜잭션 TRX 103)
        │
   [Read View 생성] 활성 트랜잭션 목록(m_ids: [102, 105]) 캡처
        │
   [레코드 확인] 대상 행의 `DB_TRX_ID`가 105(활성 중)임을 확인
        │
   [가시성 판정] TRX 105는 현재 미커밋 활성 상태이므로 현재 행은 Invisible 판정
        │
   [Undo 체인 추적] `DB_ROLL_PTR`을 따라 Undo Log의 과거 버전(TRX 102)으로 이동
        │
   [과거 버전 판정] TRX 102도 활성 상태이므로 다시 이전 버전(TRX 100)으로 이동
        │
   TRX 100은 이미 커밋된 완료 버전이므로 최종 Visible 판정 후 데이터 반환
```

#### 한줄 요약
- 가시 버전 탐색은 대기 없이 진행되지만 체인 길이에 비례하는 CPU·I/O를 소비하므로, MVCC 환경의 지연은 잠금 경합이 아니라 정리되지 않고 쌓인 옛 버전의 양에서 발생한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Strict 2PL vs MVCC**: 읽기 시 S-Lock을 걸어 쓰기를 막는 2단계 락킹(2PL)과 락 없이 스냅샷을 읽는 MVCC.

</details>

| 비교 항목 | Lock 기반 동시성 제어 (Strict 2PL) | MVCC 기반 동시성 제어 (Multi-Version) |
|:---|:---|:---|
| 읽기/쓰기 상호작용 | **읽기와 쓰기가 S-Lock/X-Lock으로 상호 블로킹** | **스냅샷 읽기로 읽기와 쓰기가 상호 대기 없음** |
| 동시 조회 처리량 | 락 경합으로 인해 동시성 급감 | **대규모 동시 읽기 환경에서 초고속 처리량 유지** |
| 스토리지 부하 | 낮음 (현재 데이터 페이지만 유지) | **높음 (Undo Log 및 구버전 데이터 세그먼트 점유)** |
| 구버전 정리 필요성 | 없음 | **Purge 스레드 및 Vacuum 주기적 실행 필수** |

#### 한줄 요약
- 2PL은 락 기반 상호 대기 제어, MVCC는 스냅샷 기반의 락-프리 동시성 제어다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Undo Log Bloat**: 장기 트랜잭션이 커밋되지 않고 살아있어 Purge 스레드가 과거 Undo 로그를 삭제하지 못해 디스크가 가득 차는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 장시간 트랜잭션으로 인한 Undo 공간 폭증(**Undo Log Bloat**)| **트랜잭션 내 외부 API 호출 배제 및 `max_execution_time` 제한** | Undo 테이블스페이스 폭증 차단 |
| PostgreSQL의 미정리 구버전 누적으로 인한 Table Bloat | **Autovacuum 파라미터(threshold, scale_factor) 공격적 튜닝** | 데드 튜플 수거 및 디스크 I/O 성능 보존 |
| MVCC 환경에서 `SELECT ... FOR UPDATE` 시 락 경합 | **조회 시 무분별한 비관적 락을 지양하고 낙관적 락(`@Version`) 병행**| 락 블로킹 최소화 및 TPS 극대화 |
| Read View 과다 생성으로 인한 CPU 부하 | **읽기 전용 트랜잭션(`@Transactional(readOnly=true)`) 명시** | 플러시 오버헤드 제거 및 최적화 |

#### 한줄 요약
- 장기 트랜잭션 제거, Autovacuum 튜닝, 낙관적 락 병행, readOnly 최적화로 성능을 유지한다.

## Ⅶ. 결론

- 현대 대부분의 RDBMS(MySQL InnoDB, Oracle, PostgreSQL) 및 분산 DB 스토리지 엔진의 **핵심 락-프리(Lock-Free) 동시성 제어 아키텍처**로 확립되었으며, 실무 운영 시에는 **Undo 공간 폭증 및 테이블 팽창(Bloat)을 방지하기 위한 장기 트랜잭션 차단, Purge/Autovacuum 백그라운드 스레드 최적화, 읽기 전용 질의의 `readOnly=true` 명시를 통한 플러시 오버헤드 제거**를 결합하여 스토리지 건전성과 최대 동시 처리량을 유지

#### 한줄 요약
- MVCC는 락 없는 스냅샷 조회를 통해 읽기와 쓰기의 동시성을 극대화하는 현대 관계형 데이터베이스의 핵심 엔진 아키텍처다.
