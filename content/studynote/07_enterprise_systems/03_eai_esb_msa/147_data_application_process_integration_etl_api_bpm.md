---
title: 147. 데이터·애플리케이션·프로세스 통합 (ETL / API / BPM)
date: '2026-04-19'
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 엔터프라이즈 통합은 [[136_variance|분산]]된 시스템 사이의 [[001_dikw_pyramid|데이터]]·기능·프로세스를 하나의 흐름으로 연결하는 것으로, **[[215_etl_vs_elt_pipeline|ETL]](Extract-Transform-Load)은 [[001_dikw_pyramid|데이터]] 통합**, **[[014_api_posix|API]]([[014_api_posix|Application Programming Interface]])와 [[389_mesh_topology|메시]]지는 애플리케이션 통합**, **[[199_bpm_business_process_management_orchestrator|BPM]]([[199_bpm_business_process_management_orchestrator|Business Process Management]])은 비즈니스 프로세스 통합**을 각각 담당한다.
> 2. **가치**: [[081_erp_enterprise_resource_planning|ERP]]·[[107_crm_customer_relationship_management|CRM]]·[[167_scm_software_configuration_management|SCM]]·레거시 시스템이 공존하는 엔터프라이즈 환경에서, [[002_silo_hyeonhyung|사일로]]([[002_silo_hyeonhyung|Silo]]) 구조를 허물고 **단일 정보 흐름([[119_gitops_single_source_of_truth|Single Source of Truth]])** 을 확보하는 통합 아키텍처의 핵심 기술 삼각형이다.
> 3. **판단 포인트**: [[001_dikw_pyramid|데이터]] 배치 이동이면 [[215_etl_vs_elt_pipeline|ETL]], [[009_real_time_system|실시간 시스템]] 간 호출이면 [[014_api_posix|API]]/[[389_mesh_topology|메시]]지, 사람+시스템의 복합 업무 흐름이면 BPM을 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

대기업 IT 환경은 수십~수백 개의 시스템이 독립적으로 발전해 온 [[002_silo_hyeonhyung|사일로]]([[002_silo_hyeonhyung|Silo]]) 구조다. 영업팀은 [[107_crm_customer_relationship_management|CRM]]([[026_three_c_analysis|Customer]] [[083_relationship_in_er_model|Relationship]] [[372_management|Management]]), 재무팀은 [[081_erp_enterprise_resource_planning|ERP]]([[081_erp_enterprise_resource_planning|Enterprise Resource Planning]]), 물류팀은 [[097_wms_warehouse_management_system|WMS]]([[097_wms_warehouse_management_system|Warehouse Management System]])를 각자 쓴다. 이 시스템들이 서로 [[001_dikw_pyramid|데이터]]를 공유하지 못하면 중복 입력, [[001_dikw_pyramid|데이터]] 불일치, 업무 [[015_지연_데이터_관점|지연]]이 발생한다.

통합은 세 수준에서 이루어진다:
- **[[001_dikw_pyramid|데이터]] 레벨**: 각 DB의 [[001_dikw_pyramid|데이터]]를 공통 저장소로 통합 → [[215_etl_vs_elt_pipeline|ETL]]
- **애플리케이션 레벨**: 시스템 간 기능 호출·[[389_mesh_topology|메시]]지 교환 → [[014_api_posix|API]], [[146_esb_enterprise_service_bus_architecture|ESB]]([[146_esb_enterprise_service_bus_architecture|Enterprise Service Bus]]), [[389_mesh_topology|메시]]지 큐
- **프로세스 레벨**: 사람+시스템+규칙을 아우르는 업무 흐름 자동화 → [[199_bpm_business_process_management_orchestrator|BPM]]

- **📢 섹션 요약 비유**: 엔터프라이즈 통합은 **'도시 지하에 상하수도·전기·통신 케이블을 매설하는 인프라 공사'** 와 같습니다. 건물(시스템)마다 우물을 따로 파는([[002_silo_hyeonhyung|사일로]]) 대신, 중앙 배관망(통합 미들웨어)으로 연결해 어느 건물에서나 물([[001_dikw_pyramid|데이터]])이 흐르도록 만드는 것입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 통합 유형 비교

```text
엔터프라이즈 통합 3계층

  ┌──────────────────────────────────────────────────────┐
  │  BPM (Business Process Management)                   │
  │  사람 + 시스템 + 규칙 → 업무 프로세스 자동화            │
  │  예: 구매 승인 → 발주 → 입고 → 정산 자동화              │
  └──────────────────┬───────────────────────────────────┘
                     │
  ┌──────────────────▼───────────────────────────────────┐
  │  애플리케이션 통합 (API / 메시지 / ESB)                │
  │  시스템 A ←─ REST API / MQ ─→ 시스템 B               │
  │  예: 주문 시스템 → 재고 확인 API → 배송 시스템          │
  └──────────────────┬───────────────────────────────────┘
                     │
  ┌──────────────────▼───────────────────────────────────┐
  │  데이터 통합 (ETL / ELT)                               │
  │  Source DB ─► Extract ─► Transform ─► Load ─► DW     │
  │  예: ERP·CRM 데이터 → 데이터 웨어하우스 적재            │
  └──────────────────────────────────────────────────────┘
```

### 2. [[215_etl_vs_elt_pipeline|ETL]](Extract-Transform-Load) 심화

**[[215_etl_vs_elt_pipeline|ETL]] 3단계**:
1. **Extract(추출)**: 소스 DB([[081_erp_enterprise_resource_planning|ERP]], [[107_crm_customer_relationship_management|CRM]], 외부 [[014_api_posix|API]], [[568_logs_distributed_logging_elk_fluentd|로그]] 등)에서 [[001_dikw_pyramid|데이터]] 읽기
2. **Transform(변환)**: [[266_data_cleansing|데이터 정제]]·표준화·가공 (null 처리, 코드 매핑, 집계 등)
3. **Load(적재)**: [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]([[209_data_warehouse_schema_on_write|DW]]) 또는 [[209_data_mart_kimball_star_schema|데이터 마트]]에 저장

```text
ETL 흐름
  ERP DB  ─┐
  CRM DB  ─┼─► Staging Area ─► Transform ─► DW / Data Mart
  API 데이터┘   (원본 임시 저장)   (정제·변환)   (분석 최적화 저장)
```

**[[034_elt|ELT]](Extract-Load-Transform)**: 클라우드 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]([[263_storage_compute_separation_bigquery|BigQuery]], [[541_cassandra|Snowflake]])의 대규모 연산 능력을 활용해 적재 후 변환. ETL과 순서가 다름.

### 3. [[014_api_posix|API]] 통합 vs. [[389_mesh_topology|메시]]지 통합

| 구분 | [[477_rest_api_architecture|REST API]] 통합 | [[389_mesh_topology|메시]]지 큐(MQ) 통합 |
|:---|:---|:---|
| 통신 방식 | 동기(Sync), 요청-응답 | 비동기(Async), 발행-구독 |
| [[195_coupling_levels|결합도]] | 강결합 (호출 시 수신자 가용 필요) | 약결합 (브로커 경유) |
| 실시간성 | 즉시 응답 | [[015_지연_데이터_관점|지연]] 가능 |
| 장애 전파 | 수신자 다운 → 호출자 실패 | 수신자 다운 시 큐에 보관 |
| 적합 상황 | 즉시 응답 필요, 단순 조회 | 비동기 이벤트, 고가용성 필요 |
| 도구 | [[461_http_stateless_connection_oriented|HTTP]] [[156_rest_representational_state_transfer|REST]], [[479_grpc_protobuf_http2|gRPC]] | RabbitMQ, [[179_kafka_flink_watermark_time_window|Kafka]], AWS SQS |

- **📢 섹션 요약 비유**: [[014_api_posix|API]] 통합은 **'전화 통화'** (즉시 연결, 응답 즉시 필요), [[389_mesh_topology|메시]]지 큐 통합은 **'우체통'** (편지 넣으면 나중에 읽음, 수신자 부재 시에도 편지 보관)입니다. 은행 이체는 전화([[014_api_posix|API]]), 쇼핑몰 주문 처리는 우체통([[389_mesh_topology|메시]]지)이 어울립니다.

---

## Ⅲ. 비교 및 연결

### 통합 방식 선택 기준

| 요구사항 | 권장 통합 방식 | 이유 |
|:---|:---|:---|
| 대용량 [[001_dikw_pyramid|데이터]]를 야간 배치로 [[209_data_warehouse_schema_on_write|DW]] 적재 | [[215_etl_vs_elt_pipeline|ETL]] | 배치 [[001_dikw_pyramid|데이터]] 이동 최적화 |
| [[081_erp_enterprise_resource_planning|ERP]] ↔ [[107_crm_customer_relationship_management|CRM]] 실시간 고객 정보 연동 | [[477_rest_api_architecture|REST API]] 또는 [[217_cdc_binlog_change_capture_debezium|CDC]] | 즉시성 요구 |
| 주문 → 재고 → 배송 연쇄 이벤트 | [[389_mesh_topology|메시]]지 큐 ([[179_kafka_flink_watermark_time_window|Kafka]]) | 비동기·높은 [[139_throughput|처리량]] |
| 구매 결재 → 발주 → 입고 → 정산 자동화 | [[199_bpm_business_process_management_orchestrator|BPM]] | 사람+시스템 복합 프로세스 |

### [[143_eai_enterprise_application_integration_hub|EAI]] vs. [[146_esb_enterprise_service_bus_architecture|ESB]] vs. [[542_api_gateway|API Gateway]]

| 구분 | [[143_eai_enterprise_application_integration_hub|EAI]] ([[143_eai_enterprise_application_integration_hub|Enterprise Application Integration]]) | [[146_esb_enterprise_service_bus_architecture|ESB]] ([[146_esb_enterprise_service_bus_architecture|Enterprise Service Bus]]) | [[542_api_gateway|API Gateway]] |
|:---|:---|:---|:---|
| 시대 | 1990년대 | 2000년대 | 2010년대~ |
| 구조 | [[142_point_to_point_integration_spaghetti|Point-to-Point]] → [[152_hub_dummy_switching_intelligent|Hub]]-and-Spoke | 중앙 [[344_bus|버스]] | [[532_microservices_decomposition_patterns|마이크로서비스]] 진입점 |
| 특징 | 독점 [[259_adapter_pattern_interface_wrapper|어댑터]] | XML/WS-* 기반 | [[156_rest_representational_state_transfer|REST]]/[[246_graphql_query_language_overfetching_solution|GraphQL]], 경량 |

- **📢 섹션 요약 비유**: EAI는 **'전화 교환수가 직접 연결'**, ESB는 **'PBX 교환기 [[152_hub_dummy_switching_intelligent|허브]]'**, [[014_api_posix|API]] Gateway는 **'클라우드 앱스토어 관문'** 입니다. 시대와 기술 복잡도에 따라 통합 방식이 진화했습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[199_bpm_business_process_management_orchestrator|BPM]] 핵심 [[603_component_independent_deployment_unit|컴포넌트]]

**[[199_bpm_business_process_management_orchestrator|BPM]]([[199_bpm_business_process_management_orchestrator|Business Process Management]])** 은 업무 프로세스를 모델링·자동화·[[229_monitor|모니터]]링·최적화하는 종합 체계다.

```text
BPM 구성 요소
  ┌──────────────────────────────────────────┐
  │  BPMN 모델 (Business Process Model & Notation)
  │  ↓
  │  BPMS (BPM Suite) — 프로세스 엔진 실행
  │  ↓
  │  사람 태스크 ─── 시스템 태스크 ─── 규칙 엔진
  │         ↓               ↓              ↓
  │  담당자 승인        API 호출        DR 결정
  └──────────────────────────────────────────┘
```

### 의사결정 [[435_checklist_based_testing|체크리스트]]

- **배치 대용량 [[001_dikw_pyramid|데이터]] 이동** → [[215_etl_vs_elt_pipeline|ETL]] (Informatica, dbt, Airbyte)
- **[[009_real_time_system|실시간 시스템]] 간 [[001_dikw_pyramid|데이터]] 연동** → [[217_cdc_binlog_change_capture_debezium|CDC]] ([[217_cdc_binlog_change_capture_debezium|Change Data Capture]]) + [[179_kafka_flink_watermark_time_window|Kafka]]
- **즉시 응답 필요 [[014_api_posix|API]] 통합** → [[477_rest_api_architecture|REST API]] / [[479_grpc_protobuf_http2|gRPC]]
- **비동기 이벤트 기반** → [[389_mesh_topology|메시]]지 큐 ([[179_kafka_flink_watermark_time_window|Kafka]], RabbitMQ)
- **복합 업무 프로세스 자동화** → [[199_bpm_business_process_management_orchestrator|BPM]] (Camunda, Activiti, IBM [[199_bpm_business_process_management_orchestrator|BPM]])

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

**[[142_point_to_point_integration_spaghetti|Point-to-Point]] 스파게티 통합**: n개 시스템을 1:1로 직접 연결하면 n*(n-1)/2개의 연결이 생겨 변경·장애 전파가 불가능해진다. [[146_esb_enterprise_service_bus_architecture|ESB]] 또는 [[014_api_posix|API]] Gateway를 통한 중앙화가 필수다.

- **📢 섹션 요약 비유**: [[142_point_to_point_integration_spaghetti|Point-to-Point]] 스파게티는 **'20명이 각자 19명과 전화선을 직접 연결한 것'** 입니다. 190개의 전화선이 뒤엉켜 한 선이 끊기면 어디가 문제인지 찾을 수 없습니다. 교환기([[146_esb_enterprise_service_bus_architecture|ESB]]) 하나에 모두 연결하면 20개의 선만 필요합니다.

---

## Ⅴ. 기대효과 및 결론

[[001_dikw_pyramid|데이터]]·애플리케이션·프로세스의 3계층 통합이 완성되면, 엔터프라이즈는 **실시간 단일 정보 관점(Single Pane of Glass)** 을 달성한다. ERP의 재고 변경이 즉시 [[107_crm_customer_relationship_management|CRM]] 영업 시스템에 반영되고, 배송 [[015_지연_데이터_관점|지연]] 이벤트가 자동으로 고객 알림 프로세스를 [[507_acid_properties|트리거]]하며, 모든 [[001_dikw_pyramid|데이터]]가 분석 플랫폼으로 실시간 흘러간다.

**한계**: 통합 복잡도 자체가 새로운 [[100_technical_debt_monitoring_release_policy|기술 부채]]가 된다. 중앙 [[344_bus|버스]]([[146_esb_enterprise_service_bus_architecture|ESB]])는 [[454_spof|단일 장애점]]([[454_spof|SPOF]])이 될 수 있고, [[215_etl_vs_elt_pipeline|ETL]] [[123_pipe|파이프]]라인은 소스 [[005_schema|스키마]] 변경 시 대규모 수정이 필요하다. [[538_event_driven_architecture_eda|이벤트 기반 아키텍처]]([[064_eda|EDA]])와 [[211_data_mesh_domain_ownership|데이터 메시]]([[320_data_mesh|Data Mesh]])가 이 문제를 [[136_variance|분산]]으로 해결하려는 최신 트렌드다.

[[215_etl_vs_elt_pipeline|ETL]]·[[014_api_posix|API]]·BPM은 "시스템을 연결하는 것"이 아니라 **"[[002_silo_hyeonhyung|사일로]]를 허물고 조직을 하나의 유기체로 만드는 것"** 이라는 [[268_strategy_pattern|전략]]적 관점으로 이해해야 한다.

- **📢 섹션 요약 비유**: 엔터프라이즈 통합은 **'흩어진 섬들 사이에 다리를 놓는 것'** 입니다. ETL은 물자([[001_dikw_pyramid|데이터]])를 실어 나르는 화물선, API는 실시간 연락하는 전화선, BPM은 섬들 간 협력 절차를 정한 협약서입니다. 세 가지가 모두 갖춰져야 비로소 섬들이 하나의 경제권(통합 엔터프라이즈)이 됩니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[215_etl_vs_elt_pipeline|ETL]] (Extract-Transform-Load)** | 대용량 배치 [[001_dikw_pyramid|데이터]] 통합; [[209_data_warehouse_schema_on_write|DW]]·BI 분석의 [[001_dikw_pyramid|데이터]] 공급 [[123_pipe|파이프]]라인 |
| **[[146_esb_enterprise_service_bus_architecture|ESB]] ([[146_esb_enterprise_service_bus_architecture|Enterprise Service Bus]])** | 시스템 간 [[389_mesh_topology|메시]]지 [[339_routing_overview_best_path_selection|라우팅]] 미들웨어; [[014_api_posix|API]] 기반으로 점차 대체 |
| **[[199_bpm_business_process_management_orchestrator|BPM]] ([[199_bpm_business_process_management_orchestrator|Business Process Management]])** | 사람+시스템+규칙을 아우르는 업무 프로세스 자동화 |
| **[[542_api_gateway|API Gateway]]** | [[213_msa_microservices_architecture|마이크로서비스 아키텍처]]에서 외부 요청 진입점 및 통합 관문 |
| **[[217_cdc_binlog_change_capture_debezium|CDC]] ([[217_cdc_binlog_change_capture_debezium|Change Data Capture]])** | DB 변경 이벤트를 실시간으로 감지해 연동하는 [[001_dikw_pyramid|데이터]] 통합 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
사일로(Silo) 시스템 난립
    │
    ▼
Point-to-Point 통합 (스파게티) → 복잡도 폭발
    │
    ▼
EAI → ESB (중앙 버스) → API Gateway (분산)
    │
    ├─► ETL → ELT → 실시간 CDC
    ├─► REST API / gRPC / GraphQL
    ├─► 메시지 큐 (Kafka, RabbitMQ)
    │
    ▼
BPM — 사람+시스템 복합 프로세스 자동화
    │
    ▼
EDA (Event-Driven Architecture) / Data Mesh (차세대)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 회사에는 영업팀, 창고팀, 재무팀이 각자 다른 컴퓨터 프로그램(시스템)을 써요. **[[215_etl_vs_elt_pipeline|ETL]]**은 각 팀의 [[001_dikw_pyramid|데이터]]를 모아 하나의 큰 보고서로 만드는 것, **[[014_api_posix|API]]**는 팀끼리 실시간으로 연락하는 것, **[[199_bpm_business_process_management_orchestrator|BPM]]**은 "주문 → [[396_validation|확인]] → 배송 → 결제" 과정을 자동으로 처리하는 규칙이에요!
2. 예전에는 모든 팀이 직접 전화([[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 통합)를 걸었는데, 선이 너무 복잡해져서 지금은 **교환기([[146_esb_enterprise_service_bus_architecture|ESB]]/[[542_api_gateway|API Gateway]])** 를 통해 체계적으로 연결해요.
3. 세 가지가 모두 갖춰지면 **회사 전체가 하나의 로봇처럼** 움직여요 — 고객이 주문하면 자동으로 재고가 줄고, 배송이 시작되고, 영수증이 발행됩니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 147 / 482

← **이전**: [[146_esb_enterprise_service_bus_architecture|146. ESB (Enterprise Service Bus) - 엔터프라이즈 서비스 버스]]
**다음**: [[148_soa_service_oriented_architecture|148. SOA (Service Oriented Architecture) - 서비스 지향 아키텍처 (2000년대 후반 엔터프라이즈 표준)]] →

---
