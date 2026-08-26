---
sidebar:
  order: 78
  label: "078. AMBA 버스 프로토콜 (AMBA Bus Protocol)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "AMBA 버스 프로토콜 (AMBA Bus Protocol)"
date: "2026-08-26T10:45:00+09:00"
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

- **AMBA(Advanced Microcontroller Bus Architecture)**: Arm 사에서 제정한 SoC 내부 IP 블록(CPU, GPU, NPU, 메모리 컨트롤러, 주변장치) 간 고성능 연결 및 데이터 교환을 위한 개방형 표준 온칩 버스 프로토콜 규격.
- **시스템 온 칩(System on Chip, SoC)**: 연산 프로세서 코어, 고속 메모리 서브시스템 및 저속 I/O 주변장치를 단일 실리콘 다이에 통합 집적한 반도체.

</details>

- 정의/개념: 성능 및 전력 요구 조건에 따라 고성능 AXI, 시스템 백본 AHB, 저전력 APB로 계층화한 **AMBA 온칩 버스 표준 규격**
- 배경/필요성: 독자 인터페이스로 인한 **IP 재사용 한계**와 복잡도 증가로 SoC 내부 **온칩 통신 병목** 발생

#### 한줄 요약
- AMBA는 고성능 AXI, 백본 AHB, 저전력 APB로 역할을 분담하여 SoC 내부의 통신 대역폭과 전력 효율을 최적화하는 온칩 버스 표준이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **AXI 5대 독립 채널**: 쓰기 주소(AW), 쓰기 데이터(W), 쓰기 응답(B), 읽기 주소(AR), 읽기 데이터(R) 채널이 물리적으로 분리되어 전이중 동시 전송을 보장하는 구조.
- **아웃스탠딩 트랜잭션(Outstanding Transactions)**: 이전 요청의 데이터 수신 완료를 기다리지 않고 연속해서 다수의 읽기/쓰기 주소 명령을 파이프라인으로 미리 발행하는 기술.

</details>

- 5개 독립 채널 기반 전이중 전송: **AXI 5채널 분리(AW, W, B, AR, R)** 구조를 통해 읽기와 쓰기 동시 병렬 처리
- 비순차 완료 및 지연 은폐: 트랜잭션 ID 태깅을 통해 메모리 응답 지연을 완화하는 **아웃스탠딩 트랜잭션** 지원
- VALID/READY 핸드셰이크: 2선 양방향 신호 기반 클록 동기화 및 **백프레셔(Backpressure)** 흐름 제어 실현

#### 한줄 요약
- 5개 독립 채널, VALID/READY 핸드셰이크, 아웃스탠딩 트랜잭션을 통해 고대역폭과 초저지연을 동시에 달성한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **AXI 크로스바 상호연결망(AXI Crossbar Interconnect)**: 다수의 마스터와 다수의 슬레이브 간 5개 채널 신호를 동시 스위칭하여 병렬 데이터 전송을 중재하는 상호연결망.
- **APB 브리지(APB Bridge)**: 고속 AXI/AHB 버스 트랜잭션을 저속 APB 버스의 2단계 제어 신호(PSEL/PENABLE)로 변환하고 완충하는 프로토콜 변환기.

</details>

```text
[AMBA 온칩 버스 계층 아키텍처]
├── AXI 고성능 마스터 계층: CPU 코어, GPU, NPU, DMA 엔진
├── AXI 크로스바 상호연결망 (Interconnect): 주소 디코더, 다중 중재기
│   ├── 고속 메모리 슬레이브: LPDDR5/DDR5 컨트롤러, 온칩 SRAM
│   └── AXI-to-APB 브리지 (Bridge): 속도 정합 비동기 FIFO, 프로토콜 변환기
└── APB 저속 주변장치 버스 계층: UART, SPI, I2C, 타이머, GPIO
```

선의 의미: 가지(`├──`, `└──`)는 계층별 하드웨어 소속 및 상호연결 관계; 고속 AXI 마스터의 요청이 크로스바를 거쳐 메모리로 가거나 APB 브리지를 통해 주변장치로 전달됨

| 구성요소 | 계층 및 위치 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|:---|
| AXI 마스터 | 고성능 연산단 | 주소 및 제어 트랜잭션을 능동 발행하여 **대용량 데이터 전송** 주도 | CPU, GPU, NPU |
| AXI 크로스바 | 중앙 인터커넥트 | 5개 채널을 독립 스위칭하여 다중 마스터의 동시 접근을 **Non-blocking 중재** | 채널 분리 스위칭 |
| 고속 슬레이브 | 메모리 제어단 | **버스트(Burst) 트랜잭션**을 수신하여 시스템 메모리에 데이터 판독/기록 | DDR5/HBM 컨트롤러 |
| APB 브리지 | 계층 전환단 | 고속 AXI 패킷을 저속 APB **2단계 타이밍**으로 변환 완충 | 프로토콜 변환 |
| APB 주변장치 | I/O 제어단 | UART, 타이머 등 레지스터 기반 **저속 제어 동작** 수행 | 저전력 단순 로직 |

#### 한줄 요약
- AMBA 시스템은 AXI 마스터, AXI 크로스바 인터커넥트, 고속 메모리 슬레이브, APB 브리지 및 APB 주변장치로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **VALID/READY Handshake**: 송신자가 데이터 유효(VALID=1)를 알리고 수신자가 수신 준비(READY=1)를 완료하여 동일 클록 에지에서 둘 다 1일 때 데이터가 전송되는 동기화 규격.
- **PSEL / PENABLE 2단계 타이밍**: APB 프로토콜에서 1단계로 슬레이브를 선택(Setup: PSEL=1)하고, 2단계에서 전송을 활성화(Access: PENABLE=1)하여 데이터를 교환하는 방식.

</details>

```text
1. AXI 마스터: 읽기/쓰기 주소 채널(AR/AW)에 VALID=1 및 목표 주소 인가
                      │
                      ▼
2. AXI 크로스바: 대상 주소 영역 디코딩을 통한 타깃 슬레이브 판별
                      │
                      ▼
3. 타깃 장치 속성(고속 AXI 메모리 vs 저속 APB 장치) 분기 판정
   ├── [고속 AXI 메모리]: DDR 컨트롤러 READY=1 응답 ➔ 5개 채널 기반 버스트 전송
   └── [저속 APB 장치]: AXI-to-APB 브리지 수신 ➔ Setup(PSEL) 및 Access(PENABLE) 수행
                      │
                      ▼
4. 응답 채널(B 또는 R)을 통해 마스터로 OKAY 완료 응답 전달
                      │
                      ▼
[트랜잭션 종료]: 버스 핸드셰이크 해제 및 다음 트랜잭션 대기
```

분기 결과: 고속 메모리는 **1클록 핸드셰이크**로 버스트 전송하며 저속 주변장치는 **APB 브리지**로 감속 제어

#### 한줄 요약
- 마스터 요청 ➔ 크로스바 주소 디코딩 ➔ 고속 AXI 핸드셰이크 또는 APB 브리지 2단계 변환 ➔ 완료 응답 반환 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **AHB(Advanced High-Performance Bus)**: 주소와 데이터 단계를 2단계 파이프라인화하여 단일 클록 전송을 지원하는 중간 성능 버스.
- **CHI(Coherent Hub Interface)**: 패킷 기반 NoC(Network-on-Chip) 구조로 대규모 멀티코어 간 완전한 캐시 일관성(Hardware Cache Coherency)을 제공하는 차세대 규격.

</details>

| AMBA 버스 규격 | AXI (Advanced eXtensible) | AHB (Advanced High-Performance) | APB (Advanced Peripheral) | CHI (Coherent Hub Interface) |
|:---|:---|:---|:---|:---|
| 핵심 버스 구조 | **5개 독립 채널**, 점대점 크로스바 | 단일 공유 버스, 2단계 파이프라인 | 2단계 비파이프라인 단순 제어 | **온칩 NoC 토폴로지** |
| 전송 모드 | **비순차 버스트** 전송 | 순차적 파이프라인 버스트 | 단일 전송 (Burst 미지원) | **캐시 일관성** 패킷 라우팅 |
| 최우선 설계 목표 | **초고대역폭** 및 초저지연 | 단순 온칩 시스템 백본 | **초저전력** 및 배선 최소화 | 대규모 멀티코어 캐시 공유 |
| 주요 적용 분야 | **CPU, GPU, NPU**, 메모리 | 온칩 SRAM, 임베디드 DMA | **UART, SPI, I2C**, 타이머 | **서버용 멀티코어**, 대형 AI SoC |

#### 한줄 요약
- 고성능 메인 백본은 AXI, 단순 온칩 메모리는 AHB, 저전력 제어는 APB, 대규모 캐시 일관성 NoC에는 CHI를 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **클록 도메인 교차(Clock Domain Crossing, CDC)**: 1GHz 고속 AXI 도메인과 50MHz 저속 APB 도메인 간에 신호가 넘어갈 때 발생하는 메타스테이빌리티(Metastability)를 방지하는 비동기 이중화 설계.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| AXI와 APB 간 클록 도메인 교차(CDC) 메타스테이빌리티 | **그레이 코드(Gray Code)** 기반 비동기 CDC FIFO 구축 | 비동기 신호 전이 안정화 및 데이터 유실 방지 |
| 저속 APB 장치 지연으로 인한 메인 버스 연쇄 블로킹 | 하드웨어 **타임아웃 타이머** 및 슬레이브 에러(SLVERR) 반환 | 지연 트랜잭션 격리 및 버스 가용성 확보 |
| 다중 마스터 동시 접근 시 AXI 크로스바 대역폭 기아 | **가중치 라운드로빈(WRR)** 기반 QoS 대역폭 중재기 실장 | 고우선순위 실시간 IP의 최소 대역폭 보장 |

#### 한줄 요약
- 실무에서는 CDC 비동기 FIFO로 클록 불일치를 잡고, 타임아웃으로 블로킹을 방지하며, WRR QoS로 대역폭을 공정 배분한다.

## Ⅶ. 결론

- IP 대역폭 요구량 분석 기반 **AXI5/CHI 백본**과 **계층형 APB 브리지** 구조 적용

#### 한줄 요약
- AMBA는 IP 재사용성과 확장성을 보장하여 복잡한 시스템 반도체를 모듈식으로 구현하는 글로벌 표준 온칩 버스다.