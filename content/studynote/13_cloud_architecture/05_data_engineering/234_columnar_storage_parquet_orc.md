+++
title = "234. 컬럼 지향 스토리지 (Columnar Storage) - Parquet / ORC"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 컬럼 지향 스토리지(Columnar Storage)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 <strong>행(Row) 단위가 아닌 열(Column) 단위로 <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a> 저장</strong>하여 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 분석 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 시 필요한 열만 읽어 I/O를 극적으로 절감한다.
> 2. **가치**: 동일 열의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 타입이 동일하므로 <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a>률이 5~10배 높고</strong>, 특정 열만 선택적으로 읽는 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)에서 로우 기반 대비 수십 배 빠른 스캔 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 발휘한다.
> 3. **판단 포인트**: Apache Parquet은 범용 컬럼 포맷, Apache ORC는 [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/)/Spark 최적화 포맷으로, [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)·레이크하우스의 <strong>표준 저장 포맷</strong>으로 반드시 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

전통 RDBMS는 한 행의 모든 컬럼을 디스크에 연속 저장한다(Row-oriented). INSERT/UPDATE [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)에는 효율적이지만, "전체 주문 중 매출 금액 합계"처럼 특정 컬럼만 읽는 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)에서는 불필요한 컬럼까지 전부 읽어야 하는 I/O 낭비가 발생한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Row-oriented 저장</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Row 1:</div><div class="kb-diagram-node">order_id=1</div><div class="kb-diagram-node">customer_id=C001</div><div class="kb-diagram-node">product="책"</div><div class="kb-diagram-node">amount=30000</div><div class="kb-diagram-node">date=2024-01-01</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Row 2:</div><div class="kb-diagram-node">order_id=2</div><div class="kb-diagram-node">customer_id=C002</div><div class="kb-diagram-node">product="노트북"</div><div class="kb-diagram-node">amount=1500000</div><div class="kb-diagram-node">date=2024-01-02</div></div>
<div class="kb-diagram-note">...</div>
<div class="kb-diagram-note">SELECT SUM(amount) FROM orders; → 모든 행의 모든 컬럼을 읽어야 함</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Column-oriented 저장</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">order_id:</div><div class="kb-diagram-node">1</div><div class="kb-diagram-node">2</div><div class="kb-diagram-node">3</div><div class="kb-diagram-node">4</div><div class="kb-diagram-note">...</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">customer_id:</div><div class="kb-diagram-node">C001</div><div class="kb-diagram-node">C002</div><div class="kb-diagram-node">C003</div><div class="kb-diagram-note">...</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">product:</div><div class="kb-diagram-node">책</div><div class="kb-diagram-node">노트북</div><div class="kb-diagram-node">마우스</div><div class="kb-diagram-note">...</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">amount:</div><div class="kb-diagram-node">30000</div><div class="kb-diagram-node">1500000</div><div class="kb-diagram-node">25000</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">이것만 읽음!</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">date:</div><div class="kb-diagram-node">2024-01-01</div><div class="kb-diagram-node">2024-01-02</div><div class="kb-diagram-note">...</div></div>
<div class="kb-diagram-note">SELECT SUM(amount) FROM orders; → amount 컬럼 파일만 읽음 (I/O 95% 절감)</div>
</div>
</div>



📢 **섹션 요약 비유**: Row-oriented는 엑셀 시트를 행 단위로 저장하는 것이고, Column-oriented는 같은 항목(열)끼리 묶어서 저장하는 것이다. "전체 직원 연봉 합계"를 구할 때, 연봉 열 하나만 꺼내면 되니 훨씬 빠르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Apache [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Parquet 파일 구조</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Magic Number (4 bytes)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Row Group 1 (행 그룹, 예: 128MB)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Column Chunk 1 (order_id)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- Data Pages (RLE+Dictionary 인코딩)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- Column Statistics (min/max/null cnt)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Column Chunk 2 (amount)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- Data Pages</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- Column Statistics</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Row Group 2 ...</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">File Footer (스키마, Row Group 위치, 통계)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Magic Number (4 bytes)</div></div>
</div>
</div>



### [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 및 인코딩 최적화

| 최적화 기법 | 설명 | 효과 |
|:---|:---|:---|
| **Dictionary Encoding** | 반복 값을 정수 ID로 치환 | 문자열 컬럼 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 우수 |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/05_string/099_rle/">RLE</a> (Run-Length Encoding)</strong> | 연속 동일 값 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) | 정렬된 컬럼 효율적 |
| <strong><a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/329_delta_encoding/">Delta Encoding</a></strong> | 이전 값과의 차이만 저장 | 타임스탬프, 순차 ID |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/">Bit</a> Packing</strong> | 필요 최소 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수로 저장 | 정수 범위 최적화 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a> 코덱</strong> | Snappy, Zstd, Gzip | Snappy: 속도↑, Zstd: [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률↑ |

### Predicate Pushdown (조건 푸시다운)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SELECT * FROM orders WHERE amount &gt; 1000000</div>
<div class="kb-diagram-note">Parquet 엔진 동작:</div>
<div class="kb-diagram-note">1. File Footer에서 Row Group 통계 확인</div>
<div class="kb-diagram-note">2. Row Group 2: amount max=500000 → amount &gt; 1000000 없음 → 스킵!</div>
<div class="kb-diagram-note">3. Row Group 5: amount max=3000000 → 조건 가능성 → 읽기</div>
<div class="kb-diagram-note">효과: 전체 파일의 70~90% 읽지 않고 건너뜀</div>
</div>
</div>



📢 **섹션 요약 비유**: Predicate Pushdown은 책 목차(Footer 통계)를 먼저 보고, 관련 없는 챕터는 넘기는 것이다. "200페이지 이후 내용만 필요하다"면 목차에서 바로 200페이지로 이동하듯, 통계로 불필요한 Row Group을 건너뛴다.

---

## Ⅲ. 비교 및 연결

### [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) vs ORC vs Avro vs CSV

| 비교 항목 | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) | ORC | Avro | CSV |
|:---|:---|:---|:---|:---|
| **저장 방식** | 컬럼 지향 | 컬럼 지향 | 행 지향 | 행 지향 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a>률</strong> | 높음 | 높음 | 중간 | 낮음 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/">OLAP</a> <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a></strong> | 우수 | 우수 | 보통 | 나쁨 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | 보통 | 보통 | 우수 | 우수 |
| **스트리밍** | 제한 | 제한 | 우수 | 우수 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a> 진화</strong> | 제한 | 제한 | 우수 | 없음 |
| **생태계** | 범용 (Spark, [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/), Presto) | [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/)/ORC 최적 | [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) | 범용 |
| **적합 사례** | [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) | [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) | 스트리밍 직렬화 | 소규모 교환 |

### [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 포맷 선택 기준

```
[워크로드별 포맷 선택]
OLAP 분석 (읽기 중심):  Parquet > ORC >> Avro > CSV
스트리밍 이벤트 직렬화: Avro (Protobuf) >> Parquet
레이크하우스 테이블:    Parquet (Delta Lake / Iceberg)
Hive DW:               ORC (Hive 네이티브 최적화)
데이터 교환:            Parquet > CSV
ML 피처 스토어:         Parquet (Feast 등)
```

📢 **섹션 요약 비유**: 포맷 선택은 짐을 싸는 방식이다. 여행 캐리어([Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)/ORC)는 체계적으로 정리해 공간 절약, 긴급 배낭(Avro)은 빠르게 넣고 빼기, 비닐백(CSV)은 단순하지만 비효율이다. 분석 여행([OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/))엔 캐리어, 마라톤(스트리밍)엔 배낭이 맞다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) 최적화 실무 가이드

```python
# Spark에서 Parquet 최적화 저장
df.write \
  .partitionBy("date", "region")  # 파티션 분할 (쿼리 범위 축소)
  .option("compression", "zstd")  # Zstandard 압축 (압축률+속도 균형)
  .option("maxRecordsPerFile", 1000000)  # Row Group 크기 조절
  .mode("overwrite") \
  .parquet("s3://bucket/silver/orders/")

# 읽기 최적화
spark.conf.set("spark.sql.parquet.filterPushdown", "true")
spark.conf.set("spark.sql.parquet.mergeSchema", "false")
df = spark.read.parquet("s3://bucket/silver/orders/") \
     .filter(col("date") >= "2024-01-01") \  # Predicate Pushdown
     .select("order_id", "amount", "status")  # Column Pruning
```

### [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">파티셔닝 설계 예시</div></div>
<div class="kb-diagram-note">s3://bucket/orders/</div>
<div class="kb-diagram-tree-item" style="--depth:0">year=2024/month=01/day=01/part-00000.parquet</div>
<div class="kb-diagram-tree-item" style="--depth:0">year=2024/month=01/day=02/part-00000.parquet</div>
<div class="kb-diagram-note">...</div>
<div class="kb-diagram-note">쿼리: WHERE date = '2024-01-15'</div>
<div class="kb-diagram-note">→ year=2024/month=01/day=15/ 폴더만 읽음 (나머지 99% 스킵)</div>
<div class="kb-diagram-note">주의: 파티션 과세분화 (너무 많은 소형 파일) 방지</div>
<div class="kb-diagram-note">적정 파일 크기: 128MB ~ 512MB</div>
</div>
</div>



📢 **섹션 요약 비유**: [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)은 서류함에 날짜별로 구분자(탭)를 꽂아두는 것이다. 1월 15일 서류만 필요하면 전체를 뒤지지 않고 "1월 탭" 안에서 "15일 탭"을 바로 꺼낼 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 정량 기준 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a>률</strong> | CSV 대비 5~10배 저장 공간 절감 |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> 속도</strong> | Row 기반 대비 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 5~50배 빠름 |
| **I/O 절감** | Column [Pruning](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/) + Predicate Pushdown으로 90%+ I/O 절감 |
| **스토리지 비용** | S3 비용 50~80% 절감 (CSV → [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) 전환) |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | Row 기반 대비 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 속도 느림 (컬럼 재조합 비용) |
| <strong>소형 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 문제</strong> | 소규모 배치 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 시 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수 폭발 (OPTIMIZE 필요) |
| **스트리밍 직렬화 불리** | 이벤트 단위 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)에는 Avro/Protobuf 선호 |
| **실시간 행 업데이트 어려움** | 컬럼 지향 특성 상 단건 UPDATE 비효율 |

📢 **섹션 요약 비유**: Parquet은 연필 케이스다. 연필([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 종류별(컬럼별)로 정렬해 넣으면 꺼낼 때 빠르고 공간도 절약된다. 단, 처음 정리하는 시간([쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 비용)이 필요하고, 연필 한 자루씩 추가하는 것(단건 업데이트)은 번거롭다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) | 컬럼 지향 스토리지가 가장 큰 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 이점을 발휘하는 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 패턴 |
| [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)/ORC가 표준 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 포맷으로 사용되는 저장소 |
| [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) / Iceberg | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) 위에 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 레이어를 추가한 테이블 포맷 |
| Predicate Pushdown | 컬럼 통계 기반 읽기 스킵으로 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화 |
| [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) 읽기·[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 최적화의 핵심 엔진 |
| [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) | 컬럼 지향 포맷과 결합하여 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 범위 최소화 |
| Avro | 스트리밍 직렬화용 행 지향 포맷, [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) |

### 👶 어린이를 위한 3줄 비유 설명
1. 컬럼 지향 저장은 학용품을 종류별로 보관하는 것이다. 연필통에는 연필만, 자 통에는 자만 넣으면, "연필 몇 개야?"라고 물을 때 연필통만 열면 된다.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">행 지향 (Row): OLTP 최적화 (INSERT/UPDATE 빠름)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">컬럼 지향 (Columnar): OLAP 최적화 (집계 쿼리 빠름)</div>
<div class="kb-diagram-tree-item" style="--depth:2">Parquet · ORC: 파일 포맷</div>
<div class="kb-diagram-tree-item" style="--depth:2">압축률 ↑: 같은 타입 데이터 연속 저장</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">벡터화 실행: SIMD · Arrow 인메모리 포맷</div>
</div>
</div>


2. Parquet은 잘 정리된 서랍장이다. 각 서랍에 같은 종류의 물건이 빽빽이 정리되어([압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)), 필요한 서랍만 열어도(컬럼 선택) 원하는 걸 빠르게 찾을 수 있다.
3. CSV는 모든 물건을 큰 상자에 섞어 넣은 것이다. 단순하지만, 연필을 찾으려면 상자 전체를 뒤져야 해서 시간이 오래 걸린다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 233 / 371

← **이전**: [233. 아파치 에어플로우 (Apache Airflow)](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/233_apache_airflow_dag_orchestration/)
**다음**: [235. 분산 NoSQL 데이터베이스 종류 개요](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/235_nosql_database_types_overview/) →

---
