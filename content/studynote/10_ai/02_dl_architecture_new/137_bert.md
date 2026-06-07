---
title: "BERT (Bidirectional Encoder Representations from Transformers)"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 137
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: BERT는 <strong>Transformer의 Encoder만 사용</strong>하여 양방향(Bidirectional)으로 문맥을 이해하는 사전 학습 언어 모델이며, [MLM](/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/)([Masked Language Model](/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/))과 [NSP](/studynote/10_ai/02_dl_architecture_new/139_nsp_next_sentence_prediction/)([Next Sentence Prediction](/studynote/10_ai/02_dl_architecture_new/139_nsp_next_sentence_prediction/))로 학습한다.
> 2. **가치**: [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)(->방향)는 왼쪽 문맥만 보지만, BERT는 **양쪽 문맥을 동시에** [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하여 "bank"가 은행인지 강둑인지 정확히 판별하며, NLU(자연어 이해) 11개 벤치마크를 동시 갱신(2018)했다.
> 3. **판단 포인트**: BERT는 <strong>이해(<a href="/studynote/12_it_management/03_ea_isp/107_classification/">Classification</a>·<a href="/studynote/16_bigdata/05_analysis/117_ner/">NER</a>·QA)에 강하고 <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a>에 약하며</strong>, GPT는 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)에 강하다. 현재는 [Encoder](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)-[Decoder](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)(T5)·[Decoder](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)-only([GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/))가 주류이나 [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) 계열은 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)·검색에 여전히 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
BERT = Transformer Encoder × 12/24 Layer
  MLM: "나는 [MASK] 이다" -> "학생" 예측 (양방향)
  NSP: "문장 A 다음에 B가 오는가?" (문장 관계)
  -> Fine-tuning: 분류·NER·QA·유사도
```

- **📢 섹션 요약 비유**: GPT는 소설 작가(앞->뒤 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)), BERT는 편집자(앞뒤 맥락으로 이해·교정)이다.

---

## Ⅱ~Ⅴ. 결론

BERT는 <strong>NLU의 기반 모델</strong>이며, [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)(Sentence-[BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/))·검색([RAG](/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/) Retriever)에서 여전히 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/">BERT</a></strong> | 양방향 [Encoder](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/) |
| <strong><a href="/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/">MLM</a></strong> | 빈칸 채우기 학습 |
| <strong><a href="/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/">GPT</a></strong> | [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) [Decoder](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) (대조) |
| <strong>Sentence-<a href="/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/">BERT</a></strong> | 문장 [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) |
| **RoBERTa** | [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) 개선 ([NSP](/studynote/10_ai/02_dl_architecture_new/139_nsp_next_sentence_prediction/) 제거) |

### 📈 관련 키워드 및 발전 흐름도

```text
[ELMo (2018)] -> [BERT (Google, 2018.10)]
    -> [RoBERTa (2019)] -> [ALBERT (경량)]
    -> [DeBERTa (2020)] -> [현재: E5/BGE — 임베딩 특화 BERT]
```

### 👶 어린이를 위한 3줄 비유 설명
1. BERT는 <strong>편집자</strong>예요. 문장의 **앞뒤를 다 보고** 의미를 이해해요.
2. GPT는 **소설 작가**(앞->뒤 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)), BERT는 **교정자**(앞뒤 맥락 파악)예요.
3. "bank"가 **은행인지 강둑인지** 앞뒤 문맥을 보고 정확히 알아내요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 137 / 420

<- **이전**: [136. Prompt Tuning - 소프트 프롬프트로 LLM 적응](/studynote/10_ai/02_dl_architecture_new/136_prompt_tuning/)
**다음**: [138. MLM (Masked Language Model) - BERT의 핵심 사전 학습 기법](/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/) ->

---
