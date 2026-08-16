---
sidebar:
  order: 34
  label: "034. 인터럽트 처리 방식: 벡터•데이지체인 (Interrupt Handling)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "인터럽트 처리 방식: 벡터•데이지체인 (Interrupt Handling)"
date: "2026-08-13T11:53:34+09:00"
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

<details><summary>용어 설명</summary>

- **인터럽트 처리 (Interrupt Handling)**: CPU가 명령어를 구동하는 도중 외부 입출력 장치나 내부 트랩 예외 신호(IRQ)가 수신되면, 현재 구동 중인 문맥을 스택에 백업하고 전용 처리 루틴(ISR)으로 제어를 전환하여 수습한 후 복귀하는 시퀀스.
- **인터럽트 요청 신호 (Interrupt Request, IRQ)**: 타이머, NIC, 디스크 제어기 등이 CPU 핀이나 메세지 버스를 통해 즉시 처리를 필요로 함을 전달하는 하드웨어 신호.
- **인터럽트 서비스 루틴 (Interrupt Service Routine, ISR)**: 특정 IRQ 번호에 1:1 결합되어 실제 장치의 입출력 데이터를 인출하거나 상태를 Clear 해주는 커널 내 함수.

</details>

- 정의/개념: 비동기적 하드웨어/소프트웨어 요청(IRQ)을 수신하여 하드웨어 제어기가 우선순위를 중재하고, CPU가 문맥 저장(Context Save) 후 해당 **인터럽트 서비스 루틴**을 실행하여 원래 기계어 상태로 복귀시키는 **인터럽트 처리** 아키텍처.
- 배경/필요성: CPU가 주기적으로 주변장치의 상태 레지스터를 조회하는 폴링(Polling) 방식의 막대한 CPU 자원 낭비를 소거하고, 입출력 완료 및 비상 에러 트랩에 즉각 반응하기 위해 도입.

#### 한줄 요약
- 하드웨어 IRQ 신호 수신 시 CPU 문맥 저장, 인터럽트 식별(벡터/데이지체인), ISR 실행 및 문맥 복원을 거치는 메커니즘.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **인터럽트 지연 (Interrupt Latency)**: 하드웨어 IRQ 신호가 발생한 순간부터 CPU가 문맥 저장을 마치고 actual ISR의 첫 번째 기계어 명령어를 실행하기 직전까지의 대기 시간.
- **중첩 인터럽트 (Nested Interrupt)**: 어떤 ISR이 구동 중일 때, 그보다 더 우선순위(Priority)가 높은 긴급 IRQ(예: 전원 트랩, NMI)가 들어오면 기존 ISR을 중단하고 우선 실행하는 구조.
- **문맥 저장/복원 (Context Save & Restore)**: CPU의 Program Counter(PC), Stack Pointer(SP), General Registers 및 Status Register 상태를 커널 스택에 푸시(Push) 및 팝(Pop)하는 작업.

</details>

- 허용된 경계에서 IRQ를 수락하고 우선순위•마스크 검사 후 **실행 흐름 전환** 발동.
- 하드웨어 인터럽트 제어기(APIC / NVIC)를 탑재하여 다중 IRQ 간의 **마스킹** 및 **우선순위 중재** 통제.
- 긴급도가 높은 IRQ 수용을 위해 **중첩 인터럽트**를 허용하되, 이로 인한 **인터럽트 지연** 및 스택 오버플로 위험 수반.

#### 한줄 요약
- APIC•NVIC 우선순위 중재와 문맥 저장•복원, 중첩 제어로 IRQ를 수습함.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

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

| 구성요소 | 책임 |
|:---|:---|
| 인터럽트 제어기 | **IRQ 마스크•우선순위•코어 라우팅** 제어 |
| 인터럽트 벡터 | 처리 원인의 **ISR 색인 번호** 제공 |
| IVT•IDT | 벡터별 **처리기 주소•권한 정보** 보관 |
| EOI 신호 | 제어기에 **처리 완료•다음 IRQ 허용** 통지 |

#### 한줄 요약
- Interrupt Controller(APIC/NVIC), Interrupt Vector, IVT/IDT 메모리 테이블 및 EOI 완료 통지 제어로 작동함.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **원인 해제 (Source Clear)**: ISR 함수 내부에서 입출력 장치 컨트롤러의 Status 레지스터 비트를 0으로 덮어써서 동일 IRQ가 재발동되는 것을 막는 행위.
- **지연 처리 (Deferred Processing / Bottom-Half, Top-Half)**: ISR(Top-Half)에서는 원인 해제 및 큐 등록만 1us 내로 하고, 시간이 걸리는 복잡한 처리는 SoftIRQ/Tasklet(Bottom-Half)으로 미루는 Linux 커널 기법.

</details>

```text
[ Hardware IRQ Signal Asserted by Device ]
                   │
                   ▼
  [ 1. 중재•식별 ]
                   │
                   ▼
  [ 2. 문맥 저장 ]
                   │
                   ▼
  [ 3. ISR 실행 ]
                   │
  [ Deferred Processing Exist? ]
        ├─ Yes ──> Queue to SoftIRQ / Tasklet (Bottom-Half)
        └─ No
                   │
                   ▼
  [ 4. 지연 처리•문맥 복원 ]
```

### 동작 원리

1. **중재•식별**: 마스크•우선순위 검사 후 벡터로 처리기를 선택함.
2. **문맥 저장**: PC•상태와 필요한 레지스터를 스택에 보존함.
3. **ISR 실행**: **Source Clear•EOI** 후 지연 작업을 큐에 등록함.
4. **지연 처리•문맥 복원**: Bottom-Half 실행을 예약하고 원래 흐름으로 복귀함.

#### 한줄 요약
- Priority Arbitration -> Context Save -> ISR Jump -> Source Clear & EOI -> Bottom-Half Offload -> Context Restore 순으로 수습됨.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **벡터 방식 (Vectored Interrupt)**: 장치가 자신의 고유 벡터 번호를 버스로 응답하여, CPU가 식별 지연 없이 IVT를 룩업해 1-Step 점프하는 현대적 하드웨어 방식.
- **데이지체인 방식 (Daisy Chain Interrupt)**: 여러 장치가 단일 IRQ 및 Interrupt Acknowledge(INTA) 신호선을 직렬(Daisy Chain) 핀으로 연결하여, 물리적 거리 우선순위에 따라 원인을 1:1 찾는 임베디드 방식.

</details>

| 비교 항목 | 벡터 방식 (Vectored Interrupt) | 데이지체인 방식 (Daisy Chain) |
|:---|:---|:---|
| **원인 식별 메커니즘**| 장치가 고유 **인터럽트 벡터 번호** 직접 송출 | INTA 승인 신호를 **직렬 체인 핀**으로 순차 패스 |
| **우선순위 결정** | **하드웨어 제어기** 프로그래밍 레지스터 | **물리적 연결 순서** (CPU에 가까운 장치 선점) |
| **식별 지연시간** | **극도로 짧음** (IVT 직접 룩업 Jump) | 긴 편임 (체인을 따라 신호 전파 지연 발생) |
| **하드웨어 복잡도**| 비쌈 (APIC 제어기 및 8-bit 데이터 버스 필요) | 매우 단순함 (단 1개의 IRQ/INTA 핀 라인으로 가능) |
| **장치 기아 현상** | 고정 우선순위 설정이면 발생 가능 | 상위 연결 장치 독점 시 발생 가능 |
| **주요 적용 시스템**| PC, 서버, x86, ARM Cortex-A/R (APIC/GIC) | 소형 임베디드, MCU, 8-bit/16-bit 컨트롤러 |

#### 한줄 요약
- 벡터 방식은 Vector 번호 기반의 저지연 direct IVT 룩업에 우수하고, 데이지체인 방식은 핀 하나로 여러 장치를 묶는 저비용 직렬 연결에 우수함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **지연 처리 (Top-Half / Bottom-Half)**: ISR(Top-Half)에서는 하드웨어 Lock을 해제하고 IRQ Clear만 가볍게(1us) 처리하고, 패킷 조립 및 Disk I/O 등 중대형 작업은 Workqueue/SoftIRQ(Bottom-Half)로 미루어 인터럽트 지연을 감축하는 기술.
- **우선순위 노화 (Priority Aging)**: APIC 스케줄링 시 저우선순위 장치가 고우선 장치에 밀려 영구 지연(Starvation)되는 것을 막고자 대기 시간에 비례해 IRQ 우선순위를 높여주는 기법.
- **MSI-X 벡터 친화도 (MSI-X Vector Affinity)**: NVMe/NIC의 멀티 큐 MSI-X 벡터를 특정 CPU 코어에 1:1 강제 결합(Binding)하여 멀티코어 간 인터럽트 캐시 미스를 차단하는 기법.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| ISR(Top-Half) 코드가 길어져 하위 인터럽트 무한 지연 발생 | **Top-Half / Bottom-Half(SoftIRQ, Workqueue)** 지연 처리 분리 | ISR 실행 시간 1us 이하로 단축 및 시스템 반응성 확보 |
| 하드웨어 디바이스 고장으로 끊임없이 IRQ가 터지는 **인터럽트 폭주** | 커널 차원의 **Interrupt Coalescing** 및 장애 장치 **Disable** | CPU Core 마비 현상 방지 및 안정성 보장 |
| 멀티코어 환경에서 IRQ가 0번 코어로만 쏠리는 부하 불균형 | **MSI-X Vector Affinity** 바인딩 및 irqbalance 데몬 구동 | 코어 간 I/O 인터럽트 부하 균등 분산 |
| 중첩 인터럽트 깊이가 깊어져 발생되는 Kernel Stack Overflow | **중첩 깊이 제한** 및 전용 IRQ 스택(Istack) 분리| 커널 스택 파손 및 Crash 예방 |

#### 한줄 요약
- Top-Half/Bottom-Half 분리, MSI-X Vector Affinity 바인딩, Dedicated IRQ Stack 사용 및 Interrupt Coalescing을 가동함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **인터럽트 설계 판단 기준 (Interrupt Architecture Decision Criteria)**: 대상 시스템의 인터럽트 발생 빈도, 허용 지연시간(Latency), CPU 코어 수 및 하드웨어 핀 제약을 평가하여 벡터/데이지체인 및 Top/Bottom Half 구조를 확정하는 결정 프레임워크.

</details>

- 다중 장치•코어는 **Vectored•MSI-X**, 단순 핀 제약은 **Daisy Chain** 선택.

#### 한줄 요약
- 빈도•지연•핀•코어 수로 식별 방식과 지연 처리 구조를 결정함.
