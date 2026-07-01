---
title: "프로세스 스케줄링 알고리즘 (Process Scheduling)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 4
---

# 📖 【암기용】 개념 완전 이해

> 목적: 프로세스 스케줄링을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: CPU를 어떤 프로세스에 언제 줄지 결정하는 정책
- **왜 필요한가**: CPU는 한정되어 있고 작업 특성은 다르므로 처리량, 응답시간, 공정성, deadline을 동시에 조정해야 한다.
- **핵심 직관**: 줄 서기 규칙을 어떻게 정하느냐에 따라 평균 대기, 긴 작업 지연, 긴급 작업 처리 결과가 달라진다.

## 깊이 이해
- **배경·문제의식**: batch 작업은 처리량, interactive 작업은 응답시간, real-time 작업은 deadline이 우선이다. 단일 알고리즘으로 모든 목표를 만족하기 어렵다.
- **작동 원리**: FCFS는 도착 순서, SJF는 예상 CPU burst, RR은 time quantum, MLFQ는 우선순위 feedback, CFS는 vruntime 기반으로 CPU 몫을 배정한다.
- **비유**: 은행 창구에서 번호표 순서, 짧은 업무 우선, 3분씩 순환, VIP 등급 조정, 사용 시간 누적 균등 배분이 각각의 스케줄링 정책이다.
- **구체 예시**: RR quantum이 1ms이면 응답시간은 줄 수 있으나 context switch/sec가 증가한다. 50ms이면 전환 비용은 줄지만 interactive p95가 커질 수 있다.
- **흔한 오해·주의점**: 평균 대기시간만 낮추면 충분하지 않다. starvation, tail latency, fairness, deadline miss를 함께 봐야 한다.

## 연결 개념
- MLFQ: interactive 우선과 aging을 결합
- CFS: Linux 기본 공정 스케줄러
- 실시간 스케줄링: RMS, EDF로 deadline 보장

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 알고리즘 이름 나열이 아니라 throughput, turnaround, waiting, response, fairness의 trade-off로 비교한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 프로세스 스케줄링은 ready queue의 실행 순서를 정해 CPU 시간을 배분하는 커널 정책이다.
> 2. **가치**: 작업 특성에 따라 처리량, 평균 반환시간, 대기시간, 응답시간, 공정성을 조정한다.
> 3. **판단 포인트**: FCFS·SJF·RR·MLFQ·CFS는 평가 지표와 starvation 대응 방식이 다르다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| scheduling metric 이해 확인 | throughput, turnaround, waiting, response, fairness | 지표 구분 없이 장단점만 서술 |
| 알고리즘별 선택 기준 확인 | FCFS, SJF, RR, MLFQ, CFS 차이 | SJF를 현실 예측 문제 없이 설명 |
| OS 병목 판단 확인 | time quantum, context switch, starvation, aging | 평균값만 보고 tail latency 누락 |

> 요약: 이 문제는 스케줄링 정책을 지표와 workload 특성에 맞춰 선택하는 역량을 본다.

---

## Ⅰ. 개요 및 필요성

- 개요: 스케줄링은 ready task CPU 배정 정책이다.
- 배경: 멀티프로그래밍 환경은 CPU burst와 I/O burst가 섞이므로 FCFS, SJF, RR, priority 정책마다 대기시간과 공정성 결과가 달라진다.
- 필요성: 정책 선택은 convoy effect, starvation, deadline miss, context switch overhead를 p95 대기시간·처리량·deadline miss rate로 통제하기 위해 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
Ready Queue -> Scheduler Policy -> Dispatch
Policy: FCFS / SJF / RR / MLFQ / CFS
Metric: throughput / turnaround / waiting / response / fairness
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Ready queue | 실행 가능한 task 보관 | priority queue, RB-tree |
| Scheduler | 다음 task 선택 | preemptive/non-preemptive |
| Dispatcher | context switch 수행 | dispatch latency 발생 |
| Timer | time slice 만료 감지 | RR, CFS preemption 기준 |

> 요약: 스케줄링은 ready queue, 선택 정책, dispatch, timer가 결합된 CPU 배분 체계이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Task Ready 등록 -> 정책별 우선순위 계산
-> Next Task 선택 -> Context Switch
-> Time Slice/Block/Exit 감지 -> Queue 재배치 -> Metric 측정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | runnable task를 ready queue에 삽입 | queue length |
| 2 | policy 기준으로 우선순위 또는 vruntime 계산 | scheduler latency |
| 3 | dispatcher가 CPU context 전환 | context switch/sec |
| 4 | timer interrupt 또는 I/O block 발생 | time slice 사용률 |
| 5 | waiting, ready, terminated 상태로 재분류 | turnaround, response |

> 요약: 스케줄러는 task 상태 변화를 queue 이동으로 반영하고 지표 기반으로 정책 효과를 판단한다.

---

## Ⅳ. 특징

| 알고리즘 | 선택 기준 | 장점/한계 | 수치·기술 포인트 |
|:---|:---|:---|:---|
| FCFS | 도착 순서 | 구현 단순, convoy effect | long job 선점 불가 |
| SJF/SRTF | CPU burst 짧은 작업 | 평균 대기 감소, burst 예측 필요 | exponential average |
| RR | time quantum 순환 | interactive 응답 보장, switch 증가 | quantum 1~50ms 조정 |
| MLFQ | priority feedback | I/O bound 우대, aging 필요 | starvation 방지 |
| CFS | vruntime 최소 task | CPU share 공정성 | red-black tree O(log n) |

> 요약: batch는 SJF, interactive는 RR/MLFQ, 일반 Linux 서버는 CFS, deadline 작업은 실시간 스케줄러가 적합하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 FIFO | 다중 정책 스케줄링 | workload 다양성 |
| 비용/성능 | 긴 quantum | 짧은 quantum/feedback | p95 response vs switch/sec |
| 운영/위험 | starvation 방치 | aging, fair share | longest wait time |

> 요약: 스케줄링 선택은 평균 처리량보다 p95 응답시간과 starvation 방지 기준을 함께 둔다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| convoy effect | 긴 CPU-bound job 선점 불가 | preemptive RR/MLFQ | average waiting time |
| starvation | 낮은 priority 장기 대기 | aging, minimum share | max wait time |
| switch overhead | quantum 과소 설정 | quantum 튜닝, batching | context switch/sec |

> 요약: 주요 리스크는 긴 작업 독점, 낮은 우선순위 기아, 과도한 전환이며 지표별 대응이 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 처리량 | 기준 workload TPS 10% 이상 감소 금지 | benchmark, load test |
| 응답시간 | interactive p95 100ms 이하 | APM, scheduler trace |
| 공정성 | CPU share 오차 5% 이내 | cgroup cpu.stat, perf sched |

> 요약: 스케줄러 평가는 처리량, 응답시간, CPU share 오차를 함께 측정해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. interactive 서비스는 RR/MLFQ 성격의 짧은 time slice와 priority boost를 적용하고 p95 response를 100ms 이하로 관리
2. Linux 서버는 CFS nice, cgroup cpu.weight, quota를 사용해 batch와 online workload의 CPU share를 분리
3. scheduler trace와 perf sched latency로 run queue 지연, switch/sec, starvation task를 주기 측정

**결론 (2줄):**
- 기술사 판단: batch는 평균 반환시간, interactive는 p95 응답시간, multi-tenant는 CPU share 공정성을 기준으로 정책을 선택함
- 향후 방향: 컨테이너 환경에서는 OS 스케줄러와 cgroup quota가 겹치므로 application pool 크기까지 함께 조정해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "스케줄링 알고리즘을 설명하시오" | queue 이동과 dispatch 흐름 | 알고리즘별 지표 비교 |
| 요구사항 명시형 | "비교하시오", "선택 기준을 제시하시오" | workload별 평가 지표 | 응답시간·처리량·공정성 trade-off |

> 요약: 설명형은 알고리즘 폭을, 비교형은 지표별 선택 기준을 전면에 둔다.
