+++
title = "348. 버디 시스템 (Buddy System) 할당기 - 2의 승수로 분할 및 병합 (외부 단편화 절충)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 버디 시스템(Buddy System) 할당기는 메모리를 요청받았을 때, 전체 물리 메모리를 <strong>무조건 2의 승수(2^k) 크기로만 반씩 쪼개어(Split) 할당</strong>하고, 반환될 때는 쪼개졌던 <strong>자신의 쌍둥이 조각(Buddy)과 <a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/">초고속</a>으로 병합(Coalescing)하는 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 메모리 할당 기법</strong>이다.
> 2. **가치**: 일반적인 가변 분할 방식의 느린 탐색과 병합 오버헤드를 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 연산 기반의 O(1) [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 병합으로 해결하면서, 고정 분할 방식의 장점(빠른 속도)과 가변 분할의 장점(유연성)을 황금비율로 융합했다.
> 3. **융합**: 비록 구조상 2의 승수로 올림 처리하느라 [내부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/)([Internal Fragmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/))가 발생하지만, 악성 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)(External)를 효과적으로 방어하여 오늘날 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)(Linux [Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))의 물리 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 프레임 할당을 담당하는 핵심 엔진으로 자리 잡았다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 버디 시스템은 메모리를 1MB, 512KB, 256KB 등 정확히 $2^k$ 크기의 블록들로만 유지 관리하는 동적 할당 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. 21KB를 요구하면 21KB를 잘라주지 않고 무조건 32KB($2^5$)를 할당해버린다. 프로세스가 종료되면, 이 32KB는 자신과 원래 한 몸이었던 '쌍둥이(Buddy) 32KB'가 비어있는지 확인하고 즉시 합쳐져 64KB로 퓨전(Fusion)한다.
- **필요성**: 기존의 최적/[최초 적합](/knowledge-base/studynote/02_operating_system/06_memory_management/344_first_fit/)(Best/[First-Fit](/knowledge-base/studynote/02_operating_system/06_memory_management/344_first_fit/)) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 흩어진 빈 구멍을 합치기(병합) 위해 긴 [연결 리스트](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/) 장부를 앞뒤로 스캔해야 했다. 이 오버헤드는 1분 1초가 급한 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 심장부([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리 할당)에서는 치명적인 병목이었다. [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)로 메모리가 너덜너덜해지는 것을 막으면서도 "장부를 뒤질 필요 없이 빛의 속도로 병합하는 마법"이 절실했다.

- **등장 배경 및 아키텍처 타협**:
  1. **가변 분할의 실패**: 프로세스 크기(예: 13KB)에 딱 맞춰 잘라주었더니, 나중에 빈 공간을 합칠 때 옆집 주소가 뭔지 찾느라 CPU가 고통받았다.
  2. **수학적 우회 (2의 승수)**: 공학자들은 "무조건 2의 승수로만 자르자"고 합의했다. 이렇게 하면 쪼개진 쌍둥이(Buddy)의 주소는 자신의 주소에서 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)([Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/)) 1개만 뒤집으면(XOR 연산) 0.001초 만에 알아낼 수 있다.
  3. <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/">내부 단편화</a>의 수용</strong>: 17KB를 요구하면 32KB를 줘야 하므로 무려 15KB의 [내부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/)가 버려진다. 하지만 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) 방어력과 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 런타임 속도를 얻기 위해 이 공간적 낭비를 쿨하게 지불(Trade-off)하기로 했다.

```text
┌───────────────────────────────────────────────────────────────────┐
│           버디 시스템(Buddy System)의 쪼개기와 할당 시각화        │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│ [ 초기 상태: 1024KB 통짜 메모리 하나 ]                            │
│ ┌─────────────────────────────────────────────────────┐           │
│ │ 1024KB (전체 텅 빈 공간)                               │        │
│ └─────────────────────────────────────────────────────┘           │
│                                                                   │
│ [ 100KB 프로세스 A 요청 발생 ]                                    │
│ 1. 100KB가 들어갈 가장 가까운 2의 승수는? → 128KB ($2^7$)         │
│ 2. 1024를 반으로 쪼갬 → 512, 512                                  │
│ 3. 512 하나를 반으로 쪼갬 → 256, 256                              │
│ 4. 256 하나를 반으로 쪼갬 → 128, 128 (원하던 크기 도달!)          │
│                                                                   │
│ ▶ 쪼개진 메모리 최종 결과:                                        │
│ ┌──────┬──────┬─────────────┬────────────────────────┐            │
│ │A:128 │빈 128│  빈방 256   │       빈방 512         │            │
│ └──────┴──────┴─────────────┴────────────────────────┘            │
│  (100KB사용)                                                      │
│  (28KB 내부단편화 낭비)                                           │
└───────────────────────────────────────────────────────────────────┘
```
**[다이어그램 해설]** 버디 시스템은 마치 세포 분열처럼 동작한다. 100KB를 원한다고 100KB를 맞춰 주지 않는다. 무조건 128KB 방을 준다. 이 128KB 방의 짝꿍(Buddy)은 바로 옆에 있는 빈방 128KB다. 나중에 A가 종료되면, 이 두 128KB 방은 쌍둥이이므로 묻지도 따지지도 않고 결합하여 256KB로 복원된다. 이 '규격화된 쪼개기와 합치기'가 핵심 철학이다.

- **📢 섹션 요약 비유**: 피자를 조각낼 때 무조건 반, 반의반, 반의반의 반으로만 자르는 칼잡이입니다. 손님이 애매한 크기를 원해도 무조건 한 조각 규격을 던져주어 부스러기 낭비([내부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/))는 생기지만, 나중에 남은 조각들을 다시 합쳐 동그란 피자를 만들기에는 세계 최고로 쉬운 방식입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 버디(Buddy)의 수학적 조건

두 메모리 블록이 "버디(쌍둥이 짝꿍)"가 되려면 반드시 다음 세 가지 조건을 동시에 만족해야 한다.
1. **크기가 정확히 똑같아야 한다.** (예: 둘 다 64KB)
2. **반드시 같은 큰 블록에서 분할되어 나온 형제여야 한다.** (옆에 있는 64KB라도 부모가 다르면 합칠 수 없음)
3. **물리적으로 인접해 있어야 한다.**

이 조건 덕분에, 주소 `A`를 가진 크기 `K`의 블록의 짝꿍(Buddy) 주소는 하드웨어적으로 단 번의 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) XOR 연산(`A XOR K`)으로 찾아낼 수 있다. (리스트 장부를 스캔할 필요가 전혀 없다!)

---

### 병합(Coalescing)의 연쇄 폭발 아키텍처

프로세스가 종료되어 메모리를 반환할 때, 버디 시스템의 진가가 폭발한다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│              버디 반환 시 연쇄 병합 (Domino Coalescing)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ [ 현재 상태 ]                                                               │
│ ┌──────┬──────┬─────────────┬────────────────────────┐                      │
│ │A:128 │빈 128│  빈방 256   │       빈방 512         │                      │
│ └──────┴──────┴─────────────┴────────────────────────┘                      │
│                                                                             │
│ [ 프로세스 A (128KB) 종료 및 반환 ]                                         │
│ 1단계: A가 나감. 내 짝꿍(빈 128)이 비어있네? 합체! → [빈 256] 생성.         │
│ 2단계: 새로 생긴 256의 짝꿍(빈 256)이 옆에 비어있네? 합체! → [빈 512] 생성. │
│ 3단계: 새로 생긴 512의 짝꿍(빈 512)이 옆에 비어있네? 합체! → [빈 1024] 복원!│
│                                                                             │
│ ▶ 결과: 1초도 안 되는 찰나의 3번 XOR 연산만으로                             │
│        잘게 찢어졌던 메모리가 완벽한 1024KB 통짜 블록으로 부활함!           │
└─────────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 가변 분할의 First-Fit이었다면 이 쪼개진 방들을 합치기 위해 메모리 주소를 비교하고 포인터를 갱신하느라 수십 사이클을 낭비했을 것이다. 버디 시스템은 마치 도미노가 쓰러지듯, 쌍둥이들이 비어있기만 하면 눈 깜짝할 사이에 최상위 거대 노드(Big Block)로 연쇄 융합한다. 이 강력한 '거대 블록 복원력' 덕분에 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)에 대한 내성이 극강으로 올라간다.

---

### 자료구조 (Free List [Array](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/))

버디 시스템을 구현하는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 단 하나의 장부가 아니라, <strong>크기별로 <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/">배열</a>(<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/">Array</a> of Linked Lists)</strong>을 만들어 장부를 유지한다.
- `List[0]`: 4KB 빈방들 모음
- `List[1]`: 8KB 빈방들 모음
- `List[5]`: 128KB 빈방들 모음
만약 128KB가 필요하면 `List[5]`를 열어보고, 없으면 `List[6](256KB)`에서 하나를 꺼내 반으로 쪼갠 뒤 128KB 하나는 할당하고 남은 128KB는 `List[5]`에 꽂아 넣는다. 탐색 속도는 철저하게 $O(1)$에 수렴한다.

- **📢 섹션 요약 비유**: 물방울(메모리) 두 개가 만나면 순식간에 두 배 크기의 큰 물방울로 뽁! 하고 합쳐지는 슬라임 액체괴물 같은 구조적 유연성을 자랑합니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: 일반 동적 할당(First/[Best-Fit](/knowledge-base/studynote/02_operating_system/06_memory_management/345_best_fit/)) vs 버디 시스템

| 비교 항목 | 일반 가변 분할 할당 | 버디 시스템 (Buddy System) |
|:---|:---|:---|
| **할당 단위** | 프로세스가 요구한 크기([바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/))에 정확히 맞춤 | $2^k$ (2, 4, 8, 16...) 단위로 강제 반올림 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/">내부 단편화</a></strong> | **전혀 없음** (0%) | **치명적임** (요구량에 따라 최대 49.9% 낭비) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/">외부 단편화</a></strong> | 치명적 발생 (33% 낭비, [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 유발) | 병합이 너무 빨라 거대 구멍이 잘 복원됨 (우수) |
| **탐색 및 병합**| 장부 스캔에 O(N) 시간 소요 (느림) | [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 연산을 통한 O(1) [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 병합 (극강의 속도) |

### 극단적인 [내부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/)의 비극 (Trade-off)

버디 시스템의 유일하고도 치명적인 약점은 바로 '[내부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/)'다.
- 프로세스가 만약 <strong>33KB</strong>를 요청했다면?
- 버디 시스템은 가장 가까운 2의 승수인 <strong>64KB</strong>를 통째로 내어주어야 한다.
- 결과적으로 64 - 33 = <strong>31KB</strong>가 그 방 안에서 아무도 쓰지 못한 채 공중으로 증발해버린다. (거의 50%의 [내부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/))
- 공학자들은 이 거대한 공간적 손실을 감수하고서라도, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨에서는 '탐색/병합 속도 보장'과 '큰 블록의 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) 파괴 방어'가 훨씬 더 갚지다고 판단했다.

```text
┌──────────┬────────────┬────────────┬──────────────────────────────────┐
│ 최적화 포인트│ 가변 분할(동적)│ 페이징(가상)  │ 버디 시스템(커널)     │
├──────────┼────────────┼────────────┼──────────────────────────────────┤
│ 속도 확보  │ ❌ 느림      │ 🟡 TLB 필요 │ 🟢 비트연산 초고속          │
│ 단편화 방어 │ ❌ 둘 다 뚫림 │ 🟢 외부 방어 │ 🟡 외부는 강함, 내부 약함│
│ 주 적용처  │ 낡은 OS, User앱│ OS 논리 주소 │ OS 커널 물리 메모리      │
└──────────┴────────────┴────────────┴──────────────────────────────────┘
```
**[매트릭스 해설]** 범용 유저 애플리케이션에서는 버디 시스템을 거의 쓰지 않는다. 메모리 낭비가 너무 심하기 때문이다. 하지만 하드웨어와 가장 가까운 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)(리눅스)은 디바이스 드라이버나 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 자료구조를 띄우기 위해 "반드시 물리적으로 연속된" 메모리 조각이 필요하다(페이징의 가상 주소 가라치기가 안 통함). 이 물리적 연속 공간을 가장 빠르고 파편화 없이 잘라주는 유일한 해답이 버디 시스템이었다.

- **📢 섹션 요약 비유**: 3만 1천 원짜리 물건을 사는데 잔돈 깎아주기 귀찮다고 5만 원을 내고 거스름돈을 안 받는 쿨한 재벌([내부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/) 낭비)입니다. 돈은 낭비하지만 계산하는 시간(스캔 속도)은 빛처럼 빠릅니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: Linux [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 [Page Frame](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 할당 (Zone Allocator)

1. **상황**: 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 부팅될 때 16GB 물리 메모리를 관리해야 한다. 리눅스는 메모리를 4KB 크기의 '[페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 프레임' 단위로 쪼갠다.
2. <strong>리눅스 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a>의 선택</strong>:
   - 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 물리 프레임을 나눠줄 때 바로 이 <strong>버디 시스템 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>을 심장 엔진으로 사용한다.
   - 4KB 프레임을 기본 단위(Order 0)로 하여, 1개(4KB), 2개(8KB), 4개(16KB), 8개, ..., 최대 1024개(4MB, Order [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/))의 연속된 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 프레임을 2의 승수 단위로 묶어서 `free_area` [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)(장부)에 보관한다.
3. **디바이스 드라이버의 요청**:
   - 네트워크 랜카드 드라이버가 [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) 버퍼용으로 연속된 물리 메모리 15KB를 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 요청(`kmalloc`)한다.
   - [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 버디 시스템은 "15KB? 오케이 16KB(Order 2, 프레임 4장) 블록 던져줄게!" 하고 $O(1)$ 속도로 잘라서 던져준다.
   - 이 견고한 버디 할당기 덕분에 리눅스 서버는 수백 일 동안 켜져 있어도 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 영역의 물리적 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)로 죽는 일이 거의 발생하지 않는다.

### [슬랩](/knowledge-base/studynote/02_operating_system/11_exam_summary/760_slab_allocator_object_caching/)([Slab](/knowledge-base/studynote/02_operating_system/11_exam_summary/760_slab_allocator_object_caching/)) 할당기와의 완벽한 공조 ([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 투트랙)
버디 시스템이 [내부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/)(33KB 요청 시 64KB 줌)로 메모리를 너무 심하게 버리는 문제를 보완하기 위해, 리눅스는 버디 시스템 위에 <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/349_slab_allocator/">슬랩 할당기</a>(<a href="/knowledge-base/studynote/02_operating_system/06_memory_management/349_slab_allocator/">Slab Allocator</a>)</strong>를 이중으로 얹었다.
- 거대한 땅(수십 KB 단위)은 버디 시스템이 큼직하게 잘라주고,
- 그 땅 안에서 작은 오브젝트(수십 [Byte](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 단위)들은 [슬랩 할당기](/knowledge-base/studynote/02_operating_system/06_memory_management/349_slab_allocator/)가 현미경처럼 잘게 썰어서 나누어준다.
- 이 버디-[슬랩](/knowledge-base/studynote/02_operating_system/11_exam_summary/760_slab_allocator_object_caching/) 콤보는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리 관리의 완성형으로 불린다. (다음 키워드에서 상세 서술)

- **📢 섹션 요약 비유**: 고기를 손질할 때 거대한 도끼(버디 시스템)로 소의 뼈대에 맞춰 큼직한 덩어리로 쳐낸 다음, 셰프의 정밀한 회칼([슬랩 할당기](/knowledge-base/studynote/02_operating_system/06_memory_management/349_slab_allocator/))로 손님 입에 쏙 들어갈 크기로 썰어내는 완벽한 이중 분업 시스템입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 내용 |
|:---|:---|
| **메모리 할당/해제 O(1) 달성**| 수학적 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) XOR 연산과 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 인덱싱을 통해 탐색 루프 없이 가장 빠른 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 속도 보장 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/">외부 단편화</a> 내성</strong> | 해제 즉시 도미노처럼 거대 블록으로 융합(Coalescing)되어 물리적 덩어리가 쪼개진 채 방치되는 현상 [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/) |
| **연속된 물리 메모리 보장**| [DMA](/knowledge-base/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) 장치나 하드웨어 드라이버가 필수적으로 요구하는 '물리적으로 이어져 있는 램 공간'을 안정적으로 제공 |

### 결론 및 미래 전망

버디 시스템 (Buddy System) 할당기는 "어떻게 하면 가장 완벽하게 딱 맞춰 자를까([Best-Fit](/knowledge-base/studynote/02_operating_system/06_memory_management/345_best_fit/))"를 포기하고 "어떻게 하면 가장 빠르고 쉽게 원상 복구시킬까"로 철학적 방향을 전환한 위대한 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. 무조건 2의 배수로 자른다는 단순 무식한 규칙 하나가 끔찍했던 장부 스캔의 오버헤드를 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 연산의 우아함으로 승화시켰다. 50%에 달하는 엄청난 [내부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/)라는 대가를 치르면서도 수십 년간 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 최하단 코어 엔진 자리를 지키고 있다는 사실은, 소프트웨어 공학에서 '예측 가능한 빠른 속도'와 '[단편화](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/) 복원력'이 얼마나 압도적인 가치인지를 증명하는 살아있는 역사다.

- **📢 섹션 요약 비유**: 부서진 도자기 조각을 풀로 이어 붙이는 고통([압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)/병합)을 겪느니, 아예 처음부터 블록들을 레고처럼 규격화(2의 승수)시켜놔서 눈 감고도 1초 만에 조립과 해체를 할 수 있게 만든 하드웨어적 타협의 예술입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [최악 적합](/knowledge-base/studynote/02_operating_system/06_memory_management/346_worst_fit/) ([Worst-Fit](/knowledge-base/studynote/02_operating_system/06_memory_management/346_worst_fit/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) ([Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [슬랩 할당기](/knowledge-base/studynote/02_operating_system/06_memory_management/349_slab_allocator/) ([Slab Allocator](/knowledge-base/studynote/02_operating_system/06_memory_management/349_slab_allocator/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [비연속 메모리 할당](/knowledge-base/studynote/02_operating_system/06_memory_management/350_non_contiguous_memory_allocation/) ([Non-contiguous Memory Allocation](/knowledge-base/studynote/02_operating_system/06_memory_management/350_non_contiguous_memory_allocation/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[압축 (Compaction)]
    │
    ▼
[버디 시스템 (Buddy System) 할당기]
    │
    ├──▶ [슬랩 할당기 (Slab Allocator)]
    └──▶ [비연속 메모리 할당 (Non-contiguous Memory Allocation)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 버디 시스템 (Buddy System) 할당기은 컴퓨터가 메모리를 방처럼 나눠 쓰고 주소를 찾는 방법이에요.
2. 먼저 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) ([Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/))을 이해하면 버디 시스템 (Buddy System) 할당기이 왜 필요한지 더 쉽게 보여요.
3. 그래서 버디 시스템 (Buddy System) 할당기을 잘 알면 나중에 [슬랩 할당기](/knowledge-base/studynote/02_operating_system/06_memory_management/349_slab_allocator/) ([Slab Allocator](/knowledge-base/studynote/02_operating_system/06_memory_management/349_slab_allocator/))도 훨씬 쉽게 배울 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 348 / 800

← **이전**: [347. 압축 (Compaction) - 외부 단편화 해결, 동적 재배치 시에만 가능, 오버헤드 막심](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)
**다음**: [349. 슬랩 할당기 (Slab Allocator) - 커널 객체 캐싱, 단편화 방지 및 속도 향상](/knowledge-base/studynote/02_operating_system/06_memory_management/349_slab_allocator/) →

---
