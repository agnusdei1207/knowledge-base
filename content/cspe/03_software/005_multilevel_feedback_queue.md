---
title: "멀티레벨 피드백 큐 MLFQ (Multilevel Feedback Queue)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 5
---

# 📖 【암기용】 개념 완전 이해

> 목적: MLFQ를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 여러 우선순위 큐와 feedback으로 CPU를 배분하는 스케줄링
- **왜 필요한가**: interactive 작업은 짧게 자주 CPU를 쓰고, CPU-bound 작업은 길게 CPU를 쓰므로 같은 줄에 세우면 응답시간이 늘어난다.
- **핵심 직관**: 짧게 끝내는 손님은 빠른 창구에 두고, 오래 붙잡는 손님은 뒤 창구로 내려보내는 방식이다.

## 깊이 이해
- **배경·문제의식**: SJF는 CPU burst 예측이 필요하고 RR은 모든 작업을 같은 quantum으로 처리한다. MLFQ는 실제 CPU 사용 패턴을 관찰해 우선순위를 조정한다.
- **작동 원리**: 새 작업은 높은 우선순위 큐에서 시작한다. quantum 안에 CPU를 반납하면 높은 우선순위를 유지하고, quantum을 다 쓰면 낮은 큐로 이동한다. 오래 기다린 작업은 aging으로 다시 올린다.
- **비유**: 놀이공원에서 빠르게 끝나는 탑승객은 앞줄을 유지하지만, 여러 번 긴 상담을 하는 고객은 일반 대기줄로 이동한다. 너무 오래 기다리면 우선 호출권을 준다.
- **구체 예시**: Q0 quantum 4ms, Q1 8ms, Q2 16ms로 두면 키보드 입력·GUI 이벤트는 Q0에서 p95 20ms 이내로 처리하고, 컴파일 작업은 Q2에서 긴 quantum을 받는다.
- **흔한 오해·주의점**: MLFQ는 priority만 나눈 구조가 아니다. 핵심은 CPU 사용 행동에 따라 큐를 내리고, aging으로 다시 올리는 feedback이다.

## 연결 개념
- RR: 각 큐 내부에서 time quantum 순환
- Starvation Aging: 낮은 큐 장기 대기 방지
- CFS: vruntime 기반 공정성 정책과 비교 대상

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: MLFQ는 interactive 응답시간과 CPU-bound 처리량의 균형을 priority feedback, quantum, aging으로 달성하는 정책이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MLFQ는 다단계 우선순위 큐와 실행 이력 feedback으로 task 우선순위를 동적으로 조정하는 스케줄러이다.
> 2. **가치**: CPU burst가 짧은 interactive task에는 짧은 대기시간, CPU-bound task에는 긴 quantum을 제공한다.
> 3. **판단 포인트**: 큐 수, quantum 배율, demotion, promotion, aging 주기를 workload에 맞게 설정해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| feedback 기반 스케줄링 이해 확인 | high queue 시작, quantum 소진 시 demotion, aging promotion | 단순 fixed priority queue로 설명 |
| interactive와 CPU-bound 구분 확인 | I/O block task 우대, CPU-bound task 하위 큐 이동 | 응답시간과 처리량 trade-off 누락 |
| starvation 방지 판단 확인 | aging, priority boost, minimum share | 낮은 큐 기아 문제 누락 |

> 요약: 이 문제는 MLFQ의 동적 우선순위 조정과 기아 방지 장치를 함께 요구한다.

---

## Ⅰ. 개요 및 필요성

MLFQ는 feedback 기반 다단계 우선순위 스케줄링이다.
운영체제는 작업의 실제 CPU 사용 패턴을 관찰해 interactive task를 상위 큐에 유지하고 CPU-bound task를 하위 큐로 이동시킨다.
CPU burst 예측 없이 응답시간과 처리량을 함께 조정하기 위해 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
New Task -> Q0 High Priority Short Quantum
CPU 사용량 적음 -> Q0/Q1 유지
Quantum 소진 -> Q1/Q2 Demotion
Long Wait -> Aging/Boost -> Higher Queue
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Priority queue | 우선순위별 ready task 저장 | Q0가 Q1보다 먼저 실행 |
| Time quantum | 큐별 CPU 사용 한도 | 하위 큐일수록 길게 설정 |
| Feedback rule | CPU 사용량 기반 승강급 | quantum 소진 시 demotion |
| Aging/Boost | 장기 대기 task 승급 | starvation 방지 |

> 요약: MLFQ는 우선순위 큐, 큐별 quantum, feedback rule, aging으로 task 위치를 동적으로 바꾼다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Task 도착 -> 최상위 큐 삽입
-> Q0부터 runnable 확인 -> Dispatch
-> Quantum 내 I/O block이면 상위 유지
-> Quantum 소진이면 하위 큐 이동
-> Aging 조건 충족이면 상위 큐 승급
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 신규 task를 Q0 또는 정책 기준 큐에 삽입 | new task latency |
| 2 | 가장 높은 non-empty queue에서 task 선택 | priority order 준수 |
| 3 | quantum 내 block/yield 시 interactive로 판단 | I/O wait ratio |
| 4 | quantum 소진 시 CPU-bound로 보고 demotion | demotion count |
| 5 | 장기 대기 task를 aging으로 promotion | max wait time |

> 요약: MLFQ는 실행 결과를 다음 우선순위에 반영해 interactive task와 CPU-bound task를 자동 분류한다.

---

## Ⅳ. 특징

| 구분 | MLFQ 방식 | 대안 방식 | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 우선순위 | 실행 이력으로 동적 변경 | fixed priority | priority inversion 감시 |
| quantum | 상위 짧고 하위 길게 | RR 단일 quantum | 4/8/16ms 계층 |
| starvation 대응 | aging, periodic boost | 낮은 priority 대기 | max wait time 제한 |
| workload 적합성 | interactive+batch 혼합 | pure batch는 SJF 유리 | p95 response 기준 |

> 요약: MLFQ는 실제 CPU 사용 패턴을 관찰해 응답시간과 처리량의 균형점을 찾는 정책이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | RR 단일 큐 | 다중 큐+feedback | interactive 비율 30% 이상 |
| 비용/성능 | 공정하지만 분류 없음 | 분류 가능, 튜닝 필요 | p95 response, throughput |
| 운영/위험 | CPU-bound 독점 가능 | aging으로 기아 방지 | max wait time 상한 |

> 요약: interactive 응답시간이 채점 포인트이면 MLFQ의 demotion과 aging 구조를 먼저 제시한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| gaming | task가 quantum 직전 yield | CPU usage window 누적 평가 | suspicious yield rate |
| starvation | 하위 큐 task 장기 대기 | aging interval, global boost | max wait time |
| 튜닝 실패 | quantum이 workload와 불일치 | 4/8/16ms 등 배율 실험 | p95 latency, switch/sec |

> 요약: MLFQ 운영 리스크는 gaming, starvation, quantum 튜닝이며 계측 기반 조정이 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 응답시간 | interactive p95 50ms 이하 | scheduler trace, APM |
| 공정성 | 하위 큐 max wait 1s 이하 | queue wait histogram |
| 전환 비용 | switch/sec 기준선 20% 이내 증가 | perf sched, vmstat |

> 요약: MLFQ 효과는 interactive p95, max wait, switch/sec로 동시에 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 큐 3~5개, quantum 4/8/16/32ms 배율로 시작해 interactive p95와 switch/sec를 함께 측정
2. aging interval을 500ms~1s 범위로 설정하고 하위 큐 max wait가 SLO를 넘으면 priority boost 수행
3. CPU 사용 window를 누적해 gaming task를 탐지하고, container별 CPU quota와 결합해 tenant별 share 보장

**결론 (2줄):**
- 기술사 판단: interactive와 batch가 혼합된 범용 OS는 MLFQ, 공정 share가 핵심인 Linux 서버는 CFS 계열을 선택함
- 향후 방향: 클라우드 환경에서는 MLFQ 개념을 cgroup, quota, latency SLO와 결합해 workload별 CPU 정책으로 확장해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "MLFQ를 설명하시오" | 큐 이동, demotion, aging 흐름 | RR·SJF·CFS와 차이 |
| 요구사항 명시형 | "응답시간 개선 방안을 제시하시오" | quantum/aging 튜닝 절차 | interactive p95와 starvation 대응 |

> 요약: 설명형은 feedback 원리, 방안형은 quantum과 aging 지표를 중심으로 전개한다.
