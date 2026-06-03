---
title: 698. Test-and-Set 연산 하드웨어 (Test And Set Hardware Atomic)
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Test-and-Set(TAS) 연산은 [[014_concurrency|동시성]] 프로그래밍에서 "변수의 현재 값을 [[396_validation|확인]](Test)하고 동시에 새로운 값으로 덮어쓰는(Set)" 두 가지 동작을 **하드웨어(CPU)가 절대 끊기지 않는 1개의 원자적(Atomic) 기계어로 묶어버린 치트키**다.
> 2. **메커니즘**: 소프트웨어로 `if (lock == 0) { lock = 1; }`을 짜면 두 줄 사이에 [[211_context_switch|문맥 교환]]이 발생해 레이스 컨디션이 터지지만, 하드웨어 [[158_instruction|명령어]]인 `TSL (Test and Set Lock)`이나 `CMPXCHG`를 쓰면 CPU가 **메모리 [[344_bus|버스]]를 잠가버리고([[344_bus|Bus]] [[510_lock|Lock]])** 이 두 단계를 한 호흡에 끝내버린다.
> 3. **가치**: 피터슨의 [[001_algorithm_definition|알고리즘]] 같은 무겁고 취약한 소프트웨어 [[212_synchronization_mechanisms|동기화]]를 영원히 멸종시켰으며, 현대 OS의 모든 뮤텍스([[223_mutex|Mutex]]), [[224_semaphore|세마포어]]([[224_semaphore|Semaphore]]), 그리고 락프리([[256_lock_free_data_structures|Lock-free]]) 자료구조를 지탱하는 가장 밑바닥의 절대적 인프라다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **[[193_atomicity_all_or_nothing|원자성]] ([[193_atomicity_all_or_nothing|Atomicity]])**: 더 이상 쪼갤 수 없는 성질. 실행 도중 [[016_interrupt_mechanism|인터럽트]]에 의해 중단되지 않으며, 완전히 실행되거나 아예 실행되지 않거나 둘 중 하나만 존재하는 특성.
  - **Test-and-Set (TAS)**: 메모리 주소를 읽어 원래 있던 값을 반환함과 동시에, 그 자리에 1(또는 참)을 덮어쓰는 하드웨어 원자적 [[158_instruction|명령어]].

- **필요성 (소프트웨어 [[212_synchronization_mechanisms|동기화]]의 한계와 붕괴)**: 
  - 초창기 학자들은 [[283_mutual_exclusion|상호 배제]]를 위해 데커(Dekker)의 [[001_algorithm_definition|알고리즘]]이나 피터슨(Peterson)의 [[001_algorithm_definition|알고리즘]] 같은 소프트웨어 [[369_logic_bomb|논리]]를 짰다.
  - 하지만 멀티코어가 등장하고, 컴파일러와 CPU가 성능을 높이려고 코드 실행 순서를 마음대로 섞어버리자([[158_instruction|Instruction]] Reordering), 이 완벽해 보이던 소프트웨어 락들이 다 깨져버렸다.
  - 게다가 `if (lock == 0)`을 [[396_validation|확인]]하고 `lock = 1`을 쓰려는 찰나에 [[211_context_switch|문맥 교환]]이 터지면 무조건 레이스 컨디션이 났다.
  - **해결책**: "소프트웨어로는 답이 없다! CPU를 만드는 인텔이나 AMD가 아예 읽고(Test) 쓰는(Set) 걸 하나의 기계어 덩어리로 만들어서 제공해라!"

  - **소프트웨어 락 (실패)**: 화장실 문을 열어보고(Test) 빈 것을 [[396_validation|확인]]했다. 들어가서 문을 잠그려(Set) 하는데, 내가 손잡이를 잡기 직전 0.1초 찰나에 누군가 밀치고 같이 들어와 버렸다.
  - **Test-and-Set (성공)**: 문을 열어보고 빈 것을 [[396_validation|확인]]하는 순간, 내 손과 문고리가 '원자적'으로 융합된다. 문을 열고 들어가서 잠글 때까지 시간이 말 그대로 '멈춰서' 아무도 끼어들 수 없는 마법의 손잡이를 다는 것이다.

- **발전 과정**:
  1. **소프트웨어 락**: [[016_interrupt_mechanism|인터럽트]] Disable이나 [[186_character_stuffing_dle_stx_etx|플래그]] 변수 조합 (한계 봉착).
  2. **Test-and-Set (TAS)**: 초창기 하드웨어 원자 연산. 1로 바꾸는 것만 가능.
  3. **[[415_compare_and_swap|Compare-and-Swap]] ([[768_cas_compare_and_swap_lock_free|CAS]])**: 현대 하드웨어의 표준. `CMPXCHG` [[158_instruction|명령어]]. 기존 값이 내가 예상한 값과 같을 때만 새 값으로 바꾸는 훨씬 진보된 원자 연산.

- **📢 섹션 요약 비유**: 소프트웨어의 말장난으로 도둑([[213_race_condition|경쟁 조건]])을 막는 데 지친 프로그래머들이, 아예 철물점(CPU 제조사)에 가서 절대로 끊어지지 않는 티타늄 사슬(TAS)을 주문 제작해 온 것입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Test-and-Set 연산의 C 언어적 표현 (내부 [[369_logic_bomb|논리]])

이 코드는 소프트웨어로 짠 것 같지만, 실제로는 **CPU가 내부적으로 한 번에 처리하는 하드웨어 동작**을 C언어로 풀어쓴 것뿐이다. 이 함수 전체가 한 덩어리(Atomic)로 실행된다.

```c
boolean TestAndSet(boolean *target) {
    boolean rv = *target;  // 1. 현재 자물쇠 상태(target)를 읽어서 rv에 저장 (Test)
    *target = true;        // 2. 자물쇠를 무조건 잠금 상태(true)로 덮어씀 (Set)
    return rv;             // 3. 방금 읽었던 예전 자물쇠 상태를 반환
}
```

### TAS를 이용한 [[222_spinlock|스핀락]]([[222_spinlock|Spinlock]]) 구현

위의 치트키 [[158_instruction|명령어]]를 사용하면 [[283_mutual_exclusion|상호 배제]]([[223_mutex|Mutex]]) 락 코드가 허무할 정도로 짧고 완벽해진다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 Test-And-Set 기반의 완벽한 상호 배제 아키텍처            │
  ├───────────────────────────────────────────────────────────────────┤
  │  [공유 변수: boolean lock = false (초기에는 문이 열려있음)]              │
  │                                                                   │
  │  [스레드 A 진입 시도]                                                │
  │   - while (TestAndSet(&lock)) { ... }                             │
  │   - TestAndSet이 lock을 읽음 -> false (열려있음!)                    │
  │   - TestAndSet이 즉시 lock = true로 덮어씀. (이제 잠김!)              │
  │   - false를 반환했으므로 while문을 뚫고 [임계 구역] 진입 성공!            │
  │                                                                   │
  │  [스레드 B 진입 시도 (A가 임계 구역에 있을 때)]                          │
  │   - while (TestAndSet(&lock)) { ... }                             │
  │   - TestAndSet이 lock을 읽음 -> true (A가 잠가둠!)                   │
  │   - TestAndSet이 lock을 true로 덮어씀. (어차피 true였으니 변화 없음)    │
  │   - true를 반환했으므로 B는 while문에 갇혀서 무한 뺑뺑이 (Spinning) 도는 중! │
  │                                                                   │
  │  [스레드 A 퇴출]                                                    │
  │   - lock = false; (A가 볼일 다 보고 문을 엶)                          │
  │   - 뺑뺑이 돌던 B가 드디어 false를 반환받고 임계 구역으로 들어감!             │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 핵심은 "이미 잠긴 문을 [[396_validation|확인]]하는 놈(B)이 다시 잠가도 어차피 잠긴 상태"라는 점이다. `TestAndSet`은 무조건 문을 잠가버리면서, **"방금 전까지 문이 열려있었나?"**를 나에게 알려준다. 오직 문이 열려있었다는 대답(false)을 들은 단 한 명의 [[092_thread_lwp|스레드]]만이 [[214_critical_section|임계 구역]]의 합법적인 주인이 되는 완벽한 하드웨어 로터리 시스템이다.

---

### 하드웨어 레벨의 [[344_bus|버스]] 잠금 ([[344_bus|Bus]] [[213_locking_mechanism_concurrency_control|Locking]])

멀티코어 환경에서 코어 1과 코어 2가 동시에 TAS 명령을 내리면 CPU는 이를 어떻게 원자적으로 처리할까?

- **[[344_bus|Bus]] [[510_lock|Lock]] (`LOCK` prefix)**: 구형 CPU는 TAS [[158_instruction|명령어]]가 실행되는 순간 메인보드의 메모리 [[344_bus|버스]]([[365_fsb|FSB]])에 전기적 잠금([[510_lock|Lock]]) 신호를 쏴서 다른 코어들이 아예 RAM에 접근하지 못하게 전파를 차단했다. 
- **Cache [[510_lock|Lock]] (현대 CPU)**: 메모리 [[344_bus|버스]]를 통째로 잠그면 시스템 전체가 마비되므로, 현대 CPU(MESI [[295_protocol_field_tcp_udp_icmp|프로토콜]])는 그 락 변수가 들어있는 **L1 캐시 라인(64바이트) 하나만 독점**하여 초고속으로 TAS 연산을 수행한다.

- **📢 섹션 요약 비유**: TAS는 총알입니다. 방아쇠를 당기면([[158_instruction|명령어]] 실행) 공이가 화약을 때리고 총알이 날아가는 과정이 중간에 멈출 수 없이 한 번에 일어납니다. 소프트웨어 락이 장전부터 격발까지 일일이 수동으로 하느라 오발 사고가 난다면, TAS는 완벽한 일체형 권총입니다.

---

## Ⅲ. 비교 및 연결

### TAS vs [[768_cas_compare_and_swap_lock_free|CAS]] ([[415_compare_and_swap|Compare-And-Swap]])의 진화

TAS는 무조건 값을 1(True)로 바꾸기 때문에 단순한 락(잠금/해제) 용도로만 쓸 수 있었다. 이를 숫자를 더하고 빼는 범용 [[001_dikw_pyramid|데이터]] 조작으로 진화시킨 것이 CAS다.

| 비교 항목 | Test-And-Set (TAS) | [[415_compare_and_swap|Compare-And-Swap]] ([[768_cas_compare_and_swap_lock_free|CAS]]) |
|:---|:---|:---|
| **동작 방식** | 현재 값을 읽고, **무조건** 1(True)로 덮어씀 | 현재 값이 **내가 기대한 값과 같을 때만** 새 값으로 덮어씀 |
| **[[158_instruction|명령어]] (x86)**| `TSL` 또는 `XCHG` | `CMPXCHG` |
| **주 사용처** | [[223_mutex|Mutex]], Spinlock의 뼈대 구현 | **[[256_lock_free_data_structures|Lock-Free]] 자료구조**, `AtomicInteger` 구현 |
| **특징** | 락([[510_lock|Lock]])을 만들기 위한 도구 | 락([[510_lock|Lock]]) 자체를 없애기 위한(회피하기 위한) 도구 |

### 과목 융합 관점

- **자료구조 ([[001_dikw_pyramid|Data]] Structure)**: 연결 리스트나 스택에 멀티스레드로 노드를 추가할 때, TAS로 락을 걸고 추가하면 병목이 터진다. 최상급 개발자는 [[768_cas_compare_and_swap_lock_free|CAS]] [[158_instruction|명령어]]를 루프문(`while`)으로 감싸서 락 없이 노드 포인터를 바꿔치기하는 **락 프리([[256_lock_free_data_structures|Lock-Free]])** 스택을 구현하여 병목을 없앤다.
- **클라우드 / [[136_variance|분산]] 시스템**: TAS/CAS의 철학은 단일 CPU를 넘어 [[136_variance|분산]] 시스템으로 확장되었다. [[542_redis|Redis]] 서버에서 키를 쓸 때 사용하는 `SETNX (Set if Not eXists)` [[158_instruction|명령어]]는, [[136_variance|분산]] 환경의 여러 마이크로서비스들이 레디스에 접근할 때 레이스 컨디션을 막아주는 완벽한 "[[136_variance|분산]]형 TAS" [[158_instruction|명령어]]다.

- **📢 섹션 요약 비유**: TAS가 화장실 문이 비어있는지 [[396_validation|확인]]하고 무조건 잠가버리는 '자물쇠'라면, CAS는 "내 통장 잔고가 정확히 [[489_raid_10_hybrid|10]],000원일 때만 15,000원으로 덮어써라"라고 지시하는 매우 정교한 스마트 계약서입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — Java의 `synchronized` 병목을 `AtomicInteger`로 회피**: 조회수를 늘리는 서버 코드에서 `public synchronized void increment()`를 썼더니 CPU 코어 16개 중 1개만 일하고 15개는 락 대기에 빠져 서버가 뻗음.
   - **원인 분석**: `synchronized`는 내부적으로 OS의 무거운 [[699_mutex_lock_sleep_wait|뮤텍스 락]](TAS 기반)을 부른다. 조회수를 1 올리는 가벼운 작업에 락을 걸면 [[092_thread_lwp|스레드]]가 [[022_kernel_role|커널]] 모드로 진입하고 대기(Sleep) 상태로 빠지는 [[211_context_switch|문맥 교환]] 오버헤드가 더 크다.
   - **아키텍처 적용**: `synchronized` 블록을 지워버리고, 변수를 `AtomicInteger`로 교체한 뒤 `.incrementAndGet()`을 호출한다. 이 메서드는 JVM 내부의 `Unsafe.compareAndSwapInt`를 호출하여 OS [[022_kernel_role|커널]]의 락(Sleep) 도움 없이, CPU 하드웨어의 [[768_cas_compare_and_swap_lock_free|CAS]] [[158_instruction|명령어]]로 직접 조회수를 올린다(User-space [[256_lock_free_data_structures|Lock-free]]). 성능이 수십 배 향상된다.

2. **시나리오 — [[222_spinlock|스핀락]]([[222_spinlock|Spinlock]])의 한계와 ABA 문제**: 하드웨어 [[768_cas_compare_and_swap_lock_free|CAS]] 연산으로 락프리 큐를 짰다. A [[092_thread_lwp|스레드]]가 큐의 머리(Head)가 '노드 1'인 것을 [[396_validation|확인]]하고 '노드 2'로 바꾸려는 찰나 CPU를 뺏겼다. 그사이 B [[092_thread_lwp|스레드]]가 노드 1을 빼고 새로운 노드를 넣었는데, 우연히 그 새 노드의 메모리 주소가 다시 '노드 1'과 같아졌다(메모리 재활용).
   - **원인 분석**: 다시 깨어난 A [[092_thread_lwp|스레드]]가 큐의 머리를 보니 여전히 '노드 1'이다. [[768_cas_compare_and_swap_lock_free|CAS]] 연산은 "주소가 같네? 문제없군!" 하고 통과해 버렸다. 하지만 사실 그 노드 1은 아까의 노드 1이 아니라 완전히 다른 [[001_dikw_pyramid|데이터]]가 들어있는 껍데기만 같은 노드였다. 이것이 하드웨어 [[768_cas_compare_and_swap_lock_free|CAS]] 연산의 치명적 결함인 **ABA 문제**다. (A -> B -> 다시 A로 돌아왔을 때 변화를 눈치채지 못함)
   - **대응 (기술사적 가이드)**: 이 문제를 막기 위해 하드웨어 아키텍트는 [[768_cas_compare_and_swap_lock_free|CAS]] 연산에 주소뿐만 아니라 **[[288_version_ihl_tos_total_length|버전]] 관리 번호(Stamp)**를 같이 묶어서 비교하게 만들었다(Double-word [[768_cas_compare_and_swap_lock_free|CAS]]). 자바의 `AtomicStampedReference` 클래스가 바로 이 ABA 문제를 하드웨어적으로 막아주는 전용 방패다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 동시성 제어 인프라(락 vs 락프리) 결정 플로우              │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [멀티스레드 환경에서 공유 변수 조작 로직을 작성해야 함]                    │
  │                │                                                  │
  │                ▼                                                  │
  │      공유 변수를 조작하는 임계 구역이 긴가? (I/O, 파일 쓰기, 긴 루프 포함)      │
  │          ├─ 예 ─────▶ [OS 뮤텍스(Mutex/Semaphore) 사용 필수]          │
  │          │            (TAS 기반의 락으로, 락 획득 실패 시 스레드를 재워버림)  │
  │          └─ 아니오 (단순히 숫자 1을 더하거나 노드 포인터 하나만 바꿈)           │
  │                │                                                  │
  │                ▼                                                  │
  │      스레드 간의 락 경합(Contention)이 매우 심한가? (초당 수십만 번 호출)     │
  │          ├─ 예 ─────▶ [CAS 하드웨어 명령어 기반의 Lock-Free 자료구조 도입]│
  │          │            (Atomic 클래스 사용. 스레드가 자지 않고 무한 재시도)   │
  │          │                                                        │
  │          └─ 아니오 ──▶ 단순 Spinlock (순수 TAS 명령어 루프) 사용 가부 판단 │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** "락 프리([[256_lock_free_data_structures|Lock-free]])가 무조건 제일 빠르다"는 것은 주니어의 환상이다. [[092_thread_lwp|스레드]] 1,000개가 동시에 [[768_cas_compare_and_swap_lock_free|CAS]](Atomic) 연산을 시도하면, 1개만 성공하고 999개는 실패하여 `while` 문을 다시 돈다(CPU 100% 점유율). 차라리 OS 뮤텍스를 써서 999개를 쿨하게 재워버리는(Sleep) 것이 전체 시스템 성능에 훨씬 좋을 때가 많다. 아키텍트는 락이 물려있는 '시간(Duration)'을 정확히 계산해 무기를 골라야 한다.

### 도입 [[435_checklist_based_testing|체크리스트]]
- **[[416_memory_barrier|메모리 배리어]] ([[416_memory_barrier|Memory Barrier]] / Fence)**: 멀티코어 환경에서 TAS나 CAS를 쓸 때, 컴파일러나 CPU가 코드를 맘대로 섞어버리면 최악의 레이스 컨디션이 터진다. [[413_hardware_synchronization|하드웨어 동기화]] [[158_instruction|명령어]] 앞뒤로 `mfence`나 `volatile` 키워드를 박아 넣어 "이 변수 읽기/[[289_cqrs_db|쓰기]] 순서는 절대 바꾸지 마라"고 하드웨어를 통제했는가?

- **📢 섹션 요약 비유**: TAS와 [[768_cas_compare_and_swap_lock_free|CAS]] 연산은 외과 수술용 레이저 메스입니다. 아주 얇고 정교하게 썩은 부위([[014_concurrency|동시성]] 에러)만 도려낼 수 있지만, 자칫 헛방(ABA 문제, 무한 경합)을 치면 환자(CPU)의 체력을 바닥나게 만듭니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 소프트웨어 [[212_synchronization_mechanisms|동기화]] (Peterson 등) | 하드웨어 TAS / [[768_cas_compare_and_swap_lock_free|CAS]] [[158_instruction|명령어]] 도입 | 개선 효과 |
|:---|:---|:---|:---|
| **정성 ([[003_integrity|무결성]])** | CPU 파이프라인 최적화에 의해 박살 남 | 하드웨어 [[344_bus|버스]]/캐시 락으로 완벽한 보장 | Memory Reordering에 안전한 시스템 구축 |
| **정량 (속도)** | 복잡한 [[186_character_stuffing_dle_stx_etx|플래그]] 연산 수십 클럭 소모 | 단일 기계어로 수 클럭 내 처리 | [[214_critical_section|임계 구역]] 진입 오버헤드 90% 소멸 |
| **정성 (확장성)** | 2개 프로세스 간 [[212_synchronization_mechanisms|동기화]] 한정 | N개의 멀티코어 프로세스 통제 가능 | 현대 OS 스케줄링 및 멀티스레드 생태계 완성 |

### 미래 전망
- **인텔 TSX ([[269_htm_intel_tsx|하드웨어 트랜잭셔널 메모리]])**: TAS나 CAS로 변수 1개를 락 없이 바꾸는 건 되는데, 변수 2개를 락 없이 동시에 바꿀 수는 없다(하드웨어의 한계). 이를 극복하기 위해 인텔은 아예 여러 개의 변수 수정 작업을 L1 캐시에 임시로 담아두고, 충돌이 없으면 한 번에 메모리에 반영(Commit)해 버리는 거대한 하드웨어 원자 연산 묶음([[513_htm|HTM]])을 도입하여 [[014_concurrency|동시성]] 제어의 패러다임을 소프트웨어에서 하드웨어로 완전히 떠넘기고 있다.

### 결론
Test-and-Set(TAS) 연산은 컴퓨터 구조가 소프트웨어의 한계를 구원하기 위해 내려준 데우스 엑스 마키나(Deus ex machina)다. [[369_logic_bomb|논리]]만으로는 해결할 수 없었던 수만 갈래의 [[675_multitasking_terminology_preemptive|멀티태스킹]] 난제를, 칩셋 내부의 '[[344_bus|버스]] 잠금'이라는 압도적인 물리력으로 평정해 버렸다. 오늘날 우리가 자바에서 쓰는 `synchronized`, 리눅스의 [[022_kernel_role|커널]] 락, DB의 [[014_concurrency|동시성]] 제어까지 모든 안전한 코드는 이 1바이트짜리 하드웨어 [[158_instruction|명령어]]의 어깨 위에 서 있다. 결국 시스템 소프트웨어의 궁극적인 최적화는 하드웨어 실리콘과 어떻게 대화하느냐에 달려 있음을 이 [[158_instruction|명령어]]가 증명하고 있다.

- **📢 섹션 요약 비유**: 복잡한 철학적 논쟁(소프트웨어 락)으로 문을 열지 말지 싸우던 사람들에게, CPU 제조사가 아주 크고 무식한 강철 빗장(TAS)을 던져주며 "그냥 이거 걸고 잠가라. 절대 안 뚫린다"라고 문제를 일축해 버린 하드웨어 공학의 승리입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[213_race_condition|경쟁 조건]] ([[213_race_condition|Race Condition]]) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[214_critical_section|임계 구역]] 3가지 요구조건 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[699_mutex_lock_sleep_wait|뮤텍스 락]] ([[699_mutex_lock_sleep_wait|Mutex Lock]]) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[700_spinlock_busy_waiting|스핀락 바쁜 대기]] ([[700_spinlock_busy_waiting|Busy Wait]]) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[임계 구역 3가지 요구조건]
    │
    ▼
[Test-and-Set 연산 하드웨어 (Test And Set Hardware Atomic)]
    │
    ├──▶ [뮤텍스 락 (Mutex Lock)]
    └──▶ [스핀락 바쁜 대기 (Busy Wait)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 게임방 문이 잠겼는지 [[396_validation|확인]]하고(Test), 열려있으면 팻말을 '사용 중'으로 뒤집고(Set) 들어가는 규칙이 있어요.
2. 소프트웨어로 하면 "문이 열려있네?" [[396_validation|확인]]하고 팻말을 뒤집으려는 순간, 0.1초 만에 얌체 친구가 쏙 들어가서 문을 잠가버려요! (레이스 컨디션)
3. 'Test-and-Set 하드웨어'는 마법의 손잡이에요! 문이 열린 걸 [[396_validation|확인]]하는 순간, 내 손과 문고리가 찰싹 붙어서 내가 문을 잠글 때까지 시간이 멈춰버려요. 아무도 새치기를 할 수 없는 절대 방어막이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 698 / 800

← **이전**: [[697_critical_section_three_requirements|697. 임계 구역 3가지 요구조건 (Critical Section Three Requirements)]]
**다음**: [[699_mutex_lock_sleep_wait|699. 뮤텍스 락 (Mutex Lock)]] →

---
