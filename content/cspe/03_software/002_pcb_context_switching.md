---
title: "PCB·컨텍스트 스위칭 (PCB Context Switching)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 2
---

# 📖 【암기용】 개념 완전 이해

> 목적: PCB와 컨텍스트 스위칭을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: PCB는 실행 상태 기록표, 컨텍스트 스위칭은 CPU 주인 교체 절차
- **왜 필요한가**: CPU는 한 순간 하나의 실행 흐름만 처리하므로, 운영체제는 현재 상태를 저장하고 다음 상태를 복원해 다중 작업처럼 보이게 한다.
- **핵심 직관**: 책갈피와 작업 일지를 남긴 뒤 다른 책을 펼치는 절차가 컨텍스트 스위칭이다.

## 깊이 이해
- **배경·문제의식**: 시분할 OS는 짧은 time slice마다 실행 주체를 바꾼다. 저장할 정보가 누락되면 명령 위치나 스택이 틀어져 프로세스가 잘못 실행된다.
- **작동 원리**: 커널은 interrupt/trap/timer tick에서 현재 PC, SP, general register, 상태 레지스터, MMU 정보, scheduling metadata를 PCB에 저장한다. 이후 scheduler가 다음 PCB를 고르고 레지스터·주소공간을 복원한다.
- **비유**: 콜센터 상담원이 고객 A의 상담 메모와 화면 상태를 저장하고 고객 B 화면으로 전환하는 과정이다. 메모가 세밀할수록 복귀는 정확하지만 전환 시간은 증가한다.
- **구체 예시**: Linux에서 voluntary/involuntary context switch가 초당 수만 회로 증가하면 cache pollution과 TLB miss가 늘어 p99 latency가 10ms에서 80ms로 튈 수 있다.
- **흔한 오해·주의점**: 컨텍스트 스위칭은 사용자 코드가 처리한 일이 아니다. 전환 시간은 overhead이며, runnable thread가 core 수보다 많으면 처리량보다 지연시간 악화가 먼저 나타난다.

## 연결 개념
- 프로세스 스케줄링: 다음 실행 대상을 고르는 정책
- TLB·Cache: 전환 후 재사용성이 깨지는 하드웨어 상태
- PCB·TCB: 저장 범위가 프로세스와 스레드에서 달라짐

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: PCB 항목 암기가 아니라 CPU 상태 저장·MMU 전환·cache/TLB 영향·scheduler overhead를 연결한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PCB는 프로세스의 CPU·메모리·스케줄링 상태를 저장하는 커널 자료구조이고, 컨텍스트 스위칭은 그 상태를 저장·복원하는 절차이다.
> 2. **가치**: 시분할, preemption, blocking I/O를 가능하게 하지만 전환 중에는 사용자 작업이 진행되지 않는다.
> 3. **판단 포인트**: register 저장 비용보다 TLB flush, cache pollution, run queue 길이, lock contention이 p95 지연을 좌우한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| OS가 실행 상태를 보존하는 방식 확인 | PC, SP, register, state, priority, MMU 정보 | PCB를 단순 ID 목록으로 축소 |
| 스케줄러와 전환 절차 연결 확인 | interrupt -> save -> select -> restore -> return | scheduler 선택과 context switch 분리 누락 |
| 전환 overhead 판단 확인 | TLB flush, cache pollution, kernel/user mode 전환 | 전환 횟수와 latency 영향 누락 |

> 요약: 이 문제는 PCB 구성요소와 스위칭 절차를 성능 지표까지 연결하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: PCB는 실행 문맥 저장 구조이다.
- 배경: 시분할 OS는 timer interrupt, system call, I/O blocking 시점마다 현재 PC·SP·register·MMU 정보를 저장하고 다음 실행 주체를 복원한다.
- 필요성: 컨텍스트 스위칭은 멀티태스킹을 제공하지만 switch/sec, system CPU, p99 latency 기준으로 overhead를 관리해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Running Process -> CPU Context Save -> PCB
PCB -> Scheduler Metadata / MMU Info / Resource Info
Next PCB -> CPU Context Restore -> User Mode Return
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| CPU context | PC, SP, general register, flags 저장 | 명령 재개 위치 보존 |
| Scheduling info | state, priority, vruntime, time slice | run queue 선택 기준 |
| MMU info | page table base, address space id | TLB flush/ASID 영향 |
| Resource info | open file, signal, credential | 권한·자원 추적 |

> 요약: PCB는 CPU 재개 정보와 스케줄링·메모리·자원 정보를 묶어 프로세스 복원을 가능하게 한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Timer/Interrupt/Block 발생 -> Kernel Mode 진입
-> Current Register Save -> Current PCB 갱신
-> Scheduler가 Next PCB 선택 -> MMU/Kernel Stack 전환
-> Next Register Restore -> User Mode 복귀
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | timer interrupt, system call, page fault로 커널 진입 | trap count, interrupt rate |
| 2 | 현재 PC·SP·register를 PCB/커널 스택에 저장 | register corruption 0건 |
| 3 | scheduler가 priority, vruntime, deadline 기준으로 next 선택 | run queue latency |
| 4 | page table base, kernel stack, CPU register 복원 | TLB miss, cache miss |
| 5 | return-from-trap으로 사용자 모드 재개 | context switch/sec |

> 요약: 컨텍스트 스위칭은 인터럽트 진입부터 사용자 모드 복귀까지의 저장·선택·복원 연속 절차이다.

---

## Ⅳ. 특징

| 구분 | Thread Switch | Process Switch | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 주소공간 | 동일 page table 가능 | page table 변경 가능 | ASID/PCID 없으면 TLB flush |
| 저장 범위 | register, stack, TCB 중심 | PCB, MMU, resource 영향 | us 단위 overhead |
| cache 영향 | working set 유사 시 낮음 | working set 변경으로 miss 증가 | LLC miss, branch predictor 영향 |
| 발생 조건 | lock wait, yield, time slice | fork/exec, blocking I/O, preemption | voluntary/involuntary 구분 |

> 요약: 프로세스 전환은 메모리 주소공간 전환 때문에 스레드 전환보다 TLB·cache 비용이 커질 수 있다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 협력형 스케줄링 | 선점형 context switch | 응답시간 보장 필요 여부 |
| 비용/성능 | 긴 time slice | 짧은 time slice | interactive p95 vs switch/sec |
| 운영/위험 | thread 과다 생성 | pool과 affinity 제어 | run queue/core 1~2 |

> 요약: time slice가 짧으면 응답성은 개선되지만 switch/sec 증가로 CPU 유효 작업 시간이 감소한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| switch storm | thread 수가 core 수 초과 | thread pool 제한, async I/O | context switch/sec |
| TLB miss 증가 | process address space 빈번 전환 | CPU affinity, PCID/ASID 활용 | dTLB-load-misses |
| cache pollution | working set 다른 task 교대 | workload pinning, batch size 조정 | LLC-load-misses |

> 요약: 전환 overhead는 thread 수 제한, affinity, hardware counter 측정으로 줄인다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 전환 횟수 | 서비스 기준선 대비 20% 이내 증가 | vmstat, pidstat -w |
| 지연시간 | p99 latency SLO 초과율 1% 이하 | APM, eBPF tracing |
| CPU overhead | system CPU 30% 이하 | perf stat, top |

> 요약: 컨텍스트 스위칭은 switch/sec, p99 latency, system CPU를 함께 봐야 병목 판단이 가능하다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. thread pool을 CPU core 수와 blocking ratio 기준으로 산정하고, runnable thread/core 2 이하 유지
2. eBPF/perf로 context-switch, sched:sched_switch, dTLB miss를 수집해 전환 원인을 syscall·lock·I/O로 분류
3. CPU affinity와 NUMA binding으로 cache locality를 보존하고, 비동기 I/O로 blocking wakeup 횟수 감소

**결론 (2줄):**
- 기술사 판단: 응답시간 목표가 엄격하면 선점 스케줄링을 쓰되 switch/sec와 system CPU 상한을 함께 둔다
- 향후 방향: Linux CFS, io_uring, user-level thread는 전환 경로를 줄이는 방향으로 발전하며, 관측성 기반 튜닝이 필수임

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "PCB와 컨텍스트 스위칭을 설명하시오" | 저장·선택·복원 단계 | PCB 구성요소와 overhead |
| 요구사항 명시형 | "오버헤드 저감 방안을 제시하시오" | 발생 지점별 측정 흐름 | TLB·cache·run queue별 대응 |

> 요약: 설명형은 절차를, 방안형은 전환 횟수와 하드웨어 부작용을 중심으로 목차를 전환한다.
