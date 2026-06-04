+++
title = "70. 빌드 도구 (Build Tools) - Maven, Gradle (Java), npm (Node.js)"
date = 2026-04-10

[taxonomies]
tags = ["studynote-devops"]

[extra]
tags = ["studynote-devops"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 빌드 도구는 소스 코드 컴파일, 의존성 관리, 패키징, 테스트를 자동화하는 도구다.
> 2. **가치**: Maven, Gradle, npm은 각각 Java/Node 생태계의 표준 빌드·패키지 관리 도구다.
> 3. **판단**: 빌드 속도, 의존성 선언 방식, 확장성 차이를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

수동으로 빌드하면 실수가 많다. 빌드 도구는 이 과정을 반복 가능하게 만든다.

그래서 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD의 기본 구성요소가 된다.

- **📢 섹션 요약 비유**: 레시피대로 자동으로 요리를 해 주는 주방이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Source
  v
Build Tool
  v
Artifact
  v
Deploy
```

| 도구 | 특징 |
| :-- | :-- |
| Maven | 선언적, 표준화 |
| Gradle | 유연, 빠름 |
| npm | JS 생태계 중심 |

빌드 도구는 의존성을 받고, 테스트를 돌리고, 배포 산출물을 만든다.

- **📢 섹션 요약 비유**: 재료를 모아 요리를 완성하는 기계다.

---

## Ⅲ. 비교 및 연결

| 도구 | 장점 | 단점 |
| :-- | :-- | :-- |
| Maven | 규칙 명확 | 유연성 낮음 |
| Gradle | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)/유연성 | 학습 곡선 |
| npm | JS 친화 | 의존성 복잡 |

| 기능 | 의미 |
| :-- | :-- |
| [Dependency Management](/knowledge-base/studynote/09_security/uncategorized/1042_dependency_management/) | [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 관리 |
| Build Lifecycle | 빌드 단계 |
| Script | 자동화 |

빌드 도구는 언어 생태계에 맞게 선택해야 한다.

- **📢 섹션 요약 비유**: 같은 요리라도 주방 도구가 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 의존성 선언이 명확한가?
2. 빌드 재현성이 있는가?
3. 테스트가 자동화되는가?
4. CI와 연결되는가?
5. 도구 선택이 생태계에 맞는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 수동 빌드를 반복하는 설계
- [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 고정 없이 의존성을 쓰는 설계
- 도구별 특성을 무시하는 설계
- 빌드와 테스트를 분리하지 않는 설계

기술사 관점에서는 빌드 도구를 "자동화된 산출물 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)기"로 설명해야 한다.

- **📢 섹션 요약 비유**: 레시피대로 매번 같은 맛을 내는 주방장이다.

---

## Ⅴ. 기대효과 및 결론

빌드 도구를 잘 쓰면 반복 작업이 줄고 품질이 안정된다.

결론적으로 빌드 도구는 빌드와 패키징을 자동화하는 핵심 도구다.

- **📢 섹션 요약 비유**: 재료만 넣으면 완성품을 만들어 주는 기계다.

---

## 관련 개념 맵

```text
Source
  v
Build Tool
  v
Artifact
  v
CI/CD
```

---

## 관련 키워드 및 발전 흐름도

```text
Maven / Gradle / npm
  v
Build Tool
  v
Dependency Management
  v
CI/CD
```

---

## 어린이를 위한 3줄 비유 설명

재료를 넣으면 요리가 돼요.
자동으로 만들어 주는 거예요.
빌드 도구는 그런 도구예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 70 / 373

<- **이전**: [69. 커밋 메시지 컨벤션 - feat, fix, docs 등 접두어 표준화](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/069_commit_message_convention_feat_fix/)
**다음**: [71. 젠킨스 (Jenkins) - 오픈소스 CI/CD 자동화 빌드 서버](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/) ->

---
