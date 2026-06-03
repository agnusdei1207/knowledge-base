+++
weight = 78
title = "78. DataStream API / Table API & SQL — Flink 두 계층"
description = "Naive Bayes 분류기의 확률적 원리, 조건부 독립 가정,贝叶斯定理 적용 방법, 텍스트 분류에서의 활용"
date = "2026-04-05"
[taxonomies]
tags = ["NaiveBayes", "나이브 베이즈", "베이즈 정리", "조건부 독립", "확률적 분류기", "텍스트 분류"]
categories = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Naive Bayes는 Bayes theorem과 조건부 독립 가정을 이용한 [[130_probability|확률]]적 [[104_classification_analysis|분류]]기다.
> 2. **가치**: 희소한 텍스트나 작은 [[001_dikw_pyramid|데이터]]에서도 빠르고 설명 가능한 기준선을 만든다.
> 3. **판단 포인트**: [[096_iso_iec_20000_itsm_certification|ITSM]] ([[061_itsm|IT Service Management]])과 [[062_itil|ITIL]] (Information Technology Infrastructure [[336_library_vs_framework|Library]])에서는 티켓 [[104_classification_analysis|분류]], 스팸 필터, 태깅에 특히 잘 맞는다.

---

## Ⅰ. 개요 및 필요성

[[104_classification_analysis|분류]] 문제는 "이 [[001_dikw_pyramid|데이터]]가 어느 클래스에 속하는가"를 빠르게 정하는 일이다. Naive Bayes는 단순하지만 강한 기준선으로 자주 쓰인다.
IT 운영에서는 [[090_service_kubernetes_network_load_balancing|서비스]] 요청, 장애 티켓, 문서 태깅처럼 라벨이 분명한 업무가 많다. 이런 곳에서 [[130_probability|확률]] 기반 [[104_classification_analysis|분류]]는 자동화의 첫 단계가 된다.
```text
특징 → prior / likelihood → posterior → class label
P(class|features) ∝ P(class) × Π P(feature|class)
```

- **📢 섹션 요약 비유**: 문서와 티켓을 빠르게 [[104_classification_analysis|분류]]하는 단순한 기준선이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

학습 단계에서는 클래스별 prior를 세고, 각 특징의 likelihood를 집계한다. 예측 단계에서는 posterior를 계산해 가장 높은 클래스를 고른다.
조건부 독립 가정은 현실을 단순화한 것이지만, 텍스트처럼 희소하고 특징 수가 많은 문제에서 의외로 잘 동작한다. Laplace smoothing은 0 [[130_probability|확률]] 문제를 막는다.
| 요소 | 역할 | 메모 |
| --- | --- | --- |
| Prior | 사전 [[130_probability|확률]] | 클래스 빈도를 반영한다 |
| Likelihood | 특징이 주어졌을 때의 [[130_probability|확률]] | 특징별 증거를 모은다 |
| Posterior | 최종 클래스 [[130_probability|확률]] | 비교 기준이 된다 |
| [[350_laplace_smoothing|Laplace smoothing]] | 0 [[130_probability|확률]] 방지 | 희소 [[001_dikw_pyramid|데이터]]에 중요하다 |
| MAP (Maximum A Posteriori) | 가장 큰 posterior 선택 | [[104_classification_analysis|분류]] 결정 규칙이다 |

- **📢 섹션 요약 비유**: prior, likelihood, posterior를 곱해 가장 가능성 높은 클래스를 고른다.

---

## Ⅲ. 비교 및 연결

Naive Bayes는 [[087_process_state_transition|생성]] 모델이라 분포를 먼저 배우고, logistic regression은 판별 모델이라 경계를 직접 배운다. decision tree는 규칙 분기 중심이라 해석 방식이 또 다르다.
독립 가정이 강할수록 단순해지지만, 상관관계가 큰 [[247_feature_label_variables|피처]]에서는 성능이 약해질 수 있다. 그래서 모델은 [[001_dikw_pyramid|데이터]]의 형태와 함께 선택해야 한다.
| 비교축 | Naive Bayes | [[227_logistic_regression_clt_pvalue_type_error|Logistic Regression]] | [[124_decision_tree|Decision Tree]] |
| --- | --- | --- | --- |
| 학습 철학 | [[087_process_state_transition|생성]] 모델 | 판별 모델 | 규칙 분기 |
| [[001_dikw_pyramid|데이터]] 요구 | 작아도 시작 가능 | 중간 이상 | 중간 |
| 해석성 | [[130_probability|확률]] 증거를 읽기 쉽다 | [[267_weight_bias_activation|가중치]] 해석 | 경로 해석 |

- **📢 섹션 요약 비유**: [[087_process_state_transition|생성]] 모델의 단순함이 텍스트 [[104_classification_analysis|분류]]에서 힘을 발휘한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 티켓 제목, 설명, 키워드 같은 텍스트 특징을 이용해 라우팅에 쓴다. 자동 [[104_classification_analysis|분류]]가 잘 되면 1차 응답 속도와 운영 효율이 크게 좋아진다.
다만 특징 간 상관관계가 강하거나 [[130_probability|확률]] 보정이 중요하면 다른 모델도 함께 봐야 한다. 특히 smoothing 없이 쓰면 희소 특징에서 0 [[130_probability|확률]]이 쉽게 터진다.
### [[435_checklist_based_testing|체크리스트]]

1. 클래스 prior와 likelihood가 충분히 학습됐는가?
2. Laplace smoothing이 적용됐는가?
3. [[096_iso_iec_20000_itsm_certification|ITSM]] 프로세스와 [[104_classification_analysis|분류]] 결과가 연결되는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 0 [[130_probability|확률]] 문제를 무시한 채 그대로 쓰는 것
- 상관된 특징을 많이 넣고 독립 가정이 무너지게 두는 것

- **📢 섹션 요약 비유**: smoothing과 [[247_feature_label_variables|피처]] 설계가 성능을 좌우한다.

---

## Ⅴ. 기대효과 및 결론

Naive Bayes는 복잡한 모델이 나오기 전에도 빠른 자동화를 가능하게 하는 강한 기준선이다. 작은 [[001_dikw_pyramid|데이터]]와 텍스트 업무에서 특히 유용하다.
앞으로는 임베딩과 결합한 하이브리드 [[104_classification_analysis|분류]]가 더 많아지겠지만, [[130_probability|확률]]적 기준선의 가치는 줄지 않는다.
기술사는 이 주제를 "적은 정보로도 빠르게 우선순위를 매기는 [[130_probability|확률]] [[104_classification_analysis|분류]]"로 기억하면 된다.

- **📢 섹션 요약 비유**: 작은 [[001_dikw_pyramid|데이터]]에서도 빠르게 자동화를 시작하게 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| --- | --- |
| [[131_bayes_theorem|Bayes theorem]] | 사전 [[130_probability|확률]]과 우도를 결합한다 |
| Prior | 클래스의 기본 비율이다 |
| Likelihood | 특징이 주어졌을 때의 [[130_probability|확률]]이다 |
| Posterior | 최종 판단 [[130_probability|확률]]이다 |
| [[350_laplace_smoothing|Laplace smoothing]] | 희소성 때문에 생기는 0 [[130_probability|확률]]을 막는다 |
| [[096_iso_iec_20000_itsm_certification|ITSM]] / [[062_itil|ITIL]] | 운영 티켓 [[104_classification_analysis|분류]]와 잘 맞는다 |

### 📈 관련 키워드 및 발전 흐름도

```text
training data
  │
  ▼
count features by class
  │
  ▼
estimate prior / likelihood
  │
  ▼
compute posterior
  │
  ▼
route to class
```

### 👶 어린이를 위한 3줄 비유 설명

1. 탐정이 단서 몇 개만 보고도 어느 상자에서 왔는지 맞히는 것과 같다.
2. 단서가 서로 얼마나 잘 어울리는지 [[130_probability|확률]]로 계산하면 더 빨리 맞힐 수 있다.
3. 그래서 컴퓨터는 적은 정보로도 가장 그럴듯한 답을 찾는다.
