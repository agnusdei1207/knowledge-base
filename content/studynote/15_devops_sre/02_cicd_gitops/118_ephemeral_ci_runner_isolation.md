---
title: "118. Ephemeral Ci Runner Isolation"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Ephemeral [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) Runner는 <strong>빌드마다 새로운 러너(<a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a>/<a href="/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/">VM</a>)를 <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a>하고, 빌드 완료 후 즉시 삭제</strong>하는 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 실행 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로, 이전 빌드의 잔여물(캐시·[파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)·프로세스)이 다음 빌드에 영향을 주지 않는 <strong>완전 격리(Clean Room)</strong>를 보장한다.
> 2. **가치**: 영구 러너(Persistent Runner)는 이전 빌드의 `node_modules`·악성 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)·[환경 변수](/studynote/02_operating_system/02_process_thread/156_environment_variables/)가 남아 <strong>빌드 오염(Build Pollution)·보안 침해</strong>를 유발하지만, Ephemeral 러너는 매번 깨끗한 상태에서 시작한다.
> 3. **판단 포인트**: GitHub Actions(기본 Ephemeral)·GitLab Runner([Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) executor)·[Jenkins](/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/)(K8s [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) agent)가 대표 구현이며, <strong>빌드 시간 vs 격리 보안</strong>의 트레이드오프(캐시 활용 어려움)를 관리해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Persistent vs Ephemeral Runner                     |
+-------------------------------------------------------+
|  [Persistent (영구)]                                  |
|   Build 1 -> Runner A (파일 잔여) ->                   |
|   Build 2 -> Runner A (오염된 환경!) ⚠️               |
|   -> 재현 불가, 보안 취약                              |
|                                                       |
|  [Ephemeral (일회성)]                                 |
|   Build 1 -> Runner X (새 생성) -> 빌드 -> 삭제 🗑️     |
|   Build 2 -> Runner Y (새 생성) -> 빌드 -> 삭제 🗑️     |
|   -> 완전 격리, 재현 가능, 보안 강화                   |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Persistent Runner는 매번 같은 접시에 음식을 담는 것(이전 음식 잔여물 위험)이고, Ephemeral Runner는 매번 새 일회용 접시를 사용하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 도구별 Ephemeral 구현

| [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 도구 | 구현 방식 | 기본 모드 |
|:---|:---|:---|
| **GitHub Actions** | 매 워크플로마다 새 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) | **Ephemeral (기본)** |
| **GitLab Runner** | [Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) executor | [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 필요 |
| <strong><a href="/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/">Jenkins</a></strong> | K8s [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) agent | [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 필요 |
| **Buildkite** | [스팟 인스턴스](/studynote/06_ict_convergence/03_cloud_infrastructure/209_spot_instance_cloud_cost_optimization/) + 자동 종료 | [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 필요 |

### 캐시 트레이드오프

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 격리 | 속도 |
|:---|:---|:---|
| **완전 Ephemeral** | **최고** | 느림 (매번 설치) |
| **캐시 레이어 분리** | 높음 | **빠름 (캐시 재사용)** |

- **📢 섹션 요약 비유**: 완전 Ephemeral은 매번 새 주방을 짓는 것이고, 캐시 분리는 냉장고(캐시)만 공유하고 조리대(러너)는 새로 만드는 절충안이다.

---

## Ⅲ. 비교 및 연결

| 비교 | Persistent | Ephemeral |
|:---|:---|:---|
| **격리** | 없음 | **완전** |
| **보안** | 취약 | **강화** |
| **재현성** | 낮음 | **높음** |
| **속도** | 빠름 (캐시) | 느림 (해결: 캐시 레이어) |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [Best Practice](/studynote/07_enterprise_systems/02_erp_systems/087_erp_package_advantages_best_practice/)
1. **러너**: Ephemeral 기본, 캐시는 외부 저장소(S3) 활용.
2. <strong><a href="/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/">시크릿</a></strong>: 러너 종료 시 메모리에서 삭제 -> 유출 방지.
3. **Self-hosted**: K8s [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) agent로 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·삭제.

---

## Ⅴ. 기대효과 및 결론

| 지표 | Persistent | Ephemeral | 개선 |
|:---|:---|:---|:---|
| 빌드 오염 | 빈번 | **0건** | 완전 제거 |
| [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 유출 | [잔여 위험](/studynote/09_security/01_intro_principles/038_residual_risk/) | **삭제 보장** | 보안 강화 |
| 재현성 | 환경 의존 | **100%** | [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 신뢰 |

Ephemeral Runner는 <strong><a href="/studynote/12_it_management/02_itsm_itil/874_configuration_item/">CI</a>/CD 보안의 기본 원칙</strong>이며, SLSA Level 3 이상에서는 격리된 빌드 환경이 필수 요구 사항이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **빌드 오염 (Build Pollution)** | Persistent Runner의 핵심 위험 |
| **GitHub Actions** | 기본 Ephemeral Runner |
| <strong>K8s <a href="/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/">Pod</a> Agent</strong> | [Jenkins](/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/)/GitLab의 Ephemeral 구현 |
| **SLSA** | 격리 빌드를 요구하는 [공급망 보안](/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/) 프레임워크 |
| **캐시 레이어** | Ephemeral + 속도의 절충안 |

### 📈 관련 키워드 및 발전 흐름도

```text
[물리 빌드 서버 (Persistent, 2000s)]
    |
    v
[Docker 기반 CI (GitLab Runner, 2015~)]
    |
    v
[GitHub Actions (2019) — 기본 Ephemeral VM]
    |
    v
[K8s Pod Agent (2020~) — 자동 생성·삭제]
    |
    v
[현재: SLSA + Ephemeral — 공급망 보안 필수 요건]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 영구 러너는 **같은 접시를 계속 쓰는** 거예요. 이전 음식 찌꺼기가 남아있을 수 있어요 ⚠️
2. 일회성 러너는 <strong>매번 새 일회용 접시</strong>를 사용해서 항상 깨끗해요! 🧹
3. 덕분에 이전 빌드의 나쁜 것이 **다음 빌드에 절대 영향을 주지 않아서** 안전하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 118 / 373

<- **이전**: [117. TextOps/DocOps 자동화 - 문서 파이프라인 CI/CD·Docs-as-Code](/studynote/15_devops_sre/02_cicd_gitops/117_textops_docops_automation/)
**다음**: [119. Pre-commit Hook 린팅 (Pre-commit Hook Linting) - 커밋 전 자동 코드 품질 검증](/studynote/15_devops_sre/02_cicd_gitops/119_pre_commit_hook_linting/) ->

---
