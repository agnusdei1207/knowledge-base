---
title: "146. Quantization Qlora Model Compression"
date: "2026-04-19"
tags:
  - "studynote-dataengineering"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/))는 <strong>FP32/FP16 가중치를 INT8/INT4로 축소</strong>하여 메모리·연산을 줄이는 모델 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 기법이며, QLoRA는 <strong>4비트 <a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/">양자화</a>된 모델에 LoRA를 적용</strong>하여 단일 소비자 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)(24GB)에서 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) Fine-tuning을 가능하게 했다.
> 2. **가치**: 7B 모델 FP16은 <strong>14GB 메모리</strong>이지만, 4비트 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 시 <strong>3.5GB</strong>로 축소되어 소비자 GPU에서 추론·학습이 가능하다.
> 3. **판단 포인트**: PTQ(Post-[Training](/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/) [Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/), 학습 후)·QAT([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)-Aware [Training](/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/), 학습 중)로 구분하며, GPTQ·AWQ·bitsandbytes가 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)의 핵심 도구이다.

---

## Ⅰ. 개요 및 필요성

```text
FP16: 7B × 2B = 14GB
INT4: 7B × 0.5B = 3.5GB (4배 축소)
QLoRA = NF4 양자화 + LoRA + Double Quantization
  -> 단일 24GB GPU에서 65B 모델 Fine-tuning
```

- **📢 섹션 요약 비유**: [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 <strong>고해상도 사진을 <a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a></strong>하는 것이다. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(메모리)은 작아지지만 품질([성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))은 거의 유지된다.

---

## Ⅱ~Ⅴ. 결론

[양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)+QLoRA는 <strong><a href="/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/">LLM</a> 민주화의 핵심 기술</strong>이며, 소비자 GPU에서 대규모 모델 활용을 가능하게 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/">양자화</a></strong> | [FP](/studynote/12_it_management/05_security_compliance/293_fp_function_point/)->INT 축소 |
| <strong><a href="/studynote/10_ai/05_data_science_ml/404_qlora/">QLoRA</a></strong> | 4비트+[LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) |
| **GPTQ** | PTQ 도구 |
| **AWQ** | 활성화 기반 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) |
| **NF4** | [정규 분포](/studynote/08_algorithm_stats/08_stats/138_normal_distribution/) 4비트 |

### 📈 관련 키워드 및 발전 흐름도

```text
[FP32 학습 (전통)] -> [FP16/BF16 Mixed Precision (2018)]
    -> [INT8 양자화 (2020)] -> [GPTQ (2022)]
    -> [QLoRA (2023)] -> [현재: AWQ·GGUF — 추론 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 <strong>사진 <a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a></strong>이에요. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 작아지지만 **사진은 거의 같아요**.
2. QLoRA는 <strong><a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a> 사진에 포스트잇(<a href="/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/">LoRA</a>)</strong>을 붙이는 거예요. 빠르고 저렴해요.
3. 보통 컴퓨터에서도 **큰 AI를 돌릴 수** 있게 해줘요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 146 / 258

<- **이전**: [145. PEFT & LoRA (Low-Rank Adaptation) - 효율적 파라미터 미세 조정](/studynote/14_data_engineering/03_ml_dl_llm/145_peft_lora_low_rank_adaptation/)
**다음**: [147. 인스트럭션 튜닝 (Instruction Tuning) & RLHF](/studynote/14_data_engineering/03_ml_dl_llm/147_instruction_tuning_rlhf_alignment/) ->

---
