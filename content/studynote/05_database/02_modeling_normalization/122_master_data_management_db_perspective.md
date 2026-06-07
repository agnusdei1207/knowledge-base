---
title: "Master Data Management Db Perspective"
date: "2026-04-19"
tags:
  - "studynote-database"
weight: 122
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MDM은 고객·상품·조직·자산 등 <strong>핵심 마스터 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>의 단일 골든 레코드(Golden Record)를 <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a>·유지</strong>하여, 전사 시스템([ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)·[CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/)·[DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)) 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)과 품질을 보장하는 관리 체계다.
> 2. **가치**: 마스터 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 시스템마다 다르면(고객명이 [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)="홍길동", [CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/)="길동 홍") <strong>보고서 불일치·중복 마케팅·재고 오류</strong>가 발생하며, MDM이 <strong>단일 진실 원천(Single Source of Truth)</strong>을 제공한다.
> 3. **판단 포인트**: [Registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)([참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)형)·Consolidation(통합형)·Centralized(중앙 집중형)·Coexistence(공존형)의 4가지 구현 스타일을 구분하고, [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)와의 연계가 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    MDM 필요성                                         |
+-------------------------------------------------------+
|  [MDM 없음]                                           |
|   ERP: 고객ID=1001, 홍길동                           |
|   CRM: 고객ID=A99, 길동 홍                           |
|   DW: ???  -> 같은 사람? 다른 사람?                   |
|                                                       |
|  [MDM 적용]                                           |
|   MDM Hub: 고객 골든 레코드 = "홍길동, ID=M001"      |
|   ERP: M001 -> 홍길동 ✅                              |
|   CRM: M001 -> 홍길동 ✅                              |
|   -> 전사 일관된 고객 뷰                              |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: MDM은 전사 <strong>주민등록 시스템</strong>이다. 이름이 조금씩 다르게 적힌 주민을 하나의 정확한 레코드로 통합한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [MDM](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 구현 스타일

| 스타일 | 설명 | 적합 |
|:---|:---|:---|
| <strong><a href="/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/">Registry</a></strong> | 기존 시스템에 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 키만 매핑 | 낮은 침습성 |
| **Consolidation** | 읽기 전용 [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)에 통합 | 분석·보고 |
| **Centralized** | [MDM](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)가 유일한 원천 | <strong>최고 <a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a></strong> |
| **Coexistence** | [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) ↔ 시스템 양방향 동기 | 유연성 |

- **📢 섹션 요약 비유**: Registry는 전화번호부([참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)만), Centralized는 중앙은행(모든 거래의 원천)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [MDM](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 없음 | [MDM](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 적용 |
|:---|:---|:---|
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a></strong> | 시스템별 상이 | **골든 레코드 통합** |
| **보고서** | 불일치 | **신뢰 가능** |
| **중복** | 빈번 | **제거** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [MDM](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 구축 핵심 단계
1. <strong><a href="/studynote/02_operating_system/10_security/613_profiling_gprof/">프로파일링</a></strong>: 현행 [데이터 품질 진단](/studynote/11_design_supervision/01_audit_framework/041_contractor_late_penalty/).
2. **매칭/병합**: 중복 레코드 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)·통합.
3. **골든 레코드**: 단일 마스터 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/).
4. **거버넌스**: [데이터 스튜어드](/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) 지정·[정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 수립.

---

## Ⅴ. 기대효과 및 결론

MDM은 <strong><a href="/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/">데이터 거버넌스</a>의 기술적 구현체</strong>이며, [CDP](/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/)·[데이터 메시](/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)·[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질의 기반이 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **골든 레코드** | MDM의 핵심 산출물 |
| <strong><a href="/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/">데이터 거버넌스</a></strong> | MDM의 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)·조직 프레임워크 |
| <strong><a href="/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/">CDP</a></strong> | 고객 마스터의 마케팅 특화 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 품질</strong> | MDM이 보장하는 핵심 가치 |
| <strong><a href="/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/">데이터 스튜어드</a></strong> | [MDM](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 운영 책임자 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 데이터 정제 (엑셀, 2000s)]
    |
    v
[MDM 솔루션 (Informatica·IBM, 2005~)]
    |
    v
[클라우드 MDM (Reltio, 2015~)]
    |
    v
[데이터 메시 + MDM (2020~) — 분산 소유권]
    |
    v
[현재: AI MDM — 자동 매칭·병합·품질 보정]
```

### 👶 어린이를 위한 3줄 비유 설명
1. MDM은 학교 <strong>출석부 관리 시스템</strong>이에요. 같은 학생이 다른 이름으로 등록되면 안 돼요.
2. "홍길동"과 "길동 홍"이 같은 사람인지 확인해서 **하나로 합쳐요** (골든 레코드).
3. 덕분에 어떤 선생님(시스템)이 봐도 <strong>같은 학생 정보</strong>를 볼 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 122 / 600

<- **이전**: [121. 데이터 아키텍처 프레임워크 (Zachman Framework) - 엔터프라이즈 데이터 설계 체계](/studynote/05_database/02_modeling_normalization/121_data_architecture_framework_zachman/)
**다음**: [123. 참조 데이터 & 코드 테이블 (Reference Data & Code Tables) - 코드성 데이터 표준화](/studynote/05_database/02_modeling_normalization/123_reference_data_code_tables/) ->

---
