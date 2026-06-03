---
title: 137. BERT (Bidirectional Encoder Representations from Transformers)
date: '2026-04-19'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: BERT는 **Transformer의 Encoder만 사용**하여 양방향(Bidirectional)으로 문맥을 이해하는 사전 학습 언어 모델이며, [[138_mlm_learning|MLM]]([[138_mlm_learning|Masked Language Model]])과 [[139_nsp_next_sentence_prediction|NSP]]([[139_nsp_next_sentence_prediction|Next Sentence Prediction]])로 학습한다.
> 2. **가치**: [[302_gpt_autoregressive|GPT]](→방향)는 왼쪽 문맥만 보지만, BERT는 **양쪽 문맥을 동시에** [[316_reference_pattern_nosql|참조]]하여 "bank"가 은행인지 강둑인지 정확히 판별하며, NLU(자연어 이해) 11개 벤치마크를 동시 갱신(2018)했다.
> 3. **판단 포인트**: BERT는 **이해([[107_classification|Classification]]·[[117_ner|NER]]·QA)에 강하고 [[087_process_state_transition|생성]]에 약하며**, GPT는 [[087_process_state_transition|생성]]에 강하다. 현재는 [[040_encoder|Encoder]]-[[039_decoder|Decoder]](T5)·[[039_decoder|Decoder]]-only([[302_gpt_autoregressive|GPT]])가 주류이나 [[301_bert_mlm|BERT]] 계열은 [[278_instruction_tuning|임베딩]]·검색에 여전히 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
BERT = Transformer Encoder × 12/24 Layer
  MLM: "나는 [MASK] 이다" → "학생" 예측 (양방향)
  NSP: "문장 A 다음에 B가 오는가?" (문장 관계)
  → Fine-tuning: 분류·NER·QA·유사도
```

- **📢 섹션 요약 비유**: GPT는 소설 작가(앞→뒤 [[087_process_state_transition|생성]]), BERT는 편집자(앞뒤 맥락으로 이해·교정)이다.

---

## Ⅱ~Ⅴ. 결론

BERT는 **NLU의 기반 모델**이며, [[278_instruction_tuning|임베딩]](Sentence-[[301_bert_mlm|BERT]])·검색([[276_fine_tuning|RAG]] Retriever)에서 여전히 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[301_bert_mlm|BERT]]** | 양방향 [[040_encoder|Encoder]] |
| **[[138_mlm_learning|MLM]]** | 빈칸 채우기 학습 |
| **[[302_gpt_autoregressive|GPT]]** | [[008_단방향_반이중_전이중|단방향]] [[039_decoder|Decoder]] (대조) |
| **Sentence-[[301_bert_mlm|BERT]]** | 문장 [[278_instruction_tuning|임베딩]] |
| **RoBERTa** | [[301_bert_mlm|BERT]] 개선 ([[139_nsp_next_sentence_prediction|NSP]] 제거) |

### 📈 관련 키워드 및 발전 흐름도

```text
[ELMo (2018)] → [BERT (Google, 2018.10)]
    → [RoBERTa (2019)] → [ALBERT (경량)]
    → [DeBERTa (2020)] → [현재: E5/BGE — 임베딩 특화 BERT]
```

### 👶 어린이를 위한 3줄 비유 설명
1. BERT는 **편집자**예요. 문장의 **앞뒤를 다 보고** 의미를 이해해요.
2. GPT는 **소설 작가**(앞→뒤 [[289_cqrs_db|쓰기]]), BERT는 **교정자**(앞뒤 맥락 파악)예요.
3. "bank"가 **은행인지 강둑인지** 앞뒤 문맥을 보고 정확히 알아내요!
