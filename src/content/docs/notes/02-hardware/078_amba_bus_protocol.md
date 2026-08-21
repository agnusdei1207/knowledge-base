---
sidebar:
  order: 78
  label: "078. AMBA 버스 프로토콜"
  badge:
    text: "미출 · 50%"
    variant: note
title: "AMBA 버스 프로토콜 (AMBA Bus Protocol)"
date: "2026-08-17T09:25:00+09:00"
tags:
  - "notes-hardware"
weight: 78
extra:
  question_no: "078"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "SoC 온칩 버스 계층 비교"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **AMBA(Advanced Microcontroller Bus Architecture)**: Arm 사에서 제정한 SoC(System on Chip) 내부 IP 블록 간 고성능 연결 및 데이터 교환을 위한 개방형 표준 온칩 버스 규격.
- **SoC(System on Chip)**: CPU, GPU, NPU, 메모리 컨트롤러 및 주변장치를 단일 실리콘 칩 다이에 통합한 시스템 반도체.
- **Transaction(트랜잭션)**: 마스터와 슬레이브 간에 주소 전송, 데이터 읽기/쓰기, 응답 확인까지 완료되는 일련의 원자적 버스 동작.

</details>

- 정의/개념: Arm 아키텍처 기반 SoC(System-on-Chip) 내부에서 고성능 프로세서, 메모리 컨트롤러 및 저속 주변장치 IP 블록 간의 효율적인 연결과 고속 데이터 전송을 위해 규정된 온칩(On-Chip) 버스 통신 표준 프로토콜 계층 체계
- 배경/필요성: 단일 실리콘 다이에 수십~수백 개의 이종 IP 통합 시 인터페이스 호환성 확보 및 트랜잭션 처리량 극대화 필요

#### 한줄 요약

- Arm SoC 내부의 고속 연산 IP부터 저속 주변장치까지 **계층별 최적화된 온칩 버스 표준 규격(AXI, AHB, APB)** ## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **AXI(Advanced eXtensible Interface)**: 읽기/쓰기 주소 및 데이터 등 5개의 독립 채널을 통해 비순차(Out-of-Order) 버스트 전송을 지원하는 고성능 버스.
- **AHB(Advanced High-Performance Bus)**: 주소와 데이터 단계를 파이프라인화하여 고속 클록에서 단일 클록 에지 전송을 제공하는 시스템 버스.
- **APB(Advanced Peripheral Bus)**: 단순한 2단계 핸드셰이크를 사용하여 제어 레지스터 및 저속 주변장치를 연결하는 초저전력 버스.
- **Outstanding Transaction**: 이전 트랜잭션의 완료 응답을 기다리지 않고 연속해서 다수의 읽기/쓰기 요청을 발행하는 기법.

</details>

- 5개의 독립적인 단방향 채널(AR, R, AW, W, B)을 통해 양방향 동시 전송 및 **미완료 트랜잭션(Outstanding) 지원 (AXI)**
- 파이프라인 주소/데이터 전송 및 단일 공유 버스 기반의 **고효율 시스템 인터커넥트 (AHB)**
- 복잡한 제어 로직을 배제하고 무대기(No-Wait) 2단계 신호로 저전력을 달성하는 **주변장치 전용 인터페이스 (APB)** #### 한줄 요약

- **5개 독립 채널 및 Out-of-Order 지원(AXI)·파이프라인 주소/데이터(AHB)·2단계 무대기 단순 제어(APB)** ## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Master(Manager)**: 트랜잭션(읽기/쓰기 요청)을 주도적으로 생성하여 버스에 전달하는 IP(CPU, GPU, DMA).
- **Slave(Subordinate)**: 마스터의 요청 주소를 디코딩하여 데이터를 공급하거나 레지스터를 갱신하는 수동적 IP(메모리, 타이머).
- **Protocol Bridge**: AXI/AHB 고속 프로토콜 신호를 APB 저속 신호 타이밍으로 변환하고 속도를 완충하는 인터페이스 변환기.

</details>

```text
[ AMBA 온칩 버스 계층 구조 및 브리지 아키텍처 ]
┌──────────────────────────────┐        ┌──────────────────────────────┐
│ AXI 마스터 (CPU / GPU / DMA) │        │ AXI 슬레이브 (DDR 컨트롤러)  │
└──────────────┬───────────────┘        └──────────────┬───────────────┘
               │                                       │
┌──────────────┴───────────────────────────────────────┴──────────────┐
│ AXI Crossbar Interconnect (5개 독립 채널 중재 및 라우팅)            │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ [ AXI-to-APB Bridge (속도/프로토콜 변환) ]
┌──────────────────────────────┴──────────────────────────────────────┐
│ APB 버스 (저속/저전력 주변장치 제어 버스)                            │
│  ├─ UART 컨트롤러             ├─ I2C / SPI 마스터                    │
│  ├─ 하드웨어 타이머 (Timer)   └─ GPIO 레지스터                       │
└─────────────────────────────────────────────────────────────────────┘
```

선의 의미: AXI 마스터 블록, AXI 크로스바 상호연결망, AXI-APB 브리지 및 슬레이브/주변장치 간의 AMBA 온칩 버스 계층 구조도.

| 구성요소 | 책임 |
|:---|:---|
| 마스터(Manager) | 주소 및 제어 신호 트랜잭션을 능동적으로 생성하여 버스에 전달(CPU, GPU, DMA) |
| 고속 상호 연결망(Crossbar) | 5개 독립 채널 신호를 디코딩하여 라우팅 및 다중 마스터 요청 중재 수행 |
| 프로토콜 브리지(Bridge) | 고속 AXI/AHB 신호를 저속 APB 버스 타이밍으로 변환하고 속도 차 완충 |
| 슬레이브(Subordinate) | 브리지 또는 크로스바의 지시를 받아 레지스터 읽기/쓰기 및 제어 동작 수행 |

#### 한줄 요약

- **마스터 블록(Manager)·AXI Crossbar Interconnect·프로토콜 브리지(Bridge)·슬레이브 블록(Subordinate)** ## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **VALID/READY Handshake**: 송신자가 데이터 유효(VALID=1)를 알리고 수신자가 수신 준비(READY=1)를 완료하여 동일 클록 에지에서 둘 다 1일 때 전송이 성립되는 AXI 표준 동기화 기법.
- **PSEL / PENABLE**: APB 프로토콜에서 대상 슬레이브 선택(Setup Phase: PSEL=1) 후 다음 사이클에서 데이터 전송을 활성화(Access Phase: PENABLE=1)하는 2단계 신호.

</details>

```text
[ AMBA 버스 트랜잭션 전송 및 브리지 변환 시퀀스 ]
                         │
                         ▼
   [ 1. AXI 마스터가 읽기/쓰기 주소 채널(AR/AW)에 VALID 신호 송출 ]
                         │
        +────────────────┴────────────────────────+
        │             [ 목적지 주소 영역 판정 ]   │
        │             /                         \ │
        │     [ 고속 AXI 슬레이브 ]           [ 저속 APB 주변장치 ]
        │            │                            │
        │ 2. VALID/READY 핸드셰이크     3. AXI-APB 브리지가 수신 후
        │    동시 1 클록 에지에서          Setup(PSEL) ──> Access(PENABLE)
        │    고속 데이터 전송 완료         2사이클 저속 트랜잭션 구동
        +────────────────┬────────────────────────+
                         │
                         ▼
   [ 4. 슬레이브 응답 채널(B/R)을 통해 마스터로 전송 완료(OKAY/SLVERR) 반환 ]
```

**동작 원리** 1. **트랜잭션 요청**: AXI 마스터가 주소와 버스트 길이를 싣고 AWVALID/ARVALID=1 인가
2. **AXI 고속 전송**: 크로스바가 주소를 디코딩하여 타깃 슬레이브와 VALID/READY 일치 사이클에 버스트 데이터 전송
3. **APB 브리지 변환**: 타깃이 저속 IP일 경우 브리지가 AXI 요청을 받아 PSEL=1(Setup) $\to$ PENABLE=1(Access) 2단계로 변환
4. **응답 수신**: 전송 완료 후 슬레이브가 BRESP/RRESP(OKAY, EXOKAY, SLVERR, DECERR) 신호를 반환하여 트랜잭션 종결

#### 한줄 요약

- 마스터 트랜잭션 요청 $\to$ **AXI VALID/READY 양방향 핸드셰이크 $\to$ 브리지 경유 시 PSEL/PENABLE 2단계 절체 $\to$ 데이터 전송 $\to$ BRESP/RRESP 응답 완료** ## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **AXI vs AHB vs APB 비교**:
  - AXI: 5개 독립 채널, 비순차 전송, 최고 대역폭 (CPU/GPU/DRAM)
  - AHB: 단일 파이프라인 버스, 중간 대역폭 (온칩 SRAM/DMA)
  - APB: 2단계 단순 제어, 초저전력/저속 (UART/Timer/GPIO)

</details>

| 구분 | AXI (Advanced eXtensible Interface) | AHB (Advanced High-performance Bus) | APB (Advanced Peripheral Bus) |
|:---|:---|:---|:---|
| 채널 구조 및 전송 모드 | 5개 독립 채널 (AR, R, AW, W, B), 비순차(OoO) 버스트 | 단일 공유 버스, 파이프라인 주소/데이터 버스트 | 2단계 비파이프라인 제어 (Setup, Access) |
| 주 용도 및 대역폭 | CPU, GPU, NPU, DDR 메모리 컨트롤러 (최고 성능) | 온칩 온보드 SRAM, DMA 제어기 (중간 성능) | UART, 타이머, I2C, GPIO 레지스터 (저속/초저전력) |
| 한계 및 하드웨어 복잡도 | 배선 및 로직 면적 오버헤드 급증 | 다중 마스터 경합 시 중재 병목 발생 | 대용량 고속 버스트 전송 불가 |

#### 한줄 요약

- 최고성능 고대역폭은 **AXI**, 온칩 시스템 백본은 **AHB**, 저전력 주변장치 제어는 **APB** ## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **CDC(Clock Domain Crossing)**: 1GHz 고속 AXI 도메인과 50MHz 저속 APB 도메인 간 신호 전달 시 발생하는 메타스테이빌리티(Metastability)를 방지하기 위한 비동기 FIFO 구조.
- **Protocol Checker**: RTL 시뮬레이션 단계에서 VALID가 올라간 후 READY 전에 데이터가 변경되는 등 AMBA 프로토콜 위반을 실시간 감지하는 검증 IP.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 비순차(Out-of-Order) 전송 시 AXI 트랜잭션 ID 순서 꼬임으로 인한 데드락 발생 | 시뮬레이션 단계에서 **Assertion 기반 Protocol Checker** 전수 배치 | 트랜잭션 프로토콜 위반 실시간 감지 및 시스템 락 방지 |
| 고속 AXI 도메인과 저속 APB 도메인 간 클록 불일치로 인한 메타스테이빌리티(Metastability) 발생 | 클록 도메인 교차 지점에 **CDC(Clock Domain Crossing) Async FIFO** 구축 | 비동기 클록 신호 동기화 및 데이터 정합성 보장 |
| 저속 APB 슬레이브의 응답 지연으로 인한 브리지 버퍼 오버플로우 및 AXI 버스 연쇄 블로킹 | 브리지 버퍼 용량 최적화 및 **하드웨어 타임아웃/슬레이브 에러(SLVERR)** 강제 반환 | 지연된 트랜잭션 조기 격리 및 메인 시스템 버스 가용성 유지 |

#### 한줄 요약

- **Assertion 기반 Protocol Checker 검증·CDC Async FIFO 비동기 클록 도메인 격리·브리지 타임아웃/슬레이브 에러(SLVERR) 격리** ## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **AMBA CHI (Coherent Hub Interface)**: 대규모 멀티코어 SoC 및 칩렛 환경에서 캐시 일관성(Cache Coherency)과 패킷 기반 NoC 통신을 지원하는 최상위 AMBA 프로토콜.

</details>

- 차세대 복합 SoC 및 칩렛(Chiplet) 설계에서 **코어 백본은 AXI5/CHI 표준 채택 및 말단 제어부에 AXI-APB 계층화 브리지 표준 적용** #### 한줄 요약

- **대역폭 요구량과 전력/면적 예산(PPA)** 에 맞춘 AXI/AHB/APB 계층 버스 토폴로지 최적화
