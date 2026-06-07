---
title: "ITIL ITSM Audit"
date: "2026-05-01"
tags:
  - "studynote-design-supervision"
weight: 54
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [ITIL](/studynote/12_it_management/02_itsm_itil/846_itil/)/[ITSM](/studynote/12_it_management/02_itsm_itil/880_iso_iec_20000_itsm_certification/) [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 관리 프로세스가 정의된 절차와 증거에 따라 수행되는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)다.
> 2. **가치**: 인시던트, 문제, 변경, [서비스 수준 관리](/studynote/12_it_management/02_itsm_itil/868_service_level_management/) 등 핵심 프로세스의 준수와 효과성을 검증한다.
> 3. **판단 포인트**: 문서 존재만 보지 말고, 실제 티켓과 기록이 절차대로 움직였는지를 봐야 한다.

---

## Ⅰ. 개요 및 필요성

[ITIL](/studynote/12_it_management/02_itsm_itil/846_itil/) 기반 ITSM은 [서비스 운영](/studynote/12_it_management/02_itsm_itil/067_service_operation/)을 표준화한다. [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 그 표준이 실제로 지켜지고 있는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 절차다.

문서와 현실이 다르면 통제는 실패한 것이다. 그래서 증거 중심으로 봐야 한다.

- **📢 섹션 요약 비유**: [ITIL](/studynote/12_it_management/02_itsm_itil/846_itil/)/[ITSM](/studynote/12_it_management/02_itsm_itil/880_iso_iec_20000_itsm_certification/) [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 규칙집이 아니라 실제 운동장에서 규칙이 지켜지는지 보는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 프로세스 정의, 증적 수집, 샘플 검사, 부적합 판정, 개선 권고로 흐른다. ITSM은 사람의 기억이 아니라 기록으로 평가해야 한다.

```text
Process Definition -> Ticket/Evidence Review -> Compliance Check -> Findings -> Improvement
```

| 대상 | [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 포인트 | 예시 |
| :--- | :--- | :--- |
| Incident | 응답/[복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차 | [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/) 준수 |
| Change | 승인/[롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) | [CAB](/studynote/12_it_management/02_itsm_itil/080_cab/) 기록 |
| Problem | RCA/[KEDB](/studynote/12_it_management/02_itsm_itil/862_kedb/) | 재발 방지 |
| [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Level | 측정/보고 | [KPI](/studynote/12_it_management/01_governance_strategy/018_kpi/)/[SLA](/studynote/12_it_management/02_itsm_itil/869_sla/) |

핵심은 [ITIL](/studynote/12_it_management/02_itsm_itil/846_itil/) 프로세스가 실제 운영에서 유지되는지, 그리고 증빙이 남는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 것이다.

- **📢 섹션 요약 비유**: [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 시험지뿐 아니라 채점표와 답안지를 같이 보는 선생님이다.

---

## Ⅲ. 비교 및 연결

[ITIL](/studynote/12_it_management/02_itsm_itil/846_itil/)/[ITSM](/studynote/12_it_management/02_itsm_itil/880_iso_iec_20000_itsm_certification/) [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 일반 IT [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)와 다르게 [서비스 운영](/studynote/12_it_management/02_itsm_itil/067_service_operation/) 프로세스에 더 집중한다. 둘은 겹치지만 초점이 다르다.

| 항목 | [ITIL](/studynote/12_it_management/02_itsm_itil/846_itil/)/[ITSM](/studynote/12_it_management/02_itsm_itil/880_iso_iec_20000_itsm_certification/) [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) | 일반 IT [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) |
| :--- | :--- | :--- |
| 초점 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 프로세스 | IT 통제 전반 |
| 증거 | 티켓, [KPI](/studynote/12_it_management/01_governance_strategy/018_kpi/), [CAB](/studynote/12_it_management/02_itsm_itil/080_cab/) | 접근권한, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 구성 |
| 목적 | 운영 성숙도 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 통제 적합성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |

[ITIL](/studynote/12_it_management/02_itsm_itil/846_itil/) [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 incident/problem/change 흐름이 제대로 이어지는지, 고객 영향이 관리되는지, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 개선이 누적되는지 본다.

- **📢 섹션 요약 비유**: [ITIL](/studynote/12_it_management/02_itsm_itil/846_itil/) [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 급식소의 위생과 배식 순서를 보는 검사다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 프로세스 문서, 샘플 티켓, 승인 기록, 측정 지표, 개선 조치가 핵심 증거다. [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 일회성 점검이 아니라 지속 개선과 연결되어야 한다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 프로세스 문서와 실제 수행이 일치하는가?
2. 승인/기록/증거가 남는가?
3. KPI와 SLA가 측정되는가?
4. 부적합 항목에 대한 개선이 이뤄지는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 문서만 있고 티켓 증거가 없는 경우
- 승인 절차가 형식만 남은 경우
- [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 후 개선 조치가 추적되지 않는 경우

기술사 관점에서는 [ITSM](/studynote/12_it_management/02_itsm_itil/880_iso_iec_20000_itsm_certification/) [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)가 단순 서류 검토가 아니라 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 관리의 실행력을 검증하는 활동이라는 점을 설명해야 한다.

- **📢 섹션 요약 비유**: [ITIL](/studynote/12_it_management/02_itsm_itil/846_itil/)/[ITSM](/studynote/12_it_management/02_itsm_itil/880_iso_iec_20000_itsm_certification/) [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 청소 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)와 실제 바닥 상태를 같이 보는 일이다.

---

## Ⅴ. 기대효과 및 결론

[ITIL](/studynote/12_it_management/02_itsm_itil/846_itil/)/[ITSM](/studynote/12_it_management/02_itsm_itil/880_iso_iec_20000_itsm_certification/) [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 [서비스 운영](/studynote/12_it_management/02_itsm_itil/067_service_operation/)의 일관성과 개선 가능성을 높인다. 증거 기반으로 프로세스를 검증할 때 조직의 성숙도가 올라간다.

정리하면, [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 규칙이 현장에서 살아 있는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 거울이다.

- **📢 섹션 요약 비유**: [ITIL](/studynote/12_it_management/02_itsm_itil/846_itil/)/[ITSM](/studynote/12_it_management/02_itsm_itil/880_iso_iec_20000_itsm_certification/) [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 운동장에 그려진 선이 지워지지 않았는지 보는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Incident | [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 프로세스 |
| Change | 승인/배포 |
| Problem | 원인 분석 |
| [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 |
| Evidence | 증적 |

### 📈 관련 키워드 및 발전 흐름도

```text
프로세스 정의
    |
    v
운영 증적
    |
    v
감사 검토
    |
    v
부적합 / 개선
```

이 흐름은 IT [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 관리가 규칙에서 증거 기반 개선으로 이어지는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [ITIL](/studynote/12_it_management/02_itsm_itil/846_itil/)/[ITSM](/studynote/12_it_management/02_itsm_itil/880_iso_iec_20000_itsm_certification/) [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 선생님이 숙제 규칙이 지켜졌는지 보는 거예요.
2. 말만 하는 게 아니라 실제로 한 기록이 있어야 해요.
3. 그래서 다음에는 더 잘하게 만들 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 81 / 530

<- **이전**: [53. 블록체인 감사 (Blockchain Audit)](/studynote/11_design_supervision/01_audit_framework/053_blockchain_audit/)
**다음**: [55. ISMS-P 감사 (ISMS-P Audit)](/studynote/11_design_supervision/01_audit_framework/055_isms_p_audit/) ->

---
