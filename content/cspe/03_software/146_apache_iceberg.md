---
title: "Apache Iceberg (Apache Iceberg)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 146
---

# 📖 【암기용】 개념 완전 이해

> 목적: Apache Iceberg를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Apache Iceberg는 대규모 분석 테이블을 snapshot, manifest, metadata 파일로 관리하는 오픈 테이블 포맷임
- **왜 필요한가**: Hive 테이블은 파티션 변경, schema evolution, 다중 엔진 동시 접근에 한계가 있음. Iceberg는 테이블 메타데이터를 명시적으로 관리해 엔진 독립성을 높임.
- **핵심 직관**: 거대한 파일 묶음에 목차, 판본, 변경 이력, 찾기 색인을 붙여 현재 표준판을 정확히 가리키는 방식임.

## 깊이 이해
- **배경·문제의식**: 레이크하우스 환경은 Spark, Flink, Trino, Presto가 같은 테이블을 읽고 써야 하므로 파일 목록과 파티션 정보를 엔진별로 다르게 해석하면 오류가 발생함.
- **작동 원리**: metadata file이 현재 snapshot을 가리키고, snapshot은 manifest list, manifest는 data/delete file 목록과 통계를 보관함.
- **비유**: 창고 물품을 직접 뒤지는 대신 최신 재고 장부, 구역별 목록, 물품별 위치표를 따라 필요한 상자만 찾는 방식임.
- **구체 예시**: 날짜 파티션을 월 단위에서 일 단위로 바꿔도 hidden partitioning으로 쿼리 사용자는 파티션 구조 변경을 직접 알 필요가 없음.
- **흔한 오해·주의점**: Iceberg는 처리 엔진이 아니라 테이블 포맷임. Spark나 Flink 같은 엔진과 catalog가 함께 있어야 읽기·쓰기 수행 가능함.

## 연결 개념
- 오픈 테이블 포맷: Delta Lake, Iceberg, Hudi 비교 축
- 데이터 레이크하우스: Iceberg가 제공하는 ACID·snapshot 기반 아키텍처
- Catalog: Iceberg 테이블 위치와 metadata pointer를 관리하는 계층

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Iceberg 답안은 snapshot/manifest 구조와 다중 엔진 호환성, hidden partitioning, schema evolution 판단을 분리해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Apache Iceberg는 객체 스토리지 파일을 snapshot과 manifest 메타데이터로 관리하는 오픈 테이블 포맷이다.
> 2. **가치**: 다중 엔진 접근, hidden partitioning, schema/partition evolution, time travel로 레이크하우스 운영 범위를 넓힌다.
> 3. **판단 포인트**: Spark·Flink·Trino 동시 사용, 벤더 종속 축소, 대규모 테이블 metadata pruning 요구를 기준으로 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Iceberg 구조 이해 | metadata file, snapshot, manifest list, manifest | Parquet 포맷으로만 설명 |
| 오픈 포맷 선택 판단 | 다중 엔진, hidden partition, schema evolution | Delta와 동일 기능으로 뭉뚱그림 |
| 운영 리스크 인식 | snapshot expire, orphan file, compaction | catalog 장애와 metadata 증가 누락 |

> 요약: Iceberg는 엔진 독립성과 메타데이터 기반 pruning을 강조해야 채점 포인트를 충족한다.

---

## Ⅰ. 개요 및 필요성

Apache Iceberg는 대규모 분석 테이블용 오픈 테이블 포맷이다. 객체 스토리지의 Parquet/ORC/Avro 파일을 snapshot과 manifest 메타데이터로 관리한다. 다중 엔진 분석, 파티션 변경, schema evolution이 필요한 레이크하우스에서 활용된다.

---

## Ⅱ. 구조 및 구성요소

```text
Catalog -> Metadata File -> Snapshot -> Manifest List -> Manifest -> Data / Delete Files
                              +-> Schema / Partition Spec
                              +-> Statistics / Metrics
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Catalog | 현재 metadata 위치 관리 | Hive, Glue, REST, Nessie |
| Metadata File | schema, partition, snapshot 목록 저장 | table version 기준 |
| Snapshot | 특정 시점 테이블 상태 | time travel, rollback |
| Manifest | data/delete file 목록과 통계 | pruning, delete file |

> 요약: Iceberg는 catalog가 metadata를 가리키고 snapshot·manifest 계층이 유효 파일과 통계를 관리한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
쓰기 요청 -> data file 생성 -> manifest 갱신 -> snapshot 생성
-> metadata pointer commit -> engine snapshot 조회 -> 필요한 파일만 scan
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | writer가 data/delete file 생성 | 파일 완성, checksum |
| 2 | manifest에 파일 경로·통계 기록 | column stats 존재 |
| 3 | snapshot과 metadata file 생성 | snapshot id 연속성 |
| 4 | catalog pointer를 원자적으로 갱신 | commit conflict 검출 |

> 요약: Iceberg는 파일 변경을 manifest와 snapshot으로 묶고 catalog pointer를 갱신해 일관된 테이블 상태를 제공한다.

---

## Ⅳ. 특징

| 구분 | Hive Table | Apache Iceberg | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 파티션 | 사용자가 경로 구조 인지 | hidden partitioning | partition evolution 가능 |
| 메타데이터 | 디렉터리 listing 의존 | manifest 기반 pruning | 대규모 파일 목록 조회 감소 |
| 엔진 | Hive 중심 | Spark, Flink, Trino 지원 | 다중 엔진 PoC 필요 |
| 삭제 | 파티션 재작성 중심 | position/equality delete | GDPR 삭제·CDC 반영 |

> 요약: Iceberg는 파티션과 메타데이터를 테이블 포맷이 관리해 대규모 다중 엔진 분석에 적합하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Apache Iceberg | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Hive metastore+파일 listing | snapshot/manifest 메타데이터 | 파일 수 100만 개 이상 |
| 비용/성능 | 파티션 경로 스캔 | metadata pruning | 필터 컬럼 통계 활용 |
| 운영/위험 | 단일 엔진 최적화 | 다중 엔진 호환성 관리 | Spark/Flink/Trino 공동 사용 |

> 요약: Iceberg는 파일 수가 많고 다중 엔진 접근이 필요한 레이크하우스에서 선택 가치가 크다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 메타데이터 증가 | snapshot·manifest 누적 | expire snapshot, rewrite manifest | metadata size, query planning time |
| 고아 파일 | commit 실패 후 파일 잔존 | remove orphan files | orphan file count |
| 엔진별 결과 차이 | 커넥터 버전 불일치 | 호환성 매트릭스, 회귀 테스트 | query mismatch 0건 |

> 요약: Iceberg 운영은 snapshot 정리, 고아 파일 제거, 엔진 호환성 테스트가 필수 통제 항목이다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 계획 시간 | query planning p95 3초 이하 | engine query profile |
| 메타데이터 | snapshot 보관 7~30일 | metadata table 조회 |
| 호환성 | 주요 쿼리 결과 불일치 0건 | Spark/Trino/Flink regression |

> 요약: Iceberg는 쿼리 실행보다 planning time과 metadata 규모까지 지표로 봐야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Glue/REST Catalog 기반 Iceberg 테이블을 구성하고 Spark 쓰기, Trino 조회, Flink 스트림 반영 시나리오를 PoC로 검증
2. hidden partitioning과 column statistics를 설계해 파일 수 100만 개 이상 테이블의 planning p95 3초 이하 목표 설정
3. expire snapshot, rewrite manifest, remove orphan files를 주 1회 실행하고 엔진별 회귀 쿼리 결과 불일치 0건 확인

**결론 (2줄):**
- 기술사 판단: 다중 엔진 개방성과 partition evolution이 필요하면 Iceberg, Spark 중심 MERGE 운영이면 Delta Lake 우선 검토
- 향후 방향: Iceberg는 REST Catalog와 Nessie 같은 표준 catalog 생태계와 결합해 벤더 종속 축소 방향으로 발전

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Apache Iceberg를 설명하시오" | snapshot, manifest, catalog commit 흐름 | Hive 테이블 대비 파티션·메타데이터 차이 |
| 요구사항 명시형 | "Delta와 비교", "도입 방안", "설계하시오" | 다중 엔진, hidden partitioning, metadata 운영 | 엔진 호환성·planning time·snapshot 관리 |

> 요약: 설명형은 내부 메타데이터 구조, 비교형은 다중 엔진과 partition evolution 선택 기준으로 전환한다.
