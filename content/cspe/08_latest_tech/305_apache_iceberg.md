---
title: "Apache Iceberg (Apache Iceberg)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 305
---

# 📖 【암기용】 개념 완전 이해

> 목적: Apache Iceberg를 대규모 분석 테이블을 snapshot metadata로 관리해 여러 엔진이 일관되게 읽고 쓰게 하는 open table format으로 이해하게 만든다.

## 한눈에
- **개요**: 대규모 데이터 레이크 테이블을 snapshot, manifest, catalog로 관리하는 Apache open table format
- **왜 필요한가**: Hive-style partition은 스키마·파티션 변경이 어렵고, 파일 목록 조회 비용이 커지며, 여러 엔진 동시 접근에서 일관성이 흔들린다.
- **핵심 직관**: 책장 전체를 매번 뒤지는 대신 목차와 판본 정보를 보고 어느 파일 묶음이 현재 테이블인지 찾는 방식임.

## 깊이 이해
- **배경·문제의식**: 클라우드 오브젝트 스토리지는 directory listing과 rename이 DBMS만큼 싸지 않아 테이블 상태를 파일 경로 규칙에 의존하면 대규모 쿼리 계획이 느려진다.
- **작동 원리**: Iceberg는 metadata file, manifest list, manifest file, data/delete file 계층으로 snapshot을 구성하고 catalog의 pointer를 atomic swap한다.
- **비유**: 백과사전 여러 판본을 관리할 때 책 자체를 복사하지 않고 판본별 목차와 수정 목록을 관리해 특정 시점 내용을 재구성하는 방식임.
- **구체 예시**: 날짜 파티션을 `days(ts)`에서 `hours(ts)`로 바꿔도 사용자는 `where ts between '2026-07-01' and '2026-07-02'` 조건을 쓰며 hidden partitioning이 파일 pruning에 필요한 변환을 처리한다.
- **흔한 오해·주의점**: Iceberg는 쿼리 엔진이 아니다. Spark, Flink, Trino, Snowflake 같은 엔진이 Iceberg 테이블 메타데이터를 읽어 처리한다.

## 연결 개념
- Open Table Format — Iceberg, Delta, Hudi 비교 축
- Data Catalog — Iceberg table pointer와 권한 관리
- Data Lakehouse — Iceberg 적용 아키텍처

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Iceberg는 hidden partitioning과 snapshot metadata를 중심으로 Delta/Hudi와 비교해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Apache Iceberg는 대규모 분석 테이블의 스키마, 파티션, snapshot, 파일 목록을 명시적 metadata로 관리하는 open table format임.
> 2. **가치**: hidden partitioning, time travel, schema evolution, multi-engine 접근으로 데이터 레이크 테이블 운영을 단순 파일 관리에서 분리함.
> 3. **판단 포인트**: catalog, manifest 계층, snapshot isolation, partition evolution, delete file, engine 호환성을 확인해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| open table format 구조 이해 확인 | metadata file, manifest, snapshot | Parquet 저장 포맷으로만 설명 |
| 대규모 레이크 운영 판단 확인 | hidden partitioning, schema evolution | Hive partition과 동일시 |
| 비교 역량 확인 | Delta/Hudi 대비 catalog·engine 호환성 | 특정 제품 우열 단정 |

> 요약: 이 문제는 Iceberg의 metadata 계층이 대규모 테이블 계획과 진화를 어떻게 처리하는지 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 스냅샷 기반 테이블 포맷
- 배경: Hive-style partition과 파일 listing 기반 테이블 관리는 대규모 오브젝트 스토리지에서 계획 비용과 진화 비용이 커짐.
- 필요성: 여러 엔진이 같은 테이블 snapshot을 읽고 쓰려면 catalog pointer와 metadata commit이 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
Catalog Pointer -> Metadata File -> Snapshot -> Manifest List
        +-> Manifest Files -> Data Files / Delete Files
        +-> Schema / Partition Spec / Sort Order
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Catalog | 현재 metadata file 위치 관리 | REST, Hive, JDBC catalog |
| Metadata File | 스키마·파티션·snapshot 목록 저장 | atomic pointer swap |
| Manifest | data/delete file 목록과 통계 보관 | file pruning |
| Snapshot | 특정 시점 테이블 상태 표현 | time travel, rollback |

> 요약: Iceberg는 catalog pointer와 manifest 계층으로 현재 테이블 상태와 파일 목록을 추적한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
쓰기 작업 -> data/delete file 생성 -> manifest 갱신
-> metadata file 생성 -> catalog pointer atomic commit -> reader snapshot 조회
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | writer가 데이터 파일과 삭제 파일 생성 | file metrics |
| 2 | manifest에 파일 경로, partition, 통계 기록 | manifest validity |
| 3 | 새 metadata file과 snapshot 생성 | snapshot id |
| 4 | catalog pointer를 새 metadata로 교체 | commit success |

> 요약: Iceberg는 데이터 파일을 직접 현재 상태로 보지 않고 snapshot metadata와 catalog pointer로 일관성을 보장한다.

---

## Ⅳ. 특징

| 구분 | Hive Table | Apache Iceberg | 판단 기준 |
|:---|:---|:---|:---|
| 파티션 | 경로 규칙 노출 | hidden partitioning | 사용자의 조건 작성 부담 |
| 스키마 변경 | 위치 기반 오류 가능 | field ID 기반 evolution | column rename/delete |
| 테이블 상태 | 디렉터리 listing | snapshot metadata | 대규모 파일 수 |
| 엔진 연계 | Hive ecosystem 중심 | Spark/Flink/Trino 등 | multi-engine 요구 |

> 요약: Iceberg는 Hive table의 경로 의존성을 metadata 계층으로 대체해 스키마·파티션 진화와 엔진 호환성을 확보한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| Delta Lake | transaction log 중심 | manifest/snapshot 중심 | Spark 중심 vs multi-engine |
| Hudi | upsert·incremental 중심 | 대규모 analytic table 중심 | CDC 빈도 |
| Plain Parquet | 파일 목록 직접 관리 | catalog metadata 관리 | table count와 file count |

> 요약: Iceberg는 엔진 중립성과 대규모 분석 테이블 진화가 중요할 때 우선 검토한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| manifest 증가 | 잦은 소규모 commit | rewrite manifests, compaction | manifest count |
| catalog 병목 | 중앙 metadata 요청 집중 | catalog HA, cache | catalog latency |
| delete file 누적 | row-level delete 반복 | rewrite data files | delete file ratio |

> 요약: Iceberg 운영 리스크는 manifest, catalog, delete file 누적이며 주기적 rewrite와 catalog 확장으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 계획 시간 | query planning SLA 충족 | engine explain/log |
| snapshot 관리 | 보존 정책 내 snapshot 유지 | expire snapshots |
| 엔진 호환 | 주요 엔진 read/write 통과 | compatibility test |

> 요약: Iceberg 도입 효과는 query planning, snapshot 보존, multi-engine 호환성으로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. REST Catalog 또는 Hive Catalog를 선정하고 catalog HA, 권한 정책, metadata 백업 절차를 설계함.
2. partition evolution, schema evolution, snapshot retention 정책을 테이블 등급별로 정의함.
3. Spark, Flink, Trino 등 사용 엔진별 Iceberg version과 delete/merge 지원 범위를 사전 검증함.

**결론 (2줄):**
- 기술사 판단: 다중 분석 엔진과 대규모 테이블 진화가 핵심이면 Iceberg가 적합하고, Spark 중심 변경 처리 워크로드는 Delta와 비교해야 함.
- 향후 방향: Iceberg는 REST Catalog, vendor-neutral lakehouse, open table interoperability의 중심 포맷으로 확산됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Apache Iceberg를 설명하시오" | manifest와 snapshot commit 흐름 | Hive table 대비 차이 |
| 요구사항 명시형 | "open table format을 비교하시오" | catalog·snapshot·delete file 처리 | Delta/Hudi 대비 선택 기준 |

> 요약: 설명형은 metadata 계층을, 비교형은 엔진 중립성과 운영 리스크를 중심으로 작성한다.
