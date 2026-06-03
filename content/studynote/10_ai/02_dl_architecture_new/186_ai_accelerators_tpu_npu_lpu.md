---
title: 186. AI 반도체 엑셀러레이터 (TPU, NPU, LPU)
date: '2026-04-17'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[190_ai_llm_requirements_specification|AI]] [[009_semiconductor|반도체]] 엑셀러레이터는 [[425_tpu|TPU]] ([[425_tpu|Tensor Processing Unit]]), [[424_npu|NPU]] ([[424_npu|Neural Processing Unit]]), [[438_lpu|LPU]] ([[317_lpu_language_processing_unit|Language Processing Unit]])처럼 **행렬 곱셈과 추론 [[001_dikw_pyramid|데이터]] 흐름**에 맞춰 회로를 재배치한 [[070_asic|주문형 반도체]]([[070_asic|ASIC]], Application-Specific Integrated Circuit)다.
> 2. **가치**: [[282_performance_tactics|성능]]의 핵심 병목이 계산기 수보다 메모리 이동량에 있다는 점을 겨냥해, [[418_gpu|GPU]] ([[418_gpu|Graphics Processing Unit]]) 대비 더 높은 전성비와 더 낮은 [[015_지연_데이터_관점|지연]]시간을 만든다.
> 3. **판단 포인트**: 훈련용인지 추론용인지, 모델 구조가 규칙적인지, 컴파일러·프레임워크 생태계가 충분한지에 따라 [[425_tpu|TPU]]·[[424_npu|NPU]]·LPU의 채택 결과가 크게 달라진다.

---

## Ⅰ. 개요 및 필요성

[[190_ai_llm_requirements_specification|AI]] [[009_semiconductor|반도체]] 엑셀러레이터는 딥러닝 연산을 범용 CPU (Central Processing Unit)나 범용 [[418_gpu|GPU]] 위에서 억지로 수행하지 않고, 신경망이 반복하는 핵심 작업만 회로 수준에서 가속하는 특수 프로세서다. 딥러닝의 대부분은 곱셈-누산([[673_mac_message_authentication_code|MAC]], [[428_mac_operation|Multiply-Accumulate]])과 텐서 이동으로 구성되므로, 범용 명령 해석과 복잡한 제어 회로보다 **규칙적인 [[430_index_fast_full_scan|병렬]] 연산과 메모리 근접성**이 더 중요하다.

[[459_quic_fec_forward_error_correction|초기]]에는 CPU가 모델 학습과 추론을 모두 맡았지만, 코어 수가 적고 [[430_index_fast_full_scan|병렬]] [[001_dikw_pyramid|데이터]] 흐름이 약해 대규모 행렬 연산에서 한계가 분명했다. 이후 GPU가 대규모 [[430_index_fast_full_scan|병렬]] 연산으로 딥러닝 붐을 열었지만, 그래픽 [[123_pipe|파이프]]라인 유산과 높은 [[466_power_consumption|전력 소모]], 메모리 이동 비용 때문에 [[190_ai_llm_requirements_specification|AI]] 전용 칩의 필요성이 커졌다. 결국 [[190_ai_llm_requirements_specification|AI]] 인프라는 “더 많은 연산기” 경쟁에서 “[[001_dikw_pyramid|데이터]]를 얼마나 덜 움직이게 설계했는가” 경쟁으로 넘어왔다.

TPU는 대규모 클라우드 훈련과 서빙을 겨냥했고, NPU는 모바일·엣지 장치의 저전력 추론에 최적화됐으며, LPU는 [[582_llm_based_code_generation_tools|대규모 언어 모델]] 토큰 [[087_process_state_transition|생성]] [[015_지연_데이터_관점|지연]]을 줄이는 방향으로 등장했다. 즉 이름은 달라도 공통 질문은 같다. **모델의 계산 패턴을 가장 잘 흘려보낼 수 있는 하드웨어 배관이 무엇인가**가 핵심이다.

- **📢 섹션 요약 비유**: 범용 칩이 만능 공구 세트라면, [[190_ai_llm_requirements_specification|AI]] 엑셀러레이터는 “나사만 하루 종일 조이는 공장”에 맞춰 전동드라이버를 벽면에 고정 설치한 것과 같다. 다른 일은 못 하지만, 그 일 하나는 훨씬 빠르고 전기도 덜 먹는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[190_ai_llm_requirements_specification|AI]] 엑셀러레이터의 설계 포인트는 단순하다. 외부 메모리에서 [[001_dikw_pyramid|데이터]]를 자주 왕복하면 연산기가 놀게 되므로, 연산기 주변에 큰 온칩 버퍼를 두고 [[001_dikw_pyramid|데이터]]가 칩 내부를 한 번 흐를 때 최대한 많은 연산을 끝내야 한다. 이 때문에 TPU는 [[426_systolic_array|시스톨릭 어레이]]([[426_systolic_array|Systolic Array]]), 모바일 NPU는 저정밀 정수 연산기와 로컬 버퍼, LPU는 대규모 [[250_sram|SRAM]] (Static Random Access Memory) 중심 [[123_pipe|파이프]]라인을 강조한다.

아래 그림은 엑셀러레이터가 [[282_performance_tactics|성능]]을 내는 지점을 보여준다. 핵심은 “연산기 개수”보다 “[[495_hbm|HBM]] ([[495_hbm|High Bandwidth Memory]])·LPDDR에서 가져온 [[001_dikw_pyramid|데이터]]를 칩 안에서 얼마나 오래 재사용하느냐”다.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                AI 엑셀러레이터의 공통 데이터 경로: 메모리 이동 최소화       │
├──────────────────────────────────────────────────────────────────────────────┤
│ Host CPU        Compiler/XLA         Global Memory         On-Chip Fabric   │
│    │                 │               (HBM/LPDDR)                │           │
│    ▼                 ▼                    │                      ▼           │
│ [작업 배치] ──▶ [그래프 최적화] ──▶ [타일 적재] ──▶ [SRAM Scratchpad]       │
│                                                                  │           │
│                                                                  ▼           │
│                                                        [MAC Array / Tensor]  │
│                                                                  │           │
│                 TPU  : 시스톨릭 어레이로 행렬 파동 처리          │           │
│                 NPU  : INT8/INT4 중심 저전력 추론 파이프라인      │           │
│                 LPU  : 토큰 생성용 고정 지연 파이프라인            │           │
│                                                                  ▼           │
│                                                     [Activation / Output]    │
└──────────────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| [[426_systolic_array|시스톨릭 어레이]] ([[426_systolic_array|Systolic Array]]) | [[001_dikw_pyramid|데이터]]가 격자 형태 연산기를 통과하며 누산 | 대형 행렬에 강함, 규칙적 텐서 필요 |
| 온칩 [[250_sram|SRAM]] 버퍼 | 중간 결과 재사용, 외부 메모리 왕복 감소 | [[140_bandwidth|대역폭]] 확보, 용량 한계 관리 |
| 저정밀 연산기 | INT8·BF16·FP16 등 낮은 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 처리 | 정확도 손실과 [[282_performance_tactics|성능]] 이득의 균형 |
| 컴파일러 [[057_stack|스택]] | [[070_graph_datastructure|그래프]] 분할, 연산 융합, 메모리 배치 | XLA, TensorRT, Neuron 같은 생태계 중요 |
| 인터커넥트 | 다수 칩 묶음 학습·서빙 | [[198_pod_kubernetes_minimum_deployment_unit|Pod]], [[389_mesh_topology|Mesh]], [[367_noc|NoC]]([[367_noc|Network on Chip]]) 효율 |

TPU의 대표 특징은 행렬이 어레이 내부를 파도처럼 통과하며 중간 결과를 메모리로 되돌리지 않는 점이다. NPU는 모바일 배터리와 열 설계를 고려해 INT8·INT4 추론, 영상 [[130_signal|신호]] 처리, 카메라 [[123_pipe|파이프]]라인과의 결합을 강화한다. LPU는 거대 언어 모델 추론에서 토큰 1개 [[087_process_state_transition|생성]]마다 발생하는 메모리 [[015_지연_데이터_관점|지연]]을 줄이기 위해 고정된 실행 경로와 예측 가능한 [[015_지연_데이터_관점|지연]]시간을 강하게 추구한다.

- **📢 섹션 요약 비유**: 일반 서버가 창고에서 부품을 계속 들고 오는 작업장이라면, [[190_ai_llm_requirements_specification|AI]] 엑셀러레이터는 필요한 부품을 컨베이어 옆에 미리 쌓아두고 조립자가 손만 뻗으면 바로 이어서 작업하는 생산 라인이다.

---

## Ⅲ. 비교 및 연결

[[425_tpu|TPU]]·[[424_npu|NPU]]·LPU는 모두 AI용이지만, 겨냥하는 병목이 서로 다르다. TPU는 대규모 훈련과 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 추론, NPU는 모바일·엣지 추론, LPU는 대형 언어 모델의 토큰 [[087_process_state_transition|생성]] [[015_지연_데이터_관점|지연]] 단축에 초점이 있다. 따라서 “[[190_ai_llm_requirements_specification|AI]] 칩”이라는 공통 이름만 보고 동일하게 비교하면 설계 의도를 놓친다.

| 구분 | [[425_tpu|TPU]] | [[424_npu|NPU]] | [[438_lpu|LPU]] | [[418_gpu|GPU]] |
| :--- | :--- | :--- | :--- | :--- |
| 주 무대 | 클라우드 훈련·대규모 서빙 | 모바일·엣지·자동차 | [[263_llm_large_language_model|LLM]] 추론 서버 | 범용 훈련·추론 |
| 핵심 강점 | 대형 행렬 처리와 [[136_variance|분산]] 묶음 | 저전력·저발열 | 토큰 [[015_지연_데이터_관점|지연]] 최소화 | 범용성·생태계 성숙 |
| 주 메모리 [[268_strategy_pattern|전략]] | [[495_hbm|HBM]] + 대형 [[055_array|배열]] | 로컬 버퍼 + LPDDR | 대규모 [[250_sram|SRAM]] 중심 | [[495_hbm|HBM]] 활용, 범용 캐시 |
| 적합 모델 | [[246_transformer_self_attention_parallel_positional_encoding|Transformer]], [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] 대형 배치 | 비전·음성·온디바이스 모델 | [[039_decoder|Decoder]] 기반 [[263_llm_large_language_model|LLM]] | 거의 모든 딥러닝 모델 |
| 약점 | 전용 컴파일러 의존 | 모델 크기 제한 | 범용성 부족 | 전력·비용 부담 |

이 차이는 [[348_mlops|MLOps]] 설계와도 연결된다. 훈련 단계에서는 GPU나 TPU가 유리하고, 서빙 단계에서는 [[434_quantization|양자화]]([[434_quantization|Quantization]])된 NPU나 [[015_지연_데이터_관점|지연]] 특화 LPU가 더 경제적일 수 있다. 결국 [[190_ai_llm_requirements_specification|AI]] 하드웨어 선택은 칩 자체의 FLOPS보다 **모델 구조, 배치 크기, [[015_지연_데이터_관점|지연]] 요구, 소프트웨어 이식성**을 함께 보는 문제다.

- **📢 섹션 요약 비유**: 대형 화물열차([[425_tpu|TPU]]), 전기 스쿠터([[424_npu|NPU]]), 특급 오토바이 퀵서비스([[438_lpu|LPU]]), 다목적 트럭([[418_gpu|GPU]])은 모두 짐을 옮기지만, 싣는 짐과 가야 할 길이 다르기 때문에 최고 속도보다 “어떤 길에 올릴 것인가”가 더 중요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 “가장 빠른 칩”보다 “내 모델을 안정적으로 태울 수 있는 칩”을 골라야 한다. 첫째, 프레임워크와 컴파일러 성숙도를 [[396_validation|확인]]해야 한다. PyTorch 모델이 있다고 해서 모든 [[425_tpu|TPU]]·NPU에서 바로 돌아가는 것은 아니며, 동적 shape가 많은 모델은 전용 컴파일러 최적화가 깨질 수 있다. 둘째, 훈련과 추론을 분리해야 한다. 수천억 파라미터 모델 훈련과 모바일 추론을 같은 하드웨어에 묶으면 비용 구조가 급격히 나빠진다.

### 채택 [[435_checklist_based_testing|체크리스트]]

1. 모델이 Transformer처럼 큰 행렬 연산 중심인가, 아니면 제어 흐름이 복잡한가?
2. [[015_지연_데이터_관점|지연]]시간이 중요한가, [[228_batch_processing_hadoop_spark|배치 처리]]량이 중요한가?
3. BF16·FP16·INT8 같은 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 축소를 허용할 수 있는가?
4. 전용 SDK와 드라이버, [[229_monitor|모니터]]링 도구가 운영팀 역량 안에 들어오는가?
5. [[051_vendor_lock_in_cloud_computing|벤더 종속]]([[362_lock_in_portability|Lock-in]]) 비용보다 [[282_performance_tactics|성능]]·전력 절감 효과가 큰가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 불규칙한 [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] ([[244_rnn_time_series_lstm_cell_gate_long_term_dependency|Recurrent Neural Network]]) 계열이나 사용자 정의 연산이 많은 모델을 전용 가속기에 무리하게 태우는 경우
- 훈련용 고가 칩을 그대로 온라인 추론에 사용해 비용과 전력을 동시에 악화시키는 경우
- 하드웨어 스펙만 보고 컴파일러, 디버깅, [[613_profiling_gprof|프로파일링]] 도구의 미성숙을 무시하는 경우

기술사 답안에서는 “[[425_tpu|TPU]]/[[424_npu|NPU]]/LPU는 모두 [[418_gpu|GPU]] 대체재”라고 [[289_cqrs_db|쓰기]]보다, **훈련 vs 추론, 클라우드 vs 엣지, [[139_throughput|처리량]] vs [[015_지연_데이터_관점|지연]]시간**으로 판단 축을 나눠 쓰는 편이 설득력이 높다. 하드웨어-소프트웨어 공동 설계(Hw/SW Co-design)가 성패를 좌우한다는 점도 반드시 함께 언급하는 것이 좋다.

- **📢 섹션 요약 비유**: [[148_5g_embb_urllc_mmtc|초고속]] 열차를 사는 것보다 먼저 봐야 할 것은 우리 동네에 그 열차가 달릴 선로가 있는지다. 칩 [[282_performance_tactics|성능]]보다 소프트웨어 선로와 운영 역량이 더 먼저다.

---

## Ⅴ. 기대효과 및 결론

[[190_ai_llm_requirements_specification|AI]] 엑셀러레이터의 가장 큰 효과는 같은 모델을 더 낮은 전력과 더 짧은 시간 안에 학습·서빙할 수 있다는 점이다. 이는 단순한 비용 절감이 아니라, 더 큰 모델 실험, 더 빠른 배포, 온디바이스 [[190_ai_llm_requirements_specification|AI]] 확대 같은 [[268_strategy_pattern|전략]]적 선택지를 열어 준다. 특히 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 전력과 냉각이 병목이 되는 시점에는 칩의 전성비가 곧 [[090_service_kubernetes_network_load_balancing|서비스]] 경쟁력으로 이어진다.

그러나 만능 해법은 아니다. 전용 칩일수록 소프트웨어 [[344_compatibility_usability|호환성]]과 벤더 의존성이 커지고, 모델 구조 변화에 덜 유연할 수 있다. 따라서 [[190_ai_llm_requirements_specification|AI]] [[009_semiconductor|반도체]]는 “GPU를 완전히 대체하는 존재”가 아니라, **특정 병목을 극적으로 줄이기 위해 [[418_gpu|GPU]] 생태계를 보완·분화시키는 흐름**으로 기억하는 편이 정확하다.

- **📢 섹션 요약 비유**: 맞춤형 경주화는 트랙에서는 압도적이지만, 등산길과 눈길까지 책임지지는 못한다. [[190_ai_llm_requirements_specification|AI]] 엑셀러레이터도 가장 잘 맞는 경기장에서 쓸 때 진짜 가치가 나온다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[427_tensor_core|텐서 코어]] ([[427_tensor_core|Tensor Core]]) | GPU가 [[190_ai_llm_requirements_specification|AI]] 전용 연산기로 진화한 출발점 |
| [[426_systolic_array|시스톨릭 어레이]] ([[426_systolic_array|Systolic Array]]) | [[425_tpu|TPU]] 계열의 대표적 [[001_dikw_pyramid|데이터]]흐름 아키텍처 |
| [[434_quantization|양자화]] ([[434_quantization|Quantization]]) | [[424_npu|NPU]]·LPU에서 전성비를 높이는 핵심 기법 |
| [[495_hbm|HBM]] ([[495_hbm|High Bandwidth Memory]]) | 대규모 훈련 칩의 외부 메모리 병목 축 |
| [[250_sram|SRAM]] (Static Random Access Memory) | 추론 [[015_지연_데이터_관점|지연]]을 줄이는 온칩 메모리 축 |
| XLA (Accelerated Linear Algebra) | [[425_tpu|TPU]] 계열 최적화에서 중요한 컴파일러 층 |
| [[348_mlops|MLOps]] ([[220_mlops_machine_learning_operations|Machine Learning Operations]]) | 훈련/서빙 하드웨어 분리 [[268_strategy_pattern|전략]]과 직접 연결 |

### 📈 관련 키워드 및 발전 흐름도

```text
CPU 기반 학습
    │
    ▼
GPU 병렬 연산 · 텐서 코어
    │
    ▼
TPU 시스톨릭 어레이 · 대규모 분산 학습
    │
    ├──────────────▶ NPU 온디바이스 저전력 추론
    │
    └──────────────▶ LPU 초저지연 LLM 토큰 생성
                           │
                           ▼
                Hw/SW Co-design · 전용 추론 인프라
```

이 흐름은 “범용 [[430_index_fast_full_scan|병렬]]화 → [[001_dikw_pyramid|데이터]]흐름 특화 → 사용처별 세분화”로 [[190_ai_llm_requirements_specification|AI]] 하드웨어가 분화되는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 보통 컴퓨터 칩은 이것저것 다 잘하는 만능 선수인데, [[231_ai_turing_test|인공지능]]은 같은 계산을 너무 많이 해서 더 전문 선수가 필요했어요.
2. [[425_tpu|TPU]], [[424_npu|NPU]], LPU는 [[231_ai_turing_test|인공지능]] 계산만 엄청 빨리 하도록 만든 전용 운동선수예요.
3. 그래서 어디서 뛸지에 따라 선수도 달라져요. 큰 경기장에서는 [[425_tpu|TPU]], 휴대폰 안에서는 [[424_npu|NPU]], 말 빨리하기 경기는 LPU가 더 잘 맞아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 186 / 420

← **이전**: [[185_tensor_core_gpu|185. GPU 아키텍처 기반 텐서 코어 (Tensor Core GPU Architecture)]]
**다음**: [[187_mixed_precision_training|187. 혼합 정밀도 훈련 (Mixed Precision Training)]] →

---
