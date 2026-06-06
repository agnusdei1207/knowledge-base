---
title: "124. Named Pipe Fifo"
date: "2026-05-08"
tags:
  - "studynote-operating-system"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) (Named [Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/) / [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/))는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 상에 이름을 가진 특수 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 존재하여, 부모-자식 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 없는 독립적인 프로세스 간에도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 전달할 수 있는 [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) (Inter-[Process](/studynote/12_it_management/05_security_compliance/943_process/) Communication) 메커니즘이다.
> 2. **가치**: 일반 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) ([Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/))가 부모-자식 프로세스 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)에 종속되는 반면, 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 경로를 통해 어떤 프로세스든 접근할 수 있으므로 관련 없는 [프로세스 간 통신](/studynote/02_operating_system/02_process_thread/117_ipc/)의 유연성을 극대화한다.
> 3. **융합**: 쉘 스크립트의 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 연결, 클라이언트-서버 모델의 간단한 구현, 그리고 데몬 (Daemon) 프로세스와 사용자 프로세스 간의 로컬 메시징 등 다양한 시스템 프로그래밍 시나리오에서 핵심 통신 수단으로 활용된다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) (Named [Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/) / [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/))는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 내에 `mkfifo` [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 또는 `mkfifo()` 시스템 콜 ([System Call](/studynote/02_operating_system/01_overview_architecture/013_system_call/))로 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되는 특수 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) (Special [File](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))이다. FIFO는 First-In-First-Out의 약자로, 먼저 쓰인 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 먼저 읽히는 큐 ([Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/)) 동작 방식을 따른다. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 상에 경로가 존재하므로, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 경로를 아는 모든 프로세스가 이를 열어 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받을 수 있다.

- **필요성**: 일반 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) (Unnamed [Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/))는 `pipe()` 시스템 콜로 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되며, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터 ([File](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) Descriptor)를 통해서만 접근할 수 있으므로 반드시 `fork()`로 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 부모-자식 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)의 프로세스 간에서만 사용할 수 있다. 하지만 실제 시스템 환경에서는 전혀 다른 팀에서 개발한 독립적인 두 프로그램이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 교환해야 하는 경우가 빈번하다. 예를 들어, 백엔드 데몬이 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 경로를 통해 클라이언트 애플리케이션과 통신해야 한다면 일반 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)로는 구현이 불가능하다. 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이라는 공통의 이름 공간 ([Namespace](/studynote/02_operating_system/01_overview_architecture/061_namespace/))을 매개로 이러한 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 없는 [프로세스 간 통신](/studynote/02_operating_system/02_process_thread/117_ipc/)을 가능하게 하는 필수 메커니즘이다.

- **등장 배경 및 발전 과정**:
  1. <strong><a href="/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> UNIX <a href="/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a>의 한계</strong>: 1973년 켄 톰슨 (Ken Thompson)이 도입한 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 `|` 연산자를 통한 쉘 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 가능하게 했으나, `fork()`를 경유하지 않은 프로세스 간에는 사용할 수 없는 근본적 제약이 있었다.
  2. **System V FIFO의 도입**: AT&T UNIX System V에서 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 상에 존재하는 FIFO라는 개념이 도입되어, 경로명만 알면 어느 프로세스든 통신에 참여할 수 있는 패러다임이 확립되었다.
  3. **POSIX 표준화**: POSIX (Portable [Operating System](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) Interface)에서 `mkfifo()` API가 표준화되면서, 리눅스 (Linux), macOS, BSD 계열 모든 유닉스 계열 OS에서 일관된 동작을 보장하게 되었다.

이 도식은 일반 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) (Unnamed [Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/))가 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터 기반이므로 부모-자식 프로세스 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)에 종속되는 반면, 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 경로를 통해 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 없는 프로세스도 통신할 수 있다는 구조적 차이를 명확히 보여준다.

```text
  +----------------------------------------------------------------+
  |          일반 파이프 vs 지명 파이프 (FIFO) 접근 방식 비교      |
  +----------------------------------------------------------------+
  |                                                                |
  |  [일반 파이프 (Unnamed Pipe)]                                  |
  |                                                                |
  |   Parent Process                                               |
  |   +-------------------+                                        |
  |   | pipe(fd[2])       | --fork()---> fd[0], fd[1] 상속          |
  |   | fd[0]=읽기        |               |                        |
  |   | fd[1]=쓰기        |               v                        |
  |   +-------------------+     Child Process (상속된 FD만 접근)   |
  |                                                                |
  |   ⚠ 부모-자식 관계 필수, 외부 프로세스 접근 불가               |
  |                                                                |
  |  [지명 파이프 (Named Pipe / FIFO)]                             |
  |                                                                |
  |   파일 시스템: /tmp/my_fifo (특수 파일)                        |
  |                     ^            ^                             |
  |                     |            |                             |
  |              Process A        Process B                        |
  |              (독립 프로세스)    (독립 프로세스)                |
  |              open("/tmp/my_fifo", O_WRONLY)                    |
  |              open("/tmp/my_fifo", O_RDONLY)                    |
  |                                                                |
  |   ✅ 부모-자식 관계 무관, 경로만 알면 접근 가능                |
  +----------------------------------------------------------------+
```

**[다이어그램 해설]** 이 구조도의 핵심은 통신 경로에 대한 접근 권한의 차이다. 일반 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 `pipe()` 시스템 콜이 반환하는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터 ([File](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) Descriptor) [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) `fd[0]`(읽기 전용)과 `fd[1]`([쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 전용)만을 통해 접근할 수 있으며, 이 디스크립터는 `fork()`에 의해 자식 프로세스에게만 [상속](/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)된다. 따라서 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터 테이블을 공유하지 않는 완전히 독립적인 프로세스는 일반 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)에 접근할 방법이 없다. 반면 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) (Named [Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/) / [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/))는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 상에 `/tmp/my_fifo`와 같은 실제 경로로 존재하는 특수 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이므로, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 경로를 알고 있는 모든 프로세스가 `open()` 시스템 콜을 통해 이 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 열고 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 작업을 수행할 수 있다. 이러한 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 기반 접근 모델 덕분에 관련 없는 데몬 프로세스, 사용자 애플리케이션, 심지어 다른 사용자 권한의 프로세스까지도 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 퍼미션 (Permission) 범위 내에서 통신에 참여할 수 있다. 이는 시스템 프로그래밍에서 프로세스 간 [결합도](/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) ([Coupling](/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/))를 크게 낮추는 구조적 장점이다.

- **📢 섹션 요약 비유**: 일반 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)가 아버지와 아들끼리만 쓰는 가족용 비밀 통신판이라면, 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 동네 골목에 세워진 공용 게시판이라 길만 알면 누구나 와서 메시지를 남기고 읽어갈 수 있는 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| <strong><a href="/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/">FIFO</a> 특수 <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a></strong> | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 상의 통신 종단점 | `mkfifo()`로 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), `inode`에 [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) 타입 마킹 | [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) ([Virtual File System](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/)) | 공용 우체통 주소 |
| <strong><a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> <a href="/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a> 버퍼 (<a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">Kernel</a> <a href="/studynote/02_operating_system/02_process_thread/123_pipe/">Pipe</a> Buffer)</strong> | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 공간의 순환 큐 버퍼 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) 순서로 임시 저장, [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 단위 관리 | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리 관리 | 우편물 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 대기함 |
| <strong>읽기/<a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 대기열 (<a href="/studynote/02_operating_system/02_process_thread/089_wait_queue/">Wait Queue</a>)</strong> | 블로킹 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 관리 | 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 프로세스가 대기하는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [대기 큐](/studynote/02_operating_system/02_process_thread/089_wait_queue/) | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) | 우체통 앞 줄 서는 사람들 |
| <strong><a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 퍼미션 (<a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">File</a> Permission)</strong> | 접근 제어 | 일반 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)과 동일한 rwx 권한 모델 적용 | POSIX [ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) ([Access Control List](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)) | 우체통 자물쇠 |

---

### 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)의 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 및 동작 흐름

지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 `mkfifo` 쉘 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)나 `mkfifo()` 시스템 콜을 통해 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되며, [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시에는 실제 디스크 공간을 차지하지 않고 단지 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 inode ([Index Node](/studynote/02_operating_system/09_file_system/528_unix_inode_mechanism/))에 [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) 타입으로만 마킹된다. [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 후에는 양측 프로세스가 `open()`으로 각각 읽기 전용과 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 전용으로 열어야만 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송이 시작된다.

이 흐름도는 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)를 통한 두 독립 [프로세스 간 통신](/studynote/02_operating_system/02_process_thread/117_ipc/)의 전체 생명주기를 시각화한 것으로, 특히 `open()` 호출 시의 블로킹 동작과 [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 순서를 명확히 보여준다.

```text
  +----------------------------------------------------------------+
  |           지명 파이프 (Named Pipe / FIFO) 통신 흐름도          |
  +----------------------------------------------------------------+
  |                                                                |
  |  [생성 단계]                                                   |
  |  $ mkfifo /tmp/my_fifo                                         |
  |     또는                                                       |
  |  mkfifo("/tmp/my_fifo", 0666);  // 프로그램 내 생성            |
  |     |                                                          |
  |     v                                                          |
  |  파일 시스템에 FIFO 특수 파일 생성 (inode 타입 = FIFO)         |
  |                                                                |
  |  [통신 단계]                                                   |
  |                                                                |
  |  Process A (Writer)            Process B (Reader)              |
  |       |                            |                           |
  |   open(O_WRONLY)               open(O_RDONLY)                  |
  |       |                            |                           |
  |       |   <--- 둘 다 열릴 때까지 ---> |  (기본 블로킹 동작)      |
  |       |       open()이 대기          |                         |
  |       v                            v                           |
  |   write("Hello") -------> [FIFO 버퍼] -------> read(buf)         |
  |   write("World") -------> [Kernel    ] -------> read(buf)        |
  |   write("!!!")  -------> [Pipe Buf ] -------> read(buf)          |
  |                          |                                     |
  |                    FIFO 순서: Hello -> World -> !!!              |
  |                          |                                     |
  |       v                            v                           |
  |    close()                      close()                        |
  |                                                                |
  |  ⚠ Reader가 close하면 Writer의 write()는 SIGPIPE 시그널 발생   |
  +----------------------------------------------------------------+
```

**[다이어그램 해설]** 이 흐름도에서 가장 중요한 동작 특성은 `open()` 호출의 블로킹 ([Blocking](/studynote/02_operating_system/02_process_thread/122_sync_async_communication/)) 동작이다. 기본적으로 읽기 전용으로 열려는 프로세스는 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 전용 프로세스가 나타날 때까지 대기 (Block)하고, 반대로 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 전용 프로세스도 읽기 전용 프로세스가 나타날 때까지 대기한다. 즉, 양측이 모두 준비되지 않으면 통신이 시작되지 않는다. 이는 양측 프로세스 간의 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) ([Synchronization](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/))가 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 열기 단계에서 자연스럽게 이루어짐을 의미한다. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) 버퍼 ([Kernel](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/) Buffer)에 [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) (First-In-First-Out) 순서로 적재되며, 버퍼가 가득 차면 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 프로세스도 블로킹된다. 특히 읽기 프로세스가 `close()`를 호출하면 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)의 읽기 측이 끊어진 것으로 간주하여, [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 프로세스의 후속 `write()` 호출은 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 의해 SIGPIPE 시그널 ([Signal](/studynote/02_operating_system/02_process_thread/130_signal/))을 발생시키거나 EPIPE 에러를 반환한다. 이러한 동작 특성 덕분에 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 단순한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전달뿐만 아니라 프로세스 간의 생존 감지 (Liveness [Detection](/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/)) 용도로도 활용될 수 있다.

### 심층 동작 원리

① <strong><a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a></strong>: `mkfifo()`는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템에 inode를 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하되, 일반 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)과 달리 디스크 블록을 할당하지 않는다. inode의 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 타입 필드에 [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) 마크만 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)하여, 이후 `open()` 시 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) 동작을 수행하도록 유도한다.

② <strong>열기 (Open) <a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a></strong>: `open(O_RDONLY)`와 `open(O_WRONLY)`는 기본적으로 상대방이 나타날 때까지 블로킹된다. 단, `O_NONBLOCK` [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)를 사용하면 읽기 측은 즉시 반환되고, [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 측은 상대가 없으면 ENXIO 에러를 반환한다.

③ <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 전송</strong>: `write()`는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 버퍼에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 복사하고, `read()`는 버퍼에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 꺼낸다. 버퍼 크기는 시스템마다 다르며, 리눅스 기본값은 한 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) (4KB)에서 64KB까지 확장 가능하다.

④ **반반이중 (Half-Duplex) 동작**: POSIX 표준에서 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) (Half-Duplex) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름만 보장한다. 양방향 통신이 필요한 경우 두 개의 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)를 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하여 각각 반대 방향으로 사용해야 한다.

⑤ **종료 및 정리**: 모든 프로세스가 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터를 닫으면 [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 여전히 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템에 남아있으나, 내부 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 버퍼와 대기열은 해제된다. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 자체는 `unlink()`로 삭제해야 한다.

- **📢 섹션 요약 비유**: 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)의 open() 대기는 마치 주방의 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)를 설치할 때 양쪽 끝이 모두 연결되어야 물이 흐르는 것과 같아서, 한쪽만 연결된 상태에서는 수도꼭지를 돌려도 물이 나오지 않고 기다려야 하는 구조와 같습니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: 일반 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) (Unnamed [Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/)) vs 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) (Named [Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/) / [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/))

| 비교 항목 | 일반 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) (Unnamed [Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/)) | 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) (Named [Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/) / [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/)) | 판단 포인트 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> 방식</strong> | `pipe()` 시스템 콜 | `mkfifo()` 시스템 콜 또는 `mkfifo` [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 의존 여부 |
| <strong><a href="/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/">식별</a> 방법</strong> | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터 ([File](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) Descriptor) | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 경로 (Path) | 외부 프로세스 접근 가능성 |
| <strong>프로세스 <a href="/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a></strong> | 부모-자식 (fork 후 [상속](/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)) 필수 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 무관 (경로만 알면 접근 가능) | 프로세스 독립성 요구 |
| **생존 주기** | [프로세스 종료](/studynote/02_operating_system/02_process_thread/107_process_termination/) 시 자동 소멸 | `unlink()` 전까지 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템에 존재 | 통신 채널 지속성 |
| **주 사용처** | 쉘 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인, 부모-자식 간 간단 통신 | 독립 [프로세스 간 통신](/studynote/02_operating_system/02_process_thread/117_ipc/), 데몬-클라이언트 모델 | 아키텍처 복잡도 |

이 도식은 동일한 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) 버퍼를 사용하면서도, [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 방법과 프로세스 간 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 요구 사항에서 근본적으로 다른 두 메커니즘의 아키텍처 차이를 시각화한 것이다.

```text
  +----------------------------------------------------------------+
  |       일반 파이프 vs 지명 파이프 — 커널 자원 관점 비교         |
  +----------------------------------------------------------------+
  |                                                                |
  |  [일반 파이프]                                                 |
  |                                                                |
  |  +--- Process A ---+         +--- Process B ---+               |
  |  | fd[1] --(쓰기)--+--------->| fd[0] --(읽기) |                |
  |  +-----------------+         +-----------------+               |
  |                    |                                           |
  |                    v                                           |
  |         +---------------------+                                |
  |         |  Kernel Pipe Buffer |  (FD가 닫히면 자동 해제)       |
  |         |  (FIFO 순환 큐)     |                                |
  |         +---------------------+                                |
  |                                                                |
  |  [지명 파이프]                                                 |
  |                                                                |
  |  +--- Process C ---+         +--- Process D ---+               |
  |  | (관계 없음)      |         | (관계 없음)      |             |
  |  | O_WRONLY -------+--------->| O_RDONLY ------- |              |
  |  +-----------------+         +-----------------+               |
  |                    |                                           |
  |                    v                                           |
  |  +-- File System ---------------------------+                  |
  |  | /tmp/my_fifo (FIFO inode, 타입 마킹)      |                 |
  |  |   +---> Kernel Pipe Buffer (FIFO 순환 큐)  |                 |
  |  +-------------------------------------------+                 |
  |                                                                |
  |  차이점: 접근 경로가 FD 상속 vs 파일 시스템 경로               |
  |  공통점: 내부 동작은 동일한 커널 파이프 버퍼 사용              |
  +----------------------------------------------------------------+
```

**[다이어그램 해설]** [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 자원 관점에서 보면 일반 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)와 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 동일한 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) 버퍼 ([Kernel](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/) Buffer)를 사용한다. 핵심 차이는 이 버퍼에 도달하는 "접근 경로"에 있다. 일반 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 프로세스의 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터 테이블 내에서만 존재하므로 `fork()`를 통해 테이블이 복사되지 않으면 접근 불가능하다. 반면 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) ([Virtual File System](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/)) 계층을 통해 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 경로로 버퍼에 매핑된다. 즉, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내부의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송 메커니즘은 완전히 동일하지만, 외부에서 이 메커니즘을 "어떻게 찾아가는가"라는 접근 계층만 다를 뿐이다. 이러한 구조적 통일성 덕분에 개발자는 통신 대상 프로세스와의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)에 따라 두 메커니즘 중 하나를 선택하기만 하면 되며, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송의 동작 방식에 대해서는 추가적인 학습이 불필요하다. 실무에서는 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 동일하므로 프로세스 간 독립성 요구 사항만 고려하면 된다.

### 비교 2: 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) vs Unix [Domain](/studynote/05_database/02_modeling_normalization/064_relation_domain/) [Socket](/studynote/02_operating_system/02_process_thread/125_socket/) (UDS)

- <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong>: 두 메커니즘 모두 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리 복사만으로 통신하므로 네트워크 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 오버헤드가 없다. 그러나 Unix [Domain](/studynote/05_database/02_modeling_normalization/064_relation_domain/) Socket은 `sendmsg()`/`recvmsg()` 시스템 콜을 통한 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터 전달 (Ancillary [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 가능하므로, 더 복잡한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 교환이 필요한 경우 유리하다.
- **사용 편의성**: 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 쉘 스크립트에서 `$ mkfifo` 명령 한 줄로 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 가능하므로 간단한 [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) 시나리오에서 훨씬 접근성이 높다.

### 과목 융합 관점

- <strong><a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a></strong>: PostgreSQL은 리눅스 환경에서 클라이언트와 서버 간의 로컬 통신에 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)를 사용할 수 있으며, [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 루프백 오버헤드를 회피하여 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 응답 레이턴시를 개선한다.
- **네트워크 프로그래밍**: 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 네트워크 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) ([Socket](/studynote/02_operating_system/02_process_thread/125_socket/))의 단순화된 대안으로, 동일 호스트 내의 클라이언트-서버 통신에서 복잡한 연결 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) (Handshake) 없이 구현할 수 있는 경량 통신 채널이다.

- **📢 섹션 요약 비유**: 일반 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)와 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 내부적으로 같은 수도관([커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 버퍼)을 사용하지만, 전자는 벽 안에 숨겨진 가정용 배관이고 후자는 길가에 공개된 공용 수도전이라 접근성에서 결정적 차이가 나는 것과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — <a href="/studynote/09_security/13_secops_ir_forensics/626_log_collection/">로그 수집</a> 데몬과 애플리케이션 간 통신</strong>: 다수의 애플리케이션 프로세스가 중앙 [로그 수집](/studynote/09_security/13_secops_ir_forensics/626_log_collection/) 데몬에게 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 전달해야 하는 상황. 각 애플리케이션은 부모-자식 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 아니므로 일반 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)를 사용할 수 없다. 아키텍트는 각 애플리케이션의 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 출력을 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)로 리다이렉트 (Redirect)하여 데몬이 이를 읽도록 구성하는 설계를 선택한다. 예: `app > /tmp/log_fifo &` 방식으로 실행.

2. <strong>시나리오 — 지명 <a href="/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a>의 데드락 (<a href="/studynote/02_operating_system/05_deadlock/281_deadlock_definition/">Deadlock</a>) 위험</strong>: 양방향 통신을 단일 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)로 구현하려는 시도에서, 양측 프로세스가 모두 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)로 인해 버퍼가 가득 차고 양측 모두 읽기를 시도하지 않아 영원히 대기하는 데드락 상태가 발생한 상황. 개발자는 반드시 두 개의 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) (각각 [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/))를 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하여 명확한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름 방향을 보장해야 한다.

이 다이어그램은 단일 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)로 양방향 통신을 시도할 때 발생하는 데드락의 메커니즘과, 두 개의 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)를 사용하여 이를 해결하는 올바른 아키텍처를 시각화한 것이다.

```text
  +--------------------------------------------------------------------+
  |           지명 파이프 양방향 통신 — 데드락과 해결                  |
  +--------------------------------------------------------------------+
  |                                                                    |
  |  [잘못된 설계: 단일 FIFO로 양방향 통신 시도]                       |
  |                                                                    |
  |  Process A                FIFO Buffer              Process B       |
  |  +----------+         +---------------+         +----------+       |
  |  | Request  |--------->| [FULL] 쓰기   |         | Response |       |
  |  | (쓰기)   |         | 대기 중...     |--------->| (쓰기)   |      |
  |  |          |<---------| 읽기 시도?     |         |          |      |
  |  | (읽기)   |         | 누가 먼저?    |<---------| (읽기)   |       |
  |  +----------+         +---------------+         +----------+       |
  |       |                                                  |         |
  |       +---- 둘 다 쓰기만 시도 -> 버퍼 만원 -> DEADLOCK ---+          |
  |                                                                    |
  |  [올바른 설계: 쌍방향 FIFO (각각 단방향)]                          |
  |                                                                    |
  |  Process A                                              Process B  |
  |  +----------+         +---------------+         +----------+       |
  |  | Request  |--------->| FIFO_AB       |--------->| Response |       |
  |  | (쓰기)   |         | (A->B 전용)     |         | (읽기)   |      |
  |  +----------+         +---------------+         +----------+       |
  |  +----------+         +---------------+         +----------+       |
  |  | Response |<---------| FIFO_BA       |<---------| Request  |       |
  |  | (읽기)   |         | (B->A 전용)     |         | (쓰기)   |      |
  |  +----------+         +---------------+         +----------+       |
  |                                                                    |
  |  ✅ 데이터 흐름 방향이 명확 -> 데드락 불가                          |
  +--------------------------------------------------------------------+
```

**[다이어그램 해설]** 이 비교도의 핵심은 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)의 [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/)성 (Half-Duplex)이라는 근본 설계 특성이다. 단일 FIFO로 양방향 통신을 시도하면, [Process](/studynote/12_it_management/05_security_compliance/943_process/) A와 [Process](/studynote/12_it_management/05_security_compliance/943_process/) B가 동시에 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 작업을 수행할 때 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) 버퍼가 가득 차게 되고, 양측 모두 버퍼에 공간이 생기기를 기다리며 읽기를 수행하지 않는 상황, 즉 고전적인 데드락 ([Deadlock](/studynote/02_operating_system/05_deadlock/281_deadlock_definition/))에 빠진다. POSIX 표준에서 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 동작만을 보장하므로, 양방향 통신이 필요한 경우에는 반드시 두 개의 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)를 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하여 각각 명확한 [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름 (A->B, B->A)을 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)해야 한다. 이 패턴은 실무에서 클라이언트-서버 모델의 요청-응답 통신을 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)로 구현할 때 반드시 준수해야 하는 설계 원칙이다. [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 채널을 명확히 분리하는 것은 [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) 설계에서 데드락을 예방하는 가장 기본적이고 확실한 방법이다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **기술적**: 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) 버퍼 크기 (리눅스 기본 `/proc/sys/fs/pipe-max-size`)가 전송할 메시지의 최대 크기를 수용할 수 있는가? O_NONBLOCK [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) 사용 여부에 따른 에러 처리 로직이 구현되었는가?
- **운영·보안적**: 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 퍼미션이 (0666 등) 불필요한 프로세스의 접근을 차단하도록 [최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/) ([Least Privilege](/studynote/09_security/01_intro_principles/010_least_privilege/))으로 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)되었는가? 사용이 끝난 [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 잔류하지 않도록 정리 (Cleanup) 메커니즘이 구현되었는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **SIGPIPE 무시 누락**: Reader 프로세스가 비정상 종료되면 Writer의 `write()` 호출이 SIGPIPE를 발생시켜 프로세스가 강제 종료된다. 반드시 `signal(SIGPIPE, SIG_IGN)`으로 시그널을 무시하거나, `write()` 반환값과 `errno == EPIPE`를 확인하여 우아하게 (Gracefully) 처리해야 한다.

- **📢 섹션 요약 비유**: 양방향 도로를 단일 차선으로 만들면 양쪽에서 온 차가 마주 보고 서로 양보하지 않아 길이 막히는 것(데드락)과 같으므로, 반드시 각 방향 전용 차선([FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) 두 개)을 분리 설치해야 하는 것과 같습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 일반 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 기반 통신 | 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) ([FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/)) 도입 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) I/O 경유 (디스크 접근) | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리 버퍼만 사용 | 통신 레이턴시 **수십~수백 배 단축** |
| **정량** | 수동 파싱 및 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 구현 필요 | [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) 순서 자동 보장 | [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 코드 **제거로 개발 시간 단축** |
| **정성** | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 잔류로 인한 디스크 오염 가능 | 디스크 블록 할당 없음 | 시스템 청결성 유지 |

### 미래 전망
- <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a> 환경에서의 역할 확대</strong>: Docker와 [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 환경에서 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 간의 간단한 메시지 전달에 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)가 볼륨 마운트를 통해 활용되며, 네트워크 오버헤드가 없는 초경량 [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) 채널로 주목받고 있다.
- **이벤트 기반 시스템과의 결합**: systemd 등의 현대 init 시스템에서 데몬 간 통신 알림 채널로 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)를 활용하여, [소켓](/studynote/02_operating_system/02_process_thread/125_socket/)보다 가벼운 이벤트 통지 (Notification) 메커니즘을 구현하는 사례가 증가하고 있다.

### 참고 표준
- **POSIX.1-2008 (IEEE Std 1003.1)**: `mkfifo()`, [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) 특수 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 동작 및 의미 규정
- <strong>SUSv4 (Single UNIX <a href="/studynote/04_software_engineering/03_design_architecture/148_requirements_specification_formal_informal/">Specification</a> v4)</strong>: 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)의 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 통합 동작 표준

- **📢 섹션 요약 비유**: 복잡한 우편 시스템(네트워크 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/))이나 무거운 택배([공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/)) 대신, 동네 골목의 공용 게시판(지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/))은 설치가 쉽고 유지보수가 간편하여 소규모 시스템에서 여전히 활발하게 쓰이는 것과 같습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [동기식 통신](/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) ([Blocking](/studynote/02_operating_system/02_process_thread/122_sync_async_communication/)) vs 비동기식 통신 (Non-[blocking](/studynote/02_operating_system/02_process_thread/122_sync_async_communication/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) ([Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) ([Socket](/studynote/02_operating_system/02_process_thread/125_socket/)) 통신 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [RPC](/studynote/02_operating_system/02_process_thread/126_rpc/) ([Remote Procedure Call](/studynote/02_operating_system/02_process_thread/126_rpc/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[파이프 (Pipe)]
    |
    v
[지명 파이프 (Named Pipe / FIFO)]
    |
    +---> [소켓 (Socket) 통신]
    +---> [RPC (Remote Procedure Call)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 지명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)는 학교 복도에 놓인 <strong>"공용 편지함"</strong>이에요. 이름이 적혀 있어서([FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/)) 어떤 반 친구든 편지를 넣고 꺼낼 수 있어요.
2. 편지함에 먼저 넣은 편지가 먼저 읽힌다는 규칙(First-In-First-Out)이 있어서, 순서가 섞이지 않고 꼭 차례대로 배달된답니다.
3. 편지함 양쪽 문이 모두 열려야 편지를 주고받을 수 있어서, 친구가 오기 전에는 내가 쓴 편지가 편지함 안에서 기다리고 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 124 / 800

<- **이전**: [123. 파이프 (Pipe) - 단방향(Half-duplex), 부모-자식 간](/studynote/02_operating_system/02_process_thread/123_pipe/)
**다음**: [125. 소켓 (Socket) 통신 - 네트워크, 서로 다른 시스템 간 통신](/studynote/02_operating_system/02_process_thread/125_socket/) ->

---
