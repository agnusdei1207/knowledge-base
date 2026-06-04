---
title: "54. 변경 관리와 CAB (Change Management CAB)"
date: "2026-05-01"
tags:
  - "studynote-enterprise-systems"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [변경 관리](/studynote/12_it_management/02_itsm_itil/079_change_enablement/) ([Change Management](/studynote/04_software_engineering/01_overview_principles/027_change_management/))는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 변경의 위험을 통제하는 [ITSM](/studynote/12_it_management/02_itsm_itil/880_iso_iec_20000_itsm_certification/) ([IT Service Management](/studynote/12_it_management/02_itsm_itil/845_itsm/)) 절차다.
> 2. **가치**: [CAB](/studynote/12_it_management/02_itsm_itil/080_cab/) (Change Advisory Board)는 변경의 영향, 우선순위, 승인 여부를 검토한다.
> 3. **판단 포인트**: 표준 변경, 정상 변경, 긴급 변경을 구분해야 승인 흐름이 명확해진다.

---

## Ⅰ. 개요 및 필요성

[서비스 운영](/studynote/12_it_management/02_itsm_itil/067_service_operation/)에서는 모든 변경이 위험이다. 패치, [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 변경, 배포, 인프라 수정은 고객 영향으로 이어질 수 있다.

[변경 관리](/studynote/12_it_management/02_itsm_itil/079_change_enablement/)는 이런 위험을 미리 검토하고, 누가 승인할지 정하는 절차다.

- **📢 섹션 요약 비유**: [변경 관리](/studynote/12_it_management/02_itsm_itil/079_change_enablement/)는 공사 전에 안전 점검표를 보는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

변경은 보통 요청 -> 평가 -> 승인 -> 실행 -> 검토 순서로 흐른다. CAB는 이 과정에서 영향도와 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)를 판단한다.

```text
Change Request -> Impact/Risk Review -> CAB Approval -> Implementation -> Review
```

| 유형 | 의미 | 승인 흐름 |
| :--- | :--- | :--- |
| Standard Change | 반복적 저위험 | 사전 승인 |
| Normal Change | 일반 변경 | [CAB](/studynote/12_it_management/02_itsm_itil/080_cab/) 검토 |
| Emergency Change | 긴급 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | [ECAB](/studynote/12_it_management/02_itsm_itil/865_feature_engineering/)/신속 승인 |

핵심은 변경을 막는 것이 아니라, 안전하게 통과시키는 것이다. CAB는 모든 변경을 사람 감으로 승인하는 조직이 아니라, 기준과 증거를 보는 위원회다.

- **📢 섹션 요약 비유**: CAB는 공사 허가를 내기 전에 설계도와 안전계획을 보는 심사위원이다.

---

## Ⅲ. 비교 및 연결

[변경 관리](/studynote/12_it_management/02_itsm_itil/079_change_enablement/)는 Incident/Problem Management와 연결된다. 장애를 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)하는 것과, 변경을 승인해 배포하는 것은 다른 절차다.

| 항목 | [변경 관리](/studynote/12_it_management/02_itsm_itil/079_change_enablement/) | 장애 관리 |
| :--- | :--- | :--- |
| 목적 | 안전한 변경 | 빠른 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| 핵심 질문 | 바꿔도 되는가 | 지금 어떻게 살릴까 |
| 결과 | 승인/거부 | [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)/우회 |

CAB는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 안정성, 보안, 규정 준수를 동시에 고려해야 한다. 그래서 변경 일정, 유지보수 창, [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 계획이 중요하다.

- **📢 섹션 요약 비유**: [변경 관리](/studynote/12_it_management/02_itsm_itil/079_change_enablement/)는 문을 열어 줄지 말지 보는 경비실, 장애 관리는 불 난 건물에서 사람을 꺼내는 소방대다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 변경 요청서, 영향도 분석, 테스트 결과, [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 계획, 승인 기록을 남겨야 한다. 긴급 변경도 사후 검토가 필요하다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 변경 유형이 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)되는가?
2. 영향도와 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)가 문서화되는가?
3. [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 계획이 있는가?
4. [CAB](/studynote/12_it_management/02_itsm_itil/080_cab/)/[ECAB](/studynote/12_it_management/02_itsm_itil/865_feature_engineering/) 승인 기록이 남는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모든 변경을 긴급처럼 처리하는 경우
- 승인 없이 운영 배포를 강행하는 경우
- 사후 검토 없이 변경만 누적하는 경우

기술사 관점에서는 CAB가 단순 결재 조직이 아니라 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)를 관리하는 통제 포인트라는 점을 설명해야 한다.

- **📢 섹션 요약 비유**: CAB는 차가 들어오기 전에 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)등 색을 바꾸는 교통 관제실이다.

---

## Ⅴ. 기대효과 및 결론

[변경 관리](/studynote/12_it_management/02_itsm_itil/079_change_enablement/)는 장애를 줄이고, 변경 이력을 남기며, 운영 안정성을 높인다. CAB는 그 결정을 체계화하는 장치다.

정리하면, 잘 된 [변경 관리](/studynote/12_it_management/02_itsm_itil/079_change_enablement/)는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 안전벨트다.

- **📢 섹션 요약 비유**: [변경 관리](/studynote/12_it_management/02_itsm_itil/079_change_enablement/)는 가구를 옮기기 전에 문폭을 재는 습관이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [CAB](/studynote/12_it_management/02_itsm_itil/080_cab/) | 변경 심의 |
| [ECAB](/studynote/12_it_management/02_itsm_itil/865_feature_engineering/) | 긴급 심의 |
| Standard Change | 사전 승인 |
| [Risk](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) Assessment | 영향 평가 |
| [Rollback](/studynote/02_operating_system/05_deadlock/313_rollback/) | [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 계획 |

### 📈 관련 키워드 및 발전 흐름도

```text
변경 요청
    |
    v
리스크 평가
    |
    v
CAB / ECAB 승인
    |
    v
실행 / 검토
```

이 흐름은 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 변경이 통제된 절차를 통해 운영되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. CAB는 방을 고치기 전에 어른들이 모여서 안전한지 보는 회의예요.
2. 급한 경우도 있지만, 그때도 꼭 다시 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해요.
3. 그래서 집이 망가지지 않게 할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 54 / 482

<- **이전**: [53. 문제 관리와 근본 원인 분석 (Problem Management RCA)](/studynote/07_enterprise_systems/01_strategy_governance/053_problem_management_rca/)
**다음**: [55. 릴리스와 배포 관리 (Release and Deployment Management)](/studynote/07_enterprise_systems/01_strategy_governance/055_release_and_deployment_management/) ->

---
