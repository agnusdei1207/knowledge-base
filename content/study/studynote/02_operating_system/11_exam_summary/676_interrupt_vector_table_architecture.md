---
title: 676. 인터럽트 벡터 테이블 구조화 (Interrupt Vector Table Architecture)
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[019_interrupt_vector|인터럽트 벡터]] 테이블([[019_interrupt_vector|Interrupt Vector]] Table, IVT)은 CPU가 외부 장치의 [[017_hardware_interrupt|하드웨어 인터럽트]]나 소프트웨어 예외(Exception)를 받았을 때, **어떤 [[022_kernel_role|커널]] 함수([[020_isr|ISR]]: [[317_isr|Interrupt Service Routine]])를 실행해야 할지 찾아가는 '메모리상의 주소록([[055_array|배열]])'**이다.
> 2. **메커니즘**: [[016_interrupt_mechanism|인터럽트]]가 발생하면 장치는 CPU에 고유한 번호(Vector, 0~255)를 보낸다. CPU는 이 번호를 인덱스로 삼아 미리 설정된 IVT(또는 IDT) [[055_array|배열]]을 조회하고, 거기에 적힌 함수 포인터 주소로 [[164_pc|프로그램 카운터]]([[164_pc|PC]])를 즉시 점프시킨다.
> 3. **가치**: 이 테이블 구조 덕분에 CPU는 수많은 장치(키보드, 마우스, 디스크)가 보내는 예측 불가능한 [[130_signal|신호]]를 `if-else` 문으로 검사하는 [[448_polling_programmed_io|폴링]]([[747_io_polling_overhead|Polling]]) 오버헤드 없이, $O(1)$의 하드웨어 직통 속도로 정확한 핸들러로 라우팅할 수 있다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **[[016_interrupt_mechanism|인터럽트]] ([[016_interrupt_mechanism|Interrupt]])**: CPU가 현재 하던 일을 멈추고 우선적으로 처리해야 할 긴급한 사건이 발생했음을 알리는 [[130_signal|신호]].
  - **[[019_interrupt_vector|인터럽트 벡터]] (Vector)**: [[016_interrupt_mechanism|인터럽트]]의 종류를 식별하는 고유 번호 (예: 0번은 0으로 나누기 에러, 14번은 [[720_page_fault_isr|페이지 폴트]]).
  - **[[019_interrupt_vector|인터럽트 벡터]] 테이블 (IVT / IDT)**: 이 벡터 번호를 인덱스로 하여, 처리할 함수의 메모리 주소가 순서대로 적혀 있는 [[055_array|배열]].

- **필요성 (하드웨어와 소프트웨어의 통신 병목 해결)**: 
  - 컴퓨터에 마우스, 키보드, 랜카드, 디스크 등 수십 개의 하드웨어가 달렸다.
  - CPU가 "마우스 눌렸니? 키보드 눌렸니?"를 계속 묻고 다니는 것([[747_io_polling_overhead|Polling]])은 심각한 CPU 낭비다.
  - 그래서 장치가 CPU를 찌르는([[016_interrupt_mechanism|Interrupt]]) 방식을 택했는데, CPU가 찔렸을 때 "누가 날 찔렀지? 마우스인가? 키보드인가?"를 소프트웨어적으로 하나하나 검사하면 응답이 너무 늦다.
  - **해결책**: 장치가 CPU를 찌를 때 '번호표(Vector)'를 같이 주게 하고, CPU는 묻지도 따지지도 않고 그 번호표에 해당하는 '사물함(IVT)'을 열어 그 안에 적힌 지시서(함수 주소)대로 즉시 행동하게 만드는 하드웨어 룩업 테이블(Lookup Table)이 필요했다.

  - **테이블이 없을 때 ([[747_io_polling_overhead|Polling]])**: 학교 경비 아저씨(CPU)가 1반부터 10반까지 계속 돌아다니며 "무슨 일 있니?"라고 묻는다.
  - **[[019_interrupt_vector|인터럽트 벡터]] 테이블 (IVT)**: 경비실에 1번부터 10번까지 버튼이 있는 상황판이 있다. 3반에서 싸움이 나서 3반 학생이 비상벨을 누르면, 상황판에 3번 불이 켜진다(Vector 3). 경비 아저씨는 벽에 붙은 매뉴얼(IVT)을 본다. "3번 불: 양호 선생님 호출". 아저씨는 즉시 양호 선생님을 부른다([[020_isr|ISR]] 실행).

- **발전 과정**:
  1. **단일 [[016_interrupt_mechanism|인터럽트]]**: 모든 [[016_interrupt_mechanism|인터럽트]]가 한 곳으로 모여 OS가 `if-else`로 분기. 느리고 복잡함.
  2. **IVT ([[019_interrupt_vector|Interrupt Vector]] Table, 리얼 모드)**: [[459_quic_fec_forward_error_correction|초기]] x86 프로세서(16비트). 메모리 0번지부터 1KB 공간에 고정 할당.
  3. **IDT ([[016_interrupt_mechanism|Interrupt]] Descriptor Table, [[571_protection_vs_security|보호]] 모드)**: 현대 32/64비트 프로세서. 메모리 어디든 위치할 수 있으며, 권한(DPL) 검사 등 보안 기능이 추가된 진보된 테이블 구조.

- **📢 섹션 요약 비유**: 전화가 왔을 때 누군지 목소리를 듣고 추리하는 것이 아니라, 발신자 번호(Vector)가 뜨자마자 내 스마트폰 주소록(IVT)을 뒤져서 바로 누구인지 사진([[020_isr|ISR]])을 띄워주는 [[148_5g_embb_urllc_mmtc|초고속]] 매칭 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### x86 아키텍처의 IDT ([[016_interrupt_mechanism|Interrupt]] Descriptor Table) 구조

현대 x86 프로세서에서는 IVT 대신 **IDT**라는 용어를 사용한다. IDT는 총 256개의 엔트리(0~255번)를 가진다. 각 엔트리(Descriptor)는 8바이트(또는 16바이트) 크기다.

| 벡터 번호 | [[104_classification_analysis|분류]] | 설명 및 주요 [[016_interrupt_mechanism|인터럽트]] |
|:---:|:---|:---|
| **0 ~ 31** | **하드웨어 예외 (Exceptions)** | CPU 내부에서 발생하는 오류. (0: Divide by [[585_zero_skipping|zero]], 13: General [[571_protection_vs_security|Protection]] Fault, 14: **[[387_page_fault|Page Fault]]**) |
| **32 ~ 47** | **외부 하드웨어 (Hardware IRQ)** | 키보드, 마우스, 디스크 등 외부 기기가 PIC/APIC를 통해 발생시키는 [[016_interrupt_mechanism|인터럽트]] |
| **48 ~ 255** | **소프트웨어 [[016_interrupt_mechanism|인터럽트]] (Software)**| OS [[022_kernel_role|커널]]이 자체적으로 배정한 번호. (예: Linux의 `INT 0x80` - 시스템 콜 진입점) |

---

### [[016_interrupt_mechanism|인터럽트]] 처리 ([[339_routing_overview_best_path_selection|Routing]]) 메커니즘 4단계

마우스를 클릭했을 때 CPU가 IDT를 참조하여 어떻게 동작하는지 살펴보자.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 하드웨어 인터럽트 라우팅 및 IDT 참조 원리                │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  [상황 1: 하드웨어 이벤트 발생]                                         │
  │   - 마우스 클릭 -> 마우스 컨트롤러가 전기 신호를 보냄.                      │
  │   - APIC (인터럽트 컨트롤러)가 이를 받아 벡터 번호 [ 44번 ]을 생성하여 CPU에 쏨.│
  │                                                                   │
  │  [상황 2: CPU의 하드웨어적 반응]                                        │
  │   - CPU는 하던 연산을 즉시 멈추고, 현재 상태(PC, 플래그 레지스터 등)를 스택에 백업.│
  │   - CPU 내부의 [ IDTR 레지스터 ]를 읽어 IDT 테이블의 시작 주소를 알아냄.      │
  │                                                                   │
  │  [상황 3: IDT 룩업 (Lookup)]                                        │
  │   - IDT 시작 주소 + (44 * 8바이트) 계산 = 44번 엔트리 주소 도달.          │
  │                                                                   │
  │   [ IDT 배열 ]                                                     │
  │     ...                                                           │
  │     [ 43번 엔트리 ] -> (키보드 ISR 주소)                             │
  │     [ 44번 엔트리 ] -> (마우스 ISR 주소: 0xffffffff81abc000) ◀── 당첨!│
  │     ...                                                           │
  │                                                                   │
  │  [상황 4: 커널 공간 점프 및 ISR 실행]                                   │
  │   - CPU는 권한(Ring)을 검사한 후, PC(Program Counter)를 44번의 주소로 덮어씀.│
  │   - Linux 커널의 `mouse_interrupt_handler()` 함수가 실행됨!          │
  │   - 처리가 끝나면 `iret` (Interrupt Return) 명령으로 아까 하던 일로 복귀.   │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** IDT의 핵심은 **IDTR (IDT [[175_register_addressing|Register]])**이다. 부팅 시 리눅스 [[022_kernel_role|커널]]이 메모리 빈 공간에 이 256칸짜리 테이블을 예쁘게 그려놓고, `lidt`라는 어셈블리 [[158_instruction|명령어]]를 통해 "CPU야, 앞으로 [[016_interrupt_mechanism|인터럽트]] 들어오면 여기 메모리 주소(IDTR)를 참조해라"라고 세팅한다. 이후 [[016_interrupt_mechanism|인터럽트]]가 터지면, OS의 소프트웨어 개입 없이 **순수 하드웨어(CPU)**가 직접 산수(시작 주소 + 벡터*오프셋)를 해서 즉각 점프한다. 이것이 [[016_interrupt_mechanism|인터럽트]]가 소프트웨어 분기문(`if-else`)보다 수백 배 빠른 이유다.

---

### [[016_interrupt_mechanism|인터럽트]] 디스크립터(엔트리)의 내부 구조와 권한 제어

단순히 주소만 있는 것이 아니다. 해커가 유저 모드에서 임의의 [[016_interrupt_mechanism|인터럽트]]를 발생시켜 [[022_kernel_role|커널]]을 터뜨리는 것을 막기 위해 권한 제어가 들어간다.

- **DPL (Descriptor Privilege Level)**: 이 [[016_interrupt_mechanism|인터럽트]]를 소프트웨어적(`INT` [[158_instruction|명령어]])으로 부를 수 있는 최소 권한. 
- 예를 들어, 14번 [[286_page_frame|Page]] Fault의 DPL은 0([[022_kernel_role|커널]])이다. 유저 앱(Ring 3)이 `INT 14`를 쳐서 억지로 부르려 하면 DPL 위반으로 거부된다.
- 단, 0x80번(시스템 콜)의 DPL은 3(유저)으로 열어두어, 유저 앱이 합법적으로 [[022_kernel_role|커널]]로 넘어갈 수 있는 유일한 '개구멍'을 만들어 준다.

- **📢 섹션 요약 비유**: IDT는 성벽의 '출입증 검사소 목록'입니다. 44번 문(마우스)은 하드웨어 [[130_signal|신호]]만 들어올 수 있고, 0x80번 문(시스템 콜)은 백성(유저)도 출입증만 있으면 들어올 수 있게 권한(DPL)을 세밀하게 조율해 놓았습니다.

---

## Ⅲ. 비교 및 연결

### [[016_interrupt_mechanism|인터럽트]] vs 예외(Exception) vs [[677_trap_based_system_call_implementation|트랩]]([[677_trap_based_system_call_implementation|Trap]])

IVT를 타는 세 가지 사건의 미묘한 차이다.

| 구분 | 발생 주체 | 발생 시점 | 동기/비동기 | 예시 및 처리 방식 |
|:---|:---|:---|:---|:---|
| **[[017_hardware_interrupt|하드웨어 인터럽트]]**| **외부 장치 (I/O)** | CPU [[158_instruction|명령어]] 실행과 무관 | **[[017_hardware_interrupt|비동기적]]** | 키보드 입력. 현재 [[158_instruction|명령어]] 실행 완료 후 멈춤. |
| **예외 (Exception)**| **CPU 내부 (오류)** | 특정 [[158_instruction|명령어]] 실행 도중 | **동기적 (Fault)** | 0으로 나누기, [[387_page_fault|Page Fault]]. 오류 난 [[158_instruction|명령어]]를 나중에 **재시도**함. |
| **[[677_trap_based_system_call_implementation|트랩]] ([[677_trap_based_system_call_implementation|Trap]])** | **소프트웨어 (App)** | 특정 [[158_instruction|명령어]](`INT`) 의도적 실행 | **동기적 ([[677_trap_based_system_call_implementation|Trap]])** | 시스템 콜, 디버그(Breakpoint). 실행 후 **다음 [[158_instruction|명령어]]**부터 재개. |

이 세 가지 모두 결국 **IDT([[019_interrupt_vector|인터럽트 벡터]] 테이블)**를 조회하여 각자의 [[022_kernel_role|커널]] 함수로 점프한다는 점에서는 아키텍처가 100% 동일하다.

### 과목 융합 관점

- **[[001_operating_system_purpose|운영체제]] (OS)**: 디바이스 드라이버를 개발할 때 `request_irq()` 함수를 호출한다. 이 함수가 하는 일이 바로, [[022_kernel_role|커널]]이 미리 잡아놓은 IDT 테이블의 특정 벡터(예: 44번) 뒤에 존재하는 [[022_kernel_role|커널]] 링크드 리스트에 **내가 짠 C 함수([[020_isr|ISR]])**를 등록해 주는 과정이다.
- **[[015_virtualization|가상화]] (Cloud)**: 가상머신([[713_kvm_over_ip|KVM]])은 이 IDT를 어떻게 훔쳐볼까? 인텔의 [[015_virtualization|가상화]] 하드웨어(VT-x)는 VM이 [[016_interrupt_mechanism|인터럽트]]를 받을 때 진짜 CPU의 IDT를 타지 않고, VM만을 위한 가짜 IDT([[529_vmcs|VMCS]] 내부에 세팅)를 타도록 하드웨어 레벨에서 완벽히 속인다(IDT Shadowing). 

- **📢 섹션 요약 비유**: 외부에서 던진 돌([[017_hardware_interrupt|하드웨어 인터럽트]]), 내 스스로 낸 상처(예외), 내가 의도적으로 누른 비상벨([[677_trap_based_system_call_implementation|트랩]]) 모두 종류는 다르지만 결국 응급실(IDT)이라는 하나의 문을 통해 수술실([[022_kernel_role|커널]])로 향하게 됩니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — IRQ 충돌(Conflict)로 인한 디바이스 인식 불가**: 옛날 리눅스 서버에 새 랜카드를 꽂았더니, 기존에 있던 사운드 카드가 먹통이 되고 랜카드도 핑이 빠짐.
   - **원인 분석**: 과거 시스템(PIC)은 [[016_interrupt_mechanism|인터럽트]] 선(IRQ 라인)이 15개밖에 없어서, 랜카드와 사운드 카드가 똑같은 11번 IRQ(벡터)를 공유하게 됨. IDT의 11번 엔트리 하나에 랜카드 ISR과 사운드 ISR이 동시에 물렸는데, 드라이버가 공유(IRQ Sharing) 처리를 제대로 못 해 엉뚱한 장치가 응답한 것이다.
   - **대응 (기술사적 가이드)**: 최신 시스템은 **APIC (Advanced Programmable [[016_interrupt_mechanism|Interrupt]] Controller)**와 **MSI-X ([[561_msi|Message Signaled Interrupts]])**를 사용한다. 디바이스가 물리적 선을 쓰지 않고 메모리에 벡터 번호를 직접 써서 수백 개의 독립된 [[019_interrupt_vector|인터럽트 벡터]]를 사용할 수 있다. 관리자는 BIOS에서 MSI-X를 활성화하여 IRQ 충돌을 원천 차단해야 한다.

2. **시나리오 — 클라우드/보안 환경에서의 IDT 후킹 ([[603_rootkit_syscall_hooking|Rootkit]] 탐지)**: 보안 관제팀이 서버 메모리를 덤프 떠서 분석해 보니, IDT의 0x80번(시스템 콜) 엔트리 주소가 [[022_kernel_role|커널]] 영역이 아닌 이상한 메모리 공간을 가리키고 있었다.
   - **원인 분석**: 전형적인 **IDT Hooking** 기법을 쓰는 [[603_rootkit_syscall_hooking|루트킷]]([[603_rootkit_syscall_hooking|Rootkit]]) 악성코드에 감염된 것이다. 해커가 [[022_kernel_role|커널]] 메모리를 조작해, IDT의 주소를 원래 [[022_kernel_role|커널]]의 `system_call` 함수가 아니라 자신이 만든 악성 함수로 바꿔치기했다.
   - **대응**: 최신 리눅스/윈도우 [[022_kernel_role|커널]]은 **KPP ([[022_kernel_role|Kernel]] Patch [[571_protection_vs_security|Protection]], PatchGuard)**나 Read-Only 메모리 속성을 통해 IDT가 쓰여진 메모리 [[286_page_frame|페이지]]를 강제로 잠가버린다. 이 기능이 활성화(`CONFIG_STRICT_KERNEL_RWX`)되어 있는지 [[396_validation|확인]]하고, 시스템의 무결성을 검증해야 한다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 인터럽트 벡터 및 핸들링 성능 최적화 플로우               │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [10Gbps 이상 고대역폭 네트워크 서버 (수백만 번의 인터럽트 발생)]             │
  │                │                                                  │
  │                ▼                                                  │
  │      하나의 특정 CPU 코어(예: Core 0)에만 모든 인터럽트가 몰리고 있는가?      │
  │      (top 명령어 실행 시 Core 0의 %hi(하드웨어 인터럽트) 수치만 100% 임)  │
  │          ├─ 예 ─────▶ [SMP Affinity (IRQ 밸런싱) 튜닝 필요]          │
  │          │            대책: `irqbalance` 데몬을 켜거나, /proc/irq/*/smp_affinity │
  │          │                  파일을 수정해 랜카드의 다중 큐(Multi-queue) 벡터를│
  │          │                  여러 코어(Core 1, 2, 3...)로 분산시킨다.   │
  │          └─ 아니오                                                │
  │                │                                                  │
  │                ▼                                                  │
  │      인터럽트 폭풍(Interrupt Storm)으로 인해 시스템 전체가 뻗을 위험이 있는가?│
  │          ├─ 예 ─────▶ [NAPI (New API) 및 인터럽트 병합(Coalescing) 적용]│
  │          │            대책: 랜카드가 패킷 하나당 인터럽트 1번(벡터 호출)을 쏘는 게 │
  │          │                  아니라, 100개 모아서 1번 쏘도록 하드웨어 튜닝.   │
  │          └─ 아니오 ──▶ 기본 커널 인터럽트 핸들링 유지                  │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** IDT를 거쳐 ISR로 점프하는 하드웨어 메커니즘 자체는 빠르지만, [[211_context_switch|문맥 교환]]([[033_context|Context]] Save) 비용 때문에 초당 10만 번 이상 발생하면 CPU가 죽어난다. 아키텍트는 [[017_hardware_interrupt|하드웨어 인터럽트]](Vector)가 여러 코어에 골고루 떨어지도록(RSS: Receive Side Scaling) 벡터를 찢어발기거나, 아예 [[016_interrupt_mechanism|인터럽트]] 발생 횟수 자체를 묶어버리는([[016_interrupt_mechanism|Interrupt]] Coalescing) 시스템 튜닝을 반드시 할 줄 알아야 한다.

### 도입 [[435_checklist_based_testing|체크리스트]]
- **Top Half / Bottom Half 설계**: 개발자가 디바이스 드라이버를 짤 때, IDT를 통해 즉각 점프해 온 함수(Top Half, [[020_isr|ISR]]) 내에서 무거운 루프를 돌고 있지 않은가? ISR에서는 상태 플래그만 세팅하고 즉시 리턴한 뒤, 워크큐(Workqueue)나 Tasklet 같은 Bottom Half로 일을 넘기도록 코드 리뷰를 철저히 했는가? (안 그러면 시스템 마우스가 멈춤)

- **📢 섹션 요약 비유**: 우체국 창구 직원(CPU)에게 손님(장치)이 올 때마다 인사를 90도로 하는 것([[016_interrupt_mechanism|인터럽트]] 오버헤드)은 힘듭니다. 손님 10명이 모였을 때 한 번만 인사하게 만들거나(NAPI), 옆 창구 직원들과 손님을 골고루 나누어 받는 것(IRQ 밸런싱)이 대형 우체국을 운영하는 기술입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [[448_polling_programmed_io|폴링]] ([[747_io_polling_overhead|Polling]] / if-else 검사) | [[019_interrupt_vector|인터럽트 벡터]] 테이블 (IVT/IDT) 구조 | 개선 효과 |
|:---|:---|:---|:---|
| **정량 ([[324_seek_time|탐색 시간]])** | 장치 수(N)에 비례하는 $O(N)$ [[015_지연_데이터_관점|지연]] | **즉각적 $O(1)$ 점프 (하드웨어 매핑)** | 이벤트 응답성 수만 배 향상 |
| **정량 (CPU 낭비)** | 아무 일 없을 때도 계속 장치 [[396_validation|확인]] | 이벤트 발생 시에만 CPU 개입 | CPU 활용률(Utilization) 극대화 |
| **정성 (확장성)** | 새 장치 추가 시 OS 코어 로직 수정 필요 | IDT 엔트리만 추가하고 드라이버 링킹 | 무한한 하드웨어 플러그앤플레이(PnP) 생태계 형성 |

### 미래 전망
- **MSI-X를 통한 100% [[015_virtualization|가상화]] 매핑**: 차세대 디바이스([[482_nvme|NVMe]], [[436_dpu|DPU]])는 기존 256개의 좁은 벡터 테이블을 넘어선다. MSI-X를 통해 장치가 무려 2,000개가 넘는 가상 벡터(메시지)를 쏘면, 하이퍼바이저가 이를 가로채지 않고 IOMMU를 통해 가상머신의 vCPU IDT에 직결로 꽂아버리는([[016_interrupt_mechanism|Interrupt]] [[657_vfio_virtual_function_io_passthrough|Passthrough]]) 완전한 제로 오버헤드 아키텍처가 표준이 되었다.
- **[[615_ebpf|eBPF]] 기반 동적 [[021_interrupt_handler|인터럽트 핸들러]]**: 기존에는 IDT 엔트리에 연결된 함수를 바꾸려면 [[022_kernel_role|커널]] 모듈을 다시 짜서 올려야 했지만, 최근 리눅스 [[022_kernel_role|커널]]에서는 하드웨어 예외나 [[677_trap_based_system_call_implementation|트랩]] 벡터가 발생했을 때 [[568_jit_access|JIT]] 컴파일된 [[615_ebpf|eBPF]] 프로그램이 이를 즉각 낚아채서 유저 공간으로 넘겨주거나 로깅하는 동적 라우팅이 발전하고 있다.

### 결론
[[019_interrupt_vector|인터럽트 벡터]] 테이블(IVT/IDT) 구조화는 "예측할 수 없는 외부 세계(하드웨어)의 [[130_signal|신호]]를, 철저하게 질서 잡힌 소프트웨어 세계(OS [[022_kernel_role|커널]])로 어떻게 우아하게 끌어들일 것인가?"에 대한 컴퓨터 구조학의 가장 위대한 해답이다. [[055_array|배열]]의 인덱스와 하드웨어 점프라는 가장 단순한 아이디어가 만남으로써, CPU는 무의미한 감시의 굴레([[747_io_polling_overhead|Polling]])에서 벗어나 연산에만 집중할 수 있게 되었다. 현대 [[001_operating_system_purpose|운영체제]]의 비동기 I/O, [[675_multitasking_terminology_preemptive|멀티태스킹]], [[381_virtual_memory|가상 메모리]]([[387_page_fault|Page Fault]])의 모든 기적이 바로 이 1KB짜리 작은 주소록 [[055_array|배열]]에서부터 시작된다.

- **📢 섹션 요약 비유**: 왕(CPU)이 성 밖에서 무슨 일이 일어나는지 매일 망루에서 쳐다보지([[448_polling_programmed_io|폴링]]) 않아도 됩니다. 성벽에 256개의 봉화대(벡터)를 세우고, 빨간 연기(44번)가 피어오르면 장군(마우스 핸들러)이, 파란 연기(14번)가 피어오르면 의사([[720_page_fault_isr|페이지 폴트]] 핸들러)가 즉각 튀어나가게 만든 가장 완벽한 자동 경보 시스템입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[003_time_sharing_system|시분할 시스템]] [[138_response_time|응답 시간]] 최적화 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[675_multitasking_terminology_preemptive|멀티태스킹]] ([[675_multitasking_terminology_preemptive|Multitasking]]) 용어 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[677_trap_based_system_call_implementation|트랩]] ([[677_trap_based_system_call_implementation|Trap]]) 기반 시스템 콜 구현 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[022_kernel_role|커널]] 모드 진입 메커니즘 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[멀티태스킹 (Multitasking) 용어]
    │
    ▼
[인터럽트 벡터 테이블 구조화 (Interrupt Vector Table Architecture)]
    │
    ├──▶ [트랩 (Trap) 기반 시스템 콜 구현]
    └──▶ [커널 모드 진입 메커니즘]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 수위 아저씨(CPU)가 반마다 돌아다니며 "무슨 일 있니?" 묻는 건 너무 힘들어요.
2. 그래서 경비실에 1번부터 100번까지 불이 들어오는 전광판([[019_interrupt_vector|인터럽트 벡터]] 테이블)을 달았어요!
3. 3반에서 누가 싸워서 비상벨을 누르면 3번 불이 반짝! 켜져요. 아저씨는 전광판 옆 매뉴얼을 보고 "3번 불? 양호 선생님 출동!" 하고 1초 만에 바로 행동할 수 있답니다.
