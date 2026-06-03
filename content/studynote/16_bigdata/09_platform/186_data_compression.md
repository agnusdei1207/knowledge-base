---
title: 186. 데이터 컴프레션 전략 (Data Compression Strategy) — Snappy/Zstd/Gzip
date: '2026-04-21'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)

- [[347_compaction|압축]] [[001_algorithm_definition|알고리즘]] 선택은 [[347_compaction|압축]]률([[159_compression|Compression]] Ratio)과 속도([[139_throughput|Throughput]])의 트레이드오프이며, 빅데이터 환경에서 I/O 비용이 CPU 비용보다 클 때 높은 [[347_compaction|압축]]률이 전체 [[282_performance_tactics|성능]]을 향상시킨다.
- Snappy는 속도 우선([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 기본), Gzip은 [[347_compaction|압축]]률 우선([[461_http_stateless_connection_oriented|HTTP]]), LZ4는 [[148_5g_embb_urllc_mmtc|초고속]] 실시간 스트리밍, Zstd는 속도와 [[347_compaction|압축]]률을 모두 잡는 현재 최선의 범용 선택이다.
- 컬럼형 포맷([[178_parquet_rle_encoding_columnar_compression|Parquet]]/ORC)에서 [[099_rle|RLE]] (Run-Length Encoding)과 딕셔너리 인코딩이 [[001_dikw_pyramid|데이터]] 특성 기반 고압축을 실현하며, 이는 일반 [[347_compaction|압축]] 코덱보다 훨씬 효율적이다.

---

## Ⅰ. 개요 및 필요성

### 1-1. [[347_compaction|압축]]이 빅데이터에서 중요한 이유

- **스토리지 비용**: S3/[[013_hdfs|HDFS]] 저장 비용 직접 절감
- **I/O [[139_throughput|처리량]]**: 디스크 읽기·네트워크 전송 [[001_dikw_pyramid|데이터]] 감소 → [[298_qkv_attention|쿼리]] 속도 향상
- **CPU vs I/O 균형**: I/O 병목 환경에서 [[347_compaction|압축]] CPU 비용 < I/O 절감 효과

### 1-2. [[347_compaction|압축]] [[001_algorithm_definition|알고리즘]] 선택 기준

| 기준 | 우선 고려 [[001_algorithm_definition|알고리즘]] |
|:---|:---|
| 최고 속도 (실시간 스트리밍) | LZ4 |
| 최고 [[347_compaction|압축]]률 (아카이빙) | Gzip level 9, Brotli, LZMA |
| 속도 + [[347_compaction|압축]]률 균형 (범용) | Zstd |
| [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 전통 환경 | Snappy |
| [[461_http_stateless_connection_oriented|HTTP]] 웹 [[347_compaction|압축]] | Gzip, Brotli |

> 📢 **섹션 요약 비유**: [[347_compaction|압축]] [[001_algorithm_definition|알고리즘]] 선택은 짐을 꾸릴 때의 [[268_strategy_pattern|전략]]과 같다. 빠른 출발(실시간)이 중요하면 대충 넣고, 장기 보관(아카이빙)이라면 꼼꼼히 [[347_compaction|압축]]한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. [[347_compaction|압축]] [[001_algorithm_definition|알고리즘]] [[282_performance_tactics|성능]] 비교

```
압축률      ┤                                    Brotli
            │                                 ●
높음        │                           Gzip ●
            │                       Zstd ●
            │               Snappy ●
낮음        │       LZ4 ●
            └────────────────────────────────────────▶
                  빠름                           느림
                         압축/해제 속도
```

### 2-2. 주요 [[001_algorithm_definition|알고리즘]] 상세

| [[001_algorithm_definition|알고리즘]] | [[347_compaction|압축]] 속도 | 해제 속도 | [[347_compaction|압축]]률 | 특징 |
|:---|:---|:---|:---|:---|
| **LZ4** | 500 MB/s | 1700 MB/s | 낮음 | [[148_5g_embb_urllc_mmtc|초고속]], 실시간 스트리밍 |
| **Snappy** | 250 MB/s | 500 MB/s | 중간 | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 기본, 속도 중시 |
| **Zstd** | 400 MB/s | 1600 MB/s | 높음 | 속도+[[347_compaction|압축]]률 균형, 레벨 조절 |
| **Gzip** | 30 MB/s | 200 MB/s | 높음 | [[461_http_stateless_connection_oriented|HTTP]] 표준, CPU 부하 큼 |
| **Brotli** | 5 MB/s | 300 MB/s | 매우 높음 | 정적 웹 콘텐츠 아카이빙 |

### 2-3. 컬럼형 인코딩 (Columnar Encoding)

[[178_parquet_rle_encoding_columnar_compression|Parquet]]/ORC에서 사용하는 [[001_dikw_pyramid|데이터]] 특성 기반 인코딩:

| 인코딩 | 원리 | 최적 [[001_dikw_pyramid|데이터]] 특성 |
|:---|:---|:---|
| **Dictionary Encoding** | 반복 값을 정수 [[154_database_index_b_tree_search_optimization|인덱스]]로 치환 | 저카디널리티 (국가, 카테고리) |
| **[[099_rle|RLE]] (Run-Length Encoding)** | 연속 반복 값을 (값, 횟수) 쌍으로 | 정렬된 컬럼, 연속 동일 값 |
| **[[329_delta_encoding|Delta Encoding]]** | 연속 값의 차이를 저장 | 단조 증가 (타임스탬프, ID) |
| **[[086_fenwick_tree|Bit]] Packing** | 작은 정수를 최소 [[073_bit|비트]]로 저장 | 작은 숫자 범위 |

> 📢 **섹션 요약 비유**: Dictionary Encoding은 반복되는 단어를 번호로 대체하는 속기술처럼, "대한민국"이 1000번 나오면 숫자 1로 저장해 공간을 절약한다.

---

## Ⅲ. 비교 및 연결

### Parquet에서의 [[347_compaction|압축]] 효과

| 원본 (CSV) | [[178_parquet_rle_encoding_columnar_compression|Parquet]] (Snappy) | [[178_parquet_rle_encoding_columnar_compression|Parquet]] (Zstd) | [[178_parquet_rle_encoding_columnar_compression|Parquet]] (Gzip) |
|:---|:---|:---|:---|
| 100 GB | ~15 GB (85% 절감) | ~[[489_raid_10_hybrid|10]] GB (90% 절감) | ~8 GB (92% 절감) |
| 스캔 속도 | 빠름 | 빠름 | 느림 |

컬럼형 포맷 자체의 [[347_compaction|압축]] 효과 + 추가 코덱 [[347_compaction|압축]]의 시너지

### 스트리밍 vs 배치 [[347_compaction|압축]] 선택

- **[[179_kafka_flink_watermark_time_window|Kafka]] [[389_mesh_topology|메시]]지**: LZ4 (Producer [[347_compaction|압축]], Broker 저장, Consumer 해제)
- **Spark [[228_batch_processing_hadoop_spark|배치 처리]]**: Snappy 또는 Zstd (중간 [[501_file_definition_logical_record|파일]])
- **S3 아카이빙**: Gzip 또는 Zstd (장기 보관)
- **[[001_dikw_pyramid|데이터]] 이관**: Zstd (속도+[[347_compaction|압축]]률 균형)

> 📢 **섹션 요약 비유**: 스트리밍에 LZ4를 쓰는 건 빠르게 서류를 [[501_file_definition_logical_record|파일]]에 꽂는 것이고, 아카이빙에 Gzip을 쓰는 건 진공포장기로 꼼꼼히 [[347_compaction|압축]]해 보관하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. Zstd 채택 가이드

```
Zstd 레벨 1~22:
Level 1: LZ4와 유사한 속도, Snappy보다 나은 압축률 (일반 스트리밍)
Level 3: 기본값, 속도·압축률 균형 (범용 빅데이터)
Level 10-19: Gzip과 유사한 압축률, 더 빠른 해제 (아카이빙)
Level 20-22: 최고 압축률 (Cold Storage)
```

### 4-2. Splittability (분할 가능성)

[[843_hadoop_rack_awareness_data_replication_topology|Hadoop]]/Spark에서 대용량 [[347_compaction|압축]] [[501_file_definition_logical_record|파일]]이 여러 [[150_task|태스크]]로 [[430_index_fast_full_scan|병렬]] 처리되려면 분할 가능해야 한다.

| [[001_algorithm_definition|알고리즘]] | Splittable |
|:---|:---:|
| Snappy ([[225_raw|raw]]) | ❌ |
| Gzip | ❌ |
| **Snappy (within [[178_parquet_rle_encoding_columnar_compression|Parquet]]/ORC)** | ✅ ([[501_file_definition_logical_record|파일]] 포맷 레벨에서 분할) |
| bzip2 | ✅ |
| LZO + [[154_database_index_b_tree_search_optimization|Index]] | ✅ |

컬럼형 포맷([[178_parquet_rle_encoding_columnar_compression|Parquet]]/ORC)을 사용하면 비분할 코덱(Snappy, Gzip)도 Row Group 단위로 [[430_index_fast_full_scan|병렬]] 처리 가능.

### 4-3. 기술사 시험 포인트

- [[347_compaction|압축]] 선택 근거: I/O 병목 환경 → 높은 [[347_compaction|압축]]률 우선, CPU 병목 → 빠른 코덱 우선
- [[178_parquet_rle_encoding_columnar_compression|Parquet]] + Zstd: 현재 빅데이터 표준 권장 조합
- Snappy가 여전히 사용되는 이유: [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 레거시 환경, LZO 대안

> 📢 **섹션 요약 비유**: Splittability는 긴 서류를 여러 사람이 동시에 읽을 수 있도록 챕터별로 분리된 것처럼, [[347_compaction|압축]] [[501_file_definition_logical_record|파일]]을 여러 서버가 동시에 처리할 수 있는 분할 능력이다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 스토리지 비용 | [[178_parquet_rle_encoding_columnar_compression|Parquet]] + Zstd로 CSV 대비 85~92% 절감 |
| [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]] | 스캔 [[001_dikw_pyramid|데이터]] 감소로 Athena/[[263_storage_compute_separation_bigquery|BigQuery]] [[298_qkv_attention|쿼리]] 속도 2~5배 향상 |
| 네트워크 비용 | 이그레스 [[159_compression|데이터 압축]]으로 클라우드 전송 비용 절감 |

[[347_compaction|압축]] [[268_strategy_pattern|전략]]은 비용·[[282_performance_tactics|성능]]의 양면에서 큰 효과를 내는 고효율 최적화다. 기술사 관점에서 [[645_data_pipeline_acceleration|데이터 파이프라인]] 설계 시 [[501_file_definition_logical_record|파일]] 포맷과 [[347_compaction|압축]] 코덱을 함께 명시하고, 워크로드 유형별 최적 조합을 권장해야 한다.

> 📢 **섹션 요약 비유**: 올바른 [[347_compaction|압축]] [[268_strategy_pattern|전략]]은 물건을 테트리스처럼 빈틈없이 쌓아 이사 트럭 횟수를 줄이는 것처럼, 같은 양의 [[001_dikw_pyramid|데이터]]를 적은 비용으로 저장하고 전송한다.

---

### 📌 관련 개념 맵

| 개념 | 관련 기술 | 연결 포인트 |
|:---|:---|:---|
| [[099_rle|RLE]] | [[178_parquet_rle_encoding_columnar_compression|Parquet]], ORC | 컬럼형 인코딩 |
| Dictionary Encoding | 저카디널리티 [[001_dikw_pyramid|데이터]] | 반복값 [[347_compaction|압축]] |
| Splittability | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]], Spark | [[430_index_fast_full_scan|병렬]] 처리 가능성 |
| I/O vs CPU 병목 | 하드웨어 최적화 | 코덱 선택 기준 |
| Zstd Level | [[347_compaction|압축]] 튜닝 | 워크로드별 최적화 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[무손실 압축 (Lossless Compression) — Huffman/LZ77]
    │
    ▼
[컬럼형 압축 (Columnar Compression) — Parquet/ORC]
    │
    ▼
[사전 인코딩 (Dictionary Encoding) — 반복값 치환]
    │
    ▼
[런 길이 인코딩 (RLE, Run-Length Encoding) — 연속값 압축]
    │
    ▼
[스노우플레이크 자동 압축 (Snowflake Auto-Compression) — 클라우드 최적화]
```

이 흐름은 손실 없이 [[001_dikw_pyramid|데이터]]를 줄이는 기본 [[347_compaction|압축]]에서 시작해, 컬럼형·사전·[[099_rle|RLE]] 기법을 거쳐 클라우드 자동 [[347_compaction|압축]]으로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[159_compression|데이터 압축]]은 여행 가방 짐을 [[347_compaction|압축]] 봉투에 넣어 작게 만드는 것처럼, 같은 [[001_dikw_pyramid|데이터]]를 더 작게 저장해서 공간을 아껴요.
2. 빨리 꺼내야 하면 LZ4처럼 느슨하게 넣고, 오래 보관할 거면 Gzip처럼 꼭꼭 눌러 넣어요.
3. [[178_parquet_rle_encoding_columnar_compression|Parquet]] [[501_file_definition_logical_record|파일]]은 같은 종류의 물건끼리 모아 넣어서 [[347_compaction|압축]]이 훨씬 잘 되는 특수한 가방이에요.
