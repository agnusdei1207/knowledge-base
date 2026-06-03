+++
weight = 144
title = "데이터 늪 (Data Swamp)"
date = "2024-05-22"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
1. [[208_data_lake_schema_on_read|데이터 레이크]]([[208_data_lake_schema_on_read|Data Lake]])의 거버넌스와 관리가 부재하여, **[[001_dikw_pyramid|데이터]]의 출처와 의미를 알 수 없게 된 쓸모없는 저장소**를 말한다.
2. [[012_metadata|메타데이터]]([[012_metadata|Metadata]])와 [[213_data_catalog_metadata|데이터 카탈로그]]의 부실로 인해 분석가가 원하는 [[001_dikw_pyramid|데이터]]를 찾을 수 없어 분석 효율이 극도로 저하된 상태이다.
3. 중복 [[001_dikw_pyramid|데이터]]와 저품질 [[001_dikw_pyramid|데이터]]의 범람으로 스토리지 비용만 낭비되는 '빅데이터 프로젝트의 실패 전조'이다.

---

### Ⅰ. 개요 ([[033_context|Context]] & Background)
[[208_data_lake_schema_on_read|데이터 레이크]]는 "일단 다 저장하자"는 철학으로 시작하지만, "어떻게 찾을 것인가"에 대한 대책이 없으면 순식간에 늪으로 변한다. 이는 [[208_data_lake_schema_on_read|데이터 레이크]]의 유연성이 관리의 부재와 결합할 때 발생하는 부작용으로, 기업이 쌓은 [[001_dikw_pyramid|데이터]]가 자산이 아닌 부채가 되는 현상을 의미한다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
[[288_data_swamp_metadata_management_absence|데이터 늪]]은 [[208_data_lake_schema_on_read|데이터 레이크]] 아키텍처에서 관리 계층([[372_management|Management]] Layer)이 붕괴되었을 때 발생한다.

```text
[ Data Lake vs Data Swamp / 데이터 레이크와 늪의 차이 ]

       Data Lake (Healthy)                 Data Swamp (Failed)
    +-----------------------+           +-----------------------+
    | [Metadata Catalog]    |           | [Metadata Missing]    |
    | [Access Control]      |           | [Dirty Data Overflow] |
    | [Clear Data Lineage]  |           | [Unknown Files (v1..)]|
    +-----------+-----------+           +-----------+-----------+
                |                                   |
                v                                   v
    Analysis Possible (Clear)           Analysis Impossible (Dark)
```

1. **원인 (Causes)**:
   - **거버넌스 부재**: [[001_dikw_pyramid|데이터]]의 [[087_process_state_transition|생성]], 변경, 폐기 주기가 관리되지 않음.
   - **[[012_metadata|메타데이터]] 실종**: [[501_file_definition_logical_record|파일]]명만으로는 내용을 알 수 없는 수백만 개의 [[501_file_definition_logical_record|파일]] 적체.
   - **품질 관리 미비**: 중복, 누락, 오염된 [[001_dikw_pyramid|데이터]]의 무분별한 유입.
2. **증상 (Symptoms)**: [[001_dikw_pyramid|데이터]] 분석 준비 시간([[001_dikw_pyramid|Data]] Wrangling)이 분석 시간의 90% 이상을 차지하게 됨.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | [[208_data_lake_schema_on_read|데이터 레이크]] ([[208_data_lake_schema_on_read|Data Lake]]) | [[288_data_swamp_metadata_management_absence|데이터 늪]] ([[288_data_swamp_metadata_management_absence|Data Swamp]]) |
| :--- | :--- | :--- |
| **[[001_dikw_pyramid|데이터]] 활용성** | 높음 (검색 및 가공 용이) | 매우 낮음 (탐색 불가) |
| **거버넌스 수준** | 엄격함 ([[394_catalog_metadata|카탈로그]], 권한) | 낮거나 없음 (무단 적재) |
| **비즈니스 가치** | 자산 (Insight 창출) | 비용 (부채, 스토리지 낭비) |
| **핵심 해결책** | [[255_data_observability|데이터 옵저버빌리티]] 구축 | [[001_dikw_pyramid|데이터]] 클렌징 및 거버넌스 재정립 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
1. **[[213_data_catalog_metadata|데이터 카탈로그]]([[213_data_catalog_metadata|Data Catalog]]) 자동화**: 수집 단계에서 [[012_metadata|메타데이터]]를 자동으로 추출하고 태깅하는 시스템(AWS Glue, Amundsen 등) 도입이 필수적이다.
2. **[[214_data_lineage_tracking|데이터 리니지]]([[214_data_lineage_tracking|Data Lineage]]) [[003_bigdata_7v|시각화]]**: [[001_dikw_pyramid|데이터]]가 어디서 왔고 어떻게 변했는지 족보를 관리하여 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 확보해야 한다.
3. **PE 관점의 판단**: [[288_data_swamp_metadata_management_absence|데이터 늪]]을 방지하려면 '[[001_dikw_pyramid|데이터]]를 버리는 규칙([[515_mvcc|Retention]] [[164_policy|Policy]])'도 정의해야 한다. 쓸모없는 [[001_dikw_pyramid|데이터]]를 영구 저장하는 것은 인프라 비용과 보안 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]](Privacy)만 가중시킨다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[[288_data_swamp_metadata_management_absence|데이터 늪]]을 탈출하는 과정이 곧 진정한 [[001_dikw_pyramid|데이터]] 기업으로 거듭나는 과정이다. 향후에는 AI가 스스로 [[001_dikw_pyramid|데이터]]를 [[104_classification_analysis|분류]]하고 품질을 평가하는 '자기 치유 [[001_dikw_pyramid|데이터]] 플랫폼(Self-healing [[001_dikw_pyramid|Data]] Platform)'이 표준이 될 것이며, [[001_dikw_pyramid|데이터]] 엔지니어는 늪을 막는 '환경 관리자'로서의 거버넌스 역량을 더욱 강화해야 한다.

---

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **상위 개념**: [[052_data_governance_framework|Data Governance]], [[208_data_lake_schema_on_read|Data Lake]]
- **하위 개념**: [[213_data_catalog_metadata|Data Catalog]], [[012_metadata|Metadata]], [[214_data_lineage_tracking|Data Lineage]]
- **연관 개념**: [[001_dikw_pyramid|Data]] Wrangling, [[270_data_quality_great_expectations|Data Quality]], [[062_darkdata|Dark Data]]

---

### 📈 관련 키워드 및 발전 흐름도

```text
[상위 개념: Data Governance, Data Lake]
    │
    ▼
[하위 개념: Data Catalog, Metadata, Data Lineage]
    │
    ▼
[연관 개념: Data Wrangling, Data Quality, Dark Data]
```

이 흐름도는 상위 개념: [[052_data_governance_framework|Data Governance]], [[001_dikw_pyramid|Data]] Lake에서 출발해 연관 개념: [[001_dikw_pyramid|Data]] Wrangling, [[270_data_quality_great_expectations|Data Quality]], Dark Data까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. **[[288_data_swamp_metadata_management_absence|데이터 늪]]**: 장난감 상자에 장난감을 정리 안 하고 막 집어넣어서, 나중에는 밑바닥에 뭐가 있는지 알 수 없게 된 상태예요.
2. **문제점**: 좋아하는 로봇을 찾고 싶은데, 부서진 인형과 쓰레기가 섞여 있어서 찾기가 너무 힘들어요.
3. **해결법**: 상자 겉면에 무엇이 들어있는지 이름표를 붙이고, 망가진 건 버리는 습관이 필요해요.
