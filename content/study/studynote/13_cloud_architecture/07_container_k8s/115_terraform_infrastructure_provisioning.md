+++
weight = 115
title = "115. Terraform 인프라 프로비저닝 - IaC 선언적 다중 클라우드 관리"
date = "2026-04-19"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Terraform은 HashiCorp가 개발한 **선언적 [[793_iac_idempotency_template|IaC]]([[062_infrastructure_as_code|Infrastructure as Code]])** 도구로, HCL(HashiCorp Configuration Language)로 인프라를 정의하면 `terraform apply`로 AWS·Azure·GCP 등 **다중 클라우드에 자동 [[528_provisioning|프로비저닝]]**한다.
> 2. **가치**: AWS 콘솔 클릭으로 인프라를 [[087_process_state_transition|생성]]하면 재현 불가·추적 불가·리뷰 불가이지만, Terraform은 인프라를 **코드로 Git에 관리**하여 변경 이력·[[330_code_review|코드 리뷰]]·자동 배포가 가능하다.
> 3. **판단 포인트**: [[272_state_pattern|State]] [[501_file_definition_logical_record|파일]] 관리(원격 백엔드 S3+[[545_dynamodb|DynamoDB]] [[510_lock|Lock]])·[[192_module_independence|모듈]] 재사용·Plan/Apply 분리가 [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] 운영의 핵심이며, OpenTofu([[191_oss_license_compliance|OSS]] Fork)와의 라이선스 관계를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Terraform 워크플로                                  │
├───────────────────────────────────────────────────────┤
│  1. Write: main.tf에 인프라 선언                      │
│     resource "aws_instance" "web" {                   │
│       ami           = "ami-xxx"                       │
│       instance_type = "t3.micro"                      │
│     }                                                 │
│  2. Plan: terraform plan → 변경 사항 미리 확인        │
│     + aws_instance.web will be created                │
│  3. Apply: terraform apply → 실제 생성                │
│  4. State: terraform.tfstate에 현재 상태 기록         │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Terraform은 건축 설계도(HCL)를 주면 로봇([[150_soa_triangle_architecture|Provider]])이 자동으로 건물(인프라)을 짓는 시스템이다. Plan은 시뮬레이션, Apply는 실제 시공.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 핵심 개념

| 개념 | 설명 |
|:---|:---|
| **[[150_soa_triangle_architecture|Provider]]** | AWS/Azure/GCP 등 클라우드 [[014_api_posix|API]] 연결 플러그인 |
| **Resource** | [[087_process_state_transition|생성]]할 인프라 단위 (EC2, [[836_vpc_virtual_private_cloud_subnet_isolation|VPC]], RDS 등) |
| **[[192_module_independence|Module]]** | 재사용 가능한 리소스 묶음 |
| **[[272_state_pattern|State]]** | 현재 인프라 상태 기록 [[501_file_definition_logical_record|파일]] |
| **Plan/Apply** | 변경 미리보기 → 실제 적용 2단계 |

### [[272_state_pattern|State]] 관리 [[087_erp_package_advantages_best_practice|Best Practice]]

| 방식 | 적합 | 위험 |
|:---|:---|:---|
| 로컬 [[501_file_definition_logical_record|파일]] | 개인 프로젝트 | 팀 충돌, 유실 |
| **S3 + [[545_dynamodb|DynamoDB]] [[510_lock|Lock]]** | **프로덕션** | 없음 (표준) |
| [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] Cloud | [[309_saas|SaaS]] 선호 팀 | 비용 |

- **📢 섹션 요약 비유**: State는 건축 대장(현재 건물 상태 기록)이다. 대장을 잃어버리면 Terraform이 "이 건물이 내가 지은 건지 모르겠다"며 혼란에 빠진다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] | CloudFormation | Pulumi |
|:---|:---|:---|:---|
| **클라우드** | **멀티** | AWS 전용 | 멀티 |
| **언어** | HCL | YAML/[[343_json|JSON]] | TypeScript/Python |
| **[[272_state_pattern|State]]** | [[501_file_definition_logical_record|파일]] 기반 | AWS 관리 | [[501_file_definition_logical_record|파일]]/[[309_saas|SaaS]] |
| **라이선스** | BSL (1.6+) | 무료 | Apache 2.0 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[192_module_independence|모듈]] 구조 예시
```
infra/
├── modules/
│   ├── vpc/
│   ├── eks/
│   └── rds/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
```

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **[[272_state_pattern|State]] 로컬 보관 + 팀 작업**: 동시 수정 시 [[272_state_pattern|State]] 충돌 → S3 원격 백엔드 필수.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 콘솔 수동 | [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] | 개선 |
|:---|:---|:---|:---|
| 인프라 재현성 | 불가 | **100%** | 코드로 보장 |
| 변경 추적 | 불가 | **Git 이력** | [[606_auditing_linux_auditd|감사]] 가능 |
| [[528_provisioning|프로비저닝]] | 시간 단위 | **분 단위** | 자동화 |

Terraform은 OpenTofu([[191_oss_license_compliance|OSS]] Fork)와의 생태계 분화가 [[216_progress_in_synchronization|진행]] 중이며, [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] CDK(TypeScript/Python으로 HCL [[087_process_state_transition|생성]])로 프로그래밍 언어 생태계와 통합되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[793_iac_idempotency_template|IaC]]** | Terraform이 구현하는 인프라 코드화 패러다임 |
| **HCL** | Terraform의 선언적 [[009_config|설정]] 언어 |
| **[[272_state_pattern|State]]** | 현재 인프라 상태 추적 [[501_file_definition_logical_record|파일]] |
| **[[150_soa_triangle_architecture|Provider]]** | 클라우드 [[014_api_posix|API]] 플러그인 생태계 |
| **OpenTofu** | Terraform의 [[191_oss_license_compliance|OSS]] Fork (라이선스 분화) |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 콘솔 인프라 관리 (2010s)]
    │
    ▼
[Terraform 0.x (2014, HashiCorp) — 멀티클라우드 IaC]
    │
    ▼
[Terraform Module Registry (2017~) — 재사용 모듈 생태계]
    │
    ▼
[BSL 라이선스 전환 (2023) → OpenTofu Fork]
    │
    ▼
[현재: Terraform CDK + AI 인프라 자동 생성]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 옛날에는 레고(인프라)를 **설명서 없이 손으로** 만들어서, 같은 걸 다시 만들 수 없었어요.
2. Terraform은 **레고 설명서(코드)**를 쓰면 로봇이 자동으로 조립해줘요!
3. 설명서를 Git에 보관하니까, 누가 언제 무엇을 바꿨는지 **기록이 다 남아서** 안전해요!
