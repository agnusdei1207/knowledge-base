+++
title = "98. 다대일 (Many-to-One) 스레드 모델"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 다대일 (Many-to-One) 모델은 다수의 [사용자 수준 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/096_user_level_thread/) (ULT, [User-Level Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/096_user_level_thread/))를 단일 [커널 수준 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/097_kernel_level_thread/) (KLT, [Kernel-Level Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/097_kernel_level_thread/))에 매핑하여 스케줄링하는 논리적 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) ([Concurrency](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/266_other_transparency/)) 구현 방식이다.
> 2. **가치**: [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 및 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) Switching)이 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드 진입 없이 사용자 공간 내에서만 처리되므로 오버헤드가 극도로 낮다.
> 3. **판단 포인트**: 하나의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 블로킹 ([Blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/))되면 전체 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 멈추고 멀티코어를 활용할 수 없다는 치명적 한계로 인해 현대 OS에서는 사장되었으나, [코루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/) ([Coroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/)) 등 언어 레벨 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)의 기원이 되었다.

---

## Ⅰ. 개요 및 필요성

다대일 (Many-to-One) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 모델은 응용 프로그램 내에서 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 여러 [사용자 수준 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/096_user_level_thread/) (ULT)가 단 하나의 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) (KLT)에 연결되어 동작하는 구조다. 이 구조에서 스케줄링과 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 관리는 전적으로 사용자 공간 (User Space)의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 라이브러리가 전담한다.

[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) (OS, [Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)라는 개념 자체를 알지 못했다. [프로세스 생성](/knowledge-base/studynote/02_operating_system/02_process_thread/104_process_creation/) 비용이 너무 높았기 때문에, 개발자들은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 뜯어고치지 않고도 하나의 프로세스 내에서 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)을 확보할 우회로가 필요했다. 이에 따라 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 위에서 응용 프로그램 스스로가 실행 흐름을 쪼개는 사용자 레벨 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 패키지(예: GNU [Pth](/knowledge-base/studynote/09_security/12_identity_threat_advanced/592_pth/), [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 자바의 그린 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))가 등장하게 되었다.

- **📢 섹션 요약 비유**: 은행에 손님(사용자 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))은 10명이나 찾아와서 자기들끼리 번호표를 뽑고 순서를 정하지만, 실제 창구 직원([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))은 단 1명밖에 없어 한 번에 한 명의 일만 처리할 수 있는 은행과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

이 모델의 내부는 사용자 공간의 스케줄러가 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 속이며 시분할을 구현하는 방식으로 작동한다.

```text
+--------------------------------------------------------------+
|                  다대일 모델의 아키텍처와 블로킹 한계                |
+--------------------------------------------------------------+
| [사용자 공간 (User Space)]                                     |
|   +------+   +------+   +------+                             |
|   | ULT 1|   | ULT 2|   | ULT 3|                             |
|   +--+---+   +--+---+   +--+---+                             |
|      +----------+----------+                                 |
|          [스레드 라이브러리 스케줄러]                             |
|                 | (모든 스위칭은 여기서 발생)                     |
| ----------------+------------------------------------------- |
| [커널 공간 (Kernel Space)]                                     |
|                 v                                            |
|            +---------+                                       |
|            |  KLT 1  | (단일 커널 스레드)                       |
|            +----+----+                                       |
|                 v                                            |
|             [CPU Core 0]   [CPU Core 1] (유휴 상태)            |
+--------------------------------------------------------------+
```

[스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 라이브러리는 TCB ([Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) Control Block)를 사용자 공간에 두고 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 상태를 자체적으로 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 및 복원한다. 문제는 하나의 ULT가 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 읽기와 같은 블로킹 시스템 콜 ([Blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) [System Call](/knowledge-base/studynote/02_operating_system/01_overview_architecture/013_system_call/))을 호출할 때다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 프로세스 안에 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 여러 개인지 모르기 때문에 KLT 자체를 대기 큐로 던져버린다. 결국 나머지 ULT들까지 모조리 실행 권한을 잃게 된다.

- **📢 섹션 요약 비유**: 40인승 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))에 승객(사용자 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))이 꽉 차 있는데, 단 한 명의 승객이 휴게소 화장실에 가버리면 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 기사는 그 한 명이 올 때까지 나머지 39명을 강제로 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 안에서 기다리게 만드는 것과 같습니다.

---

## Ⅲ. 비교 및 연결

멀티코어 환경이 대중화되면서, 다대일 모델과 [일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) ([One-to-One](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/)) 모델 간의 아키텍처적 한계 차이가 극명해진다.

| 비교 항목 | 다대일 (Many-to-One) 모델 | [일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) ([One-to-One](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/)) 모델 |
|:---|:---|:---|
| **매핑 구조** | 다수의 ULT ---> 1개의 KLT | 1개의 ULT ---> 1개의 KLT |
| <strong><a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/754_context_switch_cost/">문맥 교환 비용</a></strong> | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 진입이 없어 극도로 빠름 | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드 전환([트랩](/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/))으로 인해 오버헤드 큼 |
| **블로킹 영향** | 단일 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 블로킹 = 프로세스 전체 중단 | 개별 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)만 중단, 나머지 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 정상 실행 |
| **멀티코어 (Multi-core) 활용**| KLT가 1개이므로 코어를 1개만 사용 ([병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 불가) | 코어 수만큼 KLT가 분산되어 진정한 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 달성 |

[일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) 모델은 개발자가 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한 만큼 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 생겨 멀티코어의 성능을 전부 끌어내지만 오버헤드가 무겁다. 다대일 모델은 가볍지만 다차선 고속도로(멀티코어)를 두고도 1차선만 타는 구조적 한계를 안고 있다. 이러한 모순을 극복하기 위해 두 모델의 장점을 섞은 [다대다](/knowledge-base/studynote/02_operating_system/02_process_thread/100_many_to_many_model/) ([Many-to-Many](/knowledge-base/studynote/02_operating_system/02_process_thread/100_many_to_many_model/)) 모델이 파생되기도 하였다.

- **📢 섹션 요약 비유**: [일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) 모델은 직원 1명당 퀵보드 1대를 배정해 다 같이 고속도로를 달리는 것이고, 다대일 모델은 직원 100명이 퀵보드 1대에 번갈아 타려고 줄을 서서 1명만 도로를 달리는 것입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

현대 백엔드 아키텍처 설계 시 이 모델의 작동 방식을 아는 것은 병목 현상의 근본 원인을 진단하는 핵심이 된다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 및 실무 시나리오

1. **레거시 마이그레이션**: [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 자바 1.1의 그린 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) (Green [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))는 전형적인 다대일 모델이다. 이 환경에서 CPU 코어 수만 늘리는 스케일업([Scale-up](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/))은 무의미하다. JVM을 최신 네이티브 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 환경으로 교체해야 성능이 향상된다.
2. <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/">이벤트 루프</a> 기반 환경 검토</strong>: Node.js와 같은 [이벤트 루프](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/) 환경은 논리적으로 다대일 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)와 유사한 블로킹 약점을 지닌다. 단 하나의 긴 CPU 연산이 전체 시스템을 정지시키므로, 무거운 작업은 `Worker Threads` 패키지로 분리해야만 시스템 마비를 피할 수 있다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 다대일 환경이나 싱글 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [이벤트 루프](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/) 아키텍처에 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 I/O나 암호화 같은 동기적/블로킹 모듈을 결합하는 설계. 타임 슬라이스를 독점해 굶주림 ([Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/)) 현상을 유발하고 전체 서버를 먹통으로 만든다.

- **📢 섹션 요약 비유**: 수많은 소포를 처리할 때 단 한 명의 심사관(단일 코어 매핑)에게 복잡한 퍼즐 풀기(블로킹 작업)를 맡겨버리면, 뒤에 밀린 수만 개의 가벼운 소포들이 아예 컨베이어 벨트를 타지도 못하고 멈춰버리는 재앙이 발생합니다.

---

## Ⅴ. 기대효과 및 결론

OS 레벨의 다대일 모델은 멀티코어의 이점을 버리고 시스템콜 블로킹에 취약하다는 약점 때문에 역사 속으로 사라졌다. 하지만 "[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드 전환 없이 사용자 공간에서 실행 흐름을 통제한다"는 사상은 소프트웨어 공학에 지대한 유산을 남겼다.

다대일 모델의 한계를 극복하면서도 초경량 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)의 장점을 살린 개념은 Go 언어의 [고루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/) ([Goroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/)), 코틀린의 [코루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/) ([Coroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/)), 자바 21의 가상 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) (Virtual [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))로 진화하며 부활했다. 따라서 다대일 모델은 실패한 설계가 아니라, 현대 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 프로그래밍을 위한 필수적인 프로토타입으로 평가해야 한다.

- **📢 섹션 요약 비유**: 다대일 모델은 자전거 한 대에 여러 명이 올라타려던 무모한 서커스였지만, 그 '가벼운 안장' 아이디어는 오늘날 N차선 도로 위를 수만 대의 초소형 오토바이(가상 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))가 동시에 달리게 만드는 혁신적인 설계도로 재탄생했습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/">문맥 교환</a> (<a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/">Context Switch</a>)</strong> | 다대일 모델은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [트랩](/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/) 없이 사용자 공간의 TCB만 스와핑하여 이 비용을 극한으로 줄인다. |
| <strong>블로킹 시스템 콜 (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/">Blocking</a> <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/013_system_call/">System Call</a>)</strong> | KLT 하나를 멈춰버림으로써 다대일 모델을 붕괴시킨 가장 치명적인 아킬레스건 |
| <strong>그린 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a> (Green <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">Thread</a>)</strong> | JVM이 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 지원이 없는 OS 위에서 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)을 흉내 내기 위해 만든 사용자 공간 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/">코루틴</a> (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/">Coroutine</a>) / 가상 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a></strong> | 다대일 모델의 사용자 문맥 관리 철학을 계승하고 I/O 블로킹 한계를 비동기 런타임으로 극복한 현대적 구현 |

### 📈 관련 키워드 및 발전 흐름도

```text
순차적 프로세스 실행 (동시성 부재)
    |
    v
다대일 (Many-to-One) 스레드 모델 (초경량 동시성 획득, 블로킹 취약)
    |
    v
일대일 (One-to-One) 스레드 모델 (커널 스레드 매핑, 멀티코어 활용)
    |
    v
다대다 (Many-to-Many) 스레드 모델 (스레드 풀과 LWP 계층 도입)
    |
    v
언어 레벨의 코루틴 / 가상 스레드 (비동기 I/O 기반 다대다 진화)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 게임기 하나에 여러 명의 친구가 순서대로 버튼을 누르기로 약속했어요. 기계는 하나인데 친구들끼리 순서([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 관리)를 정하는 거죠.
2. 그런데 한 친구가 화장실을 간다며 기계를 일시정지(블로킹)시켜 버리면, 나머지 친구들은 아무것도 못 하고 마냥 기다려야 하는 문제가 생겨요.
3. 기계의 성능은 엄청 좋은데 줄을 하나만 서다 보니 너무 비효율적이라서, 요즘 컴퓨터는 무조건 줄을 여러 개 서게 만든답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 98 / 800

<- **이전**: [97. 커널 수준 스레드 (Kernel-level Thread) - OS가 직접 관리](/knowledge-base/studynote/02_operating_system/02_process_thread/097_kernel_level_thread/)
**다음**: [99. 일대일 (One-to-One) 스레드 모델](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) ->

---
