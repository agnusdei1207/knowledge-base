---
title: 134. PEFT (Parameter-Efficient Fine-Tuning) - 소수 파라미터만 학습하는 효율적 미세 조정
date: '2026-04-19'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: PEFT는 **Foundation Model의 전체 파라미터 중 극소수(0.1~1%)만 추가·학습**하여 [[064_relation_domain|도메인]] 적응하는 기법의 총칭이며, [[617_lora_lorawan_css_chirp_spread_spectrum|LoRA]]·[[259_adapter_pattern_interface_wrapper|Adapter]]·Prefix Tuning·Prompt Tuning이 대표이다.
> 2. **가치**: 70B LLM을 Full FT하려면 A100 8장+가 필요하지만, [[306_peft_lora|PEFT]]([[404_qlora|QLoRA]])로는 **소비자 [[418_gpu|GPU]] 1장(24GB)**으로도 Fine-tuning이 가능하여 민주화를 실현한다.
> 3. **판단 포인트**: [[617_lora_lorawan_css_chirp_spread_spectrum|LoRA]](저랭크 행렬)가 [[282_performance_tactics|성능]] 대비 효율 최고이며, 여러 [[617_lora_lorawan_css_chirp_spread_spectrum|LoRA]] [[259_adapter_pattern_interface_wrapper|어댑터]]를 교체하여 **하나의 베이스 모델로 다양한 [[064_relation_domain|도메인]]에 대응**할 수 있다.

---

## Ⅰ. 개요 및 필요성

```text
Full FT:       100% 파라미터 학습 (비용↑↑)
LoRA:          저랭크 행렬만 학습 (~1%)
Adapter:       작은 모듈 삽입 (~3%)
Prefix Tuning: 프리픽스 벡터 학습 (<0.1%)
Prompt Tuning: 소프트 프롬프트 학습 (<0.01%)
```

- **📢 섹션 요약 비유**: Full FT는 집 전체 리모델링, LoRA는 벽지만 교체, Prompt Tuning은 액자만 바꾸기이다.

---

## Ⅱ~Ⅴ. 결론

PEFT는 **[[263_llm_large_language_model|LLM]] 시대의 필수 기술**이며, [[617_lora_lorawan_css_chirp_spread_spectrum|LoRA]]/QLoRA가 사실상 표준으로 소규모 팀의 [[190_ai_llm_requirements_specification|AI]] 커스텀을 가능하게 했다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[306_peft_lora|PEFT]]** | 효율적 [[133_fine_tuning|미세 조정]] 총칭 |
| **[[617_lora_lorawan_css_chirp_spread_spectrum|LoRA]]** | 저랭크 [[259_adapter_pattern_interface_wrapper|어댑터]] (표준) |
| **[[404_qlora|QLoRA]]** | [[434_quantization|양자화]]+[[617_lora_lorawan_css_chirp_spread_spectrum|LoRA]] |
| **[[259_adapter_pattern_interface_wrapper|Adapter]]** | [[192_module_independence|모듈]] 삽입형 |
| **[[136_prompt_tuning|Prompt Tuning]]** | 소프트 프롬프트 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Full Fine-tuning (2018)] → [Adapter (2019)]
    → [Prefix Tuning (2021)] → [LoRA (2021)]
    → [QLoRA (2023)] → [현재: DoRA·LoRA+ — 차세대 PEFT]
```

### 👶 어린이를 위한 3줄 비유 설명
1. PEFT는 **집 전체를 리모델링하지 않고 벽지만 바꾸는** 거예요.
2. 벽지([[617_lora_lorawan_css_chirp_spread_spectrum|LoRA]])만 바꿔도 **분위기([[282_performance_tactics|성능]])가 완전히** 달라져요.
3. 비용이 **100분의 1**로 줄어서 누구나 AI를 맞춤 제작할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 134 / 420

← **이전**: [[133_fine_tuning|133. Fine-tuning (미세 조정) - 사전 학습 모델의 도메인 적응]]
**다음**: [[135_lora_low_rank_adaptation|135. LoRA (Low-Rank Adaptation) - 효율적 LLM 미세 조정의 표준]] →

---
