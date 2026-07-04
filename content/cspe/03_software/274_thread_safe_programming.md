---
title: "스레드 안전 프로그래밍 (Thread-Safe Programming)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 274
---

# 📖 【암기용】 개념 완전 이해

> 목적: 이 개념을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 스레드 안전(Thread-Safe)은 **동시성 제어**(Concurrency Control)의 목표 중 하나로, 여러 스레드가 같은 **공유 상태**(Shared State)에 동시 접근해도 데이터의 원자성·가시성·순서성이 깨지지 않는 프로그램의 성질이다.
- **왜 필요한가**: 멀티코어 CPU는 스레드를 진짜로 병렬 실행하므로, 같은 메모리(전역 변수·캐시·세션·큐)를 여러 스레드가 동시에 건드리면 값이 사라지거나(lost update) 잘못된 순서로 보이는(reordering) 결함이 실제로 발생한다.
- **핵심 직관**: 여러 사람이 같은 은행 계좌를 동시에 고칠 땐 번호표(락)나 원자적 갱신(CAS)이 필요하지만, 벽에 붙은 공지문처럼 아무도 고치지 않고 읽기만 한다면(불변) 동시에 봐도 아무 문제가 없다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 동시성(Concurrency) | 여러 작업이 겹쳐서(교차 또는 병렬로) 진행되는 것 — 이 문서 전체의 상위 주제 | 여러 사람이 같은 시간대에 같은 공간을 씀 |
| 공유 상태(Shared State) | 두 개 이상의 스레드가 함께 읽고 쓰는 변수·객체 | 여러 명이 함께 쓰는 화이트보드 |
| Race Condition(경쟁 조건) | 실행 순서(interleaving)에 따라 결과가 달라지는 결함 — 스레드 안전의 반대 상태 | 동시에 화이트보드에 낙서해서 누구 글씨가 남을지 운에 달림 |
| Critical Section(임계구역) | 한 번에 한 스레드만 실행해야 하는, 공유 상태를 건드리는 코드 구간 | 한 명씩만 들어갈 수 있는 탈의실 |
| Mutex/Lock | 임계구역에 한 스레드만 들어가도록 강제하는 상호배제 도구 | 탈의실 문 잠금과 번호표 |
| Atomic 연산(CAS) | CPU 명령어 수준에서 더 쪼갤 수 없는 연산 — "값이 A면 B로 바꿔라"를 한 번에 처리 | 문지기가 조건을 확인하고 즉시 바꿔주는 것 — 중간에 끼어들 틈이 없음 |
| Visibility(가시성) | 한 스레드가 쓴 값이 다른 스레드의 읽기에 실제로 보이는지 여부(CPU 캐시·컴파일러 재정렬 때문에 안 보일 수 있음) | 내가 화이트보드에 쓴 글씨가 옆방 CCTV 화면엔 아직 안 뜨는 상황 |
| happens-before | 메모리 모델(JMM 등)이 "이 쓰기가 저 읽기보다 먼저 일어난 것으로 보장한다"고 규정하는 순서 규칙 | "내가 먼저 쓴 다음에야 네가 읽는다"를 규칙으로 못 박음 |
| volatile | 가시성만 보장하는 키워드 — 복합 연산의 원자성은 보장하지 않음 | 화이트보드 글씨를 즉시 모두에게 보여주지만, 여러 명이 동시에 고치는 건 못 막음 |
| Deadlock(교착상태) | 두 스레드가 서로 상대가 쥔 자원을 기다리며 영원히 멈추는 상태 | 두 사람이 서로 "네가 먼저 문 열어"라며 마주 서서 안 움직임 |

## 깊이 이해

### count++ 가 왜 안전하지 않은가 — 3단계로 쪼개서 확인
- `count++`는 겉보기엔 한 줄이지만 내부적으로 **load(현재 값 읽기) → add(1을 더함) → store(결과 저장)** 3단계로 실행된다. 이 3단계는 원자적이지 않아서 중간에 다른 스레드가 끼어들 수 있다.
- 최소 예: count=0에서 스레드 A와 B가 거의 동시에 `count++`를 실행한다고 하자. A가 load해서 0을 읽는다 → B도 load해서 (아직 A가 store 전이므로) 0을 읽는다 → A가 add해서 1을 store한다 → B도 자기가 읽은 0에 add해서 1을 store한다. 두 번 증가했어야 할 count가 결국 1이 된다 — 이것이 lost update다.
- 규모를 키우면: 두 스레드가 각각 100,000번씩 `count++`를 실행하면 이론상 200,000이 되어야 하지만, 동기화 없이 실행하면 경쟁이 발생한 횟수만큼 값이 깎여 199,000대의 어중간한 숫자로 끝나는 것이 실제로 관찰된다 — 매 실행마다 값이 달라지는 재현 불가능성이 race condition의 특징이다.

### Lock 기반 vs CAS(Lock-free) 기반 — 원리와 비용 차이
- **Lock(예: synchronized, ReentrantLock)**: 임계구역 진입 전 락을 획득하고, 못 얻으면 스레드가 대기(blocking) 상태로 전환되어 OS 스케줄러가 개입한다. context switch 비용이 수 마이크로초~밀리초 단위로 들어 경쟁이 심하면 처리량이 급격히 떨어진다.
- **CAS(Compare-And-Swap, 예: AtomicInteger)**: "현재 값이 기대한 값 A와 같으면 B로 바꿔라, 다르면 실패"를 하드웨어 명령어 한 번으로 처리한다. 실패하면 재시도(retry loop)할 뿐 스레드를 잠재우지 않으므로 blocking이 없다(lock-free). 경쟁이 낮으면 락보다 훨씬 빠르지만(수~수십 나노초), 경쟁이 아주 심하면 재시도가 폭증해 오히려 느려질 수 있다.

### 가시성 문제 — reordering이 실제로 만드는 버그
- CPU 캐시와 컴파일러는 성능을 위해 명령어 순서를 바꿀 수 있다(reordering). 예: 스레드 A가 `data = 42; flag = true;` 순서로 썼더라도, volatile/synchronized 같은 순서 보장 장치가 없으면 스레드 B는 `flag == true`를 확인한 뒤에도 `data`가 아직 0으로 보일 수 있다.
- happens-before 규칙(volatile 쓰기→읽기, 락 해제→획득, 스레드 시작 등)은 이런 재정렬이 관측되지 않도록 컴파일러·CPU에 순서 장벽(memory barrier)을 강제한다.

### Deadlock이 만들어지는 4조건과 예방
- 교착상태는 ①상호배제 ②점유대기 ③비선점 ④순환대기 4조건이 모두 성립할 때 발생한다. 예: 스레드 A가 Lock1을 쥐고 Lock2를 기다리는 동시에, 스레드 B가 Lock2를 쥐고 Lock1을 기다리면 서로 영원히 대기(순환대기)한다.
- 가장 실무적인 예방책은 **락 순서 고정(lock ordering)**이다. 모든 코드가 항상 "Lock1을 먼저, Lock2를 나중에"만 획득하도록 강제하면 애초에 순환 자체가 생길 수 없다.

### 비유
- 은행 창구에서 잔액을 바꾸려면 번호표를 뽑고 순서를 기다려야 하지만(Lock), 벽에 붙은 공지문은 아무도 고치지 않으므로 여러 명이 동시에 읽어도 문제가 없다(Immutable/읽기 전용).

### 흔한 오해·주의점
- `volatile count++`는 여전히 race condition이다 — volatile은 가시성만 보장하지, load-add-store 3단계의 원자성은 전혀 보장하지 않는다.
- `synchronized`를 무조건 넓게 걸면 안전은 얻지만 임계구역이 커질수록 스레드들이 순서대로 줄을 서야 해서 처리량(throughput)이 크게 떨어진다 — 임계구역은 최소 범위로 좁혀야 한다.

## 연결 개념
- 동기화·락(Mutex, Monitor, CAS) — 임계구역을 보호하는 구체적 기법들
- 불변 객체(Immutable Object) — 애초에 "쓰기"를 없애 락 없이도 스레드 안전을 얻는 접근(275에서 상세)
- 메모리 모델(JMM 등) — happens-before와 가시성 규칙을 정의하는 언어별 표준

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 스레드 안전을 race condition 원인, 동기화 구조, 검증 지표 중심으로 답안화한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스레드 안전은 다중 스레드 환경에서 공유 상태의 원자성, 가시성, 순서성이 보장되는 프로그램 성질이다.
> 2. **가치**: 데이터 손실, 교착상태, 순서 오류를 줄여 요청 처리 결과의 일관성을 확보한다.
> 3. **판단 포인트**: 락 사용 여부보다 공유 상태 최소화, 임계구역 범위, happens-before, contention 지표를 봐야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 동시성 결함 이해 확인 | race condition, deadlock, visibility, atomicity | synchronized만 쓰면 해결된다는 답안 |
| 설계 기법 비교 확인 | lock, atomic, immutable, concurrent collection | 기법별 적용 조건과 비용 누락 |
| 검증 역량 확인 | stress test, thread sanitizer, lock contention | 테스트 없이 코드 패턴만 제시 |

> 요약: 스레드 안전 문제는 공유 상태 제어와 검증 지표까지 써야 판단형 답안이 된다.

---

## Ⅰ. 개요 및 필요성

- 개요: 스레드 안전은 동시 실행 중 공유 데이터 일관성을 지키는 성질이다.
- 배경: 웹 서버, 배치, 메시지 소비자는 수십~수백 스레드가 객체를 공유하므로 경쟁 조건과 가시성 문제가 발생한다.
- 필요성: lock, atomic, immutable, happens-before 규칙으로 원자성·가시성·순서성을 보장해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Thread A / Thread B -> Shared State
  -> Synchronization Policy
     / Lock / Atomic / Immutable / Message Queue
  -> Consistent Result -> Metrics
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Shared State | 동시 접근 대상 데이터 | 전역 변수, cache, session |
| Critical Section | 원자적으로 보호할 코드 | 범위 최소화 필요 |
| Synchronization | 접근 순서·가시성 보장 | mutex, monitor, CAS |
| Verification | 동시성 결함 탐지 | stress test, sanitizer |

> 요약: 스레드 안전 구조는 공유 상태를 식별하고 임계구역과 동기화 정책으로 접근을 제한한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
공유 상태 식별 -> 접근 패턴 분석 -> 보호 정책 선택
  / 쓰기 많음: lock or atomic
  / 읽기 많음: immutable or copy-on-write
  -> 동시성 테스트 -> contention 측정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 공유 변수와 객체 수명 식별 | thread escape 분석 |
| 2 | read/write 비율과 불변식 정의 | lost update 재현 여부 |
| 3 | lock, atomic, immutable 중 선택 | happens-before 보장 |
| 4 | 부하·경쟁 테스트 수행 | race finding 0건, p99 lock wait |

> 요약: 스레드 안전은 공유 상태 분석에서 시작해 정책 선택과 경쟁 지표 검증으로 완성된다.

---

## Ⅳ. 특징

| 구분 | 비안전 코드 | 스레드 안전 코드 | 정량·기술 포인트 |
|:---|:---|:---|:---|
| 원자성 | `count++` 경쟁 | AtomicInteger, lock | lost update 0건 |
| 가시성 | 캐시된 값 읽기 | volatile, lock, final | happens-before 구성 |
| 순서성 | 재정렬 영향 | memory barrier | JMM, C++ memory order |
| 처리 비용 | 동기화 없음 | contention 발생 가능 | p99 lock wait 측정 |

> 요약: 스레드 안전은 정확성을 얻는 대신 락 대기와 설계 복잡도를 지표로 관리해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| Lock | 상호배제 | 단순 불변식 보호 | 임계구역 짧고 충돌 낮을 때 |
| Atomic/CAS | lock-free | 카운터·상태 플래그 | 단일 변수 갱신 중심 |
| Immutable/Queue | 공유 변경 제거 | 함수형·Actor 모델 | 읽기 많거나 분산 이벤트 처리 |

> 요약: 단순 복합 상태는 lock, 단일 변수는 atomic, 변경 공유 제거는 immutable·queue가 선택 기준이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Race condition | 보호 없는 공유 쓰기 | lock, atomic, confinement | thread sanitizer finding 0건 |
| Deadlock | lock 순서 역전 | lock ordering, timeout | deadlock dump 0건 |
| Contention | 임계구역 과다 | sharding, read-write lock | p99 lock wait 10ms 이하 |

> 요약: 동시성 리스크는 race, deadlock, contention으로 구분해 도구와 지표로 검증한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정확성 | 동시성 stress test 1시간 오류 0건 | jcstress, Go race detector |
| 지연 | p99 lock wait 10ms 이하 | profiler, APM |
| 코드 품질 | shared mutable state 신규 0건 | code review checklist |

> 요약: 스레드 안전 품질은 오류 재현, 락 대기, 공유 변경 상태 증가 여부로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 공유 상태 목록을 작성하고 owner thread, lock order, immutable 여부를 설계 문서에 명시함.
2. Java는 `ConcurrentHashMap`, `AtomicLong`, `ReentrantReadWriteLock`을 적용하고 jcstress로 race 검출 0건을 확인함.
3. 운영은 p99 lock wait, thread pool queue depth, deadlock dump를 APM 지표로 수집하고 경보 기준을 둠.

**결론 (2줄):**
- 기술사 판단: 공유 변경 상태를 줄인 뒤 남은 임계구역에 lock·atomic을 적용하는 순서가 타당함.
- 향후 방향: actor, reactive stream, immutable data 구조로 스레드 간 공유 쓰기를 줄이는 설계가 확대됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "스레드 안전을 설명하시오" | 공유 상태 분석과 동기화 흐름 | 원자성·가시성·순서성 |
| 요구사항 명시형 | "설계하시오", "대응 방안을 제시하시오" | lock/atomic/immutable 선택 흐름 | deadlock, contention, 검증 지표 |

> 요약: 설명형은 동시성 원리, 설계형은 공유 상태 제거와 검증 체계 중심으로 전환한다.
