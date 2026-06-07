---
title: "QLoRA (Quantized LoRA)"
date: "2026-05-09"
tags:
  - "studynote-ai"
weight: 404
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: QLoRA (Quantized [LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/))는 사전 학습된 거대 모델의 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 4비트로 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/))한 상태에서, 저차원 [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)([LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/))만을 학습시켜 메모리 사용량을 획기적으로 줄인 효율적 [미세 조정](/studynote/10_ai/02_dl_architecture_new/133_fine_tuning/) 기법이다.
> 2. **가치**: 기존 LoRA보다 더 적은 메모리로도 동등한 수준의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 유지하며, 단일 소비자용 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)(예: RTX 3090)에서도 65B 파라미터급 모델을 [미세 조정](/studynote/10_ai/02_dl_architecture_new/133_fine_tuning/)할 수 있게 해주는 '[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 민주화'의 핵심 기술이다.
> 3. **판단 포인트**: 4-[bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) NormalFloat (NF4), Double [Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/), Paged Optimizers라는 세 가지 핵심 기술이 결합되어 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 손실을 최소화하고 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 하락을 방어한다.

---

## Ⅰ. 개요 및 필요성

[대규모 언어 모델](/studynote/04_software_engineering/09_cloud_native_ai_architecture/582_llm_based_code_generation_tools/)([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/))을 [미세 조정](/studynote/10_ai/02_dl_architecture_new/133_fine_tuning/)([Fine-tuning](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/))하려면 모델 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)와 [옵티마이저](/studynote/05_database/03_relational_model/163_optimizer_sql_execution_plan_generator/) 상태를 저장하기 위해 막대한 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리가 필요하다. [LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/)(306번)가 매개변수 수를 줄였음에도 불구하고, 여전히 기본 모델 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)(FP16 등) 자체가 차지하는 공간이 병목이었다. QLoRA는 이 '기본 모델'마저도 극도로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)하여 학습 가능하게 만든다.

**필요성**:
- <strong><a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/">GPU</a> 자원 한계 극복</strong>: 수천만 원대 기업용 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 없이도 개인용 GPU에서 거대 모델 학습 가능
- <strong><a href="/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/">정밀도</a> 유지</strong>: 단순히 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수만 줄이는 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)와 달리, 학습 과정에서 손실되는 정보를 NF4 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입을 통해 보존
- **학습 속도 및 비용 최적화**: 메모리 효율화를 통해 더 큰 [배치 사이즈](/studynote/10_ai/05_data_science_ml/346_batch_size_generalization/)를 사용하거나 클라우드 대여 비용 절감

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: QLoRA는 수천 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)의 백과사전(모델 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/))을 아주 작은 마이크로필름(4비트 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/))으로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)한 뒤, 그 위에 포스트잇([LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/))을 붙여 메모를 남기며 공부하는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

QLoRA는 세 가지 혁신적인 기술을 통해 4비트 환경에서도 FP16 수준의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 실현한다.

| 기술 요소 | 설명 | 특징 |
|:---|:---|:---|
| **NF4 (NormalFloat 4)** | [정규 분포](/studynote/08_algorithm_stats/08_stats/138_normal_distribution/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 최적화된 4비트 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입 | 일반적인 4비트 정수보다 정보 보존력이 우수함 |
| <strong>Double <a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/">Quantization</a></strong> | [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)에 필요한 상수([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) Constants)마저 다시 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) | 추가적인 메모리 절감 (파라미터당 약 0.37비트) |
| **Paged Optimizers** | [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리 부족 시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 CPU RAM으로 임시 이동([Paging](/studynote/02_operating_system/04_synchronization/259_paging/)) | [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) ([Out of Memory](/studynote/02_operating_system/02_process_thread/157_oom_killer/)) 에러를 방지하고 학습 연속성 보장 |

```text
[ QLoRA 학습 구조 ]

1. Base Model (Fixed, 4-bit NF4) <--- 고정된 백과사전 (압축됨)
   |
2. Dequantization (on-the-fly to BF16) <--- 연산 시에만 일시적으로 복원
   |
3. Forward/Backward Pass (LoRA Layers, BF16/FP16) <--- 실제 학습되는 부분
   |
4. Update Adapters (Weights only) <--- 포스트잇에만 기록 업데이트

    [ GPU Memory ]
    +-----------------------------------+
    | 4-bit Frozen Weights (NF4)        | <--- 대부분의 공간 (초절약)
    +-----------------------------------+
    | 16-bit LoRA Adapters (Learnable)  | <--- 미세한 조정 (정밀함)
    +-----------------------------------+
```

- **📢 섹션 요약 비유**: 연산할 때만 마이크로필름의 내용을 돋보기(Dequantization)로 비추어 보고, 필기(학습)는 별도의 노트([LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/))에 정교하게 기록하는 방식이다.

---

## Ⅲ. 비교 및 연결

| 항목 | Full [Fine-tuning](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) | [LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) (306번) | QLoRA (404번) |
|:---|:---|:---|:---|
| 메모리 점유 | 매우 높음 (전체 파라미터) | 중간 ([가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 보존 필요) | 매우 낮음 ([가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 4비트화) |
| [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) | 원본 유지 (FP32/16) | 원본 유지 (FP16) | NF4 기반 근사 ([성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 하락 거의 없음) |
| 권장 사양 | 다중 A100/H100 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) | 단일 A100급 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) | 단일 RTX 3090/4090급 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) |

QLoRA는 312번의 <strong><a href="/studynote/10_ai/04_ai_ops_ethics/312_quantization/">모델 양자화</a>(<a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/">Quantization</a>)</strong> 기술과 306번의 <strong><a href="/studynote/10_ai/04_ai_ops_ethics/306_peft_lora/">PEFT</a>(매개변수 효율적 <a href="/studynote/10_ai/02_dl_architecture_new/133_fine_tuning/">미세 조정</a>)</strong> 기술이 정교하게 결합된 형태다.

- **📢 섹션 요약 비유**: 전체 [미세 조정](/studynote/10_ai/02_dl_architecture_new/133_fine_tuning/)이 건물 전체를 새로 짓는 것이고, LoRA가 인테리어만 바꾸는 것이라면, QLoRA는 인테리어 재료마저도 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 포장해서 좁은 트럭 한 대에 다 싣고 와서 작업하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 고려 사항
1. <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 타입 선택</strong>: 하드웨어가 지원한다면 FP16보다 BF16을 사용하는 것이 QLoRA의 수치적 안정성 측면에서 유리하다.
2. <strong><a href="/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/">LoRA</a> Rank <a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong>: `r` 값(Rank)을 64나 128 정도로 충분히 높여주어야 4비트 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)로 인한 미세한 표현력 저하를 보상할 수 있다.
3. **병목 현상**: 연산 시마다 수행되는 역양자화(Dequantization) 과정으로 인해 순수 FP16 학습보다는 속도가 약간 느려질 수 있음을 감안해야 한다.

### 기술사 판단 포인트
- QLoRA는 기업이 <strong>'<a href="/studynote/09_security/16_data_privacy/809_data_sovereignty/">데이터 주권</a>(<a href="/studynote/06_ict_convergence/05_data_science/410_ai_intellectual_property_data_sovereignty_data_act/">Data Sovereignty</a>)'</strong>을 지키기 위해 폐쇄망 내부 사양의 GPU로 독자 모델을 구축하려 할 때 가장 현실적이고 강력한 대안임을 강조해야 한다.

- **📢 섹션 요약 비유**: 트럭이 작아져서(메모리 절감) 좁은 길(개인용 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))도 갈 수 있게 되었지만, [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)을 풀고 짐을 내리는 데 시간이 조금 더 걸리는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

QLoRA는 '거대 모델은 빅테크만의 전유물'이라는 편견을 깼다. 연구자들과 중소기업은 이제 적은 비용으로도 최신 SOTA 모델을 자신의 특화된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 맞춰 튜닝할 수 있게 되었다.

미래에는 4비트를 넘어 2비트, 심지어 1.5비트 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 기반의 학습 기술이 등장하여 스마트폰이나 임베디드 기기에서도 실시간 학습이 가능해지는 시대가 올 것이다.

- **📢 섹션 요약 비유**: QLoRA 덕분에 이제 누구나 자기 방 작은 책상 위에서 거대한 [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)이라는 우주선을 수리할 수 있게 되었다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| NF4 | 핵심 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입 / [정규 분포](/studynote/08_algorithm_stats/08_stats/138_normal_distribution/)를 따르는 모델 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)에 특화된 4비트 형식 |
| Paged Optimizers | 안정성 확보 / [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리 한계를 CPU로 확장하는 기술 |
| BitsAndBytes | 구현 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) / QLoRA의 핵심 연산을 담당하는 Python [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) |
| [PEFT](/studynote/10_ai/04_ai_ops_ethics/306_peft_lora/) | 상위 범주 / 매개변수 중 일부만 효율적으로 학습하는 기법들의 총칭 |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] -> [QLoRA (Quantized LoRA)] -> [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 아주 큰 로봇을 고치려면 로봇만큼 큰 창고와 장비가 필요했어요.
2. QLoRA는 로봇을 아주 작게 접어서 작은 가방 안에 쏙 넣는 마법을 부린 거예요.
3. 덕분에 내 방 작은 책상 위에서도 로봇의 중요한 부분만 콕 집어 더 똑똑하게 만들 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 404 / 420

<- **이전**: [403. RLHF 보상 모델 (Reward Model)](/studynote/10_ai/05_data_science_ml/403_rlhf_reward_model/)
**다음**: [405. 파이프라인 병렬화 (GPipe)](/studynote/10_ai/05_data_science_ml/405_gpipe_pipeline_parallelism/) ->

---
