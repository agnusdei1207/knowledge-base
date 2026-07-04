---
title: "프로세스 생성·종료·상태 전이 (Process Lifecycle)"
date: "2026-07-04"
tags:
  - "cspe-software"
weight: 3
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: 프로세스가 생성되어 실행, 대기를 거쳐 종료될 때까지 거치는 상태 변화 과정
- **왜 필요한가**: CPU는 한 번에 하나의 상태만 실행할 수 있으므로, 어떤 프로세스가 CPU를 기다리고 있고, 어떤 프로세스가 입출력을 기다리는지 명확히 구분해야 OS가 효율적으로 스케줄링할 수 있다.
- **핵심 직관**: 병원 진료와 같다. 접수(New) -> 대기실(Ready) -> 의사 진찰(Running) -> 검사 대기(Waiting/Blocked) -> 완료 및 귀가(Terminated).

## 핵심 용어 정리

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| Ready (준비) | CPU를 할당받기 위해 기다리는 상태 | 의사 진찰을 기다리는 대기실 환자 |
| Running (실행) | CPU를 할당받아 실제 명령어가 실행 중인 상태 | 의사와 면담 중인 환자 |
| Blocked/Waiting (대기) | I/O 작업 완료 등 이벤트를 기다리는 상태 | 엑스레이 결과를 기다리는 환자 |
| Suspend (지연) | 메모리가 부족하여 디스크(Swap)로 쫓겨난 상태 | 병실이 없어 집에서 대기하는 환자 |

## 깊이 이해
- **배경·문제의식**: 프로세스가 I/O를 요청하면 응답이 올 때까지 CPU를 점유하고 있는 것은 낭비다. OS는 상태를 정의하여 I/O를 기다리는 프로세스는 CPU를 뺏어(Blocked) 다른 준비된(Ready) 프로세스에 넘긴다.
- **작동 원리**: 주요 상태 전이는 Dispatch(Ready->Running), Timeout(Running->Ready), Block(Running->Blocked), Wakeup(Blocked->Ready)이다.
- **비유**: Running 상태의 프로세스가 하드디스크에서 파일을 읽어달라고 요청(I/O 시스템콜)하면, OS는 "결과 나올 때까지 비켜"하며 Blocked 상태로 보낸다. 그 사이 Ready 큐에 있던 다른 프로세스를 Running으로 올린다(Dispatch).
- **구체 예시**: `sleep(1)` 함수를 호출하면 프로세스는 즉시 Running에서 Blocked(또는 Sleep) 상태가 되고, 1초 후 타이머 인터럽트에 의해 Wakeup되어 Ready 상태로 간다.
- **흔한 오해·주의점**: Blocked 상태에서 이벤트가 완료되면 바로 Running 상태가 되는 것이 아니다! 반드시 Ready 상태(준비 큐)로 가서 순서를 다시 기다려야 한다.

## 연결 개념
- 스케줄링 알고리즘 (004 참조) — Ready 큐에서 Running으로 올릴 프로세스를 고르는 방법
- 가상 메모리 (016 참조) — Suspend 상태와 직결된 Swap 메커니즘

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 프로세스 상태 전이는 OS가 다중 프로그래밍을 위해 프로세스의 생애주기(New-Ready-Running-Blocked-Terminated)를 관리하는 메커니즘이다.
> 2. **가치**: I/O 대기 프로세스를 CPU 스케줄링 후보에서 배제하여 CPU 활용도(Utilization)를 극대화한다.
> 3. **판단 포인트**: 시스템 과부하 시 메모리 고갈을 막기 위해 Suspend(지연) 상태를 적절히 활용하여 디스크 스왑(Swap)으로 통제해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 프로세스 생명주기 제어 원리 이해 | 5가지 기본 상태 + 2가지 지연(Suspend) 상태 포함 여부 | Blocked에서 Running으로 직접 전이(오답) |
| 이벤트와 상태 전이 메커니즘 매핑 | Dispatch, Timeout/Preemption, Block, Wakeup 트리거 | 상태 명칭만 적고 전이 조건 누락 |
| 시스템 과부하(메모리 고갈) 상황 대처 | Suspend-Ready, Suspend-Blocked 스왑 인/아웃 | 메모리 관리 관점 누락 |

> 요약: 기본 5상태에 메모리 부족 시 발생하는 지연(Suspend) 2상태를 추가한 7상태 모델로 시스템 자원 병목 통제를 설명한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 프로세스가 생성(New)부터 종료(Terminated)에 이르기까지 CPU 할당 및 입출력 이벤트에 따라 겪는 상태 변화 모델
- 배경: CPU와 I/O 장치 간의 속도 차이가 크기 때문에, I/O 대기 프로세스가 CPU를 점유하는 비효율 발생
- 필요성: 시스템 자원의 효율적 분배, 다중 프로그래밍 정도(Degree of Multiprogramming) 유지, 기아(Starvation) 방지를 위해 상태 추적 필수

---

## Ⅱ. 구조 및 구성요소

```text
       New (생성)
           | (Admit)
           v
       Ready (준비) <----(Wakeup)---- Blocked (대기)
        |  ^                           ^
(Dispatch) | (Timeout)                 | (Block)
        v  |                           |
       Running (실행) -----------------+
           | (Exit)
           v
       Terminated (종료)
```

| 상태 | 설명 | 보관 위치 |
|:---|:---|:---|
| Ready (준비) | 메모리에 적재되어 CPU 할당을 기다림 | Ready Queue (메모리) |
| Running (실행) | CPU를 점유하여 명령어 실행 중 | CPU Registers |
| Blocked (대기) | I/O 등 특정 이벤트 완료를 기다림 | Wait/Device Queue (메모리) |
| Suspend-Ready | Ready 상태이나 메모리 부족으로 디스크로 쫓겨남 | Swap Space (디스크) |
| Suspend-Blocked| Blocked 상태이나 메모리 부족으로 디스크로 쫓겨남 | Swap Space (디스크) |

> 요약: 활성 상태(Ready/Running/Blocked)는 메인 메모리에 존재하며, 메모리 부족 시 프로세스를 디스크로 내리는 Suspend 상태가 추가된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
프로세스 생성(New) -> 메모리 할당(Ready)
  -> 스케줄러 선택(Dispatch) -> 실행(Running)
  -> [분기 1] I/O 요청 -> Block(Blocked) -> I/O 완료 -> Wakeup(Ready)
  -> [분기 2] 할당 시간 만료 -> Timeout(Ready)
  -> 완료 시 종료(Terminated)
```

- 1단계 [Dispatch]: OS 스케줄러가 Ready 큐에 있는 프로세스 중 하나를 선택해 CPU 할당 (상태: Ready → Running)
- 2단계 [Block / Wait]: Running 중인 프로세스가 디스크 읽기 등 I/O 요청 시 대기 큐로 이동 (상태: Running → Blocked)
- 3단계 [Wakeup]: I/O 하드웨어 인터럽트 발생 시, 대기 중이던 프로세스를 Ready 큐로 이동 (상태: Blocked → Ready)
- 4단계 [Timeout / Preemption]: 라운드 로빈 스케줄링 등에서 할당 시간 만료 시 CPU를 뺏김 (상태: Running → Ready)

> 요약: 스케줄러와 하드웨어 인터럽트가 협력하여 프로세스를 큐와 큐 사이로 끊임없이 전이시킨다.

---

## Ⅳ. 특징

- 제어 주체: 프로세스의 상태 전이는 스스로 결정하지 않으며, 운영체제의 스케줄러와 인터럽트 핸들러가 통제함
- 오버헤드 동반: Ready ↔ Running 전환 시 필연적으로 PCB 저장 및 복구(Context Switching) 비용 발생
- 큐(Queue) 기반 관리: Ready Queue, I/O Device Queue 등 다수의 자료구조를 통해 상태별 프로세스를 그룹 단위로 추적

> 요약: 상태 전이는 철저히 OS 주도하에 인터럽트 기반으로 이루어지며, 시스템 자원(CPU, 디스크) 상태를 반영한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 활성 상태 (Active) | 지연 상태 (Suspend) | 전환 기준 |
|:---|:---|:---|:---|
| 거주 위치 | 메인 메모리 | 디스크 (Swap Space) | 시스템 메모리 가용량 |
| 전이 조건 | Admit, Wakeup | Suspend (Swap-out) | 메모리 임계치(Threshold) 미달 시 |
| 복귀 조건 | - | Resume (Swap-in) | 메모리 확보 또는 중요도 높을 시 |

> 요약: 다중 프로그래밍 한계치를 넘어서면, OS는 강제로 Blocked 상태의 프로세스부터 Suspend하여 메모리를 확보한다.

**리스크·대응 (기본은 불릿):**
- 기아(Starvation) 상태: 특정 프로세스가 우선순위 밀림으로 영구 대기 → 에이징(Aging) 기법 적용 (지표: Ready Queue 체류 시간)
- 스래싱(Thrashing): Suspend ↔ Resume 교체가 너무 잦아짐 → Working Set 설정 및 동시 실행 수 조절 (지표: Page Fault Rate)

**도입 후 점검 지표 (기본은 불릿):**
- 성능/효율: Ready Queue 평균 대기 시간, CPU 활용률(Utilization)
- 품질/운영: Swap-in/Swap-out 빈도(pswpin/pswpout)

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. I/O 집약적 프로세스 최우선 할당: I/O 바운드가 Ready 상태가 되면 우선 Running시켜 장치 가동률을 높임
2. 메모리 고갈 대비 모니터링: OOM(Out of Memory) Killer 작동 전 Swap 사용률을 모니터링해 유휴 프로세스 우선 정리
3. 헬스체크 및 프로세스 재기동: 영원히 Blocked에 머무는 데드락 탐지 시, 프로세스 강제 종료 후 재기동

**결론 (2줄):**
- 기술사 판단: 프로세스 상태 전이는 단순히 이론적 모델이 아니라, 시스템 부하(Load Average)와 자원 병목을 진단하는 핵심 프레임워크다.
- 향후 방향: 컨테이너 환경에서는 프로세스 수준을 넘어 Pod의 생명주기(Pending, Running, Succeeded, Failed) 관리로 확장되고 있다.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "프로세스 상태 전이를 설명하시오" | 5상태/7상태 모델 구조도, 전이 조건 | Suspend 상태의 필요성, 큐(Queue) 연계 |
| 문제점 대책형 | "메모리 부족 시 상태 전이와 대책" | Suspend 상태로의 전이 흐름 집중 | Thrashing 원인, Swap 최적화 방안 |
