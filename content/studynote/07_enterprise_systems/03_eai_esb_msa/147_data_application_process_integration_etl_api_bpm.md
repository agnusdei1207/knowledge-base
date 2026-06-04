---
title: "147. 데이터·애플리케이션·프로세스 통합 (ETL / API / BPM)"
date: "2026-04-19"
tags:
  - "studynote-enterprise-systems"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 엔터프라이즈 통합은 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)된 시스템 사이의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·기능·프로세스를 하나의 흐름으로 연결하는 것으로, <strong><a href="/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/">ETL</a>(Extract-Transform-Load)은 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 통합</strong>, <strong><a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a>(<a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">Application Programming Interface</a>)와 <a href="/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/">메시</a>지는 애플리케이션 통합</strong>, <strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/199_bpm_business_process_management_orchestrator/">BPM</a>(<a href="/studynote/07_enterprise_systems/03_eai_esb_msa/199_bpm_business_process_management_orchestrator/">Business Process Management</a>)은 비즈니스 프로세스 통합</strong>을 각각 담당한다.
> 2. **가치**: [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)·[CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/)·[SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/)·레거시 시스템이 공존하는 엔터프라이즈 환경에서, [사일로](/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)([Silo](/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)) 구조를 허물고 <strong>단일 정보 흐름(<a href="/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">Single Source of Truth</a>)</strong> 을 확보하는 통합 아키텍처의 핵심 기술 삼각형이다.
> 3. **판단 포인트**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 배치 이동이면 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/), [실시간 시스템](/studynote/02_operating_system/01_overview_architecture/009_real_time_system/) 간 호출이면 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)/[메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지, 사람+시스템의 복합 업무 흐름이면 BPM을 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

대기업 IT 환경은 수십~수백 개의 시스템이 독립적으로 발전해 온 [사일로](/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)([Silo](/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)) 구조다. 영업팀은 [CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/)([C고객](/studynote/12_it_management/01_governance_strategy/820_three_c_analysis/) [Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/)), 재무팀은 [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)([Enterprise Resource Planning](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)), 물류팀은 [WMS](/studynote/07_enterprise_systems/02_erp_systems/097_wms_warehouse_management_system/)([Warehouse Management System](/studynote/07_enterprise_systems/02_erp_systems/097_wms_warehouse_management_system/))를 각자 쓴다. 이 시스템들이 서로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 공유하지 못하면 중복 입력, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치, 업무 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 발생한다.

통합은 세 수준에서 이루어진다:
- <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 레벨</strong>: 각 DB의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 공통 저장소로 통합 -> [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)
- **애플리케이션 레벨**: 시스템 간 기능 호출·[메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 교환 -> [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/)([Enterprise Service Bus](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/)), [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐
- **프로세스 레벨**: 사람+시스템+규칙을 아우르는 업무 흐름 자동화 -> [BPM](/studynote/07_enterprise_systems/03_eai_esb_msa/199_bpm_business_process_management_orchestrator/)

- **📢 섹션 요약 비유**: 엔터프라이즈 통합은 **'도시 지하에 상하수도·전기·통신 케이블을 매설하는 인프라 공사'** 와 같습니다. 건물(시스템)마다 우물을 따로 파는([사일로](/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)) 대신, 중앙 배관망(통합 미들웨어)으로 연결해 어느 건물에서나 물([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 흐르도록 만드는 것입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 통합 유형 비교

```text
엔터프라이즈 통합 3계층

  +------------------------------------------------------+
  |  BPM (Business Process Management)                   |
  |  사람 + 시스템 + 규칙 -> 업무 프로세스 자동화            |
  |  예: 구매 승인 -> 발주 -> 입고 -> 정산 자동화              |
  +------------------+-----------------------------------+
                     |
  +------------------v-----------------------------------+
  |  애플리케이션 통합 (API / 메시지 / ESB)                |
  |  시스템 A <-- REST API / MQ --> 시스템 B               |
  |  예: 주문 시스템 -> 재고 확인 API -> 배송 시스템          |
  +------------------+-----------------------------------+
                     |
  +------------------v-----------------------------------+
  |  데이터 통합 (ETL / ELT)                               |
  |  Source DB -► Extract -► Transform -► Load -► DW     |
  |  예: ERP·CRM 데이터 -> 데이터 웨어하우스 적재            |
  +------------------------------------------------------+
```

### 2. [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)(Extract-Transform-Load) 심화

<strong><a href="/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/">ETL</a> 3단계</strong>:
1. **Extract(추출)**: 소스 DB([ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/), [CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/), 외부 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 등)에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 읽기
2. **Transform(변환)**: [데이터 정제](/studynote/07_enterprise_systems/05_data_bi/266_data_cleansing/)·표준화·가공 (null 처리, 코드 매핑, 집계 등)
3. **Load(적재)**: [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)) 또는 [데이터 마트](/studynote/14_data_engineering/05_exam_keywords/209_data_mart_kimball_star_schema/)에 저장

```text
ETL 흐름
  ERP DB  -+
  CRM DB  -+-► Staging Area -► Transform -► DW / Data Mart
  API 데이터+   (원본 임시 저장)   (정제·변환)   (분석 최적화 저장)
```

<strong><a href="/studynote/14_data_engineering/01_infrastructure/034_elt/">ELT</a>(Extract-Load-Transform)</strong>: 클라우드 [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([BigQuery](/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/), [Snowflake](/studynote/05_database/04_transactions_concurrency/541_cassandra/))의 대규모 연산 능력을 활용해 적재 후 변환. ETL과 순서가 다름.

### 3. [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 통합 vs. [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 통합

| 구분 | [REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) 통합 | [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐(MQ) 통합 |
|:---|:---|:---|
| 통신 방식 | 동기(Sync), 요청-응답 | 비동기(Async), 발행-구독 |
| [결합도](/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) | 강결합 (호출 시 수신자 가용 필요) | 약결합 (브로커 경유) |
| 실시간성 | 즉시 응답 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 가능 |
| 장애 전파 | 수신자 다운 -> 호출자 실패 | 수신자 다운 시 큐에 보관 |
| 적합 상황 | 즉시 응답 필요, 단순 조회 | 비동기 이벤트, 고가용성 필요 |
| 도구 | [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/), [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) | RabbitMQ, [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), AWS SQS |

- **📢 섹션 요약 비유**: [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 통합은 **'전화 통화'** (즉시 연결, 응답 즉시 필요), [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐 통합은 **'우체통'** (편지 넣으면 나중에 읽음, 수신자 부재 시에도 편지 보관)입니다. 은행 이체는 전화([API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)), 쇼핑몰 주문 처리는 우체통([메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지)이 어울립니다.

---

## Ⅲ. 비교 및 연결

### 통합 방식 선택 기준

| 요구사항 | 권장 통합 방식 | 이유 |
|:---|:---|:---|
| 대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 야간 배치로 [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 적재 | [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) | 배치 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 최적화 |
| [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) ↔ [CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) 실시간 고객 정보 연동 | [REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) 또는 [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) | 즉시성 요구 |
| 주문 -> 재고 -> 배송 연쇄 이벤트 | [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐 ([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)) | 비동기·높은 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) |
| 구매 결재 -> 발주 -> 입고 -> 정산 자동화 | [BPM](/studynote/07_enterprise_systems/03_eai_esb_msa/199_bpm_business_process_management_orchestrator/) | 사람+시스템 복합 프로세스 |

### [EAI](/studynote/07_enterprise_systems/03_eai_esb_msa/143_eai_enterprise_application_integration_hub/) vs. [ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/) vs. [API Gateway](/studynote/04_software_engineering/11_testing_validation/934_api_gateway/)

| 구분 | [EAI](/studynote/07_enterprise_systems/03_eai_esb_msa/143_eai_enterprise_application_integration_hub/) ([Enterprise Application Integration](/studynote/07_enterprise_systems/03_eai_esb_msa/143_eai_enterprise_application_integration_hub/)) | [ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/) ([Enterprise Service Bus](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/)) | [API Gateway](/studynote/04_software_engineering/11_testing_validation/934_api_gateway/) |
|:---|:---|:---|:---|
| 시대 | 1990년대 | 2000년대 | 2010년대~ |
| 구조 | [Point-to-Point](/studynote/07_enterprise_systems/03_eai_esb_msa/142_point_to_point_integration_spaghetti/) -> [Hub](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)-and-Spoke | 중앙 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) | [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 진입점 |
| 특징 | 독점 [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) | XML/WS-* 기반 | [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/)/[GraphQL](/studynote/06_ict_convergence/03_cloud_infrastructure/246_graphql_query_language_overfetching_solution/), 경량 |

- **📢 섹션 요약 비유**: EAI는 **'전화 교환수가 직접 연결'**, ESB는 <strong>'PBX 교환기 <a href="/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/">허브</a>'</strong>, [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Gateway는 **'클라우드 앱스토어 관문'** 입니다. 시대와 기술 복잡도에 따라 통합 방식이 진화했습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [BPM](/studynote/07_enterprise_systems/03_eai_esb_msa/199_bpm_business_process_management_orchestrator/) 핵심 [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)

<strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/199_bpm_business_process_management_orchestrator/">BPM</a>(<a href="/studynote/07_enterprise_systems/03_eai_esb_msa/199_bpm_business_process_management_orchestrator/">Business Process Management</a>)</strong> 은 업무 프로세스를 모델링·자동화·[모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링·최적화하는 종합 체계다.

```text
BPM 구성 요소
  +------------------------------------------+
  |  BPMN 모델 (Business Process Model & Notation)
  |  v
  |  BPMS (BPM Suite) — 프로세스 엔진 실행
  |  v
  |  사람 태스크 --- 시스템 태스크 --- 규칙 엔진
  |         v               v              v
  |  담당자 승인        API 호출        DR 결정
  +------------------------------------------+
```

### 의사결정 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- <strong>배치 대용량 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 이동</strong> -> [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) (Informatica, dbt, Airbyte)
- <strong><a href="/studynote/02_operating_system/01_overview_architecture/009_real_time_system/">실시간 시스템</a> 간 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 연동</strong> -> [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) ([Change Data Capture](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)) + [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)
- <strong>즉시 응답 필요 <a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a> 통합</strong> -> [REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) / [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/)
- **비동기 이벤트 기반** -> [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐 ([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), RabbitMQ)
- **복합 업무 프로세스 자동화** -> [BPM](/studynote/07_enterprise_systems/03_eai_esb_msa/199_bpm_business_process_management_orchestrator/) (Camunda, Activiti, IBM [BPM](/studynote/07_enterprise_systems/03_eai_esb_msa/199_bpm_business_process_management_orchestrator/))

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

<strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/142_point_to_point_integration_spaghetti/">Point-to-Point</a> 스파게티 통합</strong>: n개 시스템을 1:1로 직접 연결하면 n*(n-1)/2개의 연결이 생겨 변경·장애 전파가 불가능해진다. [ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/) 또는 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Gateway를 통한 중앙화가 필수다.

- **📢 섹션 요약 비유**: [Point-to-Point](/studynote/07_enterprise_systems/03_eai_esb_msa/142_point_to_point_integration_spaghetti/) 스파게티는 **'20명이 각자 19명과 전화선을 직접 연결한 것'** 입니다. 190개의 전화선이 뒤엉켜 한 선이 끊기면 어디가 문제인지 찾을 수 없습니다. 교환기([ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/)) 하나에 모두 연결하면 20개의 선만 필요합니다.

---

## Ⅴ. 기대효과 및 결론

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·애플리케이션·프로세스의 3계층 통합이 완성되면, 엔터프라이즈는 **실시간 단일 정보 관점(Single Pane of Glass)** 을 달성한다. ERP의 재고 변경이 즉시 [CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) 영업 시스템에 반영되고, 배송 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트가 자동으로 고객 알림 프로세스를 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)하며, 모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 분석 플랫폼으로 실시간 흘러간다.

**한계**: 통합 복잡도 자체가 새로운 [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)가 된다. 중앙 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)([ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/))는 [단일 장애점](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)([SPOF](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/))이 될 수 있고, [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인은 소스 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 시 대규모 수정이 필요하다. [이벤트 기반 아키텍처](/studynote/04_software_engineering/09_cloud_native_ai_architecture/538_event_driven_architecture_eda/)([EDA](/studynote/12_it_management/02_itsm_itil/064_eda/))와 [데이터 메시](/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)([Data Mesh](/studynote/12_it_management/05_security_compliance/320_data_mesh/))가 이 문제를 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)으로 해결하려는 최신 트렌드다.

[ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)·[API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)·BPM은 "시스템을 연결하는 것"이 아니라 <strong>"<a href="/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/">사일로</a>를 허물고 조직을 하나의 유기체로 만드는 것"</strong> 이라는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 관점으로 이해해야 한다.

- **📢 섹션 요약 비유**: 엔터프라이즈 통합은 **'흩어진 섬들 사이에 다리를 놓는 것'** 입니다. ETL은 물자([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 실어 나르는 화물선, API는 실시간 연락하는 전화선, BPM은 섬들 간 협력 절차를 정한 협약서입니다. 세 가지가 모두 갖춰져야 비로소 섬들이 하나의 경제권(통합 엔터프라이즈)이 됩니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/">ETL</a> (Extract-Transform-Load)</strong> | 대용량 배치 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통합; [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)·BI 분석의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공급 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 |
| <strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/">ESB</a> (<a href="/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/">Enterprise Service Bus</a>)</strong> | 시스템 간 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 미들웨어; [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 기반으로 점차 대체 |
| <strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/199_bpm_business_process_management_orchestrator/">BPM</a> (<a href="/studynote/07_enterprise_systems/03_eai_esb_msa/199_bpm_business_process_management_orchestrator/">Business Process Management</a>)</strong> | 사람+시스템+규칙을 아우르는 업무 프로세스 자동화 |
| <strong><a href="/studynote/04_software_engineering/11_testing_validation/934_api_gateway/">API Gateway</a></strong> | [마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/)에서 외부 요청 진입점 및 통합 관문 |
| <strong><a href="/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/">CDC</a> (<a href="/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/">Change Data Capture</a>)</strong> | DB 변경 이벤트를 실시간으로 감지해 연동하는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통합 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
사일로(Silo) 시스템 난립
    |
    v
Point-to-Point 통합 (스파게티) -> 복잡도 폭발
    |
    v
EAI -> ESB (중앙 버스) -> API Gateway (분산)
    |
    +-► ETL -> ELT -> 실시간 CDC
    +-► REST API / gRPC / GraphQL
    +-► 메시지 큐 (Kafka, RabbitMQ)
    |
    v
BPM — 사람+시스템 복합 프로세스 자동화
    |
    v
EDA (Event-Driven Architecture) / Data Mesh (차세대)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 회사에는 영업팀, 창고팀, 재무팀이 각자 다른 컴퓨터 프로그램(시스템)을 써요. <strong><a href="/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/">ETL</a></strong>은 각 팀의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 모아 하나의 큰 보고서로 만드는 것, <strong><a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a></strong>는 팀끼리 실시간으로 연락하는 것, <strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/199_bpm_business_process_management_orchestrator/">BPM</a></strong>은 "주문 -> [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) -> 배송 -> 결제" 과정을 자동으로 처리하는 규칙이에요!
2. 예전에는 모든 팀이 직접 전화([P2P](/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) 통합)를 걸었는데, 선이 너무 복잡해져서 지금은 <strong>교환기(<a href="/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/">ESB</a>/<a href="/studynote/04_software_engineering/11_testing_validation/934_api_gateway/">API Gateway</a>)</strong> 를 통해 체계적으로 연결해요.
3. 세 가지가 모두 갖춰지면 **회사 전체가 하나의 로봇처럼** 움직여요 — 고객이 주문하면 자동으로 재고가 줄고, 배송이 시작되고, 영수증이 발행됩니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 147 / 482

<- **이전**: [146. ESB (Enterprise Service Bus) - 엔터프라이즈 서비스 버스](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/)
**다음**: [148. SOA (Service Oriented Architecture) - 서비스 지향 아키텍처 (2000년대 후반 엔터프라이즈 표준)](/studynote/07_enterprise_systems/03_eai_esb_msa/148_soa_service_oriented_architecture/) ->

---
