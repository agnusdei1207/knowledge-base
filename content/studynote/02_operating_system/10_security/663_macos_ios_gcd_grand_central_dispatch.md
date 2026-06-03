+++
title = "663. macOS/iOS Grand Central Dispatch (GCD) 블록 및 디스패치 큐 기반 동시성 구조"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Grand Central Dispatch (GCD, `libdispatch`)는 멀티코어 환경에서 개발자가 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)([Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))를 직접 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))을 관리하는 고통을 없애기 위해, Apple이 XNU [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)과 언어(C/Objective-C/Swift) 차원에 깊숙이 통합한 <strong>작업(<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/">Task</a>) 기반의 비동기 실행 프레임워크</strong>다.
> 2. **메커니즘**: 개발자는 단순히 실행할 코드를 '블록(Block, 클로저)'으로 감싸서 <strong>디스패치 큐(Dispatch <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/">Queue</a>)</strong>에 던지기만 하면 된다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)과 GCD가 현재 시스템의 부하 상태를 분석하여 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)([Thread Pool](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/))을 동적으로 늘리거나 줄이며 큐에 쌓인 블록들을 알아서 꺼내 실행한다.
> 3. **가치**: [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 비용과 [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/) 오버헤드를 시스템이 전역적으로 최적화해 주며, 데드락 없는 안전한 병행([Concurrency](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/266_other_transparency/)) 프로그래밍을 대중화하여 iPhone과 [Mac](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 앱 특유의 부드럽고 끊김 없는 사용자 경험(UX)을 가능하게 한 1등 공신이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **블록 (Block)**: C/C++, Objective-C, Swift에서 함수와 그 함수가 실행될 때 필요한 주변 상태([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/))를 통째로 캡처하여 객체처럼 다룰 수 있게 한 구조 (타 언어의 [람다](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)/클로저와 동일).
  - <strong>디스패치 큐 (Dispatch <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/">Queue</a>)</strong>: 개발자가 던진 블록들을 순서대로([Serial](/knowledge-base/studynote/03_network/01_data_communication/009_직렬_전송_vs_병렬_전송/)) 혹은 동시에(Concurrent) 실행하기 위해 담아두는 대기열. GCD의 핵심 인터페이스다.

- <strong>필요성 (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a> 관리의 악몽 탈피)</strong>: 
  - 과거에는 앱이 조금만 무거워져도 화면(UI [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))이 멈췄다. 이를 피하려면 개발자가 `pthread_create()`를 호출해 백그라운드 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 만들고 작업이 끝나면 `join`을 통해 메인 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)에 결과를 알려야 했다.
  - 앱 수십 개가 저마다 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 10개씩 만들면, 기기 전체에 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 수백 개가 되어 메모리가 낭비되고 CPU는 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 교체([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))하느라 정작 앱은 실행하지 못하는 끔찍한 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))이 일어났다.
  - **해결책**: "개발자들아, 제발 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)([Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))를 직접 만들지 마라! 네가 할 일([Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/))만 큐에 던져놓고 가라. [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 몇 개 띄워서 어떻게 분배할지는 가장 똑똑한 XNU [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)(OS)이 알아서 결정하겠다"는 철학으로 GCD가 탄생했다.

  - <strong>과거 (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a> 직접 관리)</strong>: 식당에 손님이 올 때마다 주방장(개발자)이 알바생([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))을 직접 채용하고 계약서를 쓴다. 손님이 없어도 알바생은 월급(메모리)을 받고, 손님이 100명 오면 알바생 100명이 주방에서 부딪히며 요리([문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))를 망친다.
  - **GCD (작업 기반 큐)**: 주방장(개발자)은 요리 레시피(블록)만 써서 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)(디스패치 큐)에 꽂아둔다. 인력사무소(OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))가 그날의 주문량에 딱 맞춰 최적의 숙련된 요리사 팀([스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/))을 알아서 파견하여 레시피대로 요리하게 하고, 한가해지면 돌려보낸다.

- **발전 과정**:
  1. <strong>POSIX Threads (<a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/790_posix_threads_pthreads_standard_api/">pthreads</a>)</strong>: 리눅스/유닉스의 기본 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) C [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/). 관리가 매우 까다로움.
  2. **NSThread / NSOperation**: Apple의 객체 지향 래퍼(Wrapper). 여전히 무거움.
  3. <strong>GCD (<a href="/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">Mac</a> OS X <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/">10</a>.6, iOS 4.0 도입)</strong>: [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨의 지원을 받는 큐 기반 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 모델.
  4. <strong>Swift <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/266_other_transparency/">Concurrency</a> (async/await)</strong>: GCD의 콜백 지옥(Callback Hell)을 문법적으로 해결한 최신 언어 레벨 프레임워크 (내부적으로는 여전히 GCD와 협력함).

- **📢 섹션 요약 비유**: 복잡한 클러치와 기어 조작([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 및 락 관리)을 완전히 없애고, 운전자가 엑셀(큐에 블록 넣기)만 밟으면 알아서 기어를 변속해 주는 완벽한 자동변속기(Auto Transmission)입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 디스패치 큐 (Dispatch [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/))의 종류

GCD는 개발자에게 크게 3가지 종류의 큐를 제공한다.

| 큐 종류 | 특징 | 주요 용도 | 동작 방식 |
|:---|:---|:---|:---|
| <strong>Main <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/">Queue</a></strong> | [Serial](/knowledge-base/studynote/03_network/01_data_communication/009_직렬_전송_vs_병렬_전송/) ([직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)) | **UI 업데이트 전용** | 앱의 메인 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)에서만 실행됨. 큐에 들어간 순서대로 1개씩 처리 |
| <strong>Global <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/">Queue</a></strong> | Concurrent ([병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)) | 백그라운드 연산, 네트워크 통신 | 시스템이 미리 만들어둔 큐. 큐에 들어간 순서대로 시작하지만, 여러 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)에서 동시에 처리하므로 끝나는 순서는 모름 ([QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 지정 가능) |
| <strong>Custom <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/">Queue</a></strong> | [Serial](/knowledge-base/studynote/03_network/01_data_communication/009_직렬_전송_vs_병렬_전송/) 또는 Concurrent | [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 접근 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)) 대체용 | 개발자가 이름을 붙여 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/). Serial로 만들면 완벽한 [상호 배제](/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/)([동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)) 달성 |

---

### 블록의 비동기 실행 메커니즘 (dispatch_async)

UI [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 멈추지 않게 무거운 작업을 백그라운드로 넘기고, 끝나면 다시 UI를 그리는 GCD의 영원한 국민 패턴이다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 GCD 비동기 처리(dispatch_async) 아키텍처             │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  [UI Thread (Main Queue)]                                         │
  │   버튼 클릭! "대용량 이미지 다운로드 시작"                               │
  │         │                                                         │
  │         │  1. dispatch_async (Global Queue) ──────────┐           │
  │         │                                             │           │
  │         ▼  (UI 스레드는 블로킹되지 않고 즉시 다음 UI를 그림!)  │           │
  │   스크롤 등 사용자 터치 계속 반응 중...                         │           │
  │                                                       ▼           │
  │  ============================================= [Global Queue] ====│
  │                                                                   │
  │  [Background Thread (Worker Pool에서 커널이 자동 할당)]               │
  │   - 커널: "어? 글로벌 큐에 블록(일감)이 들어왔네? 노는 스레드 하나 깨워!" │
  │         │                                                         │
  │         │  2. 이미지 다운로드 100MB 진행 (수 초 소요)                   │
  │         │                                                         │
  │         │  3. 다운로드 완료! 화면에 그려야지!                            │
  │         │     dispatch_async (Main Queue) ────────────┐           │
  │         ▼                                             │           │
  │  (스레드는 다른 일감 찾으러 감)                                │           │
  │                                                       │           │
  │  ============================================= [Main Queue] ======│
  │                                                       │           │
  │  [UI Thread] ◀────────────────────────────────────────┘           │
  │   - 메인 런루프가 큐에 쌓인 '화면 업데이트 블록'을 발견하고 실행             │
  │   - 이미지 화면에 짠! (UI 버벅임 0%)                                 │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 개발자는 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 만들거나 없애는 코드를 한 줄도 쓰지 않는다. 그저 `dispatch_async(global_queue) { ... }` 괄호(블록) 안에 코드를 묶어서 던질 뿐이다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 `workqueue` 시스템이 이 블록을 낚아채서 잉여 CPU 코어에 배정한다. 일이 끝나면 UI를 고치기 위해 다시 `dispatch_async(main_queue) { ... }` 로 메인 큐에 블록을 던진다. 이 핑퐁 구조가 iOS 앱 개발의 알파이자 오메가다.

---

### GCD와 XNU [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 통합 (QoS와 Workqueue)

GCD가 다른 언어의 단순한 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)([Thread Pool](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)) [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)와 차원이 다른 이유는 <strong>OS <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a>(XNU)과의 다이렉트 통신</strong> 때문이다.

1. <strong><a href="/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">QoS</a> (<a href="/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">Quality of Service</a>)</strong>: GCD는 블록에 User-Interactive(즉시), User-Initiated(수 초 내), Utility(수 분 내), Background(언젠가) 4가지 태그를 붙인다.
2. <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 연동</strong>: GCD는 이 정보를 XNU [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 쏜다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 스케줄러는 Background 블록을 에너지 효율이 좋은 효율 코어(E-Core, Icestorm)에 배정하고 클럭을 낮춰 배터리를 아낀다. User-Interactive 블록은 즉시 고성능 코어(P-Core, Firestorm)를 풀가동시켜 렌더링을 끝낸다. (Apple Silicon의 완벽한 전력 제어 비결)

- **📢 섹션 요약 비유**: 민간 택배사(앱)가 자체적으로 오토바이를 굴리는 것이 아니라, 우주국(OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))의 인공위성 관제 시스템에 "이 물건은 초특급, 저 물건은 완행"이라고 꼬리표만 달아주면, 우주국이 알아서 전파를 타고 가장 빠르고 저렴한 길로 배송해 주는 국가 통합 물류망입니다.

---

## Ⅲ. 비교 및 연결

### [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 처리 모델 비교

| 비교 항목 | [pthreads](/knowledge-base/studynote/02_operating_system/11_exam_summary/790_posix_threads_pthreads_standard_api/) (수동 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)) | GCD (디스패치 큐) | RxJava / Combine | [Coroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/) / async-await |
|:---|:---|:---|:---|:---|
| **관리 주체** | 개발자 수동 관리 | <strong>OS <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> (자동 최적화)</strong> | [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/) | 언어 런타임 ([State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) Machine) |
| **작업 단위** | [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 전체 (무거움) | **블록 (클로저, 가벼움)** | Observable 스트림 | [코루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/) (가상 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/), 매우 가벼움)|
| <strong><a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a> 방식</strong> | [Mutex](/knowledge-base/studynote/02_operating_system/04_synchronization/223_mutex/), [Semaphore](/knowledge-base/studynote/02_operating_system/04_synchronization/224_semaphore/) | <strong><a href="/knowledge-base/studynote/03_network/01_data_communication/009_직렬_전송_vs_병렬_전송/">Serial</a> <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/">Queue</a> (락 대체)</strong> | 체인 연산 | Suspend / Resume |
| <strong>코드 <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/">가독성</a></strong> | 매우 낮음 | 낮음 (콜백 지옥 발생 가능) | 높음 (단, 러닝커브 극악) | 최상 (동기 코드처럼 보임) |

<strong><a href="/knowledge-base/studynote/03_network/01_data_communication/009_직렬_전송_vs_병렬_전송/">Serial</a> Queue를 이용한 락(<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a>)의 대체</strong>: 
여러 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 배열에 동시에 접근하면 크래시가 난다. 뮤텍스(`NSLock`)를 쓰면 되지만 데드락의 위험이 있다. GCD에서는 나만의 `Serial Queue`를 하나 만들고, 배열을 건드리는 모든 코드를 `dispatch_sync`로 그 큐에 던지면 된다. 큐는 무조건 한 번에 하나씩만 실행하므로, <strong>뮤텍스를 전혀 쓰지 않고도 완벽한 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/147_thread_safe/">Thread-Safe</a> 구조(<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/256_lock_free_data_structures/">Lock-Free</a> 개념의 응용)</strong>를 만들어낸다.

### 과목 융합 관점

- <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a> (OS)</strong>: 전통적인 OS는 프로세스가 I/O 대기(Sleep)에 빠지면 그 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 멈춘다. GCD 환경에서는 특정 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 Sleep에 빠지면, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 "[스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)에 일하는 놈이 줄었네?"를 감지하고 즉시 새 워커 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 띄워 큐에 남은 다른 블록들을 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 없이 처리하게 만든다([Thread pool](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/) overcommit 방지).
- **소프트웨어공학 (SE)**: 객체 지향 프로그래밍에서 함수(동작) 자체를 일급 객체(First-class Citizen)로 취급하는 [함수형 프로그래밍](/knowledge-base/studynote/04_software_engineering/06_software_architecture/324_functional_programming_core/)(클로저)의 철학을 시스템 프로그래밍(C 언어) 영역까지 성공적으로 끌어내린 설계의 승리다.

- **📢 섹션 요약 비유**: 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))을 쓰는 것이 화장실 문을 잠그고 밖에서 사람들을 기다리게 하는 것이라면, [Serial](/knowledge-base/studynote/03_network/01_data_communication/009_직렬_전송_vs_병렬_전송/) Queue는 문을 없애고 좁은 터널([Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/))을 만들어 사람들이 한 줄로 서서 무조건 순서대로 지나갈 수밖에 없게 만드는 똑똑한 건축 설계입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — 데드락 (<a href="/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/">Deadlock</a>)을 유발하는 치명적인 실수</strong>: 주니어 iOS 개발자가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 동기적으로 받아오겠다며 메인 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)에서 아래 코드를 짰다가 앱이 완전히 멈춰버림(Freeze).
   `dispatch_sync(dispatch_get_main_queue(), ^{ print("Hello"); });`
   - **원인 분석**: `dispatch_sync`는 괄호 안의 블록이 '끝날 때까지' 현재 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(메인 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))를 대기(Block)시킨다. 그런데 그 블록을 '메인 큐'에 던졌다. 메인 큐는 현재 실행 중인 작업(방금 부른 sync)이 끝나야 다음 작업을 꺼낸다. 서로가 서로를 영원히 기다리는 완벽한 [교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)([Deadlock](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/))에 빠진 것이다.
   - **대응 (기술사적 가이드)**: 현재 자신이 돌고 있는 동일한 [Serial](/knowledge-base/studynote/03_network/01_data_communication/009_직렬_전송_vs_병렬_전송/) Queue에 대해 `dispatch_sync`를 호출하는 것은 소프트웨어 자살 행위다. UI [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)에서는 무조건 `dispatch_async`를 사용하거나, Swift Concurrency의 `await`를 사용하여 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 블로킹하지 않고 일감만 넘겨야 한다.

2. <strong>시나리오 — 수만 번의 for 문 내부에서의 비동기 호출과 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a> (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/">Out Of Memory</a>)</strong>: 서버에서 10만 개의 사진 URL을 받아와서 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 다운로드하려고 `for (int i=0; i<100000; i++) { dispatch_async(global_queue, ^{ download(); }); }` 코드를 실행했다. 앱이 메모리 부족으로 터졌다.
   - **원인 분석**: 10만 개의 클로저(블록 객체)가 순식간에 메모리 힙([Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/))에 할당되어 GCD 큐에 쌓였다. OS는 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)을 수십 개 띄워 다운로드를 시도하겠지만, 네트워크 I/O 속도보다 `for` 문이 블록을 큐에 쑤셔 넣는 속도가 수만 배 빨라 메모리 풋프린트가 폭발한 것이다 ([Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) Explosion 및 Memory Exhaustion).
   - **아키텍처 적용**: GCD의 <strong>디스패치 <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/224_semaphore/">세마포어</a>(Dispatch <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/224_semaphore/">Semaphore</a>)</strong>를 사용하여 최대 동시 실행 개수를 5개 등으로 제한해야 한다. 또는 이처럼 방대한 반복 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 연산의 경우 `dispatch_apply`를 사용하여 시스템이 코어 수에 맞게 알아서 스레딩과 메모리를 조절하며 동기적으로 기다리게 하는 최적화 기법을 써야 한다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 iOS/macOS 동시성 프로그래밍 (Concurrency) 설계 플로우       │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [앱에서 시간이 오래 걸리는 작업(네트워크, 파일, DB)을 수행해야 함]               │
  │                │                                                  │
  │                ▼                                                  │
  │      태스크 간의 종속성(A가 끝나야 B가 실행)이 복잡하고 취소(Cancel)가 필요한가? │
  │          ├─ 예 ─────▶ [NSOperation / OperationQueue 사용]            │
  │          │            (GCD 위에 얹어진 객체지향 래퍼. 취소/의존성 트리 완벽 지원)│
  │          └─ 아니오 (단순한 Fire-and-forget 백그라운드 작업이다)              │
  │                │                                                  │
  │                ▼                                                  │
  │      데이터의 상호 배제(동기화)를 위해 락(Lock)이 필요한 상황인가?             │
  │          ├─ 예 ─────▶ [Custom Serial Dispatch Queue 생성 및 sync 호출] │
  │          │            (Mutex보다 빠르고 데드락 위험이 낮음)                 │
  │          │                                                        │
  │          └─ 아니오 ──▶ [Global Concurrent Queue 비동기(async) 처리]    │
  │                         작업 완료 후 반드시 Main Queue로 돌아와 UI 갱신!     │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** GCD는 무적의 도구가 아니다. 블록을 한 번 큐에 던지면, 큐에서 꺼내져 실행을 시작하기 전까지는 취소할 방법이 매우 까다롭다. [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 다운로드처럼 "사용자가 취소 버튼을 누르면 즉시 멈춰야 하는" 태스크라면, 무지성 `dispatch_async` 대신 상태([State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)) 관리가 가능한 `NSOperation` 객체로 감싸거나, 최신의 `Task` (Swift [Concurrency](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/266_other_transparency/)) 아키텍처를 적용하는 것이 유지보수성을 살리는 길이다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **Dispatch Group의 활용**: [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 서버 3군데에서 동시에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 가져온 뒤, 3개가 모두 끝나면 화면을 한 번만 그려야 한다([Fan-in](/knowledge-base/studynote/04_software_engineering/04_testing_quality/197_fan_in_fan_out/)). 무식하게 타이머를 돌리지 말고, `dispatch_group_enter`와 `leave`, 그리고 `dispatch_group_notify`를 통해 락 없이 깔끔하게 완료 시점([Synchronization](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) Barrier)을 잡아냈는가?
- <strong><a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/205_priority_inversion/">우선순위 역전</a> (<a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/205_priority_inversion/">Priority Inversion</a>)</strong>: 높은 우선순위([QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/): User-Interactive)의 큐가 낮은 우선순위(Background)의 [Serial](/knowledge-base/studynote/03_network/01_data_communication/009_직렬_전송_vs_병렬_전송/) 큐가 잡고 있는 자원을 기다릴 때, GCD는 똑똑하게도 백그라운드 큐의 우선순위를 일시적으로 뻥튀기(Boost)해준다. 하지만 개발자가 임의의 락([Semaphore](/knowledge-base/studynote/02_operating_system/04_synchronization/224_semaphore/) 등)을 섞어 쓰면 이 부스트가 작동하지 않아 화면이 멈출 수 있음을 검토했는가?

- **📢 섹션 요약 비유**: GCD는 강력한 강물([Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/))입니다. 종이배(블록)를 강물에 띄워 놓으면 알아서 바다(완료)로 가지만, 한 번 떠내려간 배를 중간에 건져내기(취소)는 몹시 어렵습니다. 배를 띄우기 전에 밧줄(NSOperation)을 묶어둘지 말지 고민하는 것이 아키텍트의 몫입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 레거시 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 관리 (pthread) | Grand Central Dispatch (GCD) | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정량 (<a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/">컨텍스트</a> <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a>)</strong>| 100개 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)으로 인한 CPU 낭비 | 코어 수에 맞춘 최적의 Worker 풀 유지 | CPU 오버헤드 급감 및 앱 반응속도 최상 |
| **정량 (코드 라인 수)** | [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)) 관리 코드 수백 줄| 클로저 래핑 코드로 수 줄 내 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) | 비동기 프로그래밍 개발 공수 **80% 절감** |
| **정성 (앱 안정성)** | 휴먼 에러로 인한 데드락과 [Race Condition](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/) | [Serial](/knowledge-base/studynote/03_network/01_data_communication/009_직렬_전송_vs_병렬_전송/) [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/) 통제로 락 프리 효과 달성 | 크래시 없는 안정적([Thread-safe](/knowledge-base/studynote/02_operating_system/02_process_thread/147_thread_safe/)) 앱 구동 보장 |

### 미래 전망
- <strong>Swift <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/266_other_transparency/">Concurrency</a> (async/await)</strong>: GCD는 10년간 iOS 생태계를 지배했지만, "콜백 안에 콜백"이 겹치는 파멸의 피라미드(Callback Hell)와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이스 위험을 문법적으로 막지 못했다. 최근 Apple은 [코루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/)([Coroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/)) 기반의 `async/await`와 메모리 격리를 강제하는 `Actor` 모델을 언어(Swift) 차원에 도입했다. GCD의 철학은 백엔드 엔진으로서 계속 돌아가지만, 개발자가 마주하는 인터페이스는 이 안전한 Actor 모델로 100% 세대교체 중이다.
- <strong>이기종 가속 (<a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/">GPU</a>, Neural 엔진)</strong>: GCD가 단순히 CPU 코어에만 일감을 배분하던 것을 넘어, 애플의 Metal 프레임워크와 결합하여 이미지 처리 블록을 던지면 OS가 알아서 [NPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/)(신경망 엔진)나 GPU의 큐로 디스패치해 주는 시스템 레벨의 이기종([Heterogeneous](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/273_heterogeneous_db/)) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 스케줄러로 진화하고 있다.

### 결론
Grand Central Dispatch (GCD)는 "어떻게 하면 평범한 개발자도 C언어로 완벽한 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 프로그래밍을 짤 수 있을까?"라는 Apple의 집요한 고민이 만들어낸 시스템 소프트웨어의 걸작이다. [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)([Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))라는 OS의 무거운 하드웨어적 추상을 블록(Block)이라는 소프트웨어적 작업 단위로 치환해 냄으로써, 멀티코어의 성능을 공짜로 끌어다 쓸 수 있게 만들었다. 비록 최신 비동기 문법(async/await)에 자리를 내어주고 있지만, 그 기저에 깔린 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/) 오케스트레이션과 큐 기반의 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)) 회피 철학은 모든 현대 비동기 프로그래밍 프레임워크의 영원한 교과서다.

- **📢 섹션 요약 비유**: 복잡한 시계 태엽([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)와 락)을 직접 조립하던 시계공(개발자)들에게, 시간만 입력하면 알아서 톱니바퀴가 물려 돌아가는 마법의 무브먼트(GCD)를 제공하여 누구나 명품 시계를 만들 수 있게 한 혁명입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 기반 [XDP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/670_xdp/) ([eXpress Data Path](/knowledge-base/studynote/02_operating_system/10_security/661_ebpf_xdp_express_data_path/)) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 네트워크 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 우회 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 패킷 드롭/전달 프레임워크 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [안드로이드 바인더](/knowledge-base/studynote/02_operating_system/02_process_thread/135_android_binder/)([Binder](/knowledge-base/studynote/02_operating_system/10_security/662_android_binder_ipc_thread_pool/)) [IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/) 및 객체 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 매핑 메커니즘 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| Windows [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 비동기 프로시저 호출 ([APC](/knowledge-base/studynote/02_operating_system/10_security/664_windows_kernel_apc_dpc_irql/)) 및 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)된 프로시저 호출 (DPC) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [시스템 레지스트리](/knowledge-base/studynote/02_operating_system/10_security/665_windows_registry_configuration_manager/) ([Windows Registry](/knowledge-base/studynote/02_operating_system/10_security/665_windows_registry_configuration_manager/)) 및 구성 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 관리 구조 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[안드로이드 바인더(Binder) IPC 스레드 풀 및 객체 참조 매핑 메커니즘]
    │
    ▼
[macOS/iOS Grand Central Dispatch (GCD) 블록 및 디스패치 큐 기반 동시성 구조]
    │
    ├──▶ [Windows 커널 비동기 프로시저 호출 (APC) 및 지연된 프로시저 호출 (DPC)]
    └──▶ [시스템 레지스트리 (Windows Registry) 및 구성 데이터베이스 관리 구조]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 햄버거 가게에 손님이 100명 왔다고 주방장 100명을 고용하면, 좁은 주방에서 서로 부딪히고 월급만 나가서 가게가 망해요.
2. 애플(OS)이 만든 'GCD'라는 주문 시스템은, 손님들이 주문서(블록)를 레일(큐)에 주르륵 올려놓기만 하면 끝이에요!
3. 그러면 햄버거 요리의 달인 5명([스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/))이 레일에서 주문서를 하나씩 쏙쏙 뽑아서 빛의 속도로 햄버거를 만들어요. 부딪히지도 않고 돈도 아끼는 최고의 주방 시스템이랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 663 / 800

← **이전**: [662. 안드로이드 바인더(Binder) IPC 스레드 풀 및 객체 참조 매핑 메커니즘](/knowledge-base/studynote/02_operating_system/10_security/662_android_binder_ipc_thread_pool/)
**다음**: [664. Windows 커널 비동기 프로시저 호출 (APC) 및 지연된 프로시저 호출 (DPC)](/knowledge-base/studynote/02_operating_system/10_security/664_windows_kernel_apc_dpc_irql/) →

---
