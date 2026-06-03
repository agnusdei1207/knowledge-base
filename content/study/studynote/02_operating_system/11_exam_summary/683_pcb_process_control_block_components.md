+++
weight = 683
title = "683. PCB 구성 요소 필수 암기 (PCB Process Control Block Components)"
date = "2026-05-09"
[extra]
categories = "studynote-operating-system"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PCB([[300_process|Process]] Control Block, [[090_pcb_tcb|프로세스 제어 블록]])는 [[001_operating_system_purpose|운영체제]]가 수많은 프로세스를 관리하기 위해, 각 프로세스의 '모든 개인 정보와 [[178_as_is_to_be_analysis|현재 상태]]'를 기록해 두는 **[[022_kernel_role|커널]] 메모리 상의 이력서(자료구조)**다. (리눅스에서는 `task_struct`라 부른다.)
> 2. **필수 구성요소**: 가장 중요한 핵심 정보는 CPU를 빼앗길 때 [[057_register|레지스터]] 값을 임시로 적어두는 **[[033_context|Context]](문맥) 정보**, 프로세스의 생사를 나타내는 **상태([[272_state_pattern|State]])**, 메모리 위치를 알려주는 **포인터([[353_page_table|Page Table]] Base)**다.
> 3. **가치**: 이 PCB가 존재하기 때문에 CPU는 1초에 수천 번씩 프로세스를 바꾸는 [[675_multitasking_terminology_preemptive|멀티태스킹]]([[211_context_switch|Context Switch]])을 하면서도, 이전에 하던 작업을 완벽하게 기억하고 이어갈 수 있다. OS 스케줄링의 알파이자 오메가다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **PCB ([[300_process|Process]] Control Block)**: [[001_operating_system_purpose|운영체제]]가 프로세스의 생성부터 소멸까지의 전 주기를 관리하기 위해 유지하는 C 언어 구조체(Struct).
  - 프로세스가 1개 생성될 때마다 PCB도 반드시 1개씩 [[022_kernel_role|커널]] 영역에 생성된다.

- **필요성 ([[211_context_switch|문맥 교환]]의 필수품)**: 
  - CPU는 건망증이 심하다. A 프로세스를 0.1초 실행하다가 B 프로세스로 넘어가면, A가 방금까지 몇 번째 코드를 읽고 있었는지, 덧셈 결과가 뭐였는지 전부 까먹는다.
  - 나중에 다시 A의 차례가 왔을 때 원래 하던 일부터 이어서 하려면, 쫓겨나기 직전의 CPU 머릿속([[057_register|레지스터]]) 상태를 어딘가에 적어두어야 한다.
  - **해결책**: [[022_kernel_role|커널]] 메모리에 프로세스마다 고유한 금고(PCB)를 하나씩 만들어서, CPU를 뺏길 때마다 [[178_as_is_to_be_analysis|현재 상태]]를 몽땅 PCB에 때려 넣고(Save), 다시 차례가 오면 PCB에서 꺼내서 CPU에 복원(Restore)하는 메커니즘이 필요했다.

  - **CPU**: 여러 권의 소설책을 동시에 읽는 독자.
  - **프로세스**: 각각의 소설책.
  - **PCB**: 소설책 사이사이에 꽂아두는 '책갈피'이자 '독서 노트'. 독자가 A 책을 읽다가 덮을 때, 몇 [[286_page_frame|페이지]]까지 읽었는지([[164_pc|PC]]), 주인공 이름이 뭐였는지([[057_register|레지스터]]) 책갈피에 다 적어둔다. 그래야 B 책을 읽고 돌아왔을 때 헷갈리지 않고 A 책의 다음 줄부터 바로 읽을 수 있다.

- **발전 과정**:
  1. **[[459_quic_fec_forward_error_correction|초기]] OS**: PCB 구조가 단순. (상태, [[164_pc|PC]] 정도만 저장)
  2. **[[381_virtual_memory|가상 메모리]] 시대**: 메모리 [[571_protection_vs_security|보호]]를 위해 [[328_mmu|MMU]] 포인터(CR3)가 PCB에 추가됨.
  3. **멀티스레드 시대 (TCB의 분리)**: 프로세스 하나에 [[092_thread_lwp|스레드]]가 여러 개 생기면서, PCB 안의 [[057_register|레지스터]] 정보만 따로 떼어내어 **TCB ([[092_thread_lwp|Thread]] Control Block)**로 쪼개어 관리하게 됨 (경량화).

- **📢 섹션 요약 비유**: 병원의 '환자 차트'와 같습니다. 의사(CPU)가 수백 명의 환자(프로세스)를 번갈아 진료할 수 있는 것은, 환자 차트(PCB)에 지난번 처방 기록과 현재 혈압(상태)이 빠짐없이 꼼꼼하게 적혀 있기 때문입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### PCB의 6대 핵심 구성 요소 (필수 암기)

시험과 실무에서 가장 자주 언급되는 핵심 요소들이다.

| 구성 요소 (한글) | 영문 명칭 (의미) | 상세 역할 및 저장 내용 |
|:---|:---|:---|
| **1. 프로세스 [[289_identification_flags_fragmentation_offset|식별자]]** | **PID ([[300_process|Process]] ID)** | OS가 프로세스를 구분하는 고유 번호 (주민등록번호). 부모 프로세스의 번호(PPID)도 함께 저장. |
| **2. [[086_process_state|프로세스 상태]]** | **[[086_process_state|Process State]]** | 현재 프로세스가 어떤 상태인지 표기. ([[087_process_state_transition|New]], Ready, Running, Waiting/Block, Terminated) |
| **3. [[164_pc|프로그램 카운터]]** | **[[164_pc|PC]] (Program [[059_counter|Counter]])** | 다음번에 CPU가 이 프로세스를 다시 잡았을 때, **"몇 번째 줄의 코드부터 이어서 실행해야 하는가?"**에 대한 주소. |
| **4. CPU [[057_register|레지스터]]** | **CPU Registers** | CPU가 연산하다 만 중간 결과값([[161_accumulator|누산기]], [[166_sp|스택 포인터]] 등). [[211_context_switch|Context Switch]] 시 여기에 백업됨. |
| **5. 메모리 관리 정보** | **Memory Mgmt Info** | 이 프로세스가 쓰는 [[381_virtual_memory|가상 메모리]] 지도의 시작 위치 (**[[353_page_table|페이지 테이블]] 포인터, CR3 값**), Base/Limit [[057_register|레지스터]] 등. |
| **6. 스케줄링 정보** | **Scheduling Info** | 프로세스의 우선순위(Priority), CPU 점유 시간, 기다린 시간 등 (OS가 다음 차례를 정할 때 씀). |
| *7. 회계 및 I/O 정보* | *Accounting / I/O Status* | CPU 사용 요금 청구용 [[001_dikw_pyramid|데이터]], 현재 프로세스가 열어놓은 [[501_file_definition_logical_record|파일]] 목록([[501_file_definition_logical_record|File]] Descriptor Table). |

---

### PCB와 [[211_context_switch|Context Switch]] ([[211_context_switch|문맥 교환]]) 동작 원리

프로세스 $P_0$에서 $P_1$으로 CPU 제어권이 넘어갈 때 PCB가 어떻게 작동하는지 본다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 문맥 교환 시 PCB의 Save & Restore 파이프라인           │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │     [ CPU ]               [ PCB 0 (P0용) ]      [ PCB 1 (P1용) ]   │
  │                                                                   │
  │  P0 실행 중 (Running)                                              │
  │        │                                                          │
  │  ⚡ 인터럽트/시스템콜 발생                                             │
  │        │                                                          │
  │  [커널 개입] ──────────────▶ P0의 현재 레지스터                       │
  │  P0 중지 (Ready)              값을 PCB 0에 덮어씀.                     │
  │                             (Save state)                          │
  │                                                                   │
  │  [스케줄러 동작] - "다음은 P1 차례다!"                                  │
  │                                                                   │
  │  [커널 개입] ◀───────────────────────────────── PCB 1에서 과거에        │
  │  P1 시작 (Running)                             저장해둔 레지스터 값을      │
  │                                               CPU로 복원 (Restore)  │
  │        │                                                          │
  │  P1 실행 중 (Running)                                              │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 Save와 Restore 과정이 바로 **[[211_context_switch|Context Switch]] ([[211_context_switch|문맥 교환]])**다. PCB는 메모리(RAM)에 있으므로, CPU [[057_register|레지스터]]의 값을 메모리(PCB)로 옮겨 적는 데는 필연적으로 시간이 걸린다 (오버헤드). 아무 일도 안 하고 오직 백업과 복원만 하는 이 '무의미한 찰나'를 줄이기 위해, [[001_operating_system_purpose|운영체제]]는 PCB를 최대한 가볍게 만들려 노력한다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### PCB ([[300_process|Process]] Control Block) vs TCB ([[092_thread_lwp|Thread]] Control Block)

최신 OS는 프로세스 안에 여러 [[092_thread_lwp|스레드]]를 띄운다. 이때 관리의 단위가 분리된다.

| 비교 항목 | PCB ([[090_pcb_tcb|프로세스 제어 블록]]) | TCB ([[092_thread_lwp|스레드]] 제어 블록) |
|:---|:---|:---|
| **소유권** | 프로세스당 1개 | [[092_thread_lwp|스레드]]당 1개 (프로세스 하나에 여러 개) |
| **핵심 저장 정보**| **메모리([[353_page_table|페이지 테이블]])**, 열린 [[501_file_definition_logical_record|파일]](FD), PID | **[[164_pc|PC]] ([[164_pc|프로그램 카운터]])**, [[057_register|레지스터]], [[166_sp|스택 포인터]] |
| **스위칭 오버헤드**| **매우 큼** (캐시 및 [[357_tlb|TLB]] [[459_quic_fec_forward_error_correction|초기]]화 동반) | **작음** (메모리는 그대로 두고 [[057_register|레지스터]]만 교체) |
| **역할** | 자원(Resource) 소유권 관리의 주체 | 실제 CPU 실행(Execution)의 주체 |

### 과목 융합 관점

- **자료구조 ([[001_dikw_pyramid|Data]] Structure)**: [[001_operating_system_purpose|운영체제]]는 수백 개의 PCB를 어떻게 관리할까? 단순히 [[055_array|배열]]로 두지 않는다. 메모리가 부족해 자는 애들은 `Wait Queue`라는 [[056_linked_list|연결 리스트]]([[056_linked_list|Linked List]])로 묶어두고, 실행을 기다리는 애들은 `Ready Queue`(최근엔 [[204_red_black_tree_cfs|Red-Black Tree]])에 PCB 포인터를 달아두어, O(1)이나 O(log N) 속도로 스케줄링할 프로세스를 찾아낸다.
- **보안 ([[283_security_tactics|Security]])**: PCB는 철저하게 **[[022_kernel_role|커널]] 스페이스(Ring 0)**의 안전한 구역에 저장된다. 만약 PCB가 유저 스페이스에 있었다면, 일반 프로그램이 포인터 연산으로 자기 PCB의 '우선순위(Priority)' 변수를 1등으로 조작해 CPU를 영원히 독점해 버리는 해킹이 1초 만에 일어났을 것이다.

- **📢 섹션 요약 비유**: 이사를 갈 때, 집 전체의 명의와 가구 목록(PCB)을 바꾸는 것은 매우 비싸고 힘듭니다. 하지만 한 집 안에서 방만 바꾸는 것(TCB 교체)은 옷가지([[057_register|레지스터]])만 챙겨서 가면 되니 훨씬 빠르고 가볍습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — [[109_zombie_process|좀비 프로세스]]([[109_zombie_process|Zombie Process]])와 PCB 자원 고갈**: 리눅스 서버를 1년 켜놨더니 `fork()`를 많이 하는 데몬 때문에 더 이상 새로운 프로그램이 안 켜짐. `ps -ef | grep Z`를 쳐보니 [[109_zombie_process|좀비 프로세스]]가 10만 개 떠 있음.
   - **원인 분석**: [[109_zombie_process|좀비 프로세스]]는 메모리와 CPU는 전혀 쓰지 않고 죽어있는 껍데기다. 하지만 부모 프로세스가 `wait()` 시스템 콜을 통해 자식의 종료 상태를 확인하기 전까지, [[022_kernel_role|커널]]은 이 프로세스의 이력서인 **PCB (task_struct)를 [[022_kernel_role|커널]] 메모리 상에서 삭제하지 않고 남겨둔다**. PCB는 1개당 약 수 KB를 먹으므로, 좀비가 10만 개 쌓이면 [[022_kernel_role|커널]] 메모리가 고갈되고 PID 슬롯이 꽉 차서 새 앱을 켤 수 없게 된다.
   - **대응 (기술사적 가이드)**: 개발자에게 부모 코드를 고쳐 비동기 `SIGCHLD` 시그널 핸들러를 달아 자식의 PCB를 즉각 수거(reap)하도록 지시하거나, 임시방편으로 고장 난 부모 프로세스를 죽여 고아(Orphan)로 만든 뒤 init(systemd) 데몬이 PCB를 입양해 자동 수거하게 만들어야 한다.

2. **시나리오 — [[211_context_switch|Context Switch]] 폭발로 인한 [[282_performance_tactics|성능]] 저하**: 멀티스레드 웹 서버가 초당 1만 건을 처리하는데, CPU 사용률을 보니 `%us`(유저)는 30%인데 `%sy`([[022_kernel_role|커널]])가 70%를 차지함.
   - **원인 분석**: [[092_thread_lwp|스레드]]를 너무 많이 만들어서, [[022_kernel_role|커널]] [[079_kube_scheduler_pod_placement|스케줄러]]가 1초에도 수십만 번씩 **TCB/PCB의 [[057_register|레지스터]]를 백업하고 복원하는([[033_context|Context]] Save/Restore)** 작업만 하느라 정작 웹 서빙을 못 하고 있는 것이다 ([[257_thrashing|스래싱]] 현상).
   - **아키텍처 적용**: 비동기 I/O(epoll, [[464_io_uring|io_uring]])를 도입하거나, Node.js나 Go 언어처럼 [[022_kernel_role|커널]]의 PCB 교체를 피하고 유저 스페이스에서 가볍게 [[141_coroutine|코루틴]]([[140_goroutine|Goroutine]])을 스위칭하는 아키텍처로 개편하여 [[022_kernel_role|커널]] 개입을 최소화해야 한다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 서버 아키텍처 스레드/프로세스 수량 최적화 플로우           │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [고성능 분산 처리 시스템의 Worker 풀(Pool) 크기 결정]                   │
  │                │                                                  │
  │                ▼                                                  │
  │      처리하려는 작업이 파일 읽기/DB 통신(I/O Bound) 위주의 작업인가?         │
  │          ├─ 예 ─────▶ [스레드/프로세스 수를 CPU 코어의 수 배로 늘림]      │
  │          │            (I/O 대기 시간에 다른 TCB/PCB로 문맥 교환하여 효율 UP)│
  │          └─ 아니오 (순수 수학 계산, 암호화, 압축 등 CPU Bound 작업이다)     │
  │                │                                                  │
  │                ▼                                                  │
  │      [스레드/프로세스 수를 딱 CPU 코어 개수만큼만 제한 (예: 16코어 = 16개)] │
  │       - 이유: 어차피 100% CPU를 쓰는 연산인데 PCB를 100개로 늘려봐야,       │
  │               커널이 레지스터 백업(Save/Restore)하는 오버헤드만 폭증하여    │
  │               시스템 전체 처리 속도가 기하급수적으로 느려진다.              │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 초보 개발자는 "속도가 느리니 [[092_thread_lwp|스레드]](프로세스)를 더 늘리자!"고 착각한다. 프로세스가 늘어날수록 OS [[022_kernel_role|커널]] 메모리에는 수백 개의 무거운 PCB가 생겨나고, [[079_kube_scheduler_pod_placement|스케줄러]]는 누구에게 CPU를 줄지 고르는 계산에 시간을 허비하게 된다. 아키텍트는 하드웨어(코어 수)와 태스크의 성격을 일치시키는 '적정 PCB/TCB 개수 유지'의 철학을 가져야 한다.

### 도입 [[435_checklist_based_testing|체크리스트]]
- **KASLR 및 [[022_kernel_role|커널]] 보안**: 리눅스에서 `task_struct`(PCB) 안에는 사용자의 UID나 권한 증명(Credentials) 포인터가 들어있다. [[376_kernel_vulnerability|커널 취약점]]([[409_cve_lifecycle|CVE]])을 이용해 해커가 내 PCB의 `uid` 값을 0(root)으로 조작하는 [[356_privilege_escalation|권한 상승]]([[356_privilege_escalation|Privilege Escalation]]) 공격을 막기 위해, [[022_kernel_role|커널]] 포인터 [[571_protection_vs_security|보호]] 및 랜덤화 기법이 시스템에 적용되어 있는가?
- **FD ([[501_file_definition_logical_record|File]] Descriptor) 제한**: PCB 안에는 해당 프로세스가 열어놓은 [[501_file_definition_logical_record|파일]] 목록 [[055_array|배열]](FD Table)이 있다. [[001_operating_system_purpose|운영체제]]는 PCB 크기를 아끼기 위해 이 [[055_array|배열]]의 크기를 기본 1024개로 제한(`ulimit -n`)한다. 소켓을 수만 개 여는 Nginx 웹 서버를 구축할 때는 반드시 이 PCB 내부의 FD 한도를 65535 이상으로 튜닝했는지 점검해야 한다.

- **📢 섹션 요약 비유**: PCB는 [[001_operating_system_purpose|운영체제]]라는 관공서에 보관된 '시민의 호적 등본'입니다. 시민(프로세스)이 너무 많아지면 등본을 보관할 서고([[022_kernel_role|커널]] 메모리)가 터져버리고, 공무원([[079_kube_scheduler_pod_placement|스케줄러]])이 등본을 찾는 데만 하루 종일 걸려 행정 업무(컴퓨터 속도)가 완전히 마비됩니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | PCB가 없는 시스템 (불가능 가정) | PCB/TCB 기반 상태 관리 | 개선 효과 |
|:---|:---|:---|:---|
| **정성 ([[675_multitasking_terminology_preemptive|멀티태스킹]])**| 하나의 작업이 끝날 때까지 CPU 독점 | 시분할로 수십 개 프로그램 동시 실행 | 대화형(Interactive) [[001_operating_system_purpose|운영체제]]의 근간 완성 |
| **정성 (자원 격리)** | 어떤 프로그램이 어떤 메모리를 쓰는지 모름 | 프로세스별 고유한 자원(FD, Memory) 추적 | 시스템 안정성 및 프로세스 간 침범 방지 |
| **정량 ([[658_ir_recovery|복구]] 비용)** | [[016_interrupt_mechanism|인터럽트]] 시 작업 [[001_dikw_pyramid|데이터]] 증발 | [[057_register|레지스터]] 단위의 완벽한 1:1 복원 | 투명한 중단 및 재개 (Suspend & Resume) |

### 미래 전망
- **eBPF를 통한 [[150_task|Task]] 구조체 해킹(모니터링)**: 기존에는 [[022_kernel_role|커널]] 메모리 깊숙한 곳에 있는 PCB(`task_struct`)를 유저 공간에서 보려면 무거운 `/proc` [[501_file_definition_logical_record|파일]] 시스템을 까봐야 했다. 현재 [[531_cloud_native_architecture|클라우드 네이티브]] 관제(Datadog, [[825_cilium_ebpf_kubernetes_networking_security|Cilium]])는 [[615_ebpf|eBPF]] 코드를 [[022_kernel_role|커널]]에 찔러넣어, 빛의 속도로 실시간 PCB 정보(네트워크 통계, CPU [[015_지연_데이터_관점|지연]] 등)를 퍼다 나르는 혁신을 이룩했다.
- **하드웨어 [[033_context|컨텍스트]] [[238_switch_operation_principles|스위치]] 가속**: 인텔의 AMX나 최신 ARM 아키텍처에서는, TCB/PCB에 저장해야 할 [[057_register|레지스터]]가 너무 많아지자(수백 [[074_byte|바이트]]), 아예 하드웨어 칩셋 단위에서 CPU의 상태를 메모리로 한방에 던지고 엎어치는 전용 가속 명령어를 도입하여 [[211_context_switch|문맥 교환]] 오버헤드를 제로에 가깝게 만들려 하고 있다.

### 결론
PCB([[090_pcb_tcb|프로세스 제어 블록]])는 [[001_operating_system_purpose|운영체제]]가 '프로세스'라는 무형의 영혼(소프트웨어)을 '메모리'라는 물리적 실체로 붙잡아두는 닻(Anchor)이다. [[164_pc|프로그램 카운터]]([[164_pc|PC]])로 미래의 길을 기억하고, [[057_register|레지스터]]로 현재의 상태를 백업하며, [[353_page_table|페이지 테이블]]로 자신만의 세계를 짓는 이 정교한 C 언어 구조체가 없었다면 현대의 모든 시분할 [[675_multitasking_terminology_preemptive|멀티태스킹]]은 불가능했다. PCB를 이해하는 것은 [[001_operating_system_purpose|운영체제]]가 한순간도 쉬지 않고 어떻게 이 거대한 시스템의 혼돈을 우아하게 통제하고 있는지 엿보는 가장 직관적인 창문이다.

- **📢 섹션 요약 비유**: 수백 편의 드라마를 1초마다 번갈아 촬영하는 미친 스케줄의 배우(CPU)가 대사를 절대 잊어버리지 않는 이유는, 코디(OS)가 매번 촬영이 바뀔 때마다 완벽하게 정리된 대본과 감정선 요약본(PCB)을 찰나의 순간에 쥐여주기 때문입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[117_ipc|IPC]] 기법 [[282_performance_tactics|성능]] 오버헤드 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 프로세스 주소 공간 분리 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[211_context_switch|문맥 교환]] [[357_tlb|TLB]] 플러시 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[685_short_term_scheduler_dispatcher|단기 스케줄러 디스패치]] | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[프로세스 주소 공간 분리]
    │
    ▼
[PCB 구성 요소 필수 암기 (PCB Process Control Block Components)]
    │
    ├──▶ [문맥 교환 TLB 플러시]
    └──▶ [단기 스케줄러 디스패치]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[001_operating_system_purpose|운영체제]] 선생님이 100명의 학생(프로그램)을 가르치려면 누가 어디까지 공부했는지 다 외울 수가 없어요.
2. 그래서 선생님은 학생 1명당 1개씩 '비밀 수첩(PCB)'을 만들어 두었어요!
3. 학생이 공부를 멈추고 화장실에 갈 때, 선생님은 수첩에 "철수는 35페이지 덧셈을 풀다 말았고, 지우개는 2개 빌려감"이라고 꼼꼼히 적어(저장) 둡니다. 나중에 철수가 돌아오면 수첩을 보고 곧바로 35페이지부터 가르쳐 줄 수 있답니다!
