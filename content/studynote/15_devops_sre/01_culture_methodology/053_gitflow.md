+++
title = "53. GitFlow"
date = 2026-05-01

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GitFlow는 `main`, `develop`, `feature`, `release`, `hotfix` 브랜치를 구분하는 전통적인 브랜치 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.
> 2. **가치**: 명확한 릴리스 흐름과 긴 안정화 기간이 필요한 조직에 적합하다.
> 3. **판단 포인트**: 구조가 명확한 대신 복잡도가 높다. 빠른 배포 환경에서는 과할 수 있다.

---

## Ⅰ. 개요 및 필요성

GitFlow는 릴리스와 개발을 분리해 운영하는 방식이다. 여러 기능을 동시에 개발하면서도 안정된 릴리스를 유지하려는 목적에서 널리 쓰였다.

특히 정기 릴리스, 승인 절차, 핫픽스 대응이 필요한 환경에서 이해하기 쉽다.

- **📢 섹션 요약 비유**: GitFlow는 공사 중인 건물과 입주 가능한 건물을 따로 나누어 관리하는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

GitFlow는 `develop`에서 기능을 모으고, `release`에서 안정화하고, `main`에 태그를 남긴다. 긴급 수정은 `hotfix`로 바로 `main`에 반영한다.

```text
feature → develop → release → main
                   ↘ hotfix → main
```

| 브랜치 | 역할 | 특징 |
| :--- | :--- | :--- |
| main | 운영 배포 | 항상 안정 |
| develop | 통합 개발 | 다음 릴리스 준비 |
| feature | 기능 개발 | 짧게 유지 |
| release | 안정화 | 버그 수정 |
| hotfix | 긴급 패치 | 즉시 반영 |

핵심은 개발과 배포의 경계를 분명히 하는 것이다. 이 구조 덕분에 릴리스 품질은 높아지지만, 브랜치가 많아져 관리 부담이 커진다.

- **📢 섹션 요약 비유**: GitFlow는 출발선, 중간 점검소, 결승선을 따로 둔 마라톤 코스다.

---

## Ⅲ. 비교 및 연결

GitFlow는 GitHub Flow나 Trunk-Based보다 구조가 무겁다. 대신 릴리스 제어와 분기가 명확하다.

| 항목 | GitFlow | [GitHub Flow](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/054_github_flow/) | Trunk-Based |
| :--- | :--- | :--- | :--- |
| 브랜치 수 | 많음 | 적음 | 매우 적음 |
| 릴리스 방식 | 계획형 | 연속형 | 초연속형 |
| 운영 복잡도 | 높음 | 낮음 | 중간 |

GitFlow는 배포 승인과 릴리스 노트가 중요한 조직에 잘 맞는다. 반대로 빠른 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD가 목표라면 과한 구조가 될 수 있다.

- **📢 섹션 요약 비유**: GitFlow는 여러 개의 출구가 있는 고속도로, GitHub Flow는 한 개의 빠른 직진로다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 브랜치 이름, 머지 규칙, 릴리스 태그, 핫픽스 절차를 정해야 한다. 특히 `develop`과 `main`의 역할을 혼동하면 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 무너진다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. feature/release/hotfix 규칙이 문서화되어 있는가?
2. 릴리스 태그와 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리가 연결되는가?
3. hotfix가 신속하게 main에 반영되는가?
4. 브랜치 수명과 머지 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 관리되는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모든 작업을 develop에 오래 쌓아두는 경우
- release 브랜치를 무한히 끌고 가는 경우
- GitFlow를 쓰면서도 규칙을 지키지 않는 경우

기술사 관점에서는 GitFlow가 단순한 Git 기능이 아니라 릴리스 거버넌스라는 점을 설명해야 한다. 팀의 배포 리듬과 승인 절차가 핵심이다.

- **📢 섹션 요약 비유**: GitFlow는 교실에서 예습, 본수업, 시험, 보충수업을 따로 나누는 방식이다.

---

## Ⅴ. 기대효과 및 결론

GitFlow는 안정적 릴리스와 명확한 협업 구조를 제공한다. 하지만 속도와 단순함이 중요한 팀에는 부담이 될 수 있다.

정리하면, GitFlow는 통제와 안정이 중요한 조직에서 강한 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

- **📢 섹션 요약 비유**: GitFlow는 줄 서는 규칙이 엄격한 놀이공원 입장 시스템이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| main | 운영 브랜치 |
| develop | 통합 브랜치 |
| feature | 기능 개발 |
| release | 안정화 |
| hotfix | 긴급 수정 |

### 📈 관련 키워드 및 발전 흐름도

```text
feature branch
    │
    ▼
develop
    │
    ▼
release
    │
    ▼
main / hotfix
```

이 흐름은 계획된 릴리스와 긴급 수정이 분리된 전통적 브랜치 운영을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. GitFlow는 숙제한 종이를 종류별로 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 나눠 넣는 거예요.
2. 새 숙제는 따로 모으고, 시험 전에 한 번 더 정리해요.
3. 급한 수정은 바로 완성본 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 넣어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 53 / 373

← **이전**: [52. Git 브랜치 전략 (Git Branching Strategies)](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/052_git_branching_strategies/)
**다음**: [54. GitHub Flow](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/054_github_flow/) →

---
