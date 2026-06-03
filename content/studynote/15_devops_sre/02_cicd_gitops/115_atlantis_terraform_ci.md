+++
title = "115. Atlantis Terraform CI - PR 기반 IaC 자동 Plan·Apply 워크플로"
date = 2026-04-19

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Atlantis는 [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)/OpenTofu의 **[PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)([Pull Request](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)) 기반 자동 Plan/Apply 워크플로**를 제공하는 [OSS](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 도구로, PR을 열면 자동으로 `terraform plan` 결과를 코멘트로 달고, 승인 후 `atlantis apply`로 적용한다.
> 2. **가치**: 개발자가 로컬에서 `terraform apply`를 실행하면 [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 충돌·[감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 불가·리뷰 없는 변경이 발생하지만, Atlantis는 **모든 인프라 변경을 [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 리뷰 프로세스**에 통합하여 IaC의 GitOps를 실현한다.
> 3. **판단 포인트**: Atlantis는 자체 호스팅(GitHub/GitLab [Webhook](/knowledge-base/studynote/03_network/09_application_layer_web_email/498_webhook_rest_api_reverse_callback/) 연동)이 필요하며, [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) Cloud/Spacelift 같은 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 대안과 비교하여 **비용 0 + 완전 제어**가 장점이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Atlantis PR 기반 워크플로                           │
├───────────────────────────────────────────────────────┤
│  1. 개발자: main.tf 수정 → PR 생성                   │
│  2. Atlantis Bot: 자동 terraform plan 실행            │
│     → PR 코멘트에 Plan 결과 표시                      │
│     "1 to add, 0 to change, 0 to destroy"            │
│  3. 리뷰어: Plan 결과 확인 → Approve                 │
│  4. 개발자: "atlantis apply" 코멘트                   │
│  5. Atlantis Bot: terraform apply 실행                │
│     → 성공 결과 코멘트 + PR 머지                      │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Atlantis는 인프라 변경의 **4-eyes 원칙(이중 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/))**을 자동화한 것이다. 혼자 몰래 서버를 바꿀 수 없고, 반드시 [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 리뷰를 거쳐야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Atlantis 핵심 기능

| 기능 | 설명 |
|:---|:---|
| **Auto Plan** | [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시 자동 plan 실행 |
| **[PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) Comment** | Plan 결과를 [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 코멘트로 표시 |
| **[Locking](/knowledge-base/studynote/05_database/04_transactions_concurrency/213_locking_mechanism_concurrency_control/)** | 동일 [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 동시 변경 방지 |
| **Apply Require** | [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) Approve 후에만 apply 허용 |
| **Custom Workflow** | pre-plan/post-apply 훅 지원 |

### Atlantis vs [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) Cloud

| 비교 | Atlantis | [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) Cloud |
|:---|:---|:---|
| **호스팅** | 자체 ([Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)) | **[SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/)** |
| **비용** | 무료 | 유료 |
| **제어** | **완전** | HashiCorp 의존 |
| **[State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)** | 별도 관리 (S3) | 내장 |
| **Sentinel** | ✗ | ✅ ([정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)) |

- **📢 섹션 요약 비유**: Atlantis는 자가용(직접 관리, 비용 0)이고, [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) Cloud는 택시(편리하지만 비용 있음)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 로컬 apply | Atlantis | [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) Cloud |
|:---|:---|:---|:---|
| **리뷰** | 없음 | **[PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 필수** | [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 필수 |
| **[감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)** | 불가 | **Git 이력** | 내장 |
| **[State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 충돌** | 빈번 | **Lock으로 방지** | 내장 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 배포 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. Atlantis 서버를 K8s/Docker에 배포.
2. GitHub/GitLab [Webhook](/knowledge-base/studynote/03_network/09_application_layer_web_email/498_webhook_rest_api_reverse_callback/) 연결.
3. `atlantis.yaml`에 프로젝트 [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)·워크플로 정의.
4. [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) Approve → `atlantis apply` 코멘트로 적용.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 로컬 apply | Atlantis | 개선 |
|:---|:---|:---|:---|
| 인프라 변경 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) | 불가 | **[PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 이력** | 100% |
| [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 충돌 | 빈번 | **[Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)** | 0건 |
| 비용 | - | **무료** | [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 대비 절감 |

Atlantis는 [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) + Terraform의 가장 실용적인 조합이며, [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 리뷰 문화가 정착된 팀에서 인프라 거버넌스를 비용 없이 확보할 수 있는 최적의 도구다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)** | Atlantis가 자동화하는 [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 도구 |
| **[GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/)** | [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 기반 인프라 관리 = [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) |
| **[Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) Cloud** | [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 경쟁 도구 |
| **Spacelift** | 또 다른 [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 대안 |
| **[PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) [Review](/knowledge-base/studynote/04_software_engineering/03_design_architecture/153_requirements_review_inspection_walkthrough/)** | Atlantis가 강제하는 변경 리뷰 프로세스 |

### 📈 관련 키워드 및 발전 흐름도

```text
[로컬 terraform apply (2014~) — 개인 실행, 감사 불가]
    │
    ▼
[Atlantis (2017, Hootsuite) — PR 기반 자동 Plan/Apply]
    │
    ▼
[Terraform Cloud (2019~) — HashiCorp SaaS]
    │
    ▼
[Spacelift / env0 (2020~) — IaC CI SaaS 경쟁]
    │
    ▼
[현재: Atlantis + OPA/Conftest — 정책 검증 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 옛날에는 레고(인프라)를 **혼자 몰래 바꿀 수** 있었어요 → 실수해도 아무도 몰라요.
2. Atlantis는 레고를 바꾸기 전에 **친구(리뷰어)한테 보여주고** "이래도 될까?"라고 물어봐야 해요.
3. 친구가 "좋아!"라고 하면 로봇이 자동으로 바꿔주고, **기록도 다 남아서** 안전해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 115 / 373

← **이전**: [114. Kayenta 카나리 분석 (Kayenta Canary Analysis) - 자동 배포 판단·ACA](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/114_kayenta_canary_analysis/)
**다음**: [116. 인프라 드리프트 감지 (Infrastructure Drift Detection) - IaC 상태 불일치 자동 탐지](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/116_infrastructure_drift_detection/) →

---
