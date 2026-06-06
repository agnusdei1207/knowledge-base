---
title: "Data Augmentation Synthetic Data Generation"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 증강(Data Augmentation)은 기존 데이터에 결정적·확률적 변환(CutMix, RandAugment, Mixup, Back-Translation 등)을 적용해 **입력 공간의 불변성(Invariance) 학습**을 유도하는 기법이며, 합성 데이터 생성(Synthetic Data Generation)은 **GAN, VAE, Diffusion Model, LLM** 등 생성 모델로 **결합분포 p(x,y)** 를 모사하여 학습 가능한 신규 데이터셋을 창조하는 메커니즘이다. 핵심 차이는 "원본 변환"인지 "분포 샘플링"인지에 있다.
> 2. **가치**: 의료(이미지 1,000건 -> 100,000건, AUC 0.78->0.92), 자율주행(실주행 1M km -> Sim2Real 100B km, 코너케이스 재현율 4%->78%), 금융(불균형 1:1000 -> 1:10, 재현율 Recall 0.32->0.87), LLM 파인튜닝(원본 1만 건 -> 합성 100만 건, MMLU 47->63) 등 **도메인·레이블 희소성·개인정보 규제(HIPAA, GDPR)** 문제를 정량적으로 해결한다.
> 3. **판단 포인트**: (a) **신선도(Freshness) vs 충실도(Fidelity) 트레이드오프** — 합성 데이터 품질이 낮으면 *편향 증폭(Compounding Bias)* 으로 역효과 발생, (b) **합성 비율(Synthetic-to-Real Ratio)** 최적점 존재(NeurIPS 2023 연구: 의료 영상 5:5가 9:1보다 downstream 성능 14% 우수), (c) **합성 데이터의 IP/저작권 책임 소재** — 생성 모델 학습 데이터 추론 시 원본 누출(Membership Inference Attack) 가능성에 대한 거버넌스 설계가 필수.

---

## Ⅰ. 개요 및 필요성

딥러닝 모델의 일반화 성능은 **데이터의 양·다양성·라벨 품질**의 세 가지 축에 의해 결정된다. 그러나 실제 산업 현장에서는 다음의 구조적 제약이 항상 존재한다.

- **레이블 희소성(Label Scarcity)**: 의학 영상 판독, 산업 불량 검출 등은 전문가 어노테이션 비용이 데이터 1건당 5만~50만 원 수준으로, 10만 건 확보 시 50억 원의 비용 발생.
- **긴 꼬리 분포(Long-tail Distribution)**: 사기 거래(0.02%), 제조 결함(0.001%), 자율주행 코너케이스(현실 주행 1억 km당 23건) 등 정상 데이터 대비 비정상 클래스의 출현 빈도가 극단적으로 낮음.
- **프라이버시 규제**: GDPR(2018), 개인정보보호법(2023 개정), HIPAA, EU AI Act(2024) 등은 특정 개인을 식별 가능한 원본 데이터의 활용을 제한 -> *데이터 18개 속성 중 3개 결합으로 87% 재식별 가능(Sweeney, 2002)*.
- **데이터 드리프트(Data Drift)**: 2020년 이후 COVID-19 이전 학습 모델의 성능이 의료·리테일 도메인에서 평균 23% 하락(Kaggle Data Drift Survey, 2021).

이에 대한 해법으로 **데이터 증강(기존 데이터 변환)**과 **합성 데이터 생성(신규 데이터 창조)**이 등장했으며, 2023년 Gartner는 *"2030년까지 AI 모델 학습 데이터의 60%가 합성적으로 생성될 것"*으로 전망했다.

```text
+--------------------------------------------------------------------+
|           데이터 확보의 구조적困境과 2대 해결 전략                  |
+--------------------------------------------------------------------+

   [실제 데이터 확보 시도]                  [전략적 우회]
          |                                       |
          v                                       v
   +-------------+                    +----------------------+
   | ① 수집비용  |-- 高 --> 포기 --> |  A. 데이터 증강       |
   | ② 라벨비용  |-- 高 --> 포기 --> |  (Data Augmentation) |
   | ③ 프라이버시|-- 規制 --> 차단 --> |  B. 합성 데이터 생성   |
   | ④ 코너케이스|-- 稀 --> 부족 --> |  (Synthetic Data Gen) |
   +-------------+                    +----------------------+
                                                  |
        +-----------------------------------------+------------+
        |                                                      |
        v                                                      v
  +----------------+                                  +----------------+
  |  데이터 증강     |                                  |  합성 데이터 생성  |
  |  (Augmentation) |                                  |  (Generation)    |
  |                |                                  |                 |
  | • 원본 x -> x'  |                                  | • p(x,y) -> x_new|
  | • 결정적 변환   |                                  | • 확률적 샘플링   |
  | • 라벨 보존     |                                  | • 신규 라벨 생성  |
  | • 1:N 맵핑     |                                  | • 0:N 생성       |
  +----------------+                                  +----------------+
        |                                                      |
        +--------------------+---------------------------------+
                             v
                    +-----------------+
                    |  다운스트림 모델  |
                    |  학습/검증/평가  |
                    |  (Downstream)   |
                    +-----------------+
```

기존 패러다임(2014 이전, AlexNet 이전)에서는 데이터 양을 **사람 손으로만** 늘렸으나, 2014년 AlexNet(1.2M ImageNet) 이후 *"더 많은 데이터 = 더 좋은 모델"*이라는 Scaling Law 가 정설로 자리잡았다. 이후 등장한 **증강(Augmentation) -> 생성(Generation) -> 시뮬레이션(Simulation) -> 인공 데이터 인테그리티(Provenance)** 의 진화는 단순한 트릭이 아닌 **학습 데이터 공학(Data Engineering for ML)** 의 새로운 영역을 형성했다.

- **📢 섹션 요약 비유**: 데이터 증강은 *한 권의 요리책을 7가지 방법으로 재해석하는 것*(같은 레시피, 다른 표현)이고, 합성 데이터 생성은 *전혀 새로운 레시피를 창작하는 것*(분포 자체를 모방). 둘 다 "데이터 부족이라는 주방"의 위기를 해결하는 방법이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 데이터 증강의 수학적 프레임워크

데이터 증강은 **결정적 변환 T: 𝒳 -> 𝒳** 와 **확률적 변환** 두 가지로 분류된다. 라벨 함수 f에 대해 **불변성(Invariance) 조건**이 성립해야 한다.

$$
\forall x \in \mathcal{X}, \; \mathcal{L}(f(T(x;\theta)), y) \approx \mathcal{L}(f(x), y)
$$

즉, 변환된 입력에 대한 모델 출력이 라벨과 동일하게 유지되어야 의미가 있다. 다음은 도메인별 핵심 증강 기법이다.

| 도메인 | 결정적 변환 | 확률적 변환 | 라벨 불변성 보장 |
| :--- | :--- | :--- | :--- |
| **비전(Vision)** | Flip(H/V), Crop, Resize(224->256), Pad, Rotate(±15°) | ColorJitter(±0.2), GaussianNoise(σ=0.01), Cutout/RandomErasing, Mixup(α=0.2), CutMix(α=1.0), RandAugment(N=2, M=10) | 기하학적 변환은 클래스 의미 보존, Mixup은 선형 보간 라벨 사용 |
| **NLP** | Lowercase, Whitespace 정규화 | Synonym Replace(WordNet, α=0.1), Random Insertion/Swap/Deletion, Back-Translation(en->ko->en), EDA(Easy Data Augmentation), Token Masking(BERT MLM 15%) | Back-Translation은 의미 보존율 85~92%, 의미역 변화 주의 |
| **음성/오디오** | Time Stretch(0.9~1.1x), Pitch Shift(±2 semitone) | SpecAugment(Freq Mask=27, Time Mask=100, n_mask=2), Noise Injection(SNR 0~15dB), Room Impulse Response Convolution | 피치 변동은 화자 독립 분류에 강건, 음성인식 ASR에는 왜곡 가능 |
| **시계열/센서** | Window Slicing, Jittering | Magnitude Warping, Scaling, Permutation(블록 셔플) | Permutation은 시계열 분류에서 순서 정보 손실 주의 |
| **그래프/3D** | 노드 Dropout, Edge Perturbation, Subgraph Sampling | Feature Masking, Point Cloud Rotation/Scaling, Frustum Sampling | 3D BBox 라벨은 회전 변환 후에도 유지되어야 함 |

### 2. 합성 데이터 생성의 4대 패러다임

```text
+----------------------------------------------------------------------+
|            합성 데이터 생성의 4대 생성 모델 아키텍처                    |
+----------------------------------------------------------------------+

  [1] GAN 계열 (2014~)            [2] VAE 계열 (2013~)
  +----------+                    +----------+
  | G(z;θ_G) |-x_fake-->+        |  Encoder |--μ,σ--+
  |  z~N(0,I)|          +->D --> |   q(z|x) |        |
  +----------+     L_adv|        +----------+        v
        ^          (minmax)                +----------+
  +------+--+                              |  Decoder |-x_recon
  | G's upd |                              | p(x|z)   |
  +---------+                              +----------+
                                          + KL(q(z)‖p(z))
  StyleGAN3, BigGAN,            β-VAE, CVAE, VQ-VAE
  conditional GAN,              (조건부 VAE, 텍스트->라벨)
  GauGAN/SPADE
                  |
                  v
  [3] Diffusion (2020~)          [4] Self-Supervision + LLM (2022~)
  +----------+                   +-------------------------+
  | x_T~N(0,I)|                  |  Foundation Model       |
  |   v 역확산 |                  |  (GPT-4, Llama, PaLM)   |
  |   ...    |                   |  + In-Context Learning   |
  |   x_t    |                   |  + Distillation          |
  |   v      |                   +------------+------------+
  |   x_0    |                                |
  +----------+                                v
  DDPM, DDIM,            Instruction-tuned LLM (Self-Instruct, Alpaca)
  Stable Diffusion,      -> (Prompt -> Synthetic Q&A Pair)
  Imagen, DALL-E 3       -> 품질: GPT-4 Self-Rewarding
```

**핵심 알고리즘 — Conditional Tabular GAN (CTGAN, 2019)** 은 합성 데이터의 사실적 사례이다. SDV(Synthetic Data Vault) 라이브러리에 구현된 핵심 아이디어는 다음과 같다.

```python
# CTGAN 핵심 (Xu et al., 2019, NeurIPS)
# 1) Mode-Specific Normalization (이산/연속 혼합 컬럼 처리)
#    - 연속 변수: v -> α·v + β (각 모드별로 가우시안 피팅, 5-mode GM)
#    - 범주 변수: One-hot -> embedding (dim=128)
#
# 2) Conditional Generator (조건부 샘플링)
#    - P(row|mask) = (Pa_c · P(cond)) / Σ  (m-PACGAN)
#    - mask_generator: 0/1 벡터로 어떤 컬럼을 생성할지 결정
#    - sample_condition: 희소 범주 균형 샘플링 (log-frequency)
#
# 3) Loss = α·WGAN-GP + β·CrossEntropy(cond)
#    - L_GAN: Critic 네트워크의 Wasserstein-1 거리
#    - L_Info: 조건 정보 손실 (cond 정보 보존)
#
# 생성:  z ~ N(0,I)^128 + cond(c) -> G -> (연속값, 범주 softmax) -> x_synth
# 평가:  KS-test(연속), TVD(이산), DCR(거리 to Closest Record)
```

### 3. 품질 평가 메트릭 체계

합성 데이터는 "비슷한 만큼" 좋아야 하지만, *너무 비슷하면 원본 누출(Leakage)* 이 발생한다. 다음 다층 평가 프레임워크가 필요하다.

```text
+----------------------------------------------------------------+
|              합성 데이터 품질 평가 4-Layer Framework            |
+----------------------------------------------------------------+
   Layer 1: 통계적 유사도 (Fidelity)
   ---------------------------------
   • FID (Fréchet Inception Distance) — 비전, v 좋음
       FID = ‖μ_r - μ_s‖² + Tr(Σ_r + Σ_s - 2(Σ_rΣ_s)^{1/2})
   • MMD (Maximum Mean Discrepancy) — RBF Kernel
   • KS-test p-value ≥ 0.05, Wasserstein Distance
   • 컬럼별 Marginal: PDF/CDF 비교, Correlation Matrix L1 dist

   Layer 2: 실용성 (Utility)
   ------------------------
   • TSTR (Train on Synthetic, Test on Real)
   • TRTR (Train on Real, Test on Real) = Upper Bound
   • Downstream ML: F1, AUC, RMSE 차이 < 5% 이상이면 실용
   • 5-fold CV, Permutation Feature Importance 비교

   Layer 3: 프라이버시 (Privacy)
   -----------------------------
   • DCR (Distance to Closest Record): min‖x_real - x_synth‖
       - DCR < 5th percentile -> 누출 가능성
   • MIA (Membership Inference Attack) 성공률 ≤ 55%
   • Attribute Inference Attack
   • ε-Differential Privacy 보장 여부

   Layer 4: 공정성/편향 (Fairness)
   -------------------------------
   • Demographic Parity, Equalized Odds
   • Synthetic-only bias amplification 측정
       bias_amp = |DP(synth) - DP(real)| / DP(real)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **원본 데이터셋 (𝒟_real)** | 학습 입력 | Tabular(SDV, CTGAN), Image(DiGAN, StyleGAN3), Text(GPT-4 Self-Instruct), Time-series(TimeGAN) |
| **생성 모델 (Generator G)** | 신규 데이터 샘플링 | VAE(z->x), GAN(minmax), Diffusion(역확산 step), LLM(다음 토큰 예측); 하이퍼파라미터: z_dim=128, batch=512, lr_G=1e-4, lr_D=4e-4, β1=0.5, β2=0.9 |
| **조건부 입력 (Condition c)** | 라벨/속성 통제 | Class-conditional GAN, cGAN(Concatenation), CVAE, Guidance Scale(w=7.5 in Diffusion) |
| **품질 평가 모듈** | 생성->배포 게이트 | FID, TSTR/TRTR, DCR, MIA; 자동 reject 시 임계값: FID>50, DCR<5th pct -> 폐기 |
| **거버넌스/Provenance** | 라이프사이클 추적 | 데이터카드(Data Card), 모델카드(Model Card), C2PA(Content Authenticity), DVC(데이터 버전 관리) |

**하이퍼파라미터 영향 분석 — Diffusion 기반 이미지 합성의
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 273 / 300

<- **이전**: [272. 데이터 레이블링 어노테이션 능동 학습 (Data Labeling Annotation Active Learning)](/studynote/14_data_engineering/05_exam_keywords/272_data_labeling/)
**다음**: [274. 데이터 드리프트 모니터링 분포 변화 탐지 (Data Drift Monitoring Distribution Shift Detection)](/studynote/14_data_engineering/05_exam_keywords/274_data_drift/) ->

---
