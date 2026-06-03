+++
title = "217. CDC (Change Data Capture) 빈로그 데이터 변경 캡처 Debezium"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CDC(Change [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Capture)는 소스 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스에서 발생하는 INSERT·UPDATE·DELETE 변경 사항을 실시간으로 감지·캡처하여 다른 시스템에 전달하는 기술로, 전통적인 전체 테이블 복사(Full Dump) 대비 네트워크·DB 부하를 획기적으로 줄인다.
> 2. **가치**: MySQL Binlog·PostgreSQL WAL(Write-Ahead Log) 기반 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) CDC는 DB에 추가 부하 없이 변경을 캡처하며, Debezium + [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 조합으로 마이크로초 단위 실시간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 파이프라인을 구성한다.
> 3. **판단 포인트**: [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 기반 CDC는 DB 부하가 크고, 타임스탬프 기반은 DELETE를 감지 못한다 — 프로덕션 환경에서는 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 CDC(Log-based CDC)가 유일한 표준 선택이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 전통적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)의 한계

| 방법 | 설명 | 문제점 |
|:---|:---|:---|
| **전체 복사 (Full Dump)** | 주기적으로 전체 테이블 복사 | 시간·네트워크 비용 과다, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 큼 |
| **타임스탬프 기반** | `updated_at > 마지막 실행 시각` [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | DELETE 감지 불가, [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 필요 |
| **[트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 기반** | DB [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)로 변경 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 테이블 기록 | [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) DB 부하, [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 수정 필요 |
| **[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 CDC** | DB [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 직접 파싱 | 추가 부하 없음, DELETE 포함 전체 변경 캡처 |

### 1.2 CDC가 해결하는 문제

```
레거시 방식 (전체 복사):
  소스 DB ──[매시간 전체 SELECT]──► DW / 타겟 시스템
  - 100만 건 테이블에서 변경된 100건 찾기 위해 100만 건 스캔
  - 잦은 배치로 DB 부하 급증

CDC 방식 (로그 기반):
  소스 DB ──[변경된 100건만 캡처]──► Kafka ──► DW / 타겟
  - DB 복제 로그에서 변경 이벤트만 읽음
  - 소스 DB에 추가 부하 없음
  - 실시간 (수 초 이내)
```

📢 **섹션 요약 비유**: CDC는 '전화 요금 명세서'다 — 한 달 전화 기록 전체를 다시 보내는 게 아니라, 오늘 새로 발생한 통화 내역만 실시간으로 알려주는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 CDC 방식 3종 비교

| 방식 | 동작 원리 | DB 부하 | DELETE 감지 | 실시간성 |
|:---|:---|:---|:---|:---|
| **[트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 기반** | [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) → 변경 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 테이블 | 높음 | 가능 | 가능 |
| **타임스탬프 기반** | `WHERE updated_at > ?` | 중간 | 불가 | 준실시간 |
| **[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반** | DB [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 파싱 | 거의 없음 | 가능 | 실시간 |

### 2.2 MySQL Binlog 기반 CDC

MySQL의 Binlog(Binary Log)는 MySQL [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)([Replication](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))를 위해 모든 변경 사항을 기록하는 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)다.

```
MySQL 서버
├── InnoDB 스토리지
│   └── 실제 데이터 변경
└── Binlog (Binary Log)
    ├── ROW 이벤트: 행 수준 변경 상세 기록
    │   INSERT: 새 행의 모든 컬럼값
    │   UPDATE: 이전 행값(before) + 이후 행값(after)
    │   DELETE: 삭제된 행의 모든 컬럼값
    └── 이진 형식으로 순서 기록
```

**Binlog 형식 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)**:
```sql
-- MySQL Binlog 형식을 ROW로 설정 (CDC 필수)
SET GLOBAL binlog_format = 'ROW';
SET GLOBAL binlog_row_image = 'FULL';  -- 변경 전후 전체 컬럼 기록
```

### 2.3 PostgreSQL WAL (Write-Ahead Log) 기반 CDC

PostgreSQL은 WAL(Write-Ahead Log)을 통해 모든 변경을 기록한다. CDC는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)(Logical [Replication](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)) 슬롯을 통해 WAL을 읽는다.

```
PostgreSQL 서버
├── WAL (Write-Ahead Log)
│   └── 모든 변경 작업의 순서 기록
└── 논리 복제 슬롯 (Logical Replication Slot)
    └── Debezium이 이 슬롯을 통해 변경 스트림 구독
```

### 2.4 Debezium + [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) CDC 파이프라인

Debezium은 Red Hat이 개발한 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) CDC 플랫폼으로, [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect Source Connector로 동작한다.

```
┌─────────────────────────────────────────────────────────────┐
│                 CDC 파이프라인 전체 흐름                       │
│                                                             │
│  ┌──────────────┐    ┌───────────────────────────────────┐  │
│  │ MySQL/PgSQL  │    │        Kafka Connect               │  │
│  │  소스 DB     │    │  ┌─────────────────────────────┐  │  │
│  │              │    │  │   Debezium Source Connector  │  │  │
│  │  Binlog/WAL  │───►│  │  DB변경 → Kafka 이벤트 변환  │  │  │
│  │              │    │  └─────────────────────────────┘  │  │
│  └──────────────┘    └───────────────────┬───────────────┘  │
│                                          │                  │
│                       ┌──────────────────▼──────────────┐   │
│                       │         Apache Kafka             │   │
│                       │  토픽: dbserver.mydb.orders      │   │
│                       │  { op: "u", before: {...},       │   │
│                       │    after: {...}, ts_ms: ... }    │   │
│                       └──────────────────┬──────────────┘   │
│                                          │                  │
│              ┌───────────────────────────┼──────────────┐   │
│              ▼                           ▼              ▼   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────┐ │
│  │  DW (Snowflake)  │  │  Elasticsearch   │  │  캐시 DB  │ │
│  │  (Sink Connector)│  │  (검색 인덱스)   │  │  (Redis)  │ │
│  └──────────────────┘  └──────────────────┘  └───────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 2.5 Debezium 이벤트 구조

```json
{
  "op": "u",        // 연산 유형: c(create), u(update), d(delete), r(read/snapshot)
  "ts_ms": 1714000000000,
  "before": {       // 변경 전 행 데이터
    "order_id": 1001,
    "status": "pending",
    "amount": 5000
  },
  "after": {        // 변경 후 행 데이터
    "order_id": 1001,
    "status": "shipped",
    "amount": 5000
  },
  "source": {
    "db": "mydb",
    "table": "orders",
    "pos": 12345678  // Binlog 위치
  }
}
```

📢 **섹션 요약 비유**: Debezium은 DB의 '심전도 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)'다 — DB 심장(테이블)이 뛸 때마다(변경될 때마다) 파형(이벤트)을 기록하고 Kafka라는 종합 병원 기록 시스템으로 전송한다.

---

## Ⅲ. 비교 및 연결

### 3.1 CDC 활용 패턴

| 패턴 | 설명 | 도구 |
|:---|:---|:---|
| **실시간 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)** | [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)→[DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 실시간 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | Debezium + [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) + dbt |
| **캐시 무효화** | DB 변경 시 [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 캐시 자동 업데이트 | Debezium + [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) Sink |
| **[이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)** | DB 변경을 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 이벤트로 발행 | Debezium + [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) + [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) |
| **검색 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)** | DB 변경을 Elasticsearch에 즉시 반영 | Debezium + ES Sink |

### 3.2 CDC vs 기타 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 방법

| 방법 | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | DB 부하 | DELETE 처리 | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 |
|:---|:---|:---|:---|:---|
| **[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 CDC** | < 1초 | 없음 | 완벽 | 별도 처리 필요 |
| **DMS (AWS [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) Migration [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))** | 초 단위 | 낮음 | 완벽 | 자동 처리 |
| **JDBC [폴링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)** | 분 단위 | 중간 | 불가 | 자동 처리 |
| **DB 링크** | 즉시 | 높음 | 가능 | 수동 |

📢 **섹션 요약 비유**: [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 CDC는 우체국 배달부가 편지를 쓰는 순간 복사본을 만드는 것이다 — 우체통을 열어서 편지를 세는([폴링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)) 것이 아니라, 편지를 쓰는 펜 자국 자체를 복사한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 Debezium 운영 시 주의사항

| 항목 | 주의점 | 해법 |
|:---|:---|:---|
| **WAL 슬롯 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)** | 컨슈머가 느리면 WAL 슬롯 쌓임 → DB 디스크 풀 | 컨슈머 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 |
| **[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변화** | [DDL](/knowledge-base/studynote/05_database/01_db_architecture_relational/020_ddl/) 변경 시 이벤트 구조 불일치 | [Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/) [Registry](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) + Avro 사용 |
| **[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)** | 첫 실행 시 전체 테이블 [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) (부하) | 오프 피크 타임 [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) |
| **토픽 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/)** | 동일 키 변경 순서 보장 필요 | 기본키 기반 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) |

### 4.2 CDC 구축 단계

```
1단계: DB 설정
   MySQL: binlog_format=ROW, binlog_row_image=FULL
   PgSQL: wal_level=logical, max_replication_slots=5

2단계: Debezium 커넥터 배포
   Kafka Connect에 Debezium Connector 설정 JSON 배포
   소스 DB 연결 정보, 테이블 화이트리스트 설정

3단계: Kafka 토픽 확인
   dbserver.mydb.orders 토픽에 이벤트 수신 확인

4단계: Sink Connector 배포
   타겟 시스템(DW, Redis, ES)에 Sink Connector 설정
```

📢 **섹션 요약 비유**: CDC 파이프라인 구축은 '주민등록 변동 자동 통보 시스템'과 같다 — 주민등록 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(DB)가 바뀌면 관련 기관([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/), 캐시, 검색)에 자동으로 알림이 가고 각자 업데이트한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 CDC 도입 효과

| 효과 | 내용 |
|:---|:---|
| **실시간성** | 배치 대비 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 시간 단위 → 초 단위로 단축 |
| **DB 부하 감소** | [폴링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 제거로 소스 DB CPU 20~50% 절감 |
| **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)** | DELETE 포함 모든 변경 100% 캡처 |
| **아키텍처 단순화** | 여러 시스템에 동시 전파로 N개 배치 파이프라인 통합 |

### 5.2 결론 — 기술사 작성 포인트

기술사 답안에서는 **"CDC 3가지 방식의 비교와 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반이 유일한 프로덕션 표준인 이유"**를 명확히 서술하고, Debezium의 이벤트 구조(op·before·after)를 활용한 [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 기반 실시간 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 파이프라인을 [ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램으로 표현하면 차별화된 답안이 된다.

📢 **섹션 요약 비유**: CDC의 가치는 '영상 감시 카메라'에 있다 — 하루 치 녹화를 밤새 돌려보는(배치 복사) 대신, 이상 행동이 발생하는 그 순간(변경 이벤트)을 실시간으로 포착해 즉시 알린다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| CDC 구현체 | Debezium | [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect 기반 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) CDC |
| MySQL [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | Binlog (Binary Log) | MySQL [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), CDC 소스 |
| PostgreSQL [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | WAL (Write-Ahead Log) | PgSQL [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) |
| [이벤트 버스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/539_event_bus_stream_processing/) | [Apache Kafka](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) | CDC 이벤트 중개 플랫폼 |
| [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 관리 | [Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/) [Registry](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) | Avro/Protobuf [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 |
| 연관 패턴 | [이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) ([Event Sourcing](/knowledge-base/studynote/12_it_management/05_security_compliance/307_event_sourcing/)) | DB 변경을 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 이벤트로 발행 |

### 👶 어린이를 위한 3줄 비유 설명

1. CDC는 도서관 책이 빌려지거나 반납될 때마다 '딩동' 알림을 보내주는 시스템이야 — 매일 밤 전체 목록을 세는 게 아니라!

### 📈 관련 키워드 및 발전 흐름도

```text
배치 ETL (주기적 전체 복사)
    │
    ▼
CDC: 변경분만 실시간 캡처
    ├─► 로그 기반: MySQL Binlog · PostgreSQL WAL
    └─► Debezium: Kafka Connect 기반 CDC 커넥터
    │
    ▼
Outbox 패턴: 트랜잭션 보장 이벤트 발행
    │
    ▼
실시간 OLTP → OLAP 동기화 · 캐시 무효화
```
2. MySQL Binlog는 도서관의 '대출 기록지'야 — 어떤 책이 언제 누가 빌려갔고, 반납됐는지 순서대로 적혀 있어.
3. Debezium은 이 기록지를 읽어서 Kafka라는 방송 시스템으로 변환하는 '방송 번역사'야 — 그러면 여러 시스템이 동시에 소식을 들을 수 있어!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 217 / 258

← **이전**: [216. 람다 (Lambda) vs 카파 (Kappa) 아키텍처 배치·실시간](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)
**다음**: [218. NoSQL BASE (Basically Available, Soft-state, Eventually Consistent) 결과적](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/218_nosql_base_eventual_consistency_sharding/) →

---
