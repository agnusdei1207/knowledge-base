---
title: 297. 트랜스포머 (Transformer)
date: '2026-05-09'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] ([[246_transformer_self_attention_parallel_positional_encoding|Transformer]])는 [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]]/LSTM의 순차 처리를 완전히 제거하고, **셀프 어텐션 ([[124_self_attention|Self-Attention]])**으로 시퀀스 내 모든 위치 간의 의존성을 단 한 번의 [[430_index_fast_full_scan|병렬]] 행렬 연산으로 포착하는 2017년 혁명적 신경망 아키텍처다.
> 2. **가치**: 순차 처리 제거로 [[418_gpu|GPU]] [[430_index_fast_full_scan|병렬]]화 효율이 비약적으로 높아져 수조 개의 파라미터를 가진 초거대 언어 모델([[263_llm_large_language_model|LLM]]) 학습이 가능해졌으며, [[301_bert_mlm|BERT]]·[[302_gpt_autoregressive|GPT]]·T5·ChatGPT·Stable Diffusion 등 현대 [[190_ai_llm_requirements_specification|AI]] 혁명의 설계도다.
> 3. **판단 포인트**: "Attention Is All You Need"라는 논문 제목처럼 RNN이 없어도 어텐션만으로 순서 정보([[300_positional_encoding|Positional Encoding]])와 장거리 의존성을 모두 처리할 수 있음을 증명한 것이 핵심 혁신이다.

---

## Ⅰ. 개요 및 필요성

[[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]]/LSTM의 근본적 한계는 **순차 처리(Sequential Processing)**다. "나는 학교에 간다"를 처리할 때 t=1→2→3→4로 순서대로 처리해야 하므로 GPU의 [[430_index_fast_full_scan|병렬]] 코어를 100% 활용할 수 없다. 긴 시퀀스에서 [[088_vanishing_gradient_relu_skip_connection|기울기 소실]]도 여전히 위협이다.

2017년 구글 브레인의 "Attention Is All You Need" 논문은 RNN을 완전히 제거하고, 시퀀스 전체를 한꺼번에 행렬 연산으로 처리하는 Transformer를 제안했다. 셀프 어텐션이 시퀀스 내 모든 위치를 동시에 연결하므로, 위치 1과 위치 1000의 의존성을 거리 1홉(Hop)으로 처리한다.

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: RNN은 책을 한 글자씩 소리 내어 읽는 학생이고, Transformer는 책 전체를 카메라로 한 번에 찍어 사진에서 동시에 모든 [[083_relationship_in_er_model|관계]]를 파악하는 AI다. 한 글자씩 읽는 건 느리고 앞 [[286_page_frame|페이지]]를 잊지만, 사진 한 장은 빠르고 전체를 동시에 기억한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
┌────────────────────────────────────────────────────────────────────┐
│            트랜스포머 (Transformer) 전체 아키텍처                      │
├──────────────────────┬─────────────────────────────────────────────┤
│  인코더 스택           │   디코더 스택                                  │
│  (N=6 레이어 반복)     │   (N=6 레이어 반복)                            │
│                      │                                             │
│  ┌────────────────┐   │   ┌─────────────────────────────────────┐   │
│  │ Add & Norm     │   │   │ Add & Norm                          │   │
│  │                │   │   │                                     │   │
│  │ Feed-Forward   │   │   │ Feed-Forward Network                │   │
│  │ Network        │   │   │                                     │   │
│  ├────────────────┤   │   ├─────────────────────────────────────┤   │
│  │ Add & Norm     │   │   │ Add & Norm                          │   │
│  │                │   │   │                                     │   │
│  │ Multi-Head     │   │   │ Cross-Attention (인코더↔디코더)        │   │
│  │ Self-Attention │   │   │                                     │   │
│  ├────────────────┤   │   ├─────────────────────────────────────┤   │
│  │ Positional     │   │   │ Add & Norm                          │   │
│  │ Encoding +     │   │   │                                     │   │
│  │ Input Embed    │   │   │ Masked Multi-Head Self-Attention     │   │
│  └────────────────┘   │   │ (미래 토큰 마스킹)                      │   │
│                      │   └─────────────────────────────────────┘   │
└──────────────────────┴─────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 설명 |
|:---|:---|:---|
| 셀프 어텐션 ([[124_self_attention|Self-Attention]]) | 시퀀스 내 위치 간 [[083_relationship_in_er_model|관계]] 파악 | 모든 위치 쌍을 동시에 연결 |
| [[299_multi_head_attention|멀티 헤드 어텐션]] (Multi-Head) | 다양한 관점 [[430_index_fast_full_scan|병렬]] 어텐션 | H개 헤드가 독립적으로 어텐션 수행 |
| [[300_positional_encoding|포지셔널 인코딩]] ([[300_positional_encoding|Positional Encoding]]) | 순서 정보 주입 | 삼각함수로 위치를 벡터에 인코딩 |
| 피드포워드 네트워크 (FFN) | 비선형 변환 | 2층 MLP, 각 위치 독립적으로 적용 |
| 잔차 연결 + [[093_normalization|정규화]] (Add & Norm) | 기울기 흐름 안정화 | Skip Connection + Layer Norm |

- **📢 섹션 요약 비유**: Transformer의 [[040_encoder|인코더]] 1층은 마치 교실에서 토론 수업을 하는 것이다. 학생 하나하나(각 토큰)가 교실 전체를 둘러보며 "내 주장과 가장 관련 있는 동급생은 누구지?"를 동시에 파악한다(셀프 어텐션). 6층 반복은 6번의 토론 라운드로 점점 더 깊은 맥락 이해가 쌓이는 것이다.

---

## Ⅲ. 비교 및 연결

| 항목 | [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]]/[[292_lstm|LSTM]] | [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] |
|:---|:---|:---|
| 처리 방식 | 순차 (Sequential) | [[430_index_fast_full_scan|병렬]] (Parallel) |
| 장거리 의존성 | 경로 O(T), [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] 위험 | 경로 O(1), 직접 연결 |
| [[418_gpu|GPU]] 활용도 | 낮음 (순서 의존) | 높음 (전체 동시 처리) |
| 메모리 복잡도 | O(T) | O(T²) |
| 학습 속도 | 느림 | 빠름 |
| 대표 모델 | [[292_lstm|LSTM]], [[294_gru|GRU]] | [[301_bert_mlm|BERT]], [[302_gpt_autoregressive|GPT]], T5, LLaMA |

- **📢 섹션 요약 비유**: RNN이 모든 역을 정차하는 완행열차라면, Transformer는 출발지에서 목적지까지 모든 역을 동시에 연결하는 고속 네트워크다. 완행은 각 역(시점)을 차례로 거쳐야 하지만, 고속망은 서울에서 부산까지 1홉으로 연결한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 기반 모델 계보**:
- **[[040_encoder|인코더]] 전용**: [[301_bert_mlm|BERT]] (양방향 이해, [[104_classification_analysis|분류]]·NER에 강점)
- **[[039_decoder|디코더]] 전용**: [[302_gpt_autoregressive|GPT]] 시리즈 (자기회귀 [[087_process_state_transition|생성]], 텍스트 [[087_process_state_transition|생성]]에 강점)
- **[[040_encoder|인코더]]-[[039_decoder|디코더]]**: T5, BART (번역·요약 등 변환 작업에 강점)
- **비전**: ViT (Vision [[246_transformer_self_attention_parallel_positional_encoding|Transformer]], 이미지 패치를 토큰으로 처리)
- **[[158_multimodal_clip_vision_audio_encoding|멀티모달]]**: [[408_clip|CLIP]], Flamingo (텍스트+이미지 동시 처리)

**확장성 (Scaling Law)**: Transformer는 파라미터 수와 [[001_dikw_pyramid|데이터]] 크기를 늘릴수록 [[282_performance_tactics|성능]]이 예측 가능하게 향상되는 **[[249_scaling_normalization_standardization|스케일링]] 법칙(Scaling Law)**을 따른다. 이 특성이 [[302_gpt_autoregressive|GPT]]-4급 [[263_llm_large_language_model|LLM]] 개발의 이론적 근거다.

- **📢 섹션 요약 비유**: Transformer의 [[249_scaling_normalization_standardization|스케일링]] 법칙은 공장 확장 효과와 같다. 기계(파라미터)를 2배로 늘리고 원료([[001_dikw_pyramid|데이터]])를 2배로 늘리면 생산성([[190_ai_llm_requirements_specification|AI]] [[282_performance_tactics|성능]])이 예측 가능하게 증가한다. 이 예측 가능성이 수천억 원 투자 결정을 가능하게 한다.

---

## Ⅴ. 기대효과 및 결론

Transformer는 [[190_ai_llm_requirements_specification|AI]] 역사에서 가장 파급력 있는 단일 아키텍처 혁신이다. RNN이 지배하던 자연어 처리를 완전히 재편하고, 이미지·오디오·비디오·단백질 구조·코드 등 사실상 모든 [[001_dikw_pyramid|데이터]] 타입에 Transformer가 적용되는 "[[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 시대"를 열었다. [[302_gpt_autoregressive|GPT]]-4, Gemini, Claude, Stable Diffusion 모두 Transformer에서 직접 파생된 결과물이며, 향후 AGI(인공 일반 지능) 논의도 이 구조를 중심으로 전개된다.

- **📢 섹션 요약 비유**: Transformer는 [[190_ai_llm_requirements_specification|AI]] 세계의 인터넷 [[295_protocol_field_tcp_udp_icmp|프로토콜]]([[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP)이다. 인터넷이 발명된 뒤 그 위에 웹·이메일·SNS·유튜브가 올라온 것처럼, [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 위에 [[301_bert_mlm|BERT]]·[[302_gpt_autoregressive|GPT]]·ChatGPT·Stable Diffusion이 차례로 올라와 [[190_ai_llm_requirements_specification|AI]] 문명의 인프라가 됐다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 셀프 어텐션 ([[124_self_attention|Self-Attention]]) | Q/K/V, [[430_index_fast_full_scan|병렬]] / Transformer의 핵심 연산 |
| [[300_positional_encoding|포지셔널 인코딩]] | 삼각함수, 순서 정보 / [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] 없이 순서를 처리하는 방법 |
| [[301_bert_mlm|BERT]] | 양방향, [[138_mlm_learning|MLM]], [[040_encoder|인코더]] 전용 / [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] [[040_encoder|인코더]] 기반 대표 모델 |
| [[302_gpt_autoregressive|GPT]] | 자기회귀, [[039_decoder|디코더]] 전용 / [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] [[039_decoder|디코더]] 기반 대표 모델 |
| [[249_scaling_normalization_standardization|스케일링]] 법칙 | 파라미터, [[001_dikw_pyramid|데이터]], [[282_performance_tactics|성능]] / [[263_llm_large_language_model|LLM]] 확장의 이론적 근거 |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] → [트랜스포머 (Transformer)] → [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. **[[246_transformer_self_attention_parallel_positional_encoding|Transformer]]([[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]])**는 책을 한 글자씩 읽는 대신, **책 전체를 사진으로 찍어서 한 번에 모든 글자의 [[083_relationship_in_er_model|관계]]를 파악**하는 엄청나게 빠른 신경망이에요!
2. 덕분에 [[418_gpu|GPU]](컴퓨터 계산 장치)를 **최대한 동시에** 활용할 수 있어서, 엄청 큰 AI도 빠르게 학습할 수 있어요.
3. **ChatGPT, [[301_bert_mlm|BERT]], Stable Diffusion** 등 요즘 유명한 AI가 모두 이 [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] 구조를 사용하고 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 297 / 420

← **이전**: [[296_attention_mechanism|296. 어텐션 메커니즘 (Attention Mechanism)]]
**다음**: [[298_qkv_attention|298. 쿼리(Q) / 키(K) / 밸류(V)]] →

---
