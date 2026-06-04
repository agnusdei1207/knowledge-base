+++
title = "782. LFS (Log-structured File System) 랜덤 쓰기 순차화"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 구조 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 ([LFS](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/), [Log-structured File System](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/))은 디스크 여기저기에 파편화되어 흩어지는 무작위 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(Random Write) 요청들을 메모리에 큼직하게 모아두었다가, <strong>디스크의 빈 공간을 향해 거대한 통나무(Log)처럼 한 번에 순차적으로(Sequential) 내리꽂는 <a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 특화 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템</strong>이다.
> 2. **가치**: 회전하는 하드 디스크([HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/))의 가장 큰 적이자 속도 저하의 주범인 물리적 헤드 이동 시간([Seek Time](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/))을 99% 없애주어, <strong>수만 개의 흩어진 자잘한 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> <a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>을 메모리 <a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 속도에 필적할 만큼 극단적으로 뻥튀기</strong>시킨다.
> 3. **융합**: 비록 [가비지 컬렉션](/knowledge-base/studynote/02_operating_system/06_memory_management/380_garbage_collection/)(청소)의 극악한 오버헤드 때문에 범용 OS [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 왕좌에는 오르지 못했지만, 덮어쓰기가 불가능한 <strong><a href="/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/">플래시 메모리</a>(<a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/">SSD</a>)의 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/">FTL</a> 컨트롤러 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/">펌웨어</a></strong>와 키-밸류 [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/)([LSM-Tree](/knowledge-base/studynote/05_database/06_dw_olap_trends/377_lsm_tree_storage_engine/)) [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 핵심 엔진으로 환생하여 현대 스토리지 아키텍처의 절대적 기반이 되었다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - 일반 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 내용이 변경되면, 예전 그 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 있던 물리적 위치(제자리, In-place)를 찾아가서 덮어쓴다.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/">LFS</a></strong>는 디스크를 하나의 거대한 무한의 롤 종이(Log)로 본다. 기존 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 수정하든 새 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 만들든 옛날 위치는 신경 안 쓰고, 무조건 메모리에 모아뒀던 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(수 MB 크기의 세그먼트)를 디스크의 맨 끝자락(빈 공간)에 차곡차곡 순서대로 덧붙여서(Append-only) 쓴다.

- **필요성(문제의식)**:
  - 1990년대, CPU 속도는 미친 듯이 빨라지고 램(RAM) 용량도 커져서 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) '읽기(Read)'는 메모리 캐시에서 다 해결되었다.
  - 문제는 '[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(Write)'였다. 수많은 사용자가 작은 문서 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(4KB)들을 동시에 저장하니, 디스크의 물리적 헤드가 이 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 저 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 덮어쓰러 디스크판 위를 미친 듯이 왔다 갔다(Random I/O) 하느라 서버가 뻗었다. 디스크 암(Arm)의 이동 속도는 물리적 한계에 부딪혔다.
  - **해결책**: "어차피 쓰는 게 문제라면, 헤드를 움직이지 마라! 들어오는 모든 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)과 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 쓰레기통에 쑤셔 넣듯 큰 덩어리로 뭉쳐서 디스크 맨 끝에 빈 공간으로 한 번에(Sequential) 쭉 밀어버려라!"

  - **기존 덮어쓰기 (Random Write)**: 백화점 진열대 100곳에 직원이 새로 들어온 신상품([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 일일이 카트를 끌고 돌아다니며(헤드 이동) 예전 자리에 진열하는 고통스러운 노동.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/">LFS</a> 순차 <a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> (Sequential Log)</strong>: 직원은 진열대를 돌아다니지 않는다. 새로 온 모든 물건을 창고 바닥 끝 빈자리(Log 끝단)부터 그냥 차곡차곡 무조건 일렬로 쏟아놓는다(Append). 놓는 속도는 1초면 끝난다. (나중에 물건 찾을 땐 어디 뒀는지 맵만 업데이트해 두면 된다).

- **등장 배경**:
  - 1992년 [UC](/knowledge-base/studynote/12_it_management/02_itsm_itil/871_underpinning_contract/) 버클리의 논문(The Design and Implementation of a [Log-Structured File System](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/))에서 처음 제안되었다. RAM 캐시의 확대로 'Read' 병목이 사라진 미래에는 오직 'Write' 병목만 남을 것을 정확히 예견한 선구적 아키텍처다.

```text
  +-------------------------------------------------------------+
  |                 기존 파일 시스템 vs LFS의 디스크 쓰기 동작 차이       |
  +-------------------------------------------------------------+
  |                                                             |
  |  [ 전통적 파일 시스템 (In-place Update) ] - 헤드 이동 지옥        |
  |   - 파일 A, B, C를 동시에 아주 조금씩 수정함.                     |
  |                                                             |
  |   디스크 ---> [ File A ] .... [ File B ] ......... [ File C ] |
  |   헤드이동    (찌익!) --> 윙~ --> (찌익!) --> 윙~~~~ --> (찌익!)     |
  |   -> 결과: Random Write 발생. 3번 덮어쓰는데 헤드가 3번 움직임(느림) |
  |                                                             |
  |  [ 로그 구조 파일 시스템 (LFS) ] - 순차 쓰기 (Append-Only)     |
  |   - 파일 A, B, C의 수정본을 메모리에 수 MB(Segment) 덩어리로 모음.   |
  |                                                             |
  |   디스크 ---> (기존 낡은 A, B, C는 버려짐 무시)                     |
  |           .................. [ 빈 공간 ]                      |
  |   헤드이동                    v (쿵! 한 번에 내려찍음)            |
  |           .................. [ 새 A | 새 B | 새 C | Inode 정보 ]|
  |   -> 결과: Sequential Write 발생. 흩어진 파일들을 하나로 뭉쳐 맨 끝단에 |
  |           단 1번의 헤드 이동만으로 연속해서 기록해 버림! 🚀            |
  +-------------------------------------------------------------+
```

**[다이어그램 해설]** 하드 디스크의 원판(Platter)에서 헤드가 움직이는 시간([Seek Time](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/))은 약 5~[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 밀리초(ms)로, CPU 속도와 비교하면 영겁의 시간이다. 전통적 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템은 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)(inode) 갱신하랴, 실제 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 덮어쓰랴 헤드를 이리저리 미친 듯이 튕긴다. LFS는 이 헤드의 기계적 진자 운동을 멈춰버렸다. 새로 쓴 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 조각들, 그리고 그 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 바뀐 주소를 적은 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)(inode) 조각까지 모조리 메모리에 묶어서 하나의 큰 블록([Segment](/knowledge-base/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/))으로 만들고, 헤드가 있는 현재 위치 뒤편에 그냥 도장 찍듯 찍고 끝낸다. 랜덤 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 마법처럼 100% 순차 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)로 변환(Sequentialize)되며 디스크 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 극한을 뽑아낸다.

- **📢 섹션 요약 비유**: 하루 일과를 다이어리 원래 있던 날짜 페이지를 찾아가서 지우개로 빡빡 지우고 다시 쓰는 게 아니라(기존), 두루마리 휴지 끝에 계속해서 오늘 날짜와 바뀐 내용만 밑으로 쭉쭉 이어서 적어 내려가는([LFS](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/)) 미친 듯이 빠른 속필 기록법입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### LFS의 핵심 구조: 아이노드 맵 (i-node Map, imap)

"무조건 디스크 맨 끝에 새 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 쓴다면, 내가 찾는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(A)이 디스크의 어느 위치로 이사 갔는지 OS가 어떻게 찾지?"

기존 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템은 inode([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 정보)가 디스크의 고정된 위치에 있었다. 하지만 LFS는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)뿐만 아니라 **inode조차 매번 맨 끝에 새롭게 써버린다(부유하는 inode)**. 이 딜레마를 해결하기 위해 `imap`이라는 마스터키가 존재한다.

1. <strong>디스크 끝에 <a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a></strong>: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) A의 내용과 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) A의 새 inode를 뭉쳐서 끝에 쓴다.
2. **imap 업데이트**: 메모리에 떠 있는 `imap(아이노드 맵)` 배열에 "[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) A의 새 inode 위치는 디스크의 9999번지다"라고 갱신한다.
3. **체크포인트(Checkpoint)**: 메모리의 `imap`이 날아가면 모든 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 영원히 잃어버리므로, 주기적으로 이 `imap`을 디스크의 절대 고정 위치(Checkpoint 영역)에 저장해 둔다.

```text
  +-------------------------------------------------------------------+
  |                 LFS의 파일 추적 (Read) 매커니즘: 포인터 추적        |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [ 파일 읽기 요청: "파일 A 읽어줘!" ]                                 |
  |                                                                   |
  |   1. 고정된 Checkpoint 구역 (디스크 끝단)                             |
  |      - 메모리에 캐싱된 `imap` 배열을 확인.                            |
  |      - "파일 A의 inode는 디스크 800번지에 새로 갱신되어 있군!"            |
  |               |                                                   |
  |               v                                                   |
  |   2. 부유하는 i-node (Log의 가장 최근 부분)                            |
  |      - 800번지로 감. "아하, 파일 A의 실제 데이터는 801번, 802번에 있네!"  |
  |               |                                                   |
  |               v                                                   |
  |   3. 실제 Data Block                                              |
  |      - 801번지, 802번지에서 데이터를 읽어 사용자에게 전달!                  |
  +-------------------------------------------------------------------+
```

### 치명적 단점: [가비지 컬렉션](/knowledge-base/studynote/02_operating_system/06_memory_management/380_garbage_collection/)([Garbage Collection](/knowledge-base/studynote/02_operating_system/06_memory_management/380_garbage_collection/) / Cleaner)의 저주

LFS의 가장 빛나는 장점(항상 덧붙여 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))이 결국 LFS의 목을 조르는 치명적 단점이 된다. 롤 종이에 계속 쓰다 보면 결국 디스크 전체 용량이 꽉 찬다.

- [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) A를 10번 고치면 디스크에는 낡고 유효하지 않은 '과거의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) A' 쓰레기 9개가 자리를 차지하고 있다.
- 디스크가 꽉 차기 전에, 백그라운드의 **Cleaner(청소부)** 데몬이 돌아야 한다.
- **Cleaner의 임무**: 오래된 디스크 앞부분 블록을 읽어서, 쓰레기 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 버리고 "아직 살아있는 진짜 최신 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)"만 건져내어 다시 디스크 맨 끝단 빈 곳에 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해서 복사해 놓는다. 그리고 텅 빈 앞부분 블록을 새하얗게 지워(Free) 새로운 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 공간으로 반환한다.
- **병목 폭발**: 디스크가 90% 이상 차버리면, 이 청소부가 쓸만한 빈 공간을 만들려고 끊임없이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽고 다시 쓰는 <strong>무한 복사 루프(Cleaning Overhead)</strong>에 빠진다. 이때 사용자가 앱을 돌리려 하면 서버가 통째로 멈춰버리는 끔찍한 현상이 일어난다.

- **📢 섹션 요약 비유**: 설거지를 안 하고 매번 새 그릇을 찬장에서 꺼내 쓰니 밥 차리는 속도는 엄청나게 빠릅니다(LFS의 장점). 하지만 어느 날 찬장에 새 그릇이 다 떨어지면, 싱크대에 산더미처럼 쌓인 수천 개의 더러운 그릇을 한 번에 다 닦을 때까지([가비지 컬렉션](/knowledge-base/studynote/02_operating_system/06_memory_management/380_garbage_collection/)) 밥을 한 술도 못 먹고 쫄쫄 굶어야 하는 끔찍한 파국(오버헤드)을 맞이하게 됩니다.

---

## Ⅲ. 비교 및 연결

### 덮어쓰기(In-place Update) vs [COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/)(ZFS) vs OOW([LFS](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/))

스토리지 아키텍트의 세계관을 가르는 3대 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 철학이다.

| 철학 및 아키텍처 | 동작 방식의 비유 | 장점 (승리 구간) | 단점 (치명타 구간) |
|:---|:---|:---|:---|
| **In-place Update** (ext4, NTFS) | 틀린 글자만 지우개로 지우고 그 자리에 고쳐 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) | 여백 공간(빈 디스크) 관리가 필요 없어 편함 | 여기저기 덮어쓰느라 헤드가 미친 듯이 움직임 (랜덤 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 최악) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/">Copy-on-Write</a></strong> (ZFS, Btrfs) | 고칠 글자가 있는 종이 1장만 복사해서 고치고 원본 버림 | 원본 훼손이 없어 정전 시 안전 100% 보장 | 쓰다 보면 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 조각이 사방으로 흩어짐 ([단편화](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/) [Fragmentation](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/) 지옥) |
| **Out-of-place Write** ([LFS](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/) 계열) | 고칠 글자들을 책상에 모아뒀다, 맨 뒷장에 통째로 풀로 붙임 | **수만 개의 흩어진 랜덤 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) $\rightarrow$ 1개의 쾌속 순차 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)** | 디스크가 꽉 찼을 때 쓰레기 청소(GC)를 하느라 시스템 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 폭락 |

### 과목 융합 관점

- <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/475_ssd_structure/">솔리드 스테이트 드라이브</a> (<a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/">SSD</a> 내부 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/">FTL</a>)</strong>: LFS가 메인 운영체제에서는 실패했지만, 놀랍게도 이 아이디어는 [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 하드웨어 칩 내부로 숨어들어가 전 세계 100%의 SSD를 지배하고 있다. [플래시 메모리](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/)(NAND)는 물리적으로 "덮어쓰기"가 불가능하다. 무조건 텅 빈 새 공간에 쓰고 쓰레기는 나중에 비워야(Erase) 한다. 즉, <strong><a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/">SSD</a> 컨트롤러 안에서 도는 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/">펌웨어</a>(<a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/">FTL</a>, <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/">Flash Translation Layer</a>)가 사실상 거대한 하나의 하드웨어판 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/">LFS</a></strong>인 것이다. [마모 평준화](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)([Wear Leveling](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/))와 [가비지 컬렉션](/knowledge-base/studynote/02_operating_system/06_memory_management/380_garbage_collection/) 개념이 여기서 정확히 융합된다.
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> 아키텍처 (<a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/377_lsm_tree_storage_engine/">LSM-Tree</a>)</strong>: [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), RocksDB, LevelDB 같은 현대 클라우드 NoSQL의 심장인 <strong>LSM (Log-Structured Merge) Tree</strong>는 [LFS](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 철학을 자료구조로 그대로 본뜬 것이다. B-Tree처럼 디스크 중간을 찢어서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 넣지 않고, 메모리에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 차곡차곡 쌓았다가 디스크 맨 끝에 순차적으로(SSTable) 쏟아부어 버린다. 디스크 랜덤 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 한계를 극복한 궁극의 고속 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 엔진이다.

- **📢 섹션 요약 비유**: LFS는 90년대에 "자동차([HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/))를 타고 다닐 때 헬리콥터 조종법(순차 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))"을 제시해서 너무 시대를 앞서가 실패한 비운의 천재입니다. 하지만 하늘을 나는 드론([SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/), [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/))의 시대가 도래하자 이 천재의 조종법이 모든 드론의 뼈대 표준으로 화려하게 부활한 드라마틱한 역전승입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오 및 서버 튜닝

1. <strong>시나리오 — <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/">Cassandra</a> / RocksDB (<a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/377_lsm_tree_storage_engine/">LSM-Tree</a> 기반)의 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/">쓰기 증폭</a>(<a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/">Write Amplification</a>)과 <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">Compaction</a> 병목</strong>: 막강한 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 자랑하는 NoSQL을 AWS 클라우드에 올렸다. 평소엔 날아다니다가 새벽 2시만 되면 CPU와 디스크 I/O가 100%를 치면서 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 응답이 끊기고 뻗는다.
   - **원인 분석**: [LFS](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/) 철학을 계승한 LSM-Tree의 숙명적인 빚 청산([가비지 컬렉션](/knowledge-base/studynote/02_operating_system/06_memory_management/380_garbage_collection/)) 시간이다. 낮에 미친 듯이 쏟아부은 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)(쓰레기 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))들을 모아서, 중복된 옛날 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 버리고 깨끗한 새 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 병합하는 <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">Compaction</a>(컴팩션)</strong> 작업이 백그라운드에서 터진 것이다. 이 작업은 디스크 전체를 미친 듯이 긁으며 엄청난 I/O 증폭을 일으킨다.
   - **아키텍트 판단 (컴팩션 스로틀링 및 티어링)**: 이런 [LFS](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/) 기반 아키텍처는 결코 디스크 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 한계(IOPS)의 100%를 사용하게 내버려 두면 안 된다. 아키텍트는 튜닝 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)(`compaction_throughput_mb_per_sec`)을 통해 컴팩션 데몬이 쓸 수 있는 디스크 속도의 상한선을 걸어(Throttling) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) I/O를 보호해야 한다. 또한 공간의 여유(Over-provisioning)를 항상 30~40% 이상 비워두어 쓰레기 청소가 여유롭게 진행될 수 있는 숨통을 틔워줘야 서버 프리징을 막을 수 있다.

2. <strong>시나리오 — <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 코디네이터 (<a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/">Zookeeper</a>, <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/">etcd</a>)의 WAL(Write-Ahead Log) 디스크 병목</strong>: 쿠버네티스의 뇌인 etcd나 [Zookeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 서버가 간헐적으로 "Leader election [timeout](/knowledge-base/studynote/02_operating_system/05_deadlock/319_timeout_prevention/)" 에러를 내며 클러스터가 붕괴된다.
   - **원인 분석**: 이런 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 합의 시스템의 핵심은 "상태 변경을 메모리에 적용하기 직전에, 무조건 디스크 끝단에 순차적인 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)(WAL, LFS의 Segment와 동일)로 기록하고 fsync를 때려야 한다"는 룰에 있다. 이 디스크 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 속도가 수십 밀리초(ms) 지연되면 클러스터 리더가 죽은 줄 알고 반란이 일어난다.
   - **아키텍트 판단 (전용 WAL 디스크 분리)**: etcd나 [Zookeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 서버를 구축할 때는 절대 OS 시스템 파티션이나 다른 앱이 랜덤 I/O를 날리는 디스크에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공간을 두면 안 된다. <strong>반드시 가장 빠른 최상급 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/">NVMe</a> <a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/">SSD</a> 디스크 하나를 오직 WAL(순차 <a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a>) 전용 경로로 물리적으로 분리 매핑</strong>해야 한다. 헤드 간섭이나 디스크 컨트롤러 캐시 간섭을 차단하여, 100% 순수 순차 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(Sequential Append) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 보장하는 것이 클러스터 생존의 1원칙이다.

```text
  +-------------------------------------------------------------------+
  |                 고성능 Write-Intensive 시스템 설계를 위한 아키텍트 트리    |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [ 쓰기(Write) 트래픽이 읽기(Read)보다 압도적으로 많은 시스템 설계 ]          |
  |                |                                                  |
  |                v                                                  |
  |      기존 B-Tree 기반 RDBMS(MySQL 등)의 인덱스 업데이트가 병목을 일으키는가? |
  |          +- 예 ------> [ LFS 철학을 품은 LSM-Tree 기반 DB 도입 (Cassandra) ]|
  |          |             (랜덤 I/O를 100% 순차 쓰기로 둔갑시켜 스루풋 극대화)  |
  |          +- 아니오                                                |
  |                |                                                  |
  |                v [LSM-Tree / 로그 기반 스토리지 도입 시 필수 아키텍처 방어망] |
  |      1. 디스크 공간 통제: 전체 용량의 80%를 넘지 않도록 강력한 알람 설정.       |
  |         (80%를 넘는 순간 GC/Compaction 오버헤드로 인해 성능 1/10 토막)   |
  |      2. I/O 분리: 순차적 쓰기 로그(WAL/Commit Log) 영역은 무조건         |
  |         물리적으로 다른 독립된 NVMe 디스크 볼륨으로 분리할 것.              |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** LFS의 사상을 차용한 시스템([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/), [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))은 '아름다운 거짓말' 위에서 돌아간다. 유저에게는 미친듯한 속도를 보여주지만 뒤에서는 쓰레기를 산더미처럼 치우고 있다. 아키텍트는 이 거짓말이 파국을 맞지 않도록 2가지를 강제해야 한다. 첫째, 넉넉한 여유 공간(빈 디스크). 청소부가 짐을 옮기려면 임시로 놓아둘 거대한 여백이 무조건 필요하다. 둘째, 순차 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(Sequential)의 절대 방어. 하나의 디스크에 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)과 일반 랜덤 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 섞어 쓰면 하드웨어 블록 큐가 꼬이면서 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 순차 속도마저 박살 나버린다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> 구조 스토리지(<a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/">SSD</a>) 위에서 잦은 작은 크기(4KB 이하)의 덮어쓰기 반복</strong>: SSD는 4KB 단위로 페이지를 읽어올 수 있지만, 지울 때(Erase)는 무려 1MB~4MB의 거대한 블록 단위로만 지울 수 있다. 개발자가 1바이트짜리 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)나 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 1초에 1천 번씩 계속 덮어쓰면, SSD의 [FTL](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/)([LFS](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/) 엔진)은 그 1바이트를 살리려고 주변의 4MB짜리 남의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)까지 통째로 들어다 다른 빈 블록으로 옮겨 적고 4MB 전체를 폭파하는 무식한 짓([Write Amplification](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/), [쓰기 증폭](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/) 4만 배)을 해야 한다. 이 짓을 한 달만 하면 엔터프라이즈급 디스크도 수명이 다해 즉사한다.

- **📢 섹션 요약 비유**: 종이 1장(4KB)만 버리고 싶은데, 쓰레기차([SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) Erase 블록)는 무조건 아파트 한 동(4MB)을 통째로 부숴야만 종이를 버릴 수 있는 구조입니다. 작은 쓰레기를 계속 버리면 아파트를 부수고 짓고를 반복하다가 파산합니다. 작은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 메모리에 크게 모아서(Batch) 한방에 내려써야 수명이 보존됩니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | In-place (제자리 덮어쓰기, ext4) | [LFS](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/) ([로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 순차 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)) / [LSM-Tree](/knowledge-base/studynote/05_database/06_dw_olap_trends/377_lsm_tree_storage_engine/) DB | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (Write 스루풋)** | 랜덤 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 시 초당 수백 IOPS로 한계 | 랜덤 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 순차 기록으로 묶어 수십만 IOPS 방어 | 무작위로 쏟아지는 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)/시계열 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장의 병목 원천 제거 |
| **정성 (Crash 복원력)** | 정전 시 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 꼬임, fsck로 전체 스캔 필요 | 디스크 맨 끝단의 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 꼬리표만 보고 즉각 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성 보장](/knowledge-base/studynote/05_database/07_exam_summary/442_consistency_integrity/) 및 1초 이내의 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 시스템 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)/[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| **정량 (GC 페널티 단점)**| 디스크 99% 차도 남은 구역에 쓰는 속도 동일 | **디스크 80% 차면 GC(청소) 지연으로 속도 추락** | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 용량 포화도에 극단적으로 종속되는 'Trade-off' 발생 |

### 미래 전망
- <strong>F2FS (Flash-Friendly <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">File</a> System)</strong>: 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 공식 포함된 삼성전자가 만든 차세대 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이다. LFS가 HDD를 위해 만들어져 실패했다면, F2FS는 철저하게 스마트폰([플래시 메모리](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/))의 수명과 특성을 위해 [LFS](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/) 구조를 현대적으로 재해석했다. 안드로이드 모바일 기기에서 앱 설치와 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 기록 속도를 획기적으로 개선하며 모바일 표준으로 군림하고 있다.
- <strong>Key-Value 스토리지 하드웨어 내재화 (KV-<a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/">SSD</a>)</strong>: 블록(LBA)을 쪼개고 FTL이 뒤섞고 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이 또 뒤섞는 중복의 낭비를 없애기 위해, 호스트가 아예 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 아니라 Key-Value [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 SSD에 던지면, [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 내부 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)(하드웨어 [LFS](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/) 엔진)가 알아서 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 쌓고 컴팩션까지 쳐주는 스마트 스토리지([Computational Storage](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/498_computational_storage/)) 기술이 빅데이터 센터의 차세대 폼팩터로 등극하고 있다.

### 참고 표준
- **SSTable (Sorted String Table)**: 구글의 Bigtable 논문에서 정립된 개념으로, 메모리의 랜덤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 정렬해 두었다가 디스크에 수정 불가능한([Immutable](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/298_immutable/)) 순차 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 형태로 덤프 뜨는 [LFS](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/) 파생 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 표준 규격.
- <strong>eMMC / UFS <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">Protocol</a></strong>: 스마트폰에 탑재되는 [플래시 메모리](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/) 규격으로, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 조각난 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 명령을 하드웨어 레벨에서 버퍼링하여 순차적으로 내려꽂도록 [LFS](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/) 철학이 하드웨어 명령어로 구현된 규격.

[LFS](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/) ([Log-structured File System](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/))는 "속도(Write Speed)를 얻기 위해 공간(Space)과 청소의 고통([Garbage Collection](/knowledge-base/studynote/02_operating_system/06_memory_management/380_garbage_collection/))을 기꺼이 감내하겠다"는 컴퓨터 아키텍처의 가장 대담하고 극단적인 영혼의 거래다. 90년대 하드 디스크 시절에는 청소의 고통이 너무 커서 역사의 뒤안길로 사라진 낡은 논문인 줄 알았다. 그러나 회전하는 원판이 사라지고 전자가 실리콘을 태우는 SSD와 클라우드 빅데이터 시대가 도래하자, 인류는 무작위(Random)의 혼돈을 순차적(Sequential)인 질서로 정렬해 내는 LFS의 천재성을 다시 발굴해 냈다. 이 30년 전의 낡은 철학은 이제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)센터의 가장 깊은 곳에서 세계의 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 묵묵히 빨아들이고 있다.

- **📢 섹션 요약 비유**: 너무 무거운 철퇴([LFS](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/))라서 아무도 못 들고 창고에 버려져 있던 무기가, 30년 뒤 세상 사람들의 근력([SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/), CPU 메모리)이 폭발적으로 강해지자 창고에서 다시 꺼내져 적의 성벽(랜덤 I/O 병목)을 일격에 박살 내는 전설의 최종 무기로 부활한 완벽한 영웅 서사입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 동적 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 트레이싱 프레임워크 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| ZFS [Copy-on-Write](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/) 볼륨 관리 통합 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 모바일 환경 에너지 인지 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [하이퍼스레딩](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/199_interrupt_scheduling/) 물리 코어 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 코어 분할 구조 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[ZFS Copy-on-Write 볼륨 관리 통합]
    |
    v
[LFS (Log-structured File System) 랜덤 쓰기 순차화]
    |
    +---> [모바일 환경 에너지 인지 스케줄러]
    +---> [하이퍼스레딩 물리 코어 논리 코어 분할 구조]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 칠판(디스크)에 그림([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 지우고 새로 그리는 건 시간이 꽤 오래 걸려요. (기존 덮어쓰기)
2. 그래서 똑똑한 선생님은 아주 긴 두루마리 도화지([로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))를 가져와서, 예전 그림을 굳이 지우지 않고 무조건 끝부분 빈 공간에 새 그림을 휙휙 엄청 빨리 그려나갔어요. ([LFS](/knowledge-base/studynote/02_operating_system/09_file_system/541_log_structured_file_system/) 순차 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))
3. 다 그리다 종이가 꽉 차면, 종이의 앞부분부터 보면서 쓸데없는 낙서는 가위로 잘라버리고 예쁜 그림들만 다시 모아서 뒤쪽에 붙이는 청소([가비지 컬렉션](/knowledge-base/studynote/02_operating_system/06_memory_management/380_garbage_collection/))를 해준답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 782 / 800

<- **이전**: [781. ZFS Copy-on-Write 볼륨 관리 통합 (Zfs COW Volume Management)](/knowledge-base/studynote/02_operating_system/11_exam_summary/781_zfs_cow_volume_management/)
**다음**: [783. 모바일 환경 에너지 인지 스케줄러 (Mobile Energy Aware Scheduler Eas)](/knowledge-base/studynote/02_operating_system/11_exam_summary/783_mobile_energy_aware_scheduler_eas/) ->

---
