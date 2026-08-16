---
sidebar:
  order: 3
  label: "003. 프로세스 생성•종료•상태 전이 (Process Lifecycle)"
  badge:
    text: "미출 • 30%"
    variant: note
title: 프로세스 생성•종료•상태 전이 (Process Lifecycle)
date: "2026-08-13T12:46:00+09:00"
tags: [notes-software]
weight: 3
extra:
  question_no: "003"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "프로세스 상태 전이는 운영체제 기본 흐름"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Process Lifecycle**: 프로세스가 생성(New)부터 준비(Ready), 실행(Running), 대기(Blocked), 종료(Terminated) 상태를 순환하는 커널 상태 제어 모델.
- **fork() / exec()**: 부모 주소 공간을 복제(fork) 후, 새로운 바이너리 이미지로 교체(exec)하는 POSIX 프로세스 생성 시스템 콜.
- **Zombie Process**: 실행 완료(exit) 후, 부모 프로세스의 자원 수거(wait)가 이루어지지 않아 PID 및 PCB 메타데이터가 커널에 잔존하는 상태.

- **프로세스 생명주기(Process Lifecycle)**: 프로세스가 생성(New)되어 준비(Ready), 실행(Running), 대기(Blocked/Waiting), 종료(Terminated) 상태로 전이하는 전체 생명주기.
- **좀비 프로세스(Zombie Process)**: 실행 종료 후 자원은 반납했으나 부모 프로세스가 wait() 시스템 콜로 종료 상태(Exit Status)를 수거하지 않아 프로세스 테이블에 남아있는 프로세스.
- **상태 전이(State Transition)**: 스케줄러 디스패치, 타이머 인터럽트(선점), I/O 요청 및 완료 이벤트에 의해 프로세스의 실행 상태가 준비·실행·대기로 바뀌는 과정.
- **대기 큐(Device / Wait Queue)**: 특정 I/O 장치나 이벤트 발생을 대기하는 블록 상태의 PCB 포인터들을 관리하는 커널 연결 리스트.
</details>

- 정의: 생성부터 준비•실행•대기•종료까지의 **상태 전이** 관리
- 배경: 상태 구분 없이는 CPU 대기와 이벤트 대기의 **선택 기준 부재**

#### 한줄 요약
- CPU 할당과 이벤트 대기에 기반한 프로세스 상태 전이 메커니즘.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Ready State**: CPU 스케줄러의 선택(Dispatch)을 받아 즉시 런타임 구동 가능한 상태로 Ready Queue 상에 상주.
- **Running State**: CPU 제어권을 최종 점유하여 명령어를 인스턴스화하고 연산을 수행 중인 상태.
- **Blocked State**: I/O 요청 수신 또는 이벤트 완료 신호 수신 전까지 CPU 점유 권한을 즉시 상각하고 Wait Queue로 이탈한 상태.

</details>

- CPU를 점유하여 실제 명령어를 연산하는 오직 단 하나의 **Running State** (단일 코어 기준)
- CPU 디스패치를 대기하는 **Ready State** vs I/O 완료 이벤트를 대기하는 **Blocked State**의 명확한 큐 이원화
- 부모의 **wait()** 호출로 자식 종료 상태와 **좀비** 항목 회수

#### 한줄 요약

- 실행 상태만 CPU를 점유하고 준비 상태와 대기 상태는 자원을 기다린다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Ready Queue**: CPU 디스패치 대기 중인 PCB 포인터들이 정렬 연결된 커널 파이프라인 큐.
- **Wait/Device Queue**: 특정 디바이스 I/O(SATA, NIC 등) 또는 시그널 완결을 대기하는 PCB 포인터 큐.
- **PID(Process Identifier)**: OS 내에서 프로세스를 유일하게 식별하는 정수형 고유 식별자.

</details>

```text
                 [PCB]
                 /   \
                /     \
         [준비 큐]     [대기 큐]
             |
             |
         [스케줄러]
             |
             |
            [CPU]
```

선의 의미: PCB 메타데이터가 OS 스케줄러 상태 판정에 따라 Ready Queue 또는 Wait Queue로 이동 배치된 후 CPU 코어로 할당 디스패치되는 라이프사이클.

| 구성요소 | 책임 |
|:---|:---|
| PCB | **PID**, Process State(Ready/Running/Waiting), Context(PC/SP) 메타 기록 |
| Ready Queue | 스케줄링 알고리즘(CFS, Priority)에 따라 디스패치 대기 **PCB** 래칭 |
| OS Scheduler | Ready Queue 내 최적 PCB 선택 및 CPU 코어 **Dispatch** 제어 |
| CPU | 선택된 프로세스의 명령어(Instruction) 연산 및 레지스터 인가 |
| Wait Queue | I/O 버스 응답, 타이머 알람, Mutex 대기 등 이벤트 기반 **Blocked PCB** 래칭 |

#### 한줄 요약

- PCB, 준비 큐, 대기 큐, 스케줄러, CPU의 관리 구조이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Dispatch**: Ready Queue 내의 최상위 프로세스에게 CPU 제어권을 위임하여 Running 상태로 전환하는 스케줄러 동작.
- **Timeout/Preempt**: 타임 슬라이스 만료 시 CPU 제어권을 회수하여 Running에서 Ready 상태로 강제 복귀시키는 동작.

</details>

```text
[생성 완료•PCB 등록]
          │
          ▼
      [준비 상태] ◄───────────────┐
          │                       │
          │ 1. 디스패치           │ 2. 선점
          ▼                       │
      [실행 상태] ────────────────┘
        │      │
        │      └── 3. I/O 대기 전환 ──► [대기 상태]
        │                                  │
        │                         4. 완료 이벤트
        │                                  │
        │                                  └──► [준비 상태]
        │
        └── 5. 프로세스 종료 ──► [종료 상태]
```

### 동작 원리

1. 디스패치: 준비 큐에서 선택해 실행 상태로 전환
2. 선점: 시간 할당량 만료 시 준비 상태로 복귀
3. I/O 대기 전환: I/O 요청 후 CPU를 반납하고 대기
4. 완료 이벤트: 완료 인터럽트로 준비 큐에 재배치
5. 프로세스 종료: 실행 자원을 해제하고 종료 상태 기록

#### 한줄 요약

- 디스패치, 선점, I/O 대기 전환, 완료 이벤트, 프로세스 종료가 상태 전이를 만든다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Orphan Process**: 부모 프로세스가 자식보다 먼저 종료되어 init/systemd(PID 1) 프로세스가 부모로 재지정된 상태.

</details>

| 비교 항목 | Ready State (준비) | Running State (실행) | Blocked State (대기) |
|:---|:---|:---|:---|
| CPU 점유 여부 | 미점유 (스케줄러 선택 대기) | **점유 중** (실제 연산 수행) | 미점유 (이벤트 발생 대기) |
| 상주 큐 위치 | **Ready Queue** | CPU Core Register | **Device / Wait Queue** |
| 다음 전이 상태 | Running (Dispatch 시) | Ready (Preempt 시) / Blocked | Ready (I/O Wakeup 인터럽트 수신 시) |

#### 한줄 요약

- CPU 대기는 준비 상태, 장치•이벤트 대기는 대기 상태이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **waitpid()**: 부모 프로세스가 자식 PID의 종료 상태를 넌블로킹(WNOHANG) 또는 블로킹 방식으로 수거하여 좀비를 예방하는 함수.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 부모 미수거로 인한 **좀비 프로세스** 누적 | SIGCHLD 처리와 **waitpid()** 호출 | PID와 종료 상태 항목 회수 |
| I/O 무한 대기로 인한 대기 상태 고착 | I/O **타임아웃**과 취소 경로 설계 | 무기한 대기 방지 |
| 프로세스 폭증으로 인한 PID•메모리 고갈 | 사용자별 **생성 한도**와 감시 적용 | 운영체제 자원 고갈 억제 |

> 사례: Linux **systemd(PID 1)** 기반 Orphan Process 자식 자동 수거 및 **waitpid** 시그널 핸들링 인프라 구축

#### 한줄 요약

- 부모 프로세스가 포크 시스템 호출로 자식을 생성하고 웨이트 시스템 호출로 종료 상태를 회수한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **프로세스 수명주기 관리 기준(Process Lifecycle Management Criteria)**: 자원 해제 무결성, 좀비 방지, I/O 타임아웃 세팅에 따른 관리 체계.

</details>

- 자식 종료는 **waitpid()**로 회수하고 장기 대기는 **타임아웃** 적용

#### 한줄 요약
- 자원 해제 무결성 보장 및 좀비 프로세스 방지를 위한 상태 관리 체계 적용.
