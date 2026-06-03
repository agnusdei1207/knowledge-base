+++
weight = 24
title = "24. 형상 상태 기록 (CSA, Configuration Status Accounting)"
date = "2026-04-29"
[extra]
categories = "studynote-software-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CSA (Configuration Status Accounting, 형상 상태 기록)은 [[167_scm_software_configuration_management|SCM]] ([[020_software_configuration_management|Software Configuration Management]], [[648_ccb_configuration_control_board|소프트웨어 형상 관리]])의 4대 활동 중 하나로, 형상 항목([[090_configuration_item|CI]], [[090_configuration_item|Configuration Item]])의 [[655_ir_detection_analysis|식별]]·변경·승인 이력을 체계적으로 기록하고 이해관계자에게 보고하는 가시성(Visibility) 확보 활동이다.
> 2. **가치**: CSA는 "현재 릴리스에 어떤 [[288_version_ihl_tos_total_length|버전]]의 컴포넌트가 포함되어 있는가", "이 변경은 누가 승인했는가", "어떤 CR(Change Request)이 미해결 상태인가"를 언제든지 즉시 답할 수 있게 하여 [[606_auditing_linux_auditd|감사]]([[363_audit|Audit]])와 품질 추적성([[228_blockchain_smart_contract_traceability|Traceability]])을 보장한다.
> 3. **판단 포인트**: CSA의 핵심 산출물은 형상 상태 보고서([[169_pkcs10_csr|CSR]], Configuration Status Report)이며, 이를 통해 변경 요청(CR) 처리 현황, [[025_baseline|기준선]]([[025_baseline|Baseline]]) 구성, 릴리스 포함 항목을 공식화하여 계약·[[303_authentication_authorization_patterns|인증]] [[606_auditing_linux_auditd|감사]]의 증적으로 제출한다.

---

## Ⅰ. 개요 및 필요성

형상 상태 기록(CSA)은 SCM의 네 가지 핵심 활동([[655_ir_detection_analysis|식별]] → 통제 → 상태 기록 → [[606_auditing_linux_auditd|감사]]) 중 세 번째로, [[655_ir_detection_analysis|식별]]된 CI가 어떻게 변경되고 승인되었는지의 전 이력을 데이터베이스에 기록·보관하고 필요 시 보고서를 [[087_process_state_transition|생성]]하는 활동이다.

```text
┌───────────────────────────────────────────────────────┐
│              SCM 4대 활동과 CSA의 위치                  │
├───────────────────────────────────────────────────────┤
│                                                       │
│  1. CI 식별 (Configuration Identification)            │
│           ↓                                           │
│  2. 형상 통제 (Configuration Control) — CCB 승인       │
│           ↓                                           │
│  3. ★ 형상 상태 기록 (CSA) ← 지금 여기                │
│     ├─ 변경 이력 DB 기록                               │
│     ├─ 상태 보고서(CSR) 생성                           │
│     └─ 이해관계자 배포                                 │
│           ↓                                           │
│  4. 형상 감사 (Configuration Audit) — 검증             │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: CSA는 병원 진료 기록부다. 환자([[090_configuration_item|CI]])의 진료 이력(변경 이력), 처방전(승인 내용), 현재 복용약(현재 [[288_version_ihl_tos_total_length|버전]])이 모두 기록되어 있어 언제든 현황을 파악하고 [[606_auditing_linux_auditd|감사]]할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### CSA 기록 항목

| 항목 | 내용 |
|:---|:---|
| **[[090_configuration_item|CI]] [[289_identification_flags_fragmentation_offset|식별자]]** | 이름, [[288_version_ihl_tos_total_length|버전]], 날짜 |
| **변경 요청(CR) 번호** | 연결된 CR ID |
| **변경 이유** | 결함수정, 기능추가, 개선 |
| **승인자** | [[160_change_control_board_ccb_requirements_review|CCB]] (Change Control Board) [[095_determinant_dependent|결정자]] |
| **[[025_baseline|기준선]]([[025_baseline|Baseline]])** | 포함된 [[025_baseline|기준선]] [[289_identification_flags_fragmentation_offset|식별자]] |
| **상태** | 요청→검토→승인→구현→완료 |

### 형상 상태 보고서([[169_pkcs10_csr|CSR]]) 예시

```text
프로젝트: 결제시스템 v3.2   기준일: 2026-04-29
─────────────────────────────────────────────
CI             버전    상태    CR 번호   완료일
PaymentAPI     3.2.1   ✅완료  CR-2041  04-25
OrderService   3.1.9   🔄진행  CR-2055  미정
DBSchema       3.2.0   ✅완료  CR-2038  04-20
─────────────────────────────────────────────
미해결 CR: 1개 (CR-2055), 완료율 66.7%
```

- **📢 섹션 요약 비유**: CSR은 공사 현장의 진도표다. 어떤 공사([[090_configuration_item|CI]])가 어느 단계(상태)에 있는지, 누가 허가했는지([[160_change_control_board_ccb_requirements_review|CCB]]), 언제 완료되는지(일정)가 한눈에 보여 감독관(프로젝트 관리자)이 즉시 파악할 수 있다.

---

## Ⅲ. 비교 및 연결

| 활동 | 목적 | 산출물 |
|:---|:---|:---|
| **[[021_configuration_identification|형상 식별]]** | [[090_configuration_item|CI]] 정의 및 명명 | [[090_configuration_item|CI]] 목록, [[025_baseline|기준선]] 정의 |
| **[[022_configuration_control|형상 통제]]** | 변경 승인 프로세스 | 변경 요청서, [[160_change_control_board_ccb_requirements_review|CCB]] 회의록 |
| **형상 상태 기록 (CSA)** | 이력 기록 및 보고 | [[169_pkcs10_csr|CSR]], 변경 이력 DB |
| **[[023_configuration_audit|형상 감사]]** | [[025_baseline|기준선]] 일치 [[395_verification_process_review|검증]] | [[606_auditing_linux_auditd|감사]] 보고서 |

현대 SW 개발에서 CSA는 Git 커밋 [[568_logs_distributed_logging_elk_fluentd|로그]]·JIRA 이슈 트래커·[[071_jenkins_ci_cd_pipeline_automation|Jenkins]] 빌드 이력이 자동으로 수행하는 역할과 동일하다.

- **📢 섹션 요약 비유**: Git blame, JIRA 이슈 이력, [[071_jenkins_ci_cd_pipeline_automation|Jenkins]] 빌드 [[568_logs_distributed_logging_elk_fluentd|로그]]의 조합이 현대의 자동화 CSA 시스템이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 항공 SW [[303_authentication_authorization_patterns|인증]] [[606_auditing_linux_auditd|감사]] 대응
DO-178C [[303_authentication_authorization_patterns|인증]] 획득을 위한 항공 제어 SW CSA 수행.

1. 모든 소스 [[501_file_definition_logical_record|파일]]([[090_configuration_item|CI]])을 Git 태그 기반 [[025_baseline|기준선]]([[025_baseline|Baseline]])으로 관리.
2. 변경 시마다 JIRA 이슈(CR 번호)와 Git 커밋을 연계.
3. 릴리스 전 [[169_pkcs10_csr|CSR]] [[087_process_state_transition|생성]]: [[025_baseline|기준선]] 구성 [[090_configuration_item|CI]] 목록, 각 CR 처리 상태 포함.
4. DO-178C [[606_auditing_linux_auditd|감사]]관 요청 시 임의 릴리스의 정확한 [[090_configuration_item|CI]] 구성 즉시 추출.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 변경을 Git에는 반영하지만 공식 [[090_configuration_item|CI]] 이력 DB나 JIRA에는 기록하지 않는 [[128_water_scrum_fall_anti_pattern|안티패턴]]. [[606_auditing_linux_auditd|감사]] 시 "이 변경은 누가 승인했는가?"에 답하지 못해 [[303_authentication_authorization_patterns|인증]] 실패로 이어진다. CSA는 변경 승인 추적성([[228_blockchain_smart_contract_traceability|Traceability]])이 핵심이며, 비공식 채널의 변경은 CSA에서 보이지 않는다.

- **📢 섹션 요약 비유**: Git만 쓰고 CSA를 안 하는 건, 공사는 다 하고 건축 허가 서류를 안 남기는 것이다. 나중에 검사([[606_auditing_linux_auditd|감사]])가 오면 증거가 없어 문제가 생긴다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **가시성** | 언제든 SW 구성 현황 즉시 파악 |
| **추적성** | 변경 원인·승인·결과 [[401_transport_layer_role_end_to_end_multiplexing|end-to-end]] 연결 |
| **[[606_auditing_linux_auditd|감사]] 대응** | [[303_authentication_authorization_patterns|인증]]·계약 [[606_auditing_linux_auditd|감사]]에서 증적 즉시 제출 |

CSA는 [[652_devops_calms_culture|DevOps]] 환경에서 [[119_gitops_single_source_of_truth|GitOps]] + JIRA 자동화로 실시간 [[169_pkcs10_csr|CSR]] [[087_process_state_transition|생성]]·대시보드화되는 방향으로 발전하고 있으며, 소프트웨어 [[124_bom_bill_of_materials|BOM]] (Software [[124_bom_bill_of_materials|Bill of Materials]], [[690_sbom_software_supply_chain_security|소프트웨어 자재 명세서]])과 결합하여 [[374_supply_chain_security|공급망 보안]]([[374_supply_chain_security|Supply Chain Security]]) [[606_auditing_linux_auditd|감사]]의 핵심 도구로 확장되고 있다.

- **📢 섹션 요약 비유**: CSA는 시스템의 호적(戶籍)이다. 어떤 컴포넌트가 언제 태어나([[087_process_state_transition|생성]]), 누구 허락으로 변했는지(승인), 지금 어디 있는지([[288_version_ihl_tos_total_length|버전]])가 모두 기록된 공식 문서다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[167_scm_software_configuration_management|SCM]] ([[020_software_configuration_management|형상 관리]])** | CSA가 속하는 상위 관리 체계 |
| **[[160_change_control_board_ccb_requirements_review|CCB]] ([[080_cab|변경 통제 위원회]])** | CSA가 기록하는 승인 주체 |
| **[[025_baseline|기준선]] ([[025_baseline|Baseline]])** | CSA가 추적하는 공식 [[090_configuration_item|CI]] 집합 |
| **소프트웨어 [[124_bom_bill_of_materials|BOM]]** | CSA의 현대적 확장; [[374_supply_chain_security|공급망 보안]] |
| **[[119_gitops_single_source_of_truth|GitOps]]** | CSA를 자동화하는 현대 [[652_devops_calms_culture|DevOps]] 방식 |

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
2. "누가 언제 무엇을 바꿨고, 선생님([[160_change_control_board_ccb_requirements_review|CCB]])이 허락했는지"를 모두 기록해서 나중에 확인할 수 있어요.
3. 비행기나 의료 기기처럼 안전이 중요한 SW는 이 기록이 없으면 검사를 통과할 수 없답니다!
