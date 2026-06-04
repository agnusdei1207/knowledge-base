---
title: "341. CDC 트랜잭션 변경 실시간 캡처 DB 이관 (Change Data Capture)"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) ([Change Data Capture](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/))는 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 전체를 다시 복사하지 않고, [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에 기록된 변경분만 순서대로 읽어 다른 시스템으로 전달하는 실시간 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 기법이다.
> 2. **가치**: 배치 이관보다 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간과 다운타임을 크게 줄여, 운영 DB·분석 플랫폼·검색 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)·이벤트 스트림을 같은 사실에 가깝게 맞출 수 있다.
> 3. **판단 포인트**: [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 CDC를 선택할 때는 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간보다 더 중요하게 순서 보장, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화, 중복 처리, 컷오버 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 함께 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

[CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) ([Change Data Capture](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/))는 원본 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 삽입·수정·삭제 이벤트를 감지해 후속 시스템으로 전달하는 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 방식이다. 운영 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 24시간 동작하는 환경에서는 전체 덤프와 일괄 적재만으로는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 신선도와 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 연속성을 동시에 만족시키기 어렵다. 특히 검색 색인, [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/), 캐시, [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 늘어날수록 “한 번 더 전체 복사”는 비용도 크고 장애 반경도 커진다.

그래서 현대 DevOps와 DataOps에서는 변경분만 흘려보내는 CDC가 핵심 연결 고리가 된다. 애플리케이션에서 이중 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(Dual Write)를 구현하면 코드 복잡도와 정합성 위험이 커지지만, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 CDC는 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)가 이미 보장하는 커밋 순서를 활용해 더 안정적인 연계를 만들 수 있다. 결국 CDC의 필요성은 “빠르게 옮기는 기술”보다 “운영 중인 시스템을 멈추지 않고 옮기는 기술”에 가깝다.

- **📢 섹션 요약 비유**: CDC는 도서관 전체 책장을 매일 복사하는 대신, 오늘 새로 들어오거나 수정된 카드만 기록해 다른 지점으로 보내는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CDC의 핵심 원리는 `트랜잭션 로그 읽기 -> 변경 이벤트 표준화 -> 순서 보장 전파 -> 대상 시스템 반영`이다. 구현은 보통 원본 DB의 Binlog/WAL을 읽는 커넥터, [이벤트 버스](/studynote/04_software_engineering/11_testing_validation/931_event_bus_stream_processing/), [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 관리, 소비자 애플리케이션으로 구성된다. 이때 중요한 것은 “어떤 행이 바뀌었는가”만이 아니라 “어떤 커밋 순서로 바뀌었는가”를 잃지 않는 것이다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 소스 DB [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) (Binlog/WAL) | 변경 사실의 원본 | [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 순서와 커밋 위치 관리 |
| [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 커넥터 | [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 이벤트로 변환 | Debezium, [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect, 재시작 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| 이벤트 스트림 | 다수 소비자에 fan-out | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간, 재처리 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| 타깃 시스템 | 검색·분석·[복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 대상 | 멱등 반영, Upsert, 삭제 전파 |

다음 그림은 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 CDC가 애플리케이션 이중 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)보다 안정적인 이유를 보여준다.

```text
+--------------+   binlog/WAL   +--------------+   ordered    +--------------+
| Source DB    | --------------> | CDC Connector| ------------> | Event Stream |
+--------------+                +--------------+              +--------------+
       |                                 |                             |
       | schema change                   | offset checkpoint           | replay
       v                                 v                             v
+--------------+                +--------------+              +--------------+
| Schema Reg.  |                | Offset Store |              | Target DB    |
+--------------+                +--------------+              +--------------+
```

이 구조에서 장애 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)의 기준은 “마지막으로 성공한 오프셋(offset)이 어디인가”다. 소비자가 중복 이벤트를 받을 수 있으므로 타깃 반영은 Upsert, [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 필드, 이벤트 키 기반 멱등 처리가 필수다. [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)가 자주 바뀌는 조직이라면 [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 자체보다 [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) Registry와 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 전체 안정성을 좌우한다.

- **📢 섹션 요약 비유**: 원본 장부를 읽어 거래 내역만 택배로 보내는 방식이라, 장부 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 순서를 잃지 않아야 회계가 맞는 것과 같다.

---

## Ⅲ. 비교 및 연결

CDC를 이해하려면 배치 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) (Extract, Transform, Load), 애플리케이션 이중 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), DB [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)와의 경계를 같이 봐야 한다. 겉보기에는 모두 “[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다른 곳으로 보내는 일”이지만, 운영 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)와 정합성 지점이 크게 다르다.

| 방식 | 장점 | 한계 |
| :--- | :--- | :--- |
| 배치 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) | 구현 단순, 대량 처리 최적화 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 큼, 컷오버 창 필요 |
| 애플리케이션 이중 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 코드에서 제어 가능 | 실패 시 정합성 깨짐, 코드 결합 증가 |
| [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) | 저지연, 커밋 순서 활용 | [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 권한, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화, 운영 난이도 |

또한 CDC는 [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)([Event Sourcing](/studynote/12_it_management/05_security_compliance/307_event_sourcing/)), [데이터 레이크하우스](/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/)([Data Lakehouse](/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/)), 검색 인덱싱, 캐시 워밍과도 연결된다. [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 관점에서는 배포와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이관을 분리해 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)를 줄이는 수단이고, [SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 관점에서는 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간(Lag), 재처리율, 실패 토픽을 관찰 가능한 운영 대상이다.

- **📢 섹션 요약 비유**: 배치가 밤마다 트럭 한 대로 몰아서 배송하는 방식이라면, CDC는 주문이 찍힐 때마다 컨베이어벨트로 흘려보내는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 CDC는 단순 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 도구가 아니라 “무중단 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전환” [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 일부로 설계해야 한다. 예를 들어 레거시 DB를 신규 클라우드 DB로 옮길 때는 전체 [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 적재 후 CDC로 변경분을 계속 따라잡다가, Lag가 충분히 작아졌을 때 짧은 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 중지 구간에서 최종 컷오버를 수행한다. 이 순서를 지키지 않으면 실시간 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 도구를 써도 마지막 순간의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유실 위험을 피하기 어렵다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 소스 DB [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 접근 권한과 보관 기간이 [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 재처리 요구를 충족하는가?
2. 타깃 반영 로직이 중복 이벤트에 대해 멱등한가?
3. [DDL](/studynote/05_database/01_db_architecture_relational/020_ddl/) 변경, 컬럼 추가/삭제, 타입 변경을 어떤 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 처리할 것인가?
4. Lag, Dead Letter [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/), [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)률을 관측할 대시보드가 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 애플리케이션 코드와 CDC를 동시에 쓰면서 어느 쪽이 정답인지 정의하지 않는 구조
- [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 이벤트를 그대로 업무 계약으로 노출해 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변경이 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애로 직결되는 구조
- 삭제 이벤트([Tombstone](/studynote/05_database/05_distributed_nosql_newsql/300_schema_on_write_vs_read/))를 무시해 검색 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)와 분석계가 원본과 영구적으로 어긋나는 구조

기술사 답안에서는 “실시간이라서 [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)”가 아니라 “무중단 이관·저지연 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)·재처리 가능한 운영 모델이 필요할 때 [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)”라고 판단선을 잡아야 한다.

- **📢 섹션 요약 비유**: 이사할 때 짐을 한 번에 들고 뛰는 것보다, 먼저 큰 짐을 옮긴 뒤 마지막 순간에 새로 생긴 짐만 챙겨 출발하는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 같다.

---

## Ⅴ. 기대효과 및 결론

CDC를 잘 설계하면 운영계와 분석계, 검색계, 이벤트 구독자가 거의 같은 시간축을 공유하게 된다. 그 결과 다운타임을 줄이면서도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용도를 높일 수 있고, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼이 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 출시 속도를 따라갈 수 있다. 특히 [데이터 제품](/studynote/16_bigdata/07_data_lake/154_data_product/)이 많아질수록 전체 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)보다 변경 기반 전달이 훨씬 경제적이다.

반대로 CDC는 “만능 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)”가 아니다. [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 접근 제약이 큰 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/), [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)가 매우 불안정한 시스템, 삭제·보정 규칙이 불명확한 조직에서는 운영 비용이 급증할 수 있다. 따라서 CDC는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 기술이면서 동시에 정합성과 관찰 가능성을 관리하는 운영 체계로 기억해야 한다.

- **📢 섹션 요약 비유**: 좋은 CDC는 수도관 전체를 매번 갈아엎는 것이 아니라, 어디서 새는지 바로 찾아 필요한 물만 정확히 보내는 배관 설계와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Debezium | [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 커넥터의 대표 구현 |
| [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Connect | [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 이벤트를 스트림으로 전달하는 통합 계층 |
| [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) [Registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) | [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화와 소비자 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 관리 |
| [Event Sourcing](/studynote/12_it_management/05_security_compliance/307_event_sourcing/) | 이벤트를 사실 원장으로 삼는 설계 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
Batch ETL
   |
   v
Log-based CDC
   |
   v
Event Streaming + Schema Registry
   |
   v
Zero-downtime Migration / Real-time Analytics
```

이 흐름은 “일괄 복사 -> 변경분 추적 -> 스트림 표준화 -> 무중단 활용”으로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이관 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 진화하는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 큰 공책을 매번 통째로 베끼지 않고, 오늘 바뀐 줄만 적어 친구에게 보내는 게 CDC예요.
2. 그래서 훨씬 빨리 맞출 수 있고, 공책을 닫아 두지 않아도 돼요.
3. 대신 어느 줄이 먼저 바뀌었는지 순서를 잃지 않는 게 아주 중요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 341 / 373

<- **이전**: [340. 카프카 분산 메시지 스트리밍 (Apache Kafka Topic Partition Offset Consumer Group ISR](/studynote/15_devops_sre/05_devsecops/340_pub_sub/)
**다음**: [342. 데이터 레이크하우스 스토리지·컴퓨팅·트랜잭션 (Data Lakehouse)](/studynote/11_design_supervision/06_exam_summary/342_process/) ->

---
