+++
title = "419. GPGPU (General-Purpose GPU)"
date = 2026-03-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GPGPU (General-Purpose [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))는 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) ([Graphics Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))의 대량 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 구조를 그래픽 렌더링 밖의 일반 계산에 활용하는 범용 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 컴퓨팅 방식이다.
> 2. **가치**: 행렬 곱셈, 벡터 연산, 시뮬레이션처럼 같은 연산을 엄청난 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 반복하는 문제에서 CPU (Central Processing Unit)보다 훨씬 높은 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 제공한다.
> 3. **판단 포인트**: GPGPU의 성패는 코어 수 자체보다 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성, 메모리 이동 비용, 분기 규칙성이 맞는지에 달려 있다.

---

## Ⅰ. 개요 및 필요성

GPGPU (General-Purpose [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))는 본래 화면 그리기에 특화된 GPU를 범용 수치 계산 장치로 재해석한 아키텍처 활용 방식이다. GPU는 픽셀, 정점, 텍스처처럼 비슷한 계산을 대량 반복하는 그래픽스 문제를 해결하려고 발전했는데, 이 구조가 과학기술 계산과 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 학습의 핵심 작업과도 놀랄 만큼 잘 맞아떨어졌다.

CPU는 [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/), 예외 처리, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 제어처럼 복잡한 흐름을 빠르게 처리하는 데 강하다. 반면 대규모 행렬 연산이나 입자 시뮬레이션은 "같은 공식을 수백만 번 적용"하는 성격이 강해서, 소수의 강한 코어보다 다수의 단순 연산기가 더 유리하다. GPGPU는 바로 이 틈을 파고들어, 기존 그래픽 하드웨어를 고성능 컴퓨팅의 실용적 도구로 바꾸었다.

특히 [HPC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/548_automotive_hpc/) ([High Performance Computing](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/226_hpc_supercomputing_infrastructure/)), 딥러닝, 영상 처리 분야에서는 연산량이 폭증했지만 클럭만 올려 성능을 해결하기 어려웠다. 이때 GPGPU는 "더 복잡한 한 코어" 대신 "더 많은 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 코어"라는 대안을 제시했고, 슈퍼컴퓨터급 계산을 연구실과 기업 서버로 끌어내리는 전환점이 되었다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">왜 GPGPU가 필요해졌는가: 같은 계산의 대량 반복</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CPU가 잘하는 일</div><div class="kb-diagram-cell">GPU가 잘하는 일</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">복잡한 제어</div><div class="kb-diagram-cell">동일 연산의 대량 반복</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">분기 많은 코드</div><div class="kb-diagram-cell">벡터 · 행렬 · 픽셀 계산</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">짧은 응답시간</div><div class="kb-diagram-cell">높은 처리량</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">문제 성격: 데이터가 많고 계산식이 거의 같음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">결론: CPU 단독보다 GPU 병렬 구조를 일반 계산에 활용</div></div>
</div>
</div>



이 그림의 핵심은 GPGPU가 GPU를 "더 빠른 CPU"로 바꾸는 것이 아니라, 문제의 모양에 맞는 연산 자원을 새로 배치하는 전략이라는 점이다. 즉 GPGPU는 그래픽 장치를 탈취한 편법이 아니라, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성에 맞는 하드웨어를 재배치한 구조적 선택이다.

📢 섹션 요약 비유: GPGPU는 그림을 그리던 거대한 미술 학원을 시험 채점장으로 바꿔 쓰는 것과 같다. 학생마다 다른 논술 채점은 어렵지만, 같은 객관식 답안을 수십만 장 한꺼번에 읽는 일은 오히려 훨씬 잘한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

GPGPU의 핵심 원리는 호스트인 CPU가 전체 흐름을 제어하고, 디바이스인 GPU가 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 실행하는 [오프로딩](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/) 구조다. 프로그램은 먼저 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 CPU 메모리에서 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리로 옮기고, 이후 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) ([Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)) 함수를 수많은 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)로 동시에 실행한 뒤, 필요한 결과만 다시 CPU 쪽으로 가져온다.

이 구조가 성립하는 이유는 GPU가 [SM](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/421_streaming_multiprocessor/) ([Streaming Multiprocessor](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/421_streaming_multiprocessor/)) 단위의 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 실행 블록과 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 중심 메모리 구조를 갖기 때문이다. 각 SM은 많은 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 번갈아 실행하며, 어떤 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 묶음이 메모리 접근 때문에 멈추면 다른 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 묶음을 즉시 실행해 연산기를 쉬지 않게 만든다. 이 때문에 GPGPU는 지연시간 하나를 줄이는 것보다, 전체 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 끌어올리는 데 집중한다.

다만 성능은 연산기 수만으로 결정되지 않는다. CPU와 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 사이의 [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) ([Peripheral Component Interconnect](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/) Express) 전송, VRAM (Video Random Access Memory) 접근 패턴, 워프 단위 분기 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재사용도가 함께 맞아야 한다. 결국 GPGPU는 "[병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화"만의 문제가 아니라 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동을 포함한 전체 경로 최적화"의 문제다.

| 구성 요소 | 역할 | 설계상 핵심 질문 |
| :-- | :-- | :-- |
| CPU (Central Processing Unit) | 전체 제어, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 준비, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 호출 | 정말 GPU에 넘길 만큼 일이 큰가 |
| [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) ([Graphics Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)) | 대량 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 계산 수행 | 같은 계산을 많이 반복하는가 |
| [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) ([Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)) | [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)별로 복제되어 실행되는 함수 | 각 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 작업이 독립적인가 |
| [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) ([Peripheral Component Interconnect](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/) Express) | CPU-[GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 경로 | 복사 비용을 계산 이득이 상쇄하는가 |
| VRAM (Video Random Access Memory) | [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 측 작업 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 | 접근 패턴이 연속적이고 재사용 가능한가 |

아래 그림은 GPGPU 성능이 단순 계산 속도보다 "복사-실행-회수" 전체 파이프라인에서 결정된다는 점을 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">GPGPU 오프로딩 파이프라인의 실제 병목</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">① Host 메모리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CPU가 입력 준비</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">② PCIe 전송 ── 데이터 복사 비용 발생</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">③ GPU / SM에서 커널 병렬 실행</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">④ 결과 축약 · 저장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">⑤ PCIe 역전송 ── 결과가 작을수록 유리</div></div>
</div>
</div>



따라서 GPGPU 최적화의 본질은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 GPU에 올린 뒤 가능한 한 오래 머물게 하고, 그 안에서 많은 계산을 수행하게 만드는 것이다. 연산 밀도는 낮고 복사만 많은 작업이라면 GPU는 강점이 아니라 오히려 부담이 된다.

📢 섹션 요약 비유: GPGPU는 본사(CPU)가 대형 물류창고([GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))에 일감을 보내는 방식과 같다. 창고 안 작업자는 엄청 빠르지만, 트럭으로 상자를 보내고 다시 받아오는 시간이 더 길면 외주를 준 의미가 사라진다.

---

## Ⅲ. 비교 및 연결

GPGPU를 정확히 이해하려면 CPU 중심 계산, 전통적 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 그래픽 처리, 그리고 이후 등장한 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 전용 가속기와의 경계를 함께 봐야 한다. CPU는 범용성과 짧은 응답시간을 우선하고, GPU는 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성을 우선하며, GPGPU는 GPU의 이 장점을 그래픽 밖의 문제로 확장한 개념이다.

[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) GPGPU는 그래픽 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) ([Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))를 우회해 텍스처와 셰이더로 계산을 흉내 내야 했지만, [CUDA](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/) (Compute Unified Device [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/))와 OpenCL (Open Computing Language)이 등장하면서 일반 프로그래머도 C 계열 언어로 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 직접 다룰 수 있게 되었다. 이 변화는 GPGPU를 실험적 기법에서 산업 표준으로 끌어올린 결정적 계기였다.

또한 GPGPU는 오늘날 [이기종 컴퓨팅](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/439_heterogeneous_computing/)의 중심축이다. CPU가 제어와 예외 처리를 맡고, GPU가 행렬·벡터 연산을 처리하며, 더 나아가 [TPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/425_tpu/) ([Tensor Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/425_tpu/))나 [NPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) ([Neural Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/))가 특정 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 워크로드를 맡는 구조로 발전했다. 즉 GPGPU는 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 활용 범위를 넓힌 기술이면서, 전용 가속기 시대로 넘어가는 징검다리이기도 하다.

| 비교 축 | CPU 중심 계산 | GPGPU | [TPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/425_tpu/)/[NPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) 중심 가속 |
| :-- | :-- | :-- | :-- |
| 주력 대상 | 분기 많은 범용 코드 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 계산 | 텐서/행렬 중심 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 연산 |
| 장점 | 유연성, 제어력 | 높은 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/), 성숙한 생태계 | 전성비, 특정 모델 최적화 |
| 약점 | 대량 반복 계산 비효율 | 복사 비용, 분기 발산 | 범용성 부족 |
| 대표 환경 | OS, DB, 제어 로직 | 과학 계산, 딥러닝, 렌더링 | 추론 가속, 대규모 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 학습 일부 |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">고정 기능 그래픽 가속</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">프로그래머블 셰이더 (Programmable Shader)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">GPGPU (General-Purpose GPU)</div>
<div class="kb-diagram-tree-item" style="--depth:4">CUDA (Compute Unified Device Architecture)</div>
<div class="kb-diagram-tree-item" style="--depth:4">OpenCL (Open Computing Language)</div>
<div class="kb-diagram-tree-item" style="--depth:4">과학 계산 · 딥러닝 학습</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">전용 AI 가속기(TPU · NPU)와 역할 분화</div>
</div>
</div>



이 흐름이 보여주는 핵심은 GPGPU가 GPU의 범용화 단계라는 점이다. GPU가 모든 것을 해결하는 종착점이 아니라, [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 컴퓨팅을 대중화하고 이후 더 특화된 가속기 분화를 가능하게 만든 중간 플랫폼이라는 뜻이다.

📢 섹션 요약 비유: CPU가 만능 사무직이라면 GPGPU는 같은 서류를 수천 장 동시에 처리하는 대형 백오피스 팀이다. TPU와 NPU는 그중에서도 특정 양식만 초고속으로 처리하도록 더 전문화된 전담 부서라고 볼 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 GPGPU 도입 여부는 "GPU가 비싼가"보다 "문제가 GPGPU 친화적인가"로 판단해야 한다. 대규모 행렬 연산, 영상 필터, 배치 추론, 수치 시뮬레이션처럼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 크고 연산 규칙이 균일한 작업은 적합하다. 반면 문자열 처리, [그래프 탐색](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/613_graph_bfs_memory/), 조건 분기 많은 비즈니스 로직은 GPU에 올려도 효율이 낮거나 오히려 느려질 수 있다.

첫 번째 판단 기준은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 대비 연산량이다. CPU와 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 사이를 오가는 시간이 계산 자체보다 길다면 GPGPU는 실패한다. 그래서 실무에서는 배치 크기를 키우고, 여러 연산을 하나의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 시퀀스로 묶고, 가능한 한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리에 상주시켜 전송 횟수를 줄인다.

두 번째 판단 기준은 제어 흐름의 규칙성이다. GPGPU는 [SIMT](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/423_simt/) (Single [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/), Multiple Threads) 방식으로 움직이므로, 같은 워프 안의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 서로 다른 분기로 갈라지면 직렬화가 발생한다. 따라서 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 설계에서는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정렬, 분기 최소화, 메모리 접근 연속성을 함께 고려해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 충분히 크고 독립적인가?
2. 동일한 계산식이 반복되어 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 간 역할 분리가 쉬운가?
3. [PCIe](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) 전송 비용보다 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 내부 계산 이득이 큰가?
4. [프로파일링](/knowledge-base/studynote/02_operating_system/10_security/613_profiling_gprof/) 결과 병목이 연산인지, 메모리 이동인지 구분했는가?
5. 결과를 자주 CPU로 되돌리지 않고 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 내부에서 후속 계산까지 이어갈 수 있는가?

### 대표 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 작은 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 연산을 매번 GPU로 보내 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 호출 오버헤드만 누적하는 설계
- `if-else` 분기가 많은 비정형 로직을 그대로 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)로 옮기는 설계
- 메모리 접근이 흩어져 VRAM [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 효율을 잃는 설계
- [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 사용률 숫자만 보고 실제 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)과 병목을 착각하는 운영 방식



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">GPGPU 적용 여부 판단 트리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터가 크고 반복 계산인가?</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ No ─▶ CPU 우선</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ Yes</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">분기와 의존성이 적은가?</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ No ─▶ GPU 효율 저하 가능성 큼</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ Yes</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">복사 비용보다 계산 이득이 큰가?</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ No ─▶ CPU 또는 다른 가속 방식 검토</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ Yes ─▶ GPGPU 적용 적합</div></div>
</div>
</div>



기술사 답안 관점에서는 "GPGPU는 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 연산기"라고만 쓰면 부족하다. 반드시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성, 메모리 이동, 분기 발산, 이기종 역할 분담까지 함께 언급해야 실제 설계 판단이 된다.

📢 섹션 요약 비유: GPGPU는 대형 관광버스와 같다. 같은 목적지로 가는 승객이 많을 때는 압도적으로 효율적이지만, 각자 다른 골목으로 흩어지는 손님을 태우면 오히려 택시 여러 대보다 불편해진다.

---

## Ⅴ. 기대효과 및 결론

GPGPU는 컴퓨터 아키텍처의 중심을 "더 빠른 단일 코어"에서 "더 많은 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)"으로 이동시키는 데 결정적 역할을 했다. 그 결과 과학 시뮬레이션, 딥러닝 학습, 대규모 영상 처리 같은 작업이 현실적인 시간 안에 가능해졌고, [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 설계 자체도 CPU 단독 구조에서 CPU+[GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 협업 구조로 바뀌었다.

하지만 GPGPU의 효과는 항상 조건부다. 충분한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성, 높은 연산 밀도, 적절한 메모리 전략이 없다면 GPU는 비싼 유휴 자원이 될 수 있다. 따라서 GPGPU는 "무조건 빠른 하드웨어"가 아니라 "문제 구조가 맞을 때 폭발적인 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 내는 아키텍처"로 기억해야 한다.

앞으로는 GPGPU가 여전히 범용 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 가속의 중심 역할을 하되, 특정 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 연산은 NPU나 [TPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/425_tpu/) 같은 더 특화된 가속기로 분화될 가능성이 크다. 그럼에도 GPGPU는 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 컴퓨팅을 실무 표준으로 만든 역사적 전환점이라는 점에서 계속 중요한 기준이 된다.

📢 섹션 요약 비유: GPGPU는 작은 승용차를 더 빠르게 만든 기술이 아니라, 한 번에 훨씬 많은 짐을 옮기도록 물류 체계를 바꾼 대형 화물 시스템에 가깝다. 무엇을 얼마나 반복해서 옮길지 맞을 때 그 힘이 가장 크게 드러난다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) ([Graphics Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)) | GPGPU의 하드웨어 기반으로, 원래는 그래픽 처리용 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 연산 장치 |
| [CUDA](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/) (Compute Unified Device [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/)) | NVIDIA GPU에서 GPGPU를 실용화한 대표 프로그래밍 플랫폼 |
| OpenCL (Open Computing Language) | 특정 벤더에 묶이지 않게 GPGPU를 구현하려는 개방형 표준 |
| [SIMT](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/423_simt/) (Single [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/), Multiple Threads) | GPGPU에서 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 묶음을 효율적으로 실행하는 핵심 모델 |
| [이기종 컴퓨팅](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/439_heterogeneous_computing/) ([Heterogeneous Computing](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/439_heterogeneous_computing/)) | CPU와 GPU가 역할을 분담하는 시스템 설계 철학 |
| 워프 발산 (Warp Divergence) | GPGPU 효율을 떨어뜨리는 대표적 제어 흐름 문제 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">그래픽 전용 병렬 처리</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">프로그래머블 셰이더 (Programmable Shader)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">GPGPU (General-Purpose GPU)</div>
<div class="kb-diagram-tree-item" style="--depth:4">CUDA (Compute Unified Device Architecture)</div>
<div class="kb-diagram-tree-item" style="--depth:4">OpenCL (Open Computing Language)</div>
<div class="kb-diagram-tree-item" style="--depth:4">HPC (High Performance Computing) · 딥러닝 학습</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">이기종 컴퓨팅 · 전용 AI 가속기 분화</div>
</div>
</div>



이 흐름은 GPU가 화면 처리 장치에서 출발해 범용 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 계산의 핵심 자원으로 확장되고, 다시 더 특화된 가속기 생태계로 갈라지는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. GPGPU는 그림을 잘 그리는 사람들을 모아 두고, 같은 숫자 계산도 같이 시키는 방법이에요.
2. 모두가 똑같은 계산을 많이 해야 할 때는 한 사람보다 수천 명이 동시에 하는 편이 훨씬 빨라요.
3. 하지만 사람마다 다른 문제를 풀어야 하면, 이런 큰 팀보다 똑똑한 한 명의 선생님(CPU)이 더 잘할 수도 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 420 / 803

← **이전**: [418. GPU (Graphics Processing Unit)](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)
**다음**: [420. CUDA (Compute Unified Device Architecture)](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/) →

---
