---
title: "316. Management"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
---

> **핵심 인사이트**
> - [SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) ([Site Reliability 엔진ering](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/))는 구글이 정의한 "소프트웨어 엔지니어링 방식으로 운영 문제를 해결하는 방법론"이다.
> - [Toil](/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) ([토일](/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)) 자동화, [Error Budget](/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/) (에러 버짓) 관리, 50% 운영 업무 상한선이 SRE의 세 핵심 원칙이다.
> - DevOps는 문화·철학이고, SRE는 그 철학을 구체적으로 구현하는 실천 방법론이다.

---

## Ⅰ. [SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 정의와 DevOps와의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

SRE는 Google이 2003년에 시작한 직군으로, "[신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 소프트웨어 엔지니어링으로 달성"한다.

| 항목        | [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)                       | [SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/)                              |
|-------------|------------------------------|----------------------------------|
| 성격        | 문화·철학                     | 구체적 실천 방법론                |
| 초점        | 빠른 전달 + 안정성 균형        | [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 정량화 + 자동화            |
| 지표        | [리드 타임](/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/), 배포 빈도           | [SLI](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/), [SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/), [Error Budget](/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/)           |

```
+----------------------------------------------------+
|                 SRE 핵심 원칙                      |
|                                                    |
|  1. SLO 기반 신뢰성 목표 정의                      |
|  2. Error Budget으로 혁신-안정성 균형              |
|  3. Toil 자동화 (운영 업무 50% 상한)               |
|  4. Blameless Postmortem 문화                      |
+----------------------------------------------------+
```

> 📢 **Ⅰ 섹션 요약 비유**
> DevOps가 "빠르고 안정적으로 달리자"는 철학이라면, SRE는 그 철학을 속도계·계기판·자동운전으로 구현하는 것이다.

---

## Ⅱ. [SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 엔지니어의 역할과 50% 규칙

SRE는 운영 업무(On-[call](/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/), 티켓, 수동 배포)를 최대 50%로 제한하고, 나머지를 엔지니어링(자동화, 개선)에 써야 한다.

| 업무 유형         | 목표 비율 | 예시                           |
|-------------------|-----------|--------------------------------|
| 운영([Toil](/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/))        | ≤ 50%     | 수동 배포, 알림 처리           |
| 엔지니어링        | ≥ 50%     | 자동화, 용량 계획, 도구 개발   |

On-[call](/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/) (온콜) 부담을 줄이기 위해 알림(Alert)은 Actionable(즉각 조치 필요)한 것만 남기고, 노이즈는 제거한다.

> 📢 **Ⅱ 섹션 요약 비유**
> SRE는 소방관이 화재 진압(운영)보다 방화 시스템 설치(엔지니어링)에 더 많은 시간을 써야 한다는 원칙을 지킨다.

---

## Ⅲ. [Error Budget](/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/) 운영

[Error Budget](/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/) = `1 - SLO`

[SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) ([Service Level Objective](/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/))가 99.9%이면 월 43.8분의 다운타임이 허용되는 예산이다.

```
Error Budget 소진 시나리오
-------------------------
예산 여유 있음: 신기능 배포 가속 가능
예산 소진 경고: 배포 속도 조절, 안정화 우선
예산 완전 소진: 기능 동결, 신뢰성 개선 집중
```

이를 통해 개발팀과 운영팀이 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 공동 목표로 삼게 된다.

> 📢 **Ⅲ 섹션 요약 비유**
> Error Budget은 "이번 달 고장 허용 쿠폰" — 다 쓰면 새 기능 출시는 잠시 멈춰야 한다.

---

## Ⅳ. Capacity Planning과 Production Readiness [Review](/studynote/04_software_engineering/03_design_architecture/153_requirements_review_inspection_walkthrough/)

Capacity Planning (용량 계획): 부하 예측 기반 리소스 사전 확보로 트래픽 급증에 대비한다.

PRR (Production Readiness [Review](/studynote/04_software_engineering/03_design_architecture/153_requirements_review_inspection_walkthrough/), 프로덕션 준비성 검토): [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 [SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 운영 기준에 맞는지 검토하는 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 프로세스.

| PRR 항목        | 점검 내용                          |
|-----------------|-------------------------------------|
| [SLI](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/)/[SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) 정의    | 지표와 목표가 명확한가              |
| 알림 설계       | Actionable Alert만 구성됐는가       |
| 런북(Runbook)   | 장애 대응 절차가 문서화됐는가       |
| 자동 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)       | 배포 실패 시 자동 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 되는가     |

> 📢 **Ⅳ 섹션 요약 비유**
> PRR은 비행기 이륙 전 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) — 모든 항목을 통과해야 운항(배포)이 허가된다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소              | 역할                                     |
|------------------------|------------------------------------------|
| [SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/)                    | [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 엔지니어링 방법론                  |
| [SLI](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) / [SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) / [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/)        | [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 측정·목표·계약 지표 계층          |
| [Error Budget](/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/)           | 허용 가능한 다운타임 예산                |
| [Toil](/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)                   | 자동화 대상 반복 수동 운영 업무          |
| [Blameless Postmortem](/studynote/15_devops_sre/03_sre_observability/128_blameless_postmortem/)   | 무비난 장애 회고 문화                    |
| On-[call](/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/)                | 장애 대응 당직 체계                      |
| PRR                    | 프로덕션 진입 검토 프로세스              |

### 관련 키워드 및 발전 흐름도

```
SRE
    +-- SLI/SLO/SLA -> 신뢰성 정량화
    +-- Error Budget -> 혁신-안정성 균형
    +-- Toil 자동화 -> 운영 부담 50% 이하
    +-- Blameless Postmortem -> 장애 학습 문화
    +-- PRR / Capacity Planning -> 서비스 출시 품질 보증
```

> 🧒 **어린이 비유**
> SRE는 놀이공원 안전 관리자예요. 고장 나도 괜찮은 시간([Error Budget](/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/))을 미리 정해두고, 그 이상 고장나면 새로운 놀이기구 도입을 잠깐 멈추는 규칙을 지켜요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 316 / 373

<- **이전**: [Helm Package Manager](/studynote/15_devops_sre/05_devsecops/315_process/)
**다음**: [SLI SLO SLA Error Budget](/studynote/15_devops_sre/05_devsecops/317_sli_slo_sla/) ->

---
