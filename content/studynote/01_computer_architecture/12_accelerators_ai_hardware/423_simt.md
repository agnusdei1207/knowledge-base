---
title: "SIMT (Single Instruction Multiple Threads)"
date: "2026-03-20"
tags:
  - "studynote-computer-architecture"
weight: 423
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SIMT (Single [Instruction](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Multiple Threads)는 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) ([Graphics Processing Unit](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))가 수많은 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 개별 CPU처럼 독립 제어하지 않고, 워프 (Warp) 단위로 같은 명령 흐름에 묶어 높은 처리량을 얻는 실행 모델이다.
> 2. **가치**: [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)마다 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)와 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) ID는 독립적으로 유지하면서도 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 발행은 공유하므로, 범용 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 프로그래밍의 편의성과 [SIMD](/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) (Single [Instruction](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Multiple [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))급 대량 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성을 절충할 수 있다.
> 3. **판단 포인트**: SIMT의 성패는 코어 개수보다 워프 분기 발산 (Warp Divergence), 메모리 코얼레싱 (Memory Coalescing), 점유율 (Occupancy)을 얼마나 잘 통제하느냐에 달려 있다.

---

## Ⅰ. 개요 및 필요성

SIMT (Single [Instruction](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Multiple Threads)는 여러 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 같은 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 공유해 실행하되, 각 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 자기 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 상태를 유지하도록 만든 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 중심 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 실행 방식이다. 전통적인 CPU (Central Processing Unit)는 코어마다 복잡한 제어부를 두고 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 하나하나를 무겁게 관리하지만, 이 방식으로는 수천 개 실행 흐름을 같은 칩에 올리는 데 면적과 전력이 너무 많이 든다. 반대로 순수 SIMD는 명령 효율은 높지만, 프로그래머가 벡터 길이와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 배치를 직접 의식해야 하므로 범용 코드 작성이 어렵다.

GPU가 과학 계산과 [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 연산에 쓰이기 시작하면서, 하드웨어는 "벡터처럼 빠르되 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)처럼 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 쉬운 모델"을 필요로 했다. SIMT는 이 요구를 받아들여 프로그래머에게는 수많은 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 제공하고, 하드웨어 내부에서는 이를 워프 단위로 묶어 같은 명령을 실행하게 한다. 덕분에 `threadIdx` 같은 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 기반 코드로도 대규모 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리가 가능해졌고, 범용 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 컴퓨팅 ([GPGPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/419_gpgpu/), General-Purpose computing on [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))의 문턱이 크게 낮아졌다.

이 그림은 왜 SIMT가 CPU식 독립 제어와 SIMD식 일괄 처리의 중간 해법으로 등장했는지 보여준다.

```text
+--------------------------------------------------------------+
|            병렬 실행 모델의 현실적 절충: 왜 SIMT인가         |
+-----------------------+----------------+---------------------+
| CPU식 스레드          | SIMD           | SIMT                |
| - 제어 유연성 높음    | - 명령 효율 높음| - 스레드 추상화 제공 |
| - 제어부 비용 큼      | - 분기 대응 약함| - 워프 단위 실행     |
| - 대량 병렬 비효율    | - 프로그래밍 경직| - 대량 병렬+유연성 절충|
+-----------------------+----------------+---------------------+
```

핵심은 SIMT가 "모든 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 완전히 독립적"인 구조가 아니라, "독립 상태를 가진 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 하드웨어가 묶어서 실행"하는 구조라는 점이다. 따라서 이 모델은 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수가 많을수록 무조건 유리한 것이 아니라, 워프 내부 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)들이 얼마나 비슷한 흐름으로 움직이는지에 따라 효율이 크게 달라진다.

- **📢 섹션 요약 비유**: SIMT는 같은 교과서를 쓰는 32명의 학생을 한 반으로 묶어 수업하는 방식과 같다. 학생마다 공책은 따로 있지만, 선생님은 한 번에 한 문제만 칠판에 적기 때문에 모두가 비슷한 진도로 따라올 때 가장 효율적이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SIMT의 실행 최소 단위는 보통 32개 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)로 구성된 워프다. 워프 안의 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)들은 각자 프로그램 값, [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 값, [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) ID를 바탕으로 서로 다른 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다룰 수 있지만, [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 발행 관점에서는 같은 [프로그램 카운터](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) (Program [Counter](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/), [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)) 흐름에 묶여 있다. 즉 "명령은 함께, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 각자"가 SIMT의 핵심 원리다.

| 구성 요소 | 역할 | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 미치는 영향 |
| :-- | :-- | :-- |
| 워프 (Warp) | 하드웨어가 한 번에 스케줄링하는 실행 묶음 | 분기 발산, 메모리 접근 효율 결정 |
| [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) ID ([Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) ID) | 각 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 맡을 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위치 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | 동일 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 가능 |
| [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) ([Register](/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)) | [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)별 사적 상태 저장 | 독립 연산 상태 유지, 과다 사용 시 점유율 저하 |
| [액티브](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) 마스크 ([Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) Mask) | 현재 명령에 참여하는 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 표시 | 분기 처리 시 일부 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)만 활성화 |
| 워프 [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) (Warp Scheduler) | 준비된 워프를 골라 실행 | 메모리 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 은닉에 직접 기여 |

이 그림은 SIMT가 한 명령을 여러 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)에 적용하면서도, 분기가 생기면 [액티브](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) 마스크로 참여 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 바꿔 가며 실행하는 구조를 보여준다.

```text
+--------------------------------------------------------------+
|                 SIMT 워프 실행의 내부 구조                   |
+--------------------------------------------------------------+
| Warp 0                                                      |
|  +- Thread 0 : Register set 0 -+                            |
|  +- Thread 1 : Register set 1 -+--> 같은 명령 발행 --> 산술논리장치군 |
|  +- ...                        -+                            |
|  +- Thread 31: Register set31 -+                            |
|               ^                                              |
|               +- Active Mask : 실행 참여 스레드 선택         |
+--------------------------------------------------------------+
| 원칙: 명령 흐름은 공유하지만 데이터와 상태는 스레드별 독립   |
+--------------------------------------------------------------+
```

문제가 되는 지점은 조건 분기다. 예를 들어 워프 안 32개 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 중 절반만 `if`를 타고 나머지는 `else`를 타면, 하드웨어는 두 경로를 동시에 실행하지 못하고 한쪽 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)만 활성화한 뒤 순차적으로 처리한다. 이 현상이 워프 분기 발산이며, 이때 같은 워프 내부 연산기는 일부만 일하게 되어 처리량이 떨어진다. 반대로 워프가 서로 다른 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽더라도 주소가 연속적이면 메모리 코얼레싱이 잘 일어나 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 효율이 높아진다.

또한 SIMT는 메모리 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 "없애는" 대신 "숨긴다". 어떤 워프가 글로벌 메모리 접근 때문에 수백 사이클 동안 대기하면, 워프 [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 같은 [스트리밍 멀티프로세서](/studynote/01_computer_architecture/12_accelerators_ai_hardware/421_streaming_multiprocessor/) ([Streaming Multiprocessor](/studynote/01_computer_architecture/12_accelerators_ai_hardware/421_streaming_multiprocessor/), [SM](/studynote/01_computer_architecture/12_accelerators_ai_hardware/421_streaming_multiprocessor/)) 안의 다른 준비된 워프로 즉시 전환한다. 따라서 좋은 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 한 워프의 절대 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간보다, 동시에 충분한 워프를 유지해 연산기를 쉬지 않게 만드는 점유율 설계가 중요하다.

- **📢 섹션 요약 비유**: SIMT 워프는 한 방송국의 합창단과 같다. 악보는 한 장을 같이 보지만, 각자 자기 목소리로 노래한다. 다만 절반은 1절, 절반은 2절을 동시에 부르겠다고 하면 지휘자는 결국 한쪽씩 따로 시켜야 한다.

---

## Ⅲ. 비교 및 연결

SIMT를 정확히 이해하려면 SIMD와 [MIMD](/studynote/01_computer_architecture/10_parallel_processing_architecture/372_mimd/) (Multiple [Instruction](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Multiple [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 함께 봐야 한다. SIMD는 하나의 명령을 여러 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 적용한다는 점에서 SIMT와 닮았지만, 프로그래밍 모델이 벡터 중심이라 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)별 제어 흐름을 직접 드러내기 어렵다. MIMD는 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)마다 명령 흐름이 독립적이라 유연하지만, 제어 비용과 전력 소모가 커서 초대규모 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)에 불리하다. SIMT는 이 둘 사이에서 "프로그래밍은 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)처럼, 실행은 벡터처럼"이라는 절충을 취한다.

| 비교 축 | [SIMD](/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) | SIMT | [MIMD](/studynote/01_computer_architecture/10_parallel_processing_architecture/372_mimd/) |
| :-- | :-- | :-- | :-- |
| 제어 흐름 | 하나의 벡터 명령 흐름 | 워프 단위 공유 흐름 | [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)별 독립 흐름 |
| 프로그래밍 관점 | 벡터 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 중심 | [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)/[커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 중심 | [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)/코어 중심 |
| 분기 대응 | 매우 약함 | 가능하나 발산 비용 존재 | 상대적으로 강함 |
| 하드웨어 효율 | 높음 | 높음 | 낮아질 수 있음 |
| 대표 환경 | CPU 벡터 명령 | [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) [CUDA](/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/)/OpenCL [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) | 멀티코어 CPU |

이 차이는 다른 컴퓨터구조 개념과도 직접 연결된다. 워프 발산은 제어 흐름 병목을 설명하고, 메모리 코얼레싱은 메모리 계층과 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 활용 문제를 설명한다. 점유율은 단순한 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 개수가 아니라 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 사용량, [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/) ([Shared Memory](/studynote/02_operating_system/02_process_thread/118_shared_memory/)) 사용량, 블록 크기와 연결된다. 또한 최신 GPU의 독립 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 스케줄링 (Independent [Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) Scheduling)은 전통적 SIMT의 경직성을 완화하려는 진화로 볼 수 있다.

즉 SIMT는 하나의 고정된 기술 용어가 아니라, [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 아키텍처가 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성을 다루는 기본 철학이다. 그래서 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 분석을 할 때도 "코어가 많다"보다 "워프가 얼마나 정렬되어 움직이는가"를 보는 것이 더 실질적이다.

- **📢 섹션 요약 비유**: SIMD는 같은 모양의 쿠키를 한 번에 찍는 틀이고, MIMD는 셰프마다 다른 요리를 하는 주방이다. SIMT는 같은 레시피로 여러 접시를 만들되, 각 접시에 올리는 재료 양은 손님별로 조금씩 다른 뷔페 라인에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 SIMT 최적화는 "[스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 많이 띄우는 것"이 아니라 "워프가 하드웨어 친화적으로 움직이게 만드는 것"이다. 예를 들어 이미지 처리, 벡터 합, 행렬 연산처럼 인접 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 같은 연산을 반복하는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 SIMT와 잘 맞는다. 반면 트리 탐색, [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)별 분기 깊이가 큰 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 워프 내부 흐름이 쉽게 갈라져 효율이 급격히 떨어질 수 있다.

### 실무 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 워프 내부 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)들이 비슷한 분기 경로를 타도록 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 정렬했는가?
2. 메모리 접근 주소가 연속적이어서 코얼레싱이 잘 일어나는가?
3. 블록 크기가 워프 배수이며, [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)·[공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/) 사용량 때문에 점유율이 무너지지 않는가?
4. 짧은 분기는 프레디케이션 (Predication)이나 수식 변환으로 평탄화할 수 있는가?
5. 프로파일러에서 Branch Efficiency, Occupancy, Memory [Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 중 실제 병목이 무엇인지 확인했는가?

### 채택/회피 기준

- **채택이 유리한 경우**: 동일한 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 대량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 반복 적용하고, 제어 흐름이 단순하며, 메모리 접근을 선형화할 수 있는 경우
- **회피 또는 재설계가 필요한 경우**: [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)마다 실행 경로가 크게 다르고, 불규칙 메모리 접근이 많으며, 동적 자료구조 탐색이 핵심인 경우

### 대표 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- CPU 코드를 거의 그대로 옮겨 깊은 `if-else`와 [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/)를 남겨 두는 경우
- 구조체 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) ([Array](/studynote/08_algorithm_stats/04_datastructure/055_array/) of Structures, AoS)을 그대로 사용해 워프 내 주소 접근이 흩어지는 경우
- 블록 크기만 키우면 무조건 빨라진다고 생각해 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 압박과 점유율 저하를 놓치는 경우

기술사 관점의 핵심 판단 문장은 이것이다. **SIMT는 범용성이 아니라 처리량을 위해 설계된 모델이므로, 제어 유연성을 소프트웨어 쪽에서 정돈해 줄 때 가장 큰 효과가 난다.** 결국 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 튜닝은 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 수를 줄이는 것만큼, 같은 워프가 같은 길을 가도록 만드는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 배치와 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 설계가 중요하다.

- **📢 섹션 요약 비유**: SIMT 최적화는 관광객을 버스에 태우는 일과 같다. 같은 목적지 사람끼리 태우면 버스가 곧장 가지만, 중간마다 다른 곳에 내려 달라고 하면 큰 버스의 장점이 사라진다.

---

## Ⅴ. 기대효과 및 결론

SIMT의 가장 큰 효과는 제한된 전력과 면적 안에서 엄청난 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리량을 끌어낼 수 있다는 점이다. 명령 제어를 워프 단위로 단순화하면 더 많은 연산 유닛을 넣을 수 있고, 수많은 워프를 교대로 실행해 메모리 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)까지 숨길 수 있다. 이 때문에 그래픽 처리뿐 아니라 딥러닝 학습, 과학 시뮬레이션, 영상 처리처럼 반복적 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성이 큰 분야에서 GPU가 핵심 플랫폼이 되었다.

하지만 한계도 분명하다. 워프 내부 제어 흐름이 자주 갈라지면 이론적 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성이 실제 처리량으로 이어지지 않고, 메모리 접근이 불규칙하면 코어 수보다 메모리 병목이 먼저 드러난다. 또한 [텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) ([Tensor Core](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)) 같은 전용 행렬 가속기가 확산되면서, SIMT만으로 모든 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 연산을 최적으로 설명하기도 어려워지고 있다. 즉 SIMT는 여전히 GPU의 기본 실행 철학이지만, [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 특화 가속기와 결합하는 방향으로 진화 중이다.

따라서 SIMT는 "GPU의 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 모델"로만 외우기보다, <strong>대량 <a href="/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>성을 얻기 위해 독립 <a href="/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a>를 하드웨어 묶음으로 실행하는 절충 구조</strong>로 기억하는 것이 정확하다. 이 관점을 잡아야 워프, [SM](/studynote/01_computer_architecture/12_accelerators_ai_hardware/421_streaming_multiprocessor/), 코얼레싱, 점유율, [텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) 같은 주변 개념도 하나의 그림으로 연결된다.

- **📢 섹션 요약 비유**: SIMT는 혼자 아주 똑똑한 기사 한 명보다, 같은 길을 효율적으로 달리는 배송 차량 함대를 만드는 방식이다. 다만 차량마다 전혀 다른 골목으로 들어가야 하면, 함대의 장점은 빠르게 줄어든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| 워프 (Warp) | SIMT가 실제로 명령을 발행하는 최소 실행 단위이며, 분기 발산의 기준이 된다. |
| [SM](/studynote/01_computer_architecture/12_accelerators_ai_hardware/421_streaming_multiprocessor/) ([Streaming Multiprocessor](/studynote/01_computer_architecture/12_accelerators_ai_hardware/421_streaming_multiprocessor/)) | 여러 워프와 블록이 상주하며, 워프 [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 은닉을 수행하는 실행 공간이다. |
| 워프 분기 발산 (Warp Divergence) | 같은 워프의 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 서로 다른 분기를 타며 처리량이 떨어지는 대표 병목이다. |
| 메모리 코얼레싱 (Memory Coalescing) | 워프 단위 메모리 접근이 연속적일 때 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 효율이 높아지는 원리다. |
| 점유율 (Occupancy) | SM에 동시에 유지되는 워프 수와 자원 사용량의 균형을 보여주는 운영 지표다. |
| [텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) ([Tensor Core](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)) | SIMT 기반 [CUDA](/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/) (Compute Unified Device [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/)) 코어를 보완해 행렬 연산을 더 전용화한 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 가속 블록이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
SIMD (Single Instruction Multiple Data)
    |
    v
SIMT (Single Instruction Multiple Threads)
    |
    +--> Warp · Active Mask · Warp Divergence
    |
    +--> SM (Streaming Multiprocessor) · Occupancy · Latency Hiding
    |
    +--> Memory Coalescing · Shared Memory 최적화
    |
    +--> Independent Thread Scheduling · Tensor Core 결합
```

이 흐름은 벡터 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성의 철학이 GPU에서 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 추상화와 결합되고, 이후에는 제어 유연성 완화와 전용 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 가속기로 확장되는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. SIMT는 선생님이 32명에게 한 번에 같은 문제를 내주고, 아이들은 각자 자기 번호 문제를 푸는 방식이에요.
2. 모두 같은 설명을 들을 때는 아주 빠르지만, 절반은 덧셈하고 절반은 뺄셈해야 하면 번갈아 시켜야 해서 느려져요.
3. 그래서 GPU는 비슷한 일을 하는 아이들을 한 줄에 잘 세워 놓을수록 더 똑똑하게 빨라져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 424 / 803

<- **이전**: [422. 스레드 블록 (Thread Block)과 워프 (Warp)](/studynote/01_computer_architecture/12_accelerators_ai_hardware/422_thread_block_and_warp/)
**다음**: [424. NPU (Neural Processing Unit)](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) ->

---
