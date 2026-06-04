+++
title = "294. 자동 ML 하이퍼파라미터 NAS 탐색 (AutoML Hyperparameter NAS Search)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AutoML(Automated Machine Learning)은 **탐색 공간(Search Space)**, **탐색 전략(Search Strategy)**, **성능 추정(Performance Estimation)**의 3대 축을 통해 모델 아키텍처(NAS)와 학습 하이퍼파라미터(HPO)를 알고리즘적으로 최적화하는 메타학습 프레임워크로, DARTS, Bayesian Optimization(BOHB, TPE), Reinforcement Learning(PPO 기반 Controller), Evolutionary(NSGA-II) 등 탐색 패러다임이 수렴·분기하는 영역이다.
> 2. **가치**: 수동 튜닝 대비 **엔지니어링 비용 70~90% 절감**, **모델 정확도 1~5%p 향상**, **탐색 시간 10~100배 단축**(weight-sharing, low-fidelity proxy 기반 시), NASNet·EfficientNet·MobileNetV3 등 SOTA 모델의 자동 도출을 통해 휴리스틱 설계의 한계를 극복한다.
> 3. **판단 포인트**: **탐색 공간 정의의 폭**(macro vs cell-based), **비용 함수 설계**(FLOPs·지연시간 제약), **탐색-추론 간의 transferability**(proxy task 신뢰도), **재현성 보장**(seed locking, weight sharing 안정성), **멀티 오브젝트 trade-off**(정확도 vs latency vs 메모리) 설정이 시험 출제 핵심이며, 실무에서는 **proxy 모델 + 베이지안 + early stopping** 하이브리드 전략이 표준이다.

---

## Ⅰ. 개요 및 필요성

딥러닝 모델의 성능은 **알고리즘 자체**(Network Topology, Loss Function)뿐 아니라 **학습 환경**(Learning Rate, Batch Size, Optimizer, Regularization) 및 **아키텍처 구조**(Skip Connection, Depth, Width, Expansion Ratio)에 의해 결정되며, 이를 통칭해 **구성요소(Hyperparameter + Architecture)**라 한다. 그러나 ResNet-50만 하더라도 약 38개의 명시적·암묵적 하이퍼파라미터를 가지며, Transformer 계열은 50개 이상으로 폭증한다. 이를 **휴리스틱과 grid search로 수동 튜닝**하는 전통적 방식은 **조합 폭발(Combinatorial Explosion)** 문제로 인해 사실상 한계에 도달했다.

특히 2017년 NASNet(Google), 2018년 DARTS(Liu et al.) 이후 SOTA 모델 설계는 **"사람이 설계한다"는 전제**를 버리고 **탐색 알고리즘이 데이터로부터 최적 구조를 도출**하는 패러다임으로 전환되었다. AutoML은 (1) **Feature Engineering 자동화**(AutoFE), (2) **HPO 자동화**(AutoML-Hyper), (3) **NAS 자동화**(AutoML-Architecture), (4) **Pipeline 자동화**(CASH: Combined Algorithm Selection and Hyperparameter optimization)의 4단계로 분류되며, 본 노트는 (2)와 (3)에 초점을 맞춘다.

```text
[AutoML의 진화 단계와 탐색 비용]

   2013           2016           2017           2018           2020~현재
    |              |              |              |              |
   Grid        Random/       Bayesian        DARTS       Zero-cost Proxy
   Search      Hyperopt      (TPE/BOHB)    Differentiable   + NAS-Bench
    |              |              |              |              |
    v              v              v              v              v
 +------+     +------+     +------+     +------+     +----------+
 | O(10²)|    | O(10³)|    | O(10⁴)|    | O(10⁵)|    | O(10⁶+)  |
 | 수동  |    | 무작위 |    | 모델  |    | 1-shot |    | 메타학습  |
 +------+     +------+     +------+     +------+     +----------+
  100GPU-day    10GPU-day     1GPU-day     0.5GPU-day    0.1GPU-day
   (ResNet)     (VGG)        (DenseNet)    (DARTS)      (DrNAS)
```

**기존 패러다임의 한계**:
- **수동 설계자의 편향(Inductive Bias)**: 인간이 "Conv -> BN -> ReLU" 패턴에 익숙해 새로운 토폴로지 탐색 불가
- **Grid Search의 차원의 저주**: 차원 수 d에 대해 O(k^d)로 확장되며, 대부분의 영역이 **Non-convex, Non-smooth**하여 해석적 최적점 도출 불가
- **Reproducibility Crisis**: 동일 하이퍼파라미터라도 seed, hardware determinism에 따라 결과 변동 2~3%p

**AutoML/NAS의 등장 배경**:
- GPU 클러스터 비용 절감(20,000 GPU-hour -> 4 GPU-hour, DARTS 기준)
- 1-shot NAS 등장으로 **수천 개의 sub-network를 단일 Supernet에 weight-sharing**하여 비용 급감
- **Neural Architecture Space**는 연속적(continuous)으로 relaxation 가능 -> Gradient 기반 최적화 적용

- **📢 섹션 요약 비유**: 마치 **수천 가지 레시피(파스타, 짜장, 카레, 비빔밥)** 중 어떤 조합이 손님에게 가장 맛있는지 일일이 요리하지 않고도, **AI 셰프가 시식 데이터(맛 점수)를 학습**하여 자동으로 새 레시피를 창작해내는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

AutoML의 핵심은 **3대 컴포넌트**(Elsken et al., 2019)의 상호작용으로 정의된다. 본 섹션에서는 HPO와 NAS의 통합 아키텍처를 도식화하고, 각 컴포넌트의 알고리즘적 메커니즘을 분해한다.

```text
[AutoML HPO+NAS 통합 아키텍처: Controller-Supernet-Evaluator 3-Tier 구조]

   +-----------------------------------------------------------------+
   |  Tier 1: Search Space Controller (탐색 공간 + 전략)             |
   |  +-----------------------------------------------------------+  |
   |  | HPO Space: lr ∈ [1e-5, 1e-1]  |  batch ∈ {32,64,128,256}|  |
   |  |            wd ∈ [1e-8, 1e-3] |  dropout ∈ [0, 0.5]      |  |
   |  | NAS Space: op ∈ {SepConv3x3, DilConv5x5, Skip, Zero, ...}|  |
   |  |            edge ∈ DAG: 7 nodes × 14 edges = O(10⁹)       |  |
   |  +-----------------------------------------------------------+  |
   |                          v                                      |
   |  +-----------------------------------------------------------+  |
   |  |  Search Strategy: Bayesian(BOHB) | Evolutionary(NSGA-II) |  |
   |  |                    RL(PPO Controller) | Gradient(DARTS)   |  |
   |  +-----------------------------------------------------------+  |
   +-----------------------------------------------------------------+
                                  | Sample candidate
                                  v
   +-----------------------------------------------------------------+
   |  Tier 2: Performance Estimator (추정 전략)                       |
   |  +--------------+  +--------------+  +----------------------+  |
   |  | Low-fidelity  |  | Learning     |  | Weight-Sharing        |  |
   |  | Proxy         |  | Curve Extra- |  | Supernet (1-shot)     |  |
   |  | (CIFAR-10,    |  | polation     |  | (ENAS, DARTS,         |  |
   |  |  few epochs)  |  | (LCE,        |  |  ProxylessNAS)        |  |
   |  |               |  |  SPE)        |  |                       |  |
   |  +--------------+  +--------------+  +----------------------+  |
   +-----------------------------------------------------------------+
                                  | Validation accuracy + cost
                                  v
   +-----------------------------------------------------------------+
   |  Tier 3: Decision Engine (결정 엔진)                              |
   |  +--------------------+        +----------------------------+  |
   |  | Single-obj: argmax |   or   | Multi-obj: Pareto Front    |  |
   |  |  acc(θ)            |        |  (acc, latency, FLOPs,     |  |
   |  |  (BO surrogate)    |        |   energy, memory)          |  |
   |  +--------------------+        +----------------------------+  |
   +-----------------------------------------------------------------+
                                  | Best architecture θ*
                                  v
                       [Retrain from scratch & Deploy]
```

### 2.1 주요 구성 요소 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Search Space (탐색 공간)** | 후보 모델·하이퍼파라미터 집합 정의 | **Chain-structured**(VGG-like): layer-by-layer stack / **Cell-based**(NASNet, DARTS): Normal Cell + Reduction Cell을 분리하여 transferable 구조 탐색 / **Hierarchical**: 모듈-블록-레이어 3단계(예: NAS-FPN) / **Macro/Micro**: Micro는 operation-level(mbconv, sepconv), Macro는 connectivity-level(어떤 노드 연결). 일반적으로 **DARTS**는 8 ops × 14 edges = 약 10⁹개 후보. |
| **Search Strategy (탐색 전략)** | 후보 샘플링 규칙 | (1) **Gradient-based(DARTS)**: softmax-mixed op α·W를 bi-level 최적화(∇_α val_loss(∇_w train_loss)). (2) **Reinforcement Learning**: PPO/A3C Controller가 token sequence로 architecture sampling, reward = validation accuracy(REINFORCE: ∇J = E[R·∇log p(θ)]). (3) **Evolutionary(NSGA-II, NSGA-Net, AmoebaNet)**: Tournament selection + mutation/crossover, **non-dominated sorting**으로 Pareto front 유지. (4) **Bayesian(BOHB, TPE)**: TPE(Tree-structured Parzen Estimator)는 l(x)/g(x) likelihood ratio로 promising region sampling, BOHB는 Hyperband(미니 Successive Halving)와 결합. |
| **Performance Estimator (성능 추정)** | 후보의 성능을 빠르고 정확히 예측 | **Weight Sharing**이 핵심: 모든 sub-network가 Supernet의 가중치를 공유하여 개별 학습 없이 forward pass 1번으로 성능 근사. **Low-fidelity Proxy**는 작은 데이터셋(CIFAR-10 -> ImageNet)·짧은 epoch로 비용 절감. **Zero-Cost Proxy**(synflow, jacob_cov, grasp)는 **초기화 시점 가중치 통계만으로 점수 예측**(수 초 내). **Learning Curve Extrapolation**(LCE, SPE, AlphaEarth)는 부분 학습 곡선으로 최종 accuracy 외삽. |
| **Decision Engine (결정 엔진)** | 최종 아키텍처 선택 | **Single-objective**: argmax acc(θ) with constraints(FLOPs ≤ T). **Multi-objective**: NSGA-II의 **Pareto dominance** + **Crowding distance**로 latency-accuracy trade-off 곡선 도출(MnasNet, FBNet, MobileNetV3, ChamNet). 실무에서는 **Hard constraint**(latency < 30ms on Pixel 2) + **Soft objective**(α·ACC + (1-α)·(-LAT)) 혼합 사용. |

### 2.2 핵심 알고리즘 메커니즘

**(1) DARTS (Differentiable Architecture Search) - 핵심 수식**

$$\min_\alpha \mathcal{L}_{val}(w^*(\alpha), \alpha) \quad \text{s.t.} \quad w^*(\alpha) = \arg\min_w \mathcal{L}_{train}(w, \alpha)$$

이 bi-level 최적화는 다음의 1차 근사로 풀린다:

$$w' = w - \xi \nabla_w \mathcal{L}_{train}(w, \alpha)$$
$$\alpha' = \alpha - \eta \nabla_\alpha \mathcal{L}_{val}(w', \alpha)$$

Operation mixing은 discrete한 후보를 **continuous relaxation**으로 변환:

$$\bar{o}^{(i,j)}(x) = \sum_{o \in \mathcal{O}} \frac{\exp(\alpha_o^{(i,j)})}{\sum_{o'} \exp(\alpha_{o'}^{(i,j)})} \cdot o(x)$$

여기서 α ∈ R^(|E|×|O|)는 mixed op 가중치이며, 학습 후 가장 큰 α를 갖는 op를 최종 선택(derive discrete architecture).

**(2) BOHB (Bayesian Optimization + Hyperband)**

BOHB는 **BO**의 모델 기반 샘플링과 **HB**의 자원 적응적 할당을 결합한다:
- BO 부분: TPE로 l(x), g(x) kernel density estimator를 구성, **EI(Expected Improvement)** 기반 acquisition
- HB 부분: min_{i} Budget b_i = {1, 3, 9, 27, ...} epoch에서 Successive Halving으로 **성능 하위 1/η 후보 조기 종료**(η=3, s_max=4, B_max=81 epochs)
- 수식: $S_{max} = \lfloor \log_{\eta}(B_{max}) \rfloor$, min-budget = $\eta^{s_{max}}$

**(3) NSGA-Net (Evolutionary Multi-objective NAS)**

Pareto dominance 기준:
- **Rank 1**: 다른 모든 해집합에 의해 지배되지 않는 해 (non-dominated)
- **Crowding distance**: 같은 rank 내 분산 정도

$c_i = \sum_{m=1}^{M} \frac{|f_m^{(i+1)} - f_m^{(i-1)}|}{f_m^{max} - f_m^{min}}$

이 두 기준이 selection pressure를 형성하고, **tournament selection**(size=2) + **bit-flip mutation** + **uniform crossover**로 다음 세대 생성.

### 2.3 탐색 파이프라인의 세부 단계

```text
[Standard AutoML Pipeline: Sample -> Train -> Estimate -> Update]

  +------------+
  |  (S0) Init  |  <- Initial samples (Sobol sequence or random)
  |  10 samples |
  +-----+------+
        |
        v
  +------------+
  |  (S1) Sample|  <- BO/RL/Evolutionary generates (arch, hp) tuple
  |  candidate  |     e.g., {SepConv5x5 @ edge 3-5, lr=3e-4, wd=5e-5}
  +-----+------+
        |
        v
  +------------+
  |  (S2) Train |  <- Weight-shared Supernet or independent sub-network
  |  & evaluate |     epochs: 50 (CIFAR-10 proxy)
  +-----+------+
        |
        v
  +------------+
  |  (S3) Update|  <- Surrogate model (GP/TPE) or Controller policy
  |  Surrogate  |     or Population archive (NSGA-II)
  +-----+------+
        |
        v
  +------------+
  |  (S4) Repeat|  <- Until budget exhausted (GPU-day, wall-clock, or
  |  S1~S3      |     convergence criterion: |Δacc| < 0.001 for k iter)
  +-----+------+
        |
        v
  +------------+
  |  (S5) Derive|  <- Take top-K from Pareto front, retrain from scratch
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 294 / 300

<- **이전**: [293. 데이터 관측 가능성 이상 탐지 SLO (Data Observability Anomaly Detection SLO)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/293_data_observability/)
**다음**: [295. LLMOps 대규모 언어 모델 운영 관리 (LLMOps Large Language Model Operations)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/295_llmops/) ->

---
