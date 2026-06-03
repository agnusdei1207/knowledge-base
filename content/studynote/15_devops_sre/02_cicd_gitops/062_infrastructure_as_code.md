+++
title = "62. 인프라스트럭처 애즈 코드 (Infrastructure as Code, IaC)"
date = 2026-04-05

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)(Infrastructure [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/))는 서버, 네트워크, 스토리지 같은 인프라를 수동 클릭이 아니라 코드로 선언하고 관리하는 방식이다.
> 2. **가치**: IaC는 [구성 편류](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/)([Configuration Drift](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/)), 재현 불가능한 환경, 느린 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 문제를 줄이고 변경 이력을 Git으로 남긴다.
> 3. **판단**: 선언형([Declarative](/knowledge-base/studynote/15_devops_sre/05_devsecops/219_declarative_yaml/))과 명령형(Imperative), 상태([State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)), 프로바이더([Provider](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/150_soa_triangle_architecture/)), [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)([Module](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/))을 함께 이해해야 실제 운영 품질이 올라간다.

---

## Ⅰ. 개요 및 필요성

수동 운영은 빨리 되는 것처럼 보여도 시간이 지나면 누가 무엇을 바꿨는지 알 수 없게 된다. 서버마다 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 조금씩 달라지고, 같은 환경을 다시 만들 수도 없고, 장애가 나면 되돌리기도 어렵다.

IaC는 이 문제를 코드와 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리로 푼다. 인프라의 "정답"을 코드로 기록하고, 실제 환경이 그 정답과 같은지 계속 비교한다.

- **📢 섹션 요약 비유**: 건물 설계도가 있으면 같은 집을 다시 지을 수 있지만, 현장 구두 지시만 있으면 매번 다른 집이 나온다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Git / HCL / YAML</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Plan</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Apply</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Provider</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Cloud API</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Resources</div>
</div>
</div>



| 핵심 개념 | 역할 | 없으면 생기는 문제 |
| :-- | :-- | :-- |
| [Desired State](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/080_kube_controller_manager_desired_state/) | 원하는 최종 상태 정의 | 목표가 흐려짐 |
| [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) | 현재 배포 상태 기록 | 변경 추적 어려움 |
| [Provider](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/150_soa_triangle_architecture/) | AWS, GCP, Azure와 연결 | [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출이 흩어짐 |
| [Idempotency](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/) | 같은 코드를 반복해도 결과가 같음 | 중복 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 위험 |
| [Module](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) | 재사용 가능한 인프라 묶음 | 복붙 증가 |

선언형 IaC는 "무엇이 되어야 하는가"를 적고, 도구가 차이를 계산한다. 명령형은 "무엇을 어떻게 할 것인가"를 순서대로 적는다. 실제 운영에서는 둘을 섞어 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)도 하지만, 기준 상태를 문서화하는 힘은 선언형이 더 강하다.

- **📢 섹션 요약 비유**: 목적지를 먼저 적는 내비게이션과, 매번 방향을 외워서 가는 사람이 있다면 전자가 훨씬 덜 헤맨다.

---

## Ⅲ. 비교 및 연결

| 도구 | 스타일 | 강점 | 주 용도 |
| :-- | :-- | :-- | :-- |
| [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) | 선언형 | 멀티클라우드, 상태 관리 | [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/) |
| [Ansible](/knowledge-base/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/) | 명령형 | [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 자동화, [접근성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/292_accessibility_kwcag_wcag/) | [구성 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/089_configuration_management/) |
| Pulumi | 코드형 | 일반 언어의 표현력 | 복잡한 로직 |
| CloudFormation | 선언형 | AWS 기본 통합 | AWS 인프라 |

| 구분 | 수동 운영 | [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) |
| :-- | :-- | :-- |
| 추적성 | 낮음 | 높음 |
| 재현성 | 낮음 | 높음 |
| [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) | 어렵다 | 코드 기반으로 가능 |
| [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) | 사람 기억 의존 | Git 히스토리 의존 |

IaC는 도구 이름보다 운영 원리가 중요하다. 어떤 도구를 쓰든, 상태를 관리하고 차이를 줄이며, 변경을 [코드 리뷰](/knowledge-base/studynote/04_software_engineering/06_software_architecture/330_code_review/)로 통제하는 구조가 핵심이다.

- **📢 섹션 요약 비유**: 같은 요리라도 레시피를 남기면 다시 만들 수 있고, 감으로만 하면 맛이 매번 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 원격 [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) backend와 잠금([locking](/knowledge-base/studynote/05_database/04_transactions_concurrency/213_locking_mechanism_concurrency_control/))을 쓰는가?
2. Plan 결과를 리뷰하고 Apply를 분리하는가?
3. [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이 너무 커지지 않도록 경계를 나눴는가?
4. 비밀값은 코드와 State에 안전하게 보관되는가?
5. Drift detection과 재동기화 절차가 있는가?
6. [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) Code로 보안 규칙을 자동 검사하는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 운영자가 콘솔에서만 수정을 남기는 설계
- [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 로컬에만 두는 설계
- 비밀키를 코드에 하드코딩하는 설계
- 너무 큰 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 하나로 모든 인프라를 묶는 설계

기술사 관점에서는 IaC를 "자동화 도구"가 아니라 "운영 표준화 도구"로 봐야 한다. 자동화만 하면 편해지고, 표준화까지 해야 재현성과 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)가 따라온다.

- **📢 섹션 요약 비유**: 같은 집을 여러 사람이 지어도 설계도와 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)가 있으면 품질이 흔들리지 않는다.

---

## Ⅴ. 기대효과 및 결론

IaC가 자리 잡으면 환경 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)이 빨라지고, 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 쉬워지고, 규정 준수도 증명하기 쉬워진다. 결국 인프라가 사람의 기억이 아니라 코드의 질서 위에 놓인다.

앞으로는 [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/), [Platform Engineering](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/109_platform_engineering_cognitive_load/), [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) Code가 붙으면서 인프라 운영은 더 소프트웨어 개발처럼 바뀔 것이다.

- **📢 섹션 요약 비유**: 설계도, 공정표, 검수표가 있으면 건물을 다시 지어도 결과가 비슷하게 나온다.

---

## 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Git</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">IaC Code</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Plan / Apply</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">State / Provider</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Cloud Resources</div>
</div>
</div>



---

## 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">수동 운영</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">스크립트 자동화</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">IaC</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">GitOps / Policy as Code</div>
</div>
</div>



---

## 어린이를 위한 3줄 비유 설명

건물을 짓기 전에 설계도를 먼저 그려요.  
설계도가 있으면 같은 집을 또 지을 수 있어요.  
IaC는 컴퓨터 세상을 설계도로 관리하는 방법이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 62 / 373

← **이전**: [61. Helm Charts (헬름 차트) - 쿠버네티스 패키징](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/061_helm_charts/)
**다음**: [63. Terraform vs Ansible](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/063_terraform_ansible/) →

---
