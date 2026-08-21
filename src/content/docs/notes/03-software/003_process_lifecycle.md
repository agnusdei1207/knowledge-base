---
sidebar:
  order: 3
  label: "003. 프로세스 생성•종료•상태 전이"
  badge:
    text: "미출 · 30%"
    variant: note
title: "프로세스 생성•종료•상태 전이 (Process Lifecycle)"
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

- **Process Lifecycle(프로세스 생명주기)**: 프로세스가 생성(New)되어 준비(Ready), 실행(Running), 대기(Blocked/Wait), 종료(Terminated) 상태를 거치며 운영체제 자원을 점유하고 반납하는 전체 실행 주기.
- **fork() / exec()**: 부모 프로세스의 주소 공간을 복제(fork)하여 자식 프로세스를 생성하고, 새로운 바이너리 이미지로 교체(exec)하여 실행하는 프로세스 생성 시스템 콜.
- **Zombie Process(좀비 프로세스)**: 프로세스 실행을 마치고 종료(exit)되었으나 부모 프로세스가 `wait()` 시스템 콜을 호출하여 종료 상태 코드를 회수하지 않아 커널 프로세스 테이블(PID)에 남아 있는 상태.
- **State Transition(상태 전이)**: 스케줄러 디스패치, 타이머 만료(선점), I/O 요청 및 완료 이벤트에 의해 프로세스의 실행 상태가 변경되는 메커니즘.

</details>

- 정의/개념: 프로세스가 생성부터 준비, 실행, 대기, 종료 상태를 능동적으로 전이하며 운영체제 커널의 스케줄링 및 자원 관리를 받는 프로세스 상태 제어 아키텍처
- 배경/필요성: 다중 프로그래밍 환경에서 CPU 연산과 입출력(I/O) 작업을 효율적으로 다중화하고 시스템 자원 활용률 및 응답성을 극대화하기 위해 명확한 상태 전이 관리 필요

#### 한줄 요약

- OS 커널이 프로세스를 생성·준비·실행·대기·종료 5단계로 분류하여 스케줄링 및 자원을 최적화하는 제어 기제

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Ready State(준비 상태)**: CPU를 할당받으면 즉시 실행 가능한 상태로, Ready Queue에 적재되어 스케줄러의 디스패치를 대기.
- **Running State(실행 상태)**: CPU 제어권을 획득하여 명령어를 실제로 실행 중인 상태(단일 코어당 1개 프로세스만 실행).
- **Blocked State(대기 상태)**: I/O 완료, 세마포어 획득, 시그널 수신 등 특정 외부 이벤트가 발생할 때까지 CPU를 반납하고 대기하는 상태.

</details>

- 단일 CPU 코어 기준 **실행 상태(Running)** 는 시점당 단 하나의 프로세스에만 배정
- CPU 스케줄러 디스패치를 대기하는 **준비 상태(Ready)** 와 외부 이벤트 대기를 위한 **대기 상태(Blocked)** 의 큐 분리 운영
- 프로세스 종료 시 부모 프로세스의 `wait()`/`waitpid()` 호출을 통한 자식 프로세스 PCB 자원 정리 및 **좀비 프로세스 방지** #### 한줄 요약

- **5단계 상태 분리·Ready/Wait 큐 이원화·디스패치/선점/I/O 이벤트 기반 상태 전이** ## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Ready Queue(준비 큐)**: 메모리에 적재되어 CPU 할당을 대기하는 준비 상태의 PCB 연결 리스트.
- **Wait Queue(대기 큐)**: I/O 디바이스 또는 동기화 이벤트를 대기하는 프로세스들의 PCB 연결 리스트.
- **PID(Process Identifier)**: 운영체제가 시스템 내 프로세스를 고유하게 식별하기 위해 부여하는 고유 정수 번호.

</details>

```text
[ 프로세스 생명주기 및 상태 전이 아키텍처 ]
                 [ OS 스케줄러 (Scheduler) ]
                            │
                            ▼
     ┌─────── [ PCB (Process Control Block) ] ───────┐
     │                                              │
 [ 준비 큐 (Ready Queue) ]               [ 대기 큐 (Wait Queue) ]
     │                                              │
     └─── (디스패치: Dispatch) ──► [ CPU 코어 ] ────┘ (I/O 요청: Blocked)
```

선의 의미: OS 스케줄러가 Ready Queue의 PCB를 선택하여 CPU에 디스패치하고, I/O 발생 시 Wait Queue로 전이시키는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 프로세스 제어 블록(PCB) | PID, 프로세스 상태(Ready/Running/Blocked), 레지스터 상태, 메모리 매핑 정보 저장 |
| 준비 큐(Ready Queue) | 스케줄링 정책(우선순위, FIFO 등)에 따라 CPU 할당을 대기 중인 PCB 연결 리스트 관리 |
| OS 스케줄러 | Ready Queue에서 실행 대상 프로세스를 선택하고 CPU 제어권을 이양(Dispatch) |
| CPU 코어 | 스케줄러가 할당한 프로세스의 기계어 명령어를 인출(Fetch) 및 실행(Execute) |
| 대기 큐(Wait Queue) | I/O 요청 완료 또는 시그널 대기 중인 프로세스 PCB를 디바이스별로 격리 관리 |

#### 한줄 요약

- **PCB 상태 저장소·Ready/Wait 큐 이원화·OS 스케줄러 디스패치 및 이벤트 인터럽트 복귀** ## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Dispatch(디스패치)**: 준비 큐의 최우선 프로세스를 선택하여 CPU 제어권을 부여하고 실행 상태로 전환하는 과정.
- **Preemption(선점)**: 타임 퀀텀 만료 또는 고우선순위 프로세스 등장 시 현재 실행 중인 프로세스의 CPU를 강제 회수하는 동작.

</details>

```text
[ 프로세스 5단계 상태 전이(State Transition) 시퀀스 ]
 [ 프로세스 생성 (fork/exec) : New ]
                 │
                 ▼ (Admitted)
         [ 준비 상태 (Ready) ] ◄─────────────────┐
                 │                               │
                 │ 1. 디스패치 (Dispatch)        │ 2. 선점 (Timeout / Preempt)
                 ▼                               │
         [ 실행 상태 (Running) ] ────────────────┘
           │          │
           │          └── 3. I/O 또는 이벤트 대기 ──► [ 대기 상태 (Blocked) ]
           │                                                │
           │                               4. I/O 완료 통지 │ (Wakeup)
           │                                                └──► [ 준비 상태 (Ready) ]
           │
           └── 5. 실행 종료 (exit) ──► [ 종료 상태 (Terminated) ]
```

**동작 원리** 1. **디스패치(Dispatch)**: 스케줄러가 준비 큐에서 최우선 순위 프로세스를 선택하여 CPU를 할당하고 실행 상태로 전이
2. **타이머 선점(Preempt)**: 할당된 타임 슬라이스(Time Quantum)가 만료되면 인터럽트를 통해 프로세스를 준비 상태로 강제 복귀
3. **I/O 대기(Blocked)**: 실행 중 디스크 읽기나 네트워크 소켓 수신 요청 시 CPU를 반납하고 대기 큐로 전이
4. **이벤트 완료(Wakeup)**: 하드웨어 I/O 완료 인터럽트 수신 시 대기 상태의 프로세스를 깨워 준비 큐로 재진입
5. **프로세스 종료(Exit)**: `exit()` 시스템 콜을 통해 할당된 메모리 및 파일 자원을 반납하고 종료 상태로 전환

#### 한줄 요약

- **생성(New) $\to$ 준비(Ready) $\to$ 디스패치 후 실행(Running) $\to$ 선점/I/O 대기(Blocked) $\to$ 완료 후 종료(Terminated)** ## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Orphan Process(고아 프로세스)**: 부모 프로세스가 먼저 종료되어 부모를 잃었으나, `init`(PID 1) 또는 `systemd` 프로세스에 입양되어 정상 종료 및 자원 정리가 보장되는 프로세스.

</details>

| 구분 | 준비 상태 (Ready State) | 실행 상태 (Running State) | 대기 상태 (Blocked State) |
|:---|:---|:---|:---|
| CPU 점유 여부 | 미점유 (스케줄러 디스패치 대기) | **점유 중** (명령어 파이프라인 실행) | 미점유 (이벤트 발생 시까지 CPU 실행 불가) |
| 상주 큐 위치 | **준비 큐 (Ready Queue)** | CPU 코어 레지스터 | **대기 큐 (Device/Wait Queue)** |
| 다음 전이 상태 | **실행 (Running)** (디스패치 시) | **준비** (선점 시) / **대기** (I/O 요청 시) | **준비 (Ready)** (I/O 완료 인터럽트 수신 시) |

#### 한줄 요약

- 준비 상태는 디스패치를 대기하고, 실행 상태는 연산을 수행하며, 대기 상태는 I/O 완료 후 준비 상태로 복귀

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **waitpid()**: 특정 자식 프로세스의 종료 상태를 감시하고 자원을 회수하여 좀비 프로세스를 방지하는 POSIX 시스템 콜.
- **ulimit(User Limit)**: 단일 사용자 또는 프로세스 그룹이 생성할 수 있는 최대 프로세스 수(`max user processes`)를 제한하는 커널 설정.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 부모 프로세스의 자식 종료 상태 미회수로 인한 **좀비 프로세스 누적 및 PID 고갈** | `SIGCHLD` 시그널 핸들러 등록 및 **`waitpid(..., WNOHANG)` 비동기 회수** 적용 | 불필요한 PCB 엔트리 즉시 정리 및 PID 자원 고갈 방지 |
| 외부 네트워크/스토리지 응답 지연으로 인한 **프로세스 대기 상태(Blocked) 무한 교착** | 소켓 및 디스크 I/O 요청 시 **Non-blocking I/O 및 Timeout** 정책 강제 | 무한 블로킹 차단 및 스레드/프로세스 자원 반환 보장 |
| 프로세스 무한 포크(Fork Bomb) 공격으로 인한 **시스템 자원 고갈 및 패닉** | `/etc/security/limits.conf` 내 **`nproc` 제한(ulimit)** 설정 | 프로세스 폭증 차단 및 OS 전체 가용성 확보 |

#### 한줄 요약

- **SIGCHLD 기반 waitpid() 비동기 회수·I/O Timeout 정책·ulimit(nproc) 생성 한도 통제** ## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Process Lifecycle Management**: 프로세스 생성, 우선순위 조율, 비정상 대기 감시, 좀비 회수까지 전 과정을 안정적으로 제어하는 운영체제 관리 체계.

</details>

- 클라우드 및 컨테이너 런타임 환경에서 **안정적인 생명주기 관리(`init` 시스템 PID 1 reaping, 타임아웃, cgroups 프로세스 한도 통제)** 필수 적용

#### 한줄 요약

- **5단계 상태 전이 통제와 좀비 프로세스 방지** 활용 통한 운영체제 자원 관리 안정성 확보
