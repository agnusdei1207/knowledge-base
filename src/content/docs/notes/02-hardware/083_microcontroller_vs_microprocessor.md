---
sidebar:
  order: 83
  label: "083. 마이크로컨트롤러 vs 마이크로프로세서 (Microcontroller vs Microprocessor)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "마이크로컨트롤러 vs 마이크로프로세서 (Microcontroller vs Microprocessor)"
date: "2026-08-13T12:21:04+09:00"
tags:
  - "notes-hardware"
weight: 83
extra:
  question_no: "083"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "통합도•시간 제약•OS 요구 비교"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **MCU(Microcontroller Unit)**: CPU 코어, ROM/Flash, RAM 및 I/O 주변장치(ADC, Timer, UART 등)를 단일 실리콘 칩에 집적(One-chip)한 저전력 제어용 반도체.
- **MPU(Microprocessor Unit)**: 외부 메모리와 주변장치를 확장해 범용 OS와 고성능 응용을 처리하는 프로세서.

</details>

- 정의/개념: 하드웨어 온칩(On-chip) 통합도, MMU/OS 요구사항 및 실시간(Real-Time) 제어 목적에 따른 대표적 반도체 2대 분류인 **MCU vs MPU**
- 배경/필요성: MCU 자원은 범용 OS에 부족하고 MPU 지터·전력은 단순 제어에 부담

#### 한줄 요약

- 마이크로컨트롤러는 제어 자원을 한 칩에 통합하고, 마이크로프로세서는 외부 메모리와 입출력을 확장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **온칩(On-Chip)**: CPU, 메모리, 주변장치가 단일 반도체 실리콘 다이 내부에 물리적으로 통합된 형태.
- **MMU(Memory Management Unit)**: 가상 주소 변환과 프로세스별 메모리 보호를 수행하는 하드웨어.
- **RTOS(Real-Time Operating System)**: 결정적(Deterministic) 마감시간(Deadline) 제어를 전용 수행하는 경량 실시간 커널 (MCU 주요 구동).

- **실시간 운영체제 및 베어메탈(RTOS / Bare-Metal)**: 복잡한 가상 메모리 관리 없이 결정론적(Deterministic) 초저지연 응답을 보장하는 임베디드 펌웨어 실행 환경.
</details>

- ROM, RAM, I/O를 단일 칩에 융합한 **온칩** 형태의 소형화 및 초저전력 구동 (MCU)
- 가상 메모리를 지원하는 **MMU** 내장 및 외부 고속 LPDDR/DDR 메모리 기반 고성능 멀티태스킹 (MPU)
- **RTOS/Bare-Metal** 기반 하드 실시간 제어(MCU) vs Rich OS(Linux/Android) 기반 대용량 애플리케이션 수용(MPU)

#### 한줄 요약

- 결정적 제어와 범용 OS 기능에 따라 MCU와 MPU를 구분한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **MCU 온칩 자원**: Flash Memory, SRAM, ADC/DAC, PWM, CAN/UART/SPI 등 단일 칩 내부 레지스터 자원.
- **MPU 외부 자원**: 외부 DRAM 컨트롤러(DDR4/5), PCIe 레인, 고속 시리얼 통신 등 오프칩 확장 자원.

</details>

```text
MCU 구조: [MCU 제어부] -- [MCU 온칩 자원]

MPU 구조: [MPU 처리부] -- [MPU 외부 자원]
```

선의 의미: MCU는 온칩 제어 자원을 통합하고, MPU는 고속 버스로 외부 메모리·주변장치를 확장하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| MCU 제어부 | 경량 CPU 코어(Cortex-M 등) 기반 **RTOS** / Bare-Metal 하드 실시간 제어 |
| MCU 온칩 자원 | 단일 칩 내 상주하는 Flash/SRAM 및 물리 I/O(ADC, PWM, Timer) 제어 |
| MPU 처리부 | 고성능 멀티코어(Cortex-A 등), **MMU**, L1/L2/L3 캐시 기반 OS 제어 |
| MPU 외부 자원 | 오프칩 외부 LPDDR/DDR 메모리 버스 및 고속 인터페이스(PCIe, USB) 확장 |

#### 한줄 요약

- MCU 온칩 자원과 MPU 외부 자원의 통합·확장 구조를 비교한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **하드 실시간 요구(Hard Real-time Demand)**: 센서/모터 제어 시 마감시간(Deadline) 지연이 치명적 사고로 이어지는 제약.

</details>

```text
[시스템 시간•기능 요구]
           │
           ▼
1. 하드 실시간 요구 판정
           │
           ▼
2. OS•응용 복잡도 판정
     ┌─────┼──────────┐
     │ 제어 중심      │ 응용 중심     │ 동시 요구
     ▼                ▼               ▼
   [MCU]            [MPU]       [MCU + MPU 분할]
     └─────────┬──────┴───────────────┘
               ▼
3. 메모리•I/O•전력 검증
               │
               ▼
4. 시간•장애 경계 검증
               │
               ▼
         [처리기 구성 확정]
```

### 동작 원리

1. 하드 실시간 요구 판정: 시스템 제어 주기의 **하드 실시간 요구** 및 마감시간 지연 한계성 평가.
2. OS·응용 복잡도 판정: 가상 메모리(**MMU**), GUI/Linux 운영체제 및 대용량 멀티태스킹 필요성 파악.
3. 메모리·I/O·전력 검증: 온칩 자원으로 충족하면 **MCU**, 대용량 외부 메모리가 필요하면 **MPU** 선정.
4. 시간·장애 경계 검증: 복합 요구는 MCU와 MPU의 역할·장애 경계를 분리해 구성 확정.

#### 한줄 요약

- 하드 실시간 요구 판정과 OS·응용 복잡도 판정을 함께 수행하여 MCU, MPU 또는 역할을 나눈 혼합 구성을 결정한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **WCET(Worst-Case Execution Time)**: 태스크 자체 연산이 완료되는 최악 실행시간 상한.

</details>

| 비교 항목 | 마이크로컨트롤러 (MCU) | 마이크로프로세서 (MPU) |
|:---|:---|:---|
| 시스템 통합도 | **온칩** 메모리·I/O 통합 중심 | 외부 메모리·고속 I/O 확장 중심 |
| 주소 관리 | 제한된 주소 공간과 정적 메모리 중심 | **MMU** 기반 가상 메모리 지원이 일반적 |
| 전력 소비 및 비용 | 상대적으로 낮은 전력과 보드 복잡도 | 상대적으로 높은 전력과 보드 복잡도 |
| 주요 운용 환경 | **RTOS**, Bare-Metal (하드 실시간 제어) | Linux, Android, Windows (범용 OS) |
| 대표적 칩셋 | ARM Cortex-M0/M3/M4, AVR, STM32 | ARM Cortex-A72/A78, Intel Core, AMD |

#### 한줄 요약

- 하드 실시간 제어는 MCU, 대용량 응용은 MPU가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **신호 무결성(Signal Integrity)**: MPU 오프칩 고속 메모리 버스 설계 시 전자기적 간섭(EMI) 및 노이즈를 억제하는 PCB 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| MPU 기반 OS 런타임의 비결정적 **지터** 발생 | MCU와 MPU의 제어·응용 역할 분담 | 실시간 제어 경로의 지터 격리 |
| MPU 오프칩 고속 메모리 라인 상의 **신호 무결성** 손상 | PCB 임피던스 매칭 및 고속 버스 차폐 | 노이즈 및 버스 에러 차단 |
| MCU 내부 RAM 풋프린트 부족 및 오버플로우 | 정적 메모리 할당 및 스택 튜닝 | 메모리 파손 방지 |

> 사례: STM32 **MCU** 기반 모터 실시간 제어 및 Raspberry Pi **MPU** 기반 GUI 터치 디스플레이 연동

#### 한줄 요약

- 실시간 코어와 MCU의 제어 분담으로 MPU의 지터를 격리한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **처리기 선택 기준(Processor Selection Criteria)**: 마감시간 임계성, 대용량 메모리 요구, 소비 전력 및 칩셋 비용에 기반한 결정 체계.

</details>

- **처리기 선택 기준**에 따라 센서/액추에이터 실시간 억세스는 **MCU**, 딥러닝/GUI/웹인프라는 **MPU** 채택

#### 한줄 요약

- 실시간 저전력 제어는 MCU, 범용 OS·대용량 응용은 MPU를 선택한다.
