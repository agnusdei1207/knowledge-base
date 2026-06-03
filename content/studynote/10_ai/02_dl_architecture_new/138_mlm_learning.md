+++
title = "138. MLM (Masked Language Model) - BERT의 핵심 사전 학습 기법"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MLM은 <strong>입력 토큰의 15%를 [MASK]로 가리고 양방향 문맥으로 원래 토큰을 예측</strong>하는 BERT의 사전 학습 방식이며, 빈칸 채우기(Cloze Test)와 같은 원리이다.
> 2. **가치**: GPT의 CLM(Causal LM, 왼→오)은 왼쪽 문맥만 보지만, MLM은 **양쪽 문맥을 동시에** [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하여 "bank"가 은행인지 강둑인지 더 정확히 판별한다.
> 3. **판단 포인트**: MLM은 <strong>이해(NLU)에 최적</strong>이지만 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)에는 부적합하며, Generative 작업에는 CLM([GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/))·Prefix LM(T5)이 적합하다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-note">입력: "나는</div><div class="kb-diagram-node">MASK</div><div class="kb-diagram-note">에서</div><div class="kb-diagram-node">MASK</div><div class="kb-diagram-note">를 먹었다"</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">예측:</div><div class="kb-diagram-node">MASK1</div><div class="kb-diagram-note">= "식당",</div><div class="kb-diagram-node">MASK2</div><div class="kb-diagram-note">= "밥"</div></div>
<div class="kb-diagram-note">→ 양방향 문맥(나는, 를, 먹었다)을 모두 참조</div>
<div class="kb-diagram-note">→ 양방향 이해 능력 학습</div>
</div>
</div>



- **📢 섹션 요약 비유**: MLM은 <strong>빈칸 채우기 시험</strong>이다. 양쪽 [힌트](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/)를 보고 빈칸에 들어갈 단어를 맞춘다.

---

## Ⅱ~Ⅴ. 결론

MLM은 <strong>양방향 언어 이해의 핵심 학습 방식</strong>이며, [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)·RoBERTa·DeBERTa의 사전 학습 기반이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **MLM** | 빈칸 채우기 (양방향) |
| **CLM** | 다음 토큰 예측 ([GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)) |
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/">BERT</a></strong> | MLM 기반 모델 |
| **RoBERTa** | [NSP](/knowledge-base/studynote/10_ai/02_dl_architecture_new/139_nsp_next_sentence_prediction/) 제거 + 더 많은 학습 |
| **Denoising** | T5의 변형 MLM |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Word2Vec CBOW (2013)</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">ELMo (2018)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">BERT MLM (2018)</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">RoBERTa (NSP 제거, 2019)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">SpanBERT (Span Masking)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">현재: Replaced Token Detection (ELECTRA)</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. MLM은 <strong>빈칸 채우기 시험</strong>이에요. "나는 ___에서 ___를 먹었다"
2. 앞뒤 단어를 <strong>모두 <a href="/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/">힌트</a>로</strong> 사용해서 빈칸을 맞춰요.
3. 이렇게 공부하면 **문장의 의미를 깊이** 이해할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 138 / 420

← **이전**: [137. BERT (Bidirectional Encoder Representations from Transformers)](/knowledge-base/studynote/10_ai/02_dl_architecture_new/137_bert/)
**다음**: [139. NSP (Next Sentence Prediction) - BERT의 문장 관계 학습](/knowledge-base/studynote/10_ai/02_dl_architecture_new/139_nsp_next_sentence_prediction/) →

---
