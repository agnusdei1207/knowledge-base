---
sidebar:
  order: 128
  label: "128. ARM TrustZone 하드웨어 보안"
  badge:
    text: "기출 · 50%"
    variant: note
title: "하드웨어 기반 시스템 공간 격리 및 TEE : ARM TrustZone (GlobalPlatform TEE & ARMv8-A)"
date: "2026-09-07T14:00:00+09:00"
tags:
  - "notes-security"
weight: 128
extra:
  question_no: "128"
  source_status: "기출"
  source_history: "119회, 126회, 131회"
  priority: 50
  priority_note: "119•126•131회 반복 기출, ARM TrustZone 하드웨어 보안 아키텍처, 일반 세계(Normal World / REE) vs 보안 세계(Secure World / TEE), AXI 시스템 버스 NS(Non-Secure) 비트 제어, EL3 보안 모니터(Secure Monitor / SMC), TZASC(메모리 제어기) 및 TZPC(주변장치 제어기), GlobalPlatform TEE 표준"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **ARM TrustZone (ARM TrustZone TEE / GlobalPlatform TEE)**: 단일 물리적 프로세서 코어, 시스템 버스(AXI), 메모리 및 주변장치를 하드웨어 수준에서 일반 세계(Normal World / REE: Rich Execution Environment)와 보안 세계(Secure World / TEE: Trusted Execution Environment)로 시분할·공간 격리하여, 범용 OS가 장악되더라도 금융 결제, 생체 인증, DRM 암호화 키를 안전하게 보호하는 시스템 보안 하드웨어 아키텍처.
- **범용 OS 커널 권한 탈취 시 전면 침해 결함(Rich OS Kernel Compromise Defect)**: 안드로이드나 리눅스 등 수천만 줄의 방대한 코드베이스를 가진 범용 OS는 커널 취약점으로 인해 루트(Root) 권한이 탈취될 위험이 항상 존재하며, 소프트웨어 기반 격리만 사용할 경우 커널을 장악한 공격자가 메모리 내의 마스터 암호키와 지문/얼굴 생체 데이터를 평문으로 유출하는 구조적 결함.

</details>

- 정의/개념: 단일 하드웨어 자원을 효율적으로 활용하기 위해 **AXI 버스 NS(Non-Secure) 비트 태깅 $\rightarrow$ EL3 보안 모니터(Secure Monitor / SMC 호출) $\rightarrow$ TZASC(메모리 주소 제어) 및 TZPC(주변장치 제어) $\rightarrow$ 보안 마이크로커널(Secure OS / OP-TEE) 구동 $\rightarrow$ 신뢰 애플리케이션(TA) 암호 연산** 을 집행하는 **하드웨어 기반 시스템 격리 아키텍처**
- 배경/필요성: 수천만 라인의 복잡한 코드베이스를 가진 안드로이드/리눅스 등 범용 리치 OS(REE)는 커널 취약점 공격으로 루트(Root) 권한이 탈취될 위험이 상존하며, OS 커널이 장악될 경우 소프트웨어 기반 샌드박스가 무력화되어 메모리 내 생체 인증 템플릿과 마스터 결제 암호키가 평문 유출되는 치명적 결함이 발생함에 따라, ARMv8-A 및 GlobalPlatform TEE 표준에 기반하여 단일 프로세서 코어와 AXI 시스템 버스를 NS(Non-Secure) 비트 신호로 하드웨어 격리하고, 최상위 EL3 보안 모니터(Secure Monitor), TZASC(메모리 공간 제어기) 및 TZPC(주변장치 제어기)를 결합하는 ARM TrustZone 아키텍처를 도입하여 **범용 OS 침해 시에도 안전한 보안 세계(Secure World / TEE) 격리, 고성능 생체/결제 암호 연산 보증 및 TCB(최소 신뢰 기반) 극소화**를 달성할 필요

#### 한줄 요약
- 단일 CPU와 AXI 버스를 NS 비트와 EL3 모니터로 분할하여 일반 세계와 격리된 하드웨어 TEE를 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ARM TrustZone 핵심 3대 제어 요소**:
  - **AXI Bus NS 비트 (Non-Secure Bit)**: 프로세서가 메모리나 주변장치에 접근할 때 버스 트랜잭션에 실리는 제어 신호 (`NS=0`: 보안 세계 접근, `NS=1`: 일반 세계 접근).
  - **Secure Monitor (EL3)**: SMC(Secure Monitor Call) 인스트럭션을 수신하여 두 세계 간 레지스터를 백업/복원하고 컨텍스트 스위칭을 관장하는 최상위 특권 계층.
  - **TZASC & TZPC**: DRAM 메모리 영역별 접근 권한(TZASC)과 하드웨어 주변장치(지문 센서, 암호 가속기 등)의 보안 전용 여부(TZPC)를 하드웨어적으로 통제하는 컨트롤러.

</details>

- **하드웨어 버스 레벨의 완벽한 물리적 신호 차단**: 일반 세계(NS=1)에서 보안 메모리 영역으로의 읽기/쓰기 시도 시 AXI 버스 레벨에서 즉각 하드웨어 버스 에러(Decode Error)를 발생시켜 차단
- **최소 신뢰 기반(TCB: Trusted Computing Base) 극소화**: 수천만 줄의 Android 대신 수만 줄 규모의 초소형 보안 마이크로커널(OP-TEE, Trusty)만을 Secure World에 배치하여 공격 표면(Attack Surface) 최소화
- **고성능 대용량 보안 연산 지원**: 전용 보안 칩(SE)과 달리 메인 CPU 코어의 고속 클록과 대용량 DRAM 자원을 그대로 활용하여 안면 인식 딥러닝 및 대용량 4K DRM 복호화 실시간 처리

#### 한줄 요약
- AXI NS 비트 버스 통제, TCB 최소화 마이크로커널, EL3 보안 모니터 컨텍스트 전환, 고성능 TEE 연산을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **ARMv8-A TrustZone 4대 핵심 권한 계층 (Exception Levels)**:
  1. **EL0**: 일반 사용자 앱 (Normal) / 신뢰 애플리케이션 TA (Secure).
  2. **EL1**: 범용 리치 OS 커널(Android/Linux) / 보안 OS(OP-TEE Kernel).
  3. **EL2**: 일반 가상화 하이퍼바이저 (KVM, Xen).
  4. **EL3**: 최상위 보안 모니터 (Secure Monitor Firmware).

</details>

```text
[ARM TrustZone 격리 아키텍처]
├── [1. 일반 세계 (Normal World / REE)]
│   ├── EL0: 일반 앱 (모바일 뱅킹)
│   ├── EL1: 범용 OS 커널 (Linux/Android)
│   └── EL2: 하이퍼바이저 (가상화)
├── [2. 보안 세계 (Secure World / TEE)]
│   ├── EL0: 신뢰 앱 (TA: 생체 인증·서명)
│   └── EL1: 보안 OS (OP-TEE Microkernel)
├── [3. 보안 모니터 계층 (EL3)]
│   └── SMC 수신 및 컨텍스트 스위칭 (NS=0/1)
└── [4. 하드웨어 버스 제어기 (AXI)]
    ├── TZASC (DRAM 메모리 영역 하드웨어 격리)
    └── TZPC (지문 센서·암호 가속기 하드웨어 락)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| **일반 세계 (Normal World)** | 풍부한 UI와 범용 애플리케이션 구동 (Android/Linux, `NS=1`) |
| **보안 세계 (Secure World)** | 마이크로커널 기반 생체 인증, 키 관리, 금융 서명 연산 (`NS=0`) |
| **보안 모니터 (EL3)** | SMC 명령 수신 시 레지스터 백업·복원 및 NS 비트 상태 제어 |
| **TZASC 제어기** | 메인 DRAM을 영역별로 분할하여 일반 세계의 비인가 접근 하드웨어 차단 |
| **TZPC 제어기** | 암호 엔진, 난수 생성기, 보안 디스플레이 등 주변장치 독점 제어 |

#### 한줄 요약
- 별도 보안 칩을 두는 대신 같은 CPU와 AXI 버스에 NS 비트를 끼워 넣어 격리를 만들므로, 신뢰의 근거는 물리적 분리가 아니라 EL3만 그 비트를 바꿀 수 있다는 권한 독점과 TZASC·TZPC의 버스 단계 필터링에 놓인다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **TrustZone 보안 연산 5단계 실행 시퀀스**:
  1. 일반 앱이 TEE Client API를 통해 생체 인증/결제 서명 요청
  2. 일반 OS 커널 드라이버가 SMC(Secure Monitor Call) 인스트럭션 실행
  3. EL3 보안 모니터가 일반 세계 상태를 저장하고 CPU를 보안 세계(`NS=0`)로 전환
  4. Secure OS 상의 신뢰 애플리케이션(TA)이 보안 메모리 및 하드웨어 암호 가속기 연산 수행
  5. 연산 완료 후 EL3 모니터를 통해 일반 세계로 결과 코드만을 반환하고 복귀

</details>

```text
1. [서비스 요청] 일반 뱅킹 앱 ➔ 지문 인증을 위해 TEE Client API(`TEEC_InvokeCommand`) 호출
            │
            ▼
2. [SMC 예외 발생]
    ├─ Linux 커널 내 TEE 드라이버가 CPU `SMC` 인스트럭션 실행
    └─ [하드웨어 트랩 발생 ➔ CPU 실행 모드가 EL1(Normal)에서 EL3(Monitor)로 진입]
            │
            ▼
3. [세계 전환 (Context Switching)]
    ├─ 보안 모니터가 일반 세계의 범용 레지스터(X0~X30) 상태를 보안 메모리에 백업
    └─ [AXI 버스 제어 신호를 `NS=0`(보안)으로 설정 ➔ EL1(Secure OS)으로 분기]
            │
            ▼
4. [보안 연산 수행]
    ├─ OP-TEE 커널이 지문 인증 신뢰 앱(TA: Trusted App) 로드
    ├─ TZPC를 통해 지문 센서 SPI 통신 독점 및 템플릿 매칭 수행
    └─ [보안 DRAM 내 마스터 서명키로 결제 토큰 디지털 서명 생성 완료]
            │
            ▼
5. [결과 반환 및 복귀]
    ├─ TA가 `SMC` 명령으로 보안 모니터에 성공 결과 코드(OK) 전달
    ├─ 보안 모니터가 일반 세계 레지스터 복원 및 `NS=1` 전환
    └─ [Android 커널 ➔ 뱅킹 앱으로 서명된 결제 토큰만을 안전하게 전달]
```

**동작 원리**

1. **하드웨어 레벨 인터럽트 격리**: 보안 세계 인터럽트(FIQ)를 일반 세계 인터럽트(IRQ)보다 우선 처리하여 선점 방지
2. **원자적 컨텍스트 전환**: EL3 펌웨어가 중간 상태의 누출 없이 CPU 파이프라인과 캐시를 안전하게 분리
3. **공유 메모리 간접 통신**: 일반 세계와 보안 세계는 물리적 공유 메모리 버퍼를 통해 파라미터만 교환하고 코드는 완전 격리
4. **주변장치 탈취 원천 차단**: 결제 비밀번호 입력 시 TZPC가 터치스크린과 키패드를 보안 세계로 전환하여 화면 캡처 스파이웨어 무력화
5. **독립된 런타임 수명주기**: Android가 다운되거나 크래시되어도 Secure World는 독립적으로 동작하여 암호키 손상 방지

#### 한줄 요약
- 세계 전환마다 컨텍스트 저장·복원 비용이 붙으므로, 보안 세계에는 호출 빈도가 낮고 가치가 높은 키 연산만 남기는 것이 TEE 설계의 기준이 된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **하드웨어 보안 3대 아키텍처 비교**:
  - ARM TrustZone (TEE): 메인 SoC 내부의 하드웨어 버스/코어 논리적 격리 (고성능/대용량).
  - Secure Element (SE): 물리적으로 완전히 독립된 전용 보안 칩셋 (스마트카드급 초고도 탬퍼 방어).
  - 범용 소프트웨어 격리: 일반 OS 내 프로세스 샌드박스 및 가상화 (저비용/낮은 보안성).

</details>

| 비교 항목 | ARM TrustZone (TEE) | 보안 요소 (Secure Element, SE) | 범용 소프트웨어 격리 (OS App) |
|:---|:---|:---|:---|
| **하드웨어 형태** | **메인 AP 칩셋 내 하드웨어 논리적 분할** | **독립된 물리적 전용 보안 칩 (eSIM, eSE)**| 메인보드 및 OS 공유 (소프트웨어 전용) |
| **격리 수준** | **AXI 버스 NS 비트 및 EL3 모니터 격리** | **물리적 차폐 및 전용 버스 (HW 완전 분리)**| OS 커널 권한 기반 프로세스 격리 |
| **연산/메모리 성능**| **매우 높음 (GHz급 CPU, 수백 MB DRAM)** | 매우 낮음 (수십 MHz, 수백 KB EEPROM) | 매우 높음 (제한 없음) |
| **물리 공격 저항성**| 중간 (결함 주입 및 부채널 공격 노출 가능)| **최상 (레이저 글리치, DPA 전력 분석 방어)**| 없음 (메모리 덤프 취약) |
| **주요 적용 분야** | **생체인증, 4K DRM, 안면인식, TEE 지갑**| **금융 IC카드, USIM, 하드웨어 암호화폐 지갑**| 일반 비민감 데이터 암호화 |

#### 한줄 요약
- SE는 물리적 칩 격리로 최고 물리 보안을, TrustZone은 고성능 연산과 하드웨어 격리의 최적 균형을 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **GlobalPlatform TEE 규격 및 TCB (Trusted Computing Base)**: 신뢰 실행 환경의 API 표준 및 보안 세계 내 신뢰 기반 코드베이스.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Secure OS 내부에 복잡한 서드파티 라이브러리를 탑재하여 **TCB가 비대화되고 신뢰 앱(TA) 취약점으로 인한 Secure World 탈옥(Exploit) 발생** | **GlobalPlatform 표준 준수, Secure OS를 초소형 마이크로커널로 경량화하고 필수 암호 연산 TA만 엄격히 화이트리스트 배포** | 보안 세계 내 공격 표면(Attack Surface) 90% 이상 축소 |
| 일반 세계와 보안 세계 간 공유 메모리를 통해 파라미터를 전달할 때 발생하는 **검사 시점과 사용 시점 간의 경쟁 상태(TOCTOU) 공격** | **공유 메모리 버퍼의 데이터를 Secure World 내부 로컬 스택/힙 메모리로 즉각 복사(Double-fetch)한 후 유효성 검증 강제** | 메모리 변조 및 레이스 컨디션 취약점 100% 원천 차단 |
| CPU 투기적 실행(Speculative Execution) 및 캐시 타이밍을 분석하여 **Secure World 내의 마스터 암호키를 추론하는 마이크로아키텍처 부채널 공격** | **세계 전환(SMC) 시 L1/L2 캐시 및 분기 예측기(Branch Predictor) 플러시(Flush) 명령 강제 및 상수 시간(Constant-time) 암호화 구현** | 캐시 기반 사이드채널 정보 유출 및 키 탈취 원천 차단 |

#### 한줄 요약
- TCB 마이크로커널화로 공격 표면을 줄이고, 메모리 로컬 복사로 TOCTOU를 막으며, 캐시 플러시로 부채널 공격을 차단한다.

## Ⅶ. 결론

- 별도의 물리적 보안 칩 추가 없이 메인 SoC 내부에서 범용 OS와 완전히 격리된 고성능 신뢰 실행 환경(TEE)을 구축하는 **하드웨어 기반 시스템 공간 격리 및 프로세서 보안(ARM TrustZone / GlobalPlatform TEE / AXI NS Bit)의 핵심 플랫폼 아키텍처**로 확고히 자리 잡았으며, 모바일 결제, 지문/안면 인식, 스마트카 및 기밀 컴퓨팅(CCA: Realm Management)으로 진화하는 가운데, 실무 TrustZone TEE 시스템 설계 및 TA 개발 시에는 **초소형 마이크로커널(OP-TEE) 채택을 통한 TCB 최소화, 일반 세계와의 공유 메모리 통신 시 Double-fetch 방식을 통한 TOCTOU 경쟁 상태 공격 원천 차단, 세계 전환(SMC) 시 캐시 및 분기 예측기 플러시(Flush)를 통한 마이크로아키텍처 부채널 공격 방어**를 결합하여 완벽한 하드웨어 TEE 무결성을 완성

#### 한줄 요약
- AXI NS 비트와 EL3 모니터 및 TZASC/TZPC 하드웨어 제어를 통해 완벽한 ARM TrustZone TEE를 완성한다.
