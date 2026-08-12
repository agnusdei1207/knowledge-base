---
sidebar:
  order: 28
  label: "028. 다중 프로세서 스케줄링: SQMS•MQMS (Multiprocessor Scheduling SQMS MQMS)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "다중 프로세서 스케줄링: SQMS•MQMS (Multiprocessor Scheduling SQMS MQMS)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 28
extra:
  question_no: "028"
  source_status: "기출"
  source_history: "129회"
  priority: 50
  priority_note: "129회 기출, 다중 큐•부하분산 스케줄링"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Multiprocessor Scheduling**: 멀티코어/다중 CPU 환경에서 여러 개의 CPU 코어들에게 작업(Process/Thread)을 효율적으로 배분하고, 캐시 친화도(Cache Affinity) 및 부하 불균형(Load Imbalance)을 제어하는 스케줄링.
- **SQMS (Single Queue Multiprocessor Scheduling)**: 하나의 중앙 전역 실행 큐(Global Run-Queue)를 두고 모든 CPU 코어가 이 큐에서 작업을 꺼내어 디스패치하는 스케줄링 방식.
- **MQMS (Multi-Queue Multiprocessor Scheduling)**: CPU 코어마다 독립된 로컬 실행 큐(Per-CPU Local Run-Queue)를 두고 각 코어가 자신의 큐에서만 작업을 가져가는 스케줄링 방식.

</details>

- 정의/개념: 멀티코어 환경에서 락 경합(Lock Contention) 및 캐시 친화도(Cache Affinity)를 조율하기 위한 스케줄링 아키텍처 2대 분류인 **SQMS vs MQMS**
- 배경/필요성: 단일 큐(SQMS)의 락 억세스 병목 및 Cache Bouncing 문제 해결, 다중 큐(MQMS)의 코어 간 부하 불균형(Work Load Imbalance) 극복 요구성

#### 한줄 요약

- 전역 큐 경합과 로컬 큐 편차를 조정하는 다중 프로세서 스케줄링이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Cache Affinity (캐시 친화도)**: 특정 프로세스를 이전에 실행되었던 동일 CPU 코어에 계속 할당함으로써 L1/L2 캐시 적중률(Cache Hit)을 극대화하는 성질.
- **Work Stealing (작업 훔치기)**: MQMS 환경에서 특정 유휴 코어가 자신의 로컬 큐가 빌 경우, 분주한 타 코어의 로컬 큐 꼬리(Tail)에서 작업을 훔쳐와 부하를 분산하는 기법.

</details>

- 단일 중앙 큐 관리로 부하 평형(Load Balance) 자동 보장 (**SQMS**)
- 코어별 독립 큐 분리로 락 경합 0% 및 **Cache Affinity** 극대화 (**MQMS**)
- MQMS 부하 편차 극복을 위한 **Work Stealing / Push-Pull Migration** 인가

#### 한줄 요약

- SQMS의 경합과 MQMS의 지역성•부하 편차 사이 절충이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Lock Contention**: SQMS 환경에서 수십~수백 개의 CPU 코어가 단일 Global Run-Queue의 락을 획득하기 위해 동시에 경합할 때 유발되는 대규모 성능 병목.

</details>

```text
                  [작업 배치기]
                    /         \
          [전역 실행 큐]   [코어별 로컬 실행 큐]
                    \         /          |
                  [CPU 코어 집합]   [부하 분산기]
```

선의 의미: SQMS는 단일 전역 실행 큐가 모든 코어에 바인딩되고, MQMS는 각 코어가 로컬 큐에 직결되어 부하 분산기가 이동 제어하는 아키텍처.

| 구분 항목 | SQMS (Single Queue) | MQMS (Multi-Queue) |
|:---|:---|:---|
| 큐 구성 | **단일 전역 큐 (Global Run-Queue)** | **코어별 독립 로컬 큐 (Per-CPU Local Queue)** |
| 락 경합 (Lock Contention) | 매우 심함 (코어 수 비례 락 병목 폭증) | **없음 (코어 간 락 공유 없음)** |
| 캐시 친화도 (Cache Affinity) | 낮음 (프로세스가 코어를 무작위 이동) | **매우 높음 (동일 코어 지속 할당)** |
| 부하 균형 (Load Balance) | 완벽함 (자연스러운 큐 공유) | 불균형 가능성 존재 (**Work Stealing 필수**) |
| 현대 OS 채택 | 초기 OS 및 소형 시스템 | **현대 범용 OS (Linux CFS, Windows, FreeBSD)** |

#### 한줄 요약

- 작업 배치기, CPU 친화도, 부하 분산기가 작업 위치를 조정한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Push/Pull Migration**: 주기적으로 과부하 코어가 타 코어로 작업을 밀어내거나(Push), 유휴 코어가 타 큐의 작업을 당겨오는(Pull) 부하 재조정 메커니즘.

</details>

```text
SQMS 실행 경로

[준비 작업] ──► [전역 실행 큐 (Global Lock)] ──► [SQMS 전역 디스패치] ──► [전역 큐 락 경합]

MQMS 실행 경로

[준비 작업] ──► [로컬 큐 (Per-CPU Lock)] ──► [MQMS 로컬 디스패치] ──► [부하 불균형 탐지] ──► [Work Stealing]
```

### 동작 원리

1. **SQMS 경로**: 프로세스가 Global Run-Queue에 진입 시 락 획득 $\to$ 코어 1~N 이 락 경쟁을 거쳐 디스패치 (코어 확장에 따른 락 병목).
2. **MQMS 경로**: 프로세스가 특정 CPU의 Local Queue로 인입 $\to$ 해당 코어가 락 경합 없이 $O(1)$ 초고속 디스패치 연산.
3. **Work Stealing**: Local Queue가 비어있는 유휴 코어 발생 시 **Work Stealing** 알고리즘 발동 $\to$ 타 큐의 작업을 훔쳐와 균형(Rebalance) 수습.

#### 한줄 요약

- SQMS는 SQMS 전역 디스패치, MQMS는 MQMS 로컬 디스패치와 작업 이동이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Linux CFS Multi-Queue**: Linux 커널의 Completely Fair Scheduler가 코어별 `cfs_rq` 로컬 큐를 운영하고 `load_balance()` 함수로 주기적 Work Stealing을 수행하는 방식.

</details>

| 기능 비교 | SQMS 구조 | MQMS 구조 |
|:---|:---|:---|
| 확장성 (Scalability) | 코어 수 8개 이상 확장 시 성능 급락 | **수천 코어 이상 수평적 확장 가능** |
| 런타임 오버헤드 | 매 디스패치마다 전역 락 획득 오버헤드 | 평시 0%, **Work Stealing 발생 시에만 오버헤드** |
| 구현 복잡도 | 비교적 단순함 | 복잡함 (Work Stealing, Migration 튜닝 필요) |

#### 한줄 요약

- 자연 분산은 SQMS, 캐시 지역성은 MQMS가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Affinity Mask (taskset)**: 특정 프로세스를 지정된 CPU 코어 집합에 강제 고정하여 타 코어로의 Migration을 금지시키는 커널 설정.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| MQMS 환경에서 특정 코어에만 작업이 몰려 **Load Imbalance** 유발 | **Work Stealing** 및 주기적 **`sched_balance_domains`** 인가 | 전체 코어 가용률 평형화 |
| 코어 간 무분별한 Thread Migration으로 인한 **Cache Affinity** 파괴 | **`sched_setaffinity` (taskset)** 기반 CPU Pinning 적용 | L1/L2 캐시 히트율 극대화 |
| NUMA 노드 경계를 넘어서는 작업 이동 시 메모리 억세스 지연 | **NUMA-aware MQMS (sched_domain)** 계층화 적용 | 원격 메모리 억세스 병목 소멸 |

> 사례: Linux 커널 **CFS `cfs_rq`** 기반 코어별 MQMS 스케줄링 및 **NUMA Domain** 밸런싱

#### 한줄 요약

- 작업 이동 비용, 이동 임계값, 공정성을 함께 조정한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **멀티프로세서 스케줄링 선택 기준(Multiprocessor Scheduling Criteria)**: 물리 코어 개수, 캐시 적중률 요구 및 NUMA 토폴로지에 기반한 선택 체계.

</details>

- **멀티프로세서 스케줄링 선택 기준**에 따라 현대 대규모 멀티코어 서버 OS 인프라에는 **MQMS + Work Stealing** 구조 전면 채택

#### 한줄 요약

- 전역 경합과 로컬 편차 중 더 큰 비용을 줄이는 것이 핵심이다.
