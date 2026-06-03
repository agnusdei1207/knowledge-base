+++
title = "733. 파일 시스템 연속, 연결, 색인 할당 (File System Allocation Contiguous Linked Indexed)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 디스크에 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 저장할 때, 수많은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록들을 어떤 방식으로 흩뿌리고 이어 붙일 것인가를 결정하는 물리적 <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 할당(<a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">File</a> Allocation) 기법</strong>의 3대장이다.
> 2. **3가지 방법**: 디스크에 순서대로 쫙 붙여서 저장하는 <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/523_contiguous_allocation/">연속 할당</a>(Contiguous)</strong>, 블록들을 기차처럼 포인터로 꼬리에 꼬리를 물게 만든 <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/524_linked_allocation/">연결 할당</a>(Linked)</strong>, 그리고 목차(색인 블록) 하나를 두고 모든 블록의 위치를 적어두는 <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/">색인 할당</a>(<a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/181_indexed_addressing/">Indexed</a>)</strong> 방식이 있다.
> 3. **가치**: 연속은 속도가 빠르지만 [단편화](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)(구멍)로 멸망했고, 연결은 [단편화](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)는 잡았지만 탐색 속도가 너무 느렸으며, [색인 할당](/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/)은 이 둘의 장점을 섞어 <strong>현대 UNIX/리눅스 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템(i-node)의 뼈대</strong>가 되었다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 할당 (<a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">File</a> Allocation)</strong>: 하드디스크의 텅 빈 공간(Blocks)들에 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 어떻게 분배하고, 나중에 그 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)들을 다시 찾기 위해 [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)에 어떻게 기록해 둘 것인지 결정하는 방법.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/523_contiguous_allocation/">연속 할당</a> (<a href="/knowledge-base/studynote/02_operating_system/09_file_system/523_contiguous_allocation/">Contiguous Allocation</a>)</strong>: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 디스크의 물리적으로 연속된 빈 블록에 저장함.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/524_linked_allocation/">연결 할당</a> (<a href="/knowledge-base/studynote/02_operating_system/09_file_system/524_linked_allocation/">Linked Allocation</a>)</strong>: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 디스크 아무 데나 흩뿌리고, 각 블록의 끝에 '다음 블록의 주소(포인터)'를 적어 이어줌.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/">색인 할당</a> (<a href="/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/">Indexed Allocation</a>)</strong>: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 흩뿌려 두되, '[인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 블록(목차)' 하나를 따로 만들어서 흩어진 블록들의 주소를 한 곳에 싹 모아둠.

- **필요성 (디스크 공간과 탐색 속도의 트레이드오프)**: 
  - [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 연속해서 저장하면 디스크 헤드가 한 번만 징~ 움직이면 되니까 속도가 엄청 빠르다. 하지만 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 지웠다 썼다 하면 중간중간 빈 공간([외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/))이 생겨서, 나중엔 큰 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 저장할 수 없게 된다.
  - 빈 공간을 없애려고 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 찢어서 아무 데나 막 저장하면([연결 할당](/knowledge-base/studynote/02_operating_system/09_file_system/524_linked_allocation/)), 10번째 블록을 찾기 위해 헤드가 디스크 전체를 10번이나 이리저리 뛰어야 하는 탐색(Seek) 지옥이 열린다.
  - **해결책**: "빈 공간도 알뜰하게 쓰면서(비연속), 10번째 블록도 한 번에 훅 찾아갈 수 있는(직접 접근)" 중간 타협점([색인 할당](/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/))이 필요했다.

  - <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/523_contiguous_allocation/">연속 할당</a></strong>: 영화관에서 친구 5명이 무조건 <strong>'연속된 5자리'</strong>에만 앉는 것. 한 번에 찾기 쉽지만, 남은 자리가 띄엄띄엄 있으면 영화를 못 본다.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/524_linked_allocation/">연결 할당</a></strong>: 친구 5명이 극장 아무 데나 흩어져 앉는다. 대신 1번 친구에게 "2번 친구 어디 앉았어?" 묻고, 2번 친구에게 가서 "3번 어딨어?" 묻는 방식. 자리가 남기만 하면 무조건 앉을 수 있지만, 5번 친구를 찾으려면 1, 2, 3, 4번을 다 거쳐야 한다 (속도 최악).
  - <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/">색인 할당</a></strong>: 친구들은 아무 데나 앉되, 매표소 직원([인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 블록)이 <strong>'5명의 좌석 번호가 모두 적힌 장부'</strong>를 들고 있다. 5번 친구를 찾으려면 직원에게 장부만 보면 0.1초 만에 바로 찾아갈 수 있다.

- **발전 과정**:
  1. <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/523_contiguous_allocation/">연속 할당</a></strong>: 마그네틱 테이프 시절이나 읽기 전용 CD-ROM에서 주로 쓰임.
  2. <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/524_linked_allocation/">연결 할당</a></strong>: MS-DOS의 [FAT](/knowledge-base/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/)([File Allocation Table](/knowledge-base/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/)) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템으로 발전.
  3. <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/">색인 할당</a></strong>: 현대 UNIX의 ext4 (i-node 구조), Windows NTFS 등 거의 모든 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 스토리지의 표준.

- **📢 섹션 요약 비유**: 짐([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))을 창고(디스크)에 넣는 3가지 방식입니다. 하나로 묶어서 큰 통에 넣거나(연속), 짐들을 밧줄로 길게 묶어서 흩어놓거나(연결), 짐을 흩어놓고 보물지도(색인)를 그리는 것입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 3가지 할당 방식의 구조와 [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 구성

[디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)(폴더)가 각 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 정보를 어떻게 기록하는지가 핵심이다.

<strong>1. <a href="/knowledge-base/studynote/02_operating_system/09_file_system/523_contiguous_allocation/">연속 할당</a> (<a href="/knowledge-base/studynote/02_operating_system/09_file_system/523_contiguous_allocation/">Contiguous Allocation</a>)</strong>
- <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/">디렉터리</a> 기록</strong>: `[파일 이름] | [시작 블록 번호] | [파일 길이(블록 수)]`
- **동작**: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) `A`가 `시작: 10`, `길이: 3`이면 무조건 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/), [11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/), 12번 블록에 저장됨.
- **장점**: 순차 접근과 직접 접근(Random Access, 예: $[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) + i$) 모두 광속이다. 헤드 이동이 거의 없다.
- **단점**: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 키울 수 없다([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 뒤에 남이 자리 잡고 있으면 꼼짝 못 함). [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)가 극심하다.

<strong>2. <a href="/knowledge-base/studynote/02_operating_system/09_file_system/524_linked_allocation/">연결 할당</a> (<a href="/knowledge-base/studynote/02_operating_system/09_file_system/524_linked_allocation/">Linked Allocation</a>)</strong>
- <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/">디렉터리</a> 기록</strong>: `[파일 이름] | [시작 블록 번호] | [끝 블록 번호]`
- **동작**: `시작: 9`. 9번 블록으로 가면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 함께 "다음은 16번 블록"이라는 포인터가 있음. 16번으로 가면 "다음은 1번"... 이렇게 꼬리를 묾.
- **장점**: [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) 0%. 디스크가 꽉 찰 때까지 무조건 저장 가능. [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 크기를 마음대로 늘릴 수 있음.
- **단점**: 직접 접근 불가(100번째 블록을 보려면 1번부터 99번까지 다 읽어야 함). 포인터를 저장할 4바이트 때문에 블록 크기(512바이트)가 508바이트로 줄어들어 2의 승수 연산이 깨짐. 포인터 하나 끊어지면 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 뒷부분이 통째로 날아감.

<strong>3. <a href="/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/">색인 할당</a> (<a href="/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/">Indexed Allocation</a>)</strong>
- <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/">디렉터리</a> 기록</strong>: `[파일 이름] | [인덱스 블록 번호]`
- **동작**: [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 블록 `19`를 가리킴. 19번 블록을 열어보니 `[9, 16, 1, 10, 25]` 라고 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록 주소가 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)처럼 쫙 적혀있음.
- **장점**: 흩어져 있어도 [단편화](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)가 없고, [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 덕분에 `i`번째 블록을 한 번에 찾아가는 직접 접근($O(1)$)이 가능함.
- **단점**: 1바이트짜리 작은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 저장해도, [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 블록 1개와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록 1개, 총 2개의 블록을 무조건 써야 하는 공간 낭비(Overhead)가 발생함.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 할당 방식별 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 접근 속도(I/O [Performance](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)) 비교

| 할당 방식 | 순차 접근 (Sequential) | 직접 접근 (Random/[Direct](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/)) | 헤드 탐색(Seek) 페널티 |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/523_contiguous_allocation/">연속 할당</a></strong> | 매우 빠름 | **매우 빠름 ($O(1)$)** | 거의 없음 (연속해서 읽음) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/524_linked_allocation/">연결 할당</a></strong> | 보통 (포인터 따라감) | **매우 느림 ($O(N)$)** | 극심함 (디스크 이리저리 뜀) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/">색인 할당</a></strong> | 빠름 | **빠름 ($O(1)$)** | 보통 ([인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 먼저 읽어야 함) |

### 과목 융합 관점

- <strong>자료구조 (<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Structure)</strong>: 디스크 할당 방식은 램(RAM)의 자료구조와 완벽한 평행이론을 이룬다. 
  - [연속 할당](/knowledge-base/studynote/02_operating_system/09_file_system/523_contiguous_allocation/) = <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/">배열</a> (<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/">Array</a>)</strong>
  - [연결 할당](/knowledge-base/studynote/02_operating_system/09_file_system/524_linked_allocation/) = <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/">연결 리스트</a> (<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/">Linked List</a>)</strong>
  - [색인 할당](/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/) = <strong><a href="/knowledge-base/studynote/05_database/07_exam_summary/423_non_clustered_index/">포인터 배열</a> (<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/">Array</a> of Pointers)</strong>
- <strong>컴퓨터구조 (<a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/">CA</a>)</strong>: 디스크 암(Arm)의 움직임은 엄청나게 비싸다(ms 단위). [색인 할당](/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/)에서 최악의 시나리오는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 블록을 읽기 위해 헤드가 1번 움직이고, 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록을 읽기 위해 헤드가 2번 움직이는 <strong>Double I/O 병목</strong>이다. 이를 막기 위해 현대 OS는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 블록(inode)을 램(RAM)의 캐시에 통째로 올려두고([VFS](/knowledge-base/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) inode cache) 디스크 헤드를 움직이지 않게 방어한다.

- **📢 섹션 요약 비유**: [연속 할당](/knowledge-base/studynote/02_operating_system/09_file_system/523_contiguous_allocation/)은 백과사전 1,2,3권을 나란히 꽂는 것([배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)), [연결 할당](/knowledge-base/studynote/02_operating_system/09_file_system/524_linked_allocation/)은 1권 끝에 '다음 권은 2층 서재에 있음' 쪽지를 남기는 것(링크드 리스트), [색인 할당](/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/)은 도서관 검색대 PC에 1,2,3권의 위치를 전부 저장해 두는 것([포인터 배열](/knowledge-base/studynote/05_database/07_exam_summary/423_non_clustered_index/))입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — 동영상 편집 서버의 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템 설계 (<a href="/knowledge-base/studynote/02_operating_system/09_file_system/523_contiguous_allocation/">연속 할당</a>의 부활)</strong>: 유튜브 같은 동영상 처리 서버에서는 10GB짜리 영상을 처음부터 끝까지 순차적으로 쫙 읽어 들이는 작업(Sequential Read)이 핵심이다.
   - **아키텍처 판단**: 여기서 [색인 할당](/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/)(ext4)을 써서 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 1만 개의 조각으로 찢어지면, 헤드가 1만 번 튀어 영상이 미친 듯이 버벅거린다.
   - <strong>대응 (<a href="/knowledge-base/studynote/02_operating_system/09_file_system/531_extent_allocation/">Extent Allocation</a>)</strong>: 최신 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템(XFS, btrfs, ext4의 [Extent](/knowledge-base/studynote/02_operating_system/09_file_system/531_extent_allocation/))은 [색인 할당](/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/)의 유연성에 <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/523_contiguous_allocation/">연속 할당</a>의 속도</strong>를 합쳤다. [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 4KB 단위로 조각내지 않고, 아예 "10번부터 1,000번까지 연속으로 990개!"라는 식의 <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/531_extent_allocation/">Extent</a>(거대한 연속 덩어리)</strong> 단위로 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 묶어버린다. 동영상 서버에 특화된 극강의 순차 읽기 성능을 발휘한다.

2. <strong>시나리오 — 1바이트짜리 <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 수백만 개와 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/">색인 할당</a>의 저주 (No space left on device)</strong>: 개발자가 서버에 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 남기는데, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 1개당 "OK" (2바이트)만 적어서 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 100만 개를 생성했다. 디스크 용량은 1TB 중 1GB밖에 안 썼는데, 갑자기 "No space left on device" 에러가 뜨며 서버가 뻗었다.
   - **원인 분석**: 전형적인 [색인 할당](/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/)(i-node)의 함정이다. [색인 할당](/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/)은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 1개를 만들 때 무조건 '목차([인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 블록)'를 1개 만들어야 한다. 리눅스 ext4는 포맷할 때 이 목차 장부(i-node table)의 개수를 미리 정해놓는다(예: 100만 개).
   - 1TB 용량은 남았지만, <strong>100만 개의 <a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a> 장부가 꽉 차버려서(inode exhaustion) 더 이상 새 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>을 만들 수 없게 된 것</strong>이다. 
   - **대응 (기술사적 가이드)**: 자잘한 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 많이 다루는 서버(메일 서버, 이미지 썸네일 서버)는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 포맷(`mkfs`) 시 `-i` 옵션을 주어 **inode 덴시티(밀도)를 높이거나(목차를 많이 만들거나)**, 자잘한 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 지원하는 XFS 같이 inode를 동적 할당하는 최신 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템으로 인프라를 변경해야 한다.

### 의사결정 및 튜닝 플로우



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">워크로드 특성에 따른 파일 할당(File System) 아키텍처</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">새로운 스토리지 서버(SAN/NAS) 포맷 시 파일 시스템 아키텍처 선택</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">주로 저장되는 파일이 '작고(Small)' 개수가 '무수히 많은가(Millions)'?</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">인덱스(i-node) 최적화 FS 필수</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(ReiserFS, XFS 등 inode 동적 할당 FS 적용 또는</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ext4 포맷 시 inode ratio 극대화 튜닝)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 아니오 (기가바이트 단위의 거대한 파일이 주를 이룬다)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">거대 파일들을 '임의 접근(Random Access)'으로 자주 뒤섞어서 읽는가?</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(예: RDBMS 데이터 파일, 가상머신 이미지)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">색인 할당(Indexed) + B-Tree 구조 적용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(ZFS, Btrfs 같은 고성능 B-Tree 인덱스 파일 시스템)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 아니오 ──▶ (순차 접근 위주의 동영상, 백업 파일)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">연속 할당(Extent)이 지원되는 ext4 / XFS 사용</div></div>
</div>
</div>



**[다이어그램 해설]** "그냥 리눅스 깔 때 기본인 ext4 쓰면 되는 거 아니야?"라는 마인드는 레거시 환경에서만 통한다. 1초에 수만 개의 이미지 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 저장하는 서버에 [색인 할당](/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/)의 오버헤드를 그대로 맞으면 디스크 IOPS가 터진다. 아키텍트는 저장될 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 **크기, 개수, 접근 패턴(순차 vs 랜덤)** 3가지를 분석해 디스크 할당 철학을 디자인해야 한다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong>거대 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>의 <a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a> 한계 (<a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/">Indirect</a> Block)</strong>: [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 블록(목차) 1개가 4KB라면, 그 안에 담을 수 있는 주소는 기껏해야 1,000개(4MB 분량)다. 만약 10GB짜리 영화를 넣으려면? [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 블록이 또 다른 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 블록을 가리키게 만드는 <strong>다중 간접 할당(Multi-level <a href="/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/">Indexed Allocation</a>)</strong> 구조로 성능이 심하게 저하(I/O 깊이 증가)됨을 인지하고, 이를 [Extent](/knowledge-base/studynote/02_operating_system/09_file_system/531_extent_allocation/) 기법으로 상쇄시킬 수 있는지 체크했는가?

- **📢 섹션 요약 비유**: 1바이트짜리 메모를 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 위해 매번 양장본 가죽 다이어리([인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 블록)를 하나씩 사서 쓰는 것은 낭비(inode 고갈)입니다. 내가 쓰는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 일기장(작은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 다수)인지, 백과사전(거대 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))인지에 따라 노트의 제본 방식(할당 방식)을 다르게 골라야 합니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [연속 할당](/knowledge-base/studynote/02_operating_system/09_file_system/523_contiguous_allocation/) (Contiguous) | [연결 할당](/knowledge-base/studynote/02_operating_system/09_file_system/524_linked_allocation/) (Linked) | [색인 할당](/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/) ([Indexed](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/181_indexed_addressing/)) |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/">외부 단편화</a></strong> | 심각함 ([OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 주범) | **없음 (100% 활용)** | **없음** |
| <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 크기 변경</strong>| 거의 불가능 | **무한정 확장 가능** | 무한정 확장 가능 |
| **직접 접근(Random)**| $O(1)$ (빛의 속도) | $O(N)$ (치명적으로 느림)| **$O(1)$ (매우 빠름)** |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a> 낭비</strong>| 0% (없음) | 약간 (포인터 4바이트) | 조금 심함 ([인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 블록 통째로 낭비) |

### 미래 전망
- <strong>객체 스토리지(<a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/">Object Storage</a>)로의 진화</strong>: 블록 단위로 쪼개고 목차를 그리는 복잡한 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 시대는 지나가고 있다. AWS S3 같은 클라우드는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 블록으로 쪼개지 않고 통째로(Object) 던진 뒤, 고유한 해시 ID 값(URL)으로 [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 매핑해 버리는 플랫(Flat)한 아키텍처를 사용하여 디스크 할당 오버헤드를 아예 네트워크 레이어로 숨겨버렸다.

### 결론
[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 연속, 연결, [색인 할당](/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/)은 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 디스크라는 물리적 원판에 어떻게 아름답게 펼쳐 놓을 것인가?"에 대한 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 50년 고민이 담긴 발자취다. 속도를 위해 연속을 택했다가 파편화의 저주를 맞았고, 파편화를 잡으려 연결을 택했다가 끔찍한 탐색 속도에 좌절했다. 결국 인간은 '목차([Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/))'라는 가장 오래된 정보 검색의 진리를 디스크에 이식([색인 할당](/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/))함으로써 두 마리 토끼를 모두 잡았다. 현대의 어떤 화려한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템도 결국 이 '색인([Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/))'이라는 완벽한 타협점 위에서 뼈대를 세우고 있다.

- **📢 섹션 요약 비유**: 무식하게 줄을 세우는 것(연속)과 무책임하게 흩어놓는 것(연결)의 양극단을 피하고, 자유롭게 흩어놓되 그 모든 위치를 꿰뚫어 보는 지휘통제실(색인)을 둔 것이 현대 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이 혼돈(디스크) 속에서 질서를 유지하는 유일한 비결입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [SSD FTL](/knowledge-base/studynote/02_operating_system/11_exam_summary/731_ssd_ftl_flash_translation_layer/) ([Flash Translation Layer](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [가비지 컬렉션](/knowledge-base/studynote/02_operating_system/06_memory_management/380_garbage_collection/) 블록 지우기 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [FAT](/knowledge-base/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/) 방식 [연결 할당](/knowledge-base/studynote/02_operating_system/09_file_system/524_linked_allocation/) 최적화 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| i-node 직접/간접 포인터 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">가비지 컬렉션 블록 지우기</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">파일 시스템 연속, 연결, 색인 할당 (File System Allocation Contiguous Linked Indexed)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">FAT 방식 연결 할당 최적화</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">i-node 직접/간접 포인터 인덱스</div></div>
</div>
</div>



이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 일기장을 쓸 때, 1페이지부터 10페이지까지 <strong>쭉 이어서(<a href="/knowledge-base/studynote/02_operating_system/09_file_system/523_contiguous_allocation/">연속 할당</a>)</strong> 쓰면 읽기 편하지만, 중간에 내용을 추가하고 싶을 땐 자리가 없어서 지우고 다시 써야 해요.
2. 그래서 오늘 1페이지 쓰고, 내일은 50페이지에 쓰면서 "다음 일기는 50페이지에 있음!"이라고 <strong>꼬리표(<a href="/knowledge-base/studynote/02_operating_system/09_file_system/524_linked_allocation/">연결 할당</a>)</strong>를 달았어요. 자리는 안 모자라지만, 5번째 일기를 찾으려면 1페이지부터 꼬리표를 계속 따라가야 해서 너무 힘들어요.
3. 아하! 그래서 공책 맨 앞장에 <strong>'목차(<a href="/knowledge-base/studynote/02_operating_system/09_file_system/526_indexed_allocation/">색인 할당</a>)'</strong>를 만들었어요. 목차에 "1일차: 1p, 2일차: 50p, 5일차: 30p"라고 다 적어두니까, 일기를 아무 데나 써도 목차만 보면 한 번에 찾을 수 있게 되었답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 733 / 800

← **이전**: [732. 가비지 컬렉션 블록 지우기 (Garbage Collection Block Erase)](/knowledge-base/studynote/02_operating_system/11_exam_summary/732_garbage_collection_block_erase/)
**다음**: [734. FAT 방식 연결 할당 최적화 (Fat File Allocation Table Optimization)](/knowledge-base/studynote/02_operating_system/11_exam_summary/734_fat_file_allocation_table_optimization/) →

---
