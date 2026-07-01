---
title: "CFS 완전 공정 스케줄러 (Completely Fair Scheduler)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 6
---

# 📖 【암기용】 개념 완전 이해

> 목적: CFS를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Linux가 vruntime으로 CPU 사용 공정성을 맞추는 스케줄러
- **왜 필요한가**: 여러 task가 동시에 CPU를 요구할 때, 고정 time slice만으로는 nice 값과 CPU share를 정확히 반영하기 어렵다.
- **핵심 직관**: CPU를 덜 쓴 사람을 왼쪽 줄에 세우고, 가장 덜 쓴 사람부터 다시 CPU를 주는 방식이다.

## 깊이 이해
- **배경·문제의식**: 전통 O(1) 스케줄러는 active/expired array와 priority 조정이 복잡했다. CFS는 이상적인 공정 공유 모델을 vruntime으로 근사한다.
- **작동 원리**: task가 CPU를 쓸수록 vruntime이 증가한다. nice 값이 낮아 weight가 큰 task는 vruntime 증가 속도가 느려 더 많은 CPU share를 받는다. CFS는 red-black tree의 가장 왼쪽 task, 즉 vruntime이 가장 작은 task를 선택한다.
- **비유**: 운동장 사용 시간을 장부에 적고, 누적 사용 시간이 가장 적은 팀에게 다음 차례를 주는 방식이다. 회원 등급(nice weight)에 따라 사용권 비율이 달라진다.
- **구체 예시**: nice 0 weight 1024, nice 5 weight 335이면 nice 0 task는 같은 경쟁 조건에서 약 3배 CPU share를 받는다. target latency 24ms에서 4개 task는 각 6ms 내외 slice를 받는다.
- **흔한 오해·주의점**: CFS는 모든 task에 같은 시간을 주는 정책이 아니다. nice weight와 cgroup cpu.weight를 반영해 가중 공정성을 제공한다.

## 연결 개념
- vruntime: 실제 실행 시간을 weight로 보정한 가상 실행 시간
- red-black tree: runnable task 정렬 자료구조
- cgroup CPU: container별 CPU share·quota 제어

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: CFS는 Linux scheduler를 vruntime, nice weight, red-black tree, target latency로 설명해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CFS는 runnable task의 vruntime을 기준으로 CPU를 덜 사용한 task를 우선 실행하는 Linux 공정 스케줄러이다.
> 2. **가치**: fixed quantum 대신 target latency와 weight를 이용해 interactive 응답성과 CPU share 공정성을 조정한다.
> 3. **판단 포인트**: vruntime 산정, RB-tree 선택 비용, nice/cgroup weight, quota throttling을 함께 제시해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Linux 스케줄러 구조 이해 확인 | vruntime, RB-tree, leftmost task, nice weight | 단순 RR로 설명 |
| 공정성 판단 확인 | weight 기반 CPU share, target latency | 모든 task 동일 시간 배분으로 오해 |
| 실무 튜닝 역량 확인 | nice, cgroup cpu.weight, quota, throttling | container CPU 제한 영향 누락 |

> 요약: 이 문제는 CFS의 자료구조와 가중 공정성, 운영 튜닝 지표를 연결해야 한다.

---

## Ⅰ. 개요 및 필요성

CFS는 Linux의 가중 공정 CPU 스케줄러이다.
runnable task의 vruntime을 red-black tree에 정렬하고, CPU를 덜 받은 task를 우선 선택해 공정한 CPU share를 제공한다.
서버·컨테이너 환경에서는 nice와 cgroup으로 tenant별 CPU 배분을 제어하기 위해 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
Runnable Task -> vruntime 계산 -> RB-tree 삽입
RB-tree Leftmost -> Pick Next Task -> Execute
Execute Time -> vruntime 증가 -> Reinsert/Block/Exit
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| vruntime | 실제 실행 시간을 weight로 보정 | 작을수록 먼저 실행 |
| nice weight | task별 CPU share 가중치 | nice 0 weight 1024 |
| red-black tree | runnable task 정렬 | 선택·삽입 O(log n) |
| target latency | 전체 runnable 순환 목표 시간 | task 수에 따라 slice 계산 |
| cgroup CPU | 그룹 단위 share/quota 제어 | container throttling 발생 가능 |

> 요약: CFS는 vruntime을 RB-tree에 정렬하고 weight와 latency 기준으로 다음 실행 task를 고른다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Task runnable 등록 -> weight 확인 -> vruntime 보정
-> RB-tree 정렬 -> leftmost task 선택
-> CPU 실행 -> vruntime 증가
-> block/expire 시 tree 재삽입 또는 제거
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | runnable task의 nice/cgroup weight 확인 | cpu.weight, nice 값 |
| 2 | 실행 시간에 weight 보정해 vruntime 계산 | schedstat vruntime |
| 3 | RB-tree leftmost task를 pick_next로 선택 | scheduler latency |
| 4 | target latency와 runnable 수로 slice 산정 | sched_min_granularity |
| 5 | 실행 후 vruntime 갱신 및 재정렬 | CPU share 오차 |

> 요약: CFS는 가장 작은 vruntime을 선택하고 실행 후 vruntime을 늘려 CPU 사용 균형을 맞춘다.

---

## Ⅳ. 특징

| 구분 | CFS | MLFQ/RR | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 선택 기준 | 최소 vruntime | queue priority/time quantum | RB-tree O(log n) |
| 공정성 | nice weight 기반 share | quantum 동일 또는 priority | nice 0 weight 1024 |
| 응답성 | target latency로 조정 | 상위 큐 우대 | sched_latency_ns |
| 컨테이너 | cgroup CPU와 결합 | OS 단일 queue 중심 | cpu.weight, cpu.max |

> 요약: CFS는 우선순위 큐보다 누적 CPU 사용량을 기준으로 가중 공정성을 구현한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | O(1) priority array | RB-tree+vruntime | 공정 share 요구 |
| 비용/성능 | 고정 quantum | dynamic slice | runnable task 수, latency |
| 운영/위험 | nice만 조정 | cgroup share/quota 병행 | tenant별 CPU 격리 |

> 요약: Linux 서버에서는 CFS와 cgroup을 함께 봐야 프로세스 단위와 컨테이너 단위 CPU 배분을 설명할 수 있다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| latency spike | runnable task 과다 | pool 제한, CPU request 조정 | run queue latency |
| quota throttling | cgroup cpu.max 과소 | quota/period 조정 | throttled_time |
| share 불균형 | nice/cpu.weight 오설정 | weight 표준화, baseline test | CPU share 오차 5% 이내 |

> 요약: CFS 리스크는 task 과다, quota throttling, weight 오설정이며 cgroup 지표로 추적한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 공정성 | CPU share 오차 5% 이내 | cgroup cpu.stat, pidstat |
| 지연시간 | run queue latency p95 10ms 이하 | perf sched latency |
| throttling | throttled_time 비율 1% 이하 | cgroup cpu.stat |

> 요약: CFS 운영 품질은 CPU share 오차, run queue latency, throttling 비율로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 서비스별 nice와 cgroup cpu.weight를 표준화해 online workload에 batch 대비 2~4배 CPU share 부여
2. Kubernetes CPU limit으로 인한 throttling_time을 1% 이하로 유지하고, burst workload는 limit보다 request 중심으로 관리
3. perf sched latency와 cgroup cpu.stat을 수집해 run queue p95, nr_throttled, CPU share 오차를 대시보드화

**결론 (2줄):**
- 기술사 판단: Linux 범용 서버는 CFS를 기본으로 하고, deadline 보장이 필요하면 SCHED_FIFO/RR 또는 EDF 계열을 별도 적용함
- 향후 방향: 컨테이너 밀집 환경에서는 CFS 단독보다 cgroup, NUMA affinity, application pool 크기를 함께 튜닝해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "CFS를 설명하시오" | vruntime 계산과 RB-tree 선택 | MLFQ/RR 대비 공정성 |
| 요구사항 명시형 | "Linux CPU 튜닝 방안을 제시하시오" | cgroup weight/quota 흐름 | throttling·latency 대응 |

> 요약: 설명형은 vruntime 구조, 운영형은 cgroup과 throttling 지표를 중심으로 전환한다.
