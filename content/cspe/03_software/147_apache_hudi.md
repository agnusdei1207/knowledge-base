---
title: "Apache Hudi (Apache Hudi)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 147
---

# 📖 【암기용】 개념 완전 이해

> 목적: Apache Hudi를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Apache Hudi는 데이터 레이크에서 upsert, delete, incremental query를 지원하는 오픈 테이블 포맷임
- **왜 필요한가**: 레이크는 append 파일 저장에는 적합하지만 변경 데이터 반영과 증분 조회가 어렵다. Hudi는 record key와 timeline으로 변경 이력을 관리함.
- **핵심 직관**: 창고에 물건을 계속 추가만 하지 않고, 바코드 기준으로 교체·삭제·변경분 조회를 지원하는 재고 시스템임.

## 깊이 이해
- **배경·문제의식**: CDC 데이터를 레이크에 적재하려면 기존 파일을 모두 재작성하지 않고 특정 키의 최신 값을 반영해야 함.
- **작동 원리**: record key, precombine field, partition path로 레코드를 식별하고 timeline에 commit을 기록함. Copy-on-Write와 Merge-on-Read 테이블 타입을 선택함.
- **비유**: 매일 전체 회원 명단을 새로 만들지 않고 회원번호 기준으로 주소 변경, 탈퇴, 신규 가입만 반영하는 방식임.
- **구체 예시**: 주문 CDC 이벤트를 Hudi MoR 테이블에 쓰고, read optimized view는 집계용, incremental query는 downstream 처리용으로 사용 가능함.
- **흔한 오해·주의점**: Hudi는 스트리밍 엔진 자체가 아님. Spark/Flink 엔진, metadata table, compaction 계획이 함께 필요함.

## 연결 개념
- CDC: Hudi upsert와 incremental query의 주요 입력
- Delta Lake: transaction log 기반 대안 포맷
- Apache Iceberg: 다중 엔진·snapshot 중심 대안 포맷

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Hudi 답안은 upsert 기능만 쓰지 말고 CoW/MoR, timeline, incremental query, compaction 선택 기준을 제시해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Apache Hudi는 레이크 파일에 record-level upsert/delete와 commit timeline을 제공하는 오픈 테이블 포맷이다.
> 2. **가치**: CDC 기반 변경 데이터를 레이크에 반영하고 downstream은 incremental query로 변경분만 소비한다.
> 3. **판단 포인트**: 읽기 지연, 쓰기 빈도, compaction 비용에 따라 Copy-on-Write와 Merge-on-Read를 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Hudi 구조 이해 | record key, timeline, file group, index | 단순 upsert 라이브러리로 설명 |
| 테이블 타입 선택 | CoW vs MoR, compaction, incremental query | 읽기·쓰기 trade-off 누락 |
| CDC 적용 판단 | precombine, idempotent write, delete 처리 | 중복 이벤트와 순서 보장 미기재 |

> 요약: Hudi는 변경 데이터 처리에 초점을 둔 포맷이며, CoW/MoR 선택과 compaction 운영이 답안의 중심이다.

---

## Ⅰ. 개요 및 필요성

- 개요: Apache Hudi는 데이터 레이크용 변경 처리 테이블 포맷이다.
- 배경: CDC와 스트리밍 적재가 많은 환경은 객체 스토리지 파일의 upsert, delete, incremental query가 필요하다.
- 필요성: record key 기반 변경 처리로 전체 재작성 없이 데이터 레이크 변경분을 관리한다.

---

## Ⅱ. 구조 및 구성요소

```text
CDC / Batch Input -> Hudi Writer -> Timeline -> File Group / Index -> Query Engine
                              +-> CoW / MoR Table
                              +-> Compaction / Cleaning
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Record Key | 레코드 식별 | PK, precombine field |
| Timeline | commit, delta commit, compaction 이력 | incremental query 기준 |
| File Group | base file과 log file 묶음 | MoR에서 log merge |
| Index | key 위치 탐색 | Bloom, metadata table |

> 요약: Hudi는 record key와 timeline을 중심으로 파일 그룹 내 변경분을 추적한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
CDC 이벤트 수신 -> record key / precombine 적용 -> index 조회
-> base file 또는 log file 기록 -> timeline commit -> incremental query 제공
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 입력 이벤트에서 key와 최신성 기준 추출 | key null 0건 |
| 2 | index로 기존 레코드 위치 확인 | lookup latency |
| 3 | CoW는 base file 재작성, MoR은 log file 기록 | write amplification |
| 4 | timeline commit 후 compaction/cleaning 수행 | compaction backlog |

> 요약: Hudi는 키 기반으로 변경 대상 위치를 찾고, 테이블 타입에 따라 base file 재작성 또는 log file 병합을 수행한다.

---

## Ⅳ. 특징

| 구분 | 일반 레이크 적재 | Apache Hudi | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 변경 처리 | append 후 재처리 | upsert/delete 지원 | CDC 반영 주기 5분 이하 |
| 조회 방식 | 전체 스캔 | snapshot, read optimized, incremental | downstream 변경분 소비 |
| 테이블 타입 | 단일 파일 모델 | CoW, MoR 선택 | 읽기 p95 vs 쓰기 처리량 |
| 운영 | 파일 정리 수동 | compaction, cleaning | backlog 임계치 설정 |

> 요약: Hudi는 변경 빈도가 높은 레이크 테이블에 적합하나 compaction 지연과 index 비용을 관리해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Apache Hudi | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | append-only Parquet | record key+timeline | CDC upsert 필수 |
| 비용/성능 | 전체 파티션 재작성 | key 기반 부분 반영 | 변경률 20% 이하 |
| 운영/위험 | 단순 적재 | index, compaction 운영 | compaction backlog 통제 가능 |

> 요약: Hudi는 CDC 중심 변경 반영과 incremental pipeline이 필요한 경우 선택 가치가 크다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 중복·역전 이벤트 | CDC 순서 불일치 | precombine timestamp, idempotent write | duplicate key 0건 |
| 조회 지연 | MoR log file 누적 | compaction schedule | log file count, p95 query |
| 인덱스 비용 | 대규모 key lookup | metadata table, partition pruning | index lookup p95 |

> 요약: Hudi 리스크는 이벤트 최신성, log file 누적, index 비용이며 각각 별도 지표가 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 쓰기 | commit latency 5분 이하 | Hudi timeline |
| 조회 | read optimized p95 10초 이하 | query profile |
| 운영 | compaction backlog 3회 이하 | Hudi cleaner/compactor metric |

> 요약: Hudi 운영 성공은 commit 지연, 조회 p95, compaction backlog로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. CDC 원천은 record key와 precombine timestamp를 정의하고 duplicate key 0건을 목표로 idempotent write 구현
2. 조회 중심 테이블은 CoW, 쓰기 빈도 높은 테이블은 MoR로 분리하고 compaction backlog 3회 이하 유지
3. incremental query를 downstream ETL에 적용해 전체 스캔을 변경분 처리로 전환하고 timeline 기반 재처리 절차 수립

**결론 (2줄):**
- 기술사 판단: CDC upsert와 incremental query가 핵심이면 Hudi, 다중 엔진 개방성과 파티션 진화가 중심이면 Iceberg 검토
- 향후 방향: Hudi는 스트리밍 레이크하우스와 CDC 파이프라인에서 변경 데이터 운영 포맷으로 활용 범위가 확대

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Apache Hudi를 설명하시오" | record key, timeline, CoW/MoR 흐름 | append-only 대비 upsert·incremental 차이 |
| 요구사항 명시형 | "Delta/Iceberg와 비교", "CDC 설계", "운영 방안" | precombine, compaction, incremental query | 읽기·쓰기·compaction 선택 기준 |

> 요약: 설명형은 Hudi 내부 구조, 설계형은 CDC와 CoW/MoR 선택 조건으로 전환한다.
