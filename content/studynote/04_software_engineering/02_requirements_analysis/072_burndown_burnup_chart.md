+++
title = "72. 번다운 차트 (Burndown Chart) / 번업 차트 (Burnup Chart)"

[taxonomies]
tags = ["software_engineering"]

[extra]
tags = ["software_engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 번다운/번업 차트는 [스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/)나 프로젝트의 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)을 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)하는 [애자일 관리](/knowledge-base/studynote/12_it_management/01_governance_strategy/033_agile_management/) 도구다.
> 2. **가치**: 진척과 범위 변화를 한눈에 보여 준다.
> 3. **판단**: 번다운은 남은 일감, 번업은 완료량과 범위를 함께 본다.

---

## Ⅰ. 개요 및 필요성

프로젝트의 흐름을 숫자만으로 보면 감이 안 온다. 차트는 이를 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)한다.

그래서 팀과 이해관계자가 같은 그림을 본다.

- **📢 섹션 요약 비유**: 장작이 얼마나 남았는지 눈으로 보는 현황판이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Burndown: Remaining Work v
Burnup: Completed Work ^ + Scope
```

| 차트 | 의미 |
| :-- | :-- |
| Burndown | 남은 작업 감소 |
| Burnup | 완료 작업 증가 |
| [Scope](/knowledge-base/studynote/09_security/05_web_app_security/512_oauth_scope/) Line | 범위 변화 |

번다운은 남은 일을 줄여 나가는 관점이고, 번업은 완료와 범위 변화를 함께 본다.

- **📢 섹션 요약 비유**: 장작을 태우는지, 이미 태운 양을 보는지의 차이다.

---

## Ⅲ. 비교 및 연결

| 구분 | Burndown | Burnup |
| :-- | :-- | :-- |
| 관점 | 남은 일감 | 완료량 |
| 범위 변화 | 간접 | 직접 |
| 사용 | [스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/) 추적 | 범위 관리 |

| 효과 | 의미 |
| :-- | :-- |
| Visibility | 가시성 |
| Forecast | 예측 |

차트는 일정/범위/속도의 관계를 보여 주어 조기 경고를 가능하게 한다.

- **📢 섹션 요약 비유**: 불이 얼마나 줄었고, 얼마나 더 태울지 보여 주는 지도다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 남은 일감과 완료량을 구분하는가?
2. 범위 변화를 표시하는가?
3. 팀이 같은 지표를 보는가?
4. 예측에 활용하는가?
5. 단순 보고용이 아닌가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 숫자만 있고 해석이 없는 설계
- 번다운과 번업을 혼동하는 설계
- 범위 변경을 숨기는 설계
- 팀이 보지 않는 대시보드

기술사 관점에서는 번다운/번업 차트를 "[애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 도구"로 설명해야 한다.

- **📢 섹션 요약 비유**: 남은 장작과 태운 장작을 같이 보는 판이다.

---

## Ⅴ. 기대효과 및 결론

차트는 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 상황을 빠르게 공유하고 위험을 조기에 발견하게 한다.

결론적으로 번다운/번업 차트는 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 진척 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 도구다.

- **📢 섹션 요약 비유**: 일감이 줄어드는지 한눈에 보는 표다.

---

## 관련 개념 맵

```text
Sprint
  v
Burndown / Burnup
  v
Visibility
  v
Forecasting
```

---

## 관련 키워드 및 발전 흐름도

```text
Agile
  v
Burndown
  v
Burnup
  v
Progress Tracking
```

---

## 어린이를 위한 3줄 비유 설명

일감이 줄어드는지 봐요.
끝난 일도 같이 봐요.
차트는 그런 그림이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 72 / 973

<- **이전**: [71. 스프린트 회고 (Sprint Retrospective) - 프로세스 개선](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/071_sprint_retrospective/)
**다음**: [73. XP (e/Xtreme Programming) - 5가지 가치, 12가지 실천 방법](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/073_xp_extreme_programming/) ->

---
