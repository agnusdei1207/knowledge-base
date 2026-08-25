---
sidebar:
  order: 83
  label: "083. 마이크로컨트롤러 vs 마이크로프로세서"
  badge:
    text: "미출 · 50%"
    variant: note
title: "마이크로컨트롤러 vs 마이크로프로세서 (Microcontroller vs Microprocessor)"
date: "2026-08-25T10:25:00+09:00"
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

- **MCU(Microcontroller Unit)**: CPU 코어와 함께 RAM, Flash ROM, 타이머, ADC 및 GPIO를 단일 실리콘 다이에 통합한 올인원 제어용 반도체.
- **MPU(Microprocessor Unit)**: 고성능 CPU 코어 중심의 연산 장치로 외부 DRAM, 스토리지 및 MMU를 결합하여 범용 OS를 구동하는 고성능 프로세서.

</details>

- 정의/개념: 메모리·주변장치를 원칩 집적한 **MCU**와 외부 고속 메모리 및 MMU 기반 고성능 OS를 구동하는 **MPU**
- 배경/필요성: 단일 컴퓨팅 구조로는 **초저전력 결정론적 실시간 제어와 대규모 고성능 연산 동시 만족 불가**

#### 한줄 요약
- 실시간성과 저전력 제어에는 온칩 올인원 MCU가, 고성능 연산과 Rich OS 구동에는 확장형 MPU가 쓰인다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **결정론적 지연(Deterministic Latency)**: 인터럽트 발생 시 처리 개시까지의 지연시간 편차가 극도로 작아 마이크로초 단위로 타이밍을 보장하는 특성.
- **MMU(Memory Management Unit)**: 가상 메모리 주소를 물리 주소로 변환하고 프로세스 간 메모리 보호를 수행하여 Linux 등 범용 OS를 구동하는 하드웨어.

</details>

- MCU: 단일 칩 내부에 SRAM, Flash, ADC/PWM을 집적하여 **결정론적 지연** 및 초저전력 동작
- MPU: 기가헤르츠(GHz) 클록, 다단계 캐시, **MMU** 탑재로 Linux/Android 등 범용 OS 지원
- 이종 통합: 최근 단일 SoC 내부에 MPU 코어와 MCU 코어를 결합한 하이브리드 아키텍처 확산

#### 한줄 요약
- 하드웨어 집적도와 MMU 유무에 따라 실시간 제어(MCU)와 고성능 멀티태스킹(MPU)으로 역할이 갈린다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **온칩 주변장치(On-Chip Peripherals)**: MCU 칩 내부에 내장된 아날로그-디지털 변환기(ADC), PWM 발생기, 타이머, 통신 컨트롤러.

</details>

```text
[MCU vs MPU 하드웨어 아키텍처 비교]
|-- MCU (원칩 올인원 구조)
|   |-- 경량 코어 (Cortex-M / RISC-V)
|   |-- 온칩 메모리 (Flash 코드 롬 + SRAM)
|   `-- 온칩 주변장치 (ADC·PWM·타이머·CAN·GPIO)
`-- MPU (외부 확장 고성능 구조)
    |-- 고성능 멀티코어 (Cortex-A / x86-64 + MMU + L1~L3 캐시)
    |-- 고속 메모리 인터페이스 (DDR4/5, LPDDR5 컨트롤러)
    `-- 외부 스토리지 및 버스 (eMMC/UFS, PCIe, 고속 USB)
```

선의 의미: 계층 및 하드웨어 구성 비교

| 구성요소 | MCU (Microcontroller) 책임 | MPU (Microprocessor) 책임 |
|:---|:---|:---|
| 연산 코어 | 수십~수백 MHz 경량 코어로 확정적 명령어 실행 | 수 GHz 고성능 멀티코어로 복잡한 연산 및 스레드 병렬 처리 |
| 메모리 관리 | 온칩 SRAM/Flash 직접 매핑 (MPU 메모리 보호) | **MMU** 기반 가상 메모리 페이징 및 프로세스 격리 |
| I/O 인터페이스 | **온칩 아날로그/디지털 주변장치** 직결 제어 | 고속 직렬 버스(PCIe, USB3, MIPI) 및 외부 확장 인터페이스 |
| 전원 및 패키징 | mW 단위 초저전력 및 단순 전원 레일 | 수W~수십W 전력 소모 및 복잡한 PMIC 전원 공급 |

#### 한줄 요약
- MCU는 모든 자원을 단일 칩에 내장하며, MPU는 외부 메모리와 스토리지를 결합하여 고성능을 낸다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **최악 실행 시간(WCET)**: 실시간 제어 루프에서 인터럽트 및 작업이 가장 긴 지연 경로를 통과할 때 소요되는 최대 시간.

</details>

```text
임베디드 제어 요구사항 분석
        │
   마이크로초 단위 하드 실시간 및 WCET 보장이 필수적인가?
   ┌────┴─────┐
  예           아니오
   │             │
Linux/Android   Linux/Windows 등 범용 OS 및 대규모 GUI가 필요한가?
등 Rich OS가     ┌──┴───┐
필요한가?        아니오     예
 ┌──┴───┐         │        │
 예     아니오    MCU 채택  MPU 채택 (외부 DDR 장착)
 │       │
MPU+MCU  MCU 단독
이종 SoC  채택
(하이브리드)
```

#### 한줄 요약
- 실시간 결정론 필요성 → Rich OS/GUI 요구 여부 판정 → MCU, MPU 또는 이종 SoC 결정을 순차 진행한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **베어메탈(Bare-Metal)**: 운영체제 없이 메인 루프와 인터럽트 서비스 루틴(ISR)만으로 하드웨어를 직접 제어하는 구조.

</details>

| 프로세서 아키텍처 | 마이크로컨트롤러 (MCU) | 마이크로프로세서 (MPU) | 이종 하이브리드 SoC (MPU+MCU) |
|:---|:---|:---|:---|
| 메모리 구성 | 온칩 Flash / SRAM 올인원 | 외부 기가바이트급 DDR / eMMC | 온칩 SRAM + 외부 DDR 공유 |
| 구동 소프트웨어 | **베어메탈** 또는 경량 RTOS (FreeRTOS) | Rich OS (Embedded Linux, Android) | Linux (MPU 코어) + RTOS (MCU 코어) |
| 시간 결정론 | 나노/마이크로초 단위 확정적 지연 | 스케줄링 지터 및 비결정적 지연 | 두 영역 간 IPC로 결정론적 제어 분리 |
| 주요 응용처 | 자동차 ECU, 가전제품, 모터 제어 | 스마트폰, 차량용 IVI, 산업용 PC | 로보틱스, 드론, 스마트 게이트웨이 |

#### 한줄 요약
- 단순 제어는 MCU, 고성능 멀티태스킹은 MPU, 인지-제어가 결합된 로봇은 이종 SoC를 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **스케줄링 지터(Scheduling Jitter)**: 범용 OS의 선점형 스케줄러와 캐시 미스로 인해 제어 루프 주기가 불규칙하게 흔들리는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| MPU 범용 OS 구동 시 **스케줄링 지터**로 모터 탈조 | 실시간 제어 전담 보조 MCU 분리 또는 이종 SoC 채택 | 제어 루프 결정론적 지연 보장 및 OS 부하 격리 |
| 고속 MPU와 외부 DDR 간 PCB 고주파 노이즈 | 특성 임피던스 매칭 및 등길이 배선(Length Matching) | 신호 무결성(SI) 확보 및 메모리 비트 에러 방지 |
| 제한된 MCU SRAM 환경에서 스택 오버플로우 | 동적 할당(malloc) 배제 및 정적 메모리 풀/워터마크 감시 | 런타임 메모리 고갈 원천 차단 및 시스템 안정성 유지 |
| 배터리 구동 단말의 전력 소모 급증 | 딥슬립 모드 및 인터럽트 웨이크업 기반 전력 관리 | 대기 전력 $\mu\text{A}$ 단위 절감 및 배터리 수명 연장 |

#### 한줄 요약
- 이종 SoC로 실시간 지터를 격리하고, DDR 등길이 배선과 정적 메모리 할당으로 신뢰성을 보장한다.

## Ⅶ. 결론

- 초저전력 실시간 제어는 **MCU(Cortex-M)**, 대규모 연산 및 GUI는 **MPU(Cortex-A)**를 선정하고, 복합 시스템은 **이종 하이브리드 SoC** 아키텍처 채택

#### 한줄 요약
- 프로세서 선정은 실시간 결정론, 전력 예산, 메모리 용량 및 OS 지원 여부를 종합 고려하여 결정해야 한다.