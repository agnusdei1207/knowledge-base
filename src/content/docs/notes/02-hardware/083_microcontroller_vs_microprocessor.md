---
sidebar:
  order: 83
  label: "083. 마이크로컨트롤러 vs 마이크로프로세서"
  badge:
    text: "미출 · 50%"
    variant: note
title: "마이크로컨트롤러 vs 마이크로프로세서 (Microcontroller vs Microprocessor)"
date: "2026-09-07T09:45:00+09:00"
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

- **마이크로컨트롤러(Microcontroller Unit, MCU)**: 경량 CPU 코어와 함께 SRAM, Flash ROM, 타이머, ADC, PWM 및 통신 인터페이스를 단일 실리콘 다이에 원칩 통합한 초저전력 실시간 제어 전용 반도체.
- **마이크로프로세서(Microprocessor Unit, MPU)**: 고성능 다중 CPU 코어 중심의 연산 장치로, 외장 DRAM, 대용량 스토리지 및 MMU를 결합하여 Linux/Android 등 범용 OS(Rich OS)를 구동하는 고성능 컴퓨팅 프로세서.

</details>

- 정의/개념: 메모리와 입출력 주변장치를 원칩 집적한 **MCU**(Microcontroller)와 외장 고속 메모리 및 MMU 기반으로 고성능 OS를 구동하는 **MPU**(Microprocessor) 아키텍처 비교
- 배경/필요성: 임베디드 시스템에서 단일 아키텍처로는 초저전력 실시간 제어(**MCU**)와 고성능 멀티태스킹(MPU) 요구를 동시 충족할 수 없는 공학적 상충 한계

#### 한줄 요약
- 실시간성과 초저전력 제어에는 온칩 올인원 MCU가, 복잡한 연산과 Rich OS/GUI 구동에는 확장형 MPU가 쓰인다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **결정론적 응답 지연(Deterministic Latency)**: 외부 하드웨어 인터럽트 발생 시 처리 개시까지의 지연시간 편차가 극도로 작아 마이크로초($\mu\text{s}$) 단위로 마감시간을 확정보장하는 특성.
- **메모리 관리 장치(Memory Management Unit, MMU)**: 가상 메모리 주소를 물리 주소로 동적 변환하고 프로세스 간 메모리 보호 및 요구 페이징을 지원하여 범용 OS를 구동하는 하드웨어.

</details>

- MCU의 강점: 온칩 SRAM/Flash 내장으로 결정론적 지연 및 밀리와트(mW) 단위 초저전력 동작
- MPU의 강점: 기가헤르츠(GHz) 멀티코어 및 **MMU** 탑재로 범용 운영체제 완벽 구동
- 이종 통합(Hybrid SoC): MPU 코어와 MCU 코어를 단일 칩에 결합한 이종 하이브리드 SoC 확산

#### 한줄 요약
- 하드웨어 집적도와 MMU 유무에 따라 실시간 제어(MCU)와 고성능 멀티태스킹(MPU)으로 역할이 갈린다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **온칩 주변장치(On-Chip Peripherals)**: MCU 실리콘 내부에 내장된 아날로그-디지털 변환기(ADC), PWM 신호 발생기, 워치독 타이머(WDT), CAN/SPI 컨트롤러.

</details>

```text
[MCU vs MPU 시스템 아키텍처 비교]
  │
  ├─ [마이크로컨트롤러 (MCU)] (원칩 올인원 제어)
  │     ├─ [경량 연산 코어] (ARM Cortex-M, RISC-V)
  │     ├─ [온칩 내장 메모리] (SRAM, Flash ROM)
  │     └─ [온칩 주변장치] (ADC, PWM, CAN, WDT)
  │
  └─ [마이크로프로세서 (MPU)] (고성능 확장 컴퓨팅)
        ├─ [고성능 멀티코어] (ARM Cortex-A, x86 캐시)
        ├─ [메모리 관리 장치] (MMU 가상 메모리/격리)
        ├─ [외장 메모리 인터페이스] (DDR4/DDR5 컨트롤러)
        └─ [고속 I/O 버스] (PCIe, USB 3.0, UFS)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 비교 항목 | MCU (마이크로컨트롤러) | MPU (마이크로프로세서) |
|:---|:---|:---|
| 연산 코어 | 수십~수백 MHz 경량 코어로 확정적 명령어 실행 | 수 GHz 고성능 멀티코어로 대용량 스레드 병렬 처리 |
| 메모리 관리 | 온칩 SRAM/Flash 직접 매핑 (**MMU** 부재) | **MMU** 기반 가상 메모리 페이징 및 프로세스 격리 |
| 주변장치 I/O | 온칩 아날로그/디지털 주변장치 원칩 내장 | 외장 고속 직렬 버스(PCIe, USB) 인터페이스 |
| 소비 전력 및 PMIC | 밀리와트(mW) 단위 초저전력, 단순 전원 레일 | 수 W ~ 수십 W 소비 전력, 다채널 PMIC 필수 |
| 운영체제 환경 | Bare-Metal 또는 경량 선점형 RTOS | 범용 OS(Linux, Android, Windows) |

#### 한줄 요약
- MCU는 모든 제어 자원을 단일 칩에 내장하고, MPU는 외부 메모리와 MMU를 결합하여 고성능을 낸다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **최악 실행 시간(Worst-Case Execution Time, WCET)**: 실시간 제어 태스크에서 인터럽트 및 연산이 가장 긴 지연 경로를 통과할 때 소요되는 최대 실행 시간.

</details>

```text
시스템 개발 요구사항 분석 (실시간성, 연산량, UI, 통신 복잡도)
      │
      ▼
마이크로초($\mu\text{s}$) 단위 하드 실시간성 및 WCET 확정보장이 필수적인가?
   ├── [예: 실시간 제어 필수]
   │      │
   │      ▼
   │   대형 디스플레이 GUI 및 범용 Rich OS가 동시에 필요한가?
   │      ├── [예: 복합 시스템] ─── 이종 하이브리드 SoC 채택 (MPU + MCU)
   │      └── [아니오: 단독 제어] ── MCU 단독 채택 (Bare-Metal / RTOS)
   │
   └── [아니오: 처리량 중심]
          │
          ▼
       범용 OS 및 기가헤르츠(GHz)급 연산이 필요한가?
          ├── [예: 고성능 시스템] ── MPU 채택 (외장 DDR 연동)
          └── [아니오: 단순 제어] ── MCU 단독 채택
```

분기 결과: 실시간 결정론은 MCU, Rich OS/GUI는 MPU, 인지와 제어 결합 시 이종 하이브리드 SoC 선정

#### 한줄 요약
- 실시간 결정론이 필요하면 MCU, Rich OS·GUI가 필요하면 MPU로 갈리고, 둘이 함께 필요할 때만 하이브리드 SoC의 통합 비용을 감수한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **베어메탈(Bare-Metal)**: 운영체제(OS) 커널 없이 하드웨어 레지스터를 C/어셈블리어로 직접 조작하는 메인 무한 루프 기반 펌웨어.

</details>

| 컴퓨팅 플랫폼 | 마이크로컨트롤러 (MCU) | 마이크로프로세서 (MPU) | 이종 하이브리드 SoC (MPU + MCU) |
|:---|:---|:---|:---|
| 핵심 프로세서 구조 | Cortex-M, RISC-V RV32 | Cortex-A, x86-64 | Cortex-A + Cortex-M 하이브리드 |
| 메모리 구성 | 온칩 Flash / SRAM 올인원 | 외장 DDR4/5 + eMMC | 온칩 SRAM + 외장 DDR 공유 메모리 |
| 시간적 결정론 | 마이크로초($\mu\text{s}$) 단위 결정론적 지연 | 스케줄링 지터 및 가변 지연 | MPU와 MCU 도메인 분리 |
| 주요 적용 분야 | 자동차 ECU, 모터 제어, IoT 센서 | 스마트폰, 차량용 IVI, 산업용 PC | 로보틱스, 자율주행 드론, 스마트 게이트웨이 |

#### 한줄 요약
- 단순 제어는 MCU, 고성능 멀티태스킹은 MPU, 인지와 정밀 제어가 결합된 로봇/드론은 이종 하이브리드 SoC를 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **스케줄링 지터(Scheduling Jitter)**: 범용 리눅스 OS의 선점 스케줄러와 메모리 페이징으로 인해 주기적 제어 루프의 시작 시각이 불규칙하게 흔들리는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| MPU 범용 리눅스 구동 시 **스케줄링 지터** 발생 | **실시간 제어 전담 MCU** 코어로 제어 로직 분리 | 제어 루프 결정론적 지연 보장 및 OS 부하 격리 |
| 고속 MPU와 외장 DDR 메모리 간 고주파 노이즈 | **임피던스 매칭** 및 등길이 배선 설계 | 신호 무결성(SI) 확보 및 메모리 에러 방지 |
| 제한된 MCU SRAM 환경에서 힙 동적 할당 메모리 고갈 | 동적할당 배제 및 **정적 메모리 풀** 적용 | 메모리 단편화 방지 및 무중단 안정성 확보 |

#### 한줄 요약
- 실무에서는 이종 코어로 지터를 격리하고, DDR 등길이 배선으로 신호를 보호하며, 정적 메모리 할당으로 MCU를 안정화한다.

## Ⅶ. 결론

- 시스템 요구사항에 따라 초저전력 하드 실시간 제어는 **MCU(Cortex-M/RISC-V)**, 고성능 멀티태스킹/Rich OS는 **MPU(Cortex-A/x86)**를 채택하는 것이 정석이며, 최근에는 로보틱스/자율주행의 인지-판단-제어 융합을 위해 단일 실리콘에 Cortex-A와 Cortex-M을 결합한 이종 멀티코어 SoC(Heterogeneous SoC)로 진화

#### 한줄 요약
- 프로세서 선정은 실시간 결정론, 전력 예산, 메모리 용량 및 OS 지원 여부를 종합 고려하여 결정해야 한다.
