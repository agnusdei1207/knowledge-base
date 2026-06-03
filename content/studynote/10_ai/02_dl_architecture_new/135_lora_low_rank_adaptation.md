+++
title = "135. LoRA (Low-Rank Adaptation) - 효율적 LLM 미세 조정의 표준"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: LoRA는 **사전 학습된 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 행렬 W를 동결하고, 저랭크 행렬 A·B(rank r ≪ d)만 추가 학습**하여 W' = W + BA로 적응하는 [PEFT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/306_peft_lora/) 기법이다. 학습 파라미터가 **전체의 0.1~1%**로 극적으로 줄어든다.
> 2. **가치**: 70B LLM의 Full FT는 A100 8장+ 필요하지만, [QLoRA](/knowledge-base/studynote/10_ai/05_data_science_ml/404_qlora/)(4bit+[LoRA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/))는 **24GB [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 1장**으로 가능하여 개인/소규모 팀의 [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 커스텀을 실현했다.
> 3. **판단 포인트**: rank r=8~64, target modules=q_proj/v_proj가 표준이며, 여러 [LoRA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)를 **동적으로 교체([LoRA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) Swap)**하여 하나의 베이스 모델로 다양한 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 대응한다.

---

## Ⅰ. 개요 및 필요성

```text
LoRA: W' = W + BA  (W: 동결, B·A: 학습)
  W: d×d (수십억 파라미터)
  B: d×r, A: r×d (r=8~64, 극소수)
  → 학습 파라미터: 2dr (전체의 ~0.5%)
```

- **📢 섹션 요약 비유**: LoRA는 **건물(W)을 그대로 두고 간판([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/))만 바꾸는** 것이다. 건물 전체를 리모델링하는 것보다 100배 빠르고 저렴하다.

---

## Ⅱ~Ⅴ. 결론

LoRA는 **[LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) Fine-tuning의 사실상 표준**이며, [QLoRA](/knowledge-base/studynote/10_ai/05_data_science_ml/404_qlora/)·[DoRA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/)·[LoRA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/)+로 계속 발전하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[LoRA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/)** | 저랭크 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) |
| **[QLoRA](/knowledge-base/studynote/10_ai/05_data_science_ml/404_qlora/)** | 4bit [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) + [LoRA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) |
| **[DoRA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/)** | 방향/크기 분리 [LoRA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) |
| **[LoRA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) Swap** | [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) 동적 교체 |
| **Hugging Face [PEFT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/306_peft_lora/)** | [LoRA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) 구현 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[Full Fine-tuning (2018)] → [Adapter (2019)]
    → [LoRA (2021, Microsoft)] → [QLoRA (2023)]
    → [DoRA (2024)] → [현재: LoRA+ · GaLore — 차세대]
```

### 👶 어린이를 위한 3줄 비유 설명
1. LoRA는 건물([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))을 **그대로 두고 간판만 바꾸는** 거예요.
2. 건물 전체를 공사하는 것보다 **100배 빠르고 저렴**해요.
3. 간판만 바꿔도 **완전히 다른 가게([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/))**처럼 보인답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 135 / 420

← **이전**: [134. PEFT (Parameter-Efficient Fine-Tuning) - 소수 파라미터만 학습하는 효율적 미세 조정](/knowledge-base/studynote/10_ai/02_dl_architecture_new/134_peft/)
**다음**: [136. Prompt Tuning - 소프트 프롬프트로 LLM 적응](/knowledge-base/studynote/10_ai/02_dl_architecture_new/136_prompt_tuning/) →

---
