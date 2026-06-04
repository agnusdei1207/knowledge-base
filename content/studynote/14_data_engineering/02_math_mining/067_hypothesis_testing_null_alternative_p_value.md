+++
title = "67. 가설 검정 - 귀무 가설(H0) vs 대립 가설(H1)"
date = 2026-04-10

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 가설 검정은 표본을 이용해 귀무 가설(H0)을 기각할지 판단하는 통계 절차다.
> 2. **가치**: [p-value](/knowledge-base/studynote/06_ict_convergence/05_data_science/337_p_value_significance/), 유의수준, 검정력을 함께 봐야 판단이 의미 있다.
> 3. **판단**: H0를 증명하는 것이 아니라, H1을 지지할 만큼 H0를 기각할 수 있는지 본다.

---

## Ⅰ. 개요 및 필요성

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 우연인지 실제 효과인지 구분하려면 검정이 필요하다. 가설 검정은 이런 불확실성을 정량화한다.

그래서 실험, 품질 관리, A/B 테스트에 널리 쓰인다.

- **📢 섹션 요약 비유**: 누가 더 빠른지 달리기 기록으로 판정하는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
H0 / H1
  ↓
Test Statistic
  ↓
p-value
  ↓
Decision
```

| 항목 | 의미 |
| :-- | :-- |
| H0 | 차이 없음 |
| H1 | 차이 있음 |
| [p-value](/knowledge-base/studynote/06_ict_convergence/05_data_science/337_p_value_significance/) | H0 하에서의 희귀도 |
| α | 기각 기준 |

가설 검정은 "우연이라고 보기엔 너무 드문가?"를 묻는 과정이다.

- **📢 섹션 요약 비유**: 이상한 일이 얼마나 드문지 따지는 탐정이다.

---

## Ⅲ. 비교 및 연결

| 개념 | 의미 |
| :-- | :-- |
| H0 | 기본 가정 |
| H1 | 대안 가정 |
| [p-value](/knowledge-base/studynote/06_ict_convergence/05_data_science/337_p_value_significance/) | 관측치의 희귀도 |
| [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) | 진짜 효과를 잡는 힘 |

| 오류 | 의미 |
| :-- | :-- |
| Type I | 참인데 기각 |
| Type II | 거짓인데 기각 실패 |

가설 검정은 두 오류 사이의 균형을 정하는 일이다.

- **📢 섹션 요약 비유**: 억울하게 잡을지, 놓칠지 사이에서 기준을 정하는 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. H0/H1이 명확한가?
2. 유의수준을 정했는가?
3. p-value를 올바르게 해석하는가?
4. 검정력과 표본 수를 봤는가?
5. 오류 유형을 설명할 수 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- p-value를 효과 크기로 착각하는 설계
- H0를 참이라고 증명하려는 설계
- 표본 수를 무시하는 설계
- 검정 방법 선택을 막연히 하는 설계

기술사 관점에서는 가설 검정을 "판정 도구"가 아니라 "불확실성 절차"로 이해해야 한다.

- **📢 섹션 요약 비유**: 의심이 충분히 작아질 때만 결론을 내린다.

---

## Ⅴ. 기대효과 및 결론

가설 검정을 이해하면 실험과 분석에서 결론을 더 신뢰할 수 있다. 그래서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 의사결정의 기본이 된다.

결론적으로 가설 검정은 귀무 가설을 기각할지 판단하는 통계 절차다.

- **📢 섹션 요약 비유**: 우연인지 아닌지 기준선을 정하는 일이다.

---

## 관련 개념 맵

```text
H0 / H1
  ↓
Test Statistic
  ↓
p-value
  ↓
Decision
```

---

## 관련 키워드 및 발전 흐름도

```text
Hypothesis
  ↓
Hypothesis Testing
  ↓
p-value / Alpha
  ↓
Statistical Decision
```

---

## 어린이를 위한 3줄 비유 설명

정말 우연인지 물어보는 거예요.
기준선을 넘으면 기각해요.
가설 검정은 그런 판정이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 67 / 258

← **이전**: [66. 스피어만 순위 상관 계수 (Spearman Rank Correlation)](/knowledge-base/studynote/14_data_engineering/02_math_mining/066_spearman_rank_correlation_nonparametric_robustness/)
**다음**: [68. 유의 수준(Alpha)과 유의 확률(p-value) - 귀무 가설 기각의 마지노선](/knowledge-base/studynote/14_data_engineering/02_math_mining/068_significance_level_alpha_p_value_hypothesis/) →

---
