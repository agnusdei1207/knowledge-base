+++
weight = 510
title = "510. 통계 기초: 평균, 분산, 왜도, 첨도 (Statistics Basics Mean Variance Skewness Kurtosis)"
date = "2026-05-09"
[extra]
categories = "studynote-ict-convergence"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[100_descriptive_statistics|기술 통계]]([[100_descriptive_statistics|Descriptive Statistics]])는 [[001_dikw_pyramid|데이터]]의 중심(Central Tendency), 산포(Spread), 형태(Shape)를 네 가지 척도로 압축한다.
> 2. **가치**: 같은 평균·[[136_variance|분산]]을 가진 [[001_dikw_pyramid|데이터]]도 분포 형태가 다를 수 있음을 애스컴 4중주(Anscombe's Quartet)가 증명 — [[003_bigdata_7v|시각화]] 없는 요약 통계는 맹점을 낳는다.
> 3. **판단 포인트**: [[064_skewness_kurtosis_log_transformation|왜도]]([[064_skewness_kurtosis_log_transformation|Skewness]]) > 1이면 변환([[568_logs_distributed_logging_elk_fluentd|로그]]·제곱근) 고려, 첨도(Kurtosis) > 3이면 두꺼운 꼬리([[525_fat_file_allocation_table|Fat]] Tail) 위험 관리 필요.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]]를 처음 마주쳤을 때 가장 먼저 하는 작업이 [[100_descriptive_statistics|기술 통계]]다. 수천만 행을 몇 개의 숫자로 축약해 "이 [[001_dikw_pyramid|데이터]]가 어떻게 생겼는가"를 파악한다.

### 중심 경향 척도 (Central Tendency)

| 척도 | 정의 | 강점 | 약점 |
|:---|:---|:---|:---|
| 평균 (Mean) | Σxᵢ / n | 수학적 처리 용이 | 이상값([[076_outlier_detection_iqr_dbscan_isolation_forest|Outlier]])에 민감 |
| 중앙값 (Median) | 정렬 후 중앙 값 | 이상값에 강건(Robust) | 수학적 활용 제한 |
| 최빈값 (Mode) | 가장 자주 나타나는 값 | 범주형 [[001_dikw_pyramid|데이터]] 적합 | 다봉 분포에서 복수 존재 |

**실무 판단**: 소득·주택가격처럼 우편향(Right-Skewed) [[001_dikw_pyramid|데이터]]는 중앙값이 대표성 높다.

- **📢 섹션 요약 비유**: 평균은 반 전체 성적 합을 인원 수로 나눈 것인데, 한 명이 100점을 받으면 나머지가 다 0점이어도 평균이 높아진다. 중앙값은 줄 세운 가운데 사람의 점수라 그런 왜곡이 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 산포도(Spread) 계층 구조

```
데이터 분포 요약
┌──────────────────────────────────────────┐
│  중심: Mean / Median / Mode              │
├──────────────────────────────────────────┤
│  산포: Range │ IQR │ Variance │ Std Dev  │
├──────────────────────────────────────────┤
│  형태: Skewness (비대칭) │ Kurtosis (꼬리)│
└──────────────────────────────────────────┘
```

- **[[136_variance|분산]] ([[136_variance|Variance]], σ²)**: σ² = Σ(xᵢ − μ)² / n — 편차 제곱합의 평균. 단위가 원래 [[001_dikw_pyramid|데이터]]의 제곱이라 해석이 불편.
- **표준편차 (Standard Deviation, σ)**: σ = √σ² — 원래 단위 복원. "평균에서 평균적으로 이만큼 떨어져 있다"는 직관.
- **IQR (Interquartile Range)**: Q3 − Q1 — 이상값에 강건한 산포 척도. 박스플롯의 핵심.

### 분포 형태 척도

| 척도 | 공식(표준화) | 해석 |
|:---|:---|:---|
| [[064_skewness_kurtosis_log_transformation|왜도]] ([[064_skewness_kurtosis_log_transformation|Skewness]]) | E[(X−μ)³] / σ³ | 0: 대칭, >0: 우편향, <0: 좌편향 |
| 첨도 (Kurtosis) | E[(X−μ)⁴] / σ⁴ | 정규=3, 초과 첨도=K−3: >0이면 두꺼운 꼬리 |

- **📢 섹션 요약 비유**: 산포는 선수들의 실력 편차고, [[064_skewness_kurtosis_log_transformation|왜도]]는 "잘하는 선수가 더 많냐 못하는 선수가 더 많냐"의 기울어짐, 첨도는 "중간 실력 선수가 대부분이고 극단만 있냐(뾰족)"를 나타낸다.

---

## Ⅲ. 비교 및 연결

### 애스컴 4중주 (Anscombe's Quartet) — 통계 함정

Anscombe이 만든 4개 [[001_dikw_pyramid|데이터]]셋은 **평균, [[136_variance|분산]], 상관계수, 회귀선이 모두 동일**하지만 산점도는 완전히 다른 형태(선형, 곡선, 이상값 포함 등)를 보인다.

**[[659_ir_lessons_learned|교훈]]**: 요약 통계만으로 [[001_dikw_pyramid|데이터]]를 판단하지 말고 반드시 [[003_bigdata_7v|시각화]]를 병행하라.

| 비교 항목 | [[136_variance|분산]] ([[136_variance|Variance]]) | IQR |
|:---|:---|:---|
| 이상값 민감도 | 높음 | 낮음 |
| 활용 | 모델 학습, [[138_normal_distribution|정규 분포]] | [[064_eda|EDA]], 박스플롯 |

- **📢 섹션 요약 비유**: 동일한 성적 통계를 가진 두 반이 있어도 한 반은 모두 고른 실력, 다른 반은 상위권과 하위권이 극단적으로 나뉠 수 있다 — 평균만 보면 차이를 놓친다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**시나리오**: 전자상거래 구매 금액 분포 분석

1. 평균 구매금액 58,000원, 중앙값 22,000원 → 우편향(Right-Skewed) [[396_validation|확인]].
2. [[064_skewness_kurtosis_log_transformation|왜도]] = 2.8 → [[568_logs_distributed_logging_elk_fluentd|로그]] 변환(Log Transform) 적용 후 모델 학습.
3. 첨도 = 5.1 (초과 첨도 2.1) → 고가 구매의 극단값이 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]([[111_anomaly_detection|Anomaly Detection]]) 대상.
4. IQR 기반 박스플롯으로 이상값(1.5·IQR 초과) 28건 [[396_validation|확인]] → 제거 or 보정.

**기술사 판단 포인트**:
- [[064_skewness_kurtosis_log_transformation|왜도]] |S| > 1: 변환 또는 비모수(Non-Parametric) 검정 전환 검토.
- 첨도 > 3 (두꺼운 꼬리): 금융 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 모델에서 VaR(Value at [[096_risk_non_risk_architecture_evaluation_flaws|Risk]]) 과소 추정 위험.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 분석은 환자 혈액검사와 같다. 평균 혈당만 봐서는 안 되고, 얼마나 들쭉날쭉한지([[136_variance|분산]]), 고혈당 쪽으로 치우쳤는지([[064_skewness_kurtosis_log_transformation|왜도]]), 극단값이 자주 나타나는지(첨도)까지 종합 판단해야 한다.

---

## Ⅴ. 기대효과 및 결론

[[100_descriptive_statistics|기술 통계]]의 완전한 이해는 모든 [[001_dikw_pyramid|데이터]] 분석의 출발점이다. 중심·산포·형태를 동시에 파악하고 [[003_bigdata_7v|시각화]]로 검증할 때 [[001_dikw_pyramid|데이터]] 품질 문제와 분포 특성을 조기에 발견할 수 있다.

- **[[064_eda|EDA]]([[105_exploratory_data_analysis|Exploratory Data Analysis]]) 효율 향상**: 이상값·편향 조기 발견으로 모델 학습 전 [[266_data_cleansing|데이터 정제]] 시간 단축.
- **적절한 모델 선택**: 분포 형태에 따라 파라미터 검정 vs 비모수 검정을 올바르게 선택.
- **의사 결정 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 제고**: 요약 통계와 [[003_bigdata_7v|시각화]]를 함께 보고하여 이해관계자의 오해를 방지.

- **📢 섹션 요약 비유**: [[100_descriptive_statistics|기술 통계]]는 지도에서 현재 위치를 찍는 것이다. 위치(평균)만 알면 지형(분포 형태)을 모른다. 위치·고도·경사(중심·산포·형태)를 함께 봐야 올바른 길을 찾을 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 평균/중앙값 | 이상값 탐지, 편향 분석 · [[064_eda|EDA]] 1단계 |
| [[136_variance|분산]]/표준편차 | [[138_normal_distribution|정규 분포]], Z-Score · 표준화, [[145_hypothesis_testing|가설 검정]] |
| IQR | 박스플롯, Tukey 방법 · 이상값 제거 |
| [[064_skewness_kurtosis_log_transformation|왜도]] | [[568_logs_distributed_logging_elk_fluentd|로그]] 변환, 비모수 검정 · 전처리 판단 |
| 첨도 | 꼬리 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]], [[525_fat_file_allocation_table|Fat]] Tail · 금융·보험 모델 |

### 📈 관련 키워드 및 발전 흐름도

```text
[이상값 탐지 · 편향 분석] → [통계 기초: 평균 · 분산] → [꼬리 리스크 · Fat Tail]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 반 친구들의 키를 조사할 때 평균 키는 "전체를 고르게 나눈 키"고, 중앙값은 "줄 세웠을 때 한가운데 친구의 키"야.
2. [[136_variance|분산]]은 친구들의 키가 얼마나 들쭉날쭉한지를 나타내고, [[064_skewness_kurtosis_log_transformation|왜도]]는 키가 큰 쪽으로 몰렸는지 작은 쪽으로 몰렸는지를 알려줘.
3. 첨도는 대부분 비슷한 키인데 갑자기 아주 크거나 작은 친구가 있는지 나타내는 거야!
