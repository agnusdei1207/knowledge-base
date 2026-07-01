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
- **개요**: Delta Lake는 Parquet 파일 위에 transaction log를 더해 ACID, time travel, schema evolution을 제공하는 레이크하우스 테이블 포맷임
- **왜 필요한가**: 객체 스토리지 파일만으로는 동시 쓰기, 부분 실패, 업데이트, 삭제, 버전 복구를 다루기 어렵다. Delta Lake는 `_delta_log`로 테이블 상태를 관리함.
- **핵심 직관**: 파일 창고에 변경 이력 장부를 붙여 어느 파일이 현재 유효한지 정확히 알려주는 방식임.

## 깊이 이해
- **배경·문제의식**: 데이터 레이크는 파일 append에는 적합하지만 CDC upsert, GDPR 삭제, BI 일관성 조회에는 트랜잭션 단위 관리가 필요함.
- **작동 원리**: Parquet 데이터 파일과 JSON/Checkpoint 형태의 `_delta_log`가 commit 이력을 기록하고, 쿼리 엔진은 최신 snapshot에 포함된 파일만 읽음.
- **비유**: 도서관 서가에 책을 직접 덮어쓰지 않고, 대출·폐기·추가 이력을 장부에 기록해 현재 목록을 산출하는 방식임.
- **구체 예시**: 주문 CDC를 `MERGE INTO`로 반영하고 오류 발생 시 version 120에서 119로 time travel 조회해 장애 전 데이터를 검증 가능함.
- **흔한 오해·주의점**: Delta Lake는 Databricks 전용 개념이 아님. 다만 엔진별 기능 지원 범위와 catalog 연동 수준은 배포판에 따라 차이 있음.

## 연결 개념
- 데이터 레이크하우스: Delta Lake가 구현하는 아키텍처
- Apache Iceberg: manifest와 snapshot metadata 중심의 대안 포맷
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

| 비교 축 | 기존/대안 | Delta Lake | 선택 기준 |
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
