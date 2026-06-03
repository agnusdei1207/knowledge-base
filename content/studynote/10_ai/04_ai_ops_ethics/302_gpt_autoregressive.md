---
title: 302. GPT (Generative Pre-trained Transformer)
date: '2026-05-09'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GPT (Generative Pre-trained [[246_transformer_self_attention_parallel_positional_encoding|Transformer]])는 [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] [[039_decoder|디코더]] 구조를 사용하여 "다음 토큰 예측"이라는 단일 언어 모델링 [[150_task|태스크]]로 대규모 텍스트를 사전 학습한 뒤, 텍스트를 자기회귀적([[248_bert_encoder_mlm_gpt_decoder_autoregressive_comparison|Autoregressive]])으로 [[087_process_state_transition|생성]]하는 모델 계보다.
> 2. **가치**: 좌→우 [[008_단방향_반이중_전이중|단방향]] 언어 모델링만으로도 사전 학습 규모를 늘릴수록 번역·요약·코드 [[087_process_state_transition|생성]]·추론 등 다양한 [[150_task|태스크]]에서 SOTA를 달성하는 **[[249_scaling_normalization_standardization|스케일링]] 법칙(Scaling Law)**을 실증했으며, ChatGPT·GPT-4로 이어져 [[190_ai_llm_requirements_specification|AI]] 대중화를 이끌었다.
> 3. **판단 포인트**: GPT는 [[172_maas_mobility_as_a_service|마스]]크드 셀프 어텐션(Masked [[124_self_attention|Self-Attention]])으로 미래 토큰을 보지 않는 **인과적(Causal) 언어 모델**이며, BERT처럼 양방향이 아니라 [[008_단방향_반이중_전이중|단방향]] [[087_process_state_transition|생성]]에 특화된 구조임을 BERT와 명확히 구별해야 한다.

---

## Ⅰ. 개요 및 필요성

OpenAI는 2018년 GPT-1을 발표하며 "단순히 다음 단어를 예측하는 언어 모델을 대규모로 학습하면, 별도의 레이블 없이도 다양한 언어 [[150_task|태스크]]를 잘 수행하는 범용 표현을 배울 수 있다"는 가설을 [[395_verification_process_review|검증]]했다.

GPT는 Transformer의 [[039_decoder|디코더]] 부분만 사용하며, 학습 시 입력 시퀀스의 각 위치에서 이전 토큰들만 보고 다음 토큰을 예측한다. 이 인과적(Causal) 학습은 자기회귀 [[087_process_state_transition|생성]]에 자연스럽게 이어진다 — 추론 시에도 앞 토큰을 입력으로 다음 토큰을 한 번에 하나씩 [[087_process_state_transition|생성]]한다.

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: GPT는 소설 작가다. 앞 내용(이전 토큰들)만 보고 다음 문장(다음 토큰)을 이어 쓴다. 미래 내용은 절대 미리 보지 않는다([[172_maas_mobility_as_a_service|마스]]크드 어텐션). BERT는 완성된 소설을 전체 읽고 분석하는 문학 평론가이고, GPT는 빈 원고지를 채워가는 작가다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
┌──────────────────────────────────────────────────────────────────┐
│         GPT 자기회귀 생성 구조 (Autoregressive Generation)          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  입력: "한국의 수도는"                                              │
│   │                                                              │
│  ┌▼──────────────────────────────────────────────────────────┐   │
│  │  Transformer Decoder Block (N회 반복)                      │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │  Masked Multi-Head Self-Attention                   │  │   │
│  │  │  (현재 위치에서 미래 토큰 어텐션 마스킹)                 │  │   │
│  │  │  예: "한국의" 위치에서 "수도는"을 볼 수 없음            │  │   │
│  │  ├─────────────────────────────────────────────────────┤  │   │
│  │  │  Add & Norm → Feed-Forward Network → Add & Norm     │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  └────────────────────────────────────────────────────────────┘   │
│   │                                                              │
│  선형 레이어 + Softmax → 다음 토큰 확률 분포                        │
│   │                                                              │
│  출력 1: "서울" (확률 최고 → 그리디 또는 샘플링으로 선택)             │
│   │                                                              │
│  다시 입력: "한국의 수도는 서울" → 출력 2: "이다" → ...              │
│  (이전 출력을 입력에 추가하며 시퀀스 완성: 자기회귀)                  │
└──────────────────────────────────────────────────────────────────┘
```

| GPT [[288_version_ihl_tos_total_length|버전]] | 파라미터 | 주요 혁신 | 출시 |
|:---|:---|:---|:---|
| GPT-1 | 117M | [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] [[039_decoder|디코더]] + 사전 학습 | 2018 |
| GPT-2 | 1.5B | 스케일업, 제로샷 [[282_performance_tactics|성능]] 입증 | 2019 |
| GPT-3 | 175B | 퓨샷 학습, [[249_scaling_normalization_standardization|스케일링]] 법칙 | 2020 |
| InstructGPT / [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] | 175B | 인간 피드백 [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] | 2022 |
| ChatGPT / GPT-4 | 비공개 | 대화형 [[190_ai_llm_requirements_specification|AI]], [[158_multimodal_clip_vision_audio_encoding|멀티모달]] | 2022~2023 |

- **📢 섹션 요약 비유**: GPT [[288_version_ihl_tos_total_length|버전]] 진화는 음식점 규모 확장과 같다. GPT-1은 동네 작은 분식집(원리 [[395_verification_process_review|검증]]), GPT-2는 중형 레스토랑(메뉴 다양화), GPT-3는 프랜차이즈 대기업(175B 파라미터, 전국 진출), ChatGPT는 대국민 [[090_service_kubernetes_network_load_balancing|서비스]](사람들의 대화 스타일에 맞춤 [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] 훈련). 맛집의 본질(자기회귀 언어 모델)은 같지만 규모와 [[090_service_kubernetes_network_load_balancing|서비스]] 품질이 폭발적으로 성장했다.

---

## Ⅲ. 비교 및 연결

[[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] ([[250_rlhf_human_feedback_reinforcement_alignment_cot|Reinforcement Learning from Human Feedback]], 인간 피드백 [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]])는 InstructGPT/ChatGPT의 핵심 혁신이다:
1. **[[121_supervised_learning|지도 학습]] [[133_fine_tuning|미세 조정]](SFT)**: 인간이 작성한 이상적 답변으로 GPT [[304_fine_tuning|파인 튜닝]]
2. **보상 모델([[197_rm_rate_monotonic_scheduling|RM]]) 학습**: 인간 평가자가 여러 응답에 순위를 매겨 보상 [[130_signal|신호]] [[087_process_state_transition|생성]]
3. **[[395_ppo_clipping|PPO]] [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]**: 보상 모델 점수를 최대화하도록 GPT를 [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]]

이 세 단계 덕분에 단순 텍스트 예측 모델이 "도움이 되고 해롭지 않은 대화 [[190_ai_llm_requirements_specification|AI]]"로 변신했다.

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [[009_config|설정]] | 작은 규모, 개념 학습 |
| GPT (Generative Pre-trained [[246_transformer_self_attention_parallel_positional_encoding|Transformer]]) | [[282_performance_tactics|성능]]과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [[090_service_kubernetes_network_load_balancing|서비스]] 고도화 단계 |

- **📢 섹션 요약 비유**: RLHF는 신입 작가(SFT 학습된 GPT)에게 독자 만족도 조사(인간 평가)를 반복해 피드백을 주는 편집자 과정이다. 독자가 "이 글이 더 나아요"라고 평가하면 그 방향으로 더 쓰도록 훈련한다. 기술적 글쓰기 능력 위에 독자 공감 능력이 더해져 베스트셀러 작가가 탄생한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**추론 [[268_strategy_pattern|전략]] (Decoding [[268_strategy_pattern|Strategy]])**:
- **탐욕 탐색 (Greedy Decoding)**: 매 시점 [[130_probability|확률]] 최고 토큰 선택. 빠르지만 단조로움
- **빔 서치 (Beam Search)**: 상위 K 후보 유지. 번역·요약에 적합
- **샘플링 ([[056_표본화_Sampling|Sampling]]) + [[386_llm_temperature|Temperature]]**: [[130_probability|확률]] 분포에서 샘플링. [[386_llm_temperature|Temperature]] < 1이면 결정론적, > 1이면 다양성 증가
- **[[414_llm_decoder_top_k_temperature|Top-K]] / Top-P(Nucleus) [[056_표본화_Sampling|Sampling]]**: 상위 K개 또는 누적 [[130_probability|확률]] P 이상의 후보에서만 샘플링. 창의적 텍스트 [[087_process_state_transition|생성]]에 표준

**[[033_context|컨텍스트]] 창 ([[033_context|Context]] Window)**: GPT-4는 128K 토큰, Claude는 200K 토큰의 [[033_context|컨텍스트]] 창을 지원하며, 이는 [[300_positional_encoding|포지셔널 인코딩]](RoPE) 기술 발전의 결과다.

- **📢 섹션 요약 비유**: [[386_llm_temperature|Temperature]] [[009_config|설정]]은 작가의 창의성 다이얼이다. [[386_llm_temperature|Temperature]]=0(로봇 작가)은 항상 가장 안전한 단어만 선택해 뻔한 글을 쓰고, [[386_llm_temperature|Temperature]]=1.5(자유분방 작가)는 예상치 못한 단어를 골라 때로는 엉뚱하지만 창의적인 글을 쓴다. 목적에 맞게 다이얼을 조정하는 것이 [[149_prompt_engineering_cot_few_shot|프롬프트 엔지니어링]]의 실전 기술이다.

---

## Ⅴ. 기대효과 및 결론

GPT 계보는 "언어 모델을 충분히 크게 훈련하면 모든 언어 [[150_task|태스크]]에서 우수해진다"는 [[249_scaling_normalization_standardization|스케일링]] 법칙을 현실로 증명했다. ChatGPT는 이 기술을 대중화하여 AI의 역사를 "전문가 전용"에서 "누구나 사용"으로 바꿨다. 코드 [[087_process_state_transition|생성]](GitHub Copilot), 법률 문서 분석, 의학 연구 지원 등 지식 노동의 모든 분야에 GPT가 침투하며 생산성 혁명을 이끌고 있다.

- **📢 섹션 요약 비유**: GPT는 [[190_ai_llm_requirements_specification|AI]] 세계의 인쇄기다. 구텐베르크 인쇄기가 지식을 소수 성직자에서 모든 시민에게 해방시켰듯, GPT는 고급 [[190_ai_llm_requirements_specification|AI]] 능력을 소수 엔지니어에서 모든 사람에게 해방시켰다. 채팅창 하나로 번역·작문·코딩·분석을 모두 수행하는 시대가 열렸다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 자기회귀 ([[248_bert_encoder_mlm_gpt_decoder_autoregressive_comparison|Autoregressive]]) | 이전 토큰 → 다음 토큰 / GPT 추론의 핵심 메커니즘 |
| [[172_maas_mobility_as_a_service|마스]]크드 어텐션 | 미래 토큰 차단, 인과성 / GPT 학습 시 정보 누수 방지 |
| [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] | 인간 피드백, [[395_ppo_clipping|PPO]], 보상 모델 / ChatGPT의 대화 품질 향상 기법 |
| [[249_scaling_normalization_standardization|스케일링]] 법칙 | 파라미터 수, [[001_dikw_pyramid|데이터]], [[282_performance_tactics|성능]] 곡선 / GPT 규모 확대의 이론적 근거 |
| [[301_bert_mlm|BERT]] | 양방향, [[040_encoder|인코더]], 이해 특화 / GPT와 정반대 방향의 사전 학습 모델 |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] → [GPT (Generative Pre-trained Transformer)] → [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. **GPT**는 소설 작가처럼 **앞 내용만 보면서** "다음에는 어떤 단어가 올까?"를 수십억 번 맞추다 보니 **언어를 완벽하게 배운 [[190_ai_llm_requirements_specification|AI]]**예요!
2. "한국의 수도는" 다음에 "서울"을 쓰고, "서울" 다음에 "이다"를 쓰는 식으로 **한 단어씩 이어 [[087_process_state_transition|생성]]**하는 방식이에요.
3. GPT-3, GPT-4, **ChatGPT** 모두 이 원리인데, 크기를 엄청 키웠더니 번역·코딩·요약 등 **거의 모든 걸 잘하는** 만능 AI가 됐어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 302 / 420

← **이전**: [[301_bert_mlm|301. BERT (Bidirectional Encoder Representations from Transformers)]]
**다음**: [[303_foundation_model|303. 파운데이션 모델 (Foundation Model)]] →

---
