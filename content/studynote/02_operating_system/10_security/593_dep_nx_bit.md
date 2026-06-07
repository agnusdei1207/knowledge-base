---
title: "NX Bit / Data Execution Prevention, DEP"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 593
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [DEP](/studynote/09_security/04_endpoint_security/336_dep/) ([Data Execution Prevention](/studynote/09_security/04_endpoint_security/336_dep/))와 [NX Bit](/studynote/09_security/04_endpoint_security/335_nx_bit/) ([No-eXecute Bit](/studynote/09_security/04_endpoint_security/335_nx_bit/))는 메모리 상의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 영역([스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/), 힙)에서 기계어 코드가 실행되는 것을 하드웨어 및 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) (OS, [Operating System](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)) 레벨에서 원천 차단하는 보안 기술이다.
> 2. **가치**: [버퍼 오버플로우](/studynote/02_operating_system/10_security/591_buffer_overflow/) ([Buffer Overflow](/studynote/02_operating_system/10_security/591_buffer_overflow/)) 취약점을 통해 주입된 악성 [셸코드](/studynote/02_operating_system/10_security/592_shellcode_injection/) ([Shellcode](/studynote/02_operating_system/10_security/592_shellcode_injection/))의 실행을 구조적으로 불가능하게 만들어, 공격자가 시스템 제어권을 쉽게 탈취하지 못하게 하는 현대 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 필수 방어선이다.
> 3. **융합**: 컴퓨터구조 ([CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/), Computer [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/))의 메모리 관리 유닛([MMU](/studynote/02_operating_system/06_memory_management/328_mmu/))의 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)([Page Table](/studynote/02_operating_system/06_memory_management/353_page_table/)) 속성을 OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 제어하여 보안을 달성하며, 이를 우회하기 위해 공격자들은 [ROP](/studynote/02_operating_system/10_security/596_return_oriented_programming/) ([Return-Oriented Programming](/studynote/02_operating_system/10_security/596_return_oriented_programming/))라는 새로운 공격 패러다임을 탄생시켰다.

---

## Ⅰ. 개요 및 필요성

**개념 및 정의**
[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 실행 방지 ([DEP](/studynote/09_security/04_endpoint_security/336_dep/), [Data Execution Prevention](/studynote/09_security/04_endpoint_security/336_dep/))는 시스템 메모리를 '코드(실행 가능)' 영역과 '[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(실행 불가)' 영역으로 엄격하게 분리하는 보안 메커니즘이다. 이를 하드웨어 수준에서 지원하는 것이 [NX Bit](/studynote/09_security/04_endpoint_security/335_nx_bit/) ([No-eXecute Bit](/studynote/09_security/04_endpoint_security/335_nx_bit/), 인텔에서는 XD [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)라 명명)이다. NX [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)된 메모리 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에서 CPU가 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 읽어 들여 실행하려고 시도하면, 즉시 예외(Exception)가 발생하고 OS는 해당 프로세스를 강제 종료시킨다.

**필요성 및 등장 배경**
전통적인 폰 노이만 ([Von Neumann](/studynote/01_computer_architecture/03_architecture_basics_performance/124_von_neumann/)) 아키텍처에서는 메모리 상의 '[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)'와 '[명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)(코드)'를 구조적으로 구분하지 않는다. 이러한 아키텍처적 특성 때문에, 공격자가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 입력 영역인 버퍼(Buffer)에 기계어 코드를 밀어 넣고 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 포인터(EIP/[RIP](/studynote/03_network/07_network_layer_routing/351_rip_routing_information_protocol_distance_vector_hop/))를 그곳으로 돌리면 CPU는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 코드로 인식하고 실행해 버리는 치명적인 문제가 존재했다.

```text
+---------------------------------------------------------------+
|      폰 노이만 아키텍처의 한계와 NX Bit 도입 배경 구조도      |
+---------------------------------------------------------------+
|                                                               |
|  [기존 메모리 모델 (NX Bit 미적용)]                           |
|  +------------+-------+------------------------------+        |
|  | 코드 영역   | 데이터| 스택 영역 (버퍼)               |     |
|  | (실행 허용) | 영역  | [ A, B, C, Shellcode ... ]   |       |
|  +------------+-------+---------^--------------------+        |
|       |                             |                         |
|       +-- CPU는 스택에 있는 데이터도 기계어 코드로 취급해     |
|           아무 의심 없이 실행함 (셸코드 실행 성공)            |
|                                                               |
|  [현대 메모리 모델 (NX Bit / DEP 적용)]                       |
|  +------------+-------+------------------------------+        |
|  | 코드 영역   | 데이터| 스택 영역 (버퍼)               |     |
|  | (r-x)      | (rw-) | (rw-)  [ Shellcode ... ]     |        |
|  +------------+-------+---------^--------------------+        |
|                                     |                         |
|      CPU가 스택에서 명령어를 인출(Fetch)하려고 시도할 때      |
|      NX Bit = 1 (실행 불가) 확인 -> 💥 Segmentation Fault      |
+---------------------------------------------------------------+
```

**[다이어그램 해설]** 이 구조도는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 실행 방지 기술이 폰 노이만 아키텍처의 근본적인 맹점을 어떻게 보완하는지를 보여준다. 기존 시스템에서는 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)([Stack](/studynote/08_algorithm_stats/04_datastructure/057_stack/))이나 힙([Heap](/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/)) 같은 메모리 영역에 읽기(r), [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(w)뿐만 아니라 실행(x) 권한이 암묵적으로 부여되어 있었다. 공격자는 이 점을 악용하여 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 위장한 [셸코드](/studynote/02_operating_system/10_security/592_shellcode_injection/)를 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)에 주입했다. [DEP](/studynote/09_security/04_endpoint_security/336_dep/)/NX Bit가 적용된 현대 OS는 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)의 각 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 속성에 '실행 방지' 플래그를 명시한다. 따라서 변조된 리턴 주소를 타고 실행 흐름이 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)으로 넘어오더라도, CPU 내의 메모리 관리 유닛([MMU](/studynote/02_operating_system/06_memory_management/328_mmu/))이 권한 위반을 탐지하고 하드웨어 예외를 발생시켜 프로세스를 안전하게 종료(Kill)해 버린다.

- **📢 섹션 요약 비유**: 책([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 읽는 용도이지 악보처럼 연주(실행)하는 용도가 아니므로, 도서관(메모리)에서 누군가 책을 소리 내어 연주하려고 하면 경비원(CPU)이 즉시 쫓아내는 규칙과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소 (하드웨어 및 OS 레벨 통합 구조)

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| <strong><a href="/studynote/09_security/04_endpoint_security/335_nx_bit/">NX Bit</a> (<a href="/studynote/09_security/04_endpoint_security/335_nx_bit/">No-eXecute Bit</a>)</strong> | 하드웨어적 실행 통제 | 64비트 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 엔트리(PTE)의 63번째 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 1로 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | AMD NX, Intel XD (eXecute Disable) | 출입증의 "직원 전용" 마크 |
| <strong><a href="/studynote/02_operating_system/06_memory_management/328_mmu/">MMU</a> (<a href="/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/">Memory Management Unit</a>)</strong> | 메모리 접근 권한 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 인출([Instruction](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Fetch) 시 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)의 NX [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 워크 ([Page Table](/studynote/02_operating_system/06_memory_management/353_page_table/) Walk) | 검문소의 경비원 |
| <strong><a href="/studynote/02_operating_system/07_virtual_memory/387_page_fault/">Page Fault</a> Exception (예외)</strong> | 권한 위반 탐지 시 OS 호출 | NX [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 위반 시 [하드웨어 인터럽트](/studynote/02_operating_system/01_overview_architecture/017_hardware_interrupt/)([Trap](/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/)) 발생 | [인터럽트 벡터](/studynote/02_operating_system/01_overview_architecture/019_interrupt_vector/) ([Interrupt Vector](/studynote/02_operating_system/01_overview_architecture/019_interrupt_vector/)) | 무단 침입 경보벨 |
| <strong><a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> <a href="/studynote/09_security/04_endpoint_security/336_dep/">DEP</a> 매니저</strong> | 프로세스 강제 종료 | 예외 발생 시 해당 프로세스에 SIGSEGV 시그널 전송 | 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/), Windows 윈도우 디펜더 | 경찰의 강제 진압 |

### 심층 동작 원리 및 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 제어

DEP의 구현은 CPU의 하드웨어 지원([NX Bit](/studynote/09_security/04_endpoint_security/335_nx_bit/))과 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 관리가 완벽히 맞물려 동작한다. x86 아키텍처에서는 PAE ([Physical Address](/studynote/02_operating_system/06_memory_management/323_physical_address/) Extension) 모드를 활성화하거나 64비트 환경을 사용해야만 64비트 크기의 PTE ([Page Table](/studynote/02_operating_system/06_memory_management/353_page_table/) Entry)를 사용할 수 있고, 이 PTE의 최상위 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)(63번째 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/))가 바로 NX [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)로 사용된다.

```text
+-------------------------------------------------------------+
|      64비트 페이지 테이블 엔트리(PTE) 구조와 NX Bit 검증    |
+-------------------------------------------------------------+
|                                                             |
|  [페이지 테이블 엔트리 (PTE: 64 Bits)]                      |
|   63                                             0          |
|  +--+-----------------------------+--+--+--+--+--+          |
|  |NX|        Physical Frame       |  |  |  |R/|P |          |
|  |  |        Address (Base)       |  |  |  |W |  |          |
|  +--+-----------------------------+--+--+--+--+--+          |
|   ^                                         ^  ^            |
|   |                                         |  |            |
|   |                                         |  +-- Present (메모리 존재 여부)
|   |                                         +-- Read/Write (읽기/쓰기 권한)
|   +-- NX Bit (1 = 실행 불가, 0 = 실행 가능)                 |
|                                                             |
|  [CPU 명령어 인출(Fetch) 파이프라인]                        |
|   PC(EIP/RIP)가 가리키는 주소의 명령어 요청                 |
|             v                                               |
|   MMU가 해당 가상 주소의 PTE 검색                           |
|             v                                               |
|   IF (PTE.NX == 1) {                                        |
|       발생: Page Fault Exception (Access Violation)         |
|       결과: 커널이 프로세스를 SIGSEGV로 강제 종료           |
|   } ELSE {                                                  |
|       명령어 정상 인출 및 파이프라인 실행                   |
|   }                                                         |
+-------------------------------------------------------------+
```

**[다이어그램 해설]** 이 타이밍 및 로직 구조도는 하드웨어 수준에서 [셸코드](/studynote/02_operating_system/10_security/592_shellcode_injection/)가 어떻게 차단되는지를 보여준다. 프로세스가 메모리를 할당받을 때, OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)([Stack](/studynote/08_algorithm_stats/04_datastructure/057_stack/))과 힙([Heap](/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/)) 영역에 대응하는 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 엔트리(PTE)의 63번째 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)([NX Bit](/studynote/09_security/04_endpoint_security/335_nx_bit/))를 `1`로 세팅한다. 공격자가 [버퍼 오버플로우](/studynote/02_operating_system/10_security/591_buffer_overflow/)를 성공시켜 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 포인터(EIP/[RIP](/studynote/03_network/07_network_layer_routing/351_rip_routing_information_protocol_distance_vector_hop/))를 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 영역으로 돌려놓더라도, CPU가 그 주소에서 다음 기계어를 가져오려고(Fetch) 시도하는 순간 MMU가 개입한다. MMU는 PTE를 읽고 NX Bit가 `1`인 것을 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하여, 즉각적으로 접근 위반 예외(Access Violation Exception)를 발생시킨다. [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 이 예외를 가로채어 악의적인 행위로 간주하고 프로세스를 즉사(Kill)시킨다.

- **📢 섹션 요약 비유**: 건물(시스템)의 모든 방([페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)) 문에 '창고용([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))'과 '사무용(코드)' 팻말을 붙여두고, 직원이 창고용 방에서 사무를 보려고 하면 경보기가 울려 바로 퇴장시키는 보안 시스템과 같습니다.

---

## Ⅲ. 비교 및 연결

### 하드웨어 [DEP](/studynote/09_security/04_endpoint_security/336_dep/) vs 소프트웨어 [DEP](/studynote/09_security/04_endpoint_security/336_dep/) 비교

DEP는 구현 방식에 따라 하드웨어 기반과 소프트웨어 기반으로 나뉜다. 하드웨어 DEP가 완전한 방어를 제공하는 반면, 구형 시스템에서는 소프트웨어적 기법을 우회적으로 사용했다.

| 비교 항목 | 하드웨어 기반 [DEP](/studynote/09_security/04_endpoint_security/336_dep/) (Hardware [DEP](/studynote/09_security/04_endpoint_security/336_dep/)) | 소프트웨어 기반 [DEP](/studynote/09_security/04_endpoint_security/336_dep/) (Software [DEP](/studynote/09_security/04_endpoint_security/336_dep/) / SafeSEH) |
|:---|:---|:---|
| **기반 기술** | CPU의 NX / XD [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) (PTE 63번 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)) | OS의 예외 처리 체인 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) (Windows SafeSEH 등) |
| **방어 대상** | 메모리 상의 기계어 코드 직접 실행 | 예외 처리기(Exception Handler) 주소 변조 조작 |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 오버헤드</strong> | 거의 없음 ([MMU](/studynote/02_operating_system/06_memory_management/328_mmu/) 하드웨어 로직으로 처리) | 소프트웨어 로직 추가로 인한 약간의 오버헤드 존재 |
| <strong><a href="/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a></strong> | 매우 높음 (우회 불가, 구조적 차단) | 우회 가능성 존재 ([설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 오류 등) |
| **요구 사항** | PAE 지원 CPU 및 64비트 아키텍처 필수 | CPU와 무관하게 OS 단에서 지원 가능 |

소프트웨어 [DEP](/studynote/09_security/04_endpoint_security/336_dep/)(주로 윈도우 환경)는 실제로 메모리 실행을 하드웨어 레벨에서 막는 것이 아니라, [버퍼 오버플로우](/studynote/02_operating_system/10_security/591_buffer_overflow/)가 예외 처리 핸들러(SEH, Structured Exception Handler)를 덮어쓰는 기법을 차단하기 위해 유효한 핸들러 목록을 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 방식이다. 따라서 진정한 의미의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 실행 방지는 하드웨어 DEP를 지칭한다.

```text
+------------------------------------------------------------+
|      메모리 영역별 권한 (Permissions) 및 취약성 비교       |
+------------------------------------------------------------+
|                                                            |
|  [권한 매트릭스]                                           |
|  영역 (Segment)  | Read | Write | Execute |  보안 취약점   |
|  ---------------+------+-------+---------+-----------------+
|  .text (코드)    |  O   |   X   |    O    |  Read-Only로   |
|                  |      |       |         |  덮어쓰기 불가 |
|  ---------------+------+-------+---------+-----------------+
|  .data / .bss    |  O   |   O   |  X(DEP) |  데이터 조작,  |
|  (전역 변수)     |      |       |         |  코드 실행 불가|
|  ---------------+------+-------+---------+-----------------+
|  Stack (스택)    |  O   |   O   |  X(DEP) |  코드 실행 불가|
|                  |      |       |         | (셸코드 무력화)|
|  ---------------+------+-------+---------+-----------------+
|  Heap (힙)       |  O   |   O   |  X(DEP) |  코드 실행 불가|
|                                                            |
|  [W^X (Write XOR Execute) 보안 정책]                       |
|  어떤 메모리 페이지도 '쓰기(Write)'와 '실행(Execute)'      |
|  권한을 동시에 가질 수 없다는 현대 OS의 강력한 보안 원칙.  |
|  -> Write가 가능하면 Execute 불가, Execute가 가능하면 Write 불가.
+------------------------------------------------------------+
```

**[다이어그램 해설]** 이 표는 DEP의 철학적 기반인 **W^X (Write XOR Execute)** [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 명확하게 보여준다. 공격자가 코드를 삽입하려면 대상 메모리에 반드시 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(W) 권한이 있어야 한다. 그리고 그 코드를 동작시키려면 실행(X) 권한이 필요하다. 과거 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)과 힙은 W와 X를 동시에 허용(RWX)하는 치명적 결함을 가지고 있었다. [DEP](/studynote/09_security/04_endpoint_security/336_dep/) 적용 후, 코드 영역(.text)은 RX로 제한되어 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 불가능해졌고, [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)과 힙은 RW로 제한되어 실행이 불가능해졌다. 교집합(RWX)을 완전히 제거함으로써, [셸코드](/studynote/02_operating_system/10_security/592_shellcode_injection/) 주입 자체를 무의미하게 만들어버린 가장 우아하고 강력한 아키텍처적 방어 체계다.

- **📢 섹션 요약 비유**: 물([쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))과 불(실행)이 동시에 한 공간에 있을 수 없도록 설계하여, 침입자가 화약([셸코드](/studynote/02_operating_system/10_security/592_shellcode_injection/))에 불을 붙이려고 시도하면 즉시 소화기(Exception)가 터져버리는 튼튼한 방화 구조와 같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: [DEP](/studynote/09_security/04_endpoint_security/336_dep/) 우회를 위한 [ROP](/studynote/02_operating_system/10_security/596_return_oriented_programming/)([Return-Oriented Programming](/studynote/02_operating_system/10_security/596_return_oriented_programming/)) 공격의 등장

1. **상황**: 기업의 웹 서버 애플리케이션에 [버퍼 오버플로우](/studynote/02_operating_system/10_security/591_buffer_overflow/) 취약점이 발견되었다. 그러나 서버 OS에는 [DEP](/studynote/09_security/04_endpoint_security/336_dep/)/NX Bit가 완벽하게 적용되어 있어, 해커가 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)에 [셸코드](/studynote/02_operating_system/10_security/592_shellcode_injection/)를 주입하고 리턴 주소를 그곳으로 돌리자마자 `SIGSEGV`로 프로세스가 종료되며 공격이 차단되었다.
2. <strong>공격자의 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> (<a href="/studynote/02_operating_system/10_security/596_return_oriented_programming/">ROP</a>)</strong>: 해커는 자신이 작성한 [셸코드](/studynote/02_operating_system/10_security/592_shellcode_injection/)를 실행할 수 없다는 것을 깨닫고 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 수정한다. 대신, 이미 실행 권한(RX)을 가지고 메모리에 로드되어 있는 정상적인 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)(예: `libc.so` 내의 함수들)에 존재하는 자잘한 코드 조각([가젯](/studynote/09_security/04_endpoint_security/345_gadget_rop/), Gadget - `pop eax; ret;` 등)들의 주소를 수집한다. 공격자는 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)에 [셸코드](/studynote/02_operating_system/10_security/592_shellcode_injection/)가 아닌, 이 [가젯](/studynote/09_security/04_endpoint_security/345_gadget_rop/)들의 '주소(Address)'들을 체인처럼 연결하여 덮어쓴다. 리턴 주소를 첫 번째 [가젯](/studynote/09_security/04_endpoint_security/345_gadget_rop/)으로 돌리면, `ret` 명령이 연속적으로 실행되며 공격자가 원하는 궁극적인 함수(예: `system("/bin/sh")` 또는 `mprotect()`를 이용한 [DEP](/studynote/09_security/04_endpoint_security/336_dep/) 해제)가 호출된다.
3. **방어자의 의사결정**: [DEP](/studynote/09_security/04_endpoint_security/336_dep/) 단독으로는 ROP와 같은 코드 재사용 공격(Code-Reuse Attack)을 막을 수 없다. 따라서 실무 아키텍트는 DEP와 더불어 <strong><a href="/studynote/02_operating_system/06_memory_management/374_aslr/">ASLR</a> (주소 공간 무작위화)</strong>를 반드시 함께 적용해야 한다. [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)의 주소가 계속 바뀌면 공격자가 [가젯](/studynote/09_security/04_endpoint_security/345_gadget_rop/)의 주소를 찾을 수 없어 [ROP](/studynote/02_operating_system/10_security/596_return_oriented_programming/) 체인을 구성할 수 없게 된다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **컴파일러 옵션 강제화**: 소프트웨어 빌드 파이프라인([CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD)에서 모든 바이너리에 대해 `gcc -z noexecstack` (리눅스) 및 `/NXCOMPAT` (윈도우 MSVC) 옵션이 강제로 적용되었는지 [정적 분석](/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) 도구([SAST](/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/))로 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해야 한다.
- <strong><a href="/studynote/09_security/11_iam_access_control/568_jit_access/">JIT</a> 컴파일러 예외 관리</strong>: V8 (JavaScript) 엔진과 같이 실행 중(Run-time)에 기계어를 동적으로 생성해야 하는 [JIT](/studynote/09_security/11_iam_access_control/568_jit_access/)([Just-In-Time](/studynote/09_security/11_iam_access_control/568_jit_access/)) 컴파일러는 필연적으로 RWX 권한을 요구하는 경우가 많다. 이 경우 W와 X를 시분할로 번갈아 가며 부여하는 [JIT](/studynote/09_security/11_iam_access_control/568_jit_access/) 전용 보안 완화 기술이 적용되었는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong><code>mprotect()</code> / <code>VirtualProtect()</code> 남용</strong>: 프로그래머가 코드 내에서 메모리 권한을 변경하는 API를 사용하여 특정 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 영역을 `PROT_EXEC` (RWX)로 강제 변경하는 행위. 공격자는 ROP를 이용해 이 함수들을 먼저 호출하여 DEP를 스스로 해제시킨 뒤, [셸코드](/studynote/02_operating_system/10_security/592_shellcode_injection/)를 실행하는 방식으로 방어망을 무력화한다.

- **📢 섹션 요약 비유**: 범죄자(해커)가 직접 가져온 불법 총기([셸코드](/studynote/02_operating_system/10_security/592_shellcode_injection/)) 사용이 금지([DEP](/studynote/09_security/04_endpoint_security/336_dep/))되자, 경찰서 내부에 이미 합법적으로 존재하는 경찰관들의 총기(정상 코드 조각)를 교묘하게 조종하여 범죄를 저지르는([ROP](/studynote/02_operating_system/10_security/596_return_oriented_programming/)) 우회 전술과 같습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [DEP](/studynote/09_security/04_endpoint_security/336_dep/) 미적용 시 | [DEP](/studynote/09_security/04_endpoint_security/336_dep/) 전면 적용 시 | 기술적 함의 |
|:---|:---|:---|:---|
| **정량** | [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 기반 RCE 취약점의 100% 직격 | 직접적인 [셸코드](/studynote/02_operating_system/10_security/592_shellcode_injection/) 기반 침해율 **사실상 0% 근접** | 침해사고 대응 비용([MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/))의 획기적 감소 |
| **정성** | 초보 해커(Script Kiddie)도 쉽게 셸 권한 획득 | [ROP](/studynote/02_operating_system/10_security/596_return_oriented_programming/) 등 고난도 기법을 강제하여 공격 난이도 급상승 | 위협 행위자(Threat Actor)의 진입 장벽 형성 |
| **운영** | 서버 크래시(Crash) 발생 후 원인 파악 어려움 | OS 차원의 예외 로그를 통해 즉각적 공격 탐지 | 보안 관제([SIEM](/studynote/09_security/13_secops_ir_forensics/624_siem/)) 알람과 연동하여 가시성 확보 |

### 미래 전망
[DEP](/studynote/09_security/04_endpoint_security/336_dep/)/NX Bit는 현대 OS 보안의 가장 기초적이고 필수적인 표준이 되었다. 그러나 앞서 언급한 [ROP](/studynote/02_operating_system/10_security/596_return_oriented_programming/) 공격에 의해 방어의 한계가 명확해졌다. 향후 기술의 진화는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 실행을 막는 것에서 더 나아가, **'정상적인 실행 흐름 자체를 이탈하지 못하게'** 하는 기술로 옮겨가고 있다. 인텔(Intel)이 도입한 **CET (Control-flow Enforcement Technology)** 가 대표적이다. CET는 섀도우 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) (Shadow [Stack](/studynote/08_algorithm_stats/04_datastructure/057_stack/))을 하드웨어적으로 구현하여, 원래 함수가 저장해둔 리턴 주소와 ROP로 변조된 리턴 주소를 CPU 칩 레벨에서 비교·[검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)함으로써 [ROP](/studynote/02_operating_system/10_security/596_return_oriented_programming/) 공격마저 원천 차단하는 혁신적인 진화를 보여주고 있다.

### 참고 표준
- **CWE-284**: 부적절한 접근 제어 (Improper [Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/) - 메모리 영역 권한)
- <strong>NIST <a href="/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/">SP</a> 800-115</strong>: 기술적 보안 통제 및 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 가이드
- <strong>POSIX <code>mprotect()</code> <a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a> 규약</strong>: 프로세스 주소 공간 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)

- **📢 섹션 요약 비유**: 낡은 자물쇠(소프트웨어 패치) 대신 집 전체의 구조를 강철 프레임(하드웨어 [NX Bit](/studynote/09_security/04_endpoint_security/335_nx_bit/))으로 바꾸어 놓은 혁신이며, 해커들은 이 강철 프레임을 부수는 대신 환기구([ROP](/studynote/02_operating_system/10_security/596_return_oriented_programming/))를 찾는 방식으로 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 바꿀 수밖에 없었습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [버퍼 오버플로우](/studynote/02_operating_system/10_security/591_buffer_overflow/) ([Buffer Overflow](/studynote/02_operating_system/10_security/591_buffer_overflow/)) 원리 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [셸코드](/studynote/02_operating_system/10_security/592_shellcode_injection/) ([Shellcode](/studynote/02_operating_system/10_security/592_shellcode_injection/)) [인젝션](/studynote/04_software_engineering/11_testing_validation/872_injection/) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [가상 주소 공간](/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/) 구조 무작위화 ([ASLR](/studynote/02_operating_system/06_memory_management/374_aslr/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) ([Canary](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)) / [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 스매싱 가드 ([Stack Smashing Protector](/studynote/01_computer_architecture/15_advanced_topics/541_stack_smashing_protector/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[셸코드 (Shellcode) 인젝션]
    |
    v
[버퍼 오버플로우 방어 하드웨어 기술 (NX Bit / Data Execution Prevention, DEP)]
    |
    +---> [가상 주소 공간 구조 무작위화 (ASLR)]
    +---> [카나리 (Canary) / 스택 스매싱 가드 (Stack Smashing Protector)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 메모리는 엄청나게 큰 도서관이고, 이 안에는 <strong>책(<a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>)</strong> 도 있고 **영화(실행 코드)** 도 있어요.
2. 예전에는 나쁜 해커가 책 사이에 몰래 무서운 영화([셸코드](/studynote/02_operating_system/10_security/592_shellcode_injection/))를 끼워 넣으면 컴퓨터가 실수로 그걸 틀어버렸어요.
3. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 실행 방지([DEP](/studynote/09_security/04_endpoint_security/336_dep/))는 "책 보관소에서는 절대로 영화를 틀 수 없다!"라는 튼튼한 자물쇠(규칙)를 만들어서 해커의 속임수를 완벽하게 막아내는 기술이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 593 / 800

<- **이전**: [592. 셸코드 (Shellcode) 인젝션](/studynote/02_operating_system/10_security/592_shellcode_injection/)
**다음**: [594. 가상 주소 공간 구조 무작위화 (ASLR) - 버퍼/스택 라이브러리 주소 랜덤 배치 방어망](/studynote/02_operating_system/10_security/594_aslr_address_space_layout_randomization/) ->

---
