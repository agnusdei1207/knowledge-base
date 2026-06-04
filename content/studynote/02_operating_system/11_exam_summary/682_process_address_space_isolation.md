---
title: "682. 프로세스 주소 공간 분리 (Process Address Space Isolation)"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 프로세스 주소 공간 분리는 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 <strong><a href="/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/">가상 메모리</a>(<a href="/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/">Virtual Memory</a>)</strong>를 이용하여 각 프로세스마다 "너 혼자 컴퓨터의 모든 메모리(예: 0번지부터 4GB)를 다 쓰고 있어"라는 완벽한 환상(Illusion)을 심어주는 핵심 샌드박스 기술이다.
> 2. **메커니즘**: CPU 내부의 <strong><a href="/studynote/02_operating_system/06_memory_management/328_mmu/">MMU</a> (<a href="/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/">Memory Management Unit</a>)</strong>가 프로세스가 내뿜는 가짜 주소([논리 주소](/studynote/02_operating_system/06_memory_management/322_logical_virtual_address/))를 하드웨어적인 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)([Page Table](/studynote/02_operating_system/06_memory_management/353_page_table/))을 통해 진짜 램의 주소([물리 주소](/studynote/02_operating_system/06_memory_management/323_physical_address/))로 실시간 번역함으로써 물리적인 격리를 강제한다.
> 3. **가치**: 이 분리 덕분에 A 프로세스가 버그로 미쳐 날뛰며 아무 주소나 덮어써도 B 프로세스나 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)(OS)의 메모리는 절대 망가지지 않으며(안정성), 악성코드가 다른 프로그램의 비밀번호를 훔쳐보는 행위([보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))가 원천 차단된다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - **주소 공간 (Address Space)**: 특정 프로세스가 합법적으로 접근할 수 있는 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적인 메모리 주소의 범위.
  - <strong>공간 분리 (<a href="/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/">Isolation</a>)</strong>: 각 프로세스의 주소 공간을 완벽하게 독립시켜, 서로 겹치거나 침범할 수 없도록 물리적/[논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 벽을 치는 행위.

- **필요성 (단일 주소 공간의 재앙)**:
  - 초창기 컴퓨터(MS-DOS 시절)에는 [가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)가 없어서 모든 프로그램이 물리적 램(RAM)의 실제 주소를 직접 건드렸다.
  - 만약 A 프로그램이 주소 `0x1000`에 중요한 변수를 저장해 뒀는데, 새로 켜진 B 프로그램이 우연히 `0x1000` 주소에 값을 써버리면? A 프로그램은 이유도 모른 채 데이터가 오염되어 크래시가 난다.
  - 악성코드가 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)(OS)이 상주하는 메모리 영역을 덮어써 버리면 컴퓨터 전체가 블루스크린(BSOD)을 띄우며 죽어버린다.
  - **해결책**: 프로그램에게 '진짜 [물리 주소](/studynote/02_operating_system/06_memory_management/323_physical_address/)'를 알려주지 말고, 각자 자기만의 '가짜 주소(가상 주소 0번지)'를 쓰게 한 뒤, OS가 뒤에서 남는 [물리 주소](/studynote/02_operating_system/06_memory_management/323_physical_address/)의 빈방으로 몰래 매핑해 주는 주소 공간 분리가 탄생했다.

  - <strong>분리 전 (<a href="/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> OS)</strong>: 거대한 강당(RAM)에 100명의 학생(프로세스)이 섞여서 시험을 본다. 서로 남의 시험지를 훔쳐보거나 밟고 지나가서 시험장이 아수라장이 된다.
  - **주소 공간 분리 (현대 OS)**: 100명의 학생에게 밖이 안 보이는 완벽한 독방([가상 주소 공간](/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/))을 하나씩 준다. 모든 학생은 자기가 '1번 방'에 있는 줄 알지만, 실제로는 호텔(물리 메모리)의 302호, 501호 등에 흩어져 있다. 독방 안에서 아무리 난동을 피워도 옆방 학생은 전혀 모른다.

- **발전 과정**:
  1. <strong>Base &amp; <a href="/studynote/02_operating_system/06_memory_management/330_limit_register/">Limit Register</a></strong>: [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) CPU 하드웨어 기술. 각 프로세스의 시작 주소와 끝 주소를 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 기록해 범위를 넘으면 CPU가 차단함.
  2. <strong><a href="/studynote/02_operating_system/04_synchronization/259_paging/">페이징</a> (<a href="/studynote/02_operating_system/04_synchronization/259_paging/">Paging</a>)</strong>: 현대 OS의 표준. 메모리를 4KB 단위의 작은 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)로 잘라서, 흩어진 물리 메모리를 모아 연속된 가상 공간처럼 보이게 매핑함.

- **📢 섹션 요약 비유**: 서로 사이가 안 좋은 호랑이들을 하나의 큰 철창(물리 메모리)에 풀어놓지 않고, 보이지 않는 투명한 개별 철창([가상 주소 공간](/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/))으로 완벽하게 격리하여 서로 물어뜯는 것을 원천 봉쇄한 사파리 공원 설계입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [가상 주소 공간](/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/) ([Virtual Address Space](/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/))의 레이아웃

32비트 리눅스 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)에서 하나의 프로세스가 가지는 전형적인 4GB 주소 공간의 구조다.

```text
  +-------------------------------------------------------------------+
  |                 단일 프로세스의 논리적 가상 주소 공간 (4GB)             |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  0xFFFFFFFF +-----------------------------------------+           |
  |             |                                         |           |
  |             |   Kernel Space (1GB, 모든 프로세스 공통)     |           |
  |             |                                         |           |
  |  0xC0000000 +-----------------------------------------+           |
  |             |   User Stack (함수 지역변수, 아래로 자람)     |           |
  |             |   v                                     |           |
  |             |                                         |           |
  |             |   (여유 공간)                             |           |
  |             |                                         |           |
  |             |   ^                                     |           |
  |             |   Heap (malloc 동적 할당 메모리, 위로 자람)  |           |
  |             +-----------------------------------------+           |
  |             |   BSS Segment (초기화되지 않은 전역 변수)     |           |
  |             +-----------------------------------------+           |
  |             |   Data Segment (초기화된 전역 변수)         |           |
  |             +-----------------------------------------+           |
  |             |   Code (Text) Segment (실행할 기계어 코드)   |           |
  |  0x08048000 +-----------------------------------------+           |
  |  0x00000000   (접근 금지 영역 - Null Pointer 예방)                     |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 크롬 브라우저를 켜든 엑셀을 켜든, 프로그램 입장에서는 자기가 메모리 `0x08048000`번지부터 시작해서 3GB의 유저 공간을 독점하고 있다고 생각한다. 크롬의 `0x08048000`과 엑셀의 `0x08048000`은 똑같은 '가상 주소'이지만, CPU 안의 [MMU](/studynote/02_operating_system/06_memory_management/328_mmu/)(메모리 관리 유닛)를 거치고 나면 실제 물리 램(RAM)에서는 전혀 다른 위치(예: 크롬은 1,000번지, 엑셀은 8,000번지)로 매핑되므로 절대 충돌하지 않는다.

---

### MMU와 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)을 통한 물리적 격리

가상 주소를 [물리 주소](/studynote/02_operating_system/06_memory_management/323_physical_address/)로 번역(Translation)하는 하드웨어적 과정 자체가 바로 격리([Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/))의 본질이다.

1. <strong><a href="/studynote/02_operating_system/06_memory_management/353_page_table/">페이지 테이블</a> (<a href="/studynote/02_operating_system/06_memory_management/353_page_table/">Page Table</a>)</strong>: [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 프로세스를 만들 때마다, 그 프로세스 전용의 '비밀 지도([페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/))'를 하나씩 만들어 메모리에 둔다.
2. <strong>CR3 <a href="/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/">레지스터</a> (<a href="/studynote/02_operating_system/06_memory_management/354_ptbr_ptlr/">PTBR</a>)</strong>: CPU가 프로세스 A를 실행할 때, 프로세스 A의 비밀 지도 시작 주소를 CPU의 특정 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)(`CR3`)에 장착한다.
3. **번역과 차단**: 프로세스 A가 "내 가상 주소 100번지를 읽어줘!"라고 CPU에 명령하면, MMU는 `CR3`에 있는 A의 지도를 편다.
   - 지도에 "가상 100번 = 물리 800번"이라고 적혀 있으면 물리 800번을 읽어준다.
   - 만약 프로세스 A가 해킹을 하려고 "가상 5,000번(남의 구역) 읽어줘!"라고 했는데, A의 지도에 가상 5,000번에 대한 매핑 정보가 없거나 '권한 없음(Invalid)'으로 표시되어 있다면? MMU는 즉시 하드웨어 인터럽트인 <strong><a href="/studynote/02_operating_system/06_memory_management/364_segmentation/">Segmentation</a> Fault (<a href="/studynote/02_operating_system/07_virtual_memory/387_page_fault/">Page Fault</a>)</strong>를 발생시키고, OS는 권한을 침범한 프로세스 A를 즉결 처형(Kill)한다.

- **📢 섹션 요약 비유**: 각 죄수(프로세스)에게 자기 감방(가상 공간) 지도를 하나씩 줍니다. 죄수가 문을 열고 나가려 할 때 교도관([MMU](/studynote/02_operating_system/06_memory_management/328_mmu/))이 지도를 확인하는데, 지도에 없는 길(남의 메모리)로 가려고 하면 즉시 총([Segmentation](/studynote/02_operating_system/06_memory_management/364_segmentation/) Fault)을 쏴서 탈옥을 막는 완벽한 통제 시스템입니다.

---

## Ⅲ. 비교 및 연결

### [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)([Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/))와의 주소 공간 공유 차이

프로세스와 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 가장 결정적인 차이는 이 '주소 공간 분리' 여부에 있다.

| 구분 | 프로세스 ([Process](/studynote/12_it_management/05_security_compliance/943_process/)) | [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) ([Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)) |
|:---|:---|:---|
| **주소 공간** | 각자 독립적인 [가상 주소 공간](/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/) (CR3가 다름) | <strong>하나의 <a href="/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/">가상 주소 공간</a>을 공유함</strong> |
| **메모리 침범** | OS의 MMU가 완벽하게 차단 (안전) | [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) A가 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) B의 데이터를 덮어쓸 수 있음 (위험) |
| **통신 방식** | 무거운 [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) ([파이프](/studynote/02_operating_system/02_process_thread/123_pipe/), [소켓](/studynote/02_operating_system/02_process_thread/125_socket/), [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/)) 필수 | 전역 변수([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), [Heap](/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/))를 통해 그냥 읽고 쓰면 됨 |
| <strong><a href="/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/">문맥 교환</a></strong> | 무거움 ([페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 교체로 인한 [TLB](/studynote/02_operating_system/06_memory_management/357_tlb/) 플러시 발생) | **가벼움** ([페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 유지, [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 포인터만 변경) |

### 과목 융합 관점

- <strong>컴퓨터구조 (<a href="/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/">CA</a>)</strong>: MMU가 매번 메모리([페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/))를 읽어서 주소를 번역하면 CPU 속도가 반토막 난다. 이를 막기 위해 주소 번역 결과를 캐싱해 두는 하드웨어가 바로 <strong><a href="/studynote/02_operating_system/06_memory_management/357_tlb/">TLB</a> (<a href="/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/">Translation Lookaside Buffer</a>)</strong>다. 주소 공간 분리를 뒷받침하는 가장 중요한 하드웨어 인프라다.
- <strong><a href="/studynote/13_cloud_architecture/01_virtualization/015_virtualization/">가상화</a> (Cloud)</strong>: 프로세스의 주소 공간 분리 개념을 확장한 것이 가상머신([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))이다. VM은 아예 하이퍼바이저가 EPT ([Extended Page Table](/studynote/01_computer_architecture/15_advanced_topics/661_extended_page_table/))라는 2단계 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)을 두어, Guest OS가 자기가 물리 서버 1대를 다 쓰고 있다고 착각하게 만드는 <strong>'<a href="/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a> 레벨의 주소 공간 분리'</strong> 기술이다.

- **📢 섹션 요약 비유**: 프로세스가 완벽히 분리된 '아파트의 각 호실'이라면, [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 호실 안에서 같이 사는 '가족'입니다. 옆집(다른 프로세스) 물건은 훔칠 수 없지만, 가족(다른 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/))끼리는 거실([Heap](/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/))에 둔 지갑을 허락 없이 쓸 수 있어 주의([동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/))가 필요합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — <a href="/studynote/02_operating_system/06_memory_management/364_segmentation/">Segmentation</a> Fault(세그폴트)와 메모리 덤프 (<a href="/studynote/02_operating_system/01_overview_architecture/035_core_dump/">Core Dump</a>)</strong>: C언어로 개발된 리눅스 서버 데몬이 갑자기 `Segmentation fault (core dumped)` 메시지를 남기고 죽어버림.
   - **원인 분석**: 개발자가 실수로 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화하지 않은 포인터나 `NULL(0x0)` 포인터를 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)(`*ptr = 10;`)했다. 리눅스 [가상 주소 공간](/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/)에서 `0x0`부터 첫 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)(4KB) 영역은 일부러 매핑을 비워두어 어떠한 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 권한도 안 주도록 설계되어 있다. MMU가 이 불법 접근을 감지하고 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 일러바쳐 OS가 프로세스를 죽인 것이다. 주소 공간 분리 기술이 서버 전체가 오염되는 것을 막아낸 훌륭한 방어 사례다.
   - **대응**: [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 죽은 프로세스의 당시 [가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 상태를 고스란히 파일로 남긴 `core` 덤프 파일을 `gdb`로 열어, 몇 번째 줄의 코드에서 엉뚱한 주소 공간을 건드렸는지 원인을 추적(Backtrace)한다.

2. <strong>시나리오 — <a href="/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/">Docker</a> <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a>의 메모리 격리와 <a href="/studynote/02_operating_system/01_overview_architecture/062_cgroups/">Cgroups</a></strong>: 한 서버에 떠 있는 A [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)(웹서버)가 램(RAM)을 32GB나 혼자 다 처먹어서, 옆에 있던 B [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)(DB)가 뻗어버림.
   - **원인 분석**: 주소 공간 분리([가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/))는 "남의 메모리를 못 보게" 하는 기술이지, "네가 물리 메모리를 얼마나 낭비할지"를 막는 기술은 아니다. 가상 주소 4GB를 꽉 채워 쓰면 진짜 물리 램 4GB가 닳아 없어진다.
   - **아키텍처 적용**: 프로세스 격리 기술([Namespace](/studynote/02_operating_system/01_overview_architecture/061_namespace/))만으로는 부족하다. 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 <strong><a href="/studynote/02_operating_system/01_overview_architecture/062_cgroups/">Cgroups</a> (<a href="/studynote/01_computer_architecture/15_advanced_topics/668_cgroups_hw_resource_allocation/">Control Groups</a>)</strong> 기능을 사용하여, A [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)([프로세스 그룹](/studynote/02_operating_system/02_process_thread/159_process_group/))가 사용할 수 있는 '물리적 메모리 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)의 최대 개수([Memory Limit](/studynote/02_operating_system/07_virtual_memory/439_cgroups_memory_limit/))'를 4GB로 강제 할당해야 한다. 이 한도를 넘으려 하면 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) Killer가 A [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)만 조용히 죽여버린다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 애플리케이션 아키텍처: 멀티프로세스 vs 멀티스레드 판단        |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [동시 접속이 많은 고성능 웹 서버 / 애플리케이션 프레임워크 설계]               |
  |                |                                                  |
  |                v                                                  |
  |      하나의 작업(Task)에 치명적인 버그가 났을 때, 전체 시스템이 죽어도 되는가?    |
  |          +- 아니오 ---> [멀티프로세스 (Multi-Process) 아키텍처 채택]     |
  |          |            (예: Chrome 브라우저, Nginx 워커 프로세스)        |
  |          |            - 탭 하나가 죽어도 다른 탭(주소 공간)은 완벽히 생존  |
  |          |            - 단점: 메모리를 많이 먹고 IPC 통신 비용이 비쌈       |
  |          |                                                        |
  |          +- 예 ------> [멀티스레드 (Multi-Thread) 아키텍처 채택]        |
  |                       (예: Tomcat WAS, Redis, 게임 서버)              |
  |                       - 자원 소모가 적고 성능이 빠르나, 스레드 하나가       |
  |                         메모리를 오염시키면 프로세스 전체가 즉사함           |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 크롬 브라우저가 과거 인터넷 익스플로러(멀티스레드 기반)를 이길 수 있었던 가장 큰 이유는 바로 "주소 공간 분리"를 탭(Tab)마다 적용한 [멀티프로세스 아키텍처](/studynote/02_operating_system/02_process_thread/137_multiprocess_architecture/) 덕분이다. 악성 광고가 떠서 탭 하나가 세그폴트로 죽어도, 다른 탭에 켜둔 넷플릭스는 멈추지 않았다. 메모리를 낭비하더라도 '안정성'을 취한 아키텍트의 위대한 결정이었다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong><a href="/studynote/02_operating_system/06_memory_management/374_aslr/">ASLR</a> (Address Space Layout Randomization)</strong>: 주소 공간이 고정되어 있으면 해커가 "[스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)은 0xC0000000에 있겠군" 하고 [버퍼 오버플로우](/studynote/02_operating_system/10_security/591_buffer_overflow/) 공격을 날린다. 현대 OS 컴파일러의 `-fPIE` 옵션과 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 [ASLR](/studynote/02_operating_system/06_memory_management/374_aslr/) 기능을 켜서, 프로그램을 실행할 때마다 [가상 주소 공간](/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/)의 힙/[스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 위치를 무작위로 뒤섞어버려 해킹을 방어하고 있는가?
- <strong><a href="/studynote/02_operating_system/06_memory_management/333_shared_library/">공유 라이브러리</a> 매핑 (.so / .dll)</strong>: 100개의 프로세스가 각자의 주소 공간에 C 표준 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)(`libc`)를 들고 있으면 메모리가 100배 낭비된다. OS는 물리 메모리에 `libc`를 딱 하나만 올려두고, 100개 프로세스의 [가상 주소 공간](/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/)([페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/))이 모두 그 1개의 [물리 주소](/studynote/02_operating_system/06_memory_management/323_physical_address/)를 가리키도록 매핑(Shared [Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/))하여 램을 절약하는 기술을 쓴다.

- **📢 섹션 요약 비유**: 멀티프로세스는 각자 따로 배를 타고 항해하는 것입니다. 배 한 척에 구멍이 나서 가라앉아도(메모리 오염) 내 배는 안전합니다. 멀티스레드는 거대한 유람선 하나에 다 같이 타는 것입니다. 빠르고 호화롭지만, 누군가 배 밑바닥에 구멍을 내면 모두가 수장([프로세스 종료](/studynote/02_operating_system/02_process_thread/107_process_termination/))됩니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 주소 공간 미분리 (Real Mode) | 주소 공간 분리 (Protected Mode) | 개선 효과 |
|:---|:---|:---|:---|
| **정성 (안정성)** | 앱 충돌 시 OS 전체 블루스크린(BSOD) | 문제 앱만 종료 (Segfault) | OS 생존성(Uptime) 100% 보장 |
| <strong>정성 (<a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">보안성</a>)</strong> | 메모리 직접 덤프로 비밀번호 탈취 | 타 프로세스 메모리 접근 원천 차단 | 악성코드 및 해킹에 대한 물리적 방어막 제공 |
| **정성 (개발 편의성)**| 메모리 파편화로 큰 연속 메모리 확보 불가 | 가상 연속 메모리로 무한한 공간 착각 | 프로그래머가 램 용량을 신경 쓰지 않고 코딩 가능 |

### 미래 전망
- <strong><a href="/studynote/02_operating_system/10_security/666_secure_enclave_trustzone_sgx_tee/">보안 엔클레이브</a> (<a href="/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/">TEE</a> / <a href="/studynote/09_security/04_endpoint_security/389_sgx/">SGX</a>)</strong>: 기존 주소 공간 분리는 "유저 프로세스 간의 격리"는 완벽했지만, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)(Ring 0)은 모든 유저의 주소를 볼 수 있었다. 미래의 보안은 OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)조차 믿지 않는다. 인텔 SGX나 ARM TrustZone처럼 CPU 하드웨어 레벨에서 앱의 메모리를 아예 암호화해 버려서 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)조차 쓰레기값만 보게 만드는 극단적인 주소 공간 격리([Confidential Computing](/studynote/01_computer_architecture/15_advanced_topics/795_confidential_computing/))가 발전하고 있다.
- <strong>단일 주소 공간 OS (SASOS)와 <a href="/studynote/04_software_engineering/10_trends_pm_quality/782_memory_safety_rust_compiler_verification/">Rust</a></strong>: [가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 매핑([TLB](/studynote/02_operating_system/06_memory_management/357_tlb/) 미스) 오버헤드가 너무 커지자, 역발상으로 "모든 프로그램을 하나의 주소 공간에 다 때려 넣자!"는 연구가 나오고 있다. 대신 메모리 침범을 하드웨어([MMU](/studynote/02_operating_system/06_memory_management/328_mmu/))가 막는 게 아니라, [Rust](/studynote/04_software_engineering/10_trends_pm_quality/782_memory_safety_rust_compiler_verification/) 같은 안전한 언어의 컴파일러가 "너는 남의 메모리를 건드리지 않아"라고 100% 보증하여 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 격리를 동시에 잡는 [유니커널](/studynote/02_operating_system/10_security/640_unikernel_mirageos_architecture/) 기반의 연구가 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중이다.

### 결론
프로세스 주소 공간 분리는 현대 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 달성한 가장 위대한 '기만술(Deception)'이다. [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 [가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)와 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)이라는 정교한 마술을 통해, 수백 개의 옹졸한 프로그램들에게 "이 거대한 컴퓨터는 오직 너만을 위해 존재해"라는 황홀한 착각을 심어주었다. 이 착각(격리) 속에서 프로그램들은 남을 해칠 수도, 남에게 해를 입을 수도 없이 안전하게 자신의 비즈니스 로직에만 몰두할 수 있게 되었으며, 이것이 오늘날 멀티태스킹과 클라우드 컴퓨팅이 붕괴하지 않고 유지되는 가장 근본적인 중력의 법칙이다.

- **📢 섹션 요약 비유**: 수백 명의 아이(프로세스)들에게 각자에게만 허락된 완벽한 상상 속의 놀이방(가상 공간)을 만들어주고, 서로의 장난감을 절대 뺏을 수 없게 유리벽([MMU](/studynote/02_operating_system/06_memory_management/328_mmu/))을 쳐둔 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)라는 위대한 보육교사의 설계입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 모놀리식 vs [마이크로 커널](/studynote/04_software_engineering/09_cloud_native_ai_architecture/598_microkernel_plugin_architecture/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) 기법 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 오버헤드 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| PCB 구성 요소 필수 암기 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [문맥 교환](/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) [TLB](/studynote/02_operating_system/06_memory_management/357_tlb/) 플러시 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[IPC 기법 성능 오버헤드]
    |
    v
[프로세스 주소 공간 분리 (Process Address Space Isolation)]
    |
    +---> [PCB 구성 요소 필수 암기]
    +---> [문맥 교환 TLB 플러시]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 옛날 컴퓨터는 넓은 운동장에 모든 학생(프로그램)을 풀어놓고 놀게 했어요. 그래서 한 친구가 칠해놓은 그림을 다른 친구가 실수로 밟아서 망치는 일이 매일 일어났죠.
2. 지금의 똑똑한 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 마법을 부려서 학생마다 밖이 보이지 않는 '나만의 투명한 방([가상 주소 공간](/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/))'을 하나씩 만들어 주었어요!
3. 모든 학생은 자기가 운동장을 통째로 혼자 쓴다고 착각하지만, 사실은 마법사([MMU](/studynote/02_operating_system/06_memory_management/328_mmu/))가 각자의 공간을 철저히 분리해 두었기 때문에 절대로 남의 그림을 밟거나 싸울 일이 없어졌답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 682 / 800

<- **이전**: [681. IPC 기법 성능 오버헤드 (IPC Performance Overhead)](/studynote/02_operating_system/11_exam_summary/681_ipc_performance_overhead/)
**다음**: [683. PCB 구성 요소 필수 암기 (PCB Process Control Block Components)](/studynote/02_operating_system/11_exam_summary/683_pcb_process_control_block_components/) ->

---
