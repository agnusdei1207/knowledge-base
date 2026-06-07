---
title: "Columnar Storage Compression"
date: "2026-04-21"
tags:
  - "studynote-enterprise-systems"
weight: 311
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 컬럼 지향 저장([Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/), ORC)은 동일 컬럼 값을 연속 저장해 [RLE](/studynote/08_algorithm_stats/05_string/099_rle/) (Run-Length Encoding)와 사전 인코딩이 극적인 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 효율(10배 이상)을 달성한다.
> 2. **가치**: Predicate Pushdown과 Column Pruning으로 필요한 컬럼·행만 I/O해 Spark/[Hive](/studynote/05_database/04_transactions_concurrency/544_hive/) [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 비용을 최대 90%까지 절감한다.
> 3. **판단 포인트**: 행 삽입·수정이 잦은 OLTP는 여전히 행 지향 저장이 적합하고, [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)/ORC는 읽기 집중 [OLAP](/studynote/12_it_management/05_security_compliance/316_olap/)/빅데이터 분석에 최적화된다.

## Ⅰ. 개요 및 필요성

전통 행 지향 저장(Row-based)은 한 행의 모든 컬럼을 연속 저장해 레코드 삽입·수정에 유리하다.
반면 분석 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)는 수백 개 컬럼 중 3~5개만 읽는 경우가 대부분이므로, 불필요한 컬럼까지 모두 읽는 I/O 낭비가 발생한다.

컬럼 지향 저장([Columnar Storage](/studynote/13_cloud_architecture/05_data_engineering/234_columnar_storage_parquet_orc/))은 동일 컬럼 값을 연속 배치해:
1. 필요한 컬럼만 선택적으로 읽는 Column [Pruning](/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/) 가능
2. 같은 타입 값이 연속되어 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 효율 극대화
3. Predicate Pushdown으로 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수준에서 스캔 대상 행 그룹 제외

Apache [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) (Cloudera+Twitter 개발)와 Apache ORC ([Hive](/studynote/05_database/04_transactions_concurrency/544_hive/) 최적화)가 양대 표준이다.

📢 **섹션 요약 비유**: 컬럼 저장은 같은 색 구슬을 한 통에 모아 담는 것이다. "빨간 구슬만 주세요"라는 요청에 빨간 통만 열면 된다.

## Ⅱ. 아키텍처 및 핵심 원리

### [RLE](/studynote/08_algorithm_stats/05_string/099_rle/) (Run-Length Encoding) 메커니즘

```
원본: [A, A, A, A, B, B, C, C, C, C, C]  (11 bytes)
RLE:  [(A,4), (B,2), (C,5)]              (3 pairs -> 73% 압축)
```

저카디널리티 컬럼(성별: M/F, 상태: [ACTIVE](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)/INACTIVE)에서 효율 극대화.

사전 인코딩 (Dictionary Encoding):
```
원본: ["Seoul", "Seoul", "Busan", "Seoul", "Daegu"]
사전: {Seoul:0, Busan:1, Daegu:2}
인코딩: [0, 0, 1, 0, 2]  (int 저장 = 4~8배 절감)
```

### [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 코덱 비교

| 코덱 | [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)비 | [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 속도 | [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 해제 속도 | 적합 용도 |
|:---|:---|:---|:---|:---|
| Snappy | 2~3x | 매우 빠름 | 매우 빠름 | 스트리밍, 중간 결과 |
| ZSTD | 4~7x | 빠름 | 빠름 | 프로덕션 장기 보관 |
| GZIP | 5~8x | 느림 | 중간 | 아카이브 |
| LZ4 | 2~3x | [초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) | [초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) | 실시간 처리 |

### [ASCII](/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램: 행 지향 vs 컬럼 지향 저장 레이아웃

```
  행 지향 저장 (Row-based: CSV, JSON)
  +------------------------------------------------------------+
  | Row1: [id=1, name="Kim", age=30, city="Seoul", sal=5000]  |
  | Row2: [id=2, name="Lee", age=25, city="Busan", sal=4500]  |
  | Row3: [id=3, name="Park",age=35, city="Seoul", sal=6000]  |
  +------------------------------------------------------------+
  -> "age 평균" 쿼리 시 불필요한 name, city, salary도 모두 읽음

  컬럼 지향 저장 (Parquet / ORC)
  +---------+----------------+-----------+----------+----------+
  | id 컬럼 |   name 컬럼    | age 컬럼  |city 컬럼 | sal 컬럼 |
  | [1,2,3] |["Kim","Lee",..]|[30,25,35] |[S,B,S]   |[5000,...] |
  | RLE/Dict| Dict Encoding  | Delta     | RLE      | Delta    |
  +---------+----------------+-----------+----------+----------+
  -> "age 평균" 쿼리 시 age 컬럼만 읽음 (I/O 80% 절감)
```

### [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) Row Group vs ORC Stripe

| 항목 | [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) | ORC |
|:---|:---|:---|
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록 단위 | Row Group (기본 128MB) | Stripe (기본 64MB) |
| 통계 저장 | [Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Header (min/max) | Stripe Footer |
| 최적화 대상 | Spark, Flink, Presto | [Hive](/studynote/05_database/04_transactions_concurrency/544_hive/), ORC-vectorized |

📢 **섹션 요약 비유**: [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) Row Group은 챕터별로 정리된 책이다. 원하는 챕터(Row Group)만 열면 필요 없는 다른 챕터는 읽지 않아도 된다.

## Ⅲ. 비교 및 연결

### 컬럼 저장 vs 행 저장 사용 기준

| 기준 | 행 저장 (CSV, Avro) | 컬럼 저장 ([Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/), ORC) |
|:---|:---|:---|
| 워크로드 | INSERT/UPDATE 집중 | [SELECT](/studynote/05_database/04_transactions_concurrency/520_select/)/SCAN 집중 |
| 조회 패턴 | 전체 컬럼 필요 | 일부 컬럼만 필요 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 규모 | 수GB 이하 | 수TB 이상 |

📢 **섹션 요약 비유**: 행 저장은 손님 한 명의 모든 정보를 한 카드에, 컬럼 저장은 "나이" 정보만 따로 모아둔 서랍이다.

## Ⅳ. 실무 적용 및 기술사 판단

### [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) 최적화 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] Row Group 크기: 128MB (기본값) 유지
- [ ] 코덱 선택: 읽기 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 우선이면 Snappy, 저장 비용 우선이면 ZSTD
- [ ] [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) 컬럼: 날짜·카테고리 등 저카디널리티
- [ ] Column Stats 수집: min/max 통계로 Predicate Pushdown 극대화
- [ ] [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)당 최소 128MB 이상 권장 (Small [File](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 문제 방지)

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

| [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) | 문제 | 해결 방법 |
|:---|:---|:---|
| 고카디널리티 [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) | 수백만 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) -> [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 폭발 | 날짜·카테고리 등으로 제한 |
| GZIP on Spark | [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 해제 불가 -> [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 | Snappy 또는 ZSTD 권장 |

📢 **섹션 요약 비유**: 고카디널리티 [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/)은 사람마다 서랍을 만드는 것이다. 서랍이 백만 개가 되면 서랍장 자체가 무너진다.

## Ⅴ. 기대효과 및 결론

| 항목 | CSV (행 저장) | [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) (컬럼 저장) |
|:---|:---|:---|
| 스토리지 | 100% | [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~30% (10배 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)) |
| 컬럼 선택 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) I/O | 100% | [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~20% (Column [Pruning](/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)) |
| Spark [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 비용 | 기준 | 70~90% 절감 |

📢 **섹션 요약 비유**: Parquet는 분석 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 위한 전용 창고다. 창고 정리에 시간이 들지만, 필요한 물건을 찾는 속도가 10배 빠르다.

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) | 포맷 | 컬럼 지향 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 포맷 |
| ORC | 포맷 | [Hive](/studynote/05_database/04_transactions_concurrency/544_hive/) 최적화 컬럼 포맷 |
| [RLE](/studynote/08_algorithm_stats/05_string/099_rle/) | [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 기법 | 반복값 (값, 횟수) [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) |
| Predicate Pushdown | 최적화 | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수준 조건 필터링 |
| Column [Pruning](/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/) | 최적화 | 필요 컬럼만 I/O |
| Row Group | 구조 단위 | [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록 128MB |

### 📈 관련 키워드 및 발전 흐름도

```
행 기반 저장 (CSV, JSON) - 분석 쿼리 불필요 I/O
    |
    v
컬럼 기반 저장 (Parquet, ORC) - 컬럼 선택 I/O 최소화
    |
    v
RLE (Run-Length Encoding) + Dictionary 압축
    |
    v
Predicate Pushdown + Column Pruning 쿼리 최적화
    |
    v
Delta Lake/Iceberg - 오픈 테이블 포맷으로 진화
```

> **키워드**: [Parquet](/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/), ORC, [RLE](/studynote/08_algorithm_stats/05_string/099_rle/), [Columnar Storage](/studynote/13_cloud_architecture/05_data_engineering/234_columnar_storage_parquet_orc/), Predicate Pushdown, Snappy, Zstandard, [Data Lakehouse](/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/)

### 👶 어린이를 위한 3줄 비유 설명

1. Parquet는 색깔별로 구슬을 통에 모아 담은 것이에요. 빨간 구슬만 필요하면 빨간 통만 열어요.
2. RLE는 "빨강 100개"를 "빨강×100"으로 짧게 쓰는 방법이에요.
3. Predicate Pushdown은 "서울 사람만 필요해"라고 미리 말하면 서울 통만 열어주는 스마트 창고 직원이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 311 / 482

<- **이전**: [310. 그래프 데이터베이스 Neo4j 사기 탐지 최단 경로 (Neo4j Fraud Detection)](/studynote/07_enterprise_systems/05_data_bi/310_neo4j_fraud_detection/)
**다음**: [312. 해시 샤딩 및 디렉토리 샤딩 분산 DB 스케일 아웃 (Hash Sharding vs Directory Sharding)](/studynote/07_enterprise_systems/05_data_bi/312_hash_sharding_directory_sharding/) ->

---
