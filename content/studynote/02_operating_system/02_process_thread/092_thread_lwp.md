+++
title = "92. 스레드 (Thread) - 경량 프로세스 (LWP)"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스레드 (Thread)는 프로세스라는 거대한 자원 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 안에서 독립적인 제어 흐름만 분리해 낸 최소 CPU 할당 단위이며, LWP (Lightweight [Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/))는 이를 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 인식하도록 매핑한 가상 CPU다.
> 2. **가치**: 코드, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 힙([Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/)) 영역을 공유하므로 통신([IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/)) 비용이 제로에 가깝고, [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)) 시 메모리 주소 공간([Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/))을 교체할 필요가 없어 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 비약적으로 향상된다.
> 3. **판단 포인트**: 멀티 프로세스와 달리 완벽한 자원 공유가 가능하지만, 단 하나의 스레드에서 발생한 메모리 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 오류가 전체 프로세스를 패닉(Crash)에 빠뜨릴 수 있으므로 장애 격리와 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 설계가 필수적이다.

---

## Ⅰ. 개요 및 필요성

과거 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)에서는 '실행의 흐름'과 '자원 할당의 단위'가 프로세스([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/))라는 하나의 무거운 덩어리로 묶여 있었다. 하지만 웹 서버처럼 수천 명의 동시 접속을 처리해야 하는 환경에서 매번 프로세스를 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)(`fork()`)하는 것은 막대한 메모리 낭비와 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 오버헤드를 발생시켰다.

이 병목을 깨기 위해, 프로세스 내에서 무거운 자원(코드, 전역 변수, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터)은 하나로 공유하되, 각자의 실행 순서([스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/), [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/))만 독립적으로 갖는 스레드 (Thread) 개념이 등장했다. 스레드는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 입장에서 매우 가벼운 뼈대만 가지므로 경량 프로세스 (LWP, Lightweight [Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/))라고도 불린다. 이를 통해 멀티 코어 환경에서 복잡한 [프로세스 간 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) 없이도 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)([Concurrency](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/266_other_transparency/))을 극대화할 수 있게 되었다.

- **📢 섹션 요약 비유**: 프로세스가 주방, 식자재, 냉장고를 모두 갖춘 '독립된 식당 건물'이라면, 스레드는 한 식당 안에서 각자 프라이팬을 들고 분업하는 여러 명의 '요리사'와 같다. 건물을 새로 짓지 않아도 요리사만 늘리면 처리량이 극대화된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

하나의 프로세스 내에 여러 스레드가 존재할 때, 자원의 **'공유 영역'**과 **'독립 영역'**을 정확히 분리하는 것이 아키텍처의 핵심이다.

```text
┌───────────────────────────────────────────────────────────────────────────┐
│              단일 스레드 프로세스 vs 멀티 스레드 프로세스 구조            │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ [ Single-threaded Process ]    [ Multi-threaded Process ]                 │
│ ┌─────────────────────────┐    ┌───────────────────────────┐              │
│ │  Code │  Data │  Files  │    │   Code │  Data │  Files   │ ◀ 공유 자원 │
│ ├─────────────────────────┤    ├───────────────────────────┤              │
│ │                         │    │                           │              │
│ │      Heap (동적 메모리)    │    │        Heap (동적 메모리)     │              │
│ ├─────────────────────────┤    ├──────┬─────────┬──────────┤              │
│ │                         │    │Stack │  Stack  │  Stack   │ ◀ 독립 할당 │
│ │       Stack             │    │ (T1) │   (T2)  │   (T3)   │              │
│ │                         │    ├──────┼─────────┼──────────┤              │
│ │ Registers (PC, SP)      │    │ Regs │  Regs   │  Regs    │ ◀ 독립 할당 │
│ └─────────────────────────┘    └──────┴─────────┴──────────┘              │
│                                                                           │
│ 핵심 원리: 전역 변수와 Heap은 공유하여 통신하고, Stack과 레지스터는 각자 유지 │
└───────────────────────────────────────────────────────────────────────────┘
```

스레드가 아무리 많아져도 코드 영역과 힙, 전역 변수는 단 하나만 존재한다. 따라서 스레드 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받을 때 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)([Pipe](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/))나 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)([Socket](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)) 같은 무거운 IPC가 필요 없이 포인터 주소만 읽으면 된다. 
동시에, 각 스레드는 자신이 어디까지 실행했는지를 기억하는 [프로그램 카운터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)([PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/))와 지역 변수를 담는 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)([Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)), 그리고 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 문맥(TCB, Thread Control Block)을 독립적으로 유지함으로써, 하나의 함수 안에서도 서로 다른 변수 상태를 갖고 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 실행될 수 있다.

- **📢 섹션 요약 비유**: 회사의 공용 복사기와 회의실([Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/), [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 모든 직원이 자유롭게 공유하지만, 각 직원은 자기만의 수첩([레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/))과 개인 서랍장([스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/))을 가지고 독립적으로 업무를 기억하고 진행하는 것과 같다.

---

## Ⅲ. 비교 및 연결

멀티 프로세스와 멀티 스레드는 자원 격리와 교환 비용 측면에서 완벽한 트레이드오프 관계를 가지며, 여기에 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)과 유저 공간을 잇는 LWP의 역할이 개입한다.

| 비교 항목 | 멀티 프로세스 (Multi-[Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/)) | 멀티 스레드 (Multi-Thread) | 아키텍처 판단 포인트 |
|:---|:---|:---|:---|
| **메모리 할당** | 철저히 독립적, 분리됨 | 프로세스 자원 100% 공유 | [데이터 공유](/knowledge-base/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) 빈도 (스레드 압승) |
| **안정성/격리** | 하나가 죽어도 나머진 생존 | 하나가 패닉 나면 전체 사망 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 무중단 요건 (프로세스 승) |
| **[문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 오버헤드**| [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 플러시, [Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 교체 | [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)(TCB)만 교체 | 시스템 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) (스레드 압승) |
| **스케줄링 주체** | OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) (`fork()`) | LWP를 통한 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)/유저 혼합 (`clone()`) | 시스템 콜 오버헤드 최소화 |

유저 스레드는 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 속도가 빠르지만 I/O 대기 시 전체 프로세스가 멈추는 블로킹 문제가 있었다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 스레드는 이를 해결하지만 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 비용이 든다. 리눅스 등 현대 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 이 둘을 매핑하는 **LWP (Lightweight [Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/))** 구조를 채택했다. LWP는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 스케줄링하는 논리적 CPU 역할을 수행하여, 특정 유저 스레드가 디스크 읽기로 블로킹되더라도 다른 LWP에 매핑된 스레드는 멀쩡하게 CPU 코어에서 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 계속 실행되도록 격리한다.

- **📢 섹션 요약 비유**: 멀티 프로세스는 각자 독립된 원룸을 계약해 사생활과 안전은 보장되지만 월세가 비싼 방식이고, 멀티 스레드는 거대한 셰어하우스에서 거실을 공유해 월세는 싸지만, 한 명이 주방에 불을 내면 다 같이 죽는 구조다.

---

## Ⅳ. 실무 적용 및 기술사 판단

무조건적인 멀티 스레드 채택은 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 병목과 데드락이라는 재앙을 부른다. 워크로드 특성에 맞춘 아키텍처 의사결정이 필요하다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 및 실무 의사결정
1. **[스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/) ([Thread Pool](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)) 고갈 및 크기 산정**: 외부 API나 DB 응답을 기다리는 I/O 바운드 작업 시, [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/) 크기를 너무 작게 잡으면 병목이 생기고, 너무 크게 잡으면 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))이 발생한다. 연산 위주(CPU 바운드)라면 코어 개수와 동일하게 맞추고, I/O 위주라면 대기 시간을 고려해 넉넉히 잡거나 비동기(Non-blocking) 이벤트 루프를 결합해야 한다.
2. **[동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) ([Synchronization](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)) 병목 회피**: [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)(전역 변수)에 여러 스레드가 동시 접근하는 [임계 구역](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/)([Critical Section](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/))에 무분별하게 뮤텍스([Mutex](/knowledge-base/studynote/02_operating_system/04_synchronization/223_mutex/)) 락을 걸면 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 처리가 되어 스레드의 이점이 사라진다. 실무에서는 세밀한 락([Fine-grained](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/399_fine_grained_multithreading/) [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)), ThreadLocal 변수, 락 프리([Lock-free](/knowledge-base/studynote/02_operating_system/04_synchronization/256_lock_free_data_structures/)) 알고리즘을 사용해 경합을 분산시켜야 한다.
3. **장애 격리 아키텍처**: 브라우저 탭처럼 어떤 알 수 없는 오류가 발생할지 모르는 환경은 멀티 스레드가 아닌 크롬(Chrome) 방식의 멀티 프로세스 아키텍처로 설계하여, 탭 하나가 죽어도 전체 브라우저가 꺼지지 않게 격리해야 한다.

- **📢 섹션 요약 비유**: 최고의 외과의사(스레드) 100명을 수술실에 모아놔도, 메스([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))가 하나뿐이어서 서로 기다려야만 한다면 1명이 수술하는 것보다 오히려 더 느리고 사고가 나기 쉽다. 자원 접근 순서 통제가 핵심이다.

---

## Ⅴ. 기대효과 및 결론

멀티 스레드 구조는 다중 코어 프로세서([SMP](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/195_real_time_scheduling/))의 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 연산 능력을 100% 끌어올리고, 메모리 낭비를 극적으로 제거하여 현대 엔터프라이즈 시스템과 웹 아키텍처의 절대적인 근간이 되었다. LWP 기반의 스레딩은 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)의 페널티를 최소화하면서도 완벽한 비동기 I/O 통제를 가능하게 했다.

미래에는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 개입 비용조차 아끼기 위해 자바의 가상 스레드(Virtual Thread, [Project](/knowledge-base/studynote/05_database/01_db_architecture_relational/042_relational_algebra_project/) Loom)나 Go 언어의 [고루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/)([Goroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/))처럼, 수십만 개의 유저 레벨 스레드를 소수의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 스레드에 동적으로 얹어 스케줄링하는 **M:N [코루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/)([Coroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/)) 아키텍처**로 완전히 진화하고 있다. 스레드의 본질은 "가장 적은 비용으로 가장 많은 흐름을 통제하는 것"이다.

- **📢 섹션 요약 비유**: 무거운 내연기관 엔진(프로세스) 하나로 움직이던 기차에서, 바퀴마다 작고 독립적인 초경량 전기 모터(스레드)를 달아 각각 완벽하게 속도를 제어하는 사륜구동 하이퍼카로의 진화다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) ([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))** | 프로세스 단위 교환과 달리 스레드 단위 교환은 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 미스나 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 교체가 생략되어 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 기하급수적으로 낮다. |
| **스레드 제어 블록 (TCB)** | 프로세스를 관리하는 PCB 내부에 스레드 개수만큼 존재하며, 각 스레드의 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/), [스택 포인터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/) 정보를 저장하는 구조체. |
| **가상 스레드 (Virtual Thread)** | [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 스레드(LWP)가 가진 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 개수 한계를 극복하기 위해, 언어 런타임 수준에서 수백만 개를 가볍게 스케줄링하는 혁신 모델. |
| **[임계 구역](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/) ([Critical Section](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/))** | 멀티 스레드의 힙/[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 메모리 공유 특성으로 인해 발생하는 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 오염을 막기 위해 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))으로 보호해야 하는 코드 구간. |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 프로세스 아키텍처 (순차 실행)
    │
    ▼
멀티 프로세스 분기 (fork, 무거운 문맥 교환)
    │
    ▼
스레드(Thread) 개념의 분리 (코드/데이터 공유, 스택/PC 독립)
    │
    ▼
유저 스레드 한계 극복을 위한 커널 매핑 (LWP 도입, 1:1 / M:N 모델)
    │
    ▼
비동기 스레드 풀 (Thread Pool) 및 Non-blocking I/O 최적화
    │
    ▼
초경량 유저 레벨 런타임 동시성 (Virtual Thread, Goroutine, Coroutine)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 스레드는 커다란 도화지(프로세스)에서 여러 명의 친구가 각자 붓을 들고 동시에 색칠을 하는 **가벼운 붓놀림**이에요.
2. 도화지와 물감([공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/))은 다 같이 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 때문에 재료를 옮길 필요가 없어서 속도가 엄청나게 빠르죠.
3. 하지만 같은 곳을 칠하겠다고 서로 싸우면 그림이 망가질 수 있기 때문에, 누구 먼저 칠할지 규칙([동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/))을 잘 정하는 게 제일 중요해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 92 / 800

← **이전**: [91. PCB 요소 - PID, 상태, PC, 레지스터, 스케줄링 정보, 메모리 정보, 회계 정보, I/O 상태 정보](/knowledge-base/studynote/02_operating_system/02_process_thread/091_pcb_elements/)
**다음**: [93. 스레드의 자원 공유 - Code, Data, Heap, 열린 파일](/knowledge-base/studynote/02_operating_system/02_process_thread/093_thread_shared_resources/) →

---
