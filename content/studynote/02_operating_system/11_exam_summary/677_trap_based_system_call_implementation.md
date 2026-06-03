---
title: 677. 트랩 (Trap) 기반 시스템 콜 구현
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 시스템 콜([[013_system_call|System Call]])은 유저 스페이스(Ring 3)에서 돌아가는 애플리케이션이, 자신이 직접 할 수 없는 특권 작업([[501_file_definition_logical_record|파일]] [[289_cqrs_db|쓰기]], 네트워크 통신, 메모리 할당)을 [[022_kernel_role|커널]](Ring 0)에게 부탁하기 위해 사용하는 유일한 합법적 통로다.
> 2. **메커니즘 (Trap)**: 애플리케이션은 일반적인 [[294_function_calling_tool_use|함수 호출]](`call`)로는 [[022_kernel_role|커널]] 메모리에 들어갈 수 없다. 대신, CPU 내부에 고의적인 **소프트웨어 [[016_interrupt_mechanism|인터럽트]](트랩, 예: `int 0x80`)**를 발생시켜, 하드웨어가 강제로 권한을 높이고 [[022_kernel_role|커널]]의 시스템 콜 핸들러로 점프하게 만드는 해킹에 가까운 우회로를 사용한다.
> 3. **진화**: 과거 트랩(`int 0x80`) 방식은 [[016_interrupt_mechanism|인터럽트]] 오버헤드가 커서 느렸다. 현대 CPU는 시스템 콜만을 위한 빠르고 날렵한 전용 하드웨어 [[158_instruction|명령어]]인 **`sysenter` / `syscall` (Fast [[013_system_call|System Call]])**을 도입하여 트랩 기반의 병목을 해결했다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **트랩 (Trap)**: 프로그램이 의도적으로 특정 어셈블리 [[158_instruction|명령어]](`int`, `syscall`)를 실행하여 CPU에 소프트웨어 [[016_interrupt_mechanism|인터럽트]]를 유발하는 행위.
  - **시스템 콜 ([[013_system_call|System Call]])**: 이 트랩 메커니즘을 이용해, [[001_operating_system_purpose|운영체제]] [[022_kernel_role|커널]]의 함수를 호출하여 [[090_service_kubernetes_network_load_balancing|서비스]]를 요청하는 약속된 규약.

- **필요성 (권한 분리와 안전한 진입로)**: 
  - CPU는 치명적인 하드웨어 제어 권한을 [[022_kernel_role|커널]](Ring 0)에게만 주고, 사용자 앱(Ring 3)에게는 주지 않는다. 
  - 만약 앱이 [[022_kernel_role|커널]]의 `sys_write()` 함수를 주소만 안다고 해서 직접 호출(`call sys_write`)해 버리면 어떻게 될까? CPU는 즉각 권한 위반([[364_segmentation|Segmentation]] Fault)으로 앱을 죽여버린다.
  - 그렇다면 앱은 영원히 [[501_file_definition_logical_record|파일]]을 디스크에 쓸 수 없는가? 
  - **해결책**: "사용자가 직접 [[022_kernel_role|커널]]로 넘어오는 문은 닫아두되, 사용자가 '벨(Trap)'을 누르면, [[022_kernel_role|커널]]이 문을 열고 나와서 사용자의 요청서를 받아간 뒤 대신 일해주고 결과만 던져주자!"

  - **직접 호출 (실패)**: 은행 손님(앱)이 직접 금고실([[022_kernel_role|커널]]) 문을 열고 들어가서 돈([[001_dikw_pyramid|데이터]])을 꺼내려고 한다. 경비원(CPU)이 즉시 총을 쏜다.
  - **트랩(Trap) 방식**: 손님은 금고실에 못 들어간다. 대신 창구에 가서 '출금 요청서'를 쓰고 창구의 '호출벨(Trap)'을 띵동! 누른다. 은행원(시스템 콜 핸들러)이 벨소리를 듣고 나와서 요청서를 받아 금고실에 들어가 돈을 가져다준다.

- **발전 과정**:
  1. **단일 권한 체계 ([[599_dos_ddos_attack|DOS]] 시절)**: 트랩 없음. 앱이 하드웨어를 직접 제어. 앱 하나가 고장 나면 컴퓨터 전체가 멈춤.
  2. **트랩 기반 시스템 콜 (전통적 Unix/Linux)**: `int 0x80` [[158_instruction|명령어]]를 통한 [[016_interrupt_mechanism|인터럽트]] 방식. 권한 분리는 이뤘으나 스위칭([[033_context|Context]] Save) 오버헤드가 큼.
  3. **Fast [[013_system_call|System Call]] (현재)**: 인텔과 AMD가 `syscall` / `sysenter`라는 전용 하드웨어 [[158_instruction|명령어]]를 만들어, 불필요한 [[016_interrupt_mechanism|인터럽트]] 검사를 건너뛰고 빛의 속도로 [[022_kernel_role|커널]]로 점프하게 만듦.

- **📢 섹션 요약 비유**: 철통같이 닫힌 성문([[022_kernel_role|커널]] 방어막)을 뚫고 지나가는 유일한 방법은 성벽을 부수는 게 아니라, 성문 옆에 마련된 '봉화(Trap)'를 피워올려 성 안의 파수꾼이 스스로 문을 열게 만드는 것입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 트랩(Trap) 발생 및 시스템 콜 처리 파이프라인

과거 x86 리눅스의 전통적인 `int 0x80` 기반 시스템 콜 호출 과정을 단계별로 분해해 본다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 트랩(Trap) 기반 시스템 콜 (int 0x80) 동작 원리          │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  [User Space (Ring 3)]                                            │
  │   1. 개발자가 C언어로 `write(fd, buf, size);` 함수 호출                  │
  │   2. C 라이브러리(glibc)가 이를 어셈블리로 변환:                            │
  │      - mov eax, 4    // EAX 레지스터에 시스템 콜 번호 (4 = sys_write) 넣음│
  │      - mov ebx, fd   // 첫 번째 인자 세팅                                │
  │      - mov ecx, buf  // 두 번째 인자 세팅                                │
  │   3. `int 0x80` 명령어 실행! (Trap 발생) ───┐                        │
  │                                           │                       │
  │  =========================================│=======================│
  │  [Hardware (CPU의 권한 상승)]              ▼                       │
  │   4. CPU가 IDT(인터럽트 벡터 테이블)의 0x80(128번) 엔트리를 찾음.          │
  │   5. CPU의 권한을 Ring 3 -> Ring 0 로 하드웨어적으로 격상(Escalation). │
  │   6. 현재 User 스택 포인터를 멈추고 Kernel 스택으로 전환.                  │
  │                                           │                       │
  │  =========================================│=======================│
  │  [Kernel Space (Ring 0)]                  ▼                       │
  │   7. 커널의 `system_call()` 핸들러 진입 (C언어 진입점).                  │
  │   8. EAX 레지스터 값(4)을 꺼내서 [시스템 콜 테이블(sys_call_table)] 조회. │
  │      - sys_call_table[4] = sys_write 함수 주소                      │
  │   9. `sys_write(fd, buf, size)` 실제 실행!                          │
  │  10. 실행이 끝나면 `iret` (Interrupt Return) 명령어로 결과(EAX) 반환 및  │
  │      권한을 다시 Ring 3로 강등시킴.                                    │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 과정의 핵심은 **[[057_register|레지스터]]([[175_register_addressing|Register]])**다. 유저 공간과 [[022_kernel_role|커널]] 공간은 서로 메모리를 직접 주고받을 수 없기 때문에, 철저하게 CPU 내부의 '[[057_register|레지스터]](EAX, EBX 등)'라는 중립 지대 사물함을 통해 "무슨 함수를 부를지(시스템 콜 번호)"와 "어떤 [[001_dikw_pyramid|데이터]]를 쓸지(인자)"를 전달한다. `int 0x80`이라는 소프트웨어 [[016_interrupt_mechanism|인터럽트]]는 CPU에게 "지금부터 내가 사물함에 넣어둔 요청서를 읽어라!"라고 찌르는 강제 [[507_acid_properties|트리거]] 역할을 한다.

---

### Fast [[013_system_call|System Call]] (`syscall` / `sysenter`) 의 등장

트랩(`int 0x80`) 방식은 심각한 병목이 있었다. [[016_interrupt_mechanism|인터럽트]]가 걸릴 때마다 하드웨어는 현재 CPU의 모든 권한을 검사하고, 수십 개의 [[057_register|레지스터]]를 [[555_backup_and_restore_strategy|백업]]하고, IDT를 뒤지는 무거운 짓을 반복해야 했다.

- **혁신**: Intel과 AMD는 아예 하드웨어 칩셋 안에 시스템 콜 전용 고속도로를 뚫었다.
- **원리**: OS 부팅 시 [[022_kernel_role|커널]]이 CPU 내부의 특수 [[057_register|레지스터]](MSR: Model Specific [[175_register_addressing|Register]])에 시스템 콜 핸들러의 주소를 아예 박아둔다.
- **동작**: 앱이 `syscall`이라는 단일 [[158_instruction|명령어]]를 치면, CPU는 IDT 검사나 불필요한 [[555_backup_and_restore_strategy|백업]] 없이 즉각 MSR에 적힌 주소로 다이렉트 점프([[176_direct_addressing|Direct]] Jump)를 뛰어버린다.
- **결과**: 권한 전환([[211_context_switch|Context Switch]]) 시간이 기존 대비 수십 배 이상 빨라져, `read()`, `write()`를 초당 수백만 번 부르는 I/O 집약적 서버의 [[282_performance_tactics|성능]]이 수직 상승했다.

- **📢 섹션 요약 비유**: `int 0x80`이 매번 구청 안내데스크(IDT)에서 신분증을 검사받고 부서 번호를 물어봐서 찾아가는 방식이라면, `syscall`은 구청장실로 직행하는 전용 하이패스 게이트(MSR)를 뚫어놓은 것입니다.

---

## Ⅲ. 비교 및 연결

### [[022_kernel_role|커널]] 진입 방식(Entry) 비교

| [[022_kernel_role|커널]] 진입 메커니즘 | 발동 원인 | 주체 (누가 찌르나) | 사용 목적 |
|:---|:---|:---|:---|
| **[[013_system_call|System Call]] (Trap)** | 의도적 ([[158_instruction|명령어]]) | **유저 애플리케이션** | [[501_file_definition_logical_record|파일]] 열기, 메모리 할당 등 [[022_kernel_role|커널]] [[090_service_kubernetes_network_load_balancing|서비스]] 요청 |
| **Exception (Fault)** | 비의도적 (오류) | **CPU 하드웨어** | 0으로 나누기, [[720_page_fault_isr|페이지 폴트]] 발생 시 [[658_ir_recovery|복구]]/처벌 |
| **[[017_hardware_interrupt|Hardware Interrupt]]** | 외부 이벤트 | **외부 기기 ([[587_nic_offloading|NIC]], 디스크 등)** | 패킷 도착, 키보드 눌림 등 [[017_hardware_interrupt|비동기적]] 사건 알림 |

세 가지 모두 결국 [[022_kernel_role|커널]] 모드(Ring 0)로 진입하여 특정 핸들러를 실행한다는 점은 같으나, 트랩(시스템 콜)만이 유일하게 "애플리케이션이 원해서 스스로" 들어가는 문이다.

### 과목 융합 관점

- **컴퓨터구조 ([[089_contract_account_smart_contract|CA]])**: `syscall` [[158_instruction|명령어]]가 그토록 빠른 이유는, 점프 시 저장해야 할 정보(PC와 [[186_character_stuffing_dle_stx_etx|플래그]])를 느린 메모리 스택에 PUSH하지 않고, CPU 내부의 [[148_5g_embb_urllc_mmtc|초고속]] RCX, R11 [[057_register|레지스터]]에 덮어써 버리는 극단적인 하드웨어 최적화(Hardware Fast Path)를 적용했기 때문이다.
- **보안 ([[283_security_tactics|Security]])**: [[603_rootkit_syscall_hooking|루트킷]]([[603_rootkit_syscall_hooking|Rootkit]])이나 상용 안티바이러스는 이 트랩 과정을 하이재킹한다. MSR [[057_register|레지스터]]에 적힌 시스템 콜 핸들러 주소를 자신들의 악성 코드 주소로 덮어쓰거나, `sys_call_table`의 인덱스를 조작하여, 유저 앱이 시스템 콜을 부를 때마다 무조건 해커의 코드를 거쳐 가게 만드는 시스템 콜 후킹(Hooking)을 수행한다.

- **📢 섹션 요약 비유**: 성문([[022_kernel_role|커널]])을 여는 방법은 세 가지입니다. 백성이 정식으로 문서를 내고 문을 두드리는 것(시스템 콜), 백성이 성벽에서 떨어져서 구급차가 출동하는 것(예외), 그리고 외부 적군이나 전령이 쳐들어와 비상벨이 울리는 것([[017_hardware_interrupt|하드웨어 인터럽트]])입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — 고성능 웹 서버(Nginx/Node.js)의 과도한 시스템 콜 오버헤드 병목**: 10G 네트워크 환경에서 Nginx가 [[501_file_definition_logical_record|파일]]을 읽어 클라이언트에게 보낼 때, CPU 사용률의 60%가 `sys_read`와 `sys_write` 시스템 콜의 전환 비용(System CPU Time)으로 낭비되어 [[140_bandwidth|대역폭]]을 다 쓰지 못하는 현상.
   - **원인 분석**: [[501_file_definition_logical_record|파일]]을 1바이트씩 쪼개 읽거나, `read()` 후 `write()`를 반복하면 User Mode와 [[022_kernel_role|Kernel]] Mode를 하루에 수십억 번 와리가리([[211_context_switch|Context Switch]]) 해야 한다. `syscall` [[158_instruction|명령어]]가 아무리 빨라도 그 횟수가 수십억 번이면 치명적이다.
   - **대응 (기술사적 가이드)**: 
     - **[[566_mmap_zero_copy_sendfile|Zero-Copy]] 기술 (sendfile)**: `read`와 `write`를 따로 부르지 말고, `sendfile()`이라는 단일 시스템 콜을 사용한다. [[022_kernel_role|커널]] 안에서 [[501_file_definition_logical_record|파일]] [[001_dikw_pyramid|데이터]]를 디스크 캐시 $\rightarrow$ 랜카드 버퍼로 다이렉트로 복사하므로, [[022_kernel_role|커널]] 밖(User Space)으로 나왔다가 들어가는 트랩 횟수가 절반으로 줄어 [[282_performance_tactics|성능]]이 2배 뛴다.
     - **[[464_io_uring|io_uring]] 도입**: 최신 리눅스는 시스템 콜 자체를 안 부르고 비동기로 처리하는 `io_uring` 큐 구조를 도입하여 트랩 오버헤드 자체를 제로(0)에 가깝게 소멸시켰다.

2. **시나리오 — [[063_docker_architecture|Docker]] [[561_container_based_deployment|컨테이너]]의 시스템 콜 차단 보안 ([[080_seccomp|Seccomp]])**: [[888_multi_tenant_cloud_resource_isolation_noisy_neighbor|멀티 테넌트]] 클라우드 환경에서 악성 [[561_container_based_deployment|컨테이너]]가 시스템의 시간을 함부로 바꾸거나(`sys_settimeofday`), 모듈을 올리는(`sys_init_module`) 등 위험한 시스템 콜을 부르는 것을 막아야 한다.
   - **아키텍처 적용 ([[080_seccomp|Seccomp]]-[[069_ebpf|bpf]])**: [[063_docker_architecture|도커]]([[063_docker_architecture|Docker]])나 쿠버네티스는 [[561_container_based_deployment|컨테이너]]를 띄울 때 기본적으로 **[[080_seccomp|Seccomp]] ([[080_seccomp|Secure Computing Mode]])** 프로파일을 입힌다. 
   - [[561_container_based_deployment|컨테이너]] 내부의 앱이 트랩(`syscall`)을 날려 [[022_kernel_role|커널]]로 진입하려 할 때, [[022_kernel_role|커널]]의 얕은 입구에서 [[069_ebpf|BPF]] 필터가 가동된다. "얘가 부른 시스템 콜 번호가 화이트리스트에 있나?"를 검사하고, 금지된 번호(예: `init_module`)라면 [[022_kernel_role|커널]] 깊숙이 들어오기 전에 즉시 프로세스를 강제 종료(SIGKILL)시켜버리는 완벽한 샌드박스를 구축한다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 시스템 콜(트랩) 오버헤드 감소 아키텍처 튜닝 플로우          │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [서버 성능 모니터링 중 %sys(커널 시간)가 %user(유저 시간)를 압도함]           │
  │                │                                                  │
  │                ▼                                                  │
  │      strace 명령어로 분석 시, 엄청나게 작은 크기의 read/write가 남발되는가?│
  │          ├─ 예 ─────▶ [Application Buffer Size 증가 튜닝]            │
  │          │            (10바이트씩 10번 부르지 말고, 100바이트 1번 부르게 수정)│
  │          └─ 아니오 (대용량 파일 전송이나 대량 네트워크 소켓 통신이다)       │
  │                │                                                  │
  │                ▼                                                  │
  │      사용 중인 I/O 모델이 여전히 동기식(Blocking) I/O인가?                │
  │          ├─ 예 ─────▶ [Zero-Copy 및 I/O 다중화 프레임워크 전환]       │
  │          │            (sendfile, epoll, kqueue 등을 사용하여 시스템 콜 횟수│
  │          │             자체를 기하급수적으로 감소시킴)                  │
  │          │                                                        │
  │          └─ 아니오 ──▶ 최신 커널의 `io_uring` 백엔드 전면 도입 검토        │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 초보 개발자는 CPU 코어가 100%를 치면 "로직이 무거운가?"하고 알고리즘만 뒤진다. 하지만 실제 상용 서버에서는 `top` [[158_instruction|명령어]]를 쳤을 때 `%us` (유저 로직)보다 `%sy` (시스템 콜 처리 시간)가 비정상적으로 높은 경우가 허다하다. 시스템 콜은 '[[022_kernel_role|커널]]로 가는 비싼 톨게이트'다. 톨게이트 비용(트랩 오버헤드)을 줄이려면, 한 번 통과할 때 최대한 많은 짐(Buffer)을 싣고 가거나, 정기권을 끊어주는 `io_uring` 같은 차세대 터널을 파야 한다.

### 도입 [[435_checklist_based_testing|체크리스트]]
- **vDSO (Virtual Dynamically Shared Object)**: `gettimeofday()` 같이 단순히 시간만 묻는 아주 가벼운 시스템 콜조차 매번 트랩을 타고 [[022_kernel_role|커널]]로 가면 너무 느리다. 리눅스 [[022_kernel_role|커널]]이 이런 가벼운 함수들은 아예 [[022_kernel_role|커널]] 메모리의 일부를 유저 스페이스에 읽기 전용으로 매핑해 주어(vDSO), 트랩 없이 유저 모드에서 일반 함수처럼 시간을 읽어갈 수 있게 최적화되어 있는지(strace 시 노출 안 됨) 구조를 이해하고 있는가?

- **📢 섹션 요약 비유**: 구청([[022_kernel_role|커널]])에 가서 주민등록등본을 떼는 일(시스템 콜)이 너무 잦아서 교통비(트랩 비용)가 많이 듭니다. 그래서 구청장이 동네 입구에 무인 발급기(vDSO)를 설치해 주고, 이사 갈 때는 이삿짐센터(sendfile)가 알아서 처리하게 만들어 민원인의 발걸음을 확 줄여준 것입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 레거시 트랩 (`int 0x80`) | 고속 시스템 콜 (`syscall`) / [[566_mmap_zero_copy_sendfile|Zero-copy]] | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (전환 [[015_지연_데이터_관점|지연]])** | 수백 클럭([[045_clock|Clock]]) 사이클 소모 | 수십 클럭 사이클로 대폭 단축 | 유저-[[022_kernel_role|커널]] [[211_context_switch|문맥 교환]] 오버헤드 극감 |
| **정량 (I/O 처리)** | [[001_dikw_pyramid|Data]] 복사 + 트랩 오버헤드 | sendfile 등 [[022_kernel_role|커널]] 내 직접 처리 | 네트워크 [[140_bandwidth|대역폭]]([[139_throughput|Throughput]]) 한계 돌파 |
| **정성 (보안 통제)** | 시스템 콜 무제한 허용 | [[080_seccomp|Seccomp]] 기반 트랩 필터링 | 악성코드의 치명적 [[022_kernel_role|커널]] 훼손 원천 차단 |

### 미래 전망
- **io_uring의 천하 통일**: 30년간 리눅스 I/O의 패러다임은 동기에서 비동기(epoll)로 변해왔지만, 결국 시스템 콜을 부른다는 사실은 변하지 않았다. 하지만 `io_uring`은 유저 스페이스와 [[022_kernel_role|커널]] 스페이스 사이에 '거대한 공유 링 버퍼'를 파놓았다. 유저 앱이 이 버퍼에 시스템 콜 명령을 조용히 적어두면, [[022_kernel_role|커널]]의 백그라운드 워커가 트랩 없이([[013_system_call|System call]] [[585_zero_skipping|zero]] overhead) 이를 퍼가서 실행하고 결과를 돌려준다. 시스템 콜의 본질인 "트랩(Trap) 방식" 자체가 역사 속으로 사라지고 있는 혁명적 전환기다.
- **[[640_unikernel_mirageos_architecture|Unikernel]] ([[640_unikernel_mirageos_architecture|유니커널]])의 급부상**: 클라우드 가상머신 안에서 앱과 [[022_kernel_role|커널]]을 하나의 실행 [[501_file_definition_logical_record|파일]]로 합쳐버리는 [[640_unikernel_mirageos_architecture|유니커널]]은 아예 User/[[022_kernel_role|Kernel]] 권한의 경계를 없앴다. 시스템 콜을 부를 때 트랩을 발생시키지 않고 단순한 `C 언어 함수 호출(call)`로 대체하여, 마이크로서비스의 [[282_performance_tactics|성능]]을 수백 배 끌어올리는 극단적 아키텍처로 주목받고 있다.

### 결론
트랩(Trap) 기반 시스템 콜 구조는 [[001_operating_system_purpose|운영체제]]가 '안전([[571_protection_vs_security|Protection]])'과 '[[090_service_kubernetes_network_load_balancing|서비스]] 제공([[090_service_kubernetes_network_load_balancing|Service]])'이라는 모순된 두 마리 토끼를 잡기 위해 고안해 낸 가장 절묘한 타협안이다. 하드웨어의 권한 분리(Ring) 원칙을 철저히 지키면서도, `syscall`이라는 약속된 주문을 통해 인간(유저)과 신([[022_kernel_role|커널]])의 소통 창구를 열어주었다. 현대 IT 인프라 [[282_performance_tactics|성능]] 튜닝의 역사는 바로 이 "어떻게 하면 시스템 콜을 덜 부를 수 있을까?"에 대한 집요한 연구의 역사이며, 그 끝에서 `io_uring`과 `eBPF`라는 클라우드 네이티브의 새 시대를 열었다.

- **📢 섹션 요약 비유**: 신([[022_kernel_role|커널]])과 인간(앱) 사이를 가로막은 절대적인 차원의 벽(Ring [[571_protection_vs_security|보호]])을 넘기 위해, 인간이 피워 올리는 절박한 기도(트랩)와 그 기도를 듣고 벽을 열어 응답하는 신의 자비(시스템 콜)가 만들어낸 컴퓨터 공학의 신화입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[675_multitasking_terminology_preemptive|멀티태스킹]] ([[675_multitasking_terminology_preemptive|Multitasking]]) 용어 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[019_interrupt_vector|인터럽트 벡터]] 테이블 구조화 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[022_kernel_role|커널]] 모드 진입 메커니즘 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 시스템 콜 [[014_api_posix|API]] 래퍼 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[인터럽트 벡터 테이블 구조화]
    │
    ▼
[트랩 (Trap) 기반 시스템 콜 구현]
    │
    ├──▶ [커널 모드 진입 메커니즘]
    └──▶ [시스템 콜 API 래퍼]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 안에는 아주 무서운 경비원(CPU)이 지키는 금고실([[022_kernel_role|커널]])이 있어요. 일반 시민(앱)이 금고실에 함부로 들어가면 경비원이 쫓아내요.
2. 하지만 시민이 돈([[501_file_definition_logical_record|파일]], 인터넷 등)이 필요하면 꼭 금고실을 열어야 해요. 그래서 금고실 문 앞에 '비상벨(트랩)'을 만들어 두었어요.
3. 시민이 비상벨을 "띵동!" 하고 누르면(시스템 콜), 금고실 안에 있는 은행원이 나와서 부탁을 들어주고 돈을 건네줍니다. 이렇게 하면 시민이 금고를 어지럽히지 않으면서도 안전하게 일을 할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 677 / 800

← **이전**: [[676_interrupt_vector_table_architecture|676. 인터럽트 벡터 테이블 구조화 (Interrupt Vector Table Architecture)]]
**다음**: [[678_kernel_mode_entry_mechanism|678. 커널 모드 진입 메커니즘 (Kernel Mode Entry Mechanism)]] →

---
