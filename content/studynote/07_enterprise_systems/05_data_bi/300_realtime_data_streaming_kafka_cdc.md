+++
title = "300. 실시간 데이터 스트리밍 (Kafka + CDC)"
date = 2026-03-04

[taxonomies]
tags = ["studynote-enterprise"]

[extra]
tags = ["studynote-enterprise"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 운영 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)(DB)에서 발생하는 변경 사항을 실시간으로 감지([CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/))하여, 고성능 [메시지 브로커](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/)([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/))를 통해 분석 시스템으로 즉시 전달하는 [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) 아키텍처다.
> 2. **가치**: 배치 방식의 고질적 문제인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 시차([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))를 초 단위로 줄여주며, 원천 DB에 가해지는 조회 부하를 최소화하면서도 완벽한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)를 실현한다.
> 3. **판단 포인트**: 실시간 마케팅, 부정 거래 탐지([FDS](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/267_gnn_fraud_detection_knowledge_graph/)), 동적 가격 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 등 즉각적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 반응이 사업의 성패를 가르는 현대 비즈니스 환경의 필수 인프라다.

---

## Ⅰ. 개요 및 필요성

전통적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통합은 주로 야간 배치(Batch)를 통해 이루어졌다. 하지만 비즈니스 환경이 실시간 대응 중심으로 변하면서, "어제 팔린 물건의 통계"가 아니라 "지금 장바구니에 담은 고객에게 쿠폰을 보내는 것"이 중요해졌다.

이를 위해 운영 DB에 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 날려 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 가져오는 방식 대신, DB [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 직접 읽어 변경분만 추출하는 <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/">CDC</a> (<a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/">Change Data Capture</a>)</strong> 기술과, 이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수천 개의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 안정적으로 퍼뜨리는 <strong><a href="/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/">카프카</a>(<a href="/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/">Kafka</a>)</strong>의 결합이 실시간 [데이터 아키텍처](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)의 표준이 되었다.

- **📢 섹션 요약 비유**: 신문이 나올 때까지 기다리는(Batch) 대신, 뉴스 속보가 발생할 때마다 스마트폰 알림(Streaming)으로 즉시 받아보는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

이 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인은 원천 DB -> [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 커넥터 -> [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) -> 타겟 시스템([DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/), [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/), App) 순으로 흐른다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">운영 DB (MySQL/Oracle)</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">CDC Engine (Debezium)</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">Kafka Topic</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">분석계/Application</div></div>
<div class="kb-diagram-note">(로그 기록: Binlog) (변경 이벤트 추출) (고속 분산 저장) (실시간 활용)</div>
</div>
</div>



| 주요 구성 요소 | 역할 | 핵심 특징 |
|:---|:---|:---|
| [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) (Debezium 등) | DB의 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 읽어 변경 감지 | 원천 DB에 SQL 부하를 주지 않음 (Log-based) |
| [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) (Broker) | 스트리밍 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 순서대로 저장 및 배분 | 높은 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))과 [결함 허용](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/296_fault_tolerance_architecture/)([Fault Tolerance](/knowledge-base/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/)) |
| [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect | 소스(Source)와 싱크(Sink) 시스템 연결 | 코딩 없이 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)만으로 이기종 DB 간 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 가능 |
| 스트림즈 (Streams) | 실시간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 가공 및 분석 | [윈도우 연산](/knowledge-base/studynote/16_bigdata/04_streaming/086_window_operations/), 조인 등 실시간 비즈니스 로직 처리 |

- **📢 섹션 요약 비유**: 요리사가 요리한 음식을 일일이 서빙하는 게 아니라, 컨베이어 벨트([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)) 위에 올려두면 손님(Consumer)들이 각자 필요한 음식을 실시간으로 집어가는 원리다.

---

## Ⅲ. 비교 및 연결

기존의 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 기반(Query-based) 방식과 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반(Log-based) CDC의 차이는 원천 시스템에 주는 영향도에서 결정된다.

| 항목 | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 기반 ([Polling](/knowledge-base/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/)) | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) ([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 연동) |
|:---|:---|:---|
| DB 부하 | 주기적인 [SELECT](/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/) 실행으로 부하 높음 | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)만 읽으므로 부하 거의 없음 |
| 감지 능력 | 삭제(Delete)된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 감지 어려움 | 모든 변경(Insert/Update/Delete) 완벽 감지 |
| 전송 속도 | [폴링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) 주기에 따라 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 발생 | 이벤트 발생 즉시 전송 (초저지연) |
| 복잡도 | 단순 구현 가능 | 별도의 [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 엔진 및 [카프카](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 클러스터 필요 |

이 아키텍처는 [이벤트 기반 아키텍처](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/538_event_driven_architecture_eda/)([EDA](/knowledge-base/studynote/12_it_management/02_itsm_itil/064_eda/))와 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)([MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)) 간의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 유지하는 '아웃박스 패턴(Outbox Pattern)'의 기술적 기반이 되기도 한다.

- **📢 섹션 요약 비유**: [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 기반은 5분마다 친구에게 "일어났니?"라고 묻는 것이라면, CDC는 친구가 눈을 뜨자마자 알람이 울리도록 센서를 달아둔 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 <strong>순서 보장(<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/277_semaphore_ordering/">Ordering</a>)</strong>과 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 유실 방지(At-least-once)</strong>가 가장 중요하다. 특히 금융권이나 주문 시스템에서는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 바뀌는 순서가 어긋나면 치명적인 오류가 발생할 수 있다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 원천 DB의 부하 때문에 주간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)가 불가능한 상황인가?
2. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 삭제 이력까지 실시간으로 분석계에 반영해야 하는가?
3. [카프카](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)의 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)) 키를 적절히 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 순서를 보장했는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- [카프카](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 토픽의 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 무분별하게 늘리는 것. [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)은 늘어날 수 있으나, 동일한 키를 가진 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(예: 특정 사용자 ID)의 순서가 뒤섞여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성이 깨질 수 있다.

- **📢 섹션 요약 비유**: 줄을 서서 음식을 받는데, 빨리 주겠다고 줄을 무시하고 음식을 내주면 먼저 주문한 사람이 나중에 음식을 받는 혼란이 생기는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

실시간 스트리밍 아키텍처는 기업을 <strong>'살아 움직이는 유기체'</strong>로 만든다. 현장에서 발생하는 모든 사건이 즉시 뇌(분석 시스템)로 전달되어 대응할 수 있기 때문이다. [카프카](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)와 CDC의 결합은 단순한 기술 도입이 아니라, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 없애 비즈니스 기회 손실을 막는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 선택이다.

결론적으로, 이 기술은 [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)과 실시간 엔터프라이즈(RTE)를 실현하는 혈관이며, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델이 최신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 학습해 즉각적으로 반응하게 만드는 핵심 동력이다.

- **📢 섹션 요약 비유**: 강물이 끊임없이 흘러 바다로 가듯, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 고이지 않고 실시간으로 흐르게 하여 항상 깨끗하고 신선한 인사이트를 유지하는 것이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Debezium | 가장 널리 쓰이는 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 엔진 |
| [Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/) [Registry](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) | 스트리밍되는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 형식을 관리하여 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을 보장하는 도구 |
| [람다](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)/[카파 아키텍처](/knowledge-base/studynote/16_bigdata/04_streaming/096_kappa_architecture/) | 배치와 스트리밍을 어떻게 조합할지에 대한 아키텍처 설계 패턴 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">배치 ETL - 야간 처리, T+1 데이터 지연</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">메시지 큐 (RabbitMQ) - 실시간 이벤트 전달</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Apache Kafka - 분산 로그 스트리밍 플랫폼</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">CDC (Change Data Capture) - DB 변경 이벤트 캡처</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Kafka + Debezium + Flink 실시간 스트리밍 파이프라인</div>
</div>
</div>



> **키워드**: [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/), [Change Data Capture](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/), Debezium, [Stream Processing](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/), Real-Time [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/), Flink

### 👶 어린이를 위한 3줄 비유 설명
1. 장난감 가게에 새 장난감이 들어올 때까지 기다리는 건 너무 지루해요.
2. 그래서 장난감이 상자에 담기자마자 나에게 바로 알려주는 마법 벨을 달았어요.
3. 벨이 울리자마자 달려가면 누구보다 먼저 새 장난감을 가지고 놀 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 300 / 482

← **이전**: [299. 스파크 RDD (Resilient Distributed Dataset)](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/299_spark_rdd_resilient_distributed_dataset/)
**다음**: [301. 카프카 토픽 파티셔닝 기반 컨슈머 그룹 부하 분산 (Kafka Topic Partition Consumer Group)](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/301_kafka_topic_partition_consumer_group/) →

---
