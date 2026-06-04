+++
title = "90. 프로세스 제어 블록 (PCB, Process Control Block) / 태스크 제어 블록 (TCB)"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PCB ([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/943_process/) Control Block)는 운영체제가 각 프로세스의 상태, [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 값, 메모리 정보 등 모든 메타데이터를 추적하고 관리하기 위해 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 공간에 유지하는 핵심 자료구조다.
> 2. **가치**: CPU 시분할 환경에서 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) ([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)) 시, 현재 작업 상태를 안전하게 저장하고 다음 작업 상태를 복원할 수 있게 하여 멀티태스킹의 물리적 기반을 제공한다.
> 3. **판단 포인트**: 프로세스 내에서 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 분화함에 따라, 공유 자원은 PCB에 남기고 개별 실행 흐름은 TCB ([Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) Control Block)로 분리 관리하여 스케줄링 오버헤드를 극적으로 낮추는 계층적 아키텍처로 진화했다.

---

## Ⅰ. 개요 및 필요성

프로세스 제어 블록 (PCB, [Process](/knowledge-base/studynote/12_it_management/05_security_compliance/943_process/) Control Block)은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 시스템 내의 실행 중인 프로세스를 제어하기 위해 사용하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조체다. 리눅스에서는 `task_struct`로 구현되며, 프로세스의 생명 주기를 통제하는 '주민등록증'과 같다. 더 세밀한 실행 단위인 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 등장하면서, 고유 상태를 담는 TCB ([Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) Control Block)가 PCB 내부에 계층적으로 연결되었다.

하나의 CPU 코어는 동시에 하나의 명령어만 처리할 수 있다. 시분할 (Time-Sharing) 운영체제에서 여러 프로세스가 동시에 실행되는 것처럼 보이려면, CPU가 프로세스 A에서 B로 제어권을 넘길 때 A의 정확한 중단 지점([레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/), [프로그램 카운터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/))을 완벽히 기억해야 한다. 이 하드웨어 문맥을 안전한 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리에 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)해두는 공간이 바로 PCB다. PCB가 없다면 중단된 지점부터 다시 코드를 이어서 실행하는 것은 불가능하다.

- **📢 섹션 요약 비유**: PCB는 독서광이 두꺼운 책을 읽다 잠시 덮을 때 꽂아두는 '상세한 책갈피와 메모장'과 같다. 며칠 뒤 책을 펼쳐도 정확히 몇 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 몇 번째 줄이었는지 즉시 몰입할 수 있게 해준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

PCB는 유저가 임의로 조작하여 권한을 탈취하는 것을 막기 위해 반드시 보안이 격리된 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 공간 ([Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) Space)에만 적재된다.

| 구성 요소 | 역할 및 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 스케줄링 관점의 의미 |
| :--- | :--- | :--- |
| <strong>프로세스 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/">식별자</a> (PID)</strong> | 고유 번호, PPID, UID 저장 | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 해시 테이블에서 해당 프로세스를 찾는 키 |
| <strong>상태 (<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/">State</a>)</strong> | Ready, Running, Wait, Zombie 등 | 큐 정렬 및 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 선택의 기준 |
| <strong>CPU 문맥 (<a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/">Context</a>)</strong> | [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/), [SP](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/), [범용 레지스터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/162_gpr/) 값 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) | 다음 실행 재개 시 하드웨어에 복원할 필수 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| **메모리 관리 정보** | [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 포인터, 세그먼트 | 프로세스 간 메모리 침범 방지 및 주소 공간 고립 |
| **I/O 상태 정보** | 할당된 자원, 열린 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(FD) 목록 | 자원 반납 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 및 [교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/) 분석에 사용 |

[문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) ([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)) 시, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 실행 중이던 프로세스의 CPU [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 값을 자신의 PCB에 '저장(Save)'하고, 새롭게 선택된 프로세스의 PCB에서 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 값을 '복원(Restore)'한다.

```text
+--------------------------------------------------------------+
|           문맥 교환 (Context Switch)과 PCB의 역할            |
+--------------------------------------------------------------+
|  [프로세스 A]                [OS 커널]                [프로세스 B] |
|      |                          |                          |       |
|  (실행 중) ---> 인터럽트 발생 -->|                          |       |
|      |                   +------v------+                   |       |
|      |                   | A의 레지스터를 |                   |       |
|      |                   | PCB_A에 저장  |                   |       |
|      |                   +------+------+                   |       |
|      |                   +------v------+                   |       |
|      |                   | PCB_B에서 B의 |                   |       |
|      |                   | 레지스터 복원 |                   |       |
|      |                   +------+------+                   |       |
|      |                          |---> 복원 완료 ---------> (실행 재개)|
|      |                          |                          v       |
| * 핵심: 저장/복원 구간에서는 사용자 코드가 전혀 실행되지 않는 오버헤드 발생 |
+--------------------------------------------------------------+
```

이 과정에서 CPU는 실제 애플리케이션 연산이 아닌 운영체제의 상태 저장 작업만 수행하므로, 교환 횟수가 많아질수록 전체 시스템의 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))은 하락한다.

- **📢 섹션 요약 비유**: 게임을 끄기 전에 정확한 위치와 아이템 상태를 '세이브 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(PCB)'로 만들고, 다음 날 다시 게임을 켤 때 '로드'를 해야만 어제 잡다 만 몬스터부터 이어서 싸울 수 있는 원리다.

---

## Ⅲ. 비교 및 연결

현대 [멀티스레딩](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/397_multithreading/) 환경에서는 PCB 단일 구조의 무거운 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 비용을 줄이기 위해, 자원 공유 영역과 실행 흐름 영역을 분리하는 TCB ([Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) Control Block) 구조를 채택했다.

| 비교 항목 | 프로세스 간 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) (PCB 교체) | [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 간 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) (TCB 교체) |
| :--- | :--- | :--- |
| **전환 대상** | PCB 전체와 고유 주소 공간 맵핑 | 동일 PCB 내의 TCB만 전환 |
| **메모리 처리** | [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 교체 발생 | 기존 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 유지 (공유) |
| **캐시 (Cache)** | [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) ([Translation Lookaside Buffer](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/)) 플러시 | [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 내용 유지 ([캐시 히트](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/) 상승) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 오버헤드</strong> | 매우 무거움 | 비교적 가벼움 |

같은 프로세스 내에서 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)만 교체할 경우, 메모리 맵핑([페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/))이 동일하므로 캐시 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화나 주소 변환 캐시([TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/))의 플러시가 발생하지 않는다. 이것이 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)이 프로세스 교환보다 압도적으로 빠른 구조적 이유다.

- **📢 섹션 요약 비유**: 이사를 갈 때 살림살이를 다 싸서 아예 다른 동네로 떠나는 것(PCB 교체)과, 같은 집 안에서 거실에 있다가 안방으로 자리만 옮기는 것(TCB 교체)만큼이나 소모되는 비용이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 환경에서 PCB는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모 공간과 시스템 안정성을 결정짓는 핵심 지표로 다뤄진다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 및 실무 판단 포인트
1. <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/109_zombie_process/">좀비 프로세스</a> (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/109_zombie_process/">Zombie Process</a>) 적체 방어</strong>: 시스템 모니터링 시 'Z' 상태의 프로세스가 수백 개 쌓이는 현상. 프로세스가 메모리를 반납하고 종료되었음에도, 부모 프로세스가 `wait()` 시스템 콜을 호출하지 않아 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 PCB 뼈대와 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)(PID)를 지우지 못해 발생한다. 이는 가용 PID를 고갈시켜 신규 프로세스 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)을 막으므로, 부모 프로세스를 수정하거나 종료시켜 Init 프로세스가 회수(Reaping)하도록 조치해야 한다.
2. **포크 폭탄 (Fork Bomb) 공격 통제**: 악의적인 스크립트가 무한정 자식 프로세스를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하면, 각 PCB가 차지하는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리가 고갈되어 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) ([Out of Memory](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/)) 패닉이 발생한다. 엔지니어는 `ulimit -u` 설정을 통해 사용자당 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 가능한 최대 프로세스 수를 제한해야 한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 멀티스레드 애플리케이션에서 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 종료 시 자원을 적절히 `detach` 또는 `join`하지 않아 TCB가 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 누수(Leak)되도록 방치하는 설계.

- **📢 섹션 요약 비유**: 직원이 퇴사할 때 노트북은 반납했지만, 인사팀이 퇴사 결재(wait)를 안 해줘서 직원 명부(PCB)에 빈 이름표가 남아 신규 채용(PID 할당)을 못 하는 행정 마비 상태와 같다.

---

## Ⅴ. 기대효과 및 결론

PCB와 TCB의 정교한 관리 구조는 단일 CPU에서도 수천 개의 작업이 부드럽게 돌아가는 현대 멀티태스킹의 기적을 가능케 했다.

[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에는 무거운 상태 정보를 모두 엎어 쓰는 방식이었으나, 점차 메모리 영역은 묶어두고 실행 흐름만 가볍게 스위칭하는 TCB 계층 구조로 진화하며 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 극대화했다. 미래에는 [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 기술을 통해 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 수정 없이도 PCB의 상태 변화를 실시간으로 추적하거나, 사용자 공간(User Space)에서 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 개입 없이 수만 개의 가상 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(Virtual [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))를 직접 스케줄링하는 방식으로 아키텍처가 발전하고 있다.

- **📢 섹션 요약 비유**: 두꺼운 종이 서류철([초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) PCB) 하나로 모든 걸 관리하다가, 이제는 가벼운 포스트잇(TCB)을 서류철 안에 여러 장 붙여 빠르게 넘겨가며 일하는 고효율 시스템으로 진화한 것이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/">문맥 교환</a> (<a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/">Context Switch</a>)</strong> | CPU 점유가 넘어갈 때 이전 상태를 PCB에 저장하고 새 PCB를 읽어오는 멈춤 현상 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/">TLB</a> (<a href="/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/">Translation Lookaside Buffer</a>)</strong> | PCB 교체 시 메모리 맵핑이 달라져 플러시가 발생하며 시스템 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 떨어뜨리는 주범 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a> (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">Thread</a>)</strong> | 단일 PCB를 공유하며 독자적인 TCB만 들고 실행되는 가벼운 작업 단위 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/109_zombie_process/">좀비 프로세스</a> (Zombie)</strong> | 몸(메모리)은 죽었으나 부모가 상태를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해주지 않아 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 영혼(PCB)이 묶여있는 상태 |

### 📈 관련 키워드 및 발전 흐름도

```text
일괄 처리 (Batch Processing)
    |
    v
PCB (Process Control Block) 도입 · 멀티태스킹 (시분할) 구현
    |
    v
문맥 교환 (Context Switch) 오버헤드 최소화 요구
    |
    v
TCB (Task Control Block) 분리 · 가벼운 멀티스레딩
    |
    v
경량 사용자 스레드 (Goroutine, Virtual Thread)의 등장
```

이 흐름도는 프로세스 관리 아키텍처가 무거운 통합 구조에서 가볍고 세분화된 계층 구조로 진화하여 응답 속도를 극대화하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. PCB는 컴퓨터 안의 여러 프로그램들이 각자 자기가 어디까지 일했는지 꼼꼼히 적어두는 비밀 일기장이에요.
2. 이 일기장은 너무 중요해서 아무나 볼 수 없는 '[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 공간'이라는 튼튼한 금고 안에 안전하게 보관되어 있어요.
3. 컴퓨터가 게임을 하다가 유튜브로 넘어갈 때, 게임 일기장에 상황을 적어두고 유튜브 일기장을 꺼내오기 때문에 다시 게임을 켜도 끊김 없이 이어서 할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 90 / 800

<- **이전**: [89. 대기 큐 (Wait Queue / Device Queue)](/knowledge-base/studynote/02_operating_system/02_process_thread/089_wait_queue/)
**다음**: [91. PCB 요소 - PID, 상태, PC, 레지스터, 스케줄링 정보, 메모리 정보, 회계 정보, I/O 상태 정보](/knowledge-base/studynote/02_operating_system/02_process_thread/091_pcb_elements/) ->

---
