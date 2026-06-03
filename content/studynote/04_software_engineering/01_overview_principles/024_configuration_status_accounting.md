+++
title = "24. 형상 상태 기록 (CSA, Configuration Status Accounting)"
date = 2026-04-29

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CSA (Configuration Status Accounting, 형상 상태 기록)은 [SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/) ([Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/), [소프트웨어 형상 관리](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/648_ccb_configuration_control_board/))의 4대 활동 중 하나로, 형상 항목([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/), [Configuration Item](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/))의 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)·변경·승인 이력을 체계적으로 기록하고 이해관계자에게 보고하는 가시성(Visibility) 확보 활동이다.
> 2. **가치**: CSA는 "현재 릴리스에 어떤 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)의 컴포넌트가 포함되어 있는가", "이 변경은 누가 승인했는가", "어떤 CR(Change Request)이 미해결 상태인가"를 언제든지 즉시 답할 수 있게 하여 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)([Audit](/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/))와 품질 추적성([Traceability](/knowledge-base/studynote/12_it_management/05_security_compliance/228_blockchain_smart_contract_traceability/))을 보장한다.
> 3. **판단 포인트**: CSA의 핵심 산출물은 형상 상태 보고서([CSR](/knowledge-base/studynote/09_security/04_endpoint_security/169_pkcs10_csr/), Configuration Status Report)이며, 이를 통해 변경 요청(CR) 처리 현황, [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) 구성, 릴리스 포함 항목을 공식화하여 계약·[인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)의 증적으로 제출한다.

---

## Ⅰ. 개요 및 필요성

형상 상태 기록(CSA)은 SCM의 네 가지 핵심 활동([식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) → 통제 → 상태 기록 → [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)) 중 세 번째로, [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)된 CI가 어떻게 변경되고 승인되었는지의 전 이력을 데이터베이스에 기록·보관하고 필요 시 보고서를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 활동이다.

```text
┌───────────────────────────────────────────────────────┐
│ SCM 4대 활동과 CSA의 위치 │
├───────────────────────────────────────────────────────┤
│ │
│ 1. CI 식별 (Configuration Identification) │
│ ↓ │
│ 2. 형상 통제 (Configuration Control) — CCB 승인 │
│ ↓ │
│ 3. ★ 형상 상태 기록 (CSA) ← 지금 여기 │
│ ├─ 변경 이력 DB 기록 │
│ ├─ 상태 보고서(CSR) 생성 │
│ └─ 이해관계자 배포 │
│ ↓ │
│ 4. 형상 감사 (Configuration Audit) — 검증 │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: CSA는 병원 진료 기록부다. 환자([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/))의 진료 이력(변경 이력), 처방전(승인 내용), 현재 복용약(현재 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/))이 모두 기록되어 있어 언제든 현황을 파악하고 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### CSA 기록 항목

| 항목 | 내용 |
|:---|:---|
| **[CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)** | 이름, [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 날짜 |
| **변경 요청(CR) 번호** | 연결된 CR ID |
| **변경 이유** | 결함수정, 기능추가, 개선 |
| **승인자** | [CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/) (Change Control Board) [결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/) |
| **[기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/))** | 포함된 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) |
| **상태** | 요청→검토→승인→구현→완료 |

### 형상 상태 보고서([CSR](/knowledge-base/studynote/09_security/04_endpoint_security/169_pkcs10_csr/)) 예시

```text
프로젝트: 결제시스템 v3.2 기준일: 2026-04-29
─────────────────────────────────────────────
CI 버전 상태 CR 번호 완료일
PaymentAPI 3.2.1 ✅완료 CR-2041 04-25
OrderService 3.1.9 🔄진행 CR-2055 미정
DBSchema 3.2.0 ✅완료 CR-2038 04-20
─────────────────────────────────────────────
미해결 CR: 1개 (CR-2055), 완료율 66.7%
```

- **📢 섹션 요약 비유**: CSR은 공사 현장의 진도표다. 어떤 공사([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/))가 어느 단계(상태)에 있는지, 누가 허가했는지([CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/)), 언제 완료되는지(일정)가 한눈에 보여 감독관(프로젝트 관리자)이 즉시 파악할 수 있다.

---

## Ⅲ. 비교 및 연결

| 활동 | 목적 | 산출물 |
|:---|:---|:---|
| **[형상 식별](/knowledge-base/studynote/04_software_engineering/01_overview_principles/021_configuration_identification/)** | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 정의 및 명명 | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 목록, [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) 정의 |
| **[형상 통제](/knowledge-base/studynote/04_software_engineering/01_overview_principles/022_configuration_control/)** | 변경 승인 프로세스 | 변경 요청서, [CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/) 회의록 |
| **형상 상태 기록 (CSA)** | 이력 기록 및 보고 | [CSR](/knowledge-base/studynote/09_security/04_endpoint_security/169_pkcs10_csr/), 변경 이력 DB |
| **[형상 감사](/knowledge-base/studynote/04_software_engineering/01_overview_principles/023_configuration_audit/)** | [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) 일치 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 보고서 |

현대 SW 개발에서 CSA는 Git 커밋 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·JIRA 이슈 트래커·[Jenkins](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/) 빌드 이력이 자동으로 수행하는 역할과 동일하다.

- **📢 섹션 요약 비유**: Git blame, JIRA 이슈 이력, [Jenkins](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/) 빌드 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)의 조합이 현대의 자동화 CSA 시스템이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 항공 SW [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 대응
DO-178C [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 획득을 위한 항공 제어 SW CSA 수행.

1. 모든 소스 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/))을 Git 태그 기반 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/))으로 관리.
2. 변경 시마다 JIRA 이슈(CR 번호)와 Git 커밋을 연계.
3. 릴리스 전 [CSR](/knowledge-base/studynote/09_security/04_endpoint_security/169_pkcs10_csr/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/): [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) 구성 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 목록, 각 CR 처리 상태 포함.
4. DO-178C [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)관 요청 시 임의 릴리스의 정확한 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 구성 즉시 추출.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 변경을 Git에는 반영하지만 공식 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 이력 DB나 JIRA에는 기록하지 않는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/). [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 시 "이 변경은 누가 승인했는가?"에 답하지 못해 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 실패로 이어진다. CSA는 변경 승인 추적성([Traceability](/knowledge-base/studynote/12_it_management/05_security_compliance/228_blockchain_smart_contract_traceability/))이 핵심이며, 비공식 채널의 변경은 CSA에서 보이지 않는다.

- **📢 섹션 요약 비유**: Git만 쓰고 CSA를 안 하는 건, 공사는 다 하고 건축 허가 서류를 안 남기는 것이다. 나중에 검사([감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/))가 오면 증거가 없어 문제가 생긴다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **가시성** | 언제든 SW 구성 현황 즉시 파악 |
| **추적성** | 변경 원인·승인·결과 [end-to-end](/knowledge-base/studynote/03_network/08_transport_layer/401_transport_layer_role_end_to_end_multiplexing/) 연결 |
| **[감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 대응** | [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·계약 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)에서 증적 즉시 제출 |

CSA는 [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 환경에서 [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) + JIRA 자동화로 실시간 [CSR](/knowledge-base/studynote/09_security/04_endpoint_security/169_pkcs10_csr/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·대시보드화되는 방향으로 발전하고 있으며, 소프트웨어 [BOM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/), [소프트웨어 자재 명세서](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/690_sbom_software_supply_chain_security/))과 결합하여 [공급망 보안](/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/)([Supply Chain Security](/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/)) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)의 핵심 도구로 확장되고 있다.

- **📢 섹션 요약 비유**: CSA는 시스템의 호적()이다. 어떤 컴포넌트가 언제 태어나([생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)), 누구 허락으로 변했는지(승인), 지금 어디 있는지([버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/))가 모두 기록된 공식 문서다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/) ([형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/))** | CSA가 속하는 상위 관리 체계 |
| **[CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/) ([변경 통제 위원회](/knowledge-base/studynote/12_it_management/02_itsm_itil/080_cab/))** | CSA가 기록하는 승인 주체 |
| **[기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) ([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/))** | CSA가 추적하는 공식 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 집합 |
| **소프트웨어 [BOM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)** | CSA의 현대적 확장; [공급망 보안](/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/) |
| **[GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/)** | CSA를 자동화하는 현대 [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
[SCM 형상 식별 — CI 정의 및 기준선 설정]
│
▼
[형상 통제 — CCB 변경 승인 프로세스]
│
▼
[CSA — 변경 이력 기록, CSR 생성 (★ 지금 여기)]
│
▼
[형상 감사 — 기준선 일치 검증, 인증 증적]
│
▼
[SW BOM + GitOps — 자동화 CSA, 공급망 보안]
```

### 👶 어린이를 위한 3줄 비유 설명

1. CSA는 학교 성적 기록부처럼, 소프트웨어의 모든 변경 내역을 빠짐없이 적어놓는 것이에요!
2. "누가 언제 무엇을 바꿨고, 선생님([CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/))이 허락했는지"를 모두 기록해서 나중에 확인할 수 있어요.
3. 비행기나 의료 기기처럼 안전이 중요한 SW는 이 기록이 없으면 검사를 통과할 수 없답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 24 / 973

← **이전**: [23. 형상 감사 (Configuration Audit)](/knowledge-base/studynote/04_software_engineering/01_overview_principles/023_configuration_audit/)
**다음**: [25. 기준선 (Baseline) — 형상 관리의 공식 참조점](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) →

---
