+++
title = "186. 데이터 컴프레션 전략 (Data Compression Strategy) — Snappy/Zstd/Gzip"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)

- [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 선택은 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률([Compression](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/159_compression/) Ratio)과 속도([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))의 트레이드오프이며, 빅데이터 환경에서 I/O 비용이 CPU 비용보다 클 때 높은 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률이 전체 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 향상시킨다.
- Snappy는 속도 우선([Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 기본), Gzip은 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률 우선([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)), LZ4는 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 실시간 스트리밍, Zstd는 속도와 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률을 모두 잡는 현재 최선의 범용 선택이다.
- 컬럼형 포맷([Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)/ORC)에서 [RLE](/knowledge-base/studynote/08_algorithm_stats/05_string/099_rle/) (Run-Length Encoding)과 딕셔너리 인코딩이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 특성 기반 고압축을 실현하며, 이는 일반 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 코덱보다 훨씬 효율적이다.

---

## Ⅰ. 개요 및 필요성

### 1-1. [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)이 빅데이터에서 중요한 이유

- **스토리지 비용**: S3/[HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) 저장 비용 직접 절감
- <strong>I/O <a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a></strong>: 디스크 읽기·네트워크 전송 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 감소 → [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 속도 향상
- **CPU vs I/O 균형**: I/O 병목 환경에서 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) CPU 비용 < I/O 절감 효과

### 1-2. [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 선택 기준

| 기준 | 우선 고려 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
|:---|:---|
| 최고 속도 (실시간 스트리밍) | LZ4 |
| 최고 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률 (아카이빙) | Gzip level 9, Brotli, LZMA |
| 속도 + [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률 균형 (범용) | Zstd |
| [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 전통 환경 | Snappy |
| [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 웹 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) | Gzip, Brotli |

> 📢 **섹션 요약 비유**: [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 선택은 짐을 꾸릴 때의 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 같다. 빠른 출발(실시간)이 중요하면 대충 넣고, 장기 보관(아카이빙)이라면 꼼꼼히 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교

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

### 2-2. 주요 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 상세

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 속도 | 해제 속도 | [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률 | 특징 |
|:---|:---|:---|:---|:---|
| **LZ4** | 500 MB/s | 1700 MB/s | 낮음 | [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/), 실시간 스트리밍 |
| **Snappy** | 250 MB/s | 500 MB/s | 중간 | [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 기본, 속도 중시 |
| **Zstd** | 400 MB/s | 1600 MB/s | 높음 | 속도+[압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률 균형, 레벨 조절 |
| **Gzip** | 30 MB/s | 200 MB/s | 높음 | [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 표준, CPU 부하 큼 |
| **Brotli** | 5 MB/s | 300 MB/s | 매우 높음 | 정적 웹 콘텐츠 아카이빙 |

### 2-3. 컬럼형 인코딩 (Columnar Encoding)

[Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)/ORC에서 사용하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 특성 기반 인코딩:

| 인코딩 | 원리 | 최적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 특성 |
|:---|:---|:---|
| **Dictionary Encoding** | 반복 값을 정수 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)로 치환 | 저카디널리티 (국가, 카테고리) |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/05_string/099_rle/">RLE</a> (Run-Length Encoding)</strong> | 연속 반복 값을 (값, 횟수) 쌍으로 | 정렬된 컬럼, 연속 동일 값 |
| <strong><a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/329_delta_encoding/">Delta Encoding</a></strong> | 연속 값의 차이를 저장 | 단조 증가 (타임스탬프, ID) |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/">Bit</a> Packing</strong> | 작은 정수를 최소 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)로 저장 | 작은 숫자 범위 |

> 📢 **섹션 요약 비유**: Dictionary Encoding은 반복되는 단어를 번호로 대체하는 속기술처럼, "대한민국"이 1000번 나오면 숫자 1로 저장해 공간을 절약한다.

---

## Ⅲ. 비교 및 연결

### Parquet에서의 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 효과

| 원본 (CSV) | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) (Snappy) | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) (Zstd) | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) (Gzip) |
|:---|:---|:---|:---|
| 100 GB | ~15 GB (85% 절감) | ~[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) GB (90% 절감) | ~8 GB (92% 절감) |
| 스캔 속도 | 빠름 | 빠름 | 느림 |

컬럼형 포맷 자체의 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 효과 + 추가 코덱 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)의 시너지

### 스트리밍 vs 배치 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 선택

- <strong><a href="/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/">Kafka</a> <a href="/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/">메시</a>지</strong>: LZ4 (Producer [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/), Broker 저장, Consumer 해제)
- <strong>Spark <a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/">배치 처리</a></strong>: Snappy 또는 Zstd (중간 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))
- **S3 아카이빙**: Gzip 또는 Zstd (장기 보관)
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 이관</strong>: Zstd (속도+[압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률 균형)

> 📢 **섹션 요약 비유**: 스트리밍에 LZ4를 쓰는 건 빠르게 서류를 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 꽂는 것이고, 아카이빙에 Gzip을 쓰는 건 진공포장기로 꼼꼼히 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해 보관하는 것이다.

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

[Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)/Spark에서 대용량 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 여러 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)로 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리되려면 분할 가능해야 한다.

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | Splittable |
|:---|:---:|
| Snappy ([raw](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/)) | ❌ |
| Gzip | ❌ |
| <strong>Snappy (within <a href="/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/">Parquet</a>/ORC)</strong> | ✅ ([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 포맷 레벨에서 분할) |
| bzip2 | ✅ |
| LZO + [Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | ✅ |

컬럼형 포맷([Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)/ORC)을 사용하면 비분할 코덱(Snappy, Gzip)도 Row Group 단위로 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 가능.

### 4-3. 기술사 시험 포인트

- [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 선택 근거: I/O 병목 환경 → 높은 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률 우선, CPU 병목 → 빠른 코덱 우선
- [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) + Zstd: 현재 빅데이터 표준 권장 조합
- Snappy가 여전히 사용되는 이유: [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 레거시 환경, LZO 대안

> 📢 **섹션 요약 비유**: Splittability는 긴 서류를 여러 사람이 동시에 읽을 수 있도록 챕터별로 분리된 것처럼, [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 여러 서버가 동시에 처리할 수 있는 분할 능력이다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 스토리지 비용 | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) + Zstd로 CSV 대비 85~92% 절감 |
| [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 스캔 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 감소로 Athena/[BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 속도 2~5배 향상 |
| 네트워크 비용 | 이그레스 [데이터 압축](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/159_compression/)으로 클라우드 전송 비용 절감 |

[압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 비용·[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 양면에서 큰 효과를 내는 고효율 최적화다. 기술사 관점에서 [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) 설계 시 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 포맷과 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 코덱을 함께 명시하고, 워크로드 유형별 최적 조합을 권장해야 한다.

> 📢 **섹션 요약 비유**: 올바른 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 물건을 테트리스처럼 빈틈없이 쌓아 이사 트럭 횟수를 줄이는 것처럼, 같은 양의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 적은 비용으로 저장하고 전송한다.

---

### 📌 관련 개념 맵

| 개념 | 관련 기술 | 연결 포인트 |
|:---|:---|:---|
| [RLE](/knowledge-base/studynote/08_algorithm_stats/05_string/099_rle/) | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/), ORC | 컬럼형 인코딩 |
| Dictionary Encoding | 저카디널리티 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 반복값 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) |
| Splittability | [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/), Spark | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 가능성 |
| I/O vs CPU 병목 | 하드웨어 최적화 | 코덱 선택 기준 |
| Zstd Level | [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 튜닝 | 워크로드별 최적화 |

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

이 흐름은 손실 없이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 줄이는 기본 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)에서 시작해, 컬럼형·사전·[RLE](/knowledge-base/studynote/08_algorithm_stats/05_string/099_rle/) 기법을 거쳐 클라우드 자동 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)으로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [데이터 압축](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/159_compression/)은 여행 가방 짐을 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 봉투에 넣어 작게 만드는 것처럼, 같은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 더 작게 저장해서 공간을 아껴요.
2. 빨리 꺼내야 하면 LZ4처럼 느슨하게 넣고, 오래 보관할 거면 Gzip처럼 꼭꼭 눌러 넣어요.
3. [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 같은 종류의 물건끼리 모아 넣어서 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)이 훨씬 잘 되는 특수한 가방이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 186 / 262

← **이전**: [185. 확장성 설계 (Scalability Design) — 수평 확장/샤딩/파티셔닝/자동 확장](/knowledge-base/studynote/16_bigdata/09_platform/185_scalability_design/)
**다음**: [187. 컬럼 기반 파일 포맷 (Parquet, ORC, Iceberg, Arrow) 조회 최적화](/knowledge-base/studynote/16_bigdata/09_platform/187_parquet_orc_iceberg_arrow/) →

---
