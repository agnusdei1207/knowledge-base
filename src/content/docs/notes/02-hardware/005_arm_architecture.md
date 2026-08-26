---
sidebar:
  order: 5
  label: "005. ARM 프로세서 아키텍처•동작 모드 (ARM Architecture)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "ARM 프로세서 아키텍처•동작 모드 (ARM Architecture)"
date: "2026-08-26T10:45:00+09:00"
tags:
  - "notes-hardware"
weight: 5
extra:
  question_no: "005"
  source_status: "기출"
  source_history: "126회"
  priority: 50
  priority_note: "Arm 프로파일과 예외 수준"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Arm 아키텍처(Arm Architecture)**: 고효율 로드·스토어(Load-Store) 기반 RISC 아키텍처로, 응용 시장별 특화 프로파일(A/R/M)과 계층화된 예외 수준(EL0~EL3)을 제공하는 프로세서 표준.
- **프로파일(Profile)**: 범용 연산(A-Profile), 실시간 제어(R-Profile), 마이크로컨트롤러(M-Profile) 등 도메인별 하드웨어 기능과 메모리 시스템을 특화한 Arm 아키텍처 분류 체계.
- **실행 상태(Execution State)**: 64비트 레지스터 및 가상 주소 공간을 사용하는 AArch64와 32비트 레거시 호환을 지원하는 AArch32 동작 모드.

</details>

- 정의/개념: 로드·스토어 기반 RISC 구조를 바탕으로 응용 분야별 특화 프로파일(A/R/M)과 하드웨어 권한 격리 계층(EL0~EL3)을 제공하는 **Arm 프로세서 아키텍처**
- 배경/필요성: 단일 프로세서 구조의 한계로 인한 **도메인별 전력·성능·실시간성 상충** 극복

#### 한줄 요약
- Arm은 고효율 RISC 코어를 기반으로 A(애플리케이션), R(실시간), M(마이크로컨트롤러) 3대 프로파일과 EL0~EL3 권한 계층을 제공하여 전 영역을 커버한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **예외 수준(Exception Level, EL)**: EL0(사용자 애플리케이션), EL1(OS 커널), EL2(하이퍼바이저 가상화), EL3(보안 펌웨어/시큐어 모니터)로 실행 특권을 계층화한 Armv8/v9 권한 모델.
- **TrustZone**: 단일 물리 CPU 코어와 시스템 버스를 하드웨어 수준에서 일반 영역(Normal World)과 보안 영역(Secure World)으로 완전 격리하는 Arm 보안 기술.
- **SIMD/벡터 확장**: 128비트 미디어 가속(NEON) 및 가변 벡터 길이 기반 머신러닝·HPC 가속(SVE/SVE2)을 지원하는 데이터 병렬 처리 확장.

</details>

- 엄격한 로드/스토어 원칙: 메모리 접근을 전용 명령어로만 한정하여 코어 데이터패스 및 **파이프라인 구조** 단순화
- 4단계 특권 격리: EL0부터 EL3까지 독립된 **예외 수준**을 두어 OS, 가상화 하이퍼바이저, 보안 펌웨어 간의 상호 간섭 원천 차단
- 하드웨어 보안 격리: **TrustZone**을 통해 코어, 메모리, 인터럽트(GIC)를 일반 영역과 보안 영역으로 2차원 분리

#### 한줄 요약
- Arm은 명확한 로드/스토어 원칙으로 하드웨어 효율을 높이고, EL0~EL3 권한 모델과 TrustZone으로 시스템 안전성과 가상화 보안을 확립한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **A-profile(Application Profile)**: 가상 메모리(MMU)와 대용량 캐시, 멀티코어 및 하이퍼바이저 가상화를 지원하는 고성능 컴퓨팅용 프로파일(Cortex-A).
- **R-profile(Real-Time Profile)**: MPU(메모리 보호 장치) 기반으로 결정론적(Deterministic) 초저지연 인터럽트 응답을 보장하는 자동차·통신 제어용 프로파일(Cortex-R).
- **M-profile(Microcontroller Profile)**: 하드웨어 인터럽트 컨트롤러(NVIC)와 결합하여 초저전력 및 빠른 웨이크업에 최적화된 임베디드용 프로파일(Cortex-M).

</details>

```text
Armv8/v9 프로세서 아키텍처
├── 프로파일 분류 체계 (Cortex-A/R/M)
├── 실행 상태 (AArch64, AArch32)
├── 권한 모델 (EL0 User, EL1 OS, EL2 Hypervisor, EL3 Secure Monitor)
└── 하드웨어 보안 및 확장 (TrustZone, NEON/SVE2)
```

선의 의미: 가지(`├──`, `└──`)는 Arm 아키텍처의 프로파일, 실행 상태 및 권한 계층을 나타냄

| 구성요소 | 계층 및 영역 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|:---|
| A-Profile | 고성능 애플리케이션 | MMU 기반 가상 메모리 및 멀티코어 가상화(EL2) 지원 | 범용 OS(Linux, Android, Windows) 구동 |
| R-Profile | 실시간 임베디드 | MPU 기반 메모리 보호 및 결정론적 인터럽트 타이밍 보장 | ASIL-D 차량용 제어, 5G 모뎀 기저대역 |
| M-Profile | 초저전력 제어기 | NVIC 하드웨어 인터럽트 스케줄링 및 초저지연 웨이크업 | 센서 노드, 소형 MCU, IoT 기기 |
| 예외 수준 (EL) | 소프트웨어 권한 계층 | 시스템 호출, 폴트, 가상화 트랩 처리 및 컨텍스트 격리 | 하위 EL은 상위 EL 메모리 직접 접근 불가 |
| TrustZone | 시스템 보안 아키텍처 | 버스 마스터 및 메모리의 보안 비트 기반 하드웨어 격리 | 보안 키, 금융 인증, DRM 독립 보호 |

#### 한줄 요약
- Arm 아키텍처는 용도별 3대 프로파일과 4단계 EL 권한 계층, 그리고 TrustZone 하드웨어 격리를 통해 칩 설계의 유연성과 강력한 보안을 제공한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **예외 복귀 레지스터(ELR_ELx / SPSR_ELx)**: 예외 발생 시 복귀할 프로그램 주소(ELR)와 이전 프로세서 상태(SPSR)를 상위 EL 하드웨어가 자동으로 백업하는 특수 레지스터.
- **ERET(Exception Return)**: 상위 EL에서 예외 처리를 완료한 후 SPSR과 ELR을 원자적으로 복원하여 하위 EL의 이전 실행 지점으로 복귀하는 명령어.

</details>

```text
EL0 (사용자 앱) 실행 중 예외(SVC/인터럽트) 발생
                      │
                      ▼
1. 하드웨어 상태 백업 및 권한 승격 (SPSR_EL1, ELR_EL1 저장 ➔ EL1 전환)
                      │
                      ▼
2. 벡터 테이블(VBAR_EL1) 진입 및 예외 핸들러 실행
                      │
                      ▼
3. 서비스 완료 및 ERET 명령어 실행 (SPSR/ELR 상태 복원)
                      │
                      ▼
4. EL0 (사용자 앱) 복귀 및 다음 명령어 실행 재개
```

분기 결과: **동일 EL 처리**는 레지스터 백업 없이 즉시 실행되나, **상위 EL 승격**은 SPSR/ELR 하드웨어 백업을 거치며, **EL3 트랩**은 TrustZone 보안 세계 전환이 수반됨

#### 한줄 요약
- 예외 발생 시 하드웨어가 현재 상태와 복귀 주소를 상위 EL 레지스터(SPSR/ELR)에 자동 백업하고, 처리가 끝나면 ERET 명령어로 안전하게 복귀한다.

## Ⅴ. 종류 및 비교

| 비교 항목 | A-Profile (Cortex-A) | R-Profile (Cortex-R) | M-Profile (Cortex-M) |
|:---|:---|:---|:---|
| 주요 적용 분야 | 스마트폰, 서버, PC, 고성능 SoC | 차량 파워트레인/ADAS, 산업 로봇, 5G 모뎀 | 가전 MCU, 센서 허브, 웨어러블 IoT |
| 메모리 관리 장치 | **가상 메모리 MMU** 지원 | **물리 메모리 MPU** 지원 | 선택적 **MPU** 지원 |
| 실시간 결정성 | 비결정론적 지연 | **결정론적 응답** 보장 | **초저지연 인터럽트** 지원 |
| 가상화(EL2) 지원 | 하이퍼바이저 하드웨어 가상화 완벽 지원 | 실시간 가상화(EL2) 선택적 지원 | 미지원 (단순 권한 모드만 제공) |
| 운영체제 | Linux, Android, iOS, Windows, QNX | RTOS (FreeRTOS, AUTOSAR, Zephyr) | 베어메탈, 경량 RTOS |

#### 한줄 요약
- 범용 OS와 가상화가 필수면 A-Profile, 엄격한 실시간 응답 보장이면 R-Profile, 배터리 기반 초저전력 제어면 M-Profile을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **밀결합 메모리(Tightly Coupled Memory, TCM)**: R/M-Profile 코어 내부에 위치하여 캐시 미스 없이 1클록 내 확정적 접근 시간을 보장하는 고속 전용 SRAM.
- **인터럽트 지연시간(Interrupt Latency)**: 외부 하드웨어 인터럽트 신호 발생 시점부터 ISR의 첫 번째 명령어가 실행되기까지 소요되는 사이클 수.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| A-Profile 가상 메모리 페이징 및 캐시 미스로 인한 실시간성 훼손 | **R-Profile 코어** 및 **TCM** 적용 | 지터(Jitter) 없는 마이크로초 단위 결정론적 응답 보장 |
| Normal World의 취약점이 보안 자산(암호키 등)으로 전파될 위험 | **TrustZone** 및 **EL3 시큐어 모니터** 적용 | OS가 탈취되어도 보안 영역 내 핵심 자산 완벽 방어 |
| 다양한 프로세서 코어 간 이기종 멀티프로세싱 시 통신 오버헤드 | **DynamIQ** 및 **CCI** 적용 | Cortex-A와 Cortex-R/M 간 하드웨어 캐시 일관성 유지 |

#### 한줄 요약
- 실무 SoC 설계에서는 A-Profile(범용 UI/연산)과 R/M-Profile(실시간/보안 제어)을 TrustZone 및 캐시 인터커넥트로 통합하는 이종 아키텍처를 구성한다.

## Ⅶ. 결론

- 응용 도메인 요구에 따른 **A/R/M 프로파일** 선정 및 **TrustZone** 격리

#### 한줄 요약
- Arm은 A/R/M 3대 프로파일을 통해 임베디드부터 슈퍼컴퓨팅까지 포괄하며, EL 권한 모델과 TrustZone이 엔터프라이즈급 신뢰성을 완성한다.
