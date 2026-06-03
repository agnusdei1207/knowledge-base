+++
title = "156. 데이터 패브릭 (Data Fabric) — 위치 무관 지능형 데이터 연결"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
1. [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)([Data Fabric](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/))은 Gartner가 정의한 아키텍처 개념으로, [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)·클라우드·엣지 등 이기종 환경에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 <strong>위치 무관하게 통합 접근</strong>할 수 있는 지능형 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 연결 레이어다.
2. <strong>능동적 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a>(<a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/">Active</a> <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">Metadata</a>)</strong>와 <strong><a href="/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/">지식 그래프</a>(<a href="/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/">Knowledge Graph</a>)</strong>를 통해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 간 의미론적 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 AI가 자동으로 발견하고, 접근 경로를 동적으로 최적화한다.
3. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)([Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/))가 <strong>조직 원칙 중심(<a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 소유권)</strong>이라면, [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 <strong>기술 원칙 중심(지능형 통합 레이어)</strong>으로 상호 보완적 개념이다.

---

## Ⅰ. 개요 및 필요성

현대 기업의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) DB, AWS S3, Azure [Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/), [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 애플리케이션(Salesforce, SAP) 등 수십 개의 이기종 시스템에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)되어 있다. 이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 통합 분석하려면 복잡한 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 별도로 구축해야 하며, [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)도 각 시스템마다 중복 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)해야 한다.

[데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 이 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 환경을 단일 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 레이어로 연결하는 아키텍처다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 물리적으로 이동하지 않고도 통합 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)·거버넌스·리니지를 적용할 수 있다.

| 전통 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통합 | [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) |
|:---|:---|
| 물리적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사 ([ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)) | [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 레이어 |
| 시스템별 별도 거버넌스 | 통합 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진 |
| 정적 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 동적 최적화 |
| 수동 [메타데이터 관리](/knowledge-base/studynote/16_bigdata/10_governance/203_metadata_management/) | 능동적 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 자동 발견 |
| 단일 클라우드/[온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) | [멀티 클라우드](/knowledge-base/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/) + [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) |

> 📢 **섹션 요약 비유**: [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 도시 전체를 연결하는 지하 전기 케이블망과 같다. 각 건물([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스)의 전기([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 새 배관 없이 통합 배전반(패브릭)에서 어디서든 사용할 수 있게 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Data Fabric 아키텍처</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">온프레미스</div><div class="kb-diagram-cell">AWS S3</div><div class="kb-diagram-cell">Azure DL</div><div class="kb-diagram-cell">SaaS DB</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Oracle</div><div class="kb-diagram-cell">Parquet</div><div class="kb-diagram-cell">Gen2</div><div class="kb-diagram-cell">Salesforce</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Data Fabric 레이어</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">능동적 메타데이터</div><div class="kb-diagram-cell">지식 그래프</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Active Metadata</div><div class="kb-diagram-cell">(Knowledge Graph)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">AI 자동 수집)</div><div class="kb-diagram-cell">의미 관계 맵핑</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">통합 거버넌스</div><div class="kb-diagram-cell">데이터 가상화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(정책 엔진)</div><div class="kb-diagram-cell">(물리 이동 없음)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">소비자 (BI / ML / 앱)</div></div>
</div>
</div>



**핵심 기술 구성 요소**

| 구성 요소 | 역할 | 기술 예시 |
|:---|:---|:---|
| 능동적 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) | AI로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)·품질 자동 발견 | Alation, Collibra, Atlan |
| [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/) | 개념 간 의미 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 표현 | Neo4j, Amazon Neptune |
| [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/) | 물리 이동 없이 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 통합 | Denodo, Dremio |
| 통합 거버넌스 | 멀티 소스 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 일원 관리 | Apache Atlas, Purview |
| [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 추천 | 관련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋 자동 제안 | ML 기반 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) 검색 |

> 📢 **섹션 요약 비유**: 능동적 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 사서와 같다. 책([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 도서관에 들어오면 AI가 자동으로 주제를 파악하고, 유사한 책들과의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 카드 목록에 기록하며, 독자에게 관련 책을 추천한다.

---

## Ⅲ. 비교 및 연결

<strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/">Data Fabric</a> vs <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/">Data Mesh</a> 비교</strong>

| 항목 | [Data Fabric](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) | [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) |
|:---|:---|:---|
| 접근 방식 | 기술 중심 (지능형 레이어) | 조직 원칙 중심 ([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유권) |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 | 최소화 ([가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 선호) | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 독립 운영 |
| 거버넌스 방식 | 중앙화 + [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 자동화 | 연합 (중앙 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) + [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 자율) |
| 도입 복잡도 | 기술 플랫폼 구축 필요 | 조직 문화 변화 필요 |
| 상호 보완성 | [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) 조직에 Fabric 기술 적용 가능 | Fabric 위에 [Mesh](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/) 원칙 구현 가능 |

<strong><a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/">데이터 가상화</a> vs 물리적 통합</strong>

| 항목 | 물리적 통합 ([ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)) | [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/) |
|:---|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 | 복사 후 [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 저장 | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 시점에 소스 직접 접근 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 신선도 | 배치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 발생 | 항상 최신 |
| [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 최적화 가능 | 소스 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 의존 |
| 거버넌스 | 단일 저장소 관리 | 소스별 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 관리 |

> 📢 **섹션 요약 비유**: [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Fabric이 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 비서가 모든 방의 물건을 파악하고 찾아주는 스마트 하우스라면, [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Mesh는 각 가족([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/))이 자기 방을 책임지는 가정 관리 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/">Data Fabric</a> 도입 적합 시나리오</strong>

- <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/">멀티 클라우드</a>/하이브리드</strong>: AWS + Azure + [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)된 대기업
- **M&A 후 통합**: 서로 다른 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)을 가진 두 회사 시스템을 빠르게 통합
- **레거시 현대화**: [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 레거시 DB를 즉시 클라우드로 이전하지 않고도 분석 통합
- **규제 환경**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 거주지([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Residency) 규제로 물리적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동이 불가한 경우

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| [Data Fabric](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) 정의 | 이기종 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 위치 무관하게 연결하는 지능형 통합 레이어 |
| 능동적 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 역할 | AI가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)·품질·사용 패턴을 자동 발견·추천 |
| [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Mesh와 차이 | Fabric = 기술 중심 통합, [Mesh](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/) = 조직 중심 소유권 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) |
| [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/) 한계 | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 소스 시스템에 의존, 복잡한 조인 비용 증가 |

> 📢 **섹션 요약 비유**: [Data Fabric](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) 도입은 전국 각지 도서관을 디지털로 연결하는 국가 도서관 네트워크 구축과 같다. 어느 지역의 책도 인터넷으로 바로 읽을 수 있되, 책은 각 도서관에 그대로 있다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [접근성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/292_accessibility_kwcag_wcag/) 향상 | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 단일 인터페이스로 통합 접근 |
| [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 비용 절감 | [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)로 불필요한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사 제거 |
| 거버넌스 일원화 | 멀티 소스에 통합 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 적용 |
| [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 발견 | 숨겨진 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋 자동 탐색, 분석 준비 시간 단축 |

[데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 Gartner가 2022년부터 Top [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) Trend로 꾸준히 선정하고 있는 아키텍처 방향이다. 단기적으로는 [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/)와 통합 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/), 중장기적으로는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 능동적 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)와 [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)로 진화한다. 기술사 시험에서는 <strong>능동적 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a> 개념</strong>, <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/">Data Fabric</a> vs <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/">Data Mesh</a> 비교</strong>, <strong><a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/">데이터 가상화</a> 원리와 한계</strong>가 핵심 논점이다.

> 📢 **섹션 요약 비유**: [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 세계의 인터넷과 같다. 세계 각지의 서버([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스)가 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)(패브릭 레이어)로 연결되어, 어디서든 원하는 정보를 위치 걱정 없이 가져올 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| 능동적 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) | 핵심 기술 | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)·품질 자동 발견 |
| [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/) | 핵심 기술 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 개념 간 의미론적 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 표현 |
| [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/) | 구현 방식 | 물리 이동 없이 소스 직접 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) | 비교 개념 | 조직 원칙 중심 (vs 기술 중심 Fabric) |
| Alation / Collibra | 솔루션 | 능동적 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)·[카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) 플랫폼 |
| [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Residency | 관련 규제 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 거주지 규제로 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 필요 |

---


### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터 사일로 (Data Silo) — 부서별 분산 저장, 통합 활용 불가 문제</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">ETL / ELT — 중앙 집중 복사·변환, 실시간성·유연성 한계</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터 패브릭 (Data Fabric) — 메타데이터 지능으로 위치 무관 데이터 연결</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터 메시 (Data Mesh) — 도메인 오너십 분산, 데이터 제품화 전략</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">지식 그래프 + AI 자동화 — 패브릭 기반 자동 데이터 발견·품질·거버넌스</div></div>
</div>
</div>



이 흐름은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/) 문제를 ETL로 임시 해결하던 방식에서 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 지능 기반 패브릭으로 진화하고, [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 거버넌스([데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/))와 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 자동화로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통합의 미래를 만들어가는 과정을 보여준다.


### 👶 어린이를 위한 3줄 비유 설명
1. [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 마법의 도서관 카드예요. 전국 어느 도서관에 있는 책도 이 카드 하나로 바로 빌릴 수 있어요.
2. [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 사서(능동적 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/))가 어떤 책이 어디 있는지 자동으로 파악하고, 비슷한 책도 알려줘요.
3. 책을 우리 도서관으로 옮길 필요 없이 그 자리에서 바로 읽을 수 있어서([데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/)) 훨씬 빠르답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 156 / 262

← **이전**: [155. ELT vs ETL — 클라우드 시대 데이터 변환 패러다임 전환](/knowledge-base/studynote/16_bigdata/07_data_lake/155_elt_vs_etl/)
**다음**: [157. 클라우드 빅데이터 분석 서비스 — Amazon EMR/Azure HDInsight/GCP Dataproc](/knowledge-base/studynote/16_bigdata/07_data_lake/157_data_analysis_services/) →

---
