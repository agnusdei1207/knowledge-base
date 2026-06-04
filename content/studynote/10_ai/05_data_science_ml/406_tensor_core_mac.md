---
title: "406. 텐서 코어 (Tensor Core)"
date: "2026-05-09"
tags:
  - "studynote-ai"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)([Tensor Core](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/))는 엔비디아(NVIDIA) [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 아키텍처에 탑재된 [하드웨어 가속기](/studynote/01_computer_architecture/12_accelerators_ai_hardware/417_hardware_accelerator/)로, 딥러닝의 핵심 연산인 거대 행렬 곱셈 및 누산(FMA: Matrix [Multiply-Accumulate](/studynote/01_computer_architecture/12_accelerators_ai_hardware/428_mac_operation/))을 한 번의 클럭에 처리하도록 설계된 전용 유닛이다.
> 2. **가치**: 일반 [CUDA](/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/) 코어 대비 수십 배 빠른 연산 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 제공하며, 혼합 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)(Mixed [Precision](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)) 학습을 통해 모델의 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)는 유지하면서 학습 속도를 획기적으로 개선하고 전력 효율을 높인다.
> 3. **판단 포인트**: [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)(FP32, FP16, BF16, TF32, INT8)와 속도 사이의 트레이드오프를 하드웨어 레벨에서 최적화하므로, 최신 아키텍처(Volta~Blackwell)의 기능을 소프트웨어 프레임워크와 연동하는 것이 실무적 핵심이다.

---

## Ⅰ. 개요 및 필요성

딥러닝 모델의 90% 이상의 연산은 행렬 곱셈으로 이루어진다. 기존의 범용 [CUDA](/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/) 코어는 스칼라 연산 위주로 설계되어 거대 행렬 연산 시 수많은 클럭이 소요되는 한계가 있었다. [텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)는 '행렬 자체를 기본 연산 단위'로 취급함으로써 [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 연산의 패러다임을 바꿨다.

**필요성**:
- <strong>연산 <a href="/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a>(<a href="/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">Throughput</a>) 극대화</strong>: 한 클럭에 4x4, 16x16 행렬 연산을 동시에 수행하여 TFLOPS [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 비약적으로 향상
- <strong>혼합 <a href="/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/">정밀도</a> 지원</strong>: [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 저장은 FP16으로 하여 메모리를 아끼고, 연산 결과는 FP32로 누적하여 수치적 안정성 확보
- **거대 모델 학습 가속**: [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 기반의 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 학습에 필수적인 고속 행렬 연산 자원 제공

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 일반 [CUDA](/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/) 코어가 한 번에 한 칸씩 색칠하는 붓이라면, [텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)는 도장을 찍듯이 한 번에 수십 칸의 행렬을 채워버리는 대형 스탬프와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)의 핵심은 **D = A * B + C** 연산을 하드웨어적으로 한 번에 수행하는 하이브리드 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 연산 방식에 있다.

| 요소 | 설명 | 특징 |
|:---|:---|:---|
| **FMA (Matrix FMA)** | 행렬 곱셈 후 덧셈을 한 번에 수행 | 반올림 오차를 줄이고 속도를 높임 |
| **TF32 (Tensor Float 32)** | FP32의 범위와 FP16의 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)를 결합 | 코드 수정 없이 FP32 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 가속 (Ampere 이후) |
| **FP8 / INT8** | 더 낮은 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수의 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 지원 | 추론(Inference) 가속 및 메모리 점유 극단적 축소 |
| <strong>Sparse <a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/">Tensor Core</a></strong> | 값이 0인 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 건너뛰는 연산 가속 | 2:4 구조의 희소성(Sparsity)을 활용해 2배 속도 향상 |

```text
[ 텐서 코어 연산 메커니즘 (Mixed Precision) ]

   Input A (FP16)  x  Input B (FP16)  +  Input C (FP32)
   +-------------+    +-------------+    +-------------+
   | 4x4 Matrix  |    | 4x4 Matrix  |    | 4x4 Matrix  |
   +-------------+    +-------------+    +-------------+
          |                  |                  |
          +--------+---------+                  |
                   v                            |
        [ Tensor Core Unit ] <-------------------+
                   |
                   v
            Output D (FP32) <--- 고정밀 누산 결과
```

- **📢 섹션 요약 비유**: [텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)는 수학 문제를 풀 때 암산 대신 전용 계산기를 쓰는 것과 같다. 특히 '곱하기'와 '더하기'가 동시에 되는 마법의 계산기다.

---

## Ⅲ. 비교 및 연결

| 항목 | [CUDA](/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/) Core (범용) | [Tensor Core](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) (특화) |
|:---|:---|:---|
| 연산 단위 | 스칼라 / 벡터 (Single Value) | 행렬 (Matrix) |
| [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 범위 | FP64, FP32, FP16 등 다양함 | FP16, BF16, TF32, FP8, INT8 특화 |
| [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 밀도 | 보통 (그래픽, 물리 연산 적합) | 매우 높음 (딥러닝 학습/추론 적합) |
| 도입 세대 | 이전부터 존재 | Volta(V100) 아키텍처부터 탑재 |

[텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) 기술은 312번의 <strong><a href="/studynote/10_ai/04_ai_ops_ethics/312_quantization/">모델 양자화</a>(<a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/">Quantization</a>)</strong>를 하드웨어적으로 뒷받침하며, 405번의 <strong><a href="/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a> 학습 기법</strong>들과 결합되어 모델 학습 시간을 며칠에서 몇 시간으로 단축한다.

- **📢 섹션 요약 비유**: [CUDA](/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/) 코어가 승용차라면, [텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)는 한 번에 수백 명을 실어 나르는 고속열차와 같다. 정해진 노선(행렬 연산)에서는 압도적으로 빠르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 고려 사항
1. **Dimension Alignment**: [텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)0% 끌어내려면 행렬의 크기([배치 사이즈](/studynote/10_ai/05_data_science_ml/346_batch_size_generalization/), 히든 레이어 크기)가 8 또는 16의 배수여야 한다. ([Padding](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) 필요)
2. <strong>Automatic Mixed <a href="/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/">Precision</a> (AMP)</strong>: PyTorch나 TensorFlow에서 제공하는 AMP 기능을 활성화하여 수동 최적화 없이 [텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)를 사용하도록 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)해야 한다.
3. **Loss Scaling**: FP16 사용 시 그래디언트 값이 너무 작아져 0으로 수렴하는 [Underflow](/studynote/01_computer_architecture/02_data_representation_arithmetic/096_underflow/) 문제를 막기 위해 Loss Scaling 기법이 필수적이다.

### 기술사 판단 포인트
- [텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)의 발전은 단순히 속도 경쟁이 아니라 <strong>'<a href="/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/">정밀도</a>의 경제학'</strong>이다. 최신 H100 GPU의 FP8 지원처럼, 실제 모델의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 없이 어디까지 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)를 낮춰 연산 밀도를 높일 수 있는지가 하드웨어와 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 공동 목표임을 강조해야 한다.

- **📢 섹션 요약 비유**: 기차가 빨리 가려면 승객 수도 중요하지만, 역 간격(행렬 크기)을 일정하게 맞추고 선로 상태([정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 제어)를 잘 관리해야 사고 없이 최고 속도를 낼 수 있다.

---

## Ⅴ. 기대효과 및 결론

[텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)는 소프트웨어 발전 속도를 하드웨어가 견인한 대표적인 사례다. 이 하드웨어적 혁신이 없었다면 현재의 수조 개 파라미터를 가진 LLM은 탄생할 수 없었을 것이다.

앞으로는 [텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)를 넘어 [트랜스포머](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 전용 가속기([Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 엔진)가 탑재된 블랙웰(Blackwell) 아키텍처처럼, 특정 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에 완전히 종속된 전용 [ASIC](/studynote/01_computer_architecture/01_basic_electronics_logic/070_asic/)(Application-Specific IC)의 성격이 더욱 강해질 것이다.

- **📢 섹션 요약 비유**: [텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)는 [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)이라는 거대한 제국을 건설하기 위해 만들어진 가장 강력한 중장비다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Mixed [Precision](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) | 구현 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) / FP16과 FP32를 섞어 쓰는 효율적 학습 방식 |
| TF32 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입 / FP32의 편리함과 [텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 합친 중간 형태 |
| [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 엔진 | 진화 모델 / Hopper 이후 아키텍처에 적용된 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 특화 가속 기술 |
| [Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) | 평가 지표 / 단위 시간당 처리할 수 있는 연산의 총량 |

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수·기울기 계산] -> [텐서 코어 (Tensor Core)] -> [대규모 분산 학습·서빙 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 수학 숙제로 곱하기 문제를 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)0개 풀어야 하는데, 손으로 풀면 너무 오래 걸려요.
2. [텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)는 한 번 버튼만 누르면 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)문제를 동시에 풀어주는 '슈퍼 계산기'예요.
3. 이 계산기 덕분에 컴퓨터가 아주 어려운 문제도 눈 깜짝할 사이에 풀 수 있게 되었답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 406 / 420

<- **이전**: [405. 파이프라인 병렬화 (GPipe)](/studynote/10_ai/05_data_science_ml/405_gpipe_pipeline_parallelism/)
**다음**: [407. 코사인 어닐링 (Cosine Annealing Scheduler)](/studynote/10_ai/05_data_science_ml/407_cosine_annealing/) ->

---
