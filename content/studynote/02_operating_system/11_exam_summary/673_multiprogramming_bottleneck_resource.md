+++
title = "673. 다중 프로그래밍 (Multiprogramming) 한계 자원"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 다중 프로그래밍(Multiprogramming)은 디스크(I/O) 대기 시간 동안 CPU가 노는 것을 막기 위해, 메모리에 여러 개의 프로그램(Job)을 동시에 올려놓고 번갈아 가며 실행시켜 <strong>CPU 활용률(Utilization)</strong>을 극대화하는 1960년대의 혁명적 OS 아키텍처다.
> 2. **한계 자원 (메모리와 디스크)**: CPU를 쉬지 않게 하려면 메모리에 프로그램을 최대한 많이 올려야([다중 프로그래밍 정도](/knowledge-base/studynote/02_operating_system/04_synchronization/258_degree_of_multiprogramming/) 상승) 하지만, 물리적 램(RAM)의 크기 제한이라는 치명적 <strong>한계 자원(<a href="/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/">Bottleneck</a> Resource)</strong>에 부딪히게 된다.
> 3. **가치/진화**: 이 메모리 한계를 극복하기 위해 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 램의 일부만 사용해 프로그램을 돌리는 <strong><a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/">가상 메모리</a>(<a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/">Virtual Memory</a>)</strong>와 [스와핑](/knowledge-base/studynote/02_operating_system/06_memory_management/335_swapping/)([Swapping](/knowledge-base/studynote/02_operating_system/06_memory_management/335_swapping/)) 기술을 발명하게 되었으며, 이는 현대 모든 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 메모리 관리의 근원이 되었다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **Uniprogramming (단일 프로그래밍)**: 한 번에 오직 하나의 프로그램만 메모리에 올려 실행하는 방식 (예: MS-DOS).
  - **Multiprogramming (다중 프로그래밍)**: 메모리에 2개 이상의 프로그램을 동시에 올려두고, 하나의 프로그램이 입출력(I/O)을 하느라 멈출 때 OS가 즉시 다른 프로그램에게 CPU를 넘겨주는 방식.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/258_degree_of_multiprogramming/">Degree of Multiprogramming</a> (<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/258_degree_of_multiprogramming/">다중 프로그래밍 정도</a>)</strong>: 현재 메인 메모리에 올라가 있는 프로세스의 총개수.

- **필요성 (CPU와 I/O 장치의 극단적 속도 차이)**: 
  - 컴퓨터의 연산(CPU) 속도는 엄청나게 빠른데, 프린터를 뽑거나 디스크를 읽는 속도(I/O)는 달팽이처럼 느렸다.
  - 단일 프로그래밍 시절, 프로그램 1개가 디스크에서 데이터를 읽어오는 1초 동안 CPU는 수십억 번의 연산을 할 수 있음에도 그냥 멍하니 쉬어야 했다 (CPU 유휴 상태).
  - **해결책**: "CPU가 놀게 놔둘 수 없다! 1번 프로그램이 디스크를 읽으러 가면, 그 틈에 메모리에 대기 중이던 2번 프로그램을 CPU가 실행하게 만들자!"라는 경제적 극대화 논리가 다중 프로그래밍을 낳았다.

  - **단일 프로그래밍**: 의사 1명이 환자 1명을 진료한다. 환자가 엑스레이를 찍으러 30분 동안 자리를 비우면, 의사는 빈 진료실에서 30분 동안 유튜브를 보며 쉰다. (비효율의 극치)
  - **다중 프로그래밍**: 의사(CPU) 진료실(메모리)에 베드를 5개 놓고 환자 5명을 눕힌다. 1번 환자가 피를 뽑느라 대기하는(I/O) 찰나에, 의사는 즉시 옆 베드로 가서 2번 환자를 진찰한다. 의사는 단 1초도 쉬지 못한다.

- **발전 과정**:
  1. <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/">배치 처리</a> (<a href="/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a>)</strong>: 테이프에서 하나씩 순서대로 읽어서 실행. CPU가 빔.
  2. <strong>오프라인 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/457_spooling/">스풀링</a></strong>: I/O 전담 보조 컴퓨터 도입.
  3. **다중 프로그래밍 (OS/360)**: 메모리 파티셔닝을 통해 여러 Job을 동시 적재. 스케줄링(Scheduling) 개념의 탄생.

- **📢 섹션 요약 비유**: 세상에서 제일 비싼 장비인 CPU를 절대 놀리지 않기 위해, 작업(Job)들을 메모리라는 대기실에 꽉꽉 채워 넣고 쉴 새 없이 돌려막기를 하는 악덕 공장장(OS)의 효율화 전략입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 다중 프로그래밍의 수학적 효과 (CPU 활용률)

다중 프로그래밍이 CPU 활용률(Utilization)에 미치는 영향을 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)적으로 계산해 보자.

- 어떤 프로세스가 실행 시간 중 <strong>I/O를 대기하는 시간의 비율(p)</strong>이 80% ($p=0.8$)라고 가정하자.
- 단일 프로그래밍(메모리에 1개): CPU 활용률 = $1 - p = 1 - 0.8 = 0.2$ (20%만 일하고 80%는 놂)
- [다중 프로그래밍 정도](/knowledge-base/studynote/02_operating_system/04_synchronization/258_degree_of_multiprogramming/)가 $N$일 때, <strong>모든 프로세스가 동시에 I/O를 기다릴 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/">확률</a>(CPU가 놀게 될 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/">확률</a>)</strong>은 $p^N$ 이다.
- **CPU 활용률 공식 = $1 - p^N$**

| N (메모리에 올라간 프로세스 수) | CPU 활용률 계산식 ($1 - 0.8^N$) | 실제 활용률 |
|:---:|:---|:---:|
| 1개 | $1 - 0.8^1$ | **20.0%** |
| 2개 | $1 - 0.8^2$ | **36.0%** |
| 5개 | $1 - 0.8^5$ | **67.2%** |
| 10개 | $1 - 0.8^{[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)}$ | **89.2%** |

결론: 메모리에 프로세스를 10개 올려두면, CPU가 90%의 시간 동안 쉬지 않고 일하게 되어 컴퓨터의 효율이 4.5배나 증가한다.

---

### 한계 자원 ([Bottleneck](/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/) Resource)의 발생: 메모리(RAM)

위의 공식대로라면 N을 100개, 1,000개로 무한히 늘리면 CPU 효율이 99.99%가 되어 완벽해진다. 하지만 여기에는 치명적인 물리적 장벽이 존재한다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 다중 프로그래밍 정도(Degree)와 한계 자원 충돌            │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  [CPU 활용률을 높이려면 N을 늘려야 한다]                                 │
  │   - 프로세스 1개당 필요한 메모리 공간이 1GB라고 가정.                      │
  │                                                                   │
  │  [상황: 물리 메모리(RAM)가 총 4GB인 컴퓨터]                              │
  │   [ RAM 4GB ]                                                     │
  │   ┌───────────────┐                                               │
  │   │  OS Kernel    │ (500MB)                                       │
  │   ├───────────────┤                                               │
  │   │  Process 1    │ (1GB)                                         │
  │   ├───────────────┤                                               │
  │   │  Process 2    │ (1GB)                                         │
  │   ├───────────────┤                                               │
  │   │  Process 3    │ (1GB)                                         │
  │   └───────────────┘                                               │
  │   남은 공간: 500MB (더 이상 새로운 프로세스를 올릴 수 없음!)                 │
  │                                                                   │
  │  [결과: 한계 자원 도달]                                               │
  │   - CPU는 아직 40%나 팽팽 놀고 있는데(I/O 대기 중),                     │
  │     [물리 메모리]라는 병목(Bottleneck) 때문에 더 이상 N을 늘릴 수 없다.       │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** CPU [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 100% 다 뽑아먹고 싶은데, <strong>메모리(RAM)의 크기 제한</strong>이 그 발목을 잡는다. 다중 프로그래밍의 궁극적인 한계 자원([Bottleneck](/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/) Resource)은 언제나 메모리였다. 이 한계를 부수기 위해 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 학자들은 "어차피 프로세스 1GB 중에 지금 당장 실행에 필요한 코드는 10MB밖에 안 되잖아? 당장 안 쓰는 990MB는 디스크(Swap)에 던져두고 10MB씩만 메모리에 올리자!"라는 기상천외한 아이디어를 내놓았다. 이것이 바로 <strong><a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/">가상 메모리</a>(<a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/">Virtual Memory</a>)</strong>와 <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/">페이징</a>(<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/">Paging</a>)</strong> 기술의 탄생 배경이다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 다중 프로그래밍 vs 다중 처리 vs 다중 작업

용어가 헷갈리기 쉬우나, 아키텍처적 초점이 완전히 다르다.

| 용어 (영문) | 핵심 목적 및 특징 | 필수 하드웨어 |
|:---|:---|:---|
| **다중 프로그래밍 (Multiprogramming)** | I/O 대기 시간에 CPU를 안 놀게 함 ([CPU Utilization](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/171_cpu_utilization_throughput/) 극대화) | 1개의 CPU, 넉넉한 RAM |
| **다중 처리 (Multiprocessing)** | 여러 개의 CPU(Core)가 진짜로 동시에(Parallel) 여러 일을 함 | **2개 이상의 CPU (멀티코어)** |
| <strong>다중 작업 (<a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/">Multitasking</a> / 시분할)</strong> | I/O 대기가 없어도, 시간을 쪼개서(Time-quantum) 번갈아 실행 | 타이머 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 장치 |

현대의 스마트폰이나 PC는 이 세 가지(다중 프로그래밍 + 다중 처리 + 시분할)가 모두 결합되어 있는 궁극의 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)다.

### 과목 융합 관점

- <strong>컴퓨터구조 (<a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/">CA</a>)</strong>: 다중 프로그래밍을 위해 메모리에 여러 앱을 동시에 올리면, A 앱이 B 앱의 메모리를 훔쳐보거나 덮어쓰는 대형 보안 사고가 터진다. 이를 막기 위해 CPU 하드웨어 단에서 <strong>Base &amp; <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/330_limit_register/">Limit Register</a> (<a href="/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/307_memory_protection/">메모리 보호</a> <a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/">레지스터</a>)</strong>가 도입되었고, 이는 후일 [MMU](/knowledge-base/studynote/02_operating_system/06_memory_management/328_mmu/)(메모리 관리 유닛)로 발전한다.
- **소프트웨어공학 (SE)**: 다중 프로그래밍이 등장하면서, 여러 프로그램이 동일한 프린터나 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(공유 자원)에 동시에 접근하려다 시스템이 멈추는 [교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)([Deadlock](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/))나 [경쟁 조건](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/)([Race Condition](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/))이라는 부작용이 최초로 발생했다. 즉, 다중 프로그래밍은 '[동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 제어([Concurrency Control](/knowledge-base/studynote/05_database/04_transactions_concurrency/508_concurrency_control/))'라는 소프트웨어 공학의 거대한 숙제를 낳은 판도라의 상자였다.

- **📢 섹션 요약 비유**: 다중 프로그래밍은 좁은 무대(메모리)에 여러 배우를 억지로 구겨 넣고 연극을 시킨 것입니다. 배우들이 대기 시간 없이 일하게 되어 효율은 올랐지만, 서로 어깨를 부딪히고(메모리 침범) 소품을 뺏으려 싸우는([교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)) 새로운 골칫거리들을 만들어 냈습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a> 폭발(<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">Thread</a> Explosion)과 메모리 한계 자원 고갈</strong>: Tomcat 웹 서버([스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/) 모델)에 동시 접속자가 1만 명이 들어왔다. 요청마다 1개의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 생성하여 [다중 프로그래밍 정도](/knowledge-base/studynote/02_operating_system/04_synchronization/258_degree_of_multiprogramming/)(N)를 1만 개로 높였더니, 시스템 메모리(RAM)가 100% 꽉 차버리고 서버가 [스와핑](/knowledge-base/studynote/02_operating_system/06_memory_management/335_swapping/) 늪([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))에 빠져 죽었다.
   - **원인 분석**: [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 1개당 할당되는 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 메모리(기본 1MB)만 해도 1만 개면 10GB다. CPU는 20%밖에 안 쓰는데 메모리(한계 자원)가 먼저 고갈된 전형적인 다중 프로그래밍의 병목이다.
   - **아키텍처 대응 (Event-driven)**: Nginx, Node.js, Redis처럼 1개의 메인 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(Single [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))가 `epoll/kqueue` 같은 비동기 I/O를 활용하는 <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/538_event_driven_architecture_eda/">이벤트 기반 아키텍처</a></strong>로 전환해야 한다. 이렇게 하면 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 메모리를 낭비하지 않고도 수만 개의 동시 I/O(C10K 문제)를 CPU 유휴 시간 없이 완벽하게 처리할 수 있다.

2. <strong>시나리오 — 클라우드 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a>(<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/">Out of Memory</a>)과 과도한 오버커밋</strong>: [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)(K8s) 워커 노드(16코어, 32GB RAM)에 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))를 스케줄링할 때, CPU 사용률을 80% 이상으로 끌어올리려고 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 50개 욱여넣었다. CPU는 50%인데 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)들이 메모리 제한을 초과하며 줄줄이 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬(Kill)을 당함.
   - **원인 분석**: CPU 자원(Compressible)은 다중 프로그래밍으로 어떻게든 시분할을 쪼개서 쓸 수 있지만, 메모리 자원(Incompressible)은 물리적으로 쪼갤 수 없는 한계 자원이기 때문에 발생한 설계 오류다.
   - **기술사적 판단**: 클라우드 인프라 설계 시 서버의 스펙을 정할 때, CPU 연산 위주의 워크로드(C-Type 인스턴스)인지 메모리 적재 위주의 워크로드(R/M-Type 인스턴스)인지를 명확히 구분해야 한다. 메모리 한계 자원에 도달하는 워크로드는 아무리 CPU를 쪼개봐야 시스템 붕괴만 낳는다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 시스템 병목(Bottleneck) 식별 및 아키텍처 튜닝 플로우        │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [서버 성능 모니터링: 처리량(Throughput)이 더 이상 오르지 않음]              │
  │                │                                                  │
  │                ▼                                                  │
  │      CPU 사용률은 20~30%로 낮은데, 디스크 I/O 대기(Wait)가 높은가?        │
  │          ├─ 예 ─────▶ [I/O 병목 상태]                               │
  │          │            대책 1: 다중 프로그래밍 정도(스레드 풀 크기)를 늘려서   │
  │          │                   CPU를 더 일하게 만든다.                  │
  │          │            대책 2: 디스크를 HDD에서 NVMe SSD로 교체한다.      │
  │          └─ 아니오                                                │
  │                │                                                  │
  │                ▼                                                  │
  │      스레드 풀이나 파드를 늘렸더니, CPU는 여전히 낮은데 메모리가 고갈(OOM)되는가?│
  │          ├─ 예 ─────▶ [메모리 한계 자원(Memory Bottleneck) 봉착]      │
  │          │            대책: 스케일 업(RAM 증설) 또는 비동기(Event-loop)  │
  │          │                  논블로킹 I/O 아키텍처로 전면 개편             │
  │          │                                                        │
  │          └─ 아니오 ──▶ 시스템 콜 락(Lock) 경합 또는 네트워크 대역폭 병목 의심│
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** "CPU가 남으니까 프로그램을 더 돌리자"는 다중 프로그래밍의 1차원적 공식은 현대 시스템에서 먹히지 않는다. 프로그램을 더 올리는 순간, [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/) 오버헤드와 캐시 미스(Cache Miss), 그리고 메모리 [스와핑](/knowledge-base/studynote/02_operating_system/06_memory_management/335_swapping/)([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))이 동시에 폭발하며 시스템이 역으로 느려지는 임계점(Knee Point)이 존재하기 때문이다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **I/O Bound vs CPU Bound 분리**: 백그라운드에서 도는 배치 시스템 내에, 100% CPU만 쓰는 연산(CPU Bound)과 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)/DB만 기다리는 연산(I/O Bound)을 완벽히 분리(Decoupling)하여 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)을 다르게 가져가고 있는가? (다중 프로그래밍 효율 극대화의 기본)
- <strong><a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/">가상 메모리</a> 한계 (<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/">Thrashing</a>) 모니터링</strong>: N을 늘리다가 물리 메모리를 초과하여 [스와핑](/knowledge-base/studynote/02_operating_system/06_memory_management/335_swapping/)이 발생하면, OS가 디스크에서 페이지를 넣고 빼느라 CPU가 100%를 치는데 정작 유효한 연산은 하나도 못하는 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))에 빠졌는지 감시([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 횟수)하고 있는가?

- **📢 섹션 요약 비유**: 숟가락(CPU)이 남는다고 무작정 손님(다중 프로그래밍)을 식당에 더 밀어 넣으면, 의자(메모리)가 모자라서 손님들이 서서 밥을 먹다 결국 식당 전체가 아수라장([스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))이 됩니다. 의자 개수를 먼저 세는 것이 시스템 운영의 기본입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | Uniprogramming (단일 프로그래밍) | Multiprogramming (다중 프로그래밍) | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (CPU 활용률)**| [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~20% (나머지는 I/O 대기) | **80~90% 이상 유지** | 하드웨어 투자 대비 극강의 [ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/) 달성 |
| <strong>정량 (<a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a>)</strong> | 시간당 10개 작업 처리 | **시간당 50~100개 작업 처리** | 시스템 전체의 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)) 대폭 증가 |
| **정성 (자원 관리)**| 메모리 1개만 관리하면 됨 | [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/), [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 기법 등 필요 | 현대 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 복잡한 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 기술 진화를 촉발 |

### 미래 전망
- <strong>거대 <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 모델의 다중 프로그래밍 (<a href="/knowledge-base/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/">Multi-Tenancy</a> in <a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/">GPU</a>)</strong>: CPU에서 일어났던 다중 프로그래밍 혁명이 현재 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)(VRAM)에서 똑같이 재현되고 있다. [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 1대에 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델 1개만 띄우면 VRAM(메모리)은 모자란데 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 연산기([CUDA](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/420_cuda/) 코어)는 팽팽 논다. 이를 해결하기 위해 엔비디아(MIG)나 최신 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 기술을 통해 하나의 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 램에 여러 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델(Tenant)을 동시에 올려 빈틈없이 돌리는 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 다중 프로그래밍 기술이 클라우드 사업의 넥스트 격전지가 되었다.
- <strong>메모리 한계 극복 (<a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/">CXL</a>)</strong>: 영원한 한계 자원이었던 물리적 메모리의 용량 제한을 부수기 위해, [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)([Compute Express Link](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)) 기술을 통해 네트워크 너머에 있는 거대한 [메모리 풀](/knowledge-base/studynote/02_operating_system/06_memory_management/369_memory_pool/)(Pool)을 끌어와서 논리적으로 내 램처럼 쓰는 차세대 아키텍처가 상용화되고 있다.

### 결론
다중 프로그래밍(Multiprogramming)은 비싼 쇳덩어리(CPU)를 어떻게든 혹사시키기 위한 자본주의적 경제 논리에서 출발한 개념이다. 이 단순한 "남는 시간에 다른 거 하자"는 아이디어는, 멀티프로세스 환경, 스케줄링 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/), 메모리 격리, 그리고 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)라는 현대 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 모든 핵심 뼈대를 강제로 잉태시켰다. 다중 프로그래밍의 역사를 이해하는 것은, 오늘날 왜 서버 아키텍처가 비동기/이벤트 루프와 마이크로서비스로 찢어지게 되었는지, 그리고 메모리 최적화가 왜 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝의 전부인지 그 필연성을 깨닫는 과정이다.

- **📢 섹션 요약 비유**: 1명이 살던 단독주택(단일 프로그래밍)을 허물고 100명이 사는 아파트(다중 프로그래밍)를 지었더니, 층간 소음([메모리 보호](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/307_memory_protection/))과 엘리베이터 정체(스케줄링)라는 새로운 문제가 생겼고, 이를 해결하며 건축 기술([운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))이 비약적으로 발전한 것입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 시스템 프로그램과 응용 프로그램의 차이 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [일괄 처리 시스템](/knowledge-base/studynote/02_operating_system/11_exam_summary/672_batch_processing_system_metrics/) ([Batch Processing System](/knowledge-base/studynote/02_operating_system/11_exam_summary/672_batch_processing_system_metrics/)) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 지표 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [시분할 시스템](/knowledge-base/studynote/02_operating_system/01_overview_architecture/003_time_sharing_system/) [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 최적화 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [멀티태스킹](/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/) ([Multitasking](/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/)) 용어 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[일괄 처리 시스템 (Batch Processing System) 성능 지표]
    │
    ▼
[다중 프로그래밍 (Multiprogramming) 한계 자원]
    │
    ├──▶ [시분할 시스템 응답 시간 최적화]
    └──▶ [멀티태스킹 (Multitasking) 용어]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 의사 선생님(CPU)이 환자를 진찰하는데, 환자가 엑스레이(디스크 I/O)를 찍으러 10분 동안 자리를 비우면 의사 선생님도 10분 동안 멍때리며 쉬어야 해요.
2. 그래서 병원에 침대(메모리)를 5개 놔두고 환자 5명(다중 프로그래밍)을 동시에 받았어요! 1번 환자가 엑스레이 찍으러 가면, 그사이에 바로 2번 환자를 진찰해서 선생님이 1초도 못 쉬게 만들었죠.
3. 그런데 침대(한계 자원인 메모리)를 놓을 방이 너무 작아서 환자를 10명, 20명 무한정 받을 수는 없다는 게 이 시스템의 가장 큰 고민거리랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 673 / 800

← **이전**: [672. 일괄 처리 시스템 (Batch Processing System) 성능 지표](/knowledge-base/studynote/02_operating_system/11_exam_summary/672_batch_processing_system_metrics/)
**다음**: [674. 시분할 시스템 응답 시간 최적화 (Time Sharing Response Time Optimization)](/knowledge-base/studynote/02_operating_system/11_exam_summary/674_time_sharing_response_time_optimization/) →

---
