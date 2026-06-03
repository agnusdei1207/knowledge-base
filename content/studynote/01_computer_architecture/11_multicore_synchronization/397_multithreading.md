+++
title = "397. 멀티스레딩 (Multithreading)"
date = 2026-03-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 멀티스레딩 ([Multithreading](/knowledge-base/studynote/02_operating_system/02_process_thread/095_multithreading_benefits/))은 하나의 프로세스 ([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/)) 안에 여러 실행 흐름을 두어, 같은 주소 공간을 공유하면서도 여러 작업을 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 또는 동시적으로 처리하게 만드는 구조다.
> 2. **가치**: 코드와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 힙 ([Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/))을 공유하므로 프로세스 분리보다 통신 비용과 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 비용이 낮고, 멀티코어 환경에서는 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수준 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성 ([TLP](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/385_tlp/), [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)-Level Parallelism)을 실제 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)으로 바꾸기 쉽다.
> 3. **판단 포인트**: [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 늘리는 것만으로 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 보장되지는 않으며, [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 비용, 캐시 간섭, [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/), [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 구간이 함께 관리될 때만 멀티스레딩의 이점이 살아난다.

---

## Ⅰ. 개요 및 필요성

멀티스레딩 ([Multithreading](/knowledge-base/studynote/02_operating_system/02_process_thread/095_multithreading_benefits/))은 하나의 프로그램 내부에 여러 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) ([Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))를 두어 서로 다른 실행 흐름을 동시에 다루는 방식이다. 여기서 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 프로세스보다 작은 실행 단위이며, 같은 프로세스 안에 있으므로 주소 공간과 자원을 상당 부분 공유한다. 즉, 프로그램을 여러 개 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)하는 대신 하나의 프로그램 안에서 여러 작업자를 두는 설계라고 볼 수 있다.

이 개념이 중요해진 이유는 현대 소프트웨어가 한 가지 일만 하지 않기 때문이다. 웹 서버는 요청 수신, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 질의, 로깅, 캐시 갱신을 동시에 처리해야 하고, 사용자 인터페이스 (UI, User Interface) 프로그램은 화면 응답을 유지하면서 백그라운드 작업도 진행해야 한다. 만약 모든 일을 단일 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 순서대로 처리하면, 한 작업이 입출력 (I/O, Input/Output) 대기에 걸리는 순간 나머지 작업도 함께 멈춘 것처럼 보이게 된다.

또한 [멀티코어 프로세서](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/393_multicore_processor/)가 보편화되면서, 소프트웨어가 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성을 노출하지 않으면 하드웨어의 여러 코어를 활용하기 어렵게 되었다. 결국 멀티스레딩은 반응성을 높이는 기술이면서, 동시에 하드웨어 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성을 끌어내는 기본 수단이 되었다. 반대로 잘못 설계하면 공유 자원 충돌과 디버깅 난이도만 커질 수 있으므로, "여러 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)"는 목적이 아니라 비용을 감수하고 얻는 구조적 선택임을 기억해야 한다.

- **📢 섹션 요약 비유**: 멀티스레딩은 한 식당에서 요리사 한 명이 모든 주문을 순서대로 처리하는 대신, 여러 요리사가 같은 주방을 나눠 쓰며 동시에 움직이게 만드는 운영 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

멀티스레딩의 핵심은 <strong>무엇을 공유하고, 무엇을 각자 갖는가</strong>에 있다. 같은 프로세스의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)들은 코드 ([Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/)), 전역 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 힙 메모리를 공유하지만, [프로그램 카운터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) ([PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/), Program [Counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)), [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) ([Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)), [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) ([Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/))은 각자 독립적으로 가진다. 이 구조 덕분에 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 간 협업은 빠르지만, 공유 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 대한 동시 접근은 곧바로 경쟁 조건으로 이어질 수 있다.

| 구성 요소 | 공유 여부 | 의미 | 설계상 중요점 |
| :-- | :-- | :-- | :-- |
| 코드 영역 | 공유 | 같은 명령 집합을 실행 | 코드 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 비용 감소 |
| 전역 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) / 힙 | 공유 | 객체와 버퍼를 함께 사용 | [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 필요 |
| [프로그램 카운터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) | 개별 | 각 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 현재 실행 위치 | 독립 실행 흐름 보장 |
| [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) | 개별 | 계산 중간 상태 저장 | [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 시 저장 대상 |
| [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) | 개별 | [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/), 지역 변수 저장 | 재진입성, 지역성 유지 |

아래 그림은 멀티스레딩에서 공유 영역과 개별 영역이 어떻게 나뉘는지, 그리고 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) (OS, [Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 이를 어떻게 코어에 배치하는지 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│         One Process with Multiple Threads: shared + private         │
├──────────────────────────────────────────────────────────────────────┤
│ Shared within process                                               │
│   Code  │  Global Data  │  Heap  │  Open Files                      │
├──────────────────────────────────────────────────────────────────────┤
│ Thread A            │ Thread B            │ Thread C                │
│ PC / Registers      │ PC / Registers      │ PC / Registers          │
│ Stack               │ Stack               │ Stack                   │
├──────────────────────────────────────────────────────────────────────┤
│ OS Scheduler  ─────────▶  Core 0 / Core 1 / Core 2 로 배치          │
│                       └▶  단일 코어면 시간 분할(Time Slicing) 수행   │
└──────────────────────────────────────────────────────────────────────┘
```

단일 코어에서는 여러 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 실제로 동시에 실행되지 않더라도 시간 분할 (Time Slicing)을 통해 번갈아 실행되므로 사용자에게는 동시성처럼 보인다. 멀티코어에서는 서로 다른 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 다른 코어에서 실제 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 실행될 수 있어 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 향상 효과가 커진다. 그러나 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수가 코어 수보다 지나치게 많아지면 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) ([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)) 비용이 늘고, 같은 캐시 라인을 두고 경쟁하는 [거짓 공유](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/409_false_sharing/) ([False Sharing](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/409_false_sharing/)) 같은 미세 병목도 드러난다.

따라서 멀티스레딩의 원리는 단순히 "여러 개 돌린다"가 아니라, <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/">공유 메모리</a> 기반 협업 + <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/">스케줄러</a> 배치 + <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a> 제어</strong>의 결합으로 이해해야 한다. 같은 주소 공간을 나눠 쓰는 덕분에 빠르지만, 바로 그 공유성 때문에 설계 품질이 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 안정성을 동시에 좌우한다.

- **📢 섹션 요약 비유**: 큰 사무실의 공용 서류함은 모두가 함께 쓰면 빠르지만, 각자 책상과 메모장은 따로 있어야 일이 꼬이지 않는다. 멀티스레딩은 공용 창고와 개인 작업대를 함께 설계하는 일이다.

---

## Ⅲ. 비교 및 연결

멀티스레딩을 이해하려면 멀티프로세싱 (Multiprocessing), 그리고 [동시 멀티스레딩](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/400_smt/) ([SMT](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/400_smt/), Simultaneous [Multithreading](/knowledge-base/studynote/02_operating_system/02_process_thread/095_multithreading_benefits/))과의 경계를 분명히 해야 한다. 멀티스레딩은 소프트웨어 실행 단위를 나누는 방법이고, 멀티코어와 SMT는 그 실행 단위를 하드웨어가 받아들이는 방식이다. 즉 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 "무엇을 나눌 것인가"의 문제이고, 코어와 SMT는 "어디서 실행할 것인가"의 문제다.

| 구분 | 멀티프로세싱 | 멀티스레딩 | [SMT](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/400_smt/) |
| :-- | :-- | :-- | :-- |
| 분리 단위 | 프로세스 | [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) | 하드웨어 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) |
| 주소 공간 | 서로 분리 | 프로세스 내부 공유 | 코어 내부 실행 자원 공유 |
| 통신 방식 | [프로세스 간 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) ([IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/), Inter-[Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/) Communication) 필요 | 메모리 공유 기반 협업 | 소프트웨어 관점에서는 일반 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)처럼 보임 |
| 강점 | 격리와 안정성 | 낮은 협업 비용, 높은 반응성 | 파이프라인 유휴 자원 활용 |
| 주된 한계 | [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·통신 비용 큼 | [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경쟁 | 같은 코어 자원 간섭 |

멀티프로세싱은 격리가 강하므로 장애 전파를 줄이기 좋지만, [프로세스 간 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) 비용이 크다. 반면 멀티스레딩은 협업이 빠르지만, 잘못 공유하면 한 프로세스 내부 전체가 함께 흔들릴 수 있다. 예를 들어 웹 브라우저가 탭 단위로 프로세스를 나누는 이유는 안정성을 높이기 위해서이고, 웹 서버가 요청 처리에 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/) ([Thread Pool](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/))을 쓰는 이유는 협업 비용을 줄이기 위해서다.

또한 이 개념은 뒤이어 나오는 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 주제와 직접 연결된다. 여러 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 하나의 캐시 계층과 메모리 시스템을 공유하므로, 뮤텍스 ([Mutex](/knowledge-base/studynote/02_operating_system/04_synchronization/223_mutex/)), [세마포어](/knowledge-base/studynote/02_operating_system/04_synchronization/224_semaphore/) ([Semaphore](/knowledge-base/studynote/02_operating_system/04_synchronization/224_semaphore/)), 원자적 연산 (Atomic [Operation](/knowledge-base/studynote/05_database/06_dw_olap_trends/329_delta_encoding/)), [메모리 배리어](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/416_memory_barrier/) ([Memory Barrier](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/416_memory_barrier/))가 필수로 등장한다. 결국 멀티스레딩은 단독 개념이 아니라, 멀티코어·[캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/)·하드웨어 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)로 이어지는 관문이다.

- **📢 섹션 요약 비유**: 멀티프로세싱이 벽으로 분리된 여러 가게라면, 멀티스레딩은 한 가게 안에서 직원들이 주방을 함께 쓰는 방식이고, SMT는 한 조리대에서 두 직원이 빈 손을 번갈아 써 가며 효율을 높이는 방식에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 멀티스레딩은 "가능하니 쓴다"가 아니라, 어떤 병목을 줄이기 위해 채택하는지부터 분명해야 한다. 중앙처리장치 바운드 (CPU-bound) 작업은 보통 코어 수 근처까지 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 두는 편이 유리하지만, 입출력 바운드 (I/O-bound) 작업은 대기 시간이 길기 때문에 코어 수보다 더 많은 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 이득일 수 있다. 반대로 공유 락이 많은 구조에서는 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수를 늘릴수록 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)이 오히려 줄어드는 역효과가 나타난다.

### 실무 판단 체크포인트

1. 작업이 CPU-bound인지 I/O-bound인지 먼저 구분했는가?
2. 공유 객체를 정말 공유해야 하는지, 아니면 불변 객체 ([Immutable Object](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/172_builder_immutable_object/))나 [스레드 로컬 저장소](/knowledge-base/studynote/02_operating_system/02_process_thread/113_thread_local_storage/) ([Thread Local Storage](/knowledge-base/studynote/02_operating_system/02_process_thread/113_thread_local_storage/))로 바꿀 수 있는가?
3. [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수가 코어 수, 메모리 용량, [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 비용과 균형을 이루는가?
4. [락 경합](/knowledge-base/studynote/02_operating_system/04_synchronization/275_lock_contention_monitoring/), 데드락 ([Deadlock](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)), [거짓 공유](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/409_false_sharing/), 긴 [임계 구역](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/) ([Critical Section](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/))을 측정했는가?
5. 장애 격리가 더 중요한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)라면 프로세스 분리가 더 적합하지 않은가?

### 채택과 회피 기준

- **채택에 유리한 경우**: 요청 동시성이 높은 서버, 사용자 인터페이스와 백그라운드 작업을 동시에 처리해야 하는 애플리케이션, [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) 기반 협업이 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)상 유리한 경우
- **보수적으로 접근할 경우**: 공유 상태가 많아 락이 폭증하는 구조, 장애 전파를 최소화해야 하는 격리 중심 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 안전성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 비용이 지나치게 큰 시스템

기술사 답안 관점에서는 "멀티스레딩 = 빠름"이라고 쓰면 부족하다. 반드시 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/), [임계 구역](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/) 축소, 불필요한 공유 제거, 락프리 ([Lock-free](/knowledge-base/studynote/02_operating_system/04_synchronization/256_lock_free_data_structures/)) 자료구조 검토, 코어 친화도 ([Affinity](/knowledge-base/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/)) 설정처럼 구체적 설계 판단이 따라와야 한다. 특히 멀티코어 환경에서는 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화보다 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 비용이 먼저 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 상한을 만드는 경우가 많으므로, 채택 이유와 함께 회피 조건도 같이 설명해야 설계 답안이 완성된다.

- **📢 섹션 요약 비유**: 요리사를 더 뽑는 것보다 먼저, 모두가 같은 냄비 손잡이를 동시에 잡지 않게 주방 동선을 바꾸는 일이 중요하다. 멀티스레딩 최적화는 사람 수보다 충돌 지점을 줄이는 설계다.

---

## Ⅴ. 기대효과 및 결론

잘 설계된 멀티스레딩은 시스템 반응성과 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 함께 높인다. 하나의 프로그램이 여러 작업을 끊김 없이 수행할 수 있고, 멀티코어에서는 작업 분산을 통해 실제 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)도 확보할 수 있다. 또한 프로세스 분리보다 메모리 사용량과 통신 비용을 절약하기 쉬워, 서버·데스크톱·모바일 전 영역에서 기본 실행 모델로 자리 잡았다.

그러나 기대효과는 항상 조건부다. [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 구간이 큰 프로그램은 암달의 법칙 (Amdahl's Law) 때문에 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 늘려도 속도 향상이 제한되고, [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)가 과하면 멀티스레딩이 사실상 순차 실행처럼 변한다. 또한 멀티소켓 또는 비균일 메모리 접근 ([NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/), [Non-Uniform Memory Access](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/)) 환경에서는 메모리 배치가 잘못될 경우 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성보다 원격 메모리 접근 지연이 더 큰 비용이 되기도 한다.

앞으로의 흐름은 단순한 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수 증가보다, 가상 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) (Virtual [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)), [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 기반 런타임, 정교한 스케줄링, 하드웨어 원자 연산과의 결합으로 이동하고 있다. 따라서 멀티스레딩은 "여러 일을 동시에 한다"는 표면적 정의보다, <strong>공유 자원을 통제 가능한 비용 안에서 <a href="/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>성으로 바꾸는 실행 구조</strong>로 기억하는 것이 정확하다.

- **📢 섹션 요약 비유**: 멀티스레딩은 같은 악보를 여러 연주자가 나눠 연주하는 합주와 같다. 연주자가 많다고 무조건 좋은 것이 아니라, 박자와 역할 분담이 맞을 때만 음악이 커지고 풍성해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [멀티코어 프로세서](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/393_multicore_processor/) ([Multi-core Processor](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/393_multicore_processor/)) | 소프트웨어 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 실제 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 실행으로 옮겨 주는 하드웨어 기반 |
| [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/) ([Thread Pool](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)) | [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·소멸 비용을 줄이기 위한 대표적 운용 패턴 |
| [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) ([Synchronization](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)) | 공유 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 충돌을 막기 위해 필요한 제어 계층 |
| [거짓 공유](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/409_false_sharing/) ([False Sharing](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/409_false_sharing/)) | 서로 다른 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 같은 캐시 라인을 건드려 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 저하되는 현상 |
| [SMT](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/400_smt/) (Simultaneous [Multithreading](/knowledge-base/studynote/02_operating_system/02_process_thread/095_multithreading_benefits/)) | 하나의 코어 내부 유휴 자원을 활용해 여러 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 효율을 높이는 하드웨어 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 실행 흐름
      │
      ▼
프로세스 기반 분리
      │
      ▼
멀티스레딩 (Multithreading)
      │
      ├──▶ 스레드 풀 (Thread Pool)
      ├──▶ 동기화 (Mutex / Semaphore / Atomic Operation)
      ├──▶ 거짓 공유 (False Sharing) 대응
      ▼
멀티코어 · SMT · 가상 스레드로 확장
```

### 👶 어린이를 위한 3줄 비유 설명

1. 멀티스레딩은 한 팀 안에서 여러 사람이 일을 나눠서 같이 하는 것과 같아요.
2. 모두가 같은 창고를 쓰면 물건을 빨리 주고받을 수 있지만, 동시에 잡아당기면 엉킬 수 있어요.
3. 그래서 컴퓨터는 여러 일을 함께 하되, 서로 부딪히지 않게 순서와 규칙도 같이 정해 줘야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 398 / 803

← **이전**: [396. big.LITTLE 아키텍처](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/396_big_little_architecture/)
**다음**: [398. 거친 멀티스레딩 (Coarse-grained)](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/398_coarse_grained_multithreading/) →

---
