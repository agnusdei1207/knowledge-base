---
title: "실시간 스케줄링 (Real-Time Scheduling)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 7
---

# 📖 【암기용】 개념 완전 이해

> 목적: 실시간 스케줄링을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 정해진 deadline 안에 작업 완료를 보장하는 스케줄링
- **왜 필요한가**: 자율주행 제어, 항공, 의료기기, 공장 제어는 평균 처리량보다 deadline miss 1건의 영향이 크다.
- **핵심 직관**: 실시간 스케줄링은 빨리 끝내는 경쟁이 아니라 약속 시각을 어기지 않도록 CPU 순서를 정하는 것이다.

## 깊이 이해
- **배경·문제의식**: 일반 OS 스케줄러는 공정성과 응답성을 중시하지만, hard real-time에서는 deadline miss가 시스템 실패로 이어진다. 따라서 주기, 실행시간, deadline을 수학적으로 분석한다.
- **작동 원리**: RMS는 주기가 짧은 task에 높은 고정 우선순위를 준다. EDF는 절대 deadline이 가장 가까운 task를 먼저 실행한다. CPU utilization과 worst-case execution time이 schedulability 판단의 중심이다.
- **비유**: 택배를 많이 배송하는 것보다, 냉장 의약품 배송 마감 시각을 절대 넘기지 않도록 경로를 짜는 방식이다.
- **구체 예시**: 주기 task 3개의 utilization 합이 0.69 이하이면 RMS의 Liu-Layland bound 3(2^(1/3)-1) 약 0.779 기준에서 스케줄 가능 후보이다.
- **흔한 오해·주의점**: real-time은 처리 속도 자체가 아니라 deadline 보장이다. 평균 응답시간이 낮아도 deadline miss가 있으면 hard real-time 요구를 만족하지 못한다.

## 연결 개념
- RMS: Rate Monotonic Scheduling, 고정 우선순위
- EDF: Earliest Deadline First, 동적 우선순위
- Priority Inversion: 높은 우선순위 task가 lock 때문에 대기하는 현상

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 실시간 스케줄링은 RMS·EDF 이름보다 WCET, period, deadline, utilization bound, miss 대응이 핵심이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 실시간 스케줄링은 task의 실행시간과 deadline을 기준으로 CPU 배정 순서를 정해 deadline miss를 통제하는 정책이다.
> 2. **가치**: hard real-time은 miss 0건, soft real-time은 miss율과 지연분포를 기준으로 서비스 품질을 보장한다.
> 3. **판단 포인트**: RMS는 주기 기반 고정 우선순위, EDF는 deadline 기반 동적 우선순위이며 utilization과 WCET 분석이 필요하다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| real-time 의미 확인 | hard/soft real-time, deadline miss, WCET | 처리량 증가 문제로 오해 |
| RMS·EDF 비교 확인 | 고정 우선순위 vs 동적 deadline 우선 | 알고리즘명만 나열 |
| schedulability 판단 확인 | utilization bound, period, deadline | 평균 실행시간만 사용 |

> 요약: 이 문제는 deadline 보장 조건과 miss 리스크를 수치로 판단하게 한다.

---

## Ⅰ. 개요 및 필요성

실시간 스케줄링은 deadline 중심 CPU 배정 정책이다.
일반 스케줄링이 평균 응답시간과 공정성을 중시한다면, 실시간 스케줄링은 WCET와 deadline을 기준으로 deadline miss를 통제한다.
자율주행, 산업제어, 금융 시세 처리처럼 지연 상한이 명시된 시스템에서 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
Task Set -> Period / WCET / Deadline 분석
-> Scheduler: RMS / EDF
-> Dispatch -> Deadline Monitor -> Miss Handling
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Period | task 반복 주기 | RMS 우선순위 기준 |
| WCET | 최악 실행시간 | schedulability 입력 |
| Deadline | 완료 시각 제한 | EDF 선택 기준 |
| Scheduler | RMS/EDF로 실행 순서 결정 | preemption 필요 |
| Monitor | miss 감지와 fail-safe | hard/soft 대응 분리 |

> 요약: 실시간 스케줄링은 task 속성 분석, 정책 선택, deadline 감시가 결합된 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Task 속성 수집 -> Utilization 계산
-> RMS/EDF 정책 선택 -> Ready Queue 정렬
-> Dispatch/Preempt -> Deadline 도달 전 완료 확인
-> Miss 발생 시 degrade/fail-safe
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | task별 C 실행시간, T 주기, D deadline 산정 | WCET 측정 근거 |
| 2 | utilization U=sum(C/T) 계산 | RMS bound, EDF U<=1 |
| 3 | RMS는 짧은 주기, EDF는 가까운 deadline 우선 | priority/deadline order |
| 4 | preemption과 dispatch로 CPU 배정 | preemption latency |
| 5 | 완료 시각과 deadline 비교 | miss count, jitter |

> 요약: 실시간 스케줄링은 사전 분석과 런타임 감시를 함께 수행해 deadline miss를 통제한다.

---

## Ⅳ. 특징

| 구분 | RMS | EDF | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 우선순위 | 주기 짧을수록 높음 | deadline 가까울수록 높음 | fixed vs dynamic |
| 이용률 bound | n(2^(1/n)-1), n 무한대 약 0.693 | 이상 조건 U<=1 | overload 시 EDF 연쇄 miss |
| 구현 난이도 | 예측·검증 단순 | queue 재정렬 필요 | deadline queue |
| 적용 | safety-critical fixed task | task 변동 큰 시스템 | jitter, miss ratio |

> 요약: RMS는 분석 단순성, EDF는 높은 CPU 이용률이 장점이나 overload 대응 설계가 필요하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 일반 CFS/RR | RMS/EDF 실시간 정책 | deadline 명시 여부 |
| 비용/성능 | 평균 응답시간 중심 | miss 0건 또는 miss율 관리 | hard/soft real-time |
| 운영/위험 | best effort | WCET와 fail-safe | safety integrity 요구 |

> 요약: hard real-time은 평균 지표보다 WCET와 deadline miss 0건을 우선한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| deadline miss | WCET 과소 추정 | static analysis, margin 20% 확보 | miss count |
| priority inversion | low task가 lock 보유 | priority inheritance/ceiling | blocking time |
| overload collapse | utilization 1 초과 | admission control, degrade mode | U, queue backlog |

> 요약: 실시간 리스크는 WCET 오류, lock blocking, overload이며 사전 허가와 우선순위 상속이 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| deadline | hard RT miss 0건 | trace clock, histogram |
| jitter | 제어주기 jitter 1ms 이하 | cyclictest, oscilloscope |
| 이용률 | RMS bound 이하 또는 EDF U<=0.8 운영 | WCET/period 분석 |

> 요약: 실시간 품질은 deadline miss, jitter, utilization으로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. task별 WCET, period, deadline을 표준화하고 RMS bound 또는 EDF U<=0.8 기준으로 admission control 수행
2. Linux PREEMPT_RT, SCHED_FIFO/RR, CPU isolation, IRQ affinity로 preemption latency와 jitter를 측정·제한
3. priority inversion 방지를 위해 priority inheritance mutex를 적용하고 blocking time을 deadline budget에 포함

**결론 (2줄):**
- 기술사 판단: task 집합이 고정이면 RMS, deadline이 가변이고 CPU 이용률을 높여야 하면 EDF, safety-critical이면 fail-safe를 추가함
- 향후 방향: edge AI·SDV 제어는 AI inference latency와 RTOS scheduling을 함께 분석하는 혼합 실시간 구조로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "실시간 스케줄링을 설명하시오" | WCET·period·deadline 흐름 | RMS·EDF 비교 |
| 요구사항 명시형 | "deadline 보장 방안을 제시하시오" | schedulability 분석 절차 | miss·jitter·inversion 대응 |

> 요약: 설명형은 RMS/EDF 원리, 설계형은 deadline 보장 조건과 fail-safe를 중심으로 작성한다.
