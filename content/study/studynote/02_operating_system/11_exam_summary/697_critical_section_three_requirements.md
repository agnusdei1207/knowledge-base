+++
weight = 697
title = "697. 임계 구역 3가지 요구조건 (Critical Section Three Requirements)"
date = "2026-05-09"
[extra]
categories = "studynote-operating-system"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[214_critical_section|임계 구역]]([[214_critical_section|Critical Section]])이란 여러 [[092_thread_lwp|스레드]]가 공유 자원(변수, [[501_file_definition_logical_record|파일]])에 접근하여 Race Condition을 유발할 수 있는 '위험한 코드 구간'을 말하며, 이 구간의 [[212_synchronization_mechanisms|동기화]]를 완벽하게 해결하려면 [[001_operating_system_purpose|운영체제]]가 제시한 **3가지 엄격한 요구조건**을 모두 충족해야만 한다.
> 2. **3대 조건**: 첫째는 동시에 두 명 이상 들어갈 수 없다는 **[[283_mutual_exclusion|상호 배제]]([[283_mutual_exclusion|Mutual Exclusion]])**, 둘째는 아무도 없으면 기다리지 않고 바로 들어가야 한다는 **[[216_progress_in_synchronization|진행]]([[216_progress_in_synchronization|Progress]])**, 셋째는 영원히 순서를 못 받고 굶어 죽는 놈이 없어야 한다는 **[[217_bounded_waiting|한정된 대기]]([[217_bounded_waiting|Bounded Waiting]])**다.
> 3. **가치/설계**: 이 3가지 조건은 [[212_synchronization_mechanisms|동기화]] [[001_algorithm_definition|알고리즘]](락, [[224_semaphore|세마포어]], [[229_monitor|모니터]])이 논리적 오류 없이 작동하기 위한 절대적인 수학적 증명 기준이며, 이 중 하나라도 깨지면 시스템은 데드락([[281_deadlock_definition|Deadlock]])이나 [[315_livelock_vs_deadlock|라이브락]]([[315_livelock_vs_deadlock|Livelock]])의 재앙에 빠지게 된다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **[[214_critical_section|임계 구역]] ([[214_critical_section|Critical Section]])**: 멀티프로세스 환경에서 두 개 이상의 프로세스가 동시에 접근해서는 안 되는 공유 [[001_dikw_pyramid|데이터]](Shared [[001_dikw_pyramid|Data]])를 읽거나 쓰는 짧은 코드 덩어리.
  - **[[214_critical_section|임계 구역]] 문제 (The Critical-Section Problem)**: 프로세스들이 [[214_critical_section|임계 구역]] 안에서 충돌하지 않도록 협력 [[295_protocol_field_tcp_udp_icmp|프로토콜]](진입 구역 $\rightarrow$ [[214_critical_section|임계 구역]] $\rightarrow$ 퇴출 구역)을 설계하는 문제.

- **필요성 (엉성한 자물쇠의 비극)**: 
  - 개발자가 [[283_mutual_exclusion|상호 배제]]를 한답시고 엉성한 코드(소프트웨어 락)를 짰다고 치자. 
  - 두 [[092_thread_lwp|스레드]]가 충돌하는 것은 막았는데([[283_mutual_exclusion|상호 배제]] 성공), 화장실에 아무도 없는데도 서로 "네가 먼저 들어가"라고 양보하다가 둘 다 영원히 못 들어가는 상황이 발생했다 ([[216_progress_in_synchronization|진행]] 조건 실패, [[315_livelock_vs_deadlock|Livelock]]).
  - 또는, A와 B만 번갈아 가며 계속 화장실을 쓰고, C는 10시간째 문 밖에서 덜덜 떨며 기다리고 있다 ([[217_bounded_waiting|한정된 대기]] 실패, [[314_starvation_prevention|Starvation]]).
  - **해결책**: "단순히 남을 못 들어오게 막는 것만으로는 부족하다. 진짜 안전하고 멈추지 않는 시스템을 만들려면 3가지 철칙을 동시에 증명해야 한다"는 공학적 기준이 확립되었다.

  - **[[214_critical_section|임계 구역]]**: 1명만 사용할 수 있는 기차 안의 1인용 공용 화장실.
  - **[[283_mutual_exclusion|상호 배제]] ([[283_mutual_exclusion|Mutual Exclusion]])**: 한 명이 화장실 안에서 볼일을 보고 있으면([[510_lock|Lock]]), 밖에 있는 사람은 절대 문을 열고 들어올 수 없다.
  - **[[216_progress_in_synchronization|진행]] ([[216_progress_in_synchronization|Progress]])**: 화장실이 비어있다면, 밖에서 기다리던 사람은 즉시 화장실에 들어갈 수 있어야 한다. (아무도 없는데 화장실 문이 고장 나서 못 들어가는 일이 없어야 함)
  - **[[217_bounded_waiting|한정된 대기]] ([[217_bounded_waiting|Bounded Waiting]])**: 내가 줄을 서고 난 후에는, 내 앞에 있던 사람들이 영원히 새치기를 반복하여 내가 화장실에 영영 못 들어가는 일(기아)이 없도록 대기 횟수에 한계가 있어야 한다.

- **발전 과정**:
  1. **[[459_quic_fec_forward_error_correction|초기]] ([[283_mutual_exclusion|상호 배제]]만 집중)**: [[016_interrupt_mechanism|인터럽트]]를 끄는(Disable [[016_interrupt_mechanism|Interrupt]]) 무식한 방식으로 해결 시도. [[216_progress_in_synchronization|진행]]과 대기는 무시됨.
  2. **피터슨 [[001_algorithm_definition|알고리즘]] (Peterson's Solution)**: 소프트웨어 레벨에서 3가지 조건을 최초로 모두 만족시킨 [[001_algorithm_definition|알고리즘]] 증명.
  3. **현대 하드웨어/OS [[212_synchronization_mechanisms|동기화]]**: TAS(Test-And-Set) 명령어와 [[224_semaphore|세마포어]] 큐를 활용하여 3대 조건을 하드웨어와 OS 레벨에서 완벽 보장.

- **📢 섹션 요약 비유**: 완벽한 교차로 신호등은 사고가 안 나야 하고([[283_mutual_exclusion|상호 배제]]), 차가 없을 땐 파란불로 빨리 바뀌어야 하며([[216_progress_in_synchronization|진행]]), 아무리 좁은 골목길이라도 언젠가는 파란불이 켜져서 차가 나갈 수 있게([[217_bounded_waiting|한정된 대기]]) 설계되어야 합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[214_critical_section|임계 구역]] 문제 해결을 위한 3대 요구조건 상세

[[001_operating_system_purpose|운영체제]] 전공 시험에 100% 출제되는 철칙이며, 시스템 엔지니어가 락([[510_lock|Lock]])을 짤 때 [[395_verification_process_review|검증]]해야 하는 3단계 필터다.

| 요구 조건 | 영문 명칭 | 정의 및 위반 시 발생하는 치명적 버그 |
|:---|:---|:---|
| **1. [[283_mutual_exclusion|상호 배제]]** | **[[283_mutual_exclusion|Mutual Exclusion]]** | 프로세스 $P_1$이 [[214_critical_section|임계 구역]]에서 실행 중일 때, 다른 어떤 프로세스도 [[214_critical_section|임계 구역]]에 진입할 수 없다.<br>$\rightarrow$ **위반 시: [[213_race_condition|Race Condition]] ([[001_dikw_pyramid|데이터]] 파괴)** |
| **2. [[216_progress_in_synchronization|진행]]** | **[[216_progress_in_synchronization|Progress]]** | [[214_critical_section|임계 구역]]이 비어있고 들어가려는 프로세스가 있다면, 들어갈 프로세스를 결정하는 과정이 **무한히 연기되어서는 안 된다**.<br>$\rightarrow$ **위반 시: [[281_deadlock_definition|Deadlock]] / [[315_livelock_vs_deadlock|Livelock]] (시스템 멈춤)** |
| **3. [[217_bounded_waiting|한정된 대기]]**| **[[217_bounded_waiting|Bounded Waiting]]** | 프로세스가 [[214_critical_section|임계 구역]] 진입을 요청한 후부터 허락될 때까지, **다른 프로세스들이 새치기(진입)할 수 있는 횟수에 한계(Bound)가 있어야 한다**.<br>$\rightarrow$ **위반 시: [[314_starvation_prevention|Starvation]] (기아, 영원한 굶주림)** |

---

### [[001_algorithm_definition|알고리즘]] [[395_verification_process_review|검증]]: "[[216_progress_in_synchronization|진행]]([[216_progress_in_synchronization|Progress]])" 조건이 깨지는 나쁜 코드 예시

단순히 `turn` 변수 1개만으로 [[212_synchronization_mechanisms|동기화]]를 구현한 전형적인 초보자의 코드(Strict Alternation)다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 진행(Progress) 조건을 위반한 잘못된 Lock 설계          │
  ├───────────────────────────────────────────────────────────────────┤
  │  [상황: 공유 변수 `turn = 0` (0이면 P0 차례, 1이면 P1 차례)]               │
  │                                                                   │
  │   [ Process 0 의 코드 ]                   [ Process 1 의 코드 ]       │
  │  while (turn != 0) { 대기 };          while (turn != 1) { 대기 }; │
  │  (임계 구역 실행)                          (임계 구역 실행)               │
  │  turn = 1;                             turn = 0;                  │
  │                                                                   │
  │  [버그 발생 시나리오 - Livelock 발생]                                    │
  │   1. P0가 임계 구역을 끝내고 `turn = 1`로 바꾼 뒤 종료함.                   │
  │   2. P1은 임계 구역에 들어갈 마음이 아예 없음 (화장실 안 급함).                │
  │   3. 시간이 흘러 P0가 다시 화장실이 급해져서 코드를 실행함.                    │
  │   4. P0: "어? turn이 1이네? P1이 들어갈 차례인가 보다. 기다려야지."            │
  │   5. P1은 들어갈 생각이 없고, P0는 P1이 들어가서 0으로 바꿔주길 영원히 기다림.    │
  │                                                                   │
  │  ★ 결론: 임계 구역(화장실)은 텅 비어있는데, P0가 들어가지 못하고 무한 대기함.   │
  │          이것이 바로 "진행(Progress)" 조건 위반의 전형적인 모습이다.          │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** [[283_mutual_exclusion|상호 배제]](동시 입장 금지)는 완벽히 성공했다. 하지만 "양보의 저주"에 빠졌다. 내가 화장실이 급한데 화장실이 비어있으면 그냥 들어가야지([[216_progress_in_synchronization|Progress]]), 화장실 생각도 없는 옆 사람에게 "너 먼저 가"라고 강요하는 [[001_algorithm_definition|알고리즘]]은 시스템을 데드락(멈춤)으로 몰고 간다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 피터슨의 [[001_algorithm_definition|알고리즘]] (Peterson's Solution): 3조건 완벽 충족

과거 소프트웨어만으로 3가지를 모두 쟁취한 피터슨의 천재적 코드다. `turn`과 `flag[2]` 배열을 조합했다.

```c
  // Process 0의 진입 코드
  flag[0] = true;          // 나 화장실 급해! (의사 표현)
  turn = 1;                // 근데 일단 너(P1) 먼저 들어가! (양보)
  while (flag[1] && turn == 1); // P1도 급하고, P1 차례면 난 여기서 기다림.
```
| 요구 조건 | 증명 방식 |
|:---|:---|
| **1. [[283_mutual_exclusion|상호 배제]]** | 둘 다 깃발(`flag`)을 들었더라도, `turn`은 동시에 0과 1이 될 수 없으므로 무조건 한 명만 `while` 문을 탈출함 ([[283_mutual_exclusion|상호 배제]] 성공). |
| **2. [[216_progress_in_synchronization|진행]]** | P1이 화장실에 안 급하면 `flag[1] = false` 이므로, P0는 `turn`과 상관없이 `while`을 즉시 탈출하여 진입함 ([[216_progress_in_synchronization|진행]] 성공). |
| **3. [[217_bounded_waiting|한정된 대기]]**| P1이 화장실을 쓰고 나오면 `flag[1] = false`가 되며, 다음에 또 들어오려 해도 `turn = 0`으로 P0에게 먼저 양보해야 하므로 P0는 무조건 1턴 안에 화장실을 감 (기아 방지 성공). |

### 과목 융합 관점

- **컴퓨터구조 ([[089_contract_account_smart_contract|CA]])**: 현대 컴퓨터 공학에서 '피터슨 [[001_algorithm_definition|알고리즘]]'은 쓰레기 코드가 되었다. 현대 CPU는 [[282_performance_tactics|성능]] 향상을 위해 컴파일러나 CPU 자체가 메모리 [[289_cqrs_db|쓰기]]/읽기 순서를 자기 마음대로 뒤집어버리는 **비순차적 실행(Out-of-Order Execution) 및 Memory Reordering**을 수행하기 때문이다. `flag[0] = true` 보다 `turn = 1`이 먼저 실행되는 순간, [[283_mutual_exclusion|상호 배제]]가 와장창 깨져버린다. 따라서 현대에는 이런 S/W 락 대신 하드웨어가 순서를 보장해 주는 `Memory Barrier`와 `Atomic` 명령어를 써야 한다.

- **📢 섹션 요약 비유**: 피터슨 [[001_algorithm_definition|알고리즘]]은 논리적으로 완벽한 체스 게임입니다. 하지만 현대 CPU는 속도를 높이기 위해 체스판의 말을 마음대로 두 칸씩 옮겨버리는 반칙(Memory Reordering)을 씁니다. 그래서 아무리 논리가 완벽해도 하드웨어의 통제가 없으면 무용지물이 됩니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — [[222_spinlock|스핀락]]([[222_spinlock|Spinlock]])의 [[217_bounded_waiting|한정된 대기]]([[217_bounded_waiting|Bounded Waiting]]) 실패**: 64코어 리눅스 서버 [[022_kernel_role|커널]] 개발. 1번 코어가 [[222_spinlock|스핀락]]을 쥐고 있고, 2번부터 64번 코어가 락을 얻으려고 `while(lock == 1)`로 무한 루프를 돌며 기다리고 있다.
   - **원인 분석**: 1번 코어가 락을 푼 순간([[510_lock|lock]] = 0), 2번부터 64번 코어가 동시에 덤벼든다(Thundering Herd). 이때 하드웨어 [[344_bus|버스]] 중재기가 우연히 64번 코어에게 락을 줘버렸다. 2번 코어는 제일 먼저 와서 기다렸는데도 계속 밀려서 영원히 락을 얻지 못하고 굶어 죽었다. ([[217_bounded_waiting|Bounded Waiting]] 위반, [[314_starvation_prevention|Starvation]])
   - **아키텍처 적용 (Ticket [[510_lock|Lock]] 도입)**: 현대 리눅스 [[022_kernel_role|커널]]은 이런 무자비한 경쟁을 막기 위해 은행 번호표 방식의 **티켓 [[222_spinlock|스핀락]](Ticket [[510_lock|Lock]])**이나 **qspinlock**을 도입했다. 프로세스가 락을 요청할 때 번호표를 뽑게 만들고, 번호 순서대로 락을 획득하게 함으로써 "새치기 금지([[217_bounded_waiting|한정된 대기]] 충족)" 요건을 하드웨어 레벨에서 완벽히 보장한다.

2. **시나리오 — [[532_microservices_decomposition_patterns|마이크로서비스]] 간 [[136_variance|분산]] 락(Distributed [[510_lock|Lock]])의 [[216_progress_in_synchronization|진행]]([[216_progress_in_synchronization|Progress]]) 실패**: 10대의 결제 서버가 Redis를 이용해 [[136_variance|분산]] 락(`SETNX`)을 걸고 결제를 처리한다. A 서버가 락을 걸고 DB에 쓰는 도중에, A 서버의 랜선이 뽑혀서 서버가 날아갔다.
   - **원인 분석**: A 서버는 죽었지만 Redis에 걸어둔 락([[510_lock|Lock]])은 영원히 안 풀린다. B, C 서버는 [[214_critical_section|임계 구역]](결제 로직)이 텅텅 비어있는데도 락이 걸려있어 결제를 못 하고 시스템 전체가 멈춰 섰다. ([[216_progress_in_synchronization|진행]] [[216_progress_in_synchronization|Progress]] 조건의 치명적 붕괴).
   - **대응 (기술사적 가이드)**: [[136_variance|분산]] 락 설계 시 절대 락을 무한히 쥐게 놔두면 안 된다. [[542_redis|Redis]] 락에 반드시 **[[294_ttl_time_to_live_looping_prevention|TTL]](Time-To-Live, 만료 시간)**을 3초 단위로 걸어두어, A 서버가 죽더라도 3초 뒤엔 락이 자동 소멸하여(Eviction) 다른 서버가 [[214_critical_section|임계 구역]]으로 들어갈 수 있도록([[216_progress_in_synchronization|Progress]] 보장) 아키텍처를 방어해야 한다 (Redlock [[001_algorithm_definition|알고리즘]]의 뼈대).

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 시스템 동기화 락(Lock) 메커니즘 설계 검증 플로우           │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [자체적인 락이나 동기화 알고리즘을 개발/적용할 때의 3단계 검문]               │
  │                │                                                  │
  │                ▼                                                  │
  │      1. [상호 배제 확인] 두 스레드가 정확히 0.0001초 차이로 진입해도          │
  │         둘 중 하나는 반드시 블로킹되거나 튕겨 나가는가? (원자성 여부)           │
  │          ├─ 실패 ─▶ 데이터 오염 발생. 하드웨어 CAS 연산으로 락 보강 요망       │
  │          └─ 통과                                                  │
  │                │                                                  │
  │                ▼                                                  │
  │      2. [진행(Progress) 확인] 락을 쥔 스레드가 갑자기 죽었을 때,             │
  │         다른 스레드들이 락을 탈취(Timeout/Recovery)할 메커니즘이 있는가?    │
  │          ├─ 실패 ─▶ 데드락 발생. 타임아웃 큐 또는 OS 반환 기능 도입 요망       │
  │          └─ 통과                                                  │
  │                │                                                  │
  │                ▼                                                  │
  │      3. [한정된 대기 확인] 트래픽이 미친 듯이 몰릴 때, 가장 운 없는 스레드라도 │
  │         결국에는 락을 얻을 수 있다는 대기 큐(Wait Queue/FIFO)가 보장되는가? │
  │          ├─ 실패 ─▶ 특정 스레드 타임아웃 및 에러 뿜음. 공평한 큐잉 로직(RR) 필요│
  │          └─ 통과 ─▶ [완벽하고 안전한 임계 구역 설계 완료!]                │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** "[[283_mutual_exclusion|상호 배제]]만 잘되면 된 거 아냐?"라는 안일한 생각이 수백억 짜리 시스템을 멈추게 한다. [[283_mutual_exclusion|상호 배제]]는 '[[001_dikw_pyramid|데이터]]'를 지키는 조건이고, [[216_progress_in_synchronization|진행]]과 [[217_bounded_waiting|한정된 대기]]는 '시스템의 생명(Liveness)'을 지키는 조건이다. 아무리 [[001_dikw_pyramid|데이터]]가 깨끗해도 시스템이 멈춰있으면 그건 죽은 서비스다. 3가지 조건은 타협 불가능한 삼위일체(Trinity)다.

### 도입 [[435_checklist_based_testing|체크리스트]]
- **[[016_interrupt_mechanism|인터럽트]] 비활성화(cli)의 함정**: 싱글 코어 임베디드 장비에서 가장 쉽게 [[283_mutual_exclusion|상호 배제]]를 달성하는 방법은 아예 CPU의 [[016_interrupt_mechanism|인터럽트]]를 꺼버리는(`cli`) 것이다. 하지만 이 짓을 하면 멀티코어에서는 다른 코어가 쳐들어오는 걸 못 막을뿐더러, [[214_critical_section|임계 구역]] 안에서 에러가 나면 [[016_interrupt_mechanism|인터럽트]]가 영원히 안 켜져서 시스템 시계조차 멈춰버리는([[216_progress_in_synchronization|진행]] 조건 붕괴) 최악의 결과가 나온다. 유저 모드에서는 절대 [[016_interrupt_mechanism|인터럽트]]를 끄는 권한을 줘서는 안 된다.

- **📢 섹션 요약 비유**: 3가지 조건은 놀이공원 롤러코스터 규칙입니다. 한 칸에 1명만 타야 하고([[283_mutual_exclusion|상호 배제]]), 자리가 비었으면 열차를 놀리지 말고 바로 채워야 하며([[216_progress_in_synchronization|진행]]), 아무리 줄이 길어도 VIP 패스가 무한정 새치기해서 일반 줄이 하루 종일 멈춰있게 하면 안 됩니다([[217_bounded_waiting|한정된 대기]]).

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| [[214_critical_section|임계 구역]] 요구조건 | 결여 시 발생하는 치명적 현상 | 완벽 충족 시의 시스템 상태 |
|:---|:---|:---|
| **1. [[283_mutual_exclusion|상호 배제]] ([[283_mutual_exclusion|Mutual Exclusion]])**| Race Condition으로 잔고 마이너스, 결제 중복 | [[001_dikw_pyramid|데이터]] 정합성 100% ([[193_atomicity_all_or_nothing|원자성]] 확보) |
| **2. [[216_progress_in_synchronization|진행]] ([[216_progress_in_synchronization|Progress]])** | [[315_livelock_vs_deadlock|Livelock]], Deadlock으로 시스템 Hang | 락 해제 즉시 다음 작업 속개 ([[139_throughput|Throughput]] 방어) |
| **3. [[217_bounded_waiting|한정된 대기]] ([[217_bounded_waiting|Bounded Waiting]])**| Starvation으로 특정 유저 무한 로딩 | P99.9 [[138_response_time|응답 시간]] 보장 (Tail [[141_latency|Latency]] [[656_ir_containment|억제]]) |

### 미래 전망
- **Wait-Free [[001_dikw_pyramid|데이터]] 구조의 등장**: 3가지 조건을 충족시키기 위해 '락([[510_lock|Lock]])'을 쓰는 것 자체가 구시대의 유물이 되어가고 있다. 최고급 아키텍처는 아예 락을 없애고, 모든 [[092_thread_lwp|스레드]]가 Bounded Waiting과 Progress를 수학적으로 100% 보장하면서 각자 메모리를 덮어쓰지 않고 전진하는 **Wait-Free [[001_algorithm_definition|알고리즘]]**을 지향하고 있다. (구현 난이도가 박사급이지만, [[282_performance_tactics|성능]]은 궁극이다.)
- **언어 차원의 런타임 보증**: 개발자가 3가지 조건을 실수로 놓치는 것을 막기 위해, Go의 채널(Channel)이나 Java의 `java.util.concurrent` 패키지는 내부적으로 이 3조건이 완벽히 증명된 컴포넌트만을 조합하여 쓰도록 강제함으로써 [[014_concurrency|동시성]] 버그를 원천 차단하고 있다.

### 결론
[[214_critical_section|임계 구역]]([[214_critical_section|Critical Section]]) 문제의 3가지 요구 조건은 멀티스레딩이라는 혼돈의 세계에 질서를 부여하기 위해 컴퓨터 공학자들이 세운 절대 헌법이다. "동시에 들어가지 마라(안전성), 빈자리는 빨리 채워라(효율성), 아무도 소외시키지 마라(공정성)." 이 3가지 계명은 단순히 코드를 짜는 규칙을 넘어, 복잡한 현대 [[136_variance|분산]] 시스템과 [[532_microservices_decomposition_patterns|마이크로서비스]] 간의 통신([[619_msa_traffic_hardware|MSA]])을 설계할 때 [[171_idempotency_iac_terraform|멱등성]]([[194_idempotency|Idempotency]])과 함께 반드시 [[395_verification_process_review|검증]]해야 할 가장 아름답고 논리적인 철학적 잣대다.

- **📢 섹션 요약 비유**: 이 3가지 조건은 [[014_concurrency|동시성]]([[266_other_transparency|Concurrency]])이라는 사나운 말을 길들이는 세 가닥의 고삐입니다. 하나라도 끊어지면 말은 [[077_radix|기수]]([[001_dikw_pyramid|데이터]])를 떨어뜨리거나, 제자리에 멈추거나, 누군가를 짓밟게 됩니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[092_thread_lwp|스레드]] [[212_synchronization_mechanisms|동기화]] [[283_mutual_exclusion|상호 배제]] | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[213_race_condition|경쟁 조건]] ([[213_race_condition|Race Condition]]) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| Test-and-Set 연산 하드웨어 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[699_mutex_lock_sleep_wait|뮤텍스 락]] ([[699_mutex_lock_sleep_wait|Mutex Lock]]) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[경쟁 조건 (Race Condition)]
    │
    ▼
[임계 구역 3가지 요구조건 (Critical Section Three Requirements)]
    │
    ├──▶ [Test-and-Set 연산 하드웨어]
    └──▶ [뮤텍스 락 (Mutex Lock)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 화장실([[214_critical_section|임계 구역]])을 완벽하게 쓰려면 3가지 철칙이 필요해요! 첫째, 내가 똥 싸고 있을 땐 **절대 남이 문 열고 들어오면 안 돼요([[283_mutual_exclusion|상호 배제]])**.
2. 둘째, 화장실에 아무도 없는데 바깥에서 친구들끼리 "너 먼저 가, 아니야 너 먼저 가" 하다가 **아무도 못 들어가는 바보 같은 짓을 하면 안 돼요([[216_progress_in_synchronization|진행]])**.
3. 셋째, 내가 줄을 서고 있는데 다른 덩치 큰 애들이 **계속 내 앞으로 새치기를 해서 내가 영원히 바지에 오줌을 싸게 만들면 안 돼요([[217_bounded_waiting|한정된 대기]])**. 이 3개가 지켜져야 평화로운 화장실이랍니다!
