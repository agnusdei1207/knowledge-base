+++
title = "97. 커널 수준 스레드 (Kernel-level Thread) - OS가 직접 관리"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수준 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) (Kernel-level [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/), KLT)는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 직접 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 스케줄링, 소멸을 관리하며 TCB ([Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) Control Block)를 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 공간에 유지하는 실행 단위이다.
> 2. **가치**: 특정 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 I/O 블로킹 상태에 빠져도 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 이를 개별적으로 인지하므로, 프로세스 내 다른 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 다른 CPU 코어에 할당해 중단 없는 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)과 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 연산을 보장한다.
> 3. **판단 포인트**: KLT는 안정성과 멀티코어 활용 능력이 뛰어나지만, [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)) 시 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 개입에 따른 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 오버헤드가 발생하므로 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)([Thread Pool](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)) 크기를 물리 코어에 맞춰 제한해야 한다.

---

## Ⅰ. 개요 및 필요성

[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수준 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) (KLT, Kernel-Level [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))는 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 존재를 직접 인식하고 1:1 매핑 기반으로 관리하는 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 모델이다. 사용자가 애플리케이션에서 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하면, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 내부적으로도 이에 대응하는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 객체가 만들어진다.

이 구조는 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [사용자 수준 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/096_user_level_thread/)(ULT)의 치명적 결함을 해결하기 위해 등장했다. ULT 환경에서는 하나의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 디스크 읽기 등으로 블로킹(Block)되면, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 프로세스 전체가 멈춘 것으로 오인해 나머지 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)까지 전부 중단시켰다. 게다가 코어가 여러 개인 다중 처리기([SMP](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/195_real_time_scheduling/)) 환경에서도 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 구별하지 못해 여러 코어에 연산을 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)할 수 없었다. 이 병목을 타개하고 하드웨어 자원을 극한으로 활용하기 위해 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 직접 통제하는 아키텍처가 필요해졌다.

- **📢 섹션 요약 비유**: 회사(프로세스)의 모든 직원([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))이 국가([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))에 직접 정규직으로 등록된 상태다. 한 직원이 병가를 내더라도, 국가가 다른 직원들은 정상 출근시켜 회사가 계속 굴러가도록 보장해 준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수준 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 모델은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 공간 내부에 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 상태를 저장하는 TCB 구조를 개별적으로 유지한다. 사용자 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 하나당 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 하나가 바인딩되는 [일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/)(1:1) 구조가 현대 OS의 표준이다.

| 구성 요소 | 역할 | 실무 메커니즘 |
| :--- | :--- | :--- |
| <strong>TCB (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">Thread</a> Control Block)</strong> | 상태 저장 | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리 안에 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/), [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/), [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 정보 보관 (메모리 소모) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/013_system_call/">System Call</a> <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a></strong> | [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 및 통제 | [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 관리를 위해 유저 모드에서 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드로 진입 (Overhead) |
| <strong>OS <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/">스케줄러</a></strong> | CPU 자원 분배 | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 큐를 검사하여 각 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)에 물리적 코어 독립 할당 |

[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 1:1 매핑 구조와 블로킹 격리 원리를 시각화한다.

```text
┌──────────────────────────────────────────────────────────────┐
│           커널 수준 스레드 (KLT) 1:1 매핑 모델 아키텍처           │
├──────────────────────────────────────────────────────────────┤
│  [ 사용자 영역 (User Space) ]                                │
│  ┌──────────────────────────────────────────────────┐        │
│  │ 프로세스                                          │        │
│  │  [ ULT 1 ]          [ ULT 2 ]          [ ULT 3 ] │        │
│  └───│──────────────────│──────────────────│────────┘        │
│ ─────┼──────────────────┼──────────────────┼─ Mode Boundary ─│
│      ▼ 1:1              ▼ 1:1              ▼ 1:1           │
│  [ 커널 영역 (Kernel Space) ]                                │
│     [ KLT 1 ]          [ KLT 2 ]          [ KLT 3 ]          │
│       │ 블로킹 발생!        │                  │               │
│       ▼                   ▼                  ▼               │
│     (Wait 큐 이동)     [ 코어 1 할당 ]    [ 코어 2 할당 ]         │
│                                                              │
│ * 핵심: KLT 1이 멈춰도 커널 스케줄러가 KLT 2, 3을 타 코어에서 실행시킴 │
└──────────────────────────────────────────────────────────────┘
```

이 다이어그램은 KLT 모델에서 블로킹 장애가 어떻게 격리되는지를 보여준다. 유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 시스템 콜을 호출하여 대기 상태에 빠지면, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 해당 KLT의 상태만 'Wait'로 변경하고 동일 프로세스에 속한 다른 KLT들은 다른 물리 코어에서 작업을 멈추지 않고 지속하게 만든다.

- **📢 섹션 요약 비유**: 고속도로 요금소에서 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)(프로세스) 안 승객 수를 모르고 한 번에 통과시키던 방식에서, 승객 한 명 한 명([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))에게 단말기를 줘서 각자 빈 차선(코어)으로 쌩쌩 달리게 해주는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 시스템이다.

---

## Ⅲ. 비교 및 연결

[스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 아키텍처는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 개입 수준에 따라 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 안정성이 극명하게 갈린다. KLT는 ULT에 비해 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) Switching) 오버헤드가 크다는 뚜렷한 약점이 있다.

| 비교 축 | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수준 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) (KLT) | [사용자 수준 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/096_user_level_thread/) (ULT) | 설계적 차이점 |
| :--- | :--- | :--- | :--- |
| **관리 주체** | OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) | 유저 레벨 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 인지 유무 |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/">동시성</a> 방어</strong> | 하나의 [스레드 블록](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/422_thread_block_and_warp/) 시 타 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 정상 실행 | 블록 시 **프로세스 전체 마비** | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성 보장의 핵심 기준 |
| **모드 전환** | [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 시 유저 ↔ [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 횡단 (느림) | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 진입 없음 (매우 빠름) | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목 지점의 차이 |
| **멀티코어 활용** | [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 각 코어에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 가능 ([SMP](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/195_real_time_scheduling/)) | 단일 코어에서만 시분할 | 하드웨어 자원 활용 능력 |

KLT [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)이 느린 이유는 주소 공간([가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)) 변경은 없지만, 유저 모드에서 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드로 진입하기 위해 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 백업과 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 실행이라는 특권 계층 이동(Mode Boundary) 비용이 발생하기 때문이다.

- **📢 섹션 요약 비유**: 방 안에서 옷을 편하게 갈아입는 것(ULT)과, 굳이 경비원이 있는 현관문 밖 복도로 나가서 옷을 갈아입고 다시 방으로 들어오는 것(KLT)의 절차적 낭비 차이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

대부분의 현대 언어(Java Native [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 등)와 OS는 KLT를 기본으로 사용한다. 실무 엔지니어는 KLT의 '무거움'을 통제하는 아키텍처적 결정을 내려야 한다.

### 실무 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/">스레드 풀</a> (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/">Thread Pool</a>) 튜닝</strong>: 서버에 들어오는 요청 1개당 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(`new Thread()`)를 무한정 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는가? KLT는 하나 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)할 때마다 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) TCB와 수 MB의 유저 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 메모리를 점유한다. 트래픽 폭증 시 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/)([Out of Memory](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/))이나 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))이 발생하므로 반드시 하드웨어 코어 수의 N배 수준으로 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/) 크기를 고정해야 한다.
2. <strong>비동기 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/">이벤트 루프</a> 전환</strong>: 클라이언트 1만 명이 접속하는 C10K 환경에서는 KLT 1만 개를 유지할 수 없다. 커넥션 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 무작정 늘리는 대신 Netty나 NGINX 같은 비동기 I/O([Event Loop](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/)) 기반 멀티플렉싱 아키텍처로 넘어가 KLT 개입을 최소화했는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 단일 프로세스 내에서 KLT를 물리 코어 개수보다 수천 배 더 많이 띄우는 행위. 실제 연산 처리 시간보다 KLT 간 교대([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))를 위한 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 스케줄링 시간이 더 길어져 시스템 전체 TPS가 바닥으로 곤두박질친다.

- **📢 섹션 요약 비유**: 튼튼한 장갑차(KLT)는 포탄을 맞아도 병사를 보호하지만 기름을 너무 많이 먹는다. 1만 명의 병사를 옮기겠다고 장갑차 1만 대를 굴리면 부대의 연료가 순식간에 고갈되므로, 장갑차 수는 제한하고 효율적으로 돌려 써야 한다.

---

## Ⅴ. 기대효과 및 결론

[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수준 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 블로킹 연산의 공포에서 소프트웨어를 해방시키고, 멀티코어 하드웨어의 힘을 100% 이끌어내는 가장 안정적인 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 표준 모델이다. 개발자가 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)를 직접 구현하지 않아도 OS의 강력한 자원 관리 혜택을 온전히 누릴 수 있다.

하지만 KLT의 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 비용이 한계에 도달하면서, 미래의 트렌드는 최소한의 KLT(코어 수만큼) 위에서 수십만 개의 초경량 유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)([코루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/), Virtual [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))를 얹어 돌리는 하이브리드 [다대다](/knowledge-base/studynote/02_operating_system/02_process_thread/100_many_to_many_model/)(M:N) 매핑 방식으로 진화하고 있다. 즉 KLT는 가장 무겁지만 결코 무너지지 않는 시스템 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)의 최후 방어선으로 남게 될 것이다.

- **📢 섹션 요약 비유**: [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 고층 빌딩의 튼튼한 철골 뼈대와 같다. 그 자체는 무겁고 설치하기 힘들지만, 그 위에서 가벼운 칸막이(가상 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))들을 마음껏 나누고 부수며 놀 수 있는 안전한 지반을 제공한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/096_user_level_thread/">사용자 수준 스레드</a> (ULT)</strong> | KLT의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 개입 비용을 없앤 극단적 가벼움의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/), 하지만 차단(Block)에 취약함 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/">문맥 교환</a> (<a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/">Context</a> Switching)</strong> | KLT가 CPU 제어권을 바꿀 때 특권 계층을 오가며 발생하는 주요 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 원인 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/195_real_time_scheduling/">SMP</a> (<a href="/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/382_smp/">대칭형 다중 처리</a>)</strong> | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 여러 코어를 인지하고 KLT를 동등하게 흩뿌려주는 하드웨어 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 구조 |
| <strong>가상 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a> (Virtual <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">Thread</a>)</strong> | KLT의 무거움을 극복하기 위해 KLT 위에서 여러 개의 흐름을 쪼개 쓰는 최신 런타임 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
프로세스 시분할 (단일 실행 흐름)
    │
    ▼
사용자 수준 스레드 (가벼움, 블로킹 취약)
    │
    ▼
커널 수준 스레드 (1:1 매핑, 블로킹 면역, 무거움)
    │
    ▼
다대다 (M:N) 매핑 / 하이브리드 모델
    │
    ▼
코루틴 및 가상 스레드 (Virtual Thread) 런타임 결합
```

### 👶 어린이를 위한 3줄 비유 설명

1. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 놀이공원(컴퓨터) 본부에서 이름과 업무를 직접 관리해 주는 정식 직원들이에요.
2. 한 직원이 다쳐서 일을 못하게 돼도(블로킹), 본부가 바로 알아채고 다른 직원들에게 일을 나눠줘서 놀이기구는 절대 멈추지 않아요.
3. 하지만 직원들이 교대할 때마다 매번 본부에 찾아가서 서류 도장을 받아야 해서(모드 전환), 준비 시간이 조금 오래 걸린다는 단점이 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 97 / 800

← **이전**: [96. 사용자 수준 스레드 (User-level Thread) - 스레드 라이브러리가 관리, 커널 비개입](/knowledge-base/studynote/02_operating_system/02_process_thread/096_user_level_thread/)
**다음**: [98. 다대일 (Many-to-One) 스레드 모델](/knowledge-base/studynote/02_operating_system/02_process_thread/098_many_to_one_model/) →

---
