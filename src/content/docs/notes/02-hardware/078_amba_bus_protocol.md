---
sidebar:
  order: 78
  label: "078. AMBA 버스 프로토콜"
  badge:
    text: "미출 • 50%"
    variant: note
title: "AMBA 버스 프로토콜 (AMBA Bus Protocol)"
date: "2026-08-08T19:53:00+09:00"
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

<details><summary>핵심 용어</summary>

- **AMBA(Advanced Microcontroller Bus Architecture)**: Arm 사가 제정한 System-on-Chip(SoC) 내 CPU 코어, 메모리 컨트롤러, 온칩 주변장치 간의 표준 개방형 버스 규격.
- **SoC(System on Chip)**: CPU, GPU, NPU, 메모리 인터페이스, 입출력 레지스터가 단일 실리콘 다이에 통합된 시스템 칩.
- **거래(Transaction)**: 버스 상에서 주소(Address), 제어(Control), 데이터(Data) 패킷이 인가되어 처리 완결되는 단일 버스 동작 단위.

</details>

- 정의/개념: SoC 내부 서브시스템 기능 블록 간의 연동 신호 규격 및 **거래** 프로토콜을 계층별로 구율한 표준 규격인 **AMBA**
- 배경/필요성: IP(Intellectual Property) 부품 간 독자 인터페이스 사용 시 발생하는 재설계 오버헤드 해소 및 SoC 온칩 통합 효율성 극대화

#### 한줄 요약

- AMBA는 SoC 기능 블록 사이의 거래•응답 인터페이스를 역할과 대역폭에 맞게 표준화한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **AXI(Advanced eXtensible Interface)**: 읽기/쓰기 채널 분리, Out-of-Order 실행 및 5개 독립 채널을 지원하는 최고성능 AMBA 3/4/5 온칩 버스 규격.
- **AHB(Advanced High-Performance Bus)**: 주소와 데이터 단계를 겹쳐 파이프라이닝을 지원하는 버퍼링 시스템 버스 규격.
- **APB(Advanced Peripheral Bus)**: 단순한 2-Phase 핸드셰이크 구조를 지닌 저속/저전력 주변장치 제어용 버스 규격.
- **미완료 거래(Outstanding Transaction)**: 이전 요청에 대한 최종 응답(Response) 수신 전이라도 신규 요청을 연속 발행(Burst)하는 기법.

</details>

- 고성능 대용량 데이터 전송을 위한 **AXI**의 5개 독립 채널 및 **미완료 거래** 보장
- 파이프라인 버스트 전송을 보장하는 **AHB** 시스템 온칩 인터커넥트
- 저전력/저속 제어 레지스터 연결을 보장하는 **APB** 미들웨어 계층 구조

#### 한줄 요약

- 처리량과 거래 복잡도에 따라 AXI•AHB•APB를 계층화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Manager Block**: 읽기/쓰기 트랜잭션을 능동 발상(Master)시키는 CPU, DMA 등의 주 장치.
- **Subordinate/Target Block**: 주 장치 요청을 전달받아 메모리/레지스터 억세스를 수행(Slave)하는 종속 장치.
- **프로토콜 브리지(Protocol Bridge)**: AXI<->AHB, AHB<->APB 간 신호 패킷 변환 및 속도차 버퍼링을 담당하는 버스 브리지 칩셋.

</details>

```text
[관리자 기능 블록] ----- [고속 상호 연결망] ----- [메모리•가속기]
                                |
                        [프로토콜 브리지]
                                |
                        [저속 주변장치]
```

선의 의미: 주 관리자(Manager) 블록이 고속 상호 연결망(AXI)을 거쳐 메모리/가속기로 연동되고, 브리지를 거쳐 저속 APB 주변장치로 분기되는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 관리자(Manager/Master) | 주소, 제어 및 읽기/쓰기 **거래** 트랜잭션 능동 발행 |
| 고속 상호 연결망 | AXI 5-Channel(AR, R, AW, W, B) 라우팅, 중재 및 디코딩 |
| 프로토콜 브리지 | 고속 AXI/AHB 요청을 저속 **APB** 2-Phase 파이프라인으로 패킷 변환 |
| 저속 주변장치 | UART, Timer, GPIO 등 저속 제어 레지스터 **APB** 응답 처리 |

#### 한줄 요약

- 고속 상호 연결망과 프로토콜 브리지가 관리자 기능 블록·메모리·가속기·저속 주변장치를 계층형 SoC로 연결한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **VALID/READY 핸드셰이크**: AXI 5개 채널 상에서 송신측(VALID)과 수신측(READY) 신호가 모두 High(1)일 때 데이터 전송이 성립되는 메커니즘.
- **PSEL/PENABLE/PREADY**: APB 버스의 2-Phase(Setup Phase -> Enable Phase) 전송을 제어하는 고유 핸드셰이크 신호.

</details>

```text
[관리자 읽기•쓰기 요청]
           │
           ▼
1. 주소 디코딩•중재
           │
           ▼
2. 대상 프로토콜 실행
     ┌─────┴────────────┐
     │ 고대역 대상      │ 저속 주변장치
     ▼                  ▼
[AXI 독립 채널]   [AXI•APB 브리지]
 또는 [AHB]             │
                        ├─ APB 설정: PSEL
                        └─ APB 접근: PENABLE•PREADY
     └──────────┬───────┘
                ▼
3. 응답 변환•순서 정합
                │
                ▼
       [관리자 응답 반환]
```

### 동작 원리

1. **주소 디코딩·중재**: Master의 주소 전송 및 Interconnect 상의 주소 디코딩 및 중재(Arbitration).
2. **AXI 독립 채널 핸드셰이크**: AXI 계층에서 **VALID/READY 핸드셰이크**를 통한 병렬 Read/Write 실행.
3. **APB 브리지 변환**: 주변장치 접근 시 AXI/AHB 브리지에 의한 **PSEL**(Setup) -> **PENABLE/PREADY**(Enable) 2-Phase 신호 변환.
4. **응답 변환·순서 정합**: 완료 응답(BRESP, RRESP) 수용 및 Master로 거래 종료 반환.

#### 한줄 요약

- 요청은 주소 라우팅과 필요한 프로토콜 변환을 거쳐 대상에서 실행되고 응답 순서에 맞게 완료된다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **독립 채널(Independent Channel)**: AXI 버스 상의 5개 전용 물리 선로 (Read Addr, Read Data, Write Addr, Write Data, Write Resp).

</details>

| 비교 항목 | AXI (Advanced eXtensible Interface) | AHB (Advanced High-performance) | APB (Advanced Peripheral Bus) |
|:---|:---|:---|:---|
| 적용 기준 | 고성능 CPU, GPU, DDR/NPU 메모리 시 | 온칩 SRAM, DMA 등 중간급 인프라 시 | UART, GPIO, Timer 등 저속 I/O 제어 시 |
| 전송 구조 | 5개 **독립 채널**, Out-of-Order 실행 | 파이프라이닝 버스트, Single-Bus | 2-Phase (Setup/Enable) 단순 핸드셰이크 |
| 성능/복잡도 | 최고 성능, 높은 면적/복잡도 | 중간 성능, 표준 버스 면적 | 저성능/저전력, 극소 로직 면적 |

#### 한줄 요약

- 고대역 다중 거래에는 AXI, 중간급 파이프라인 경로에는 AHB, 단순 제어 레지스터에는 APB를 배치한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **CDC(Clock Domain Crossing)**: 서로 다른 동작 클록(Hz)을 사용하는 버스 블록 간 신호 수용 시 발생하는 준안정성(Metastability) 방지 기술.
- **Protocol Checker**: AMBA 핸드셰이크 라이프사이클 위반을 RTL 시뮬레이션 상에서 실시간 탐지하는 Verification IP.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| AXI Out-of-Order ID 혼선 시 데드락 발생 | **Protocol Checker** 및 Transaction Tracker 배치 | 핸드셰이크 에러 탐지 |
| 서브시스템 간 클록 속도 차이에 의한 **Metastability** | **CDC** Async FIFO 및 2-FF Synchronizer 구축 | 클록 도메인 도서 신호 안정화 |
| APB 억세스 병목으로 인한 AXI 버퍼 팽창 | 브리지 버퍼 튜닝 및 PREADY 타임아웃 예외 처리 | 고속 버스 지연 방지 |

> 사례: **AXI4** 고속 백본 및 **APB** 주변장치 브리지 융합 SoC 아키텍처 구축

#### 한줄 요약

- 거래 순서와 주소 지도 및 클록 도메인 경계를 함께 검증하여 응답 오배달과 준안정을 방지한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **AMBA 선택 기준(AMBA Selection Criteria)**: 대상 IP의 데이터 전송률, 동시성, 인터페이스 회로 면적에 기반한 채택 체계.

</details>

- **AMBA 선택 기준**에 따라 고속 컴퓨팅은 **AXI**, 중간 인프라는 **AHB**, 단순 주변장치 제어는 **APB** 적용

#### 한줄 요약

- SoC 서브시스템 대역폭 및 거래 특성에 맞춘 AXI/AHB/APB 계층화 및 표준 AMBA 버스 구축 체계 적용.
