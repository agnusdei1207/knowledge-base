---
title: 285. 페이징 (Paging)
date: '2026-04-20'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[259_paging|페이징]] ([[259_paging|Paging]])은 가상 주소 공간과 물리 메모리를 같은 크기의 [[286_page_frame|페이지]] ([[286_page_frame|Page]])·프레임 (Frame)으로 나누어 매핑함으로써, 프로그램에는 연속 공간을 보이게 하고 하드웨어에는 비연속 배치를 허용하는 주소 관리 방식이다.
> 2. **가치**: 고정 크기 단위로 쪼개면 [[342_external_fragmentation|외부 단편화]] ([[342_external_fragmentation|External Fragmentation]])를 사실상 제거하고, [[001_operating_system_purpose|운영체제]] ([[001_operating_system_purpose|Operating System]])가 [[286_page_frame|페이지]] 단위로 적재·[[571_protection_vs_security|보호]]·교체 [[164_policy|정책]]을 세울 수 있어 [[381_virtual_memory|가상 메모리]]의 실용성이 완성된다.
> 3. **판단 포인트**: [[352_page_size|페이지 크기]]가 작으면 낭비는 줄지만 [[353_page_table|페이지 테이블]]과 [[357_tlb|TLB]] ([[291_tlb|Translation Lookaside Buffer]]) 부담이 커지고, 크면 변환 효율은 좋아지지만 [[341_internal_fragmentation|내부 단편화]]와 입출력 증폭이 커지므로 워크로드에 맞는 절충이 핵심이다.

---

## Ⅰ. 개요 및 필요성

[[259_paging|페이징]] ([[259_paging|Paging]])은 프로세스의 [[369_logic_bomb|논리]]적 주소 공간을 고정 크기 블록으로 나눈 [[286_page_frame|페이지]]와, RAM (Random Access Memory)을 같은 크기 블록으로 나눈 프레임을 1:1로 대응시키는 메모리 관리 기법이다. 핵심은 프로그램이 보기에는 0번지부터 연속인 메모리를 쓰는 것처럼 보이지만, 실제 [[001_dikw_pyramid|데이터]]는 물리 메모리 곳곳의 빈 프레임에 흩어져 있을 수 있다는 점이다. 즉, 연속 배치의 제약을 없애고 주소 변환 계층으로 질서를 만든다.

이 방식이 필요해진 이유는 [[523_contiguous_allocation|연속 할당]]이 메모리를 너무 쉽게 망가뜨렸기 때문이다. 프로그램을 통째로 올리던 시절에는 메모리 중간중간에 작은 빈칸이 남아도, 충분히 큰 연속 구간이 없으면 새 프로세스를 적재할 수 없었다. 이것이 [[342_external_fragmentation|외부 단편화]]이며, 멀티프로그래밍 환경에서는 시간이 갈수록 심해진다. [[347_compaction|압축]] ([[347_compaction|Compaction]])으로 빈칸을 모을 수는 있지만, 실행 중인 [[001_dikw_pyramid|데이터]]를 대량 이동해야 하므로 비용이 크고 운영 복잡도도 높다.

[[259_paging|페이징]]은 이 문제를 규격화로 해결한다. 모든 조각 크기를 같게 만들면 [[001_operating_system_purpose|운영체제]]는 "이 프레임이 비었는가"만 판단하면 되고, 빈 위치가 어디인지 자체는 중요하지 않다. 덕분에 [[381_virtual_memory|가상 메모리]], [[255_demand_paging|요구 페이징]] ([[255_demand_paging|Demand Paging]]), [[286_page_frame|페이지]] [[571_protection_vs_security|보호]] 같은 상위 [[164_policy|정책]]이 가능해진다.

이 그림은 왜 [[259_paging|페이징]]이 필요한지를, [[523_contiguous_allocation|연속 할당]]과 고정 크기 매핑의 차이로 보여준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│              연속 할당의 한계와 페이징의 해결 방식 비교                   │
├───────────────────────────────┬────────────────────────────────────────────┤
│ 연속 할당                     │ 페이징                                    │
│                               │                                            │
│ [P1][빈칸][P2][빈칸][P3]      │ [F0][F1][F2][F3][F4][F5]                 │
│      ↑     ↑                 │   │   │   │   │   │   │                  │
│ 총합은 충분하지만             │  Pg2 Pg0  -  Pg1  -  Pg3                 │
│ 큰 프로세스를 넣을 연속 구간  │                                            │
│ 이 없음                       │ 빈 프레임이면 어디든 적재 가능            │
└───────────────────────────────┴────────────────────────────────────────────┘
```

왼쪽은 빈 공간의 총량과 실제 적재 가능성이 다를 수 있음을 보여주고, 오른쪽은 [[352_page_size|페이지 크기]]를 통일하면 빈 프레임만 있으면 된다는 점을 보여준다. 그래서 [[259_paging|페이징]]은 단순 저장 기법이 아니라, 메모리 배치를 주소 변환으로 추상화한 구조적 해법이다.

- **📢 섹션 요약 비유**: [[259_paging|페이징]]은 제각각 크기의 짐을 창고에 쑤셔 넣는 대신, 모두 같은 규격 박스로 바꿔 보관하는 방식이다. 박스 크기가 같아지면 창고 관리자는 빈칸이 어디냐보다 빈칸이 있느냐만 보면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[259_paging|페이징]]의 주소 변환은 가상 주소를 [[286_page_frame|페이지]] 번호와 오프셋 (Offset)으로 나누는 데서 시작한다. [[286_page_frame|페이지]] 번호는 어느 [[286_page_frame|페이지]]인지 식별하고, 오프셋은 그 [[286_page_frame|페이지]] 내부 몇 번째 바이트인지를 나타낸다. [[328_mmu|MMU]] ([[284_mmu|Memory Management Unit]])는 [[286_page_frame|페이지]] 번호를 [[353_page_table|페이지 테이블]] ([[353_page_table|Page Table]])의 인덱스로 사용해 대응하는 프레임 번호를 찾고, 최종적으로 `프레임 번호 + 같은 오프셋`을 결합해 물리 주소를 만든다. [[286_page_frame|페이지]] 내부 상대 위치는 그대로 유지되고, 바뀌는 것은 "어느 프레임에 있느냐"뿐이다.

[[001_operating_system_purpose|운영체제]]는 [[353_page_table|페이지 테이블]] 엔트리인 PTE ([[353_page_table|Page Table]] Entry)에 단순 위치 정보만 넣지 않는다. 존재 [[073_bit|비트]] (Present [[086_fenwick_tree|Bit]]), 수정 [[073_bit|비트]] ([[396_dirty_bit|Dirty Bit]]), 접근 [[073_bit|비트]] (Access [[086_fenwick_tree|Bit]]), 읽기/[[289_cqrs_db|쓰기]]/실행 권한 같은 제어 정보도 함께 기록한다. 덕분에 [[259_paging|페이징]]은 주소 변환 기법인 동시에 [[571_protection_vs_security|보호]] 메커니즘이 된다. 코드 [[286_page_frame|페이지]]는 실행 가능·[[289_cqrs_db|쓰기]] 금지로, [[001_dikw_pyramid|데이터]] [[286_page_frame|페이지]]는 [[289_cqrs_db|쓰기]] 가능·실행 금지로 분리할 수 있다.

아래 표는 [[259_paging|페이징]] 구성 요소가 각각 어떤 역할과 트레이드오프를 가지는지 요약한다.

| 구성 요소 | 역할 | 핵심 설계 포인트 |
| :-- | :-- | :-- |
| [[286_page_frame|페이지]] ([[286_page_frame|Page]]) | 가상 주소 공간의 고정 크기 단위 | 보통 4KB, 2MB, 1GB 등 크기 선택이 중요 |
| 프레임 (Frame) | 물리 메모리의 고정 크기 단위 | 빈 프레임 관리와 교체 [[164_policy|정책]] 연결 |
| [[353_page_table|페이지 테이블]] | [[286_page_frame|페이지]]→프레임 매핑과 [[571_protection_vs_security|보호]] 정보 저장 | 주소 공간이 커질수록 계층화 필요 |
| [[357_tlb|TLB]] | 최근 변환 결과 캐시 | 미스가 나면 변환 [[015_지연_데이터_관점|지연]] 증가 |
| PTE | 상태·권한·존재 여부 기록 | [[571_protection_vs_security|보호]], [[387_page_fault|페이지 부재]] 처리, 교체 알고리즘의 근거 |

이 그림은 CPU가 가상 주소를 실제 물리 주소로 바꾸는 최소 흐름을 보여준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                    페이징 기반 주소 변환의 핵심 경로                      │
├────────────────────────────────────────────────────────────────────────────┤
│ CPU 가상 주소                                                              │
│      │                                                                     │
│      ▼                                                                     │
│  [ 페이지 번호 | 오프셋 ]                                                   │
│      │                                                                     │
│      ├──────────────▶ TLB 조회 ────── Hit ─────▶ [ 프레임 번호 | 오프셋 ]  │
│      │                                                                     │
│      └──────────────▶ 페이지 테이블 조회 ── Present=1 ─▶ 물리 주소 생성    │
│                                   │                                        │
│                                   └─ Present=0 ─▶ 페이지 부재 (Page Fault) │
│                                                     │                      │
│                                                     ▼                      │
│                                            OS가 디스크에서 적재             │
└────────────────────────────────────────────────────────────────────────────┘
```

[[259_paging|페이징]]은 [[342_external_fragmentation|외부 단편화]]를 없애는 대신 [[341_internal_fragmentation|내부 단편화]] ([[341_internal_fragmentation|Internal Fragmentation]])를 감수한다. 예를 들어 [[352_page_size|페이지 크기]]가 4KB인데 프로세스의 마지막 조각이 1KB만 필요하면 나머지 3KB는 남더라도 그 프레임을 다른 [[286_page_frame|페이지]]와 공유할 수 없다. 그러나 이 낭비는 보통 "마지막 [[286_page_frame|페이지]]의 일부"에 국한되므로, [[342_external_fragmentation|외부 단편화]] 때문에 큰 프로세스 전체가 못 들어가는 상황보다 훨씬 관리 가능하다.

결국 [[259_paging|페이징]]의 핵심 원리는 **고정 크기 매핑 + [[286_page_frame|페이지]] 단위 제어 + 오프셋 보존**이다. 이 세 가지가 함께 있어야 [[001_operating_system_purpose|운영체제]]는 큰 주소 공간, [[571_protection_vs_security|보호]], 교체, [[015_지연_데이터_관점|지연]] 적재를 하나의 메커니즘으로 통합할 수 있다.

- **📢 섹션 요약 비유**: [[259_paging|페이징]]은 아파트 동·호수 체계와 같다. 몇 동인지가 프레임을 찾는 정보라면, 몇 호인지 오프셋은 그대로 유지된다. 집 내부 위치는 같고 건물 배치만 바뀌는 셈이다.

---

## Ⅲ. 비교 및 연결

[[259_paging|페이징]]의 경계를 가장 잘 드러내는 비교 대상은 [[364_segmentation|세그멘테이션]] ([[364_segmentation|Segmentation]])과 [[523_contiguous_allocation|연속 할당]]이다. [[523_contiguous_allocation|연속 할당]]은 구현이 단순하지만 [[342_external_fragmentation|외부 단편화]]와 재배치 부담이 크다. [[364_segmentation|세그멘테이션]]은 코드, [[001_dikw_pyramid|데이터]], 스택처럼 [[369_logic_bomb|논리]] 단위가 분명해 공유와 [[571_protection_vs_security|보호]] 의미를 표현하기 좋지만, 세그먼트 크기가 가변적이라 결국 [[342_external_fragmentation|외부 단편화]] 문제를 피하기 어렵다. 반면 [[259_paging|페이징]]은 [[369_logic_bomb|논리]] 의미는 약하지만 하드웨어 구현과 물리 배치 자유도에서 압도적으로 유리하다.

| 비교 항목 | [[523_contiguous_allocation|연속 할당]] | [[364_segmentation|세그멘테이션]] ([[364_segmentation|Segmentation]]) | [[259_paging|페이징]] ([[259_paging|Paging]]) |
| :-- | :-- | :-- | :-- |
| 관리 단위 | 프로세스 전체 | [[369_logic_bomb|논리]]적 세그먼트 | 고정 크기 [[286_page_frame|페이지]] |
| 분할 기준 | 없음 | 의미 중심 가변 크기 | 하드웨어 친화적 고정 크기 |
| 주된 [[291_fragmentation_and_reassembly_process|단편화]] | [[342_external_fragmentation|외부 단편화]] 큼 | [[342_external_fragmentation|외부 단편화]] 존재 | [[341_internal_fragmentation|내부 단편화]] 존재 |
| [[571_protection_vs_security|보호]]/공유 | 거칠게 적용 | 의미 단위 적용 쉬움 | [[286_page_frame|페이지]] 단위 세밀 적용 |
| 현대 활용 | 제한적 | 보조적 개념 | [[381_virtual_memory|가상 메모리]]의 표준 |

현대 [[001_operating_system_purpose|운영체제]]는 실제로 [[259_paging|페이징]]을 중심에 두고, 필요하면 [[364_segmentation|세그멘테이션]]의 개념적 [[571_protection_vs_security|보호]]를 일부 결합한다. 예를 들어 프로세스 주소 공간을 코드/[[001_dikw_pyramid|데이터]]/힙/스택으로 나누어 이해하되, 실제 적재와 [[571_protection_vs_security|보호]]는 [[286_page_frame|페이지]] 단위로 수행한다. 이 때문에 [[259_paging|페이징]]은 컴퓨터구조만의 주제가 아니라 [[001_operating_system_purpose|운영체제]]의 [[387_page_fault|페이지 부재]] 처리, 보안의 NX (No-eXecute) [[073_bit|비트]], 가상화의 EPT (Extended [[286_page_frame|Page]] Tables)와 NPT (Nested [[286_page_frame|Page]] Tables), [[282_performance_tactics|성능]] 최적화의 Huge Page로 확장된다.

또한 [[259_paging|페이징]]은 TLB와 떼어 놓고 이해할 수 없다. [[353_page_table|페이지 테이블]]이 너무 크고 변환이 잦기 때문에, 실제 [[282_performance_tactics|성능]]은 [[259_paging|페이징]] 자체보다 "[[259_paging|페이징]]을 얼마나 빠르게 숨기느냐"에 달려 있다. 그래서 [[259_paging|페이징]]은 메모리 공간 효율 문제를 해결한 뒤, TLB와 다단계 [[353_page_table|페이지 테이블]]을 통해 시간 효율 문제까지 보완하는 방향으로 진화했다.

- **📢 섹션 요약 비유**: [[364_segmentation|세그멘테이션]]이 방 용도에 따라 크기를 다르게 짓는 맞춤형 창고라면, [[259_paging|페이징]]은 모든 칸을 같은 크기로 만든 물류센터다. 맞춤성은 줄지만, 배치와 이동은 훨씬 빨라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[259_paging|페이징]]은 단순히 "메모리를 잘게 쪼갠다"가 아니라 [[352_page_size|페이지 크기]], 변환 비용, 교체 비용, [[571_protection_vs_security|보호]] [[164_policy|정책]]을 함께 설계하는 문제다. 특히 기술사 관점에서는 [[259_paging|페이징]]의 장점만 말하는 답안보다, **어떤 워크로드에서 어떤 크기와 [[164_policy|정책]]이 유리한지**를 판단하는 문장이 중요하다.

대표적인 의사결정 포인트는 [[352_page_size|페이지 크기]]다. 기본 4KB [[286_page_frame|페이지]]는 [[341_internal_fragmentation|내부 단편화]]를 줄이고 세밀한 [[571_protection_vs_security|보호]]에 유리하지만, 대용량 [[001_dikw_pyramid|데이터]]베이스나 인메모리 분석처럼 수십 GB~수 TB 영역을 자주 순차 접근하는 워크로드에서는 [[357_tlb|TLB]] 엔트리가 너무 빨리 소진된다. 이 경우 Huge Page를 쓰면 [[357_tlb|TLB]] 적중률과 [[353_page_table|페이지 테이블]] 효율이 개선된다. 반대로 작은 객체가 많고 접근 패턴이 산발적이면 큰 [[286_page_frame|페이지]]는 낭비와 I/O 증폭을 키울 수 있다.

운영 측면에서는 [[387_page_fault|페이지 부재]]율과 스왑 활동을 구분해서 봐야 한다. 가벼운 [[387_page_fault|페이지 부재]]는 정상 동작의 일부일 수 있지만, 지속적인 major fault와 디스크 스왑이 늘면 작업 집합 ([[265_working_set|Working Set]])이 물리 메모리를 초과하고 있다는 뜻이다. 이 상태를 방치하면 [[257_thrashing|스래싱]] ([[257_thrashing|Thrashing]])으로 이어져 CPU는 계산보다 [[286_page_frame|페이지]] 교체에 더 많은 시간을 쓰게 된다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. [[352_page_size|페이지 크기]] 선택이 접근 패턴과 [[357_tlb|TLB]] 용량에 맞는가?
2. [[353_page_table|페이지 테이블]] 메모리 사용량과 [[517_huge_page|Huge Page]] 이득을 함께 계산했는가?
3. 실행 금지, 읽기 전용, [[542_cow_file_system|Copy-on-Write]] 같은 [[286_page_frame|페이지]] [[571_protection_vs_security|보호]] [[164_policy|정책]]이 설계에 반영되었는가?
4. `vmstat`, `sar`, `perf` 등으로 [[387_page_fault|page fault]], swap-in/out, [[357_tlb|TLB]] miss를 분리 관찰하는가?

### 대표 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- RAM 부족을 스왑으로 장시간 버티게 하며 "[[381_virtual_memory|가상 메모리]]가 있으니 괜찮다"고 해석하는 운영
- [[001_dikw_pyramid|데이터]] 특성을 보지 않고 무조건 Huge Page만 켜는 튜닝
- 실시간 시스템에서 [[286_page_frame|페이지]] 잠금 없이 최악 [[015_지연_데이터_관점|지연]] 시간을 보장하겠다고 주장하는 설계

- **📢 섹션 요약 비유**: [[259_paging|페이징]] 튜닝은 창고 선반 간격을 정하는 일과 같다. 칸을 너무 잘게 나누면 관리표가 너무 많아지고, 칸을 너무 크게 만들면 빈 공간이 늘어난다. 결국 물건 종류와 입출고 패턴을 보고 선반 규격을 정해야 한다.

---

## Ⅴ. 기대효과 및 결론

[[259_paging|페이징]]의 가장 큰 효과는 메모리 관리의 기준을 "연속 주소 확보"에서 "[[286_page_frame|페이지]] 단위 [[164_policy|정책]]"으로 바꾼 데 있다. 덕분에 현대 시스템은 프로세스마다 독립 주소 공간을 제공하고, 필요한 [[286_page_frame|페이지]]만 적재하며, [[286_page_frame|페이지]]별 [[571_protection_vs_security|보호]] [[073_bit|비트]]로 안전성을 강제할 수 있다. 이는 [[675_multitasking_terminology_preemptive|멀티태스킹]], [[336_library_vs_framework|라이브러리]] 공유, [[131_mmap_ipc|메모리 맵 파일]], 프로세스 격리 같은 현대 [[001_operating_system_purpose|운영체제]] 기능의 바닥을 이룬다.

다만 [[259_paging|페이징]]은 공짜가 아니다. [[353_page_table|페이지 테이블]] 메모리 오버헤드, [[357_tlb|TLB]] 미스 비용, [[341_internal_fragmentation|내부 단편화]], [[387_page_fault|페이지 부재]] [[015_지연_데이터_관점|지연]]이 항상 따라온다. 따라서 좋은 설계는 "[[259_paging|페이징]]을 쓰느냐"가 아니라 "[[259_paging|페이징]]의 비용이 드러나지 않도록 지역성, 메모리 용량, [[352_page_size|페이지 크기]], 교체 [[164_policy|정책]]을 함께 맞추는가"로 평가해야 한다.

앞으로의 방향도 이 연장선에 있다. 첫째, 다단계 [[353_page_table|페이지 테이블]]과 역페이지 테이블 같은 구조로 [[012_metadata|메타데이터]] 부담을 줄인다. 둘째, Huge Page와 하드웨어 [[286_page_frame|페이지]] 워커 개선으로 변환 비용을 낮춘다. 셋째, 가상화와 [[441_cxl|CXL]] ([[441_cxl|Compute Express Link]]) 같은 확장 메모리 환경에서도 [[286_page_frame|페이지]] 단위 추상화를 유지하되 계층 간 [[015_지연_데이터_관점|지연]] 차이를 더 정교하게 다룬다.

결국 [[259_paging|페이징]]은 "메모리를 잘게 자르는 기술"이 아니라 **주소 공간을 질서 있게 운영하기 위한 고정 크기 계약**으로 기억해야 한다. [[342_external_fragmentation|외부 단편화]]를 없애고 운영 [[164_policy|정책]]의 기반을 제공했지만, [[282_performance_tactics|성능]]은 언제나 변환 비용과 지역성 관리 위에서만 성립한다.

- **📢 섹션 요약 비유**: [[259_paging|페이징]]은 도시 전체 땅을 같은 크기 필지로 정리한 도시계획과 같다. 구획이 일정해지면 배치와 관리가 쉬워지지만, 교통과 인프라를 함께 설계하지 않으면 도시가 넓어도 살기 불편해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [[381_virtual_memory|가상 메모리]] ([[381_virtual_memory|Virtual Memory]]) | [[259_paging|페이징]]을 바탕으로 프로세스마다 독립 주소 공간을 제공한다. |
| [[353_page_table|페이지 테이블]] ([[353_page_table|Page Table]]) | [[286_page_frame|페이지]] 번호를 프레임 번호와 [[571_protection_vs_security|보호]] 정보로 연결하는 핵심 장부다. |
| [[357_tlb|TLB]] ([[291_tlb|Translation Lookaside Buffer]]) | [[259_paging|페이징]]의 주소 변환 비용을 캐시해 실효 [[282_performance_tactics|성능]]을 만든다. |
| [[387_page_fault|페이지 부재]] ([[387_page_fault|Page Fault]]) | 필요한 [[286_page_frame|페이지]]가 메모리에 없을 때 [[001_operating_system_purpose|운영체제]]가 적재를 개입하는 사건이다. |
| [[341_internal_fragmentation|내부 단편화]] ([[341_internal_fragmentation|Internal Fragmentation]]) | 고정 크기 [[286_page_frame|페이지]]의 대가로 마지막 [[286_page_frame|페이지]] 일부가 남아 발생하는 낭비다. |
| [[517_huge_page|Huge Page]] | 큰 [[286_page_frame|페이지]]로 [[357_tlb|TLB]] 부담을 줄이지만, 낭비와 세밀성 손실이 따른다. |
| [[307_memory_protection|메모리 보호]] ([[307_memory_protection|Memory Protection]]) | [[286_page_frame|페이지]]별 권한 [[073_bit|비트]]로 읽기/[[289_cqrs_db|쓰기]]/실행 [[164_policy|정책]]을 강제한다. |

### 📈 관련 키워드 및 발전 흐름도

```text
연속 할당 · 외부 단편화 (External Fragmentation)
        │
        ▼
페이징 (Paging) · 페이지/프레임 고정 크기 분할
        │
        ▼
페이지 테이블 (Page Table) · PTE (Page Table Entry)
        │
        ▼
TLB (Translation Lookaside Buffer) · 다단계 페이지 테이블
        │
        ▼
요구 페이징 (Demand Paging) · 페이지 부재 (Page Fault)
        │
        ▼
Huge Page · 역페이지 테이블 · 가상화 이중 주소 변환
```

이 흐름은 "[[291_fragmentation_and_reassembly_process|단편화]] 해결 → 주소 변환 정립 → 변환 가속 → [[331_dynamic_loading|동적 적재]] → 현대 확장"으로 이어지는 [[259_paging|페이징]]의 발전 맥락을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[259_paging|페이징]]은 커다란 그림책을 똑같은 크기 상자에 나눠 담는 방법이에요.
2. 상자 크기가 모두 같아서 빈 선반이 어디 있든 하나씩 쏙 넣을 수 있어요.
3. 대신 상자 위치를 적은 목록을 잘 챙겨야 하고, 마지막 상자에 조금 빈 공간이 남을 수도 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 285 / 803

← **이전**: [[284_mmu|284. MMU (Memory Management Unit)]]
**다음**: [[286_page_frame|286. 페이지 (Page)와 프레임 (Frame)]] →

---
