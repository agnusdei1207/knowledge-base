---
title: 143. Foundation Model & LLM 사전 학습 - 기반 모델의 원리
date: '2026-04-19'
tags:
- studynote-dataengineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Foundation Model은 **대규모 비라벨 [[001_dikw_pyramid|데이터]]로 사전 학습(Pre-training)된 범용 모델**이며, Fine-tuning이나 Prompt로 다양한 다운스트림 작업에 적응한다. [[302_gpt_autoregressive|GPT]]·[[301_bert_mlm|BERT]]·LLaMA·Stable Diffusion이 대표이다.
> 2. **가치**: 각 작업마다 별도 모델을 학습하는 **"하나의 작업=하나의 모델"** 패러다임을 **"하나의 모델=모든 작업"**으로 전환하여, [[001_dikw_pyramid|데이터]]·컴퓨팅 효율을 극대화했다.
> 3. **판단 포인트**: 사전 학습 비용(수백만 달러)은 한 번만 지불하고, 이후 [[304_fine_tuning|Fine-tuning]]·Prompt 비용은 극히 적어 **규모의 경제**가 핵심 가치이다.

---

## Ⅰ. 개요 및 필요성

```text
Foundation Model:
  대규모 데이터(수조 토큰) → 사전 학습 (GPU 수천 장, 수개월)
  → 범용 능력 획득
  → Fine-tuning / Prompt → 다양한 작업 적응
  예: GPT-4, LLaMA, BERT, Stable Diffusion
```

- **📢 섹션 요약 비유**: Foundation Model은 **대학 교육**이다. 전공(작업)에 관계없이 **기초 교양(사전 학습)**을 쌓으면 어떤 전공이든 빠르게 적응한다.

---

## Ⅱ~Ⅴ. 결론

Foundation Model은 **"하나의 모델=모든 작업"** 패러다임의 핵심이며, 규모의 경제로 [[190_ai_llm_requirements_specification|AI]] 민주화를 실현한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[225_foundation_model_peft_lora|Foundation Model]]** | 범용 사전 학습 |
| **Pre-training** | 대규모 비라벨 학습 |
| **[[304_fine_tuning|Fine-tuning]]** | 작업 적응 |
| **[[132_transfer_learning|Transfer Learning]]** | FM의 핵심 원리 |
| **규모의 경제** | 비용 효율 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Task-specific 모델 (~2017)] → [BERT/GPT (2018, FM 시작)]
    → [GPT-3 (2020, 대규모 FM)]
    → [Foundation Model 보고서 (Stanford, 2021)]
    → [현재: 멀티모달 FM (GPT-4o·Gemini)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Foundation Model은 **대학 교양 과정**이에요. 기초를 넓게 배워요.
2. 교양을 배운 후 **전공([[304_fine_tuning|Fine-tuning]])**을 정하면 빠르게 적응해요.
3. 한 번 교양을 배우면 **어떤 전공이든** 할 수 있어요!
