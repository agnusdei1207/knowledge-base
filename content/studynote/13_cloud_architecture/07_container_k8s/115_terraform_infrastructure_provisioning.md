---
title: "115. Terraform Infrastructure Provisioning"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Terraform은 HashiCorp가 개발한 <strong>선언적 <a href="/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/">IaC</a>(<a href="/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/">Infrastructure as Code</a>)</strong> 도구로, HCL(HashiCorp Configuration Language)로 인프라를 정의하면 `terraform apply`로 AWS·Azure·GCP 등 <strong>다중 클라우드에 자동 <a href="/studynote/09_security/11_iam_access_control/528_provisioning/">프로비저닝</a></strong>한다.
> 2. **가치**: AWS 콘솔 클릭으로 인프라를 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하면 재현 불가·추적 불가·리뷰 불가이지만, Terraform은 인프라를 <strong>코드로 Git에 관리</strong>하여 변경 이력·[코드 리뷰](/studynote/04_software_engineering/06_software_architecture/330_code_review/)·자동 배포가 가능하다.
> 3. **판단 포인트**: [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 관리(원격 백엔드 S3+[DynamoDB](/studynote/05_database/04_transactions_concurrency/545_dynamodb/) [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/))·[모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 재사용·Plan/Apply 분리가 [Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) 운영의 핵심이며, OpenTofu([OSS](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) Fork)와의 라이선스 관계를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Terraform 워크플로                                  |
+-------------------------------------------------------+
|  1. Write: main.tf에 인프라 선언                      |
|     resource "aws_instance" "web" {                   |
|       ami           = "ami-xxx"                       |
|       instance_type = "t3.micro"                      |
|     }                                                 |
|  2. Plan: terraform plan -> 변경 사항 미리 확인        |
|     + aws_instance.web will be created                |
|  3. Apply: terraform apply -> 실제 생성                |
|  4. State: terraform.tfstate에 현재 상태 기록         |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Terraform은 건축 설계도(HCL)를 주면 로봇([Provider](/studynote/07_enterprise_systems/03_eai_esb_msa/150_soa_triangle_architecture/))이 자동으로 건물(인프라)을 짓는 시스템이다. Plan은 시뮬레이션, Apply는 실제 시공.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 핵심 개념

| 개념 | 설명 |
|:---|:---|
| <strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/150_soa_triangle_architecture/">Provider</a></strong> | AWS/Azure/GCP 등 클라우드 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 연결 플러그인 |
| **Resource** | [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)할 인프라 단위 (EC2, [VPC](/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/), RDS 등) |
| <strong><a href="/studynote/04_software_engineering/04_testing_quality/192_module_independence/">Module</a></strong> | 재사용 가능한 리소스 묶음 |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/">State</a></strong> | 현재 인프라 상태 기록 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) |
| **Plan/Apply** | 변경 미리보기 -> 실제 적용 2단계 |

### [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 관리 [Best Practice](/studynote/07_enterprise_systems/02_erp_systems/087_erp_package_advantages_best_practice/)

| 방식 | 적합 | 위험 |
|:---|:---|:---|
| 로컬 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | 개인 프로젝트 | 팀 충돌, 유실 |
| <strong>S3 + <a href="/studynote/05_database/04_transactions_concurrency/545_dynamodb/">DynamoDB</a> <a href="/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a></strong> | **프로덕션** | 없음 (표준) |
| [Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) Cloud | [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 선호 팀 | 비용 |

- **📢 섹션 요약 비유**: State는 건축 대장(현재 건물 상태 기록)이다. 대장을 잃어버리면 Terraform이 "이 건물이 내가 지은 건지 모르겠다"며 혼란에 빠진다.

---

## Ⅲ. 비교 및 연결

| 비교 | [Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) | CloudFormation | Pulumi |
|:---|:---|:---|:---|
| **클라우드** | **멀티** | AWS 전용 | 멀티 |
| **언어** | HCL | YAML/[JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) | TypeScript/Python |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/">State</a></strong> | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 기반 | AWS 관리 | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)/[SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) |
| **라이선스** | BSL (1.6+) | 무료 | Apache 2.0 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 구조 예시
```
infra/
+-- modules/
|   +-- vpc/
|   +-- eks/
|   +-- rds/
+-- environments/
|   +-- dev/
|   +-- staging/
|   +-- prod/
```

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/">State</a> 로컬 보관 + 팀 작업</strong>: 동시 수정 시 [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 충돌 -> S3 원격 백엔드 필수.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 콘솔 수동 | [Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) | 개선 |
|:---|:---|:---|:---|
| 인프라 재현성 | 불가 | **100%** | 코드로 보장 |
| 변경 추적 | 불가 | **Git 이력** | [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 가능 |
| [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/) | 시간 단위 | **분 단위** | 자동화 |

Terraform은 OpenTofu([OSS](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) Fork)와의 생태계 분화가 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중이며, [Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) CDK(TypeScript/Python으로 HCL [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/))로 프로그래밍 언어 생태계와 통합되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/">IaC</a></strong> | Terraform이 구현하는 인프라 코드화 패러다임 |
| **HCL** | Terraform의 선언적 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 언어 |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/">State</a></strong> | 현재 인프라 상태 추적 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) |
| <strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/150_soa_triangle_architecture/">Provider</a></strong> | 클라우드 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 플러그인 생태계 |
| **OpenTofu** | Terraform의 [OSS](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) Fork (라이선스 분화) |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 콘솔 인프라 관리 (2010s)]
    |
    v
[Terraform 0.x (2014, HashiCorp) — 멀티클라우드 IaC]
    |
    v
[Terraform Module Registry (2017~) — 재사용 모듈 생태계]
    |
    v
[BSL 라이선스 전환 (2023) -> OpenTofu Fork]
    |
    v
[현재: Terraform CDK + AI 인프라 자동 생성]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 옛날에는 레고(인프라)를 **설명서 없이 손으로** 만들어서, 같은 걸 다시 만들 수 없었어요.
2. Terraform은 <strong>레고 설명서(코드)</strong>를 쓰면 로봇이 자동으로 조립해줘요!
3. 설명서를 Git에 보관하니까, 누가 언제 무엇을 바꿨는지 **기록이 다 남아서** 안전해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 114 / 371

<- **이전**: [114. Argo CD (ArgoCD GitOps CD) - K8s 선언적 지속 배포·Git 단일 진실 원천](/studynote/13_cloud_architecture/07_container_k8s/114_argocd_gitops_cd/)
**다음**: [116. 컨테이너 이미지 보안 스캐닝 (Container Image Security Scanning) - CVE·SBOM·정책](/studynote/13_cloud_architecture/07_container_k8s/116_kubernetes_container_image_security_scanning/) ->

---
