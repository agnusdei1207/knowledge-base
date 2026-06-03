---
title: 337. 표준 스와핑 (전체 프로세스) vs 페이징 시스템 스와핑 (페이지 단위) (Standard Vs Paging Swapping)
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 표준 [[335_swapping|스와핑]](Standard [[335_swapping|Swapping]])은 100MB짜리 **프로세스 전체**를 통째로 디스크와 메모리 사이로 이동시키는 무식하고 고전적인 방식이며, [[259_paging|페이징]] 시스템 [[335_swapping|스와핑]]([[259_paging|Paging]] System [[335_swapping|Swapping]])은 전체 중 당장 필요한 **4KB 크기의 [[286_page_frame|페이지]] 조각**만 잘게 썰어서 이동시키는 현대적인 정밀 기법이다.
> 2. **가치**: [[259_paging|페이징]] [[335_swapping|스와핑]]([[255_demand_paging|요구 페이징]])은 한 번에 이동하는 [[001_dikw_pyramid|데이터]]의 양을 극적으로 줄여, [[335_swapping|스와핑]] 시 발생하는 치명적인 디스크 I/O 병목(Stuttering)을 해결하고 [[673_multiprogramming_bottleneck_resource|다중 프로그래밍]]의 효율을 한 차원 끌어올렸다.
> 3. **융합**: 오늘날 우리가 부르는 리눅스나 윈도우의 "[[335_swapping|스와핑]](Swap)"은 100% [[259_paging|페이징]] 기반의 [[286_page_frame|페이지]] [[335_swapping|스와핑]]([[286_page_frame|Page]]-out / [[286_page_frame|Page]]-in)을 의미하며, 이는 [[381_virtual_memory|가상 메모리]]([[381_virtual_memory|Virtual Memory]]) 아키텍처와 완벽하게 융합되어 동작한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 메모리가 꽉 찼을 때 [[001_dikw_pyramid|데이터]]를 하드디스크(백킹 스토어)로 쫓아내는 철학은 같지만, '어떤 단위(Unit)로 쫓아낼 것인가'에 따라 **전체 프로세스 단위**의 표준 [[335_swapping|스와핑]]과 **고정 크기 블록 단위**의 [[259_paging|페이징]] [[335_swapping|스와핑]]으로 나뉜다.
- **필요성**: 1970년대 초창기 [[001_operating_system_purpose|운영체제]]는 프로그램이 연속된 하나의 덩어리로 메모리에 적재되어야만 실행 가능했다. 따라서 쫓아낼 때도 통째로 쫓아내야(표준 [[335_swapping|스와핑]]) 했다. 그러나 프로그램 덩치가 수백 MB, 수 GB로 커지면서, 1GB를 통째로 디스크에 쓰고 읽는 데 수 초~수십 초가 걸려 시스템이 사실상 멈춰버리는 끔찍한 오버헤드가 발생했다. 전송 시간을 줄이기 위해 '필요한 부분만 쪼개서 옮기자'는 혁명적 아이디어가 필요했다.

- **등장 배경 및 아키텍처 진화**:
  1. **[[459_quic_fec_forward_error_correction|초기]] (표준 [[335_swapping|스와핑]])**: 베이스/[[330_limit_register|한계 레지스터]]만 있던 시절, 메모리 [[291_fragmentation_and_reassembly_process|단편화]]를 해결하거나 메모리를 비우려면 프로세스 전체 덩어리를 디스크로 [[335_swapping|Swapping]] 해야 했다.
  2. **오버헤드의 한계**: CPU 속도는 비약적으로 빨라진 반면, 물리적 회전 원판을 쓰는 하드디스크([[465_hdd_structure|HDD]])의 속도는 거의 제자리였다. I/O 대기 시간([[326_transfer_time|Transfer Time]])이 시스템 성능의 99%를 갉아먹었다.
  3. **현대 ([[259_paging|페이징]] 기반)**: [[328_mmu|MMU]] 하드웨어의 발전으로 메모리를 4KB 단위의 [[286_page_frame|페이지]]([[286_page_frame|Page]])로 쪼개어 관리하는 [[381_virtual_memory|가상 메모리]]가 도입되었다. 이에 따라 쫓아낼 때도 최근에 사용하지 않은 '[[286_page_frame|페이지]] 조각' 단위로만 스왑 영역(Swap [[514_partition_slice_volume|Partition]])으로 쫓아내는 [[286_page_frame|페이지]] [[335_swapping|스와핑]]([[286_page_frame|Page]] Out / [[286_page_frame|Page]] In)이 업계의 표준이 되었다.

```text
┌────────────────────────────────────────────────────────────────────┐
│         표준 스와핑 vs 페이징 시스템 스와핑 크기 체감 비교         │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ [ 프로세스 크기: 100MB, 하드디스크 속도: 10MB/s 가정 ]             │
│                                                                    │
│ ▶ 표준 스와핑 (프로세스 통째로 Swap Out)                           │
│    [██████████ 100MB 덩어리 ██████████]                            │
│    I/O 소요 시간: 10초 (10초 동안 컴퓨터 화면 멈춤 렉 발생)        │
│                                                                    │
│ ▶ 페이징 시스템 스와핑 (페이지 단위 Swap Out)                      │
│    [█ 4KB █][█ 4KB █] ... (가장 안 쓴 페이지 2개만 쫓아냄)         │
│    I/O 소요 시간: 0.0008초 (사용자가 전혀 눈치채지 못함)           │
└────────────────────────────────────────────────────────────────────┘
```
**[다이어그램 해설]** 이 단순한 산수가 왜 현대 [[001_operating_system_purpose|운영체제]]가 표준 [[335_swapping|스와핑]]을 버리고 [[286_page_frame|페이지]] [[335_swapping|스와핑]]으로 넘어왔는지를 완벽하게 증명한다. 메모리를 비우기 위해 10초를 낭비하면 실시간 상호작용이 불가능해진다. [[259_paging|페이징]] 기반에서는 전체 100MB 중 지금 당장 화면 렌더링에 쓰이지 않는 백그라운드 탭 [[001_dikw_pyramid|데이터]] 4KB 조각들만 핀셋으로 집어내듯 디스크로 넘긴다.

- **📢 섹션 요약 비유**: 수박 한 통을 먹기 위해 수박 전체를 한입에 우겨넣으려다 숨이 막히는 것(표준 [[335_swapping|스와핑]])과, 깍둑썰기해서 먹고 싶은 조각만 포크로 집어먹는 것([[259_paging|페이징]] [[335_swapping|스와핑]])의 차이입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소 및 전송 단위 차이

| 비교 요소 | 표준 [[335_swapping|스와핑]] (Standard [[335_swapping|Swapping]]) | [[259_paging|페이징]] 시스템 [[335_swapping|스와핑]] ([[259_paging|Paging]] [[335_swapping|Swapping]]) | 비유 |
|:---|:---|:---|:---|
| **교환 단위** | 프로세스 전체 (Entire [[300_process|Process]]) | [[286_page_frame|페이지]] 조각 단위 (보통 4KB [[286_page_frame|Page]]) | 통돼지 바베큐 vs 삼겹살 1인분 |
| **메모리 할당** | [[338_contiguous_memory_allocation|연속 메모리 할당]] (Contiguous) | [[350_non_contiguous_memory_allocation|비연속 메모리 할당]] (Non-contiguous) | 식당 통대관 vs 빈자리 흩어져 앉기 |
| **하드웨어 지원** | 베이스/[[330_limit_register|한계 레지스터]] | [[353_page_table|페이지 테이블]] ([[353_page_table|Page Table]]), [[357_tlb|TLB]] | 나침반 하나 vs 정밀 GPS 지도 |
| **발생 [[016_interrupt_mechanism|인터럽트]]** | 없음 (OS 스케줄러가 강제 수행) | [[720_page_fault_isr|페이지 폴트]] ([[387_page_fault|Page Fault]]) [[016_interrupt_mechanism|인터럽트]] 발생 | 사장님의 강제 퇴장 vs 손님의 호출 |

---

### 동작 메커니즘의 차이: Swap-out vs [[286_page_frame|Page]]-out

[[001_operating_system_purpose|운영체제]] 용어에서도 이 둘을 엄격히 구분한다. 통째로 쫓아내는 것은 **Swap-out / Swap-in**이라 부르고, [[286_page_frame|페이지]] 단위로 쫓아내는 것은 **[[286_page_frame|Page]]-out / [[286_page_frame|Page]]-in**이라 부른다. (다만 오늘날엔 두 단어를 혼용해서 쓰기도 한다.)

```text
┌───────────────────────────────────────────────────────────────────────────┐
│             표준 스와핑과 페이징 스와핑의 런타임 아키텍처                 │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ [ 1. 표준 스와핑 아키텍처 ]                                               │
│  [ CPU ] ──요청──▶ [ 메모리가 꽉 참 ]                                     │
│  중기 스케줄러 개입: "메모리가 없네. 프로세스 B(1GB) 전체를 디스크로 빼!" │
│  결과: 시스템 버스 100% 점유, 타 작업 올스톱 (비효율의 극치)              │
│                                                                           │
│ [ 2. 페이징 스와핑 (가상 메모리) 아키텍처 ]                               │
│  [ CPU ] ──요청──▶ [ 메모리 공간 부족 (Free frame 부족) ]                 │
│  페이지 교체 알고리즘(LRU 등) 작동:                                       │
│   "프로세스 A, B, C가 가진 수만 개의 4KB 페이지 중,                       │
│    가장 오랫동안 안 쓴 페이지 10개만 골라서 디스크(Swap Area)로 버려"     │
│  결과: 단 40KB의 I/O만 발생. 다른 프로세스들은 전혀 방해받지 않고 실행.   │
└───────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 두 번째 구조([[259_paging|페이징]] [[335_swapping|스와핑]])가 현대의 [[381_virtual_memory|가상 메모리]] 관리(Virtual [[610_memory_management|Memory Management]])의 척추다. [[259_paging|페이징]] 기반 [[335_swapping|스와핑]]은 프로세스 간의 불공평을 해소한다. 덩치가 큰 프로세스라고 무조건 쫓겨나는 것이 아니라, 어떤 프로세스 소속이든 관계없이 '오래 안 쓴 게으른 조각([[286_page_frame|Page]])'들만 선별적으로 추출([[286_page_frame|Page]]-out)되어 공간을 확보한다. 

---

### [[255_demand_paging|요구 페이징]] ([[255_demand_paging|Demand Paging]])과의 결합

[[259_paging|페이징]] 시스템 [[335_swapping|스와핑]]은 스왑 인(Swap In)을 할 때도 극강의 효율을 발휘한다.
- 쫓겨난 조각이 다시 필요해지면, CPU는 메모리에 없다는 것을 깨닫고 **[[720_page_fault_isr|페이지 폴트]]([[387_page_fault|Page Fault]])** 트랩을 발생시킨다.
- OS는 디스크에서 그 4KB 조각 하나만 딱 읽어서 메모리의 빈 프레임(Frame)에 꽂아 넣는다.
- 이를 **[[255_demand_paging|요구 페이징]]([[255_demand_paging|Demand Paging]])**이라 하며, "네가 부르기(Demand) 전까지는 절대 디스크에서 메모리로 올리지 않겠다"는 궁극의 [[015_지연_데이터_관점|지연]] 적재([[182_lazy_loading|Lazy Loading]]) 철학이다.

- **📢 섹션 요약 비유**: 두꺼운 백과사전 전체를 가방에 넣고 빼는(표준 스왑) 대신, 백과사전을 링바인더로 분해해 오늘 수업에 필요한 종이 3장만 빼서 파일철에 끼워 넣는([[255_demand_paging|요구 페이징]] 스왑) 혁신입니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: [[342_external_fragmentation|외부 단편화]]([[342_external_fragmentation|External Fragmentation]]) 관점

| 항목 | 표준 [[335_swapping|스와핑]] ([[523_contiguous_allocation|연속 할당]]) | [[259_paging|페이징]] [[335_swapping|스와핑]] (비연속 할당) |
|:---|:---|:---|
| **메모리 반환 시** | 100MB 프로세스가 [[336_swap_out_in|Swap Out]] 되면, 100MB짜리 거대한 구멍 1개가 생김 | 4KB [[286_page_frame|페이지]]가 [[286_page_frame|Page]] Out 되면, 4KB짜리 작은 구멍 1개가 생김 |
| **재적재 시 문제** | 디스크에서 다시 Swap In 될 때, 연속된 100MB 빈 공간이 없으면 (구멍들이 쪼개져 있으면) 적재 불가! | 빈 공간이 흩어져 있어도 상관없음. 빈 4KB 프레임 아무 곳에나 찔러넣으면 됨 |
| **결론** | **[[342_external_fragmentation|외부 단편화]] 악몽** 발생, 메모리 [[347_compaction|압축]]([[347_compaction|Compaction]]) 추가 비용 발생 | **[[342_external_fragmentation|외부 단편화]] 원천 제거**, 공간 활용률 극대화 |

### 비교 2: I/O 디바이스 대기 상태(Waiting for I/O)에서의 안정성

표준 [[335_swapping|스와핑]]에서는 하드웨어가 DMA로 [[001_dikw_pyramid|데이터]]를 전송 중일 때 프로세스를 통째로 날려버리면 끔찍한 [[001_dikw_pyramid|데이터]] 파괴가 일어난다고 앞서 배웠다. 
- 하지만 **[[259_paging|페이징]] [[335_swapping|스와핑]]**에서는 I/O 전송이 걸려있는 특정 4KB 메모리 [[286_page_frame|페이지]]만 핀(Pinning / 락)을 걸어두고 절대 [[336_swap_out_in|스왑 아웃]] 되지 않도록 잠근다.
- 그리고 나머지 수만 개의 [[286_page_frame|페이지]]들은 자유롭게 [[336_swap_out_in|스왑 아웃]] 시킨다. 훨씬 더 세밀하고 유연한 방어벽 구축이 가능하다.

```text
┌──────────┬────────────┬────────────┬──────────────────────────┐
│ 스와핑 방식│ 전송 소요 시간│ 단편화 발생  │ I/O 락(Pin)단위   │
├──────────┼────────────┼────────────┼──────────────────────────┤
│ 표준 스왑  │ 초 단위 (느림)│ 외부 단편화 심각│ 프로세스 전체  │
│ 페이징 스왑│ 밀리초 (빠름)│ 내부 단편화 존재│ 4KB 페이지 1장  │
└──────────┴────────────┴────────────┴──────────────────────────┘
```
**[매트릭스 해설]** 완벽해 보이는 [[259_paging|페이징]] 시스템에도 약점은 있다. 4KB 단위로 고정해서 자르다 보니, 1KB만 필요한 [[001_dikw_pyramid|데이터]]도 4KB를 할당받아 공간이 낭비되는 '[[341_internal_fragmentation|내부 단편화]]([[341_internal_fragmentation|Internal Fragmentation]])'가 발생한다. 하지만 수십 MB가 버려지는 [[342_external_fragmentation|외부 단편화]]에 비하면 이 정도 낭비는 현대 대용량 램 환경에서는 애교 수준이며, 속도적 이점이 이 모든 단점을 압살한다.

- **📢 섹션 요약 비유**: 주차장에 [[344_bus|버스]](표준 프로세스)를 댈 때는 세 칸이 연속으로 비어있어야 하지만, 오토바이([[286_page_frame|페이지]])는 아무 빈칸 하나에나 구겨 넣으면 되므로 주차장(메모리) 공간 효율이 차원이 달라집니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 현대 리눅스의 [[598_vm_migration_nic|vm]].swappiness 튜닝
1. **상황**: 백엔드 [[002_database_definition|데이터베이스]] 서버(MySQL, [[542_redis|Redis]])를 운영 중이다. 이들은 메모리에 캐시를 꽉 채워두고 초고속으로 응답하는 것이 생명이다.
2. **[[286_page_frame|페이지]] 아웃([[286_page_frame|Page]]-out)의 역효과**:
   - [[001_operating_system_purpose|운영체제]](리눅스)는 똑똑한 척하며 "어? DB가 캐시 [[001_dikw_pyramid|데이터]]를 메모리에 올려놓고 한참 동안 안 읽네? 디스크로 쫓아내고 남는 램을 딴 데 써야지"라며 [[286_page_frame|페이지]] 아웃을 시켜버린다.
   - 갑자기 유저가 그 [[001_dikw_pyramid|데이터]]를 요청하면 디스크에서 읽어오느라([[286_page_frame|Page]]-in) 응답 [[015_지연_데이터_관점|지연]]([[141_latency|Latency]] Spikes)이 발생한다.
3. **실무적 의사결정**:
   - 리눅스의 [[022_kernel_role|커널]] 파라미터인 `vm.swappiness` (0~100) 값을 조절한다. 기본값은 보통 60이다.
   - DB 서버에서는 이 값을 `1` 또는 `0`으로 극단적으로 낮춰, [[022_kernel_role|커널]]에게 "메모리가 터져 죽기 직전이 아니면 절대 내 [[001_dikw_pyramid|데이터]] 조각([[286_page_frame|Page]])들을 디스크로 빼내지 마라!"고 강제하여 인메모리 성능을 보장한다.

### 모바일 [[001_operating_system_purpose|운영체제]]의 선택 (안드로이드)
안드로이드 스마트폰은 [[259_paging|페이징]] 기반 [[335_swapping|스와핑]]조차 디스크([[256_flash_memory|플래시 메모리]]) 수명을 갉아먹는다고 판단했다.
대신 RAM 안의 공간을 떼어내어 [[347_compaction|압축]]하는 **zRAM([[347_compaction|압축]] 스왑 영역)**을 만들어, 디스크로 보내지 않고 메모리 내부에서 [[347_compaction|압축]]([[286_page_frame|Page]]-out to zRAM)하고 해제([[286_page_frame|Page]]-in from zRAM)하는 기법으로 CPU를 조금 더 쓰고 디스크 I/O를 원천 차단하는 기조를 택했다.

- **📢 섹션 요약 비유**: 직원이 자주 안 쓰는 물건을 창고(디스크)로 빼려고 할 때, 사장님이 "그건 창고로 빼지 말고 그냥 책상 서랍에 [[347_compaction|압축]]팩(zRAM)으로 묶어둬. 손님 오면 1초 만에 꺼내야 해!"라고 지시(swappiness 튜닝)하는 것과 같습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 내용 |
|:---|:---|
| **디스크 I/O 병목 해소**| 수백 MB [[001_dikw_pyramid|데이터]] 전송 오버헤드를 4KB 수준으로 쪼개어 시스템 중단(Stuttering) 현상 방지 |
| **[[673_multiprogramming_bottleneck_resource|다중 프로그래밍]] 극대화**| 프로세스의 필수 조각([[265_working_set|Working Set]])만 메모리에 남겨두어, 동시 실행 프로그램 수를 압도적으로 늘림 |
| **메모리 파편화 해결** | 비연속 할당([[259_paging|페이징]])과 결합하여, [[342_external_fragmentation|외부 단편화]]를 없애고 [[347_compaction|압축]]([[347_compaction|Compaction]]) 연산 비용을 제거 |

### 결론 및 미래 전망

표준 [[335_swapping|스와핑]]은 초창기 컴퓨터 공학이 하드웨어 한계를 극복하기 위해 짜낸 투박한 '망치'였다면, [[259_paging|페이징]] 기반 [[335_swapping|스와핑]]은 메스(Scalpel)처럼 정밀한 [[381_virtual_memory|가상 메모리]] 혁명의 '메스'다. 오늘날 "[[335_swapping|스와핑]]"이라는 단어는 사실상 사어(Dead [[075_word|word]])가 되었고, 시스템 관리자나 엔지니어들이 말하는 "스왑 메모리를 늘린다", "스왑이 발생한다"는 100% '[[286_page_frame|페이지]] [[335_swapping|스와핑]]([[286_page_frame|Page]] In/Out)'을 지칭한다. 미래에는 [[441_cxl|CXL]]([[441_cxl|Compute Express Link]]) 같은 기술을 통해, 네트워크 너머 다른 서버의 남는 RAM을 내 스왑 공간처럼 사용하는 '원격 메모리 [[259_paging|페이징]]' 시대로 진화하며 디스크의 그림자에서 완전히 벗어날 것이다.

- **📢 섹션 요약 비유**: 옛날엔 편지를 보내려면 역마차(표준 스왑) 전체를 대여해야 했지만, 이제는 우표 한 장 붙인 규격 봉투([[286_page_frame|페이지]])에 담아 우체통에 넣으면 알아서 초고속으로 배달되는 첨단 물류 시스템으로의 진화입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[335_swapping|스와핑]] ([[335_swapping|Swapping]]) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[336_swap_out_in|스왑 아웃]] ([[336_swap_out_in|Swap out]]) / 스왑 인 (Swap in) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[338_contiguous_memory_allocation|연속 메모리 할당]] ([[338_contiguous_memory_allocation|Contiguous Memory Allocation]]) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[339_fixed_partition|고정 분할 방식]] ([[339_fixed_partition|Fixed Partition]]) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[스왑 아웃 (Swap out) / 스왑 인 (Swap in)]
    │
    ▼
[표준 스와핑 (전체 프로세스) vs 페이징 시스템 스와핑 (페이지 단위) (Standard Vs Paging Swapping)]
    │
    ├──▶ [연속 메모리 할당 (Contiguous Memory Allocation)]
    └──▶ [고정 분할 방식 (Fixed Partition)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [[347_compaction|압축]]해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 표준 [[335_swapping|스와핑]] (전체 프로세스) vs [[259_paging|페이징]] 시스템 [[335_swapping|스와핑]] ([[286_page_frame|페이지]] 단위) (Standard Vs [[259_paging|Paging]] [[335_swapping|Swapping]])은 컴퓨터가 메모리를 방처럼 나눠 쓰고 주소를 찾는 방법이에요.
2. 먼저 [[336_swap_out_in|스왑 아웃]] ([[336_swap_out_in|Swap out]]) / 스왑 인 (Swap in)을 이해하면 표준 [[335_swapping|스와핑]] (전체 프로세스) vs [[259_paging|페이징]] 시스템 [[335_swapping|스와핑]] ([[286_page_frame|페이지]] 단위) (Standard Vs [[259_paging|Paging]] [[335_swapping|Swapping]])이 왜 필요한지 더 쉽게 보여요.
3. 그래서 표준 [[335_swapping|스와핑]] (전체 프로세스) vs [[259_paging|페이징]] 시스템 [[335_swapping|스와핑]] ([[286_page_frame|페이지]] 단위) (Standard Vs [[259_paging|Paging]] [[335_swapping|Swapping]])을 잘 알면 나중에 [[338_contiguous_memory_allocation|연속 메모리 할당]] ([[338_contiguous_memory_allocation|Contiguous Memory Allocation]])도 훨씬 쉽게 배울 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 337 / 800

← **이전**: [[336_swap_out_in|336. 스왑 아웃 (Swap out) / 스왑 인 (Swap in)]]
**다음**: [[338_contiguous_memory_allocation|338. 연속 메모리 할당 (Contiguous Memory Allocation)]] →

---
