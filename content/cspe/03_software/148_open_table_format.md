---
title: "오픈 테이블 포맷 비교 (Open Table Format)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 148
---

# 📖 【암기용】 개념 완전 이해

> 목적: 오픈 테이블 포맷을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 오픈 테이블 포맷은 객체 스토리지에 쌓인 Parquet 파일 위에 **ACID 트랜잭션**과 **스냅샷 기반 버전 관리**를 부여하는 **메타데이터 계층**이다 — 대표 구현체가 Delta Lake, Apache Iceberg, Apache Hudi다.
- **왜 필요한가**: Parquet 파일만 객체 스토리지에 쌓아 두면 "지금 이 순간 테이블을 구성하는 파일 목록이 무엇인가"를 아무도 보장하지 못한다. 여러 엔진이 동시에 쓰고 읽으면 중간에 깨진 상태를 읽거나, UPDATE/DELETE를 파티션 전체 재작성 없이 처리할 수 없다.
- **핵심 직관**: 창고에 물건(Parquet 파일)만 쌓아두는 게 아니라, "지금 유효한 재고가 정확히 무엇인지"를 기록하는 장부(메타데이터)를 별도로 두는 것이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 데이터 레이크하우스 | 오픈 테이블 포맷이 얹히는 상위 아키텍처 — 레이크의 저비용 저장 + 웨어하우스의 트랜잭션·스키마 관리 결합 | 창고(저장) 위에 회계 시스템(장부)을 얹은 구조 |
| ACID 트랜잭션 | 원자성·일관성·격리성·지속성을 보장하는 변경 처리 단위 | 은행 송금이 절반만 처리된 채 끊기지 않음 |
| 스냅샷(Snapshot) | 특정 시점에 테이블을 구성하는 파일 목록의 버전 | 특정 순간 찍은 재고 사진 |
| Transaction Log(`_delta_log`) | Delta Lake가 커밋을 순서대로 남기는 JSON 로그 디렉터리 | 은행 거래 내역 장부 |
| Manifest | Iceberg가 스냅샷에 속한 데이터 파일 목록·통계를 기록하는 메타데이터 파일 | 판본별 상세 목차 |
| Timeline | Hudi가 커밋들을 시간순 이력(instant)으로 관리하는 구조 | 사건 타임라인 카드 |
| 낙관적 동시성 제어(OCC) | 커밋 시점에만 충돌을 검사해 잠금 없이 동시 쓰기를 처리하는 방식 | 좌석 예약 시 마지막 확정 순간에만 중복 확인 |
| Copy-on-Write / Merge-on-Read | Hudi의 두 갱신 전략 — 즉시 재작성 vs 지연 병합 | 즉시 새 문서 인쇄 vs 정정지를 붙였다가 나중에 합본 |
| 파티션 진화(Partition Evolution) | 기존 데이터를 재작성하지 않고 파티션 전략을 바꾸는 기능(Iceberg 특화) | 물건은 그대로 두고 창고 구역 표지판만 새로 붙임 |
| Compaction / Vacuum | 작은 파일을 병합(compaction)하고 안 쓰는 옛 파일을 정리(vacuum)하는 유지보수 작업 | 잔돈을 큰 지폐로 바꾸고 폐기 서류를 파쇄 |

## 깊이 이해

### 왜 필요했나 — Hive 방식의 한계 (배경)
- 예전 Hive 테이블은 "파티션 디렉터리에 있는 파일 = 테이블 데이터"라는 규칙만 있었다. 문제는 객체 스토리지의 디렉터리 목록(LIST) 연산이 원자적이지 않다는 것 — 쓰기 도중에 목록을 조회하면 절반만 반영된 상태를 볼 수 있다.
- UPDATE/DELETE를 하려면 영향받는 파티션 파일 전체를 다시 써야 했고, 여러 엔진이 "지금 유효한 스냅샷"에 대한 공통 합의가 없어 같은 쿼리도 엔진마다 다른 결과를 낼 수 있었다. 이 문제를 풀기 위해 파일과 별도로 "무엇이 현재 테이블인가"를 명시하는 메타데이터 계층이 필요해졌다.

### Delta Lake — 트랜잭션 로그와 낙관적 동시성 제어
- `_delta_log/` 아래 `00000000000000000000.json`부터 커밋마다 번호가 1씩 증가하는 JSON 파일이 쌓인다. 각 JSON은 "이번 커밋에서 추가·삭제된 파일 목록"을 기록한 원자적 트랜잭션 기록이다.
- 커밋 10회마다 Parquet 체크포인트 파일을 만들어, 리더가 처음부터 모든 JSON을 재생하지 않고 최신 체크포인트 + 이후 JSON만 읽으면 현재 상태를 구성할 수 있게 한다.
- **동시 쓰기 예**: Writer A와 B가 동시에 버전 5를 커밋하려 하면, "파일이 이미 존재하면 실패"하는 원자적 put 연산을 이용해 먼저 쓴 쪽만 성공하고, 진 writer는 최신 상태를 다시 읽어 재시도한다(낙관적 동시성 제어).

### Iceberg — 3계층 메타데이터와 숨은 파티셔닝
- 구조가 3단계다: `metadata.json`(스키마·현재 스냅샷 포인터) → manifest list(스냅샷별 manifest 파일 목록, Avro) → manifest file(실제 데이터 파일 목록 + 파티션값·컬럼 min/max/null count 통계, Avro).
- **수치로 이해하는 pruning 효과**: 파일 10만 개짜리 테이블에서 특정 날짜로 필터링하면, manifest에 저장된 컬럼 min/max 통계만 보고 스캔이 불필요한 파일을 걸러내 실제로 여는 파일을 수백 개 수준으로 줄일 수 있다 — 파일을 직접 열지 않고 통계만으로 판단하는 것이 핵심이다.
- 숨은 파티셔닝(hidden partitioning): 파티션 컬럼을 `day(event_ts)`처럼 변환 함수로 정의하면, 사용자는 파티션 컬럼을 몰라도 `event_ts` 조건만 걸면 엔진이 알아서 올바른 파티션만 골라 읽는다. 스키마 진화도 컬럼명이 아니라 내부 필드 ID 기준이라 컬럼명을 바꿔도 안전하다.

### Hudi — Copy-on-Write와 Merge-on-Read
- `.hoodie/` 타임라인에 커밋(commit)·델타커밋(deltacommit)·컴팩션(compaction) 같은 instant가 요청(REQUESTED) → 진행(INFLIGHT) → 완료(COMPLETED) 상태로 순서대로 쌓인다.
- **CoW(Copy-on-Write)**: 갱신이 생기면 영향받는 파일을 즉시 새 버전으로 통째로 재작성한다. 읽기는 빠르지만 쓰기 비용이 크다.
- **MoR(Merge-on-Read)**: 갱신분을 별도의 델타 로그 파일에 append만 하고, 조회 시점 또는 백그라운드 컴팩션에서 원본과 병합한다.
- **수치 예**: 100GB 파티션에서 1%(1GB)만 업데이트됐다면, CoW는 파티션 전체 100GB를 재작성해야 하지만 MoR은 변경분 1GB만 로그에 append하면 되어 쓰기 시간을 수십 분에서 수 분 수준으로 줄일 수 있다. CDC로 초당 수천 건씩 upsert가 들어오는 파이프라인에 Hudi·MoR가 강한 이유다.

### 세 포맷을 어떻게 구분·선택하나 (판별원리)
- 디렉터리 구조만 봐도 구분된다 — `_delta_log/`가 있으면 Delta, `metadata/`에 Avro manifest가 있으면 Iceberg, `.hoodie/`가 있으면 Hudi다.
- 선택 기준: Spark 중심에 `MERGE INTO`와 time travel이 핵심이면 Delta, Spark·Trino·Flink를 섞어 쓰며 파티션 전략을 자주 바꾸면 Iceberg, 실시간 CDC upsert와 증분 조회(incremental query)가 핵심이면 Hudi다.

### 비유와 흔한 오해
- **비유**: 세 포맷 모두 같은 재질(Parquet)로 상품을 포장하지만 재고 장부를 적는 방식이 다르다 — Delta는 시간순 거래 장부, Iceberg는 판본별 상세 목차, Hudi는 바코드 이력 카드에 가깝다.
- **오해**: "세 포맷은 그냥 Parquet 저장 방식 비교"가 아니다. 메타데이터 구조, 동시성 제어 방식, 엔진 호환성, 유지보수(compaction·vacuum) 도구가 서로 다른 별개의 계층 설계다.

## 연결 개념
- 데이터 레이크하우스: 오픈 테이블 포맷이 적용되는 상위 아키텍처
- 메달리온 아키텍처: 오픈 테이블 포맷 위에서 Bronze/Silver/Gold 계층을 구현할 때 실제 저장 포맷으로 쓰임
- 데이터 카탈로그: 오픈 테이블 포맷의 스냅샷·스키마를 검색 가능하게 등록하는 상위 관리 계층

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 오픈 테이블 포맷 비교는 기능 나열이 아니라 업무 요구를 Delta, Iceberg, Hudi의 선택 기준으로 매핑해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 오픈 테이블 포맷은 레이크 파일에 ACID, snapshot, metadata, update/delete semantics를 부여하는 표준형 테이블 계층이다.
> 2. **가치**: 객체 스토리지 기반 레이크하우스에서 다중 엔진 분석과 변경 데이터 처리를 가능하게 한다.
> 3. **판단 포인트**: Delta는 Spark/MERGE, Iceberg는 다중 엔진/partition evolution, Hudi는 CDC upsert/incremental query에 강점이 있다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 레이크하우스 기술 비교 | Delta `_delta_log`, Iceberg manifest, Hudi timeline | 세 포맷을 모두 Parquet으로만 설명 |
| 선택 기준 제시 | 엔진 호환성, upsert, schema evolution, 운영 도구 | 특정 제품 우열로 단정 |
| 운영 리스크 판단 | compaction, vacuum, snapshot expire, orphan file | 유지보수 작업과 지표 누락 |

> 요약: 비교 문제는 기능명보다 업무 요구와 포맷 선택 축을 연결하는 답안이 필요하다.

---

## Ⅰ. 개요 및 필요성

- 개요: 오픈 테이블 포맷은 레이크하우스 테이블 관리 계층이다.
- 배경: 객체 스토리지의 Parquet/ORC 파일은 ACID, snapshot, update/delete, schema evolution을 자체 제공하지 않는다.
- 필요성: Delta Lake, Apache Iceberg, Apache Hudi를 비교해 엔진 호환성, 변경 처리, 거버넌스 기준으로 선택한다.

---

## Ⅱ. 구조 및 구성요소

```text
Object Storage -> Data Files -> Table Metadata Layer -> Catalog -> Engines
                            +-> Delta Log / Iceberg Manifest / Hudi Timeline
                            +-> Maintenance / Governance
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Data File | 실제 컬럼형 데이터 저장 | Parquet, ORC, Avro |
| Metadata Layer | 테이블 버전과 파일 상태 관리 | log, snapshot, timeline |
| Catalog | 테이블 위치와 권한 관리 | Glue, Hive, REST, Unity |
| Engine | 읽기·쓰기 처리 | Spark, Flink, Trino |

> 요약: 오픈 테이블 포맷은 데이터 파일과 메타데이터 계층을 분리해 엔진이 동일 테이블 상태를 보게 한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
쓰기 요청 -> 데이터 파일 생성 -> 메타데이터 commit -> catalog 갱신
-> reader snapshot 선택 -> pruning / scan -> maintenance 실행
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | writer가 신규·변경 파일 생성 | 파일 완성, checksum |
| 2 | 포맷별 메타데이터에 commit 기록 | atomic commit |
| 3 | reader가 snapshot 또는 timeline 조회 | query result consistency |
| 4 | compaction, vacuum, snapshot expire 수행 | metadata size, file count |

> 요약: 오픈 테이블 포맷은 파일 변경을 메타데이터 commit으로 감싸 reader에게 일관된 snapshot을 제공한다.

---

## Ⅳ. 특징

| 구분 | Delta Lake | Apache Iceberg | Apache Hudi |
|:---|:---|:---|:---|
| 메타데이터 | `_delta_log` transaction log | snapshot, manifest, metadata file | timeline, file group, index |
| 강점 | Spark MERGE, time travel | 다중 엔진, hidden partitioning | CDC upsert, incremental query |
| 운영 작업 | OPTIMIZE, VACUUM | expire snapshot, rewrite manifest | compaction, cleaning |
| 선택 기준 | Databricks/Spark 중심 | Trino/Flink/Spark 혼합 | 변경 데이터 파이프라인 중심 |

> 요약: Delta, Iceberg, Hudi는 모두 레이크하우스 포맷이지만 메타데이터 구조와 선택 기준이 다르다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 오픈 테이블 포맷 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Hive/파일 listing | ACID metadata layer | update/delete와 snapshot 필요 |
| 비용/성능 | 파일 스캔·파티션 의존 | pruning, statistics, compaction | 파일 수 100만 개 이상 |
| 운영/위험 | 저장 단순 | 포맷별 유지보수 필요 | 운영 자동화와 엔진 PoC 필수 |

> 요약: 오픈 테이블 포맷은 레이크하우스 필수 계층이지만 업무·엔진·운영 역량에 맞춰 선택해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 포맷 종속 | 특정 엔진·벤더 기능 의존 | 표준 API, export test | 교차 엔진 쿼리 성공률 |
| 메타데이터 팽창 | snapshot/log/timeline 누적 | retention, compaction 자동화 | metadata size, planning p95 |
| 결과 불일치 | 엔진별 커넥터 차이 | 회귀 쿼리, compatibility matrix | mismatch 0건 |

> 요약: 비교 선택 후에도 종속성, 메타데이터, 엔진 결과 차이를 운영 지표로 관리해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 호환성 | 주요 엔진 쿼리 성공률 99% 이상 | Spark/Trino/Flink regression |
| 성능 | planning p95 3초, query p95 10초 이하 | query profile |
| 유지보수 | small file ratio 5% 이하 | table maintenance report |

> 요약: 오픈 테이블 포맷 평가는 기능 목록보다 호환성, planning time, 유지보수 지표로 수행한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 요구사항을 CDC MERGE, 다중 엔진, incremental query, partition evolution으로 분류해 Delta/Iceberg/Hudi PoC 후보를 선정
2. 동일 1TB 샘플 데이터로 Spark, Trino, Flink 쿼리 결과·planning p95·write latency를 측정해 포맷별 지표 비교
3. 선택 포맷별 OPTIMIZE/VACUUM 또는 snapshot expire/compaction 작업을 CI 배치에 포함하고 월 1회 교차 엔진 회귀 테스트 수행

**결론 (2줄):**
- 기술사 판단: Spark MERGE 중심은 Delta, 다중 엔진 개방성은 Iceberg, CDC incremental pipeline은 Hudi를 우선 검토
- 향후 방향: 오픈 테이블 포맷은 REST Catalog와 거버넌스 계층 표준화로 레이크하우스 상호운용성을 확대

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "오픈 테이블 포맷을 설명하시오" | metadata commit, snapshot 조회 흐름 | Delta·Iceberg·Hudi 대표 특성 |
| 요구사항 명시형 | "비교하시오", "선택 기준", "도입 방안" | 업무 요구별 포맷 매핑 | 엔진 호환성·운영 지표·종속성 리스크 |

> 요약: 설명형은 공통 구조, 비교형은 포맷별 선택 기준과 검증 지표 중심으로 전환한다.
