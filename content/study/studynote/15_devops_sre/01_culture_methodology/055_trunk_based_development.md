+++
weight = 55
title = "55. Trunk-Based Development"
date = "2026-05-01"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Trunk-Based Development는 메인 트렁크에 자주 통합하는 브랜치 [[268_strategy_pattern|전략]]이다.
> 2. **가치**: 짧은 브랜치와 작은 변경으로 충돌과 통합 비용을 줄인다.
> 3. **판단 포인트**: feature flag와 자동화된 CI가 없으면 운영하기 어렵다.

---

## Ⅰ. 개요 및 필요성

대규모 브랜치를 오래 끌고 가면 통합이 어려워진다. Trunk-Based Development는 이를 피하기 위해 메인 브랜치 중심으로 짧게 작업한다.

빠른 피드백과 잦은 병합이 핵심이다.

- **📢 섹션 요약 비유**: Trunk-Based Development는 모두가 같은 길을 자주 오가며 합류하는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

개발자는 짧은 feature branch를 만들거나 직접 trunk에 작은 변경을 자주 넣는다. 메인 브랜치는 항상 배포 가능한 상태를 유지한다.

```text
trunk/main ─●─●─●─●─●
             \ \ \ \ \
              feature branches
```

| 요소 | 역할 | 포인트 |
| :--- | :--- | :--- |
| Trunk | 메인 라인 | 항상 안정 |
| Short-lived branch | 짧은 작업 | 빠른 merge |
| [[576_feature_flag_ab_testing_rollout|Feature flag]] | 기능 분리 | 미완성 숨김 |
| [[090_configuration_item|CI]] | 자동 [[395_verification_process_review|검증]] | 빠른 피드백 |

핵심은 통합을 미루지 않는 것이다. 미루면 충돌과 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]가 커진다.

- **📢 섹션 요약 비유**: Trunk-Based는 매일 책상 위를 정리하는 습관이다.

---

## Ⅲ. 비교 및 연결

GitFlow보다 가볍고, GitHub Flow보다 더 엄격한 trunk 중심 운영이라고 볼 수 있다. DevOps와 빠른 배포에 잘 맞는다.

| 항목 | [[053_gitflow|GitFlow]] | [[054_github_flow|GitHub Flow]] | Trunk-Based |
| :--- | :--- | :--- | :--- |
| 브랜치 수명 | 길다 | 짧다 | 매우 짧다 |
| 통합 빈도 | 낮음 | 높음 | 매우 높음 |
| [[576_feature_flag_ab_testing_rollout|feature flag]] | 선택적 | 권장 | 사실상 필수 |

Trunk-Based는 테스트 자동화와 배포 자동화가 성숙할수록 효과가 커진다.

- **📢 섹션 요약 비유**: Trunk-Based는 모두가 본선에 자주 합류하는 고속도로 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 변경 크기를 작게 유지하고, [[090_configuration_item|CI]] 실패 시 빠르게 되돌린다. feature flag를 통해 배포와 공개를 분리하는 것이 중요하다.

### [[435_checklist_based_testing|체크리스트]]

1. trunk가 항상 배포 가능한가?
2. 변경이 작고 짧은가?
3. feature flag를 쓰는가?
4. CI가 빠르게 피드백하는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 긴 feature branch를 오래 유지하는 경우
- trunk가 깨진 채 방치되는 경우
- 자동화 없이 trunk만 강조하는 경우

기술사 관점에서는 Trunk-Based Development가 빠른 통합과 낮은 충돌을 위한 운영 규칙이라는 점을 설명해야 한다.

- **📢 섹션 요약 비유**: Trunk-Based는 공용 책상에 자주 정리해 올려 놓는 방식이다.

---

## Ⅴ. 기대효과 및 결론

Trunk-Based Development는 빠른 통합, 낮은 충돌, 지속 배포에 유리하다. 작은 변경을 자주 합치는 문화가 핵심이다.

정리하면, 브랜치를 오래 끌지 말고 trunk에 자주 합쳐야 한다.

- **📢 섹션 요약 비유**: Trunk-Based는 같은 도로를 자주 정리하며 달리는 방식이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| trunk | 메인 브랜치 |
| short-lived branch | 짧은 작업 |
| [[576_feature_flag_ab_testing_rollout|feature flag]] | 미완성 숨김 |
| [[090_configuration_item|CI]] | 자동 [[395_verification_process_review|검증]] |
| merge | 잦은 통합 |

### 📈 관련 키워드 및 발전 흐름도

```text
긴 브랜치
    │
    ▼
짧은 브랜치
    │
    ▼
자주 병합
    │
    ▼
Trunk-Based + Feature Flag
```

이 흐름은 느슨한 분기에서 빠른 통합 중심으로의 변화를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Trunk-Based는 한 큰 길로 자주 모이는 거예요.
2. 오래 돌아다니지 않고 빨리 합류해요.
3. 그래서 서로 덜 부딪혀요.
