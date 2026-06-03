+++
title = "126. SCM·ERP·MES 수직 통합 - 계획→실행→현장의 데이터 연속성"
date = 2026-04-19

[taxonomies]
tags = ["studynote-enterprise-systems"]

[extra]
tags = ["studynote-enterprise-systems"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/)([공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 계획)→[ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)(경영 자원 계획)→[MES](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/)(제조 실행)의 <strong>수직 통합</strong>은 수요 예측→생산 계획→현장 실행→실적 피드백의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 끊김 없이 흐르는 체계이다.
> 2. **가치**: 3개 시스템이 분리되면 SCM의 계획이 ERP에 반영되지 않고, ERP의 작업지시가 MES에 전달되지 않아 <strong>계획과 현장의 괴리·재고 과잉·납기 <a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a></strong>이 발생한다.
> 3. **판단 포인트**: [ISA](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/)-95 표준이 [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)↔[MES](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/) 통합 인터페이스를 정의하며, [PLM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/122_plm_product_lifecycle_management/)→[SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/)→[ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)→MES의 수직 통합이 <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/">스마트 팩토리</a>의 핵심 아키텍처</strong>이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    수직 통합 레이어                                    │
├───────────────────────────────────────────────────────┤
│  [SCM]   수요예측 → 공급계획 → 조달                  │
│     ↕ (계획 연동)                                     │
│  [ERP]   생산계획 → 자재소요(MRP) → 작업지시         │
│     ↕ (ISA-95 인터페이스)                             │
│  [MES]   작업실행 → 품질검사 → 실적보고              │
│     ↕ (PLC/SCADA)                                     │
│  [현장]  설비·센서 (OT 레이어)                        │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: SCM은 여행 계획, ERP는 여행 일정표, MES는 현지 가이드(실행), 현장은 실제 여행지이다. 모두 연결되어야 좋은 여행이 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 각 시스템 역할

| 시스템 | 역할 | 시간 단위 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/">SCM</a></strong> | 수요예측·공급계획 | 월~분기 |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/">ERP</a></strong> | 생산계획·자재·원가 | 일~주 |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/">MES</a></strong> | 작업 실행·품질·실적 | **분~시간** |

### [ISA](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/)-95
[ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)↔[MES](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/) 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 교환 표준 (생산 주문·실적·품질).

- **📢 섹션 요약 비유**: [ISA](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/)-95는 사무실([ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/))과 공장([MES](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/)) 사이의 <strong>통역사(번역 표준)</strong>이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 분리 | 수직 통합 |
|:---|:---|:---|
| **계획↔실행** | 괴리 | **실시간 연동** |
| **실적** | 수동 보고 | **자동 피드백** |
| **의사결정** | 사후 | **실시간** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 통합 시 고려사항
1. [ISA](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/)-95 레벨 3([MES](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/))↔레벨 4([ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)) 인터페이스 정의.
2. 실시간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) vs 배치 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 결정.
3. [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)(현장)↔IT(사무실) 보안 분리 (퍼듀 모델).

---

## Ⅴ. 기대효과 및 결론

[SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/)·[ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)·[MES](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/) 수직 통합은 <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/">스마트 팩토리</a>의 정보 흐름 핵심</strong>이며, Digital [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)·[디지털 트윈](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/)과 결합하여 자율 제조로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/">SCM</a></strong> | [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 계획 |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/">ERP</a></strong> | 경영 자원 관리 ([MRP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/082_mrp_material_requirements_planning/) 포함) |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/">MES</a></strong> | 제조 실행 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/">ISA</a>-95</strong> | [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)↔[MES](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/) 통합 표준 |
| <strong>Digital <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">Thread</a></strong> | [PLM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/122_plm_product_lifecycle_management/)→[SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/)→[ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)→[MES](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 연속성 |

### 📈 관련 키워드 및 발전 흐름도

```text
[독립 MRP / MES (1990s)]
    │
    ▼
[ERP + MES 연동 (ISA-95, 2000s)]
    │
    ▼
[SCM + ERP + MES 수직 통합 (2010s)]
    │
    ▼
[스마트 팩토리 (IoT + 통합, 2015~)]
    │
    ▼
[현재: AI + 수직 통합 — 자율 공급망·자율 제조]
```

### 👶 어린이를 위한 3줄 비유 설명
1. SCM은 **여행 계획**, ERP는 **일정표**, MES는 <strong>현지 가이드</strong>예요.
2. 계획([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/))·일정([ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/))·가이드([MES](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/119_mes_manufacturing_execution_system/))가 <strong>서로 연결</strong>되면 완벽한 여행이 돼요.
3. 연결이 안 되면 계획은 파리인데 <strong>가이드는 런던</strong>에 가 있는 혼란이 생겨요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 126 / 482

← **이전**: [125. C-Commerce (Collaborative Commerce) - 기업 간 협업 상거래](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/125_c_commerce_collaborative_commerce/)
**다음**: [127. KMS (Knowledge Management System) - 조직 지식 관리 시스템](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/127_kms_knowledge_management_system/) →

---
