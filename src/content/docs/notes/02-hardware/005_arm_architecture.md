---
sidebar:
  order: 5
  label: "005. ARM 프로세서 아키텍처•동작 모드 (ARM Architecture)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "ARM 프로세서 아키텍처•동작 모드 (ARM Architecture)"
date: "2026-08-13T11:29:07+09:00"
tags:
  - "notes-hardware"
weight: 5
extra:
  question_no: "005"
  source_status: "기출"
  source_history: "126회"
  priority: 50
  priority_note: "임베디드•모바일 설계 기반"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Arm 아키텍처(Arm Architecture)**: 저전력 로드·스토어 기반 RISC 구조에 다단계 예외 수준(Exception Level, EL) 권한 격리와 모듈형 벡터 명령 확장을 결합한 산업 표준 ISA.
- **명령어 집합 아키텍처(Instruction Set Architecture, ISA)**: 하드웨어가 실행하는 기계어 명령, 레지스터 구조, 메모리 모델 및 특권 모드를 정의하는 하드웨어-소프트웨어 인터페이스 사양.
- **실행 상태(Execution State)**: 프로세서 코어가 실행할 레지스터 비트 폭 및 기계어 명령어 포맷을 규정하는 동작 모드(AArch64 / AArch32).
- **예외 수준(Exception Level, EL)**: 보안성 및 가상화 지원을 위해 프로세서 권한을 EL0(User)부터 EL3(Secure Monitor)까지 4단계로 계층 격리한 보안 아키텍처.
- **선택 명령 확장(Optional Extension)**: 센서, AI, 그래픽, 신호 처리 등에 특화된 연산을 지원하기 위해 아키텍처에 추가 탑재 가능한 옵션 명령어 세트.

</details>

- 정의/개념: 저전력 RISC 로드·스토어 연산 구조와 4단계 예외 수준(EL0~EL3) 기반 권한 격리 및 다중 레지스터 execution state를 규정한 글로벌 표준 **Arm 아키텍처(Arm Architecture)**.
- 배경/필요성: 단일 특권 영역 구조에서는 사용자 앱의 보안 취약점이 OS 커널 및 하이퍼바이저 전체로 확산되므로, 모바일·클라우드 서버 요구에 맞춰 하드웨어 기반 계층 격리와 전력 효율성을 극대화하기 위해 탄생.

#### 한줄 요약
- Arm 아키텍처는 저전력 RISC 코어 기반의 AArch64/AArch32 Execution State와 4단계 Exception Level 권한 격리 체계를 제공함.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **로드·스토어 구조(Load/Store Architecture)**: 메모리 직접 연산을 금지하고 오직 LDR/STR 명령으로만 메모리에 접근하며 연산은 범용 레지스터 사이에서만 수행하는 특성.
- **코어 지식재산권(Core Intellectual Property, Core IP)**: 반도체 팹리스 업체에 즉시 제공되어 SoC 칩 합성에 사용 가능한 사전에 정밀 검증된 프로세서 블록.
- **마이크로아키텍처(Microarchitecture)**: 동일한 Armv9/v8 ISA 사양을 만족시키면서 Cortex-X, Cortex-A, Cortex-M 등 파이프라인과 캐시를 다르게 구성한 물리적 회로 설계.

</details>

- **로드·스토어 구조**를 채택하여 ALU 파이프라인 동작 시 메모리 접근 대기 지연을 우회하고 실행 효율 증대.
- **AArch64** 및 **AArch32**의 **실행 상태** 전환과 **예외 수준**을 결합하여 레가시 32비트 코드 호환과 64비트 하드웨어 권한 격리를 동시 달성.
- 칩 제조사에 ISA 규격 라이선스(Architecture License) 및 사전 완성된 **코어 IP(Core IP)** 형태를 이원화 공급하여 모바일/서버/임베디드 시장 대응.

#### 한줄 요약
- Load/Store RISC 구조 및 Execution State/EL 권한 격리를 기본으로 상용 Core IP 및 개별 아키텍처 라이선싱 모델을 제공함.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **AArch64**: A64 명령어 세트와 31개의 64비트 범용 레지스터(X0~X30)를 지원하는 64비트 실행 상태.
- **AArch32**: 기존 32비트 ARM(A32) 및 Thumb(T32) 명령어 세트를 구동하며 15개의 32비트 범용 레지스터(R0~R14)를 지원하는 호환 실행 상태.
- **고정 길이 SIMD 확장(Advanced SIMD, NEON)**: 128비트 벡터 레지스터를 통해 미디어 및 데이터 병렬 처리를 수행하는 128-bit 고정 SIMD 엔진.
- **확장 가능 벡터 확장(Scalable Vector Extension, SVE/SVE2)**: 하드웨어 구현에 따라 128비트부터 2048비트까지 가변 레지스터 폭을 지원하는 최신 벡터 연산 아키텍처.
- **레지스터 집합(Register Set)**: 연산 데이터를 고속 적재하는 범용 레지스터(X0~X30/R0~R14), 스택 포인터(SP), 링크 레지스터(LR), 프로그램 카운터(PC).
- **EL 격리(Exception Level Isolation)**: EL0(User App), EL1(OS Kernel), EL2(Hypervisor), EL3(Secure Monitor/TrustZone)로 하드웨어 실행 특권을 구분하는 체계.

</details>

```text
[ Arm Processor Architecture Hierarchy ]
┌───────────────────────────────────────────────────────────┐
│ Execution State : AArch64 (64-bit)  /  AArch32 (32-bit)   │
├───────────────────────────────────────────────────────────┤
│ Exception Levels (Hardware Privilege Isolation)           │
│  - EL0 : User Applications                                │
│  - EL1 : Operating System Kernel (Linux, Android, Windows)│
│  - EL2 : Hypervisor (KVM, Xen) / Virtualization           │
│  - EL3 : Secure Monitor (TrustZone, Firmware)             │
├───────────────────────────────────────────────────────────┤
│ Vector & Floating-Point Engines : NEON / SVE / SVE2       │
└───────────────────────────────────────────────────────────┘
```

| 구성요소 | 책임 |
|:---|:---|
| AArch64 | **64비트 레지스터•A64 명령** 실행 |
| AArch32 | **A32•T32 명령** 호환 실행 |
| 예외 수준 | **EL0~EL3** 권한•예외 격리 |
| NEON•SVE | **고정•가변 벡터 연산** 수행 |

#### 한줄 요약
- AArch64/AArch32 Execution State와 4단계 Exception Level(EL0~EL3) 및 NEON/SVE 벡터 엔진이 아키텍처 핵심을 구성함.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **프로세서 상태(Processor State, PSTATE)**: N, Z, C, V 조건 플래그, DAIF 인터럽트 마스크, 현재 EL 레벨 및 execution state 정보를 보관하는 CPU 상태 필드.
- **예외 링크 레지스터(Exception Link Register, ELR_ELx)**: 예외 처리 완료 후 원본 복귀를 위해 이전 프로그램 카운터(PC) 주소를 저장하는 특수 레지스터.
- **저장 프로그램 상태 레지스터(Saved Program Status Register, SPSR_ELx)**: 예외 진입 순간의 PSTATE 값을 백업 보관하는 레지스터.
- **벡터 기준 주소 레지스터(Vector Base Address Register, VBAR_ELx)**: 타깃 예외 수준(ELx)에 대응하는 예외 벡터 테이블의 베이스 주소를 지시하는 레지스터.
- **ELx 예외 처리기(Exception Handler)**: 해당 예외 수준에서 하드웨어 트랩, 시스템 콜(SVC, HVC, SMC), IRQ/FIQ 인터럽트를 처리하는 커널 루틴.
- **예외 복귀(Exception Return, ERET)**: SPSR_ELx 및 ELR_ELx에 복원 저장된 PSTATE 및 PC로 이전 실행 환경에 복귀하는 특권 명령어.

</details>

```text
[ 소프트웨어 실행 중 (EL0 User App) ]
                 │
                 ▼ System Call (SVC) / Interrupt (IRQ) 발생
[ Arm Core Hardware Trap ]
 1. PSTATE -> SPSR_EL1 저장
 2. PC 주소 -> ELR_EL1 저장
 3. VBAR_EL1 + Vector Offset 참조 ──> EL1 Exception Handler 진입
                 │
                 ▼
[ EL1 Kernel Exception Handler 실행 및 작업 처리 ]
                 │
                 ▼ ERET 명령어 실행
[ Arm Core Register Restore ]
 SPSR_EL1 -> PSTATE 복원, ELR_EL1 -> PC 복원 ──> [ 이전 EL0 앱 실행 재개 ]
```

### 동작 원리

1. **상태 저장**: EL0에서 예외(SVC, IRQ 등) 발생 시 코어 하드웨어가 현재 **PSTATE**와 복귀 PC 주소를 타깃 수준의 레지스터인 **SPSR_ELx** 및 **ELR_ELx**에 자동 백업함.
2. **벡터 오프셋 분기**: 해당 EL의 **VBAR_ELx** 레지스터에 기록된 베이스 주소에 예외 종별 오프셋을 가산하여 예외 벡터 테이블 주소를 결정함.
3. **예외 처리**: 지정된 **ELx 예외 처리기(Exception Handler)** 로 점프하여 커널 서비스 및 인터럽트 처리를 완성함.
4. **상태 복원**: 처리 완료 후 **ERET** 명령을 실행하여 SPSR_ELx와 ELR_ELx의 값을 PSTATE 및 PC로 복원하고 이전 실행 흐름으로 복귀함.

#### 한줄 요약
- 예외 발생 시 PSTATE/PC를 SPSR_ELx/ELR_ELx에 백업하고 VBAR_ELx 트랩 후 ERET을 통해 원복하는 하드웨어 제어 흐름으로 작동함.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **시스템 온 칩(System on Chip, SoC)**: CPU 코어, GPU, NPU, 메모리 컨트롤러, 통신 모듈을 하나의 미세 반도체 다이에 집적한 시스템.
- **x86-64**: CISC 아키텍처 기반의 64비트 범용 PC 및 서버 표준 ISA (Intel / AMD).
- **레거시 부담(Legacy Overhead)**: decades 동안 누적된 가변 길이 복합 기계어 및 하위 16/32비트 억세스 모드를 완벽 지원하기 위한 하드웨어 복잡성.
- **응용 프로그램 이진 인터페이스(Application Binary Interface, ABI)**: C/C++ 컴파일러가 생성하는 레지스터 할당, 함수 호출 규약, 파라미터 전달 규격.
- **가변 길이 명령•호환 모드(Variable-Length Instruction & Compatibility Mode)**: x86-64에서 1~15바이트 가변 비트를 복합 해석하여 하위 호환성을 유지하는 방식.
- **재빌드•변환(Rebuild & Translation)**: x86 바이너리를 Arm 시스템에서 실행하기 위해 타깃 컴파일 재빌드 또는 동적 바이너리 번역(Rosetta 2 등)을 수행하는 작업.

</details>

| 비교 항목 | Arm Architecture (v8 / v9) | x86-64 Architecture (AMD64 / EM64T) |
|:---|:---|:---|
| **아키텍처 성격** | 고효율 **로드·스토어 구조** RISC | 가변 길이 복합 디코딩 기반 CISC |
| **권한 및 모드** | **EL0~EL3** 계층 체계 및 AArch64/32 | Ring 0~3 레벨 및 Real/Protected/Long Mode |
| **전력 및 집적성** | **SoC 통합•전력 제약** 중심 생태계 | 고성능 PC•서버와 기존 플랫폼 중심 생태계 |
| **소프트웨어 호환** | x86 타깃 바이너리의 **재빌드·변환** 수반 | 수십 년간 누적된 데스크톱/서버 바이너리 직구동 |
| **디코딩 오버헤드** | 정형 32-bit 인코딩으로 프런트엔드 간소 | 가변 인코딩 해석을 위한 상당한 **레거시 부담** |

#### 한줄 요약
- Arm은 SoC 저전력 효율성과 정형 인코딩 디코딩에 강점을 가지며, x86-64는 Legacy x86 Binary 구동 호환성에 강점이 있음.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **네이티브 라이브러리(Native Library)**: C/C++ 등으로 작성되어 x86/Arm 특정 타깃 기계어로 직접 컴파일된 shared library (.so, .dll).
- **런타임 기능 탐지(Runtime Feature Detection)**: 소스코드 실행 중 `getauxval()` 또는 system register 조회를 통해 NEON, SVE, SVE2 지원을 판별하는 기술.
- **최소 권한(Least Privilege)**: 보안 위험 관리를 위해 응용 프로그램은 EL0, 커널은 EL1, 가상화는 EL2로 격리 운영하는 원칙.
- **대체 코드(Fallback Code)**: 최신 SVE2 벡터 명령을 미지원하는 구형 Arm 코어 장비를 위해 마련된 일반 C/NEON 표준 코드 블록.
- **SoC 벤치마크(SoC Benchmark)**: 목표 장비의 초당 전력 소모량(W) 및 SPEC CPU, CoreMark 성능 지수를 실측 평가하는 툴.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| x86 중심 C/C++ **네이티브 라이브러리**를 Arm 인프라로 이전 시 호환성 충돌 | 타깃 Arm **AArch64 ABI** 빌드 체계 구축 및 동적 바이너리 변환(Rosetta 2/Box64) 적용 | 이종 인프라 마이그레이션 오류 제거 및 네이티브 성능 확보 |
| 불필요하게 커널/보안 권한(EL1/EL3)을 점유하여 시스템 안정성 훼손 | **최소 권한** 원칙 준수 및 EL 레벨 간 HVC/SMC 인터페이스 정밀 통제 | 하드웨어 기반 사이드채널 공격 및 보안 침입 파급력 차단 |
| SVE/SVE2 벡터 명령 사용 시 특정 구형 Arm 코어 단말에서 실행 crash | **런타임 기능 탐지** 적용 및 **대체 코드** 제공 | 단말 코어 세대 격차에 관계없이 범용 실행 안정성 보장 |
| 모바일/클라우드 부하 폭증 시 서버 스로틀링 및 전력 초과 발열 발생 | **SoC 벤치마크** 기반 전력 대 성능비(Perf/Watt) 모니터링 및 DVFS 제어 | 전력 캡 내 최고 연산 처리율 유지 및 발열 장애 방지 |

#### 한줄 요약
- AArch64 Native Build, Exception Level 최소 권한 부여, SVE Runtime Feature Detection 및 SoC Power Benchmark 체계를 적용함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **전력 효율(Power Efficiency)**: 연산 단위당 소모되는 주울(Joule) 및 와트(Watt) 전력 소비 비율.
- **네이티브 라이브러리 재빌드(Native Library Rebuild)**: 소스 코드를 타깃 Arm AArch64 크로스 컴파일러로 재빌드하는 인프라 현대화 작업.
- **ISA 선택 기준(ISA Selection Criteria)**: 대상 제품군(스마트폰, IoT, 클라우드 hyperscaler 등)의 전력 제약과 컴퓨팅 요구 성능을 산정하는 판단 표준.

</details>

- 전력•SoC 통합이 우선이고 재빌드가 가능하면 **Arm**, x86 바이너리 직결이 우선이면 **x86 유지**.

#### 한줄 요약
- 전력•통합성과 바이너리 호환성을 기준으로 Arm 전환 여부를 결정함.
