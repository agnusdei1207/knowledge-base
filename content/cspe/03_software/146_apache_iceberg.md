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
- **개요**: Apache Iceberg는 **오픈 테이블 포맷**의 하나로, **metadata file → manifest list → manifest**라는 3단 메타데이터 계층으로 데이터 파일을 관리해 여러 처리 엔진이 동일한 테이블을 안전하게 동시에 읽고 쓰게 한다.
- **왜 필요한가**: Hive 테이블은 "파티션 = 디렉터리 경로"로 파일과 스키마 정보를 암묵적으로 표현해, 파티션 구조를 바꾸면 기존 쿼리가 깨지고 파일이 수백만 개면 디렉터리 리스팅 자체가 느려진다. Iceberg는 파일 목록과 통계를 메타데이터 파일 안에 명시적으로 저장해 이 문제를 없앤다.
- **핵심 직관**: 창고 바닥을 걸어 다니며 상자를 세는 대신, 사무실 장부(메타데이터)만 보고 "어느 구역에 몇 개 상자가 있는지" 즉시 계산하는 방식이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 오픈 테이블 포맷 | Parquet/ORC 파일 위에 메타데이터 계층을 얹어 ACID·버전 관리를 제공하는 표준 규격 — Iceberg가 속하는 **상위 범주** | 낱장 문서 더미에 표지·목차를 붙인 정식 문서철 |
| Metadata File | 테이블의 현재 스키마·파티션 규칙·최신 snapshot 목록을 담은 최상위 파일 — Iceberg **정체성**의 핵심 | 회사의 최신 정관·조직도 |
| Snapshot | 특정 시점 테이블의 "유효 데이터 파일 전체 집합" | 특정 시각의 재고 스냅샷 사진 |
| Manifest List | 하나의 snapshot을 구성하는 manifest 파일들의 목록(파티션 범위 요약 포함) | 여러 창고 구역별 요약 인덱스 |
| Manifest | 실제 data/delete file 경로와 컬럼 통계(min/max, null count)를 담은 파일 | 각 구역의 상세 물품 목록표 |
| Catalog | 테이블 이름 → 현재 metadata file 위치를 가리키는 포인터를 관리 | 건물 안내데스크의 사무실 호수 대장 |
| Hidden Partitioning | 사용자는 논리 컬럼(예: event_time)으로만 쿼리하고, 실제 파티션 경로 변환은 Iceberg가 대신 처리 | 우편번호만 적으면 집배원이 알아서 배송 구역을 찾아줌 |
| Partition Evolution | 기존 데이터를 재작성하지 않고 앞으로의 파티션 규칙만 바꾸는 기능 | 앞으로는 새 분류법 적용, 옛 재고는 그대로 |
| Position/Equality Delete File | 행을 물리적으로 지우지 않고 "이 파일의 N번째 행은 삭제됨"을 기록하는 파일 | 삭제 스티커만 붙이고 실물은 나중에 치움 |

## 깊이 이해

### 왜 Hive 방식이 한계였나 — 수치로 이해
- Hive 테이블에서 파일이 100만 개면, "특정 날짜 데이터를 찾아라"는 쿼리도 디렉터리를 나열(list)하는 데만 수 분이 걸릴 수 있다(객체 스토리지는 파일시스템과 달리 디렉터리 개념이 없어 prefix 나열이 느리다). Iceberg는 이 나열을 메타데이터 파일 읽기로 대체해 계획(planning) 시간을 초 단위로 줄인다.

### 3단 메타데이터로 필요한 파일만 골라내는 과정 — 워크드 예제
- 예: 전체 테이블에 파일 100만 개, 파티션은 일 단위(365개)로 나뉘어 있다고 하자. `WHERE event_date = '2026-07-03' AND amount > 1000` 쿼리가 들어오면:
  1) Metadata file에서 최신 snapshot(v87)을 찾는다.
  2) Manifest list에서 각 manifest가 담당하는 파티션 범위(min/max event_date)를 보고, event_date=2026-07-03을 포함하지 않는 manifest(전체의 약 99.7%)는 즉시 스킵한다.
  3) 남은 manifest 안에서 각 파일의 컬럼 통계(amount의 min/max)를 보고, amount>1000이 될 수 없는 파일(예: max가 500인 파일)도 스킵한다.
- 결과적으로 100만 개 파일 중 실제로 열어보는 파일은 수십~수백 개 수준으로 줄어든다 — 이것이 metadata pruning이다.

### Hidden Partitioning — 예제
- Hive 방식이면 사용자가 `WHERE year=2026 AND month=07 AND day=03`처럼 파티션 컬럼을 직접 알고 써야 한다. 파티션을 월별에서 일별로 바꾸면 기존 쿼리가 깨진다.
- Iceberg는 `PARTITIONED BY (days(event_time))`처럼 변환 함수를 테이블 정의에 넣어두므로, 사용자는 그냥 `WHERE event_time = '2026-07-03'`이라고만 쓰면 된다. 나중에 파티션을 `days`에서 `hours`로 바꿔도(Partition Evolution) 과거 데이터는 재작성 없이 그대로 두고, 새로 들어오는 데이터부터 시간 단위로 나뉜다.

### 삭제 처리 — Position/Equality Delete 예제
- GDPR 요청으로 회원 1명(파일 하나의 1,000행 중 3행)을 삭제해야 할 때, 전통 방식은 해당 파일 전체를 재작성해야 한다. Iceberg는 "파일 X의 15, 302, 981번째 행 삭제"라는 작은 delete file만 추가하고, 다음 읽기 시 원본 파일과 delete file을 merge-on-read로 합쳐 보여준다 — 대용량 파일 재작성 없이 즉시 반영된다.

### 비유와 오해
- **비유**: 사무실 장부(메타데이터)만 보고 창고 전체를 뒤지지 않고도 필요한 상자 위치를 즉시 아는 방식이다.
- **오해 1**: Iceberg가 처리 엔진이다 — 아니다. Iceberg는 파일 형식·메타데이터 규격일 뿐이고, 실제 읽기/쓰기는 Spark·Flink·Trino 같은 엔진과 Catalog가 수행한다.
- **오해 2**: snapshot이 많아도 무해하다 — 아니다. snapshot·manifest가 만료 없이 계속 쌓이면 metadata 자체가 커져 planning이 느려지므로 expire snapshot·rewrite manifest 같은 유지보수가 필요하다.

## 연결 개념
- 오픈 테이블 포맷: Delta Lake, Apache Hudi와 함께 비교되는 상위 범주 (145·147에서 상세)
- 데이터 레이크하우스: Iceberg가 제공하는 ACID·snapshot 기반 아키텍처 (144에서 상세)
- Catalog: Iceberg 테이블 위치와 metadata pointer를 관리하는 계층(Hive, Glue, REST, Nessie)

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

- 개요: Apache Iceberg는 대규모 분석용 오픈 테이블 포맷이다.
- 배경: 객체 스토리지의 Parquet/ORC/Avro 파일은 테이블 단위 스냅샷과 파티션 변경 관리가 필요하다.
- 필요성: snapshot과 manifest 메타데이터로 다중 엔진 분석, 파티션 변경, schema evolution을 지원한다.

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
