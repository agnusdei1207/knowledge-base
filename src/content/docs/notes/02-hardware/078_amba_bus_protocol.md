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

- **AMBA(Advanced Microcontroller Bus Architecture)**: Arm 사에서 제정한 SoC 내부 IP 블록(CPU, GPU, NPU, 메모리 컨트롤러, 주변장치) 간 고성능 연결 및 데이터 교환을 위한 개방형 표준 온칩 버스 프로토콜 규격.
- **시스템 온 칩(System on Chip, SoC)**: 연산 프로세서 코어, 고속 메모리 서브시스템 및 저속 I/O 주변장치를 단일 실리콘 다이에 통합 집적한 반도체.

</details>

- 정의/개념: 단일 실리콘 다이 내부의 다양한 성능 요구 조건을 만족하기 위해 **고성능 AXI, 시스템 백본 AHB, 저전력 제어 APB**로 계층화된 **AMBA(Advanced Microcontroller Bus Architecture) 온칩 버스 표준 규격**
- 배경/필요성: 수십 개 이상의 이종 IP가 단일 칩에 집적되는 현대 SoC 환경에서 **독자 버스 인터페이스로 인한 IP 재사용 불가, 설계 복잡도 폭증 및 온칩 통신 병목 해결**

#### 한줄 요약
- AMBA는 고성능 AXI, 백본 AHB, 저전력 APB로 역할을 분담하여 SoC 내부의 통신 대역폭과 전력 효율을 최적화하는 온칩 버스 표준이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **AXI 5대 독립 채널**: 쓰기 주소(AW), 쓰기 데이터(W), 쓰기 응답(B), 읽기 주소(AR), 읽기 데이터(R) 채널이 물리적으로 분리되어 전이중 동시 전송을 보장하는 구조.
- **아웃스탠딩 트랜잭션(Outstanding Transactions)**: 이전 요청의 데이터 수신 완료를 기다리지 않고 연속해서 다수의 읽기/쓰기 주소 명령을 파이프라인으로 미리 발행하는 기술.

</details>

- 5개 독립 채널 기반 전이중 전송: **AXI 채널 분리 구조(AW, W, B, AR, R)**를 통해 읽기와 쓰기를 동시에 병렬 처리
- 비순차(Out-of-Order) 완료 및 지연 은폐: 트랜잭션 ID(ARID/AWID) 태깅을 통해 메모리 응답 지연이 발생해도 **아웃스탠딩 트랜잭션**으로 대기 시간 최소화
- **VALID/READY 핸드셰이크**: 2선 양방향 신호 기반으로 송수신단 간의 클록 타이밍을 정합하고 자연스러운 백프레셔(Backpressure) 흐름 제어 실현

#### 한줄 요약
- 5개 독립 채널, VALID/READY 핸드셰이크, 아웃스탠딩 트랜잭션을 통해 고대역폭과 초저지연을 동시에 달성한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **AXI 크로스바 상호연결망(AXI Crossbar Interconnect)**: 다수의 마스터와 다수의 슬레이브 간 5개 채널 신호를 동시 스위칭하여 병렬 데이터 전송을 중재하는 상호연결망.
- **APB 브리지(APB Bridge)**: 고속 AXI/AHB 버스 트랜잭션을 저속 APB 버스의 2단계 제어 신호(PSEL/PENABLE)로 변환하고 완충하는 프로토콜 변환기.

</details>

```text
[AMBA 온칩 버스 계층 아키텍처]
 ┌─ [AXI 고성능 마스터 계층] ────────────── CPU 코어 클러스터 / GPU / NPU / 고속 DMA 엔진
 │                                                   │ (5개 독립 채널: AW, W, B, AR, R)
 ├─ [AXI 크로스바 상호연결망 (Interconnect)] ── [주소 디코딩 + 다중 중재기 (Arbiter)]
 │   ├─ 고속 메모리 슬레이브 ──────────────── LPDDR5/DDR5 컨트롤러 / 온칩 SRAM 컨트롤러
 │   └─ [AXI-to-APB 브리지 (Bridge)] ───────── 속도 정합 비동기 FIFO + 프로토콜 변환기
 │                                                   │ (PSEL, PENABLE, PADDR, PWDATA)
 └─ [APB 저속 주변장치 버스 계층] ────────── UART / SPI / I2C / 타이머 / WDT / GPIO
```

선의 의미: 가지(`├─`, `└─`)는 하드웨어 소속 및 계층적 연결 관계; 고속 AXI 마스터의 요청이 크로스바를 거쳐 메모리로 가거나 APB 브리지를 통해 주변장치로 전달됨

| 구성요소 | 계층 및 위치 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|:---|
| **AXI 마스터** | 고성능 연산단 | 주소 및 제어 트랜잭션을 능동 발행하여 대용량 메모리/장치 접근 | CPU, GPU, NPU |
| **AXI 크로스바** | 중앙 인터커넥트 | 5개 채널을 독립 스위칭하여 다중 마스터의 동시 접근 병렬 중재 | Non-blocking 스위칭 |
| **고속 슬레이브** | 메모리 컨트롤러단 | 고속 버스트(Burst) 트랜잭션을 수신하여 시스템 메모리에 데이터 R/W | DDR5/HBM 컨트롤러 |
| **APB 브리지** | 계층 전환단 | 고속 AXI 패킷을 저속 APB 2단계 타이밍으로 변환 완충 | 프로토콜 변환 |
| **APB 주변장치** | I/O 제어단 | UART, 타이머 등 저속/저전력 레지스터 읽기/쓰기 동작 수행 | 저전력 단순 로직 |

#### 한줄 요약
- AMBA 시스템은 AXI 마스터, AXI 크로스바 인터커넥트, 고속 메모리 슬레이브, APB 브리지 및 APB 주변장치로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **VALID/READY Handshake**: 송신자가 데이터 유효(VALID=1)를 알리고 수신자가 수신 준비(READY=1)를 완료하여 동일 클록 에지에서 둘 다 1일 때 데이터가 전송되는 동기화 규격.
- **PSEL / PENABLE 2단계 타이밍**: APB 프로토콜에서 1단계로 슬레이브를 선택(Setup: PSEL=1)하고, 2단계에서 전송을 활성화(Access: PENABLE=1)하여 데이터를 교환하는 방식.

</details>

```text
1. AXI 마스터: 읽기/쓰기 주소 채널(AR/AW)에 VALID=1 신호 및 목표 주소 인가
                      │
                      ▼
2. AXI 크로스바: 대상 주소 영역을 디코딩하여 타깃 슬레이브 판별
                      │
                      ▼
3. 타깃 장치가 고속 AXI 슬레이브(DDR)인가, 저속 APB 장치(UART)인가?
   ┌──────────────────┴──────────────────┐
[ 고속 AXI 슬레이브 (DDR) ]            [ 저속 APB 주변장치 (UART) ]
   │                                     │
   ▼                                     ▼
4. DDR 컨트롤러가 READY=1 응답           4. AXI-to-APB 브리지가 요청 수신
   ➔ 동일 클록에서 핸드셰이크 성립        │
   │                                     ▼
   ▼                                  5. Setup Phase (1사이클): PSEL=1 인가
5. 5개 독립 채널을 통해 버스트 전송      │
   (클록당 데이터 1개씩 고속 스트리밍)   ▼
   │                                  6. Access Phase (2사이클): PENABLE=1 인가
   │                                     ➔ 데이터 R/W 수행 완료
   │                                     │
   └──────────────────┬──────────────────┘
                      │
                      ▼
7. 응답 채널(B 또는 R)을 통해 마스터로 트랜잭션 완료(OKAY) 반환
```

분기 결과: **고속 메모리는** 1클록 핸드셰이크로 버스트 전송되며, **저속 주변장치는** APB 브리지를 통해 2단계 제어로 안전하게 감속 변환됨

#### 한줄 요약
- 마스터 요청 ➔ 크로스바 주소 디코딩 ➔ 고속 AXI 핸드셰이크 또는 APB 브리지 2단계 변환 ➔ 완료 응답 반환 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **AHB(Advanced High-Performance Bus)**: 주소와 데이터 단계를 2단계 파이프라인화하여 단일 클록 전송을 지원하는 중간 성능 버스.
- **CHI(Coherent Hub Interface)**: 패킷 기반 NoC(Network-on-Chip) 구조로 대규모 멀티코어 간 완전한 캐시 일관성(Hardware Cache Coherency)을 제공하는 차세대 규격.

</details>

| AMBA 버스 규격 | AXI (Advanced eXtensible) | AHB (Advanced High-Performance) | APB (Advanced Peripheral) | CHI (Coherent Hub Interface) |
|:---|:---|:---|:---|:---|
| 핵심 버스 구조 | **5개 독립 채널, 점대점 크로스바** | 단일 공유 버스, 2단계 파이프라인 | 2단계 비파이프라인 단순 제어 | **패킷 기반 온칩 NoC 토폴로지** |
| 전송 모드 | **비순차(Out-of-Order) 버스트** | 순차적 파이프라인 버스트 | 단일 전송 (Burst 미지원) | 분산 패킷 라우팅 및 캐시 일관성 |
| 최우선 설계 목표 | **초고대역폭 및 고성능** | 단순 온칩 시스템 백본 | **초저전력 및 최소 배선 면적** | **대규모 멀티코어/칩렛 캐시 공유** |
| 주요 적용 분야 | **CPU, GPU, NPU, DDR 컨트롤러** | 온칩 SRAM, 레거시 임베디드 DMA | **UART, SPI, I2C, 타이머, GPIO** | **서버용 멀티코어 CPU, 대형 AI SoC** |

#### 한줄 요약
- 고성능 메인 백본은 AXI, 단순 온칩 메모리는 AHB, 저전력 제어는 APB, 대규모 캐시 일관성 NoC에는 CHI를 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **클록 도메인 교차(Clock Domain Crossing, CDC)**: 1GHz 고속 AXI 도메인과 50MHz 저속 APB 도메인 간에 신호가 넘어갈 때 발생하는 메타스테이빌리티(Metastability)를 방지하는 비동기 이중화 설계.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 고속 AXI(1GHz)와 저속 APB(50MHz) 간 **클록 도메인 교차(CDC)** 메타스테이빌리티 | **그레이 코드(Gray Code) 포인터 기반 비동기 CDC FIFO 구축** | 비동기 신호 전이 안정화 및 데이터 유실 0화 |
| 저속 APB 장치의 응답 지연으로 인한 AXI 메인 버스 연쇄 블로킹 | **하드웨어 타임아웃 타이머 및 슬레이브 에러(SLVERR) 강제 반환** | 지연 트랜잭션 조기 격리 및 메인 버스 가용성 사수 |
| 다중 마스터 동시 접근 시 AXI 크로스바 대역폭 기아(Starvation) | **가중치 라운드로빈(WRR) 기반 QoS 대역폭 중재기 실장** | 고우선순위 실시간 IP의 최소 대역폭 보장 |

#### 한줄 요약
- 실무에서는 CDC 비동기 FIFO로 클록 불일치를 잡고, 타임아웃으로 블로킹을 방지하며, WRR QoS로 대역폭을 공정 배분한다.

## Ⅶ. 결론

- 고성능 SoC 및 칩렛 아키텍처 설계를 위해 **대용량 데이터 이동 구간에는 5채널 AXI5/CHI 크로스바 백본을 표준 구축**하고, **주변장치 제어 구간에는 AXI-to-APB 브리지를 계층화**하여 PPA(성능·전력·면적)를 최적화하며, 시스템 안정성을 위해 **CDC 비동기 FIFO 및 QoS 대역폭 중재 체계**를 필수 구현하는 고신뢰 온칩 인터커넥트 확립

#### 한줄 요약
- AMBA는 IP 재사용성과 확장성을 보장하여 복잡한 시스템 반도체를 모듈식으로 구현하는 글로벌 표준 온칩 버스다.