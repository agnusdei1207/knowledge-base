---
title: "다중프로그래밍·다중처리 (Multiprogramming Multiprocessing)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 19
---

# 📖 【암기용】 개념 완전 이해

> 목적: 다중프로그래밍과 다중처리를 처음 봐도 concurrency와 parallelism의 차이로 이해하게 만든다. 시험 답안 양식이 아니라, CPU 활용과 코어 병렬 실행 원리를 설명한다.

## 한눈에
- **개요**: 다중프로그래밍은 한 CPU에서 여러 프로그램을 번갈아 실행해 CPU idle을 줄이고, 다중처리는 여러 CPU/코어에서 동시에 실행한다.
- **왜 필요한가**: I/O 대기 중 CPU가 놀면 처리량이 줄어든다. 코어가 여러 개면 작업을 실제 병렬로 나누어 throughput과 응답성을 높일 수 있다.
- **핵심 직관**: 한 명의 요리사가 여러 냄비를 번갈아 보는 것이 다중프로그래밍, 여러 요리사가 동시에 조리하는 것이 다중처리다.

## 깊이 이해
- **배경·문제의식**: 초기 batch 시스템은 한 작업이 I/O를 기다리면 CPU가 idle 상태가 됐다. OS는 ready queue와 context switch로 다른 작업을 실행해 CPU utilization을 높였다.
- **작동 원리**: 다중프로그래밍은 time sharing과 context switch로 동시성을 제공한다. 다중처리는 SMP 또는 NUMA 구조에서 여러 run queue, cache coherence, load balancing을 통해 병렬성을 제공한다.
- **비유**: 콜센터 상담원 한 명이 여러 고객을 보류 전환하며 처리하는 방식과, 상담원 여러 명이 각 고객을 동시에 처리하는 방식의 차이다.
- **구체 예시**: 단일 코어에서 10개 프로세스는 context switch로 번갈아 실행된다. 8코어 SMP에서는 최대 8개 실행 흐름이 같은 시각에 running 상태가 될 수 있다.
- **흔한 오해·주의점**: 다중프로그래밍은 병렬 실행이 아니다. 동시에 진행되는 것처럼 보이지만 단일 코어에서는 한 시각에 하나만 실행된다.

## 연결 개념
- Concurrency vs Parallelism — 동시 진행 구조와 실제 동시 실행의 차이
- Context Switch — 다중프로그래밍의 CPU 전환 비용
- SMP/NUMA — 다중처리 시스템의 대표 구조

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 다중프로그래밍과 다중처리는 CPU utilization 개선과 parallelism 확장의 차이를 명확히 비교한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 다중프로그래밍은 여러 작업을 메모리에 올려 CPU를 교대 사용하고, 다중처리는 여러 CPU/코어가 작업을 실제 병렬 실행하는 구조다.
> 2. **가치**: 전자는 I/O 대기 은폐로 CPU utilization을 높이고, 후자는 코어 수에 따라 처리량을 확장한다.
> 3. **판단 포인트**: concurrency vs parallelism, context switch 비용, SMP/NUMA 메모리 접근 비용을 구분해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| OS 실행 모델 구분 확인 | 다중프로그래밍, 다중처리, time sharing | 두 용어를 동일 의미로 쓰지 않음 |
| CPU/메모리 trade-off 판단 | context switch, cache coherence, NUMA latency | 코어 수 증가를 선형 처리량으로 단정하지 않음 |
| 스케줄링 연결 확인 | ready queue, load balancing, affinity | I/O 대기 은폐 효과 누락하지 않음 |

> 요약: 이 문제는 동시성과 병렬성을 구분하고 CPU 활용률과 코어 확장의 비용을 설명하는지 확인한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 다중프로그래밍은 교대 실행, 다중처리는 병렬 실행이다.
- 배경: I/O 대기 중 CPU가 idle 상태가 되면 처리량이 제한되고, 멀티코어에서는 run queue와 cache coherence 비용까지 고려해야 한다.
- 필요성: OS는 CPU utilization 70~85%, context switch overhead 5% 이하, throughput scaling 기준으로 동시성과 병렬성을 결합한다.

---

## Ⅱ. 구조 및 구성요소

```text
Jobs / Processes -> Ready Queue -> Scheduler
       / Multiprogramming: Context Switch -> Single CPU Time Slice
       / Multiprocessing: Load Balancer -> CPU0 / CPU1 / CPU2 / CPU3
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Ready Queue | 실행 대기 작업 관리 | 단일 큐 또는 per-CPU queue |
| Context Switch | CPU를 다른 프로세스에 넘김 | 레지스터, PC, TLB 영향 |
| Load Balancer | 코어별 작업 분산 | affinity, NUMA locality 고려 |

> 요약: 다중프로그래밍은 큐와 context switch, 다중처리는 코어별 큐와 load balancing이 중심이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Job Arrival -> Memory Admission -> Ready Queue
  -> Scheduler Select
  / Single CPU -> Time Slice -> Context Switch
  / Multi CPU -> Core Assignment -> Parallel Run
  -> I/O Wait / Completion -> Queue Update
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 작업을 메모리와 ready queue에 적재 | DOP, memory pressure |
| 2 | 스케줄러가 실행 대상 선택 | run queue length |
| 3 | 단일 CPU는 time slice마다 전환 | context switch/sec |
| 4 | 다중 CPU는 코어별 병렬 실행 | CPU utilization per core |

> 요약: 다중프로그래밍은 대기시간 은폐, 다중처리는 실제 병렬 실행으로 CPU 자원을 활용한다.

---

## Ⅳ. 특징

| 구분 | Multiprogramming | Multiprocessing | 수치·판단 기준 |
|:---|:---|:---|:---|
| 실행 의미 | concurrency | parallelism | running thread 수 <= core 수 |
| 주요 목적 | CPU idle 감소 | 처리량 확장 | CPU utilization 70% 이상 |
| 비용 | context switch, memory pressure | cache coherence, NUMA latency | context switch 10만/sec 경보 |
| 한계 | thrashing 가능 | Amdahl 한계 | parallel fraction 측정 |

> 요약: 다중프로그래밍은 CPU 대기 은폐, 다중처리는 코어 병렬성 활용이라는 목적이 다르다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 작업 batch | 다중 작업·다중 코어 | I/O wait와 CPU core 수 |
| 비용/성능 | idle CPU 발생 | switch 비용·coherence 비용 | CPU utilization과 throughput |
| 운영/위험 | 단순 운영 | thrashing, lock contention | DOP와 core affinity 조절 |

> 요약: 동시 실행 수는 CPU와 메모리 모두를 기준으로 정해야 하며, core 수만으로 판단하지 않는다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Context Switch 폭증 | time slice 과소, thread 과다 | thread pool 크기 제한 | context switch/sec |
| Thrashing | DOP가 메모리 초과 | admission control, WSS 관리 | major fault/sec |
| NUMA Penalty | 원격 메모리 접근 | CPU affinity, memory binding | remote memory access |

> 요약: 다중 실행 리스크는 switch, memory, NUMA 비용으로 나타나며 각각의 지표로 제어한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| CPU 활용 | per-core utilization 70~85% | mpstat, perf |
| 전환 비용 | context switch overhead 5% 이하 | perf sched, pidstat |
| 병렬 확장 | throughput scaling 0.7 이상 | benchmark, Amdahl 분석 |

> 요약: 활용률, 전환 비용, 병렬 확장률을 함께 봐야 다중프로그래밍과 다중처리 효과를 검증할 수 있다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. I/O bound 서비스는 thread pool 크기를 core 수보다 크게 두되 context switch overhead 5% 이하로 제한함.
2. CPU bound 서비스는 worker 수를 physical core 수 또는 core 수의 1~1.5배로 제한해 run queue 과다를 방지함.
3. NUMA 서버는 CPU affinity와 memory binding을 적용해 remote memory access와 cache miss를 줄임.

**결론 (2줄):**
- 기술사 판단: I/O 대기 은폐 목적이면 다중프로그래밍, 계산 처리량 확장 목적이면 다중처리와 병렬 알고리즘이 필요함.
- 향후 방향: 컨테이너·가상화 환경은 CPU quota, cpuset, NUMA policy를 함께 설계해 CPU quota 초과 시 throttle, cpuset binding으로 코어 간 간섭을 제거함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "다중프로그래밍과 다중처리를 설명하시오" | ready queue, time slice, core assignment 흐름 | concurrency와 parallelism 비교 |
| 요구사항 명시형 | "비교하시오", "운영 방안을 제시하시오" | context switch와 load balancing 진단 | DOP, thread pool, NUMA 선택 기준 |

> 요약: 비교형은 CPU 활용률만이 아니라 context switch, memory pressure, NUMA 비용을 포함해야 한다.
