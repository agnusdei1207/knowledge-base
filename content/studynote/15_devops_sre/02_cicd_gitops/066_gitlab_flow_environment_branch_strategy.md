---
title: "066. Gitlab Flow Environment Branch Strategy"
date: "2026-04-10"
tags:
  - "studynote-devops"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GitLab Flow는 main과 환경 브랜치(dev/staging/prod 등)를 연결해 배포 흐름을 명확히 하는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.
> 2. **가치**: 환경별 승격(promote) 흐름이 분명해 운영과 릴리스 관리가 쉬워진다.
> 3. **판단**: GitFlow와 GitHub Flow의 중간 성격을 가지며, 환경 중심 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD에 잘 맞는다.

---

## Ⅰ. 개요 및 필요성

배포 환경이 여러 개면 "어느 브랜치가 어느 환경인지"가 중요해진다. GitLab Flow는 이 문제를 해결하기 위해 환경 브랜치 개념을 쓴다.

개발, [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 운영을 브랜치와 연결하면 릴리스 상태를 명확하게 추적할 수 있다.

- **📢 섹션 요약 비유**: 완성도에 따라 장난감을 dev 방, 테스트 방, 전시 방으로 옮겨 두는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
feature -> main -> dev -> staging -> prod
```

| 브랜치 | 의미 |
| :-- | :-- |
| main | [기준선](/studynote/04_software_engineering/01_overview_principles/025_baseline/) |
| dev | 개발 환경 |
| staging | 사전 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| prod | 운영 반영 |

GitLab Flow는 환경 승격을 명시적으로 표현한다. 그래서 "어떤 커밋이 지금 어느 환경에 있는지"를 추적하기 쉽다.

- **📢 섹션 요약 비유**: 물건을 방에서 방으로 옮길 때 라벨을 붙여 두는 것과 같다.

---

## Ⅲ. 비교 및 연결

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 특징 | 강점 | 한계 |
| :-- | :-- | :-- | :-- |
| [GitHub Flow](/studynote/15_devops_sre/01_culture_methodology/054_github_flow/) | 단순 | 빠른 CD | 환경 표현 약함 |
| GitLab Flow | 환경 중심 | 추적 쉬움 | 브랜치 관리 필요 |
| Git Flow | 브랜치 많음 | 릴리스 제어 | 복잡함 |

GitLab Flow는 환경 브랜치가 중요한 조직에 잘 맞는다. 단순한 기능 브랜치보다 운영 흐름이 더 중요한 경우 유리하다.

- **📢 섹션 요약 비유**: 같은 물건이라도 전시실, 보관실, 수리실을 나눠 두면 관리가 쉬워진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 환경별 브랜치/배포 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 있는가?
2. 승격 순서가 명확한가?
3. [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)과 승인 절차가 있는가?
4. [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD와 연결되어 있는가?
5. 브랜치 폭증을 관리하는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 환경과 브랜치를 무관하게 두는 설계
- dev/staging/prod 승격을 문서로만 남기는 설계
- 배포 기록이 남지 않는 설계
- GitHub Flow와 GitLab Flow를 혼동하는 설계

기술사 관점에서는 GitLab Flow를 환경 중심 배포 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 보고, 운영 통제와 릴리스 추적성을 강조해야 한다.

- **📢 섹션 요약 비유**: 어느 방에 있는지 알 수 있어야 찾기도 쉽고 옮기기도 쉽다.

---

## Ⅴ. 기대효과 및 결론

GitLab Flow는 환경 승격과 배포 추적을 단순화한다. 그래서 기업용 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD에서 실용적이다.

결론적으로 GitLab Flow는 환경 브랜치를 중심으로 한 배포 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

- **📢 섹션 요약 비유**: 물건이 어디까지 갔는지 표를 붙여 놓는 것이다.

---

## 관련 개념 맵

```text
feature
  v
main
  v
dev / staging / prod
  v
Deployment Traceability
```

---

## 관련 키워드 및 발전 흐름도

```text
GitHub Flow
  v
GitLab Flow
  v
Environment Branching
  v
CI/CD
```

---

## 어린이를 위한 3줄 비유 설명

장난감을 방마다 옮겨요.
어느 방에 있는지 라벨을 붙여요.
GitLab Flow는 그런 환경별 배치 방법이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 66 / 373

<- **이전**: [65. GitHub Flow - 극단적 단순화 브랜치 전략과 CD](/studynote/15_devops_sre/02_cicd_gitops/065_github_flow_branch_strategy/)
**다음**: [67. Pull Request (PR) - 머지 리퀘스트 및 코드 리뷰 프로세스](/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) ->

---
