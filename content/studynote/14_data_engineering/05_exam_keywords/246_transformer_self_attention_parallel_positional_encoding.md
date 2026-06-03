+++
title = "246. 트랜스포머 (Transformer) 셀프 어텐션 병렬 처리 포지셔널 인코딩"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Transformer는 RNN을 완전히 제거하고 셀프 어텐션([Self-Attention](/knowledge-base/studynote/10_ai/02_dl_architecture_new/124_self_attention/))만으로 시퀀스 내 모든 위치 간의 의존성을 O(1)의 경로 길이로 포착하는, 현대 딥러닝의 핵심 아키텍처다.
> 2. **가치**: Q(Query)·K([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))·V(Value) 행렬 연산을 통한 스케일드 닷-프로덕트 어텐션([Scaled Dot-Product Attention](/knowledge-base/studynote/10_ai/05_data_science_ml/381_scaled_dot_product_attention/))과 멀티헤드(Multi-Head) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 어텐션이 다양한 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 동시에 포착한다.
> 3. **판단 포인트**: [포지셔널 인코딩](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/300_positional_encoding/)([Positional Encoding](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/300_positional_encoding/))은 순서 정보가 없는 어텐션에 위치 정보를 삽입하는 핵심 설계 결정이며, 사인·코사인 함수 기반 절대 인코딩과 RoPE 같은 상대적 방법이 있다.

---

## Ⅰ. 개요 및 필요성

2017년 구글의 논문 "Attention Is All You Need"(Vaswani et al.)는 [RNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/)/LSTM의 두 가지 근본적 한계를 어텐션만으로 해결했다.

| RNN의 한계 | Transformer의 해결 |
|:---|:---|
| 순차 처리 → [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 불가 | 모든 토큰 동시 처리 ([병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화) |
| 거리 비례 정보 감쇠 | 임의 거리 토큰도 직접 어텐션 |
| [기울기 소실](/knowledge-base/studynote/10_ai/01_ai_basics/088_vanishing_gradient_relu_skip_connection/) | 직접 연결로 기울기 안정 |
| O(n) 훈련 시간 | O(n²) 어텐션이지만 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) |

📢 **섹션 요약 비유**: Transformer는 독서 토론 방식의 혁신이다. 기존 RNN은 책을 처음부터 끝까지 순서대로 읽어야 했다면, Transformer는 모든 참가자가 책 전체를 동시에 펼쳐 놓고 서로 관련된 부분끼리 바로바로 대화한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 스케일드 닷-프로덕트 어텐션 ([Scaled Dot-Product Attention](/knowledge-base/studynote/10_ai/05_data_science_ml/381_scaled_dot_product_attention/))

```
입력 시퀀스 X (n × d_model)
      ↓ 선형 변환 (W_Q, W_K, W_V)
Q = X·W_Q  (n × d_k)   ← 쿼리: "나는 무엇과 관련 있는가?"
K = X·W_K  (n × d_k)   ← 키:   "내가 제공하는 정보의 라벨"
V = X·W_V  (n × d_v)   ← 값:   "실제 전달할 정보 내용"

Attention(Q, K, V) = softmax(Q·K^T / √d_k) · V

         ↑ 스케일링: 차원이 클수록 내적 값이 커져 softmax 포화 방지
```

```
어텐션 행렬 시각화 (4토큰 예시)

        나   는  학교에  간다
나    [0.8  0.1   0.05   0.05]
는    [0.3  0.5   0.1    0.1 ]
학교에[0.05 0.1   0.7    0.15]
간다  [0.1  0.05  0.2    0.65]

→ 각 토큰이 다른 모든 토큰과의 관련성 가중치
```

### 멀티헤드 어텐션 ([Multi-Head Attention](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/299_multi_head_attention/))

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) · W_O

head_i = Attention(Q·W_Q_i, K·W_K_i, V·W_V_i)

h개 헤드가 병렬로 서로 다른 관계 포착:
  head_1: 문법적 관계 (주어-동사)
  head_2: 지시어 해소 (그것 → 고양이)
  head_3: 의미적 유사성
  ...
  head_h: 위치적 관계
```

```
Transformer 인코더 블록 구조
┌─────────────────────────────────────────────┐
│  입력 임베딩 + 포지셔널 인코딩               │
│                  ↓                           │
│  ┌───────────────────────────────────────┐   │
│  │   Multi-Head Self-Attention           │   │
│  │   (쿼리·키·값 모두 같은 입력에서)     │   │
│  └────────────────┬──────────────────────┘   │
│                   │ + 잔차 연결 (Add)         │
│             Layer Normalization              │
│                   ↓                           │
│  ┌───────────────────────────────────────┐   │
│  │   Feed-Forward Network (FFN)          │   │
│  │   FFN(x) = max(0, xW₁+b₁)W₂+b₂      │   │
│  └────────────────┬──────────────────────┘   │
│                   │ + 잔차 연결 (Add)         │
│             Layer Normalization              │
│                   ↓                           │
│            다음 인코더 블록 or 출력           │
└─────────────────────────────────────────────┘
```

### [포지셔널 인코딩](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/300_positional_encoding/) ([Positional Encoding](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/300_positional_encoding/))

어텐션은 순서를 모른다 → 위치 정보를 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)에 더한다.

```
PE(pos, 2i)   = sin(pos / 10000^{2i/d_model})
PE(pos, 2i+1) = cos(pos / 10000^{2i/d_model})

X_input = Token_Embedding + Positional_Encoding

위치 0   ───→ [특정 sin/cos 패턴]
위치 1   ───→ [다른 sin/cos 패턴]
...
위치 512 ───→ [고유한 sin/cos 패턴]

→ 각 위치는 고유한 벡터를 가짐
→ 상대 위치 계산 가능 (내적 시 상대 거리 반영)
```

| 방법 | 특징 | 사용 모델 |
|:---|:---|:---|
| 절대 위치 인코딩 (sin/cos) | 고정, 훈련 불필요 | 원 Transformer |
| 학습 가능 위치 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) | 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 의존 | [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) |
| RoPE (Rotary Position [Embedding](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)) | 상대적 위치, 긴 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) | LLaMA, [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-NeoX |
| ALiBi | 어텐션 편향으로 위치 표현 | BLOOM, MPT |

📢 **섹션 요약 비유**: [포지셔널 인코딩](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/300_positional_encoding/)은 단체 사진의 번호표다. 모든 사람이 동시에 서 있으면 누가 몇 번째인지 알 수 없으니, 각자에게 고유한 번호표를 달아준다.

---

## Ⅲ. 비교 및 연결

### [인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)-[디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) 전체 아키텍처

```
인코더 (6 블록)                  디코더 (6 블록)
┌────────────────┐              ┌─────────────────────────┐
│  Nx 인코더 블록│              │  Nx 디코더 블록          │
│                │              │                          │
│  Self-Attention│              │  Masked Self-Attention   │
│  → FFN         │→ 메모리 K,V →│  → Cross-Attention (K,V) │
│                │              │  → FFN                   │
└────────────────┘              └─────────────────────────┘
     ↑ 입력 시퀀스                     ↑↓ 출력 시퀀스 (자동회귀)

Cross-Attention: 인코더 K,V + 디코더 Q → 번역 시 원문 참조
Masked Attention: 미래 토큰 차단 (자동회귀 생성 보장)
```

### [RNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/) vs Transformer 비교

| 특성 | [RNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/244_rnn_time_series_lstm_cell_gate_long_term_dependency/) / [LSTM](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/292_lstm/) | Transformer |
|:---|:---|:---|
| [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 | ❌ 순차 처리 | ✅ 완전 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) |
| 최대 경로 길이 | O(n) | O(1) |
| 메모리 복잡도 | O(n) | O(n²) |
| 장거리 의존성 | 약함 | 강함 |
| 훈련 속도 | 느림 | 빠름 ([병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)) |
| 추론 속도 | 빠름 | 느림 (n² 어텐션) |

📢 **섹션 요약 비유**: RNN이 전화 릴레이라면, Transformer는 화상 회의다. 릴레이는 순서대로 전달해 오래 걸리고 처음 정보가 왜곡되지만, 화상 회의는 모두가 동시에 직접 소통한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 어텐션 계산 복잡도와 긴 시퀀스 문제

```
표준 어텐션: O(n² · d)  ← n = 시퀀스 길이, d = 차원

n=512:   262K 연산    (일반 텍스트)
n=4096:  16.7M 연산   (장문 문서)
n=32768: 1G 연산      (책 한 권 → 메모리 부족!)

해결 방법:
  Flash Attention (2022): IO 최적화 → 메모리 O(n)
  Sparse Attention:       핵심 위치만 어텐션
  Sliding Window:         지역 어텐션 + 전역 일부
  Linear Attention:       커널 근사 → O(n)
```

### 모델 크기와 하이퍼파라미터

| 모델 변형 | 레이어 (N) | 헤드 (h) | d_model | 파라미터 |
|:---|:---|:---|:---|:---|
| Transformer (Base) | 6 | 8 | 512 | 65M |
| Transformer (Large) | 6 | 16 | 1024 | 213M |
| [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)-Base | 12 | 12 | 768 | 110M |
| [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-3 | 96 | 96 | 12288 | 175B |
| [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-4 (추정) | - | - | - | ~1.8T |

📢 **섹션 요약 비유**: Transformer 크기를 늘리는 것은 회의실에 사람을 더 넣는 것과 같다. 사람이 많을수록(파라미터 증가) 더 많은 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 파악하지만, 비용(메모리·연산)도 기하급수적으로 늘어난다.

---

## Ⅴ. 기대효과 및 결론

### Transformer가 가능하게 한 것들

```
Transformer (2017)
      ├── NLP: BERT (2018), GPT (2018~), T5 (2019)
      ├── Vision: ViT (2020), DINO, MAE
      ├── Multi-modal: CLIP, DALL-E, Flamingo
      ├── Biology: AlphaFold2 (단백질 구조)
      └── Code: Codex, GitHub Copilot

→ 딥러닝 모든 분야의 기반 아키텍처
```

### 기술사 시험 핵심 포인트

1. **Q·K·V 어텐션 수식**: `softmax(QK^T / √d_k) · V`
2. <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a>(√d_k) 이유</strong>: 내적 값 증가로 [softmax](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/) 포화 방지
3. **멀티헤드 어텐션**: 다양한 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 동시 포착
4. <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/300_positional_encoding/">포지셔널 인코딩</a></strong>: 사인·코사인 함수로 위치 정보 삽입
5. <strong><a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/">인코더</a> vs <a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/">디코더</a></strong>: 셀프 어텐션 vs 마스크드+크로스 어텐션

📢 **섹션 요약 비유**: Transformer는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 세계의 인터넷과 같다. 인터넷이 모든 정보를 연결하듯, Transformer는 시퀀스 내 모든 위치를 직접 연결한다. 이 연결성이 언어, 이미지, 단백질, 코드 등 모든 분야를 혁신하는 기반이 되었다.

---

### 📌 관련 개념 맵
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 연산 | 셀프 어텐션 ([Self-Attention](/knowledge-base/studynote/10_ai/02_dl_architecture_new/124_self_attention/)) | 시퀀스 내 모든 위치 간 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 포착 |
| 어텐션 구성 | Q·K·V 행렬 | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)·키·값으로 어텐션 계산 |
| [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 방법 | 멀티헤드 어텐션 | 다양한 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 동시 학습 |
| 위치 정보 | [포지셔널 인코딩](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/300_positional_encoding/) | 순서 없는 어텐션에 위치 삽입 |
| 안정화 기법 | 잔차 연결 + LayerNorm | 심층 훈련 안정화 |
| 전진 레이어 | 피드포워드 (FFN) | 비선형 변환 추가 |
| 파생 모델 | [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/), T5 | Transformer 기반 사전 학습 |
| 최적화 | Flash Attention | 메모리 효율적 어텐션 구현 |

### 👶 어린이를 위한 3줄 비유 설명
1. 셀프 어텐션은 문장 속 단어들이 "나는 너와 얼마나 관련 있어?"라고 서로에게 물어보고, 중요한 친구에게 더 집중하는 것이야.

### 📈 관련 키워드 및 발전 흐름도

```text
RNN (순차 처리, 병렬화 불가)
    │
    ▼
Transformer: Self-Attention + Positional Encoding
    ├─► Multi-Head Attention: 여러 관점에서 동시 분석
    └─► Feed-Forward + Layer Norm + Residual
    │
    ▼
Encoder (BERT) / Decoder (GPT) / Enc-Dec (T5)
```
2. 멀티헤드 어텐션은 같은 문장을 여러 명의 전문가(문법 선생님, 의미 분석가, 번역가)가 동시에 읽고 각자의 관점을 합치는 것이야.
3. [포지셔널 인코딩](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/300_positional_encoding/)은 순서를 모르는 어텐션에게 "이 단어는 세 번째야"라고 번호를 붙여주는 이름표야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 246 / 258

← **이전**: [245. Seq2Seq (Sequence-to-Sequence) 컨텍스트 벡터 (Context Vector) 어텐션 동적 가중](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/245_seq2seq_context_vector_attention_dynamic_weight/)
**다음**: [247. 파운데이션 모델 (Foundation Model) LLM 파라미터 창발성 (Emergence) 자기 지도 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/247_foundation_model_llm_parameter_emergence_self_supervised/) →

---
