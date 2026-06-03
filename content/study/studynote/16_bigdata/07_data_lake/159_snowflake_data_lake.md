+++
weight = 159
title = "159. Snowflake on Data Lake — External Table과 Iceberg 지원"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
1. Snowflake는 전통적 SQL 중심 DW를 넘어 External Tables와 Iceberg Tables를 통해 **객체 스토리지(S3/ADLS/GCS)의 [[001_dikw_pyramid|데이터]]를 직접 [[298_qkv_attention|쿼리]]**하는 [[146_lakehouse|레이크하우스]] 방향으로 확장하고 있다.
2. **스토리지-컴퓨팅 완전 분리(Decoupled [[319_architecture|Architecture]])**가 Snowflake의 핵심 설계 원칙이며, Virtual Warehouse(컴퓨팅)를 독립적으로 [[621_scale_up_system_bus|스케일 업]]/다운하여 [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]]과 비용을 탄력적으로 제어한다.
3. **Snowpark** (Python/Java/Scala 코드를 [[541_cassandra|Snowflake]] 내부에서 실행)와 **[[386_data_clean_room_sharing|데이터 공유]]([[001_dikw_pyramid|Data]] Sharing)** 기능이 SQL 전문가뿐 아니라 [[001_dikw_pyramid|데이터]] 엔지니어, ML 엔지니어까지 사용자 저변을 확대하고 있다.

---

## Ⅰ. 개요 및 필요성

Snowflake는 2012년 Amazon Redshift를 대체할 완전 [[531_cloud_native_architecture|클라우드 네이티브]] DW로 출발했다. 스토리지와 컴퓨팅을 분리하고, [[298_qkv_attention|쿼리]]량에 따라 Virtual Warehouse를 독립적으로 조정하는 혁신적 아키텍처로 시장을 장악했다.

그러나 [[210_data_lakehouse_delta_lake|데이터 레이크하우스]] 패러다임이 부상하면서 Snowflake는 객체 스토리지의 [[001_dikw_pyramid|데이터]]를 직접 [[298_qkv_attention|쿼리]]하는 External Table, 오픈 포맷인 Iceberg Table, 그리고 Python 코드를 [[541_cassandra|Snowflake]] 내에서 실행하는 Snowpark를 출시하여 [[146_lakehouse|레이크하우스]] 기능을 보강하고 있다.

| [[541_cassandra|Snowflake]] 진화 단계 | 핵심 기능 | 포지셔닝 |
|:---|:---|:---|
| 1세대 (2014~) | Virtual Warehouse, Time Travel | Cloud [[209_data_warehouse_schema_on_write|DW]] |
| 2세대 (2018~) | [[001_dikw_pyramid|Data]] Sharing, Secure [[151_sql_view_virtual_table|View]] | [[001_dikw_pyramid|Data]] Exchange |
| 3세대 ([[477_owasp_top_10_2021|2021]]~) | Snowpark, External Table | Analytics Platform |
| 4세대 (2023~) | Iceberg Table, Arctic ([[190_ai_llm_requirements_specification|AI]]) | [[146_lakehouse|Lakehouse]] + [[190_ai_llm_requirements_specification|AI]] |

> 📢 **섹션 요약 비유**: Snowflake의 진화는 식당이 배달 [[090_service_kubernetes_network_load_balancing|서비스]]와 밀키트까지 확장하는 것이다. 원래 레스토랑([[209_data_warehouse_schema_on_write|DW]])에서 시작했지만 이제는 다른 냉장고(레이크) 안의 재료도 직접 요리([[298_qkv_attention|쿼리]])할 수 있게 됐다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌──────────────────────────────────────────────────────────────────┐
│               Snowflake 레이크하우스 아키텍처                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │         외부 객체 스토리지 (S3 / ADLS Gen2 / GCS)        │     │
│  │         Parquet / Iceberg 형식 파일                      │     │
│  └──────────────────┬─────────────────────────────────────┘     │
│                     │                                           │
│           ┌─────────┴─────────┐                                 │
│           │                   │                                 │
│  ┌────────▼───────┐  ┌────────▼────────────┐                   │
│  │ External Table │  │ Snowflake-Managed    │                   │
│  │ (메타데이터만)  │  │ Iceberg Table       │                   │
│  │ 스키마 정의,   │  │ (Snowflake가 카탈로그│                   │
│  │ 직접 파일 읽기 │  │  관리, 외부 엔진도   │                   │
│  └────────────────┘  │  읽기 가능)          │                   │
│                      └────────────────────┘                    │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │          Virtual Warehouse (컴퓨팅, 독립 스케일)          │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │     │
│  │  │ XSmall   │  │  Large   │  │  Snowpark (Python/   │  │     │
│  │  │ (SQL 분석)│  │  (ETL)   │  │  Java/Scala 실행)    │  │     │
│  │  └──────────┘  └──────────┘  └──────────────────────┘  │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │          Cloud Services Layer (메타데이터·쿼리 최적화)    │     │
│  └────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

**External Table vs Iceberg Table vs Internal Table**

| 항목 | Internal Table | External Table | Iceberg Table |
|:---|:---|:---|:---|
| [[001_dikw_pyramid|데이터]] 위치 | [[541_cassandra|Snowflake]] 스토리지 | S3/ADLS/GCS (외부) | S3/ADLS/GCS (외부) |
| 포맷 | Micro-[[514_partition_slice_volume|partition]] (독점) | [[178_parquet_rle_encoding_columnar_compression|Parquet]]/ORC (사용자 관리) | [[148_apache_iceberg|Apache Iceberg]] |
| ACID 보장 | 완전 | 없음 (읽기 전용) | Iceberg 스펙 따름 |
| 외부 엔진 접근 | 불가 | [[501_file_definition_logical_record|파일]] 직접 접근 가능 | Spark/Trino 등 접근 가능 |
| 타임 트래블 | 90일 | 없음 | Iceberg [[022_snapshot_backup_architecture|스냅샷]] |
| 비용 | [[541_cassandra|Snowflake]] 스토리지 비용 | 외부 스토리지 비용만 | 외부 스토리지 비용만 |

> 📢 **섹션 요약 비유**: Internal Table은 식당 내부 냉장고(전용), External Table은 외부 창고를 바라보는 창문(읽기만), Iceberg Table은 외부 창고에서 식당과 외부 업체 모두가 쓸 수 있는 공용 [[561_container_based_deployment|컨테이너]]다.

---

## Ⅲ. 비교 및 연결

**[[541_cassandra|Snowflake]] vs [[074_photon_engine|Databricks]] — [[146_lakehouse|레이크하우스]] 관점**

| 항목 | [[541_cassandra|Snowflake]] | [[074_photon_engine|Databricks]] |
|:---|:---|:---|
| 스토리지 포맷 | 독점(Internal) + Iceberg(External) | [[147_delta_lake|Delta Lake]] ([[191_oss_license_compliance|오픈소스]]) |
| SQL 경험 | 최상 (ANSI SQL 완전 지원) | 좋음 ([[056_spark_sql|Spark SQL]]) |
| ML/[[190_ai_llm_requirements_specification|AI]] 지원 | Snowpark ML (성장 중) | 최고 수준 ([[180_mlflow|MLflow]] 내장) |
| 스트리밍 | Snowpipe (마이크로 배치) | [[061_structured_streaming|Structured Streaming]] (진정한 스트리밍) |
| 오픈 포맷 | Iceberg 지원 (부분) | Delta + Iceberg + Hudi |
| 운영 모델 | 완전 [[206_serverless_cold_start|서버리스]] | 클러스터 관리 일부 필요 |

**Snowpark 활용**
- Python DataFrame API를 [[541_cassandra|Snowflake]] 내에서 실행 ([[001_dikw_pyramid|데이터]] 이동 없음)
- ML 모델 훈련을 [[541_cassandra|Snowflake]] Warehouse 위에서 직접 수행
- [[541_cassandra|Snowflake]] ML Functions: [[263_llm_large_language_model|LLM]]·예측 모델을 SQL 함수처럼 호출

> 📢 **섹션 요약 비유**: [[541_cassandra|Snowflake]] on Lakehouse는 전통 백화점이 온라인 쇼핑몰도 운영하는 것이다. 백화점 내 상품(Internal Table)뿐 아니라 외부 창고(External/Iceberg) 상품도 같은 앱에서 주문할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[[541_cassandra|Snowflake]] [[146_lakehouse|레이크하우스]] 도입 시나리오**

- **SQL 우선 조직**: 기존 [[541_cassandra|Snowflake]] [[209_data_warehouse_schema_on_write|DW]] 투자 보존 + 레이크 [[001_dikw_pyramid|데이터]] 통합 [[298_qkv_attention|쿼리]]
- **비용 최적화**: 비활성 [[001_dikw_pyramid|데이터]]를 [[541_cassandra|Snowflake]] 스토리지에서 S3 External Table로 이전
- **멀티엔진 환경**: Iceberg Table로 Spark·Trino와 Snowflake가 동일 테이블 공유
- **[[386_data_clean_room_sharing|데이터 공유]]**: Secure [[001_dikw_pyramid|Data]] Sharing으로 파트너사에 실시간 [[001_dikw_pyramid|데이터]] 피드 제공

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| Virtual Warehouse 동작 | 독립 컴퓨팅 클러스터, [[298_qkv_attention|쿼리]]별 자동 확장, 사용 시간만 과금 |
| External Table 한계 | [[184_partition_pruning|파티션 프루닝]] 효율 낮음, ACID 없음, [[289_cqrs_db|쓰기]] 불가 |
| Iceberg Table 이점 | 외부 엔진과 공유 가능, Iceberg ACID, [[514_partition_slice_volume|파티션]] 진화 |
| Snowpark 활용 이유 | Python 코드를 [[541_cassandra|Snowflake]] 내에서 실행 → [[001_dikw_pyramid|데이터]] 이동 없음 |

> 📢 **섹션 요약 비유**: Virtual Warehouse는 택시 호출 앱과 같다. 손님([[298_qkv_attention|쿼리]])이 생기면 택시(컴퓨팅)를 불러 태우고, 목적지(결과)에 도달하면 요금만 내고 해산한다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 스토리지 비용 절감 | External Table로 비활성 [[001_dikw_pyramid|데이터]]를 저비용 객체 스토리지에 보존 |
| 멀티엔진 유연성 | Iceberg Table로 Spark/Trino/[[541_cassandra|Snowflake]] 공유 접근 |
| SQL 생산성 유지 | 레이크 [[001_dikw_pyramid|데이터]]를 기존 SQL [[298_qkv_attention|쿼리]] 패턴으로 접근 |
| [[386_data_clean_room_sharing|데이터 공유]] | [[541_cassandra|Snowflake]] [[001_dikw_pyramid|Data]] Exchange로 파트너사와 실시간 공유 |

Snowflake는 SQL 네이티브 강점을 유지하면서 [[146_lakehouse|레이크하우스]] 기능을 점진적으로 강화하는 [[268_strategy_pattern|전략]]을 취하고 있다. Iceberg 지원 심화, Snowpark ML 성장, Arctic([[190_ai_llm_requirements_specification|AI]] 통합)이 2024~2025년 주요 방향이다. 기술사 시험에서는 **Virtual Warehouse 스케일 분리 원리**, **External Table vs Internal Table 트레이드오프**, **[[541_cassandra|Snowflake]] vs [[074_photon_engine|Databricks]] 포지셔닝 비교**가 핵심 논점이다.

> 📢 **섹션 요약 비유**: Snowflake의 [[146_lakehouse|레이크하우스]] 확장은 전통 은행이 핀테크 [[090_service_kubernetes_network_load_balancing|서비스]]를 추가하는 것이다. 기존 고객 기반(SQL 사용자)을 보존하면서 새로운 기능(Iceberg, Snowpark)으로 더 넓은 시장을 공략한다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| Virtual Warehouse | 컴퓨팅 레이어 | 독립 스케일, 사용 시간 과금 |
| External Table | 레이크 통합 | 객체 스토리지 직접 [[298_qkv_attention|쿼리]] (읽기 전용) |
| Iceberg Table | 오픈 포맷 통합 | 멀티엔진 공유, ACID 보장 |
| Snowpark | 코드 실행 | Python/Java/Scala [[541_cassandra|Snowflake]] 내 실행 |
| [[001_dikw_pyramid|Data]] Sharing | 외부 공유 | 복사 없는 실시간 [[386_data_clean_room_sharing|데이터 공유]] |
| Micro-[[514_partition_slice_volume|partition]] | 내부 스토리지 | 자동 클러스터링, 16~512MB 블록 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[기존 데이터 웨어하우스 (DW) — 정형 데이터 전용, 비용 높음, 비정형 처리 불가]
    │
    ▼
[데이터 레이크 (Data Lake) — 원시 데이터 모든 형식 저장, 스키마 온 리드]
    │
    ▼
[Snowflake External Table — S3/GCS 오브젝트 스토리지를 Snowflake에서 SQL 조회]
    │
    ▼
[Apache Iceberg 통합 — 오픈 테이블 포맷, ACID 트랜잭션·타임 트래블 지원]
    │
    ▼
[데이터 레이크하우스 (Data Lakehouse) — DW 성능 + 데이터 레이크 유연성 통합]
    │
    ▼
[데이터 메시 (Data Mesh) — 도메인별 분산 소유권, Snowflake Data Sharing 연동]
```
이 흐름은 [[002_structured_data|정형 데이터]] 전용 DW의 한계를 [[208_data_lake_schema_on_read|데이터 레이크]]로 극복하고, Snowflake의 외부 테이블·Iceberg 통합을 통해 [[146_lakehouse|레이크하우스]] 아키텍처로 수렴하며, [[211_data_mesh_domain_ownership|데이터 메시]] 패러다임과 결합하는 현대 [[001_dikw_pyramid|데이터]] 플랫폼의 진화를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. Snowflake는 처음에는 식당([[209_data_warehouse_schema_on_write|DW]])이었는데, 이제는 외부 슈퍼마켓(레이크) 재료도 가져와서 요리([[298_qkv_attention|쿼리]])할 수 있어요.
2. Virtual Warehouse는 손님([[298_qkv_attention|쿼리]])이 많으면 요리사(컴퓨팅)를 더 부르고, 한가하면 집에 보내는 스마트 주방이에요.
3. Snowpark는 SQL만 쓰던 식당에서 Python 요리사도 일할 수 있게 해주는 새 조리 방식이에요.
