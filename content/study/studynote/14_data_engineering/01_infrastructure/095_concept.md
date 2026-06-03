+++
title = "#95 DataEng (데이터엔지니어링)概念"
description = "Study note #95 for DataEng (데이터엔지니어링)"
authors = ["Copilot"]
tags = ["14_data_engineering", "study", "education"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[001_dikw_pyramid|데이터]] 엔지니어링 인프라는 원시 [[001_dikw_pyramid|데이터]]를 수집, 저장, 정제하여 분석가와 [[190_ai_llm_requirements_specification|AI]] 모델이 즉시 활용할 수 있도록 파이프라인을 구축하는 기술적 토대다.
> 2. **가치**: [[001_dikw_pyramid|데이터]] 파편화([[002_silo_hyeonhyung|Silo]])를 해소하고 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]([[270_data_quality_great_expectations|Data Quality]])을 보장함으로써, 기업의 [[001_dikw_pyramid|데이터]] 기반 의사결정([[001_dikw_pyramid|Data]]-driven Decision) 속도를 극대화한다.
> 3. **판단 포인트**: 배치(Batch)와 스트리밍(Streaming) 방식의 선택은 비즈니스 요구 지연시간([[141_latency|Latency]])과 비용의 트레이드오프에 따라 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]] 엔지니어링 ([[001_dikw_pyramid|Data]] Engineering) 인프라는 다양한 소스(RDBMS, [[568_logs_distributed_logging_elk_fluentd|로그]], 외부 [[014_api_posix|API]] 등)에서 생성되는 대규모 [[001_dikw_pyramid|데이터]]를 추출(Extract), 변환(Transform), 적재(Load)하여 쓸모 있는 정보로 가공하는 시스템의 집합이다. 빅데이터 시대에 접어들며 [[001_dikw_pyramid|데이터]]의 볼륨([[001_bigdata_3v_5v|Volume]])과 속도(Velocity)가 폭증함에 따라, 단일 서버의 [[501_file_definition_logical_record|파일]] 시스템으로는 감당할 수 없는 한계에 직면했다.

만약 이 인프라가 제대로 구축되지 않으면, [[001_dikw_pyramid|데이터]] 과학자는 분석 모델을 훈련하기 전에 원시 [[001_dikw_pyramid|데이터]]를 정제하는 데 80% 이상의 시간을 낭비하게 된다. 따라서 안정적이고 확장 가능한 [[136_variance|분산]] 저장소와 자동화된 파이프라인 없이는 아무리 훌륭한 [[190_ai_llm_requirements_specification|AI]] 알고리즘도 무용지물이 된다.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 엔지니어링은 흙탕물(원시 [[001_dikw_pyramid|데이터]])을 끌어와 정수장(파이프라인)을 거쳐 각 가정의 수도꼭지(분석가)로 깨끗한 물을 안정적으로 보내는 거대한 상수도 공학이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

현대 [[001_dikw_pyramid|데이터]] 엔지니어링 인프라는 [[208_data_lake_schema_on_read|데이터 레이크]]([[208_data_lake_schema_on_read|Data Lake]])와 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]([[209_data_warehouse_schema_on_write|DW]], [[208_data_warehouse_schema_on_write_inmon|Data Warehouse]])를 중심으로 구축되며, 이들을 연결하는 파이프라인([[215_etl_vs_elt_pipeline|ETL]]/[[034_elt|ELT]]) 엔진으로 구성된다.

| 계층 | 주요 역할 | 대표 기술 [[057_stack|스택]] |
| :--- | :--- | :--- |
| **수집 (Ingestion)** | 실시간 스트리밍 및 배치 [[001_dikw_pyramid|데이터]] 추출 | [[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]], Logstash |
| **저장 (Storage)** | 정형/비정형 [[001_dikw_pyramid|데이터]]의 영구적 [[136_variance|분산]] 보관 | Amazon S3, [[013_hdfs|HDFS]] |
| **처리 (Processing)** | [[266_data_cleansing|데이터 정제]], 집계, [[005_schema|스키마]] 변환 연산 | [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]], Flink, dbt |
| **[[090_service_kubernetes_network_load_balancing|서비스]] (Serving)** | 최종 분석 및 BI 도구를 위한 [[298_qkv_attention|쿼리]] 엔진 | [[541_cassandra|Snowflake]], [[263_storage_compute_separation_bigquery|BigQuery]] |

```text
┌──────────────────────────────────────────────────────────────┐
│           데이터 흐름: 추출부터 서비스까지의 파이프라인      │
├──────────────────────────────────────────────────────────────┤
│ [Source DB] ─CDC─▶ [Kafka] ─▶ [Spark 연산] ─▶ [Cloud DW]   │
│ (Raw Data)       (실시간 수집)  (ETL 정제)      (BI/AI 연동)│
│                                                             │
│ * 핵심 병목: 정제 단계의 분산 컴퓨팅(Scale-out) 성능        │
└──────────────────────────────────────────────────────────────┘
```

최근에는 [[001_dikw_pyramid|데이터]]를 목적지까지 옮겨서 변환([[215_etl_vs_elt_pipeline|ETL]])하는 대신, 값싼 클라우드 스토리지에 무조건 적재(Load)한 뒤 강력한 클라우드 [[209_data_warehouse_schema_on_write|DW]] 내부의 연산력을 빌려 변환(Transform)하는 [[034_elt|ELT]] 아키텍처가 대세로 자리 잡았다.

- **📢 섹션 요약 비유**: 수집은 원자재를 광산에서 캐내는 것이고, 저장은 거대한 창고에 쌓아두는 것이며, 처리는 공장에서 쓸모 있는 제품으로 조립해 매장([[090_service_kubernetes_network_load_balancing|서비스]])에 진열하는 과정이다.

---

## Ⅲ. 비교 및 연결

[[001_dikw_pyramid|데이터]] 아키텍처의 철학은 [[208_data_lake_schema_on_read|데이터 레이크]]와 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]를 거쳐 [[210_data_lakehouse_delta_lake|데이터 레이크하우스]]로 진화하고 있다.

| 항목 | [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] ([[209_data_warehouse_schema_on_write|DW]]) | [[208_data_lake_schema_on_read|데이터 레이크]] ([[208_data_lake_schema_on_read|Data Lake]]) |
| :--- | :--- | :--- |
| **[[001_dikw_pyramid|데이터]] 형태** | [[002_structured_data|정형 데이터]] ([[010_schema_on_write|스키마 온 라이트]]) | 모든 [[001_dikw_pyramid|데이터]] ([[009_schema_on_read|스키마 온 리드]]) |
| **주요 목적** | BI 리포팅 및 과거 실적 분석 | [[241_machine_learning_basics|머신러닝]] 모델 훈련 및 원본 보존 |
| **저장 비용** | 상대적으로 고가 (컴퓨팅 결합형) | 매우 저렴 ([[494_object_storage|Object Storage]]) |

DW는 엄격한 구조로 인해 속도가 빠르지만 비싸고 유연성이 떨어지며, [[208_data_lake_schema_on_read|데이터 레이크]]는 저렴하지만 자칫 관리가 안 되면 [[288_data_swamp_metadata_management_absence|데이터 늪]]([[288_data_swamp_metadata_management_absence|Data Swamp]])으로 전락한다. 두 개념은 서로 경쟁하다가, 최근에는 레이크의 저비용 저장소 위에 DW의 [[191_transaction_concept_states|트랜잭션]](ACID) 기능을 부여한 **[[054_open_table_format_iceberg_delta_hudi|오픈 테이블 포맷]] ([[148_apache_iceberg|Apache Iceberg]], [[147_delta_lake|Delta Lake]])** 기술을 통해 '[[210_data_lakehouse_delta_lake|데이터 레이크하우스]]'로 융합되고 있다.

- **📢 섹션 요약 비유**: DW는 예쁘게 포장된 백화점 진열대이고, [[208_data_lake_schema_on_read|데이터 레이크]]는 무엇이든 던져놓는 거대한 야외 창고다. [[146_lakehouse|레이크하우스]]는 야외 창고에 백화점식 재고 관리 시스템을 도입한 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[001_dikw_pyramid|데이터]] 인프라를 설계할 때는 속도(Speed)와 비용(Cost) 사이의 의사결정이 가장 중요하다. 모든 [[001_dikw_pyramid|데이터]]를 실시간([[179_kafka_flink_watermark_time_window|Kafka]]/Flink)으로 처리하는 것은 환상에 불과하며 막대한 인프라 비용을 초래한다.

### 실무 [[435_checklist_based_testing|체크리스트]]
1. **[[001_dikw_pyramid|데이터]] 신선도 ([[001_dikw_pyramid|Data]] Freshness)**: 비즈니스 요구사항이 초 단위 실시간 분석을 요하는가, 아니면 1일 1회 배치(Batch) 분석으로 충분한가?
2. **[[171_idempotency_iac_terraform|멱등성]] ([[194_idempotency|Idempotency]]) 확보**: 파이프라인이 중간에 끊겨서 재실행되더라도 [[001_dikw_pyramid|데이터]]가 중복 적재되지 않고 동일한 결과를 보장하는가?
3. **[[005_schema|스키마]] 에볼루션 ([[505_schema|Schema]] Evolution)**: 원본 DB의 테이블 컬럼이 추가되거나 삭제될 때, 다운스트림 파이프라인이 터지지 않고 유연하게 대응하는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 수십 TB 단위의 단순 [[568_logs_distributed_logging_elk_fluentd|로그]] [[001_dikw_pyramid|데이터]]를 값비싼 DW에 무작정 적재하여 비용 폭탄을 맞는 아키텍처
- [[288_version_ihl_tos_total_length|버전]] 관리나 [[213_data_catalog_metadata|데이터 카탈로그]] 없이 수작업 스크립트로만 파이프라인을 엮어 유지보수가 불가능한 스파게티 시스템 구성

- **📢 섹션 요약 비유**: 로켓 배송(실시간 스트리밍)이 좋다고 해서, 유통기한이 긴 휴지(과거 분석 [[001_dikw_pyramid|데이터]])까지 굳이 비싼 오토바이 퀵으로 배달시킬 필요는 없다.

---

## Ⅴ. 기대효과 및 결론

견고한 [[001_dikw_pyramid|데이터]] 엔지니어링 인프라가 구축되면, 조직 내의 [[002_silo_hyeonhyung|사일로]]([[002_silo_hyeonhyung|Silo]])가 붕괴되고 누구나 신뢰할 수 있는 단일 진실 공급원(SSOT)에 접근할 수 있게 된다. 이는 [[241_machine_learning_basics|머신러닝]] 파이프라인([[348_mlops|MLOps]])의 기반이 되어 [[190_ai_llm_requirements_specification|AI]] 도입을 앞당긴다.

앞으로는 기술적 복잡성을 추상화하는 매니지드 [[090_service_kubernetes_network_load_balancing|서비스]](Managed [[090_service_kubernetes_network_load_balancing|Service]])가 더욱 발전할 것이며, 궁극적으로는 [[064_relation_domain|도메인]] 팀 스스로가 [[001_dikw_pyramid|데이터]] 프로덕트를 생산하고 소비하는 **[[211_data_mesh_domain_ownership|데이터 메시]]([[320_data_mesh|Data Mesh]])** 사상으로 조직 아키텍처 자체가 전환될 것이다. [[001_dikw_pyramid|데이터]] 엔지니어링은 단순한 파이프라인 구축을 넘어 "기업의 피([[001_dikw_pyramid|데이터]])를 순환시키는 심장"으로 기억해야 한다.

- **📢 섹션 요약 비유**: 정수장(인프라)이 완벽하게 돌아가면, 사람들은 물이 어디서 오는지 신경 쓰지 않고 수도꼭지(대시보드)만 틀어 편하게 갈증(비즈니스 문제)을 해소하게 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[209_data_warehouse_schema_on_write|데이터 웨어하우스]] ([[209_data_warehouse_schema_on_write|DW]]) | 정제된 [[001_dikw_pyramid|데이터]]를 다차원으로 분석하기 위해 [[005_schema|스키마]]에 맞춰 저장하는 중앙 DB |
| [[215_etl_vs_elt_pipeline|ETL]] / [[034_elt|ELT]] | 추출, 변환, 적재의 순서 차이. 최근에는 클라우드 파워를 활용하는 ELT가 대세 |
| [[213_data_catalog_metadata|데이터 카탈로그]] ([[213_data_catalog_metadata|Data Catalog]]) | [[136_variance|분산]]된 [[001_dikw_pyramid|데이터]]의 위치와 메타데이터를 검색 가능하게 만드는 구글 같은 존재 |
| [[216_lambda_kappa_architecture_batch_realtime|람다]]/[[096_kappa_architecture|카파 아키텍처]] | 배치 레이어와 스피드(실시간) 레이어를 어떻게 분리/통합할 것인지에 대한 설계 패턴 |

### 📈 관련 키워드 및 발전 흐름도

```text
온프레미스 RDBMS (단일 서버 한계)
    │
    ▼
하둡 (Hadoop) 기반 데이터 레이크 (저비용 분산 저장)
    │
    ▼
클라우드 데이터 웨어하우스 (Snowflake, BigQuery) + ELT
    │
    ▼
데이터 레이크하우스 (Data Lakehouse) (오픈 테이블 포맷 융합)
    │
    ▼
데이터 메시 (Data Mesh) (중앙 집중형에서 분산/도메인 오너십으로 진화)
```

이 흐름도는 "단일 저장 → 대용량 [[136_variance|분산]] 저장 → 연산 분리 및 클라우드화 → 구조 융합 → 조직 및 아키텍처 혁신"으로 개념이 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[001_dikw_pyramid|데이터]] 엔지니어링은 숲속의 옹달샘, 빗물, 강물(원시 [[001_dikw_pyramid|데이터]])을 모아서 커다란 물탱크에 담는 일이에요.
2. 그냥 마시면 배가 아프니까, 정수기(파이프라인)를 설치해서 깨끗하고 맛있는 물로 바꿔줘요.
3. 그러면 요리사([[001_dikw_pyramid|데이터]] 분석가)들이 언제든 수도꼭지만 틀어서 맛있는 요리([[231_ai_turing_test|인공지능]])를 만들 수 있답니다!
