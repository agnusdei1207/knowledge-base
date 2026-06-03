+++
title = "222. 데이터 메시 (Data Mesh) 분산 오너십 데이터 프로덕트"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)([Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/))는 중앙집중식 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 팀의 병목을 제거하기 위해 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 프로덕트([Data Product](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/))의 소유권과 품질을 직접 책임지는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)형 [데이터 아키텍처](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 패러다임이다.
> 2. **가치**: 조직 규모가 커질수록 중앙 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 거버넌스·속도 한계가 선형 이상으로 커지는데, [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 이를 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)으로 극복하여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 민첩성([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Agility)을 유지한다.
> 3. **판단 포인트**: [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀의 [데이터 리터러시](/knowledge-base/studynote/12_it_management/01_governance_strategy/058_data_literacy/)([Data Literacy](/knowledge-base/studynote/12_it_management/01_governance_strategy/058_data_literacy/))와 자율 운영 능력이 성숙하지 않으면 오히려 혼란만 증가하므로, 조직 성숙도 평가가 도입 전 필수 조건이다.

---

## Ⅰ. 개요 및 필요성

### 중앙집중식 [데이터 아키텍처](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)의 한계

2010년대 빅데이터 물결은 중앙 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)([Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)) 또는 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)([Data Warehouse](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/208_data_warehouse_schema_on_write_inmon/))로 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 집결시키는 패턴을 낳았다. 하지만 조직 규모가 커지면서 다음 문제가 심화되었다.

- **처리 병목**: 중앙 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어링 팀이 모든 파이프라인 요청을 처리해야 하는 구조
- **품질 책임 모호**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 생산자([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀)와 소비자(분석 팀) 사이 품질 책임 공백
- **지식 단절**: 중앙 팀은 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 비즈니스 맥락을 모르고, [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀은 [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) 기술을 모름
- **확장 한계**: [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 수 증가 시 중앙 팀 부하 O(n) 이상 증가

Zhamak Dehghani가 2019년 제안한 [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 이 문제를 <strong>"마이크로서비스가 애플리케이션 개발을 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>시킨 것처럼 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>도 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>시키자"</strong> 는 사상으로 해결한다.

📢 **섹션 요약 비유**: 중앙 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 팀은 "모든 부서의 서류 복사를 혼자 담당하는 복사실"과 같다. 처음엔 효율적이지만 회사가 커지면 항상 대기줄이 생긴다. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 각 부서에 복사기를 두는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) 4원칙



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Data Mesh 4 Principles</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">① Domain</div><div class="kb-diagram-cell">② Data as a Product</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Ownership</div><div class="kb-diagram-cell">(데이터를 제품으로 취급)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(도메인 소유권)</div><div class="kb-diagram-cell">- 검색 가능 (Discoverable)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 주소 지정 가능 (Addressable)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">도메인 팀이</div><div class="kb-diagram-cell">- 이해 가능 (Understandable)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 생산·</div><div class="kb-diagram-cell">- 신뢰 가능 (Trustworthy)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">관리·제공 책임</div><div class="kb-diagram-cell">- 자체 완비 (Self-contained)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">③ Self-Serve Data</div><div class="kb-diagram-cell">④ Federated Computational</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Infrastructure Platform</div><div class="kb-diagram-cell">Governance</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(셀프 서빙 플랫폼)</div><div class="kb-diagram-cell">(연합 거버넌스)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">도메인 팀이 인프라</div><div class="kb-diagram-cell">중앙·도메인 공동 거버넌스</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">없이도 데이터 제품을</div><div class="kb-diagram-cell">정책, 표준, 계약 협의</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">자율 생산할 수 있도록</div><div class="kb-diagram-cell">자율성 + 글로벌 일관성</div></div>
</div>
</div>



### 2-2. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 프로덕트([Data Product](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/)) 구조

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 프로덕트는 단순한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋이 아니라 <strong>"비즈니스 가치를 제공하는 소비 가능한 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 단위"</strong> 다.

| [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) | 설명 | 예시 |
|:---|:---|:---|
| Discoverable (탐색 가능) | [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)에 등록 | Apache Atlas, DataHub |
| Addressable (주소 지정 가능) | 고유 URI 또는 ARN으로 접근 | s3://[domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)/product/v1/ |
| Understandable (이해 가능) | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)·문서·[데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/) | OpenAPI 스펙, README |
| Trustworthy (신뢰 가능) | [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)·품질 [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) 명시 | 99.9% [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/), [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) < 1h |
| Interoperable (상호운용 가능) | 표준 포맷·[API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/), [REST](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/), [gRPC](/knowledge-base/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) |
| Self-contained (자체 완비) | 파이프라인·[스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 포함 | dbt + Airflow [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 포함 |

📢 **섹션 요약 비유**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 프로덕트는 "완성된 도시락 제품"이다. 재료(원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 아니라, 먹을 수 있게 포장되고 유통기한([SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/))이 붙고 성분표(문서)가 있는 완제품이다.

---

## Ⅲ. 비교 및 연결

### 3-1. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) vs [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) vs [데이터 레이크하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/)

| 구분 | [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) | [데이터 레이크하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/) | [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) |
|:---|:---|:---|:---|
| 소유권 | 중앙 집중 | 중앙 집중 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) |
| 거버넌스 | 중앙 일괄 | 중앙 일괄 | 연합(Federated) |
| 확장성 | 팀 병목 | 팀 병목 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 독립 확장 |
| 품질 책임 | 불명확 | 불명확 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀 책임 |
| 도입 난이도 | 낮음 | 중간 | 높음 (조직 변화 필요) |

### 3-2. [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유권의 실제 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Federated Governance Layer</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(글로벌 정책: 보안, 개인정보,</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 계약 표준)</div></div>
<div class="kb-diagram-note">정책 제공</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">주문 도메인</div><div class="kb-diagram-cell">고객 도메인</div><div class="kb-diagram-cell">물류 도메인</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Order Domain</div><div class="kb-diagram-cell">Customer Domain</div><div class="kb-diagram-cell">Logistics Domain</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">주문 이력</div><div class="kb-diagram-cell">고객 프로파일</div><div class="kb-diagram-cell">배송 현황</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">주문 분석</div><div class="kb-diagram-cell">CLV 분석</div><div class="kb-diagram-cell">창고 재고</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Data Product A)</div><div class="kb-diagram-cell">(Data Product B)</div><div class="kb-diagram-cell">(Data Product C)</div></div>
<div class="kb-diagram-note">소비</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Self-Serve Platform</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(공통 인프라: 카탈로그,</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스토리지, 컴퓨팅 API)</div></div>
</div>
</div>



📢 **섹션 요약 비유**: [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 "프랜차이즈 식당" 모델이다. 각 가맹점([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀)은 자체 운영 권한이 있지만, 본사(연합 거버넌스)의 레시피 표준과 식품 안전 규정을 따른다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) 성숙도 모델

| 단계 | 특징 | 조건 |
|:---|:---|:---|
| **Level 1** 탐색 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 정의, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 인벤토리 파악 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오너 지정 |
| **Level 2** 기반 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 파이프라인 분리, [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) 구축 | 셀프 서빙 플랫폼 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) |
| **Level 3** 제품화 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)·계약([Data Contract](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/)) 적용 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀 리터러시 확보 |
| **Level 4** 최적화 | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 품질 모니터링, 연합 거버넌스 자동화 | 전사 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 문화 정착 |

### 4-2. 도입 실패 패턴 및 대응

- **실패 패턴 1**: [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀 역량 미비 → 대응: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)(Embedded) 운영
- **실패 패턴 2**: 셀프 서빙 플랫폼 부재 → 대응: [IDP](/knowledge-base/studynote/09_security/11_iam_access_control/536_idp_identity_provider/)([Internal Developer Platform](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/200_internal_developer_platform_backstage/), [내부 개발자 플랫폼](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/110_idp_internal_developer_platform_backstage/)) 먼저 구축
- **실패 패턴 3**: 표준 없는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) → 대응: [데이터 계약](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/)([Data Contract](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/)) 표준 선행 정의

📢 **섹션 요약 비유**: [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) 도입은 "직원들에게 재택근무를 허용하는 것"과 같다. 성숙한 조직에는 생산성 폭발이지만, 준비 없이 시행하면 소통 부재와 혼란만 커진다.

---

## Ⅴ. 기대효과 및 결론

[데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)의 궁극적 목표는 <strong>"<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>의 민주화(Democratization)"</strong> 다. 모든 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 생산자이자 소비자가 되어, 조직 전체의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용 속도와 품질을 동시에 높인다.

### [핵심 성과 지표](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/)

| [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) | 기대 개선 |
|:---|:---|
| [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) 리드타임 | 중앙 팀 대기 제거 → 60~80% 감소 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 오류율 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 책임 명확화 → 30~50% 감소 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재사용률 | 검색 가능한 [Data Product](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/) → 2~3× 향상 |
| 거버넌스 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 대응 속도 | 리니지 자동화 → 80% 단축 |

기술사 시험에서 [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 <strong>"조직 중심(Organization-Centric) <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/">데이터 아키텍처</a>"</strong> 로, 기술 문제가 아닌 조직·문화적 전환임을 강조해야 한다.

📢 **섹션 요약 비유**: [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 "중앙 우체국 없이 각 동네에 우편함을 두는 것"이다. 배달은 빨라지지만, 각 동네가 자기 우편함을 관리하는 책임을 져야 한다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 4원칙 | [Domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) Ownership ([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유권) | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 책임 |
| 4원칙 | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a Product ([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 제품화) | 소비 가능한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 단위 |
| 4원칙 | Self-Serve Platform (셀프 서빙 플랫폼) | 공통 인프라 플랫폼 |
| 4원칙 | Federated Governance (연합 거버넌스) | 중앙+[도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 협력 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| 산출물 | [Data Contract](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/) ([데이터 계약](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/)) | 생산자-소비자 간 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 약속 |
| 비교 | [Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) ([데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)) | 중앙집중식 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소 |
| 비교 | [Data Fabric](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) ([데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)) | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 통합 아키텍처 |
| 도구 | DataHub / Apache Atlas | [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/), 리니지 도구 |
| 개념 | [Data Literacy](/knowledge-base/studynote/12_it_management/01_governance_strategy/058_data_literacy/) ([데이터 리터러시](/knowledge-base/studynote/12_it_management/01_governance_strategy/058_data_literacy/)) | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용 역량 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. 학교에서 모든 숙제를 교무실 한 곳에서만 검사받는 것처럼 중앙 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 팀이 모든 일을 처리하다 보면 줄이 너무 길어진다.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">중앙 집중 데이터 팀 (병목 · 확장 한계)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Data Mesh: 도메인별 데이터 소유권 분산</div>
<div class="kb-diagram-tree-item" style="--depth:2">도메인 데이터 프로덕트: 자율 운영</div>
<div class="kb-diagram-tree-item" style="--depth:2">Self-Serve 인프라 플랫폼</div>
<div class="kb-diagram-tree-item" style="--depth:2">연방 거버넌스: 전사 표준 + 도메인 자율</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Data Product Thinking → API · SLA 기반 데이터 계약</div>
</div>
</div>


2. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 각 반 선생님([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀)이 직접 자기 반 숙제를 검사하고 관리하도록 바꾸는 것이다.
3. 교장 선생님(연합 거버넌스)은 전체 채점 기준만 정해주고, 각 반은 그 기준 안에서 자유롭게 운영한다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 222 / 258

← **이전**: [221. LSM 트리 (Log-Structured Merge-Tree) 멤테이블 순차 플러시 콤팩션](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/221_lsm_tree_memtable_sequential_flush_compaction/)
**다음**: [223. 데이터 패브릭 (Data Fabric) 메타데이터 가상화 AI 통합](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/223_data_fabric_metadata_virtualization_integration/) →

---
