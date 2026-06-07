---
title: "81. ERP (Enterprise Resource Planning)"
date: "2026-05-08"
tags:
  - "studynote-enterprise-systems"
weight: 81
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ERP (Enterprise Resource Planning)는 재무·생산·구매·영업·인사 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 하나의 기준 정보와 프로세스로 묶는 전사 통합 운영 플랫폼이다.
> 2. **가치**: 부서별 [사일로](/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)를 줄여 단일 진실 원천 ([Single Source of Truth](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/))을 만들고, 주문부터 회계 반영까지의 흐름을 실시간에 가깝게 연결한다.
> 3. **판단 포인트**: ERP의 성패는 패키지 구매보다 <strong>표준 프로세스 수용, <a href="/studynote/05_database/07_exam_summary/539_mdm_master_data_management/">마스터 데이터</a> 정합성, 권한 통제</strong>를 얼마나 설계했는가에 달려 있다.

---

## Ⅰ. 개요 및 필요성

ERP는 기업의 핵심 업무를 공통 [데이터 모델](/studynote/05_database/01_db_architecture_relational/014_data_model_components/)과 표준 프로세스로 통합하는 전사적 자원 관리 시스템이다. 부서별로 회계 시스템, 생산 시스템, 엑셀 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 따로 움직이면 같은 재고를 두고도 숫자가 다르고, 영업 수주가 재무 결산과 생산 계획에 늦게 반영된다. ERP는 이런 정보 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 중복 입력을 줄여 "한 번 입력하면 전사에 반영되는 구조"를 만들기 위해 등장했다.

[MRP II](/studynote/07_enterprise_systems/02_erp_systems/083_mrp_2_manufacturing_resource_planning/) ([Manufacturing Resource Planning](/studynote/07_enterprise_systems/02_erp_systems/083_mrp_2_manufacturing_resource_planning/))가 제조 자원 중심이었다면, ERP는 범위를 재무·인사·구매·영업까지 넓혀 기업 전체의 운영 체계를 다룬다. 그래서 ERP는 단순 소프트웨어가 아니라 프로세스 표준화와 내부 통제의 기반으로 이해해야 한다.

- **📢 섹션 요약 비유**: ERP는 각 부서가 따로 쓰던 공책을 하나의 공식 장부로 바꾸는 일과 같다. 같은 사건을 모두가 같은 장부에 적어야 숫자 싸움이 줄어든다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ERP의 핵심은 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이 따로 보여도 <strong><a href="/studynote/05_database/07_exam_summary/539_mdm_master_data_management/">마스터 데이터</a>와 거래 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>는 연결</strong>된다는 점이다. 고객, 품목, 원가, 계정, 조직 정보가 공통으로 관리되고, 한 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)의 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 다른 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)의 후속 업무를 자동으로 유발한다.

| [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/) | 주요 역할 | 연결 포인트 |
| :--- | :--- | :--- |
| FI (Financial Accounting) | 회계 전표, 채권·채무, 결산 | 구매·영업 결과를 회계로 반영 |
| MM (Materials [Management](/studynote/12_it_management/05_security_compliance/1013_management/)) | 구매, 입고, 재고 관리 | 생산·영업과 재고를 공유 |
| [PP](/studynote/12_it_management/01_governance_strategy/015_payback_period/) (Production Planning) | 생산 계획, 작업 지시 | [MRP](/studynote/07_enterprise_systems/02_erp_systems/082_mrp_material_requirements_planning/), [BOM](/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/), 재고와 연동 |
| SD (Sales and Distribution) | 수주, 출하, 청구 | 재고·매출채권과 연결 |
| HCM (Human Capital [Management](/studynote/12_it_management/05_security_compliance/1013_management/)) | 인사, 급여, 조직 | 원가·권한 체계와 연결 |

아래 흐름은 ERP가 "주문 입력" 하나를 여러 부서의 동시 작업으로 바꾸는 방식을 보여준다.

```text
+--------------------------------------------------------------+
| ERP integrated flow                                          |
+--------------------------------------------------------------+
| Sales Order                                                  |
|      |                                                       |
|      +-> SD : order / delivery plan                          |
|      +-> MM : ATP check / inventory update                   |
|      +-> PP : production requirement if stock is short       |
|      +-> FI : receivable / revenue posting                   |
|                                                              |
| Shared master data: item, customer, supplier, account, org   |
+--------------------------------------------------------------+
```

즉 ERP는 화면을 합치는 것이 아니라, <strong>거래의 파급 효과를 같은 <a href="/studynote/05_database/01_db_architecture_relational/014_data_model_components/">데이터 모델</a> 안에서 연쇄적으로 처리</strong>하는 구조다. 이 때문에 인터페이스보다 [마스터 데이터](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 설계와 코드 체계가 더 중요하다.

- **📢 섹션 요약 비유**: ERP는 주문 벨이 울리면 주방, 창고, 계산대가 동시에 움직이는 식당 시스템과 같다. 벨은 하나지만 반응은 여러 곳에서 동시에 일어난다.

---

## Ⅲ. 비교 및 연결

ERP의 경계는 "기능별 개별 시스템"과 "외부까지 확장된 통합 체계" 사이에서 분명해진다.

| 구분 | 기능별 개별 시스템 | ERP | 확장형 ERP / [Postmodern ERP](/studynote/07_enterprise_systems/02_erp_systems/089_postmodern_erp_best_of_breed/) |
| :--- | :--- | :--- | :--- |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 부서별 분리 | 전사 공통 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 전사 + 외부 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/)/[API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 연계 |
| 프로세스 | 배치·수기 전달 중심 | 내부 프로세스 실시간 통합 | 외부 파트너·베스트오브브리드 결합 |
| 강점 | 도입 범위가 작음 | 내부 통제와 정합성 우수 | 민첩성, 확장성 우수 |
| 약점 | 불일치·중복 입력 | 구축 비용·변화관리 부담 | 통합 거버넌스가 복잡 |

ERP는 [MRP](/studynote/07_enterprise_systems/02_erp_systems/082_mrp_material_requirements_planning/)·[MRP](/studynote/07_enterprise_systems/02_erp_systems/082_mrp_material_requirements_planning/) II에서 출발해 [SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/) ([Supply Chain](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/)), [CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) ([C고객](/studynote/12_it_management/01_governance_strategy/820_three_c_analysis/) [Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/)), [MES](/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/) ([Manufacturing Execution System](/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/))와 연결되며 확장되었다. 따라서 ERP를 기억할 때는 "모든 기능을 한 제품에 넣는다"보다, <strong>기업 내부의 기준 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>와 프로세스를 중심에 둔다</strong>는 관점이 더 중요하다.

- **📢 섹션 요약 비유**: 개별 시스템은 각자 악보를 들고 연주하는 소규모 팀이고, ERP는 한 지휘자 아래 총보를 보는 오케스트라에 가깝다. 확장형 ERP는 여기에 외부 합창단까지 붙인 형태다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 ERP는 "통합"보다 "표준화와 통제"의 문제로 실패하거나 성공한다. 기존 업무를 모두 커스터마이징으로 옮기면 업그레이드가 막히고, [마스터 데이터](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)가 틀리면 통합된 만큼 오류도 전사로 확산된다. 따라서 ERP 도입 시에는 Fit-to-Standard 원칙, 단계적 오픈, 역할 기반 권한 관리가 핵심 판단 기준이 된다.

### 설계 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 품목·거래처·계정과목 등 [마스터 데이터](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 기준이 전사적으로 합의되었는가?
2. 표준 프로세스를 우선 적용하고, 예외만 확장 포인트로 처리하는가?
3. SoD (Segregation of Duties) 원칙에 따라 발주·검수·지급 권한이 분리되어 있는가?
4. 빅뱅 방식보다 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)·법인·공장 단위의 단계적 전환이 가능한가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 기존 관행을 그대로 살리기 위해 ERP를 과도하게 수정하는 것
- 실재고·[BOM](/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)·원가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 없이 화면 구축부터 시작하는 것
- 통합 시스템인데도 부서별 엑셀을 공식 기준으로 남겨 두는 것

- **📢 섹션 요약 비유**: ERP 구축은 낡은 골목길 위에 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)등만 세우는 일이 아니다. 도로 폭, 표지판, 통행 규칙을 함께 바꾸지 않으면 교통체증은 그대로 남는다.

---

## Ⅴ. 기대효과 및 결론

ERP가 제대로 정착되면 결산 속도, 재고 정확도, 납기 예측력, 내부 통제 수준이 함께 좋아진다. 특히 주문-구매-생산-회계의 연결이 빨라져 경영진은 늦은 보고가 아니라 [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)에 가까운 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 볼 수 있다. 또한 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적성과 표준 프로세스가 강화되어 기업 운영의 재현성과 책임성이 높아진다.

반면 ERP는 모든 문제를 자동 해결하지 않는다. 조직이 표준 프로세스를 받아들이지 못하거나, 예외 업무를 무분별하게 누적하면 오히려 더 무거운 레거시가 된다. 결국 ERP는 "패키지 도입"이 아니라 <strong>전사 운영 규칙을 하나의 체계로 묶는 일</strong>로 기억하는 것이 정확하다.

- **📢 섹션 요약 비유**: ERP는 회사의 혈관을 하나로 정리하는 순환계 수술과 같다. 피가 잘 돌면 몸 전체가 좋아지지만, 기준 혈관이 막히면 영향도 전신으로 번진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [MRP II](/studynote/07_enterprise_systems/02_erp_systems/083_mrp_2_manufacturing_resource_planning/) ([Manufacturing Resource Planning](/studynote/07_enterprise_systems/02_erp_systems/083_mrp_2_manufacturing_resource_planning/)) | ERP의 제조 중심 전신 |
| [SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/) ([Supply Chain](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/)) | ERP를 [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 외부로 확장 |
| [CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) ([C고객](/studynote/12_it_management/01_governance_strategy/820_three_c_analysis/) [Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/)) | 고객 접점 정보를 ERP와 연계 |
| [MES](/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/) ([Manufacturing Execution System](/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/)) | 현장 실행 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 ERP와 연결 |
| SoD (Segregation of Duties) | ERP 권한 통제의 핵심 원칙 |

### 📈 관련 키워드 및 발전 흐름도

```text
MRP
  |
  v
MRP II
  |
  v
ERP
  |
  +-> SCM / CRM / MES integration
  |
  v
Cloud ERP / Composable ERP / Intelligent ERP
```

### 👶 어린이를 위한 3줄 비유 설명

1. ERP는 회사 안의 모든 팀이 같은 큰 공책을 함께 쓰는 거예요.
2. 누가 물건을 팔면 창고, 공장, 계산하는 팀이 그 내용을 동시에 알 수 있어요.
3. 그래서 "재고가 몇 개야?" 같은 질문에 모두가 같은 답을 말하게 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 81 / 482

<- **이전**: [080. 하이퍼오토메이션 (Hyperautomation: RPA + AI)](/studynote/07_enterprise_systems/01_strategy_governance/080_hyperautomation_rpa_ai/)
**다음**: [82. MRP (Material Requirements Planning)](/studynote/07_enterprise_systems/02_erp_systems/082_mrp_material_requirements_planning/) ->

---
