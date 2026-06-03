+++
title = "418. 메모리 매핑 파일 (Memory-Mapped Files, mmap)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 메모리 매핑 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)([mmap](/knowledge-base/studynote/02_operating_system/11_exam_summary/749_memory_mapped_file_mmap/))은 하드디스크에 있는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(`.txt`, `.db`)을 전통적인 `read/write` 함수로 읽어오는 대신, <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>의 내용을 통째로 프로세스의 <a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/">가상 주소 공간</a>(<a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/">Virtual Address Space</a>) <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/">배열</a>에 다이렉트로 꽂아(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/">Mapping</a>) 넣어, 포인터 조작만으로 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>을 램(RAM) 다루듯 씹어먹는 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a>의 흑마술</strong>이다.
> 2. **가치**: [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 공간 버퍼에서 유저 공간 버퍼로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 복사해야 하는 극악의 메모리 카피(Memcpy) 오버헤드를 완벽히 박멸([Zero-Copy](/knowledge-base/studynote/02_operating_system/09_file_system/566_mmap_zero_copy_sendfile/))하여, <strong>기가바이트 단위의 초대형 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>을 파싱하거나 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 기반 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/">IPC</a>(<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/">프로세스 간 통신</a>)를 할 때 압도적인 <a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/">초고속</a> I/O <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong>을 뽑아낸다.
> 3. **융합**: [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)의 코어 엔진인 <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/">요구 페이징</a>(<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/">Demand Paging</a>)</strong> 시스템 위에 그대로 올라타기 때문에, 10GB [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 맵핑해도 램은 1바이트도 소모되지 않다가 CPU가 찌르는(Touch) 순간 딱 4KB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)만 디스크에서 램으로 빨려 올라오는 궁극의 게으른 로딩([Lazy Loading](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/))을 완성한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: `mmap()` (메모리 맵)은 리눅스/유닉스 시스템 콜이다. 1GB짜리 `data.txt` [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 이 함수로 부르면, OS는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 0바이트부터 1GB까지를 프로세스의 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)(예: `0x1000` ~ `0x400000`)에 그대로 포개어 놓는다. 이후 프로그래머는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) I/O 함수를 쓸 필요 없이, 그냥 C언어 포인터 `char* p = 0x1000; p[5] = 'A';` 를 치는 것만으로 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 5번째 글자를 'A'로 바꿔버릴 수 있다.
- **필요성**: 고전적인 `read()` 함수로 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 읽으려면 고통이 따른다. 1) 시스템 콜을 부른다 ([문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 발생), 2) 하드디스크가 읽어서 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리에 일단 담는다. 3) OS가 그걸 다시 유저 앱의 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)([Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/))로 한 땀 한 땀 복사(Memcpy)해 준다. 만약 10GB짜리 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 스캔한다면? 메모리 복사에만 CPU 사이클이 폭발하고 램은 2배로 터져나간다. "아니, 어차피 OS가 램([페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 캐시)에 디스크 내용을 올려놓을 거면, 굳이 내 방(유저 램)으로 복사하지 말고 그냥 OS 방에 있는 그 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 내가 다이렉트로 읽게 허락해 주면 안 돼?"라는 뼈저린 최적화의 갈망이 `mmap`을 창조했다.

- **등장 배경 및 I/O 병목의 분쇄**:
  1. <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/013_system_call/">System Call</a> 오버헤드</strong>: `read()` 루프를 100만 번 돌리면 시스템 콜 100만 번이 터져 서버가 기어갔다.
  2. **Double Copy의 저주**: 디스크 -> [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) -> 유저로 이어지는 이중 복사로 인해 램 대역폭이 작살남.
  3. <strong><a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/">가상 메모리</a> 융합</strong>: 어차피 [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) 시스템이 스왑 디스크를 램처럼 매핑하는 짓([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/))을 잘하니까, 스왑 대신 일반 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 꽂아버려도 완벽히 똑같이 돌겠다는 천재적인 깨달음.

```text
┌─────────────────────────────────────────────────────────────────────┐
│        고전적 read() vs mmap()의 데이터 복사(Zero-Copy) 시각화      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ▶ 1. 고전적 read() 궤적 (비효율의 극치)                             │
│   하드디스크 ──복사1──▶ [ OS 커널 램 (Page Cache) ]                 │
│                         └──복사2──▶ [ 유저 램 (내 앱 배열) ]        │
│   ⚠ 단점: 복사 2번! 램 점유율 2배! 속도 느림!                       │
│                                                                     │
│ ▶ 2. mmap() 궤적 (Zero-Copy 마법)                                   │
│   하드디스크 ──복사1──▶ [ OS 커널 램 (Page Cache) ]                 │
│                              ▲                                      │
│   [ 유저 램 (가상 주소 포인터) ] ──┘ (복사 안 함! 화살표만 연결함!) │
│   ✅ 장점: 램 복사 0회! (Zero-Copy). 유저가 포인터를 찌르면         │
│            OS 커널 램의 데이터가 다이렉트로 수정됨. (빛의 속도)     │
└─────────────────────────────────────────────────────────────────────┘
```
**[다이어그램 해설]** `mmap`은 복사(Copy)를 혐오하는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 해커들의 예술 작품이다. 유저 프로세스의 가상 주소(PTE)를 슬쩍 조작해서, 그 화살표가 가리키는 끝단이 내 힙([Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/))이 아니라 OS가 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 올려둔 램([Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Cache)으로 향하게 만든다. 유저 앱은 자기 변수를 고친다고 생각하지만, 사실은 OS 심장부에 있는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 직빵으로 후드려 패고 있는 셈이다.

- **📢 섹션 요약 비유**: 피자집에서 피자([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))를 시켜 먹을 때, 배달원(read)을 시켜 우리 집 식탁(유저 램)으로 피자를 옮겨와 먹으면 식고 배달비도 듭니다. `mmap`은 아예 식당 주방([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 램)에 뚫린 작은 창구(가상 주소)에 입만 대고, 주방장이 굽는 족족 바로 뜯어먹어 배달비(복사)를 0원으로 만드는 얌체 같은 최적화입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)([Demand Paging](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/))과의 소름 돋는 콜라보
`mmap("10GB_movie.mp4")` 함수를 실행했을 때, 램 16GB 컴퓨터는 터지지 않는다. 왜 그럴까?
- `mmap` 함수 자체는 램에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 1바이트도 올리지 않는다. 그냥 프로세스 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)(장부) 10GB어치를 모두 <strong><code>Invalid(I)</code></strong> 비트로 도배해 놓고 끝난다. (0.001초 컷).
- 프로그래머가 10GB 중 중간에 있는 5GB 위치의 픽셀을 포인터로 찌른다. (`pixel = p[5000000];`)
- 그 순간 하드웨어 MMU가 `I` 비트를 밟고 <strong><a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/">페이지 폴트</a>(<a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/">Page Fault</a>)</strong>를 터뜨린다.
- [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 헐레벌떡 뛰어나와 디스크에서 딱 그 5GB 위치에 있는 4KB 조각 하나만 램으로 퍼와서 꽂아준다.
- 즉, <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>을 다루는 모든 I/O 작업이 <a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/">가상 메모리</a>의 <a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/">페이지 폴트</a> 엔진에 100% 흡수</strong>되어 버린다. 시스템 개발자는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) I/O 코드를 짤 필요조차 없어진다!

---

### Dirty Page와 MSYNC (디스크 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/))
포인터로 값을 바꾸면 램([Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Cache)에 있는 값만 바뀌지, 하드디스크 원본 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 아직 안 바뀐 상태(Dirty)가 된다.
- 이 상태로 전기가 나가면 내가 수정한 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 내용이 다 날아간다.
- OS 백그라운드 데몬(`pdflush`)이 주기적으로 이 Dirty Page들을 디스크에 쓱쓱 덮어써 주긴 하지만, DB 개발자들은 이 게으름을 못 참는다.
- 그래서 메모리를 수정한 뒤 반드시 <strong><code>msync()</code></strong> 라는 시스템 콜을 때려 강제로 "지금 당장 램의 Dirty 조각들을 디스크 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 물리적으로 박아 넣어!"라고 채찍질을 한다. (이것이 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) DB가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유실을 막는 핵심 아키텍처다).

- **📢 섹션 요약 비유**: 칠판(램)에 분필로 아무리 멋진 그림([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수정)을 그려놔도, 폴라로이드 사진(디스크 저장)으로 찰칵! 찍어두지 않으면 밤에 청소부가 칠판을 다 지웠을 때 영원히 사라집니다. `msync`는 불안할 때마다 강제로 사진을 찍게 강제하는 셔터 버튼입니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: 고전 I/O (`read/write`) vs 메모리 맵 (`mmap`)

어떤 상황에서 무엇을 써야 서버가 폭발하지 않는가?

| 비교 항목 | `read()` / `write()` 시스템 콜 | `mmap()` 시스템 콜 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 복사(Copy)</strong> | 디스크 -> [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) -> 유저 (2회 복사) | 디스크 -> [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) (<strong>1회 복사, <a href="/knowledge-base/studynote/02_operating_system/09_file_system/566_mmap_zero_copy_sendfile/">Zero-copy</a></strong>) |
| <strong>적합한 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 크기</strong> | 수십 KB 수준의 작은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | <strong>기가바이트 단위의 초대형 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a></strong> |
| **적합한 접근 패턴** | 처음부터 끝까지 쭉 읽는 **순차(Sequential)** | 여기저기 포인터로 찌르는 **무작위(Random)** |
| **메모리(RAM) 소모** | 내 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 크기만큼 강제로 점유 | OS [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 캐시가 관리하므로 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) 방어 유리 |
| **치명적 단점** | 루프 돌 때마다 시스템 콜 렉 터짐 | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 크기가 바뀌거나(Append) 확장될 때 처리 극혐 |

### 메모리 맵을 이용한 [프로세스 간 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) ([IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) [Shared Memory](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/))
`mmap`의 진짜 파괴력은 혼자 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 읽는 데 있지 않다. 카카오톡과 엑셀이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받아야 한다고 치자.
- [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)이나 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)([Pipe](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/))로 통신하면, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 버퍼로 복사하고 핑퐁 치느라 오버헤드가 작살난다.
- **해결책**: 카톡과 엑셀이 똑같은 `shared_data.txt` [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 `mmap`으로 매핑한다.
- OS는 두 프로세스의 가상 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 화살표를 물리 램의 '동일한 프레임([Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Cache 1장)'에 십자수처럼 꽂아버린다.
- 카톡이 포인터 변수에 `A`를 쓰면, 엑셀이 0.000001초 만에 자기 포인터에서 `A`를 바로 읽어낸다! 
- 시스템 콜 0회, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사 0회. <strong>세상에서 존재하는 가장 빠르고 폭력적인 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/">프로세스 간 통신</a>(<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/">IPC</a>) 채널이 바로 이 <code>mmap</code> <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/">공유 메모리</a>다.</strong>

```text
┌──────────┬────────────┬────────────┬──────────────────────────────┐
│ 통신 방식  │ 커널 개입 횟수│ 데이터 복사 횟수│ 속도 한계          │
├──────────┼────────────┼────────────┼──────────────────────────────┤
│ Pipe(파이프)│ 매번 개입 (느림)│ 2번 (커널 거침) │ 메가바이트 급   │
│ Socket   │ 매번 개입 (느림)│ 2번 + 네트워킹 │ 킬로바이트 급       │
│ **mmap** │ **초기 1번 끝**│ **0번(Zero!)**│ **램 스피드(기가급)** │
└──────────┴────────────┴────────────┴──────────────────────────────┘
```
**[매트릭스 해설]** 로컬 머신에서 안드로이드 카메라 앱의 1초에 60장씩 뿜어내는 4K 무압축 프레임(수십 MB)을 렌더링 앱으로 넘길 때, [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)나 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)을 쓰면 폰이 불타며 폭발한다. 무조건 안드로이드의 `Ashmem`이나 `mmap`을 통해 물리적 복사 없이 껍데기 포인터만 던져주는 메모리 맵 공유를 써야만 실시간 60프레임이 유지된다.

- **📢 섹션 요약 비유**: 옆집과 편지([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 주고받을 때 우체부([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))를 부르면 하루가 걸립니다([파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)/[소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)). 대신 두 집 사이의 벽을 허물고 커다란 칠판([mmap](/knowledge-base/studynote/02_operating_system/11_exam_summary/749_memory_mapped_file_mmap/) [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/))을 하나 놔두면, 내가 분필로 글을 쓰는 그 즉시 옆집에서 실시간으로 읽고 답장을 쓸 수 있는 빛의 속도 통신망이 열립니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: MongoDB의 흑역사와 ElasticSearch의 성공
1. <strong>MongoDB의 <a href="/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> 실수</strong>: 
   - 몽고DB [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 버전은 자체적인 디스크 읽기 로직을 버리고 100% OS의 `mmap`에 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 관리를 위임했다. "[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)아 네가 알아서 램에 올리고 지워줘!"
   - [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 1TB로 커지자 대재앙이 났다. 잦은 수정(Write)으로 Dirty Page가 수백 GB 쌓였는데, 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 데몬(`pdflush`)이 이걸 하드디스크에 한 번에 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)시키려고 스레드를 얼려버려 DB가 수십 초씩 기절했다. (결국 몽고DB는 mmap을 버리고 WiredTiger 엔진으로 도망침).
2. **ElasticSearch의 승리 (Lucene 엔진)**:
   - 전 세계 최고의 검색 엔진 엘라스틱서치는 반대로 `mmap`을 신처럼 다룬다.
   - 검색 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(`.cfs`)은 만들어진 후 절대 수정되지 않는 **읽기 전용(Read-Only, Clean)** [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이다.
   - 100GB짜리 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 `mmap`으로 올려두면, 아무리 램이 꽉 차서 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 쫓겨나도 Dirty Page가 아니므로 디스크 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 렉(8ms)이 전혀 발생하지 않고 0.1초 만에 램에서 쓱쓱 삭제(Drop)된다. 
   - 램 64GB짜리 서버로 1TB [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 전문 검색을 0.1초 만에 끝내는 ES의 미친 속도는 바로 이 `mmap`의 특징(Clean [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 드랍)을 극한까지 악용한 아키텍처 덕분이다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/): mmap에 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 덧붙이기 (Append)
`mmap`은 치명적 약점이 있다. 처음에 `1GB`로 맵핑을 딱 박아놓았는데, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이라서 뒤에 글씨를 추가(Append)해 1.1GB가 되면? 맵핑된 가상 주소 바깥을 뚫고 나가므로 냅다 <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/">Segmentation</a> Fault</strong>를 맞고 서버가 즉사한다. `mmap`은 크기가 픽스된 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 씹어먹을 땐 로켓이지만, 카카오톡 채팅 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)처럼 길이가 쭉쭉 늘어나는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 쓰면 `remap` 하느라 지옥을 본다.

- **📢 섹션 요약 비유**: `mmap`은 이미 다 만들어진 백과사전(Read-Only [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))을 이리저리 뒤적거리며 찾을 때는 천하무적의 돋보기입니다. 하지만 오늘부터 내가 일기를 매일 한 장씩 추가로 써 내려가는 공책(Append [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))에 이 돋보기를 쓰면 책의 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 늘어날 때마다 돋보기 렌즈를 깨부수고 새로 맞춰야 하는 끔찍한 제약이 있습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 내용 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/566_mmap_zero_copy_sendfile/">Zero-Copy</a> <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 달성</strong> | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리에서 유저 메모리로의 이중 복사를 원천 차단하여, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) I/O에 소모되는 CPU 사이클과 램 대역폭을 사실상 0으로 수렴 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/">요구 페이징</a>의 I/O 융합</strong> | C언어의 포인터 접근(`*p`) 하나만으로 복잡한 디스크 섹터 읽기를 하드웨어 [Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Fault로 퉁쳐버리는 우아한 코드 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) |
| <strong>가장 빠른 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/">IPC</a> 제공</strong> | 수백 MB의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 프로세스끼리 주고받을 때 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)이나 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)의 병목 없이 램 스피드(GB/s)로 통신하는 물리적 지름길 제공 |

### 결론 및 미래 전망

메모리 매핑 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) (`mmap`)은 "모든 것은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이다(Everything is a [file](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))"라는 유닉스의 고전 철학과 "모든 것은 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)다"라는 현대 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 진리가 충돌하여 빚어낸 가장 찬란한 합작품이다. 디스크 I/O와 램 접근이라는 완전히 다른 두 세계의 장벽을 '[페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 매핑'이라는 망치 하나로 박살 내버린 이 흑마술은, 오늘날 수조 단위의 문서를 검색하는 ElasticSearch부터 초당 60프레임을 그리는 모바일 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 버퍼 셰어링에 이르기까지 모든 고성능 소프트웨어의 심장부에서 펄떡이고 있다. 미래에는 NVM(비휘발성 메모리)이 디스크를 완전히 대체하게 되면서, `read`/`write`라는 구시대의 함수는 박물관으로 가고 오직 `mmap` 형태의 직접 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)(Byte-Addressable) 접근만이 [영구 스토리지](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/098_kubernetes_storage_volume_pv_pvc/) I/O의 유일한 표준으로 천하를 통일할 것이다.

- **📢 섹션 요약 비유**: 은행 창구(read/write)를 거쳐 서류를 내고 10분 기다려 돈([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 뽑아 쓰던 구시대에서, 내 통장 계좌를 직접 스마트폰 핀테크([mmap](/knowledge-base/studynote/02_operating_system/11_exam_summary/749_memory_mapped_file_mmap/))로 연결해 버튼 한 번 누르는 즉시 내 지갑으로 돈이 복사되는 핀테크(FinTech) 혁명이 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 안에서 벌어진 것입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [워킹 셋 모델](/knowledge-base/studynote/02_operating_system/07_virtual_memory/416_working_set_model/) ([Working-Set Model](/knowledge-base/studynote/02_operating_system/07_virtual_memory/416_working_set_model/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [페이지 부재 빈도](/knowledge-base/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/) ([PFF](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/), [Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)-Fault Frequency) 모델 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) I/O를 메모리 접근으로 변환, [버퍼 캐시](/knowledge-base/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/) 활용, 프로세스 간 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)로 사용 가능 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 메모리 맵 I/O (Memory-Mapped I/O) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[페이지 부재 빈도 (PFF, Page-Fault Frequency) 모델]
    │
    ▼
[메모리 매핑 파일 (Memory-Mapped Files, mmap)]
    │
    ├──▶ [파일 I/O를 메모리 접근으로 변환, 버퍼 캐시 활용, 프로세스 간 공유 메모리로 사용 가능]
    └──▶ [메모리 맵 I/O (Memory-Mapped I/O)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 메모리 매핑 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) (Memory-Mapped Files, [mmap](/knowledge-base/studynote/02_operating_system/11_exam_summary/749_memory_mapped_file_mmap/))은 컴퓨터가 메모리를 더 크게 보이게 하고 부족함을 숨기는 방법이에요.
2. 먼저 [페이지 부재 빈도](/knowledge-base/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/) ([PFF](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/), [Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)-Fault Frequency) 모델을 이해하면 메모리 매핑 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) (Memory-Mapped Files, [mmap](/knowledge-base/studynote/02_operating_system/11_exam_summary/749_memory_mapped_file_mmap/))이 왜 필요한지 더 쉽게 보여요.
3. 그래서 메모리 매핑 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) (Memory-Mapped Files, [mmap](/knowledge-base/studynote/02_operating_system/11_exam_summary/749_memory_mapped_file_mmap/))을 잘 알면 나중에 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) I/O를 메모리 접근으로 변환, [버퍼 캐시](/knowledge-base/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/) 활용, 프로세스 간 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)로 사용 가능도 훨씬 쉽게 배울 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 418 / 800

← **이전**: [417. 페이지 부재 빈도 (PFF, Page-Fault Frequency) 모델 - 상한/하한 설정하여 동적 프레임 할당 조절](/knowledge-base/studynote/02_operating_system/07_virtual_memory/417_page_fault_frequency/)
**다음**: [419. 파일 I/O를 메모리 접근으로 변환, 버퍼 캐시 활용, 프로세스 간 공유 메모리로 사용 가능 (mmap Shared Memory)](/knowledge-base/studynote/02_operating_system/07_virtual_memory/419_mmap_shared_memory/) →

---
