---
title: "Causal Inference Instrumental Variable DAG"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 도구 변수(Instrumental Variable, IV)는 숨겨진 교란변수(Unobserved Confounder) $U$로 인해 발생하는 내생성(Endogeneity) 문제를, $U$와 직접적 상관관계가 없으면서 내생 설명변수 $X$에만 영향을 주는 외생 변수 $Z$를 활용하여 $\text{Cov}(Z, U) = 0$, $\text{Cov}(Z, X) \neq 0$ 조건 하에서 인과효과 $\beta$를 일치추정(Consistent Estimation)하는 인과 추론의 1차 정 Identification 전략이다.
> 2. **가치**: 관측 불가능한 교란변수(예: 역선택, 동시성 편향, 측정오차)가 존재하는 상황에서 RCT가 불가능한 준실험(Quasi-Experiment) 환경에서 인과효과를 복원하며, 2SLS/Two-Stage Least Squares 추정 시 약도구(Weak Instrument) 문제가 발생하지 않으면 일치성과 점근정규분포(Asymptotic Normal Distribution) 성질을 보장한다.
> 3. **판단 포인트**: IV의 타당성은 ① 관련성(Relevance), ② 배제제약(Exclusion Restriction), ③ 외생성(Exchangeability) 3대 가정의 검증 가능성에 달려 있으며, 약도구 편향, LATE(Local Average Treatment Effect) vs ATE 해석의 한계, MTE(Marginal Treatment Effect) 프레임워크로의 확장 여부를 데이터 특성에 따라 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

데이터 기반 의사결정에서 가장 빈번하게 마주치는 문제는 "관측 데이터만으로 인과효과를 식별할 수 없다"는 점이다. 마케팅 ROI 측정, 정책 효과 분석, 추천 시스템의 처치효과(Treatment Effect) 추정 등 실무 현장에서는 통제된 실험(Randomized Controlled Trial, RCT)이 불가능한 경우가 대부분이며, 이때 무시된 교란변수(Unobserved Confounding)로 인해 OLS(Ordinary Least Squares) 추정량이 편향(Biased)된다.

예를 들어, 광고비($X$)와 매출($Y$)의 관계를 단순 회귀로 추정하면 "광고가 매출을 늘린다"는 외관적 상관관계가 도출되지만, 광고 집행 시점에는 동시에 가격 할인, 프로모션, 경쟁사 이슈라는 숨겨진 변수 $U$가 작용하여 광고의 순수 인과효과($\beta_{causal}$)를 과대평가한다. 이를 **동시성 편향(Simultaneity Bias)** 또는 **내생성(Endogeneity)**이라 한다.

인과 그래프(Directed Acyclic Graph, DAG)는 Pearl(1995)의 인과 추론 프레임워크에서 변수 간 인과 구조를 시각적으로 표현하는 도구로, $X \leftarrow U \rightarrow Y$ 형태의 Backdoor Path를 식별하고 차단하기 위한 $d$-separation, $do$-calculus 연산의 기반이 된다. **도구 변수 인과 그래프(IV-DAG)**는 이 두 가지를 결합하여, 비실험적 관측 데이터에서도 $U$의 영향을 제거한 처치 효과($\beta_{IV} = \frac{\text{Cov}(Z, Y)}{\text{Cov}(Z, X)}$)를 식별 가능하게 만든다.

```text
[전통적 회귀의 한계 vs IV-DAG 접근]

      전통적 OLS 회귀                    IV-DAG 기반 인과 추론
  (내생성 문제 발생)                  (도구 변수로 식별 복원)

        Y(매출)                          Y(매출)
        ^                               ^   ^
        |                               |   |
        X(광고)--+                 +---> X(광고) <--- Z(도구)
        |      |                 |     ^              |
        |      v                 |     |              v
        +--> U(교란) <----관측불가--+     +-------------- U(교란)
                  (Backdoor Path)         (Exclusion: Z⊥Y|X)

  • OLS: β_hat = β + Cov(X,U)/Var(X)  • IV: β_IV = Cov(Z,Y)/Cov(Z,X)
  • β_hat은 일치추정량 아님              • Z가 U와 독립이면 일치추정
```

기존 머신러닝/통계 모델은 $P(Y|X)$ 형태의 **조건부 확률**을 추정하는 데 집중했지만, IV-DAG 접근은 $P(Y|do(X))$ 형태의 **개입적 확률(Interventional Probability)**을 복원하여 "만약 우리가 $X$를 강제로 $x$로 설정한다면?"이라는 반사실적(Counterfactual) 질의에 답할 수 있게 한다. 이는 A/B 테스트가 불가능한 사후 분석(Post-hoc Analysis) 환경, 네트워크 효과가 존재하는 시장, 정책 시행 전 효과 예측에서 핵심적인 역할을 수행한다.

- **📢 섹션 요약 비유**: 인과 그래프는 자동차의 **배선도**와 같다. 전선(변수)이 어떻게 연결되어 있고, 어떤 스위치(개입)를 눌렀을 때 어느 전구(결과)에 불이 들어오는지 정확히 보여준다. 도구 변수는 이 배선도에서 **고장 난 교란 회로의 영향을 우회하는 보조 와이어** 역할을 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IV-DAG의 핵심은 **3개 노드(Z, X, Y) + 1개 교란노드(U)**로 구성된 구조적 인과 모델(Structural Causal Model, SCM)에서, $Z$를 통해 $X$의 외생 변동(Exogenous Variation)만을 추출하여 $X \rightarrow Y$의 인과 경로를 고립시키는 것이다.

```text
[IV-DAG 구조 및 2SLS 추정 흐름]

   +-------------------------------------------------------------+
   |                  Structural Causal Model                    |
   |                                                             |
   |       Z (도구/Instrument)                                    |
   |       |                                                     |
   |       | γ(≠0)                                               |
   |       v                                                     |
   |       X (내생 처치/Endogenous Treatment)                     |
   |       |                                                     |
   |       | β_causal (식별하고자 하는 인과효과)                  |
   |       v                                                     |
   |       Y (결과/Outcome)                                       |
   |                                                             |
   |  숨겨진 교란:                                                |
   |       U ---> X (Endogeneity)                                 |
   |       U ---> Y (Confounding)                                 |
   |                                                             |
   |  ※ 가정: Z ⊥ U (배제제약)                                   |
   +-------------------------------------------------------------+

   [2SLS 추정 단계]

   Stage 1:  X = π₀ + π₁·Z + ν          (First-Stage Regression)
             -> X_hat = π_hat₁ · Z       (예측값 도출)

   Stage 2:  Y = α + β·X_hat + ε        (Second-Stage Regression)
             -> β_IV, β_2SLS 추정
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :---|
| **노드(Node)**: $Z$ | 도구 변수(Instrument) | $X$에 대한 직접적 인과 효과 $\pi_1 \neq 0$ 존재, $Y$에 대한 직접 경로 부재, $U$와 통계적 독립. 실무 예: 풍속(광고 효과), 조기 우편 도달(정책), 거리/연도/계절성, Angrist-Krueger(1991) QB/QTM 변수 |
| **노드(Node)**: $X$ | 내생 처치 변수(Endogenous Treatment) | $U$로부터 영향을 받아 OLS 편향 발생, 1단계 회귀에서 $Z$로 설명되는 분산 $\text{Var}(\hat{X}\|Z)$이 클수록 효율적 추정. 1단계 $F$-통계량 $\geq 10$ (Staiger-Stock, 1997 규칙) |
| **노드(Node)**: $Y$ | 결과 변수(Outcome) | $X$로부터의 인과 경로 $\beta_{causal}$ 외 $U$를 통한 비인과 경로 존재. 잠재결과 프레임워크 $Y_i = Y_{1i} \cdot D_i + Y_{0i} \cdot (1-D_i)$에서의 관측 결과 |
| **노드(Node)**: $U$ | 비관측 교란변수(Unobserved Confounder) | $X \leftarrow U \rightarrow Y$의 Backdoor Path 생성. 역선택(Bias), 동시성 편향, 측정오차(Measurement Error)가 $U$의 실체. $do$-calculus의 Backdoor Adjustment $\sum_u P(Y\|x,u) P(u)$로 차단 시도하나 $U$ 미관측 시 직접 차단 불가 |
| **추정 알고리즘**: 2SLS | 도구 변수의 선형 추정량 | (1) $X$를 $Z$에 회귀하여 $\hat{X}$ 산출 (2) $\hat{X}$를 $Y$에 회귀하여 $\beta_{2SLS}$ 추정. $\hat{\beta}_{2SLS} = (Z'X)^{-1}Z'Y = (Z'Z)^{-1}Z'Y / (Z'Z)^{-1}Z'X = \text{Cov}(Z,Y)/\text{Cov}(Z,X)$ |
| **추정 알고리즘**: GMM | 과대식별(Over-ID) 상황 일반화 | 한계조건 $\mathbb{E}[Z \cdot \epsilon] = 0$을 최소 거리($\min \sum (Z'\epsilon)^2 W$)로 최소화. Hansen J-test로 과대식별 제약 검증. Hamiliton(2017) 기준 |
| **식별 프레임워크**: LATE/IV | 불이행(Non-Compliance) 하위그룹 효과 | Imbens-Angrist(1994) LATE Theorem: $\beta_{IV} = \mathbb{E}[Y_1 - Y_0 \| \text{Complier}]$ (도구에 반응하는 Complier 집단만의 인과효과) |
| **식별 프레임워크**: MTE | 한계처치효과 곡선 | Heckman-Vytlacil(2005): $\beta_{IV}(p) = \mathbb{E}[Y_1 - Y_0 \| U_D = p]$를 다양한 도구로 추정하여 ATE/ATT/LATE/TT 통합 복원 |

**핵심 수학적 구조**:

구조방정식 기준:
- $X_i = \pi_0 + \pi_1 Z_i + \gamma U_i + \nu_i$
- $Y_i = \alpha + \beta X_i + \delta U_i + \epsilon_i$

여기서 $\text{Cov}(Z_i, U_i) = 0$, $\text{Cov}(Z_i, \epsilon_i) = 0$, $\text{Cov}(\nu_i, \epsilon_i) = 0$ 가정.

OLS 추정 시 $\text{plim}\,\hat{\beta}_{OLS} = \beta + \frac{\text{Cov}(X, U) \cdot \delta}{\text{Var}(X)}$로 편향 발생.

IV 추정 시:
$$\beta_{IV} = \frac{\text{Cov}(Z, Y)}{\text{Cov}(Z, X)} = \frac{\text{Cov}(Z, \alpha + \beta X + \delta U + \epsilon)}{\text{Cov}(Z, X)} = \frac{\beta \pi_1 \sigma_Z^2 + \delta \text{Cov}(Z,U)}{\pi_1 \sigma_Z^2} \xrightarrow{\text{Cov}(Z,U)=0} \beta$$

**약도구(Weak Instrument) 문제**: $\pi_1$이 0에 가까우면 1단계 $F$-통계량이 작아져 2SLS의 편향이 OLS 편향의 $1/F$ 수준에 근접(Staiger-Stock 1997), 영편향 보정(LIML, Fuller estimator)을 고려해야 한다.

- **📢 섹션 요약 비유**: 도구 변수는 **마술사의 지팡이**와 같다. 마술사(교란 $U$)가 직접 보지도 못하면서, 관객에게 "카드($X$)가 바뀌었어!"라고 말하게 만드는 트릭($Z$)이 바로 도구 변수다. 지팡이가 카드를 만지는 힘($\pi_1$)이 약하면 트릭이 실패하고, 지팡이가 다른 카드(관측 불가능한 경로)에 영향을 주면 마술이 들통난다.

---

## Ⅲ. 비교 및 연결

| 구분 | **IV (도구 변수법)** | **PSM (성향점수 매칭)** | **RCT (무작위 통제 실험)** | **DiD (이중차분법)** | **RDD (회귀불연속설계)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **교란 통제 방식** | 도구 변수로 $U$ 우회적 차단 | $X$ 조건부로 $D \perp U$ 만족하도록 재가중 | 무작위 배정으로 $D \perp U$ 보장 | 시간불변(time-invariant) $U$ 제거 | $X$ 임계값 근방에서 국소적 무작위성 가정 |
| **필요 가정** | 관련성, 배제제약, 외생성 | 조건부 독립성(CIA), 공통지지(Common Support) | 완전 무작위, 순응(Compliance) | 평행추세(Parallel Trends) | 연속성, 국소 조작 불가(McCrary 검정) |
| **추정 대상** | LATE (Compliers) | ATT (Treated) | ATE (전체) | ATT (시간에 따른 변화분) | LATE (임계값 인근) |
| **편향 강건성** | 배제제약 위배 시 심각 | 비관측 교란 잔존 가능 | 가장 강건 (Gold Standard) | 추세 위배 시 편향 | 임계값 외삽 불가 |
| **데이터 요구** | 외생 변동원 $Z$ 필요 | 풍부한 공변량 $X$ 필요 | 실험 설계 및 통제권 | 패널/시계열 + 시점 정보 | 결정변수 + 임계값 규칙 |
| **실무 활용** | 마케팅 도구, 풍속, 조기 노출 | 관측 데이터 propensity 보정 | 신규 기능 출시, 정책 파일럿 | 정책 시행 전후 비교 | 학점/소득 임계값 효과 |

**다른 인과 추론 기법과의 결합**:
- **IV + 머신러닝**: Double Machine Learning(DML, Chernozhukov et al. 2018)은 도구 변수의 외생 변동과 ML 모델의 비선형성을 결합. Stage 1에서 $\hat{X} = f(Z, W)$ (ML 모델), Stage 2에서 $Y \sim \hat{X}$로 잔차 회귀하여 정규성 가정 없이 인과효과 추정.
- **IV + 베이지안**: 약도구 상황에서 사전분포($\pi_1 \sim \mathcal{N}(\mu, \tau^2)$)를 결합하여 강건 추정 (Conley-Hansen 2010, "plausibly exogenous" 프레임워크).
- **IV + 그래프 알고리즘**: DAG에서 도구 변수를 자동 탐색 (Bareinboim-Eaton 2014), $d$-separation 규칙으로 $Z \perp Y | X$를 만족하는 노드 집합 식별.
- **IV + A/B 테스트**: 네트워크 효과가 있는 경우 처치 $D_i$가 $D_j$의 결과에 누설(Peering/Spillover)될 때, hash-based IV(Manski 1993, Basse-Feller 2018)로 군집 무작위화 + 개인 변동 추출.

- **📢 섹션 요약 비유**: RCT는 완벽한 **온실에서 키운 식물**이고, IV는 **자연의 햇빛과 비 데이터를 활용해 야외에서 정원을 복원하는 기술**이다. 둘 다 같은 식물(인과효과)을 키우지만, 환경 제약이 다를 뿐 IV는 자연의 교란(교란변수) 속에서도 결과를 식별할 수 있게 해준다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**실무 시나리오별 적용 전략**:

1. **마케팅 믹스 모델링(MMM)**: 거시경제 시계열 데이터에서 광고비 인과효과 추정 시, 광고 노출 빈도가 낮은 시기/지역의 변동 또는 경쟁사 광고 단종 이벤트를 도구로 사용. 1단계 회귀에서 1차 자기상관(AR(1)) 조정 필요.
2. **의료/제약 데이터베이스 분석**: 의사의 처방 선호(Preference-Based IV)를 도구로 활용. 예: 1년 동안 해당 약물 처방 빈도가 중간값보다 높은 의사가 환자에게 처방할 확률.
3. **경제 정책 평가**: 양자역학에서
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 276 / 300

<- **이전**: [275. A/B 테스트 실험 설계 통계적 유의성 (A/B Testing Experiment Design Statistical Significance)](/studynote/14_data_engineering/05_exam_keywords/275_ab_testing/)
**다음**: [277. 데이터 윤리 편향 감지 공정성 평가 (Data Ethics Bias Detection Fairness Evaluation)](/studynote/14_data_engineering/05_exam_keywords/277_data_ethics_bias/) ->

---
