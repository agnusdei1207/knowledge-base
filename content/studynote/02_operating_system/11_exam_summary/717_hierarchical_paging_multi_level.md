+++
title = "717. 다단계 페이지 테이블 사이즈 줄이기 (Hierarchical Paging Multi Level)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) 시스템의 가장 큰 부작용은 [가상 주소 공간](/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/)이 커질수록(32비트 $\rightarrow$ 64비트) 메모리를 매핑하기 위한 '[페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)(지도)' 자체가 수십 MB에서 수백 GB까지 커져, <strong>정작 유저 프로그램이 쓸 메모리(RAM)를 지도가 다 잡아먹는 배보다 배꼽이 큰 사태</strong>가 터진다는 점이다.
> 2. **메커니즘 (다단계/Hierarchical)**: 이를 막기 위해 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)을 책의 '목차'처럼 2단계, 3단계, 4단계로 쪼갠다. 가장 핵심인 대목차(Root [Directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/))만 메모리에 항상 올려두고, <strong>실제 사용하지 않는 빈 <a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/">가상 메모리</a> 구역의 하위 <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/">페이지 테이블</a>은 아예 메모리에 생성조차 하지 않는 동적 할당(Dynamic Allocation)</strong>이 가능해진다.
> 3. **트레이드오프**: [다단계 페이징](/knowledge-base/studynote/02_operating_system/06_memory_management/361_hierarchical_paging/)은 물리 메모리 낭비를 극적으로(99% 이상) 줄여주지만, [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)을 4번 쪼개면 주소를 한 번 찾을 때 램을 4번이나 읽어야 하는 <strong>메모리 접근 <a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>(<a href="/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">Page</a> Walk Overhead)</strong>을 낳는다. 이를 하드웨어 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 캐시로 덮고(Cover) 있는 것이 현대 OS의 현실이다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong>1단계 (단일) <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/">페이지 테이블</a></strong>: 가상 주소의 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 개수만큼 무조건 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)([Array](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/))의 칸을 다 만들어두는 1차원 구조.
  - <strong><a href="/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/289_multilevel_page_table/">다단계 페이지 테이블</a> (Multi-level <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/">Paging</a>)</strong>: [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)을 여러 계층([Directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) $\rightarrow$ Middle $\rightarrow$ Table)으로 트리(Tree)처럼 나누어 관리하는 구조.

- **필요성 (메모리 폭발의 공포)**:
  - 32비트 시스템에서 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 크기는 4GB다. [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 크기가 4KB면 총 100만 개의 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 나온다.
  - [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 번호를 적어두는 엔트리 1개가 4바이트라고 하면, **프로세스 1개당 "순수 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 용량"만 딱 4MB(100만 * 4바이트)**가 필요하다.
  - 프로세스를 1,000개 띄우면? 지도(Table) 크기만 4GB가 되어 물리 램이 터져버린다.
  - 심지어 프로세스는 보통 코드, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)만 쓰므로 4GB 가상 주소 중 99%는 텅텅 비어있는데(Sparse Address Space), 1단계 테이블은 이 안 쓰는 99%의 주소록 칸도 무조건 만들어둬야 했다.
  - **해결책**: "안 쓰는 구역의 지도는 아예 만들지 말자!" 목차([Directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/))만 만들어두고, 진짜로 그 동네에 아파트(메모리)를 지을 때만 그 동네의 상세 지도([Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/))를 메모리에 올리자는 아이디어가 나왔다.

  - <strong>1단계 <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/">페이징</a> (종이 지도책)</strong>: 전 세계 모든 골목길 지도가 담긴 두꺼운 책을 들고 다닌다. 내가 평생 한국 밖을 나갈 일이 없는데도, 아프리카 사하라 사막의 골목길 지도(빈 공간)까지 억지로 들고 다녀야 해서 가방(RAM)이 무거워 터진다.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/361_hierarchical_paging/">다단계 페이징</a> (인터넷 지도 앱)</strong>: 내 폰에는 전 세계 '국가 목록(1단계 Root)'만 있다. 내가 "한국"을 누르면 "한국의 시/도 지도(2단계)"만 다운받는다. 내가 아프리카를 갈 일이 없으면 아프리카 지도는 평생 폰(RAM)에 다운받을 일이 없다. 가방이 텅텅 비고 가벼워진다.

- **발전 과정**:
  1. <strong>1-Level <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/">Paging</a></strong>: 16비트 시절, 메모리가 작아 가능했음.
  2. <strong>2-Level <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/">Paging</a></strong>: 32비트(x86) 환경의 표준. ([Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) [Directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) + [Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/))
  3. <strong>4-Level <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/">Paging</a></strong>: 64비트(x86-64) 환경. 가상 주소가 너무 방대해져 4단계로 쪼갬.
  4. <strong>5-Level <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/">Paging</a></strong>: 테라바이트급 서버를 위해 인텔 Ice Lake부터 도입된 최신 구조.

- **📢 섹션 요약 비유**: 두꺼운 백과사전([페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/))을 통째로 펴놓고 보는 대신, 목차만 책상에 올려놓고 필요할 때만 서고에서 해당 챕터의 낱장만 빼오는 궁극의 메모리 다이어트 기술입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 32비트 시스템의 2단계 [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) 아키텍처 (x86 기준)

[논리 주소](/knowledge-base/studynote/02_operating_system/06_memory_management/322_logical_virtual_address/) 32비트를 어떻게 쪼개서 테이블 사이즈를 줄이는지 수학적으로 분해한다.

- <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/322_logical_virtual_address/">논리 주소</a> 분할 (<a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/">10</a> + <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/">10</a> + 12 = 32비트)</strong>:
  - `p1 (10 bits)`: [Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) [Directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) [Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) (대목차 번호)
  - `p2 (10 bits)`: [Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) [Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) (소목차 번호)
  - `d (12 bits)`: Offset (4KB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 내의 정확한 번지)

```text
  +-------------------------------------------------------------------+
  |                 2단계 페이징을 통한 "메모리 다이어트" 동작 원리          |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  [ CR3 레지스터 ] ---> [ 1단계: Page Directory (항상 RAM에 있음) ]       |
  |                       (1024칸 * 4Byte = 딱 4KB 크기!)                 |
  |                                                                   |
  |                       [ 0번 칸 (Code 영역) ] ----> [ 2단계 Page Table 0 ]|
  |                       [ 1번 칸 (텅 빔) ]      ----> (NULL! 메모리 할당 안 함)|
  |                       [ 2번 칸 (텅 빔) ]      ----> (NULL! 메모리 할당 안 함)|
  |                       ...                                         |
  |                       [ 1023번 칸 (Stack) ]  ----> [ 2단계 Page Table X ]|
  |                                                                   |
  |  ★ 기적의 결과:                                                       |
  |   - 1단계 페이징이었다면 무조건 [ 4MB ]의 지도가 램에 있어야 했다.              |
  |   - 2단계 페이징에서는 Code용 테이블(4KB) + Stack용 테이블(4KB) +             |
  |     Root 디렉터리(4KB) = 고작 [ 12KB ]면 지도를 완벽하게 그릴 수 있다!!        |
  |   - 약 99.7%의 메모리 공간 절약 (Memory Saving) 성공!                 |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** "어? 쪼개면 4MB 덩어리가 1024개 생기니까 총 용량은 오히려 $4KB + 4MB$로 더 커지는 거 아니야?" 라고 묻는다면 반만 맞다. 만약 프로세스가 4GB [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)를 1바이트도 안 남기고 100% 꽉 채워 쓴다면, 2단계 [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/)이 1단계보다 오히려 용량을 더 먹는다. 하지만 <strong>현실의 프로그램은 <a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/">가상 메모리</a>의 1%도 쓰지 않는 듬성듬성한(Sparse) 구조</strong>다. 중간에 텅 비어있는 99%의 가상 공간에 대해서는 아예 2단계 테이블(4KB)을 `malloc` 해주지 않기 때문에, 현실 세계에서는 기적적인 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 효과가 나타나는 것이다.

---

### 역방향 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) ([Inverted Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/363_inverted_page_table/))

다단계로 쪼개도 64비트 환경에서는 너무 벅차다. 발상을 180도 뒤집은 아키텍처다.

- **원리**: 기존 방식은 "프로세스마다" 가상 주소 지도를 가졌다. 역방향 방식은 <strong>"시스템 전체에 딱 1개의 물리 램(RAM) 지도"</strong>만 둔다.
- **크기**: 램이 16GB고 프레임이 4KB면, 테이블 크기는 프로세스가 1만 개든 10만 개든 상관없이 무조건 <strong>4백만 칸(약 16MB)으로 영구 고정</strong>된다.
- **검색 방식**: 가상 주소 `p`를 주면, 이 테이블의 꼭대기부터 끝까지 훑으면서 "지금 이 프레임 안에 가상 주소 `p`를 쓰는 프로세스가 있나?"를 $O(N)$으로 뒤져서 프레임 번호를 역산한다. 검색이 너무 느리므로 보통 <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/">해시 테이블</a>(<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/067_hash_table/">Hash Table</a>)</strong>을 결합하여 속도를 보완한다. (PowerPC, IA-64 등에서 제한적 사용)

- **📢 섹션 요약 비유**: [다단계 페이징](/knowledge-base/studynote/02_operating_system/06_memory_management/361_hierarchical_paging/)이 "주민등록번호(가상)를 주면 집 주소(물리)를 찾아주는 책"이라면, 역 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)은 "전국 집 주소록(물리)을 펴놓고, 그 집에 사는 사람 이름(가상)을 찾는 짓"입니다. 책이 딱 한 권이라 공간은 엄청 적게 차지하지만, 찾을 때 숨이 넘어갑니다.

---

## Ⅲ. 비교 및 연결

### [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) 테이블 사이즈 최적화 기법 3대장

| 기법 | 장점 (메모리 관점) | 단점 (속도 관점) | 적용 분야 |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/361_hierarchical_paging/">다단계 페이징</a> (Hierarchical)</strong>| 안 쓰는 테이블을 동적 할당하여 극적인 메모리 절약 | 번역 단계가 깊어져 [Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Walk [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)($O(depth)$) | <strong>모든 현대 <a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/">PC</a> / 서버 OS 표준</strong> |
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/362_hashed_page_table/">해시 페이지 테이블</a> (Hashed)</strong> | 64비트 주소 공간에서 테이블 크기를 [해시 충돌](/knowledge-base/studynote/05_database/04_transactions_concurrency/563_hash_collision_chaining_linear_probing/) 수준으로 [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/) | [해시 충돌](/knowledge-base/studynote/05_database/04_transactions_concurrency/563_hash_collision_chaining_linear_probing/)([Collision](/knowledge-base/studynote/05_database/04_transactions_concurrency/563_hash_collision_chaining_linear_probing/)) 해결을 위한 체이닝([Chaining](/knowledge-base/studynote/12_it_management/03_ea_isp/887_chaining/)) 탐색 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 주소 공간이 극도로 큰 시스템 |
| <strong>역방향 <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/">페이지 테이블</a> (Inverted)</strong>| 프로세스 수와 무관하게 시스템 램 크기에만 비례 (최소 공간) | 주소를 역으로 찾아야 해서 극단적인 [탐색 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/) $O(N)$ 소모 | 일부 특수 아키텍처 |

### 과목 융합 관점

- <strong>컴퓨터구조 (<a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/">CA</a>) - <a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/433_memory_wall/">Memory Wall</a></strong>: [다단계 페이징](/knowledge-base/studynote/02_operating_system/06_memory_management/361_hierarchical_paging/)은 메모리 용량 부족 문제를 해결했지만, '메모리 장벽'이라는 재앙을 불렀다. 4단계 [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/)(x86-64)에서 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) Miss가 나면, CPU는 진짜 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 1번을 읽기 위해 RAM(Root $\rightarrow$ Dir $\rightarrow$ Mid $\rightarrow$ PT)을 무려 4번이나 추가로 다녀와야 한다([Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Walk). 평소 100ns 걸리던 메모리 접근 시간이 순간적으로 500ns로 뛰어버린다.
- **TLB의 절대적 권력**: 이 5배의 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 막는 유일한 구원자가 바로 CPU 내부의 캐시인 <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/">TLB</a></strong>다. [다단계 페이징](/knowledge-base/studynote/02_operating_system/06_memory_management/361_hierarchical_paging/)이 실전에서 쓸만한 이유는, [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) [적중률](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/264_hit_ratio/)([Hit Ratio](/knowledge-base/studynote/02_operating_system/06_memory_management/359_effective_access_time/))이 99%를 넘기 때문에 "어차피 100번에 1번만 [Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Walk를 갈 거면 이 정도 손해(Trade-off)는 감수하자"는 하드웨어와 소프트웨어의 도박이 성공했기 때문이다.

- **📢 섹션 요약 비유**: 짐([페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/))을 줄이기 위해 택배를 4번 갈아타는 끔찍한 국도([다단계 페이징](/knowledge-base/studynote/02_operating_system/06_memory_management/361_hierarchical_paging/))를 만들었습니다. 하지만 우리가 평소에 타고 다니는 하이패스 직통 고속도로([TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/))가 워낙 빵빵해서, 1년에 한두 번 국도를 탈 때의 짜증 정도는 가볍게 눈감아 주고 있는 상황입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — 클라우드 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a>(<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/">Out Of Memory</a>) 킬러의 숨겨진 주범 (<a href="/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/">Page Table</a> Bloat)</strong>: Node.js/Python 기반의 웹 크롤러 프로세스 1,000개를 도커로 띄웠다. 프로세스당 실제 사용하는 메모리는 10MB밖에 안 되는데, 노드의 32GB 램이 꽉 차서 OOM이 났다.
   - **원인 분석**: `cat /proc/meminfo | grep PageTables`를 쳐보니, [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 자체가 10GB를 먹고 있었다! [다단계 페이징](/knowledge-base/studynote/02_operating_system/06_memory_management/361_hierarchical_paging/)이라 할지라도, 프로세스를 너무 많이(1,000개) 띄우거나, [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 공간 이곳저곳(힙 끝, [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 끝, [mmap](/knowledge-base/studynote/02_operating_system/11_exam_summary/749_memory_mapped_file_mmap/) 공간)에 산발적으로([Fragmentation](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 할당하면 그 성긴 공간들을 매핑하기 위해 2단계, 3단계 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)들이 무수히 동적 할당되어 [메모리 누수](/knowledge-base/studynote/02_operating_system/10_security/612_memory_leak_detection/) 뺨치는 오버헤드를 낳는다 ([Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) Bloat).
   - **대응 (아키텍처 적용)**: 쓸데없이 멀티프로세스로 띄우지 말고, 주소 공간(CR3) 하나를 공유하는 <strong>멀티스레드(Multi-Thread)</strong>나 <strong>비동기 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/">이벤트 루프</a>(Coroutines)</strong> 모델로 아키텍처를 변경해야 한다. 스레드는 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)을 100% 공유하므로 스레드가 1,000개 떠도 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 용량은 1개분(수 MB)으로 완벽하게 다이어트된다.

2. <strong>시나리오 — <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a>(<a href="/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/">Oracle</a>, SAP HANA) 성능을 위한 <a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/517_huge_page/">Huge Page</a> 도입</strong>: 위의 문제와 정반대로, [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)이 너무 많아서 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 캐시 미스가 폭발하고 시스템 성능이 안 나온다.
   - <strong>해결책 (<a href="/knowledge-base/studynote/02_operating_system/06_memory_management/371_huge_pages/">Huge Pages</a>)</strong>: 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 기본 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)(4KB) 대신 <strong>2MB (<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/517_huge_page/">Huge Page</a>)</strong>를 적용한다.
   - **다단계 테이블 파괴 효과**: 2MB [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 쓰면 x86-64의 4단계 [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) 트리에서 마지막 4단계 테이블(PTE) 층이 아예 사라져 버리고 3단계(PMD)에서 끝난다. 주소 번역 단계가 1단계 줄어들어 [Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Walk 속도가 25% 빨라지며, 1,000개의 매핑을 기억해야 할 테이블이 2개로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)되므로 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 자체가 먹는 메모리 용량(Bloat)도 기적적으로 줄어든다. 거대 서버 엔지니어링의 치트키다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 메모리 테이블 오버헤드 최적화 아키텍처 플로우              |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [서버 튜닝 중, 페이지 테이블 용량과 TLB 미스로 인한 병목 발견]              |
  |                |                                                  |
  |                v                                                  |
  |      가상 메모리를 너무 넓게 휘저어 쓰는(Sparse) 프로세스들이 수만 개 떠 있는가? |
  |          +- 예 ------> [멀티프로세스 -> 멀티스레드 아키텍처 전환]       |
  |          |            (스레드 간 페이지 테이블 공유로 테이블 용량 오버헤드 박살냄)|
  |          +- 아니오 (거대한 프로세스 1개가 수백 GB를 통째로 쓰고 있다)       |
  |                |                                                  |
  |                v                                                  |
  |      [Huge Page(2MB / 1GB) 튜닝 강력 권고]                           |
  |      - 효과 1: 다단계 트리의 높이(Depth)가 1~2계층 줄어 탐색 속도 증가.  |
  |      - 효과 2: 페이지 테이블 자체가 점유하는 커널 메모리 용량이 1/500로 극감.|
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** "메모리 32GB 꽂았는데 왜 부족하지?"라고 할 때, 개발자들은 자기 앱의 `User Space` 메모리릭만 의심한다. 시스템 아키텍트는 `Kernel Space`에 숨어있는 <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/">Page Table</a></strong>이라는 거대한 괴물을 볼 줄 알아야 한다. 이 괴물은 프로세스가 늘어날수록 조용히, 그러나 기하급수적으로 서버의 피(RAM)를 빨아먹는다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong>KSM (<a href="/knowledge-base/studynote/02_operating_system/10_security/631_ksm_kernel_samepage_merging/">Kernel Samepage Merging</a>)</strong>: 수백 개의 가상머신([VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))을 띄우는 [KVM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/) 클라우드 환경에서, 각 VM이 윈도우 OS를 띄우느라 들고 있는 똑같은 내용의 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)들(DLL 등)을 백그라운드 스레드가 스캔하여 물리 프레임 하나로 합치고(Merge) [다단계 페이지 테이블](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/289_multilevel_page_table/) 포인터를 하나로 모아주어 물리 램을 엄청나게 절약해 주는(Overcommit) KSM 데몬을 활성화했는가?

- **📢 섹션 요약 비유**: 수만 권의 책(메모리)을 관리하려고 두꺼운 엑셀 장부(단일 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/))를 만들었더니 장부 놓을 자리도 부족해졌습니다. 그래서 장부를 카테고리별 작은 수첩(다단계)으로 나누고, 아예 책들을 두꺼운 합본([Huge Page](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/517_huge_page/))으로 묶어버리거나 같은 책은 하나로 합쳐버려서(KSM) 장부 관리를 편하게 만든 도서관의 진화입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 1단계 (단일) [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) | 다단계 (Hierarchical) [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (테이블 크기)**| 32비트 기준 무조건 프로세스당 4MB 할당 | **사용하는 양에 비례해 수 KB~MB 동적 할당**| OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리 낭비 90% 이상 절감 |
| **정량 (변환 속도)** | 1번의 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 인덱싱 (매우 빠름) | 트리 구조로 4번 읽음 ([Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Walk 느림) | (단점) 속도를 내어주고 공간을 취함 |
| **정성 (확장성)** | 64비트 환경에서 아예 구현 불가능 | 무한한 [가상 주소 공간](/knowledge-base/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/) 쪼개기 가능 | x86-64 및 최신 칩셋 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)의 유일한 대안 |

### 미래 전망
- <strong>5-Level <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/">Paging</a> (인텔 Ice Lake 이후)</strong>: 빅데이터와 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 붐으로 인해 물리적 서버 메모리가 수십 테라바이트를 넘어가자, 4단계(4-level, 48비트 가상 주소, 256TB 한계)로도 모자라게 되었다. 그래서 루트 디렉터리를 한 번 더 감싸는 5단계 [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/)(57비트 가상 주소, 128PB 한계)이 메인라인 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 도입되었다. 이는 공간 확장을 위해 [탐색 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))을 한 번 더 희생한 하드웨어의 눈물겨운 땜질이다.

### 결론
[다단계 페이지 테이블](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/289_multilevel_page_table/)([Hierarchical Paging](/knowledge-base/studynote/02_operating_system/06_memory_management/361_hierarchical_paging/)) 사이즈 줄이기는 컴퓨터 과학의 가장 위대한 트레이드오프인 <strong>"공간(Memory)을 얻기 위해 시간(Time)을 판다"</strong>는 명제를 가장 극단적으로 보여주는 건축물이다. [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) 시스템을 구하기 위해 무려 4~5번의 포인터 추적(Pointer Chasing)이라는 미친 속도 저하를 허락했고, 그 떨어진 속도를 다시 메꾸기 위해 TLB라는 비싼 하드웨어 캐시를 발라버리는 거대한 폭탄 돌리기의 연속이었다. 하지만 이 위태로운 곡예 덕분에, 오늘날 64비트 시대의 프로그램들은 우주만큼 넓은 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 공간을 에러 하나 없이 공짜로 펑펑 쓸 수 있게 되었다.

- **📢 섹션 요약 비유**: 방이 좁다고 침대를 접이식(다단계 테이블)으로 바꿨습니다. 잘 때마다 침대를 펴고 접는 건([Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Walk) 너무 귀찮지만, 덕분에 방을 10배로 넓게 쓸 수 있습니다. 그리고 평소에는 낮잠용 소파([TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/))에서 자니까 귀찮음도 별로 못 느낍니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) 시스템 프레임 테이블 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) [적중률](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/264_hit_ratio/) 캐시 속도 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) 재발 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/) ([Demand Paging](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[TLB 적중률 캐시 속도]
    |
    v
[다단계 페이지 테이블 사이즈 줄이기 (Hierarchical Paging Multi Level)]
    |
    +---> [세그멘테이션 외부 단편화 재발]
    +---> [요구 페이징 (Demand Paging)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 전 세계 골목길이 다 적힌 엄청나게 두꺼운 지도책(1단계 테이블)을 가방에 넣고 다니려니까 허리가 부러질 것 같았어요.
2. 그래서 책을 다 찢어버리고, '국가 이름표(1단계 목차)'만 남겼어요. 내가 미국에 놀러 갈 때만 동사무소에 가서 '미국 상세 지도(2단계 목차)'를 뽑아왔죠! ([다단계 페이징](/knowledge-base/studynote/02_operating_system/06_memory_management/361_hierarchical_paging/))
3. 이렇게 하니까 가방은 엄청 가벼워졌어요(메모리 절약). 지도를 찾을 때 단계를 두 번 거쳐야 해서 조금 느려졌지만, 그래도 허리가 안 아픈 게 최고랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 717 / 800

<- **이전**: [716. TLB 적중률 캐시 속도 (TLB Hit Ratio Cache Speed)](/knowledge-base/studynote/02_operating_system/11_exam_summary/716_tlb_hit_ratio_cache_speed/)
**다음**: [718. 세그멘테이션 외부 단편화 재발 (Segmentation External Fragmentation)](/knowledge-base/studynote/02_operating_system/11_exam_summary/718_segmentation_external_fragmentation/) ->

---
