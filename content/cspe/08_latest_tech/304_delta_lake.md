---
title: "Delta Lake (Delta Lake)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 304
extra:
  question_no: "304"
  exam_status: "기출"
  exam_history: "137회"
  exam_note: "전망"
---

## 미리 알고가기

- Delta Lake는 Parquet 파일 위에 트랜잭션 로그를 추가해 데이터 레이크를 테이블처럼 관리하는 기술임
- append only 로그와 checkpoint를 이용해 최신 테이블 상태를 재구성함
- Lakehouse 구현에서 ACID와 schema enforcement와 time travel을 제공하는 대표 포맷 중 하나임

## Ⅰ. 개요

- **정의/개념**: Delta Lake는 오브젝트 스토리지의 Parquet 파일 집합에 transaction log를 결합해 ACID 트랜잭션과 스키마 관리와 버전 조회를 제공하는 lakehouse용 오픈 테이블 기술임
- **배경/필요성**: 기존 데이터 레이크는 동시 쓰기와 업데이트와 삭제와 스키마 변경 관리가 약해 분석 신뢰성이 떨어졌고 이를 보완할 메타데이터 기반 테이블 관리가 요구됨

## Ⅱ. 특징

- commit log 중심 구조라 쓰기 이력과 변경 추적이 비교적 직관적임
- schema enforcement와 schema evolution 기능이 강해 데이터 품질 통제에 유리함
- Spark 생태계와 결합성이 높아 배치와 스트리밍 통합 처리에 적합함
- 작은 파일 관리와 로그 최적화를 주기적으로 하지 않으면 성능 저하가 빠르게 나타날 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Delta Lake | Apache Iceberg | Apache Hudi |
|:---|:---|:---|:---|
| 메타데이터 방식 | transaction log 중심 | snapshot metadata tree | timeline and file services |
| 강점 | Spark 통합성과 관리 편의 | 멀티엔진 호환성 | 증분 처리와 upsert |
| 동시성 관점 | optimistic concurrency | snapshot commit | write mode 다양 |
| 대표 활용 | lakehouse 분석 플랫폼 | 대규모 멀티엔진 분석 | 실시간 데이터 레이크 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Parquet Data Files | 실제 레코드를 저장하는 물리 계층으로 컬럼형 분석 성능을 제공하면서 로그 메타데이터와 결합해 테이블을 구성함 |
| Delta Transaction Log | add와 remove와 metadata 변경 이력을 기록해 테이블 상태를 재구성하고 ACID commit의 기준점이 되는 핵심 제어 계층임 |
| Checkpoint Files | 누적 로그를 압축한 스냅샷 요약본으로 로그 재생 비용을 줄여 대형 테이블의 조회 초기 지연을 완화함 |
| Schema and Constraint Manager | 스키마 강제와 진화를 관리해 잘못된 적재를 줄이고 운영 데이터 품질을 유지하는 검증 계층임 |
| Optimization Services | compaction과 data skipping과 vacuum을 수행해 파일 단편화와 불필요한 버전 잔재를 줄이는 운영 계층임 |

```text
+---------------+    +---------------+    +---------------+
| Delta Log     | -> | Checkpoint    | -> | Query Snapshot|
+---------------+    +---------------+    +---------------+
        |
        v
+---------------+
| Parquet Files |
+---------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 데이터 쓰기   | -> | 임시 파일 생성 | -> | 로그 커밋     | -> | 스냅샷 확정   | -> | 조회/최적화   |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **데이터 쓰기**: 작업 노드가 변경 대상 데이터를 생성함
2. **임시 파일 생성**: Parquet 파일을 먼저 저장소에 기록함
3. **로그 커밋**: 변경 파일 목록과 메타데이터를 Delta log에 원자적으로 반영함
4. **스냅샷 확정**: 로그와 checkpoint를 이용해 최신 일관 상태를 노출함
5. **조회와 최적화**: 읽기 엔진이 스냅샷을 참조하고 운영 작업이 compaction과 vacuum을 수행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 작은 파일과 잦은 커밋이 누적되면 로그와 메타데이터 탐색 비용이 커져 쿼리 지연과 운영 부하가 함께 증가할 수 있음
   - 해결방안: auto compaction과 optimized write policy를 적용하고 average file size와 snapshot load latency로 검증함
2. 문제: 엔진별 Delta 기능 지원 수준이 다르면 멀티엔진 환경에서 동일 테이블의 기능 활용 범위가 제한될 수 있음
   - 해결방안: feature compatibility baseline과 engine certification test를 적용하고 supported feature coverage와 cross engine read failure count로 검증함
3. 문제: vacuum과 retention 설정을 과도하게 줄이면 time travel과 복구 가능 범위가 예상보다 빠르게 사라질 수 있음
   - 해결방안: retention governance와 recovery objective mapping을 적용하고 recoverable version window와 accidental data loss incident count로 검증함

## Ⅶ. 적용 사례

- 대규모 ETL 플랫폼이 optimized write를 적용하며 확인 지표는 average file size와 snapshot load latency임
- 멀티엔진 분석 환경이 기능 인증 테스트를 운영하며 확인 지표는 supported feature coverage와 cross engine read failure count임
- 운영 데이터 레이크가 retention 정책을 업무 중요도별로 관리하며 확인 지표는 recoverable version window와 accidental data loss incident count임

## Ⅷ. 결론

Delta Lake는 로그 기반 관리로 lakehouse 운영을 단순화하지만 파일 최적화와 엔진 호환성 정책을 같이 운영해야 장점이 유지됨.
