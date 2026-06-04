+++
title = "408. AI 보안 적대적 공격 방어 전략 (AI Security Adversarial Attack Defense)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 적대적 공격(Adversarial Attack)은 모델 그래디언트·결정 경계를 교란하는 L∞/L2 노이즈 perturbation(ε-bound, FGSM·PGD·C&W), 데이터셋 백도어(Triggered Poisoning) 및 모델 추출(Model Stealing)·인버전(Inversion) 공격으로 구성되며, 방어 전략은 **Adversarial Training(AT)**, **Randomized Smoothing(Certified Defense)**, **Defensive Distillation**, **Input Preprocessing(Denoising/Sanitization)**, **Detection-based Defense(MagNet, Feature Squeeze)** 등 다층 방어(Defense-in-Depth) 체계를 통해 ε-perturbation 하에서의 Robust Accuracy를 최대화하는 것이 핵심이다.
> 2. **가치**: Robust Accuracy 40%→82%(PGD-AT, ε=8/255 CIFAR-10 기준), Certified Radius r=1.5@95% 보장(Randomized Smoothing), 탐지 latency 12ms 이내로 실시간 차단 가능(MagNet), NIST AI RMF·EU AI Act·국내 AI기본법(2026.1 시행) 컴플라이언스 충족을 통한 비즈니스 리스크 60%↓, MLOps 파이프라인 통합 시 모델 신뢰성 SLA 99.9% 달성.
> 3. **판단 포인트**: ① **방어 기법 선택 trade-off**(Adversarial Training: 정확도↓ 10~15% vs Robustness↑ vs 학습 비용 3~5×), ② **공격 표면 분류**(Evasion vs Poisoning vs Inference Threat Model), ③ **L∞/L2/L0 노름 기준 및 ε-budget** 결정, ④ **White-box vs Black-box 공격 가정**, ⑤ **인퍼런스 지연(latency) vs Robustness** 균형, ⑥ **설명가능성(XAI)·프라이버시(DP)·페어니스**와 Robustness의 통합 거버넌스 설계.

---

## Ⅰ. 개요 및 필요성

딥러닝 모델은 **입력 공간의 고차원 비선형성**과 **결정 경계의 국소적 취약성**으로 인해, 사람 눈에는 인지 불가능한 미세한 perturbation(ε ≤ 8/255, 픽셀당 0~1 정규화 기준)만으로 오분류를 유도할 수 있다. 2013년 Szegedy 등이 처음 보고한 Adversarial Example 현상은 이후 **자율주행(Tesla 차선 인식 오류, 2019)**, **의료 영상(악성/양성 오진, Nature Medicine 2021)**, **악성코드 분류기 우회(DeepLocker, IBM 2018)**, **얼굴인식 시스템 위장(Surveillance evasion)**, **LLM Prompt Injection(ChatGPT DAN, 2023)** 등 실 환경에서 다수 확인되며 AI 시스템의 신뢰성·안전성·보안 패러다임 자체를 재정의하고 있다.

특히 **생성형 AI(LLM) 시대**에 진입하면서, 적대적 공격은 단순 이미지 perturbation을 넘어 **① Jailbreak(시스템 프롬프트 우회)**, **② Indirect Prompt Injection(외부 문서/RAG 데이터 오독)**, **③ Training Data Extraction(개인정보/학습 데이터 유출)**, **④ Model Supply Chain Poisoning(HuggingFace 모델 백도어)** 등 **공격 표면(Attack Surface)**이 폭발적으로 확장되었다. MITRE ATLAS(2024 v4.0)에는 14개 Tactics, 66개 Techniques가 등재되어 전통 사이버 킬체인(MITRE ATT&CK)과 매핑되며, AI Red Teaming은 단순 모의 침투를 넘어 **모델 거버넌스의 필수 절차**로 자리잡았다.

기존 ML 파이프라인(Scikit-learn 기반)에서는 robust optimization이 선택 사항이었으나, **MLSecOps·Secure AI Lifecycle**로 전환되면서 **데이터 수집→라벨링→학습→배포→모니터링** 전 단계에 adversarial validation이 의무화되고 있다. EU AI Act(2024.8 시행, 고위험 AI 분류 시 Robustness 인증 의무), NIST AI RMF 1.0(2023.1), 국내 「인공지능 기본법」(2026.1 시행, 신뢰성·투명성 의무화)이 모두 Robustness를 핵심 통제 항목으로 명시하고 있어, 기술사 관점에서 **AI Risk = f(Adversarial Robustness, Privacy, Fairness, Explainability, Safety)** 통합 프레임워크 설계 역량이 요구된다.

```text
  ┌──────────────────────────────────────────────────────────────────────┐
  │          AI Security Threat Landscape (공격 표면 진화)                │
  └──────────────────────────────────────────────────────────────────────┘

   2013 ─────── 2017 ─────── 2020 ─────── 2023 ─────── 2025+ ───────▶
   Szegedy      Madry         DeepLocker   LLM Jailbreak  Agentic AI
   FGSM         PGD-AT        BadNets      Prompt Inje.    Tool-Use Exfil
   L-BFGS       C&W           Trojaning    Model Steal     Multi-Modal
   │            │             │            │               │
   ▼            ▼             ▼            ▼               ▼
   [단순        [강화학습형     [공급망       [생성형 AI      [자율 AI 에이전트
    노이즈]      적대학습]      백도어]       신 위협]        오용·남용]

  ┌─────────────────────────────────────────────────────────────────┐
  │  공격 유형 매트릭스 (Threat Model Taxonomy)                       │
  ├────────────┬─────────────┬──────────────┬──────────────────────┤
  │ 분류       │ 공격 목표    │ 대표 기법     │ 영향 영역             │
  ├────────────┼─────────────┼──────────────┼──────────────────────┤
  │ Evasion    │ 오분류 유발  │ FGSM,PGD,C&W │ Inference-time       │
  │ Poisoning  │ 백도어 삽입  │ BadNets,Blnd │ Training-time        │
  │ Model Inv. │ 학습데이터복원│ MIA,DLG      │ Privacy 위반         │
  │ Model Stl. │ API 지식추출 │ Knockoff,JS  │ IP 침해              │
  │ Backdoor   │ 조건부오작동 │ Trojan,Sleep │ Supply Chain         │
  │ Extraction │ 프롬프트탈취 │ Prefix Inj.  │ LLM Jailbreak        │
  └────────────┴─────────────┴──────────────┴──────────────────────┘

  ┌───────────────────────────────────────────────────────────────┐
  │  전통 보안 vs AI 보안 패러다임 비교                            │
  ├────────────────────┬──────────────────────────────────────────┤
  │ 전통 사이버보안     │ AI·ML 보안                               │
  ├────────────────────┼──────────────────────────────────────────┤
  │ 시그니처/규칙 기반  │ 그래디언트/최적화 기반                     │
  │ 정적 위협 모델      │ 적대적/능동적 위협 모델                    │
  │ 경계 방어(Perimeter)│ 모델 중심 방어(Model-centric)             │
  │ Patch·Signature Update│ 재학습·Robust Retraining (주기적)     │
  │ 영향: 시스템 침해    │ 영향: 의사결정 오류·안전사고·사회적 편향  │
  └────────────────────┴──────────────────────────────────────────┘
```

**기존 vs 신규 패러다임**: 전통적 사이버보안이 **"알려진 악성코드 시그니처 차단"** 중심이었다면, AI 보안은 **"알 수 없는 입력에 대한 결정 경계의 수학적 보장"** 중심이다. 시그니처가 없는 0-day 적대적 입력(Adversarial Example)까지 방어해야 하므로 **확률적 인증 방어(Certified Defense)**, **게임이론 기반 min-max 최적화(Madry's Robust Optimization)**, **인퍼런스 시점 다중 분류기 앙상블** 등 새로운 보안 수학이 요구된다.

- **📢 섹션 요약 비유**: 적대적 공격은 **"안경점에 뿌려진 보이지 않는 먼지"**와 같다. 일반인(사람)에게는 깨끗해 보이지만, AI 모델(고감도 광학센서)에게는 **결정 경계가 흔들려** 전혀 다른 물체로 인식하게 만드는 미세 교란이다. 방어 전략은 이 **"보이지 않는 먼지"**에 대해 **광학 코팅(전처리)**, **다중 렌즈 비교(앙상블)**, **센서 자체 보정(적대적 재학습)** 등 다층 필터를 적용하는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. 적대적 공격의 수학적 정의

주어진 분류 모델 f_θ: X → Y, 입력 x ∈ X, 정답 y ∈ Y에 대해 **적대적 예제** x' = x + δ는 다음 조건을 만족한다:

```
         ‖δ‖_p ≤ ε  (perturbation budget, p ∈ {0, 1, 2, ∞})
         f_θ(x') ≠ y   (공격 성공)
```

**대표 공격 알고리즘**:
- **FGSM**(Fast Gradient Sign Method, Goodfellow'14): δ = ε · sign(∇_x L(θ, x, y))
- **PGD**(Projected Gradient Descent, Madry'18): FGSM을 k-iteration 반복, x_t+1 = Π_{B(x,ε)} (x_t + α · sign(∇_x L))
- **C&W**(Carlini & Wagner'17): min ‖δ‖_p + c · f(x+δ) (최적화 기반, 가장 강력)
- **DeepFool**(Moosavi-Dezfooli'16): 결정 경계까지의 최소 거리
- **AutoAttack**(Croce&Hein'20): APGD-CE + APGD-T + FAB-T + Square Attack 앙상블 (현재 SOTA 평가 벤치마크)

### B. 방어 전략 아키텍처 (Layered Defense)

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │      AI Adversarial Defense-in-Depth Architecture                    │
  └─────────────────────────────────────────────────────────────────────┘

   입력 x (정상/적대적) ──▶ ┌─────────────────────────────┐
                            │  Layer 1: 입력 검증·전처리    │
                            │  (Input Sanitization)        │
                            │  • JPEG 압축 / Feature Sq.   │
                            │  • Denoising Autoencoder     │
                            │  • Spatial Smoothing (Gaussian)
                            │  • Pixel Deflection / TVM    │
                            └──────────┬──────────────────┘
                                       │ x_clean
                                       ▼
                            ┌─────────────────────────────┐
                            │  Layer 2: 탐지 (Detection)   │
                            │  • MagNet (Detector)         │
                            │  • NIC (Neural Invariant)    │
                            │  • Feature Squeeze (Binary)  │
                            │  • Activation Clustering     │
                            │  • LID (Local Intrinsic Dim) │
                            └──────────┬──────────────────┘
                                       │ 정상 분류 입력
                                       ▼
                            ┌─────────────────────────────┐
                            │  Layer 3: Robust Model       │
                            │  • PGD-AT / TRADES / MART   │
                            │  • Defensive Distillation    │
                            │  • Randomized Smoothing      │
                            │  • Deep Ensembles            │
                            │  • Lipschitz-bounded Net     │
                            └──────────┬──────────────────┘
                                       │ ŷ (예측)
                                       ▼
                            ┌─────────────────────────────┐
                            │  Layer 4: 인증 방어·모니터링  │
                            │  • Certified Radius Check    │
                            │  • Prediction Consistency    │
                            │  • Model Watermarking        │
                            │  • Drift & Outlier Alerting  │
                            │  • MLOps Audit Trail         │
                            └─────────────────────────────┘

  ┌───────────────────────────────────────────────────────────────┐
  │  Robust Optimization (Madry's Framework)                      │
  │                                                               │
  │       min_θ  E_(x,y)~D  [ max_{‖δ‖_p ≤ ε}  L(θ, x+δ, y) ]   │
  │        └─ 학습       └─ 입력 분포         └─내부: 적대자       │
  │                                                               │
  │  • 외부 min: 모델 파라미터 θ 최적화 (방어자)                    │
  │  • 내부 max: perturbation δ 탐색 (공격자)                       │
  │  • 동시 Nash Equilibrium 수렴 (안정 시)                          │
  └───────────────────────────────────────────────────────────────┘
```

### C. 핵심 방어 메커니즘 비교

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Adversarial Training (AT)** | 모델 파라미터 직접 robust화 | min-max 게임: 내부 PGD로 최강 perturbation 생성 → 외부는 L(θ, x+δ, y) 최소화. ε=8/255 CIFAR-10에서 Clean 87%→83%, Robust 0%→48% 달성 (PGD-AT, ResNet-50). TRADES는 β·L_clean + L_robust 분해로 정확도-강건성 trade-off 명시적 제어 |
| **Randomized Smoothing (RS)** | 확률적 인증 방어 (Certified Defense) | 가우시안 노이즈 σ 추가 후 다수결: ĝ(x) = argmax_c P(f(x+σ·N(0,I))=c). Cohen et al.(NeurIPS'19): certified radius R = σ/2 · (Φ⁻¹(p_A) - Φ⁻¹(p_B)) (CIFAR-10, σ=0.25, R=0.5@76%). **첫 L2 certified defense**, pero-샘플 100회 추론 필요 → latency 50~100× 증가 |
| **Defensive Distillation** | 그래디언트 마스킹으로 공격 난이도 ↑ | Soft label(T=20~40)로 Knowledge Distillation 시 작은 ‖∇L‖ → FGSM/C&W 효과 감소. Papernot et al.(2016). 단, **C&W 공격에는 무력** (gradient masking 한계, Athalye'18) |
| **Input Preprocessing** | perturbation 차감·왜곡 | ① Feature Squeeze(비트 깊이↓, Spatial Smoothing), ② Pixel Deflection, ③ JPEG/JPEG2000 압축, ④ Total Variation Minimization, ⑤ Super-resolution 기반 denoising. **공격 적응성 한계** (Adaptive Attack에 약함) |
| **Detection (MagNet, NIC)** | 적대적 입력 조기 차단 | MagNet: Autoencoder Reconstructor + Noisy Detector. NIC: 입력 다양체 학습 → off-manifold 입력 reject. LID, Activation Clustering 등 통계 기반 지표 활용. FPR 5% 이하에서 TPR 90%+ 달성 (MagNet, MNIST 기준) |
| **Defensive Ensemble & Lipschitz Control** | 결정 경계 평탄화 | ① Deep Ensemble(독립 AT 모델 N개), ② Parseval Networks(각 레이어 Lipschitz 상한 명시), ③ Spectral Normalization. robust accuracy +2~4% 향상 |
| **Model Watermarking & Provenance** | IP 보호·공급망 인증 | DNN Watermarking(backdoor trigger, signature), Hugging Face Model Signing, **Sigstore**(Cosign)로 가중치 해시 서명, MLOps lineage tracking (MLflow, Weights & Biases) |
| **Adversarial Robustness 검증 도구** | 자동 Red Teaming | IBM **ART**(Adversarial Robustness Toolbox, 100+ 공격·50+ 방어), Microsoft **Counterfit**, NVIDIA **Triton + MLPerf Security**, **Foolbox**, **CleverHans**, **TextAttack**(NLP), **PromptBench**(LLM) |

### D. 학습 시 핵심 수식·파라미터

**TRADES 손실함수** (Zhang et al., ICML'19):
```
L_TRADES = L_CE(f_θ(x), y) + β · KL( f_θ
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 408 / 800

← **이전**: [407. OT 보안 산업 제어 시스템 SCADA](/knowledge-base/studynote/12_it_management/05_security_compliance/407_ot_security_ics_scada_protection/)
**다음**: [409. 양자 내성 암호 PQC 전환 계획](/knowledge-base/studynote/12_it_management/05_security_compliance/409_post_quantum_cryptography_pqc_transition/) →

---
