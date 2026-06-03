+++
weight = 594
title = "594. 가상 주소 공간 구조 무작위화 (ASLR) - 버퍼/스택 라이브러리 주소 랜덤 배치 방어망"
date = "2026-05-09"
[extra]
categories = "studynote-operating-system"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[374_aslr|ASLR]] (Address Space Layout Randomization)은 프로그램이 실행될 때마다 [[057_stack|스택]]([[057_stack|Stack]]), 힙([[078_heap_datastructure|Heap]]), [[333_shared_library|공유 라이브러리]]([[333_shared_library|Shared Library]]), 그리고 실행 [[501_file_definition_logical_record|파일]](Executable)의 메모리 로드 주소를 무작위로 변경하는 [[001_operating_system_purpose|운영체제]] (OS, [[001_operating_system_purpose|Operating System]]) 레벨의 보안 기술이다.
> 2. **가치**: 해커가 [[591_buffer_overflow|버퍼 오버플로우]] ([[591_buffer_overflow|Buffer Overflow]])나 [[596_return_oriented_programming|ROP]] ([[596_return_oriented_programming|Return-Oriented Programming]]) 공격을 시도할 때, 특정 [[592_shellcode_injection|셸코드]]([[592_shellcode_injection|Shellcode]])나 [[596_return_oriented_programming|ROP]] [[345_gadget_rop|가젯]](Gadget)의 메모리 주소를 미리 예측할 수 없게 만들어 익스플로잇 (Exploit) 성공률을 0에 가깝게 떨어뜨린다.
> 3. **융합**: [[001_dikw_pyramid|데이터]] 실행 방지 ([[336_dep|DEP]], [[336_dep|Data Execution Prevention]])와 융합(Combo)되어 현대 시스템 보안의 양대 산맥을 이루며, 이를 완벽하게 지원하기 위해서는 컴파일러 수준에서 위치 독립 실행 [[501_file_definition_logical_record|파일]] ([[338_pie|PIE]], [[338_pie|Position Independent Executable]]) 옵션이 반드시 활성화되어야 한다.

---

## Ⅰ. 개요 및 필요성

**개념 및 정의**
주소 공간 [[055_array|배열]] 무작위화 ([[374_aslr|ASLR]], Address Space Layout Randomization)는 프로세스가 [[381_virtual_memory|가상 메모리]] 공간([[381_virtual_memory|Virtual Memory]] Space)에 로드될 때 주요 메모리 세그먼트들의 시작 주소를 난수(Random Number)를 기반으로 다르게 배치하는 기술이다. 이를 통해 공격자가 시스템의 고정된 주소값을 하드코딩하여 악용하는 것을 방지한다.

**필요성 및 등장 배경**
과거의 [[001_operating_system_purpose|운영체제]](예: 윈도우 [[073_xp_extreme_programming|XP]] SP2 이전, [[459_quic_fec_forward_error_correction|초기]] 리눅스 [[022_kernel_role|커널]])에서는 동일한 프로그램을 여러 번 실행하더라도 [[057_stack|스택]], 힙, [[336_library_vs_framework|라이브러리]]가 항상 동일한 가상 주소에 매핑되었다. 해커는 자신의 시스템에서 해당 프로그램의 취약점을 분석해 [[592_shellcode_injection|셸코드]] 주소나 `libc.so` 내부의 `system()` 함수 주소를 알아낸 뒤, 그 고정된 주소를 공격 페이로드에 하드코딩하여 전 세계 모든 동일 시스템을 일격에 해킹할 수 있었다. (이를 "Return-to-libc" 공격이라 한다.)

```text
┌─────────────────────────────────────────────────────────────┐
│      ASLR 미적용 vs ASLR 적용 시의 메모리 매핑 비교도       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [ASLR 미적용 (고정 주소)]                                  │
│  실행 1차            실행 2차             해커의 관점       │
│  0x08048000 [Code]   0x08048000 [Code]    ← 주소 고정       │
│  0x40000000 [libc]   0x40000000 [libc]    ← 주소 고정       │
│  0x0804a000 [Heap]   0x0804a000 [Heap]    ← 주소 고정       │
│  0xbffff000 [Stack]  0xbffff000 [Stack]   ← 주소 고정       │
│  => 해커: "system() 함수는 무조건 0x40001234에 있군!"       │
│                                                             │
│  [ASLR 적용 (무작위 주소)]                                  │
│  실행 1차            실행 2차             해커의 관점       │
│  0x56a42000 [Code]   0x51b8c000 [Code]    ← 매번 변경       │
│  0x7f23a000 [libc]   0x7f99c000 [libc]    ← 매번 변경       │
│  0x56a4b000 [Heap]   0x51b8e000 [Heap]    ← 매번 변경       │
│  0x7fffbc00 [Stack]  0x7fffc800 [Stack]   ← 매번 변경       │
│  => 해커: "주소가 계속 바뀌어서 어디로 점프해야 할지 모름!" │
└─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 비교도는 ASLR이 공격자의 예측 가능성을 어떻게 파괴하는지 명확하게 보여준다. ASLR이 없던 시절에는 메모리 레이아웃이 정적이어서 공격 페이로드(Payload)를 한 번만 잘 만들면 범용적으로 사용할 수 있었다. 하지만 ASLR이 적용된 환경에서는 [[022_kernel_role|커널]]([[022_kernel_role|Kernel]])이 프로세스를 생성할 때(`execve` 시스템 콜 호출 시), [[328_mmu|MMU]]([[284_mmu|Memory Management Unit]])에 [[009_config|설정]]할 가상 주소의 Base offset(기준 주소)을 난수 발생기(Random Number Generator)를 통해 무작위로 밀어버린다(Shift). 결과적으로, 공격자가 [[095_overflow|오버플로우]]를 발생시키더라도 변조해야 할 정확한 리턴 주소(RET)를 알 수 없어 프로세스는 `Segmentation Fault`를 내고 죽어버린다.

- **📢 섹션 요약 비유**: 해커가 은행(프로그램) 도면을 훔쳐서 금고(system 함수) 위치를 완벽히 외웠는데, 은행이 매일 아침마다 건물의 방 구조를 통째로 랜덤하게 재배치해 버리는 마법과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소 (ASLR의 메모리 오프셋 난수화)

| 요소명 | 역할 | 내부 동작 | 비유 |
|:---|:---|:---|:---|
| **[[749_memory_mapped_file_mmap|mmap]] Base Randomization** | [[333_shared_library|공유 라이브러리]](.so, .dll) 주소 무작위화 | `mmap()` 호출 시 시작 주소에 랜덤 오프셋 적용 | 책장의 책 위치 매일 바꾸기 |
| **[[057_stack|Stack]] Randomization** | [[057_stack|스택]]([[057_stack|Stack]]) 영역 시작 주소 무작위화 | `execve()` 실행 시 [[459_quic_fec_forward_error_correction|초기]] [[166_sp|스택 포인터]]([[382_esp_encapsulating_security_payload_confidentiality|ESP]]/RSP)를 난수만큼 하향 이동 | 계단 시작 높이 조절 |
| **[[078_heap_datastructure|Heap]] Randomization** | 힙([[078_heap_datastructure|Heap]]) 영역 시작 주소 무작위화 | `brk()` 호출 시 힙 베이스 주소에 랜덤 [[098_padding_convolutional_neural_network_same_valid|패딩]] 추가 | 창고 시작 지점 조절 |
| **[[338_pie|PIE]] (Position Independent Exec)** | 실행 [[501_file_definition_logical_record|파일]]([[082_process_memory_structure|Code]], [[001_dikw_pyramid|Data]]) 자체의 무작위화 | 메인 바이너리가 고정된 `0x08048000`이 아닌 임의 주소에 로드 가능토록 상대 주소 컴파일 | 건물의 기초 위치 이동 |

### 심층 동작 원리 및 [[151_entropy|엔트로피]] ([[151_entropy|Entropy]])

ASLR의 보안 강도는 주소가 얼마나 '무작위'인가를 나타내는 [[151_entropy|엔트로피]] ([[151_entropy|Entropy]])에 전적으로 의존한다. [[151_entropy|엔트로피]]가 낮으면 공격자가 무차별 대입 (Brute-Force) 공격으로 주소를 때려 맞출 수 있다. 

[[001_operating_system_purpose|운영체제]]는 [[286_page_frame|페이지]] 단위(주로 4KB = $2^{12}$ Bytes)로 메모리를 관리하므로, 시작 주소의 하위 12비트(0x000 ~ 0xFFF)는 [[286_page_frame|페이지]] 정렬([[286_page_frame|Page]] Alignment)을 위해 무작위화할 수 없고 항상 고정된다. 따라서 32비트 [[001_operating_system_purpose|운영체제]]와 64비트 [[001_operating_system_purpose|운영체제]]의 [[374_aslr|ASLR]] 방어력에는 극명한 차이가 존재한다.

```text
┌───────────────────────────────────────────────────────────────┐
│      32비트 vs 64비트 시스템에서의 ASLR 엔트로피 비교         │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  [32비트 메모리 주소 (32 Bits)]                               │
│  ┌───────────────┬───────────────────┬─────────────┐          │
│  │ 커널 전용 (8b) │ 무작위화 구역 (12b)│ 페이지 오프셋│       │
│  │ 고정          │ (Entropy)         │ 하위 12b 고정│         │
│  └───────────────┴───────────────────┴─────────────┘          │
│  => 난수화 가능 비트: 고작 8 ~ 12비트                         │
│  => 경우의 수: 2^8 ~ 2^12 = 256 ~ 4,096개                     │
│  => 공격자가 Brute-Force로 몇 분 안에 돌파 가능!              │
│                                                               │
│  [64비트 메모리 주소 (64 Bits, 48비트 가상 주소 사용)]        │
│  ┌───────┬───────────────────────────┬─────────────┐          │
│  │ 미사용 │ 무작위화 구역 (28 ~ 32b)  │ 페이지 오프셋│        │
│  │ (16b) │ (Entropy)                 │ 하위 12b 고정│         │
│  └───────┴───────────────────────────┴─────────────┘          │
│  => 난수화 가능 비트: 28 ~ 32비트                             │
│  => 경우의 수: 2^28 ~ 2^32 = 약 2.6억 ~ 40억 개               │
│  => Brute-Force 공격 사실상 불가능!                           │
└───────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 구조도는 왜 32비트 시스템에서 ASLR이 "반쪽짜리 방어막"에 불과한지를 수치적으로 증명한다. 32비트 OS에서는 유저 공간이 보통 3GB로 제한되고, [[286_page_frame|페이지]] 정렬 때문에 하위 12비트는 랜덤화할 수 없다. 결과적으로 [[336_library_vs_framework|라이브러리]]나 [[057_stack|스택]]이 가질 수 있는 시작 주소의 경우의 수([[151_entropy|엔트로피]])가 수천 개에 불과하다. 해커는 스크립트를 짜서 수천 번의 접속을 시도(Brute-forcing)하면 단 몇 분 만에 정확한 주소를 얻어낼 수 있다. 반면, 64비트 OS에서는 무작위화할 수 있는 여유 비트가 28비트 이상 확보되므로, 수십억 개의 경우의 수가 발생하여 무차별 대입 공격이 수학적·물리적으로 완전히 차단된다. 

- **📢 섹션 요약 비유**: 32비트 ASLR은 범인이 숨을 수 있는 방이 4천 개뿐이라 경찰이 금방 찾아내지만, 64비트 ASLR은 방이 40억 개나 되는 거대한 미로여서 우연히 마주칠 확률이 제로에 수렴하는 것과 같습니다.

---

## Ⅲ. 비교 및 연결

### [[374_aslr|ASLR]] 우회 기법과 방어의 창과 방패

완벽해 보이는 ASLR도 메모리 정보 누출([[612_memory_leak_detection|Memory Leak]]) 취약점 앞에서는 무력화된다. 공격자와 방어자의 진화 과정을 매트릭스로 비교한다.

| 공격자의 무기 ([[374_aslr|ASLR]] 우회 기법) | 기술적 원리 | 방어자의 방패 (OS 레벨 완화 기술) |
|:---|:---|:---|
| **메모리 릭 ([[612_memory_leak_detection|Memory Leak]])** | Format String 버그나 Out-of-bounds Read를 통해 포인터 주소를 유출. 하나의 주소만 알면 상대적 오프셋(Offset)을 더해 전체 [[336_library_vs_framework|라이브러리]] 주소를 유추. | **포인터 암호화 ([[542_pointer_authentication|Pointer Authentication]])**, 엄격한 코드 오디팅. |
| **Bypass via non-[[338_pie|PIE]] Exec** | 메인 실행 [[501_file_definition_logical_record|파일]]이 PIE가 아닌 고정 주소로 컴파일된 점을 악용해, 메인 코드 내부의 [[596_return_oriented_programming|ROP]] [[345_gadget_rop|가젯]]만 사용하여 공격. | **[[338_pie|PIE]] ([[338_pie|Position Independent Executable]])** 컴파일러 옵션 전면 강제화. |
| **[[078_heap_datastructure|Heap]] Spraying ([[349_heap_spray|힙 스프레이]])** | 거대한 크기의 NOP Sled와 [[592_shellcode_injection|셸코드]]를 힙에 무수히 많이(Spray) 뿌려, 임의의 주소로 점프해도 [[592_shellcode_injection|셸코드]]에 걸리도록 확률을 조작. | **[[078_heap_datastructure|Heap]] [[374_aslr|ASLR]] 강화** 및 브라우저의 메모리 할당 제한. |
| **[[456_brute_force|Brute Force]] (무차별 대입)** | 주소가 맞을 때까지 계속 크래시를 내며 반복 실행 시도 (주로 32비트나 분기 데몬에서 발생). | **크래시 후 재시작 [[015_지연_데이터_관점|지연]] (Crash Throttling)** 및 관제([[624_siem|SIEM]]) 알람 연동. |

ASLR을 완벽히 뚫기 위해 해커들이 사용하는 가장 우아한 기법은 '오프셋(Offset)'을 이용한 베이스 주소 계산이다. `libc`와 같은 [[336_library_vs_framework|라이브러리]]는 통째로 메모리에 로드되므로, 내부 함수들 간의 거리는 ASLR이 적용되어도 변하지 않는다.

```text
┌─────────────────────────────────────────────────────────────┐
│      메모리 릭(Memory Leak)을 통한 ASLR 무력화 (Base 도출)  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [로컬 파일 분석 (고정된 Offset)]                           │
│  libc.so 파일 내에서:                                       │
│    printf()의 오프셋 = 0x050000                             │
│    system()의 오프셋 = 0x040000                             │
│    두 함수의 거리 차이 = 0x010000 (절대 불변)               │
│                                                             │
│  [런타임 공격 시나리오 (Memory Leak 발생)]                  │
│  ① 해커가 정보 유출 취약점(예: %x 포맷스트링)으로           │
│     현재 메모리에 로드된 printf()의 주소를 빼냄.            │
│     유출된 주소 = 0x7f88a2050000                            │
│                                                             │
│  ② 해커의 실시간 수학 계산:                                 │
│     libc Base 주소 = 0x7f88a2050000 - 0x050000              │
│                    = 0x7f88a2000000                         │
│                                                             │
│  ③ 타겟 system() 주소 도출:                                 │
│     system() 주소 = libc Base (0x7f88a2000000) + 0x040000   │
│                   = 0x7f88a2040000  ← ASLR 무력화 완료!     │
└─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** ASLR은 메모리의 "시작 주소(Base Address)"를 흔드는 기술이지, [[192_module_independence|모듈]] 내부 구조를 뒤섞는 기술이 아니다. 따라서 해커가 애플리케이션의 취약점을 통해 특정 함수(예: `printf`)의 런타임 메모리 주소를 단 한 개만 알아낼 수 있다면(메모리 릭), 해커는 로컬에서 분석해 둔 [[336_library_vs_framework|라이브러리]]의 상대적 거리(Offset)를 이용하여 메모리 전체의 지도를 순식간에 재구성할 수 있다. 이 과정을 통해 ASLR의 무작위성은 완벽히 파훼되며, 알아낸 `system` 주소로 [[596_return_oriented_programming|ROP]] 페이로드를 조립하여 원격 코드 실행(RCE)을 달성한다. 이 때문에 현대 보안에서는 [[591_buffer_overflow|버퍼 오버플로우]](Write)뿐만 아니라, 메모리 내용 유출(Read) 취약점도 `Critical` 등급으로 취급된다.

- **📢 섹션 요약 비유**: 미로의 위치가 매번 바뀌더라도([[374_aslr|ASLR]]), 미로의 '내부 지도(Offset)'를 가진 사람이 '현재 내 위치 표지판([[612_memory_leak_detection|Memory Leak]])' 하나만 발견하면 즉시 출구(System 함수)를 찾아낼 수 있는 원리입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: [[338_pie|PIE]] 미적용으로 인한 [[374_aslr|ASLR]] 반쪽 방어 실패 사례

1. **상황**: 기업 인프라 팀은 리눅스 [[022_kernel_role|커널]] 파라미터 `kernel.randomize_va_space=2`를 [[009_config|설정]]하여 시스템 전역에 강력한 ASLR을 적용했다고 확신했다. 그러나 [[455_penetration_testing_vulnerability_scanning|모의 해킹]]([[676_penetration_testing|Penetration Testing]]) 결과, 자사 데몬 프로그램이 [[596_return_oriented_programming|ROP]] 공격에 속수무책으로 당해버렸다.
2. **원인 분석 (Root Cause)**: 개발팀이 C 코드를 컴파일할 때 `-fPIE -pie` 옵션을 누락했다. 이로 인해 [[057_stack|스택]], 힙, `libc.so` [[336_library_vs_framework|라이브러리]]는 무작위 주소에 배치되었으나, **가장 중요한 데몬 실행 [[501_file_definition_logical_record|파일]] 자체(.text 영역)** 는 고정된 주소(`0x400000`)에 로드되었다.
3. **공격자의 [[268_strategy_pattern|전략]]**: 해커는 `libc`의 랜덤 주소를 찾는 대신, 고정된 메인 실행 [[501_file_definition_logical_record|파일]] 내부에 존재하는 쓸만한 기계어 조각([[345_gadget_rop|가젯]])들만을 긁어모아 제한적인 [[596_return_oriented_programming|ROP]] 체인을 구성(이를 Return-to-csu, BROP 등의 심화 기법이라 함)하여 공격에 성공했다.
4. **방어자의 의사결정**: ASLR은 OS([[022_kernel_role|커널]])의 지원만으로 완성되지 않는다. 애플리케이션 자체가 무작위 주소에서 실행될 수 있도록 위치 독립 코드(PIC/[[338_pie|PIE]])로 컴파일되어야 한다. 실무자는 [[090_configuration_item|CI]]/CD 파이프라인의 빌드 스크립트에 PIE와 [[341_relro|RELRO]]([[341_relro|Relocation Read-Only]]) 강제 적용 룰을 추가해야 한다.

### 도입 [[435_checklist_based_testing|체크리스트]] (컴파일러 및 [[022_kernel_role|커널]] [[009_config|설정]])
- **리눅스 [[022_kernel_role|커널]] [[009_config|설정]]**: `sysctl -a | grep randomize_va_space`의 값이 `2`인지 [[396_validation|확인]]. (`0`=Off, `1`=[[057_stack|스택]]/[[336_library_vs_framework|라이브러리]]만, `2`=힙까지 모두 적용).
- **윈도우 PE(Portable Executable) [[009_config|설정]]**: Visual Studio 빌드 링커 옵션에서 `/DYNAMICBASE` ([[374_aslr|ASLR]] 활성화) 및 `/HIGHENTROPYVA` (64비트 고엔트로피 [[374_aslr|ASLR]])가 켜져 있는지 [[396_validation|확인]].
- **[[192_module_independence|모듈]] 전수 검사**: 프로세스 익스플로러나 `checksec` 도구를 사용하여, 로드된 모든 DLL/SO [[501_file_definition_logical_record|파일]] 중 단 하나라도 [[374_aslr|ASLR]]([[338_pie|PIE]])이 꺼진 [[192_module_independence|모듈]]이 없는지 주기적으로 [[606_auditing_linux_auditd|감사]]([[363_audit|Audit]])해야 한다. (하나의 고정 [[192_module_independence|모듈]]이 전체 방어망을 무너뜨린다.)

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **포크(Fork) 서버의 구조적 취약점**: 아파치나 Nginx처럼 메인 프로세스가 `fork()`를 통해 자식 프로세스를 생성하는 서버의 경우, 자식 프로세스는 부모의 메모리 레이아웃([[374_aslr|ASLR]] 주소)을 100% 동일하게 복제한다. 만약 자식 프로세스가 크래시되어도 메인 서버가 동일한 주소로 다시 자식을 살려낸다면, 해커는 주소가 변하지 않는다는 점을 악용해 [[074_byte|바이트]] 단위로 주소를 때려 맞추는 'Blind [[596_return_oriented_programming|ROP]]' 공격을 수행할 수 있다.

- **📢 섹션 요약 비유**: 튼튼한 금고([[374_aslr|ASLR]])를 사놓고도 정작 금고 문([[338_pie|PIE]] 옵션)을 잠그지 않거나, 10명의 경비원 중 1명(단일 [[192_module_independence|모듈]])이 매수당하면 성 전체가 함락되는 보안의 '가장 약한 고리(Weakest Link)' 원칙을 보여줍니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [[338_pie|PIE]] 미적용 [[374_aslr|ASLR]] (부분 방어) | [[338_pie|PIE]] 포함 전면 [[374_aslr|ASLR]] + [[336_dep|DEP]] 적용 | 기술적 함의 |
|:---|:---|:---|:---|
| **정량** | 실행 [[501_file_definition_logical_record|파일]] [[345_gadget_rop|가젯]]을 이용한 [[596_return_oriented_programming|ROP]] 공격 성공률 높음 | 64비트 환경에서 공격 성공률 **사실상 0% ([[612_memory_leak_detection|Memory Leak]] 없을 시)** | 공격자의 리소스 및 시간 비용 기하급수적 증가 |
| **운영** | 레거시 바이너리 호환성은 유지됨 | PIE로 인한 상대 주소 계산 비용으로 CPU 오버헤드 (약 1~3%) 발생 | 보안을 위해 극소량의 [[282_performance_tactics|성능]] 저하를 감수하는 현대 OS의 철학 |
| **정성** | 주소 하드코딩 방식의 구형 웜/[[589_virus|바이러스]] 차단 | [[761_zero_day|제로데이]] 공격 시에도 메모리 릭 취약점이 동반되어야만 Exploit 가능 | 다중 취약점 체이닝(Vulnerability [[103_chaining|Chaining]]) 강제화 |

### 미래 전망
단순한 베이스 주소 무작위화(Base [[374_aslr|ASLR]])는 메모리 릭(Leak) 한 번에 무너지는 한계가 있다. 이에 대한 대응으로 미래의 보안 기술은 **[[399_fine_grained_multithreading|Fine-Grained]] [[374_aslr|ASLR]] (세립도 [[374_aslr|ASLR]])** 로 발전하고 있다. 이는 [[192_module_independence|모듈]] 단위의 덩어리 배치가 아니라, 함수 단위, 심지어 기본 블록(Basic Block) 단위로 코드의 순서를 마구잡이로 뒤섞어버리는 기술이다. 이렇게 되면 해커가 Base 주소를 유출하더라도 함수 내부의 구조가 엉망진창이므로 [[596_return_oriented_programming|ROP]] [[345_gadget_rop|가젯]]의 위치를 전혀 유추할 수 없게 된다. 컴파일러(LLVM/Clang) 레벨에서의 런타임 난수화 기술이 [[531_cloud_native_architecture|클라우드 네이티브]] 워크로드의 핵심 방어 기제로 채택될 것이다.

### 참고 표준
- **CWE-120**: 버퍼 복사 시 입력 크기 [[395_verification_process_review|검증]] 부재
- **[[848_nist_sp_800_53|NIST SP 800-53]] (SC-18)**: 악성 코드 방지 및 [[307_memory_protection|메모리 보호]] ([[307_memory_protection|Memory Protection]])
- **Linux [[283_security_tactics|Security]] Standard**: `kernel.randomize_va_space=2` 권고안

- **📢 섹션 요약 비유**: 책장의 위치만 바꾸는 것(기본 [[374_aslr|ASLR]])을 넘어, 아예 책 속의 [[286_page_frame|페이지]] 순서까지 무작위로 섞어버리는([[399_fine_grained_multithreading|Fine-Grained]] [[374_aslr|ASLR]]) 궁극의 방어 체계로 진화하고 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[592_shellcode_injection|셸코드]] ([[592_shellcode_injection|Shellcode]]) [[480_injection|인젝션]] | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[591_buffer_overflow|버퍼 오버플로우]] 방어 하드웨어 기술 ([[335_nx_bit|NX Bit]] / [[336_dep|Data Execution Prevention]], [[336_dep|DEP]]) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[595_canary_stack_smashing_protector|카나리]] ([[595_canary_stack_smashing_protector|Canary]]) / [[057_stack|스택]] 스매싱 가드 ([[541_stack_smashing_protector|Stack Smashing Protector]]) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[596_return_oriented_programming|ROP]] ([[596_return_oriented_programming|Return-Oriented Programming]]) 기법 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[버퍼 오버플로우 방어 하드웨어 기술 (NX Bit / Data Execution Prevention, DEP)]
    │
    ▼
[가상 주소 공간 구조 무작위화 (ASLR)]
    │
    ├──▶ [카나리 (Canary) / 스택 스매싱 가드 (Stack Smashing Protector)]
    └──▶ [ROP (Return-Oriented Programming) 기법]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 해커들은 도둑질을 할 때 "3층 오른쪽 끝 방"처럼 건물의 **고정된 주소**를 외워서 빠르고 쉽게 침투해요.
2. 하지만 가상 주소 무작위화([[374_aslr|ASLR]]) 기술을 쓰면, 프로그램이 실행될 때마다 방의 위치가 마법처럼 무작위(랜덤)로 계속 바뀌어요!
3. 그래서 해커가 3층 오른쪽 방 문을 부수고 들어갔는데, 엉뚱하게도 화장실이 나와서 도둑질에 실패하고 경비원에게 잡히게 되는 거랍니다.
