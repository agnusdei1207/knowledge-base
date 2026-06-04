---
title: "737. VFS 가상 파일 시스템 (VFS Virtual File System Abstraction)"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/)([Virtual File System](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/))는 리눅스/유닉스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내부에서 사용자 애플리케이션과 실제 물리적 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템(ext4, [FAT](/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/), NTFS 등) 사이에 존재하는 <strong>강력한 <a href="/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/">추상화</a>(<a href="/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/">Abstraction</a>) 계층이자 <a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a> <a href="/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a></strong>다.
> 2. <strong>메커니즘 (객체 지향 <a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a>)</strong>: VFS는 세상의 모든 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템을 아우를 수 있는 '공통 인터페이스(super_block, inode, dentry, [file](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 객체)'를 정의해 둔다. 앱이 `read()` 시스템 콜을 부르면 VFS가 이를 받아, 현재 [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/)된 하단 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 진짜 `read` 함수 포인터로 연결해 준다.
> 3. **가치**: 이 아키텍처 덕분에 앱 개발자는 "이 디스크가 [USB](/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/)(FAT32)인지, 리눅스 서버(ext4)인지, 네트워크 드라이브([NFS](/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/))인지"를 전혀 알 필요 없이 오직 하나의 표준 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)(`open`, `read`, `write`)만 사용하여 세상의 모든 저장 장치를 투명하게 읽고 쓸 수 있다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong><a href="/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/">VFS</a> (<a href="/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/">Virtual File System</a> / Virtual <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">File</a> <a href="/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">Switch</a>)</strong>: 서로 다른 다양한 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템들이 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 위에서 동일하게 작동하는 것처럼 보이게 만들어주는 가상의 소프트웨어 계층.
  - 리눅스의 철학인 "Everything is a [file](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(모든 것은 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이다)"을 기술적으로 완성시키는 핵심 뼈대.

- <strong>필요성 (파편화된 <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템의 통일)</strong>:
  - 리눅스에는 ext4가 있고, USB를 꽂으면 FAT32가 들어오고, 윈도우 하드를 꽂으면 NTFS가 들어온다.
  - 만약 VFS가 없다면? C언어로 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 읽으려면 개발자가 `ext4_read()`, `fat32_read()`, `ntfs_read()` 함수를 각각 따로 짜야 한다.
  - 게다가 `cp` 명령어로 ext4에 있는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 FAT32 USB로 복사할 때, 두 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이 서로 데이터를 어떻게 주고받을지 아키텍처가 전무했다.
  - **해결책**: "OS 안에 가짜 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템([VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/))을 하나 크게 만들자! 앱은 VFS에게만 명령을 내리고, VFS가 뒤에서 각 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 전용 드라이버를 호출해 주는 다형성(Polymorphism)을 구현하자!"

  - **앱**: 한국어만 할 줄 아는 손님.
  - <strong>실제 <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템 (ext4, <a href="/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/">FAT</a>, NTFS)</strong>: 프랑스 식당, 일본 식당, 중국 식당. 각 식당마다 주문받는 언어와 방식이 완전히 다르다.
  - <strong><a href="/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/">VFS</a> (가상 <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템)</strong>: 배달의 민족(배달 앱). 손님은 배달 앱에 들어가서 "터치 한 번(read/write)"으로 음식을 주문한다. 배달 앱([VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/)) 내부에서 알아서 프랑스어, 일본어로 통역해서 각 식당에 주문을 넣어주고 결과를 손님에게 가져다준다. 손님은 식당의 언어를 몰라도 된다.

- **발전 과정**:
  1. **단일 FS 시대**: 초창기 UNIX. 1개의 디스크 포맷만 지원.
  2. <strong><a href="/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/">VFS</a> 도입 (SunOS 2.0, 1985년)</strong>: [네트워크 파일 시스템](/studynote/02_operating_system/11_exam_summary/774_nfs_stateless_network_file_system/)([NFS](/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/))을 로컬 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)처럼 투명하게 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 위해 처음 고안됨.
  3. <strong>리눅스 <a href="/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/">VFS</a></strong>: 현재 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 VFS는 디스크뿐만 아니라 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/), [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/), `/proc`, `/sys` 같은 하드웨어가 없는 메모리 기반 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)까지 몽땅 [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 아래로 편입시켰다.

- **📢 섹션 요약 비유**: VFS는 만능 돼지코(멀티 [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/))입니다. 어떤 나라의 플러그([파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템)를 가져와도, 이 돼지코에 꽂기만 하면 우리는 똑같은 220V 구멍(`open`, `read`, `write`)으로 전기를 마음껏 쓸 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### VFS의 4대 핵심 객체 (Object) 모델

C언어로 짜인 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 완벽한 '객체 지향([OOP](/studynote/04_software_engineering/06_software_architecture/322_oop_4_characteristics/))'을 구현한 곳이 바로 VFS다. (C++의 인터페이스/가상 함수 역할을 함수 포인터로 구현함)

| [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 객체 | 역할 (클래스) | 비유 |
|:---|:---|:---|
| <strong><a href="/studynote/02_operating_system/09_file_system/518_vfs_objects_superblock_inode_dentry_file/">Superblock</a> (슈퍼블록) 객체</strong> | [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/)된 특정 <strong><a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템 전체</strong>의 정보(종류, 총 용량, 빈 블록 수)를 담고 있음. | "이 USB는 FAT32 마을이다" |
| **Inode (아이노드) 객체** | 특정 <strong><a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 1개의 고유한 <a href="/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a></strong>(크기, 권한, [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)일)를 담고 있음. | "이 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 주민등록증" |
| **Dentry (디엔트리) 객체** | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 <strong>이름</strong>과 그 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 속한 <strong>경로(계층 구조)</strong>를 [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)함. (예: `/home/user/file.txt`) | "이름표와 동네 지도" |
| <strong><a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">File</a> (<a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>) 객체</strong> | <strong>현재 열려 있는 <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a></strong>과 사용자와의 상호작용 상태(예: 현재 어디까지 읽었나, Offset)를 담고 있음. | "지금 내가 읽고 있는 책갈피" |

---

### VFS를 통한 다형성(Polymorphism) 동작 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인

앱이 `read(fd, buf, 100)` 시스템 콜을 쳤을 때 VFS가 이를 분기하는 과정이다.

```text
  +-------------------------------------------------------------------+
  |                 VFS의 파일 읽기(Read) 시스템 콜 처리 파이프라인           |
  +-------------------------------------------------------------------+
  |  [ User Space ]                                                   |
  |   - `read(fd, buf, 100);` 호출                                     |
  |                                                                   |
  |  ========================= [ System Call (Trap) ] ================|
  |  [ Kernel Space - VFS 계층 ]                                       |
  |   1. 커널의 `sys_read()`가 실행됨.                                    |
  |   2. fd(파일 디스크립터)를 통해 현재 열린 [File 객체]를 찾음.               |
  |   3. File 객체 안에는 [f_op (File Operations)]라는 함수 포인터 묶음이 있음.|
  |                                                                   |
  |   ★ VFS의 핵심 마술: `file->f_op->read(file, buf, 100);` 실행!       |
  |                                                                   |
  |  ========================= [ 실제 File System 계층 ] ===============|
  |   - 만약 이 파일이 ext4 라면?  -> `f_op->read`는 `ext4_file_read()`로 연결됨! |
  |   - 만약 이 파일이 FAT32 라면? -> `f_op->read`는 `fat_file_read()`로 연결됨!  |
  |   - 만약 이 파일이 NFS 라면?   -> `f_op->read`는 `nfs_file_read()`로 연결됨!  |
  |                                                                   |
  |  [ Hardware / Network 계층 ]                                       |
  |   - 각 FS 전용 드라이버가 디스크를 돌리거나 랜카드로 패킷을 쏴서 데이터를 가져옴. |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** VFS는 자기가 직접 디스크를 읽지 않는다. VFS의 `sys_read` 함수 안에는 `if (ext4) else if (fat)` 같은 지저분한 코드가 **단 한 줄도 없다**. 그저 현재 열린 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 객체에 꽂혀있는 함수 포인터(`f_op->read`)를 실행할 뿐이다. 이것이 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 새로운 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템(예: zfs, btrfs)이 세상에 나와도 [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 소스코드를 1바이트도 수정하지 않고 그대로 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)로 끼워 넣을 수 있는 미친 확장성(Extensibility)의 비밀이다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 3대 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 철학 비교

| 비교 항목 | 리눅스 / 유닉스 ([VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/)) | Windows (I/O Manager) | macOS (XNU [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/)) |
|:---|:---|:---|:---|
| **설계 철학** | <strong>Everything is a <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">file</a> (모든 것은 <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>이다)</strong> | 객체와 핸들(Handle) 중심의 비동기 I/O | 리눅스와 유사한 [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 구조 [상속](/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) |
| <strong><a href="/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/">추상화</a> 범위</strong> | 디스크, 키보드, [소켓](/studynote/02_operating_system/02_process_thread/125_socket/), 프로세스 정보(`/proc`) 전체 | 디스크, 네트워크 등 기능별 API가 다소 다름 | 디스크 및 권한 체계 통합 |
| **경로(Path) 매핑** | 오직 단일 Root `/` 아래에 모두 [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/)됨 | `C:\`, `D:\` 처럼 드라이브 문자(Drive Letter) 사용 | `/Volumes/` 하위에 자동 [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/) |

### 과목 융합 관점

- <strong>시스템 보안 (<a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a>)</strong>: 리눅스의 샌드박스나 권한 제어는 이 [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 단에서 이루어진다. 악성 앱이 USB의 `autorun.inf`를 읽으려고 할 때, 하단의 FAT32 드라이버로 내려가기 전, VFS의 Inode 객체에서 "너 이 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 읽을 권한(R/W/X) 있어?"라고 1차 검문소 역할을 완벽하게 수행한다.
- <strong><a href="/studynote/13_cloud_architecture/01_virtualization/015_virtualization/">가상화</a> (Cloud / <a href="/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/">Docker</a>)</strong>: [도커](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)([Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)) [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)의 핵심 기술인 <strong>OverlayFS (오버레이 <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템)</strong>는 디스크 구조를 가진 진짜 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이 아니다. VFS에 기생하여 "아래 깔린 읽기 전용 이미지 레이어"와 "위에 얹혀진 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 전용 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 레이어"를 합쳐서 VFS에게 "이거 그냥 평범한 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이야"라고 사기를 치는 순수 소프트웨어 [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 드라이버다.

- **📢 섹션 요약 비유**: VFS는 국제 연합(UN) 통역 센터입니다. 프랑스(ext4), 영국(NTFS), 미국([NFS](/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/)) 대표들이 모였지만, 통역 센터([VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/))를 거치면 모두가 '영어(표준 시스템 콜)'라는 하나의 언어로 매끄럽게 대화할 수 있는 완벽한 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)의 전당입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — /proc <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템의 미스터리</strong>: 리눅스에서 `cat /proc/cpuinfo`를 치면 CPU의 스펙이 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 텍스트로 쭉 출력된다. 하드디스크의 어디에 이 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 저장되어 있을까?
   - **아키텍처 분석**: 저장되어 있지 않다! `/proc`은 디스크(블록 디바이스)와 연결되지 않은 <strong>가상 <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템(Pseudo Filesystem)</strong>이다.
   - **VFS의 마법**: 우리가 `read("/proc/cpuinfo")`를 날리면 VFS가 `procfs` 드라이버를 호출한다. 이 드라이버의 `read` 함수는 디스크를 읽는 대신, OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리를 뒤져서 현재 CPU 상태를 문자열(String)로 조립한 뒤 뱉어낸다. [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 덕분에 개발자들은 복잡한 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) API를 몰라도, 그냥 평범한 텍스트 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 읽듯이(`cat`) [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 뇌를 들여다볼 수 있게 된 것이다.

2. <strong>시나리오 — 클라우드 <a href="/studynote/02_operating_system/09_file_system/553_distributed_file_system/">분산 파일 시스템</a>(<a href="/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/">NFS</a>, EFS)의 <a href="/studynote/02_operating_system/09_file_system/516_mount_mechanism/">마운트</a> <a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>(Hang)</strong>: AWS EC2 서버 10대에 EFS([NFS](/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/) 기반)를 [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/)해서 쓰고 있다. EFS 네트워크에 10초간 장애가 발생했는데, EC2 서버에서 `ls` 명령어만 쳐도 셸이 완전히 얼어붙어(Hang) 아무것도 못 함.
   - **원인 분석**: `ls` 명령어는 현재 디렉터리의 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 목록을 얻기 위해 VFS의 `dentry`와 `inode`를 읽는 시스템 콜을 날린다. VFS는 이 요청을 하단의 [NFS](/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/) 드라이버로 패스했다. [NFS](/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/) 드라이버는 네트워크 너머의 EFS에 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 요청을 날리고 무한 대기(Block)에 빠졌다. VFS는 하단 드라이버가 응답을 안 주니 `ls` 프로세스를 Uninterruptible Sleep(D 상태)으로 묶어버렸고, 사용자는 터미널에서 Ctrl+C를 눌러도 안 꺼지는 공포를 겪게 된다.
   - **대응 (아키텍처 튜닝)**: VFS는 하단 FS의 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)에 매우 취약하다. [NFS](/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/) [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/) 시 반드시 <strong><code>soft</code> (또는 <code>intr</code>) 및 <code>timeo=30</code> 옵션</strong>을 주어야 한다. 네트워크가 3초 이상 끊기면 [NFS](/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/) 드라이버가 무한 대기를 풀고 VFS에게 에러([Timeout](/studynote/02_operating_system/05_deadlock/319_timeout_prevention/))를 리턴하게 만들어, `ls` 명령어가 에러 메시지를 뿜고 종료되도록(Fail-Fast) 튜닝해야 서버 마비를 막을 수 있다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 파일 I/O 시스템 콜 및 VFS 성능 병목 우회 플로우            |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [고성능 데이터베이스나 인메모리 캐시 서버(Redis)를 설계/운영할 때]           |
  |                |                                                  |
  |                v                                                  |
  |      애플리케이션이 파일이나 디스크를 직접(Direct) 세밀하게 컨트롤해야 하는가?   |
  |          +- 예 (RDBMS) --> [O_DIRECT 플래그 사용]                   |
  |          |            대책: VFS의 혜택(페이지 캐시, 미리 읽기)을 강제로 끄고,  |
  |          |                  앱이 디스크 하드웨어와 거의 직결로 통신하게 만듦.    |
  |          +- 아니오 (일반 앱)                                            |
  |                |                                                  |
  |                v                                                  |
  |      VFS 계층에서 발생하는 컨텍스트 스위칭과 커널 락(Lock) 오버헤드가 버거운가?|
  |          +---> [Kernel Bypass (SPDK) 도입 검토]                      |
  |          |    결론: VFS 자체를 아예 버려버림. 유저 스페이스에서 NVMe 드라이브와|
  |          |          직접 폴링(Polling)으로 통신하여 VFS의 오버헤드를 0으로 만듦.|
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** VFS는 만능이지만, 만능이라는 말은 곧 "여러 계층(Layers)을 거치느라 무겁다"는 뜻이다. SSD가 나오기 전 [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 시절에는 어차피 디스크가 너무 느려서 VFS의 소프트웨어 오버헤드는 티도 안 났다. 하지만 [NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) 시대가 열리면서, 초당 100만 번의 I/O를 치려니 VFS의 객체(inode, dentry) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 락([Lock](/studynote/05_database/04_transactions_concurrency/510_lock/))이 치명적인 병목이 되어버렸다. 최고의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 위해서는 VFS의 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)를 깨부수고 하드웨어로 내려가는 것이 현대의 극한 튜닝이다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong><a href="/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/">VFS</a> Dentry Cache (dcache)</strong>: 서버 메모리 사용량이 높은데 범인을 못 찾겠다면 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 [Slab](/studynote/02_operating_system/11_exam_summary/760_slab_allocator_object_caching/) 메모리를 의심해야 한다. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수백만 개를 만들고 지우는 서버(임시 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버)는 VFS가 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 경로를 빠르게 찾기 위해 `dentry` 객체를 메모리에 수 기가바이트 [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)해 둔다(dentry bloat). 이때 `echo 2 > /proc/sys/vm/drop_caches`를 날려 [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 껍데기 메모리를 비워주는 유지보수 스크립트가 필요한가?

- **📢 섹션 요약 비유**: VFS는 편안한 자동변속기(오토매틱)입니다. 누구나 쉽게 엑셀(read)과 브레이크(write)를 밟아 운전할 수 있게 해 주죠. 하지만 F1 레이서(고성능 DB)에게는 이 자동변속기가 기어를 바꾸는 0.1초의 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)마저 거슬리기 때문에, 수동 변속기([O_DIRECT](/studynote/02_operating_system/09_file_system/565_o_direct_io_bypass_cache/), [SPDK](/studynote/01_computer_architecture/15_advanced_topics/672_spdk/))로 뜯어고쳐 버리는 것입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 단일 FS 시대 ([VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 부재) | [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 도입 후 현대 OS | 개선 효과 |
|:---|:---|:---|:---|
| **정성 (개발 생산성)**| FS마다 전용 API를 따로 써야 함 | <strong>모든 기기를 <code>open, read, write</code>로 통일</strong> | 앱의 완벽한 이식성(Portability) 확보 |
| **정성 (확장성)** | 새 디스크 포맷 지원 시 OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수정 | <strong><a href="/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/">VFS</a> 인터페이스만 맞춰 <a href="/studynote/04_software_engineering/04_testing_quality/192_module_independence/">모듈</a>(.ko) 추가</strong> | [KVM](/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/), [Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/), 클라우드 스토리지의 생태계 폭발 |
| <strong>정량 (I/O <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>)</strong> | 각 FS마다 제각각 [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/) 구현 | VFS가 통합된 [Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Cache 관리 | 글로벌 메모리 최적화를 통한 디스크 I/O 속도 극대화 |

### 미래 전망
- **io_uring과의 결합**: 리눅스의 I/O 패러다임을 바꾼 `io_uring`은 VFS를 거치는 시스템 콜 [트랩](/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/)([Trap](/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/))의 오버헤드를 소멸시켰다. [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 하단의 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 오퍼레이션(f_op)들은 이제 비동기로 동작하도록 전면 개조되고 있으며, VFS는 점차 "동기식 함수 호출의 브로커"에서 "비동기 I/O 큐의 라우터"로 체질 개선을 강제받고 있다.

### 결론
[VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/)(가상 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템)는 컴퓨터 과학에서 <strong>"<a href="/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/">추상화</a>(<a href="/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/">Abstraction</a>)가 시스템의 무한한 확장을 만든다"</strong>는 진리를 증명하는 가장 거대하고 아름다운 소프트웨어 아키텍처다. 하드디스크, [USB](/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/), 네트워크 드라이브, 마우스, 키보드, 심지어 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 내부 상태(proc)까지 모든 이질적인 존재들을 "[파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)([File](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))"이라는 단 하나의 철학적 개념으로 녹여낸 [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 용광로 덕분에, 우리는 1970년대의 유닉스 명령어를 가지고 2024년의 최첨단 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 클라우드 스토리지를 완벽하게 다룰 수 있게 되었다.

- **📢 섹션 요약 비유**: 수백 개의 서로 다른 충전 단자를 가진 전자기기들이, VFS라는 '[USB](/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/)-C 타입'이라는 하나의 절대 표준으로 통일되었습니다. 우리는 그 안에 흐르는 전기가 태양광이든 원자력이든 상관없이, 그저 케이블(시스템 콜)만 꽂으면 모든 기기가 완벽하게 작동하는 축복을 누리고 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| i-node 직접/간접 포인터 [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [하드 링크](/studynote/02_operating_system/09_file_system/511_hard_link/) / [심볼릭 링크](/studynote/02_operating_system/09_file_system/512_symbolic_link/) 차이 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [버퍼 캐시](/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 입출력 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [접근 제어 목록](/studynote/02_operating_system/11_exam_summary/739_access_control_list_acl/) ([ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[하드 링크 / 심볼릭 링크 차이]
    |
    v
[VFS 가상 파일 시스템 (VFS Virtual File System Abstraction)]
    |
    +---> [버퍼 캐시 파일 입출력 지연]
    +---> [접근 제어 목록 (ACL)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 철수네 식당에는 프랑스인, 중국인, 일본인 요리사(실제 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템)가 각자 자기 나라 말로만 주문을 받아요.
2. 철수(앱)가 프랑스어나 중국어를 배워서 주문(C언어 코딩)하려면 너무 머리가 아프겠죠?
3. 그래서 주방장([VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 가상 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템)을 고용했어요! 철수가 한국어로 "김치찌개 줘!"라고 주방장에게 말하면, 주방장이 알아서 요리사 나라에 맞는 언어로 통역해서 주문을 넣어줘요. 철수는 한국어만 알아도 전 세계 요리를 다 시킬 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 737 / 800

<- **이전**: [736. 하드 링크 / 심볼릭 링크 차이 (Hard Link Vs Symbolic Link)](/studynote/02_operating_system/11_exam_summary/736_hard_link_vs_symbolic_link/)
**다음**: [738. 버퍼 캐시 파일 입출력 지연 (Buffer Cache File I/O Delayed Write)](/studynote/02_operating_system/11_exam_summary/738_buffer_cache_file_io_delayed_write/) ->

---
