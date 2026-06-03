+++
title = "426. 시스톨릭 어레이 (Systolic Array)"
date = 2026-03-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 시스톨릭 어레이 (Systolic [Array](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/))는 다수의 PE (Processing Element)를 격자로 배치해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 메모리로 되돌아가지 않고 이웃 PE 사이를 박동처럼 흘러가며 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) ([Multiply-Accumulate](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/428_mac_operation/)) 연산을 누적하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)플로 하드웨어다.
> 2. **가치**: 핵심 이득은 연산 속도 자체보다 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재사용이다. 한 번 불러온 입력과 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 칩 내부에서 반복 재사용해 메모리 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 병목과 전력 소모를 크게 줄인다.
> 3. **판단 포인트**: 밀집 행렬·텐서 연산에는 매우 강하지만, 분기·불규칙 접근·높은 희소성처럼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름이 깨지는 작업에는 비효율적이므로 워크로드 적합성이 채택의 기준이다.

---

## Ⅰ. 개요 및 필요성

시스톨릭 어레이 (Systolic [Array](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/))는 동일한 연산을 반복하는 격자형 연산기 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 리듬 있게 흘려보내며 대규모 행렬 연산을 처리하는 구조다. 이름의 어원인 systolic은 심장이 수축하며 혈액을 밀어내는 움직임에서 왔고, 여기서는 클럭마다 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 한 칸씩 이동하는 규칙적인 파동을 뜻한다. 즉, 계산 자체보다 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 어떻게 움직일 것인가</strong>에 초점을 맞춘 아키텍처다.

이 구조가 필요해진 이유는 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 추론과 학습의 중심이 되는 행렬 곱셈, [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/), 어텐션 같은 연산이 대부분 거대한 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 반복이기 때문이다. 범용 CPU (Central Processing Unit)나 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) ([Graphics Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))는 연산기는 빠르지만, 필요한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 계속 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)·캐시·메모리에서 끌어오는 과정에서 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)과 전력의 벽을 만난다. 이른바 [메모리 월](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/433_memory_wall/) ([Memory Wall](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/433_memory_wall/))은 연산기를 놀게 만들고, 특히 전력 제약이 큰 모바일·엣지 환경에서는 더 치명적이다.

시스톨릭 어레이는 이 문제를 "계산하러 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 왔다 갔다 하지 말고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 흐르는 길 위에 연산기를 고정하자"는 발상으로 풀었다. 입력 행렬의 원소와 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)가 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)의 가장자리에서 들어오면, 내부 PE는 받은 값을 곱하고 부분합을 넘기면서 결과를 만든다. 따라서 외부 메모리 접근 횟수는 줄고, 칩 내부의 짧은 로컬 연결이 반복 사용되므로 전성비가 좋아진다.

- **📢 섹션 요약 비유**: 시스톨릭 어레이는 학생 100명이 각자 창고에 공책을 가지러 뛰는 방식이 아니라, 맨 앞 학생이 공책을 받아 옆 사람에게 차례로 넘기는 교실 릴레이다. 뛰는 거리가 줄어드니 수업도 빨라지고 힘도 덜 든다.

---

## Ⅱ. 아키텍처 및 핵심 원리

시스톨릭 어레이의 기본 단위는 PE다. 각 PE는 보통 곱셈기, 가산기, 누산 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/), 짧은 로컬 버퍼를 가지며, 매 클럭마다 입력값 일부를 받아 계산하고 다음 PE로 전달한다. 핵심은 모든 PE가 복잡한 명령 해석 없이 같은 템포로 움직인다는 점이며, 이 규칙성이 높은 집적도와 예측 가능한 지연시간을 만든다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| PE (Processing Element) | 곱셈·덧셈·누산 수행 | [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)(Int8, BF16 ([BFloat16](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/092_bfloat16/)) 등), 누산 폭 |
| 로컬 버퍼 / [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) | 직전 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 부분합 유지 | 외부 메모리 접근 최소화 |
| 인터커넥트 | 이웃 PE 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전달 | 짧은 배선, 규칙적 배치 |
| 컨트롤러 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 주입·배출 시점 제어 | [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 활용률, [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |

아래 그림은 "입력은 가로로, [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)는 세로로, 부분합은 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 안에서 축적된다"는 원리를 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4×4 시스톨릭 어레이의 파동형 데이터 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">좌측 입력 A(i,k) ▶</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">상단 입력 B(k,j) ▼</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PE00</div><div class="kb-diagram-cell">PE01</div><div class="kb-diagram-cell">PE02</div><div class="kb-diagram-cell">PE03</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PE10</div><div class="kb-diagram-cell">PE11</div><div class="kb-diagram-cell">PE12</div><div class="kb-diagram-cell">PE13</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PE20</div><div class="kb-diagram-cell">PE21</div><div class="kb-diagram-cell">PE22</div><div class="kb-diagram-cell">PE23</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PE30</div><div class="kb-diagram-cell">PE31</div><div class="kb-diagram-cell">PE32</div><div class="kb-diagram-cell">PE33</div><div class="kb-diagram-cell">▶ 출력 C</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">각 PE: A는 오른쪽, B는 아래쪽, 부분합은 로컬에 누적</div></div>
</div>
</div>



실제 행렬 곱셈에서는 A 행렬 원소가 오른쪽으로 이동하고, B 행렬 원소가 아래로 이동하면서, 각 교차점의 PE가 해당 곱을 부분합에 더한다. 클럭이 진행될수록 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 파면이 대각선으로 퍼지고, [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)이 가득 차면 거의 모든 PE가 매 사이클 유효한 MAC을 수행한다. 이 상태가 되면 처리량은 매우 높아지고, 메모리에서 같은 값을 다시 읽는 낭비가 줄어든다.

대표적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)플로로는 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 고정 ([Weight](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) Stationary), 출력 고정 (Output Stationary), 입력 고정 (Input Stationary)이 있다. 예를 들어 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 고정은 각 PE에 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 오래 머물게 해 추론처럼 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 재사용이 큰 작업에 유리하고, 출력 고정은 부분합을 오래 잡아 두어 누산 이동 비용을 줄이는 데 강하다. 결국 시스톨릭 어레이의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 크기만이 아니라 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 어디에 오래 붙잡아 둘지에 의해 달라진다.

- **📢 섹션 요약 비유**: 이 구조는 주방 조리대마다 같은 도구를 놓고 재료를 옆 칸으로 넘기는 분업 라인과 같다. 칼과 냄비를 매번 창고에서 찾지 않으니, 요리 속도는 사람 수보다 동선 설계에서 갈린다.

---

## Ⅲ. 비교 및 연결

시스톨릭 어레이를 제대로 이해하려면 범용 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 구조와의 차이를 봐야 한다. GPU의 [SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) (Single [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/), Multiple [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 또는 [SIMT](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/423_simt/) (Single [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/), Multiple Threads)는 많은 스레드를 동시에 돌리지만, 여전히 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)·[공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)·캐시 계층을 폭넓게 활용하며 비교적 유연한 제어를 허용한다. 반면 시스톨릭 어레이는 제어 유연성을 줄이고 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 경로를 거의 고정해, 특정 텐서 연산의 효율을 극단적으로 끌어올린다.

| 비교 항목 | [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) / 범용 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 프로세서 | 시스톨릭 어레이 |
| :--- | :--- | :--- |
| 주된 강점 | 다양한 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 실행 | 밀집 행렬·텐서 연산의 높은 전성비 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 | 메모리 계층을 폭넓게 활용 | 이웃 PE 중심의 국소 이동 |
| 제어 구조 | 비교적 유연한 스케줄링 | 정형화된 파이프라인 흐름 |
| 취약한 작업 | 작은 배치, 제어 분기 과다 | 희소성 높음, 불규칙 메모리 접근 |

연결 관점에서는 [TPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/425_tpu/) ([Tensor Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/425_tpu/)), [NPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) ([Neural Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/)), [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) ([Tensor Core](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/))가 모두 이 철학의 서로 다른 구현이라고 볼 수 있다. TPU는 대형 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)을 통해 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 추론·학습에 집중했고, 모바일 NPU는 작은 전력 예산 안에서 영상·음성 처리용 행렬 연산을 가속한다. GPU의 [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)는 범용 그래픽 프로세서 내부에 축소된 행렬 전용 유닛을 넣어, 유연성과 특화 효율 사이의 절충점을 만든 사례다.

또한 이 구조는 메모리 계층 설계와 떼어 놓고 볼 수 없다. [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)이 아무리 빨라도 온칩 [SRAM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/250_sram/) (Static Random Access Memory)에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 제때 공급하지 못하면 곧장 버블이 생기고 활용률이 떨어진다. 그래서 시스톨릭 어레이는 단순 연산기 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)이 아니라, 메모리 타일링·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재배치·양자화까지 함께 보는 시스템 설계 문제다.

- **📢 섹션 요약 비유**: GPU가 여러 종류의 손님을 빠르게 응대하는 대형 푸드코트라면, 시스톨릭 어레이는 햄버거만 초고속으로 만드는 전용 조리 라인이다. 메뉴가 딱 맞으면 압도적이지만, 주문이 제각각이면 오히려 답답해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 시스톨릭 어레이의 채택 여부는 "행렬 곱셈이 많다"만으로 결정되지 않는다. 첫째, 텐서 형상이 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 크기와 잘 맞아야 한다. 예를 들어 128×128 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)을 가진 가속기에 작은 73×73 타일을 계속 넣으면 많은 PE가 놀게 되어 이론 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실제 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이가 커진다. 그래서 프레임워크 수준에서 [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/), 타일링, 연산 재배치를 통해 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 점유율을 높여야 한다.

둘째, [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)와 메모리 용량을 함께 봐야 한다. Int8이나 BF16처럼 낮은 비트폭은 더 많은 PE [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화와 낮은 전력에 유리하지만, 정확도 저하를 감당할 수 있는 모델이어야 한다. 또한 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)와 활성값을 온칩 버퍼에 얼마나 오래 머물게 할 수 있는지가 재사용률을 좌우하므로, 연산량만 보지 말고 [SRAM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/250_sram/) 용량과 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)까지 함께 산정해야 한다.

셋째, 워크로드 특성을 구분해야 한다. 대규모 Dense GEMM (Dense General Matrix Multiply), [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/), 고정 길이 추론은 적합하지만, 희소 행렬, [그래프 신경망](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/306_graph_neural_network_gnn/), 복잡한 분기 기반 후처리는 종종 CPU나 GPU가 더 낫다. 즉 "AI니까 무조건 [NPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/)"가 아니라, 규칙적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)플로가 유지되는 구간만 가속기로 오프로딩하는 이기종 분할이 현실적이다.

### 실무 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 핵심 연산이 밀집 텐서 곱셈 위주인가?
2. 입력 형상과 배치 크기를 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 친화적으로 고정·[패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)할 수 있는가?
3. [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)·활성값을 온칩 버퍼에 충분히 재사용할 수 있는가?
4. 분기·희소성 때문에 파이프라인 버블이 자주 생기지 않는가?

### 대표 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 희소도가 높은 모델을 아무 전처리 없이 그대로 올려 0 연산을 양산하는 경우
- 작은 배치를 계속 넣어 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 활용률이 낮아지는 경우
- 후처리 분기 로직까지 같은 가속기에서 해결하려다 CPU 폴백이 빈번해지는 경우

- **📢 섹션 요약 비유**: 시스톨릭 어레이는 큰 화물을 규칙적으로 싣는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 선박과 같다. 상자가 규격에 맞고 물량이 많으면 최고의 효율을 내지만, 짐 크기가 제각각이거나 중간에 자꾸 내려야 하면 오히려 작은 트럭이 더 낫다.

---

## Ⅴ. 기대효과 및 결론

시스톨릭 어레이의 가장 큰 효과는 메모리 접근을 줄여 연산 밀도와 전성비를 동시에 끌어올린다는 점이다. 같은 전력 예산에서도 더 많은 MAC을 수행할 수 있고, 규칙적인 배치 덕분에 칩 구현과 검증도 상대적으로 단순해진다. 이 때문에 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)용 [TPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/425_tpu/), 모바일 [NPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/), 일부 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 텐서 가속 블록이 모두 이 철학을 채택하고 있다.

다만 만능 해법은 아니다. [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)이 커질수록 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 채워 넣는 전처리, 온칩 버퍼 설계, 칩 간 통신 비용이 다시 병목으로 떠오른다. 특히 초거대 모델에서는 단일 어레이 내부 효율보다 여러 어레이와 메모리 스택을 어떻게 연결할지가 더 중요한 문제가 된다.

앞으로의 방향은 세 가지로 요약할 수 있다. 첫째, 저정밀도 연산과 양자화를 더 깊게 결합해 같은 면적에서 더 높은 처리량을 얻는 방향이다. 둘째, 3D 적층 메모리와 결합해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공급 거리를 줄이는 방향이다. 셋째, [PIM](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/430_pim/) ([Processing-In-Memory](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/430_pim/))처럼 메모리 자체에 연산을 녹여 시스톨릭 철학을 더 안쪽으로 밀어 넣는 방향이다. 따라서 이 개념은 "행렬 곱셈기"가 아니라 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동을 연산 구조에 맞게 재설계한 가속 철학"으로 기억하는 것이 맞다.

- **📢 섹션 요약 비유**: 좋은 시스톨릭 어레이는 엔진 마력만 키운 자동차가 아니라, 도로·변속기·연료 흐름까지 함께 맞춘 경주차다. 진짜 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 큰 엔진보다 끊기지 않는 흐름에서 나온다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| PE (Processing Element) | 시스톨릭 어레이의 최소 연산 단위로, 곱셈·누산과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전달을 담당 |
| [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) ([Multiply-Accumulate](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/428_mac_operation/)) | 행렬 곱셈과 [합성곱](/knowledge-base/studynote/10_ai/03_llm_nlp/228_cnn_1d_2d_3d_video_medical/)의 기본 연산이며, [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)의 거의 모든 PE가 반복 수행 |
| [메모리 월](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/433_memory_wall/) ([Memory Wall](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/433_memory_wall/)) | 시스톨릭 어레이가 등장한 직접 배경으로, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 비용이 연산 비용을 압도하는 현상 |
| [Weight](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) Stationary | [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 PE 내부에 오래 유지해 재사용률을 높이는 대표 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)플로 |
| [TPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/425_tpu/) ([Tensor Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/425_tpu/)) / [NPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) ([Neural Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/)) | 시스톨릭 어레이를 상용 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 가속기로 구현한 대표 사례 |
| [PIM](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/430_pim/) ([Processing-In-Memory](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/430_pim/)) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동을 더 줄이기 위해 메모리와 연산을 더욱 밀착시키는 확장 방향 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">벡터 프로세서 · 배열 프로세서</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">메모리 월 (Memory Wall) · 데이터 재사용 요구</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">시스톨릭 어레이 (Systolic Array)</div>
<div class="kb-diagram-tree-item" style="--depth:6">▶ Weight Stationary / Output Stationary / Input Stationary</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">TPU (Tensor Processing Unit) · NPU (Neural Processing Unit) · Tensor Core</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">저정밀도 양자화 · 3D 적층 메모리 · PIM (Processing-In-Memory)</div>
</div>
</div>



이 흐름도는 "[배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)형 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리의 계보"가 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시대의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 최적화 문제와 만나, 전용 가속기와 메모리 결합 구조로 확장되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 시스톨릭 어레이는 친구들이 네모 줄을 서서 물건을 옆 사람에게 계속 넘겨 주는 릴레이 놀이와 같아요.
2. 필요한 물건을 매번 창고까지 뛰어가서 가져오지 않으니까 시간도 아끼고 힘도 덜 들어요.
3. 하지만 네모 줄에 딱 맞는 물건일 때 가장 잘하고, 모양이 제멋대로면 다른 도구가 더 잘할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 427 / 803

← **이전**: [425. TPU (Tensor Processing Unit)](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/425_tpu/)
**다음**: [427. 텐서 코어 (Tensor Core)](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) →

---
