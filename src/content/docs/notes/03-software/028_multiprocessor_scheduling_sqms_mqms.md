---
sidebar:
  order: 28
  label: "028. 다중 프로세서 스케줄링: SQMS•MQMS (Multiprocessor Scheduling SQMS MQMS)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "다중 프로세서 스케줄링: SQMS•MQMS (Multiprocessor Scheduling SQMS MQMS)"
date: "2026-08-13T14:09:00+09:00"
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
- 배경/필요성: 코어 증가 시 전역 큐 **락 경합** 또는 로컬 큐 편차 발생

#### 한줄 요약

- 전역 큐 경합과 로컬 큐 편차를 조정하는 다중 프로세서 스케줄링이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Cache Affinity (캐시 친화도)**: 특정 프로세스를 이전에 실행되었던 동일 CPU 코어에 계속 할당함으로써 L1/L2 캐시 적중률(Cache Hit)을 극대화하는 성질.
- **Work Stealing (작업 훔치기)**: MQMS 환경에서 특정 유휴 코어가 자신의 로컬 큐가 빌 경우, 분주한 타 코어의 로컬 큐 꼬리(Tail)에서 작업을 훔쳐와 부하를 분산하는 기법.

</details>

- 단일 중앙 큐를 공유해 작업 선택 범위를 통합하는 **SQMS**
- 코어별 큐로 경합을 줄이고 **Cache Affinity**를 높이는 MQMS
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

| 구성요소 | 책임 |
|:---|:---|
| 작업 배치기 | 신규 작업의 전역•로컬 큐 위치 결정 |
| 전역 실행 큐 | 모든 코어가 공유하는 **SQMS** 준비 작업 보관 |
| 코어별 로컬 실행 큐 | 코어별 **MQMS** 작업과 캐시 지역성 유지 |
| CPU 코어 집합 | 큐에서 선택한 작업 실행 |
| 부하 분산기 | 로컬 큐 편차를 감지해 작업 이동 |

#### 한줄 요약

- 작업 배치기, CPU 친화도, 부하 분산기가 작업 위치를 조정한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Push/Pull Migration**: 주기적으로 과부하 코어가 타 코어로 작업을 밀어내거나(Push), 유휴 코어가 타 큐의 작업을 당겨오는(Pull) 부하 재조정 메커니즘.

</details>

```text
SQMS 실행 경로

[준비 작업] ──► [전역 실행 큐] ──► [1. SQMS 전역 디스패치] ──► [작업 실행]

MQMS 실행 경로

[준비 작업] ──► [로컬 실행 큐] ──► [2. MQMS 로컬 디스패치] ──► [편차 탐지] ──► [3. 작업 훔치기]
```

### 동작 원리

1. **SQMS 전역 디스패치**: 공유 큐에서 작업을 선택해 유휴 코어에 배정
2. **MQMS 로컬 디스패치**: 각 코어가 자신의 로컬 큐에서 작업 선택
3. **작업 훔치기**: 유휴 코어가 다른 로컬 큐의 작업을 이동

#### 한줄 요약

- SQMS는 SQMS 전역 디스패치, MQMS는 MQMS 로컬 디스패치와 작업 이동이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Linux CFS Multi-Queue**: Linux 커널의 Completely Fair Scheduler가 코어별 `cfs_rq` 로컬 큐를 운영하고 `load_balance()` 함수로 주기적 Work Stealing을 수행하는 방식.

</details>

| 기능 비교 | SQMS 구조 | MQMS 구조 |
|:---|:---|:---|
| 확장성 | 코어 증가 시 공유 큐 경합 가능 | 로컬 큐로 경합 분산 가능 |
| 런타임 비용 | 전역 큐 동기화 비용 | 부하 측정과 **작업 이동** 비용 |
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
| NUMA 경계를 넘는 작업 이동의 원격 접근 | **NUMA-aware sched_domain** 계층 적용 | 원격 메모리 접근 빈도 감소 |

> 사례: Linux 커널 **CFS `cfs_rq`** 기반 코어별 MQMS 스케줄링 및 **NUMA Domain** 밸런싱

#### 한줄 요약

- 작업 이동 비용, 이동 임계값, 공정성을 함께 조정한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **멀티프로세서 스케줄링 선택 기준(Multiprocessor Scheduling Criteria)**: 물리 코어 개수, 캐시 적중률 요구 및 NUMA 토폴로지에 기반한 선택 체계.

</details>

- 소수 코어•단순성은 **SQMS**, 확장성•지역성은 **MQMS** 선택

#### 한줄 요약

- 전역 경합과 로컬 편차 중 더 큰 비용을 줄이는 것이 핵심이다.
