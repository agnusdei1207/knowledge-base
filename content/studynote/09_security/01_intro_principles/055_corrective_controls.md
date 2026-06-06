---
title: "Corrective Controls"
date: "2026-05-01"
tags:
  - "studynote-security"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 교정 통제 ([Corrective](/studynote/04_software_engineering/06_software_architecture/380_maintenance_types/) Controls)는 사고나 이상이 발생한 뒤 원상 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)하거나 피해를 줄이는 보안 통제다.
> 2. **가치**: [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 패치, [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), 계정 복원, 구성 수정이 대표적인 교정 수단이다.
> 3. **판단 포인트**: 예방·탐지 통제와 연결되어야 효과가 있다. [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차가 없으면 교정이 아니다.

---

## Ⅰ. 개요 및 필요성

사고를 완전히 막지 못하는 현실에서, 빠르게 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)하는 능력은 매우 중요하다. 교정 통제는 바로 그 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 능력을 담당한다.

침해나 장애가 발생한 뒤 피해를 최소화하고 정상 상태로 돌려놓는 것이 목적이다.

- **📢 섹션 요약 비유**: 교정 통제는 깨진 그릇을 다시 붙이거나 새 그릇으로 바꾸는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

교정 통제는 탐지 후 대응, [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 재설정, 검증으로 이어진다. 단순한 사후 처리보다 재발 방지까지 포함하는 경우가 많다.

```text
Incident -> Containment -> Recovery -> Restoration -> Verification
```

| 수단 | 역할 | 예시 |
| :--- | :--- | :--- |
| [Backup](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)/Restore | [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복원 |
| Patch | 수정 | 취약점 보완 |
| [Rollback](/studynote/02_operating_system/05_deadlock/313_rollback/) | 되돌리기 | 배포 취소 |
| Reconfiguration | 재설정 | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 수정 |

핵심은 사고 후에 시스템을 정상으로 돌리는 것과, 다음 사고를 줄이기 위한 보완까지 포함한다는 점이다.

- **📢 섹션 요약 비유**: 교정 통제는 넘어져서 찢어진 옷을 꿰매는 일이다.

---

## Ⅲ. 비교 및 연결

교정 통제는 예방 통제와 탐지 통제를 보완한다. 예방이 실패하고 탐지가 끝나면, 교정이 실제 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를 맡는다.

| 통제 유형 | 역할 |
| :--- | :--- |
| Preventive | 막기 |
| Detective | 찾기 |
| [Corrective](/studynote/04_software_engineering/06_software_architecture/380_maintenance_types/) | 고치기 |

[복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)만 하고 원인 제거를 하지 않으면 같은 사고가 반복된다. 그래서 문제 관리와도 이어진다.

- **📢 섹션 요약 비유**: 예방은 문 잠그기, 탐지는 누가 들어왔는지 알기, 교정은 들어온 뒤 치우기다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시험, [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 절차, [패치 관리](/studynote/09_security/04_endpoint_security/406_patch_management/), 재해복구(Disaster [Recovery](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)) 계획이 핵심이다. [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 목표와 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시점 목표도 중요하다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차가 문서화되어 있는가?
2. [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 복원 테스트를 하는가?
3. [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)이 실제로 가능한가?
4. 교정 후 재발 방지 조치가 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)은 있지만 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 안 되는 경우
- 패치만 하고 재발 방지는 없는 경우
- [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차를 사람 기억에만 의존하는 경우

기술사 관점에서는 교정 통제가 사고 후 피해를 줄이고 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 연속성을 회복하는 핵심이라는 점을 설명해야 한다.

- **📢 섹션 요약 비유**: 교정 통제는 부서진 장난감을 고치는 수리공이다.

---

## Ⅴ. 기대효과 및 결론

교정 통제는 사고 후 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 속도를 높이고 피해를 최소화한다. 운영 안정성과 복원력을 높이는 마지막 방어선이다.

정리하면, 교정 통제는 "이미 일어난 일"을 수습하는 핵심 통제다.

- **📢 섹션 요약 비유**: 교정 통제는 넘어졌을 때 일으켜 세우는 손이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Backup](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)/Restore | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| Patch | 취약점 수정 |
| [Rollback](/studynote/02_operating_system/05_deadlock/313_rollback/) | 되돌리기 |
| [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) | 재해복구 |
| [Verification](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |

### 📈 관련 키워드 및 발전 흐름도

```text
사고 발생
    |
    v
격리 / 복구
    |
    v
원상 복원
    |
    v
검증 / 재발 방지
```

이 흐름은 보안 사고나 장애 이후 시스템을 정상 상태로 되돌리는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 교정 통제는 망가진 장난감을 고치는 일이에요.
2. 다시 놀 수 있게 원래대로 돌려놓아요.
3. 다음엔 덜 망가지도록 방법도 바꿔요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 55 / 1108

<- **이전**: [54. 탐지 통제 (Detective Controls)](/studynote/09_security/01_intro_principles/054_detective_controls/)
**다음**: [56. 억제 통제 (Deterrent Controls) - 위협 행동 억제](/studynote/09_security/01_intro_principles/056_deterrent_controls/) ->

---
