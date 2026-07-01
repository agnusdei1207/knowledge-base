---
title: "Delta Lake (Delta Lake)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 304
---

# 📖 【암기용】 개념 완전 이해

> 목적: Delta Lake를 Parquet 파일에 트랜잭션 로그를 더해 데이터 레이크를 관리형 테이블처럼 다루게 하는 open table format으로 이해하게 만든다.

## 한눈에
- **개요**: Parquet 데이터와 `_delta_log`를 결합해 ACID, time travel, schema 관리를 제공하는 테이블 포맷
- **왜 필요한가**: 데이터 레이크는 파일 덮어쓰기와 동시 쓰기에서 정합성 문제가 생기며, 과거 버전 조회와 upsert 처리가 어렵다.
- **핵심 직관**: 폴더 안 파일만 보는 대신 모든 변경을 장부에 기록해 현재 테이블 상태를 계산하는 방식임.

## 깊이 이해
- **배경·문제의식**: 배치와 스트리밍 작업이 같은 경로에 파일을 쓰면 일부 파일만 보이거나 스키마가 섞여 분석 결과가 흔들릴 수 있다.
- **작동 원리**: Delta Lake는 JSON/Parquet transaction log에 add/remove file, schema, protocol 정보를 기록하고 optimistic concurrency control로 commit 충돌을 감지한다.
- **비유**: 은행 잔고를 현금 더미로 세는 대신 입출금 장부로 계산하면 어느 시점의 잔고도 재구성할 수 있다.
- **구체 예시**: CDC로 들어온 주문 변경을 `MERGE INTO`로 반영하고, 오류 적재가 발생하면 특정 table version으로 rollback하거나 time travel 쿼리를 수행한다.
- **흔한 오해·주의점**: Delta Lake는 Parquet를 대체하는 파일 포맷이 아니다. Parquet 파일 위에 transaction log와 table protocol을 추가하는 테이블 계층이다.

## 연결 개념
- Data Lakehouse — Delta Lake가 구현하는 대표 아키텍처
- Apache Iceberg — snapshot metadata 기반 대안 포맷
- Change Data Capture — MERGE와 Change Data Feed 적용 대상

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Delta Lake는 Spark 친화적 transaction log 기반 테이블 포맷이며, ACID와 time travel을 `_delta_log`로 설명해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Delta Lake는 Parquet 파일 집합을 transaction log로 관리해 데이터 레이크에 ACID 테이블 기능을 제공함.
> 2. **가치**: 동시 쓰기, schema enforcement, time travel, upsert/delete를 지원해 레이크하우스 테이블 정합성을 확보함.
> 3. **판단 포인트**: `_delta_log`, optimistic concurrency, MERGE, vacuum, Change Data Feed, engine 호환성을 확인해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 테이블 포맷 구조 이해 확인 | Parquet + transaction log | 단순 저장소로 설명 |
| ACID 동작 판단 확인 | atomic commit, optimistic concurrency | RDBMS 로그와 동일시 |
| lakehouse 적용 역량 확인 | MERGE, time travel, schema evolution | Spark 기능으로만 축소 |

> 요약: 이 문제는 Delta Lake의 `_delta_log`가 파일 레이크를 트랜잭션 테이블로 바꾸는 원리를 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 로그 기반 레이크 테이블
- 배경: Parquet 파일만으로는 동시 쓰기, 삭제, upsert, 과거 버전 조회를 일관되게 처리하기 어려움.
- 필요성: 배치·스트리밍·CDC가 같은 테이블을 갱신할 때 atomic commit과 schema 검증이 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
Parquet Data Files -> _delta_log -> Table Version / Snapshot
        +-> Schema / Protocol
        +-> Spark / Trino / Flink Reader -> Catalog / Governance
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Parquet Files | 실제 컬럼 데이터 저장 | 압축·컬럼 pruning |
| _delta_log | 테이블 변경 이력 기록 | JSON, checkpoint parquet |
| Transaction Protocol | commit 충돌 감지와 버전 관리 | optimistic concurrency |
| Table Operations | MERGE, UPDATE, DELETE, time travel | CDC·SCD 처리 |

> 요약: Delta Lake는 데이터 파일과 별도 transaction log를 결합해 현재 snapshot과 과거 버전을 계산한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
쓰기 요청 -> 대상 파일 계산 -> commit log 작성 시도
-> 충돌 검사 -> version 증가 -> reader가 최신 snapshot 조회
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 쓰기 작업이 add/remove file 목록 생성 | file action completeness |
| 2 | `_delta_log`에 atomic commit 시도 | version ordering |
| 3 | 충돌 발생 시 재시도 또는 실패 처리 | conflict detection |
| 4 | reader가 log와 checkpoint로 snapshot 구성 | snapshot consistency |

> 요약: Delta Lake는 파일 변경을 직접 현재 상태로 보지 않고 commit log를 기준으로 일관된 snapshot을 제공한다.

---

## Ⅳ. 특징

| 구분 | Plain Parquet | Delta Lake | 판단 기준 |
|:---|:---|:---|:---|
| 트랜잭션 | 파일 쓰기 단위 | table commit 단위 | 동시 writer 여부 |
| 변경 처리 | overwrite 중심 | MERGE/UPDATE/DELETE | CDC·SCD 필요성 |
| 이력 | 별도 백업 필요 | time travel, rollback | 감사 요구 |
| 유지보수 | 파일 관리 수동 | optimize, vacuum | 저장 비용·파일 수 |

> 요약: Delta Lake는 변경이 잦은 분석 테이블에서 plain Parquet의 정합성 한계를 transaction log로 보완한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 엔진 생태계 | Iceberg, Hudi | Delta Lake | Spark/Databricks 중심 여부 |
| 변경 패턴 | append-only | MERGE·delete 다수 | CDC 처리 빈도 |
| 상호운용 | format별 metadata | UniForm 등 호환 계층 | 다중 엔진 읽기 요구 |

> 요약: Spark 중심 레이크하우스와 MERGE 중심 워크로드는 Delta Lake가 적합하고, vendor-neutral catalog 요구는 Iceberg와 비교해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 로그 비대화 | commit 빈도 증가 | checkpoint, vacuum | log size, planning time |
| small file | 스트리밍 micro-batch | optimize, auto compaction | average file size |
| 호환성 차이 | 엔진별 Delta 기능 지원 차이 | protocol version 관리 | failed reader count |

> 요약: Delta Lake 운영 리스크는 로그 크기, 작은 파일, 엔진 호환성으로 관리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정합성 | failed/partial commit 0건 | transaction log audit |
| 조회 계획 | snapshot planning SLA 충족 | query engine metrics |
| 보존 정책 | vacuum retention 정책 준수 | table history 점검 |

> 요약: Delta Lake 성과는 ACID commit 성공률, snapshot 계획 시간, 이력 보존 정책 준수로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. bronze-silver-gold 테이블별로 schema enforcement, partition, optimize, vacuum 정책을 정의함.
2. CDC·SCD 처리는 `MERGE INTO`와 Change Data Feed를 사용하고, critical 테이블은 rollback 가능 기간을 보존함.
3. Spark 외 엔진을 사용하는 경우 Delta protocol version과 connector 지원 범위를 배포 전 검증함.

**결론 (2줄):**
- 기술사 판단: Spark 중심 분석과 upsert가 많은 lakehouse는 Delta Lake를 우선 검토하고, 다중 vendor catalog 요구가 강하면 Iceberg와 비교해야 함.
- 향후 방향: Delta Lake는 UniForm과 connector 확대로 Iceberg·Hudi와의 metadata 상호운용을 확대하는 방향임.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Delta Lake를 설명하시오" | `_delta_log` commit과 snapshot 구성 | plain Parquet 대비 차이 |
| 요구사항 명시형 | "레이크하우스 테이블 포맷을 비교하시오" | ACID·MERGE·time travel 흐름 | Iceberg/Hudi 대비 선택 기준 |

> 요약: 설명형은 transaction log를, 비교형은 엔진 생태계와 변경 처리 패턴을 중심으로 작성한다.
