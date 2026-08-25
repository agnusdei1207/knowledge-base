---
sidebar:
  order: 78
  label: "078. AMBA 버스 프로토콜 (AMBA Bus Protocol)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "AMBA 버스 프로토콜 (AMBA Bus Protocol)"
date: "2026-08-25T10:25:00+09:00"
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

- **AMBA(Advanced Microcontroller Bus Architecture)**: Arm 사에서 제정한 SoC 내부 IP 블록 간 고성능 연결 및 데이터 교환을 위한 개방형 표준 온칩 버스 규격.
- **SoC(System on Chip)**: CPU, GPU, NPU, 메모리 컨트롤러 및 주변장치를 단일 실리콘 칩 다이에 통합한 시스템 반도체.

</details>

- 정의/개념: SoC 내부 이종 IP 간의 고속 연결 및 통신을 위해 계층별 최적화된 온칩 표준 버스 **AMBA** 규격
- 배경/필요성: 단일 실리콘 다이에 다수 이종 IP 집적 시 **독자 인터페이스의 호환성 결여 및 온칩 통신 병목 해결 불가**

#### 한줄 요약
- 고성능 AXI, 시스템 백본 AHB, 저전력 제어 APB로 계층화하여 온칩 상호연결을 최적화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **AXI(Advanced eXtensible Interface)**: 읽기/쓰기 주소 및 데이터 등 5개 독립 채널을 통해 비순차(Out-of-Order) 버스트 전송을 지원하는 고성능 버스.
- **아웃스탠딩 트랜잭션(Outstanding Transaction)**: 이전 요청의 완료 응답을 기다리지 않고 연속해서 다수의 읽기/쓰기 명령을 발행하는 파이프라인 기법.

</details>

- **AXI** 프로토콜의 5개 독립 채널(AW, W, B, AR, R)을 통한 전이중 동시 전송
- **아웃스탠딩 트랜잭션** 및 비순차(Out-of-Order) 응답을 통한 지연시간 은폐
- VALID/READY 2선 양방향 핸드셰이크 기반의 비동기 속도 정합 및 백프레셔 제어

#### 한줄 요약
- 5개 독립 채널과 VALID/READY 핸드셰이크를 통해 고대역폭 비순차 데이터 전송을 실현한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **AXI 크로스바(Crossbar)**: 다수의 마스터와 슬레이브 간 5개 채널 신호를 동시 스위칭하여 병렬 데이터 전송을 지원하는 상호연결망.
- **APB 브리지(Bridge)**: 고속 AXI/AHB 버스 프로토콜을 저속 APB 버스의 2단계 제어 신호로 변환하는 프로토콜 변환기.

</details>

```text
[AMBA 온칩 버스 계층 구조]
|-- AXI 마스터 계층 (CPU 코어·GPU·NPU·고속 DMA)
|-- AXI 크로스바 상호연결망 (5개 채널 디코딩 및 다중 중재)
|   |-- 고속 슬레이브 (DDR5 메모리 컨트롤러·온칩 SRAM)
|   `-- AXI-to-APB 브리지 (속도 및 프로토콜 변환)
`-- APB 저속 주변장치 버스
    |-- 통신 인터페이스 (UART·I2C·SPI)
    `-- 시스템 제어기 (하드웨어 타이머·WDT·GPIO)
```

선의 의미: 계층 및 버스 브리지 구조

| 구성요소 | 책임 |
|:---|:---|
| AXI 마스터 | 주소 및 제어 트랜잭션을 능동적으로 생성하여 버스에 전달 (CPU, GPU) |
| **AXI 크로스바** | 5개 독립 채널을 디코딩하여 다중 마스터 요청을 병렬 라우팅 및 중재 |
| **APB 브리지** | 고속 AXI 패킷을 저속 APB 타이밍(Setup/Access)으로 변환 완충 |
| 고속 슬레이브 | DDR 컨트롤러 등 대용량 고속 버스트 트랜잭션 수신 및 처리 |
| APB 주변장치 | UART, 타이머 등 저속/저전력 레지스터 읽기 및 쓰기 동작 수행 |

#### 한줄 요약
- AXI 마스터, 크로스바 인터커넥트, APB 브리지, 주변장치 슬레이브가 계층적으로 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **VALID/READY Handshake**: 송신자가 데이터 유효(VALID=1)를 알리고 수신자가 수신 준비(READY=1)를 완료하여 동일 클록 에지에서 둘 다 1일 때 전송이 성립되는 AXI 표준 동기화 기법.
- **PSEL / PENABLE**: APB 프로토콜에서 대상 슬레이브 선택(Setup Phase: PSEL=1) 후 다음 사이클에서 데이터 전송을 활성화(Access Phase: PENABLE=1)하는 2단계 신호.

</details>

```text
AXI 마스터가 주소 채널(AR/AW)에 VALID 신호 송출
        │
   AXI 크로스바가 목적지 주소 영역을 디코딩
        │
   대상 장치가 고속 AXI 슬레이브인가?
   ┌────┴─────┐
  예           아니오 (저속 APB 장치)
   │             │
VALID/READY     AXI-APB 브리지가 요청 수신
핸드셰이크로      │
1 클록 버스트     PSEL=1 (Setup Phase, 1사이클)
데이터 전송 완료   │
   │            PENABLE=1 (Access Phase, 2사이클) 저속 전송
   │             │
   └────┬────────┘
        │
   응답 채널(B/R)을 통해 마스터로 전송 완료(OKAY) 반환
```

#### 한줄 요약
- 마스터 요청 → 주소 디코딩 → 고속 AXI 전송 또는 APB 브리지 2단계 변환 → 응답 반환 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **AHB(Advanced High-Performance Bus)**: 주소와 데이터 단계를 파이프라인화하여 단일 클록 전송을 지원하는 중간 성능 버스.
- **APB(Advanced Peripheral Bus)**: 단순한 2단계 제어로 배선과 전력을 극소화한 제어 전용 버스.

</details>

| AMBA 버스 프로토콜 | AXI (Advanced eXtensible) | AHB (Advanced High-performance) | APB (Advanced Peripheral) | CHI (Coherent Hub Interface) |
|:---|:---|:---|:---|:---|
| 채널 구조 및 전송 | 5개 독립 채널, 비순차 버스트 | 단일 공유 버스, 파이프라인 버스트 | 2단계 비파이프라인 제어 | 패킷 기반 NoC, 캐시 일관성 |
| 주 용도 및 대역폭 | CPU, GPU, NPU, DDR 컨트롤러 | 온칩 SRAM, DMA 제어기 | UART, 타이머, I2C, GPIO | 멀티코어 클러스터, 칩렛 백본 |
| 한계 및 복잡도 | 배선 및 로직 면적 오버헤드 | 다중 마스터 경합 시 병목 | 대용량 고속 버스트 불가 | 프로토콜 검증 난이도 극상 |

#### 한줄 요약
- 고대역폭 메인 백본은 AXI, 단순 온칩 메모리는 AHB, 저전력 제어는 APB, 칩렛 캐시 일관성은 CHI를 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **CDC(Clock Domain Crossing)**: 1GHz 고속 AXI 도메인과 50MHz 저속 APB 도메인 간 신호 전달 시 발생하는 메타스테이빌리티(Metastability)를 방지하기 위한 비동기 FIFO 구조.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 비순차 전송 시 AXI 트랜잭션 ID 순서 꼬임 데드락 | Assertion 기반 Protocol Checker 전수 검증 | 프로토콜 위반 조기 탐지 및 버스 락 방지 |
| 고속 AXI와 저속 APB 간 클록 불일치 메타스테이빌리티 | 클록 도메인 교차 지점에 **CDC 비동기 FIFO** 구축 | 비동기 신호 동기화 및 데이터 정합성 보장 |
| 저속 APB 슬레이브 지연으로 인한 AXI 버스 연쇄 블로킹 | 하드웨어 타임아웃 및 슬레이브 에러(SLVERR) 강제 반환 | 지연 트랜잭션 조기 격리 및 메인 버스 가용성 확보 |
| 다중 마스터 동시 접근 시 AXI 크로스바 대역폭 포화 | QoS 기반 가중치 라운드로빈(WRR) 중재기 구성 | 고우선순위 실시간 IP의 최소 대역폭 보장 |

#### 한줄 요약
- Protocol Checker 검증, CDC 비동기 FIFO, 하드웨어 타임아웃 격리, QoS 중재기로 온칩 버스 신뢰성을 확보한다.

## Ⅶ. 결론

- 고성능 SoC 및 칩렛 설계 시 **AXI5/CHI 기반 메인 백본**을 구축하고, **AXI-APB 계층화 브리지**를 통해 PPA(성능·전력·면적) 최적화 달성

#### 한줄 요약
- AMBA는 IP 재사용성과 확장성을 보장하여 복잡한 시스템 반도체를 빠르고 안정적으로 구현하는 산업 표준 버스다.