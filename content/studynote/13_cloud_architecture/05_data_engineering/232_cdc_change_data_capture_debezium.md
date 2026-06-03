+++
title = "232. CDC (Change Data Capture / 변경 데이터 캡처)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)([Change Data Capture](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/), [변경 데이터 캡처](/knowledge-base/studynote/12_it_management/05_security_compliance/218_cdc_change_data_capture/))는 운영 DB의 <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a> <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a>(<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/">Redo</a> Log/Binlog)</strong>를 직접 읽어 INSERT·UPDATE·DELETE 이벤트를 실시간 추출하는 기술로, DB에 추가 부하 없이 변경분만 캡처한다.
> 2. **가치**: 전통적 ETL의 "전체 테이블 스캔 주기 배치" 대신, <strong>밀리초 단위 실시간 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a></strong>를 가능하게 하여 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)·DW의 신선도를 획기적으로 향상한다.
> 3. **판단 포인트**: <strong>Debezium</strong>이 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) CDC의 사실상 표준으로, [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect 기반으로 MySQL·PostgreSQL·[Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/)·[MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) 등 주요 DB의 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 토픽으로 스트리밍한다.

---

## Ⅰ. 개요 및 필요성

전통적 ETL은 주기적으로(야간) 운영 DB에서 `SELECT * WHERE updated_at > 어제`로 변경 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 추출한다. 이 방식의 문제는:
- DB 부하: 대용량 스캔 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 운영 DB 성능에 영향
- [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/): T+1일 또는 최소 수분 주기, 실시간 불가
- 삭제 감지 불가: 물리 삭제된 행은 `updated_at` 방식으로 감지 불가
- 타임스탬프 없는 테이블: 변경 감지 자체 불가

CDC는 이 모든 문제를 DB의 <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a> <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a></strong>를 읽는 방식으로 해결한다.

```
[전통 ETL 방식]
Batch 쿼리 (SELECT * WHERE updated > ?)
운영 DB ──────────────────────────────▶ DW
        ↑ DB 부하 발생, 매 시간/일 스캔

[CDC 방식]
트랜잭션 로그 (Binlog/Redo Log)
운영 DB ──▶ Debezium ──▶ Kafka ──▶ DW/레이크
        ↑ 로그 읽기 (읽기 전용, 최소 부하)
        ↑ 밀리초 단위 실시간 전송
```

📢 **섹션 요약 비유**: CDC는 [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/) 영상 기록이다. 누군가 가게(DB)에 들어와 물건을 가져가거나(DELETE), 추가하거나(INSERT), 바꾸면(UPDATE), [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/)([트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))가 자동으로 기록한다. 가게를 닫고 재고 조사(배치 스캔)를 하지 않아도 실시간으로 변화를 감지한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Debezium 아키텍처

```
┌────────────────────────────────────────────────────────────────┐
│                    CDC 파이프라인 (Debezium)                    │
│                                                                │
│  MySQL/PostgreSQL        Kafka Connect          Kafka Topic    │
│  ┌──────────────┐        ┌───────────────┐      ┌──────────┐  │
│  │  운영 DB     │  로그   │   Debezium    │  이벤트│ orders.  │  │
│  │  Binlog/    │ ──────▶ │  Source       │ ────▶ │ public.  │  │
│  │  WAL 읽기   │        │  Connector    │       │ orders   │  │
│  │             │        │               │       └──────────┘  │
│  │ INSERT/     │        │  변경 이벤트  │                     │
│  │ UPDATE/     │        │  to JSON/Avro │  ┌────────────────┐ │
│  │ DELETE      │        │               │  │ Kafka Sink     │ │
│  └──────────────┘        └───────────────┘  │ Connector      │ │
│                                             │ (S3/Snowflake/ │ │
│                                             │  Elasticsearch)│ │
│                                             └────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

### [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 이벤트 메시지 구조 (Debezium [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/) 예시)

```json
{
  "op": "u",            // c=create, u=update, d=delete, r=read(snapshot)
  "before": {           // 변경 전 상태
    "order_id": 1001,
    "status": "pending",
    "amount": 50000
  },
  "after": {            // 변경 후 상태
    "order_id": 1001,
    "status": "shipped",
    "amount": 50000
  },
  "source": {
    "table": "orders",
    "ts_ms": 1705123456789,  // 이벤트 발생 타임스탬프
    "pos": "mysql-bin.000001:12345"  // 로그 위치
  }
}
```

### 주요 DB별 [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 메커니즘

| DB | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 유형 | Debezium 커넥터 |
|:---|:---|:---|
| **MySQL** | Binary Log (Binlog) | debezium-mysql |
| **PostgreSQL** | Write-Ahead Log (WAL) | debezium-postgres |
| <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/">Oracle</a></strong> | [Redo](/knowledge-base/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/) Log | debezium-[oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) |
| **SQL Server** | [Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Log | debezium-sqlserver |
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/">MongoDB</a></strong> | Oplog (Operations Log) | debezium-[mongodb](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) |
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/">DynamoDB</a></strong> | [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) Streams | AWS native [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) |

📢 **섹션 요약 비유**: Debezium은 DB의 "일기장"을 읽는 독자다. DB는 모든 변경 내역을 일기장([트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))에 자동으로 쓴다. Debezium은 이 일기장을 몰래 읽어(비침습적) Kafka에 전달한다. DB는 일기를 쓰는 것 외에 추가 작업이 없다.

---

## Ⅲ. 비교 및 연결

### [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) vs 전통 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 배치 비교

| 비교 항목 | [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) (Debezium + [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)) | 전통 배치 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">지연 시간</a></strong> | 밀리초~초 | 분~시간 |
| **DB 부하** | 매우 낮음 ([로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 읽기) | 높음 (테이블 풀스캔) |
| **삭제 감지** | 가능 (DELETE 이벤트) | 불가 (행 사라짐) |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a> 없는 테이블</strong> | 가능 | 타임스탬프 없으면 불가 |
| <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong> | 복잡 ([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)) | 단순 (SQL [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)) |
| **운영 복잡성** | 높음 | 낮음 |
| **적합 환경** | 실시간 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 필요 | 일 배치 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 적재 |

### [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 활용 패턴

| 패턴 | 설명 | 사례 |
|:---|:---|:---|
| <strong>DB → <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/">Data Lake</a></strong> | 운영 DB 변경분 실시간 레이크 적재 | RDS → S3 [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/) |
| <strong>DB → <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/">DW</a></strong> | 운영 DB → [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 실시간 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) | MySQL → [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) |
| **DB → Cache** | DB 변경 시 캐시 즉시 무효화 | PostgreSQL → [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a> <a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/">이벤트 소싱</a></strong> | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) DB 변경 → 다른 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 이벤트 발행 | Order DB → Email [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |
| <strong>DB → <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/302_cdc/">Elasticsearch</a></strong> | DB [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 실시간 검색 인덱싱 | MySQL → ES 전문 검색 |

📢 **섹션 요약 비유**: [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 파이프라인은 실시간 번역가다. 한국어(MySQL 이벤트)를 즉시 영어([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/))로 번역해서 전 세계 독자([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/), 레이크, 캐시)에게 동시에 전달한다. 번역가는 원래 연설자(DB)의 연설을 방해하지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Debezium 커넥터 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 예시 (MySQL)

```json
{
  "name": "mysql-orders-connector",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.hostname": "mysql-prod.example.com",
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "secret",
    "database.server.id": "1",
    "database.server.name": "mysql-prod",
    "database.include.list": "ecommerce",
    "table.include.list": "ecommerce.orders,ecommerce.products",
    "database.history.kafka.bootstrap.servers": "kafka:9092",
    "database.history.kafka.topic": "schema-changes.ecommerce",
    "transforms": "unwrap",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState"
  }
}
```

### MySQL Binlog [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) (사전 요건)

```sql
-- MySQL 서버 설정 확인
SHOW VARIABLES LIKE 'log_bin';          -- ON 필요
SHOW VARIABLES LIKE 'binlog_format';    -- ROW 필요
SHOW VARIABLES LIKE 'binlog_row_image'; -- FULL 권장

-- Debezium 전용 복제 권한 부여
GRANT SELECT, RELOAD, SHOW DATABASES, REPLICATION SLAVE,
      REPLICATION CLIENT ON *.* TO 'debezium'@'%';
```

**기술사 핵심 판단**: [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 도입 시 "왜 배치 ETL을 CDC로 대체하는가"를 실시간성·DB 부하 감소·삭제 감지 3가지로 논리화하고, Debezium 아키텍처를 [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect Source/Sink 흐름으로 설명한다.

📢 **섹션 요약 비유**: [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)은 DB에 "[도청](/knowledge-base/studynote/03_network/14_network_security_threats/701_sniffing_eavesdropping_promiscuous/) 장치"를 합법적으로 설치하는 것이다. DB의 자체 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)(Binlog)를 읽는 것이므로 DB 성능에 영향이 없고, 모든 변경 사항을 빠짐없이 실시간으로 캡처한다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| <strong>실시간 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 신선도</strong> | 배치 T+1일 → 밀리초 단위 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)로 전환 |
| **DB 부하 최소화** | 풀스캔 제거, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 읽기로 운영 DB [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) |
| **완전한 변경 이력** | INSERT·UPDATE·DELETE 모두 캡처, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적 |
| <strong>이벤트 기반 <a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a></strong> | DB 변경을 이벤트로 발행해 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 결합 해소 |
| **캐시 자동 무효화** | DB 변경 즉시 [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 캐시 자동 업데이트 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> <a href="/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/">스냅샷</a></strong> | 기존 전체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 적재(Initial [Snapshot](/knowledge-base/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/)) 시간 소요 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a> 변경</strong> | ADD COLUMN 등 [DDL](/knowledge-base/studynote/05_database/01_db_architecture_relational/020_ddl/) 변경 처리 복잡 ([스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 필요) |
| <strong>Binlog <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> 권한</strong> | DB 서버 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 변경 권한 필요 (보안 승인) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> 보존 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a></strong> | 빠른 처리 필요, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 디스크 소진 주의 |
| **운영 복잡성** | [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect 클러스터 관리, 커넥터 모니터링 |

📢 **섹션 요약 비유**: CDC는 강력하지만, 처음 설치할 때 전체 재고 조사(Initial [Snapshot](/knowledge-base/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/))는 한 번 해야 한다. 이후에는 변경분만 추적하므로 효율적이지만, "[CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/) 시스템"을 유지 관리하는 관리자([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect 운영)가 항상 필요하다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| Debezium | [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 구현의 사실상 표준 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) |
| [Apache Kafka](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) | [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 이벤트 전송 [메시지 브로커](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/) |
| [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) | CDC로 대체되는 전통 배치 변경 추출 방식 |
| [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | CDC의 핵심 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스 (Binlog/WAL/[Redo](/knowledge-base/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/) Log) |
| [이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) | [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 이벤트를 시스템 이벤트로 활용하는 패턴 |
| [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect | Debezium이 동작하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 통합 플랫폼 |
| [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) | [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 이벤트 메시지의 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 |

### 👶 어린이를 위한 3줄 비유 설명
1. CDC는 도서관 사서가 책 반납 기록부([트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))를 보고 "어떤 책이 대출되고 반납됐는지" 실시간으로 확인하는 것이다. 직접 책장을 다 뒤지지 않아도 된다.

### 📈 관련 키워드 및 발전 흐름도

```text
풀 스캔 동기화 (전체 복사, 비효율)
    │
    ▼
CDC: 변경분만 캡처 (Log-based · Trigger-based)
    ├─► Debezium: MySQL/PG WAL → Kafka 토픽
    └─► Kafka Connect: Source/Sink 커넥터
    │
    ▼
실시간 ETL · 이벤트 소싱 · CQRS 패턴 연동
```
2. Debezium은 기록부를 읽는 비서다. 사서(DB)가 기록부에 쓰는 것을 지켜보다가, 새 내용이 생기면 즉시 공지 게시판([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/))에 붙여준다.
3. 덕분에 다른 도서관들([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/), 레이크, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)들)은 게시판만 보면 원본 도서관 상황을 실시간으로 알 수 있어, 일일이 원본 도서관(운영 DB)에 전화하지 않아도 된다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 231 / 371

← **이전**: [231. 카프카 토픽 / 파티션 / 컨슈머 그룹](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/231_kafka_topic_partition_consumer_group/)
**다음**: [233. 아파치 에어플로우 (Apache Airflow)](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/233_apache_airflow_dag_orchestration/) →

---
