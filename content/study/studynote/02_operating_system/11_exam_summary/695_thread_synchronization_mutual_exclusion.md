+++
weight = 695
title = "695. 스레드 동기화 상호 배제 (Thread Synchronization Mutual Exclusion)"
date = "2026-05-09"
[extra]
categories = "studynote-operating-system"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[092_thread_lwp|스레드]] [[212_synchronization_mechanisms|동기화]]([[092_thread_lwp|Thread]] [[212_synchronization_mechanisms|Synchronization]])의 가장 기본이 되는 **[[283_mutual_exclusion|상호 배제]]([[283_mutual_exclusion|Mutual Exclusion]])**란, 여러 [[092_thread_lwp|스레드]]가 동시에 공유 자원(변수, [[501_file_definition_logical_record|파일]])을 건드릴 때 [[001_dikw_pyramid|데이터]]가 깨지는 것을 막기 위해 "한 번에 하나의 [[092_thread_lwp|스레드]]만 접근할 수 있도록" 물리적/논리적으로 벽을 치는 행위다.
> 2. **해결의 딜레마**: [[283_mutual_exclusion|상호 배제]]를 달성하려면 락([[510_lock|Lock]])을 걸어야 하는데, 락을 걸면 필연적으로 멀티스레드의 존재 이유인 '병렬성(Parallelism)'이 훼손되어 시스템이 직렬화(Serialization)되고 [[282_performance_tactics|성능]]이 급락한다.
> 3. **가치**: 따라서 우수한 아키텍처는 [[283_mutual_exclusion|상호 배제]]를 포기하는 것이 아니라, **[[214_critical_section|임계 구역]]([[214_critical_section|Critical Section]])의 크기를 머리카락 굵기만큼 얇게 깎아내거나**, 아예 락을 쓰지 않는 락 프리([[256_lock_free_data_structures|Lock-free]]) 자료구조로 우회하여 "안전함과 속도"라는 두 마리 토끼를 잡는 데 그 목적이 있다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **[[092_thread_lwp|스레드]] [[212_synchronization_mechanisms|동기화]] ([[092_thread_lwp|Thread]] [[212_synchronization_mechanisms|Synchronization]])**: 다수의 [[092_thread_lwp|스레드]]가 협력하여 일할 때, 서로의 작업 순서를 맞추거나 공유 [[001_dikw_pyramid|데이터]]의 파괴를 막기 위해 조율하는 모든 기법.
  - **[[283_mutual_exclusion|상호 배제]] ([[283_mutual_exclusion|Mutual Exclusion]], [[223_mutex|Mutex]])**: [[212_synchronization_mechanisms|동기화]]의 부분집합으로, "내가 화장실에 들어가 있으면([[214_critical_section|임계 구역]]), 다른 누구도 화장실 문을 열고 들어올 수 없다"는 독점적 접근 보장 원칙.

- **필요성 (멀티스레딩의 치명적 부작용)**: 
  - 멀티스레드의 장점은 메모리([[001_dikw_pyramid|Data]], [[078_heap_datastructure|Heap]] 영역)를 공유한다는 점이다. 
  - 하지만 [[092_thread_lwp|스레드]] A가 통장 잔고(1만 원)를 읽어서 5,000원을 더하려는 찰나(연산 중), [[092_thread_lwp|스레드]] B가 동시에 잔고(1만 원)를 읽어서 3,000원을 빼버리고 저장했다 치자. A가 연산을 끝내고 15,000원을 덮어써 버리면 B가 출금한 기록은 영원히 허공으로 증발한다 ([[203_lost_update_concurrency_problem|Lost Update]]).
  - **해결책**: "통장 잔고를 읽고 쓰는 그 찰나의 시간([[214_critical_section|임계 구역]])에는, OS가 보증하는 강철 자물쇠([[223_mutex|Mutex]])를 채워 다른 [[092_thread_lwp|스레드]]가 꼼짝없이 밖에서 기다리게 만들자!"

  - **[[283_mutual_exclusion|상호 배제]] 없음**: 10명의 직원이 1권의 회의록에 동시에 펜을 들고 글을 쓴다. 서로의 글씨가 겹쳐서 무슨 말인지 아무도 알아볼 수 없게 된다 ([[001_dikw_pyramid|데이터]] 오염).
  - **[[283_mutual_exclusion|상호 배제]] 적용**: 회의록 옆에 '말하기 지휘봉([[510_lock|Lock]])'을 딱 하나 둔다. 지휘봉을 쥔 사람만 회의록에 글을 쓸 수 있고, 다른 사람들은 지휘봉을 넘겨받을 때까지 펜을 내려놓고 무조건 기다려야 한다. 글씨는 완벽하게 적히지만(안전), 회의 시간은 엄청나게 길어진다([[282_performance_tactics|성능]] 저하).

- **발전 과정**:
  1. **소프트웨어적 해결**: 피터슨(Peterson)의 [[001_algorithm_definition|알고리즘]]. [[186_character_stuffing_dle_stx_etx|플래그]]([[186_character_stuffing_dle_stx_etx|Flag]]) 변수 2개를 썼지만, 현대 CPU의 비순차적 실행 때문에 무용지물이 됨.
  2. **하드웨어 지원 (Test-And-Set)**: CPU 칩셋이 아예 메모리 읽기와 쓰기를 한 번에 원자적(Atomic)으로 묶어주는 [[158_instruction|명령어]]를 제공하여 [[283_mutual_exclusion|상호 배제]] 완벽 구현.
  3. **OS 레벨 [[212_synchronization_mechanisms|동기화]]**: 위 하드웨어 [[158_instruction|명령어]]를 기반으로 OS가 뮤텍스, [[224_semaphore|세마포어]], [[229_monitor|모니터]] 같은 사용하기 편한 API를 개발자에게 제공.

- **📢 섹션 요약 비유**: 도로에 신호등([[283_mutual_exclusion|상호 배제]])이 없으면 차들이 엉켜서 대형 사고([[001_dikw_pyramid|데이터]] 파괴)가 납니다. 하지만 신호등을 너무 촘촘하게 세우면 차들이 계속 멈춰야 해서 고속도로(멀티코어)의 의미가 사라집니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[283_mutual_exclusion|상호 배제]]의 실패: [[014_concurrency|동시성]] 버그 ([[213_race_condition|Race Condition]])

가장 단순한 `count++` 코드가 어셈블리(기계어) 레벨에서 어떻게 파괴되는지 본다. `count++`는 1줄짜리 C 코드지만, CPU 내부에서는 **3줄의 기계어(Read $\rightarrow$ Modify $\rightarrow$ Write)**로 나뉘어 실행된다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 상호 배제가 없을 때의 'Lost Update' 시나리오           │
  ├───────────────────────────────────────────────────────────────────┤
  │  [상황: 공유 변수 Count = 5]                                         │
  │                                                                   │
  │     [ Thread A (Count++) ]            [ Thread B (Count--) ]      │
  │                                                                   │
  │  1. 메모리에서 5를 레지스터로 읽음 (R1=5)                               │
  │  2. 레지스터 값에 1을 더함 (R1=6)                                     │
  │  ========= ⚡ (Context Switch! A 멈춤, B 시작) ⚡ ================│
  │                                                                   │
  │                                     3. 메모리에서 5를 레지스터로 읽음 (R2=5)│
  │                                     4. 레지스터 값에 1을 뺌 (R2=4)     │
  │                                     5. 메모리에 4를 덮어씀 (Count=4)   │
  │  ========= ⚡ (Context Switch! B 멈춤, A 재개) ⚡ ================│
  │                                                                   │
  │  6. 아까 계산해 둔 6을 메모리에 덮어씀 (Count=6)                        │
  │                                                                   │
  │  ★ 최종 결과: Count는 5여야 정상인데, B의 -1 연산이 완전히 씹히고 6이 됨.  │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** [[283_mutual_exclusion|상호 배제]]의 본질은 저 3줄의 어셈블리 [[158_instruction|명령어]] 묶음(Read-Modify-Write)이 실행되는 중간에, **"절대 어떤 [[092_thread_lwp|스레드]]도 끼어들지 못하게(Atomic, 불가분성) 하나의 덩어리로 묶어버리는 것"**이다. 그 묶인 공간을 우리는 [[214_critical_section|임계 구역]]([[214_critical_section|Critical Section]])이라 부르며, [[283_mutual_exclusion|상호 배제]]는 [[214_critical_section|임계 구역]]의 입구를 막는 자물쇠다.

---

### [[283_mutual_exclusion|상호 배제]]([[283_mutual_exclusion|Mutual Exclusion]])의 동작 아키텍처

락([[510_lock|Lock]])을 획득하고 반납하는 과정이다.

1. **[[510_lock|Lock]] 획득 (Acquire / [[510_lock|Lock]])**:
   - [[092_thread_lwp|스레드]] A가 [[214_critical_section|임계 구역]]에 들어가기 전 락을 요청한다.
   - 락이 열려있으면 잠그고 들어간다.
   - 만약 [[092_thread_lwp|스레드]] B가 이미 락을 쥐고 있다면? [[092_thread_lwp|스레드]] A는 락이 풀릴 때까지 제자리를 맴돌거나([[222_spinlock|Spinlock]], Busy-waiting), 아예 OS 스케줄러에 의해 강제 수면(Sleep/Block) 상태에 빠져 CPU를 양보한다([[223_mutex|Mutex]]/[[224_semaphore|Semaphore]]).
2. **[[214_critical_section|임계 구역]] ([[214_critical_section|Critical Section]])**:
   - [[092_thread_lwp|스레드]] A 혼자서 우아하게 공유 변수(`count`)를 수정한다. 절대 방해받지 않는다.
3. **[[510_lock|Lock]] 반환 (Release / Unlock)**:
   - A가 수정을 마치고 락을 푼다.
   - 자고 있던 [[092_thread_lwp|스레드]] B를 커널이 깨워주고(Wake-up), 이제 B가 락을 쥐고 들어간다.

- **📢 섹션 요약 비유**: [[283_mutual_exclusion|상호 배제]]는 기차 화장실과 같습니다. 내가 안에 들어가서 문을 잠그면([[510_lock|Lock]]), 밖에 있는 100명의 승객은 내가 볼일을 다 보고 문을 열고(Unlock) 나올 때까지 오직 밖에서 덜덜 떨며 기다려야만 합니다.

---

## Ⅲ. 비교 및 연결

### [[283_mutual_exclusion|상호 배제]]([[283_mutual_exclusion|Mutual Exclusion]]) vs [[281_deadlock_definition|교착 상태]]([[281_deadlock_definition|Deadlock]])의 [[083_relationship_in_er_model|관계]]

[[283_mutual_exclusion|상호 배제]]는 안전을 위한 필수 조건이지만, 이것이 '[[281_deadlock_definition|교착 상태]](데드락)'라는 악마를 낳는 가장 큰 원흉이다.

| 특징 | [[283_mutual_exclusion|상호 배제]] ([[283_mutual_exclusion|Mutual Exclusion]]) | [[281_deadlock_definition|교착 상태]] ([[281_deadlock_definition|Deadlock]]) |
|:---|:---|:---|
| **본질** | 공유 자원을 보호하기 위한 의도적인 '잠금' 기법 | 락이 꼬여서 [[092_thread_lwp|스레드]]들이 서로를 무한히 기다리는 '장애' |
| **인과 [[083_relationship_in_er_model|관계]]** | [[283_mutual_exclusion|상호 배제]]가 없으면 데드락은 절대 안 생김 | 데드락 성립의 4대 필수 조건 중 첫 번째가 '[[283_mutual_exclusion|상호 배제]]'임 |
| **목표** | [[001_dikw_pyramid|데이터]] 정합성([[003_integrity|Integrity]]) 100% 보장 | 발생을 막거나(Prevention), 회피(Avoidance)해야 함 |

### 과목 융합 관점

- **자료구조 ([[001_dikw_pyramid|Data]] Structure)**: [[056_linked_list|연결 리스트]]([[056_linked_list|Linked List]])에 노드를 추가할 때, [[283_mutual_exclusion|상호 배제]]를 위해 리스트 전체에 락을 거는 것을 `Coarse-grained Lock(통 락)`이라 한다. 반면 내가 건드리는 노드와 그다음 노드 단 2개에만 락을 거는 것을 `Fine-grained Lock(미세 락)`이라 한다. 자료구조 아키텍처에서 [[282_performance_tactics|성능]]의 한계는 이 락의 범위를 얼마나 잘게 쪼개느냐에 달려 있다.
- **클라우드/[[136_variance|분산]] 시스템**: 하나의 서버 안에서는 [[092_thread_lwp|스레드]]끼리 OS가 제공하는 락([[223_mutex|Mutex]])을 쓰면 되지만, 서버가 10대([[136_variance|분산]] 환경)라면? OS 락은 통하지 않는다. 이때는 Redis나 [[798_distributed_lock_zookeeper_consensus|ZooKeeper]] 같은 외부 저장소를 이용해 네트워크 너머로 [[283_mutual_exclusion|상호 배제]]를 획득하는 **[[136_variance|분산]] 락(Distributed [[510_lock|Lock]])** 아키텍처로 진화하게 된다.

- **📢 섹션 요약 비유**: 문을 잠그는 기술([[283_mutual_exclusion|상호 배제]])은 도둑을 막는 최고의 방법입니다. 하지만 내가 방 안에서 문을 잠갔는데 열쇠를 잃어버리고 밖의 사람도 못 들어오는 상황이 데드락입니다. 보안이 강력할수록 갇혀 죽을 위험도 커지는 법입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — 티켓 예매 시스템의 초과 예매(Overbooking) 사태**: 아이돌 콘서트 티켓 100장을 오픈했다. 수만 명이 동시에 "예매" 버튼을 눌렀는데, DB에 남은 티켓이 0장인데도 105명에게 "예매 성공"이 떨어짐.
   - **원인 분석**: 전형적인 [[283_mutual_exclusion|상호 배제]] 실패([[213_race_condition|Race Condition]])다. 티켓이 1장 남았을 때, [[092_thread_lwp|스레드]] 5개가 동시에 `if (ticket > 0)` 코드를 통과해버렸다. 그리고 5명 모두 `ticket--`를 실행해 버린 것이다.
   - **아키텍처 적용 ([[283_mutual_exclusion|상호 배제]] 강제)**: 
     - 1) 애플리케이션 레벨: Java의 `synchronized` 블록이나 `ReentrantLock`을 사용하여 티켓 차감 로직([[214_critical_section|Critical Section]])을 단 1명의 [[092_thread_lwp|스레드]]만 진입하도록 강제 직렬화시킨다.
     - 2) DB 레벨 (더 흔함): DB 쿼리를 쏠 때 `SELECT ... FOR UPDATE` 구문을 사용하여 DB의 레코드(Row) 자체에 배타적 락(X-[[510_lock|Lock]])을 걸어 [[283_mutual_exclusion|상호 배제]]를 달성한다. (티켓 초과 예매 완벽 차단)

2. **시나리오 — 무분별한 `synchronized` 남용으로 인한 시스템 [[139_throughput|처리량]](TPS) 폭락**: [[283_mutual_exclusion|상호 배제]]의 중요성을 배운 주니어 개발자가 "안전한 게 최고야!"라며 [[090_service_kubernetes_network_load_balancing|서비스]] 로직의 핵심 함수 전체(I/O, 네트워크 대기 포함)에 자바의 `synchronized`를 걸어버림.
   - **원인 분석**: 1만 명의 접속자가 와도, 그 핵심 함수 안에는 한 번에 1명의 [[092_thread_lwp|스레드]]만 들어갈 수 있다. 나머지 9,999명은 톰캣 [[092_thread_lwp|스레드]] 풀에서 락을 기다리며 대기(Block) 상태로 빠져 서버 CPU는 5%인데 응답은 10초가 넘어가는 극심한 병목([[275_lock_contention_monitoring|Lock Contention]])이 터졌다.
   - **대응 (기술사적 가이드)**: [[283_mutual_exclusion|상호 배제]]의 제1원칙은 **"[[214_critical_section|임계 구역]]([[214_critical_section|Critical Section]])을 머리카락처럼 얇게 깎아라"**다. 함수 전체에 락을 걸지 말고, DB 통신이나 복잡한 계산은 락 밖에서 다 끝낸 뒤, 마지막에 전역 변수에 값을 덮어쓰는 그 단 한 줄의 코드(`count = result`)에만 락을 걸어 락 점유 시간을 나노초 단위로 줄여야 한다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 멀티스레드 동기화(상호 배제) 설계 최적화 플로우          │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [전역 변수나 공유 자료구조를 변경해야 하는 비즈니스 로직 작성]                 │
  │                │                                                  │
  │                ▼                                                  │
  │      그 변수를 '읽기'만 하는 스레드가 압도적으로 많고 '쓰기'는 가끔 일어나는가?│
  │          ├─ 예 ─────▶ [Reader-Writer Lock 도입]                   │
  │          │            (읽는 놈들끼리는 상호 배제를 풀어서 동시 접근 허용,     │
  │          │             쓸 때만 상호 배제를 거는 성능 극대화 락)           │
  │          └─ 아니오                                                │
  │                │                                                  │
  │                ▼                                                  │
  │      공유 변수가 단순한 숫자 카운터(`count++`)나 불리언 플래그인가?           │
  │          ├─ 예 ─────▶ [상호 배제(Mutex) 락 아예 사용 금지]            │
  │          │            대책: CPU가 제공하는 [Atomic 연산 (CAS)]을 사용하여 │
  │          │                  락 없이(Lock-free) 하드웨어적으로 원자성 보장  │
  │          │                                                        │
  │          └─ 아니오 ──▶ [Mutex / Spinlock] 등 전통적인 상호 배제 적용   │
  │                         (단, 임계 구역 내에서 절대 Sleep, I/O 금지)      │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** [[283_mutual_exclusion|상호 배제]]는 만병통치약이 아니라 최후의 수단이다. 최고 수준의 아키텍트는 락([[510_lock|Lock]])을 잘 쓰는 사람이 아니라, 아예 락을 쓸 상황을 만들지 않는 사람이다. 변수를 [[092_thread_lwp|스레드]]별로 쪼개거나([[694_thread_local_storage_tls|TLS]]), 읽기 전용으로 설계하거나([[298_immutable|Immutable]]), 락프리 [[001_algorithm_definition|알고리즘]]을 도입하여 [[283_mutual_exclusion|상호 배제]]에 따르는 '직렬화의 저주'를 피해 가는 것이 백엔드 튜닝의 핵심이다.

### 도입 [[435_checklist_based_testing|체크리스트]]
- **[[317_lockdep_lock_ordering|Lock Ordering]] (락 순서)**: [[283_mutual_exclusion|상호 배제]]를 위해 락 A와 락 B를 동시에 쥐어야 하는 로직이 있다면, 모든 [[092_thread_lwp|스레드]]가 무조건 "A를 먼저 쥐고 B를 쥔다"는 순서 규칙을 확립했는가? (한 놈은 A->B, 한 놈은 B->A로 쥐면 100% 데드락이 터진다.)

- **📢 섹션 요약 비유**: 100명이 1개의 화장실([[214_critical_section|임계 구역]])을 써야 할 때, 제일 멍청한 짓은 화장실 안에서 양치하고 머리까지 감는 것(락 안에서 무거운 연산)입니다. 밖에서 양치와 세수를 다 끝내고, 화장실에 들어가서는 오직 '볼일'만 보고 10초 만에 나오는 것이 [[283_mutual_exclusion|상호 배제]] 설계의 정수입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [[283_mutual_exclusion|상호 배제]] 미적용 ([[213_race_condition|Race Condition]]) | [[283_mutual_exclusion|상호 배제]] 적용 ([[223_mutex|Mutex]] 등) | 개선 효과 |
|:---|:---|:---|:---|
| **정성 ([[003_integrity|무결성]])** | 재현 불가능한 간헐적 [[001_dikw_pyramid|데이터]] 파괴 | **[[001_dikw_pyramid|데이터]]의 완벽한 ACID 정합성 보장** | 치명적인 비즈니스 오류(결제, 예매) 원천 차단 |
| **정량 (병렬성)** | 코어가 많을수록 [[282_performance_tactics|성능]] 오름 ([[001_dikw_pyramid|데이터]]는 깨짐) | 코어 많아져도 락([[510_lock|Lock]]) 지점에선 1열 종대 | [[282_performance_tactics|성능]]의 암묵적 상한선(Amdahl's Law) 발생 |
| **정성 (디버깅)** | 우연한 타이밍에 터져서 원인 찾기 극악 | 논리적 순서가 강제되어 동작 예측 가능 | 시스템의 결정론적(Deterministic) 행동 보장 |

### 미래 전망
- **[[269_htm_intel_tsx|하드웨어 트랜잭셔널 메모리]] ([[513_htm|HTM]])**: "[[283_mutual_exclusion|상호 배제]]를 걸면 너무 느려진다"는 한계를 부수기 위해 인텔(TSX) 등은 하드웨어 캐시를 이용해 락 없이 여러 [[092_thread_lwp|스레드]]를 일단 동시에 실행(낙관적 실행)시킨 뒤, 충돌이 났을 때만 하드웨어가 [[098_rollback_strategy_pipeline_error_threshold|롤백]]([[313_rollback|Rollback]])시켜주는 [[513_htm|HTM]] 기술을 도입했다. 소프트웨어 락의 시대를 하드웨어가 끝내려는 위대한 시도다.
- **Actor 모델 ([[1004_erlang_traffic_load_unit_calculation|Erlang]], Swift)**: 최신 프로그래밍 언어(Swift의 Actor 등)는 아예 "변수 공유" 자체를 언어 차원에서 금지해 버렸다. [[092_thread_lwp|스레드]]끼리 [[001_dikw_pyramid|데이터]]를 공유([[283_mutual_exclusion|상호 배제]])하는 대신, 캡슐화된 상태를 유지하며 "메시지"만 주고받는([[119_message_passing|Message Passing]]) Actor 모델이 차세대 [[014_concurrency|동시성]] 프로그래밍의 표준으로 자리 잡고 있다.

### 결론
[[092_thread_lwp|스레드]] [[212_synchronization_mechanisms|동기화]]와 [[283_mutual_exclusion|상호 배제]]([[283_mutual_exclusion|Mutual Exclusion]])는, 멀티코어가 선사한 "무한한 병렬성"이라는 달콤한 축복 뒤에 숨겨진 "[[001_dikw_pyramid|데이터]] 오염"이라는 저주를 막아내는 운영체제의 최후 방어선이다. 이 자물쇠([[510_lock|Lock]]) 덕분에 우리는 은행 잔고가 뒤섞이거나 미사일 궤도가 엉키는 대참사를 면할 수 있었다. 하지만 무분별한 [[283_mutual_exclusion|상호 배제]]는 시스템의 숨통을 조여 단일 코어보다 못한 속도를 내게 만든다. 락을 어디에, 얼마나 짧게, 어떤 방식으로 걸 것인가에 대한 고민은 시스템 아키텍트가 평생 짊어져야 할 십자가이자 가장 우아한 예술의 영역이다.

- **📢 섹션 요약 비유**: 자유(멀티스레드)는 무한한 힘을 주지만 질서([[283_mutual_exclusion|상호 배제]])가 없으면 자멸합니다. 완벽한 도시는 자유를 빼앗는 감옥이 아니라, 가장 좁은 골목([[214_critical_section|임계 구역]])에만 완벽한 신호등을 세워 아무도 다치지 않고 쌩쌩 달리게 만드는 곳입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[693_multithread_user_mode_kernel_mode|멀티스레드 유저모드 커널모드]] | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[694_thread_local_storage_tls|스레드 로컬 스토리지]] ([[694_thread_local_storage_tls|TLS]]) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[213_race_condition|경쟁 조건]] ([[213_race_condition|Race Condition]]) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[214_critical_section|임계 구역]] 3가지 요구조건 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[스레드 로컬 스토리지 (TLS)]
    │
    ▼
[스레드 동기화 상호 배제 (Thread Synchronization Mutual Exclusion)]
    │
    ├──▶ [경쟁 조건 (Race Condition)]
    └──▶ [임계 구역 3가지 요구조건]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 유치원에 '로봇 장난감(공유 자원)'이 딱 1개 있어요. 친구 10명이 동시에 로봇 팔, 다리를 잡아당기면 로봇이 박살 나겠죠([[001_dikw_pyramid|데이터]] 오염)?
2. 선생님이 규칙을 정했어요. "로봇은 텐트([[214_critical_section|임계 구역]]) 안에 두고, 입구에 있는 열쇠([[283_mutual_exclusion|상호 배제]] 락)를 가진 사람 딱 1명만 들어가서 놀 수 있어!"
3. 열쇠를 못 가진 친구들은 텐트 밖에서 기다려야 해서 조금 지루하지만, 이렇게 '[[283_mutual_exclusion|상호 배제]]' 규칙을 지켜야 로봇이 망가지지 않고 모두가 안전하게 놀 수 있답니다!
