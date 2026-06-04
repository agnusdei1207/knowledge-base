---
title: "712. 외부 단편화 가변 분할 (External Fragmentation Variable Partition)"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 가변 분할(Variable [Partitioning](/studynote/05_database/03_relational_model/179_table_partitioning_concept/))은 프로세스의 크기에 딱 맞춰 메모리를 동적으로 잘라 주는 [연속 메모리 할당](/studynote/02_operating_system/06_memory_management/338_contiguous_memory_allocation/) 기법이다. 하지만 프로세스들이 켜지고 꺼지기를 반복하다 보면, <strong>메모리 중간중간에 쓰지 못하는 자잘한 빈 공간(Hole)들이 흩어지게 되는 <a href="/studynote/02_operating_system/06_memory_management/342_external_fragmentation/">외부 단편화</a>(<a href="/studynote/02_operating_system/06_memory_management/342_external_fragmentation/">External Fragmentation</a>)</strong>가 발생한다.
> 2. **치명적 문제**: 빈 공간들을 다 합치면 100MB인데도 불구하고, 새로 들어오려는 50MB짜리 프로세스가 "연속된 50MB 공간"을 찾지 못해 실행을 거부당하는 메모리 낭비 현상이 [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)의 핵심이다.
> 3. **해결책**: 이를 해결하기 위해 조각난 빈 공간을 한쪽으로 몰아 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)([Compaction](/studynote/02_operating_system/06_memory_management/347_compaction/))하는 기법이 도입되었으나 오버헤드가 너무 커서 실패했고, 결국 "메모리를 연속으로 할당해야 한다"는 고정관념을 깬 <strong><a href="/studynote/02_operating_system/04_synchronization/259_paging/">페이징</a>(<a href="/studynote/02_operating_system/04_synchronization/259_paging/">Paging</a>)</strong> 기술의 등장으로 [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)는 현대 OS에서 영원히 소멸하였다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong>가변 분할 (Dynamic / Variable <a href="/studynote/05_database/03_relational_model/179_table_partitioning_concept/">Partitioning</a>)</strong>: 메모리를 미리 나눠두지 않고, 프로그램이 실행될 때 그 크기(예: 12MB, 5MB)만큼 정확히 잘라서 할당해 주는 방식.
  - <strong><a href="/studynote/02_operating_system/06_memory_management/342_external_fragmentation/">외부 단편화</a> (<a href="/studynote/02_operating_system/06_memory_management/342_external_fragmentation/">External Fragmentation</a>)</strong>: 메모리 할당과 해제가 반복되면서, 사용 중인 메모리 사이사이에 작은 빈 공간(Hole)들이 조각조각 남는 현상. 전체 남은 용량은 충분하지만 조각나 있어서 큰 프로그램을 올릴 수 없는 상태.

- **필요성 (고정 분할의 메모리 낭비 극복 시도)**:
  - 초창기에는 램(RAM)을 10MB씩 똑같이 썰어두는 고정 분할(Fixed [Partitioning](/studynote/05_database/03_relational_model/179_table_partitioning_concept/))을 썼다. 하지만 1MB짜리 프로그램이 10MB 방에 들어가면 9MB가 고스란히 버려지는 '[내부 단편화](/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/)' 문제가 심각했다.
  - **해결책**: "프로그램 크기에 딱 맞춰서 방을 만들어 주자(가변 분할)!" 이렇게 하면 남는 공간 없이 알뜰하게 쓸 수 있을 줄 알았다.
  - 하지만, 방이 생겼다 없어지기를 반복하다 보니 결국 이빨 빠진 것처럼 중간중간에 1MB, 2MB짜리 쓸모없는 자투리 공간([외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/))이 생겨나 시스템이 멈추는 부작용이 터졌다.

  - **가변 분할**: 주차장(메모리)에 선이 그어져 있지 않다. 소형차(작은 앱), 대형 트럭(큰 앱)이 들어올 때마다 자기 차 크기만큼만 딱 맞춰 주차하게 해준다.
  - <strong><a href="/studynote/02_operating_system/06_memory_management/342_external_fragmentation/">외부 단편화</a></strong>: 트럭이 나간 자리에 소형차가 쏙 들어갔다. 그런데 그 옆에 자전거나 들어갈 법한 아주 애매한 틈새(Hole)가 남았다. 이런 틈새가 주차장 곳곳에 100개가 생겼다. 틈새를 다 합치면 트럭 10대가 들어갈 넓이인데, 트럭 한 대도 주차할 수가 없다.

- **발전 과정**:
  1. **고정 분할**: 너무 많은 [내부 단편화](/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/)(버려지는 공간) 발생.
  2. **가변 분할**: [내부 단편화](/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/)는 없앴으나, 최악의 [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) 발생.
  3. <strong><a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a> (<a href="/studynote/02_operating_system/06_memory_management/347_compaction/">Compaction</a>)</strong>: [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)를 모으려 시도했으나 CPU 과부하로 포기.
  4. <strong><a href="/studynote/02_operating_system/04_synchronization/259_paging/">페이징</a> (<a href="/studynote/02_operating_system/04_synchronization/259_paging/">Paging</a>)</strong>: 연속 할당을 포기하고 조각을 흩뿌리는 방식으로 [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) 완전 정복.

- **📢 섹션 요약 비유**: 테트리스를 할 때, 블록 모양에 맞춰 빈틈없이 쌓으려다 보면 결국 중간중간에 비어있는 한 칸짜리 구멍([외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/))들이 생겨나고, 긴 막대기 블록을 꽂을 수 없어 게임 오버([OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/))가 되는 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) 발생 시뮬레이션

프로세스 A, B, C, D가 들어오고 나가는 과정을 통해 구멍(Hole)이 어떻게 생기는지 살펴본다. (전체 메모리 100MB)

```text
  +-------------------------------------------------------------------+
  |                 가변 분할 환경의 외부 단편화 생성 타임라인            |
  +-------------------------------------------------------------------+
  |  [ T=1. 초기 할당 ]                                                 |
  |   [ A (20MB) ] [ B (30MB) ] [ C (20MB) ] [ 빈 공간 (30MB) ]      |
  |                                                                   |
  |  [ T=2. 프로세스 B 종료 (해제) ]                                     |
  |   [ A (20MB) ] [ 빈 공간 (30MB) ] [ C (20MB) ] [ 빈 공간 (30MB) ] |
  |                                                                   |
  |  [ T=3. 새로운 프로세스 D (10MB) 도착 및 할당 (First-Fit) ]         |
  |   [ A (20MB) ] [ D (10MB) ] [ 빈 공간 (20MB) ] [ C (20MB) ]       |
  |                             [ 빈 공간 (30MB) ]                    |
  |                                                                   |
  |  [ T=4. 거대 프로세스 E (40MB) 가 도착했다! ]                        |
  |   - 현재 남은 메모리 총합: 20MB + 30MB = 50MB (용량은 충분함!)        |
  |   - 하지만 E는 40MB짜리 연속된 덩어리가 필요하다.                        |
  |   - 20MB 구멍이나 30MB 구멍 어디에도 들어갈 수 없다.                    |
  |   ★ 결론: E는 메모리 할당을 받지 못하고 거절당함 (External Fragmentation) |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 가변 분할 시스템에서 OS는 빈 공간들의 시작 주소와 크기를 [연결 리스트](/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)(Free List)로 관리한다. E 프로세스가 40MB를 달라고 할 때, OS가 이 리스트를 끝까지 뒤져봐도 조건에 맞는 덩어리가 없으면 즉시 [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/)([Out of Memory](/studynote/02_operating_system/02_process_thread/157_oom_killer/)) 에러를 뱉는다. 물리적인 용량이 남았음에도 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 사용할 수 없는 이 상태가 컴퓨터 구조 역사상 가장 뼈아픈 낭비였다.

---

### [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)의 해결 시도: [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) ([Compaction](/studynote/02_operating_system/06_memory_management/347_compaction/) / Defragmentation)

"조각이 나 있으면, 프로세스들을 한쪽으로 쓱 밀어서 흩어진 빈 공간들을 하나로 뭉치자!"

- **메커니즘**: 메모리에 떠 있는 프로세스들의 실행을 전부 멈추고(Stop the world), 물리 램의 바이트를 복사하여 한쪽 끝으로 차곡차곡 재배치한다.
- **실패 원인 (오버헤드 폭발)**:
  1. 기가바이트(GB) 단위의 메모리를 복사(Memory Copy)하는 데 엄청난 CPU 연산과 시간이 소모된다 (수 초~수십 초간 시스템 마비).
  2. 프로세스들이 이사를 갔으므로, MMU의 Base [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 주소를 전부 갱신해 주어야 한다 (<strong><a href="/studynote/02_operating_system/06_memory_management/327_execution_time_binding/">실행 시간 바인딩</a></strong> 환경에서만 가능).
- **결론**: 실시간으로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)을 돌리는 것은 컴퓨터를 너무 느리게 만들어, [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 단위에서는 폐기된 아이디어다.

- **📢 섹션 요약 비유**: 이 빠진 책장의 빈 공간을 합치려고 책 수천 권을 전부 빼서 왼쪽으로 꽉꽉 밀어 넣는 작업([압축](/studynote/02_operating_system/06_memory_management/347_compaction/))입니다. 공간은 생기지만 책을 밀어 넣느라 진이 다 빠져서 정작 책을 읽을(연산) 체력이 남지 않게 됩니다.

---

## Ⅲ. 비교 및 연결

### [내부 단편화](/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/) vs [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)

메모리 관리 시험 문제의 절대적인 단골 비교 주제다.

| 비교 항목 | [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) ([External Fragmentation](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)) | [내부 단편화](/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/) ([Internal Fragmentation](/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/)) |
|:---|:---|:---|
| **발생 환경** | **가변 분할** (프로세스 크기대로 자를 때) | <strong>고정 분할 / <a href="/studynote/02_operating_system/04_synchronization/259_paging/">페이징</a></strong> (정해진 블록 크기로 자를 때) |
| **현상** | 메모리 조각들이 흩어져 큰 덩어리를 못 넣음 | 할당된 블록 안에서 안 쓰고 남은 공간이 버려짐 |
| **위치** | 프로세스들에게 할당되지 않은 '바깥(Hole)' | 프로세스에게 할당된 공간 '내부' |
| **현대 OS의 대처**| <strong><a href="/studynote/02_operating_system/04_synchronization/259_paging/">페이징</a>(<a href="/studynote/02_operating_system/04_synchronization/259_paging/">Paging</a>)을 도입하여 완벽히 멸종시킴</strong> | 완벽히 없앨 수 없으므로, 블록([Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)) 크기를 작게(4KB) 잘라서 낭비를 최소화함 |

### 과목 융합 관점

- <strong>자료구조 (<a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Structure)</strong>: [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 메모리는 아니지만, 개발자가 C/C++에서 쓰는 힙 메모리(`malloc`) 동작 원리가 바로 이 <strong>가변 분할</strong>과 100% 똑같다. 개발자가 `malloc(10)`과 `free()`를 수없이 반복하면, 힙([Heap](/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/)) 공간에 엄청난 <strong><a href="/studynote/02_operating_system/06_memory_management/342_external_fragmentation/">외부 단편화</a></strong>가 발생한다. C언어 서버가 1달쯤 켜놓으면 메모리가 충분한데도 `malloc`이 실패하며 죽는 이유가 바로 힙의 [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) 때문이다.
- **저장 장치 (Storage)**: 과거 [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 시절, 파일을 지웠다 썼다 하면 디스크 표면에 파일들이 조각조각 나뉘어 저장되는 '디스크 [단편화](/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)'가 발생해 I/O 속도가 수십 배 느려졌다. 이를 물리적으로 뭉쳐주는 유틸리티가 바로 윈도우의 '디스크 조각 모음(Defragmentation = [Compaction](/studynote/02_operating_system/06_memory_management/347_compaction/))'이었다.

- **📢 섹션 요약 비유**: 피자를 시킬 때, "내가 먹을 만큼만 잘라줘(가변 분할)"라고 하면 피자 판에 모양이 이상한 자투리 조각([외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/))들이 남아 버리기 애매해집니다. "무조건 8등분 해놔(고정 분할)"라고 하면 조각 크기는 깔끔하지만, 조금만 먹고 남긴 피자 테두리([내부 단편화](/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/))가 버려지게 됩니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — <a href="/studynote/05_database/04_transactions_concurrency/542_redis/">Redis</a>(인메모리 DB)의 jemalloc 파편화 (<a href="/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/">Fragmentation</a> Ratio)</strong>: [레디스](/studynote/05_database/05_distributed_nosql_newsql/297_snowflake_schema/) 서버에 32GB 램을 주었는데, 실제 저장된 Key-Value 데이터는 20GB밖에 안 되는데 OS는 [레디스](/studynote/05_database/05_distributed_nosql_newsql/297_snowflake_schema/)가 30GB를 쓴다고 보고함.
   - **원인 분석**: [레디스](/studynote/05_database/05_distributed_nosql_newsql/297_snowflake_schema/)가 메모리를 할당할 때 쓰는 `jemalloc` 할당기 내부에서 파편화가 발생한 것이다. 작은 크기의 Key를 지우고 큰 크기의 Key를 쓰는 행위가 반복되면서, 힙 영역에 10GB에 달하는 구멍(Holes)들이 흩어졌지만, 이 구멍들을 연속된 공간으로 합치지 못해 OS에 메모리를 반환하지 못한 전형적인 메모리 관리 레벨의 [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) 현상이다.
   - **대응 (기술사적 가이드)**: `INFO memory` 명령어로 `mem_fragmentation_ratio` 지표를 확인한다. 비율이 1.5 이상으로 치솟으면 파편화가 심각한 상태다. [레디스](/studynote/05_database/05_distributed_nosql_newsql/297_snowflake_schema/) 4.0 이상부터 지원되는 [액티브](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) 디프래그먼테이션(`activedefrag yes`)을 켜서, [레디스](/studynote/05_database/05_distributed_nosql_newsql/297_snowflake_schema/)가 백그라운드에서 메모리 복사를 통해 조각을 모으게([Compaction](/studynote/02_operating_system/06_memory_management/347_compaction/)) 튜닝해야 OOM을 막을 수 있다.

2. <strong>시나리오 — JVM <a href="/studynote/05_database/uncategorized/591_mvcc_garbage_collection_vacuum/">가비지 컬렉터</a>(GC)의 <a href="/studynote/02_operating_system/06_memory_management/347_compaction/">Compaction</a>(<a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a>) 오버헤드</strong>: 자바 서버에서 갑자기 10초간 응답이 뚝 끊기는 Stop-The-World (STW) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 발생.
   - **원인 분석**: JVM의 힙([Heap](/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/)) 메모리(가변 분할)에 객체들이 쌓이고 해제되면서 [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)가 극심해졌다. 거대한 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) 객체를 새로 만들려는데 빈 공간이 없자, JVM의 Old Generation GC가 작동하여 힙 메모리 전체를 훑으면서 살아남은 객체들을 한쪽으로 싹 밀어버리는 <strong><a href="/studynote/02_operating_system/06_memory_management/347_compaction/">Compaction</a>(<a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a>)</strong> 작업을 수행하느라 앱을 10초간 정지시킨 것이다.
   - **아키텍처 적용**: 멈춤(STW) 시간을 없애기 위해, 객체를 한쪽으로 밀어버리는 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)([Compaction](/studynote/02_operating_system/06_memory_management/347_compaction/))을 아예 포기하거나, 혹은 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)을 하더라도 앱을 멈추지 않고 백그라운드에서 동시(Concurrent)에 주소를 매핑해 주는 **G1GC** 나 **ZGC**, 최신의 <strong>Shenandoah GC</strong>로 런타임 아키텍처를 교체해야 한다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 애플리케이션 메모리 파편화(Fragmentation) 대응 플로우      |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [C/C++ 서버나 DB가 장기 구동될수록 메모리 사용량이 비정상적으로 증가함]        |
  |                |                                                  |
  |                v                                                  |
  |      1. Valgrind 등의 툴로 "메모리 누수(Memory Leak)" 여부를 확인한다.     |
  |         - `free()`를 빼먹은 누수인가? -> 소스코드 로직 버그. 수정 필요.     |
  |         - 누수는 0바이트인데 OS 메모리는 계속 차는가?                       |
  |                |                                                  |
  |                v                                                  |
  |      2. [메모리 할당기의 외부 단편화(Fragmentation) 확진]               |
  |         - 원인: glibc의 기본 `malloc`이 작은 객체의 잦은 생성/삭제에 취약함.|
  |                |                                                  |
  |                v                                                  |
  |      3. [메모리 할당기(Allocator) 아키텍처 교체]                         |
  |         대책: 파편화 방지에 특화된 [jemalloc] (FaceBook 개발) 이나       |
  |               [tcmalloc] (Google 개발) 라이브러리로 링크를 교체하여      |
  |               할당 알고리즘 자체를 업그레이드 (성능 20% 상승 효과)          |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(OS)가 앱을 띄울 때 램에 할당하는 방식은 [페이징](/studynote/02_operating_system/04_synchronization/259_paging/)([Paging](/studynote/02_operating_system/04_synchronization/259_paging/)) 기술 덕분에 [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)가 완전히 멸종되었다. 하지만, <strong>"앱 내부에서(User Space) 힙(<a href="/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/">Heap</a>) 메모리를 쪼개 쓰는 방식"은 여전히 가변 분할의 저주를 받고 있다.</strong> 아키텍트는 OS 수준의 [단편화](/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)와 어플리케이션 수준의 힙 [단편화](/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)를 명확히 구분하고 대처해야 한다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong>Object Pool (<a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/442_memory_pooling/">메모리 풀링</a>)</strong>: 게임 엔진(C++)이나 고성능 서버 개발 시, `new`와 `delete`를 수만 번 부르면 파편화가 생겨 서버가 터진다. 이를 막기 위해 시작 시점에 똑같은 크기의 객체를 1만 개 미리 할당(정적 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/))해 두고, 끄고 켜는 [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)([Flag](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/))만 조작하여 [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) 자체를 물리적으로 원천 차단하는 **오브젝트 풀(Object Pool)** 디자인 패턴을 필수적으로 적용했는가?

- **📢 섹션 요약 비유**: OS는 [페이징](/studynote/02_operating_system/04_synchronization/259_paging/)이라는 '규격화된 택배 상자'를 써서 트럭(램)의 빈 공간 낭비를 100% 없앴습니다. 하지만 그 상자 안에 물건을 쑤셔 넣고 정리하는 일은 여전히 개발자(malloc)의 몫이며, 여기서 정리를 못 해 쓰레기 [더미](/studynote/04_software_engineering/11_testing_validation/851_dummy_test_double/)(파편화)를 만드는 것은 순전히 개발자의 책임입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 단순 가변 분할 (malloc 남용) | 파편화 최적화 ([Memory Pool](/studynote/02_operating_system/06_memory_management/369_memory_pool/) / [페이징](/studynote/02_operating_system/04_synchronization/259_paging/)) | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정량 (<a href="/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a> 비율)</strong> | 조각난 메모리로 인해 잦은 할당 실패 | 조각 발생 원천 차단 | 장기 구동(Uptime) 서버의 메모리 에러 [제로화](/studynote/01_computer_architecture/15_advanced_topics/784_zeroization_circuit/) |
| <strong>정성 (<a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 지터)</strong> | [Compaction](/studynote/02_operating_system/06_memory_management/347_compaction/) 발동 시 수 초간 멈춤 | 할당/해제 속도 $O(1)$ 상수 시간 보장| P99 응답 시간의 튀는 현상([Spike](/studynote/04_software_engineering/02_requirements_analysis/129_spike_agile_technical_investigation/)) 제거 |
| **정량 (자원 활용)** | 램 공간 30~40% 허공에 낭비 | 남는 자투리 공간 0% (완전 활용) | 클라우드 메모리(RAM) 비용의 대폭 절감 |

### 미래 전망
- <strong><a href="/studynote/02_operating_system/11_exam_summary/760_slab_allocator_object_caching/">SLAB</a> / SLUB 할당기의 진화</strong>: 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 스스로도 내부 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 객체를 만들 때 파편화에 시달렸다. 이를 극복하기 위해 크기가 똑같은 객체(예: inode 구조체 전용)들만 모아두는 [SLAB](/studynote/02_operating_system/11_exam_summary/760_slab_allocator_object_caching/) 할당기를 도입하여 가변 분할의 약점을 완전히 극복했으며, 오늘날 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 메모리 관리를 세계 최고로 만든 일등 공신이 되었다.
- <strong><a href="/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a> 기반 힙 <a href="/studynote/02_operating_system/10_security/613_profiling_gprof/">프로파일링</a></strong>: 힙 [단편화](/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)를 분석하려면 예전에는 앱을 껐다 켜면서 무거운 툴을 붙여야 했다. 이제는 eBPF를 통해 운영 중인 서버에서 0.1%의 오버헤드만으로 실시간 `malloc`/`free` 크기 분포를 시각화하여 파편화의 주범 코드를 즉각 찾아내는 관제 시스템이 표준이 되었다.

### 결론
가변 분할과 [외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)([External Fragmentation](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/))는 "사용자의 요구사항(프로세스 크기)을 100% 맞춰주겠다"는 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 순진한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 정신이 낳은 비극적인 결말이다. 완벽히 맞춰서 주려다 보니, 정작 남은 잉여 자원들을 통제할 수 없게 되어 시스템 전체가 무너지는 역설에 빠진 것이다. 이 뼈아픈 실패를 통해, 컴퓨터 공학자들은 "연속해서 줘야 한다"는 낡은 환상을 깨부수고, 데이터를 잘게 찢어서 여기저기 흩뿌리는 <strong><a href="/studynote/02_operating_system/04_synchronization/259_paging/">페이징</a>(<a href="/studynote/02_operating_system/04_synchronization/259_paging/">Paging</a>)이라는 인류 최고의 우회술</strong>을 발명해 내는 위대한 도약을 이루게 된다.

- **📢 섹션 요약 비유**: 각자의 입맛(프로세스 크기)에 딱 맞춘 주문 제작(가변 분할)은 결국 재고의 짜투리 낭비([외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/))를 버티지 못하고 망합니다. 세상을 구원한 것은 사이즈를 딱 하나(4KB)로 고정하여 공장식으로 찍어낸 규격화의 혁명([페이징](/studynote/02_operating_system/04_synchronization/259_paging/))이었습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [주소 바인딩](/studynote/02_operating_system/06_memory_management/324_address_binding_stages/) 컴파일/로드/실행 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [논리 주소](/studynote/02_operating_system/06_memory_management/322_logical_virtual_address/) [물리 주소](/studynote/02_operating_system/06_memory_management/323_physical_address/) 변환 [MMU](/studynote/02_operating_system/06_memory_management/328_mmu/) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [내부 단편화](/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/) 고정/[페이징](/studynote/02_operating_system/04_synchronization/259_paging/) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 동적 할당 First/Best/[Worst Fit](/studynote/02_operating_system/06_memory_management/346_worst_fit/) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[논리 주소 물리 주소 변환 MMU]
    |
    v
[외부 단편화 가변 분할 (External Fragmentation Variable Partition)]
    |
    +---> [내부 단편화 고정/페이징]
    +---> [동적 할당 First/Best/Worst Fit]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 주차장(메모리)에 주차 선을 안 그려놓고, 차가 올 때마다 딱 차 크기만큼만 바짝 붙여서 주차하게 했어요(가변 분할).
2. 트럭이랑 자전거가 번갈아 가며 주차했다 나갔다 하니까, 나중에는 자전거 1대만 들어갈 만한 아주 좁은 빈틈(구멍)들이 주차장 곳곳에 100개나 생겼어요.
3. 틈새들을 다 합치면 트럭 10대도 들어갈 크기인데, 틈새가 뿔뿔이 흩어져([단편화](/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)) 있으니까 진짜 트럭이 오면 주차를 못 하고 쫓겨나는 바보 같은 상황이 바로 '[외부 단편화](/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)'랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 712 / 800

<- **이전**: [711. 논리 주소 물리 주소 변환 MMU (Logical Physical Address Translation MMU)](/studynote/02_operating_system/11_exam_summary/711_logical_physical_address_translation_mmu/)
**다음**: [713. 내부 단편화 고정/페이징 (Internal Fragmentation Fixed Paging)](/studynote/02_operating_system/11_exam_summary/713_internal_fragmentation_fixed_paging/) ->

---
