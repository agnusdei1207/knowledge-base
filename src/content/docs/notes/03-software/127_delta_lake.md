---
sidebar:
  order: 127
  label: "127. Delta Lake (Delta Lake)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "Delta Lake (Delta Lake)"
date: "2026-08-06T23:27:50+09:00"
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

- 정의/개념: 가성비 높은 S3 객체 스토리지의 Parquet 파일 상에 트랜잭션 로그(`_delta_log`)를 레이어링하여, ACID 트랜잭션, 스키마 강제, 타임 트래블을 구현한 오픈소스 Open Table Format 기술인 **Delta Lake**
- 배경/필요성: 기존 S3 Parquet 파일의 동시 쓰기 시 파일 덮어쓰기 파행 및 부분 실패(Partial Fail)로 인한 데이터 오염 극복 요구성

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

## Ⅲ. 구조 및 구성요소 (Delta Log 메커니즘 및 3대 액션)

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

| 구성요소 (Element) | 역할 및 기술 메커니즘 | 실무 튜닝 포인트 |
|:---|:---|:---|
| **`_delta_log/`** | **모든 CUD 변경 이력 JSON 커밋 로그 보존** | 10번째마다 Checkpoint Parquet 합성 |
| **Parquet Files** | **실제 테이블 데이터가 열 지향 불변 압축 저장됨** | Snappy 압축 적용 |
| **`OPTIMIZE` Engine**| **자자한 Small Files를 1GB 단위 큰 파일로 병합 (Bin-packing)**| 스캔 쿼리 속도 10배 가속 |
| **`VACUUM` Engine** | **`_delta_log`에서 `RemoveFile` 처리된 쓰레기 Parquet 물리 파기**| Default 7일 이전 파일 삭제 |

#### 한줄 요약

- 데이터 파일과 변경 장부를 분리해 각 버전의 표를 재현한다.

## Ⅳ. 흐름도 (Delta Lake Time Travel & MERGE INTO 흐름)

<details><summary>핵심 용어</summary>

- **Time Travel Query**: `SELECT * FROM my_table VERSION AS OF 3` 또는 `TIMESTAMP AS OF '2026-08-01'` 형태로 과거 특정 버전 데이터를 0.1초 만에 렌더링.

</details>

```text
[Client Query: VERSION AS OF 2] ──► [_delta_log/ 0000~0002.json 스캔]
                                          │
                                          ▼
 [AddFile 로 남아있는 유효 Parquet 목록 추출] ──► [S3 해당 Parquet 만 읽어 즉시 리턴!]
```

### 동작 원리

1. **Version Target**: 사용자가 버전 2 시점의 쿼리 요청.
2. **Log Replay**: `_delta_log` 0~2번 JSON 파일을 순차 읽어 해당 시점의 `AddFile` 포인터 집합 계산.
3. **Scan Execution**: 제거되지 않은 과거 Parquet 파일만 S3에서 읽어 반환 (**완벽한 Time Travel 구현**).

#### 한줄 요약

- 새 파일을 먼저 만들고 겹친 변경이 없을 때만 다음 장부 번호를 차지해 전체 변경을 공개한다.

## Ⅴ. 종류 및 비교 (Delta Lake vs Apache Iceberg vs Apache Hudi)

<details><summary>핵심 용어</summary>

- **Open Table Format 3대장**: Databricks의 Delta Lake, Netflix의 Apache Iceberg, Uber의 Apache Hudi.

</details>

| 비교 항목 | Delta Lake (Databricks) | Apache Iceberg (Netflix) | Apache Hudi (Uber) |
|:---|:---|:---|:---|
| **개발 및 주도 체계**| **Databricks 중심 오픈소스** | **Apache 재단 (독립 생태계)** | **Apache 재단 (스트리밍 중심)**|
| **메타데이터 구조** | **JSON Log + Parquet Checkpoint**| **AVRO Manifest List + Manifest File**| Timeline Log + Avro |
| **Spark 통합성** | **극상 (Spark 엔진 최적화 1순위)**| 상 (모든 엔진 중립성) | 상 (스트리밍 CDC 최적화) |
| **ACID 동시성 제어**| **Optimistic Concurrency (OCC)** | **Optimistic Concurrency (OCC)** | MVCC / Copy-on-Write |

#### 한줄 요약

- 일반 파일 묶음과 달리 몇 번째 장부인지가 현재 표와 과거 표를 결정한다.

## Ⅵ. 실무 고려사항 및 대책 (Delta Lake 운영 최적화 지침)

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

- **Delta Lake 수립 기준**에 따라 Databricks/Spark 기반 레이크하우스 구축 시 **Delta Lake & OPTIMIZE Z-Ordering** 필수 적용

#### 한줄 요약

- 장부와 실제 파일이 모두 있어야 현재와 과거의 표를 안전하게 되살릴 수 있다.
