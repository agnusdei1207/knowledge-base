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
- **개요**: 여러 CPU 코어에 실행 가능한 작업을 배치하고 이동시키는 OS 스케줄링 방식
- **왜 필요한가**: 단일 코어에서는 다음에 실행할 프로세스만 고르면 됐지만, 멀티코어에서는 어느 코어에서 실행할지, 큐를 하나로 둘지, 코어별로 둘지, 작업 이동 비용을 고려해야 한다.
- **핵심 직관**: 계산대를 하나로 줄 세우는 방식(SQMS)과 계산대마다 줄을 따로 두는 방식(MQMS)의 차이이다.

## 깊이 이해
- **배경·문제의식**: 코어 수가 늘면 단일 run queue에 대한 lock contention이 증가한다. 반대로 코어별 큐를 두면 경합은 줄지만 어떤 코어는 바쁘고 다른 코어는 쉬는 load imbalance가 생길 수 있다.
- **작동 원리**: SQMS(Single Queue Multiprocessor Scheduling)는 모든 CPU가 하나의 전역 ready queue에서 작업을 가져간다. MQMS(Multi Queue Multiprocessor Scheduling)는 CPU별 또는 CPU 그룹별 run queue를 두고 주기적으로 load balancing과 task migration을 수행한다.
- **비유**: SQMS는 은행 번호표 1개로 모든 창구가 손님을 부르는 방식이다. MQMS는 창구별 줄이 따로 있고, 한 줄이 길어지면 안내원이 손님을 다른 줄로 옮기는 방식이다.
- **구체 예시**: Linux CFS는 CPU별 run queue를 사용하고 scheduler domain을 기준으로 load balancing을 수행한다. task migration은 cache locality 손실을 유발하므로 migration cost를 고려한다.
- **흔한 오해·주의점**: 부하 균등만 추구하면 캐시 적중률이 떨어진다. CPU affinity와 migration cost를 함께 고려해야 처리량과 지연시간이 균형을 이룬다.

## 연결 개념
- Run Queue — 실행 가능한 태스크를 담는 스케줄링 큐
- CPU Affinity — 특정 태스크를 특정 CPU에 붙여 캐시 locality를 유지하는 기법
- Load Balancing — 코어별 부하 불균형을 줄이는 작업 이동

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

다중 프로세서 스케줄링은 여러 CPU에 태스크를 배치하는 기법이다. 멀티코어 환경에서는 ready queue 접근 경합, 코어별 부하 불균형, 캐시 locality 손실이 발생한다. SQMS와 MQMS는 run queue 구조에 따라 공정성, 경합, 이동 비용이 달라진다.

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
