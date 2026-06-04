+++
title = "74. GitLab CI/CD - 파이프라인 자동화"
date = 2026-04-10

[taxonomies]
tags = ["studynote-devops"]

[extra]
tags = ["studynote-devops"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GitLab [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD는 GitLab에 내장된 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 자동화 시스템이다.
> 2. **가치**: 코드 저장소와 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD가 자연스럽게 연결된다.
> 3. **판단**: .gitlab-[ci](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/).yml과 Runner 개념이 핵심이다.

---

## Ⅰ. 개요 및 필요성

저장소와 배포가 가까울수록 자동화가 쉬워진다.

GitLab [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD가 그 예다.

- **📢 섹션 요약 비유**: 공장 옆에 컨베이어벨트를 바로 붙인 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
.gitlab-ci.yml
  v runner
Jobs / Stages
```

| 요소 | 의미 |
| :-- | :-- |
| YAML | [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 정의 |
| Runner | 실행기 |
| Stage | 단계 |

GitLab [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD는 저장소에 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 코드로 두고 자동 실행한다.

- **📢 섹션 요약 비유**: 레시피가 창고 안에 바로 있는 것이다.

---

## Ⅲ. 비교 및 연결

| 구분 | GitLab [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD | [Jenkins](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/) |
| :-- | :-- | :-- |
| 통합 | 높음 | 플러그인 중심 |
| 정의 | YAML | Jenkinsfile |

| 기능 | 의미 |
| :-- | :-- |
| [Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/) | 자동화 흐름 |
| Runner | 실행 자원 |

GitLab [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD는 Git과 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인의 통합이 강하다.

- **📢 섹션 요약 비유**: 창고와 공장이 한 건물에 있는 느낌이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. .gitlab-[ci](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/).yml을 쓰는가?
2. Runner를 관리하는가?
3. Stage/Job을 이해하는가?
4. 보안 변수 관리를 하는가?
5. 배포 흐름이 자동화되었는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- YAML을 방치하는 설계
- Runner 자원 계획이 없는 설계
- 저장소와 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD를 분리해 두는 설계
- 변수/[시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)을 노출하는 설계

기술사 관점에서는 GitLab [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD를 "저장소 내장형 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 자동화"로 설명해야 한다.

- **📢 섹션 요약 비유**: 코드를 넣으면 바로 공정이 돈다.

---

## Ⅴ. 기대효과 및 결론

GitLab [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD는 자동화와 추적성을 높인다.

결론적으로 GitLab [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD는 저장소 통합형 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 자동화 시스템이다.

- **📢 섹션 요약 비유**: 저장소에 레시피와 공장이 같이 있다.

---

## 관련 개념 맵

```text
.gitlab-ci.yml
  v
Runner
  v
Pipeline
```

---

## 관련 키워드 및 발전 흐름도

```text
GitLab
  v
CI/CD
  v
Runner
```

---

## 어린이를 위한 3줄 비유 설명

코드 저장소에서 바로 일해요.
줄을 정해 자동으로 움직여요.
GitLab [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD는 그런 시스템이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 74 / 373

<- **이전**: [073. GitHub Actions 기반 CI/CD 워크플로우 (GitHub Actions CI/CD)](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/073_github_actions_ci_cd_workflow/)
**다음**: [75. 아티팩트 (Artifact) - 파이프라인의 최종 빌드 산출물 보관](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/) ->

---
