+++
title = "169. 디스패치 지연 (Dispatch Latency)"
date = 2026-03-22

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) (Dispatch [Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 현재 작업에서 다음 작업으로 CPU 제어권을 넘기는 동안 소비하는 순수 전환 시간이다.
> 2. **가치**: 이 시간이 짧고 예측 가능해야 스케줄링 알고리즘의 장점이 실제 응답성, 실시간성, 사용자 체감 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)으로 이어진다.
> 3. **판단 포인트**: 평균 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)보다 중요한 것은 최악 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) (Worst-case [Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))이며, [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 비용뿐 아니라 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 락, 캐시/[TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 재적응, 선점 불가 구간까지 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 새 프로세스나 스레드가 선택된 뒤 실제 첫 사용자 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 실행하기까지 걸리는 시간이다. [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/) ([Short-term Scheduler](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/))가 "누가 다음 차례인가"를 정하면, [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/) ([Dispatcher](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/))는 현재 문맥 저장, 새 문맥 복원, 권한 전환을 수행한다. 이 사이 구간이 바로 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이다.

이 시간이 중요한 이유는 CPU 스케줄링이 선택만으로 끝나지 않기 때문이다. [라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/) (Round Robin)처럼 자주 선점하는 시스템에서 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 길면, CPU는 실제 일보다 전환에 더 많은 시간을 쓰게 된다. 특히 실시간 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) (Real-Time [Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), RTOS)에서는 높은 평균 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)보다 "가장 늦어도 몇 마이크로초 안에 바꿀 수 있는가"가 더 중요하다.

즉 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 [멀티태스킹](/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/)의 숨은 세금이다. 짧을수록 응답성은 좋아지고, 길거나 흔들릴수록 스케줄링 이론은 현실에서 힘을 잃는다.

- **📢 섹션 요약 비유**: 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 무대에서 주연 배우를 바꾸는 막간 시간과 같다. 다음 배우가 준비되어 있어도 커튼 뒤 정리가 길어지면 관객은 공연이 끊겼다고 느낀다.

---

## Ⅱ. 아키텍처 및 핵심 원리

디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 한 번의 명령이 아니라 여러 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 단계의 합이다. [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)나 시스템 호출로 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 진입한 뒤 현재 문맥을 저장하고, [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 판단을 반영해 새 작업의 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)·[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)·주소 공간을 복원한 뒤 다시 사용자 모드로 돌아가야 한다. 여기에 선점 불가 구간이 끼면 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 더 늘어난다.

아래 그림은 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 어디서 생기는지 시간축으로 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│              dispatch latency on a context switch           │
├──────────────────────────────────────────────────────────────┤
│ Running T0                                                   │
│    │ timer interrupt / wake-up                               │
│    ▼                                                         │
│ [kernel entry]                                               │
│    ├─ save old context                                       │
│    ├─ wait for preemption-safe point / lock release          │
│    ├─ choose next runnable task                              │
│    ├─ restore new context + address space                    │
│    └─ return to user mode ───────────────▶ Running T1        │
│                                                              │
│ <------------------- dispatch latency ---------------------> │
└──────────────────────────────────────────────────────────────┘
```

디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)의 핵심 비용은 크게 네 가지다. 첫째, [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)와 [프로그램 카운터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) (Program [Counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/), [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)) 저장·복원 비용이다. 둘째, 메모리 관리 장치 ([Memory Management Unit](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/), [MMU](/knowledge-base/studynote/02_operating_system/06_memory_management/328_mmu/))와 변환 색인 버퍼 ([Translation Lookaside Buffer](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/), [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/)) 관련 비용이다. 셋째, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 락 때문에 즉시 선점하지 못하는 대기 시간이다. 넷째, 전환 후 캐시가 차가워져 원래 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)으로 복귀하기까지의 숨은 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간이다.

| 구성 요소 | 설명 | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 특성 |
| :-------- | :--- | :-------- |
| 문맥 저장/복원 | [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/), [스택 포인터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/), 일반 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 보관 | 비교적 예측 가능 |
| [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 경로 | 다음 실행 대상 탐색 | 자료구조·부하에 영향 |
| [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/) 구간 | 락 해제 전까지 대기 | 최악 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)의 핵심 원인 |
| [MMU](/knowledge-base/studynote/02_operating_system/06_memory_management/328_mmu/)/[TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/)/캐시 영향 | 주소 공간 전환 후 재적응 | 숨은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 손실 |

트레이드오프도 분명하다. 선점성을 높이면 응답성은 좋아지지만 락 분해, [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 복잡도, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 비용이 커진다. 반대로 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 중심으로 뭉툭하게 설계하면 평균은 괜찮아도 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스파이크가 커질 수 있다.

- **📢 섹션 요약 비유**: 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 택배 기사 교대와 같다. 열쇠만 넘기는 것이 아니라 차량 상태, 배송 목록, 내비게이션, 화물 위치까지 모두 정리해야 다음 기사가 제대로 출발할 수 있다.

---

## Ⅲ. 비교 및 연결

디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 종종 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) ([Interrupt Latency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/545_interrupt_latency/))이나 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) ([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))과 혼동된다. [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 외부 이벤트가 들어온 뒤 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 반응하기 시작할 때까지의 시간이고, 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 그 반응 이후 실제 다른 작업을 실행시키기까지의 시간이다. [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)은 디스패치 경로의 핵심 작업이지만, 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 전체와 완전히 같지는 않다.

| 비교 대상 | 초점 | 포함 범위 |
| :-------- | :--- | :-------- |
| [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 이벤트에 얼마나 빨리 반응하는가 | [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 인식~핸들러 진입 |
| 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 새 작업을 얼마나 빨리 실행시키는가 | 선택~첫 실행 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) |
| [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) | 무엇을 저장·복원하는가 | [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)·주소 공간 전환 중심 |

또 다른 중요한 비교는 일반 범용 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)와 RTOS의 차이다. 범용 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 평균 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)과 공정성을 우선하므로 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 분산이 커질 수 있다. RTOS는 오히려 일부 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 희생하더라도 선점 불가 구간을 최소화해 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 상한을 작게 만든다.

이 개념은 [CPU affinity](/knowledge-base/studynote/02_operating_system/02_process_thread/144_cpu_affinity/), [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 바이패스 ([Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) Bypass), 사용자 수준 스레드와도 연결된다. 이유는 간단하다. 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 줄이는 방법은 "전환을 빠르게" 하는 것과 "전환 자체를 덜 하게" 하는 것으로 나뉘기 때문이다.

- **📢 섹션 요약 비유**: [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 초인종 소리를 듣기까지의 시간이라면, 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 문을 열고 손님을 거실에 앉히기까지의 시간이다. 초인종을 빨리 들어도 손님 안내가 느리면 전체 응답은 느리다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 절대값과 변동성으로 함께 관리해야 한다. 예를 들어 오디오 버퍼 주기가 2ms인데 최악 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 3ms면 평균 CPU 사용률이 낮아도 끊김이 발생한다. 반면 웹 서버처럼 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 중심 환경에서는 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 그 자체보다 과도한 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 횟수가 더 큰 문제일 수 있다.

### 실무 시나리오

1. **실시간 오디오 처리**: 48kHz 오디오에서 버퍼가 128샘플이면 대략 2.67ms마다 처리해야 한다. 이때 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 스파이크가 버퍼 주기를 넘으면 드롭아웃이 발생하므로 `PREEMPT_RT` 같은 저지연 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 유리하다.
2. **산업 제어 장비**: 센서 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 후 100μs 안에 제어 스레드를 깨워야 한다면, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 락 길이와 최악 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 측정이 평균 CPU 이용률보다 더 중요하다.
3. <strong>고속 네트워크 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 평면</strong>: 100GbE 수준에서는 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)와 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 디스패치 자체가 병목이 될 수 있어, [DPDK](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/671_dpdk/) ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Plane Development Kit)처럼 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 바이패스 전략을 선택하기도 한다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- 요구사항이 평균 응답성인가, 최악 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 보장인가?
- [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 자체보다 락 대기나 캐시 워밍 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 더 큰가?
- 같은 작업을 고정 코어에 묶어 CPU affinity로 재적응 비용을 줄일 수 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 스케줄링 정책만 바꾸면 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 문제가 해결된다고 믿는 것
- 평균 지표만 보고 실시간성을 판단하는 것
- [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/) 구간을 측정하지 않은 채 RTOS 수준 응답을 기대하는 것

- **📢 섹션 요약 비유**: 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 관리는 엘리베이터 속도만 높이는 일이 아니다. 문이 오래 닫혀 있거나 사람이 갈아타는 동선이 꼬이면, 모터가 빨라도 체감 이동 시간은 줄지 않는다.

---

## Ⅴ. 기대효과 및 결론

디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 잘 제어하면 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 같은 하드웨어에서도 훨씬 더 민첩하게 보인다. 사용자 입력 응답, 실시간 이벤트 처리, [멀티태스킹](/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/) 부드러움, CPU 유효 활용률이 함께 개선되기 때문이다. 특히 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 상한이 작고 예측 가능할수록 시스템은 제어 가능한 플랫폼이 된다.

다만 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 0에 가깝게 만드는 데는 비용이 따른다. 완전 선점 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/), 세밀한 락 설계, 하드웨어 지원, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 바이패스는 구현 복잡도와 유지보수 비용을 높일 수 있다. 따라서 시스템 목표가 데스크톱 반응성인지, 소프트 리얼타임인지, 하드 리얼타임인지에 따라 최적점이 달라진다.

결국 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 스케줄링의 부차적 숫자가 아니라, "선택된 작업이 언제 실제로 움직이기 시작하는가"를 결정하는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 현실 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 지표다. 좋은 스케줄링은 좋은 디스패치 없이는 완성되지 않는다.

- **📢 섹션 요약 비유**: 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 릴레이 경기의 바통 전달 구간과 같다. 주자 선발이 완벽해도 바통을 늦게 넘기면 기록은 절대 좋아지지 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :---------- |
| [디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/) ([Dispatcher](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)) | 실제 CPU 제어권 전달을 수행하는 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) |
| [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) ([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)) | 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)의 핵심 내부 작업 |
| [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) ([Interrupt Latency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/545_interrupt_latency/)) | 디스패치 전에 선행되는 반응 시간 |
| RTOS | 최악 디스패치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 제한하는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 철학 |
| [CPU affinity](/knowledge-base/studynote/02_operating_system/02_process_thread/144_cpu_affinity/) | 캐시/[TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 재적응 비용을 줄이는 실무 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
타이머 인터럽트 · wake-up 이벤트
    │
    ▼
커널 진입
    │
    ▼
문맥 저장 · 스케줄러 선택 · 문맥 복원
    │
    ▼
Dispatch Latency 측정
    │
    ├──────────────▶ 선점 커널 최적화
    ├──────────────▶ CPU affinity · cache locality 개선
    └──────────────▶ RTOS · Kernel Bypass 선택
```

이 흐름도는 이벤트 반응이 단순 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 처리에서 끝나지 않고, 실제 실행 전환과 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 최적화 문제로 확장되는 구조를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 한 친구가 그네에서 내려오고 다른 친구가 올라타려면 잠깐 자리를 바꾸는 시간이 필요해요.
2. 그 짧은 바꾸는 시간이 길어질수록 실제로 노는 시간은 줄어들어요.
3. 컴퓨터도 그래서 일을 바꿀 때 그 준비 시간을 아주 짧고 빠르게 만들려고 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 169 / 800

← **이전**: [168. 디스패처 (Dispatcher) - 문맥 교환 수행 모듈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)
**다음**: [170. 스케줄링 기준 (Scheduling Criteria) - CPU 이용률, 처리량, 반환시간, 대기시간, 응답시간](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/170_scheduling_criteria/) →

---
