---
title: 734. FAT 방식 연결 할당 최적화 (Fat File Allocation Table Optimization)
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[525_fat_file_allocation_table|FAT]]([[525_fat_file_allocation_table|File Allocation Table]])는 기존 [[524_linked_allocation|연결 할당]]([[524_linked_allocation|Linked Allocation]])의 가장 치명적인 단점이었던 "다음 블록을 찾기 위해 디스크를 계속 읽어야 하는 탐색 [[015_지연_데이터_관점|지연]]([[467_disk_access_time|Seek Time]])"을 해결하기 위해, **각 블록의 '포인터'들만 모아서 하나의 거대한 표(Table)로 빼내어 메모리에 올려버린 혁신적인 [[501_file_definition_logical_record|파일]] 시스템**이다.
> 2. **메커니즘 (테이블 분리)**: 디스크의 [[001_dikw_pyramid|데이터]] 블록 안에는 순수하게 [[001_dikw_pyramid|데이터]]만 남겨두고, "1번 블록 다음은 5번, 5번 다음은 9번"이라는 링크 정보는 디스크 맨 앞의 [[525_fat_file_allocation_table|FAT]] 테이블에 [[055_array|배열]] 형태로 기록한다. OS는 부팅 시 이 [[525_fat_file_allocation_table|FAT]] 테이블을 램(RAM)에 캐싱한다.
> 3. **가치**: 포인터 추적(Pointer Chasing)이 디스크가 아닌 램에서 빛의 속도로 이루어지므로, [[524_linked_allocation|연결 할당]]의 장점([[342_external_fragmentation|외부 단편화]] 0%)을 그대로 유지하면서도 치명적이었던 **직접 접근(Random Access) 속도를 O(1)에 가깝게 끌어올린 MS-DOS와 Windows의 뼈대 기술**이 되었다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **[[525_fat_file_allocation_table|FAT]] ([[525_fat_file_allocation_table|File Allocation Table]])**: 디스크 내의 모든 클러스터(블록)들의 연결 상태(다음 블록 번호, 빈 블록 여부, [[501_file_definition_logical_record|파일]] 끝 표시 등)를 기록해 둔 1차원 [[055_array|배열]] 형태의 테이블.
  - **클러스터 (Cluster)**: [[525_fat_file_allocation_table|FAT]] [[501_file_definition_logical_record|파일]] 시스템이 디스크를 관리하는 기본 단위 (보통 4KB ~ 32KB).

- **필요성 ([[524_linked_allocation|연결 할당]]의 디스크 I/O 병목 극복)**: 
  - 구형 [[524_linked_allocation|연결 할당]] 방식은 1번 블록을 읽어야 그 끝에 적힌 2번 블록의 주소를 알 수 있었고, 2번을 읽어야 3번을 알 수 있었다.
  - 만약 영화 [[501_file_definition_logical_record|파일]]의 1,000번째 블록부터 보고 싶으면? 하드디스크를 무려 999번이나 읽고 버려야 했다. 탐색에만 수 초가 걸렸다.
  - **해결책**: "[[001_dikw_pyramid|데이터]]와 포인터를 분리하자! 포인터들만 싹 다 모아서 표([[525_fat_file_allocation_table|FAT]])를 만든 다음, 컴퓨터가 켜질 때 이 표를 램(RAM)에 올려버리면 1,000번째 블록 주소도 램 안에서 0.001초 만에 찾을 수 있잖아!"

  - **기존 [[524_linked_allocation|연결 할당]] (보물찾기 쪽지)**: 1번 나무 밑을 파보면 "다음 보물은 5번 바위 밑에 있음" 쪽지가 나온다. 5번 바위 밑을 파야 "9번 우물 밑" 쪽지가 나온다. 100번째 보물을 찾으려면 99번이나 땅을 파야 한다 (느림).
  - **[[525_fat_file_allocation_table|FAT]] 방식 (마스터 지도)**: 마을 이장님(RAM)이 아예 **'보물 연결 지도([[525_fat_file_allocation_table|FAT]])'**를 통째로 들고 있다. 100번째 보물이 어딨는지 지도를 눈으로 쓱 따라가 본 뒤(빛의 속도), "아, 100번째 보물은 77번 우물에 있네" 하고 바로 77번 우물로 직행해서 땅을 딱 한 번만 파면 된다.

- **발전 과정**:
  1. **FAT12**: 플로피 디스크 시절 (클러스터 개수 4,096개 한계).
  2. **FAT16 / FAT32**: MS-DOS와 Windows 95 시절. [[359_usb|USB]] 메모리의 영원한 표준 포맷.
  3. **exFAT**: FAT32의 4GB 단일 [[501_file_definition_logical_record|파일]] 크기 제한을 깬 최신 [[256_flash_memory|플래시 메모리]] 전용 포맷.

- **📢 섹션 요약 비유**: 책의 내용 뒤에 "다음 내용은 50페이지로"라고 써두는 대신, 아예 책 맨 앞장에 목차와 흐름도를 통째로 빼놓아 독자가 책장을 펄럭이지 않고도 한눈에 이야기의 흐름을 파악하게 만든 편집의 마술입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[525_fat_file_allocation_table|FAT]] 테이블 구조와 [[501_file_definition_logical_record|파일]] 탐색 시뮬레이션

디스크의 0번 블록에 [[525_fat_file_allocation_table|FAT]] 테이블이 저장되어 있고, 부팅 시 RAM에 올라와 있다.
[[506_directory_structure_symbol_table|디렉터리]]에는 `[파일명: A.txt | 시작 블록: 10]` 이라고 적혀 있다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 FAT (File Allocation Table)의 링크 추적 원리           │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  [ 디렉터리 ]                                                      │
  │   - 파일 "A.txt", 시작 블록 번호 = [ 10 ]                           │
  │                                                                   │
  │  [ RAM에 올라와 있는 FAT 테이블 (배열 인덱스 = 블록 번호) ]             │
  │                                                                   │
  │   인덱스(블록) │ FAT 배열에 적힌 값 (다음 블록 번호)                    │
  │  ─────────┼──────────────────────────────────────────         │
  │      ...    │ ...                                                │
  │       10    │  25  ◀── (A.txt의 시작점 10번. 다음은 25번!)          │
  │       25    │  17  ◀── (A.txt의 2번째 덩어리. 다음은 17번!)         │
  │       17    │  EOF ◀── (A.txt의 3번째 덩어리. 파일 끝(End Of File))│
  │                                                                   │
  │  [ 동작 결과 ]                                                     │
  │   - OS는 디스크를 한 번도 안 읽고, RAM 안에서만 테이블을 뒤져           │
  │     A.txt가 "10 -> 25 -> 17" 순서로 저장되어 있음을 알아냈다!            │
  │   - 만약 3번째 블록을 원하면 바로 디스크 17번 블록으로 헤드를 옮기면 끝!    │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 테이블의 값은 딱 3종류다. **다음 블록 번호**, **빈 블록 표시(Free, 보통 0)**, **[[501_file_definition_logical_record|파일]]의 끝 표시(EOF, 보통 -1이나 특수기호)**. 새로운 [[501_file_definition_logical_record|파일]]을 쓸 때는 테이블을 쫙 스캔해서 0(Free)인 [[154_database_index_b_tree_search_optimization|인덱스]]를 찾아 그 번호에 [[001_dikw_pyramid|데이터]]를 쓰고 포인터를 이어주면 끝이다.

---

### FAT32의 치명적 한계: 4GB 장벽

가장 유명한 [[359_usb|USB]] 포맷인 FAT32는 왜 [[501_file_definition_logical_record|파일]] 1개당 4GB밖에 저장을 못 할까?
- FAT32에서 [[501_file_definition_logical_record|파일]]의 크기를 기록하는 [[506_directory_structure_symbol_table|디렉터리]] 엔트리의 '[[501_file_definition_logical_record|파일]] 크기([[501_file_definition_logical_record|File]] Size)' 필드가 정확히 **32비트(4바이트)**로 설계되어 있기 때문이다.
- 32비트로 표현할 수 있는 최대 숫자는 $2^{32} - 1$ = `4,294,967,295 Byte` = **약 4GB** 다.
- 디스크 용량이 1TB가 남아돌아도, [[501_file_definition_logical_record|파일]] 시스템의 껍데기([[506_directory_structure_symbol_table|디렉터리]] 구조)가 4GB까지만 셀 수 있어서 못 넣는 어처구니없는 수학적 한계다. (이를 해결하기 위해 64비트 크기 필드를 쓰는 exFAT이 등장했다.)

- **📢 섹션 요약 비유**: [[525_fat_file_allocation_table|FAT]] 테이블은 기차표와 같습니다. 10번 칸에 앉은 사람에게 "당신 다음 일행은 25번 칸에 있어요"라고 표에 적어주는 겁니다. 역장(OS)은 열차 밖에서 표만 쓱 보고 일행이 어디 어디 흩어져 있는지 완벽하게 파악합니다.

---

## Ⅲ. 비교 및 연결

### [[525_fat_file_allocation_table|FAT]] vs UNIX i-node ([[526_indexed_allocation|색인 할당]]) 비교

세계에서 가장 많이 쓰이는 두 [[501_file_definition_logical_record|파일]] 시스템 뼈대의 정면승부다.

| 비교 항목 | [[525_fat_file_allocation_table|FAT]] (Windows / MS-DOS) | i-node (UNIX / Linux ext4) |
|:---|:---|:---|
| **할당 방식** | **[[524_linked_allocation|연결 할당]] (Linked)의 진화형** | **[[526_indexed_allocation|색인 할당]] ([[181_indexed_addressing|Indexed]]) 기반** |
| **[[012_metadata|메타데이터]] 위치**| **디스크 맨 앞**에 하나의 거대한 [[525_fat_file_allocation_table|FAT]] 테이블 집중 | [[501_file_definition_logical_record|파일]] 1개당 **개별적인 i-node** 블록 존재 |
| **장점** | 구조가 단순해 메모리가 적은 기기([[359_usb|USB]], 디카)에 유리 | 거대한 [[501_file_definition_logical_record|파일]] 탐색과 [[014_concurrency|동시성]] 제어에 압도적 유리 |
| **단점 (오버헤드)**| 디스크가 커지면 [[525_fat_file_allocation_table|FAT]] 테이블 자체도 거대해져 RAM 낭비 | [[501_file_definition_logical_record|파일]]이 작아도 무조건 i-node를 1개씩 소모 (inode 고갈) |
| **안정성 (Crash)**| [[525_fat_file_allocation_table|FAT]] 테이블(1개)이 깨지면 **디스크 전체 [[001_dikw_pyramid|데이터]] 증발** | 특정 i-node가 깨져도 **해당 [[501_file_definition_logical_record|파일]] 하나만 날아감** |

### 과목 융합 관점

- **자료구조 ([[001_dikw_pyramid|Data]] Structure)**: FAT는 램 안에서 일어나는 '[[055_array|배열]] [[154_database_index_b_tree_search_optimization|인덱스]] 기반의 [[008_단방향_반이중_전이중|단방향]] [[056_linked_list|연결 리스트]](Singly [[056_linked_list|Linked List]])'다. 리스트의 치명적 단점은 역방향 탐색이 안 된다는 것이다. 동영상 뒤로 가기를 누르면 FAT는 다시 [[501_file_definition_logical_record|파일]]의 시작점부터 링크를 타고 내려와야 한다. (물론 램 속도라 빠르긴 하지만 연산 낭비다.)
- **컴퓨터구조 ([[089_contract_account_smart_contract|CA]])**: [[525_fat_file_allocation_table|FAT]] 시스템의 가장 무서운 적은 **"정전([[069_type_1_2_error_statistical_power|Power]] Loss)"**이다. OS가 [[501_file_definition_logical_record|파일]]을 쓰면서 RAM에 있는 [[525_fat_file_allocation_table|FAT]] 테이블만 갱신해 두고, 아직 디스크의 실제 [[525_fat_file_allocation_table|FAT]] 구역에 Flush 하지 않았는데 정전이 나면 어떻게 될까? 새로 쓴 [[501_file_definition_logical_record|파일]]은 '고아(Orphan)'가 되어 디스크 용량만 차지하는 유령(Lost Cluster)이 된다. 이를 [[658_ir_recovery|복구]]하는 툴이 윈도우의 `chkdsk` 다.

- **📢 섹션 요약 비유**: FAT는 한 권의 두꺼운 주소록(단일 실패 지점)에 전 국민의 주소를 다 적어놓은 것이라 주소록을 잃어버리면 나라가 망합니다. i-node는 동사무소마다([[501_file_definition_logical_record|파일]]마다) 따로따로 주민등록등본을 관리하는 [[136_variance|분산]] 구조라 훨씬 튼튼합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — 블랙박스/[[933_cctv|CCTV]] 메모리 카드의 잦은 포맷 요구 ([[525_fat_file_allocation_table|FAT]] 손상)**: 차량용 블랙박스의 SD 카드(FAT32)가 한 달에 한 번씩 "SD 카드를 포맷하십시오" 에러를 뿜음.
   - **원인 분석**: [[525_fat_file_allocation_table|FAT]] 구조의 태생적 한계다. [[501_file_definition_logical_record|파일]] [[001_dikw_pyramid|데이터]]는 디스크 곳곳에 쓰이지만, **모든 [[501_file_definition_logical_record|파일]]의 링크 정보는 디스크 맨 앞부분(Sector 0 근처)의 '[[525_fat_file_allocation_table|FAT]] 영역'에 집중적으로 덮어쓰기** 된다. [[256_flash_memory|플래시 메모리]](SD카드)는 [[289_cqrs_db|쓰기]] 수명이 정해져 있는데, 맨 앞의 [[525_fat_file_allocation_table|FAT]] 영역만 수십만 번 덮어써지면서 해당 낸드 셀이 물리적으로 타버린 것이다([[479_wear_leveling|Wear Leveling]] 한계 돌파). FAT가 깨지니 [[501_file_definition_logical_record|파일]] 시스템 전체가 죽었다.
   - **아키텍처 적용**: 이를 막기 위해 [[525_fat_file_allocation_table|FAT]] 시스템은 `FAT1`과 똑같은 복사본인 `FAT2`를 바로 뒤에 무조건 [[555_backup_and_restore_strategy|백업]]용으로 기록한다. 하지만 실시간 녹화 중 시동이 꺼지는 가혹한 블랙박스 환경에서는 [[456_dual_redundancy|이중화]]도 뚫린다. 따라서 최근 블랙박스들은 FAT를 버리고 덮어쓰기 집중을 막는 고유의 TAT(Time Allocation Table) 포맷을 써서 수명을 10배 늘리고 있다.

2. **시나리오 — 대용량 [[359_usb|USB]] 메모리의 exFAT 포맷 전환 필요성**: 64GB [[359_usb|USB]] 메모리를 샀는데 5GB짜리 4K 영화가 안 들어간다. "[[501_file_definition_logical_record|파일]]이 너무 큽니다" 에러 발생.
   - **대응 (기술사적 가이드)**: 윈도우는 32GB 이하 USB를 기본적으로 FAT32로 포맷한다. 위에서 배운 대로 FAT32의 [[501_file_definition_logical_record|파일]] 크기 한계는 4GB다. 이를 해결하려면 윈도우/맥/리눅스에서 모두 호환되면서 64비트 크기 필드를 지원하여 단일 [[501_file_definition_logical_record|파일]] 16EB(엑사바이트)까지 넣을 수 있는 **exFAT (Extended [[525_fat_file_allocation_table|FAT]])** 형식으로 포맷해야 한다. (현재 스마트폰 SD카드의 표준)

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 이동식 저장 매체(USB/SD카드) 파일 시스템 선택 플로우        │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [새로운 USB 메모리 또는 외장 하드를 포맷하려고 함]                        │
  │                │                                                  │
  │                ▼                                                  │
  │      이 드라이브를 Windows와 Mac OS, 스마트TV 등에 번갈아 가며 꽂을 것인가?   │
  │          ├─ 예 ─────▶ [NTFS와 APFS는 상호 호환성 문제로 배제]           │
  │          │            (Mac은 NTFS 쓰기 불가, Win은 APFS 읽기 불가)      │
  │          │            대책: [exFAT] 포맷 적용. 완벽한 크로스플랫폼 호환성 보장.│
  │          └─ 아니오 (오직 윈도우 서버/PC에서만 영구적으로 박아두고 쓴다)      │
  │                │                                                  │
  │                ▼                                                  │
  │      [NTFS 포맷 강력 권장]                                             │
  │      - FAT 계열은 저널링(Journaling) 기능이 없어 정전 시 데이터가 100% 날아감.│
  │      - NTFS는 색인 할당(MFT) 기반이라 보안(ACL), 저널링, 압축 기능을 완벽 지원함.│
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** "그냥 아무거나 포맷하면 되는 거 아냐?" 아니다. [[501_file_definition_logical_record|파일]] 시스템은 운영체제와 하드웨어가 소통하는 언어다. exFAT은 마이크로소프트가 [[256_flash_memory|플래시 메모리]]를 위해 FAT의 군더더기를 쫙 빼고(오버헤드 최소화) 배터리를 아끼도록 만든 최고의 모바일용 포맷이다. 반면 서버에 exFAT을 쓰면 정전 한 번에 DB [[501_file_definition_logical_record|파일]]이 몽땅 날아가는 재앙을 맞는다.

### 도입 [[435_checklist_based_testing|체크리스트]]
- **클러스터 크기(Cluster Size, 할당 단위) 튜닝**: 포맷할 때 '할당 단위 크기'를 고르는 옵션이 나온다. 이게 바로 페이징의 딜레마다.
  - 클러스터를 32KB로 큼직하게 잡으면? [[525_fat_file_allocation_table|FAT]] 테이블 길이가 짧아져서 탐색이 엄청 빠르다. 하지만 1KB 텍스트 [[501_file_definition_logical_record|파일]]을 저장해도 31KB가 버려지는 **[[341_internal_fragmentation|내부 단편화]]([[341_internal_fragmentation|Internal Fragmentation]])** 폭탄을 맞는다.
  - 주로 용량이 큰 동영상을 담는 하드라면 할당 단위를 32KB~64KB로 최대화하고, 자잘한 문서 위주라면 4KB(디폴트)로 세팅하는 센스가 엔지니어의 기본이다.

- **📢 섹션 요약 비유**: FAT는 전 세계 모든 사람이 쓰는 공용어(영어)와 같습니다. 깊이 있는 문학(보안, 저널링)을 표현하긴 부족하지만, 윈도우, 맥, 스마트폰, 자동차 내비게이션 어디에 꽂아도 100% 말이 통하는 최강의 이식성을 자랑합니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 일반 [[524_linked_allocation|연결 할당]] (Linked) | [[525_fat_file_allocation_table|FAT]] 방식 [[524_linked_allocation|연결 할당]] | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (탐색 속도)** | [[501_file_definition_logical_record|파일]] 끝을 찾으려면 수백 번 디스크 I/O | **디스크 I/O 없이 RAM에서 $O(N)$ 탐색**| [[501_file_definition_logical_record|파일]] 탐색 속도 수백 배~수천 배 폭증 |
| **정량 (블록 활용)** | 포인터 4바이트 때문에 2의 승수 깨짐 | 포인터를 밖으로 빼서 **블록 100% [[001_dikw_pyramid|데이터]] 활용** | 메모리 정렬(Alignment) 최적화로 I/O 가속 |
| **정성 ([[001_dikw_pyramid|데이터]] 보존)**| 중간 블록 뻑나면 뒷부분 통째로 유실 | **[[525_fat_file_allocation_table|FAT]] 테이블만 [[555_backup_and_restore_strategy|백업]]([[456_dual_redundancy|이중화]])해 두면 안전**| [[001_dikw_pyramid|데이터]] [[658_ir_recovery|복구]] 가능성 비약적 상승 |

### 미래 전망
- **FAT의 쇠퇴와 [[032_firmware|펌웨어]] 종속**: 서버와 [[164_pc|PC]] 세계에서 FAT는 20년 전에 이미 죽은 기술이다 (NTFS, ext4에 밀림). 하지만 [[101_iot_concept|IoT]]([[101_iot_concept|사물인터넷]]), 드론, 라즈베리 파이 같은 마이크로 생태계에서는 가볍다는 이유 하나만으로 절대 권력을 유지하고 있다. 앞으로도 운영체제가 없는 Bare-metal 환경이나 임베디드 칩셋의 [[032_firmware|펌웨어]] 업데이트 통로로는 영원히 살아남을 포맷이다.

### 결론
[[525_fat_file_allocation_table|FAT]]([[525_fat_file_allocation_table|File Allocation Table]])는 [[524_linked_allocation|연결 할당]]의 치명적 약점인 "디스크 탐색 [[015_지연_데이터_관점|지연]]"을 **"[[012_metadata|메타데이터]]를 모조리 램에 올려버린다"**는 대담하고 무식한 방법으로 해결한 1970년대 마이크로소프트의 역작이다. 이 기법은 디스크가 작았던 시절에는 최고의 묘수였으나, 디스크가 테라바이트급으로 커지자 램을 지나치게 갉아먹는 괴물로 전락해 버렸다. 그럼에도 불구하고 FAT32와 exFAT은 그 단순함과 직관성 덕분에 세상의 모든 이종 기기(스마트폰, 카메라, [[164_pc|PC]], 자동차)를 이어주는 [[359_usb|USB]] 스토리지의 유일무이한 표준으로 역사에 영원히 남게 되었다.

- **📢 섹션 요약 비유**: FAT는 낡고 오래된 마을 이장님입니다. 현대적인 빌딩 숲(서버)에서는 최첨단 보안 시스템(NTFS)에 자리를 내주었지만, 시골 마을([[359_usb|USB]], 디카)에서는 누가 언제 이사 왔는지 장부 하나만 보고 1초 만에 다 꿰뚫어 보는 여전히 가장 빠르고 믿음직한 정보통입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[380_garbage_collection|가비지 컬렉션]] 블록 지우기 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[501_file_definition_logical_record|파일]] 시스템 연속, 연결, [[526_indexed_allocation|색인 할당]] | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| i-node 직접/간접 포인터 [[154_database_index_b_tree_search_optimization|인덱스]] | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[511_hard_link|하드 링크]] / [[512_symbolic_link|심볼릭 링크]] 차이 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[파일 시스템 연속, 연결, 색인 할당]
    │
    ▼
[FAT 방식 연결 할당 최적화 (Fat File Allocation Table Optimization)]
    │
    ├──▶ [i-node 직접/간접 포인터 인덱스]
    └──▶ [하드 링크 / 심볼릭 링크 차이]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 철수가 보물찾기를 하는데 "다음 보물은 2번 나무 밑, 그다음은 5번 바위 밑..." 이렇게 땅을 파봐야만 다음 장소를 알 수 있었어요 (기존 [[524_linked_allocation|연결 할당]]). 땅 파느라 너무 힘들었죠.
2. 그래서 마을 촌장님이 아예 종이 한 장에 "1번 다음은 2번, 2번 다음은 5번"이라는 **마스터 지도([[525_fat_file_allocation_table|FAT]] 테이블)**를 싹 그려서 철수에게 줬어요!
3. 철수는 이제 삽질을 10번 할 필요 없이, 지도만 눈으로 쓱 훑어보고 마지막 보물이 있는 100번 나무로 바로 뛰어가서 땅을 한 번만 파면 된답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 734 / 800

← **이전**: [[733_file_system_allocation_contiguous_linked_indexed|733. 파일 시스템 연속, 연결, 색인 할당 (File System Allocation Contiguous Linked Indexed)]]
**다음**: [[735_inode_direct_indirect_pointer_index|735. i-node 직접/간접 포인터 인덱스 (Inode Direct Indirect Pointer Index)]] →

---
