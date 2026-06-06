---
title: "122. Plm Product Lifecycle Management"
date: "2026-04-19"
tags:
  - "studynote-enterprise-systems"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: PLM은 제품의 <strong>기획->설계->제조-><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>->폐기까지 전 생명주기에 걸친 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>·프로세스·사람을 통합 관리</strong>하는 엔터프라이즈 시스템이다.
> 2. **가치**: CAD 도면·[BOM](/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)(부품 목록)·변경 이력·품질 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 부서별로 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)되면 <strong>설계 변경 누락·부품 불일치·품질 사고</strong>가 발생하지만, PLM이 <strong>단일 제품 <a href="/studynote/16_bigdata/09_platform/180_data_hub/">데이터 허브</a></strong>를 제공하여 전사 협업을 보장한다.
> 3. **판단 포인트**: PLM은 [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)(생산·재무)·[MES](/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/)(제조 실행)·[SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/)([공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/))과 통합되어 <strong>제품 중심 디지털 <a href="/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a>(Digital <a href="/studynote/02_operating_system/02_process_thread/092_thread_lwp/">Thread</a>)</strong>를 구성하며, [디지털 트윈](/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/)의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 원천이 된다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    PLM이 관리하는 제품 전주기                          |
+-------------------------------------------------------+
|  기획 -> 설계(CAD) -> 시뮬레이션(CAE) -> 제조(CAM)     |
|     -> 품질관리 -> 서비스·유지보수 -> 폐기·재활용      |
|                                                       |
|  PLM 관리 대상:                                       |
|   - CAD 도면·3D 모델                                 |
|   - BOM (Bill of Materials, 부품 목록)               |
|   - ECO (Engineering Change Order, 설계 변경)        |
|   - 품질·시험 데이터                                 |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: PLM은 제품의 <strong>출생(기획)부터 사망(폐기)</strong>까지의 모든 기록을 보관하는 전자 건강 기록부다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### PLM 핵심 기능

| 기능 | 설명 |
|:---|:---|
| **CAD 관리** | 도면·3D 모델 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 |
| <strong><a href="/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/">BOM</a> 관리</strong> | 부품 구성 트리, E-[BOM](/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)/M-[BOM](/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/) |
| <strong><a href="/studynote/12_it_management/02_itsm_itil/079_change_enablement/">변경 관리</a></strong> | ECR->ECO->ECN 워크플로 |
| **프로젝트 관리** | 제품 개발 일정·마일스톤 |
| **품질 관리** | [FMEA](/studynote/01_computer_architecture/15_advanced_topics/752_fmea/)·CAPA 연동 |

- **📢 섹션 요약 비유**: BOM은 요리 레시피(재료 목록)이고, ECO는 레시피 변경 승인 절차다.

---

## Ⅲ. 비교 및 연결

| 비교 | PLM | [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) | [MES](/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/) |
|:---|:---|:---|:---|
| **관점** | <strong>제품 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong> | 경영·재무 | 제조 실행 |
| **단계** | 설계~폐기 | 계획~재무 | 생산 현장 |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong> | CAD·[BOM](/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)·ECO | 주문·재고·원가 | 실적·품질 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Digital [Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)
PLM->[ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)->[MES](/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/)->[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 관통하는 제품 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 연속적 흐름으로, 설계 변경이 제조·[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 즉시 반영된다.

---

## Ⅴ. 기대효과 및 결론

PLM은 <strong>제조업 <a href="/studynote/04_software_engineering/10_trends_pm_quality/726_platform_engineering_idp_dx/">DX</a>(<a href="/studynote/12_it_management/01_governance_strategy/055_digital_transformation/">디지털 전환</a>)의 핵심 축</strong>이며, [디지털 트윈](/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/)·[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시뮬레이션과 결합하여 제품 개발 기간을 30~50% 단축하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/">BOM</a></strong> | 부품 구성 목록 (PLM 핵심 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) |
| **ECO** | 설계 [변경 관리](/studynote/12_it_management/02_itsm_itil/079_change_enablement/) |
| <strong>Digital <a href="/studynote/02_operating_system/02_process_thread/092_thread_lwp/">Thread</a></strong> | PLM->[ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)->[MES](/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 연속성 |
| <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/">디지털 트윈</a></strong> | PLM [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 가상 모델 |
| **CAD/CAE/CAM** | PLM이 관리하는 설계 도구 산출물 |

### 📈 관련 키워드 및 발전 흐름도

```text
[PDM (Product Data Management, 1990s)]
    |
    v
[PLM (전주기 확장, 2000s) — Siemens·PTC·Dassault]
    |
    v
[클라우드 PLM (2015~) — SaaS 기반]
    |
    v
[Digital Thread + 디지털 트윈 (2020~)]
    |
    v
[현재: AI PLM — 생성적 설계·자동 BOM 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. PLM은 제품의 <strong>출생(기획)부터 은퇴(폐기)</strong>까지의 모든 기록을 관리하는 시스템이에요.
2. 레시피([BOM](/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))를 바꾸려면 <strong>승인(ECO)</strong>을 받아야 해서 실수가 줄어요.
3. 덕분에 자동차·비행기 같은 복잡한 제품도 <strong>체계적으로 개발</strong>할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 122 / 482

<- **이전**: [121. 스마트 팩토리 4단계 (Smart Factory Maturity Levels) - Industry 4.0 성숙도 모델](/studynote/07_enterprise_systems/02_erp_systems/121_smart_factory_4_levels/)
**다음**: [123. PDM (Product Data Management) - 제품 데이터 관리 시스템](/studynote/07_enterprise_systems/02_erp_systems/123_pdm_product_data_management/) ->

---
