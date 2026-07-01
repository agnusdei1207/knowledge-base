---
title: "임계 구역·상호 배제 (Critical Section Mutual Exclusion)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 14
---

# 📖 【암기용】 개념 완전 이해

> 목적: 임계 구역과 상호 배제를 처음 봐도 race condition을 막는 기본 조건으로 이해하게 만든다. 시험 답안 양식이 아니라, 원자성과 진행 조건을 설명한다.

## 한눈에
- **개요**: 임계 구역은 공유 자원을 읽고 쓰는 코드 구간이고, 상호 배제는 한 번에 하나의 실행 흐름만 들어가게 하는 조건이다.
- **왜 필요한가**: 멀티코어에서는 두 스레드가 같은 변수, 파일, 큐를 동시에 바꿀 수 있다. 순서 제어가 없으면 결과가 실행 시점마다 달라진다.
- **핵심 직관**: 공유 장부를 고치는 동안 한 사람만 펜을 잡게 하고, 나머지는 순서를 기다리게 만드는 규칙이다.

## 깊이 이해
- **배경·문제의식**: `balance = balance - 100`은 한 문장처럼 보이나 실제로는 읽기, 계산, 쓰기 단계로 나뉜다. 두 스레드가 섞이면 lost update가 발생한다.
- **작동 원리**: 임계 구역 문제는 mutual exclusion, progress, bounded waiting 3조건을 만족해야 한다. 구현은 Peterson 알고리즘, test-and-set lock, compare-and-swap, mutex 등으로 발전했다.
- **비유**: 단일 좌석 화장실은 문 잠금으로 한 명만 사용한다. 대기 줄이 사라지지 않도록 순번을 관리해야 bounded waiting 조건도 충족된다.
- **구체 예시**: 두 스레드가 `counter++`를 100만 번씩 수행하면 기대값은 200만이다. 잠금이 없으면 context switch 지점에 따라 200만보다 작은 값이 나온다.
- **흔한 오해·주의점**: 상호 배제만 만족해도 충분하지 않다. 모두 양보해 아무도 못 들어가는 상황은 progress 위반이고, 특정 스레드가 계속 밀리면 bounded waiting 위반이다.

## 연결 개념
- Race Condition — 실행 순서에 따라 결과가 달라지는 경쟁 상태
- Atomic Operation — 중간 상태가 관찰되지 않는 단일 연산
- CAS(Test-and-Set) — 현대 잠금 구현의 하드웨어 원자 명령

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 임계 구역 답안은 lock 이름 나열이 아니라 mutual exclusion, progress, bounded waiting 조건과 구현 수단의 trade-off로 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 임계 구역은 공유 상태를 변경하는 코드 구간이며, 상호 배제는 동시에 하나의 실행 흐름만 진입시키는 동시성 안전 조건이다.
> 2. **가치**: 원자성 보장으로 lost update, inconsistent read, memory ordering 오류를 차단한다.
> 3. **판단 포인트**: mutual exclusion, progress, bounded waiting을 모두 만족해야 하며 구현은 Peterson, TSL, CAS, mutex로 구분한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 동시성 기본 조건 이해 확인 | race condition, atomicity, 3조건 | mutual exclusion만 쓰고 progress 누락하지 않음 |
| 구현 원리 비교 확인 | Peterson, TSL, CAS, mutex | 소프트웨어 알고리즘과 하드웨어 원자 명령 혼동 지양 |
| 적용 판단 확인 | 임계 구역 길이, lock granularity, 대기 방식 | 모든 공유 데이터에 단일 전역 lock 적용 지양 |

> 요약: 이 문제는 공유 자원 보호를 3조건과 구현 수단, 검증 지표까지 연결해 쓰는지 확인한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 임계 구역은 공유 자원 접근 코드이다.
- 배경: 멀티스레드·멀티코어 환경에서는 명령 interleaving으로 공유 상태 갱신 순서가 바뀌어 race condition과 데이터 불일치가 발생한다.
- 필요성: 상호 배제는 mutual exclusion, progress, bounded waiting 기준으로 원자적 갱신과 race detector 0건을 확보하기 위해 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
Thread A / Thread B -> Entry Section -> Critical Section
  -> Exit Section -> Remainder Section
  / Mutual Exclusion + Progress + Bounded Waiting
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Entry Section | lock 획득, 조건 검사 | CAS, TSL, mutex 사용 |
| Critical Section | 공유 자원 읽기·쓰기 | 가능한 짧게 유지 |
| Exit Section | lock 해제, 대기자 깨움 | memory barrier 필요 가능 |

> 요약: 임계 구역 구조는 진입, 실행, 해제 단계로 나뉘며 3조건을 만족해야 동시성 오류를 막는다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Request CS -> Check Lock / Flag -> Acquire Atomicity
  -> Execute Shared Update -> Release Lock
  -> Wake or Allow Next Thread -> Validate Invariant
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 진입 전 lock 상태 또는 turn 확인 | mutual exclusion 위반 0건 |
| 2 | 원자 명령으로 소유권 획득 | CAS failure rate |
| 3 | 공유 상태 갱신 수행 | invariant violation 0건 |
| 4 | lock 해제와 다음 대기자 진행 | max wait, progress 확인 |

> 요약: 임계 구역은 원자적 진입과 확실한 해제, 대기자 진행 보장이 함께 있어야 한다.

---

## Ⅳ. 특징

| 구분 | 소프트웨어 방식 | 하드웨어 원자 명령 | OS 동기화 |
|:---|:---|:---|:---|
| 대표 기법 | Peterson | TSL, CAS | mutex, semaphore |
| 적용 조건 | 2개 프로세스 교육 모델 | 멀티코어 lock 구현 | 실제 커널·런타임 |
| 한계 | compiler reorder 취약 | busy waiting 가능 | context switch 비용 3~10us |
| 판단 지표 | 3조건 만족 | CAS retry count | lock wait p99 |

> 요약: 실제 시스템은 하드웨어 원자 명령 위에 OS 동기화 객체를 올려 상호 배제와 대기 제어를 결합한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | lock 없는 공유 갱신 | 임계 구역 보호 | 복합 상태 2개 이상 갱신 시 |
| 비용/성능 | 동기화 비용 0 | lock wait, cache coherence 비용 | contention 5% 이하 목표 |
| 운영/위험 | race condition | deadlock, starvation | lock ordering과 timeout 필요 |

> 요약: 임계 구역은 정확성을 위해 동기화 비용을 지불하며, lock 범위와 경합률로 비용을 관리한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Race Condition | lock 누락 | static analysis, race detector | ThreadSanitizer 0건 |
| Deadlock | 다중 lock 순서 역전 | lock hierarchy, try-lock timeout | deadlock 0건 |
| Starvation | 불공정 lock wakeup | FIFO wait queue, aging | max wait 30초 이하 |

> 요약: 임계 구역 설계는 race 제거 후 deadlock과 starvation을 별도 지표로 검증해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정확성 | invariant violation 0건 | stress test, model checking |
| 대기시간 | lock wait p99 1ms 이하 | eBPF, profiler |
| 경합률 | contention 5% 이하 | perf lock, runtime metrics |

> 요약: 정확성, lock wait p99, contention 비율을 함께 봐야 상호 배제 설계의 품질을 판단할 수 있다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 공유 상태를 식별하고 read-only, atomic 단일 변수, mutex 필요 복합 상태로 분류해 lock 범위를 최소화함.
2. 다중 lock은 전역 lock ordering 문서를 두고 code review에서 순서 위반을 차단함.
3. 테스트에는 ThreadSanitizer, stress test 1만 반복, lock wait p99 측정을 포함해 race와 장기 대기를 검출함.

**결론 (2줄):**
- 기술사 판단: 임계 구역은 mutual exclusion만이 아니라 progress와 bounded waiting을 만족할 때 운영체제 수준 답안이 됨.
- 향후 방향: lock-free 자료구조, RCU, STM은 임계 구역 폭을 줄이지만 memory ordering 검증이 추가로 필요함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "임계 구역과 상호 배제를 설명하시오" | 3조건과 진입·해제 흐름 | Peterson, TSL, CAS, mutex 비교 |
| 요구사항 명시형 | "구현 방안을 제시하시오", "비교하시오" | lock ordering, 검증 흐름 | deadlock·starvation 리스크 대응 |

> 요약: 구현형 문제는 이론 알고리즘보다 lock 범위, 검증 지표, 운영 리스크 대응을 앞세운다.
