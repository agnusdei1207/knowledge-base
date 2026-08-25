---
sidebar:
  order: 64
  label: "064. Arm TrustZone 보안 확장 (Arm TrustZone)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "Arm TrustZone 보안 확장 (Arm TrustZone)"
date: "2026-08-25T10:25:00+09:00"
tags:
  - "notes-hardware"
weight: 64
extra:
  question_no: "064"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "하드웨어 보안 격리와 TEE 신뢰 실행 환경의 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Arm TrustZone**: 프로세서 코어, 메모리, 시스템 버스 및 주변장치를 일반 영역(Normal World)과 보안 영역(Secure World)으로 하드웨어 격리하는 Arm 보안 확장 아키텍처.
- **신뢰 실행 환경(Trusted Execution Environment, TEE)**: 범용 OS와 물리적으로 분리되어 인증, 결제, 암호 키 관리 등 민감 연산을 안전하게 실행하는 하드웨어 보호 영역.

</details>

- 정의/개념: 단일 프로세서와 버스를 보안·비보안 두 상태로 분할해 **신뢰 실행 환경(TEE)**을 구축하는 **Arm TrustZone** 기술
- 배경/필요성: 기존 단일 권한 소프트웨어 구조로는 **범용 OS 침해 시 암호 키 및 기밀 데이터 보호 불가**

#### 한줄 요약
- Arm TrustZone은 하드웨어 버스 레벨에서 Normal World와 Secure World를 격리하여 OS가 해킹되어도 암호 자산을 보호한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **NS(Non-Secure) 비트**: AXI/AMBA 시스템 버스 트랜잭션 신호에 포함되어 현재 접근이 보안 영역인지 비보안 영역인지 하드웨어적으로 판별하는 제어 비트.
- **보안 모니터(Secure Monitor)**: EL3 최고 특권 레벨에서 Secure World와 Normal World 간의 레지스터 문맥 전환을 안전하게 중계하는 펌웨어 계층.

</details>

- 시스템 버스의 **NS 비트**를 통해 메모리 및 주변장치 접근을 하드웨어 레벨에서 통제
- **보안 모니터(Secure Monitor)**를 유일한 전환 관문으로 삼아 두 World 간 안전한 문맥 교환 보장
- Secure World의 신뢰 코드 베이스(TCB)를 최소화하여 공격 표면(Attack Surface) 축소

#### 한줄 요약
- 소프트웨어 권한이 아닌 시스템 버스 트랜잭션 신호로 격리를 강제하므로 상위 OS가 장악되어도 보안 영역은 침범되지 않는다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **TZASC(TrustZone Address Space Controller)**: DRAM 메인 메모리를 보안 영역과 일반 영역으로 동적 분할 보호하는 하드웨어 컨트롤러.
- **TZPC(TrustZone Protection Controller)**: 타이머, 인터럽트 컨트롤러 등 온칩 주변장치의 보안 속성을 제어하는 모듈.

</details>

```text
[Arm TrustZone 하드웨어 격리 구조]
|-- 일반 영역 (Normal World - 비신뢰 환경)
|   |-- 클라이언트 앱 (CA - 안드로이드/리눅스 앱)
|   `-- 범용 OS (Rich OS - Android, Linux)
|-- 보안 모니터 (EL3 최고 특권 레벨 - 안전한 문맥 전환 중계)
|-- 보안 영역 (Secure World - 신뢰 환경, TEE)
|   |-- 신뢰 앱 (TA - 결제·생체인증·DRM·키 관리)
|   `-- 신뢰 OS (Trusted OS - OP-TEE 등)
`-- 시스템 버스 보호 하드웨어
    |-- TZASC (메모리 영역 보안 격리 컨트롤러)
    `-- TZPC (온칩 주변장치 보안 잠금 컨트롤러)
```

선의 의미: 계층 및 하드웨어 보안 경계

| 구성요소 | 책임 |
|:---|:---|
| 일반 영역 (Normal World) | 범용 OS 및 일반 앱 구동 환경 |
| 보안 영역 (Secure World) | 경량 Trusted OS가 암호 키, 결제, 생체 정보 등 기밀 자산 처리 |
| **보안 모니터** | SMC(Secure Monitor Call) 호출 시 레지스터 정화 및 두 World 간 안전한 문맥 전환 |
| **TZASC** | DRAM 주소 공간을 보안/비보안으로 분할하여 Normal World의 무단 접근 차단 |
| **TZPC** | 암호 엔진, 보안 타이머 등 온칩 주변장치를 Secure World 전용으로 잠금 제어 |

#### 한줄 요약
- Normal World, Secure World, 보안 모니터 및 TZASC/TZPC 버스 컨트롤러가 결합된 구조다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SMC(Secure Monitor Call)**: Normal World에서 Secure World의 보안 서비스를 호출하기 위해 하드웨어 트랩을 발생시키는 특권 명령어.

</details>

```text
일반 앱(CA)이 결제·인증 요청 발생
        │
   SMC 명령어로 최고 특권 계층(EL3 보안 모니터)에 트랩
        │
   보안 모니터가 호출 파라미터 유효성을 검증했는가?
   ┌────┴─────┐
아니오          예
   │             │
오류 반환      일반 영역 레지스터 문맥 저장 후 Secure World 진입
   │             │
   │        신뢰 앱(TA)이 보안 메모리와 암호 엔진으로 연산 수행
   │             │
   │        결과 텐서/토큰만 공유 버퍼에 안전하게 기록
   │             │
   │        민감 레지스터 정화(Zeroing) 후 문맥 복원
   └────┬────────┘
        │
   일반 OS로 제어 복귀
```

#### 한줄 요약
- SMC 호출 → 보안 모니터 검증 및 문맥 저장 → Secure World 신뢰 앱 연산 → 레지스터 정화 후 복귀 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Intel SGX**: x86 환경에서 프로세스 메모리 영역을 하드웨어 암호화 엔클레이브(Enclave)로 격리하는 기밀 컴퓨팅 기술.
- **TPM/SE**: 변조 방지(Tamper-Resistant) 물리 보안 칩으로 독립 버스를 통해 암호 키를 안전하게 보관하는 하드웨어 모듈.

</details>

| 하드웨어 보안 격리 기술 | Arm TrustZone | Intel SGX (Enclave) | 하이퍼바이저 가상화 | 하드웨어 보안 칩 (TPM/SE) |
|:---|:---|:---|:---|:---|
| 적용 기준 | 모바일·임베디드·차량용 SoC 전역 보안 | x86 서버 클라우드 기밀 컴퓨팅 | 다중 OS 격리 및 서버 가상화 | 물리적 변조 방지 독립 암호화 모듈 |
| 핵심 특징 | 단일 칩을 2개의 World(Normal/Secure)로 분리 | 프로세스 단위의 암호화 엔클레이브(Enclave) | VM 간 가상 하드웨어 파티셔닝 | 별도의 독립 물리 보안 칩(I2C/SPI 버스) |
| 한계 | Secure World 내부 취약점 시 전체 TEE 장악 | 사이드 채널(Spectre 등) 공격 취약 | 거대한 하이퍼바이저 TCB 및 성능 오버헤드 | 느린 I/O 속도 및 복잡한 연산 처리 불가 |

#### 한줄 요약
- TrustZone은 SoC 전역 하드웨어 격리를 제공하며, 클라우드 Enclave(SGX)나 독립 보안 칩(TPM)과 상호 보완적이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **TOCTOU(Time-of-Check to Time-of-Use)**: 검사 시점과 사용 시점 사이에 악성 일반 OS가 공유 메모리 데이터를 바꿔치기하는 취약점.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공유 버퍼에서 **TOCTOU** 데이터 변조 발생 | 보안 메모리로 1차 복사 후 유효성 검증 수행 | 검사 후 사용 시점 사이의 데이터 변조 차단 |
| 비보안 DMA 장치가 보안 메모리에 우회 접근 | SMMU(System MMU) 및 버스 NS 비트 연동 검증 | DMA 우회 경로를 통한 메모리 탈취 차단 |
| 단일 신뢰 앱(TA) 취약점으로 TEE 전체 탈취 | TA 간 메모리 격리 및 최소 권한 원칙 적용 | 단일 TA 손상 시 피해 전파 억제 |
| 부팅 시점 펌웨어 변조로 보안 영역 무력화 | 하드웨어 RoT 기반 보안 부팅(Secure Boot) 연동 | 변조된 Trusted OS 및 부트로더 실행 원천 차단 |

#### 한줄 요약
- TOCTOU 방지를 위한 보안 메모리 복사, SMMU DMA 통제, 보안 부팅 연동으로 신뢰 실행 환경을 방어한다.

## Ⅶ. 결론

- 모바일·차량용 임베디드 단말은 **Arm TrustZone 기반 TEE**를 구축하고, **하드웨어 보안 부팅(Secure Boot)**과 결합하여 종단 간 보안 체계 완성

#### 한줄 요약
- TrustZone은 시스템 버스 신호 기반의 강력한 물리적 격리를 통해 일반 OS 침해 시에도 핵심 암호 자산을 보호하는 모바일 보안의 핵심 뼈대다.