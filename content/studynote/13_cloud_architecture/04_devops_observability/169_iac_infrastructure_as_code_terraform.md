---
title: 169. 인프라스트럭처 애즈 코드 (IaC, Infrastructure as Code)
date: '2026-04-21'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[793_iac_idempotency_template|IaC]]([[062_infrastructure_as_code|Infrastructure as Code]])는 [[598_vm_migration_nic|VM]], 네트워크, [[002_database_definition|데이터베이스]] 같은 인프라를 손으로 콘솔에서 클릭하는 대신 코드 [[501_file_definition_logical_record|파일]]로 정의하고 [[288_version_ihl_tos_total_length|버전]] 관리하는 방식이다.
> 2. **가치**: 인프라 변경 이력이 Git에 남아 [[606_auditing_linux_auditd|감사]]·롤백이 가능해지고, 동일 환경을 수십 번 반복 재현할 수 있어 "눈송이 서버([[541_cassandra|Snowflake]] Server)" 문제를 근본적으로 해결한다.
> 3. **판단 포인트**: [[528_provisioning|프로비저닝]]([[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]])과 [[089_configuration_management|구성 관리]]([[198_ansible_os_configuration_management_ssh|Ansible]])는 역할이 다르며, 두 도구를 조합하는 것이 실무 표준이다.

---

## Ⅰ. 개요 및 필요성

클라우드 이전 시대에는 인프라 변경이 서버실 담당자의 수동 작업으로 이루어졌다. 수개월에 걸쳐 조금씩 수정된 서버는 "눈송이([[541_cassandra|Snowflake]])"처럼 다른 서버와 조금씩 다른 유일한 존재가 되어 장애 재현이 불가능하고 확장이 어려워진다. IaC는 이 문제를 코드화로 해결한다.

[[195_terraform_hashicorp_agnostic_aws_gcp|테라폼]]([[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]])은 HashiCorp가 개발한 대표적인 선언형 [[793_iac_idempotency_template|IaC]] 도구다. HCL(HashiCorp Configuration Language)로 클라우드 리소스를 정의하면 `terraform apply` 한 번으로 AWS, Azure, GCP 등 [[202_multi_cloud_hybrid_cloud_governance|멀티 클라우드]] 인프라를 동시 [[528_provisioning|프로비저닝]]할 수 있다. [[198_ansible_os_configuration_management_ssh|앤서블]]([[198_ansible_os_configuration_management_ssh|Ansible]])은 [[528_provisioning|프로비저닝]]보다는 이미 생성된 서버의 소프트웨어 설치·설정을 코드화하는 데 강점이 있다.

IaC의 핵심 가치는 인프라의 "재현 가능성"과 "검토 가능성"이다. 인프라 변경이 Pull Request를 통해 코드 리뷰를 받고 승인된 후 적용되므로, 운영 실수가 사전에 차단된다.

📢 **섹션 요약 비유**: IaC는 건물 설계 도면이다. 도면 없이 지은 건물은 수리할 때마다 어디에 파이프가 있는지 몰라 힘들지만, 도면이 있으면 어디서나 똑같은 건물을 다시 지을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] 동작 흐름

```
.tf 파일 작성       terraform plan        terraform apply
(HCL 코드)   →   (변경 계획 미리보기)  →  (실제 인프라 생성·변경)
     ↓                   ↓                       ↓
  Git 저장소        콘솔에 변경 diff        terraform.tfstate
  (버전 관리)        출력, 검토 가능         (현재 상태 기록)
```

| 개념 | 설명 |
|:---|:---|
| 선언형([[219_declarative_yaml|Declarative]]) | 최종 원하는 상태를 기술. 도달 방법은 도구가 결정 |
| [[171_idempotency_iac_terraform|멱등성]]([[194_idempotency|Idempotency]]) | 동일 코드를 반복 실행해도 결과 상태 동일 |
| [[272_state_pattern|State]] [[501_file_definition_logical_record|파일]] | 현재 인프라 상태를 JSON으로 기록한 `.tfstate` |
| [[150_soa_triangle_architecture|Provider]] | AWS, GCP, Azure 등 클라우드별 [[014_api_posix|API]] [[259_adapter_pattern_interface_wrapper|어댑터]] |
| [[192_module_independence|Module]] | 재사용 가능한 [[793_iac_idempotency_template|IaC]] 코드 단위 |
| Remote Backend | [[272_state_pattern|State]] [[501_file_definition_logical_record|파일]]을 S3, GCS에 저장해 팀 협업 지원 |

📢 **섹션 요약 비유**: Terraform의 [[272_state_pattern|State]] [[501_file_definition_logical_record|파일]]은 집의 현재 상태를 찍은 사진이고, .tf 코드는 앞으로 만들 집의 설계 도면이다. 두 가지를 비교해서 무엇이 달라야 하는지 plan이 알려준다.

---

## Ⅲ. 비교 및 연결

### [[793_iac_idempotency_template|IaC]] 도구 비교

| 도구 | 주요 용도 | 방식 | 언어 | 특징 |
|:---|:---|:---|:---|:---|
| [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] | 인프라 [[528_provisioning|프로비저닝]] | 선언형 | HCL | [[202_multi_cloud_hybrid_cloud_governance|멀티 클라우드]], [[272_state_pattern|State]] 관리 |
| [[198_ansible_os_configuration_management_ssh|Ansible]] | [[089_configuration_management|구성 관리]]·배포 | 선언형(주) | YAML | 에이전트리스, [[538_ssh_vs_telnet_secure_remote|SSH]] |
| Pulumi | 인프라 [[528_provisioning|프로비저닝]] | 선언형 | Python/TS | 범용 언어 사용 가능 |
| CloudFormation | AWS 전용 [[528_provisioning|프로비저닝]] | 선언형 | YAML/[[343_json|JSON]] | AWS 네이티브 |
| Chef/Puppet | [[089_configuration_management|구성 관리]] | 선언형 | Ruby DSL | 에이전트 필요 |

**선언형 vs 명령형**:
- 선언형: `resource "aws_instance" "web" { instance_type = "t3.micro" }` → 결과 정의
- 명령형: `aws ec2 run-instances --instance-type t3.micro` → 행동 나열

📢 **섹션 요약 비유**: 선언형은 "피자 도우를 얇게 해주세요"라고 결과를 말하는 것이고, 명령형은 "반죽을 밀대로 3번 밀고, 냉장고에 10분 넣고…"처럼 과정을 말하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] 워크플로 4단계:**
1. `terraform init` — [[150_soa_triangle_architecture|Provider]] 플러그인 다운로드
2. `terraform plan` — 변경 사항 미리 [[396_validation|확인]] (diff 출력)
3. `terraform apply` — 실제 인프라 변경 수행
4. `terraform destroy` — 인프라 전체 삭제

**팀 협업 [[087_erp_package_advantages_best_practice|Best Practice]]:**
- Remote Backend(S3 + [[545_dynamodb|DynamoDB]] 잠금): [[272_state_pattern|State]] [[501_file_definition_logical_record|파일]] 공유 및 동시 수정 방지
- [[067_pull_request_pr_merge_request_code_review|PR]] 기반 검토: `terraform plan` 결과를 [[067_pull_request_pr_merge_request_code_review|PR]] 코멘트에 자동 게시
- Terragrunt: 대규모 환경에서 [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] 코드 중복 제거

**실무 시나리오**: 서비스가 3개 환경(dev/stage/prod)을 가질 때, 환경별 변수만 달리하는 [[192_module_independence|모듈]] 구조로 동일 코드로 3개 환경을 관리한다. 실수로 prod를 삭제했을 때 `terraform apply` 한 번으로 5분 내 복원이 가능하다.

📢 **섹션 요약 비유**: Remote Backend의 [[545_dynamodb|DynamoDB]] 잠금은 여러 팀원이 동시에 같은 문서를 편집하지 못하게 막는 "편집 중 잠금" 기능과 같다.

---

## Ⅴ. 기대효과 및 결론

IaC를 도입하면 인프라 변경 리드타임이 주 단위에서 분 단위로 단축되고, 환경 간 차이([[066_gitlab_flow_environment_branch_strategy|Environment]] Drift)가 코드 수준에서 관리된다. 장애 [[658_ir_recovery|복구]] 시 동일 인프라를 분 단위로 재구성할 수 있어 [[176_rto_recovery_time_objective|RTO]]([[176_rto_recovery_time_objective|Recovery Time Objective]])가 획기적으로 줄어든다.

제약으로는 [[272_state_pattern|State]] [[501_file_definition_logical_record|파일]] 손상 또는 유실 시 인프라 상태 추적이 불가해지는 위험이 있으므로, [[272_state_pattern|State]] [[501_file_definition_logical_record|파일]]의 원격 저장 및 [[288_version_ihl_tos_total_length|버전]] 관리가 필수다. 또한 기존 수동 관리 인프라를 IaC로 가져오는 `terraform import` 작업은 상당한 [[459_quic_fec_forward_error_correction|초기]] 투자가 필요하다.

📢 **섹션 요약 비유**: IaC는 요리 레시피다. 레시피가 있으면 누구나 언제든 같은 맛의 음식을 만들 수 있고, 다음에 더 맛있게 개선하는 것도 "레시피 수정"으로 기록에 남길 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [[119_gitops_single_source_of_truth|GitOps]] | [[793_iac_idempotency_template|IaC]] 코드를 Git으로 관리하면 [[119_gitops_single_source_of_truth|GitOps]] 실현 |
| [[171_idempotency_iac_terraform|멱등성]] | [[793_iac_idempotency_template|IaC]] 반복 실행의 안전성 보장 원칙 |
| [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]] | IaC로 새 이미지 배포가 더 쉬워짐 |
| [[090_configuration_item|CI]]/CD | 파이프라인에서 [[195_terraform_hashicorp_agnostic_aws_gcp|terraform]] plan/apply 자동 실행 |
| [[193_configuration_drift|Configuration Drift]] | IaC로 코드와 실제 인프라 상태 일치 유지 |
| [[652_devops_calms_culture|DevOps]] | IaC는 개발-운영 협업의 핵심 도구 |

### 👶 어린이를 위한 3줄 비유 설명
1. IaC는 레고 조립 설명서예요. 설명서대로 하면 누구나 같은 레고 성을 만들 수 있어요.

### 📈 관련 키워드 및 발전 흐름도

```text
수동 콘솔 클릭 (재현 불가, 드리프트)
    │
    ▼
IaC: 인프라를 코드로 선언 (Terraform · Pulumi · CDK)
    ├─► terraform plan → apply → state 관리
    └─► 버전 관리: Git + PR 리뷰 + CI 검증
    │
    ▼
Policy as Code (OPA · Sentinel) → GitOps 연동
```
2. 예전에는 손으로 하나하나 클릭해서 서버를 만들었지만, 이제는 코드로 한 번에 뚝딱 만들어요.
3. 설명서(코드)가 있으면 실수로 성이 무너져도 똑같이 다시 만들 수 있어서 걱정이 없어요!
