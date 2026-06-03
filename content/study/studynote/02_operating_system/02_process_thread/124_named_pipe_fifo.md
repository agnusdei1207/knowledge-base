---
title: 124. 지명 파이프 (Named Pipe / FIFO) - 양방향 가능, 부모-자식 관계 무관
date: '2026-05-08'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 지명 [[123_pipe|파이프]] (Named [[123_pipe|Pipe]] / [[261_fifo_page_replacement|FIFO]])는 [[501_file_definition_logical_record|파일]] 시스템 상에 이름을 가진 특수 [[501_file_definition_logical_record|파일]]로 존재하여, 부모-자식 [[083_relationship_in_er_model|관계]]가 없는 독립적인 프로세스 간에도 [[001_dikw_pyramid|데이터]]를 전달할 수 있는 [[117_ipc|IPC]] (Inter-[[300_process|Process]] Communication) 메커니즘이다.
> 2. **가치**: 일반 [[123_pipe|파이프]] ([[123_pipe|Pipe]])가 부모-자식 프로세스 [[083_relationship_in_er_model|관계]]에 종속되는 반면, 지명 [[123_pipe|파이프]]는 [[501_file_definition_logical_record|파일]] 시스템 경로를 통해 어떤 프로세스든 접근할 수 있으므로 관련 없는 [[117_ipc|프로세스 간 통신]]의 유연성을 극대화한다.
> 3. **융합**: 쉘 스크립트의 [[123_pipe|파이프]]라인 연결, 클라이언트-서버 모델의 간단한 구현, 그리고 데몬 (Daemon) 프로세스와 사용자 프로세스 간의 로컬 메시징 등 다양한 시스템 프로그래밍 시나리오에서 핵심 통신 수단으로 활용된다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 지명 [[123_pipe|파이프]] (Named [[123_pipe|Pipe]] / [[261_fifo_page_replacement|FIFO]])는 [[501_file_definition_logical_record|파일]] 시스템 내에 `mkfifo` [[158_instruction|명령어]] 또는 `mkfifo()` 시스템 콜 ([[013_system_call|System Call]])로 [[087_process_state_transition|생성]]되는 특수 [[501_file_definition_logical_record|파일]] (Special [[501_file_definition_logical_record|File]])이다. FIFO는 First-In-First-Out의 약자로, 먼저 쓰인 [[001_dikw_pyramid|데이터]]가 먼저 읽히는 큐 ([[058_queue|Queue]]) 동작 방식을 따른다. [[501_file_definition_logical_record|파일]] 시스템 상에 경로가 존재하므로, [[501_file_definition_logical_record|파일]] 경로를 아는 모든 프로세스가 이를 열어 [[001_dikw_pyramid|데이터]]를 주고받을 수 있다.

- **필요성**: 일반 [[123_pipe|파이프]] (Unnamed [[123_pipe|Pipe]])는 `pipe()` 시스템 콜로 [[087_process_state_transition|생성]]되며, [[501_file_definition_logical_record|파일]] 디스크립터 ([[501_file_definition_logical_record|File]] Descriptor)를 통해서만 접근할 수 있으므로 반드시 `fork()`로 [[087_process_state_transition|생성]]된 부모-자식 [[083_relationship_in_er_model|관계]]의 프로세스 간에서만 사용할 수 있다. 하지만 실제 시스템 환경에서는 전혀 다른 팀에서 개발한 독립적인 두 프로그램이 [[001_dikw_pyramid|데이터]]를 교환해야 하는 경우가 빈번하다. 예를 들어, 백엔드 데몬이 [[501_file_definition_logical_record|파일]] 시스템 경로를 통해 클라이언트 애플리케이션과 통신해야 한다면 일반 [[123_pipe|파이프]]로는 구현이 불가능하다. 지명 [[123_pipe|파이프]]는 [[501_file_definition_logical_record|파일]] 시스템이라는 공통의 이름 공간 ([[061_namespace|Namespace]])을 매개로 이러한 [[083_relationship_in_er_model|관계]] 없는 [[117_ipc|프로세스 간 통신]]을 가능하게 하는 필수 메커니즘이다.

- **등장 배경 및 발전 과정**:
  1. **[[459_quic_fec_forward_error_correction|초기]] UNIX [[123_pipe|파이프]]의 한계**: 1973년 켄 톰슨 (Ken Thompson)이 도입한 [[123_pipe|파이프]]는 `|` 연산자를 통한 쉘 [[123_pipe|파이프]]라인을 가능하게 했으나, `fork()`를 경유하지 않은 프로세스 간에는 사용할 수 없는 근본적 제약이 있었다.
  2. **System V FIFO의 도입**: AT&T UNIX System V에서 [[501_file_definition_logical_record|파일]] 시스템 상에 존재하는 FIFO라는 개념이 도입되어, 경로명만 알면 어느 프로세스든 통신에 참여할 수 있는 패러다임이 확립되었다.
  3. **POSIX 표준화**: POSIX (Portable [[001_operating_system_purpose|Operating System]] Interface)에서 `mkfifo()` API가 표준화되면서, 리눅스 (Linux), macOS, BSD 계열 모든 유닉스 계열 OS에서 일관된 동작을 보장하게 되었다.

이 도식은 일반 [[123_pipe|파이프]] (Unnamed [[123_pipe|Pipe]])가 [[501_file_definition_logical_record|파일]] 디스크립터 기반이므로 부모-자식 프로세스 [[083_relationship_in_er_model|관계]]에 종속되는 반면, 지명 [[123_pipe|파이프]]는 [[501_file_definition_logical_record|파일]] 시스템 경로를 통해 [[083_relationship_in_er_model|관계]] 없는 프로세스도 통신할 수 있다는 구조적 차이를 명확히 보여준다.

```text
  ┌────────────────────────────────────────────────────────────────┐
  │          일반 파이프 vs 지명 파이프 (FIFO) 접근 방식 비교      │
  ├────────────────────────────────────────────────────────────────┤
  │                                                                │
  │  [일반 파이프 (Unnamed Pipe)]                                  │
  │                                                                │
  │   Parent Process                                               │
  │   ┌───────────────────┐                                        │
  │   │ pipe(fd[2])       │ ──fork()──▶ fd[0], fd[1] 상속          │
  │   │ fd[0]=읽기        │               │                        │
  │   │ fd[1]=쓰기        │               ▼                        │
  │   └───────────────────┘     Child Process (상속된 FD만 접근)   │
  │                                                                │
  │   ⚠ 부모-자식 관계 필수, 외부 프로세스 접근 불가               │
  │                                                                │
  │  [지명 파이프 (Named Pipe / FIFO)]                             │
  │                                                                │
  │   파일 시스템: /tmp/my_fifo (특수 파일)                        │
  │                     ▲            ▲                             │
  │                     │            │                             │
  │              Process A        Process B                        │
  │              (독립 프로세스)    (독립 프로세스)                │
  │              open("/tmp/my_fifo", O_WRONLY)                    │
  │              open("/tmp/my_fifo", O_RDONLY)                    │
  │                                                                │
  │   ✅ 부모-자식 관계 무관, 경로만 알면 접근 가능                │
  └────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 구조도의 핵심은 통신 경로에 대한 접근 권한의 차이다. 일반 [[123_pipe|파이프]]는 `pipe()` 시스템 콜이 반환하는 [[501_file_definition_logical_record|파일]] 디스크립터 ([[501_file_definition_logical_record|File]] Descriptor) [[055_array|배열]] `fd[0]`(읽기 전용)과 `fd[1]`([[289_cqrs_db|쓰기]] 전용)만을 통해 접근할 수 있으며, 이 디스크립터는 `fork()`에 의해 자식 프로세스에게만 [[234_uml_class_relationships_generalization_dependency|상속]]된다. 따라서 [[501_file_definition_logical_record|파일]] 디스크립터 테이블을 공유하지 않는 완전히 독립적인 프로세스는 일반 [[123_pipe|파이프]]에 접근할 방법이 없다. 반면 지명 [[123_pipe|파이프]] (Named [[123_pipe|Pipe]] / [[261_fifo_page_replacement|FIFO]])는 [[501_file_definition_logical_record|파일]] 시스템 상에 `/tmp/my_fifo`와 같은 실제 경로로 존재하는 특수 [[501_file_definition_logical_record|파일]]이므로, [[501_file_definition_logical_record|파일]] 경로를 알고 있는 모든 프로세스가 `open()` 시스템 콜을 통해 이 [[501_file_definition_logical_record|파일]]을 열고 읽기/[[289_cqrs_db|쓰기]] 작업을 수행할 수 있다. 이러한 [[501_file_definition_logical_record|파일]] 시스템 기반 접근 모델 덕분에 관련 없는 데몬 프로세스, 사용자 애플리케이션, 심지어 다른 사용자 권한의 프로세스까지도 [[501_file_definition_logical_record|파일]] 퍼미션 (Permission) 범위 내에서 통신에 참여할 수 있다. 이는 시스템 프로그래밍에서 프로세스 간 [[195_coupling_levels|결합도]] ([[195_coupling_levels|Coupling]])를 크게 낮추는 구조적 장점이다.

- **📢 섹션 요약 비유**: 일반 [[123_pipe|파이프]]가 아버지와 아들끼리만 쓰는 가족용 비밀 통신판이라면, 지명 [[123_pipe|파이프]]는 동네 골목에 세워진 공용 게시판이라 길만 알면 누구나 와서 메시지를 남기고 읽어갈 수 있는 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **[[261_fifo_page_replacement|FIFO]] 특수 [[501_file_definition_logical_record|파일]]** | [[501_file_definition_logical_record|파일]] 시스템 상의 통신 종단점 | `mkfifo()`로 [[087_process_state_transition|생성]], `inode`에 [[261_fifo_page_replacement|FIFO]] 타입 마킹 | [[517_virtual_file_system_vfs|VFS]] ([[517_virtual_file_system_vfs|Virtual File System]]) | 공용 우체통 주소 |
| **[[022_kernel_role|커널]] [[123_pipe|파이프]] 버퍼 ([[022_kernel_role|Kernel]] [[123_pipe|Pipe]] Buffer)** | [[022_kernel_role|커널]] 공간의 순환 큐 버퍼 | [[001_dikw_pyramid|데이터]]를 [[261_fifo_page_replacement|FIFO]] 순서로 임시 저장, [[286_page_frame|페이지]] 단위 관리 | [[022_kernel_role|커널]] 메모리 관리 | 우편물 [[104_classification_analysis|분류]] 대기함 |
| **읽기/[[289_cqrs_db|쓰기]] 대기열 ([[089_wait_queue|Wait Queue]])** | 블로킹 [[212_synchronization_mechanisms|동기화]] 관리 | 읽기/[[289_cqrs_db|쓰기]] 프로세스가 대기하는 [[022_kernel_role|커널]] [[089_wait_queue|대기 큐]] | [[022_kernel_role|커널]] [[079_kube_scheduler_pod_placement|스케줄러]] | 우체통 앞 줄 서는 사람들 |
| **[[501_file_definition_logical_record|파일]] 퍼미션 ([[501_file_definition_logical_record|File]] Permission)** | 접근 제어 | 일반 [[501_file_definition_logical_record|파일]]과 동일한 rwx 권한 모델 적용 | POSIX [[549_acl_access_control_list|ACL]] ([[549_acl_access_control_list|Access Control List]]) | 우체통 자물쇠 |

---

### 지명 [[123_pipe|파이프]]의 [[087_process_state_transition|생성]] 및 동작 흐름

지명 [[123_pipe|파이프]]는 `mkfifo` 쉘 [[158_instruction|명령어]]나 `mkfifo()` 시스템 콜을 통해 [[087_process_state_transition|생성]]되며, [[087_process_state_transition|생성]] 시에는 실제 디스크 공간을 차지하지 않고 단지 [[501_file_definition_logical_record|파일]] 시스템의 inode ([[528_unix_inode_mechanism|Index Node]])에 [[261_fifo_page_replacement|FIFO]] 타입으로만 마킹된다. [[087_process_state_transition|생성]] 후에는 양측 프로세스가 `open()`으로 각각 읽기 전용과 [[289_cqrs_db|쓰기]] 전용으로 열어야만 [[001_dikw_pyramid|데이터]] 전송이 시작된다.

이 흐름도는 지명 [[123_pipe|파이프]]를 통한 두 독립 [[117_ipc|프로세스 간 통신]]의 전체 생명주기를 시각화한 것으로, 특히 `open()` 호출 시의 블로킹 동작과 [[261_fifo_page_replacement|FIFO]] [[001_dikw_pyramid|데이터]] 순서를 명확히 보여준다.

```text
  ┌────────────────────────────────────────────────────────────────┐
  │           지명 파이프 (Named Pipe / FIFO) 통신 흐름도          │
  ├────────────────────────────────────────────────────────────────┤
  │                                                                │
  │  [생성 단계]                                                   │
  │  $ mkfifo /tmp/my_fifo                                         │
  │     또는                                                       │
  │  mkfifo("/tmp/my_fifo", 0666);  // 프로그램 내 생성            │
  │     │                                                          │
  │     ▼                                                          │
  │  파일 시스템에 FIFO 특수 파일 생성 (inode 타입 = FIFO)         │
  │                                                                │
  │  [통신 단계]                                                   │
  │                                                                │
  │  Process A (Writer)            Process B (Reader)              │
  │       │                            │                           │
  │   open(O_WRONLY)               open(O_RDONLY)                  │
  │       │                            │                           │
  │       │   ◀── 둘 다 열릴 때까지 ──▶ │  (기본 블로킹 동작)      │
  │       │       open()이 대기          │                         │
  │       ▼                            ▼                           │
  │   write("Hello") ──────▶ [FIFO 버퍼] ──────▶ read(buf)         │
  │   write("World") ──────▶ [Kernel    ] ──────▶ read(buf)        │
  │   write("!!!")  ──────▶ [Pipe Buf ] ──────▶ read(buf)          │
  │                          │                                     │
  │                    FIFO 순서: Hello → World → !!!              │
  │                          │                                     │
  │       ▼                            ▼                           │
  │    close()                      close()                        │
  │                                                                │
  │  ⚠ Reader가 close하면 Writer의 write()는 SIGPIPE 시그널 발생   │
  └────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 흐름도에서 가장 중요한 동작 특성은 `open()` 호출의 블로킹 ([[122_sync_async_communication|Blocking]]) 동작이다. 기본적으로 읽기 전용으로 열려는 프로세스는 [[289_cqrs_db|쓰기]] 전용 프로세스가 나타날 때까지 대기 (Block)하고, 반대로 [[289_cqrs_db|쓰기]] 전용 프로세스도 읽기 전용 프로세스가 나타날 때까지 대기한다. 즉, 양측이 모두 준비되지 않으면 통신이 시작되지 않는다. 이는 양측 프로세스 간의 [[212_synchronization_mechanisms|동기화]] ([[212_synchronization_mechanisms|Synchronization]])가 [[501_file_definition_logical_record|파일]] 열기 단계에서 자연스럽게 이루어짐을 의미한다. [[001_dikw_pyramid|데이터]]는 [[022_kernel_role|커널]]의 [[123_pipe|파이프]] 버퍼 ([[022_kernel_role|Kernel]] [[123_pipe|Pipe]] Buffer)에 [[261_fifo_page_replacement|FIFO]] (First-In-First-Out) 순서로 적재되며, 버퍼가 가득 차면 [[289_cqrs_db|쓰기]] 프로세스도 블로킹된다. 특히 읽기 프로세스가 `close()`를 호출하면 [[123_pipe|파이프]]의 읽기 측이 끊어진 것으로 간주하여, [[289_cqrs_db|쓰기]] 프로세스의 후속 `write()` 호출은 [[022_kernel_role|커널]]에 의해 SIGPIPE 시그널 ([[130_signal|Signal]])을 발생시키거나 EPIPE 에러를 반환한다. 이러한 동작 특성 덕분에 지명 [[123_pipe|파이프]]는 단순한 [[001_dikw_pyramid|데이터]] 전달뿐만 아니라 프로세스 간의 생존 감지 (Liveness [[961_deepfake_detection|Detection]]) 용도로도 활용될 수 있다.

### 심층 동작 원리

① **[[087_process_state_transition|생성]]**: `mkfifo()`는 [[501_file_definition_logical_record|파일]] 시스템에 inode를 [[087_process_state_transition|생성]]하되, 일반 [[501_file_definition_logical_record|파일]]과 달리 디스크 블록을 할당하지 않는다. inode의 [[501_file_definition_logical_record|파일]] 타입 필드에 [[261_fifo_page_replacement|FIFO]] 마크만 [[009_config|설정]]하여, 이후 `open()` 시 [[022_kernel_role|커널]]이 [[123_pipe|파이프]] 동작을 수행하도록 유도한다.

② **열기 (Open) [[212_synchronization_mechanisms|동기화]]**: `open(O_RDONLY)`와 `open(O_WRONLY)`는 기본적으로 상대방이 나타날 때까지 블로킹된다. 단, `O_NONBLOCK` [[186_character_stuffing_dle_stx_etx|플래그]]를 사용하면 읽기 측은 즉시 반환되고, [[289_cqrs_db|쓰기]] 측은 상대가 없으면 ENXIO 에러를 반환한다.

③ **[[001_dikw_pyramid|데이터]] 전송**: `write()`는 [[022_kernel_role|커널]] 버퍼에 [[001_dikw_pyramid|데이터]]를 복사하고, `read()`는 버퍼에서 [[001_dikw_pyramid|데이터]]를 꺼낸다. 버퍼 크기는 시스템마다 다르며, 리눅스 기본값은 한 [[286_page_frame|페이지]] (4KB)에서 64KB까지 확장 가능하다.

④ **반반이중 (Half-Duplex) 동작**: POSIX 표준에서 지명 [[123_pipe|파이프]]는 [[008_단방향_반이중_전이중|단방향]] (Half-Duplex) [[001_dikw_pyramid|데이터]] 흐름만 보장한다. 양방향 통신이 필요한 경우 두 개의 지명 [[123_pipe|파이프]]를 [[087_process_state_transition|생성]]하여 각각 반대 방향으로 사용해야 한다.

⑤ **종료 및 정리**: 모든 프로세스가 [[501_file_definition_logical_record|파일]] 디스크립터를 닫으면 [[261_fifo_page_replacement|FIFO]] [[501_file_definition_logical_record|파일]]은 여전히 [[501_file_definition_logical_record|파일]] 시스템에 남아있으나, 내부 [[022_kernel_role|커널]] 버퍼와 대기열은 해제된다. [[501_file_definition_logical_record|파일]] 자체는 `unlink()`로 삭제해야 한다.

- **📢 섹션 요약 비유**: 지명 [[123_pipe|파이프]]의 open() 대기는 마치 주방의 [[123_pipe|파이프]]를 설치할 때 양쪽 끝이 모두 연결되어야 물이 흐르는 것과 같아서, 한쪽만 연결된 상태에서는 수도꼭지를 돌려도 물이 나오지 않고 기다려야 하는 구조와 같습니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: 일반 [[123_pipe|파이프]] (Unnamed [[123_pipe|Pipe]]) vs 지명 [[123_pipe|파이프]] (Named [[123_pipe|Pipe]] / [[261_fifo_page_replacement|FIFO]])

| 비교 항목 | 일반 [[123_pipe|파이프]] (Unnamed [[123_pipe|Pipe]]) | 지명 [[123_pipe|파이프]] (Named [[123_pipe|Pipe]] / [[261_fifo_page_replacement|FIFO]]) | 판단 포인트 |
|:---|:---|:---|:---|
| **[[087_process_state_transition|생성]] 방식** | `pipe()` 시스템 콜 | `mkfifo()` 시스템 콜 또는 `mkfifo` [[158_instruction|명령어]] | [[501_file_definition_logical_record|파일]] 시스템 의존 여부 |
| **[[655_ir_detection_analysis|식별]] 방법** | [[501_file_definition_logical_record|파일]] 디스크립터 ([[501_file_definition_logical_record|File]] Descriptor) | [[501_file_definition_logical_record|파일]] 시스템 경로 (Path) | 외부 프로세스 접근 가능성 |
| **프로세스 [[083_relationship_in_er_model|관계]]** | 부모-자식 (fork 후 [[234_uml_class_relationships_generalization_dependency|상속]]) 필수 | [[083_relationship_in_er_model|관계]] 무관 (경로만 알면 접근 가능) | 프로세스 독립성 요구 |
| **생존 주기** | [[107_process_termination|프로세스 종료]] 시 자동 소멸 | `unlink()` 전까지 [[501_file_definition_logical_record|파일]] 시스템에 존재 | 통신 채널 지속성 |
| **주 사용처** | 쉘 [[123_pipe|파이프]]라인, 부모-자식 간 간단 통신 | 독립 [[117_ipc|프로세스 간 통신]], 데몬-클라이언트 모델 | 아키텍처 복잡도 |

이 도식은 동일한 [[123_pipe|파이프]] 버퍼를 사용하면서도, [[655_ir_detection_analysis|식별]] 방법과 프로세스 간 [[083_relationship_in_er_model|관계]] 요구 사항에서 근본적으로 다른 두 메커니즘의 아키텍처 차이를 시각화한 것이다.

```text
  ┌────────────────────────────────────────────────────────────────┐
  │       일반 파이프 vs 지명 파이프 — 커널 자원 관점 비교         │
  ├────────────────────────────────────────────────────────────────┤
  │                                                                │
  │  [일반 파이프]                                                 │
  │                                                                │
  │  ┌─── Process A ───┐         ┌─── Process B ───┐               │
  │  │ fd[1] ──(쓰기)──┼────────▶│ fd[0] ──(읽기) │                │
  │  └─────────────────┘         └─────────────────┘               │
  │                    │                                           │
  │                    ▼                                           │
  │         ┌─────────────────────┐                                │
  │         │  Kernel Pipe Buffer │  (FD가 닫히면 자동 해제)       │
  │         │  (FIFO 순환 큐)     │                                │
  │         └─────────────────────┘                                │
  │                                                                │
  │  [지명 파이프]                                                 │
  │                                                                │
  │  ┌─── Process C ───┐         ┌─── Process D ───┐               │
  │  │ (관계 없음)      │         │ (관계 없음)      │             │
  │  │ O_WRONLY ───────┼────────▶│ O_RDONLY ─────── │              │
  │  └─────────────────┘         └─────────────────┘               │
  │                    │                                           │
  │                    ▼                                           │
  │  ┌── File System ───────────────────────────┐                  │
  │  │ /tmp/my_fifo (FIFO inode, 타입 마킹)      │                 │
  │  │   └──▶ Kernel Pipe Buffer (FIFO 순환 큐)  │                 │
  │  └───────────────────────────────────────────┘                 │
  │                                                                │
  │  차이점: 접근 경로가 FD 상속 vs 파일 시스템 경로               │
  │  공통점: 내부 동작은 동일한 커널 파이프 버퍼 사용              │
  └────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** [[022_kernel_role|커널]] 자원 관점에서 보면 일반 [[123_pipe|파이프]]와 지명 [[123_pipe|파이프]]는 동일한 [[123_pipe|파이프]] 버퍼 ([[022_kernel_role|Kernel]] [[123_pipe|Pipe]] Buffer)를 사용한다. 핵심 차이는 이 버퍼에 도달하는 "접근 경로"에 있다. 일반 [[123_pipe|파이프]]는 프로세스의 [[501_file_definition_logical_record|파일]] 디스크립터 테이블 내에서만 존재하므로 `fork()`를 통해 테이블이 복사되지 않으면 접근 불가능하다. 반면 지명 [[123_pipe|파이프]]는 [[517_virtual_file_system_vfs|VFS]] ([[517_virtual_file_system_vfs|Virtual File System]]) 계층을 통해 [[501_file_definition_logical_record|파일]] 시스템 경로로 버퍼에 매핑된다. 즉, [[022_kernel_role|커널]] 내부의 [[001_dikw_pyramid|데이터]] 전송 메커니즘은 완전히 동일하지만, 외부에서 이 메커니즘을 "어떻게 찾아가는가"라는 접근 계층만 다를 뿐이다. 이러한 구조적 통일성 덕분에 개발자는 통신 대상 프로세스와의 [[083_relationship_in_er_model|관계]]에 따라 두 메커니즘 중 하나를 선택하기만 하면 되며, [[001_dikw_pyramid|데이터]] 전송의 동작 방식에 대해서는 추가적인 학습이 불필요하다. 실무에서는 [[282_performance_tactics|성능]]이 동일하므로 프로세스 간 독립성 요구 사항만 고려하면 된다.

### 비교 2: 지명 [[123_pipe|파이프]] vs Unix [[064_relation_domain|Domain]] [[125_socket|Socket]] (UDS)

- **[[282_performance_tactics|성능]]**: 두 메커니즘 모두 [[022_kernel_role|커널]] 메모리 복사만으로 통신하므로 네트워크 [[057_stack|스택]] 오버헤드가 없다. 그러나 Unix [[064_relation_domain|Domain]] Socket은 `sendmsg()`/`recvmsg()` 시스템 콜을 통한 [[501_file_definition_logical_record|파일]] 디스크립터 전달 (Ancillary [[001_dikw_pyramid|Data]])이 가능하므로, 더 복잡한 [[001_dikw_pyramid|데이터]] 교환이 필요한 경우 유리하다.
- **사용 편의성**: 지명 [[123_pipe|파이프]]는 쉘 스크립트에서 `$ mkfifo` 명령 한 줄로 [[087_process_state_transition|생성]] 가능하므로 간단한 [[117_ipc|IPC]] 시나리오에서 훨씬 접근성이 높다.

### 과목 융합 관점

- **[[002_database_definition|데이터베이스]]**: PostgreSQL은 리눅스 환경에서 클라이언트와 서버 간의 로컬 통신에 지명 [[123_pipe|파이프]]를 사용할 수 있으며, [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 루프백 오버헤드를 회피하여 [[298_qkv_attention|쿼리]] 응답 레이턴시를 개선한다.
- **네트워크 프로그래밍**: 지명 [[123_pipe|파이프]]는 네트워크 [[125_socket|소켓]] ([[125_socket|Socket]])의 단순화된 대안으로, 동일 호스트 내의 클라이언트-서버 통신에서 복잡한 연결 [[009_config|설정]] (Handshake) 없이 구현할 수 있는 경량 통신 채널이다.

- **📢 섹션 요약 비유**: 일반 [[123_pipe|파이프]]와 지명 [[123_pipe|파이프]]는 내부적으로 같은 수도관([[022_kernel_role|커널]] 버퍼)을 사용하지만, 전자는 벽 안에 숨겨진 가정용 배관이고 후자는 길가에 공개된 공용 수도전이라 접근성에서 결정적 차이가 나는 것과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — [[626_log_collection|로그 수집]] 데몬과 애플리케이션 간 통신**: 다수의 애플리케이션 프로세스가 중앙 [[626_log_collection|로그 수집]] 데몬에게 [[568_logs_distributed_logging_elk_fluentd|로그]]를 전달해야 하는 상황. 각 애플리케이션은 부모-자식 [[083_relationship_in_er_model|관계]]가 아니므로 일반 [[123_pipe|파이프]]를 사용할 수 없다. 아키텍트는 각 애플리케이션의 [[568_logs_distributed_logging_elk_fluentd|로그]] 출력을 지명 [[123_pipe|파이프]]로 리다이렉트 (Redirect)하여 데몬이 이를 읽도록 구성하는 설계를 선택한다. 예: `app > /tmp/log_fifo &` 방식으로 실행.

2. **시나리오 — 지명 [[123_pipe|파이프]]의 데드락 ([[281_deadlock_definition|Deadlock]]) 위험**: 양방향 통신을 단일 지명 [[123_pipe|파이프]]로 구현하려는 시도에서, 양측 프로세스가 모두 [[289_cqrs_db|쓰기]]로 인해 버퍼가 가득 차고 양측 모두 읽기를 시도하지 않아 영원히 대기하는 데드락 상태가 발생한 상황. 개발자는 반드시 두 개의 지명 [[123_pipe|파이프]] (각각 [[008_단방향_반이중_전이중|단방향]])를 [[087_process_state_transition|생성]]하여 명확한 [[001_dikw_pyramid|데이터]] 흐름 방향을 보장해야 한다.

이 다이어그램은 단일 지명 [[123_pipe|파이프]]로 양방향 통신을 시도할 때 발생하는 데드락의 메커니즘과, 두 개의 지명 [[123_pipe|파이프]]를 사용하여 이를 해결하는 올바른 아키텍처를 시각화한 것이다.

```text
  ┌────────────────────────────────────────────────────────────────────┐
  │           지명 파이프 양방향 통신 — 데드락과 해결                  │
  ├────────────────────────────────────────────────────────────────────┤
  │                                                                    │
  │  [잘못된 설계: 단일 FIFO로 양방향 통신 시도]                       │
  │                                                                    │
  │  Process A                FIFO Buffer              Process B       │
  │  ┌──────────┐         ┌───────────────┐         ┌──────────┐       │
  │  │ Request  │────────▶│ [FULL] 쓰기   │         │ Response │       │
  │  │ (쓰기)   │         │ 대기 중...     │────────▶│ (쓰기)   │      │
  │  │          │◀────────│ 읽기 시도?     │         │          │      │
  │  │ (읽기)   │         │ 누가 먼저?    │◀────────│ (읽기)   │       │
  │  └──────────┘         └───────────────┘         └──────────┘       │
  │       │                                                  │         │
  │       └──── 둘 다 쓰기만 시도 → 버퍼 만원 → DEADLOCK ───┘          │
  │                                                                    │
  │  [올바른 설계: 쌍방향 FIFO (각각 단방향)]                          │
  │                                                                    │
  │  Process A                                              Process B  │
  │  ┌──────────┐         ┌───────────────┐         ┌──────────┐       │
  │  │ Request  │────────▶│ FIFO_AB       │────────▶│ Response │       │
  │  │ (쓰기)   │         │ (A→B 전용)     │         │ (읽기)   │      │
  │  └──────────┘         └───────────────┘         └──────────┘       │
  │  ┌──────────┐         ┌───────────────┐         ┌──────────┐       │
  │  │ Response │◀────────│ FIFO_BA       │◀────────│ Request  │       │
  │  │ (읽기)   │         │ (B→A 전용)     │         │ (쓰기)   │      │
  │  └──────────┘         └───────────────┘         └──────────┘       │
  │                                                                    │
  │  ✅ 데이터 흐름 방향이 명확 → 데드락 불가                          │
  └────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 비교도의 핵심은 지명 [[123_pipe|파이프]]의 [[008_단방향_반이중_전이중|단방향]]성 (Half-Duplex)이라는 근본 설계 특성이다. 단일 FIFO로 양방향 통신을 시도하면, [[300_process|Process]] A와 [[300_process|Process]] B가 동시에 [[289_cqrs_db|쓰기]] 작업을 수행할 때 [[022_kernel_role|커널]] [[123_pipe|파이프]] 버퍼가 가득 차게 되고, 양측 모두 버퍼에 공간이 생기기를 기다리며 읽기를 수행하지 않는 상황, 즉 고전적인 데드락 ([[281_deadlock_definition|Deadlock]])에 빠진다. POSIX 표준에서 지명 [[123_pipe|파이프]]는 [[008_단방향_반이중_전이중|단방향]] 동작만을 보장하므로, 양방향 통신이 필요한 경우에는 반드시 두 개의 지명 [[123_pipe|파이프]]를 [[087_process_state_transition|생성]]하여 각각 명확한 [[008_단방향_반이중_전이중|단방향]] [[001_dikw_pyramid|데이터]] 흐름 (A→B, B→A)을 [[009_config|설정]]해야 한다. 이 패턴은 실무에서 클라이언트-서버 모델의 요청-응답 통신을 지명 [[123_pipe|파이프]]로 구현할 때 반드시 준수해야 하는 설계 원칙이다. [[008_단방향_반이중_전이중|단방향]] 채널을 명확히 분리하는 것은 [[117_ipc|IPC]] 설계에서 데드락을 예방하는 가장 기본적이고 확실한 방법이다.

### 도입 [[435_checklist_based_testing|체크리스트]]
- **기술적**: 지명 [[123_pipe|파이프]] 버퍼 크기 (리눅스 기본 `/proc/sys/fs/pipe-max-size`)가 전송할 메시지의 최대 크기를 수용할 수 있는가? O_NONBLOCK [[186_character_stuffing_dle_stx_etx|플래그]] 사용 여부에 따른 에러 처리 로직이 구현되었는가?
- **운영·보안적**: 지명 [[123_pipe|파이프]] [[501_file_definition_logical_record|파일]]의 퍼미션이 (0666 등) 불필요한 프로세스의 접근을 차단하도록 [[010_least_privilege|최소 권한 원칙]] ([[010_least_privilege|Least Privilege]])으로 [[009_config|설정]]되었는가? 사용이 끝난 [[261_fifo_page_replacement|FIFO]] [[501_file_definition_logical_record|파일]]이 잔류하지 않도록 정리 (Cleanup) 메커니즘이 구현되었는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **SIGPIPE 무시 누락**: Reader 프로세스가 비정상 종료되면 Writer의 `write()` 호출이 SIGPIPE를 발생시켜 프로세스가 강제 종료된다. 반드시 `signal(SIGPIPE, SIG_IGN)`으로 시그널을 무시하거나, `write()` 반환값과 `errno == EPIPE`를 확인하여 우아하게 (Gracefully) 처리해야 한다.

- **📢 섹션 요약 비유**: 양방향 도로를 단일 차선으로 만들면 양쪽에서 온 차가 마주 보고 서로 양보하지 않아 길이 막히는 것(데드락)과 같으므로, 반드시 각 방향 전용 차선([[261_fifo_page_replacement|FIFO]] 두 개)을 분리 설치해야 하는 것과 같습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 일반 [[501_file_definition_logical_record|파일]] 기반 통신 | 지명 [[123_pipe|파이프]] ([[261_fifo_page_replacement|FIFO]]) 도입 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | [[501_file_definition_logical_record|파일]] I/O 경유 (디스크 접근) | [[022_kernel_role|커널]] 메모리 버퍼만 사용 | 통신 레이턴시 **수십~수백 배 단축** |
| **정량** | 수동 파싱 및 [[212_synchronization_mechanisms|동기화]] 구현 필요 | [[261_fifo_page_replacement|FIFO]] 순서 자동 보장 | [[212_synchronization_mechanisms|동기화]] 코드 **제거로 개발 시간 단축** |
| **정성** | [[501_file_definition_logical_record|파일]] 잔류로 인한 디스크 오염 가능 | 디스크 블록 할당 없음 | 시스템 청결성 유지 |

### 미래 전망
- **[[561_container_based_deployment|컨테이너]] 환경에서의 역할 확대**: Docker와 [[205_kubernetes_container_orchestration|Kubernetes]] 환경에서 [[561_container_based_deployment|컨테이너]] 간의 간단한 메시지 전달에 지명 [[123_pipe|파이프]]가 볼륨 마운트를 통해 활용되며, 네트워크 오버헤드가 없는 초경량 [[117_ipc|IPC]] 채널로 주목받고 있다.
- **이벤트 기반 시스템과의 결합**: systemd 등의 현대 init 시스템에서 데몬 간 통신 알림 채널로 지명 [[123_pipe|파이프]]를 활용하여, [[125_socket|소켓]]보다 가벼운 이벤트 통지 (Notification) 메커니즘을 구현하는 사례가 증가하고 있다.

### 참고 표준
- **POSIX.1-2008 (IEEE Std 1003.1)**: `mkfifo()`, [[261_fifo_page_replacement|FIFO]] 특수 [[501_file_definition_logical_record|파일]]의 동작 및 의미 규정
- **SUSv4 (Single UNIX [[148_requirements_specification_formal_informal|Specification]] v4)**: 지명 [[123_pipe|파이프]]의 [[501_file_definition_logical_record|파일]] 시스템 통합 동작 표준

- **📢 섹션 요약 비유**: 복잡한 우편 시스템(네트워크 [[125_socket|소켓]])이나 무거운 택배([[118_shared_memory|공유 메모리]]) 대신, 동네 골목의 공용 게시판(지명 [[123_pipe|파이프]])은 설치가 쉽고 유지보수가 간편하여 소규모 시스템에서 여전히 활발하게 쓰이는 것과 같습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[122_sync_async_communication|동기식 통신]] ([[122_sync_async_communication|Blocking]]) vs 비동기식 통신 (Non-[[122_sync_async_communication|blocking]]) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[123_pipe|파이프]] ([[123_pipe|Pipe]]) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[125_socket|소켓]] ([[125_socket|Socket]]) 통신 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[126_rpc|RPC]] ([[126_rpc|Remote Procedure Call]]) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[파이프 (Pipe)]
    │
    ▼
[지명 파이프 (Named Pipe / FIFO)]
    │
    ├──▶ [소켓 (Socket) 통신]
    └──▶ [RPC (Remote Procedure Call)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 지명 [[123_pipe|파이프]]는 학교 복도에 놓인 **"공용 편지함"**이에요. 이름이 적혀 있어서([[261_fifo_page_replacement|FIFO]]) 어떤 반 친구든 편지를 넣고 꺼낼 수 있어요.
2. 편지함에 먼저 넣은 편지가 먼저 읽힌다는 규칙(First-In-First-Out)이 있어서, 순서가 섞이지 않고 꼭 차례대로 배달된답니다.
3. 편지함 양쪽 문이 모두 열려야 편지를 주고받을 수 있어서, 친구가 오기 전에는 내가 쓴 편지가 편지함 안에서 기다리고 있어요!
