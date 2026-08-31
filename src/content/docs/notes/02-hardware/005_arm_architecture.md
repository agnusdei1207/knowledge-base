---
sidebar:
  order: 5
  label: "005. ARM 프로세서 아키텍처•동작 모드 (ARM Architecture)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "ARM 프로세서 아키텍처•동작 모드 (ARM Architecture)"
date: "2026-08-31T09:55:00+09:00"
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

- **Arm 아키텍처(Arm Architecture)**: 로드·스토어 기반 ISA와 용도별 A/R/M 프로파일을 제공하는 프로세서 표준.
- **프로파일(Profile)**: 범용 연산(A-Profile), 실시간 제어(R-Profile), 마이크로컨트롤러(M-Profile) 등 도메인별 하드웨어 기능과 메모리 시스템을 특화한 Arm 아키텍처 분류 체계.
- **실행 상태(Execution State)**: 64비트 레지스터 및 가상 주소 공간을 사용하는 AArch64와 32비트 레거시 호환을 지원하는 AArch32 동작 모드.

</details>

- 정의/개념: 로드·스토어 기반 RISC 구조를 바탕으로 응용 분야별 특화 프로파일(A/R/M)과 하드웨어 권한 격리 계층(EL0~EL3)을 제공하는 **Arm 프로세서 아키텍처**
- 배경/필요성: 단일 아키텍처 규격으로는 모바일 고성능 연산, 차량·산업용 실시간 제어, 초저전력 IoT 마이크로컨트롤러의 상충되는 하드웨어 요구조건 충족 불가

#### 한줄 요약
- Arm은 고효율 RISC 코어를 기반으로 A(애플리케이션), R(실시간), M(마이크로컨트롤러) 3대 프로파일과 EL0~EL3 권한 계층을 제공하여 전 영역을 커버한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **예외 수준(Exception Level, EL)**: A-profile에서 EL0~EL3로 애플리케이션·운영체제·하이퍼바이저·보안 펌웨어 권한을 구분하는 모델.
- **TrustZone**: 시스템 자원을 일반 영역과 보안 영역으로 구분하고 접근을 통제하는 Arm 보안 기술.
- **SIMD/벡터 확장**: 128비트 미디어 가속(NEON) 및 가변 벡터 길이 기반 머신러닝·HPC 가속(SVE/SVE2)을 지원하는 데이터 병렬 처리 확장.

</details>

- 엄격한 로드/스토어 원칙: 메모리 접근을 전용 명령어로만 한정하여 코어 데이터패스 및 **파이프라인 구조** 단순화
- A-profile 특권 격리: EL0~EL3 **예외 수준**으로 운영체제·가상화·보안 펌웨어 권한 분리
- 하드웨어 보안 격리: **TrustZone**을 통해 코어, 메모리, 인터럽트(GIC)를 일반 영역과 보안 영역으로 2차원 분리

#### 한줄 요약
- Arm은 명확한 로드/스토어 원칙으로 하드웨어 효율을 높이고, EL0~EL3 권한 모델과 TrustZone으로 시스템 안전성과 가상화 보안을 확립한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **A-profile(Application Profile)**: 가상 메모리(MMU)와 대용량 캐시, 멀티코어 및 하이퍼바이저 가상화를 지원하는 고성능 컴퓨팅용 프로파일(Cortex-A).
- **R-profile(Real-Time Profile)**: MPU·TCM으로 예측 가능한 지연을 지원하는 자동차·통신 제어용 프로파일(Cortex-R).
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

| 구성요소 | 책임 |
|:---|:---|
| A-Profile | **MMU** 기반 가상 메모리와 EL2 가상화 지원 |
| R-Profile | **MPU·TCM** 기반 결정론적 응답 보장 |
| M-Profile | **NVIC** 기반 저지연 인터럽트와 저전력 제어 |
| 예외 수준(EL) | 시스템 호출·트랩과 **권한 계층** 격리 |
| TrustZone | 메모리·버스의 **보안 영역** 하드웨어 분리 |

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
EL0 사용자 앱 복귀 및 다음 명령어 실행 재개
```

분기 결과: **예외 유형**과 현재 EL에 따라 진입할 벡터 엔트리와 목표 **예외 수준**이 갈리지만, 어느 갈래든 SPSR·ELR 저장과 ERET 복원이라는 고정 비용은 예외마다 동일하게 지불됨

**동작 원리**

1. **하드웨어 상태 백업 및 권한 승격**: PSTATE와 복귀 주소를 SPSR_EL1·ELR_EL1에 저장
2. **벡터 테이블 진입 및 예외 핸들러 실행**: VBAR_EL1 기준 엔트리로 제어 전환
3. **서비스 완료 및 ERET 명령어 실행**: 저장 상태와 PC를 복원해 하위 EL로 복귀

#### 한줄 요약
- 예외 발생 시 하드웨어가 현재 상태와 복귀 주소를 상위 EL 레지스터(SPSR/ELR)에 자동 백업하고, 처리가 끝나면 ERET 명령어로 안전하게 복귀한다.

## Ⅴ. 종류 및 비교

| Arm 프로파일 | A-Profile (Cortex-A) | R-Profile (Cortex-R) | M-Profile (Cortex-M) |
|:---|:---|:---|:---|
| 주요 적용 분야 | 스마트폰, 서버, PC, 고성능 SoC | 차량 파워트레인/ADAS, 산업 로봇, 5G 모뎀 | 가전 MCU, 센서 허브, 웨어러블 IoT |
| 메모리 관리 장치 | **가상 메모리 MMU** 지원 | **물리 메모리 MPU** 지원 | 선택적 **MPU** 지원 |
| 실시간 결정성 | 캐시·가상 메모리로 지연 변동 | **예측 가능한 응답** 지원 | **저지연 인터럽트** 지원 |
| 가상화 지원 | 하드웨어 가상화 지원 | 구현 세대에 따라 지원 | 비가상화 제어 중심 |
| 운영체제 | Linux, Android, iOS, Windows, QNX | RTOS (FreeRTOS, AUTOSAR, Zephyr) | 베어메탈, 경량 RTOS |

#### 한줄 요약
- 범용 OS와 가상화가 필수면 A-Profile, 엄격한 실시간 응답 보장이면 R-Profile, 배터리 기반 초저전력 제어면 M-Profile을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **밀결합 메모리(Tightly Coupled Memory, TCM)**: R/M-profile에서 캐시를 우회해 예측 가능한 접근 시간을 제공하는 전용 SRAM.
- **인터럽트 지연시간(Interrupt Latency)**: 외부 하드웨어 인터럽트 신호 발생 시점부터 ISR의 첫 번째 명령어가 실행되기까지 소요되는 사이클 수.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| A-profile의 캐시·가상 메모리로 응답 지연 변동 | **R-profile** 및 **TCM** 적용 | 메모리 접근 지연의 예측 가능성 향상 |
| 일반 영역 취약점이 보안 자산 접근으로 확산 | **TrustZone** 및 보안 모니터 적용 | 보안 영역의 접근 경계 분리 |
| A/R/M 코어 간 공유 메모리 통신 오버헤드 | 공유 버퍼·메일박스와 명시적 동기화 | 이종 코어 간 데이터 전달 일관성 확보 |

#### 한줄 요약
- 실무 SoC 설계에서는 A-Profile(범용 UI/연산)과 R/M-Profile(실시간/보안 제어)을 TrustZone 및 캐시 인터커넥트로 통합하는 이종 아키텍처를 구성한다.

## Ⅶ. 결론

- 모바일 시장의 지배적 표준을 넘어 **클라우드 데이터센터(Neoverse) 및 차량용 반도체(Armv9)**로 확산 중이며, 향후 **기밀 컴퓨팅(CCA) 및 AI 벡터 가속(SVE2)**을 중심으로 아키텍처 영향력 지속 확대 전망

#### 한줄 요약
- Arm은 A/R/M 3대 프로파일을 통해 임베디드부터 슈퍼컴퓨팅까지 포괄하며, EL 권한 모델과 TrustZone이 엔터프라이즈급 신뢰성을 완성한다.
