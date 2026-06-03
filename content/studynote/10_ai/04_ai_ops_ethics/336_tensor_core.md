+++
title = "336. 텐서 코어 (Tensor Core)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) ([Tensor Core](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)) 는 NVIDIA [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 에 내장된 전용 행렬 곱셈 가속기로, WMMA (Warp Matrix Multiply Accumulate) 연산을 FP16 입력 + FP32 누산 방식으로 단일 클록에 수행해 [CUDA](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/) Core 대비 수십 배 [FLOPS](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/137_flops/) 를 달성한다.
> 2. **가치**: FP16/BF16 혼합 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) ([Mixed Precision Training](/knowledge-base/studynote/14_data_engineering/04_mlops/173_tensor_core_hbm_mixed_precision_training/)) 를 활성화하면 VRAM 사용량 절반 감소 + [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) 풀 가속이라는 이중 이득이 발생한다.
> 3. **판단 포인트**: TF32 (TensorFloat-32) 는 FP32 범위에 FP16 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)를 결합한 NVIDIA 독자 포맷으로, Ampere 이상 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 에서 코드 변경 없이 자동 적용된다는 점이 출제 포인트다.

---

## Ⅰ. 개요 및 필요성

### 딥러닝 연산의 병목: 행렬 곱셈

[트랜스포머](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) ([Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)) 모델의 연산 중 약 85% 이상이 행렬 곱셈 (GEMM, General Matrix Multiply) 으로 구성된다. 기존 [CUDA](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/) Core 는 스칼라 (Scalar) 연산에 최적화되어 있어 행렬 곱셈을 수천 번의 FMA (Fused Multiply-Add) 로 분해해 처리했다.

| 하드웨어 | 연산 단위 | A100 FP16 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 비고 |
|:---|:---|:---:|:---|
| [CUDA](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/) Core | 스칼라 FP32 | 19.5 TFLOPS | 범용 연산 |
| [Tensor Core](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) | 행렬 4×4 FP16 | 312 TFLOPS | 행렬 곱 전용 |
| [Tensor Core](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) FP8 | 행렬 FP8 (H100) | 3,958 TFLOPS | 추론 특화 |

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)는 "계산기 대신 행렬 덧셈 전용 슈퍼 계산기"다. 일반 계산기([CUDA](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/) Core)로 행렬 덧셈을 하면 하나씩 더해야 하지만, [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)는 4×4 블록을 한 번에 처리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### WMMA (Warp Matrix Multiply Accumulate) 연산 구조

```
  텐서 코어 WMMA 연산: D = A × B + C
  ┌─────────────────────────────────────────────────────────┐
  │ A (FP16, 16×16) × B (FP16, 16×16) + C (FP32, 16×16)   │
  │ ─────────────────────────────────────────────────────── │
  │              D (FP32, 16×16)                            │
  │  한 클록 사이클에 16×16×16 = 4,096 회 FMA 수행          │
  └─────────────────────────────────────────────────────────┘

  GPU SM (Streaming Multiprocessor) 내부 구조
  ┌───────────────────────────────────────┐
  │          SM (A100 기준)               │
  │  ┌──────────────┐  ┌──────────────┐  │
  │  │  CUDA Core   │  │ Tensor Core  │  │
  │  │    × 128     │  │    × 4       │  │
  │  └──────────────┘  └──────────────┘  │
  │  ┌──────────────────────────────┐    │
  │  │    L1 Cache / Shared Memory  │    │
  │  └──────────────────────────────┘    │
  └───────────────────────────────────────┘
```

### [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 포맷 비교

| 포맷 | 부호 | 지수 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) | 가수 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) | 총 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) | 용도 |
|:---:|:---:|:---:|:---:|:---:|:---|
| FP32 | 1 | 8 | 23 | 32 | 기존 학습, 누산 |
| FP16 | 1 | 5 | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) | 16 | [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) 입력 |
| BF16 | 1 | 8 | 7 | 16 | [TPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/425_tpu/), Ampere+ 학습 |
| TF32 | 1 | 8 | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) | 19* | NVIDIA 자동 적용 |
| FP8 E4M3 | 1 | 4 | 3 | 8 | H100 추론 특화 |

*TF32 는 내부 연산 포맷, 저장 시 FP32 사용

### 혼합 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 학습 ([Mixed Precision Training](/knowledge-base/studynote/14_data_engineering/04_mlops/173_tensor_core_hbm_mixed_precision_training/)) 흐름

```
  ┌──────────────────────────────────────────────────────────┐
  │           Mixed Precision Training 파이프라인             │
  ├──────────────────────────────────────────────────────────┤
  │  FP32 마스터 가중치  ──▶  FP16 복사본 생성               │
  │         │                        │                       │
  │         │              순전파 (FP16 텐서 코어 가속)       │
  │         │                        │                       │
  │         │              역전파 (FP16 그래디언트 계산)      │
  │         │                        │                       │
  │         │     Loss Scaling 적용  │  (FP16 언더플로우 방지)│
  │         │                        │                       │
  │         └──◀ FP32 변환 후 가중치 업데이트 ───────────────┘
  └──────────────────────────────────────────────────────────┘
```

### Loss Scaling (손실 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)) 필요성

FP16 의 최솟값 약 6×[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)⁻⁵ 보다 작은 그래디언트는 <strong><a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/096_underflow/">언더플로우</a> (<a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/096_underflow/">Underflow</a>)</strong> 로 0이 된다. 해결책: Loss 에 2¹⁶ 를 곱해 그래디언트를 증폭한 뒤, FP32 변환 후 스케일 나눔.

- **📢 섹션 요약 비유**: 혼합 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)는 "초안(FP16)은 빠른 볼펜으로, 최종 서명(FP32)은 정확한 만년필로" 하는 것과 같다. 속도를 위해 낮은 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)로 계산하되, 핵심 보관은 높은 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)로 유지한다.

---

## Ⅲ. 비교 및 연결

### cuDNN / cuBLAS 와 [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) 연동

- <strong>cuBLAS (<a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/">CUDA</a> Basic Linear Algebra Subroutines)</strong>: GEMM 을 [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)로 자동 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)
- <strong>cuDNN (<a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/">CUDA</a> Deep Neural Network <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/">library</a>)</strong>: [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 선택 시 [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) 우선 활용
- **PyTorch**: `torch.set_float32_matmul_precision('high')` 로 TF32 활성화

### 세대별 [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) 발전

| 세대 | [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) | 추가된 포맷 | 최대 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) (FP16) |
|:---|:---|:---|:---:|
| Volta 1세대 | V100 | FP16 | 125 TFLOPS |
| Turing 2세대 | T4 | FP16, INT8, INT4 | 130 TFLOPS |
| Ampere 3세대 | A100 | BF16, TF32 추가 | 312 TFLOPS |
| Hopper 4세대 | H100 | FP8 추가 | 3,958 TFLOPS |

- **📢 섹션 요약 비유**: [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) 세대는 "연필(FP32) → 볼펜(FP16) → 레이저 프린터(FP8)" 로의 진화처럼, [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)를 조금 희생하는 대신 속도를 폭발적으로 높이는 방향으로 발전한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### PyTorch AMP (Automatic Mixed [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)) 활성화 예시

```python
from torch.cuda.amp import autocast, GradScaler
scaler = GradScaler()

for batch in dataloader:
    with autocast():           # FP16 자동 적용
        output = model(batch)
        loss = criterion(output, target)
    scaler.scale(loss).backward()   # Loss Scaling
    scaler.step(optimizer)
    scaler.update()
```

### 기술사 출제 포인트

- WMMA 연산의 입력 (FP16) + 누산 (FP32) 구조 명시
- FP16 vs BF16 비교: 지수 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수에 따른 수치 범위 차이
- Loss Scaling 필요 이유와 GradScaler 동작 원리
- TF32 가 코드 변경 없이 자동 적용되는 Ampere 이상 특성

- **📢 섹션 요약 비유**: Loss Scaling 은 "너무 가벼운 깃털을 저울로 달기 위해 무게를 100배로 불렸다가, 읽고 나서 100으로 나누는" 측정 트릭이다. FP16 의 표현 한계를 우회하는 영리한 방법이다.

---

## Ⅴ. 기대효과 및 결론

- **속도**: FP16 Mixed [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 으로 학습 속도 2~3배 향상
- **메모리**: VRAM 사용량 약 40~50% 절감
- **에너지**: 동일 연산량 대비 전력 소비 감소
- **생태계**: PyTorch AMP, TensorFlow, JAX 모두 자동 활성화 지원
- **한계**: 행렬 차원이 8 또는 16의 배수가 아니면 [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) 비활성화

[텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)는 현대 딥러닝 가속의 핵심 하드웨어 혁신이다. 기술사 시험에서는 WMMA 연산 구조, Mixed [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인, Loss Scaling 필요성, BF16 vs FP16 비교를 체계적으로 서술하면 고득점 가능하다.

- **📢 섹션 요약 비유**: [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)는 "[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 학습이라는 수백만 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 책을 1페이지씩 읽던 것을 챕터 단위로 한꺼번에 스캔하는 산업용 스캐너"다. 같은 책이지만 처리 속도가 수십 배 빠르다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| WMMA | 16×16 행렬 곱, 단일 사이클 / [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)의 핵심 연산 단위 |
| Mixed [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) | FP16 + FP32 누산 / [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) 활용의 필수 조합 |
| Loss Scaling | GradScaler, [언더플로우](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/096_underflow/) 방지 / FP16 수치 안정성 보완 |
| BF16 | 넓은 지수 범위, [TPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/425_tpu/) 친화 / FP16 대안, [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 선호 포맷 |
| TF32 | NVIDIA 독자 포맷, 자동 적용 / Ampere 이상 투명 가속 |
| cuBLAS / cuDNN | GEMM, Conv 최적화 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) / [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 처리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] → [텐서 코어 (Tensor Core)] → [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 🔢 [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)는 "수학 숙제를 한 문제씩 푸는 대신, 4×4 표 전체를 한 번에 푸는 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 수학 기계"예요.
2. 💡 FP16 은 더 빠르지만 소수점이 덜 정확해서, 중요한 결과만 FP32 로 꼼꼼히 보관해요.
3. 🚀 이 덕분에 같은 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 로 2~3배 빠르게, 메모리도 절반만 써서 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 를 학습할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 336 / 420

← **이전**: [335. 오토인코더 (Autoencoder)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/)
**다음**: [337. RLHF (Reinforcement Learning from Human Feedback)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/337_rlhf/) →

---
