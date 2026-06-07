---
title: "Streaming Sql"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 97
---
## 핵심 인사이트 (3줄 요약)

- **본질**: 스트리밍 SQL (Streaming SQL)은 무한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스트림에 지속적으로 실행되는 SQL [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)로, 표준 SQL에 윈도우 함수·[워터마크](/studynote/16_bigdata/04_streaming/085_watermark/)·스트림-테이블 조인 등 스트리밍 고유 연산이 추가된 형태이며, ksqlDB ([Confluent](/studynote/12_it_management/02_itsm_itil/878_reinforcement_learning/)), Flink SQL ([Apache Flink](/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/)), [Spark Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/) SQL이 3대 주요 엔진이다.
- **가치**: 스트리밍 처리를 위해 Java/Python API를 배우지 않아도 SQL 한 줄로 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 스트림 집계·필터·조인을 구현할 수 있어 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어의 진입 장벽을 낮추고, 선언적 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)로 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)가 [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/)을 자동 최적화한다.
- **판단 포인트**: ksqlDB는 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)-native로 운영이 단순하지만 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 생태계에 종속되고, Flink SQL은 ANSI SQL 완전성과 이벤트 시간 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)가 가장 높으며, Spark SQL은 기존 Spark 인프라를 그대로 활용하는 마이크로배치 방식으로 [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)이 수 초 이상이다.

---

## Ⅰ. 개요 및 필요성

### 1. 스트리밍 SQL의 등장 배경

```
기존 스트리밍 개발의 장벽:
  - DataStream API (Flink): Java/Scala/Python 코드 수백 줄
  - RDD API (Spark): 함수형 프로그래밍 패러다임
  - Storm Topology: 복잡한 빌더 패턴

스트리밍 SQL의 혁신:
  SELECT user_id, COUNT(*) AS event_count
  FROM clicks
  WHERE event_type = 'purchase'
  GROUP BY user_id, TUMBLE(event_time, INTERVAL '5' MINUTE)

  -> 동일한 로직을 SQL 한 줄로!
```

### 2. 3대 스트리밍 SQL 엔진 개요

| 엔진 | 기반 | 배포 방식 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 수준 |
|:---|:---|:---|:---|
| ksqlDB | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Streams | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 클러스터와 함께 배포 | 밀리초~초 |
| Flink SQL | [Apache Flink](/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/) | Flink 클러스터 필요 | 밀리초~초 |
| [Spark Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/) | [Apache Spark](/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) | Spark 클러스터 필요 | 초~분 (마이크로배치) |

**📢 섹션 요약 비유**
> 스트리밍 SQL은 "흐르는 강물에 그물(SQL)을 치는 것"이다. 물([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 흐르는 동안 그물이 지속적으로 물고기(집계 결과)를 잡아준다. 낚싯대(DataStream [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/))보다 그물(SQL)이 더 쉽고 생산적이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. ksqlDB ([Confluent](/studynote/12_it_management/02_itsm_itil/878_reinforcement_learning/))

```sql
-- ksqlDB: Kafka 토픽에서 직접 SQL 실행
-- 스트림 생성
CREATE STREAM clicks (
    user_id VARCHAR,
    page_url VARCHAR,
    event_time BIGINT
) WITH (
    kafka_topic = 'user-clicks',
    value_format = 'JSON',
    timestamp = 'event_time'
);

-- 5분 윈도우 집계 (지속적 쿼리)
CREATE TABLE page_views_per_5min AS
SELECT page_url,
       COUNT(*) AS view_count,
       WINDOWSTART AS window_start
FROM clicks
WINDOW TUMBLING (SIZE 5 MINUTES)
GROUP BY page_url
EMIT CHANGES;  -- 변경될 때마다 결과 출력
```

### 2. Flink SQL

```sql
-- Flink SQL: ANSI SQL 완전 호환 + 스트리밍 확장
-- 카탈로그 테이블(Kafka 소스) 정의
CREATE TABLE clicks (
    user_id    STRING,
    page_url   STRING,
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND  -- 워터마크 설정
) WITH (
    'connector' = 'kafka',
    'topic' = 'user-clicks',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json'
);

-- 이벤트 시간 기반 텀블링 윈도우 집계
SELECT page_url,
       TUMBLE_START(event_time, INTERVAL '5' MINUTE) AS window_start,
       COUNT(*) AS view_count
FROM clicks
GROUP BY page_url, TUMBLE(event_time, INTERVAL '5' MINUTE);
```

### 3. [Spark Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/) SQL

```python
# Spark Structured Streaming + SQL
from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col

spark = SparkSession.builder.getOrCreate()

# Kafka에서 스트림 읽기
stream_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "user-clicks") \
    .load()

# SQL 기반 집계
stream_df.createOrReplaceTempView("clicks")
result = spark.sql("""
    SELECT page_url,
           window.start AS window_start,
           COUNT(*) AS view_count
    FROM clicks
    GROUP BY page_url, window(event_time, '5 minutes')
""")

# 출력
result.writeStream.format("console").start()
```

### 4. 3엔진 비교

| 항목 | ksqlDB | Flink SQL | [Spark SQL](/studynote/16_bigdata/03_spark/056_spark_sql/) (Streaming) |
|:---|:---|:---|:---|
| SQL 표준 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 특화 SQL | ANSI SQL 완전 호환 | ANSI SQL (3.x+) |
| 이벤트 시간 | ✅ | ✅ ([Watermark](/studynote/16_bigdata/04_streaming/085_watermark/) 정밀) | ✅ (마이크로배치 기반) |
| 처리 방식 | 이벤트 단위 | 이벤트 단위 | 마이크로배치 |
| 스트림-테이블 조인 | ✅ ([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) KTable) | ✅ (Temporal [Join](/studynote/05_database/04_transactions_concurrency/521_join/)) | ✅ (Static [join](/studynote/05_database/04_transactions_concurrency/521_join/)) |
| 운영 단순성 | 최고 ([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 일체형) | 중간 | 기존 Spark 재활용 |
| 성숙도 | 중간 | 높음 | 높음 |

**📢 섹션 요약 비유**
> ksqlDB는 "[Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 전용 만능 스위스칼", Flink SQL은 "ANSI 표준 수술 도구 세트", [Spark SQL](/studynote/16_bigdata/03_spark/056_spark_sql/) 스트리밍은 "기존 연구소 장비(Spark)에 스트리밍 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 추가"이다. 각각의 환경에서 최적이다.

---

## Ⅲ. 비교 및 연결

### 1. 스트리밍 SQL의 특수 기능

```sql
-- 스트림-스트림 인터벌 조인 (Flink SQL)
SELECT c.user_id, p.product_id, c.event_time
FROM clicks c
JOIN purchases p ON c.user_id = p.user_id
AND p.event_time BETWEEN c.event_time AND c.event_time + INTERVAL '30' MINUTE;

-- 스트림-테이블 조인 (ksqlDB: 사용자 정보로 이벤트 enrichment)
SELECT c.user_id, c.page_url, u.user_name
FROM clicks c
LEFT JOIN users u ON c.user_id = u.user_id;
```

### 2. 연결 개념

- <strong><a href="/studynote/16_bigdata/04_streaming/086_window_operations/">Window Operations</a></strong>: 스트리밍 SQL의 [GROUP BY](/studynote/05_database/04_transactions_concurrency/522_group_by/) TUMBLE/HOP/[SESSION](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)
- <strong><a href="/studynote/16_bigdata/04_streaming/085_watermark/">Watermark</a></strong>: Flink SQL의 [WATERMARK](/studynote/16_bigdata/04_streaming/085_watermark/) 선언으로 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트 허용
- **Exactly-Once**: Flink SQL의 [체크포인팅](/studynote/16_bigdata/03_spark/071_checkpointing/)과 연계

**📢 섹션 요약 비유**
> 스트리밍 SQL의 스트림-테이블 조인은 "흐르는 강(스트림)에서 주소록(테이블)을 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)해 편지 주인 이름을 찾는 것"이다. 편지(이벤트)가 계속 흘러와도 주소록은 고정되어 있어 언제든 이름을 찾을 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 1. 스트리밍 SQL 엔진 선택 가이드

| 상황 | 권장 엔진 |
|:---|:---|
| [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 생태계에서 빠른 프로토타이핑 | ksqlDB |
| 이벤트 시간 정밀 집계, 표준 SQL | Flink SQL |
| 기존 Spark 클러스터 활용, 배치+스트리밍 통합 | [Spark Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/) |
| 복잡한 [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) + 이벤트 시간 + 멀티소스 | Flink SQL |
| 비기술 사용자의 [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) 구축 | ksqlDB (가장 단순) |

### 2. [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] 이벤트 시간 필드와 [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 정의
- [ ] 윈도우 유형 (TUMBLE/HOP/[SESSION](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)) 비즈니스 요구에 맞게 선택
- [ ] 스트림-테이블 조인 시 테이블 갱신 주기와 조인 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 검토
- [ ] Exactly-Once 필요 여부 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) -> Flink SQL + [체크포인팅](/studynote/16_bigdata/03_spark/071_checkpointing/)
- [ ] NULL 및 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트 처리 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 명확화

**📢 섹션 요약 비유**
> 스트리밍 SQL 선택은 "음식 조리 도구 선택"과 같다. ksqlDB는 전자레인지(빠르고 단순), Flink SQL은 풀 세트 주방(기능 완전), [Spark SQL](/studynote/16_bigdata/03_spark/056_spark_sql/) 스트리밍은 기존 주방 기기에 인덕션 추가(기존 환경 활용)이다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| 개발 생산성 | SQL로 스트리밍 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 10배 빠른 개발 |
| 진입 장벽 감소 | Java/Scala [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 없이 SQL로 스트리밍 구현 |
| 자동 최적화 | SQL [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/)가 [실행 계획](/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| 표준화 | 다른 팀과 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 공유·재사용 용이 |

### 2. 결론

스트리밍 SQL은 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 엔지니어링의 민주화</strong>를 가능하게 하는 핵심 기술이다. 기술사 답안에서는 ksqlDB/Flink SQL/[Spark Streaming](/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/) SQL의 특성 비교, 스트리밍 고유 SQL 구문(TUMBLE, HOP, [WATERMARK](/studynote/16_bigdata/04_streaming/085_watermark/), EMIT CHANGES), 그리고 스트림-테이블 조인의 실무적 활용을 서술하면 된다.

**📢 섹션 요약 비유**
> 스트리밍 SQL은 "강이 되어버린 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 SQL 낚시 면허증"을 부여한 것이다. 이제 엔지니어뿐 아니라 SQL을 아는 분석가도 흐르는 강에서 직접 물고기(인사이트)를 잡을 수 있게 되었다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [Window Operations](/studynote/16_bigdata/04_streaming/086_window_operations/) | 핵심 구현 | 스트리밍 SQL의 TUMBLE/HOP/[SESSION](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) |
| [Watermark](/studynote/16_bigdata/04_streaming/085_watermark/) | Flink SQL 연동 | 이벤트 시간 기반 집계의 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 처리 |
| [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) (ksqlDB) | 소스 시스템 | ksqlDB의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스 및 싱크 |
| Exactly-Once | [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) | Flink SQL [체크포인팅](/studynote/16_bigdata/03_spark/071_checkpointing/)으로 달성 |
| [CEP](/studynote/16_bigdata/04_streaming/098_cep/) | 확장 기능 | Flink의 복합 이벤트 패턴 감지 |

### 📈 관련 키워드 및 발전 흐름도

```text
[정적 배치 SQL — 저장된 테이블 대상 질의]
    |
    v
[스트리밍 SQL — 흐르는 스트림에 SQL 적용]
    |
    v
[Window 연산 (TUMBLE·HOP·SESSION) — 시간 구간 집계]
    |
    v
[Watermark — 이벤트 지연 허용 및 집계 완료 트리거]
    |
    v
[ksqlDB (Kafka) / Flink SQL — 프로덕션 스트리밍 SQL 표준]
```
정적 SQL 문법을 흐르는 스트림에 적용하고, 창(Window)과 [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/)([Watermark](/studynote/16_bigdata/04_streaming/085_watermark/))로 시간 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 처리하며, ksqlDB와 Flink SQL이 각각 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)·범용 스트리밍 표준으로 자리잡는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

스트리밍 SQL은 "흐르는 물에 낚시 그물을 치는 것"이에요. SQL(그물 모양)만 설명하면 시스템이 알아서 계속 물고기([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 잡아줘요. ksqlDB는 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 강에 사는 물고기 전용 그물, Flink SQL은 모든 강에서 쓸 수 있는 표준 그물, [Spark SQL](/studynote/16_bigdata/03_spark/056_spark_sql/) 스트리밍은 기존 낚시터(Spark)에 새 그물을 추가한 거예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 97 / 262

<- **이전**: [21. 카파 아키텍처 (Kappa Architecture) — 스트리밍 단일화](/studynote/16_bigdata/04_streaming/096_kappa_architecture/)
**다음**: [23. CEP (Complex Event Processing) — 복합 이벤트 처리](/studynote/16_bigdata/04_streaming/098_cep/) ->

---
