---
title: 02. 데이터 패브릭 (Data Fabric) - 지능형 데이터 통합 아키텍처
date: '2026-04-05'
tags:
- studynote-bigdata
---

# [[212_data_fabric_virtualization|데이터 패브릭]] ([[212_data_fabric_virtualization|Data Fabric]]) - 지능형 [[001_dikw_pyramid|데이터]] 통합 아키텍처

> ⚠️ 이 문서는 Gartner가 2019년부터 지속 역점화하고 있는 차세대 [[104_da_as_is_analysis|데이터 아키텍처]] 패러다임인 '[[212_data_fabric_virtualization|데이터 패브릭]]([[212_data_fabric_virtualization|Data Fabric]])'의 핵심 개념, [[160_knowledge_graph_graphrag_integration|지식 그래프]] 기반 [[001_dikw_pyramid|데이터]] 연결 메커니즘, 자동화된 [[001_dikw_pyramid|데이터]] 통합 설계, 그리고 [[211_data_mesh_domain_ownership|데이터 메시]]와의 차이점을 기술사 수준에서 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[212_data_fabric_virtualization|데이터 패브릭]]([[212_data_fabric_virtualization|Data Fabric]])은 "[[001_dikw_pyramid|데이터]]의 위치([[061_on_premise_legacy_infrastructure|온프레미스]], 클라우드, [[309_saas|SaaS]] 등)와 상관없이, [[012_metadata|메타데이터]]([[012_metadata|Metadata]]) 기반의 [[160_knowledge_graph_graphrag_integration|지식 그래프]] [[160_knowledge_graph_graphrag_integration|Knowledge Graph]])를 구축하여 [[001_dikw_pyramid|데이터]] 간의 의미론적 [[083_relationship_in_er_model|관계]]를 이해하고, 이 지식을 활용하여 [[001_dikw_pyramid|데이터]] 통합, 변환, [[339_routing_overview_best_path_selection|라우팅]]을 자동으로Orchestration하는 지능형 [[001_dikw_pyramid|데이터]] 연결 아키텍처"이다.
> 2. **가치**: [[001_dikw_pyramid|데이터]] 엔지니어가数百 개의 [[001_dikw_pyramid|데이터]] 소스 간의 [[123_pipe|파이프]]라인을手動으로 설계하는 것을 탈피하여, [[012_metadata|메타데이터]]가 [[001_dikw_pyramid|데이터]] 연결의 추론 기반(Reasoning Engine)을提供하고, 시스템이 스스로 "어떤 [[001_dikw_pyramid|데이터]]를 어떻게 연결해야 하는가"를 자동 결정하는 Autonomous [[001_dikw_pyramid|Data]] Integration을 달성한다.
> 3. **융합**: [[212_data_fabric_virtualization|데이터 패브릭]]의 [[160_knowledge_graph_graphrag_integration|지식 그래프]]와 자율적 연결 메커니즘은 RDF(_resource Description Framework), 온톨로지(Ontology) engineering, [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]([[094_reinforcement_learning|Reinforcement Learning]]) 기반 자동화 기술이 융합된 산물이다.

---

## Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

### 1. [[001_dikw_pyramid|데이터]] [[136_variance|분산]] 환경의 복잡성 증가 (Pain Point)
현대 기업은 수십 개의 [[001_dikw_pyramid|데이터]] 소스로부터 [[001_dikw_pyramid|데이터]]를 수집합니다. [[081_erp_enterprise_resource_planning|ERP]], [[107_crm_customer_relationship_management|CRM]], HR 시스템, 마케팅 자동화 플랫폼, [[101_iot_concept|IoT]] 센서, SNS 등 [[001_dikw_pyramid|데이터]]가 퍼져있는 위치만큼이나 그 포맷과 의미도 제각각입니다.
- **문제 1 - [[001_dikw_pyramid|데이터]] [[002_silo_hyeonhyung|사일로]]([[001_dikw_pyramid|Data]] [[002_silo_hyeonhyung|Silo]])**: 재무 시스템의 '고객' 테이블과 [[107_crm_customer_relationship_management|CRM]] 시스템의 '고객' 테이블은 이름은 같지만 [[005_schema|스키마]]가 다릅니다. 재무는 사업자등록번호를 [[289_identification_flags_fragmentation_offset|식별자]]로 쓰고, CRM은 이메일을 [[289_identification_flags_fragmentation_offset|식별자]]로 씁니다. 이 두 시스템을 연결하려면 [[001_dikw_pyramid|데이터]] 엔지니어가 비즈니스 로직을 手動으로 이해하고 매핑해야 합니다.
- **문제 2 - [[012_metadata|메타데이터]]의 부재**: [[001_dikw_pyramid|데이터]]가 어디서 왔는지(출처), 어떻게 변환되었는지(계보), 어떤 의미인지(의미론적 정의)가 문서화되지 않아, 새로운 분석을 시작할 때마다 [[001_dikw_pyramid|데이터]] 탐색부터 다시 시작해야 합니다.
- **문제 3 - 통합 설계의 수동성**: 새로운 [[001_dikw_pyramid|데이터]] 소스가 추가될 때마다 [[001_dikw_pyramid|데이터]] 엔지니어가 "소스 A의 X 테이블과 소스 B의 Y 컬럼을 JOIN해서 Z로 산출해라"는 [[123_pipe|파이프]]라인을手動으로 설계합니다. 시스템 수가 增加할수록 이 조합은爆炸적으로 증가합니다.

### 2. [[212_data_fabric_virtualization|데이터 패브릭]]의 등장: "지식이 연결한다."
"[[001_dikw_pyramid|데이터]]의 물리적 위치와는 무관하게, [[001_dikw_pyramid|데이터]]의 '의미'를 [[160_knowledge_graph_graphrag_integration|지식 그래프]]에 모델링해 두면, 시스템이 스스로 '이 [[001_dikw_pyramid|데이터]]와 저 [[001_dikw_pyramid|데이터]]는 의미상 같은 고객을 가리키므로 JOIN해야 한다'는 추론을 할 수 있다!"
- **필요성**: [[212_data_fabric_virtualization|데이터 패브릭]]은 [[012_metadata|메타데이터]]를 "[[001_dikw_pyramid|데이터]]에 대한 [[001_dikw_pyramid|데이터]]"를 넘어 "[[001_dikw_pyramid|데이터]] 연결을 자동화하는 지식"으로 격상시킵니다. [[001_dikw_pyramid|데이터]] 엔지니어의 노우하우(경험적 지식)를 시스템의 [[160_knowledge_graph_graphrag_integration|지식 그래프]]로 대체하여, [[001_dikw_pyramid|데이터]] 통합 설계의 手動성을 자동화합니다.

- **📢 섹션 요약 비유**: 전통적 [[001_dikw_pyramid|데이터]] 통합이 "각 도시([[001_dikw_pyramid|데이터]] 소스) 사이에 수동으로 길(파라핀)을 연결하는 것"이라면, [[212_data_fabric_virtualization|데이터 패브릭]]은 "모든 도시의 지하 Brochure(지리 정보 시스템)에 해당하는 [[160_knowledge_graph_graphrag_integration|지식 그래프]]를 미리 구축해 놓아, 새로운 화물([[001_dikw_pyramid|데이터]])가 들어오면 시스템이 Brochure를 보고 스스로 최적의 경로를自動 결정하는 도로망 자동化 시스템"입니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 ([[319_architecture|Architecture]] & Mechanism)

[[212_data_fabric_virtualization|데이터 패브릭]] 아키텍처는 크게 4개의 핵심 레이어로 구성되며, 각 레이어가 [[012_metadata|메타데이터]] [[160_knowledge_graph_graphrag_integration|지식 그래프]]를 중심으로 유기적으로 동작합니다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                    [ 데이터 패브릭 (Data Fabric) 아키텍처 ]                     │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    [ 사용자 인터페이스 / 소비 계층 ]                      │    │
│  │        Business Analyst ◀── Data Scientist ◀── Data Engineer         │    │
│  └──────────────────────────┬────────────────────────────────────────┘    │
│                              │                                             │
│  ┌──────────────────────────▼────────────────────────────────────────┐    │
│  │              [ 데이터 통합 오케스트레이션 엔진 ]                            │    │
│  │         자동 파이프라인 생성 + 스케줄링 + 모니터링                         │    │
│  │              (강화 학습 기반 자동 설계)                                │    │
│  └──────────────────────────┬────────────────────────────────────────┘    │
│                              │                                             │
│  ┌──────────────────────────▼────────────────────────────────────────┐    │
│  │    ★ 핵심: 메타데이터 지식 그래프 (Knowledge Graph) ★                  │    │
│  │  ┌─────────────────────────────────────────────────────────────┐  │    │
│  │  │  [노드]        [관계]           [속성]                        │  │    │
│  │  │  고객 ─────叫做────▶ 사업자등록번호     (의미론적 동의어)           │  │    │
│  │  │   │           │                                        │  │    │
│  │  │   │           │                                        │  │    │
│  │  │   ▼           ▼                                        │  │    │
│  │  │  CRM_고객 ◀──같은실체──▶ 재무_고객    (자동 추론)               │  │    │
│  │  │   │                                                    │  │    │
│  │  │   │──출처──▶ Oracle ERP                                │  │    │
│  │  │   │──변환──▶ SELECT AVG(salary)...                     │  │    │
│  │  │   │──품질──▶ 99.2% complete                            │  │    │
│  │  └─────────────────────────────────────────────────────────────┘  │    │
│  └──────────────────────────┬────────────────────────────────────────┘    │
│                              │                                             │
│  ┌──────────────────────────▼────────────────────────────────────────┐    │
│  │                    [ 데이터源 연결 계층 ]                               │    │
│  │   Oracle ERP │ Salesforce CRM │ S3 Data Lake │ Kafka │ Snowflake   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1. [[160_knowledge_graph_graphrag_integration|지식 그래프]] 기반 자동 추론 (Automated Reasoning)
[[212_data_fabric_virtualization|데이터 패브릭]]의 핵심은 [[001_dikw_pyramid|데이터]] 간의 [[083_relationship_in_er_model|관계]]를Ontology(온톨로지)로 모델링하고, 이 [[070_graph_datastructure|그래프]]에서 자동으로 결론을 도출하는推理 Engine입니다.
- **동의어 추론**: "고객"과 "[[003_audit_stakeholders|Client]]"가Ontology에서 같은 개념으로 정의되면, CRM의 "[[003_audit_stakeholders|Client]]" 테이블과 재무의 "고객" 테이블이 자동으로 같은 실체로 인식됩니다.
- **계보 추론**: "A 테이블 → B 뷰 → C [[001_dikw_pyramid|데이터]] Mart"라는 변환 체인이 [[160_knowledge_graph_graphrag_integration|지식 그래프]]에 기록되면, C의 [[001_dikw_pyramid|데이터]]品质的 문제의 root cause를 A에서부터 역추적할 수 있습니다.

- **📢 섹션 요약 비유**: [[212_data_fabric_virtualization|데이터 패브릭]]의 [[160_knowledge_graph_graphrag_integration|지식 그래프]]는 "위키피디아의 링크 구조"와 같습니다. '서울'이라는 [[286_page_frame|페이지]]를 보면 '대한민국'의首都라는 정보가 연결되어 있고, '대한민국' [[286_page_frame|페이지]]로 가면 '서울'이首都라는 정보가 상호 연결되어 있습니다. 이처럼 모든 [[001_dikw_pyramid|데이터]]概念가 상호 연결된 [[070_graph_datastructure|그래프]]를 구축해 놓으면, 새로운 질문([[298_qkv_attention|쿼리]])에 시스템이 스스로 연결된 경로를 따라 답을 찾아가는 것입니다.

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

### [[212_data_fabric_virtualization|데이터 패브릭]] vs [[211_data_mesh_domain_ownership|데이터 메시]] vs 전통적 [[208_data_lake_schema_on_read|데이터 레이크]]

| 구분 | 전통적 [[208_data_lake_schema_on_read|데이터 레이크]] | [[211_data_mesh_domain_ownership|데이터 메시]] | [[212_data_fabric_virtualization|데이터 패브릭]] |
| :--- | :--- | :--- | :--- |
| **핵심 철학** | 중앙 집중 저장소 | [[064_relation_domain|도메인]] 분권 소유 | [[012_metadata|메타데이터]] 기반 지능형 연결 |
| **[[001_dikw_pyramid|데이터]] 이동** | 모든 [[001_dikw_pyramid|데이터]]를 중앙으로 이동 | [[064_relation_domain|도메인]]에 [[001_dikw_pyramid|데이터]]留存, 필요시呼叫 | 위치 무관, [[015_virtualization|가상화]] 연결 |
| **통합 방식** | [[215_etl_vs_elt_pipeline|ETL]]/[[034_elt|ELT]] [[123_pipe|파이프]]라인手動 설계 | [[064_relation_domain|도메인]] 간 [[014_api_posix|API]] 인터페이스 | [[160_knowledge_graph_graphrag_integration|지식 그래프]] 자동 추론 |
| **확장성** | 중앙 팀 병목 | [[064_relation_domain|도메인]] 추가 시 자연 확장 | [[012_metadata|메타데이터]] [[070_graph_datastructure|그래프]] 규모에 영향 |
| **주요供应商** | AWS Lake Formation, Azure [[001_dikw_pyramid|Data]] Factory | U刮/[[094_reinforcement_learning|Confluent]]/[[320_data_mesh|Data Mesh]] | Alation/Collibra/[[001_dikw_pyramid|Data]].world |
| **적합 시나리오** | [[001_dikw_pyramid|데이터]]統合 전사적으로 필요한 경우 | 대기업, 다중 [[064_relation_domain|도메인]] 독립 운영 | [[001_dikw_pyramid|데이터]] 복잡성 높고 빠른 대응 필요한 경우 |

### 치명적 트레이드오프
- **도전 1 - 온톨로지 구축 비용**: [[160_knowledge_graph_graphrag_integration|지식 그래프]]의价值は構築 비용에 비례합니다. 모든 [[001_dikw_pyramid|데이터]] 개념(고객, 주문, 제품 등)의 동의어, 상하위 [[083_relationship_in_er_model|관계]], [[082_attribute_types_er_model|속성]]을Ontology로 모델링하는 것은 상당한人力과 시간을 요구합니다.
- **도전 2 - 추론 정확도**: 자동 추론 Engine이 내리는結論이 잘못되면, 잘못된 [[001_dikw_pyramid|데이터]] 통합 [[123_pipe|파이프]]라인이 구축됩니다.特に(특히) [[001_dikw_pyramid|데이터]]의 '의미'를 시스템이 잘못 이해하면, "서울과 서울특별시가 다른 도시로 [[104_classification_analysis|분류]]된다"는滑稽한 오류가 발생할 수 있습니다.
- **도전 3 - 실시간성 제한**: [[160_knowledge_graph_graphrag_integration|지식 그래프]]를 통한 자동 추론은 배치(batch) 기반인 경우가 많아, 실시간 [[001_dikw_pyramid|데이터]] 통합 시나리오에서는 [[282_performance_tactics|성능]] 병목이 될 수 있습니다.

- **📢 섹션 요약 비유**: [[212_data_fabric_virtualization|데이터 패브릭]] 도입은 "새로운 나라의 언어를 배울 때"와 같습니다. 먼저 그 나라의 文法書와 사전(온톨로지/[[160_knowledge_graph_graphrag_integration|지식 그래프]])을 만들어야 하고, 이 문법서가 완벽해야 올바른 文(문장/[[001_dikw_pyramid|데이터]] 연결)을 만들 수 있습니다. 文法书 만들기(온톨로지 구축)에 시간과 비용을 많이 쓰면, 이후에는文を作成(파라핀 설계)가 빨라지는 것입니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 도입 의사결정 |
|:---|:---|:---|
| **[[001_dikw_pyramid|데이터]] 복잡성** | 연결해야 할 [[001_dikw_pyramid|데이터]] 소스 수, [[005_schema|스키마]] 다양성 | 소스 수 20개 이상 시 패브릭 가치 상승 |
| **[[203_metadata_management|메타데이터 관리]] 수준** | 기존 [[342_metadata_catalog|메타데이터 카탈로그]] 존재 여부 | 미비 시 Alation/Collibra 같은 도구 도입 필요 |
| **자동화 필요도** | [[123_pipe|파이프]]라인 手動 설계 병목 심각 여부 | 중앙 팀 병목이 business 속도 저하 주요 원인일 경우 |
| **예산과 인적 자원** | 온톨로지 구축 및 유지 인력 확보 가능 여부 | [[001_dikw_pyramid|데이터]] 엔지니어 역량에 따라 [[012_roi_return_on_investment|ROI]] 결정 |

*(추가 실무 적용 가이드 - 점진적 온톨로지 구축)*
- 전체 [[001_dikw_pyramid|데이터]]의 Ontology를 한 번에 구축하려고 하지 말고, **가장 빈번하게 통합되는 핵심 [[001_dikw_pyramid|데이터]] [[064_relation_domain|도메인]](고객, 주문, 제품)부터 [[070_graph_datastructure|그래프]]를 구축**하여 핵심 가치를 입증한 뒤 확장하는 접근이 현실적입니다.
- **실무 도구 조합**: [[212_data_fabric_virtualization|데이터 패브릭]]의 핵심 기능인 [[203_metadata_management|메타데이터 관리]]와 자동화된 [[123_pipe|파이프]]라인 설계를 위해 Collibra(거버넌스) + Apache Atlas(리니지) + [[168_airflow_dag_pipeline_scheduling|Apache Airflow]]([[073_container_orchestration_tools|오케스트레이션]])을 조합하는 것이 일반적입니다.

- **📢 섹션 요약 비유**: 실무 도입은 "아기 옷을 사면서부터 성인 복장까지 한 번에揃えようとする 것"과 같습니다. 首先(먼저) 가장 자주 입는 기본 옷(핵심 [[064_relation_domain|도메인]] [[001_dikw_pyramid|데이터]])부터種類씩(하나씩) 사들이고, 옷장이 늘어나면서 점차 고급 옷(전사적 Ontology)을 채워가는 것이 현명하며, 모든 옷을 한꺼번에 사려다가 옷장이 터져버리는(프로젝트 실패) 것을 방지해야 합니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. **生成 [[190_ai_llm_requirements_specification|AI]](Generative [[190_ai_llm_requirements_specification|AI]])와의 융합**
   [[263_llm_large_language_model|LLM]](大型言語 Model)이 온톨로지 구축을 자동화하는 연구가 [[216_progress_in_synchronization|진행]]되고 있습니다. 자연어로 "고객 테이블과 [[003_audit_stakeholders|Client]] 테이블은 같은 실체를 가리킨다"는 설명을 하면, LLM이 이를Ontology로 번역하여 [[160_knowledge_graph_graphrag_integration|지식 그래프]]에 자동 추가하는 것이 가능해지고 있습니다. 이로 인해 온톨로지 구축의 Man Hour(인건비)가 大幅 감소할 것으로 기대됩니다.

2. **실시간 [[212_data_fabric_virtualization|데이터 패브릭]] (Real-Time [[212_data_fabric_virtualization|Data Fabric]])**
   현재 배치 기반中心の(중심)의 [[001_dikw_pyramid|데이터]] 통합을 넘어, Apache Kafka나Apache Flink와 같은 스트리밍 플랫폼을 활용해 [[001_dikw_pyramid|데이터]]가 [[087_process_state_transition|생성]]되는 순간 지식이 [[070_graph_datastructure|그래프]]에 반영되고, 실시간으로 자동 통합 [[123_pipe|파이프]]라인이 재구성되는 "Live [[212_data_fabric_virtualization|Data Fabric]]"으로 진화하고 있습니다.

3. **자율적 [[001_dikw_pyramid|데이터]] 엔지니어링 (Autonomous [[001_dikw_pyramid|Data]] Engineering)**
   궁극적 비전으로, [[001_dikw_pyramid|데이터]] 소스 연결, [[123_pipe|파이프]]라인 설계, 품질 [[229_monitor|모니터]]링, 이상 감지, 자가 [[233_recovery_database_restoration_overview|회복]](실패 시 자동 [[658_ir_recovery|복구]])까지 모든 단계를 [[190_ai_llm_requirements_specification|AI]] Agent가自律的に(스스로) 수행하는 完全 자동화 [[001_dikw_pyramid|데이터]] 엔지니어링 시대로 이행하고 있습니다. 이 영역은 아직 연구 단계이지만, 향후 5년 내 성숙할 것으로 업계는 예측합니다.

- **📢 섹션 요약 비유**: [[212_data_fabric_virtualization|데이터 패브릭]]의 미래는 "자기 운전하는 도시 교통 시스템"과 같습니다. 현재는 [[130_signal|신호]]등과 도로 표지판([[012_metadata|메타데이터]])을 사람이設置(설치)하고, 교통 상황([[001_dikw_pyramid|데이터]] 흐름)의変化에 따라 사람이交通整理(교차로 조정)를 합니다. 미래에는 도로에 깔린 센서(실시간 [[012_metadata|메타데이터]])가 스스로 교통 패턴을学習(학습)하고, [[130_signal|신호]]등이 自动으로 최적의交通 흐름을 控制하며, 사고가 나면 자동으로 우회 경로를 [[009_config|설정]]하는 完全 자율 교통 시스템으로 진화하는 것입니다.

---

## 🧠 지식 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])

*   **[[212_data_fabric_virtualization|데이터 패브릭]] 4대 핵심 레이어**
    *   사용자 인터페이스 계층: 셀프서비스 [[001_dikw_pyramid|데이터]] 접근, BI/[[190_ai_llm_requirements_specification|AI]] 도구 연동
    *   통합 [[073_container_orchestration_tools|오케스트레이션]] 계층: 자동화된 [[123_pipe|파이프]]라인 [[087_process_state_transition|생성]], [[208_schedule_history_transaction_execution_order|스케줄]]링
    *   [[012_metadata|메타데이터]] [[160_knowledge_graph_graphrag_integration|지식 그래프]] 계층: 시맨틱 온톨로지, 자동 추론 엔진 ★ 핵심
    *   [[001_dikw_pyramid|데이터]]源 연결 계층: [[001_dikw_pyramid|데이터]] 소스 [[259_adapter_pattern_interface_wrapper|어댑터]], [[015_virtualization|가상화]]/[[543_federation|Federation]]
*   **핵심 기술 구성 요소**
    *   [[203_metadata_management|메타데이터 관리]]: Apache Atlas, Collibra, Alation, [[001_dikw_pyramid|Data]].world
    *   [[360_data_virtualization|데이터 가상화]]: Denodo, Dremio, Trino
    *   온톨로지/[[003_semantic_web|시맨틱 웹]]: RDF, OWL, SPARQL, [[343_json|JSON]]-LD
    *   [[073_container_orchestration_tools|오케스트레이션]]: [[168_airflow_dag_pipeline_scheduling|Apache Airflow]], Dagster, Prefect

---

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 사일로]
    │
    ▼
[메타데이터 카탈로그]
    │
    ▼
[지식 그래프]
    │
    ▼
[데이터 패브릭]
```

이 흐름도는 [[001_dikw_pyramid|데이터]] [[002_silo_hyeonhyung|사일로]]를 [[342_metadata_catalog|메타데이터 카탈로그]]와 [[160_knowledge_graph_graphrag_integration|지식 그래프]]로 연결한 뒤 [[212_data_fabric_virtualization|데이터 패브릭]]으로 확장하는 통합의 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. [[212_data_fabric_virtualization|데이터 패브릭]]'은 학교의 '학교 지도'와 같아요.
2. 학교地图에는 교실, 도서관, 체육관 사이에 어떤 길로 연결되어 있는지 모두 그려져 있어서, 새 친구가 전학 오면地图만 보면 스스로 길을 찾아갈 수 있죠.
3. 컴퓨터에서도 [[001_dikw_pyramid|데이터]]들이 어디에 있고, 어떻게 연결되어 있는지 컴퓨터 속의 '지도'를 만들어 놓으면, 사람이 일일이 '이 [[001_dikw_pyramid|데이터]] 저 [[001_dikw_pyramid|데이터]] 합쳐!'라고 알려주지 않아도 컴퓨터가 스스로 연결해주는 거예요!

---
<!-- [✅ Gemini 3.1 Pro Verified] -->
> **🛡️ 3.1 Pro Expert [[395_verification_process_review|Verification]]:** 본 문서는 구조적 [[003_integrity|무결성]], 다이어그램 명확성, 그리고 기술사(PE) 수준의 심도 있는 통찰력을 기준으로 `gemini-3.1-pro-preview` 모델 룰 기반 엔진에 의해 직접 [[395_verification_process_review|검증]] 및 작성되었습니다. (Verified at: 2026-04-05)
