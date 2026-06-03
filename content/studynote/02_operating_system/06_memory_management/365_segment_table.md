+++
title = "365. 세그먼트 테이블 (Segment Table) - 기준(Base) 주소와 한계(Limit) 길이"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 세그먼트 테이블([Segment](/knowledge-base/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/) Table)은 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) 기법에서 CPU가 요구한 2차원 [논리 주소](/knowledge-base/studynote/02_operating_system/06_memory_management/322_logical_virtual_address/)(세그먼트 번호 $s$, 오프셋 $d$)를 실제 물리 메모리 주소로 변환해 주는 <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/328_mmu/">MMU</a> 내부의 핵심 하드웨어 맵핑 장부</strong>다.
> 2. **가치**: [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)이 오직 '시작 주소(Frame)'만 기록하는 1차원적 장부라면, 세그먼트 테이블은 조각의 크기가 제각각이므로 각 줄마다 <strong>'물리적 시작 주소(Base)'와 '해당 조각의 최대 크기(Limit)' 두 가지를 동시에 품고 있는 2차원 방어 장부</strong>의 역할을 한다.
> 3. **융합**: 번역 과정에서 오프셋 $d$가 Limit을 넘어서는지 실시간으로 검사하는 [트랩](/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/)([Trap](/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/)) 하드웨어 로직과 결합되어 있으며, 이 깐깐한 경계 검사가 바로 <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/">Segmentation</a> Fault(세그폴트)</strong>를 발생시키는 원천 메커니즘이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 세그먼트 테이블은 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) 아키텍처에서 [논리 주소](/knowledge-base/studynote/02_operating_system/06_memory_management/322_logical_virtual_address/)를 물리 주소로 이어주는 자료구조다. 장부의 각 줄(Entry)은 해당 세그먼트가 메모리의 어디에 처박혀 있는지 알려주는 `Base`와, 그 세그먼트의 덩치가 도대체 얼만한지 알려주는 `Limit`의 쌍(Pair)으로 구성되어 있다.
- **필요성**: [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) 시스템에서는 모든 방이 4KB로 획일화되어 있어서, 방 번호만 알면 크기 검사는 필요가 없었다. 100보 이상 걸어갈 일이 없으니까. 하지만 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)은 1번 방(세그먼트)은 5MB짜리 운동장이고, 2번 방은 10바이트짜리 공중전화 박스다. 만약 2번 방에서 500보를 걸어가라는 악성 명령(해킹)이 떨어지면, 10바이트를 뚫고 옆방의 남의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 훔쳐보는 참사가 벌어진다. 이를 기계적으로 막아낼 '개별 맞춤형 철조망(Limit)'이 장부마다 절대적으로 필요했다.

- **등장 배경 및 아키텍처 차별점**:
  1. **가변 크기의 딜레마**: 프로그램 조각을 의미 단위로 잘라냈기 때문에(예: main함수 3KB, math함수 80KB), 조각 크기를 예측할 수 없다.
  2. **1차원 장부의 파괴**: [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)처럼 시작 주소만 적어두면 악성 오프셋 침범을 막을 도리가 없었다.
  3. **Limit의 의무화**: 장부 한 줄 한 줄에 반드시 이 조각의 합법적인 길이를 명시하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 필드(Limit)를 추가하여 하드웨어적 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)벽을 세웠다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">세그먼트 테이블(Segment Table)의 내부 데이터 구조</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">논리 주소 공간 (프로그래머가 작성한 의미 단위)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Seg 0 (Main 함수) : 1000 Bytes</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Seg 1 (수학 라이브러리) : 400 Bytes</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Seg 2 (배열 데이터) : 600 Bytes</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▶ 세그먼트 테이블 (메모리에 상주)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Seg #</div><div class="kb-diagram-cell">Limit (크기)</div><div class="kb-diagram-cell">Base (시작점)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">0</div><div class="kb-diagram-cell">1000</div><div class="kb-diagram-cell">1400</div><div class="kb-diagram-cell">◀ Main 함수 매핑</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1</div><div class="kb-diagram-cell">400</div><div class="kb-diagram-cell">6300</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2</div><div class="kb-diagram-cell">600</div><div class="kb-diagram-cell">4300</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">※ 핵심: Base가 뒤죽박죽인 건 비연속 할당이니까 당연함.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">진짜 무서운 건 Limit가 제각각 다르게 통제된다는 점!</div></div>
</div>
</div>


**[다이어그램 해설]** 테이블 구조를 보면 [연속 할당](/knowledge-base/studynote/02_operating_system/09_file_system/523_contiguous_allocation/) 시절 전체 프로세스에 딱 하나 걸려있던 `Limit/Base 레지스터`가 아예 조각조각마다 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)의 형태로 수십 개 내려앉은 모습이다. 이 표 덕분에, OS는 600바이트짜리 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)(Seg 2)에 700바이트를 밀어 넣으려는 [버퍼 오버플로우](/knowledge-base/studynote/02_operating_system/10_security/591_buffer_overflow/) 해킹 시도를 이 테이블의 Limit 값만 비교해서 나노초 단위로 차단할 수 있다.

- **📢 섹션 요약 비유**: 부동산 등기부등본(세그먼트 테이블)입니다. "땅의 주소(Base)"만 적혀있는 게 아니라, "몇 평(Limit)"인지 정확히 적혀있어서, 내 땅 주소에서 시작했어도 남의 땅 평수를 침범해 울타리를 치면 구청에서 쇠고랑을 채우는 엄격한 문서입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 주소 번역 및 하드웨어 [트랩](/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/)([Trap](/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/)) 3단계 방어선

CPU가 뱉어낸 [논리 주소](/knowledge-base/studynote/02_operating_system/06_memory_management/322_logical_virtual_address/) `<s, d>`가 물리 메모리에 도달하기까지, [MMU](/knowledge-base/studynote/02_operating_system/06_memory_management/328_mmu/) 내부에서는 삼엄한 2중 검문소가 돌아간다. 



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MMU의 세그먼트 주소 번역 및 보안 트랩 흐름도</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">CPU 명령</div><div class="kb-diagram-note">JUMP &lt;Seg 2, Offset 700&gt; (2번 조각의 700번째로 가라)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▼ 1차 방어선 (STLR)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">SegFault 에러 사살</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(네, 정상적인 조각 번호입니다.)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">세그먼트 테이블(장부) 조회</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Base: 4300, Limit: 600 꺼내옴.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▼ 2차 방어선 (크기 오버플로우 체크)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">SegFault 에러 사살</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(※ 700을 요구했는데 한계가 600이므로 💥여기서 처형됨!)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Base(4300) + d (통과 시)</div><div class="kb-diagram-cell">──▶ 물리 주소 완성! (RAM 접근)</div></div>
</div>
</div>



**[다이어그램 해설]** [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) 번역 과정과의 가장 큰 차이점은 '2차 방어선(Limit Check)'의 존재 유무다. [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/)에서는 $d$ 값을 검사하는 하드웨어 게이트가 존재하지 않는다. (그냥 뒤에 비트를 붙여버림). 하지만 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)은 덧셈(+)을 하기 전 무조건 "Limit보다 $d$가 작은가?"를 빼기 비교 회로로 통과해야 한다. 이 한 번의 비교 연산 회로가 추가됨으로써 번역 속도는 [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/)보다 필연적으로 더 느려질 수밖에 없는 하드웨어적 한계를 지닌다.

---

### STBR과 STLR의 역할

[페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)에 PTBR이 있듯, 세그먼트 테이블도 램(RAM)에 상주하므로 이를 가리키는 포인터 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 세트가 CPU 안에 존재한다.
- <strong>STBR (<a href="/knowledge-base/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/">Segment</a>-Table <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/329_base_register/">Base Register</a>)</strong>: 현재 프로세스의 세그먼트 테이블이 램의 몇 번지에 있는지 가리키는 닻(Anchor). [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 시 이 값만 바꾼다.
- <strong>STLR (<a href="/knowledge-base/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/">Segment</a>-Table Length <a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/">Register</a>)</strong>: 현재 프로세스가 도대체 '몇 개'의 세그먼트 조각을 가지고 있는지(예: 3조각) 장부의 총길이를 명시. (위 회로도의 1차 방어선을 담당).

- **📢 섹션 요약 비유**: STBR이 내비게이션에 찍힌 '호텔 로비 주소'라면, STLR은 그 호텔에 '총 몇 층까지 있는지'를 알려주는 정보입니다. 10층짜리(STLR) 호텔 로비(STBR)에 가서 "15층 버튼(오류)"을 누르면 엘리베이터가 즉시 경고음을 울리는 안전장치입니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 엔트리(PTE) vs 세그먼트 테이블 엔트리(STE)

장부의 1줄을 구성하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 필드의 철학적 차이다.

| 항목 | [Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) Entry (PTE) | [Segment](/knowledge-base/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/) Table Entry (STE) |
|:---|:---|:---|
| **위치 정보** | 물리 **프레임(Frame) 번호** (단순 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)) | 물리 **Base 주소** ([바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 단위의 절대 주소) |
| **크기 제어** | 없음 (프레임 크기는 4KB로 항상 고정 불변) | **Limit 값 필수** (세그먼트마다 크기가 천차만별) |
| **오프셋 결합**| `Frame 번호` 뒤에 `오프셋`을 텍스트처럼 **이어 붙임(Bypass)** | `Base 값`과 `오프셋`을 하드웨어 가산기로 **더함(Addition)** |
| <strong>보안/<a href="/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a></strong> | 조각 안에 코드/[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 섞여 있어 권한 제어 애매함 | 코드, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 완벽히 분리되어 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 락킹이 극강의 투명성을 가짐 |

### [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) ([External Fragmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/))의 필연성

세그먼트 테이블의 `Base` 필드를 쭉 들여다보면, 물리 메모리의 어떤 곳은 4300번지, 어떤 곳은 6300번지 등 제멋대로 시작한다.
- 조각이 빠져나가면 600바이트 구멍, 400바이트 구멍이 남게 된다.
- 이 구멍들은 크기가 고정되어 있지 않아, 나중에 1000바이트 세그먼트가 오면 빈 공간의 합은 1000인데 들어갈 곳이 없는 '[외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)'가 무조건 발생한다.
- 즉, 세그먼트 테이블은 <strong><a href="/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a>적 <a href="/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a>와 공유에서는 천재적이지만, 물리적 공간 효율에서는 낙제점</strong>을 받은 기형적 장부다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">장부 종류</div><div class="kb-diagram-cell">주소 결합 연산</div><div class="kb-diagram-cell">크기 방어(Limit)</div><div class="kb-diagram-cell">물리 단편화 발생</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">페이지 테이블</div><div class="kb-diagram-cell">단순 이어붙임</div><div class="kb-diagram-cell">필요 없음</div><div class="kb-diagram-cell">내부 미세 단편화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">세그먼트 테이블</div><div class="kb-diagram-cell">덧셈 연산(느림)</div><div class="kb-diagram-cell">무조건 필수 (느림)</div><div class="kb-diagram-cell">☠️ 치명적 외부 단편화</div></div>
</div>
</div>


**[매트릭스 해설]** 하드웨어 설계자 입장에서 세그먼트 테이블은 쳐다보기도 싫은 존재다. 주소를 1번 바꿀 때마다 덧셈과 크기 비교(뺄셈)라는 무거운 연산을 매 클럭마다 돌려야 하고, 기껏 돌렸더니 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) 때문에 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)([Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/))까지 해달라 떼를 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 때문이다. 결국 순수 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) 아키텍처는 이 테이블의 오버헤드와 파편화라는 십자포화를 맞고 역사 속으로 사라졌다.

- **📢 섹션 요약 비유**: [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) 장부는 블록의 '레고 칸 번호'만 불러주면 1초 만에 딱 끼워지는 기계식 매뉴얼이지만, 세그먼트 장부는 블록의 '밀리미터(mm) 길이와 넓이'까지 일일이 계산해서 끼워 넣어야 하는 수제작 공예품 가이드와 같아 속도가 너무 느립니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 인텔 x86의 GDT/LDT 흑역사
1. **인텔의 야심작 (80286)**: 
   - 32비트 시대를 열며 인텔은 이 우아한 세그먼트 테이블 기술을 CPU 하드웨어 단에 완전히 박아넣었다. 
   - 시스템 전역 장부인 <strong>GDT(Global Descriptor Table)</strong>와 프로세스 개별 장부인 <strong>LDT(Local Descriptor Table)</strong>를 만들고, 이 장부를 거치지 않고서는 램을 1바이트도 만질 수 없게 아키텍처를 고정해 버렸다.
2. <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a>(Linux/Windows)의 반란</strong>:
   - 세그먼트 테이블 연산이 너무 느리고 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)가 끔찍하자, 리눅스 토발즈와 윈도우 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 개발자들은 이 하드웨어를 우회하기로 결심했다.
3. **Flat Memory Model (투명 인간 기법)**:
   - [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 개발자들은 GDT(세그먼트 테이블) 안에 딱 4개의 빈 껍데기 세그먼트([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 코드, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 유저 코드, 유저 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))만 만들어 두고, <strong>이 4개의 Base 주소를 몽땅 0번지로, Limit을 몽땅 4GB(무한대)로 세팅</strong>해 버렸다.
   - CPU가 억지로 이 세그먼트 테이블을 읽고 덧셈을 해봐야 `가상 주소 + 0 = 가상 주소`, `Limit은 4GB 통과`가 되면서 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 0으로 [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) 유닛으로 주소를 그대로 패스해 버리게 만들었다. 
   - 즉, 현업 실무에서는 이 세그먼트 테이블을 "어쩔 수 없이 거쳐 가야 하는 바보 같은 0 더하기 관문"으로 전락시켜 버린 것이다.

### 진정한 유산: [Segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) Fault (SIGSEGV)
비록 메모리 할당 장부로서의 세그먼트 테이블은 죽었지만, 이 장부가 행하던 <strong>'Limit Check(경계 검사)'의 철학</strong>은 [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) 테이블의 V/I(유효/무효) 비트로 고스란히 이식되었다. 그래서 오늘날 리눅스에서 [포인터 배열](/knowledge-base/studynote/05_database/07_exam_summary/423_non_clustered_index/) 범위를 넘어서는 버그를 낼 때, "[Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Limit Fault"가 아니라 여전히 <strong><code>Segmentation fault (core dumped)</code></strong>라는 낡은 이름표를 달고 프로세스가 사살되는 것이다.

- **📢 섹션 요약 비유**: 세그먼트 테이블은 건물 입구에 설치된 깐깐한 전신 스캐너(Limit 검사기)였는데, 검사 시간이 너무 오래 걸려 손님들이 화를 내자, 아예 기계의 경고 센서를 다 끄고(Base 0, Limit 무한대) 그냥 걸어가게 방치해 둔 최신 건물의 멍청해진 스캐너와 같습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 내용 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a>적 <a href="/knowledge-base/studynote/02_operating_system/10_security/602_sandboxing_kernel_wrapper/">샌드박싱</a> 확립</strong> | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/), [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 코드 등 덩어리 전체의 Limit를 하드웨어적으로 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)하는 직관적 [샌드박싱](/knowledge-base/studynote/02_operating_system/10_security/602_sandboxing_kernel_wrapper/) 모델 제시 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/333_shared_library/">공유 라이브러리</a> 기초</strong> | 코드를 찢지 않고 온전한 1개의 세그먼트로 보존함으로써, R/O 비트를 통한 프로세스 간 코드 공유의 수학적 토대 마련 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/">페이징</a> 진화의 반면교사</strong> | 덧셈 연산과 가변 크기 장부의 속도 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) 지옥을 실증함으로써 [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) 아키텍처의 위대함을 역설적으로 증명 |

### 결론 및 미래 전망

세그먼트 테이블 ([Segment](/knowledge-base/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/) Table)은 기계의 효율성보다 프로그래머의 사고방식([배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/), 함수, 힙, [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/))을 존중하여 메모리 장부를 설계했던 눈물겨운 휴머니즘의 산물이다. 조각의 시작과 끝(Base & Limit)을 명확히 정의하는 이 2차원 장부는 보안과 공유에 있어서는 완벽에 가까운 투명성을 보여주었지만, 가변 분할이 낳는 파편화의 재앙([압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 오버헤드)을 극복하지 못하고 결국 무식하지만 효율적인 [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) 테이블의 승리로 막을 내렸다. 오늘날 x86 하드웨어 안에서 Base=0, Limit=MAX로 세팅된 채 숨만 쉬고 있는 이 테이블은, 소프트웨어의 우아함과 하드웨어의 무자비한 물리적 효율이 부딪혔을 때 결국 기계적 효율이 이길 수밖에 없다는 시스템 아키텍처 역사의 차가운 묘비명으로 남아있다.

- **📢 섹션 요약 비유**: 책의 내용(의미)에 따라 목차 장부를 만들려다 글자 수가 안 맞아 인쇄기가 고장([외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)) 나는 바람에, 결국 내용은 다 무시하고 무조건 4KB 단위로 잘라 목차 장부([페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/))를 인쇄하는 공장식 찍어내기가 문학적 낭만(세그먼트 테이블)을 무너뜨린 역사입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [역 페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/363_inverted_page_table/) ([Inverted Page Table](/knowledge-base/studynote/02_operating_system/06_memory_management/363_inverted_page_table/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) ([Segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [세그멘테이션과 외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/366_segmentation_external_fragmentation/) ([가변 크기이므로 재발생](/knowledge-base/studynote/02_operating_system/06_memory_management/366_segmentation_external_fragmentation/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [세그멘테이션 기반 페이징](/knowledge-base/studynote/02_operating_system/06_memory_management/367_paged_segmentation/) ([Paged Segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/367_paged_segmentation/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">세그멘테이션 (Segmentation)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">세그먼트 테이블 (Segment Table)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">세그멘테이션과 외부 단편화 (가변 크기이므로 재발생)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">세그멘테이션 기반 페이징 (Paged Segmentation)</div></div>
</div>
</div>



이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 세그먼트 테이블 ([Segment](/knowledge-base/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/) Table)은 컴퓨터가 메모리를 방처럼 나눠 쓰고 주소를 찾는 방법이에요.
2. 먼저 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) ([Segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/))을 이해하면 세그먼트 테이블 ([Segment](/knowledge-base/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/) Table)이 왜 필요한지 더 쉽게 보여요.
3. 그래서 세그먼트 테이블 ([Segment](/knowledge-base/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/) Table)을 잘 알면 나중에 [세그멘테이션과 외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/366_segmentation_external_fragmentation/) ([가변 크기이므로 재발생](/knowledge-base/studynote/02_operating_system/06_memory_management/366_segmentation_external_fragmentation/))도 훨씬 쉽게 배울 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 365 / 800

← **이전**: [364. 세그멘테이션 (Segmentation) - 사용자 관점의 가변 크기 논리적 단위(함수, 객체) 분할](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)
**다음**: [366. 세그멘테이션과 외부 단편화 (가변 크기이므로 재발생) (Segmentation External Fragmentation)](/knowledge-base/studynote/02_operating_system/06_memory_management/366_segmentation_external_fragmentation/) →

---
