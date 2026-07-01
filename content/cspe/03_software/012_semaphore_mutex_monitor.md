---
title: "세마포어·뮤텍스·모니터 (Semaphore Mutex Monitor)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 12
---

# 📖 【암기용】 개념 완전 이해

> 목적: 세마포어, 뮤텍스, 모니터를 처음 봐도 동시성 제어 도구의 차이로 이해하게 만든다. 시험 답안 양식이 아니라, 공유 자원 보호 원리를 설명한다.

## 한눈에
- **개요**: 세 도구는 여러 스레드가 공유 자원에 동시에 접근할 때 race condition을 막는 동기화 기법이다.
- **왜 필요한가**: CPU 코어 수가 늘면 같은 데이터에 접근하는 실행 흐름도 늘어난다. 잠금 없이 갱신하면 계좌 잔액, 큐 포인터, 파일 메타데이터가 깨진다.
- **핵심 직관**: 세마포어는 입장권 개수, 뮤텍스는 열쇠 소유자, 모니터는 열쇠와 대기실을 언어 구조 안에 넣은 방식이다.

## 깊이 이해
- **배경·문제의식**: 공유 변수 `count++`도 실제로는 load, add, store 3단계다. 두 스레드가 중간에 끼어들면 한 번의 증가가 사라진다.
- **작동 원리**: 세마포어는 정수 카운터를 P(wait)와 V(signal) 원자 연산으로 조작한다. 뮤텍스는 소유 스레드만 unlock할 수 있는 배타 잠금이다. 모니터는 lock, condition variable, invariant를 묶어 진입과 대기를 구조화한다.
- **비유**: 세마포어는 주차장 남은 자리 수, 뮤텍스는 회의실 열쇠, 모니터는 회의실 예약 시스템과 대기 알림을 합친 시설이다.
- **구체 예시**: DB 커넥션 풀 20개는 counting semaphore 값 20으로 제한하고, 전역 LRU 리스트 수정은 mutex 1개로 보호하며, bounded buffer는 monitor와 condition variable `notFull`, `notEmpty`로 구현한다.
- **흔한 오해·주의점**: binary semaphore와 mutex는 둘 다 값 0/1처럼 보이나 mutex는 ownership이 있어 다른 스레드가 unlock하면 오류 처리 대상이다.

## 연결 개념
- 임계 구역(Critical Section) — 공유 자원을 보호해야 하는 코드 구간
- 조건 변수(Condition Variable) — 모니터 내부에서 조건 충족까지 대기하는 큐
- 교착상태(Deadlock) — 잠금 순서와 해제 누락으로 발생하는 진행 중단

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 세 도구 이름을 나열하지 말고, 카운터·소유권·언어 수준 캡슐화 차이와 적용 조건을 비교한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 세마포어·뮤텍스·모니터는 공유 자원 접근 순서를 제어해 race condition과 lost update를 방지하는 동기화 원시기법이다.
> 2. **가치**: counting semaphore는 N개 자원, mutex는 단일 임계 구역, monitor는 lock과 condition variable을 캡슐화한다.
> 3. **판단 포인트**: 자원 개수, 소유권 필요성, 조건 대기, 언어 런타임 지원 여부로 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 동기화 원시기법 구분 확인 | counting/binary semaphore, mutex ownership, monitor invariant | binary semaphore와 mutex 동일 처리 지양 |
| 임계 구역 보호 역량 확인 | wait/signal, lock/unlock, condition wait/notify | busy waiting과 blocking 차이 누락 |
| 적용 판단 확인 | pool 제한, 단일 자원 보호, 조건 대기 모델 | unlock 누락·lost wakeup 리스크 미기재 |

> 요약: 이 문제는 공유 자원 개수와 조건 대기 필요성에 따라 동기화 도구를 선택하는 판단을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 동기화 원시기법은 공유 접근 순서 제어이다.
- 배경: 멀티스레드 프로그램은 공유 변수 갱신이 load, update, store로 분리되어 race condition, lost update, visibility 문제가 발생한다.
- 필요성: 세마포어·뮤텍스·모니터는 자원 수량, 소유권, 조건 대기 여부를 기준으로 race detector 0건과 lock wait p99를 관리하게 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Shared Resource -> Synchronization Primitive -> Critical Section
        / Semaphore: counter + wait/signal
        / Mutex: owner + lock/unlock
        / Monitor: lock + condition variable + invariant
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Semaphore | 카운터로 동시 접근 수 제한 | counting N, binary 0/1 |
| Mutex | 단일 소유자 기반 배타 접근 | owner thread만 unlock |
| Monitor | 객체 내부 lock과 조건 대기 캡슐화 | condition variable, invariant 유지 |

> 요약: 세마포어는 수량 제한, 뮤텍스는 소유권 배타, 모니터는 조건 대기까지 포함한 구조화된 동기화다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Thread Request -> Acquire Primitive -> Condition / Counter Check
  -> Enter Critical Section -> Update Shared State
  -> Signal / Unlock -> Wake Waiting Thread
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 공유 자원 접근 전 acquire 수행 | lock state, counter 값 확인 |
| 2 | 조건 불충족 시 wait queue로 이동 | blocked thread count |
| 3 | 임계 구역에서 상태 변경 | invariant 위반 0건 |
| 4 | release 후 대기 스레드 깨움 | wakeup loss 0건 |

> 요약: 동기화는 acquire, 조건 확인, 상태 변경, release와 wakeup 순서가 지켜질 때 공유 상태 일관성을 유지한다.

---

## Ⅳ. 특징

| 구분 | Semaphore | Mutex | Monitor |
|:---|:---|:---|:---|
| 제어 단위 | N개 자원 수량 | 1개 임계 구역 | 객체·메서드 단위 |
| 소유권 | 소유권 없음 | owner thread 존재 | 런타임이 lock 소유 관리 |
| 대기 방식 | wait queue 또는 spin | blocking 또는 adaptive | condition variable wait |
| 수치 예 | pool size 20 제한 | critical section 10us 이하 | bounded buffer 1024 slots |

> 요약: 세마포어는 동시성 수, 뮤텍스는 배타 소유, 모니터는 상태 조건과 불변식 관리에 맞다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | atomic 변수 단독 | lock 기반 임계 구역 | 복합 상태 2개 이상 갱신 시 |
| 비용/성능 | lock-free CAS loop | blocking mutex, semaphore | critical section 10us 초과면 blocking |
| 운영/위험 | 수동 lock 관리 | monitor 캡슐화 | lost wakeup 방지와 코드 가독성 |

> 요약: 단일 카운터는 atomic, 복합 상태는 mutex, 조건 대기 포함 객체는 monitor를 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Deadlock | 잠금 순서 역전 | lock ordering, timeout | lock wait p99, deadlock 0건 |
| Lost Wakeup | signal 전 조건 검사 누락 | while 조건 재검사 | missed signal test 0건 |
| Priority Inversion | 낮은 우선순위 owner가 lock 보유 | priority inheritance | high-priority wait time |

> 요약: 동기화 리스크는 잠금 순서, 조건 재검사, 우선순위 상속으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정확성 | race detector 경고 0건 | ThreadSanitizer, stress test |
| 대기시간 | lock wait p99 1ms 이하 | profiler, eBPF lock trace |
| 처리량 | contention 5% 이하 | perf lock, throughput benchmark |

> 요약: 적용 효과는 race 검출 결과, lock wait p99, contention 비율로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. DB connection pool, worker slot, rate limit은 counting semaphore로 동시 접근 수를 N개로 제한함.
2. 해시맵, LRU 리스트, reference count 복합 갱신은 mutex로 감싸고 critical section을 10us 이하 목표로 분해함.
3. 생산자-소비자 큐는 monitor와 condition variable `notFull`, `notEmpty`를 사용하고 wait 조건을 while로 재검사함.

**결론 (2줄):**
- 기술사 판단: 자원 수량 제어는 semaphore, 단일 임계 구역은 mutex, 조건 기반 상태 전이는 monitor가 적합함.
- 향후 방향: 언어 런타임은 structured concurrency와 race detector를 결합해 동기화 오류를 빌드·테스트 단계에서 차단함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "세마포어, 뮤텍스, 모니터를 설명하시오" | acquire, wait, release 흐름 | 세 도구의 소유권·조건 대기 차이 |
| 요구사항 명시형 | "비교하시오", "설계하시오" | pool, 임계 구역, bounded buffer 적용 흐름 | 자원 수·대기시간·lost wakeup 선택 기준 |

> 요약: 설명형은 개념 차이를, 설계형은 공유 자원 패턴별 도구 선택을 중심으로 전개한다.
