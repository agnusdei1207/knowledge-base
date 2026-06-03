+++
title = "데이터 늪 (Data Swamp)"
date = 2024-05-22

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
1. [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)([Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))의 거버넌스와 관리가 부재하여, <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>의 출처와 의미를 알 수 없게 된 쓸모없는 저장소</strong>를 말한다.
2. [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)([Metadata](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/))와 [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)의 부실로 인해 분석가가 원하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 찾을 수 없어 분석 효율이 극도로 저하된 상태이다.
3. 중복 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 저품질 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 범람으로 스토리지 비용만 낭비되는 '빅데이터 프로젝트의 실패 전조'이다.

---

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
[데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 "일단 다 저장하자"는 철학으로 시작하지만, "어떻게 찾을 것인가"에 대한 대책이 없으면 순식간에 늪으로 변한다. 이는 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 유연성이 관리의 부재와 결합할 때 발생하는 부작용으로, 기업이 쌓은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 자산이 아닌 부채가 되는 현상을 의미한다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
[데이터 늪](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/)은 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 아키텍처에서 관리 계층([Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) Layer)이 붕괴되었을 때 발생한다.

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
   - **거버넌스 부재**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 변경, 폐기 주기가 관리되지 않음.
   - <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a> 실종</strong>: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)명만으로는 내용을 알 수 없는 수백만 개의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 적체.
   - **품질 관리 미비**: 중복, 누락, 오염된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 무분별한 유입.
2. **증상 (Symptoms)**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석 준비 시간([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Wrangling)이 분석 시간의 90% 이상을 차지하게 됨.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) ([Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)) | [데이터 늪](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/) ([Data Swamp](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/)) |
| :--- | :--- | :--- |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 활용성</strong> | 높음 (검색 및 가공 용이) | 매우 낮음 (탐색 불가) |
| **거버넌스 수준** | 엄격함 ([카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/), 권한) | 낮거나 없음 (무단 적재) |
| **비즈니스 가치** | 자산 (Insight 창출) | 비용 (부채, 스토리지 낭비) |
| **핵심 해결책** | [데이터 옵저버빌리티](/knowledge-base/studynote/16_bigdata/13_intro_trends/255_data_observability/) 구축 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클렌징 및 거버넌스 재정립 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
1. <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/">데이터 카탈로그</a>(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/">Data Catalog</a>) 자동화</strong>: 수집 단계에서 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 자동으로 추출하고 태깅하는 시스템(AWS Glue, Amundsen 등) 도입이 필수적이다.
2. <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/">데이터 리니지</a>(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/">Data Lineage</a>) <a href="/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/">시각화</a></strong>: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어디서 왔고 어떻게 변했는지 족보를 관리하여 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 확보해야 한다.
3. **PE 관점의 판단**: [데이터 늪](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/)을 방지하려면 '[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 버리는 규칙([Retention](/knowledge-base/studynote/05_database/04_transactions_concurrency/515_mvcc/) [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))'도 정의해야 한다. 쓸모없는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 영구 저장하는 것은 인프라 비용과 보안 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)(Privacy)만 가중시킨다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[데이터 늪](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/)을 탈출하는 과정이 곧 진정한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기업으로 거듭나는 과정이다. 향후에는 AI가 스스로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하고 품질을 평가하는 '자기 치유 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼(Self-healing [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Platform)'이 표준이 될 것이며, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어는 늪을 막는 '환경 관리자'로서의 거버넌스 역량을 더욱 강화해야 한다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념**: [Data Governance](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/), [Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)
- **하위 개념**: [Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/), [Metadata](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/), [Data Lineage](/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/)
- **연관 개념**: [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Wrangling, [Data Quality](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/270_data_quality_great_expectations/), [Dark Data](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/)

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

이 흐름도는 상위 개념: [Data Governance](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/), [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Lake에서 출발해 연관 개념: [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Wrangling, [Data Quality](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/270_data_quality_great_expectations/), Dark Data까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. <strong><a href="/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/">데이터 늪</a></strong>: 장난감 상자에 장난감을 정리 안 하고 막 집어넣어서, 나중에는 밑바닥에 뭐가 있는지 알 수 없게 된 상태예요.
2. **문제점**: 좋아하는 로봇을 찾고 싶은데, 부서진 인형과 쓰레기가 섞여 있어서 찾기가 너무 힘들어요.
3. **해결법**: 상자 겉면에 무엇이 들어있는지 이름표를 붙이고, 망가진 건 버리는 습관이 필요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 144 / 262

← **이전**: [데이터 레이크 (Data Lake)](/knowledge-base/studynote/16_bigdata/07_data_lake/143_data_lake/)
**다음**: [데이터 웨어하우스 (Data Warehouse)](/knowledge-base/studynote/16_bigdata/07_data_lake/145_data_warehouse/) →

---
