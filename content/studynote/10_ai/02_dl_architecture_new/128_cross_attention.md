---
title: 128. Cross-Attention - 인코더→디코더 참조 메커니즘
date: '2026-04-19'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Cross-Attention은 **Query는 [[039_decoder|디코더]]에서, [[067_db_key_uniqueness_minimality|Key]]·Value는 [[040_encoder|인코더]]에서 오는 Attention**이며, [[039_decoder|디코더]]가 [[040_encoder|인코더]]의 출력을 [[316_reference_pattern_nosql|참조]]하여 **소스→타겟 매핑(번역·요약)을 수행**한다.
> 2. **가치**: [[040_encoder|인코더]]만으로는 소스 문장을 이해하지만 타겟을 [[087_process_state_transition|생성]]하지 못하고, [[039_decoder|디코더]]만으로는 소스를 [[316_reference_pattern_nosql|참조]]하지 못하므로, Cross-Attention이 **[[040_encoder|인코더]]의 정보를 [[039_decoder|디코더]]로 전달하는 유일한 경로**이다.
> 3. **판단 포인트**: [[124_self_attention|Self-Attention]](Q=K=V 같은 시퀀스) vs Cross-Attention(Q≠K,V 다른 시퀀스)을 구분하고, [[040_encoder|인코더]]-[[039_decoder|디코더]] 모델(T5·BART)에서만 사용되며, [[302_gpt_autoregressive|GPT]]([[039_decoder|디코더]] 전용)에는 없다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Cross-Attention 동작                               │
├───────────────────────────────────────────────────────┤
│  [인코더] "나는 학생이다" → 인코더 출력 (K, V)       │
│                                                       │
│  [디코더] "I am a" → 디코더 상태 (Q)                 │
│                                                       │
│  Cross-Attention:                                     │
│   Q("a"의 상태) × K(인코더 출력)^T → Attention Score │
│   → V(인코더 출력) 가중합 → "student" 예측           │
│                                                       │
│  핵심: Q는 디코더, K·V는 인코더에서 옴               │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Cross-Attention은 **통역사**이다. 화자([[040_encoder|인코더]])의 말을 듣고(K,V), 청자([[039_decoder|디코더]])가 이해하는 언어(Q)로 번역한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Self vs Cross

| 비교 | [[124_self_attention|Self-Attention]] | Cross-Attention |
|:---|:---|:---|
| **Q** | 같은 시퀀스 | **[[039_decoder|디코더]]** |
| **K, V** | 같은 시퀀스 | **[[040_encoder|인코더]]** |
| **용도** | 내부 [[083_relationship_in_er_model|관계]] | **소스→타겟 매핑** |
| **모델** | [[301_bert_mlm|BERT]], [[302_gpt_autoregressive|GPT]] | **T5, BART** |

- **📢 섹션 요약 비유**: Self는 자기 자신을 비추는 거울, Cross는 다른 사람을 비추는 쌍안경이다.

---

## Ⅲ. 비교 및 연결

| 모델 | Self | Masked Self | Cross |
|:---|:---|:---|:---|
| **[[301_bert_mlm|BERT]]** | ✅ | ❌ | ❌ |
| **[[302_gpt_autoregressive|GPT]]** | ❌ | ✅ | ❌ |
| **T5** | ✅ | ✅ | **✅** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Cross-Attention 적용
- 기계 번역 (T5, mBART).
- 이미지 캡셔닝 (이미지 [[040_encoder|인코더]] → 텍스트 [[039_decoder|디코더]]).
- Stable Diffusion (텍스트 → 이미지 [[087_process_state_transition|생성]]에서 텍스트를 K,V로).

---

## Ⅴ. 기대효과 및 결론

Cross-Attention은 **서로 다른 모달리티·언어 간 정보를 전달하는 핵심 메커니즘**이며, [[158_multimodal_clip_vision_audio_encoding|멀티모달]] AI의 기반이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Cross-Attention** | Q([[039_decoder|디코더]])↔K,V([[040_encoder|인코더]]) |
| **[[124_self_attention|Self-Attention]]** | 같은 시퀀스 내 [[316_reference_pattern_nosql|참조]] |
| **[[040_encoder|인코더]]-[[039_decoder|디코더]]** | Cross-Attention이 필요한 구조 |
| **Stable Diffusion** | 텍스트 Cross-Attention으로 이미지 [[087_process_state_transition|생성]] |
| **T5** | [[040_encoder|인코더]]-[[039_decoder|디코더]] 대표 모델 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Attention (Bahdanau, 2014) — 최초 Cross-Attention]
    │
    ▼
[Transformer (2017) — Self + Cross + Masked]
    │
    ▼
[T5 / BART (2019~2020) — 인코더-디코더 사전 학습]
    │
    ▼
[Stable Diffusion (2022) — Cross-Attention으로 이미지 제어]
    │
    ▼
[현재: 멀티모달 Cross-Attention — 이미지·텍스트·오디오 융합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Cross-Attention은 **통역사**예요. 한국어([[040_encoder|인코더]])를 듣고 영어([[039_decoder|디코더]])로 번역해요.
2. 통역사가 없으면 한국어만 아는 사람과 영어만 아는 사람이 **대화를 못 해요**.
3. Stable Diffusion도 "고양이 그려줘"라는 **글([[040_encoder|인코더]])을 그림([[039_decoder|디코더]])으로 통역**한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 128 / 420

← **이전**: [[127_masked_self_attention|127. Masked Self-Attention - 자기 회귀 디코더의 미래 토큰 차단]]
**다음**: [[129_position_wise_feed_forward_ffnn|129. Position-wise FFN - Transformer 내 2층 MLP 비선형 변환]] →

---
