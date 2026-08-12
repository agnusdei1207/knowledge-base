---
sidebar:
  order: 34
  label: "034. 인터럽트 처리 방식: 벡터•데이지체인 (Interrupt Handling)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "인터럽트 처리 방식: 벡터•데이지체인 (Interrupt Handling)"
date: "2026-08-08T17:12:00+09:00"
tags:
  - "notes-hardware"
weight: 34
extra:
  question_no: "034"
  source_status: "기출"
  source_history: "128회, 132회"
  priority: 70
  priority_note: "반복 기출, 우선순위•벡터 비교"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **인터럽트 처리 (Interrupt Handling)**: CPU가 명령어를 구동하는 도중 외부 입출력 장치나 내부 트랩 예외 신호(IRQ)가 수신되면, 현재 구동 중인 문맥을 스택에 백업하고 전용 처리 루틴(ISR)으로 제어를 전환하여 수습한 후 복귀하는 시퀀스.
- **인터럽트 요청 신호 (Interrupt Request, IRQ)**: 타이머, NIC, 디스크 제어기 등이 CPU 핀이나 메세지 버스를 통해 즉시 처리를 필요로 함을 전달하는 하드웨어 신호.
- **인터럽트 서비스 루틴 (Interrupt Service Routine, ISR)**: 특정 IRQ 번호에 1:1 결합되어 실제 장치의 입출력 데이터를 인출하거나 상태를 Clear 해주는 커널 내 함수.

</details>

- 정의/개념: 비동기적 하드웨어/소프트웨어 요청(IRQ)을 수신하여 하드웨어 제어기가 우선순위를 중재하고, CPU가 문맥 저장(Context Save) 후 해당 **인터럽트 서비스 루틴(ISR)**을 실행하여 원래 기계어 상태로 복귀시키는 **인터럽트 처리(Interrupt Handling)** 아키텍처.
- 배경/필요성: CPU가 주기적으로 주변장치의 상태 레지스터를 조회하는 폴링(Polling) 방식의 막대한 CPU 자원 낭비를 소거하고, 입출력 완료 및 비상 에러 트랩에 즉각 반응하기 위해 도입.

#### 한줄 요약
- 하드웨어 IRQ 신호 수신 시 CPU 문맥 저장, 인터럽트 식별(벡터/데이지체인), ISR 실행 및 문맥 복원을 거치는 메커니즘.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **인터럽트 지연 (Interrupt Latency)**: 하드웨어 IRQ 신호가 발생한 순간부터 CPU가 문맥 저장을 마치고 actual ISR의 첫 번째 기계어 명령어를 실행하기 직전까지의 대기 시간.
- **중첩 인터럽트 (Nested Interrupt)**: 어떤 ISR이 구동 중일 때, 그보다 더 우선순위(Priority)가 높은 긴급 IRQ(예: 전원 트랩, NMI)가 들어오면 기존 ISR을 중단하고 우선 실행하는 구조.
- **문맥 저장/복원 (Context Save & Restore)**: CPU의 Program Counter(PC), Stack Pointer(SP), General Registers 및 Status Register 상태를 커널 스택에 푸시(Push) 및 팝(Pop)하는 작업.

</details>

- CPU 명령어 실행 경계(Instruction Boundary) 완결 직후 IRQ 핀을 샘플링하여 1주기 이내로 **실행 흐름 전환(Execution Flow Transfer)** 발동.
- 하드웨어 인터럽트 제어기(APIC / NVIC)를 탑재하여 다중 IRQ 간의 **마스킹(Masking)** 및 **우선순위 중재(Arbitration)** 통제.
- 긴급도가 높은 IRQ 수용을 위해 **중첩 인터럽트(Nested Interrupt)**를 허용하되, 이로 인한 **인터럽트 지연(Interrupt Latency)** 및 스택 오버플로 위험 수반.

#### 한줄 요약
- APIC/NVIC 제어기를 통한 우선순위 중재, 1클록 내 문맥 저장/복원 및 중첩 인터럽트 제어를 통한 저지연 수습을 특성으로 가짐.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **인터럽트 제어기 (Interrupt Controller / APIC, NVIC)**: 각 장치의 IRQ 핀을 집적 받아 마스킹, 우선순위 판정 후 CPU Core로 대표 IRQ 신호를 보류 발송하는 전용 반도체.
- **인터럽트 벡터 테이블 (Interrupt Vector Table, IVT)**: 0번지 메모리 구역에 배치되어, 각 인터럽트 벡터 번호(0~255)마다 처리할 32/64-bit ISR 시작 메모리 주소를 매핑해둔 함수 포인터 배열.
- **인터럽트 벡터 (Interrupt Vector)**: 해당 IRQ 장치가 8-bit 데이터 버스로 CPU에 전송해 주는 고유 오프셋 번호.

</details>

```text
[ Hardware Interrupt Controller & IVT Architecture ]
┌───────────────────────────────────────────────────────────┐
│ Peripheral Devices (Timer, NVMe, NIC, Keyboard)           │
│  └─ Generate Hardware IRQ Lines (IRQ 0, IRQ 1 ... IRQ N)  │
├───────────────────────────────────────────────────────────┤
│ Interrupt Controller (APIC / NVIC)                        │
│  ├─ Priority Masking & Interrupt Arbitration Logic        │
│  └─ Output Vector Number (e.g., Vector 0x21) to CPU       │
├───────────────────────────────────────────────────────────┤
│ CPU Core ──> Read Vector 0x21 ──> Lookup IVT / IDT        │
│  ├─ Save Context (PC, Flags, GPRs to Kernel Stack)        │
│  └─ Jump to Target ISR Address (0xFFFFFFFF81001234)       │
└───────────────────────────────────────────────────────────┘
```

| 구성요소 | 역할 및 작동 원리 | 차별점 및 실무 유용성 |
|:---|:---|:---|
| **인터럽트 제어기 (APIC/NVIC)**| IRQ 신호 수신, 마스킹 비트 대조 및 우선순위 중재 | 멀티코어 환경에서 특정 CPU 코어로 인터럽트 분산 로드 밸런싱 |
| **인터럽트 벡터 (Vector)** | IRQ 장치가 CPU로 발송하는 1-Byte 식별 번호 | 소프트웨어가 빠르게 해당 장치의 원인을 식별하는 색인값 제공 |
| **인터럽트 벡터 테이블 (IVT/IDT)**| 메모리 상에 1:1 ISR 함수 시작 주소를 보관 | 1클록 테이블 룩업만으로 목표 ISR 주소로 직통 JUMP 수행 |
| **EOI (End of Interrupt)**| ISR 완결 시 CPU가 제어기로 발송하는 완료 신호 | 제어기 내 차단 중이던 동일/하위 우선순위 IRQ 락업 해제 |

#### 한줄 요약
- Interrupt Controller(APIC/NVIC), Interrupt Vector, IVT/IDT 메모리 테이블 및 EOI 완료 통지 제어로 작동함.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **원인 해제 (Source Clear)**: ISR 함수 내부에서 입출력 장치 컨트롤러의 Status 레지스터 비트를 0으로 덮어써서 동일 IRQ가 재발동되는 것을 막는 행위.
- **지연 처리 (Deferred Processing / Bottom-Half, Top-Half)**: ISR(Top-Half)에서는 원인 해제 및 큐 등록만 1us 내로 하고, 시간이 걸리는 복잡한 처리는 SoftIRQ/Tasklet(Bottom-Half)으로 미루는 Linux 커널 기법.

</details>

```text
[ Hardware IRQ Signal Asserted by Device ]
                   │
                   ▼
  [ 1. Interrupt Controller Priority Arbitration & Masking Check ]
                   │
                   ▼
  [ 2. CPU Finishes Current Instruction & Reads Interrupt Vector ]
                   │
                   ▼
  [ 3. Context Save : Push PC, Flags, GPRs to Kernel Stack ]
                   │
                   ▼
  [ 4. Jump to ISR (Top-Half) : Source Clear & EOI Signal Assert ]
                   │
  [ Deferred Processing Exist? ]
        ├─ Yes ──> Queue to SoftIRQ / Tasklet (Bottom-Half)
        └─ No
                   │
                   ▼
  [ 5. Context Restore : Pop Registers & Return to Original Program ]
```

### 동작 원리

1. **중재 및 식별**: 제어기가 마스킹 및 우선순위를 중재하고, CPU가 **인터럽트 벡터**를 수신하여 IVT 테이블을 룩업함.
2. **문맥 저장(Context Save)**: 현재 명령을 완료한 CPU가 PC, Flags, 레지스터 상태를 커널 스택에 **문맥 저장**함.
3. **ISR(Top-Half) 실행**: ISR로 점프하여 **원인 해제(Source Clear)**를 수행하고 제어기로 **EOI(End of Interrupt)**를 전달함.
4. **지연 처리 및 문맥 복원**: 시간 소요 작업은 **Bottom-Half(SoftIRQ)**로 오프로드하고, 스택에서 문맥을 복원하여 원래 프로그램을 재개함.

#### 한줄 요약
- Priority Arbitration -> Context Save -> ISR Jump -> Source Clear & EOI -> Bottom-Half Offload -> Context Restore 순으로 수습됨.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **벡터 방식 (Vectored Interrupt)**: 장치가 자신의 고유 벡터 번호를 버스로 응답하여, CPU가 식별 지연 없이 IVT를 룩업해 1-Step 점프하는 현대적 하드웨어 방식.
- **데이지체인 방식 (Daisy Chain Interrupt)**: 여러 장치가 단일 IRQ 및 Interrupt Acknowledge(INTA) 신호선을 직렬(Daisy Chain) 핀으로 연결하여, 물리적 거리 우선순위에 따라 원인을 1:1 찾는 임베디드 방식.

</details>

| 비교 항목 | 벡터 방식 (Vectored Interrupt) | 데이지체인 방식 (Daisy Chain) |
|:---|:---|:---|
| **원인 식별 메커니즘**| 장치가 고유 **인터럽트 벡터 번호** 직접 송출 | INTA 승인 신호를 **직렬 체인 핀**으로 순차 패스 |
| **우선순위 결정** | **하드웨어 제어기(APIC)** 프로그래밍 레지스터 | **물리적 연결 순서** (CPU에 가까운 장치 선점) |
| **식별 지연시간** | **극도로 짧음** (IVT 직접 룩업 Jump) | 긴 편임 (체인을 따라 신호 전파 지연 발생) |
| **하드웨어 복잡도**| 비쌈 (APIC 제어기 및 8-bit 데이터 버스 필요) | 매우 단순함 (단 1개의 IRQ/INTA 핀 라인으로 가능) |
| **장치 기아 현상** | **없음** (우선순위 노화/APIC 스케줄링 적용) | 발생 가능 (상위 장치가 신호를 독점 시 기아) |
| **주요 적용 시스템**| PC, 서버, x86, ARM Cortex-A/R (APIC/GIC) | 소형 임베디드, MCU, 8-bit/16-bit 컨트롤러 |

#### 한줄 요약
- 벡터 방식은 Vector 번호 기반의 저지연 direct IVT 룩업에 우수하고, 데이지체인 방식은 핀 하나로 여러 장치를 묶는 저비용 직렬 연결에 우수함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **지연 처리 (Top-Half / Bottom-Half)**: ISR(Top-Half)에서는 하드웨어 Lock을 해제하고 IRQ Clear만 가볍게(1us) 처리하고, 패킷 조립 및 Disk I/O 등 중대형 작업은 Workqueue/SoftIRQ(Bottom-Half)로 미루어 인터럽트 지연을 감축하는 기술.
- **우선순위 노화 (Priority Aging)**: APIC 스케줄링 시 저우선순위 장치가 고우선 장치에 밀려 영구 지연(Starvation)되는 것을 막고자 대기 시간에 비례해 IRQ 우선순위를 높여주는 기법.
- **MSI-X 벡터 친화도 (MSI-X Vector Affinity)**: NVMe/NIC의 멀티 큐 MSI-X 벡터를 특정 CPU 코어에 1:1 강제 결합(Binding)하여 멀티코어 간 인터럽트 캐시 미스를 차단하는 기법.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| ISR(Top-Half) 코드가 길어져 하위 인터럽트 무한 지연 발생 | **Top-Half / Bottom-Half(SoftIRQ, Workqueue)** 지연 처리 분리 | ISR 실행 시간 1us 이하로 단축 및 시스템 반응성 확보 |
| 하드웨어 디바이스 고장으로 끊임없이 IRQ가 터지는 **인터럽트 폭주** | 커널 차원의 **Interrupt Coalescing** 및 장애 장치 **Disable** | CPU Core 마비 현상 방지 및 안정성 보장 |
| 멀티코어 환경에서 IRQ가 0번 코어로만 쏠리는 부하 불균형 | **MSI-X Vector Affinity** 바인딩 및 irqbalance 데몬 구동 | 코어 간 I/O 인터럽트 부하 균등 분산 |
| 중첩 인터럽트 깊이가 깊어져 발생되는 Kernel Stack Overflow | **중첩 깊이 제한(Nesting Limit)** 및 전용 IRQ 스택(Istack) 분리| 커널 스택 파손 및 Crash 예방 |

#### 한줄 요약
- Top-Half/Bottom-Half 분리, MSI-X Vector Affinity 바인딩, Dedicated IRQ Stack 사용 및 Interrupt Coalescing을 가동함.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **인터럽트 설계 판단 기준 (Interrupt Architecture Decision Criteria)**: 대상 시스템의 인터럽트 발생 빈도, 허용 지연시간(Latency), CPU 코어 수 및 하드웨어 핀 제약을 평가하여 벡터/데이지체인 및 Top/Bottom Half 구조를 확정하는 결정 프레임워크.

</details>

- **인터럽트 설계 판단 기준 (Interrupt Architecture Decision Criteria)**에 의거하여 고성능 엔터프라이즈 및 멀티코어 시스템을 구축할 시, 하드웨어 레벨에서는 저지연 direct JUMP를 제공하는 **APIC/GIC 기반 벡터 방식(Vectored Interrupt)**과 **MSI-X**를 채택하고, OS 커널 레벨에서는 **Top-Half/Bottom-Half 지연 처리** 및 코어 Affinity 바인딩 체계 적용 필수.

#### 한줄 요약
- 초고속 비동기 수습을 위한 하드웨어 벡터 방식 인터럽트 채택 및 커널 Top-Half/Bottom-Half 지연 처리 결합 체계 적용.
