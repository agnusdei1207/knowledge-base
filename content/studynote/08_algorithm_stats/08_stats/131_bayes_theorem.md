+++
title = "2. 베이즈 정리 (Bayes' Theorem) — 사전/사후 확률 업데이트"
date = 2026-04-21

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

## 핵심 인사이트

> 베이즈 정리 (Bayes' Theorem) 는 "새로운 증거가 들어올 때마다 내 믿음을 정확하게 업데이트하는 공식"이다.
> 사전 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) (Prior [Probability](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)) → 우도 (Likelihood) → 사후 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) (Posterior [Probability](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)) 의 흐름이 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 추론의 핵심 골격이다.
> 직관과 반대되는 결과(기저율 무시 오류)가 자주 발생하므로, 분모 P(B) 계산에 전확률 법칙을 정확히 적용해야 한다.

---

## Ⅰ. 베이즈 정리 — 공식과 각 항의 의미

### 공식 유도

[조건부 확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/132_conditional_probability/)의 정의에서 출발한다:

```
P(A|B) = P(A∩B) / P(B)
P(B|A) = P(A∩B) / P(A)

두 식에서 P(A∩B) = P(B|A)·P(A) 를 대입하면:

┌─────────────────────────────────────────────────────┐
│                                                     │
│   P(A|B) = P(B|A) · P(A)                           │
│             ─────────────                           │
│                 P(B)                                │
│                                                     │
│   = P(B|A) · P(A)                                  │
│     ─────────────────────────────────────────────  │
│     P(B|A)·P(A)  +  P(B|Ā)·P(Ā)   (전확률 공식)   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 각 항의 이름과 역할

| 항 | 이름 | 의미 |
|:---:|:---:|:---|
| P(A) | 사전 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) (Prior [Probability](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)) | 증거 B를 보기 전 A에 대한 믿음 |
| P(B\|A) | 우도 (Likelihood) | A가 사실일 때 B가 관찰될 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) |
| P(B) | 증거 (Evidence) | B가 관찰될 전체 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) ([정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 상수) |
| P(A\|B) | 사후 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) (Posterior [Probability](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)) | 증거 B를 본 후 업데이트된 A의 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) |

📢 **섹션 요약 비유**: 범죄 현장에서 발자국(증거 B)을 발견했을 때, "용의자 A가 범인일 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)"을 업데이트하는 과정이 베이즈 정리다. 발자국을 보기 전 의심도가 사전 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/), 보고 난 후가 사후 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)이다.

---

## Ⅱ. 전확률 법칙 — P(B) 계산

<strong>전확률 법칙 (Law of Total <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/">Probability</a>)</strong>:
사건 A₁, A₂, ..., Aₙ 이 Ω 를 분할 ([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)) 할 때:

```
P(B) = Σᵢ P(B|Aᵢ) · P(Aᵢ)
     = P(B|A₁)·P(A₁) + P(B|A₂)·P(A₂) + ... + P(B|Aₙ)·P(Aₙ)
```

**베이즈 업데이트 흐름도**:

```
┌──────────────────────────────────────────────────────────┐
│                  베이즈 추론 파이프라인                    │
│                                                          │
│  ┌──────────┐   관찰 증거   ┌──────────┐   ┌──────────┐ │
│  │  사전    │  ──────────→  │  우도    │   │  사후    │ │
│  │  확률    │               │  계산    │ → │  확률    │ │
│  │  P(A)    │               │ P(B|A)   │   │ P(A|B)   │ │
│  └──────────┘               └──────────┘   └──────────┘ │
│       ↑                         ↓                ↓      │
│   도메인 지식                전확률 법칙          다음    │
│  이전 실험 결과              P(B) 계산         사전 확률 │
│                                                          │
│  → 증거가 쌓일수록 사후 확률은 더욱 정밀해짐             │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 전확률 법칙은 "비가 올 전체 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)"을 구할 때, "봄에 비 올 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) × 봄일 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)" + "여름에 비 올 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) × 여름일 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)" + ...처럼 모든 경로를 합산하는 것이다.

---

## Ⅲ. 의료 진단 예시 — 직관의 함정

### 문제 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)

- 희귀 질환 유병률 (Prevalence) = 0.1% (기저율, Base Rate)
- 검사 민감도 (Sensitivity) = 99% → 실제 환자 중 99%를 양성으로 판별
- 검사 특이도 (Specificity) = 95% → 정상인 중 95%를 음성으로 판별

<strong>양성 판정을 받았을 때 실제 환자일 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/">확률</a> (PPV, Positive Predictive Value)?</strong>

```
P(질환) = 0.001,   P(정상) = 0.999
P(양성|질환) = 0.99   (민감도, Sensitivity)
P(양성|정상) = 0.05   (1 - 특이도, 1 - Specificity)

P(양성) = 0.99 × 0.001 + 0.05 × 0.999
        = 0.00099 + 0.04995
        = 0.05094

P(질환|양성) = 0.99 × 0.001 / 0.05094 ≈ 0.019 = 약 1.9%
```

**충격적 결과**: 정확도 99% 검사를 통과해도 실제 환자일 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)은 겨우 1.9%!

### [혼동 행렬](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/) ([Confusion Matrix](/knowledge-base/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/))

| | 실제 양성 | 실제 음성 |
|:---:|:---:|:---:|
| **예측 양성** | TP (True Positive) | [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) (False Positive) |
| **예측 음성** | FN (False Negative) | TN (True Negative) |

- **민감도 (Sensitivity)** = TP / (TP + FN)
- **특이도 (Specificity)** = TN / (TN + [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/))
- **PPV (Positive Predictive Value, 양성 예측값)** = TP / (TP + [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/))
- <strong><a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/013_npv/">NPV</a> (Negative Predictive Value, 음성 예측값)</strong> = TN / (TN + FN)

📢 **섹션 요약 비유**: 희귀한 보물이 숨겨진 넓은 사막에서 탐지기가 "여기 있다!"고 했을 때, 탐지기 정확도가 높더라도 실제 보물이 있을 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)은 낮다 — 왜냐하면 사막은 넓고 보물은 희귀하기 때문이다(기저율의 힘).

---

## Ⅳ. 스팸 필터 예시 — [나이브 베이즈 분류기](/knowledge-base/studynote/10_ai/01_ai_basics/060_naive_bayes_classifier_conditional_independence/)

<strong><a href="/knowledge-base/studynote/10_ai/01_ai_basics/060_naive_bayes_classifier_conditional_independence/">나이브 베이즈 분류기</a> (<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/101_naive_bayes_classifier/">Naive Bayes Classifier</a>)</strong> 는 베이즈 정리에 "특징 간 조건부 독립" 가정을 추가한 실용 모델이다.

### 스팸 판별 과정

```
목표: P(스팸|이메일 단어들) 를 계산

P(스팸|w₁,w₂,...,wₙ) ∝ P(스팸) · Π P(wᵢ|스팸)

나이브(Naive) 가정: 각 단어 wᵢ 는 서로 조건부 독립
```

**예시 계산**:

| 단어 | P(단어\|스팸) | P(단어\|정상) |
|:---:|:---:|:---:|
| "무료" | 0.80 | 0.05 |
| "클릭" | 0.70 | 0.[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) |
| "지금" | 0.60 | 0.20 |

```
P(스팸) = 0.3
P(정상) = 0.7

P(스팸|단어들) ∝ 0.3 × 0.80 × 0.70 × 0.60 = 0.1008
P(정상|단어들) ∝ 0.7 × 0.05 × 0.10 × 0.20 = 0.0007

정규화: P(스팸|단어들) = 0.1008 / (0.1008+0.0007) ≈ 99.3%
```

📢 **섹션 요약 비유**: 스팸 필터는 "수상한 단어 조합"이라는 증거를 조각조각 쌓아 베이즈 정리로 최종 판결을 내리는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 검사관이다.

---

## Ⅴ. 베이즈 추론 — 증거 축적과 순차적 업데이트

베이즈 추론 (Bayesian Inference) 의 강점은 <strong>증거가 들어올 때마다 사후 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/">확률</a>을 새로운 사전 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/">확률</a>로 재활용</strong>할 수 있다는 점이다.

```
초기: P(θ)  (사전 지식)
증거 1 관찰: P(θ|x₁) ← 새로운 사전 확률로 사용
증거 2 관찰: P(켭|x₁,x₂) ← 다시 업데이트
...
증거 n 관찰: P(θ|x₁,...,xₙ) ← 최종 사후 확률
```

**응용 분야**:

- **A/B 테스팅**: 실험 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중 실시간 결과 업데이트
- <strong>의료 <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a></strong>: 검사 결과가 추가될 때마다 진단 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 갱신
- **자율주행**: 센서 데이터를 받을 때마다 위치 추정 업데이트 (칼만 필터, Kalman Filter)
- **NLP (Natural Language Processing)**: 문맥이 추가될수록 단어 의미 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 업데이트

📢 **섹션 요약 비유**: 베이즈 추론은 퍼즐 조각을 하나씩 맞출 때마다 "전체 그림"에 대한 확신을 업데이트하는 과정이다 — 처음엔 흐릿하지만, 증거가 쌓일수록 점점 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|:---|
| 베이즈 정리 | [조건부 확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/132_conditional_probability/) ([Conditional Probability](/knowledge-base/studynote/08_algorithm_stats/08_stats/132_conditional_probability/)) | 기반 공식 |
| 사전 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) | 사후 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) | 업데이트 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
| 전확률 법칙 | 분할 ([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)) | P(B) 계산 도구 |
| [나이브 베이즈](/knowledge-base/studynote/10_ai/03_llm_nlp/264_naive_bayes/) | 조건부 독립 가정 | 단순화 핵심 |
| 민감도·특이도 | ROC 곡선 | [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가 |
| 베이즈 추론 | 칼만 필터 | 실시간 업데이트 응용 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[베이즈 정리]
    │
    ▼
[사전 확률]
    │
    ▼
[전확률 법칙]
    │
    ▼
[나이브 베이즈]
    │
    ▼
[민감도·특이도]
```

이 흐름도는 베이즈 정리에서 출발해 베이즈 추론까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

- 친구가 "오늘 우산 챙겼어?"라고 말하면, 비가 올 가능성이 높아지는 것처럼, 새 정보가 생기면 우리의 예상([확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/))을 바꿔야 해.
- 베이즈 정리는 "새 소식을 들었을 때 내 생각을 얼마나 바꿔야 하는지"를 계산해주는 공식이야.
- [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 의사는 검사 결과 하나하나가 나올 때마다 베이즈 정리로 "이 병일 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)"을 계속 업데이트해서 진단을 내려.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 131 / 175

← **이전**: [1. 확률 (Probability) — 고전/상대도수/주관 확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)
**다음**: [3. 조건부 확률 (Conditional Probability) — P(A|B)](/knowledge-base/studynote/08_algorithm_stats/08_stats/132_conditional_probability/) →

---
