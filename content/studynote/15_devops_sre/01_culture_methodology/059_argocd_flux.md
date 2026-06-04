---
title: "59. Argo CD / Flux - GitOps 지속적 배포"
date: "2026-04-05"
tags:
  - "studynote-devops-sre"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Argo CD와 Flux는 Git에 선언적으로 저장된 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 원하는 상태를 지속적으로 맞춰 주는 [GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 도구다.
> 2. **가치**: 배포 이력을 Git으로 관리해 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/), [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), 드리프트 감지를 쉽게 만들고, 배포 자격증명 노출도 줄인다.
> 3. **판단 포인트**: Pull 기반 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/), 리컨실리에이션(Reconciliation), 멀티 클러스터 운영, UI/[모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)성 차이를 구분해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 배포는 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 서버가 클러스터에 직접 명령을 보내는 Push 방식이 많았다. 그러나 이 방식은 자격증명 노출과 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 드리프트([Configuration Drift](/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/)) 관리가 어려웠다.

GitOps는 "Git이 진실의 원천"이라는 관점으로 이 문제를 바꾼다. 클러스터 내부의 에이전트가 Git을 보고 원하는 상태와 실제 상태를 맞춘다.

- **📢 섹션 요약 비유**: 선장이 직접 배를 움직이는 대신, 항해 일지를 보고 배가 스스로 항로를 맞추는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

GitOps의 핵심은 선언적(manifest) 정의와 지속적 비교다. Argo CD와 Flux는 주기적으로 Git 상태와 클러스터 상태를 비교하고 차이가 나면 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)한다.

```text
Git Repo
   v desired state
Argo CD / Flux
   v reconcile
Kubernetes Cluster
   ^ live state diff
```

| 구성 요소 | 역할 |
| :-- | :-- |
| Git Repo | 원하는 상태의 단일 진실 출처 |
| Controller | 상태 차이를 감지하고 적용 |
| Manifest | YAML, [Helm](/studynote/06_ict_convergence/03_cloud_infrastructure/207_helm_kubernetes_package_manager_chart/), [Kustomize](/studynote/15_devops_sre/02_cicd_gitops/091_kustomize_kubernetes_declarative_overlay_manifest/) 등 선언형 정의 |
| Cluster | 실제 실행 중인 [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) |

Push 방식은 외부 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 서버가 클러스터에 접근해야 하지만, Pull 방식은 클러스터 안의 컨트롤러가 스스로 Git을 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다. 그래서 보안과 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)에 유리하다.

- **📢 섹션 요약 비유**: 관리자 한 명이 문을 두드리는 대신, 방 안에 있는 감시 카메라가 스스로 약속과 현실을 비교하는 구조다.

---

## Ⅲ. 비교 및 연결

Argo CD와 Flux는 둘 다 [GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 도구이지만 강점이 다르다.

| 항목 | [Argo CD](/studynote/13_cloud_architecture/07_container_k8s/114_argocd_gitops_cd/) | Flux |
| :-- | :-- | :-- |
| 강점 | Web UI, 가시성, 수동 승인 | [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)-native, [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)성 |
| 운영 감각 | 대시보드 중심 | 컨트롤러 중심 |
| 적합한 경우 | 운영 가시성이 중요할 때 | 경량/자동화가 중요할 때 |

전통 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD와 비교하면, GitOps는 배포를 "[파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 결과"가 아니라 "Git 상태 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)"로 본다. 따라서 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)은 `git revert`에 가까운 동작이 된다.

- **📢 섹션 요약 비유**: 바로 전화해서 지시하는 방식과, 적어 둔 메모를 보고 자동으로 움직이는 방식의 차이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

GitOps는 단순 배포 자동화가 아니라, 운영 상태를 코드로 재현 가능하게 만드는 운영 철학이다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. Git이 진짜 원하는 상태의 단일 출처인가?
2. [Argo CD](/studynote/13_cloud_architecture/07_container_k8s/114_argocd_gitops_cd/)/Flux가 드리프트를 탐지할 수 있는가?
3. 멀티 클러스터, [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/), [시크릿 관리](/studynote/13_cloud_architecture/04_devops_observability/177_secrets_management_vault_kubernetes/)가 준비되어 있는가?
4. App of Apps, [Kustomize](/studynote/15_devops_sre/02_cicd_gitops/091_kustomize_kubernetes_declarative_overlay_manifest/), [Helm](/studynote/06_ict_convergence/03_cloud_infrastructure/207_helm_kubernetes_package_manager_chart/) 같은 구성 표준이 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- Git에 실제 운영 상태와 다른 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 남기는 설계
- 자동 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)만 믿고 승인/배포 통제를 비우는 설계
- [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)을 평문으로 Git에 두는 설계

- **📢 섹션 요약 비유**: 책장에 적어 둔 목록과 실제 꽂힌 책이 늘 같아야 하는 도서관 운영이다.

---

## Ⅴ. 기대효과 및 결론

Argo CD와 Flux는 배포를 사람 손의 작업에서 선언적 운영으로 바꾼다. 덕분에 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 가능성과 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)성이 높아지고, 클러스터 상태를 더 예측 가능하게 만든다.

다만 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과 권한 설계를 잘못하면 자동화가 곧 자동 사고가 될 수 있다. 결국 GitOps는 도구보다 운영 규율이 먼저다.

- **📢 섹션 요약 비유**: 레시피를 적어 두고, 주방은 그 레시피대로만 움직이게 하는 조리 시스템이다.

---

## 관련 개념 맵

```text
Git Repo
   v
Argo CD / Flux
   v
Reconciliation
   v
Kubernetes Desired State
```

---

## 관련 키워드 및 발전 흐름도

```text
Push 배포
   v
GitOps
   v
Argo CD / Flux
   v
드리프트 감지 / 자동 롤백
```

---

## 어린이를 위한 3줄 비유 설명

Argo CD와 Flux는 공책에 적어 둔 약속대로 방을 정리하는 로봇이에요.
공책과 방이 다르면 바로 알려 주고 맞춰 줘요.
그래서 늘 같은 상태를 유지하기 쉬워요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 59 / 373

<- **이전**: [58. 개발자 경험 (DX, Developer Experience) 향상 전략](/studynote/15_devops_sre/01_culture_methodology/058_dx_developer_experience/)
**다음**: [60. ChatOps (Chat + Operations) 협업 운영 모델](/studynote/15_devops_sre/01_culture_methodology/060_chatops/) ->

---
