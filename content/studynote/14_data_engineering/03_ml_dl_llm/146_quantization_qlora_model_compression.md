---
title: 146. 양자화 & QLoRA - 모델 압축과 효율적 학습
date: '2026-04-19'
tags:
- studynote-dataengineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[434_quantization|양자화]]([[434_quantization|Quantization]])는 **FP32/FP16 가중치를 INT8/INT4로 축소**하여 메모리·연산을 줄이는 모델 [[347_compaction|압축]] 기법이며, QLoRA는 **4비트 [[434_quantization|양자화]]된 모델에 LoRA를 적용**하여 단일 소비자 [[418_gpu|GPU]](24GB)에서 [[263_llm_large_language_model|LLM]] Fine-tuning을 가능하게 했다.
> 2. **가치**: 7B 모델 FP16은 **14GB 메모리**이지만, 4비트 [[434_quantization|양자화]] 시 **3.5GB**로 축소되어 소비자 GPU에서 추론·학습이 가능하다.
> 3. **판단 포인트**: PTQ(Post-[[588_mlops_pipeline_automation|Training]] [[434_quantization|Quantization]], 학습 후)·QAT([[434_quantization|Quantization]]-Aware [[588_mlops_pipeline_automation|Training]], 학습 중)로 구분하며, GPTQ·AWQ·bitsandbytes가 [[263_llm_large_language_model|LLM]] [[434_quantization|양자화]]의 핵심 도구이다.

---

## Ⅰ. 개요 및 필요성

```text
FP16: 7B × 2B = 14GB
INT4: 7B × 0.5B = 3.5GB (4배 축소)
QLoRA = NF4 양자화 + LoRA + Double Quantization
  → 단일 24GB GPU에서 65B 모델 Fine-tuning
```

- **📢 섹션 요약 비유**: [[434_quantization|양자화]]는 **고해상도 사진을 [[347_compaction|압축]]**하는 것이다. [[501_file_definition_logical_record|파일]](메모리)은 작아지지만 품질([[282_performance_tactics|성능]])은 거의 유지된다.

---

## Ⅱ~Ⅴ. 결론

[[434_quantization|양자화]]+QLoRA는 **[[263_llm_large_language_model|LLM]] 민주화의 핵심 기술**이며, 소비자 GPU에서 대규모 모델 활용을 가능하게 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[434_quantization|양자화]]** | [[293_fp_function_point|FP]]→INT 축소 |
| **[[404_qlora|QLoRA]]** | 4비트+[[617_lora_lorawan_css_chirp_spread_spectrum|LoRA]] |
| **GPTQ** | PTQ 도구 |
| **AWQ** | 활성화 기반 [[434_quantization|양자화]] |
| **NF4** | [[138_normal_distribution|정규 분포]] 4비트 |

### 📈 관련 키워드 및 발전 흐름도

```text
[FP32 학습 (전통)] → [FP16/BF16 Mixed Precision (2018)]
    → [INT8 양자화 (2020)] → [GPTQ (2022)]
    → [QLoRA (2023)] → [현재: AWQ·GGUF — 추론 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[434_quantization|양자화]]는 **사진 [[347_compaction|압축]]**이에요. [[501_file_definition_logical_record|파일]]은 작아지지만 **사진은 거의 같아요**.
2. QLoRA는 **[[347_compaction|압축]] 사진에 포스트잇([[617_lora_lorawan_css_chirp_spread_spectrum|LoRA]])**을 붙이는 거예요. 빠르고 저렴해요.
3. 보통 컴퓨터에서도 **큰 AI를 돌릴 수** 있게 해줘요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 146 / 258

← **이전**: [[145_peft_lora_low_rank_adaptation|145. PEFT & LoRA (Low-Rank Adaptation) - 효율적 파라미터 미세 조정]]
**다음**: [[147_instruction_tuning_rlhf_alignment|147. 인스트럭션 튜닝 (Instruction Tuning) & RLHF]] →

---
