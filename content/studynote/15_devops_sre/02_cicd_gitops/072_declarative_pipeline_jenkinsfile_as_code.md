+++
title = "72. 선언적 파이프라인 - Jenkinsfile (Pipeline as Code)"
date = 2026-04-10

[taxonomies]
tags = ["studynote-devops"]

[extra]
tags = ["studynote-devops"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 선언적 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인은 Jenkinsfile로 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 흐름을 코드로 정의하는 방식이다.
> 2. **가치**: 빌드/테스트/배포를 표준화하고 재현성을 높인다.
> 3. **판단**: 선언적 구문과 단계적 실행 구조를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

UI로만 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 만들면 추적이 어렵다.

Jenkinsfile로 관리하면 [코드 리뷰](/knowledge-base/studynote/04_software_engineering/06_software_architecture/330_code_review/)와 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리가 가능하다.

- **📢 섹션 요약 비유**: 요리 순서를 종이에 적어 두는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Jenkinsfile
  v declarative pipeline
Stages / Steps
```

| 요소 | 의미 |
| :-- | :-- |
| [pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/) | 전체 흐름 |
| stage | 단계 |
| agent | 실행 환경 |

선언적 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인은 구조가 명확하고 읽기 쉬워 표준화에 적합하다.

- **📢 섹션 요약 비유**: 레시피가 깔끔하게 정리된 요리책이다.

---

## Ⅲ. 비교 및 연결

| 구분 | [Declarative](/knowledge-base/studynote/15_devops_sre/05_devsecops/219_declarative_yaml/) | Scripted |
| :-- | :-- | :-- |
| 구조 | 명확 | 유연 |
| [가독성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/) | 높음 | 낮을 수 있음 |
| 사용 | 표준화 | 복잡한 제어 |

| 관련 | 의미 |
| :-- | :-- |
| [Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/) [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) | 코드화 |
| [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD | 자동화 |

선언적 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인은 운영 표준과 협업에 유리하다.

- **📢 섹션 요약 비유**: 약속된 레시피라서 누구나 따라 하기 쉽다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. Jenkinsfile로 관리하는가?
2. stage와 agent를 나눴는가?
3. [코드 리뷰](/knowledge-base/studynote/04_software_engineering/06_software_architecture/330_code_review/)가 가능한가?
4. 재현성이 있는가?
5. 운영 표준과 맞는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- UI에만 의존하는 설계
- scripted와 declarative를 혼동하는 설계
- [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 문서처럼만 보는 설계
- [환경 변수](/knowledge-base/studynote/02_operating_system/02_process_thread/156_environment_variables/)를 무질서하게 쓰는 설계

기술사 관점에서는 선언적 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 "코드로 정의된 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 표준"으로 설명해야 한다.

- **📢 섹션 요약 비유**: 순서를 코드로 써 둔 자동 공정표다.

---

## Ⅴ. 기대효과 및 결론

Jenkinsfile은 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 재현 가능하게 만든다.

결론적으로 선언적 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인은 Jenkinsfile로 정의하는 [Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/) [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) Code다.

- **📢 섹션 요약 비유**: 작업 순서를 코드로 적는 것이다.

---

## 관련 개념 맵

```text
Jenkinsfile
  v
Declarative Pipeline
  v
Stages / Steps
  v
CI/CD
```

---

## 관련 키워드 및 발전 흐름도

```text
Pipeline as Code
  v
Jenkinsfile
  v
Declarative Pipeline
```

---

## 어린이를 위한 3줄 비유 설명

순서를 코드로 적어요.
자동으로 따라 해요.
선언적 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인은 그런 방식이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 72 / 373

<- **이전**: [71. 젠킨스 (Jenkins) - 오픈소스 CI/CD 자동화 빌드 서버](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/)
**다음**: [073. GitHub Actions 기반 CI/CD 워크플로우 (GitHub Actions CI/CD)](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/073_github_actions_ci_cd_workflow/) ->

---
