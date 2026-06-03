---
title: 115. Atlantis Terraform CI - PR 기반 IaC 자동 Plan·Apply 워크플로
date: '2026-04-19'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Atlantis는 [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]]/OpenTofu의 **[[067_pull_request_pr_merge_request_code_review|PR]]([[067_pull_request_pr_merge_request_code_review|Pull Request]]) 기반 자동 Plan/Apply 워크플로**를 제공하는 [[191_oss_license_compliance|OSS]] 도구로, PR을 열면 자동으로 `terraform plan` 결과를 코멘트로 달고, 승인 후 `atlantis apply`로 적용한다.
> 2. **가치**: 개발자가 로컬에서 `terraform apply`를 실행하면 [[272_state_pattern|State]] 충돌·[[606_auditing_linux_auditd|감사]] 불가·리뷰 없는 변경이 발생하지만, Atlantis는 **모든 인프라 변경을 [[067_pull_request_pr_merge_request_code_review|PR]] 리뷰 프로세스**에 통합하여 IaC의 GitOps를 실현한다.
> 3. **판단 포인트**: Atlantis는 자체 호스팅(GitHub/GitLab [[498_webhook_rest_api_reverse_callback|Webhook]] 연동)이 필요하며, [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] Cloud/Spacelift 같은 [[309_saas|SaaS]] 대안과 비교하여 **비용 0 + 완전 제어**가 장점이다.

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

- **📢 섹션 요약 비유**: Atlantis는 인프라 변경의 **4-eyes 원칙(이중 [[396_validation|확인]])**을 자동화한 것이다. 혼자 몰래 서버를 바꿀 수 없고, 반드시 [[067_pull_request_pr_merge_request_code_review|PR]] 리뷰를 거쳐야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Atlantis 핵심 기능

| 기능 | 설명 |
|:---|:---|
| **Auto Plan** | [[067_pull_request_pr_merge_request_code_review|PR]] [[087_process_state_transition|생성]] 시 자동 plan 실행 |
| **[[067_pull_request_pr_merge_request_code_review|PR]] Comment** | Plan 결과를 [[067_pull_request_pr_merge_request_code_review|PR]] 코멘트로 표시 |
| **[[213_locking_mechanism_concurrency_control|Locking]]** | 동일 [[506_directory_structure_symbol_table|디렉터리]] 동시 변경 방지 |
| **Apply Require** | [[067_pull_request_pr_merge_request_code_review|PR]] Approve 후에만 apply 허용 |
| **Custom Workflow** | pre-plan/post-apply 훅 지원 |

### Atlantis vs [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] Cloud

| 비교 | Atlantis | [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] Cloud |
|:---|:---|:---|
| **호스팅** | 자체 ([[063_docker_architecture|Docker]]) | **[[309_saas|SaaS]]** |
| **비용** | 무료 | 유료 |
| **제어** | **완전** | HashiCorp 의존 |
| **[[272_state_pattern|State]]** | 별도 관리 (S3) | 내장 |
| **Sentinel** | ✗ | ✅ ([[164_policy|정책]]) |

- **📢 섹션 요약 비유**: Atlantis는 자가용(직접 관리, 비용 0)이고, [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] Cloud는 택시(편리하지만 비용 있음)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 로컬 apply | Atlantis | [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] Cloud |
|:---|:---|:---|:---|
| **리뷰** | 없음 | **[[067_pull_request_pr_merge_request_code_review|PR]] 필수** | [[067_pull_request_pr_merge_request_code_review|PR]] 필수 |
| **[[606_auditing_linux_auditd|감사]]** | 불가 | **Git 이력** | 내장 |
| **[[272_state_pattern|State]] 충돌** | 빈번 | **Lock으로 방지** | 내장 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 배포 [[435_checklist_based_testing|체크리스트]]
1. Atlantis 서버를 K8s/Docker에 배포.
2. GitHub/GitLab [[498_webhook_rest_api_reverse_callback|Webhook]] 연결.
3. `atlantis.yaml`에 프로젝트 [[506_directory_structure_symbol_table|디렉터리]]·워크플로 정의.
4. [[067_pull_request_pr_merge_request_code_review|PR]] Approve → `atlantis apply` 코멘트로 적용.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 로컬 apply | Atlantis | 개선 |
|:---|:---|:---|:---|
| 인프라 변경 [[606_auditing_linux_auditd|감사]] | 불가 | **[[067_pull_request_pr_merge_request_code_review|PR]] 이력** | 100% |
| [[272_state_pattern|State]] 충돌 | 빈번 | **[[510_lock|Lock]]** | 0건 |
| 비용 | - | **무료** | [[309_saas|SaaS]] 대비 절감 |

Atlantis는 [[119_gitops_single_source_of_truth|GitOps]] + Terraform의 가장 실용적인 조합이며, [[067_pull_request_pr_merge_request_code_review|PR]] 리뷰 문화가 정착된 팀에서 인프라 거버넌스를 비용 없이 확보할 수 있는 최적의 도구다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]]** | Atlantis가 자동화하는 [[793_iac_idempotency_template|IaC]] 도구 |
| **[[119_gitops_single_source_of_truth|GitOps]]** | [[067_pull_request_pr_merge_request_code_review|PR]] 기반 인프라 관리 = [[793_iac_idempotency_template|IaC]] [[119_gitops_single_source_of_truth|GitOps]] |
| **[[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] Cloud** | [[309_saas|SaaS]] 경쟁 도구 |
| **Spacelift** | 또 다른 [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] [[090_configuration_item|CI]] [[309_saas|SaaS]] 대안 |
| **[[067_pull_request_pr_merge_request_code_review|PR]] [[153_requirements_review_inspection_walkthrough|Review]]** | Atlantis가 강제하는 변경 리뷰 프로세스 |

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
