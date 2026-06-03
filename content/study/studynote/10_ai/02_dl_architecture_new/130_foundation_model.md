+++
weight = 130
title = "130. Foundation Model (파운데이션 모델) - 대규모 사전 학습 범용 AI 모델"
date = "2026-04-19"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Foundation Model은 **대규모 [[001_dikw_pyramid|데이터]]로 사전 학습(Pre-[[588_mlops_pipeline_automation|training]])된 범용 [[190_ai_llm_requirements_specification|AI]] 모델**로, 다양한 하위 작업(NLP·Vision·코드)에 [[304_fine_tuning|Fine-tuning]] 또는 Prompting으로 적응 가능하며, [[302_gpt_autoregressive|GPT]]·[[301_bert_mlm|BERT]]·Stable Diffusion이 대표이다.
> 2. **가치**: 개별 작업마다 처음부터 모델을 학습하면 비용이 막대하지만, Foundation Model을 **기반으로 [[133_fine_tuning|미세 조정]]**하면 소량 [[001_dikw_pyramid|데이터]]로도 높은 [[282_performance_tactics|성능]]을 달성할 수 있다([[132_transfer_learning|Transfer Learning]]).
> 3. **판단 포인트**: 스탠포드 HAI([[477_owasp_top_10_2021|2021]])가 명명했으며, **[[265_emergent_abilities|Emergent Abilities]](창발 능력)**—규모가 커지면 사전에 학습하지 않은 능력이 나타나는 현상—이 핵심 특성이다.

---

## Ⅰ. 개요 및 필요성

```text
Foundation Model = 대규모 데이터 + 대규모 파라미터 + 자기지도 학습
  → 범용 표현 학습 → 다양한 하위 작업에 적응
  예: GPT-4(텍스트), CLIP(이미지+텍스트), Codex(코드)
```

- **📢 섹션 요약 비유**: Foundation Model은 **대학 교양 교육**이다. 교양(사전 학습)을 받은 후 전공([[304_fine_tuning|Fine-tuning]])을 선택하면 빠르게 전문가가 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 특성 | 설명 |
|:---|:---|
| **사전 학습** | 대규모 비라벨 [[001_dikw_pyramid|데이터]] |
| **Transfer** | 하위 작업에 적응 |
| **Emergent** | 규모↑ → 새 능력 출현 |
| **[[158_multimodal_clip_vision_audio_encoding|멀티모달]]** | 텍스트+이미지+오디오 |

---

## Ⅲ~Ⅴ. 결론

Foundation Model은 **현대 AI의 패러다임**이며, 규모의 법칙(Scaling Law)에 의해 계속 발전하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[225_foundation_model_peft_lora|Foundation Model]]** | 범용 사전 학습 모델 |
| **[[265_emergent_abilities|Emergent Abilities]]** | 규모 확대 시 창발 |
| **[[304_fine_tuning|Fine-tuning]]** | 하위 작업 적응 |
| **Scaling Law** | 규모와 [[282_performance_tactics|성능]]의 [[083_relationship_in_er_model|관계]] |
| **[[132_transfer_learning|Transfer Learning]]** | 사전 학습 → 전이 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Word2Vec (2013)] → [BERT (2018)] → [GPT-3 (2020)]
    → [Foundation Model 명명 (Stanford HAI, 2021)]
    → [GPT-4 / Gemini (2023~2024)]
    → [현재: 오픈소스 FM — Llama·Mistral·Qwen]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Foundation Model은 **대학 교양 교육**이에요. 많이 배우면 **뭐든 할 수 있는 기초**가 돼요.
2. 교양(사전 학습) 후 **전공([[304_fine_tuning|Fine-tuning]])**을 선택하면 빠르게 전문가가 돼요.
3. 정말 많이 배우면 **가르치지 않은 것도 알게 되는(창발)** 신기한 현상이 일어나요!
