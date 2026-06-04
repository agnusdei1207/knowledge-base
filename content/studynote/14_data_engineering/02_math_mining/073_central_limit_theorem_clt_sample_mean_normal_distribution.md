---
title: "73. 중심 극한 정리 (CLT) - 30개 표본 정규분포 마법"
date: "2026-04-10"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [중심 극한 정리](/studynote/08_algorithm_stats/08_stats/139_clt/)는 표본 수가 충분히 크면 표본평균의 분포가 정규분포에 가까워진다는 정리다.
> 2. **가치**: 통계 추론의 핵심 기반이다.
> 3. **판단**: 모집단 분포가 정규가 아니어도 표본평균은 정규에 가까워질 수 있다.

---

## Ⅰ. 개요 및 필요성

복잡한 모집단을 직접 다루기 어려울 때 표본평균을 본다.

CLT는 그 표본평균을 정규분포로 다룰 수 있게 해 준다.

- **📢 섹션 요약 비유**: 여러 조각을 모으면 전체 모양이 비슷해지는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Population
  v sample means
Approximately Normal
```

| 요소 | 의미 |
| :-- | :-- |
| Sample Mean | 표본평균 |
| Normal Approximation | 정규 근사 |
| Standard Error | 표준오차 |

표본 수가 커질수록 표본평균 분포는 평균 주위로 정규형태에 가까워진다.

- **📢 섹션 요약 비유**: 작은 조각을 많이 모으면 가운데 모양이 예뻐진다.

---

## Ⅲ. 비교 및 연결

| 개념 | 의미 |
| :-- | :-- |
| Population | 모집단 |
| Sample Mean | 표본평균 |
| [CLT](/studynote/08_algorithm_stats/08_stats/139_clt/) | [중심 극한 정리](/studynote/08_algorithm_stats/08_stats/139_clt/) |

| 활용 | 설명 |
| :-- | :-- |
| Hypothesis Test | [가설 검정](/studynote/08_algorithm_stats/08_stats/145_hypothesis_testing/) |
| [Confidence Interval](/studynote/08_algorithm_stats/08_stats/146_confidence_interval/) | 신뢰구간 |

CLT는 통계 추론 전체의 바닥에 깔린 기초다.

- **📢 섹션 요약 비유**: 많은 작은 점들이 모여 가운데 법칙을 만든다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 표본 수가 충분한가?
2. 표본평균 분포를 보는가?
3. 표준오차를 이해하는가?
4. 정규근사를 사용할 수 있는가?
5. 추론의 기반으로 쓰는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모집단과 표본평균을 혼동하는 설계
- CLT를 만능으로 보는 설계
- 표본 수를 무시하는 설계
- 정규성 가정을 무조건 적용하는 설계

기술사 관점에서는 CLT를 "표본평균의 정규 근사 원리"로 설명해야 한다.

- **📢 섹션 요약 비유**: 작은 것들을 많이 모으면 가운데가 안정된다.

---

## Ⅴ. 기대효과 및 결론

CLT는 통계 추론을 가능하게 하는 핵심 정리다.

결론적으로 [중심 극한 정리](/studynote/08_algorithm_stats/08_stats/139_clt/)는 표본평균이 정규분포에 가까워진다는 원리다.

- **📢 섹션 요약 비유**: 많은 표본이 모이면 정규 모양이 된다.

---

## 관련 개념 맵

```text
Population
  v
Sample Mean
  v
CLT
  v
Inference
```

---

## 관련 키워드 및 발전 흐름도

```text
Sampling
  v
CLT
  v
Normal Approximation
  v
Statistical Inference
```

---

## 어린이를 위한 3줄 비유 설명

조각을 많이 모아요.
가운데 모양이 예뻐져요.
CLT는 그런 법칙이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 73 / 258

<- **이전**: [72. 카이제곱 검정 (Chi-square Test) - 범주형 데이터 독립성/적합성](/studynote/14_data_engineering/02_math_mining/072_chi_square_test_categorical_independence_goodness_of_fit/)
**다음**: [74. 대수의 법칙 (LLN, Law of Large Numbers) - 수렴 확률](/studynote/14_data_engineering/02_math_mining/074_law_of_large_numbers_lln_convergence_probability/) ->

---
