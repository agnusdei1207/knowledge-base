---
sidebar:
  order: 83
  label: "083. 마이크로컨트롤러 vs 마이크로프로세서 (Microcontroller vs Microprocessor)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "마이크로컨트롤러 vs 마이크로프로세서 (Microcontroller vs Microprocessor)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **MCU(Microcontroller Unit)**: CPU 코어, ROM/Flash, RAM 및 I/O 주변장치(ADC, Timer, UART 등)를 단일 실리콘 칩에 집적(One-chip)한 저전력 제어용 반도체.
- **MPU(Microprocessor Unit)**: 외부 DRAM 및 스토리지 패브릭 억세스를 기본 전제로 하는 범용 고성능 연산 중심 반도체.

</details>

- 정의/개념: 하드웨어 온칩(On-chip) 통합도, MMU/OS 요구사항 및 실시간(Real-Time) 제어 목적에 따른 대표적 반도체 2대 분류인 **MCU vs MPU**
- 배경/필요성: 단일 칩 임베디드 소형화 제어 요구(MCU)와 고성능 멀티태스킹 OS(Linux/Windows) 구동 요구(MPU)에 따른 아키텍처 이원화

#### 한줄 요약

- 마이크로컨트롤러는 제어 자원을 한 칩에 통합하고, 마이크로프로세서는 외부 메모리와 입출력을 확장한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **온칩(On-Chip)**: CPU, 메모리, 주변장치가 단일 반도체 실리콘 다이 내부에 물리적으로 통합된 형태.
- **MMU(Memory Management Unit)**: 가상 메모리(Virtual Memory) 주소 변환 및 가상 공간 프로세스 메모리 보호를 수행하는 하드웨어 (MPU 필수 탑재).
- **RTOS(Real-Time Operating System)**: 결정적(Deterministic) 마감시간(Deadline) 제어를 전용 수행하는 경량 실시간 커널 (MCU 주요 구동).

</details>

- ROM, RAM, I/O를 단일 칩에 융합한 **온칩(On-chip)** 형태의 소형화 및 초저전력 구동 (MCU)
- 가상 메모리를 지원하는 **MMU** 내장 및 외부 고속 LPDDR/DDR 메모리 기반 고성능 멀티태스킹 (MPU)
- **RTOS/Bare-Metal** 기반 하드 실시간 제어(MCU) vs Rich OS(Linux/Android) 기반 대용량 애플리케이션 수용(MPU)

#### 한줄 요약

- 결정적 제어와 범용 OS 기능에 따라 MCU와 MPU를 구분한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **MCU 온칩 자원**: Flash Memory, SRAM, ADC/DAC, PWM, CAN/UART/SPI 등 단일 칩 내부 레지스터 자원.
- **MPU 외부 자원**: 외부 DRAM 컨트롤러(DDR4/5), PCIe 레인, 고속 시리얼 통신 등 오프칩 확장 자원.

</details>

```text
MCU 구조: [MCU 제어부] -- [MCU 온칩 자원]

MPU 구조: [MPU 처리부] -- [MPU 외부 자원]
```

선의 의미: MCU는 내부 온칩 통합 제어망을 구축하고, MPU는 고속 억세스 버스를 통해 외부 메모리/주변장치를 연동하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| MCU 제어부 | 경량 CPU 코어(Cortex-M 등) 기반 **RTOS** / Bare-Metal 하드 실시간 제어 |
| MCU 온칩 자원 | 단일 칩 내 상주하는 Flash/SRAM 및 물리 I/O(ADC, PWM, Timer) 제어 |
| MPU 처리부 | 고성능 멀티코어(Cortex-A 등), **MMU**, L1/L2/L3 캐시 기반 OS 제어 |
| MPU 외부 자원 | 오프칩 외부 LPDDR/DDR 메모리 버스 및 고속 인터페이스(PCIe, USB) 확장 |

#### 한줄 요약

- MCU 온칩 자원과 MPU 외부 자원의 통합·확장 구조를 비교한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

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

1. **하드 실시간 요구 판정**: 시스템 제어 주기의 **하드 실시간 요구** 및 마감시간 지연 한계성 평가.
2. **OS·응용 복잡도 판정**: 가상 메모리(**MMU**), GUI/Linux 운영체제 및 대용량 멀티태스킹 필요성 파악.
3. **메모리·I/O·전력 검증**: 온칩 메모리 범위 충족 시 **MCU**, 대용량 오프칩 필요 시 **MPU**선정.
4. **시간·장애 경계 검증**: 복합 요구 시 MCU+MPU 이원화 노드 맵핑 및 최종 선택 확정.

#### 한줄 요약

- 하드 실시간 요구 판정과 OS·응용 복잡도 판정을 함께 수행하여 MCU, MPU 또는 역할을 나눈 혼합 구성을 결정한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **WCET(Worst-Case Execution Time)**: 연산 수행 시 유발 가능한 최악 반응 지연시간 수치.

</details>

| 비교 항목 | 마이크로컨트롤러 (MCU) | 마이크로프로세서 (MPU) |
|:---|:---|:---|
| 시스템 통합도 | **온칩(On-chip)** (CPU + RAM + ROM + I/O 일체) | Off-chip (CPU 위주, 외부 DRAM/Flash 필수) |
| MMU 탑재 여부 | 미탑재 (가상 메모리 미지원, MPU 전용) | 탑재 (**MMU** 필수, 가상 메모리 및 OS 지원) |
| 전력 소비 및 비용 | 초저전력 (mW~μW 단위), 저비용 칩셋 | 고전력 (W 단위), 메인보드 설계 복잡 및 고비용 |
| 주요 운용 환경 | **RTOS**, Bare-Metal (하드 실시간 제어) | Linux, Android, Windows (범용 OS) |
| 대표적 칩셋 | ARM Cortex-M0/M3/M4, AVR, STM32 | ARM Cortex-A72/A78, Intel Core, AMD |

#### 한줄 요약

- 하드 실시간 제어는 MCU, 대용량 응용은 MPU가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **신호 무결성(Signal Integrity)**: MPU 오프칩 고속 메모리 버스 설계 시 전자기적 간섭(EMI) 및 노이즈를 억제하는 PCB 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| MPU 기반 OS 런타임의 비결정적 **지터(Jitter)** 발생 | MCU 코어 연동(Heterogeneous Multicore) 분담 | 하드 실시간성 보장 |
| MPU 오프칩 고속 메모리 라인 상의 **신호 무결성** 손상 | PCB 임피던스 매칭 및 고속 버스 차폐 | 노이즈 및 버스 에러 차단 |
| MCU 내부 RAM 풋프린트 부족 및 오버플로우 | 정적 메모리 할당 및 스택 튜닝 | 메모리 파손 방지 |

> 사례: STM32 **MCU** 기반 모터 실시간 제어 및 Raspberry Pi **MPU** 기반 GUI 터치 디스플레이 연동

#### 한줄 요약

- 실시간 코어와 MCU의 제어 분담으로 MPU의 지터를 격리한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **처리기 선택 기준(Processor Selection Criteria)**: 마감시간 임계성, 대용량 메모리 요구, 소비 전력 및 칩셋 비용에 기반한 결정 체계.

</details>

- **처리기 선택 기준**에 따라 센서/액추에이터 실시간 억세스는 **MCU**, 딥러닝/GUI/웹인프라는 **MPU** 채택

#### 한줄 요약

- 온칩 통합도, MMU/OS 요구사항 및 실시간 제어 반응성에 따른 MCU/MPU 차등 채택 및 최적 프로세서 아키텍처 구축 체계 적용.
