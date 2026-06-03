---
title: 694. 스레드 로컬 스토리지 (TLS)
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[092_thread_lwp|스레드]] 로컬 스토리지([[113_thread_local_storage|Thread Local Storage]], TLS)는 같은 프로세스 내의 [[092_thread_lwp|스레드]]들이 힙([[078_heap_datastructure|Heap]])과 [[001_dikw_pyramid|데이터]]([[001_dikw_pyramid|Data]]) 영역을 공유한다는 대전제를 살짝 비틀어, **"전역(Global) 변수처럼 생겼지만 실제로는 각 [[092_thread_lwp|스레드]]마다 독립적인 복사본을 가지는 특수한 메모리 공간"**을 의미한다.
> 2. **메커니즘**: 컴파일러와 OS가 협력하여 특정 변수(예: C언어의 `__thread` 키워드)를 TLS 섹션에 할당하고, CPU [[057_register|레지스터]](x86의 FS/GS [[057_register|레지스터]])를 통해 현재 실행 중인 [[092_thread_lwp|스레드]]의 고유한 TLS 주소 시작점을 가리키게 하여 $O(1)$ 속도로 [[092_thread_lwp|스레드]]별 변수에 접근하게 한다.
> 3. **가치**: 글로벌 변수를 쓸 때마다 락([[223_mutex|Mutex]])을 걸어야 하는 엄청난 병목(Contention)을 회피할 수 있게 해 주며, `errno` 같은 전통적인 에러 변수나 무작위 [[486_trng|난수 생성기]](RNG) 상태 등을 **[[256_lock_free_data_structures|Lock-Free]]**하게 관리하게 해주는 현대 고성능 [[397_multithreading|멀티스레딩]]의 필수 인프라다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **TLS ([[113_thread_local_storage|Thread Local Storage]])**: 변수 선언 시 [[092_thread_lwp|스레드]] 단위로 생명 주기가 관리되는 저장 공간. A [[092_thread_lwp|스레드]]의 TLS 변수 `count`와 B [[092_thread_lwp|스레드]]의 TLS 변수 `count`는 이름만 같고 메모리 주소가 완전히 다르다.

- **필요성 (전역 변수의 배신과 락 병목)**: 
  - 멀티스레드의 장점은 "메모리를 공유"하는 것이다. 하지만 이게 독이 될 때가 있다.
  - C언어에서 시스템 콜이 실패하면 그 이유를 전역 변수인 `errno`에 적는다. [[092_thread_lwp|스레드]] A가 실패해서 `errno=5`를 적었는데, 그 찰나에 [[092_thread_lwp|스레드]] B가 덮어쓰고, A가 `errno`를 읽으면 엉뚱한 에러를 보게 된다 ([[213_race_condition|Race Condition]]).
  - 이걸 막으려면 `errno`를 읽고 쓸 때마다 락([[510_lock|Lock]])을 걸어야 하는데, 그러면 멀티스레드의 장점(병렬성)이 다 날아가고 시스템이 단일 [[092_thread_lwp|스레드]]처럼 느려진다.
  - **해결책**: "이름은 똑같이 전역 변수 `errno`인데, [[092_thread_lwp|스레드]] A가 부를 때와 B가 부를 때 몰래 다른 메모리 주소를 가리키게 마술을 부려주자!" 이것이 TLS의 탄생이다.

  - **전역 변수 (공유)**: 회사 휴게실에 있는 단 1개의 공용 다이어리. 모두가 동시에 글을 쓰려다 보니 펜을 잡으려고 싸움([[510_lock|Lock]])이 나고, 남이 내 글을 지울 수도 있다.
  - **지역 변수 ([[057_stack|Stack]])**: 직원들이 각자 주머니에 넣고 다니는 포스트잇. 안전하지만, 다른 부서(다른 함수)에 갈 때마다 일일이 손으로 건네줘야 해서 귀찮다.
  - **TLS ([[092_thread_lwp|Thread]] Local)**: 회사에서 모든 직원에게 "나만의 비밀 서랍"을 하나씩 나눠주었다. 휴게실(어느 함수에서든)에 가서 "내 비밀 서랍 열어!"라고 하면, 지문 인식을 통해 기가 막히게 내 서랍만 열린다. 전역 변수처럼 편하게 부르지만, 내용은 완벽히 독립적이다.

- **발전 과정**:
  1. **[[459_quic_fec_forward_error_correction|초기]] [[397_multithreading|멀티스레딩]]**: TLS 개념이 없어 전역 변수 [[212_synchronization_mechanisms|동기화]] 지옥에 빠짐 (`errno` 문제).
  2. **명시적 [[014_api_posix|API]] 시대**: `pthread_key_create()` 같은 복잡한 C API를 써서 수동으로 매핑함.
  3. **컴파일러 지원 (현재)**: C11의 `thread_local`, Java의 `ThreadLocal<T>` 처럼 키워드 하나만 붙이면 컴파일러와 OS가 알아서 메모리를 찢어주는 마법 구현.

- **📢 섹션 요약 비유**: 락([[510_lock|Lock]])이 여러 [[092_thread_lwp|스레드]]가 하나의 화장실(변수)을 [[289_cqrs_db|쓰기]] 위해 줄을 서는 것이라면, TLS는 아예 [[092_thread_lwp|스레드]] 개수만큼 1인용 화장실을 복사해서 지어주는 플렉스(Flex)입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### TLS의 3가지 메모리 [[104_classification_analysis|분류]] ([[382_virtual_address_space|가상 주소 공간]] 내 위치)

[[092_thread_lwp|스레드]] 1개가 [[381_virtual_memory|가상 메모리]] 내에서 갖는 공간은 크게 3가지로 나뉜다. TLS는 [[057_stack|스택]]과 힙의 애매한 중간 성격을 띤다.

| 구분 | 생명 주기 (Lifetime) | 공유 여부 | 용도 |
|:---|:---|:---|:---|
| **지역 변수 ([[057_stack|Stack]])** | 함수(`{ }`)가 끝나면 소멸 | [[092_thread_lwp|스레드]] 전용 (독립) | 함수 내부의 임시 [[001_dikw_pyramid|데이터]] 처리 |
| **전역/힙 ([[001_dikw_pyramid|Data]]/[[078_heap_datastructure|Heap]])**| 프로세스가 끝날 때까지 생존 | **모든 [[092_thread_lwp|스레드]]가 공유** | [[092_thread_lwp|스레드]] 간 [[001_dikw_pyramid|데이터]] 통신, 대규모 [[001_dikw_pyramid|데이터]] |
| **TLS 변수** | **[[092_thread_lwp|스레드]]가 죽을 때까지 생존** | **[[092_thread_lwp|스레드]] 전용 (독립)** | **함수를 넘나들며 유지해야 하는 [[092_thread_lwp|스레드]]만의 고유 상태 (예: [[191_transaction_concept_states|트랜잭션]] ID)** |

---

### 하드웨어와 OS의 마술: FS / GS [[057_register|레지스터]] (x86 기준)

C코드에서 `__thread int my_id;` 라고 치면 어떻게 각 [[092_thread_lwp|스레드]]마다 다른 주소를 찾아갈까? 
이것은 [[001_operating_system_purpose|운영체제]]가 [[211_context_switch|문맥 교환]]([[211_context_switch|Context Switch]])을 할 때 CPU [[057_register|레지스터]]를 교묘하게 조작하기 때문이다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 x86 아키텍처 기반의 TLS 포인터 매핑 구조               │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  [상황: 스레드 1 실행 중]                                             │
  │   - 커널 스케줄러가 스레드 1로 문맥 교환 시,                           │
  │     특수 레지스터인 [FS 레지스터]에 "0x1000" (스레드 1의 TLS 주소)를 넣음.│
  │   - `my_id` 변수는 컴파일러에 의해 `FS:[0x08]` 위치로 번역됨.            │
  │   - 스레드 1이 `my_id = 5`를 하면 물리적으로 "0x1008" 에 5가 써짐.      │
  │                                                                   │
  │  ========== ⚡ 스레드 2로 문맥 교환 (Context Switch) ⚡ ===========│
  │                                                                   │
  │  [상황: 스레드 2 실행 중]                                             │
  │   - 커널이 이번엔 [FS 레지스터]에 "0x2000" (스레드 2의 TLS 주소)를 넣음.│
  │   - 스레드 2가 동일한 코드 `my_id = 10`을 실행함. (명령어는 `FS:[0x08]`) │
  │   - 하지만 FS가 0x2000이므로, 물리적으로 "0x2008" 에 10이 써짐!         │
  │                                                                   │
  │  [결론] 소스 코드 상의 이름(`my_id`)과 어셈블리 명령어(`FS:[0x08]`)는     │
  │         완벽하게 똑같지만, OS가 스위칭 때마다 기준점(FS)을 바꿔치기하여    │
  │         마법처럼 다른 메모리를 건드리게 한다.                            │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 개발자는 `my_id`라는 똑같은 글자를 친다. 하지만 컴파일러는 이 변수가 TLS임을 알고, 절대 주소를 쓰지 않고 `FS 레지스터로부터 +8칸 떨어진 곳`이라는 **상대 주소**로 코드를 짠다. OS는 [[092_thread_lwp|스레드]]를 교체할 때마다 이 FS [[057_register|레지스터]]의 '영점(Base)'을 해당 [[092_thread_lwp|스레드]]의 전용 힙 공간(TCB 근처)으로 슬쩍 옮겨 놓는다. $O(1)$의 하드웨어 속도로 전역 변수 이름 충돌 없이 완벽한 격리가 달성되는 원리다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### TLS와 파라미터 패싱(Parameter Passing)의 설계 비교

함수 깊숙한 곳(Depth [[489_raid_10_hybrid|10]])에 [[092_thread_lwp|스레드]]의 고유 정보를 전달하고 싶을 때 아키텍트의 선택이다.

| 비교 항목 | Call-by-Value (매개변수 전달) | [[113_thread_local_storage|Thread Local Storage]] (TLS) |
|:---|:---|:---|
| **코드 형태** | `funcA(..., thread_id) -> funcB(..., thread_id)` | 그냥 전역 변수 `thread_id` 호출 |
| **코드 오염도** | 최악 (모든 함수의 파라미터에 id를 추가해야 함) | **최상 (함수 시그니처 변경 없음)** |
| **메모리 할당** | 유저 [[057_stack|스택]]([[057_stack|Stack]]) 영역 | OS가 배정해 준 특정 TLS [[001_dikw_pyramid|데이터]] 영역 |
| **은닉 버그** | 명시적이므로 버그 추적 쉬움 | **어디서 값이 바뀌었는지 추적 어려움 (전역 변수의 단점 유지)** |

### 과목 융합 관점

- **소프트웨어공학 (SE)**: 스프링 프레임워크(Spring)의 핵심 철학인 `Transaction Synchronization`은 100% TLS(Java의 `ThreadLocal`) 덕분에 성립한다. 사용자의 [[461_http_stateless_connection_oriented|HTTP]] 요청 1개가 들어와서 컨트롤러 $\rightarrow$ [[090_service_kubernetes_network_load_balancing|서비스]] $\rightarrow$ 레포지토리 계층으로 파고들 때, DB 커넥션(Connection) 객체를 함수 파라미터로 넘기지 않아도 어디서든 똑같은 DB 락을 쥘 수 있는 이유는 프레임워크가 맨 앞에서 DB 커넥션을 낚아채어 TLS에 몰래 꽂아두었기 때문이다.
- **컴퓨터구조 ([[089_contract_account_smart_contract|CA]])**: `FS/GS 레지스터`는 원래 인텔의 세그먼테이션([[364_segmentation|Segmentation]]) 메모리 모델에서 쓰던 낡은 유물이었다. [[259_paging|페이징]]([[259_paging|Paging]])이 도입되며 쓸모없어진 이 [[057_register|레지스터]]를, 리눅스와 윈도우 OS 개발자들이 "어? 이거 TLS 기준점 잡는 데 쓰면 대박이겠는데?" 하고 재활용하여 부활시킨 공학적 해킹의 산물이다.

- **📢 섹션 요약 비유**: 회사에서 내 사원번호를 증명하기 위해, 모든 부서 사무실 문을 열 때마다 일일이 사원증을 꺼내 보여주는 것(파라미터 패싱)은 피곤합니다. TLS는 회사 출입구에서 내 목에 '스마트 태그(FS [[057_register|레지스터]])'를 한 번 걸어주면, 어느 사무실을 들어가든 문이 내 신원을 알아서 읽어주는 마법 목걸이입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — 멀티스레드 [[486_trng|난수 생성기]](Random) 락 병목 및 캐시 핑퐁**: 게임 서버에서 1,000개의 [[092_thread_lwp|스레드]]가 데미지 계산을 위해 초당 수만 번씩 전역 `rand()` 함수를 호출함. 서버 CPU가 100%를 치는데 게임이 뚝뚝 끊김.
   - **원인 분석**: C언어의 전통적인 `rand()` 함수는 내부에 전역 시드(Seed) 변수를 하나 두고, [[092_thread_lwp|스레드]]들이 이 변수를 갱신하면서 난수를 뽑는다. 1,000개의 [[092_thread_lwp|스레드]]가 1개의 전역 변수에 뮤텍스 락을 걸고 다투며([[275_lock_contention_monitoring|Lock Contention]]), MESI 프로토콜에 의해 엄청난 **캐시라인 핑퐁([[409_false_sharing|False Sharing]])**이 발생한 것이다.
   - **대응 (기술사적 가이드)**: [[486_trng|난수 생성기]]를 **TLS ([[092_thread_lwp|Thread]] Local)**로 격리해야 한다. `__thread unsigned int seed;` 처럼 각 [[092_thread_lwp|스레드]]마다 자신만의 고유한 시드 변수를 주면, [[092_thread_lwp|스레드]]들은 락([[510_lock|Lock]])을 전혀 걸지 않고 남의 캐시를 박살 내지 않으며([[256_lock_free_data_structures|Lock-Free]] & 0-Contention) 완벽한 병렬로 난수를 수백 배 빨리 뽑아낼 수 있다.

2. **시나리오 — Java ThreadLocal [[612_memory_leak_detection|메모리 누수]]([[612_memory_leak_detection|Memory Leak]]) 대참사**: Tomcat(WAS) 환경에서 유저의 장바구니 정보를 `ThreadLocal`에 담아두는 코드를 짰다. 며칠 뒤 서버가 `OutOfMemoryError (OOM)`를 뿜으며 사망함.
   - **원인 분석**: 톰캣은 요청마다 [[092_thread_lwp|스레드]]를 만들고 부수는 게 아니라, **[[103_thread_pool|스레드 풀]]([[103_thread_pool|Thread Pool]])**을 사용하여 한 번 만든 [[092_thread_lwp|스레드]]를 계속 재활용한다. A 유저의 요청을 처리하며 `ThreadLocal`에 [[001_dikw_pyramid|데이터]]를 넣었는데, 요청이 끝날 때 명시적으로 `remove()`를 해주지 않았다. 이 [[092_thread_lwp|스레드]]가 풀로 반환된 후 B 유저의 요청을 맡았을 때, B 유저가 A 유저의 장바구니를 보게 되는 치명적 버그가 터지고 남은 [[001_dikw_pyramid|데이터]]가 [[591_mvcc_garbage_collection_vacuum|가비지 컬렉터]](GC)에 수거되지 않아 메모리가 터진 것이다.
   - **아키텍처 적용**: [[103_thread_pool|스레드 풀]] 환경에서 TLS를 쓸 때는, 요청이 끝나는 `finally` 블록이나 `Filter/Interceptor`의 최후단에서 **반드시 TLS 변수를 `remove()` (Clear)**하여 [[092_thread_lwp|스레드]]를 갓 태어난 순수한 상태로 [[459_quic_fec_forward_error_correction|초기]]화하는 방어 코드를 OS/프레임워크 레벨에 강제해야 한다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 전역(Global) 상태 변수 아키텍처 설계 플로우               │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [멀티스레드 환경에서 여러 함수가 공통으로 접근해야 하는 상태 변수 발생]          │
  │                │                                                  │
  │                ▼                                                  │
  │      이 변수를 모든 스레드가 100% 동일한 값으로 공유해야 하는가? (예: 시스템 설정) │
  │          ├─ 예 ─────▶ [전역 변수 + Reader-Writer Lock 사용]          │
  │          │            (단, 수정이 잦으면 병목 터지므로 RCU 기법 등 고려)     │
  │          └─ 아니오 (스레드마다 자기만의 값을 가지면 된다)                    │
  │                │                                                  │
  │                ▼                                                  │
  │      그 값을 스레드가 살아있는 내내 유지해야 하는가?                         │
  │          ├─ 예 ─────▶ [Thread Local Storage (TLS) 적극 활용]       │
  │          │            (Lock-free 효과로 성능 극대화. 메모리 할당기, 로깅 ID) │
  │          │                                                        │
  │          └─ 아니오 ──▶ 그냥 지역 변수(Stack)와 함수 파라미터 패싱으로 해결    │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** "멀티스레드 [[212_synchronization_mechanisms|동기화]]([[510_lock|Lock]])가 너무 힘들어요"라고 징징대는 개발자에게 시니어 아키텍트가 내리는 최고의 처방전은 "그럼 [[212_synchronization_mechanisms|동기화]]를 하지 마라([[306_embedding_model|Shared Nothing]])"이다. 애초에 공유를 안 하면 락도 필요 없다. 전역 변수를 과감히 찢어서 [[092_thread_lwp|스레드]] 각자의 바구니(TLS)에 던져주고, 마지막에 결과만 메인 [[092_thread_lwp|스레드]]에서 합치는(Map-Reduce 방식) 설계가 초고성능 스케일 아웃의 비밀이다.

### 도입 [[435_checklist_based_testing|체크리스트]]
- **동적 로딩 (dlopen / [[333_shared_library|Shared Library]])**: C/C++에서 앱 실행 중에 `.so` (동적 [[336_library_vs_framework|라이브러리]])를 늦게 로딩할 경우, 미리 깎아둔 TLS 메모리 공간이 모자라서 충돌이 날 수 있다. 컴파일 옵션(`-ftls-model=initial-exec` vs `global-dynamic`)을 통해 TLS 접근 속도와 동적 로딩 [[344_compatibility_usability|호환성]] 사이의 아키텍처적 조율을 거쳤는가?

- **📢 섹션 요약 비유**: 전역 변수를 쓰는 것은 1차선 좁은 다리 양 끝에 신호등([[510_lock|Lock]])을 세우는 것입니다. TLS를 쓰는 것은 아예 [[092_thread_lwp|스레드]] 개수만큼 다리 100개를 지어서(메모리 투자), 신호등 없이 자동차들이 쌩쌩 달리게 만드는 고속도로 인프라 투자입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 전역 변수 + [[699_mutex_lock_sleep_wait|Mutex Lock]] | [[113_thread_local_storage|Thread Local Storage]] (TLS) | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (처리 속도)** | 병목(Contention)으로 코어 늘수록 [[282_performance_tactics|성능]] 하락 | **[[510_lock|Lock]]-Free로 코어 수에 비례한 선형 [[282_performance_tactics|성능]] 증가** | $O(1)$ 속도로 [[148_5g_embb_urllc_mmtc|초고속]] 무정지 연산 달성 |
| **정량 (캐시 효율)** | Cache Invalidation 핑퐁 폭발 | 각 [[092_thread_lwp|스레드]] 전용 캐시 라인 점유 | CPU 캐시 친화도([[778_process_affinity_scheduling_pinning|Affinity]]) 극대화 |
| **정성 (코드 [[333_readability_vs_efficiency|가독성]])**| 파라미터 더미로 함수 시그니처 오염 | 전역 변수처럼 깔끔한 호출 | 비즈니스 로직과 시스템 상태([[303_trace_id|Trace ID]] 등)의 관심사 분리 |

### 미래 전망
- **M:N [[092_thread_lwp|스레드]] 모델(가상 [[092_thread_lwp|스레드]])에서의 TLS 한계**: 최근 Java 21의 가상 [[092_thread_lwp|스레드]]나 Go 언어 같은 경량 [[092_thread_lwp|스레드]]는 1만 개가 아니라 '수백만 개'가 뜬다. 만약 수백만 개의 가상 [[092_thread_lwp|스레드]]가 10MB짜리 TLS를 갖는다면 메모리가 수십 TB가 필요해 당장 서버가 터진다. 이를 막기 위해 자바 진영은 TLS를 불변([[298_immutable|Immutable]]) 객체로 한정 짓고, 값을 수정할 수 없는 **Scoped Value**라는 새로운 개념을 도입하여 무분별한 TLS 남용 시대를 강제로 끝내려 하고 있다.

### 결론
[[092_thread_lwp|스레드]] 로컬 스토리지(TLS)는 [[397_multithreading|멀티스레딩]]이 태생적으로 안고 있는 "메모리 공유의 저주"를 풀기 위해 [[001_operating_system_purpose|운영체제]]와 컴파일러가 합작해 낸 최고의 우회로다. 겉보기엔 편리한 전역 변수의 탈을 쓰고 있지만, 속으로는 [[057_register|레지스터]](FS/GS)를 조작하여 락([[510_lock|Lock]]) 없이 완벽한 독립을 보장하는 이 이중성은 현대 백엔드 서버가 초당 수만 건의 [[191_transaction_concept_states|트랜잭션]]을 엉킴 없이 쳐낼 수 있는 숨은 공신이다. [[212_synchronization_mechanisms|동기화]]([[212_synchronization_mechanisms|Synchronization]])의 가장 완벽한 해답은 [[212_synchronization_mechanisms|동기화]]를 잘하는 것이 아니라, TLS를 통해 애초에 [[212_synchronization_mechanisms|동기화]]할 상황을 만들지 않는 것이다.

- **📢 섹션 요약 비유**: 수백 명의 요리사가 하나의 도마(전역 변수)를 공유하며 멱살을 잡고 싸울 때([[510_lock|Lock]] 경합), 사장([[001_operating_system_purpose|운영체제]])이 요리사마다 전용 미니 도마(TLS)를 하나씩 사주어 주방에 완벽한 침묵과 [[148_5g_embb_urllc_mmtc|초고속]] 요리 폭풍을 가져온 위대한 경영 판단입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[187_hrn_scheduling|HRN]] 대기 시간 공식 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[693_multithread_user_mode_kernel_mode|멀티스레드 유저모드 커널모드]] | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[092_thread_lwp|스레드]] [[212_synchronization_mechanisms|동기화]] [[283_mutual_exclusion|상호 배제]] | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[213_race_condition|경쟁 조건]] ([[213_race_condition|Race Condition]]) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[멀티스레드 유저모드 커널모드]
    │
    ▼
[스레드 로컬 스토리지 (TLS)]
    │
    ├──▶ [스레드 동기화 상호 배제]
    └──▶ [경쟁 조건 (Race Condition)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 반 친구들 30명이 칠판(전역 변수) 하나에 동시에 그림을 그리려고 하면, 서로 부딪히고 남의 그림을 망쳐서 싸움([[213_race_condition|경쟁 조건]])이 나요.
2. 싸움을 말리려면 한 명씩 줄을 서서(락, [[510_lock|Lock]]) 그려야 하는데 그러면 너무 오래 걸리죠.
3. 그래서 선생님이 아예 친구들 각자에게 개인용 '작은 스케치북([[092_thread_lwp|스레드]] 로컬 스토리지)'을 하나씩 나눠줬어요! 이제 싸우지 않고도 30명이 동시에 [[148_5g_embb_urllc_mmtc|초고속]]으로 그림을 그릴 수 있게 되었답니다.
