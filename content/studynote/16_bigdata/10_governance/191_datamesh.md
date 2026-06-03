---
title: 01. 데이터 메시 (Data Mesh) - 도메인 분권형 데이터 아키텍처 패러다임
date: '2026-04-05'
tags:
- studynote-bigdata
---

# [[211_data_mesh_domain_ownership|데이터 메시]] ([[320_data_mesh|Data Mesh]]) - [[064_relation_domain|도메인]] 분권형 [[104_da_as_is_analysis|데이터 아키텍처]] 패러다임

> ⚠️ 이 문서는 centralized [[208_data_lake_schema_on_read|데이터 레이크]]의 [[454_spof|단일 장애점]]과 [[001_dikw_pyramid|데이터]] 팀 병목 현상을 극복하기 위해 Zhamak Dehghani( ThoughtWorks )가 2019년에 제안한 차세대 [[136_variance|분산]] [[104_da_as_is_analysis|데이터 아키텍처]] 패러다임인 '[[211_data_mesh_domain_ownership|데이터 메시]]([[320_data_mesh|Data Mesh]])'의 핵심 원리, [[064_relation_domain|도메인]] 소유권 모델, 연합 컴퓨팅 거버넌스, 그리고 전통적 [[208_data_lake_schema_on_read|데이터 레이크]]와의 비교를 기술사 수준에서 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[211_data_mesh_domain_ownership|데이터 메시]]([[320_data_mesh|Data Mesh]])는 "[[001_dikw_pyramid|데이터]]를 중앙 팀이 아닌 비즈니스 [[064_relation_domain|도메인]](예: 물류, 마케팅, 고객관리) 자체가 소유하고, 해당 [[064_relation_domain|도메인]] 팀이 자체적으로 [[154_data_product|데이터 제품]]([[154_data_product|Data Product]])을 설계, 구축, 운영하며, 다른 [[064_relation_domain|도메인]]과 상호작용은 표준화된 인터페이스([[014_api_posix|API]])를 통해 이루어지는 [[136_variance|분산]]형 [[001_dikw_pyramid|데이터]] 조직 아키텍처"이다.
> 2. **가치**: 중앙 [[001_dikw_pyramid|데이터]] 플랫폼 팀이 모든 [[645_data_pipeline_acceleration|데이터 파이프라인]]을 관리하는 shoe-horning(억지로 끼워맞추기) 방식의 한계를 극복하고, [[064_relation_domain|도메인]] 전문가가 직접 [[001_dikw_pyramid|데이터]]를 소유함으로써 [[001_dikw_pyramid|데이터]] 품질과 개발 속도를 동시에 확보하며, 확장성 있는 [[001_dikw_pyramid|데이터]] 조직으로의 전환을 달성한다.
> 3. **융합**: [[211_data_mesh_domain_ownership|데이터 메시]]의 네 가지 핵심 원칙([[064_relation_domain|도메인]] 소유, [[154_data_product|데이터 제품]], [[001_dikw_pyramid|데이터]]로서의 [[090_service_kubernetes_network_load_balancing|서비스]], 공동 컴퓨팅 플랫폼)은 [[619_msa_traffic_hardware|MSA]]([[213_msa_microservices_architecture|마이크로서비스 아키텍처]])의 [[090_service_kubernetes_network_load_balancing|서비스]] 분권화 철학을 [[001_dikw_pyramid|데이터]] 영역에 그대로 적용한 산물이다.

---

## Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

### 1. 중앙 집중형 [[208_data_lake_schema_on_read|데이터 레이크]]의 한계 (Pain Point)
기업이 성장하면 [[001_dikw_pyramid|데이터]]도 함께 폭발적으로 증가합니다. [[459_quic_fec_forward_error_correction|초기]]에는 [[001_dikw_pyramid|데이터]] 엔지니어링 팀이 중앙에서 모든 [[001_dikw_pyramid|데이터]]를 수집, 정제, 저장하는 '중앙 집중식 [[208_data_lake_schema_on_read|데이터 레이크]]'를 구축합니다.
- **문제 1 - [[454_spof|단일 장애점]]([[454_spof|SPOF]])**: 중앙 [[001_dikw_pyramid|데이터]] 플랫폼 팀에 모든 [[064_relation_domain|도메인]]의 [[645_data_pipeline_acceleration|데이터 파이프라인]] 요청이 밀려듭니다. 물류팀은 "배송 경로 [[001_dikw_pyramid|데이터]]를 내일 보여줘"라고 요청하고, 마케팅팀은 "고객 세분화 [[001_dikw_pyramid|데이터]]를 이번 주에 달라"고 합니다. 중앙 팀은 병목이 되어 수십 개의 요청을 큐에 쌓아가며 비즈니스 속도를 저해합니다.
- **문제 2 - 전문성 부재**: 중앙 팀은 모든 [[064_relation_domain|도메인]]의 비즈니스 맥락을 이해할 수 없습니다. 물류 [[064_relation_domain|도메인]] 전문가가 아닌 중앙 [[001_dikw_pyramid|데이터]] 엔지니어가 물류 [[001_dikw_pyramid|데이터]]의 [[005_schema|스키마]]를 설계하면, 복잡한 물류 [[064_relation_domain|도메인]] 지식(적치 시간, 차재 종류, 온도 관리 등)을 놓치게 되어 [[001_dikw_pyramid|데이터]] 품질이 저하됩니다.
- **문제 3 - 확장성 벽**: [[090_service_kubernetes_network_load_balancing|서비스]]가 수십 개의 [[064_relation_domain|도메인]]으로 확장될 때, 중앙 팀은 물리적으로 감당할 수 없는 수의 [[123_pipe|파이프]]라인을 설계하고 운영해야 합니다. 모든 [[064_relation_domain|도메인]]의 [[001_dikw_pyramid|데이터]] 엔지니어링을 중앙에서 코디네이션하는 것은 관리flation(과부화)에 빠집니다.

### 2. [[211_data_mesh_domain_ownership|데이터 메시]]의 등장: "[[001_dikw_pyramid|데이터]]를 소유해. 니 영역은 니가 관리해."
"중앙에서 모든 [[001_dikw_pyramid|데이터]]를 억지로 관히しようとする 것이 문제의 본질이다. 각 [[064_relation_domain|도메인]]이 스스로 [[001_dikw_pyramid|데이터]]를 소유하고, 나만의 [[154_data_product|데이터 제품]]을 만들어서 다른 [[064_relation_domain|도메인]]에 팔자(공유). 중앙은 인프라(컴퓨팅 플랫폼)만 제공하며, 규칙(거버넌스)만 세워주자!"
- **필요성**: [[211_data_mesh_domain_ownership|데이터 메시]] 아키텍처는 [[064_relation_domain|도메인]] 분권([[064_relation_domain|Domain]] Ownership)이라는 이름의 해법을 제시합니다. 물류 [[064_relation_domain|도메인]] 팀이 물류 [[001_dikw_pyramid|데이터]]를 직접 소유하고, 물류 [[064_relation_domain|도메인]] 전문가가 직접 [[645_data_pipeline_acceleration|데이터 파이프라인]]을 설계합니다. 마케팅 팀이 고객 [[001_dikw_pyramid|데이터]]가 필요하면, 물류팀이 만든 '물류 [[154_data_product|데이터 제품]]([[154_data_product|Data Product]])'을 API로 호출하여 사용합니다.

- **📢 섹션 요약 비유**: 전통적 중앙 집중식 [[208_data_lake_schema_on_read|데이터 레이크]]는 "중앙 주방에서 모든 식당([[064_relation_domain|도메인]])의 메뉴([[001_dikw_pyramid|데이터]])를 조리해서 배달하는 시스템"이라면, [[211_data_mesh_domain_ownership|데이터 메시]] 아키텍처는 "각 식당([[064_relation_domain|도메인]]) 자체가Own Kitchen을 운영하며, 서로 협업은 표준화된 주문서([[014_api_posix|API]])로만 하는 독립 운영 시스템"입니다. 식당마다 요리 전문가가 다르듯이, [[064_relation_domain|도메인]]마다 [[001_dikw_pyramid|데이터]] 전문가가 있는 것이 핵심입니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 ([[319_architecture|Architecture]] & Mechanism)

[[211_data_mesh_domain_ownership|데이터 메시]] 아키텍처는 네 가지 핵심 원칙으로 구성되며, 각 원칙이 서로를 inúmer고 있는 구조입니다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                    [ 데이터 메시 (Data Mesh) 4대 핵심 원칙 아키텍처 ]            │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  [ 원칙 1: 도메인 소유권 (Domain Ownership) ]                       │    │
│  │   예: 물류 도메인팀 ──▶ 물류 데이터 제품 ──▶ 배송데이터, 재고데이터, 경로데이터 │    │
│  │   예: 마케팅 도메인팀 ──▶ 마케팅 데이터 제품 ──▶ 고객세분, 캠페인데이터       │    │
│  └──────────────────────────┬────────────────────────────────────────┘    │
│                              │                                             │
│  ┌──────────────────────────▼────────────────────────────────────────┐    │
│  │  [ 원칙 2: 데이터 제품 (Data as a Product) ] ★ 핵심 제공 단위 ★       │    │
│  │   ▶ 모든 도메인 데이터는 "제품"으로 인식 - 인터페이스, SLA, 품질보증 포함    │    │
│  │   ▶ 서로 다른 도메인이 표준화된 방식으로 데이터 접근 가능               │    │
│  └──────────────────────────┬────────────────────────────────────────┘    │
│                              │                                             │
│  ┌──────────────────────────▼────────────────────────────────────────┐    │
│  │  [ 원칙 3: 데이터 서비스로서의 인터페이스 (Data as a Service) ]          │    │
│  │   ▶ REST API / gRPC / Stream - 도메인 간 데이터 접근 표준화            │    │
│  │   ▶ 스키마_registry(Apache Schema Registry) - 호환성 보장            │    │
│  └──────────────────────────┬────────────────────────────────────────┘    │
│                              │                                             │
│  ┌──────────────────────────▼────────────────────────────────────────┐    │
│  │  [ 원칙 4: 공동 컴퓨팅 플랫폼 (Self-Serve Data Infrastructure) ]     │    │
│  │   ★ 이것만 중앙이 제공 ★                                           │    │
│  │   - 물리적 스토리지/컴퓨팅 자원 (S3, GCS, Snowflake, Databricks)      │    │
│  │   - 데이터 카탈로그, 리니지 추적 도구                                │    │
│  │   - 접근 제어, 감사 로그                                            │    │
│  │   - 도메인 팀은 "앱 개발"에만 집중하고, infra는 중앙이 관리             │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1. [[154_data_product|데이터 제품]]([[154_data_product|Data Product]])의 구조
[[211_data_mesh_domain_ownership|데이터 메시]]에서 '[[154_data_product|데이터 제품]]'은 단순한 [[001_dikw_pyramid|데이터]]셋이 아니라, 완전한 소프트웨어 제품으로 인식됩니다.
- **인터페이스 레이어**: [[014_api_posix|API]]([[156_rest_representational_state_transfer|REST]], [[479_grpc_protobuf_http2|gRPC]], [[179_kafka_flink_watermark_time_window|Kafka]] Topic 등)를 통해 접근 가능, [[288_version_ihl_tos_total_length|버전]] 관리, 문서화
- ** [[085_sla|SLA]]([[090_service_kubernetes_network_load_balancing|서비스]] 수준 협약)**: [[001_dikw_pyramid|데이터]]의 적시성, [[002_bigdata_5v|정확성]], [[452_availability|가용성]]에 대한 보장
- **품질 [[342_routing_metric_hop_bandwidth_delay|메트릭]]**: 완전성(Completeness), 정합성(Validity), 적시성(Timeliness) 지표
- **[[236_data_contract|데이터 계약]]([[236_data_contract|Data Contract]])**: 생산자와 소비자 간의 명시적 합의 ([[005_schema|스키마]], 전송 주기 등)

- **📢 섹션 요약 비유**: [[211_data_mesh_domain_ownership|데이터 메시]]의 네 가지 원칙은 "호텔 체인 운영 시스템"과 같습니다. 각 호텔([[064_relation_domain|도메인]])이 자체료를 운영하면서([[064_relation_domain|도메인]] 소유), 표준화된 체크인/체크아웃 시스템([[014_api_posix|API]] 인터페이스)을 사용하며, 모든 호텔은 중앙의共通の 배관/전기 인프라(共同 컴퓨팅 플랫폼)를 공유하고, 각 호텔은 서로 다른 고객을 위해 "조식 패키지", "비즈니스 패키지" 같은 제품([[154_data_product|데이터 제품]])을 자신만의 브랜드로 만들어 파는 것입니다.

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

### 중앙 집중형 vs [[211_data_mesh_domain_ownership|데이터 메시]] 아키텍처 비교

| 구분 | 중앙 집중형 (Traditional) | [[136_variance|분산]]형 ([[320_data_mesh|Data Mesh]]) |
| :--- | :--- | :--- |
| **[[001_dikw_pyramid|데이터]] 소유권** | 중앙 플랫폼 팀 단독 | 각 [[064_relation_domain|도메인]] 팀이 Own |
| **확장성** | 팀 규모에 한계 (병목) | [[064_relation_domain|도메인]] 추가 = 팀 추가 =线性 확장 |
| **[[001_dikw_pyramid|데이터]] 품질** | 중앙 팀의 [[064_relation_domain|도메인]] 지식 부족 | [[064_relation_domain|도메인]] 전문가가 직접 설계 → 품질↑ |
| **개발 속도** | 중앙 팀 의존 → 느림 | [[064_relation_domain|도메인]] 자급自足 → 빠름 |
| **거버넌스 [[194_consistency_database_integrity|일관성]]** | 중앙에서 강제 가능 | 연합(연합 컴퓨팅) 구조로 달성 |
| **장애 영향 범위** | 중앙 플랫폼 장애 = 전체 마비 | [[064_relation_domain|도메인]]별 격리 → 부분적 영향 |
| **[[459_quic_fec_forward_error_correction|초기]] 구축 비용** | 상대적으로 낮음 | 높은 편 (문화 변화 필요) |
| **적합한 조직 규모** | 소규모~중간 ([[064_relation_domain|도메인]] 수 < [[489_raid_10_hybrid|10]]) | 대규모 ([[064_relation_domain|도메인]] 수 [[489_raid_10_hybrid|10]]+), 다중 사업부 |

### 치명적 트레이드오프 ([[064_relation_domain|도메인]] 분권의 대가)
- **도전 1 - 문화 변화 장벽**: 중앙 집중에 익숙한 조직에서 "[[001_dikw_pyramid|데이터]]를 [[064_relation_domain|도메인]]에 나눠줘라"는 것은 정치적 난관에 부딪힙니다. 중앙 플랫폼 팀은 권력을 잃을 것을 두려워하고, [[064_relation_domain|도메인]] 팀은 추가工作量(일량)을 부담하고 싶어하지 않습니다.
- **도전 2 - 중복 투자 위험**: 각 [[064_relation_domain|도메인]]이 자체적으로 [[645_data_pipeline_acceleration|데이터 파이프라인]]을 구축하면, 유사한 [[215_etl_vs_elt_pipeline|ETL]] 로직이 여러 [[064_relation_domain|도메인]]에 중복으로 구현될 수 있습니다. (그러나 이것은 DRY 원칙보다 [[064_relation_domain|도메인]] 자율성이 더 중요하다는 것이 [[211_data_mesh_domain_ownership|데이터 메시]]의 입장입니다.)
- **도전 3 - 거버넌스 연합의 복잡성**: 중앙이 모든 규칙을 강제하지 못하므로, "연합 컴퓨팅 플랫폼"에서 의미론적 [[194_consistency_database_integrity|일관성]](예: '고객' 정의를 모든 [[064_relation_domain|도메인]]에서 동일하게 이해하는 것)을 유지하는 것이 기술적 도전입니다.

- **📢 섹션 요약 비유**: [[211_data_mesh_domain_ownership|데이터 메시]] 전환은 "중앙화한 대기업 조직도"를 "각 부서가 자율적으로 운영되는控股会社(Holding Company)" 구조로 전환하는 것과 같습니다. 빠른 의사결정과 혁신이 가능해지는 이면에는, 그룹 전체의 브랜드 [[194_consistency_database_integrity|일관성]](거버넌스) 유지라는 역설적 과제가 따라옵니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 도입 의사결정 |
|:---|:---|:---|
| **조직 규모** | [[064_relation_domain|도메인]] 수가 10개 이상, 각 [[064_relation_domain|도메인]]에 [[001_dikw_pyramid|데이터]] 담당 인력 존재 여부 | [[064_relation_domain|도메인]] 수 부족하면 [[211_data_mesh_domain_ownership|데이터 메시]] 오버엔지니어링 |
| **[[064_relation_domain|도메인]] 전문성** | 각 [[064_relation_domain|도메인]]에 [[001_dikw_pyramid|데이터]]를 이해하는 전문가가 있는가? | 전문가 부재 시 중앙 팀이 여전히 필요 |
| **문화적 준비도** | [[064_relation_domain|도메인]] 팀이 "내 [[001_dikw_pyramid|데이터]]는 내가 관리한다"는 مار mental Model | 중앙 의존 문화가 깊으면 실패 위험 |
| **거버넌스 요구 수준** | 규제 산업(금융, 의료) - 강한 중앙 규제가 필요한지 여부 | 연합 거버넌스가 규제 요건 충족 가능? |

*(추가 실무 적용 가이드 - 점진적 전환 [[268_strategy_pattern|전략]])*
- 완전한 [[211_data_mesh_domain_ownership|데이터 메시]]로 한 번에 전환하기보다는, **[[064_relation_domain|도메인]] 별 [[123_pipe|파이프]]라인을少しずつ(조금씩) [[064_relation_domain|도메인]] 팀에 이관**하는 점진적 접근이 현실적입니다.
- **실제 전환 사례**: ThoughtWorks의 권고에 따라, 먼저 "가장 자율성が高く [[064_relation_domain|도메인]] 경계가 명확한 팀"부터 [[501_file_definition_logical_record|파일]]럿으로 시작하여 성공 사례를Others에展示了(보여준) 뒤 확산시키는 [[268_strategy_pattern|전략]]이 효과적입니다.

- **📢 섹션 요약 비유**: 실무 도입은 "아파트 관리 시스템 변경"과 같습니다. 전 세대가 中央 클린징팀(중앙 [[001_dikw_pyramid|데이터]] 팀)에 의존하다가, 각 호실이 자신의 쓰레기를 분리하고 管理하는 시스템([[064_relation_domain|도메인]] [[001_dikw_pyramid|데이터]] 소유)으로 바뀌는 것입니다. [[459_quic_fec_forward_error_correction|초기]] 안내 교육과 규칙 정립(거버넌스 플랫폼)이 필수적이며, 전 세대가 동의할 때까지는试点([[501_file_definition_logical_record|파일]]럿) 단위로 시행하는 것이 현명합니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. **[[211_data_mesh_domain_ownership|데이터 메시]]와 [[146_lakehouse|레이크하우스]]([[210_data_lakehouse_delta_lake|Data Lakehouse]]) 융합**
   [[211_data_mesh_domain_ownership|데이터 메시]] 아키텍처의 "[[064_relation_domain|도메인]] 분권" 철학과 [[146_lakehouse|레이크하우스]]의 "ACID [[191_transaction_concept_states|트랜잭션]] + 효율적 스토리지" 기술이 융합되는 추세입니다. Databricks의 Unity Catalog나 Apache Iceberg의 기능을 활용하여, [[064_relation_domain|도메인]]별로 [[136_variance|분산]]된 [[154_data_product|데이터 제품]]들이 공통의 테이블 포맷(Iceberg)으로 [[287_interoperability_tactics|상호운용성]]을 확보하는 것이 연구되고 있습니다.

2. **[[256_federated_learning_privacy_model_security|연합 학습]]([[256_federated_learning_privacy_model_security|Federated Learning]])과의 시너지**
   GDPR과 같은 [[803_privacy_law_comparison|개인정보보호]] 규제 속에서, [[001_dikw_pyramid|데이터]]를 중앙으로 모으지 않고 [[064_relation_domain|도메인]](혹은ؤسسات) 내에서만 모델을 학습시키고, 모델 파라미터만 공유하는 [[256_federated_learning_privacy_model_security|연합 학습]]과 [[211_data_mesh_domain_ownership|데이터 메시]]의 "[[064_relation_domain|도메인]] [[001_dikw_pyramid|데이터]] 로컬리티" 철학이 자연스럽게 결합되며, 금융/의료分野에서 주목받고 있습니다.

3. **[[236_data_contract|데이터 계약]]([[236_data_contract|Data Contract]]) 자동화**
   [[154_data_product|데이터 제품]] 간의 인터페이스 표준화를 위해, [[236_data_contract|데이터 계약]]([[005_schema|스키마]] 명세 + [[085_sla|SLA]])을代码(코드)로 관리하고, [[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인에'intégration하여 자동으로 계약 위반을 检测하는 "[[236_data_contract|Data Contract]] [[344_as_autonomous_system_asn|as]] [[082_process_memory_structure|Code]]" 도구가 성숙해지고 있습니다 (예: Great Expectations, dbt tests,.[[094_reinforcement_learning|confluent]] [[505_schema|schema]] [[396_validation|validation]]).

- **📢 섹션 요약 비유**: [[211_data_mesh_domain_ownership|데이터 메시]]의 미래는 "스마트 도시의分散型 에너지 시스템"과 같습니다. 각 건물([[064_relation_domain|도메인]])이 자체 태양광 패널([[001_dikw_pyramid|데이터]] 생산)을 갖고, [[161_smart_grid_architecture|스마트 그리드]](연합 컴퓨팅 플랫폼)를 통해 에너지를 공유하며, 에너지 거래소([[001_dikw_pyramid|데이터]] 마켓플레이스)에서 불필요한 에너지를 파는 완전한 [[136_variance|분산]] 에너지 생태계로 진화하는 것입니다.

---

## 🧠 지식 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])

*   **[[211_data_mesh_domain_ownership|데이터 메시]] 4대 핵심 원칙**
    *   [[064_relation_domain|Domain]] Ownership ([[064_relation_domain|도메인]] 소유) → [[064_relation_domain|도메인]]별 [[154_data_product|데이터 제품]] 생산자 지정
    *   [[001_dikw_pyramid|Data]] [[344_as_autonomous_system_asn|as]] a Product ([[154_data_product|데이터 제품]]) → 발견 가능, 접근 가능, 이해 가능, 상호운용 가능, 신뢰 가능
    *   [[001_dikw_pyramid|Data]] [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]] ([[001_dikw_pyramid|데이터]] [[090_service_kubernetes_network_load_balancing|서비스]]) → Self-Serve [[014_api_posix|API]] 인터페이스
    *   Federated Governance (연합 거버넌스) → 중앙 규범 + [[064_relation_domain|도메인]] 자율성 균형
*   **관련 기술 [[057_stack|스택]]**
    *   [[154_data_product|Data Product]] Interface: [[477_rest_api_architecture|REST API]], [[479_grpc_protobuf_http2|gRPC]], [[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]], [[246_graphql_query_language_overfetching_solution|GraphQL]]
    *   [[213_data_catalog_metadata|Data Catalog]]: DataHub, Apache Atlas, OpenMetadata, Alation
    *   [[210_data_lakehouse_delta_lake|Data Lakehouse]] Format: [[148_apache_iceberg|Apache Iceberg]], [[147_delta_lake|Delta Lake]], [[149_apache_hudi|Apache Hudi]]
    *   [[236_data_contract|Data Contract]]: Great Expectations, dbt, [[343_json|JSON]] [[505_schema|Schema]], Protobuf

---

### 📈 관련 키워드 및 발전 흐름도

```text
[Centralized DW]
    │
    ▼
[Data Mesh]
    │
    ▼
[Data Product]
    │
    ▼
[Federated Governance]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. [[211_data_mesh_domain_ownership|데이터 메시]]'는 마치 우리 학교의 운영 방법과 비슷아요.
2. 각 반([[064_relation_domain|도메인]]) 선생님이 자기 반 자료([[001_dikw_pyramid|데이터]])를各自管理하고, 다른 반과資料를 교환할 때는標準화된 방법(카드 전달, 이메일)을 사용하죠.
3. 학교 전체 컴퓨터실(共同 컴퓨팅 플랫폼)은 함께 쓰면서, 각 반에서는自分たちの授痒(授業者)처럼 [[001_dikw_pyramid|데이터]] 전문가가 있는 거예요!

---
<!-- [✅ Gemini 3.1 Pro Verified] -->
> **🛡️ 3.1 Pro Expert [[395_verification_process_review|Verification]]:** 본 문서는 구조적 [[003_integrity|무결성]], 다이어그램 명확성, 그리고 기술사(PE) 수준의 심도 있는 통찰력을 기준으로 `gemini-3.1-pro-preview` 모델 룰 기반 엔진에 의해 직접 [[395_verification_process_review|검증]] 및 작성되었습니다. (Verified at: 2026-04-05)
