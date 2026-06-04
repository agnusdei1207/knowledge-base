+++
title = "223. 데이터 패브릭 (Data Fabric) 메타데이터 가상화 AI 통합"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)([Data Fabric](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/))은 이기종 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스를 이동 없이 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)([Data Virtualization](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/247_data_virtualization_federated_query/))로 연결하고, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML이 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 자동으로 탐색·[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하여 통합 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 레이어를 형성하는 아키텍처다.
> 2. **가치**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 물리적으로 복사하지 않아도 어디서든 일관된 뷰([View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/))를 제공하므로, 멀티클라우드·[온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 혼합 환경에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Silo](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/))를 제거한다.
> 3. **판단 포인트**: [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 기술 중심([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)·[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/))이고 [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 조직 중심([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유권)이므로, 두 접근법은 배타적이 아니라 상호 보완 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)다.

---

## Ⅰ. 개요 및 필요성

Gartner는 [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)을 <strong>"<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 관리 설계 개념으로, <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>·이기종 환경 전반에 걸쳐 유연하고 탄력적인 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 통합을 가능하게 하는 아키텍처"</strong> 로 정의한다. 핵심은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 한 곳에 모으지 않고, 있는 자리에서 연결하는 것이다.

### 등장 배경

| 문제 | 설명 |
|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/) ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Silo](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)) | 부서별·시스템별 고립된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소 |
| 멀티클라우드 복잡성 | AWS·Azure·GCP·[온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 혼재 |
| 거버넌스 파편화 | 소스별 상이한 보안·품질 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 비용 | 모든 소스를 복사하는 파이프라인 유지 비용 |

📢 **섹션 요약 비유**: [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 "도서관 책을 한 곳으로 모으지 않고, 전국 도서관 통합 검색 시스템을 구축하는 것"이다. 책은 제자리에 있지만 어디서든 검색하고 대출 예약할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) 아키텍처 전체 구조

```
        애플리케이션 / 분석 / AI·ML 소비자
              |          |          |
              v          v          v
+--------------------------------------------------+
|           Unified Data Access Layer              |
|        (통합 데이터 접근 레이어)                  |
|  +--------------------------------------------+  |
|  |   Data Virtualization Engine               |  |
|  |   (데이터 가상화 엔진, 물리 이동 없이 쿼리) |  |
|  +--------------------------------------------+  |
|  +--------------------------------------------+  |
|  |   Intelligent Metadata Layer               |  |
|  |   (AI 기반 메타데이터 자동 탐색·분류·추천)  |  |
|  +--------------------------------------------+  |
|  +--------------------------------------------+  |
|  |   Federated Governance & Security          |  |
|  |   (접근제어·마스킹·감사 로그 통합 관리)     |  |
|  +--------------------------------------------+  |
+--------------------------------------------------+
          |         |         |         |
          v         v         v         v
    +------+   +------+  +------+  +------+
    |Oracle|   | S3   |  |Kafka |  |SAP   |
    | DB   |   |Lake  |  |Stream|  |ERP   |
    +------+   +------+  +------+  +------+
     온프레미스    AWS       이벤트    SaaS
```

### 2-2. 핵심 구성 요소

| 구성 요소 | 역할 | 기술 예시 |
|:---|:---|:---|
| [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [Metadata](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) (능동 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)) | AI가 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 자동 수집·[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)·추천 | Atlan, Alation |
| [Data Virtualization](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/247_data_virtualization_federated_query/) ([데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/)) | 물리 이동 없이 이기종 소스 통합 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | Denodo, Dremio, Starburst |
| [Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/) ([지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 간 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)·리니지 [그래프 표현](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/033_graph_representation/) | Neo4j, AWS Neptune |
| Governance Automation | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 자동 적용, 마스킹, 접근제어 | Apache Ranger, [OPA](/knowledge-base/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) |
| [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Fabric | RESTful·[GraphQL](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/246_graphql_query_language_overfetching_solution/) 통합 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | Kong, MuleSoft |

### 2-3. [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 자동화 흐름

```
데이터 소스 연결
      |
      v
+-------------------------------------+
|  Metadata Crawler (자동 탐색 봇)    |
|  - 스키마 자동 감지                  |
|  - PII (개인식별정보) 자동 태그      |
|  - 데이터 분류 (민감도 레벨)         |
+-------------------------------------+
      |
      v
+-------------------------------------+
|  Active Metadata Engine             |
|  - 사용 패턴 학습 -> 연관 데이터 추천 |
|  - 품질 이상 자동 감지               |
|  - 리니지 자동 생성                  |
+-------------------------------------+
      |
      v
   데이터 소비자에게 "검색 -> 이해 -> 신뢰" 경험 제공
```

📢 **섹션 요약 비유**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 엔진은 "도서관 사서 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)"다. 새 책이 들어오면 자동으로 제목·저자·장르를 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하고, 이 책을 좋아하는 독자에게 추천까지 한다.

---

## Ⅲ. 비교 및 연결

### 3-1. [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) vs [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) 비교

| 구분 | [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) ([Data Fabric](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)) | [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) ([Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/)) |
|:---|:---|:---|
| 중심축 | 기술 ([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)·[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)) | 조직 ([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유권) |
| 접근 방식 | 중앙 기술 레이어로 통합 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 자율 운영 |
| 거버넌스 | 자동화된 중앙 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진 | 연합(Federated) 공동 협의 |
| [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 활용 | 핵심 ([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 자동화) | 보조적 (품질 모니터링) |
| 적합 조직 | 기존 시스템 복잡한 대기업 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀 역량 높은 조직 |
| 배타 여부 | 상호 보완 가능 | 상호 보완 가능 |

### 3-2. [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/)([Data Virtualization](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/247_data_virtualization_federated_query/)) 심화

[데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/)는 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 복사하지 않고, [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 시점에 소스에서 직접 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 가져와 통합 뷰를 제공한다.

- **Push-Down Optimization (푸시다운 최적화)**: 필터·집계 연산을 원본 소스에서 실행해 네트워크 전송량 최소화
- **Semantic Layer (시맨틱 레이어)**: 비즈니스 용어로 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 가능하게 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)
- <strong><a href="/knowledge-base/studynote/14_data_engineering/04_mlops/195_federated_query_data_fabric_distributed_join/">Federated Query</a> (연합 <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a>)</strong>: 여러 소스를 단일 SQL로 조회

📢 **섹션 요약 비유**: [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/)는 "여러 은행 잔액을 하나의 금융 앱에서 보는 것"이다. 돈을 한 은행으로 옮기지 않아도 전체 자산 현황을 즉시 볼 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. 멀티클라우드 [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) 구현 시나리오

**시나리오: 금융그룹 멀티클라우드 통합**

```
온프레미스 Oracle ERP -+
AWS S3 데이터 레이크   -+  Data Fabric Layer  -->  통합 BI·AI 분석
Azure Synapse DW      -+  (Denodo + Atlan)
GCP BigQuery          -+
```

| 단계 | 작업 | 기술 |
|:---|:---|:---|
| 연결 | 4개 소스 커넥터 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | JDBC, [REST](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/), ODBC |
| 탐색 | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 크롤러로 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 자동 수집 | Atlan Crawler |
| [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) | 통합 뷰 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 푸시다운 최적화 | Denodo VQL |
| 거버넌스 | PII 자동 탐지, 마스킹 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 적용 | Apache Ranger |
| 서빙 | 단일 [REST](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) API로 소비자 제공 | [GraphQL](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/246_graphql_query_language_overfetching_solution/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) |

### 4-2. Gartner [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) 구성 요소 (2023 정의 기준)

1. <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Integration &amp; Transformation</strong> — 통합 [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)/[ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) 파이프라인
2. <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/">Data Catalog</a> &amp; <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">Metadata</a></strong> — 능동 [메타데이터 카탈로그](/knowledge-base/studynote/05_database/06_dw_olap_trends/342_metadata_catalog/)
3. <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/247_data_virtualization_federated_query/">Data Virtualization</a></strong> — 물리 이동 없는 가상 통합
4. <strong><a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/">Data Governance</a> &amp; <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a></strong> — 자동화된 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 관리
5. <strong>Master <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/1013_management/">Management</a> (<a href="/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/">MDM</a>, <a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/051_mdm_master_data_management/">마스터 데이터 관리</a>)</strong> — 단일 진실 소스 유지
6. **Analytics & Insights** — 통합 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석 레이어

📢 **섹션 요약 비유**: [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) 도입은 "여러 나라 전화망을 하나의 국제전화 시스템으로 연결하는 것"이다. 각 나라 망은 그대로지만 어디서나 통화할 수 있게 된다.

---

## Ⅴ. 기대효과 및 결론

[데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) 구축·유지 비용을 최소화하면서도 통합 [접근성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/292_accessibility_kwcag_wcag/)과 거버넌스를 제공한다. 특히 레거시 시스템이 많고 클라우드 마이그레이션이 점진적으로 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중인 대기업에 가장 적합하다.

### 기대 효과 요약

| 영역 | 기대 효과 |
|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [접근성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/292_accessibility_kwcag_wcag/) | 이기종 소스 단일 인터페이스 접근 |
| [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 비용 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사 제거 -> 30~50% 파이프라인 감소 |
| 거버넌스 | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 자동 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) -> 컴플라이언스 대응 속도 80% 향상 |
| 시간 절감 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 탐색·이해 시간 70% 단축 |

기술사 시험에서 [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 <strong>"능동 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a>(<a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/">Active</a> <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">Metadata</a>)와 <a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/">데이터 가상화</a>(<a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/247_data_virtualization_federated_query/">Data Virtualization</a>)가 핵심 차별점"</strong> 임을 중심으로 설명해야 한다.

📢 **섹션 요약 비유**: [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)의 최종 목표는 "모든 직원이 회사 어딘 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)든 구글 검색하듯 찾아 쓸 수 있는 세상"을 만드는 것이다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 기술 | [Data Virtualization](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/247_data_virtualization_federated_query/) ([데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/)) | 물리 이동 없는 통합 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| 핵심 기술 | [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [Metadata](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) (능동 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)) | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 자동 탐색·[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| 핵심 기술 | [Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/) ([지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)·리니지 표현 |
| 비교 | [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) ([데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)) | 조직 중심 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 아키텍처 |
| 비교 | [Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) ([데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)) | 물리 집중 저장소 |
| 도구 | Denodo / Dremio | [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/) 플랫폼 |
| 도구 | Atlan / Alation | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [메타데이터 카탈로그](/knowledge-base/studynote/05_database/06_dw_olap_trends/342_metadata_catalog/) |
| 표준 | Gartner [Data Fabric](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) Definition | 산업 표준 정의 |
| 연관 | [Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) ([데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)) | [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 탐색·관리 |
| 연관 | [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) (Master [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/1013_management/)) | [마스터 데이터](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 관리 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. 여러 도서관의 책을 한 곳으로 모으지 않고, 통합 검색 앱 하나만 만들어서 어느 도서관 책이든 검색하고 빌릴 수 있게 하는 것이 [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)이다.

### 📈 관련 키워드 및 발전 흐름도

```text
데이터 사일로 (시스템 간 단절)
    |
    v
Data Fabric: 메타데이터 기반 통합 · 가상화
    +-► 메타데이터 자동 수집 · AI 기반 추천
    +-► 데이터 가상화: 물리 이동 없이 접근
    +-► 통합 거버넌스 · 보안 정책
    |
    v
Data Mesh와 상호 보완 관계
```
2. 앱이 새 책을 자동으로 인식하고 장르·내용을 AI가 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)해 주는 것이 능동 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 기능이다.
3. 각 도서관의 규칙(거버넌스)은 그대로지만, 앱이 어느 책이 어린이용인지 성인용인지 자동으로 알아서 접근을 통제해준다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 223 / 258

<- **이전**: [222. 데이터 메시 (Data Mesh) 분산 오너십 데이터 프로덕트](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/222_data_mesh_distributed_ownership_data_product/)
**다음**: [224. 데이터 리니지 (Data Lineage) 흐름 족보 카탈로그 태그 거버넌스](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/224_data_lineage_flow_catalog_tagging/) ->

---
