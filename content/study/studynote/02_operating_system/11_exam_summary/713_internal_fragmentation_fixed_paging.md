---
title: 713. 내부 단편화 고정/페이징 (Internal Fragmentation Fixed Paging)
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[341_internal_fragmentation|내부 단편화]]([[341_internal_fragmentation|Internal Fragmentation]])는 운영체제가 메모리를 일정하게 고정된 크기(블록이나 [[286_page_frame|페이지]])로 미리 잘라놓고 나누어 줄 때, **프로세스가 요구한 메모리 양보다 할당된 공간이 더 커서 발생하는 '블록 내부의 버려지는 짜투리 공간'**을 의미한다.
> 2. **[[259_paging|페이징]]의 딜레마**: [[342_external_fragmentation|외부 단편화]]를 100% 멸종시킨 **[[259_paging|페이징]]([[259_paging|Paging]])** 시스템 역시 메모리를 4KB 단위의 고정 크기로 쪼개어 쓰므로, 필연적으로 프로세스의 마지막 [[286_page_frame|페이지]] 끝자락에 최대 `4KB - 1Byte`만큼의 [[341_internal_fragmentation|내부 단편화]]를 유발한다.
> 3. **가치/타협**: 하지만 이 [[341_internal_fragmentation|내부 단편화]]로 잃는 메모리 낭비율은 전체 메모리 대비 1%도 되지 않으며, 이를 감수함으로써 얻는 **'메모리 관리의 단순화'와 '[[342_external_fragmentation|외부 단편화]] 제거'의 이득**이 압도적으로 크기 때문에 현대 OS가 기꺼이 지불하는 필수적인 '포장지 비용'이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **고정 분할 (Fixed [[179_table_partitioning_concept|Partitioning]])**: 메모리를 미리 정해진 고정 크기(예: 10MB)로 썰어두는 옛날 방식.
  - **[[259_paging|페이징]] ([[259_paging|Paging]])**: 메모리를 4KB(또는 2MB 등) 단위의 고정된 프레임(Frame)으로 아주 잘게 썰어 쓰는 현대적 방식.
  - **[[341_internal_fragmentation|내부 단편화]] ([[341_internal_fragmentation|Internal Fragmentation]])**: 할당된 고정 [[514_partition_slice_volume|파티션]](또는 [[286_page_frame|페이지]]) 내부에서, 사용자가 쓰지 않고 남겨두었지만 다른 누구도 쓸 수 없게 버려진 공간.

- **필요성 (관리의 단순함을 향한 타협)**: 
  - 가변 분할(원하는 만큼만 딱 잘라주는 방식)을 썼더니, [[342_external_fragmentation|외부 단편화]]([[342_external_fragmentation|External Fragmentation]])가 발생해서 남는 메모리를 아예 못 쓰는 최악의 사태가 벌어졌다. [[347_compaction|압축]]([[347_compaction|Compaction]])을 하려니 CPU가 죽어났다.
  - **해결책**: "사용자 입맛에 맞추는 걸 포기하자! 메모리는 무조건 내가 정해둔 '상자 크기'로만 줄 테니, 물건이 작아도 상자 하나를 다 써라!" 
  - 이렇게 하면 상자(블록)들 사이의 [[342_external_fragmentation|외부 단편화]]는 완전히 사라지고 관리가 미친 듯이 편해지지만, 상자 안의 남는 공간([[341_internal_fragmentation|내부 단편화]])이라는 새로운 부작용이 생겼다.

  - **[[342_external_fragmentation|외부 단편화]] (가변 분할)**: 피자를 손님이 원하는 모양과 크기로 잘라주다 보니, 피자 판에 이상한 모양의 찌꺼기가 남아 다음 손님에게 피자를 못 주는 현상.
  - **[[341_internal_fragmentation|내부 단편화]] (고정/[[259_paging|페이징]])**: 피자를 무조건 8등분(고정 크기)해서 한 조각 단위로만 판다. 피자가 애매하게 남는 일([[342_external_fragmentation|외부 단편화]])은 없다. 하지만 배가 별로 안 고픈 손님이 한 조각을 사서 한 입만 먹고 버리면? 남은 피자 테두리([[341_internal_fragmentation|내부 단편화]])는 아깝지만 그냥 버려야 한다.

- **발전 과정**:
  1. **고정 분할**: 너무 크게 잘라서(예: 10MB) [[341_internal_fragmentation|내부 단편화]]가 심각했음.
  2. **가변 분할**: [[341_internal_fragmentation|내부 단편화]]를 없애려다 최악의 [[342_external_fragmentation|외부 단편화]] [[087_process_state_transition|생성]].
  3. **[[259_paging|페이징]] ([[259_paging|Paging]])**: 고정 분할로 돌아오되, 상자 크기를 **4KB**로 아주 잘게 쪼개어 [[341_internal_fragmentation|내부 단편화]]의 낭비를 극한으로 줄인 궁극의 타협.

- **📢 섹션 요약 비유**: 택배를 보낼 때 물건 크기에 딱 맞는 맞춤형 상자(가변)를 구하는 수고로움 대신, 우체국 표준 1호 상자([[259_paging|페이징]])를 씁니다. 물건이 상자보다 약간 작아서 남는 빈 공간([[341_internal_fragmentation|내부 단편화]])에 뽁뽁이를 채워 버려야 하지만, 택배 분류와 적재 효율은 완벽해집니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[341_internal_fragmentation|내부 단편화]]의 수학적 발생 모델 ([[259_paging|페이징]] 시스템)

현대 리눅스/윈도우의 기본 [[286_page_frame|페이지]]([[286_page_frame|Page]]) 크기는 **4KB (4,096 Bytes)** 다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 페이징(Paging) 환경의 내부 단편화 발생 원리             │
  ├───────────────────────────────────────────────────────────────────┤
  │  [상황: 프로세스 A가 17KB의 메모리를 요구함]                            │
  │                                                                   │
  │   - OS의 페이지 크기 = 4KB                                          │
  │   - 필요 페이지 수 계산: 17KB / 4KB = 4장 ... 나머지 1KB             │
  │   - OS는 무조건 '온전한 페이지' 단위로만 할당해야 함! (쪼개기 불가)         │
  │   - 결론: OS는 프로세스 A에게 [ 5장의 페이지 (총 20KB) ]를 할당함.      │
  │                                                                   │
  │  [메모리 할당 맵]                                                    │
  │   [Page 1] (4KB 꽉 참)                                             │
  │   [Page 2] (4KB 꽉 참)                                             │
  │   [Page 3] (4KB 꽉 참)                                             │
  │   [Page 4] (4KB 꽉 참)                                             │
  │   [Page 5] (1KB 사용됨) + [ 3KB의 버려진 공간 (내부 단편화!) ] ◀──     │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** [[259_paging|페이징]] 시스템에서 [[341_internal_fragmentation|내부 단편화]]는 **오직 프로세스의 '가장 마지막 [[286_page_frame|페이지]]'에서만 발생**한다. 따라서 1개 프로세스당 발생하는 [[341_internal_fragmentation|내부 단편화]]의 최댓값은 `페이지 크기 - 1Byte (약 4KB)`를 넘을 수 없으며, **평균적인 [[341_internal_fragmentation|내부 단편화]] 크기는 [[352_page_size|페이지 크기]]의 절반(약 2KB)**이다. 프로세스의 크기가 수백 MB라 하더라도 낭비되는 메모리는 고작 2KB에 불과하므로, 이 정도의 낭비는 현대 OS에서 완전히 무시된다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 메모리 할당 기법별 [[291_fragmentation_and_reassembly_process|단편화]] 발생표 (핵심 암기)

이 표 하나가 메모리 관리 아키텍처의 모든 변천사를 설명한다.

| 할당 기법 | [[342_external_fragmentation|외부 단편화]] | [[341_internal_fragmentation|내부 단편화]] | 특징 및 원인 |
|:---|:---:|:---:|:---|
| **고정 분할 (Fixed)** | **발생 (O)** | **발생 (O)** | 상자가 커서 안이 남고(내부), 상자보다 큰 프로세스는 못 들어감(외부) |
| **가변 분할 (Variable)**| **발생 (O)** | 발생 안 함 (X) | 크기를 딱 맞춰 주므로 안쪽은 꽉 차나, 밖의 자투리가 흩어짐 |
| **[[259_paging|페이징]] ([[259_paging|Paging]])** | 발생 안 함 (X) | **발생 (O)** | 모든 블록이 4KB라 밖엔 구멍이 안 나지만, 마지막 [[286_page_frame|페이지]] 내부가 남음 |
| **[[364_segmentation|세그멘테이션]] (Seg)** | **발생 (O)** | 발생 안 함 (X) | [[369_logic_bomb|논리]]적 크기(함수 등)로 딱 맞춰 자르므로 가변 분할의 [[342_external_fragmentation|외부 단편화]] 재발 |

### 과목 융합 관점

- **네트워크 (NW)**: 네트워크의 MTU([[292_packet_encapsulation_mtu_ethernet_1500_bytes|Maximum Transmission Unit]], 보통 1500바이트) 개념과 똑같다. 내가 "Ok"라는 2바이트짜리 메시지를 보내려 해도, 이더넷은 무조건 46바이트 이상의 프레임으로 래핑([[098_padding_convolutional_neural_network_same_valid|Padding]])해서 보낸다. 헤더와 패딩으로 낭비되는 이 공간이 바로 네트워크 세계의 [[341_internal_fragmentation|내부 단편화]]다.
- **[[002_database_definition|데이터베이스]] (DB)**: 오라클이나 MySQL의 [[001_dikw_pyramid|데이터]] 저장 최소 단위인 '블록(Block, 8KB)'에도 [[341_internal_fragmentation|내부 단편화]]가 존재한다. 10KB [[001_dikw_pyramid|데이터]]를 저장하려면 8KB 블록 2개가 필요하고, 두 번째 블록의 6KB는 텅 빈 상태로 버려진다.

- **📢 섹션 요약 비유**: [[259_paging|페이징]]의 [[341_internal_fragmentation|내부 단편화]]는 마트에서 묶음 상품을 살 때의 손해와 같습니다. 라면이 3개 필요한데 5개 묶음 팩(고정 크기)밖에 안 팔면 2개([[341_internal_fragmentation|내부 단편화]])를 버릴 각오를 하고 사야 합니다. 하지만 마트 입장에서는 낱개로 파는 것보다 묶음으로 파는 게 재고 관리([[342_external_fragmentation|외부 단편화]] 제로)가 100배 편합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — [[371_huge_pages|Huge Pages]] (2MB/1GB) 적용 시 [[341_internal_fragmentation|내부 단편화]]의 역습**: [[190_ai_llm_requirements_specification|AI]] 딥러닝 서버에서 [[357_tlb|TLB]] Miss 병목을 없애기 위해 기본 [[352_page_size|페이지 크기]]를 4KB에서 `2MB (Huge Page)`로 강제 설정했다. 그런데 서버의 램(RAM) 사용량이 평소보다 비정상적으로 치솟아 OOM이 났다.
   - **원인 분석**: [[352_page_size|페이지 크기]]를 2MB로 늘리면, 어떤 프로세스가 10KB의 작은 메모리만 요구해도 OS는 무조건 2MB 단위의 통짜 상자를 내어주어야 한다. 이 경우 **프로세스 1개당 발생하는 [[341_internal_fragmentation|내부 단편화]](버려지는 공간)가 최대 2MB-1Byte**로 폭증한다! 수천 개의 작은 프로세스가 뜨면 허공에 증발하는 메모리가 기가바이트(GB) 단위가 된다.
   - **대응 (기술사적 가이드)**: Huge Page는 [[357_tlb|TLB]] 성능을 비약적으로 올리지만, [[341_internal_fragmentation|내부 단편화]]의 저주를 함께 가져오는 양날의 검이다. 따라서 10KB씩 자잘하게 쓰는 웹 서버나 [[532_microservices_decomposition_patterns|마이크로서비스]] 노드에는 절대 Huge Page를 쓰면 안 되며, 수십 GB를 통짜로 잡고 쓰는 [[188_pl_sql_t_sql_procedural|Oracle]] DB, JVM [[078_heap_datastructure|Heap]], [[542_redis|Redis]] 캐시 서버 환경에만 선별적으로(Transparent [[371_huge_pages|Huge Pages]] 튜닝) 적용해야 한다.

2. **시나리오 — [[760_slab_allocator_object_caching|Slab]] 할당기 (리눅스 [[022_kernel_role|커널]]의 [[341_internal_fragmentation|내부 단편화]] 극복)**: 리눅스 [[022_kernel_role|커널]]이 4KB [[286_page_frame|페이지]] 단위로만 메모리를 쓰다 보니, [[022_kernel_role|커널]]이 자주 만드는 `inode`(약 600바이트)나 `task_struct`(약 1.5KB) 같은 작은 구조체를 만들 때마다 4KB [[286_page_frame|페이지]]를 쓰면 심각한 [[341_internal_fragmentation|내부 단편화]]가 발생했다.
   - **아키텍처 적용**: [[022_kernel_role|커널]]은 이 [[341_internal_fragmentation|내부 단편화]]를 극복하기 위해 **[[349_slab_allocator|Slab Allocator]]**라는 특수 [[369_memory_pool|메모리 풀]](Pool) 아키텍처를 도입했다. OS가 4KB [[286_page_frame|페이지]]를 통째로 받아온 뒤, 그 내부를 `task_struct` 크기(1.5KB)에 딱 맞게 여러 칸으로 쪼개서(Cache) [[022_kernel_role|커널]] 객체 전용 빵틀로 사용한다. 이를 통해 [[259_paging|페이징]] 시스템의 [[341_internal_fragmentation|내부 단편화]]를 [[022_kernel_role|커널]] 레벨에서 0%로 소멸시켰다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 애플리케이션 메모리 단편화 (Fragmentation) 진단 플로우     │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [서버의 실제 사용량(RSS)이 논리적 데이터 크기보다 비정상적으로 높을 때]      │
  │                │                                                  │
  │                ▼                                                  │
  │      서버에 할당된 페이지 크기(Page Size)가 얼마인가? (`getconf PAGE_SIZE`)│
  │          ├─ 2MB / 1GB (Huge Page 환경)                            │
  │          │    ├──▶ [내부 단편화(Internal Fragmentation) 과다 의심]   │
  │          │    └──▶ 대책: THP(Transparent Huge Pages)를 Disable 하거나│
  │          │              어플리케이션 특성에 맞춰 4KB 기본 페이지로 롤백.   │
  │          └─ 4KB (기본 환경)                                        │
  │                │                                                  │
  │                ▼                                                  │
  │      4KB 환경인데도 메모리 낭비가 심하다면, 범인은 페이징(OS)이 아니다!         │
  │          ├──▶ [어플리케이션 Heap의 '외부 단편화' 확진]                 │
  │          │    대책: 유저 스페이스 할당기(malloc, jemalloc)의 파편화 튜닝 │
  │          │          또는 Java GC의 Compaction 지연 문제 점검.         │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** "[[341_internal_fragmentation|내부 단편화]]"는 4KB 기본 리눅스 환경에서는 완전히 무시해도 되는(1개 프로세스당 2KB 낭비) 교과서적인 개념이다. 하지만 클라우드 엔지니어가 [[002_database_definition|데이터베이스]] 튜닝을 위해 **Huge Page를 건드리는 순간, [[341_internal_fragmentation|내부 단편화]]는 시스템을 멈추게 하는 치명적인 현실의 괴물**로 다가온다. 상자의 크기([[352_page_size|Page Size]])를 키우는 것은 항상 낭비([[341_internal_fragmentation|내부 단편화]])와의 트레이드오프임을 계산해야 한다.

### 도입 [[435_checklist_based_testing|체크리스트]]
- **jemalloc의 Size Class**: 개발자가 C언어에서 `malloc(13)`을 불렀을 때, `jemalloc`은 [[341_internal_fragmentation|내부 단편화]]를 막기 위해 13을 주지 않고 딱 정해진 규격인 `16바이트` 묶음(Size Class)으로 올림해서 준다. (3바이트 [[341_internal_fragmentation|내부 단편화]] 발생). 이렇게 고정된 묶음으로 줘서 [[342_external_fragmentation|외부 단편화]]를 막는 대신 미세한 [[341_internal_fragmentation|내부 단편화]]를 허용하는 최신 할당기의 철학을 코딩 시 이해하고 있는가?

- **📢 섹션 요약 비유**: 4KB [[259_paging|페이징]]의 [[341_internal_fragmentation|내부 단편화]]는 머리카락 한 가닥의 무게입니다. 무시하면 됩니다. 하지만 [[517_huge_page|Huge Page]](2MB)를 잘못 쓰면 2MB 상자에 구슬 1개를 넣고 밀봉하는 짓이 반복되어, 거대한 창고(RAM)가 텅 빈 상자들로 가득 차버리는 재앙이 발생합니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 가변 분할 ([[342_external_fragmentation|외부 단편화]] 발생) | [[259_paging|페이징]] ([[341_internal_fragmentation|내부 단편화]] 감수) | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (메모리 파편화)**| 흩어진 공간으로 30% 이상 사용 불가 | **물리 메모리 100% 완전 활용 가능**| 메모리 할당 실패([[157_oom_killer|OOM]]) 원천 차단 |
| **정량 (버려지는 공간)**| 0 [[074_byte|바이트]] (안쪽은 꽉 참) | 프로세스당 최대 4KB 버려짐 (무시 가능)| 전체 시스템 메모리 대비 0.1% 미만의 미미한 손실 |
| **정성 (OS 구현)** | 흩어진 빈 공간 리스트 관리 복잡 | 4KB 프레임의 단순 비트맵 매핑 | OS [[022_kernel_role|커널]]의 메모리 관리 로직 초단순화 및 극강화 |

### 미래 전망
- **다중 [[352_page_size|페이지 크기]] 혼용 (Mixed [[286_page_frame|Page]] Sizes)**: [[341_internal_fragmentation|내부 단편화]]와 [[342_external_fragmentation|외부 단편화]]([[357_tlb|TLB]])의 딜레마를 동시에 풀기 위해, 현대 OS와 CPU(ARM64 등)는 4KB, 16KB, 64KB, 2MB 등 여러 개의 [[352_page_size|페이지 크기]]를 동시에 섞어 쓰는 기술을 지원한다. [[022_kernel_role|커널]]이 앱의 메모리 할당 패턴을 런타임에 분석하여, 거대한 배열에는 2MB [[286_page_frame|페이지]]를 주어 TLB를 최적화하고, 자잘한 객체에는 4KB [[286_page_frame|페이지]]를 주어 [[341_internal_fragmentation|내부 단편화]]를 막는 하이브리드 자동 변속 시스템이 대세가 되었다.

### 결론
[[341_internal_fragmentation|내부 단편화]]([[341_internal_fragmentation|Internal Fragmentation]])는 운영체제가 "완벽함"을 포기하고 "단순함의 미학"을 선택한 위대한 타협의 흔적이다. 가변 분할 시절, 1바이트의 메모리도 낭비하지 않으려다 오히려 램 전체가 조각나버리는 최악의 결말([[342_external_fragmentation|외부 단편화]])을 맞이했던 공학자들은 깨달았다. **"조금 버려도 좋으니, 규격을 통일하자."** [[259_paging|페이징]]([[259_paging|Paging]])이 도입되며 발생한 프로세스 끝자락의 2KB 남짓한 [[341_internal_fragmentation|내부 단편화]]는, [[342_external_fragmentation|외부 단편화]]라는 악마를 물리치기 위해 우리가 기꺼이 지불한 가장 저렴하고 합리적인 세금이다.

- **📢 섹션 요약 비유**: 바지를 살 때 내 다리 길이에 완벽하게 1mm까지 맞춤 재단(가변 분할)을 하면 옷감이 낭비되지 않지만 재단사가 과로사합니다. 그냥 공장에서 S, M, L 기성복([[259_paging|페이징]])을 찍어내서 입고, 바짓단이 조금 남으면 접어 입는 것([[341_internal_fragmentation|내부 단편화]])이 인류를 풍요롭게 만든 대량 생산의 지혜입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[322_logical_virtual_address|논리 주소]] [[323_physical_address|물리 주소]] 변환 [[328_mmu|MMU]] | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[342_external_fragmentation|외부 단편화]] 가변 분할 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 동적 할당 First/Best/[[346_worst_fit|Worst Fit]] | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[259_paging|페이징]] 시스템 프레임 테이블 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[외부 단편화 가변 분할]
    │
    ▼
[내부 단편화 고정/페이징 (Internal Fragmentation Fixed Paging)]
    │
    ├──▶ [동적 할당 First/Best/Worst Fit]
    └──▶ [페이징 시스템 프레임 테이블]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [[347_compaction|압축]]해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 철수가 피자 가게에서 "나는 피자 1.5조각만 먹을래!"라고 주문했어요.
2. 하지만 피자집 주인([[259_paging|페이징]])은 "우리는 무조건 온전한 1조각 단위로만 팝니다!"라며 피자 2조각을 주었어요. 
3. 철수는 피자 1.5조각을 먹고, 남은 0.5조각은 배가 불러서 그냥 쓰레기통에 버려야 했어요. 이렇게 정해진 크기로만 주다 보니 어쩔 수 없이 버려지는 자투리 0.5조각을 '[[341_internal_fragmentation|내부 단편화]]'라고 부른답니다!
