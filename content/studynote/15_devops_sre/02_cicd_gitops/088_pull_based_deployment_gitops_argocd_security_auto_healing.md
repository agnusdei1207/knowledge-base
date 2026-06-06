---
title: "088. Pull Based Deployment Gitops Argocd Security Auto Healing"
date: "2026-04-10"
tags:
  - "studynote-devops"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 풀 기반(Pull-based) 배포는 클러스터 내부에 설치된 에이전트(예: ArgoCD)가 외부 Git 저장소를 주기적으로 관찰하여, 변경된 배포 명세서를 스스로 끌어와 적용하는 아키텍처다.
> 2. **가치**: 외부 `CI (Continuous Integration)` 서버가 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 클러스터의 관리자 자격 증명(Credential)을 알 필요가 없어지므로, 공격 표면이 극단적으로 축소되고 보안 수준이 획기적으로 향상된다.
> 3. **판단 포인트**: '명령'이 아닌 '선언'을 중심으로, Git에 저장된 명세와 실제 인프라 상태 간의 드리프트(Drift)를 자동으로 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)(Reconciliation)하는 운영 패러다임 전환이 필요할 때 도입한다.

---

## Ⅰ. 개요 및 필요성

전통적인 푸시(Push) 기반 배포 방식에서는 [젠킨스](/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/)([Jenkins](/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/))와 같은 외부 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 도구가 빌드를 마친 후 직접 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 클러스터에 접속하여 배포 명령(`kubectl apply`)을 내렸다. 이 구조에서는 외부 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 서버가 핵심 인프라의 막강한 제어 권한과 비밀번호를 모두 들고 있어야 했으며, [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 서버가 해킹당하면 전체 인프라가 넘어가는 심각한 보안 위협이 존재했다.

이러한 문제를 해결하기 위해 배포의 방향을 180도 뒤집은 것이 풀 기반(Pull-based) 배포다. 클러스터 안쪽에 권한을 가진 에이전트를 배치하고, 이 에이전트가 오직 바깥의 Git 저장소만 쳐다보며 변경 사항을 가져오게(Pull) 만든 것이다. 이를 통해 외부에서는 클러스터의 존재조차 알 필요가 없는 강력한 격리 환경이 완성되었다.

- **📢 섹션 요약 비유**: 배달원이 집 안까지 들어와 냉장고에 반찬을 넣고 가는 위험한 방식(Push) 대신, 집주인이 우편함에 도착한 레시피를 보고 스스로 요리를 채워 넣는 안전한 방식(Pull)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

풀 기반 배포, 즉 [GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 아키텍처는 진실의 원천, 클러스터 내부 에이전트, 그리고 지속적인 재조정(Reconciliation) 루프로 구성된다.

| 구성 요소 | 핵심 역할 | 동작 원리 및 효과 |
| :--- | :--- | :--- |
| **Git 저장소 (SSOT)** | 인프라 상태의 절대 기준 | `IaC (Infrastructure as Code)` 선언문 보관, `SSOT (Single Source of Truth)` 역할 수행 |
| **Pull 에이전트 (ArgoCD)** | 상태 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 및 배포 수행 | 클러스터 내부에서 실행되며, Git 저장소를 [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)([Polling](/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/))하거나 [웹훅](/studynote/03_network/09_application_layer_web_email/498_webhook_rest_api_reverse_callback/)([Webhook](/studynote/03_network/09_application_layer_web_email/498_webhook_rest_api_reverse_callback/))으로 감지 |
| **Reconciliation Loop** | 드리프트(Drift) 자동 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | Git 명세([Desired State](/studynote/13_cloud_architecture/02_iaas_paas_saas/080_kube_controller_manager_desired_state/))와 [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)(Actual [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))를 지속 비교하여 불일치 시 자동 재조정 |

```text
+--------------------------------------------------------------+
|           Pull-based GitOps 아키텍처 (보안 격리 구조)        |
+--------------------------------------------------------------+
| [외부 환경]                    | [쿠버네티스 클러스터 내부]  |
|                                |                             |
| 1. 개발자 Commit               |                             |
|       |                        |   3. Pull (변경 감지)       |
|       v                        |      <------------+          |
| 2. Git 저장소 (SSOT) <---------+- ArgoCD Controller |          |
|    (Desired State)             |      |            |          |
|                                |      v            |          |
|    * CI 서버는 Git만           |   4. K8s API Apply |          |
|      업데이트하고 배포 끝      |      v            |          |
|                                |  실제 파드 (Actual State)    |
+--------------------------------------------------------------+
```

이 루프 구조의 가장 큰 특징은 <strong>자동 치유(Auto-healing)</strong>다. 누군가 수동 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)로 클러스터 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)을 무단으로 변경하더라도, 에이전트가 즉각 이를 감지하고 Git에 선언된 원래 상태로 되돌려버린다.

- **📢 섹션 요약 비유**: 방을 어지럽혀도(Drift 발생), 로봇 청소기(ArgoCD)가 사진첩(Git)에 있는 완벽하게 정돈된 원래 방의 모습 그대로 5분마다 다시 정리해 놓는 것과 같다.

---

## Ⅲ. 비교 및 연결

푸시 모델과 풀 모델은 인프라 접근 권한의 방향성에서 명확한 차이를 보인다. `CI (Continuous Integration)`와 `CD (Continuous Delivery)`를 분리하는 것이 현대적 트렌드다.

| 비교 축 | [Push-based](/studynote/15_devops_sre/02_cicd_gitops/087_push_based_deployment_jenkins_ci_cd_security_risk/) 배포 | Pull-based 배포 ([GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/)) |
| :--- | :--- | :--- |
| **제어 주체 위치** | 클러스터 외부 ([Jenkins](/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/), GitHub Actions) | 클러스터 내부 (ArgoCD, FluxCD) |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a> 및 <a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">인가</a> 보안</strong> | 외부 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 서버가 클러스터 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 소유해야 함 | 클러스터가 외부 Git 접근 토큰만 보유하면 됨 |
| **진실의 원천 (SSOT)** | [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 스크립트 실행 결과 | Git에 저장된 선언형 매니페스트 (YAML) |
| <strong>장애 시 <a href="/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a> 방식</strong> | 이전 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 재실행 등 수동 개입 | Git Commit Revert 시 즉각 자동 반영 |

Pull 방식은 애플리케이션 소스코드를 담은 'App Repo'와 배포 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) YAML을 담은 '[Config](/studynote/15_devops_sre/01_culture_methodology/009_config/) Repo'를 분리하는 구조와 강하게 연결된다. 빌드는 App Repo에서 푸시 방식으로 끝나고, 배포는 [Config](/studynote/15_devops_sre/01_culture_methodology/009_config/) Repo 업데이트를 통해 풀 방식으로 처리되기 때문이다.

- **📢 섹션 요약 비유**: 주방장([CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/))은 요리(빌드)만 해서 진열대에 올려두고, 매장 매니저(CD 에이전트)가 진열대(Git)를 보고 직접 매장(클러스터)을 꾸미도록 역할을 철저히 분리한 구조다.

---

## Ⅳ. 실무 적용 및 기술사 판단

풀 기반 배포는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)의 선언형([Declarative](/studynote/15_devops_sre/05_devsecops/219_declarative_yaml/)) 철학과 완벽히 맞물리며 [데브옵스](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 보안의 표준으로 자리 잡았다.

### 💡 기술사 판단 ([체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/))
1. <strong><a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">Config</a> Repo 분리</strong>: 소스코드와 매니페스트 저장소를 분리하여, 코드 빌드가 일어날 때마다 불필요한 인프라 배포 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)가 발생하지 않도록 차단했는가?
2. <strong><a href="/studynote/09_security/01_intro_principles/010_least_privilege/">최소 권한 원칙</a> (<a href="/studynote/09_security/11_iam_access_control/569_rbac/">RBAC</a>)</strong>: 내부 에이전트(ArgoCD)에게 부여된 `RBAC (Role-Based Access Control)` 권한이 해당 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/)나 배포 대상 리소스로만 적절히 제한되어 있는가?
3. <strong>드리프트 처리 <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a></strong>: 수동 변경을 무조건 Git 상태로 덮어씌우는 Auto-Sync를 켤 것인지, 위험을 알리기만 하고 멈출 것인지(Out of Sync 알림) 환경별 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 수립했는가?

### 🚫 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **운영 환경 직접 수정 (Hotfix)**: 장애 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를 위해 `kubectl edit`으로 운영 환경을 수정하고, 이를 Git에 반영하지 않는 행위. 다음 Pull 주기가 돌아오면 수정한 내용이 사라져 2차 장애를 유발한다.

- **📢 섹션 요약 비유**: 네비게이션(Git) 경로를 무시하고 운전자가 맘대로 핸들을 꺾어도(수동 수정), 자율주행 시스템(ArgoCD)이 다시 네비게이션 경로로 강제로 차선을 복귀시키는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

풀 기반 배포는 클러스터의 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 정보를 외부에 노출하지 않는다는 압도적인 보안 향상 효과를 가져오며, Git의 커밋 히스토리가 곧 인프라 변경의 완벽한 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)([Audit](/studynote/12_it_management/05_security_compliance/363_audit/) Log)가 되는 투명성을 제공한다. 인프라의 재현성이 보장되므로 재난 시 새로운 클러스터 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)도 매우 빠르다.

하지만 모든 변경이 Git을 거쳐야 하므로 긴급 상황에서의 우회 대처가 몹시 까다로워진다는 단점이 있다. 결론적으로 Pull-based Deployment는 "보안과 인프라 자동화의 수준을 극대화하기 위해, 인프라 제어권을 사람의 손에서 떼어내어 Git과 내부 로봇에게 온전히 이양하는 아키텍처"다.

- **📢 섹션 요약 비유**: 돈통의 열쇠를 직원들에게 나누어주는 대신(Push), 투입구에 적힌 장부(Git)대로만 금고 문이 내부에서 자동으로 열리고 닫히는(Pull) 완벽한 통제 시스템이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a></strong> | "Git을 유일한 진실의 원천(SSOT)으로 삼고, 선언형 인프라와 애플리케이션 배포를 자동화한다"는 전체 운영 방법론 |
| **ArgoCD / FluxCD** | 풀 기반 배포를 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 환경에서 실제로 구현해 주는 양대산맥 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 에이전트 |
| <strong><a href="/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/">IaC</a> (<a href="/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/">Infrastructure as Code</a>)</strong> | 배포 상태를 코드로 선언하여 보관하는 기반 기술 ([Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/), [Kustomize](/studynote/15_devops_sre/02_cicd_gitops/091_kustomize_kubernetes_declarative_overlay_manifest/), [Helm](/studynote/06_ict_convergence/03_cloud_infrastructure/207_helm_kubernetes_package_manager_chart/)) |
| <strong>SSOT (<a href="/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">Single Source of Truth</a>)</strong> | 시스템 전체의 상태를 판단하는 단 하나의 절대적인 기준점 |

### 📈 관련 키워드 및 발전 흐름도

```text
[배포의 한계와 위험]
Push-based Deployment (외부 CI의 과도한 권한)
        |
        v
[보안 및 권한 분리 모델]
CI/CD 파이프라인 분리 (App Repo vs Config Repo)
        |
        v
[새로운 배포 패러다임]
Pull-based Deployment (클러스터 내부 통제)
        |
        v
[선언형 인프라의 완성]
GitOps 아키텍처 및 SSOT 확립
        |
        v
[자동화의 끝판왕]
Reconciliation Loop를 통한 Auto-healing (자동 복구)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 옛날에는 택배 아저씨가 우리 집 비밀번호를 알고 들어와서 물건을 놓고 갔어요. (조금 무섭죠?)
2. 그래서 지금은 집 안에 똑똑한 로봇을 두고, 그 로봇이 우편함만 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해서 물건을 집 안으로 가져오게 했어요.
3. 풀 기반 배포(Pull-based)는 이렇게 외부 사람에게 비밀번호를 주지 않고, 내부 로봇이 알아서 집 안을 정리하는 안전한 방법이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 88 / 373

<- **이전**: [87. 푸시 기반(Push-based) 배포 - 기존 CI/CD 젠킨스의 보안 한계](/studynote/15_devops_sre/02_cicd_gitops/087_push_based_deployment_jenkins_ci_cd_security_risk/)
**다음**: [89. ArgoCD - 쿠버네티스를 위한 GitOps 선언적 배포 도구](/studynote/15_devops_sre/02_cicd_gitops/089_argocd_gitops_continuous_delivery_kubernetes/) ->

---
