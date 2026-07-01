---
title: "스핀락 vs 뮤텍스 (Spinlock vs Mutex)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 13
---

# 📖 【암기용】 개념 완전 이해

> 목적: 스핀락과 뮤텍스를 처음 봐도 CPU 사용 방식과 임계 구역 길이 관점에서 구분하게 만든다. 시험 답안 양식이 아니라, 잠금 대기 비용을 직관적으로 설명한다.

## 한눈에
- **개요**: 스핀락은 CPU를 점유한 채 잠금 해제를 반복 확인하고, 뮤텍스는 잠금이 없을 때까지 잠들어 대기한다.
- **왜 필요한가**: 잠금 대기 방식은 응답시간과 CPU 사용률을 직접 바꾼다. 짧은 커널 임계 구역에는 스핀락, 긴 사용자 영역 대기에는 뮤텍스가 맞다.
- **핵심 직관**: 문 앞에서 계속 손잡이를 돌려보는 방식이 스핀락, 번호표를 받고 의자에 앉아 기다리는 방식이 뮤텍스다.

## 깊이 이해
- **배경·문제의식**: 잠금이 이미 잡혀 있을 때 대기 스레드는 두 선택지를 가진다. 계속 CPU를 쓰며 확인하거나, 커널에 넘겨 sleep 상태가 된다.
- **작동 원리**: 스핀락은 atomic test-and-set 또는 compare-and-swap으로 lock word를 반복 검사한다. 뮤텍스는 실패 시 wait queue에 들어가고 scheduler가 다른 스레드를 실행한다.
- **비유**: 1초 안에 열릴 문이면 서서 기다리는 편이 이동 비용을 줄인다. 10분 뒤 열릴 문이면 대기실로 가서 다른 일을 배정받는 편이 CPU 낭비를 막는다.
- **구체 예시**: critical section 2us, context switch 3~10us이면 spinlock이 유리하다. critical section 1ms이면 spin 대기 동안 CPU 1코어가 100% 소모된다.
- **흔한 오해·주의점**: 단일 코어에서 preemption이 켜진 상태의 스핀락은 owner가 CPU를 못 받아 해제할 수 없으므로 커널은 interrupt/preemption 제어와 함께 사용한다.

## 연결 개념
- Busy Waiting — CPU를 점유한 채 조건을 반복 확인하는 대기 방식
- Context Switch — 뮤텍스 대기 전환의 주요 비용
- Multicore Kernel — 스핀락이 의미를 갖는 대표 환경

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: busy waiting과 sleep의 차이를 CPU 낭비가 아니라 critical section 길이, preemption, multicore 조건으로 판단한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스핀락은 busy waiting 기반 잠금, 뮤텍스는 blocking 기반 잠금으로 대기 중 CPU 사용 방식이 다르다.
> 2. **가치**: 임계 구역이 context switch 비용보다 짧으면 스핀락, 길거나 I/O를 포함하면 뮤텍스가 CPU 낭비를 줄인다.
> 3. **판단 포인트**: critical section 길이, 코어 수, preemption/interrupt 상태, 커널·사용자 영역 여부로 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 잠금 대기 비용 이해 확인 | busy waiting vs sleep, context switch 비용 | 스핀락을 무조건 나쁜 방식으로 단정하지 않음 |
| 커널 동시성 판단 확인 | interrupt disable, preemption disable, SMP | 단일 코어 조건 누락 |
| 적용 기준 제시 확인 | 임계 구역 10us 이하, I/O 포함 여부 | 장시간 lock 보유에 spinlock 적용 지양 |

> 요약: 이 문제는 lock 종류 암기가 아니라 대기 비용과 CPU 스케줄링 조건을 함께 보는 선택 문제다.

---

## Ⅰ. 개요 및 필요성

스핀락과 뮤텍스는 임계 구역을 보호하는 잠금 방식이다. 차이는 잠금 실패 시 CPU를 계속 쓰는지, sleep 상태로 전환하는지에 있다. 멀티코어 커널과 사용자 스레드 환경은 대기 비용 구조가 다르므로 선택 기준이 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
Thread -> Lock Request -> Lock Word
       / Spinlock: CAS loop -> Busy Wait -> Acquire
       / Mutex: Futex/Kernel Queue -> Sleep -> Wakeup -> Acquire
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Lock Word | 잠금 상태를 원자적으로 표시 | CAS, test-and-set 사용 |
| Spin Loop | 잠금 해제까지 반복 확인 | CPU 1코어 점유 가능 |
| Wait Queue | 뮤텍스 대기 스레드 보관 | scheduler wakeup 필요 |

> 요약: 스핀락은 lock word를 반복 검사하고, 뮤텍스는 wait queue와 scheduler를 이용해 CPU를 다른 작업에 넘긴다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Acquire Attempt -> Atomic CAS
  / Success -> Critical Section -> Release
  / Fail + Short CS -> Spin Retry -> Acquire
  / Fail + Long CS -> Sleep Queue -> Wakeup -> Acquire
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | atomic 연산으로 lock 획득 시도 | CAS success rate |
| 2 | 실패 시 대기 방식 결정 | critical section p95 |
| 3 | 스핀 또는 sleep 대기 수행 | CPU utilization, wait time |
| 4 | release 후 owner 전환 | lock handoff latency |

> 요약: 잠금 실패 후 임계 구역 길이와 context switch 비용을 비교해 spin 또는 blocking 경로를 선택한다.

---

## Ⅳ. 특징

| 구분 | Spinlock | Mutex | 수치·판단 기준 |
|:---|:---|:---|:---|
| 대기 방식 | busy waiting | sleep/blocking | CS 10us 이하이면 spin 검토 |
| CPU 사용 | 대기 중 코어 점유 | 다른 스레드 실행 가능 | CPU steal 0, run queue 관측 |
| 적용 영역 | SMP kernel, interrupt context | user thread, 긴 임계 구역 | I/O 포함 시 mutex |

> 요약: 스핀락은 짧은 커널 임계 구역의 wakeup 비용을 없애고, 뮤텍스는 긴 대기에서 CPU 소모를 줄인다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | sleep 전용 mutex | spin 또는 adaptive mutex | CS p95가 context switch보다 짧음 |
| 비용/성능 | context switch 3~10us | spin wait 1~5us 목표 | lock hold p95 10us 이하 |
| 운영/위험 | CPU 소모 낮음 | lock convoy, starvation 가능 | contention 5% 이하 유지 |

> 요약: adaptive mutex는 짧게 스핀한 뒤 sleep으로 전환해 두 방식의 비용 경계를 완화한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| CPU 소모 폭증 | 긴 임계 구역에서 spin 지속 | spin count 제한, mutex 전환 | CPU utilization 90% 이상 경보 |
| Preemption Deadlock | owner가 CPU를 잃고 waiter가 spin | preemption disable, per-CPU lock | owner running 여부 |
| Lock Convoy | 여러 스레드가 같은 lock 대기 | lock striping, sharding | contention ratio, wait p99 |

> 요약: 스핀락은 preemption 제어와 spin 상한이 없으면 CPU 소모와 진행 지연을 만든다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Lock Hold Time | p95 10us 이하 | ftrace, eBPF lock histogram |
| Contention | lock contention 5% 이하 | perf lock report |
| CPU 영향 | spin CPU time 3% 이하 | CPU profile, scheduler trace |

> 요약: lock hold time, contention, spin CPU time을 함께 측정해야 잠금 방식 선택을 검증할 수 있다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 커널의 짧은 자료구조 갱신은 spinlock을 적용하고 lock hold p95를 10us 이하로 유지함.
2. 사용자 영역 파일 I/O, 네트워크 I/O, 조건 대기는 mutex 또는 condition variable로 전환해 sleep 대기를 사용함.
3. 경합이 5%를 넘는 공유 구조는 lock striping, per-CPU data, RCU를 적용해 단일 lock 병목을 분산함.

**결론 (2줄):**
- 기술사 판단: CS 길이가 context switch 비용보다 짧고 owner가 다른 코어에서 실행 중이면 spinlock, 그 외에는 mutex 선택이 타당함.
- 향후 방향: 커널은 adaptive spinning과 lock contention tracing으로 workload별 대기 경로를 동적으로 조정함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "스핀락과 뮤텍스를 설명하시오" | CAS, busy wait, sleep queue 흐름 | CPU 사용 방식과 적용 영역 차이 |
| 요구사항 명시형 | "비교하시오", "선택 기준을 제시하시오" | CS 길이와 context switch 비용 비교 | SMP kernel, I/O 포함 여부, p95 지표 |

> 요약: 비교형은 스핀 여부가 아니라 critical section 시간과 preemption 조건을 기준으로 답안을 구성한다.
