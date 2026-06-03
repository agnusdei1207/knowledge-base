+++
title = "749. 메모리 매핑 파일 (mmap)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [메모리 매핑 파일](/knowledge-base/studynote/02_operating_system/07_virtual_memory/418_memory_mapped_file_mmap/) (mmap)은 하드 디스크에 있는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 내용을 프로세스의 [가상 주소 공간](/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/)([Virtual Address Space](/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/))에 논리적으로 1:1 연결(매핑)하여, <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> I/O를 마치 메모리 <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/">배열</a>(<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/">Array</a>)에 접근하는 것처럼 처리하는 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 기술</strong>이다.
> 2. **가치**: 지루하고 무거운 `read()`, `write()` 시스템 콜과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 중복 복사(CPU Copy) 과정을 완전히 제거함으로써, 대용량 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 처리와 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 엔진의 I/O [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 극한으로 끌어올리는 제로 카피([Zero-copy](/knowledge-base/studynote/02_operating_system/09_file_system/566_mmap_zero_copy_sendfile/))의 근간이 된다.
> 3. **융합**: [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)의 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)([Demand Paging](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)) 메커니즘과 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 캐시([Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Cache)를 물리적으로 통합시킨 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 아키텍처의 걸작이며, 프로세스 간 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)([Shared Memory](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)) 구현에도 널리 쓰인다.

---

## Ⅰ. 개요 및 필요성

- **개념**: UNIX/Linux의 `mmap()` (Memory Mapped) 시스템 콜은 특정 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 일부나 전체를 프로세스의 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 영역으로 끌어들인다. 매핑이 끝나면 개발자는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)([File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) Descriptor)를 통한 [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/) 대신, 단순한 포인터 변수(`char *p`)에 값을 대입하는 것만으로 디스크의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 수정할 수 있다.

- <strong>필요성 (전통적 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">File</a> I/O의 비효율 극복)</strong>: 
  - 전통적인 `read()` 함수로 1GB [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 읽으려면 끔찍한 병목이 발생한다.
  - 디스크에서 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리([버퍼 캐시](/knowledge-base/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/))로 1번 복사 $\rightarrow$ [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리에서 유저 메모리(앱 버퍼)로 2번 복사(CPU 소모) $\rightarrow$ 이 과정에서 수백 번의 유저-[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)) 발생.
  - **해결책**: "[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 있는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 캐시 공간 주소를, 아예 유저 프로세스의 포인터에 다이렉트로 연결(매핑)해주자. 그러면 복사도, 시스템 콜도 필요 없다!"

  - **전통적 read/write**: 도서관 서고(디스크)에 있는 책을 볼 때마다, 사서([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))에게 신청서(시스템 콜)를 내서 책 내용을 복사기(버퍼)로 복사본을 뜬 뒤 내 책상으로 가져와서 보는 방식. (느리고 귀찮고 복사본 쓰레기가 생김)
  - **mmap (메모리 매핑)**: 아예 도서관 서고의 특정 책장 위치로 직통하는 '마법의 창문(포인터)'을 내 책상 위에 뚫어놓은 것. 창문 너머로 펜을 뻗어 책에 직접 글씨를 쓰면(메모리 수정) 그게 곧바로 도서관 원본 책([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))에 반영되는 방식.

- **등장 배경**: 
  - 시스템 메모리 용량이 커지면서, [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 서브시스템과 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 캐시 계층을 하나로 합치는 <strong>통합 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/">버퍼 캐시</a> (Unified <a href="/knowledge-base/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/">Buffer Cache</a>)</strong> 아키텍처가 최신 OS에 정착됨에 따라 자연스럽게 구현된 강력한 I/O 최적화 기법이다.

```text
  ┌─────────────────────────────────────────────────────────────┐
  │                 전통적 파일 I/O vs 메모리 매핑 파일(mmap) 구조 차이     │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  [ 전통적 read() / write() ]                                │
  │   ┌── 유저 공간 (User Space) ──────────┐                    │
  │   │  App 버퍼 (char buf[4096])       │                    │
  │   └─── ▲ ──── | ────────────────────┘                    │
  │     (CPU 복사) ▼  (수백 번의 시스템 콜)                       │
  │   ┌── 커널 공간 (Kernel Space) ────────┐                    │
  │   │  페이지 캐시 (Page Cache)         │                    │
  │   └─── ▲ ──── | ────────────────────┘                    │
  │      (DMA)     ▼                                            │
  │   [ 하드 디스크 (데이터 파일) ]                                  │
  │                                                             │
  │                                                             │
  │  [ 메모리 매핑 (mmap) ]  - "복사도 없고 시스템 콜도 없다!"             │
  │   ┌── 유저 가상 메모리 공간 ────────────┐                     │
  │   │  포인터 주소 (char *p) ---------┐   │                     │
  │   └─────────────────────────────────┼─┘                     │
  │                                     │  논리적 1:1 매핑        │
  │   ┌── 커널 공간 (Kernel Space) ────────┼─┐                    │
  │   │  페이지 캐시 (Page Cache) ◀-------┘  │                    │
  │   └─── ▲ ──── | ────────────────────┘                    │
  │      (DMA)     ▼                                            │
  │   [ 하드 디스크 (데이터 파일) ]                                  │
  └─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 위쪽의 전통적 방식은 유저 공간과 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 공간 사이에 거대한 장벽이 있다. 앱이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 원할 때마다 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 문을 두드려야 하고, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 자신의 캐시 공간에 있는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 굳이 유저의 버퍼로 한 번 더 복사(CPU 연산 소모)해서 넘겨준다. 반면 아래쪽의 `mmap` 방식은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 자신이 쥐고 있는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 캐시(물리 메모리)의 주소록을 유저 프로세스의 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)(가상 주소)에 그대로 등록해 버린다. 즉, 유저가 메모리 포인터(`*p`)를 읽고 쓰면, 그게 사실은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 캐시 메모리를 직접 건드리는 것이다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복 복사가 사라지는 궁극의 제로 카피([Zero-copy](/knowledge-base/studynote/02_operating_system/09_file_system/566_mmap_zero_copy_sendfile/))가 완성된다.

- **📢 섹션 요약 비유**: 물건을 살 때마다 중간 유통 상인([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 복사)을 거쳐 수수료를 내는 구조에서, 산지 농장 창고([페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 캐시)와 내 냉장고 사이에 직통 텔레포트 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)(mmap)를 연결하여 중간 유통 단계를 완전히 삭제해 버린 혁명적인 유통망입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### mmap의 내부 동작 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 ([요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)과의 결합)

초보자들이 흔히 하는 오해는 "`mmap`을 호출하면 1GB [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 메모리에 통째로 올라가서 메모리가 펑크 난다"는 것이다. 틀렸다. `mmap`의 천재성은 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)의 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)([Demand Paging](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/))과 결합하여, <strong>내가 진짜로 포인터를 건드린 부분(<a href="/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">Page</a>)만 메모리에 올라온다</strong>는 점이다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 mmap의 지연 할당 (Lazy Loading) 기반 내부 동작 원리       │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   1. 매핑 셋업 (mmap 호출 시점)                                        │
  │      App: `p = mmap(..., "big_file.dat", ...)`                    │
  │      OS : 가상 주소 공간에 VMA(Virtual Memory Area) 구조체만 딸랑 만듦.  │
  │           페이지 테이블은 비어 있음 (Valid 비트 = 0).                  │
  │           ※ 주의: 이때 디스크 I/O는 1바이트도 일어나지 않음! 🚀 초고속      │
  │                                                                   │
  │   2. 실제 메모리 접근 (포인터 읽기/쓰기 시점)                             │
  │      App: `char c = p[5000];` (특정 오프셋 데이터 접근 시도)            │
  │      CPU: 어? 페이지 테이블에 매핑된 물리 메모리가 없네?                 │
  │           ──▶ 🚨 페이지 폴트 (Page Fault) 인터럽트 발생!             │
  │                                                                   │
  │   3. 커널의 페이지 폴트 핸들러 처리                                      │
  │      OS : "아! mmap 해둔 파일이구나!"                                 │
  │           디스크에서 파일의 5000번지 근처 4KB(1페이지) 조각만 DMA로 퍼올림. │
  │           페이지 테이블에 방금 가져온 물리 프레임 주소 연결 (Valid = 1)   │
  │                                                                   │
  │   4. 변경분 동기화 (Dirty Page Write-back)                           │
  │      App: `p[5000] = 'Z';` (데이터 수정)                             │
  │      OS : 백그라운드 스레드(pdflush)나 `msync()` 호출 시, 더티 페이지를    │
  │           모아두었다가 디스크 원본 파일에 비동기로 몰아서 씀.                │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** `mmap`의 심장부는 '가짜 약속([Lazy Loading](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/))'이다. 100GB짜리 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 mmap으로 묶어도, OS는 "이 가상 주소 범위는 디스크 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 어느 위치와 연결되어 있다"라는 명함([VMA](/knowledge-base/studynote/02_operating_system/07_virtual_memory/428_vma_struct/))만 파놓을 뿐 물리적 RAM은 1바이트도 소모하지 않는다. 나중에 애플리케이션 코드가 그 주소를 진짜 건드리는 순간에 하드웨어가 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)) 트랩을 걸고, OS가 그제야 부리나케 디스크에서 해당 4KB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 단위만 쏙 뽑아 메모리에 채워준다. 메모리가 꽉 차면 안 쓰는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)부터 다시 디스크 스왑이 아닌 원본 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 내쫓으면 되므로 메모리 관리조차 완벽하게 효율적이다.

### mmap의 두 가지 필수 공유 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) (MAP_SHARED vs MAP_PRIVATE)

[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 매핑할 때, 내가 메모리에 쓴 내용이 원본 디스크 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에까지 영향을 미칠 것인지 결정해야 한다.

| [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) | 매핑 방식 | 메모리 수정 시 동작 (Write 행위) | 활용 시나리오 |
|:---|:---|:---|:---|
| **MAP_SHARED** | 공유 매핑 | 내가 포인터에 쓴 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 <strong>원본 디스크 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>에 영구히 덮어씌워짐</strong>. 다른 프로세스도 이 뷰를 실시간으로 공유함. | [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) I/O, [IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) 통신 ([공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)) |
| **MAP_PRIVATE**| 개별 복사 매핑 | 내가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쓰려고 하는 순간 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 통째로 메모리에 하나 더 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)함 (<strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/">Copy-on-Write</a></strong>). 원본 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 절대 바뀌지 않음. | C/C++ 프로그램 실행 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(바이너리) 적재, [공유 라이브러리](/knowledge-base/studynote/02_operating_system/06_memory_management/333_shared_library/)(.so, .dll) 로딩 |

- **📢 섹션 요약 비유**: `MAP_SHARED`는 구글 독스(Google Docs) 링크를 열어 여러 명이 원본 문서를 실시간으로 동시 편집하는 것이고, `MAP_PRIVATE`는 구글 독스 문서를 "내 컴퓨터로 다운로드([복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))"해서 나 혼자만 빨간 펜으로 낙서해 보는 것과 같습니다.

---

## Ⅲ. 비교 및 연결

### Mmap (제로 카피) vs 일반 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) I/O 시스템 콜 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교

어떤 기법이 무조건 좋은 것은 아니다. I/O 패턴에 따라 치명적인 역효과가 발생하기도 한다.

| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 요소 | mmap 기반 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 접근 | read() / write() 기반 접근 |
|:---|:---|:---|
| **오버헤드** | [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 없음, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사(CPU Copy) 0회 | 매 호출마다 시스템 콜 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 발생, 버퍼 복사 1회 추가 발생 |
| **순차 읽기 (Sequential)**| 오히려 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 처리 오버헤드 때문에 느릴 수 있음 | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 '[미리 읽기](/knowledge-base/studynote/02_operating_system/09_file_system/537_read_ahead_delayed_write/)([Read-ahead](/knowledge-base/studynote/02_operating_system/09_file_system/537_read_ahead_delayed_write/))' 최적화가 완벽히 적용되어 매우 빠름 |
| **랜덤 읽기 (Random)** | 극도로 빠름. 포인터 이동만으로 랜덤 섹터 즉시 접근 | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 `lseek()`로 계속 포인터 이동해야 하므로 최악의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
| **코드 복잡도** | 포인터 연산(`*p`)으로 단순함 | 버퍼 사이즈 쪼개기, 예외 처리(While 루프) 복잡함 |
| <strong>대형 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> (100GB 이상)</strong>| 32비트 OS에서는 [가상 주소 공간](/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/)(4GB) 고갈로 에러 남 (64비트 필수) | 가상 주소 한계 없이 청크(Chunk) 단위로 무한정 처리 가능 |

### 과목 융합 관점

- <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a> <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/">프로세스 간 통신</a> (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/">IPC</a>)</strong>: 서로 남남인 프로세스 A와 프로세스 B가 통신할 때, 가장 빠르고 효율적인 방법이 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)([Shared Memory](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/))다. 굳이 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)나 소켓을 쓰지 않고, 두 프로세스가 동일한 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 `MAP_SHARED`로 `mmap` 해버리면 두 프로세스의 포인터가 똑같은 물리 RAM [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 가리키게 된다. A가 포인터에 글자를 쓰면 B의 포인터에서 즉시 그 글자가 보인다. (물론 [세마포어](/knowledge-base/studynote/02_operating_system/04_synchronization/224_semaphore/)/뮤텍스 동기화는 필수다).
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> 아키텍처 (DB)</strong>: [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/), LMDB, [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 릴레이셔널 DB의 일부 엔진들은 거대한 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) I/O 서브시스템을 직접 짜는 대신, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 통째로 OS의 `mmap`에 맡겨버렸다. "메모리 캐싱과 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 교체는 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 세계 최고니, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 VMM([Virtual Memory](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) Manager)에게 DB 메모리 관리 전체를 외주 주겠다"는 강력하고 게으른 철학이다.

- **📢 섹션 요약 비유**: 순차적으로 처음부터 끝까지 책을 읽을 때는 그냥 한 장씩 넘겨주는 기계(read)가 빠릅니다. 하지만 책의 10페이지, 800페이지, 35페이지를 미친 듯이 왔다 갔다 넘겨보며(랜덤 액세스) 공부할 때는, 책 전체를 내 책상에 쫙 펼쳐놓고 눈동자만 굴리는(mmap) 방식이 압도적으로 유리합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오 및 최적화 함정

1. <strong>시나리오 — 대용량 <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 검색 시스템의 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 저하</strong>: 50GB짜리 아파치 웹 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에서 특정 에러 코드를 검색하는(grep) 스크립트를 C언어로 짰다. `mmap`이 무조건 빠르다는 소문을 듣고 50GB 전체를 mmap으로 매핑해서 `strstr` 함수로 순차 검색을 돌렸는데, 기존 `read()` 방식보다 시스템이 버벅거리고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 더 안 나온다.
   - **원인 분석**: `mmap`은 접근할 때마다 숨겨진 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/))를 일으킨다. 순차적으로 한 번만 훑고 버리는(Sequential Scan) 작업에서는, 4KB마다 지속적으로 폴트 인터럽트가 걸리는 mmap보다, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 알아서 2MB씩 통째로 메모리로 당겨주는([Read-ahead](/knowledge-base/studynote/02_operating_system/09_file_system/537_read_ahead_delayed_write/)) `read()` 시스템 콜이 오버헤드가 훨씬 적다.
   - **아키텍트 판단**: mmap 맹신은 안티패턴이다. 랜덤 액세스가 잦거나, 여러 번 반복해서 읽는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)일 때만 mmap을 쓴다. 만약 굳이 mmap을 써야 한다면 `madvise(MADV_SEQUENTIAL)` 함수를 OS에 힌트로 던져주어, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 미리 앞의 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 공격적으로 당겨오게끔([Read-ahead](/knowledge-base/studynote/02_operating_system/09_file_system/537_read_ahead_delayed_write/)) 하드웨어 튜닝을 지시해야 한다.

2. <strong>시나리오 — 메모리 맵 기반 DB 엔진의 블로킹(<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/">Blocking</a>) 크래시 현상</strong>: mmap 기반으로 구동되는 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)에서 쿼리를 처리하다가, 갑자기 DB 프로세스 전체가 수 밀리초 동안 멈칫(Stall)하는 현상이 주기적으로 발생한다.
   - **원인 분석**: 포인터 연산(`*p`)은 코드상으로는 CPU [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 연산처럼 보여서 즉시 끝날 것 같다. 하지만 해당 주소의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 아직 메모리에 안 올라와서 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)가 터지면, OS는 디스크에서 그 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 퍼 올릴 때까지(수 밀리초) 프로세스를 블로킹(I/O Wait) 상태로 무자비하게 재워버린다.
   - **아키텍트 판단**: 애플리케이션 입장에서는 변수에 접근했을 뿐인데 스레드가 정지당하는 끔찍한 예측 불가능성이 mmap의 치명적 단점이다. [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 시간이 치명적인 시스템에서는 mmap 대신 `io_uring` 이나 비동기 I/O (AIO)를 통해 디스크 I/O를 철저히 이벤트 루프로 관리하는 모던 아키텍처로 넘어가야 한다. (그래서 최신 [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) WiredTiger 엔진 등은 mmap 의존도를 줄이고 자체 버퍼 풀을 구축했다.)

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 파일 I/O 기술 선택을 위한 아키텍트 의사결정 트리            │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ 대용량 데이터 파일 처리 모듈을 설계한다 ]                             │
  │                │                                                  │
  │                ▼                                                  │
  │      접근 패턴이 순차적(Sequential)이고 한 번만 읽고 버리는가?            │
  │          ├─ 예 ─────▶ [ read() / write() + 큰 청크 버퍼 사용 ]     │
  │          │                                                        │
  │          └─ 아니오 (이리저리 건너뛰며 반복적으로 탐색/수정한다)              │
  │                │                                                  │
  │                ▼                                                  │
  │      파일의 일부분만 랜덤하게 자주 수정하거나, 프로세스 간 공유가 필요한가?    │
  │          ├─ 예 ─────▶ [ mmap() 적용 검토 (제로 카피 효과 극대화) ] │
  │          │             (단, 64비트 OS 여부 및 페이지 폴트 지연 주의)    │
  │          │                                                        │
  │          └─ 아니오 (극단적 저지연 Non-blocking 반응이 무조건 필수다)        │
  │                │                                                  │
  │                ▼                                                  │
  │      [ io_uring 또는 Direct I/O (O_DIRECT) 도입 ]                  │
  │      OS 페이지 캐시를 아예 믿지 않고 애플리케이션이 직접 메모리 큐를 통제       │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 흐름도는 I/O 처리의 정답이 없음을 보여준다. 무거운 대용량 시스템에서는 단순히 함수 하나 바꾸는 것이 튜닝이 아니다. `read`는 중복 복사가 문제고, `mmap`은 예측 불허의 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 멈춤 현상이 문제다. 궁극의 실시간성이 필요하면 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 모든 개입([페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 캐시)을 치워버리고 디스크와 직접 대화하는 `Direct I/O`라는 어둠의 마법을 꺼내 들어야 한다. 기술사는 이 세 가지 무기의 장단점을 상황에 맞게 꺼내 쓰는 지휘관이다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **SIGBUS 에러 방어**: mmap을 걸어둔 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 크기(예: 10MB)를 넘어서는 포인터 주소(예: 11MB 오프셋)를 앱에서 읽으려 하거나, 다른 프로세스가 원본 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 삭제(Truncate)해버렸을 때, 내 프로세스는 `SIGBUS`라는 치명적인 하드웨어 시그널을 맞고 즉시 강제 종료(Crash)된다. mmap을 쓸 때는 반드시 시그널 핸들러를 등록하여 비정상적인 메모리 접근에 대한 예외 처리를 해야 한다.

- **📢 섹션 요약 비유**: 서고의 책과 내 노트를 통로(mmap)로 연결해 편하게 쓰고 있는데, 갑자기 도서관 사서가 그 책을 찢어버리면 통로 너머로 펜을 뻗었던 내 팔이 부러지는(SIGBUS 크래시) 대형 사고가 납니다. 포인터의 유효성을 항상 안전하게 방어해야 합니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 일반 시스템 콜 (read/write) | 메모리 매핑 (mmap) | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (복사 오버헤드)**| [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 버퍼 $\rightarrow$ 유저 버퍼 복사 1회 발생 | [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 캐시를 다이렉트로 공유하여 복사 0회 | CPU 사이클 절감 및 메모리 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 트래픽 대폭 감소 |
| <strong>정량 (<a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/">컨텍스트</a> <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a>)</strong>| 1KB 읽을 때마다 [System Call](/knowledge-base/studynote/02_operating_system/01_overview_architecture/013_system_call/) [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) | 포인터 접근 시 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 외엔 개입 없음 | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)-유저 모드 전환에 따른 나노초 단위 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 수백 배 절감 |
| **정성 (코드 직관성)** | 오프셋을 구하는 `lseek` 코드 난립 | [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 변수에 인덱스로 `array[i]` 접근 | [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(예: [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) 탐색) 로직 작성의 극단적 단순화 |

### 미래 전망
- **NVDIMM과 영구 메모리 (Persistent Memory) 시대의 표준 I/O**: Intel Optane DC 같은 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 단위 접근이 가능한 [차세대 비휘발성 메모리](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/493_scm_pram_mram/)(PMEM)가 서버 메인보드에 꽂히면서, 디스크와 램의 경계가 완전히 무너졌다. 이 환경에서는 블록 단위의 `read/write` [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 자체가 성립하지 않으므로, OS의 I/O 시스템을 모두 건너뛰고 CPU가 메모리 맵(DAX, [Direct](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) Access) 포인터로 디스크에 직접 글자를 새기는 <strong>mmap 전성시대</strong>가 다시 열리고 있다.
- <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/639_rdma_kernel_bypass/">RDMA</a> 기반 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> mmap</strong>: 로컬 디스크의 매핑을 넘어, 클러스터로 묶인 원격 서버의 물리 메모리 자체를 내 프로세스의 가상 주소로 `mmap`하여 다이렉트로 읽고 쓰는(Distributed [Shared Memory](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)) 초거대 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 아키텍처 연구가 [HPC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/548_automotive_hpc/)(고성능 컴퓨팅) 분야에서 가속화되고 있다.

### 참고 표준
- **POSIX.1b (mmap, msync, munmap)**: UNIX 계열 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)에서 [메모리 매핑 파일](/knowledge-base/studynote/02_operating_system/07_virtual_memory/418_memory_mapped_file_mmap/)을 구현하고 제어하는 국제 표준 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 스펙.
- **SNIA PMDK (Persistent Memory Development Kit)**: 영구 메모리(PMEM) 환경에서 mmap을 기반으로 [락-프리](/knowledge-base/studynote/02_operating_system/04_synchronization/256_lock_free_data_structures/), 제로 카피 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조를 구축하기 위한 개방형 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 집합.

[메모리 매핑 파일](/knowledge-base/studynote/02_operating_system/07_virtual_memory/418_memory_mapped_file_mmap/)(mmap)은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 이질적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 덩어리를, CPU가 가장 사랑하고 잘 다루는 순수한 형태인 '메모리 포인터'로 둔갑시켜주는 우아한 마법이다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 복사되며 시스템 계층을 오르내리는 마찰(Friction)을 0으로 만들어버리는 이 "제로 카피" 철학은 훗날 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 전송 함수인 `sendfile()`과 네트워크 패킷 바이패스 기술들의 영감적 토대가 되었으며, 오늘날 영구 메모리 하드웨어의 출현과 함께 컴퓨터 공학의 궁극적 I/O 형태로 귀환하고 있다.

- **📢 섹션 요약 비유**: 옛날에는 외국(디스크)에서 온 편지를 번역가([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))를 통해 한 줄씩 듣고 답장해야 했다면, mmap은 외국어 자체가 내 머릿속 메모리에 직접 번역되어 꽂히는 텔레파시 임플란트 칩을 박아 넣은 것과 같은 소통의 혁명입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| I/O [풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/) ([Polling](/knowledge-base/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/)) 오버헤드 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [스풀링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/457_spooling/) ([Spooling](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/457_spooling/)) 버퍼 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [쓰기 시 복사](/knowledge-base/studynote/02_operating_system/07_virtual_memory/393_copy_on_write/) ([COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [SMP](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/195_real_time_scheduling/) [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) 폴스 셰어링 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[스풀링 (Spooling) 버퍼]
    │
    ▼
[메모리 매핑 파일 (mmap)]
    │
    ├──▶ [쓰기 시 복사 (COW)]
    └──▶ [SMP 캐시 일관성 폴스 셰어링]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 전통적인 방식은 도서관(하드디스크)에 있는 책을 보려면 사서 선생님([운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))한테 부탁해서 내 책상으로 책 복사본을 무겁게 가져와야 했어요.
2. 하지만 메모리 매핑(mmap) 마법을 쓰면, 내 책상 위에 '마법의 투명 창문(포인터)'이 생겨서 도서관에 있는 원본 책이 짠! 하고 비쳐 보인답니다.
3. 책을 일일이 복사해서 옮길 필요 없이 창문 너머로 펜을 뻗어 글씨를 쓰면 원본 책이 즉시 수정되니까, 컴퓨터가 엄청나게 빠르게 일을 처리할 수 있게 된 거예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 749 / 800

← **이전**: [748. 스풀링 (Spooling) 버퍼](/knowledge-base/studynote/02_operating_system/11_exam_summary/748_spooling_buffer/)
**다음**: [750. 쓰기 시 복사 (COW)](/knowledge-base/studynote/02_operating_system/11_exam_summary/750_copy_on_write_cow/) →

---
