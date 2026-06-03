+++
weight = 687
title = "687. 선점 / 비선점 스케줄링 차이 (Preemptive Vs Non Preemptive Scheduling)"
date = "2026-05-09"
[extra]
categories = "studynote-operating-system"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CPU 스케줄링의 가장 근본적인 [[104_classification_analysis|분류]] 기준으로, 프로세스가 CPU를 잡았을 때 **"스스로 내놓을 때까지 기다려줄 것인가([[285_no_preemption|비선점]])"** 아니면 **"OS가 중간에 강제로 뺏을 수 있는가(선점)"**의 권력 구조 차이를 의미한다.
> 2. **[[285_no_preemption|비선점]] (Non-Preemptive)**: 한 번 CPU를 잡으면 I/O 대기나 종료 전까지 절대 뺏기지 않는다. 오버헤드([[211_context_switch|문맥 교환]])가 적어 과거의 일괄 처리 시스템에 쓰였으나, 버그 난 프로그램 하나가 전체 시스템을 멈추게 하는 치명적 단점이 있다.
> 3. **선점 (Preemptive)**: 타이머 [[016_interrupt_mechanism|인터럽트]] 등을 통해 OS가 정해진 시간(타임 [[331_neuromorphic_ai_db|슬라이스]])마다 강제로 CPU를 뺏어 다른 프로세스에게 넘긴다. 오버헤드가 크고 [[212_synchronization_mechanisms|동기화]]([[510_lock|Lock]]) 문제가 생기지만, 빠른 응답 속도를 보장하여 현대 시분할 [[675_multitasking_terminology_preemptive|멀티태스킹]] OS의 표준이 되었다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **[[167_non_preemptive_scheduling|비선점형 스케줄링]] (Non-Preemptive)**: 실행 중인 프로세스가 I/O를 요청하거나 스스로 종료할 때까지 CPU를 계속 독점하는 방식.
  - **[[166_preemptive_scheduling|선점형 스케줄링]] (Preemptive)**: OS가 [[017_hardware_interrupt|하드웨어 인터럽트]]를 이용해 실행 중인 프로세스의 CPU를 강제로 회수하고, 다른 우선순위가 높은 프로세스에 할당할 수 있는 방식.

- **필요성 (독재의 종식과 반응성 확보)**: 
  - [[285_no_preemption|비선점]]형 방식에서는 개발자가 실수로 `while(true)` 무한 루프 코드를 짜면, 그 프로세스가 CPU를 영원히 쥐고 놔주지 않아서 마우스도 안 움직이고 컴퓨터 전체가 먹통(Freeze)이 된다.
  - 시간이 중요한 대화형 시스템(사용자 입력)에서는, 다른 무거운 작업이 돌고 있더라도 내 키보드 입력이 즉시 처리되어야 한다.
  - **해결책**: 프로세스의 '자발적 양보'에 기대는 순진한 생각을 버리고, OS [[022_kernel_role|커널]]이 타이머 칩(하드웨어)을 무기로 삼아 **"시간 다 됐어! 강제 하차해!"**라고 쫓아내는 선점형(강압적) 스케줄링이 필수적으로 대두되었다.

  - **[[285_no_preemption|비선점]]형**: 마이크를 한 번 잡으면, 자기가 연설을 스스로 끝내고 내려오기 전까지는 아무도 마이크를 뺏을 수 없는 자유 발언대. 한 명이 10시간 떠들면 나머지 사람은 다 집에 가야 한다.
  - **선점형**: 1분마다 무조건 마이크 전원을 꺼버리고 다음 사람에게 마이크를 강제로 넘기는 TV 토론. 누군가 헛소리를 길게 늘어놓아도 1분 뒤면 입이 막히므로 토론회 전체가 마비되지 않는다.

- **발전 과정**:
  1. **[[459_quic_fec_forward_error_correction|초기]] OS ([[285_no_preemption|비선점]])**: [[173_fcfs_scheduling|FCFS]](First Come First Served), [[175_sjf_scheduling|SJF]]([[175_sjf_scheduling|Shortest Job First]]). 스위칭 오버헤드가 없어 연산 효율은 좋음.
  2. **과도기 (협력적 [[675_multitasking_terminology_preemptive|멀티태스킹]])**: Windows 3.1, [[673_mac_message_authentication_code|Mac]] OS 9. 앱들이 스스로 `yield()`를 불러서 양보하게 만듦 (결국 [[285_no_preemption|비선점]]의 일종이라 잘 멈춤).
  3. **현대 OS (선점형)**: Windows NT, Linux, macOS. [[834_load_balancing_algorithm_round_robin_least_connection|RR]](Round Robin), [[177_srtf_scheduling|SRTF]], [[691_mlfq_multi_level_feedback_queue|MLFQ]]. [[017_hardware_interrupt|하드웨어 인터럽트]] 기반의 절대 권력 통제.

- **📢 섹션 요약 비유**: [[285_no_preemption|비선점]]형이 '착한 사람(양보하는 프로세스)들만 산다는 가정'하에 만든 유토피아 법이라면, 선점형은 '누구든 배신(무한 루프)할 수 있다'는 비관적 전제하에 만들어진 냉혹한 공권력(OS) 통치 체제입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[079_kube_scheduler_pod_placement|스케줄러]]가 개입하는 4가지 상황 (결정적 차이)

프로세스의 상태 변화 중 [[079_kube_scheduler_pod_placement|스케줄러]]가 언제 개입하느냐에 따라 선점과 [[285_no_preemption|비선점]]이 나뉜다.

1. `Running` $\rightarrow$ `Waiting(Block)` : (예: I/O 요청 시 스스로 잠듦)
2. `Running` $\rightarrow$ `Terminated` : (예: 프로그램 정상 종료)
3. **`Running` $\rightarrow$ `Ready` : (예: 타이머 만료로 강제 쫓겨남) ★**
4. **`Waiting` $\rightarrow$ `Ready` : (예: I/O가 끝난 애가 기존 실행 놈을 새치기함) ★**

- **[[285_no_preemption|비선점]]형**: 1번과 2번 상황에서만 [[079_kube_scheduler_pod_placement|스케줄러]]가 동작한다. (프로세스가 '스스로' 비킬 때만 개입)
- **선점형**: 1, 2번뿐만 아니라 **3번(시간 초과)과 4번([[205_priority_inversion|우선순위 역전]])** 상황에서도 OS가 개입해 강제로 CPU를 뺏는다.

---

### [[166_preemptive_scheduling|선점형 스케줄링]]의 2가지 핵심 무기 ([[071_os_timer|Timer]] & [[016_interrupt_mechanism|Interrupt]])

선점(강제로 뺏기)이 성립하려면 소프트웨어(OS)의 힘만으로는 안 되고 **하드웨어의 지원**이 절대적으로 필요하다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 선점형 스케줄링의 강제 탈취 메커니즘                   │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  [상황: 악성 앱 A가 `while(true)`를 돌며 CPU 100% 독점 중]             │
  │                                                                   │
  │  1. 하드웨어 타이머 (APIC Timer)                                     │
  │     - 메인보드의 시계 칩이 10ms(타임 슬라이스)마다 전기 신호를 발생시킴.        │
  │     - "띠딕! 10ms 지났다!"                                          │
  │                                                                   │
  │  2. 인터럽트 발생 (Hardware Interrupt)                               │
  │     - CPU는 악성 앱 A의 코드를 실행하다가 이 전기 신호를 맞고 강제로 멈춤.    │
  │     - 제어권이 즉시 OS 커널(ISR: Interrupt Service Routine)로 넘어감! │
  │                                                                   │
  │  3. 커널 스케줄러 개입 (Context Switch)                              │
  │     - OS: "A야, 네 시간(10ms) 다 썼어. 방 빼."                        │
  │     - A의 레지스터를 강제로 PCB에 저장하고, 앱 B를 메모리에서 깨움.          │
  │                                                                   │
  │  [결과] 아무리 지독한 무한 루프 코드도 하드웨어 타이머 앞에서는 10ms짜리에 불과함.│
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 초보 개발자는 "[[001_operating_system_purpose|운영체제]]가 주기적으로 프로세스를 감시한다"고 생각하지만 틀렸다. CPU가 악성 코드를 돌리고 있을 때는 [[001_operating_system_purpose|운영체제]]의 코드도 멈춰(휴면) 있다! 오직 외부에서 강제로 때려주는 **물리적 알람(타이머 [[016_interrupt_mechanism|인터럽트]])**만이 멈춰있는 OS의 영혼을 CPU로 다시 불러들여 심판의 철퇴(선점)를 내리게 할 수 있다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 대표적인 스케줄링 [[001_algorithm_definition|알고리즘]] [[104_classification_analysis|분류]]

| [[001_algorithm_definition|알고리즘]] 명칭 | 선점 / [[285_no_preemption|비선점]] | 특징 및 동작 방식 |
|:---|:---|:---|
| **[[173_fcfs_scheduling|FCFS]]** (First Come First Served) | **[[285_no_preemption|비선점]]** | 은행 창구 줄 서기. 먼저 온 놈이 끝날 때까지 다 씀 |
| **[[175_sjf_scheduling|SJF]]** ([[175_sjf_scheduling|Shortest Job First]]) | **[[285_no_preemption|비선점]]** | 실행 시간이 제일 짧은 놈부터. 끝날 때까지 안 뺏음 |
| **[[177_srtf_scheduling|SRTF]]** (Shortest Remaining Time First) | **선점** | SJF의 선점형. 실행 중인데 더 짧은 놈이 나타나면 뺏음 |
| **[[834_load_balancing_algorithm_round_robin_least_connection|RR]]** (Round Robin) | **선점** | 모두에게 공평하게 시간(Time [[690_round_robin_time_quantum|Quantum]])을 주고 뺏음 |
| **[[691_mlfq_multi_level_feedback_queue|MLFQ]]** (Multi-Level Feedback [[058_queue|Queue]]) | **선점** | 큐([[058_queue|Queue]])가 여러 개. 현대 OS 스케줄링의 근간 |

### 선점형의 부작용: [[211_context_switch|문맥 교환]] 오버헤드와 [[212_synchronization_mechanisms|동기화]]([[213_race_condition|Race Condition]])

선점형이 무조건 좋은 것만은 아니다. 치명적인 두 가지 대가를 치러야 한다.

1. **[[211_context_switch|Context Switch]] 오버헤드**: 강제로 뺏고 넘겨주는 행위 자체가 [[057_register|레지스터]] 복사와 [[357_tlb|TLB]] 플러시를 유발하여 시스템을 느리게 만든다.
2. **[[213_race_condition|Race Condition]] ([[001_dikw_pyramid|데이터]] 충돌)**: 프로세스 A가 공유 메모리의 `Count = 5`를 `6`으로 바꾸려는 찰나(Read만 한 상태), OS가 강제로 CPU를 뺏어 프로세스 B에게 넘겼다. B가 `Count`를 `4`로 깎고 턴을 마쳤다. 다시 A가 깨어나서 원래 하던 대로 6을 써버렸다. 정답은 5가 되어야 하는데 [[001_dikw_pyramid|데이터]]가 깨졌다. ([[285_no_preemption|비선점]]형에서는 절대 발생하지 않는 문제)

- **📢 섹션 요약 비유**: 경찰(선점형 OS)이 너무 자주 개입하면 동네(시스템)가 안전해지지만, 사람들이 걸핏하면 멈춰서 신분증 검사를 받아야 하니 피곤해지고(오버헤드), 말하던 중간에 강제로 말이 끊겨 오해가 쌓이게 됩니다([[212_synchronization_mechanisms|동기화]] 문제).

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — [[016_interrupt_mechanism|인터럽트]] 처리 중의 [[022_kernel_role|커널]] 선점([[022_kernel_role|Kernel]] Preemption) 금지로 인한 랙(Lag)**: 과거 구형 리눅스 서버(2.4 [[288_version_ihl_tos_total_length|버전]] 이하)에서 커다란 파일을 디스크에서 지우고([[197_rm_rate_monotonic_scheduling|rm]]) 있으면, 마우스 커서마저 안 움직이고 서버 전체가 뚝뚝 끊기는 현상.
   - **원인 분석**: 유저 프로그램끼리는 "선점형([[834_load_balancing_algorithm_round_robin_least_connection|RR]])"이라도, 프로그램이 시스템 콜을 호출해 **"[[022_kernel_role|커널]] 모드(Ring 0)"**로 들어간 순간, 옛날 리눅스는 그 [[022_kernel_role|커널]] 코드를 '[[285_no_preemption|비선점]]형'으로 취급했다. 즉, [[022_kernel_role|커널]]이 파일을 지우는 무거운 작업을 하는 동안에는 다른 유저 앱이 아무리 급해도 CPU를 뺏을 수 없었다.
   - **아키텍처 대응 (Preemptible [[022_kernel_role|Kernel]])**: 리눅스 2.6부터는 `CONFIG_PREEMPT` 기능이 도입되어, [[022_kernel_role|커널]] 모드 안에서 코드가 돌고 있더라도 급한 [[016_interrupt_mechanism|인터럽트]]나 [[092_thread_lwp|스레드]]가 나타나면 **[[022_kernel_role|커널]] 코드마저 강제로 중단시키고 선점([[022_kernel_role|Kernel]] Preemption)**할 수 있게 진화하여 데스크탑의 부드러움을 쟁취했다.

2. **시나리오 — 실시간(RTOS) 환경에서의 [[205_priority_inversion|우선순위 역전]] ([[205_priority_inversion|Priority Inversion]])**: 화성 탐사선 패스파인더에서, 우선순위가 가장 높은 1번 [[092_thread_lwp|스레드]](선점형)가, 가장 낮은 3번 [[092_thread_lwp|스레드]]가 쥐고 있는 락([[510_lock|Lock]])을 기다리며 멈춰버린 대형 사고.
   - **원인 분석**: 1번이 3번의 락을 기다리는데, 중간 우선순위인 2번 [[092_thread_lwp|스레드]]가 나타나서 3번 [[092_thread_lwp|스레드]]의 CPU를 뺏어버렸다(선점). 3번은 CPU를 뺏겨서 락을 영원히 풀지 못하고, 1번도 영원히 멈추게 된 것이다. [[166_preemptive_scheduling|선점형 스케줄링]]과 락([[510_lock|Lock]])이 결합할 때 터지는 최악의 재앙이다.
   - **대응 (우선순위 [[234_uml_class_relationships_generalization_dependency|상속]], PIP)**: OS [[022_kernel_role|커널]]이 이 상황을 감지하고, 락을 쥐고 있는 비루한 3번 [[092_thread_lwp|스레드]]의 우선순위를 일시적으로 1번(최고)으로 뻥튀기(Boost)해 준다. 그러면 2번 [[092_thread_lwp|스레드]]가 감히 3번을 선점하지 못하게 되고, 3번이 빨리 락을 풀고 1번을 살려내게 된다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 시스템 요구사항에 따른 선점/비선점 모드 튜닝 플로우         │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [새로운 산업용 임베디드 또는 클라우드 OS 환경 구축]                       │
  │                │                                                  │
  │                ▼                                                  │
  │      초저지연 응답 속도(UI/UX, 실시간 제어)가 시스템의 생명인가?             │
  │          ├─ 예 ─────▶ [완벽한 선점형(Fully Preemptive) 아키텍처]      │
  │          │            대책: 타임 슬라이스를 잘게 쪼개고, 커널 내부 코드조차   │
  │          │                  언제든 강제로 뺏기도록(Preempt_RT) 튜닝      │
  │          └─ 아니오 (슈퍼컴퓨터 과학 연산, 딥러닝 AI 학습, 하둡 배치)        │
  │                │                                                  │
  │                ▼                                                  │
  │      CPU 캐시가 날아가는 문맥 교환 오버헤드를 0으로 만들어야 하는가?           │
  │          ├─ 예 ─────▶ [비선점에 가까운 튜닝 (Throughput 우선)]        │
  │          │            대책 1: CFS 스케줄러의 타임 슬라이스를 100ms 이상으로 증가│
  │          │            대책 2: 특정 코어는 `isolcpus`로 선점 스케줄러에서 배제 │
  │          │                                                        │
  │          └─ 아니오 ──▶ 일반적인 서버/데스크탑 균형 설정 (디폴트 유지)      │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 많은 사람이 "선점형이 무조건 더 좋은 최신 기술"이라고 착각한다. 선점형은 '응답성'을 위해 'CPU 전체 [[282_performance_tactics|성능]]'을 깎아 먹는 이율배반적 구조다. 빅데이터 분석이나 그래픽 렌더링 팜에서는 OS가 중간중간 끼어들어 CPU를 뺏는 선점 행위가 오히려 방해만 된다. 아키텍트는 워크로드에 맞춰 선점의 빈도([[073_tick_jiffies|Tick]] Rate)를 의도적으로 낮추는 [[285_no_preemption|비선점]] 지향 튜닝을 할 줄 알아야 한다.

### 도입 [[435_checklist_based_testing|체크리스트]]
- **Reentrancy (재진입성)**: 우리가 만든 [[333_shared_library|공유 라이브러리]](함수)가 선점형 환경에 안전한가? A 프로세스가 함수를 실행하다가 강제로 뺏겨서 B 프로세스가 동일한 함수에 진입(재진입)하더라도, 전역 변수가 꼬이지 않고 완벽히 지역 변수([[057_stack|Stack]])로만 동작하도록 100% [[147_thread_safe|Thread-safe]] 하게 짜였는가 검증해야 한다.

- **📢 섹션 요약 비유**: 칼잡이(프로세스)에게 등을 보이면 안 되는 무림(선점형 OS)에서는 항상 빈틈을 막을 방패([[510_lock|Lock]])를 들어야 하지만, 서로 절대 등을 찌르지 않기로 약속한 신사들의 결투([[285_no_preemption|비선점]]형 OS)에서는 방패를 버리고 칼질(연산)에만 집중할 수 있습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [[285_no_preemption|비선점]]형 (Non-Preemptive) | 선점형 (Preemptive) | 비교 요약 |
|:---|:---|:---|:---|
| **[[138_response_time|응답 시간]] ([[138_response_time|Response Time]])**| 예측 불가 (앞사람이 늦게 끝나면 무한 대기) | **예측 가능 (n초 이내 무조건 턴 돌아옴)** | 대화형(UI) 시스템에 필수 |
| **[[139_throughput|처리량]] ([[139_throughput|Throughput]])** | **최대화 (스위칭 오버헤드 0%)** | 다소 희생됨 ([[211_context_switch|Context Switch]] 비용) | 배치 처리에는 [[285_no_preemption|비선점]]형이 유리 |
| **[[212_synchronization_mechanisms|동기화]] ([[212_synchronization_mechanisms|Synchronization]])**| 단순함 (스스로 양보 전엔 충돌 없음) | **극도로 복잡함 ([[510_lock|Lock]], [[224_semaphore|세마포어]] 필수)** | [[213_race_condition|Race Condition]] 방어 비용 발생 |

### 미래 전망
- **사용자 공간 선점 스케줄링 (User-space Preemption)**: Go 언어의 [[140_goroutine|고루틴]]([[140_goroutine|Goroutine]])은 [[459_quic_fec_forward_error_correction|초기]]에는 [[285_no_preemption|비선점]]형(협력적)으로 동작하여 버그 시 무한 루프에 빠졌다. 하지만 Go 1.14부터는 백그라운드의 sysmon [[092_thread_lwp|스레드]]가 너무 오래 CPU를 먹는 [[140_goroutine|고루틴]]에 강제로 비동기 시그널(SIGURG)을 쏴서 탈취하는 '유저 스페이스 레벨의 [[166_preemptive_scheduling|선점형 스케줄링]]'을 도입하여 언어 런타임 자체의 안정성을 OS 급으로 끌어올렸다.
- **eBPF를 통한 선점 로직의 마이크로 컨트롤**: 리눅스 [[022_kernel_role|커널]]의 고정된 스케줄링 정책을 벗어나, 클라우드 워크로드의 특성에 맞춰 "이 [[085_pod_kubernetes_container_unit|파드]]([[198_pod_kubernetes_minimum_deployment_unit|Pod]])는 선점하지 마, 저 컨테이너는 1ms마다 선점해"라는 초정밀 스케줄링 정책을 eBPF로 런타임에 동적 삽입하는 기술이 하이퍼스케일러들의 비밀 무기가 되고 있다.

### 결론
선점(Preemption)과 [[285_no_preemption|비선점]](Non-Preemption)의 차이는 단순히 CPU를 누가 놓느냐의 차이가 아니라, "[[001_operating_system_purpose|운영체제]]와 애플리케이션 중 누구에게 시스템의 통제 권력을 쥐여줄 것인가"에 대한 철학적 결단의 산물이다. 현대 IT 생태계는 애플리케이션의 신뢰성을 부정하고 강력한 OS의 강제 권력(선점형 타이머)을 채택함으로써, 악성코드나 버그가 시스템 전체를 무너뜨리는 것을 완벽하게 막아냈다. 비록 그 대가로 락([[510_lock|Lock]])과 레이스 컨디션이라는 동시성의 지옥이 열렸지만, 그것이 수십억 명이 스마트폰 하나로 백 가지 앱을 동시에 돌릴 수 있게 만든 가장 위대한 기회비용이었음은 틀림없다.

- **📢 섹션 요약 비유**: 개인의 선의와 양보([[285_no_preemption|비선점]])에 의존하는 도덕 정치를 포기하고, 시간이 되면 가차 없이 칼을 휘둘러 권력을 강제로 회수(선점)하는 냉혹한 법치주의를 도입한 덕분에, 수많은 앱들이 다 같이 평화롭게 공존하는 현대 [[001_operating_system_purpose|운영체제]]라는 거대한 제국이 완성되었습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[685_short_term_scheduler_dispatcher|단기 스케줄러 디스패치]] | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| CPU 바운드 vs I/O 바운드 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[173_fcfs_scheduling|FCFS]] [[174_convoy_effect|호위 효과]] ([[174_convoy_effect|Convoy Effect]]) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[175_sjf_scheduling|SJF]] 기아 ([[314_starvation_prevention|Starvation]]) 발생 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[CPU 바운드 vs I/O 바운드]
    │
    ▼
[선점 / 비선점 스케줄링 차이 (Preemptive Vs Non Preemptive Scheduling)]
    │
    ├──▶ [FCFS 호위 효과 (Convoy Effect)]
    └──▶ [SJF 기아 (Starvation) 발생]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감이 하나뿐인 놀이방에서, '[[285_no_preemption|비선점]]형' 규칙은 "한 친구가 다 놀고 스스로 장난감을 내려놓을 때까지 무조건 기다려야 해"라는 천사들의 규칙이에요. (근데 안 내려놓으면 아무도 못 놀아요!)
2. '선점형' 규칙은 선생님([[001_operating_system_purpose|운영체제]])이 10분짜리 알람 시계를 들고 있다가, 띠링 울리면 놀던 친구의 장난감을 강제로 확 뺏어서 다음 친구에게 줘버리는 무서운 규칙이에요.
3. 뺏길 땐 억울하지만, 선생님이 이렇게 강제로 뺏어주지 않으면 욕심쟁이 친구 한 명 때문에 놀이방이 망해버리니까 지금은 모든 컴퓨터가 이 '선점형(강제 뺏기)' 규칙을 쓴답니다!
