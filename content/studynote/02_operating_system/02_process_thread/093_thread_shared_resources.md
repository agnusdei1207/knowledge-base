+++
title = "93. 스레드의 자원 공유 - Code, Data, Heap, 열린 파일"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) ([Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))의 자원 공유는 단일 프로세스 ([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/)) 내에서 동작하는 여러 실행 흐름이 주소 공간 중 코드 ([Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/)), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)), 힙 ([Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/)) 영역과 열린 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) (Open Files)을 공동으로 소유하고 직접 접근하는 메커니즘이다.
> 2. **가치**: 독립된 주소 공간을 갖는 [프로세스 간 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) ([IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/)) 방식에 비해, 메모리를 직접 읽고 쓰는 자원 공유 구조는 [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/) ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) Switching) 오버헤드를 대폭 줄이고 전체 시스템 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 극대화한다.
> 3. **판단 포인트**: 공유 자원의 편리함은 필연적으로 경쟁 상태 ([Race Condition](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/))라는 치명적 부작용을 동반하므로, 뮤텍스 ([Mutex](/knowledge-base/studynote/02_operating_system/04_synchronization/223_mutex/))나 [세마포어](/knowledge-base/studynote/02_operating_system/04_synchronization/224_semaphore/) ([Semaphore](/knowledge-base/studynote/02_operating_system/04_synchronization/224_semaphore/))와 같은 엄격한 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) ([Synchronization](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)) 제어가 아키텍처 설계의 최우선 고려사항이 되어야 한다.

---

## Ⅰ. 개요 및 필요성

[스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) ([Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))의 자원 공유는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) (OS)가 프로세스에 할당한 한정된 시스템 자원과 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 공간을 여러 실행 단위([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))가 쪼개지 않고 함께 사용하는 구조적 특징을 말한다.

전통적인 다중 프로세스 (Multi-[Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/)) 환경에서는 각 프로세스가 완전히 독립적인 메모리 공간을 가져 안정성은 높았으나, 프로그램 코드와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 매번 중복 적재해야 하는 심각한 메모리 낭비가 발생했다. 더욱이 프로세스끼리 통신하려면 커널을 거치는 무거운 [IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) (Inter-[Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/) Communication) 기법을 사용해야만 했다. [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) ([Concurrency](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/266_other_transparency/))이 강조되는 현대 애플리케이션 환경에서 이러한 비효율은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목으로 직결되었고, 결국 실행의 흐름만 독립적으로 유지하되 무거운 짐(자원)은 하나만 두고 다 같이 돌려 쓰는 '[스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)'라는 가벼운 패러다임이 필수적으로 등장하게 되었다.

- **📢 섹션 요약 비유**: 프로세스가 하나의 "큰 주방"이라면, [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 주방 안에서 일하는 "여러 명의 요리사"와 같다. 요리사들은 각자의 도마([스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/))는 따로 쓰지만, 냉장고([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 영역)나 조리 도구(열린 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)), 레시피(코드)는 공동으로 공유하여 불필요한 동선을 최소화한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

프로세스의 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 레이아웃 내에서 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 오직 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) ([Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)) 영역과 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) ([Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)) 상태만 분리하고, 나머지 모든 영역을 100% 공유한다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ 프로세스 내 스레드 간 자원 공유 아키텍처 │
├─────────────────────────────────────────────────────────────────────────┤
│ [ 운영체제가 할당한 단일 프로세스 (Process) 가상 주소 공간 ] │
│ │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Code (Text) : 프로그램 명령어 (읽기 전용, 100% 공유) │ │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ Data (BSS/Init): 전역 변수, 정적 변수 (읽기/쓰기 공유) │ │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ Heap : 동적 할당 메모리 공간 (객체 포인터 공유) │ │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ [공유 시스템 자원] 열린 파일 목록 (FD Table), 시그널 정보 │ │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ ↓ (Heap은 아래로 확장) (Stack은 ↑) │ │
│ │ │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │ │
│ │ │ Thread 1 │ │ Thread 2 │ │ Thread 3 │ │ │
│ │ │ Stack │ │ Stack │ │ Stack │ │ │
│ │ │ (독립 할당) │ │ (독립 할당) │ │ (독립 할당) │ │ │
│ │ └──────────────┘ └──────────────┘ └──────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

코드 ([Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/)) 영역은 모든 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 동일한 명령어를 읽어들이는(Fetch) 바탕이 되며, 전역 변수가 놓인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 영역과 런타임에 객체가 생성되는 힙 ([Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/)) 영역은 메모리 주소(포인터)만 알면 어떤 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)든 즉각 읽고 쓸 수 있다. 또한 프로세스 단위로 [열린 파일 테이블](/knowledge-base/studynote/02_operating_system/09_file_system/521_open_file_table/) ([File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) Descriptor Table)을 공유하기 때문에, [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 1이 연 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 2가 권한 없이 곧바로 이어서 쓸 수 있다. 이 구조 덕분에 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 전환 시 무거운 캐시 플러시 (Cache Flush)나 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 교체가 일어나지 않아 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)이 가능해진다.

- **📢 섹션 요약 비유**: 여러 지점을 둔 회사가 매번 새로운 건물을 똑같이 지어서 쓰는 것(멀티프로세스)을 포기하고, 하나의 거대한 사옥에 여러 부서를 입주시킨 뒤 복도, 회의실, 정수기(공유 자원)를 다 같이 쓰게 만들어 비용과 시간을 아끼는(멀티스레드) 아키텍처다.

---

## Ⅲ. 비교 및 연결

자원 공유의 달콤함은 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 격리 (Fault [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/))의 상실과 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 복잡도 증가라는 무거운 청구서를 가져온다.

| 비교 항목 | [다중 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/095_multithreading_benefits/) (Multi-[Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)) | 다중 프로세스 (Multi-[Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/)) | 판단 포인트 |
|:---|:---|:---|:---|
| **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통신 공간** | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), [Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/) 직접 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) ([공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)) | 독립된 주소 공간 (접근 불가) | **자원 분리 및 독립성** |
| **통신 속도** | L1/L2 캐시 속도 (수 ns, 즉각적) | [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/), [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 등 [IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) 통신 (수천 ns) | **통신 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) ([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))** |
| **[문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 오버헤드** | 작음 ([가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 맵 유지, 캐시 히트율 높음)| 큼 ([TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 플러시, 전체 캐시 미스 발생) | **시스템 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) ([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))** |
| **[결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 격리 ([Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/))**| **한 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 오류(Segfault) 시 전체 사망** | 한 프로세스가 죽어도 타 프로세스 생존 | **안정성 및 장애 전파 ([Reliability](/knowledge-base/studynote/04_software_engineering/06_software_architecture/345_reliability_security/))** |
| **개발 복잡도** | **[Race Condition](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/), [Deadlock](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/) 방어 필수 (높음)** | OS가 통제를 대행하므로 상대적으로 낮음 | **[동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) ([Synchronization](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)) 난이도** |

[다중 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/095_multithreading_benefits/) 환경에서는 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) A가 Heap의 변수를 업데이트하면 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) B는 일반 메모리 로드 명령 한 줄로 그 값을 즉각 인식한다. 하지만 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)의 치명적인 약점은 생사()를 함께한다는 점이다. [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 하나가 잘못된 포인터를 건드려 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) 폴트 ([Segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) Fault)를 일으키면, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 해당 주소 공간 전체를 회수하므로 프로세스 내부의 무고한 다른 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)까지 몰살당한다.

- **📢 섹션 요약 비유**: [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 자원 공유는 **'옆자리에 앉은 동료에게 문서를 직접 건네주는 것'**처럼 빠르지만, 만약 그 동료가 실수로 책상에 커피를 엎지르면 내 서류까지 몽땅 젖어버리는([결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 격리 실패) 치명적 위험을 내포한다. 프로세스의 IPC는 우체국을 통해 등기 우편을 보내는 것처럼 느리지만 확실히 안전하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

무분별한 자원 공유는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 전체를 예측 불가능한 버그의 늪으로 몰아넣는다. 실무에서는 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 통제가 핵심이다.

1. **경쟁 상태 ([Race Condition](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/)) 방어 설계**
여러 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 영역의 전역 변수(예: 조회수 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/))를 동시에 증가시킬 때, 메모리 로드(Load)-연산(Add)-저장(Store)의 비원자성 때문에 카운트가 누락되는 현상이 잦다. 실무 엔지니어는 공유 자원 접근 구간인 [임계 구역](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/) ([Critical Section](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/))을 식별하고, 반드시 뮤텍스 ([Mutex](/knowledge-base/studynote/02_operating_system/04_synchronization/223_mutex/))나 [스핀락](/knowledge-base/studynote/02_operating_system/04_synchronization/222_spinlock/) ([Spinlock](/knowledge-base/studynote/02_operating_system/04_synchronization/222_spinlock/))을 걸어 배타적 접근을 보장하거나, 하드웨어 단의 [CAS](/knowledge-base/studynote/02_operating_system/11_exam_summary/768_cas_compare_and_swap_lock_free/) ([Compare-And-Swap](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/415_compare_and_swap/)) 명령을 사용하는 원자적 (Atomic) 자료구조를 도입해야 한다.
2. **[OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 방어 및 열린 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 한계 튜닝**
웹 서버(Nginx, Tomcat)에서 수만 개의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 띄울 때, 모든 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 열린 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 목록을 공유하므로 OS의 `ulimit` ([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터 최대 한계) 설정치를 초과해 "Too many open files" 에러가 발생하기 쉽다. 또한 [Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/) 영역의 메모리 릭 ([Memory Leak](/knowledge-base/studynote/02_operating_system/10_security/612_memory_leak_detection/))은 단일 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 실수가 프로세스 전체의 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) ([Out Of Memory](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/)) 킬러 호출로 이어지므로 엄격한 할당 해제 검증이 필수다.

- **📢 섹션 요약 비유**: 공유 도로([공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/))에서는 모든 차들이 장애물 없이 쌩쌩 달릴 수 있어 빠르지만, 교차로 한가운데에 정확한 신호등([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))을 설치해 주지 않으면 결국 대형 교통사고([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 훼손)가 나고 모든 도로가 마비되는 결과를 낳는다.

---

## Ⅴ. 기대효과 및 결론

[스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 자원 공유는 현대 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 프로그래밍이 달성한 최고의 아키텍처적 타협안이다. 가장 무거운 [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/), [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), Heap을 과감히 하나로 합침으로써 가용 메모리를 대폭 절약했고, [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/)의 짐을 가볍게 만들어 실시간 고성능 서버 구축을 가능케 했다.

하지만 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))에 의존하는 기존의 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 방식은 병목 현상을 유발하므로, 미래의 설계는 락 프리 ([Lock-free](/knowledge-base/studynote/02_operating_system/04_synchronization/256_lock_free_data_structures/)) 알고리즘으로 넘어가거나 [스레드 로컬 스토리지](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) ([TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/), [Thread Local Storage](/knowledge-base/studynote/02_operating_system/02_process_thread/113_thread_local_storage/))를 활용해 "최대한 공유하지 않고 각자 독립적으로 일하게 만드는" 방향으로 진화하고 있다. 자원 공유는 필수불가결하지만 맹신할 수 없는 기술이며, 어느 영역을 공유하고 어느 영역을 분리할지 결정하는 것이 고급 아키텍트의 진정한 역량이다.

- **📢 섹션 요약 비유**: 자원 공유는 험난한 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 처리라는 산을 오르기 위한 가장 가볍고 효율적인 배낭이다. 하지만 그 안에 담긴 짐들을 서로 엉키지 않게 꽉 묶는 규칙([동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/))을 지키지 않으면 결국 배낭 안에서 모든 것이 부서져 산을 오를 수 없게 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[가상 주소 공간](/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/) ([Virtual Address Space](/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/))** | [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)들이 자원을 공유하기 위해 밟고 서 있는 프로세스 단위의 거대한 논리적 토대 |
| **[문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) Switching)** | 공유 자원 구조 덕분에 캐시나 매핑 테이블을 갈아엎지 않고 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 전환을 가능하게 하는 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 무기 |
| **뮤텍스 ([Mutex](/knowledge-base/studynote/02_operating_system/04_synchronization/223_mutex/)) & [임계 구역](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/) ([Critical Section](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/))** | [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)들이 [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)/[Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/) 영역의 동일 변수에 동시 접근할 때 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 파괴를 막는 필수 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 메커니즘 |

### 📈 관련 키워드 및 발전 흐름도

```text
다중 프로세스의 메모리 낭비 및 무거운 IPC 병목
│
▼
스레드 (Thread) 등장 · 주소 공간 (Code/Data/Heap) 공유 메커니즘
│
▼
경쟁 상태 (Race Condition) 발생 · 결함 격리 실패
│
▼
뮤텍스 (Mutex), 세마포어 (Semaphore)를 통한 동기화 제어
│
▼
락 프리 (Lock-free) 자료구조 및 TLS (Thread Local Storage) 도입 (현대적 최적화)
```

### 👶 어린이를 위한 3줄 비유 설명

1. [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 자원 공유는 한 집에 사는 가족들이 거실, 주방, 화장실([Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/), [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), [Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/))을 다 같이 쓰는 것과 같아요.
2. 각자 집을 따로 짓고 살면 돈(메모리)도 많이 들고 서로 대화하기도 멀어서 힘든데, 한 집에서 살면 금방 물건을 빌려줄 수 있어서 엄청 빠르고 효율적이에요.
3. 하지만 주방의 도마(공유 자원)를 여러 명이 동시에 쓰려고 하면 싸움이 나니까, 꼭 한 번에 한 명씩만 쓰는 규칙([동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/))을 잘 지켜야 한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 93 / 800

← **이전**: [92. 스레드 (Thread) - 경량 프로세스 (LWP)](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)
**다음**: [94. 스레드의 독립 자원 - Thread ID, PC, 레지스터 집합, 스택](/knowledge-base/studynote/02_operating_system/02_process_thread/094_thread_independent_resources/) →

---
