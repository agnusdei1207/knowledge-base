---
title: 180. CDC (Change Data Capture)와 Debezium 기반 Binlog 실시간 동기화
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[217_cdc_binlog_change_capture_debezium|CDC]] ([[217_cdc_binlog_change_capture_debezium|Change Data Capture]], [[218_cdc_change_data_capture|변경 데이터 캡처]])는 [[002_database_definition|데이터베이스]]([[501_database|Database]], DB)의 INSERT·UPDATE·DELETE를 [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]에서 읽어 순서 있는 변경 이벤트 스트림으로 바꾸는 기술이다.
> 2. **가치**: Debezium은 MySQL Binary Log (Binlog), PostgreSQL Write-Ahead Log (WAL) 같은 [[568_logs_distributed_logging_elk_fluentd|로그]]를 Kafka로 흘려 보내 [[209_data_warehouse_schema_on_write|DW]] ([[208_data_warehouse_schema_on_write_inmon|Data Warehouse]]), 검색 [[154_database_index_b_tree_search_optimization|인덱스]], 캐시, [[247_feature_label_variables|피처]] 스토어를 초 단위로 [[212_synchronization_mechanisms|동기화]]하게 해 준다.
> 3. **판단 포인트**: 실시간성보다 중요한 것은 **정확한 삭제 반영, 순서 보존, 재시작 [[658_ir_recovery|복구]], Sink의 멱등 반영**이며, 이를 위해 [[568_logs_distributed_logging_elk_fluentd|로그]] 기반 [[217_cdc_binlog_change_capture_debezium|CDC]]·[[022_snapshot_backup_architecture|스냅샷]] [[268_strategy_pattern|전략]]·[[005_schema|스키마]] 진화·키 설계를 함께 잡아야 한다.

---

## Ⅰ. 개요 및 필요성

CDC는 "원본 DB에 생긴 변화를 다른 시스템으로 언제, 얼마나 정확하게 옮길 것인가?"라는 문제에서 출발한다. 전통적인 배치 [[215_etl_vs_elt_pipeline|ETL]] (Extract, Transform, Load)은 하루 한 번 전체 테이블을 읽거나 `updated_at` 기준으로 증분을 가져와 DW에 적재한다. 이 방식은 구현이 단순하지만, [[001_dikw_pyramid|데이터]]가 이미 늦고 삭제가 빠지기 쉬우며 소스 DB에 스캔 부하를 준다.

특히 주문, 결제, 사용자 프로필처럼 계속 바뀌는 Online [[191_transaction_concept_states|Transaction]] Processing ([[327_hint_handoff|OLTP]]) [[001_dikw_pyramid|데이터]]에서는 "최종 상태만" 복사하는 방식이 부족하다. 오전 10시에 `A → B`, 10시 1분에 `B → C`로 바뀐 행을 밤 12시에 한 번 읽으면 중간 상태와 정확한 변경 순서를 잃는다. 검색 [[154_database_index_b_tree_search_optimization|인덱스]], 캐시 무효화, [[241_machine_learning_basics|머신러닝]](Machine [[240_switch_learning_forwarding_flooding|Learning]], ML) 온라인 [[247_feature_label_variables|피처]], 실시간 대시보드는 바로 이 중간 변화까지 필요로 하는 경우가 많다.

아래 그림은 전통 [[212_synchronization_mechanisms|동기화]]와 [[568_logs_distributed_logging_elk_fluentd|로그]] 기반 CDC의 차이를 보여 준다. 핵심은 CDC가 테이블을 반복 조회하는 것이 아니라, **이미 DB가 쓰고 있는 커밋 [[568_logs_distributed_logging_elk_fluentd|로그]]를 읽는다**는 점이다.

```text
┌──────────────────────────────────────────────────────────────┐
│ 전통 동기화 vs 로그 기반 CDC                                  │
├──────────────────────────────────────────────────────────────┤
│ Polling / Batch                                               │
│ Source DB ─▶ SELECT updated_at > t ─▶ ETL ─▶ Target          │
│   └─ full scan · delete 누락 · T+1 지연                      │
│                                                              │
│ Log-based CDC                                                 │
│ COMMIT ─▶ Binlog / WAL ─▶ Debezium ─▶ Kafka ─▶ Targets       │
│   └─ 순서 보존 · delete 캡처 · source 부하 최소화            │
└──────────────────────────────────────────────────────────────┘
```

그래서 CDC는 단순 [[016_replication_factor|복제]] 기술이 아니라, 운영계 [[001_dikw_pyramid|데이터]]를 분석계·검색계·이벤트계로 안전하게 확장하는 연결 계층이다. [[001_dikw_pyramid|데이터]] 엔지니어링 관점에서는 배치 [[015_지연_데이터_관점|지연]]을 줄이는 수단이고, [[348_mlops|MLOps]] ([[220_mlops_machine_learning_operations|Machine Learning Operations]]) 관점에서는 온라인·오프라인 [[001_dikw_pyramid|데이터]]의 시간 차를 줄이는 기반이 된다.

- **📢 섹션 요약 비유**: CDC는 창고 재고를 밤마다 다시 세는 방식이 아니라, 입고·출고가 일어날 때마다 CCTV로 바로 기록해 다른 창고에도 동시에 알려 주는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Debezium 기반 [[217_cdc_binlog_change_capture_debezium|CDC]] 파이프라인은 보통 네 층으로 이해하면 쉽다. **소스 [[568_logs_distributed_logging_elk_fluentd|로그]]**, **커넥터**, **메시지 [[344_bus|버스]]**, **반영 Sink** 층이다. 소스 DB는 [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]를 만들고, Debezium 커넥터는 그 [[568_logs_distributed_logging_elk_fluentd|로그]]를 읽어 이벤트로 변환하며, Apache Kafka는 이를 내구성 있는 스트림으로 보관하고 여러 소비자에게 전달한다. 마지막으로 Sink는 이 이벤트를 MERGE, UPSERT, 인덱싱, 캐시 무효화 같은 방식으로 반영한다.

| 구성 요소 | 역할 | 핵심 판단 |
| :--- | :--- | :--- |
| Binary Log / WAL | 커밋 순서와 행 변경 기록 보존 | 행 단위 [[568_logs_distributed_logging_elk_fluentd|로그]] [[009_config|설정]]과 보존 기간 필요 |
| Debezium Connector | [[568_logs_distributed_logging_elk_fluentd|로그]] 파싱 후 변경 이벤트 [[087_process_state_transition|생성]] | [[459_quic_fec_forward_error_correction|초기]] [[022_snapshot_backup_architecture|스냅샷]], 오프셋 관리, [[020_ddl|DDL]] 감지 |
| [[179_kafka_flink_watermark_time_window|Kafka]] Connect / [[179_kafka_flink_watermark_time_window|Kafka]] | 이벤트 전달·재시작·팬아웃 | 토픽 키, [[514_partition_slice_volume|파티션]], 재처리 [[268_strategy_pattern|전략]] 설계 |
| [[505_schema|Schema]] [[235_registry_immutable_tag|Registry]] | [[005_schema|스키마]] 진화 관리 | [[344_compatibility_usability|호환성]] [[164_policy|정책]] 없으면 Sink 연쇄 장애 발생 |
| Sink Applier | 타깃 시스템 반영 | 멱등 처리, upsert [[067_db_key_uniqueness_minimality|key]], delete [[164_policy|정책]] 필요 |

Debezium의 동작은 **[[459_quic_fec_forward_error_correction|초기]] [[022_snapshot_backup_architecture|스냅샷]]**과 **[[568_logs_distributed_logging_elk_fluentd|로그]] 스트리밍** 두 단계로 나뉜다. [[459_quic_fec_forward_error_correction|초기]] [[022_snapshot_backup_architecture|스냅샷]]은 현재 테이블 상태를 한 번 읽어 기준선을 만들고, 이후부터는 Binlog/WAL에서 들어오는 변경만 계속 전송한다. 이때 Debezium은 마지막으로 읽은 [[568_logs_distributed_logging_elk_fluentd|로그]] 위치를 저장해 재시작 뒤에도 이어서 읽을 수 있게 한다.

```text
┌──────────────────────────────────────────────────────────────┐
│ Debezium 동작 단계                                            │
├──────────────────────────────────────────────────────────────┤
│ 1) Initial Snapshot                                           │
│    Table Scan ─▶ op = r 이벤트 생성                           │
│                     │                                         │
│                     └─ 현재 로그 위치 기록                    │
│                                                              │
│ 2) Streaming Phase                                            │
│    Binlog / WAL ─▶ op = c / u / d 이벤트 ─▶ Kafka Topic      │
│                     │                                         │
│                     └─ Offset 저장 후 재시작 복구             │
└──────────────────────────────────────────────────────────────┘
```

이벤트 구조도 중요하다. Debezium 이벤트는 보통 `before`, `after`, `op`, `source`, `ts_ms` 정보를 가진다. `before/after`는 변경 전후 값을, `op`는 [[087_process_state_transition|생성]](Create)·수정(Update)·삭제(Delete)를, `source`는 [[568_logs_distributed_logging_elk_fluentd|로그]] 위치와 테이블 정보를 나타낸다. 그래서 Sink는 "지금 상태가 무엇인가"뿐 아니라 "무슨 이유로 바뀌었는가"를 기준으로 반영 [[164_policy|정책]]을 세울 수 있다.

다만 Debezium을 쓴다고 자동으로 [[401_transport_layer_role_end_to_end_multiplexing|end-to-end]] Exactly-Once가 보장되는 것은 아니다. [[179_kafka_flink_watermark_time_window|Kafka]] Connect와 Kafka는 재시작 [[658_ir_recovery|복구]]와 재전송에 강하지만, 최종 Sink가 중복 이벤트를 안전하게 처리하지 못하면 결과는 흔들릴 수 있다. 따라서 실무 핵심은 **소스 [[568_logs_distributed_logging_elk_fluentd|로그]]의 [[002_bigdata_5v|정확성]] + 커넥터 오프셋 [[658_ir_recovery|복구]] + Sink의 멱등 반영**을 하나의 체인으로 보는 것이다.

- **📢 섹션 요약 비유**: Debezium은 공장 컨베이어벨트의 감시 카메라와 같다. 물건이 언제 올라왔고, 무엇이 수정됐고, 무엇이 폐기됐는지를 순서대로 기록해 다른 창고가 같은 상태를 재현하도록 돕는다.

---

## Ⅲ. 비교 및 연결

CDC는 구현 방식에 따라 성격이 크게 달라진다. [[298_qkv_attention|쿼리]] 기반 증분은 가장 단순하지만 삭제 감지와 중간 상태 보존이 약하고, [[507_acid_properties|트리거]] 기반은 즉시성은 좋지만 원본 DB 부하와 운영 복잡도가 커진다. [[568_logs_distributed_logging_elk_fluentd|로그]] 기반 CDC가 현대 시스템에서 선호되는 이유는 **애플리케이션 코드 변경 없이, 커밋 순서를 유지한 채, 삭제까지 잡을 수 있기 때문**이다.

| 방식/개념 | Source of Truth | 장점 | 한계 | 잘 맞는 경우 |
| :--- | :--- | :--- | :--- | :--- |
| [[298_qkv_attention|쿼리]] 기반 증분 | 테이블 최종 상태 | 구현 단순 | delete 누락, 순서 손실, [[448_polling_programmed_io|폴링]] [[015_지연_데이터_관점|지연]] | 소규모 레거시 |
| [[507_acid_properties|트리거]] 기반 [[217_cdc_binlog_change_capture_debezium|CDC]] | 테이블 + [[507_acid_properties|트리거]] 테이블 | 즉시성 확보 가능 | DB 부하, [[507_acid_properties|트리거]] 관리 부담 | 제한적 시스템 연동 |
| [[568_logs_distributed_logging_elk_fluentd|로그]] 기반 [[217_cdc_binlog_change_capture_debezium|CDC]] | Binlog / WAL | 순서 보존, delete 캡처, source 부하 낮음 | DB [[009_config|설정]]·운영 지식 필요 | 프로덕션 실시간 [[212_synchronization_mechanisms|동기화]] |
| Outbox Pattern | 비즈니스 [[191_transaction_concept_states|트랜잭션]] + Outbox 테이블 | DB 저장과 이벤트 발행 [[193_atomicity_all_or_nothing|원자성]] 확보 | 앱 [[005_schema|스키마]] 설계 필요 | [[532_microservices_decomposition_patterns|마이크로서비스]] 이벤트 발행 |
| [[307_event_sourcing|Event Sourcing]] | 이벤트 저장소 자체 | 완전한 [[064_relation_domain|도메인]] 이력 | 모델 복잡도 높음 | 이벤트 중심 시스템 |

여기서 Outbox Pattern은 CDC와 자주 같이 등장한다. CDC가 "기존 테이블 변경을 읽는 기술"이라면, Outbox는 "[[064_relation_domain|도메인]] 이벤트를 안전하게 내보내기 위한 설계 패턴"이다. 즉 주문 테이블에 변경이 생겼다고 해서 항상 의미 있는 비즈니스 이벤트가 되는 것은 아니므로, [[532_microservices_decomposition_patterns|마이크로서비스]]에서는 주문 저장과 함께 outbox 테이블에 발행할 이벤트를 기록하고, Debezium이 그 outbox만 읽도록 만드는 경우가 많다.

또한 CDC는 [[146_lakehouse|레이크하우스]]([[146_lakehouse|Lakehouse]])와 ML [[247_feature_label_variables|피처]] 파이프라인에도 연결된다. 주문 변경이 Kafka로 들어오면 Bronze 영역에는 원본 변경 이벤트를 쌓고, Silver 영역에서는 최신 상태를 재구성하며, 온라인 [[247_feature_label_variables|피처]] 스토어는 초 단위로 최신 값을 공급할 수 있다. 이렇게 하면 배치 학습용 [[001_dikw_pyramid|데이터]]와 실시간 추론 입력 사이의 시차를 줄일 수 있다.

- **📢 섹션 요약 비유**: [[568_logs_distributed_logging_elk_fluentd|로그]] 기반 CDC와 Outbox의 차이는 CCTV와 우편 발송함의 차이와 같다. CCTV는 실제로 일어난 모든 움직임을 기록하고, Outbox는 밖으로 보내야 할 공식 편지만 따로 담아 두는 장치다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 도구 선택보다 **CDC가 실패하는 지점을 먼저 통제**해야 한다. 소스 DB [[009_config|설정]]이 잘못되면 아예 필요한 [[568_logs_distributed_logging_elk_fluentd|로그]]가 남지 않고, 테이블에 안정적인 키가 없으면 Sink가 중복을 제거하지 못하며, [[005_schema|스키마]] 진화가 통제되지 않으면 하류 파이프라인이 연쇄 실패한다.

대표적인 MySQL [[009_config|설정]] 예시는 아래와 같다. 핵심은 행 기반 [[568_logs_distributed_logging_elk_fluentd|로그]]와 충분한 [[568_logs_distributed_logging_elk_fluentd|로그]] 보존 기간이다.

```ini
[mysqld]
server-id=1
log_bin=mysql-bin
binlog_format=ROW
binlog_row_image=FULL
expire_logs_days=7
```

| 판단 항목 | 권장 선택 | 이유 |
| :--- | :--- | :--- |
| [[459_quic_fec_forward_error_correction|초기]] 적재가 큰 테이블 | `initial` 대신 증분 [[022_snapshot_backup_architecture|스냅샷]] 또는 별도 백필 검토 | 첫 [[022_snapshot_backup_architecture|스냅샷]]이 운영 부하와 [[015_지연_데이터_관점|지연]]을 키울 수 있음 |
| [[070_primary_key_alternate_key|기본 키]](Primary [[067_db_key_uniqueness_minimality|Key]])가 없음 | [[217_cdc_binlog_change_capture_debezium|CDC]] 대상에서 제외하거나 [[071_alternate_key|대체 키]] 설계 | 멱등 upsert와 delete 반영이 어려움 |
| 삭제 반영 필요 | [[300_schema_on_write_vs_read|tombstone]] 또는 명시적 delete [[164_policy|정책]] 유지 | 최신 상태 테이블과 이벤트 [[568_logs_distributed_logging_elk_fluentd|로그]]의 의미가 달라짐 |
| 다수 Sink 팬아웃 | [[179_kafka_flink_watermark_time_window|Kafka]] 토픽 키·[[005_schema|스키마]] [[235_registry_immutable_tag|레지스트리]] 고정 | 검색, [[209_data_warehouse_schema_on_write|DW]], 캐시가 같은 계약을 보게 해야 함 |
| 초단위 신선도 요구 | source commit 시각 vs sink 반영 시각 모니터링 | [[179_kafka_flink_watermark_time_window|Kafka]] lag만 보면 전체 [[015_지연_데이터_관점|지연]]을 놓칠 수 있음 |

운영 체크리스트는 다음과 같다.

1. Binlog/WAL 보존 기간이 장애 [[658_ir_recovery|복구]] 시간보다 충분히 긴가?
2. [[637_zfs_snapshot_cow_architecture|Snapshot]] 중에도 애플리케이션 쓰기와 일관성이 유지되는가?
3. Sink는 `UPSERT`나 `MERGE`로 중복 이벤트를 안전하게 처리하는가?
4. [[020_ddl|DDL]] ([[020_ddl|Data Definition Language]]) 변경 시 [[505_schema|Schema]] [[235_registry_immutable_tag|Registry]] [[344_compatibility_usability|호환성]] [[164_policy|정책]]이 있는가?
5. 테이블별 토픽 [[514_partition_slice_volume|파티션]] [[268_strategy_pattern|전략]]이 키 분산과 순서 보존 요구를 동시에 만족하는가?

흔한 안티패턴도 분명하다. `updated_at` [[448_polling_programmed_io|폴링]]을 "사실상 [[217_cdc_binlog_change_capture_debezium|CDC]]"라고 착각하는 경우, [[070_primary_key_alternate_key|기본 키]] 없는 테이블을 그대로 싱크에 밀어 넣는 경우, [[217_cdc_binlog_change_capture_debezium|CDC]] 이벤트를 중복 제거 없이 바로 집계 테이블에 합산하는 경우가 대표적이다. 기술사 답안에서는 단순히 "Debezium이 편하다"가 아니라, **[[568_logs_distributed_logging_elk_fluentd|로그]] [[009_config|설정]] → [[637_zfs_snapshot_cow_architecture|snapshot]] → offset [[658_ir_recovery|복구]] → sink [[171_idempotency_iac_terraform|멱등성]] → [[005_schema|스키마]] 진화**를 한 줄로 이어 설명해야 설계력이 드러난다.

- **📢 섹션 요약 비유**: [[217_cdc_binlog_change_capture_debezium|CDC]] 운영은 수도관을 여는 일보다 수압·밸브·역류 방지 장치를 함께 설계하는 일에 가깝다. 물이 흐르기만 하면 끝이 아니라, 끊겨도 다시 이어지고 새지도 않아야 한다.

---

## Ⅴ. 기대효과 및 결론

CDC를 잘 도입하면 OLTP와 [[211_olap_drill_down_roll_up_surrogate_key|Online Analytical Processing]] ([[316_olap|OLAP]]) 계층 사이의 시간 간격이 크게 줄어든다. 검색 [[154_database_index_b_tree_search_optimization|인덱스]]는 최신 주문 상태를 더 빨리 반영하고, DW는 새벽 배치 대신 근실시간 분석이 가능해지며, [[247_feature_label_variables|피처]] 스토어와 캐시는 최신 비즈니스 상태를 따라간다. 무엇보다 원본 시스템은 반복 조회 부하에서 어느 정도 해방된다.

하지만 CDC는 만능이 아니다. [[568_logs_distributed_logging_elk_fluentd|로그]] 보존이 끊기면 재동기화 비용이 커지고, 큰 [[022_snapshot_backup_architecture|스냅샷]]은 운영 부하를 만들며, 잘못된 [[005_schema|스키마]] 변경은 하류 전체를 무너뜨릴 수 있다. 또한 CDC는 "변경을 옮기는 기술"이지, 의미 없는 이벤트를 자동으로 비즈니스 가치로 바꾸는 기술은 아니다. 그래서 [[064_relation_domain|Domain]] Event 설계, Upsert [[164_policy|정책]], 품질 검증이 함께 따라가야 한다.

결론적으로 CDC는 DB를 이벤트 소스로 승격시키는 현실적인 방법이다. Debezium은 그 과정에서 [[568_logs_distributed_logging_elk_fluentd|로그]]를 안전한 스트림으로 바꾸는 표준 도구이고, Binlog/WAL은 그 스트림의 진짜 출발점이다. 이 둘을 제대로 이해하면 배치 중심 [[212_synchronization_mechanisms|동기화]]에서 실시간 [[001_dikw_pyramid|데이터]] 제품화로 자연스럽게 넘어갈 수 있다.

- **📢 섹션 요약 비유**: CDC는 매일 밤 장부를 다시 베끼는 일이 아니라, 거래가 일어나는 순간 거래 전표가 자동으로 복사돼 회계팀·물류팀·매장에 동시에 전달되는 시스템과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Binlog / WAL | DB 커밋 순서와 변경 내용을 담는 CDC의 출발점 |
| Debezium | [[568_logs_distributed_logging_elk_fluentd|로그]]를 변경 이벤트로 바꾸는 [[179_kafka_flink_watermark_time_window|Kafka]] Connect 기반 커넥터 |
| [[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]] | 변경 이벤트를 내구성 있게 팬아웃하는 메시지 [[344_bus|버스]] |
| [[505_schema|Schema]] [[235_registry_immutable_tag|Registry]] | [[217_cdc_binlog_change_capture_debezium|CDC]] 이벤트 [[005_schema|스키마]] 진화를 통제하는 계약 저장소 |
| Outbox Pattern | [[064_relation_domain|도메인]] 이벤트를 원자적으로 발행하기 위한 [[532_microservices_decomposition_patterns|마이크로서비스]] 패턴 |
| MERGE / UPSERT | 최신 상태 테이블에 CDC를 멱등 반영하는 핵심 연산 |
| [[165_feature_store_training_serving_consistency|Feature Store]] | [[217_cdc_binlog_change_capture_debezium|CDC]] 기반 최신 [[247_feature_label_variables|피처]]를 온라인 추론에 제공하는 소비자 계층 |

### 📈 관련 키워드 및 발전 흐름도

```text
OLTP 트랜잭션 커밋
    │
    ▼
Binlog / WAL 기록
    │
    ▼
Debezium CDC 이벤트 변환
    │
    ▼
Kafka Topic 축적 · 재전송
    │
    ├─▶ DW / Lakehouse 적재
    ├─▶ Search / Cache 동기화
    └─▶ Feature Store / Microservice 소비
```

이 흐름은 테이블 복사 중심 사고에서, 변경 이벤트를 여러 소비자가 재사용하는 실시간 [[001_dikw_pyramid|데이터]] 파이프라인으로의 전환을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. CDC는 책장에서 책이 빠지거나 새로 들어올 때마다 바로 기록하는 똑똑한 사서 메모장이에요.
2. Debezium은 그 메모장을 읽고 "이 책이 옮겨졌어!"라고 다른 방 친구들에게 바로 알려 주는 전달자예요.
3. 그래서 모두가 밤까지 기다리지 않고도 같은 책장 상태를 거의 바로 알 수 있어요.
