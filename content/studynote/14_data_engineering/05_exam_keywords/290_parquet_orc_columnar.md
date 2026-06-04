---
title: "290. 파케이 ORC 열 지향 저장 포맷 최적화 (Parquet ORC Columnar Storage Format)"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Apache Parquet와 Apache ORC는 컬럼 단위 물리 저장(Columnar Physical Layout) + 메타데이터 푸시다운(Min/Max, BloomFilter, Dictionary Index) + 청크 단위 인코딩(RLE, Dictionary, Delta, Byte Stream Split)을 결합한 이진 트리 기반 OLAP 최적화 포맷으로, 행 전체가 아닌 필요한 컬럼만 디스크에서 읽어 I/O를 근본적으로 줄인다.
> 2. **가치**: 동일 데이터셋에서 행 지향(Avro/CSV) 대비 I/O 70~90% 절감, Snappy/Zstd 압축 시 디스크 점유 5~10× 축소, Predicate Pushdown 기반 TPC-DS 쿼리 처리 시간 10~100× 단축, 분석 워크로드의 CPU-bound -> IO-bound 전환을 통한 클러스터 자원 효율 3~5× 개선 효과가 입증되어 있다.
> 3. **판단 포인트**: (a) Row Group/Strip 크기(기본 128MB vs 64MB) 및 Page 크기(1MB) 튜닝, (b) Parquet ↔ ORC 선택 기준(중첩 데이터/Schema Evolution은 Parquet, Hive-native 압축·ACID는 ORC), (c) 작은 파일(Small Files) 문제에 대한 Compaction 전략, (d) Z-Order/希尔伯特 곡선을 통한 클러스터링, (e) Delta Lake/Iceberg/Hudi 같은 Table Format 레이어 도입 여부.

---

## Ⅰ. 개요 및 필요성

### 1. 배경: OLAP 워크로드의 I/O 병목

2010년대 들어 Hadoop, Spark, Impala, Presto 등 분산 컴퓨팅 엔진이 보편화되면서 페타바이트급 데이터 분석이 일상화되었다. 그러나 전통적인 행 지향(Row-Oriented) 포맷인 CSV, JSON, Avro, SequenceFile은 분석 쿼리에서 **심각한 I/O 비효율**을 야기했다.

핵심 문제점:
- **선택성(Selectivity) 문제**: `SELECT avg(salary) FROM employees WHERE dept='SALES'` 쿼리에서 실제 읽기 필요한 컬럼은 2개(salary, dept)뿐이지만 행 지향 포맷은 100개 컬럼 전체를 디스크에서 읽음
- **압축 효율 저하**: 같은 컬럼 내 데이터는 유사한 분포(예: `dept` 컬럼은 5개 값 반복)를 가지지만 행 지향은 컬럼 값들이 섞여 저장되어 Entropy가 높아짐
- **반복 필드 처리 비효율**: 로그 데이터의 `tags[], attributes{}` 같은 반정형 데이터는 행 지향에서 가독성은 좋지만 컬럼형 분석에는 부적합

### 2. 컬럼 지향 포맷의 등장

**Apache Parquet**는 2013년 Twitter와 Cloudera가 공동 개발하여 Apache TLP에 기증한 포맷으로, Google Dremel 논문의 **"Striping/Assembly 알고리즘"**과 Google Protocol Buffers의 **신호 없는 VarInt 인코딩**을 계승했다. **Apache ORC(Optimized Row Columnar)**는 2015년 Hortonworks가 Hive 0.11의 RCFile을 개선하여 출시, ACID 트랜잭션과 경량 인덱스(Painted 인덱스, Bloom Filter)를 네이티브 지원한다.

두 포맷 모두 2015년 Apache TLP로 승격되어 현재 **빅데이터 생태계의 de facto 표준**으로 자리잡았으며, Spark SQL, Hive, Impala, Presto/Trino, Drill, Dremio, DuckDB, ClickHouse 등 모든 주요 분석 엔진이 기본 입력 포맷으로 채택하고 있다.

```text
[Row-Oriented vs Column-Oriented 물리 레이아웃 비교]

    Row-Oriented (Avro/CSV)                  Column-Oriented (Parquet/ORC)
    +--------------------------+             +--------------------------+
    | Block 1: 1,000 rows      |             | Block 1: Col A 1,000 vals|
    | +--+--+--+--+--+        |             | [1][1][1][2][2][2][3]... |
    | |id|nm|dt|vl|st|        |             +--------------------------+
    | +--+--+--+--+--+        |             | Block 1: Col B 1,000 vals|
    | |1 |A |X |10|OK|        |             | [A][A][A][B][B][B][C]... |
    | |1 |A |Y |20|OK|        |             +--------------------------+
    | |1 |A |Z |30|ER|        |             | Block 1: Col C 1,000 vals|
    | |2 |B |X |40|OK|        |             | [X][Y][Z][X][Y][Z][X]... |
    | |2 |B |Y |50|OK|        |             +--------------------------+
    | |2 |B |Z |60|ER|        |             | Block 1: Col D 1,000 vals|
    | |3 |C |X |70|OK|        |             | [10][20][30][40][50]...  |
    | |3 |C |Y |80|OK|        |             +--------------------------+
    | |3 |C |Z |90|ER|        |             | Block 1: Col E 1,000 vals|
    | +--+--+--+--+--+        |             | [OK][OK][ER][OK][OK]...  |
    | 전체 행을 순차 읽음      |             | 컬럼만 선택적으로 읽음    |
    +--------------------------+             +--------------------------+
    SELECT avg(vl) -> 5컬럼 읽음              SELECT avg(vl) -> 1컬럼만 읽음
    I/O = 5×필요량                            I/O = 1×필요량 (80% 절감)
```

### 3. 기술적 패러다임 전환: "Read-Optimized" 시대

| 항목 | OLTP (행 지향) | OLAP (열 지향) |
|:---|:---|:---|
| **워크로드** | 단건/소량 행 조회·갱신 | 대량 행 스캔·집계 |
| **읽기 패턴** | 임의 접근(Random Read) | 순차 접근(Sequential Scan) |
| **쓰기 패턴** | 빈번(INSERT/UPDATE/DELETE) | 배치 단위 일괄 적재 |
| **압축 친화성** | 낮음(컬럼 혼재) | 높음(컬럼 내 데이터 동질성) |
| **벡터화 친화성** | 없음 | 높음(SIMD, GPU 친화) |
| **인덱스 전략** | B+Tree, Hash | Min/Max Zone Map, Bloom Filter |
| **대표 포맷** | MySQL InnoDB, Avro, Protobuf | **Parquet, ORC, Arrow** |

- **📢 섹션 요약 비유**: 행 지향 저장소는 "사물함 1개당 1명분 옷(전신)을 한꺼번에 넣어두는 것"이고, 열 지향 저장소는 "상의/하의/양말을 종류별로 별도 서랍에 분리 저장"하는 것입니다. "양말만 꺼내달라"고 하면 전신 옷을 꺼내는 행 지향 서랍장보다 양말 서랍만 열어보는 열 지향 서랍장이 압도적으로 빠릅니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Parquet 파일 구조: 3단계 계층 + Thrift 메타데이터

Parquet 파일은 **Row Group -> Column Chunk -> Page**의 3단계 계층으로 구성되며, **Thrift로 인코딩된 Footer(파일 메타데이터)**가 모든 인덱스 정보를 포함한다. Footer는 파일 끝에 위치하므로 **읽기 시점에 한 번의 `seek + read`로 전체 인덱스를 메모리에 적재**할 수 있다.

```text
[Parquet File Internal Layout (Magic: PAR1)]

    +-------------------------------------------------------------+
    |                  Row Group 0 (default 128MB)                |
    | +----------+ +----------+ +----------+ +----------+         |
    | | Column   | | Column   | | Column   | | Column   |         |
    | | Chunk A  | | Chunk B  | | Chunk C  | | Chunk D  |  ...    |
    | | +------+ | | +------+ | | +------+ | | +------+ |         |
    | | |Page 0| | | |Page 0| | | |Page 0| | | |Page 0| |         |
    | | |(1MB) | | | |(1MB) | | | |(1MB) | | | |(1MB) | |         |
    | | +------+ | | +------+ | | +------+ | | +------+ |         |
    | | |Page 1| | | |Page 1| | | |Page 1| | | |Page 1| |         |
    | | |(1MB) | | | |(1MB) | | | |(1MB) | | | |(1MB) | |         |
    | | +------+ | | +------+ | | +------+ | | +------+ |         |
    | +----------+ +----------+ +----------+ +----------+         |
    +-------------------------------------------------------------+
    |                  Row Group 1 (128MB)                        |
    |                  ... (동일 구조) ...                         |
    +-------------------------------------------------------------+
    |              File Footer (Thrift 인코딩)                     |
    |  • version, schema, num_rows                                |
    |  • row_groups[i]: {                                          |
    |      columns[j]: {                                           |
    |        file_offset, file_path,                              |
    |        encodings (PLAIN/RLE/PLAIN_DICTIONARY/...)           |
    |        path_in_schema, codec (SNAPPY/GZIP/ZSTD/...)         |
    |        encodings,                                            |
    |        total_compressed_size, total_uncompressed_size,      |
    |        data_page_offset, index_page_offset,                 |
    |        statistics: { min, max, null_count, distinct_count,  |
    |                      min_value, max_value, is_max_value_exact|
    |                      is_min_value_exact }                   |
    |      }                                                       |
    |    }                                                         |
    +-------------------------------------------------------------+
    |              4-byte length (footer size)                    |
    |              "PAR1" Magic (파일 시작/끝 검증)                |
    +-------------------------------------------------------------+

    ★ Predicate Pushdown: Footer 읽기 -> Min/Max로 Row Group 스킵 결정
    ★ Projection Pushdown: 필요한 Column Chunk만 디스크 Read
```

### 2. ORC 파일 구조: Stripe + 인덱스 스트림

ORC는 Parquet의 3단계 구조를 **Stripe (≈Row Group) -> Row Index (≈10,000 rows) -> Stream**으로 단순화하면서, **Footer가 아닌 Stripe Footer**에 인덱스를 두어 스트리밍 쓰기/읽기에 최적화했다. **Painted Min-Max Index**는 10,000행 단위 Granularity로 `min/max/null_count`를 저장해 Stripe 스킵이 가능하다.

```text
[ORC File Internal Layout (Magic: ORC)]

    +-------------------------------------------------------------+
    |  Postscript (압축 종류, Footer 크기, 버전)                  |
    +-------------------------------------------------------------+
    |  File Footer (Thrift 인코딩)                                |
    |  • stripeCount, rowCount, schema                            |
    |  • columnStatistics: { intSum, doubleSum, min, max, count }  |
    |  • stripes[i]: { fileOffset, indexLength, dataLength, footer}|
    +-------------------------------------------------------------+
    |  Stripe 0 (default 64MB = 16MB × 4 buffer)                 |
    |  +------------------------------------------+               |
    |  |  Index Stream: Row Index (10K row 단위)  |               |
    |  |           + Bloom Filter (선택 컬럼)     |               |
    |  +------------------------------------------+               |
    |  |  Data Stream (Present/Length/Data)       |               |
    |  |   Col A: +-Present-+ +-Data-+           |               |
    |  |          | 10110.. | | 1 1 1|           |               |
    |  |          +---------+ | 2 2 2|           |               |
    |  |   Col B: +-Length--+ | ... |           |               |
    |  |          | 0010... | +------+           |               |
    |  |          +---------+                    |               |
    |  +------------------------------------------+               |
    |  |  Stripe Footer (열별 스트림 위치)        |               |
    |  +------------------------------------------+               |
    +-------------------------------------------------------------+
    |  Stripe 1 (64MB) ... (반복)                                |
    +-------------------------------------------------------------+

    ★ Columnar Stream: 컬럼별 Present(Null 여부) / Length(가변길이)
                      / Data / Secondary(Dictionary/Index) 4개 스트림
```

### 3. 핵심 인코딩 & 압축 파이프라인

Parquet와 ORC 모두 **인코딩(Encoding) -> 압축(Compression)** 2단계 파이프라인을 사용한다. 인코딩은 데이터의 표현을 최적화하고, 압축은 비트 패턴의 중복을 제거한다.

| 인코딩 | 원리 | 적용 대상 | 효과 |
|:---|:---|:---|:---|
| **PLAIN** | 무인코딩 (4/8-byte 고정) | 모든 타입 (
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 290 / 300

<- **이전**: [289. 스키마 진화 호환성 레지스트리 관리 (Schema Evolution Compatibility Registry)](/studynote/14_data_engineering/05_exam_keywords/289_schema_evolution/)
**다음**: [291. 아이스버그 후디 델타 레이크 테이블 형식 (Iceberg Hudi Delta Lake Table Format)](/studynote/14_data_engineering/05_exam_keywords/291_iceberg_hudi_delta/) ->

---
