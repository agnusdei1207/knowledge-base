+++
title = "91. Apache Pulsar — Kafka 대안, 컴퓨팅/스토리지 분리, 멀티 테넌시"
description = "Transformer의 Self-Attention 메커니즘, BERT의 사전 학습 및 파인튜닝, 자연어 처리에서의 혁신"
date = 2026-04-05

[taxonomies]
tags = ["it_management"]

[extra]
tags = ["it_management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Transformer는 기존 RNN의 순차 처리 한계를 극복하기 위해, 입력된 시퀀스 내의 모든 단어 위치 간 의존성을 동시에 계산하는 셀프 어텐션([Self-Attention](/knowledge-base/studynote/10_ai/02_dl_architecture_new/124_self_attention/)) 메커니즘만으로 구성된 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 인공신경망 아키텍처다.
> 2. **가치**: 이 아키텍처의 [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)([Encoder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/))만을 분리해 대규모 텍스트로 양방향 문맥을 학습시킨 모델이 BERT이며, 특정 도메인의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 조금 추가하는 파인튜닝([Fine-tuning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/))만으로 다양한 자연어 처리 문제에서 압도적 성능을 낸다.
> 3. **판단 포인트**: 시계열이나 순서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 맥락을 완벽히 이해해야 할 때 [RNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/) 대신 [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 계열을 채택하되, 텍스트의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)나 문맥 파악이 목적이면 [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)([인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/))를, 텍스트 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)이 목적이면 [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)([디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/))를 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

Transformer는 2017년 구글이 "Attention Is All You Need" 논문에서 발표한 딥러닝 아키텍처로, 자연어 처리(NLP) 분야의 패러다임을 바꾼 핵심 기술이다. 

과거 언어 번역이나 문장 분석에는 단어를 순서대로 하나씩 읽어 들이는 [RNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/)([Recurrent Neural Network](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/))이 표준으로 사용되었다. 그러나 RNN은 치명적인 단점이 있었다. 순서대로 읽다 보니 문장이 길어지면 앞에 읽었던 단어의 의미를 잊어버리는 [장기 의존성](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/291_long_term_dependency/)([Long-term Dependency](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/291_long_term_dependency/)) 문제가 발생했고, 이전 단어 처리가 끝나야 다음 단어를 처리할 수 있어 GPU를 활용한 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 연산이 불가능했다. Transformer는 단어의 순서에 얽매이지 않고 문장 전체를 한 번에 입력받아, 모든 단어가 서로 어떤 연관이 있는지를 셀프 [어텐션 메커니즘](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/296_attention_mechanism/)을 통해 동시에 계산해냄으로써 이 두 가지 문제를 완벽하게 해결했다.

- **📢 섹션 요약 비유**: 과거의 RNN이 한 줄로 서서 앞사람이 뒷사람에게 귓속말로 문장을 전달하다가 내용이 왜곡되는 '전화 게임'이라면, Transformer는 단체 채팅방에 모든 사람이 동시에 들어와 누가 어떤 맥락으로 말했는지 실시간으로 파악하는 효율적인 화상 회의와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 모델은 입력을 분석하는 [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)([Encoder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/))와 결과를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)([Decoder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/))로 나뉜다. 이 아키텍처의 핵심 심장부는 <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/299_multi_head_attention/">멀티 헤드 어텐션</a> (<a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/299_multi_head_attention/">Multi-Head Attention</a>)</strong>이다.

| 구성 요소 | 역할 | 핵심 특징 |
| :--- | :--- | :--- |
| <strong>셀프 어텐션 (<a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/124_self_attention/">Self-Attention</a>)</strong> | 문장 내 단어 간의 연관성([가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)) 계산 | Query, [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/), Value 벡터의 내적으로 중요도 점수 산출 |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/299_multi_head_attention/">멀티 헤드 어텐션</a></strong> | 어텐션을 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 여러 개 수행 | 문법적 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/), 의미적 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 등 다양한 관점의 문맥 포착 |
| <strong>위치 인코딩 (<a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/300_positional_encoding/">Positional Encoding</a>)</strong> | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 입력으로 잃어버린 단어의 순서 정보 주입 | 사인/코사인 함수를 사용해 위치마다 고유한 값 부여 |

```text
┌──────────────────────────────────────────────────────────────┐
│             Self-Attention의 Q, K, V 계산 흐름             │
├──────────────────────────────────────────────────────────────┤
│ "The", "cat", "sat" (모든 단어 동시 입력)                  │
│        │                                                   │
│        ▼ (선형 변환)                                       │
│    [ Query(Q) ] : "나는 어떤 정보가 필요한가?"             │
│    [ Key(K) ]   : "나는 이런 정보를 가지고 있다"           │
│    [ Value(V) ] : "나의 실제 의미 값은 이것이다"           │
│        │                                                   │
│        ▼                                                   │
│  Attention Score = Softmax( (Q × K^T) / √d ) × V          │
│        │                                                   │
│        ▼                                                   │
│   "cat"과 "sat"의 연관성이 높음을 수학적으로 도출          │
└──────────────────────────────────────────────────────────────┘
```

[BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)(Bidirectional [Encoder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/) Representations from Transformers)는 이 [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 구조 중에서 [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)를 버리고 <strong><a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/">인코더</a>만</strong>을 차용한 모델이다. BERT의 가장 큰 원리는 문장의 일부 단어를 빈칸([MASK])으로 뚫어놓고, 주변의 양방향 문맥을 모두 고려해 빈칸을 맞추도록 대규모 사전 학습(Pre-training)을 수행한다는 점이다.

- **📢 섹션 요약 비유**: 셀프 어텐션은 소개팅 자리와 같다. Query(내 이상형)와 [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)(상대방 프로필)를 대조해 매칭 점수(Attention Score)를 내고, 점수가 높은 사람의 Value(실제 성격)에 가장 큰 비중을 두고 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 맺는 수학적 연관도 측정법이다.

---

## Ⅲ. 비교 및 연결

자연어 처리의 양대 산맥인 BERT와 GPT는 모두 Transformer에서 파생되었으나, 채택한 아키텍처 부품과 목적이 극명하게 다르다.

| 항목 | [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) | [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) |
| :--- | :--- | :--- |
| **차용 아키텍처** | Transformer의 <strong><a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/">인코더</a>(<a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/">Encoder</a>)</strong> | Transformer의 <strong><a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/">디코더</a>(<a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/">Decoder</a>)</strong> |
| <strong>문맥 <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a> 방향</strong> | **양방향 (Bidirectional)** | <strong><a href="/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/">단방향</a> (Unidirectional, 좌→우)</strong> |
| **학습 방식** | 문장 중간의 빈칸([MASK]) 단어 예측 | 주어진 단어들 다음으로 올 단어 예측 |
| **강점 분야** | 텍스트 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/), [감성 분석](/knowledge-base/studynote/12_it_management/03_ea_isp/105_exploratory_data_analysis/), [기계 독해](/knowledge-base/studynote/10_ai/03_llm_nlp/208_mrc_machine_reading_comprehension/)(QA) | 텍스트 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 대화형 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), 요약 |

BERT는 문장의 처음과 끝을 동시에 파악하므로 문맥의 의미를 깊게 이해하는 데 탁월하다. 반면 GPT는 오직 이전 단어들만 보고 다음 단어를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)해야 하므로 작문 능력에 특화되어 있다. 이들 모두 방대한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 '사전 학습(Pre-training)'을 마친 뒤, 특정 목적에 맞게 지식을 미세 조정하는 '파인튜닝([Fine-tuning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/))'이라는 공통된 패러다임을 공유한다.

- **📢 섹션 요약 비유**: BERT는 지문 전체를 앞뒤로 꼼꼼히 읽고 빈칸 추론 문제의 정답을 찾아내는 깐깐한 '독해 수험생'이고, GPT는 앞 단어의 흐름만 보고 뒤이어 나올 단어들을 술술 지어내는 창의적인 '소설가'다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 현장에서 NLP 프로젝트를 시작할 때 무작정 모델을 처음부터 학습시키는 것은 시간과 비용의 낭비다. [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 기반 모델을 활용한 [전이 학습](/knowledge-base/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/)([Transfer Learning](/knowledge-base/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/)) 전략이 필수적이다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. <strong>문제의 성격이 <a href="/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a>인가, <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a>인가?</strong> 고객의 리뷰가 긍정인지 부정인지 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하는 문제라면 [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)(또는 RoBERTa, ALBERT) 계열을, 챗봇처럼 자연스러운 답변을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)해야 한다면 [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 계열을 선택한다.
2. **사전 학습된 모델이 도메인에 맞는가?** 의료, 법률 등 특수 도메인일 경우 일반 텍스트로 학습된 기본 BERT보다는 BioBERT, LegalBERT 등 특화된 코퍼스로 사전 학습된 모델을 베이스로 가져와 파인튜닝해야 한다.
3. <strong><a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/">GPU</a> 메모리와 연산 한계가 존재하는가?</strong> Transformer는 시퀀스 길이의 제곱(O(N²))에 비례하여 메모리를 소모한다. 모바일이나 엣지 디바이스 환경이라면 파라미터를 경량화한 DistilBERT나 TinyBERT 채택을 검토한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 수만 건에 불과한 소규모 자체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋만으로 [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 모델을 바닥부터(From Scratch) 학습시키려는 설계. (반드시 거대 코퍼스로 사전 학습된 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 불러와야 한다.)
- 긴 문서(예: 1만 단어 이상의 보고서)를 전처리 없이 BERT에 한 번에 밀어 넣는 행위. (입력 토큰 길이 제한(보통 512)에 걸려 에러가 발생한다.)

- **📢 섹션 요약 비유**: 일반인([초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 모델)에게 의학 지식을 가르치는 것보다, 이미 수능 만점을 받은 엘리트 의대생(사전 학습된 [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/))을 데려와 우리 병원의 차트 작성법(파인튜닝)만 3일간 가르쳐 현장에 투입하는 것이 훨씬 빠르고 정확한 실무 전략이다.

---

## Ⅴ. 기대효과 및 결론

Transformer와 BERT의 등장은 자연어 처리 역사상 가장 거대한 도약이다. [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리를 통한 방대한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 학습 능력을 바탕으로, 인공지능이 문맥의 뉘앙스를 인간 수준으로 이해하게 되었다. 

그러나 시퀀스 길이에 따른 폭발적인 연산 비용과 거대 언어 모델([LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/))이 요구하는 천문학적인 컴퓨팅 자원([GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))은 뚜렷한 한계점이다. 앞으로는 Longformer, Linformer처럼 연산 복잡도를 줄이는 연구와, 언어를 넘어 이미지, 음성까지 하나의 Transformer로 통합 처리하는 [멀티모달](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/)([Multimodal](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/)) 기술로 확장이 가속화될 것이다. 결론적으로 Transformer는 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 순서를 무시하고 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)의 본질에 직접 집중한 혁명적 아키텍처"로 기억해야 한다.

- **📢 섹션 요약 비유**: 고가의 최고급 만능 조리기([Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)/[BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/))를 들여오면 세상 모든 요리를 최고급 레스토랑 수준으로 만들 수 있지만, 그만큼 주방([GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리)이 엄청나게 넓어야 하고 전기세(연산 비용)를 감당해야 하는 트레이드오프가 남는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/">RNN</a> / <a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/292_lstm/">LSTM</a></strong> | [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 이전에 시계열 및 자연어 처리를 담당하던 순차 처리 기반 모델 |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/296_attention_mechanism/">어텐션 메커니즘</a> (Attention)</strong> | [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)의 특정 단어에 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 두어 [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)에 전달하던 기존 기법을, Transformer가 Self-Attention으로 승화시킴 |
| <strong>사전 학습 (Pre-training) &amp; 파인튜닝 (<a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/">Fine-tuning</a>)</strong> | 거대 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 언어의 보편적 규칙을 배운 뒤, 소량의 정답 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 특정 태스크에 맞추는 학습 패러다임 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/">LLM</a> (<a href="/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/">Large Language Model</a>)</strong> | [Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 아키텍처를 기반으로 파라미터 수를 수천억 개로 확장한 거대 언어 모델 |

### 📈 관련 키워드 및 발전 흐름도

```text
RNN / LSTM (순차 처리, 장기 의존성 한계)
    │
    ▼
Attention Mechanism 도입 (Seq2Seq 성능 개선)
    │
    ▼
Transformer (RNN 제거, 100% 병렬 Self-Attention)
    │
    ├──────────────┬──────────────┐
    ▼              ▼              ▼
  인코더 활용    디코더 활용  인코더-디코더 모두 활용
 (BERT 계열)    (GPT 계열)      (T5, BART 계열)
    │              │
 문맥 이해 최적화 텍스트 생성 최적화
    │              │
    ▼              ▼
 다양한 도메인 파인튜닝 및 초거대 LLM(GPT-4 등) 진화
```

### 👶 어린이를 위한 3줄 비유 설명

1. 옛날 AI는 책을 읽을 때 글자를 손가락으로 짚어가며 하나하나 순서대로 읽어서 시간이 오래 걸렸어요.
2. [트랜스포머](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)([Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/))는 책의 한 페이지를 카메라로 찰칵 찍어서 전체 단어들이 서로 무슨 뜻으로 연결되었는지 한 번에 알아채는 똑똑한 방법이에요.
3. 그중에서도 버트([BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/))는 문장에 뚫린 빈칸을 기가 막히게 잘 맞추는 훈련을 받아서, 글의 진짜 의미를 가장 잘 이해하는 반장 같은 모델이랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 165 / 587

← **이전**: [90. CI (Configuration Item)](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)
**다음**: [91. CMDB (Configuration Management Database)](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/) →

---
