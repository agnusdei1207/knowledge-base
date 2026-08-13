---
sidebar:
  order: 2
  label: "002. CPU 구성: ALU•CU•레지스터•버스 (CPU Components)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "CPU 구성: ALU•CU•레지스터•버스 (CPU Components)"
date: "2026-08-13T11:58:00+09:00"
tags:
  - "notes-hardware"
weight: 2
extra:
  question_no: "002"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "CPU 구성과 명령어 주기의 핵심 기초"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **중앙 처리 장치(Central Processing Unit, CPU)**: 기억장치로부터 기계어 명령어를 인출(Fetch), 해독(Decode), 실행(Execute), 저장(Write-back)하여 연산과 하드웨어를 총괄 제어하는 핵심 프로세서.
- **제어장치(Control Unit, CU)**: 명령어 레지스터의 오퍼코드를 해독하여 내부 데이터 경로 및 외부 버스의 제어 신호(Control Signal)를 타이밍에 맞게 생성하는 장치.
- **산술논리장치(Arithmetic Logic Unit, ALU)**: 제어 신호에 따라 피연산자에 대한 2진 덧셈, 뺄셈 등 산술 연산과 AND, OR, XOR 등 논리 연산 및 시프트 연산을 수행하는 콤비네이션 논리 회로.
- **내부 버스(Internal Processor Bus)**: CPU 코어 내부에서 ALU, 레지스터 파일, CU 간에 데이터, 주소, 제어 신호를 고속으로 전송하는 칩 내부 통신 선로.

</details>

- 정의/개념: 연산(ALU), 제어(CU), 저장(Register File), 전송(Internal Bus) 장치가 유기적으로 결합하여 명령어 인출·해독·실행·기록 주기를 분담 수행하는 컴퓨터의 핵심 처리 모듈.
- 배경/필요성: 단순 연산 조합회로만으로는 프로그램 실행 제어 흐름 관리, 중간 연산 결과 보관, 동기화 클록 기반 데이터 이동을 달성할 수 없으므로, 제어 경로와 데이터 경로를 체계적으로 분리하여 연산 처리율을 극대화할 필요성 증대.

#### 한줄 요약
- 제어 경로(CU)의 명령어 인출·해독 기능과 데이터 경로(ALU, 레지스터, 버스)의 실행·기록 기능을 통합하여 CPU 명령어 주기를 완결함.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **제어 경로(Control Path)**: 명령어 해독 결과와 시스템 상태를 바탕으로 데이터 경로의 MUX, ALU, 레지스터 쓰기 활성화 신호를 제어하는 로직 회로.
- **데이터 경로(Data Path)**: 피연산자가 저장된 레지스터, 연산을 담당하는 ALU, 결과 전달 버스로 구성되어 실제 데이터 연산과 이동을 담당하는 하드웨어 라인.
- **레지스터(Register)**: 플립플롭(Flip-Flop) 및 래치(Latch) 회로로 구성되어 CPU 연산 주기 내에서 피연산자, 메모리 주소, 시스템 상태를 초고속 보관하는 저장 소자.
- **클록 엣지(Clock Edge)**: 동기식 디지털 회로에서 신호 상태를 레지스터에 저장하거나 상태를 전환하는 클록 파형의 상승(Rising) 또는 하강(Falling) 시점.

</details>

- **제어 경로(Control Path)**의 해독 신호(Control Output Signal)를 통해 **데이터 경로(Data Path)** 상의 멀티플렉서(MUX) 선택 및 ALU 연산 모드를 실시간 결정.
- 레지스터 파일 중심의 피연산자 공급 체계를 구축하여 연산 수행 시 메인 메모리 접근 빈도를 줄이고 접근 지연 시간 극소화.
- 기준 **클록 엣지(Clock Edge)**에 맞춰 연산 결과와 상태 플래그를 정밀하게 동기화 갱신하여 인스트럭션 실행 안정성 보장.

#### 한줄 요약
- 제어장치의 신호 생성을 바탕으로 데이터 경로 연산을 제어하며 클록 엣지 타이밍 동기화를 통해 레지스터 상태 갱신을 수행함.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **산술논리장치(Arithmetic Logic Unit, ALU)**: 범용 레지스터가 제공한 피연산자를 입력받아 제어 신호에 따른 정수/논리 연산을 실행하고 상태 플래그를 출력하는 연산 장치.
- **제어장치(Control Unit, CU)**: IR에 적재된 명령어 오퍼코드(Op-code)를 마이크로 명령 또는 경선제어(Hardwired) 방식으로 해독하는 장치.
- **레지스터 파일(Register File)**: 복수의 범용 레지스터(GPR)를 배열 형태로 묶어 동시 읽기/쓰기 접근 포트를 제공하는 고속 데이터 배열.
- **특수 목적 레지스터(Special-Purpose Register, SPR)**: PC, IR, SP, PSR 등 프로세서의 명령 실행 위치 및 제어 상태 유지를 위해 배정된 전용 레지스터.
- **내부 버스(Internal Bus)**: 레지스터 포트와 ALU 입력/출력 핀 간 데이터 전송 대역폭을 보장하는 프로세서 내부 버스.
- **제어 신호(Control Signal)**: 레지스터 래칭, ALU 연산자 선택, 버스 트라이스테이트 버퍼 활성화를 통제하는 1비트/다비트 제어선.

</details>

```text
+-------------------------------------------------------------------+
|                        CPU Core Architecture                      |
|                                                                   |
|   [ Control Path ]                     [ Data Path ]              |
|   +-------------------+                +----------------------+   |
|   | Control Unit (CU) |==Control Lines==> Register File(GPR) |   |
|   +-------------------+                +----------------------+   |
|     | Instruction Deco.                  | Operand 1 & 2          |
|     v                                    v                        |
|   +-------------------+                +----------------------+   |
|   | SPR (PC, IR, PSR) |                |   ALU (Arithmetic)   |   |
|   +-------------------+                +----------------------+   |
|                                                  | Result         |
|                                                  v                |
|   <=============== Internal Processor Bus ===================>   |
+-------------------------------------------------------------------+
```

| 구성요소 | 책임 |
|:---|:---|
| 제어장치 | 오퍼코드 해독•타이밍별 **제어 신호** 생성 |
| 레지스터 파일 | **피연산자•연산 결과** 고속 보관 |
| 특수 목적 레지스터 | **PC•IR•PSR**로 실행 위치•상태 관리 |
| 산술논리장치 | 제어 신호에 따른 **산술•논리 연산** 수행 |
| 내부 버스 | 블록 간 **피연산자•결과** 전송 |

#### 한줄 요약
- Control Path(CU, PC, IR)가 전체 타이밍을 통제하고 Data Path(GPR, ALU, Internal Bus)가 피연산자 연산 및 결과 저장 라운드트립을 수행함.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **프로그램 카운터(Program Counter, PC)**: 다음 순서에 인출할 메모리 내 기계어 명령어의 주소값을 보유하는 특수 레지스터.
- **명령어 레지스터(Instruction Register, IR)**: 메모리에서 인출한 명령어를 CU가 해독하기 직전까지 격리 보관하는 레지스터.
- **상태 비트(Status Bit / Flag)**: ALU 연산 결과 발생 여부(Zero, Carry, Overflow, Sign 등)를 기록하는 조건 플래그 비트.
- **명령어 인출(Instruction Fetch, IF)**: PC가 나타내는 메인 메모리/캐시 주소에서 기계어를 읽어 IR에 적재하는 단계.
- **명령어 해독(Instruction Decode, ID)**: CU가 IR의 명령어 필드를 분석하여 피연산자 주소와 ALU 작동 제어 신호를 생성하는 단계.
- **피연산자 읽기(Operand Fetch, OF)**: 명령어가 지정한 레지스터 번호나 메모리 주소에서 실제 데이터 피연산자를 읽어오는 단계.
- **연산 실행(Execute, EX)**: ALU가 제어 신호에 맞추어 피연산자에 대한 산술/논리 계산을 진행하는 단계.
- **결과 기록(Write-Back, WB)**: 연산 최종 결과값을 목표 범용 레지스터에 기록하고 ALU 상태 비트를 PSR에 저장하는 단계.

</details>

```text
[PC 주소 인출 요청] ──> 1. 명령어 인출 (Instruction Fetch)
                                │
                                ▼
                       2. 명령어 해독 (Instruction Decode)
                                │
                                ▼
                       3. 피연산자 읽기 (Operand Fetch)
                                │
                                ▼
                       4. 연산 실행 (Execute)
                                │
                                ▼
                       5. 결과 기록 (Write-Back) ──> [레지스터 & PSR 상태비트 갱신]
```

### 동작 원리

1. **명령어 인출(IF)**: **PC(Program Counter)**가 가리키는 메모리 주소의 명령어를 Fetch하여 **IR(Instruction Register)**에 저장하고 PC 주소값을 명령어 크기만큼 증가시킴.
2. **명령어 해독(ID)**: **CU(Control Unit)**가 IR의 Op-code를 해독하여 ALU 연산 종류와 Register File 읽기 선택 신호를 구동함.
3. **피연산자 읽기(OF)**: 명령어가 지시하는 레지스터 번호에 접근하여 **레지스터 파일(Register File)**에서 입력 데이터 2개를 읽어 ALU 입력 버스에 연결함.
4. **연산 실행(EX)**: **ALU**가 지정된 기능(ADD, SUB, AND 등)을 실행하고 결과를 출력 버스에 싣는 동시에 Zero/Overflow 등 **상태 비트(Status Bit)**를 생성함.
5. **결과 기록(WB)**: 연산 결과를 지정된 레지스터에 쓰기(Latching)하고 상태 비트를 PSR에 갱신하여 1개 기계어 실행 주기를 완료함.

#### 한줄 요약
- PC -> Memory Fetch -> IR -> CU Decode -> Register Read -> ALU Execute -> WB 순서로 5단계 인스트럭션 사이클이 연동됨.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **범용 레지스터(General-Purpose Register, GPR)**: 정수, 부동소수점, 메모리 포인터 등의 데이터 연산 피연산자 및 결과를 임시 저장하는 멀티플레이 레지스터.
- **스택 포인터(Stack Pointer, SP)**: 서브루틴 호출 및 파라미터 전달을 위한 메모리 스택의 최상단 주소를 추적하는 특수 레지스터.
- **상태 레지스터(Program Status Register, PSR)**: 프로세서 동작 모드(User/Privileged), 인터럽트 마스크, ALU 결과 플래그를 관리하는 제어 레지스터.
- **제어 레지스터(Control Register)**: 프로세서 동작 옵션, 메모리 가상화 보호 모드, MMU 활성 상태 등을 보관하는 제어 소자.
- **주소 레지스터(Address Register)**: 메모리 간 데이터 전송 시 참조 주소(MAR, SP 등)를 지정하기 위해 특화된 레지스터.

</details>

| 레지스터 유형 | 대표 레지스터 | 저장 데이터 | 처리 역할 및 실무 유용성 |
|:---|:---|:---|:---|
| **GPR (범용 레지스터)** | R0~R15, RAX~RDX | 연산 피연산자, 중간 계산 결과 | ALU 직접 연산 입력 공급 및 메모리 접근 횟수 최소화 |
| **제어 레지스터** | **PC** (Program Counter), **IR** | 다음 명령 주소, 현재 기계어 | 명령어 인출 및 해독 제어 흐름의 연쇄성 유지 |
| **주소 레지스터** | **SP** (Stack Pointer), **MAR** | 메모리 스택 Top 주소, RAM 주소 | 함수 호출 복귀 주소 관리 및 구조화된 메모리 추적 |
| **상태 레지스터** | **PSR** (Status Register), Flags | Carry, Zero, Overflow, Interrupt Mask | 조건 분기(Branch) 판단 기준 제공 및 예외 상태 제어 |

#### 한줄 요약
- GPR은 연산 데이터 피연산자를 임시 보관하고 Control/상태 레지스터(PC, IR, PSR, SP)는 프로세서 Executing Context 유지 및 제어 흐름을 관장함.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **다중 포트 레지스터 파일(Multi-Ported Register File)**: 단일 클록 주기에 여러 딜리버리 포트를 통해 복수의 Read/Write를 동시 수행할 수 있는 회로 구조.
- **데이터 해저드(Data Hazard)**: 이전 명령어의 결과 기록이 완료되지 않은 상태에서 다음 명령어 데이터가 접근을 시도하여 선후 의존성이 파괴되는 문제.
- **포워딩(Forwarding / Bypassing)**: ALU 연산 결과를 레지스터 파일에 기록하기 전에 다음 클록 연산의 입력으로 직접 바이패스시키는 기술.
- **파이프라인 인터록(Pipeline Interlock)**: 의존성 해저드가 해결될 때까지 파이프라인 제어 신호를 동결하여 파이프라인 정지(Stall)를 유발하는 감지 회로.
- **버스 경합(Bus Contention)**: 다수의 하드웨어 모듈이 단일 내부 버스 자원을 동시 사용하려 할 때 신호 충돌이 발생하는 현상.
- **버스 중재(Bus Arbitration)**: 버스 요청기들 간에 우선순위를 할당하여 버스 점유 권한을 제어하는 중재 메커니즘.
- **설정•유지 시간(Setup/Hold Time)**: 레지스터 플립플롭의 데이터 입력 시 클록 엣지 이전과 이후에 신호가 안정되게 유지되어야 하는 최소 정밀 시간.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 파이프라인 슈퍼스칼라 구조에서 동시 피연산자 접근 시 레지스터 병목 발생 | 2-Read / 1-Write 이상의 **다중 포트 레지스터 파일(Multi-Ported Register File)** 구축 | 동일 주기에 다수 피연산자 병렬 인출로 파이프라인 대기 대폭 절감 |
| 선행 명령어 연산 결과 비기록으로 인한 RAW(Read-After-Write) **데이터 해저드** | ALU 출력을 입력으로 즉각 회선 연결하는 **포워딩(Forwarding)** 및 **파이프라인 인터록** 구현 | 레지스터 쓰기 대기 시간을 우회하여 연속 명령어 연산 처리율 유지 |
| 다수 내부 소자의 동시에 의한 **버스 경합(Bus Contention)** 및 신호 왜곡 | 고정/순환 우선순위 방식의 **버스 중재(Bus Arbitration)** 논리 회로 내장 | 내부 데이터 이동 충돌 예방 및 확정적 데이터 전송 시간 확보 |
| 클록 고속화 시 데이터 경로 신호 지연으로 인한 **설정•유지 시간(Setup/Hold Time)** 위반 | Static Timing Analysis (STA) 기반 Critical Path 최적화 및 셋업 타임 마진 확보 | 메타스태빌리티(Metastability) 방지 및 프로세서 고속 동작 안정성 확보 |

#### 한줄 요약
- Multi-ported Register File, Forwarding Unit, Pipeline Hazard Interlock 및 Bus Arbitration 설계를 통해 CPU 내부 해저드와 버스 병목을 해소함.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **명령어 집합 아키텍처(Instruction Set Architecture, ISA)**: 하드웨어 설계자와 소프트웨어 개발자 사이의 약속으로, 명령어 형태, 레지스터 구조, 주소 지정 방식을 지정하는 인터페이스 사양.
- **CPU 구성 설계 기준(CPU Architecture Design Criteria)**: ISA의 타깃 목표(고성능 서버, 저전력 임베디드 등)에 따라 레지스터 폭, ALU 수, 제어 구조를 정형화하는 설계 지침.

</details>

- **ISA 비트 폭•발행 폭**에 맞춰 레지스터 포트와 **ALU 수**를 정하고 STA로 타이밍 검증

#### 한줄 요약
- ISA와 발행 폭에 맞춰 레지스터 포트•ALU 수를 정하고 데이터 경로 타이밍을 검증한다.
