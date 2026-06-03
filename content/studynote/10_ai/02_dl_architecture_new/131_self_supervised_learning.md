+++
title = "131. 자기 지도 학습 (Self-Supervised Learning) - 라벨 없이 학습하는 사전 훈련"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [Self-Supervised Learning](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/)(SSL)은 <strong>라벨 없는 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>에서 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 자체로 학습 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/">신호</a>를 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a></strong>하는 방법이며, "다음 단어 예측([GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/))"·"빈칸 채우기([BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/))"가 대표적 pretext task이다.
> 2. **가치**: 라벨링은 비용이 높지만 비라벨 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 무한하므로, SSL로 대규모 사전 학습 후 소량 라벨 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 Fine-tuning하면 <strong>라벨 효율이 극대화</strong>된다.
> 3. **판단 포인트**: NLP([MLM](/knowledge-base/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/)·CLM)·Vision(Contrastive·MAE)·[멀티모달](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/)([CLIP](/knowledge-base/studynote/10_ai/05_data_science_ml/408_clip/)) 각 분야의 SSL 방식을 이해해야 한다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">지도 학습: 데이터+라벨 필요 (비쌈)</div>
<div class="kb-diagram-note">SSL: 데이터만 (무료), 라벨은 데이터 자체에서 생성</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">NLP: "나는</div><div class="kb-diagram-node">MASK</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">학생 예측 (BERT)</div></div>
<div class="kb-diagram-note">Vision: 이미지 일부 가림 → 복원 (MAE)</div>
</div>
</div>



- **📢 섹션 요약 비유**: SSL은 <strong>빈칸 채우기 시험</strong>이다. 선생님(라벨)이 정답을 알려주지 않아도 문장([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 자체에서 정답을 유추한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 분야 | SSL 방식 | 대표 |
|:---|:---|:---|
| **NLP** | [MLM](/knowledge-base/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/), CLM | [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/), [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) |
| **Vision** | Contrastive, MAE | SimCLR, MAE |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/">멀티모달</a></strong> | 이미지-텍스트 매칭 | <strong><a href="/knowledge-base/studynote/10_ai/05_data_science_ml/408_clip/">CLIP</a></strong> |

---

## Ⅲ~Ⅴ. 결론

SSL은 <strong>Foundation Model의 핵심 학습 패러다임</strong>이며, 라벨 없는 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 범용 표현을 학습하는 것이 현대 AI의 기본이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **SSL** | 라벨 없이 학습 |
| <strong><a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/138_mlm_learning/">MLM</a></strong> | 빈칸 채우기 ([BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/)) |
| **CLM** | 다음 단어 예측 ([GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)) |
| **Contrastive** | 유사/비유사 쌍 학습 |
| <strong><a href="/knowledge-base/studynote/10_ai/05_data_science_ml/408_clip/">CLIP</a></strong> | 이미지-텍스트 SSL |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">지도 학습 (라벨 필수)</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Word2Vec SSL (2013)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">BERT MLM / GPT CLM (2018)</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">SimCLR (2020, Vision SSL)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">CLIP (2021, 멀티모달)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">현재: DINO v2 / MAE — Vision SSL 표준</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. SSL은 <strong>빈칸 채우기 시험</strong>이에요. 선생님이 정답을 안 알려줘도 <strong>문장에서 유추</strong>해요.
2. "나는 ___ 이다"에서 "학생"을 **스스로 맞추는** 거예요.
3. 정답(라벨)이 없어도 **엄청 많은 문제를 풀면** AI가 똑똑해진답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 131 / 420

← **이전**: [130. Foundation Model (파운데이션 모델) - 대규모 사전 학습 범용 AI 모델](/knowledge-base/studynote/10_ai/02_dl_architecture_new/130_foundation_model/)
**다음**: [132. Transfer Learning (전이 학습) - 사전 학습 모델의 재활용](/knowledge-base/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/) →

---
