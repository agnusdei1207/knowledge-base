+++
title = "393. 멀티코어 프로세서 (Multi-core Processor)"
date = 2026-03-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 멀티코어 프로세서 (Multi-core Processor)는 한 칩 안에 여러 CPU 코어 (Central Processing Unit Core)를 넣어, 클럭만 높이지 않고도 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 능력을 키우는 구조다.
> 2. **가치**: [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상의 축이 "더 빠른 한 명"에서 "적절히 빠른 여러 명"으로 바뀌면서, 전력·발열 한계 속에서도 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)과 응답성을 함께 확보할 수 있게 되었다.
> 3. **판단 포인트**: 코어 수가 늘어도 [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) ([Cache Coherence](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/)), 메모리 병목, [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 구간이 정리되지 않으면 체감 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 기대만큼 늘지 않는다.

---

## Ⅰ. 개요 및 필요성

멀티코어 프로세서 (Multi-core Processor)는 하나의 [반도체](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/009_semiconductor/) 다이 (Die) 안에 둘 이상의 실행 코어를 집적해 여러 명령 흐름을 동시에 처리하는 프로세서다. 이 구조가 본격적으로 중요해진 이유는 싱글 코어의 클럭 주파수를 계속 높이는 방식이 전력 벽 ([Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Wall)과 발열 벽 (Thermal Wall)에 부딪혔기 때문이다. 즉, 더 빠른 코어 하나를 만드는 비용이 너무 커지자, 적절한 속도의 코어 여러 개를 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 배치하는 방향이 현실적인 해법이 되었다.

특히 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) ([Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))는 이미 여러 프로세스와 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) ([Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))를 동시에 다루고 있었기 때문에, 멀티코어는 소프트웨어의 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성을 실제 하드웨어 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)으로 바꿔 주는 기반이 되었다. 사용자 입장에서는 브라우저, 영상 재생, 백그라운드 업데이트가 동시에 돌아가도 시스템이 덜 버벅이는 이유가 여기에 있다. 반대로 멀티코어가 없다면 모든 작업은 결국 하나의 코어 시간 조각을 두고 경쟁해야 하므로, 다중 작업 환경에서 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 쉽게 누적된다.

아래 그림은 멀티코어가 등장한 배경을 "클럭 증가" 중심에서 "[병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 증가" 중심으로 바꾼 흐름으로 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│      성능 향상의 축 변화: 더 빠른 1코어 → 함께 일하는 N코어 │
├──────────────────────────────────────────────────────────────┤
│ 과거 접근                                                   │
│   1 Core × 매우 높은 Clock  ──▶ 발열 증가 ──▶ 한계 도달      │
│                                                              │
│ 현대 접근                                                   │
│   N Cores × 적정 Clock      ──▶ 병렬 처리 ──▶ 총 처리량 향상 │
└──────────────────────────────────────────────────────────────┘
```

핵심은 멀티코어가 단순한 "코어 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)"가 아니라, 물리 한계에 대응하기 위한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 전략의 전환이라는 점이다. 따라서 멀티코어를 이해할 때는 코어 개수보다 먼저, 왜 클럭 중심 시대가 끝났는지를 같이 기억해야 한다.

- **📢 섹션 요약 비유**: 예전에는 한 사람에게 더 빨리 뛰라고만 시켰다면, 멀티코어는 적당히 빠른 여러 사람이 짐을 나눠 드는 방식이다. 한 사람을 무한히 몰아붙이는 것보다, 팀을 만드는 편이 더 오래 안정적으로 일할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

멀티코어 내부는 "여러 코어 + 계층형 캐시 + 칩 내부 연결망"으로 이해하면 된다. 각 코어는 자체 파이프라인과 L1 캐시 ([Level 1 Cache](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/260_l1_cache/)), 종종 L2 캐시 ([Level 2 Cache](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/261_l2_cache/))를 가지며, 더 바깥에는 여러 코어가 함께 쓰는 [LLC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/) (Last Level Cache) 또는 L3 캐시 ([Level 3 Cache](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/262_l3_cache/))가 놓인다. 이들을 연결하는 통로는 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/), 링, [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/) 기반 [NoC](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/367_noc/) ([Network on Chip](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/367_noc/))로 구성되며, 코어 수가 많아질수록 단순 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)보다 확장성이 좋은 구조가 필요해진다.

| 구성 요소 | 역할 | 설계 포인트 |
| :-- | :-- | :-- |
| 코어 (Core) | 명령 실행과 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 처리 | 파이프라인 효율, [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/), 실행 폭 |
| 사설 캐시 (Private Cache) | 각 코어의 가까운 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 최소화, 캐시 미스 감소 |
| 공유 캐시 (Shared [LLC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/)) | 코어 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재사용 및 메모리 완충 | 용량, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 간섭 관리 |
| 칩 내부 연결망 ([NoC](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/367_noc/)) | 코어·캐시·메모리 컨트롤러 연결 | [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), 홉 수, 확장성 |
| 메모리 컨트롤러 | 외부 [DRAM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) (Dynamic Random Access Memory) 접근 제어 | 병목 완화, 채널 활용도 |

이 구조에서 가장 중요한 문제는 [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) ([Cache Coherence](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/))이다. 코어 0과 코어 1이 같은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 각자 캐시에 들고 있을 때, 한쪽이 값을 바꾸면 다른 쪽의 오래된 복사본을 어떻게 무효화하거나 갱신할지가 핵심이 된다. 이를 위해 MESI (Modified, Exclusive, Shared, Invalid) 같은 프로토콜이 사용되며, 하드웨어는 스누핑 (Snooping) 또는 [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 기반 제어로 어느 캐시가 최신 상태인지를 관리한다.

아래 그림은 여러 코어가 공유 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다룰 때 왜 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 제어가 필요한지 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│        공유 데이터 X에 대한 멀티코어 접근과 일관성 유지      │
├──────────────────────────────────────────────────────────────┤
│ Core 0              Shared LLC               Core 1          │
│ ┌──────────┐        ┌──────────┐        ┌──────────┐         │
│ │ L1: X=10 │◀──────▶│   X=10   │◀──────▶│ L1: X=10 │         │
│ └────┬─────┘        └──────────┘        └────┬─────┘         │
│      │  write X=20                                │          │
│      ▼                                            │          │
│  상태 변경 + 다른 복사본 무효화 요청 ───────────────▶ invalidate │
│                                                   ▼          │
│                                             L1: X=invalid    │
└──────────────────────────────────────────────────────────────┘
```

멀티코어의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 단순히 코어를 많이 붙인다고 끝나지 않는다. 코어가 늘수록 메모리 접근 경쟁, 캐시 간섭, 연결망 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 커지므로, 실제 확장성은 공유 자원을 얼마나 잘 설계했는지에 달려 있다. 그래서 현대 프로세서는 코어 수 증가와 함께 프리패치, [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) ([Non-Uniform Memory Access](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/)) 최적화, 하이브리드 코어 배치까지 함께 고려한다.

- **📢 섹션 요약 비유**: 멀티코어는 여러 요리사가 있는 주방과 같다. 각자 개인 도구는 빨라야 하고, 냉장고와 통로는 막히지 않아야 하며, 같은 주문표를 서로 다르게 읽지 않게 주방 규칙도 정확해야 한다.

---

## Ⅲ. 비교 및 연결

멀티코어를 제대로 보려면 싱글 코어, 멀티프로세서, [동시 멀티스레딩](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/400_smt/) ([SMT](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/400_smt/), Simultaneous [Multithreading](/knowledge-base/studynote/02_operating_system/02_process_thread/095_multithreading_benefits/))과의 경계를 구분해야 한다. 싱글 코어는 한 시점에 주 실행 자원이 제한되므로 응답성과 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 확장이 작고, 멀티코어는 물리 코어를 늘려 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 실행 기반을 넓힌다. 반면 SMT는 하나의 물리 코어 내부 유휴 자원을 활용해 여러 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 섞어 실행하므로, 멀티코어와 비슷해 보여도 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 증가의 원천이 다르다.

| 구분 | 핵심 특징 | 강점 | 주된 한계 |
| :-- | :-- | :-- | :-- |
| 싱글 코어 | 코어 1개 중심 실행 | 구조 단순, [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 부담 적음 | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 한계 큼 |
| 멀티코어 | 물리 코어 여러 개 | 높은 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/), [멀티태스킹](/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/) 유리 | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)·메모리 병목 증가 |
| [SMT](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/400_smt/) | 1코어 내 [다중 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/095_multithreading_benefits/) 혼합 실행 | 유휴 자원 활용도 향상 | 물리 자원 공유로 간섭 발생 |
| 멀티소켓 [SMP](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/195_real_time_scheduling/) (Symmetric Multiprocessing) | 여러 CPU 패키지 확장 | 대규모 서버 확장 | [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 간 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)·비용 증가 |

또한 멀티코어는 다른 과목 개념과도 깊게 연결된다. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)에서는 스케줄러가 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 어떤 코어에 배치하느냐가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 크게 바꾸고, 알고리즘에서는 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수준 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성 ([TLP](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/385_tlp/), [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)-Level Parallelism)을 얼마나 확보하느냐가 멀티코어 효과를 결정한다. [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)에서는 [락 경합](/knowledge-base/studynote/02_operating_system/04_synchronization/275_lock_contention_monitoring/)과 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화가, 네트워크 서버에서는 큐 분산과 코어 친화도 ([Affinity](/knowledge-base/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/))가 병목이 된다.

여기서 반드시 기억할 법칙이 암달의 법칙 (Amdahl's Law)이다. 프로그램의 일부가 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)로 남아 있으면 코어 수를 늘려도 전체 속도 향상은 상한을 가진다. 즉 멀티코어는 "하드웨어 확장"이지만, 실제 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 결국 "소프트웨어 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 품질"과 결합되어야 완성된다.

- **📢 섹션 요약 비유**: 차선을 여러 개 늘려도 톨게이트가 하나면 전체 속도는 거기서 막힌다. 멀티코어는 도로를 넓히는 기술이고, [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 소프트웨어는 톨게이트를 줄이는 기술이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 멀티코어는 "코어 수가 많다"보다 "부하가 코어에 잘 나뉘는가"가 더 중요하다. 예를 들어 웹 서버는 요청 처리 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 커넥션 풀, 비동기 작업 큐가 코어 수와 맞지 않으면 일부 코어만 바쁘고 나머지는 쉬게 된다. 반대로 락이 많은 애플리케이션은 32코어 장비에서도 실제로는 2~3코어 수준의 효율만 낼 수 있다.

### 실무 판단 체크포인트

1. **업무 특성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)**: CPU 바운드 (CPU-bound) 작업인지, I/O 바운드 (Input/Output-bound) 작업인지 먼저 구분한다.
2. **[병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 가능 구간 측정**: 프로파일링으로 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 구간, [락 경합](/knowledge-base/studynote/02_operating_system/04_synchronization/275_lock_contention_monitoring/), 캐시 미스 비율을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. **메모리 구조 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)**: [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 환경이면 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)와 메모리를 같은 노드에 묶는 배치가 필요하다.
4. **코어 수와 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수 분리**: [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 프로세서 수만 보고 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 과도하게 늘리면 문맥 교환만 증가할 수 있다.
5. **[거짓 공유](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/409_false_sharing/) 방지**: 서로 다른 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 같은 캐시 라인을 건드리면 False Sharing이 생겨 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 급락한다.

### 대표 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 코어 수만 늘리면 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 선형 확장된다고 가정하는 설계
- 전역 락 하나로 전체 작업을 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화하는 설계
- 코어 친화도 없이 짧은 작업을 과도하게 이동시켜 캐시 지역성을 깨는 운영
- 메모리 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 한계를 무시하고 계산 자원만 추가하는 인프라 투자

기술사 관점에서는 "멀티코어 채택 여부"보다 "어떤 병목이 먼저 터질지"를 설명할 수 있어야 한다. [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 서버, 실시간 분석, 미디어 인코딩처럼 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성이 높은 업무는 멀티코어의 이익이 크지만, 강한 순차 의존성과 공유 상태가 많은 업무는 구조 개선 없이 장비만 키워도 기대 효과가 제한적이다.

- **📢 섹션 요약 비유**: 주방에 요리사를 더 뽑기 전에, 칼 하나를 모두가 돌려 쓰는 상황부터 없애야 한다. 도구와 동선이 엉켜 있으면 사람 수를 늘릴수록 더 복잡해질 뿐이다.

---

## Ⅴ. 기대효과 및 결론

멀티코어 프로세서는 클럭 상승의 한계를 우회하면서 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/), [멀티태스킹](/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/), 에너지 효율을 동시에 개선한 현대 컴퓨팅의 기본 토대다. 서버에서는 더 많은 요청을 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리하고, 데스크톱과 모바일에서는 사용자 체감 응답성을 높이며, [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 환경에서는 여러 워크로드를 한 장비 위에 안정적으로 공존시킨다. 즉 멀티코어는 단순 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 기술이 아니라, 현대 소프트웨어 구조 전체를 가능하게 한 전제조건에 가깝다.

다만 효과는 항상 조건부다. [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) 비용, 메모리 병목, [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 구간, 스케줄링 오버헤드가 통제되지 않으면 코어 증가는 빠르게 수익 체감 구간에 들어간다. 그래서 앞으로의 방향은 동일 코어를 무작정 늘리는 것보다, [이기종 멀티코어](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/395_heterogeneous_multicore/) ([Heterogeneous Multi-core](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/395_heterogeneous_multicore/)), 가속기 통합, 소프트웨어 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성 개선을 함께 묶는 쪽으로 발전한다.

결국 멀티코어는 "코어가 많을수록 빠르다"가 아니라, "[병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 나눌 수 있는 일을, 메모리와 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 비용 안에서 얼마나 잘 분산하느냐"로 기억해야 한다. 하드웨어는 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 무대를 제공하고, 진짜 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 그 무대를 활용하는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)와 소프트웨어가 완성한다.

- **📢 섹션 요약 비유**: 멀티코어는 큰 공연장의 무대를 넓혀 놓은 것과 같다. 무대가 넓어도 배우들의 동선과 대사가 엉키면 공연은 망하고, 잘 맞춰지면 훨씬 큰 장면을 동시에 펼칠 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수준 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성 ([TLP](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/385_tlp/), [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)-Level Parallelism) | 멀티코어가 실제 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)으로 바뀌기 위한 소프트웨어 측 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 기반 |
| [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) ([Cache Coherence](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/)) | 여러 코어의 캐시 복사본이 같은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 어떻게 일치시키는지 결정 |
| 암달의 법칙 (Amdahl's Law) | [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 구간이 멀티코어 확장 효과의 상한을 만든다는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 법칙 |
| [대칭형 다중 처리](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/382_smp/) ([SMP](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/195_real_time_scheduling/), Symmetric Multiprocessing) | [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 여러 코어를 대등한 실행 자원으로 다루는 기본 모델 |
| [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) ([Non-Uniform Memory Access](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/)) | 코어 수가 커진 시스템에서 메모리 위치에 따라 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 달라지는 구조 |
| [동시 멀티스레딩](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/400_smt/) ([SMT](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/400_smt/), Simultaneous [Multithreading](/knowledge-base/studynote/02_operating_system/02_process_thread/095_multithreading_benefits/)) | 멀티코어와 함께 CPU 활용도를 높이지만 물리 코어 추가와는 다른 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
싱글 코어 고클럭 경쟁
        │
        ▼
전력 벽 (Power Wall) · 발열 벽 (Thermal Wall)
        │
        ▼
멀티코어 프로세서 (Multi-core Processor)
        │
        ├──▶ 캐시 일관성 (Cache Coherence) · MESI
        │
        ├──▶ SMP (Symmetric Multiprocessing) 스케줄링
        │
        └──▶ NUMA · 이기종 멀티코어 · CPU+가속기 통합
```

이 흐름은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 전략이 "클럭 증가"에서 "[병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 구조 + [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 관리 + 자원 배치 최적화"로 이동하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 멀티코어는 똑똑한 한 명을 더 빨리 뛰게 하는 대신, 똑똑한 여러 명이 일을 나눠 하는 컴퓨터 두뇌예요.
2. 그래서 게임, 음악, 다운로드를 동시에 해도 한 사람이 모든 일을 맡을 때보다 훨씬 덜 힘들어요.
3. 하지만 여러 명이 같은 메모를 같이 볼 때는 서로 내용이 다르지 않게 계속 맞춰 봐야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 394 / 803

← **이전**: [392. 다단 연결망 (MIN, Multistage Interconnection Network)](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/392_multistage_interconnection_network/)
**다음**: [394. CMP (Chip Multi-Processor)](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/394_cmp/) →

---
