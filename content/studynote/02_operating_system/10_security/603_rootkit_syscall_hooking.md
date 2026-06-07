---
title: "603. Rootkit Syscall Hooking"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 603
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 루트킷 (Rootkit)은 시스템의 최고 관리자 권한(Root)을 탈취한 후, [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) (OS, [Operating System](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)) [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내부로 숨어들어 자신의 존재와 악성 행위를 시스템 관리자 및 보안 솔루션으로부터 완벽하게 은폐하는 최고도 수준의 악성코드 패키지다.
> 2. **가치**: 애플리케이션 레벨의 해킹을 넘어 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 핵심 자료구조(시스템 콜 테이블 등)를 조작하므로, 기존의 안티바이러스나 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 검사 도구마저 거짓 결과를 출력하게 만드는 '시스템 신뢰 붕괴'의 정점에 서 있다.
> 3. **융합**: 컴퓨터구조 ([CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/))의 [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/)([Virtual File System](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/)), [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 처리, [가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 관리와 깊게 연동되며, 이를 방어하기 위해 하드웨어 기반의 [보안 부팅](/studynote/02_operating_system/10_security/608_secure_boot/)([Secure Boot](/studynote/02_operating_system/10_security/608_secure_boot/))과 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 서명([Module](/studynote/04_software_engineering/04_testing_quality/192_module_independence/) Signature) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 아키텍처가 융합되어 발전했다.

---

## Ⅰ. 개요 및 필요성

**개념 및 정의**
루트킷 (Rootkit)은 'Root(최고 관리자 권한)'와 'Kit(도구 모음)'의 합성어로, 공격자가 시스템에 무단 침입한 뒤 [백도어](/studynote/03_network/14_network_security_threats/737_backdoor_c2_beacon_behavior_analysis/)([Backdoor](/studynote/09_security/15_malware_attack_vectors/727_backdoor/))를 설치하고 지속적인 제어권을 유지하기 위해 자신의 흔적(프로세스, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 네트워크 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 등)을 OS 레벨에서 숨겨주는 악성 프로그램 세트다. 동작하는 권한 계층에 따라 유저 모드(User-mode) 루트킷과 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드([Kernel](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)-mode) 루트킷으로 나뉜다.

**필요성 및 등장 배경**
해커가 [제로 데이](/studynote/02_operating_system/10_security/597_zero_day_exploit/)나 버퍼 오버플로우를 통해 루트 권한을 획득하더라도, 단순히 [백도어](/studynote/03_network/14_network_security_threats/737_backdoor_c2_beacon_behavior_analysis/) 데몬을 띄워놓으면 관리자가 `ps`, `netstat`, `ls` 같은 기본 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 치거나 백신을 돌렸을 때 즉각 감지된다. 공격자는 "OS 자체가 거짓말을 하게 만들면 아무도 나를 찾을 수 없다"는 발상을 하게 되었다. 이를 위해 해커는 관리자가 사용하는 진단 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)들이 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 정보를 요청할 때, 그 응답값을 중간에서 조작(Hooking)하여 악성코드의 존재만 쏙 빼고 정상인 것처럼 반환하게 만드는 [커널 루트킷](/studynote/09_security/04_endpoint_security/360_kernel_rootkit/)을 탄생시켰다.

```text
+------------------------------------------------------------+
|      정상적인 시스템 모니터링 vs 루트킷 감염 시의 은폐 과정 |
+------------------------------------------------------------+
|                                                            |
|  [정상 시스템 (루트킷 없음)]                               |
|  관리자 --(명령: ps -ef)---> OS 커널 (시스템 콜 처리)      |
|                                 |                          |
|  OS 응답: "현재 프로세스는 [httpd], [sshd], [hack_bot] 임" |
|  => 관리자: "어? hack_bot? 악성코드 발견! 삭제!"           |
|                                                            |
|  [커널 루트킷 감염 시스템 (OS 자체의 신뢰 붕괴)]           |
|  관리자 --(명령: ps -ef)---> OS 커널 --+                   |
|                                          v                 |
|                              +-------------------------+   |
|                              | [루트킷의 System Call Hook] | |
|                              | OS가 수집한 목록 중         | |
|                              | 'hack_bot' 항목만 삭제함!   | |
|                              +-----------+-------------+   |
|                                          |                 |
|  조작된 응답 <----------------------------+                 |
|  "현재 프로세스는 [httpd], [sshd] 임 (거짓말)"             |
|  => 관리자: "음, 내 서버는 완벽히 깨끗하군!"               |
+------------------------------------------------------------+
```

**[다이어그램 해설]** 이 그림은 루트킷의 본질적인 공포, 즉 "OS가 관리자를 속인다"는 메커니즘을 보여준다. 유저 영역의 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)(`ls`, `ps`)들은 결국 하드디스크의 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이나 메모리의 프로세스 정보를 읽기 위해 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에게 시스템 콜을 요청해야 한다. [커널 루트킷](/studynote/09_security/04_endpoint_security/360_kernel_rootkit/)은 이 연결 고리의 정중앙을 장악(후킹)하여, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 정상적으로 읽어온 결과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 자신의 악성 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이나 악성 네트워크 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)([포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)) 정보만 지워버린 뒤 유저에게 돌려준다. 관리자는 OS가 제공하는 도구를 100% 신뢰하지만, 그 도구의 근간이 되는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 자체가 부패했으므로 악성코드를 절대 눈치챌 수 없다.

- **📢 섹션 요약 비유**: 은행을 터는 도둑이 단순히 CCTV를 부수는 게 아니라, [CCTV](/studynote/09_security/18_iot_ot_physical/933_cctv/) 관제실의 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/) 선을 조작하여 도둑이 없는 평온한 복도 화면만 반복해서 보여주게 만들어, 경비원(관리자)이 화면만 보고 안심하게 만드는 교활한 전술과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소 ([커널 루트킷](/studynote/09_security/04_endpoint_security/360_kernel_rootkit/)의 후킹 타겟)

| 요소명 | 역할 | 내부 동작 | 비유 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/02_operating_system/01_overview_architecture/067_lkm/">LKM</a> (Loadable <a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">Kernel</a> <a href="/studynote/04_software_engineering/04_testing_quality/192_module_independence/">Module</a>)</strong> | 루트킷을 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 공간에 삽입하는 매개체 | `insmod` 명령으로 동적으로 악성 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈 적재](/studynote/02_operating_system/01_overview_architecture/067_lkm/) | 시스템(성) 내부에 합법적으로 진입하는 마차 |
| <strong><a href="/studynote/02_operating_system/01_overview_architecture/013_system_call/">System Call</a> Table</strong> | 가장 고전적인 후킹 지점 | `sys_call_table`의 메모리 주소를 악성 함수 주소로 덮어쓰기 | 성의 이정표(표지판) 방향을 몰래 바꾸기 |
| <strong><a href="/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/">VFS</a> (<a href="/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/">Virtual File System</a>) 객체</strong> | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 은폐의 핵심 타겟 | inode, dentry의 함수 포인터(readdir 등)를 조작 | 문서 보관소 직원을 매수해 특정 서류 숨기기 |
| <strong>DKOM (<a href="/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/">Direct</a> <a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">Kernel</a> Object Manipulation)</strong> | 최신/최고 난이도 루트킷 기법 | 리눅스의 `task_struct` 연결 리스트를 직접 끊어 프로세스 은폐 | 호적(주민등록부)에서 이름 자체를 물리적으로 파내기 |

### 심층 동작 원리: 시스템 콜 테이블 후킹 ([System Call](/studynote/02_operating_system/01_overview_architecture/013_system_call/) Table Hooking)

초기이자 가장 널리 쓰인 [커널 루트킷](/studynote/09_security/04_endpoint_security/360_kernel_rootkit/)의 동작 방식은 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리 내부에 존재하는 <strong>시스템 콜 테이블(<a href="/studynote/02_operating_system/01_overview_architecture/013_system_call/">System Call</a> Table)</strong> 의 함수 포인터를 조작하는 것이다. 리눅스에서 `sys_call_table`은 각 시스템 콜 번호(예: `sys_read`, `sys_getdents`)와 실제 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 함수의 주소를 매핑해둔 거대한 배열이다.

```text
+------------------------------------------------------------+
|      LKM 기반 System Call Table 후킹 및 은폐 메커니즘      |
+------------------------------------------------------------+
|                                                            |
|  [1. 정상적인 커널 상태 (Hooking 전)]                      |
|   유저 요청: ls 명령 (시스템 콜: sys_getdents 호출)        |
|                |                                           |
|  [ sys_call_table 배열 (커널 메모리) ]                     |
|  인덱스 77 : [ 0xffffffff81234000 ] ---> 진짜 sys_getdents()|
|                                           (모든 파일 반환) |
|                                                            |
|  [2. 루트킷(LKM) 적재 및 테이블 조작 (Hooking 후)]         |
|   해커가 메모리 보호(CR0 레지스터 WP 비트)를 해제하고,     |
|   배열의 포인터를 자신이 만든 악성 함수로 덮어씀.          |
|                                                            |
|  [ 변조된 sys_call_table ]                                 |
|  인덱스 77 : [ 0xffffffffc0011000 ] ---> 악성 fake_getdents() |
|                                            |               |
|                    +-----------------------+               |
|                    v                                       |
|      ① 진짜 sys_getdents() 를 백그라운드에서 몰래 호출     |
|      ② 결과 리스트에서 "rootkit_virus.ko" 텍스트 삭제 처리 |
|      ③ 깔끔하게 조작된 결과를 유저의 'ls' 명령에 반환      |
+------------------------------------------------------------+
```

**[다이어그램 해설]** 이 구조도는 [LKM](/studynote/02_operating_system/01_overview_architecture/067_lkm/)(적재 가능 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)) 루트킷이 어떻게 OS의 눈과 귀를 가리는지 보여준다. 유저 영역의 `ls` [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)는 [디렉터리](/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 목록을 읽기 위해 시스템 콜 `sys_getdents`(또는 `getdents64`)를 호출한다. 루트킷은 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 방지(WP, Write-Protect) 기능을 해제한 뒤, 시스템 콜 테이블 배열에서 `sys_getdents`가 위치한 인덱스의 함수 포인터를 자신이 작성한 가짜 함수(`fake_getdents`)의 주소로 덮어쓴다. 이제부터 시스템 내의 모든 `ls` 명령은 해커의 가짜 함수를 거치게 된다. 가짜 함수는 진짜 함수를 몰래 실행해 전체 목록을 받아온 뒤, 자신의 악성 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 이름만 쏙 빼고 결과를 반환하므로 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 상에서 루트킷은 완벽히 투명해진다(Invisible).

- **📢 섹션 요약 비유**: 전화 교환국의 배선판(시스템 콜 테이블)을 몰래 조작하여, 경찰서(ls [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/))로 가는 모든 전화를 먼저 해커의 비밀 사무실(가짜 함수)로 연결되게 한 뒤, 해커가 불리한 내용을 빼고 경찰서에 통화를 넘겨주는 감청/조작 시스템과 같습니다.

---

## Ⅲ. 비교 및 연결

### User-Mode 루트킷 vs [Kernel](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)-Mode 루트킷의 차원

루트킷은 시스템 아키텍처의 어느 링(Ring)에서 동작하느냐에 따라 난이도와 파괴력이 극명하게 갈린다.

| 비교 항목 | User-Mode 루트킷 (Ring 3) | [Kernel](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)-Mode 루트킷 (Ring 0) |
|:---|:---|:---|
| **동작 위치 및 권한** | 애플리케이션 계층, `LD_PRELOAD` 환경변수 조작, [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 후킹 | OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내부, [모듈 적재](/studynote/02_operating_system/01_overview_architecture/067_lkm/), [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 포인터 조작, DKOM |
| **은폐 대상** | `ls`, `ps`, `netstat` 등 특정 바이너리 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 자체를 변조하거나 `libc` 후킹 | 시스템 콜 테이블, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 자료구조 자체를 변조 |
| **탐지 난이도** | 중간 ([무결성](/studynote/09_security/01_intro_principles/003_integrity/) 검사 도구인 Tripwire, 백신 등으로 쉽게 탐지됨) | **극상** (OS 자체가 오염되었으므로 로컬 백신도 무력화됨) |
| **안정성 (Crash 위험)** | 구현이 쉽고 잘못 짜여도 해당 프로세스만 죽음 (Segfault) | 구현이 극도로 어렵고 1바이트 실수 시 <strong><a href="/studynote/02_operating_system/01_overview_architecture/036_kernel_panic/">Kernel Panic</a> (블루스크린/멈춤)</strong> 발생 |
| **우회 기법 예시** | `IAT/GOT` (Import Address Table) 후킹 | `IDT` ([인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 테이블) 후킹, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 오브젝트 직접 조작(DKOM) |

현대의 최상위 [APT](/studynote/09_security/15_malware_attack_vectors/748_apt/)([지능형 지속 위협](/studynote/09_security/04_endpoint_security/374_apt/)) 해커들은 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 넘어 아예 메인보드의 [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/)(BIOS/[UEFI](/studynote/01_computer_architecture/15_advanced_topics/706_uefi/))나 [부트로더](/studynote/02_operating_system/01_overview_architecture/029_bootloader/) 레벨에 감염되는 <strong><a href="/studynote/09_security/04_endpoint_security/362_bootkit/">부트킷</a>(<a href="/studynote/09_security/04_endpoint_security/362_bootkit/">Bootkit</a>)</strong>이나 [가상화 하이퍼바이저](/studynote/02_operating_system/11_exam_summary/743_virtualization_hypervisor/) 층에 숨는 초고도화된 기술까지 사용한다.

```text
+------------------------------------------------------------+
|      운영체제 권한 계층(Ring Architecture)과 루트킷의 깊이 |
+------------------------------------------------------------+
|                                                            |
|   [ 하드웨어 (Ring -1 / -2) ] ---> Firmware/Hypervisor Rootkit |
|        (운영체제조차 자신의 아래에 하이퍼바이저가 있는지 모름) |
|           ^                                                |
|   [ OS 커널 (Ring 0) ] ----------> Kernel Rootkit (LKM, DKOM)|
|        (시스템 콜, 파일시스템, 프로세스 스케줄러 완전 장악) |
|           ^                                                |
|   [ 유저 공간 (Ring 3) ] --------> User Rootkit (LD_PRELOAD) |
|        (일반적인 백신, 앱, 관리자 명령어 실행 영역)        |
|                                                            |
|  ※ 핵심 원리: "높은 권한(아래쪽 계층)은 낮은 권한(위쪽 계층)을|
|               완벽하게 기만하고 속일 수 있다."             |
+------------------------------------------------------------+
```

**[다이어그램 해설]** 이 다이어그램은 루트킷의 파괴력이 컴퓨터구조의 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 링([Protection](/studynote/02_operating_system/10_security/571_protection_vs_security/) Ring)과 직결되어 있음을 보여준다. 백신([Anti-Virus](/studynote/09_security/04_endpoint_security/323_antivirus/)) 프로그램은 보통 Ring 0([커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))와 Ring 3(유저)에 걸쳐 동작한다. 만약 루트킷이 유저 모드(Ring 3)에 있다면 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 권한을 빌려 쉽게 탐지하고 삭제할 수 있다. 하지만 루트킷이 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드(Ring 0)를 먼저 장악해버리면, 같은 Ring 0에 있는 백신에게 거짓 정보를 주어 무력화시킨다. 한발 더 나아가, [부트킷](/studynote/09_security/04_endpoint_security/362_bootkit/)([Bootkit](/studynote/09_security/04_endpoint_security/362_bootkit/))처럼 OS가 로드되기 전인 [UEFI](/studynote/01_computer_architecture/15_advanced_topics/706_uefi/) [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/)나 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 층(Ring -1)에 자리 잡으면, OS를 포맷하고 재설치해도 루트킷이 살아남아 계속해서 시스템을 감염시키는 좀비 같은 생명력을 가지게 된다.

- **📢 섹션 요약 비유**: 유저 모드 루트킷이 직원들의 서류철을 몰래 훔쳐보는 사기꾼이라면, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드 루트킷은 회사 사장(OS)의 뇌를 세뇌시킨 최면술사이고, [부트킷](/studynote/09_security/04_endpoint_security/362_bootkit/)은 아예 건물(하드웨어)의 설계도 자체에 비밀 통로를 만들어놓고 건물을 부수고 다시 지어도 나타나는 설계자입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: [커널 루트킷](/studynote/09_security/04_endpoint_security/360_kernel_rootkit/) 탐지 및 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 서명([Module](/studynote/04_software_engineering/04_testing_quality/192_module_independence/) Signature) 방어

1. **상황**: 기업의 핵심 DB 서버가 외부 해킹에 의해 루트 권한을 탈취당했다. 이후 해커는 LKM을 이용해 [커널 루트킷](/studynote/09_security/04_endpoint_security/360_kernel_rootkit/)을 적재하여 자신의 [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)(예: [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 4444)를 완벽히 숨겼다. 시스템 관리자가 서버에 접속해 `netstat -antp`를 쳐도 4444 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)는 보이지 않고 평온해 보인다.
2. <strong>탐지자의 의사결정 (<a href="/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/">교차 검증</a>, Cross-View <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">Validation</a>)</strong>:
   - 로컬 OS의 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)(`netstat`, `ps`)는 이미 오염되어 믿을 수 없다.
   - 방어자는 서버 "외부"의 네트워크 스위치에서 흐르는 패킷을 덤프하거나, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리 덤프 도구(Volatility 등)를 이용해 물리적 메모리를 직접 스캔한다.
   - 외부 스위치에서는 "DB 서버(IP)가 4444 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 외부와 통신하는 패킷"이 명확히 보이는데, 서버 내부에서 `netstat`을 쳤을 때는 4444 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 안 보인다면, 이 **관점의 불일치(Cross-View)** 가 바로 루트킷이 존재한다는 100% 명백한 증거가 된다.
3. <strong>아키텍트의 근본적 방어 결단 (<a href="/studynote/02_operating_system/10_security/608_secure_boot/">보안 부팅</a> 및 <a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 서명)</strong>:
   - 사후 탐지가 너무 어려우므로 애초에 악성 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이 올라가지 못하게 OS 아키텍처를 변경해야 한다.
   - 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 빌드 시 `CONFIG_MODULE_SIG_FORCE=y` 옵션을 켜서, <strong><a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> <a href="/studynote/04_software_engineering/04_testing_quality/192_module_independence/">모듈</a> 서명 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>(<a href="/studynote/02_operating_system/10_security/645_kernel_module_signature_verification/">Module Signature Verification</a>)</strong>을 강제한다.
   - 해커가 악성 `.ko` [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 `insmod`로 올리려 해도, 사전에 등록된 신뢰할 수 있는 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 키(Public [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))로 서명되지 않은 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)은 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 절대 적재를 허용하지 않게 만든다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) (루트킷 방어 하드닝)
- **kptr_restrict 및 dmesg 제한**: [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리의 주소가 유출되어야 시스템 콜 테이블 위치를 덮어쓸 수 있다. `/proc/sys/kernel/kptr_restrict` 값을 `2`로 설정하여 유저 레벨에서 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 포인터 주소를 볼 수 없게 ASLR과 연동하여 차단했는가?
- <strong><a href="/studynote/09_security/04_endpoint_security/206_uefi_secure_boot_verification/">UEFI Secure Boot</a> (<a href="/studynote/02_operating_system/10_security/608_secure_boot/">보안 부팅</a>) 활성화</strong>: 하드웨어 메인보드 [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/) 단에서 서명된 [부트로더](/studynote/02_operating_system/01_overview_architecture/029_bootloader/)와 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)만 로딩하도록 강제하여, 하드 디스크의 MBR이나 VBR을 감염시키는 [부트킷](/studynote/09_security/04_endpoint_security/362_bootkit/)의 실행 체인을 물리적으로 끊어냈는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>운영 편의를 위한 <a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 락다운 해제</strong>: "[모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 솔루션이나 커스텀 드라이버 설치가 불편하다"는 이유로 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 서명 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 끄고(`Secure Boot` 비활성화), root 권한이면 아무 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이나 맘대로 올릴 수 있게 허용하는 레거시 관행. 이는 [제로 데이](/studynote/02_operating_system/10_security/597_zero_day_exploit/) 취약점 한 번에 시스템 전체를 영구적으로 빼앗기는 지름길이다.

- **📢 섹션 요약 비유**: 서명 없는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈 적재](/studynote/02_operating_system/01_overview_architecture/067_lkm/)를 허용하는 것은, 아무나 경찰 제복만 사서 입고 오면 신원(암호학적 서명)을 확인하지 않고 바로 경찰서 내부 전산망([커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리) 접속 권한을 내어주는 최악의 출입 통제와 같습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과 ([커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 서명 및 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 아키텍처 도입 시)

| 구분 | 루트킷 방어 부재 시 | [Secure Boot](/studynote/02_operating_system/10_security/608_secure_boot/) + [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 서명 적용 | 기술적 함의 |
|:---|:---|:---|:---|
| **가시성** | 해킹 후 몇 년간 침해 사실 인지 불가 (은폐 성공) | 악성 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈 적재](/studynote/02_operating_system/01_overview_architecture/067_lkm/) 시도 시 즉각 에러 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 및 차단 | OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨의 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)([Integrity](/studynote/09_security/01_intro_principles/003_integrity/)) 및 가시성 [회복](/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/) |
| <strong>운영 (<a href="/studynote/01_computer_architecture/04_instruction_set_architecture/165_ir/">IR</a>)</strong> | 감염 의심 시 포맷 및 OS 재설치 외엔 답이 없음 (비용 큼) | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 진입이 불가능하므로 유저 모드 침해로 범위 축소 | 침해 [사고 대응](/studynote/09_security/01_intro_principles/009_incident_response/)([IR](/studynote/01_computer_architecture/04_instruction_set_architecture/165_ir/)) 비용 감소 및 원인 분석 명확화 |
| <strong>정성 (<a href="/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/">신뢰도</a>)</strong> | [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 도구(ps, netstat) 결과를 신뢰할 수 없음 | OS가 출력하는 결과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 대한 절대적 신뢰 복원 | "[제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)" 기반 시스템 신뢰 사슬(Chain of Trust) 완성 |

### 미래 전망
전통적인 시스템 콜 후킹([LKM](/studynote/02_operating_system/01_overview_architecture/067_lkm/) 조작) 방식의 루트킷은 최신 리눅스의 엄격한 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 서명과 메모리 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)(Read-Only [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 기술)로 인해 사실상 불가능해지고 있다. 이에 따라 해커들은 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 코드를 변조하는 대신, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조체 자체의 연결 고리만 교묘하게 수정하여 프로세스를 숨기는 <strong>DKOM (<a href="/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/">Direct</a> <a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">Kernel</a> Object Manipulation)</strong> 기법으로 진화했다. 또한 방어자들은 이에 맞서 [eBPF](/studynote/02_operating_system/10_security/615_ebpf/)(Extended [BPF](/studynote/02_operating_system/01_overview_architecture/069_ebpf/))를 활용하여 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 코어 영역 밖에서 안전하게 시스템 상태를 실시간 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링하고, 클라우드 벤더(AWS, Azure) 차원에서 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 밖에서 게스트 OS 메모리의 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 외부 스캔([Virtual Machine](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) [Introspection](/studynote/09_security/05_web_app_security/496_graphql_introspection/), [VMI](/studynote/07_enterprise_systems/02_erp_systems/099_vmi_vendor_managed_inventory/))하는 차세대 클라우드 보안 기술로 맞서고 있다.

### 참고 표준
- <strong>Linux <a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">Kernel</a> <code>module_signature</code></strong>: 암호학적 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 로딩 표준
- <strong><a href="/studynote/09_security/04_endpoint_security/206_uefi_secure_boot_verification/">UEFI Secure Boot</a> 사양</strong>: 하드웨어에서 OS [부트로더](/studynote/02_operating_system/01_overview_architecture/029_bootloader/)까지의 신뢰 사슬 규격
- <strong><a href="/studynote/09_security/13_secops_ir_forensics/642_mitre_attack/">MITRE ATT&CK</a></strong>: T1014 (Rootkit), T1547.001 ([Kernel](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) Modules and Extensions)

- **📢 섹션 요약 비유**: 성 안에서 거짓말하는 첩자(루트킷)를 찾기 위해 병사들을 다그치는 대신, 아예 성을 하늘에서 내려다보는 인공위성([하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 기반 [VMI](/studynote/07_enterprise_systems/02_erp_systems/099_vmi_vendor_managed_inventory/) 스캔)을 띄워 첩자의 움직임을 외부의 시선(Cross-View)으로 완벽하게 감시하는 체계로 발전하고 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [침입 탐지 시스템](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/) ([IDS](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/)) / 침입 방지 시스템 ([IPS](/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/)) 시스템 콜 트레이싱 기반 [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [샌드박싱](/studynote/02_operating_system/10_security/602_sandboxing_kernel_wrapper/) ([Sandboxing](/studynote/02_operating_system/10_security/602_sandboxing_kernel_wrapper/)) 기술 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 래퍼 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [사용자 인증](/studynote/02_operating_system/10_security/604_authentication_factors/) ([Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/)) 요소 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [비밀번호 솔팅](/studynote/02_operating_system/10_security/605_password_salting_hash/) ([Salting](/studynote/02_operating_system/10_security/605_password_salting_hash/)) 기반 해시 처리 방어 구조 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[샌드박싱 (Sandboxing) 기술 커널 래퍼]
    |
    v
[루트킷 (Rootkit) 커널 모듈 감염 방식 (시스템 콜 테이블 후킹)]
    |
    +---> [사용자 인증 (Authentication) 요소]
    +---> [비밀번호 솔팅 (Salting) 기반 해시 처리 방어 구조]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 시스템 관리자가 컴퓨터에게 "지금 누가 활동 중이야?" 하고 물어보면 컴퓨터가 정직하게 알려줘요.
2. 하지만 나쁜 악당 프로그램(루트킷)이 컴퓨터의 '뇌([커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))' 속에 몰래 숨어들어, 컴퓨터가 거짓말을 하도록 뇌를 세뇌시켜 버렸어요.
3. 그래서 관리자가 물어보면 세뇌당한 컴퓨터는 "아무 문제 없어요~ 악당은 없어요~"라고 대답해서, 악당이 평생 컴퓨터 안에서 몰래 나쁜 짓을 할 수 있게 만드는 가장 무서운 마법이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 603 / 800

<- **이전**: [602. 샌드박싱 (Sandboxing) 기술 커널 래퍼](/studynote/02_operating_system/10_security/602_sandboxing_kernel_wrapper/)
**다음**: [604. 사용자 인증 (Authentication) 요소 - Something you know, have, are](/studynote/02_operating_system/10_security/604_authentication_factors/) ->

---
