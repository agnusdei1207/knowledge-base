---
title: 73. XP (e/Xtreme Programming) - 5가지 가치, 12가지 실천 방법
tags:
- software_engineering
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: XP는 코딩 품질과 고객 피드백을 극대화하는 [[004_agile_relation|애자일]] 개발 방법론이다.
> 2. **가치**: 5가지 가치와 12가지 실천이 기술 중심 개발 문화를 만든다.
> 3. **판단**: [[164_tdd_test_driven_development|TDD]], 짝 프로그래밍, CI가 핵심 실천이다.

---

## Ⅰ. 개요 및 필요성

코드를 잘 만드는 방법이 따로 필요하다. XP는 그 답을 제시한다.

그래서 [[004_agile_relation|애자일]]의 실천 축으로 중요하다.

- **📢 섹션 요약 비유**: 운동 선수의 기본기 훈련 같은 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Values
  ↓
Practices
  ↓
High-quality Code
```

| 가치 | 의미 |
| :-- | :-- |
| Communication | 소통 |
| [[014_simplicity|Simplicity]] | 단순성 |
| Feedback | 피드백 |
| Courage | 용기 |
| Respect | 존중 |

XP는 5가지 가치 위에 12가지 실천을 얹어 품질을 높인다.

- **📢 섹션 요약 비유**: 기본 체력과 훈련 메뉴를 같이 챙기는 것이다.

---

## Ⅲ. 비교 및 연결

| 실천 | 의미 |
| :-- | :-- |
| [[164_tdd_test_driven_development|TDD]] | 테스트 먼저 |
| [[074_pair_programming_driver_navigator|Pair Programming]] | 짝 프로그래밍 |
| [[090_configuration_item|CI]] | [[076_ci_continuous_integration|지속적 통합]] |

| 특징 | 설명 |
| :-- | :-- |
| [[026_three_c_analysis|Customer]] Feedback | 빠른 [[395_verification_process_review|검증]] |
| [[078_refactoring_code_smells|Refactoring]] | 개선 |

XP는 스크럼보다 개발 실천에 더 깊게 들어간다.

- **📢 섹션 요약 비유**: 팀 훈련보다 기술 훈련에 더 집중하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. TDD를 실천하는가?
2. 짝 프로그래밍을 활용하는가?
3. CI가 붙어 있는가?
4. 리팩토링을 지속하는가?
5. 고객 피드백을 받는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 가치 없이 실천만 외우는 설계
- TDD와 단순 테스트를 혼동하는 설계
- 짝 프로그래밍을 형식으로만 보는 설계
- [[090_configuration_item|CI]] 없이 XP를 말하는 설계

기술사 관점에서는 XP를 "기술 실천 중심 [[004_agile_relation|애자일]]"로 설명해야 한다.

- **📢 섹션 요약 비유**: 좋은 코드 습관을 매일 반복하는 훈련이다.

---

## Ⅴ. 기대효과 및 결론

XP는 품질과 피드백 속도를 높인다.

결론적으로 XP는 개발 실천을 극한까지 끌어올린 [[004_agile_relation|애자일]] 방법론이다.

- **📢 섹션 요약 비유**: 기본기를 끝까지 다듬는 방식이다.

---

## 관련 개념 맵

```text
Values
  ↓
XP Practices
  ↓
TDD / Pair Programming / CI
```

---

## 관련 키워드 및 발전 흐름도

```text
Agile
  ↓
XP
  ↓
TDD / CI / Pair Programming
```

---

## 어린이를 위한 3줄 비유 설명

코드를 잘 쓰는 연습이에요.  
친구와 같이 쓰기도 해요.  
XP는 그런 방법이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 73 / 973

← **이전**: [[072_burndown_burnup_chart|72. 번다운 차트 (Burndown Chart) / 번업 차트 (Burnup Chart)]]
**다음**: [[074_pair_programming_driver_navigator|74. 페어 프로그래밍 (Pair Programming) - Driver / Navigator]] →

---
