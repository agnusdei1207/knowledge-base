---
title: "PEFT (Parameter-Efficient Fine-Tuning) / LoRA (Low-Rank Adaptation)"
date: "2026-05-09"
tags:
  - "studynote-ai"
weight: 306
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PEFT (Parameter-Efficient [Fine-Tuning](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/), [파라미터 효율적 미세 조정](/studynote/06_ict_convergence/04_ai_llm/282_peft_parameter_efficient_fine_tuning/))는 대형 모델의 전체 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 동결(Freeze)하고 소수의 추가 파라미터만 학습하는 [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) 기법으로, [LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) ([Low-Rank Adaptation](/studynote/14_data_engineering/03_ml_dl_llm/145_peft_lora_low_rank_adaptation/), 저랭크 적응)는 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 업데이트 ΔW를 두 개의 저랭크 행렬 A·B의 곱으로 근사하는 가장 인기 있는 PEFT 방법이다.
> 2. **가치**: 전체 [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) 대비 학습 파라미터를 99% 이상 줄이면서 거의 동등한 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 달성하여, 소비자 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)(24GB VRAM) 한 장으로도 70B 파라미터 LLM의 [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)을 가능하게 한다.
> 3. **판단 포인트**: LoRA에서 랭크(Rank, r)는 핵심 하이퍼파라미터로, r이 클수록 표현력은 높지만 파라미터 수가 늘어난다. 실무에서는 r=4~64 범위에서 [태스크](/studynote/02_operating_system/02_process_thread/150_task/) 복잡도에 맞게 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)한다.

---

## Ⅰ. 개요 및 필요성

[GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-3는 175B(1750억) 개의 파라미터를 가진다. 전체 [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)을 위해 [역전파](/studynote/10_ai/03_llm_nlp/272_backpropagation/) 그래디언트를 모든 파라미터에 대해 저장하면 FP32 기준 700GB 이상의 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리가 필요하다. 이는 수십 장의 고가 A100 GPU를 요구하며, 대부분의 기업과 연구자에게 접근 불가능한 수준이다.

PEFT는 이 문제를 "대부분의 파라미터는 동결(Frozen)하고, 핵심 위치에 소수의 학습 가능한 파라미터만 추가한다"는 아이디어로 해결한다. LoRA는 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 행렬의 실제 업데이트가 <strong>낮은 내재 차원(Low Intrinsic Dimension)</strong>에서 이루어진다는 가설을 기반으로, ΔW를 두 저랭크 행렬의 곱으로 표현한다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 175B 파라미터 전체를 [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)하는 건 직원 1억 명 회사에서 모든 직원의 업무 방식을 바꾸는 것이고, LoRA는 핵심 의사결정자 10명(저랭크 행렬)의 업무 방식만 바꿔서 회사 전체 방향을 조정하는 것이다. 10명만 교육해도 전체 성과가 바뀌는 마법이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+------------------------------------------------------------------+
|         LoRA (Low-Rank Adaptation) 수학적 구조                     |
+------------------------------------------------------------------+
|                                                                  |
|  전체 파인 튜닝:                                                    |
|  W' = W + ΔW  (W: d×d 행렬, ΔW: d×d 행렬 전체 학습)              |
|  파라미터 수: d×d (예: 4096×4096 = 16.7M)                         |
|                                                                  |
|  LoRA:                                                           |
|  W' = W + ΔW = W + (B · A)                                      |
|    W: d×d  <- 동결 (Frozen, 학습 안 함)                             |
|    A: d×r  <- 학습 가능 (r << d, 예: r=8, d=4096 -> 4096×8 = 32K) |
|    B: r×d  <- 학습 가능 (r=8, d=4096 -> 8×4096 = 32K)             |
|    ΔW = B·A: d×d  (행렬 곱이지만 파라미터는 2×d×r만 학습)           |
|                                                                  |
|  파라미터 절감 비율:                                                 |
|  전체: d^ = 16.7M | LoRA(r=8): 2×d×r = 65K -> 0.39% 만 학습!     |
|                                                                  |
|  +------------------------------------------------+              |
|  |  입력 x                                         |              |
|  |    +---> W (동결) ----------------------+       |              |
|  |    +---> A (학습) ---> B (학습) -------> + ---> 출력|              |
|  +------------------------------------------------+              |
|                                                                  |
|  초기화: A = 랜덤 가우시안, B = 0 (학습 초기 ΔW=0으로 시작)          |
|  스케일링: ΔW에 α/r 비율로 스케일 적용 (α: 스케일 하이퍼파라미터)      |
+------------------------------------------------------------------+
```

| PEFT 방법 | 파라미터 추가 위치 | 특징 |
|:---|:---|:---|
| [LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) | 어텐션 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 행렬 내 | 추론 시 병합 가능, 속도 패널티 없음 |
| [QLoRA](/studynote/10_ai/05_data_science_ml/404_qlora/) | [LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) + 4비트 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) | 70B 모델을 소비자 GPU에서 [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) |
| [Adapter](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) | [트랜스포머](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 레이어 사이 삽입 | 레이어 간 작은 MLP 추가 |
| Prefix Tuning | 입력 앞에 학습 가능 토큰 추가 | 프롬프트 수준의 경량 적응 |

- **📢 섹션 요약 비유**: LoRA에서 B를 0으로 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화하는 이유는 설계도다. 새 사원([LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) 파라미터)이 입사 첫날 기존 업무(W)에 아무 영향을 주지 않도록 "처음엔 조용히 있다가 학습이 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)되면 조금씩 기여해"라고 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)하는 것이다. 갑자기 개입했다가 기존 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 망치는 사고를 방지한다.

---

## Ⅲ. 비교 및 연결

<strong><a href="/studynote/10_ai/05_data_science_ml/404_qlora/">QLoRA</a> (<a href="/studynote/10_ai/05_data_science_ml/404_qlora/">Quantized LoRA</a>)</strong>: LoRA에 4비트 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/))를 결합하여 70B LLM을 단일 48GB [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)(예: RTX 4090 2장)에서 [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) 가능하게 한다. 2023년 등장 직후 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 커뮤니티의 표준 [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) 방법으로 자리 잡았다.

<strong><a href="/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/">LoRA</a> 병합 (<a href="/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/">LoRA</a> Merging)</strong>: 훈련 완료 후 W' = W + B·A를 계산하여 원본 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)에 통합하면, 추론 시 별도의 A·B 행렬 연산이 필요 없어 추론 속도 패널티가 제로다.

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 작은 규모, 개념 학습 |
| PEFT (Parameter-Efficient [Fine-Tuning](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)) / [LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) ([Low-Rank Adaptation](/studynote/14_data_engineering/03_ml_dl_llm/145_peft_lora_low_rank_adaptation/)) | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 고도화 단계 |

- **📢 섹션 요약 비유**: QLoRA는 기존 집에 에어컨([LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) 파라미터)을 달면서 집 전체를 미니어처로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)([양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/))하는 것이다. 집이 1/4 크기로 줄어도 에어컨이 작동하니 냉방([파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)) 효과는 유지된다. 작은 원룸(소비자 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))에도 에어컨 달린 집을 들여놓을 수 있게 됐다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/">LoRA</a> 하이퍼파라미터 설계 가이드</strong>:
- `r` (랭크): 4~64. [태스크](/studynote/02_operating_system/02_process_thread/150_task/) 복잡도가 높을수록 크게. 기본값 r=8
- `alpha`: 보통 r의 2배. ΔW의 스케일 조정
- `target_modules`: Q, V 행렬에만 적용 (Attention 레이어 권장)
- `lora_dropout`: 0.05~0.1 (과적합 방지)

<strong><a href="/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/">LoRA</a> 적용 레이어 선택</strong>: 어텐션 레이어의 Q, V 행렬에 LoRA를 적용하는 것이 가장 효과적이다. K 행렬은 Q와 유사 역할을 해 중복될 수 있으며, FFN(Feed-[Forward](/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/) Network) 레이어 추가 적용 시 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상과 파라미터 증가 트레이드오프를 고려해야 한다.

- **📢 섹션 요약 비유**: [LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) 레이어 선택은 건물 보강 공사와 같다. 전체 기둥(모든 레이어)에 철근([LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/))을 추가하면 완벽하지만 공사비가 폭발한다. 가장 중요한 핵심 기둥(Q, V 어텐션 행렬)에만 철근을 추가해도 건물(모델) 강도는 충분히 높아진다.

---

## Ⅴ. 기대효과 및 결론

PEFT/LoRA는 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)의 민주화를 실현했다. 수십 장의 A100 GPU가 필요하던 작업을 RTX 3090 한 장으로 가능하게 하여, 개인 연구자와 스타트업도 최신 LLM을 자신의 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 맞게 커스터마이징할 수 있게 됐다. LoRA를 기반으로 한 다양한 변형([DoRA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/), AdaLoRA, GaLore)이 계속 등장하며 파라미터 효율성의 한계를 계속 넓히고 있다. [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 [LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)은 이제 표준 구성 요소다.

- **📢 섹션 요약 비유**: LoRA는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 세계의 3D 프린터다. 과거에는 전문 공장(대형 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 클러스터)에서만 AI를 만들 수 있었지만, [LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) 덕분에 이제 개인 집에서 3D 프린터(소비자 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))로 맞춤 부품([파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) 모델)을 바로 뽑아낼 수 있다. [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 제조의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)화·민주화 혁명이 일어나고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 저랭크 [행렬 분해](/studynote/08_algorithm_stats/10_linear_algebra/161_matrix_decomposition/) | 랭크 r, A×B / LoRA의 핵심 수학 원리 |
| [QLoRA](/studynote/10_ai/05_data_science_ml/404_qlora/) | 4비트 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/), 소비자 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) / LoRA에 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)를 결합한 경량화 |
| [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) ([Fine-Tuning](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)) | [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 업데이트, [전이 학습](/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/) / PEFT가 개선하는 기존 학습 방식 |
| [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) ([Adapter](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)) | 레이어 삽입, PEFT 변형 / LoRA와 함께 대표적 PEFT 방법 |
| [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) ([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)) | INT8, INT4, 모델 경량화 / QLoRA에서 LoRA와 결합되는 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] -> [PEFT (Parameter-Efficient Fine-Tuning) / LoRA (Low-Rank Adaptation)] -> [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. <strong><a href="/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/">LoRA</a></strong>는 엄청 큰 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)(175B 파라미터)를 가르칠 때, **전체 대신 핵심 부분 1%만 바꿔서** 거의 같은 효과를 내는 똑똑한 절약법이에요!
2. 큰 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 행렬 ΔW를 두 개의 <strong>작은 행렬 A×B의 곱</strong>으로 대신 표현해서 배워야 하는 숫자를 99% 줄이는 수학 마법이에요.
3. 덕분에 집에 있는 게임용 GPU로도 <strong>거대한 ChatGPT급 모델을 내 용도에 맞게 학습</strong>시킬 수 있게 됐어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 306 / 420

<- **이전**: [305. 프롬프트 엔지니어링 (Prompt 엔진ering)](/studynote/10_ai/04_ai_ops_ethics/305_prompt_engineering/)
**다음**: [307. 할루시네이션 (Hallucination)](/studynote/10_ai/04_ai_ops_ethics/307_hallucination/) ->

---
