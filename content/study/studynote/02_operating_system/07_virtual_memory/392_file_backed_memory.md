---
title: 392. 파일 지원 메모리 (File-backed Memory) - 실행 파일, 공유 라이브러리
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[501_file_definition_logical_record|파일]] 지원 메모리([[501_file_definition_logical_record|File]]-backed Memory)는 물리 램(RAM)에 올라온 특정 [[001_dikw_pyramid|데이터]] 조각이 **하드디스크의 실제 [[501_file_definition_logical_record|파일]](예: `.exe`, `.so`, `.txt`) 내용과 1:1로 매핑([[010_schema_mapping|Mapping]])되어, 확실한 원본(고향)을 두고 있는 축복받은 메모리 공간**을 의미한다.
> 2. **가치**: 램이 꽉 차서 이 메모리를 쫓아내야(Eviction) 할 때, 내용이 바뀌지 않은(Clean) 코드 영역이라면 **느린 스왑(Swap) 디스크에 쓸 필요 없이 램에서 그냥 삭제해 버리는(Drop) O(1) [[148_5g_embb_urllc_mmtc|초고속]] 처리가 가능**하여 시스템의 램 회수 능력을 극대화한다.
> 3. **융합**: 운영체제의 [[501_file_definition_logical_record|파일]] 입출력 로직(`read/write`)을 가상 메모리의 [[259_paging|페이징]] 시스템으로 덮어씌워버린 **[[749_memory_mapped_file_mmap|mmap]]([[308_memory_mapped_file|Memory-Mapped File]])** 시스템 콜과 완벽히 융합되어, [[501_file_definition_logical_record|파일]]을 읽을 때 메모리 복사 오버헤드를 제로화하는 현대적 I/O 아키텍처를 완성했다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 물리 메모리([[286_page_frame|Page Frame]])에 적재된 [[001_dikw_pyramid|데이터]] 중, 디스크의 특정 [[501_file_definition_logical_record|파일]]블록(Block)과 논리적으로 연결된 메모리다. 실행 [[501_file_definition_logical_record|파일]](Text/[[082_process_memory_structure|Code]] 영역), 동적 링크 [[336_library_vs_framework|라이브러리]](DLL/SO [[501_file_definition_logical_record|파일]]), 그리고 프로그래머가 명시적으로 매핑한 일반 [[501_file_definition_logical_record|파일]]들이 이에 속한다.
- **필요성**: 램(RAM)은 비싸고 좁다. 램을 비우는 가장 좋은 방법은 [[001_dikw_pyramid|데이터]]를 지우는 것이다. 앞서 배운 [[391_anonymous_memory|익명 메모리]]([[078_heap_datastructure|Heap]]/[[057_stack|Stack]])는 원본이 없어서 지우기 전에 반드시 느려 터진 스왑(Swap) [[514_partition_slice_volume|파티션]]에 [[555_backup_and_restore_strategy|백업]](Write)을 해야만 했다(매우 느림). 하지만 카카오톡의 '실행 코드(기계어)' 부분은 어차피 하드디스크 `kakao.exe` 안에 똑같은 복사본이 영원히 존재한다. "어차피 고향(디스크 원본)에 똑같은 애가 있는데 뭐 하러 스왑에 힘들게 [[555_backup_and_restore_strategy|백업]]해? 그냥 램에서 시원하게 찢어버려!"라는 극한의 램 절약 및 최적화 철학이 이 개념을 낳았다.

- **등장 배경 및 I/O 철학의 진화**:
  1. **과거의 [[501_file_definition_logical_record|파일]] 읽기**: [[501_file_definition_logical_record|파일]]을 읽으려면 `read()`를 호출해 디스크에서 [[022_kernel_role|커널]]로, [[022_kernel_role|커널]]에서 유저 램으로 [[001_dikw_pyramid|데이터]]를 2번씩 복사(Memcpy)하는 생노가다를 뛰었다.
  2. **가상 메모리의 각성**: "어차피 [[259_paging|페이징]] 시스템이 디스크에서 램으로 4KB씩 기가 막히게 잘 퍼오는데, 굳이 [[501_file_definition_logical_record|파일]] I/O를 따로 만들 필요가 있나?"
  3. **mmap의 탄생**: [[501_file_definition_logical_record|파일]]의 주소를 냅다 프로세스의 가상 주소 공간에 꽂아버려([[010_schema_mapping|Mapping]]), 프로세스가 램 변수를 건드리듯 [[501_file_definition_logical_record|파일]]을 조작하면 하드웨어가 알아서 폴트([[387_page_fault|Page Fault]])를 터뜨려 [[501_file_definition_logical_record|파일]]을 로드하게 만드는 천재적 융합이 일어났다.

```text
┌────────────────────────────────────────────────────────────────────────┐
│        파일 지원 메모리 (File-backed)의 쿨(Cool)한 램 반환 구조        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│ [ 상황: 16GB RAM이 꽉 차서 OS가 메모리를 비우려 함 ]                   │
│                                                                        │
│ ▶ 1. 타겟 A: 익명 메모리 (힙/스택)                                     │
│   - OS: "이거 버리면 데이터 날아가니 스왑 파티션에 기록(Write)해라!"   │
│   - 징벌: 디스크 쓰기 속도 때문에 8 밀리초 이상 렉 발생 ☠️             │
│                                                                        │
│ ▶ 2. 타겟 B: 파일 지원 메모리 (읽기 전용 코드 / Clean)                 │
│   - OS: "이거 원본 파일에 그대로 있잖아? 그냥 램에서 1초 만에 지워!"   │
│   - 쾌감: 디스크 기록 0회! 0.0001초 만에 램 확보 완료 🚀               │
│                                                                        │
│ ▶ 3. 타겟 C: 파일 지원 메모리 (수정된 데이터 / Dirty)                  │
│   - OS: "원본에서 퍼왔는데 메모리에서 값을 바꿨네? 원본 파일에 덮어써!"│
│   - 결과: 백그라운드 데몬(pdflush)이 원본 파일(.txt)에 동기화함.       │
└────────────────────────────────────────────────────────────────────────┘
```
**[다이어그램 해설]** 이것이 리눅스가 램 부족([[157_oom_killer|OOM]]) 상황을 귀신같이 피하면서 버티는 진짜 이유다. 리눅스의 램에는 사실 내가 실행한 수많은 프로그램의 '실행 코드([[501_file_definition_logical_record|File]]-backed)'들이 [[286_page_frame|페이지]] 캐시([[286_page_frame|Page]] Cache) 형태로 가득 차 있다. 램이 모자라는 순간, OS는 이 코드들을 스왑 디스크에 쓰는 수고 없이 그냥 램 매핑만 툭툭 끊어버려 순식간에 수 기가바이트의 빈 램(Free Frame)을 창출해 낸다.

- **📢 섹션 요약 비유**: 마트(램)에서 진열대 자리가 모자랄 때, 유통기한이 없는 캔커피(Clean [[501_file_definition_logical_record|파일]] 메모리)는 굳이 창고에 다시 넣을 필요 없이 그냥 버려도 공장에서 다시 찍어냅니다. 하지만 손님이 주문해서 막 튀겨낸 치킨([[391_anonymous_memory|익명 메모리]])은 버리면 끝이니 무조건 보온 창고(스왑)에 넣고 살려야 하는 폐기 우선순위입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[749_memory_mapped_file_mmap|mmap]] ([[308_memory_mapped_file|Memory-Mapped File]])의 매핑 파이프라인

[[501_file_definition_logical_record|파일]] 지원 메모리의 꽃은 `mmap()` 시스템 콜이다. 10GB짜리 영화 [[501_file_definition_logical_record|파일]]을 램 16GB 컴퓨터에서 메모리로 다루는 방법이다.

1. **가상 주소 매핑 ([[010_schema_mapping|Mapping]])**: 
   프로그램이 `mmap("movie.mp4")`을 호출하면, OS는 램에 [[001_dikw_pyramid|데이터]]를 1바이트도 안 올리고, 텅 빈 가상 주소 10GB(예: `0x1000 ~ 0x3000`)에 이 [[501_file_definition_logical_record|파일]]을 논리적으로 연결만(PTE I비트) 해둔다.
2. **게으른 로딩 ([[182_lazy_loading|Lazy Loading]] & [[387_page_fault|Page Fault]])**:
   앱이 영화의 1시간째 장면(가상 주소 `0x2000`)을 터치한다.
   MMU가 `Invalid(I)` [[073_bit|비트]]를 밟고 [[677_trap_based_system_call_implementation|트랩]]([[387_page_fault|Page Fault]])을 던진다.
   OS는 `movie.mp4` [[501_file_definition_logical_record|파일]]의 하드디스크 중간 섹터로 날아가 딱 그 4KB 조각만 램으로 퍼 올린다.
3. **메모리 복사(Memcpy)의 멸망**:
   과거 `read()`는 "디스크 -> [[022_kernel_role|커널]] 램 -> 유저 램"으로 두 번 복사했다. `mmap`은 "디스크 -> [[022_kernel_role|커널]] 램([[286_page_frame|Page]] Cache)"으로 한 번만 퍼오고 유저 [[353_page_table|페이지 테이블]]을 여기에 직접 꽂아버린다([[566_mmap_zero_copy_sendfile|Zero-Copy]] 효율).

---

### Clean(깨끗한) [[286_page_frame|페이지]]와 Dirty(더러워진) [[286_page_frame|페이지]]

[[501_file_definition_logical_record|파일]] 지원 메모리가 램에서 쫓겨날 때의 운명을 가르는 가장 중요한 상태 [[073_bit|비트]]다. [[353_page_table|페이지 테이블]] 엔트리(PTE) 안에 있는 **M (Modify) [[073_bit|비트]] / Dirty [[073_bit|비트]]**가 이를 판별한다.

- **Clean [[286_page_frame|Page]] (수정 안 됨)**: 디스크에서 퍼온 원본과 램의 [[001_dikw_pyramid|데이터]]가 100% 똑같은 상태. (주로 실행 코드). 쫓아낼 때 그냥 **삭제(Discard)** 하면 끝이다. I/O 오버헤드 0.
- **Dirty [[286_page_frame|Page]] (수정됨)**: 램으로 퍼온 뒤 CPU가 값을 바꿨다. (예: 워드에서 글씨를 침). 디스크 원본 [[501_file_definition_logical_record|파일]]과 내용이 달라진 상태. 쫓아낼 때 반드시 디스크 원본 [[501_file_definition_logical_record|파일]]에 **[[212_synchronization_mechanisms|동기화]] 기록([[277_write_back|Write-back]])**을 한 뒤 지워야 한다. I/O 오버헤드가 크다.

- **📢 섹션 요약 비유**: 도서관에서 책을 빌려와서 눈으로만 읽은 책(Clean)은 반납할 때 그냥 던져놓고 가도 되지만, 책에 연필로 밑줄을 찍찍 그어놓은 책(Dirty)은 사서가 지우개로 다 지우는 수고([[277_write_back|Write-back]])를 거쳐야만 책장에 꽂을 수 있는 페널티 원리입니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: [[391_anonymous_memory|익명 메모리]](Anonymous) vs [[501_file_definition_logical_record|파일]] 메모리([[501_file_definition_logical_record|File]]-backed) 최종 정리

| 비교 척도 | [[391_anonymous_memory|익명 메모리]] ([[391_anonymous_memory|Anonymous Memory]]) | [[501_file_definition_logical_record|파일]] 지원 메모리 ([[501_file_definition_logical_record|File]]-backed Memory) |
|:---|:---|:---|
| **소속 영역** | [[057_stack|스택]]([[057_stack|Stack]]), 힙([[078_heap_datastructure|Heap]], malloc) | 코드([[082_process_memory_structure|Code]]), [[333_shared_library|공유 라이브러리]](.so/.dll), [[749_memory_mapped_file_mmap|mmap]] |
| **디스크 고향** | 고향 없음 (램에서 허공에 태어남) | 하드디스크의 뚜렷한 원본 [[501_file_definition_logical_record|파일]] (`.exe`, `.txt`) |
| **[[336_swap_out_in|스왑 아웃]] 시**| **무조건 스왑 [[514_partition_slice_volume|파티션]]**에 눈물겹게 묻힘 | **스왑 안 감.** (Clean은 삭제, Dirty는 원본 [[501_file_definition_logical_record|파일]]에 씀) |
| **[[459_quic_fec_forward_error_correction|초기]]화 과정** | 해킹 방지 위해 0으로 덮음 (ZFOD) | 디스크 원본을 읽어와서 채움 |
| **공유 (Sharing)**| 프로세스 간 공유 까다로움 | **100명이 똑같은 프레임을 공유하기 최적화됨** |

### 시스템 [[257_thrashing|스래싱]] 방어의 최전선: [[286_page_frame|Page]] Cache

윈도우 작업 관리자나 리눅스의 `free -m` 명령어를 치면 램 사용량이 99%로 뜰 때가 있다.
놀랍게도 이건 램이 꽉 찬 게 아니다. **OS가 남는 램을 모조리 긁어모아 '[[501_file_definition_logical_record|파일]] 지원 메모리([[286_page_frame|Page]] Cache)'로 써먹고 있는 훈장**이다.
- 리눅스는 램이 10GB 비어있으면, 한 번 읽었던 [[501_file_definition_logical_record|파일]]들([[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]], DB [[501_file_definition_logical_record|파일]] 등)을 램에서 지우지 않고 가득 채워둔다. 나중에 또 찾을 때 0.1초 만에 주려고.
- 그러다 카톡이 "램 2GB 줘!"라고 요청하면? [[022_kernel_role|커널]]은 0.001초의 망설임도 없이 꽉 찬 [[501_file_definition_logical_record|파일]] 캐시 중 Clean 한 놈들을 2GB치 찢어버리고 카톡에게 던져준다.
- 즉, **[[501_file_definition_logical_record|파일]] 지원 메모리는 OS의 가장 거대하고 유연한 완충 지대(Shock Absorber)**로서, 시스템의 체감 속도를 [[465_hdd_structure|HDD]] 속도에서 RAM 속도로 끌어올려 주는 기적의 캐시다.

```text
┌──────────┬────────────┬────────────┬───────────────────────┐
│ 램 부족 시 │ Clean 파일 │ Dirty 파일 │ 익명(스택/힙)       │
├──────────┼────────────┼────────────┼───────────────────────┤
│ OS의 조치  │ 1순위 사살   │ 2순위 디스크 씀│ 3순위 스왑 씀 │
│ 지연 시간  │ 🚀 로켓 속도 │ 🐢 느려짐    │ ☠️ 지옥의 렉    │
└──────────┴────────────┴────────────┴───────────────────────┘
```
**[매트릭스 해설]** 리눅스의 메모리 회수(Reclaim) 정책의 뼈대다. 가장 싸고 버리기 쉬운 [[501_file_definition_logical_record|파일]] 캐시(Clean)부터 죽여서 램을 확보한다. 만약 Clean 캐시가 다 말라서 [[391_anonymous_memory|익명 메모리]]를 스왑으로 밀어내야 하는 순간이 오면, 그때부터 시스템은 멈추기([[257_thrashing|Thrashing]]) 시작한다.

- **📢 섹션 요약 비유**: 통장(램)에 돈이 꽉 차 있을 때, 위기가 닥치면 당장 쓸데없는 취미생활(Clean [[501_file_definition_logical_record|파일]]) 예산부터 1초 만에 확 깎아버립니다. 그다음엔 적금(Dirty [[501_file_definition_logical_record|파일]])을 깨야 하고, 최악의 경우엔 집([[391_anonymous_memory|익명 메모리]] 스왑)까지 팔아야 하는 자산 관리의 우선순위입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: [[179_kafka_flink_watermark_time_window|Kafka]]/Elasticsearch의 [[566_mmap_zero_copy_sendfile|Zero-Copy]] 마술
1. **상황**: 대용량 메시지 큐인 Kafka는 초당 기가바이트 단위의 [[001_dikw_pyramid|데이터]]를 디스크에서 읽어 네트워크 랜카드([[587_nic_offloading|NIC]])로 쏘아 보낸다.
2. **과거의 병목 (`read` & `send`)**:
   - 디스크 -> [[022_kernel_role|커널]] 공간 -> 유저 힙 공간(익명) 복사 -> [[022_kernel_role|커널]] [[125_socket|소켓]] 버퍼 복사 -> 랜카드 
   - 메모리 복사가 4번, [[033_context|컨텍스트]] 스위칭이 4번 일어나며 CPU가 터져버린다.
3. **mmap과 sendfile의 융합 ([[566_mmap_zero_copy_sendfile|Zero-Copy]])**:
   - Kafka는 [[501_file_definition_logical_record|파일]] [[001_dikw_pyramid|데이터]] 1GB를 **`mmap` ([[501_file_definition_logical_record|파일]] 지원 메모리)**으로 램에 딱 1번 올린다([[286_page_frame|Page]] Cache).
   - 유저 공간으로 복사하지도 않는다. [[022_kernel_role|커널]]에게 `sendfile()` 명령을 때리면, [[022_kernel_role|커널]] 공간에 떠 있는 그 [[501_file_definition_logical_record|파일]] 지원 메모리 조각의 '포인터'만 네트워크 카드([[746_io_direct_memory_access_dma|DMA]])로 넘겨버린다.
   - **결과**: 메모리 복사 횟수 0회([[566_mmap_zero_copy_sendfile|Zero-Copy]]). CPU 사용률은 바닥을 기면서 네트워크 [[140_bandwidth|대역폭]] 한계까지 [[001_dikw_pyramid|데이터]]를 쏴주는 현존 최고 효율의 서버 아키텍처가 완성된다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]: DB의 [[749_memory_mapped_file_mmap|mmap]] 오남용과 MongoDB의 뼈저린 [[659_ir_lessons_learned|교훈]]
[[540_mongodb|MongoDB]] [[459_quic_fec_forward_error_correction|초기]] 버전은 자체적인 메모리 관리를 포기하고 100GB짜리 DB [[501_file_definition_logical_record|파일]]을 몽땅 OS의 `mmap` ([[501_file_definition_logical_record|파일]] 지원 메모리)에 엎어쳐서 구동했다. "OS가 알아서 캐싱하고 디스크에 써주겠지!"라는 나이브한 발상이었다.
결과는 대참사였다. 수만 개의 쿼리가 Dirty Page를 만들어내자, OS 백그라운드 [[212_synchronization_mechanisms|동기화]] 데몬(pdflush)이 통제를 잃고 디스크 I/O를 터뜨려 서버 전체가 마비(I/O 스톨)되었다. 결국 MongoDB는 [[749_memory_mapped_file_mmap|mmap]] 꼼수를 버리고 WiredTiger라는 정교한 자체 스토리지 엔진(자체 [[369_memory_pool|메모리 풀]] 관리)을 도입하여 살아났다. [[501_file_definition_logical_record|파일]] 지원 메모리는 만능이 아니며, [[502_dbms|DBMS]] 같은 초정밀 제어 시스템에서는 맹신하면 독이 된다.

- **📢 섹션 요약 비유**: 택배 배달([[001_dikw_pyramid|데이터]] 전송)을 할 때, 창고(디스크)에서 물건을 빼서 배달원 트럭(유저 앱)에 싣고 다시 고객 차(네트워크)로 옮겨 싣는 게 아니라, 아예 창고 컨베이어 벨트를 고객 차 트렁크([[566_mmap_zero_copy_sendfile|Zero-copy]])에 직빵으로 연결해 버리는 물류 혁신입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 내용 |
|:---|:---|
| **[[566_mmap_zero_copy_sendfile|Zero-Copy]] 통신 지원** | 유저 모드 메모리 복사본(익명)을 만들지 않고 [[022_kernel_role|커널]] [[286_page_frame|페이지]] 캐시([[501_file_definition_logical_record|파일]] 메모리)를 하드웨어(랜카드)로 직통 매핑해 시스템 [[140_bandwidth|대역폭]] 100% 활용 |
| **코드 공유(Sharing) 극대화**| 수백 개의 크롬 탭이 `chrome.dll` [[501_file_definition_logical_record|파일]]을 요구해도, 물리 램에는 딱 1장만 올려놓고 공유하여 램 낭비 원천 차단 |
| **[[157_oom_killer|OOM]](메모리 부족) [[015_지연_데이터_관점|지연]] 방어**| 램 회수 시 스왑(Swap) [[514_partition_slice_volume|파티션]]에 [[289_cqrs_db|쓰기]](Write)를 해야 하는 최악의 오버헤드를 건너뛰고 0초 만에 램 확보(Clean Drop)를 달성 |

### 결론 및 미래 전망

[[501_file_definition_logical_record|파일]] 지원 메모리 ([[501_file_definition_logical_record|File]]-backed Memory)는 "왜 [[501_file_definition_logical_record|파일]] I/O와 메모리 관리는 떨어져 있어야 하는가?"라는 고전적 질문에 대해 "[[501_file_definition_logical_record|파일]]이 곧 메모리고 메모리가 곧 [[501_file_definition_logical_record|파일]]이다"라고 선언하며 [[259_paging|페이징]]과 [[501_file_definition_logical_record|파일]] 시스템을 우아하게 융합한 천재적인 아키텍처다. 스왑(Swap)이라는 지저분한 창고에 의존하는 [[391_anonymous_memory|익명 메모리]]와 달리, 뚜렷한 고향(원본 [[501_file_definition_logical_record|파일]])을 가진 이 메모리는 리눅스 서버 성능을 떠받치는 가장 거대하고 튼튼한 캐시([[286_page_frame|Page]] Cache) 생태계를 형성했다. 향후 PMEM(영구 메모리)이나 NVMe가 더욱 진화하여 [[501_file_definition_logical_record|파일]]과 램의 접근 속도 차이가 완전히 소멸하는 시대가 오면, 모든 램 구조는 [[391_anonymous_memory|익명 메모리]]의 허물을 벗고 이 1:1 매핑 기반의 '영구 [[501_file_definition_logical_record|파일]] 지원 메모리' 아키텍처로 흡수 통합되어 부팅이라는 개념 자체가 사라지는 차세대 컴퓨팅 혁명을 이끌 것이다.

- **📢 섹션 요약 비유**: 컴퓨터의 모든 [[001_dikw_pyramid|데이터]]를 "어디서 왔는지 족보도 없는 떠돌이([[391_anonymous_memory|익명 메모리]])"와 "돌아갈 고향 집이 있는 명문가 자제([[501_file_definition_logical_record|파일]] 지원 메모리)"로 나누어, 전쟁(램 부족)이 났을 때 돌아갈 집이 있는 애들은 가볍게 고향으로 돌려보내 희생을 줄이는 완벽한 계급적 최적화 전략입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[390_swap_space|스왑 공간]] ([[390_swap_space|Swap Space]]) / 베이킹 스토어 (Backing Store) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[391_anonymous_memory|익명 메모리]] ([[391_anonymous_memory|Anonymous Memory]]) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[393_copy_on_write|쓰기 시 복사]] ([[542_cow_file_system|COW]], [[542_cow_file_system|Copy-on-Write]]) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[394_vfork|vfork]]() | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[익명 메모리 (Anonymous Memory)]
    │
    ▼
[파일 지원 메모리 (File-backed Memory)]
    │
    ├──▶ [쓰기 시 복사 (COW, Copy-on-Write)]
    └──▶ [vfork()]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[501_file_definition_logical_record|파일]] 지원 메모리 ([[501_file_definition_logical_record|File]]-backed Memory)은 컴퓨터가 메모리를 더 크게 보이게 하고 부족함을 숨기는 방법이에요.
2. 먼저 [[391_anonymous_memory|익명 메모리]] ([[391_anonymous_memory|Anonymous Memory]])을 이해하면 [[501_file_definition_logical_record|파일]] 지원 메모리 ([[501_file_definition_logical_record|File]]-backed Memory)이 왜 필요한지 더 쉽게 보여요.
3. 그래서 [[501_file_definition_logical_record|파일]] 지원 메모리 ([[501_file_definition_logical_record|File]]-backed Memory)을 잘 알면 나중에 [[393_copy_on_write|쓰기 시 복사]] ([[542_cow_file_system|COW]], [[542_cow_file_system|Copy-on-Write]])도 훨씬 쉽게 배울 수 있어요.
