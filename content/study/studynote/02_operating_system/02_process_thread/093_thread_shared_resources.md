+++
weight = 93
title = "93. 스레드의 자원 공유 - Code, Data, Heap, 열린 파일"
date = "2026-03-21"
[extra]
categories = "studynote-operating-system"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[092_thread_lwp|스레드]] ([[092_thread_lwp|Thread]])의 자원 공유는 단일 프로세스 ([[300_process|Process]]) 내에서 동작하는 여러 실행 흐름이 주소 공간 중 코드 ([[082_process_memory_structure|Code]]), [[001_dikw_pyramid|데이터]] ([[001_dikw_pyramid|Data]]), 힙 ([[078_heap_datastructure|Heap]]) 영역과 열린 [[501_file_definition_logical_record|파일]] (Open Files)을 공동으로 소유하고 직접 접근하는 메커니즘이다.
> 2. **가치**: 독립된 주소 공간을 갖는 [[117_ipc|프로세스 간 통신]] ([[117_ipc|IPC]]) 방식에 비해, 메모리를 직접 읽고 쓰는 자원 공유 구조는 [[034_context_switch|컨텍스트 스위칭]] ([[033_context|Context]] Switching) 오버헤드를 대폭 줄이고 전체 시스템 [[139_throughput|처리량]]을 극대화한다.
> 3. **판단 포인트**: 공유 자원의 편리함은 필연적으로 경쟁 상태 ([[213_race_condition|Race Condition]])라는 치명적 부작용을 동반하므로, 뮤텍스 ([[223_mutex|Mutex]])나 [[224_semaphore|세마포어]] ([[224_semaphore|Semaphore]])와 같은 엄격한 [[212_synchronization_mechanisms|동기화]] ([[212_synchronization_mechanisms|Synchronization]]) 제어가 아키텍처 설계의 최우선 고려사항이 되어야 한다.

---

## Ⅰ. 개요 및 필요성

[[092_thread_lwp|스레드]] ([[092_thread_lwp|Thread]])의 자원 공유는 [[001_operating_system_purpose|운영체제]] (OS)가 프로세스에 할당한 한정된 시스템 자원과 [[381_virtual_memory|가상 메모리]] 공간을 여러 실행 단위([[092_thread_lwp|스레드]])가 쪼개지 않고 함께 사용하는 구조적 특징을 말한다.

전통적인 다중 프로세스 (Multi-[[300_process|Process]]) 환경에서는 각 프로세스가 완전히 독립적인 메모리 공간을 가져 안정성은 높았으나, 프로그램 코드와 [[001_dikw_pyramid|데이터]]를 매번 중복 적재해야 하는 심각한 메모리 낭비가 발생했다. 더욱이 프로세스끼리 통신하려면 커널을 거치는 무거운 [[117_ipc|IPC]] (Inter-[[300_process|Process]] Communication) 기법을 사용해야만 했다. [[014_concurrency|동시성]] ([[266_other_transparency|Concurrency]])이 강조되는 현대 애플리케이션 환경에서 이러한 비효율은 [[282_performance_tactics|성능]] 병목으로 직결되었고, 결국 실행의 흐름만 독립적으로 유지하되 무거운 짐(자원)은 하나만 두고 다 같이 돌려 쓰는 '[[092_thread_lwp|스레드]]'라는 가벼운 패러다임이 필수적으로 등장하게 되었다.

- **📢 섹션 요약 비유**: 프로세스가 하나의 "큰 주방"이라면, [[092_thread_lwp|스레드]]는 주방 안에서 일하는 "여러 명의 요리사"와 같다. 요리사들은 각자의 도마([[057_stack|스택]])는 따로 쓰지만, 냉장고([[001_dikw_pyramid|데이터]] 영역)나 조리 도구(열린 [[501_file_definition_logical_record|파일]]), 레시피(코드)는 공동으로 공유하여 불필요한 동선을 최소화한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

프로세스의 [[381_virtual_memory|가상 메모리]] 레이아웃 내에서 [[092_thread_lwp|스레드]]는 오직 [[057_stack|스택]] ([[057_stack|Stack]]) 영역과 [[057_register|레지스터]] ([[175_register_addressing|Register]]) 상태만 분리하고, 나머지 모든 영역을 100% 공유한다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│               프로세스 내 스레드 간 자원 공유 아키텍처                  │
├─────────────────────────────────────────────────────────────────────────┤
│  [ 운영체제가 할당한 단일 프로세스 (Process) 가상 주소 공간 ]             │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────┐            │
│  │  Code (Text)  : 프로그램 명령어 (읽기 전용, 100% 공유)       │            │
│  ├─────────────────────────────────────────────────────────┤            │
│  │  Data (BSS/Init): 전역 변수, 정적 변수 (읽기/쓰기 공유)        │            │
│  ├─────────────────────────────────────────────────────────┤            │
│  │  Heap         : 동적 할당 메모리 공간 (객체 포인터 공유)      │            │
│  ├─────────────────────────────────────────────────────────┤            │
│  │  [공유 시스템 자원] 열린 파일 목록 (FD Table), 시그널 정보      │            │
│  ├─────────────────────────────────────────────────────────┤            │
│  │  ↓ (Heap은 아래로 확장)                           (Stack은 ↑) │            │
│  │                                                         │            │
│  │ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │            │
│  │ │  Thread 1    │  │  Thread 2    │  │  Thread 3    │    │            │
│  │ │   Stack      │  │   Stack      │  │   Stack      │    │            │
│  │ │  (독립 할당)   │  │  (독립 할당)   │  │  (독립 할당)   │    │            │
│  │ └──────────────┘  └──────────────┘  └──────────────┘    │            │
│  └─────────────────────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────────────────┘
```

코드 ([[082_process_memory_structure|Code]]) 영역은 모든 [[092_thread_lwp|스레드]]가 동일한 명령어를 읽어들이는(Fetch) 바탕이 되며, 전역 변수가 놓인 [[001_dikw_pyramid|데이터]] ([[001_dikw_pyramid|Data]]) 영역과 런타임에 객체가 생성되는 힙 ([[078_heap_datastructure|Heap]]) 영역은 메모리 주소(포인터)만 알면 어떤 [[092_thread_lwp|스레드]]든 즉각 읽고 쓸 수 있다. 또한 프로세스 단위로 [[521_open_file_table|열린 파일 테이블]] ([[501_file_definition_logical_record|File]] Descriptor Table)을 공유하기 때문에, [[092_thread_lwp|스레드]] 1이 연 [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]]을 [[092_thread_lwp|스레드]] 2가 권한 없이 곧바로 이어서 쓸 수 있다. 이 구조 덕분에 [[092_thread_lwp|스레드]] 전환 시 무거운 캐시 플러시 (Cache Flush)나 [[353_page_table|페이지 테이블]] 교체가 일어나지 않아 [[148_5g_embb_urllc_mmtc|초고속]] [[211_context_switch|문맥 교환]]이 가능해진다.

- **📢 섹션 요약 비유**: 여러 지점을 둔 회사가 매번 새로운 건물을 똑같이 지어서 쓰는 것(멀티프로세스)을 포기하고, 하나의 거대한 사옥에 여러 부서를 입주시킨 뒤 복도, 회의실, 정수기(공유 자원)를 다 같이 쓰게 만들어 비용과 시간을 아끼는(멀티스레드) 아키텍처다.

---

## Ⅲ. 비교 및 연결

자원 공유의 달콤함은 [[352_defect_definition|결함]] 격리 (Fault [[195_isolation_concurrency_control|Isolation]])의 상실과 [[212_synchronization_mechanisms|동기화]] 복잡도 증가라는 무거운 청구서를 가져온다.

| 비교 항목 | [[095_multithreading_benefits|다중 스레드]] (Multi-[[092_thread_lwp|Thread]]) | 다중 프로세스 (Multi-[[300_process|Process]]) | 판단 포인트 |
|:---|:---|:---|:---|
| **[[001_dikw_pyramid|데이터]] 통신 공간** | [[001_dikw_pyramid|Data]], [[078_heap_datastructure|Heap]] 직접 [[316_reference_pattern_nosql|참조]] ([[118_shared_memory|공유 메모리]]) | 독립된 주소 공간 (접근 불가) | **자원 분리 및 독립성** |
| **통신 속도** | L1/L2 캐시 속도 (수 ns, 즉각적) | [[123_pipe|파이프]], [[125_socket|소켓]] 등 [[117_ipc|IPC]] 통신 (수천 ns) | **통신 [[015_지연_데이터_관점|지연]] ([[141_latency|Latency]])** |
| **[[211_context_switch|문맥 교환]] 오버헤드** | 작음 ([[381_virtual_memory|가상 메모리]] 맵 유지, 캐시 히트율 높음)| 큼 ([[357_tlb|TLB]] 플러시, 전체 캐시 미스 발생) | **시스템 [[139_throughput|처리량]] ([[139_throughput|Throughput]])** |
| **[[352_defect_definition|결함]] 격리 ([[195_isolation_concurrency_control|Isolation]])**| **한 [[092_thread_lwp|스레드]] 오류(Segfault) 시 전체 사망** | 한 프로세스가 죽어도 타 프로세스 생존 | **안정성 및 장애 전파 ([[345_reliability_security|Reliability]])** |
| **개발 복잡도** | **[[213_race_condition|Race Condition]], [[281_deadlock_definition|Deadlock]] 방어 필수 (높음)** | OS가 통제를 대행하므로 상대적으로 낮음 | **[[212_synchronization_mechanisms|동기화]] ([[212_synchronization_mechanisms|Synchronization]]) 난이도** |

[[095_multithreading_benefits|다중 스레드]] 환경에서는 [[092_thread_lwp|스레드]] A가 Heap의 변수를 업데이트하면 [[092_thread_lwp|스레드]] B는 일반 메모리 로드 명령 한 줄로 그 값을 즉각 인식한다. 하지만 [[118_shared_memory|공유 메모리]]의 치명적인 약점은 생사(生死)를 함께한다는 점이다. [[092_thread_lwp|스레드]] 하나가 잘못된 포인터를 건드려 [[364_segmentation|세그멘테이션]] 폴트 ([[364_segmentation|Segmentation]] Fault)를 일으키면, [[001_operating_system_purpose|운영체제]]는 해당 주소 공간 전체를 회수하므로 프로세스 내부의 무고한 다른 [[092_thread_lwp|스레드]]까지 몰살당한다.

- **📢 섹션 요약 비유**: [[092_thread_lwp|스레드]]의 자원 공유는 **'옆자리에 앉은 동료에게 문서를 직접 건네주는 것'**처럼 빠르지만, 만약 그 동료가 실수로 책상에 커피를 엎지르면 내 서류까지 몽땅 젖어버리는([[352_defect_definition|결함]] 격리 실패) 치명적 위험을 내포한다. 프로세스의 IPC는 우체국을 통해 등기 우편을 보내는 것처럼 느리지만 확실히 안전하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

무분별한 자원 공유는 [[090_service_kubernetes_network_load_balancing|서비스]] 전체를 예측 불가능한 버그의 늪으로 몰아넣는다. 실무에서는 [[212_synchronization_mechanisms|동기화]] 통제가 핵심이다.

1. **경쟁 상태 ([[213_race_condition|Race Condition]]) 방어 설계**  
   여러 [[092_thread_lwp|스레드]]가 [[001_dikw_pyramid|Data]] 영역의 전역 변수(예: 조회수 [[059_counter|카운터]])를 동시에 증가시킬 때, 메모리 로드(Load)-연산(Add)-저장(Store)의 비원자성 때문에 카운트가 누락되는 현상이 잦다. 실무 엔지니어는 공유 자원 접근 구간인 [[214_critical_section|임계 구역]] ([[214_critical_section|Critical Section]])을 식별하고, 반드시 뮤텍스 ([[223_mutex|Mutex]])나 [[222_spinlock|스핀락]] ([[222_spinlock|Spinlock]])을 걸어 배타적 접근을 보장하거나, 하드웨어 단의 [[768_cas_compare_and_swap_lock_free|CAS]] ([[415_compare_and_swap|Compare-And-Swap]]) 명령을 사용하는 원자적 (Atomic) 자료구조를 도입해야 한다.
2. **[[157_oom_killer|OOM]] 방어 및 열린 [[501_file_definition_logical_record|파일]] 한계 튜닝**  
   웹 서버(Nginx, Tomcat)에서 수만 개의 [[092_thread_lwp|스레드]]를 띄울 때, 모든 [[092_thread_lwp|스레드]]가 열린 [[501_file_definition_logical_record|파일]] 목록을 공유하므로 OS의 `ulimit` ([[501_file_definition_logical_record|파일]] 디스크립터 최대 한계) 설정치를 초과해 "Too many open files" 에러가 발생하기 쉽다. 또한 [[078_heap_datastructure|Heap]] 영역의 메모리 릭 ([[612_memory_leak_detection|Memory Leak]])은 단일 [[092_thread_lwp|스레드]]의 실수가 프로세스 전체의 [[157_oom_killer|OOM]] ([[157_oom_killer|Out Of Memory]]) 킬러 호출로 이어지므로 엄격한 할당 해제 검증이 필수다.

- **📢 섹션 요약 비유**: 공유 도로([[118_shared_memory|공유 메모리]])에서는 모든 차들이 장애물 없이 쌩쌩 달릴 수 있어 빠르지만, 교차로 한가운데에 정확한 신호등([[510_lock|Lock]])을 설치해 주지 않으면 결국 대형 교통사고([[001_dikw_pyramid|데이터]] [[003_integrity|무결성]] 훼손)가 나고 모든 도로가 마비되는 결과를 낳는다.

---

## Ⅴ. 기대효과 및 결론

[[092_thread_lwp|스레드]]의 자원 공유는 현대 [[014_concurrency|동시성]] 프로그래밍이 달성한 최고의 아키텍처적 타협안이다. 가장 무거운 [[082_process_memory_structure|Code]], [[001_dikw_pyramid|Data]], Heap을 과감히 하나로 합침으로써 가용 메모리를 대폭 절약했고, [[034_context_switch|컨텍스트 스위칭]]의 짐을 가볍게 만들어 실시간 고성능 서버 구축을 가능케 했다.

하지만 락([[510_lock|Lock]])에 의존하는 기존의 [[212_synchronization_mechanisms|동기화]] 방식은 병목 현상을 유발하므로, 미래의 설계는 락 프리 ([[256_lock_free_data_structures|Lock-free]]) 알고리즘으로 넘어가거나 [[694_thread_local_storage_tls|스레드 로컬 스토리지]] ([[694_thread_local_storage_tls|TLS]], [[113_thread_local_storage|Thread Local Storage]])를 활용해 "최대한 공유하지 않고 각자 독립적으로 일하게 만드는" 방향으로 진화하고 있다. 자원 공유는 필수불가결하지만 맹신할 수 없는 기술이며, 어느 영역을 공유하고 어느 영역을 분리할지 결정하는 것이 고급 아키텍트의 진정한 역량이다.

- **📢 섹션 요약 비유**: 자원 공유는 험난한 [[014_concurrency|동시성]] 처리라는 산을 오르기 위한 가장 가볍고 효율적인 배낭이다. 하지만 그 안에 담긴 짐들을 서로 엉키지 않게 꽉 묶는 규칙([[212_synchronization_mechanisms|동기화]])을 지키지 않으면 결국 배낭 안에서 모든 것이 부서져 산을 오를 수 없게 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[382_virtual_address_space|가상 주소 공간]] ([[382_virtual_address_space|Virtual Address Space]])** | [[092_thread_lwp|스레드]]들이 자원을 공유하기 위해 밟고 서 있는 프로세스 단위의 거대한 논리적 토대 |
| **[[211_context_switch|문맥 교환]] ([[033_context|Context]] Switching)** | 공유 자원 구조 덕분에 캐시나 매핑 테이블을 갈아엎지 않고 [[148_5g_embb_urllc_mmtc|초고속]] 전환을 가능하게 하는 [[092_thread_lwp|스레드]]의 무기 |
| **뮤텍스 ([[223_mutex|Mutex]]) & [[214_critical_section|임계 구역]] ([[214_critical_section|Critical Section]])** | [[092_thread_lwp|스레드]]들이 [[001_dikw_pyramid|Data]]/[[078_heap_datastructure|Heap]] 영역의 동일 변수에 동시 접근할 때 [[001_dikw_pyramid|데이터]] 파괴를 막는 필수 [[571_protection_vs_security|보호]] 메커니즘 |

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

1. [[092_thread_lwp|스레드]] 자원 공유는 한 집에 사는 가족들이 거실, 주방, 화장실([[082_process_memory_structure|Code]], [[001_dikw_pyramid|Data]], [[078_heap_datastructure|Heap]])을 다 같이 쓰는 것과 같아요.
2. 각자 집을 따로 짓고 살면 돈(메모리)도 많이 들고 서로 대화하기도 멀어서 힘든데, 한 집에서 살면 금방 물건을 빌려줄 수 있어서 엄청 빠르고 효율적이에요.
3. 하지만 주방의 도마(공유 자원)를 여러 명이 동시에 쓰려고 하면 싸움이 나니까, 꼭 한 번에 한 명씩만 쓰는 규칙([[212_synchronization_mechanisms|동기화]])을 잘 지켜야 한답니다!
