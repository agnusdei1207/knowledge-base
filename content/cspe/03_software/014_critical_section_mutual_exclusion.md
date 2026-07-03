---
title: "임계 구역·상호 배제 (Critical Section Mutual Exclusion)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 14
---

# 📖 【암기용】 개념 완전 이해

> 목적: 상호 배제를 실제 코드 구조(진입-실행-해제)와 구현 수단의 트레이드오프로 이해하게 만든다. 3대 조건 자체보다 "어떻게 구현하고 무엇을 검증하는가"에 집중한다.

## 한눈에
- **개요**: **상호 배제(Mutual Exclusion)**를 실제 코드로 구현하면 진입 절차(Entry Section) → 임계 구역(Critical Section) → 해제 절차(Exit Section) → 나머지 코드(Remainder Section)의 4단계 흐름이 된다. 이 흐름을 지탱하는 것이 **원자적 잠금 연산(Atomic Lock)**이다.
- **왜 필요한가**: 상호 배제·진행·한정된 대기라는 3대 조건을 안다고 끝이 아니다. 실무에서는 "락을 얼마나 넓게 걸까(Granularity)", "여러 락을 어떤 순서로 잡을까"에 따라 데드락·기아·성능이 갈린다. 그래서 구현 구조와 위험 유형을 구분해서 알아야 한다.
- **핵심 직관**: 은행 창구의 번호표 발급기(Entry Section) → 창구 업무 처리(Critical Section) → 다음 번호 호출(Exit Section)로 이어지는 4단계 파이프라인이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| Entry Section (진입 구간) | 락을 획득하고 진입 조건을 검사하는 구간 | 번호표 뽑고 대기 |
| Critical Section (임계 구역) | 공유 자원을 실제로 읽고 쓰는 구간 | 창구에서 업무 처리 |
| Exit Section (해제 구간) | 락을 해제하고 대기자를 깨우는 구간 | 다음 번호 호출 |
| Remainder Section (나머지 구간) | 공유 자원과 무관한 나머지 코드 | 창구 밖에서 볼일 보기 |
| TSL (Test-and-Set Lock) | TAS 명령어로 구현한 스핀락 | 될 때까지 문고리를 계속 돌려보는 방식 |
| CAS (Compare-And-Swap) | 예상값과 같을 때만 새 값으로 교체하는 원자 명령 | "이 값이 A면 B로 바꿔라"는 조건부 도장 |
| Deadlock (교착 상태) | 서로 상대가 쥔 자원을 기다리며 영원히 멈춤 | 두 사람이 서로 다른 방문 앞에서 상대 열쇠를 기다림 |
| Starvation (기아 상태) | 특정 스레드가 계속 밀려 자원을 못 받음 | 새치기꾼들에 밀려 평생 못 들어가는 사람 |
| Lock Granularity (락 범위) | 하나의 락이 보호하는 데이터 범위의 크기 | 방 전체를 잠그는가, 서랍 하나만 잠그는가 |
| Contention (경합) | 여러 스레드가 동시에 같은 락을 요구하는 정도 | 창구 앞 대기 줄의 길이 |

## 깊이 이해

### 4단계 구조로 본 임계 구역
- 스레드는 `Entry Section`에서 락(또는 flag/turn) 상태를 확인해 진입 자격을 얻고, 얻으면 `Critical Section`에서 공유 데이터를 갱신하고, `Exit Section`에서 락을 풀며 대기 중인 스레드를 깨운다. 락과 무관한 코드는 `Remainder Section`에서 자유롭게 실행된다.
- 이 4단계 중 `Critical Section`만 짧게 유지하면 나머지 3단계는 여러 스레드가 겹쳐 실행할 수 있어 전체 처리량이 올라간다.

### 갱신 손실을 수치로 확인 (Lost Update)
- 계좌 잔액 10,000원에서 스레드 A, B가 각각 3,000원을 동시에 출금한다고 하자. 락이 없으면 둘 다 잔액을 10,000원으로 읽고, 각자 계산한 7,000원을 순서대로 덮어쓴다. 최종 잔액은 7,000원이 되어 원래 4,000원이어야 할 값에서 3,000원이 증발한다.
- Entry Section에서 CAS로 "현재 값이 10,000이면 7,000으로 교체"를 시도하면, 두 번째 스레드는 CAS 실패(예상값 불일치)를 감지해 최신값(7,000)을 다시 읽고 4,000으로 재시도한다 — 증발이 일어나지 않는다.

### 구현 수단 비교 (Peterson → TSL → CAS → mutex)
- Peterson(소프트웨어)은 프로세스 2개, 명령어 재배치가 없는 환경에서만 성립한다.
- TSL(TAS 기반 스핀락)은 락을 얻을 때까지 CPU를 계속 소모하며 반복 검사(Busy Waiting)한다 — 락 보유 시간이 수 마이크로초로 짧을 때만 효율적이다.
- CAS는 "예상값이 맞을 때만 교체"하는 낙관적 방식이라 실패해도 곧바로 재시도할 수 있어 스핀락보다 유연하다.
- mutex/semaphore는 락 획득 실패 시 CPU를 쓰지 않고 대기 큐에서 잠들었다가(Sleep), 락이 풀리면 OS가 깨워준다(Wake) — 락 보유 시간이 길 때(예: I/O 포함) 유리하지만, 잠들고 깨는 데 컨텍스트 스위치 비용(수 마이크로초)이 든다.

### 데드락과 기아의 차이를 수치로 구분
- 데드락 예: 스레드 A가 락1을 잡고 락2를 기다리는 동안, 스레드 B는 락2를 잡고 락1을 기다린다 — 대기 시간이 무한대로 발산하며 둘 다 영원히 멈춘다. 해법은 모든 스레드가 락을 항상 같은 순서(예: 락1 → 락2)로 획득하도록 강제하는 lock ordering이다.
- 기아 예: 대기 큐가 우선순위 기반이라 우선순위 낮은 스레드가 30초 넘게 락을 못 받는 경우다. 데드락과 달리 시스템 전체는 계속 진행되지만 특정 스레드만 손해를 본다. 해법은 대기 시간이 길어질수록 우선순위를 높이는 에이징(Aging)이나 FIFO 대기열이다.

### 락 범위(Granularity)와 경합의 트레이드오프
- 전역 락 1개로 모든 데이터를 보호하면 코드는 단순하지만, 스레드 100개가 동시에 락을 요구하면 대부분이 대기 상태가 되어 경합률(Contention)이 90% 이상으로 치솟는다.
- 데이터를 작은 단위(예: 계좌별 락)로 쪼개면(Fine-grained Lock) 서로 다른 계좌를 다루는 스레드끼리는 대기 없이 병렬 실행되어 경합률이 5% 이하로 떨어진다. 다만 락 개수가 늘어난 만큼 lock ordering을 지키지 않으면 데드락 위험도 함께 커진다.

## 연결 개념
- Race Condition — 임계 구역 미보호로 발생하는 결과 자체 (원인은 이 파일의 Lost Update)
- Atomic Operation — TSL·CAS가 제공하는, 중간 상태가 관찰되지 않는 연산의 성질
- 014_critical_section(같은 폴더) — 그 파일이 3대 조건과 Peterson·SW→HW 진화 원리를 다룬다면, 이 파일은 Entry/Exit 구조와 데드락·기아·락 범위 같은 구현 리스크를 다룬다

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
