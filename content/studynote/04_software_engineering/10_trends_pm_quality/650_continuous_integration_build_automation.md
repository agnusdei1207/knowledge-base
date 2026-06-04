+++
title = "650. CI/CD 지속적 통합, 배포 파이프라인"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/), 배포 파이프라인은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

과거의 개발 방식은 이랬다. 개발자 5명이 각자 맡은 기능을 한 달 동안 자기 PC에서 짰다. 그리고 오픈 전날, 모두 모여서 5개의 코드를 메인 서버(SVN, CVS)에 합치기 시작했다.

당연히 A가 짠 함수와 B가 짠 함수가 이름이 겹치고, C가 바꾼 DB 테이블 때문에 D의 코드가 뻗어버렸다. 이 거대한 충돌을 해결하느라 일주일 내내 집에 가지 못했다. 이를 <strong>'통합의 지옥(Integration Hell)'</strong>이라고 부른다.

익스트림 프로그래밍([XP](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/073_xp_extreme_programming/))의 창시자 켄트 벡은 이 지옥을 끝내기 위해 제안했다. **"통합하는 게 고통스럽다면, 아예 하루에 10번씩 통합해 버리자!"** 코드가 아주 조금(몇십 줄) 바뀌었을 때 바로 합치면, 에러가 나도 원인을 단번에 알 수 있다. 이것이 바로 <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/">지속적 통합</a>(<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/">CI</a>)</strong> 사상의 출발이다.

- **📢 섹션 요약 비유**: 설거지를 한 달 치 모아뒀다가 한 번에 하려면 음식물이 굳어서 며칠이 걸리고 그릇도 깬다(통합의 지옥). CI는 밥을 한 숟갈 먹을 때마다 1초 만에 물로 쓱 헹궈두는 습관이다. 설거지거리가 쌓일 틈이 없다.

---

다음은 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/), 배포 파이프의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
+-------------------------------------------------------------+
|                  CI/CD 지속적 통합, 배포 파이프                        |
+-------------------------------------------------------------+
|                                                             |
|  [입력/요구사항] ---> [핵심 처리 과정] ---> [출력/결과물]  |
|       |                    |                    |          |
|       v                    v                    v          |
|   요구 분석           설계·적용           품질 검증        |
|                                                             |
+-------------------------------------------------------------+
```

이 다이어그램은 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/), 배포 파이프가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

CI는 철저하게 자동화된 **빌드(Build) 파이프라인 아키텍처** 위에서 돌아간다.

- **📢 섹션 요약 비유**: [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/), 배포 파이프라인은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

| 항목 | 설명 | 비고 |
| :--- | :--- | :--- |
| 핵심 특성 | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/), 배포 파이프라인의 핵심 특성과 동작 방식 | 필수 이해 요소 |
| 적용 범위 | 어떤 프로젝트·상황에서 활용하는지 | 선택 기준 |
| 제약 조건 | 적용 시 주의해야 할 전제·한계 | 트레이드오프 |

---

---

---

## Ⅲ. 비교 및 연결

CI는 항상 CD와 묶여서 <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/">CI</a>/CD</strong>라고 불리지만, 역할은 명확히 나뉜다.

| 비교 항목 | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) ([Continuous Integration](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/)) | CD ([Continuous Delivery](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/)/[Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/)) |
|:---|:---|:---|
| **번역** | [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/) | [지속적 제공](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/) / [지속적 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/099_continuous_deployment_cd/) |
| **핵심 목적** | **"코드가 건강하게 합쳐졌는가?"** | **"합쳐진 코드가 고객에게 잘 갔는가?"** |
| **주요 활동** | 빌드, [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/), [정적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) | 스테이징 배포, [인수 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/406_acceptance_test_uat/), 운영 배포 |
| **결과물** | 테스트가 끝난 빌드 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) ([Artifact](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/)) | 실서버에서 돌아가는 살아있는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |
| **주요 도구** | [Jenkins](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/), Travis [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/), GitHub Actions | ArgoCD, AWS CodeDeploy, [Spinnaker](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/093_spinnaker_multi_cloud_cd_canary_analysis/) |

**CI가 없는 CD는 재앙이다.** 테스트도 안 된 고장 난 코드를 고객의 실서버로 빛의 속도로 배달해 버리는 '자동화된 쓰레기 배차 시스템'이 되기 때문이다.

- **📢 섹션 요약 비유**: 식당에서 CI는 주방장이 요리(코드)를 접시에 담고 독이 없는지 기미상궁(테스트)이 맛을 보는 과정이다. CD는 그 안전한 접시를 서빙 로봇이 손님 식탁(실서버)까지 쏟지 않고 나르는 과정이다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 CI를 도입할 때 가장 많이 실패하는 이유는, [젠킨스](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/)([Jenkins](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/))를 깔아놓고 <strong>'테스트 코드'는 하나도 안 짜는 가짜 <a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/">CI</a></strong>를 운영하기 때문이다.

- **📢 섹션 요약 비유**: [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/), 배포 파이프라인은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

---

## Ⅴ. 기대효과 및 결론

완벽한 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 파이프라인이 구축된 팀은 버그에 대한 두려움 없이 과감하게 코드를 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)([Refactoring](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/078_refactoring_code_smells/))할 수 있다. 내가 코드를 망치더라도 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 서버가 1분 안에 알려줄 것이라는 '안전망'이 있기 때문이다. 이는 개발팀 전체의 코딩 속도와 심리적 안정감([Psychological Safety](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/036_psychological_safety/))을 폭발적으로 끌어올린다.

결론적으로 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)([지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/))는 단순히 [젠킨스](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/)([Jenkins](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/)) 서버를 설치하는 '기술'이 아니다. "문제가 생기면 뒤로 미루지 않고, 지금 당장 다 같이 모여서 고친다"는 <strong>개발자들의 행동 양식이자 조직 문화(Culture)</strong>다. 기술 리더는 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 서버의 빨간불을 부끄러워하지 않고, 오히려 일찍 터진 것을 축하하는 문화를 만들어야 한다.

- **📢 섹션 요약 비유**: 서커스단원이 밑에 '안전그물([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/))'이 쳐져 있다는 걸 100% 믿을 때만, 공중그네에서 몸을 던지는 화려한 묘기(혁신적인 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/))를 부릴 수 있다. 안전그물이 없으면 무서워서 아무것도 못 하고 제자리에 멈춰있게 된다.

---

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/), 배포 파이프라인의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/), 배포 파이프라인은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/), 배포 파이프라인 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/), 배포 파이프라인에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    |
    v
CI/CD 지속적 통합, 배포 파이프라인 개념 정립
    |
    v
표준화 및 방법론 체계화 (ISO, CMMI, Agile)
    |
    v
클라우드 네이티브·AI 기반 확장 적용
    |
    v
지속적 개선 및 DevOps·MLOps 통합
```

이 흐름은 [소프트웨어 위기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 -> 체계적 방법론 개발 -> 표준화 -> 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/), 배포 파이프라인은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 818 / 973

<- **이전**: [650. CI/CD 지속적 통합, 배포 파이프라인](/knowledge-base/studynote/04_software_engineering/uncategorized/650_ci_cd_pipeline/)
**다음**: [651. 카나리 배포 / 블루-그린 배포 무중단](/knowledge-base/studynote/04_software_engineering/uncategorized/651_canary_blue_green_deployment/) ->

---
