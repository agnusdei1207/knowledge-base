---
title: "프로세스 스레싱 (Process Thrashing)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 15
---

# 📖 【암기용】 개념 완전 이해

> 목적: 스레싱을 처음 봐도 메모리 부족이 CPU 처리량을 무너뜨리는 현상으로 이해하게 만든다. 시험 답안 양식이 아니라, page fault storm의 원인을 설명한다.

## 한눈에
- **개요**: 스레싱은 프로세스들이 필요한 페이지를 메모리에 유지하지 못해 페이지 교체만 반복하는 현상이다.
- **왜 필요한가**: 가상 메모리는 메모리보다 큰 프로그램 실행을 돕지만, 동시에 너무 많은 프로세스를 올리면 디스크 I/O가 폭증하고 CPU는 놀게 된다.
- **핵심 직관**: 책상 위 공간보다 펼쳐야 할 책이 많아 매번 책을 넣고 빼느라 공부 시간이 사라지는 상황이다.

## 깊이 이해
- **배경·문제의식**: 다중프로그래밍 정도를 높이면 CPU 대기시간은 줄지만, 각 프로세스의 resident set이 working set보다 작아지는 순간 page fault가 연쇄 발생한다.
- **작동 원리**: page fault가 늘면 OS는 victim page를 내보내고 필요한 page를 가져온다. 이 I/O 동안 프로세스는 block되고, scheduler는 다른 프로세스를 올리지만 그 프로세스도 page fault를 내며 악순환이 생긴다.
- **비유**: 회의실에 사람이 너무 많아 자료를 보려 할 때마다 밖 창고에 다녀오면, 회의는 진행되지 않고 출입만 반복된다.
- **구체 예시**: RAM 8GB 시스템에서 활성 프로세스 working set 합이 12GB이면 page fault rate가 초당 수천 건으로 증가하고 CPU utilization이 80%에서 20% 이하로 떨어질 수 있다.
- **흔한 오해·주의점**: 스레싱은 CPU가 느린 문제가 아니다. 병목은 메모리 부족과 swap I/O이며, CPU 증설보다 working set 조절이 먼저다.

## 연결 개념
- Working Set — 최근 참조한 페이지 집합, 스레싱 판단 기준
- Page Fault Frequency — page fault 비율로 resident set을 조절하는 제어 방식
- Degree of Multiprogramming — 동시에 메모리에 올린 프로세스 수

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 스레싱은 page fault storm과 CPU utilization drop을 working set 초과, 다중프로그래밍 정도, swap I/O 관점으로 설명한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스레싱(Thrashing)은 메모리 resident set이 working set보다 작아 page fault와 swap I/O가 반복되는 현상이다.
> 2. **가치**: 원인을 파악하면 다중프로그래밍 정도, resident set 크기, PFF 제어로 CPU utilization을 회복할 수 있다.
> 3. **판단 포인트**: CPU busy가 아니라 major fault/sec, swap in/out, run queue, I/O wait를 함께 봐야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 가상 메모리 병목 이해 확인 | working set 초과, page fault storm | 단순 CPU 성능 문제로 쓰지 않음 |
| 제어 정책 판단 확인 | DOP 축소, PFF, local replacement | page replacement 알고리즘만 나열하지 않음 |
| 운영 지표 연결 확인 | CPU utilization drop, swap I/O, major fault | 평균 메모리 사용률만 제시하지 않음 |

> 요약: 이 문제는 메모리 과다 적재가 CPU 처리량을 떨어뜨리는 경로와 제어 지표를 묻는다.

---

## Ⅰ. 개요 및 필요성

스레싱은 페이지 교체가 실행보다 많이 발생하는 상태다. working set 합이 물리 메모리를 넘으면 page fault가 연쇄 발생하고 CPU utilization이 급락한다. OS는 다중프로그래밍 정도와 resident set을 조절해 스레싱을 통제한다.

---

## Ⅱ. 구조 및 구성요소

```text
Processes -> Working Set Demand -> Physical Memory Frames
       / Page Fault Handler -> Swap I/O -> Replacement Policy
       / DOP Controller -> Suspend / Resume Process
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Working Set | 최근 참조 페이지 집합 | window delta로 추정 |
| Page Fault Handler | 부재 페이지 적재 | major fault는 디스크 I/O 포함 |
| DOP Controller | 동시 실행 프로세스 수 제어 | swap 폭증 시 일부 suspend |

> 요약: 스레싱 구조는 working set 수요가 물리 frame 공급을 넘을 때 page fault handler와 swap I/O가 병목화되는 형태다.

---

## Ⅲ. 동작원리 및 흐름도

```text
High DOP -> Resident Set Shrink -> Working Set Miss
  -> Major Page Fault -> Swap In/Out -> I/O Wait Increase
  -> CPU Utilization Drop -> More Processes Admitted -> Thrashing Loop
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 다중프로그래밍 정도 증가 | runnable process count |
| 2 | 프로세스별 frame 수 감소 | RSS vs WSS 비교 |
| 3 | major page fault 증가 | major fault/sec |
| 4 | I/O wait 증가와 CPU utilization 감소 | iowait, CPU utilization |

> 요약: 스레싱은 DOP 증가, resident set 축소, major fault 증가, CPU utilization 감소가 순환하는 병목이다.

---

## Ⅳ. 특징

| 구분 | 정상 페이징 | 스레싱 상태 | 수치·판단 기준 |
|:---|:---|:---|:---|
| Page Fault | 지역성 내부에서 간헐 발생 | 초당 수천 건 major fault | major fault/sec 급증 |
| CPU 사용 | 계산 수행 중심 | I/O wait 중심 | CPU utilization 20% 이하 가능 |
| 메모리 상태 | WSS 합 <= RAM | WSS 합 > RAM | swap in/out 지속 증가 |

> 요약: 스레싱은 메모리 부족이 swap I/O를 늘리고 CPU 실행 시간을 빼앗는 상태다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | global replacement | working set 기반 제어 | 프로세스 간 page steal 과다 시 |
| 비용/성능 | DOP 높게 유지 | DOP 축소로 fault 감소 | CPU utilization 회복 우선 |
| 운영/위험 | 메모리 overcommit | admission control, cgroup limit | swap storm 재발 방지 |

> 요약: 스레싱 대응은 더 많은 프로세스를 실행하는 것이 아니라 일부를 줄여 working set을 메모리에 맞추는 것이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Swap Storm | WSS 합이 RAM 초과 | DOP 축소, process suspend | swap in/out MB/s |
| Tail Latency 증가 | major fault가 요청 경로에 발생 | memory reservation, mlock | p99 latency, major fault |
| OOM Kill | overcommit 과다 | cgroup memory.max, oom_score 조정 | OOM event count |

> 요약: 운영 리스크는 swap storm, tail latency, OOM으로 나타나며 cgroup과 admission control로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Fault Rate | major fault/sec 기준선 대비 50% 이하 | vmstat, perf, sar |
| CPU 회복 | CPU utilization 70% 이상, iowait 10% 이하 | top, mpstat |
| 메모리 적합 | WSS 합 <= RAM 80% | working set sampling, RSS 분석 |

> 요약: 스레싱 해소는 major fault 감소, CPU utilization 회복, WSS와 RAM의 적합성으로 확인한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. PFF(Page Fault Frequency) 상한을 설정해 fault rate가 임계값을 넘으면 resident set 확대 또는 프로세스 suspend를 수행함.
2. 컨테이너 환경은 cgroup memory.max, memory.high, swap 제한을 설정해 한 workload의 page fault storm이 노드 전체로 번지지 않게 함.
3. 배치·분석 작업은 working set 산정 후 RAM 80% 이내 admission control을 적용하고 초과 시 queue 대기로 전환함.

**결론 (2줄):**
- 기술사 판단: CPU utilization 급락과 major fault/sec 급증이 함께 보이면 CPU 증설보다 DOP 축소와 working set 제어가 우선임.
- 향후 방향: eBPF memory trace와 PSI(Pressure Stall Information) 기반 자동 admission control로 스레싱을 사전 감지함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "스레싱을 설명하시오" | DOP 증가에서 CPU utilization drop까지 흐름 | 정상 페이징과 스레싱 비교 |
| 요구사항 명시형 | "방안을 제시하시오", "원인을 분석하시오" | page fault storm 진단 절차 | PFF, working set, cgroup 대응 기준 |

> 요약: 원인 분석형은 CPU보다 major fault와 WSS 초과 여부를 먼저 제시해야 한다.
