---
title: "277. 데이터 윤리 편향 감지 공정성 평가 (Data Ethics Bias Detection Fairness Evaluation)"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 윤리 편향 감지 공정성 평가는 ML 파이프라인(Data Ingestion -> Feature Engineering -> Model Training -> Serving) 전 단계에서 Statistical Parity Difference(SPD), Equalized Odds Ratio, Disparate Impact(4/5 Rule) 등 정량적 메트릭으로 Demographic Bias, Sampling Bias, Historical Bias, Measurement Bias를 측정하고, Pre-processing(Reweighing, Disparate Impact Remover), In-processing(Adversarial Debiasing, Exponentiated Gradient Reduction), Post-processing(Reject Option Classification, Calibrated Equalized Odds) 3-단계 Mitigation 전략을 통해 ε-fairness(ε ≤ 0.05)를 달성하는 MLOps 거버넌스 체계이다.
> 2. **가치**: IBM AI Fairness 360(AIF360), Microsoft Fairlearn, Google What-If Tool, Aequitas 등의 오픈소스 툴킷 활용 시 모델의 Protected Attribute(성별, 인종, 연령)별 TPR/FPR 격차를 평균 12~37% 감소시킬 수 있으며, EU AI Act(2024.08 시행)·AI 기본법(2026.01 시행)에 따른 High-Risk AI 시스템의 Conformity Assessment 통과 및 Algorithmic Audit 대응 시간을 약 65% 단축한다.
> 3. **판단 포인트**: Group Fairness(Demographic Parity, Equalized Odds)와 Individual Fairness(Similarity-based Lipschitz 조건)는 **Chouldechova(2017)·Kleinberg(2016) 불가능성 정리(Incompatibility Theorem)** 에 의해 Calibrated 조건 하에서 동시 달성 불가하므로, **도메인 맥락**(금융·의료·채용·사법)과 **Base Rate** 차이를 고려해 Fairness-Accuracy Trade-off(Accuracy Drop 0.5~3%)와 Explainability(XAI: SHAP, LIME) 간 우선순위를 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

기계학습 모델이 의료 진단, 신용 평가, 채용 스크리닝, 사법 리스크 분석 등 **High-Stakes 의사결정**에 적용되면서 학습 데이터에 내재된 역사적·사회적 편향이 모델 출력으로 그대로 전이되는 **Algorithmic Discrimination** 문제가 대두되고 있다. 2018년 Amazon의 성별 차별 채용 AI, 2019년 Apple Card의 성별 한도 차등 부여, 2020년 COMPAS 재범 위험 평가의 인종별 형량 불균형 등의 사건은 단순한 기술 오류를 넘어 **데이터 거버넌스·법적 책임·사회적 신뢰** 차원의 핵심 이슈로 격상되었다.

이에 EU는 2024년 8월 **AI Act(Regulation 2024/1689)** 를 통해 신용평가·채용·사법 등 High-Risk AI 시스템에 대해 **Bias Detection 의무화(Article 10)**, **Data Quality & Governance(Article 10)**, **Fundamental Rights Impact Assessment(FRIA, Article 27)** 를 법적 요건으로 명시하였고, 대한민국 역시 **인공지능 발전과 신뢰 기반 조성 등에 관한 기본법**(2024.09 제정, 2026.01 시행, 이하 "AI 기본법") 제31조(이용자의 권리), 제33조(고영향 인공지능 사업자의 의무)를 통해 High-Impact AI 사업자에게 **자동화된 의사결정에 대한 설명·이의 제기 권리 보장** 및 **위험관리 체계 구축**을 의무화하고 있다.

기술사적 관점에서 편향 감지와 공정성 평가는 **Model Risk Management(MRM)**, **Model Governance Framework(MGF)**, **AI Governance, Risk, and Compliance(AI GRC)** 의 핵심 구성요소이며, BCBS 239, SR 11-7, ECB Guide on Model Risk Management 등의 금융 규제 프레임워크와도 직접 연결된다.

```text
+------------------------------------------------------------------------+
|           End-to-End AI Lifecycle 내 편향·공정성 통합 거버넌스          |
+------------------------------------------------------------------------+
|                                                                        |
|  +---------+   +----------+   +----------+   +----------+   +------+|
|  | ① Data  |--->|② Feature |--->|③ Model   |--->|④ Eval   |--->|⑤ Svc ||
|  | Collection|   | Eng.     |   | Training |   | (Bias +  |   |Monitor||
|  |          |   |          |   |          |   | Fairness)|   |      ||
|  +----+----+   +----+-----+   +----+-----+   +----+-----+   +--+---+|
|       |             |             |             |             |    |
|       v             v             v             v             v    |
|  +----------------------------------------------------------------+  |
|  |           Fairness Layer (AIF360 / Fairlearn / Aequitas)        |  |
|  |  [Pre]        [In-processing]               [Post-processing]   |  |
|  |  Reweighing   Adversarial Debiasing         Reject Option       |  |
|  |  Sampling     Exponentiated Gradient        Calibrated EqOdds   |  |
|  |  DIRemover    Fairness Constraint           Equalized Odds      |  |
|  +----------------------------------------------------------------+  |
|       |             |             |             |             |    |
|       v             v             v             v             v    |
|  +----------------------------------------------------------------+  |
|  |        Monitoring & Audit  (Drift + Fairness Drift + XAI)       |  |
|  |   Evidently AI · Alibi Detect · SHAP · LIME · Integrated Grad |  |
|  +----------------------------------------------------------------+  |
|                                                                        |
|  Output: Model Card · Datasheet · AI Bias Impact Assessment (ABIA)     |
+------------------------------------------------------------------------+
```

과거에는 모델 성능 지표(Accuracy, AUC, F1)만을 사용해 모델을 평가하는 **Performance-Centric Paradigm** 이 지배적이었으나, 근래에는 **Fairness-aware Evaluation**, **Robustness**, **Privacy(SL, DP, FL)**, **Explainability** 를 동시 만족하는 **Responsible AI Paradigm** 으로 전환이 가속화되고 있다.

- **📢 섹션 요약 비유**: 편향 감지는 **거울 속 자화상 테스트**와 같다. 거울(모델)에 비친 모습이 실제 모습(사회적 공정성 기준)과 어디서, 얼마나 다르게 보이는지를 정밀하게 측정하고, 거울 자체를 갈아 끼우거나(Pre-processing) 시야각을 조정(In-processing)하거나 사진(예측 결과)을 보정(Post-processing)해 균형을 맞추는 전 과정이 필요한 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 편향의 7대 유형 (Seven Categories of Bias)

| 편향 유형 | 정의 | 발생 단계 | 전형적 사례 |
|:---|:---|:---|:---|
| **Historical Bias** | 사회·역사적 차별이 데이터에 이미 존재 | 데이터 생성기 | 성별 임금 격차 데이터로 학습한 채용 모델 |
| **Representation / Sampling Bias** | 모집단이 실제 분포를 반영하지 못함 | Data Collection | 모바일 기반 설문조사가 저소득층·고령층을 과소 대표 |
| **Measurement Bias** | Feature/Proxy 측정 방식의 체계적 오차 | Feature Engineering | 범죄율 = 검거율(과잉 단속 지역에서 부풀려짐) |
| **Aggregation Bias** | 이질적 하위집단을 단일 모델로 묶음 | Modeling | SNP별(서로 다른 민족) 의학 모델 통합 |
| **Learning Bias** | 모델이 부적절한 Proxy Feature에 의존 | Training | 우편번호 -> 인종 상관관계 학습 |
| **Evaluation Bias** | 벤치마크/테스트셋이 편향됨 | Evaluation | 얼굴 인식의 Faces-in-the-Wild 평가셋白人 편중 |
| **Deployment Bias** | 실제 사용 환경과 학습 환경 미스매치 | Serving | ICU 모델을 일반 병동에 적용 |

### 2. 공정성 수학적 정의 (Mathematical Fairness Notions)

편향 감지의 핵심은 **Protected/Sensitive Attribute** $A \in \{0, 1\}$ (예: 성별, 인종), **Label** $Y \in \{0, 1\}$, **Prediction** $\hat{Y} \in \{0, 1\}$ 사이의 확률적 관계를 정량화하는 것이다.

**① Demographic Parity (통계적 동등성, Dwork et al. 2012)**
$$
P(\hat{Y}=1 \mid A=0) = P(\hat{Y}=1 \mid A=1)
$$
- **Statistical Parity Difference (SPD)** = $P(\hat{Y}=1 \mid A=0) - P(\hat{Y}=1 \mid A=1)$
- **Disparate Impact (DI)** = $\frac{\min(P(\hat{Y}=1 \mid A=a))}{\max(P(\hat{Y}=1 \mid A=a))}$ -> **4/5 Rule**(EEOC 기준 DI ≥ 0.8)
- 한계: Base Rate 차이를 무시 -> 잘못된 양성 Equalization 위험

**② Equalized Odds (Hardt et al. 2016)**
$$
P(\hat{Y}=1 \mid A=0, Y=y) = P(\hat{Y}=1 \mid A=1, Y=y), \quad \forall y \in \{0, 1\}
$$
- TPR(재현율)과 FPR(위양성률)을 Protected Group 간 동등하게 유지
- **Equal Opportunity** = Equalized Odds 중 $Y=1$ (실제 양성) 조건만 만족

**③ Predictive Parity / Calibration (Chouldechova 2017)**
$$
P(Y=1 \mid \hat{Y}=1, A=0) = P(Y=1 \mid \hat{Y}=1, A=1)
$$
- 같은 예측 점수 -> 같은 실제 양성 확률

**④ Counterfactual Fairness (Kusner et al. 2017)**
$$
P(\hat{Y}_{A \leftarrow 0}(U) = y \mid X = x, A = a) = P(\hat{Y}_{A \leftarrow 1}(U) = y \mid X = x, A = a)
$$
- 인과 구조(SCM: Structural Causal Model) 기반: 반사실 개입 시 예측 불변

**⑤ Individual Fairness (Dwork et al. 2012)**
$$
d_Y(\hat{y}(x_i), \hat{y}(x_j)) \leq L \cdot d_X(x_i, x_j)
$$
- 유사한 개인은 유사한 예측을 받아야 함 (Lipschitz 조건)

```text
+------------------------------------------------------------------+
|        Fairness Metrics 계산 파이프라인 (AIF360 기준)             |
+------------------------------------------------------------------+
|                                                                  |
|   dataset (X, Y, A)                                              |
|        |                                                         |
|        v                                                         |
|   +----------------+    +----------------------------------+    |
|   | MetricDataset  |---->|  BinaryLabelDatasetMetric        |    |
|   | (privileged,   |    |  - SPD, DI, EOD, AOD, Theil Index|    |
|   |  unprivileged) |    +----------------------------------+    |
|   +--------+-------+                    |                        |
|            v                            v                        |
|   +----------------+    +----------------------------------+    |
|   |  Train & Pred  |---->|  ClassificationMetric             |    |
|   |  (y_pred)      |    |  - TPR_parity, FPR_parity, PPV,   |    |
|   +----------------+    |    NPV, FNR_parity, FDR_parity   |    |
|                         |  - Error Rate, Num Predictive      |    |
|                         +----------------------------------+    |
|                                       |                          |
|                                       v                          |
|                         +----------------------------------+    |
|                         |  Sample Distortion / Generalized  |    |
|                         |  Entropy Index · Differential     |    |
|                         |  Fairness (Fairlearn) · Causal    |    |
|                         |  Discrimination (DoWhy, EconML)  |    |
|                         +----------------------------------+    |
+------------------------------------------------------------------+
```

### 3. 3-Stage Mitigation 아키텍처

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Pre-processing** | 학습 전 데이터 자체를 변환해 편향 완화 | **Reweighing**(각 (A, Y) 조합에 가중치 부여), **Disparate Impact Remover**(Feature 간 그룹 분리 정보 projection으로 제거), **Learning Fair Representations(LFR, Zemel 2013)** — VAE 기반 인코더로 Latent Z에 비민감 표현 학습, **Optimized Preprocessing(Calandriello 2020)** — Distribution matching |
| **In-processing** | 학습 단계에서 Fairness Constraint / Penalty 직접 최적화 | **Exponentiated Gradient Reduction(EG, Agarwal 2018, Fairlearn)** — Lagrangian Duality로 ε-fairness 만족 분류기 앙상블, **Adversarial Debiasing(Zhang 2018, AIF360)** — Predictor와 Adversarial Network의 min-max 게임: $\min_\theta \mathbb{E}[L_{pred}] - \lambda \mathbb{E}[L_{adv}]$, **Fairness Constraint(Constrained Optimization)** — $\min L_{CE}$ s.t. $\text{SPD} \leq \epsilon$, **MetaFairClassifier** — Group vs Individual Fairness 자동 트레이드오프 |
| **Post-processing** | 학습 완료된 모델의 출력/임계값 조정 | **Reject Option Classification(Kamiran 2012)** — 임계영역($\theta \leq \hat{P}(Y) \leq 1-\theta$)에서 Privileged/Unprivileged 그룹에 반대로 라벨 부여, **Calibrated Equalized Odds(Pleiss 2017)** — 확률 보정 후 Randomized Threshold, **Equalized Odds Post-processing(Hardt 2016)** — Group별 $\hat{Y}$를 $Y, A$ 조건부 확률로 재매핑, **MultiAccuracy(Awasthi 2020)** — 부분집합별 정확도 보장 부스팅 |

```text
         +----------------------------------------------------+
         |      Bias-Fairness Trade-off 시각화 (Pareto)        |
         |                                                      |
         |  Accuracy | 100% + ●---------●                      |
         |           |      |             \                     |
         |           |  95% +              ●----●                |
         |           |      |                   \                |
         |           |  90% +                    ●               |
         |           |      |                  (Pareto Front)    |
         |           |  85% +                                   |
         |           |      +-----+-----+-----+-----+----->     |
         |           |          0%   5%   10%   15%   20%      |
         |           |             (1 - Demographic Parity)     |
         |           |                                           |
         |           |  선택: 도메인별 ε 임계치(보통 0.05)       |
         +----------------------------------------------------+
```

### 4. 핵심 알고리즘 의사코드

**Exponentiated Gradient Reduction (Fairlearn, Agarwal 2018)**
```
Input: Classifier M, Fairness constraint C (e.g., Demographic Parity),
       Learning rate η, Number of rounds T
Initialize: Q uniform distribution over hypotheses
For t = 1, ..., T:
    Sample classifier h_t ~ Q
    Compute loss ℓ_t(h_t) and constraint violation c_t(h_t)
    Q <- Q · exp(-η * ℓ_t) / Z_t       # Hedge algorithm
    Project Q onto constraint set {Q: E_Q[c] ≤ ε}
Output: Randomized classifier Q̅ = (1/T) Σ Q
```

**Adversarial Debiasing (AIF360)**
```
Parameter: Predictor θ_p, Adversary θ_a
Repeat:
    ŷ = Predictor(X; θ_p)
    ŷ_a = Adversary(ŷ, X; θ_a)        # A 예측 시도
    L_p = -log P(Y|ŷ)                 # Predictor 손실
    L_a
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 277 / 300

<- **이전**: [276. 인과 추론 도구 변수 인과 그래프 (Causal Inference Instrumental Variable DAG)](/studynote/14_data_engineering/05_exam_keywords/276_causal_inference/)
**다음**: [278. 개인정보 비식별화 가명처리 k-익명성 (De-identification Pseudonymization k-Anonymity)](/studynote/14_data_engineering/05_exam_keywords/278_de_identification/) ->

---
