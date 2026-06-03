---
title: 131. 자기 지도 학습 (Self-Supervised Learning) - 라벨 없이 학습하는 사전 훈련
date: '2026-04-19'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[266_self_supervised_learning|Self-Supervised Learning]](SSL)은 **라벨 없는 [[001_dikw_pyramid|데이터]]에서 [[001_dikw_pyramid|데이터]] 자체로 학습 [[130_signal|신호]]를 [[087_process_state_transition|생성]]**하는 방법이며, "다음 단어 예측([[302_gpt_autoregressive|GPT]])"·"빈칸 채우기([[301_bert_mlm|BERT]])"가 대표적 pretext task이다.
> 2. **가치**: 라벨링은 비용이 높지만 비라벨 [[001_dikw_pyramid|데이터]]는 무한하므로, SSL로 대규모 사전 학습 후 소량 라벨 [[001_dikw_pyramid|데이터]]로 Fine-tuning하면 **라벨 효율이 극대화**된다.
> 3. **판단 포인트**: NLP([[138_mlm_learning|MLM]]·CLM)·Vision(Contrastive·MAE)·[[158_multimodal_clip_vision_audio_encoding|멀티모달]]([[408_clip|CLIP]]) 각 분야의 SSL 방식을 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
지도 학습: 데이터+라벨 필요 (비쌈)
SSL: 데이터만 (무료), 라벨은 데이터 자체에서 생성
  NLP: "나는 [MASK] 이다" → 학생 예측 (BERT)
  Vision: 이미지 일부 가림 → 복원 (MAE)
```

- **📢 섹션 요약 비유**: SSL은 **빈칸 채우기 시험**이다. 선생님(라벨)이 정답을 알려주지 않아도 문장([[001_dikw_pyramid|데이터]]) 자체에서 정답을 유추한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 분야 | SSL 방식 | 대표 |
|:---|:---|:---|
| **NLP** | [[138_mlm_learning|MLM]], CLM | [[301_bert_mlm|BERT]], [[302_gpt_autoregressive|GPT]] |
| **Vision** | Contrastive, MAE | SimCLR, MAE |
| **[[158_multimodal_clip_vision_audio_encoding|멀티모달]]** | 이미지-텍스트 매칭 | **[[408_clip|CLIP]]** |

---

## Ⅲ~Ⅴ. 결론

SSL은 **Foundation Model의 핵심 학습 패러다임**이며, 라벨 없는 대규모 [[001_dikw_pyramid|데이터]]로 범용 표현을 학습하는 것이 현대 AI의 기본이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **SSL** | 라벨 없이 학습 |
| **[[138_mlm_learning|MLM]]** | 빈칸 채우기 ([[301_bert_mlm|BERT]]) |
| **CLM** | 다음 단어 예측 ([[302_gpt_autoregressive|GPT]]) |
| **Contrastive** | 유사/비유사 쌍 학습 |
| **[[408_clip|CLIP]]** | 이미지-텍스트 SSL |

### 📈 관련 키워드 및 발전 흐름도

```text
[지도 학습 (라벨 필수)] → [Word2Vec SSL (2013)]
    → [BERT MLM / GPT CLM (2018)] → [SimCLR (2020, Vision SSL)]
    → [CLIP (2021, 멀티모달)]
    → [현재: DINO v2 / MAE — Vision SSL 표준]
```

### 👶 어린이를 위한 3줄 비유 설명
1. SSL은 **빈칸 채우기 시험**이에요. 선생님이 정답을 안 알려줘도 **문장에서 유추**해요.
2. "나는 ___ 이다"에서 "학생"을 **스스로 맞추는** 거예요.
3. 정답(라벨)이 없어도 **엄청 많은 문제를 풀면** AI가 똑똑해진답니다!
