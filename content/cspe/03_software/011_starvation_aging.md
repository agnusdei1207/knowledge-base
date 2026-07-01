---
title: "기아·에이징 (Starvation Aging)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 11
---

# 📖 【암기용】 개념 완전 이해

> 목적: 기아와 에이징을 처음 봐도 스케줄링 공정성 관점에서 이해하게 만든다. 시험 답안 양식이 아니라, CPU 배분 문제를 직관적으로 설명한다.

## 한눈에
- **개요**: 기아는 실행 가능한 작업이 계속 밀려 CPU를 받지 못하는 현상이다.
- **왜 필요한가**: 우선순위 스케줄링은 응답시간을 줄이지만 낮은 우선순위 작업이 무기한 대기할 수 있다. 운영체제는 처리량과 공정성을 함께 맞춰야 한다.
- **핵심 직관**: 오래 기다린 작업의 우선순위를 조금씩 올려 "언젠가는 반드시 실행"되게 만드는 장치가 에이징이다.

## 깊이 이해
- **배경·문제의식**: SJF, Priority, MLFQ는 평균 대기시간과 대화형 응답시간을 줄이지만, 짧은 작업이나 높은 우선순위 작업이 계속 들어오면 낮은 작업은 준비 큐에 갇힌다.
- **작동 원리**: 스케줄러는 대기시간, 우선순위, CPU 사용 이력을 추적한다. 대기시간이 임계값을 넘으면 우선순위를 1단계 올리거나 vruntime 보정치를 부여해 선택 확률을 증가시킨다.
- **비유**: 병원 접수에서 응급 환자를 먼저 보되, 오래 기다린 일반 환자에게 번호 보정권을 주어 진료 누락을 막는 방식과 같다.
- **구체 예시**: 우선순위 0~31 체계에서 1초 대기마다 우선순위 값을 1 감소시키면, priority 30 작업도 30초 후 priority 0 수준으로 승격된다.
- **흔한 오해·주의점**: 기아는 교착상태가 아니다. 교착상태는 자원 순환 대기 때문에 모두 멈추는 상황이고, 기아는 시스템은 계속 진행되지만 특정 작업만 선택되지 않는 상황이다.

## 연결 개념
- 우선순위 역전(Priority Inversion) — 낮은 우선순위 작업이 잠금을 쥐어 높은 작업을 막는 별도 문제
- 공정 스케줄링(Fair Scheduling) — CPU 시간을 비율로 배분해 장기 불균형을 줄이는 접근
- 한정 대기(Bounded Waiting) — 임계 구역과 스케줄링에서 무기한 대기 방지 조건

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 기아를 단순 대기 현상으로 쓰지 말고, 우선순위 정책의 응답시간·처리량·공정성 trade-off와 에이징 보정으로 설명한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 기아(Starvation)는 준비 상태 프로세스가 스케줄링 정책상 계속 선택되지 않아 대기시간 상한이 사라지는 현상이다.
> 2. **가치**: 에이징(Aging)은 대기시간에 비례해 우선순위를 보정하여 bounded waiting과 CPU 배분 공정성을 확보한다.
> 3. **판단 포인트**: priority inversion은 잠금 소유 관계 문제, starvation은 스케줄러 선택 편향 문제로 구분해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 스케줄링 공정성 이해 확인 | 기아 원인, 에이징 보정, bounded waiting | 교착상태와 동일시하지 않음 |
| 우선순위 정책 trade-off 판단 | 응답시간, 처리량, 공정성, 대기시간 상한 | 높은 우선순위만 계속 선택하는 답안 지양 |
| priority inversion과 구분 확인 | 잠금 소유 문제 vs 큐 선택 편향 | 우선순위 상속을 기아 해법으로만 쓰지 않음 |

> 요약: 이 문제는 우선순위 스케줄링의 편향을 어떻게 대기시간 기반 보정으로 통제하는지 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 기아는 실행 가능 작업의 무기한 대기이다.
- 배경: 우선순위·SJF·MLFQ는 높은 우선순위나 짧은 작업을 반복 선택해 낮은 우선순위 작업의 CPU 배분을 장기간 0에 가깝게 만들 수 있다.
- 필요성: 에이징은 max wait, starvation count, interactive p95 기준으로 대기시간을 스케줄링 입력값에 반영한다.

---

## Ⅱ. 구조 및 구성요소

```text
Ready Queue -> Priority Scheduler -> CPU Dispatch
       / Waiting Time Tracker -> Aging Policy -> Priority Recalculation
       / Fairness Guard -> Bounded Waiting Check
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Ready Queue | 실행 가능 프로세스 보관 | priority, vruntime, wait time 포함 |
| Aging Policy | 대기시간 기반 우선순위 보정 | 1초당 1단계 승격, 또는 가중치 증가 |
| Fairness Guard | 대기시간 상한 감시 | max wait 30초, starvation count 측정 |

> 요약: 기아 제어 구조는 큐 상태를 관측하고 대기시간을 우선순위 재계산에 넣어 dispatch 편향을 줄인다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Process Ready -> Wait Time Accumulate -> Aging Threshold Check
  -> Priority Boost / vruntime Compensation -> Scheduler Select
  -> CPU Dispatch -> Wait Metric Reset or Continue
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 준비 큐 진입 시 대기 시작 시각 기록 | enqueue timestamp 존재 |
| 2 | tick 또는 dispatch 시점에 대기시간 계산 | wait time p95, max wait |
| 3 | 임계값 초과 작업 우선순위 보정 | boost interval 1~5초 |
| 4 | 보정된 우선순위로 CPU 배정 | bounded waiting 위반 0건 |

> 요약: 에이징은 대기시간 측정, 보정, 재선택, 지표 초기화의 반복으로 무기한 대기를 차단한다.

---

## Ⅳ. 특징

| 구분 | 기존 우선순위 스케줄링 | 에이징 적용 | 수치·판단 기준 |
|:---|:---|:---|:---|
| 공정성 | 낮은 우선순위 작업 장기 대기 | 대기시간 비례 우선순위 상승 | max wait 30초 이하 |
| 응답시간 | 높은 우선순위 작업 즉시 배정 | 보정 작업이 일부 CPU 확보 | interactive p95 100ms 관리 |
| 처리량 | 짧은 작업 위주 처리 | 장기 대기 작업도 주기적 실행 | starvation count 0건 |

> 요약: 에이징은 응답시간 일부를 비용으로 사용해 대기시간 상한과 장기 공정성을 확보한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 고정 우선순위 | 대기시간 기반 동적 보정 | 실시간 hard deadline 없을 때 |
| 비용/성능 | 계산 비용 낮음 | tick마다 wait 계산 비용 발생 | 큐 길이 10만 이상이면 lazy aging |
| 운영/위험 | 응답시간 예측 용이 | priority inflation 발생 가능 | boost 상한, decay 정책 필요 |

> 요약: hard real-time은 고정 우선순위를 유지하고, 범용 OS는 에이징으로 starvation count를 0에 맞춘다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 우선순위 인플레이션 | 모든 작업이 동시에 승격 | boost cap, decay interval 적용 | runnable priority 분포 |
| 대화형 지연 증가 | 오래 기다린 batch 작업 dispatch | interactive weight 별도 부여 | UI p95 latency 100ms 이하 |
| 실시간 작업 deadline miss | 에이징이 RT 큐에 개입 | RT class와 normal class 분리 | deadline miss rate 0건 |

> 요약: 에이징은 적용 범위를 normal class로 제한하고 우선순위 상한을 두어 응답시간 회귀를 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 공정성 | starvation count 0건, max wait 30초 이하 | scheduler trace, run queue log |
| 응답시간 | interactive p95 100ms 이하 | perf sched, eBPF latency histogram |
| 처리량 | context switch overhead 5% 이하 | CPU profile, throughput benchmark |

> 요약: 성공 여부는 평균 대기시간보다 max wait, starvation count, p95 응답시간으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 우선순위 기반 배치 시스템은 1~5초 aging tick과 max wait 30초 목표를 설정해 장기 대기 작업을 승격함.
2. Linux CFS 계열은 priority boost 대신 vruntime 보정과 nice weight 조정으로 CPU 점유율 편차를 10% 이내로 관리함.
3. RT 작업은 SCHED_FIFO/RR 별도 클래스로 분리하고 normal class 에이징이 deadline miss를 만들지 않도록 cgroup CPU quota를 설정함.

**결론 (2줄):**
- 기술사 판단: 응답시간 우선 시스템이면 제한적 에이징, batch 혼합 시스템이면 bounded waiting 중심 에이징을 선택함.
- 향후 방향: eBPF 기반 scheduler latency 관측과 cgroup weight 제어로 공정성 정책을 workload별로 조정함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "기아와 에이징을 설명하시오" | 대기시간 측정, 우선순위 보정 흐름 | 교착상태·priority inversion과 구분 |
| 요구사항 명시형 | "방안을 제시하시오", "비교하시오" | bounded waiting 달성 절차 | 응답시간·처리량·공정성 선택 기준 |

> 요약: 설명형은 원인과 원리를 넓게 쓰고, 방안형은 max wait와 starvation count 지표 중심으로 목차를 전환한다.
