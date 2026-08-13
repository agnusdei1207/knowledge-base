---
sidebar:
  order: 127
  label: "127. Delta Lake (Delta Lake)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "Delta Lake (Delta Lake)"
date: "2026-08-13T23:27:00+09:00"
tags:
  - "notes-software"
weight: 127
extra:
  question_no: "127"
  source_status: "기출"
  source_history: "137회"
  priority: 30
  priority_note: "137회 기출, Delta Lake 구현 사례 성격"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Delta Lake**: Databricks가 개발하여 오픈소스화한 대표적인 Open Table Format 기술로, 클라우드 객체 스토리지(S3, ADLS)의 불변 Parquet 파일 상에 JSON 트랜잭션 로그(`_delta_log/`)를 추가하여 ACID 트랜잭션, 타임 트래블, 멱등성 병합(UPSERT/MERGE)을 보장하는 스토리지 레이어.
- **Delta Transaction Log (`_delta_log`)**: 테이블의 모든 파일 추가/삭제(Add/Remove Actions), 스키마 변경 이력이 순차적 JSON 커밋 파일(0000.json, 0001.json...)로 기록되는 산출물 디렉터리.
- **ACID & Time Travel**: `_delta_log` 버전을 추적하여 과거 시점의 데이터를 복원하거나 조회하는 기능 및 동시성 100% 보장.

</details>

- 정의/개념: Parquet와 트랜잭션 로그를 결합한 **Delta Lake**
- 배경/필요성: 파일 직접 갱신은 **부분 실패•동시 쓰기 충돌** 유발

#### 한줄 요약

- 파일을 직접 고쳐 쓰지 않고 어떤 파일을 넣고 뺐는지 거래 일지에 남긴다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **ACID Transactions**: S3 위에서 멀티노드 동시 Write/Read 시 100% 원자성 및 일관성 보장.
- **UPSERT & MERGE Support**: RDBMS처럼 `MERGE INTO` 구문으로 소스 데이터를 타깃 Delta 테이블에 멱등 병합.

</details>

- **JSON Transaction Log (`_delta_log`) 기반 ACID 및 Time Travel 지원**
- **Unified Batch and Streaming (Spark Structured Streaming과 100% 통합)**
- **Schema Enforcement & Schema Evolution (잘못된 컬럼 유입 시 자동 블로킹 및 차단)**

#### 한줄 요약

- 장부가 남아도 가리키는 옛 파일을 지우면 그 시점으로 돌아갈 수 없으므로 보존 기간을 함께 정해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Add & Remove File Actions**: Delta Log 파일 내부의 핵심 JSON 액션으로, 새 파티션 파일이 생성되면 `AddFile`, 이전 파일이 삭제/병합되면 `RemoveFile`을 기록.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Delta Lake Storage Architecture                 │
├────────────────────────────────────────────────────────────────────────┤
│ MyTable/                                                               │
│ ├── _delta_log/                                                        │
│ │   ├── 00000000000000000000.json  (AddFile: part-00001.parquet)       │
│ │   ├── 00000000000000000001.json  (RemoveFile: part-00001, Add: 00002)│
│ │   └── 00000000000000000010.checkpoint.parquet (Log Compaction)      │
│ ├── part-00001-c000.snappy.parquet                                     │
│ └── part-00002-c000.snappy.parquet                                     │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Parquet 실체 데이터 파일과 `_delta_log/` 트랜잭션 로그 파일이 결합하여 ACID 버전을 완성하는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| **`_delta_log`** | Add•Remove•스키마•프로토콜 이력 보관 |
| **Checkpoint** | 누적 로그 상태를 Parquet로 압축 |
| **Parquet Files** | 테이블 행을 불변 열 지향 파일로 저장 |
| **OPTIMIZE** | 작은 파일 병합•데이터 배치 개선 |
| **VACUUM** | 보존 기간이 지난 미참조 파일 제거 |

#### 한줄 요약

- 데이터 파일과 변경 장부를 분리해 각 버전의 표를 재현한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Time Travel Query**: `SELECT * FROM my_table VERSION AS OF 3` 또는 `TIMESTAMP AS OF '2026-08-01'` 형태로 과거 특정 버전 데이터를 0.1초 만에 렌더링.

</details>

```text
[버전 조회 요청]
      │
      ▼
1. 대상 버전 확인
      │
      ▼
2. 최근 Checkpoint 로드
      │
      ▼
3. 후속 로그 재생
      │
      ▼
4. 유효 파일 집합 계산
      │
      ▼
5. Parquet 스캔•반환
```

### 동작 원리

1. **대상 버전 확인**: 버전•시각을 커밋 번호로 해석
2. **최근 Checkpoint 로드**: 대상 이전 압축 상태 복원
3. **후속 로그 재생**: Add•Remove 액션을 순서대로 적용
4. **유효 파일 집합 계산**: 대상 시점의 참조 파일 확정
5. **Parquet 스캔•반환**: 통계 가지치기 후 파일 조회

#### 한줄 요약

- 새 파일을 먼저 만들고 겹친 변경이 없을 때만 다음 장부 번호를 차지해 전체 변경을 공개한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Open Table Format 3대장**: Databricks의 Delta Lake, Netflix의 Apache Iceberg, Uber의 Apache Hudi.

</details>

| 비교 항목 | Delta Lake (Databricks) | Apache Iceberg (Netflix) | Apache Hudi (Uber) |
|:---|:---|:---|:---|
| **개발 및 주도 체계**| **Databricks 중심 오픈소스** | **Apache 재단 (독립 생태계)** | **Apache 재단 (스트리밍 중심)**|
| **메타데이터 구조** | **JSON Log + Parquet Checkpoint**| **AVRO Manifest List + Manifest File**| Timeline Log + Avro |
| **엔진 통합 특성** | Spark•Databricks 중심 | 다중 엔진 중립성 중심 | 증분•CDC 처리 중심 |
| **ACID 동시성 제어**| **Optimistic Concurrency (OCC)** | **Optimistic Concurrency (OCC)** | MVCC / Copy-on-Write |

#### 한줄 요약

- 일반 파일 묶음과 달리 몇 번째 장부인지가 현재 표와 과거 표를 결정한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Z-Ordering**: 특정 컬럼(예: `user_id`, `date`) 공간 채움 곡선을 따라 데이터를 물리적으로 재배치하여 데이터 건너뛰기(Data Skipping) 극대화.

</details>

| 위험 요소 / 문제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| Small File 누적으로 쿼리 속도 저하 | 스트리밍 삽입으로 Small File 무한 생성 | **`OPTIMIZE my_table ZORDER BY (col)` 실행** |
| S3 용량 비용 폭탄 발생 | 삭제된 구버전 Parquet 파일 무한 누적 | **`VACUUM my_table RETAIN 168 HOURS` 주기적 실행**|
| Concurrent Append 충돌 | 다중 노드가 동시에 동일 파티션 쓰기 | **Auto-retry 및 Partition Pruning 분리** |

> 사례: **Databricks 플랫폼 상의 Spark & Delta Lake 기반 모던 데이터 레이크하우스 운용**

#### 한줄 요약

- 주문 수정 파일을 모두 준비해 한 장의 거래 기록으로 공개하고, 읽는 중인 옛 파일은 보존 기간 전에 지우지 않는다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Delta Lake 수립 기준(Delta Lake Standards)**: `_delta_log` 메타데이터, `OPTIMIZE Z-Order` 파일 병합, `VACUUM` 7일 보존 및 Spark 통합성에 의거한 체계.

</details>

- Spark 중심 운영은 **Delta Lake**, 다중 엔진은 Iceberg도 비교

#### 한줄 요약

- 장부와 실제 파일이 모두 있어야 현재와 과거의 표를 안전하게 되살릴 수 있다.
