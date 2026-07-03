---
title: "다중 프로세서 스케줄링 — SQMS·MQMS (Multiprocessor Scheduling SQMS MQMS)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 30
---

# 📖 【암기용】 개념 완전 이해

> 목적: 다중 프로세서 스케줄링과 SQMS·MQMS를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: SQMS(Single Queue Multiprocessor Scheduling)와 MQMS(Multi Queue Multiprocessor Scheduling)는 다중 CPU 코어 환경에서 실행 가능한 프로세스를 담는 Run Queue를 몇 개 둘지에 대한 두 가지 스케줄러 설계 방식이며, 이 큐 구조 선택이 락 경합·캐시 지역성(Cache Locality)·부하 균형이라는 세 지표를 동시에 좌우한다.
- **왜 필요한가**: 코어 수가 늘어날수록 큐 접근에 걸리는 락 대기 시간과, 프로세스가 실행 코어를 옮길 때 발생하는 캐시·TLB 재적재 비용(Migration Cost)이 시스템 처리량을 갉아먹기 시작한다. 어떤 큐 구조를 쓰느냐에 따라 이 두 비용의 크기가 정반대로 나타난다.
- **핵심 직관**: 큐가 1개면 락 대기가 코어 수에 비례해 커지고, 큐가 코어별이면 락은 사라지지만 대신 큐 사이의 작업 이동(마이그레이션)을 관리하는 로직이 별도로 필요해진다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| Run Queue | 실행 가능 상태 프로세스의 대기열 자료구조 | 번호표 대기열 |
| SQMS | 전역 Run Queue 1개를 모든 코어가 공유 | 창구 여러 개, 대기줄 1개 |
| MQMS | 코어(또는 스케줄링 그룹)마다 독립된 Run Queue | 창구마다 별도 대기줄 |
| Lock Contention(락 경합) | 여러 코어가 동시에 같은 큐 자료구조를 수정하려 할 때 상호배제 락 획득을 놓고 대기하는 현상 | 문이 1개뿐인 창고에 여러 명이 동시에 들어가려는 것 |
| CPU Affinity | 특정 프로세스를 특정 CPU(또는 코어 집합)에 우선 배정하도록 지정하는 속성 | 지정 좌석제 |
| Migration Cost | 프로세스가 실행 코어를 옮길 때 캐시·TLB(주소 변환 캐시)가 비워져 재적재하는 데 드는 비용 | 이사할 때 짐을 다시 푸는 시간 |
| Load Balancer(로드 밸런서) | 코어별 큐 길이를 주기적으로 비교해 불균형 시 프로세스를 이동시키는 스케줄러 서브모듈 | 줄 길이를 보고 손님을 옮겨주는 안내원 |
| sched_domain(스케줄링 도메인) | 리눅스 커널이 SMT-물리코어-패키지(소켓)-NUMA 노드 단계로 코어 근접도를 계층화한 구조 | 팀-부서-본부-지사로 나뉜 조직도 |

## 깊이 이해

### SQMS의 락 경합을 정량적으로 보기
전역 큐 1개를 코어 N개가 동시에 두드리면, 큐 접근이 상호배제(mutual exclusion)로 직렬화되므로 스케줄링 결정 자체의 처리량이 큐 락을 잡고 있는 시간의 역수 수준으로 상한이 걸린다. 코어가 4개면 락을 짧게 잡는 구현에서는 체감 병목이 작지만, 코어가 수십 개로 늘어나면 동시에 스케줄링을 시도하는 코어 수가 늘어 락 대기 행렬이 길어지고 스케줄링 지연(wakeup latency)이 눈에 띄게 악화될 수 있다. SQMS가 소규모 SMP(코어 수 개 이하)에는 적합하지만 대규모 서버에는 쓰이지 않는 이유다.

### MQMS와 CFS의 실제 구현 — Per-CPU Run Queue와 vruntime
리눅스 CFS는 코어마다 Run Queue(`struct rq`)를 두고, 그 안의 실행 가능 프로세스를 vruntime(가상 실행 시간, 실제 실행 시간을 우선순위 가중치로 나눈 값) 순으로 정렬된 레드-블랙 트리에 보관한다. 코어는 자신의 큐에서만 트리를 탐색하므로 다른 코어와 락을 공유하지 않는다. 새 프로세스는 기본적으로 부모가 마지막에 실행된 코어의 큐(또는 상대적으로 한가한 큐)에 놓이고, 이후 실행 코어를 옮기지 않는 한 그 큐에 남는다.

### sched_domain 계층과 로드 밸런싱 주기
리눅스 커널은 코어 근접도를 SMT(같은 물리 코어의 논리 스레드) → MC(같은 소켓의 물리 코어들) → NUMA(코어 소켓 간)의 계층으로 나눈 `sched_domain`을 구성한다. 로드 밸런서는 계층 하위(SMT)일수록 자주(매 스케줄링 틱 또는 코어가 유휴 상태가 되는 즉시), 계층 상위(NUMA)일수록 드물게 균형을 점검한다 — 가까운 코어끼리는 옮겨도 비용이 작지만, NUMA 노드를 넘는 이동은 원격 메모리 접근 지연까지 함께 유발하기 때문에 더 신중하게 판단해야 한다.

### Migration Cost가 발생하는 구체 지점
프로세스가 코어 0에서 코어 1로 옮겨지면 세 가지 비용이 함께 발생한다. ① 코어 0의 L1/L2 캐시에 있던 데이터를 코어 1에서 다시 채워야 하는 캐시 미스 비용, ② TLB(가상-물리 주소 변환 캐시)가 초기화되어 페이지 테이블 워크가 다시 발생하는 비용, ③ NUMA 환경이면 메모리 자체가 이전 코어의 로컬 노드에 남아있어 이후 접근이 전부 원격 접근이 되는 비용. 이 때문에 로드 밸런서는 큐 길이 차이가 일정 임계치를 넘을 때만 마이그레이션을 수행하도록 설계된다 — 사소한 불균형마다 옮기면 마이그레이션 비용이 락 경합 절감 이득을 상쇄하기 때문이다.

### SQMS와 MQMS 중 무엇을 고를까 — 판별 기준
코어 수가 적고(수 개 이하) 워크로드가 짧고 균일하게 도착해 로드 밸런싱이 중요할 때는 SQMS의 단순성과 완벽한 균형이 유리하다. 코어 수가 많고(8개 이상) 워크로드가 캐시 재사용에 민감할 때는 MQMS와 로드 밸런서의 조합이 유리하다. 현대 범용 OS(리눅스, 윈도우)는 사실상 전부 MQMS 계열을 채택하고 있다 — 서버·데스크톱 모두 코어 수가 계속 늘어나는 추세이기 때문이다.

## 연결 개념
- CFS(Completely Fair Scheduler) — MQMS 구조 위에서 vruntime 기반 공정성을 구현하는 리눅스 기본 스케줄러.
- NUMA-aware 스케줄링(031) — `sched_domain`의 NUMA 계층을 활용해 마이그레이션이 원격 메모리 접근을 유발하지 않도록 제약하는 확장.
- CPU Affinity / cpuset — 마이그레이션 범위를 특정 코어 집합으로 제한해 캐시 지역성을 강제로 보존하는 운영 기법.

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: SQMS와 MQMS는 큐 개수 비교가 아니라 lock contention, load balancing, affinity, migration cost 관점에서 판단해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 다중 프로세서 스케줄링은 여러 CPU에 runnable task를 배치하고, 큐 경합과 부하 균형을 조정하는 OS 기능이다.
> 2. **가치**: SQMS는 단순성과 전역 공정성을 제공하고, MQMS는 코어별 큐로 lock contention과 cache miss를 줄인다.
> 3. **판단 포인트**: 코어 수, run queue lock, task affinity, load imbalance, migration cost를 함께 고려해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 멀티코어 스케줄링 이해 확인 | SQMS, MQMS, run queue, load balancing | 단일 CPU 스케줄링 알고리즘만 서술 |
| 성능 병목 분석 확인 | lock contention, cache locality, migration cost | MQMS를 무조건 우위로 단정 |
| 운영 튜닝 판단 확인 | affinity, CPU isolation, scheduler domain | CPU 사용률만 보고 판단 |

> 요약: 이 문제는 큐 구조와 작업 이동 비용을 멀티코어 성능 지표로 연결해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 다중 프로세서 스케줄링은 CPU별 태스크 배치이다.
- 배경: 멀티코어 환경은 ready queue lock 경합, 코어별 부하 불균형, task migration에 따른 cache locality 손실을 만든다.
- 필요성: SQMS와 MQMS는 run queue lock wait, CPU utilization 편차 10% 이하, migration/sec 기준으로 선택해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Runnable Task -> Scheduler
  / SQMS: Global Run Queue -> CPU0 / CPU1 / CPU2
  / MQMS: CPU0 Queue / CPU1 Queue / CPU2 Queue -> Load Balancer
  -> Affinity / Migration Cost -> Dispatch
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Global Run Queue | 모든 CPU가 공유하는 큐 | SQMS, lock contention 가능 |
| Per-CPU Run Queue | CPU별 runnable task 저장 | MQMS, cache locality 유지 |
| Load Balancer | 큐 길이와 부하를 비교해 task 이동 | periodic/idle balancing |
| CPU Affinity | 태스크 실행 CPU 선호도 지정 | cache warmth 유지 |
| Migration Cost | 태스크 이동 시 캐시·TLB 손실 비용 | 과도한 이동 억제 |

> 요약: SQMS는 전역 큐, MQMS는 CPU별 큐와 load balancer를 중심으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Task runnable 전환 -> run queue 삽입 -> CPU 선택
  -> SQMS는 global queue lock 획득
  -> MQMS는 per-CPU queue 선택 / load balance
  -> dispatch -> affinity와 migration cost 갱신
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | I/O 완료 또는 wakeup으로 task runnable 전환 | wakeup latency |
| 2 | SQMS는 전역 큐에 삽입 후 CPU가 dequeue | run queue lock wait |
| 3 | MQMS는 현재 CPU 또는 선호 CPU 큐에 삽입 | per-CPU queue length |
| 4 | load balancer가 불균형 시 task migration | migration count |
| 5 | CPU가 task를 dispatch하고 실행 통계 갱신 | context switch, cache miss |

> 요약: MQMS는 per-CPU 큐로 경합을 줄이고 load balancing으로 불균형을 조정하지만 migration cost를 통제해야 한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | 본 기술 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| SQMS | 단일 전역 큐 | 구현 단순, 전역 공정성 | 코어 수 4개 이하에서 부담 제한 |
| MQMS | CPU별 큐 | lock contention 감소 | 코어 수 8개 이상에서 유리 |
| Load balancing | 주기적 task 이동 | 부하 균형 확보 | imbalance 10% 이하 목표 |
| Affinity | 선호 CPU 유지 | cache locality 보존 | LLC miss rate |

> 요약: 코어 수가 작으면 SQMS 단순성이 장점이고, 코어 수가 커질수록 MQMS의 경합 감소와 affinity 유지가 유효하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | SQMS 전역 큐 | MQMS per-CPU 큐 | 코어 수, run queue lock 경합 |
| 비용/성능 | 큐 경합 증가 | migration과 balancing 비용 | context switch, cache miss |
| 운영/위험 | 자동 스케줄러 기본값 | affinity, CPU set, isolation | 지연 민감 서비스와 배치 분리 |

> 요약: MQMS는 경합 감소 효과와 migration 비용을 함께 비교해 선택해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 큐 경합 | SQMS global lock 집중 | per-CPU queue, lock 분산 | run queue lock wait |
| 부하 불균형 | MQMS 큐 분리로 특정 CPU 집중 | periodic/idle load balancing | CPU utilization 편차 10% 이하 |
| 캐시 손실 | task migration 과다 | affinity, migration threshold | LLC miss rate, migration/sec |

> 요약: 멀티코어 스케줄링 리스크는 큐 경합, 부하 불균형, 캐시 손실이며 각 지표를 동시에 본다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 성능/지연 | wakeup latency p95 1ms 이하 | perf sched, eBPF |
| 품질/균형 | CPU utilization 편차 10% 이하 | mpstat, scheduler trace |
| 운영/자원 | migration/sec 기준선 대비 20% 이내 | perf stat, ftrace |

> 요약: 도입 효과는 wakeup latency, CPU 편차, migration과 cache miss 지표로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 코어 수 8개 이상 서버는 per-CPU run queue 기반 스케줄러를 사용하고 CPU utilization 편차 10% 이하를 목표로 load balancing을 점검한다.
2. 지연 민감 프로세스는 CPU affinity와 cpuset으로 고정하고 배치 작업은 별도 CPU 그룹에 배치한다.
3. perf sched, ftrace, eBPF로 wakeup latency, migration/sec, LLC miss rate를 수집해 migration threshold를 조정한다.

**결론 (2줄):**
- 기술사 판단: 소규모 SMP는 SQMS 단순성이 유효하고, 다코어 서버는 MQMS와 affinity 기반 부하 조정이 적합하다.
- 향후 방향: 스케줄러는 NUMA, 에너지, 캐시 계층을 함께 고려하는 topology-aware scheduling으로 확장된다.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "다중 프로세서 스케줄링을 설명하시오" | SQMS/MQMS 큐 처리 흐름 | 경합·균형·affinity 특징 |
| 요구사항 명시형 | "비교하시오", "개선 방안을 제시하시오" | load balancing과 migration 흐름 | 코어 수별 선택 기준과 지표 |

> 요약: 설명형은 큐 구조와 동작을, 비교형은 lock contention과 migration cost 기준을 중심으로 작성한다.
