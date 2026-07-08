---
title: "Apache Iceberg (Apache Iceberg)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 305
extra:
  question_no: "305"
  exam_status: "기출"
  exam_history: "137회"
  exam_note: "전망"
---

## 미리 알고가기

- Apache Iceberg는 대규모 분석 환경에서 스냅샷 기반 테이블 관리를 제공하는 오픈 테이블 포맷임
- metadata file과 manifest 구조를 사용해 어떤 데이터 파일이 현재 테이블을 구성하는지 추적함
- 멀티엔진 조회와 hidden partitioning이 강점으로 자주 언급됨

## Ⅰ. 개요

- **정의/개념**: Apache Iceberg는 오브젝트 스토리지 위의 데이터 파일과 메타데이터 파일과 manifest 계층을 사용해 스냅샷 기반 ACID 테이블과 진화 가능한 스키마와 파티션 관리를 제공하는 오픈 테이블 포맷임
- **배경/필요성**: 기존 Hive 계열 테이블은 파티션 관리와 메타데이터 탐색과 대규모 동시성 처리에서 한계가 커져 엔진 독립적이고 확장성 높은 테이블 구조가 필요해짐

## Ⅱ. 특징

- 스냅샷과 manifest 구조를 통해 대규모 파일 집합도 효율적으로 추적함
- hidden partitioning으로 사용자가 물리 파티션 세부 구조를 직접 의식하지 않고도 성능을 확보하기 좋음
- Spark와 Trino와 Flink 등 멀티엔진 활용성이 높아 데이터 공유 플랫폼에 적합함
- 메타데이터와 manifest 관리가 복잡해져 유지보수 자동화가 부족하면 운영 난도가 상승함

## Ⅲ. 종류 및 비교

| 판단 기준 | Apache Iceberg | Delta Lake | Apache Hudi |
|:---|:---|:---|:---|
| 메타데이터 구조 | metadata file + manifest | transaction log | timeline + file groups |
| 멀티엔진 호환성 | 높음 | 중간 | 중간 |
| 파티션 관리 | hidden partitioning | 명시적 관리 중심 | workload 별 전략 다양 |
| 대표 강점 | 대규모 분석 공유 | Spark 중심 lakehouse | 증분 ingest와 upsert |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Catalog Pointer | 현재 테이블 메타데이터 파일 위치를 가리켜 원자적 스냅샷 전환을 가능하게 하는 진입점임 |
| Metadata File | 스키마와 파티션과 스냅샷 목록을 관리해 테이블 상태를 정의하는 최상위 메타데이터 계층임 |
| Manifest List and Manifest | 스냅샷이 참조하는 데이터 파일 묶음과 통계를 기록해 대규모 테이블에서도 계획 수립 비용을 줄이는 탐색 계층임 |
| Data Files | Parquet나 ORC 파일에 실제 데이터를 저장하며 메타데이터 계층의 참조를 통해 논리 테이블에 연결됨 |
| Maintenance Actions | rewrite, expire snapshots, compaction을 수행해 성능과 저장 비용을 균형 있게 유지하는 운영 계층임 |

```text
+---------------+
| Catalog       |
+---------------+
        |
        v
+---------------+
| Metadata File |
+---------------+
        |
        v
+---------------+
| Manifests     |
+---------------+
        |
        v
+---------------+
| Data Files    |
+---------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 데이터 작성   | -> | manifest 생성 | -> | metadata 갱신 | -> | catalog 전환 | -> | 스냅샷 조회   |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **데이터 작성**: 새로운 데이터 파일을 저장소에 기록함
2. **manifest 생성**: 데이터 파일 목록과 통계를 manifest에 반영함
3. **metadata 갱신**: 새 스냅샷을 가리키는 metadata file을 생성함
4. **catalog 전환**: catalog pointer를 원자적으로 바꿔 최신 스냅샷을 노출함
5. **스냅샷 조회**: 읽기 엔진이 manifest 통계를 기반으로 필요한 파일만 스캔함

## Ⅵ. 문제점 및 해결 방안

1. 문제: snapshot과 manifest가 지속 증가하면 메타데이터 읽기와 계획 수립 비용이 커져 대규모 쿼리 성능이 저하될 수 있음
   - 해결방안: manifest rewrite와 snapshot expiration policy를 적용하고 planning latency와 metadata size growth rate로 검증함
2. 문제: catalog 일관성과 엔진별 commit 처리 차이가 맞지 않으면 동시 쓰기 충돌과 운영 혼선이 발생할 수 있음
   - 해결방안: catalog consistency control과 commit retry standard를 적용하고 commit conflict rate와 failed snapshot publish count로 검증함
3. 문제: hidden partitioning 특성을 이해하지 못한 채 오래된 질의 습관을 유지하면 파티션 설계 장점이 운영에서 충분히 활용되지 않을 수 있음
   - 해결방안: query optimization guideline과 partition evolution governance를 적용하고 partition pruning effectiveness와 query scan reduction rate로 검증함

## Ⅶ. 적용 사례

- 대규모 멀티엔진 분석 플랫폼이 manifest 정리 작업을 자동화하며 확인 지표는 planning latency와 metadata size growth rate임
- 데이터 플랫폼 팀이 catalog 일관성 기준을 운영하며 확인 지표는 commit conflict rate와 failed snapshot publish count임
- 분석 조직이 파티션 진화 가이드를 적용하며 확인 지표는 partition pruning effectiveness와 query scan reduction rate임

## Ⅷ. 결론

Apache Iceberg는 대규모 멀티엔진 공유에 강하지만 catalog 통제와 메타데이터 유지보수를 꾸준히 운영해야 확장성이 실효성을 가짐.
