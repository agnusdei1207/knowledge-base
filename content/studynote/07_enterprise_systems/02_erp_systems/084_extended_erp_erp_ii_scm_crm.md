---
title: "ERP II"
date: "2026-06-07"
tags:
  - "enterprise_systems"
  - "studynote-enterprise-systems"
weight: 84
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) II (Extended [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/))는 [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) ([Enterprise Resource Planning](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/))를 회사 밖의 [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)과 고객 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)까지 확장한 통합 운영 모델이다.
> 2. **가치**: [SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/) ([Supply Chain](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/))과 [CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) ([C고객](/studynote/12_it_management/01_governance_strategy/820_three_c_analysis/) [Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/))을 연결해 내부 실행과 외부 협업을 같은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름으로 묶는다.
> 3. **판단 포인트**: 패키지 설치보다 중요한 것은 [마스터 데이터](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/), 프로세스 표준화, 인터페이스 거버넌스다.

---

## Ⅰ. 개요 및 필요성

[ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) ([Enterprise Resource Planning](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/))는 회계, 생산, 구매, 재고, 인사 같은 내부 자원을 하나의 기준으로 관리하려는 시스템이다. [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) II (Extended [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/))는 여기서 한 걸음 더 나아가 공급업체와 고객, 파트너까지 연동해 기업 경계를 넘어선 협업을 가능하게 한다. 즉 ERP가 내부 운영의 통합이라면, [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) II는 외부 가치사슬까지 포함한 통합이다.

이 확장이 필요한 이유는 주문, 납기, 재고, 고객 요구가 이제 한 회사 내부에서만 결정되지 않기 때문이다. SCM과 CRM이 분리돼 있으면 수요 예측과 생산 계획이 어긋나고, 고객 응대와 실제 재고가 불일치한다.

```text
Supplier --► SCM --► ERP Core --► CRM --► Customer
                 ^         |         |
                 +-------- MDM / Workflow / API --------+
```

- **📢 섹션 요약 비유**: 가게 안의 장부만 맞는다고 끝이 아니라, 납품처와 손님 기록까지 같아야 진짜 운영이 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) II의 핵심은 내부 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)을 넘어 파트너와 고객의 정보를 실시간에 가깝게 연결하는 것이다. 이를 위해 [MDM](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) (Master [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/))로 기준 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 맞추고, [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) ([Application Programming Interface](/studynote/02_operating_system/01_overview_architecture/014_api_posix/))와 워크플로우로 외부 시스템과 연결한다. 내부 프로세스가 바뀌면 외부 협업 흐름도 같이 바뀐다.

| 구성 | 역할 | 효과 |
| :--- | :--- | :--- |
| [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) Core | 회계 / 생산 / 구매의 중심 | 업무 기준 통일 |
| [SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/) ([Supply Chain](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/)) | [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 계획과 실행 | 납기와 재고 안정 |
| [CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) ([C고객](/studynote/12_it_management/01_governance_strategy/820_three_c_analysis/) [Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/)) | 고객 접점과 판매 관리 | 수요와 응대 개선 |
| [MDM](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) | 기준 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통합 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치 감소 |
| [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) / Portal | 외부 연계 창구 | 협업 범위 확대 |

```text
내부 프로세스 -> ERP Core -> 외부 프로세스
          |            |            |
          +-- 표준 데이터와 워크플로우로 연결 --+
```

이 구조에서 가장 중요한 것은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 흐르는 방향보다 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 기준이 하나인지다. [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)과 고객 정보가 여러 시스템에 따로 존재하면 [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) II는 이름만 화려한 연결망이 되고, 기준 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 맞아야 비로소 통합이 된다.

- **📢 섹션 요약 비유**: 같은 주소록을 회사, 택배사, 고객센터가 같이 써야 우편이 엇갈리지 않는다.

---

## Ⅲ. 비교 및 연결

전통 ERP는 내부 부서 통합에 강하지만, [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) II는 외부 파트너와 고객까지 포함한다는 점이 다르다. 반면 점 솔루션은 특정 부서에는 빠르지만 전체 흐름을 보기 어렵다. 결국 [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) II는 시스템 수를 늘리는 것이 아니라, 경계를 넓혀 같은 업무 언어를 공유하게 만드는 것이다.

| 비교 축 | 전통 [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) | [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) II | 점 솔루션 |
| :--- | :--- | :--- | :--- |
| 범위 | 내부 부서 | [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) / 고객까지 | 특정 기능 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 내부 중심 | 내부 + 외부 기준 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) |
| 협업 | 부서 간 | 기업 간 | 제한적 |
| 장점 | 통제 용이 | 엔드투엔드 가시성 | 빠른 도입 |
| 한계 | 외부 연계 약함 | 통합 복잡도 높음 | [사일로](/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/) 심화 |

[ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) II는 SCM과 CRM을 따로 붙인다고 끝나지 않는다. 주문 예측, 생산 계획, 납기 관리, 고객 응대가 같은 기준 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 같은 이벤트 흐름 위에 있어야 한다.

- **📢 섹션 요약 비유**: 방 안만 정리하는 것과 집 전체 동선을 함께 정리하는 것은 난이도가 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 도입에서는 먼저 [마스터 데이터](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)와 업무 프로세스를 표준화해야 한다. 그다음 단계적으로 [SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/), 외부 파트너 포털을 연결한다. [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) II는 패키지를 사는 문제가 아니라, [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)와 조직 변경을 함께 설계하는 문제다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [마스터 데이터](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)의 기준과 책임자가 정해졌는가?
2. [SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/) / [CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) / [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) 간 인터페이스 계약이 문서화됐는가?
3. 외부 파트너와의 예외 처리와 재전송 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 있는가?
4. 도입 후 [변경 관리](/studynote/12_it_management/02_itsm_itil/079_change_enablement/)와 교육 계획이 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 기존 엑셀과 개별 시스템을 그대로 두고 중복 입력만 늘리는 경우
- 커스터마이징을 먼저 하고 프로세스 표준화를 나중에 하는 경우
- 외부 연동 실패 시 책임 경계가 불명확한 경우

- **📢 섹션 요약 비유**: 여러 사람이 같은 노트를 쓰려면 먼저 필기 규칙과 담당자를 정해야 한다.

---

## Ⅴ. 기대효과 및 결론

[ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) II의 기대효과는 부서 단위 최적화를 넘어서 기업 전체와 파트너까지 이어지는 가시성을 얻는 데 있다. 수요 예측 정확도, 재고 회전, 고객 응대 속도, 협력사 납기 관리가 함께 좋아질 수 있다. 단, 통합 범위가 넓어질수록 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질과 [변경 관리](/studynote/12_it_management/02_itsm_itil/079_change_enablement/)의 중요도도 같이 높아진다.

결론적으로 [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) II는 '더 큰 [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)'가 아니라 '경계를 넓힌 운영 플랫폼'으로 이해해야 한다. 내부와 외부를 같은 흐름으로 묶을 수 있을 때 비로소 가치가 나온다.

- **📢 섹션 요약 비유**: 가게 장부, 배송 장부, 손님 장부가 모두 맞아야 진짜 매출이 보인다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) ([Enterprise Resource Planning](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)) | 내부 자원 통합의 기준 |
| [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) II | 외부 가치사슬까지 확장한 통합 |
| [SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/) ([Supply Chain](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/)) | [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 계획과 실행 |
| [CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) ([C고객](/studynote/12_it_management/01_governance_strategy/820_three_c_analysis/) [Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/)) | 고객 접점과 판매 관리 |
| [MDM](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) (Master [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/)) | 기준 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 유지 |
| [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) / Portal | 기업 간 연계 창구 |

### 📈 관련 키워드 및 발전 흐름도

```text
고객 주문
  |
  v
CRM
  |
  v
ERP Core
  |
  v
SCM -> 공급사 협업 -> 납품 / 피드백
```

흐름의 핵심은 내부 처리와 외부 협업이 같은 기준 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 이어지는 것이다.

### 👶 어린이를 위한 3줄 비유 설명

1. 가게 안 기록만 맞추면 아직 반쪽짜리예요.
2. 물건을 보내는 곳과 사는 사람 기록도 함께 맞아야 해요.
3. [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) II는 가게 밖 사람들까지 한 장의 노트로 이어 주는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 84 / 482

<- **이전**: [83. MRP II (Manufacturing Resource Planning) - 자재뿐 아니라 설비, 인력 등 생산 자원 전체 포괄](/studynote/07_enterprise_systems/02_erp_systems/083_mrp_2_manufacturing_resource_planning/)
**다음**: [85. ERP 구축 생명주기 - 패키지 선정 -> 커스터마이징 / CBO (Custom Built Object) -> 데이터 이관 ->](/studynote/07_enterprise_systems/02_erp_systems/085_erp_implementation_lifecycle/) ->

---
