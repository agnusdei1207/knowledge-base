+++
title = "197. 데이터 메시 (Data Mesh)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-enterprise"]

[extra]
tags = ["studynote-enterprise"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) ([Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/))는 분석용 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 중앙 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)팀의 공용 자산이 아니라, 각 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)이 책임지는 [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/) ([Data Product](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/))으로 다루는 운영 모델이다.
> 2. **가치**: [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 지식을 가진 팀이 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/), 품질, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 목표 ([SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/), [Service Level Objective](/knowledge-base/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/))를 직접 관리하므로, 중앙 적체를 줄이면서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 의미 왜곡과 전달 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 함께 낮춘다.
> 3. **판단 포인트**: [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)의 성패는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 그 자체가 아니라, 셀프서비스 플랫폼과 연합 거버넌스 (Federated Governance)로 자율성과 표준을 동시에 설계했는가에 달려 있다.

---

## Ⅰ. 개요 및 필요성

[데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) ([Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/))는 분석용 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 중심 조직이 직접 소유·운영·제공하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)형 [데이터 아키텍처](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)다. 전통적인 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) ([Data Warehouse](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/))나 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) ([Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)) 모델은 분석용 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 중앙 팀이 모아 정제하는 방식이었지만, 규모가 커질수록 모든 요청이 중앙 큐에 몰리며 병목이 심해진다. 특히 영업, 결제, 물류처럼 의미가 다른 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 중앙 엔지니어가 모두 이해하기는 어렵기 때문에, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 쌓여도 [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)와 전달 속도는 오히려 떨어진다.

[데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)가 등장한 배경은 조직 구조와 시스템 구조가 이미 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)되었다는 현실에 있다. [마이크로서비스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), [Microservice Architecture](/knowledge-base/studynote/07_enterprise_systems/06_exam_summary/365_msa_microservice_architecture/))로 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 책임은 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)별로 나누었는데, 분석 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 여전히 중앙팀이 책임지면 변경 속도가 맞지 않는다. 결과적으로 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 하루에도 여러 번 바뀌는데 분석 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인은 주 단위로 따라오면서, 현업은 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 많은데 쓸 수는 없는" 상태를 경험하게 된다.

따라서 [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)의 핵심 문제의식은 저장 기술이 아니라 책임 소재다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 의미를 가장 잘 아는 팀이 품질과 계약을 책임져야, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 단순 적재물이 아니라 재사용 가능한 제품이 된다.

- **📢 섹션 요약 비유**: [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 모든 식재료를 본사 주방으로 보내는 대신, 각 전문 주방이 자기 요리를 직접 책임지고 손님에게 내놓게 만드는 식당 체계와 같다. 재료를 가장 잘 아는 요리사가 조리해야 맛과 속도가 함께 살아난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)의 구조는 네 가지 원리로 요약된다. 첫째, [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 주도 소유권 ([Domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)-oriented Ownership)으로 각 팀이 자기 [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)과 품질을 책임진다. 둘째, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 제품처럼 다루어 문서, [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/), 접근 방식, 품질 지표를 함께 제공한다. 셋째, 셀프서비스 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼 (Self-serve [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Platform)이 저장소, [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인, [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/), 권한 관리를 공통 기능으로 제공한다. 넷째, 연합 거버넌스가 보안·표준·상호운용 규칙을 최소 공통 규범으로 유지한다.

| 원리 | 의미 | 빠지면 생기는 문제 |
| :-- | :-- | :-- |
| [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유권 | [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 주체가 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)·품질·배포를 책임 | 중앙 적체, 의미 왜곡 |
| [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/)화 | 문서, 계약, [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/), 접근 경로를 포함해 제공 | 덤프 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)만 쌓이고 재사용 불가 |
| 셀프서비스 플랫폼 | 인프라, [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/), 관측, 권한 기능을 공통화 | 각 팀이 도구를 제각각 재구축 |
| 연합 거버넌스 | 표준 명명, 보안, [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/), [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 공통 적용 | 포맷 불일치, 품질 혼란 |

아래 그림은 [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)가 "[도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 자율성"과 "공통 플랫폼"을 동시에 요구한다는 점을 보여준다.

```text
+----------------------------------------------------------------------------+
|                   Domain-owned data products on shared platform            |
+----------------------------------------------------------------------------+
| Sales Domain      Payment Domain      Logistics Domain                     |
|      |                 |                    |                              |
|      v                 v                    v                              |
| [Data Product]    [Data Product]       [Data Product]                     |
|      +---------------+--------------------+---------------+               |
|                      v                    v                               |
|   Catalog · Access Control · Observability · Storage · Pipeline Runtime   |
|                              |                                             |
|                              v                                             |
|                Cross-domain analytics / reports / apps                 |
+----------------------------------------------------------------------------+
```

이 구조에서 플랫폼 팀은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 대신 만들지 않는다. 대신 표준 템플릿, [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 수집, [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) ([Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)), 접근 제어, 품질 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 같은 기반 기능을 제공해 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀이 빠르게 제품을 만들게 돕는다. 즉 [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 "모두가 각자 알아서 하라"가 아니라, "공통 기반 위에서 책임만 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)하라"는 모델이다.

- **📢 섹션 요약 비유**: [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 각 가게가 자기 상품을 책임지되, 쇼핑몰 건물·결제 시스템·안내판은 중앙이 제공하는 백화점과 같다. 매장은 독립적이어도 손님 경험은 하나로 맞춰야 한다.

---

## Ⅲ. 비교 및 연결

[데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 [데이터 레이크하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/) ([Lakehouse](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/))나 [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) ([Data Fabric](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/))과 자주 혼동되지만 초점이 다르다. [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)는 저장 구조를 통합하는 기술 접근이고, [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 소유권과 운영 방식을 바꾸는 조직 접근이다. [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자산을 자동 탐색·연결·[정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)화하는 자동화 계층으로, [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)를 보완할 수는 있지만 대체하지는 않는다.

| 구분 | 중앙 레이크/[레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) | [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) | [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) |
| :-- | :-- | :-- | :-- |
| 중심 질문 | 어디에 저장할 것인가 | 누가 책임질 것인가 | 어떻게 자동 연결할 것인가 |
| 소유 구조 | 중앙 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)팀 중심 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀 중심 | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 자산 전반 |
| 강점 | 통합 저장, 관리 단순성 | 확장성, 현업 의미 보존 | [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 자동화, 연결성 |
| 약점 | 중앙 병목, 의미 손실 | 조직 역량 요구, 거버넌스 비용 | 소유권 문제를 직접 해결하지 못함 |

아키텍처 관점에서는 [도메인 주도 설계](/knowledge-base/studynote/12_it_management/05_security_compliance/310_architecture/) ([DDD](/knowledge-base/studynote/12_it_management/05_security_compliance/310_architecture/), [Domain-Driven Design](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/127_ddd_domain_driven_design/))와도 강하게 연결된다. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계를 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 맞춰 나누었다면, 분석 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경계도 같은 기준으로 맞추는 편이 변화 대응에 유리하다. 반대로 전사 기준코드, 회계 [마스터 데이터](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)처럼 강한 중앙 통제가 필요한 영역은 완전 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)보다 중앙 [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/)으로 남기는 편이 더 합리적일 수 있다.

- **📢 섹션 요약 비유**: [데이터 레이크하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/)가 거대한 창고를 잘 짓는 기술이라면, [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 어떤 팀이 어떤 물건을 책임지고 진열할지 정하는 운영 원칙이다. 좋은 창고만으로는 좋은 상점 운영이 자동으로 되지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스가 많고 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 간 변경 속도가 크게 다른 대기업에서 특히 효과가 크다. 중앙 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)팀 요청 대기 시간이 길고, 팀별 의미 차이 때문에 품질 이슈가 반복된다면 채택 우선순위가 높다. 반대로 조직이 작고 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어링 역량이 충분히 성숙하지 않았다면, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)보다 중앙 플랫폼 고도화가 먼저일 수 있다.

### 채택이 유리한 경우

1. [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 수가 많아 중앙 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 팀이 병목이 된 경우
2. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정의와 품질 책임을 현업 가까운 팀에 두는 편이 정확한 경우
3. [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/), 권한, 관측성, 표준 배포를 제공할 플랫폼 팀이 존재하는 경우

### 회피하거나 단계 도입이 필요한 경우

- 작은 조직에서 동일 인력이 운영과 분석을 모두 맡아 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 이점이 거의 없는 경우
- 공통 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 표준과 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 체계가 없어 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 즉시 혼란이 커지는 경우
- [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀이 [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/) 운영을 맡을 시간과 인력 없이 선언만 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)하는 경우

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/)마다 소유 팀, [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 계약, 갱신 주기, 품질 지표가 명확한가?
- 공통 플랫폼이 접근 제어, [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/), [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 템플릿을 제공하는가?
- 연합 거버넌스가 명명 규칙, [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/), 상호운용 포맷을 강제하는가?
- 소비자 팀이 [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/)을 셀프서비스로 발견하고 사용할 수 있는가?

흔한 실패는 "중앙팀은 손 떼고 각자 알아서 하라"는 선언형 도입이다. 이것은 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)가 아니라 [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)의 재생산이다. 기술사 답안에서는 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 자율성과 중앙 표준의 균형, 그리고 플랫폼 팀의 역할을 함께 제시해야 설득력이 높다.

- **📢 섹션 요약 비유**: [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) 도입은 프랜차이즈를 열어 주면서 레시피, 위생 규칙, 판매 시점 정보 시스템 (POS, Point of Sale)은 본사가 통일하는 것과 같다. 간판만 나눠 주고 운영 규칙을 주지 않으면 매장 수만 늘어난다.

---

## Ⅴ. 기대효과 및 결론

[데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)를 잘 설계하면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 제공 리드타임이 줄고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 책임이 명확해지며, [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 분석 재사용성이 높아진다. 중앙팀은 개별 요청 처리보다 플랫폼과 표준 고도화에 집중할 수 있어, 전체 조직의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 생산성이 단계적으로 좋아진다. 또한 [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/) 단위로 품질과 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 협약 ([SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/), [Service Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/))를 측정하면, "누가 왜 잘못했는가"가 아니라 "어떤 계약이 깨졌는가"로 문제를 다루기 쉬워진다.

다만 [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)가 모든 조직의 정답은 아니다. [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 엔지니어링 역량, [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 문화, 공통 플랫폼 투자 없이는 운영 비용만 늘 수 있다. 따라서 이 개념은 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장하자"가 아니라, <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 책임을 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 책임처럼 제품화하자</strong>는 관점으로 기억하는 것이 핵심이다.

- **📢 섹션 요약 비유**: [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)의 목표는 창고를 여러 개 만드는 것이 아니라, 각 창고가 자기 물건을 책임 있게 관리하면서도 전체 물류망은 한 몸처럼 움직이게 만드는 데 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [도메인 주도 설계](/knowledge-base/studynote/12_it_management/05_security_compliance/310_architecture/) ([DDD](/knowledge-base/studynote/12_it_management/05_security_compliance/310_architecture/), [Domain-Driven Design](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/127_ddd_domain_driven_design/)) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경계를 비즈니스 경계와 맞추는 출발점 |
| [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/) ([Data Product](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/)) | [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)에서 제공 단위를 정의하는 핵심 개념 |
| [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) ([Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)된 [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/)의 발견 가능성을 높이는 도구 |
| 연합 거버넌스 (Federated Governance) | 자율성과 표준을 함께 유지하는 운영 원리 |
| [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) ([Data Fabric](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 연결·자동화를 보완하는 기술 층 |

### 📈 관련 키워드 및 발전 흐름도

```text
중앙 데이터 웨어하우스
    |
    v
데이터 레이크 · 레이크하우스
    |
    v
중앙 병목과 의미 왜곡 인식
    |
    v
도메인 소유 데이터 제품
    |
    v
셀프서비스 플랫폼 + 연합 거버넌스
    |
    v
데이터 메시 운영 모델
```

이 흐름은 저장소 통합 중심 사고에서, [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 책임과 제품 운영 중심 사고로 무게가 이동한 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 예전에는 모든 장난감을 한 큰 상자에 넣고 한 명이 다 정리했어요.
2. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 자동차 장난감은 자동차 팀이, 블록은 블록 팀이 자기 상자를 직접 정리하게 하는 거예요.
3. 대신 상자 이름표와 정리 규칙은 모두 같게 해서 누구나 쉽게 찾을 수 있게 만들어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 197 / 482

<- **이전**: [196. 서버리스 아키텍처 - BaaS와 FaaS 기반 엔터프라이즈 통합](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/196_serverless_architecture_baas_integration/)
**다음**: [198. 비즈니스 룰 엔진 (BRE, Business Rule 엔진)](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/198_business_rule_engine_brm_logic_decoupling/) ->

---
