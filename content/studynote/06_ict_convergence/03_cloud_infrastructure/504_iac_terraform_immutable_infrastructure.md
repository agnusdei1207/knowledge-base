---
title: "IaC Terraform Immutable Infrastructure"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)([Infrastructure as Code](/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/))는 인프라 구성을 코드로 선언하여 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리, 재현성, 자동화를 확보하는 방법론이며, Terraform은 그 사실상 표준 도구다.
> 2. **가치**: [불변 인프라](/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)([Immutable Infrastructure](/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/))는 서버를 수정하는 대신 새 이미지로 교체하여 [구성 편류](/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/)([Configuration Drift](/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/))를 근본적으로 차단한다.
> 3. **판단 포인트**: [GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 파이프라인에서 인프라 변경도 [PR](/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)/코드 리뷰를 거치게 하면, [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적([Audit Trail](/studynote/11_design_supervision/01_audit_framework/065_audit_trail_worm_storage_compliance/))과 협업이 동시에 실현된다.

---

## Ⅰ. 개요 및 필요성

전통적인 인프라 관리는 담당자가 수동으로 서버에 접속하여 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)을 변경하는 방식이었다. 이 방식은 시간이 지남에 따라 서버마다 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)이 달라지는 <strong><a href="/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/">구성 편류</a>(<a href="/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/">Configuration Drift</a>)</strong> 문제를 유발한다. 어느 서버는 Apache 2.4.29, 다른 서버는 2.4.41이 설치되어 있는 식이다.

**IaC가 해결하는 문제**:
- 재현성: 동일한 코드로 동일한 환경을 몇 번이든 재생성
- [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리: 인프라 변경 이력이 Git으로 추적됨
- 협업: 코드 리뷰를 통한 인프라 변경 검토
- 자동화: [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 파이프라인에서 인프라 배포까지 자동화

- **📢 섹션 요약 비유**: [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 없는 서버 관리는 레시피 없이 요리하는 것이다 — 매번 조금씩 달라지고, 담당자가 바뀌면 아무도 재현할 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

<strong><a href="/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/">Terraform</a>(HCL) Plan-Apply 워크플로</strong>:

```
+-------------------------------------------------------------+
|                    GitOps + Terraform 흐름                   |
|                                                             |
|  개발자 -> PR(HCL 변경) -> 코드 리뷰 -> merge                  |
|                                    v                        |
|             terraform plan  (변경 사항 미리 보기)             |
|                    v        (diff: +3 리소스, -1 리소스)      |
|             terraform apply (실제 적용, State 파일 갱신)      |
|                    v                                        |
|             State 파일 (terraform.tfstate, S3 원격 저장)      |
+-------------------------------------------------------------+
```

| 도구 | 방식 | 특징 | 주요 사용 |
|:---|:---:|:---|:---|
| [Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) | 선언적 | HCL, [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 관리, [멀티 클라우드](/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/) | 인프라 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/) |
| [Ansible](/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/) | 절차적 | YAML [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/), 에이전트리스 | 서버 [구성 관리](/studynote/12_it_management/02_itsm_itil/873_configuration_management/) |
| Pulumi | 선언적 | 일반 프로그래밍 언어(Python/TS) | 개발자 친화적 [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) |
| CloudFormation | 선언적 | AWS 전용, [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/)/YAML | AWS 네이티브 관리 |

<strong><a href="/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/">불변 인프라</a>(<a href="/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/">Immutable Infrastructure</a>) vs <a href="/studynote/13_cloud_architecture/04_devops_observability/170_immutable_infrastructure_mutable_vs_immutable/">가변 인프라</a>(<a href="/studynote/13_cloud_architecture/04_devops_observability/170_immutable_infrastructure_mutable_vs_immutable/">Mutable Infrastructure</a>)</strong>:
- <strong><a href="/studynote/13_cloud_architecture/04_devops_observability/170_immutable_infrastructure_mutable_vs_immutable/">가변 인프라</a></strong>: 서버를 멈추지 않고 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 변경 -> 시간이 지나면 [Configuration Drift](/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/) 발생
- <strong><a href="/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/">불변 인프라</a></strong>: 변경이 필요하면 새 이미지를 만들어 기존 서버를 교체 -> 항상 동일한 상태 보장

[불변 인프라](/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)는 [도커 이미지](/studynote/13_cloud_architecture/02_iaas_paas_saas/068_docker_image_immutable_package/) + Terraform의 조합으로 구현된다: 코드 변경 -> [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 파이프라인 -> 새 [Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) 이미지 빌드 -> Terraform으로 새 EC2/ECS 인스턴스 배포 -> 구 인스턴스 종료.

- **📢 섹션 요약 비유**: [불변 인프라](/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)는 스마트폰 OS 업데이트와 같다 — 기존 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 수정하지 않고 새 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 전체를 설치하기 때문에, 업데이트 전과 후의 상태가 항상 명확히 다르다.

---

## Ⅲ. 비교 및 연결

<strong><a href="/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/">Terraform</a> <a href="/studynote/04_software_engineering/04_testing_quality/192_module_independence/">모듈</a>(<a href="/studynote/04_software_engineering/04_testing_quality/192_module_independence/">Module</a>)</strong>: 반복 사용하는 인프라 패턴을 재사용 가능한 코드 블록으로 캡슐화. 예: [VPC](/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/) [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/), EKS 클러스터 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/). [Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) Registry에서 공개 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 활용 가능.

<strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/">State</a> <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 관리</strong>: `terraform.tfstate`에 현재 인프라 상태 기록. 팀 협업 시 S3 + [DynamoDB](/studynote/05_database/04_transactions_concurrency/545_dynamodb/)(잠금)로 원격 [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 저장 필수. [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 비밀 값이 포함될 수 있으므로 암호화 필수.

<strong><a href="/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a></strong>: 인프라와 애플리케이션 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)을 모두 Git에서 관리하고, 자동화된 시스템이 실제 상태를 Git 상태와 일치시킨다. ArgoCD(앱), Flux(인프라), Atlantis([Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) [PR](/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 자동화).

- **📢 섹션 요약 비유**: [Terraform State](/studynote/15_devops_sre/05_devsecops/294_tfstate/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 인프라의 주민등록증 보관함이다. 여기가 털리거나 분실되면 인프라의 "공식 현황"을 잃어버린다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**기술사 시험 판단 포인트**:
1. 선언적([Declarative](/studynote/15_devops_sre/05_devsecops/219_declarative_yaml/)) vs 절차적(Procedural) IaC의 차이를 [Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) vs Ansible로 대비 설명한다.
2. [불변 인프라](/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/) 구현 흐름(이미지 빌드 -> 배포 -> 구 인스턴스 교체)을 순서대로 기술한다.
3. [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 역할과 원격 저장 필요성(팀 협업, 잠금)을 보안 관점에서 언급한다.

**실무 시나리오**: [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 50개를 운영하는 기업이 서버 [구성 편류](/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/) 문제로 장애를 반복 경험. 해결책: 모든 서비스를 [Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) 이미지화 + Terraform으로 EKS 클러스터 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/) + Atlantis로 [PR](/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 기반 인프라 변경 승인 -> 장애 원인의 60%를 차지하던 "환경 차이" 문제 해소.

- **📢 섹션 요약 비유**: GitOps는 인프라도 코드처럼 관리하는 방식이다. 회계 장부([State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))를 혼자 관리하면 실수가 나지만, 팀 리뷰([PR](/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 승인)를 거치면 오류가 줄어든다.

---

## Ⅴ. 기대효과 및 결론

IaC와 [불변 인프라](/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)를 도입하면:
- **재현성 100%**: 동일 코드 -> 동일 환경, 재난 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시 수 분 내 인프라 재생성
- <strong><a href="/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/">Configuration Drift</a> 제거</strong>: 불변 이미지 교체로 서버 상태 항상 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 유지
- <strong><a href="/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a> 추적</strong>: Git 커밋 이력이 인프라 변경 내역의 완전한 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)
- **팀 협업**: [PR](/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)/코드 리뷰로 보안 검토와 지식 공유 자동화

IaC는 단순한 도구가 아니라 <strong>인프라 관리의 패러다임 전환</strong>이며, [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 운영의 필수 전제 조건이다.

- **📢 섹션 요약 비유**: IaC는 건축 설계도다. 설계도 없이 지은 건물은 수리할 때마다 벽을 뜯어봐야 하지만, 설계도가 있으면 어디를 어떻게 바꿔야 하는지 즉시 알 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [멀티 클라우드](/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/) ([Multi-Cloud](/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/)) | [Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/), 이식성, 벤더 독립 · 500 |
| [불변 인프라](/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/) ([Immutable Infrastructure](/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)) | [도커 이미지](/studynote/13_cloud_architecture/02_iaas_paas_saas/068_docker_image_immutable_package/), [Configuration Drift](/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/) · 501 |
| [GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) | ArgoCD, Atlantis, [PR](/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 기반 인프라 · 502 |
| [Ansible](/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/) | 절차적 [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/), [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/), 에이전트리스 · 540 |
| [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD ([지속적 통합](/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/)/배포) | 파이프라인, 빌드, 배포 자동화 · 505 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Terraform · 이식성] -> [IaC 테라폼과 불변 인프라 선언] -> [파이프라인 · 빌드]
```

### 👶 어린이를 위한 3줄 비유 설명

1. IaC는 서버 설치 설명서를 코드로 쓰는 것이에요 — 설명서만 있으면 똑같은 서버를 언제든 다시 만들 수 있어요.
2. [불변 인프라](/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)는 낡은 장난감을 고치는 대신 새 것으로 교환하는 것처럼, 서버도 수리 대신 새 것으로 바꿔요.
3. GitOps는 인프라 변경도 숙제처럼 선생님(팀원)한테 검사를 받아야 적용되는 방식이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 504 / 552

<- **이전**: [503. 서버리스 콜드 스타트 지연 제어 (Serverless Cold Start Latency Control)](/studynote/06_ict_convergence/03_cloud_infrastructure/503_serverless_cold_start_latency_control/)
**다음**: [505. 마이크로서비스, API 게이트웨이, 서비스 메시 (MSA API Gateway Service Mesh)](/studynote/06_ict_convergence/03_cloud_infrastructure/505_microservices_api_gateway_service_mesh/) ->

---
