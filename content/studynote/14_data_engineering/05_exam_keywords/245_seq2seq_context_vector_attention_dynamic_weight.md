+++
title = "245. Seq2Seq (Sequence-to-Sequence) 컨텍스트 벡터 (Context Vector) 어텐션 동적 가중"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Seq2Seq(Sequence-to-Sequence)는 [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)([Encoder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/))가 입력 시퀀스를 고정 길이 [컨텍스트 벡터](/knowledge-base/studynote/10_ai/02_dl_architecture_new/120_context_vector/)([Context Vector](/knowledge-base/studynote/10_ai/02_dl_architecture_new/120_context_vector/))로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하고 [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)([Decoder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/))가 이를 펼쳐 출력 시퀀스를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 아키텍처다.
> 2. **가치**: [어텐션 메커니즘](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/296_attention_mechanism/)([Attention Mechanism](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/296_attention_mechanism/))은 [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)가 출력 토큰마다 [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)의 모든 은닉 상태에 동적 가중합(Dynamic Weighted Sum)을 수행해 정보 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 병목([Bottleneck](/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/))을 극복한다.
> 3. **판단 포인트**: [어텐션 메커니즘](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/296_attention_mechanism/)은 Transformer의 핵심 셀프 어텐션([Self-Attention](/knowledge-base/studynote/10_ai/02_dl_architecture_new/124_self_attention/))으로 진화했으며, Seq2Seq 자체는 기계 번역·요약·챗봇의 기반 아키텍처로 여전히 널리 참조된다.

---

## Ⅰ. 개요 및 필요성

기존 [RNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/) 기반 언어 모델은 단일 문장 또는 고정 길이 시퀀스만 처리할 수 있었다. Seq2Seq는 가변 길이 입력을 가변 길이 출력으로 변환하는 범용 시퀀스 변환 프레임워크를 제공한다.

### Seq2Seq 등장 배경

| 한계 | 설명 | 해결 방법 |
|:---|:---|:---|
| 고정 크기 입력 | 기존 신경망은 고정 길이 벡터 필요 | [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)-[디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) 분리 |
| 가변 길이 출력 | 번역 결과는 입력과 길이 다름 | [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) 자기 회귀 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| 입출력 정렬 불필요 | 언어마다 어순 다름 | [컨텍스트 벡터](/knowledge-base/studynote/10_ai/02_dl_architecture_new/120_context_vector/) [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) |

**핵심 응용 분야**: 기계 번역, [텍스트 요약](/knowledge-base/studynote/16_bigdata/05_analysis/115_text_summarization/), 챗봇, 음성 인식, 코드 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)

📢 **섹션 요약 비유**: Seq2Seq는 통역사와 같다. 한국어 연설을 완전히 이해한 후([인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)), 영어로 다시 말하는([디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)) 과정이다. 단어 하나씩 번역하는 것이 아니라 전체 의미를 이해한 후 재표현한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 기본 Seq2Seq 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">입력: "나는 학교에 간다"</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">인코더 (Encoder)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">LSTM</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">LSTM</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">LSTM</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">는 학교에 간다</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">h_n</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">컨텍스트 벡터 c</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(고정 길이 벡터)</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">디코더 (Decoder)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">LSTM</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">LSTM</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">...</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">"I" "go"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">컨텍스트 c가 초기 상태로 주입</div></div>
<div class="kb-diagram-note">출력: "I go to school"</div>
</div>
</div>



<strong>핵심 문제: 정보 병목(Information <a href="/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/">Bottleneck</a>)</strong>



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">입력 길이가 길수록:</div>
<div class="kb-diagram-note">"나는 어제 학교 도서관에서 친구와 함께 수학 공부를 열심히 했다"</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">단 하나의 벡터로 압축!</div></div>
<div class="kb-diagram-note">30 단어 c ∈ ℝ^{512} ← 손실 발생!</div>
</div>
</div>



### [어텐션 메커니즘](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/296_attention_mechanism/) ([Attention Mechanism](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/296_attention_mechanism/))

Bahdanau et al. 2015 — "Neural Machine Translation by Jointly [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) to Align and Translate"



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">어텐션 가중치 계산 과정</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">인코더 은닉 상태: h_1, h_2, ..., h_T</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">e_{s,t} = score(s_{s-1}, h_t)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">= 정렬 점수 (Alignment Score)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">α_{s,t} = softmax(e_{s,t})</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">= 어텐션 가중치 (합 = 1)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">c_s = Σ_t α_{s,t} · h_t</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">= 동적 컨텍스트 벡터 (매 스텝 갱신)</div></div>
<div class="kb-diagram-note">예시: "I go to school" 생성 시</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">나:0.9, 는:0.05, 학교:0.02, 간다:0.03</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">나:0.1, 는:0.05, 학교:0.05, 간다:0.8</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">나:0.05, 는:0.1, 학교:0.8, 간다:0.05</div></div>
</div>
</div>



### Bahdanau vs Luong 어텐션

| 구분 | Bahdanau 어텐션 | Luong 어텐션 |
|:---|:---|:---|
| 정렬 함수 | additive (덧셈) | multiplicative (내적) |
| score 계산 | v^T · [tanh](/knowledge-base/studynote/10_ai/01_ai_basics/070_hyperbolic_tangent_tanh_activation/)(W₁h + W₂s) | h^T · W · s |
| 입력 상태 | h_{t-1} (이전 상태) | h_t ([현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)) |
| 연산 비용 | 높음 | 낮음 |
| 특징 | 부드러운 정렬 | 빠른 연산 |

📢 **섹션 요약 비유**: 어텐션은 통역사가 번역 중 중요한 부분을 다시 확인하는 것이다. "I"를 말할 때는 "나"를, "school"을 말할 때는 "학교에"를 다시 보듯, 매 순간 가장 관련 있는 부분에 집중한다.

---

## Ⅲ. 비교 및 연결

### Seq2Seq 아키텍처 진화



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">2014: Vanilla Seq2Seq</div>
<div class="kb-diagram-note">단일 컨텍스트 벡터 → 정보 병목</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">2015: Seq2Seq + Bahdanau Attention</div>
<div class="kb-diagram-note">동적 컨텍스트 벡터 → 병목 해결, 정렬 시각화 가능</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">2017: Transformer (Attention Is All You Need)</div>
<div class="kb-diagram-note">셀프 어텐션으로 RNN 완전 대체 → 병렬화, 장거리 의존성 해결</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">2018~: BERT, GPT 등 사전 학습 모델</div>
<div class="kb-diagram-note">대규모 코퍼스 사전 학습 + 다운스트림 파인튜닝</div>
</div>
</div>



### 어텐션 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) — 정렬 행렬(Alignment Matrix)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">출력</div><div class="kb-diagram-cell">나</div><div class="kb-diagram-cell">는</div><div class="kb-diagram-cell">학교에</div><div class="kb-diagram-cell">간다</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">I</div><div class="kb-diagram-cell">██</div><div class="kb-diagram-cell">▒</div><div class="kb-diagram-cell">▒</div><div class="kb-diagram-cell">▒</div><div class="kb-diagram-cell">← "나"에 집중</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">go</div><div class="kb-diagram-cell">▒</div><div class="kb-diagram-cell">▒</div><div class="kb-diagram-cell">▒</div><div class="kb-diagram-cell">██</div><div class="kb-diagram-cell">← "간다"에 집중</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">to</div><div class="kb-diagram-cell">▒</div><div class="kb-diagram-cell">▒</div><div class="kb-diagram-cell">██</div><div class="kb-diagram-cell">▒</div><div class="kb-diagram-cell">← "학교에"에 집중</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">school</div><div class="kb-diagram-cell">▒</div><div class="kb-diagram-cell">▒</div><div class="kb-diagram-cell">██</div><div class="kb-diagram-cell">▒</div><div class="kb-diagram-cell">← "학교에"에 집중</div></div>
<div class="kb-diagram-note">██ = 높은 어텐션 가중치</div>
<div class="kb-diagram-note">→ 번역 시 어느 단어를 참조했는지 해석 가능 (설명 가능 AI)</div>
</div>
</div>



| 특성 | Seq2Seq (w/o Attention) | Seq2Seq + Attention |
|:---|:---|:---|
| [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) | 고정 벡터 c | 매 스텝 동적 c_s |
| 장문 처리 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 급락 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 유지 |
| 해석 가능성 | 낮음 | 어텐션 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) |
| 파라미터 추가 | 없음 | 소수 (정렬 함수) |

📢 **섹션 요약 비유**: 어텐션이 없는 Seq2Seq는 책 전체를 읽고 요약을 기억해 번역하는 것이다. 어텐션이 있는 Seq2Seq는 번역 중 필요할 때마다 원문의 해당 부분을 다시 보는 것이다. 훨씬 정확하고 긴 문장도 처리할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기계 번역 시스템 구현 예시



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">훈련 파이프라인</div>
<div class="kb-diagram-note">병렬 코퍼스 수집</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">토큰화 + BPE (Byte Pair Encoding) 어휘 구축</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">인코더-디코더 LSTM 학습</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Teacher Forcing (훈련) / Beam Search (추론)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">BLEU Score 평가</div>
<div class="kb-diagram-note">Beam Search (빔 탐색):</div>
<div class="kb-diagram-tree-item" style="--depth:1">매 스텝 상위 k개 후보 유지</div>
<div class="kb-diagram-tree-item" style="--depth:1">탐욕적 디코딩(Greedy) 대비 번역 품질 향상</div>
<div class="kb-diagram-tree-item" style="--depth:1">k=4~10이 일반적</div>
</div>
</div>



### 산업 적용 사례

| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 아키텍처 | 특이점 |
|:---|:---|:---|
| Google Translate | [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 기반 | Seq2Seq에서 전환 |
| Siri/Alexa | Seq2Seq + 대화 관리 | 다중 턴 문맥 유지 |
| GitHub Copilot | [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 기반 자동 회귀 | Seq2Seq 원리 응용 |
| 문서 요약 | T5 / BART | [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)-[디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) 사전 학습 |

📢 **섹션 요약 비유**: Seq2Seq와 어텐션은 현대 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 번역기의 심장이다. "의미를 이해하고 재표현한다"는 철학이 Google Translate부터 ChatGPT까지 이어지는 핵심 원리다.

---

## Ⅴ. 기대효과 및 결론

### Seq2Seq가 열어준 가능성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Seq2Seq 프레임워크의 적용 영역</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">입력 시퀀스 → 출력 시퀀스</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">한국어 문장 → 영어 번역</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">긴 문서 → 요약문</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">사용자 질문 → 챗봇 응답</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">음성 파형 → 텍스트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">소스 코드 → 설명문</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">SQL 자연어 → 쿼리문</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">단백질 서열 → 구조 예측</div></div>
</div>
</div>



### 기술사 시험 핵심 포인트

1. <strong><a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/120_context_vector/">컨텍스트 벡터</a> 병목</strong>: 고정 길이 벡터의 정보 손실 문제
2. <strong>어텐션 <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">가중치</a> 계산</strong>: `α = softmax(score(s, h))` → `c = Σα·h`
3. **Bahdanau vs Luong**: additive vs multiplicative 비교
4. **Teacher Forcing**: 훈련 효율화 기법 (정답 토큰 강제 입력)
5. **Beam Search**: 추론 품질 향상 기법

📢 **섹션 요약 비유**: Seq2Seq와 어텐션의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 독서실과 개방형 스터디룸의 차이다. 독서실([컨텍스트 벡터](/knowledge-base/studynote/10_ai/02_dl_architecture_new/120_context_vector/))에서는 공부를 마친 후 노트 하나만 들고 나오지만, 개방형 스터디룸(어텐션)에서는 필요할 때마다 원하는 책을 펼쳐볼 수 있다.

---

### 📌 관련 개념 맵
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 기반 구조 | Seq2Seq | [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)-[디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) 시퀀스 변환 |
| 핵심 문제 | 정보 병목 (Information [Bottleneck](/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/)) | 고정 [컨텍스트 벡터](/knowledge-base/studynote/10_ai/02_dl_architecture_new/120_context_vector/) 한계 |
| 핵심 해결 | [어텐션 메커니즘](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/296_attention_mechanism/) (Attention) | 동적 가중합으로 병목 극복 |
| 어텐션 유형 | Bahdanau Attention | 덧셈 기반 정렬 함수 |
| 어텐션 유형 | Luong Attention | 내적 기반 정렬 함수 |
| 발전 방향 | [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) | 셀프 어텐션 + 병렬화 |
| 추론 기법 | Beam Search | 상위 k 후보 유지 탐색 |
| 훈련 기법 | Teacher Forcing | 정답 토큰 강제 입력 |

### 👶 어린이를 위한 3줄 비유 설명
1. Seq2Seq는 한국어로 된 편지를 읽고 완전히 이해한 다음, 영어로 새로 써주는 친절한 번역 도우미야.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">RNN Encoder-Decoder (고정 길이 Context Vector 병목)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Attention: 매 출력 단어마다 입력 전체를 참조 (동적 가중치)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Self-Attention → Transformer (병렬 처리 가능)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">BERT · GPT · T5 (Foundation Models)</div>
</div>
</div>


2. [컨텍스트 벡터](/knowledge-base/studynote/10_ai/02_dl_architecture_new/120_context_vector/) 없는 어텐션은 책을 다 읽고 메모지 하나에만 적어 두는 것, 어텐션이 있으면 번역할 때 원본 책을 다시 펼쳐볼 수 있어.
3. 어텐션 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)는 번역가가 "이 영어 단어를 쓸 때 한국어의 어느 부분을 보고 있었는지" 색깔로 보여주는 지도야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 245 / 258

← **이전**: [244. RNN (Recurrent Neural Network) 시계열 LSTM 셀 게이트 장기 의존성 극복](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/)
**다음**: [246. 트랜스포머 (Transformer) 셀프 어텐션 병렬 처리 포지셔널 인코딩](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) →

---
