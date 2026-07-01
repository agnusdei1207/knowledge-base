---
title: "스레드 안전 프로그래밍 (Thread-Safe Programming)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 274
---

# 📖 【암기용】 개념 완전 이해

> 목적: 스레드 안전을 여러 스레드가 동시에 접근해도 자료구조 불변식이 깨지지 않는 성질로 이해하게 만든다.

## 한눈에
- **개요**: 스레드 안전은 공유 상태 동시 접근 시 데이터 경쟁과 순서 오류를 막는 설계 성질이다.
- **왜 필요한가**: 멀티코어 서버는 요청을 병렬 처리하므로 공유 변수, 캐시, 세션, 큐 접근에서 경쟁 조건이 발생한다.
- **핵심 직관**: 여러 사람이 같은 문서를 동시에 수정할 때 잠금, 버전, 복사본을 써서 덮어쓰기를 막는 방식이다.

## 깊이 이해
- **배경·문제의식**: CPU 코어가 늘어나면서 스레드는 같은 메모리 공간을 공유한다. 읽기·수정·쓰기 연산이 원자적이지 않으면 lost update, dirty read, visibility 문제가 생긴다.
- **작동 원리**: mutex, monitor, atomic, immutable object, thread confinement, message passing으로 공유 상태 접근 경로를 제한한다.
- **비유**: 은행 창구 잔액 변경은 번호표와 잠금이 필요하고, 공지문처럼 읽기 전용 문서는 여러 명이 동시에 봐도 문제가 없다.
- **구체 예시**: `count++`는 load, add, store 3단계라 두 스레드가 동시에 실행하면 100,000회 증가 후 값이 99,321처럼 손실될 수 있다.
- **흔한 오해·주의점**: `volatile`은 가시성 보장이지 복합 연산 원자성 보장이 아니다. `volatile count++`는 데이터 경쟁을 제거하지 못한다.

## 연결 개념
- 동기화·락 — 임계구역 보호 기법
- 불변 객체 — 공유 상태 변경 자체를 제거하는 접근
- 메모리 모델 — happens-before와 가시성 규칙

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

스레드 안전은 동시 실행 환경에서 공유 데이터가 일관된 결과를 내는 성질이다. 웹 서버, 배치, 메시지 소비자는 수십~수백 스레드가 객체를 공유하므로 원자성·가시성·순서성 보장이 필요하다.

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
