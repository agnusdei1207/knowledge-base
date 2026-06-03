+++
title = "693. 멀티스레드 유저모드 커널모드 (Multithread User Mode Kernel Mode)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 멀티스레드 환경에서 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 '누가 관리하느냐'에 따라, [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)가 유저 공간에서 스스로 관리하는 <strong>유저 수준 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a>(<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/096_user_level_thread/">User-level Thread</a>)</strong>와 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(OS)가 직접 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고 스케줄링하는 <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/097_kernel_level_thread/">커널 수준 스레드</a>(<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/097_kernel_level_thread/">Kernel-level Thread</a>)</strong>로 나뉜다.
> 2. <strong>유저 수준 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a>의 명암</strong>: [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 개입이 없어 스위칭 속도가 빛처럼 빠르지만(장점), OS 입장에서는 프로세스 전체가 1개의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)로 보이므로, [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 중 하나만 I/O를 호출해 블로킹(Sleep)되어도 <strong>프로세스 내의 모든 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a>가 통째로 멈춰버리는 치명적 단점</strong>이 있다.
> 3. <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/097_kernel_level_thread/">커널 수준 스레드</a>의 승리</strong>: [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 하나가 블로킹되어도 다른 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 멀쩡히 돌아가며, 멀티코어 CPU의 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성을 완벽하게 끌어다 쓸 수 있어 현대 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(Windows, Linux, Java [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))의 압도적 표준 모델(1:1 매핑)로 자리 잡았다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a> (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">Thread</a>)</strong>: 하나의 프로세스 내에서 실행되는 여러 작업의 흐름.
  - <strong>유저 수준 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a> (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/096_user_level_thread/">User-level Thread</a>)</strong>: OS가 모르게, 유저 스페이스의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)(예: [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) POSIX Threads, 그린 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))가 알아서 쪼개고 스케줄링하는 가짜 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/).
  - <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/097_kernel_level_thread/">커널 수준 스레드</a> (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/097_kernel_level_thread/">Kernel-level Thread</a>)</strong>: OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 존재를 100% 인지하고, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 스페이스에 TCB([Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) Control Block)를 두어 직접 스케줄링하는 진짜 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/).

- <strong>필요성 (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a>를 구현하는 두 가지 철학)</strong>: 
  - 초창기 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(MS-DOS 등)는 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)라는 개념 자체를 몰랐다. 하지만 개발자들은 하나의 앱 안에서 여러 일을 동시에 하고 싶었다.
  - **유저 레벨의 등장**: OS를 뜯어고칠 수 없으니, 유저 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 차원에서 타이머를 돌려 "가짜 [멀티태스킹](/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/)"을 구현했다. (하지만 I/O 병목으로 한계 직면)
  - <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 레벨의 등장</strong>: 하드웨어가 발전하고 멀티코어가 보급되면서, OS가 직접 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 관리해 주지 않으면 멀티코어를 100% 쓸 수 없게 되자, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 관리를 통째로 떠안게 되었다.

  - <strong>유저 수준 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a> (다단계 하청)</strong>: 건설 회사(OS)가 하청업체(프로세스)에 일감을 하나만 줬다. 하청 소장은 몰래 일꾼 10명(유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))을 고용해서 일을 쪼개 시킨다. 만약 일꾼 1명이 다쳐서 병원에 가면, 소장은 일을 멈추고 기다려야 하므로 나머지 9명도 강제로 놀게 된다.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/097_kernel_level_thread/">커널 수준 스레드</a> (정식 채용)</strong>: 건설 회사(OS)가 아예 처음부터 일꾼 10명([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))을 정식 직원으로 개별 계약했다. 1명이 다쳐서 병원에 가도, 회사는 나머지 9명에게 계속 일을 시킨다. 심지어 10명을 각기 다른 현장(멀티코어)에 동시에 투입할 수도 있다.

- **발전 과정**:
  1. <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/098_many_to_one_model/">다대일</a> (N:1)</strong>: 초창기 유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/). 여러 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 1개의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 감당. (I/O 병목으로 도태)
  2. <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/">일대일</a> (1:1)</strong>: 현대 OS의 표준. 유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 1개 만들면 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 1개가 무조건 매핑됨.
  3. <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/100_many_to_many_model/">다대다</a> (M:N)</strong>: 두 모델의 절충안이나 복잡성 때문에 사장됨.
  4. <strong>언어 레벨 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/">코루틴</a></strong>: OS의 1:1 무거움을 피해, 최근 Go([Goroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/))나 Kotlin에서 N:1 / M:N 철학을 현대적으로 재해석하여 부활.

- **📢 섹션 요약 비유**: 유저 수준 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 한 명의 신분증(PID)으로 10명이 클럽에 몰래 들어간 것이라, 한 명만 쫓겨나도 다 같이 쫓겨납니다. [커널 수준 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/097_kernel_level_thread/)는 10명 모두가 각자의 신분증(TCB)을 발급받아 떳떳하게 노는 것입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 매핑 모델 ([Mapping](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/) Models)

유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)와 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 어떻게 연결하느냐에 따라 아키텍처가 3가지로 나뉜다.

| 모델 명칭 | [다대일](/knowledge-base/studynote/02_operating_system/02_process_thread/098_many_to_one_model/) (N:1) | [일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) (1:1) | [다대다](/knowledge-base/studynote/02_operating_system/02_process_thread/100_many_to_many_model/) (M:N) |
|:---|:---|:---|:---|
| **설명** | 다수의 유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 1개의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)에 매핑 | 1개의 유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 1개의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)에 1:1 매핑 | 다수의 유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 다수의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)에 매핑 |
| **I/O 블로킹** | **한 놈이 막히면 프로세스 전체가 정지 (치명적)** | **한 놈이 막혀도 다른 놈은 생존** | 일부 막혀도 다른 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)로 우회 생존 |
| **멀티코어 활용**| 불가능 (어차피 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 눈엔 1개라 코어 1개만 씀) | <strong>완벽한 멀티코어 <a href="/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a> 처리 가능</strong> | 가능 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a>/문맥 비용</strong>| 극도로 빠르고 가벼움 (유저 모드 내에서 교체) | <strong>무거움 (<a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 진입 및 TCB 스위칭 발생)</strong> | 유연하지만 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 개발 난이도 극악 |
| **실제 사례** | 과거 Java Green Threads, GNU [Pth](/knowledge-base/studynote/09_security/12_identity_threat_advanced/592_pth/) | **현재 Linux (NPTL), Windows, Java** | 과거 Solaris, 현재 Go([Goroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/))의 사상 |

---

### [커널 수준 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/097_kernel_level_thread/)(1:1)의 오버헤드 메커니즘

현대 리눅스 환경에서 `pthread_create()`를 호출할 때 벌어지는 일이다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 일대일(1:1) 커널 수준 스레드 동작 원리                 │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  [User Space]                                                     │
  │   - 개발자가 `pthread_create()` 호출                               │
  │        │ (시스템 콜: clone() 실행)                                 │
  │  ======▼==========================================================│
  │  [Kernel Space (Ring 0)]                                          │
  │                                                                   │
  │   1. TCB (task_struct) 할당:                                      │
  │      커널이 완전히 새로운 [스레드 제어 블록(TCB)]을 생성한다.              │
  │                                                                   │
  │   2. 메모리(CR3) 공유 매핑:                                         │
  │      새로 만든 TCB의 메모리 포인터(Page Table)를 부모 프로세스의 것과      │
  │      100% 동일하게 덮어쓴다! (즉, 메모리 공간은 공유함)                  │
  │                                                                   │
  │   3. 커널 스케줄러 큐 진입:                                          │
  │      이 새 스레드는 부모와는 완전히 독립된 자격으로 Ready 큐에 등록된다.     │
  │      이제 커널은 부모 스레드를 Core 1에, 자식 스레드를 Core 2에           │
  │      동시에(Parallel) 밀어 넣을 수 있다.                              │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 리눅스는 프로세스와 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 내부적으로 엄격히 구분하지 않는다. 그냥 똑같이 `task_struct`(TCB/PCB) 구조체를 만들되, 메모리를 공유하게 묶어버리면(CLONE_VM) 그게 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 되는 것이다. 1:1 모델에서는 유저가 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 1만 개 띄우면, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 안에도 1만 개의 `task_struct`가 생겨 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리가 터져나가고 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 과부하에 걸린다. 이것이 바로 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 폭발([Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) Explosion)의 근본 원인이다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 자바(Java) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 모델의 변천사

언어의 런타임 환경이 OS와 어떻게 타협했는지 보여주는 가장 훌륭한 역사다.

1. <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> Java (Green Threads, N:1)</strong>:
   - 1990년대, OS마다 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 지원 여부가 달라서 자바는 JVM 안에서 스스로 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 관리하는 '그린 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)'를 썼다.
   - 단점: 솔라리스 서버의 코어가 16개인데도 자바가 1개 코어밖에 못 쓰는 비극이 발생했다. ([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 눈엔 JVM 프로세스 1개로 보임)
2. **현대 Java (Native Threads, 1:1)**:
   - 멀티코어가 대중화되자 자바는 그린 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 버리고, `Thread.start()`를 부르면 즉시 OS의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(`pthread`)를 1:1로 맵핑시키는 Native 모델로 완전히 돌아섰다. 완벽한 멀티코어 활용이 가능해졌다.
3. <strong>미래 Java (Virtual Threads, <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/042_relational_algebra_project/">Project</a> Loom, M:N)</strong>:
   - 1:1 모델은 너무 무거워서 수만 개의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 띄울 수 없었다(C10K 문제).
   - 최근 자바 21부터 도입된 가상 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(Virtual [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 100개(Carrier) 위에 수백만 개의 가상 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(User Level)를 띄워, 블로킹이 발생하면 JVM이 유저 레벨에서 다른 가상 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)로 갈아 끼워주는 <strong>M:N <a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/">멀티태스킹</a>의 궁극적 부활</strong>을 알렸다.

### 과목 융합 관점

- <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a> (OS)</strong>: [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 관점에서 보자. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 간의 스위칭은 유저 $\rightarrow$ [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 진입 $\rightarrow$ TCB 교체 $\rightarrow$ 유저로 돌아오는 수백 클럭이 소요된다. 반면 유저 수준 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 간의 스위칭은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드 진입([Trap](/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/)) 없이 단순히 유저 공간의 [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/)(`jmp`)로 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 포인터만 바꾸면 되므로 수십 클럭에 끝나는 압도적 속도를 자랑한다.
- <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 시스템 (Distributed)</strong>: 비동기 I/O(epoll) 기반의 [이벤트 루프](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/)(Node.js, Nginx)는 1개의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 위에서 수만 개의 I/O를 동시다발적으로 처리하므로, 굳이 무거운 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 여러 개 만들지 않고 유저 레벨 통제력만으로 고성능을 뽑아내는 아키텍처다.

- **📢 섹션 요약 비유**: 1:1 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 1인 1승용차 출퇴근이라면 쾌적하고 자유롭지만 도로(OS 메모리)가 꽉 막힙니다. M:N 모델이나 비동기 루프는 대형 버스에 사람(가상 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))을 수백 명 태워서 이동시키는 최신 대중교통 시스템과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — 레거시 C++ 멀티스레드 서버의 블로킹 락(Lag) 사태**: 유저 수준 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)(Coroutines)로 자체 구현한 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 시스템을 쓰다가, 어떤 루틴에서 `fsync()` (디스크 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/))라는 블로킹 시스템 콜을 호출했다.
   - **원인 분석**: 유저 수준 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 입장에서는 그냥 1개의 프로세스다. 하나의 유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 `fsync`를 호출해 OS가 "너 디스크 쓸 때까지 기다려(Sleep)" 하고 그 프로세스를 정지시키면, [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)조차 같이 멈춰버려 다른 유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 10만 개가 모두 멈춰버린다.
   - **대응 (기술사적 가이드)**: 유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)([코루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/)) 환경에서는 <strong>절대 동기식(<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/">Blocking</a>) 시스템 콜을 호출하면 안 된다</strong>. 반드시 `O_NONBLOCK` 플래그나 비동기 I/O(AIO, [io_uring](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/464_io_uring/))를 사용해야 하며, 부득이하게 블로킹이 필요한 로직은 별도의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)([Thread Pool](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/))로 격리하여 던져버려야([Offloading](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)) 메인 [코루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/) 루프가 죽지 않는다.

2. <strong>시나리오 — K8s/클라우드 환경의 CPU Throttling (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a> 과다 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a>)</strong>: 컨테이너에 CPU `1 Core` 리밋을 줬는데, 자바 톰캣 서버에서 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(`Thread.start()`)를 500개 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)했다. 애플리케이션 응답 속도가 박살 남.
   - **원인 분석**: [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 500개 만들면 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 CFS [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 이 500개를 번갈아 가며 디스패치한다. CPU 리밋이 1코어밖에 안 되는데 500개의 TCB를 교체하느라 '[Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 폭풍'이 발생하여 실제 연산은 못 하고 OS 스위칭 오버헤드로 할당된 CPU 퀀텀을 다 깎아 먹은 것이다.
   - **아키텍처 적용**: [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 코어 개수에 맞게 최소화(예: 코어 x 2배)하는 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)을 유지해야 한다. 동시에 1만 개의 트래픽을 처리해야 한다면 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)에 의존하지 말고, 언어 단에서 제공하는 경량 유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)([Goroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/), Java Virtual [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))로 전환하여 스케줄링 오버헤드를 유저 스페이스로 떠넘겨야 한다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 애플리케이션 스레드 아키텍처 (런타임) 선택 플로우            │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [새로운 초대용량 동시 접속(100K+) 서버 프레임워크 언어 선정]               │
  │                │                                                  │
  │                ▼                                                  │
  │      사용자의 요청당 1개의 OS 커널 스레드를 1:1로 할당하는 구조인가?         │
  │      (예: 전통적인 Java Thread, C++ std::thread)                  │
  │          ├─ 예 ─────▶ [메모리 및 컨텍스트 스위치 오버헤드로 서버 붕괴 위험]  │
  │          │            대책: 스레드 풀(Thread Pool) 크기를 엄격히 제한하고, │
  │          │                  초과 요청은 큐(Queue)에 대기시킴.             │
  │          └─ 아니오 (비동기 처리나 경량 스레드를 쓴다)                       │
  │                │                                                  │
  │                ▼                                                  │
  │      개발자가 비동기(Callback, Promise) 코드를 짜기 어려워하는가?           │
  │          ├─ 예 ─────▶ [Go(Goroutine) 또는 Java 21(Virtual Thread) 채택]│
  │          │            개발자는 동기식(1:1)처럼 쉽게 코드를 짜고, 런타임이 알아서│
  │          │            M:N 유저 레벨 스케줄링으로 커널 스위칭 오버헤드를 없애줌.│
  │          │                                                        │
  │          └─ 아니오 ──▶ Node.js, Rust Tokio 등 완벽한 비동기 I/O 채택       │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** "[스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 공짜가 아니다." OS가 만들어주는 1:1 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 메모리 1MB와 무거운 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 스위칭 비용을 청구한다. 과거에는 하드웨어 스펙으로 이를 버텼지만, 현재의 클라우드 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 환경에서는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 덜어내고 런타임 언어(유저 스페이스)가 자체적으로 M:N 스케줄링을 해주는 언어(Go, [Erlang](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1004_erlang_traffic_load_unit_calculation/), 최신 Java)를 고르는 것이 곧 아키텍처의 승리다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong>User <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">Thread</a> 패닉 방어</strong>: 파이썬(`gevent`)이나 Go 언어로 유저 수준 스레딩을 할 때, [서드파티](/knowledge-base/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) C [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)(예: 이미지 처리)를 호출하면 그 C 코드가 블로킹일 경우 프로세스 전체가 죽는다. [서드파티](/knowledge-base/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)의 블로킹 여부를 반드시 검증하고 비동기 래퍼(Wrapper)를 씌웠는가?

- **📢 섹션 요약 비유**: OS([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))에게 모든 걸 맡기면 안전하지만 비쌉니다(1:1 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)). 반대로 내(유저 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/))가 다 알아서 하면 싸고 빠르지만, 한 번 실수하면 회사 전체가 망합니다(유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 블로킹). 이 둘을 융합한 최신 언어(M:N 가상 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))들이 현대 백엔드의 진정한 승자입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 유저 수준 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) (순수 N:1) | [커널 수준 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/097_kernel_level_thread/) (순수 1:1) | M:N 하이브리드 ([Goroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/) 등) |
|:---|:---|:---|:---|
| **멀티코어 활용** | 전혀 불가능 (1개 코어만 씀) | <strong>완벽한 <a href="/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>(Parallel) 처리</strong> | <strong>완벽한 <a href="/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a> 처리</strong> |
| **블로킹(I/O) 영향**| 프로세스 전체 먹통 (치명적) | 해당 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)만 멈춤 (안전함) | 해당 유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)만 다른 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)로 우회 (완벽) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/">문맥 교환</a> 속도</strong> | <strong>수십 나노초 (<a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/">초고속</a>)</strong> | 수 마이크로초 (무거움) | <strong>수십 나노초 (<a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/">초고속</a>)</strong> |
| <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a> 한계수</strong> | 수백만 개 가능 (가벼움) | 수천 개 한계 (C10K 병목) | 수백만 개 가능 (C10M 돌파) |

### 미래 전망
- <strong>OS <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a>의 역할 축소</strong>: 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 개발자들은 "더 이상 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에서 수만 개의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 관리하는 것은 미친 짓"이라고 인정하고 있다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 물리 CPU 코어 개수(예: 16개)만큼만 띄워두고, 실제 수십만 개의 마이크로 작업들은 User Space의 런타임(Envoy, JVM, Go 런타임)이 `io_uring` 위에서 자체적으로 쪼개고 스케줄링하는 유저/[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 완벽한 분업 시대로 나아가고 있다.

### 결론
유저 모드 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)와 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 발전사는, "무거운 작업의 책임을 누가 질 것인가?"에 대한 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)와 프로그래밍 언어 간의 밀당의 역사다. [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)엔 OS가 무능해서 유저가 책임을 졌고(유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)), OS가 강력해지자 OS에게 모든 걸 떠넘겼지만([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)), 트래픽이 폭발하는 클라우드 시대가 오자 OS마저 지쳐 쓰러지며 다시 유저 공간의 똑똑한 런타임(가상 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))에게 왕관을 돌려주는 나선형 진화를 보여준다. 아키텍트는 자신이 다루는 언어와 프레임워크가 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 힘을 어떻게 빌려다 쓰는지 그 밑바닥([Mapping](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/) Model)을 명확히 투시할 줄 알아야 한다.

- **📢 섹션 요약 비유**: 처음엔 직원들(유저 앱)끼리 주먹구구로 일하다가(유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)), 나라(OS)가 모든 것을 통제하는 공산주의([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 1:1)로 발전했습니다. 하지만 국가 행정력이 마비되자, 다시 민간 기업(언어 런타임)에게 권한을 주되 국가는 인프라(멀티코어)만 제공하는 세련된 자본주의(M:N 모델)로 진화한 것입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [다단계 피드백 큐](/knowledge-base/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/) ([MLFQ](/knowledge-base/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/)) 천이 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [HRN](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/187_hrn_scheduling/) 대기 시간 공식 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [스레드 로컬 스토리지](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) ([TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) [상호 배제](/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[HRN 대기 시간 공식]
    │
    ▼
[멀티스레드 유저모드 커널모드 (Multithread User Mode Kernel Mode)]
    │
    ├──▶ [스레드 로컬 스토리지 (TLS)]
    └──▶ [스레드 동기화 상호 배제]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. '유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)'는 학생들끼리 몰래 짠 조별 과제예요. 선생님(OS)은 이 조에 1명만 있는 줄 알죠. 그래서 조원 한 명이 화장실에 가면 조 전체의 발표가 멈춰버려요(치명적 단점).
2. '[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)'는 선생님이 직접 조원 10명을 다 확인하고 각자에게 임무를 준 거예요. 한 명이 화장실 가도 나머지 9명은 멀쩡히 발표를 계속할 수 있죠!
3. 요즘 최신 컴퓨터(Go, Java 21)는 '하이브리드 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)'를 써요. 선생님이 2명만 확인했는데, 사실 그 2명 뒤에 100명의 미니 로봇들이 숨어서 엄청나게 빠른 속도로 번갈아 가며 과제를 해치우는 완벽한 마술을 부린답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 693 / 800

← **이전**: [692. HRN 대기 시간 공식 (Hrn Highest Response Ratio Next)](/knowledge-base/studynote/02_operating_system/11_exam_summary/692_hrn_highest_response_ratio_next/)
**다음**: [694. 스레드 로컬 스토리지 (TLS)](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) →

---
