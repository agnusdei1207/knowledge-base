+++
weight = 126
title = "126. Positional Encoding - Transformer에 순서 정보를 주입하는 기법"
date = "2026-04-19"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Positional Encoding은 **Self-Attention이 순서를 모르는 한계를 보완**하기 위해 각 토큰의 위치 정보를 **sin/cos 함수 또는 학습 벡터**로 [[278_instruction_tuning|임베딩]]에 더하는 기법이다.
> 2. **가치**: "I love you" vs "You love I"는 Self-Attention만으로는 동일하게 처리되지만, Positional Encoding이 **1번 위치·2번 위치·3번 위치를 구분**하여 어순의 의미를 보존한다.
> 3. **판단 포인트**: **Sinusoidal(고정형)**은 학습 불필요·임의 길이 확장 가능, **Learned(학습형)**은 [[001_dikw_pyramid|데이터]] 적응적이나 최대 길이 고정, **RoPE(회전형)**는 상대 위치 인코딩으로 최신 [[263_llm_large_language_model|LLM]](Llama)에서 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Positional Encoding                                │
├───────────────────────────────────────────────────────┤
│  입력 임베딩: [I, love, you]                          │
│  위치 인코딩: [pos=0, pos=1, pos=2]                   │
│                                                       │
│  Sinusoidal:                                          │
│   PE(pos, 2i)   = sin(pos / 10000^(2i/d))            │
│   PE(pos, 2i+1) = cos(pos / 10000^(2i/d))            │
│                                                       │
│  최종 입력 = 단어 임베딩 + 위치 인코딩               │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Positional Encoding은 좌석 번호이다. Self-Attention은 모든 사람을 볼 수 있지만, 좌석 번호가 없으면 "누가 앞줄이고 뒷줄인지" 모른다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### PE 유형 비교

| 유형 | 방식 | 특징 |
|:---|:---|:---|
| **Sinusoidal** | sin/cos (고정) | 학습 불필요, 임의 길이 |
| **Learned** | 학습 벡터 | [[001_dikw_pyramid|데이터]] 적응적, 길이 고정 |
| **RoPE** | 회전 행렬 | **상대 위치**, [[263_llm_large_language_model|LLM]] 표준 |
| **ALiBi** | 거리 기반 편향 | 외삽 가능 |

- **📢 섹션 요약 비유**: Sinusoidal은 수학 공식으로 만든 좌석표, Learned는 연습을 통해 외운 좌석표, RoPE는 "나와 옆 사람의 거리"로 좌석을 파악하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | PE 없음 | PE 있음 |
|:---|:---|:---|
| **어순** | 무시 | **보존** |
| **"I love you" vs "You love I"** | 동일 | **구분** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 최신 LLM에서의 PE
- [[302_gpt_autoregressive|GPT]]-2/3: Learned PE.
- [[302_gpt_autoregressive|GPT]]-4/Llama: **RoPE** (상대 위치, 길이 외삽).
- ALiBi: MPT 등에서 사용.

---

## Ⅴ. 기대효과 및 결론

Positional Encoding은 **Transformer가 순서를 이해하게 하는 유일한 장치**이며, RoPE가 최신 LLM의 사실상 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Sinusoidal PE** | 원본 [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] (고정) |
| **Learned PE** | [[302_gpt_autoregressive|GPT]]-2/[[301_bert_mlm|BERT]] (학습) |
| **RoPE** | 회전 기반 상대 위치 (Llama) |
| **ALiBi** | 거리 편향 (길이 외삽) |
| **[[033_context|Context]] Length** | PE가 결정하는 최대 시퀀스 길이 |

### 📈 관련 키워드 및 발전 흐름도

```text
[RNN 순서 (내재적, ~2016)]
    │
    ▼
[Sinusoidal PE (Transformer, 2017)]
    │
    ▼
[Learned PE (BERT/GPT-2, 2018~2019)]
    │
    ▼
[RoPE (2021) — 상대 위치 인코딩]
    │
    ▼
[현재: YaRN / NTK-RoPE — 긴 컨텍스트 확장]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Positional Encoding은 교실의 **좌석 번호**예요.
2. 좌석 번호가 없으면 "누가 앞줄이고 뒷줄인지" **모르니까** 혼란스러워요.
3. 좌석 번호 덕분에 AI가 **단어의 순서**를 이해할 수 있답니다!
