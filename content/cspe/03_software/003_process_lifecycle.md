---
title: "프로세스 생성·종료·상태 전이 (Process Lifecycle)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 3
---

# 📖 【암기용】 개념 완전 이해

> 목적: 프로세스 생명주기를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 프로세스가 생성부터 종료까지 거치는 상태 변화
- **왜 필요한가**: 운영체제는 CPU를 쓸 수 있는 프로세스, I/O를 기다리는 프로세스, 종료 후 정리 대기 중인 프로세스를 구분해야 한다.
- **핵심 직관**: 프로세스는 입장 대기, 작업 중, 창구 대기, 퇴장 처리 같은 상태표를 따라 이동한다.

## 깊이 이해
- **배경·문제의식**: 프로그램 파일은 디스크에 있는 정적 객체이고, 프로세스는 메모리에 적재되어 CPU 시간을 받는 동적 객체이다. OS는 상태 전이를 추적해야 CPU idle, zombie 누적, orphan 방치를 막는다.
- **작동 원리**: new에서 PCB가 생성되고, ready queue에 들어가면 CPU 배정을 기다린다. running은 CPU를 점유한 상태, waiting은 I/O·lock·event 대기 상태, terminated는 실행 종료 후 자원 회수 단계이다.
- **비유**: 병원 접수와 같다. 접수(new), 대기(ready), 진료(running), 검사 대기(waiting), 수납 후 퇴장(terminated) 순서로 상태가 이동한다.
- **구체 예시**: Unix에서 부모가 fork 후 wait를 호출하지 않으면 자식 종료 정보가 process table에 남아 zombie가 된다. 부모가 먼저 종료되면 init/systemd가 orphan을 입양한다.
- **흔한 오해·주의점**: terminated와 zombie는 다르다. 실행은 끝났지만 부모가 exit status를 회수하지 않으면 zombie는 PID와 종료 코드가 남는다.

## 연결 개념
- fork/exec/wait: Unix 프로세스 생성·교체·회수
- 스케줄링 큐: ready queue와 wait queue 관리
- PCB: 상태·부모·자식·종료 코드 저장

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 상태 이름 암기가 아니라 CPU 배정 가능성, I/O 대기, 부모-자식 회수 책임을 연결한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 프로세스 생명주기는 new, ready, running, waiting, terminated 상태와 그 전이 조건을 관리하는 OS 실행 모델이다.
> 2. **가치**: CPU 활용률, 응답시간, 자원 회수를 상태별 queue와 event로 통제한다.
> 3. **판단 포인트**: fork/exec/wait, zombie/orphan, blocking I/O, preemption을 상태 전이 관점으로 설명해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| OS 상태 모델 이해 확인 | new, ready, running, waiting, terminated | 상태명만 나열하고 전이 조건 누락 |
| Unix 프로세스 제어 이해 확인 | fork, exec, wait, exit, signal | fork와 exec 역할 혼동 |
| 자원 회수 리스크 판단 확인 | zombie, orphan, PID table, exit status | zombie를 실행 중 프로세스로 오해 |

> 요약: 이 문제는 상태 전이 조건과 자원 회수 책임을 함께 묻는다.

---

## Ⅰ. 개요 및 필요성

프로세스 생명주기는 생성·실행·대기·종료 상태 전이다.
운영체제는 상태별 queue로 CPU 배정 대상과 I/O 대기 대상을 분리하고, 종료 시 PCB·메모리·파일 자원을 회수한다.
상태 추적이 부정확하면 CPU idle 증가, zombie 누적, PID 고갈, 응답시간 증가가 발생한다.

---

## Ⅱ. 구조 및 구성요소

```text
Program File -> New -> Ready Queue -> Running
Running -> Waiting / Ready / Terminated
Waiting -> Ready
Terminated -> Parent wait -> Resource Reclaim
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| New | PCB 생성, 주소공간 준비 | fork/CreateProcess 진입 |
| Ready | CPU 배정 대기 | ready queue, priority |
| Running | CPU 명령 실행 | time slice, trap 발생 |
| Waiting | I/O, lock, event 대기 | wait queue, wakeup |
| Terminated | 종료 코드 보존 후 회수 | wait 호출 전 zombie 가능 |

> 요약: 생명주기는 실행 가능 여부와 자원 회수 단계에 따라 queue를 이동하는 모델이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
fork/CreateProcess -> PCB 생성 -> Ready 등록
-> Scheduler Dispatch -> Running
-> I/O 요청이면 Waiting -> Event 완료 -> Ready
-> exit -> Zombie/Terminated -> wait -> 자원 회수
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 프로세스 생성과 PID/PCB 할당 | PID table 사용률 |
| 2 | exec로 프로그램 이미지 적재 | address space mapping |
| 3 | scheduler가 ready에서 running으로 dispatch | dispatch latency |
| 4 | I/O·lock 대기 시 waiting으로 이동 | blocked time |
| 5 | exit 후 부모 wait로 종료 상태 회수 | zombie count 0건 |

> 요약: 프로세스는 CPU 필요 여부와 event 완료 여부에 따라 ready, running, waiting을 반복하다가 wait로 회수된다.

---

## Ⅳ. 특징

| 구분 | 정상 상태 전이 | 예외 상태 | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 생성 | fork -> exec -> ready | exec 실패, 권한 오류 | errno, audit log |
| 실행 | ready -> running | time slice 만료 | run queue latency |
| 대기 | running -> waiting | lock wait 장기화 | blocked time p95 |
| 종료 | exit -> wait -> 회수 | zombie, orphan | zombie count, PID 사용률 |

> 요약: 상태 전이는 CPU 스케줄링뿐 아니라 종료 회수와 PID 자원 관리까지 포함한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단순 실행/종료 관점 | 5상태 전이 모델 | OS queue 분석 필요 여부 |
| 비용/성능 | blocking 호출 방치 | waiting 분리와 wakeup 관리 | CPU utilization, wait time |
| 운영/위험 | 부모 wait 누락 | zombie 회수 정책 | PID 고갈 방지 |

> 요약: 상태 전이 모델은 CPU 시간과 자원 회수를 같은 표로 관리하게 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| zombie 누적 | 부모가 wait 미호출 | SIGCHLD handler, waitpid loop | zombie count 0건 |
| orphan 방치 | 부모 프로세스 선종료 | systemd supervisor, re-parenting 확인 | orphan process count |
| ready queue 증가 | CPU core 대비 runnable 과다 | worker 수 제한, backpressure | load average/core |

> 요약: 생명주기 리스크는 종료 회수 누락과 runnable 폭증이며, supervisor와 queue 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| CPU 활용 | idle 20% 이하 또는 정책 기준 | sar, mpstat |
| 대기 시간 | blocked p95 50ms 이하 | eBPF off-CPU profiling |
| 종료 회수 | zombie 0건 유지 | ps, procfs, alert |

> 요약: 상태 관리 품질은 CPU idle, blocked time, zombie count로 확인한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 프로세스 생성 경로에 fork/exec 실패 로그, exit code, signal 원인을 남겨 장애 분석 시간을 30분 이내로 제한
2. long-running daemon은 systemd Restart 정책과 watchdog을 설정하고, SIGCHLD handler로 자식 종료를 즉시 회수
3. eBPF off-CPU profiling으로 waiting 원인을 I/O, lock, sleep으로 분류하고 blocked p95를 SLO 지표에 포함

**결론 (2줄):**
- 기술사 판단: CPU 병목이면 ready/running 지표, I/O 병목이면 waiting 지표, 회수 문제이면 zombie/orphan 지표를 우선 확인함
- 향후 방향: 컨테이너·마이크로서비스 환경에서는 PID namespace와 supervisor 정책까지 포함해 생명주기를 설계해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "프로세스 상태 전이를 설명하시오" | 5상태 전이와 fork/exec/wait | zombie·orphan 사례 |
| 요구사항 명시형 | "운영 문제 대응 방안을 제시하시오" | queue별 병목 진단 흐름 | PID 고갈·대기시간 대응 |

> 요약: 설명형은 상태 전이를, 운영형은 queue 지표와 종료 회수 리스크를 중심으로 작성한다.
