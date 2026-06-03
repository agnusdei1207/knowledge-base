+++
title = "114. 가우시안 혼합 모델 (GMM, Gaussian Mixture Model) - EM 알고리즘·소프트 클러스터링"
date = 2026-04-19

[taxonomies]
tags = ["studynote-dataengineering"]

[extra]
tags = ["studynote-dataengineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [GMM](/knowledge-base/studynote/10_ai/05_data_science_ml/360_gmm_em_algorithm/)(Gaussian Mixture Model)은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 <strong>K개의 가우시안(정규) 분포의 가중 합</strong>으로 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되었다고 가정하고, 각 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포인트가 어느 가우시안에 속하는지 <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/">확률</a>적으로 추정(소프트 클러스터링)</strong>하는 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 모델이다.
> 2. **가치**: K-Means가 각 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 <strong>하나의 클러스터에 확정(하드 할당)</strong>하는 반면, GMM은 "이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 A 클러스터에 70%, B에 30%"처럼 <strong>소속 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/">확률</a>을 제공</strong>하여 경계 모호성을 표현할 수 있다.
> 3. **판단 포인트**: GMM의 파라미터(평균·공분산·혼합 계수)는 <strong>EM(<a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/142_em_algorithm/">Expectation-Maximization</a>) <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>으로 추정하며, 클러스터 수 K는 BIC(Bayesian Information Criterion)로 선택한다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">K-Means (하드) vs GMM (소프트) 클러스터링</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">K-Means</div><div class="kb-diagram-node">GMM</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">○○○ ●●● ○○◐ ◐●●</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">확정 할당 확률적 할당</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">"A 아니면 B" "A에 70%, B에 30%"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">원형 클러스터만 타원형 클러스터 가능</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: K-Means는 학생을 "반드시 A반 또는 B반"에 배정하는 것이고, GMM은 "A반에 70% 속하고 B반에도 30% 속한다"고 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적으로 표현하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### EM [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 2단계

| 단계 | 작업 | 비유 |
|:---|:---|:---|
| **E-step (Expectation)** | 현재 파라미터로 각 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 소속 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)(Responsibility) 계산 | 학생이 각 반에 속할 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 계산 |
| **M-step (Maximization)** | 소속 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)로 가중 평균·공분산·혼합 계수 재추정 | [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 기반으로 반 중심·크기 재조정 |
| **반복** | E→M 반복 → 수렴 | 최적의 반 배정 완성 |

### [GMM](/knowledge-base/studynote/10_ai/05_data_science_ml/360_gmm_em_algorithm/) 파라미터

| 파라미터 | 의미 |
|:---|:---|
| $\mu_k$ | k번째 가우시안의 평균 (중심) |
| $\Sigma_k$ | k번째 가우시안의 공분산 (모양·방향) |
| $\pi_k$ | k번째 가우시안의 혼합 계수 (비중) |

- **📢 섹션 요약 비유**: EM은 눈을 가리고 과녁을 맞추는 궁수가, 화살을 쏘고(E) → 눈가리개를 살짝 올려 위치를 조정(M)하는 반복 훈련이다.

---

## Ⅲ. 비교 및 연결

| 비교 | K-Means | [GMM](/knowledge-base/studynote/10_ai/05_data_science_ml/360_gmm_em_algorithm/) |
|:---|:---|:---|
| **할당** | 하드 (0 or 1) | <strong>소프트 (<a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/">확률</a>)</strong> |
| **클러스터 형태** | 원형 | **타원형 (공분산)** |
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong> | 거리 기반 | <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/">확률</a> 기반 (EM)</strong> |
| **속도** | 빠름 | 느림 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/">이상치</a></strong> | 민감 | [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)로 흡수 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 활용 시나리오
1. **고객 세분화**: 경계 모호한 고객 그룹 (VIP와 일반 사이) [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/).
2. <strong><a href="/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/">이상 탐지</a></strong>: 정상 분포를 GMM으로 모델링 → 낮은 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) = [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/).
3. **음성 인식**: 음소별 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 분포 모델링 (HMM-[GMM](/knowledge-base/studynote/10_ai/05_data_science_ml/360_gmm_em_algorithm/)).

---

## Ⅴ. 기대효과 및 결론

GMM은 K-Means의 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적 일반화이며, 클러스터 경계가 모호하거나 타원형 분포를 갖는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 우수한 성능을 보인다. Variational Inference·Bayesian GMM으로 확장되어 자동 클러스터 수 결정도 가능하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **K-Means** | GMM의 하드 클러스터링 특수 케이스 |
| <strong>EM <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong> | [GMM](/knowledge-base/studynote/10_ai/05_data_science_ml/360_gmm_em_algorithm/) 파라미터 추정 방법 |
| **BIC / AIC** | 최적 클러스터 수 K 선택 기준 |
| **HMM** | GMM을 방출 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)로 사용하는 시퀀스 모델 |
| <strong>Bayesian <a href="/knowledge-base/studynote/10_ai/05_data_science_ml/360_gmm_em_algorithm/">GMM</a></strong> | 클러스터 수 자동 결정 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">K-Means (1957) — 하드 클러스터링</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">EM 알고리즘 (1977, Dempster) — 불완전 데이터 MLE</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">GMM + EM (1990s) — 소프트 클러스터링 표준</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Bayesian GMM (2000s) — 자동 K 결정</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재: VAE·Flow — 심층 생성 모델이 GMM을 대체/확장</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. K-Means는 학생을 <strong>"반드시 A반!"</strong>이라고 정하는 거예요.
2. GMM은 <strong>"A반에 70%, B반에 30%"</strong>처럼 어느 반에 더 가까운지 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)로 말해줘요.
3. 세상에는 딱 나눌 수 없는 것이 많으니까, GMM처럼 <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/">확률</a>로 표현</strong>하는 게 더 정확하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 114 / 258

← **이전**: [113. 매니폴드 가설 (Manifold Hypothesis) - 고차원 데이터와 차원 축소의 수학적 근거](/knowledge-base/studynote/14_data_engineering/02_math_mining/113_manifold_hypothesis_dimensionality_reduction/)
**다음**: [115. DBSCAN 클러스터링 - 밀도 기반 군집화·노이즈 분리·비구형 클러스터](/knowledge-base/studynote/14_data_engineering/02_math_mining/115_dbscan_clustering/) →

---
