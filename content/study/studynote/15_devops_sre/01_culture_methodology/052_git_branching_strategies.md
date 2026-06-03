+++
weight = 52
title = "52. Git 브랜치 전략 (Git Branching Strategies)"
date = "2026-05-01"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Git 브랜치 [[268_strategy_pattern|전략]]은 여러 개발자가 한 저장소에서 안전하게 [[430_index_fast_full_scan|병렬]] 작업하기 위해 합의한 브랜치 운영 규칙이다.
> 2. **가치**: [[053_gitflow|GitFlow]], [[054_github_flow|GitHub Flow]], Trunk-Based Development는 릴리스 주기와 팀 규모에 따라 선택이 달라진다.
> 3. **판단 포인트**: 브랜치가 길어질수록 충돌이 늘고 배포가 늦어진다. 짧은 브랜치와 자주 병합이 핵심이다.

---

## Ⅰ. 개요 및 필요성

브랜치 [[268_strategy_pattern|전략]]이 없으면 각자 다른 방향으로 개발하다가 합칠 때 충돌이 폭발한다. 브랜치 [[268_strategy_pattern|전략]]은 언제 브랜치를 만들고, 언제 병합하고, 언제 삭제할지 정하는 협업 규칙이다.

Git은 브랜치를 싸게 만들 수 있으므로, [[268_strategy_pattern|전략]]만 있으면 [[430_index_fast_full_scan|병렬]] 개발과 안정 배포를 둘 다 잡을 수 있다.

- **📢 섹션 요약 비유**: 브랜치 [[268_strategy_pattern|전략]]은 공용 주방의 정리 규칙과 같다. 각자 요리하되, 마지막에는 같은 접시에 예쁘게 담아야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

대표 [[268_strategy_pattern|전략]]은 [[053_gitflow|GitFlow]], [[054_github_flow|GitHub Flow]], Trunk-Based Development다. 각각 릴리스 중심, 단순 배포 중심, 초단기 병합 중심으로 나뉜다.

```text
┌──────────────────────────────────────────────────────────────┐
│                Branch Strategy Landscape                    │
├──────────────────────────────────────────────────────────────┤
│ GitFlow → develop / feature / release / hotfix             │
│ GitHub Flow → main / feature                                │
│ Trunk-Based → main 중심 + short-lived branch + feature flag │
└──────────────────────────────────────────────────────────────┘
```

| [[268_strategy_pattern|전략]] | 특징 | 적합한 환경 |
| :--- | :--- | :--- |
| [[053_gitflow|GitFlow]] | 릴리스 브랜치가 많음 | 정기 릴리스, 대형 조직 |
| [[054_github_flow|GitHub Flow]] | 단순하고 짧음 | 웹 [[090_service_kubernetes_network_load_balancing|서비스]], 빠른 배포 |
| Trunk-Based | 메인 중심, 매우 짧음 | 고빈도 배포, [[652_devops_calms_culture|DevOps]] |

브랜치 병합에서는 merge와 rebase를 구분해야 한다. merge는 히스토리를 보존하고, rebase는 히스토리를 선형으로 정리한다. 협업에서 공개된 커밋을 rebase하는 것은 주의가 필요하다.

- **📢 섹션 요약 비유**: merge는 사진첩에 새 [[286_page_frame|페이지]]를 붙이는 것이고, rebase는 사진을 시간순으로 다시 [[055_array|배열]]하는 것이다.

---

## Ⅲ. 비교 및 연결

브랜치 [[268_strategy_pattern|전략]]은 팀 특성에 따라 달라진다. 규제가 강하고 릴리스 주기가 길면 GitFlow가 맞고, 작은 팀과 빠른 배포면 GitHub Flow가 잘 맞으며, [[652_devops_calms_culture|DevOps]] 성숙도가 높으면 Trunk-Based가 강하다.

| 항목 | [[053_gitflow|GitFlow]] | [[054_github_flow|GitHub Flow]] | Trunk-Based |
| :--- | :--- | :--- | :--- |
| 브랜치 수 | 많음 | 적음 | 매우 적음 |
| 병합 주기 | 길다 | 짧다 | 매우 짧다 |
| 운영 복잡도 | 높음 | 낮음 | 중간 |
| 배포 속도 | 느림 | 빠름 | 매우 빠름 |

브랜치 [[268_strategy_pattern|전략]]은 [[090_configuration_item|CI]]/CD와 [[576_feature_flag_ab_testing_rollout|피처 플래그]]와도 연결된다. 특히 Trunk-Based는 feature flag와 함께 써야 메인 브랜치를 자주 병합하면서도 배포 위험을 낮출 수 있다.

- **📢 섹션 요약 비유**: GitFlow는 출입문이 많은 큰 아파트, GitHub Flow는 단순한 원룸, Trunk-Based는 하나의 넓은 방을 계속 정리하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 팀 규모, 릴리스 빈도, 규제 수준, [[098_rollback_strategy_pipeline_error_threshold|롤백]] 난이도를 기준으로 [[268_strategy_pattern|전략]]을 고른다. 또한 브랜치 이름 규칙, [[067_pull_request_pr_merge_request_code_review|PR]] 크기, [[330_code_review|코드 리뷰]], 자동 테스트를 같이 정해야 한다.

### [[435_checklist_based_testing|체크리스트]]

1. 릴리스 주기가 짧은가 긴가?
2. 브랜치 수명이 짧은가?
3. 메인 브랜치가 항상 배포 가능 상태인가?
4. feature flag와 [[090_configuration_item|CI]]/CD가 연결되어 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 장수 브랜치를 오래 끌고 가는 경우
- 메인에 직접 대규모 커밋을 넣는 경우
- 브랜치 [[268_strategy_pattern|전략]] 없이 사람 감으로만 운영하는 경우

기술사 관점에서는 브랜치 [[268_strategy_pattern|전략]]이 단순 Git 사용법이 아니라 배포 거버넌스라는 점을 설명해야 한다. 협업 안정성과 배포 빈도를 함께 보아야 한다.

- **📢 섹션 요약 비유**: 브랜치 [[268_strategy_pattern|전략]]은 교통 체계와 같다. 차선이 없으면 다 부딪히고, 규칙이 있으면 막히지 않는다.

---

## Ⅴ. 기대효과 및 결론

좋은 브랜치 [[268_strategy_pattern|전략]]은 충돌을 줄이고 배포를 빠르게 하며, [[058_dx_developer_experience|개발자 경험]]을 높인다. 팀이 작을수록 단순한 [[268_strategy_pattern|전략]]이 유리하고, 팀이 커질수록 규칙과 자동화가 중요해진다.

결국 핵심은 "브랜치를 얼마나 오래 살릴 것인가"다. 짧고 자주 합치는 습관이 가장 안전하다.

- **📢 섹션 요약 비유**: 브랜치 [[268_strategy_pattern|전략]]은 빨래를 오래 쌓아두지 않고 자주 개는 것과 같다. 오래 쌓을수록 엉킨다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| merge | 히스토리 보존 |
| rebase | 선형 히스토리 |
| [[576_feature_flag_ab_testing_rollout|feature flag]] | Trunk-Based 보완 |
| [[090_configuration_item|CI]]/CD | 브랜치 [[268_strategy_pattern|전략]]과 배포 연결 |
| [[067_pull_request_pr_merge_request_code_review|PR]] / [[330_code_review|Code Review]] | 협업 품질 통제 |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 trunk 개발
    │
    ▼
GitFlow
    │
    ▼
GitHub Flow
    │
    ▼
Trunk-Based + Feature Flag
```

이 흐름은 브랜치가 길고 무거운 구조에서 짧고 자동화된 구조로 진화한 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 브랜치는 각자 숙제하는 작은 책상이에요.
2. 숙제는 따로 해도, 마지막엔 한 책상에 깨끗하게 모아야 해요.
3. 그래서 규칙이 있으면 친구들과 같이 작업해도 덜 싸워요.
