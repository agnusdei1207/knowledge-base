+++
title = "133. Fine-tuning (미세 조정) - 사전 학습 모델의 도메인 적응"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Fine-tuning은 <strong>사전 학습된 Foundation Model의 <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">가중치</a>를 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 특화 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>로 추가 학습하여 특정 작업 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>을 최적화</strong>하는 기법이며, Full [Fine-tuning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)·[LoRA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/)·Prompt Tuning으로 구분된다.
> 2. **가치**: 사전 학습 모델은 범용이라 특정 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)(의료·법률)에서 정확도가 부족하지만, Fine-tuning으로 <strong>소량 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>만으로도 전문 모델 수준</strong>을 달성한다.
> 3. **판단 포인트**: Full FT(전체 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/))는 비용^, [LoRA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/)(저랭크 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/))는 <strong>파라미터의 1% 미만만 학습</strong>하여 효율적이며, [QLoRA](/knowledge-base/studynote/10_ai/05_data_science_ml/404_qlora/)([양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)+[LoRA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/))로 소비자 GPU에서도 [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) Fine-tuning이 가능하다.

---

## Ⅰ. 개요 및 필요성

```text
Full FT:     전체 가중치 재학습 (GPU 많이 필요)
LoRA:        저랭크 행렬만 추가 학습 (효율적)
QLoRA:       4bit 양자화 + LoRA (소비자 GPU 가능)
Prompt Tuning: 프롬프트 벡터만 학습 (가장 경량)
```

- **📢 섹션 요약 비유**: Full FT는 집 전체 리모델링, LoRA는 벽지·가구만 교체, Prompt Tuning은 인테리어 소품만 바꾸기이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 방식 | 학습 파라미터 | [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
|:---|:---|:---|:---|
| **Full FT** | 100% | 많이 | 최고 |
| <strong><a href="/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/">LoRA</a></strong> | ~1% | **적음** | 우수 |
| <strong><a href="/knowledge-base/studynote/10_ai/05_data_science_ml/404_qlora/">QLoRA</a></strong> | ~1% | **최소** | 우수 |
| **Prompt** | <0.1% | 극소 | 보통 |

---

## Ⅲ~Ⅴ. 결론

[LoRA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/)/QLoRA는 <strong><a href="/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/">LLM</a> Fine-tuning의 사실상 표준</strong>이며, 소규모 팀도 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 특화 AI를 구축할 수 있게 했다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/">Fine-tuning</a></strong> | 사전 학습 후 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 적응 |
| <strong><a href="/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/">LoRA</a></strong> | 저랭크 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) (효율적) |
| <strong><a href="/knowledge-base/studynote/10_ai/05_data_science_ml/404_qlora/">QLoRA</a></strong> | [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)+[LoRA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) (소비자 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)) |
| **SFT** | Supervised [Fine-tuning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/250_rlhf_human_feedback_reinforcement_alignment_cot/">RLHF</a></strong> | 인간 피드백 강화학습 |

### 📈 관련 키워드 및 발전 흐름도

```text
[ImageNet Fine-tuning (2012)] -> [BERT Fine-tuning (2018)]
    -> [GPT-3 Few-shot (2020)] -> [LoRA (2021)]
    -> [QLoRA (2023)] -> [현재: DoRA·LoRA+ — 차세대 효율 FT]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Fine-tuning은 **대학 졸업생이 회사에서 실무를 배우는** 거예요.
2. LoRA는 <strong>핵심 과목만 추가 수강</strong>하는 효율적인 방법이에요.
3. [QLoRA](/knowledge-base/studynote/10_ai/05_data_science_ml/404_qlora/) 덕분에 <strong>작은 컴퓨터</strong>로도 AI를 맞춤 교육할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 133 / 420

<- **이전**: [132. Transfer Learning (전이 학습) - 사전 학습 모델의 재활용](/knowledge-base/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/)
**다음**: [134. PEFT (Parameter-Efficient Fine-Tuning) - 소수 파라미터만 학습하는 효율적 미세 조정](/knowledge-base/studynote/10_ai/02_dl_architecture_new/134_peft/) ->

---
