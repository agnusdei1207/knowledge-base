---
title: "프로세스 생애주기 (Process Lifecycle)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-software"
weight: 3
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **정의**: 프로세스가 생성(New)되어 준비(Ready), 실행(Running), 대기(Waiting/Blocked) 상태를 거쳐 종료(Terminated)되기까지의 **상태 변화 과정**.
- **핵심 직관**: 식당의 고객이 입장(New)해서 줄을 서고(Ready), 테이블에 앉아 먹다가(Running), 주문한 음식을 기다리고(Blocked), 계산하고 나가는(Terminated) 과정과 같음.
- **왜 중요한가**: OS 스케줄러가 '누구에게 CPU를 줄 것인가'를 결정하기 위한 가장 기초적인 판단 근거가 되기 때문임.

## 깊이 이해
- **5단계 상태 모델**:
    - **New**: 프로그램이 메모리에 적재되어 PCB를 할당받은 단계. (아직 승인은 안 됨)
    - **Ready**: CPU만 주어지면 즉시 실행 가능한 상태. (준비 큐에서 대기)
    - **Running**: 실제 CPU를 점유하여 명령어를 실행 중인 상태.
    - **Waiting (Blocked)**: I/O 작업 완료 등 특정 이벤트가 발생할 때까지 CPU를 반납하고 기다리는 상태.
    - **Terminated**: 실행이 완료되어 자원을 반납 중인 상태.
- **지연 상태 (Suspended State)**: 메모리가 부족하면 OS가 프로세스를 통째로 디스크(Swap 영역)로 쫓아냄. 이때 'Suspended Ready'나 'Suspended Blocked' 상태가 추가됨.
- **상태 전이의 트리거**:
    - **Dispatch**: Ready -> Running (스케줄러의 선택)
    - **Timeout**: Running -> Ready (할당 시간 만료)
    - **Event Wait**: Running -> Waiting (I/O 요청 등)
    - **Event Occurrence**: Waiting -> Ready (I/O 완료 등)

## 연결 개념
- **PCB (002)**: 프로세스 상태 정보가 저장되는 장소.
- **스케줄링 (004)**: Ready 상태의 프로세스 중 하나를 골라 Running으로 만드는 알고리즘.
- **가상 메모리 (016)**: Suspended 상태와 밀접한 연관(Swapping).

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 프로세스 상태 전이는 OS가 한정된 자원(CPU, Memory)을 다수의 프로세스에게 공정하고 효율적으로 배분하기 위한 **상태 관리 메커니즘**임.
> 2. **기술적 핵심**: Running 상태에서 Blocked로의 자발적 전이와 Ready로의 비자발적 전이(Timeout)를 구분하여 이해하는 것이 스케줄링 최적화의 시작임.
> 3. **운영 가치**: 상태 전이도를 통해 시스템의 병목(I/O Bound vs CPU Bound)을 진단하고 지연 상태(Suspended) 관리를 통해 메모리 스레싱을 방지함.

## Ⅰ. OS 스케줄링의 기초, 프로세스 생애주기 개요
- **정의**: 프로세스가 생성된 시점부터 종료될 때까지 OS의 제어 하에 변화하는 동적인 상태의 집합.
- **목적**: CPU 이용률 극대화, 응답 시간 최소화, 자원 활용의 효율성 확보.

## Ⅱ. 프로세스 5단계 상태 전이도 (State Transition Diagram)

### 1. 상태 전이 메커니즘 (ASCII Diagram)
```text
      [입입]                   [스케줄러 디스패치]
        │                         ┌─────────┐
        ▼           Timeout       │         │          Exit
      New  ──────>  Ready  <──────┤ Running ├───────> Terminated
                    ▲  │          │         │
                    │  └──────────┘         │
                    │       [I/O Wait]      │
                    │                       │
                    └──────  Waiting  <─────┘
                           (Blocked)
```

### 2. 주요 상태 및 전이 조건 기술
| 상태/전이 | 상세 설명 | 트리거 (Trigger) |
|:---:|:---|:---|
| **Admitted** | New -> Ready | 커널이 프로세스 생성을 승인하고 메모리 할당 |
| **Dispatch** | Ready -> Running | 준비 큐의 프로세스 중 하나를 CPU에 할당 |
| **Timeout** | Running -> Ready | 할당된 Time Slice(Quantum)를 모두 소모 (Preemption) |
| **I/O Wait** | Running -> Blocked | 입출력 요청, 자원 할당 대기 (자발적 반납) |
| **Wake-up** | Blocked -> Ready | I/O 완료 신호 수신, 인터럽트 발생 |

## Ⅲ. 성능 최적화를 위한 7단계 모델 (Suspended State 포함)

### 1. 지연(Suspended) 상태의 등장 배경
- 시스템 메모리(RAM) 부족 시, 실행 가능성이 낮은 프로세스를 디스크의 **Swap 영역**으로 이동(Swap-out)시켜 가용 메모리를 확보하기 위함.

### 2. 추가된 상태 기술
- **Suspended Ready**: Ready 상태에서 메모리를 잃고 디스크에 머무는 상태.
- **Suspended Blocked**: Blocked 상태에서 메모리를 잃고 디스크에 머무는 상태. (이 상태에서 I/O가 완료되면 Suspended Ready로 전이됨)

## Ⅳ. 프로세스 생애주기 관리의 특수 사례

- **좀비 프로세스 (Zombie)**: 자식 프로세스가 종료되었으나, 부모 프로세스가 종료 상태(`exit code`)를 회수하지 않아 PCB만 남은 상태.
- **고아 프로세스 (Orphan)**: 부모 프로세스가 자식보다 먼저 종료되어, 부모가 `init` (PID 1) 프로세스로 변경된 상태.
- **스레싱 (Thrashing)**: 빈번한 Swap-in/out으로 인해 프로세스가 Running 상태보다 Suspended 상태에 머무는 시간이 길어져 시스템 성능이 급락하는 현상.

## Ⅴ. 스케줄러 계층과 프로세스 상태의 관계

| 계층 | 역할 | 관련 상태 |
|:---:|:---|:---|
| **장기 스케줄러** | 어떤 작업을 Ready 큐에 넣을지 결정 (Job Scheduler) | New -> Ready |
| **중기 스케줄러** | 메모리 부족 시 프로세스를 Swap 영역으로 이동 | Suspended 관련 |
| **단기 스케줄러** | 다음 실행할 프로세스 선택 (CPU Scheduler) | Ready -> Running |

## Ⅵ. 기술사 관점의 결론
- 프로세스 생애주기 이해는 **커널 튜닝 및 애플리케이션 성능 최적화**의 기본임.
- 실무적으로는 `top`, `ps`, `vmstat` 등의 도구를 통해 프로세스 상태 비중을 모니터링하여, 시스템이 CPU Bound(Running 비중 높음)인지 I/O Bound(Blocked 비중 높음)인지를 판단하고 적절한 자원 증설이나 아키텍처 개선(비동기 I/O 도입 등)을 결정해야 함.

---
### 🔀 문제 유형별 목차 전환
| 유형 | 강조 포인트 | 추천 목차 구성 |
|:---:|:---|:---|
| **원각형** | 5단계/7단계 상태 전이 | Ⅱ.5단계 모델, Ⅲ.7단계(Suspended) |
| **관리형** | 좀비/고아 프로세스 대응 | Ⅳ.특수사례, Ⅵ.실무모니터링 방안 |
| **스케줄링형** | 스케줄러 계층과의 연계 | Ⅴ.스케줄러 계층별 역할과 상태 |
