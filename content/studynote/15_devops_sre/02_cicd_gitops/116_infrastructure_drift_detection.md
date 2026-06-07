---
title: "116. Infrastructure Drift Detection"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 116
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인프라 드리프트(Drift)란 <strong><a href="/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/">IaC</a> 코드(<a href="/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/">Terraform</a>/CloudFormation)에 정의된 기대 상태와 실제 클라우드 인프라 상태가 불일치</strong>하는 현상이며, Drift Detection은 이를 자동으로 탐지·알림·복원하는 프로세스다.
> 2. **가치**: 운영자가 콘솔에서 수동 변경(보안 그룹 열기, 인스턴스 타입 변경)하면 [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 코드와 실제가 달라져 **"코드가 진실이 아니게"** 되며, 이후 `terraform apply` 시 예기치 않은 변경이 발생한다.
> 3. **판단 포인트**: `terraform plan`을 주기적으로 실행하여 Diff를 감지하거나, <strong>Driftctl·AWS CloudFormation Drift <a href="/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/">Detection</a>·Spacelift</strong>로 자동화한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    드리프트 발생 시나리오                              |
+-------------------------------------------------------+
|  1. Terraform: security_group = [22, 443]            |
|  2. 운영자: AWS 콘솔에서 8080 포트 수동 추가 ⚠️      |
|  3. 실제 상태: [22, 443, 8080]                        |
|     Terraform 코드: [22, 443]                         |
|     -> 드리프트 발생!                                  |
|  4. terraform apply 실행 시:                          |
|     8080이 코드에 없으므로 삭제됨 -> 서비스 장애!     |
|                                                       |
|  해결: 주기적 terraform plan으로 Diff 감지            |
|     -> 코드 동기화 또는 수동 변경 되돌리기             |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 드리프트는 건축 대장([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/))과 실제 건물(인프라)이 다른 상태다. 건축 대장대로 리모델링하면 몰래 만든 방이 철거된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 드리프트 감지 도구

| 도구 | 방식 | 특징 |
|:---|:---|:---|
| <strong><a href="/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/">terraform</a> plan</strong> | [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) vs 실제 비교 | 기본, 수동/크론 실행 |
| **Driftctl** | [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 미관리 리소스 탐지 | [OSS](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), 커버리지 높음 |
| **CloudFormation Drift** | CF [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) vs 실제 비교 | AWS 네이티브 |
| **Spacelift** | 자동 드리프트 스캔 + 알림 | [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) |

### 드리프트 대응 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 설명 |
|:---|:---|
| **Reconcile** | [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 코드를 실제 상태에 맞춰 수정 (코드 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)) |
| **Remediate** | 실제 상태를 [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 코드에 맞춰 복원 (자동 적용) |
| **Alert** | 드리프트 감지 시 알림만 (수동 판단) |

- **📢 섹션 요약 비유**: Reconcile은 "몰래 만든 방을 대장에 추가"하는 것이고, Remediate는 "몰래 만든 방을 철거"하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 드리프트 미감지 | 주기적 Plan | 자동 감지+복원 |
|:---|:---|:---|:---|
| **코드 신뢰** | ✗ | 수동 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | **100%** |
| **사고 위험** | 높음 | 중간 | **낮음** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 자동화 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인
```yaml
# GitHub Actions: 매일 드리프트 스캔
schedule:
  - cron: '0 9 * * *'
steps:
  - run: terraform plan -detailed-exitcode
  # exit code 2 = drift detected -> Slack 알림
```

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **콘솔 수동 변경 허용**: [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) [GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 원칙 파괴. 콘솔 변경 시 반드시 [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 코드에 반영.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 드리프트 미감지 | 드리프트 감지 | 개선 |
|:---|:---|:---|:---|
| [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 코드 [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) | 불확실 | **100%** | 단일 진실 원천 |
| 예기치 않은 변경 | 빈번 | **즉시 감지** | 사고 예방 |

드리프트 감지는 [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) GitOps의 <strong>필수 보완 장치</strong>이며, [OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/)([Open Policy Agent](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/))와 결합하여 드리프트 유형별 자동 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)(허용/거부/알림)을 적용하는 방향으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/">IaC</a> (<a href="/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/">Terraform</a>)</strong> | 드리프트가 발생하는 [인프라 코드](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) |
| <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a></strong> | 코드 = 진실이라는 원칙, 드리프트가 위반하는 대상 |
| **Driftctl** | [OSS](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 드리프트 감지 도구 |
| <strong><a href="/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/">terraform</a> plan</strong> | 기본적인 드리프트 감지 명령 |
| <strong><a href="/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/">OPA</a></strong> | 드리프트 대응 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 자동화 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 인프라 관리 (콘솔 변경 빈번)]
    |
    v
[IaC 도입 (2014~) — 코드로 인프라 관리]
    |
    v
[드리프트 문제 인식 (2018~) — 코드 vs 실제 불일치]
    |
    v
[Driftctl / CF Drift Detection (2020~) — 자동 감지]
    |
    v
[현재: 자동 Remediation — 드리프트 감지->자동 복원]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 설계도([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/))에는 <strong>방 3개</strong>라고 써있는데, 누군가 몰래 **방 1개를 더 만들었어요** (드리프트).
2. 나중에 설계도대로 리모델링하면 **몰래 만든 방이 없어져서** 사고가 나요.
3. 드리프트 감지는 매일 설계도와 실제 건물을 **비교해서 다른 점을 찾아주는** 검사원이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 116 / 373

<- **이전**: [115. Atlantis Terraform CI - PR 기반 IaC 자동 Plan·Apply 워크플로](/studynote/15_devops_sre/02_cicd_gitops/115_atlantis_terraform_ci/)
**다음**: [117. TextOps/DocOps 자동화 - 문서 파이프라인 CI/CD·Docs-as-Code](/studynote/15_devops_sre/02_cicd_gitops/117_textops_docops_automation/) ->

---
