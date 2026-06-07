---
title: "Condition Variable"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 228
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 조건 변수 (Condition Variable)는 특정 조건(상태)이 만족될 때까지 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 <strong>뮤텍스(<a href="/studynote/02_operating_system/04_synchronization/223_mutex/">Mutex</a>) 락을 풀고 수면(Sleep) 상태로 대기</strong>시키고, 조건이 만족되면 다른 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 <strong><a href="/studynote/02_operating_system/02_process_thread/130_signal/">신호</a>(<a href="/studynote/02_operating_system/02_process_thread/130_signal/">Signal</a>/Broadcast)를 보내 깨워주는</strong> 이벤트 통지형 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 객체다.
> 2. **가치**: [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 "원하는 값이 들어왔나?" 확인하려고 [임계 구역](/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/)([Critical Section](/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/)) 안에서 무한 루프([Busy Waiting](/studynote/02_operating_system/04_synchronization/227_busy_waiting/))를 도는 최악의 CPU 낭비를 막아주며, <strong><a href="/studynote/02_operating_system/04_synchronization/229_monitor/">모니터</a>(<a href="/studynote/02_operating_system/04_synchronization/229_monitor/">Monitor</a>) <a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a> 구조의 핵심 부품</strong>으로 동작한다.
> 3. **융합**: 조건 변수는 절대로 혼자 쓸 수 없으며 <strong>반드시 뮤텍스(<a href="/studynote/02_operating_system/04_synchronization/223_mutex/">Mutex</a>)와 1:1로 짝을 지어(Pairing) 사용해야만</strong> [경쟁 조건](/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/)(Lost Wakeup)을 막을 수 있는 독특한 융합 아키텍처를 가진다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 공유 데이터를 조작하려 할 때, 아직 자신이 원하는 상태(Condition, 예: 큐에 데이터가 들어옴)가 아닐 경우 일단 대기실로 물러나 자고, 다른 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 상태를 변경한 뒤 "이제 조건이 맞으니 일어나라!"라고 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 보내주는 메커니즘이다.
- **필요성**: 뮤텍스([Mutex](/studynote/02_operating_system/04_synchronization/223_mutex/))는 "방에 1명만 들어가게"는 막아주지만, 방에 들어갔는데 정작 할 일이 없으면 문제가 된다.
  예를 들어, 프린터 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 방([임계 구역](/studynote/02_operating_system/03_cpu_scheduling/214_critical_section/))에 들어갔는데 인쇄할 종이가 없다. 이때 종이가 올 때까지 방 안에서 문을 잠그고 멍때리면([Busy Waiting](/studynote/02_operating_system/04_synchronization/227_busy_waiting/)), 밖에 있는 사용자 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 종이를 넣어주려 해도 문이 잠겨있어 들어가지 못하는 <strong>치명적 데드락(<a href="/studynote/02_operating_system/05_deadlock/281_deadlock_definition/">Deadlock</a>)</strong>에 빠진다. 따라서 "종이가 없으면 일단 문을 열어주고(Unlock) 밖에서 자라"는 고급 제어 기능이 필요했다.

- **등장 배경**: C.A.R. Hoare 와 Brinch Hansen 등의 학자들이 "[세마포어](/studynote/02_operating_system/04_synchronization/224_semaphore/)가 너무 원시적이라 프로그래머들이 계속 데드락을 낸다"고 비판하며, 이를 더 고차원적이고 안전하게 제어하기 위한 <strong><a href="/studynote/02_operating_system/04_synchronization/229_monitor/">모니터</a>(<a href="/studynote/02_operating_system/04_synchronization/229_monitor/">Monitor</a>)</strong>라는 개념을 발표할 때 그 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)의 내부 핵심 부품으로 설계되었다.

```text
  [조건 변수가 없는 세상의 참사 vs 조건 변수(CV) 도입의 기적]

  [ ❌ 조건 변수 없이 무식하게 짤 때 (Spinlock) ]
  Consumer: "Mutex 잠금 --> 데이터 있나? 없네. --> Mutex 풀기" (이걸 1초에 100만 번 반복함)
  -> 결과: CPU 코어 1개가 100% 혹사당하며 발열 폭발.

  [ ✅ 조건 변수(CV)를 썼을 때 (Sleep & Wakeup) ]
  Consumer: "Mutex 잠금 --> 데이터 있나? 없네. --> CV.wait() 호출!"
            (💥 기적 발생: OS가 Consumer를 'Sleep' 시키면서 동시에 'Mutex 락'을 툭 풀어줌!)
  Producer: (락이 풀렸으므로 진입) --> 데이터 넣음 --> "CV.signal() --> 얘들아 일어나!"
  Consumer: (Wakeup!) --> 다시 Mutex를 쥐고 깨어남 --> 데이터 빼서 처리함!
```
**[다이어그램 해설]** 조건 변수의 진정한 마법은 `wait()` 함수가 호출되는 그 찰나의 순간에 있다. 내가 쥐고 있던 락([Mutex](/studynote/02_operating_system/04_synchronization/223_mutex/))을 반납함과 동시에 대기 큐로 들어가 잠드는 동작이 OS 레벨에서 완벽하게 원자적(Atomic)으로 이루어진다. 이 덕분에 CPU 낭비율 0%의 무결점 생산자-소비자 파이프라인이 완성된다.

- **📢 섹션 요약 비유**: 미용실에서 의자([Mutex](/studynote/02_operating_system/04_synchronization/223_mutex/))에 앉았는데, 아직 파마약(Condition)이 도착하지 않았습니다. 의자에 계속 앉아있으면 다른 손님이 머리를 못 깎습니다. 조건 변수는 이럴 때 의자에서 일어나 대기실 소파로 가라고 안내하고, 파마약이 도착하면 매니저([Signal](/studynote/02_operating_system/02_process_thread/130_signal/))가 소파에 자는 손님을 불러 다시 의자에 앉히는 완벽한 동선 관리입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 조건 변수의 3대 핵심 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) (POSIX [Pthreads](/studynote/02_operating_system/11_exam_summary/790_posix_threads_pthreads_standard_api/) 기준)

조건 변수(`pthread_cond_t`)는 절대 혼자 쓰이지 않으며 반드시 뮤텍스(`pthread_mutex_t`)와 함께 파라미터로 엮여 들어간다.

1. <strong><code>wait(cond, mutex)</code></strong>:
   - 내가 쥐고 있는 `mutex`를 풀고, [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 `cond` 대기 큐에 넣어 잠재운다. (이 과정이 원자적으로 일어남)
   - 나중에 누군가 깨워주면, 다시 `mutex`를 쟁취하기 위해 싸운 뒤, 쟁취하는 순간 함수가 반환(리턴)되며 잠에서 깬다.
2. <strong><code>signal(cond)</code></strong>:
   - `cond` 대기 큐에서 자고 있는 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 중 **딱 1명만** 깨운다. (라운드 로빈이나 우선순위에 따라 OS가 고름)
3. <strong><code>broadcast(cond)</code></strong>:
   - `cond` 대기 큐에서 자고 있는 <strong>모든 <a href="/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a>를 다 깨운다</strong> (알람 대폭발). 깨어난 놈들은 각자 `mutex`를 다시 잡으려고 피 터지게 싸운다 (Thundering Herd 현상).

### 왜 `if` 가 아니라 `while` 로 묶어야 하는가? (Spurious Wakeup)

전 세계 모든 시니어 개발자가 신입에게 첫 번째로 하는 [코드 리뷰](/studynote/04_software_engineering/06_software_architecture/330_code_review/) 지적이다. **"조건 변수 wait()는 무조건 while 루프 안에서 써라!"**

```c
  // ❌ 최악의 코드 (if 사용)
  pthread_mutex_lock(&mutex);
  if (count == 0) {
      pthread_cond_wait(&cond, &mutex); // 자고 일어남
  }
  // 🚨 여기서 count가 0인데도 물건을 빼려고 해서 NullPointerException 터짐!
  take_item();
  pthread_mutex_unlock(&mutex);
```
**왜 터질까?**
1. 내가 자고 있는데 누군가 `signal()`을 쳐서 내가 깼다.
2. 그런데 내가 락을 다시 쥐기 직전의 찰나에, 엉뚱한 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 먼저 락을 쥐고 홀랑 물건을 빼가서 다시 `count = 0`이 되었다.
3. 나는 기분 좋게 락을 쥐고 `if`문을 빠져나와 물건을 집으려 했으나 허공을 짚고 에러가 난다. (이를 **가짜 기상 / Spurious Wakeup** 이라 부른다).

```c
  // ✅ 완벽한 교과서적 코드 (while 사용)
  pthread_mutex_lock(&mutex);
  while (count == 0) {   // ⭐ 깨어나서도 조건이 맞는지 독하게 다시 검사함!
      pthread_cond_wait(&cond, &mutex);
  }
  take_item();
  pthread_mutex_unlock(&mutex);
```
**[해설]** OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 [하드웨어 인터럽트](/studynote/02_operating_system/01_overview_architecture/017_hardware_interrupt/) 등의 이유로 `signal()`을 안 쳤는데도 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 가끔 실수로 깨어나는 현상(Spurious Wakeup)을 스펙상 허용한다. 따라서 프로그래머는 내가 깨어났을 때 "진짜 물건이 있어서 깨운 건지, 헛것을 보고 깬 건지, 아니면 남이 쌔벼간 건지"를 `while`을 돌며 끈질기게 재검증해야만 무결성이 보장된다.

- **📢 섹션 요약 비유**: 진동벨이 울려서 [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)로 갔는데 내 햄버거가 나온 게 맞는지(while 검사) 다시 확인해야 합니다. 가끔 기계 오류로 벨이 잘못 울릴 때도 있고(가짜 기상), 다른 손님이 내 햄버거를 낚아채서 이미 가져갔을 수도(새치기) 있기 때문입니다.

---

## Ⅲ. 비교 및 연결

### [세마포어](/studynote/02_operating_system/04_synchronization/224_semaphore/)([Semaphore](/studynote/02_operating_system/04_synchronization/224_semaphore/)) vs 조건 변수(Condition Variable)

두 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 객체는 매우 비슷해 보이지만 철학이 정반대다.

| 특성 | [세마포어](/studynote/02_operating_system/04_synchronization/224_semaphore/) ([Semaphore](/studynote/02_operating_system/04_synchronization/224_semaphore/)) | 조건 변수 (Condition Variable) |
|:---|:---|:---|
| **상태 기억력 (Memory)** | [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)(`S`)가 내장되어 있어 <strong>과거의 <code>signal()</code> 횟수를 기억한다.</strong> | **기억력 제로 (Memoryless)**. 아무도 안 잘 때 `signal()` 치면 그냥 허공으로 날아간다. |
| <strong>뮤텍스와의 <a href="/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a></strong> | 스스로 [상호 배제](/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/) 기능을 할 수 있어 독고다이로 쓰임 | 스스로 락 기능이 전혀 없어 <strong>무조건 뮤텍스와 합체</strong>해야만 쓸 수 있음 |
| **사용 목적** | N개의 자원 개수 카운팅, 제한 (Throttling) | 어떤 복잡한 <strong>논리적 상태(Condition)</strong>가 달성될 때까지 대기 |
| **데드락 위험** | 개발자가 `wait`, `signal` 순서를 꼬면 100% 데드락 | `wait()`가 내부적으로 락을 자동으로 풀어주어 상대적으로 데드락 방어에 강함 |

### Lost Wakeup (잃어버린 기상)의 공포
만약 조건 변수를 쓸 때 뮤텍스를 깜빡하고 안 걸었다면?
1. [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) A가 "어? 값이 0이네, 자러 가야지(`wait` 호출 직전)" 하고 멈칫했다.
2. 그 찰나에 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) B가 값을 1로 바꾸고 `signal()`을 때렸다!
3. 근데 아직 A가 `wait()` 방에 들어가기 전이라, `signal()`은 허공으로 날아갔다 (Memoryless 이므로).
4. 그 직후 A가 `wait()` 방에 들어가서 영원한 잠(Sleep)에 빠진다. B는 이미 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 줬으므로 영원히 깨워주지 않는다.
이것이 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)의 재앙인 **Lost Wakeup** 버그다. 뮤텍스로 이 전체 과정을 단단히 묶지([Lock](/studynote/05_database/04_transactions_concurrency/510_lock/)) 않으면 조건 변수는 살인 무기로 돌변한다.

- **📢 섹션 요약 비유**: [세마포어](/studynote/02_operating_system/04_synchronization/224_semaphore/)는 "우체통"입니다. 편지([Signal](/studynote/02_operating_system/02_process_thread/130_signal/))를 넣고 가면 나중에 온 사람이 언제든 꺼내볼 수 있습니다(기억력 O). 조건 변수는 "무전기"입니다. 내가 무전을 쳤을 때 상대방이 무전기를 들고 있지 않으면(타이밍 어긋남) 그 소리는 그냥 우주로 날아가 버리고 상대는 평생 소식을 못 듣게 됩니다(기억력 X).

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오
1. <strong>Java의 <code>Object.wait()</code>와 <code>notifyAll()</code></strong>: 자바의 모든 객체(Object)는 태어날 때부터 내부에 보이지 않는 "뮤텍스 1개 + 조건 변수 1개"를 쌍으로 가지고 태어난다. (이걸 Monitor라고 부른다).
   - **실무 규칙**: 자바에서 `wait()`를 호출하려면 무조건 그 객체의 `synchronized` 블록(뮤텍스 획득) 안에 있어야 한다. 밖에서 호출하면 `IllegalMonitorStateException`을 뱉으며 뺨을 때린다. OS의 철칙(뮤텍스와 CV의 결합)을 언어 레벨에서 완벽하게 강제한 가장 성공적인 아키텍처다.
2. <strong><a href="/studynote/02_operating_system/02_process_thread/130_signal/">Signal</a> vs Broadcast (Thundering Herd Problem 방어)</strong>: 1개의 데이터가 들어왔는데 대기실에 1,000개의 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 자고 있다.
   - **아키텍트의 실수**: 아무 생각 없이 `broadcast()`를 때렸다. 1,000개가 일제히 깨어나서 뮤텍스 1개를 잡으려고 좀비떼처럼 덤벼들며 999개의 문맥 교환이 발생하여 CPU가 폭파된다(이를 <strong>Thundering Herd, 천둥 치는 소떼 현상</strong>이라 부른다).
   - **실무 조치**: 들어온 데이터가 1개뿐이라면 절대 `broadcast()`를 치지 말고 <strong><code>signal()</code> (자바에선 <code>notify()</code>)</strong>을 쳐서 딱 1마리만 조용히 깨워야 한다. 반면, "[설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 파일이 업데이트됨!"처럼 모두가 알아야 하는 글로벌 이벤트일 때는 무조건 `broadcast()`를 쳐야 999명이 영원히 자는 버그를 막을 수 있다.

```text
  +---------------------------------------------------------------------+
  |     고성능 생산자-소비자(Producer-Consumer) 아키텍처의 진화 트리    |
  +---------------------------------------------------------------------+
  |                                                                     |
  |   [요구사항: 초당 10만 건의 로그를 큐(Queue)를 통해 전달해야 함]    |
  |                |                                                    |
  |                v 동기화 도구의 선택                                 |
  |   [ 1단계: 세마포어(Semaphore) 사용 ]                               |
  |     -> 단점: 변수 3개를 조작해야 해서 코드가 더럽고 휴먼 에러 폭발.  |
  |                                                                     |
  |   [ 2단계: Mutex + 조건 변수 (Condition Variable) 사용 ]            |
  |     -> 장점: while 루프와 락의 조화로 가장 안정적인 교과서적 구현.   |
  |     -> 단점: 락 획득/해제 오버헤드와 Thundering Herd 위험성 존재.    |
  |                                                                     |
  |   [ 3단계: Language Level - BlockingQueue 사용 (Java) ]             |
  |     -> 특징: 내부적으로 2개의 조건 변수(notEmpty, notFull)를         |
  |             은닉하여 개발자가 락을 아예 안 보게 만듦. 극강의 생산성.|
  |                                                                     |
  |   [ 4단계: Lock-free 링 버퍼 (Disruptor 등) 사용 ]                  |
  |     -> 특징: 조건 변수의 Sleep조차 무거워서 아예 CAS로 뺑뺑이 돌림.  |
  |     -> 결과: OS 개입 0. 주식 거래소 수준의 Ultra-Low Latency 달성.   |
  +---------------------------------------------------------------------+
```
**[다이어그램 해설]** "조건 변수가 훌륭하다"고 해서 실무 백엔드(Java/Go)에서 개발자가 직접 `wait/notify`를 치는 것은 2010년 이전에 끝났다. 이 로직은 너무 취약해서 버그를 양산한다. 현대 엔지니어링의 정답은 OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 개발자가 조건 변수를 활용해 한 땀 한 땀 깎아 만든 안전한 [동시성](/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 컬렉션(Concurrent Collection)을 가져다 조립만 하는 것이다.

- **📢 섹션 요약 비유**: 조건 변수([CV](/studynote/12_it_management/04_sdlc_testing/156_cv_cost_variance/))를 직접 다루는 것은 식칼의 칼날을 맨손으로 쥐고 요리하는 것만큼 위험합니다. 현대의 프로그래머들은 칼날([CV](/studynote/12_it_management/04_sdlc_testing/156_cv_cost_variance/))이 안전한 손잡이(BlockingQueue, Channel)에 단단히 박혀있는 완성된 식칼을 사 와서 요리에만 집중해야 합니다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과
뮤텍스([Mutex](/studynote/02_operating_system/04_synchronization/223_mutex/))와 조건 변수([CV](/studynote/12_it_management/04_sdlc_testing/156_cv_cost_variance/))를 결합한 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)([Monitor](/studynote/02_operating_system/04_synchronization/229_monitor/)) 구조를 정확히 체화하면, 복잡한 상태([State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))를 가진 멀티스레드 애플리케이션에서 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)들이 쓸데없이 CPU를 태우지 않고 0%의 점유율로 완벽한 숙면(Sleep)을 취하다가, 데이터가 도달하는 정확히 그 나노초의 타이밍에 즉각 깨어나 처리하는 궁극의 <strong>이벤트 기반(Event-Driven) <a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a></strong>를 달성할 수 있다.

### 결론 및 미래 전망
조건 변수는 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 역사상 '[상호 배제](/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/)([Lock](/studynote/05_database/04_transactions_concurrency/510_lock/))'와 '[스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 스케줄링(Sleep/Wakeup)'이라는 두 거대한 영역을 하나의 우아한 함수(`wait()`)로 접합시켜 낸 컴퓨터 과학의 걸작이다.
미래에는 이 무거운 OS 레벨의 조건 변수가 유저 영역(User Space)으로 올라오고 있다. Go 언어의 `sync.Cond` 나 [코루틴](/studynote/02_operating_system/02_process_thread/141_coroutine/)([Coroutine](/studynote/02_operating_system/02_process_thread/141_coroutine/)) 프레임워크들은 OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 부르지 않고(시스템 콜 배제), 런타임 환경 내부에서 수십만 개의 깃털 같은 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(Fiber)들을 메모리 배열만 살짝 조작하여 1나노초 만에 재우고 깨우는 <strong>"경량화된 가상 조건 변수"</strong>의 시대로 진화하며 클라우드 스케일의 [동시성](/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)을 감당하고 있다.

- **📢 섹션 요약 비유**: 옛날엔 편지를 부치려면 무조건 국가 기관(OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 콜)인 우체국에 가서 줄을 서야 했습니다. 지금은 회사 사내 메신저(유저 레벨 [코루틴](/studynote/02_operating_system/02_process_thread/141_coroutine/))가 생겨서, 밖으로 나갈 필요 없이 자리에서 클릭 한 번이면 옆 부서 직원을 즉각 깨울(Wakeup) 수 있는 [초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 통신의 시대로 진입했습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 메모리 장벽 ([Memory Barrier](/studynote/01_computer_architecture/11_multicore_synchronization/416_memory_barrier/) / Memory Fence) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 하드웨어 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 기반 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [Compare-and-Swap](/studynote/01_computer_architecture/11_multicore_synchronization/415_compare_and_swap/) ([CAS](/studynote/02_operating_system/11_exam_summary/768_cas_compare_and_swap_lock_free/)) [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 원자적 변수 (Atomic Variable) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[하드웨어 명령어 기반 동기화]
    |
    v
[조건 변수 (Condition Variable)]
    |
    +---> [Compare-and-Swap (CAS) 명령어]
    +---> [원자적 변수 (Atomic Variable)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 조건 변수 (Condition Variable)은 컴퓨터가 여러 친구가 동시에 만져도 부딪히지 않게 순서를 맞추는 규칙이에요.
2. 먼저 하드웨어 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 기반 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)을 이해하면 조건 변수 (Condition Variable)이 왜 필요한지 더 쉽게 보여요.
3. 그래서 조건 변수 (Condition Variable)을 잘 알면 나중에 [Compare-and-Swap](/studynote/01_computer_architecture/11_multicore_synchronization/415_compare_and_swap/) ([CAS](/studynote/02_operating_system/11_exam_summary/768_cas_compare_and_swap_lock_free/)) [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)도 훨씬 쉽게 배울 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 228 / 800

<- **이전**: [227. 바쁜 대기 (Busy Waiting)](/studynote/02_operating_system/04_synchronization/227_busy_waiting/)
**다음**: [229. 모니터 (Monitor)](/studynote/02_operating_system/04_synchronization/229_monitor/) ->

---
