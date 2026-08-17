---
sidebar:
  order: 64
  label: "064. Arm TrustZone 보안 확장 (Arm TrustZone)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "Arm TrustZone 보안 확장 (Arm TrustZone)"
date: "2026-08-17T16:50:00+09:00"
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

- **Arm TrustZone**: 단일 물리 CPU 및 시스템 버스를 논리적으로 보안(Secure World)과 비보안(Normal World) 영역으로 완전 격리하는 Arm 프로세서 보안 아키텍처.
- **신뢰 실행 환경(TEE, Trusted Execution Environment)**: 결제, 지문 인증, 암호 키 관리 등 최고 수준의 기밀 작업만 전담하는 하드웨어 격리 실행 영역.

</details>

- 정의/개념: 단일 프로세서 코어를 하드웨어적으로 **보안(Secure World)과 비보안(Normal World)** 영역으로 분리하여 신뢰 실행 환경(TEE)을 구축하는 보안 확장 기술
- 배경/필요성: 범용 모바일/임베디드 OS(안드로이드/리눅스)의 권한 탈취 시 **금융 결제 및 암호화 키 유출 위험** 직면

#### 한줄 요약
- 스마트폰이나 임베디드 칩 내부에 해킹 불가능한 '금고 방(Secure World)'을 따로 만들어 중요한 암호와 결제를 지킨다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **NS(Non-Secure) 비트**: AXI/AMBA 시스템 버스 트랜잭션 신호에 포함되어 현재 접근이 보안 영역인지 비보안 영역인지 하드웨어적으로 판별하는 제어 비트.
- **보안 모니터(Secure Monitor)**: EL3 최고 특권 레벨에서 Secure World와 Normal World 간의 레지스터 문맥 전환을 안전하게 중계하는 펌웨어 계층.

</details>

- 시스템 버스 상의 **NS(Non-Secure) 비트** 기반 하드웨어 메모리 및 주변장치 접근 통제
- **SMC(Secure Monitor Call)** 명령어를 통한 안전한 월드 전환 및 레지스터 정화
- 최소 신뢰 기반(TCB, Trusted Computing Base) 축소로 공격 표면(Attack Surface) 최소화

#### 한줄 요약
- 하드웨어 버스 신호(NS-bit)로 메모리와 장치를 물리적으로 차단하고, SMC 명령어로만 출입을 허용한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **TZASC(TrustZone Address Space Controller)**: DRAM 메인 메모리를 보안 영역과 일반 영역으로 동적 분할 보호하는 하드웨어 컨트롤러.
- **TZPC(TrustZone Protection Controller)**: 타이머, 인터럽트 컨트롤러 등 온칩 주변장치의 보안 속성을 제어하는 모듈.

</details>

```text
┌─────────────────────────────────────────────────────────────┐
│ Arm TrustZone 하드웨어 및 소프트웨어 아키텍처              │
│                                                             │
│  [ 일반 영역 (Normal World) ]      [ 보안 영역 (Secure World) ]│
│  ┌────────────────────────┐        ┌──────────────────────┐ │
│  │ Rich OS (Android/Linux)│        │ Trusted OS (OP-TEE)  │ │
│  │ 사용자 애플리케이션    │        │ 신뢰 앱 (TA: 결제/인증)│ │
│  └───────────┬────────────┘        └──────────▲───────────┘ │
│              │ (SMC 명령어 호출)              │             │
│  ┌───────────▼────────────────────────────────┴───────────┐ │
│  │ 보안 모니터 (Secure Monitor @ EL3 / TF-A 펌웨어)       │ │
│  └──────────────────────────┬─────────────────────────────┘ │
│                             ▼                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ AXI 시스템 버스 (NS-bit 전파 및 하드웨어 방화벽)        │ │
│  │  ┌─────────────────────────┐ ┌──────────────────────┐  │ │
│  │  │ TZASC (메모리 DRAM 격리)│ │ TZPC (주변장치 통제) │  │ │
│  │  └─────────────────────────┘ └──────────────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

선의 의미: 일반 영역에서 SMC를 호출하면 보안 모니터가 문맥을 저장하고 AXI 버스 방화벽을 통해 보안 영역 TA를 구동

| 구성요소 | 책임 |
|:---|:---|
| 일반 영역 (Normal World) | 안드로이드/리눅스 등 범용 OS와 일반 앱이 구동되는 비신뢰(Non-secure) 환경 |
| 보안 영역 (Secure World) | 경량 Trusted OS가 실행되며 DRM, 지문 데이터, 암호 키 등 기밀 자산 보호 |
| 보안 모니터 (Secure Monitor) | EL3 레벨에서 월드 전환 시 범용 레지스터를 클리어하고 스택 문맥 교환 수행 |
| 메모리 격리 제어기 (TZASC) | DRAM의 특정 물리 주소 영역을 Secure 전용으로 지정하여 Normal World 접근 차단 |
| 주변장치 제어기 (TZPC) | 암호화 가속기, 난수 발생기(TRNG) 등의 장치를 보안 모드 전용으로 잠금 |

#### 한줄 요약
- 일반 OS, 보안 OS(TEE), 보안 모니터(EL3), TZASC 메모리 방화벽, TZPC 장치 통제기가 하나의 보호 체계를 이룬다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **클라이언트 앱(CA) & 신뢰 앱(TA)**: Normal World의 일반 앱(Client App)이 Secure World의 전용 보안 서비스(Trusted App)를 호출하는 구조.

</details>

```text
일반 앱에서 지문 인증 또는 결제 요청 발생
      │
      ▼
1. TEE 클라이언트 드라이버: 요청 패킷 구성 및 SMC(Secure Monitor Call) 명령어 실행
      │
      ▼
2. 보안 모니터(EL3): CPU 상태를 Secure 모드로 전환하고 Normal World 레지스터 백업
      │
      ▼
3. Trusted OS 디스패치: Secure World의 신뢰 앱(TA)으로 암호화 요청 전달
      │
      ▼
4. 보안 연산 수행: TZASC 보호 메모리 내 마스터 키를 읽어 서명 생성 및 하드웨어 암호화
      │
      ▼
5. 결과 반환: 보안 모니터가 레지스터를 정화(Sanitize) 후 Normal World로 복귀
```

**동작 원리**

1. **보안 서비스 호출**: 안드로이드 결제 앱이 TEE 드라이버를 통해 보안 서비스 호출 요청
2. **트랩 및 모니터 진입**: CPU가 SMC 명령어를 만나면 즉시 최고 특권 EL3 보안 모니터로 트랩
3. **월드 상태 전환**: 모니터가 레지스터를 안전하게 스택에 저장하고 CPU의 NS 비트를 Secure(0)로 전환
4. **신뢰 실행**: Secure World의 TA가 지문 센서(TZPC 통제)를 직접 제어하고 암호 서명 생성
5. **안전한 복귀**: 서명 결과만 공유 버퍼에 담고 CPU 내부의 민감 레지스터를 삭제한 후 일반 OS로 제어권 반환

#### 한줄 요약
- 결제 요청 → SMC 호출 → 보안 모니터 전환 → TEE 신뢰 연산 → 레지스터 정화 및 복귀 순으로 동작한다.

## Ⅴ. 종류 및 비교

| 하드웨어 보안 격리 기술 | Arm TrustZone | Intel SGX (Enclave) | 하이퍼바이저 가상화 | 하드웨어 보안 칩 (TPM/SE) |
|:---|:---|:---|:---|:---|
| 적용 기준 | 모바일·임베디드·차량용 SoC 전역 보안 | x86 서버 클라우드 기밀 컴퓨팅 | 다중 OS 격리 및 서버 가상화 | 물리적 변조 방지 독립 암호화 모듈 |
| 핵심 특징 | 단일 칩을 2개의 World(Normal/Secure)로 분리 | 프로세스 단위의 암호화 엔클레이브(Enclave) | VM 간 가상 하드웨어 파티셔닝 | 별도의 독립 물리 보안 칩(I2C/SPI 버스) |
| 한계 | Secure World 내부 취약점 시 전체 TEE 장악 | 사이드 채널(Spectre 등) 공격 취약 | 거대한 하이퍼바이저 TCB 및 성능 오버헤드 | 느린 I/O 속도 및 복잡한 연산 처리 불가 |

#### 한줄 요약
- 모바일/임베디드는 TrustZone, x86 클라우드는 SGX, 다중 VM은 하이퍼바이저, 독립 물리 칩은 TPM을 쓴다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **TOCTOU(Time-of-Check to Time-of-Use)**: 검사 시점과 사용 시점 사이에 악성 일반 OS가 공유 메모리 데이터를 바꿔치기하는 취약점.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공유 메모리 접근 시 **TOCTOU 경쟁 조건(Race Condition) 공격** | Normal World 버퍼를 Secure World 로컬 메모리로 선 복사 후 유효성 검증 | 데이터 변조 및 메모리 오염 원천 차단 |
| 비보안 DMA 장치에 의한 **보안 DRAM 우회 접근 위험** | **IOMMU/SMMU** 보안 연동 및 DMA 마스터 버스 NS-bit 강제 검증 | 비인가 DMA 탈취 공격 완벽 방어 |
| Secure World 내 취약점으로 인한 **TEE 전체 탈취 위험** | TCB 최소화 원칙 준수 및 서브 파티셔닝(TrustZone-M 등) 적용 | 단일 TA 손상 시에도 커널 및 타 TA 보호 |
| 칩 부팅 시 악성 펌웨어 변조를 통한 **TrustZone 무력화** | **하드웨어 RoT(Root of Trust) 기반 보안 부팅(Secure Boot)** 연동 | 변조 펌웨어 부팅 즉각 차단 |

#### 한줄 요약
- 로컬 선 복사로 TOCTOU를 막고, SMMU로 DMA를 통제하며, 보안 부팅으로 펌웨어 무결성을 검증한다.

## Ⅶ. 결론

- 모바일 기기 및 스마트 전자기기 보안은 **Arm TrustZone 기반 TEE 구축**과 **보안 부팅(Secure Boot)** 의 결합 필수

#### 한줄 요약
- 하드웨어 기반 월드 격리와 최소 신뢰 기반(TCB) 설계를 통해 범용 OS가 해킹당해도 핵심 기밀 자산을 완벽히 수호해야 한다.
