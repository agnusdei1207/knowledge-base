---
title: 225. KDD (Knowledge Discovery in Databases) T검정 ANOVA 통계 분석
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: KDD(Knowledge Discovery in Databases, [[002_database_definition|데이터베이스]] 지식 발견)는 원시 [[001_dikw_pyramid|데이터]]에서 유효하고 새롭고 유용한 패턴을 추출하는 체계적 프로세스이며, 통계 검정은 발견된 패턴이 우연이 아님을 수학적으로 보증한다.
> 2. **가치**: T검정·[[071_anova_analysis_of_variance_f_value_post_hoc|ANOVA]]·[[147_chi_square_test|카이제곱 검정]]을 통해 집단 간 차이의 통계적 유의성을 [[395_verification_process_review|검증]]함으로써, [[001_dikw_pyramid|데이터]] 분석 결과가 비즈니스 의사결정에 신뢰할 만한 근거가 된다.
> 3. **판단 포인트**: 검정 방법 선택은 변수 유형(수치형/범주형)과 집단 수(2개/다수)에 따라 결정되며, p-value만으로 의사결정하지 않고 효과 크기(Effect Size)를 함께 보는 것이 현대 통계의 요구사항이다.

---

## Ⅰ. 개요 및 필요성

### KDD(Knowledge Discovery in Databases) 프로세스

KDD는 1996년 Fayyad et al.이 정의한 5단계 지식 발견 프레임워크다. 단순한 [[284_data_mining_association_classification_clustering_crisp_dm|데이터 마이닝]]([[284_data_mining_association_classification_clustering_crisp_dm|Data Mining]])이 아니라, 전처리부터 해석까지 포함하는 완전한 파이프라인이다.

```
┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐
│ ① Selection│───→│②Preprocess│───→│③Transform │───→│④Data Mining───→│⑤Interpret │
│  (선택)   │    │ (전처리)  │    │  (변환)   │    │ (데이터  │    │ /Evaluate │
│           │    │           │    │           │    │  마이닝) │    │  (해석)   │
│ 분석 목적에│    │ 결측값 처리│    │ 정규화    │    │ 패턴 탐색│    │ 비즈니스  │
│ 맞는 데이터│    │ 이상값 제거│    │ 차원 축소 │    │ 분류·군집│    │ 적용 가능 │
│ 하위집합  │    │ 노이즈 제거│    │ 특성 공학 │    │ 회귀·연관│    │ 여부 검증 │
└───────────┘    └───────────┘    └───────────┘    └───────────┘    └───────────┘
```

📢 **섹션 요약 비유**: KDD는 "금광에서 금 캐는 과정"이다. 산([[001_dikw_pyramid|데이터]])을 선택하고, 흙(노이즈)을 제거하고, 돌을 분쇄(변환)하고, 금맥(패턴)을 찾고, 순도 검사(해석)를 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. 통계 검정 선택 가이드

```
분석 목적: 집단 간 차이가 유의한가?
         │
         ▼
   변수 유형은?
    │          │
수치형(연속)    범주형(이산)
    │              │
    ▼              ▼
집단 수는?     카이제곱 검정
  │    │       (Chi-Square Test)
 2개  3개+
  │    │
  ▼    ▼
T검정  ANOVA
│     (일원분산분석)
├─ 독립표본 T검정
│   (두 집단 평균 비교)
└─ 대응표본 T검정
    (동일 집단 전후 비교)
```

### 2-2. T검정 ([[070_t_test_independent_paired_mean_difference|T-Test]])

T검정은 두 집단의 평균 차이가 통계적으로 유의한지 [[395_verification_process_review|검증]]한다.

| 유형 | 설명 | 예시 |
|:---|:---|:---|
| 독립표본 T검정 (Independent Samples [[070_t_test_independent_paired_mean_difference|T-Test]]) | 서로 다른 두 집단 평균 비교 | A/B 테스트: 대조군 vs 실험군 [[090_ctr_mode|CTR]] |
| 대응표본 T검정 (Paired Samples [[070_t_test_independent_paired_mean_difference|T-Test]]) | 동일 집단의 전후 비교 | 교육 전후 시험 점수 비교 |
| 일표본 T검정 (One-Sample [[070_t_test_independent_paired_mean_difference|T-Test]]) | 표본 평균이 기준값과 다른지 | 불량률 평균이 2% 기준과 다른가 |

T 통계량 계산:
```
       x̄₁ - x̄₂
t = ─────────────────
     √(s²/n₁ + s²/n₂)

x̄₁, x̄₂: 두 집단의 표본 평균
s²: 합동 표준편차
n₁, n₂: 두 집단 표본 크기
```

### 2-3. 일원분산분석 (One-Way [[071_anova_analysis_of_variance_f_value_post_hoc|ANOVA]], Analysis of [[136_variance|Variance]])

ANOVA는 3개 이상 집단의 평균 차이를 동시에 [[395_verification_process_review|검증]]한다. (T검정을 반복하면 1종 오류가 누적됨)

```
F = 집단 간 분산(Between-Group Variance)
    ─────────────────────────────────────
    집단 내 분산(Within-Group Variance)

F 값 크면 → 집단 간 차이가 내부 변동보다 크다 → 유의한 차이 존재
```

| 구분 | 검정 통계량 | 귀무가설 | 사후검정 필요 |
|:---|:---:|:---|:---:|
| T검정 | t | μ₁ = μ₂ | 불필요 |
| One-Way [[071_anova_analysis_of_variance_f_value_post_hoc|ANOVA]] | F | μ₁ = μ₂ = μ₃ = ... = μₖ | 필요 (Tukey HSD 등) |
| Two-Way [[071_anova_analysis_of_variance_f_value_post_hoc|ANOVA]] | F | 두 독립변수 각각·교호작용 효과 없음 | 필요 |

[[071_anova_analysis_of_variance_f_value_post_hoc|ANOVA]] 이후 사후검정(Post-hoc Test): Tukey HSD, Bonferroni 보정, Games-Howell

### 2-4. [[147_chi_square_test|카이제곱 검정]] ([[147_chi_square_test|Chi-Square Test]])

범주형 변수 간 독립성을 [[395_verification_process_review|검증]]한다.

| 유형 | 목적 | 예시 |
|:---|:---|:---|
| 독립성 검정 | 두 범주 변수 연관성 | 성별 × 구매 여부 독립인가? |
| 적합도 검정 | 관측 분포 vs 기대 분포 | 주사위 균등 분포 [[395_verification_process_review|검증]] |

```
교차분석 (Cross Tabulation) 예시:

            구매O   구매X   합계
  남성        120     80     200
  여성         90    110     200
  합계        210    190     400

χ² = Σ (관측값 - 기대값)² / 기대값

자유도 = (행수-1) × (열수-1) = 1
```

📢 **섹션 요약 비유**: 통계 검정은 "법정에서 증거 채택 기준"이다. 단순히 숫자가 다르다는 것(관측)만으로는 부족하고, p-value라는 기준으로 "우연일 [[130_probability|확률]]이 충분히 낮을 때"만 차이가 있다고 인정한다.

---

## Ⅲ. 비교 및 연결

### 3-1. 검정 방법 종합 비교표

| 검정 방법 | 변수 유형 | 집단 수 | 가정 | 비모수 대안 |
|:---|:---|:---:|:---|:---|
| 독립표본 T검정 | 수치형 | 2 | 정규분포, 등분산 | Mann-Whitney U |
| 대응표본 T검정 | 수치형 | 2 (전후) | 차이값 정규분포 | Wilcoxon |
| One-Way [[071_anova_analysis_of_variance_f_value_post_hoc|ANOVA]] | 수치형 | 3+ | 정규분포, 등분산 | Kruskal-Wallis |
| [[147_chi_square_test|카이제곱 검정]] | 범주형 | 2+ | 기대빈도 ≥ 5 | Fisher's Exact Test |
| [[226_pearson_correlation_regression_r2_vif_multicollinearity|피어슨 상관]] | 수치형 2개 | - | 정규분포, 선형 | Spearman 상관 |

### 3-2. 효과 크기 (Effect Size) — p-value만으론 부족한 이유

표본이 매우 크면 작은 차이도 p < 0.05가 된다. 효과 크기는 실질적 유의미성을 측정한다.

| 검정 | 효과 크기 지표 | 기준 |
|:---|:---|:---|
| T검정 | Cohen's d | 0.2 소, 0.5 중, 0.8 대 |
| [[071_anova_analysis_of_variance_f_value_post_hoc|ANOVA]] | η² (에타 제곱) | 0.01 소, 0.06 중, 0.14 대 |
| 카이제곱 | Cramér's V | 0~1 사이, 클수록 강한 연관 |

📢 **섹션 요약 비유**: p-value는 "유죄 vs 무죄 판결"이고, 효과 크기는 "형량"이다. 유죄(p < 0.05)라도 형량이 작으면(효과 크기 small) 실제로 중요하지 않을 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. A/B 테스트 적용 시나리오

**시나리오: 이커머스 결제 버튼 색상 변경 효과 [[395_verification_process_review|검증]]**

```
[실험 설계]
대조군 (n=5,000): 파란색 버튼
실험군 (n=5,000): 빨간색 버튼

[측정값]
대조군 전환율: 3.2% ± 0.5%
실험군 전환율: 3.8% ± 0.5%

[독립표본 T검정 적용]
H₀: μ대조군 = μ실험군
H₁: μ대조군 ≠ μ실험군

결과: t = 4.2, p = 0.00003 → p < 0.05이므로 귀무가설 기각
Cohen's d = 0.24 → 소~중 효과 크기

결론: 통계적으로 유의하나 효과 크기는 작음 → 배포 결정 시 비용-편익 분석 추가 필요
```

### 4-2. KDD-통계 분석 통합 파이프라인

| KDD 단계 | 통계 적용 포인트 |
|:---|:---|
| 전처리 | 이상값 Z-score 기반 탐지, 결측값 대체 [[268_strategy_pattern|전략]] |
| 변환 | 정규분포 변환(Box-Cox), 범주형 인코딩 |
| [[001_dikw_pyramid|데이터]]마이닝 | [[104_classification_analysis|분류]] 전 특성 중요도 F검정 기반 선택 |
| 해석 | 검정 결과 효과 크기, 신뢰구간과 함께 보고 |

📢 **섹션 요약 비유**: A/B 테스트는 "신약 임상시험"과 같다. 약을 먹은 집단(실험군)과 위약을 먹은 집단(대조군)을 T검정으로 비교해 효과가 진짜인지 확인한다.

---

## Ⅴ. 기대효과 및 결론

KDD 프로세스와 통계 검정의 결합은 **[[001_dikw_pyramid|데이터]] 기반 의사결정(DDDM, [[001_dikw_pyramid|Data]]-Driven Decision Making)**의 수학적 기반이다. "느낌과 경험"이 아닌 "증거와 [[130_probability|확률]]"로 비즈니스를 운영할 수 있게 한다.

### 통계 검정 핵심 요약

| 항목 | 내용 |
|:---|:---|
| 귀무가설 (H₀) | 차이 없음, 효과 없음 |
| 대립가설 (H₁) | 차이 있음, 효과 있음 |
| 유의수준 (α) | 보통 0.05 (5% 오류 허용) |
| [[337_p_value_significance|p-value]] | 귀무가설이 참일 때 관측값 이상 극단값 [[130_probability|확률]] |
| 결정 기준 | p < α → 귀무가설 기각 |

기술사 시험에서 KDD는 **"5단계 프로세스 + 각 단계별 기법 매핑"** 으로, 통계 검정은 **"검정 선택 기준(변수 유형·집단 수) + 가정·한계"** 를 중심으로 서술해야 한다.

📢 **섹션 요약 비유**: KDD와 통계 검정은 "과학적 요리 레시피"다. 재료 선택([[022_mcts_four_stages|Selection]])부터 완성 요리 평가(Interpret)까지 체계적 순서가 있고, 맛 [[395_verification_process_review|검증]](통계 검정)은 결과가 우연이 아님을 보증한다.

---

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 프로세스 | KDD 5단계 | 선택→전처리→변환→마이닝→해석 |
| 검정 | 독립표본 T검정 | 두 독립 집단 평균 비교 |
| 검정 | 대응표본 T검정 | 동일 집단 전후 비교 |
| 검정 | One-Way [[071_anova_analysis_of_variance_f_value_post_hoc|ANOVA]] | 3개 이상 집단 [[071_anova_analysis_of_variance_f_value_post_hoc|분산 분석]] |
| 검정 | [[147_chi_square_test|Chi-Square Test]] (카이제곱) | 범주형 변수 독립성 |
| 보완 | Effect Size (효과 크기) | 실질적 유의미성 측정 |
| 보완 | [[146_confidence_interval|Confidence Interval]] (신뢰구간) | 모수 추정 범위 |
| 응용 | A/B Testing (A/B 테스트) | 실험군·대조군 비교 |
| 비모수 | Mann-Whitney U | T검정 정규분포 가정 위반 시 |
| 비모수 | Kruskal-Wallis | [[071_anova_analysis_of_variance_f_value_post_hoc|ANOVA]] 정규분포 가정 위반 시 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. "우리 반이 옆 반보다 평균 키가 크다"는 것을 그냥 말하는 것과 T검정으로 증명하는 것은 다르다. T검정은 그 차이가 "우연"이 아님을 수학으로 보여준다.

### 📈 관련 키워드 및 발전 흐름도

```text
KDD 프로세스: 데이터 선택 → 전처리 → 변환 → 마이닝 → 평가
    │
    ▼
통계 검정
    ├─► T-Test: 두 집단 평균 비교
    ├─► ANOVA: 세 집단 이상 분산 분석
    └─► 카이제곱: 범주형 변수 독립성 검정
    │
    ▼
유의수준(α) · p-value · 1종/2종 오류
```
2. 3개 반 이상 비교할 때는 T검정을 여러 번 쓰면 오류가 쌓이므로, ANOVA라는 한 번에 모두 비교하는 방법을 쓴다.
3. KDD는 "보물 지도에서 보물을 찾는 5단계 과정"이고, 통계 검정은 "찾은 것이 진짜 보물인지 감정하는 단계"이다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 225 / 258

← **이전**: [[224_data_lineage_flow_catalog_tagging|224. 데이터 리니지 (Data Lineage) 흐름 족보 카탈로그 태그 거버넌스]]
**다음**: [[226_pearson_correlation_regression_r2_vif_multicollinearity|226. 피어슨 상관 (Pearson Correlation) 회귀 R² 결정계수 다중공선성 VIF]] →

---
