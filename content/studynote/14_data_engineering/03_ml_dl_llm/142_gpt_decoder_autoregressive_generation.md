---
title: "142. GPT Decoder - 자기회귀 생성 모델 상세"
date: "2026-04-19"
tags:
  - "studynote-dataengineering"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) Decoder는 <strong><a href="/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/">Transformer</a> Decoder에서 Masked <a href="/studynote/10_ai/02_dl_architecture_new/124_self_attention/">Self-Attention</a>(Causal Mask)을 사용</strong>하여 왼->오 방향으로만 문맥을 참조하며 다음 토큰을 예측(CLM)하는 자기회귀 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 모델이다.
> 2. **가치**: [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)(양방향)는 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 불가이지만, [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)([단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/))는 <strong>토큰을 하나씩 순차 <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a></strong>하여 텍스트·코드·대화를 자연스럽게 만들어낸다. [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시 [Temperature](/studynote/10_ai/05_data_science_ml/386_llm_temperature/)·[Top-k](/studynote/06_ict_convergence/05_data_science/414_llm_decoder_top_k_temperature/)·Top-p로 다양성을 제어한다.
> 3. **판단 포인트**: KV Cache로 이전 토큰의 [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)·Value를 재사용하여 <strong>추론 속도를 O(n^)->O(n)으로 최적화</strong>하며, Speculative Decoding이 추가 가속 기법이다.

---

## Ⅰ. 개요 및 필요성

```text
GPT 생성: "나는" -> "학교에" -> "갔다" (순차)
Causal Mask: 미래 토큰 참조 차단
KV Cache: 이전 K,V 재사용 -> 추론 가속
디코딩 전략: Greedy | Top-k | Top-p (Nucleus)
```

- **📢 섹션 요약 비유**: GPT는 <strong>릴레이 소설</strong>이다. 앞사람이 쓴 내용만 보고 다음 문장을 이어 쓴다.

---

## Ⅱ~Ⅴ. 결론

[GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) Decoder는 <strong>텍스트 <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a>의 핵심 아키텍처</strong>이며, KV Cache와 Speculative Decoding이 추론 최적화의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Causal Mask** | 미래 토큰 차단 |
| **CLM** | 다음 토큰 예측 |
| <strong><a href="/studynote/06_ict_convergence/04_ai_llm/291_kv_cache/">KV Cache</a></strong> | 추론 가속 |
| <strong><a href="/studynote/10_ai/05_data_science_ml/386_llm_temperature/">Temperature</a></strong> | [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 다양성 |
| **Top-p** | [Nucleus Sampling](/studynote/10_ai/05_data_science_ml/387_topk_topp_sampling/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[GPT-1 (2018)] -> [GPT-2 (2019)] -> [GPT-3 (2020)]
    -> [KV Cache 최적화 (2021~)]
    -> [Speculative Decoding (2023)]
    -> [현재: Medusa/Eagle — 다중 토큰 동시 생성]
```

### 👶 어린이를 위한 3줄 비유 설명
1. GPT는 <strong>릴레이 소설</strong>이에요. 앞 내용만 보고 **다음 문장을 써요**.
2. 뒤 내용은 **아직 없으니까** 볼 수 없어요(Causal Mask).
3. KV Cache는 <strong>이미 쓴 부분을 기억</strong>해서 더 빨리 써요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 142 / 258

<- **이전**: [141. BERT Encoder - MLM 양방향 사전 학습 상세](/studynote/14_data_engineering/03_ml_dl_llm/141_bert_encoder_mlm_bidirectional/)
**다음**: [143. Foundation Model & LLM 사전 학습 - 기반 모델의 원리](/studynote/14_data_engineering/03_ml_dl_llm/143_foundation_model_llm_pretraining/) ->

---
