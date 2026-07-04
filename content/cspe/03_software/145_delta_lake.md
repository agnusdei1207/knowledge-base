---
title: "Delta Lake (Delta Lake)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 145
---

# 📖 【암기용】 개념 완전 이해

> 목적: Delta Lake를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Delta Lake는 객체 스토리지 위 Parquet 데이터 파일에 **`_delta_log`라는 트랜잭션 로그**를 더해 **ACID**, time travel, schema evolution을 제공하는 오픈 테이블 포맷이다.
- **왜 필요한가**: 순수 Parquet 레이크는 "지금 어떤 파일이 유효한가"를 파일 목록(listing)에 의존해 판단하므로 동시 쓰기·부분 실패·삭제 요구에 취약하다. Delta Lake는 이 판단을 `_delta_log`라는 단일 진실 소스(source of truth)로 옮긴다.
- **핵심 직관**: 서가의 책을 직접 바꿔치기하지 않고, "몇 번 서가에 어떤 책을 추가/제거했다"는 이력을 장부에 적어, 장부만 보면 현재 서가 상태를 정확히 알 수 있게 하는 방식이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| `_delta_log` | 테이블이 겪은 모든 변경(add/remove file)을 기록한 로그 디렉터리 — Delta Lake의 **정체성**인 트랜잭션 로그 | 창고 입출고를 한 줄씩 적는 장부 |
| Commit | 하나의 트랜잭션을 순번 있는 JSON 파일(`00000000000000000010.json` 등)로 기록하는 단위 | 장부의 한 페이지(거래 1건) |
| Action (add/remove) | 커밋 안에서 "이 파일을 추가/제거했다"를 나타내는 최소 기록 단위 | 장부 한 줄: "입고 A박스" / "출고 B박스" |
| Checkpoint | 로그가 길어지면 지금까지의 상태를 요약해 Parquet로 스냅샷 저장(기본 10커밋마다) | 매달 장부를 정리해 요약본을 만드는 것 |
| Snapshot | 특정 버전까지의 add/remove를 모두 적용한 "현재 유효 파일 목록" | 장부를 처음부터 다 읽어 계산한 현재 재고 |
| Optimistic Concurrency Control | 커밋 전에 충돌 여부만 확인하고, 충돌 시에만 재시도하는 동시성 제어 방식 | 일단 써보고, 남이 먼저 썼으면 그때 다시 쓰기 |
| MERGE INTO | 키 매칭 여부에 따라 UPDATE/INSERT/DELETE를 한 문장으로 처리 | 명부에서 기존 항목 수정, 신규 항목 추가를 동시에 처리 |
| Time Travel | `VERSION AS OF n` 또는 시각 지정으로 과거 snapshot을 조회 | 장부를 거슬러 올라가 특정 날짜의 재고 확인 |
| VACUUM | commit에서 remove된, 더 이상 참조되지 않는 물리 파일을 실제 삭제 | 장부에서 폐기 처리된 물건을 실제로 창고에서 치우기 |
| OPTIMIZE / Z-ORDER | 작은 파일을 큰 파일로 병합(compaction)하고, 자주 필터링하는 컬럼 기준으로 파일 내 데이터를 재정렬 | 흩어진 소포를 큰 상자로 재포장하고, 자주 찾는 물건순으로 정리 |

## 깊이 이해

### commit이 정합성을 만드는 방식 — 워크드 예제(충돌 시나리오)
- writer A, B가 동시에 버전 v10에서 시작. A가 파일 추가 커밋(v11)에 먼저 성공. B는 자신의 트랜잭션이 v10을 읽었는데 실제 최신이 v11임을 감지 → B의 변경이 A와 실제로 겹치는지(같은 파일을 건드렸는지) 검사한 뒤, 안 겹치면 자동 재시도로 v12 커밋, 겹치면 충돌 예외로 실패시킨다.
- 예: v11에서 `file_003.parquet`를 추가했고 B도 동일 파일을 remove하려 했다면 충돌 → 실패. B가 다른 파티션의 `file_099.parquet`를 추가하는 거라면 충돌 없이 v12로 성공한다.

### `_delta_log`를 실제로 읽어보며 이해하기
- 예: 테이블에 처음 100개 파일을 쓰면 `00000000000000000000.json`에 add action 100개가 기록된다. 이후 MERGE로 5개 파일을 remove, 5개를 add하면 다음 커밋 파일에 add 5 + remove 5가 기록된다. 현재 snapshot을 계산하려면 로그를 처음부터 재생(replay)해 "add된 것 − remove된 것"을 구해야 한다.
- 커밋이 1,000개 쌓이면 매번 처음부터 재생하는 게 느려지므로, 기본 10커밋마다 checkpoint(누적 상태를 Parquet로 요약)를 만들어 재생 범위를 최근 커밋 구간으로 줄인다.

### CDC MERGE와 time travel 워크드 예제
- 주문 CDC 이벤트 1일 50만 건이 들어올 때, `MERGE INTO orders USING cdc ON orders.id = cdc.id WHEN MATCHED AND cdc.op='D' THEN DELETE WHEN MATCHED THEN UPDATE SET * WHEN NOT MATCHED THEN INSERT *`로 upsert/delete를 한 번에 반영한다.
- 배포 후 집계 오류를 발견하면 `SELECT * FROM orders VERSION AS OF 119`로 문제 발생 직전 버전(예: v120이 오류 버전이면 v119)을 조회해 정상 값과 비교하고, 필요 시 `RESTORE TABLE orders TO VERSION AS OF 119`로 되돌린다.

### 파일 관리 — OPTIMIZE/VACUUM 수치 예제
- 스트리밍 적재가 5분마다 작은 파일(평균 8MB)을 만들면 하루 288개 파일이 쌓여 쿼리 시 파일 오픈 오버헤드가 커진다. OPTIMIZE를 야간에 실행하면 target size(예: 256MB)로 병합해 파일 수를 1/30 수준으로 줄일 수 있다.
- VACUUM은 기본 retention 168시간(7일) 이전에 remove된 파일만 실제 삭제한다. retention을 너무 짧게(예: 1시간) 잡으면, 아직 조회 중인 time travel 쿼리나 진행 중인 리더가 참조하는 파일이 삭제되어 조회 실패가 날 수 있다 — 그래서 최소 7일을 권장한다.

### 비유와 오해
- **비유**: 도서관 서가를 직접 뒤지지 않고 장부(로그)만 보고 "지금 몇 번 서가에 어떤 책이 있는지" 정확히 아는 시스템이다.
- **오해 1**: Delta Lake가 Databricks 전용 상용 기능이다 — 아니다. 오픈소스 스펙이며 Spark·Flink·Trino 등에서 커넥터로 읽고 쓸 수 있다(다만 기능 성숙도는 엔진마다 차이가 있다).
- **오해 2**: `_delta_log`만 있으면 파일 관리가 저절로 된다 — 아니다. OPTIMIZE·VACUUM을 주기적으로 실행하지 않으면 작은 파일과 로그가 계속 쌓여 조회 성능이 떨어진다.

## 연결 개념
- 데이터 레이크하우스: Delta Lake가 구현하는 상위 아키텍처 (144에서 상세)
- Apache Iceberg: manifest·snapshot metadata 중심의 대안 오픈 테이블 포맷 (146에서 상세)
- 메달리온 아키텍처: Delta 테이블을 Bronze/Silver/Gold로 계층화하는 패턴

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Delta Lake 답안은 Parquet 저장과 `_delta_log`의 관계, ACID commit, MERGE, vacuum 운영을 분리해 설명해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Delta Lake는 Parquet 데이터 파일과 transaction log로 레이크 테이블의 현재 snapshot을 정의하는 오픈 테이블 포맷이다.
> 2. **가치**: CDC upsert, time travel, schema evolution, batch/stream 통합 처리로 레이크하우스 정합성을 제공한다.
> 3. **판단 포인트**: Databricks/Spark 중심 생태계, MERGE 요구, vacuum·optimize 운영 능력을 기준으로 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Delta 구조 이해 | Parquet, `_delta_log`, ACID, snapshot | 단순 파일 포맷으로 설명 |
| 레이크하우스 기능 판단 | MERGE, time travel, schema enforcement | upsert와 삭제 처리 누락 |
| 운영 관리 역량 | OPTIMIZE, VACUUM, checkpoint, small file | 로그 보관과 복구 정책 미기재 |

> 요약: Delta Lake는 로그 기반 테이블 상태 관리와 운영 유지보수까지 포함해야 완성된 답안이 된다.

---

## Ⅰ. 개요 및 필요성

- 개요: Delta Lake는 레이크하우스용 테이블 포맷이다.
- 배경: 데이터 레이크의 Parquet 파일만으로는 ACID, 버전 조회, 스키마 통제 요구를 처리하기 어렵다.
- 필요성: transaction log로 CDC, 스트리밍, BI가 같은 테이블을 사용할 때 파일 단위 불일치를 줄인다.

---

## Ⅱ. 구조 및 구성요소

```text
Object Storage -> Parquet Data Files
              -> _delta_log -> Snapshot -> Spark / SQL / Streaming
                         +-> Checkpoint
                         +-> Vacuum / Optimize
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Parquet Files | 실제 데이터 저장 | columnar, partition |
| `_delta_log` | commit 이력과 파일 상태 기록 | JSON log, checkpoint |
| Snapshot | 특정 버전의 유효 파일 집합 | time travel 기준 |
| Maintenance | 파일·로그 정리 | OPTIMIZE, VACUUM |

> 요약: Delta Lake는 데이터 파일과 로그를 분리하고, 로그가 현재 테이블 snapshot을 결정한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
쓰기 요청 -> optimistic transaction -> log commit -> snapshot 갱신
-> reader snapshot 선택 -> Parquet 읽기 -> optimize / vacuum 관리
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | writer가 변경 파일 생성 | 임시 파일 완성 여부 |
| 2 | `_delta_log`에 commit 기록 | commit conflict 0건 |
| 3 | reader가 version 기준 snapshot 조회 | version consistency |
| 4 | 오래된 파일·작은 파일 정리 | target file 128~512MB |

> 요약: Delta Lake는 optimistic transaction으로 commit하고 reader는 버전별 snapshot을 읽어 일관된 결과를 얻는다.

---

## Ⅳ. 특징

| 구분 | 일반 Parquet 레이크 | Delta Lake | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 정합성 | 파일 나열 결과 의존 | ACID transaction log | partial write 노출 방지 |
| 변경 처리 | 재작성 중심 | MERGE/UPDATE/DELETE | CDC upsert 처리 |
| 복구 | 백업 파일 의존 | time travel version 조회 | retention 7~30일 |
| 운영 | 파일 증가 방치 가능 | OPTIMIZE, VACUUM 필요 | small file ratio 5% 이하 |

> 요약: Delta Lake는 레이크 파일에 트랜잭션 의미를 부여하지만 로그 보관과 파일 정리 운영이 필요하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | Delta Lake | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Hive Parquet 테이블 | `_delta_log` 기반 snapshot | Spark/Databricks 중심 분석 |
| 비용/성능 | 전체 파일 스캔 | data skipping, optimize | 파티션·통계 컬럼 활용 |
| 운영/위험 | 파일 관리 단순 | log retention, vacuum 관리 | 복구 보관기간 명확화 |

> 요약: Delta Lake는 Spark 기반 MERGE와 time travel 요구가 큰 레이크하우스에 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 복구 불가 | VACUUM 보관기간 과소 | retention 7일 이상, 백업 정책 | time travel 성공률 |
| 쿼리 지연 | 작은 파일·파티션 과다 | OPTIMIZE, Z-ORDER | p95 query, file count |
| 스키마 충돌 | producer 컬럼 변경 | schema enforcement, 승인 절차 | schema failure rate |

> 요약: Delta 운영은 VACUUM, 작은 파일, 스키마 변경을 배포 절차로 통제해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 커밋 | commit failure 0.1% 이하 | transaction log audit |
| 파일 | 평균 파일 128~512MB | table detail, storage scan |
| 복구 | time travel retention 7~30일 | version query test |

> 요약: Delta Lake 품질은 commit 성공률, 파일 크기 분포, time travel 보관기간으로 확인한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. CDC 테이블은 `MERGE INTO` 기준으로 PK upsert를 구현하고 `_delta_log` commit audit을 일 단위 점검
2. Silver/Gold 테이블은 OPTIMIZE와 Z-ORDER를 야간 실행해 평균 파일 256MB, p95 query 10초 이하 목표 설정
3. VACUUM retention 168시간 이상, schema enforcement, 배포 전 호환성 검사로 복구와 스키마 리스크 통제

**결론 (2줄):**
- 기술사 판단: Spark 중심 레이크하우스와 CDC MERGE가 필요하면 Delta Lake, 다중 엔진 개방성이 최우선이면 Iceberg 검토
- 향후 방향: Delta Lake는 오픈 테이블 포맷 경쟁 속에서 catalog 표준화와 다중 엔진 호환성 확대가 관건

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Delta Lake를 설명하시오" | `_delta_log`, snapshot, time travel 흐름 | Parquet 레이크 대비 차이 |
| 요구사항 명시형 | "Iceberg와 비교", "운영 방안", "설계하시오" | MERGE, OPTIMIZE, VACUUM 절차 | 엔진 호환성·복구·파일 관리 기준 |

> 요약: 설명형은 transaction log 구조, 비교형은 Iceberg/Hudi 대비 선택 조건 중심으로 목차를 전환한다.
