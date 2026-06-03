+++
title = "302. GPT (Generative Pre-trained Transformer)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GPT (Generative Pre-trained [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/))는 [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) 구조를 사용하여 "다음 토큰 예측"이라는 단일 언어 모델링 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)로 대규모 텍스트를 사전 학습한 뒤, 텍스트를 자기회귀적([Autoregressive](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/248_bert_encoder_mlm_gpt_decoder_autoregressive_comparison/))으로 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 모델 계보다.
> 2. **가치**: 좌→우 [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 언어 모델링만으로도 사전 학습 규모를 늘릴수록 번역·요약·코드 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·추론 등 다양한 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)에서 SOTA를 달성하는 <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a> 법칙(Scaling Law)</strong>을 실증했으며, ChatGPT·GPT-4로 이어져 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 대중화를 이끌었다.
> 3. **판단 포인트**: GPT는 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)크드 셀프 어텐션(Masked [Self-Attention](/knowledge-base/studynote/10_ai/02_dl_architecture_new/124_self_attention/))으로 미래 토큰을 보지 않는 <strong>인과적(Causal) 언어 모델</strong>이며, BERT처럼 양방향이 아니라 [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)에 특화된 구조임을 BERT와 명확히 구별해야 한다.

---

## Ⅰ. 개요 및 필요성

OpenAI는 2018년 GPT-1을 발표하며 "단순히 다음 단어를 예측하는 언어 모델을 대규모로 학습하면, 별도의 레이블 없이도 다양한 언어 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)를 잘 수행하는 범용 표현을 배울 수 있다"는 가설을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)했다.

GPT는 Transformer의 [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) 부분만 사용하며, 학습 시 입력 시퀀스의 각 위치에서 이전 토큰들만 보고 다음 토큰을 예측한다. 이 인과적(Causal) 학습은 자기회귀 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)에 자연스럽게 이어진다 — 추론 시에도 앞 토큰을 입력으로 다음 토큰을 한 번에 하나씩 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Background Problem → Need → Adoption Value</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Existing limitation</div><div class="kb-diagram-cell">Operational pressure</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">New requirement</div><div class="kb-diagram-cell">Design decision point</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: GPT는 소설 작가다. 앞 내용(이전 토큰들)만 보고 다음 문장(다음 토큰)을 이어 쓴다. 미래 내용은 절대 미리 보지 않는다([마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)크드 어텐션). BERT는 완성된 소설을 전체 읽고 분석하는 문학 평론가이고, GPT는 빈 원고지를 채워가는 작가다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">GPT 자기회귀 생성 구조 (Autoregressive Generation)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">입력: "한국의 수도는"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Transformer Decoder Block (N회 반복)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Masked Multi-Head Self-Attention</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(현재 위치에서 미래 토큰 어텐션 마스킹)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">예: "한국의" 위치에서 "수도는"을 볼 수 없음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Add &amp; Norm → Feed-Forward Network → Add &amp; Norm</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">선형 레이어 + Softmax → 다음 토큰 확률 분포</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">출력 1: "서울" (확률 최고 → 그리디 또는 샘플링으로 선택)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">다시 입력: "한국의 수도는 서울" → 출력 2: "이다" → ...</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(이전 출력을 입력에 추가하며 시퀀스 완성: 자기회귀)</div></div>
</div>
</div>



| GPT [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) | 파라미터 | 주요 혁신 | 출시 |
|:---|:---|:---|:---|
| GPT-1 | 117M | [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) + 사전 학습 | 2018 |
| GPT-2 | 1.5B | 스케일업, 제로샷 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 입증 | 2019 |
| GPT-3 | 175B | 퓨샷 학습, [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) 법칙 | 2020 |
| InstructGPT / [RLHF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/) | 175B | 인간 피드백 [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/) | 2022 |
| ChatGPT / GPT-4 | 비공개 | 대화형 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), [멀티모달](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/) | 2022~2023 |

- **📢 섹션 요약 비유**: GPT [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 진화는 음식점 규모 확장과 같다. GPT-1은 동네 작은 분식집(원리 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)), GPT-2는 중형 레스토랑(메뉴 다양화), GPT-3는 프랜차이즈 대기업(175B 파라미터, 전국 진출), ChatGPT는 대국민 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(사람들의 대화 스타일에 맞춤 [RLHF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/) 훈련). 맛집의 본질(자기회귀 언어 모델)은 같지만 규모와 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질이 폭발적으로 성장했다.

---

## Ⅲ. 비교 및 연결

[RLHF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/) ([Reinforcement Learning from Human Feedback](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/), 인간 피드백 [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/))는 InstructGPT/ChatGPT의 핵심 혁신이다:
1. <strong><a href="/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/">지도 학습</a> <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/133_fine_tuning/">미세 조정</a>(SFT)</strong>: 인간이 작성한 이상적 답변으로 GPT [파인 튜닝](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)
2. <strong>보상 모델(<a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/197_rm_rate_monotonic_scheduling/">RM</a>) 학습</strong>: 인간 평가자가 여러 응답에 순위를 매겨 보상 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)
3. <strong><a href="/knowledge-base/studynote/10_ai/05_data_science_ml/395_ppo_clipping/">PPO</a> <a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/">강화 학습</a></strong>: 보상 모델 점수를 최대화하도록 GPT를 [강화 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/253_reinforcement_learning_mdp_policy_value_q_learning_dqn/)

이 세 단계 덕분에 단순 텍스트 예측 모델이 "도움이 되고 해롭지 않은 대화 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)"로 변신했다.

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 작은 규모, 개념 학습 |
| GPT (Generative Pre-trained [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)) | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 고도화 단계 |

- **📢 섹션 요약 비유**: RLHF는 신입 작가(SFT 학습된 GPT)에게 독자 만족도 조사(인간 평가)를 반복해 피드백을 주는 편집자 과정이다. 독자가 "이 글이 더 나아요"라고 평가하면 그 방향으로 더 쓰도록 훈련한다. 기술적 글쓰기 능력 위에 독자 공감 능력이 더해져 베스트셀러 작가가 탄생한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong>추론 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> (Decoding <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">Strategy</a>)</strong>:
- **탐욕 탐색 (Greedy Decoding)**: 매 시점 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 최고 토큰 선택. 빠르지만 단조로움
- **빔 서치 (Beam Search)**: 상위 K 후보 유지. 번역·요약에 적합
- <strong>샘플링 (<a href="/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/">Sampling</a>) + <a href="/knowledge-base/studynote/10_ai/05_data_science_ml/386_llm_temperature/">Temperature</a></strong>: [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 분포에서 샘플링. [Temperature](/knowledge-base/studynote/10_ai/05_data_science_ml/386_llm_temperature/) < 1이면 결정론적, > 1이면 다양성 증가
- <strong><a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/414_llm_decoder_top_k_temperature/">Top-K</a> / Top-P(Nucleus) <a href="/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/">Sampling</a></strong>: 상위 K개 또는 누적 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) P 이상의 후보에서만 샘플링. 창의적 텍스트 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)에 표준

<strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/">컨텍스트</a> 창 (<a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/">Context</a> Window)</strong>: GPT-4는 128K 토큰, Claude는 200K 토큰의 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 창을 지원하며, 이는 [포지셔널 인코딩](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/300_positional_encoding/)(RoPE) 기술 발전의 결과다.

- **📢 섹션 요약 비유**: [Temperature](/knowledge-base/studynote/10_ai/05_data_science_ml/386_llm_temperature/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)은 작가의 창의성 다이얼이다. [Temperature](/knowledge-base/studynote/10_ai/05_data_science_ml/386_llm_temperature/)=0(로봇 작가)은 항상 가장 안전한 단어만 선택해 뻔한 글을 쓰고, [Temperature](/knowledge-base/studynote/10_ai/05_data_science_ml/386_llm_temperature/)=1.5(자유분방 작가)는 예상치 못한 단어를 골라 때로는 엉뚱하지만 창의적인 글을 쓴다. 목적에 맞게 다이얼을 조정하는 것이 [프롬프트 엔지니어링](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/149_prompt_engineering_cot_few_shot/)의 실전 기술이다.

---

## Ⅴ. 기대효과 및 결론

GPT 계보는 "언어 모델을 충분히 크게 훈련하면 모든 언어 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)에서 우수해진다"는 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) 법칙을 현실로 증명했다. ChatGPT는 이 기술을 대중화하여 AI의 역사를 "전문가 전용"에서 "누구나 사용"으로 바꿨다. 코드 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)(GitHub Copilot), 법률 문서 분석, 의학 연구 지원 등 지식 노동의 모든 분야에 GPT가 침투하며 생산성 혁명을 이끌고 있다.

- **📢 섹션 요약 비유**: GPT는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 세계의 인쇄기다. 구텐베르크 인쇄기가 지식을 소수 성직자에서 모든 시민에게 해방시켰듯, GPT는 고급 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 능력을 소수 엔지니어에서 모든 사람에게 해방시켰다. 채팅창 하나로 번역·작문·코딩·분석을 모두 수행하는 시대가 열렸다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 자기회귀 ([Autoregressive](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/248_bert_encoder_mlm_gpt_decoder_autoregressive_comparison/)) | 이전 토큰 → 다음 토큰 / GPT 추론의 핵심 메커니즘 |
| [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)크드 어텐션 | 미래 토큰 차단, 인과성 / GPT 학습 시 정보 누수 방지 |
| [RLHF](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/) | 인간 피드백, [PPO](/knowledge-base/studynote/10_ai/05_data_science_ml/395_ppo_clipping/), 보상 모델 / ChatGPT의 대화 품질 향상 기법 |
| [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) 법칙 | 파라미터 수, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 곡선 / GPT 규모 확대의 이론적 근거 |
| [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) | 양방향, [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/), 이해 특화 / GPT와 정반대 방향의 사전 학습 모델 |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] → [GPT (Generative Pre-trained Transformer)] → [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. <strong>GPT</strong>는 소설 작가처럼 **앞 내용만 보면서** "다음에는 어떤 단어가 올까?"를 수십억 번 맞추다 보니 <strong>언어를 완벽하게 배운 <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a></strong>예요!
2. "한국의 수도는" 다음에 "서울"을 쓰고, "서울" 다음에 "이다"를 쓰는 식으로 <strong>한 단어씩 이어 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a></strong>하는 방식이에요.
3. GPT-3, GPT-4, **ChatGPT** 모두 이 원리인데, 크기를 엄청 키웠더니 번역·코딩·요약 등 **거의 모든 걸 잘하는** 만능 AI가 됐어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 302 / 420

← **이전**: [301. BERT (Bidirectional Encoder Representations from Transformers)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)
**다음**: [303. 파운데이션 모델 (Foundation Model)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/303_foundation_model/) →

---
